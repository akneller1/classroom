#!/usr/bin/env python3
"""Build a teacher review packet for every new or corrected Statistics item.

Usage: python3 make_review_packet.py <output_root> <statistics-course.json>
Writes reports/review/review-sheet.csv (one row per item, with blank Decision and Notes
columns for the reviewer) and reports/review/review-packet.html (printable, grouped by unit,
skill, and level, with Approve / Revise / Remove boxes).

Flags shown to the reviewer:
  * conceptual       — not numerically verified; check the key and distractors by hand
  * key-longest      — in multiple choice, the key is the longest option (a guessing cue)
  * similar-to <id>  — prompt is >85% similar to another item in the same cell (number swap)
  * implied-input    — verifier could not find an input number printed in the prompt
  * corrected        — baseline item whose part answers were replaced
"""
import csv, difflib, html, json, os, re, subprocess, sys
from collections import defaultdict

ROOT, COURSE = sys.argv[1], sys.argv[2]
course = json.load(open(COURSE, encoding="utf-8"))
OUT = os.path.join(ROOT, "reports", "review")
os.makedirs(OUT, exist_ok=True)
checks = json.load(open(os.path.join(ROOT, "scripts", "verification", "checks.json"), encoding="utf-8"))
corrected = {l.split(":")[0] for l in open(os.path.join(ROOT, "scripts", "verification", "corrections.log"), encoding="utf-8") if l.strip()}
v = subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "verify_expansion.py"), ROOT], capture_output=True, text=True).stdout
implied = {m.group(1) for m in re.finditer(r"WARN (\S+):", v)}

PURPOSE = [("_tarsia)", "Tarsia"), ("Partner Check pair", "Partner Check"), ("_error)", "Error Analysis"),
           ("_escape)", "Escape Room"), ("_mcfill)", "MC fill (Detective/Millionaire)")]
skillname = {s["id"]: s["name"] for u in course["units"] for s in u["skills"]}
cells = defaultdict(list)
for u in course["units"]:
    for q in json.load(open(os.path.join(ROOT, "question-banks", "statistics", u["id"] + ".json"), encoding="utf-8"))["questions"]:
        if "-x" in q["id"] or q["id"] in corrected:
            cells[(u["name"], q["skillId"], q["level"])].append(q)

rows = []
for key in sorted(cells, key=lambda k: (k[1], ["cp2", "cp1", "honors"].index(k[2]))):
    qs = cells[key]
    norm = [re.sub(r"[\d.,]+", "#", q["prompt"].lower()) for q in qs]
    for i, q in enumerate(qs):
        flags = []
        if q["id"] in corrected:
            flags.append("corrected")
        if q["id"] not in checks:
            flags.append("conceptual")
        if q["format"] == "multiple-choice":
            longest = max(q["options"], key=lambda o: len(o["text"]))
            if longest["correct"] and sum(len(o["text"]) == len(longest["text"]) for o in q["options"]) == 1:
                flags.append("key-longest")
        for j in range(i):
            if difflib.SequenceMatcher(None, norm[i], norm[j]).ratio() > 0.85:
                flags.append("similar-to " + qs[j]["id"]); break
        if q["id"] in implied:
            flags.append("implied-input")
        purpose = next((p for tag, p in PURPOSE if tag in q.get("sourceNotes", "")), "Practice")
        opts = " | ".join(("✓ " if o["correct"] else "  ") + o["text"] for o in q.get("options", []))
        parts = " | ".join(f"({chr(97 + k)}) {p['prompt']} → {p['answer']}" for k, p in enumerate(q.get("parts", [])))
        ans = q["answer"] if isinstance(q["answer"], str) else "; ".join(q["answer"])
        rows.append({"id": q["id"], "unit": key[0], "skill": skillname[q["skillId"]], "level": q["level"], "format": q["format"], "purpose": purpose,
                     "prompt": q["prompt"], "options": opts, "parts": parts, "answer": ans, "solution": " / ".join(q["solutionSteps"]),
                     "verification": "numeric, independently recomputed" if q["id"] in checks else "conceptual (review by hand)",
                     "flags": "; ".join(flags), "decision": "", "notes": ""})

with open(os.path.join(OUT, "review-sheet.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

E = html.escape
doc = ["<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Statistics bank — teacher review packet</title><style>",
       "body{font-family:Georgia,serif;max-width:900px;margin:24px auto;color:#111;line-height:1.4}h1{font-size:22px}h2{font-size:18px;border-bottom:2px solid #333;margin-top:28px}",
       "h3{font-size:15px;margin:18px 0 6px}.q{border:1px solid #bbb;padding:10px 12px;margin:8px 0;page-break-inside:avoid}.meta{font:12px sans-serif;color:#444}",
       ".p{white-space:pre-wrap;margin:6px 0}.k{font-weight:bold}.f{font:12px sans-serif;color:#8a1c1c}.box{font:12px sans-serif;margin-top:6px}",
       "ul{margin:4px 0 4px 18px;padding:0}@media print{body{margin:0}}</style></head><body>",
       "<h1>Statistics question bank — teacher review packet</h1>",
       f"<p class='meta'>{len(rows)} items to review (all new items plus {len(corrected)} corrected baseline items). Numeric items were independently recomputed; "
       "items marked <b>conceptual</b> need a hand check of the key and distractors. Flags: key-longest = the correct option is the longest (guessing cue); "
       "similar-to = near-duplicate of another item in the same cell; implied-input = a number is implied by wording rather than printed. Mark each item "
       "Approve, Revise, or Remove. The same list is in review-sheet.csv for spreadsheets.</p>"]
cur_u = cur_s = None
for r in rows:
    if r["unit"] != cur_u:
        doc.append(f"<h2>{E(r['unit'])}</h2>"); cur_u, cur_s = r["unit"], None
    if (r["skill"], r["level"]) != cur_s:
        doc.append(f"<h3>{E(r['skill'])} — {r['level'].upper()}</h3>"); cur_s = (r["skill"], r["level"])
    doc.append("<div class='q'>")
    doc.append(f"<div class='meta'>{E(r['id'])} · {E(r['format'])} · {E(r['purpose'])} · {E(r['verification'])}</div>")
    doc.append(f"<div class='p'>{E(r['prompt'])}</div>")
    if r["options"]:
        doc.append("<ul>" + "".join(f"<li{' class=k' if o.startswith('✓') else ''}>{E(o)}</li>" for o in r["options"].split(" | ")) + "</ul>")
    if r["parts"]:
        doc.append("<ul>" + "".join(f"<li>{E(p)}</li>" for p in r["parts"].split(" | ")) + "</ul>")
    doc.append(f"<div><span class='k'>Answer:</span> {E(r['answer'])}</div>")
    doc.append(f"<div class='meta'>Solution: {E(r['solution'])}</div>")
    if r["flags"]:
        doc.append(f"<div class='f'>Flags: {E(r['flags'])}</div>")
    doc.append("<div class='box'>☐ Approve &nbsp; ☐ Revise &nbsp; ☐ Remove &nbsp; Notes: ______________________________</div></div>")
doc.append("</body></html>")
open(os.path.join(OUT, "review-packet.html"), "w", encoding="utf-8").write("\n".join(doc))

from collections import Counter
fc = Counter(f.split(" ")[0] for r in rows for f in r["flags"].split("; ") if f)
print(f"review items: {len(rows)}; conceptual: {sum('conceptual' in r['flags'] for r in rows)}; flags: {dict(fc)}")
