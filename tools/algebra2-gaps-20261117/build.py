"""Algebra 2 audit batch D: add the standards-gap skills and the context problems to the banks.

New skills are registered at the end of course-catalog.js (existing ids stay stable; the new id is
<unit>-skill-NN by catalog order) and get 16 items per level: 7 short answer, 6 multiple choice,
2 find-the-mistake and 1 four-part open response. Context problems are added to an existing skill in
each unit (9 per level per unit; conic sections split 6 + 3 between parabolas and circles).
Check data for verify.py goes to out/checks.json.

Usage: python3 tools/algebra2-gaps-20261117/build.py
Re-running is safe: skills and context sets that already exist are skipped.
"""
import json, os, random, re, subprocess, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import families as FAM  # noqa: E402  (also puts the 2026-11-16 helpers on the path)
from core import Reject  # noqa: E402

LEVELS = ["cp2", "cp1", "honors"]
NAMES = ["Ava", "Ben", "Chloe", "Diego", "Emma", "Farah", "Gabe", "Hana", "Isaac", "Jada", "Kenji", "Leah", "Mateo", "Nia", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tariq"]
NOTE = ("Original Claude-authored item (family: {fam}). Answer, every option and every student answer re-checked from the printed "
        "problem by tools/algebra2-gaps-20261117/verify.py. Awaiting human review.")
CAT = os.path.join(ROOT, "course-catalog.js")
CHECKS = os.path.join(HERE, "out", "checks.json")
MARK = "  // Algebra 2 audit additions, November 17, 2026 (standards gaps). Existing skill IDs stay stable.\n"
EXPORT = "  root.MK_COURSE_CATALOG = {"
CONTEXT_TAG = "context-problem"


def load_json(p):
    raw = open(p, encoding="utf-8").read()
    return json.loads(raw, object_pairs_hook=OrderedDict), raw


def dump_json(p, data, raw):
    ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else (0 if raw.startswith('{\n"') else None))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=ind)
        if raw.endswith("\n"):
            f.write("\n")


def catalog_names(unit):
    out = subprocess.run(["node", "-e", "require(process.argv[1]);console.log(JSON.stringify(globalThis.MK_COURSE_CATALOG.getSkills('algebra2',process.argv[2])))", CAT, unit],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def add_to_catalog(unit, name):
    names = catalog_names(unit)
    if name in names:
        return names.index(name) + 1
    s = open(CAT, encoding="utf-8").read()
    if MARK not in s:
        s = s.replace(EXPORT, MARK + EXPORT, 1)
    line = f"  skills[\"algebra2\"][{json.dumps(unit)}].push({json.dumps(name, ensure_ascii=False)});\n"
    s = s.replace(EXPORT, line + EXPORT, 1)
    open(CAT, "w", encoding="utf-8").write(s)
    names = catalog_names(unit)
    assert names[-1] == name
    return len(names)


def make(fns, r, L, used, min_wrongs=0, tries=4000):
    for _ in range(tries):
        fn = r.choice(fns)
        try:
            it = fn(r, L)
        except Reject:
            continue
        if it["prompt"] in used or len(it["wrongs"]) < min_wrongs:
            continue
        used.add(it["prompt"])
        return it
    raise SystemExit(f"could not make a new item from {[f.__name__ for f in fns]} at level {L}")


def item(kind, it, r, base, unit, checks, skill_name, worked_parts=None):
    if kind == "sa":
        q = base(it, "short-answer")
        q["solutionSteps"] = it["steps"]
        checks[q["id"]] = dict(it["check"])
        return q, [], it["fam"]
    if kind == "mc":
        q = base(it, "multiple-choice")
        opts = [OrderedDict(text=it["answer"], correct=True)] + [OrderedDict(text=t, correct=False) for t, _ in it["wrongs"][:3]]
        r.shuffle(opts)
        q["options"] = opts
        q["solutionSteps"] = it["steps"]
        checks[q["id"]] = dict(it["check"])
        return q, [], it["fam"]
    if kind == "ea":
        wrong, why = it["wrongs"][0]
        who = r.choice(NAMES)
        q = base(it, "short-answer")
        q["prompt"] = f"{who} answered this problem incorrectly.\n{it['prompt']}\n{who}'s answer: {wrong}\nIdentify the mistake and give the correct answer."
        q["solutionSteps"] = [f"Mistake: {who} {why}."] + it["steps"] + [f"The correct answer is {it['answer']}, not {wrong}."]
        checks[q["id"]] = dict(it["check"], student=wrong)
        return q, ["error-analysis", "misconception"], it["fam"] + "_error"
    parts = worked_parts
    q = base(dict(prompt=f"Practice set ({skill_name}): answer each part and show your work.", answer=""), "open-response")
    q["parts"] = [OrderedDict(prompt=p["prompt"], answer=p["answer"]) for p in parts]
    q["answer"] = "; ".join(f"({'abcd'[i]}) {p['answer'].rstrip('.')}" for i, p in enumerate(parts))
    q.move_to_end("answer")
    q["solutionSteps"] = [f"({'abcd'[i]}) " + " ".join(p["steps"]) for i, p in enumerate(parts)]
    checks[q["id"]] = dict(parts=[p["check"] for p in parts])
    return q, ["multistep"], parts[0]["fam"] + "_open"


SKILL_PLAN = ["sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "ea", "or", "ea"]
CONTEXT_PLAN = {9: ["sa", "mc", "sa", "sa", "mc", "sa", "ea", "sa", "mc"], 6: ["sa", "mc", "sa", "sa", "mc", "ea"], 3: ["sa", "mc", "sa"]}


def build(unit, sidx, fns, stds, prefix, plan, idtag, r, used, checks, skill_name, extra_tags=()):
    out, tags = [], {}
    worked = [f for f in fns if not getattr(f, "mc_only", False)]
    for L, lv in enumerate(LEVELS):
        n = 0
        avail = [f for f in worked]

        def base(it, fmt):
            nonlocal n
            n += 1
            return OrderedDict(id=f"{prefix}-s{sidx:02d}-{lv}-{idtag}{n:03d}", skillId=f"{unit}-skill-{sidx:02d}", level=lv, format=fmt, prompt=it["prompt"], answer=it["answer"])

        for kind in plan:
            if kind == "or":
                parts = [make(avail, r, L, used) for _ in range(4)]
                q, tg, fam = item(kind, None, r, base, unit, checks, skill_name, parts)
            else:
                it = make(fns if kind == "mc" else avail, r, L, used, min_wrongs=3 if kind == "mc" else 1)
                q, tg, fam = item(kind, it, r, base, unit, checks, skill_name)
            q["standards"] = stds
            q["sourceNotes"] = NOTE.format(fam=fam)
            ctx = ("modeling", CONTEXT_TAG) if re.sub(r"_(error|open)$", "", fam) in FAM.CONTEXTUAL else ()
            tags[q["id"]] = list(dict.fromkeys(list(tg) + list(extra_tags) + list(ctx)))
            out.append(q)
    return out, tags


def append(unit, qs, tags):
    bp = os.path.join(ROOT, "question-banks", "algebra2", unit + ".json")
    bank, raw = load_json(bp)
    ids = {q["id"] for q in bank["questions"]}
    assert not ids & {q["id"] for q in qs}, unit
    bank["questions"].extend(qs)
    dump_json(bp, bank, raw)
    tp = os.path.join(ROOT, "question-banks", "algebra2", "meta", unit + ".tags.json")
    tg, traw = load_json(tp)
    tg.update(tags)
    dump_json(tp, tg, traw)


def main():
    os.makedirs(os.path.dirname(CHECKS), exist_ok=True)
    checks = json.load(open(CHECKS)) if os.path.exists(CHECKS) else {}
    for unit, name, fns, stds, prefix in FAM.NEW_SKILLS:
        bank, _ = load_json(os.path.join(ROOT, "question-banks", "algebra2", unit + ".json"))
        sidx = add_to_catalog(unit, name)
        sid = f"{unit}-skill-{sidx:02d}"
        if any(q["skillId"] == sid for q in bank["questions"]):
            print(f"skip {sid} (already has items)")
            continue
        r = random.Random(f"a2-gap-{unit}-{name}")
        used = {q["prompt"] for q in bank["questions"]}
        qs, tags = build(unit, sidx, fns, stds, prefix, SKILL_PLAN, "", r, used, checks, name)
        append(unit, qs, tags)
        print(f"{sid} {name}: + {len(qs)} items")
    for key, (sidx, fns, stds, prefix) in FAM.CONTEXT.items():
        unit = key.split("#")[0]
        per = 3 if key.endswith("#circle") else (6 if unit == "conic-sections" else 9)
        bank, _ = load_json(os.path.join(ROOT, "question-banks", "algebra2", unit + ".json"))
        sid = f"{unit}-skill-{sidx:02d}"
        if any(q["skillId"] == sid and re.search(r"-w\d{3}$", q["id"]) for q in bank["questions"]):
            print(f"skip context {sid}")
            continue
        r = random.Random(f"a2-context-{key}")
        used = {q["prompt"] for q in bank["questions"]}
        name = catalog_names(unit)[sidx - 1]
        qs, tags = build(unit, sidx, fns, stds, prefix, CONTEXT_PLAN[per], "w", r, used, checks, name, extra_tags=("modeling", CONTEXT_TAG))
        append(unit, qs, tags)
        print(f"{sid} context: + {len(qs)} items")
    json.dump(checks, open(CHECKS, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
