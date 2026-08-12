#!/usr/bin/env python3
# Tägliche Umsätze TUIC DACH 9127, exkl. Payback (426667,469409), via Transactions-API.
# Output: .tuic_9127_daily_data.json  (enthält ABSOLUTE Tageswerte — bleibt lokal, NICHT auf GitHub)
import json, os, sys, urllib.request, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CRED = os.path.join(BASE, ".awin-credentials")
OUT  = os.path.join(BASE, ".tuic_9127_daily_data.json")
EXCLUDE = {426667, 469409}
ADV = 9127

token = None
with open(CRED) as f:
    for line in f:
        line = line.strip()
        if line.startswith("AWIN_API_TOKEN"):
            token = line.split("=", 1)[1].strip().strip('"').strip("'")
if not token:
    print("NO_TOKEN"); sys.exit(1)

today = datetime.date.today()

def last_day(y, m):
    nxt = datetime.date(y+1,1,1) if m==12 else datetime.date(y, m+1, 1)
    return nxt - datetime.timedelta(days=1)

daily = {}   # 'YYYY-MM-DD' -> sale sum excl payback
def fetch_chunk(y, m):
    start = datetime.date(y, m, 1)
    end = last_day(y, m)
    if end > today: end = today
    if start > today: return
    url = (f"https://api.awin.com/advertisers/{ADV}/transactions/"
           f"?startDate={start:%Y-%m-%d}T00:00:00&endDate={end:%Y-%m-%d}T23:59:59"
           f"&dateType=transaction&timezone=Europe/Berlin")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        rows = json.load(r)
    for t in rows:
        pid = int(t.get("publisherId", 0) or 0)
        if pid in EXCLUDE: continue
        if (t.get("commissionStatus") or "").lower() == "declined": continue
        td = t.get("transactionDate","")[:10]
        if not td: continue
        amt = (t.get("saleAmount") or {}).get("amount", 0) or 0
        daily[td] = daily.get(td, 0.0) + float(amt)

for y in (2025, 2026):
    for m in range(1, 13):
        if datetime.date(y, m, 1) > today: continue
        fetch_chunk(y, m)

daily = {k: round(v, 2) for k, v in sorted(daily.items())}
out = {"advertiser": ADV, "excluded": sorted(EXCLUDE),
       "generatedAt": datetime.datetime.now().isoformat(timespec="seconds"),
       "today": today.isoformat(), "daily": daily}
with open(OUT, "w") as f:
    json.dump(out, f, indent=0, ensure_ascii=False)
# Monatssummen zur Kontrolle
mon = {}
for k, v in daily.items():
    mon[k[:7]] = mon.get(k[:7], 0.0) + v
print("DAYS", len(daily))
print("MONTHS", json.dumps({k: round(v) for k, v in sorted(mon.items())}))
