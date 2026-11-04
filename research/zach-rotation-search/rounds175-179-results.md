# Rounds 175-179: results (2026-11-03)

The sixth batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 175-179"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round175/` to `round179/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, from each round's first month to 1999-12, against R65-1 over the same
months:**

| Round | Candidate | Try | From | Yearly return (R65-1) | Gain | Worst drop (R65-1) | Steadiness | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|---|
| 175 | A quarter each in 122, 131, 134, 140 | 126 | 1927-07 | 18.79% (15.35%) | **+3.44** | 71.7% (76.2%) | 0.649 | 5.9x | **shortlist** |
| 176 | Half each in 141 and 134 | 127 | 1927-07 | 19.20% (15.35%) | **+3.86** | 69.7% (76.2%) | 0.659 | 7.4x | **shortlist** |
| 177 | Half each in 146 and 134 | 128 | 1927-07 | 18.96% (15.35%) | **+3.61** | 74.7% (76.2%) | 0.595 | 4.2x | **shortlist** |
| 178 | All in the best of 146, 131, 141 over the past 12 months | 129 | 1928-07 | 19.42% (15.02%) | **+4.41** | 72.8% (76.2%) | 0.642 | 6.9x | **shortlist** |
| 179 | 146, 131, 141, 134 weighted by 1 / swings | 130 | 1930-07 | 19.23% (15.30%) | **+3.93** | 55.7% (65.5%) | 0.670 | 6.1x | **shortlist** |

- G1 needs a gain of +1.0. G2 needs a worst drop no more than 5 points deeper than R65-1's
  over the same months.
- All five beat R65-1 in both halves and the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for all five to six decimal places, at both
  cost settings.

## Rounds 178 and 179 start later, so a fairer comparison

Rounds 178 and 179 need 12 and 36 months of their parts' own returns, so they start in
1928-07 and 1930-07. Their gains are still measured against R65-1 over the same months, as
the rules say. But other rounds start in 1927-07, so their gains aren't directly
comparable. **Computed after seeing the results, to read them, not to judge them:** the
equal-share blends and their parts over the same later months, at doubled costs:

| Over | Rule | Gain over R65-1 | Worst drop |
|---|---|---|---|
| 1928-07 to 1999-12 | **178: all in the best part** | **+4.41** | 72.8% |
| | Equal thirds in 146, 131, 141 (round 160's blend) | +3.87 | 72.5% |
| | Best single part (141) | +3.93 | 66.8% |
| 1930-07 to 1999-12 | **179: weighted by 1 / swings** | **+3.93** | 55.7% |
| | Equal quarters in 146, 131, 141, 134 (round 171's blend) | +3.91 | 56.0% |
| | Best single part (146 and 141, level) | +3.90, +3.89 | 58.4%, 48.8% |

- **Weighting by swings (round 179) added almost nothing:** +0.02 over equal quarters.
  Its third place in the exam list comes from starting in 1930-07, not from the
  weighting. Its smaller drop (55.7%) is also the later start: the 1929-1932 crash was
  already partly over.
- **Following the best part (round 178) earned about 0.5 points a year more than equal
  thirds** over the same months, and more than any single part. It followed round 146 in
  39% of months, 141 in 35% and 131 in 27%, switching about 1.7 times a year.
- **Round 178 should be read with care:**
  - It undoes the spreading that made blends steadier. It holds one part, so 2 groups,
    at a time.
  - Picking whichever rule did best lately is one try among 130. Its +0.5 over equal
    thirds is about the size of the blending bonus, and could easily be luck.
  - It's built on 141 and 146, the two rules that look tuned.

## What rounds 175-177 show

- **Every blend tried so far has passed** (rounds 160 and 165-177). The best without 141
  and 146 is still round 173 (+3.54). Round 175, with all four families on the top-4 buffer, gained
  +3.44 and fell 71.7%.
- **The 49-industry rule blends best with round 141** (round 176: +3.86, drop 69.7%,
  steadiness 0.659). It blends less well with round 146 (round 177: +3.61, steadiness 0.595,
  barely above 146's own +3.59).

## The exam's top 5

- **178 (+4.41), 165 (+3.96), 179 (+3.93), 170 (+3.90), 141 (+3.89).** Rounds 176 (+3.86),
  171 (+3.83) and 160 (+3.83) follow.
- **All five still include round 141.** Two of them (178 and 179) are ranked on later
  start months, which favours them a little.
- The selection rule stays as written unless the group changes it before the exam.
- **The shortlist has 49 rules.** **Tries so far: 130.**
