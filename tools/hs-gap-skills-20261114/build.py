"""Add the 2026-11-14 HS gap skills to the published banks without touching existing items.

For each new skill: append its name to course-catalog.js (so the skill id is <unit>-skill-NN by
catalog order), then append 16 items per level (7 short answer, 6 multiple choice, 2 error
analysis, 1 four-part open response) to question-banks/<course>/<unit>.json, add tags to
question-banks/<course>/meta/<unit>.tags.json, and write the check data to out/checks.json.
Run verify.py afterwards (must print TOTAL ERRORS 0).

Usage: python3 build.py <repo root> calc|precalc|pa7
Re-running is safe: skills already in the catalog are skipped.
"""
import json, os, random, re, sys
from collections import OrderedDict

ROOT, WHICH = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
if WHICH == "calc":
    from calc_families import SKILLS, Reject
elif WHICH == "pa7":
    from pa7_families import SKILLS, Reject, NEW_UNITS
else:
    from precalc_families import SKILLS, Reject, NEW_UNITS
NEW_UNITS = globals().get("NEW_UNITS", {})

LEVELS = ["cp2", "cp1", "honors"]
MC_ONLY = {"cmp_infer"}          # statement answers: multiple choice only
NO_WORKED = {"lh_check"} | MC_ONLY  # not used for error analysis or open response
NAMES = ["Ava", "Ben", "Chloe", "Diego", "Emma", "Farah", "Gabe", "Hana", "Isaac", "Jada", "Kenji", "Leah", "Mateo", "Nia", "Omar", "Priya", "Quinn", "Rosa", "Sam", "Tariq"]
NOTE = ("Original Claude-authored item (family: {fam}). Answer, every option and every student answer re-checked numerically from the printed "
        "problem by tools/hs-gap-skills-20261114/verify.py. Awaiting human review.")
CAT = os.path.join(ROOT, "course-catalog.js")
CHECKS = os.path.join(HERE, "out", "checks.json")


def load_json(p):
    raw = open(p, encoding="utf-8").read()
    return json.loads(raw, object_pairs_hook=OrderedDict), raw


def dump_json(p, data, raw):
    ind = 1 if raw.startswith('{\n "') else (2 if raw.startswith('{\n  "') else (0 if raw.startswith('{\n"') else None))
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=ind)
        if raw.endswith("\n"):
            f.write("\n")


def ensure_unit(course, unit, first_name):
    """Add an empty-bank unit: catalog block (with its first skill), bank, tags and manifest entry."""
    s = open(CAT, encoding="utf-8").read()
    m = re.search(r'\n  "%s": \{' % re.escape(course), s)
    end = s.index("\n},", m.end())
    if re.search(r'\n  "%s": \[' % re.escape(unit), s[m.end():end]):
        return
    s = s[:end] + ",\n  " + json.dumps(unit) + ": [\n    " + json.dumps(first_name, ensure_ascii=False) + "\n  ]" + s[end:]
    open(CAT, "w", encoding="utf-8").write(s)
    bp = os.path.join(ROOT, "question-banks", course, unit + ".json")
    if not os.path.exists(bp):
        dump_json(bp, OrderedDict(schemaVersion=1, courseId=course, unitId=unit, questions=[]), '{\n "x"\n')
        dump_json(os.path.join(ROOT, "question-banks", course, "meta", unit + ".tags.json"), OrderedDict(), '{\n"x"\n')
    mp = os.path.join(ROOT, "question-banks", "manifest.json")
    man, mraw = load_json(mp)
    if not any(b["courseId"] == course and b["unitId"] == unit for b in man["banks"]):
        i = max(i for i, b in enumerate(man["banks"]) if b["courseId"] == course)
        man["banks"].insert(i + 1, OrderedDict(courseId=course, unitId=unit, path=f"question-banks/{course}/{unit}.json", approved=True, teacherUse=True))
        dump_json(mp, man, mraw)


def add_to_catalog(course, unit, name):
    s = open(CAT, encoding="utf-8").read()
    m = re.search(r'\n  "%s": \{' % re.escape(course), s)
    start = m.end()
    m2 = re.search(r'\n( +)"%s": \[\n(.*?)\n\1\]' % re.escape(unit), s[start:], re.S)
    body = m2.group(2)
    names = [json.loads(line.strip().rstrip(",")) for line in body.split("\n")]
    if name in names:
        return names.index(name) + 1, False
    pad = re.match(r" *", body).group(0)
    new_body = body + ",\n" + pad + json.dumps(name, ensure_ascii=False)
    s = s[:start + m2.start(2)] + new_body + s[start + m2.end(2):]
    open(CAT, "w", encoding="utf-8").write(s)
    return len(names) + 1, True


def make(fns, r, L, used, want_mc=False, tries=400):
    for _ in range(tries):
        fn = r.choice(fns)
        try:
            it = fn(r, L)
        except Reject:
            continue
        if it["prompt"] in used or (want_mc and len(it["wrongs"]) < 3):
            continue
        used.add(it["prompt"])
        return it
    raise SystemExit(f"could not make a new item from {[f.__name__ for f in fns]} at level {L}")


def build_skill(course, unit, name, fns, stds, sidx, prefix, r, used, checks):
    out, tags = [], {}
    for L, lv in enumerate(LEVELS):
        n = 0

        def nid():
            nonlocal n
            n += 1
            return f"{prefix}-s{sidx:02d}-{lv}-{n:03d}"

        def base(it, fmt):
            q = OrderedDict(id=nid(), skillId=f"{unit}-skill-{sidx:02d}", level=lv, format=fmt, prompt=it["prompt"], answer=it["answer"])
            return q

        plan = ["sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "mc", "sa", "ea", "or", "ea"]
        for kind in plan:
            if kind == "sa":
                it = make([f for f in fns if f.__name__ not in MC_ONLY], r, L, used)
                q = base(it, "short-answer")
                q["solutionSteps"] = it["steps"]
                tags[q["id"]] = ["reasoning"] if it["fam"] in ("lh_check",) else []
                checks[q["id"]] = dict(it["check"], bank=[course, unit])
            elif kind == "mc":
                it = make(fns, r, L, used, want_mc=True)
                q = base(it, "multiple-choice")
                opts = [OrderedDict(text=it["answer"], correct=True)] + [OrderedDict(text=t, correct=False) for t, _ in it["wrongs"][:3]]
                r.shuffle(opts)
                q["options"] = opts
                q["solutionSteps"] = it["steps"]
                tags[q["id"]] = []
                checks[q["id"]] = dict(it["check"], bank=[course, unit])
            elif kind == "ea":
                it = make([f for f in fns if f.__name__ not in NO_WORKED], r, L, used)
                wrong, why = it["wrongs"][0]
                who = r.choice(NAMES)
                q = base(it, "short-answer")
                q["prompt"] = f"{who} answered this problem incorrectly.\n{it['prompt']}\n{who}'s answer: {wrong}\nIdentify the mistake and give the correct answer."
                q["solutionSteps"] = [f"Mistake: {why[0].upper() + why[1:]}."] + it["steps"] + [f"The correct answer is {it['answer']}, not {wrong}."]
                tags[q["id"]] = ["error-analysis", "misconception"]
                checks[q["id"]] = dict(it["check"], bank=[course, unit], student=wrong)
                it["fam"] += "_error"
            else:
                parts = [make([f for f in fns if f.__name__ not in NO_WORKED], r, L, used) for _ in range(4)]
                q = OrderedDict(id=nid(), skillId=f"{unit}-skill-{sidx:02d}", level=lv, format="open-response", prompt="Answer each part. Show your work.",
                                parts=[OrderedDict(prompt=p["prompt"], answer=p["answer"]) for p in parts])
                q["answer"] = "; ".join(f"({'abcd'[i]}) {p['answer']}" for i, p in enumerate(parts))
                q["solutionSteps"] = [f"({'abcd'[i]}) " + " ".join(p["steps"]) for i, p in enumerate(parts)]
                tags[q["id"]] = ["multistep"]
                checks[q["id"]] = dict(bank=[course, unit], parts=[p["check"] for p in parts])
                it = dict(fam=parts[0]["fam"] + "_open")
            q["standards"] = stds
            q["sourceNotes"] = NOTE.format(fam=it["fam"])
            out.append(q)
    return out, tags


def main():
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    checks = json.load(open(CHECKS, encoding="utf-8")) if os.path.exists(CHECKS) else {}
    for (course, unit, name), (fns, stds) in SKILLS.items():
        if (course, unit) in NEW_UNITS:
            ensure_unit(course, unit, name)
        sidx, added = add_to_catalog(course, unit, name)
        bp = os.path.join(ROOT, "question-banks", course, unit + ".json")
        tp = os.path.join(ROOT, "question-banks", course, "meta", unit + ".tags.json")
        bank, raw = load_json(bp)
        tg, traw = load_json(tp)
        if any(q["skillId"] == f"{unit}-skill-{sidx:02d}" for q in bank["questions"]):
            print(f"skip {course}/{unit}: '{name}' already has questions (skill {sidx})")
            continue
        prefix = bank["questions"][0]["id"].rsplit("-s", 1)[0] if bank["questions"] else NEW_UNITS[(course, unit)][0]
        used = {q["prompt"] for q in bank["questions"]}
        r = random.Random(f"{course}/{unit}/{name}/20261114")
        items, tags = build_skill(course, unit, name, fns, stds, sidx, prefix, r, used, checks)
        bank["questions"].extend(items)
        tg.update(tags)
        dump_json(bp, bank, raw)
        dump_json(tp, tg, traw)
        print(f"{course}/{unit}: skill {sidx:02d} '{name}' + {len(items)} items")
    json.dump(checks, open(CHECKS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


main()
