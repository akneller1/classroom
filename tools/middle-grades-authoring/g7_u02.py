"""Grade 7 Unit 2 — Solving One-Step Equations and Inequalities (one-step-equations-inequalities)."""
from glib import *

UNIT_ID = "one-step-equations-inequalities"
ABBR = "osei"
VARS = ["x", "n", "y", "m", "k", "a", "t", "w"]


# ============================================================== S1 Properties of Numbers
PROPS = [("Commutative Property of Addition", "{a} + {b} = {b} + {a}"), ("Commutative Property of Multiplication", "{a} × {b} = {b} × {a}"),
         ("Associative Property of Addition", "({a} + {b}) + {c} = {a} + ({b} + {c})"), ("Associative Property of Multiplication", "({a} × {b}) × {c} = {a} × ({b} × {c})"),
         ("Identity Property of Addition", "{a} + 0 = {a}"), ("Identity Property of Multiplication", "{a} × 1 = {a}"),
         ("Distributive Property", "{a}({b} + {c}) = {a} × {b} + {a} × {c}"), ("Zero Property of Multiplication", "{a} × 0 = 0")]


@fam("012", mode="mc")
def s1_name(r, L):
    a, b, c = r.sample(range(2, 30), 3)
    pool = PROPS[:6] if L == 0 else PROPS
    i = r.randrange(len(pool))
    nm, f = pool[i]
    if L == 2:
        v = pick(r, ["x", "y", "n"])
        a = v
    st = f.format(a=a, b=b, c=c)
    near = [p for p in PROPS if p[0] != nm and (p[0].split()[0] == nm.split()[0] or p[0].split()[-1] == nm.split()[-1])]
    rest = [p for p in PROPS if p[0] != nm and p not in near]
    r.shuffle(near)
    r.shuffle(rest)
    opts = [(nm, True)] + [(p[0], False) for p in (near + rest)[:3]]
    r.shuffle(opts)
    return Q(f"Which property is shown? {st}", nm, [f"{st} shows the {nm}."], options=opts, chk=TXT(nm), mode="mc", tags=["reasoning"])


@fam("012")
def s1_missing(r, L):
    a, b, c = r.sample(range(2, 20), 3)
    forms = [(f"{a} + {b} = {b} + ?", a, "Commutative Property of Addition"), (f"{a} × ? = {b} × {a}", b, "Commutative Property of Multiplication"),
             (f"({a} + {b}) + {c} = {a} + (? + {c})", b, "Associative Property of Addition"), (f"{a} × 1 = ?", a, "Identity Property of Multiplication"),
             (f"{a}({b} + {c}) = {a} × {b} + {a} × ?", c, "Distributive Property"), (f"({a} × {b}) × {c} = {a} × ({b} × ?)", c, "Associative Property of Multiplication")]
    st, v, nm = pick(r, forms if L else forms[:4])
    return Q(f"What number makes the statement true? {st}", str(v), [f"This uses the {nm}.", f"The missing number is {v}."],
             [str(x) for x in (a + b, a * b, b + c, a, b, c) if x != v][:3], PY("missing_num", st=st), why=["Computed instead of using the property", "", ""], mode="sa")


@fam("012")
def s1_mental(r, L):
    if L == 0:
        a, b = r.randint(11, 49), r.randint(11, 49)
        c = 100 - a if a < 100 else 50
        e = f"{a} + {b} + {c}"
        return Q(f"Use properties to find the sum mentally: {e}", str(a + b + c), [f"Reorder (Commutative Property): {a} + {c} + {b}.", f"{a} + {c} = {a + c}.", f"{a + c} + {b} = {a + b + c}."],
                 [str(a + b + c + 10), str(a + b + c - 10), str(a * b)], V(e), why=["Made a regrouping error", "", ""])
    if L == 1:
        a, b = pick(r, [2, 4, 5, 20, 25, 50]), r.randint(3, 49)
        c = {2: 5, 4: 25, 5: 2, 20: 5, 25: 4, 50: 2}[a]
        e = f"{a} × {b} × {c}"
        return Q(f"Use properties to find the product mentally: {e}", str(a * b * c), [f"Reorder: {a} × {c} × {b}.", f"{a} × {c} = {a * c}.", f"{a * c} × {b} = {a * b * c}."],
                 [str(a * b + c), str(a + b + c), str(a * b * c * 10)], V(e), why=["Added instead of multiplying the last factor", "", ""])
    a, b = r.randint(3, 9), r.randint(1, 4)
    n = 100 + b if r.random() < 0.5 else 100 - b
    e = f"{a} × {n}"
    return Q(f"Use the Distributive Property to find {e} mentally.", str(a * n), [f"{n} = 100 {'+' if n > 100 else '-'} {b}.", f"{a} × 100 {'+' if n > 100 else '-'} {a} × {b}.",
                                                                             f"{100 * a} {'+' if n > 100 else '-'} {a * b} = {a * n}."],
             [str(100 * a + b if n > 100 else 100 * a - b), str(a * n + 10), str(100 * a)], V(e), why=["Multiplied only the 100 by the factor", "", "Ignored the extra part"])


# ============================================================== S2 Distributive Property
@fam("012")
def s2_expand(r, L):
    v = pick(r, VARS)
    a = r.randint(2, 9) if L == 0 else nz(r, -9, 9)
    b = r.randint(1, 12) if L == 0 else nz(r, -12, 12)
    c = 1 if L < 2 else r.randint(2, 6)
    inner = lin((c, v), (b, ""))
    e = f"{a}({inner})" if a > 0 else f"-{abs(a)}({inner})" if a != -1 else f"-({inner})"
    ans = lin((a * c, v), (a * b, ""))
    return Q(f"Use the Distributive Property to simplify {e}.", ans, [f"Multiply {a} by each term inside the parentheses.", f"{a} × {coef_text(c, v)} = {coef_text(a * c, v)} and {a} × {par(b)} = {a * b}.", f"Result: {ans}."],
             [lin((a * c, v), (b, "")), lin((a * c, v), (-a * b, "")), lin((a + c, v), (a + b, "")), lin((c, v), (a * b, ""))], EQV(e, [v]),
             why=["Multiplied only the first term", "Made a sign error with the second term", "Added instead of multiplying", "Multiplied only the second term"])


@fam("012")
def s2_factor(r, L):
    v = pick(r, VARS)
    g = r.randint(2, 9)
    p, q = r.randint(1, 9), r.randint(1, 9)
    need(math.gcd(p, q) == 1)
    e = lin((g * p, v), (g * q * (1 if L < 2 else pick(r, [1, -1])), ""))
    qq = g * q * (1 if " + " in e else -1) // g
    ans = f"{g}({lin((p, v), (qq, ''))})"
    return Q(f"Factor using the greatest common factor: {e}", ans, [f"The GCF of {g * p} and {g * q} is {g}.", f"Divide each term by {g}: {coef_text(p, v)} and {qq}.", f"{e} = {ans}."],
             [f"{g}({lin((g * p, v), (qq, ''))})", f"{g * p}({v} {'+' if qq > 0 else '-'} {N(F(abs(qq), p))})" if p > 1 else f"1({e})", f"{g}({coef_text(p, v)}{abs(qq)})"],
             PY("factored", expr=e, gcf=g, vars=[v]), why=["Divided only the constant term by the GCF", "", ""]) if L else \
        Q(f"Write {g * p} × {g * q} + {g * p} × {r.randint(1, 3)}  … ", None, []) if False else \
        Q(f"Complete: {g}({p} + {q}) = {g} × {p} + {g} × ?", str(q), [f"Distribute {g} to both {p} and {q}.", f"The missing factor is {q}."], [str(g * q), str(p), str(g + q)],
          PY("missing_num", st=f"{g}({p} + {q}) = {g} × {p} + {g} × ?"), why=["Multiplied instead of finding the factor", "", ""])


@fam("012")
def s2_area(r, L):
    a, b, c = r.randint(3, 12), r.randint(2, 9), r.randint(2, 9)
    if L < 2:
        return Q(f"A rectangle is {a} m wide and its length is split into parts of {b} m and {c} m. Find the area using the Distributive Property.", f"{a * (b + c)} square meters",
                 [f"Area = {a}({b} + {c}).", f"= {a} × {b} + {a} × {c} = {a * b} + {a * c}.", f"= {a * (b + c)} square meters."],
                 [f"{a * b + c} square meters", f"{a + b + c} square meters", f"{2 * (a + b + c)} square meters"], V(f"{a}*({b} + {c})"),
                 why=["Multiplied only the first part", "Added the dimensions", "Found the perimeter"], tags=["connections"])
    v = pick(r, ["x", "w"])
    return Q(f"A rectangle is {a} units wide and ({v} + {b}) units long. Write a simplified expression for its area.", f"{a}{v} + {a * b}",
             [f"Area = {a}({v} + {b}).", f"Distribute: {a}{v} + {a * b}."], [f"{a}{v} + {b}", f"{a + b}{v}", f"2{v} + {2 * (a + b)}"], EQV(f"{a}({v} + {b})", [v]),
             why=["Multiplied only the first term", "Combined unlike terms", "Wrote the perimeter"], tags=["connections"])


# ============================================================== S3 Simplifying Variable Expressions
@fam("012")
def s3_combine(r, L):
    v = pick(r, VARS)
    if L == 0:
        a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(1, 15)
        e = f"{a}{v} + {c} + {b}{v}"
        ans = lin((a + b, v), (c, ""))
        wr = [f"{a + b + c}{v}", lin((a * b, v), (c, "")), lin((a + b, v), (c, v))]
    elif L == 1:
        a, b, c, d = r.randint(2, 12), nz(r, -9, 9), r.randint(1, 15), nz(r, -15, 15)
        e = f"{a}{v} {sgn(c)} {sgn(b)[0]} {coef_text(abs(b), v)} {sgn(d)}".replace("+ +", "+")
        e = f"{a}{v} + {c} {'+' if b > 0 else '-'} {coef_text(abs(b), v)} {'+' if d > 0 else '-'} {abs(d)}"
        ans = lin((a + b, v), (c + d, ""))
        wr = [lin((a + abs(b), v), (c + d, "")), lin((a + b, v), (c - d, "")), f"{a + b + c + d}{v}"]
    else:
        a, b, c, d = nz(r, -6, 6), r.randint(2, 6), nz(r, -9, 9), nz(r, -9, 9)
        e = f"{a}({v} {'+' if c > 0 else '-'} {abs(c)}) {'+' if b > 0 else '-'} {b}{v} {'+' if d > 0 else '-'} {abs(d)}"
        e = e.replace("1(", "(") if a == 1 else e.replace("-1(", "-(") if a == -1 else e
        ans = lin((a + b, v), (a * c + d, ""))
        wr = [lin((a + b, v), (c + d, "")), lin((a + b, v), (-a * c + d, "")), lin((a * b, v), (a * c + d, ""))]
    need(lin((a + b, v), (0, "")) != "0")
    return Q(f"Simplify: {e}", ans, ["Identify like terms (same variable part).", "Distribute first if there are parentheses." if L == 2 else "Group the variable terms and the constants.", f"Combine: {ans}."],
             wr, PY("poly_std", expr=e, vars=[v]), why=["Combined unlike terms" if L == 0 else "Ignored the sign in front of a term", "Made a sign error with a constant", "Multiplied coefficients instead of adding"])


@fam("12")
def s3_perimeter(r, L):
    v = pick(r, ["x", "s"])
    a, b, c = r.randint(1, 6), r.randint(1, 9), r.randint(1, 9)
    sides = [f"{coef_text(a, v)} + {b}", f"{coef_text(a + 1, v)}", f"{v} + {c}"]
    ans = lin((a + a + 1 + 1, v), (b + c, ""))
    return Q(f"A triangle has sides ({sides[0]}), ({sides[1]}), and ({sides[2]}). Write a simplified expression for its perimeter.", ans,
             ["Perimeter is the sum of the sides.", f"Add the {v}-terms: {a} + {a + 1} + 1 = {2 * a + 2}.", f"Add the constants: {b} + {c} = {b + c}.", f"Perimeter: {ans}."],
             [lin((2 * a + 1, v), (b + c, "")), f"{2 * a + 2 + b + c}{v}", lin((2 * a + 2, v), (b * c, ""))], EQV(f"({sides[0]}) + ({sides[1]}) + ({sides[2]})", [v]),
             why=["Forgot the coefficient 1 on the last side", "Combined unlike terms", "Multiplied the constants"], tags=["connections"])


@fam("012", mode="mc")
def s3_equiv(r, L):
    v = pick(r, VARS)
    a, b, c = r.randint(2, 7), r.randint(2, 9), r.randint(1, 9)
    e = f"{a}({v} + {b}) + {c}{v}"
    good = lin((a + c, v), (a * b, ""))
    opts = [(good, True), (lin((a + c, v), (b, ""), ), False), (lin((a * c, v), (a * b, "")), False), (f"{a + b + c}{v}", False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Which expression is equivalent to {e}?", good, [f"Distribute: {a}{v} + {a * b} + {c}{v}.", f"Combine like terms: {good}."], options=opts, chk=EQV(e, [v]), mode="mc")


# ============================================================== S4 Variables and Equations
@fam("012")
def s4_is_solution(r, L):
    v = pick(r, VARS)
    a, x = r.randint(2, 9), r.randint(-9 if L else 1, 12)
    b = r.randint(1, 20)
    rhs = a * x + b
    test = x if r.random() < 0.5 else x + pick(r, [1, -1, 2])
    eq = f"{a}{v} + {b} = {rhs}" if L < 2 else f"{a}({v} - {b}) = {a * (x - b)}"
    if L == 2:
        rhs = a * (x - b)
    ok = (a * test + b == rhs) if L < 2 else a * (test - b) == rhs
    ans = "Yes" if ok else "No"
    return Q(f"Is {v} = {test} a solution of {eq}?", ans, [f"Substitute {test} for {v}.", f"Left side = {a * test + b if L < 2 else a * (test - b)}; right side = {rhs}.",
                                                          f"{'They are equal, so yes' if ok else 'They are not equal, so no'}."],
             ["No" if ok else "Yes"], PY("is_solution", rel=eq, var=v, v=str(test)), mode="sa", why=["Made a substitution error"])


@fam("012", mode="mc")
def s4_classify(r, L):
    a, b = r.randint(2, 20), r.randint(2, 20)
    kind = pick(r, ["true", "false", "open"])
    st = {"true": f"{a} + {b} = {a + b}", "false": f"{a} × {b} = {a + b + 1}", "open": f"{a} + n = {a + b}"}[kind]
    need(not (kind == "false" and a * b == a + b + 1))
    opts = [("true", kind == "true"), ("false", kind == "false"), ("open", kind == "open")]
    ans = kind
    return Q(f"Is the equation true, false, or open? {st}", ans, ["An open sentence contains a variable.", "Otherwise evaluate each side and compare.", f"The equation is {ans}."],
             options=opts + [("cannot be decided", False)], chk=PY("classify_eq", st=st), mode="mc", tags=["reasoning"])


@fam("012")
def s4_write(r, L):
    v = pick(r, VARS)
    a, b = r.randint(2, 15), r.randint(20, 90)
    ctx = [(f"A number {v} increased by {a} is {b}.", f"{v} + {a} = {b}", [(f"{a}{v} = {b}", "Multiplied instead of adding"), (f"{v} - {a} = {b}", "Subtracted instead of adding"), (f"{v} = {a} + {b} + 1", "")]),
           (f"{a} times a number {v} is {a * b}.", f"{a}{v} = {a * b}", [(f"{v} + {a} = {a * b}", "Added instead of multiplying"), (f"{v}/{a} = {a * b}", "Divided instead of multiplying"), (f"{a * b}{v} = {a}", "Reversed the numbers")]),
           (f"After spending ${a}, Kim has ${b} left. Let {v} be the amount she started with.", f"{v} - {a} = {b}", [(f"{a} - {v} = {b}", "Reversed the subtraction"), (f"{v} + {a} = {b}", "Added instead of subtracting"), (f"{a}{v} = {b}", "")])]
    st, ans, wr = pick(r, ctx)
    return Q(f"Write an equation: {st}", ans, ["Translate words into symbols.", "“is” means =.", f"Equation: {ans}."], [w for w, _ in wr], PY("eq_same", eq=ans, var=v),
             why=[y for _, y in wr], tags=["modeling"])


# ============================================================== S5 / S6 One-step equations
def one_step(r, L, ops):
    v = pick(r, VARS)
    op = pick(r, ops)
    if L == 0:
        x, a = r.randint(1, 30), r.randint(2, 20)
    elif L == 1:
        x, a = nz(r, -40, 40), nz(r, -25, 25)
    else:
        x, a = nz(r, -60, 60), nz(r, -30, 30)
    if op == "add":
        eq, b = f"{v} + {a}" if a > 0 else f"{v} - {-a}", x + a
        eq = f"{eq} = {b}"
        if L == 2 and r.random() < 0.5:
            eq = f"{b} = {a} + {v}" if a > 0 else f"{b} = {v} - {-a}"
        wr = [x + 2 * a, -x, b]
        why = ["Added instead of subtracting (did not undo the operation)", "Made a sign error", "Gave the right-side value"]
        st = [f"Undo {'adding' if a > 0 else 'subtracting'} {abs(a)}: {'subtract' if a > 0 else 'add'} {abs(a)} on both sides.", f"{v} = {b} {'-' if a > 0 else '+'} {abs(a)}.", f"{v} = {x}.", f"Check: substitute {x} into the original equation."]
    elif op == "sub":
        b = x - a
        eq = f"{v} - {par(a)} = {b}" if L else f"{v} - {a} = {b}"
        wr = [x - 2 * a, -x, b]
        why = ["Subtracted again instead of adding", "Made a sign error", "Gave the right-side value"]
        st = [f"Undo subtracting {par(a)}: add {par(a)} to both sides.", f"{v} = {b} + {par(a)}.", f"{v} = {x}.", "Check by substitution."]
    elif op == "mul":
        a = abs(a) if L == 0 else a
        need(abs(a) > 1)
        b = a * x
        eq = f"{a}{v} = {b}"
        wr = [b - a, -x, b * a]
        why = ["Subtracted the coefficient instead of dividing", "Made a sign error when dividing", "Multiplied instead of dividing"]
        st = [f"Undo multiplying by {a}: divide both sides by {a}.", f"{v} = {b} ÷ {par(a)}.", f"{v} = {x}.", "Check by substitution."]
    else:
        a = abs(a) if L == 0 else a
        need(abs(a) > 1)
        b = x
        x = a * b
        eq = f"{v}/{a} = {b}" if a > 0 else f"{v}/({a}) = {b}"
        wr = [N(F(b, a)), -x, b + a]
        why = ["Divided instead of multiplying", "Made a sign error", "Added instead of multiplying"]
        st = [f"Undo dividing by {a}: multiply both sides by {a}.", f"{v} = {b} × {par(a)}.", f"{v} = {x}.", "Check by substitution."]
    wr = [f"{v} = {N(w)}" for w in wr]
    return Q(f"Solve: {eq}", f"{v} = {x}", st, wr, EQ(eq, v), why=why)


@fam("012")
def s5_solve(r, L):
    return one_step(r, L, ["add", "sub"])


@fam("012")
def s6_solve(r, L):
    return one_step(r, L, ["mul", "div"])


@fam("012")
def s5_context(r, L):
    nm = name(r)
    a, x = r.randint(5, 60), r.randint(5, 90)
    ctx = [(f"{nm} read some pages on Monday and {a} pages on Tuesday, for {a + x} pages in all. Write and solve an equation to find p, the pages read on Monday.", f"p + {a} = {a + x}", "p"),
           (f"After a ${a} discount, a jacket costs ${x}. Write and solve an equation to find c, the original price.", f"c - {a} = {x}", "c"),
           (f"The temperature rose {a}°F to reach {x}°F. Write and solve an equation to find t, the starting temperature.", f"t + {a} = {x}", "t")]
    if L == 2:
        ctx.append((f"An elevator went down {a} floors and is now on floor {x}. Then it rose 3 floors. Write and solve an equation to find f, the floor it started on.", f"f - {a} = {x}", "f"))
    t, eq, v = pick(r, ctx)
    sol = M_solve(eq, v)
    need(sol.denominator == 1)
    return Q(t, f"{v} = {sol}", [f"Equation: {eq}.", "Use the inverse operation on both sides.", f"{v} = {sol}."], [f"{v} = {sol + 2 * a if '+' in eq else sol - 2 * a}", f"{v} = {abs(x - a) + (1 if abs(x - a) == sol else 0)}", f"{v} = {x}"],
             EQ(eq, v), why=["Used the same operation instead of the inverse", "", "Gave the final value instead of solving"], tags=["modeling"])


def M_solve(eq, v):
    import mathtext
    return F(mathtext.solve_linear(eq, v)[1])


@fam("012")
def s6_context(r, L):
    nm = name(r)
    a, x = r.randint(2, 12), r.randint(3, 25)
    ctx = [(f"{nm} bought {a} identical books for ${a * x}. Write and solve an equation to find b, the cost of one book.", f"{a}b = {a * x}", "b"),
           (f"A ribbon was cut into {a} equal pieces, each {x} cm long. Write and solve an equation to find r, the original length in centimeters.", f"r/{a} = {x}", "r"),
           (f"A car travels at a constant speed and covers {a * x} miles in {a} hours. Write and solve an equation to find s, the speed in miles per hour.", f"{a}s = {a * x}", "s")]
    if L == 2:
        d = r.randint(2, 6)
        ctx.append((f"A diver's depth changed by -{d * x} feet over {d} equal stages. Write and solve an equation to find c, the change per stage.", f"{d}c = -{d * x}", "c"))
    t, eq, v = pick(r, ctx)
    sol = M_solve(eq, v)
    return Q(t, f"{v} = {N(sol)}", [f"Equation: {eq}.", "Use the inverse operation on both sides.", f"{v} = {N(sol)}."],
             [f"{v} = {N(sol * a * a) if '/' not in eq else N(F(x, a))}", f"{v} = {N(sol + a)}", f"{v} = {N(-sol)}"], EQ(eq, v),
             why=["Used the same operation instead of the inverse", "", "Made a sign error"], tags=["modeling"])


# ============================================================== S7 Guess, Check, and Revise
@fam("012")
def s7_sum_diff(r, L):
    a, b = r.randint(5, 40), r.randint(2, 30)
    need(a > b)
    if L == 0:
        p = f"Two numbers have a sum of {a + b} and a difference of {a - b}. What are the numbers? (Give the greater number first.)"
        conds = [f"x + y = {a + b}", f"x - y = {a - b}"]
    elif L == 1:
        p = f"The sum of two numbers is {a + b} and their product is {a * b}. What are the numbers? (Give the greater number first.)"
        conds = [f"x + y = {a + b}", f"x*y = {a * b}", "x ≥ y"]
    else:
        k = r.randint(2, 4)
        b = r.randint(2, 15)
        a = k * b
        p = f"One number is {k} times another. Their sum is {a + b}. What are the numbers? (Give the greater number first.)"
        conds = [f"x = {k}y", f"x + y = {a + b}"]
    return Q(p, f"{a} and {b}", ["Guess a pair that fits one condition.", "Check the other condition.", "Revise the guess up or down until both conditions are true.", f"The numbers are {a} and {b}."],
             [f"{a + 1} and {b - 1}", f"{a + b} and {a - b}", f"{b} and {a}" if L == 2 else f"{a - 1} and {b + 1}"], PY("conds", vars=["x", "y"], conds=conds),
             why=["Stopped after checking only one condition", "Used the given sum and difference as the numbers", "Did not check the second condition"], tags=["reasoning"])


@fam("012")
def s7_tickets(r, L):
    pa, pc = r.randint(6, 15), r.randint(2, 5)
    na, nc = r.randint(2, 12), r.randint(2, 12)
    tot_n, tot_c = na + nc, pa * na + pc * nc
    need(pa != pc)
    return Q(f"Adult tickets cost ${pa} and child tickets cost ${pc}. A group bought {tot_n} tickets for ${tot_c}. How many adult tickets did they buy?", str(na),
             [f"Guess a number of adult tickets, a; then child tickets = {tot_n} - a.", f"Check: {pa}a + {pc}({tot_n} - a) should equal {tot_c}.", "Revise the guess based on whether the total is too high or too low.",
              f"a = {na}: {pa}({na}) + {pc}({nc}) = {tot_c}."], [str(nc), str(na + 1), str(tot_c // pa)], PY("conds", vars=["a"], conds=[f"{pa}a + {pc}({tot_n} - a) = {tot_c}"]),
             why=["Gave the number of child tickets", "", "Divided the total cost by the adult price"], tags=["modeling", "multistep"])


@fam("12")
def s7_legs(r, L):
    c, d = r.randint(3, 15), r.randint(3, 15)
    return Q(f"A farm has chickens and cows. There are {c + d} animals with {2 * c + 4 * d} legs in all. How many cows are there?", str(d),
             ["Guess a number of cows; the rest are chickens.", "Count the legs: 4 per cow and 2 per chicken.", "Adjust the guess until the leg total matches.", f"{d} cows and {c} chickens: 4({d}) + 2({c}) = {2 * c + 4 * d}."],
             [str(c), str((2 * c + 4 * d) // 4), str(c + d - 1)], PY("conds", vars=["w"], conds=[f"4w + 2({c + d} - w) = {2 * c + 4 * d}"]), why=["Gave the number of chickens", "Divided all legs by 4", ""],
             tags=["modeling"])


# ============================================================== S8 Inequalities and their graphs
def ineq_text(v, op, b):
    return f"{v} {op} {N(b)}"


@fam("012")
def s8_from_graph(r, L):
    b = r.randint(-8, 8)
    op = pick(r, ["<", ">", "≤", "≥"])
    d, closed = ("+" if op in (">", "≥") else "-"), op in ("≤", "≥")
    flip = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}
    oc = {"<": "≤", ">": "≥", "≤": "<", "≥": ">"}
    alt = f"Number line from {b - 6} to {b + 6}. A {'closed (filled)' if closed else 'open'} circle at {b} with an arrow pointing {'right' if d == '+' else 'left'}."
    return Q("Write the inequality shown by the graph. Use x as the variable.", ineq_text("x", op, b), [f"The circle is at {b}.", f"{'Closed circle: include' if closed else 'Open circle: do not include'} {b}.",
                                                                                                     f"Arrow points {'right (greater)' if d == '+' else 'left (less)'}.", f"Inequality: x {op} {b}."],
             [ineq_text("x", flip[op], b), ineq_text("x", oc[op], b), ineq_text("x", flip[oc[op]], b)], PY("ineq", ineq=f"x {op} {b}"),
             why=["Reversed the direction of the arrow", "Mixed up open and closed circles", "Reversed the direction and the circle"],
             diagram={"alt": alt, "draw": numline_draw(b - 6, b + 6, ray=(b, d, closed))}, tags=["graph"])


@fam("12", mode="mc")
def s8_choose_graph(r, L):
    b = r.randint(-6, 6)
    op = pick(r, ["<", ">", "≤", "≥"])
    d, closed = ("+" if op in (">", "≥") else "-"), op in ("≤", "≥")
    cands = [(b, d, closed), (b, "-" if d == "+" else "+", closed), (b, d, not closed), (-b if b else b + 2, d, closed)]
    need(len(set(cands)) == 4)
    r.shuffle(cands)
    labs = ["A", "B", "C", "D"]
    graphs = {f"Graph {l}": [str(c[0]), c[1], c[2]] for l, c in zip(labs, cands)}
    ans = [k for k, c in graphs.items() if (int(c[0]), c[1], c[2]) == (b, d, closed)][0]
    alt = "Four number lines. " + " ".join(f"{k}: {'closed' if c[2] else 'open'} circle at {c[0]}, arrow {'right' if c[1] == '+' else 'left'}." for k, c in graphs.items())
    return Q(f"Which graph shows x {op} {b}?", ans, [f"The boundary is {b}.", f"{'Closed' if closed else 'Open'} circle because the symbol is {op}.", f"Shade to the {'right' if d == '+' else 'left'}."],
             options=[(k, k == ans) for k in graphs], chk=PY("ray_match", ineq=f"x {op} {b}", graphs=graphs), mode="mc", tags=["graph"],
             diagram={"alt": alt, "draw": numline_panels([numline_draw(-8, 8, ray=c) for c in cands])})


@fam("012")
def s8_words(r, L):
    v = pick(r, ["a", "h", "s", "p", "t"])
    n = r.randint(5, 80)
    ctx = [(f"You must be at least {n} years old to vote. Let {v} be age.", "≥"), (f"The speed limit is {n} miles per hour; let {v} be a legal speed (not over the limit).", "≤"),
           (f"A ride requires riders taller than {n} inches. Let {v} be a rider's height.", ">"), (f"Fewer than {n} people can fit in the room. Let {v} be the number of people.", "<"),
           (f"A bag can hold no more than {n} pounds. Let {v} be the weight of the bag.", "≤"), (f"You need more than {n} points to win. Let {v} be your points.", ">")]
    t, op = pick(r, ctx)
    oc = {"<": "≤", ">": "≥", "≤": "<", "≥": ">"}
    flip = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}
    return Q(f"Write an inequality: {t}", ineq_text(v, op, n), ["“at least” means ≥; “no more than” or “not over” means ≤; “more than” or “taller than” means >; “fewer than” or “less than” means <.", f"{v} {op} {n}."],
             [ineq_text(v, oc[op], n), ineq_text(v, flip[op], n), ineq_text(v, flip[oc[op]], n)], PY("ineq", ineq=f"{v} {op} {n}", var=v),
             why=["Included or excluded the boundary incorrectly", "Reversed the inequality", ""], tags=["modeling"])


@fam("012")
def s8_check(r, L):
    b = r.randint(-9, 9)
    op = pick(r, ["<", ">", "≤", "≥"])
    t = b + pick(r, [0, 0, 1, -1, 3, -3])
    ok = {"<": t < b, ">": t > b, "≤": t <= b, "≥": t >= b}[op]
    return Q(f"Is {t} a solution of x {op} {b}?", "Yes" if ok else "No", [f"Substitute: {t} {op} {b}.", f"This is {'true' if ok else 'false'}.", f"{'Yes' if ok else 'No'}."],
             ["No" if ok else "Yes"], PY("is_solution", rel=f"x {op} {b}", v=str(t)), mode="sa", why=["Did not check the boundary correctly"])


# ============================================================== S9 / S10 One-step inequalities
def flip_op(op):
    return {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}[op]


def ineq_one(r, L, kind):
    v = pick(r, VARS)
    op = pick(r, ["<", ">", "≤", "≥"])
    x = r.randint(-15, 25) if L else r.randint(1, 25)
    if kind == "add":
        a = nz(r, -20, 20) if L else r.randint(2, 20)
        lhs = f"{v} + {a}" if a > 0 else f"{v} - {-a}"
        rhs = x + a
        st = [f"{'Subtract' if a > 0 else 'Add'} {abs(a)} on both sides.", f"{v} {op} {rhs} {'-' if a > 0 else '+'} {abs(a)}.", f"{v} {op} {x}."]
        wr = [ineq_text(v, op, rhs + a), ineq_text(v, flip_op(op), x), ineq_text(v, op, -x) if x else ineq_text(v, op, a)]
        why = ["Did the same operation instead of the inverse", "Reversed the inequality sign unnecessarily", "Made a sign error"]
        ans_op = op
    else:
        a = r.randint(2, 9) if L == 0 else nz(r, -9, 9)
        need(abs(a) > 1)
        if r.random() < 0.5:
            lhs, rhs = f"{a}{v}", a * x
            st = [f"Divide both sides by {a}.", "Dividing by a negative number reverses the inequality sign." if a < 0 else "Dividing by a positive number keeps the sign.", f"{v} {flip_op(op) if a < 0 else op} {x}."]
        else:
            lhs, rhs = (f"{v}/{a}" if a > 0 else f"{v}/({a})"), x
            x = a * x
            st = [f"Multiply both sides by {a}.", "Multiplying by a negative number reverses the inequality sign." if a < 0 else "Multiplying by a positive number keeps the sign.", f"{v} {flip_op(op) if a < 0 else op} {x}."]
        ans_op = flip_op(op) if a < 0 else op
        wr = [ineq_text(v, op if a < 0 else flip_op(op), x), ineq_text(v, ans_op, -x) if x else ineq_text(v, ans_op, 1), ineq_text(v, ans_op, rhs - a)]
        why = ["Forgot to reverse the sign when dividing or multiplying by a negative" if a < 0 else "Reversed the sign when the number was positive", "Made a sign error", "Subtracted instead of dividing"]
    full = f"{lhs} {op} {rhs}"
    return Q(f"Solve: {full}", ineq_text(v, ans_op, x), st, wr, PY("ineq", ineq=full, var=v), why=why, tags=["misconception"] if kind == "mul" and L else [])


@fam("012")
def s9_solve(r, L):
    return ineq_one(r, L, "add")


@fam("012")
def s10_solve(r, L):
    return ineq_one(r, L, "mul")


@fam("012")
def s9_context(r, L):
    nm = name(r)
    a, b = r.randint(10, 60), r.randint(70, 150)
    return Q(f"{nm} has ${a} and wants to have at least ${b}. Write and solve an inequality for d, the dollars {nm} still needs to save.", f"d ≥ {b - a}",
             [f"{a} + d ≥ {b}.", f"Subtract {a} from both sides.", f"d ≥ {b - a}."], [f"d ≤ {b - a}", f"d ≥ {a + b}", f"d > {b - a}"], PY("ineq", ineq=f"{a} + d ≥ {b}", var="d"),
             why=["Reversed the inequality sign", "Added instead of subtracting", "Used > for “at least”"], tags=["modeling"])


@fam("012")
def s10_context(r, L):
    p, B = r.randint(3, 15), r.randint(40, 200)
    k = B // p
    nm = name(r)
    return Q(f"{nm} has ${B} to spend on shirts that cost ${p} each. Write and solve an inequality for s, the number of shirts. What is the greatest number of shirts {nm} can buy?", str(k),
             [f"{p}s ≤ {B}.", f"Divide by {p}: s ≤ {N(F(B, p))}.", f"s must be a whole number, so the greatest is {k}.", f"Check: {p}({k}) = {p * k} ≤ {B}."],
             [str(k + 1) if p * (k + 1) != B else str(k + 2), N(F(B, p)) if B % p else str(k * 2), str(B - p)], PY("max_int", ineq=f"{p}s ≤ {B}", var="s"),
             why=["Rounded up instead of down", "Did not round to a whole number", "Subtracted instead of dividing"], tags=["modeling", "multistep"])


@fam("2")
def s10_graph(r, L):
    a = nz(r, -6, -2)
    x = r.randint(-6, 6)
    op = pick(r, ["<", ">", "≤", "≥"])
    full = f"{a}x {op} {a * x}"
    ans_op = flip_op(op)
    d, closed = ("+" if ans_op in (">", "≥") else "-"), ans_op in ("≤", "≥")
    alt = f"Number line from {x - 6} to {x + 6} with a {'closed' if closed else 'open'} circle at {x} and an arrow pointing {'right' if d == '+' else 'left'}."
    return Q(f"The graph shows the solution of an inequality. Which inequality has this solution? Use the graph to choose.", None, []) if False else \
        Q(f"Solve {full}. Then write the inequality shown by the graph of its solution.", f"x {ans_op} {x}", [f"Divide by {a}.", "Reverse the sign because {a} is negative.".format(a=a), f"x {ans_op} {x}.",
                                                                                                        f"Graph: {'closed' if closed else 'open'} circle at {x}, arrow {'right' if d == '+' else 'left'}."],
          [f"x {op} {x}", f"x {ans_op} {-x}" if x else f"x {ans_op} 1", f"x {op} {-x}" if x else f"x {op} -1"], PY("ineq", ineq=full), why=["Forgot to reverse the sign", "Made a sign error", ""],
          diagram={"alt": alt, "draw": numline_draw(x - 6, x + 6, ray=(x, d, closed))}, tags=["graph", "misconception"])


SKILLS = {
    1: dict(name="Properties of Numbers", std=["6.EE.A.3", "7.EE.A.1"], fams=[s1_name, s1_missing, s1_mental], extra=[err_of(s1_mental), open_of(s1_mental)]),
    2: dict(name="The Distributive Property", std=["6.EE.A.3", "7.EE.A.1"], fams=[s2_expand, s2_factor, s2_area], extra=[err_of(s2_expand), open_of(s2_expand), select_of(s2_expand)]),
    3: dict(name="Simplifying Variable Expressions", std=["7.EE.A.1", "6.EE.A.4"], fams=[s3_combine, s3_perimeter, s3_equiv], extra=[err_of(s3_combine), open_of(s3_combine), select_of(s3_combine)]),
    4: dict(name="Variables and Equations", std=["6.EE.B.5", "6.EE.B.7"], fams=[s4_is_solution, s4_classify, s4_write], extra=[err_of(s4_write), open_of(s4_is_solution)]),
    5: dict(name="Solving Equations by Adding or Subtracting", std=["6.EE.B.7"], fams=[s5_solve, s5_context], extra=[err_of(s5_solve), open_of(s5_solve), select_of(s5_solve)]),
    6: dict(name="Solving Equations by Multiplying or Dividing", std=["6.EE.B.7"], fams=[s6_solve, s6_context], extra=[err_of(s6_solve), open_of(s6_solve), select_of(s6_solve)]),
    7: dict(name="Guess, Check, and Revise", std=["MP.1", "7.EE.B.3"], fams=[s7_sum_diff, s7_tickets, s7_legs], extra=[err_of(s7_tickets), open_of(s7_sum_diff)]),
    8: dict(name="Inequalities and Their Graphs", std=["6.EE.B.8"], fams=[s8_from_graph, s8_choose_graph, s8_words, s8_check], extra=[err_of(s8_words), open_of(s8_words), err_of(s8_from_graph)]),
    9: dict(name="Solving One-Step Inequalities by Adding or Subtracting", std=["6.EE.B.8", "7.EE.B.4b"], fams=[s9_solve, s9_context], extra=[err_of(s9_solve), open_of(s9_solve), select_of(s9_solve)]),
    10: dict(name="Solving One-Step Inequalities by Multiplying or Dividing", std=["7.EE.B.4b"], fams=[s10_solve, s10_context, s10_graph], extra=[err_of(s10_solve), open_of(s10_solve), select_of(s10_solve)]),
}
