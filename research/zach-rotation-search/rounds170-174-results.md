# Rounds 170-174: results (2026-11-03)

The fifth batch after the search was extended to round 200 (`rounds106-150-rules.md`,
"Rounds 170-174"). The queue and all five scripts were committed and pushed before any of
them ran. Every run used data cut off at 1999-12. Each script first rebuilt R65-1's
1927-1999 figure, and it matched round 66's exactly. Figures are in
`history/backtests/variants/round170/` to `round174/`.

**The runs:** each round was run twice, and the result files and printed output were
byte-for-byte identical. Before any run, each part alone in the combined 30-plus-49
account reproduced its own round's return exactly.

**Doubled costs, 1927-07 to 1999-12, against R65-1 (15.35% a year, worst drop 76.2%,
steadiness 0.614):**

| Round | Blend | Try | Yearly return | Gain | Worst drop | Steadiness | Trades a year | Result |
|---|---|---|---|---|---|---|---|---|
| 170 | A third each in 146, 141, 134 | 121 | 19.25% | **+3.90** | 71.9% | 0.663 | 5.9x | **shortlist** |
| 171 | A quarter each in 146, 131, 141, 134 | 122 | 19.18% | **+3.83** | 72.5% | 0.665 | 6.0x | **shortlist** |
| 172 | Half each in 122 and 140 | 123 | 18.54% | **+3.19** | 69.7% | 0.617 | 6.1x | **shortlist** |
| 173 | Half each in 131 and 134 | 124 | 18.89% | **+3.54** | 73.8% | 0.620 | 5.8x | **shortlist** |
| 174 | A third each in 131, 134, 140 | 125 | 18.77% | **+3.42** | 71.7% | 0.643 | 6.7x | **shortlist** |

- G1 needs a gain of +1.0. G2 needs a worst drop of 81.2% or less (R65-1's 76.2% plus 5).
- All five beat R65-1 in both halves (to 1963-12 and from 1964-01), and the market in each
  development quarter-century.
- **An independent rebuild** in plain Python, without pandas or the shared scripts, gave the
  same return, drop and half-period figures for all five to six decimal places, at both
  cost settings.

## Each blend against its parts

| Blend | Its parts | Blend's gain | Average of the parts | Best part | Blend's drop | Parts' drops | Blend's steadiness | Steadiest part |
|---|---|---|---|---|---|---|---|---|
| 170 | 146, 141, 134 | +3.90 | +3.57 | +3.89 | 71.9% | 76.8, 66.8, 73.5 | 0.663 | 0.612 |
| 171 | 146, 131, 141, 134 | +3.83 | +3.52 | +3.89 | 72.5% | 76.8, 74.8, 66.8, 73.5 | 0.665 | 0.612 |
| 172 | 122, 140 | +3.19 | +2.95 | +3.11 | 69.7% | 72.9, 67.3 | 0.617 | 0.549 |
| 173 | 131, 134 | +3.54 | +3.29 | +3.35 | 73.8% | 74.8, 73.5 | 0.620 | 0.575 |
| 174 | 131, 134, 140 | +3.42 | +3.13 | +3.35 | 71.7% | 74.8, 73.5, 67.3 | 0.643 | 0.575 |

## What rounds 170-174 show

- **Blending helped again, by 0.24 to 0.33 points a year over the parts' average.** It was
  largest in the three- and four-part blends that include the 49-industry rule (170, 171,
  174). Every blend was steadier than each of its parts.
- **Blends without rounds 141 and 146 still did well:**
  - **Round 173** (131 and 134) gained +3.54, and **round 174** (131, 134 and 140) gained
    +3.42. Both beat every one of their parts.
  - **Round 172** used round 165's two families on their top-4 buffers instead of their
    peak settings. It gained +3.19 with a worst drop of 69.7%, against round 165's +3.96.
    So about 0.8 points of round 165's gain comes from those peak settings.
- **Round 170 is now second**, at +3.90. It replaces round 131 in round 160 with the
  49-industry rule, and is a little ahead of round 160.
- **The exam's top 5:** 165 (+3.96), 170 (+3.90), 141 (+3.89), 171 (+3.83), 160 (+3.83).
  Round 146 (+3.59) drops to sixth. **All five now include round 141,** so the overlap
  noted after rounds 165-169 is greater. The rule picking the top 5 by gain stays as
  written unless the group decides otherwise before the exam.
- **The shortlist has 44 rules.** **Tries so far: 125.**
