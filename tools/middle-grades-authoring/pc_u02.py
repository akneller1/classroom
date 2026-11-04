"""Precalculus Unit 2 — Functions (functions)."""
from hslib import *

UNIT_ID = "functions"
ABBR = "fun"


def ri(r, a, b):
    return rint(r, a, b, True)


def q_(r, L, lo=-6, hi=6):
    return sp.Integer(ri(r, lo, hi)) if L == 0 else sp.Rational(ri(r, lo, hi), pick(r, [1, 2, 3]))


def fx_lin(r, L):
    return q_(r, L) * x + rint(r, -9, 9)


def fx_quad(r):
    return sp.Integer(ri(r, -3, 3)) * x ** 2 + rint(r, -5, 5) * x + rint(r, -6, 6)


# ============================================================== S1 Linear graphs, slope, intercepts, zeros
@fam("012")
def s1_zero(r, L):
    f = fx_lin(r, L)
    z = sp.solve(f, x)[0]
    kind = pick(r, ["zero", "y-intercept", "x-intercept"])
    if kind == "y-intercept":
        v = f.subs(x, 0)
        return Q(f"What is the y-intercept of f(x) = {T(f)}?", f"(0, {T(v)})", ["Set x = 0.", f"f(0) = {T(v)}.", f"y-intercept: (0, {T(v)})."], [f"({T(z)}, 0)", f"(0, {T(-v)})" if v else "(0, 1)", f"({T(v)}, 0)"],
                 H(f"[0, P('{T(f)}').subs(x, 0)]", "point"), why=["Gave the x-intercept", "Made a sign error", "Switched the coordinates"])
    pre = "zero of" if kind == "zero" else "x-intercept of the graph of"
    ans = f"x = {T(z)}" if kind == "zero" else f"({T(z)}, 0)"
    w = [T(-z) if z else "1", T(f.subs(x, 0)), T(1 / z) if z not in (0,) else "2"]
    return Q(f"Find the {pre} f(x) = {T(f)}.", ans, ["Set f(x) = 0.", f"Solve {T(f)} = 0.", f"x = {T(z)}."], [f"x = {v}" if kind == "zero" else f"({v}, 0)" for v in w],
             H(f"solve(P('{T(f)}'), x)[0]" if kind == "zero" else f"[solve(P('{T(f)}'), x)[0], 0]", "expr" if kind == "zero" else "point"), why=["Made a sign error", "Gave the y-intercept value", "Took the reciprocal"])


@fam("012")
def s1_slope_std(r, L):
    a, b = ri(r, -9, 9), ri(r, -9, 9)
    c = rint(r, -15, 15)
    m = sp.Rational(-a, b)
    return Q(f"Find the slope of the line {T(a * x + b * y)} = {c}.", T(m), [f"Solve for y: y = {T(m * x + sp.Rational(c, b))}.", f"The slope is {T(m)}."], [T(-m), T(1 / m) if m else "1", T(sp.Rational(c, b))],
             H(f"-diff(P('{T(a * x + b * y)}'), x)/diff(P('{T(a * x + b * y)}'), y)"), why=["Forgot the negative sign", "Used b/a instead of -a/b", "Gave the y-intercept"])


# ============================================================== S2 Operations and composition
@fam("012")
def s2_compose_num(r, L):
    f = fx_lin(r, 0) if L == 0 else fx_quad(r)
    g = fx_lin(r, 0)
    a = rint(r, -4, 4)
    order = pick(r, ["fg", "gf"])
    v = f.subs(x, g.subs(x, a)) if order == "fg" else g.subs(x, f.subs(x, a))
    nm = "(f ∘ g)" if order == "fg" else "(g ∘ f)"
    wrong = g.subs(x, f.subs(x, a)) if order == "fg" else f.subs(x, g.subs(x, a))
    return Q(f"Let f(x) = {T(f)} and g(x) = {T(g)}. Find {nm}({a}).", T(v), [f"{nm}({a}) = {'f(g(' if order == 'fg' else 'g(f('}{a}))." if True else "", f"Inside first: {'g' if order == 'fg' else 'f'}({a}) = {T((g if order == 'fg' else f).subs(x, a))}.",
                                                                            f"Then apply {'f' if order == 'fg' else 'g'}: {T(v)}."],
             [T(wrong) if wrong != v else T(v + 1), T(f.subs(x, a) * g.subs(x, a)), T(f.subs(x, a) + g.subs(x, a))], H(f"(lambda F, G: {'F.subs(x, G.subs(x, ' if order == 'fg' else 'G.subs(x, F.subs(x, '}{a})))(P('{T(f)}'), P('{T(g)}'))"),
             why=["Composed in the wrong order", "Multiplied the functions", "Added the functions"])


@fam("12")
def s2_compose_expr(r, L):
    f = fx_lin(r, 0) if L == 1 else fx_quad(r)
    g = fx_lin(r, 0)
    v = sp.expand(f.subs(x, g))
    return Q(f"Let f(x) = {T(f)} and g(x) = {T(g)}. Find (f ∘ g)(x) and simplify.", T(v), [f"(f ∘ g)(x) = f(g(x)) = f({T(g)}).", f"Substitute {T(g)} for x in f.", f"Expand: {T(v)}."],
             [T(sp.expand(g.subs(x, f))), T(sp.expand(f * g)), T(sp.expand(f + g))], H(f"P('{T(f)}').subs(x, P('{T(g)}'))"), why=["Composed in the wrong order", "Multiplied the functions", "Added the functions"])


@fam("012")
def s2_ops(r, L):
    f, g = fx_lin(r, 0), fx_lin(r, 0)
    op = pick(r, ["+", "-", "·"])
    v = sp.expand(f + g if op == "+" else f - g if op == "-" else f * g)
    nm = {"+": "(f + g)(x)", "-": "(f - g)(x)", "·": "(f · g)(x)"}[op]
    return Q(f"Let f(x) = {T(f)} and g(x) = {T(g)}. Find {nm}.", T(v), [f"{nm} = ({T(f)}) {op} ({T(g)}).", "Combine like terms." if op != "·" else "Multiply each term (FOIL).", f"{T(v)}."],
             [T(sp.expand(f - g if op != "-" else f + g)), T(sp.expand(f.subs(x, g))), T(sp.expand(f + g + 1)) if op == "·" else T(sp.expand(f - g.subs(x, -x)))],
             H(f"(lambda F, G: {'F + G' if op == '+' else 'F - G' if op == '-' else 'F*G'})(P('{T(f)}'), P('{T(g)}'))"), why=["Used the wrong operation", "Composed instead", "Distributed the subtraction incorrectly" if op == "-" else ""])


# ============================================================== S3 Iteration
@fam("012")
def s3_iterate(r, L):
    f = (ri(r, -3, 3) * x + rint(r, -5, 5)) if L < 2 else (x ** 2 + rint(r, -3, 2))
    x0 = rint(r, -3, 3)
    k = 3 if L < 2 else 3
    seq = [sp.Integer(x0)]
    for _ in range(k):
        seq.append(f.subs(x, seq[-1]))
    need(abs(seq[-1]) < 10 ** 6)
    return Q(f"Let f(x) = {T(f)} and x₀ = {x0}. Find the third iterate x₃ (x₁ = f(x₀), x₂ = f(x₁), x₃ = f(x₂)).", T(seq[-1]), [f"x₁ = f({x0}) = {T(seq[1])}.", f"x₂ = f({T(seq[1])}) = {T(seq[2])}.", f"x₃ = f({T(seq[2])}) = {T(seq[3])}."],
             [T(seq[2]), T(f.subs(x, 3 * x0)), T(seq[1] * 3)], H(f"(lambda F: F.subs(x, F.subs(x, F.subs(x, {x0}))))(P('{T(f)}'))"), why=["Stopped one iteration early", "Substituted 3 times the starting value", "Multiplied the first iterate by 3"])


# ============================================================== S4 Twelve basic functions and domains
@fam("012")
def s4_domain(r, L):
    a = rint(r, -8, 8)
    kind = pick(r, ["sqrt", "recip", "ln"] if L else ["sqrt", "recip"])
    if kind == "sqrt":
        c = ri(r, -3, 3) if L == 2 else 1
        f = sp.sqrt(c * (x - a))
        bnd = a
        dom = sp.Interval(a, sp.oo) if c > 0 else sp.Interval(-sp.oo, a)
        ans = set_text(dom)
        wr = [set_text(sp.Interval.open(a, sp.oo)) if c > 0 else set_text(sp.Interval(a, sp.oo)), set_text(sp.Interval(-a, sp.oo)) if a else set_text(sp.Interval(1, sp.oo)), "(-∞, ∞)"]
        code = f"sp_domain_sqrt('{T(f)}')"
    elif kind == "recip":
        f = 1 / (x - a)
        dom = sp.Union(sp.Interval.open(-sp.oo, a), sp.Interval.open(a, sp.oo))
        ans = set_text(dom)
        wr = [set_text(sp.Union(sp.Interval.open(-sp.oo, -a), sp.Interval.open(-a, sp.oo))) if a else "(0, ∞)", "(-∞, ∞)", set_text(sp.Interval.open(a, sp.oo))]
        code = f"Union(Interval.open(-oo, solve(1/P('{T(f)}'), x)[0]), Interval.open(solve(1/P('{T(f)}'), x)[0], oo))"
    else:
        f = sp.log(x - a)
        dom = sp.Interval.open(a, sp.oo)
        ans = set_text(dom)
        wr = [set_text(sp.Interval(a, sp.oo)), set_text(sp.Interval.open(-a, sp.oo)) if a else set_text(sp.Interval.open(1, sp.oo)), "(-∞, ∞)"]
        code = f"Interval.open(solve(P('{T(x - a)}'), x)[0], oo)"
    if kind == "sqrt":
        code = f"ineq_set('{T(c * (x - a))} ≥ 0')"
    return Q(f"Find the domain of f(x) = {T(f)}. Use interval notation.", ans, ["Square roots need a nonnegative radicand; denominators cannot be 0; logarithms need a positive argument.", f"Solve the restriction for x.", f"Domain: {ans}."],
             wr, H(code, "interval"), why=["Excluded or included the endpoint incorrectly", "Used the opposite of the boundary value", "Ignored the restriction"])


@fam("012", mode="mc")
def s4_identify(r, L):
    props = [("is its own inverse and has asymptotes at both axes", "f(x) = 1/x"), ("has range [0, ∞) and a V shape", "f(x) = |x|"), ("is bounded between -1 and 1 and passes through the origin", "f(x) = sin(x)"),
             ("has domain (0, ∞) and passes through (1, 0)", "f(x) = ln(x)"), ("has range (0, ∞) and passes through (0, 1)", "f(x) = eˣ"), ("is the identity function", "f(x) = x"),
             ("has domain [0, ∞) and is increasing", "f(x) = √x"), ("is an odd function that is increasing on all reals and passes through (1, 1)", "f(x) = x³"),
             ("has range [0, ∞) and is a U-shaped even function", "f(x) = x²"), ("has horizontal asymptotes y = 0 and y = 1", "f(x) = 1/(1 + e^(-x))"),
             ("is the greatest integer function (a step function)", "f(x) = ⌊x⌋"), ("is bounded between -1 and 1 and has value 1 at x = 0", "f(x) = cos(x)")]
    i = r.randrange(len(props))
    d, f = props[i]
    others = [p[1] for j, p in enumerate(props) if j != i]
    r.shuffle(others)
    opts = [(f, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"Which basic function {d}?", f, [f"{f} {d}."], options=opts, chk=TXT(f), mode="mc")


# ============================================================== S5 Piecewise, step, absolute value
@fam("012")
def s5_piecewise(r, L):
    c = rint(r, -3, 3)
    f1, f2 = fx_lin(r, 0), (fx_lin(r, 0) if L < 2 else fx_quad(r))
    a = pick(r, [c, c - rint(r, 1, 4), c + rint(r, 1, 4)])
    v = f1.subs(x, a) if a < c else f2.subs(x, a)
    wrong = f2.subs(x, a) if a < c else f1.subs(x, a)
    return Q(f"f(x) = {T(f1)} if x < {c}; f(x) = {T(f2)} if x ≥ {c}. Find f({a}).", T(v), [f"Decide which piece applies: {a} {'<' if a < c else '≥'} {c}.", f"Use {T(f1) if a < c else T(f2)}.", f"f({a}) = {T(v)}."],
             [T(wrong) if wrong != v else T(v + 1), T(f1.subs(x, a) + f2.subs(x, a)), T(-v) if v else "1"], H(f"Piecewise((P('{T(f1)}'), x < {c}), (P('{T(f2)}'), True)).subs(x, {a})"),
             why=["Used the wrong piece", "Added both pieces", "Made a sign error"])


@fam("012")
def s5_step_abs(r, L):
    if r.random() < 0.5:
        v = sp.Rational(rint(r, -40, 40), pick(r, [2, 4, 5, 10]))
        need(v.q != 1)
        e = f"⌊{T(v) if v.q not in (2, 4, 5, 10) else D(v)}⌋"
        ans = math.floor(v)
        return Q(f"Evaluate the greatest integer function: {e}", str(ans), ["⌊x⌋ is the greatest integer less than or equal to x.", f"{D(v)} lies between {math.floor(v)} and {math.floor(v) + 1}.", f"{e} = {ans}."],
                 [str(math.ceil(v)), str(int(v)), str(round(float(v)) if round(float(v)) not in (math.floor(v), int(v), math.ceil(v)) else math.floor(v) - 1)], H(f"floor({v})"),
                 why=["Rounded up", "Dropped the decimal part (truncated toward 0)", ""])
    a, b, c = ri(r, -3, 3), rint(r, -5, 5), rint(r, -6, 6)
    p = rint(r, -6, 6)
    f = a * sp.Abs(x - b) + c
    v = f.subs(x, p)
    return Q(f"Evaluate f({p}) for f(x) = {T(f)}.", T(v), [f"f({p}) = {T(a)}|{p} - {par(b)}| + {T(c)}." if False else f"Substitute {p} for x.", f"|{p - b}| = {abs(p - b)}.", f"f({p}) = {T(v)}."],
             [T(a * (p - b) + c), T(a * abs(p + b) + c) if abs(p + b) != abs(p - b) else T(v + 2), T(-a * abs(p - b) + c)], H(f"P('{T(f)}').subs(x, {p})"),
             why=["Ignored the absolute value", "Changed the sign inside the absolute value", "Made a sign error with the coefficient"])


# ============================================================== S6 Transformations / S7 Families
PAR = [(x ** 2, "x²"), (sp.Abs(x), "|x|"), (sp.sqrt(x), "√x"), (x ** 3, "x³"), (1 / x, "1/x")]


@fam("012")
def s6_write(r, L):
    f, nm = pick(r, PAR[:3] if L == 0 else PAR)
    h, k = rint(r, -5, 5), rint(r, -5, 5)
    need(h or k)
    a = 1 if L == 0 else pick(r, [-1, 2, -2, 3, sp.Rational(1, 2)])
    g = a * f.subs(x, x - h) + k
    desc = (["reflected over the x-axis"] if a < 0 else []) + ([f"vertically stretched by a factor of {T(abs(a))}"] if abs(a) > 1 else [f"vertically compressed by a factor of {T(abs(a))}"] if abs(a) < 1 else []) + \
           ([f"shifted {abs(h)} units {'right' if h > 0 else 'left'}"] if h else []) + ([f"shifted {abs(k)} units {'up' if k > 0 else 'down'}"] if k else [])
    ans = "g(x) = " + T(g)
    w1 = a * f.subs(x, x + h) + k
    w2 = a * f.subs(x, x - h) - k
    w3 = a * f.subs(x, x - k) + h
    return Q(f"The graph of f(x) = {nm} is {', then '.join(desc)}. Write an equation for the new function g.", ans, ["Horizontal shift h: replace x with x - h.", "Vertical shift k: add k.", "Stretch or reflect by multiplying by a.", f"{ans}."],
             ["g(x) = " + T(w) for w in (w1, w2, w3)], H(f"{sp.srepr(g)}".replace("Symbol('x', real=True)", "x") if False else f"P('{T(g)}')"),
             why=["Shifted horizontally in the wrong direction", "Shifted vertically in the wrong direction", "Mixed up the horizontal and vertical shifts"])


@fam("01", mode="mc")
def s6_graph(r, L):
    f, nm = pick(r, PAR[:3])
    h, k = rint(r, -4, 4), rint(r, -4, 4)
    need(h and k)
    a = 1 if L == 0 else pick(r, [-1, 2, -2])
    g = a * f.subs(x, x - h) + k
    gf = sp.lambdify(x, g, "math")
    xs = [h + (-8 + 16 * i / 600) for i in range(601)]
    if nm == "√x":
        xs = [h + 9 * i / 600 for i in range(601)]
    ys = [gf(v) for v in xs]
    opts = [("y = " + T(g), True), ("y = " + T(a * f.subs(x, x + h) + k), False), ("y = " + T(a * f.subs(x, x - k) + h), False), ("y = " + T(-a * f.subs(x, x - h) + k), False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    win_ = (min(-2, h - 6), min(-2, h - 6) + 12)
    return Q(f"The graph shows a transformation of y = {nm}. Which equation matches it? The marked point is the image of (0, 0).", "y = " + T(g),
             [f"The marked point moved from (0, 0) to ({h}, {k}), so h = {h} and k = {k}.", "Check the direction and stretch." if a != 1 else "The shape is not stretched or reflected.", "y = " + T(g) + "."], options=opts, chk=H(f"P('{T(g)}')"), mode="mc",
             diagram={"alt": f"Graph of a transformed {nm} curve with key point ({h}, {k}){', reflected over a horizontal line' if a < 0 else ''}{', vertically stretched by ' + str(abs(a)) if abs(a) != 1 else ''}.",
                      "draw": curve_draw([(xs, ys, "solid")], win_, (min(-2, k - 6), min(-2, k - 6) + 12), pts=[(h, k, "")])})


@fam("012")
def s7_point(r, L):
    px, py = rint(r, -6, 6), rint(r, -6, 6)
    h, k = rint(r, -5, 5), rint(r, -5, 5)
    a = 1 if L == 0 else pick(r, [-1, 2, 3, -2])
    b_ = 1 if L < 2 else pick(r, [2, sp.Rational(1, 2)])
    nx = sp.Rational(px, 1) / b_ + h
    ny = a * py + k
    gtxt = f"{'' if a == 1 else '-' if a == -1 else T(a)}f({'' if b_ == 1 else T(b_)}{'(' if b_ != 1 else ''}x {'-' if h > 0 else '+'} {abs(h)}{')' if b_ != 1 else ''}) {'+' if k >= 0 else '-'} {abs(k)}"
    return Q(f"The point ({px}, {py}) is on the graph of y = f(x). What point must be on the graph of y = {gtxt}?", f"({T(nx)}, {T(ny)})",
             ["Horizontal changes act on x in the opposite way: x → x/b + h.", "Vertical changes act on y: y → a·y + k.", f"New point: ({T(nx)}, {T(ny)})."],
             [f"({T(px - h)}, {T(ny)})", f"({T(nx)}, {T(py + k)})" if a != 1 else f"({T(nx)}, {T(py - k)})", f"({T(px * b_ + h)}, {T(ny)})" if b_ != 1 else f"({T(ny)}, {T(nx)})"],
             H(f"[solve(Eq({T(b_) if b_ != 1 else 1}*(x - ({h})), {px}), x)[0], {a}*{py} + {k}]", "point"), why=["Shifted x in the wrong direction", "Forgot the vertical stretch or reflection" if a != 1 else "Shifted y the wrong way",
                                                                                                         "Multiplied instead of dividing for the horizontal compression" if b_ != 1 else "Switched the coordinates"])


@fam("012", mode="mc")
def s7_family(r, L):
    h, k = rint(r, -5, 5), rint(r, -5, 5)
    need(h and k)
    f, nm = pick(r, PAR[:3])
    g = f.subs(x, x - h) + k
    good = f"{abs(h)} units {'right' if h > 0 else 'left'} and {abs(k)} units {'up' if k > 0 else 'down'}"
    bad = [f"{abs(h)} units {'left' if h > 0 else 'right'} and {abs(k)} units {'up' if k > 0 else 'down'}", f"{abs(k)} units {'right' if k > 0 else 'left'} and {abs(h)} units {'up' if h > 0 else 'down'}",
           f"{abs(h)} units {'right' if h > 0 else 'left'} and {abs(k)} units {'down' if k > 0 else 'up'}"]
    opts = [(good, True)] + [(b, False) for b in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"How is the graph of y = {T(g)} related to the graph of y = {nm}?", good, ["y = f(x - h) + k shifts the graph h units horizontally and k units vertically.", f"h = {h}, k = {k}."], options=opts,
             chk=PY("shift_desc", h=h, k=k), mode="mc")


# ============================================================== S8 Nonlinear and absolute value inequalities
@fam("012")
def s8_abs(r, L):
    a = 1 if L == 0 else ri(r, 1, 4)
    b, c = rint(r, -8, 8), rint(r, 1, 10)
    op = pick(r, ["<", "≤", ">", "≥"])
    st = f"|{T(a * x + b)}| {op} {c}"
    lo, hi = sp.Rational(-c - b, a), sp.Rational(c - b, a)
    cl = op in ("≤", "≥")
    ans = ivl(lo, hi, cl, cl) if op in ("<", "≤") else ivl(-sp.oo, lo, False, cl) + " ∪ " + ivl(hi, sp.oo, cl, False)
    wr = [ivl(-sp.oo, lo, False, cl) + " ∪ " + ivl(hi, sp.oo, cl, False) if op in ("<", "≤") else ivl(lo, hi, cl, cl), ivl(lo, hi, not cl, not cl) if op in ("<", "≤") else ivl(-sp.oo, lo, False, not cl) + " ∪ " + ivl(hi, sp.oo, not cl, False),
          ivl(sp.Rational(-c + b, a), sp.Rational(c + b, a), cl, cl) if b and op in ("<", "≤") else ivl(-sp.oo, sp.Rational(-c + b, a), False, cl) + " ∪ " + ivl(sp.Rational(c + b, a), sp.oo, cl, False) if b else ivl(-sp.oo, hi, False, cl)]
    return Q(f"Solve {st}. Write the answer in interval notation.", ans, [f"|u| {op} {c} means {'-' + str(c) + ' ' + op + ' u ' + op + ' ' + str(c) if op in ('<', '≤') else 'u ' + ('<' if op == '>' else '≤') + ' -' + str(c) + ' or u ' + op + ' ' + str(c)}.",
                                                                          "Solve each part for x.", f"{ans}."], wr, H(f"ineq_set('{st}')", "interval"),
             why=["Used “between” for a greater-than inequality (or the reverse)", "Used the wrong brackets", "Moved the constant with the wrong sign"])


@fam("12")
def s8_rational(r, L):
    a, b = r.sample(range(-6, 7), 2)
    op = pick(r, ["≥", "<", ">", "≤"])
    st = f"(x - {a})/(x - {b}) {op} 0".replace("- -", "+ ")
    expr = (x - a) / (x - b)
    sol = sp.solve_univariate_inequality({"<": expr < 0, ">": expr > 0, "≤": expr <= 0, "≥": expr >= 0}[op], x, relational=False)
    ans = set_text(sol)
    comp = sp.Complement(sp.S.Reals, sol)
    wr = [set_text(comp.simplify()) if isinstance(comp.simplify(), (sp.Interval, sp.Union)) else "(-∞, ∞)", ans.replace("[", "(").replace("]", ")") if "[" in ans else ans.replace(f"({a}", f"[{a}").replace(f"{a})", f"{a}]"), ans.replace(f"{b})", f"{b}]").replace(f"({b}", f"[{b}") if True else ""]
    return Q(f"Solve {st}. Write the answer in interval notation.", ans, [f"Critical values: x = {a} (numerator) and x = {b} (denominator).", "Test the sign in each interval.", f"x = {b} is never included (division by zero).", f"{ans}."],
             wr, H(f"ineq_set('{T(expr)} {op} 0')", "interval"), why=["Chose the regions with the wrong sign", "Included or excluded the zero of the numerator incorrectly", "Included the value that makes the denominator 0"])


# ============================================================== S9 Inverse functions
@fam("012")
def s9_inverse(r, L):
    if L == 0:
        a, b = ri(r, -6, 6), rint(r, -9, 9)
        f = a * x + b
    elif L == 1:
        f = pick(r, [ri(r, 2, 5) * x ** 3 + rint(r, -9, 9), sp.Rational(ri(r, 1, 5), pick(r, [2, 3])) * x + rint(r, -6, 6), ri(r, 2, 5) * sp.sqrt(x) + rint(r, -5, 5)])
    else:
        a, b, c = ri(r, 1, 6), rint(r, -6, 6), ri(r, -5, 5)
        f = (a * x + b) / (x + c)
        need(sp.simplify(f - a) != 0 and b - a * c != 0)
    inv = sp.solve(sp.Eq(y, f), x)
    need(len(inv) == 1)
    g = sp.simplify(inv[0].subs(y, x))
    ws = [sp.together(sp.simplify(1 / f)), sp.together(sp.expand(-f)), sp.together(sp.simplify(g.subs(x, -x)))]
    allv = [g] + ws
    need(all(sp.simplify(allv[i] - allv[j]) != 0 for i in range(4) for j in range(i + 1, 4)))
    return Q(f"Find f⁻¹(x) for f(x) = {T(f)}." + (" (Domain of f: x ≥ 0.)" if "√" in T(f) else ""), "f⁻¹(x) = " + T(g), ["Write y = f(x).", "Swap x and y.", "Solve for y.", f"f⁻¹(x) = {T(g)}."],
             ["f⁻¹(x) = " + T(w) for w in ws], H(f"solve(Eq(x, P('{T(f)}').subs(x, y)), y)[0]"),
             why=["Took the reciprocal instead of the inverse", "Took the opposite", "Made a sign error while solving"])


@fam("012")
def s9_value(r, L):
    a, b = ri(r, -6, 6), rint(r, -9, 9)
    f = a * x + b if L < 2 else a * x ** 3 + b
    t0 = rint(r, -4, 4)
    v = f.subs(x, t0)
    return Q(f"For f(x) = {T(f)}, find f⁻¹({T(v)}).", str(t0), [f"f⁻¹({T(v)}) is the x-value with f(x) = {T(v)}.", f"Solve {T(f)} = {T(v)}.", f"x = {t0}."],
             [T(f.subs(x, v)), T(sp.Rational(1, 1) / v) if v else "1", T(-t0) if t0 else "1"], H(f"solve(Eq(P('{T(f)}'), {v}), x)[0]" if L < 2 else f"[s_ for s_ in solve(Eq(P('{T(f)}'), {v}), x) if s_.is_real][0]"),
             why=["Evaluated f instead of f⁻¹", "Took the reciprocal", "Made a sign error"])


# ============================================================== S10 Variation
@fam("012")
def s10_variation(r, L):
    kind = pick(r, ["direct", "inverse", "joint"] if L else ["direct", "inverse"])
    k = sp.Rational(ri(r, 1, 12), pick(r, [1, 1, 2]))
    if kind == "direct":
        x1, x2 = r.sample(range(2, 15), 2)
        y1 = k * x1
        v = k * x2
        st = f"y varies directly with x, and y = {T(y1)} when x = {x1}. Find y when x = {x2}."
        code = f"({y1})/{x1}*{x2}"
        wr = [T(y1 * x1 / x2), T(y1 + x2 - x1), T(k)]
    elif kind == "inverse":
        x1, x2 = r.sample(range(2, 15), 2)
        y1 = k / x1
        v = k / x2
        st = f"y varies inversely with x, and y = {T(y1)} when x = {x1}. Find y when x = {x2}."
        code = f"({y1})*{x1}/{x2}"
        wr = [T(y1 / x1 * x2), T(y1 * x1 * x2), T(k)]
    else:
        x1, z1, x2, z2 = [rint(r, 2, 9) for _ in range(4)]
        y1 = k * x1 * z1
        v = k * x2 * z2
        st = f"y varies jointly with x and z, and y = {T(y1)} when x = {x1} and z = {z1}. Find y when x = {x2} and z = {z2}."
        code = f"({y1})/({x1}*{z1})*{x2}*{z2}"
        wr = [T(y1 / (x1 * z1) * x2 / z2), T(y1 * x2 * z2), T(k)]
    return Q(st, T(v), [f"Write the variation equation and find k = {T(k)}.", "Use k with the new values.", f"y = {T(v)}."], wr, H(code),
             why=["Used the wrong type of variation", "Forgot to find k first", "Gave k instead of y"], tags=["modeling"])


# ============================================================== S11 Quadratic equations and quadratic form
@fam("012")
def s11_quad(r, L):
    if L == 0:
        a, b = r.sample(range(-8, 9), 2)
        f = sp.expand((x - a) * (x - b))
    elif L == 1:
        a_, b_, c_ = ri(r, 1, 4), rint(r, -8, 8), rint(r, -8, 8)
        f = a_ * x ** 2 + b_ * x + c_
        dsc = b_ ** 2 - 4 * a_ * c_
        need(dsc > 0 and sp.sqrt(dsc).is_Integer is False)
    else:
        p, q = r.sample([1, 4, 9, 16, 25, 2, 3], 2)
        f = sp.expand((x ** 2 - p) * (x ** 2 - q))
    sols = [s_ for s_ in sp.solve(f, x) if s_.is_real]
    ans = " or ".join(f"x = {T(sp.nsimplify(s_))}" for s_ in sorted(sols, key=lambda v: float(v)))
    w1 = f"x = {p} or x = {q}" if L == 2 else " or ".join(f"x = {T(-s_)}" for s_ in sorted(sols, key=lambda v: float(v)))
    w2 = " or ".join(f"x = {T(s_)}" for s_ in sorted(sols, key=lambda v: float(v))[: max(1, len(sols) // 2)])
    w3 = " or ".join(f"x = {T(s_ + 1)}" for s_ in sorted(sols, key=lambda v: float(v)))
    need(w1 != ans)
    return Q(f"Solve {T(f)} = 0. Give exact solutions.", ans, ["Factor, use the quadratic formula, or substitute u = x² for quadratic form." if L == 2 else "Factor or use the quadratic formula.", f"Solutions: {ans}."] +
             (["With u = x²: solve the quadratic in u, then take ± square roots."] if L == 2 else []), [w1, w2, w3], H(f"[s_ for s_ in solve(P('{T(f)}'), x) if s_.is_real]", "set"),
             why=["Made a sign error with the roots", "Missed some solutions", "Made an arithmetic error"])


# ============================================================== S12 Rational functions and asymptotes
@fam("012")
def s12_asym(r, L):
    a, b = r.sample(range(-6, 7), 2)
    m, c = ri(r, 1, 5), ri(r, -4, 4)
    kind = pick(r, ["va", "ha"] if L < 2 else ["va", "ha", "hole"])
    if kind == "hole":
        f = sp.expand(m * (x - a) * (x - b)) / sp.expand((x - a) * (x - c))
        need(len({a, b, c}) == 3)
        ftxt = f"({T(sp.expand(m * (x - a) * (x - b)))})/({T(sp.expand((x - a) * (x - c)))})"
        hy = sp.Rational(m * (a - b), a - c)
        return Q(f"Find the coordinates of the hole in the graph of f(x) = {ftxt}.", f"({a}, {T(hy)})", [f"Factor: {T(m)}(x - {a})(x - {b}) ÷ [(x - {a})(x - {c})]." .replace("- -", "+ "), f"x - {a} cancels, so there is a hole at x = {a}.".replace("- -", "+ "),
                                                                                                 f"Simplified: {T(m * (x - b) / (x - c))}; at x = {a} it equals {T(hy)}."],
                 [f"({c}, 0)", f"({a}, 0)", f"({b}, {T(hy)})"], H(f"[{a}, limit(P('{ftxt}'), x, {a})]", "point"), why=["Gave the vertical asymptote", "Assumed the hole is on the x-axis", "Used a zero of the numerator"])
    f_num = (m * x + c) if kind == "ha" or L else sp.Integer(m)
    f = f_num / (x - a)
    ftxt = f"({T(f_num)})/({T(x - a)})" if f_num != m else f"{m}/({T(x - a)})"
    need(f_num.subs(x, a) != 0 and (f_num.coeff(x) if f_num.has(x) else 0) != a)
    if kind == "va":
        return Q(f"Find the vertical asymptote of f(x) = {ftxt}.", f"x = {a}", ["Vertical asymptotes occur where the denominator is 0 (and the numerator is not).", f"x - {a} = 0.".replace("- -", "+ "), f"x = {a}."],
                 [f"x = {-a}" if a else "x = 1", f"y = {T(f_num.coeff(x)) if f_num.has(x) else 0}", f"x = {T(sp.Rational(-c, m))}" if f_num.has(x) and sp.Rational(-c, m) != a else f"x = {a + 1}"],
                 H(f"solve(1/P('{ftxt}'), x)[0]"), why=["Made a sign error", "Gave the horizontal asymptote", "Used the zero of the numerator"])
    ha = f_num.coeff(x) if f_num.has(x) else 0
    return Q(f"Find the horizontal asymptote of f(x) = {ftxt}.", f"y = {T(ha)}", ["Compare degrees of numerator and denominator.", "Equal degrees: y = ratio of leading coefficients; numerator lower: y = 0.", f"y = {T(ha)}."],
             [f"x = {a}", f"y = {T(sp.Rational(c, -a)) if a and sp.Rational(c, -a) != ha else ha + 1}", "no horizontal asymptote"], H(f"limit(P('{ftxt}'), x, oo)"),
             why=["Gave the vertical asymptote", "Divided the constant terms", "Thought there is none"])


# ============================================================== S13 Remainder and factor theorems
@fam("012")
def s13_remainder(r, L):
    coeffs = [ri(r, -3, 3)] + [rint(r, -6, 6) for _ in range(2 if L == 0 else 3)]
    p = polyx(coeffs)
    a = rint(r, -3, 3)
    rem = p.subs(x, a)
    kind = pick(r, ["rem", "factor"]) if L else "rem"
    if kind == "factor":
        p = sp.expand(p - rem) if r.random() < 0.5 else p
        rem = p.subs(x, a)
        ans = "Yes" if rem == 0 else "No"
        return Q(f"Is (x - {a}) a factor of P(x) = {T(p)}?".replace("- -", "+ "), ans, [f"By the Factor Theorem, check P({a}).", f"P({a}) = {T(rem)}.", "Yes: P(a) = 0." if rem == 0 else "No: P(a) ≠ 0."],
                 ["No" if rem == 0 else "Yes"], H(f"'Yes' if P('{T(p)}').subs(x, {a}) == 0 else 'No'", "text"), mode="sa", why=["Evaluated P at the wrong number (sign error)"])
    return Q(f"Use the Remainder Theorem to find the remainder when P(x) = {T(p)} is divided by x - {a}.".replace("- -", "+ "), T(rem), [f"The remainder is P({a}).", f"P({a}) = {T(rem)}."],
             [T(p.subs(x, -a)), T(p.subs(x, 0)), T(rem + 1)], H(f"sp_rem('{T(p)}', {a})"), why=["Evaluated P at the opposite number", "Gave the constant term", ""])


@fam("12")
def s13_find_k(r, L):
    a = ri(r, -3, 3)
    c2, c1 = ri(r, -4, 4), rint(r, -6, 6)
    kv = rint(r, -20, 20)
    p_known = c2 * x ** 3 + c1 * x ** 2
    rest = sp.expand(p_known.subs(x, a))
    need((-rest - kv * a) % 1 == 0)
    const = -rest - kv * a
    ptxt = f"{T(p_known + const)} + kx".replace("+ -", "- ") if False else T(p_known) + " + kx " + (f"+ {const}" if const >= 0 else f"- {-const}")
    return Q(f"Find k so that x - {a} is a factor of P(x) = {ptxt}.".replace("- -", "+ "), f"k = {kv}", [f"Factor Theorem: P({a}) = 0.", f"{T(rest)} + {a}k + {const} = 0." .replace("+ -", "- "), f"k = {kv}."],
             [f"k = {-kv}", f"k = {T(sp.Rational(-rest - const, 1))}", f"k = {kv + 1}"], H(f"solve(P('{T(p_known)}').subs(x, {a}) + {a}*k + {const}, k)[0]"), why=["Made a sign error", "Forgot to divide by a", ""])


# ============================================================== S14 Locating polynomial zeros
@fam("012")
def s14_zeros(r, L):
    roots = r.sample(range(-5, 6), 3)
    lead = 1 if L < 2 else ri(r, 2, 3)
    p = sp.expand(lead * (x - roots[0]) * (x - roots[1]) * (x - roots[2]))
    if L == 0:
        given = roots[0]
        need(sorted(-v for v in roots[1:]) != sorted(roots[1:]))
        return Q(f"x = {given} is a zero of P(x) = {T(p)}. Find the other two zeros.", " or ".join(f"x = {v}" for v in sorted(roots[1:])),
                 [f"Divide P(x) by (x - {given}) using synthetic division.".replace("- -", "+ "), f"The quotient is {T(sp.expand(lead * (x - roots[1]) * (x - roots[2])))}.", "Factor the quotient.", f"Zeros: {roots[1]} and {roots[2]}."],
                 [" or ".join(f"x = {-v}" for v in sorted(roots[1:])), f"x = {roots[1]}", " or ".join(f"x = {v}" for v in sorted(roots))], H(f"[s_ for s_ in solve(P('{T(p)}'), x) if s_ != {given}]", "set"),
                 why=["Made sign errors with the factors", "Found only one", "Included the given zero"])
    if L == 2 and r.random() < 0.6:
        rr = sp.Rational(rint(r, -5, 5, True), pick(r, [2, 3]))
        need(rr.q != 1)
        p = sp.expand((rr.q * x - rr.p) * (x - roots[1]) * (x - roots[2]))
        zs = sorted([rr, sp.Integer(roots[1]), sp.Integer(roots[2])])
        return Q(f"Find all real zeros of P(x) = {T(p)}.", " or ".join(f"x = {T(v)}" for v in zs), ["Possible rational zeros: ± factors of the constant over factors of the leading coefficient.", "Test candidates with synthetic division and divide out a zero.",
                                                                                                   "Factor or solve the remaining quadratic.", "Zeros: " + ", ".join(T(v) for v in zs) + "."],
                 [" or ".join(f"x = {T(-v)}" for v in zs), " or ".join(f"x = {T(v)}" for v in zs if v.q == 1), " or ".join(f"x = {T(v.p if v.q != 1 else v)}" for v in zs)], H(f"solve(P('{T(p)}'), x)", "set"),
                 why=["Made sign errors with the factors", "Missed the fractional zero", "Forgot to divide by the leading coefficient"])
    if L == 1:
        return Q(f"Find all real zeros of P(x) = {T(p)}.", " or ".join(f"x = {v}" for v in sorted(roots)), ["List possible rational zeros (factors of the constant over factors of the leading coefficient).", "Test candidates; divide out a zero you find.", "Factor the remaining quadratic.",
                                                                                                       "Zeros: " + ", ".join(map(str, sorted(roots))) + "."],
                 [" or ".join(f"x = {-v}" for v in sorted(roots)), " or ".join(f"x = {v}" for v in sorted(roots)[:2]), " or ".join(f"x = {v + 1}" for v in sorted(roots))], H(f"solve(P('{T(p)}'), x)", "set"),
                 why=["Made sign errors with the factors", "Missed a zero", ""])
    a = rint(r, -5, 4)
    q2 = sp.expand(lead * x ** 3 + rint(r, -5, 5) * x ** 2 + rint(r, -5, 5) * x + rint(r, -9, 9))
    va, vb = q2.subs(x, a), q2.subs(x, a + 1)
    need(va * vb < 0)
    return Q(f"P(x) = {T(q2)}. P({a}) = {T(va)} and P({a + 1}) = {T(vb)}. What does the Intermediate Value Theorem guarantee?", f"P has a zero between {a} and {a + 1}",
             ["P is a polynomial, so it is continuous.", f"P({a}) and P({a + 1}) have opposite signs.", f"So P has a zero between {a} and {a + 1}."],
             [f"P has a zero at x = {a}", f"P has no zero between {a} and {a + 1}", f"P has a zero at x = {T(sp.Rational(2 * a + 1, 2))}"], H(f"'P has a zero between {a} and {a + 1}' if P('{T(q2)}').subs(x, {a})*P('{T(q2)}').subs(x, {a + 1}) < 0 else ''", "text"),
             why=["Assumed the zero is at an endpoint", "Ignored the sign change", "Assumed the zero is at the midpoint"], tags=["reasoning"])


# ============================================================== S15 Exponential and logistic
@fam("012")
def s15_exp(r, L):
    if L < 2 or r.random() < 0.5:
        a = rint(r, 2, 50) * 10
        b = sp.Rational(pick(r, [sp.Rational(3, 2), 2, sp.Rational(1, 2), sp.Rational(3, 4), 3, sp.Rational(6, 5)]))
        tv = rint(r, 2, 5)
        v = a * b ** tv
        return Q(f"Evaluate f({tv}) for f(x) = {a}({T(b) if b.q == 1 else D(F(b.p, b.q))})ˣ." + (" Round to the nearest tenth." if not is_term(F(v.p, v.q)) else ""), D(F(v.p, v.q)) if is_term(F(v.p, v.q)) else Rd(F(v.p, v.q), 1),
                 [f"f({tv}) = {a}({D(F(b.p, b.q))}){sup(tv)}.", f"({D(F(b.p, b.q))}){sup(tv)} = {D(F(b.p ** tv, b.q ** tv)) if is_term(F(b.p ** tv, b.q ** tv)) else Rd(F(b.p ** tv, b.q ** tv), 4)}.", f"f({tv}) ≈ {Rd(F(v.p, v.q), 1)}."],
                 [(lambda q_: D(q_) if is_term(q_) else Rd(q_, 1))(F(a) * F(b.p, b.q) * tv), (lambda q_: D(q_) if is_term(q_) else Rd(q_, 1))(F(a) * F(b.p, b.q) ** (tv - 1)), (lambda q_: D(q_) if is_term(q_) else Rd(q_, 1))(F(a) + F(b.p, b.q) ** tv)],
                 H(f"{a}*({b})**{tv}", "round", places=1) if not is_term(F(v.p, v.q)) else H(f"{a}*({b})**{tv}"), why=["Multiplied by the exponent", "Used one fewer factor of the base", "Added instead of multiplying"])
    cpop, a, b = rint(r, 5, 50) * 100, rint(r, 2, 20), pick(r, [sp.Rational(1, 2), sp.Rational(3, 10), sp.Rational(1, 5)])
    kind = pick(r, ["capacity", "initial"])
    if kind == "capacity":
        return Q(f"A population follows P(t) = {cpop}/(1 + {a}e^(-{D(F(b.p, b.q))}t)). What is the carrying capacity?", str(cpop), ["As t → ∞, e^(-bt) → 0.", f"P(t) → {cpop}/1 = {cpop}."],
                 [T(sp.Rational(cpop, 1 + a)), str(cpop * a), str(a)], H(f"limit(P('{cpop}/(1 + {a}e^(-{D(F(b.p, b.q))}t))'), t, oo)"), why=["Gave the initial value", "Multiplied by a", "Gave a"], tags=["modeling"])
    return Q(f"A population follows P(t) = {cpop}/(1 + {a}e^(-{D(F(b.p, b.q))}t)). What is the initial population P(0)? Round to the nearest whole number.", Rd(F(cpop, 1 + a), 0),
             [f"P(0) = {cpop}/(1 + {a}·e⁰).", f"= {cpop}/{1 + a}.", f"≈ {Rd(F(cpop, 1 + a), 0)}."], [str(cpop), Rd(F(cpop, a), 0), str(cpop * (1 + a))], H(f"P('{cpop}/(1 + {a}e^(-{D(F(b.p, b.q))}t))').subs(t, 0)", "round", places=0),
             why=["Gave the carrying capacity", "Forgot to add 1", "Multiplied instead of dividing"], tags=["modeling"])


# ============================================================== S16 The number e
@fam("012")
def s16_e(r, L):
    kind = pick(r, ["continuous", "solve", "eval"])
    if kind == "continuous":
        P0, rr, tt = rint(r, 5, 50) * 100, pick(r, [2, 3, 4, 5, 6]), rint(r, 2, 15)
        v = P0 * sp.exp(sp.Rational(rr, 100) * tt)
        return Q(f"${P0:,} is invested at {rr}% interest compounded continuously. Find the balance after {tt} years, to the nearest cent.", "$" + Rd(float(v), 2),
                 ["A = Pe^(rt).", f"A = {P0}e^({D(F(rr, 100))} × {tt}).", f"A ≈ ${Rd(float(v), 2)}."], ["$" + Rd(P0 * (1 + rr / 100) ** tt, 2), "$" + Rd(P0 * (1 + rr * tt / 100), 2), "$" + Rd(P0 * math.exp(rr / 100) * tt, 2)],
                 H(f"{P0}*exp({rr}/100*{tt})", "round", places=2), why=["Used annual compounding", "Used simple interest", "Multiplied by t outside the exponent"], tags=["modeling"])
    if kind == "solve":
        k = rint(r, 2, 30)
        c = ri(r, 1, 4)
        ans = sp.log(k) / c
        return Q(f"Solve e^({c if c > 1 else ''}x) = {k}. Give an exact answer.", "x = " + T(ans), [f"Take ln of both sides: {c if c > 1 else ''}x = ln({k}).", f"x = {T(ans)}."],
                 ["x = " + T(sp.log(k) * c) if c > 1 else f"x = {T(sp.log(k) + 1)}", f"x = {T(sp.Rational(k, c))}", f"x = {T(sp.exp(k) / c)}"], H(f"solve(Eq(P('e^({c}x)'), {k}), x)[0]"),
                 why=["Multiplied by the coefficient instead of dividing", "Divided instead of taking a logarithm", "Exponentiated instead of taking ln"])
    a = pick(r, [1, 2, 3, -1, sp.Rational(1, 2)])
    return Q(f"Evaluate e^({T(a)}) to the nearest thousandth.", Rd(math.exp(float(a)), 3), [f"e ≈ 2.71828.", f"e^({T(a)}) ≈ {Rd(math.exp(float(a)), 3)}."], [Rd(2.718 * float(a), 3), Rd(10 ** float(a), 3), Rd(math.log(abs(float(a)) + 1), 3)],
             H(f"exp({a})", "round", places=3), why=["Multiplied e by the exponent", "Used base 10", "Used ln instead"])


# ============================================================== S17 Logarithms
@fam("012")
def s17_log(r, L):
    b = pick(r, [2, 3, 5, 10])
    e = rint(r, -2, 5) if L else rint(r, 0, 4)
    v = sp.Integer(b) ** e
    kind = pick(r, ["eval", "convert", "solve"]) if L else pick(r, ["eval", "convert"])
    sub = str(b).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
    if kind == "eval":
        lt = f"log({T(v)})" if b == 10 else f"log{sub}({T(v)})"
        return Q(f"Evaluate {lt}.", str(e), [f"{lt} asks: {b} to what power is {T(v)}?", f"{b}{sup(e)} = {T(v)}.", f"So {lt} = {e}."], [T(v / b) if (v / b).q == 1 else str(e + 1), str(-e) if e else "1", T(sp.Rational(v.p, b)) if v.q == 1 and v.p % b == 0 and sp.Rational(v.p, b) != e else str(e - 1)],
                 H(f"P('{lt}')"), why=["Divided by the base", "Made a sign error", "Divided the argument by the base"])
    if kind == "convert":
        return Q(f"Write {b}{sup(e)} = {T(v)} in logarithmic form.", f"log{sub}({T(v)}) = {e}", ["bᵉ = y is equivalent to log_b(y) = e.", f"log{sub}({T(v)}) = {e}."],
                 [f"log{sub}({e}) = {T(v)}", f"log{str(e).translate(str.maketrans('0123456789-', '₀₁₂₃₄₅₆₇₈₉₋'))}({T(v)}) = {b}" if e > 1 else f"log({T(v)}) = {e}", f"log{sub}({b}) = {e}"],
                 PY("log_form", b=b, e=e, v=str(v)), why=["Switched the argument and the exponent", "Used the exponent as the base", "Used the base as the argument"])
    c = rint(r, 1, 9)
    st = f"log{sub}(x - {c}) = {e}".replace("- -", "+ ")
    return Q(f"Solve {st}.", f"x = {T(v + c)}", [f"Rewrite in exponential form: x - {c} = {b}{sup(e)}.".replace("- -", "+ "), f"x = {T(v)} + {c} = {T(v + c)}.", "Check: the argument must be positive."],
             [f"x = {T(v)}", f"x = {T(b * e + c)}", f"x = {T(v - c)}"], H(f"solve(Eq(P('{st.split(' = ')[0]}'), {e}), x)[0]"), why=["Forgot to add the constant", "Multiplied the base by the exponent", "Subtracted instead of adding"])


@fam("012")
def s17_domain(r, L):
    a = rint(r, -8, 8)
    c = pick(r, [1, -1])
    f = sp.log(c * (x - a))
    ans = set_text(sp.Interval.open(a, sp.oo) if c > 0 else sp.Interval.open(-sp.oo, a))
    return Q(f"Find the domain of f(x) = {T(f)}.", ans, ["The argument of a logarithm must be positive.", f"Solve {T(c * (x - a))} > 0.", f"Domain: {ans}."],
             [ans.replace("(", "[", 1) if c > 0 else ans.replace(")", "]", 1), set_text(sp.Interval.open(-a, sp.oo)) if a else set_text(sp.Interval.open(1, sp.oo)), set_text(sp.Interval.open(-sp.oo, a) if c > 0 else sp.Interval.open(a, sp.oo))],
             H(f"ineq_set('{T(c * (x - a))} > 0')", "interval"), why=["Included the endpoint", "Made a sign error", "Solved the inequality in the wrong direction"])


SKILLS = {
    1: dict(name="Linear Graphs, Slope, Intercepts, and Zeros", std=["F-IF.C.7a", "F-IF.B.4"], fams=[s1_zero, s1_slope_std], extra=[err_of(s1_zero), open_of(s1_zero), select_of(s1_slope_std)]),
    2: dict(name="Function Operations and Composition", std=["F-BF.A.1b", "F-BF.A.1c"], fams=[s2_compose_num, s2_compose_expr, s2_ops], extra=[err_of(s2_compose_num), open_of(s2_compose_num), select_of(s2_ops)]),
    3: dict(name="Function Iteration", std=["F-BF.A.2", "F-IF.A.3"], fams=[s3_iterate], extra=[err_of(s3_iterate), open_of(s3_iterate)]),
    4: dict(name="Twelve Basic Functions and Domains", std=["F-IF.A.1", "F-IF.B.5"], fams=[s4_domain, s4_identify], extra=[err_of(s4_domain), open_of(s4_domain)]),
    5: dict(name="Piecewise, Step, and Absolute Value Functions", std=["F-IF.C.7b"], fams=[s5_piecewise, s5_step_abs], extra=[err_of(s5_piecewise), open_of(s5_piecewise), select_of(s5_step_abs)]),
    6: dict(name="Parent Functions and Graph Transformations", std=["F-BF.B.3"], fams=[s6_write, s7_family, s6_graph], extra=[err_of(s6_write), open_of(s6_write)]),
    7: dict(name="Families of Related Graphs", std=["F-BF.B.3"], fams=[s7_point, s7_family], extra=[err_of(s7_point), open_of(s7_point)]),
    8: dict(name="Nonlinear and Absolute Value Inequalities", std=["A-REI.B.3", "A-CED.A.1"], fams=[s8_abs, s8_rational], extra=[err_of(s8_abs), open_of(s8_abs)]),
    9: dict(name="Inverse Functions and Relations", std=["F-BF.B.4a"], fams=[s9_inverse, s9_value], extra=[err_of(s9_inverse), open_of(s9_value), select_of(s9_value)]),
    10: dict(name="Direct, Inverse, and Joint Variation", std=["A-CED.A.2"], fams=[s10_variation], extra=[err_of(s10_variation), open_of(s10_variation)]),
    11: dict(name="Quadratic Equations and Quadratic Form", std=["A-REI.B.4b", "A-SSE.A.2"], fams=[s11_quad], extra=[err_of(s11_quad), open_of(s11_quad)]),
    12: dict(name="Rational Functions and Asymptotes", std=["F-IF.C.7d"], fams=[s12_asym], extra=[err_of(s12_asym), open_of(s12_asym)]),
    13: dict(name="Remainder and Factor Theorems", std=["A-APR.B.2"], fams=[s13_remainder, s13_find_k], extra=[err_of(s13_remainder), open_of(s13_remainder)]),
    14: dict(name="Locating Polynomial Zeros", std=["A-APR.B.3", "N-CN.C.9"], fams=[s14_zeros], extra=[err_of(s14_zeros), open_of(s14_zeros)]),
    15: dict(name="Exponential and Logistic Functions", std=["F-LE.A.1", "F-IF.C.8b"], fams=[s15_exp], extra=[err_of(s15_exp), open_of(s15_exp)]),
    16: dict(name="The Number e and Natural Exponential Functions", std=["F-LE.A.4", "A-SSE.B.3c"], fams=[s16_e], extra=[err_of(s16_e), open_of(s16_e)]),
    17: dict(name="Logarithmic Functions and Graphs", std=["F-BF.B.5", "F-LE.A.4"], fams=[s17_log, s17_domain], extra=[err_of(s17_log), open_of(s17_log)]),
}
