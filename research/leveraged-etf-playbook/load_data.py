"""Convert saved Robinhood historicals responses (equity + index, daily bars) into per-symbol CSVs in data/.

Usage: python load_data.py <dir containing the saved JSON responses>
"""
import glob
import json
import os
import sys

import pandas as pd

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def rows_from(bar, is_index):
    if bar.get("interpolated"):
        return None
    p = "_value" if is_index else "_price"
    row = {"date": bar["begins_at"][:10]}
    for k in ("open", "high", "low", "close"):
        row[k] = float(bar[k + p])
    if not is_index:
        row["volume"] = int(bar.get("volume") or 0)
    return row


def load_dir(src):
    frames = {}
    for fn in sorted(glob.glob(os.path.join(src, "*"))):
        try:
            d = json.load(open(fn))
        except (json.JSONDecodeError, UnicodeDecodeError, IsADirectoryError):
            continue
        for r in d.get("data", {}).get("results", []):
            if r.get("interval") != "day" or "bars" not in r:
                continue
            is_index = "instrument_id" in r
            rows = [x for x in (rows_from(b, is_index) for b in r["bars"]) if x]
            if rows:
                frames.setdefault(r["symbol"], []).append(pd.DataFrame(rows))
    return {s: pd.concat(fs).drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
            for s, fs in frames.items()}


def main(src):
    os.makedirs(OUT, exist_ok=True)
    data = load_dir(src)
    spy_dates = set(data["SPY"]["date"])
    for sym, df in sorted(data.items()):
        df.to_csv(os.path.join(OUT, f"{sym}.csv"), index=False)
        first, last = df["date"].iloc[0], df["date"].iloc[-1]
        missing = sorted({d for d in spy_dates if first <= d <= last} - set(df["date"]))
        bad_hl = ((df["high"] < df[["open", "close"]].max(axis=1) - 1e-9) | (df["low"] > df[["open", "close"]].min(axis=1) + 1e-9)).sum()
        print(f"{sym:5s} rows={len(df):5d} {first}..{last} missing_vs_SPY={len(missing)} hl_inconsistent={bad_hl}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
