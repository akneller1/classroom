"""Algebra 2 Unit 2 — Linear Functions and Systems (linear-functions-systems). Top-up families."""
from hslib import *
import pc_u01 as F1
import pc_u02 as F2
import ca_u01 as CA1
import g7_u08 as L7

UNIT_ID = "linear-functions-systems"
ABBR = "ls"


def ri(r, a, b):
    return rint(r, a, b, True)


@fam("012")
def s2_slope_points(r, L):
    x1, x2 = r.sample(range(-9, 10), 2)
    y1, y2 = rint(r, -12, 12), rint(r, -12, 12)
    m = sp.Rational(y2 - y1, x2 - x1)
    if L == 0:
        need(m.q == 1)
    wr = [T(sp.Rational(x2 - x1, y2 - y1)) if y2 != y1 else "undefined", T(-m) if m else "1", T(sp.Rational(y2 + y1, x2 - x1)) if y1 else T(m + 1)]
    need(len(set(wr) | {T(m)}) == 4)
    return Q(f"Find the slope of the line through ({x1}, {y1}) and ({x2}, {y2}).", T(m),
             ["m = (y₂ - y₁)/(x₂ - x₁).", f"m = ({y2} - {par(y1)})/({x2} - {par(x1)}) = {T(sp.Integer(y2 - y1))}/{T(sp.Integer(x2 - x1))}.", f"m = {T(m)}."],
             wr, H(f"Rational({y2} - ({y1}), {x2} - ({x1}))"), why=["Divided the change in x by the change in y", "Subtracted the coordinates in different orders", "Added the y-values instead of subtracting"])


@fam("012")
def s2_rate(r, L):
    who = name(r)
    t1, t2 = sorted(r.sample(range(1, 13), 2))
    rate = ri(r, -9, 15) * (1 if L < 2 else pick(r, [1, 1, sp.Rational(1, 2)]))
    start = rint(r, 20, 400)
    y1, y2 = start + rate * t1, start + rate * t2
    need(y1 > 0 and y2 > 0 and (rate.q == 1 if hasattr(rate, "q") else True))
    unit, per = pick(r, [("gallons of water in a tank", "hour"), ("dollars in an account", "week"), ("feet of elevation", "minute"), ("pages read", "day")])
    v = sp.Rational(y2 - y1, t2 - t1)
    return Q(f"There are {T(y1)} {unit} after {t1} {per}s and {T(y2)} after {t2} {per}s. Assuming a constant rate, find the rate of change in {unit.split(' ')[0]} per {per}.", T(v),
             ["Rate of change = change in amount ÷ change in time.", f"({T(y2)} - {T(y1)}) ÷ ({t2} - {t1}) = {T(v)}.", f"The rate is {T(v)} {unit.split(' ')[0]} per {per}."],
             [T(sp.Rational(t2 - t1, y2 - y1)) if y2 != y1 else "0", T(sp.Rational(y2, t2)), T(y2 - y1)], H(f"Rational({T(y2)} - ({T(y1)}), {t2} - {t1})"),
             why=["Divided time by amount", "Divided one amount by its own time", "Forgot to divide by the change in time"], tags=["modeling"])


@fam("012")
def s3_table(r, L):
    m, b = ri(r, -8, 8) * (1 if L < 2 else pick(r, [1, sp.Rational(1, 2)])), rint(r, -15, 30)
    x0 = rint(r, 0, 3)
    step = pick(r, [1, 2, 3, 5])
    xs = [x0 + step * i for i in range(4)]
    ys = [m * v + b for v in xs]
    need(all(sp.sympify(v).is_Integer for v in ys))
    tbl = "; ".join(f"({a}, {T(c)})" for a, c in zip(xs, ys))
    ans = "y = " + T(m * x + b)
    wr = ["y = " + T(m * step * x + b), "y = " + T(m * x + ys[0]) if xs[0] else "y = " + T(m * x + b + m), "y = " + T(b * x + m)]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"The points {tbl} lie on a line. Write the equation of the line in slope-intercept form.", ans,
             [f"Slope: change in y ÷ change in x = {T(ys[1] - ys[0])} ÷ {step} = {T(m)}.", f"Use ({xs[0]}, {T(ys[0])}): {T(ys[0])} = {T(m)}({xs[0]}) + b, so b = {T(b)}.", f"{ans}."],
             wr, H(f"y - P('{T(m * x + b)}')", "eqn"),
             why=["Used the change in y per row as the slope without dividing by the x-step", "Used the first y-value as the y-intercept", "Switched the slope and the intercept"], tags=["modeling"])


@fam("012", mode="mc")
def s3_interpret(r, L):
    rate, start = rint(r, 2, 40), rint(r, 15, 300)
    ctx = pick(r, [("C", "the cost in dollars of a gym membership after m months", "m", "the monthly fee", "the sign-up fee"),
                   ("T", "the total pay in dollars for a tutor who works h hours", "h", "the hourly rate", "a fixed booking fee"),
                   ("D", "the distance in miles from home after t hours of driving", "t", "the speed in miles per hour", "the starting distance from home")])
    f, desc, v, slope_m, int_m = ctx
    part = pick(r, ["slope", "intercept"])
    ans = f"{rate}, {slope_m}" if part == "slope" else f"{start}, {int_m}"
    opts = [(ans, True), (f"{start}, {slope_m}" if part == "slope" else f"{rate}, {int_m}", False),
            (f"{rate}, {int_m}" if part == "slope" else f"{start}, {slope_m}", False), (f"{rate + start}, the total after one {('month' if v == 'm' else 'hour')}", False)]
    return Q(f"{f}({v}) = {rate}{v} + {start} gives {desc}. Which gives the {'slope' if part == 'slope' else 'y-intercept'} and its meaning?", ans,
             [f"In {f}({v}) = m{v} + b, m = {rate} is the rate of change and b = {start} is the starting value.", f"The {'slope' if part == 'slope' else 'y-intercept'} is {ans}."],
             options=opts, chk=H(f"'{ans}'", "text"), mode="mc", tags=["modeling"])


@fam("012")
def s5_elim(r, L):
    x0, y0 = rint(r, -7, 7), rint(r, -7, 7)
    while True:
        a1, b1, a2, b2 = [ri(r, -6, 6) for _ in range(4)]
        if a1 * b2 - a2 * b1 != 0 and (L or b1 == -b2 or a1 == -a2 or b1 == b2):
            break
    c1, c2 = a1 * x0 + b1 * y0, a2 * x0 + b2 * y0
    e1, e2 = f"{T(a1 * x + b1 * y)} = {c1}", f"{T(a2 * x + b2 * y)} = {c2}"
    ans = f"({x0}, {y0})"
    wr = [f"({y0}, {x0})", f"({-x0}, {y0})" if x0 else f"({x0}, {-y0})", f"({x0}, {-y0})" if y0 else f"({x0 + 1}, {y0})"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve the system by elimination: {e1} and {e2}.", ans,
             ["Multiply one or both equations so one variable has opposite coefficients.", "Add the equations to eliminate that variable and solve for the other.",
              "Substitute back to find the remaining variable.", f"The solution is {ans}."],
             wr, H(f"(lambda s: (s[x], s[y]))(solve([Eq(P('{T(a1 * x + b1 * y)}'), {c1}), Eq(P('{T(a2 * x + b2 * y)}'), {c2})], [x, y]))", "point"),
             why=["Switched the x- and y-values", "Made a sign error when eliminating", "Made a sign error when substituting back"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Linear equations in multiple forms", fams=[rr(F1.s1_two_points), rr(F1.s1_standard), rr(F2.s1_slope_std)],
            extra=[err_of(rr(F1.s1_two_points, tag="e")), err_of(rr(F1.s1_standard, tag="e")), open_of(rr(F1.s1_two_points, tag="o")), select_of(rr(F1.s1_standard, tag="s"))]),
    2: dict(name="Slope and rate of change", fams=[s2_slope_points, s2_rate, rr(CA1.s5_aroc)], extra=[err_of(s2_slope_points), err_of(s2_rate), open_of(s2_slope_points)]),
    3: dict(name="Writing linear models", fams=[s3_table, rr(F1.s1_context, (1, 1, 2)), s3_interpret], extra=[err_of(s3_table), err_of(rr(F1.s1_context, (1, 1, 2), "e")), open_of(s3_table)]),
    4: dict(name="Systems by graphing and substitution", fams=[rr(F1.s8_system), rr(F1.s8_context, (1, 1, 2)), rr(F1.s3_graph, (0, 0, 0))],
            extra=[err_of(rr(F1.s8_system, tag="e")), err_of(rr(F1.s3_graph, (0, 0, 0), "e")), open_of(rr(F1.s8_system, tag="o")), select_of(rr(F1.s8_system, tag="s"))]),
    5: dict(name="Systems by elimination", fams=[s5_elim, rr(F1.s9_three, (0, 0, 1))], extra=[err_of(s5_elim), err_of(rr(F1.s9_three, (0, 0, 1), "e")), open_of(s5_elim)]),
    6: dict(name="Linear inequalities and systems", fams=[rr(L7.s8_point, (1, 1, 2)), rr(L7.s8_which, (1, 1, 2)), rr(L7.s8_boundary, (1, 1, 2)), rr(F1.s10_test)],
            extra=[err_of(rr(L7.s8_point, (1, 1, 2), "e")), err_of(rr(F1.s10_test, tag="e")), open_of(rr(F1.s10_test, tag="o"))]),
    7: dict(name="Linear programming and applications", fams=[rr(F1.s11_lp), rr(F1.s10_vertex)], extra=[err_of(rr(F1.s11_lp, tag="e")), err_of(rr(F1.s10_vertex, tag="e")), open_of(rr(F1.s11_lp, tag="o"))]),
}
