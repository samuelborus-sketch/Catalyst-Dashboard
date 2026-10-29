"""One-at-a-time parameter sweeps: is the result a stable plateau or a knife-edge?"""
import sys
from dataclasses import replace

import numpy as np

from backtest import Params, decide, load_frames, metrics, simulate

SPY, QQQ = load_frames()


def run(p):
    dec = decide(SPY, QQQ, p)
    out = {}
    for lab, s, e in (("full", None, None), ("is", None, "2012-12-31"), ("oos", "2013-01-01", None)):
        tr, eq = simulate(SPY, QQQ, dec, p, s, e)
        out[lab] = metrics(eq, tr)
    return out


def row(label, p):
    r = run(p)
    f, i, o = r["full"], r["is"], r["oos"]
    print(f"{label:38s} FULL cagr={f['cagr']:6.2f}% dd={f['max_dd']:6.1f}% sh={f['sharpe']:.2f} n/yr={f['per_year']:5.1f} | "
          f"IS cagr={i['cagr']:6.2f}% dd={i['max_dd']:6.1f}% | OOS cagr={o['cagr']:6.2f}% dd={o['max_dd']:6.1f}%")


def main(which):
    base = Params()
    if which in ("all", "base"):
        row("BASE", base)
    if which in ("all", "tom"):
        for v in (0.0, 0.10, 0.12, 0.15, 0.18, 0.20, 0.25):
            row(f"tom_min_rv20={v}", replace(base, tom_min_rv20=v))
        for v in (2, 3, 4, 5):
            row(f"tom_days={v}", replace(base, tom_days=v))
        row("tom_family=QQQ", replace(base, tom_family="QQQ"))
        row("use_tom=False", replace(base, use_tom=False))
    if which in ("all", "dip"):
        for v in (2, 3, 4, 5):
            row(f"dip_streak={v}", replace(base, dip_streak=v))
        for v in (-0.005, -0.002, 0.0, 0.002, 0.005, 1.0):
            row(f"dip_max_gap={v}", replace(base, dip_max_gap=v))
        row("dip_family=QQQ", replace(base, dip_family="QQQ"))
        row("use_dip=False", replace(base, use_dip=False))
    if which in ("all", "opex"):
        row("opex_family=SPY", replace(base, opex_family="SPY"))
        for v in (-0.01, -0.005, -0.002):
            row(f"opex_skip_gap_down={v}", replace(base, opex_skip_gap_down=v))
        for v in (0.25, 0.35, 0.50):
            row(f"opex_max_rv20={v}", replace(base, opex_max_rv20=v))
        row("use_opex=False", replace(base, use_opex=False))
    if which in ("all", "other"):
        row("no_long_last_day=False", replace(base, no_long_last_day=False))
        for c in (0.0, 0.0005, 0.001, 0.002):
            row(f"cost={c}", replace(base, cost=c))
        for s in (0.0, 0.005, 0.01, 0.02):
            row(f"stop_slip={s}", replace(base, stop_slip=s))
        for s in (-0.03, -0.04, -0.06, -0.10, -0.99):
            row(f"daily_stop={s}", replace(base, daily_stop=s))
        for s in (-0.05, -0.15, -0.99):
            row(f"weekly_stop={s}", replace(base, weekly_stop=s))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
