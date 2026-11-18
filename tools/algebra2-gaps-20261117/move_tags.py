"""Move A-REI.D.11 off the linear-system items (they solve systems algebraically: A-REI.C.6).

A-REI.D.11 now belongs to "Solving f(x) = g(x) with graphs and tables" only. Idempotent.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "algebra2-audit-20261117"))
from lib import load, save, items

NEW = "linear-functions-systems-skill-08"
banks = load()
moved = 0
for _, q in items(banks):
    s = q.get("standards", [])
    if "A-REI.D.11" in s and q["skillId"] != NEW:
        s = [x for x in s if x != "A-REI.D.11"]
        if "A-REI.C.6" not in s:
            s.append("A-REI.C.6")
        q["standards"] = s
        moved += 1
save(banks)
print("moved", moved)
