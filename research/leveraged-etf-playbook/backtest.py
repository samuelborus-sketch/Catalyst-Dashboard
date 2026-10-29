"""Staged daily playbook on 3x leveraged ETFs with 100% sizing, -5% daily and -10% weekly circuit breakers."""
import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

from features import build, load

LEV = 3


@dataclass
class Params:
    # instrument family per signal: "SPY" -> SPXL/SPXS, "QQQ" -> TQQQ/SQQQ
    opex_family: str = "QQQ"
    tom_family: str = "SPY"
    dip_family: str = "SPY"
    # signal switches and filters
    use_opex: bool = True
    use_tom: bool = True
    use_dip: bool = True
    tom_days: int = 3
    tom_min_rv20: float = 0.15        # month-start long only when SPY 20d realized vol >= this
    tom_max_rv20: float = 0.40        # ...and <= this
    dip_streak: int = 3
    dip_max_gap: float = 0.003        # skip the dip long if the open gaps up more than this
    opex_skip_gap_down: float = -0.003  # skip opex short if gap below this (-1 = never skip)
    opex_max_rv20: float = 9.0        # skip opex short if SPY rv20 above this
    max_rv20_all: float = 9.0         # no trades of any kind above this SPY rv20
    # risk rules
    daily_stop: float = -0.05
    weekly_stop: float = -0.10
    # frictions
    drag: float = 0.0002              # measured ETF intraday drag vs 3x model, per trade
    cost: float = 0.0003              # spread/slippage vs official open & close, per round trip
    stop_slip: float = 0.0025         # extra loss when a stop order fills


def load_frames():
    spy = build("SPY")
    qqq = build("QQQ")
    return spy, qqq


def decide(spy, qqq, p: Params):
    """Return per-day (side, family, signal) using only information available at the open."""
    idx = spy.index
    side = pd.Series(0, index=idx)
    fam = pd.Series("", index=idx, dtype=object)
    sig = pd.Series("", index=idx, dtype=object)

    bull = pd.Series(False, index=idx)
    bull_fam = pd.Series("", index=idx, dtype=object)
    bull_sig = pd.Series("", index=idx, dtype=object)
    if p.use_tom:
        m = (spy["tdom"] <= p.tom_days) & (spy["rv20"] >= p.tom_min_rv20) & (spy["rv20"] <= p.tom_max_rv20)
        bull |= m
        bull_fam[m] = p.tom_family
        bull_sig[m] = "MONTH_START"
    if p.use_dip:
        src = spy if p.dip_family == "SPY" else qqq
        m = (src["dn_streak"] >= p.dip_streak) & (src["r_co"] <= p.dip_max_gap)
        bull_fam[m & ~bull] = p.dip_family
        bull_sig[m & ~bull] = "DIP_BOUNCE"
        bull_sig[m & (bull_sig == "MONTH_START")] = "MONTH_START+DIP"
        bull |= m

    bear = pd.Series(False, index=idx)
    if p.use_opex:
        src = spy if p.opex_family == "SPY" else qqq
        bear = (spy["opex"] == 1) & (src["r_co"] >= p.opex_skip_gap_down) & (spy["rv20"] <= p.opex_max_rv20)

    calm_enough = spy["rv20"] <= p.max_rv20_all
    bull &= calm_enough
    bear &= calm_enough
    conflict = bull & bear
    side[bull & ~conflict] = 1
    fam[bull & ~conflict] = bull_fam[bull & ~conflict]
    sig[bull & ~conflict] = bull_sig[bull & ~conflict]
    side[bear & ~conflict] = -1
    fam[bear & ~conflict] = p.opex_family
    sig[bear & ~conflict] = "OPEX_FADE"
    sig[conflict] = "CONFLICT_FLAT"
    return pd.DataFrame({"side": side, "family": fam, "signal": sig})


def simulate(spy, qqq, dec, p: Params, start=None, end=None):
    """Walk forward day by day applying the breakers. Returns (trades, daily equity)."""
    frames = {"SPY": spy, "QQQ": qqq}
    idx = spy.index[1:]
    if start:
        idx = idx[idx >= pd.Timestamp(start)]
    if end:
        idx = idx[idx <= pd.Timestamp(end)]
    eq = 1.0
    week_key = None
    week_start_eq = 1.0
    locked_week = False
    equity = []
    trades = []
    for d in idx:
        wk = d.to_period("W-FRI")
        if wk != week_key:
            week_key, week_start_eq, locked_week = wk, eq, False
        s = dec.at[d, "side"]
        if s == 0 or locked_week:
            equity.append((d, eq))
            if s != 0 and locked_week:
                trades.append(dict(date=d, signal=dec.at[d, "signal"], side=int(s), family=dec.at[d, "family"],
                                   ret=0.0, exit="WEEK_LOCKED", eq_after=eq))
            continue
        f = frames[dec.at[d, "family"]].loc[d]
        lev = LEV * s
        base = 1 + lev * f["r_co"]
        close_v = (1 + lev * f["r_cc"]) / base
        adverse = f["r_lo"] if lev > 0 else f["r_hi"]
        worst_v = (1 + lev * adverse) / base
        # the tighter of the daily breaker and what is left of the weekly breaker
        week_room = (1 + p.weekly_stop) * week_start_eq / eq - 1
        stop = max(p.daily_stop, week_room)
        if worst_v <= 1 + stop:
            r = stop - p.stop_slip - p.cost - p.drag
            how = "STOP_DAILY" if stop == p.daily_stop else "STOP_WEEKLY"
        else:
            r = close_v - 1 - p.cost - p.drag
            how = "CLOSE"
        eq *= 1 + r
        if eq / week_start_eq - 1 <= p.weekly_stop + 1e-12:
            locked_week = True
        trades.append(dict(date=d, signal=dec.at[d, "signal"], side=int(s), family=dec.at[d, "family"],
                           ret=r, exit=how, eq_after=eq, und_oc=f["r_oc"], gap=f["r_co"]))
        equity.append((d, eq))
    eqs = pd.Series(dict(equity))
    return pd.DataFrame(trades), eqs


def metrics(eqs, trades=None, label=""):
    yrs = (eqs.index[-1] - eqs.index[0]).days / 365.25
    total = eqs.iloc[-1] / eqs.iloc[0]
    cagr = total ** (1 / yrs) - 1
    dr = eqs.pct_change().dropna()
    sharpe = dr.mean() / dr.std() * np.sqrt(252) if dr.std() > 0 else np.nan
    dd = (eqs / eqs.cummax() - 1).min()
    out = dict(label=label, start=str(eqs.index[0].date()), end=str(eqs.index[-1].date()),
               total_x=round(total, 2), cagr=round(cagr * 100, 2), max_dd=round(dd * 100, 1), sharpe=round(sharpe, 2))
    if trades is not None and len(trades):
        t = trades[trades["exit"] != "WEEK_LOCKED"]
        wins = t[t["ret"] > 0]["ret"].sum()
        losses = -t[t["ret"] <= 0]["ret"].sum()
        out.update(trades=len(t), per_year=round(len(t) / yrs, 1), win=round((t["ret"] > 0).mean() * 100, 1),
                   pf=round(wins / losses, 2) if losses > 0 else np.inf,
                   avg=round(t["ret"].mean() * 100, 3), stops=int(t["exit"].str.startswith("STOP").sum()),
                   week_locks=int((trades["exit"] == "WEEK_LOCKED").sum()))
    return out


def benchmark(sym="SPY", start=None, end=None, div_yield=0.0):
    c = load(sym)["close"]
    if start:
        c = c[c.index >= pd.Timestamp(start)]
    if end:
        c = c[c.index <= pd.Timestamp(end)]
    r = c.pct_change().fillna(0) + div_yield / 252
    return (1 + r).cumprod()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", nargs="*", default=[], help="override params key=value")
    a = ap.parse_args()
    p = Params()
    for kv in a.set:
        k, v = kv.split("=")
        t = type(getattr(p, k))
        setattr(p, k, (v.lower() in ("1", "true", "yes")) if t is bool else t(v))
    spy, qqq = load_frames()
    dec = decide(spy, qqq, p)
    print(json.dumps(asdict(p)))
    for lab, s, e in (("FULL 2000-2026", None, None), ("IS 2000-2012", None, "2012-12-31"), ("OOS 2013-2026", "2013-01-01", None)):
        tr, eq = simulate(spy, qqq, dec, p, s, e)
        print(metrics(eq, tr, lab))
        print("   SPY B&H price-only:", metrics(benchmark("SPY", s, e), label="spy"))
        if lab.startswith("FULL"):
            yr = eq.groupby(eq.index.year).last() / eq.groupby(eq.index.year).first().shift(1).fillna(1.0)
            first = eq.groupby(eq.index.year).first()
            last = eq.groupby(eq.index.year).last()
            prev = last.shift(1)
            prev.iloc[0] = 1.0
            yr = last / prev - 1
            b = benchmark("SPY")
            bl = b.groupby(b.index.year).last()
            bp = bl.shift(1)
            bp.iloc[0] = b.iloc[0]
            by = bl / bp - 1
            print("   year: strategy% / SPY%")
            print("   " + "  ".join(f"{y}:{yr[y] * 100:+.0f}/{by[y] * 100:+.0f}" for y in yr.index))
            print("   by signal:")
            for sg, g in tr[tr["exit"] != "WEEK_LOCKED"].groupby("signal"):
                print(f"     {sg:16s} n={len(g):4d} win={(g.ret > 0).mean() * 100:4.1f}% avg={g.ret.mean() * 100:+.3f}% "
                      f"logsum={np.log1p(g.ret).sum() * 100:+7.1f}% stops={g.exit.str.startswith('STOP').sum()}")
            print("   conflicts flat:", int((dec["signal"] == "CONFLICT_FLAT").sum()))


if __name__ == "__main__":
    main()
