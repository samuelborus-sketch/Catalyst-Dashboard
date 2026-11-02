"""Backtest of the 5-minute bull/bear flag strategy (9/21 EMA + VWAP, target = session high/low).

Rules are fixed in RULES before any results were seen; see the PDF "Claude agent bull/bear flag EMA VWAP strategy".
Results are in R: profit or loss divided by the distance from entry to the stop.
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RULES = dict(
    pole_bars=3,             # impulse leg length
    pole_min_atr=3.0,        # pole net move >= 3x the average 5-min bar range (prior 20 bars)
    flag_min=3, flag_max=15,  # flag length in bars
    flag_max_frac=0.5,       # flag range <= 50% of pole height
    min_reward_r=1.0,        # skip if session high/low is less than 1R away
    no_trade_first_bars=3,   # nothing before 9:45
    last_entry="15:00",
    max_trades_day=3, max_loss_r_day=-2.0,
    cost_pct=0.0002,         # round-trip spread/slippage on the ETF, as a fraction of price
)


def load(sym):
    df = pd.read_csv(os.path.join(HERE, "data", f"{sym}_5min.csv"))
    df["ts"] = pd.to_datetime(df["ts"], utc=True).dt.tz_convert("America/New_York")
    df["day"] = df["ts"].dt.date
    df["ema9"] = df["close"].ewm(span=9, adjust=False).mean()
    df["ema21"] = df["close"].ewm(span=21, adjust=False).mean()
    tp = (df["high"] + df["low"] + df["close"]) / 3
    df["vwap"] = (tp * df["volume"]).groupby(df["day"]).cumsum() / df["volume"].groupby(df["day"]).cumsum()
    df["atr"] = (df["high"] - df["low"]).rolling(20).mean().shift(1)
    df["sess_hi"] = df.groupby("day")["high"].cummax()
    df["sess_lo"] = df.groupby("day")["low"].cummin()
    df["bar"] = df.groupby("day").cumcount()
    return df.reset_index(drop=True)


def find_setup(df, t, side, R):
    """Return (flag_hi, flag_lo) if bar t is a valid breakout from a flag, else None."""
    c = df.iloc[t]
    p = df.iloc[t - 1]
    if side > 0:
        if not (p.ema9 > p.ema21 and df.ema21.iloc[t - 1] >= df.ema21.iloc[t - 4]):
            return None
        if not (c.close > c.ema9 and c.close > c.vwap):
            return None
    else:
        if not (p.ema9 < p.ema21 and df.ema21.iloc[t - 1] <= df.ema21.iloc[t - 4]):
            return None
        if not (c.close < c.ema9 and c.close < c.vwap):
            return None
    if c.high - c.low < c.atr:  # breakout candle must expand
        return None
    for k in range(R["flag_min"], R["flag_max"] + 1):
        fs, fe = t - k, t - 1
        ps, pe = fs - R["pole_bars"], fs - 1
        if ps < 0 or df.day.iloc[ps] != c.day:
            break
        flag, pole = df.iloc[fs:fe + 1], df.iloc[ps:pe + 1]
        f_hi, f_lo = flag.high.max(), flag.low.min()
        p_hi, p_lo = pole.high.max(), pole.low.min()
        height = p_hi - p_lo
        if side > 0:
            move = pole.close.iloc[-1] - pole.open.iloc[0]
            ok = (move >= R["pole_min_atr"] * c.atr and (pole.close > pole.open).sum() >= 2
                  and f_hi <= p_hi and f_hi - f_lo <= R["flag_max_frac"] * height
                  and (flag.close > flag.vwap).all() and c.close > f_hi)
        else:
            move = pole.open.iloc[0] - pole.close.iloc[-1]
            ok = (move >= R["pole_min_atr"] * c.atr and (pole.close < pole.open).sum() >= 2
                  and f_lo >= p_lo and f_hi - f_lo <= R["flag_max_frac"] * height
                  and (flag.close < flag.vwap).all() and c.close < f_lo)
        if ok:
            return f_hi, f_lo
    return None


def run(df, R=RULES, entry="breakout"):
    trades = []
    t, n = 25, len(df)
    day_trades, day_r, cur_day = 0, 0.0, None
    while t < n - 1:
        c = df.iloc[t]
        if c.day != cur_day:
            cur_day, day_trades, day_r = c.day, 0, 0.0
        if (c.bar < R["no_trade_first_bars"] or c.ts.strftime("%H:%M") > R["last_entry"]
                or day_trades >= R["max_trades_day"] or day_r <= R["max_loss_r_day"] or np.isnan(c.atr)):
            t += 1
            continue
        setup, side = None, 0
        for s in (1, -1):
            setup = find_setup(df, t, s, R)
            if setup:
                side = s
                break
        if not setup:
            t += 1
            continue
        f_hi, f_lo = setup
        # session extreme before the breakout bar is the target
        target = df.sess_hi.iloc[t - 1] if side > 0 else df.sess_lo.iloc[t - 1]
        stop = f_lo if side > 0 else f_hi
        e_idx = t
        entry_px = c.close
        if entry == "retest":
            level = f_hi if side > 0 else f_lo
            e_idx = None
            for j in range(t + 1, min(t + 7, n)):
                b = df.iloc[j]
                if b.day != c.day:
                    break
                if (side > 0 and b.low <= stop) or (side < 0 and b.high >= stop):
                    break
                if (side > 0 and b.low <= level and b.close > level) or (side < 0 and b.high >= level and b.close < level):
                    e_idx, entry_px = j, b.close
                    break
            if e_idx is None:
                t += 1
                continue
        risk = (entry_px - stop) * side
        reward = (target - entry_px) * side
        if risk <= 0 or reward < R["min_reward_r"] * risk:
            t += 1
            continue
        exit_px, how, j = None, None, e_idx + 1
        while j < n and df.day.iloc[j] == c.day:
            b = df.iloc[j]
            hit_stop = b.low <= stop if side > 0 else b.high >= stop
            hit_tgt = b.high >= target if side > 0 else b.low <= target
            if hit_stop:
                exit_px, how = stop, "stop"
                break
            if hit_tgt:
                exit_px, how = target, "target"
                break
            inval = (b.close < b.ema21 or b.close < b.vwap) if side > 0 else (b.close > b.ema21 or b.close > b.vwap)
            if inval:
                exit_px, how = b.close, "invalidated"
                break
            if b.ts.strftime("%H:%M") >= "15:55":
                exit_px, how = b.close, "close"
                break
            j += 1
        if exit_px is None:
            j -= 1
            exit_px, how = df.close.iloc[j], "close"
        pnl = (exit_px - entry_px) * side - R["cost_pct"] * entry_px
        r = pnl / risk
        trades.append(dict(ts=df.ts.iloc[e_idx], side="BULL" if side > 0 else "BEAR", entry=entry_px, stop=stop,
                           target=target, exit=exit_px, how=how, r=r, ret_pct=pnl / entry_px * 100,
                           risk_pct=risk / entry_px * 100, reward_r=reward / risk))
        day_trades += 1
        day_r += r
        t = j + 1
    return pd.DataFrame(trades)


def summarize(tr, label):
    if tr.empty:
        print(f"{label}: no trades")
        return
    wins, losses = tr[tr.r > 0].r.sum(), -tr[tr.r <= 0].r.sum()
    days = tr.ts.dt.date.nunique()
    print(f"{label:28s} n={len(tr):4d} win={(tr.r > 0).mean() * 100:4.1f}% avgR={tr.r.mean():+.3f} totalR={tr.r.sum():+7.1f} "
          f"PF={wins / losses if losses else np.inf:4.2f} avg_ret={tr.ret_pct.mean():+.3f}% risk={tr.risk_pct.mean():.2f}% "
          f"target%={(tr.how == 'target').mean() * 100:3.0f} stop%={(tr.how == 'stop').mean() * 100:3.0f}")


def random_baseline(df, tr, seeds=200, R=RULES):
    """Same number of trades per day, same direction, entered at a random eligible bar with the same stop distance and R target."""
    rng = np.random.default_rng(3)
    out = []
    by_day = {d: g for d, g in df.groupby("day")}
    for _ in range(seeds):
        rs = []
        for _, x in tr.iterrows():
            g = by_day[x.ts.date()]
            g = g[(g.bar >= R["no_trade_first_bars"]) & (g.ts.dt.strftime("%H:%M") <= R["last_entry"])]
            i = rng.integers(0, len(g))
            e = g.iloc[i]
            side = 1 if x.side == "BULL" else -1
            risk = x.risk_pct / 100 * e.close
            stop, tgt = e.close - side * risk, e.close + side * x.reward_r * risk
            rest = df.loc[g.index[i] + 1:][df.loc[g.index[i] + 1:].day == e.day]
            px = rest.close.iloc[-1] if len(rest) else e.close
            for _, b in rest.iterrows():
                if (side > 0 and b.low <= stop) or (side < 0 and b.high >= stop):
                    px = stop
                    break
                if (side > 0 and b.high >= tgt) or (side < 0 and b.low <= tgt):
                    px = tgt
                    break
            rs.append(((px - e.close) * side - R["cost_pct"] * e.close) / risk)
        out.append(np.mean(rs))
    return np.array(out)


if __name__ == "__main__":
    syms = sys.argv[1:] or ["QQQ", "SPY"]
    for sym in syms:
        df = load(sym)
        print(f"\n===== {sym}: {df.day.nunique()} sessions {df.day.min()} .. {df.day.max()} =====")
        for entry in ("breakout", "retest"):
            tr = run(df, entry=entry)
            summarize(tr, f"{entry} ALL")
            if tr.empty:
                continue
            for s in ("BULL", "BEAR"):
                summarize(tr[tr.side == s], f"{entry} {s}")
            mid = pd.Timestamp("2026-06-30", tz="America/New_York")
            summarize(tr[tr.ts <= mid], f"{entry} Feb-Jun")
            summarize(tr[tr.ts > mid], f"{entry} Jul-Oct")
            summarize(tr[tr.ts.dt.hour < 12], f"{entry} morning")
            summarize(tr[tr.ts.dt.hour >= 12], f"{entry} afternoon")
            if entry == "breakout":
                tr.to_csv(os.path.join(HERE, f"trades_{sym}.csv"), index=False)
                base = random_baseline(df, tr)
                print(f"   random-entry baseline avgR: mean {base.mean():+.3f}, 95th pct {np.percentile(base, 95):+.3f}; "
                      f"real {tr.r.mean():+.3f} beats {(base < tr.r.mean()).mean() * 100:.0f}% of random runs")
