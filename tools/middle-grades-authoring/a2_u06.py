"""Algebra 2 Unit 6 — Exponential and Logarithmic Functions (exponential-logarithmic-functions). Top-up families."""
from hslib import *
import math
import pc_u02 as F2
import ca_u01 as CA1

UNIT_ID = "exponential-logarithmic-functions"
ABBR = "el"
SUBS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def lg(b, arg):
    return f"log({arg})" if b == 10 else f"log{str(b).translate(SUBS)}({arg})"


# ============================================================== S1 Exponential growth and decay
@fam("012")
def s1_identify(r, L):
    a = rint(r, 2, 90) * pick(r, [1, 10])
    pct = pick(r, [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30, 35, 40])
    grow = r.random() < 0.5
    b = sp.Rational(100 + pct, 100) if grow else sp.Rational(100 - pct, 100)
    ftxt = f"y = {a}({D(F(b.p, b.q))})ᵗ"
    ask = pick(r, ["kind", "rate"]) if L else "kind"
    if ask == "kind":
        ans = f"{'growth' if grow else 'decay'}, {pct}%"
        wr = [f"{'decay' if grow else 'growth'}, {pct}%", f"{'growth' if grow else 'decay'}, {D(F(b.p, b.q))}%", f"{'growth' if grow else 'decay'}, {100 + pct if grow else 100 - pct}%"]
        return Q(f"Does {ftxt} model exponential growth or decay, and at what percent rate per time period?", ans,
                 [f"The base is {D(F(b.p, b.q))}, which is {'greater' if grow else 'less'} than 1, so it is {'growth' if grow else 'decay'}.", f"Rate: |{D(F(b.p, b.q))} - 1| = {D(F(pct, 100))} = {pct}%."],
                 wr, PY("growth_word", b=str(b)), why=["Mixed up growth and decay", "Used the base as the percent", "Used the base times 100 as the rate"], tags=["modeling"])
    item = pick(r, ["A town's population", "The value of a car", "A bacteria culture", "The number of app users", "The mass of a sample"])
    return Q(f"{item} is modeled by {ftxt}, where t is in years. By what percent does it {'increase' if grow else 'decrease'} each year?", f"{pct}%",
             [f"The growth factor is b = {D(F(b.p, b.q))}.", f"{'b - 1' if grow else '1 - b'} = {D(F(pct, 100))} = {pct}%."],
             [f"{D(F(b.p, b.q) * 100)}%", f"{D(F(b.p, b.q))}%", f"{100 - pct if grow else 100 + pct}%"], H(f"Abs(nsimplify('{D(F(b.p, b.q))}') - 1)"),
             why=["Used the growth factor as the percent", "Wrote the factor as a percent without subtracting from 1", "Subtracted from 100 incorrectly"], tags=["modeling"])


@fam("012")
def s1_model(r, L):
    P0 = rint(r, 2, 80) * pick(r, [10, 100])
    pct = pick(r, [2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    grow = r.random() < 0.55
    t_ = rint(r, 2, 10)
    b = 1 + pct / 100 if grow else 1 - pct / 100
    v = P0 * b ** t_
    what = pick(r, [("A population", "people"), ("An investment", "dollars"), ("A herd", "animals")]) if grow else pick(r, [("A car's value", "dollars"), ("A medication amount", "milligrams"), ("A lake's fish population", "fish")])
    return Q(f"{what[0]} starts at {P0:,} {what[1]} and {'grows' if grow else 'decreases'} by {pct}% per year. Find the amount after {t_} years, to the nearest whole number.", f"{round(v):,}",
             [f"y = {P0}(1 {'+' if grow else '-'} {D(F(pct, 100))})ᵗ = {P0}({D(F(round(b * 100), 100))})ᵗ.", f"y = {P0}({D(F(round(b * 100), 100))}){sup(t_)} ≈ {v:.2f}.", f"About {round(v):,} {what[1]}."],
             [f"{round(P0 * (1 + (pct if grow else -pct) * t_ / 100)):,}", f"{round(P0 * (1 - pct / 100 if grow else 1 + pct / 100) ** t_):,}", f"{round(P0 * (pct / 100) ** t_ if False else P0 * b * t_):,}"],
             H(f"{P0}*({'1 + ' if grow else '1 - '}Rational({pct}, 100))**{t_}", "round", places=0), why=["Used simple (linear) growth", "Used growth instead of decay" if not grow else "Used decay instead of growth", "Multiplied by t instead of raising to the power t"], tags=["modeling"])


# ============================================================== S2 Graphing exponential functions
@fam("012")
def s2_features(r, L):
    a = pick(r, [1, 2, 3, -1, -2]) if L else pick(r, [1, 2, 3])
    b = sp.sympify(pick(r, [2, 3, 4, 5, sp.Rational(1, 2), sp.Rational(1, 3)]))
    h_, k_ = (rint(r, -4, 4), rint(r, -6, 6)) if L else (0, rint(r, -6, 6))
    bt = T(b) if b.q == 1 else f"({T(b)})"
    ex = "x" if h_ == 0 else f"(x {'-' if h_ > 0 else '+'} {abs(h_)})"
    pw = (bt + "ˣ") if h_ == 0 else f"{bt}^{ex}"
    if a not in (1, -1) and not bt.startswith("("):
        pw = f"({bt})" + pw[len(bt):]
    ftxt = ("" if a == 1 else "-" if a == -1 else str(a)) + pw + ("" if k_ == 0 else f" {'+' if k_ > 0 else '-'} {abs(k_)}")
    ask = pick(r, ["asym", "yint", "range"])
    if ask == "asym":
        ans, wr, why = f"y = {k_}", [f"x = {h_}" if h_ else f"y = {a}", f"y = {-k_}" if k_ else "y = 1", f"y = {k_ + a}"], ["Gave a vertical line or the leading coefficient", "Used the wrong sign for the vertical shift", "Used the y-intercept"]
        code, mode = f"limit(P('{ftxt}'), x, {'-oo' if b > 1 else 'oo'})", "expr"
        ans_chk = ans[4:]
        q = f"What is the equation of the horizontal asymptote of f(x) = {ftxt}?"
        st = ["The parent function bˣ approaches 0 on one side.", f"Adding {k_} moves the asymptote to y = {k_}.", f"{ans}."]
    elif ask == "yint":
        v = a * b ** (-h_) + k_
        ans, wr, why = f"(0, {T(v)})", [f"(0, {T(a + k_)})" if a + k_ != v else f"(0, {T(v + 1)})", f"({T(v)}, 0)", f"(0, {T(k_)})" if k_ != v else f"(0, {T(v - 1)})"], ["Ignored the horizontal shift" if h_ else "Forgot that b⁰ = 1", "Switched the coordinates", "Used the asymptote value"]
        code, mode = f"(0, P('{ftxt}').subs(x, 0))", "point"
        q = f"Find the y-intercept of f(x) = {ftxt}."
        st = ["Substitute x = 0.", f"f(0) = {T(v)}.", f"{ans}."]
    else:
        rng = sp.Interval.open(k_, sp.oo) if a > 0 else sp.Interval.open(-sp.oo, k_)
        ans = set_text(rng)
        wr, why = [set_text(sp.Interval(k_, sp.oo)) if a > 0 else set_text(sp.Interval(-sp.oo, k_)), "(-∞, ∞)", set_text(sp.Interval.open(-sp.oo, k_) if a > 0 else sp.Interval.open(k_, sp.oo))], ["Included the asymptote value", "Gave the domain", "Reversed the direction of the range"]
        code, mode = f"Interval.open({k_}, oo)" if a > 0 else f"Interval.open(-oo, {k_})", "interval"
        code = f"__import__('sympy').calculus.util.function_range(P('{ftxt}'), x, Reals)"
        q = f"Find the range of f(x) = {ftxt}. Use interval notation."
        st = [f"The horizontal asymptote is y = {k_}.", f"The graph is {'above' if a > 0 else 'below'} the asymptote because a = {a} is {'positive' if a > 0 else 'negative'}.", f"Range: {ans}."]
    need(len(set(wr) | {ans}) == 4)
    if ask == "asym":
        return Q(q, ans, st, wr, H(f"Eq(y, {code})", "eqn") if False else H(f"y - ({code})", "eqn"), why=why)
    return Q(q, ans, st, wr, H(code, mode), why=why)


# ============================================================== S3 Inverse relationship of exponentials and logarithms
@fam("012")
def s3_convert(r, L):
    b = pick(r, [2, 3, 4, 5, 6, 10])
    e = rint(r, -3, 5) if L else rint(r, 1, 4)
    v = sp.Integer(b) ** e
    direction = pick(r, ["to_log", "to_exp"])
    if direction == "to_log":
        etxt = f"{b}{sup(e)} = {T(v)}"
        ans = f"{lg(b, T(v))} = {e}"
        wr = [f"{lg(T(v), b) if False else lg(e if e > 1 else b + 1, T(v))} = {b}", f"{lg(b, e)} = {T(v)}" if e > 0 else f"{lg(b, T(v))} = {-e}", f"{lg(T(v) if v.is_Integer and v > 1 else b + 2, b)} = {e}" if v.is_Integer and v > 1 else f"{lg(b, T(v))} = {e + 1}"]
        why = ["Used the exponent as the base", "Switched the exponent and the value", "Switched the base and the value"]
        need(len(set(wr) | {ans}) == 4)
        return Q(f"Write {etxt} in logarithmic form.", ans, ["bᵉ = v is equivalent to log_b(v) = e.", f"Base {b}, exponent {e}, value {T(v)}.", f"{ans}."],
                 wr, PY("log_form", b=b, e=e, v=str(v)), why=why)
    ltxt = f"{lg(b, T(v))} = {e}"
    ans = f"{b}{sup(e)} = {T(v)}"
    wr = [f"{e}{sup(b)} = {T(v)}" if e > 0 else f"{b}{sup(-e)} = {T(v)}", f"{T(v)}{sup(e)} = {b}" if v.is_Integer and e > 0 else f"{b}{sup(e + 1)} = {T(v)}", f"{b}{sup(e)} = {T(v * b)}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Write {ltxt} in exponential form.", ans, ["log_b(v) = e is equivalent to bᵉ = v.", f"{ans}."], wr, PY("exp_form", b=b, e=e, v=str(v)),
             why=["Switched the base and the exponent", "Switched the base and the value", "Made an error in the value"])


@fam("012")
def s3_inverse(r, L):
    b = pick(r, [2, 3, 4, 5, 10])
    h_, k_ = (rint(r, -5, 5), rint(r, -5, 5)) if L else (0, 0)
    if L == 0:
        ftxt, ans = f"{b}ˣ", f"f⁻¹(x) = {lg(b, 'x')}"
        wr = [f"f⁻¹(x) = {lg('x', b) if False else lg(b, 'x') + ' + 1'}", f"f⁻¹(x) = x{sup(b)}" if b < 10 else "f⁻¹(x) = x¹⁰", f"f⁻¹(x) = 1/{b}ˣ"]
        why = ["Added a shift that is not there", "Used a power function instead of a logarithm", "Used the reciprocal instead of the inverse"]
        code = f"{lg(b, 'x')}"
    else:
        ex = "x" if h_ == 0 else f"(x {'-' if h_ > 0 else '+'} {abs(h_)})"
        ftxt = f"{b}^{ex}" + ("" if k_ == 0 else f" {'+' if k_ > 0 else '-'} {abs(k_)}")
        arg = "x" if k_ == 0 else f"x {'-' if k_ > 0 else '+'} {abs(k_)}"
        inv = lg(b, arg) + ("" if h_ == 0 else f" {'+' if h_ > 0 else '-'} {abs(h_)}")
        ans = "f⁻¹(x) = " + inv
        arg2 = "x" if k_ == 0 else f"x {'+' if k_ > 0 else '-'} {abs(k_)}"
        wr = ["f⁻¹(x) = " + lg(b, arg2) + ("" if h_ == 0 else f" {'+' if h_ > 0 else '-'} {abs(h_)}"), "f⁻¹(x) = " + lg(b, arg) + ("" if h_ == 0 else f" {'-' if h_ > 0 else '+'} {abs(h_)}") if h_ else "f⁻¹(x) = " + lg(b, arg) + " + 1",
              "f⁻¹(x) = " + lg(b, "x") + (f" {'+' if h_ - k_ > 0 else '-'} {abs(h_ - k_)}" if h_ - k_ else " + 2")]
        why = ["Undid the vertical shift in the wrong direction", "Undid the horizontal shift in the wrong direction", "Combined the shifts outside the logarithm"]
        code = inv
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Find the inverse of f(x) = {ftxt}.", ans, ["Write y = f(x), switch x and y, and solve for y.", "Rewrite the exponential equation in logarithmic form.", f"{ans}."],
             wr, PY("inverse_of", f=ftxt), why=why)


# ============================================================== S5 Evaluating logarithms
@fam("12")
def s5_change_base(r, L):
    b = pick(r, [2, 3, 5, 6, 7, 8, 9])
    v = rint(r, 2, 200)
    need(not sp.log(v, b).is_Rational)
    val = math.log(v) / math.log(b)
    ans = Rd(val, 3)
    return Q(f"Use the change-of-base formula to evaluate {lg(b, v)} to the nearest thousandth.", ans,
             [f"{lg(b, v)} = log({v}) ÷ log({b}).", f"= {Rd(math.log10(v), 4)} ÷ {Rd(math.log10(b), 4)} ≈ {ans}."],
             [Rd(math.log(b) / math.log(v), 3), Rd(math.log10(v / b), 3), Rd(v / b, 3)], H(f"log({v})/log({b})", "round", places=3),
             why=["Divided in the wrong order", "Took the log of the quotient", "Divided the numbers without taking logarithms"])


# ============================================================== S6 Solving exponential equations
@fam("012")
def s6_common(r, L):
    base = pick(r, [2, 3, 5])
    p1, p2 = rint(r, 1, 3), rint(r, 1, 3)
    b1, b2 = base ** p1, base ** p2
    a1, c1 = (1, rint(r, -4, 4)) if L == 0 else (rint(r, 1, 3), rint(r, -4, 4))
    a2, c2 = (0, rint(r, 1, 4)) if L < 2 else (rint(r, 1, 3), rint(r, -4, 4))
    need(p1 * a1 != p2 * a2)
    sol = sp.Rational(p2 * c2 - p1 * c1, p1 * a1 - p2 * a2)
    if L == 0:
        need(sol.q == 1)
    e1 = T(a1 * x + c1)
    need(a2 or b2 ** c2 <= 3125)
    lhs = f"{b1}ˣ" if e1 == "x" else f"{b1}^({e1})"
    rhs = f"{b2}^({T(a2 * x + c2)})" if a2 else T(sp.Integer(b2) ** c2)
    ans = f"x = {T(sol)}"
    wr = [f"x = {T(sp.Rational(c2 - c1, a1 - a2) if a1 != a2 else c2 - c1 + 1)}", f"x = {T(-sol)}" if sol else "x = 1", f"x = {T(sp.Rational(b2 ** c2 if not a2 else c2, 1) - c1)}" if not a2 else f"x = {T(sol + 1)}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve {lhs} = {rhs}.", ans, [f"Write both sides as powers of {base}.", "Set the exponents equal.", f"Solve: {ans}."], wr, H(f"solve(Eq(P('{lhs}'), P('{rhs}')), x)", "set"),
             why=["Set the exponents equal without rewriting the bases", "Made a sign error", "Ignored the exponent and solved with the value"])


@fam("12")
def s6_log_solve(r, L):
    b = pick(r, [2, 3, 5, 7, 10])
    a = rint(r, 1, 6)
    c = rint(r, 2, 300)
    need(not sp.log(sp.Rational(c, a), b).is_Rational)
    lhs = f"{a if a != 1 else ''}({b})ˣ" if False else (f"{a}·{b}ˣ" if a != 1 else f"{b}ˣ")
    v = math.log(c / a) / math.log(b)
    return Q(f"Solve {lhs} = {c}. Round to the nearest thousandth.", f"x ≈ {Rd(v, 3)}",
             [f"Divide by {a}: {b}ˣ = {T(sp.Rational(c, a))}." if a != 1 else f"{b}ˣ = {c}.", f"Take the log of both sides: x = log({T(sp.Rational(c, a))}) ÷ log({b}).", f"x ≈ {Rd(v, 3)}."],
             [f"x ≈ {Rd(math.log(c) / math.log(a * b), 3)}", f"x ≈ {Rd(math.log(c / a), 3)}", f"x ≈ {Rd(math.log(c) / math.log(b), 3)}" if a != 1 else f"x ≈ {Rd(c / b, 3)}"],
             PY("approx_eq", code=f"log(Rational({c}, {a}))/log({b})", places=3), why=["Multiplied the coefficient into the base", "Forgot to divide by log of the base", "Did not divide by the coefficient first" if a != 1 else "Divided instead of using logarithms"])


# ============================================================== S7 Solving logarithmic equations
@fam("012")
def s7_solve(r, L):
    b = pick(r, [2, 3, 4, 5, 10])
    c = rint(r, 1, 3 if b < 10 else 2)
    a = rint(r, 1, 4) if L else 1
    k_ = rint(r, -9, 9)
    rhs = sp.Integer(b) ** c
    need((rhs - k_) % a == 0)
    sol = sp.Rational(rhs - k_, a)
    arg = T(a * x + k_)
    if L == 2 and r.random() < 0.5:
        # log_b(x) + log_b(x + d) = c
        d = rint(r, 1, 9)
        roots = sp.solve(x * (x + d) - rhs, x)
        good = [s_ for s_ in roots if s_.is_Integer and s_ > 0]
        need(len(good) == 1)
        ans = f"x = {good[0]}"
        bad = [s_ for s_ in roots if s_ != good[0]][0]
        txt = f"{lg(b, 'x')} + {lg(b, T(x + d))} = {c}"
        return Q(f"Solve {txt}.", ans, [f"Combine: {lg(b, T(sp.expand(x * (x + d))))} = {c}.", f"Exponential form: {T(sp.expand(x * (x + d)))} = {rhs}.", f"Solutions {good[0]} and {bad}; x = {bad} makes a logarithm undefined.", f"{ans}."],
                 [f"x = {good[0]} or x = {bad}", f"x = {bad}", f"x = {T(sp.Rational(rhs - d, 2))}" if (rhs - d) % 2 == 0 else f"x = {rhs}"], H(f"solve(Eq(P('{lg(b, 'x')}') + P('{lg(b, T(x + d))}'), {c}), x)", "set"),
                 why=["Did not check for extraneous solutions", "Kept only the extraneous solution", "Added the arguments instead of multiplying"])
    ans = f"x = {T(sol)}"
    wr = [f"x = {T(sp.Rational(b * c - k_, a))}", f"x = {T(sp.Rational(c ** b - k_, a))}" if c ** b != rhs else f"x = {T(sol + 1)}", f"x = {T(sp.Rational(rhs + k_, a))}" if k_ else f"x = {T(rhs * a)}"]
    need(len(set(wr) | {ans}) == 4)
    txt = f"{lg(b, arg)} = {c}"
    return Q(f"Solve {txt}.", ans, [f"Rewrite in exponential form: {arg} = {b}{sup(c)} = {rhs}.", f"Solve: {ans}.", "Check: the argument is positive, so the solution is valid."],
             wr, H(f"solve(Eq(P('{lg(b, arg)}'), {c}), x)", "set"), why=["Multiplied the base by the exponent", "Switched the base and the exponent", "Made a sign error moving the constant"])


# ============================================================== S8 Compound interest and real-world models
@fam("012")
def s8_compound(r, L):
    P0 = rint(r, 5, 80) * 100
    rate = pick(r, [2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7])
    n_, word = pick(r, [(1, "annually"), (2, "semiannually"), (4, "quarterly"), (12, "monthly")])
    t_ = rint(r, 2, 20)
    v = P0 * (1 + rate / 100 / n_) ** (n_ * t_)
    rt = F(str(rate)) / 100
    return Q(f"${P0:,} is deposited at {rate}% annual interest compounded {word}. Find the balance after {t_} years, to the nearest cent.", "$" + f"{v:,.2f}",
             [f"A = P(1 + r/n)^(nt) = {P0}(1 + {D(rt)}/{n_})^({n_}·{t_}).", f"A ≈ ${v:,.2f}."],
             ["$" + f"{P0 * (1 + rate / 100) ** t_:,.2f}" if n_ != 1 else "$" + f"{P0 * (1 + rate / 100 * t_):,.2f}", "$" + f"{P0 * (1 + rate / 100 * t_):,.2f}" if n_ != 1 else "$" + f"{P0 * (1 + rate / 100) ** (t_ + 1):,.2f}", "$" + f"{P0 * (1 + rate / n_) ** (n_ * t_) if False else P0 * (1 + rate / 100 / n_) ** t_:,.2f}"],
             H(f"{P0}*(1 + Rational({rt.numerator}, {rt.denominator})/{n_})**({n_}*{t_})", "round", places=2),
             why=["Ignored how often the interest is compounded" if n_ != 1 else "Used simple interest", "Used simple interest" if n_ != 1 else "Used one extra year", "Raised to t instead of nt"], tags=["modeling"])


@fam("12")
def s8_double(r, L):
    rate = pick(r, [2, 3, 4, 5, 6, 7, 8, 9, 10])
    kind = pick(r, ["annual", "continuous"]) if L == 2 else "annual"
    if kind == "annual":
        v = math.log(2) / math.log(1 + rate / 100)
        code = f"log(2)/log(1 + Rational({rate}, 100))"
        q = f"How many years will it take an investment to double at {rate}% interest compounded annually? Round to the nearest tenth of a year."
        st = [f"2 = (1.{rate:02d})ᵗ.", f"t = log 2 ÷ log(1.{rate:02d}).", f"t ≈ {Rd(v, 1)} years."]
    else:
        v = math.log(2) / (rate / 100)
        code = f"log(2)/Rational({rate}, 100)"
        q = f"How many years will it take an investment to double at {rate}% interest compounded continuously? Round to the nearest tenth of a year."
        st = [f"2 = e^({D(F(rate, 100))}t).", f"t = ln 2 ÷ {D(F(rate, 100))}.", f"t ≈ {Rd(v, 1)} years."]
    return Q(q, f"{Rd(v, 1)} years", st, [f"{Rd(100 / rate / 2, 1)} years", f"{Rd(100 / rate, 1)} years", f"{Rd(math.log(2) * rate, 1)} years"], H(code, "round", places=1),
             why=["Halved the simple-interest doubling time", "Used simple interest", "Multiplied by the rate instead of dividing"], tags=["modeling"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Exponential growth and decay", fams=[s1_identify, s1_model, rr(F2.s15_exp)], extra=[err_of(s1_identify), err_of(s1_model), open_of(s1_model)]),
    2: dict(name="Graphing exponential functions", fams=[s2_features], extra=[err_of(s2_features), open_of(s2_features)]),
    3: dict(name="Inverse relationship of exponentials and logarithms", fams=[s3_convert, s3_inverse], extra=[err_of(s3_convert), err_of(s3_inverse), open_of(s3_convert)]),
    4: dict(name="Logarithm properties", fams=[rr(CA1.s3_props)], extra=[err_of(rr(CA1.s3_props, tag="e")), open_of(rr(CA1.s3_props, tag="o"))]),
    5: dict(name="Evaluating logarithms", fams=[rr(F2.s17_log), s5_change_base], extra=[err_of(rr(F2.s17_log, tag="e")), err_of(s5_change_base), open_of(rr(F2.s17_log, tag="o"))]),
    6: dict(name="Solving exponential equations", fams=[s6_common, s6_log_solve, rr(CA1.s2_solve)], extra=[err_of(s6_common), err_of(s6_log_solve), open_of(s6_common)]),
    7: dict(name="Solving logarithmic equations", fams=[s7_solve], extra=[err_of(s7_solve), open_of(s7_solve)]),
    8: dict(name="Compound interest and real-world models", fams=[s8_compound, s8_double, rr(F2.s16_e)], extra=[err_of(s8_compound), err_of(s8_double), open_of(s8_compound)]),
}
