#!/usr/bin/env python3
import json, os

BASE = "/Users/nicoleemrich/Documents/Claude/Projects/WPP Media"
src = os.path.join(BASE, ".tuic_9127_daily_data.json")
dst = os.path.join(BASE, "tuic_9127_abs_data.json")

with open(src) as f:
    raw = json.load(f)

today = raw["today"]
daily = raw["daily"]  # {"YYYY-MM-DD": value}

d2025, d2026 = {}, {}
for date, val in daily.items():
    y, m, d = date.split("-")
    key = f"{m}-{d}"
    if y == "2025":
        d2025[key] = val
    elif y == "2026":
        d2026[key] = val

out = {
    "meta": {
        "label": "Mein Schiff DACH 9127",
        "today": today,
        "generatedAt": raw.get("generatedAt", today),
        "note": "Absolute €-Tageswerte, exkl. Payback (426667+469409), netto (Stornos raus)"
    },
    "targets": {"2025": 24500000, "2026": 30700000},
    "corr": {
        "amount": 1128000,
        "from": "2026-04-20",
        "full_by": "2026-05-31",
        "note": "Cashback/Voucher-Cluster (Standardlink-Defekt ab 20.04.2026)"
    },
    "d2025": d2025,
    "d2026": d2026
}

with open(dst, "w") as f:
    json.dump(out, f, ensure_ascii=False, separators=(", ", ": "))

# compact single-line JSON for the DATA block
print(json.dumps(out, ensure_ascii=False, separators=(", ", ": ")))
