"""Materialise Grade 7 (prealgebra7) / Grade 6 (math6) banks from the authored families.

Usage: python3 gbuild.py <courseId> [unit-module ...]
Env: MG_REPO (repository root; default: two levels up), MG_OUT (output root).
Writes under MG_OUT:
  question-banks/<course>/<unit>.json, question-banks/<course>/meta/<unit>.tags.json,
  question-banks/assets/<course>/<unit>/<qid>.png, tools/middle-grades-authoring/out/<course>/<unit>.checks.json
Deterministic: each case is seeded from course/unit/skill/level/family/attempt.
Per skill and level: 7 short-answer + 6 multiple-choice + 3 extras (2 error analysis + 1 select-all / open response) = 16.
"""
import importlib, json, os, subprocess, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from glib import P, Reject, seed_rng, norm_key  # noqa
from lib import LEVELS, TAGS

REPO = os.environ.get("MG_REPO", os.path.abspath(os.path.join(HERE, "..", "..")))
OUT = os.environ.get("MG_OUT", "/home/claude/work/out")
COURSES = {
    "prealgebra7": dict(prefix="pa7", units=["g7_u01", "g7_u02", "g7_u03", "g7_u04", "g7_u05", "g7_u06", "g7_u07",
                                             "g7_u08", "g7_u09", "g7_u10", "g7_u11", "g7_u12", "g7_u13"]),
    "math6": dict(prefix="m6", units=["g6_u01", "g6_u02", "g6_u03", "g6_u04", "g6_u05", "g6_u06", "g6_u07"]),
}
TARGET = {"sa": 7, "mc": 6, "extra": 3}
NOTE = ("Original Claude-authored item (family: {fam}). Answer computed in the authoring script and re-checked by the "
        "independent verifier (tools/middle-grades-authoring/gverify.py). Awaiting human review.")
SEEN = {}
CAT_JS = r"""
const fs=require('fs'),vm=require('vm'),path=require('path');const root=process.argv[1],course=process.argv[2];
const ctx={window:{}};vm.runInNewContext(fs.readFileSync(path.join(root,'data.js'),'utf8'),ctx);
vm.runInNewContext(fs.readFileSync(path.join(root,'course-catalog.js'),'utf8'),ctx);
const c=ctx.window.LIBRARY.courses.find(c=>c.id===course);const out={};
for(const u of c.units)out[u.id]={name:u.name,skills:ctx.window.MK_COURSE_CATALOG.getSkillRecords(course,u.id)};
console.log(JSON.stringify(out));
"""
_cat = {}


def catalog(course):
    if course not in _cat:
        _cat[course] = json.loads(subprocess.run(["node", "-e", CAT_JS, REPO, course], capture_output=True, text=True, check=True).stdout)
    return _cat[course]


def pnorm(p):
    s = " ".join(str(p["prompt"]).lower().split())
    if p.get("parts"):
        s += "||" + "|".join(" ".join(str(x[0]).lower().split()) for x in p["parts"])
    if p.get("options") and p.get("parts") is None:
        s += "||" + "|".join(sorted(str(o[0]) for o in p["options"]))
    if p.get("diagram"):
        s += "||" + p["diagram"]["alt"].lower()
    return s


def nkey(p):
    import re
    s = pnorm(p)
    return (re.sub(r"\d+", "#", s), tuple(sorted(re.findall(r"\d+", s))), str(p.get("answer")))


NEAR = set()
VSEEN = {}


def vkey(q):
    """Same duplicate key as the verifier: prompt, diagram alt text, option texts, part prompts."""
    return " ".join(q["prompt"].lower().split()) + "|" + str(q.get("diagram", {}).get("spec", {}).get("alt", "")) + "|" + \
        "|".join(p["prompt"] for p in q.get("parts", [])) + "|" + "|".join(sorted(o["text"] for o in q.get("options", [])))


def build_mc(p, pos, r):
    if p.get("options"):
        return [{"text": t, "correct": bool(c)} for t, c in p["options"]]
    ck = norm_key(p["answer"])
    seen, ds = {ck}, []
    for w in p["wrong"]:
        k = norm_key(w)
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


SING = {"units": "unit", "feet": "foot", "inches": "inch", "meters": "meter", "miles": "mile", "cups": "cup", "hours": "hour", "blocks": "block", "visits": "visit",
        "points": "point", "years": "year", "days": "day", "pages": "page", "students": "student", "tickets": "ticket", "bags": "bag", "servings": "serving", "buses": "bus",
        "bottles": "bottle", "cells": "cell", "parts": "part", "gallons": "gallon", "centimeters": "centimeter", "kilometers": "kilometer", "liters": "liter", "grams": "gram",
        "kilograms": "kilogram", "milliliters": "milliliter", "millimeters": "millimeter", "pounds": "pound", "ounces": "ounce", "quarts": "quart", "pints": "pint", "yards": "yard"}
_SING_RE = __import__("re").compile(r"(?<![\d.,/])((?:-)?1) (" + "|".join(SING) + r")\b")


def fix_text(t):
    """Grammar: '1 units' -> '1 unit' (a whole-number 1 only)."""
    return _SING_RE.sub(lambda m: m.group(1) + " " + SING[m.group(2)], t) if isinstance(t, str) else t


def fix_q(q):
    q["prompt"] = fix_text(q["prompt"])
    if isinstance(q.get("answer"), str):
        q["answer"] = fix_text(q["answer"])
    elif isinstance(q.get("answer"), list):
        q["answer"] = [fix_text(a) for a in q["answer"]]
    for o in q.get("options", []) or []:
        o["text"] = fix_text(o["text"])
    for p in q.get("parts", []) or []:
        p["prompt"], p["answer"] = fix_text(p["prompt"]), fix_text(p["answer"])
    q["solutionSteps"] = [fix_text(s) for s in q["solutionSteps"]]
    return q


class Ctx:
    def __init__(self, course, unit):
        self.course, self.unit, self.prefix = course, unit, COURSES[course]["prefix"]


def emit(cx, rec, std, L, idx, p, fmt, fname, r, pos=None):
    lv = LEVELS[L]
    qid = f"{cx.prefix}-{cx.unit.ABBR}-s{rec['index']:02d}-{lv}-{idx:03d}"
    q = {"id": qid, "skillId": rec["id"], "level": lv, "format": fmt,
         "prompt": p["mc_prompt"] if fmt == "multiple-choice" and p.get("mc_prompt") else p["prompt"]}
    chk = {"q": p["chk"]}
    if fmt == "multiple-choice":
        q["answer"] = p["answer"]
        q["options"] = build_mc(p, pos, r)
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
        src = f"question-banks/assets/{cx.course}/{cx.unit.UNIT_ID}/{qid}.png"
        q["diagram"] = {"type": "image", "spec": {"src": src, "alt": p["diagram"]["alt"]}}
        p["diagram"]["path"] = os.path.join(OUT, src)
    q["standards"] = std
    q["sourceNotes"] = NOTE.format(fam=fname)
    tags = sorted({t for t in p["tags"] if t in TAGS} | ({"graph"} if p.get("diagram") and "graph" in p["tags"] else set()))
    chk["family"] = fname
    fix_q(q)
    if chk.get("parts") is None and isinstance(chk.get("q"), dict) and chk["q"].get("fn") == "claims":
        chk["q"]["table"] = {fix_text(k): v for k, v in chk["q"]["table"].items()}
    return q, tags, chk


def make_one(cx, f, sk, L, attempt):
    r = seed_rng(cx.course, cx.unit.UNIT_ID, sk, L, f.__name__, attempt)
    try:
        p = f(r, L)
    except (Reject, ZeroDivisionError):
        return None, r
    if p is None:
        return None, r
    return p, r


def build_skill(cx, rec, spec, L):
    fams = [f for f in spec["fams"] if L in f.levels]
    extras = [f for f in spec.get("extra", []) if L in f.levels]
    out, need = [], {"sa": TARGET["sa"], "mc": TARGET["mc"]}
    used, attempts, fails, dead = Counter(), Counter(), Counter(), set()
    famcount = defaultdict(Counter)
    pr = seed_rng("pos", cx.unit.UNIT_ID, rec["id"], L)
    positions = [0, 1, 2, 3] * 3
    pr.shuffle(positions)
    pi, idx = 0, 1

    def fail(fn):
        fails[fn] += 1
        if fails[fn] > 80:
            dead.add(fn)

    while need["sa"] + need["mc"] > 0:
        def ok_mode(f):
            m = f.mode or "any"
            return (m in ("any", "sa") and need["sa"] > 0) or (m in ("any", "mc") and need["mc"] > 0)
        cands = [f for f in fams if f.__name__ not in dead and ok_mode(f)]
        if not cands:
            raise RuntimeError(f"{rec['id']} L{L}: families exhausted, need {need}")
        f = min(cands, key=lambda g: (used[g.__name__], fams.index(g)))
        attempts[f.__name__] += 1
        p, r = make_one(cx, f, rec["id"], L, attempts[f.__name__])
        if p is None:
            fail(f.__name__)
            continue
        key = pnorm(p)
        if key in SEEN or nkey(p) in NEAR:
            fail(f.__name__)
            continue
        NEAR.add(nkey(p))
        m = p["mode"] if p["mode"] != "any" else (f.mode or "any")
        if m == "mc":
            fmt = "mc" if need["mc"] else None
        elif m == "sa":
            fmt = "sa" if need["sa"] else None
        else:
            fc = famcount[f.__name__]
            order = ["mc", "sa"] if (fc["multiple-choice"] < fc["short-answer"] or need["mc"] * 7 > need["sa"] * 6) else ["sa", "mc"]
            fmt = next((x for x in order if need[x] > 0), None)
        if fmt is None:
            fail(f.__name__)
            continue
        pos = positions[pi % len(positions)]
        if fmt == "mc":
            if p.get("options"):
                pos = [i for i, (t, c) in enumerate(p["options"]) if c][0]
            elif build_mc(p, pos, seed_rng("probe", key)) is None:
                if m == "any" and need["sa"] > 0:
                    fmt = "sa"
                else:
                    fail(f.__name__)
                    continue
        full = "multiple-choice" if fmt == "mc" else "short-answer"
        if fmt == "mc" and not p.get("options"):
            pi += 1
        q, tags, chk = emit(cx, rec, spec["std"], L, idx, p, full, f.__name__, r, pos if fmt == "mc" else None)
        if vkey(q) in VSEEN:
            fail(f.__name__)
            continue
        VSEEN[vkey(q)] = q["id"]
        SEEN[key] = q["id"]
        idx += 1
        need[fmt] -= 1
        used[f.__name__] += 1
        famcount[f.__name__][full] += 1
        out.append((q, tags, chk, p.get("diagram")))
    got, k, ea = 0, 0, Counter()
    while got < TARGET["extra"]:
        live = [f for f in extras if f.__name__ not in dead]
        if not live:
            raise RuntimeError(f"{rec['id']} L{L}: extras exhausted")
        errs = [g for g in live if g.__name__.endswith("_error")]
        rest = [g for g in live if not g.__name__.endswith("_error")]
        # slot 0 and 2: error analysis (the Error Analysis printable needs >= 2 per skill and level); slot 1: other formats
        pool_ = (errs or rest) if got != 1 else (rest or errs)
        f = pool_[(k // 2) % len(pool_)] if got != 1 else pool_[k % len(pool_)]
        k += 1
        ea[f.__name__] += 1
        p, r = make_one(cx, f, rec["id"], L, 1000 + ea[f.__name__])
        if p is None:
            fail(f.__name__)
            continue
        key = pnorm(p)
        if key in SEEN or nkey(p) in NEAR:
            fail(f.__name__)
            continue
        NEAR.add(nkey(p))
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
        if full == "multiple-choice" and p.get("options"):
            pos = [i for i, (t, c) in enumerate(p["options"]) if c][0]
        q, tags, chk = emit(cx, rec, spec["std"], L, idx, p, full, f.__name__, r, pos)
        if vkey(q) in VSEEN:
            fail(f.__name__)
            continue
        VSEEN[vkey(q)] = q["id"]
        SEEN[key] = q["id"]
        idx += 1
        got += 1
        out.append((q, tags, chk, p.get("diagram")))
    return out


def build_unit(course, modname, draw=True):
    unit = importlib.import_module(modname)
    cx = Ctx(course, unit)
    recs = catalog(course)[unit.UNIT_ID]["skills"]
    assert len(recs) == len(unit.SKILLS), (unit.UNIT_ID, len(recs), len(unit.SKILLS))
    questions, tags, checks, diagrams = [], {}, {}, []
    for rec in recs:
        spec = unit.SKILLS[rec["index"]]
        assert spec["name"] == rec["name"], (spec["name"], rec["name"])
        for L in range(3):
            for q, t, c, d in build_skill(cx, rec, spec, L):
                questions.append(q)
                tags[q["id"]] = t
                checks[q["id"]] = c
                if d:
                    diagrams.append(d)
    bank = {"schemaVersion": 1, "courseId": course, "unitId": unit.UNIT_ID, "questions": questions}
    bdir = os.path.join(OUT, "question-banks", course)
    os.makedirs(os.path.join(bdir, "meta"), exist_ok=True)
    json.dump(bank, open(os.path.join(bdir, unit.UNIT_ID + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(tags, open(os.path.join(bdir, "meta", unit.UNIT_ID + ".tags.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    cdir = os.path.join(OUT, "tools", "middle-grades-authoring", "out", course)
    os.makedirs(cdir, exist_ok=True)
    json.dump(checks, open(os.path.join(cdir, unit.UNIT_ID + ".checks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=str)
    if draw:
        adir = os.path.join(OUT, "question-banks", "assets", course, unit.UNIT_ID)
        if os.path.isdir(adir):
            for fn in os.listdir(adir):
                os.remove(os.path.join(adir, fn))
        for d in diagrams:
            d["draw"](d["path"])
    return unit.UNIT_ID, len(questions), len(diagrams)


if __name__ == "__main__":
    course = sys.argv[1]
    mods = sys.argv[2:] or COURSES[course]["units"]
    draw = os.environ.get("MG_NODRAW") != "1"
    # global duplicate detection: preload prompts of every built bank of BOTH grades not being rebuilt
    for c, cfg in COURSES.items():
        for m in cfg["units"]:
            if c == course and m in mods:
                continue
            if not os.path.exists(os.path.join(HERE, m + ".py")):
                continue
            uid = importlib.import_module(m).UNIT_ID
            f = os.path.join(OUT, "question-banks", c, uid + ".json")
            if os.path.exists(f):
                for q in json.load(open(f, encoding="utf-8"))["questions"]:
                    SEEN.setdefault(" ".join(q["prompt"].lower().split()), q["id"])
    # published Grade 8 banks in the repository are also off limits
    import glob
    for f in glob.glob(os.path.join(REPO, "question-banks", "prealgebra", "*.json")):
        for q in json.load(open(f, encoding="utf-8"))["questions"]:
            VSEEN.setdefault(vkey(q), q["id"])
    for c, cfg in COURSES.items():
        for m in cfg["units"]:
            if c == course and m in mods or not os.path.exists(os.path.join(HERE, m + ".py")):
                continue
            f = os.path.join(OUT, "question-banks", c, importlib.import_module(m).UNIT_ID + ".json")
            if os.path.exists(f):
                for q in json.load(open(f, encoding="utf-8"))["questions"]:
                    VSEEN.setdefault(vkey(q), q["id"])
    for m in mods:
        print(*build_unit(course, m, draw))
