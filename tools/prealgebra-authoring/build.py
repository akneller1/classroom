"""Materialise the Grade 8 Pre-Algebra banks from the authored families.

Usage: python3 build.py [unit-module ...]      (default: all seven units)
Writes (under $PA8_OUT, default /home/claude/work/pkg):
  question-banks/prealgebra/<unit>.json
  question-banks/prealgebra/meta/<unit>.tags.json
  question-banks/assets/prealgebra/<unit>/<qid>.png
  tools/prealgebra-authoring/out/<unit>.checks.json   (verification specs, read by verify.py)
Deterministic: every random case is seeded from unit/skill/level/family/attempt.
"""
import importlib, json, os, sys, traceback
from collections import Counter, defaultdict
from lib import P, Reject, LEVELS, TAGS, ROOT, COURSE, seed_rng, norm_key

UNITS = ["u1_real_numbers", "u2_equations", "u3_functions", "u4_systems", "u5_bivariate",
         "u6_transformations", "u7_geometry"]
TARGET = {"sa": 10, "mc": 8, "extra": 2}
NOTE = ("Original Claude-authored item (family: {fam}). Answer computed in the authoring script and "
        "re-checked by the independent verifier (tools/prealgebra-authoring/verify.py). Awaiting human review.")
SEEN_PROMPTS = {}


def pnorm(p):
    s = " ".join(str(p["prompt"]).lower().split())
    if p.get("parts"):
        s += "||" + "|".join(" ".join(str(x[0]).lower().split()) for x in p["parts"])
    if p.get("options") and p.get("parts") is None:
        s += "||" + "|".join(sorted(str(o[0]) for o in p["options"]))
    if p.get("diagram"):
        s += "||" + p["diagram"]["alt"].lower()
    return s


def build_mc(p, pos, r):
    """4 options: correct + 3 distinct misconception distractors. Returns options or None."""
    if p.get("options"):
        return [{"text": t, "correct": bool(c)} for t, c in p["options"]]
    keyf = p.get("eq_key") or norm_key
    ck = keyf(p["answer"])
    seen = {ck}
    ds = []
    for w in p["wrong"]:
        k = keyf(w)
        if k in seen or not str(w).strip():
            continue
        seen.add(k)
        ds.append(str(w))
    if len(ds) < 3:
        return None
    ds = ds[:3]
    r.shuffle(ds)
    ds.insert(pos, p["answer"])
    return [{"text": t, "correct": i == pos} for i, t in enumerate(ds)]


def emit(unit, skill_rec, std, L, idx, p, fmt, fname, r, pos=None):
    lv = LEVELS[L]
    qid = f"pa8-{unit.ABBR}-s{skill_rec['index']:02d}-{lv}-{idx:03d}"
    q = {"id": qid, "skillId": skill_rec["id"], "level": lv, "format": fmt,
         "prompt": p["mc_prompt"] if fmt == "multiple-choice" and p.get("mc_prompt") else p["prompt"]}
    chk = {"q": p["chk"]}
    if fmt == "multiple-choice":
        opts = build_mc(p, pos, r)
        q["answer"] = p["answer"]
        q["options"] = opts
    elif fmt == "select-all":
        opts = list(p["options"])
        r.shuffle(opts)
        q["options"] = [{"text": t, "correct": bool(c)} for t, c in opts]
        q["answer"] = [t for t, c in opts if c]
    elif fmt == "open-response":
        q["parts"] = [{"prompt": a, "answer": b} for a, b, _ in p["parts"]]
        q["answer"] = "; ".join(f"({chr(97 + i)}) {b}" for i, (a, b, _) in enumerate(p["parts"]))
        chk["parts"] = [c for _, _, c in p["parts"]]
    else:
        q["answer"] = p["answer"]
    q["solutionSteps"] = p["steps"]
    if p.get("diagram"):
        src = f"question-banks/assets/{COURSE}/{unit.UNIT_ID}/{qid}.png"
        q["diagram"] = {"type": "image", "spec": {"src": src, "alt": p["diagram"]["alt"]}}
        p["diagram"]["path"] = os.path.join(ROOT, src)
    q["standards"] = std
    q["sourceNotes"] = NOTE.format(fam=fname)
    tags = sorted({t for t in p["tags"] if t in TAGS} | ({"graph"} if p.get("diagram") and "graph" in p["tags"] else set()))
    chk["family"] = fname
    return q, tags, chk


def make_one(f, unit, sk, L, attempt):
    r = seed_rng(unit.UNIT_ID, sk, L, f.__name__, attempt)
    try:
        p = f(r, L)
    except Reject:
        return None, r
    return p, r


def build_skill(unit, rec, spec, L, log):
    """Return list of (question, tags, chk, diagram) for one skill and level."""
    fams = [f for f in spec["fams"] if L in f.levels]
    extras = [f for f in spec.get("extra", []) if L in f.levels]
    out = []
    need = {"sa": TARGET["sa"], "mc": TARGET["mc"]}
    used = Counter()
    attempts = Counter()
    fails = Counter()
    dead = set()
    pr = seed_rng("pos", unit.UNIT_ID, rec["id"], L)
    positions = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    pr.shuffle(positions)
    pi = 0
    idx = 1
    famcount = defaultdict(Counter)
    while need["sa"] + need["mc"] > 0:
        live = [f for f in fams if f.__name__ not in dead]
        if not live:
            raise RuntimeError(f"{rec['id']} L{L}: families exhausted, need {need}")
        # family whose current usage is lowest and that can still fill a needed format
        def ok_mode(f):
            m = f.mode or "any"
            return (m in ("any", "sa") and need["sa"] > 0) or (m in ("any", "mc") and need["mc"] > 0)
        cands = [f for f in live if ok_mode(f)]
        if not cands:
            raise RuntimeError(f"{rec['id']} L{L}: no family can fill {need}")
        f = min(cands, key=lambda g: (used[g.__name__], fams.index(g)))
        attempts[f.__name__] += 1
        p, r = make_one(f, unit, rec["id"], L, attempts[f.__name__])
        if p is None:
            fails[f.__name__] += 1
            if fails[f.__name__] > 60:
                dead.add(f.__name__)
            continue
        key = pnorm(p)
        if key in SEEN_PROMPTS:
            fails[f.__name__] += 1
            if fails[f.__name__] > 60:
                dead.add(f.__name__)
            continue
        m = p["mode"] if p["mode"] != "any" else (f.mode or "any")
        # format choice: balance within family, honour remaining needs
        if m == "mc":
            fmt = "mc" if need["mc"] else None
        elif m == "sa":
            fmt = "sa" if need["sa"] else None
        else:
            fc = famcount[f.__name__]
            order = ["mc", "sa"] if (fc["multiple-choice"] < fc["short-answer"] or need["mc"] * 10 > need["sa"] * 8) else ["sa", "mc"]
            fmt = next((x for x in order if need[x] > 0), None)
        if fmt is None:
            fails[f.__name__] += 1
            if fails[f.__name__] > 60:
                dead.add(f.__name__)
            continue
        if fmt == "mc":
            pos = positions[pi % len(positions)]
            if p.get("options"):
                pos = [i for i, (t, c) in enumerate(p["options"]) if c][0]
            if not p.get("options") and build_mc(p, pos, seed_rng("probe", key)) is None:
                if m == "any" and need["sa"] > 0:
                    fmt = "sa"
                else:
                    fails[f.__name__] += 1
                    if fails[f.__name__] > 60:
                        dead.add(f.__name__)
                    continue
        full = "multiple-choice" if fmt == "mc" else "short-answer"
        if fmt == "mc" and not p.get("options"):
            pi += 1
        q, tags, chk = emit(unit, rec, spec["std"], L, idx, p, full, f.__name__, r, pos if fmt == "mc" else None)
        SEEN_PROMPTS[key] = q["id"]
        idx += 1
        need[fmt] -= 1
        used[f.__name__] += 1
        famcount[f.__name__][full] += 1
        out.append((q, tags, chk, p.get("diagram")))
    # extras: select-all / open-response / error-analysis
    got = 0
    ea = Counter()
    k = 0
    while got < TARGET["extra"]:
        live = [f for f in extras if f.__name__ not in dead]
        if not live:
            raise RuntimeError(f"{rec['id']} L{L}: extras exhausted")
        f = live[k % len(live)]
        k += 1
        ea[f.__name__] += 1
        p, r = make_one(f, unit, rec["id"], L, 1000 + ea[f.__name__])
        if p is None:
            fails[f.__name__] += 1
            if fails[f.__name__] > 60:
                dead.add(f.__name__)
            continue
        key = pnorm(p)
        if key in SEEN_PROMPTS:
            fails[f.__name__] += 1
            if fails[f.__name__] > 60:
                dead.add(f.__name__)
            continue
        if p.get("parts"):
            full = "open-response"
        elif p.get("options") and sum(1 for _, c in p["options"] if c) >= 2:
            full = "select-all"
        elif p.get("options"):
            full = "multiple-choice"
        elif p["wrong"] and p["mode"] != "sa":
            full = "multiple-choice"
        else:
            full = "short-answer"
        pos = positions[pi % len(positions)]
        if full == "multiple-choice" and not p.get("options"):
            if build_mc(p, pos, seed_rng("probe", key)) is None:
                full = "short-answer"
            else:
                pi += 1
        q, tags, chk = emit(unit, rec, spec["std"], L, idx, p, full, f.__name__, r, pos)
        SEEN_PROMPTS[key] = q["id"]
        idx += 1
        got += 1
        out.append((q, tags, chk, p.get("diagram")))
    return out


def build_unit(modname, draw=True):
    unit = importlib.import_module(modname)
    import vm_catalog
    recs = vm_catalog.records(COURSE, unit.UNIT_ID)
    assert len(recs) == len(unit.SKILLS), (unit.UNIT_ID, len(recs), len(unit.SKILLS))
    questions, tags, checks, diagrams = [], {}, {}, []
    log = []
    for rec in recs:
        spec = unit.SKILLS[rec["index"]]
        assert spec["name"] == rec["name"], (spec["name"], rec["name"])
        for L in range(3):
            for q, t, c, d in build_skill(unit, rec, spec, L, log):
                questions.append(q)
                tags[q["id"]] = t
                checks[q["id"]] = c
                if d:
                    diagrams.append(d)
    bank = {"schemaVersion": 1, "courseId": COURSE, "unitId": unit.UNIT_ID, "questions": questions}
    bdir = os.path.join(ROOT, "question-banks", COURSE)
    os.makedirs(os.path.join(bdir, "meta"), exist_ok=True)
    with open(os.path.join(bdir, unit.UNIT_ID + ".json"), "w", encoding="utf-8") as fh:
        json.dump(bank, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(bdir, "meta", unit.UNIT_ID + ".tags.json"), "w", encoding="utf-8") as fh:
        json.dump(tags, fh, ensure_ascii=False, indent=0)
    cdir = os.path.join(ROOT, "tools", "prealgebra-authoring", "out")
    os.makedirs(cdir, exist_ok=True)
    with open(os.path.join(cdir, unit.UNIT_ID + ".checks.json"), "w", encoding="utf-8") as fh:
        json.dump(checks, fh, ensure_ascii=False, indent=0, default=lambda o: str(o))
    if draw:
        adir = os.path.join(ROOT, "question-banks", "assets", COURSE, unit.UNIT_ID)
        if os.path.isdir(adir):
            for fn in os.listdir(adir):
                os.remove(os.path.join(adir, fn))
        for d in diagrams:
            d["draw"](d["path"])
    return unit.UNIT_ID, len(questions), len(diagrams)


if __name__ == "__main__":
    mods = sys.argv[1:] or UNITS
    # duplicate detection is global across units: load prompts of units not being rebuilt
    for m in UNITS:
        if m in mods:
            continue
        u = importlib.import_module(m) if os.path.exists(m + ".py") else None
        if u is None:
            continue
        f = os.path.join(ROOT, "question-banks", COURSE, u.UNIT_ID + ".json")
        if os.path.exists(f):
            for q in json.load(open(f, encoding="utf-8"))["questions"]:
                pk = " ".join(q["prompt"].lower().split())
                SEEN_PROMPTS.setdefault(pk, q["id"])
    for m in mods:
        print(*build_unit(m))
