"""Check how well a 3x daily-reset model built from SPY/QQQ reproduces real 3x ETF intraday moves."""
import os

import numpy as np
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(sym):
    return pd.read_csv(os.path.join(D, f"{sym}.csv"), parse_dates=["date"]).set_index("date")


def model_intraday(und, lev):
    """Open->close, open->worst and open->best return of a daily-reset ETF with leverage `lev`."""
    pc = und["close"].shift(1)
    r_co = und["open"] / pc - 1
    r_cc = und["close"] / pc - 1
    r_adverse = (und["low"] if lev > 0 else und["high"]) / pc - 1
    r_favor = (und["high"] if lev > 0 else und["low"]) / pc - 1
    base = 1 + lev * r_co
    return pd.DataFrame({
        "oc": (1 + lev * r_cc) / base - 1,
        "worst": (1 + lev * r_adverse) / base - 1,
        "best": (1 + lev * r_favor) / base - 1,
    })


def compare(und_sym, etf_sym, lev):
    m = model_intraday(load(und_sym), lev)
    etf = load(etf_sym)
    a = pd.DataFrame({
        "oc": etf["close"] / etf["open"] - 1,
        "worst": etf["low"] / etf["open"] - 1,
        "best": etf["high"] / etf["open"] - 1,
    })
    j = m.join(a, lsuffix="_m", rsuffix="_a", how="inner").dropna().iloc[1:]
    diff = j["oc_a"] - j["oc_m"]
    print(f"\n=== {etf_sym} vs {lev:+d}x {und_sym}  days={len(j)}  {j.index[0].date()}..{j.index[-1].date()}")
    print(f"  corr(open->close)          {np.corrcoef(j['oc_a'], j['oc_m'])[0, 1]:.4f}")
    print(f"  mean actual {j['oc_a'].mean() * 100:+.4f}%/day   mean model {j['oc_m'].mean() * 100:+.4f}%/day")
    print(f"  diff (actual-model): mean {diff.mean() * 100:+.4f}%/day  median {diff.median() * 100:+.4f}%  sd {diff.std() * 100:.4f}%")
    print(f"  |diff| p50/p90/p99         {diff.abs().quantile(.5) * 100:.3f}% / {diff.abs().quantile(.9) * 100:.3f}% / {diff.abs().quantile(.99) * 100:.3f}%")
    print(f"  compounded open->close every day: actual {(np.prod(1 + j['oc_a']) - 1) * 100:+.1f}%  model {(np.prod(1 + j['oc_m']) - 1) * 100:+.1f}%")
    print(f"  intraday worst (vs open): corr {np.corrcoef(j['worst_a'], j['worst_m'])[0, 1]:.4f}  mean diff {(j['worst_a'] - j['worst_m']).mean() * 100:+.4f}%")
    print(f"  P(-5% stop touched): actual {(j['worst_a'] <= -0.05).mean() * 100:.2f}%  model {(j['worst_m'] <= -0.05).mean() * 100:.2f}%")
    yr = j.groupby(j.index.year).apply(lambda g: pd.Series({
        "actual": np.prod(1 + g["oc_a"]) - 1, "model": np.prod(1 + g["oc_m"]) - 1}))
    print("  yearly compounded open->close, actual/model %:")
    print("   " + "  ".join(f"{y}:{r.actual * 100:+.0f}/{r.model * 100:+.0f}" for y, r in yr.iterrows()))
    return diff.mean()


if __name__ == "__main__":
    drag = {
        "SPXL": compare("SPY", "SPXL", 3),
        "SPXS": compare("SPY", "SPXS", -3),
        "TQQQ": compare("QQQ", "TQQQ", 3),
        "SQQQ": compare("QQQ", "SQQQ", -3),
    }
    print("\nmean intraday drag actual-model (%/day):", {k: round(v * 100, 4) for k, v in drag.items()})
