"""Flag strategy v2: how 5-minute flag traders actually trade it (pullback entry, HOD/LOD first target, 9 EMA trail).

Rules fixed before results were seen:
- Trend: 9 EMA above 21 EMA, 21 EMA rising, price above VWAP (bull; mirror for bear).
- Pole: the session high was set 2-12 bars ago, by a push of >= 2x the average 5-min bar range within 6 bars.
- Flag: the pullback since that high retraced 20-62% of the pole, every close stayed above the 21 EMA and VWAP,
  and price came within 0.25 bar-ranges of the 9 EMA.
- Entry: first bar that closes above the prior bar's high (and above the 9 EMA), from 9:45 to 15:00.
- Stop: the flag low. Half off at the session high, then stop to breakeven; runner exits on a close below the 9 EMA
  or at 15:55.
- At most 3 trades a day; stop for the day at -2R.
"""
import os
import sys

import numpy as np
import pandas as pd

from flag_backtest import load

R = dict(pole_min_atr=2.0, pole_max_bars=6, flag_min=2, flag_max=12, retrace_min=0.20, retrace_max=0.62,
         ema_touch_atr=0.25, min_room_r=0.5, first_bar=3, last_entry="15:00", max_trades=3, max_loss_r=-2.0,
         cost_pct=0.0002)


def setup_at(df, t, side):
    c, p = df.iloc[t], df.iloc[t - 1]
    if np.isnan(c.atr):
        return None
    trend = (p.ema9 > p.ema21 and df.ema21.iloc[t - 1] > df.ema21.iloc[t - 4]) if side > 0 else \
            (p.ema9 < p.ema21 and df.ema21.iloc[t - 1] < df.ema21.iloc[t - 4])
    if not trend:
        return None
    day_start = t - int(c.bar)
    for k in range(R["flag_min"], R["flag_max"] + 1):
        x = t - k  # extreme bar
        if x <= day_start:
            break
        ext = df.high.iloc[x] if side > 0 else df.low.iloc[x]
        sess_ext = df.sess_hi.iloc[t - 1] if side > 0 else df.sess_lo.iloc[t - 1]
        if ext != sess_ext:
            continue
        lo = max(day_start, x - R["pole_max_bars"])
        pole_start = df.low.iloc[lo:x + 1].min() if side > 0 else df.high.iloc[lo:x + 1].max()
        height = (ext - pole_start) * side
        if height < R["pole_min_atr"] * c.atr:
            return None
        flag = df.iloc[x + 1:t]
        f_ext = flag.low.min() if side > 0 else flag.high.max()
        retr = (ext - f_ext) * side / height
        if not (R["retrace_min"] <= retr <= R["retrace_max"]):
            return None
        held = ((flag.close > flag.ema21) & (flag.close > flag.vwap)).all() if side > 0 else \
               ((flag.close < flag.ema21) & (flag.close < flag.vwap)).all()
        near9 = ((flag.low - flag.ema9) <= R["ema_touch_atr"] * c.atr).any() if side > 0 else \
                ((flag.ema9 - flag.high) <= R["ema_touch_atr"] * c.atr).any()
        trigger = (c.close > p.high and c.close > c.ema9) if side > 0 else (c.close < p.low and c.close < c.ema9)
        if held and near9 and trigger:
            return dict(stop=f_ext, t1=ext)
        return None
    return None


def run(df):
    trades, n, t = [], len(df), 25
    cur, cnt, dayr = None, 0, 0.0
    while t < n - 1:
        c = df.iloc[t]
        if c.day != cur:
            cur, cnt, dayr = c.day, 0, 0.0
        if c.bar < R["first_bar"] or c.ts.strftime("%H:%M") > R["last_entry"] or cnt >= R["max_trades"] or dayr <= R["max_loss_r"]:
            t += 1
            continue
        side, s = 0, None
        for sd in (1, -1):
            s = setup_at(df, t, sd)
            if s:
                side = sd
                break
        if not s:
            t += 1
            continue
        e = c.close
        risk = (e - s["stop"]) * side
        room = (s["t1"] - e) * side
        if risk <= 0 or room < R["min_room_r"] * risk:
            t += 1
            continue
        stop, half_done, realized, j, how = s["stop"], False, 0.0, t + 1, "close"
        exit_px = None
        while j < n and df.day.iloc[j] == c.day:
            b = df.iloc[j]
            if (side > 0 and b.low <= stop) or (side < 0 and b.high >= stop):
                exit_px, how = stop, ("stop" if not half_done else "breakeven")
                break
            if not half_done and ((side > 0 and b.high >= s["t1"]) or (side < 0 and b.low <= s["t1"])):
                realized, half_done, stop = 0.5 * (s["t1"] - e) * side, True, e
            if half_done and ((side > 0 and b.close < b.ema9) or (side < 0 and b.close > b.ema9)):
                exit_px, how = b.close, "trail"
                break
            if b.ts.strftime("%H:%M") >= "15:55":
                exit_px, how = b.close, "close"
                break
            j += 1
        if exit_px is None:
            j -= 1
            exit_px = df.close.iloc[j]
        rest = 0.5 if half_done else 1.0
        pnl = realized + rest * (exit_px - e) * side - R["cost_pct"] * e
        r = pnl / risk
        trades.append(dict(ts=c.ts, side="BULL" if side > 0 else "BEAR", entry=e, stop=s["stop"], t1=s["t1"],
                           exit=exit_px, how=how, half=half_done, r=r, ret_pct=pnl / e * 100, risk_pct=risk / e * 100))
        cnt += 1
        dayr += r
        t = j + 1
    return pd.DataFrame(trades)


def summary(tr, label):
    if tr.empty:
        print(f"{label}: no trades")
        return
    w, l = tr[tr.r > 0].r.sum(), -tr[tr.r <= 0].r.sum()
    print(f"{label:16s} n={len(tr):4d} ({len(tr) / tr.ts.dt.date.nunique():.1f}/active day) win={(tr.r > 0).mean() * 100:4.1f}% "
          f"avgR={tr.r.mean():+.3f} totalR={tr.r.sum():+6.1f} PF={w / l if l else np.inf:4.2f} "
          f"avg_ret={tr.ret_pct.mean():+.3f}% hit_T1={tr.half.mean() * 100:3.0f}% stopped={(tr.how == 'stop').mean() * 100:3.0f}%")


def placebo(df, tr, runs=200, seed=5):
    """Same trades per day and direction, entered on a random bar; same stop distance in %, same 1R-ish T1, same trail."""
    rng = np.random.default_rng(seed)
    days = {d: g.index for d, g in df.groupby("day")}
    means = []
    for _ in range(runs):
        rs = []
        for _, x in tr.iterrows():
            idx = days[x.ts.date()]
            ok = [i for i in idx if df.bar[i] >= R["first_bar"] and df.ts[i].strftime("%H:%M") <= R["last_entry"]]
            i = ok[rng.integers(0, len(ok))]
            side = 1 if x.side == "BULL" else -1
            e = df.close[i]
            risk = x.risk_pct / 100 * e
            t1 = e + side * abs(x.t1 - x.entry) / x.entry * e
            stop, half, real, ex = e - side * risk, False, 0.0, None
            for j in idx[idx > i]:
                b = df.iloc[j]
                if (side > 0 and b.low <= stop) or (side < 0 and b.high >= stop):
                    ex = stop
                    break
                if not half and ((side > 0 and b.high >= t1) or (side < 0 and b.low <= t1)):
                    real, half, stop = 0.5 * (t1 - e) * side, True, e
                if half and ((side > 0 and b.close < b.ema9) or (side < 0 and b.close > b.ema9)):
                    ex = b.close
                    break
            if ex is None:
                ex = df.close[idx[-1]]
            rs.append((real + (0.5 if half else 1) * (ex - e) * side - R["cost_pct"] * e) / risk)
        means.append(np.mean(rs))
    return np.array(means)


if __name__ == "__main__":
    for sym in sys.argv[1:] or ["QQQ", "SPY"]:
        df = load(sym)
        tr = run(df)
        print(f"\n===== {sym} v2: {df.day.nunique()} sessions =====")
        summary(tr, "ALL")
        if tr.empty:
            continue
        for sd in ("BULL", "BEAR"):
            summary(tr[tr.side == sd], sd)
        mid = pd.Timestamp("2026-06-30", tz="America/New_York")
        summary(tr[tr.ts <= mid], "Feb-Jun")
        summary(tr[tr.ts > mid], "Jul-Oct")
        summary(tr[tr.ts.dt.hour < 12], "before noon")
        summary(tr[tr.ts.dt.hour >= 12], "after noon")
        print("   exits:", tr.how.value_counts().to_dict(), " avg risk", round(tr.risk_pct.mean(), 3), "%")
        pl = placebo(df, tr)
        print(f"   random-entry placebo avgR {pl.mean():+.3f} (95th pct {np.percentile(pl, 95):+.3f}); "
              f"real avgR {tr.r.mean():+.3f} beats {(pl < tr.r.mean()).mean() * 100:.0f}% of placebo runs")
        tr.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"trades_v2_{sym}.csv"), index=False)
