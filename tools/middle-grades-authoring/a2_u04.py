"""Algebra 2 Unit 4 — Polynomial Functions (polynomial-functions). Top-up families."""
from hslib import *
import pc_u02 as F2
import pc_u07 as V7
import ca_u01 as CA1

UNIT_ID = "polynomial-functions"
ABBR = "pf"
cx = V7.cx
I = sp.I


def ri(r, a, b):
    return rint(r, a, b, True)


def rpoly(r, deg, lo=-9, hi=9):
    cs = [ri(r, -5, 5)] + [rint(r, lo, hi) for _ in range(deg)]
    return sum(c * x ** (deg - i) for i, c in enumerate(cs))


# ============================================================== S1 Polynomial operations
@fam("012")
def s1_addsub(r, L):
    p, q = rpoly(r, 2 + (L == 2)), rpoly(r, 2)
    op = pick(r, ["+", "-"])
    res = sp.expand(p + q if op == "+" else p - q)
    need(len(sp.Poly(res, x).terms()) >= 2)
    wr = [T(sp.expand(p + q if op == "-" else p - q)), T(sp.expand(p - q.subs(x, x) + 2 * q.coeff(x, 0))) if op == "-" else T(sp.expand(p + q - 2 * q.coeff(x, 0))),
          T(sp.expand(p + q * (-1 if op == "-" else 1) + (q.coeff(x, 1) * x * (2 if op == "-" else -2))))]
    need(len(set(wr) | {T(res)}) == 4)
    return Q(f"Simplify ({T(p)}) {op} ({T(q)}).", T(res),
             ["Distribute the sign to every term of the second polynomial." if op == "-" else "Remove the parentheses.", "Combine like terms.", f"{T(res)}."],
             wr, H(f"expand(P('{T(p)}') {op} P('{T(q)}'))"),
             why=["Used the wrong operation" if op == "+" else "Added instead of subtracting", "Did not distribute the subtraction to the last term" if op == "-" else "Made a sign error on the constant",
                  "Did not distribute the subtraction to the x-term" if op == "-" else "Made a sign error on the x-term"])


@fam("012")
def s1_mult(r, L):
    a, b = ri(r, -6, 6), ri(r, -6, 6)
    p = (x + a) if L == 0 else (ri(r, -3, 3) * x + a)
    q = (x + b) if L == 0 else rpoly(r, 2, -6, 6)
    res = sp.expand(p * q)
    wr = [T(sp.expand(sp.Poly(p, x).LC() * sp.Poly(q, x).LC() * x ** (sp.degree(q, x) + 1) + p.coeff(x, 0) * q.coeff(x, 0))),
          T(sp.expand(p * q - 2 * p.coeff(x, 0) * q.coeff(x, 0))), T(sp.expand(p * q + (x if sp.degree(q, x) == 1 else x ** 2)))]
    need(len(set(wr) | {T(res)}) == 4)
    return Q(f"Multiply and simplify: ({T(p)})({T(q)}).", T(res),
             ["Multiply each term of the first polynomial by each term of the second.", "Combine like terms.", f"{T(res)}."],
             wr, H(f"expand(P('{T(p)}')*P('{T(q)}'))"),
             why=["Multiplied only the first terms and the last terms", "Made a sign error on the constant term", "Combined unlike terms incorrectly"])


# ============================================================== S2 Special products and factoring
@fam("012")
def s2_special(r, L):
    a, b = (1 if L == 0 else rint(r, 1, 4)), rint(r, 1, 9)
    kind = pick(r, ["sq+", "sq-", "conj"] if L < 2 else ["sq+", "sq-", "conj", "cube"])
    if kind == "sq+":
        e, txt = (a * x + b) ** 2, f"({T(a * x + b)})²"
        wr = [T(a * a * x ** 2 + b * b), T(sp.expand((a * x + b) ** 2) - a * b * x), T(a * a * x ** 2 + 2 * b * x + b * b) if a != 1 else T(x ** 2 + b * x + 2 * b)]
        why = ["Squared each term and left out the middle term", "Did not double the middle term", "Forgot to multiply the middle term by the coefficient of x" if a != 1 else "Mixed up the middle and last terms"]
    elif kind == "sq-":
        e, txt = (a * x - b) ** 2, f"({T(a * x - b)})²"
        wr = [T(a * a * x ** 2 - b * b), T(sp.expand((a * x - b) ** 2) + 4 * a * b * x), T(a * a * x ** 2 - a * b * x + b * b)]
        why = ["Squared each term and kept the minus sign", "Made the middle term positive", "Did not double the middle term"]
    elif kind == "conj":
        e, txt = (a * x + b) * (a * x - b), f"({T(a * x + b)})({T(a * x - b)})"
        wr = [T(a * a * x ** 2 + b * b), T(sp.expand((a * x - b) ** 2)), T(a * a * x ** 2 - 2 * b)]
        why = ["Made the last term positive", "Squared the difference instead", "Doubled b instead of squaring it"]
    else:
        e, txt = (a * x + b) ** 3, f"({T(a * x + b)})³"
        wr = [T(a ** 3 * x ** 3 + b ** 3), T(sp.expand((a * x + b) ** 2 * (a * x - b))), T(sp.expand(a ** 3 * x ** 3 + 3 * a * a * b * x ** 2 + b ** 3))]
        why = ["Cubed each term and left out the middle terms", "Multiplied by the conjugate in the last step", "Left out the x term"]
    res = sp.expand(e)
    need(len(set(wr) | {T(res)}) == 4)
    return Q(f"Expand: {txt}", T(res), ["Use the special-product pattern: (a ± b)² = a² ± 2ab + b², (a + b)(a - b) = a² - b², (a + b)³ = a³ + 3a²b + 3ab² + b³.", f"{txt} = {T(res)}."],
             wr, H(f"expand(P('{txt}'))"), why=why)


# ============================================================== S3 Long and synthetic division
@fam("012")
def s3_divide(r, L):
    a = ri(r, -5, 5)
    deg = 2 if L == 0 else 3
    qq = rpoly(r, deg - 1, -6, 6)
    rem = 0 if (L == 0 and r.random() < 0.5) else rint(r, -9, 9)
    f = sp.expand(qq * (x - a) + rem)
    need(len(sp.Poly(f, x).all_coeffs()) == deg + 1)
    ans = T(qq) + (f", remainder {rem}" if True else "")
    wr = [T(sp.expand(sp.quo(f, x + a))) + f", remainder {T(sp.rem(f, x + a))}", T(qq) + f", remainder {-rem}" if rem else T(qq) + ", remainder 1",
          T(sp.expand(qq + rem)) + ", remainder 0" if rem else T(sp.expand(qq * x)) + ", remainder 0"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Divide ({T(f)}) ÷ ({T(x - a)}). Give the quotient and the remainder.", ans,
             [f"Use synthetic division with {a} (the zero of {T(x - a)}).", f"Bring down, multiply by {a}, and add across the coefficients {', '.join(str(c) for c in sp.Poly(f, x).all_coeffs())}.",
              f"Quotient {T(qq)}, remainder {rem}."],
             wr, PY("divres", f=T(f), d=T(x - a)),
             why=["Used the opposite sign in synthetic division", "Made a sign error in the last step", "Added the remainder to the quotient"])


# ============================================================== S5 Zeros and multiplicities
@fam("012")
def s5_mult(r, L):
    zs = r.sample([v for v in range(-6, 7) if v], 3 if L else 2)
    ms = [rint(r, 1, 3) for _ in zs]
    need(len(set(ms)) > 1)
    c = ri(r, -3, 3) if L == 2 else 1
    txt = (str(c) if c not in (1, -1) else "-" if c == -1 else "") + "".join(f"({T(x - z)})" + (str(m).translate(SUP) if m > 1 else "") for z, m in zip(zs, ms))
    txt = "x" + txt[txt.index("(x)") + 3:] if "(x)" in txt and False else txt
    i = r.randrange(len(zs))
    ask = pick(r, ["mult", "behavior"] if L else ["mult"])
    if ask == "mult":
        ans = str(ms[i])
        wr = [str(ms[(i + 1) % len(ms)]) if ms[(i + 1) % len(ms)] != ms[i] else str(ms[i] + 1), str(-zs[i]) if -zs[i] != ms[i] else str(ms[i] + 2), str(sum(ms)) if sum(ms) != ms[i] else str(ms[i] + 3)]
        need(len(set(wr) | {ans}) == 4)
        return Q(f"For f(x) = {txt}, what is the multiplicity of the zero x = {zs[i]}?", ans,
                 [f"The factor {T(x - zs[i])} appears with exponent {ms[i]}.", f"The multiplicity of x = {zs[i]} is {ms[i]}."],
                 wr, PY("multiplicity", f=txt, z=zs[i]), why=["Read the exponent of a different factor", "Used the zero instead of its exponent", "Used the degree of the polynomial"])
    ans = "touches (bounces)" if ms[i] % 2 == 0 else "crosses"
    other = "crosses" if ans != "crosses" else "touches (bounces)"
    return Q(f"For f(x) = {txt}, does the graph cross the x-axis or touch it and turn around at x = {zs[i]}?", ans,
             [f"The multiplicity of x = {zs[i]} is {ms[i]}.", "Odd multiplicity → crosses; even multiplicity → touches and turns.", f"The graph {ans} at x = {zs[i]}."],
             [other, "neither: the graph does not reach the x-axis there", "it is a vertical asymptote"], PY("cross_touch", f=txt, z=zs[i]),
             why=["Mixed up the odd and even rules", "Did not recognize a zero of the polynomial", "Confused a zero with an asymptote"])


# ============================================================== S6 Graphing polynomial functions
END = {(1, 1): "As x → ∞, f(x) → ∞; as x → -∞, f(x) → ∞", (1, -1): "As x → ∞, f(x) → ∞; as x → -∞, f(x) → -∞",
       (-1, 1): "As x → ∞, f(x) → -∞; as x → -∞, f(x) → -∞", (-1, -1): "As x → ∞, f(x) → -∞; as x → -∞, f(x) → ∞"}


@fam("012")
def s6_end(r, L):
    deg = rint(r, 2, 5)
    f = rpoly(r, deg) if L else ri(r, -4, 4) * x ** deg + rint(r, -9, 9) * x + rint(r, -9, 9)
    if L == 2 and r.random() < 0.5:
        f = sp.expand(ri(r, -3, 3) * x * (x - rint(r, -4, 4)) * (x ** 2 + rint(r, 1, 5)) if deg > 3 else f)
        deg = sp.degree(f, x)
    lc = sp.sign(sp.Poly(f, x).LC())
    key = (int(lc), 1 if deg % 2 == 0 else -1)
    ans = END[key]
    wr = [v for k, v in END.items() if k != key]
    whys = {k: w for k, w in zip([(-key[0], key[1]), (key[0], -key[1]), (-key[0], -key[1])],
                                 ["Ignored the sign of the leading coefficient", "Mixed up even and odd degree", "Reversed both ends"])}
    order = [(-key[0], key[1]), (key[0], -key[1]), (-key[0], -key[1])]
    return Q(f"Describe the end behavior of f(x) = {T(f)}.", ans,
             [f"Leading term: {T(sp.Poly(f, x).LC() * x ** sp.degree(f, x))}.", f"Degree {deg} is {'even' if deg % 2 == 0 else 'odd'}; the leading coefficient is {'positive' if lc > 0 else 'negative'}.", ans + "."],
             [END[k] for k in order], PY("end_behavior", f=T(f)), why=[whys[k] for k in order])


@fam("012", mode="mc")
def s6_turning(r, L):
    deg = rint(r, 3, 6)
    f = rpoly(r, deg)
    ask = pick(r, ["turn", "zeros"])
    v = deg - 1 if ask == "turn" else deg
    opts = [(str(v), True)] + [(str(w), False) for w in (v + 1, v - 1, 2 * deg if 2 * deg not in (v, v + 1, v - 1) else v + 2)]
    return Q(f"What is the greatest possible number of {'turning points' if ask == 'turn' else 'real zeros'} of the graph of f(x) = {T(f)}?", str(v),
             [f"The degree is {deg}.", f"A degree-n polynomial has at most {'n - 1 turning points' if ask == 'turn' else 'n real zeros'}: {v}."],
             options=opts, chk=H(f"degree(P('{T(f)}'), x) - {1 if ask == 'turn' else 0}"), mode="mc")


# ============================================================== S7 Fundamental theorem of algebra
@fam("012")
def s7_build(r, L):
    if L == 0:
        zs = r.sample(range(-6, 7), 2 + (r.random() < 0.5))
        f = sp.expand(sp.prod([x - z for z in zs]))
        desc = ", ".join(map(str, zs[:-1])) + f", and {zs[-1]}" if len(zs) > 2 else f"{zs[0]} and {zs[1]}"
        wr = [T(sp.expand(sp.prod([x + z for z in zs]))), T(sp.expand(sp.prod([x - z for z in zs]) + 2 * sp.prod([-z for z in zs]))) if sp.prod(zs) else T(sp.expand(f + 1)), T(sp.expand(f - x ** len(zs) + 2 * x ** len(zs)))]
        why = ["Used factors (x + r) for zeros r", "Made a sign error on the constant term", "Used the wrong leading coefficient"]
        code = "expand(" + "*".join(f"(x - ({z}))" for z in zs) + ")"
    else:
        a = rint(r, -5, 5)
        p, q = rint(r, -4, 4), rint(r, 1, 4)
        kind = pick(r, ["complex", "radical"]) if L == 2 else "complex"
        if kind == "complex":
            z = p + q * I
            f = sp.expand((x - a) * (x ** 2 - 2 * p * x + p * p + q * q))
            desc = f"{a} and {cx(z)}"
            code = f"expand((x - ({a}))*(x - P('{cx(z)}'))*(x - conjugate(P('{cx(z)}'))))"
        else:
            m = pick(r, [2, 3, 5, 7])
            f = sp.expand((x - a) * ((x - p) ** 2 - m))
            desc = f"{a} and {p} + √{m}" if p else f"{a} and √{m}"
            code = f"expand((x - ({a}))*(x - P('{p} + √{m}'))*(x - ({p}) + sqrt({m})))"
        wr = [T(sp.expand((x - a) * (x - p) ** 2)), T(sp.expand((x + a) * sp.expand(f / (x - a)) if a else f + x)), T(sp.expand(f + 2 * (f.coeff(x, 1)) * x)) if f.coeff(x, 1) else T(f + x)]
        why = ["Left out the conjugate zero", "Used the factor (x + a) for the zero a", "Made a sign error in the x-term"]
    ans = T(f)
    need(len(set(wr) | {ans}) == 4)
    q = f"Write a polynomial function of least degree with leading coefficient 1 and zeros {desc}." if L == 0 else \
        f"Write a polynomial function of least degree with rational coefficients and leading coefficient 1 that has zeros {desc}."
    return Q(q, "f(x) = " + ans,
             ["Each zero r gives a factor (x - r)." + (" Irrational and complex zeros come in conjugate pairs, so include the conjugate too." if L else ""), "Multiply the factors.", f"f(x) = {ans}."],
             ["f(x) = " + w for w in wr], H(code), why=why)


@fam("012")
def s7_count(r, L):
    deg = rint(r, 2, 7)
    f = rpoly(r, deg)
    kind = pick(r, ["complex", "conj"] if L else ["complex"])
    if kind == "complex":
        return Q(f"How many complex zeros (counting multiplicity) does f(x) = {T(f)} have?", str(deg),
                 ["By the Fundamental Theorem of Algebra, a degree-n polynomial has exactly n complex zeros, counting multiplicity.", f"The degree is {deg}, so there are {deg}."],
                 [str(deg - 1), str(len(sp.Poly(f, x).terms())) if len(sp.Poly(f, x).terms()) not in (deg, deg - 1) else str(deg + 1), str(2 * deg)], H(f"degree(P('{T(f)}'), x)"),
                 why=["Counted turning points instead of zeros", "Counted the terms", "Doubled the degree"])
    p, q = ri(r, -6, 6), rint(r, 1, 6)
    z = p + q * I
    return Q(f"A polynomial with real coefficients has {cx(z)} as a zero. What other number must be a zero?", cx(sp.conjugate(z)),
             ["Complex zeros of a polynomial with real coefficients come in conjugate pairs.", f"The conjugate of {cx(z)} is {cx(sp.conjugate(z))}."],
             [cx(-z), cx(-sp.conjugate(z)), cx(q + p * I)], H(f"conjugate(P('{cx(z)}'))"),
             why=["Negated the whole number instead of only the imaginary part", "Negated only the real part", "Switched the real and imaginary parts"])


# ============================================================== S8 Polynomial equations and applications
@fam("012")
def s8_solve(r, L):
    kind = pick(r, ["gcf", "group"] if L < 2 else ["group", "quartic"])
    if kind == "gcf":
        p_, q_ = r.sample(range(-7, 8), 2)
        need(p_ and q_)
        c = rint(r, 1, 3)
        f = sp.expand(c * x * (x - p_) * (x - q_))
        sols = sorted({0, p_, q_})
        why = ["Divided both sides by x and lost the solution x = 0", "Used the wrong signs", "Gave only one solution"]
        wr = [" or ".join(f"x = {v}" for v in sorted({p_, q_})), " or ".join(f"x = {-v}" for v in sols), f"x = {max(p_, q_)}"]
    elif kind == "group":
        a = ri(r, -6, 6)
        m = pick(r, [1, 4, 9, 16, 25])
        f = sp.expand((x - a) * (x ** 2 - m))
        sols = sorted({a, int(sp.sqrt(m)), -int(sp.sqrt(m))})
        why = ["Forgot the negative square root", "Used the wrong signs", "Gave only the solution from the linear factor"]
        wr = [" or ".join(f"x = {v}" for v in sorted({a, int(sp.sqrt(m))})), " or ".join(f"x = {-v}" for v in sols), f"x = {a}"]
    else:
        m1, m2 = r.sample([1, 4, 9, 16], 2)
        f = sp.expand((x ** 2 - m1) * (x ** 2 - m2))
        sols = sorted({int(sp.sqrt(m1)), -int(sp.sqrt(m1)), int(sp.sqrt(m2)), -int(sp.sqrt(m2))})
        why = ["Gave only the positive solutions", "Solved for x² instead of x", "Gave the solutions of only one factor"]
        wr = [" or ".join(f"x = {v}" for v in sols if v > 0), f"x = {m1} or x = {m2}", f"x = {-int(sp.sqrt(m1))} or x = {int(sp.sqrt(m1))}"]
    ans = " or ".join(f"x = {v}" for v in sols)
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve {T(f)} = 0.", ans, ["Factor completely (GCF, grouping, or quadratic form).", "Set each factor equal to 0.", f"{ans}."], wr, H(f"solve(P('{T(f)}'), x)", "set"), why=why)


@fam("012")
def s8_box(r, L):
    Lg, W = pick(r, [(20, 16), (24, 18), (30, 20), (16, 12), (18, 14), (40, 30)])
    c = rint(r, 1, min(W // 2 - 1, 6))
    V = c * (Lg - 2 * c) * (W - 2 * c)
    if L < 2:
        return Q(f"An open box is made from a {Lg}-inch by {W}-inch sheet by cutting x-inch squares from each corner, so V(x) = x({Lg} - 2x)({W} - 2x). Find the volume when x = {c}.", f"{V} cubic inches",
                 [f"V({c}) = {c}({Lg} - {2 * c})({W} - {2 * c}).", f"= {c}({Lg - 2 * c})({W - 2 * c}) = {V}."],
                 [f"{c * (Lg - c) * (W - c)} cubic inches", f"{(Lg - 2 * c) * (W - 2 * c)} cubic inches", f"{c * Lg * W} cubic inches"], H(f"P('x({Lg} - 2x)({W} - 2x)').subs(x, {c})"),
                 why=["Subtracted only one square from each side", "Forgot to multiply by the height x", "Did not subtract the cut squares"], tags=["modeling"])
    return Q(f"An open box is made from a {Lg}-inch by {W}-inch sheet by cutting x-inch squares from each corner. Write V(x) in standard form.", f"V(x) = {T(sp.expand(x * (Lg - 2 * x) * (W - 2 * x)))}",
             [f"Length {Lg} - 2x, width {W} - 2x, height x.", f"V(x) = x({Lg} - 2x)({W} - 2x).", f"Expand: {T(sp.expand(x * (Lg - 2 * x) * (W - 2 * x)))}."],
             [f"V(x) = {T(sp.expand(x * (Lg - x) * (W - x)))}", f"V(x) = {T(sp.expand((Lg - 2 * x) * (W - 2 * x)))}", f"V(x) = {T(sp.expand(x * (Lg - 2 * x) * (W - 2 * x) + 4 * x ** 3))}"],
             H(f"expand(x*({Lg} - 2*x)*({W} - 2*x))"), why=["Subtracted only one square from each side", "Forgot the height", "Made a sign error on the x³ term"], tags=["modeling"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Polynomial operations", fams=[s1_addsub, s1_mult], extra=[err_of(s1_addsub), err_of(s1_mult), open_of(s1_mult), select_of(s1_addsub)]),
    2: dict(name="Special products and factoring", fams=[s2_special, rr(CA1.s1_factor, (1, 1, 2))], extra=[err_of(s2_special), err_of(rr(CA1.s1_factor, (1, 1, 2), "e")), open_of(s2_special)]),
    3: dict(name="Long division and synthetic division", fams=[s3_divide], extra=[err_of(s3_divide), open_of(s3_divide)]),
    4: dict(name="Remainder and factor theorems", fams=[rr(F2.s13_remainder), rr(F2.s13_find_k, (1, 1, 2))], extra=[err_of(rr(F2.s13_remainder, tag="e")), open_of(rr(F2.s13_remainder, tag="o"))]),
    5: dict(name="Zeros and multiplicities", fams=[s5_mult, rr(F2.s14_zeros)], extra=[err_of(s5_mult), err_of(rr(F2.s14_zeros, tag="e")), open_of(rr(F2.s14_zeros, tag="o"))]),
    6: dict(name="Graphing polynomial functions", fams=[s6_end, s6_turning], extra=[err_of(s6_end), open_of(s6_end)]),
    7: dict(name="Fundamental theorem of algebra", fams=[s7_build, s7_count], extra=[err_of(s7_build), err_of(s7_count), open_of(s7_count)]),
    8: dict(name="Polynomial equations and applications", fams=[s8_solve, s8_box], extra=[err_of(s8_solve), err_of(s8_box), open_of(s8_solve)]),
}
