# Notes for Zach Cheney — Claude Trading Agent

**From:** Sam (written up by Claude at Sam's request)
**Date:** Wed Oct 21, 2026
**Status:** Day 1 of a live test. Small account, real money.

## What this is

Sam is testing Claude as an intraday trading agent on Robinhood. Sam writes the strategy, Claude follows it, and Sam approves every order on their phone.

- **Broker access:** Claude uses the Robinhood connector (MCP tools) for quotes, historical bars, technical indicators, VIX, earnings calendar, and orders.
- **Account:** only the Robinhood *agentic* account nicknamed "MCP" (ends 6604). Claude cannot trade Sam's other accounts; Robinhood shows them as read-only to the agent.
- **Size:** about $108 total, so trades are about $27–54 each and risk well under $1. The goal is to test the mechanics, not to make money.
- **Approval:** "trades require approval" is ON in the Robinhood app. Each order Claude sends appears in the app as a pending request, and Sam approves or declines it.

## How it runs

- Claude runs as a Claude Code cloud session (this repo, branch `claude/robinhood-trading-agent-jt8qqj`).
- It wakes itself with one-time scheduled messages: a market check at 9:00 ET, then every 15 minutes, and every 5 minutes while in a trade or when a setup is forming.
- Every check is written to `trading-agent/logs/YYYY-MM-DD.md` and pushed. Sam gets a status message in the chat about every 30 minutes, plus a phone notification whenever an order needs approval.

## The strategy (full text: [`STRATEGY.md`](STRATEGY.md))

Sam designed it with regular Claude and then pasted it in. It works in layers:

1. **Market read at 9:00 ET.** Ten signals score +1/−1 each: SPY vs. its 20/50/200-day averages, VIX, credit (HYG), breadth (RSP vs. SPY), defensive vs. cyclical sectors, the dollar (UUP), and bonds (TLT). The total sets the day: **GREEN** (full size), **YELLOW** (half size), or **RED** (no trades).
2. **Reasons to skip the day:** VIX above 25, SPY gapping more than 1%, Fed/CPI/PCE/jobs days, two or more megacaps reporting earnings, loss limits hit.
3. **Day type, from 10:30 ET:** TREND or RANGE, based on how SPY behaves around VWAP and its opening range. The day type decides which setups are allowed.
4. **Five entry setups.** A: opening-range breakout. B: VWAP pullback. C: afternoon continuation. D: range-day VWAP reversion. E: pullback in the strongest ETF. Each needs these market conditions, plus a score of at least 6 out of 10 on a checklist:
   - at least 5 of 9 sectors up
   - at least 3 of 6 megacaps above VWAP
   - VIX flat or falling
5. **Exits:** target 2× the risk. At +1R the stop moves to breakeven, and at +1.5R it trails. Early exit if two warning signs show up. Out of every trade by 3:45 ET, with nothing held overnight.
6. **Risk:** 0.5% of the account at risk per trade (half on YELLOW days), each trade capped at 50% of the account, one position at a time, at most 3 entries a day. Loss limits: **−$7.50 a day, −$25 a week.**
7. **Tradable:** SPY, DIA, QQQ, RSP, XLK, XLF. Long only: no options, margin, leveraged ETFs, or single stocks.
8. **Rotation (added today):** if the open trade is up at least $0.10, or has stalled for 30 minutes at breakeven or better, Claude may sell it and switch into a clearly better setup, one that scores at least 1 point higher. It never switches out of a losing trade.

## What happened on day 1

- **Pre-market:** score +1 → YELLOW day. Nothing triggered a skip.
- **Morning:** Sam sold the old BRK.B position by hand, so the account was all cash. The morning was choppy (a RANGE day), and Claude passed on several near-setups because they didn't meet the rules: low volume on the breakout, the reward too small for the risk, or VIX rising.
- **~11:27 ET:** SPY held above VWAP for 45 minutes and broke out of its opening range, so the day became **TREND**.
- **11:35 ET:** first live trade. **Setup A in SPY, score 6/10. Bought $54 (0.069938 sh) at $772.11.** Stop 770.48, target 775.37.
- At the time of writing it was up a few cents. The end-of-day log will have the result.

## Lessons learned (useful if you build something similar)

- **Robinhood can't approve fractional-share limit orders.** The app shows "0 shares / enter at least 1 share". With a small account, every order has to be a **market order**: dollar amounts for entries, the full share quantity for exits. This is now a rule.
- **Claude Code's own safety check** blocked one real-money order until Sam gave explicit go-ahead in the chat. Expect that the first time.
- **Some data isn't available:** VIX9D isn't in Robinhood's data (that signal scores 0), and there's no 15-minute bar size (proxied with the 10- and 30-minute EMAs).
- **Scheduled check-ins can fire 1–5 minutes late**, so stops are watched by Claude, not placed as resting orders. With approval on, a stop-out also waits for Sam's tap.
- **The pattern-day-trader rule:** FINRA dropped it as of June 2026, with brokers phasing the change in. The rules say to stop if Robinhood ever flags a day trade.

## Files

- [`STRATEGY.md`](STRATEGY.md): the full rules, plus every change Sam approved during the day, with timestamps.
- [`logs/2026-10-21.md`](logs/2026-10-21.md): the check-by-check log for today, with each market read, setup score, order, and fill.

Questions go to Sam.
