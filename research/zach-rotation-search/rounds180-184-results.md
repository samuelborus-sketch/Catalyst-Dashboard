# Rounds 180-184: results (2026-11-03)

The seventh batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 180-184"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round180/` to `round184/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, from each round's first month to 1999-12, against R65-1 over the same
months:**

| Round | Candidate | Try | From | Yearly return (R65-1) | Gain | Worst drop (R65-1) | Steadiness | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|---|
| 180 | Half each in 146 and 131 | 131 | 1927-07 | 18.97% (15.35%) | **+3.62** | 75.5% (76.2%) | 0.609 | 5.0x | **shortlist** |
| 181 | Half each in 131 and 141 | 132 | 1927-07 | 19.07% (15.35%) | **+3.72** | 70.6% (76.2%) | 0.625 | 8.2x | **shortlist** |
| 182 | All in the best of 146, 131, 141, 134 over 12 months | 133 | 1928-07 | 19.35% (15.02%) | **+4.33** | 69.6% (76.2%) | 0.585 | 8.2x | **shortlist** |
| 183 | Half in the best of 146, 131, 141 over 12 months, half in equal thirds | 134 | 1928-07 | 19.21% (15.02%) | **+4.19** | 72.5% (76.2%) | 0.663 | 6.6x | **shortlist** |
| 184 | All in the best of 146, 131, 141 over 6 months | 135 | 1928-01 | 19.43% (15.13%) | **+4.30** | 71.7% (76.2%) | 0.633 | 7.4x | **shortlist** |

- G1 needs a gain of +1.0. G2 needs a worst drop no more than 5 points deeper than R65-1's
  over the same months (81.2% here).
- All five beat R65-1 in both halves and the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for all five to six decimal places, at both
  cost settings.

## Following the leading part held up

**Computed after seeing the results, to read them, not to judge them:** each
follow-the-leader rule against equal shares in the same parts over the same months, at
doubled costs:

| Round | Over | Follow-the-leader gain | Equal shares in the same parts | Difference |
|---|---|---|---|---|
| 178 | 1928-07 to 1999-12 | +4.41 | +3.87 (thirds: 146, 131, 141) | +0.54 |
| 182 | 1928-07 to 1999-12 | +4.33 | +3.86 (quarters: 146, 131, 141, 134) | +0.47 |
| 183 (half follows) | 1928-07 to 1999-12 | +4.19 | +3.87 (thirds) | +0.32 |
| 184 (6 months) | 1928-01 to 1999-12 | +4.30 | +3.95 (thirds) | +0.35 |

- **Following the part that did best lately beat equal shares in every version:** with
  12 or 6 months, with three or four parts, and with all or half the money.
- **But these aren't four independent checks.** They use the same parts on the same
  years, so if round 178's edge was luck, the others would mostly share it.
- **Following the leader gives up some steadiness.** Rounds 178, 182 and 184 hold only one
  part (2 groups) at a time. Round 183 keeps half in equal thirds and is the steadiest of
  the batch (0.663), for 0.2 points less gain than round 178.
- **Why it might work:** the parts are momentum rules, and momentum tends to do better in
  some stretches than others. A part that has led for a year may keep leading for a while.
  That's a reasonable story, but it's the kind told after a result, and one test can't
  separate it from luck.

## The last two pairs (rounds 180 and 181)

- **Both passed, with smaller blending bonuses** than earlier pairs:
  - 180 (146 + 131): +3.62, against a parts' average of +3.47 (+0.15).
  - 181 (131 + 141): +3.72, against +3.62 (+0.10).
  - 165 (146 + 141): +3.96, against +3.74 (+0.22).
- **The bonus follows how often two parts hold the same groups.** Holding the same groups
  leaves less to smooth out:

| Pair | Groups in common in an average month | Months with none in common |
|---|---|---|
| 146 + 141 | 0.85 | 34% |
| 146 + 131 | 1.03 | 19% |
| 131 + 141 | 1.38 | 12% |

  Round 131's score mixes the other two scores, so it often picks what they pick.

## The exam's top 5

- **178 (+4.41), 182 (+4.33), 184 (+4.30), 183 (+4.19), 165 (+3.96).** Round 179 (+3.93)
  is sixth.
- **Four of the five follow the leading part,** and all five are built on rounds 141 and
  146. The exam would mostly ask one question: do rounds 141 and 146, and following the
  one that's ahead, hold up after 1999?
- The first four start in 1928, which favours them by about 0.04 to 0.12 points against a
  1927-07 start (equal thirds: +3.83 from 1927-07, +3.87 from 1928-07, +3.95 from 1928-01).
- The selection rule stays as written unless the group changes it before the exam.
- **The shortlist has 54 rules.** **Tries so far: 135.**
