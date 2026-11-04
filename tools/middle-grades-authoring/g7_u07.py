"""Grade 7 Unit 7 — Solving Equations and Inequalities (solving-equations-inequalities)."""
from glib import *

UNIT_ID = "solving-equations-inequalities"
ABBR = "sei"
VARS = ["x", "n", "y", "m", "k", "a", "t", "p"]


def ans_wr(v, x, ws):
    return f"{v} = {mixed(x) if F(x).denominator > 1 else N(x)}", [f"{v} = {mixed(w) if F(w).denominator > 1 else N(w)}" for w in ws]


# ============================================================== S1 Two-step equations
@fam("012")
def s1_solve(r, L):
    v = pick(r, VARS)
    x = r.randint(1, 12) if L == 0 else nz(r, -15, 15)
    a = r.randint(2, 9) if L == 0 else nz(r, -9, 9)
    need(abs(a) > 1)
    b = r.randint(1, 20) if L == 0 else nz(r, -25, 25)
    form = pick(r, ["ax+b", "x/a+b"] if L else ["ax+b"])
    if form == "ax+b":
        rhs = a * x + b
        eq = f"{lin((a, v), (b, ''))} = {rhs}" if not (L == 2 and r.random() < 0.4) else f"{rhs} = {lin((b, ''), (a, v))}"
        st = [f"{'Subtract' if b > 0 else 'Add'} {abs(b)} on both sides: {coef_text(a, v)} = {rhs - b}.", f"Divide both sides by {a}.", f"{v} = {x}.", f"Check: {a}({x}) {sgn(b)} = {rhs}."]
        a_, w = ans_wr(v, x, [F(rhs + b, a), F(rhs, a) - b, F(rhs - b) * a if L == 0 else -x])
        why = ["Added instead of subtracting the constant", "Divided before subtracting the constant", "Multiplied instead of dividing" if L == 0 else "Made a sign error"]
    else:
        x = a * nz(r, -9, 9)
        rhs = F(x, a) + b
        eq = f"{v}/{a} {sgn(b)} = {N(rhs)}" if a > 0 else f"{v}/({a}) {sgn(b)} = {N(rhs)}"
        st = [f"{'Subtract' if b > 0 else 'Add'} {abs(b)} on both sides: {v}/{par(a)} = {N(rhs - b)}." if False else f"{'Subtract' if b > 0 else 'Add'} {abs(b)} on both sides.", f"Multiply both sides by {a}.", f"{v} = {x}.", "Check by substituting."]
        a_, w = ans_wr(v, x, [(rhs + b) * a, rhs * a - b, F(rhs - b, a)])
        why = ["Added instead of subtracting the constant", "Multiplied before subtracting the constant", "Divided instead of multiplying"]
    return Q(f"Solve: {eq}", a_, st, w, EQ(eq, v), why=why)


@fam("012")
def s1_context(r, L):
    nm = name(r)
    fee, rate, n = r.randint(5, 40), r.randint(2, 15), r.randint(2, 12)
    tot = fee + rate * n
    ctx = pick(r, [(f"A gym charges a ${fee} sign-up fee plus ${rate} per class. {nm} paid ${tot}. How many classes did {nm} take?", "c", f"{rate}c + {fee} = {tot}"),
                   (f"A taxi charges ${fee} plus ${rate} per mile. A ride cost ${tot}. How many miles was the ride?", "m", f"{rate}m + {fee} = {tot}"),
                   (f"{nm} has ${fee} and saves ${rate} each week. After how many weeks will {nm} have ${tot}?", "w", f"{fee} + {rate}w = {tot}")])
    t, v, eq = ctx
    return Q(t, str(n), [f"Equation: {eq}.", f"Subtract {fee}: {rate}{v} = {tot - fee}.", f"Divide by {rate}: {v} = {n}.", f"Check: {fee} + {rate}({n}) = {tot}."],
             [str(F(tot + fee, rate)) if (tot + fee) % rate == 0 else str(tot - fee), N(F(tot, rate)) if tot % rate == 0 else str(n + 1), str((tot - fee) * rate)], PY("eq_val", eq=eq, var=v),
             why=["Added the fee instead of subtracting it", "Forgot to subtract the fee", "Multiplied instead of dividing"], tags=["modeling"])


# ============================================================== S2 Multi-step equations
@fam("012")
def s2_solve(r, L):
    v = pick(r, VARS)
    x = r.randint(1, 10) if L == 0 else nz(r, -12, 12)
    if L == 0:
        a, b, c = r.randint(2, 6), r.randint(1, 5), r.randint(1, 12)
        lhs = f"{a}{v} + {b}{v} + {c}"
        rhs = (a + b) * x + c
        st = [f"Combine like terms: {a + b}{v} + {c} = {rhs}.", f"Subtract {c}: {a + b}{v} = {rhs - c}.", f"Divide by {a + b}: {v} = {x}.", "Check by substituting."]
        w = [F(rhs - c, a), F(rhs + c, a + b), F(rhs - c, a * b)]
        why = ["Did not combine all the like terms", "Added the constant instead of subtracting", "Multiplied the coefficients"]
    else:
        a, b, c = nz(r, -6, 6), nz(r, -8, 8), nz(r, -9, 9)
        need(abs(a) > 1)
        lhs = f"{a}({lin((1, v), (b, ''))}) {sgn(c)}{'' if L == 1 else ''}"
        d = 0
        if L == 2:
            d = nz(r, -5, 5)
            need(a + d != 0)
            lhs = f"{a}({lin((1, v), (b, ''))}) {'+' if d > 0 else '-'} {coef_text(abs(d), v)} {sgn(c)}"
        rhs = (a + d) * x + a * b + c
        st = [f"Distribute: {lin((a, v), (a * b, ''))}{' ' + ('+' if d > 0 else '-') + ' ' + coef_text(abs(d), v) if d else ''} {sgn(c)} = {rhs}.", f"Combine like terms: {lin((a + d, v), (a * b + c, ''))} = {rhs}.",
              f"{'Subtract' if a * b + c > 0 else 'Add'} {abs(a * b + c)}: {coef_text(a + d, v)} = {rhs - a * b - c}.", f"Divide by {a + d}: {v} = {x}."]
        w = [F(rhs - b - c, a + d), F(rhs - a * b + c, a + d), -x if x else F(1)]
        why = ["Multiplied only the first term when distributing", "Made a sign error with the constant", "Made a sign error at the last step"]
    eq = f"{lhs} = {rhs}"
    a_, ww = ans_wr(v, x, w)
    return Q(f"Solve: {eq}", a_, st, ww, EQ(eq, v), why=why, tags=["multistep"])


@fam("12")
def s2_perimeter(r, L):
    x = r.randint(2, 15)
    a, b = r.randint(1, 4), r.randint(1, 9)
    P_ = 2 * (a * x + b) + 2 * x
    return Q(f"A rectangle has length ({coef_text(a, 'x')} + {b}) cm and width x cm. Its perimeter is {P_} cm. Find x.", f"x = {x}",
             [f"2({coef_text(a, 'x')} + {b}) + 2x = {P_}.", f"{2 * a}x + {2 * b} + 2x = {P_}.", f"{2 * a + 2}x = {P_ - 2 * b}.", f"x = {x}."],
             [f"x = {N(F(P_ - b, a + 1))}", f"x = {N(F(P_ - 2 * b, 2 * a))}", f"x = {N(F(P_, 2 * a + 2))}"], EQ(f"2({a}x + {b}) + 2x = {P_}"),
             why=["Used only one length and one width", "Forgot the two widths", "Forgot to subtract the constant"], tags=["connections", "multistep"])


# ============================================================== S3 Fractions and decimals
@fam("012")
def s3_solve(r, L):
    v = pick(r, VARS)
    if r.random() < 0.5:
        d = pick(r, [2, 3, 4, 5, 6])
        n = r.randint(1, d - 1)
        c = F(n, d)
        x = F(r.randint(1, 10) * d) * (pick(r, [1, -1]) if L == 2 else 1)
        b = F(r.randint(1, 9), pick(r, [1, 2, 4])) if L else F(r.randint(1, 9))
        rhs = c * x + b
        eq = f"({N(c)}){v} + {N(b)} = {N(rhs)}"
        st = [f"Subtract {N(b)}: ({N(c)}){v} = {N(rhs - b)}.", f"Multiply by the reciprocal {N(1 / c)}.", f"{v} = {N(x)}.", f"(Or multiply every term by the LCD to clear fractions first.)"]
        w = [(rhs + b) / c, (rhs - b) * c, rhs / c - b]
    else:
        c = F(r.randint(2, 50), 10)
        x = F(r.randint(1, 40) * (1 if L < 2 else pick(r, [1, -1])), pick(r, [1, 2, 10] if L else [1]))
        b = F(r.randint(1, 90), 10)
        rhs = c * x + b
        need(is_term(rhs) and c != 1)
        eq = f"{D(c)}{v} + {D(b)} = {D(rhs)}"
        st = [f"Subtract {D(b)}: {D(c)}{v} = {D(rhs - b)}.", f"Divide by {D(c)} (or multiply every term by 10 first).", f"{v} = {D(x)}.", "Check by substituting."]
        w = [(rhs + b) / c, (rhs - b) * c, rhs / c - b]
    a_, ww = ans_wr(v, x, w)
    return Q(f"Solve: {eq}", a_, st, ww, EQ(eq, v), why=["Added the constant instead of subtracting", "Multiplied by the coefficient instead of dividing", "Divided before subtracting"], tags=["multistep"])


@fam("12")
def s3_clear(r, L):
    v = pick(r, VARS)
    d1, d2 = r.sample([2, 3, 4, 5, 6], 2)
    x = F(d1 * d2 * r.randint(1, 4))
    a, b = r.randint(1, d1 - 1) if d1 > 2 else 1, r.randint(1, d2 - 1) if d2 > 2 else 1
    rhs = F(a, d1) * x + F(b, d2) * x
    eq = f"({a}/{d1}){v} + ({b}/{d2}){v} = {N(rhs)}"
    lcd = d1 * d2 // math.gcd(d1, d2)
    return Q(f"Solve: {eq}", f"{v} = {N(x)}", [f"Multiply every term by the LCD, {lcd}.", f"{lcd * a // d1}{v} + {lcd * b // d2}{v} = {N(rhs * lcd)}.", f"{lcd * a // d1 + lcd * b // d2}{v} = {N(rhs * lcd)}.", f"{v} = {N(x)}."],
             [f"{v} = {mixed(rhs / F(a + b, d1 + d2))}", f"{v} = {mixed(rhs * lcd)}", f"{v} = {mixed(rhs / (F(a, d1) * F(b, d2)))}"], EQ(eq, v),
             why=["Added the fractions by adding numerators and denominators", "Multiplied only the right side by the LCD", "Multiplied the coefficients instead of adding"], tags=["multistep"])


# ============================================================== S4 Write an Equation
@fam("012")
def s4_word(r, L):
    nm = name(r)
    x = r.randint(3, 30)
    k, c = r.randint(2, 5), r.randint(2, 20)
    ctx = [(f"Twice a number increased by {c} is {2 * x + c}. Find the number.", f"2n + {c} = {2 * x + c}", "n", x),
           (f"{nm} is {k} times as old as her cousin. The sum of their ages is {(k + 1) * x}. How old is the cousin?", f"{k}c + c = {(k + 1) * x}", "c", x),
           (f"The sum of three consecutive integers is {3 * x + 3}. What is the smallest integer?", f"n + (n + 1) + (n + 2) = {3 * x + 3}", "n", x)]
    if L == 2:
        y = r.randint(2, 9)
        ctx += [(f"A rectangle's length is {y} more than twice its width. Its perimeter is {2 * (2 * x + y) + 2 * x}. Find the width.", f"2(2w + {y}) + 2w = {2 * (2 * x + y) + 2 * x}", "w", x),
                (f"{nm} has ${c + k * x * 2} and spends ${2 * k} per day. {name(r)} has ${c} and saves ${k} per day. After how many days will they have the same amount?", f"{c + k * x * 2} - {2 * k}d = {c} + {k}d", "d", F(2 * k * x, 3 * k))]
    t, eq, v, sol = pick(r, ctx if L else ctx[:2])
    need(F(sol).denominator == 1)
    return Q(t, N(sol), [f"Let {v} be the unknown.", f"Equation: {eq}.", f"Solve: {v} = {N(sol)}.", "Check the answer in the words of the problem."],
             [N(sol + 1), N(sol * 2), N(F(sol) + c)], PY("eq_val", eq=eq, var=v), why=["Found the next integer instead", "Doubled the answer", "Added the constant instead of subtracting"], tags=["modeling"])


@fam("012", mode="mc")
def s4_which_eq(r, L):
    x = r.randint(3, 20)
    a, b = r.randint(2, 9), r.randint(3, 30)
    good = f"{a}n - {b} = {a * x - b}"
    opts = [(good, True), (f"{b} - {a}n = {a * x - b}", False), (f"{a}(n - {b}) = {a * x - b}", False), (f"n - {a * b} = {a * x - b}", False)]
    r.shuffle(opts)
    return Q(f"Which equation represents “{b} less than {a} times a number is {a * x - b}”?", good, ["“times a number” → an; “less than” subtracts from that product.", f"{good}."], options=opts,
             chk=PY("eq_same", eq=good, var="n"), mode="mc", tags=["modeling"])


# ============================================================== S5 Variables on both sides
@fam("012")
def s5_solve(r, L):
    v = pick(r, VARS)
    x = r.randint(1, 12) if L == 0 else nz(r, -12, 12)
    a, c = r.sample(range(2, 12), 2) if L == 0 else (nz(r, -9, 9), nz(r, -9, 9))
    need(a != c)
    b = r.randint(1, 20) if L == 0 else nz(r, -20, 20)
    d = a * x + b - c * x
    lhs = lin((a, v), (b, ""))
    rhs = lin((c, v), (d, ""))
    if L == 2:
        k = r.randint(2, 4)
        lhs = f"{k}({lin((a, v), (b, ''))})"
        d = k * (a * x + b) - c * x
        rhs = lin((c, v), (d, ""))
        a, b = k * a, k * b
    eq = f"{lhs} = {rhs}"
    st = ([f"Distribute: {lin((a, v), (b, ''))} = {rhs}."] if L == 2 else []) + [f"{'Subtract' if c > 0 else 'Add'} {coef_text(abs(c), v)} on both sides: {lin((a - c, v), (b, ''))} = {d}.",
                                                                              f"{'Subtract' if b > 0 else 'Add'} {abs(b)}: {coef_text(a - c, v)} = {d - b}.", f"Divide by {a - c}: {v} = {x}.", "Check in the original equation."]
    w = [F(d - b, a + c) if a + c else F(x + 1), F(d + b, a - c), F(d - b, c - a)]
    a_, ww = ans_wr(v, x, w)
    return Q(f"Solve: {eq}", a_, st, ww, EQ(eq, v), why=["Added the variable terms instead of subtracting", "Added the constant instead of subtracting", "Made a sign error when collecting variable terms"], tags=["multistep"])


@fam("12")
def s5_special(r, L):
    v = pick(r, VARS)
    a, b = r.randint(2, 7), r.randint(1, 9)
    k = r.randint(2, 4)
    kind = pick(r, ["none", "all", "one"])
    if kind == "all":
        eq = f"{k}({lin((a, v), (b, ''))}) = {lin((k * a, v), (k * b, ''))}"
        ans = "infinitely many solutions"
    elif kind == "none":
        eq = f"{k}({lin((a, v), (b, ''))}) = {lin((k * a, v), (k * b + r.randint(1, 5), ''))}"
        ans = "no solution"
    else:
        x = nz(r, -8, 8)
        c = k * a + pick(r, [1, -1, 2])
        eq = f"{k}({lin((a, v), (b, ''))}) = {lin((c, v), (k * a * x + k * b - c * x, ''))}"
        ans = f"{v} = {x}"
    others = [o for o in ["no solution", "infinitely many solutions", f"{v} = 0"] if o != ans]
    return Q(f"Solve: {eq}. If there is no solution or infinitely many solutions, say so.", ans, ["Distribute and collect the variable terms on one side.",
                                                                                              "If the variables cancel: a true statement means infinitely many solutions; a false statement means no solution.", f"Result: {ans}."],
             others, EQ(eq, v), why=["Thought the variables canceling means the answer is 0"] * len(others), tags=["reasoning"])


@fam("12")
def s5_context(r, L):
    a, b = r.randint(20, 60), r.randint(5, 15)
    c = r.randint(2, 6)
    d = b + c * r.randint(2, 10)
    x = F(a, d - b) * 0
    m = r.randint(2, 15)
    fee1, rate1 = r.randint(20, 60), r.randint(2, 6)
    rate2 = rate1 + r.randint(1, 5)
    fee2 = fee1 - (rate2 - rate1) * m
    need(fee2 > 0)
    return Q(f"Gym A charges ${fee1} plus ${rate1} per visit. Gym B charges ${fee2} plus ${rate2} per visit. After how many visits do the gyms cost the same?", f"{m} visits",
             [f"{fee1} + {rate1}v = {fee2} + {rate2}v.", f"Subtract {rate1}v: {fee1} = {fee2} + {rate2 - rate1}v.", f"Subtract {fee2}: {fee1 - fee2} = {rate2 - rate1}v.", f"v = {m}."],
             [f"{N(F(fee1 + fee2, rate1 + rate2))} visits" if (fee1 + fee2) % (rate1 + rate2) == 0 else f"{m + 1} visits", f"{fee1 - fee2} visits", f"{N(F(fee1, rate1))} visits" if fee1 % rate1 == 0 else f"{m * 2} visits"],
             PY("eq_val", eq=f"{fee1} + {rate1}v = {fee2} + {rate2}v", var="v"), why=["Added the costs instead of setting them equal", "Forgot to divide by the difference in rates", "Used only one gym"], tags=["modeling"])


# ============================================================== S6 Two-step inequalities
def flip(op):
    return {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}[op]


@fam("012")
def s6_solve(r, L):
    v = pick(r, VARS)
    op = pick(r, ["<", ">", "≤", "≥"])
    x = r.randint(1, 12) if L == 0 else nz(r, -10, 10)
    a = r.randint(2, 9) if L == 0 else nz(r, -8, 8)
    need(abs(a) > 1)
    b = r.randint(1, 20) if L == 0 else nz(r, -20, 20)
    rhs = a * x + b
    full = f"{lin((a, v), (b, ''))} {op} {rhs}"
    ans_op = flip(op) if a < 0 else op
    return Q(f"Solve: {full}", f"{v} {ans_op} {x}", [f"{'Subtract' if b > 0 else 'Add'} {abs(b)}: {coef_text(a, v)} {op} {rhs - b}.",
                                                    f"Divide by {a}." + (" Dividing by a negative reverses the sign." if a < 0 else ""), f"{v} {ans_op} {x}.", f"Check a value, such as {x + (1 if ans_op in ('>', '≥') else -1)}."],
             [f"{v} {op if a < 0 else flip(op)} {x}", f"{v} {ans_op} {N(F(rhs + b, a))}", f"{v} {ans_op} {-x}" if x else f"{v} {ans_op} 1"], PY("ineq", ineq=full, var=v),
             why=["Forgot to reverse the sign when dividing by a negative" if a < 0 else "Reversed the sign when dividing by a positive", "Added the constant instead of subtracting", "Made a sign error"],
             tags=["misconception"] if a < 0 else [])


@fam("012")
def s6_context(r, L):
    nm = name(r)
    have, rate, goal = r.randint(10, 80), r.randint(5, 20), r.randint(150, 400)
    w = math.ceil(F(goal - have, rate))
    need(goal > have)
    return Q(f"{nm} has ${have} and earns ${rate} per hour. {nm} wants at least ${goal}. What is the least whole number of hours {nm} must work?", str(w),
             [f"{have} + {rate}h ≥ {goal}.", f"{rate}h ≥ {goal - have}.", f"h ≥ {mixed(F(goal - have, rate))}.", f"The least whole number is {w}."],
             [str(w - 1) if F(goal - have, rate).denominator > 1 else str(w + 1), str(math.ceil(F(goal, rate))) if math.ceil(F(goal, rate)) != w else str(w + 2), mixed(F(goal - have, rate)) if F(goal - have, rate).denominator > 1 else str(w * 2)],
             PY("min_int", ineq=f"{have} + {rate}h ≥ {goal}", var="h"), why=["Rounded down instead of up", "Ignored the money already saved", "Did not round to a whole number"], tags=["modeling", "multistep"])


@fam("2")
def s6_graph(r, L):
    a = nz(r, -5, 5)
    need(abs(a) > 1)
    x, b = r.randint(-5, 5), nz(r, -9, 9)
    op = pick(r, ["<", ">", "≤", "≥"])
    full = f"{lin((a, 'x'), (b, ''))} {op} {a * x + b}"
    ao = flip(op) if a < 0 else op
    d, closed = ("+" if ao in (">", "≥") else "-"), ao in ("≤", "≥")
    cands = [(x, d, closed), (x, "-" if d == "+" else "+", closed), (x, d, not closed), (-x if x else 2, d, closed)]
    need(len(set(cands)) == 4)
    r.shuffle(cands)
    graphs = {f"Graph {l}": [str(c[0]), c[1], c[2]] for l, c in zip("ABCD", cands)}
    ans = [k for k, c in graphs.items() if (int(c[0]), c[1], c[2]) == (x, d, closed)][0]
    alt = "Four number lines. " + " ".join(f"{k}: {'closed' if c[2] else 'open'} circle at {c[0]}, arrow {'right' if c[1] == '+' else 'left'}." for k, c in graphs.items())
    return Q(f"Which graph shows the solution of {full}?", ans, [f"Solve: x {ao} {x}.", f"{'Closed' if closed else 'Open'} circle at {x}.", f"Arrow to the {'right' if d == '+' else 'left'}."],
             options=[(k, k == ans) for k in graphs], chk=PY("ray_match", ineq=full, graphs=graphs), mode="mc", tags=["graph"],
             diagram={"alt": alt, "draw": numline_panels([numline_draw(-8, 8, ray=c) for c in cands])})


# ============================================================== S7 Transforming Formulas
SIMPLE = [("d = rt", "r", "r = d/t", ["r = dt", "r = t/d", "r = d - t"], ["d", "r", "t"]),
          ("A = lw", "l", "l = A/w", ["l = Aw", "l = w/A", "l = A - w"], ["A", "l", "w"]),
          ("P = 4s", "s", "s = P/4", ["s = 4P", "s = P - 4", "s = 4/P"], ["P", "s"]),
          ("V = Bh", "h", "h = V/B", ["h = VB", "h = B/V", "h = V - B"], ["V", "B", "h"]),
          ("y = x + b", "x", "x = y - b", ["x = y + b", "x = b - y", "x = y/b"], ["y", "x", "b"]),
          ("C = πd", "d", "d = C/π", ["d = Cπ", "d = C - π", "d = π/C"], ["C", "d"])]
FORMS = [("d = rt", "t", "t = d/r", ["t = dr", "t = r/d", "t = d - r"], ["d", "r", "t"]),
         ("A = lw", "w", "w = A/l", ["w = Al", "w = l/A", "w = A - l"], ["A", "l", "w"]),
         ("P = 2l + 2w", "l", "l = (P - 2w)/2", ["l = P - 2w", "l = (P + 2w)/2", "l = P/2 - 2w"], ["P", "l", "w"]),
         ("V = lwh", "h", "h = V/(lw)", ["h = V - lw", "h = Vlw", "h = lw/V"], ["V", "l", "w", "h"]),
         ("I = prt", "r", "r = I/(pt)", ["r = Ipt", "r = I - pt", "r = pt/I"], ["I", "p", "r", "t"]),
         ("y = mx + b", "b", "b = y - mx", ["b = y + mx", "b = (y - x)/m", "b = mx - y"], ["y", "m", "x", "b"]),
         ("y = mx + b", "x", "x = (y - b)/m", ["x = y - b/m", "x = (y + b)/m", "x = m(y - b)"], ["y", "m", "x", "b"]),
         ("C = 2πr", "r", "r = C/(2π)", ["r = 2πC", "r = C - 2π", "r = 2C/π"], ["C", "r"]),
         ("A = (1/2)bh", "h", "h = 2A/b", ["h = A/(2b)", "h = 2Ab", "h = A/b"], ["A", "b", "h"]),
         ("F = 1.8C + 32", "C", "C = (F - 32)/1.8", ["C = F/1.8 - 32", "C = 1.8(F - 32)", "C = (F + 32)/1.8"], ["F", "C"])]


@fam("012")
def s7_solve_for(r, L):
    pool = SIMPLE + FORMS[:2] if L == 0 else FORMS[:8] + SIMPLE[:3] if L == 1 else FORMS[2:]
    f, v, ans, wr, vs = pick(r, pool)
    return Q(f"Solve {f} for {v}.", ans, [f"Isolate {v} using inverse operations.", "Undo addition or subtraction first, then multiplication or division.", f"{ans}."], wr,
             PY("formula", orig=f, target=v, vars=vs), why=["Multiplied instead of dividing", "Divided in the wrong order", "Used the wrong inverse operation"])


@fam("012")
def s7_use(r, L):
    rt, t = r.randint(30, 70), r.randint(2, 8)
    d = rt * t
    l, w = r.randint(3, 20), r.randint(2, 15)
    ctx = [(f"Use t = d/r to find the time to travel {d} miles at {rt} miles per hour.", f"{t} hours", f"{d}/{rt}", [f"{d * rt} hours", f"{d - rt} hours", f"{N(F(rt, d))} hours"]),
           (f"Use w = A/l to find the width of a rectangle with area {l * w} square feet and length {l} feet.", f"{w} feet", f"{l * w}/{l}", [f"{l * w * l} feet", f"{l * w - l} feet", f"{N(F(l, l * w))} feet"])]
    if L:
        P_ = 2 * l + 2 * w
        ctx.append((f"Use l = (P - 2w)/2 to find the length of a rectangle with perimeter {P_} m and width {w} m.", f"{l} meters", f"({P_} - 2*{w})/2", [f"{P_ - 2 * w} meters", f"{N(F(P_ + 2 * w, 2))} meters", f"{N(F(P_, 2)) if P_ % 2 == 0 else l + 1} meters"]))
    t_, ans, ex, wr = pick(r, ctx)
    return Q(t_, ans, ["Substitute the known values.", "Evaluate.", f"{ans}."], wr, V(ex), why=["Multiplied instead of dividing", "Subtracted instead of dividing", "Divided in the wrong order"], tags=["modeling"])


# ============================================================== S8 Simple and Compound Interest
@fam("012")
def s8_simple(r, L):
    p = r.randint(2, 50) * 100
    rate = pick(r, [2, 3, 4, 5, 6]) if L == 0 else pick(r, [F(5, 2), F(7, 2), F(9, 2), 3, 5, F(11, 4)])
    t = r.randint(2, 10) if L < 2 else pick(r, [F(1, 2), F(3, 2), F(5, 2), 2, 4])
    i = p * F(rate) / 100 * t
    need(is_term(i))
    if L == 2 and r.random() < 0.5:
        return Q(f"How much is in an account after {mixed(F(t))} years if ${p:,} earns {D(F(rate))}% simple interest per year?", f"${Rd(p + i, 2)}",
                 [f"I = prt = {p} × {D(F(rate) / 100)} × {D(F(t))}.", f"I = ${Rd(i, 2)}.", f"Balance = {p} + {Rd(i, 2)} = ${Rd(p + i, 2)}."],
                 [f"${Rd(i, 2)}", f"${Rd(p + p * F(rate) * t, 2)}", f"${Rd(p * (1 + F(rate) / 100) ** int(t) if F(t).denominator == 1 else p + i + 1, 2)}"], V(f"{p} + {p}*{D(F(rate))}/100*{D(F(t))}"),
                 why=["Gave only the interest", "Did not change the rate to a decimal", "Used compound interest"], tags=["modeling"])
    return Q(f"Find the simple interest earned on ${p:,} at {D(F(rate))}% per year for {mixed(F(t))} years.", f"${Rd(i, 2)}",
             [f"I = prt.", f"I = {p} × {D(F(rate) / 100)} × {D(F(t))}.", f"I = ${Rd(i, 2)}."], [f"${Rd(p * F(rate) * t, 2)}", f"${Rd(p + i, 2)}", f"${Rd(p * F(rate) / 100, 2)}"],
             V(f"{p}*{D(F(rate))}/100*{D(F(t))}"), why=["Did not change the percent to a decimal", "Gave the balance instead of the interest", "Forgot to multiply by the time"], tags=["modeling"])


@fam("012")
def s8_compound(r, L):
    p = r.randint(5, 50) * 100
    rate = pick(r, [2, 3, 4, 5, 6, 8, 10])
    t = r.randint(2, 3) if L < 2 else r.randint(3, 6)
    bal = p * (1 + F(rate, 100)) ** t
    simple = p + p * F(rate, 100) * t
    return Q(f"${p:,} is invested at {rate}% interest compounded annually. What is the balance after {t} years, to the nearest cent?", f"${Rd(bal, 2)}",
             [f"Balance = p(1 + r)ᵗ.", f"= {p}(1 + {D(F(rate, 100))}){sup(t)}.", f"= {p}({D(1 + F(rate, 100))}){sup(t)}.", f"≈ ${Rd(bal, 2)}."],
             [f"${Rd(simple, 2)}", f"${Rd(p * F(rate, 100) * t, 2)}", f"${Rd(p * (1 + F(rate, 100) * t) ** 1 + p * F(rate, 100) * (t - 1) if False else bal - p, 2)}"], AP(f"{p}*(1 + {rate}/100)^{t}", 2),
             why=["Used simple interest", "Found simple interest only", "Gave only the interest earned"], tags=["modeling", "multistep"])


@fam("12", mode="mc")
def s8_compare(r, L):
    p = r.randint(10, 50) * 100
    rate = pick(r, [3, 4, 5, 6])
    t = r.randint(3, 8)
    s = p * F(rate, 100) * t
    c = p * (1 + F(rate, 100)) ** t - p
    opts = [("Compound interest earns more.", True), ("Simple interest earns more.", False), ("They earn the same amount.", False), ("It depends on the bank.", False)]
    r.shuffle(opts)
    return Q(f"${p:,} is invested for {t} years at {rate}% per year. Which earns more: simple interest or interest compounded annually?", "Compound interest earns more.",
             [f"Simple: ${Rd(s, 2)}.", f"Compound: about ${Rd(c, 2)}.", "Compound interest also earns interest on earlier interest."], options=opts,
             chk=PY("interest_cmp", p=p, rate=rate, t=t), mode="mc", tags=["reasoning"])


SKILLS = {
    1: dict(name="Solving Two-Step Equations", std=["7.EE.B.4a"], fams=[s1_solve, s1_context], extra=[err_of(s1_solve), open_of(s1_solve), select_of(s1_solve)]),
    2: dict(name="Solving Multi-Step Equations", std=["7.EE.B.4a", "8.EE.C.7b"], fams=[s2_solve, s2_perimeter], extra=[err_of(s2_solve), open_of(s2_solve), select_of(s2_solve)]),
    3: dict(name="Multi-Step Equations with Fractions and Decimals", std=["7.EE.B.4a", "7.EE.B.3"], fams=[s3_solve, s3_clear], extra=[err_of(s3_solve), open_of(s3_solve), select_of(s3_solve)]),
    4: dict(name="Write an Equation", std=["7.EE.B.4", "7.EE.B.4a"], fams=[s4_word, s4_which_eq], extra=[err_of(s4_word), open_of(s4_word)]),
    5: dict(name="Solving Equations with Variables on Both Sides", std=["8.EE.C.7"], fams=[s5_solve, s5_special, s5_context], extra=[err_of(s5_solve), open_of(s5_solve), select_of(s5_solve)]),
    6: dict(name="Solving Two-Step Inequalities", std=["7.EE.B.4b"], fams=[s6_solve, s6_context, s6_graph], extra=[err_of(s6_solve), open_of(s6_solve), select_of(s6_solve)]),
    7: dict(name="Transforming Formulas", std=["A-CED.A.4", "7.EE.B.4"], fams=[s7_solve_for, s7_use], extra=[err_of(s7_solve_for), open_of(s7_use)]),
    8: dict(name="Simple and Compound Interest", std=["7.RP.A.3"], fams=[s8_simple, s8_compound, s8_compare], extra=[err_of(s8_simple), open_of(s8_simple)]),
}
