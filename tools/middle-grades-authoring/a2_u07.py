"""Algebra 2 Unit 7 — Rational Functions (rational-functions). Top-up families."""
from hslib import *
import math
import pc_u02 as F2
import ca_u01 as CA1

UNIT_ID = "rational-functions"
ABBR = "rf"


def ri(r, a, b):
    return rint(r, a, b, True)


def lin(a):
    return T(x - a)


def ftext(e):
    """Factored text: (x - 2)(x + 3)."""
    fs = sp.factor_list(sp.expand(e))
    c, facs = fs
    out = "".join(f"({T(b_)})" + (str(k_).translate(SUP) if k_ > 1 else "") for b_, k_ in facs)
    return (T(c) if c not in (1, -1) else "-" if c == -1 else "") + out if out else T(c)


def frac(num, den):
    n_, d_ = T(num), ftext(den) if not sp.sympify(den).is_number else T(den)
    nt = n_ if sp.sympify(num).is_number or (sp.sympify(num).is_Symbol) else f"({n_})"
    dt = d_ if (d_.startswith("(") and d_.endswith(")") and d_.count("(") == 1) or sp.sympify(den).is_number else f"({d_})"
    return f"{nt}/{dt}"


# ============================================================== S1 Simplifying rational expressions
@fam("012")
def s1_simp(r, L):
    a, b, c = r.sample([v for v in range(-7, 8)], 3)
    k = 1 if L == 0 else pick(r, [1, 2, 3, -1])
    num = sp.expand(k * (x - a) * (x - b))
    den = sp.expand((x - a) * (x - c)) if L else sp.expand((x - a) * pick(r, [2, 3, 4, 5]))
    simp = sp.cancel(num / den)
    ans = frac(sp.expand(sp.numer(sp.together(simp))), sp.denom(sp.together(simp))) if sp.denom(sp.together(simp)) != 1 else T(simp)
    wr = [frac(sp.expand(k * (x + a) * (x - b)) if a else k * (x - b) + 1, sp.denom(sp.together(simp))) if not simp.is_polynomial(x) else T(simp + 1),
          frac(num.coeff(x, 0), den.coeff(x, 0)) if den.coeff(x, 0) else T(simp * 2), frac(k * (x - b) * -1, sp.denom(sp.together(simp))) if not simp.is_polynomial(x) else T(-simp)]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Simplify ({T(num)})/({T(den)}).", ans,
             [f"Factor the numerator: {ftext(num)}.", f"Factor the denominator: {ftext(den)}.", f"Cancel the common factor ({lin(a)}): {ans}."],
             wr, H(f"cancel(P('({T(num)})/({T(den)})'))"), why=["Made a sign error when factoring", "Cancelled terms instead of factors", "Made a sign error in the result"])


# ============================================================== S2 Multiplying and dividing
@fam("012")
def s2_muldiv(r, L):
    a, b, c, d = r.sample([v for v in range(-6, 7) if v], 4)
    op = pick(r, ["·", "÷"]) if L else "·"
    k1, k2 = (rint(r, 2, 6), rint(r, 2, 6))
    e1n, e1d = sp.expand(k1 * (x - a)), sp.expand((x - b) * (x - c))
    e2n, e2d = sp.expand((x - b)), sp.expand(k2 * (x - a) * (x - d)) if L == 2 else sp.expand(k2 * (x - d))
    if op == "÷":
        e2n, e2d = e2d, e2n
    t1, t2 = f"({T(e1n)})/({T(e1d)})", f"({T(e2n)})/({T(e2d)})"
    t1 = t1.replace(f"({T(e1n)})/", f"{T(e1n)}/") if " " not in T(e1n) else t1
    res = sp.cancel(e1n * e2n / (e1d * e2d)) if op == "·" else sp.cancel(e1n * e2d / (e1d * e2n))
    num, den = sp.fraction(sp.factor(res))
    ans = frac(sp.expand(num), den) if den != 1 else T(sp.expand(num))
    bad = sp.cancel(e1n * e2n / (e1d * e2d)) if op == "÷" else sp.cancel(e1n * e2d / (e1d * e2n))
    bn, bd = sp.fraction(sp.factor(bad))
    wr = [frac(sp.expand(bn), bd) if bd != 1 else T(sp.expand(bn)), frac(sp.expand(num) + 1, den) if den != 1 else T(sp.expand(num) + 1), frac(sp.expand(num), sp.expand(den * (x - b))) if den != 1 else T(sp.expand(num * 2))]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Simplify: ({t1}) {op} ({t2})", ans,
             ["Factor every numerator and denominator." + (" To divide, multiply by the reciprocal of the second fraction." if op == "÷" else ""), "Cancel common factors.", f"{ans}."],
             wr, H(f"cancel(P('({t1}) {'*' if op == '·' else '/'} ({t2})'))"),
             why=["Multiplied instead of dividing" if op == "÷" else "Divided instead of multiplying", "Made an arithmetic error after cancelling", "Did not cancel a common factor"])


# ============================================================== S3 Adding and subtracting
@fam("012")
def s3_addsub(r, L):
    p, q = r.sample([v for v in range(-6, 7) if v], 2)
    a, b = ri(r, -6, 6), rint(r, 1, 6)
    op = pick(r, ["+", "-"])
    if L == 0:
        q = p
    e = a / (x - p) + (b if op == "+" else -b) / (x - q)
    tot = sp.together(e)
    num, den = sp.fraction(sp.factor(tot))
    num = sp.expand(num)
    need(num != 0)
    ans = frac(num, den) if not num.is_number else f"{T(num)}/{ftext(den) if not ftext(den).startswith('(') or ftext(den).count('(') > 1 else ftext(den)}" if False else frac(num, den)
    t = f"{a}/({lin(p)}) {op} {b}/({lin(q)})"
    wr = [frac(a + b if op == "+" else a - b, sp.expand((x - p) + (x - q))) if p != q else frac(a + b if op == "-" else a - b, x - p),
          frac(sp.expand(a * (x - q) - (b if op == "+" else -b) * (x - p)), den) if p != q else frac(a * b, x - p),
          frac(sp.expand(num + (2 * b if op == "-" else -2 * b)), den) if p != q else frac(num, sp.expand(2 * (x - p)))]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Simplify: {t}", ans,
             ["Use the common denominator " + (f"({lin(p)})({lin(q)})." if p != q else f"{lin(p)}."), "Rewrite each fraction over the common denominator and combine the numerators.", f"{ans}."],
             wr, H(f"together(P('{t}'))"), why=["Added the denominators" if p != q else "Used the wrong operation on the numerators",
                                                 ("Did not distribute the subtraction" if op == "-" else "Subtracted the second numerator") if p != q else "Multiplied the numerators",
                                                 "Made a sign error combining the numerators" if p != q else "Added the denominators"])


# ============================================================== S4 Solving rational equations
@fam("012")
def s4_solve(r, L):
    kind = pick(r, ["prop", "lcd"])
    if kind == "prop":
        b, m, kk = rint(r, 1, 7), rint(r, 2, 9), rint(r, 1, 3)
        need(math.gcd(b, m) == 1)
        a = b * kk * pick(r, [1, -1])
        c = rint(r, -6, 6)
        v = sp.Integer(a * m // b - c)
        txt = f"{a}/({T(x + c)}) = {b}/{m}" if c else f"{a}/x = {b}/{m}"
        ans = f"x = {T(v)}"
        wr = [f"x = {T(sp.Rational(b * m, a) - c)}", f"x = {T(sp.Rational(a * m, b) + c)}", f"x = {T(sp.Rational(a * m, b))}" if c else f"x = {T(v + 1)}"]
        st = ["Cross-multiply.", f"{b}({T(x + c)}) = {a * m}." if c else f"{b}x = {a * m}.", f"{ans}."]
        why = ["Cross-multiplied the wrong pairs", "Made a sign error with the constant", "Forgot to subtract the constant"]
    else:
        # a/x + b = c/x  → a + bx = c → x = (c - a)/b ; or 1/x + 1/(2x) = k
        a, b = ri(r, -9, 9), ri(r, -5, 5)
        v = ri(r, -6, 6)
        c = a + b * v
        need(c != a)
        txt = f"{a}/x {'+' if b > 0 else '-'} {abs(b)} = {c}/x"
        ans = f"x = {v}"
        wr = [f"x = {T(sp.Rational(a - c, b))}", f"x = {T(sp.Rational(c + a, b))}" if (c + a) != 0 and sp.Rational(c + a, b) != v else f"x = {v + 2}", f"x = {T(sp.Rational(c, b))}" if sp.Rational(c, b) != v else f"x = {v - 1}"]
        st = ["Multiply every term by the LCD, x.", f"{a} {'+' if b > 0 else '-'} {abs(b)}x = {c}.", f"{ans}; x = {v} does not make a denominator 0, so it is valid."]
        why = ["Made a sign error moving the constant", "Added instead of subtracting", "Forgot to multiply the constant term by x"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve {txt}.", ans, st, wr, H(f"solve(Eq(P('{txt.split(' = ')[0]}'), P('{txt.split(' = ')[1]}')), x)", "set"), why=why)


# ============================================================== S5 Excluded values and extraneous solutions
@fam("012")
def s5_excluded(r, L):
    a, b = sorted(r.sample(range(-8, 9), 2))
    k = pick(r, [1, 2, 3])
    num = sp.expand(k * x + rint(r, -9, 9))
    den = sp.expand((x - a) * (x - b)) if L else (x - a)
    if L == 0:
        b = None
    t = f"({T(num)})/({T(den)})"
    ans = f"x = {a}" if b is None else f"x = {a} or x = {b}"
    wr = [f"x = {-a}" if b is None else f"x = {-a} or x = {-b}", f"x = {T(sp.solve(num, x)[0])}", f"x = {T(den.subs(x, 0))}" if L and den.subs(x, 0) not in (a, b, -a, -b) else "none; every real number is allowed"]
    need(len(set(wr) | {ans}) == 4 and num.subs(x, a) != 0 and (b is None or num.subs(x, b) != 0))
    return Q(f"What value(s) of x must be excluded from the domain of {t}?", ans,
             [f"Set the denominator equal to 0: {T(den)} = 0.", f"Factor: {ftext(den)} = 0." if L else f"{T(den)} = 0.", f"Exclude {ans}."],
             wr, H(f"solve(P('{T(den)}'), x)", "set"), why=["Used the opposite signs", "Set the numerator equal to 0", "Used the constant term of the denominator" if L and den.subs(x, 0) not in (a, b, -a, -b) else "Did not look for values that make the denominator 0"])


@fam("012")
def s5_extraneous(r, L):
    a = ri(r, -6, 6)
    b = ri(r, -6, 6)
    need(a != b)
    # x/(x - a) = a/(x - a) + b  → x = a + b(x - a) → (1 - b)x = a - ab → x = a (excluded) when b ≠ 1
    # use: x²/(x - a) = a²/(x - a)  → x² = a² → x = ±a; x = a extraneous
    need(a != 0)
    t = f"x²/({T(x - a)}) = {a * a}/({T(x - a)})"
    ans = f"x = {-a}"
    wr = [f"x = {a} or x = {-a}", f"x = {a}", "no solution"]
    return Q(f"Solve {t}. Identify any extraneous solutions.", ans,
             ["Multiply both sides by the LCD.", f"x² = {a * a}, so x = {a} or x = {-a}.", f"x = {a} makes the denominator 0, so it is extraneous.", f"{ans}."],
             wr, H(f"solve(Eq(P('{t.split(' = ')[0]}'), P('{t.split(' = ')[1]}')), x)", "set"),
             why=["Did not check for extraneous solutions", "Kept the extraneous solution", "Rejected both solutions"])


# ============================================================== S6 Asymptotes
@fam("012")
def s6_ha(r, L):
    n_deg = pick(r, [0, 1]) if L == 0 else pick(r, [0, 1, 2])
    d_deg = 1 if L == 0 else pick(r, [1, 2])
    a, b = ri(r, -6, 6), ri(r, -6, 6)
    num = a * x ** n_deg + rint(r, -9, 9) if n_deg else sp.Integer(a)
    den = b * x ** d_deg + rint(r, -9, 9)
    need(n_deg <= d_deg)
    f = num / den
    ha = sp.Rational(a, b) if n_deg == d_deg else 0
    t = f"({T(num)})/({T(den)})" if n_deg else f"{a}/({T(den)})"
    ans = f"y = {T(ha)}"
    wr = [f"y = {T(sp.Rational(b, a))}" if n_deg == d_deg and sp.Rational(b, a) != ha else "y = 1", f"x = {T(sp.solve(den, x)[0])}" if d_deg == 1 else "x = 0", f"y = {T(a)}" if a != ha else f"y = {T(ha + 1)}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Find the horizontal asymptote of f(x) = {t}.", ans,
             ["Compare the degrees of the numerator and the denominator.", "Equal degrees: y = ratio of leading coefficients. Smaller numerator degree: y = 0.", f"{ans}."],
             wr, H(f"y - limit(P('{t}'), x, oo)", "eqn"), why=["Flipped the ratio of leading coefficients", "Gave the vertical asymptote", "Used only the numerator's leading coefficient"])


# ============================================================== S7 Graphing rational functions
@fam("012")
def s7_features(r, L):
    a, b, c = r.sample([v for v in range(-6, 7)], 3)
    k = pick(r, [1, 2, -1, 3])
    ask = pick(r, ["xint", "va", "hole"] if L else ["xint", "va"])
    if ask == "hole":
        num, den = sp.expand(k * (x - a) * (x - b)), sp.expand((x - a) * (x - c))
        hy = sp.Rational(k * (a - b), a - c)
        t = f"({T(num)})/({T(den)})"
        ans = f"({a}, {T(hy)})"
        wr = [f"({c}, 0)", f"({a}, 0)", f"({b}, {T(hy)})" if b != a else f"({a}, {T(hy + 1)})"]
        need(len(set(wr) | {ans}) == 4)
        return Q(f"Find the hole in the graph of f(x) = {t}.", ans, [f"Factor: {ftext(num)} over {ftext(den)}.", f"The common factor {lin(a)} gives a hole at x = {a}.", f"Simplified value at x = {a}: {T(hy)}. Hole: {ans}."],
                 wr, H(f"({a}, limit(P('{t}'), x, {a}))", "point"), why=["Gave the vertical asymptote", "Put the hole on the x-axis", "Used the zero of the numerator"])
    num, den = sp.expand(k * (x - b)), sp.expand(x - c) if L == 0 else sp.expand((x - c) * (x - a))
    need(b != c and b != a)
    t = f"({T(num)})/({T(den)})"
    if ask == "xint":
        ans = f"({b}, 0)"
        wr = [f"({c}, 0)", f"(0, {T(sp.Rational(num.subs(x, 0), den.subs(x, 0)))})" if den.subs(x, 0) else f"({-b}, 0)", f"({-b}, 0)" if b else f"({b + 1}, 0)"]
        need(len(set(wr) | {ans}) == 4)
        return Q(f"Find the x-intercept of f(x) = {t}.", ans, ["x-intercepts are where the numerator is 0 (and the denominator is not).", f"{T(num)} = 0 → x = {b}.", f"{ans}."],
                 wr, H(f"[(s_, 0) for s_ in solve(P('{t}'), x)][0]", "point"), why=["Used the zero of the denominator", "Gave the y-intercept", "Made a sign error"])
    vas = sorted({c, a}) if L else [c]
    ans = " and ".join(f"x = {v}" for v in vas)
    wr = [" and ".join(f"x = {-v}" for v in vas) if any(vas) else "x = 1", f"x = {b}", f"y = {k}" if L == 0 else f"x = {vas[0]}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Find all vertical asymptotes of f(x) = {t}.", ans, ["Vertical asymptotes are where the denominator is 0 and the numerator is not.", f"{ftext(den)} = 0.", f"{ans}."],
             wr, PY("vas", f=t), why=["Made a sign error", "Used the zero of the numerator", "Gave the horizontal asymptote" if L == 0 else "Missed one of the asymptotes"])


# ============================================================== S8 Rational variation and modeling
@fam("012")
def s8_work(r, L):
    a, b = r.sample([2, 3, 4, 5, 6, 8, 10, 12, 15, 20], 2)
    t_ = sp.Rational(a * b, a + b)
    n1, n2 = name(r), name(r)
    need(n1 != n2)
    job = pick(r, ["paint a fence", "mow a lawn", "clean a gym", "grade a stack of tests", "fill a pool"])
    return Q(f"{n1} can {job} in {a} hours, and {n2} can do it in {b} hours. How long will it take them working together?", f"{T(t_)} hours",
             [f"Rates: 1/{a} and 1/{b} of the job per hour.", f"Together: 1/{a} + 1/{b} = {T(sp.Rational(a + b, a * b))} per hour.", f"Time = 1 ÷ {T(sp.Rational(a + b, a * b))} = {T(t_)} hours."],
             [f"{T(sp.Rational(a + b, 2))} hours", f"{a + b} hours", f"{T(sp.Rational(a + b, a * b))} hours"], H(f"solve(Eq(t/{a} + t/{b}, 1), t)[0]"),
             why=["Averaged the two times", "Added the times", "Gave the combined rate instead of the time"], tags=["modeling"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Simplifying rational expressions", fams=[s1_simp, rr(CA1.s1_simplify)], extra=[err_of(s1_simp), err_of(rr(CA1.s1_simplify, tag="e")), open_of(s1_simp)]),
    2: dict(name="Multiplying and dividing rational expressions", fams=[s2_muldiv], extra=[err_of(s2_muldiv), open_of(s2_muldiv)]),
    3: dict(name="Adding and subtracting rational expressions", fams=[s3_addsub], extra=[err_of(s3_addsub), open_of(s3_addsub)]),
    4: dict(name="Solving rational equations", fams=[s4_solve], extra=[err_of(s4_solve), open_of(s4_solve)]),
    5: dict(name="Excluded values and extraneous solutions", fams=[s5_excluded, s5_extraneous], extra=[err_of(s5_excluded), err_of(s5_extraneous), open_of(s5_excluded)]),
    6: dict(name="Vertical and horizontal asymptotes", fams=[s6_ha, rr(F2.s12_asym)], extra=[err_of(s6_ha), err_of(rr(F2.s12_asym, tag="e")), open_of(s6_ha)]),
    7: dict(name="Graphing rational functions", fams=[s7_features], extra=[err_of(s7_features), open_of(s7_features)]),
    8: dict(name="Rational variation and modeling", fams=[rr(F2.s10_variation), s8_work], extra=[err_of(rr(F2.s10_variation, tag="e")), err_of(s8_work), open_of(s8_work)]),
}
