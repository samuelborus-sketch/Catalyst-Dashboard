"""Today's play for the 3x morning playbook, from live inputs. Prints one JSON object.

Example:
  python live_signal.py --date 2026-11-20 --spy-closes 761.2,...,772.31 --spy-open 771.9 \
      --qqq-prev-close 725.61 --qqq-open 726.0 --equity 105.35 --week-start-equity 105.35

--spy-closes: at least 21 completed SPY closes, oldest first, the last one being the previous session.
Omit --spy-open/--qqq-open before 9:30 ET to see which plays are candidates.
"""
import argparse
import datetime as dt
import json
import math
import statistics

NYSE_HOLIDAYS = {
    "2025-01-01", "2025-01-09", "2025-01-20", "2025-02-17", "2025-04-18", "2025-05-26", "2025-06-19", "2025-07-04",
    "2025-09-01", "2025-11-27", "2025-12-25",
    "2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25", "2026-06-19", "2026-07-03", "2026-09-07",
    "2026-11-26", "2026-12-25",
    "2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31", "2027-06-18", "2027-07-05", "2027-09-06",
    "2027-11-25", "2027-12-24",
}
DAILY_STOP = -0.05
WEEKLY_STOP = -0.10
MONTH_START_DAYS = 3
VOL_BAND = (0.15, 0.40)
DIP_STREAK = 3
NO_CHASE = 0.003


def is_open(d, holidays=NYSE_HOLIDAYS):
    return d.weekday() < 5 and d.isoformat() not in holidays


def trading_day_of_month(d, holidays=NYSE_HOLIDAYS):
    return sum(is_open(d.replace(day=k), holidays) for k in range(1, d.day + 1))


def is_third_friday(d):
    return d.weekday() == 4 and 15 <= d.day <= 21


def down_streak(closes):
    n = 0
    for prev, cur in zip(reversed(closes[:-1]), reversed(closes[1:])):
        if cur < prev:
            n += 1
        else:
            break
    return n


def realized_vol20(closes):
    rets = [b / a - 1 for a, b in zip(closes[:-1], closes[1:])][-20:]
    return statistics.stdev(rets) * math.sqrt(252)


def decide(date, spy_closes, spy_open=None, qqq_prev_close=None, qqq_open=None, equity=1.0, week_start_equity=1.0,
           holidays=NYSE_HOLIDAYS):
    if len(spy_closes) < 21:
        raise ValueError("need at least 21 completed SPY closes")
    out = dict(date=date.isoformat(), play="CASH", symbol=None, reasons=[])
    if not is_open(date, holidays):
        out["reasons"].append("market closed today")
        return out
    week_pnl = equity / week_start_equity - 1
    out["week_pnl"] = round(week_pnl, 5)
    if week_pnl <= WEEKLY_STOP:
        out["play"] = "LOCKED_FOR_WEEK"
        out["reasons"].append(f"account {week_pnl:.2%} since Monday's open, at or past the -10% weekly lock")
        return out
    stop = max(DAILY_STOP, (1 + WEEKLY_STOP) / (1 + week_pnl) - 1)
    out["stop_pct"] = round(stop, 5)
    tdom = trading_day_of_month(date, holidays)
    opex = is_third_friday(date)
    streak = down_streak(spy_closes)
    rv20 = realized_vol20(spy_closes)
    out.update(trading_day_of_month=tdom, opex_friday=opex, spy_down_streak=streak, spy_vol20=round(rv20, 4))

    month_start = tdom <= MONTH_START_DAYS and VOL_BAND[0] <= rv20 <= VOL_BAND[1]
    if tdom <= MONTH_START_DAYS:
        out["reasons"].append(f"month-start window, 20d vol {rv20:.1%} " + ("inside" if month_start else "outside") + " 15-40%")
    dip_setup = streak >= DIP_STREAK
    if dip_setup:
        out["reasons"].append(f"SPY down {streak} closes in a row")
    if opex:
        out["reasons"].append("monthly options-expiration Friday")

    if spy_open is None or (opex and qqq_open is None):
        pending = []
        if dip_setup:
            pending.append("DIP_BOUNCE")
        if opex:
            pending.append("OPEX_FADE")
        out["play"] = "WAIT_FOR_OPEN" if pending else ("MONTH_START" if month_start else "CASH")
        out["candidates"] = pending + (["MONTH_START"] if month_start else [])
        if out["play"] == "MONTH_START":
            out["symbol"] = "SPXL"
        return out

    spy_gap = spy_open / spy_closes[-1] - 1
    out["spy_gap"] = round(spy_gap, 5)
    dip = dip_setup and spy_gap <= NO_CHASE
    if dip_setup and not dip:
        out["reasons"].append(f"SPY opened {spy_gap:+.2%}, more than +0.3%: skip the dip")
    bear = False
    if opex:
        qqq_gap = qqq_open / qqq_prev_close - 1
        out["qqq_gap"] = round(qqq_gap, 5)
        bear = qqq_gap >= -NO_CHASE
        if not bear:
            out["reasons"].append(f"QQQ opened {qqq_gap:+.2%}, more than -0.3%: skip the fade")
    bull = month_start or dip
    if bull and bear:
        out["play"] = "CASH"
        out["reasons"].append("bull and bear plays both qualify: stay in cash")
    elif bull:
        out["play"] = "DIP_BOUNCE" if dip else "MONTH_START"
        if dip and month_start:
            out["play"] = "MONTH_START+DIP"
        out["symbol"] = "SPXL"
    elif bear:
        out["play"] = "OPEX_FADE"
        out["symbol"] = "SQQQ"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True)
    ap.add_argument("--spy-closes", required=True)
    ap.add_argument("--spy-open", type=float)
    ap.add_argument("--qqq-prev-close", type=float)
    ap.add_argument("--qqq-open", type=float)
    ap.add_argument("--equity", type=float, default=1.0)
    ap.add_argument("--week-start-equity", type=float, default=1.0)
    a = ap.parse_args()
    closes = [float(x) for x in a.spy_closes.split(",") if x.strip()]
    res = decide(dt.date.fromisoformat(a.date), closes, a.spy_open, a.qqq_prev_close, a.qqq_open, a.equity,
                 a.week_start_equity)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
