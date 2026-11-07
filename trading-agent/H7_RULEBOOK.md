# H7: Leveraged Nasdaq trend with calendar day trades (LIVE from 2026-11-09)

**Source:** Zach's Experiment H, version H7 (`zcheney000/Portfolio_Sentinel`, branch
`experiment-h-leveraged-trend`, `experiments/2026-10-30-experiment-h/README.md`), with
Experiment G's day-trade signals (`experiments/2026-10-29-experiment-g/README.md`).

**Sam's decision, 2026-11-07:** run H7 in the MCP account (••6604), live, with real
money, using the whole account. The morning breakout rulebook (`CLAUDE.md`) keeps running
in the same account under the coexistence rules in §7 below. Approvals are OFF, so the
mode is AUTO: orders execute without Sam's tap. Push-notify Sam on every H7 order.

**The honest caveats (from Zach's write-up):**
- Most of the extra return comes from leverage, not skill.
- The rules were found on the same data they were tested on.
- They failed or didn't help on 1986–1999.
- The 2× hold has no stop except the 200-day rule. The tests showed about a 1-in-5
  chance of a drop past −50% at some point.

---

## 1. Funds

| Role | Fund |
|---|---|
| Held between day trades | QLD (2× Nasdaq-100) |
| "Up" day trade | UPRO (3× S&P 500) |
| "Down" day trade | SQQQ (−3× Nasdaq-100) |

## 2. The held position (QLD)

- **Trend rule:**
  - QQQ's close above its 200-day simple average → hold QLD, including overnight.
  - Close at or below it → cash.
- **When to act:** check after each close. A change is made at the **next** trading day's close.
- **Size (set weekly):**
  - Share of the account in QLD = 20% ÷ QQQ's 20-day volatility (yearly figure, from
    daily log returns), never more than 100%.
  - Work it out from Thursday's close and change it at Friday's close.
  - The rest stays in cash.
- **No stop on QLD** other than the 200-day rule.

## 3. Day-trade signals (Experiment G, unchanged)

Each signal is known the evening before, except the gap checks, which use the 9:30 ET
opening prices.

| Signal | When | Gap check at 9:30 | Buys |
|---|---|---|---|
| Month start | Trading days 1–3 of the month, if SPY's 20-day volatility (up to yesterday) is 15–40% a year | none | UPRO |
| Dip bounce | SPY closed lower 3+ days in a row | skip if SPY opens > 0.3% above yesterday's close | UPRO |
| Pre-holiday | Last trading day before a weekday market holiday | none | UPRO |
| Options-expiry fade | Third Friday of the month (day 15–21) | skip if QQQ opens > 0.3% below yesterday's close | SQQQ |

- **Priority:** month start, dip bounce and options-expiry first. Pre-holiday only on a day none of them fires.
- **Conflict:** an up signal and the options-expiry signal on the same day → **no trade**.
- **Limit:** at most one day trade a day.

### H7's rule while holding QLD (from H6)
- **Above the 200-day average,** an **up** signal (UPRO) is **not traded**. Keep QLD; it's an ordinary holding day.
- **Options-expiry (SQQQ) days while holding:**
  1. At 9:30, if the gap check says trade, sell QLD and buy SQQQ (within 60 s).
  2. Sell SQQQ just before 4:00.
  3. Buy QLD back at the close.
  - The account is limited margin, so sale money can be reused the same day (Zach, 2026-10-31).
- **While in cash** (below the 200-day average), every signal trades at full size.

## 4. Execution

1. **Evening before:** work out tomorrow's possible signal and save it to
   `state.json → h7.next_signal` (with its gap rule).
2. **9:30:00 ET** (the MORNING run handles this; §7):
   - Read SPY's and QQQ's opening prices with a quote at 9:30:02–9:30:10.
   - Apply the gap check.
   - Within 60 s, send a **dollar-based market** buy: 99% of buying power after any QLD sale.
   - *Deviation from G:* G used a limit a little above the open. Fractional limit orders aren't usable here, so it's market.
3. **During the day:** check the day-trade fund every 3–5 minutes, with lean checks (quote + new 1-minute bars).
   - **Trade stop:** a completed 1-minute bar closes ≥ 5% below the buy price → sell now.
   - **Emergency stop:** the bid is ever ≥ 8% below the buy price → sell immediately.
   - *Deviation from G:* G checked every minute; we check every 3–5 minutes.
4. **Close:**
   - At **15:59:00 ET**, market-sell the day-trade fund.
   - Then buy QLD back if §2 says hold.
   - On an **early-close day** (e.g. Fri 2026-11-27, close at 13:00 ET), use 12:59.
5. **Holding changes** (trend flip or weekly size) are made with a market order at 15:59 ET on the action day.

## 5. Brakes

- **Weekly brake:** once the **whole account** is 10% down from the week's start (Monday open), no more day trades that week. The QLD holding stays.
- **H7 loss limit** (Zach's proposal; Sam to confirm): if the account falls 50% below its high since H7 started (`h7.equity_hwm`, updated after each close; now \$105.35 → **\$52.68**):
  - Set `h7.halted = true`, sell everything, tell Sam.
  - Only Sam clears it.

## 6. Bad data or broken orders

- **Stale quote or missing open price at 9:30:** no day trade that day; log it.
- **Order rejected / not filled within 60 s / account doesn't match:** stop, log it, push-notify Sam. Never resend blindly; use §2.9 of `CLAUDE.md` (ref_id idempotency).
- **The afternoon run can't place the 15:59 sell** (session down): the 12:17 ET BACKSTOP does **not** sell H7 day trades. The next run that sees an H7 day-trade fund held after 16:00 sells it at the next open and alerts Sam.

## 7. Living with the morning breakout (`CLAUDE.md`)

- **H7 signal days:**
  - The MORNING run executes H7 at 9:30 and **skips the breakout entirely**.
  - It stays in the session to monitor H7's stops until 15:59.
- **Other days:**
  - The breakout may trade only **free cash** = buying power not needed by H7 (QLD target \$ already held).
  - With H7 in cash, that is the whole account; with QLD at 61%, it is about 39%.
- **Positions:** the breakout and its BACKSTOPs ignore QLD and any fund recorded in `state.json → h7.position`. Those belong to H7.
- **Breakout circuit breakers** (weekly −6%, drawdown −15%, floor) count **breakout trades only** (`state.json → breakout_pnl`), so an H7 swing can't halt the breakout and vice versa.

## 8. Schedule (ET; Arizona is ET − 2 h until March)

| Run | When | Job |
|---|---|---|
| MORNING | weekdays 8:52 | breakout as usual; on an H7 signal day, H7 at 9:30 instead |
| BACKSTOPs | weekdays 10:27, 12:17 | breakout only; leave H7 positions alone |
| H7 CLOSE | weekdays 15:22 (waits to 15:59) | sell day-trade fund, apply QLD changes, then after 16:00 compute tomorrow's signal, the 200-day state and (Thursday) next size; journal; push |
