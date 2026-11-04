"""Precalculus Unit 1 — Equations and Inequalities (equations-inequalities)."""
from hslib import *
import g7_u08 as L7
import itertools

UNIT_ID = "equations-inequalities"
ABBR = "eqi"


def line(m, b):
    return "y = " + T(sp.nsimplify(m) * x + sp.nsimplify(b))


def frac(r, L, lo=-6, hi=6):
    if L == 0:
        return sp.Integer(rint(r, lo, hi, True))
    return sp.Rational(rint(r, lo, hi, True), pick(r, [1, 2, 3, 4] if L == 1 else [2, 3, 4, 5]))


# ============================================================== S1 Writing Linear Equations
@fam("012")
def s1_two_points(r, L):
    m, b = frac(r, L), sp.Integer(rint(r, -8, 8))
    x1, x2 = r.sample(range(-6, 7), 2)
    if L:
        need((m * x1).q == 1 and (m * x2).q == 1)
    p1, p2 = (x1, m * x1 + b), (x2, m * x2 + b)
    ans = line(m, b)
    return Q(f"Write an equation in slope-intercept form for the line through ({T(p1[0])}, {T(p1[1])}) and ({T(p2[0])}, {T(p2[1])}).", ans,
             [f"m = ({T(p2[1])} - {par(p1[1]) if False else '(' + T(p1[1]) + ')'}) ÷ ({x2} - ({x1})) = {T(m)}.", f"Substitute ({x1}, {T(p1[1])}): {T(p1[1])} = {T(m)}({x1}) + b.", f"b = {T(b)}.", f"{ans}."],
             [line(1 / m if m not in (0,) else 1, b), line(m, p1[1]), line(-m, b), line(m, -b) if b else line(m, 1)], H(f"Y - ({sp.srepr(m * x + b) if False else str(m * x + b)})".replace("Y", "y"), "eqn"),
             why=["Used run over rise for the slope", "Used a y-coordinate as the y-intercept", "Subtracted the coordinates in different orders", "Made a sign error finding b"])


@fam("012")
def s1_standard(r, L):
    a, b_ = rint(r, 1, 9), rint(r, -9, 9, True)
    need(math.gcd(a, abs(b_)) == 1)
    c = rint(r, -20, 20)
    m, bb = sp.Rational(-a, b_), sp.Rational(c, b_)
    if L == 0 or r.random() < 0.5:
        st = f"{T(a * x + b_ * y)} = {c}"
        return Q(f"Write {st} in slope-intercept form.", line(m, bb), [f"Subtract {T(a * x)} from both sides: {T(b_ * y)} = {T(-a * x + c)}.", f"Divide by {b_}.", f"{line(m, bb)}."],
                 [line(-m, bb), line(m, c), line(sp.Rational(a, 1), bb)], H(f"{a}*x + ({b_})*y - ({c})", "eqn"),
                 why=["Did not change the sign when moving the x-term", "Forgot to divide the constant", "Forgot to divide by the y-coefficient"])
    return Q(f"Write the equation {line(m, bb)} in standard form Ax + By = C with integer A > 0.", f"{T(a * x + b_ * y)} = {c}",
             [f"Multiply every term by {abs(b_)} to clear fractions.", "Move the x-term to the left side.", "Make A positive."],
             [f"{T(a * x - b_ * y)} = {c}", f"{T(a * x + b_ * y)} = {-c}", f"{T(b_ * x + a * y)} = {c}"], H(f"{a}*x + ({b_})*y - ({c})", "eqn"),
             why=["Made a sign error with the y-term", "Made a sign error with the constant", "Switched the coefficients"])


@fam("12")
def s1_context(r, L):
    rate, start = rint(r, 2, 25), rint(r, 20, 200)
    t1, t2 = r.sample(range(1, 12), 2)
    nm = name(r)
    return Q(f"{nm}'s savings grow linearly. After {t1} weeks there is ${start + rate * t1}; after {t2} weeks there is ${start + rate * t2}. Write an equation for the savings y after x weeks.",
             line(rate, start), [f"Rate: ({start + rate * t2} - {start + rate * t1}) ÷ ({t2} - {t1}) = {rate}.", f"Initial amount: {start + rate * t1} - {rate}({t1}) = {start}.", f"{line(rate, start)}."],
             [line(rate, start + rate * t1), line(start, rate), line(sp.Rational(start + rate * t2, t2), 0)], H(f"y - ({rate}*x + {start})", "eqn"),
             why=["Used a later amount as the starting amount", "Switched the rate and the start", "Divided an amount by its week number"], tags=["modeling"])


# ============================================================== S2 Parallel and Perpendicular
@fam("012")
def s2_line(r, L):
    m = frac(r, L, -5, 5)
    b0 = rint(r, -9, 9)
    px, py = rint(r, -6, 6), rint(r, -6, 6)
    kind = pick(r, ["parallel", "perpendicular"])
    mm = m if kind == "parallel" else -1 / m
    bb = py - mm * px
    ans = line(mm, bb)
    return Q(f"Write an equation of the line through ({px}, {py}) that is {kind} to {line(m, b0)}.", ans,
             [f"{'Parallel lines have equal slopes' if kind == 'parallel' else 'Perpendicular slopes are opposite reciprocals'}: m = {T(mm)}.", f"Substitute ({px}, {py}): {py} = {T(mm)}({px}) + b.", f"b = {T(bb)}.", f"{ans}."],
             [line(-mm if kind == "perpendicular" else -m, py - (-mm if kind == "perpendicular" else -m) * px), line(1 / m if kind == "perpendicular" else -1 / m, py - (1 / m if kind == "perpendicular" else -1 / m) * px), line(mm, b0), line(mm, py)],
             H(f"y - ({mm}*x + ({bb}))", "eqn"), why=["Used the opposite but not the reciprocal" if kind == "perpendicular" else "Used the opposite slope", "Used the reciprocal but not the opposite" if kind == "perpendicular" else "Used a perpendicular slope",
                                                       "Kept the original y-intercept", "Used the y-coordinate as the intercept"])


@fam("012", mode="mc")
def s2_classify(r, L):
    m = frac(r, L, -4, 4)
    kind = pick(r, ["parallel", "perpendicular", "neither"])
    m2 = m if kind == "parallel" else -1 / m if kind == "perpendicular" else m + pick(r, [1, -1, 2])
    need(m2 != -1 / m or kind == "perpendicular")
    b1, b2 = rint(r, -6, 6), rint(r, -6, 6)
    need(b1 != b2)
    e1, e2 = line(m, b1), line(m2, b2)
    opts = [(k, k == kind) for k in ["parallel", "perpendicular", "neither"]] + [("the same line", False)]
    return Q(f"Are the lines {e1} and {e2} parallel, perpendicular, or neither?", kind, [f"Slopes: {T(m)} and {T(m2)}.", "Equal slopes → parallel; product of slopes -1 → perpendicular.", f"They are {kind}."],
             options=opts, chk=H(f"'parallel' if {m} == {m2} else 'perpendicular' if ({m})*({m2}) == -1 else 'neither'", "text"), mode="mc")


# ============================================================== S3 Solving Equations Graphically
def graph_poly(fx, gx, xr=(-6, 6), yr=(-8, 8), pts=()):
    f_ = sp.lambdify(x, fx)
    g_ = sp.lambdify(x, gx) if gx is not None else None

    def draw(path):
        fig, ax = new_fig(5.8, 5.8)
        grid_axes(ax, xr, yr, 1, label_every=2)
        xs = [xr[0] + i * (xr[1] - xr[0]) / 400 for i in range(401)]
        for fn, col, ls, lab in ((f_, "#1f4e9c", "-", "y = " + T(fx)), (g_, "#b23a3a", "--", "y = " + T(gx) if gx is not None else None)):
            if fn is None:
                continue
            ys = [fn(v) for v in xs]
            ax.plot([a for a, b in zip(xs, ys) if yr[0] - 1 <= b <= yr[1] + 1], [b for b in ys if yr[0] - 1 <= b <= yr[1] + 1], color=col, lw=2.3, ls=ls, label=lab)
        for p in pts:
            ax.plot([float(p[0])], [float(p[1])], "o", color="black", ms=6, zorder=6)
        ax.set_ylim(*yr)
        ax.legend(loc="upper left", fontsize=10, framealpha=0.95)
        save(fig, path)
    return draw


@fam("012")
def s3_graph(r, L):
    a, b = r.sample(range(-4, 5), 2)
    if L == 0:
        m = rint(r, -3, 3, True)
        c = rint(r, -3, 3)
        fx, gx = m * (x - a) + c, sp.Integer(c) if r.random() < 0.5 else (m + pick(r, [1, -1])) * (x - a) + c
        need(m != 0)
        sols = [a]
        pts = [(a, c)]
    else:
        lead = pick(r, [1, -1]) if L == 1 else pick(r, [1, -1, sp.Rational(1, 2)])
        fx = sp.expand(lead * (x - a) * (x - b))
        gx = sp.Integer(0) if L == 1 else sp.Integer(rint(r, -2, 2))
        sols = [s_ for s_ in sp.solve(sp.Eq(fx, gx), x) if s_.is_real]
        need(all(s_.is_Integer for s_ in sols) and len(sols) == 2 and all(-6 < s_ < 6 for s_ in sols))
        pts = [(s_, gx) for s_ in sols]
        need(all(-8 < fx.subs(x, v) < 8 for v in (-6, 6)) or True)
    st = f"{T(fx)} = {T(gx)}"
    ans = " or ".join(f"x = {T(s_)}" for s_ in sorted(sols))
    alt = f"Graphs of y = {T(fx)} (solid) and y = {T(gx)} (dashed) on a grid from -6 to 6; they intersect at " + ", ".join(f"({T(p[0])}, {T(p[1])})" for p in pts) + "."
    return Q(f"Use the graph to solve {st}.", ans, ["The solutions are the x-coordinates of the intersection points.", "Read each intersection from the graph.", f"{ans}."],
             [" or ".join(f"x = {T(p[1])}" for p in pts) if any(p[1] != p[0] for p in pts) else "x = 0", " or ".join(f"x = {T(-s_)}" for s_ in sols), f"x = {T(fx.subs(x, 0))}"],
             H(f"solve(Eq(P('{T(fx)}'), P('{T(gx)}')), x)", "set"), why=["Gave y-coordinates instead of x-coordinates", "Read the x-values with the wrong sign", "Gave the y-intercept"], tags=["graph"],
             diagram={"alt": alt, "draw": graph_poly(fx, gx, pts=pts)})


@fam("12")
def s3_algebra(r, L):
    a, b = r.sample(range(-6, 7), 2)
    fx = sp.expand((x - a) * (x - b))
    c = rint(r, 1, 6)
    st = f"{T(fx + c)} = {c}"
    return Q(f"Solve {st}. (Check by graphing both sides.)", " or ".join(f"x = {v}" for v in sorted((a, b))), [f"Subtract {c}: {T(fx)} = 0.", f"Factor: {T(sp.factor(fx))} = 0.", f"x = {a} or x = {b}."],
             [" or ".join(f"x = {-v}" for v in sorted((a, b))), f"x = {a}", " or ".join(f"x = {v}" for v in sorted((a + c, b)))], H(f"solve(Eq(P('{T(fx + c)}'), {c}), x)", "set"),
             why=["Used the opposite signs of the factors", "Found only one solution", "Did not subtract the constant first"])


# ============================================================== S4 Applications of Equations
@fam("012")
def s4_apps(r, L):
    kind = pick(r, ["mixture", "distance", "work", "consecutive"] if L else ["distance", "consecutive", "mixture"])
    if kind == "mixture":
        p1, p2 = pick(r, [(10, 40), (20, 50), (15, 35), (5, 30)])
        v1 = rint(r, 2, 12)
        tgt = rint(r, p1 + 1, p2 - 1)
        v2 = sp.Rational(v1 * (tgt - p1), p2 - tgt)
        need(v2.q in (1, 2, 4))
        return Q(f"How many liters of a {p2}% acid solution must be added to {v1} L of a {p1}% solution to make {'an' if str(tgt)[0] == '8' or tgt in (11, 18) else 'a'} {tgt}% solution?", f"{T(v2)} L",
                 [f"Let v be the liters of {p2}% solution.", f"0.{p1:02d}({v1}) + 0.{p2:02d}v = 0.{tgt:02d}({v1} + v).", f"Solve: v = {T(v2)}.", "Check the total acid."],
                 [f"{T(sp.Rational(v1 * (tgt - p1), p2))} L", f"{v1} L", f"{T(sp.Rational(v1 * (p2 - tgt), tgt - p1))} L"], H(f"solve(Eq({p1}*{v1} + {p2}*u, {tgt}*({v1} + u)), u)[0]"),
                 why=["Did not include the added liquid in the total", "Assumed equal amounts", "Set up the ratio upside down"], tags=["modeling"])
    if kind == "distance":
        s1, s2 = rint(r, 30, 60), rint(r, 40, 75)
        tt = sp.Rational(rint(r, 1, 6) * 2 + 1, 2) if L else sp.Integer(rint(r, 2, 6))
        d = (s1 + s2) * tt
        return Q(f"Two cars leave the same town at the same time traveling in opposite directions at {s1} mph and {s2} mph. When will they be {T(d)} miles apart?", f"{T(tt)} hours",
                 ["Distance apart = (sum of speeds) × time.", f"({s1} + {s2})t = {T(d)}.", f"t = {T(tt)} hours."], [f"{T(d / s2)} hours", f"{T(d / abs(s2 - s1)) if s1 != s2 else T(tt * 2)} hours", f"{T(d / (s1 * s2))} hours"],
                 H(f"solve(Eq(({s1} + {s2})*t, {d}), t)[0]"), why=["Used only one speed", "Subtracted the speeds", "Multiplied the speeds"], tags=["modeling"])
    if kind == "work":
        a, b = r.sample([2, 3, 4, 5, 6, 8, 10, 12], 2)
        tt = sp.Rational(a * b, a + b)
        return Q(f"One pump fills a tank in {a} hours and another in {b} hours. How long do they take working together?", f"{T(tt)} hours",
                 [f"Rates: 1/{a} and 1/{b} tank per hour.", f"(1/{a} + 1/{b})t = 1.", f"t = {T(tt)} hours."], [f"{T(sp.Rational(a + b, 2))} hours", f"{a + b} hours", f"{T(sp.Rational(abs(a - b), 1)) if a != b else 1} hours"],
                 H(f"solve(Eq(t/{a} + t/{b}, 1), t)[0]"), why=["Averaged the times", "Added the times", "Subtracted the times"], tags=["modeling"])
    k = rint(r, 2, 4)
    n0 = rint(r, -20, 40)
    s = sum(n0 + 2 * i for i in range(k + 1)) if L == 2 else sum(n0 + i for i in range(k + 1))
    word = "consecutive even" if L == 2 and n0 % 2 == 0 else "consecutive"
    need(word == "consecutive" or n0 % 2 == 0)
    stp = 2 if word.endswith("even") else 1
    return Q(f"The sum of {k + 1} {word} integers is {s}. What is the least integer?", str(n0), [f"Let n be the least: " + " + ".join(f"(n + {stp * i})" if i else "n" for i in range(k + 1)) + f" = {s}.",
                                                                                        f"{k + 1}n + {stp * k * (k + 1) // 2} = {s}.", f"n = {n0}."],
             [str(n0 + stp), str(sp.Rational(s, k + 1)) if s % (k + 1) == 0 and sp.Rational(s, k + 1) != n0 else str(n0 - stp), str(n0 + stp * k)], H(f"solve(Eq({k + 1}*n + {stp * k * (k + 1) // 2}, {s}), n)[0]"),
             why=["Gave the second integer", "Divided the sum by the count", "Gave the greatest integer"], tags=["modeling"])


# ============================================================== S5 Linear, compound, polynomial inequalities
@fam("012")
def s5_ineq(r, L):
    kind = pick(r, ["linear", "compound"]) if L == 0 else pick(r, ["linear", "compound", "poly"]) if L == 1 else pick(r, ["compound", "poly", "cubic"])
    if kind == "linear":
        a = rint(r, -6, 6, True)
        b, c = rint(r, -10, 10), rint(r, -10, 10)
        op = pick(r, ["<", ">", "≤", "≥"])
        st = f"{T(a * x + b)} {op} {c}"
        code = f"ineq_set('{st}')"
        bnd = sp.Rational(c - b, a)
        lc = op in ("≤", "≥")
        right = (op in (">", "≥")) == (a > 0)
        ans = ivl(bnd, sp.oo, lc, False) if right else ivl(-sp.oo, bnd, False, lc)
        wr = [ivl(-sp.oo, bnd, False, lc) if right else ivl(bnd, sp.oo, lc, False), ivl(bnd, sp.oo, not lc, False) if right else ivl(-sp.oo, bnd, False, not lc), ivl(-bnd, sp.oo, lc, False) if right and bnd else ivl(-sp.oo, -bnd if bnd else 1, False, lc)]
        why = ["Did not reverse the sign when dividing by a negative" if a < 0 else "Reversed the inequality sign", "Used the wrong bracket for the endpoint", "Made a sign error"]
    elif kind == "compound":
        a = rint(r, 1, 5)
        b = rint(r, -8, 8)
        lo, hi = sorted(r.sample(range(-15, 16), 2))
        need((lo - b) % a == 0 and (hi - b) % a == 0)
        o1, o2 = pick(r, ["<", "≤"]), pick(r, ["<", "≤"])
        st = f"{lo} {o1} {T(a * x + b)} {o2} {hi}"
        code = f"ineq_set('{lo} {o1} {T(a * x + b)}').intersect(ineq_set('{T(a * x + b)} {o2} {hi}'))"
        L_, R_ = sp.Rational(lo - b, a), sp.Rational(hi - b, a)
        ans = ivl(L_, R_, o1 == "≤", o2 == "≤")
        wr = [ivl(L_, R_, o1 != "≤", o2 != "≤"), ivl(lo - b, hi - b, o1 == "≤", o2 == "≤") if a > 1 else ivl(L_ - 1, R_, o1 == "≤", o2 == "≤"), ivl(-sp.oo, L_, False, o1 == "≤") + " ∪ " + ivl(R_, sp.oo, o2 == "≤", False)]
        why = ["Used the wrong brackets", "Forgot to divide every part by the coefficient", "Wrote the outside of the interval"]
    elif kind == "poly":
        a, b = sorted(r.sample(range(-7, 8), 2))
        op = pick(r, ["<", ">", "≤", "≥"])
        fx = sp.expand((x - a) * (x - b))
        st = f"{T(fx)} {op} 0"
        code = f"ineq_set('{st}')"
        cl = op in ("≤", "≥")
        inside = op in ("<", "≤")
        ans = ivl(a, b, cl, cl) if inside else ivl(-sp.oo, a, False, cl) + " ∪ " + ivl(b, sp.oo, cl, False)
        wr = [ivl(-sp.oo, a, False, cl) + " ∪ " + ivl(b, sp.oo, cl, False) if inside else ivl(a, b, cl, cl), ivl(a, b, not cl, not cl) if inside else ivl(-sp.oo, a, False, not cl) + " ∪ " + ivl(b, sp.oo, not cl, False),
              ivl(-b, -a, cl, cl) if inside else ivl(-sp.oo, -b, False, cl) + " ∪ " + ivl(-a, sp.oo, cl, False)]
        why = ["Tested the wrong sign region", "Used the wrong brackets", "Used the opposites of the zeros"]
    else:
        a, b, c = sorted(r.sample(range(-6, 7), 3))
        fx = sp.expand((x - a) * (x - b) * (x - c))
        op = pick(r, [">", "≥", "<"])
        st = f"{T(fx)} {op} 0"
        code = f"ineq_set('{st}')"
        cl = op == "≥"
        if op in (">", "≥"):
            ans = ivl(a, b, cl, cl) + " ∪ " + ivl(c, sp.oo, cl, False)
            wr = [ivl(-sp.oo, a, False, cl) + " ∪ " + ivl(b, c, cl, cl), ivl(c, sp.oo, cl, False), ivl(a, c, cl, cl)]
        else:
            ans = ivl(-sp.oo, a, False, False) + " ∪ " + ivl(b, c, False, False)
            wr = [ivl(a, b, False, False) + " ∪ " + ivl(c, sp.oo, False, False), ivl(-sp.oo, a, False, False), ivl(a, c, False, False)]
        why = ["Tested the wrong sign regions", "Missed an interval", "Ignored the middle zero"]
    return Q(f"Solve {st}. Write the answer in interval notation.", ans, ["Find the boundary values.", "Test a value in each region (or reason about the sign).", "Use ( ) for excluded and [ ] for included endpoints.", f"{ans}."],
             wr, H(code, "interval"), why=why)


# ============================================================== S6 Interval notation
@fam("012")
def s6_convert(r, L):
    a, b = sorted(r.sample(range(-12, 13), 2))
    kind = pick(r, ["one", "two", "or"]) if L else pick(r, ["one", "two"])
    if kind == "one":
        op = pick(r, ["<", ">", "≤", "≥"])
        st = f"x {op} {a}"
        cl = op in ("≤", "≥")
        ans = ivl(a, sp.oo, cl, False) if op in (">", "≥") else ivl(-sp.oo, a, False, cl)
        wr = [ivl(-sp.oo, a, False, cl) if op in (">", "≥") else ivl(a, sp.oo, cl, False), ivl(a, sp.oo, not cl, False) if op in (">", "≥") else ivl(-sp.oo, a, False, not cl), f"[{a}, ∞]" if op in (">", "≥") else f"[-∞, {a}]"]
        code = f"ineq_set('{st}')"
    elif kind == "two":
        o1, o2 = pick(r, ["<", "≤"]), pick(r, ["<", "≤"])
        st = f"{a} {o1} x {o2} {b}"
        ans = ivl(a, b, o1 == "≤", o2 == "≤")
        wr = [ivl(a, b, o1 != "≤", o2 != "≤"), f"{'(' if o1 == '<' else '['}{b}, {a}{')' if o2 == '<' else ']'}", ivl(-sp.oo, a, False, o1 == "≤") + " ∪ " + ivl(b, sp.oo, o2 == "≤", False)]
        code = f"ineq_set('{a} {o1} x').intersect(ineq_set('x {o2} {b}'))"
    else:
        st = f"x < {a} or x ≥ {b}"
        ans = ivl(-sp.oo, a, False, False) + " ∪ " + ivl(b, sp.oo, True, False)
        wr = [ivl(a, b, False, True), ivl(-sp.oo, a, False, True) + " ∪ " + ivl(b, sp.oo, False, False), f"(-∞, {a}) ∩ [{b}, ∞)"]
        code = f"Union(ineq_set('x < {a}'), ineq_set('x ≥ {b}'))"
    return Q(f"Write {st} in interval notation.", ans, ["Use ( ) when an endpoint is not included and [ ] when it is.", "∞ and -∞ always get parentheses.", "Use ∪ to join two separate pieces." if "∪" in ans else f"{ans}."],
             wr, H(code, "interval"), why=["Pointed the interval the wrong way", "Used the wrong bracket", "Wrote a bracket on infinity" if kind == "one" else "Wrote the complement"])


@fam("12")
def s6_from_graph(r, L):
    a, b = sorted(r.sample(range(-6, 7), 2))
    ca, cb = r.random() < 0.5, r.random() < 0.5
    alt = f"Number line from -8 to 8 with a segment from {a} to {b}; {'closed' if ca else 'open'} circle at {a} and {'closed' if cb else 'open'} circle at {b}."
    ans = ivl(a, b, ca, cb)
    return Q("Write the set shown on the number line in interval notation.", ans, ["Closed circle → [ or ]; open circle → ( or ).", f"{ans}."],
             [ivl(a, b, not ca, not cb), ivl(-sp.oo, a, False, ca) + " ∪ " + ivl(b, sp.oo, cb, False), f"{'[' if cb else '('}{b}, {a}{']' if ca else ')'}"],
             H(f"Interval({a}, {b}, left_open={not ca}, right_open={not cb})", "interval"), why=["Mixed up open and closed circles", "Wrote the outside region", "Reversed the endpoints"], tags=["graph"],
             diagram={"alt": alt, "draw": numline_draw(-8, 8, seg=(a, b, ca, cb))})


# ============================================================== S8 Systems in two variables
@fam("012")
def s8_system(r, L):
    x0, y0 = (rint(r, -8, 8), rint(r, -8, 8)) if L < 2 else (sp.Rational(rint(r, -9, 9), 2), sp.Rational(rint(r, -9, 9), 3))
    while True:
        a1, b1, a2, b2 = [rint(r, -6, 6, True) for _ in range(4)]
        if a1 * b2 - a2 * b1:
            break
    if L == 0:
        b1 = 1
        need(a1 * b2 - a2 * b1 != 0)
    c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
    need(sp.nsimplify(c1).q <= 6 and sp.nsimplify(c2).q <= 6)
    e1, e2 = f"{T(a1 * x + b1 * y)} = {T(c1)}", f"{T(a2 * x + b2 * y)} = {T(c2)}"
    ans = f"({T(x0)}, {T(y0)})"
    return Q(f"Solve the system: {e1} and {e2}.", ans, ["Use substitution or elimination.", "Eliminate one variable and solve for the other.", "Substitute back to find the remaining variable.", f"Solution: {ans}."],
             [f"({T(y0)}, {T(x0)})", f"({T(-x0)}, {T(y0)})", f"({T(x0)}, {T(-y0)})" if y0 else f"({T(x0)}, 1)"], H(f"[s_[X] for s_ in [solve([P('{T(a1 * x + b1 * y)}') - ({c1}), P('{T(a2 * x + b2 * y)}') - ({c2})], [x, y], dict=True)[0]] for X in (x, y)][0]" if False else
                                                                                                              f"(lambda s_: [s_[x], s_[y]])(solve([P('{T(a1 * x + b1 * y)}') - ({c1}), P('{T(a2 * x + b2 * y)}') - ({c2})], [x, y], dict=True)[0])", "point"),
             why=["Switched x and y", "Made a sign error in x", "Made a sign error in y"], tags=["multistep"])


@fam("12")
def s8_context(r, L):
    a, b = rint(r, 5, 40), rint(r, 5, 40)
    pa, pb = rint(r, 8, 20), rint(r, 3, 7)
    return Q(f"A school sold {a + b} tickets for ${pa * a + pb * b}. Adult tickets were ${pa} and student tickets were ${pb}. How many adult tickets were sold?", str(a),
             [f"a + s = {a + b} and {pa}a + {pb}s = {pa * a + pb * b}.", f"Substitute s = {a + b} - a.", f"{pa - pb}a = {pa * a + pb * b - pb * (a + b)}.", f"a = {a}."],
             [str(b), str((pa * a + pb * b) // pa), str((a + b) // 2)], H(f"solve([Eq(x + y, {a + b}), Eq({pa}*x + {pb}*y, {pa * a + pb * b})], [x, y], dict=True)[0][x]"),
             why=["Gave the number of student tickets", "Divided the total by the adult price", "Split the tickets evenly"], tags=["modeling"])


# ============================================================== S9 Systems in three variables
@fam("012")
def s9_three(r, L):
    sol = [rint(r, -5, 5) for _ in range(3)]
    for _ in range(50):
        A = sp.Matrix(3, 3, [rint(r, -3, 3) if L else rint(r, 0, 3) for _ in range(9)])
        if A.det() != 0 and all(any(A.row(i)) for i in range(3)):
            break
    else:
        raise Reject()
    if L == 0:
        A[0, :] = sp.Matrix([[1, 1, 1]])
        need(A.det() != 0)
    b = A * sp.Matrix(sol)
    z = sp.Symbol("z", real=True)
    eqs = [f"{T(A[i, 0] * x + A[i, 1] * y + A[i, 2] * z)} = {b[i]}" for i in range(3)]
    ans = f"({sol[0]}, {sol[1]}, {sol[2]})"
    return Q(f"Solve the system: {'; '.join(eqs)}. Give the answer as (x, y, z).", ans, ["Use two pairs of equations to eliminate the same variable.", "Solve the resulting system of two equations.", "Substitute back to find the third variable.",
                                                                                        f"Solution: {ans}."],
             [f"({sol[1]}, {sol[0]}, {sol[2]})", f"({-sol[0]}, {sol[1]}, {sol[2]})", f"({sol[0]}, {sol[1]}, {-sol[2] if sol[2] else 1})"],
             H("(lambda z: (lambda s_: [s_[x], s_[y], s_[z]])(solve([" + ", ".join(f"Eq(P('{e.split(' = ')[0]}'.replace('z','*Z')) if False else 0, 0)" for e in eqs[:0]) +
               ", ".join(f"Eq({A[i, 0]}*x + ({A[i, 1]})*y + ({A[i, 2]})*z, {b[i]})" for i in range(3)) + "], [x, y, z], dict=True)[0]))(Symbol('z', real=True))", "point"),
             why=["Switched x and y", "Made a sign error in x", "Made a sign error in z"], tags=["multistep"])


# ============================================================== S10 Systems of linear inequalities / S11 Linear programming
def region(r):
    """Feasible polygon from x ≥ 0, y ≥ 0, a1x + b1y ≤ c1, a2x + b2y ≤ c2 with integer vertices."""
    for _ in range(80):
        p, q = rint(r, 2, 9), rint(r, 2, 9)
        s_, t_ = rint(r, 2, 9), rint(r, 2, 9)
        vx = sp.Rational(q * t_ - 0, 1)
        c = [(q, p, p * q), (t_, s_, s_ * t_)]   # x/p + y/q ≤ 1 → qx + py ≤ pq ; x/s + y/t ≤ 1
        A = sp.Matrix([[q, p], [t_, s_]])
        if A.det() == 0:
            continue
        sol = A.solve(sp.Matrix([p * q, s_ * t_]))
        if not (sol[0] > 0 and sol[1] > 0 and sol[0].q == 1 and sol[1].q == 1):
            continue
        verts = [(0, 0), (min(p, s_), 0), (sol[0], sol[1]), (0, min(q, t_))]
        if (p - s_) * (q - t_) >= 0:
            continue
        return c, verts
    raise Reject()


@fam("012")
def s10_test(r, L):
    c, verts = region(r)
    px, py = rint(r, 0, 9), rint(r, 0, 9)
    ok = all(a * px + b * py <= cc for a, b, cc in c)
    ineqs = ["x ≥ 0", "y ≥ 0"] + [f"{T(a * x + b * y)} ≤ {cc}" for a, b, cc in c]
    return Q(f"Is ({px}, {py}) a solution of the system {', '.join(ineqs)}?", "Yes" if ok else "No", ["Substitute the point into every inequality.", "A solution must satisfy all of them.", "Yes" if ok else "No: at least one inequality is false."],
             ["No" if ok else "Yes"], H(f"'Yes' if all([{', '.join(f'{a}*{px} + {b}*{py} <= {cc}' for a, b, cc in c)}]) else 'No'", "text"), mode="sa", why=["Checked only one inequality"])


@fam("012")
def s10_vertex(r, L):
    c, verts = region(r)
    (a1, b1, c1), (a2, b2, c2) = c
    vx, vy = verts[2]
    return Q(f"The region x ≥ 0, y ≥ 0, {T(a1 * x + b1 * y)} ≤ {c1}, {T(a2 * x + b2 * y)} ≤ {c2} has a corner where the two slanted boundary lines meet. Find that vertex.", f"({T(vx)}, {T(vy)})",
             [f"Solve {T(a1 * x + b1 * y)} = {c1} and {T(a2 * x + b2 * y)} = {c2} together.", "Use elimination.", f"Vertex: ({T(vx)}, {T(vy)})."],
             [f"({T(vy)}, {T(vx)})", f"({T(sp.Rational(c1, a1))}, 0)", f"(0, {T(sp.Rational(c2, b2))})"], H(f"(lambda s_: [s_[x], s_[y]])(solve([Eq({a1}*x + {b1}*y, {c1}), Eq({a2}*x + {b2}*y, {c2})], [x, y], dict=True)[0])", "point"),
             why=["Switched the coordinates", "Gave an x-intercept of one boundary", "Gave a y-intercept of one boundary"], tags=["multistep"])


@fam("012")
def s11_lp(r, L):
    c, verts = region(r)
    pa, pb = rint(r, 1, 9), rint(r, 1, 9)
    goal = pick(r, ["maximum", "minimum"]) if L == 2 else "maximum"
    vals = [(pa * vx + pb * vy, (vx, vy)) for vx, vy in verts]
    best = max(vals)[0] if goal == "maximum" else min(v for v in vals if v[1] != (0, 0))[0] if False else (max(vals)[0] if goal == "maximum" else min(vals)[0])
    (a1, b1, c1), (a2, b2, c2) = c
    ineqs = f"x ≥ 0, y ≥ 0, {T(a1 * x + b1 * y)} ≤ {c1}, {T(a2 * x + b2 * y)} ≤ {c2}"
    need(goal == "maximum" or best != 0 or True)
    other = sorted({v for v, _ in vals} - {best})
    return Q(f"Find the {goal} value of P = {T(pa * x + pb * y)} subject to {ineqs}.", str(best),
             [f"The vertices of the feasible region are " + ", ".join(f"({T(a)}, {T(b)})" for a, b in verts) + ".", "Evaluate P at each vertex: " + ", ".join(f"P({T(a)}, {T(b)}) = {T(v)}" for v, (a, b) in vals) + ".",
              f"The {goal} is {best}.", "The optimum of a linear objective occurs at a vertex."],
             [str(v) for v in other[-3:]] + [str(best + pa)], H(f"lp({pa}, {pb}, {[[a, b, cc] for a, b, cc in c]}, '{goal}')"),
             why=["Evaluated a vertex that is not the optimum"] * 3 + [""], tags=["modeling", "multistep"])


SKILLS = {
    1: dict(name="Writing Linear Equations", std=["F-LE.A.2", "A-CED.A.2"], fams=[s1_two_points, s1_standard, s1_context], extra=[err_of(s1_two_points), open_of(s1_two_points), select_of(s1_standard)]),
    2: dict(name="Parallel and Perpendicular Lines", std=["G-GPE.B.5"], fams=[s2_line, s2_classify], extra=[err_of(s2_line), open_of(s2_line)]),
    3: dict(name="Solving Equations Graphically", std=["A-REI.D.11"], fams=[s3_graph, s3_algebra], extra=[err_of(s3_graph), open_of(s3_algebra)]),
    4: dict(name="Applications of Equations", std=["A-CED.A.1", "A-CED.A.3"], fams=[s4_apps], extra=[err_of(s4_apps), open_of(s4_apps)]),
    5: dict(name="Linear, Compound, and Polynomial Inequalities", std=["A-REI.B.3", "A-APR.B.3"], fams=[s5_ineq], extra=[err_of(s5_ineq), open_of(s5_ineq)]),
    6: dict(name="Interval Notation", std=["F-IF.A.1"], fams=[s6_convert, s6_from_graph], extra=[err_of(s6_convert), open_of(s6_convert), select_of(s6_convert)]),
    7: dict(name="Graphing Linear Inequalities", std=["A-REI.D.12"], fams=[reuse(L7.s8_point, (1, 1, 2), "p"), reuse(L7.s8_which, (1, 1, 2), "p"), reuse(L7.s8_boundary, (1, 1, 2), "p")],
            extra=[err_of(reuse(L7.s8_point, (1, 1, 2), "pe")), open_of(reuse(L7.s8_point, (1, 1, 2), "po"))]),
    8: dict(name="Systems of Equations in Two Variables", std=["A-REI.C.6"], fams=[s8_system, s8_context], extra=[err_of(s8_system), open_of(s8_system), select_of(s8_system)]),
    9: dict(name="Systems of Equations in Three Variables", std=["A-REI.C.6", "A-REI.C.9"], fams=[s9_three], extra=[err_of(s9_three), open_of(s9_three)]),
    10: dict(name="Systems of Linear Inequalities", std=["A-REI.D.12"], fams=[s10_test, s10_vertex], extra=[err_of(s10_vertex), open_of(s10_test)]),
    11: dict(name="Linear Programming", std=["A-CED.A.3"], fams=[s11_lp, s10_vertex], extra=[err_of(s11_lp), open_of(s11_lp)]),
}
