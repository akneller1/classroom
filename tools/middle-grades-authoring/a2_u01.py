"""Algebra 2 Unit 1 — Functions and Transformations (functions-transformations). Top-up families."""
from hslib import *
import pc_u02 as F2

UNIT_ID = "functions-transformations"
ABBR = "ft"
FR = "__import__('sympy').calculus.util.function_range"


def ri(r, a, b):
    return rint(r, a, b, True)


# ============================================================== S1 Function notation and evaluation
@fam("012")
def s1_eval(r, L):
    a, b, c = ri(r, -4, 4), rint(r, -6, 6), rint(r, -9, 9)
    k = ri(r, -4, 4) if L else rint(r, -3, 3)
    f = a * x ** 2 + b * x + c if L < 2 else a * x ** 3 + b * x ** 2 + c
    v = f.subs(x, k)
    nm = pick(r, ["f", "g", "h"])
    sq = 2 if L < 2 else 3
    w1 = f.subs(x, k) - 2 * a * k ** sq if k < 0 and sq == 2 else f.subs(x, -k)
    w2 = a * k * sq + b * k * (1 if L < 2 else k) + c if L < 2 else a * k * 3 + b * k * 2 + c
    w3 = f.subs(x, k) - 2 * (b * k if L < 2 else c)
    wr = [w for w in (w1, w2, w3) if w != v]
    need(len(set(wr)) == 3)
    return Q(f"Let {nm}(x) = {T(f)}. Find {nm}({k}).", T(v),
             [f"Substitute {k} for every x: {nm}({k}) = {T(f).replace('x', '(' + str(k) + ')')}.", "Evaluate powers first, then multiply, then add.", f"{nm}({k}) = {T(v)}."],
             [T(w) for w in wr], H(f"P('{T(f)}').subs(x, {k})"),
             why=["Squared the input but lost its negative sign" if k < 0 and sq == 2 else "Substituted the opposite of the input",
                  "Multiplied by the exponent instead of raising to a power", "Made a sign error on one term"])


@fam("012")
def s1_solve(r, L):
    nm = pick(r, ["f", "g", "h"])
    if L == 0:
        m, b = ri(r, -6, 6), rint(r, -12, 12)
        x0 = rint(r, -8, 8)
        f, v = m * x + b, m * x0 + b
        sols = [x0]
        wr = ["x = " + T(f.subs(x, v)), "x = " + (T(sp.Rational(v - b, 1) * m) if m not in (1, -1) else T(v + b)), "x = " + T(sp.Rational(v + b, m))]
        why = ["Evaluated the function at the output value instead of solving", "Multiplied by the slope instead of dividing", "Added the constant instead of subtracting it"]
    else:
        p_, q_ = r.sample(range(-7, 8), 2)
        a = 1 if L == 1 else pick(r, [1, 2, -1])
        k0 = rint(r, -9, 9)
        f = sp.expand(a * (x - p_) * (x - q_) + k0)
        v = k0
        sols = sorted([p_, q_])
        need(p_ != q_)
        wr = [" or ".join(f"x = {T(-s_)}" for s_ in sols), f"x = {T(sols[0])}", f"x = {T(f.subs(x, 0))}"]
        why = ["Used the opposite sign for both solutions", "Gave only one of the two solutions", "Evaluated the function at 0 instead of solving"]
    ans = " or ".join(f"x = {T(s_)}" for s_ in sols)
    need(len(set(wr) | {ans}) == 4)
    return Q(f"For {nm}(x) = {T(f)}, find all x such that {nm}(x) = {T(v)}.", ans,
             [f"Set the rule equal to {T(v)}: {T(f)} = {T(v)}.", "Solve the equation (move everything to one side and factor if needed).", f"{ans}."],
             wr, H(f"solve(Eq(P('{T(f)}'), {v}), x)", "set"), why=why)


@fam("12")
def s1_expr(r, L):
    b, c = rint(r, -6, 6), rint(r, -9, 9)
    a = 1 if L == 1 else ri(r, -3, 3)
    s = ri(r, -4, 4)
    f = a * x ** 2 + b * x + c
    res = sp.expand(f.subs(x, x + s))
    wr = [T(sp.expand(a * x ** 2 + a * s ** 2 + b * x + b * s + c)), T(sp.expand(f + s)), T(sp.expand(a * x ** 2 + b * x + c + s * b))]
    need(len({T(res)} | set(wr)) == 4)
    return Q(f"Let f(x) = {T(f)}. Find and simplify f(x {'+' if s > 0 else '-'} {abs(s)}).", T(res),
             [f"Replace every x with (x {'+' if s > 0 else '-'} {abs(s)}).", f"Expand (x {'+' if s > 0 else '-'} {abs(s)})² = {T(sp.expand((x + s) ** 2))} and distribute.", f"Combine like terms: {T(res)}."],
             wr, H(f"expand(P('{T(f)}').subs(x, x + ({s})))"),
             why=["Squared each term separately: (x + a)² is not x² + a²", "Added the number to the whole function instead of the input", "Only substituted into the linear term"])


# ============================================================== S2 Domain and range
@fam("012")
def s2_range(r, L):
    h_, k_ = rint(r, -6, 6), rint(r, -8, 8)
    a = ri(r, -3, 3) if L else pick(r, [1, -1, 2, -2])
    kind = pick(r, ["quad", "abs", "sqrt"] if L else ["quad", "abs"])
    if kind == "quad":
        f = a * (x - h_) ** 2 + k_
        txt = T(sp.expand(f)) if L == 2 else f"{'' if a == 1 else '-' if a == -1 else a}(x {'-' if h_ >= 0 else '+'} {abs(h_)})² {'+' if k_ >= 0 else '-'} {abs(k_)}"
    elif kind == "abs":
        f = a * sp.Abs(x - h_) + k_
        txt = f"{'' if a == 1 else '-' if a == -1 else a}|x {'-' if h_ >= 0 else '+'} {abs(h_)}| {'+' if k_ >= 0 else '-'} {abs(k_)}"
    else:
        f = a * sp.sqrt(x - h_) + k_
        txt = f"{'' if a == 1 else '-' if a == -1 else a}√(x {'-' if h_ >= 0 else '+'} {abs(h_)}) {'+' if k_ >= 0 else '-'} {abs(k_)}"
    txt = txt.replace("x - 0", "x").replace("x + 0", "x").replace(" + 0", "").replace(" - 0", "")
    txt = txt.replace("(x)²", "x²").replace("√(x)", "√x")
    rng = sp.Interval(k_, sp.oo) if a > 0 else sp.Interval(-sp.oo, k_)
    ans = set_text(rng)
    wr = [set_text(sp.Interval(-sp.oo, k_) if a > 0 else sp.Interval(k_, sp.oo)), set_text(sp.Interval(h_, sp.oo)) if h_ != k_ else "(-∞, ∞)", "(-∞, ∞)" if h_ != k_ else set_text(sp.Interval.open(k_, sp.oo))]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Find the range of f(x) = {txt}. Use interval notation.", ans,
             [("The vertex" if kind == "quad" else "The vertex of the V" if kind == "abs" else "The starting point") + f" is ({h_}, {k_}).",
              f"The leading coefficient {a} is {'positive, so the graph rises from there' if a > 0 else 'negative, so the graph falls from there'}.", f"Range: {ans}."],
             wr, H(f"{FR}(P('{txt}'), x, {'Interval(' + str(h_) + ', oo)' if kind == 'sqrt' else 'Reals'})", "interval"),
             why=["Reversed the direction of the range", "Used the x-coordinate of the vertex", "Ignored the minimum or maximum value"])


@fam("012", mode="mc")
def s2_from_points(r, L):
    xs = sorted(r.sample(range(-9, 10), 4 + L))
    ys = [rint(r, -9, 9) for _ in xs]
    need(len(set(ys)) == len(ys))
    pts = ", ".join(f"({a}, {b})" for a, b in zip(xs, ys))
    dom, rng = "{" + ", ".join(map(str, xs)) + "}", "{" + ", ".join(map(str, sorted(ys))) + "}"
    ask = pick(r, ["domain", "range"])
    ans = dom if ask == "domain" else rng
    other = rng if ask == "domain" else dom
    opts = [(ans, True), (other, False), ("{" + ", ".join(map(str, sorted(set(xs) | set(ys)))) + "}", False), ("{" + ", ".join(map(str, sorted(-v for v in (xs if ask == 'domain' else ys)))) + "}", False)]
    need(len({o for o, _ in opts}) == 4)
    return Q(f"A function is the set of points {pts}. What is its {ask}?", ans,
             [f"The {ask} is the set of all {'x' if ask == 'domain' else 'y'}-values.", f"List them once each, in order: {ans}."],
             options=opts, chk=H(f"'{ans}'", "text"), mode="mc")


# ============================================================== S7 Even and odd functions
def _parity(L, r):
    kind = pick(r, ["even", "odd", "neither"])
    cs = [ri(r, -5, 5) for _ in range(3)]
    if kind == "even":
        f = cs[0] * x ** pick(r, [2, 4]) + cs[1] * x ** 2 * (1 if L else 0) + cs[2]
        f = cs[0] * x ** 4 + cs[1] * x ** 2 + cs[2] if L else cs[0] * x ** 2 + cs[2]
    elif kind == "odd":
        f = cs[0] * x ** 3 + cs[1] * x if L else cs[0] * x ** 3 + cs[1] * x * 0 + cs[1] * x
    else:
        f = cs[0] * x ** 3 + cs[1] * x ** 2 + cs[2] if L else cs[0] * x ** 2 + cs[1] * x
    if L == 2 and r.random() < 0.5:
        if kind == "odd":
            f = cs[0] * x / (x ** 2 + abs(cs[1]))
        elif kind == "even":
            f = cs[0] / (x ** 2 + abs(cs[1]))
        else:
            f = cs[0] / (x + abs(cs[1]))
    return kind, sp.simplify(f) if L == 2 else f


@fam("012")
def s7_classify(r, L):
    kind, f = _parity(L, r)
    fm = sp.simplify(f.subs(x, -x))
    opts = [(k_, k_ == kind) for k_ in ["even", "odd", "neither"]] + [("both even and odd", False)]
    others = [k_ for k_ in ["even", "odd", "neither"] if k_ != kind]
    whys = {"even": "Assumed a function with only an x² term must be even even though other terms change sign", "odd": "Looked only at the leading term",
            "neither": "Did not compare f(-x) with both f(x) and -f(x)"}
    return Q(f"Is f(x) = {T(f)} even, odd, or neither?", kind,
             [f"Find f(-x) = {T(fm)}.", f"Compare with f(x) = {T(f)} and -f(x) = {T(-f)}.",
              "f(-x) = f(x) means even; f(-x) = -f(x) means odd; otherwise neither.", f"The function is {kind}."],
             others + ["both even and odd"], H(f"(lambda F: 'even' if simplify(F.subs(x, -x) - F) == 0 else 'odd' if simplify(F.subs(x, -x) + F) == 0 else 'neither')(P('{T(f)}'))", "text"),
             why=[whys[o] for o in others] + ["Thought a function could be both because some terms are even and some are odd"])


@fam("012")
def s7_point(r, L):
    kind = pick(r, ["even", "odd"])
    a, b = ri(r, -9, 9), ri(r, -9, 9)
    ans = f"({-a}, {b if kind == 'even' else -b})"
    wr = [f"({-a}, {-b if kind == 'even' else b})", f"({a}, {-b})", f"({b}, {a})"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"The graph of an {kind} function passes through ({a}, {b}). Which other point must be on the graph?", ans,
             ["An even function is symmetric about the y-axis: (x, y) → (-x, y)." if kind == "even" else "An odd function is symmetric about the origin: (x, y) → (-x, -y).",
              f"Apply this to ({a}, {b}).", f"{ans}."],
             wr, H(f"({-a}, {b if kind == 'even' else -b})", "point"),
             why=["Used the symmetry rule for the other type of function", "Reflected across the x-axis instead", "Switched x and y"])


# ============================================================== S8 Modeling with functions
@fam("012")
def s8_profit(r, L):
    fixed, var = pick(r, [200, 240, 300, 360, 450, 500, 600, 720]), rint(r, 2, 15)
    price = var + pick(r, [2, 3, 4, 5, 6, 8, 10, 12])
    need(fixed % (price - var) == 0)
    item = pick(r, ["shirts", "candles", "phone cases", "posters", "mugs", "bracelets"])
    be = fixed // (price - var)
    ask = pick(r, ["breakeven", "profit"]) if L else "breakeven"
    C, R = f"C(x) = {var}x + {fixed}", f"R(x) = {price}x"
    if ask == "breakeven":
        return Q(f"A club sells {item}. The cost to make x of them is {C} dollars and the revenue is {R} dollars. How many must they sell to break even?", f"{be} {item}",
                 [f"Break even when R(x) = C(x): {price}x = {var}x + {fixed}.", f"{price - var}x = {fixed}.", f"x = {be}."],
                 [f"{math.ceil(fixed / price)} {item}", f"{fixed // var if fixed % var == 0 else round(fixed / var)} {item}", f"{be * 2} {item}"],
                 H(f"solve(Eq({price}*x, {var}*x + {fixed}), x)[0]"), why=["Ignored the cost per item", "Divided the fixed cost by the cost per item", "Doubled the answer"], tags=["modeling"])
    n0 = be + rint(r, 5, 60)
    p = (price - var) * n0 - fixed
    return Q(f"A club sells {item}. The cost to make x of them is {C} dollars and the revenue is {R} dollars. Write P(x) = R(x) - C(x) and find the profit from selling {n0} {item}.", f"${p}",
             [f"P(x) = {price}x - ({var}x + {fixed}) = {price - var}x - {fixed}.", f"P({n0}) = {price - var}({n0}) - {fixed}.", f"P({n0}) = {p} dollars."],
             [f"${(price - var) * n0 + fixed}", f"${price * n0 - fixed}", f"${price * n0}"], H(f"{price}*{n0} - ({var}*{n0} + {fixed})"),
             why=["Added the fixed cost instead of subtracting it", "Forgot the cost per item", "Gave the revenue instead of the profit"], tags=["modeling"])


@fam("12")
def s8_area(r, L):
    per = pick(r, [40, 48, 60, 64, 80, 96, 100, 120])
    kind = pick(r, ["fence3", "fence4"]) if L == 2 else "fence4"
    if kind == "fence4":
        w = per // 4
        mx = w * w
        return Q(f"A rectangular pen uses {per} feet of fencing. Its area is A(w) = w({per // 2} - w), where w is the width. What is the greatest possible area?", f"{mx} square feet",
                 [f"A(w) = -w² + {per // 2}w opens down, so the maximum is at the vertex.", f"w = {per // 2} ÷ 2 = {w}.", f"A({w}) = {w}({per // 2} - {w}) = {mx}."],
                 [f"{(per // 2) ** 2} square feet", f"{per // 2 * w} square feet", f"{w} square feet"], H(f"{FR}(P('w({per // 2} - w)'.replace('w', 'x')), x, Reals).sup"),
                 why=["Squared the half-perimeter", "Used the full half-perimeter as the length", "Gave the width instead of the area"], tags=["modeling"])
    w = per // 4
    mx = w * (per - 2 * w)
    return Q(f"A rectangular garden is fenced on three sides with {per} feet of fencing (a wall forms the fourth side). Its area is A(w) = w({per} - 2w). What is the greatest possible area?", f"{mx} square feet",
             [f"A(w) = -2w² + {per}w opens down, so the maximum is at w = -b/(2a) = {per}/4 = {w}.", f"Length = {per} - 2({w}) = {per - 2 * w}.", f"A = {w}({per - 2 * w}) = {mx}."],
             [f"{(per // 4) ** 2} square feet", f"{per * w} square feet", f"{(per // 3) * (per - 2 * (per // 3))} square feet"], H(f"{FR}(P('x({per} - 2x)'), x, Reals).sup"),
             why=["Treated it as a square with four fenced sides", "Forgot to subtract twice the width", "Split the fencing into three equal sides"], tags=["modeling"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Function notation and evaluation", fams=[s1_eval, s1_solve, s1_expr], extra=[err_of(s1_eval), err_of(s1_solve), open_of(s1_eval), select_of(s1_eval)]),
    2: dict(name="Domain and range", fams=[s2_range, rr(F2.s4_domain), s2_from_points], extra=[err_of(s2_range), err_of(rr(F2.s4_domain, tag="e")), open_of(s2_range)]),
    3: dict(name="Operations and composition of functions", fams=[rr(F2.s2_compose_num), rr(F2.s2_compose_expr), rr(F2.s2_ops)],
            extra=[err_of(rr(F2.s2_compose_num, tag="e")), err_of(rr(F2.s2_compose_expr, tag="e")), open_of(rr(F2.s2_compose_num, tag="o")), select_of(rr(F2.s2_ops, tag="s"))]),
    4: dict(name="Inverse functions", fams=[rr(F2.s9_inverse), rr(F2.s9_value)], extra=[err_of(rr(F2.s9_inverse, tag="e")), err_of(rr(F2.s9_value, tag="e")), open_of(rr(F2.s9_value, tag="o"))]),
    5: dict(name="Parent functions and graph transformations", fams=[rr(F2.s6_write), rr(F2.s7_family), rr(F2.s7_point)],
            extra=[err_of(rr(F2.s6_write, tag="e")), err_of(rr(F2.s7_point, tag="e")), open_of(rr(F2.s7_point, tag="o"))]),
    6: dict(name="Piecewise functions", fams=[rr(F2.s5_piecewise), rr(F2.s5_step_abs)], extra=[err_of(rr(F2.s5_piecewise, tag="e")), open_of(rr(F2.s5_piecewise, tag="o")), select_of(rr(F2.s5_step_abs, tag="s"))]),
    7: dict(name="Even and odd functions", fams=[s7_classify, s7_point], extra=[err_of(s7_classify), err_of(s7_point), open_of(s7_point)]),
    8: dict(name="Modeling with functions", fams=[s8_profit, s8_area], extra=[err_of(s8_profit), err_of(s8_area), open_of(s8_profit)]),
}
