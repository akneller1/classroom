"""Grade 6 Unit 4 — Expressions and Equations (expressions-equations)."""
from glib import *
import g7_u01 as A7, g7_u02 as E7, g7_u04 as X7

UNIT_ID = "expressions-equations"
ABBR = "exq"


# ============================================================== S1 Numerical expressions with exponents
@fam("012")
def s1_eval(r, L):
    b, e = r.randint(2, 6), r.randint(2, 3)
    c, d = r.randint(1, 9), r.randint(2, 5)
    forms = [f"{b}{sup(e)} + {c}", f"{c} × {b}{sup(2)}", f"{b}{sup(e)} - {d}"] if L == 0 else \
            [f"{b}{sup(2)} + {c} × {d}", f"({b} + {c}){sup(2)}", f"{d}{sup(3)} ÷ {d} + {c}"] if L == 1 else \
            [f"(1/{d}){sup(2)} × {d * d * c}", f"(0.{c}){sup(2)}", f"{b}{sup(3)} - ({c} + {d}){sup(2)} ÷ ({c} + {d})"]
    t = pick(r, forms)
    import mathtext
    v = mathtext.ev(t)
    w2 = mathtext.ev(t.replace(sup(2), "*2").replace(sup(3), "*3"))
    return Q(f"Evaluate: {t}", N(v) if F(v).denominator > 1 and not is_term(F(v)) else D(F(v)), ["Evaluate exponents first (after any parentheses).", "Then multiply or divide, then add or subtract.", f"Result: {D(F(v)) if is_term(F(v)) else N(v)}."],
             [D(F(w2)) if is_term(F(w2)) else N(w2), D(F(v) + 1) if is_term(F(v)) else N(v + 1), D(F(v) * 2) if is_term(F(v)) else N(v * 2)], V(t),
             why=["Multiplied the base by the exponent", "Made an arithmetic error", ""])


# ============================================================== S4 Equivalent Expressions
@fam("012")
def s4_equiv_yesno(r, L):
    v = pick(r, ["x", "y", "n"])
    a, b, c = r.randint(2, 9), r.randint(1, 9), r.randint(1, 9)
    pairs = [(f"{a}({v} + {b})", f"{a}{v} + {a * b}", True), (f"{a}({v} + {b})", f"{a}{v} + {b}", False), (f"{v} + {v} + {v}", f"3{v}", True), (f"{v} + {v} + {v}", f"{v}{sup(3)}", False),
             (f"{a}{v} + {c}{v}", f"{a + c}{v}", True), (f"{a}{v} + {c}", f"{a + c}{v}", False), (f"{a * b}{v} + {a * c}", f"{a}({b}{v} + {c})", True), (f"{v} · {v}", f"2{v}", False)]
    e1, e2, ok = pick(r, pairs)
    return Q(f"Are the expressions {e1} and {e2} equivalent?", "Yes" if ok else "No", ["Equivalent expressions have the same value for every value of the variable.", f"Test {v} = 2: {e1} → {N(evv(e1, v, 2))}; {e2} → {N(evv(e2, v, 2))}.",
                                                                                 "Yes" if ok else "No (one counterexample is enough)."], ["No" if ok else "Yes"], PY("equiv_yn", a=e1, b=e2, var=v), mode="sa",
             why=["Checked only one value or combined unlike terms"], tags=["reasoning"])


def evv(e, v, x):
    import mathtext
    return mathtext.ev(e, {v: F(x)})


@fam("012", mode="mc")
def s4_which(r, L):
    v = pick(r, ["x", "y", "a"])
    a, b, c = r.randint(2, 6), r.randint(1, 9), r.randint(2, 6)
    e = f"{a}({v} + {b}) + {c}{v}" if L else f"{a}({v} + {b})"
    good = lin((a + (c if L else 0), v), (a * b, ""))
    bad = [lin((a + (c if L else 0), v), (b, "")), lin((a * (c if L else 1), v), (a * b, "")) if L else lin((a, v), (a + b, "")), f"{a + b + (c if L else 0)}{v}"]
    opts = [(good, True)] + [(x, False) for x in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Which expression is equivalent to {e}?", good, [f"Distribute: {lin((a, v), (a * b, ''))}" + (f" + {c}{v}." if L else "."), f"Combine like terms: {good}."], options=opts, chk=EQV(e, [v]), mode="mc")


# ============================================================== S5 Solutions of Equations
@fam("012", mode="mc")
def s5_which_value(r, L):
    v = pick(r, ["x", "n", "m"])
    x = r.randint(1, 15)
    a, b = r.randint(2, 9), r.randint(1, 20)
    eq = pick(r, [f"{v} + {b} = {x + b}", f"{a}{v} = {a * x}", f"{a}{v} + {b} = {a * x + b}"] if L else [f"{v} + {b} = {x + b}", f"{a}{v} = {a * x}"])
    cands = sorted({x, x + 1, max(1, x - 2), x + b, a * x} - {0})
    need(len(cands) >= 4)
    others = [c for c in cands if c != x]
    r.shuffle(others)
    opts = [(f"{v} = {x}", True)] + [(f"{v} = {c}", False) for c in others[:3]]
    r.shuffle(opts)
    return Q(f"Which value is a solution of {eq}?", f"{v} = {x}", ["Substitute each value.", f"Only {v} = {x} makes both sides equal."], options=opts, chk=EQ(eq, v), mode="mc")


# ============================================================== S6 Solving one-variable equations
@fam("012")
def s6_rational(r, L):
    v = pick(r, ["x", "n", "y", "p"])
    kind = pick(r, ["add", "mul"])
    if L == 0:
        x, a = r.randint(1, 50), r.randint(2, 30)
    else:
        x = F(r.randint(1, 40), pick(r, [2, 4, 10])) if L == 1 else F(r.randint(1, 60), pick(r, [3, 4, 5, 8]))
        a = F(r.randint(1, 20), pick(r, [2, 4, 10])) if L == 1 else F(r.randint(1, 12), pick(r, [3, 4, 6]))
    if kind == "add":
        eq = f"{v} + {N(a) if F(a).denominator > 1 else a} = {N(F(x) + a)}"
        sol = F(x)
        wr = [F(x) + 2 * F(a), F(x) + F(a), F(a)]
        why = ["Added instead of subtracting", "Gave the right side", "Gave the number added"]
    else:
        need(F(a) != 1)
        eq = f"{N(a) if F(a).denominator > 1 else a}{v} = {N(F(x) * F(a))}" if F(a).denominator == 1 else f"({N(a)}){v} = {N(F(x) * F(a))}"
        sol = F(x)
        wr = [F(x) * F(a) * F(a), F(x) * F(a) - F(a), 1 / F(x) if x else F(2)]
        why = ["Multiplied instead of dividing", "Subtracted instead of dividing", "Divided in the wrong order"]
    return Q(f"Solve: {eq}", f"{v} = {mixed(sol)}", ["Use the inverse operation on both sides.", f"{v} = {mixed(sol)}.", "Check by substituting."], [f"{v} = {mixed(w)}" for w in wr], EQ(eq, v), why=why)


# ============================================================== S7 Dependent and Independent Variables
@fam("012", mode="mc")
def s7_identify(r, L):
    ctx = pick(r, [("the number of hours worked", "the money earned"), ("the number of tickets bought", "the total cost"), ("the time a candle burns", "the height of the candle"),
                   ("the number of pages read", "the time spent reading"), ("the distance driven", "the gas used"), ("the number of guests", "the amount of food needed")])
    ind, dep = ctx
    ask = pick(r, ["dependent", "independent"])
    good = dep if ask == "dependent" else ind
    opts = [(good, True), (ind if ask == "dependent" else dep, False), ("both quantities", False), ("neither quantity", False)]
    r.shuffle(opts)
    return Q(f"In the relationship between {ind} and {dep}, which is the {ask} variable?", good, ["The dependent variable changes in response to the independent variable.", f"{dep.capitalize()} depends on {ind}.", f"The {ask} variable is {good}."],
             options=opts, chk=TXT(good), mode="mc")


@fam("012")
def s7_equation(r, L):
    k, b = r.randint(2, 15), r.randint(0, 20) if L == 2 else 0
    xs = sorted(r.sample(range(1, 10), 3))
    ys = [k * x + b for x in xs]
    ctx = pick(r, [("t", "d", "hours", "miles"), ("n", "c", "items", "dollars"), ("w", "p", "weeks", "pages")])
    xv, yv, xu, yu = ctx
    rule = f"{yv} = {k}{xv}" + (f" + {b}" if b else "")
    return Q(f"A table shows {xu} ({xv}): {', '.join(map(str, xs))} and {yu} ({yv}): {', '.join(map(str, ys))}. Write an equation for {yv} in terms of {xv}.", rule,
             ["Look for how the dependent variable changes as the independent variable changes.", f"{yv} increases by {k} for each 1 added to {xv}.", f"{rule}." + (" Check the starting amount with a table value." if b else "")],
             [f"{xv} = {k}{yv}", f"{yv} = {xv} + {ys[0] - xs[0]}", f"{yv} = {ys[0]}{xv}"], PY("rule_xy", xv=xv, yv=yv, pts=[[x, y] for x, y in zip(xs, ys)]),
             why=["Switched the dependent and independent variables", "Used a constant difference between x and y", "Used the first y-value as the rate"], tags=["multiple-representations", "modeling"])


@fam("12")
def s7_evaluate(r, L):
    k, x = r.randint(3, 25), r.randint(2, 15)
    return Q(f"A plumber charges c = {k}h dollars for h hours of work. Which variable is dependent, and what is c when h = {x}?", f"c is dependent; c = {k * x}", ["c depends on h, so c is the dependent variable.", f"c = {k} × {x} = {k * x}."],
             [f"h is dependent; c = {k * x}", f"c is dependent; c = {k + x}", f"h is dependent; c = {k + x}"], PY("dep_eval", k=k, x=x), why=["Switched dependent and independent", "Added instead of multiplying", ""])


SKILLS = {
    1: dict(name="Writing and Evaluating Numerical Expressions with Exponents", std=["6.EE.A.1"], fams=[s1_eval, reuse(X7.s2_eval, (0, 0, 1)), reuse(X7.s2_write, (0, 1, 1))], extra=[err_of(s1_eval), open_of(s1_eval), select_of(s1_eval)]),
    2: dict(name="Writing and Evaluating Algebraic Expressions", std=["6.EE.A.2"], fams=[reuse(A7.s2_translate), reuse(A7.s4_evaluate, (0, 0, 1)), reuse(A7.s2_context), reuse(A7.s2_parts)],
            extra=[err_of(reuse(A7.s4_evaluate, (0, 0, 1), "e")), open_of(reuse(A7.s2_translate, (0, 1, 2), "o")), select_of(reuse(A7.s4_evaluate, (0, 0, 1), "s"))]),
    3: dict(name="The Order of Operations", std=["6.EE.A.2c", "5.OA.A.1"], fams=[reuse(A7.s3_eval), reuse(A7.s3_fraction_bar), reuse(A7.s3_context), reuse(A7.s3_parens, (1, 1, 2))],
            extra=[err_of(reuse(A7.s3_eval, (0, 1, 2), "e")), open_of(reuse(A7.s3_eval, (0, 1, 2), "o")), select_of(reuse(A7.s3_eval, (0, 1, 2), "s"))]),
    4: dict(name="Equivalent Expressions", std=["6.EE.A.3", "6.EE.A.4"], fams=[s4_equiv_yesno, s4_which, reuse(E7.s2_expand, (0, 0, 1)), reuse(E7.s3_combine, (0, 0, 1))],
            extra=[err_of(reuse(E7.s2_expand, (0, 0, 1), "e")), open_of(reuse(E7.s3_combine, (0, 0, 1), "o"))]),
    5: dict(name="Solutions of Equations", std=["6.EE.B.5"], fams=[s5_which_value, reuse(E7.s4_is_solution, (0, 0, 1)), reuse(E7.s4_classify)], extra=[err_of(reuse(E7.s4_write, (0, 1, 2), "e")), open_of(reuse(E7.s4_is_solution, (0, 0, 1), "o"))]),
    6: dict(name="Solving One-Variable Equations", std=["6.EE.B.7"], fams=[s6_rational, reuse(E7.s5_context), reuse(E7.s6_context, (0, 1, 1))], extra=[err_of(s6_rational), open_of(s6_rational), select_of(s6_rational)]),
    7: dict(name="Dependent and Independent Variables", std=["6.EE.C.9"], fams=[s7_identify, s7_equation, s7_evaluate], extra=[err_of(s7_equation), open_of(s7_equation)]),
}
