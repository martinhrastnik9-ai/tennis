import json, os, urllib.request, datetime

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

os.makedirs("data", exist_ok=True)


def prenesi(url, ime):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as r:
            vsebina = r.read()
        with open("data/" + ime, "wb") as f:
            f.write(vsebina)
        print("OK   " + ime + "  " + str(len(vsebina) // 1024) + " KB")
    except Exception as e:
        print("FAIL " + ime + ": " + str(e))


k = os.environ.get("K")
if k:
    try:
        sports = json.load(urllib.request.urlopen(
            "https://api.the-odds-api.com/v4/sports/?apiKey=" + k, timeout=60))
        keys = [s["key"] for s in sports
                if s["key"].startswith("tennis") and s.get("active")]
        out = {}
        for key in keys:
            url = ("https://api.the-odds-api.com/v4/sports/" + key + "/odds/"
                   "?apiKey=" + k + "&regions=eu&markets=h2h&oddsFormat=decimal")
            try:
                out[key] = json.load(urllib.request.urlopen(url, timeout=60))
            except Exception as e:
                out[key] = {"napaka": str(e)}
        json.dump(out, open("data/kvote.json", "w"), ensure_ascii=False, indent=1)
        print("OK   kvote.json  " + str(len(keys)) + " turnirjev")
    except Exception as e:
        print("FAIL kvote: " + str(e))

prenesi("https://tennisabstract.com/reports/atp_elo_ratings.html", "elo_atp.html")
prenesi("https://tennisabstract.com/reports/wta_elo_ratings.html", "elo_wta.html")
prenesi("https://www.tennisratio.com/", "ratio.html")

MCP = "https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master"
prenesi(MCP + "/charting-m-matches.csv", "mcp_m_matches.csv")
prenesi(MCP + "/charting-w-matches.csv", "mcp_w_matches.csv")

with open("data/zajeto.txt", "w") as f:
    f.write(datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")
print("koncano")
