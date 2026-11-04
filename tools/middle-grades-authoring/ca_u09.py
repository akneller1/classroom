"""Calculus Unit 9 — AP Review (ap-review). Mixed review built from the verified families of Units 2–8,
plus justification and notation items written for this unit."""
from hslib import *
import ca_u02 as C2
import ca_u03 as C3
import ca_u04 as C4
import ca_u05 as C5
import ca_u06 as C6
import ca_u07 as C7
import ca_u08 as C8

UNIT_ID = "ap-review"
ABBR = "apr"


def rr(f, lv=(0, 1, 2), tag="r"):
    g = reuse(f, lv, tag)
    g.__name__ = "cal_" + f.__name__ + tag
    return g


# ============================================================== Justifications
@fam("012", mode="mc")
def s6_justify(r, L):
    a, b = sorted(r.sample(range(-4, 8), 2))
    c = rint(r, a, b)
    k_ = rint(r, -5, 5)
    items = [
        (f"f is differentiable, f′({c}) = 0, and f′ changes from positive to negative at x = {c}. Which conclusion and justification is correct?",
         f"f has a relative maximum at x = {c} because f′ changes from positive to negative there",
         [f"f has a relative minimum at x = {c} because f′({c}) = 0", f"f has a relative maximum at x = {c} because f′({c}) = 0", f"f has an inflection point at x = {c} because f′ changes sign"]),
        (f"f is twice differentiable and f″ changes from negative to positive at x = {c}. Which conclusion is justified?",
         f"The graph of f has a point of inflection at x = {c} because f″ changes sign there",
         [f"f has a relative minimum at x = {c} because f″ changes sign", f"f has a point of inflection at x = {c} because f″({c}) = 0", f"f is increasing at x = {c} because f″ > 0 after it"]),
        (f"f is continuous on [{a}, {b}], f({a}) = {k_ - 3}, and f({b}) = {k_ + 4}. Which conclusion is justified?",
         f"f(x) = {k_} for some x in ({a}, {b}) by the Intermediate Value Theorem",
         [f"f′(x) = {k_} for some x in ({a}, {b}) by the Mean Value Theorem", f"f(x) = {k_} for some x in ({a}, {b}) by the Extreme Value Theorem", f"f has a zero in ({a}, {b}) because f is continuous"]),
        (f"f is differentiable on ({a}, {b}) and continuous on [{a}, {b}], with f({a}) = 2 and f({b}) = {2 + 3 * (b - a)}. Which conclusion is justified?",
         f"f′(c) = 3 for some c in ({a}, {b}) by the Mean Value Theorem",
         [f"f(c) = 3 for some c in ({a}, {b}) by the Intermediate Value Theorem", f"f′(c) = 0 for some c in ({a}, {b}) by Rolle's Theorem", f"f′(x) = 3 for every x in ({a}, {b})"]),
        (f"v(t) is a particle's velocity, v({c}) = -4, and a({c}) = -2. Is the particle speeding up at t = {c}?",
         "Yes, because velocity and acceleration have the same sign",
         ["No, because acceleration is negative", "No, because velocity is negative", "Yes, because acceleration is negative"]),
        (f"g(x) = ∫ from {a} to x f(t) dt and f({c}) > 0. What can be concluded about g at x = {c}?",
         f"g is increasing at x = {c} because g′({c}) = f({c}) > 0",
         [f"g is concave up at x = {c} because f({c}) > 0", f"g({c}) > 0 because f({c}) > 0", f"g has a maximum at x = {c}"])]
    qtxt, good, bad = pick(r, items)
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    r.shuffle(opts)
    return Q(qtxt, good, ["Match the conclusion to the definition or theorem whose hypotheses are met.", good + "."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


@fam("012", mode="mc")
def s7_notation(r, L):
    a, b = sorted(r.sample(range(0, 10), 2))
    items = [("Which expression gives the instantaneous rate of change of f at x = a?", "lim (h → 0) (f(a + h) - f(a))/h", ["(f(b) - f(a))/(b - a)", "lim (h → 0) (f(a + h) - f(a))", "f(a + h) - f(a)"]),
             (f"Which expression gives the average value of f on [{a}, {b}]?", f"(1/({b} - {a})) ∫ from {a} to {b} f(x) dx", [f"∫ from {a} to {b} f(x) dx", f"(f({b}) + f({a}))/2", f"(f({b}) - f({a}))/({b} - {a})"]),
             (f"Which expression gives the average rate of change of f on [{a}, {b}]?", f"(f({b}) - f({a}))/({b} - {a})", [f"(1/({b} - {a})) ∫ from {a} to {b} f(x) dx", f"f′(({a} + {b})/2)", f"f({b}) - f({a})"]),
             ("Which notation means the second derivative of y with respect to x?", "y″", ["(y′)²", "2y′", "y²"]),
             (f"A tank's volume is V(t). Which expression gives the change in volume from t = {a} to t = {b}?", f"∫ from {a} to {b} V′(t) dt", [f"∫ from {a} to {b} V(t) dt", f"V′({b}) - V′({a})", f"V′({b})"]),
             (f"Which expression gives the total distance traveled from t = {a} to t = {b} with velocity v(t)?", f"∫ from {a} to {b} |v(t)| dt", [f"∫ from {a} to {b} v(t) dt", f"|∫ from {a} to {b} v(t) dt|", f"v({b}) - v({a})"])]
    need(a != b)
    qtxt, good, bad = pick(r, items)
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    r.shuffle(opts)
    return Q(qtxt, good, [good + "."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


@fam("012")
def s5_table_mix(r, L):
    xs = [0, 2, 5, 7, 10] if L else [0, 2, 4, 6, 8]
    vals = [rint(r, -10, 20) for _ in xs]
    kind = pick(r, ["deriv", "trap", "avg"])
    tbl = "; ".join(f"f({a}) = {b}" for a, b in zip(xs, vals))
    if kind == "deriv":
        i = rint(r, 1, 3)
        v = sp.Rational(vals[i + 1] - vals[i - 1], xs[i + 1] - xs[i - 1])
        return Q(f"A differentiable function has {tbl}. Estimate f′({xs[i]}) using the nearest values on either side.", T(v), [f"(f({xs[i + 1]}) - f({xs[i - 1]})) ÷ ({xs[i + 1]} - {xs[i - 1]}) = {T(v)}."],
                 [T(sp.Rational(vals[i + 1] - vals[i], xs[i + 1] - xs[i])) if sp.Rational(vals[i + 1] - vals[i], xs[i + 1] - xs[i]) != v else T(v + 1), str(vals[i]), T(sp.Rational(xs[i + 1] - xs[i - 1], vals[i + 1] - vals[i - 1])) if vals[i + 1] != vals[i - 1] else "1"],
                 H(f"Rational({vals[i + 1]} - ({vals[i - 1]}), {xs[i + 1]} - ({xs[i - 1]}))"), why=["Used a one-sided difference", "Gave the function value", "Inverted the ratio"])
    tr = sum(sp.Rational((vals[i] + vals[i + 1]) * (xs[i + 1] - xs[i]), 2) for i in range(4))
    if kind == "trap":
        return Q(f"A continuous function has {tbl}. Use a trapezoidal sum with these four subintervals to approximate ∫ from {xs[0]} to {xs[-1]} f(x) dx.", T(tr),
                 ["Each trapezoid: width × average of the two heights.", f"Sum = {T(tr)}."], [T(sum(vals[i] * (xs[i + 1] - xs[i]) for i in range(4))), T(sum(vals)), T(2 * tr)], PY("table_sum", xs=xs, ys=vals, how="trap"),
                 why=["Used a left sum", "Added the values without widths", "Forgot the 1/2"])
    av = tr / (xs[-1] - xs[0])
    return Q(f"A continuous function has {tbl}. Use a trapezoidal sum with these four subintervals to approximate the average value of f on [{xs[0]}, {xs[-1]}].", T(av),
             [f"∫ ≈ {T(tr)}.", f"Average ≈ {T(tr)} ÷ {xs[-1] - xs[0]} = {T(av)}."], [T(tr), T(sp.Rational(sum(vals), 5)), T(sp.Rational(vals[0] + vals[-1], 2))], PY("table_avg", xs=xs, ys=vals),
             why=["Forgot to divide by the interval length", "Averaged the table values", "Averaged the endpoint values"])


SKILLS = {
    1: dict(name="Limits and Continuity Review", std=["AP LIM-1.E", "AP LIM-2.A"], fams=[rr(C2.s3_algebra), rr(C2.s4_piece), rr(C2.s6_k), rr(C2.s5_infty)], extra=[err_of(rr(C2.s3_algebra, tag="e")), open_of(rr(C2.s6_k, tag="o"))]),
    2: dict(name="Derivatives and Their Applications Review", std=["AP FUN-3.A", "AP FUN-4.A", "AP CHA-3.D"], fams=[rr(C3.s3_rule), rr(C3.s6_tangent), rr(C4.s4_absolute), rr(C4.s6_related)],
            extra=[err_of(rr(C3.s3_rule, tag="e")), open_of(rr(C4.s6_related, tag="o"))]),
    3: dict(name="Integrals and the Fundamental Theorem Review", std=["AP FUN-6.B", "AP FUN-5.A", "AP CHA-4.C"], fams=[rr(C6.s5_eval), rr(C6.s4_chain), rr(C7.s5_total), rr(C7.s6_area)],
            extra=[err_of(rr(C6.s5_eval, tag="e")), open_of(rr(C7.s3_avg, tag="o"))]),
    4: dict(name="Differential Equations Review", std=["AP FUN-7.D", "AP FUN-7.E"], fams=[rr(C8.s5_general), rr(C8.s6_particular), rr(C8.s3_euler), rr(C8.s1_slope)],
            extra=[err_of(rr(C8.s6_particular, tag="e")), open_of(rr(C8.s3_euler, tag="o"))]),
    5: dict(name="Connecting Graphs, Tables, Formulas, and Verbal Descriptions", std=["AP FUN-4.A", "AP CHA-2.D", "AP LIM-5.A"], fams=[s5_table_mix, rr(C3.s7_graph), rr(C6.s2_accum), rr(C4.s1_meaning)],
            extra=[err_of(s5_table_mix), open_of(s5_table_mix)]),
    6: dict(name="Justifying Solutions with Definitions and Theorems", std=["AP FUN-1.A", "AP FUN-1.B", "AP FUN-4.A"], fams=[s6_justify, rr(C2.s8_ivt), rr(C4.s10_mvt), rr(C4.s2_classify)],
            extra=[err_of(rr(C4.s10_mvt, tag="e")), open_of(rr(C2.s8_ivt, tag="o"))]),
    7: dict(name="Calculus Notation and Written Explanations", std=["AP LIM-1.A", "AP FUN-6.A", "AP CHA-4.A"], fams=[s7_notation, rr(C5.s4_convert), rr(C7.s1_meaning), rr(C5.s7_props)],
            extra=[err_of(rr(C5.s7_props, tag="e")), open_of(rr(C5.s7_props, tag="o"))]),
}
