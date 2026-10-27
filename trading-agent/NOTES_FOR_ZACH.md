# Notes for Zach Cheney: Claude Trading Agent

**From:** Sam (written up by Claude at Sam's request)
**Updated:** Tue Oct 27, 2026
**Status:** Live on a small account (about \$108). Every order needs Sam's approval in the Robinhood app.

The full rulebook the agent follows is [`CLAUDE.md`](CLAUDE.md). This note explains it in plain English and covers what happened in week 1.

---

## 1. What this is

- **The agent** is Claude running as a Claude Code cloud session on this repo, branch `claude/robinhood-trading-agent-jt8qqj`.
- **Market data and orders** go through the **Robinhood MCP connector**: quotes, 5-minute bars, VWAP/EMA/ATR, VIX, the earnings calendar, and order placement.
- **Account:** only Sam's Robinhood **agentic account "MCP" (ends 6604)**. Sam's other accounts are read-only to the agent.
- **Approvals:** "trades require approval" is ON. The agent sends an order, Sam gets a push notification, and Sam taps approve in the app. Nothing executes without Sam.
- **Scheduling:** the agent wakes itself with scheduled messages. MORNING runs at 9:00 ET. BACKSTOP runs at 10:30 and 12:15 ET as a safety net that flattens anything left open if the morning session died.

## 2. The strategy: "Morning Leveraged-ETF Breakout"

**Idea:** take one high-conviction trade per morning, all-in, in a 3× index ETF. Skip the chaotic first 15 minutes, use that range as the map, and only buy confirmed breakouts that have volume, trend and the rest of the market behind them. No-trade days are normal.

### Universe: 4 pairs, buy side only
| Underlying (watched) | Bull 3× | Bear 3× |
|---|---|---|
| QQQ (Nasdaq-100) | TQQQ | SQQQ |
| SPY (S&P 500) | UPRO | SPXU |
| SOXX (semiconductors) | SOXL | SOXS |
| IWM (Russell 2000) | TNA | TZA |

A bearish view is expressed by **buying** the bear ETF. The agent never shorts and never uses options or margin.

### Daily timeline (ET)
1. **9:00 pre-flight:**
   - Account and flags.
   - Holiday check.
   - Economic calendar: no entries from 5 minutes before to 15 minutes after any scheduled release inside the window.
   - Earnings.
   - VIX: 35 or higher means no trading; 25 or higher means caution.
   - Daily ATR(14), EMA(20) and SMA(50).
   - 10-day opening-range volume baseline.
2. **9:30–9:45 opening range (OR):** no orders. Record the OR high, low, middle and width, plus relative volume (RVOL).
3. **9:50–11:00 entry window:** the agent checks 10 seconds after **every 5-minute bar close**.
4. **Manage the trade,** with a hard exit at **12:00 ET**. Nothing is ever held overnight.

### Entry gates (all must pass)
- **G1:** a bar closes above the ETF's OR high.
- **G2:** the ETF is above its VWAP, and the underlying is on the matching side of its own VWAP.
- **G3:** the stop is at the OR middle, clamped to 0.75–2.0% below entry.
- **G4:** no chasing. The ask must be ≤ OR high + ½ OR width.
- **G5:** account risk ≤ 2%.
- **G6:** the spread is ≤ 0.10% and the quote is fresh.
- **G7:** no event blackout and no circuit breaker. One entry per day.

### Score (0–14); need ≥ 10, or ≥ 11 when a caution flag is on
- RVOL of the underlying: 2 points.
- Trend stack (price, EMA20 and SMA50): 2 points.
- The other three underlyings confirming the direction (VWAP and OR middle): 2 points.
- Beyond the prior day's high or low: 1 point.
- VIX moving the right way: 1 point.
- Tight opening range (≤ 35% of ATR): 1 point.
- Strong breakout bar on volume: 1 point.
- **Volume block (added Oct 27), 1 point each:**
  - OBV makes a new session high along with the price.
  - MFI(14) is between 50 and 80, so buying is not stretched.
  - Dips happen on lighter volume than the moves up.
  - The traded fund's recent volume is stronger than its twin's (for example, SOXS vs. SOXL).
- Volume profile, breadth and Level 2 aren't available through the connector, so they aren't used.

### Sizing (changed Oct 23)
- **Dollar-based market order for 99% of buying power,** in fractional shares. It's all-in every trade, which means about 300% exposure to the index.
- The stop is the risk dial: a normal stop-out costs about 1–2% of the account.

### Managing the trade
- **Monitored stop:** Robinhood can't hold a stop order on fractional shares, so the agent watches the stop itself.
  - It checks every **3 minutes** and sells as soon as the bid touches the stop.
  - **Disaster rule:** exit immediately if price gaps 1.5× past the stop.
- **Stop moves:**
  - At +1R the stop moves to breakeven.
  - At +2R it starts trailing 1R behind the highest high, tightening to 0.75R after +3R.
- **Other exits:**
  - VWAP failure while the trade is under +0.5R.
  - **Time stop:** 45 minutes without reaching +1R.
  - **Market-flip exit:** 3 of the 4 indexes reverse and VIX moves against the trade.
  - The 12:00 hard exit.
- **Lean in-trade checks:** while in a trade, each check pulls only the held ETF, the 4 underlyings in a single quote call, and VIX. This saves usage.

### Circuit breakers
- 2 losses in a row → threshold 11.
- 3 losses in a row → skip the next session.
- Down 6% for the week → done for the week.
- Down 15% from the high-water mark → HALT.
- Below the account floor (\$81.30) → HALT.
- Only Sam can clear a HALT.

## 3. How it evolved during week 1

| When | Change | Why |
|---|---|---|
| Wed 10/21 | v1 was a looser multi-setup intraday ETF strategy, with SPY and QQQ trades | It worked but was busy and used a lot of Claude usage |
| Wed 10/21 | Moved to market orders | The Robinhood app **can't approve fractional-share limit orders** |
| Wed night | v2 rulebook (above) adopted. Went live instead of simulating, at Sam's call | Focus on one morning trade |
| Wed night | Removed approval deadlines and added push alerts for every order | Sam can't know when an order will come |
| Thu 10/22 | Entry scans went from 8 minutes to **5 minutes on bar closes** | The 8-minute gap missed a valid SQQQ breakdown and pushed it past the no-chase limit |
| Fri 10/23 | **Dollar-based, whole-account sizing**, plus monitored stops | Whole-share sizing on a \$108 account made the S&P and chip pairs unaffordable |

## 4. Week 1 results

- **System trades (v2 rules): 0.** Thursday had a valid setup (SQQQ, 7/10), but the 8-minute check gap missed the entry. Friday was a low-volume chop day, and nothing scored above 5.
- **Sam's manual trades:**

| Day | Trades | Result |
|---|---|---|
| Wed (v1) | SPY +\$0.125, QQQ −\$0.20 | −\$0.08 |
| Thu | TQQQ +\$0.44, then a TQQQ re-entry −\$1.83 (held past the planned stop) | −\$1.39 |
| Fri | 5 quick scalps (4× SOXS, 1× SQQQ), each held under about 70 seconds, 5/5 winners | +\$1.11 |

- The account is about **\$108.12** (it started the week at \$108.40).

## 5. Lessons (useful if you build something similar)

1. **Fractional shares through this connector:** market orders only, and no resting stop orders. Plan for agent-monitored stops.
2. **Check timing matters for breakout strategies.** Check right after each bar closes. Checking more often between closes adds nothing, because the rules only act on completed bars.
3. **Usage is the real constraint.** Keep checks lean when flat. Spend usage on watching an open trade.
4. **Cloud sessions restart sometimes.** Scheduled wakes can drop, so keep a backstop run, and keep `state.json` as the source of truth.
5. **The pattern-day-trader rule:** FINRA replaced it on June 4, 2026, and Robinhood says there are no day-trade limits now. The agent still stops if Robinhood ever shows a flag.
6. **Claude Code's own safety check** sometimes blocks risk-loosening edits until the human confirms explicitly. Expect that.
7. **Manual trades followed the playbook only some of the time.** The −\$1.83 came from buying a dip below VWAP on a down-trending day and holding past the stop. The rules exist for exactly that situation.

## 6. Files

- [`CLAUDE.md`](CLAUDE.md): the complete rulebook (source of truth).
- `state.json`: flags, high-water mark, opening-range volume history, today's levels, any open trade.
- `journal/YYYY-MM-DD.md`: every check, candidate score, order and fill.
- `logs/2026-10-21.md`: the v1 day log.
- [`STRATEGY_v1_archived.md`](STRATEGY_v1_archived.md): the retired v1 strategy.

Questions go to Sam.
