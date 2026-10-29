"""Sub-split each candidate signal by trend / volatility / gap to see which filters help (decide on IS only)."""
import numpy as np
import pandas as pd

from explore import IS_END, lev_day
from features import build


def g(x):
    return np.log1p(x).mean() * 1e4 if len(x) else np.nan


def line(f, mask, label, side):
    col = "bull" if side > 0 else "bear"
    out = []
    for name, per in (("IS", f["year"] <= IS_END), ("OOS", f["year"] > IS_END)):
        m = mask & per
        x = f.loc[m, col]
        tot = np.log1p(x).sum() * 100
        out.append(f"{name}: n={m.sum():4d} g={g(x):+6.1f}bp win={(x > 0).mean() * 100 if len(x) else np.nan:4.1f}% sum={tot:+6.1f}%")
    print(f"   {label:40s} " + "  |  ".join(out))


def frame(sym):
    f = build(sym)
    f["bull"] = lev_day(f, 3)
    f["bear"] = lev_day(f, -3)
    return f.iloc[1:]


def splits(f, base, side, title):
    print(f"\n== {title}")
    line(f, base, "ALL", side)
    line(f, base & (f["above_sma200"] == 1), "above SMA200", side)
    line(f, base & (f["above_sma200"] == 0), "below SMA200", side)
    line(f, base & (f["above_sma50"] == 1), "above SMA50", side)
    line(f, base & (f["above_sma50"] == 0), "below SMA50", side)
    q = f["rv20"]
    line(f, base & (q < .15), "rv20 < 15%", side)
    line(f, base & (q >= .15) & (q < .25), "rv20 15-25%", side)
    line(f, base & (q >= .25), "rv20 >= 25%", side)
    line(f, base & (f["vix"] < 20), "VIX < 20", side)
    line(f, base & (f["vix"] >= 20) & (f["vix"] < 30), "VIX 20-30", side)
    line(f, base & (f["vix"] >= 30), "VIX >= 30", side)
    line(f, base & (f["r_co"] > 0.002), "gap up > +0.2%", side)
    line(f, base & (f["r_co"].abs() <= 0.002), "gap flat", side)
    line(f, base & (f["r_co"] < -0.002), "gap down < -0.2%", side)
    line(f, base & (f["r_cc_1"] > 0), "prior day up", side)
    line(f, base & (f["r_cc_1"] <= 0), "prior day down", side)


def main():
    for sym in ("SPY", "QQQ"):
        f = frame(sym)
        print(f"\n################ {sym} ################")
        splits(f, f["opex"] == 1, -1, "OPEX FRIDAY -> 3x BEAR")
        splits(f, f["tdom"] <= 3, +1, "FIRST 3 TRADING DAYS -> 3x BULL")
        for k in (1, 2, 3, 4, 5):
            line(f, f["tdom"] == k, f"TDOM == {k}", +1)
        line(f, f["tdom_rev"] == 1, "last day of month (bull)", +1)
        line(f, f["tdom_rev"] == 2, "2nd-last day of month (bull)", +1)
        splits(f, f["dn_streak"] >= 3, +1, "DOWN STREAK >= 3 -> 3x BULL")
        line(f, f["dn_streak"] == 2, "down streak == 2", +1)
        line(f, f["dn_streak"] == 3, "down streak == 3", +1)
        line(f, f["dn_streak"] >= 4, "down streak >= 4", +1)
        print("\n== opex-week context")
        wk = f.index.to_period("W-FRI")
        opex_week = pd.Series(f["opex"].values, index=f.index).groupby(wk).transform("max") == 1
        line(f, opex_week & (f["opex"] == 0), "opex week Mon-Thu (bull)", +1)
        line(f, opex_week & (f["opex"] == 0), "opex week Mon-Thu (bear)", -1)
        post = pd.Series(opex_week.values, index=f.index).shift(5).fillna(False).astype(bool)
        line(f, post, "week after opex (bear)", -1)
        quad = (f["opex"] == 1) & f.index.month.isin([3, 6, 9, 12])
        line(f, quad, "quarterly (quad witching) opex (bear)", -1)
        line(f, (f["opex"] == 1) & ~f.index.month.isin([3, 6, 9, 12]), "non-quarterly opex (bear)", -1)
        thu = (f["dow"] == 3) & (f.index.day >= 14) & (f.index.day <= 20)
        line(f, thu, "Thursday before opex (bear)", -1)
        line(f, thu, "Thursday before opex (bull)", +1)


if __name__ == "__main__":
    main()
