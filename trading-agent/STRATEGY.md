# Index ETF Intraday Strategy — Agent Rules

Source of truth for the Claude trading agent. Rules below are the user's, verbatim
except where an **[Implementation note]** records a tool limitation. Never change a
rule without the user's explicit OK.

Account: Robinhood Agentic account "MCP" (ends 6604). Never touch any other account.
All times US Eastern. Trade approval in the Robinhood app is ON — every order the
agent places waits for the user to approve it in the app.

## ONE-TIME TASK (first morning only — Wed 2026-10-21)
- Sell 0.15 sh of the BRK.B position (0.2 sh → 0.05 sh remaining) after 9:45 ET. (Changed from 0.1 sh at the user's request on 2026-10-20.)
- Limit order at the bid. If fractional limit orders aren't allowed, use a market order during regular hours only.
- Confirm the fill and new buying power, then report.

## TRADABLE UNIVERSE (long only)
SPY, DIA, QQQ, RSP. No shorting, options, margin, crypto, leveraged or inverse ETFs, or single stocks.

## WATCH-ONLY (signals, never traded)
- Volatility: VIX, VIX9D
- Intermarket: TLT, HYG, UUP, GLD
- Sectors: XLK, XLF, XLE, XLV, XLI, XLY, XLP, XLU, SMH
- Breadth: RSP vs SPY, IWM vs SPY
- Megacaps: AAPL, MSFT, NVDA, AMZN, GOOGL, META

**[Implementation note]** VIX9D is not available through the Robinhood tools (VIX is).

## USER-APPROVED CLARIFICATIONS (2026-10-20)
1. Regime signal 5 (VIX9D below VIX) scores 0 while VIX9D is unavailable; thresholds unchanged.
2. Exits: if the limit-at-bid exit is rejected or unfilled after ~1 minute, sell at market (regular hours).
3. Entries: limit at the ask; if fractional limits are rejected, use a market order (regular hours).

## LAYER 1: DAILY REGIME (9:00 ET)
Score each +1 / −1:
1. SPY above 20-day SMA
2. SPY 20-day SMA above 50-day SMA
3. SPY above 200-day SMA
4. VIX below 20 and below its 10-day average
5. VIX9D below VIX
6. HYG above 20-day SMA
7. RSP 5-day return ≥ SPY 5-day return
8. XLU+XLP underperforming XLY+XLI over 5 days
9. UUP not up more than 1% over 5 days
10. TLT not down more than 2% over 5 days

≥ +5 GREEN (normal size, all setups) · +1 to +4 YELLOW (half size, A and B only) · ≤ 0 RED (no trades).

## LAYER 2: DAY FILTERS (skip the day if any true)
- VIX > 25, or VIX up > 15% pre-market
- SPY gap > 1.0% either way
- FOMC decision, CPI, PCE, or jobs report today
- Two or more megacaps reported after yesterday's close
- Half-day session or holiday
- Daily or weekly loss limit already hit

## LAYER 3: INTRADAY CONTEXT (every 15 min)
Each ETF vs session VWAP; 5-min 9 EMA vs 20 EMA; 5-min RSI(14); 9 sectors ranked by % change and count green;
megacaps above VWAP (of 6); VIX direction since open; relative volume vs 10-day average at same time of day.

## LAYER 4: ENTRY SETUPS
All require: regime GREEN/YELLOW, ≥ 5/9 sectors green, ≥ 4/6 megacaps above VWAP, VIX flat/falling since open, setup score ≥ 7/10.

**A — Opening Range Breakout (9:45–11:30).** OR = 9:30–9:45 high/low; skip if width < 0.15% or > 0.8%.
Trigger: 5-min close above OR high, above VWAP, volume > prior 3-candle avg. Stop: tighter of OR midpoint or 0.5% below entry.

**B — VWAP Pullback (10:00–14:30).** Above VWAP 30+ min with 9 EMA > 20 EMA; pulls back within 0.1% of VWAP or 20 EMA with RSI 40–55.
Trigger: 5-min candle closes back up off the level, above prior candle's high. Stop: 0.15% below VWAP or pullback low, whichever lower, max 0.5%.

**C — Afternoon Continuation (14:00–15:15, GREEN only).** Up > 0.4% on day, above VWAP all afternoon, higher highs.
Trigger: 5-min close above day's high. Stop: 0.4% below entry or below VWAP, whichever tighter.

## SETUP SCORE (1 pt each, need 7+; log every setup seen)
1. Regime GREEN · 2. Strongest of the 4 ETFs today · 3. RSP outperforming SPY intraday · 4. Leading sector cyclical (XLK/SMH/XLF/XLY/XLI)
5. Relative volume ≥ 1.0 · 6. 5-min RSI 50–70 · 7. 15-min 9 EMA > 20 EMA · 8. HYG green · 9. TLT not down > 0.5% · 10. No megacap down > 2%

## EXITS (check every 5 min in a position)
- Target 2R (R = entry − stop). At +1R stop → breakeven. At +1.5R trail at 5-min 9 EMA.
- Early exit if 2+ of: VIX +5% from entry, 5-min close below VWAP, sectors green < 4, HYG red.
- Hard flat by 15:45. Never hold overnight.
- Stops are monitored by the agent (not resting orders); exit with a limit at the bid.

## POSITION SIZING
Risk 0.5% of equity; shares = (equity × 0.005) ÷ (entry − stop), capped at 50% of equity.
YELLOW: halve. After 2 straight losses: halve until next win.

## HARD RISK LIMITS
- One position at a time, max 3 entries/day, max 1 per setup type
- Daily loss −$5 → stop for the day (changed from −2% at the user's request on 2026-10-21)
- Weekly loss −$25 → stop and wait for user go-ahead (changed from −5% at the user's request on 2026-10-21)
- No re-entry in the same ETF within 30 min of a stop-out
- Stop and message the user on: order rejected, day-trade/margin flag, stale data, anything unclear

## SCHEDULE & REPORTING
- 9:00 regime check; 9:20 morning report; checks every 15 min (5 min in a position or when a setup is forming); 15:50 EOD report.
- Each fill: ETF, setup, score breakdown, qty, fill, stop, target, R, reasoning.
- Each exit: fill, P&L $ / % / R, reason.
- EOD: trades, skipped setups + scores, P&L, equity, weekly running P&L, one-line market note.
- Friday: weekly summary — win rate, avg R, which setups/signals worked.

---

## ADDENDUM (2026-10-21 ~10:30 ET) — overrides the rules above where they conflict

**Account:** one-time BRK.B task is void (user sold all manually). Account is all cash (~$108).
**Heartbeat:** log one line at every check (time, regime, day type, setups watched, score, action). Status message to the user every 30 min, even with no trade.

**Tradable universe (long only):** SPY, DIA, QQQ, RSP, XLK, XLF.

**Loosened gates:** setup score threshold 6/10 · megacaps above VWAP ≥ 3/6 · sectors green ≥ 5/9 (unchanged) ·
score item 10 = "no more than one megacap down 2%+" · Setup A window extended to 12:00 ET.

**Day-type classifier** (10:30 ET, then every 30 min):
- TREND: SPY above or below VWAP 45+ consecutive min AND outside its OR → Setups A, B, C
- RANGE: SPY crossed VWAP 3+ times in the first hour AND inside/near its OR → Setups D and E only

**Setup D — Range-day VWAP reversion** (RANGE only, 10:30–14:30; SPY or RSP; max 1/day):
price ≥ 0.20% below session VWAP and at/near OR low, 5-min RSI(14) ≤ 35, then a green 5-min close above the prior candle's high.
Target VWAP. Stop 0.20% below the pullback low, max 0.35% from entry. Need target ≥ 1.2R.

**Setup E — Relative-strength leader pullback** (any day type, 10:30–14:30):
strongest of QQQ/XLK/XLF by % on day; must be up ≥ 0.4% and beat SPY by ≥ 0.3%.
Pulls back to within 0.10% of its VWAP or 5-min 20 EMA while staying above VWAP, then a 5-min close above the prior candle's high.
Stop 0.15% below VWAP, max 0.5% from entry. Target 2R or day's high, whichever closer; need ≥ 1.5R.
Skip if more than 1 of NVDA/AAPL/MSFT/META is red on the day.

**Earnings caution:** META and TSLA report after the close today → no new QQQ/XLK entries after 14:30 ET today.
Thu Oct 22: run the regime check but skip the day if META or TSLA moves more than ±5% pre-market.

**Risk (addendum restates):** 0.5% risk (half in YELLOW), max 50% of equity per position; one position; max 3 entries/day;
−2% daily / −5% weekly; flat by 15:45; limit orders, self-monitored stops, exit with limit at the bid.
**[Resolved 2026-10-21 ~10:50 ET]** User set loss limits: **daily −$7.50, weekly −$25** (these replace the addendum's −2%/−5% and the earlier −$5 daily).

**Before every order:** message the user "SETUP [X] in [ETF] | score [n]/10 | entry [x] | stop [x] | target [x] | R:R [x]", then submit.

**[User rule 2026-10-21 11:35 ET] Order type:** all orders are **market orders, regular hours**. Entries are **dollar-based** (dollar_amount = position size).
Exits sell the full share quantity held, at market. (The Robinhood app cannot approve fractional-share limit orders.)

**[User rule 2026-10-21 ~11:42 ET] Rotation ("swap to a better trade"):** still one position at a time. While in a position, keep scanning all setups.
Rotate (market-sell the current position, then enter the new one) only when ALL are true:
1. Current trade is **up ≥ +0.5R** (unrealized).
2. Current trade is **stagnant**: no new high since entry-high for the last 3 five-minute bars (15 min) AND it has not reached +1R.
3. The new setup fully qualifies (all gates, its own trigger, R:R rules) and **scores ≥ the current trade's score + 1**.
4. An entry is still available (max 3/day; the rotation's new entry counts) and the new setup type hasn't been used today.
Message the user before both orders ("ROTATE: exit X (+$ / +R, stagnant) → SETUP Y in Z | score | entry | stop | target | R:R").

**[User update 2026-10-21 ~11:48 ET] Rotation thresholds (replace items 1–2 above):**
- Rotation-eligible when the open trade is **up ≥ +$0.10** (unrealized), OR it has been **stagnant 30 min** (no new high since entry for 6 five-minute bars) **and is at or above breakeven**.
- **Never rotate out of a red trade.** If stagnant in the red but the thesis still holds (setup structure intact, early-exit rules not triggered), stay in; the stop governs.
- Items 3–4 unchanged: the new setup must fully qualify and score ≥ current + 1; an entry must be available.

**[User rule 2026-10-21 ~12:36 ET] Thesis-based exit on the open trade:** "If signs still show it should go up, hold; if not, sell."
Each check, judge the bullish thesis. **Sell (market, full qty) if ANY of these break:**
- 5-min close back below the breakout level (Setup A: OR high), or below the 5-min 20 EMA with 9 EMA crossing under 20 EMA;
- 5-min close below VWAP;
- any one early-exit warning (VIX ≥ +5% from entry level, sectors green < 4, HYG red) together with price below the 20 EMA.
Otherwise hold. Hard stop / target / 15:45 rules still apply. Message the user with the reason before selling.
