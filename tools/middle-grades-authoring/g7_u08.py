"""Grade 7 Unit 8 — Linear Functions and Graphing (linear-functions-graphing)."""
from glib import *

UNIT_ID = "linear-functions-graphing"
ABBR = "lfg"


def pts_text(ps):
    return "{" + ", ".join(f"({a}, {b})" for a, b in ps) + "}"


def eqline(m, b):
    return "y = " + lin((m, "x"), (b, ""))


# ============================================================== S1 Relations and Functions
@fam("012")
def s1_is_function(r, L):
    n = 4 if L == 0 else 5
    xs = r.sample(range(-6, 9), n)
    ys = [r.randint(-6, 9) for _ in xs]
    if r.random() < 0.5:
        i, j = r.sample(range(n), 2)
        xs[j] = xs[i]
        need(ys[j] != ys[i])
    ps = list(zip(xs, ys))
    need(len(set(ps)) == n)
    ok = len(set(xs)) == n
    return Q(f"Is the relation a function? {pts_text(ps)}", "Yes" if ok else "No", ["A relation is a function if each input (x) has exactly one output (y).",
                                                                                  "Look for repeated x-values with different y-values.", "It is a function." if ok else "An x-value repeats with different y-values, so it is not a function."],
             ["No" if ok else "Yes"], PY("is_func", pts=ps), mode="sa", why=["Looked for repeated y-values instead of x-values"])


@fam("012")
def s1_domain(r, L):
    xs = r.sample(range(-8, 10), 4)
    ys = [r.randint(-8, 9) for _ in xs]
    ps = list(zip(xs, ys))
    which = pick(r, ["domain", "range"])
    vals = sorted(set(xs if which == "domain" else ys))
    other = sorted(set(ys if which == "domain" else xs))
    need(vals != other)
    return Q(f"List the {which} of the relation {pts_text(ps)} in order from least to greatest.", ", ".join(map(str, vals)),
             [f"The {which} is the set of {'x' if which == 'domain' else 'y'}-values.", f"{', '.join(map(str, vals))}."], [", ".join(map(str, other)), ", ".join(map(str, vals[::-1])) if len(vals) > 1 else "0", ", ".join(map(str, sorted(set(xs + ys))))],
             PY("seq_eq", items=[str(v) for v in vals]), why=[f"Listed the {'range' if which == 'domain' else 'domain'} instead", "Listed from greatest to least", "Listed every number"])


@fam("12", mode="mc")
def s1_graph(r, L):
    xs = r.sample(range(-5, 6), 5)
    ys = [r.randint(-5, 5) for _ in xs]
    func = r.random() < 0.5
    if not func:
        xs[4] = xs[0]
        need(ys[4] != ys[0])
    ps = list(zip(xs, ys))
    need(len(set(ps)) == 5)
    ok = len(set(xs)) == 5
    alt = "Coordinate plane with points " + ", ".join(f"({a}, {b})" for a, b in ps) + "."
    opts = [("Yes, it passes the vertical line test.", ok), ("No, two points lie on the same vertical line.", not ok), ("Yes, because no two points share a y-value.", False), ("No, because the points are not on a line.", False)]
    return Q("Does the graph show a function?", [o for o, t in opts if t][0], ["Vertical line test: a vertical line cannot pass through two points of a function.", "It passes." if ok else "A vertical line hits two points."],
             options=opts, chk=PY("func_claim", pts=ps), mode="mc", tags=["graph"], diagram={"alt": alt, "draw": plane_draw((-6, 6), (-6, 6), points=[(a, b, "") for a, b in ps])})


@fam("12")
def s1_evaluate(r, L):
    m, b = nz(r, -6, 6), r.randint(-9, 9)
    x = nz(r, -8, 8)
    fx = f"f(x) = {lin((m, 'x'), (b, ''))}" if L == 1 else f"f(x) = {lin((m, 'x'), (b, ''))}" if r.random() < 0.5 else f"f(x) = x² {sgn(b)}"
    v = m * x + b if "²" not in fx else x * x + b
    ex = fx.split("= ")[1].replace("x", f"({x})")
    return Q(f"For {fx}, find f({x}).", str(v), [f"Substitute {x} for x: {ex}.", f"f({x}) = {v}."], [str(-v) if v else "1", str(m + x + b) if "²" not in fx else str(2 * x + b), str(v + 2)],
             V(ex), why=["Made a sign error", "Added instead of multiplying" if "²" not in fx else "Multiplied by 2 instead of squaring", ""])


# ============================================================== S2 Equations with Two Variables
@fam("012")
def s2_is_solution(r, L):
    m, b = nz(r, -5, 6), r.randint(-9, 9)
    x = r.randint(-6, 6)
    y = m * x + b + (0 if r.random() < 0.5 else pick(r, [1, -1, 2]))
    ok = y == m * x + b
    eq = eqline(m, b) if L < 2 else f"{lin((-m, 'x'), (1, 'y'))} = {b}"
    return Q(f"Is ({x}, {y}) a solution of {eq}?", "Yes" if ok else "No", [f"Substitute x = {x} and y = {y}.", f"Check whether both sides are equal.", "Yes" if ok else "No"],
             ["No" if ok else "Yes"], PY("is_sol2", eq=eq, x=str(x), y=str(y)), mode="sa", why=["Substituted the values into the wrong variables"])


@fam("012")
def s2_find_y(r, L):
    a, b, c = nz(r, -6, 6), nz(r, -6, 6), None
    x = r.randint(-6, 6)
    if L == 0:
        m, k = r.randint(2, 6), r.randint(-8, 8)
        eq = eqline(m, k)
        y = m * x + k
    else:
        y0 = r.randint(-6, 6)
        need(b != 0)
        c = a * x + b * y0
        eq = f"{lin((a, 'x'), (b, 'y'))} = {c}"
        y = F(c - a * x, b)
        need(y.denominator == 1 or L == 2)
    return Q(f"Find the value of y when x = {x} for the equation {eq}.", f"y = {N(y)}", [f"Substitute x = {x}.", "Solve for y.", f"y = {N(y)}."],
             [f"y = {N(-F(y))}" if y else "y = 1", f"y = {N(F(y) + 1)}", f"y = {x}"], EQ(eq.replace("x", f"({x})"), "y"), why=["Made a sign error", "", "Gave the x-value"])


@fam("12")
def s2_table(r, L):
    m, b = nz(r, -4, 5), r.randint(-6, 8)
    xs = [-1, 0, 1, 2, 3]
    i = r.randrange(5)
    v = m * xs[i] + b
    return Q(f"Complete the table for {eqline(m, b)}. What is y when x = {xs[i]}?", str(v), [f"y = {m}({xs[i]}) {sgn(b)}.", f"y = {v}."], [str(m + xs[i] + b), str(-v) if v else "1", str(m * xs[i] - b)],
             V(f"{m}*({xs[i]}) + ({b})"), why=["Added instead of multiplying", "Made a sign error", "Subtracted the constant instead of adding"], tags=["multiple-representations"])


# ============================================================== S3 Slope and y-intercept
@fam("012")
def s3_two_points(r, L):
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    dx = nz(r, -6, 6)
    m = F(nz(r, -5, 5), 1) if L == 0 else F(nz(r, -9, 9), r.randint(1, 4))
    dy = m * dx
    need(F(dy).denominator == 1)
    x2, y2 = x1 + dx, y1 + int(dy)
    return Q(f"Find the slope of the line through ({x1}, {y1}) and ({x2}, {y2}).", N(m), [f"Slope = (y₂ - y₁) ÷ (x₂ - x₁).", f"= ({y2} - {par(y1)}) ÷ ({x2} - {par(x1)}) = {int(dy)} ÷ {dx}.", f"Slope = {N(m)}."],
             [N(1 / m) if m not in (1, -1) else N(m * 2), N(-m), N(F(y2 + y1, x2 + x1)) if x2 + x1 and F(y2 + y1, x2 + x1) != m else N(m + 1)], V(f"({y2} - ({y1})) ÷ ({x2} - ({x1}))"),
             why=["Divided the change in x by the change in y", "Subtracted in different orders (sign error)", "Added coordinates instead of subtracting"])


@fam("012")
def s3_from_eq(r, L):
    m, b = (nz(r, -6, 6), r.randint(-9, 9)) if L < 2 else (F(nz(r, -5, 5), pick(r, [2, 3])), r.randint(-9, 9))
    what = pick(r, ["slope", "y-intercept"])
    if L == 2 and r.random() < 0.6:
        a, c = nz(r, -6, 6), r.randint(2, 5)
        need(a % c != 0)
        k = r.randint(-9, 9) * c
        eq = f"{lin((a, 'x'), (c, 'y'))} = {k}"
        m, b = F(-a, c), F(k, c)
    else:
        eq = eqline(m, b)
    v = m if what == "slope" else b
    return Q(f"What is the {what} of the line {eq}?", N(v), ["Write the equation in slope-intercept form y = mx + b." if L == 2 else "In y = mx + b, m is the slope and b is the y-intercept.",
                                                            f"m = {N(m)}, b = {N(b)}.", f"The {what} is {N(v)}."],
             [N(b if what == "slope" else m), N(-v) if v else "1", N(1 / v) if v not in (0, 1, -1) else N(v + 2)], V(N(v)), why=["Mixed up the slope and the y-intercept", "Made a sign error", "Gave the reciprocal"])


@fam("012")
def s3_graph(r, L):
    m = F(nz(r, -3, 3)) if L == 0 else F(nz(r, -4, 4), pick(r, [1, 2, 3]))
    b = r.randint(-4, 4)
    need(abs(m) <= 3)
    what = pick(r, ["slope", "y-intercept"]) if L else "slope"
    v = m if what == "slope" else b
    p1 = (0, b)
    p2 = (m.denominator, b + m.numerator)
    alt = f"Coordinate plane with a line through ({p1[0]}, {p1[1]}) and ({p2[0]}, {p2[1]})."
    return Q(f"What is the {what} of the line in the graph?", N(v), [f"The line passes through {pt(*p1)} and {pt(*p2)}.", f"Rise ÷ run = {m.numerator} ÷ {m.denominator} = {N(m)}." if what == "slope" else f"It crosses the y-axis at {b}.", f"The {what} is {N(v)}."],
             [N(-v) if v else "1", N(1 / v) if v not in (0, 1, -1) else N(v + 2), N(b if what == "slope" else m)], V(N(v)), why=["Made a sign error (read the direction wrong)", "Used run over rise", "Mixed up slope and intercept"],
             diagram={"alt": alt, "draw": plane_draw((-7, 7), (-7, 7), lines=[(m, b, None)], points=[(p1[0], p1[1], ""), (p2[0], p2[1], "")])}, tags=["graph"])


@fam("12", mode="mc")
def s3_type(r, L):
    kind = pick(r, ["positive", "negative", "zero", "undefined"])
    a, b = r.randint(-5, 5), r.randint(-5, 5)
    if kind == "zero":
        p, q = (a, b), (a + r.randint(1, 5), b)
    elif kind == "undefined":
        p, q = (a, b), (a, b + r.randint(1, 5))
    else:
        dx, dy = r.randint(1, 5), r.randint(1, 5) * (1 if kind == "positive" else -1)
        p, q = (a, b), (a + dx, b + dy)
    opts = [(k, k == kind) for k in ["positive", "negative", "zero", "undefined"]]
    return Q(f"What type of slope does the line through {pt(*p)} and {pt(*q)} have?", kind, ["Find rise and run.", "Horizontal lines have zero slope; vertical lines have undefined slope.", f"The slope is {kind}."],
             options=opts, chk=PY("slope_type", p=list(p), q=list(q)), mode="mc")


# ============================================================== S4 Writing Rules for Linear Functions
@fam("012")
def s4_table_rule(r, L):
    m, b = (r.randint(1, 6), r.randint(0, 10)) if L == 0 else (nz(r, -6, 6), r.randint(-10, 10))
    xs = [0, 1, 2, 3] if L == 0 else sorted(r.sample(range(-3, 7), 4))
    ys = [m * x + b for x in xs]
    rule = eqline(m, b)
    return Q(f"Write a rule for the linear function in the table. x: {', '.join(map(str, xs))}; y: {', '.join(map(str, ys))}", rule,
             [f"Slope: change in y ÷ change in x = {m}.", f"y-intercept: y when x = 0 is {b}." if 0 in xs else f"Substitute a point to find b: {ys[0]} = {m}({xs[0]}) + b, so b = {b}.", f"Rule: {rule}."],
             [eqline(b, m) if b else eqline(m, 1), eqline(m, ys[0]) if ys[0] != b else eqline(m, b + 1), eqline(ys[1] - ys[0], 0) if b else eqline(-m, b)], PY("linear_rule", pts=[[x, y] for x, y in zip(xs, ys)]),
             why=["Switched the slope and the intercept", "Used the first y-value as the intercept", "Left out the y-intercept"], tags=["multiple-representations"])


@fam("12")
def s4_two_points(r, L):
    m, b = nz(r, -5, 5), r.randint(-8, 8)
    x1, x2 = r.sample(range(-5, 6), 2)
    p, q = (x1, m * x1 + b), (x2, m * x2 + b)
    rule = eqline(m, b)
    return Q(f"Write an equation in slope-intercept form for the line through {pt(*p)} and {pt(*q)}.", rule,
             [f"m = ({q[1]} - {par(p[1])}) ÷ ({x2} - {par(x1)}) = {m}.", f"Substitute {pt(*p)}: {p[1]} = {m}({x1}) + b.", f"b = {b}.", f"{rule}."],
             [eqline(F(1, m) if abs(m) > 1 else m * 2, b), eqline(m, p[1]), eqline(-m, b)], PY("linear_rule", pts=[list(p), list(q)]), why=["Used run over rise for the slope", "Used a y-coordinate as the intercept", "Made a sign error in the slope"])


@fam("012")
def s4_words(r, L):
    rate, start = r.randint(2, 20), r.randint(5, 60)
    ctx = pick(r, [(f"A plumber charges ${start} plus ${rate} per hour. Write a rule for the cost y after x hours.", rate, start),
                   (f"A candle is {start + rate * 10} cm tall and burns {rate} cm per hour. Write a rule for its height y after x hours.", -rate, start + rate * 10),
                   (f"A pool has {start * 10} gallons and fills at {rate * 5} gallons per minute. Write a rule for the gallons y after x minutes.", rate * 5, start * 10)])
    t, m, b = ctx
    rule = eqline(m, b)
    return Q(t, rule, ["The rate of change is the slope m.", "The starting amount is the y-intercept b.", f"{rule}."], [eqline(b, m), eqline(-m, b), eqline(m, 0)],
             PY("linear_rule", pts=[[0, b], [1, m + b]]), why=["Switched the rate and the starting amount", "Used the wrong sign for the rate", "Left out the starting amount"], tags=["modeling"])


# ============================================================== S5 Scatter Plots
def scatter_data(r, kind, n=9):
    xs = sorted(r.sample(range(1, 13), n))
    if kind == "positive":
        ys = [x + r.randint(-2, 2) + 2 for x in xs]
    elif kind == "negative":
        ys = [14 - x + r.randint(-2, 2) for x in xs]
    else:
        ys = [r.randint(1, 13) for _ in xs]
    return xs, ys


def corr(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy) if sxx and syy else 0


@fam("012", mode="mc")
def s5_type(r, L):
    kind = pick(r, ["positive", "negative", "no"])
    xs, ys = scatter_data(r, kind)
    c = corr(xs, ys)
    need((kind == "positive" and c > 0.7) or (kind == "negative" and c < -0.7) or (kind == "no" and abs(c) < 0.25))
    labs = {"positive": "positive correlation", "negative": "negative correlation", "no": "no correlation"}
    opts = [(labs[k], k == kind) for k in labs] + [("cannot be determined", False)]
    alt = "Scatter plot with points " + ", ".join(f"({a}, {b})" for a, b in zip(xs, ys)) + "."
    return Q("What type of correlation does the scatter plot show?", labs[kind], ["Positive: y tends to increase as x increases.", "Negative: y tends to decrease as x increases.", f"This plot shows {labs[kind]}."],
             options=opts, chk=PY("corr_type", xs=xs, ys=ys), mode="mc", tags=["graph"],
             diagram={"alt": alt, "draw": plane_draw((0, 14), (0, 16), points=[(a, b, "", "#1f4e9c") for a, b in zip(xs, ys)], data=True, xstep=2, ystep=2, xlabel="x", ylabel="y")})


@fam("012", mode="mc")
def s5_context(r, L):
    pairs = [("hours studied", "test score", "positive"), ("outdoor temperature", "hot chocolate sales", "negative"), ("shoe size", "favorite number", "no"),
             ("age of a car", "its resale value", "negative"), ("height of a person", "arm span", "positive"), ("number of absences", "class grade", "negative"),
             ("minutes exercising", "calories burned", "positive"), ("day of the month", "a student's height", "no")]
    a, b, k = pick(r, pairs)
    labs = {"positive": "positive correlation", "negative": "negative correlation", "no": "no correlation"}
    opts = [(labs[x], x == k) for x in labs]
    return Q(f"What type of correlation would you expect between {a} and {b}?", labs[k], ["Think about whether one tends to increase or decrease as the other increases.", f"Expected: {labs[k]}."], options=opts + [("perfect correlation", False)],
             chk=TXT(labs[k]), mode="mc", tags=["reasoning", "modeling"])


@fam("012")
def s5_predict(r, L):
    m, b = F(r.randint(2, 9), 2), r.randint(5, 30)
    x = r.randint(8, 20)
    v = m * x + b
    return Q(f"A trend line for a scatter plot of hours practiced (x) and points scored (y) is y = {N(m) if m.denominator == 1 else D(m)}x + {b}. Predict the points for {x} hours of practice.", D(v),
             [f"Substitute x = {x}.", f"y = {D(m)}({x}) + {b} = {D(v)}."], [D(m * (x + b)), D(m + x + b), D(v - b)], V(f"{D(m)}*{x} + {b}"), why=["Added before multiplying", "Added all the numbers", "Forgot the y-intercept"], tags=["modeling"])


# ============================================================== S6 / S7 Systems
@fam("012")
def s6_graph(r, L):
    x0, y0 = nz(r, -4, 4), r.randint(-4, 4)
    m1, m2 = r.sample([-3, -2, -1, 1, 2, 3], 2) if L < 2 else r.sample([F(-1, 2), F(1, 2), -2, 2, 1, -1, F(3, 2)], 2)
    b1, b2 = y0 - m1 * x0, y0 - m2 * x0
    need(F(b1).denominator == 1 and F(b2).denominator == 1 and abs(b1) <= 8 and abs(b2) <= 8)
    e1, e2 = eqline(m1, b1), eqline(m2, b2)
    alt = f"Coordinate plane with the lines {e1} and {e2}, which intersect at ({x0}, {y0})."
    return Q(f"The graph shows {e1} and {e2}. What is the solution of the system?", f"({x0}, {y0})", ["The solution is the point where the lines intersect.", f"They intersect at ({x0}, {y0}).",
                                                                                                       f"Check: {y0} = {N(m1)}({x0}) + {N(b1)} and {y0} = {N(m2)}({x0}) + {N(b2)}."],
             [f"({y0}, {x0})", f"(0, {N(b1)})", f"(0, {N(b2)})"], {"kind": "sys", "eqs": [e1, e2]}, why=["Switched the coordinates", "Gave a y-intercept", "Gave a y-intercept"],
             diagram={"alt": alt, "draw": plane_draw((-8, 8), (-8, 8), lines=[(m1, b1, None, e1), (m2, b2, None, e2)], points=[(x0, y0, "")])}, tags=["graph"])


@fam("012")
def s6_check(r, L):
    x0, y0 = r.randint(-5, 5), r.randint(-5, 5)
    m1, m2 = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    b1, b2 = y0 - m1 * x0, y0 - m2 * x0
    tx, ty = (x0, y0) if r.random() < 0.5 else (x0, y0 + pick(r, [1, -1]))
    ok = (tx, ty) == (x0, y0)
    e1, e2 = eqline(m1, b1), eqline(m2, b2)
    return Q(f"Is ({tx}, {ty}) a solution of the system {e1} and {e2}?", "Yes" if ok else "No", ["Substitute the point into BOTH equations.", "A solution must make both equations true.", "Yes" if ok else "No"],
             ["No" if ok else "Yes"], PY("sys_point", eqs=[e1, e2], x=str(tx), y=str(ty)), mode="sa", why=["Checked only one equation"])


@fam("012", mode="mc")
def s6_count(r, L):
    m = nz(r, -4, 4)
    b = r.randint(-6, 6)
    kind = pick(r, ["one", "none", "infinite"])
    e1 = eqline(m, b)
    e2 = eqline(m + pick(r, [1, -1, 2]), b + 1) if kind == "one" else eqline(m, b + pick(r, [2, -3, 4])) if kind == "none" else f"{lin((-2 * m, 'x'), (2, 'y'))} = {2 * b}"
    labs = {"one": "exactly one solution", "none": "no solution", "infinite": "infinitely many solutions"}
    opts = [(labs[k], k == kind) for k in labs] + [("exactly two solutions", False)]
    return Q(f"How many solutions does the system {e1} and {e2} have?", labs[kind], ["Compare slopes and y-intercepts.", "Different slopes: one solution. Same slope, different intercept: no solution. Same line: infinitely many.", f"{labs[kind]}."],
             options=opts, chk=PY("sys_count", eqs=[e1, e2]), mode="mc", tags=["reasoning"])


@fam("012")
def s7_sub(r, L):
    x0, y0 = nz(r, -8, 8), nz(r, -8, 8)
    if L == 0:
        m, b = r.randint(2, 5), None
        b = y0 - m * x0
        a, c = r.randint(1, 5), None
        c = a * x0 + y0
        e1, e2 = eqline(m, b), f"{lin((a, 'x'), (1, 'y'))} = {c}"
    else:
        a, b2 = nz(r, -5, 5), nz(r, -5, 5)
        e1 = f"x = {lin((pick(r, [2, 3, -2]), 'y'), (0, ''))}"
        k = int(re.search(r"(-?\d+)y", e1).group(1))
        need(x0 == k * y0 or True)
        x0 = k * y0 + r.randint(-5, 5)
        cst = x0 - k * y0
        e1 = f"x = {lin((k, 'y'), (cst, ''))}"
        c2 = a * x0 + b2 * y0
        e2 = f"{lin((a, 'x'), (b2, 'y'))} = {c2}"
        need(a * k + b2 != 0)
    return Q(f"Solve the system by substitution: {e1} and {e2}", f"({x0}, {y0})", [f"Substitute the expression from the first equation into the second.", "Solve the resulting one-variable equation.",
                                                                               "Substitute back to find the other variable.", f"Solution: ({x0}, {y0})."],
             [f"({y0}, {x0})", f"({-x0}, {y0})", f"({x0}, {-y0})"], {"kind": "sys", "eqs": [e1, e2]}, why=["Switched x and y", "Made a sign error in x", "Made a sign error in y"], tags=["multistep"])


@fam("12")
def s7_context(r, L):
    a, c = r.randint(5, 30), r.randint(5, 30)
    pa, pc = r.randint(8, 15), r.randint(3, 7)
    tot, money_ = a + c, pa * a + pc * c
    return Q(f"A theater sold {tot} tickets for ${money_}. Adult tickets cost ${pa} and child tickets cost ${pc}. How many adult tickets were sold?", str(a),
             [f"a + c = {tot} and {pa}a + {pc}c = {money_}.", f"Substitute c = {tot} - a: {pa}a + {pc}({tot} - a) = {money_}.", f"{pa - pc}a = {money_ - pc * tot}.", f"a = {a}."],
             [str(c), str(money_ // pa), str(tot // 2)], PY("conds", vars=["a"], conds=[f"{pa}a + {pc}({tot} - a) = {money_}"]), why=["Gave the number of child tickets", "Divided total money by the adult price", "Split the tickets evenly"],
             tags=["modeling", "multistep"])


# ============================================================== S8 Graphing Linear Inequalities
def shade_draw(m, b, op):
    def draw(path):
        fig, ax = new_fig(5.6, 5.6)
        grid_axes(ax, (-7, 7), (-7, 7))
        xs = [-7, 7]
        ys = [float(m) * x + float(b) for x in xs]
        top = op in (">", "≥")
        ax.fill_between(xs, ys, [7.5 if top else -7.5] * 2, color="#1f4e9c", alpha=0.18)
        ax.plot(xs, ys, color="#1f4e9c", lw=2.4, ls="-" if op in ("≤", "≥") else "--")
        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
        save(fig, path)
    return draw


@fam("012")
def s8_point(r, L):
    m, b = nz(r, -3, 3), r.randint(-5, 5)
    op = pick(r, ["<", ">", "≤", "≥"])
    x, y = r.randint(-5, 5), r.randint(-6, 6)
    if r.random() < 0.3:
        y = m * x + b
    ineq = f"y {op} {lin((m, 'x'), (b, ''))}"
    ok = {"<": y < m * x + b, ">": y > m * x + b, "≤": y <= m * x + b, "≥": y >= m * x + b}[op]
    return Q(f"Is ({x}, {y}) a solution of {ineq}?", "Yes" if ok else "No", [f"Substitute: {y} {op} {m}({x}) {sgn(b)}.", f"{y} {op} {m * x + b} is {'true' if ok else 'false'}.", "Yes" if ok else "No"],
             ["No" if ok else "Yes"], PY("is_sol2", eq=ineq, x=str(x), y=str(y)), mode="sa", why=["Did not check the boundary correctly"])


@fam("012", mode="mc")
def s8_which(r, L):
    m, b = nz(r, -3, 3), r.randint(-4, 4)
    op = pick(r, ["<", ">", "≤", "≥"])
    good = f"y {op} {lin((m, 'x'), (b, ''))}"
    flip = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}
    oc = {"<": "≤", ">": "≥", "≤": "<", "≥": ">"}
    bad = [f"y {flip[op]} {lin((m, 'x'), (b, ''))}", f"y {oc[op]} {lin((m, 'x'), (b, ''))}", f"y {op} {lin((-m, 'x'), (b, ''))}"]
    opts = [(good, True)] + [(x, False) for x in bad]
    r.shuffle(opts)
    alt = f"Graph of the line y = {lin((m, 'x'), (b, ''))} drawn {'solid' if op in ('≤', '≥') else 'dashed'}, with the region {'above' if op in ('>', '≥') else 'below'} the line shaded."
    return Q("Which inequality is shown by the graph?", good, [f"The boundary line is y = {lin((m, 'x'), (b, ''))}.", f"{'Solid' if op in ('≤', '≥') else 'Dashed'} line → {'≤ or ≥' if op in ('≤', '≥') else '< or >'}.",
                                                           f"Shaded {'above' if op in ('>', '≥') else 'below'} → {'y >' if op in ('>', '≥') else 'y <'}.", f"{good}."],
             options=opts, chk=PY("shade_match", m=m, b=b, op=op), mode="mc", tags=["graph"], diagram={"alt": alt, "draw": shade_draw(m, b, op)})


@fam("012", mode="mc")
def s8_boundary(r, L):
    m, b = nz(r, -4, 4), r.randint(-6, 6)
    op = pick(r, ["<", ">", "≤", "≥"])
    line = "solid" if op in ("≤", "≥") else "dashed"
    side = "above" if op in (">", "≥") else "below"
    good = f"{line} line, shade {side}"
    opts = [(f"{l} line, shade {s}", (l, s) == (line, side)) for l in ("solid", "dashed") for s in ("above", "below")]
    return Q(f"How do you graph y {op} {lin((m, 'x'), (b, ''))}?", good, ["≤ and ≥ use a solid boundary; < and > use a dashed boundary.", "y > or y ≥ shade above; y < or y ≤ shade below.", f"{good}."],
             options=opts, chk=PY("boundary_rule", op=op), mode="mc")


@fam("12")
def s5_solve_trend(r, L):
    m, b = r.randint(2, 9), r.randint(5, 40)
    x = r.randint(4, 15)
    y = m * x + b
    return Q(f"A trend line for hours worked (x) and dollars earned (y) is y = {m}x + {b}. About how many hours are needed to earn ${y}?", f"{x} hours",
             [f"Set y = {y}: {y} = {m}x + {b}.", f"Subtract {b}: {y - b} = {m}x.", f"x = {x} hours."], [f"{m * y + b} hours", f"{N(F(y, m))} hours" if y % m == 0 else f"{x + 1} hours", f"{y - b} hours"],
             PY("eq_val", eq=f"{y} = {m}x + {b}", var="x"), why=["Substituted the dollars for x", "Forgot to subtract the intercept", "Forgot to divide by the slope"], tags=["modeling"])


SKILLS = {
    1: dict(name="Relations and Functions", std=["8.F.A.1"], fams=[s1_is_function, s1_domain, s1_graph, s1_evaluate], extra=[err_of(s1_domain), open_of(s1_is_function)]),
    2: dict(name="Equations with Two Variables", std=["8.EE.C.8", "6.EE.C.9"], fams=[s2_is_solution, s2_find_y, s2_table], extra=[err_of(s2_find_y), open_of(s2_find_y), select_of(s2_find_y)]),
    3: dict(name="Slope and y-intercept", std=["8.EE.B.6", "8.F.B.4"], fams=[s3_two_points, s3_from_eq, s3_graph, s3_type], extra=[err_of(s3_two_points), open_of(s3_two_points), select_of(s3_two_points)]),
    4: dict(name="Writing Rules for Linear Functions", std=["8.F.B.4"], fams=[s4_table_rule, s4_two_points, s4_words], extra=[err_of(s4_table_rule), open_of(s4_table_rule)]),
    5: dict(name="Scatter Plots", std=["8.SP.A.1", "8.SP.A.3"], fams=[s5_type, s5_context, s5_predict, s5_solve_trend], extra=[err_of(s5_predict), open_of(s5_predict)]),
    6: dict(name="Solving Systems of Linear Equations by Graphing", std=["8.EE.C.8a"], fams=[s6_graph, s6_check, s6_count], extra=[err_of(s6_graph), open_of(s6_check)]),
    7: dict(name="Solving Systems of Linear Equations by Substitution", std=["8.EE.C.8b"], fams=[s7_sub, s7_context], extra=[err_of(s7_sub), open_of(s7_sub), select_of(s7_sub)]),
    8: dict(name="Graphing Linear Inequalities", std=["A-REI.D.12"], fams=[s8_point, s8_which, s8_boundary], extra=[err_of(s8_point), open_of(s8_point)]),
}
