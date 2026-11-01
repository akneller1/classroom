"""Unit 4 — Systems of Linear Equations (systems-linear-equations)."""
from lib import *

UNIT_ID = "systems-linear-equations"
ABBR = "sys"


def yeq(m, b):
    return f"y = {mx_b(m, b)}"


def std(a, b, c):
    return f"{lin((a, 'x'), (b, 'y'))} = {N(c)}"


def sys_txt(e1, e2):
    return f"{e1} and {e2}"


def rand_si(r, int_slope=True, rng=4):
    m = F(nz(r, -rng, rng)) if int_slope else F(nz(r, -5, 5), pick(r, [1, 2, 3]))
    return m, F(r.randint(-6, 6))


def two_lines(r, x0, y0, int_slope=True):
    for _ in range(50):
        m1 = F(nz(r, -3, 3)) if int_slope else F(nz(r, -4, 4), pick(r, [1, 2]))
        m2 = F(nz(r, -3, 3)) if int_slope else F(nz(r, -4, 4), pick(r, [1, 2, 3]))
        if m1 != m2:
            b1, b2 = y0 - m1 * x0, y0 - m2 * x0
            if b1.denominator == 1 and b2.denominator == 1 and abs(b1) <= 9 and abs(b2) <= 9:
                return (m1, b1), (m2, b2)
    raise Reject()


def std_from_point(r, x0, y0, avoid=None):
    for _ in range(50):
        a, b = nz(r, -6, 6), nz(r, -6, 6)
        if math.gcd(abs(a), abs(b)) != 1:
            continue
        if avoid and F(a, b) == F(avoid[0], avoid[1]):
            continue
        return a, b, a * x0 + b * y0
    raise Reject()


# ======================================================================= S1 Graphing in slope-intercept form
@fam("012")
def s1_identify(r, L):
    m, b = rand_si(r, int_slope=L == 0)
    if L == 2:
        a, bb = nz(r, -6, 6), nz(r, -6, 6)
        c = r.randint(-12, 12)
        m, b = F(-a, bb), F(c, bb)
        shown = std(a, bb, c)
        steps = [f"Solve for y: {coef_text(bb, 'y')} = {lin((-a, 'x'), (c, ''))}, so y = {mx_b(m, b)}."]
    else:
        shown = yeq(m, b) if r.random() < 0.6 else f"y = {lin((b, ''), (m, 'x'))}"
        steps = []
    ans = f"slope {N(m)}, y-intercept {N(b)}"
    return P(f"To graph {shown}, what are the slope and the y-intercept?", ans, steps + [f"In y = mx + b form, m = {N(m)} and b = {N(b)}."],
             [f"slope {N(b)}, y-intercept {N(m)}", f"slope {N(-m)}, y-intercept {N(b)}", f"slope {N(m)}, y-intercept {N(-b)}" if b else f"slope {N(m + 1)}, y-intercept 0"],
             chk_py("slope_int_text", eq=shown), tags=["misconception"])


@fam("012")
def s1_next_point(r, L):
    m, b = rand_si(r, int_slope=L == 0)
    need(m != 0)
    k = pick(r, [1, 2]) if L == 2 else 1
    p = (m.denominator * k, b + m.numerator * k)
    return P(f"To graph y = {mx_b(m, b)}, Lea plots the y-intercept and then uses the slope once{' and then again' if k == 2 else ''}, moving right. What point does she reach?",
             pt(*p), [f"Start at (0, {N(b)}).", f"Slope {N(m)} = rise {m.numerator} over run {m.denominator}" + (", twice." if k == 2 else "."), f"Point {pt(*p)}."],
             [pt(b + m.numerator * k, m.denominator * k), pt(m.denominator * k, b - m.numerator * k), pt(m.numerator * k, b + m.denominator * k) if m.numerator != m.denominator else pt(k, b)],
             chk_py("on_graph", eq=yeq(m, b)), tags=["graph"])


@fam("012", mode="mc")
def s1_match(r, L):
    m, b = rand_si(r, int_slope=True)
    need(b != 0 and abs(m) != abs(b))
    cands = [(m, b), (m, -b), (-m, b), (b, m) if abs(b) <= 4 else (-m, -b)]
    need(len(set(cands)) == 4)
    order = [0, 1, 2, 3]
    r.shuffle(order)
    good = "ABCD"[order.index(0)]
    alt = "Four line graphs: " + "; ".join(f"Graph {l}: y = {mx_b(*cands[i])}" for l, i in zip("ABCD", order))
    shown = yeq(m, b) if L < 2 else std(-m.numerator, 1, b)
    return P(f"Which graph shows {shown}?", f"Graph {good}", [f"{'Rewrite: y = ' + mx_b(m, b) + '. ' if L == 2 else ''}y-intercept {N(b)}, slope {N(m)}.", f"Graph {good}."],
             options=[(f"Graph {l}", l == good) for l in "ABCD"], chk=chk_py("panel_line", lines=[[N(cands[i][0]), N(cands[i][1])] for i in order], eq=shown),
             diagram={"draw": panels_draw([plane_draw(lines=[cands[i]], label_every=2) for i in order]), "alt": alt}, tags=["graph"], mode="mc")


@fam("12")
def s1_rewrite(r, L):
    a, bb = nz(r, -6, 6), nz(r, -6, 6)
    c = bb * r.randint(-5, 5)
    need(a % bb == 0 or L == 2)
    m, b = F(-a, bb), F(c, bb)
    ans = yeq(m, b)
    return P(f"Rewrite {std(a, bb, c)} in slope-intercept form so it can be graphed.", ans, [f"Subtract {coef_text(a, 'x')} from both sides, then divide by {bb}.", ans],
             [yeq(-m, b), yeq(m, -b) if b else yeq(m, F(1)), yeq(F(a, bb), F(c))], {"kind": "equiv", "expr": mx_b(m, b), "vars": ["x"]}, tags=["multiple-representations"])


@fam("2")
def s1_from_graph_two(r, L):
    m, b = rand_si(r, int_slope=False)
    x1 = m.denominator * 2
    need(abs(float(m * x1 + b)) <= 7 and abs(float(m * -x1 + b)) <= 7)
    p1, p2 = (-x1, m * -x1 + b), (x1, m * x1 + b)
    drw = plane_draw(lines=[(m, b)], points=[(p1[0], p1[1], pt(*p1)), (p2[0], p2[1], pt(*p2))])
    return P("The graph shows a line through two labeled points. Write its equation in slope-intercept form.", yeq(m, b),
             [f"slope = ({N(p2[1])} - {paren(p1[1])}) ÷ ({x1} - ({-x1})) = {N(m)}.", f"Midway point gives b = {N(b)}.", yeq(m, b)],
             [yeq(1 / m, b), yeq(-m, b), yeq(m, b + 1)], chk_py("line_through", pts=[[N(p1[0]), N(p1[1])], [N(p2[0]), N(p2[1])]]),
             diagram={"draw": drw, "alt": f"A line through the labeled points {pt(*p1)} and {pt(*p2)}."}, tags=["graph"])


@fam("012")
def s1_error(r, L):
    m, b = rand_si(r)
    need(b != 0 and m != b)
    return P(f"To graph y = {mx_b(m, b)}, Gus plotted (0, {N(m)}) as the first point. Which point should he plot as the y-intercept?", pt(0, b),
             ["Gus used the slope as the y-intercept.", f"The y-intercept is the constant term: (0, {N(b)})."],
             [pt(0, m), pt(b, 0), pt(m, b)], chk_py("intercept_pt", eq=yeq(m, b), which="y"), tags=["error-analysis", "misconception"])


@fam("012")
def s1_select(r, L):
    m, b = rand_si(r)
    xs = r.sample(range(-5, 6), 6)
    opts = [(pt(x, m * x + b + (0 if i < 3 else nz(r, -2, 2))), i < 3) for i, x in enumerate(xs)]
    return P(f"Select ALL points that lie on the graph of y = {mx_b(m, b)}.", None, ["Substitute each point into the equation."], options=opts,
             chk=chk_py("on_graph", eq=yeq(m, b)), tags=["graph"])


@fam("012")
def s1_open(r, L):
    m, b = rand_si(r, int_slope=L < 2)
    need(m != 0)
    return P(f"Graph y = {mx_b(m, b)} using the slope and y-intercept.", None, ["Constant term.", "Coefficient.", "Rise/run from the intercept.", "Set y = 0."],
             parts=[("What point do you plot first?", pt(0, b), chk_py("intercept_pt", eq=yeq(m, b), which="y")), ("What is the slope?", N(m), chk_val(N(m))),
                    ("Name a second point by moving one slope step to the right.", pt(m.denominator, b + m.numerator), chk_py("on_graph", eq=yeq(m, b))),
                    ("Where does the line cross the x-axis?", pt(-b / m, 0), chk_py("intercept_pt", eq=yeq(m, b), which="x"))], tags=["graph"])


# ======================================================================= S2 Solving systems by graphing
def sys_graph(r, L):
    x0, y0 = r.randint(-4, 4), r.randint(-4, 4)
    (m1, b1), (m2, b2) = two_lines(r, x0, y0, int_slope=L < 2)
    return x0, y0, (m1, b1), (m2, b2)


@fam("012")
def s2_read(r, L):
    x0, y0, l1, l2 = sys_graph(r, L)
    e1, e2 = yeq(*l1), yeq(*l2)
    drw = plane_draw(lines=[(l1[0], l1[1], COLORS[0], e1), (l2[0], l2[1], COLORS[1], e2)])
    return P(f"The graph shows the system {sys_txt(e1, e2)}. What is the solution of the system?", pt(x0, y0),
             ["The solution is the point where the lines intersect.", f"Check: {pt(x0, y0)} satisfies both equations."],
             [pt(y0, x0) if x0 != y0 else pt(x0 + 1, y0), pt(0, l1[1]), pt(0, l2[1]) if l2[1] != l1[1] else pt(x0, y0 + 1)], {"kind": "sys", "eqs": [e1, e2]},
             diagram={"draw": drw, "alt": f"Line {e1} (solid) and line {e2} (dashed) crossing at {pt(x0, y0)}."}, tags=["graph"])


@fam("012", mode="mc")
def s2_special(r, L):
    m, b = rand_si(r)
    kind = pick(r, ["none", "all", "one"])
    if kind == "none":
        b2 = b + nz(r, -4, 4)
        e2 = yeq(m, b2)
        lines = [(m, b), (m, b2)]
    elif kind == "all":
        k = pick(r, [2, 3, -2])
        e2 = f"{lin((-m * k, 'x'), (k, 'y'))} = {N(b * k)}"
        lines = [(m, b), (m, b)]
    else:
        x0 = r.randint(-3, 3)
        y0 = m * x0 + b
        m2 = m + pick(r, [1, -1, 2])
        e2 = yeq(m2, y0 - m2 * x0)
        lines = [(m, b), (m2, y0 - m2 * x0)]
    e1 = yeq(m, b)
    want = {"none": "no solution", "all": "infinitely many solutions", "one": "exactly one solution"}[kind]
    drw = plane_draw(lines=[(lines[0][0], lines[0][1], COLORS[0], e1), (lines[1][0], lines[1][1], COLORS[1], e2)])
    opts = [(t, t == want) for t in ["exactly one solution", "no solution", "infinitely many solutions", "exactly two solutions"]]
    return P(f"The system {sys_txt(e1, e2)} is graphed. How many solutions does it have?", want,
             [{"none": "The lines are parallel (same slope, different intercepts): they never meet.", "all": "Both equations describe the same line: every point on it is a solution.",
               "one": "Different slopes: the lines cross at exactly one point."}[kind]], options=opts, chk=chk_py("sys_count", eqs=[e1, e2]),
             diagram={"draw": drw, "alt": f"Graph of {e1} (solid) and {e2} (dashed)" + (", which are parallel." if kind == "none" else ", which coincide." if kind == "all" else ", which intersect once.")},
             tags=["graph", "reasoning"], mode="mc")


@fam("012", mode="mc")
def s2_check(r, L):
    x0, y0, l1, l2 = sys_graph(r, L)
    e1 = yeq(*l1)
    a, b, c = std_from_point(r, x0, y0, avoid=(-l1[0].numerator, l1[0].denominator) if False else None)
    e2 = std(a, b, c)
    need(F(-a, b) != l1[0])
    cands = [(x0, y0), (x0 + 1, l1[0] * (x0 + 1) + l1[1]), (y0, x0), (x0, y0 + 2)]
    need(len(set(cands)) == 4)
    opts = [(pt(*p), i == 0) for i, p in enumerate(cands)]
    r.shuffle(opts)
    return P(f"Which point is the solution of the system {sys_txt(e1, e2)}?", pt(x0, y0),
             ["A solution must make BOTH equations true.", f"{pt(x0, y0)}: {N(l1[0] * x0 + l1[1])} = {y0} ✓ and {a}({x0}) + {b}({y0}) = {c} ✓."],
             options=opts, chk={"kind": "sys", "eqs": [e1, e2]}, tags=["reasoning"], mode="mc")


@fam("12")
def s2_context_graph(r, L):
    f1, r1 = r.randint(0, 3) * 10, r.randint(2, 6) * 5
    r2 = r1 + r.randint(1, 4) * 5
    t = r.randint(2, 6)
    f2 = f1 + r1 * t - r2 * t
    need(f2 >= 0)
    drw = plane_draw(xr=(0, 10), yr=(0, float(f2 + r2 * 10) + 10), lines=[(F(r1), F(f1), COLORS[0], "Plan A"), (F(r2), F(f2), COLORS[1], "Plan B")], data=True, xstep=1,
                     ystep=float(max(10, round((f2 + r2 * 10) / 8, -1))), xlabel="months", ylabel="total cost ($)")
    return P(f"Plan A costs ${f1} plus ${r1} per month. Plan B costs {'$' + str(f2) + ' plus ' if f2 else ''}${r2} per month. The graph shows both plans. After how many months do the plans cost the same, and what is that cost?",
             f"{t} months, ${f1 + r1 * t}", [f"The lines cross at ({t}, {f1 + r1 * t}).", f"Check: {f1} + {r1}({t}) = {f2} + {r2}({t}) = {f1 + r1 * t}."],
             [f"{f1 + r1 * t} months, ${t}", f"{t + 1} months, ${f1 + r1 * (t + 1)}", f"{t} months, ${f2 + r1 * t}"],
             chk_py("sys_ctx_pair", eqs=[f"y = {r1}x + {f1}", f"y = {r2}x + {f2}"], fmt="{x} months, ${y}"),
             diagram={"draw": drw, "alt": f"Plan A: y = {r1}x + {f1}; Plan B: y = {r2}x + {f2}; the lines cross at ({t}, {f1 + r1 * t})."}, tags=["graph", "modeling"])


@fam("2")
def s2_estimate(r, L):
    x0 = F(r.randint(-7, 7), 2)
    need(x0.denominator == 2)
    m1, m2 = F(nz(r, -2, 2)), F(nz(r, -2, 2))
    need(m1 != m2 and m1 != -m2)
    y0 = F(r.randint(-3, 3))
    b1, b2 = y0 - m1 * x0, y0 - m2 * x0
    e1, e2 = yeq(m1, b1), yeq(m2, b2)
    drw = plane_draw(lines=[(m1, b1, COLORS[0], e1), (m2, b2, COLORS[1], e2)])
    return P(f"The graph of {sys_txt(e1, e2)} crosses between grid lines. Use the equations to find the exact solution.", pt(x0, y0),
             [f"Set {mx_b(m1, b1)} = {mx_b(m2, b2)}.", f"x = {N(x0)}, then y = {N(y0)}.", "A graph only estimates; algebra gives the exact point."],
             [pt(round(x0), y0), pt(x0, y0 + 1), pt(y0, x0)], {"kind": "sys", "eqs": [e1, e2]}, diagram={"draw": drw, "alt": f"Lines {e1} and {e2} crossing at {pt(x0, y0)}, between grid points."},
             tags=["graph", "challenge"])


@fam("012")
def s2_error(r, L):
    x0, y0, l1, l2 = sys_graph(r, 1)
    need(l1[1] != y0 and x0 != 0)
    e1, e2 = yeq(*l1), yeq(*l2)
    drw = plane_draw(lines=[(l1[0], l1[1], COLORS[0], e1), (l2[0], l2[1], COLORS[1], e2)])
    return P(f"Omar says the solution of {sys_txt(e1, e2)} is (0, {N(l1[1])}), the point where the solid line crosses the y-axis. What is the correct solution?", pt(x0, y0),
             ["A y-intercept of one line is not a solution unless the other line passes through it too.", f"The lines intersect at {pt(x0, y0)}."],
             [pt(0, l1[1]), pt(0, l2[1]), pt(y0, x0) if x0 != y0 else pt(x0, y0 + 1)], {"kind": "sys", "eqs": [e1, e2]},
             diagram={"draw": drw, "alt": f"Line {e1} (solid) and {e2} (dashed) intersecting at {pt(x0, y0)}."}, tags=["error-analysis", "graph"])


@fam("012")
def s2_select(r, L):
    x0, y0 = r.randint(-3, 3), r.randint(-3, 3)
    eqs = []
    for k in range(3):
        a, b, c = std_from_point(r, x0, y0)
        eqs.append((std(a, b, c), True))
    for k in range(3):
        a, b, c = std_from_point(r, x0, y0)
        eqs.append((std(a, b, c + nz(r, -3, 3)), False))
    need(len({e for e, _ in eqs}) == 6)
    return P(f"The point {pt(x0, y0)} is the solution of a system. Select ALL equations that could be in that system (that pass through the point).", None,
             ["Substitute the point into each equation."], options=eqs, chk=chk_py("eq_has_point", p=[x0, y0]), tags=["reasoning"])


@fam("012")
def s2_open(r, L):
    x0, y0, l1, l2 = sys_graph(r, 0)
    e1, e2 = yeq(*l1), yeq(*l2)
    return P(f"Solve the system {sys_txt(e1, e2)} by graphing.", None, ["y-intercept of line 1.", "y-intercept of line 2.", "Intersection.", "Check."],
             parts=[(f"What is the y-intercept of {e1}?", N(l1[1]), chk_val(N(l1[1]))), (f"What is the y-intercept of {e2}?", N(l2[1]), chk_val(N(l2[1]))),
                    ("Where do the lines intersect?", pt(x0, y0), {"kind": "sys", "eqs": [e1, e2]}),
                    (f"Substitute the solution into {e2}. What value of y does it give?", str(y0), chk_val(f"{N(l2[0])}*({x0}) + {N(l2[1])}"))], tags=["graph"])


# ======================================================================= S3 Substitution
def rand_sol(r, L):
    return (F(r.randint(-6, 8)), F(r.randint(-6, 8))) if L < 2 else (F(r.randint(-12, 12), pick(r, [1, 2, 3])), F(r.randint(-8, 8), pick(r, [1, 2])))


@fam("012")
def s3_solve(r, L):
    x0, y0 = rand_sol(r, L)
    if L == 0:
        b = y0 - 2 * x0 if False else None
        k = pick(r, ["y=", "x="])
        if k == "y=":
            m = F(nz(r, -4, 4))
            e1 = yeq(m, y0 - m * x0)
        else:
            c = F(nz(r, -4, 4))
            e1 = f"x = {lin((c, 'y'), (x0 - c * y0, ''))}"
        a, bb, cc = std_from_point(r, x0, y0)
        e2 = std(a, bb, cc)
    else:
        m = F(nz(r, -5, 5))
        e1 = yeq(m, y0 - m * x0) if L == 1 else f"y = {mx_b(m, y0 - m * x0)}"
        a, bb, cc = std_from_point(r, x0, y0)
        e2 = std(a, bb, cc) if L == 1 else f"{lin((a, 'x'), (bb, 'y'))} = {N(cc)}"
    from mathtext import solve_system
    need(solve_system(e1, e2)[0] == "one")
    return P(f"Solve by substitution: {sys_txt(e1, e2)}", pt(x0, y0),
             ["Substitute the expression for one variable into the other equation.", "Solve the one-variable equation, then substitute back.", f"Solution: {pt(x0, y0)}."],
             [pt(y0, x0) if x0 != y0 else pt(x0, -y0), pt(x0, y0 + 1), pt(-x0, y0) if x0 else pt(1, y0)], {"kind": "sys", "eqs": [e1, e2]}, tags=["multistep"])


@fam("012")
def s3_first_step(r, L):
    x0, y0 = rand_sol(r, 0)
    m = F(nz(r, -4, 4))
    b = y0 - m * x0
    a, bb, cc = std_from_point(r, x0, y0)
    need(a + bb * m != 0)
    e1, e2 = yeq(m, b), std(a, bb, cc)
    sg = "+" if bb > 0 else "-"
    co = abs(bb) if abs(bb) != 1 else ""
    ans = f"{coef_text(a, 'x')} {sg} {co}({mx_b(m, b)}) = {cc}"
    wrong = [f"{coef_text(a, 'x')} {sg} {co}({mx_b(m, b)}) = {mx_b(m, b)}", f"{coef_text(a, 'x')} {sg} {abs(bb)} · {mx_b(m, b)} = {cc}", f"{coef_text(a, 'y')} {sg} {co}({mx_b(m, b)}) = {cc}".replace("y", "x", 0)]
    wrong[2] = f"{coef_text(a, 'x')} {sg} {co}({mx_b(m, b)}) = {cc + 1}"
    return P(f"For the system {sys_txt(e1, e2)}, substitute the first equation into the second. What one-variable equation results?", ans,
             [f"Replace y in {e2} with ({mx_b(m, b)})."], wrong, chk_py("same_solution", eq=f"{coef_text(a, 'x')} + {bb}({mx_b(m, b)}) = {cc}"), tags=["misconception"])


@fam("12")
def s3_special(r, L):
    m, b = F(nz(r, -4, 4)), F(r.randint(-6, 6))
    k = pick(r, [2, 3, -2])
    kind = pick(r, ["none", "all"])
    c = b * k if kind == "all" else b * k + nz(r, -5, 5)
    e1, e2 = yeq(m, b), f"{lin((-m * k, 'x'), (k, 'y'))} = {N(c)}"
    want = "no solution" if kind == "none" else "infinitely many solutions"
    return P(f"Solve by substitution: {sys_txt(e1, e2)}", want, ["Substitute y and simplify.", f"The x-terms cancel, leaving {N(b * k)} = {N(c)}, which is {'false: no solution' if kind == 'none' else 'always true: infinitely many solutions'}."],
             ["no solution" if kind == "all" else "infinitely many solutions", pt(0, b), pt(1, m + b)], {"kind": "sys", "eqs": [e1, e2]}, tags=["reasoning"])


@fam("012")
def s3_context(r, L):
    a, s = r.randint(5, 30), r.randint(5, 30)
    pa, ps = r.randint(8, 15), r.randint(3, 7)
    q = pick(r, ["adult", "student"])
    tot = a + s
    money_ = pa * a + ps * s
    if L == 0:
        diff = a - s
        need(diff > 0)
        return P(f"There are {diff} more adults than students on a trip (a = s + {diff}), and {tot} people in all (a + s = {tot}). How many {'adults' if q == 'adult' else 'students'} are there?",
                 str(a if q == "adult" else s), [f"Substitute: (s + {diff}) + s = {tot}.", f"2s = {tot - diff}, s = {s}; a = {a}."],
                 [str(s if q == "adult" else a), str(tot // 2), str(diff)], chk_py("sys_var", eqs=[f"x = y + {diff}", f"x + y = {tot}"], var="x" if q == "adult" else "y"), tags=["modeling"])
    return P(f"A play sold {tot} tickets for ${money_}. Adult tickets cost ${pa} and student tickets cost ${ps}. How many {q} tickets were sold?", str(a if q == "adult" else s),
             [f"a + s = {tot}, so s = {tot} - a.", f"{pa}a + {ps}({tot} - a) = {money_}.", f"a = {a}, s = {s}."], [str(s if q == "adult" else a), str(money_ // (pa + ps)), str(tot - 1 - (a if q == "adult" else s))],
             chk_py("sys_var", eqs=[f"x + y = {tot}", f"{pa}x + {ps}y = {money_}"], var="x" if q == "adult" else "y"), tags=["modeling"])


@fam("012")
def s3_error(r, L):
    x0, y0 = rand_sol(r, 0)
    m = F(nz(r, 2, 4))
    b = y0 - m * x0
    a, bb = r.randint(2, 5), r.randint(2, 4)
    cc = a * x0 + bb * y0
    e1, e2 = yeq(m, b), std(a, bb, cc)
    wrong_eq = f"{a}x + {bb}({mx_b(m, b)}) = {cc}"
    wrongx = F(cc - b, a + bb * m)
    need(wrongx != x0)
    steps = [f"{a}x + {N(bb * m)}x + {N(b)} = {cc}", f"{N(a + bb * m)}x = {N(cc - b)}", f"x = {N(wrongx)}"]
    opts = [("Step 1", True), ("Step 2", False), ("Step 3", False), ("There is no error", False)]
    return P(f"Solving {sys_txt(e1, e2)}, a student substituted to get {wrong_eq}, then wrote Step 1: {steps[0]}. Step 2: {steps[1]}. Step 3: {steps[2]}. In which step is the first error?", "Step 1",
             [f"Step 1 should distribute {bb} to both terms: {bb}({mx_b(m, b)}) = {mx_b(bb * m, bb * b)}.", f"Correct: x = {N(x0)}, y = {N(y0)}."],
             options=opts, chk=chk_py("err_steps", orig=f"{a}x + {bb}({mx_b(m, b)}) = {cc}", steps=steps), tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s3_select(r, L):
    x0, y0 = rand_sol(r, 0)
    m = F(nz(r, -4, 4))
    b = y0 - m * x0
    a, bb, cc = std_from_point(r, x0, y0)
    need(F(-a, bb) != m)
    e1, e2 = yeq(m, b), std(a, bb, cc)
    opts = [(f"x = {N(x0)}", True), (f"y = {N(y0)}", True), (f"The point {pt(x0, y0)} satisfies both equations.", True),
            (f"x = {N(y0)}" if x0 != y0 else f"x = {N(x0 + 1)}", False), (f"y = {N(b)}" if b != y0 else f"y = {N(y0 + 2)}", False), ("The system has no solution.", False)]
    return P(f"Solve {sys_txt(e1, e2)} by substitution. Select ALL true statements.", None, [f"Solution {pt(x0, y0)}."], options=opts,
             chk=chk_py("sys_statement", eqs=[e1, e2]), tags=["reasoning"])


@fam("012")
def s3_open(r, L):
    x0, y0 = rand_sol(r, 0)
    m = F(nz(r, -3, 3))
    b = y0 - m * x0
    a, bb, cc = std_from_point(r, x0, y0)
    need(a + bb * m != 0)
    e1, e2 = yeq(m, b), std(a, bb, cc)
    return P(f"Solve {sys_txt(e1, e2)} by substitution.", None, ["Substitute.", "Solve for x.", "Back-substitute.", "Check."],
             parts=[("Substitute and write an equation in x only.", f"{coef_text(a, 'x')} + {bb}({mx_b(m, b)}) = {cc}".replace("+ -", "- "), chk_py("same_solution", eq=f"{coef_text(a, 'x')} + {bb}({mx_b(m, b)}) = {cc}")),
                    ("Solve for x.", f"x = {N(x0)}", chk_py("sys_var", eqs=[e1, e2], var="x")), ("Find y.", f"y = {N(y0)}", chk_py("sys_var", eqs=[e1, e2], var="y")),
                    ("Write the solution as an ordered pair.", pt(x0, y0), {"kind": "sys", "eqs": [e1, e2]})], tags=["multistep"])


# ======================================================================= S4 Elimination
@fam("012")
def s4_solve(r, L):
    x0, y0 = rand_sol(r, 0 if L < 2 else 1)
    for _ in range(40):
        a1, b1 = nz(r, -6, 6), nz(r, -6, 6)
        if L == 0:
            a2, b2 = nz(r, -6, 6), -b1 if r.random() < 0.5 else b1
        elif L == 1:
            k = pick(r, [2, 3, -2])
            a2, b2 = nz(r, -6, 6), b1 * k
        else:
            a2, b2 = nz(r, -7, 7), nz(r, -7, 7)
        if a1 * b2 != a2 * b1 and math.gcd(a2, b2) in (1, 2):
            break
    else:
        raise Reject()
    e1, e2 = std(a1, b1, a1 * x0 + b1 * y0), std(a2, b2, a2 * x0 + b2 * y0)
    hint = {0: "Add or subtract the equations so one variable cancels.", 1: "Multiply one equation so a variable has opposite (or equal) coefficients, then add or subtract.",
            2: "Multiply both equations to make one pair of coefficients opposites, then add."}[L]
    return P(f"Solve by elimination: {sys_txt(e1, e2)}", pt(x0, y0), [hint, "Solve for the remaining variable, then substitute back.", f"Solution: {pt(x0, y0)}."],
             [pt(y0, x0) if x0 != y0 else pt(x0, y0 + 2), pt(-x0, y0) if x0 else pt(2, y0), pt(x0, -y0) if y0 else pt(x0, 1)], {"kind": "sys", "eqs": [e1, e2]}, tags=["multistep"])


@fam("012", mode="mc")
def s4_which_multiply(r, L):
    a1, b1 = r.randint(1, 5), r.randint(1, 5)
    k = pick(r, [2, 3, 4])
    a2, b2 = r.randint(1, 6), b1 * k
    need(a1 * b2 != a2 * b1 and a2 != a1 * k)
    c1, c2 = r.randint(-10, 20), r.randint(-10, 20)
    e1, e2 = std(a1, b1, c1), std(a2, b2, c2)
    good = f"Multiply the first equation by {-k}, then add."
    opts = [(good, True), (f"Multiply the first equation by {k}, then add.", False), (f"Multiply the second equation by {k}, then add.", False), ("Add the equations as they are.", False)]
    r.shuffle(opts)
    return P(f"Which step eliminates y in {sys_txt(e1, e2)}?", good, [f"The y-coefficients are {b1} and {b2}. Multiplying the first by {-k} gives {-b1 * k}y, the opposite of {b2}y."],
             options=opts, chk=chk_py("elim_step", e1=[a1, b1], e2=[a2, b2]), tags=["reasoning"], mode="mc")


@fam("12")
def s4_special(r, L):
    a, b = nz(r, -5, 5), nz(r, -5, 5)
    c = r.randint(-10, 10)
    k = pick(r, [2, 3, -1, -2])
    kind = pick(r, ["none", "all"])
    e1, e2 = std(a, b, c), std(a * k, b * k, c * k + (0 if kind == "all" else nz(r, -4, 4)))
    want = "no solution" if kind == "none" else "infinitely many solutions"
    return P(f"Solve by elimination: {sys_txt(e1, e2)}", want, [f"Multiply the first equation by {k} and subtract: both variables cancel.", f"The result is {'a false' if kind == 'none' else 'a true'} statement, so {want}."],
             ["no solution" if kind == "all" else "infinitely many solutions", pt(0, 0), pt(c, 0) if a == 1 else pt(1, 1)], {"kind": "sys", "eqs": [e1, e2]}, tags=["reasoning"])


@fam("012")
def s4_context(r, L):
    x0, y0 = r.randint(2, 12), r.randint(2, 12)
    pa, pb = r.randint(2, 9), r.randint(2, 9)
    need(pa != pb)
    qa, qb = r.randint(2, 6), r.randint(2, 6)
    need(pa * qb != pb * qa)
    item = pick(r, [("pens", "notebooks"), ("tacos", "drinks"), ("apples", "pears")])
    q = pick(r, [0, 1])
    t1, t2 = pa * x0 + pb * y0, qa * x0 + qb * y0
    return P(f"{pa} {item[0]} and {pb} {item[1]} cost ${t1}. {qa} {item[0]} and {qb} {item[1]} cost ${t2}. What is the price of one {item[q][:-1]}?",
             f"${x0 if q == 0 else y0}", [f"{pa}x + {pb}y = {t1} and {qa}x + {qb}y = {t2}.", "Eliminate one variable and solve.", f"x = {x0}, y = {y0}."],
             [f"${y0 if q == 0 else x0}", f"${(x0 if q == 0 else y0) + 1}", f"${(x0 if q == 0 else y0) + 2}", f"${N(F(t1, pa + pb))}"], chk_py("sys_var", eqs=[f"{pa}x + {pb}y = {t1}", f"{qa}x + {qb}y = {t2}"], var="xy"[q]),
             tags=["modeling"])


@fam("012")
def s4_error(r, L):
    x0, y0 = rand_sol(r, 0)
    a1, b1, a2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
    need(a1 != a2)
    c1, c2 = a1 * x0 + b1 * y0, a2 * x0 - b1 * y0
    orig1, orig2 = std(a1, b1, c1), std(a2, -b1, c2)
    # student subtracts instead of adds, but keeps working
    steps = [f"{a1 + a2}x = {c1 - c2}", f"x = {N(F(c1 - c2, a1 + a2))}"]
    need(F(c1 - c2, a1 + a2) != x0)
    return P(f"To solve {sys_txt(orig1, orig2)}, Nia wrote: \"Add the equations: {steps[0]}, so {steps[1]}.\" What is the correct value of x?", f"x = {N(x0)}",
             [f"Adding gives ({a1} + {a2})x + 0y = {c1} + {paren(c2)} = {c1 + c2}; Nia subtracted the constants instead.", f"{a1 + a2}x = {c1 + c2}, so x = {N(x0)}."],
             [steps[1], f"x = {N(y0)}" if y0 != x0 else f"x = {N(x0 + 1)}", f"x = {N(F(c1 + c2, a1 - a2))}"], chk_py("sys_var", eqs=[orig1, orig2], var="x"),
             tags=["error-analysis", "misconception"])


@fam("012")
def s4_select(r, L):
    a1, b1 = r.randint(1, 5), r.randint(1, 5)
    a2, b2 = r.randint(1, 5), -b1 * pick(r, [1, 2])
    need(a1 * b2 != a2 * b1)
    e1, e2 = std(a1, b1, 10), std(a2, b2, 4)
    k = -b2 // b1
    good = [f"Multiply the first equation by {k}, then add." if k != 1 else "Add the equations.", f"Multiply the first equation by {a2} and the second by {-a1}, then add.", f"Multiply the first equation by {-b2} and the second by {b1}, then add."]
    bad = ["Subtract the equations without multiplying." if b1 != b2 and a1 != a2 else "Multiply the first equation by 5, then add.", f"Multiply the first equation by {a1}, then add.", f"Multiply the first equation by {b1 + 6}, then add."]
    need(a1 * a1 + a2 != 0 and b1 * a1 + b2 != 0 and (b1 + 6) * a1 + a2 != 0 and (b1 + 6) * b1 + b2 != 0)
    opts = [(g, True) for g in good] + [(b_, False) for b_ in bad]
    need(len({o[0] for o in opts}) == 6)
    return P(f"Select ALL steps that would eliminate a variable in {sys_txt(e1, e2)}.", None, ["A step works if it makes the coefficients of x or of y opposites before adding (or equal before subtracting)."],
             options=opts, chk=chk_py("elim_step", e1=[a1, b1], e2=[a2, b2]), tags=["reasoning"])


@fam("012")
def s4_open(r, L):
    x0, y0 = rand_sol(r, 0)
    a1, b1, a2 = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
    e1, e2 = std(a1, b1, a1 * x0 + b1 * y0), std(a2, -b1, a2 * x0 - b1 * y0)
    need(a1 + a2 != 0)
    return P(f"Solve {sys_txt(e1, e2)} by elimination.", None, ["The y-terms are opposites.", "Divide.", "Substitute.", "Ordered pair."],
             parts=[("Add the equations. Write the result.", f"{a1 + a2}x = {a1 * x0 + a2 * x0}", chk_py("same_solution", eq=f"{a1 + a2}x = {(a1 + a2) * x0}")),
                    ("Solve for x.", f"x = {N(x0)}", chk_py("sys_var", eqs=[e1, e2], var="x")), ("Find y.", f"y = {N(y0)}", chk_py("sys_var", eqs=[e1, e2], var="y")),
                    ("Write the solution.", pt(x0, y0), {"kind": "sys", "eqs": [e1, e2]})], tags=["multistep"])


# ======================================================================= S5 Inspection
def typed_pair(r, kind, form):
    m, b = F(nz(r, -4, 4)), F(r.randint(-6, 6))
    if form == "si":
        e1 = yeq(m, b)
        if kind == "one":
            e2 = yeq(m + pick(r, [1, -1, 2]), F(r.randint(-6, 6)))
        elif kind == "none":
            e2 = yeq(m, b + nz(r, -5, 5))
        else:
            e2 = f"y = {lin((b, ''), (m, 'x'))}" if b else yeq(m, b) + " "
        return e1, e2.strip()
    a, bb = nz(r, -5, 5), nz(r, -5, 5)
    c = r.randint(-10, 10)
    k = pick(r, [2, 3, -2])
    e1 = std(a, bb, c)
    if kind == "one":
        e2 = std(a * k, bb * k + pick(r, [1, -1]), c * k)
    elif kind == "none":
        e2 = std(a * k, bb * k, c * k + nz(r, -4, 4))
    else:
        e2 = std(a * k, bb * k, c * k)
    return e1, e2


@fam("012", mode="mc")
def s5_classify(r, L):
    kind = pick(r, ["one", "none", "all"])
    form = "si" if L == 0 else pick(r, ["si", "std"]) if L == 1 else "std"
    e1, e2 = typed_pair(r, kind, form)
    need(e1 != e2 or kind == "all")
    want = {"one": "one solution", "none": "no solution", "all": "infinitely many solutions"}[kind]
    return P(f"Without solving, how many solutions does the system {sys_txt(e1, e2)} have?", want,
             ["Compare slopes and y-intercepts (or whether one equation is a multiple of the other).",
              {"one": "Different slopes → one solution.", "none": "Same slope, different intercepts → parallel → no solution.", "all": "Same slope and intercept → same line → infinitely many."}[kind]],
             options=[(t, t == want) for t in ["one solution", "no solution", "infinitely many solutions"]] + [("two solutions", False)], chk=chk_py("sys_count", eqs=[e1, e2]),
             tags=["reasoning"], mode="mc")


@fam("012", mode="sa")
def s5_classify_sa(r, L):
    kind = pick(r, ["one", "none", "all"])
    e1, e2 = typed_pair(r, kind, "si" if L < 2 else "std")
    want = {"one": "one solution", "none": "no solution", "all": "infinitely many solutions"}[kind]
    return P(f"By inspection, does {sys_txt(e1, e2)} have one solution, no solution, or infinitely many solutions?", want,
             ["Look at the slope and intercept of each line.", want + "."], [], chk_py("sys_count", eqs=[e1, e2]), tags=["reasoning"], mode="sa")


@fam("12")
def s5_param(r, L):
    m, b = F(nz(r, -4, 4)), F(r.randint(-6, 6))
    want = pick(r, ["none", "all"])
    if want == "none":
        eq2 = f"y = kx + {N(b + 3)}" if b + 3 >= 0 else f"y = kx - {N(-(b + 3))}"
        return P(f"For what value of k does the system y = {mx_b(m, b)} and {eq2} have no solution?", f"k = {N(m)}", ["Parallel lines: same slope, different intercepts.", f"k = {N(m)}."],
                 [f"k = {N(-m)}", f"k = {N(b)}", f"k = {N(1 / m)}"], chk_py("sys_param", e1=yeq(m, b), e2=eq2, want="none"), tags=["reasoning"])
    eq2 = f"y = {mx_b(m, F(0))} + k" if m else "y = k"
    return P(f"For what value of k does the system y = {mx_b(m, b)} and {eq2} have infinitely many solutions?", f"k = {N(b)}", ["Same line: same slope and same intercept.", f"k = {N(b)}."],
             [f"k = {N(m)}", f"k = {N(-b)}" if b else "k = 1", f"k = {N(b + 1)}"], chk_py("sys_param", e1=yeq(m, b), e2=eq2, want="all"), tags=["reasoning"])


@fam("2", mode="mc")
def s5_write_second(r, L):
    m, b = F(nz(r, -4, 4)), F(r.randint(-5, 5))
    want = pick(r, ["none", "all", "one"])
    cands = {"none": yeq(m, b + 3), "all": f"{lin((-2 * m, 'x'), (2, 'y'))} = {N(2 * b)}", "one": yeq(-m, b)}
    extra = yeq(m, b + 3) if want != "none" else f"{lin((-2 * m, 'x'), (2, 'y'))} = {N(2 * b)}"
    opts = [(cands[k], k == want) for k in cands]
    opts.append((yeq(2 * m, b + 1) if want != "one" else yeq(m, b - 2), False))
    r.shuffle(opts)
    word = {"none": "no solution", "all": "infinitely many solutions", "one": "exactly one solution"}[want]
    good = [t for t, c in opts if c][0]
    return P(f"Which equation, paired with y = {mx_b(m, b)}, makes a system with {word}?", good,
             [{"none": "Same slope, different intercept.", "all": "An equivalent equation (a multiple of the same line).", "one": "A different slope."}[want]],
             options=opts, chk=chk_py("sys_pair_type", e1=yeq(m, b), want=want), tags=["reasoning", "challenge"], mode="mc")


@fam("012")
def s5_error(r, L):
    m, b = F(nz(r, 2, 4)), F(r.randint(1, 6))
    k = 2
    e1, e2 = yeq(m, b), f"{lin((-m * k, 'x'), (k, 'y'))} = {N(b * k)}"
    opts = [("No. The second equation simplifies to the same line, so there are infinitely many solutions.", True), ("Yes. Different coefficients mean the lines cross once.", False),
            ("Yes. The lines are parallel.", False), ("No. There is no solution.", False)]
    r.shuffle(opts)
    return P(f"Mo says {sys_txt(e1, e2)} has exactly one solution because the equations \"look different.\" Is Mo correct?", opts[[c for _, c in opts].index(True)][0],
             [f"Divide the second equation by {k}: y = {mx_b(m, b)}.", "Same line → infinitely many solutions."], options=opts,
             chk={"kind": "text", "accept": ["No. The second equation simplifies to the same line, so there are infinitely many solutions."]}, tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s5_select(r, L):
    items = [(typed_pair(r, "none", "si"), True), (typed_pair(r, "none", "std"), True), (typed_pair(r, "one", "si"), False), (typed_pair(r, "all", "std"), False),
             (typed_pair(r, "none", "si"), True), (typed_pair(r, "one", "std"), False)]
    opts = [(sys_txt(*p), c) for p, c in items]
    need(len({o[0] for o in opts}) == 6)
    return P("Select ALL systems that have NO solution.", None, ["No solution: parallel lines (same slope, different intercepts)."], options=opts,
             chk=chk_py("sys_text_type", want="none"), tags=["reasoning"])


@fam("012")
def s5_open(r, L):
    m, b = F(nz(r, -4, 4)), F(r.randint(-5, 5))
    e = yeq(m, b)
    return P(f"Start with the equation {e}.", None, ["Same slope, different intercept.", "Same line.", "Different slope.", "Inspect slopes."],
             parts=[("Write a second equation so the system has no solution.", yeq(m, b + 2), chk_py("sys_pair_type", e1=e, want="none")),
                    ("Write a second equation so the system has infinitely many solutions.", f"{lin((-2 * m, 'x'), (2, 'y'))} = {N(2 * b)}", chk_py("sys_pair_type", e1=e, want="all")),
                    ("Write a second equation so the system has exactly one solution.", yeq(m + 1, b), chk_py("sys_pair_type", e1=e, want="one")),
                    (f"How many solutions does {e} and {yeq(m, b - 1)} have?", "no solution", chk_py("sys_count", eqs=[e, yeq(m, b - 1)]))], tags=["reasoning"])


# ======================================================================= S6 Applications
@fam("012")
def s6_tickets(r, L):
    x0, y0 = r.randint(10, 80), r.randint(10, 80)
    p1, p2 = r.randint(5, 15), r.randint(2, 8)
    need(p1 != p2)
    item = pick(r, [("adult", "child", "tickets"), ("large", "small", "pizzas"), ("hardcover", "paperback", "books")])
    q = pick(r, [0, 1])
    return P(f"A sale had {x0 + y0} {item[2]} for a total of ${p1 * x0 + p2 * y0}. {item[0].capitalize()} {item[2]} cost ${p1} and {item[1]} {item[2]} cost ${p2}. How many {item[q]} {item[2]} were sold?",
             str([x0, y0][q]), [f"x + y = {x0 + y0}; {p1}x + {p2}y = {p1 * x0 + p2 * y0}.", f"Solve: x = {x0}, y = {y0}."], [str([y0, x0][q]), str((x0 + y0) // 2), str([x0, y0][q] + 1)],
             chk_py("sys_var", eqs=[f"x + y = {x0 + y0}", f"{p1}x + {p2}y = {p1 * x0 + p2 * y0}"], var="xy"[q]), tags=["modeling"])


@fam("012")
def s6_plans(r, L):
    f1, r1 = r.randint(20, 80), r.randint(2, 10)
    r2 = r1 + r.randint(2, 8)
    t = r.randint(3, 20)
    f2 = f1 + (r1 - r2) * t
    need(f2 >= 0)
    q = pick(r, ["when", "cheaper"]) if L else "when"
    if q == "when":
        return P(f"Gym A charges ${f1} plus ${r1} per visit. Gym B charges ${f2} plus ${r2} per visit. For how many visits do the gyms cost the same?", f"{t} visits",
                 [f"{f1} + {r1}v = {f2} + {r2}v.", f"{r2 - r1}v = {f1 - f2}, v = {t}."], [f"{t + 1} visits", f"{f1 - f2} visits", f"{N(F(f1 + f2, r1 + r2))} visits"],
                 chk_py("sys_var", eqs=[f"y = {r1}x + {f1}", f"y = {r2}x + {f2}"], var="x"), tags=["modeling"])
    v = t + r.randint(2, 6)
    return P(f"Gym A charges ${f1} plus ${r1} per visit. Gym B charges ${f2} plus ${r2} per visit. Which gym is cheaper for {v} visits?", "Gym A",
             [f"They cost the same at {t} visits.", f"A: {f1 + r1 * v}; B: {f2 + r2 * v}. Gym A is cheaper."], ["Gym B", "They cost the same", "Cannot be determined"],
             chk_py("cheaper_plan", A=[f1, r1], B=[f2, r2], v=v), tags=["modeling", "reasoning"])


@fam("12")
def s6_mixture(r, L):
    x0, y0 = r.randint(2, 20), r.randint(2, 20)
    c1, c2 = pick(r, [(F(3, 2), F(4)), (F(2), F(5)), (F(5, 2), F(6))])
    tot = c1 * x0 + c2 * y0
    need(is_term(tot))
    return P(f"A trail mix uses peanuts at ${D(c1)} per pound and cashews at ${D(c2)} per pound. A {x0 + y0}-pound batch costs ${D(tot)}. How many pounds of cashews are in it?",
             f"{y0} pounds", [f"p + c = {x0 + y0}; {D(c1)}p + {D(c2)}c = {D(tot)}.", f"c = {y0}."], [f"{x0} pounds", f"{(x0 + y0) // 2} pounds", f"{y0 + 1} pounds"],
             chk_py("sys_var", eqs=[f"x + y = {x0 + y0}", f"{D(c1)}x + {D(c2)}y = {D(tot)}"], var="y"), tags=["modeling"])


@fam("012")
def s6_numbers(r, L):
    a, b = r.randint(5, 60), r.randint(1, 40)
    need(a > b)
    if L == 0:
        return P(f"The sum of two numbers is {a + b} and their difference is {a - b}. What is the larger number?", str(a), [f"x + y = {a + b}, x - y = {a - b}.", f"Add: 2x = {2 * a}, x = {a}."],
                 [str(b), str(a + b), str((a + b) // 2)], chk_py("sys_var", eqs=[f"x + y = {a + b}", f"x - y = {a - b}"], var="x"), tags=["modeling"])
    k = r.randint(2, 4)
    need(a != k * b)
    return P(f"Ana is {a - b} years older than Ben. The sum of their ages is {a + b}. How old is Ben?", str(b),
             [f"a = b + {a - b}; a + b = {a + b}.", f"2b + {a - b} = {a + b}, b = {b}."], [str(a), str(a - b), str((a + b) // 2)],
             chk_py("sys_var", eqs=[f"x = y + {a - b}", f"x + y = {a + b}"], var="y"), tags=["modeling"])


@fam("2")
def s6_speed(r, L):
    p, w = r.randint(8, 20), r.randint(1, 5)
    need(p > w)
    t = r.randint(2, 4)
    return P(f"A boat travels {(p + w) * t} km downstream in {t} hours and {(p - w) * t} km upstream in {t} hours. What is the speed of the current?", f"{w} km per hour",
             [f"(b + c){t} = {(p + w) * t} and (b - c){t} = {(p - w) * t}.", f"b + c = {p + w}, b - c = {p - w}; c = {w}."], [f"{p} km per hour", f"{p + w} km per hour", f"{2 * w} km per hour"],
             chk_py("sys_var", eqs=[f"x + y = {p + w}", f"x - y = {p - w}"], var="y"), tags=["modeling", "challenge"])


@fam("012")
def s6_error(r, L):
    x0, y0 = r.randint(5, 30), r.randint(5, 30)
    p1, p2 = r.randint(3, 9), r.randint(1, 4)
    need(p1 != p2)
    opts = [(f"x + y = {x0 + y0} and {p1}x + {p2}y = {p1 * x0 + p2 * y0}", True), (f"x + y = {p1 * x0 + p2 * y0} and {p1}x + {p2}y = {x0 + y0}", False),
            (f"{p1}x + {p2}y = {x0 + y0} and x + y = {p1 + p2}", False), (f"x + y = {x0 + y0} and {p2}x + {p1}y = {p1 * x0 + p2 * y0}", False)]
    r.shuffle(opts)
    return P(f"A farm stand sold {x0 + y0} baskets: x baskets of berries at ${p1} each and y baskets of plums at ${p2} each, earning ${p1 * x0 + p2 * y0}. Ivy wrote x + y = {p1 * x0 + p2 * y0} and {p1}x + {p2}y = {x0 + y0}. Which system is correct?",
             f"x + y = {x0 + y0} and {p1}x + {p2}y = {p1 * x0 + p2 * y0}", ["Ivy switched the totals: the count equation uses the number of baskets, the money equation uses dollars.",
                                                                         f"Solution: x = {x0}, y = {y0}."], options=opts, chk=chk_py("sys_model", sol=[x0, y0], money=[p1, p2]),
             tags=["error-analysis", "modeling"], mode="mc")


@fam("012")
def s6_select(r, L):
    x0, y0 = r.randint(3, 15), r.randint(3, 15)
    p1, p2 = r.randint(4, 9), r.randint(1, 3)
    opts = [(f"x + y = {x0 + y0}", True), (f"{p1}x + {p2}y = {p1 * x0 + p2 * y0}", True), (f"y = {x0 + y0} - x", True),
            (f"x + y = {p1 * x0 + p2 * y0}", False), (f"{p2}x + {p1}y = {p1 * x0 + p2 * y0}", p2 * x0 + p1 * y0 == p1 * x0 + p2 * y0), (f"{p1 + p2}(x + y) = {p1 * x0 + p2 * y0}", False)]
    need(not opts[4][1])
    return P(f"A class bought {x0 + y0} items: x posters at ${p1} each and y stickers at ${p2} each, spending ${p1 * x0 + p2 * y0}. Select ALL equations that correctly model the situation.", None,
             ["Count equation and cost equation (and their rearrangements)."], options=opts, chk=chk_py("eq_has_point", p=[x0, y0]), tags=["modeling"])


@fam("012")
def s6_open(r, L):
    x0, y0 = r.randint(4, 20), r.randint(4, 20)
    p1, p2 = r.randint(5, 12), r.randint(2, 6)
    need(p1 != p2)
    return P(f"A food truck sold {x0 + y0} meals: burritos at ${p1} and quesadillas at ${p2}, for ${p1 * x0 + p2 * y0}. Let b be burritos and q be quesadillas.", None,
             ["Count.", "Money.", "Solve.", "Solve."],
             parts=[("Write the count equation.", f"b + q = {x0 + y0}", chk_py("eq_has_point_bq", p=[x0, y0], total=x0 + y0)),
                    ("Write the money equation.", f"{p1}b + {p2}q = {p1 * x0 + p2 * y0}", chk_py("eq_has_point_bq", p=[x0, y0], total=p1 * x0 + p2 * y0)),
                    ("How many burritos were sold?", str(x0), chk_py("sys_var", eqs=[f"x + y = {x0 + y0}", f"{p1}x + {p2}y = {p1 * x0 + p2 * y0}"], var="x")),
                    ("How many quesadillas were sold?", str(y0), chk_py("sys_var", eqs=[f"x + y = {x0 + y0}", f"{p1}x + {p2}y = {p1 * x0 + p2 * y0}"], var="y"))], tags=["modeling"])


SKILLS = {
    1: dict(name="Graphing in slope-intercept form", std=["8.EE.B.6", "8.F.A.3"], fams=[s1_identify, s1_next_point, s1_match, s1_rewrite, s1_from_graph_two], extra=[s1_error, s1_select, s1_open]),
    2: dict(name="Solving systems by graphing", std=["8.EE.C.8a", "8.EE.C.8b"], fams=[s2_read, s2_special, s2_check, s2_context_graph, s2_estimate], extra=[s2_error, s2_select, s2_open]),
    3: dict(name="Solving systems by substitution", std=["8.EE.C.8b"], fams=[s3_solve, s3_first_step, s3_special, s3_context], extra=[s3_error, s3_select, s3_open]),
    4: dict(name="Solving systems by elimination", std=["8.EE.C.8b"], fams=[s4_solve, s4_which_multiply, s4_special, s4_context], extra=[s4_error, s4_select, s4_open]),
    5: dict(name="Solving systems by inspection", std=["8.EE.C.8b"], fams=[s5_classify, s5_classify_sa, s5_param, s5_write_second], extra=[s5_error, s5_select, s5_open]),
    6: dict(name="Applications of systems of linear equations", std=["8.EE.C.8c"], fams=[s6_tickets, s6_plans, s6_mixture, s6_numbers, s6_speed], extra=[s6_error, s6_select, s6_open]),
}
