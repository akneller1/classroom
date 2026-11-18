"""Precalculus audit #13 (batch P6): select-all items about properties, with 2 to 6 correct choices.

The 19 existing select-all items all read "Select ALL problems that are matched with the correct answer" and all
had exactly 3 correct choices. This adds one property item per level to a skill in every unit (27 items, ids ending
-x###); the number of correct choices varies (the bank schema needs at least 2). Check data goes to out/checks.json
and verify.py re-decides every choice. Re-running is safe: units that already have -x items are skipped.

Usage: python3 tools/precalculus-audit-20261118/gaps/selectall.py
"""
import json, os, random, sys
from collections import OrderedDict
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402
from families import num, poly  # noqa: E402

LEVELS = ["cp2", "cp1", "honors"]
NOTE = ("Original Claude-authored select-all item (family: {fam}). Every choice re-decided from the printed problem by "
        "tools/precalculus-audit-20261118/gaps/verify.py. Teacher reviewed 2026-11-18.")


def pick_counts(r, n_true, n_false, true_pool, false_pool):
    t = r.sample(true_pool, n_true)
    f = r.sample(false_pool, n_false)
    return t, f


# Each family returns (prompt, [(text, correct)], check)
def sa_even(r, L):
    pool = [("x⁴ - 3x²", True), ("|x| + 2", True), ("x² + 1", True), ("5 - x⁶", True), ("(x - 1)(x + 1)", True), ("2x² - |x|", True), ("x⁴ + x² - 7", True),
            ("x³", False), ("x² + x", False), ("(x - 2)²", False), ("x³ - x", False), ("|x - 1|", False), ("2x + 4", False), ("x⁵ + x²", False)]
    return "Select ALL functions that are even (f(-x) = f(x) for every x).", [(f"f(x) = {t}", ok) for t, ok in pool], dict(k="sa_even")


def sa_coterminal(r, L):
    d = r.choice([30, 45, 60, 120, 135, 150, 210, 240, 300, 315])
    true = [d + 360 * k for k in (-2, -1, 1, 2, 3) if d + 360 * k != d]
    false = [d + 180, d - 180, 360 - d, d + 90, -d, d + 270, 180 - d]
    false = [x for x in dict.fromkeys(false) if (x - d) % 360 != 0]
    return f"Select ALL angles that are coterminal with {d}°.", [(f"{x}°", True) for x in true] + [(f"{x}°", False) for x in false], dict(k="sa_coterminal", d=d)


def sa_orthogonal(r, L):
    a, b = r.choice([(2, 3), (1, -4), (3, 5), (-2, 5), (4, 1), (1, 2), (3, -2)])
    true = [(-b * k, a * k) for k in (1, -1, 2, -2, 3)]
    false = [(a, b), (b, a), (-a, b), (b, -a) if (b * a + -a * b) != 0 else (a + 1, b), (a * 2, b * 2), (-b, -a), (a - b, a + b)]
    false = [v for v in dict.fromkeys(false) if a * v[0] + b * v[1] != 0]
    return (f"Select ALL vectors that are orthogonal to ⟨{a}, {b}⟩.", [(f"⟨{x}, {y}⟩", True) for x, y in true] + [(f"⟨{x}, {y}⟩", False) for x, y in false],
            dict(k="sa_orthogonal", v=[a, b]))


def sa_invertible(r, L):
    opts = []
    while len(opts) < 24:
        m = [r.randint(-6, 6) for _ in range(4)]
        opts.append((f"[{m[0]}, {m[1]}; {m[2]}, {m[3]}]", m[0] * m[3] - m[1] * m[2] != 0))
        k = r.randint(-3, 3) or 2
        a, b = r.randint(-5, 5), r.randint(-5, 5)
        opts.append((f"[{a}, {b}; {k * a}, {k * b}]", False))
    return "Select ALL matrices that have an inverse.", list(dict.fromkeys(opts)), dict(k="sa_invertible")


def sa_ellipse(r, L):
    opts = []
    for A, C in [(4, 9), (2, 5), (3, 1), (9, 16), (1, 4), (5, 2), (4, 4), (3, 3), (1, -4), (-2, 5), (9, -1), (0, 3), (2, 0), (1, 1)]:
        D, E, Fc = r.randint(-8, 8), r.randint(-8, 8), r.randint(20, 60)

        def term(c, v, first=False):
            if c == 0:
                return ""
            mag = v if abs(c) == 1 else f"{abs(c)}{v}"
            return (("-" if c < 0 else "") + mag) if first else ((" - " if c < 0 else " + ") + mag)
        lead = term(A, "x²", True) or term(C, "y²", True)
        txt = lead + (term(C, "y²") if A else "") + term(D, "x") + term(E, "y") + f" - {Fc} = 0"
        opts.append((txt, A * C > 0 and A != C))
    return "Select ALL equations whose graphs are ellipses that are not circles. (Assume none is degenerate.)", opts, dict(k="sa_ellipse")


def sa_ineq(r, L):
    m, b = r.choice([1, 2, -1, -2, 3]), r.randint(-4, 4)
    op = r.choice(["<", ">", "≤", "≥"])
    rhs = poly({1: m, 0: b})
    pts = [(x, y) for x in range(-4, 5) for y in range(-6, 7)]
    r.shuffle(pts)
    test = {"<": lambda x, y: y < m * x + b, ">": lambda x, y: y > m * x + b, "≤": lambda x, y: y <= m * x + b, "≥": lambda x, y: y >= m * x + b}[op]
    # include boundary points so ≤ / < matters
    bound = [(x, m * x + b) for x in range(-3, 4) if abs(m * x + b) <= 6]
    pts = bound[:2] + pts
    return f"Select ALL points that are solutions of y {op} {rhs}.", [(f"({x}, {y})", test(x, y)) for x, y in pts[:40]], dict(k="sa_ineq", m=m, b=b, op=op)


def sa_acute(r, L):
    opts = []
    for _ in range(80):
        a, b, c = sorted(r.randint(3, 15) for _ in range(3))
        if a + b <= c:
            continue
        opts.append((f"{a}, {b}, {c}", a * a + b * b > c * c))
    return "Select ALL sets of side lengths that form an acute triangle. (Use the Law of Cosines: the largest angle is acute when c² < a² + b².)", list(dict.fromkeys(opts)), dict(k="sa_acute")


def sa_mutex(r, L):
    ev = {"an even number": {2, 4, 6}, "an odd number": {1, 3, 5}, "a number greater than 4": {5, 6}, "a number less than 3": {1, 2}, "a 6": {6},
          "a prime number": {2, 3, 5}, "a multiple of 3": {3, 6}, "a 1": {1}, "a number greater than 3": {4, 5, 6}}
    names = list(ev)
    pairs = [(x, y) for i, x in enumerate(names) for y in names[i + 1:]]
    return ("A number cube is rolled once. Select ALL pairs of events that are mutually exclusive.",
            [(f"rolling {x} and rolling {y}", not (ev[x] & ev[y])) for x, y in pairs], dict(k="sa_mutex"))


def sa_geometric(r, L):
    opts = []
    for _ in range(40):
        a = r.choice([1, 2, 3, -2, 4, 5, -1, 81, 64])
        kind = r.random()
        if kind < 0.5:
            q = r.choice([F(2), F(3), F(-2), F(1, 2), F(-1, 3), F(1, 3)])
            terms = [F(a) * q ** i for i in range(4)]
        else:
            d = r.choice([2, 3, -3, 5, 4])
            terms = [F(a + d * i) for i in range(4)]
        ok = all(t != 0 for t in terms) and len({terms[i + 1] / terms[i] for i in range(3)}) == 1
        opts.append((", ".join(num(t) for t in terms) + ", …", ok))
    return "Select ALL sequences that are geometric.", list(dict.fromkeys(opts)), dict(k="sa_geometric")


PLAN = {
    "functions": (4, sa_even, "pc-fun"),
    "trigonometric-functions": (3, sa_coterminal, "pc-trg"),
    "vectors": (8, sa_orthogonal, "pc-vec"),
    "matrices": (8, sa_invertible, "pc-mat"),
    "conics": (6, sa_ellipse, "pc-con"),
    "equations-inequalities": (7, sa_ineq, "pc-eqi"),
    "general-triangle-trigonometry": (4, sa_acute, "pc-gtt"),
    "probability": (4, sa_mutex, "pc-prb"),
    "sequences-series-limits": (1, sa_geometric, "pc-ssl"),
}
COUNTS = [2, 3, 4, 5, 6, 2, 4, 3, 5]   # correct choices per item (cycled), so the count varies across the bank


def main():
    checks_p = os.path.join(HERE, "out", "checks.json")
    checks = json.load(open(checks_p))
    i = 0
    for unit, (sidx, fn, prefix) in PLAN.items():
        bp = os.path.join(B.ROOT, "question-banks", "precalculus", unit + ".json")
        bank, raw = B.load_json(bp)
        sid = f"{unit}-skill-{sidx:02d}"
        if any(q["skillId"] == sid and q["id"].split("-")[-1].startswith("x") for q in bank["questions"]):
            print("skip", unit)
            continue
        stds = next(q["standards"] for q in bank["questions"] if q["skillId"] == sid)
        r = random.Random("pc-selectall-" + unit)
        out, tags = [], {}
        for L, lv in enumerate(LEVELS):
            prompt, opts, check = fn(r, L)
            good = [t for t, ok in opts if ok]
            bad = [t for t, ok in opts if not ok]
            k = COUNTS[i % len(COUNTS)]
            i += 1
            k = min(k, len(good))
            chosen = [(t, True) for t in r.sample(good, k)] + [(t, False) for t in r.sample(bad, 6 - k)]
            r.shuffle(chosen)
            q = OrderedDict(id=f"{prefix}-s{sidx:02d}-{lv}-x001", skillId=sid, level=lv, format="select-all", prompt=prompt,
                            options=[OrderedDict(text=t, correct=ok) for t, ok in chosen], answer=[t for t, ok in chosen if ok])
            q["solutionSteps"] = ["Check each choice."] + [f"{t}: {'yes' if ok else 'no'}." for t, ok in chosen] + [f"{k} of the 6 choices are correct."]
            q["standards"] = stds
            q["sourceNotes"] = NOTE.format(fam=check["k"])
            checks[q["id"]] = check
            tags[q["id"]] = []
            out.append(q)
        bank["questions"].extend(out)
        B.dump_json(bp, bank, raw)
        tp = os.path.join(B.ROOT, "question-banks", "precalculus", "meta", unit + ".tags.json")
        tg, traw = B.load_json(tp)
        tg.update(tags)
        B.dump_json(tp, tg, traw)
        print(unit, "+", len(out), "select-all items")
    json.dump(checks, open(checks_p, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
