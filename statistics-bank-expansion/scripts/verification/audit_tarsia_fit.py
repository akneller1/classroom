#!/usr/bin/env python3
"""Audit every bank in a site's question-banks/manifest.json (all courses) for Tarsia fit.

Usage: python3 audit_tarsia_fit.py <site_root> [--max-prompt 110] [--max-answer 20] [--need 18]
An item is Tarsia-eligible if it is short-answer or multiple-choice, its answer is a single
string of <= max-answer characters, its prompt is <= max-prompt characters with no line
break, and it has no diagram. A Tarsia puzzle also needs DISTINCT answers (case- and
space-insensitive), because pieces are matched by answer text. For each course/unit/level the
report gives the eligible count, the distinct-answer count, and whether it reaches --need
(18 = edges of a standard 16-triangle Tarsia). Long-prompt counts show how many items
would overflow a cell if the generator does not filter them.
"""
import json, os, re, sys, collections
args = sys.argv[1:]
root = args[0]
opt = lambda n, d: int(args[args.index(n) + 1]) if n in args else d
MP, MA, NEED = opt("--max-prompt", 110), opt("--max-answer", 20), opt("--need", 18)
man = json.load(open(os.path.join(root, "question-banks", "manifest.json"), encoding="utf-8"))
rows, missing = [], []
for b in man["banks"]:
    path = os.path.join(root, b["path"])
    if not os.path.exists(path):
        missing.append(b["path"]); continue
    qs = json.load(open(path, encoding="utf-8"))["questions"]
    for lv in ("cp2", "cp1", "honors"):
        L = [q for q in qs if q.get("level") == lv]
        el = [q for q in L if q["format"] in ("short-answer", "multiple-choice") and isinstance(q.get("answer"), str)
              and len(q["answer"]) <= MA and len(q["prompt"]) <= MP and "\n" not in q["prompt"] and not q.get("diagram")]
        norm = {re.sub(r"\s+", " ", q["answer"].strip().casefold()) for q in el}
        longp = sum(len(q["prompt"]) > MP or "\n" in q["prompt"] for q in L)
        rows.append((b["courseId"], b["unitId"], lv, len(L), len(el), len(norm), longp))
print(f"{'course':14s}{'unit':36s}{'level':7s}{'items':>6s}{'elig':>6s}{'distinct':>9s}{'long':>6s}  status")
bad = 0
for r in rows:
    ok = r[5] >= NEED
    bad += not ok
    print(f"{r[0]:14s}{r[1]:36s}{r[2]:7s}{r[3]:6d}{r[4]:6d}{r[5]:9d}{r[6]:6d}  {'OK' if ok else 'SHORT'}")
print(f"\n{len(rows)} unit-levels audited; {bad} below {NEED} distinct eligible answers.")
if missing:
    print(f"{len(missing)} manifest banks not found under {root} (not audited): " + ", ".join(missing))
