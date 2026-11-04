"""Calculus Unit 6 — Fundamental Theorem of Calculus (fundamental-theorem-calculus)."""
from hslib import *
import ca_u05 as C5

UNIT_ID = "fundamental-theorem-calculus"
ABBR = "ftc"
integ = C5.integ


def pl_points(r):
    pts = [(-4, rint(r, -3, 3))]
    for xv in (-2, 0, 2, 4):
        pts.append((xv, rint(r, -3, 3)))
    return pts


def pl_expr(pts):
    return sp.Piecewise(*[((y0 + sp.Rational(y1 - y0, x1 - x0) * (x - x0)), x <= x1) for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:])])


def pl_draw(pts, ylab="f"):
    xs_, ys_ = [float(p_[0]) for p_ in pts], [float(p_[1]) for p_ in pts]
    return curve_draw([(xs_, ys_, "solid")], (-5, 5), (-5, 5), pts=[(p_[0], p_[1], "") for p_ in pts], label_every=1)


def pw(e):
    s_ = T(e)
    return f"({s_})" if " " in s_ else s_


def sign_set(pts, sgn):
    """Open set (as a sympy Union) inside (-4, 4) where the piecewise linear f has the given sign."""
    out = sp.S.EmptySet
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        y0s, y1s = sgn * y0, sgn * y1
        if y0s > 0 and y1s > 0:
            out = out | sp.Interval.open(x0, x1)
        elif y0s > 0 and y1s <= 0:
            out = out | sp.Interval.open(x0, x0 + sp.Rational(y0, y0 - y1) * (x1 - x0))
        elif y0s <= 0 and y1s > 0:
            out = out | sp.Interval.open(x0 + sp.Rational(-y0, y1 - y0) * (x1 - x0) if y0 != y1 else x0, x1)
    # merge across shared endpoints where f stays positive
    for (xv, yv) in pts[1:-1]:
        if sgn * yv > 0:
            out = out | sp.FiniteSet(xv)
    return sp.simplify(out)


def zero_xs(pts):
    zs = set()
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        if y0 == 0:
            zs.add(sp.Integer(x0))
        if y0 * y1 < 0:
            zs.add(x0 + sp.Rational(-y0, y1 - y0) * (x1 - x0))
    if pts[-1][1] == 0:
        zs.add(sp.Integer(pts[-1][0]))
    return sorted(zs)


# ============================================================== S1 Connecting differentiation and integration
@fam("012")
def s1_net(r, L):
    a, b = sorted(r.sample(range(-3, 9), 2))
    fa, fb = rint(r, -20, 20), rint(r, -20, 20)
    kind = pick(r, ["net", "find_fb"]) if L else "net"
    if kind == "net":
        return Q(f"f is differentiable with f({a}) = {fa} and f({b}) = {fb}. Find ∫ from {a} to {b} f′(x) dx.", str(fb - fa), ["FTC: ∫ from a to b f′(x) dx = f(b) - f(a).", f"{fb} - {par(fa)} = {fb - fa}."],
                 [str(fa - fb), str(fb + fa), str(sp.Rational(fb - fa, b - a)) if (fb - fa) % (b - a) == 0 and (fb - fa) // (b - a) != fb - fa else str(fb)], PY("ftc_net", a=a, b=b, fa=fa, fb=fb),
                 why=["Subtracted in the wrong order", "Added the values", "Divided by the length of the interval"])
    I_ = rint(r, -15, 15, True)
    return Q(f"f({a}) = {fa} and ∫ from {a} to {b} f′(x) dx = {I_}. Find f({b}).", str(fa + I_), ["f(b) = f(a) + ∫ from a to b f′(x) dx.", f"{fa} + {par(I_)} = {fa + I_}."],
             [str(I_ - fa), str(fa - I_), str(I_)], PY("ftc_net2", fa=fa, I=I_), why=["Subtracted f(a)", "Subtracted the integral", "Forgot the starting value"])


@fam("012", mode="mc")
def s1_ftc1(r, L):
    a = rint(r, -3, 3)
    g = pick(r, ["cos(t²)", "√(1 + t³)", "e^(-t²)", "sin(t)/t", "ln(1 + t²)", "1/(1 + t⁴)"])
    good = g.replace("t", "x")
    bad = [g.replace("t", "x").replace("x", "x", 1) + f" - {g.replace('t', str(a)) if a else g.replace('t', '0')}" if False else f"{g.replace('t', 'x')} - {g.replace('t', '(' + str(a) + ')')}" if a else f"{g.replace('t', 'x')} - {g.replace('t', '0')}",
           f"∫ {g.replace('t', 'x')} dx", "0"]
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Find d/dx [∫ from {a} to x {g} dt].", good, ["FTC Part 1: d/dx ∫ from a to x f(t) dt = f(x).", good + "."], options=opts, chk=PY("ftc1", g=g, a=a), mode="mc")


# ============================================================== S2 Accumulation functions
@fam("012")
def s2_accum(r, L):
    pts = pl_points(r)
    start = pick(r, [-4, 0, -2])
    k_ = pick(r, [v for v in (-4, -2, 0, 2, 4) if v != start])
    f = pl_expr(pts)
    v = sp.integrate(f, (x, start, k_))
    absv = sp.integrate(sp.Abs(f), (x, min(start, k_), max(start, k_)))
    need(absv != abs(v))
    return Q(f"The graph of f is made of line segments through the marked points. Let g(x) = ∫ from {start} to x f(t) dt. Find g({k_}).", T(v),
             [f"g({k_}) = ∫ from {start} to {k_} f(t) dt.", "Add signed areas of triangles and trapezoids" + (" (the upper limit is less than the lower, so negate)." if k_ < start else "."), f"g({k_}) = {T(v)}."],
             [T(absv if k_ > start else -absv), T(-v) if v else "1", str(pts[[p_[0] for p_ in pts].index(k_)][1]) if str(pts[[p_[0] for p_ in pts].index(k_)][1]) != T(v) else T(v + 1)],
             PY("pl_integral", pts=[list(p_) for p_ in pts], a=start, b=k_), why=["Treated area below the axis as positive", "Made a sign error with the limits", "Gave f instead of g"],
             diagram={"alt": "Piecewise linear graph of f through " + ", ".join(f"({p_[0]}, {p_[1]})" for p_ in pts) + ".", "draw": pl_draw(pts)})


@fam("012")
def s2_formula(r, L):
    a = rint(r, 0, 3)
    c2, c1 = rint(r, -3, 3, True), rint(r, -5, 5)
    f = 3 * c2 * t ** 2 + 2 * c1 * t + rint(r, -4, 4)
    G = sp.integrate(f, (t, a, x))
    ans = T(sp.expand(G))
    return Q(f"Find a formula for g(x) = ∫ from {a} to x ({T(f)}) dt.", "g(x) = " + ans, [f"Antiderivative: {T(sp.integrate(f, t))}.", f"Evaluate from {a} to x.", "g(x) = " + ans + "."],
             ["g(x) = " + T(sp.integrate(f, t).subs(t, x)), "g(x) = " + T(sp.diff(f, t).subs(t, x)), "g(x) = " + T(f.subs(t, x))], H(f"integrate(P('{T(f)}').subs(t, Symbol('s_')), (Symbol('s_'), {a}, x))"),
             why=["Forgot to subtract the value at the lower limit", "Differentiated instead", "Gave the integrand"])


# ============================================================== S3 Analyzing functions defined by integrals
@fam("012")
def s3_analyze(r, L):
    pts = pl_points(r)
    need(sum(1 for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]) if y0 * y1 < 0 or y1 == 0) >= 1)
    ask = pick(r, ["gprime", "inc", "max"] if L else ["gprime", "inc"])
    f = pl_expr(pts)
    if ask == "gprime":
        k_ = pick(r, [-2, 0, 2])
        v = dict(pts)[k_]
        return Q(f"g(x) = ∫ from -4 to x f(t) dt, where the graph of f is shown. Find g′({k_}).", str(v), ["FTC Part 1: g′(x) = f(x).", f"g′({k_}) = f({k_}) = {v}."],
                 [T(sp.integrate(f, (x, -4, k_))) if T(sp.integrate(f, (x, -4, k_))) != str(v) else str(v + 1), str(T(sp.Rational(pts[[p_[0] for p_ in pts].index(k_) + 1][1] - v, 2))), str(-v) if v else "1"],
                 PY("pl_value", pts=[list(p_) for p_ in pts], at=k_), why=["Computed g instead of g′", "Gave the slope of f (that is g″)", "Made a sign error"],
                 diagram={"alt": "Piecewise linear graph of f through " + ", ".join(f"({p_[0]}, {p_[1]})" for p_ in pts) + ".", "draw": pl_draw(pts)})
    zs = zero_xs(pts)
    ivs = sign_set(pts, 1)
    if ask == "inc":
        need(ivs != sp.S.EmptySet and ivs != sp.Interval.open(-4, 4))
        ans = set_text(ivs)
        comp = sp.Interval.open(-4, 4) - ivs - sp.FiniteSet(*[p_[0] for p_ in pts])
        neg = sign_set(pts, -1)
        need(neg != sp.S.EmptySet)
        return Q("g(x) = ∫ from -4 to x f(t) dt, where the graph of f is shown on (-4, 4). On what open interval(s) is g increasing?", ans, ["g′(x) = f(x).", "g is increasing where f(x) > 0.", ans + "."],
                 [set_text(neg), set_text(sp.Interval.open(-4, 0)) if set_text(sp.Interval.open(-4, 0)) not in (ans, set_text(neg)) else set_text(sp.Interval.open(0, 4)), "(-4, 4)"],
                 PY("g_inc", pts=[list(p_) for p_ in pts]), why=["Used where f is negative", "Read only half of the graph", "Assumed g always increases"],
                 diagram={"alt": "Piecewise linear graph of f through " + ", ".join(f"({p_[0]}, {p_[1]})" for p_ in pts) + ".", "draw": pl_draw(pts)})
    maxes = [z for z in zs if -4 < z < 4 and f.subs(x, z - sp.Rational(1, 100)) > 0 and f.subs(x, z + sp.Rational(1, 100)) < 0]
    need(len(maxes) == 1)
    mins = [z for z in zs if -4 < z < 4 and f.subs(x, z - sp.Rational(1, 100)) < 0 and f.subs(x, z + sp.Rational(1, 100)) > 0]
    ans = f"x = {T(maxes[0])}"
    return Q("g(x) = ∫ from -4 to x f(t) dt, where the graph of f is shown. At what x in (-4, 4) does g have a relative maximum?", ans, ["g′ = f.", "A relative max of g is where f changes from positive to negative.", ans + "."],
             [f"x = {T(mins[0])}" if mins else "x = 0" if maxes[0] != 0 else "x = 1", f"x = {max(pts, key=lambda p_: p_[1])[0]}" if max(pts, key=lambda p_: p_[1])[0] != maxes[0] else "x = 4", "x = 4" if maxes[0] != 4 else "x = -4"],
             PY("g_max", pts=[list(p_) for p_ in pts]), why=["Used a sign change from negative to positive", "Chose where f is largest", "Chose an endpoint"],
             diagram={"alt": "Piecewise linear graph of f through " + ", ".join(f"({p_[0]}, {p_[1]})" for p_ in pts) + ".", "draw": pl_draw(pts)})


# ============================================================== S4 Differentiating integrals (chain rule)
@fam("012")
def s4_chain(r, L):
    g = pick(r, [t ** 2 + 1, sp.sqrt(1 + t ** 2), sp.sin(t), sp.exp(t), t ** 3, sp.cos(t) + t])
    u = pick(r, [x ** 2, x ** 3, 2 * x, sp.sin(x), 3 * x + 1, sp.sqrt(x), sp.exp(x)]) if L else pick(r, [x ** 2, 2 * x, 3 * x, x ** 3, 4 * x - 1])
    a = rint(r, -2, 2)
    if L == 2 and r.random() < 0.5:
        lo = pick(r, [x, 2 * x, -x])
        need(lo != u)
        v = g.subs(t, u) * sp.diff(u, x) - g.subs(t, lo) * sp.diff(lo, x)
        prompt = f"Find d/dx [∫ from {pw(lo)} to {pw(u)} {pw(g)} dt]."
        code = f"diff(integrate(P('{T(g)}'), (t, P('{T(lo)}'), P('{T(u)}'))), x)"
        w = [g.subs(t, u) - g.subs(t, lo), g.subs(t, u) * sp.diff(u, x), g.subs(t, u) * sp.diff(u, x) + g.subs(t, lo) * sp.diff(lo, x)]
    else:
        v = g.subs(t, u) * sp.diff(u, x)
        prompt = f"Find d/dx [∫ from {a} to {pw(u)} {pw(g)} dt]."
        code = f"diff(integrate(P('{T(g)}'), (t, {a}, P('{T(u)}'))), x)"
        w = [g.subs(t, u), g.subs(t, x) * sp.diff(u, x) if u != x else g.subs(t, x) - g.subs(t, a), g.subs(t, u) * sp.diff(u, x) - g.subs(t, a)]
    wt = [T(sp.simplify(z)) for z in w]
    need(T(sp.simplify(v)) not in wt and len(set(wt)) == 3)
    return Q(prompt, T(sp.simplify(v)), ["FTC with the chain rule: d/dx ∫ from a to u(x) f(t) dt = f(u(x))·u′(x).", f"= {T(sp.simplify(v))}."], wt, H(code),
             why=["Forgot the chain-rule factor", "Substituted the wrong variable" if u != x else "Subtracted the lower-limit value", "Subtracted a constant term"])


# ============================================================== S5 Evaluating definite integrals
@fam("012")
def s5_eval(r, L):
    kind = pick(r, ["poly"] if L == 0 else ["poly", "trig", "exp", "recip"] if L == 1 else ["usub_poly", "usub_trig", "usub_exp", "trig", "cubic", "cubic"])
    if kind == "poly":
        f = polyx([rint(r, -3, 3, True) * 3, rint(r, -6, 6) * 2, rint(r, -9, 9)])
        a, b = sorted(r.sample(range(-3, 5), 2))
    elif kind == "trig":
        f = rint(r, 1, 5) * pick(r, [sp.sin(x), sp.cos(x)])
        a, b = pick(r, [(0, sp.pi), (0, sp.pi / 2), (sp.pi / 6, sp.pi / 2), (0, sp.pi / 3), (sp.pi / 4, sp.pi / 2)])
    elif kind == "exp":
        f = rint(r, 1, 4) * sp.exp(x)
        a, b = 0, rint(r, 1, 3)
    elif kind == "recip":
        f = sp.Integer(rint(r, 1, 6)) / x
        a, b = pick(r, [(1, sp.E), (1, sp.E ** 2), (1, 4), (2, 8), (1, 3)])
    elif kind == "usub_poly":
        n_ = rint(r, 2, 4)
        c = rint(r, 1, 3)
        f = 2 * c * x * (c * x ** 2 + 1) ** n_
        a, b = 0, 1
    elif kind == "usub_trig":
        k_ = rint(r, 2, 4)
        f = sp.cos(k_ * x)
        a, b = 0, pick(r, [sp.pi / (2 * k_), sp.pi / (6 * k_)])
    elif kind == "cubic":
        f = polyx([rint(r, -2, 2, True) * 4, rint(r, -3, 3) * 3, rint(r, -6, 6) * 2, rint(r, -9, 9)])
        a, b = sorted(r.sample(range(-3, 4), 2))
    else:
        k_ = rint(r, 1, 3)
        f = 2 * k_ * x * sp.exp(k_ * x ** 2)
        a, b = 0, pick(r, [1, 2])
    v = sp.simplify(sp.integrate(f, (x, a, b)))
    F_ = sp.integrate(f, x)
    w = [sp.simplify(F_.subs(x, a) - F_.subs(x, b)), sp.simplify(f.subs(x, b) - f.subs(x, a)), sp.simplify(F_.subs(x, b))]
    wt = [T(z) for z in w]
    need(T(v) not in wt and len(set(wt)) == 3 and v != 0)
    return Q(f"Evaluate {integ(f, a, b)}.", T(v), [f"Antiderivative: F(x) = {T(F_)}" + (" (substitution u = inner function)." if kind.startswith("usub") else "."), f"F({T(b)}) - F({T(a)}) = {T(v)}."], wt,
             H(f"integrate(P('{T(f)}'), (x, P('{T(a)}'), P('{T(b)}')))"), why=["Subtracted in the wrong order", "Evaluated the integrand instead of an antiderivative", "Forgot to subtract F(a)"])


SKILLS = {
    1: dict(name="Connecting Differentiation and Integration", std=["AP FUN-5.A", "AP FUN-6.A"], fams=[s1_net, s1_ftc1], extra=[err_of(s1_net), open_of(s1_net)]),
    2: dict(name="Accumulation Functions", std=["AP FUN-5.A"], fams=[s2_accum, s2_formula], extra=[err_of(s2_formula), open_of(s2_formula)]),
    3: dict(name="Analyzing Functions Defined by Integrals", std=["AP FUN-5.A", "AP FUN-4.A"], fams=[s3_analyze, s2_accum], extra=[err_of(s2_formula), open_of(s2_formula)]),
    4: dict(name="Differentiating Functions Defined by Integrals", std=["AP FUN-5.A"], fams=[s4_chain], extra=[err_of(s4_chain), open_of(s4_chain)]),
    5: dict(name="Evaluating Definite Integrals with Antiderivatives", std=["AP FUN-6.B", "AP FUN-6.D"], fams=[s5_eval], extra=[err_of(s5_eval), open_of(s5_eval)]),
}
