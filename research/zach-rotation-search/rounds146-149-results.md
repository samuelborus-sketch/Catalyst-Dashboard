# Rounds 146-149: results, and the final shortlist (2026-11-03)

The last batch of the return-first sealed search (`rounds106-150-rules.md`). The queue and
all four scripts were committed before any of them ran. Every run used data cut off at
1999-12. Each script first rebuilt R65-1's 1927-1999 figure, and it matched round 66's
exactly. Figures are in `history/backtests/variants/round146/` to `round149/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%):**

| Round | Candidate | Try | Yearly return | Gain | Worst drop | Halves vs R65-1 | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 146 | Top 2, kept while in the top 5 | 97 | 18.94% | **+3.59** | 76.8% | both better | 3.6x | **shortlist** |
| 147 | Two scores, top 2, kept while in the top 3 | 98 | 18.67% | **+3.32** | 80.8% | both better | 8.3x | **shortlist** |
| 148 | 49 industries, top 2, kept while in the top 3 | 99 | 18.37% | **+3.02** | 75.5% | both better | 5.7x | **shortlist** |
| 149 | 49 industries, top 2, kept while in the top 6 | 100 | 16.83% | **+1.48** | 78.7% | both better | 3.6x | **shortlist** |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
  Round 147's 80.8% was 0.4 points inside the cap.
- All four beat the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for all four to six decimal places, at both
  cost settings.

## How each finalist's family behaves

Each row is one rule with only the buffer changed: a held group stays while it ranks in
the top 2 (no buffer), 3, 4, 5 or 6. Gains at doubled costs, 1927-1999.

| Family | Top 2 | Top 3 | Top 4 | Top 5 | Top 6 |
|---|---|---|---|---|---|
| R65-1's score, 30 groups | +2.90 (116) | +2.88 (126) | +3.11 (122) | **+3.59 (146)** | +2.01 (127) |
| Two scores, 30 groups | +3.26 (130) | +3.32 (147) | +3.35 (131) | | +1.94 (138) |
| R65-1's score, 49 groups | | +3.02 (148) | +3.23 (134) | | +1.48 (149) |
| Nearest the 12-month high, 30 groups | +2.45 (128, over the drop cap) | **+3.89 (141)** | +2.79 (140) | | +0.50 (142) |

- **The two-score family is the most even** from no buffer up to the top 4 (+3.26 to
  +3.35).
- **R65-1's own score is fairly even too,** with a high point at the top 5 (round 146).
- **The nearness family is the least even:** round 141 is a spike.
- **Every family falls back with a top-6 buffer.**

## The final shortlist

25 rules passed G1-G4. The rules fixed before round 106 send the 5 largest gains to the
final exam.

| Rank | Round | Rule | Gain | Yearly return | Worst drop | Trades a year | Exam |
|---|---|---|---|---|---|---|---|
| 1 | 141 | Nearest the high, top 2, kept while in the top 3 | +3.89 | 19.23% | 66.8% | 10.0x | yes |
| 2 | 146 | Top 2, kept while in the top 5 | +3.59 | 18.94% | 76.8% | 3.6x | yes |
| 3 | 131 | Two scores, top 2, kept while in the top 4 | +3.35 | 18.70% | 74.8% | 6.7x | yes |
| 4 | 147 | Two scores, top 2, kept while in the top 3 | +3.32 | 18.67% | 80.8% | 8.3x | yes |
| 5 | 130 | Two scores, top 2 | +3.26 | 18.61% | 76.8% | 11.0x | yes |
| 6 | 134 | 49 industries, top 2, kept while in the top 4 | +3.23 | 18.58% | 73.5% | 4.8x | no |
| 7 | 122 | Top 2, kept while in the top 4 | +3.11 | 18.45% | 72.9% | 4.2x | no |
| 8 | 148 | 49 industries, top 2, kept while in the top 3 | +3.02 | 18.37% | 75.5% | 5.7x | no |
| 9-25 | 116, 126, 140, 125, 133, 139, 127, 138, 132, 120, 114, 106, 149, 136, 124, 113, 111 | | +2.90 to +1.05 | | | | no |

## What the search found

- **Holding very few leaders, usually 2, earned the most on 1927-1999.** Every finalist
  holds 2 groups. Each one earned 3.3 to 3.9 points a year more than R65-1, with worst
  drops between 67% and 81% against R65-1's 76%.
- **The cost is a bumpier lead.** All five finalists' steadiness (0.56-0.61) is at or
  below R65-1's 0.614.
- **Three of the five are the two-score family,** the most even one. The other two are a
  spike (141) and a high point (146) on less even families.
- **44 tries in this search (57-100).** The exam's luck check will count all 100 tries
  counted so far.
- **Next: round 150, the final exam.** Each finalist gets one run on 2000-2026 and the
  Fidelity funds under X1-X3, and every finalist that passes goes to paper tracking beside
  R65-1.
