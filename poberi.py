import json, os, urllib.request

k = os.environ["K"]
os.makedirs("data", exist_ok=True)

sports = json.load(urllib.request.urlopen(
    "https://api.the-odds-api.com/v4/sports/?apiKey=" + k, timeout=60))
keys = [s["key"] for s in sports
        if s["key"].startswith("tennis") and s.get("active")]

out = {}
for key in keys:
    url = ("https://api.the-odds-api.com/v4/sports/" + key +
           "/odds/?apiKey=" + k +
           "&regions=eu&markets=h2h&oddsFormat=decimal")
    try:
        out[key] = json.load(urllib.request.urlopen(url, timeout=60))
    except Exception as e:
        out[key] = {"napaka": str(e)}

json.dump(out, open("data/kvote.json", "w"), ensure_ascii=False, indent=1)
print("turnirjev:", len(keys))
