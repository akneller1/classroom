"""Calculus Unit 3 — Derivatives (derivatives)."""
from hslib import *

UNIT_ID = "derivatives"
ABBR = "der"


def poly(r, deg, lo=-6, hi=6):
    return polyx([rint(r, lo, hi, True)] + [rint(r, lo, hi) for _ in range(deg)])


def cpos(r):
    return rint(r, 2, 7)


def build_f(r, L, kind=None):
    """Return (f, rule) with a differentiable f built from rule families."""
    kinds = {0: ["power", "poly", "root"], 1: ["product", "quotient", "chain", "trig", "exp"], 2: ["chain_trig", "product_exp", "quotient", "log_chain", "chain_power"]}[L]
    k_ = kind or pick(r, kinds)
    a, b, c = rint(r, 2, 6), rint(r, -6, 6, True), rint(r, 2, 5)
    if k_ == "power":
        f = rint(r, -5, 5, True) * x ** rint(r, 2, 7) + rint(r, -9, 9) * x
    elif k_ == "poly":
        f = poly(r, 3)
    elif k_ == "root":
        f = a * sp.sqrt(x) + sp.Integer(b) / x
    elif k_ == "product":
        f = (x ** 2 + b) * (a * x + rint(r, -5, 5))
    elif k_ == "quotient":
        f = (a * x + b) / (x ** 2 + c) if L == 1 else (x ** 2 + b) / (a * x + c)
    elif k_ == "chain":
        f = (a * x + b) ** c
    elif k_ == "trig":
        f = a * sp.sin(x) + b * sp.cos(x) if r.random() < 0.5 else a * sp.tan(x) - b * x
    elif k_ == "exp":
        f = a * sp.exp(b * x) + c * sp.log(x)
    elif k_ == "chain_trig":
        f = sp.sin(a * x ** 2 + b) if r.random() < 0.5 else sp.cos(x) ** c
    elif k_ == "product_exp":
        f = x ** c * sp.exp(b * x)
    elif k_ == "log_chain":
        f = sp.log(x ** 2 + c) if r.random() < 0.5 else x * sp.log(a * x)
    else:
        f = sp.sqrt(a * x ** 2 + c)
    return f, k_


RULE = {"power": "Power rule.", "poly": "Power rule term by term.", "root": "Rewrite as powers: x^(1/2) and x^(-1).", "product": "Product rule: (uv)′ = u′v + uv′.", "quotient": "Quotient rule: (u ÷ v)′ = (u′v - uv′) ÷ v².",
        "chain": "Chain rule: n(inside)ⁿ⁻¹ · (inside)′.", "trig": "(sin x)′ = cos x, (cos x)′ = -sin x, (tan x)′ = sec² x.", "exp": "(e^(kx))′ = ke^(kx), (ln x)′ = 1 ÷ x.",
        "chain_trig": "Chain rule with a trigonometric outer function.", "product_exp": "Product rule with the chain rule for e^(kx).", "log_chain": "(ln u)′ = u′ ÷ u (product rule if needed).", "chain_power": "Rewrite as (inside)^(1/2) and use the chain rule."}


def wrong_derivs(f, k_):
    fp = sp.diff(f, x)
    out = []
    if isinstance(f, sp.Mul) and k_ in ("product", "product_exp"):
        u, v = f.as_two_terms()
        out.append(sp.diff(u, x) * sp.diff(v, x))
    if k_ == "quotient":
        n_, d_ = sp.fraction(sp.together(f))
        out.append((n_ * sp.diff(d_, x) - sp.diff(n_, x) * d_) / d_ ** 2)
        out.append(sp.diff(n_, x) / sp.diff(d_, x))
    if k_ in ("chain", "chain_trig", "chain_power", "log_chain"):
        out.append(fp / sp.diff(f.args[0] if f.args else x, x) if f.args and sp.diff(f.args[0], x) != 0 else fp * 2)
    out += [fp * -1, sp.integrate(f, x) if k_ in ("power", "poly") else fp + 1, fp.subs(x, 2 * x), sp.diff(f, x, 2)]
    res = []
    for w in out:
        w = sp.simplify(w)
        if sp.simplify(w - fp) != 0 and T(w) not in [T(z) for z in res]:
            res.append(w)
    return res[:3]


# ============================================================== S1 Definition
@fam("012")
def s1_def(r, L):
    a_, b_, c_ = rint(r, -4, 4, True), rint(r, -6, 6), rint(r, -6, 6)
    f = a_ * x ** 2 + b_ * x + c_
    p = rint(r, -4, 4)
    if L == 0:
        v = 2 * a_ * p + b_
        return Q(f"Use the definition f′(a) = lim (h → 0) (f(a + h) - f(a))/h to find f′({p}) for f(x) = {T(f)}.", str(v),
                 [f"f({p} + h) - f({p}) = {T(sp.expand(f.subs(x, p + h) - f.subs(x, p)))}.", f"Divide by h: {T(sp.expand((f.subs(x, p + h) - f.subs(x, p)) / h))}.", f"Let h → 0: f′({p}) = {v}."],
                 [str(f.subs(x, p)), str(a_ * p + b_), str(2 * a_ * p)], H(f"limit((P('{T(f)}').subs(x, {p} + h) - P('{T(f)}').subs(x, {p}))/h, h, 0)"), why=["Evaluated f instead of f′", "Forgot the factor 2", "Dropped the linear term"])
    if L == 1:
        dq = sp.expand((f.subs(x, x + h) - f) / h)
        return Q(f"For f(x) = {T(f)}, simplify the difference quotient (f(x + h) - f(x))/h (h ≠ 0).", T(dq), [f"f(x + h) = {T(sp.expand(f.subs(x, x + h)))}.", f"Subtract f(x) and divide by h.", f"= {T(dq)}."],
                 [T(2 * a_ * x + b_), T(sp.expand(dq + a_ * h)), T(sp.expand(f.subs(x, x + h) - f))], H(f"cancel((P('{T(f)}').subs(x, x + h) - P('{T(f)}'))/h)"),
                 why=["Took the limit too early", "Made an expansion error in (x + h)²", "Forgot to divide by h"])
    n_ = rint(r, 2, 5)
    base = pick(r, [2, 3, 4, 5, 9, 16])
    kind = pick(r, ["pow", "root", "sin"])
    if kind == "pow":
        expr, fnt, pt = f"((({base} + h){str(n_).translate(SUP)} - {base ** n_})/h)", f"f(x) = x{str(n_).translate(SUP)}", base
        v = n_ * base ** (n_ - 1)
    elif kind == "root":
        b2 = pick(r, [4, 9, 16, 25])
        expr, fnt, pt = f"((√({b2} + h) - {int(math.isqrt(b2))})/h)", "f(x) = √x", b2
        v = sp.Rational(1, 2 * math.isqrt(b2))
    else:
        ang = pick(r, [sp.pi / 6, sp.pi / 3, sp.pi / 4, sp.pi / 2, sp.pi])
        expr, fnt, pt = f"((sin({T(ang)} + h) - sin({T(ang)}))/h)", "f(x) = sin(x)", ang
        v = sp.cos(ang)
    return Q(f"The limit lim (h → 0) {expr} represents f′(a) for some f and a. Identify f and a, and evaluate the limit.", f"{fnt}, a = {T(pt)}; value {T(v)}",
             ["Match the form (f(a + h) - f(a)) ÷ h.", f"{fnt} and a = {T(pt)}.", f"f′(a) = {T(v)}."], [f"{fnt}, a = {T(pt)}; value {T(sp.nsimplify(v) + 1)}", f"{fnt}, a = 0; value {T(v)}", f"{fnt}, a = {T(pt)}; value 0"],
             PY("deflimit", expr=expr), why=["Made an arithmetic error", "Used the wrong point", "Thought 0 ÷ 0 = 0"])


# ============================================================== S2 Estimating derivatives
@fam("012")
def s2_table(r, L):
    xs = sorted(r.sample(range(0, 16), 4))
    ys = [rint(r, -30, 60) for _ in xs]
    i = rint(r, 1, 2)
    c = xs[i]
    v = sp.Rational(ys[i + 1] - ys[i - 1], xs[i + 1] - xs[i - 1])
    tbl = "; ".join(f"f({a}) = {b}" for a, b in zip(xs, ys))
    return Q(f"f is differentiable with {tbl}. Estimate f′({c}) using the values on either side of {c}.", T(v), [f"Use the symmetric difference quotient (f({xs[i + 1]}) - f({xs[i - 1]})) ÷ ({xs[i + 1]} - {xs[i - 1]}).",
                                                                                                                f"({ys[i + 1]} - {par(ys[i - 1])}) ÷ {xs[i + 1] - xs[i - 1]} = {T(v)}."],
             [T(sp.Rational(xs[i + 1] - xs[i - 1], ys[i + 1] - ys[i - 1])) if ys[i + 1] != ys[i - 1] else "1", str(ys[i]), str(ys[i + 1] - ys[i - 1])], H(f"Rational({ys[i + 1]} - ({ys[i - 1]}), {xs[i + 1]} - ({xs[i - 1]}))"),
             why=["Inverted the ratio", "Gave f(c) instead of the slope", "Forgot to divide by the change in x"])


@fam("012")
def s2_numeric(r, L):
    f, k_ = build_f(r, 0 if L < 2 else 1, pick(r, ["power", "poly", "trig", "exp"]) if L else "poly")
    a = rint(r, 1, 3)
    hh = sp.Rational(1, 1000)
    est = (f.subs(x, a + hh) - f.subs(x, a - hh)) / (2 * hh)
    v = float(sp.N(est, 30))
    exact = float(sp.N(sp.diff(f, x).subs(x, a), 30))
    need(abs(v) < 1e5)
    return Q(f"Use the symmetric difference quotient with h = 0.001 to estimate f′({a}) for f(x) = {T(f)}. Round to the nearest hundredth.", Rd(v, 2),
             [f"(f({a} + 0.001) - f({a} - 0.001)) ÷ 0.002.", f"≈ {Rd(v, 2)}."], [Rd(float(sp.N(f.subs(x, a), 30)), 2), Rd(float(sp.N((f.subs(x, a + hh) - f.subs(x, a)) / (2 * hh), 30)), 2), Rd(v * 2, 2)],
             H(f"(P('{T(f)}').subs(x, {a} + Rational(1, 1000)) - P('{T(f)}').subs(x, {a} - Rational(1, 1000)))/Rational(2, 1000)", "round", places=2),
             why=["Evaluated f instead", "Used a one-sided difference with the wrong denominator", "Forgot to divide by 2h"])


# ============================================================== S3 Calculating derivatives
@fam("012")
def s3_rule(r, L):
    f, k_ = build_f(r, L)
    fp = sp.simplify(sp.diff(f, x))
    if k_ in ("product", "poly", "power"):
        fp = sp.expand(fp)
    if k_ in ("quotient",):
        fp = sp.factor(sp.together(fp))
    ws = wrong_derivs(f, k_)
    need(len(ws) == 3)
    return Q(f"Find f′(x) for f(x) = {T(f)}.", T(fp), [RULE[k_], f"f′(x) = {T(fp)}."], [T(w) for w in ws], H(f"diff(P('{T(f)}'), x)"),
             why=["Used an incorrect rule (for example, multiplied the derivatives)" if k_ in ("product", "product_exp") else "Applied the rule incorrectly", "Made a sign error or missed a factor", "Made an error with the rule"])


@fam("012")
def s3_value(r, L):
    f, k_ = build_f(r, L, None)
    a = pick(r, [1, 2, 0, -1]) if k_ not in ("root", "exp", "log_chain") else pick(r, [1, 4, 9]) if k_ == "root" else 1
    if k_ in ("trig", "chain_trig"):
        a = pick(r, [0, sp.pi / 2, sp.pi, sp.pi / 4, sp.pi / 6])
    v = sp.nsimplify(sp.simplify(sp.diff(f, x).subs(x, a)))
    need(v.is_finite and v.is_real)
    return Q(f"Find f′({T(a)}) for f(x) = {T(f)}.", T(v), [RULE[k_], f"Substitute x = {T(a)}.", f"f′({T(a)}) = {T(v)}."], [T(sp.nsimplify(f.subs(x, a))), T(-v) if v else "1", T(v * 2) if v else "2"],
             H(f"diff(P('{T(f)}'), x).subs(x, P('{T(a)}'))"), why=["Evaluated f instead of f′", "Made a sign error", "Made an error with the rule"])


# ============================================================== S4 Higher-order derivatives
@fam("012")
def s4_second(r, L):
    f, k_ = build_f(r, 0 if L == 0 else 1)
    n_ = 2 if L < 2 else pick(r, [2, 3])
    d = sp.simplify(sp.diff(f, x, n_))
    if k_ in ("poly", "power", "product"):
        d = sp.expand(d)
    nm = "f″(x)" if n_ == 2 else "f‴(x)"
    ws = [sp.diff(f, x), sp.diff(f, x, n_ + 1), -d]
    wt = [T(sp.simplify(w)) for w in ws]
    need(T(d) not in wt and len(set(wt)) == 3)
    return Q(f"Find {nm} for f(x) = {T(f)}.", T(d), ["Differentiate, then differentiate again" + (" (three times in all)." if n_ == 3 else "."), f"{nm} = {T(d)}."], wt, H(f"diff(P('{T(f)}'), x, {n_})"),
             why=["Stopped after one derivative", "Differentiated one time too many", "Made a sign error"])


@fam("012")
def s4_accel(r, L):
    c3, c2, c1 = rint(r, -2, 3, True), rint(r, -9, 9), rint(r, -12, 12)
    s_ = c3 * t ** 3 + c2 * t ** 2 + c1 * t + rint(r, 0, 20)
    a = rint(r, 0, 5)
    v = sp.diff(s_, t, 2).subs(t, a)
    return Q(f"A particle's position is s(t) = {T(s_)} meters. Find its acceleration at t = {a} seconds.", f"{v} m/s²", ["a(t) = s″(t).", f"s″(t) = {T(sp.diff(s_, t, 2))}.", f"a({a}) = {v} m/s²."],
             [f"{sp.diff(s_, t).subs(t, a)} m/s²", f"{s_.subs(t, a)} m/s²", f"{sp.diff(s_, t, 3).subs(t, a) * a} m/s²"], H(f"diff(P('{T(s_)}'), t, 2).subs(t, {a})"), why=["Found the velocity", "Found the position", "Differentiated three times"], tags=["modeling"])


# ============================================================== S5 Differentiability and continuity
@fam("012", mode="mc")
def s5_diffble(r, L):
    a = rint(r, -3, 3)
    kind = pick(r, ["corner", "smooth", "jump", "cusp"])
    if kind == "corner":
        ft = f"f(x) = |{T(x - a)}|" if a else "f(x) = |x|"
        good = "continuous but not differentiable (corner)"
    elif kind == "smooth":
        ft = f"f(x) = {T(sp.expand((x - a) ** 2))}"
        good = "differentiable (and continuous)"
    elif kind == "jump":
        ft = f"f(x) = x + 1 for x < {a}, f(x) = x + 2 for x ≥ {a}"
        good = "not continuous, so not differentiable"
    else:
        ft = f"f(x) = ∛({T(x - a)})²" if a else "f(x) = ∛(x²)"
        ft = f"f(x) = ({T(x - a)})^(2/3)" if a else "f(x) = x^(2/3)"
        good = "continuous but not differentiable (cusp)"
    opts = [(o, o == good) for o in ["differentiable (and continuous)", "continuous but not differentiable (corner)", "continuous but not differentiable (cusp)", "not continuous, so not differentiable"]]
    return Q(f"At x = {a}, which describes {ft}?", good, ["Differentiable implies continuous; continuity alone does not guarantee differentiability.", "Compare the one-sided slopes at the point.", good + "."], options=opts,
             chk=PY("diff_kind", f=ft.split("= ", 1)[1] if kind != "jump" else "", a=a, pieces=["x + 1", "x + 2"] if kind == "jump" else []), mode="mc", tags=["reasoning"])


@fam("012")
def s5_ab(r, L):
    a = rint(r, -2, 3, True)
    c2 = rint(r, -3, 3, True)
    # f = c2 x² for x ≤ a; m x + b for x > a, differentiable: m = 2 c2 a, b = c2 a² - m a
    m = 2 * c2 * a
    b = c2 * a * a - m * a
    ans = f"m = {m}, b = {b}"
    return Q(f"f(x) = {T(c2 * x ** 2)} for x ≤ {a} and f(x) = mx + b for x > {a}. Find m and b so that f is differentiable at x = {a}.", ans,
             [f"Differentiable: slopes match: m = {T(2 * c2 * x)} at x = {a} = {m}.", f"Continuous: {m}({a}) + b = {c2 * a * a}.", f"b = {b}."],
             [f"m = {c2 * a}, b = {c2 * a * a - c2 * a * a}", f"m = {m}, b = {c2 * a * a}", f"m = {m}, b = {c2 * a * a + m * a}"], PY("mb", c2=c2, a=a), why=["Forgot the factor 2 in the derivative", "Forgot to subtract ma", "Made a sign error"], mode="sa")


# ============================================================== S6 Tangent lines
@fam("012")
def s6_tangent(r, L):
    f, k_ = build_f(r, 0 if L == 0 else 1 if L == 1 else pick(r, [1, 2]), pick(r, ["poly", "power"]) if L == 0 else None)
    a = pick(r, [1, 2, -1, 0]) if k_ not in ("root", "exp", "log_chain") else 1
    if k_ == "root":
        a = pick(r, [1, 4])
    if k_ in ("trig", "chain_trig"):
        a = 0
    fa, m = sp.nsimplify(f.subs(x, a)), sp.nsimplify(sp.diff(f, x).subs(x, a))
    need(fa.is_finite and m.is_finite and fa.is_Rational and m.is_Rational)
    normal = L == 2 and m != 0 and r.random() < 0.4
    sl = -1 / m if normal else m
    line = sp.expand(sl * (x - a) + fa)
    ans = "y = " + T(line)
    w = ["y = " + T(sp.expand(m * x + fa)) if a else "y = " + T(sp.expand(fa * x + m)), "y = " + T(sp.expand((-1 / m if not normal else m) * (x - a) + fa)) if m else "y = " + T(fa + 1), "y = " + T(sp.expand(sl * (x + a) + fa)) if a else "y = " + T(sp.expand(sl * x - fa)) if fa else "y = " + T(sl * x + 1)]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Find the equation of the {'normal' if normal else 'tangent'} line to f(x) = {T(f)} at x = {a}.", ans,
             [f"f({a}) = {T(fa)}.", f"f′({a}) = {T(m)}" + (f"; the normal slope is {T(sl)}." if normal else "."), f"y - {par(fa)} = {T(sl)}(x - {par(a)}).", ans + "."],
             w, H(f"(lambda F: {'-1/diff(F, x).subs(x, ' + str(a) + ')' if normal else 'diff(F, x).subs(x, ' + str(a) + ')'}*(x - ({a})) + F.subs(x, {a}))(P('{T(f)}'))"),
             why=["Used the wrong point-slope form" if a else "Switched the slope and intercept", "Used the " + ("tangent" if normal else "normal") + " slope", "Made a sign error with the point"])


@fam("12")
def s6_horizontal(r, L):
    p, q = r.sample(range(-4, 5), 2)
    c = rint(r, 1, 3) * pick(r, [1, -1])
    fp = c * 3 * (x - p) * (x - q)
    f = sp.integrate(fp, x) + rint(r, -5, 5)
    need(all(cf.is_Integer for cf in sp.Poly(f, x).all_coeffs()))
    sols = sorted([p, q])
    ans = " or ".join(f"x = {v}" for v in sols)
    return Q(f"Find all x where f(x) = {T(f)} has a horizontal tangent line.", ans, [f"f′(x) = {T(sp.expand(fp))}.", "Set f′(x) = 0 and factor.", ans + "."],
             [" or ".join(f"x = {-v}" for v in sols), " or ".join(f"x = {v}" for v in sp.solve(f - f.subs(x, 0), x) if v.is_real and v.is_Rational)[:40] or "x = 0", f"x = {sols[0]}"],
             H(f"solve(diff(P('{T(f)}'), x), x)", "set"), why=["Made sign errors", "Solved f(x) = f(0) instead of f′(x) = 0", "Missed a solution"])


# ============================================================== S7 Connecting f and f′
@fam("012")
def s7_sign(r, L):
    p, q = sorted(r.sample(range(-5, 6), 2))
    c = pick(r, [1, -1]) if L else 1
    fp = c * (x - p) * (x - q)
    ask = pick(r, ["inc", "dec"])
    inc = c > 0
    out = f"(-∞, {p}) ∪ ({q}, ∞)"
    mid = f"({p}, {q})"
    ans = (out if inc else mid) if ask == "inc" else (mid if inc else out)
    other = mid if ans == out else out
    return Q(f"f′(x) = {T(sp.expand(fp))}. On what interval(s) is f {'increasing' if ask == 'inc' else 'decreasing'}?", ans,
             [f"f′(x) = {'' if c == 1 else '-'}(x - {p})(x - {q})".replace("- -", "+ "), f"Sign chart: f′ is {'positive' if inc else 'negative'} outside [{p}, {q}] and {'negative' if inc else 'positive'} inside.", f"f is {'increasing' if ask == 'inc' else 'decreasing'} on {ans}."],
             [other, f"({p}, ∞)", f"(-∞, {q})"], H(f"ineq_set('{T(sp.expand(fp))} {'>' if ask == 'inc' else '<'} 0')", "interval"), why=["Mixed up where f′ is positive and negative", "Used only one critical point", "Used only one critical point"])


@fam("012")
def s7_graph(r, L):
    p, q = sorted(r.sample(range(-4, 5), 2))
    need(q - p >= 2)
    c = pick(r, [1, -1])
    fp = c * (x - p) * (x - q) / 2
    ask = pick(r, ["max", "min"])
    mx = p if c > 0 else q
    mn = q if c > 0 else p
    ans = f"x = {mx if ask == 'max' else mn}"
    fn = sp.lambdify(x, fp, "math")
    xs = [-6 + 12 * i / 400 for i in range(401)]
    ys = [fn(v) for v in xs]
    vx = (p + q) / 2
    return Q(f"The graph shows y = f′(x) (the derivative of f). At what x-value does f have a local {'maximum' if ask == 'max' else 'minimum'}?", ans,
             [f"f′ changes sign at x = {p} and x = {q}.", f"A local {'max' if ask == 'max' else 'min'} of f is where f′ changes from {'positive to negative' if ask == 'max' else 'negative to positive'}.", ans + "."],
             [f"x = {mn if ask == 'max' else mx}", f"x = {T(sp.Rational(p + q, 2))}", f"x = {T(fp.subs(x, sp.Rational(p + q, 2)))}"], PY("fp_extreme", p=p, q=q, c=c, ask=ask),
             why=["Mixed up the sign change for a maximum and a minimum", "Chose the extreme point of f′", "Used a y-value"],
             diagram={"alt": f"Parabola-shaped graph of f′ crossing the x-axis at x = {p} and x = {q}, opening {'up' if c > 0 else 'down'}.", "draw": curve_draw([(xs, ys, "solid")], (-6, 6), (-6, 6), pts=[(p, 0, ""), (q, 0, "")], label_every=1)})


SKILLS = {
    1: dict(name="The Derivative as a Limit of Difference Quotients", std=["AP CHA-2.A", "AP CHA-2.B"], fams=[s1_def], extra=[err_of(s1_def), open_of(s1_def)]),
    2: dict(name="Estimating Derivatives from Graphs and Tables", std=["AP CHA-2.D"], fams=[s2_table, s2_numeric], extra=[err_of(s2_table), open_of(s2_table)]),
    3: dict(name="Calculating Derivatives", std=["AP FUN-3.A", "AP FUN-3.B", "AP FUN-3.C"], fams=[s3_rule, s3_value, mc_of(s3_value)], extra=[err_of(s3_rule), open_of(s3_rule)]),
    4: dict(name="Higher-Order Derivatives", std=["AP FUN-3.F"], fams=[s4_second, s4_accel, mc_of(s4_accel)], extra=[err_of(s4_second), open_of(s4_second)]),
    5: dict(name="Differentiability and Continuity", std=["AP FUN-2.A"], fams=[s5_diffble, s5_ab], extra=[err_of(s5_ab), open_of(s5_ab)]),
    6: dict(name="Tangent Lines and Their Slopes", std=["AP CHA-2.C", "AP CHA-3.F"], fams=[s6_tangent, s6_horizontal], extra=[err_of(s6_tangent), open_of(s6_tangent)]),
    7: dict(name="Connecting a Function and Its Derivative", std=["AP FUN-4.A"], fams=[s7_sign, s7_graph], extra=[err_of(s7_sign), open_of(s7_sign)]),
}
