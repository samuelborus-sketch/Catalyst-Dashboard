"""Exploratory: where do open->close returns lean long or short, and does it hold out of sample?"""
import sys

import numpy as np
import pandas as pd

from features import build

IS_END = 2012
STOP = -0.05
FRICTION = 0.0005  # ETF drag + trading cost per round trip, before stop slippage


def lev_day(f, lev, stop=STOP, friction=FRICTION):
    """Per-day return of a lev-x daily-reset ETF bought at the open and sold at the close or stopped."""
    base = 1 + lev * f["r_co"]
    close_v = (1 + lev * f["r_cc"]) / base
    adverse = f["r_lo"] if lev > 0 else f["r_hi"]
    worst_v = (1 + lev * adverse) / base
    out = np.where(worst_v <= 1 + stop, 1 + stop, close_v) - 1 - friction
    return pd.Series(out, index=f.index)


def stats(x):
    x = x.dropna()
    n = len(x)
    if n < 2:
        return dict(n=n)
    return dict(n=n, mean_bp=x.mean() * 1e4, t=x.mean() / (x.std() / np.sqrt(n)), win=(x > 0).mean() * 100)


def show(f, mask, label):
    rows = []
    for name, period in (("IS", f["year"] <= IS_END), ("OOS", f["year"] > IS_END)):
        m = mask & period
        s = stats(f.loc[m, "r_oc"])
        gb = np.log1p(f.loc[m, "bull"]).mean() * 1e4 if m.sum() else np.nan
        gs = np.log1p(f.loc[m, "bear"]).mean() * 1e4 if m.sum() else np.nan
        rows.append(f"{name}: n={s.get('n',0):4d} oc={s.get('mean_bp',np.nan):+6.1f}bp t={s.get('t',np.nan):+5.2f} win={s.get('win',np.nan):4.1f}% | 3xBull g={gb:+6.1f}bp 3xBear g={gs:+6.1f}bp")
    print(f"{label:34s} " + "  ||  ".join(rows))


def main(sym="SPY"):
    f = build(sym)
    f["bull"] = lev_day(f, 3)
    f["bear"] = lev_day(f, -3)
    f = f.iloc[1:]
    print(f"\n######## {sym} ########")
    print("\nYear: overnight% intraday% | 3x bull every day% 3x bear every day% (stop -5%, 0.05% friction)")
    for y, g in f.groupby("year"):
        on = np.prod(1 + g["r_co"]) - 1
        intra = np.prod(1 + g["r_oc"]) - 1
        b = np.prod(1 + g["bull"]) - 1
        s = np.prod(1 + g["bear"]) - 1
        print(f"  {y}: ON {on*100:+6.1f}  ID {intra*100:+6.1f} | bull {b*100:+7.1f}  bear {s*100:+7.1f}")
    allm = pd.Series(True, index=f.index)
    print("\n--- Conditional open->close (IS=2000-2012, OOS=2013-2026); g = mean daily log growth of 3x position ---")
    show(f, allm, "ALL DAYS")
    show(f, f["above_sma200"] == 1, "above SMA200")
    show(f, f["above_sma200"] == 0, "below SMA200")
    show(f, f["above_sma50"] == 1, "above SMA50")
    show(f, f["above_sma50"] == 0, "below SMA50")
    show(f, f["sma50_gt_sma200"] == 1, "SMA50>SMA200")
    show(f, f["sma50_gt_sma200"] == 0, "SMA50<SMA200")
    for lo, hi in ((0, .12), (.12, .18), (.18, .25), (.25, .35), (.35, 9)):
        show(f, (f["rv20"] >= lo) & (f["rv20"] < hi), f"rv20 {lo:.2f}-{hi:.2f}")
    for lo, hi in ((0, 15), (15, 20), (20, 25), (25, 30), (30, 40), (40, 999)):
        show(f, (f["vix"] >= lo) & (f["vix"] < hi), f"VIX {lo}-{hi}")
    for lo, hi in ((-1, -.01), (-.01, -.004), (-.004, -.001), (-.001, .001), (.001, .004), (.004, .01), (.01, 1)):
        show(f, (f["r_co"] >= lo) & (f["r_co"] < hi), f"gap {lo*100:+.1f}%..{hi*100:+.1f}%")
    for lo, hi in ((-1, -.02), (-.02, -.01), (-.01, -.003), (-.003, .003), (.003, .01), (.01, .02), (.02, 1)):
        show(f, (f["r_cc_1"] >= lo) & (f["r_cc_1"] < hi), f"prior day {lo*100:+.1f}%..{hi*100:+.1f}%")
    for lo, hi in ((0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)):
        show(f, (f["ibs_1"] >= lo) & (f["ibs_1"] < hi), f"prior IBS {lo:.1f}-{hi:.1f}")
    for k in range(5):
        show(f, f["dow"] == k, f"weekday {['Mon','Tue','Wed','Thu','Fri'][k]}")
    show(f, f["tdom"] <= 3, "first 3 trading days of month")
    show(f, f["tdom_rev"] == 1, "last trading day of month")
    show(f, (f["tdom"] > 3) & (f["tdom_rev"] > 1), "mid-month")
    show(f, f["opex"] == 1, "monthly opex Friday")
    show(f, f["before_long_break"] == 1, "day before long weekend/holiday")
    show(f, f["after_long_break"] == 1, "day after long weekend/holiday")
    for k in (2, 3, 4):
        show(f, f["dn_streak"] >= k, f"down streak >= {k}")
        show(f, f["up_streak"] >= k, f"up streak >= {k}")
    for lo, hi in ((-1, -.2), (-.2, -.1), (-.1, -.05), (-.05, -.02), (-.02, 0.0001)):
        show(f, (f["dd_252"] >= lo) & (f["dd_252"] < hi), f"drawdown from 52w high {lo*100:.0f}..{hi*100:.0f}%")
    for lo, hi in ((-1, -.05), (-.05, -.02), (-.02, 0), (0, .02), (.02, .05), (.05, 1)):
        show(f, (f["ret_20d"] >= lo) & (f["ret_20d"] < hi), f"20d return {lo*100:+.0f}..{hi*100:+.0f}%")
    for lo, hi in ((-1, -.005), (-.005, 0), (0, .005), (.005, 1)):
        show(f, (f["r_oc_1"] >= lo) & (f["r_oc_1"] < hi), f"prior intraday {lo*100:+.1f}..{hi*100:+.1f}%")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "SPY")
