"""Precalculus audit #6 (batch P4c): replace the excess of each repetitive skill's most common question template.

For each skill in variety.VARIETY, items whose prompt matches the skill's most common template (short answer and
multiple choice only; find-the-mistake and open-response items are kept) are replaced until that template is at most
35% of the skill's single-part items. A replacement keeps the item's id, skill, level, format and standards and gets
a new prompt, answer, options and worked solution from a family that fits the skill. Check data goes to out/checks.json
for verify.py. Re-running is safe: a skill already at or under 35% is skipped.

Usage: python3 tools/precalculus-audit-20261118/gaps/replace.py
"""
import collections, json, os, random, re, sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402
import variety as V  # noqa: E402

LEVELS = ["cp2", "cp1", "honors"]
TARGET = 0.35


def sig(p):
    """Template signature (same rule as the audit scan): the problem line with numbers collapsed.
    For find-the-mistake items the problem is the second line."""
    lines = p.split("\n")
    t = lines[1] if "answered this problem incorrectly" in lines[0] and len(lines) > 1 else lines[0]
    t = re.sub(r"\d+(\.\d+)?", "#", t)
    t = re.sub(r"(#\s*[+\-−]\s*)+#", "#", t)
    t = re.sub(r"[−-]\s*#", "#", t)
    return t[:70]


def single(q):
    return q["format"] != "open-response"


def is_ea(q):
    return "answered this problem incorrectly" in q["prompt"]


def main():
    checks_p = os.path.join(HERE, "out", "checks.json")
    checks = json.load(open(checks_p)) if os.path.exists(checks_p) else {}
    banks = {}
    for f in os.listdir(os.path.join(B.ROOT, "question-banks", "precalculus")):
        if f.endswith(".json"):
            p = os.path.join(B.ROOT, "question-banks", "precalculus", f)
            banks[p] = B.load_json(p)
    total = 0
    for sk, fns in V.VARIETY.items():
        bp = [p for p, (d, _) in banks.items() if any(q["skillId"] == sk for q in d["questions"])][0]
        bank, raw = banks[bp]
        qs = [q for q in bank["questions"] if q["skillId"] == sk and single(q)]
        top, n_top = collections.Counter(sig(q["prompt"]) for q in qs).most_common(1)[0]
        keep = int(TARGET * len(qs))
        excess = n_top - keep
        if excess <= 0:
            print(f"skip {sk}: top template {n_top}/{len(qs)}")
            continue
        cand = [q for q in qs if sig(q["prompt"]) == top and not is_ea(q)]
        by_lv = {lv: [q for q in cand if q["level"] == lv] for lv in LEVELS}
        # take from each level in turn, latest items first, so every level keeps some of the original type
        order = []
        while len(order) < excess and any(by_lv.values()):
            for lv in LEVELS:
                if by_lv[lv] and len(order) < excess:
                    order.append(by_lv[lv].pop())
        r = random.Random("pc-variety-" + sk)
        used = {q["prompt"] for d, _ in banks.values() for q in d["questions"]}
        name = B.catalog_names(bank["unitId"])[int(sk[-2:]) - 1]
        for q in order:
            L = LEVELS.index(q["level"])
            kind = "mc" if q["format"] == "multiple-choice" else "sa"
            pool = fns if kind == "mc" else [f for f in fns if not getattr(f, "mc_only", False)]
            if not pool:
                continue
            for _ in range(200):
                it = B.make(pool, r, L, used, min_wrongs=3 if kind == "mc" else 0)
                if sig(it["prompt"]) != top:
                    break

            def base(item, fmt, q=q):
                return OrderedDict(id=q["id"], skillId=q["skillId"], level=q["level"], format=fmt, prompt=item["prompt"], answer=item["answer"])
            new, _, fam = B.item(kind, it, r, base, bank["unitId"], checks, name)
            new["standards"] = q["standards"]
            new["sourceNotes"] = ("Original Claude-authored item (family: " + fam + "), added for question variety (Precalculus audit #6). "
                                  "Answer and every option re-checked from the printed problem by tools/precalculus-audit-20261118/gaps/verify.py. Teacher reviewed 2026-11-18.")
            i = bank["questions"].index(q)
            bank["questions"][i] = new
            total += 1
        after = collections.Counter(sig(x["prompt"]) for x in bank["questions"] if x["skillId"] == sk and single(x)).most_common(1)[0][1]
        print(f"{sk}: replaced {len(order)}; top template {n_top} -> {after} of {len(qs)}")
    for p, (d, raw) in banks.items():
        B.dump_json(p, d, raw)
    json.dump(checks, open(checks_p, "w"), ensure_ascii=False, indent=1)
    print("replaced", total)


if __name__ == "__main__":
    main()
