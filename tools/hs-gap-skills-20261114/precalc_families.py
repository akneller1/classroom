"""Precalculus gap skills (2026-11-14).

Trigonometric Functions unit: fundamental identities, double- and half-angle identities, solving
trigonometric equations with identities.
Vectors, Complex Numbers & Polar Coordinates unit: polar equations and graphs, parametric equations.
New unit "Sequences, Series, and Limits": arithmetic and geometric sequences and series, infinite
geometric series, sigma notation, introduction to limits.
Same item contract as calc_families.py.
"""
import math
from fractions import Fraction as F
from hsfmt import sup, num, coef, join, poly
from calc_families import I, Reject, need, ri, lin, pw

PI_TXT = {F(0): "0", F(1, 6): "π/6", F(1, 4): "π/4", F(1, 3): "π/3", F(1, 2): "π/2", F(2, 3): "2π/3", F(3, 4): "3π/4", F(5, 6): "5π/6", F(1): "π",
          F(7, 6): "7π/6", F(5, 4): "5π/4", F(4, 3): "4π/3", F(3, 2): "3π/2", F(5, 3): "5π/3", F(7, 4): "7π/4", F(11, 6): "11π/6"}


def ang(fr):
    v = F(fr) % 2
    if v in PI_TXT:
        return PI_TXT[v]
    n_, d_ = v.numerator, v.denominator
    return (f"{n_}π" if n_ != 1 else "π") + (f"/{d_}" if d_ != 1 else "")


def rad(fr):
    """Exact text of √ values: (p, q) means p√q."""
    return fr


def sq(n):
    """Simplest radical form of √n as (outside, inside)."""
    o, i = 1, n
    for k in range(int(math.isqrt(n)), 1, -1):
        if i % (k * k) == 0:
            o, i = o * k, i // (k * k)
    return o, i


def frac_rad(sign, a, rootin, b):
    """Text for sign·a√rootin / b, simplified (rootin = 1 means rational)."""
    o, i = sq(rootin) if rootin > 1 else (1, 1)
    top = F(a * o, b)
    s = "-" if sign < 0 else ""
    if i == 1:
        return s + num(top)
    n_, d_ = top.numerator, top.denominator
    lead = "" if n_ == 1 else str(n_)
    t = f"{lead}√{i}"
    return s + (t if d_ == 1 else f"({t})/{d_}")


# Pythagorean-triple setups: sin, cos, tan from one given ratio and a quadrant
TRI = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
SIGNS = {1: (1, 1), 2: (1, -1), 3: (-1, -1), 4: (-1, 1)}  # (sin sign, cos sign)
QWORD = {1: "Quadrant I", 2: "Quadrant II", 3: "Quadrant III", 4: "Quadrant IV"}


def setup(r):
    a, b, c = r.choice(TRI)
    if r.random() < 0.5:
        a, b = b, a
    qd = r.randint(1, 4)
    ss, cs = SIGNS[qd]
    return F(ss * a, c), F(cs * b, c), qd


# =================================================================== Fundamental identities
def id_value(r, L):
    s, c, qd = setup(r)
    given, gv = r.choice([("sin", s), ("cos", c)]) if L < 2 else r.choice([("sin", s), ("cos", c), ("tan", s / c)])
    want = r.choice([w for w in (["cos", "tan"] if given == "sin" else ["sin", "tan"] if given == "cos" else ["sin", "cos"]) ] + (["sec", "csc", "cot"] if L > 0 else []))
    vals = {"sin": s, "cos": c, "tan": s / c, "sec": 1 / c, "csc": 1 / s, "cot": c / s}
    ans = vals[want]
    w = [(num(-ans), "used the wrong sign for the quadrant"), (num(1 / ans), "used the reciprocal ratio"),
         (num(vals["cos" if want != "cos" else "sin"] if want not in ("cos", "sin") else (c if want == "sin" else s)), "mixed up the ratios")]
    p = f"Given {given} θ = {num(gv)} and θ is in {QWORD[qd]}, find {want} θ."
    st = [f"Use sin²θ + cos²θ = 1: the missing ratio is ±{num(abs(c if given == 'sin' else s))}.", f"In {QWORD[qd]}, sin θ is {'positive' if s > 0 else 'negative'} and cos θ is {'positive' if c > 0 else 'negative'}.", f"{want} θ = {num(ans)}."]
    return I(p, num(ans), st, w, {"k": "trigval", "given": given, "v": num(gv), "quad": qd, "want": f"{want}(t)"}, "id_value")


SIMP = [  # (expression, simplest form, wrong forms with reasons) — L0
    ("sin(x)/cos(x)", "tan(x)", [("cot(x)", "flipped the quotient identity"), ("1", "cancelled sin and cos"), ("sec(x)", "mixed up the reciprocal identities")]),
    ("1 - sin²(x)", "cos²(x)", [("sin²(x)", "used the wrong Pythagorean identity"), ("cos(x)", "dropped the square"), ("-cos²(x)", "added a negative sign")]),
    ("1 - cos²(x)", "sin²(x)", [("cos²(x)", "used the wrong Pythagorean identity"), ("sin(x)", "dropped the square"), ("tan²(x)", "used 1 + tan² = sec²")]),
    ("1/cos(x)", "sec(x)", [("csc(x)", "mixed up sec and csc"), ("cot(x)", "mixed up the reciprocal identities"), ("cos(x)", "ignored the reciprocal")]),
    ("cos(x)/sin(x)", "cot(x)", [("tan(x)", "flipped the quotient identity"), ("1", "cancelled sin and cos"), ("csc(x)", "mixed up the reciprocal identities")]),
    ("sec²(x) - 1", "tan²(x)", [("cot²(x)", "used the cotangent identity"), ("sec(x)", "dropped the square"), ("1", "cancelled the secant")]),
]
SIMP1 = [
    ("sin(x)sec(x)", "tan(x)", [("1", "treated sec as 1/sin"), ("cot(x)", "flipped the quotient"), ("sin²(x)", "multiplied sin by sin")]),
    ("cos(x)tan(x)", "sin(x)", [("cos²(x)", "treated tan as cos"), ("1", "cancelled everything"), ("sin(x)cos(x)", "did not simplify")]),
    ("(1 - cos²(x))/sin(x)", "sin(x)", [("cos(x)", "used the wrong identity"), ("sin²(x)", "did not cancel"), ("1", "cancelled too much")]),
    ("csc(x) - sin(x)", "cos(x)cot(x)", [("cos(x)", "dropped a factor"), ("0", "treated csc as sin"), ("cot(x)", "dropped a factor")]),
    ("tan(x)cot(x) + tan²(x)", "sec²(x)", [("tan²(x)", "dropped the 1"), ("2tan²(x)", "treated cot as tan"), ("csc²(x)", "used the cotangent identity")]),
    ("sin²(x)cot²(x)", "cos²(x)", [("sin²(x)", "treated cot as 1"), ("1", "cancelled everything"), ("cot²(x)", "cancelled the sine only")]),
]
SIMP2 = [
    ("(sin(x) + cos(x))² - 1", "2sin(x)cos(x)", [("0", "forgot the middle term"), ("1", "used (a + b)² = a² + b²"), ("sin(x)cos(x)", "dropped the 2")]),
    ("sin(x)/(1 + cos(x)) + (1 + cos(x))/sin(x)", "2csc(x)", [("csc(x)", "dropped the 2"), ("2sin(x)", "flipped the result"), ("2", "cancelled too much")]),
    ("(sec(x) - cos(x))/tan(x)", "sin(x)", [("cos(x)", "simplified the wrong ratio"), ("tan(x)", "did not finish"), ("1", "cancelled too much")]),
    ("cos(x)/(1 - sin(x)) - tan(x)", "sec(x)", [("csc(x)", "mixed up sec and csc"), ("cos(x)", "dropped the reciprocal"), ("1", "cancelled too much")]),
    ("(1 + tan²(x))cos²(x)", "1", [("tan²(x)", "dropped the 1"), ("sec²(x)", "did not multiply by cos²"), ("cos²(x)", "treated 1 + tan² as 1")]),
    ("csc²(x) - cot²(x) + sin²(x)", "1 + sin²(x)", [("sin²(x)", "dropped the 1"), ("1", "dropped sin²(x)"), ("cos²(x)", "used the wrong identity")]),
]


def id_simplify(r, L):
    e, ans, w = r.choice([SIMP, SIMP1, SIMP2][L])
    arg = r.choice(["x", "x", "2x", "3x", "4x", "5x"])
    if arg != "x":
        e, ans = e.replace("(x)", f"({arg})"), ans.replace("(x)", f"({arg})")
        w = [(t.replace("(x)", f"({arg})"), why) for t, why in w]
    k = r.choice([1, 2, 3, 4])
    if k > 1:  # scaled versions for variety: k·(expression)
        sc = lambda t: t if t == "0" else (str(k) if t == "1" else (f"{k}({t})" if (" + " in t or " - " in t) else f"{k}{t}"))
        e, ans = f"{k}({e})", sc(ans)
        w = [(sc(t), why) for t, why in w]
    return I(f"Simplify {e} to a single trigonometric expression.", ans, ["Rewrite with sin and cos, then use sin²x + cos²x = 1, 1 + tan²x = sec²x or 1 + cot²x = csc²x.", f"= {ans}."],
             w, {"k": "ident", "e": e}, "id_simplify")


# =================================================================== Double- and half-angle identities
def da_value(r, L):
    s, c, qd = setup(r)
    if L == 2 and r.random() < 0.5:
        want = r.choice(["sin(t/2)", "cos(t/2)"])
        # θ in [0, 2π): θ/2 is in [0, π) → sin(θ/2) ≥ 0; cos(θ/2) ≥ 0 iff θ ≤ π (QI, QII)
        sgn = 1 if want.startswith("sin") or qd in (1, 2) else -1
        rad_in = (1 - c) / 2 if want.startswith("sin") else (1 + c) / 2  # value under the root
        # rad_in = p/q → √p/√q → √(pq)/q
        p_, q_ = rad_in.numerator, rad_in.denominator
        ans = frac_rad(sgn, 1, p_ * q_, q_)
        w = [(frac_rad(-sgn, 1, p_ * q_, q_), "chose the wrong sign for θ/2"), (num(rad_in), "forgot the square root"),
             (frac_rad(sgn, 1, ((1 + c) / 2 if want.startswith("sin") else (1 - c) / 2).numerator * ((1 + c) / 2 if want.startswith("sin") else (1 - c) / 2).denominator, ((1 + c) / 2 if want.startswith("sin") else (1 - c) / 2).denominator), "used the other half-angle formula")]
        wtxt = want.replace("t", "θ")
        st = [f"{wtxt} = ±√((1 {'-' if want.startswith('sin') else '+'} cos θ)/2) = ±√({num(rad_in)}).", "θ is between 0 and 2π, so θ/2 is between 0 and π; choose the sign for that quadrant.", f"{wtxt} = {ans}."]
        p = f"Given cos θ = {num(c)} and θ is in {QWORD[qd]} (0 ≤ θ < 2π), find {wtxt}."
        return I(p, ans, st, w, {"k": "trigval", "given": "cos", "v": num(c), "quad": qd, "want": want}, "da_half")
    want = r.choice(["sin(2t)", "cos(2t)", "tan(2t)"] if L > 0 else ["sin(2t)", "cos(2t)"])
    vals = {"sin(2t)": 2 * s * c, "cos(2t)": c * c - s * s, "tan(2t)": 2 * s * c / (c * c - s * s)}
    ans = vals[want]
    w = [(num(2 * (s if "sin" in want else c if "cos" in want else s / c)), "doubled the ratio instead of the angle"), (num(-ans), "used the wrong sign"),
         (num(s * c if "sin" in want else 1 - 2 * c * c if "cos" in want else 2 * s / c), "dropped a factor or used the wrong form")]
    given = r.choice(["sin", "cos"])
    gv = s if given == "sin" else c
    wtxt = want.replace("t", "θ")
    p = f"Given {given} θ = {num(gv)} and θ is in {QWORD[qd]}, find {wtxt}."
    st = [f"Find the other ratio: sin θ = {num(s)}, cos θ = {num(c)}.", "Use sin 2θ = 2 sin θ cos θ, cos 2θ = cos²θ - sin²θ, tan 2θ = sin 2θ / cos 2θ.", f"{wtxt} = {num(ans)}."]
    return I(p, num(ans), st, w, {"k": "trigval", "given": given, "v": num(gv), "quad": qd, "want": want}, "da_double")


def da_rewrite(r, L):
    a = ri(r, 1, 6)
    ax = "x" if a == 1 else f"{a}x"
    a2 = "2x" if a == 1 else f"{2 * a}x"
    k = ri(r, 2, 5) if L > 0 else 1
    pool = [(f"2sin({ax})cos({ax})", f"sin({a2})", [(f"sin({ax})", "did not double the angle"), (f"2sin({a2})", "kept the factor 2"), (f"cos({a2})", "used the cosine formula")]),
            (f"cos²({ax}) - sin²({ax})", f"cos({a2})", [(f"cos({ax})", "did not double the angle"), (f"1", "used the Pythagorean identity"), (f"sin({a2})", "used the sine formula")]),
            (f"1 - 2sin²({ax})", f"cos({a2})", [(f"cos²({ax})", "used 1 - sin² only"), (f"-cos({a2})", "lost the sign"), (f"sin({a2})", "used the sine formula")]),
            (f"2cos²({ax}) - 1", f"cos({a2})", [(f"cos²({ax})", "dropped the 2 and the 1"), (f"sin({a2})", "used the sine formula"), (f"cos({ax})", "did not double the angle")])]
    if L == 2:
        pool = [(f"(1 - cos({a2}))/2", f"sin²({ax})", [(f"cos²({ax})", "used the other power-reducing form"), (f"sin({ax})", "dropped the square"), (f"sin²({a2})", "kept the doubled angle")]),
                (f"(1 + cos({a2}))/2", f"cos²({ax})", [(f"sin²({ax})", "used the other power-reducing form"), (f"cos({ax})", "dropped the square"), (f"cos²({a2})", "kept the doubled angle")]),
                (f"sin({a2})/(1 + cos({a2}))", f"tan({ax})", [(f"cot({ax})", "flipped the result"), (f"tan({a2})", "kept the doubled angle"), (f"sin({ax})", "cancelled incorrectly")])]
    e, ans, w = r.choice(pool)
    if k > 1:
        e, ans = f"{k}({e})" if not e.startswith("2sin") else f"{2 * k}sin({ax})cos({ax})", f"{k}{ans}"
        w = [((f"{k}{t}" if t != "1" else str(k)), why) for t, why in w]
    return I(f"Write {e} as a single trigonometric expression.", ans, ["Match a double-angle or power-reducing identity.", f"= {ans}."], w, {"k": "ident", "e": e}, "da_rewrite")


# =================================================================== Trig equations with identities
def te(r, L):
    """Equations on [0, 2π) whose solutions are standard angles. Answers list every solution."""
    if L == 0:
        opts = [("2sin(x) - 1 = 0", [F(1, 6), F(5, 6)]), ("2cos(x) + 1 = 0", [F(2, 3), F(4, 3)]), ("tan(x) - 1 = 0", [F(1, 4), F(5, 4)]),
                ("2sin(x) + √3 = 0", [F(4, 3), F(5, 3)]), ("√2cos(x) - 1 = 0", [F(1, 4), F(7, 4)]), ("sin²(x) - 1 = 0", [F(1, 2), F(3, 2)]),
                ("4cos²(x) - 3 = 0", [F(1, 6), F(5, 6), F(7, 6), F(11, 6)]), ("2sin²(x) - 1 = 0", [F(1, 4), F(3, 4), F(5, 4), F(7, 4)])]
    elif L == 1:
        opts = [("2sin²(x) - sin(x) - 1 = 0", [F(1, 2), F(7, 6), F(11, 6)]), ("2cos²(x) + cos(x) - 1 = 0", [F(1, 3), F(1), F(5, 3)]),
                ("sin(2x) - cos(x) = 0", [F(1, 6), F(1, 2), F(5, 6), F(3, 2)]), ("cos(2x) + sin(x) = 0", [F(1, 2), F(7, 6), F(11, 6)]),
                ("2cos²(x) - 3cos(x) + 1 = 0", [F(0), F(1, 3), F(5, 3)]), ("tan²(x) - 3 = 0", [F(1, 3), F(2, 3), F(4, 3), F(5, 3)]),
                ("sin(x)cos(x) = 0", [F(0), F(1, 2), F(1), F(3, 2)])]
    else:
        opts = [("2sin²(x) + 3cos(x) - 3 = 0", [F(0), F(1, 3), F(5, 3)]), ("cos(2x) - cos(x) = 0", [F(0), F(2, 3), F(4, 3)]),
                ("sin(2x) + sin(x) = 0", [F(0), F(2, 3), F(1), F(4, 3)]), ("2cos²(x) + sin(x) - 1 = 0", [F(1, 2), F(7, 6), F(11, 6)]),
                ("sec²(x) - 2tan(x) = 0", [F(1, 4), F(5, 4)]), ("cos(2x) + 3cos(x) + 2 = 0", [F(2, 3), F(1), F(4, 3)]),
                ("sin²(x) - cos²(x) = 0", [F(1, 4), F(3, 4), F(5, 4), F(7, 4)]), ("2sin(x)cos(x) - sin(x) = 0", [F(0), F(1, 3), F(1), F(5, 3)])]
    eq, sols = r.choice(opts)
    single = not any(t in eq for t in ("2x", "sin(x)cos(x)", "tan(x)", "sec")) and (eq.count("sin") == 0 or eq.count("cos") == 0)
    k = r.choice([1, 1, 2, 3]) if (single and L > 0) else 1
    if k > 1:
        eq = eq.replace("(x)", f"({k}x)")
        sols = sorted({(u + 2 * m) / k for u in sols for m in range(k)})
    c = r.choice([1, 1, 2, 3])
    if c > 1 and eq.endswith(" = 0"):
        lhs = eq[:-4]
        eq = f"{c}({lhs}) = 0"
    fmt = lambda ss: "x = " + ", ".join(ang(v) for v in ss)
    ans = fmt(sols)
    w = []
    if len(sols) > 1:
        w.append((fmt(sols[:1]), "stopped after the first solution"))
        w.append((fmt(sols[:-1]), "missed a solution"))
    w.append((fmt(sorted({(v + F(1, 2)) % 2 for v in sols})), "used the wrong reference angle"))
    w.append((fmt(sorted({(2 - v) % 2 for v in sols} | set(sols))) if set((2 - v) % 2 for v in sols) - set(sols) else fmt(sorted({(1 - v) % 2 for v in sols})), "added angles from the wrong quadrants"))
    st = ["Rewrite with one function using an identity (sin 2x = 2 sin x cos x, cos 2x = 1 - 2sin²x = 2cos²x - 1, sin²x + cos²x = 1, sec²x = 1 + tan²x).",
          "Factor and set each factor equal to 0.", f"Solutions in [0, 2π): {ans[4:]}."]
    return I(f"Solve {eq} on the interval [0, 2π).", ans, st, w, {"k": "trigeq", "eq": eq}, "te_solve")


# =================================================================== Polar equations and graphs
def pol_convert(r, L):
    a = ri(r, 2, 8)
    if L == 0:
        pool = [(f"r = {a}", f"x² + y² = {a * a}", [(f"x² + y² = {a}", "forgot to square r"), (f"x + y = {a}", "replaced r with x + y"), (f"y = {a}x", "confused r with a slope")]),
                (f"r = {a}sec(θ)", f"x = {a}", [(f"y = {a}", "used sin instead of cos"), (f"x² + y² = {a * a}", "treated it as a circle"), (f"x = {F(1, a)}", "inverted the constant")] if False else [(f"y = {a}", "used sin instead of cos"), (f"x² + y² = {a * a}", "treated it as a circle"), (f"x = -{a}", "lost the sign")]),
                (f"r = {a}csc(θ)", f"y = {a}", [(f"x = {a}", "used cos instead of sin"), (f"x² + y² = {a * a}", "treated it as a circle"), (f"y = -{a}", "lost the sign")])]
    elif L == 1:
        pool = [(f"r = {a}cos(θ)", f"x² + y² = {a}x", [(f"x² + y² = {a}y", "used y instead of x"), (f"x² + y² = {a * a}", "treated it as a circle at the origin"), (f"x = {a}", "replaced r cos θ only")]),
                (f"r = {a}sin(θ)", f"x² + y² = {a}y", [(f"x² + y² = {a}x", "used x instead of y"), (f"x² + y² = {a * a}", "treated it as a circle at the origin"), (f"y = {a}", "replaced r sin θ only")]),
                (f"rcos(θ) + rsin(θ) = {a}", f"x + y = {a}", [(f"x - y = {a}", "mixed up a sign"), (f"x² + y² = {a}", "squared the terms"), (f"xy = {a}", "multiplied instead of adding")])]
    else:
        b = ri(r, 2, 6)
        pool = [(f"r = {a}/(cos(θ) + sin(θ))", f"x + y = {a}", [(f"x - y = {a}", "mixed up a sign"), (f"x² + y² = {a * a}", "treated it as a circle"), (f"xy = {a}", "multiplied instead of adding")]),
                (f"r = {a}/({b}cos(θ) - sin(θ))", f"{b}x - y = {a}", [(f"{b}x + y = {a}", "lost the sign of the sine term"), (f"x - {b}y = {a}", "swapped x and y"), (f"{b}y - x = {a}", "swapped x and y")]),
                (f"r² = {a * a}sec(2θ)" if False else f"r²cos(2θ) = {a * a}", f"x² - y² = {a * a}", [(f"x² + y² = {a * a}", "used cos² + sin² instead of cos² - sin²"), (f"y² - x² = {a * a}", "used the wrong double-angle form"), (f"2xy = {a * a}", "used the sine double-angle form")])]
    p_, ans, w = r.choice(pool)
    st = ["Use x = r cos θ, y = r sin θ and x² + y² = r² (multiply by r first if needed).", f"Rectangular form: {ans}."]
    return I(f"Write the polar equation {p_} in rectangular form.", ans, st, w, {"k": "polar", "eq": p_}, "pol_convert")


def pol_rose(r, L):
    a, n = ri(r, 2, 9), ri(r, 2, 7)
    f = r.choice(["sin", "cos"])
    eq = f"r = {a}{f}({n}θ)"
    petals = n if n % 2 else 2 * n
    if L == 0 or (L == 1 and r.random() < 0.5):
        q = f"How many petals does the rose curve {eq} have?"
        ans = str(petals)
        w = [(str(n if n % 2 == 0 else 2 * n), "used the wrong rule for odd and even n"), (str(a), "used the coefficient instead of n"), (str(n + 1), "counted one extra petal")]
        st = [f"n = {n} is {'odd' if n % 2 else 'even'}, so there are {'n' if n % 2 else '2n'} petals.", f"{ans} petals."]
        chk = {"k": "petals", "eq": eq}
    else:
        q = f"What is the maximum distance from the pole to a point on the graph of {eq}?"
        ans = str(a)
        w = [(str(n), "used n instead of the coefficient"), (str(2 * a), "doubled the coefficient"), (str(a * n), "multiplied a and n")]
        st = [f"|{f}({n}θ)| ≤ 1, so |r| ≤ {a}.", f"Maximum distance: {a}."]
        chk = {"k": "rmax", "eq": eq}
    return I(q, ans, st, w, chk, "pol_rose")


# =================================================================== Parametric equations
def par_elim(r, L):
    a, b, c, d = ri(r, 2, 5), ri(r, -6, 6, True), ri(r, 2, 5), ri(r, -6, 6)
    if L == 0:
        xs, ys = f"x = t + {b}" if b > 0 else f"x = t - {-b}", f"y = {lin(c, d).replace('x', 't')}"
        # t = x - b → y = c(x - b) + d
        ans = f"y = {lin(c, d - c * b)}"
        w = [(f"y = {lin(c, d + c * b)}", "used t = x + b"), (f"y = {lin(c, d)}", "replaced t with x"), (f"y = {lin(1, d - b)}", "dropped the coefficient")]
    elif L == 1:
        xs = f"x = {lin(a, b).replace('x', 't')}"
        ys = f"y = t² + {d}" if d > 0 else (f"y = t² - {-d}" if d < 0 else "y = t²")
        # t = (x - b)/a → y = (x - b)²/a² + d
        ans = f"y = ({poly({1: 1, 0: -b})})²/{a * a} + {d}" if d > 0 else (f"y = ({poly({1: 1, 0: -b})})²/{a * a} - {-d}" if d < 0 else f"y = ({poly({1: 1, 0: -b})})²/{a * a}")
        w = [(ans.replace(f"/{a * a}", f"/{a}"), "forgot to square the coefficient"), (ans.replace(poly({1: 1, 0: -b}), poly({1: 1, 0: b})), "used the wrong sign when solving for t"),
             (ans.replace(f"/{a * a}", ""), "ignored the coefficient of t")]
    else:
        k = r.choice(["circle", "ellipse"])
        if k == "circle":
            xs, ys = f"x = {a}cos(t)", f"y = {a}sin(t)"
            ans = f"x² + y² = {a * a}"
            w = [(f"x² + y² = {a}", "forgot to square the radius"), (f"x + y = {a}", "added without squaring"), (f"x² - y² = {a * a}", "subtracted the squares")]
        else:
            need(a != c)
            xs, ys = f"x = {a}cos(t)", f"y = {c}sin(t)"
            ans = f"x²/{a * a} + y²/{c * c} = 1"
            w = [(f"x²/{a} + y²/{c} = 1", "forgot to square the coefficients"), (f"x²/{c * c} + y²/{a * a} = 1", "swapped the denominators"), (f"x² + y² = {a * a + c * c}", "added the squares of the coefficients")]
    p = f"Eliminate the parameter: {xs}, {ys}. Write an equation in x and y."
    st = ["Solve one equation for t (or use cos²t + sin²t = 1).", "Substitute into the other equation.", ans + "."]
    return I(p, ans, st, w, {"k": "param", "x": xs[4:], "y": ys[4:]}, "par_elim")


def par_point(r, L):
    a, b, c, d, t0 = ri(r, 2, 5), ri(r, -6, 6), ri(r, -4, 4, True), ri(r, -6, 6), ri(r, -3, 3)
    xs = lin(a, b).replace("x", "t")
    ys = (poly({2: 1, 1: c, 0: d}) if L > 0 else lin(c, d)).replace("x", "t")
    if L == 2:
        xs = f"{a}cos(πt/{ri(r, 2, 4)})"
        need(True)
    x0 = "?"  # computed by the verifier from the printed equations; here exact values
    import math as _m
    def ev(t, s):
        from hsfmt import val
        return val(s, t=t)
    xv, yv = ev(t0, xs), ev(t0, ys)
    def nt(v):
        vv = round(v, 9)
        if abs(vv - round(vv)) < 1e-9:
            return str(int(round(vv)))
        for den in (2, 3, 4):
            if abs(vv * den - round(vv * den)) < 1e-9:
                return num(F(int(round(vv * den)), den))
        o2 = vv * 2 / _m.sqrt(2)
        if abs(o2 - round(o2)) < 1e-9:
            k_ = int(round(o2))
            sg, k_ = ("-" if k_ < 0 else ""), abs(k_)
            if k_ % 2 == 0:
                return sg + ("√2" if k_ == 2 else f"{k_ // 2}√2")
            return sg + (f"(√2)/2" if k_ == 1 else f"({k_}√2)/2")
        o3 = vv * 2 / _m.sqrt(3)
        if abs(o3 - round(o3)) < 1e-9:
            k_ = int(round(o3))
            sg, k_ = ("-" if k_ < 0 else ""), abs(k_)
            if k_ % 2 == 0:
                return sg + ("√3" if k_ == 2 else f"{k_ // 2}√3")
            return sg + (f"(√3)/2" if k_ == 1 else f"({k_}√3)/2")
        raise Reject()
    ans = f"({nt(xv)}, {nt(yv)})"
    w = [(f"({nt(yv)}, {nt(xv)})", "swapped x and y"), (f"({nt(ev(-t0, xs))}, {nt(ev(-t0, ys))})" if t0 else f"({nt(ev(1, xs))}, {nt(ev(1, ys))})", "used the wrong value of t"),
         (f"({nt(xv)}, {nt(ev(t0 + 1, ys))})", "made an error in y")]
    p = f"A particle moves along the curve x = {xs}, y = {ys}. Find its position at t = {t0}."
    return I(p, ans, ["Substitute t into both equations.", f"Position: {ans}."], w, {"k": "parpt", "x": xs, "y": ys, "t": t0}, "par_point")


# =================================================================== Sequences, series and limits
def seq_term(r, L):
    if r.random() < 0.5:
        a1, d, n = ri(r, -20, 20), ri(r, -9, 9, True), ri(r, 10, 60)
        terms = [a1 + i * d for i in range(4)]
        ans = a1 + (n - 1) * d
        w = [(str(a1 + n * d), "used n instead of n - 1"), (str(n * d), "forgot the first term"), (str(a1 + (n - 1) * d + d), "counted one extra step")]
        st = [f"Arithmetic: d = {d}.", f"aₙ = a₁ + (n - 1)d = {a1} + ({n - 1})({d}) = {ans}."]
    else:
        a1, q, n = ri(r, 1, 6) * r.choice([1, -1]), r.choice([2, 3, -2, F(1, 2), -3]), ri(r, 5, 9 if L < 2 else 11)
        terms = [a1 * q ** i for i in range(4)]
        ans = a1 * q ** (n - 1)
        w = [(num(a1 * q ** n), "used n instead of n - 1"), (num((a1 * q) ** (n - 1)), "raised the first term to the power too"), (num(a1 + (n - 1) * q), "treated it as arithmetic")]
        st = [f"Geometric: r = {num(q)}.", f"aₙ = a₁rⁿ⁻¹ = {a1}({num(q)}){sup(n - 1)} = {num(ans)}."]
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    p = f"Find the {n}{suf} term of the sequence {', '.join(num(t) for t in terms)}, …"
    return I(p, num(ans), st, w, {"k": "seqterm", "terms": [num(t) for t in terms], "n": n}, "seq_term")


def seq_sum(r, L):
    if r.random() < 0.5 or L == 0:
        a1, d, n = ri(r, -10, 15), ri(r, -6, 8, True), ri(r, 8, 40)
        terms = [a1 + i * d for i in range(4)]
        an = a1 + (n - 1) * d
        ans = n * (a1 + an) // 2 if n * (a1 + an) % 2 == 0 else F(n * (a1 + an), 2)
        w = [(num(F(n * (a1 + an))), "forgot to divide by 2"), (num(F((n - 1) * (a1 + an), 2)), "used n - 1 terms"), (str(an), "found the last term instead of the sum")]
        st = [f"a₁ = {a1}, d = {d}, a{''.join('₀₁₂₃₄₅₆₇₈₉'[int(ch)] for ch in str(n))} = {an}.", f"Sₙ = n(a₁ + aₙ)/2 = {num(ans)}."]
    else:
        a1, q, n = ri(r, 1, 5) * r.choice([1, -1]), r.choice([2, 3, -2]), ri(r, 5, 10)
        terms = [a1 * q ** i for i in range(4)]
        ans = F(a1 * (1 - q ** n), 1 - q)
        w = [(num(F(a1 * (1 - q ** (n - 1)), 1 - q)), "used n - 1 terms"), (num(a1 * q ** (n - 1)), "found the last term instead of the sum"), (num(F(a1, 1 - q)), "used the infinite-series formula")]
        st = [f"Geometric: a₁ = {a1}, r = {q}.", f"Sₙ = a₁(1 - rⁿ)/(1 - r) = {num(ans)}."]
    p = f"Find the sum of the first {n} terms of the series {' + '.join(num(t) for t in terms)} + …".replace("+ -", "- ")
    return I(p, num(ans), st, w, {"k": "seqsum", "terms": [num(t) for t in terms], "n": n}, "seq_sum")


def seq_inf(r, L):
    a1 = ri(r, 1, 30) * r.choice([1, 1, -1])
    q = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2), F(-1, 3), F(2, 5)] if L > 0 else [F(1, 2), F(1, 3), F(1, 4), F(2, 3)])
    terms = [a1 * q ** i for i in range(4)]
    ans = F(a1) / (1 - q)
    w = [(num(F(a1) / (1 + q)), "used 1 + r"), (num(F(a1) * (1 - q)), "multiplied instead of dividing"), ("The series diverges.", "thought every infinite series diverges")]
    p = f"Find the sum of the infinite geometric series {' + '.join(num(t) for t in terms)} + …".replace("+ -", "- ")
    st = [f"r = {num(q)} and |r| < 1, so the series converges.", f"S = a₁/(1 - r) = {a1}/(1 - {num(q)}) = {num(ans)}."]
    if L == 2 and r.random() < 0.4:
        q2 = r.choice([F(3, 2), F(-2), F(5, 4)])
        terms = [a1 * q2 ** i for i in range(4)]
        p = f"Find the sum of the infinite geometric series {' + '.join(num(t) for t in terms)} + …, or say that it diverges.".replace("+ -", "- ")
        ans_t = "The series diverges."
        w = [(num(F(a1) / (1 - q2)), "used a₁/(1 - r) even though |r| ≥ 1"), (num(F(a1) / (1 + q2)), "used 1 + r"), ("0", "thought the terms cancel")]
        return I(p, ans_t, [f"r = {num(q2)} and |r| ≥ 1.", "The series diverges."], w, {"k": "seqinf", "terms": [num(t) for t in terms]}, "seq_inf")
    return I(p, num(ans), st, w, {"k": "seqinf", "terms": [num(t) for t in terms]}, "seq_inf")


def sigma(r, L):
    lo, hi = ri(r, 1, 2), ri(r, 5, 12)
    if L == 0:
        a, b = ri(r, 2, 6), ri(r, -9, 9)
        e = lin(a, b).replace("x", "k")
    elif L == 1:
        a, b = ri(r, 1, 3), ri(r, -5, 5)
        e = poly({2: a, 0: b}).replace("x", "k")
    else:
        a, q = ri(r, 1, 5), r.choice([2, 3])
        e = f"{a}({q}){'^(k - 1)'}"
        e = f"{a}·{q}^(k - 1)" if a > 1 else f"{q}^(k - 1)"
    from hsfmt import val
    total = sum(val(e, k=k) for k in range(lo, hi + 1))
    ans = str(int(round(total)))
    w = [(str(int(round(total - val(e, k=lo)))), "skipped the first term"), (str(int(round(total + val(e, k=hi + 1)))), "added one extra term"), (str(int(round(val(e, k=hi)))), "found only the last term")]
    p = f"Evaluate Σ from k = {lo} to {hi} of ({e})."
    return I(p, ans, [f"Add the terms for k = {lo}, {lo + 1}, …, {hi} (or use a sum formula).", f"Sum = {ans}."], w, {"k": "sigma", "e": e, "lo": lo, "hi": hi}, "sigma")


def lim_intro(r, L):
    a = ri(r, -5, 5, True)
    if L == 0:
        b = ri(r, -6, 6)
        need(b != -a)
        e = f"({poly({2: 1, 1: b - a, 0: -a * b})})/(x - {a})" if a > 0 else f"({poly({2: 1, 1: b - a, 0: -a * b})})/(x + {-a})"
        ans = F(a + b)
        w = [("0", "stopped at 0/0"), ("The limit does not exist.", "thought 0/0 means no limit"), (num(F(b - a)), "used the wrong factor")]
        at = str(a)
        st = [f"Factor: (x - {a})(x + {b}) over x - {a}." if a > 0 else f"Factor and cancel the common factor.", f"The limit is {num(ans)}."]
    elif L == 1:
        c, d, m = ri(r, 1, 9), ri(r, 1, 9), ri(r, 0, 2)
        e = f"({poly({2: c, 1: ri(r, -5, 5), 0: 1})})/({poly({2: d, 0: -3})})" if m == 0 else (f"({poly({1: c, 0: 2})})/({poly({2: d, 0: 1})})" if m == 1 else f"({poly({2: c, 0: 1})})/({poly({1: d, 0: 5})})")
        at = "∞"
        if m == 0:
            ans = F(c, d)
            w = [(num(F(d, c)), "flipped the ratio"), ("0", "thought the limit at ∞ is always 0"), ("∞", "thought the limit at ∞ is always ∞")]
        elif m == 1:
            ans = F(0)
            w = [(num(F(c, d)), "compared leading coefficients with different degrees"), ("∞", "thought the numerator wins"), ("1", "guessed 1")]
        else:
            ans_t = "∞"
            w = [(num(F(c, d)), "compared leading coefficients with different degrees"), ("0", "thought the denominator wins"), ("1", "guessed 1")]
            return I(f"Evaluate lim (x → ∞) {e}.", ans_t, ["The numerator has the higher degree and both leading coefficients are positive.", "The limit is ∞."], w, {"k": "limit", "e": e, "at": "∞"}, "lim_intro")
        st = ["Compare the degrees of the numerator and the denominator.", f"The limit is {num(ans)}."]
    else:
        b = a * a
        k = r.choice(["root", "abs", "cube", "recip"])
        if k == "cube":
            c = ri(r, -4, 4, True)
            e, at, ans = (f"(x³ - {c ** 3})/(x - {c})" if c > 0 else f"(x³ + {-c ** 3})/(x + {-c})"), str(c), F(3 * c * c)
            w = [("0", "stopped at 0/0"), (str(c * c), "used only x² from the factorization"), (str(2 * c * c), "missed a term of x² + cx + c²")]
            st = ["Factor the difference (or sum) of cubes and cancel.", f"The limit is {num(ans)}."]
            return I(f"Evaluate lim (x → {at}) {e}.", num(ans), st, w, {"k": "limit", "e": e, "at": at}, "lim_intro")
        if k == "recip":
            c = ri(r, 2, 9)
            e, at, ans = f"(1/x - 1/{c})/(x - {c})", str(c), F(-1, c * c)
            w = [(num(F(1, c * c)), "lost the negative sign"), ("0", "stopped at 0/0"), (num(F(-1, c)), "forgot to divide by x")]
            st = [f"Combine: ({c} - x)/({c}x), then divide by (x - {c}) to get -1/({c}x).", f"The limit is {num(ans)}."]
            return I(f"Evaluate lim (x → {at}) {e}.", num(ans), st, w, {"k": "limit", "e": e, "at": at}, "lim_intro")
        if k == "root":
            c = ri(r, 1, 5)
            e, at, ans = f"(√(x + {c * c}) - {c})/x", "0", F(1, 2 * c)
            w = [("0", "stopped at 0/0"), (num(F(1, c)), "forgot the factor 2 when multiplying by the conjugate"), ("The limit does not exist.", "thought 0/0 means no limit")]
            st = ["Multiply by the conjugate √(x + c²) + c.", f"The limit is {num(ans)}."]
        else:
            c = ri(r, 1, 6)
            e, at = f"(x² - {c * c})/(|x - {c}|)", str(c)
            ans_t = "The limit does not exist."
            w = [(str(2 * c), "used only the right-hand limit"), (str(-2 * c), "used only the left-hand limit"), ("0", "stopped at 0/0")]
            return I(f"Evaluate lim (x → {at}) {e}.", ans_t, [f"From the right the expression approaches {2 * c}; from the left it approaches {-2 * c}.", "The one-sided limits differ, so the limit does not exist."],
                     w, {"k": "limitdne", "e": e, "at": at}, "lim_intro")
    return I(f"Evaluate lim (x → {at}) {e}.", num(ans), st, w, {"k": "limit", "e": e, "at": at}, "lim_intro")


NEW_UNITS = {("precalculus", "sequences-series-limits"): ("pc-ssl", "Sequences, Series, and Limits")}

SKILLS = {
    ("precalculus", "trigonometric-functions", "Fundamental Trigonometric Identities"): ([id_value, id_simplify], ["F-TF.C.8"]),
    ("precalculus", "trigonometric-functions", "Double-Angle and Half-Angle Identities"): ([da_value, da_rewrite], ["F-TF.C.9"]),
    ("precalculus", "trigonometric-functions", "Solving Trigonometric Equations with Identities"): ([te], ["F-TF.B.7", "F-TF.C.8"]),
    ("precalculus", "vectors", "Polar Equations and Graphs"): ([pol_convert, pol_rose], ["N-CN.B.4"]),
    ("precalculus", "vectors", "Parametric Equations"): ([par_elim, par_point], ["A-CED.A.2"]),
    ("precalculus", "sequences-series-limits", "Arithmetic and Geometric Sequences"): ([seq_term], ["F-BF.A.2", "F-LE.A.2"]),
    ("precalculus", "sequences-series-limits", "Finite Arithmetic and Geometric Series"): ([seq_sum], ["A-SSE.B.4"]),
    ("precalculus", "sequences-series-limits", "Infinite Geometric Series"): ([seq_inf], ["A-SSE.B.4"]),
    ("precalculus", "sequences-series-limits", "Sigma Notation"): ([sigma], ["A-SSE.B.4"]),
    ("precalculus", "sequences-series-limits", "Introduction to Limits"): ([lim_intro], ["F-IF.C.7d"]),
}
