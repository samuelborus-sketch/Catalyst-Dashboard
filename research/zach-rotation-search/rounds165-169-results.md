# Rounds 165-169: results (2026-11-03)

The fourth batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 165-169"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round165/` to `round169/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%):**

| Round | Candidate | Try | Yearly return | Gain | Worst drop | Steadiness | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 165 | Half each in rounds 146 and 141 | 116 | 19.31% | **+3.96** | 71.5% | 0.651 | 6.5x | **shortlist** |
| 166 | A third each in 122, 131, 140 (all top-4 buffers) | 117 | 18.66% | **+3.31** | 71.3% | 0.625 | 6.3x | **shortlist** |
| 167 | A third each in 146, 150, 155 (all top-5 buffers) | 118 | 18.29% | **+2.94** | 75.3% | 0.605 | 5.4x | **shortlist** |
| 168 | A third each in 126, 147, 141 (all top-3 buffers) | 119 | 18.93% | **+3.58** | 73.7% | 0.635 | 7.6x | **shortlist** |
| 169 | Half in round 160, half in R65-1 | 120 | 17.36% | **+2.01** | 73.5% | **0.684** | 5.4x | **shortlist** |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
- All five beat R65-1 in both halves (to 1963-12 and from 1964-01), and the market in each
  development quarter-century. R65-1's steadiness over these months is 0.614.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for all five to six decimal places, at both
  cost settings.

## Spreading across rules helped every time

Each blend against the rules it's made of (doubled costs, 1927-1999):

| Blend | Its parts | Blend's gain | Average of the parts | Best part | Blend's drop | Parts' drops | Blend's steadiness | Steadiest part |
|---|---|---|---|---|---|---|---|---|
| 160 | 146, 131, 141 | +3.83 | +3.61 | +3.89 | 72.5% | 76.8, 74.8, 66.8 | 0.647 | 0.612 |
| 165 | 146, 141 | +3.96 | +3.74 | +3.89 | 71.5% | 76.8, 66.8 | 0.651 | 0.612 |
| 166 | 122, 131, 140 | +3.31 | +3.08 | +3.35 | 71.3% | 72.9, 74.8, 67.3 | 0.625 | 0.575 |
| 167 | 146, 150, 155 | +2.94 | +2.71 | +3.59 | 75.3% | 76.8, 81.5, 67.3 | 0.605 | 0.560 |
| 168 | 126, 147, 141 | +3.58 | +3.36 | +3.89 | 73.7% | 73.5, 80.8, 66.8 | 0.635 | 0.612 |

- **Every blend earned about 0.22-0.23 points a year more than the average of its parts,**
  and was steadier than each of them.
- **Why that happens:** the parts often hold different groups, so their bad months don't
  all line up. Resetting to equal shares each month sells some of whichever part has risen
  and buys whichever has fallen. Smaller swings lose less to compounding: a fall of 50%
  needs a rise of 100% to get back, so a smoother path ends higher at the same average
  return.
- **This holds with every buffer setting (166-168),** not just the peak ones round 160 used.
  So the blend's gain over its parts doesn't look tuned.
- **But a blend inherits its parts' luck.** The extra 0.2 points is small next to the
  parts' own gains of +2.6 to +3.9. If those gains were partly luck on 1927-1999, most of
  the blend's gain is too.
- **Half in R65-1 (round 169)** kept +2.01 of round 160's +3.83 and was the steadiest rule
  on the shortlist (0.684), holding R65-1's 9 groups for half the money.

## The exam's top 5 now repeats two ideas

- **The exam's top 5:** 165 (+3.96), 141 (+3.89), 160 (+3.83), 146 (+3.59), 168 (+3.58).
  Rounds 131 (+3.35) and 147 (+3.32) drop to sixth and seventh.
- **Every one of the five is round 141, round 146, or a blend containing one or both.** So
  the exam would mostly test those two rules five times, and if 141 and 146 fail on
  2000-2026, the blends will probably fail with them.
- **The rule fixed before round 106 picks finalists by gain alone,** and it stays as
  written. Any change, such as letting at most one rule into the exam from each mix of
  parts, would be a choice made after seeing these results. It would have to be written
  down and flagged before the exam runs. That's for the group to decide.
- **The shortlist has 39 rules.** **Tries so far: 120.**
