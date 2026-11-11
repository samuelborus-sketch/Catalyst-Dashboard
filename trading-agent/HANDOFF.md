# Trading agent handoff (written 2026-11-11)

Read this first, then `state.json`, `CLAUDE.md` (breakout) and `H7_RULEBOOK.md` (H7).
`state.json` is the source of truth; the journals are the history.

## Account
- Robinhood agentic account **"MCP" ••6604** (`account_number 954376604`). Never touch any other account.
- **Trade approvals are OFF** (Sam, 2026-10-29), so the mode is AUTO: the agent's orders execute without a tap.
  - Note: this Claude session's own safety check **blocked** an automatic market sell on 11/9 ("real-world transaction"). Expect a run to need Sam's explicit OK in chat for real orders unless the session's permissions allow it.
- Value **\$96.30** cash, flat (2026-11-11). Week start \$105.35. HWM \$108.84. Account floor \$81.30.

## Strategies (both live, same account)
1. **Breakout** (`CLAUDE.md`):
   - Morning 3× ETF breakout, threshold **10/14** (11/14 with a caution flag: VIX ≥ 25 or 2 losses in a row).
   - Dollar-based market orders, 99% of *free* cash; monitored stops every 3 min; flat by 12:00 ET.
   - `consecutive_losses` = 1.
   - `halted` = false (Sam cleared it 11/11).
2. **H7** (`H7_RULEBOOK.md`):
   - QLD while QQQ is above its 200-day average (size 20%/vol20, capped at 100%), else cash.
   - Experiment G calendar day trades in UPRO/SQQQ (buy at 9:30 open, sell 15:59).
   - Currently **cash**: QQQ 674.76 vs 200-day 681.42 on 11/10.
   - Next known signals: **Fri 11/20 SQQQ** (options expiry; skip if QQQ opens > 0.3% down), **Wed 11/25 UPRO** (pre-Thanksgiving), Fri 11/27 early close 13:00 ET, Dec 1–3 month start.
   - Loss limit: 50% below H7's high (\$52.68 now). Weekly brake: −10% on the account.

## Coexistence rules (CLAUDE.md §0A, H7 §7)
- **H7 signal day:** the MORNING run does H7 at 9:30 and skips the breakout.
- **Breakout** uses free cash only. QLD and `h7.position` belong to H7.
- **Backstops** handle the breakout only.

## Sam's standing decisions
- **Never change rules, thresholds or settings without asking Sam.** Report, don't advise trades for other accounts.
- **H7 runs live** with real money (11/7, his choice over a paper test).
- **Breakout keeps running** alongside H7.
- **Manual trades:** Sam sometimes trades by hand in this account (SOXS 11/6–11/9, −\$9.05). The rule for a held 8-ETF position at pre-flight is: sell at 9:30:15 and set `halted`. Better: ask Sam first (idea #2 below).
- **Fresh sessions per scheduled run:** Sam said yes via Middle Manager, 11/11, pending direct confirmation in chat. Wants usage minimized.

## Schedule (this session's scheduled tasks; ET)
| Task | When | trigger |
|---|---|---|
| MORNING | weekdays 8:52 | trig_01JCu3fmtfpPyVPxbFnW8U9j |
| BACKSTOP | weekdays 10:27 | trig_012cjYBcmcR5Hk13cc6jf8u6 |
| BACKSTOP | weekdays 12:17 | trig_01EQWQvuG7UhiY7nfa9FD2NG |
| H7 CLOSE | weekdays 15:22 | trig_0112xbknJEfNB5GBhVVB2sNQ |

All four fire into one long session. On 11/10 they were delivered about 20 h late (worker restarts). The plan is to move them to fresh sessions.

## Open items / ideas (Sam approved "implement all ideas to save usage", via Middle Manager)
1. Fresh session per run, reading state.json + rulebooks (in progress).
2. Manual-trade detection: alert Sam and tag `manual_positions` instead of auto-selling.
3. Allocation budget across H7 / breakout / manual.
4. Paper-shadow log of near-miss setups and R65-1 monthly picks (R65-1 is not traded).
5. One short daily status card.
