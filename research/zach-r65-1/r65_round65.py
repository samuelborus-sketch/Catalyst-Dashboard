"""Round 65 (round65-rules.md): R65-1, R63-1 over Ken French's 30 US industries, holding the top 9, 1927-07 on.

    uv run python -I experiments/2026-10-28-dip-rule-backtest/scripts/r65_round65.py check
    uv run python -I experiments/2026-10-28-dip-rule-backtest/scripts/r65_round65.py run <normal|stressed>

Industry returns are the first block ("Average Value Weighted Returns -- Monthly") of 30_Industry_Portfolios.csv;
the market is Mkt-RF + RF from round 63's F-F_Research_Data_Factors.csv. Both are monthly, in %.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, norm, skew

RAW = Path("data_cache/backtest/round65-french/raw")
RAW63 = Path("data_cache/backtest/round63-french/raw")
OUT = Path("history/backtests/variants/round65")
R63 = Path("history/backtests/variants/round63")
FIRST, TOP, LOOKBACK, TRIES, EULER_GAMMA = pd.Period("1927-07", "M"), 9, 11, 11, 0.5772156649
QUARTERS = [("1927-07", "1950-12"), ("1951-01", "1975-12"), ("1976-01", "2000-12"), ("2001-01", None)]
mode = sys.argv[1]
setting = sys.argv[2] if mode == "run" else "normal"
COST = 0.0005 * (2.0 if setting == "stressed" else 1.0)


def first_block(path, header_start):
    """As r63_round63.py: the first monthly block after the header line, as fractions; -99.99/-999 → NaN."""
    lines = path.read_text(encoding="latin-1").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(header_start))
    cols = [c.strip() for c in lines[start].split(",")[1:]]
    rows = {}
    for line in lines[start + 1:]:
        parts = [p.strip() for p in line.split(",")]
        if len(parts[0]) != 6 or not parts[0].isdigit():
            break
        vals = [float(p) for p in parts[1:]]
        rows[pd.Period(f"{parts[0][:4]}-{parts[0][4:]}", "M")] = [np.nan if v <= -99.99 else v / 100 for v in vals]
    return pd.DataFrame.from_dict(rows, orient="index", columns=cols)


ind = first_block(RAW / "30_Industry_Portfolios.csv", ",Food")


def firm_counts(path):
    """The "Number of Firms in Portfolios" block, by month."""
    lines = path.read_text(encoding="latin-1").splitlines()
    at = next(i for i, line in enumerate(lines) if "Number of Firms in Portfolios" in line)
    cols, rows = [c.strip() for c in lines[at + 1].split(",")[1:]], {}
    for line in lines[at + 2:]:
        parts = [p.strip() for p in line.split(",")]
        if len(parts[0]) != 6 or not parts[0].isdigit():
            break
        rows[pd.Period(f"{parts[0][:4]}-{parts[0][4:]}", "M")] = [int(p) for p in parts[1:]]
    return pd.DataFrame.from_dict(rows, orient="index", columns=cols)


firms = firm_counts(RAW / "30_Industry_Portfolios.csv")
ff = first_block(RAW63 / "F-F_Research_Data_Factors.csv", ",Mkt-RF")
if len(ind.columns) != 30 or not ind.index.equals(ff.index):
    raise ValueError("expected 30 groups and the market file's months")
mkt = ff["Mkt-RF"] + ff["RF"]
missing = ind.isna().sum()
if missing.any() or mkt.isna().any():
    raise ValueError(f"missing months, so the run stops (round65-rules.md): {missing[missing > 0].to_dict()}")
LAST = ind.index[-1]
months = ind.loc[FIRST:].index

if mode == "check":
    print(f"{ind.index[0]} to {LAST}, {len(ind)} months, {len(ind.columns)} groups, none missing")
    big = ind.stack()
    big = big[big.abs() >= 0.50]
    for (m, g), v in big.items():
        print(f"  {m} {g}: {v * 100:+.1f}% (market {mkt.loc[m] * 100:+.1f}%)")
    sys.exit()


def psr(r, benchmark=0.0):
    """As sentinel/evaluate.py's probabilistic_sharpe."""
    n, sr = len(r), r.mean() / r.std(ddof=1)
    denom = np.sqrt(1 - skew(r) * sr + (kurtosis(r, fisher=False) - 1) / 4 * sr ** 2)
    return float(norm.cdf((sr - benchmark) * np.sqrt(n - 1) / denom))


def luck_best(n_tries, spread):
    """As sentinel/evaluate.py's expected_max_sharpe, with the no-skill spread."""
    return spread * ((1 - EULER_GAMMA) * norm.ppf(1 - 1 / n_tries) + EULER_GAMMA * norm.ppf(1 - 1 / (n_tries * np.e)))


def score(m):
    """Return over the 11 months before the latest one, as known at the end of month m - 1."""
    window = ind.loc[m - 1 - LOOKBACK:m - 2]
    if len(window) != LOOKBACK:
        raise ValueError(f"short score window for {m}")
    return (1 + window).prod() - 1


def account(pick, cost):
    """As r63_round63.py: monthly returns after `cost` per unit traded, reset to equal amounts of `pick(m)` monthly;
    also the value traded each month."""
    drifted, out, traded_by = None, {}, {}
    for m in months:
        chosen = pick(m)
        target = pd.Series(0.0, index=ind.columns)
        target[chosen] = 1 / len(chosen)
        traded = 1.0 if drifted is None else float((target - drifted).abs().sum())
        out[m] = (1 - cost * traded) * (1 + float((target * ind.loc[m]).sum())) - 1
        traded_by[m] = traded
        grown = target * (1 + ind.loc[m])
        drifted = grown / grown.sum()
    return pd.Series(out), pd.Series(traded_by)


def yearly(r):
    return float(((1 + r).prod() ** (12 / len(r)) - 1) * 100)


def drop(r):
    v = pd.concat([pd.Series([1.0]), (1 + r).cumprod().reset_index(drop=True)])
    return float(-(v / v.cummax() - 1).min() * 100)


def luck(lead):
    lead = np.asarray(lead)
    return {"one_try": psr(lead), "deflated": psr(lead, luck_best(TRIES, 1 / np.sqrt(len(lead))))}


picks = {m: list(score(m).nlargest(TOP).index) for m in months}
rule, traded = account(lambda m: picks[m], COST)
equal, _ = account(lambda m: list(ind.columns), COST)
held = mkt.loc[FIRST:]
r63 = json.loads((R63 / f"R63-1-{setting}.json").read_text())
quarters = {}
for a, b in QUARTERS:
    sl = slice(pd.Period(a, "M"), pd.Period(b, "M") if b else LAST)
    quarters[f"{a} to {b or str(LAST)}"] = {k: yearly(s.loc[sl]) for k, s in
                                           (("rule", rule), ("market", held), ("equal", equal))}
decades = {}
for d in range(1930, 2030, 10):
    sl = slice(pd.Period(f"{d}-01", "M"), min(pd.Period(f"{d + 9}-12", "M"), LAST))
    decades[str(d)] = float((((1 + rule.loc[sl]).prod() / (1 + held.loc[sl]).prod()) ** (12 / len(rule.loc[sl])) - 1)
                            * 100)
lead = rule - held
whole = {k: {"return": yearly(s), "drop": drop(s)} for k, s in (("rule", rule), ("market", held), ("equal", equal))}
lo, hi = 0.0, 0.05                                     # cost per unit traded at which the lead over the market vanishes
for _ in range(60):
    c = (lo + hi) / 2
    lo, hi = (c, hi) if (1 + account(lambda m: picks[m], c)[0]).prod() > (1 + held).prod() else (lo, c)
small = pd.Series({m: bool((firms.loc[m, picks[m]] < 10).any()) for m in months})
tiny = {"months_holding_one_per_year": float(small.mean() * 12),
        "share_of_months": float(small.mean()),
        "lead_per_year_those_months": float(lead[small].mean() * 12 * 100) if small.any() else None,
        "lead_per_year_other_months": float(lead[~small].mean() * 12 * 100)}
tests = {"T1": whole["rule"]["return"] > whole["market"]["return"],
         "T2": all(q["rule"] > q["market"] for q in quarters.values()),
         "T3": whole["rule"]["drop"] <= whole["market"]["drop"] + 0.5,
         "T4": bool(luck(lead)["deflated"] >= 0.95)}
result = {"setting": setting, "months": len(rule), "from": str(FIRST), "to": str(LAST), "whole": whole,
          "quarters": quarters, "lead_by_decade": decades, "tests": tests, "passes": all(tests.values()),
          "lead_per_year": float(lead.mean() * 12 * 100),
          "info_ratio_per_year": float(lead.mean() / lead.std(ddof=1) * np.sqrt(12)),
          **luck(lead), "vs_equal": luck(rule - equal),
          "after_publication": {"lead_per_year": float(lead.loc["2000-01":].mean() * 12 * 100),
                                **luck(lead.loc["2000-01":])},
          "change_months_per_year": float(np.mean([set(picks[m]) != set(picks[m - 1]) for m in months[1:]]) * 12),
          "value_traded_per_year": float(traded.iloc[1:].mean() * 12),
          "break_even_cost_pct": lo * 100,
          "tiny_groups": tiny,
          "R63-1": {"return": r63["whole"]["rule"]["return"], "drop": r63["whole"]["rule"]["drop"],
                    "info_ratio_per_year": r63["info_ratio_per_year"], "deflated_9_tries": r63["deflated"]},
          "picks": {str(m): sorted(p) for m, p in picks.items()}}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / f"R65-1-{setting}.json").write_text(json.dumps(result, indent=1))
for k, x in whole.items():
    print(f"{setting} {k:6} {x['return']:.2f}/yr, worst drop {x['drop']:.1f}")
print(f"{setting} R63-1  {r63['whole']['rule']['return']:.2f}/yr, worst drop {r63['whole']['rule']['drop']:.1f}, "
      f"info ratio {r63['info_ratio_per_year']:.2f}")
for q, x in quarters.items():
    print(f"{setting} {q}: rule {x['rule']:.2f} market {x['market']:.2f} equal {x['equal']:.2f}")
print(f"{setting} lead by decade: " + ", ".join(f"{d} {v:+.2f}" for d, v in decades.items()))
print(f"{setting} lead {result['lead_per_year']:+.2f}/yr, info ratio {result['info_ratio_per_year']:.2f}; luck one try "
      f"{result['one_try']:.3f}, deflated over {TRIES} tries {result['deflated']:.3f}; vs equal deflated "
      f"{result['vs_equal']['deflated']:.3f}; from 2000 lead {result['after_publication']['lead_per_year']:+.2f}, "
      f"deflated {result['after_publication']['deflated']:.3f}")
print(f"{setting} changes {result['change_months_per_year']:.1f} months/yr, trades {result['value_traded_per_year']:.2f}x "
      f"a year, break-even cost {result['break_even_cost_pct']:.2f}%")
print(f"{setting} held a group under 10 firms in {tiny['share_of_months'] * 100:.0f}% of months; lead then "
      f"{tiny['lead_per_year_those_months']}, otherwise {tiny['lead_per_year_other_months']:+.2f}/yr")
print(f"{setting} " + " ".join(f"{t} {'pass' if v else 'FAIL'}" for t, v in tests.items())
      + f" -> {'PASSES' if result['passes'] else 'fails'}")
