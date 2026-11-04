# Round 65: industry rotation over 30 groups, 1927-2026 (written before any download)

Asked by Zach on 2026-11-02 ("Yes, plan and download"). This plan is committed before
the data is downloaded. The script is written after opening the file to see its
layout, and committed before the rule runs on it.

## Why

- **R63-1's lead is real enough to show, but too thin for the luck check.** Over about
  99 years the check needs a steadiness score (information ratio) of about 0.32-0.33.
  R63-1 had 0.35 at normal costs and 0.32 at doubled (`round63-rules.md`).
- **Slowing it down made things worse** (`round64-rules.md`). Monthly switching to the
  fresh leaders is the part that works.
- **Spreading the bet should make the lead steadier.** A rule that makes many small,
  partly separate bets usually has a steadier lead than one making a few big ones.
  This is the "fundamental law of active management": steadiness grows with the
  square root of the number of separate bets.

## A caution, written now

- **It's the same stocks and the same years as rounds 63-64,** split into finer groups.
  A pass would be a better-built version of the same test, not fresh evidence.
- **It's chosen after seeing rounds 63-64,** so it's partly fitted to this data.
- **It's try 11.** The best luck score the check expects rises to 1.62 no-skill
  spreads, so the steadiness needed over 99 years is about 0.33 (0.32 at 9 tries).
- **Round 63's cautions still apply:** industry momentum is a published idea (1999),
  the early decades are paper returns at costs nobody paid then, and the luck check
  counts only our tries.

## Data

- **Ken French's `30_Industry_Portfolios_CSV.zip`** (about 314 KB): monthly returns of
  30 US industry groups, with dividends, from 1926-07. Only the first block, "Average
  Value Weighted Returns -- Monthly", is used.
- **The market** is round 63's: `Mkt-RF + RF` from `F-F_Research_Data_Factors.csv`,
  already downloaded.
- **Data checks:**
  - **If any group has a missing month (−99.99 or −999) from 1926-07 on, the run
    stops before the rule runs.** The plan is then revisited in writing. No figure is
    filled in.
  - Every monthly move of 50% or more is listed and checked against known events.
    That's higher than round 63's 25%, because small groups move more.
  - The months must match the market file's months exactly.

## The rule (R65-1, try 11; fixed now, no setting changed later)

It's R63-1, with only the number of groups changed:

- **At each month end, it scores every group by its return over the 11 months before
  the latest one.**
- **It holds the 9 highest-scoring of the 30 groups,** a ninth each, for the next
  month. That's the same 30% share as 3 of 10.
- **It resets to ninths every month,** as R63-1 reset to thirds, and never holds cash.
- **It runs from 1927-07 to the last month in the file.**
- **Costs:** 0.05% of the value traded each month; 0.10% at doubled costs.

## Tests (fixed now), at both cost settings, over 1927-07 to the end

They're the same as rounds 63-64, with the luck check counting 11 tries:

- **(T1)** beat the market held: a higher yearly return;
- **(T2)** beat the market in every quarter-century: 1927-07 to 1950, 1951-1975,
  1976-2000, and 2001 to the end;
- **(T3)** a worst drop, from month-end values, no deeper than the market's, within
  0.5 points;
- **(T4)** the luck check:
  - the monthly lead over the market;
  - it needs a deflated Sharpe ratio of 0.95 or more, counting 11 tries;
  - the no-skill spread is 1/√(number of months).

**R65-1 passes only if all four pass at both settings.**

**Also reported, not tested:**
- each quarter-century and each decade;
- holding all 30 groups in equal amounts, reset monthly, and the luck check against it;
- R63-1's figures alongside;
- the lead from 2000-01 on, with its luck check;
- how much it trades: months with a change, value traded per year, and the cost per
  trade at which the lead over the market would vanish.

**The runs are done twice** at each setting, because this PC has had memory faults. A
result is accepted only if both runs give identical files.

## Added after the data checks, before any run (2026-11-02)

- **No group has a missing month** from 1926-07 to 2026-09, so the run goes ahead.
- **Moves of 50% or more:**
  - **Matched to known events:** the 1932-33 rebound, including April 1933's dollar
    devaluation; beer in 1933-05 as Prohibition ended; coal in 1939-09 at the start
    of WWII; textiles in 2009-04's rebound.
  - **Not confirmed:** "services" in 1930-35 (up to +123% in a month). No figure is
    edited.
- **Some groups were tiny.** The file's firm counts show several groups with fewer
  than 10 companies in the early decades. For example, in 1930-07 beer, telecoms and
  services each had 4. Coal and tobacco fell to 3 in recent years.
  - With so few companies, a group's return can be one company's luck.
  - The rule isn't changed for this, because that would be another try. Instead, the
    results also report how often the rule held a group with fewer than 10 companies,
    and its lead in those months and in the others.


## Results (2026-11-02)

**The runs:** each setting was run twice, and the files were byte-for-byte identical.
A separate rebuild written another way (in the session's scratch folder, not
committed) gave the same 9 groups every month and the same returns: 14.76% and 14.49%.

Figures are in `history/backtests/variants/round65/`.

**The whole period, 1927-07 to 2026-09:**

| | Yearly return | Worst drop |
|---|---|---|
| R65-1 (top 9 of 30) | 14.76% (14.49% at doubled costs) | 76.1% |
| R63-1 (top 3 of 10) | 13.20% (12.91%) | 74.1% |
| Market held | 10.26% | 83.7% |
| All 30 groups, equal amounts | 10.77% | 84.0% |

**Each quarter-century (yearly return, normal costs):**

| | R65-1 | Market | Equal amounts |
|---|---|---|---|
| 1927-07 to 1950 | 11.44 | 6.60 | 7.55 |
| 1951-1975 | 16.08 | 9.66 | 10.50 |
| 1976-2000 | 18.58 | 15.43 | 15.30 |
| 2001 to 2026-09 | 12.93 | 9.35 | 9.72 |

**R65-1 passes all four tests at both settings.**

| Test | Normal | Doubled costs |
|---|---|---|
| T1: beat the market held | pass | pass |
| T2: beat it in every quarter-century | pass | pass |
| T3: worst drop no deeper | pass | pass |
| T4: luck check, deflated over 11 tries, ≥ 0.95 | pass (1.000) | pass (1.000) |

**Also reported, as planned (normal costs; doubled in brackets where it matters):**
- **Lead over the market:** +4.22 points a year (+3.98), with a steadiness score
  (information ratio) of 0.57 (0.54). The luck check needed about 0.33.
- **Lead by decade:** 3.2, 6.1, 2.8, 7.8, 5.9, 1.8, 1.9, 6.2, 1.1 (2010s), 3.8. It
  was positive in all 10.
- **Against equal amounts of all 30 groups:** deflated 1.000 (0.999). The lead comes
  from choosing, not from spreading money evenly.
- **After publication (2000-01 on, 321 months):** +3.88 a year (+3.62). That's 0.74
  (0.69) deflated over 11 tries. It's stronger than R63-1's 0.38, but those years
  alone still don't prove it.
- **Trading:** the groups held change in 11 months a year, and it trades about 4.7
  times the account's value a year. The lead over the market would vanish at a cost of
  about 0.89% a trade.
- **Tiny groups:** it held at least one group with fewer than 10 companies in 70% of
  months. The lead in those months was +4.5 a year, and +3.4 in the others. So tiny
  groups add to the lead, but they aren't the whole of it.

**Added after the run, for information only.** These are not tests, not tries, and
none of them replaces R65-1. They come from the scratch rebuild, at normal costs:

| Change | Yearly return | Steadiness |
|---|---|---|
| R65-1 as planned | 14.76% | 0.57 |
| Leave out groups with under 10 companies (known the month before) | 13.75% | 0.53 |
| Leave out groups with under 20 companies | 12.85% | 0.49 |
| Score skips 2 months instead of 1 | 14.65% | 0.56 |
| Top 6 of 30 | 14.97% | 0.49 |
| Top 12 of 30 | 14.00% | 0.56 |

Each one stays well above the 0.33 needed, so the pass doesn't hinge on these
particular settings or on the tiny groups.

## What round 65 shows

- **R65-1 is the first rule in this search to pass every test at both cost settings.**
  It beat the market by about 4 points a year over 99 years, in every quarter-century
  and every decade, and the luck check can tell it apart from luck even counting all
  11 tries.
- **The idea behind it worked as planned.** Spreading the same monthly bet over more
  groups made the lead steadier: 0.57 against R63-1's 0.35.
- **The cautions stay:**
  - It was chosen after rounds 63-64, on the same stocks and years.
  - It's a published idea, and the luck check counts only our tries.
  - The early decades are paper returns at costs nobody paid then.
  - **Nobody can buy these 30 groups directly.** They're Ken French's research
    portfolios, not funds, so a real version would need funds that roughly match them.
  - The years after publication are the most honest part, and they show +3.9 a year.
    But 27 years alone aren't enough to prove it.
- **The next evidence has to be new months,** by paper tracking, as the group planned
  for a winner.
