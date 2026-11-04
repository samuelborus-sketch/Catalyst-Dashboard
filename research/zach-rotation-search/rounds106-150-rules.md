# Rounds 106-150: a sealed search for higher return (written before round 106)

Asked by Zach on 2026-11-03, after round 105: "lets now go for 150, aiming to try to get
even higher return... I want to have at least 5 candidates and if we cant find 5 then
thats alright". His choices:

- **Return bar:** at least 1 point a year more than R65-1, with the worst drop capped.
- **Final test:** reuse 2000-2026 and the Fidelity funds, then paper tracking.
- **Finalists:** the top 5 by return gain.
- **Leverage:** asked what we did before. Every rule since round 59 has been unlevered,
  so candidates stay unlevered.

## Why a new bar

- **Rounds 66-105 judged steadiness:** how evenly a rule's lead over the market comes.
  That bar was a hard one, and no rule cleared it.
- **This search judges return:** the yearly gain over R65-1.
- **The drop cap stops "more return" meaning only "more risk."** R65-1's own worst drop
  was 76.2% over 1927-1999, so the cap is already generous.

## Rules for each round, 106 to 149

- **One candidate per round, written down before it runs.** Every candidate counts as a
  try; the count continues from 56.
- **The seal:** every round loads data through `scripts/sealed.py` (or the same cut in
  `scripts/sealed_return.py`), so nothing after 1999-12 is computed.
- **Judging, at doubled costs, over the candidate's first month to 1999-12, against R65-1
  over the same months:**
  - **G1:** yearly return at least R65-1's plus 1.0 point;
  - **G2:** worst drop no more than 5 points deeper than R65-1's;
  - **G3:** it beats the market in each development quarter-century;
  - **G4:** it beats R65-1's yearly return in each half, to 1963-12 and from 1964-01.
    This check is added to the bar Zach chose, carried over from rounds 80-104. Round 98
    showed how a gain found only before 1964 can fail later.
- **A candidate that passes all four goes on the shortlist.** Nothing more is run on it
  until round 150.
- **No leverage:** a candidate holds at most 100% of the account and never borrows.
- **The runs are done twice,** and accepted only if both give identical files.
- **Five rounds per batch.** Each batch's queue is written here before it runs.

## The final exam, round 150 (fixed now)

- **The finalists:** the 5 shortlisted candidates with the largest return gain over R65-1
  at doubled costs. Fewer than 5 on the shortlist means all of them go. An empty shortlist
  means no exam, and R65-1 stays the rule.
- **Each finalist gets one run, with no changes:**
  - **X1:** over 2000-01 to 2026-09 at doubled costs, a yearly return above R65-1's
    (12.19%), and a worst drop no more than 5 points deeper than R65-1's over the same
    months;
  - **X2:** round 65's four tests over the whole period, at both settings, with the luck
    check counting every try made by then;
  - **X3:** if it can be run on round 77's Fidelity funds (it uses only returns, and its
    own parameters): a yearly return at doubled costs above R65-1's 14.31%, a worst drop
    no more than 5 points deeper than R65-1's 48.5%, and round 77's F1-F4.
- **Every finalist that passes goes to paper tracking** beside R65-1, month by month. None
  replaces R65-1 until the group decides, from what paper tracking shows.
- **A weaker test than round 105's, said now:** 2000-2026 has judged candidates in rounds
  67, 70, 73 and 105, and the Fidelity data in round 105. Ideas here may also lean on what
  was learned from those years. Paper tracking is the only fully fresh test.

## Rounds 106-110, fixed on 2026-11-03 before they ran

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 106 | Top 3 | 57 | R65-1's score, holding only the 3 highest; concentration usually raises return and swings |
| 107 | Top 5 | 58 | The same, holding 5 |
| 108 | 49 finer industries, top 9 | 59 | R65-1's rule on Ken French's 49 industries (cut at 1999-12). A group qualifies with 12 months of returns before m and at least 5 firms at the end of m-1. Round 67 found that one- or two-company groups drove its early gains, hence the 5-firm floor |
| 109 | Last month's winners | 60 | Top 9 by the m-1 return alone. Moskowitz and Grinblatt (1999) found industries, unlike single stocks, tend to continue rather than reverse over one month. Trades a lot |
| 110 | Half in the top 3 | 61 | R65-1's top 9, but the top 3 hold half the money (1/6 each) and ranks 4-9 the other half (1/12 each) |

## Rounds 111-115, fixed on 2026-11-03 before they ran

Written after rounds 106-110's results, with round 106 (top 3) on the shortlist. Round 111
checks whether the jump from 5 groups to 3 is smooth. Rounds 113 and 114 build on round
106, and that's flagged here: building on a shortlisted rule makes a 1927-1999 win more
likely to be luck.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 111 | Top 4 | 62 | R65-1's score, holding the 4 highest. The top 3 gained +1.59 and the top 5 only +0.38, so this shows whether the gain fades smoothly or jumps |
| 112 | Leaders still rising | 63 | Take R65-1's top 9, then hold the 3 of them with the highest m-1 return. Round 96 found that dropping last month's biggest risers hurt, so this keeps them instead |
| 113 | 49 finer industries, top 5 | 64 | Round 108's rule (12 months of returns, at least 5 firms) holding 5 instead of 9 |
| 114 | Top 3, kept while in the top 6 | 65 | Round 106 with a buffer: a held group stays while it ranks 6th or better; empty places go to the best-ranked groups not held. Aims to keep round 106's return while cutting its 7 trades a year. Starts 1927-07 with the top 3 |
| 115 | Weighted by lead over the 10th | 66 | R65-1's top 9, each weighted by how far its score is above the 10th-ranked group's score, so the strongest get the most. A hunch between holding 9 equally and holding 3 |

## Rounds 116-120, fixed on 2026-11-03 before they ran

Written after rounds 111-115's results, with rounds 114, 106, 113 and 111 on the
shortlist. Rounds 117, 119 and 120 build on shortlisted rules, and round 116 extends the
same "fewer groups" idea; that's flagged here. Round 118 adds a market-trend switch, a
different kind of idea.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 116 | Top 2 | 67 | R65-1's score, holding the 2 highest. Shows whether the return keeps rising below 3 groups, and whether the drop cap stops it |
| 117 | Top 3, kept while in the top 9 | 68 | Round 114 with a wider buffer: a held group stays while it ranks 9th or better, i.e. while it's still one of R65-1's picks. Starts 1927-07 with the top 3 |
| 118 | Top 3 when the market is rising, else top 9 | 69 | Hold R65-1's top 3 when the market's value at the end of m-1 is above its average month-end value over m-10 to m-1 (Faber's 10-month average); otherwise hold R65-1's top 9. A hunch: concentrate when markets trend up, spread out when they don't. The share of months in each is reported |
| 119 | 49 finer industries, top 3, kept while in the top 6 | 70 | Round 114's buffer on round 113's groups (12 months of returns, at least 5 firms). A held group that stops qualifying is sold. Starts 1927-07 with the top 3 |
| 120 | Top 3, two overlapping months | 71 | Half in this month's top 3 and half in last month's top 3 (Jegadeesh and Titman's overlapping design, as round 84 did with 9). Starts 1927-08 |

## Rounds 121-125, fixed on 2026-11-03 before they ran

Written after rounds 116-120's results, with six rules on the shortlist (116, 120, 114,
106, 113, 111). Rounds 121, 122 and 125 push the "fewer groups" idea further and build on
round 116; rounds 123 and 124 try other scores with 3 groups. All of this is flagged: each
step on the same idea makes a 1927-1999 win more likely to be luck.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 121 | Top 1 | 72 | R65-1's score, holding only the single highest group. Shows where the drop cap stops the "fewer groups" trend |
| 122 | Top 2, kept while in the top 4 | 73 | Round 116 with round 114's kind of buffer: a held group stays while it ranks 4th or better; empty places go to the best-ranked groups not held. Starts 1927-07 with the top 2 |
| 123 | Top 3 by the no-skip score | 74 | Rank by the return over m-12 to m-1 (round 69's window, counting the latest month); hold the top 3 |
| 124 | Top 3 nearest their 12-month high | 75 | Rank by each group's value at the end of m-1 divided by its highest month-end value over m-12 to m-1, ties to the higher R65-1 score; hold the top 3. George and Hwang (2004) found nearness to the 52-week high predicted single stocks' returns; round 68 tried it with 9 groups |
| 125 | Top 2, two overlapping months | 76 | Half in this month's top 2 and half in last month's top 2 (round 120's design with 2). Starts 1927-08 |

## Rounds 126-130, fixed on 2026-11-03 before they ran

Written after rounds 121-125's results, with 9 rules on the shortlist and rounds 122, 116,
125, 120 and 114 in the exam's top 5. Rounds 126 and 127 check whether round 122's buffer
of 4 was a lucky choice. Rounds 128 and 130 put round 124's score on 2 groups, and round
129 tries R63-1's coarser groups. All build on shortlisted rules, which is flagged here.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 126 | Top 2, kept while in the top 3 | 77 | Round 122 with a narrower buffer. Starts 1927-07 with the top 2 |
| 127 | Top 2, kept while in the top 6 | 78 | Round 122 with a wider buffer. Starts 1927-07 with the top 2 |
| 128 | Top 2 nearest their 12-month high | 79 | Round 124's score (value at the end of m-1 over its highest month-end value in m-12 to m-1, ties to the higher R65-1 score), holding 2 |
| 129 | 10 broad industries, top 2 | 80 | R65-1's score on Ken French's 10 industries (round 63's file, cut at 1999-12), holding the 2 highest. Two of ten is a broader bet than two of thirty |
| 130 | Top 2 by two scores | 81 | Rank by R65-1's score and separately by nearness to the 12-month high; hold the 2 lowest rank sums, ties to the higher R65-1 score |

## Rounds 131-135, fixed on 2026-11-03 before they ran

Written after rounds 126-130's results, with 12 rules on the shortlist and rounds 130, 122,
116, 126 and 125 in the exam's top 5. Rounds 131-133 and 135 build on round 130's two
scores, and round 134 on round 122's buffer; all flagged. Stacking changes found on the
same data raises the chance that a 1927-1999 win is luck.

"Two scores" below means round 130's order: rank by R65-1's score and separately by
nearness to the 12-month high (value at the end of m-1 over the highest month-end value in
m-12 to m-1), sum the two ranks, lowest first, ties to the higher R65-1 score.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 131 | Two scores, top 2, kept while in the top 4 | 82 | Round 130's order with round 122's buffer, to cut round 130's 11 trades a year. Starts 1927-07 with the top 2 |
| 132 | Two scores, top 2, two overlapping months | 83 | Half in this month's top 2 by two scores, half in last month's. Starts 1927-08 |
| 133 | Two scores, top 3 | 84 | Round 130 holding 3 |
| 134 | 49 finer industries, top 2, kept while in the top 4 | 85 | Round 122's rule on round 113's groups (12 months of returns, at least 5 firms). A held group that stops qualifying is sold. Starts 1927-07 with the top 2 |
| 135 | Three scores, top 2 | 86 | Round 130's two ranks plus a third, last month's (m-1) return; hold the 2 lowest rank sums, ties to the higher R65-1 score |

## Rounds 136-140, fixed on 2026-11-03 before they ran

Written after rounds 131-135's results, with 16 rules on the shortlist and rounds 131, 130,
134, 122 and 116 in the exam's top 5. All five build on shortlisted rules (flagged). Rounds
138 and 139 check whether round 131's buffer and nearness window were lucky choices.
"Two scores" is round 130's order (see rounds 131-135 above). Every buffered round starts
in 1927-07 with the top of its order.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 136 | Two scores, top 3, kept while in the top 6 | 87 | Round 133 with round 114's buffer: round 133 was as steady as R65-1, and a buffer may cut its 9.5 trades a year |
| 137 | 49 finer industries, two scores, top 2, kept while in the top 4 | 88 | Round 131's rule on round 134's groups (12 months of returns, at least 5 firms); nearness uses the same 12 months. A held group that stops qualifying is sold |
| 138 | Two scores, top 2, kept while in the top 6 | 89 | Round 131 with a wider buffer |
| 139 | Two scores with a 6-month high, top 2, kept while in the top 4 | 90 | Round 131, but nearness measured against the highest month-end value in m-6 to m-1 |
| 140 | Nearest the 12-month high, top 2, kept while in the top 4 | 91 | Round 128's score alone (it fell 81.3%, 0.1 points past the cap) with round 122's buffer |

## Rounds 141-145, fixed on 2026-11-03 before they ran

Written after rounds 136-140's results, with 20 rules on the shortlist and the exam's top
5 unchanged (131, 130, 134, 122, 116). Round 140 (top 2 nearest the 12-month high, kept
while in the top 4) had the smallest worst drop of the search, 67.3%. These five change one
of its settings at a time, to see whether that drop and its +2.79 gain hold up nearby or
sit on a peak, as round 131's did. All build on round 140 (flagged). Every round starts
in 1927-07 with the top of its order. "Nearness" is round 124's score, ties to the higher
R65-1 score.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 141 | Nearest the high, top 2, kept while in the top 3 | 92 | Round 140 with a narrower buffer |
| 142 | Nearest the high, top 2, kept while in the top 6 | 93 | Round 140 with a wider buffer |
| 143 | Nearest the high, top 3, kept while in the top 6 | 94 | Round 140 holding 3 |
| 144 | 49 finer industries, nearest the high, top 2, kept while in the top 4 | 95 | Round 140 on round 134's groups (12 months of returns, at least 5 firms). A held group that stops qualifying is sold |
| 145 | Nearest the 6-month high, top 2, kept while in the top 4 | 96 | Round 140 measuring nearness over m-6 to m-1 |

## Rounds 146-149, fixed on 2026-11-03 before they ran

The last four sealed rounds, written after rounds 141-145's results. The exam's top 5 are
141, 131, 130, 134 and 122. Round 141 sat on a sharp spike. These rounds fill the gaps
around three other finalists, so the exam's results can be read against their
neighbours. All build on shortlisted rules (flagged), and each counts as a try. Every
round starts in 1927-07 with the top of its order.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 146 | Top 2, kept while in the top 5 | 97 | R65-1's score, between round 122 (top 4, +3.11) and round 127 (top 6, +2.01) |
| 147 | Two scores, top 2, kept while in the top 3 | 98 | Round 131 with a narrower buffer (its top 6 version, round 138, gained +1.94) |
| 148 | 49 finer industries, top 2, kept while in the top 3 | 99 | Round 134 with a narrower buffer |
| 149 | 49 finer industries, top 2, kept while in the top 6 | 100 | Round 134 with a wider buffer |

## Extended to round 200, fixed on 2026-11-03 before round 150 ran

Asked by Zach on 2026-11-03, after round 149: "lets make it 200, feel like the numbers kept
improving as we went". So:

- **Rounds 150-199 are sealed rounds** under the same rules as rounds 106-149 (G1-G4 on
  1927-1999, no leverage, five rounds per batch, each queue written here before it runs).
- **The final exam moves to round 200,** unchanged: the 5 largest gains on the shortlist
  each get one run under X1-X3. The luck check counts every try made by then. Passers go
  to paper tracking beside R65-1.
- **Nothing after 1999 has been computed** for any candidate, so moving the exam doesn't
  weaken it.
- **A caution, written now:** the best 1927-1999 gain rose from +1.59 (round 106) to +3.89
  (round 141). Part of that rise is expected from searching more on the same years:
  each new rule is built from what worked on them, so its 1927-1999 figure overstates
  what it would earn on unseen years. Only the exam can show how much is real.

## Rounds 150-154, fixed on 2026-11-03 before they ran

All build on shortlisted rules (flagged). They fill the remaining buffer gaps around the
finalists, and round 154 tries uneven amounts in the top 2. Every round starts in 1927-07
with the top of its order. "Two scores" is round 130's order.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 150 | Two scores, top 2, kept while in the top 5 | 101 | The gap between round 131 (top 4, +3.35) and round 138 (top 6, +1.94) |
| 151 | 49 finer industries, top 2, kept while in the top 5 | 102 | The gap between round 134 (top 4, +3.23) and round 149 (top 6, +1.48) |
| 152 | Top 3, kept while in the top 5 | 103 | R65-1's score, between round 106 (no buffer, +1.59) and round 114 (top 6, +1.69) |
| 153 | Two scores, top 3, kept while in the top 4 | 104 | Between round 133 (no buffer, +2.60) and round 136 (top 6, +1.43) |
| 154 | Top 2, kept while in the top 5, two-thirds in the leader | 105 | Round 146 with 2/3 of the money in the higher-ranked of the two holdings and 1/3 in the other, re-ranked each month |

## Rounds 155-159, fixed on 2026-11-03 before they ran

Written after rounds 150-154's results, with 28 rules on the shortlist and the exam's top
5 unchanged (141, 146, 131, 147, 130). Rounds 155-158 fill the last empty places in the
buffer table, so every finalist's neighbours are known. Round 159 checks whether round 146
depends on its exact score window. All build on shortlisted rules (flagged). Every round
starts in 1927-07 with the top of its order. "Two scores" is round 130's order and
"nearness" is round 124's score, ties to the higher R65-1 score.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 155 | Nearest the high, top 2, kept while in the top 5 | 106 | The gap between round 140 (top 4, +2.79) and round 142 (top 6, +0.50) |
| 156 | Top 3, kept while in the top 4 | 107 | R65-1's score, between round 106 (no buffer, +1.59) and round 152 (top 5, +2.60) |
| 157 | 49 finer industries, top 2 | 108 | Round 134's groups (12 months of returns, at least 5 firms) with no buffer, the empty place in that row |
| 158 | Two scores, top 3, kept while in the top 5 | 109 | Between round 153 (top 4, +2.35) and round 136 (top 6, +1.43) |
| 159 | Top 2 by a 6-month score, kept while in the top 5 | 110 | Round 146 with the score taken over m-7 to m-2 instead of m-12 to m-2 |

## Rounds 160-164, fixed on 2026-11-03 before they ran

Written after rounds 155-159's results, with 32 rules on the shortlist, the buffer table
complete and the exam's top 5 unchanged (141, 146, 131, 147, 130). Round 159 showed that
round 146 depends on its 12-month score. These five try new kinds of change: spreading
across three finalists (160), a score adjusted for how much a group swings (161), a
second check on the score windows of rounds 146 and 141 (162, 164), and a trend check on
each holding (163). All build on shortlisted rules (flagged). Every round starts in
1927-07 with the top of its order. "Two scores" is round 130's order and "nearness" is
round 124's score, ties to the higher R65-1 score.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 160 | A third each in rounds 146, 131 and 141 | 111 | Each third follows its own rule's holdings (top 2, with its own buffer), 1/6 per group; a group held by two rules gets both shares. One finalist from each family, so no single tuned setting carries the whole account |
| 161 | Top 2 by score over swings, kept while in the top 5 | 112 | Round 146's buffer, ranked by the m-12 to m-2 compounded return divided by the standard deviation (ddof=1) of the same 11 monthly returns |
| 162 | Top 2 by a 9-month score, kept while in the top 5 | 113 | Round 146 with the score taken over m-10 to m-2 |
| 163 | Round 146, each holding checked against its trend | 114 | Round 146's holdings, but a held group whose value at the end of m-1 is not above the average of its month-end values over m-10 to m-1 (round 92's check) has its half in the market that month |
| 164 | Nearest the 9-month high, top 2, kept while in the top 3 | 115 | Round 141 measuring nearness over m-9 to m-1 (round 145's 6-month version fell 85%) |

## Rounds 165-169, fixed on 2026-11-03 before they ran

Written after rounds 160-164's results, with 34 rules on the shortlist and the exam's top
5 at 141, 160, 146, 131 and 147. Round 160 (a third each in rounds 146, 131 and 141) gained
+3.83 and was the steadiest rule on the shortlist, but it's built from two finalists
that look tuned. These five check whether spreading across rules helps on its own, or
only with those exact settings. Rounds 166-168 give all three families the same buffer, so
none uses its peak setting by choice. All build on round 160 and other shortlisted rules
(flagged). Every round starts in 1927-07. Each part follows its own rule's holdings (top
2 of 30 groups), and a group held by two parts gets both shares. "R65-1's score",
"two scores" and "nearness" are the orders of rounds 146, 131 and 141.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 165 | Half each in rounds 146 and 141 | 116 | Round 160 without round 131's third: do the two tuned rules carry the gain? |
| 166 | A third each, all kept while in the top 4 | 117 | Rounds 122, 131 and 140: each family with the top-4 buffer |
| 167 | A third each, all kept while in the top 5 | 118 | Rounds 146, 150 and 155: each family with the top-5 buffer (round 150 alone broke the drop cap) |
| 168 | A third each, all kept while in the top 3 | 119 | Rounds 126, 147 and 141: each family with the top-3 buffer |
| 169 | Half in round 160, half in R65-1 | 120 | Round 160's holdings for half the money and R65-1's top 9 (1/18 each) for the other half, to see how much of the gain survives with far less concentration |

## Rounds 170-174, fixed on 2026-11-03 before they ran

Written after rounds 165-169's results, with 39 rules on the shortlist. Every blend so far
beat its parts' average by about 0.22 points a year. But the exam's top 5 (165, 141, 160,
146, 168) is now all rounds 141, 146 or blends of them. These five bring in round 134
(the 49 finer industries, a different set of groups), and two of them (173, 174) leave
out rounds 141 and 146 entirely. Round 172 gives round 165's two families their top-4
buffers instead of their peak settings. All build on shortlisted rules (flagged). Every
round starts in 1927-07.

- **How the 30- and 49-group rules are held together:** one account holds both sets of
  groups side by side. Each part follows its own rule (top 2, its own buffer) and gets an
  equal share, split equally between its two groups. Round 134's part keeps its own rules:
  12 months of returns and at least 5 firms, and a held industry that stops qualifying is
  sold.
- **A check made before any run:** each part, run alone in that combined account,
  reproduced its own round's 1927-1999 return exactly (rounds 146, 141, 134, 131, 122
  and 140).

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 170 | A third each in rounds 146, 141 and 134 | 121 | Round 160 with the 49-industry rule in place of round 131 |
| 171 | A quarter each in rounds 146, 131, 141 and 134 | 122 | Round 160 plus the 49-industry rule |
| 172 | Half each in rounds 122 and 140 | 123 | Round 165's two families, each with the top-4 buffer |
| 173 | Half each in rounds 131 and 134 | 124 | A blend with neither round 141 nor round 146 |
| 174 | A third each in rounds 131, 134 and 140 | 125 | A blend with neither round 141 nor round 146, one part from each family on the top-4 buffer |

## Rounds 175-179, fixed on 2026-11-03 before they ran

Written after rounds 170-174's results, with 44 rules on the shortlist. Every blend so
far beat its parts' average, and the exam's top 5 (165, 170, 141, 171, 160) all contain
round 141. Rounds 175-177 fill in the remaining blends with the 49-industry rule (134).
Rounds 178 and 179 try two new ways of splitting money between parts instead of equal
shares. All build on shortlisted rules (flagged). Parts, the combined 30-plus-49 account
and the part rules are as in rounds 170-174.

- **A part's own return** in a month is the average of its two groups' returns that month,
  before costs (each part resets to equal halves monthly).

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 175 | A quarter each in rounds 122, 131, 134 and 140 | 126 | Round 174 plus round 122: every family on the top-4 buffer, without 141 or 146 |
| 176 | Half each in rounds 141 and 134 | 127 | The pair missing from round 170 |
| 177 | Half each in rounds 146 and 134 | 128 | The other pair missing from round 170 |
| 178 | All in the best of rounds 146, 131 and 141 over the past 12 months | 129 | Each month, all the money follows the part with the highest compounded return over m-12 to m-1 (ties to 146, then 131). Starts 1928-07, the first month with 12 months of part returns. A hunch that rules, like industries, have runs |
| 179 | Rounds 146, 131, 141 and 134, each weighted by 1 / its swings | 130 | Each part's share is in proportion to 1 / the standard deviation (ddof=1) of its own returns over m-36 to m-1, so steadier parts get more. Starts 1930-07, the first month with 36 months of part returns |

## Rounds 180-184, fixed on 2026-11-03 before they ran

Written after rounds 175-179's results, with 49 rules on the shortlist and the exam's top
5 at 178, 165, 179, 170 and 141. Rounds 180 and 181 are the two pairs of finalists not yet
blended. Rounds 182-184 check round 178 (all in the part that did best over the past 12
months, +4.41, about 0.5 over equal thirds), which may be luck:
- 182 adds the 49-industry part;
- 183 puts only half the money in the leading part;
- 184 judges the parts over 6 months instead of 12.

All build on shortlisted rules (flagged). Parts, the combined account and part returns are
as in rounds 170-179.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 180 | Half each in rounds 146 and 131 | 131 | The last untried pair of round 160's parts |
| 181 | Half each in rounds 131 and 141 | 132 | The other untried pair |
| 182 | All in the best of rounds 146, 131, 141 and 134 over the past 12 months | 133 | Round 178 with the 49-industry part added (ties to 146, 131, 141, then 134). From 1928-07 |
| 183 | Half in the best of rounds 146, 131 and 141 over 12 months, half in equal thirds | 134 | A milder round 178 that keeps some spread. From 1928-07 |
| 184 | All in the best of rounds 146, 131 and 141 over the past 6 months | 135 | Round 178 judging the parts over m-6 to m-1. From 1928-01, the first month with 6 months of part returns |

## Rounds 185-189, fixed on 2026-11-03 before they ran

Written after rounds 180-184's results, with 54 rules on the shortlist. Following the part
that did best lately ("following the leader") beat equal shares in every version tried
(+0.32 to +0.54). But every version used rounds 141 and 146, which look tuned. These five
check it in other ways:
- 185 and 186 use parts with no 141 or 146 (the top-4 buffer versions, plus round 134);
- 187 holds the two leading parts instead of one;
- 188 puts the other half in R65-1 itself;
- 189 judges the parts over 9 months, between round 184's 6 and round 178's 12.

All build on shortlisted rules (flagged). Parts, the combined account and part returns are
as in rounds 170-184. Ties go to the earlier part in each list.

| Round | Candidate | Try | Idea |
|---|---|---|---|
| 185 | All in the best of rounds 122, 131 and 140 over 12 months | 136 | Following the leader without 141 or 146. From 1928-07 |
| 186 | All in the best of rounds 122, 131, 140 and 134 over 12 months | 137 | The same, adding the 49-industry part. From 1928-07 |
| 187 | Half each in the two best of rounds 146, 131, 141 and 134 over 12 months | 138 | Round 182 holding two leaders instead of one. From 1928-07 |
| 188 | Half in the best of rounds 146, 131 and 141 over 12 months, half in R65-1's top 9 | 139 | Round 178 with half the money in R65-1 (1/18 per group). From 1928-07 |
| 189 | All in the best of rounds 146, 131 and 141 over 9 months | 140 | Round 178 judging the parts over m-9 to m-1. From 1928-04 |
