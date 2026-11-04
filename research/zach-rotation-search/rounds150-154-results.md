# Rounds 150-154: results (2026-11-03)

The first batch after Zach extended the return-first sealed search to round 200
(`rounds106-150-rules.md`, "Extended to round 200"). The change, the queue and all five
scripts were committed before any of them ran. Every run used data cut off at 1999-12.
Each script first rebuilt R65-1's 1927-1999 figure, and it matched round 66's exactly.
Figures are in `history/backtests/variants/round150/` to `round154/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%):**

| Round | Candidate | Try | Yearly return | Gain | Worst drop | Halves vs R65-1 | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 150 | Two scores, top 2, kept while in the top 5 | 101 | 17.29% | +1.94 | 81.5% | both better | 5.7x | out |
| 151 | 49 industries, top 2, kept while in the top 5 | 102 | 17.87% | **+2.52** | 77.0% | both better | 4.1x | **shortlist** |
| 152 | Top 3, kept while in the top 5 | 103 | 17.95% | **+2.60** | 71.5% | both better | 4.0x | **shortlist** |
| 153 | Two scores, top 3, kept while in the top 4 | 104 | 17.70% | **+2.35** | 73.7% | both better | 7.5x | **shortlist** |
| 154 | Top 2, kept while in the top 5, two-thirds in the leader | 105 | 18.46% | +3.11 | 83.4% | both better | 4.9x | out |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
- **Rounds 150 and 154 failed only G2:** they fell 81.5% (0.3 points over the cap) and
  83.4%.
- All five beat the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for rounds 151, 152 and 153 to six decimal
  places, at both cost settings.

## The buffer families, updated

Gains at doubled costs, 1927-1999. A held group stays while it ranks in the top 2 (no
buffer), 3, 4, 5 or 6. A dash means that combination wasn't tried; "cap" means it failed
the drop cap.

| Family | Top 2 | Top 3 | Top 4 | Top 5 | Top 6 |
|---|---|---|---|---|---|
| R65-1's score, hold 2 | +2.90 | +2.88 | +3.11 | **+3.59** | +2.01 |
| Two scores, hold 2 | +3.26 | +3.32 | +3.35 | +1.94 (cap) | +1.94 |
| R65-1's score, 49 groups, hold 2 | - | +3.02 | +3.23 | +2.52 | +1.48 |
| Nearest the high, hold 2 | +2.45 (cap) | **+3.89** | +2.79 | - | +0.50 |
| R65-1's score, hold 3 | +1.59 | - | - | +2.60 | +1.69 |
| Two scores, hold 3 | +2.60 | - | +2.35 | - | +1.43 |

## What rounds 150-154 show

- **The numbers stopped improving this batch.** None of the five beat the exam's fifth
  place (+3.26). The two that came closest, 150 and 154, broke the drop cap.
- **The two-score family falls off sharply after the top 4:** +3.35 at the top 4, +1.94
  at the top 5, with a worst drop over the cap.
- **Two-thirds in the leader added a little return but fell harder** (round 154: +3.11,
  83.4%, against round 146's +3.59, 76.8% with equal amounts).
- **Round 152 (top 3, kept while in the top 5) had the third-smallest worst drop of the
  search,** 71.5%, behind rounds 141 (66.8%) and 140 (67.3%).
- **The exam's top 5 is unchanged:** 141 (+3.89), 146 (+3.59), 131 (+3.35), 147 (+3.32),
  130 (+3.26). **The shortlist has 28 rules.** **Tries so far: 105.**
