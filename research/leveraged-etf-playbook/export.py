"""Export everything the strategy sheet needs into results/ (JSON + trade log CSV)."""
import json
import os

import numpy as np
import pandas as pd

from backtest import Params, benchmark, decide, load_frames, metrics, simulate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def main():
    os.makedirs(OUT, exist_ok=True)
    p = Params()
    spy, qqq = load_frames()
    dec = decide(spy, qqq, p)
    tr, eq = simulate(spy, qqq, dec, p)
    # both series start from the same instant: the close before the first tradable session
    eq = pd.concat([pd.Series({spy.index[0]: 1.0}), eq])
    spy_bh = benchmark("SPY")
    qqq_bh = benchmark("QQQ")

    full = metrics(eq, tr, "strategy")
    is_ = metrics(*simulate(spy, qqq, dec, p, None, "2012-12-31")[::-1], "is")
    oos = metrics(*simulate(spy, qqq, dec, p, "2013-01-01", None)[::-1], "oos")
    traded = tr[tr["exit"] != "WEEK_LOCKED"]
    days_in_market = len(traded) / len(eq)

    # pattern-day-trader exposure: trades in any rolling 5-session window
    is_trade = pd.Series(0, index=eq.index)
    is_trade[traded["date"]] = 1
    roll5 = is_trade.rolling(5).sum()
    pdt = dict(max_in_5_sessions=int(roll5.max()), windows_over_3=int((roll5 > 3).sum()),
               pct_weeks_over_3=round(float((roll5 > 3).groupby(roll5.index.to_period("W")).max().mean() * 100), 1))

    yr_end = eq.groupby(eq.index.year).last()
    prev = yr_end.shift(1)
    prev.iloc[0] = 1.0
    b_end = spy_bh.groupby(spy_bh.index.year).last()
    bprev = b_end.shift(1)
    bprev.iloc[0] = 1.0
    q_end = qqq_bh.groupby(qqq_bh.index.year).last()
    qprev = q_end.shift(1)
    qprev.iloc[0] = 1.0
    years = [dict(year=int(y), strategy=round((yr_end[y] / prev[y] - 1) * 100, 1),
                  spy=round((b_end[y] / bprev[y] - 1) * 100, 1), qqq=round((q_end[y] / qprev[y] - 1) * 100, 1),
                  trades=int((traded["date"].dt.year == y).sum()))
             for y in yr_end.index]

    daily = pd.DataFrame({"strategy": eq, "spy": spy_bh.reindex(eq.index).ffill(), "qqq": qqq_bh.reindex(eq.index).ffill()})
    daily = daily / daily.iloc[0] * 10000
    month_end = daily.groupby(daily.index.to_period("M")).tail(1)
    points = pd.concat([daily.iloc[[0]], month_end])
    points = points[~points.index.duplicated()]
    dd = (eq / eq.cummax() - 1).groupby(eq.index.to_period("M")).min()
    sdd = (spy_bh / spy_bh.cummax() - 1).groupby(spy_bh.index.to_period("M")).min()
    curve = [dict(d=str(k.date()), s=round(r.strategy), b=round(r.spy), q=round(r.qqq),
                  sdd=round(float(dd.get(k.to_period("M"), 0)) * 100, 1), bdd=round(float(sdd.get(k.to_period("M"), 0)) * 100, 1))
             for k, r in points.iterrows()]

    total_log = np.log1p(traded["ret"]).sum()
    signals = []
    for sig, g in traded.groupby("signal"):
        lg = np.log1p(g["ret"]).sum()
        wins, losses = g.loc[g.ret > 0, "ret"].sum(), -g.loc[g.ret <= 0, "ret"].sum()
        signals.append(dict(signal=sig, trades=len(g), win=round((g.ret > 0).mean() * 100, 1),
                            avg=round(g.ret.mean() * 100, 2), pf=round(wins / losses, 2),
                            share=round(lg / total_log * 100, 1), stops=int(g.exit.str.startswith("STOP").sum()),
                            best=round(g.ret.max() * 100, 1), worst=round(g.ret.min() * 100, 1)))

    res = dict(params=p.__dict__, full=full, is_=is_, oos=oos,
               spy=metrics(spy_bh, label="spy"), qqq=metrics(qqq_bh, label="qqq"),
               spy_is=metrics(benchmark("SPY", None, "2012-12-31"), label="spy_is"),
               spy_oos=metrics(benchmark("SPY", "2013-01-01"), label="spy_oos"),
               days_in_market_pct=round(days_in_market * 100, 1), pdt=pdt,
               losing_years=[y["year"] for y in years if y["strategy"] < 0],
               beat_spy_years=sum(1 for y in years if y["strategy"] > y["spy"]), n_years=len(years),
               years=years, curve=curve, signals=signals,
               exits=traded["exit"].value_counts().to_dict(), week_locks=int((tr["exit"] == "WEEK_LOCKED").sum()))
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(res, fh, default=lambda o: o.item() if hasattr(o, "item") else str(o), indent=1)
    out = tr.copy()
    out["etf"] = [{("SPY", 1): "SPXL", ("SPY", -1): "SPXS", ("QQQ", 1): "TQQQ", ("QQQ", -1): "SQQQ"}[(f, s)]
                  for f, s in zip(out["family"], out["side"])]
    out["date"] = out["date"].dt.date
    out[["date", "signal", "etf", "side", "gap", "und_oc", "ret", "exit", "eq_after"]].round(5).to_csv(
        os.path.join(OUT, "trades.csv"), index=False)
    print(json.dumps({k: res[k] for k in ("full", "is_", "oos", "spy", "qqq", "spy_oos", "days_in_market_pct", "pdt",
                                          "losing_years", "beat_spy_years", "n_years", "exits", "week_locks")},
                     default=str, indent=1))
    for s in signals:
        print(s)


if __name__ == "__main__":
    main()
