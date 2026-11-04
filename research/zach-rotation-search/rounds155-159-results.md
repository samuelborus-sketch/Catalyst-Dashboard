# Rounds 155-159: results (2026-11-03)

The second batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 155-159"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round155/` to `round159/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%):**

| Round | Candidate | Try | Yearly return | Gain | Worst drop | Halves vs R65-1 | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 155 | Nearest the high, top 2, kept while in the top 5 | 106 | 17.93% | **+2.58** | 67.3% | both better | 7.7x | **shortlist** |
| 156 | Top 3, kept while in the top 4 | 107 | 17.04% | **+1.69** | 72.8% | both better | 5.0x | **shortlist** |
| 157 | 49 industries, top 2, no buffer | 108 | 18.18% | **+2.83** | 72.2% | both better | 8.1x | **shortlist** |
| 158 | Two scores, top 3, kept while in the top 5 | 109 | 17.81% | **+2.46** | 74.8% | both better | 6.1x | **shortlist** |
| 159 | Top 2 by a 6-month score, kept while in the top 5 | 110 | 13.82% | −1.52 | 88.3% | worse, then level | 5.8x | out |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
- **Round 159 failed G1, G2 and G4:** it earned 10.76% a year before 1964 against R65-1's
  13.72%, and 17.018% from 1964 against 17.021%.
- All five beat the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for rounds 155, 156, 157 and 158 to six decimal
  places, at both cost settings.

**Steadiness, doubled costs (R65-1: 0.614):** 155 0.542, 156 0.527, 157 0.498, 158 0.607.

## The buffer table, now complete

Gains at doubled costs, 1927-1999. A held group stays while it ranks in the top 3, 4, 5 or
6; "no buffer" means only the top 2 (or top 3) are held. For rules holding 3, "no buffer"
and "top 3" are the same rule. "cap" means it failed the drop cap. Bold marks the exam's
finalists.

| Family | No buffer | Top 3 | Top 4 | Top 5 | Top 6 |
|---|---|---|---|---|---|
| R65-1's score, hold 2 | +2.90 | +2.88 | +3.11 | **+3.59** | +2.01 |
| Two scores, hold 2 | **+3.26** | **+3.32** | **+3.35** | +1.94 (cap) | +1.94 |
| R65-1's score, 49 groups, hold 2 | +2.83 | +3.02 | +3.23 | +2.52 | +1.48 |
| Nearest the high, hold 2 | +2.45 (cap) | **+3.89** | +2.79 | +2.58 | +0.50 |
| R65-1's score, hold 3 | +1.59 | same | +1.69 | +2.60 | +1.69 |
| Two scores, hold 3 | +2.60 | same | +2.35 | +2.46 | +1.43 |

## What rounds 155-159 show

- **Nothing reached the exam's top 5 again.** The best was round 157 (+2.83). The fifth
  place is still +3.26.
- **Round 146 depends on its 12-month score.** Swapping in a 6-month score (round 159)
  turned a +3.59 gain into −1.52 and a worst drop of 88%. Round 146's gain also falls off
  on either side of its buffer (+3.11 at the top 4, +2.01 at the top 6). That is two signs
  its exact settings are tuned to 1927-1999.
- **Round 141's spike is a little less sharp than it looked.** With a top-5 buffer the
  same score gained +2.58 and fell 67.3%, so the row runs +2.79, +2.58 after the +3.89
  peak, before dropping to +0.50 at the top 6.
- **The two-score family is still the most even** up to the top 4 (+3.26 to +3.35).
- **The 49 finer industries hold up without a buffer** (round 157, +2.83, the best of this
  batch), though they trade 8 times a year.
- **Round 158 is close to R65-1's steadiness** (0.607 against 0.614) while gaining +2.46.
- **The exam's top 5 is unchanged:** 141 (+3.89), 146 (+3.59), 131 (+3.35), 147 (+3.32),
  130 (+3.26). **The shortlist has 32 rules.** **Tries so far: 110.**
