"""Run the flag backtest across a fixed grid of looser rule settings; every cell is reported."""
from dataclasses import dataclass
import numpy as np, pandas as pd
import flag_backtest as fb

GRID = [(3.0, 1.0), (2.0, 1.0), (2.0, 0.5), (1.5, 1.0), (1.5, 0.5)]
for sym in ("QQQ", "SPY"):
    df = fb.load(sym)
    print(f"\n===== {sym} =====")
    for pole, rr in GRID:
        R = dict(fb.RULES, pole_min_atr=pole, min_reward_r=rr)
        for entry in ("breakout", "retest"):
            tr = fb.run(df, R, entry)
            fb.summarize(tr, f"pole>={pole} room>={rr}R {entry}")
            if entry == "breakout" and len(tr) >= 20 and (pole, rr) == (2.0, 0.5):
                base = fb.random_baseline(df, tr, seeds=100, R=R)
                print(f"   random-entry baseline avgR {base.mean():+.3f} (95th pct {np.percentile(base,95):+.3f}); real beats {(base < tr.r.mean()).mean()*100:.0f}% of random runs")
                for s in ("BULL", "BEAR"): fb.summarize(tr[tr.side == s], f"   {s}")
                mid = pd.Timestamp("2026-06-30", tz="America/New_York")
                fb.summarize(tr[tr.ts <= mid], "   Feb-Jun"); fb.summarize(tr[tr.ts > mid], "   Jul-Oct")
