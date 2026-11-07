#!/usr/bin/env python3
"""Coverage by unit/skill/level/format plus activity-pool counts.

Usage: python3 scripts/verification/coverage_report.py <output_root> <statistics-course.json> [--print]
Writes <output_root>/reports/coverage-expanded.csv and reports/activity-pools.csv.
Activity rules (from the reference pack README and course-source.js / algebra2-bank-native.js):
  * Detective: >= 10 multiple-choice items at one level (per skill when a single skill is chosen).
  * Millionaire: a 15-question session of multiple-choice items at one level.
  * Course-source games select multiple-choice + short-answer by skill and level.
  * Escape Room candidate: short-answer whose answer is a single positive integer 1–25 and
    whose solutionSteps has >= 4 entries.
  * Authored Error Analysis: sourceNotes contains "(family: …_error)".
These are pool counts only; no game was executed.
"""
import csv
import difflib
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT, COURSE = sys.argv[1], sys.argv[2]
course = json.load(open(COURSE, encoding="utf-8"))
os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
FORMATS = ["multiple-choice", "short-answer", "select-all", "open-response"]
cnt = Counter()
cellq = defaultdict(list)
pool = defaultdict(Counter)
esc = Counter()
err = Counter()
for unit in course["units"]:
    bank = json.load(open(os.path.join(ROOT, "question-banks", "statistics", unit["id"] + ".json"), encoding="utf-8"))
    for q in bank["questions"]:
        key = (unit["id"], q["skillId"], q["level"])
        cnt[key + (q["format"],)] += 1
        cellq[key].append(re.sub(r"[\d.,]+", "#", q["prompt"].lower()))
        if q["format"] == "short-answer" and re.fullmatch(r"\s*([1-9]|1\d|2[0-5])\s*", str(q["answer"])) and len(q["solutionSteps"]) >= 4:
            esc[(unit["id"], q["level"])] += 1
        if re.search(r"\(family: [^)]*_error\)", q.get("sourceNotes", "")):
            err[(unit["id"], q["level"])] += 1
        if q["format"] == "multiple-choice":
            pool[(unit["id"], q["level"])]["mc"] += 1

def distinct(prompts):
    """Collapse prompts that are >85% similar after replacing numbers (number swaps)."""
    parent = list(range(len(prompts)))
    def find(i):
        while parent[i] != i:
            i = parent[i]
        return i
    for i in range(len(prompts)):
        for j in range(i + 1, len(prompts)):
            if difflib.SequenceMatcher(None, prompts[i], prompts[j]).ratio() > 0.85:
                parent[find(j)] = find(i)
    return len({find(i) for i in range(len(prompts))})


rows = []
for unit in course["units"]:
    for s in unit["skills"]:
        for lv in ["cp2", "cp1", "honors"]:
            f = [cnt[(unit["id"], s["id"], lv, x)] for x in FORMATS]
            tot = sum(f)
            rows.append([unit["id"], s["id"], s["name"], lv, tot] + f + [distinct(cellq[(unit["id"], s["id"], lv)]), max(0, 8 - tot), max(0, 10 - tot), "yes" if f[0] >= 10 else "no", "yes" if f[0] >= 15 else "no"])
with open(os.path.join(ROOT, "reports", "coverage-expanded.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["unitId", "skillId", "skill", "level", "total"] + FORMATS + ["distinct_after_collapsing_number_swaps", "gap_to_8", "gap_to_10", "skill_detective_ready_10mc", "skill_millionaire_ready_15mc"])
    w.writerows(rows)
with open(os.path.join(ROOT, "reports", "activity-pools.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["unitId", "level", "unit_mc_pool", "detective_unit_ready(>=10)", "millionaire_unit_ready(>=15)", "escape_room_candidates(int 1-25, >=4 steps)", "authored_error_analysis_items"])
    for unit in course["units"]:
        for lv in ["cp2", "cp1", "honors"]:
            m = pool[(unit["id"], lv)]["mc"]
            w.writerow([unit["id"], lv, m, m >= 10, m >= 15, esc[(unit["id"], lv)], err[(unit["id"], lv)]])
if "--print" in sys.argv:
    tot = sum(r[4] for r in rows)
    print("total questions:", tot)
    print("cells <8:", sum(r[4] < 8 for r in rows), " cells <10:", sum(r[4] < 10 for r in rows),
          " cells with <5 MC:", sum(r[5] < 5 for r in rows), " skill-level cells >=10 MC:", sum(r[5] >= 10 for r in rows))
    print("distinct (number swaps collapsed):", sum(r[9] for r in rows), " cells with <8 distinct:", sum(r[9] < 8 for r in rows))
    for r in rows:
        flag = " <8" if r[4] < 8 else ""
        print(f"{r[1]:34s} {r[3]:6s} total {r[4]:3d}  MC {r[5]:2d} SA {r[6]:2d} SEL {r[7]:2d} OR {r[8]:2d} distinct {r[9]:2d}{flag}")
    print("formats:", {f: sum(cnt[k] for k in cnt if k[3] == f) for f in FORMATS})
