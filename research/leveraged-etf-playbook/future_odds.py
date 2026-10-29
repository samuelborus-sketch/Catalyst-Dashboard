"""How likely is the edge to hold? Placebo (random-day) test, edge-decay scenarios, 5-year forward odds, cash-account settlement."""
from dataclasses import replace

import numpy as np
import pandas as pd

from backtest import Params, benchmark, decide, load_frames, metrics, simulate

P = Params()
SPY, QQQ = load_frames()
DEC = decide(SPY, QQQ, P)
TR, EQ = simulate(SPY, QQQ, DEC, P)
RNG = np.random.default_rng(11)
SPY_DIV = 0.018  # rough average SPY dividend yield 2000-2026, added to the benchmark


def traded(tr):
    return tr[tr["exit"] != "WEEK_LOCKED"]


def avg_trade(tr, start=None):
    t = traded(tr)
    if start:
        t = t[t["date"] >= start]
    return t["ret"].mean()


def placebo_decisions(dec):
    """Same number of long and short days in each calendar year, placed on random days."""
    out = dec.copy()
    for _, idx in dec.groupby(dec.index.year).groups.items():
        perm = RNG.permutation(len(idx))
        out.loc[idx, ["side", "family", "signal"]] = dec.loc[idx, ["side", "family", "signal"]].values[perm]
    return out


def placebo_runs(n=200):
    cagr, avg_all, avg_recent, curves = [], [], [], []
    for _ in range(n):
        tr, eq = simulate(SPY, QQQ, placebo_decisions(DEC), P)
        cagr.append(metrics(eq, tr)["cagr"])
        avg_all.append(avg_trade(tr))
        avg_recent.append(avg_trade(tr, "2013-01-01"))
        curves.append(eq)
    return np.array(cagr), np.mean(avg_all), np.mean(avg_recent), curves


def no_back_to_back(dec):
    """Cash-account worst case: proceeds not usable at the next open, so skip a trade the day after a trade."""
    out = dec.copy()
    prev = False
    for d in out.index:
        if out.at[d, "side"] != 0:
            if prev:
                out.at[d, "side"] = 0
                out.at[d, "signal"] = "SKIPPED_SETTLEMENT"
                prev = False
            else:
                prev = True
        else:
            prev = False
    return out


def forward_odds(strat_eq, years=5, n=5000, bench=None):
    """Joint monthly block bootstrap of strategy and SPY (with dividends) over a forward horizon."""
    bench = bench if bench is not None else benchmark("SPY")
    df = pd.DataFrame({"s": strat_eq.pct_change(), "b": bench.pct_change() + SPY_DIV / 252}).dropna()
    months = [g.values for _, g in df.groupby(df.index.to_period("M"))]
    k = years * 12
    beat, loss, dd40, cagr = 0, 0, 0, []
    for _ in range(n):
        block = np.concatenate([months[i] for i in RNG.integers(0, len(months), k)])
        s = np.cumprod(1 + block[:, 0])
        b = np.prod(1 + block[:, 1])
        beat += s[-1] > b
        loss += s[-1] < 1
        dd40 += (s / np.maximum.accumulate(s) - 1).min() <= -0.40
        cagr.append(s[-1] ** (1 / years) - 1)
    return dict(beat_spy=beat / n * 100, lose_money=loss / n * 100, dd_40=dd40 / n * 100, median_cagr=np.median(cagr) * 100)


def main():
    t = traded(TR)
    prev_day = pd.Series(DEC.index, index=DEC.index).shift(1)
    trade_days = set(t["date"])
    b2b = sum(1 for d in t["date"] if prev_day[d] in trade_days)
    print(f"[settlement] {b2b} of {len(t)} trades ({b2b / len(t) * 100:.0f}%) come the session after another trade")
    tr2, eq2 = simulate(SPY, QQQ, no_back_to_back(DEC), P)
    m2 = metrics(eq2, tr2)
    print(f"[settlement] if those had to be skipped: CAGR {m2['cagr']}% (vs {metrics(EQ, TR)['cagr']}%), max DD {m2['max_dd']}%, trades/yr {m2['per_year']}")

    print("\n[recent] per-play average trade and total, by period")
    for lab, s, e in (("2000-12", "2000-01-01", "2012-12-31"), ("2013-19", "2013-01-01", "2019-12-31"),
                      ("2020-21", "2020-01-01", "2021-12-31"), ("2022-26", "2022-01-01", "2026-12-31")):
        g = t[(t["date"] >= s) & (t["date"] <= e)]
        parts = []
        for sig in ("OPEX_FADE", "DIP_BOUNCE", "MONTH_START"):
            x = g[g["signal"] == sig]["ret"]
            parts.append(f"{sig} n={len(x):3d} avg={x.mean() * 100:+.2f}% win={(x > 0).mean() * 100:3.0f}% total={np.expm1(np.log1p(x).sum()) * 100:+5.0f}%")
        print(f"   {lab}: " + " | ".join(parts))

    pc, pavg, pavg_recent, curves = placebo_runs()
    real_cagr = metrics(EQ, TR)["cagr"]
    print(f"\n[placebo] 200 runs, same trade counts on random days: median CAGR {np.median(pc):.1f}%, "
          f"best {pc.max():.1f}%, 95th pct {np.percentile(pc, 95):.1f}%; runs >= real {real_cagr}%: {(pc >= real_cagr).sum()}")
    real_avg, real_avg_recent = avg_trade(TR), avg_trade(TR, "2013-01-01")
    print(f"[edge] avg trade real {real_avg * 100:+.3f}% vs random {pavg * 100:+.3f}% -> edge {(real_avg - pavg) * 100:.3f}% per trade; "
          f"2013-26: real {real_avg_recent * 100:+.3f}% vs random {pavg_recent * 100:+.3f}% -> edge {(real_avg_recent - pavg_recent) * 100:.3f}%")

    edge_full, edge_recent = real_avg - pavg, real_avg_recent - pavg_recent
    scen = {
        "A. edge as strong as 2000-2026": EQ,
        "B. edge as strong as 2013-2026": simulate(SPY, QQQ, DEC, replace(P, cost=P.cost + (edge_full - edge_recent)))[1],
        "C. half the 2013-2026 edge": simulate(SPY, QQQ, DEC, replace(P, cost=P.cost + edge_full - edge_recent / 2))[1],
    }
    print("\n[forward] next 5 years, joint monthly bootstrap of 2000-2026 markets (SPY incl. ~1.8%/yr dividends)")
    for name, eq in scen.items():
        r = forward_odds(eq)
        print(f"   {name:34s} full-period CAGR {metrics(eq)['cagr']:5.1f}% | 5y: beat SPY {r['beat_spy']:4.0f}%  lose money {r['lose_money']:4.0f}%  "
              f"drop <= -40% {r['dd_40']:4.0f}%  median {r['median_cagr']:5.1f}%/yr")
    pooled = []
    for _ in range(5):
        pooled.append(forward_odds(curves[RNG.integers(0, len(curves))], n=1000))
    r = {k: np.mean([p[k] for p in pooled]) for k in pooled[0]}
    print(f"   {'D. no edge (random days)':34s} full-period CAGR {np.median(pc):5.1f}% | 5y: beat SPY {r['beat_spy']:4.0f}%  lose money {r['lose_money']:4.0f}%  "
          f"drop <= -40% {r['dd_40']:4.0f}%  median {r['median_cagr']:5.1f}%/yr")
    spy_eq = benchmark("SPY")
    hist = []
    for y in range(2000, 2022):
        s, e = pd.Timestamp(f"{y}-01-01"), pd.Timestamp(f"{y + 5}-01-01")
        q, b = EQ[(EQ.index >= s) & (EQ.index < e)], spy_eq[(spy_eq.index >= s) & (spy_eq.index < e)]
        hist.append((q.iloc[-1] / q.iloc[0]) > (b.iloc[-1] / b.iloc[0]) * (1 + SPY_DIV) ** 5)
    print(f"[history] beat SPY incl. dividends in {sum(hist)} of {len(hist)} rolling 5-year windows")


if __name__ == "__main__":
    main()
