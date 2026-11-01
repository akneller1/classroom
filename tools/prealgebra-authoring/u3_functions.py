"""Unit 3 — Linear and Functional Relationships (linear-functional-relationships)."""
from lib import *

UNIT_ID = "linear-functional-relationships"
ABBR = "lfr"


def yeq(m, b, v="y", x="x"):
    return f"{v} = {mx_b(m, b, x)}"


def rand_line(r, L, int_slope=None):
    if int_slope or (int_slope is None and L == 0):
        m = F(nz(r, -4, 4)) if L else F(r.randint(1, 4))
    else:
        m = F(nz(r, -5, 5), pick(r, [1, 2, 3, 4]))
    b = F(r.randint(-6, 6))
    return m, b


def xs_for(r, m, L):
    step = m.denominator
    start = r.randint(-3, 1) * step
    k = pick(r, [1, 1, 2]) if L == 2 else 1
    return [start + i * step * k for i in range(4)]


def line_window(m, b, pts=()):
    ys = [float(m) * x + float(b) for x in (-8, 8)]
    return (-8, 8), (-8, 8)


# ======================================================================= S1 Intro to functions and rules
def pair_set(r, func):
    xs = r.sample(range(-5, 8), 4)
    ys = [r.randint(-6, 9) for _ in xs]
    pairs = list(zip(xs, ys))
    if not func:
        i, j = r.sample(range(4), 2)
        y2 = ys[i] + nz(r, -4, 4)
        pairs[j] = (xs[i], y2)
    return pairs


def ptxt(pairs):
    return "{" + ", ".join(pt(a, b) for a, b in pairs) + "}"


@fam("012", mode="sa")
def s1_is_function(r, L):
    func = r.random() < 0.5
    pairs = pair_set(r, func)
    ans = "yes" if func else "no"
    rep = [x for x, _ in pairs]
    why = "Each input (x-value) is paired with exactly one output." if func else f"The input {[x for x in rep if rep.count(x) > 1][0]} is paired with two different outputs."
    return P(f"Is the relation {ptxt(pairs)} a function? Answer yes or no.", ans, [why], ["no" if func else "yes"],
             chk_py("is_function_pairs", pairs=[[a, b] for a, b in pairs]), tags=["reasoning"], mode="sa")


@fam("012", mode="mc")
def s1_which_function(r, L):
    good = pair_set(r, True)
    bads = [pair_set(r, False) for _ in range(3)]
    if L == 2:
        # a function may repeat outputs: include a repeated-output function as the correct one
        xs = r.sample(range(-5, 8), 4)
        y = r.randint(-5, 5)
        good = [(x, y if i < 2 else y + i) for i, x in enumerate(xs)]
    opts = [(ptxt(b), False) for b in bads] + [(ptxt(good), True)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return P("Which relation is a function?", ptxt(good), ["A function pairs each input with exactly one output.", "Repeated outputs are allowed; a repeated input with different outputs is not."],
             options=opts, chk=chk_py("is_function_set"), tags=["reasoning", "misconception"] if L == 2 else ["reasoning"], mode="mc")


@fam("012")
def s1_rule_from_table(r, L):
    m, b = rand_line(r, L, int_slope=L < 2)
    xs = xs_for(r, m, L) if L < 2 else sorted(r.sample(range(-4, 9), 4))
    ys = [m * x + b for x in xs]
    need(all(y.denominator == 1 for y in ys))
    ans = yeq(m, b)
    wrong = [yeq(m, b + m), yeq(ys[1] - ys[0], b) if ys[1] - ys[0] != m else yeq(-m, b), yeq(b, m) if b != m else yeq(m + 1, b)]
    return P(f"Write a function rule for the table. {table_text(xs, ys)}", ans,
             [f"Rate of change = change in y ÷ change in x = {N(ys[1] - ys[0])} ÷ {N(xs[1] - xs[0])} = {N(m)}.", f"Use a point to find b: {N(ys[0])} = {N(m)}({N(xs[0])}) + b, so b = {N(b)}.", ans],
             wrong, chk_py("rule_fits", pts=[[N(x), N(y)] for x, y in zip(xs, ys)]), tags=["multiple-representations"])


@fam("012")
def s1_evaluate(r, L):
    a, b = nz(r, -6, 6), r.randint(-9, 9)
    x = r.randint(-5, 6)
    if L == 0:
        f = f"f(x) = {mx_b(a, b)}"
        expr = f"{a}*({x}) + {b}"
        v = a * x + b
        wrong = [a + x + b, a * x - b, -v]
    elif L == 1:
        c = r.randint(1, 3)
        f = f"f(x) = {lin((c, 'x²'), (a, 'x'), (b, ''))}".replace("x²x", "x²")
        f = f"f(x) = {c if c > 1 else ''}x² {'+' if a > 0 else '-'} {abs(a) if abs(a) != 1 else ''}x {'+' if b >= 0 else '-'} {abs(b)}"
        expr = f"{c}*({x})^2 + {a}*({x}) + {b}"
        v = c * x * x + a * x + b
        wrong = [-c * x * x + a * x + b, c * 2 * x + a * x + b, v + 2 * a * x if a * x else v + 1]
    else:
        y = r.randint(-5, 6)
        f = f"f(x) = {mx_b(a, b)}"
        t = a * y + b
        return P(f"For {f}, find the value of x for which f(x) = {t}.", f"x = {y}", [f"Set {mx_b(a, b)} = {t}.", f"{coef_text(a, 'x')} = {t - b}, so x = {y}."],
                 [f"x = {a * t + b}", f"x = {-y}", f"x = {N(F(t + b, a))}" if F(t + b, a) != y else f"x = {y + 1}"], {"kind": "eq", "eq": f"{mx_b(a, b)} = {t}"}, tags=["reasoning"])
    return P(f"For {f}, find f({x}).", str(v), [f"Substitute x = {x}: {f.split('= ')[1].replace('x', f'({x})')}.", f"f({x}) = {v}."], [str(w) for w in wrong], chk_val(expr),
             tags=["misconception"] if x < 0 else [])


@fam("01")
def s1_verbal(r, L):
    a, b = r.randint(2, 9), r.randint(1, 15)
    kind = pick(r, ["more", "less", "times-sum"] if L else ["more", "less"])
    if kind == "more":
        s, rule = f"The output is {b} more than {a} times the input.", f"y = {a}x + {b}"
        wr = [f"y = {b}x + {a}", f"y = {a}(x + {b})", f"y = {a}x - {b}"]
    elif kind == "less":
        s, rule = f"The output is {b} less than {a} times the input.", f"y = {a}x - {b}"
        wr = [f"y = {b} - {a}x", f"y = {a}(x - {b})", f"y = {a}x + {b}"]
    else:
        s, rule = f"The output is {a} times the sum of the input and {b}.", f"y = {a}(x + {b})"
        wr = [f"y = {a}x + {b}", f"y = {a} + x + {b}", f"y = {b}(x + {a})"]
    return P(f"Write a function rule (y in terms of x): \"{s}\"", rule, ["Translate the words into operations on x.", rule], wr,
             {"kind": "equiv", "expr": rule.split("= ")[1], "vars": ["x"]}, tags=["modeling"])


@fam("12")
def s1_domain_range(r, L):
    pairs = pair_set(r, True)
    which = pick(r, ["domain", "range"])
    vals = sorted({a for a, _ in pairs}) if which == "domain" else sorted({b for _, b in pairs})
    ans = "{" + ", ".join(str(v) for v in vals) + "}"
    other = sorted({b for _, b in pairs}) if which == "domain" else sorted({a for a, _ in pairs})
    wr = ["{" + ", ".join(str(v) for v in other) + "}", "{" + ", ".join(str(v) for v in sorted(set(vals) | set(other))) + "}", "{" + ", ".join(str(v) for v in vals[:-1]) + "}"]
    return P(f"What is the {which} of the function {ptxt(pairs)}?", ans, [f"The {which} is the set of all {'inputs (x-values)' if which == 'domain' else 'outputs (y-values)'}, listed once each.", ans],
             wr, chk_py("domain_range", pairs=[[a, b] for a, b in pairs], which=which), tags=["misconception"])


@fam("2", mode="mc")
def s1_vertical_line(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    shapes = {"line": plane_draw(lines=[(m, b)]),
              "vertical": plane_draw(lines=[(None, r.randint(-5, 5))]),
              "circle": plane_draw(polys=[([(3 * math.cos(t / 20 * 2 * math.pi), 3 * math.sin(t / 20 * 2 * math.pi)) for t in range(20)], None, None, True)]),
              "sideways": plane_draw(polys=[([(y * y / 3 - 4, y) for y in [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]], None, None, False)])}
    order = ["line", "vertical", "circle", "sideways"]
    r.shuffle(order)
    good = "ABCD"[order.index("line")]
    alt = "Four graphs: " + "; ".join(f"Graph {l}: " + {"line": f"a slanted line y = {mx_b(m, b)}", "vertical": "a vertical line", "circle": "a circle centered at the origin with radius 3",
                                                         "sideways": "a parabola opening to the right"}[k] for l, k in zip("ABCD", order))
    return P("Which graph represents y as a function of x?", f"Graph {good}", ["Use the vertical line test: a graph is a function if no vertical line crosses it more than once.",
                                                                               "Only the non-vertical line passes; the others have some x-value with two or more y-values."],
             options=[(f"Graph {l}", l == good) for l in "ABCD"], chk=chk_py("vlt_choice", kinds=order), diagram={"draw": panels_draw([shapes[k] for k in order]), "alt": alt},
             tags=["graph", "reasoning"], mode="mc")


@fam("012")
def s1_select(r, L):
    f1, f2 = pair_set(r, True), pair_set(r, True)
    n1, n2 = pair_set(r, False), pair_set(r, False)
    eqf = f"y = {mx_b(nz(r, -4, 4), r.randint(-5, 5))}"
    eqn = f"x = {r.randint(-5, 5)}"
    opts = [(ptxt(f1), True), (ptxt(f2), True), (eqf, True), (ptxt(n1), False), (ptxt(n2), False), (eqn, False)]
    need(len({o[0] for o in opts}) == 6)
    return P("Select ALL relations that represent y as a function of x.", None, ["Each input must have exactly one output.", "A vertical line x = c pairs one input with every output, so it is not a function."],
             options=opts, chk=chk_py("is_function_any"), tags=["reasoning"])


@fam("012")
def s1_open(r, L):
    m, b = r.randint(2, 5), r.randint(1, 9)
    x0 = r.randint(2, 8)
    return P(f"A function machine multiplies the input by {m} and then adds {b}.", None, ["Translate the machine.", "Substitute.", "Solve the equation.", "Every input gives one output."],
             parts=[("Write the function rule using f(x).", f"f(x) = {m}x + {b}", {"kind": "equiv", "expr": f"{m}x + {b}", "vars": ["x"]}),
                    (f"Find f({x0}).", str(m * x0 + b), chk_val(f"{m}*{x0} + {b}")),
                    (f"Find the input that gives an output of {m * (x0 + 3) + b}.", str(x0 + 3), {"kind": "eq", "eq": f"{m}x + {b} = {m * (x0 + 3) + b}"}),
                    ("Is this relation a function? Answer yes or no.", "yes", {"kind": "text", "accept": ["yes"]})], tags=["multiple-representations"])


# ======================================================================= S2 Graphing functions
@fam("012", mode="mc")
def s2_point_on(r, L):
    if L < 2:
        m, b = rand_line(r, L, int_slope=True)
        rule = yeq(m, b)
        f = lambda x: m * x + b
        vars_ = "lin"
    else:
        a, c = pick(r, [1, -1, 2]), r.randint(-4, 4)
        rule = f"y = {'-' if a == -1 else '' if a == 1 else a}x² {'+' if c >= 0 else '-'} {abs(c)}"
        f = lambda x: a * x * x + c
    x0 = r.randint(-4, 4)
    good = (x0, f(x0))
    bads = [(x0, f(x0) + 1), (f(x0), x0) if f(x0) != x0 else (x0 + 1, f(x0)), (-x0, -f(x0)) if f(-x0) != -f(x0) else (x0 + 2, f(x0))]
    opts = [(pt(*b_), False) for b_ in bads] + [(pt(*good), True)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return P(f"Which point lies on the graph of {rule}?", pt(*good), [f"Substitute x = {x0}: y = {N(f(x0))}.", f"So {pt(*good)} is on the graph; the others do not satisfy the equation."],
             options=opts, chk=chk_py("on_graph", eq=rule), tags=["misconception"], mode="mc")


@fam("012")
def s2_table_value(r, L):
    if L == 2:
        a, c = pick(r, [1, 2, -1]), r.randint(-3, 3)
        rule = f"y = {'-' if a == -1 else '' if a == 1 else a}x² {'+' if c >= 0 else '-'} {abs(c)}"
        f = lambda x: a * x * x + c
    else:
        m, b = rand_line(r, L, int_slope=True)
        rule = yeq(m, b)
        f = lambda x: m * x + b
    xs = [-2, -1, 0, 1, 2]
    k = r.randint(0, 4)
    ys = [N(f(x)) if i != k else "?" for i, x in enumerate(xs)]
    v = f(xs[k])
    return P(f"Complete the table of values for {rule}. {table_text(xs, ys)}. What value replaces the ?", N(v),
             [f"Substitute x = {xs[k]} into {rule}.", f"y = {N(v)}."], [N(v + 1), N(-v) if v else "1", N(f(-xs[k]) if f(-xs[k]) != v else v + 2)],
             chk_val(rule.split("= ")[1].replace("x", f"({xs[k]})")), tags=["multiple-representations"])


@fam("012")
def s2_read_graph(r, L):
    if L < 2:
        m, b = rand_line(r, L, int_slope=True)
        f = lambda x: m * x + b
        x0 = pick(r, [x for x in range(-6, 7) if -7 <= f(x) <= 7])
        drw = plane_draw(lines=[(m, b)], points=[(0, b, None)])
        alt = f"A line through (0, {N(b)}) with slope {N(m)}; it passes through ({x0}, {N(f(x0))})."
    else:
        pts_ = [(-6, r.randint(-5, 5))]
        for x in (-3, 0, 2, 5):
            pts_.append((x, r.randint(-6, 6)))
        f = lambda x: next(F(y0) + F(y1 - y0, x1 - x0) * (x - x0) for (x0_, y0), (x1, y1) in zip(pts_, pts_[1:]) if x0_ <= x <= x1 for x0 in [x0_])
        x0 = pick(r, [p[0] for p in pts_])
        drw = plane_draw(polys=[(pts_, None)])
        alt = "A piecewise-linear graph through " + ", ".join(pt(*p) for p in pts_) + "."
    v = f(x0)
    need(v.denominator == 1 if isinstance(v, F) else True)
    return P(f"Use the graph of y = f(x). What is f({x0})?", N(v), [f"Find x = {x0} on the x-axis, move to the graph, and read the y-value.", f"f({x0}) = {N(v)}."],
             [N(F(x0) if v != x0 else v + 1), N(-v) if v else "1", N(v + 1)], chk_py("read_value", f=("lin", N(m), N(b)) if L < 2 else ("pw", [[a, b_] for a, b_ in pts_]), x=x0),
             diagram={"draw": drw, "alt": alt}, tags=["graph"])


@fam("012", mode="mc")
def s2_match_graph(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    need(b != 0 and m != b and m != -b)
    cands = [(m, b), (-m, b), (m, -b), (b, m) if abs(b) <= 4 else (-m, -b)]
    need(len(set(cands)) == 4)
    order = list(range(4))
    r.shuffle(order)
    drawers = [plane_draw(lines=[cands[i]], label_every=2) for i in order]
    good = "ABCD"[order.index(0)]
    alt = "Four graphs of lines: " + "; ".join(f"Graph {l}: y = {mx_b(*cands[i])}" for l, i in zip("ABCD", order)) + "."
    return P(f"Which graph shows y = {mx_b(m, b)}?", f"Graph {good}", [f"The y-intercept is {N(b)} and the slope is {N(m)} ({'rises' if m > 0 else 'falls'} left to right).", f"Graph {good} matches both."],
             options=[(f"Graph {l}", l == good) for l in "ABCD"], chk=chk_py("panel_line", lines=[[N(cands[i][0]), N(cands[i][1])] for i in order], eq=f"y = {mx_b(m, b)}"),
             diagram={"draw": panels_draw(drawers), "alt": alt}, tags=["graph", "multiple-representations"], mode="mc")


@fam("2")
def s2_nonlinear_value(r, L):
    a = pick(r, [1, 2, 3, -1])
    x0 = nz(r, -4, 4)
    c = r.randint(1, 5)
    cubic = r.random() < 0.4
    co = "-" if a == -1 else "" if a == 1 else str(a)
    expr = f"{co}x³" if cubic else f"{co}x² - {c}"
    f = (lambda t: a * t ** 3) if cubic else (lambda t: a * t * t - c)
    g = (lambda t: a * 3 * t) if cubic else (lambda t: a * 2 * t - c)
    v = f(x0)
    return P(f"Find the y-coordinate of the point on the graph of y = {expr} with x = {x0}.", str(v),
             [f"Substitute x = {paren(x0)} (use parentheses for negatives).", f"y = {v}."], [str(f(-x0)) if f(-x0) != v else str(v + 2), str(g(x0)), str(v + 1)],
             chk_val(expr.replace("x", f"({x0})")), tags=["misconception"])


def eval_poly(expr, x):
    t = expr.replace("x³", f"({x})**3").replace("x²", f"({x})**2").replace("-(", "-1*(")
    t = re.sub(r"(\d)\(", r"\1*(", t)
    return eval(t)


@fam("012")
def s2_select(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    rule = yeq(m, b)
    xs = r.sample(range(-5, 6), 6)
    opts = []
    for i, x in enumerate(xs):
        y = m * x + b + (0 if i < 3 else nz(r, -3, 3))
        opts.append((pt(x, y), i < 3))
    return P(f"Select ALL points on the graph of {rule}.", None, [f"A point is on the graph exactly when its coordinates make {rule} true."] + [f"{t}: {'yes' if c else 'no'}." for t, c in opts],
             options=opts, chk=chk_py("on_graph", eq=rule), tags=["multiple-representations"])


@fam("012")
def s2_open(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    rule = yeq(m, b)
    return P(f"Graph the function {rule} by making a table.", None, ["Substitute each x.", "Substitute each x.", "Substitute each x.", "The points lie on one line."],
             parts=[("Find y when x = -2.", N(m * -2 + b), chk_val(f"{N(m)}*(-2) + {N(b)}")), ("Find y when x = 0.", N(b), chk_val(N(b))),
                    ("Find y when x = 2.", N(m * 2 + b), chk_val(f"{N(m)}*2 + {N(b)}")),
                    ("Is the graph a line, a curve that is not a line, or separate points? (x can be any number.)", "a line", {"kind": "text", "accept": ["a line"]})],
             tags=["graph", "multiple-representations"])


# ======================================================================= S3 Linear vs nonlinear
def nl_table(r, linear):
    xs = [0, 1, 2, 3, 4]
    if linear:
        m, b = nz(r, -5, 5), r.randint(-5, 9)
        ys = [m * x + b for x in xs]
    else:
        kind = pick(r, ["sq", "dbl", "bump"])
        if kind == "sq":
            ys = [x * x + r.randint(-3, 3) for x in xs]
            c = ys[0] - 0
            ys = [x * x + c for x in xs]
        elif kind == "dbl":
            a = r.randint(1, 3)
            ys = [a * 2 ** x for x in xs]
        else:
            m, b = nz(r, -4, 4), r.randint(-3, 5)
            ys = [m * x + b for x in xs]
            ys[3] += nz(r, -2, 2)
    return xs, ys


@fam("012", mode="sa")
def s3_table(r, L):
    lin_ = r.random() < 0.5
    xs, ys = nl_table(r, lin_)
    if L == 2:
        perm = [0, 2, 1, 4, 3]
        xs, ys = [xs[i] for i in perm], [ys[i] for i in perm]
    ans = "linear" if lin_ else "nonlinear"
    return P(f"Does the table represent a linear or nonlinear function? {table_text(xs, ys)}", ans,
             ["Order by x and compare the change in y for each change of 1 in x.", "Constant rate of change → linear; otherwise nonlinear." + (" (Order the x-values first.)" if L == 2 else "")],
             ["nonlinear" if lin_ else "linear"], chk_py("table_linear", xs=xs, ys=ys), tags=["reasoning"], mode="sa")


EQ_LIN = ["y = {a}x + {b}", "y = {b} - {a}x", "y = x/{a}", "{a}x + {b}y = {c}", "y = {b}", "y = {a}(x - {b})"]
EQ_NL = ["y = {a}x² + {b}", "y = {a}/x", "y = x³ - {b}", "y = {a}ˣ", "xy = {c}", "y = √x + {b}"]


@fam("012", mode="mc")
def s3_equation(r, L):
    a, b, c = r.randint(2, 6), r.randint(1, 9), r.randint(2, 12)
    want_lin = r.random() < 0.5
    good = pick(r, EQ_LIN if want_lin else EQ_NL).format(a=a, b=b, c=c)
    bad = [e.format(a=a, b=b, c=c) for e in pick(r, EQ_NL if want_lin else EQ_LIN, 3)]
    opts = [(x, False) for x in bad] + [(good, True)]
    r.shuffle(opts)
    return P(f"Which equation represents a {'linear' if want_lin else 'nonlinear'} function?", good,
             ["A linear function can be written y = mx + b: x appears only to the first power, not in a denominator, exponent, product with y, or root."],
             options=opts, chk=chk_py("eq_linear", want=want_lin), tags=["reasoning"], mode="mc")


@fam("12", mode="mc")
def s3_graph(r, L):
    kinds = ["line", "parab", "abs", "cubic"]
    want_lin = r.random() < 0.5
    m, b = rand_line(r, 1, int_slope=True)
    drawers = {"line": plane_draw(lines=[(m, b)]), "parab": plane_draw(polys=[([(x / 2, (x / 2) ** 2 / 2 - 3) for x in range(-8, 9)], None)]),
               "abs": plane_draw(polys=[([(-7, 4), (0, -3), (7, 4)], None)]), "cubic": plane_draw(polys=[([(x / 2, (x / 2) ** 3 / 8) for x in range(-11, 12)], None)])}
    r.shuffle(kinds)
    if want_lin:
        good = "ABCD"[kinds.index("line")]
    else:
        good = "ABCD"[kinds.index(pick(r, ["parab", "abs", "cubic"]))]
        # only one nonlinear answer allowed: make the others lines
        others = [k for k in kinds if "ABCD"[kinds.index(k)] != good]
        lines = [(F(1), F(-2)), (F(-2), F(1)), (F(1, 2), F(3))]
        for k, ln in zip(others, lines):
            drawers[k + "_l"] = plane_draw(lines=[ln])
        kinds = [k if "ABCD"[i] == good else k + "_l" for i, k in enumerate(kinds)]
    alt = "Four graphs: " + "; ".join(f"Graph {l}: " + ("a straight line" if k == "line" or k.endswith("_l") else {"parab": "a U-shaped curve", "abs": "a V shape", "cubic": "an S-shaped curve"}[k]) for l, k in zip("ABCD", kinds))
    return P(f"Which graph shows a {'linear' if want_lin else 'nonlinear'} function?", f"Graph {good}",
             ["A linear function's graph is a straight (non-vertical) line; curves and bent graphs are nonlinear."],
             options=[(f"Graph {l}", l == good) for l in "ABCD"], chk=chk_py("panel_kind", kinds=kinds, want="linear" if want_lin else "nonlinear"),
             diagram={"draw": panels_draw([drawers[k] for k in kinds]), "alt": alt}, tags=["graph"], mode="mc")


@fam("012", mode="sa")
def s3_context(r, L):
    ctx = [("the perimeter P of a square with side length s", "linear", "P = 4s"), ("the area A of a square with side length s", "nonlinear", "A = s²"),
           ("the total cost C of n tickets at $12 each plus a $5 fee", "linear", "C = 12n + 5"), ("the volume V of a cube with edge length e", "nonlinear", "V = e³"),
           ("the distance d traveled in t hours at a constant 55 miles per hour", "linear", "d = 55t"), ("the number of bacteria b after h hours if the amount doubles every hour, starting at 100", "nonlinear", "b = 100 · 2ʰ"),
           ("the circumference C of a circle with radius r", "linear", "C = 2πr"), ("the area A of a circle with radius r", "nonlinear", "A = πr²"),
           ("the time t to drive 120 miles at speed s", "nonlinear", "t = 120/s"), ("the temperature in °F, F, for a Celsius temperature c", "linear", "F = (9/5)c + 32")]
    s, ans, rule = pick(r, ctx)
    return P(f"Is {s} a linear or nonlinear function?", ans, [f"The rule is {rule}.", "Linear: constant rate of change (variable to the first power, not in a denominator or exponent)." if ans == "linear" else "The rate of change is not constant, so it is nonlinear."],
             ["nonlinear" if ans == "linear" else "linear"], chk_py("rule_linear", rule=rule), tags=["modeling"], mode="sa")


@fam("2")
def s3_complete_linear(r, L):
    m, b = nz(r, -5, 5), r.randint(-6, 9)
    xs = [0, 2, 4, 6]
    ys = [m * x + b for x in xs]
    k = r.randint(1, 3)
    shown = [str(y) if i != k else "?" for i, y in enumerate(ys)]
    return P(f"The table is meant to show a linear function. What value of ? makes it linear? {table_text(xs, shown)}", str(ys[k]),
             [f"Use two known entries: y changes by {2 * m} for each increase of 2 in x.", f"? = {ys[k]}."],
             [str(ys[k] + m), str(ys[k] - 1), str(ys[k] * 2 if ys[k] else 3)], chk_py("makes_linear", xs=xs, ys=shown), tags=["reasoning"])


@fam("012")
def s3_select(r, L):
    a, b, c = r.randint(2, 6), r.randint(1, 9), r.randint(2, 12)
    lins = [e.format(a=a, b=b, c=c) for e in pick(r, EQ_LIN, 3)]
    nls = [e.format(a=a, b=b, c=c) for e in pick(r, EQ_NL, 3)]
    opts = [(x, True) for x in lins] + [(x, False) for x in nls]
    return P("Select ALL equations that represent linear functions.", None, ["Linear functions can be written as y = mx + b."], options=opts, chk=chk_py("eq_linear", want=True), tags=["reasoning"])


@fam("012")
def s3_open(r, L):
    s = r.randint(2, 4)
    xs = [s, s + 1, s + 2, s + 3]
    per = [4 * x for x in xs]
    ar = [x * x for x in xs]
    return P(f"Squares have side lengths {', '.join(map(str, xs))} units.", None, ["Perimeter = 4s.", "Area = s².", "Perimeter differences are constant.", "Area differences change."],
             parts=[("List the perimeters.", ", ".join(map(str, per)), {"kind": "text", "accept": [", ".join(map(str, per))]}),
                    ("List the areas.", ", ".join(map(str, ar)), {"kind": "text", "accept": [", ".join(map(str, ar))]}),
                    ("Is perimeter a linear or nonlinear function of side length?", "linear", chk_py("table_linear", xs=xs, ys=per)),
                    ("Is area a linear or nonlinear function of side length?", "nonlinear", chk_py("table_linear", xs=xs, ys=ar))], tags=["multiple-representations"])


# ======================================================================= S4 Exploring linear functions (slope)
@fam("012")
def s4_slope_points(r, L):
    for _ in range(50):
        x1, y1, x2, y2 = [r.randint(-8, 9) for _ in range(4)]
        if x1 != x2 and (L == 2 or (y2 - y1) % (x2 - x1) == 0 or L == 1):
            break
    need(x1 != x2)
    m = F(y2 - y1, x2 - x1)
    wrong = [N(F(x2 - x1, y2 - y1)) if y2 != y1 else "undefined", N(-m) if m else "1", N(F(y2 + y1, x2 + x1)) if x2 + x1 else N(m + 1)]
    return P(f"Find the slope of the line through {pt(x1, y1)} and {pt(x2, y2)}.", N(m),
             [f"slope = (y₂ - y₁) ÷ (x₂ - x₁) = ({y2} - {paren(y1)}) ÷ ({x2} - {paren(x1)}) = {y2 - y1} ÷ {x2 - x1}.", f"= {N(m)}."], wrong,
             chk_py("slope_of", pts=[[x1, y1], [x2, y2]]), tags=["misconception"])


@fam("012")
def s4_slope_table(r, L):
    m, b = rand_line(r, L, int_slope=L == 0)
    xs = xs_for(r, m, L)
    if L == 2:
        xs = [xs[0], xs[0] + 2 * m.denominator, xs[0] + 3 * m.denominator, xs[0] + 6 * m.denominator]
    ys = [m * x + b for x in xs]
    need(all(y.denominator == 1 for y in ys))
    return P(f"Find the rate of change (slope) of the linear function in the table. {table_text(xs, ys)}", N(m),
             [f"Δy ÷ Δx = ({N(ys[1])} - {paren(ys[0])}) ÷ ({N(xs[1])} - {paren(xs[0])}) = {N(m)}."], [N(ys[1] - ys[0]), N(1 / m) if m else "1", N(-m)],
             chk_py("slope_of", pts=[[N(x), N(y)] for x, y in zip(xs, ys)]), tags=["multiple-representations"])


@fam("012")
def s4_slope_graph(r, L):
    m, b = rand_line(r, L, int_slope=L == 0)
    need(m != 0)
    x0 = 0
    x1 = m.denominator * pick(r, [1, 2]) if L else 1
    need(abs(float(m * x1 + b)) <= 7)
    p0, p1 = (0, b), (x1, m * x1 + b)
    drw = plane_draw(lines=[(m, b)], points=[(p0[0], p0[1], pt(*p0)), (p1[0], p1[1], pt(*p1))])
    return P("Find the slope of the line shown.", N(m), [f"Use the marked points {pt(*p0)} and {pt(*p1)}.", f"rise ÷ run = {N(p1[1] - p0[1])} ÷ {N(p1[0] - p0[0])} = {N(m)}."],
             [N(1 / m), N(-m), N(b) if b != m else N(m + 1)], chk_py("slope_of", pts=[[N(p0[0]), N(p0[1])], [N(p1[0]), N(p1[1])]]),
             diagram={"draw": drw, "alt": f"A line through the marked points {pt(*p0)} and {pt(*p1)}."}, tags=["graph"])


@fam("012", mode="mc")
def s4_slope_type(r, L):
    kind = pick(r, ["positive", "negative", "zero", "undefined"])
    a, c = r.randint(-6, 6), r.randint(-6, 6)
    if kind == "positive":
        p1, p2 = (a, c), (a + r.randint(1, 4), c + r.randint(1, 5))
    elif kind == "negative":
        p1, p2 = (a, c), (a + r.randint(1, 4), c - r.randint(1, 5))
    elif kind == "zero":
        p1, p2 = (a, c), (a + r.randint(1, 6), c)
    else:
        p1, p2 = (a, c), (a, c + r.randint(1, 6))
    opts = [(t, t == kind) for t in ["positive", "negative", "zero", "undefined"]]
    return P(f"Is the slope of the line through {pt(*p1)} and {pt(*p2)} positive, negative, zero, or undefined?", kind,
             [f"Δy = {p2[1] - p1[1]}, Δx = {p2[0] - p1[0]}.", {"positive": "Both change in the same direction: positive.", "negative": "y decreases as x increases: negative.",
                                                               "zero": "Δy = 0: horizontal line, slope 0.", "undefined": "Δx = 0: vertical line, slope undefined."}[kind]],
             options=opts, chk=chk_py("slope_kind", pts=[list(p1), list(p2)]), tags=["reasoning"], mode="mc")


@fam("2")
def s4_missing_coord(r, L):
    m = F(nz(r, -4, 4), pick(r, [1, 2, 3]))
    x1, y1 = r.randint(-5, 5), r.randint(-5, 5)
    dx = m.denominator * pick(r, [1, 2, 3])
    x2 = x1 + dx
    y2 = y1 + m * dx
    return P(f"A line with slope {N(m)} passes through {pt(x1, y1)} and ({x2}, k). Find k.", f"k = {N(y2)}",
             [f"slope = (k - {paren(y1)}) ÷ ({x2} - {paren(x1)}) = {N(m)}.", f"k - {paren(y1)} = {N(m)} · {dx} = {N(m * dx)}, so k = {N(y2)}."],
             [f"k = {N(y1 - m * dx)}", f"k = {N(y1 + m)}", f"k = {N(y2 + 1)}"], chk_py("missing_y", m=N(m), p=[x1, y1], x=x2), tags=["reasoning", "challenge"])


@fam("12")
def s4_intercept(r, L):
    m, b = rand_line(r, L, int_slope=True)
    x1 = r.randint(1, 5) * pick(r, [1, -1])
    p1 = (x1, m * x1 + b)
    x2 = x1 + r.randint(1, 4)
    p2 = (x2, m * x2 + b)
    return P(f"A line passes through {pt(*p1)} and {pt(*p2)}. What is its y-intercept?", N(b),
             [f"slope = {N(m)}.", f"b = y - mx = {N(p1[1])} - {paren(m)}({x1}) = {N(b)}."], [N(m), N(p1[1]), N(-b) if b else "1"],
             chk_py("intercept_of", pts=[[N(p1[0]), N(p1[1])], [N(p2[0]), N(p2[1])]]), tags=["multistep"])


@fam("012")
def s4_error(r, L):
    x1, y1, x2, y2 = r.randint(-5, 5), r.randint(-5, 5), r.randint(-5, 5), r.randint(-5, 5)
    need(x1 != x2 and y1 != y2 and F(y2 - y1, x2 - x1) != F(x2 - x1, y2 - y1))
    m = F(y2 - y1, x2 - x1)
    return P(f"Dana found the slope through {pt(x1, y1)} and {pt(x2, y2)} as ({x2} - {paren(x1)}) ÷ ({y2} - {paren(y1)}) = {N(F(x2 - x1, y2 - y1))}. What is the correct slope?",
             N(m), ["Dana divided change in x by change in y. Slope is change in y ÷ change in x.", f"({y2} - {paren(y1)}) ÷ ({x2} - {paren(x1)}) = {N(m)}."],
             [N(F(x2 - x1, y2 - y1)), N(-m), N(F(y2 - y1, x1 - x2 - (x2 - x1)))], chk_py("slope_of", pts=[[x1, y1], [x2, y2]]), tags=["error-analysis", "misconception"])


@fam("012")
def s4_select(r, L):
    m = F(nz(r, -4, 4), pick(r, [1, 2]))
    x0, y0 = r.randint(-4, 4), r.randint(-4, 4)
    good = [(x0 + m.denominator * k, y0 + m.numerator * k) for k in (1, 2, -1)]
    bad = [(x0 + m.denominator, y0 - m.numerator), (x0 + m.numerator, y0 + m.denominator) if m.numerator != m.denominator else (x0 + 2, y0 + 1), (x0 + 1, y0 + m.numerator + 1)]
    opts = [(f"{pt(x0, y0)} and {pt(*g)}", True) for g in good] + [(f"{pt(x0, y0)} and {pt(*b_)}", False) for b_ in bad]
    need(len({o[0] for o in opts}) == 6)
    return P(f"Select ALL pairs of points that lie on a line with slope {N(m)}.", None, ["Compute Δy ÷ Δx for each pair."], options=opts,
             chk=chk_py("pair_slope", m=N(m)), tags=["reasoning"])


@fam("012")
def s4_open(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    p1, p2 = (1, m + b), (3, 3 * m + b)
    return P(f"A line passes through {pt(*p1)} and {pt(*p2)}.", None, ["Δy ÷ Δx.", "b = y - mx.", "Substitute.", "Sign of slope."],
             parts=[("Find the slope.", N(m), chk_py("slope_of", pts=[list(map(N, p1)), list(map(N, p2))])), ("Find the y-intercept.", N(b), chk_py("intercept_of", pts=[list(map(N, p1)), list(map(N, p2))])),
                    ("Find y when x = 5.", N(5 * m + b), chk_val(f"{N(m)}*5 + {N(b)}")),
                    ("Does the line rise or fall from left to right?", "rise" if m > 0 else "fall", {"kind": "text", "accept": ["rise" if m > 0 else "fall"]})], tags=["multistep"])


# ======================================================================= S5 Equations of linear functions
@fam("012")
def s5_slope_point(r, L):
    m, b = rand_line(r, L, int_slope=L == 0)
    x0 = m.denominator * r.randint(-2, 3)
    y0 = m * x0 + b
    ans = yeq(m, b)
    return P(f"Write the equation in slope-intercept form of the line with slope {N(m)} through {pt(x0, y0)}.", ans,
             [f"b = y - mx = {N(y0)} - ({N(m)})({x0}) = {N(b)}.", ans], [yeq(m, y0), yeq(m, b + 2 * m * x0) if x0 else yeq(m, -b if b else 1), yeq(-m, b)],
             chk_py("line_through", m=N(m), pts=[[N(x0), N(y0)]]), tags=["multistep"])


@fam("012")
def s5_two_points(r, L):
    m, b = rand_line(r, L, int_slope=L < 2)
    x1 = m.denominator * r.randint(-3, 0)
    x2 = x1 + m.denominator * r.randint(1, 3)
    p1, p2 = (x1, m * x1 + b), (x2, m * x2 + b)
    ans = yeq(m, b)
    return P(f"Write the equation of the line through {pt(*p1)} and {pt(*p2)} in slope-intercept form.", ans,
             [f"m = ({N(p2[1])} - {paren(p1[1])}) ÷ ({x2} - {paren(x1)}) = {N(m)}.", f"b = {N(p1[1])} - ({N(m)})({x1}) = {N(b)}.", ans],
             [yeq(1 / m, b) if m else yeq(F(1), b), yeq(m, p1[1]), yeq(-m, b)], chk_py("line_through", pts=[[N(p1[0]), N(p1[1])], [N(p2[0]), N(p2[1])]]), tags=["multistep"])


@fam("012")
def s5_context(r, L):
    k = pick(r, ["phone", "tank", "taxi"])
    if k == "phone":
        b, m = r.randint(10, 50), r.randint(2, 15)
        return P(f"A phone plan costs ${b} per month plus ${m} for each gigabyte g of data used. Write an equation for the monthly cost C.", f"C = {m}g + {b}",
                 [f"Starting value (g = 0): {b}. Rate: {m} per gigabyte.", f"C = {m}g + {b}."], [f"C = {b}g + {m}", f"C = {m + b}g", f"C = {m}g - {b}"],
                 {"kind": "equiv", "expr": f"{m}g + {b}", "vars": ["g"]}, tags=["modeling"])
    if k == "tank":
        v0, rate = r.randint(20, 80), r.randint(2, 6)
        t, v1 = r.randint(2, 6), None
        v1 = v0 - rate * t
        need(v1 > 0)
        if L == 0:
            return P(f"A tank holds {v0} gallons and drains at {rate} gallons per minute. Write an equation for the amount A after t minutes.", f"A = {v0} - {rate}t",
                     [f"Start {v0}; decreases {rate} each minute.", f"A = {v0} - {rate}t."], [f"A = {rate}t + {v0}", f"A = {v0}t - {rate}", f"A = {rate}t - {v0}"],
                     {"kind": "equiv", "expr": f"{v0} - {rate}t", "vars": ["t"]}, tags=["modeling"])
        return P(f"A tank drains at a constant rate. After {t} minutes it holds {v1} gallons; after {t + 3} minutes it holds {v1 - 3 * rate} gallons. Write an equation for the amount A after t minutes.",
                 f"A = -{rate}t + {v0}", [f"Rate = ({v1 - 3 * rate} - {v1}) ÷ 3 = -{rate} gallons per minute.", f"A = -{rate}t + b; {v1} = -{rate}({t}) + b, so b = {v0}."],
                 [f"A = {rate}t + {v0}", f"A = -{rate}t + {v1}", f"A = -{3 * rate}t + {v0}"], {"kind": "equiv", "expr": f"-{rate}t + {v0}", "vars": ["t"]}, tags=["modeling", "multistep"])
    b, m = F(r.randint(25, 45), 10), F(r.randint(15, 35), 10)
    n1, n2 = r.randint(2, 5), r.randint(6, 12)
    return P(f"A taxi ride of {n1} miles costs ${D(b + m * n1)} and a ride of {n2} miles costs ${D(b + m * n2)}. The cost is a linear function of miles. Write an equation for cost C after m miles.",
             f"C = {D(m)}m + {D(b)}", [f"Rate = ({D(b + m * n2)} - {D(b + m * n1)}) ÷ ({n2} - {n1}) = {D(m)}.", f"b = {D(b + m * n1)} - {D(m)}({n1}) = {D(b)}."],
             [f"C = {D(b)}m + {D(m)}", f"C = {D(m)}m + {D(b + m * n1)}", f"C = {D(m + 1)}m + {D(b)}"], {"kind": "equiv", "expr": f"{D(m)}m + {D(b)}", "vars": ["m"]}, tags=["modeling"])


@fam("12")
def s5_standard_to_si(r, L):
    a, bb = nz(r, -6, 6), nz(r, -6, 6)
    c = r.randint(-12, 12)
    need(math.gcd(math.gcd(abs(a), abs(bb)), abs(c) or abs(a)) == 1)
    m, b = F(-a, bb), F(c, bb)
    ans = yeq(m, b)
    return P(f"Write {lin((a, 'x'), (bb, 'y'))} = {c} in slope-intercept form.", ans, [f"Subtract {coef_text(a, 'x')}: {coef_text(bb, 'y')} = {lin((-a, 'x'), (c, ''))}.", f"Divide by {bb}: {ans}."],
             [yeq(-m, b), yeq(m, -b) if b else yeq(m, F(1)), yeq(F(a, bb), F(c))], {"kind": "equiv", "expr": mx_b(m, b), "vars": ["x"]}, tags=["multiple-representations"])


@fam("2", mode="mc")
def s5_parallel(r, L):
    m, b = rand_line(r, 1, int_slope=False)
    x0, y0 = r.randint(-4, 4), r.randint(-4, 4)
    nb = y0 - m * x0
    need(nb != b)
    ans = yeq(m, nb)
    wr = [yeq(m, b), yeq(-1 / m, y0 + 1 / m * x0) if m else yeq(F(1), nb), yeq(m, y0)]
    opts = [(w, False) for w in wr] + [(ans, True)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return P(f"Which equation describes the line through {pt(x0, y0)} with the same rate of change as {yeq(m, b)}?", ans,
             [f"Same rate of change → slope {N(m)}.", f"b = {y0} - ({N(m)})({x0}) = {N(nb)}."], options=opts, chk=chk_py("line_through", m=N(m), pts=[[x0, y0]]), tags=["challenge"], mode="mc")


@fam("012")
def s5_error(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    x0 = nz(r, -4, 4)
    y0 = m * x0 + b
    wrong_b = y0 + m * x0
    need(wrong_b != b)
    return P(f"Max wrote the line with slope {N(m)} through {pt(x0, y0)} as {yeq(m, wrong_b)}, using b = y + mx. What is the correct equation?", yeq(m, b),
             ["Substitute into y = mx + b and solve for b: b = y - mx.", f"b = {N(y0)} - ({N(m)})({x0}) = {N(b)}.", yeq(m, b)],
             [yeq(m, wrong_b), yeq(m, y0), yeq(-m, b)], chk_py("line_through", m=N(m), pts=[[x0, N(y0)]]), tags=["error-analysis", "misconception"])


@fam("012")
def s5_select(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    good = [yeq(m, b), f"{lin((-m, 'x'), (1, 'y'))} = {N(b)}", f"y - {paren(m + b)} = {N(m)}(x - 1)".replace("- (-", "+ (").replace("(x - 1)", "(x - 1)")]
    good[2] = f"y - {N(m + b)} = {N(m)}(x - 1)" if m + b >= 0 else f"y + {N(-(m + b))} = {N(m)}(x - 1)"
    bad = [yeq(-m, b), yeq(m, -b) if b else yeq(m, F(2)), yeq(b, m) if b != m else yeq(m + 1, b)]
    opts = [(g, True) for g in good] + [(x, False) for x in bad]
    need(len({o[0] for o in opts}) == 6)
    return P(f"Select ALL equations of the line with slope {N(m)} and y-intercept {N(b)}.", None, ["Each correct equation rearranges to the same y = mx + b."],
             options=opts, chk=chk_py("same_line", m=N(m), b=N(b)), tags=["multiple-representations"])


@fam("012")
def s5_open(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    p1, p2 = (2, 2 * m + b), (5, 5 * m + b)
    return P(f"A linear function passes through {pt(*p1)} and {pt(*p2)}.", None, ["Slope.", "Intercept.", "Equation.", "Evaluate."],
             parts=[("Find the slope.", N(m), chk_py("slope_of", pts=[list(map(N, p1)), list(map(N, p2))])), ("Find the y-intercept.", N(b), chk_py("intercept_of", pts=[list(map(N, p1)), list(map(N, p2))])),
                    ("Write the equation.", yeq(m, b), chk_py("line_through", pts=[list(map(N, p1)), list(map(N, p2))])), ("Find y when x = -3.", N(-3 * m + b), chk_val(f"{N(m)}*(-3) + {N(b)}"))],
             tags=["multistep"])


# ======================================================================= S6 Graphs of linear functions
@fam("012")
def s6_equation_from_graph(r, L):
    m, b = rand_line(r, L, int_slope=L == 0)
    x1 = m.denominator * pick(r, [1, 2])
    need(abs(float(m * x1 + b)) <= 7 and abs(float(b)) <= 7)
    drw = plane_draw(lines=[(m, b)], points=[(0, b, None), (x1, m * x1 + b, None)])
    ans = yeq(m, b)
    return P("Write the equation of the graphed line in slope-intercept form.", ans,
             [f"y-intercept: (0, {N(b)}).", f"From (0, {N(b)}) to {pt(x1, m * x1 + b)}: rise {N(m * x1)}, run {x1}, slope {N(m)}.", ans],
             [yeq(1 / m, b) if m else yeq(F(1), b), yeq(-m, b), yeq(m, -b) if b else yeq(m, F(1))], chk_py("line_through", pts=[[0, N(b)], [x1, N(m * x1 + b)]]),
             diagram={"draw": drw, "alt": f"A line crossing the y-axis at (0, {N(b)}) and passing through {pt(x1, m * x1 + b)}; both points are marked."}, tags=["graph"])


@fam("012")
def s6_intercepts(r, L):
    a, bb = nz(r, -6, 6), nz(r, -6, 6)
    xi, yi = F(r.randint(-6, 6)), F(r.randint(-6, 6))
    need(xi != 0 and yi != 0)
    c = a * xi
    need(F(c, bb) == yi or True)
    # build line through (xi,0) and (0,yi): x/xi + y/yi = 1 -> (yi)x + (xi)y = xi*yi
    A, B, C = yi, xi, xi * yi
    g = math.gcd(math.gcd(int(A), int(B)), int(C))
    A, B, C = A / g, B / g, C / g
    which = pick(r, ["x", "y"])
    eq = f"{lin((A, 'x'), (B, 'y'))} = {N(C)}"
    ans = pt(xi, 0) if which == "x" else pt(0, yi)
    return P(f"Find the {which}-intercept of the graph of {eq}.", ans, [f"At the {which}-intercept, {'y' if which == 'x' else 'x'} = 0.", f"Solve: {ans}."],
             [pt(0, xi) if which == "x" else pt(yi, 0), pt(0, yi) if which == "x" else pt(xi, 0), pt(C, 0) if which == "x" else pt(0, C)],
             chk_py("intercept_pt", eq=eq, which=which), tags=["misconception"])


@fam("012", mode="mc")
def s6_compare(r, L):
    m1, b1 = rand_line(r, 1, int_slope=True)
    m2 = m1 + pick(r, [-2, -1, 1, 2])
    need(m2 != 0)
    b2 = F(r.randint(-5, 5))
    q = pick(r, ["steeper", "higher_int"])
    drw = plane_draw(lines=[(m1, b1, COLORS[0], "Line A"), (m2, b2, COLORS[1], "Line B")])
    alt = f"Line A: y = {mx_b(m1, b1)} (solid). Line B: y = {mx_b(m2, b2)} (dashed)."
    if q == "steeper":
        need(abs(m1) != abs(m2))
        good = "Line A" if abs(m1) > abs(m2) else "Line B"
        prompt = "Which line is steeper?"
    else:
        need(b1 != b2)
        good = "Line A" if b1 > b2 else "Line B"
        prompt = "Which line has the greater y-intercept?"
    opts = [("Line A", good == "Line A"), ("Line B", good == "Line B"), ("They are the same", False), ("Cannot be determined from the graph", False)]
    return P(prompt, good, [f"Line A: slope {N(m1)}, y-intercept {N(b1)}. Line B: slope {N(m2)}, y-intercept {N(b2)}.", "Steepness compares |slope|." if q == "steeper" else "Compare where each line crosses the y-axis."],
             options=opts, chk=chk_py("compare_lines", A=[N(m1), N(b1)], B=[N(m2), N(b2)], q=q), diagram={"draw": drw, "alt": alt}, tags=["graph"], mode="mc")


@fam("12", mode="mc")
def s6_which_graph(r, L):
    a, bb = r.randint(1, 4), r.randint(1, 4)
    c = a * bb * pick(r, [1, 2])
    xi, yi = F(c, a), F(c, bb)
    need(xi <= 7 and yi <= 7)
    lines = [(-yi / xi, yi), (yi / xi, yi), (-xi / yi, xi), (-yi / xi, -yi)]
    need(len({(l[0], l[1]) for l in lines}) == 4)
    order = [0, 1, 2, 3]
    r.shuffle(order)
    good = "ABCD"[order.index(0)]
    alt = "Four graphs: " + "; ".join(f"Graph {l}: line through (0, {N(lines[i][1])}) with slope {N(lines[i][0])}" for l, i in zip("ABCD", order))
    return P(f"Which graph shows {lin((a, 'x'), (bb, 'y'))} = {c}?", f"Graph {good}", [f"x-intercept: {a}x = {c} → ({N(xi)}, 0). y-intercept: {bb}y = {c} → (0, {N(yi)}).", f"Graph {good} passes through both intercepts."],
             options=[(f"Graph {l}", l == good) for l in "ABCD"], chk=chk_py("panel_line", lines=[[N(lines[i][0]), N(lines[i][1])] for i in order], eq=f"{lin((a, 'x'), (bb, 'y'))} = {c}"),
             diagram={"draw": panels_draw([plane_draw(lines=[lines[i]], label_every=2) for i in order]), "alt": alt}, tags=["graph"], mode="mc")


@fam("2")
def s6_translate(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    k = nz(r, -5, 5)
    return P(f"The graph of y = {mx_b(m, b)} is shifted {'up' if k > 0 else 'down'} {abs(k)} units. What is the equation of the new line?", yeq(m, b + k),
             [f"A vertical shift changes only the y-intercept: {N(b)} {'+' if k > 0 else '-'} {abs(k)} = {N(b + k)}.", "The slope stays the same."],
             [yeq(m + k, b), yeq(m, b - k), yeq(m * k, b)], {"kind": "equiv", "expr": mx_b(m, b + k), "vars": ["x"]}, tags=["reasoning"])


@fam("012")
def s6_error(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    need(b != 0 and m != b)
    opts = [(f"No. The slope is {N(m)} and the y-intercept is {N(b)}.", True), (f"Yes. The slope is {N(b)} and the y-intercept is {N(m)}.", False),
            (f"No. The slope is {N(-m)} and the y-intercept is {N(b)}.", False), (f"No. The slope is {N(m)} and the y-intercept is {N(-b)}.", False)]
    r.shuffle(opts)
    return P(f"Alex says the graph of y = {mx_b(m, b)} has slope {N(b)} and y-intercept {N(m)}. Is Alex correct?", f"No. The slope is {N(m)} and the y-intercept is {N(b)}.",
             ["In y = mx + b, m (the coefficient of x) is the slope and b is the y-intercept.", "Alex switched them."], options=opts,
             chk=chk_py("slope_int_statement", m=N(m), b=N(b)), tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s6_select(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    need(b != 0)
    stmts = [(f"The slope is {N(m)}.", True), (f"The y-intercept is {N(b)}.", True), (f"The line passes through {pt(1, m + b)}.", True),
             (f"The slope is {N(b)}.", b == m), (f"The line passes through {pt(b, 0)}.", m * b + b == 0), (f"The line {'falls' if m > 0 else 'rises'} from left to right.", False)]
    need(not stmts[3][1] and not stmts[4][1])
    drw = plane_draw(lines=[(m, b)])
    return P(f"The graph of y = {mx_b(m, b)} is shown. Select ALL true statements.", None, [f"Slope {N(m)}, y-intercept {N(b)}; at x = 1, y = {N(m + b)}."],
             options=stmts, chk=chk_py("line_statement", m=N(m), b=N(b)), diagram={"draw": drw, "alt": f"The line y = {mx_b(m, b)}."}, tags=["graph"])


@fam("012")
def s6_open(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    need(m != 0)
    xi = -b / m
    return P(f"Consider the line y = {mx_b(m, b)}.", None, ["Coefficient of x.", "Constant term.", "Set y = 0.", "Substitute."],
             parts=[("What is the slope?", N(m), chk_val(N(m))), ("What is the y-intercept (as a point)?", pt(0, b), chk_py("intercept_pt", eq=f"y = {mx_b(m, b)}", which="y")),
                    ("What is the x-intercept (as a point)?", pt(xi, 0), chk_py("intercept_pt", eq=f"y = {mx_b(m, b)}", which="x")),
                    ("What is y when x = 4?", N(4 * m + b), chk_val(f"{N(m)}*4 + {N(b)}"))], tags=["graph", "multistep"])


# ======================================================================= S7 Tables of linear functions
@fam("012")
def s7_missing(r, L):
    m, b = rand_line(r, L, int_slope=L == 0)
    xs = xs_for(r, m, L)
    if L == 2:
        xs = [xs[0], xs[0] + m.denominator, xs[0] + 3 * m.denominator, xs[0] + 4 * m.denominator]
    ys = [m * x + b for x in xs]
    need(all(y.denominator == 1 for y in ys))
    k = r.randint(1, 3)
    shown = [N(y) if i != k else "?" for i, y in enumerate(ys)]
    return P(f"The table shows a linear function. Find the missing value. {table_text(xs, shown)}", N(ys[k]),
             [f"Rate of change = {N(m)} per 1 unit of x.", f"y at x = {N(xs[k])}: {N(ys[k])}."], [N(ys[k] + m), N(ys[k - 1] + (ys[1] - ys[0]) if k > 1 else ys[k] - 1), N(ys[k] * 2) if ys[k] else "1"],
             chk_py("makes_linear", xs=xs, ys=shown), tags=["reasoning"])


@fam("012")
def s7_rule(r, L):
    m, b = rand_line(r, L, int_slope=L < 2)
    xs = [m.denominator * k for k in (0, 1, 2, 3)] if L < 2 else [m.denominator * k for k in (1, 3, 4, 7)]
    ys = [m * x + b for x in xs]
    need(all(y.denominator == 1 for y in ys))
    ans = yeq(m, b)
    return P(f"Write an equation for the linear function in the table. {table_text(xs, ys)}", ans,
             [f"Slope = {N(ys[1] - ys[0])} ÷ {N(xs[1] - xs[0])} = {N(m)}.", f"y-intercept: {N(b)}.", ans],
             [yeq(ys[1] - ys[0], b) if ys[1] - ys[0] != m else yeq(m + 1, b), yeq(m, ys[0]) if ys[0] != b else yeq(m, b + 1), yeq(b, m) if b != m else yeq(-m, b)],
             chk_py("rule_fits", pts=[[N(x), N(y)] for x, y in zip(xs, ys)]), tags=["multiple-representations"])


@fam("012")
def s7_context_table(r, L):
    base, rate = r.randint(5, 40), r.randint(2, 12)
    hrs = [1, 2, 4, 5] if L else [0, 1, 2, 3]
    ys = [base + rate * h for h in hrs]
    q = pick(r, ["rate", "start", "predict"])
    tbl = table_text(hrs, ys, "hours h", "cost C ($)")
    if q == "rate":
        return P(f"A kayak rental's cost is linear in time. {tbl}. What is the hourly rate?", f"${rate} per hour",
                 [f"({ys[1]} - {ys[0]}) ÷ ({hrs[1]} - {hrs[0]}) = {rate}."], [f"${ys[0]} per hour", f"${base} per hour", f"${N(F(ys[-1], hrs[-1]))} per hour"],
                 chk_val(f"({ys[1]} - {ys[0]})/({hrs[1]} - {hrs[0]})"), tags=["modeling"])
    if q == "start":
        return P(f"A kayak rental's cost is linear in time. {tbl}. What is the fixed fee (the cost for 0 hours)?", f"${base}",
                 [f"Rate: {rate} per hour.", f"Fee = {ys[0]} - {rate}({hrs[0]}) = {base}."], [f"${ys[0]}", f"${rate}", f"${base + rate}"],
                 chk_py("intercept_of", pts=[[hrs[0], ys[0]], [hrs[1], ys[1]]]), tags=["modeling"])
    h = r.randint(6, 12)
    return P(f"A kayak rental's cost is linear in time. {tbl}. Predict the cost for {h} hours.", f"${base + rate * h}",
             [f"C = {rate}h + {base}.", f"C = {rate}({h}) + {base} = {base + rate * h}."], [f"${rate * h}", f"${ys[-1] + rate}", f"${N(F(ys[-1] * h, hrs[-1]))}" if F(ys[-1] * h, hrs[-1]) != base + rate * h else f"${base + rate * h + rate}"],
             chk_py("predict_linear", pts=[[hrs[0], ys[0]], [hrs[1], ys[1]]], x=h), tags=["modeling"])


@fam("2", mode="mc")
def s7_which_table(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    xs = [-1, 0, 2, 3]
    good = [m * x + b for x in xs]
    bads = [[m * x + b + (1 if i == 2 else 0) for i, x in enumerate(xs)], [m * x + b for x in [-1, 0, 1, 2]], [-m * x + b for x in xs]]
    opts = [(table_text(xs, good), True)] + [(table_text(xs, bb), False) for bb in bads]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return P(f"Which table represents y = {mx_b(m, b)}?", table_text(xs, good), ["Substitute each x into the equation; every pair must match.", "Watch for x-values that skip (2 to 3 vs 0 to 2)."],
             options=opts, chk=chk_py("table_matches", eq=f"y = {mx_b(m, b)}"), tags=["multiple-representations", "misconception"], mode="mc")


@fam("012")
def s7_error(r, L):
    m, b = nz(r, 2, 5), r.randint(1, 9)
    xs = [0, 2, 4, 6]
    ys = [m * x + b for x in xs]
    step = ys[1] - ys[0]
    return P(f"Kira said the rule for this table is y = {step}x + {b} because y goes up by {step} each time. {table_text(xs, ys)}. What is the correct rule?", f"y = {m}x + {b}",
             [f"y increases by {step} when x increases by 2, so the rate is {step} ÷ 2 = {m}.", f"y = {m}x + {b}."], [f"y = {step}x + {b}", f"y = {m}x + {step}", f"y = {b}x + {m}"],
             chk_py("rule_fits", pts=[[x, y] for x, y in zip(xs, ys)]), tags=["error-analysis", "misconception"])


@fam("012")
def s7_select(r, L):
    m, b = rand_line(r, 1, int_slope=True)
    pts_ = [(x, m * x + b) for x in r.sample(range(-6, 9), 6)]
    opts = [(pt(*p), True) for p in pts_[:3]] + [(pt(p[0], p[1] + nz(r, -2, 2)), False) for p in pts_[3:]]
    xs = [-1, 0, 1, 2]
    return P(f"A linear function has this table: {table_text(xs, [m * x + b for x in xs])}. Select ALL ordered pairs that also belong to the function.", None,
             [f"The rule is y = {mx_b(m, b)}."], options=opts, chk=chk_py("on_graph", eq=f"y = {mx_b(m, b)}"), tags=["reasoning"])


@fam("012")
def s7_open(r, L):
    m, b = r.randint(2, 6), r.randint(10, 30)
    xs = [0, 1, 2, 3]
    return P(f"A plant is {b} cm tall and grows {m} cm per week.", None, ["Start + rate × weeks.", "Substitute.", "Rule.", "Solve."],
             parts=[("Complete the height for weeks 0, 1, 2, 3 (list).", ", ".join(str(b + m * x) for x in xs), {"kind": "text", "accept": [", ".join(str(b + m * x) for x in xs)]}),
                    ("What is the height after 10 weeks?", f"{b + 10 * m} cm", chk_val(f"{b} + {m}*10")),
                    ("Write a rule for height h after w weeks.", f"h = {m}w + {b}", {"kind": "equiv", "expr": f"{m}w + {b}", "vars": ["w"]}),
                    (f"After how many weeks is the plant {b + 13 * m} cm tall?", "13", {"kind": "eq", "eq": f"{m}w + {b} = {b + 13 * m}", "var": "w"})], tags=["modeling"])


# ======================================================================= S8 Increasing/decreasing/max/min
def pw_points(r, n=5, lo=-7, hi=7):
    xs = sorted(r.sample(range(-7, 8), n))
    ys = [r.randint(-6, 6) for _ in xs]
    for i in range(1, n):
        if ys[i] == ys[i - 1] and r.random() < 0.6:
            ys[i] += pick(r, [-2, 2])
    return list(zip(xs, ys))


def pw_desc(pts_):
    return ", ".join(pt(*p) for p in pts_)


@fam("012")
def s8_interval(r, L):
    pts_ = pw_points(r, 4 if L == 0 else 5)
    segs = [(a, b) for a, b in zip(pts_, pts_[1:])]
    kind = pick(r, ["increasing", "decreasing", "constant"] if L else ["increasing", "decreasing"])
    want = [s for s in segs if (s[1][1] > s[0][1] if kind == "increasing" else s[1][1] < s[0][1] if kind == "decreasing" else s[1][1] == s[0][1])]
    need(len(want) == 1)
    s = want[0]
    ans = f"from x = {s[0][0]} to x = {s[1][0]}"
    others = [f"from x = {t[0][0]} to x = {t[1][0]}" for t in segs if t != s]
    drw = plane_draw(polys=[(pts_, None)], points=[(x, y, None) for x, y in pts_])
    return P(f"The graph shows a function made of line segments. Over which interval is the function {kind}?", ans,
             ["Read the graph from left to right.", f"{kind.capitalize()}: the graph {'rises' if kind == 'increasing' else 'falls' if kind == 'decreasing' else 'stays level'} from x = {s[0][0]} to x = {s[1][0]}."],
             others + [f"from y = {s[0][1]} to y = {s[1][1]}"], chk_py("pw_interval", pts=[list(p) for p in pts_], seg=kind),
             diagram={"draw": drw, "alt": "Segments connecting " + pw_desc(pts_) + "."}, tags=["graph"])


@fam("012")
def s8_maxmin(r, L):
    pts_ = pw_points(r, 5)
    ys = [y for _, y in pts_]
    which = pick(r, ["maximum", "minimum"])
    tgt = max(ys) if which == "maximum" else min(ys)
    need(ys.count(tgt) == 1)
    p = pts_[ys.index(tgt)]
    q = pick(r, ["value", "x"]) if L else "value"
    drw = plane_draw(polys=[(pts_, None)], points=[(x, y, None) for x, y in pts_])
    if q == "value":
        return P(f"The graph shows a function on the interval from x = {pts_[0][0]} to x = {pts_[-1][0]}. What is the {which} value of the function?", str(tgt),
                 [f"The {'highest' if which == 'maximum' else 'lowest'} point is {pt(*p)}.", f"The {which} value is the y-coordinate: {tgt}."],
                 [str(p[0]), str(max(ys) if which == "minimum" else min(ys)), str(tgt + 1)], chk_py("pw_extreme", pts=[list(x) for x in pts_], which=which, q="value"),
                 diagram={"draw": drw, "alt": "Segments connecting " + pw_desc(pts_) + ", with endpoints at the first and last points."}, tags=["graph", "misconception"])
    return P(f"The graph shows a function on the interval from x = {pts_[0][0]} to x = {pts_[-1][0]}. At what x-value does the {which} occur?", f"x = {p[0]}",
             [f"The {'highest' if which == 'maximum' else 'lowest'} point is {pt(*p)}.", f"It occurs at x = {p[0]}."],
             [f"x = {tgt}", f"x = {pts_[[y for _, y in pts_].index(max(ys) if which == 'minimum' else min(ys))][0]}", f"x = {p[0] + 1}"],
             chk_py("pw_extreme", pts=[list(x) for x in pts_], which=which, q="x"), diagram={"draw": drw, "alt": "Segments connecting " + pw_desc(pts_) + "."}, tags=["graph"])


@fam("012", mode="sa")
def s8_linear_trend(r, L):
    m, b = rand_line(r, L, int_slope=False)
    form = pick(r, ["eq", "table"]) if L else "eq"
    if form == "eq":
        s = f"y = {mx_b(m, b)}"
    else:
        xs = [m.denominator * k for k in (-1, 0, 1, 2)]
        s = "the function in the table " + table_text(xs, [m * x + b for x in xs])
    ans = "increasing" if m > 0 else "decreasing" if m < 0 else "constant"
    return P(f"Is {s} increasing, decreasing, or constant?", ans, [f"The rate of change is {N(m)}.", "Positive rate → increasing; negative → decreasing; zero → constant."],
             [t for t in ["increasing", "decreasing", "constant"] if t != ans], chk_py("trend_of", m=N(m)), tags=["reasoning"], mode="sa")


@fam("12")
def s8_context(r, L):
    h0, peak, tpk, tend = r.randint(0, 5), r.randint(20, 60), r.randint(2, 6), r.randint(8, 14)
    pts_ = [(0, h0), (tpk, peak), (tend, 0)]
    drw = plane_draw(xr=(0, 15), yr=(0, 70), polys=[(pts_, None)], data=True, xstep=1, ystep=10, xlabel="time (seconds)", ylabel="height (feet)")
    q = pick(r, ["inc", "max"])
    if q == "inc":
        return P("The graph shows the height of a model rocket over time. During which time interval is the height increasing?", f"from 0 to {tpk} seconds",
                 [f"The graph rises from (0, {h0}) to ({tpk}, {peak}), then falls."], [f"from {tpk} to {tend} seconds", f"from 0 to {tend} seconds", f"from {h0} to {peak} seconds"],
                 chk_py("pw_interval_ctx", pts=[list(p) for p in pts_], seg="increasing", unit="seconds"), diagram={"draw": drw, "alt": f"Height rises in a straight segment from (0, {h0}) to ({tpk}, {peak}), then falls to ({tend}, 0)."},
                 tags=["graph", "modeling"])
    return P("The graph shows the height of a model rocket over time. What is the maximum height, and when does it occur?", f"{peak} feet at {tpk} seconds",
             [f"The highest point is ({tpk}, {peak})."], [f"{tpk} feet at {peak} seconds", f"{peak} feet at {tend} seconds", f"{h0} feet at 0 seconds"],
             chk_py("max_ctx", pts=[list(p) for p in pts_]), diagram={"draw": drw, "alt": f"Height rises from (0, {h0}) to ({tpk}, {peak}), then falls to ({tend}, 0)."}, tags=["graph", "modeling"])


@fam("012")
def s8_error(r, L):
    pts_ = [(-6, r.randint(-5, -1)), (-2, r.randint(2, 6)), (3, r.randint(-6, -1)), (6, r.randint(0, 5))]
    need(pts_[1][1] != pts_[3][1])
    drw = plane_draw(polys=[(pts_, None)], points=[(x, y, None) for x, y in pts_])
    opts = [(f"No. The function decreases from x = -2 to x = 3 because the graph falls there.", True), ("Yes. The y-values in that interval are negative.", False),
            ("Yes. The graph is below the x-axis at x = 3.", False), ("No. The function is constant there.", False)]
    r.shuffle(opts)
    return P("Jay says the function is increasing from x = -2 to x = 3 because the graph \"goes to the right.\" Is Jay correct?", "No. The function decreases from x = -2 to x = 3 because the graph falls there.",
             ["Increasing and decreasing describe the y-values as x moves right.", f"From {pt(*pts_[1])} to {pt(*pts_[2])} the y-values drop, so it is decreasing."],
             options=opts, chk=chk_py("pw_claim", pts=[list(p) for p in pts_], a=-2, b=3), diagram={"draw": drw, "alt": "Segments connecting " + pw_desc(pts_) + "."},
             tags=["error-analysis", "misconception", "graph"], mode="mc")


@fam("012")
def s8_select(r, L):
    pts_ = pw_points(r, 5)
    segs = list(zip(pts_, pts_[1:]))
    kinds = ["increasing" if b[1] > a[1] else "decreasing" if b[1] < a[1] else "constant" for a, b in segs]
    want = "increasing" if kinds.count("increasing") >= 2 else "decreasing"
    need(kinds.count(want) >= 2 and len(kinds) - kinds.count(want) >= 1)
    opts = [(f"from x = {a[0]} to x = {b[0]}", k == want) for (a, b), k in zip(segs, kinds)]
    drw = plane_draw(polys=[(pts_, None)], points=[(x, y, None) for x, y in pts_])
    return P(f"Select ALL intervals on which the graphed function is {want}.", None, [f"{o[0]}: {k}." for o, k in zip(opts, kinds)], options=opts,
             chk=chk_py("pw_interval", pts=[list(p) for p in pts_], seg=want), diagram={"draw": drw, "alt": "Segments connecting " + pw_desc(pts_) + "."}, tags=["graph"])


@fam("012")
def s8_open(r, L):
    pts_ = pw_points(r, 4)
    ys = [y for _, y in pts_]
    need(ys.count(max(ys)) == 1 and ys.count(min(ys)) == 1)
    segs = list(zip(pts_, pts_[1:]))
    inc = [s for s in segs if s[1][1] > s[0][1]]
    need(len(inc) == 1)
    drw = plane_draw(polys=[(pts_, None)], points=[(x, y, None) for x, y in pts_])
    s = inc[0]
    return P("Use the graph of the function.", None, ["Highest point.", "Lowest point.", "Rising segment.", "Read the endpoint."],
             parts=[("What is the maximum value?", str(max(ys)), chk_py("pw_extreme", pts=[list(p) for p in pts_], which="maximum", q="value")),
                    ("What is the minimum value?", str(min(ys)), chk_py("pw_extreme", pts=[list(p) for p in pts_], which="minimum", q="value")),
                    ("Over which interval is it increasing?", f"from x = {s[0][0]} to x = {s[1][0]}", chk_py("pw_interval", pts=[list(p) for p in pts_], seg="increasing")),
                    (f"What is f({pts_[-1][0]})?", str(pts_[-1][1]), chk_py("read_value", f=("pw", [list(p) for p in pts_]), x=pts_[-1][0]))],
             diagram={"draw": drw, "alt": "Segments connecting " + pw_desc(pts_) + "."}, tags=["graph"])


# ======================================================================= S9 Interpreting rates of change
CTX = [("A car's distance d (miles) after t hours", "miles per hour", "d", "t"), ("The cost C (dollars) of n pounds of apples", "dollars per pound", "C", "n"),
       ("The water level w (inches) in a pool after h hours of filling", "inches per hour", "w", "h"), ("A runner's distance d (meters) after s seconds", "meters per second", "d", "s"),
       ("The amount A (dollars) left on a gift card after b drinks", "dollars per drink", "A", "b")]


@fam("012")
def s9_meaning(r, L):
    c = pick(r, CTX)
    m = F(r.randint(2, 60)) if c[0][2] != "A" else F(-r.randint(3, 6))
    b = F(r.randint(0, 50)) if c[3] != "b" else F(r.randint(20, 50))
    eq = f"{c[2]} = {mx_b(m, b, c[3])}"
    q = pick(r, ["rate", "start"]) if L else "rate"
    if q == "rate":
        ans = f"{N(m)} {c[1]}"
        return P(f"{c[0]} is modeled by {eq}. What is the rate of change, with units?", ans, [f"The coefficient of {c[3]} is the rate of change: {N(m)} {c[1]}."],
                 [f"{N(b)} {c[1]}", f"{N(m + b)} {c[1]}", f"{N(-m)} {c[1]}"], chk_py("rate_with_units", m=N(m), units=c[1]), tags=["modeling"])
    return P(f"{c[0]} is modeled by {eq}. What does the number {N(b)} represent?", f"the value of {c[2]} when {c[3]} = 0",
             [f"{N(b)} is the constant term: the starting value of {c[2]} when {c[3]} = 0."], [f"the change in {c[2]} for each 1 unit of {c[3]}", f"the value of {c[3]} when {c[2]} = 0", f"the total change in {c[2]}"],
             {"kind": "text", "accept": [f"the value of {c[2]} when {c[3]} = 0"]}, tags=["modeling"])


@fam("012", mode="mc")
def s9_compare(r, L):
    m1, m2 = r.randint(3, 20), r.randint(3, 20)
    need(m1 != m2)
    b1 = r.randint(0, 20)
    hrs = [1, 2, 3]
    tbl = table_text(hrs, [m2 * h + r.randint(0, 0) for h in hrs], "hours", "pages")
    nm1, nm2 = pick(r, NAMES, 2)
    good = nm1 if m1 > m2 else nm2
    opts = [(nm1, good == nm1), (nm2, good == nm2), ("They read at the same rate", False), ("Cannot be determined", False)]
    return P(f"{nm1}'s reading is modeled by p = {m1}h + {b1} (pages after h hours). {nm2}'s reading: {tbl}. Who reads at the faster rate?", good,
             [f"{nm1}: {m1} pages per hour.", f"{nm2}: ({m2 * 2} - {m2}) ÷ 1 = {m2} pages per hour.", f"{good} is faster."],
             options=opts, chk=chk_py("faster_rate", A=[nm1, m1], B=[nm2, [[h, m2 * h] for h in hrs]]), tags=["multiple-representations"], mode="mc")


@fam("012")
def s9_from_two(r, L):
    t1, t2 = r.randint(1, 4), r.randint(5, 10)
    m = F(r.randint(5, 60), pick(r, [1, 2]))
    b = r.randint(10, 100)
    v1, v2 = b + m * t1, b + m * t2
    need(v1.denominator == 1 and v2.denominator == 1)
    obj = pick(r, [("A delivery truck's odometer read", "miles", "hours"), ("A savings account held $", "dollars", "weeks")])
    if obj[1] == "miles":
        p = f"A delivery truck had traveled {N(v1)} miles after {t1} hours and {N(v2)} miles after {t2} hours, at a constant speed. Find the speed in miles per hour."
    else:
        p = f"A savings account held ${N(v1)} after {t1} weeks and ${N(v2)} after {t2} weeks, growing by the same amount each week. Find the rate in dollars per week."
    return P(p, f"{N(m)} {obj[1]} per {obj[2][:-1]}", [f"Rate = ({N(v2)} - {N(v1)}) ÷ ({t2} - {t1}) = {N(m)}."],
             [f"{N(F(v2, t2))} {obj[1]} per {obj[2][:-1]}", f"{N(v2 - v1)} {obj[1]} per {obj[2][:-1]}", f"{N(F(v1, t1))} {obj[1]} per {obj[2][:-1]}"],
             chk_val(f"({N(v2)} - {N(v1)})/({t2} - {t1})"), tags=["modeling", "misconception"])


@fam("2")
def s9_graph_rate(r, L):
    m = F(r.randint(2, 9) * 5)
    b = F(r.randint(0, 4) * 10)
    tmax = 6
    drw = plane_draw(xr=(0, tmax), yr=(0, float(b + m * tmax) + 10), lines=[(m, b)], data=True, xstep=1, ystep=float(max(10, (b + m * tmax) // 6 // 10 * 10)),
                     xlabel="time (minutes)", ylabel="water (liters)", points=[(2, b + 2 * m, pt(2, b + 2 * m)), (4, b + 4 * m, pt(4, b + 4 * m))])
    return P("The graph shows the amount of water in a tank as it fills. At what rate is the tank filling, in liters per minute?", f"{N(m)} liters per minute",
             [f"Use the marked points (2, {N(b + 2 * m)}) and (4, {N(b + 4 * m)}).", f"({N(b + 4 * m)} - {N(b + 2 * m)}) ÷ (4 - 2) = {N(m)}."],
             [f"{N(b + 2 * m)} liters per minute", f"{N(F(b + 4 * m, 4))} liters per minute", f"{N(b)} liters per minute"], chk_py("slope_of", pts=[[2, N(b + 2 * m)], [4, N(b + 4 * m)]]),
             diagram={"draw": drw, "alt": f"Line from (0, {N(b)}) rising; marked points (2, {N(b + 2 * m)}) and (4, {N(b + 4 * m)})."}, tags=["graph", "modeling"])


@fam("012")
def s9_error(r, L):
    m, b = r.randint(15, 40), r.randint(20, 60)
    t = r.randint(3, 6)
    return P(f"A scooter rental costs C = {m}m + {b} cents for m minutes. Pia says the rate is {N(F(m * t + b, t))} cents per minute because a {t}-minute ride costs {m * t + b} cents. What is the actual rate?",
             f"{m} cents per minute", [f"Pia divided the total cost by time, which includes the {b}-cent starting fee.", f"The rate of change is the coefficient of m: {m} cents per minute."],
             [f"{N(F(m * t + b, t))} cents per minute", f"{b} cents per minute", f"{m + b} cents per minute"], chk_py("rate_with_units", m=str(m), units="cents per minute"),
             tags=["error-analysis", "misconception"])


@fam("012")
def s9_select(r, L):
    m, b = r.randint(2, 9), r.randint(10, 40)
    stm = [(f"The car wash earns ${m} for each car.", True), (f"The car wash started the day with ${b} in the register.", True), (f"After 10 cars, there is ${b + 10 * m}.", True),
           (f"The car wash earns ${b} for each car.", False), (f"After 10 cars, there is ${10 * (m + b)}.", False), (f"The amount decreases by ${m} per car.", False)]
    return P(f"The money M (dollars) in a car wash's register after c cars is M = {m}c + {b}. Select ALL true statements.", None,
             [f"Rate {m} dollars per car; starting amount {b}; M(10) = {b + 10 * m}."], options=stm, chk=chk_py("register_stmt", m=m, b=b), tags=["modeling"])


@fam("012")
def s9_open(r, L):
    m, b = r.randint(3, 9), r.randint(20, 80)
    return P(f"A candle is {b} mm tall and burns down at {m} mm per hour.", None, ["Negative rate.", "Starting value.", "Equation.", "Solve h = 0."],
             parts=[("What is the rate of change (include the sign)?", f"-{m} mm per hour", chk_py("rate_with_units", m=str(-m), units="mm per hour")),
                    ("What is the initial height?", f"{b} mm", chk_val(str(b))), ("Write an equation for the height h after t hours.", f"h = {b} - {m}t", {"kind": "equiv", "expr": f"{b} - {m}t", "vars": ["t"]}),
                    ("After how many hours does the candle burn out? (Round to the nearest tenth if needed.)", Rd(F(b, m), 1) if F(b, m).denominator != 1 else str(b // m), {"kind": "approx", "expr": f"{b}/{m}", "places": 1} if F(b, m).denominator != 1 else chk_val(f"{b}/{m}"))],
             tags=["modeling"])


# ======================================================================= S10 Interpreting functions in context
STORIES = [("walks away from home at a steady pace, stops to talk with a friend, then walks home quickly", [(0, 0), (4, 4), (6, 4), (8, 0)], "distance from home"),
           ("walks to a friend's house, waits there, then both walk farther away slowly", [(0, 0), (3, 5), (6, 5), (10, 7)], "distance from home"),
           ("starts at a park far from home and walks steadily toward home until arriving", [(0, 8), (8, 0)], "distance from home"),
           ("runs away from home, slows to a walk while still moving away, then stops", [(0, 0), (2, 5), (6, 7), (10, 7)], "distance from home"),
           ("leaves home, returns home to get a forgotten bag, then leaves again", [(0, 0), (3, 4), (5, 0), (9, 6)], "distance from home"),
           ("rides away from home, then rides back slowly part of the way, then stops", [(0, 0), (3, 6), (7, 2), (10, 2)], "distance from home"),
           ("stands still at a bus stop, then rides the bus away quickly", [(0, 2), (4, 2), (7, 8)], "distance from home"),
           ("jogs away from home at a constant speed the whole time", [(0, 0), (10, 8)], "distance from home")]


@fam("012", mode="mc")
def s10_match_story(r, L):
    idx = r.sample(range(len(STORIES)), 4)
    k = pick(r, idx)
    nm = pick(r, NAMES)
    drawers = [plane_draw(xr=(0, 10), yr=(0, 9), polys=[(STORIES[i][1], None)], data=True, xstep=2, ystep=2, xlabel="time (min)", ylabel="distance (blocks)") for i in idx]
    good = "ABCD"[idx.index(k)]
    alt = "Four distance-time graphs: " + "; ".join(f"Graph {l}: segments through " + ", ".join(pt(*p) for p in STORIES[i][1]) for l, i in zip("ABCD", idx))
    return P(f"{nm} {STORIES[k][0]}. Which graph shows {nm}'s distance from home over time?", f"Graph {good}",
             ["Rising: moving away. Flat: stopped. Falling: returning. Steeper means faster."], options=[(f"Graph {l}", l == good) for l in "ABCD"],
             chk=chk_py("story_graph", order=idx, k=k), diagram={"draw": panels_draw(drawers), "alt": alt}, tags=["graph", "modeling"], mode="mc")


@fam("012")
def s10_interpret_value(r, L):
    m, b = r.randint(20, 60), r.randint(50, 300)
    x0 = r.randint(2, 9)
    v = m * x0 + b
    ctx = pick(r, [("C(n)", "the cost, in dollars, of a field trip for n students", "students", "dollars"), ("D(t)", "the distance, in miles, a train is from the station after t hours", "hours", "miles")])
    f = ctx[0][0]
    var = ctx[0][2]
    return P(f"{ctx[0]} = {m}{var} + {b} gives {ctx[1]}. What does {f}({x0}) = {v} mean?",
             f"For {x0} {ctx[2]}, the value is {v} {ctx[3]}.", [f"The input {x0} is the number of {ctx[2]}; the output {v} is in {ctx[3]}."],
             [f"For {v} {ctx[2]}, the value is {x0} {ctx[3]}.", f"The rate is {v} {ctx[3]} per {ctx[2][:-1]}.", f"For {x0} {ctx[2]}, the value is {m} {ctx[3]}."],
             chk_py("io_statement", x=x0, y=v, xu=ctx[2], yu=ctx[3], rule=[m, b]), tags=["modeling"])


@fam("012")
def s10_read_context(r, L):
    pts_ = [(0, 0), (2, r.randint(2, 5) * 10), (5, 0)]
    pts_[2] = (r.randint(5, 8), pts_[1][1])
    pts_.append((pts_[2][0] + r.randint(2, 4), 0))
    drw = plane_draw(xr=(0, 13), yr=(0, 60), polys=[(pts_, None)], data=True, xstep=1, ystep=10, xlabel="time (hours)", ylabel="distance from camp (km)")
    q = pick(r, ["stopped", "far", "back"])
    if q == "stopped":
        ans = f"{pts_[2][0] - pts_[1][0]} hours"
        return P("The graph shows a hiker's distance from camp. For how long did the hiker stay in one place?", ans, [f"The graph is flat from t = {pts_[1][0]} to t = {pts_[2][0]}."],
                 [f"{pts_[1][0]} hours", f"{pts_[3][0]} hours", f"{pts_[1][1]} hours"], chk_py("flat_duration", pts=[list(p) for p in pts_]),
                 diagram={"draw": drw, "alt": "Distance from camp: segments through " + pw_desc(pts_) + "."}, tags=["graph", "modeling"])
    if q == "far":
        return P("The graph shows a hiker's distance from camp. What was the hiker's greatest distance from camp?", f"{pts_[1][1]} km", ["Read the highest point of the graph."],
                 [f"{pts_[2][0]} km", f"{pts_[3][0]} km", f"{pts_[1][1] // 2} km"], chk_py("pw_extreme", pts=[list(p) for p in pts_], which="maximum", q="value"),
                 diagram={"draw": drw, "alt": "Distance from camp: segments through " + pw_desc(pts_) + "."}, tags=["graph", "modeling"])
    sp = F(pts_[1][1], pts_[3][0] - pts_[2][0])
    return P("The graph shows a hiker's distance from camp. What was the hiker's speed returning to camp, in km per hour?", f"{N(sp)} km per hour",
             [f"Return: {pts_[1][1]} km in {pts_[3][0] - pts_[2][0]} hours.", f"{pts_[1][1]} ÷ {pts_[3][0] - pts_[2][0]} = {N(sp)}."],
             [f"{N(F(pts_[1][1], pts_[1][0]))} km per hour" if F(pts_[1][1], pts_[1][0]) != sp else f"{N(sp + 1)} km per hour", f"{N(F(pts_[1][1], pts_[3][0]))} km per hour", f"{pts_[1][1]} km per hour"],
             chk_py("slope_of", pts=[[pts_[2][0], -pts_[1][1]], [pts_[3][0], 0]]), diagram={"draw": drw, "alt": "Distance from camp: segments through " + pw_desc(pts_) + "."}, tags=["graph", "modeling"])


@fam("2")
def s10_domain_context(r, L):
    m = r.randint(5, 15)
    cap = m * r.randint(4, 10)
    return P(f"A bucket holds {cap} liters. It fills at {m} liters per minute: V = {m}t. For what times t does the model make sense? Give the greatest t.", f"t = {cap // m} minutes",
             [f"The volume cannot exceed {cap} liters: {m}t ≤ {cap}.", f"t ≤ {cap // m}; also t ≥ 0."], [f"t = {cap} minutes", f"t = {cap * m} minutes", f"t = {cap // m + 1} minutes"],
             {"kind": "eq", "eq": f"{m}t = {cap}", "var": "t"}, tags=["modeling", "reasoning"])


@fam("012")
def s10_error(r, L):
    pts_ = [(0, 0), (3, 6), (6, 6), (8, 0)]
    drw = plane_draw(xr=(0, 10), yr=(0, 8), polys=[(pts_, None)], data=True, xstep=1, ystep=1, xlabel="time (min)", ylabel="speed (m per s)")
    opts = [("No. Speed stays at 6 m per s from 3 to 6 minutes, so the cyclist is still moving.", True), ("Yes. A flat graph always means stopped.", False),
            ("Yes. The speed is 0 from 3 to 6 minutes.", False), ("No. The cyclist is moving backward.", False)]
    r.shuffle(opts)
    return P("The graph shows a cyclist's SPEED over time. Ren says the flat part means the cyclist was stopped. Is Ren correct?", opts[[c for _, c in opts].index(True)][0],
             ["Read the vertical axis label: it is speed, not distance.", "A flat speed graph at 6 means constant speed 6, not stopped."],
             options=opts, chk={"kind": "text", "accept": ["No. Speed stays at 6 m per s from 3 to 6 minutes, so the cyclist is still moving."]},
             diagram={"draw": drw, "alt": "Speed (m per s) vs time (min): rises from (0, 0) to (3, 6), flat to (6, 6), falls to (8, 0)."}, tags=["error-analysis", "graph", "misconception"], mode="mc")


@fam("012")
def s10_select(r, L):
    a, b = r.randint(10, 30), r.randint(2, 6)
    stm = [(f"The pool starts with {a} cm of water.", True), (f"The water level rises {b} cm each hour.", True), (f"After 5 hours the level is {a + 5 * b} cm.", True),
           (f"The pool starts with {b} cm of water.", False), (f"After 5 hours the level is {5 * (a + b)} cm.", False), ("The water level is decreasing.", False)]
    return P(f"The water level L (cm) in a pool after h hours is L = {b}h + {a}. Select ALL true statements.", None, [f"Starting level {a}; rate {b} cm per hour."], options=stm,
             chk=chk_py("register_stmt2", m=b, b=a), tags=["modeling"])


@fam("012")
def s10_open(r, L):
    m, b = r.randint(2, 5), r.randint(10, 40)
    return P(f"A cell phone battery is at {b + 20 * m}% and drops {m}% each hour while streaming video.", None, ["Rate.", "Equation.", "Evaluate.", "Solve."],
             parts=[("What is the rate of change (include units)?", f"-{m}% per hour", {"kind": "text", "accept": [f"-{m}% per hour"]}),
                    ("Write an equation for the battery level B after h hours.", f"B = {b + 20 * m} - {m}h", {"kind": "equiv", "expr": f"{b + 20 * m} - {m}h", "vars": ["h"]}),
                    ("What is the level after 4 hours?", f"{b + 16 * m}%", chk_val(f"{b + 20 * m} - {m}*4")),
                    (f"After how many hours will the level be {b}%?", "20", {"kind": "eq", "eq": f"{b + 20 * m} - {m}h = {b}", "var": "h"})], tags=["modeling"])


# ======================================================================= S11 Sketching piecewise functions
@fam("012")
def s11_evaluate(r, L):
    c = r.randint(-2, 3)
    m1, b1, m2, b2 = nz(r, -3, 3), r.randint(-4, 4), nz(r, -3, 3), r.randint(-4, 4)
    rule = f"f(x) = {mx_b(m1, b1)} for x < {c}, and f(x) = {mx_b(m2, b2)} for x ≥ {c}"
    x0 = pick(r, [c - 2, c - 1, c, c + 1, c + 3])
    v = m1 * x0 + b1 if x0 < c else m2 * x0 + b2
    other = m2 * x0 + b2 if x0 < c else m1 * x0 + b1
    need(other != v)
    return P(f"A piecewise function is defined as {rule}. Find f({x0}).", str(v),
             [f"{x0} {'<' if x0 < c else '≥'} {c}, so use f(x) = {mx_b(m1, b1) if x0 < c else mx_b(m2, b2)}.", f"f({x0}) = {v}."],
             [str(other), str(v + 1), str(-v) if v else "1"], chk_py("piecewise_eval", pieces=[[N(m1), N(b1)], [N(m2), N(b2)]], c=c, x=x0), tags=["misconception"] if x0 == c else [])


@fam("012")
def s11_from_story(r, L):
    rate1, t1 = r.randint(2, 6), r.randint(2, 4)
    t2 = t1 + r.randint(1, 3)
    rate3 = r.randint(1, 4)
    t3 = t2 + r.randint(2, 4)
    v1 = rate1 * t1
    v3 = v1 + rate3 * (t3 - t2) if L else v1
    nm = pick(r, NAMES)
    pts_ = [(0, 0), (t1, v1), (t2, v1), (t3, v3)]
    q = pick(r, ["value", "seg"])
    story = f"{nm} fills a tank at {rate1} liters per minute for {t1} minutes, stops for {t2 - t1} minutes, then fills at {rate3} liters per minute for {t3 - t2} more minutes." if L else \
        f"{nm} fills a tank at {rate1} liters per minute for {t1} minutes, then stops for {t3 - t1} minutes."
    if not L:
        pts_ = [(0, 0), (t1, v1), (t3, v1)]
    if q == "value":
        return P(f"{story} A graph of liters vs. minutes is sketched. What are the coordinates of the last point of the sketch?", pt(*pts_[-1]),
                 [f"First piece ends at {pt(*pts_[1])}."] + ([f"Flat piece to {pt(*pts_[2])}; then rises {rate3 * (t3 - t2)} liters."] if L else ["Then it stays flat."]) + [f"End: {pt(*pts_[-1])}."],
                 [pt(pts_[-1][1], pts_[-1][0]), pt(pts_[-1][0], v1 + rate1 * (t3 - t2)) if L else pt(t3, rate1 * t3), pt(pts_[-1][0] - 1, pts_[-1][1])],
                 chk_py("story_endpoint", r=[[rate1, t1]] + ([[0, t2 - t1], [rate3, t3 - t2]] if L else [[0, t3 - t1]])), tags=["modeling"])
    return P(f"{story} How many line segments does the sketch of liters vs. minutes have, and which one is horizontal?",
             f"{len(pts_) - 1} segments; segment 2 is horizontal", ["Each change in rate starts a new segment; a rate of 0 is horizontal."],
             [f"{len(pts_)} segments; segment 2 is horizontal", f"{len(pts_) - 1} segments; segment 1 is horizontal", f"{len(pts_) - 1} segments; none are horizontal"],
             chk_py("story_segments", rates=[rate1, 0] + ([rate3] if L else [])), tags=["modeling"])


@fam("012")
def s11_graph_rule(r, L):
    c = r.randint(-2, 2)
    m1, m2 = nz(r, -2, 2), nz(r, -2, 2)
    b1 = r.randint(-3, 3)
    yc = m1 * c + b1
    b2 = yc - m2 * c
    pts_ = [(c - 4, m1 * (c - 4) + b1), (c, yc), (c + 4, m2 * (c + 4) + b2)]
    need(all(abs(y) <= 8 for _, y in pts_))
    drw = plane_draw(polys=[(pts_, None)], points=[(x, y, None) for x, y in pts_])
    which = pick(r, ["left", "right"])
    m, b = (m1, b1) if which == "left" else (m2, b2)
    return P(f"The graph is made of two line segments meeting at {pt(c, yc)}. Write the equation of the {'left' if which == 'left' else 'right'} piece in slope-intercept form.", yeq(m, b),
             [f"Use two points on the {which} piece.", f"slope {N(m)}, y-intercept {N(b)}: {yeq(m, b)}."], [yeq(m2 if which == 'left' else m1, b), yeq(-m, b), yeq(m, b + 1)],
             chk_py("line_through", pts=[[pts_[0][0], pts_[0][1]], [c, yc]] if which == "left" else [[c, yc], [pts_[2][0], pts_[2][1]]]),
             diagram={"draw": drw, "alt": "Two segments: from " + pt(*pts_[0]) + " to " + pt(*pts_[1]) + ", then to " + pt(*pts_[2]) + "."}, tags=["graph"])


@fam("2")
def s11_step(r, L):
    rate = r.randint(2, 6)
    hrs = F(r.randint(3, 15), 2)
    cost = rate * math.ceil(hrs)
    return P(f"A parking garage charges ${rate} for each hour or part of an hour. What is the cost for {D(hrs)} hours?", f"${cost}",
             [f"Any part of an hour counts as a full hour: {D(hrs)} hours is charged as {math.ceil(hrs)} hours.", f"{math.ceil(hrs)} × {rate} = {cost}."],
             [f"${D(rate * hrs)}", f"${rate * math.floor(hrs)}", f"${cost + rate}"], chk_py("step_cost", rate=rate, h=D(hrs)), tags=["modeling", "challenge"])


@fam("012")
def s11_error(r, L):
    c = r.randint(0, 3)
    rule = f"f(x) = 2x for x < {c}, and f(x) = x + 5 for x ≥ {c}"
    v = c + 5
    return P(f"Ben evaluated {rule} at x = {c} and got {2 * c} using the first piece. What is the correct value of f({c})?", str(v),
             [f"x = {c} is not less than {c}; it belongs to the piece x ≥ {c}.", f"f({c}) = {c} + 5 = {v}."], [str(2 * c), str(2 * c + 5), str(c)],
             chk_py("piecewise_eval", pieces=[["2", "0"], ["1", "5"]], c=c, x=c), tags=["error-analysis", "misconception"])


@fam("012")
def s11_select(r, L):
    c = r.randint(-1, 2)
    m1, b1, m2, b2 = 1, r.randint(0, 3), -1, r.randint(4, 8)
    f = lambda x: m1 * x + b1 if x < c else m2 * x + b2
    xs = r.sample(range(-4, 6), 6)
    opts = []
    for i, x in enumerate(xs):
        y = f(x) if i < 3 else f(x) + nz(r, -2, 2)
        opts.append((pt(x, y), i < 3))
    return P(f"For f(x) = x + {b1} when x < {c} and f(x) = -x + {b2} when x ≥ {c}, select ALL points on the graph.", None, ["Use the piece whose condition the x-value satisfies."],
             options=opts, chk=chk_py("piecewise_point", pieces=[["1", str(b1)], ["-1", str(b2)]], c=c), tags=["reasoning"])


@fam("012")
def s11_open(r, L):
    a, t1, t2 = r.randint(2, 5), r.randint(2, 4), r.randint(5, 8)
    return P(f"A walker leaves home at {a} km per hour for {t1} hours, rests until hour {t2}, then walks home at {a} km per hour.", None,
             ["Distance at end of first piece.", "Flat piece.", "Return time.", "Number of pieces."],
             parts=[(f"How far from home is the walker at hour {t1}?", f"{a * t1} km", chk_val(f"{a}*{t1}")), (f"How far from home at hour {t2}?", f"{a * t1} km", chk_val(f"{a}*{t1}")),
                    ("At what hour does the walker arrive home?", str(t2 + t1), chk_val(f"{t2} + {a * t1}/{a}")),
                    ("How many line segments does the sketch of distance vs. time have?", "3", chk_val("3"))], tags=["modeling"])


SKILLS = {
    1: dict(name="Introduction to functions and writing function rules", std=["8.F.A.1"], fams=[s1_is_function, s1_which_function, s1_rule_from_table, s1_evaluate, s1_verbal, s1_domain_range, s1_vertical_line],
            extra=[s1_select, s1_open]),
    2: dict(name="Graphing functions", std=["8.F.A.1"], fams=[s2_point_on, s2_table_value, s2_read_graph, s2_match_graph, s2_nonlinear_value], extra=[s2_select, s2_open]),
    3: dict(name="Distinguishing linear and nonlinear functions", std=["8.F.A.3"], fams=[s3_table, s3_equation, s3_graph, s3_context, s3_complete_linear], extra=[s3_select, s3_open]),
    4: dict(name="Exploring linear functions", std=["8.F.B.4", "8.EE.B.6"], fams=[s4_slope_points, s4_slope_table, s4_slope_graph, s4_slope_type, s4_missing_coord, s4_intercept],
            extra=[s4_error, s4_select, s4_open]),
    5: dict(name="Equations of linear functions", std=["8.F.B.4", "8.EE.B.6"], fams=[s5_slope_point, s5_two_points, s5_context, s5_standard_to_si, s5_parallel], extra=[s5_error, s5_select, s5_open]),
    6: dict(name="Graphs of linear functions", std=["8.F.A.3", "8.F.B.4"], fams=[s6_equation_from_graph, s6_intercepts, s6_compare, s6_which_graph, s6_translate], extra=[s6_error, s6_select, s6_open]),
    7: dict(name="Tables of linear functions", std=["8.F.B.4", "8.F.A.2"], fams=[s7_missing, s7_rule, s7_context_table, s7_which_table], extra=[s7_error, s7_select, s7_open]),
    8: dict(name="Increasing, decreasing, maximum, and minimum", std=["8.F.B.5"], fams=[s8_interval, s8_maxmin, s8_linear_trend, s8_context], extra=[s8_error, s8_select, s8_open]),
    9: dict(name="Interpreting rates of change", std=["8.F.B.4", "8.F.A.2"], fams=[s9_meaning, s9_compare, s9_from_two, s9_graph_rate], extra=[s9_error, s9_select, s9_open]),
    10: dict(name="Interpreting functions in context", std=["8.F.B.5", "8.F.B.4"], fams=[s10_match_story, s10_interpret_value, s10_read_context, s10_domain_context], extra=[s10_error, s10_select, s10_open]),
    11: dict(name="Sketching piecewise functions", std=["8.F.B.5"], fams=[s11_evaluate, s11_from_story, s11_graph_rule, s11_step], extra=[s11_error, s11_select, s11_open]),
}
