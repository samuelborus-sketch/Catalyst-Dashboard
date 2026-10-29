"""Pre-open features (everything known before/at the opening bell) and same-day outcomes."""
import os

import numpy as np
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(sym):
    return pd.read_csv(os.path.join(D, f"{sym}.csv"), parse_dates=["date"]).set_index("date")


def build(sym="SPY"):
    px = load(sym)
    vix = load("VIX")["close"].rename("vix_close")
    f = pd.DataFrame(index=px.index)
    o, h, l, c = px["open"], px["high"], px["low"], px["close"]
    pc = c.shift(1)

    # same-day outcomes (NOT features)
    f["r_oc"] = c / o - 1
    f["r_co"] = o / pc - 1            # the opening gap; known at the open
    f["r_cc"] = c / pc - 1
    f["r_lo"] = l / pc - 1
    f["r_hi"] = h / pc - 1

    # trend (as of prior close)
    for n in (20, 50, 100, 200):
        f[f"above_sma{n}"] = (pc > c.rolling(n).mean().shift(1)).astype(float)
        f[f"dist_sma{n}"] = pc / c.rolling(n).mean().shift(1) - 1
    f["sma200_slope20"] = c.rolling(200).mean().shift(1) / c.rolling(200).mean().shift(21) - 1
    f["sma50_gt_sma200"] = (c.rolling(50).mean().shift(1) > c.rolling(200).mean().shift(1)).astype(float)
    for n in (1, 2, 3, 5, 10, 20, 60, 120, 252):
        f[f"ret_{n}d"] = pc / c.shift(1 + n) - 1
    f["dd_252"] = pc / c.rolling(252).max().shift(1) - 1

    # volatility (as of prior close)
    r = c.pct_change()
    for n in (5, 10, 20, 60):
        f[f"rv{n}"] = r.rolling(n).std().shift(1) * np.sqrt(252)
    f["rv_ratio"] = f["rv5"] / f["rv60"]
    rng = (h - l) / pc
    f["range_1d"] = rng.shift(1)
    f["range_avg10"] = rng.rolling(10).mean().shift(1)
    f["vix"] = vix.shift(1).reindex(f.index)  # prior close of VIX
    f.loc[f.index < vix.index[0], "vix"] = np.nan
    f["vix_vs_20"] = f["vix"] / vix.rolling(20).mean().shift(1).reindex(f.index) - 1

    # prior-day candle
    f["ibs_1"] = ((c - l) / (h - l)).shift(1)
    f["r_oc_1"] = f["r_oc"].shift(1)
    f["r_co_1"] = f["r_co"].shift(1)
    f["r_cc_1"] = f["r_cc"].shift(1)
    up = (c > pc).astype(int)
    dn = (c < pc).astype(int)
    f["up_streak"] = up.groupby((up != up.shift()).cumsum()).cumsum().where(up == 1, 0).shift(1)
    f["dn_streak"] = dn.groupby((dn != dn.shift()).cumsum()).cumsum().where(dn == 1, 0).shift(1)

    # calendar
    idx = f.index
    f["dow"] = idx.dayofweek
    f["month"] = idx.month
    ym = idx.to_period("M")
    f["tdom"] = pd.Series(1, index=idx).groupby(ym).cumsum().values
    f["tdom_rev"] = pd.Series(1, index=idx)[::-1].groupby(ym[::-1]).cumsum()[::-1].values
    gap_days = pd.Series(idx, index=idx).diff().dt.days
    f["after_long_break"] = (gap_days > 3).astype(float)
    f["before_long_break"] = (pd.Series(idx, index=idx).shift(-1) - pd.Series(idx, index=idx)).dt.days.gt(3).astype(float)
    third_fri = (idx.dayofweek == 4) & (idx.day >= 15) & (idx.day <= 21)
    f["opex"] = third_fri.astype(float)
    f["year"] = idx.year
    return f


if __name__ == "__main__":
    f = build("SPY")
    print(f.dropna().shape, f.index[0].date(), f.index[-1].date())
    print(f.iloc[-1].round(4).to_string())
