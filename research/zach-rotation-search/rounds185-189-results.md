# Rounds 185-189: results (2026-11-03)

The eighth batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 185-189"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round185/` to `round189/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, from each round's first month to 1999-12, against R65-1 over the same
months:**

| Round | Candidate | Try | From | Yearly return (R65-1) | Gain | Worst drop (R65-1) | Steadiness | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|---|
| 185 | All in the best of 122, 131, 140 over 12 months | 136 | 1928-07 | 17.91% (15.02%) | **+2.90** | 77.4% (76.2%) | 0.523 | 6.8x | **shortlist** |
| 186 | All in the best of 122, 131, 140, 134 over 12 months | 137 | 1928-07 | 18.30% (15.02%) | **+3.28** | 75.7% (76.2%) | 0.513 | 8.1x | **shortlist** |
| 187 | Half each in the two best of 146, 131, 141, 134 over 12 months | 138 | 1928-07 | 19.57% (15.02%) | **+4.56** | 70.7% (76.2%) | 0.654 | 7.3x | **shortlist** |
| 188 | Half in the best of 146, 131, 141 over 12 months, half in R65-1 | 139 | 1928-07 | 17.34% (15.02%) | **+2.33** | 73.7% (76.2%) | **0.692** | 5.7x | **shortlist** |
| 189 | All in the best of 146, 131, 141 over 9 months | 140 | 1928-04 | 19.75% (15.03%) | **+4.71** | 73.0% (76.2%) | 0.663 | 7.0x | **shortlist** |

- G1 needs a gain of +1.0. G2 needs a worst drop no more than 5 points deeper than R65-1's
  over the same months (81.2% here).
- All five beat R65-1 in both halves and the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for all five to six decimal places, at both
  cost settings.

## Following the leader only works with rounds 141 and 146

**Computed after seeing the results, to read them, not to judge them:** each rule against
equal shares in the same parts over the same months, at doubled costs:

| Round | Parts | Follow the leader | Equal shares | Difference |
|---|---|---|---|---|
| 185 | 122, 131, 140 | +2.90 | +3.38 | **−0.48** |
| 186 | 122, 131, 140, 134 | +3.28 | +3.49 | **−0.21** |
| 187 (two leaders) | 146, 131, 141, 134 | +4.56 | +3.86 | +0.70 |
| 188 (half in R65-1) | 146, 131, 141, with R65-1 | +2.33 | +2.03 | +0.30 |
| 189 (9 months) | 146, 131, 141 | +4.71 | +4.02 | +0.69 |
| Earlier: 178, 182, 183, 184 | always 141 and 146 | | | +0.32 to +0.54 |

- **Without rounds 141 and 146, following the leader lost to equal shares.** Round 185
  even trailed the average of its own parts (+3.15), and fell further (77.4%) than any of
  them.
- **With 141 and 146 among the parts, it won every time** (+0.30 to +0.70), whatever the
  lookback (6, 9 or 12 months) or the number of leaders held.
- **The likely reason:** rounds 141 and 146 were chosen because they did best on these
  same 1927-1999 years. A rule picked that way has long strong stretches on those years
  almost by design, and following whichever is ahead rides them. That shows nothing about
  later years. The rules built on parts that weren't tuned show what following the leader
  does on its own, and there it lost.
- **So the follow-the-leader gains look like a second layer of fitting** on top of rounds
  141 and 146, not a separate effect. This is a judgement from these comparisons, not a
  test, and only the exam can check it.

## The exam's top 5

- **189 (+4.71), 187 (+4.56), 178 (+4.41), 182 (+4.33), 184 (+4.30).** Rounds 183 (+4.19)
  and 165 (+3.96) follow.
- **All five follow the leader among parts that include rounds 141 and 146,** the
  combination these comparisons suggest is fitted. All five also start in 1928, which
  favours them a little.
- **The exam would test one idea five times.** If rounds 141 and 146 fade after 1999, all
  five will probably fail together, and the exam will say little about anything else on
  the shortlist (equal-share blends, the rules without 141 and 146, the hold-3 rules).
- The selection rule stays as written unless the group changes it before the exam.
- **The shortlist has 59 rules.** **Tries so far: 140.**
