"""Calculus Unit 1 — Precalculus Review (precalculus-review)."""
from hslib import *
import pc_u02 as F2
import pc_u04 as F4

UNIT_ID = "precalculus-review"
ABBR = "pcr"


def rr(f, lv=(0, 1, 2), tag="c"):
    g = reuse(f, lv, tag)
    g.__name__ = "cal_" + f.__name__ + tag
    return g


# ============================================================== S1 Factoring and simplifying
@fam("012")
def s1_factor(r, L):
    kind = pick(r, ["trinomial", "dos", "gcf"] if L == 0 else ["trinomial", "dos", "cubes", "grouping"] if L == 1 else ["cubes", "grouping", "quartic", "trinomial"])
    if kind == "trinomial":
        a_ = 1 if L == 0 else pick(r, [1, 2, 3, 4, 6])
        p, q = r.sample(range(-9, 10), 2)
        c_ = pick(r, [1, 2, 3]) if a_ > 1 else 1
        e = sp.expand((c_ * x - p) * ((a_ // c_ if a_ % c_ == 0 else a_) * x - q))
    elif kind == "dos":
        a_, b_ = rint(r, 1, 6), rint(r, 1, 9)
        e = sp.expand((a_ * x) ** 2 - b_ ** 2)
    elif kind == "gcf":
        g = rint(r, 2, 6)
        e = sp.expand(g * x * (x + rint(r, -8, 8, True)))
    elif kind == "cubes":
        a_, b_ = rint(r, 1, 3), rint(r, 1, 5)
        e = sp.expand((a_ * x) ** 3 + pick(r, [1, -1]) * b_ ** 3)
    elif kind == "grouping":
        p, q = rint(r, -6, 6, True), rint(r, 1, 9)
        e = sp.expand((x ** 2 + pick(r, [q, -q])) * (x - p))
    else:
        p, q = r.sample([1, 4, 9, 16, 25], 2)
        e = sp.expand((x ** 2 - p) * (x ** 2 + q))
    f = sp.factor(e)
    need(f != e)
    ans = T(f)
    w = [T(sp.factor(sp.expand(e.subs(x, -x)))), T(sp.factor(e + 2 * e.coeff(x, 0))) if e.coeff(x, 0) else T(sp.factor(e + x)), T(sp.expand(e))]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Factor completely: {T(e)}", ans, ["Look for a GCF, then a pattern (trinomial, difference of squares, sum or difference of cubes, grouping).", f"{T(e)} = {ans}."],
             w, PY("factored", expr=T(e)), why=["Made sign errors in the factors", "Factored a different constant term", "Did not factor"])


@fam("012")
def s1_simplify(r, L):
    a, b = r.sample(range(-7, 8), 2)
    c = rint(r, -7, 7)
    num = sp.expand((x - a) * (x - b)) if L else sp.expand((x - a) * (x + a))
    den = sp.expand((x - a) * (x - c)) if L == 2 else (x - a)
    need(len({a, b, c}) == 3)
    simp = sp.cancel(num / den)
    ntxt, dtxt = T(num), T(den)
    ans = T(simp) + f", x ≠ {a}"
    w = [T(sp.cancel(num / den) + 2 * a) + f", x ≠ {a}", T(sp.simplify(num.subs(x, 0) / den.subs(x, 0))) if den.subs(x, 0) else T(simp + 1), T(simp)]
    return Q(f"Simplify ({ntxt})/({dtxt}) and state the excluded value from the original expression that cancels.", ans, [f"Factor: numerator {T(sp.factor(num))}, denominator {T(sp.factor(den))}.", f"Cancel (x - {a})." .replace("- -", "+ "),
                                                                                                                    f"{T(simp)}, with x ≠ {a}" + (f" (and x ≠ {c})" if L == 2 else "") + "."],
             w, PY("simp_rat", num=ntxt, den=dtxt, a=a), why=["Made a sign error while cancelling", "Cancelled terms instead of factors", "Forgot the excluded value"])


# ============================================================== S2 Exponential functions
@fam("012")
def s2_rules(r, L):
    a, b = rint(r, 2, 6), rint(r, -4, 6, True)
    c_ = rint(r, 2, 5)
    kind = pick(r, ["prod", "quot", "power"])
    if kind == "prod":
        e_txt = f"(e^({T(a * x)}))(e^({T(b * x)}))" if L else f"e^({a}x)·e^({b}x)"
        v = sp.exp((a + b) * x)
        w = [sp.exp(a * b * x * x), sp.exp(a * b * x), 2 * sp.exp((a + b) * x)]
    elif kind == "quot":
        e_txt = f"e^({T(a * x)}) ÷ e^({T(b * x)})"
        v = sp.exp((a - b) * x)
        need(a != b)
        w = [sp.exp(sp.Rational(a, b) * x), sp.exp((a + b) * x), sp.exp((b - a) * x)]
    else:
        e_txt = f"(e^({T(a * x)})){str(c_).translate(SUP)}"
        v = sp.exp(a * c_ * x)
        w = [sp.exp((a + c_) * x), sp.exp(a ** c_ * x), c_ * sp.exp(a * x)]
    return Q(f"Simplify {e_txt}.", T(v), ["Product: add exponents. Quotient: subtract exponents. Power: multiply exponents.", f"= {T(v)}."], [T(w_) for w_ in w], H(f"P('{e_txt.replace('÷', '/')}')"),
             why=["Multiplied (or divided) the exponents instead", "Used the wrong exponent rule", "Used the wrong exponent rule"])


@fam("012")
def s2_solve(r, L):
    b = pick(r, [2, 3, 5])
    k_ = rint(r, 1, 4)
    e1 = rint(r, 1, 3)
    c = rint(r, -5, 5)
    sol = sp.Rational(k_ * e1 - c, e1) if False else None
    # b^(x + c) = b^k  →  x = k - c
    rhs = sp.Integer(b) ** k_
    eq = f"{b}^(x {'+' if c >= 0 else '-'} {abs(c)}) = {rhs}" if c else f"{b}^x = {rhs}"
    if L == 2:
        eq = f"{b}^(2x {'+' if c >= 0 else '-'} {abs(c)}) = {rhs}"
        v = sp.Rational(k_ - c, 2)
    else:
        v = sp.Integer(k_ - c)
    return Q(f"Solve {eq}.", f"x = {T(v)}", [f"Write {rhs} as {b}{str(k_).translate(SUP)}.", "Set the exponents equal.", f"x = {T(v)}."], [f"x = {T(sp.Rational(rhs, b) - c)}", f"x = {T(v + 2 * c) if c else T(v + 1)}", f"x = {k_}"],
             H(f"solve(Eq(P('{eq.split(' = ')[0]}'), {rhs}), x)[0]"), why=["Divided by the base instead of rewriting the power", "Made a sign error", "Ignored the shift"])


# ============================================================== S3 Logarithmic functions
@fam("012")
def s3_props(r, L):
    kind = pick(r, ["expand", "condense", "eval"])
    a, b = rint(r, 2, 5), rint(r, 2, 4)
    if kind == "expand":
        e_txt = f"ln({a}x{str(b).translate(SUP)})" if L == 0 else f"ln(x{str(b).translate(SUP)} ÷ {a}y)" if False else f"ln((x{str(b).translate(SUP)})/(y{str(a).translate(SUP)}))"
        ans = f"ln({a}) + {b}ln(x)" if L == 0 else f"{b}ln(x) - {a}ln(y)"
        w = [f"{b}ln({a}x)", f"ln({a}) · {b}ln(x)", f"{a * b}ln(x)"] if L == 0 else [f"{b}ln(x) + {a}ln(y)", f"{b}ln(x) ÷ {a}ln(y)", f"ln({b}x) - ln({a}y)"]
        return Q(f"Expand {e_txt} using properties of logarithms.", ans, ["ln(MN) = ln M + ln N; ln(M ÷ N) = ln M - ln N; ln(Mᵖ) = p·ln M.", ans + "."], w,
                 PY("log_expand", src=e_txt, ans_vars=["x", "y"]), why=["Applied the power to the whole argument", "Multiplied the logs", "Combined incorrectly"])
    if kind == "condense":
        e_txt = f"{b}ln(x) - ln({a})" if L < 2 else f"{b}ln(x) + ln({a}) - ln(y)"
        ans = f"ln((x{str(b).translate(SUP)})/{a})" if L < 2 else f"ln(({a}x{str(b).translate(SUP)})/y)"
        w = [f"ln({b}x - {a})", f"ln(x{str(b).translate(SUP)} - {a})", f"ln({b}x/{a})"] if L < 2 else [f"ln({a}x{str(b).translate(SUP)}y)", f"ln({b}x + {a} - y)", f"ln(({a} + x{str(b).translate(SUP)})/y)"]
        return Q(f"Write {e_txt} as a single logarithm.", ans, ["Bring coefficients up as exponents.", "Sums become products; differences become quotients.", ans + "."], w,
                 PY("log_expand", src=ans, ans_vars=["x", "y"], rev=e_txt), why=["Kept the coefficient in front of x", "Subtracted inside the logarithm", "Mixed up the rules"])
    n_ = rint(r, -3, 4)
    e_txt = pick(r, [f"ln(e{str(n_).translate(SUP)})", f"e^(ln({a}))", f"ln(1)", f"log({10 ** abs(n_)})"])
    v = {f"ln(e{str(n_).translate(SUP)})": n_, f"e^(ln({a}))": a, "ln(1)": 0, f"log({10 ** abs(n_)})": abs(n_)}[e_txt]
    return Q(f"Evaluate {e_txt}.", str(v), ["ln and eˣ are inverse functions; log means base 10.", f"{e_txt} = {v}."], [str(v + 1), str(-v) if v else "1", "e" if v != "e" else "1"], H(f"P('{e_txt}')"),
             why=["Made an arithmetic error", "Made a sign error", "Did not simplify"])


@fam("12")
def s3_solve(r, L):
    a_, k_ = rint(r, 2, 9), rint(r, 2, 40)
    c_ = rint(r, 1, 4)
    v = sp.log(sp.Rational(k_, a_)) / c_
    eq = f"{a_}e^({c_ if c_ > 1 else ''}x) = {k_}"
    return Q(f"Solve {eq}. Give the exact answer and its value to the nearest thousandth.", f"x = {T(v)} ≈ {Rd(float(v), 3)}", [f"e^({c_ if c_ > 1 else ''}x) = {k_}/{a_}." if False else f"Divide by {a_}: e^({c_ if c_ > 1 else ''}x) = {T(sp.Rational(k_, a_))}.", f"Take ln: {c_ if c_ > 1 else ''}x = ln({T(sp.Rational(k_, a_))}).", f"x = {T(v)} ≈ {Rd(float(v), 3)}."],
             [f"x = {T(sp.log(k_ - a_) / c_) if k_ > a_ else T(sp.log(k_) / c_)} ≈ {Rd(float(sp.log(k_ - a_) / c_) if k_ > a_ else float(sp.log(k_) / c_), 3)}", f"x = {T(sp.log(k_) / (a_ * c_))} ≈ {Rd(float(sp.log(k_) / (a_ * c_)), 3)}", f"x = {T(c_ * sp.log(sp.Rational(k_, a_)))} ≈ {Rd(float(c_ * sp.log(sp.Rational(k_, a_))), 3)}"],
             PY("exact_approx", code=f"solve(Eq(P('{a_}e^({c_}x)'), {k_}), x)[0]", places=3), why=["Subtracted instead of dividing", "Divided ln by the product", "Multiplied by the coefficient"])


# ============================================================== S5 Representations
@fam("012")
def s5_aroc(r, L):
    kind = pick(r, ["table", "formula"]) if L < 2 else "formula"
    if kind == "table":
        xs = sorted(r.sample(range(-3, 12), 4))
        ys = [rint(r, -20, 40) for _ in xs]
        i, j = sorted(r.sample(range(4), 2))
        v = sp.Rational(ys[j] - ys[i], xs[j] - xs[i])
        tbl = "; ".join(f"f({a}) = {b}" for a, b in zip(xs, ys))
        return Q(f"Use the table ({tbl}) to find the average rate of change of f from x = {xs[i]} to x = {xs[j]}.", T(v), ["Average rate of change = (f(b) - f(a)) ÷ (b - a).", f"({ys[j]} - {par(ys[i])}) ÷ ({xs[j]} - {par(xs[i])}) = {T(v)}."],
                 [T(sp.Rational(xs[j] - xs[i], ys[j] - ys[i])) if ys[j] != ys[i] else "undefined", T(sp.Rational(ys[j] + ys[i], xs[j] - xs[i])), str(ys[j] - ys[i])], H(f"Rational({ys[j]} - ({ys[i]}), {xs[j]} - ({xs[i]}))"),
                 why=["Inverted the ratio", "Added the outputs", "Forgot to divide by the change in x"])
    f = pick(r, [rint(r, -3, 3, True) * x ** 2 + rint(r, -5, 5) * x, x ** 3 - rint(r, 0, 4) * x, sp.sqrt(x), 1 / x, sp.Integer(2) ** x] if L else [rint(r, -3, 3, True) * x ** 2 + rint(r, -5, 5) * x + rint(r, -5, 5)])
    a, b = sorted(r.sample(range(1, 9), 2))
    if f == sp.sqrt(x):
        a, b = pick(r, [(1, 4), (4, 9), (1, 9), (0, 4), (9, 16), (0, 1)])
    v = sp.Rational(1, 1) * (f.subs(x, b) - f.subs(x, a)) / (b - a)
    ft = T(f) if f != sp.Integer(2) ** x else "2ˣ"
    return Q(f"Find the average rate of change of f(x) = {ft} on [{a}, {b}].", T(sp.nsimplify(v)), [f"f({b}) = {T(f.subs(x, b))}, f({a}) = {T(f.subs(x, a))}.", f"({T(f.subs(x, b))} - {par(f.subs(x, a)) if f.subs(x, a).is_Integer else '(' + T(f.subs(x, a)) + ')'}) ÷ ({b} - {a}) = {T(sp.nsimplify(v))}."],
             [T(sp.nsimplify((f.subs(x, b) + f.subs(x, a)) / (b - a))), T(sp.nsimplify(f.subs(x, b) - f.subs(x, a))), T(sp.nsimplify((b - a) / (f.subs(x, b) - f.subs(x, a)))) if f.subs(x, b) != f.subs(x, a) else "0"],
             H(f"(P('{ft}').subs(x, {b}) - P('{ft}').subs(x, {a}))/({b} - {a})"), why=["Added the outputs", "Forgot to divide by b - a", "Inverted the ratio"])


@fam("012")
def s5_graph(r, L):
    pts = sorted(r.sample(range(-5, 6), 4))
    ys = [rint(r, -5, 5) for _ in pts]
    need(len(set(ys)) > 2)
    i, j = sorted(r.sample(range(4), 2))
    v = sp.Rational(ys[j] - ys[i], pts[j] - pts[i])
    xs_, ys_ = [float(p_) for p_ in pts], [float(q_) for q_ in ys]
    return Q(f"The graph of f is made of line segments through the marked points. Find the average rate of change of f on [{pts[i]}, {pts[j]}].", T(v),
             [f"Read f({pts[i]}) = {ys[i]} and f({pts[j]}) = {ys[j]}.", f"({ys[j]} - {par(ys[i])}) ÷ ({pts[j]} - {par(pts[i])}) = {T(v)}."],
             [T(sp.Rational(pts[j] - pts[i], ys[j] - ys[i])) if ys[j] != ys[i] else "1", str(ys[j] - ys[i]), T(-v) if v else "1"], H(f"Rational({ys[j]} - ({ys[i]}), {pts[j]} - ({pts[i]}))"),
             why=["Inverted the ratio", "Forgot to divide by the change in x", "Made a sign error"],
             diagram={"alt": "Piecewise linear graph through " + ", ".join(f"({a}, {b})" for a, b in zip(pts, ys)) + ".", "draw": curve_draw([(xs_, ys_, "solid")], (-6, 6), (-6, 6), pts=[(a, b, "") for a, b in zip(pts, ys)], label_every=1)})


@fam("012", mode="mc")
def s1_gcf(r, L):
    g = rint(r, 2, 9)
    m1, m2 = r.sample([2, 3, 5, 7], 2)
    e1, e2 = rint(r, 1, 5), rint(r, 1, 5)
    t1, t2 = g * m1 * x ** e1, g * m2 * x ** e2
    v = g * x ** min(e1, e2)
    return Q(f"Find the greatest common factor of {T(t1)} and {T(t2)}.", T(v), ["GCF of the coefficients and the lowest power of x.", f"GCF = {T(v)}."], [T(g * x ** max(e1, e2)), T(g * m1 * m2 * x ** min(e1, e2)), T(x ** min(e1, e2))],
             H(f"gcd(P('{T(t1)}'), P('{T(t2)}'))"), why=["Used the highest power", "Multiplied the coefficients", "Forgot the numerical factor"])


SKILLS = {
    1: dict(name="Factoring and Simplifying Expressions", std=["A-SSE.A.2", "A-APR.D.6"], fams=[s1_factor, s1_simplify, s1_gcf], extra=[err_of(s1_factor), open_of(s1_factor)]),
    2: dict(name="Exponential Functions", std=["F-LE.A.1", "F-IF.C.8b"], fams=[s2_rules, s2_solve, rr(F2.s15_exp), rr(F2.s16_e), mc_of(s2_solve)], extra=[err_of(s2_solve), open_of(s2_rules)]),
    3: dict(name="Logarithmic Functions", std=["F-LE.A.4", "F-BF.B.5"], fams=[s3_props, s3_solve, rr(F2.s17_log), mc_of(rr(F2.s17_log, tag='q'))], extra=[err_of(s3_props), open_of(rr(F2.s17_log, tag="o"))]),
    4: dict(name="Unit Circle and Exact Trigonometric Values", std=["F-TF.A.2", "F-TF.A.3"], fams=[rr(F4.s2_exact), rr(F4.s1_point), rr(F4.s9_solve)], extra=[err_of(rr(F4.s2_exact, tag="e")), open_of(rr(F4.s2_exact, tag="o"))]),
    5: dict(name="Graphical, Numerical, and Algebraic Representations", std=["F-IF.B.6", "F-IF.C.9"], fams=[s5_aroc, s5_graph, mc_of(s5_aroc)], extra=[err_of(s5_aroc), open_of(s5_aroc)]),
}
