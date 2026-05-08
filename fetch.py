import json, os, urllib.request, datetime

UA = "Dinesh Kumar dinesh@levylens.co (Rockefeller Harness)"
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

def fetch(url, ua=UA):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return {"status": "OK", "code": r.status, "body": r.read().decode("utf-8", errors="replace")}
    except Exception as e:
        return {"status": "FAIL", "error": str(e)}

result = {
    "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
    "target_date": yesterday,
    "edgar": fetch(f"https://efts.sec.gov/LATEST/search-index?q=&forms=4&dateRange=custom&startdt={yesterday}&enddt={yesterday}"),
    "openinsider": fetch("http://openinsider.com/screener?xp=1&fd=30&sortcol=0&cnt=100",
                         ua="Mozilla/5.0 (compatible; RockefellerHarness/1.0)")
}
os.makedirs("data", exist_ok=True)
with open(f"data/feed-{yesterday}.json", "w") as f:
    json.dump(result, f, indent=2)
with open("data/latest.json", "w") as f:
    json.dump(result, f, indent=2)
print(f"EDGAR: {result['edgar']['status']} | OpenInsider: {result['openinsider']['status']}")
