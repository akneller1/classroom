"""Shared authoring helpers for the Statistics bank expansion.

Each new question is appended through `Q(...)`. Computed questions also record a
`check` spec in a sidecar (scripts/verification/checks.json) so that the
independent verifier can recompute the key from the numbers printed in the
prompt. The sidecar is NOT part of the bank schema and is never shipped inside
the banks.
"""
import math
import random
from collections import defaultdict

UNITS = ["exploring-data", "sampling-experimentation", "anticipating-patterns", "statistical-inference"]
UNUM = {u: i + 1 for i, u in enumerate(UNITS)}
ITEMS = defaultdict(list)     # unit -> list of question dicts
CHECKS = {}                   # id -> check spec
_counter = defaultdict(int)

NOTE = ("Original Claude-authored item (family: {fam}). {how} Awaiting human review.")
HOW_COMPUTED = "Answer computed in the authoring script and re-checked from the printed numbers by the independent verifier (scripts/verification/verify_expansion.py)."
HOW_CONCEPT = "Conceptual key and distractors reviewed by hand against standard AP Statistics usage."


def skill(unit, k):
    return f"{unit}-skill-{k:02d}"


def nid(unit, k, level):
    key = (unit, k, level)
    _counter[key] += 1
    return f"stat-u{UNUM[unit]}-s{k:02d}-{level}-x{_counter[key]:02d}"


def fmt(x, d=None):
    if d is not None:
        s = f"{x:.{d}f}"
    else:
        s = f"{x:.6f}".rstrip("0").rstrip(".")
    if s in ("-0", "-0.0", "-0.00", "-0.000", "-0.0000"):
        s = s[1:]
    return s


def lst(v):
    return ", ".join(fmt(x) for x in v)


def _rng(tag):
    return random.Random("stat-expansion::" + tag)


def Q(unit, k, level, fmt_, prompt, answer, steps, *, family, std, options=None, parts=None,
      check=None, diagram=None, concept=None, note=None):
    qid = nid(unit, k, level)
    computed = check is not None
    q = {
        "id": qid,
        "skillId": skill(unit, k),
        "level": level,
        "format": fmt_,
        "prompt": prompt,
        "answer": answer,
        "solutionSteps": steps,
    }
    if options is not None:
        q["options"] = options
    if parts is not None:
        q["parts"] = parts
    if diagram is not None:
        q["diagram"] = diagram
    q["standards"] = std
    q["sourceNotes"] = NOTE.format(fam=family, how=HOW_COMPUTED if computed else HOW_CONCEPT) + (" " + note if note else "")
    ITEMS[unit].append(q)
    if check is not None:
        CHECKS[qid] = check
    return q


def mc_opts(correct, wrongs, tag):
    seen = {correct.strip().casefold()}
    ws = []
    for w in wrongs:
        k = w.strip().casefold()
        if k in seen:
            continue
        seen.add(k)
        ws.append(w)
    assert len(ws) >= 3, (correct, wrongs)
    opts = [{"text": correct, "correct": True}] + [{"text": w, "correct": False} for w in ws[:3]]
    _rng(tag).shuffle(opts)
    return opts


def MC(unit, k, level, prompt, correct, wrongs, steps, *, family, std, check=None, diagram=None):
    return Q(unit, k, level, "multiple-choice", prompt, correct, steps, family=family, std=std,
             options=mc_opts(correct, wrongs, prompt + family), check=check, diagram=diagram)


def num_mc(unit, k, level, prompt, value, wrong_values, d, steps, *, family, std, check, unit_txt="",
           diagram=None, bounds=None):
    """Numeric multiple choice: distractors must round to different text and stay in bounds."""
    f = lambda v: fmt(v, d) + unit_txt
    key = f(value)
    wr = []
    for w in wrong_values:
        if w is None or (isinstance(w, float) and (math.isnan(w) or math.isinf(w))):
            continue
        if bounds and not (bounds[0] <= w <= bounds[1]):
            continue
        if abs(w - value) < 1.5 * 10 ** (-d):
            continue
        t = f(w)
        if t != key and t not in wr:
            wr.append(t)
    j = 1
    while len(wr) < 3:
        for w in (value * (1 + 0.1 * j), value * (1 - 0.1 * j) if value != 0 else -0.1 * j, value + j * 10 ** (1 - d)):
            if bounds and not (bounds[0] <= w <= bounds[1]):
                continue
            t = f(w)
            if t != key and t not in wr and abs(w - value) >= 1.5 * 10 ** (-d):
                wr.append(t)
                break
        j += 1
    return MC(unit, k, level, prompt, key, wr[:3], steps, family=family, std=std, check=check, diagram=diagram)


def SA(unit, k, level, prompt, answer, steps, *, family, std, check=None, diagram=None, note=None):
    return Q(unit, k, level, "short-answer", prompt, answer, steps, family=family, std=std, check=check, diagram=diagram, note=note)


def SEL(unit, k, level, prompt, corrects, wrongs, steps, *, family, std, check=None):
    assert len(corrects) >= 2 and len(wrongs) >= 2
    opts = [{"text": c, "correct": True} for c in corrects] + [{"text": w, "correct": False} for w in wrongs]
    _rng(prompt + family).shuffle(opts)
    assert len({o["text"].casefold() for o in opts}) == len(opts)
    ans = [o["text"] for o in opts if o["correct"]]
    return Q(unit, k, level, "select-all", prompt, ans, steps, family=family, std=std, options=opts, check=check)


def OR(unit, k, level, prompt, parts, guide, *, family, std, check=None, diagram=None):
    """Open response: parts = [(prompt, answer), ...] (>= 4); guide = list of scoring lines."""
    assert len(parts) >= 4
    ps = [{"prompt": p, "answer": a} for p, a in parts]
    ans = "; ".join(f"({chr(97 + i)}) {a}" for i, (_, a) in enumerate(parts))
    steps = [f"({chr(97 + i)}) {a}" for i, (_, a) in enumerate(parts)] + ["Scoring guide (4 points):"] + guide
    return Q(unit, k, level, "open-response", prompt, ans, steps, family=family, std=std, parts=ps,
             check=check, diagram=diagram)


# --------------------------- numerical helpers (authoring side) ---------------------------
import numpy as np
from scipy import stats as st


def median(v):
    return float(np.median(v))


def quartiles(v):
    s = sorted(v)
    n = len(s)
    return median(s[: n // 2]), median(s[(n + 1) // 2:])


def sd(v):
    return float(np.std(v, ddof=1))


def Phi(z):
    return float(st.norm.cdf(z))


def tstar(conf, df):
    return float(st.t.ppf(1 - (1 - conf / 100) / 2, df))


ZSTAR = {80: 1.282, 90: 1.645, 95: 1.96, 98: 2.326, 99: 2.576}
