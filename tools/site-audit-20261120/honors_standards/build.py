"""Whole-site audit 2, item #7 (2026-11-20): add practice for honors-only standards with no items.

Adds 12 items per standard (per level: short answer, multiple choice, short answer, multiple choice) to the most
closely related existing skill in the Precalculus and Algebra 2 banks. Ids end -x### / -y###. Check data for
verify.py goes to out/checks.json. Re-running is safe: a skill that already has items with the id tag is skipped.

Usage: python3 tools/site-audit-20261120/honors_standards/build.py
"""
import json, os, random, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import families as FAM  # noqa: E402

LEVELS = ["cp2", "cp1", "honors"]
PLAN = ["sa", "mc", "sa", "mc"]
NOTE = ("Original Claude-authored item (family: {fam}). Answer and every option re-checked from the printed problem by "
        "tools/site-audit-20261120/honors_standards/verify.py.")
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


def make(fn, r, L, used, min_wrongs):
    for _ in range(5000):
        try:
            it = fn(r, L)
        except FAM.Reject:
            continue
        if it["prompt"] in used or len(it["wrongs"]) < min_wrongs:
            continue
        used.add(it["prompt"])
        return it
    raise SystemExit(f"could not make a new {fn.__name__} item at level {L}")


def main():
    os.makedirs(os.path.dirname(CHECKS), exist_ok=True)
    checks = json.load(open(CHECKS)) if os.path.exists(CHECKS) else {}
    for course, unit, sidx, prefix, tag, stds, fn in FAM.PLAN:
        bp = os.path.join(ROOT, "question-banks", course, unit + ".json")
        bank, raw = load_json(bp)
        sid = f"{unit}-skill-{sidx:02d}"
        pat = f"{prefix}-s{sidx:02d}-"
        if any(q["id"].startswith(pat) and q["id"][-4] == tag for q in bank["questions"]):
            print(f"skip {course} {sid} {tag}")
            continue
        r = random.Random(f"site-audit2-{course}-{sid}-{tag}")
        used = {q["prompt"] for q in bank["questions"]}
        qs, tags = [], OrderedDict()
        for L, lv in enumerate(LEVELS):
            for n, kind in enumerate(PLAN, 1):
                it = make(fn, r, L, used, 3 if kind == "mc" else 1)
                q = OrderedDict(id=f"{pat}{lv}-{tag}{n:03d}", skillId=sid, level=lv, format="multiple-choice" if kind == "mc" else "short-answer",
                                prompt=it["prompt"], answer=it["answer"])
                if kind == "mc":
                    opts = [OrderedDict(text=it["answer"], correct=True)] + [OrderedDict(text=t, correct=False) for t, _ in it["wrongs"][:3]]
                    r.shuffle(opts)
                    q["options"] = opts
                q["solutionSteps"] = it["steps"]
                q["standards"] = stds
                q["sourceNotes"] = NOTE.format(fam=it["fam"])
                checks[q["id"]] = dict(it["check"], course=course)
                tags[q["id"]] = []
                qs.append(q)
        assert not {q["id"] for q in bank["questions"]} & {q["id"] for q in qs}
        bank["questions"].extend(qs)
        dump_json(bp, bank, raw)
        tp = os.path.join(ROOT, "question-banks", course, "meta", unit + ".tags.json")
        if os.path.exists(tp):
            tg, traw = load_json(tp)
            tg.update(tags)
            dump_json(tp, tg, traw)
        print(f"{course} {sid} {stds[0]}: + {len(qs)} items")
    json.dump(checks, open(CHECKS, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
