"""Audit #14: list the bank-driven Stations Generator for the seven Algebra 2 units that had no station set.

The printables generator (worksheet-generator/printables.html, kind=stations) already builds station pages from
the Algebra 2 banks for every unit; this adds the library listing and a thumbnail, as Algebra 1 and Geometry have.
Edits data.js as text so its formatting is unchanged. Idempotent.
"""
import json, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
UNITS = ["polynomial-functions", "radicals-rational-exponents", "rational-functions", "sequences-series", "conic-sections", "trigonometric-functions", "probability-statistics"]
DESC = ("Make station pages for this unit from the Algebra 2 question bank: choose 2–6 stations and 6–10 problems each, and the chosen "
        "skills are split across the stations. CP2/CP1/Honors, up to three versions, a one-page answer key and worked solutions. Every answer is checked.")
path = os.path.join(ROOT, "data.js")
s = open(path, encoding="utf-8").read()
a = s.index("window.LIBRARY = ") + len("window.LIBRARY = ")
lib = json.loads(s[a:s.index("\n};\n", a) + 2])
course = next(c for c in lib["courses"] if c["id"] == "algebra2")
tpl = open(os.path.join(ROOT, "thumbs/stations-generator-quadratics.svg"), encoding="utf-8").read()
start = s.index('"id": "algebra2"', a)
added = 0
for unit in UNITS:
    name = next(u["name"] for u in course["units"] if u["id"] == unit)
    href = f"worksheet-generator/printables.html#unit=algebra2-{unit}&kind=stations"
    if href in s:
        continue
    thumb = f"thumbs/stations-generator-algebra2-{unit}.svg"
    svg = tpl.replace("QUADRATIC FUNCTIONS AND EQUATIONS", name.upper().replace("&", "&amp;"))
    open(os.path.join(ROOT, thumb), "w", encoding="utf-8").write(svg)
    i = s.index(f'"id": "{unit}"', start)
    j = s.index('"artifacts": [', i)
    # matching close bracket of this artifacts array
    depth, k = 0, j + len('"artifacts": ')
    while True:
        ch = s[k]
        if ch == "[": depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0: break
        elif ch == '"':
            k += 1
            while s[k] != '"':
                k += 2 if s[k] == "\\" else 1
        k += 1
    entry = {"title": "Stations Generator", "path": href, "thumb": thumb, "description": DESC, "type": "Printable",
             "topics": ["Printable generator", "Stations", name], "level": ["CP2", "CP1", "Honors"], "added": "2026-11-17"}
    body = json.dumps(entry, indent=2, ensure_ascii=False).replace("\n", "\n" + " " * 12)
    before = s[:k].rstrip()
    s = before + ",\n" + " " * 12 + body + "\n" + " " * 10 + s[k:]
    added += 1
open(path, "w", encoding="utf-8").write(s)
a = s.index("window.LIBRARY = ") + len("window.LIBRARY = ")
json.loads(s[a:s.index("\n};\n", a) + 2])  # still valid JSON
print("added", added, "Stations Generator listings")
