"""H7 (Zach's Experiment H) rebuilt on daily bars, plus Sam's variant (full-size hold, -10% day stop, -20% hold stop).

Day trades: Experiment G's signals (month start, dip bounce, pre-holiday -> 3x S&P; options-expiry fade -> 3x short
Nasdaq), H6/H7's stay-put rule. Held fund: 2x Nasdaq-100 while QQQ is above its 200-day average (decided at a close,
acted on at the next close). Funds are modeled from SPY/QQQ daily moves with the daily-reset formula.
"""
import os
import sys
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "leveraged-etf-playbook", "data")


@dataclass
class P:
    sized: bool = True            # H7: hold share = min(1, 20% / QQQ 20-day vol), set weekly
    day_stop: float = -0.05
    hold_stop: float = None       # e.g. -0.20 from the hold's entry; None = no stop
    rt_cost: float = 0.0010       # per round trip
    stop_slip: float = 0.0025
    hold_drag: float = 0.02       # yearly fee + financing drag on the 2x fund
    weekly_brake: float = -0.10


def load(sym):
    return pd.read_csv(os.path.join(DATA, f"{sym}.csv"), parse_dates=["date"]).set_index("date")


def build():
    spy, qqq = load("SPY"), load("QQQ")
    d = pd.DataFrame(index=spy.index)
    for s, df in (("s", spy), ("q", qqq)):
        pc = df.close.shift(1)
        d[f"{s}_co"] = df.open / pc - 1
        d[f"{s}_cc"] = df.close / pc - 1
        d[f"{s}_lo"] = df.low / pc - 1
        d[f"{s}_hi"] = df.high / pc - 1
    r = spy.close.pct_change()
    d["rv20"] = r.rolling(20).std().shift(1) * np.sqrt(252)
    dn = (spy.close < spy.close.shift(1)).astype(int)
    d["streak"] = (dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn).shift(1).fillna(0)
    qv = qqq.close.pct_change().rolling(20).std() * np.sqrt(252)
    d["q_vol20"] = qv
    d["above200"] = qqq.close > qqq.close.rolling(200).mean()
    idx = d.index
    ym = idx.to_period("M")
    d["tdom"] = pd.Series(1, index=idx).groupby(ym).cumsum().values
    d["opex"] = (idx.dayofweek == 4) & (idx.day >= 15) & (idx.day <= 21)
    nxt = pd.Series(idx, index=idx).shift(-1)
    gap_days = pd.bdate_range(idx[0], idx[-1])
    traded = set(idx)
    pre_hol = []
    for t, n in zip(idx, nxt):
        if pd.isna(n):
            pre_hol.append(False)
            continue
        skipped = [b for b in pd.bdate_range(t + pd.Timedelta(days=1), n - pd.Timedelta(days=1)) if b not in traded]
        pre_hol.append(len(skipped) > 0)
    d["pre_hol"] = pre_hol
    return d.iloc[201:]


def lev_day(row, lev, und):
    base = 1 + lev * row[f"{und}_co"]
    close_v = (1 + lev * row[f"{und}_cc"]) / base
    adverse = row[f"{und}_lo"] if lev > 0 else row[f"{und}_hi"]
    worst_v = (1 + lev * adverse) / base
    return close_v - 1, worst_v - 1


def signal(row):
    up = None
    if row.tdom <= 3 and 0.15 <= row.rv20 <= 0.40:
        up = "month_start"
    if row.streak >= 3 and row.s_co <= 0.003:
        up = "dip"
    if up is None and row.pre_hol and not row.opex:
        up = "pre_holiday"
    down = row.opex and row.q_co >= -0.003
    if up and down:
        return None
    return up or ("opex" if down else None)


def run(d, p: P):
    eq, rows = 1.0, []
    hold_on = False          # currently holding the 2x fund
    hold_entry_val = None    # account value of the held slice at entry (for the hold stop)
    hold_share = 1.0
    stopped_wait = False     # after a hold stop: wait for QQQ to go below then above its 200-day
    want_hold_prev = False   # yesterday's close signal
    week, wk_start, wk_locked = None, 1.0, False
    hold_days = trades = stops = hold_stops = 0
    for t, row in d.iterrows():
        wk = t.to_period("W-FRI")
        if wk != week:
            week, wk_start, wk_locked = wk, eq, False
        if p.sized and t.dayofweek == 4:
            hold_share = min(1.0, 0.20 / row.q_vol20) if row.q_vol20 > 0 else 1.0
        share = hold_share if p.sized else 1.0
        sig = signal(row)
        day_r = 0.0
        if hold_on and sig == "opex" and not wk_locked:
            # overnight on the held fund to the open, then SQQQ for the day, then back at the close
            gap = 2 * row.q_co - p.hold_drag / 252
            eq_open = eq * (1 + share * gap)
            r, worst = lev_day(row, -3, "q")
            stop = max(p.day_stop, (1 + p.weekly_brake) * wk_start / eq_open - 1)
            if worst <= stop:
                r, stops = stop - p.stop_slip, stops + 1
            eq = eq_open * (1 + r - p.rt_cost * 2)  # SQQQ round trip + sell/rebuy held fund
            trades += 1
            if hold_entry_val is not None:
                hold_entry_val = hold_entry_val  # entry reference unchanged
        elif hold_on:
            # ordinary holding day (up signals while holding: stay put)
            hd = 2 * row.q_cc - p.hold_drag / 252
            if p.hold_stop is not None:
                worst = (1 + 2 * row.q_lo) * eq / hold_entry_val - 1 if hold_entry_val else 0
                cur_after = eq * (1 + share * hd)
                if eq * (1 + share * 2 * row.q_lo) <= hold_entry_val * (1 + p.hold_stop):
                    exit_v = hold_entry_val * (1 + p.hold_stop) - eq * share * p.stop_slip
                    eq = min(exit_v, eq) - eq * share * p.rt_cost / 2
                    hold_on, hold_entry_val, stopped_wait, hold_stops = False, None, True, hold_stops + 1
                    rows.append((t, eq))
                    want_hold_prev = False
                    continue
            eq *= 1 + share * hd
            hold_days += 1
        elif sig and not wk_locked:
            lev, und = (3, "s") if sig != "opex" else (-3, "q")
            r, worst = lev_day(row, lev, und)
            stop = max(p.day_stop, (1 + p.weekly_brake) * wk_start / eq - 1)
            if worst <= stop:
                r, stops = stop - p.stop_slip, stops + 1
            eq *= 1 + r - p.rt_cost
            trades += 1
        if eq / wk_start - 1 <= p.weekly_brake:
            wk_locked = True
        # end-of-day: decide tomorrow's hold (acted on at today's close per H: "change made at the next day's close")
        if not row.above200:
            stopped_wait = False
        want = bool(row.above200) and not stopped_wait
        if want_hold_prev and not hold_on and want:
            hold_on, hold_entry_val = True, eq
            eq *= 1 - p.rt_cost / 2
        elif hold_on and not want_hold_prev:
            hold_on, hold_entry_val = False, None
            eq *= 1 - p.rt_cost / 2
        want_hold_prev = want
        rows.append((t, eq))
    s = pd.Series(dict(rows))
    return s, dict(trades=trades, stops=stops, hold_stops=hold_stops, hold_days=hold_days)


def stats(s, start=None, end=None):
    x = s[(s.index >= pd.Timestamp(start)) if start else slice(None)]
    if start:
        x = s[s.index >= pd.Timestamp(start)]
    if end:
        x = x[x.index <= pd.Timestamp(end)]
    yrs = (x.index[-1] - x.index[0]).days / 365.25
    cagr = (x.iloc[-1] / x.iloc[0]) ** (1 / yrs) - 1
    dd = (x / x.cummax() - 1).min()
    yr = x.groupby(x.index.year).last() / x.groupby(x.index.year).first() - 1
    return f"{cagr * 100:6.1f}%/yr  worst drop {dd * 100:6.1f}%  worst year {yr.min() * 100:6.1f}% ({yr.idxmin()})"


if __name__ == "__main__":
    d = build()
    variants = {
        "H7 as Zach froze it": P(),
        "Sam: full size, -10% day, -20% hold": P(sized=False, day_stop=-0.10, hold_stop=-0.20),
        "Sam's stops, sized hold": P(day_stop=-0.10, hold_stop=-0.20),
        "Full size, -10% day, no hold stop": P(sized=False, day_stop=-0.10),
        "Full size, -5% day, no hold stop": P(sized=False),
    }
    for name, p in variants.items():
        s, info = run(d, p)
        print(f"\n{name}  {info}")
        print("   2000-2026:", stats(s))
        print("   2010-2026:", stats(s, "2010-01-01"))
        print("   2016-2024:", stats(s, "2016-01-01", "2024-10-31"))
