"""Add the 2026-11-16 audit gap skills to the published banks without touching existing items.

For each new skill: register its name at the end of course-catalog.js (existing skill ids stay
stable; the new id is <unit>-skill-NN by catalog order), then append 16 items per level (7 short
answer, 6 multiple choice, 2 error analysis, 1 four-part open response) to
question-banks/<course>/<unit>.json, add tags where the course keeps a tags file, and write the
check data to out/checks.json. Run verify.py afterwards (must print TOTAL ERRORS 0).

Usage: python3 build.py <repo root>
Re-running is safe: skills that already have questions are skipped.
"""
import json, os, random, re, subprocess, sys
from collections import OrderedDict

ROOT = os.path.abspath(sys.argv[1])
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from core import Reject
import ms_families, stat_families, hs_families, geo_families

SKILLS = OrderedDict()
for mod in (ms_families, hs_families, stat_families, geo_families):
    SKILLS.update(mod.SKILLS)

LEVELS = ["cp2", "cp1", "honors"]
NAMES = ["Ava", "Ben", "Chloe", "Diego", "Emma", "Farah", "Gabe", "Hana", "Isaac", "Jada", "Kenji", "Leah", "Mateo", "Nia", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tariq"]
NOTE = ("Original Claude-authored item (family: {fam}). Answer, every option and every student answer re-checked from the printed "
        "problem by tools/audit-gap-skills-20261116/verify.py. Awaiting human review.")
CAT = os.path.join(ROOT, "course-catalog.js")
CHECKS = os.path.join(HERE, "out", "checks.json")
MARK = "  // Coverage-gap additions, November 16, 2026 (site audit). Existing skill IDs stay stable.\n"
EXPORT = "  root.MK_COURSE_CATALOG = {"


def load_json(p):
    raw = open(p, encoding="utf-8").read()
    return json.loads(raw, object_pairs_hook=OrderedDict), raw


def dump_json(p, data, raw):
    ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else (0 if raw.startswith('{\n"') else None))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=ind)
        if raw.endswith("\n"):
            f.write("\n")


def catalog_names(course, unit):
    out = subprocess.run(["node", "-e", "require(process.argv[1]);console.log(JSON.stringify(globalThis.MK_COURSE_CATALOG.getSkills(process.argv[2],process.argv[3])))", CAT, course, unit], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def add_to_catalog(course, unit, name):
    names = catalog_names(course, unit)
    if name in names:
        return names.index(name) + 1
    s = open(CAT, encoding="utf-8").read()
    if MARK not in s:
        s = s.replace(EXPORT, MARK + EXPORT, 1)
    line = f"  skills[{json.dumps(course)}][{json.dumps(unit)}].push({json.dumps(name, ensure_ascii=False)});\n"
    s = s.replace(EXPORT, line + EXPORT, 1)
    open(CAT, "w", encoding="utf-8").write(s)
    names = catalog_names(course, unit)
    assert names[-1] == name
    return len(names)


def ensure_bank(course, unit):
    bp = os.path.join(ROOT, "question-banks", course, unit + ".json")
    if not os.path.exists(bp):
        dump_json(bp, OrderedDict(schemaVersion=1, courseId=course, unitId=unit, questions=[]), '{\n "x"\n')
    mp = os.path.join(ROOT, "question-banks", "manifest.json")
    man, mraw = load_json(mp)
    if not any(b["courseId"] == course and b["unitId"] == unit for b in man["banks"]):
        i = max(i for i, b in enumerate(man["banks"]) if b["courseId"] == course)
        man["banks"].insert(i + 1, OrderedDict(courseId=course, unitId=unit, path=f"question-banks/{course}/{unit}.json", approved=True))
        dump_json(mp, man, mraw)


def make(fns, r, L, used, min_wrongs=0, tries=3000):
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


def build_skill(course, unit, fns, stds, sidx, prefix, r, used, checks):
    out, tags = [], {}
    worked = [f for f in fns if not getattr(f, "mc_only", False)]
    for L, lv in enumerate(LEVELS):
        n = 0

        def base(it, fmt):
            nonlocal n
            n += 1
            return OrderedDict(id=f"{prefix}-s{sidx:02d}-{lv}-{n:03d}", skillId=f"{unit}-skill-{sidx:02d}", level=lv, format=fmt, prompt=it["prompt"], answer=it["answer"])

        for kind in ["sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "ea", "or", "ea"]:
            if kind == "sa":
                it = make(worked, r, L, used)
                q = base(it, "short-answer")
                q["solutionSteps"] = it["steps"]
                tags[q["id"]] = []
                checks[q["id"]] = dict(it["check"], bank=[course, unit])
                fam = it["fam"]
            elif kind == "mc":
                it = make(fns, r, L, used, min_wrongs=3)
                q = base(it, "multiple-choice")
                opts = [OrderedDict(text=it["answer"], correct=True)] + [OrderedDict(text=t, correct=False) for t, _ in it["wrongs"][:3]]
                r.shuffle(opts)
                q["options"] = opts
                q["solutionSteps"] = it["steps"]
                tags[q["id"]] = []
                checks[q["id"]] = dict(it["check"], bank=[course, unit])
                fam = it["fam"]
            elif kind == "ea":
                it = make(worked, r, L, used, min_wrongs=1)
                wrong, why = it["wrongs"][0]
                who = r.choice(NAMES)
                q = base(it, "short-answer")
                q["prompt"] = f"{who} answered this problem incorrectly.\n{it['prompt']}\n{who}'s answer: {wrong}\nIdentify the mistake and give the correct answer."
                q["solutionSteps"] = [f"Mistake: {who} {why}."] + it["steps"] + [f"The correct answer is {it['answer']}, not {wrong}." if len(it["answer"]) <= 40 and not it["answer"].endswith(".") else f"Correct answer: {it['answer']}"]
                tags[q["id"]] = ["error-analysis", "misconception"]
                checks[q["id"]] = dict(it["check"], bank=[course, unit], student=wrong)
                fam = it["fam"] + "_error"
            else:
                parts = [make(worked, r, L, used) for _ in range(4)]
                q = base(dict(prompt="Answer each part. Show your work.", answer=""), "open-response")
                q["parts"] = [OrderedDict(prompt=p["prompt"], answer=p["answer"]) for p in parts]
                q["answer"] = "; ".join(f"({'abcd'[i]}) {p['answer'].rstrip('.')}" for i, p in enumerate(parts))
                q.move_to_end("answer")
                q["solutionSteps"] = [f"({'abcd'[i]}) " + " ".join(p["steps"]) for i, p in enumerate(parts)]
                tags[q["id"]] = ["multistep"]
                checks[q["id"]] = dict(bank=[course, unit], parts=[p["check"] for p in parts])
                fam = parts[0]["fam"] + "_open"
            q["standards"] = stds
            q["sourceNotes"] = NOTE.format(fam=fam)
            out.append(q)
    return out, tags


def main():
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    checks = json.load(open(CHECKS, encoding="utf-8")) if os.path.exists(CHECKS) else {}
    for (course, unit, name), spec in SKILLS.items():
        if spec.get("new_bank"):
            ensure_bank(course, unit)
        sidx = add_to_catalog(course, unit, name)
        bp = os.path.join(ROOT, "question-banks", course, unit + ".json")
        tp = os.path.join(ROOT, "question-banks", course, "meta", unit + ".tags.json")
        bank, raw = load_json(bp)
        if any(q["skillId"] == f"{unit}-skill-{sidx:02d}" for q in bank["questions"]):
            print(f"skip {course}/{unit}: '{name}' already has questions (skill {sidx})")
            continue
        used = {q["prompt"] for q in bank["questions"]}
        r = random.Random(f"{course}/{unit}/{name}/20261116")
        items, tags = build_skill(course, unit, spec["fns"], spec["stds"], sidx, spec["prefix"], r, used, checks)
        ids = {q["id"] for q in bank["questions"]}
        assert not ids & {q["id"] for q in items}, "id collision"
        bank["questions"].extend(items)
        dump_json(bp, bank, raw)
        if os.path.exists(tp):
            tg, traw = load_json(tp)
            tg.update(tags)
            dump_json(tp, tg, traw)
        print(f"{course}/{unit}: skill {sidx:02d} '{name}' + {len(items)} items")
    json.dump(checks, open(CHECKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
