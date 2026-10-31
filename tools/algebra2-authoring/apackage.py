import json, os, glob, zipfile, collections, datetime
REPO = "/home/claude/repo/classroom-main"
import sys; sys.path.insert(0, REPO)
OUT = "out"; DEL = "/mnt/user-data/outputs"; os.makedirs(DEL, exist_ok=True)
# usage: python3 package.py [batch-name unit ...]  → one batch ZIP holding those units (default: one ZIP per unit)
BATCH = sys.argv[1] if len(sys.argv) > 2 else None; ONLY = set(sys.argv[2:]) if BATCH else None
cat = json.loads(os.popen(f"cd {REPO} && node -e \"require('./course-catalog.js');console.log(JSON.stringify(globalThis.MK_COURSE_CATALOG.skills.algebra))\"").read())
UNITS = list(cat.keys())
done = {}
for f in sorted(glob.glob(f"{OUT}/question-banks/algebra/*.json")):
    d = json.load(open(f)); done[d["unitId"]] = d
TARGET = 30
LES = json.loads(os.popen(f"cd {REPO} && node -e \"global.window=global;require('./worksheet-generator/planner/lesson-skills.js');console.log(JSON.stringify(global.MKPLAN_SKILLS.lessons))\"").read())
matrix = ["# Algebra 1 coverage matrix", "", f"Generated {datetime.date.today()}. Legacy generator coverage from worksheet-generator/planner/lesson-skills.js (one lesson per catalog skill). New shared-format bank items were written only for skills the generators cover partly or not at all. Target ≈ {TARGET} items per gap skill.", "",
          "| Unit | Skill | Skill name | Legacy generator | CP2 | CP1 | Honors | Bank total | Status |", "|---|---|---|---|---|---|---|---|---|"]
for ui, u in enumerate(UNITS, 1):
    for i, name in enumerate(cat[u], 1):
        sid = f"{u}-skill-{i:02d}"; cov = LES.get(f"U{ui}-L{i}", {}).get("cover", "?")
        c = collections.Counter(q["level"] for q in done.get(u, {"questions": []})["questions"] if q["skillId"] == sid)
        tot = sum(c.values())
        st = ("draft complete (gap filled)" if tot >= TARGET else "draft (below target)") if tot else ("generator only" if cov == "full" else "GAP — not started")
        matrix.append(f"| {u} | {i:02d} | {name} | {cov} | {c['cp2']} | {c['cp1']} | {c['honors']} | {tot} | {st} |")
open(f"{OUT}/ALGEBRA1_COVERAGE_MATRIX.md", "w").write("\n".join(matrix) + "\n")

def key_md(d):
    L = [f"# Answer key — algebra / {d['unitId']}", "", "Draft for human review. Not approved.", ""]
    names = cat[d["unitId"]]
    for i, nm in enumerate(names, 1):
        sid = f"{d['unitId']}-skill-{i:02d}"
        qs = [q for q in d["questions"] if q["skillId"] == sid]
        if not qs: continue
        L += [f"## Skill {i:02d}: {nm}", ""]
        for q in qs:
            L.append(f"**{q['id']}** ({q['level']}, {q['format']}){' [diagram: ' + q['diagram']['spec']['src'].split('/')[-1] + ']' if 'diagram' in q else ''}  ")
            L.append(q["prompt"] + "  ")
            for o in q.get("options", []): L.append(f"- {'✔' if o['correct'] else '○'} {o['text']}")
            for j, p in enumerate(q.get("parts", [])): L.append(f"- ({chr(97+j)}) {p['prompt']} → **{p['answer']}**")
            if "parts" not in q: L.append(f"Answer: **{q['answer'] if not isinstance(q['answer'], list) else '; '.join(q['answer'])}**  ")
            L.append("Solution: " + " ".join(q["solutionSteps"]))
            L.append("")
    return "\n".join(L)

zb = zipfile.ZipFile(f"{DEL}/algebra1-{BATCH}.zip", "w", zipfile.ZIP_DEFLATED) if BATCH else None
for u, d in done.items():
    if ONLY and u not in ONLY: continue
    tags = json.load(open(f"{OUT}/question-banks/algebra/meta/{u}.tags.json"))
    tagc = collections.Counter(t for v in tags.values() for t in v)
    fmtc = collections.Counter(q["format"] for q in d["questions"])
    dia = sum(1 for q in d["questions"] if "diagram" in q)
    rep = [f"# Coverage report — algebra/{u}", "", f"Questions: {len(d['questions'])} | diagrams: {dia} | formats: {dict(fmtc)}", f"Enrichment tags: {dict(tagc)}", "",
           "| Skill | CP2 | CP1 | Honors | Total |", "|---|---|---|---|---|"]
    for i, nm in enumerate(cat[u], 1):
        sid = f"{u}-skill-{i:02d}"; c = collections.Counter(q["level"] for q in d["questions"] if q["skillId"] == sid)
        if not sum(c.values()): continue
        rep.append(f"| {i:02d} {nm} | {c['cp2']} | {c['cp1']} | {c['honors']} | {sum(c.values())} |")
    note = f"""# Integration note — algebra/{u}

This bank holds ONLY the gap skills of this unit (skills the legacy generators cover partly or not at all); other skills remain generator-only. It does not replace the legacy Algebra 1 generators.

Files (copy into the repo at the same relative paths):
- question-banks/algebra/{u}.json — bank payload, schemaVersion 1; skill IDs from MK_COURSE_CATALOG.getSkillRecords('algebra', '{u}').
- question-banks/assets/algebra/{u}/*.png — raster graphs referenced by diagram.spec.src (type "image", alt text included).
- question-banks/algebra/meta/{u}.tags.json — sidecar map id → enrichment tags (challenge, misconception, error-analysis, modeling, graph, multiple-representations, reasoning, connections, multistep). Kept outside the bank because the schema forbids extra question properties.
- ANSWER_KEY.md — human-readable key with worked solutions for reviewer sign-off.

Dependencies: none beyond the existing course-catalog.js, question-bank-adapter.js and question-bank-loader.js.
Check: `node scripts/check-question-bank.cjs question-banks/algebra/{u}.json` (passes).
Per docs/CLAUDE_QUESTION_BANK_HANDOFF.md, do NOT add `approved: true` to question-banks/manifest.json until a human has reviewed the math. Shared games currently skip items that have a diagram ({dia} items here).
Text notation is plain Unicode (x², √, ≤, π, i); no TeX.
"""
    z = zb or zipfile.ZipFile(f"{DEL}/algebra1-{u}.zip", "w", zipfile.ZIP_DEFLATED)
    pre = f"docs/algebra1-banks/{u}/" if zb else ""
    z.write(f"{OUT}/question-banks/algebra/{u}.json", f"question-banks/algebra/{u}.json")
    z.write(f"{OUT}/question-banks/algebra/meta/{u}.tags.json", f"question-banks/algebra/meta/{u}.tags.json")
    for a in sorted(glob.glob(f"{OUT}/question-banks/assets/algebra/{u}/*.png")):
        z.write(a, a[len(OUT) + 1:])
    z.writestr(pre + "ANSWER_KEY.md", key_md(d)); z.writestr(pre + "COVERAGE_REPORT.md", "\n".join(rep) + "\n"); z.writestr(pre + "INTEGRATION_NOTE.md", note)
    if not zb: z.close()
if zb:
    zb.write(f"{OUT}/ALGEBRA1_COVERAGE_MATRIX.md", "docs/algebra1-banks/ALGEBRA1_COVERAGE_MATRIX.md")
    if os.path.exists("ALGEBRA1_PROGRESS.md"): zb.write("ALGEBRA1_PROGRESS.md", "docs/algebra1-banks/PROGRESS.md")
    for f in sorted(["a1_gaps.py", "lib.py", "mathlite.py", "fill.py", "apackage.py"]): zb.write(f, "tools/bank-authoring/" + f)
    zb.close(); print("wrote", f"{DEL}/algebra1-{BATCH}.zip")
print(open(f"{OUT}/ALGEBRA1_COVERAGE_MATRIX.md").read()[:400])
