# 0DTE 14:00 bull put spread (Sam, 2026-11-12) — the ONLY active strategy

Breakout (CLAUDE.md) and H7 (H7_RULEBOOK.md) are retired; their 4 scheduled tasks are disabled.
Account: MCP ••6604 only.

- Tickers: SPY, QQQ, IWM, on days each has same-day-expiry options.
- 14:00 ET: short put at or just below (price − 2-hour expected move from implied vol); long put $1 lower. Target credit ~$0.10.
- Size: ≤12% of account per ticker, ≤14% total per afternoon, measured as max loss ($100 − credit per spread).
- Limit orders only, at the mid. Cancel if the fill would be > $0.01 worse than the target credit. No chasing.
- Hold to expiry. 16:05 ET: log P&L, fills, slippage to journal/.
- Sam: minimal messages; only alert on fills, rejections, or anything blocking.

## Blockers (2026-11-12)
1. The MCP account has **no options approval**; spreads usually need Level 3.
2. At $96.30, 14% = $13.48 < ~$90 max loss of one spread → **0 contracts**. One spread needs ≳ $650.
The 14:00 task is not scheduled until both are cleared.
