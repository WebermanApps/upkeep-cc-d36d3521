#!/usr/bin/env python3
"""Refresh the Financial Forecast data on the dashboard from forecast v3 (monthly model, Oct 17 2026).
Usage (from this repo):
  git -C /path/to/smartupkeep-ops pull && node /path/to/smartupkeep-ops/forecast/run.js
  /workspace/security/pagelock/unlock .
  python3 forecast_section.py /path/to/smartupkeep-ops/forecast/forecast-output.json
  /workspace/security/pagelock/relock .   # then commit and push
The data is written inline into index.html (between FC-DATA markers) so it stays inside the
password-locked page; a separate .js file would be public on GitHub Pages. ALL FIGURES ARE PROJECTIONS."""
import json, sys, re, datetime
src = sys.argv[1] if len(sys.argv) > 1 else "/workspace/smartkeep/ops-private/forecast/forecast-output.json"
O = json.load(open(src))
data = {"generated": datetime.datetime.now().strftime("%b %d %Y %H:%M ICT"), "version": 3, "scenarios": {}}
for n, r in O.items():
    R, Mo = r["rows"], r["months"]
    yr = lambda y: [x for x in Mo if x["ym"][:4] == str(y) or (y == 2027 and x["month"] == 0)]
    data["scenarios"][n] = {
        "label": r.get("label", n),
        "mAt": {str(k): round(Mo[k]["members"]) for k in (1, 3, 6, 12, 24, 36)},
        "launch": round(Mo[0]["members"]),
        "rev": {str(y): round(sum(x["membershipRevenue"] + x["addonRevenue"] for x in yr(y))) for y in (2027, 2028, 2029)},
        "profit": {str(y): round(sum(x["profit"] for x in yr(y))) for y in (2027, 2028, 2029)},
        "ad2027": round(sum(x["adSpend"] for x in yr(2027))), "cac": r["inputs"]["cac"],
        "p36": round(Mo[-1]["cumulativeProfit"]), "beMembers": r["perMember"]["breakEvenMembers"],
        "beLabel": r.get("breakEvenLabel"), "cumBeLabel": r.get("cumulativeBreakEvenLabel"),
        "lowCash": round(min(x["cashBalanceAfterStartup"] for x in Mo)),
        "lowCashLabel": min(Mo, key=lambda x: x["cashBalanceAfterStartup"])["label"],
        "ltvCac": round(r["perMember"]["ltvToCac"], 1), "contrib": round(r["perMember"]["contribution"], 2),
        "rows": [{"q": x["quarter"], "ql": x["label"].replace(" 20", " '"), "mem": round(x["members"]), "new": round(x["newMembers"]), "vans": x["vansAndWorkers"],
                  "rev": round(x["membershipRevenue"] + x["addonRevenue"]), "mkt": round(x["marketing"]), "profit": round(x["profit"]),
                  "cum": round(x["cumulativeProfit"]), "cash": round(x["cashBalanceAfterStartup"]), "def": round(x["deferredRevenue"])} for x in R]}
p = "index.html"; s = open(p).read()
new = "/*FC-DATA-START*/window.FC_DATA=" + json.dumps(data, separators=(",", ":")) + ";/*FC-DATA-END*/"
s2, k = re.subn(r"/\*FC-DATA-START\*/.*?/\*FC-DATA-END\*/", lambda m: new, s, flags=re.S)
assert k == 1, "FC-DATA markers not found (is index.html unlocked?)"
open(p, "w").write(s2); print("forecast data refreshed:", data["generated"])
