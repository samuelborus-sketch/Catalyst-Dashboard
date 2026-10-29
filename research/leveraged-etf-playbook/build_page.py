"""Assemble page data from the backtest + robustness suite and inject it into the HTML template."""
import json
import os
import sys

import numpy as np

import robustness as rb
from export import main as export_main

HERE = os.path.dirname(os.path.abspath(__file__))


def why_stats():
    spy, qqq = rb.SPY, rb.QQQ
    op = qqq[spy["opex"] == 1]
    tom = spy[(spy["tdom"] <= rb.P.tom_days) & spy["rv20"].between(rb.P.tom_min_rv20, rb.P.tom_max_rv20)]
    dip = spy[(spy["dn_streak"] >= rb.P.dip_streak) & (spy["r_co"] <= rb.P.dip_max_gap)]
    allspy = spy.iloc[1:]
    return dict(opex_down=(op["r_oc"] < 0).mean() * 100, opex_mean_bp=op["r_oc"].mean() * 1e4,
                tom_up=(tom["r_oc"] > 0).mean() * 100, tom_mean_bp=tom["r_oc"].mean() * 1e4,
                dip_up=(dip["r_oc"] > 0).mean() * 100, dip_mean_bp=dip["r_oc"].mean() * 1e4,
                all_mean_bp=allspy["r_oc"].mean() * 1e4)


def main(out_path):
    export_main()
    with open(os.path.join(HERE, "results", "summary.json")) as fh:
        s = json.load(fh)
    t = rb.TR[rb.TR["exit"] != "WEEK_LOCKED"]
    real = rb.real_etf_check()
    iwm, iwm_bh = rb.playbook_on("IWM", "IWM")
    dia, dia_bh = rb.playbook_on("DIA", "DIA")
    stress = rb.stress()
    bs = rb.bootstrap()
    roll = rb.rolling()
    lag = [r for r in roll if r["strat"] < r["spy"]]
    mk_iwm, mk_dia = rb.market_test("IWM"), rb.market_test("DIA")
    markets = [dict(label=k, vals=[mk_iwm[k][0]["avg_pct"], mk_iwm[k][1]["avg_pct"], mk_dia[k][0]["avg_pct"], mk_dia[k][1]["avg_pct"]])
               for k in mk_iwm]
    no_rules = next(r for r in stress if r["label"].startswith("Without either"))
    page = dict(
        full=s["full"], spy=s["spy"], is_=s["is_"], oos=s["oos"], spy_oos=s["spy_oos"],
        curve=s["curve"], years=s["years"], signals=s["signals"],
        days_in_market_pct=s["days_in_market_pct"], beat_spy_years=s["beat_spy_years"], n_years=s["n_years"],
        losing_years=s["losing_years"],
        avg_win=float(t[t.ret > 0].ret.mean() * 100), avg_loss=float(t[t.ret <= 0].ret.mean() * 100),
        why=why_stats(),
        robust=dict(
            real_cagr=real["real_cagr"], model_cagr=real["model_cagr"], real_trades=real["trades"],
            iwm_cagr=iwm["cagr"], iwm_bh=iwm_bh["cagr"], dia_cagr=dia["cagr"], dia_bh=dia_bh["cagr"],
            bs_p5=bs["p5"], bs_p95=bs["p95"], bs_below_spy=bs["below_hurdle"],
            roll_lag=len(lag), roll_n=len(roll), roll_first_end=min(r["end"] for r in lag), roll_last_end=max(r["end"] for r in lag),
            cost_of_rules=no_rules["cagr"] - stress[0]["cagr"], no_rules_cagr=no_rules["cagr"], no_rules_dd=no_rules["dd"],
            stress=[r for r in stress if not r["label"].startswith("Without either")],
            markets=markets,
        ),
    )
    with open(os.path.join(HERE, "results", "page_data.json"), "w") as fh:
        json.dump(page, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    blob = json.dumps(page, separators=(",", ":"), default=lambda o: o.item() if hasattr(o, "item") else str(o))
    blob = blob.replace("</", "<\\/")
    with open(os.path.join(HERE, "page_template.html")) as fh:
        html = fh.read()
    assert "/*__DATA__*/" in html
    html = html.replace("/*__DATA__*/", blob)
    with open(out_path, "w") as fh:
        fh.write(html)
    print("wrote", out_path, len(html), "bytes")
    print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in page["robust"].items() if k not in ("stress", "markets")}))
    for r in page["robust"]["stress"]:
        print("  stress", r["label"], round(r["cagr"], 2), r["dd"], round(r["end"]))
    for r in markets:
        print("  market", r["label"], [round(v, 2) for v in r["vals"]])
    print("  why", {k: round(v, 1) for k, v in page["why"].items()})
    print("  lag windows", [(r["start"], r["end"], round(r["strat"], 1), round(r["spy"], 1)) for r in lag])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "playbook.html"))
