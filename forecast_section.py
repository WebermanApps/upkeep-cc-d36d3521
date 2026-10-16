#!/usr/bin/env python3
"""Refresh the Financial Forecast data on the dashboard from forecast v2.
Usage (from this repo):
  git -C /path/to/smartupkeep-ops pull && node /path/to/smartupkeep-ops/forecast/run.js
  /workspace/security/pagelock/unlock .
  python3 forecast_section.py /path/to/smartupkeep-ops/forecast/forecast-output.json
  /workspace/security/pagelock/relock .   # then commit and push
The data is written inline into index.html (between FC-DATA markers) so it stays inside the
password-locked page; a separate .js file would be public on GitHub Pages."""
import json, sys, re, datetime
src = sys.argv[1] if len(sys.argv) > 1 else "/workspace/smartkeep/ops-private/forecast/forecast-output.json"
O = json.load(open(src))
data = {"generated": datetime.datetime.now().strftime("%b %d %Y %H:%M ICT"), "scenarios": {}}
for n, r in O.items():
    R = r["rows"]
    data["scenarios"][n] = {
        "m12": round(R[3]["members"]), "m36": round(R[11]["members"]),
        "y1": round(sum(x["profit"] for x in R[:4])), "p36": round(R[11]["cumulativeProfit"]),
        "beMembers": r["perMember"]["breakEvenMembers"], "beQ": r["breakEvenQuarter"], "cumBeQ": r["cumulativeBreakEvenQuarter"],
        "lowCash": round(min(x["cashBalanceAfterStartup"] for x in R)),
        "lowCashQ": min(range(len(R)), key=lambda i: R[i]["cashBalanceAfterStartup"]) + 1,
        "rows": [{"q": x["quarter"], "mem": round(x["members"]), "new": round(x["newMembers"]), "vans": x["vansAndWorkers"],
                  "rev": round(x["membershipRevenue"] + x["addonGrossProfit"]), "profit": round(x["profit"]),
                  "cum": round(x["cumulativeProfit"]), "cash": round(x["cashBalanceAfterStartup"]), "def": round(x["deferredRevenue"])} for x in R]}
p = "index.html"; s = open(p).read()
new = "/*FC-DATA-START*/window.FC_DATA=" + json.dumps(data, separators=(",", ":")) + ";/*FC-DATA-END*/"
s2, k = re.subn(r"/\*FC-DATA-START\*/.*?/\*FC-DATA-END\*/", lambda m: new, s, flags=re.S)
assert k == 1, "FC-DATA markers not found (is index.html unlocked?)"
open(p, "w").write(s2); print("forecast data refreshed:", data["generated"])
