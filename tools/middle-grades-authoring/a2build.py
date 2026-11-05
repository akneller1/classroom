"""Algebra 2 top-up: add questions to the existing Algebra 2 banks so every skill has at least 16 questions
at each level (CP2, CP1, Honors), including 2 error-analysis items per skill and level.

Existing questions are never changed or removed. New items continue each skill/level's numbering
(a2-<abbr>-sNN-<level>-NNN) and carry the same "(family: ...)" source note as the other generated banks.

Usage (from the repository root):
  MG_OUT=<scratch> python3 tools/middle-grades-authoring/a2build.py [a2_u01 ...]   # writes new-only banks + checks to MG_OUT
  MG_OUT=<scratch> python3 tools/middle-grades-authoring/a2verify.py               # independent verification, must print TOTAL ERRORS 0
  MG_OUT=<scratch> python3 tools/middle-grades-authoring/a2build.py --merge         # appends the verified items to question-banks/algebra2
"""
import glob, importlib, json, math, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gbuild as G
import gchecks, hschecks, a2checks  # noqa: F401  checks used when screening error-analysis answers
from gbuild import make_one, pnorm, nkey, vkey, build_mc, emit, Ctx, seed_rng

G.SING.update({"weeks": "week", "months": "month", "minutes": "minute", "seconds": "second", "dollars": "dollar", "items": "item"})
G._SING_RE = re.compile(r"(?<![\d.,/])((?:-)?1) (" + "|".join(G.SING) + r")\b")
_fix0 = G.fix_text


def _fix(t):
    t = _fix0(t)
    if isinstance(t, str):
        t = re.sub(r"\b(How (?:tall|far|high|long|wide|much|many)[^.?\n]*?) (Round to)", r"\1? \2", t)
        t = re.sub(r"(sin|cos|tan)\(\((x [+-] [^()]+)\)\)", r"\1(\2)", t)
    return t


G.fix_text = _fix
G.COURSES["algebra2"] = dict(prefix="a2", units=[f"a2_u{i:02d}" for i in range(1, 12)])
COURSE = "algebra2"
REPO, OUT = G.REPO, G.OUT
MIN_PER_LEVEL, N_ERR = 16, 2
LV = {0: "cp2", 1: "cp1", 2: "honors"}


def existing(uid):
    return json.load(open(os.path.join(REPO, "question-banks", COURSE, uid + ".json"), encoding="utf-8"))


def plan(have):
    """How many of each kind to add to a skill/level that already has `have` questions."""
    deficit = max(0, MIN_PER_LEVEL - have)
    other = 1 if deficit >= 8 else 0
    core = max(0, deficit - N_ERR - other)
    sa = math.ceil(core * 7 / 13)
    return {"sa": sa, "mc": core - sa, "err": N_ERR, "other": other}


def build_skill(cx, rec, spec, L, want, start):
    fams = [f for f in spec["fams"] if L in f.levels]
    extras = [f for f in spec.get("extra", []) if L in f.levels]
    errs_f = [f for f in extras if f.__name__.endswith("_error")]
    rest_f = [f for f in extras if not f.__name__.endswith("_error")]
    out, need = [], {"sa": want["sa"], "mc": want["mc"]}
    used, attempts, fails, dead = Counter(), Counter(), Counter(), set()
    famcount = defaultdict(Counter)
    pr = seed_rng("pos", cx.unit.UNIT_ID, rec["id"], L)
    positions = [0, 1, 2, 3] * 4
    pr.shuffle(positions)
    st = {"pi": 0, "idx": start}

    def fail(fn):
        fails[fn] += 1
        if fails[fn] > 120:
            dead.add(fn)

    def accept(p, full, f, r, pos):
        q, tags, chk = emit(cx, rec, spec["std"], L, st["idx"], p, full, f.__name__, r, pos)
        if vkey(q) in G.VSEEN:
            return False
        G.VSEEN[vkey(q)] = q["id"]
        G.SEEN[pnorm(p)] = q["id"]
        st["idx"] += 1
        out.append((q, tags, chk, p.get("diagram")))
        return True

    while need["sa"] + need["mc"] > 0:
        def ok_mode(f):
            m = f.mode or "any"
            return (m in ("any", "sa") and need["sa"] > 0) or (m in ("any", "mc") and need["mc"] > 0)
        cands = [f for f in fams if f.__name__ not in dead and ok_mode(f)]
        if not cands and need["mc"] and not need["sa"]:
            need["sa"], need["mc"] = need["mc"], 0      # no unused multiple-choice item left: use short answer instead
            continue
        if not cands and need["sa"] and not need["mc"] and any(f.__name__ not in dead and (f.mode or "any") in ("any", "mc") for f in fams):
            need["mc"], need["sa"] = need["sa"], 0
            continue
        if not cands:
            raise RuntimeError(f"{rec['id']} L{L}: families exhausted, need {need}")
        f = min(cands, key=lambda g: (used[g.__name__], fams.index(g)))
        attempts[f.__name__] += 1
        p, r = make_one(cx, f, rec["id"] + "+a2", L, attempts[f.__name__])
        if p is None:
            fail(f.__name__)
            continue
        key = pnorm(p)
        if key in G.SEEN or nkey(p) in G.NEAR:
            fail(f.__name__)
            continue
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
        pos = positions[st["pi"] % len(positions)]
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
            st["pi"] += 1
        if not accept(p, full, f, r, pos if fmt == "mc" else None):
            fail(f.__name__)
            continue
        G.NEAR.add(nkey(p))
        need[fmt] -= 1
        used[f.__name__] += 1
        famcount[f.__name__][full] += 1

    def extra_loop(pool, count, tag):
        got, k, ea = 0, 0, Counter()
        while got < count:
            live = [f for f in pool if f.__name__ not in dead]
            if not live:
                raise RuntimeError(f"{rec['id']} L{L}: {tag} families exhausted")
            f = live[k % len(live)]
            k += 1
            ea[f.__name__] += 1
            p, r = make_one(cx, f, rec["id"] + "+a2", L, 1000 + ea[f.__name__])
            if p is None:
                fail(f.__name__)
                continue
            key = pnorm(p)
            if key in G.SEEN or nkey(p) in G.NEAR:
                fail(f.__name__)
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
            pos = positions[st["pi"] % len(positions)]
            if full == "multiple-choice" and not p.get("options"):
                if build_mc(p, pos, seed_rng("probe", key)) is None:
                    full = "short-answer"
                else:
                    st["pi"] += 1
            if full == "multiple-choice" and p.get("options"):
                pos = [i for i, (t, c) in enumerate(p["options"]) if c][0]
            if not accept(p, full, f, r, pos):
                fail(f.__name__)
                continue
            G.NEAR.add(nkey(p))
            got += 1
    extra_loop(errs_f, want["err"], "error")
    if want["other"]:
        extra_loop(rest_f or errs_f, want["other"], "other")
    return out


def build_unit(modname, draw=True):
    unit = importlib.import_module(modname)
    cx = Ctx(COURSE, unit)
    recs = G.catalog(COURSE)[unit.UNIT_ID]["skills"]
    assert len(recs) == len(unit.SKILLS), (unit.UNIT_ID, len(recs), len(unit.SKILLS))
    old = existing(unit.UNIT_ID)["questions"]
    have, top = Counter(), Counter()
    std = {}
    for q in old:
        have[(q["skillId"], q["level"])] += 1
        m = re.search(r"-(\d+)$", q["id"])
        top[(q["skillId"], q["level"])] = max(top[(q["skillId"], q["level"])], int(m.group(1)))
        std.setdefault(q["skillId"], q["standards"])
        assert q["id"].split("-")[1] == unit.ABBR, (q["id"], unit.ABBR)
    questions, tags, checks, diagrams = [], {}, {}, []
    for rec in recs:
        spec = dict(unit.SKILLS[rec["index"]])
        assert spec["name"] == rec["name"], (spec["name"], rec["name"])
        spec["std"] = std.get(rec["id"], spec.get("std"))
        for L in range(3):
            lv = LV[L]
            for q, t, c, d in build_skill(cx, rec, spec, L, plan(have[(rec["id"], lv)]), top[(rec["id"], lv)] + 1):
                questions.append(q)
                tags[q["id"]] = t
                checks[q["id"]] = c
                if d:
                    diagrams.append(d)
    bank = {"schemaVersion": 1, "courseId": COURSE, "unitId": unit.UNIT_ID, "questions": questions}
    bdir = os.path.join(OUT, "question-banks", COURSE)
    os.makedirs(os.path.join(bdir, "meta"), exist_ok=True)
    json.dump(bank, open(os.path.join(bdir, unit.UNIT_ID + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(tags, open(os.path.join(bdir, "meta", unit.UNIT_ID + ".tags.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    cdir = os.path.join(OUT, "tools", "middle-grades-authoring", "out", COURSE)
    os.makedirs(cdir, exist_ok=True)
    json.dump(checks, open(os.path.join(cdir, unit.UNIT_ID + ".checks.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0, default=str)
    if draw:
        adir = os.path.join(OUT, "question-banks", "assets", COURSE, unit.UNIT_ID)
        os.makedirs(adir, exist_ok=True)
        for d in diagrams:
            d["draw"](d["path"])
    return unit.UNIT_ID, len(questions), len(diagrams)


def preload(skip_units):
    """Existing Algebra 2 questions and every other generated course bank are off limits for duplicates."""
    for f in glob.glob(os.path.join(REPO, "question-banks", "*", "*.json")):
        for q in json.load(open(f, encoding="utf-8"))["questions"]:
            G.VSEEN.setdefault(vkey(q), q["id"])
            G.SEEN.setdefault(" ".join(q["prompt"].lower().split()), q["id"])
    for f in glob.glob(os.path.join(OUT, "question-banks", COURSE, "*.json")):
        uid = os.path.basename(f)[:-5]
        if uid in skip_units:
            continue
        for q in json.load(open(f, encoding="utf-8"))["questions"]:
            G.VSEEN.setdefault(vkey(q), q["id"])
            G.SEEN.setdefault(" ".join(q["prompt"].lower().split()), q["id"])


def merge():
    for f in sorted(glob.glob(os.path.join(OUT, "question-banks", COURSE, "*.json"))):
        uid = os.path.basename(f)[:-5]
        new = json.load(open(f, encoding="utf-8"))["questions"]
        newtags = json.load(open(os.path.join(OUT, "question-banks", COURSE, "meta", uid + ".tags.json"), encoding="utf-8"))
        bp = os.path.join(REPO, "question-banks", COURSE, uid + ".json")
        tp = os.path.join(REPO, "question-banks", COURSE, "meta", uid + ".tags.json")
        bank, tags = json.load(open(bp, encoding="utf-8")), json.load(open(tp, encoding="utf-8"))
        ids = {q["id"] for q in bank["questions"]}
        add = [q for q in new if q["id"] not in ids]
        bank["questions"] += add
        for q in add:
            tags[q["id"]] = newtags.get(q["id"], [])
        json.dump(bank, open(bp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        json.dump(tags, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        src = os.path.join(OUT, "question-banks", "assets", COURSE, uid)
        if os.path.isdir(src):
            dst = os.path.join(REPO, "question-banks", "assets", COURSE, uid)
            os.makedirs(dst, exist_ok=True)
            for fn in os.listdir(src):
                if any(fn.startswith(q["id"]) for q in add):
                    with open(os.path.join(src, fn), "rb") as a, open(os.path.join(dst, fn), "wb") as b:
                        b.write(a.read())
        print(uid, "added", len(add), "total", len(bank["questions"]))


if __name__ == "__main__":
    if sys.argv[1:] == ["--merge"]:
        merge()
        sys.exit(0)
    mods = sys.argv[1:] or G.COURSES[COURSE]["units"]
    preload({importlib.import_module(m).UNIT_ID for m in mods})
    for m in mods:
        print(*build_unit(m, os.environ.get("MG_NODRAW") != "1"), flush=True)
