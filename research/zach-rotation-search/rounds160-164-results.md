# Rounds 160-164: results (2026-11-03)

The third batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 160-164"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round160/` to `round164/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%):**

| Round | Candidate | Try | Yearly return | Gain | Worst drop | Halves vs R65-1 | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 160 | A third each in rounds 146, 131 and 141 | 111 | 19.18% | **+3.83** | 72.5% | both better | 6.4x | **shortlist** |
| 161 | Top 2 by score over swings, kept while in the top 5 | 112 | 16.49% | **+1.14** | 69.0% | both better | 4.1x | **shortlist** |
| 162 | Top 2 by a 9-month score, kept while in the top 5 | 113 | 18.33% | +2.98 | 83.0% | both better | 4.0x | out |
| 163 | Round 146, a holding below its trend swapped for the market | 114 | 17.63% | +2.28 | 82.6% | both better | 5.0x | out |
| 164 | Nearest the 9-month high, top 2, kept while in the top 3 | 115 | 16.57% | +1.22 | 87.4% | worse, then better | 10.4x | out |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
- **Rounds 162 and 163 failed only G2** (83.0% and 82.6%). **Round 164 failed G2 and G4:**
  it earned 13.04% a year before 1964 against R65-1's 13.72%.
- All five beat the market in each development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for rounds 160 and 161 to six decimal places,
  at both cost settings.

**Round 160 in detail (doubled costs):** 17.07% a year before 1964 and 21.36% from 1964,
against R65-1's 13.72% and 17.02%. Worst drop 72.5%. Steadiness 0.647, above R65-1's 0.614
and the highest of any shortlisted rule in this search. Because the three rules often hold
the same groups, it held 3.5 different groups in an average month (2 in 15% of months, 6 in
3%), and its largest single holding averaged 43% of the account.

## What rounds 160-164 show

- **Spreading across three finalists worked best so far on 1927-1999,** but read it with
  care:
  - **Round 160 is second in the exam's top 5,** just behind round 141 (+3.89). Its worst
    drop (72.5%) is smaller than two of its three parts (146: 76.8%, 131: 74.8%), and it's
    steadier than any of them.
  - **It is built from three finalists, two of which look tuned** (rounds 141 and 146). If
    those were lucky on 1927-1999, round 160 shares the luck.
  - **The exam will run it beside three of its own parts,** so their results won't be
    independent of each other.
- **Both finalists that look tuned also depend on their score windows:**
  - Round 146 (R65-1's score): 6 months −1.52 (round 159), 9 months +2.98 but a worst drop
    of 83% (round 162), 12 months +3.59.
  - Round 141 (nearness to the high): 6 months +1.46 with an 85% drop (round 145),
    9 months +1.22 with an 87% drop (round 164), 12 months +3.89.
  - In both families only the 12-month window passes. Neither window was picked in this
    search: R65-1's score has used 12 months since round 63, and a 12-month (52-week) high
    is the published version of nearness. But both gains sit on a narrow peak.
- **A trend check on each holding didn't protect** (round 163). Moving a falling holding to
  the market cut the gain from +3.59 to +2.28, and the worst drop got deeper, 82.6% against
  round 146's 76.8%.
- **Adjusting the score for swings** (round 161) gave a small gain (+1.14) with one of the
  smallest drops on the shortlist (69.0%, fourth), but its steadiness was low (0.463
  against R65-1's 0.614).
- **The exam's top 5 has changed:** 141 (+3.89), **160 (+3.83)**, 146 (+3.59), 131 (+3.35),
  147 (+3.32). Round 130 (+3.26) drops to sixth. **The shortlist has 34 rules.** **Tries so
  far: 115.**
