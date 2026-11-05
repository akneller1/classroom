"""Algebra 2 Unit 5 — Radicals and Rational Exponents (radicals-rational-exponents). Top-up families."""
from hslib import *
import math
import pc_u02 as F2

UNIT_ID = "radicals-rational-exponents"
ABBR = "rr"


def ri(r, a, b):
    return rint(r, a, b, True)


SQF = [2, 3, 5, 6, 7, 10, 11]


# ============================================================== S1 Simplifying radicals
@fam("012")
def s1_simp(r, L):
    root = 3 if (L == 2 and r.random() < 0.5) else 2
    k = rint(r, 2, 7 if root == 2 else 4)
    m = pick(r, SQF if root == 2 else [2, 3, 4, 5, 6, 7, 9, 10])
    n_ = k ** root * m
    sym = "√" if root == 2 else "∛"
    v = sp.root(n_, root)
    ans = f"{k}{sym}{m}"
    wr = [f"{k * k if root == 2 else k ** 2}{sym}{m}", f"{m}{sym}{k}", f"{k}{sym}{m * k}" if root == 2 else f"{k * 3}{sym}{m}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Simplify {sym}{n_}.", ans,
             [f"Find the largest perfect {'square' if root == 2 else 'cube'} factor: {n_} = {k ** root} · {m}.", f"{sym}{n_} = {sym}{k ** root} · {sym}{m} = {ans}."],
             wr, H(f"{'sqrt' if root == 2 else 'real_root'}({n_}{'' if root == 2 else ', 3'})"),
             why=[f"Left the perfect {'square' if root == 2 else 'cube'} {'squared' if root == 2 else 'unsimplified'} outside the radical", "Switched the number outside and the number inside", "Did not take the root of the factor correctly"])


# ============================================================== S2 Operations with radical expressions
@fam("012")
def s2_addsub(r, L):
    m = pick(r, [2, 3, 5, 6, 7])
    a, b = rint(r, 1, 4), rint(r, 2, 5)
    c1, c2 = rint(r, 1, 6), ri(r, -6, 6)
    n1, n2 = a * a * m, b * b * m
    v = (c1 * a + c2 * b) * sp.sqrt(m)
    t1 = f"{c1 if c1 != 1 else ''}√{n1}"
    t2 = f"{abs(c2) if abs(c2) != 1 else ''}√{n2}"
    txt = f"{t1} {'+' if c2 > 0 else '-'} {t2}"
    need(v != 0)
    ans = T(v)
    wr = [T((c1 + c2) * sp.sqrt(m)), f"{c1 + c2 if abs(c1 + c2) != 1 else ('' if c1 + c2 == 1 else '-')}√{n1 + n2 if c2 > 0 else abs(n1 - n2)}" if c1 + c2 else "0", T((c1 * a - c2 * b) * sp.sqrt(m))]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Simplify {txt}.", ans, [f"Simplify each radical: √{n1} = {T(sp.sqrt(n1))} and √{n2} = {T(sp.sqrt(n2))}.", "Combine like radicals by adding their coefficients.", f"{ans}."],
             wr, H(f"P('{txt}')"), why=["Combined the coefficients without simplifying the radicals first", "Added the numbers under the radicals", "Made a sign error"])


@fam("012")
def s2_mult(r, L):
    a, b = rint(r, 1, 6), rint(r, 1, 6)
    m, n_ = r.sample([2, 3, 5, 6, 7, 10, 12, 15], 2)
    v = a * b * sp.sqrt(m * n_)
    txt = f"({a if a != 1 else ''}√{m})({b if b != 1 else ''}√{n_})"
    ans = T(v)
    wr = [f"{a * b if a * b != 1 else ''}√{m * n_}" if not sp.sqrt(m * n_).is_Integer and sp.sqrt(m * n_) != sp.sqrt(m * n_).as_coeff_Mul()[1] else T(a * b * (m * n_)), f"{a + b}√{m * n_}", T((a * b) * sp.sqrt(m + n_))]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Multiply and simplify: {txt}.", ans, ["Multiply the coefficients and multiply the radicands.", f"{a * b}√{m * n_}.", f"Simplify: {ans}."],
             wr, H(f"P('{txt}')"), why=["Did not simplify the radical" if wr[0].count("√") else "Forgot to take the square root", "Added the coefficients", "Added the radicands"])


@fam("12")
def s2_rationalize(r, L):
    if L == 1 or r.random() < 0.4:
        m = pick(r, [2, 3, 5, 6, 7])
        c = pick(r, [mm * k for mm in [m] for k in (1, 2, 3, 4)] + [rint(r, 1, 9)])
        txt = f"{c}/(√{m})"
        v = sp.radsimp(c / sp.sqrt(m))
        wr = [f"{c}√{m}", T(sp.Rational(c, m)), T(sp.radsimp(c / sp.sqrt(m) * 2)) if True else ""]
        why = ["Multiplied by √m but did not divide by m", "Dropped the radical", "Multiplied the numerator by √m twice"]
        st = [f"Multiply the numerator and the denominator by √{m}.", f"({c}√{m})/{m}.", f"Simplify: {T(v)}."]
    else:
        a, m, c = rint(r, 2, 7), pick(r, [2, 3, 5, 6, 7]), rint(r, 1, 9)
        need(a * a != m)
        sg = pick(r, [1, -1])
        txt = f"{c}/({a} {'+' if sg > 0 else '-'} √{m})"
        v = sp.radsimp(c / (a + sg * sp.sqrt(m)))
        wr = [T(sp.radsimp(c / (a - sg * sp.sqrt(m)))), T(sp.radsimp(c * (a - sg * sp.sqrt(m)) / (a * a + m))), T(sp.radsimp(c * (a - sg * sp.sqrt(m)) / (a - m)))]
        why = ["Used the wrong sign in the result", "Added a² and m in the denominator", "Forgot to square a in the denominator"]
        st = [f"Multiply by the conjugate ({a} {'-' if sg > 0 else '+'} √{m}) over itself.", f"Denominator: {a}² - {m} = {a * a - m}.", f"Result: {T(v)}."]
    ans = T(v)
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Rationalize the denominator and simplify: {txt}", ans, st, wr, H(f"P('{txt}')"), why=why)


# ============================================================== S3 Rational exponents
@fam("012")
def s3_eval(r, L):
    base_root = pick(r, [(4, 2, 2), (9, 2, 3), (16, 2, 4), (25, 2, 5), (36, 2, 6), (8, 3, 2), (27, 3, 3), (64, 3, 4), (16, 4, 2), (81, 4, 3), (32, 5, 2), (125, 3, 5)])
    b, n_, rt = base_root
    m = rint(r, 1, 3) if L else rint(r, 1, 2)
    if r.random() < 0.35:
        d_ = pick(r, [2, 3, 4, 5])
        b, rt = sp.Rational(b, d_ ** n_), sp.Rational(rt, d_)
    neg = L == 2 and r.random() < 0.6
    e = sp.Rational(-m if neg else m, n_)
    v = sp.sympify(b) ** e
    txt = f"({T(b)})^({T(e)})" if not sp.sympify(b).is_Integer else f"{b}^({T(e)})"
    ans = T(v)
    b = sp.sympify(b)
    wr = [T(b * sp.Rational(m, n_)), T(-b ** sp.Rational(m, n_)) if neg else T(sp.sympify(rt) ** (m + 1)), T(b ** sp.Rational(m, n_)) if neg else T(rt * m)]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Evaluate {txt}.", ans,
             [f"b^(m/n) = (ⁿ√b)ᵐ: the {dict([(2, 'square'), (3, 'cube'), (4, 'fourth'), (5, 'fifth')])[n_]} root of {T(b)} is {T(rt)}.", f"Raise to the power {m}: {T(sp.sympify(rt) ** m)}." + (" A negative exponent means take the reciprocal." if neg else ""), f"{txt} = {ans}."],
             wr, H(f"nsimplify('{T(b)}')**Rational({e.p}, {e.q})"),
             why=["Multiplied the base by the exponent", "Treated the negative exponent as a negative number" if neg else "Raised the root to the wrong power", "Ignored the negative exponent" if neg else "Multiplied the root by the exponent"])


@fam("012")
def s3_simplify(r, L):
    a, b = sp.Rational(rint(r, 1, 5), pick(r, [2, 3, 4])), sp.Rational(rint(r, 1, 5), pick(r, [2, 3, 4, 6]))
    if L == 0:
        d_ = pick(r, [2, 3, 4, 5])
        a, b = sp.Rational(rint(r, 1, 7), d_), sp.Rational(rint(r, 1, 7), d_)
    op = pick(r, ["mul", "div", "pow"])
    if op == "mul":
        txt, v = f"x^({T(a)}) · x^({T(b)})", a + b
        wr = [a * b, a + b + 1, a - b]
        why = ["Multiplied the exponents instead of adding", "Made an error adding the fractions", "Subtracted the exponents"]
    elif op == "div":
        txt, v = f"x^({T(a)}) ÷ x^({T(b)})", a - b
        wr = [a / b, a + b, b - a]
        why = ["Divided the exponents instead of subtracting", "Added the exponents", "Subtracted in the wrong order"]
    else:
        k = rint(r, 2, 4)
        txt, v = f"(x^({T(a)}))^{k}", a * k
        wr = [a + k, a / k, a ** k]
        why = ["Added the exponents instead of multiplying", "Divided the exponent by the power", "Raised the exponent to the power"]
    fmt_ = lambda e: "1" if e == 0 else "x" if e == 1 else f"x^({T(e)})" if e.q != 1 else "x" + str(int(e)).translate(SUP)
    ans = fmt_(v)
    wrs = [fmt_(sp.nsimplify(w)) for w in wr]
    need(len(set(wrs) | {ans}) == 4 and v != 0)
    return Q(f"Simplify {txt}. Assume x > 0.", ans, ["Use the exponent rules: xᵃ·xᵇ = xᵃ⁺ᵇ, xᵃ ÷ xᵇ = xᵃ⁻ᵇ, (xᵃ)ᵏ = xᵃᵏ.", f"The exponent is {T(v)}.", f"{ans}."],
             wrs, PY("pos_equiv", expr=txt.replace("·", "*").replace("÷", "/")), why=why)


# ============================================================== S4 Converting between radicals and exponents
@fam("012")
def s4_convert(r, L):
    n_ = pick(r, [2, 3, 4, 5])
    m = rint(r, 1, 4) if L else rint(r, 1, 2)
    need(math.gcd(m, n_) == 1)
    var = pick(r, ["x", "y", "a", "b", "m"])
    coef = pick(r, ["", "", "2", "3", "5", "4"])
    direction = pick(r, ["to_exp", "to_rad"])
    rad = ("√" if n_ == 2 else "∛" if n_ == 3 else f"{n_}√") if True else ""
    if n_ in (2, 3):
        rtxt = f"{rad}x" if m == 1 else f"{rad}(x{str(m).translate(SUP)})"
    else:
        rtxt = f"(x{str(m).translate(SUP) if m > 1 else ''})^(1/{n_})"
    etxt = f"x^({T(sp.Rational(m, n_))})"
    if n_ > 3:
        direction = "to_exp_word"
    if direction == "to_rad":
        q, ans = f"Write {etxt} in radical form. Assume x > 0.", rtxt
        wr = [f"{'√' if m == 2 else '∛' if m == 3 else ('√' if n_ == 2 else '∛')}(x{str(n_).translate(SUP)})" if m in (2, 3) else f"{rad}(x{str(m + 1).translate(SUP)})",
              f"x{str(m).translate(SUP) if m > 1 else ''}/{n_}", f"{n_}x{str(m).translate(SUP) if m > 1 else ''}"]
        why = ["Switched the index and the power", "Divided by the index instead of taking a root", "Multiplied by the index"]
        need(n_ in (2, 3))
    else:
        root_word = {2: "square", 3: "cube", 4: "fourth", 5: "fifth"}[n_]
        src = rtxt if n_ in (2, 3) else f"the {root_word} root of x{str(m).translate(SUP) if m > 1 else ''}"
        q, ans = f"Write {src} using a rational exponent. Assume x > 0.", etxt
        wr = [f"x^({T(sp.Rational(n_, m))})", f"x^({m * n_})" if m * n_ > 1 else "x^(2)", f"x^({T(sp.Rational(m, n_ + 1))})" if True else ""]
        why = ["Put the index in the numerator", "Multiplied the power by the index", "Used the wrong index"]
    sub = lambda t_: coef + t_.replace("x", var) if t_.startswith(("x", "√", "∛", "(")) else t_.replace("x", var)
    q = q.replace(rtxt, sub(rtxt)).replace(etxt, sub(etxt)).replace("the " + (root_word if direction != "to_rad" else "") + " root of x", "the " + (root_word if direction != "to_rad" else "") + " root of " + var).replace("Assume x > 0", f"Assume {var} > 0")
    if coef and direction != "to_rad" and n_ > 3:
        q = q.replace("Write the", f"Write {coef} times the")
    ans, wr, etxt = sub(ans), [sub(w) for w in wr], sub(etxt)
    need(len(set(wr) | {ans}) == 4)
    return Q(q, ans, ["ⁿ√(xᵐ) = x^(m/n): the power goes in the numerator and the index in the denominator.", f"{ans}."], wr,
             PY("pos_equiv", expr=etxt), why=why)


# ============================================================== S5/S6 Solving radical equations, extraneous solutions
@fam("012")
def s5_solve(r, L):
    a = ri(r, -5, 5) if L else rint(r, 1, 5)
    c = rint(r, 2, 9)
    x0 = sp.Rational(c * c - rint(r, -9, 9), 1)
    b = c * c - a * x0
    if L == 0:
        need(b % 1 == 0)
    inner = T(a * x + b)
    k = rint(r, 0, 6) if L == 2 else 0
    txt = f"√({inner}) {'+' if k else ''} {k if k else ''}".strip().replace("+ ", "+ ") + f" = {c + k}"
    txt = txt.replace("  ", " ")
    ans = f"x = {T(x0)}"
    wr = [f"x = {T(sp.Rational(c - b, a))}", f"x = {T(sp.Rational((c + k) ** 2 - b, a))}" if k else f"x = {T(sp.Rational(c * c + b, a))}", f"x = {T(sp.Rational(c * c, a))}" if b else f"x = {T(sp.Rational(c, a) * 2)}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve {txt}.", ans, [("Subtract " + str(k) + " from both sides. " if k else "") + f"Square both sides: {inner} = {c * c}.", f"Solve: x = {T(x0)}.", "Check in the original equation: it works."],
             wr, H(f"solve(Eq(P('{txt.split(' = ')[0]}'), {c + k}), x)", "set"),
             why=["Did not square the right side", "Squared before isolating the radical" if k else "Added the constant instead of subtracting", "Ignored the constant inside the radical"])


@fam("012")
def s6_extraneous(r, L):
    # √(x + a) = x + b with roots of (x + b)² = x + a: pick one valid root u (u + b ≥ 0) and one extraneous v (v + b < 0)
    u = rint(r, -3, 8)
    b = rint(r, -6, 4)
    need(u + b > 0)
    v = 1 - 2 * b - u             # sum of roots of x² + (2b - 1)x + (b² - a) = 0 is 1 - 2b
    need(v + b < 0 and u != v)
    a = (u + b) ** 2 - u
    need(a == (v + b) ** 2 - v)
    lhs = f"√({T(x + a)})" if a else "√x"
    rhs = T(x + b)
    ask = pick(r, ["solve", "which"] if L else ["solve"])
    if ask == "solve":
        ans = f"x = {u}"
        wr = [f"x = {u} or x = {v}", f"x = {v}", "no solution"]
        why = ["Did not check for extraneous solutions", "Kept the extraneous solution and rejected the real one", "Rejected both solutions"]
        return Q(f"Solve {lhs} = {rhs}. Check for extraneous solutions.", ans,
                 [f"Square both sides: {T(x + a)} = {T(sp.expand((x + b) ** 2))}.", f"Solve: x = {u} or x = {v}.", f"Check: x = {v} makes the right side {v + b} < 0, so it is extraneous.", f"{ans}."],
                 wr, H(f"solve(Eq(P('{lhs}'), P('{rhs}')), x)", "set"), why=why)
    return Q(f"Squaring both sides of {lhs} = {rhs} gives the solutions x = {min(u, v)} and x = {max(u, v)}. Which one is extraneous?", f"x = {v}",
             [f"Substitute each value into the original equation.", f"x = {u}: both sides equal {u + b}. x = {v}: the left side is {abs(v + b)} but the right side is {v + b}.", f"x = {v} is extraneous."],
             [f"x = {u}", "neither", "both"], PY("extraneous_root", lhs=lhs, rhs=rhs, cands=[u, v]),
             why=["Chose the valid solution", "Did not substitute into the original equation", "Thought every squared solution fails"])


# ============================================================== S7/S8 Square-root and cube-root functions, transformations
def rad_fn(a, h_, k_, kind):
    sym = "√" if kind == "sqrt" else "∛"
    s = "" if a == 1 else "-" if a == -1 else str(a)
    inner = "x" if h_ == 0 else f"(x {'-' if h_ > 0 else '+'} {abs(h_)})"
    return f"{s}{sym}{inner}" + ("" if k_ == 0 else f" {'+' if k_ > 0 else '-'} {abs(k_)}")


@fam("012")
def s7_domain_range(r, L):
    a = ri(r, -3, 3) if L else pick(r, [1, 2, -1])
    h_, k_ = rint(r, -7, 7), rint(r, -7, 7)
    kind = pick(r, ["sqrt", "cbrt"]) if L == 2 else "sqrt"
    ftxt = rad_fn(a, h_, k_, kind)
    ask = pick(r, ["domain", "range"])
    if kind == "cbrt":
        ans = "(-∞, ∞)"
        wr = [set_text(sp.Interval(h_, sp.oo)), set_text(sp.Interval(k_, sp.oo)), set_text(sp.Interval(-sp.oo, k_))]
        why = ["Treated the cube root like a square root", "Used the shift as a starting value", "Used the vertical shift as a bound"]
        code = "Interval(-oo, oo)"
    elif ask == "domain":
        ans = set_text(sp.Interval(h_, sp.oo))
        wr = [set_text(sp.Interval(-h_, sp.oo)) if h_ else set_text(sp.Interval.open(0, sp.oo)), set_text(sp.Interval(k_, sp.oo)) if k_ != h_ else "(-∞, ∞)", set_text(sp.Interval(-sp.oo, h_))]
        why = ["Used the opposite sign of the horizontal shift", "Used the vertical shift", "Reversed the inequality"]
        code = f"ineq_set('{T(x - h_)} ≥ 0')"
    else:
        rng = sp.Interval(k_, sp.oo) if a > 0 else sp.Interval(-sp.oo, k_)
        ans = set_text(rng)
        wr = [set_text(sp.Interval(-sp.oo, k_) if a > 0 else sp.Interval(k_, sp.oo)), set_text(sp.Interval(h_, sp.oo)) if h_ != k_ else "(-∞, ∞)", "(-∞, ∞)" if h_ != k_ else set_text(sp.Interval.open(k_, sp.oo))]
        why = ["Ignored the reflection from the negative coefficient" if a < 0 else "Reversed the direction of the range", "Used the horizontal shift", "Thought the range is all real numbers"]
        code = f"__import__('sympy').calculus.util.function_range(P('{ftxt}'), x, Interval({h_}, oo))"
    need(len(set(wr) | {ans}) == 4)
    nm = "domain" if (ask == "domain" or kind == "cbrt") and kind != "cbrt" else ask
    return Q(f"Find the {nm} of f(x) = {ftxt}. Use interval notation.", ans,
             [f"The parent function is y = {'√x' if kind == 'sqrt' else '∛x'}.", f"The graph starts at ({h_}, {k_})" + (" and continues in both directions." if kind == "cbrt" else f" and goes {'up' if a > 0 else 'down'} to the right."), f"{nm.capitalize()}: {ans}."],
             wr, H(code, "interval"), why=why)


@fam("012")
def s8_write(r, L):
    kind = pick(r, ["sqrt", "cbrt"])
    h_, k_ = ri(r, -6, 6), rint(r, -8, 8)
    a = 1 if L == 0 else pick(r, [1, 2, 3, -1, -2])
    steps, desc = [], []
    if a == -1:
        desc.append("reflected across the x-axis")
    elif a != 1:
        desc.append(f"vertically stretched by a factor of {abs(a)}" + (" and reflected across the x-axis" if a < 0 else ""))
    desc.append(f"shifted {abs(h_)} unit{'s' if abs(h_) != 1 else ''} {'right' if h_ > 0 else 'left'}")
    if k_:
        desc.append(f"shifted {abs(k_)} unit{'s' if abs(k_) != 1 else ''} {'up' if k_ > 0 else 'down'}")
    ans = "g(x) = " + rad_fn(a, h_, k_, kind)
    wr = ["g(x) = " + rad_fn(a, -h_, k_, kind), "g(x) = " + rad_fn(a, k_, h_, kind) if k_ and k_ != h_ else "g(x) = " + rad_fn(a, h_, h_, kind), "g(x) = " + rad_fn(-a, h_, k_, kind)]
    need(len(set(wr) | {ans}) == 4)
    parent = "√x" if kind == "sqrt" else "∛x"
    return Q(f"The graph of f(x) = {parent} is " + ", then ".join(desc) + ". Write an equation for the new function g.", ans,
             ["A horizontal shift of h units right replaces x with (x - h).", "A vertical shift adds k; a stretch or reflection multiplies the function.", f"{ans}."],
             wr, H(f"P('{rad_fn(a, h_, k_, kind)}')"), why=["Used the wrong direction for the horizontal shift", "Switched the horizontal and vertical shifts", "Missed the reflection" if a < 0 else "Added a reflection that is not there"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Simplifying radicals", fams=[s1_simp], extra=[err_of(s1_simp), open_of(s1_simp), select_of(s1_simp)]),
    2: dict(name="Operations with radical expressions", fams=[s2_addsub, s2_mult, s2_rationalize], extra=[err_of(s2_addsub), err_of(s2_mult), open_of(s2_mult)]),
    3: dict(name="Rational exponents", fams=[s3_eval, s3_simplify], extra=[err_of(s3_eval), err_of(s3_simplify), open_of(s3_eval)]),
    4: dict(name="Converting between radicals and exponents", fams=[s4_convert, s3_eval], extra=[err_of(s4_convert), open_of(s3_eval)]),
    5: dict(name="Solving radical equations", fams=[s5_solve], extra=[err_of(s5_solve), open_of(s5_solve)]),
    6: dict(name="Extraneous solutions", fams=[s6_extraneous], extra=[err_of(s6_extraneous), open_of(s6_extraneous)]),
    7: dict(name="Graphing square-root and cube-root functions", fams=[s7_domain_range], extra=[err_of(s7_domain_range), open_of(s7_domain_range)]),
    8: dict(name="Radical function transformations", fams=[s8_write, rr(F2.s6_write)], extra=[err_of(s8_write), open_of(s8_write)]),
}
