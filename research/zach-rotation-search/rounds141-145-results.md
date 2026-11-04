# Rounds 141-145: results (2026-11-03)

The eighth batch of the return-first sealed search (`rounds106-150-rules.md`). The queue and
all five scripts were committed before any of them ran. Every run used data cut off at
1999-12. Each script first rebuilt R65-1's 1927-1999 figure, and it matched round 66's
exactly. Figures are in `history/backtests/variants/round141/` to `round145/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%):**

| Round | Candidate | Try | Yearly return | Gain | Worst drop | Halves vs R65-1 | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 141 | Nearest the high, top 2, kept while in the top 3 | 92 | 19.23% | **+3.89** | 66.8% | both better | 10.0x | **shortlist** |
| 142 | Nearest the high, top 2, kept while in the top 6 | 93 | 15.85% | +0.50 | 72.0% | both better | 7.1x | out |
| 143 | Nearest the high, top 3, kept while in the top 6 | 94 | 16.06% | +0.72 | 73.9% | better, then worse | 7.5x | out |
| 144 | 49 industries, nearest the high, top 2, kept while in the top 4 | 95 | 15.86% | +0.51 | 73.1% | both better | 9.4x | out |
| 145 | Nearest the 6-month high, top 2, kept while in the top 4 | 96 | 16.81% | +1.46 | 85.1% | worse, then better | 9.6x | out |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
- Round 143 earned 16.92% from 1964 against R65-1's 17.02%. Round 145 earned 13.40%
  before 1964 against 13.72%, and fell 85.1% at its worst.
- All five beat the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for round 141 to six decimal places, at both
  cost settings. It also reproduced round 140.

**Round 141 in detail (doubled costs):** 17.23% a year before 1964 and 21.30% from 1964,
against R65-1's 13.72% and 17.02%. Worst drop 66.8%. Steadiness 0.612, level with R65-1's
0.614.

## What rounds 141-145 show

- **Round 141 has the highest gain and the smallest drop of the search so far**, but it
  sits on a sharp spike.
  Nearest the 12-month high, top 2, with each buffer setting:

| Kept while in the top | Round | Gain | Worst drop |
|---|---|---|---|
| 2 (no buffer) | 128 | +2.45 | 81.3% (over the cap) |
| 3 | 141 | **+3.89** | 66.8% |
| 4 | 140 | +2.79 | 67.3% |
| 6 | 142 | +0.50 | 72.0% |

- **Its other neighbours fall away too:** holding 3 (+0.72), the 49 groups (+0.51), a
  6-month high (+1.46, falling 85%). A gain that disappears when one setting moves a
  little is what luck looks like.
- **R65-1's own score with 2 groups is smoother** across the same buffers: +2.90, +2.88,
  +3.11 and +2.01 (rounds 116, 126, 122 and 127).
- **Round 141 still takes first place in the exam.** The rules fixed before round 106 rank
  finalists by gain alone, and changing that after seeing the results would be an
  after-the-fact choice. Its exam result should be read with this spike in mind.
- **The exam's top 5:** 141 (+3.89), 131 (+3.35), 130 (+3.26), 134 (+3.23), 122 (+3.11).
  Round 116 (+2.90) drops to sixth.
- **The shortlist now has 21 rules.** **Tries so far: 96.**
