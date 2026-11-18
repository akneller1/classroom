"""Precalculus audit #12 (batch P6): Advanced items that differ in kind, not only in the numbers.

In five skills every Advanced question type also appeared at Support. advanced.py replaces three Advanced short-answer or
multiple-choice items of each (from the most common Advanced template) with a harder variant that only Advanced gets.
Same contract as variety.py; verify.py re-checks them. Re-running is safe: a skill whose Advanced items already include
a family from here is skipped.

Usage: python3 tools/precalculus-audit-20261118/gaps/advanced.py
"""
import collections, json, math, os, random, sys
from collections import OrderedDict
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402
from families import I, need, ri, num  # noqa: E402
from contexts import rd  # noqa: E402
from replace import sig, is_ea  # noqa: E402


def adv_lp_area(r, L):
    need(L == 2)
    X, Y = ri(r, 1, 6), ri(r, 1, 6)
    a1, b1, a2, b2 = ri(r, 1, 4), ri(r, 2, 6), ri(r, 2, 6), ri(r, 1, 4)
    need(a1 * b2 != a2 * b1 and F(a1, b1) < F(a2, b2))
    c1, c2 = a1 * X + b1 * Y, a2 * X + b2 * Y
    yi, xi = min(F(c1, b1), F(c2, b2)), min(F(c1, a1), F(c2, a2))
    need(yi.denominator == 1 and xi.denominator == 1)
    P = [(0, 0), (xi, 0), (X, Y), (0, yi)]
    area = abs(sum(P[i][0] * P[(i + 1) % 4][1] - P[(i + 1) % 4][0] * P[i][1] for i in range(4))) / 2
    reg = f"x ≥ 0, y ≥ 0, {a1}x + {b1}y ≤ {c1}, {a2}x + {b2}y ≤ {c2}".replace(" 1x", " x").replace(" 1y", " y")
    prompt = f"Find the area of the feasible region {reg}."
    steps = [f"Corners: (0, 0), ({xi}, 0), ({X}, {Y}), (0, {yi}).", f"Split along the segment from (0, 0) to ({X}, {Y}): ½·{xi}·{Y} + ½·{yi}·{X} = {num(area)}."]
    wr = [(num(xi * yi / 2), "used the triangle under the intercepts"), (num(xi * yi), "used the rectangle"), (num(F(X * Y)), "used the rectangle at the corner"), (num(area * 2), "forgot the ½")]
    return I(prompt, num(area), steps, wr, dict(k="adv_lp_area", l1=[a1, b1, c1], l2=[a2, b2, c2], show=[reg]), "adv_lp_area")


def adv_amb_range(r, L):
    need(L == 2)
    A = r.choice([30, 30, 45, 60])
    b = 2 * ri(r, 3, 12)
    lo = {30: f"{b // 2}", 45: f"{b // 2}√2", 60: f"{b // 2}√3"}[A]
    prompt = f"In triangle ABC, A = {A}° and b = {b}. For which values of side a are there exactly two triangles?"
    ans = f"{lo} < a < {b}"
    steps = [f"The height is h = b sin A = {b} sin {A}° = {lo}.", f"Two triangles when h < a < b: {ans}."]
    wr = [(f"a > {b}", "gave the one-triangle case"), (f"a < {lo}", "gave the no-triangle case"), (f"{lo} ≤ a ≤ {b}", "included the endpoints, which give one triangle"),
          (f"{b} < a < {2 * b}", "used the wrong bounds")]
    return I(prompt, ans, steps, wr, dict(k="adv_amb_range", A=A, b=b, show=[f"A = {A}°", f"b = {b}"]), "adv_amb_range")


def adv_heron_consec(r, L):
    need(L == 2)
    x = ri(r, 3, 20)
    a, b, c = x, x + 1, x + 2
    s = F(a + b + c, 2)
    A = math.sqrt(s * (s - a) * (s - b) * (s - c))
    P = a + b + c
    prompt = f"A triangle's sides are three consecutive whole numbers and its perimeter is {P}. Use Heron's formula to find its area to the nearest tenth."
    ans = "≈ " + rd(A, 1)
    steps = [f"x + (x + 1) + (x + 2) = {P}, so the sides are {a}, {b}, {c}.", f"s = {num(s)}; area = √({num(s)}·{num(s - a)}·{num(s - b)}·{num(s - c)}) {ans}."]
    wr = [("≈ " + rd(math.sqrt(float(s * (s - a) * (s - b) * (s - c)) * 4), 1), "used the perimeter instead of the semiperimeter in one factor"),
          ("≈ " + rd(a * b / 2, 1), "used ½ab as if the triangle were right"), ("≈ " + rd(float(s * (s - a) * (s - b) * (s - c)), 1), "forgot the square root"),
          ("≈ " + rd(A + 2, 1), "made an arithmetic slip")]
    return I(prompt, ans, steps, wr, dict(k="adv_heron_consec", P=P, show=[str(P)]), "adv_heron_consec")


def adv_norm_between(r, L):
    need(L == 2)
    mu, sd = ri(r, 40, 90), ri(r, 3, 12)
    k1, k2 = r.choice([(-1, 2), (-2, 1), (-2, 3), (-3, 1), (0, 2), (-1, 0), (1, 2), (-3, -1)])
    cum = {-3: F(15, 1000), -2: F(25, 1000), -1: F(16, 100), 0: F(50, 100), 1: F(84, 100), 2: F(975, 1000), 3: F(9985, 10000)}
    p = (cum[k2] - cum[k1]) * 100
    lo, hi = mu + k1 * sd, mu + k2 * sd
    prompt = f"Using the 68–95–99.7 rule, what percent of data lie between {lo} and {hi} in a normal distribution with mean {mu} and standard deviation {sd}?"
    ans = f"{num(p) if p.denominator == 1 else format(float(p), 'g')}%"
    steps = [f"{lo} is {k1} and {hi} is {k2} standard deviations from the mean.", f"Add the empirical-rule pieces between them: {ans}."]
    wr = [("68%", "used the one-standard-deviation percent"), ("95%", "used the two-standard-deviation percent"), (f"{format(float(p) / 2, 'g')}%", "took only half"),
          (f"{format(100 - float(p), 'g')}%", "found the percent outside")]
    return I(prompt, ans, steps, wr, dict(k="adv_norm_between", k1=k1, k2=k2, show=[f"between {lo} and {hi}", f"mean {mu}", f"deviation {sd}"]), "adv_norm_between")


def adv_two_angles(r, L):
    need(L == 2)
    d = 10 * ri(r, 5, 30)
    a, b = ri(r, 20, 40), ri(r, 45, 70)
    h = d / (1 / math.tan(math.radians(a)) - 1 / math.tan(math.radians(b)))
    prompt = (f"From a point on level ground the angle of elevation to the top of a tower is {a}°. After walking {d} ft straight toward the tower "
              f"it is {b}°. How tall is the tower? Round to the nearest foot.")
    ans = "≈ " + rd(h, 0) + " ft"
    steps = [f"With x the distance from the second point: h = x tan {b}° and h = (x + {d}) tan {a}°.", f"So h = {d}/(cot {a}° - cot {b}°) {ans}."]
    wr = [("≈ " + rd(d * math.tan(math.radians(b)), 0) + " ft", "used only the second angle with the walked distance"),
          ("≈ " + rd(d * math.tan(math.radians(a)), 0) + " ft", "used only the first angle"),
          ("≈ " + rd(d / (math.tan(math.radians(b)) - math.tan(math.radians(a))), 0) + " ft", "subtracted tangents instead of cotangents"),
          ("≈ " + rd(h * 1.1, 0) + " ft", "made a rounding slip")]
    return I(prompt, ans, steps, wr, dict(k="adv_two_angles", d=d, a=a, b=b, show=[f"{a}°", f"{b}°", f"{d} ft"]), "adv_two_angles")


ADV = {
    "equations-inequalities-skill-10": adv_lp_area,
    "general-triangle-trigonometry-skill-03": adv_amb_range,
    "general-triangle-trigonometry-skill-05": adv_heron_consec,
    "probability-skill-08": adv_norm_between,
    "trigonometric-functions-skill-05": adv_two_angles,
}


def main():
    checks_p = os.path.join(HERE, "out", "checks.json")
    checks = json.load(open(checks_p))
    for sk, fn in ADV.items():
        unit = sk.rsplit("-skill-", 1)[0]
        bp = os.path.join(B.ROOT, "question-banks", "precalculus", unit + ".json")
        bank, raw = B.load_json(bp)
        hon = [q for q in bank["questions"] if q["skillId"] == sk and q["level"] == "honors" and q["format"] in ("short-answer", "multiple-choice")]
        if any(f"family: {fn.__name__}" in q["sourceNotes"] for q in hon):
            print("skip", sk)
            continue
        top = collections.Counter(sig(q["prompt"]) for q in hon).most_common(1)[0][0]
        cand = [q for q in hon if sig(q["prompt"]) == top and not is_ea(q)][-3:]
        r = random.Random("pc-advanced-" + sk)
        used = {q["prompt"] for q in bank["questions"]}
        name = B.catalog_names(unit)[int(sk[-2:]) - 1]
        for q in cand:
            kind = "mc" if q["format"] == "multiple-choice" else "sa"
            it = B.make([fn], r, 2, used, min_wrongs=3 if kind == "mc" else 0)

            def base(item, fmt, q=q):
                return OrderedDict(id=q["id"], skillId=q["skillId"], level=q["level"], format=fmt, prompt=item["prompt"], answer=item["answer"])
            new, _, fam = B.item(kind, it, r, base, unit, checks, name)
            new["standards"] = q["standards"]
            new["sourceNotes"] = ("Original Claude-authored Advanced item (family: " + fam + "), added so Advanced differs in kind (Precalculus audit #12). "
                                  "Answer and every option re-checked by tools/precalculus-audit-20261118/gaps/verify.py. Teacher reviewed 2026-11-18.")
            bank["questions"][bank["questions"].index(q)] = new
        B.dump_json(bp, bank, raw)
        print(sk, "replaced", len(cand))
    json.dump(checks, open(checks_p, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
