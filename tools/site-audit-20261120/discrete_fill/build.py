"""Whole-site audit 2, item #6 (2026-11-20): bring every Discrete Math skill and level to at least 12 items.

For each thin skill/level, new items come from families.py: the skill's Support/Standard family for cp2 and cp1, and
its own Advanced family for honors. Prompts never repeat an existing prompt, multiple-choice keys are spread
evenly over positions A–D, and every item carries a family tag. Ids end -f## . Re-running is safe: cells already at
12 are skipped.

Usage: python3 tools/site-audit-20261120/discrete_fill/build.py
"""
import os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "discrete-audit-20261118"))
import families as F  # noqa: E402
from lib import load, save, items  # noqa: E402

TARGET = 12
CODE = {'speaking-mathematically': 'sm', 'compound-statements-logic': 'lg', 'number-theory-proof': 'np', 'sequences-induction-recursion': 'sq',
        'set-theory': 'st', 'properties-relations': 'rl', 'counting-probability': 'cn', 'graphs-trees': 'gr', 'election-theory': 'el', 'linear-programming': 'lp'}
NOTE = ("Original Claude-authored Discrete Math item (family: {}). Whole-site audit 2 (2026-11-20, tools/site-audit-20261120/discrete_fill): "
        "answer computed by brute force in the script.")


def main():
    B = load()
    prompts = {q["prompt"] for _, q in items(B)}
    ids = {q["id"] for _, q in items(B)}
    mc_pos = [0, 0, 0, 0]
    for _, q in items(B):
        if q["format"] == "multiple-choice" and len(q.get("options", [])) == 4:
            mc_pos[[o["correct"] for o in q["options"]].index(True)] += 1
    added = 0
    for skill, (base, adv) in F.FAMILIES.items():
        unit = skill.rsplit("-skill-", 1)[0]
        s = int(skill.rsplit("-", 1)[1])
        bank = B[unit]["questions"]
        strand = {q["standards"][0] for q in bank if q["skillId"] == skill and q.get("standards")}
        assert len(strand) == 1, (skill, strand)
        std = [*strand] + sorted({x for q in bank if q["skillId"] == skill for x in q.get("standards", [])} - strand)
        for lv in ("cp2", "cp1", "honors"):
            have = sum(1 for q in bank if q["skillId"] == skill and q["level"] == lv)
            fn = adv if lv == "honors" else base
            if have >= TARGET:
                continue
            assert fn, (skill, lv)
            r = random.Random(f"dm-fill-{skill}-{lv}")
            for _ in range(TARGET - have):
                for _try in range(4000):
                    try:
                        it = fn(r)
                    except F.Reject:
                        continue
                    if it["prompt"] in prompts or (it["fmt"] == "multiple-choice" and len(it["wrongs"]) < 3):
                        continue
                    break
                else:
                    raise SystemExit(f"no new item for {skill} {lv}")
                prompts.add(it["prompt"])
                k = 1
                while f"dm-{CODE[unit]}-s{s:02d}-{lv}-f{k:02d}" in ids:
                    k += 1
                qid = f"dm-{CODE[unit]}-s{s:02d}-{lv}-f{k:02d}"
                ids.add(qid)
                q = {"id": qid, "skillId": skill, "level": lv, "format": it["fmt"], "prompt": it["prompt"], "answer": it["answer"]}
                if it["fmt"] == "multiple-choice":
                    pos = mc_pos.index(min(mc_pos))
                    opts = [{"text": w, "correct": False} for w in it["wrongs"][:3]]
                    opts.insert(pos, {"text": it["answer"], "correct": True})
                    assert len({o["text"] for o in opts}) == 4, qid
                    mc_pos[pos] += 1
                    q["options"] = opts
                q["solutionSteps"] = it["steps"]
                q["sourceNotes"] = NOTE.format(it["fam"])
                q["standards"] = std
                bank.append(q)
                added += 1
    save(B)
    print(f"added {added} items; MC key positions {mc_pos}")


if __name__ == "__main__":
    main()
