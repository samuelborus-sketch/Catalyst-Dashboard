"""Robustness: real ETF prices, untouched markets (IWM/DIA), cost stress, bootstrap, rolling windows."""
from dataclasses import replace

import numpy as np
import pandas as pd

from backtest import Params, benchmark, decide, load_frames, metrics, simulate
from explore import lev_day
from features import build, load

P = Params()
SPY, QQQ = load_frames()
DEC = decide(SPY, QQQ, P)
TR, EQ = simulate(SPY, QQQ, DEC, P)
ETF = {("SPY", 1): "SPXL", ("SPY", -1): "SPXS", ("QQQ", 1): "TQQQ", ("QQQ", -1): "SQQQ"}


def real_etf_check():
    """Re-price every trade since TQQQ/SQQQ launched with the actual fund's own open/low/close."""
    px = {s: load(s) for s in ETF.values()}
    t = TR[(TR["exit"] != "WEEK_LOCKED") & (TR["date"] >= "2010-02-12")].copy()
    real = []
    for _, r in t.iterrows():
        e = px[ETF[(r.family, r.side)]].loc[r.date]
        if e["low"] / e["open"] - 1 <= P.daily_stop:
            real.append(P.daily_stop - P.stop_slip - P.cost)
        else:
            real.append(e["close"] / e["open"] - 1 - P.cost)
    t["real"] = real
    yrs = (t["date"].iloc[-1] - t["date"].iloc[0]).days / 365.25
    out = dict(trades=len(t),
               model_cagr=(np.exp(np.log1p(t["ret"]).sum() / yrs) - 1) * 100,
               real_cagr=(np.exp(np.log1p(t["real"]).sum() / yrs) - 1) * 100,
               corr=float(np.corrcoef(t["ret"], t["real"])[0, 1]),
               by_signal={s: (g.ret.mean() * 100, g.real.mean() * 100, len(g)) for s, g in t.groupby("signal")})
    return out


def market_test(sym):
    """Each signal on an index never used in development, trading its own synthetic 3x."""
    f = build(sym)
    f["bull"] = lev_day(f, 3)
    f["bear"] = lev_day(f, -3)
    f = f.iloc[1:]
    sigs = {
        "Opex fade": ((f["opex"] == 1) & (f["r_co"] >= P.opex_skip_gap_down), "bear"),
        "Month start": ((f["tdom"] <= P.tom_days) & f["rv20"].between(P.tom_min_rv20, P.tom_max_rv20), "bull"),
        "Dip bounce": ((f["dn_streak"] >= P.dip_streak) & (f["r_co"] <= P.dip_max_gap), "bull"),
        "3x long every day": (pd.Series(True, index=f.index), "bull"),
        "3x short every day": (pd.Series(True, index=f.index), "bear"),
    }
    out = {}
    for name, (m, col) in sigs.items():
        cells = []
        for per in (f["year"] <= 2012, f["year"] > 2012):
            x = np.log1p(f.loc[m & per, col])
            cells.append(dict(n=len(x), avg_pct=(np.exp(x.mean()) - 1) * 100, win=(x > 0).mean() * 100))
        out[name] = cells
    return out


def playbook_on(sym_bull, sym_bear):
    """Whole playbook re-run with another index in place of SPY (longs) and QQQ (opex short)."""
    a, b = build(sym_bull), build(sym_bear)
    common = a.index.intersection(b.index)
    a, b = a.loc[common], b.loc[common]
    dec = decide(a, b, P)
    tr, eq = simulate(a, b, dec, P)
    return metrics(eq, tr), metrics(benchmark(sym_bull, str(eq.index[0].date())))


STRESS = (
    ("Base case: 0.05% costs, 0.25% stop slippage", P),
    ("Costs doubled to 0.10% a trade", replace(P, cost=0.0008)),
    ("Costs tripled to 0.15% a trade", replace(P, cost=0.0013)),
    ("Stops fill 1% worse", replace(P, stop_slip=0.01)),
    ("Stops fill 2% worse", replace(P, stop_slip=0.02)),
    ("0.10% costs and stops 1% worse", replace(P, cost=0.0008, stop_slip=0.01)),
    ("Without the weekly −10% lock", replace(P, weekly_stop=-0.99)),
    ("Without the daily −5% stop", replace(P, daily_stop=-0.99)),
    ("Without either risk rule", replace(P, daily_stop=-0.99, weekly_stop=-0.99)),
)


def stress():
    rows = []
    for lab, p in STRESS:
        dec = decide(SPY, QQQ, p)
        tr, eq = simulate(SPY, QQQ, dec, p)
        m = metrics(eq, tr)
        rows.append(dict(label=lab, cagr=m["cagr"], dd=m["max_dd"], end=10000 * m["total_x"], sharpe=m["sharpe"]))
    return rows


def bootstrap(n=5000, seed=7, hurdle=0.083):
    """Monthly block bootstrap of daily strategy returns: a luck check, not an overfitting check."""
    r = EQ.pct_change().fillna(0)
    months = [g.values for _, g in r.groupby(r.index.to_period("M"))]
    rng = np.random.default_rng(seed)
    yrs = len(r) / 252
    cagr, mdd = [], []
    for _ in range(n):
        pick = rng.integers(0, len(months), len(months))
        path = np.cumprod(1 + np.concatenate([months[i] for i in pick]))
        cagr.append(path[-1] ** (1 / yrs) - 1)
        mdd.append((path / np.maximum.accumulate(path) - 1).min())
    cagr, mdd = np.array(cagr), np.array(mdd)
    return dict(n=n, p5=np.percentile(cagr, 5) * 100, p50=np.percentile(cagr, 50) * 100, p95=np.percentile(cagr, 95) * 100,
                below_hurdle=np.mean(cagr < hurdle) * 100, dd_p50=np.percentile(mdd, 50) * 100, dd_p5=np.percentile(mdd, 5) * 100,
                dd_worse_40=np.mean(mdd < -0.40) * 100, dd_worse_50=np.mean(mdd < -0.50) * 100)


def rolling(years=5):
    b = benchmark("SPY")
    rows = []
    for end in range(2000 + years, 2027):
        s = pd.Timestamp(f"{end - years}-01-01")
        e = pd.Timestamp(f"{end}-01-01") if end < 2026 else EQ.index[-1]
        q = EQ[(EQ.index >= s) & (EQ.index <= e)]
        bb = b[(b.index >= s) & (b.index <= e)]
        yrs = (q.index[-1] - q.index[0]).days / 365.25
        rows.append(dict(start=end - years, end=min(end, 2026),
                         strat=((q.iloc[-1] / q.iloc[0]) ** (1 / yrs) - 1) * 100,
                         spy=((bb.iloc[-1] / bb.iloc[0]) ** (1 / yrs) - 1) * 100))
    return rows


def extreme_days():
    days = ["2008-10-10", "2010-05-06", "2010-05-07", "2011-08-08", "2015-08-24", "2018-02-05", "2020-03-16",
            "2020-03-20", "2024-08-05", "2025-04-03", "2025-04-07", "2025-04-09"]
    t = TR.set_index("date")
    out = []
    for d in days:
        d = pd.Timestamp(d)
        if d in t.index:
            r = t.loc[d]
            out.append(f"{d.date()} {r.signal} {'BULL' if r.side > 0 else 'BEAR'} {r.family} ret={r.ret * 100:+.2f}% {r.exit}")
        else:
            out.append(f"{d.date()} flat")
    return out


if __name__ == "__main__":
    print("[1] real ETF check:", real_etf_check())
    for s in ("IWM", "DIA"):
        print(f"[2] {s}:", {k: [(round(c['avg_pct'], 2), c['n']) for c in v] for k, v in market_test(s).items()})
    for pair in (("IWM", "IWM"), ("DIA", "DIA"), ("DIA", "IWM")):
        m, bh = playbook_on(*pair)
        print(f"[2b] playbook on {pair}: cagr={m['cagr']} dd={m['max_dd']} | B&H cagr={bh['cagr']} dd={bh['max_dd']}")
    for r in stress():
        print("[3]", r)
    print("[4] bootstrap:", {k: round(v, 2) for k, v in bootstrap().items()})
    for r in rolling():
        print("[5]", {k: round(v, 1) if isinstance(v, float) else v for k, v in r.items()})
    print("[6]", *extreme_days(), sep="\n    ")
