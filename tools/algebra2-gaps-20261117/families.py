"""Question families for the Algebra 2 audit, batch D (2026-11-17).

New skills (standards the audit found with no items) and real-world context problems for every unit.
A family is fn(r, L) -> I(prompt, answer, steps, wrongs, check, fam), as in
tools/audit-gap-skills-20261116/core.py (L: 0 Support/cp2, 1 Standard/cp1, 2 Advanced/honors).
`check` holds the parameters; verify.py recomputes every answer, option and student answer from
them with its own formulas, and confirms that check["show"] text is printed in the prompt.
Families marked mc_only have worded answers and appear only as multiple choice.
"""
import math, os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audit-gap-skills-20261116"))
from core import I, Reject, need, ri, g, levels, safe_round  # noqa: E402
from fmt import sup, num, coef, join, poly  # noqa: E402


def com(v):
    """12000 -> 12,000; 7.5 -> 7.5."""
    v = F(v)
    if v.denominator == 1:
        return f"{v.numerator:,}"
    return g(v)


def pct(v):
    return g(v) + "%"


def lin(m, b, var="x"):
    return join([coef(m, var) if m else "", num(b) if b else ""]) if (m or b) else "0"


def vform(a, h, k):
    """a(x - h)² + k."""
    inner = "x" if h == 0 else (f"x - {h}" if h > 0 else f"x + {-h}")
    lead = "" if a == 1 else ("-" if a == -1 else str(a))
    s = f"{lead}({inner})²"
    return s if k == 0 else (f"{s} + {k}" if k > 0 else f"{s} - {-k}")


def mc_only(fn):
    fn.mc_only = True
    return fn


def table(xs, rows):
    """rows: [(label, values)] -> 'x: -1, 0, 1 | f(x): 3, 1, 3' (one line per row)."""
    lines = ["x: " + ", ".join(str(x) for x in xs)]
    for lab, vals in rows:
        lines.append(f"{lab}: " + ", ".join(com(v) for v in vals))
    return "\n".join(lines)


# ======================================================== F-IF.C.9 comparing functions
def f_text(spec):
    t = spec["t"]
    if t == "lin":
        return lin(spec["m"], spec["b"])
    if t == "quad":
        return vform(spec["a"], spec["h"], spec["k"])
    if t == "exp":
        return f"{spec['a']}·{spec['b']}^x"
    raise ValueError(t)


def f_eval(spec, x):
    t = spec["t"]
    if t == "lin":
        return F(spec["m"]) * x + spec["b"]
    if t == "quad":
        return F(spec["a"] * (x - spec["h"]) ** 2 + spec["k"])
    return spec["a"] * F(spec["b"]) ** x


def cmp_rate(r, L):
    x1 = ri(r, -1, 1)
    x2 = x1 + ri(r, 2, 3)
    if L == 0:
        f = dict(t="lin", m=ri(r, -4, 6), b=ri(r, -6, 6))
        need(f["m"] != 0)
    elif L == 1:
        f = dict(t="quad", a=r.choice([1, 2, -1]), h=ri(r, -2, 2), k=ri(r, -5, 5))
    else:
        f = dict(t="exp", a=r.choice([1, 2, 3]), b=r.choice([2, 3]))
        x1 = ri(r, 0, 1)
        x2 = x1 + 2
    n = ri(r, -3, 8)
    c = ri(r, -6, 9)
    xs = list(range(x1, x1 + 4)) if x2 - x1 < 4 else list(range(x1, x2 + 1))
    need(x2 in xs)
    gv = [n * x + c for x in xs]
    rf = (f_eval(f, x2) - f_eval(f, x1)) / (x2 - x1)
    rg = F(n)
    need(rf.denominator == 1 and rf != rg)
    ans = abs(rf - rg)
    ft = f_text(f)
    prompt = (f"f(x) = {ft}. The table gives values of g.\n{table(xs, [('g(x)', gv)])}\n"
              f"Find the average rate of change of each function from x = {x1} to x = {x2}. How much greater is the larger rate than the smaller one?")
    steps = [f"f: [f({x2}) - f({x1})]/({x2} - ({x1})) = ({num(f_eval(f, x2))} - ({num(f_eval(f, x1))}))/{x2 - x1} = {num(rf)}.",
             f"g: from the table, [g({x2}) - g({x1})]/{x2 - x1} = ({gv[xs.index(x2)]} - ({gv[0]}))/{x2 - x1} = {num(rg)}.",
             f"Difference: |{num(rf)} - ({num(rg)})| = {num(ans)}."]
    wr = [(num(rf), "gave only the rate of f"), (num(rg), "gave only the rate of g"),
          (num(abs(rf - rg) * (x2 - x1)), "compared the total changes instead of the rates"), (num(abs(rf + rg)), "added the rates")]
    return I(prompt, num(ans), steps, wr, dict(k="cmp_rate", f=f, n=n, c=c, xs=xs, x1=x1, x2=x2, show=[ft, ", ".join(com(v) for v in gv)]), "compare_rate")


def cmp_max(r, L):
    a = -1 if L == 0 else r.choice([-1, -2, -3])
    h, k = ri(r, -3, 3), ri(r, -4, 9)
    h2, k2 = ri(r, -2, 4), ri(r, -4, 9)
    c = r.choice([1, 2, 3])
    need(k != k2 and h != h2)
    xs = list(range(h2 - 2, h2 + 3))
    gv = [k2 - c * (x - h2) ** 2 for x in xs]
    ft = vform(a, h, k)
    big = max(k, k2)
    prompt = (f"f(x) = {ft}. The quadratic function g has these values:\n{table(xs, [('g(x)', gv)])}\n"
              "Each function has a maximum value. What is the greater of the two maximum values?")
    steps = [f"f is in vertex form with a < 0, so its maximum is k = {k} (at x = {h}).",
             f"The table for g is symmetric about x = {h2}, so g's maximum is g({h2}) = {k2}.",
             f"The greater maximum is {big}."]
    wr = [(str(min(k, k2)), "gave the smaller maximum"), (str(h if k >= k2 else h2), "gave the x-value of the vertex instead of the maximum value"),
          (str(max(gv[0], gv[-1], -k)), "read the wrong value from the table or sign of k"), (str(k + k2), "added the two maximums")]
    return I(prompt, str(big), steps, wr, dict(k="cmp_max", a=a, h=h, kk=k, xs=xs, gv=gv, show=[ft, ", ".join(str(v) for v in gv)]), "compare_max")


def cmp_cross(r, L):
    X, Y = ri(r, -4, 5), ri(r, -6, 8)
    m1, m2 = ri(r, -4, 4), ri(r, -4, 4)
    need(m1 != m2 and m1 != 0)
    p1, p2 = (X + 1, Y + m1), (X + 3, Y + 3 * m1)
    b2 = Y - m2 * X
    gt = lin(m2, b2)
    prompt = (f"f is the linear function whose graph passes through ({p1[0]}, {p1[1]}) and ({p2[0]}, {p2[1]}). "
              f"g(x) = {gt}. For what value of x is f(x) = g(x)?")
    bf = Y - m1 * X
    steps = [f"Slope of f: ({p2[1]} - ({p1[1]}))/({p2[0]} - ({p1[0]})) = {m1}; using ({p1[0]}, {p1[1]}), f(x) = {lin(m1, bf)}.",
             f"Set f(x) = g(x): {lin(m1, bf)} = {gt}, so {coef(m1 - m2, 'x')} = {num(b2 - bf)}.",
             f"x = {X}."]
    wr = [(str(Y), "gave the y-coordinate of the intersection"), (str(X + 1), "used the first given point"), (str(-X) if X else str(X + 2), "made a sign error solving")]
    return I(prompt, str(X), steps, wr, dict(k="cmp_cross", p1=p1, p2=p2, m2=m2, b2=b2, show=[gt, f"({p1[0]}, {p1[1]})"]), "compare_cross")


def cmp_plans(r, L):
    r1, r2 = ri(r, 6, 12), ri(r, 2, 5)
    m = ri(r, 3, 12)
    F1 = ri(r, 10, 30)
    F2 = F1 + (r1 - r2) * m
    item = r.choice([("gym", "visits", "per visit"), ("phone plan", "gigabytes", "per gigabyte"), ("bike rental", "hours", "per hour")])
    xs = [0, 2, 4, 6]
    bv = [F2 + r2 * x for x in xs]
    prompt = (f"Two {item[0]} options. Option A costs C = {F1} + {r1}n dollars for n {item[1]}. "
              f"Option B's cost is shown in the table.\n{table(xs, [('Option B cost ($)', bv)])}\n"
              f"For how many {item[1]} do the two options cost the same?")
    steps = [f"From the table, Option B starts at ${F2} and rises ${(bv[1] - bv[0]) // 2} {item[2]}: C = {F2} + {r2}n.",
             f"Set them equal: {F1} + {r1}n = {F2} + {r2}n, so {r1 - r2}n = {F2 - F1}.",
             f"n = {m} {item[1]}."]
    wr = [(str(F1 + r1 * m), "gave the cost instead of the number of " + item[1]), (str(F2 - F1), "gave the difference in starting costs"),
          (str(m + 1), "rounded up past the break-even point"), (str((F2 - F1) // r2) if (F2 - F1) % r2 == 0 else str(m * 2), "divided by only one rate")]
    return I(prompt, str(m), steps, wr, dict(k="cmp_plans", F1=F1, r1=r1, xs=xs, bv=bv, show=[f"C = {F1} + {r1}n", ", ".join(str(v) for v in bv)]), "compare_plans")


def cmp_zero(r, L):
    levels(L, 1, 2)
    p, q = ri(r, -5, 2), ri(r, 3, 7)
    z = ri(r, -6, 8)
    need(z not in (p, q))
    m = r.choice([2, 3, -2])
    xs = list(range(z - 2, z + 3))
    gv = [m * (x - z) for x in xs]
    ft = f"(x {'-' if p >= 0 else '+'} {abs(p)})(x - {q})" if p else f"x(x - {q})"
    big = max(p, q, z)
    prompt = (f"f(x) = {ft}. The linear function g has these values:\n{table(xs, [('g(x)', gv)])}\n"
              "Consider every x-intercept of f and of g. What is the greatest of them?")
    steps = [f"f(x) = 0 when x = {p} or x = {q}.", f"From the table, g(x) = 0 at x = {z}.", f"The greatest x-intercept is {big}."]
    wr = [(str(min(p, q, z)), "gave the least x-intercept"), (str(-p) if p else str(-q), "used the opposite sign of a factor"), (str(gv[0]), "read a y-value from the table")]
    return I(prompt, str(big), steps, wr, dict(k="cmp_zero", p=p, q=q, xs=xs, gv=gv, show=[ft, ", ".join(str(v) for v in gv)]), "compare_zero")


# ======================================================== F-IF.C.10 parametric
def par_point(r, L):
    a, b, c, d = ri(r, -4, 5), ri(r, -6, 6), ri(r, -3, 4), ri(r, -6, 6)
    need(a and c)
    t0 = ri(r, -3, 4)
    xt = lin(a, b, "t")
    yt = lin(c, d, "t") if L == 0 else join([coef(c, "t²"), num(d) if d else ""])
    x = a * t0 + b
    y = c * t0 + d if L == 0 else c * t0 ** 2 + d
    ctx = r.choice(["", "A drone's position after t seconds is given in meters by ", "A point moves so that at time t, "])
    prompt = f"{ctx}x = {xt} and y = {yt}. Find the point (x, y) when t = {t0}." if ctx else f"A curve is defined parametrically by x = {xt} and y = {yt}. Find the point (x, y) when t = {t0}."
    steps = [f"x = {xt.replace('t', f'({t0})')} = {x}.", f"y = {yt.replace('t', f'({t0})')} = {y}.", f"The point is ({x}, {y})."]
    wr = [(f"({y}, {x})", "switched x and y"), (f"({x}, {c * t0 + d})" if L else f"({x}, {c * t0})", "made an error computing y"),
          (f"({a + b}, {y})", "used t = 1 for x"), (f"({t0}, {y})", "gave t instead of x")]
    return I(prompt, f"({x}, {y})", steps, wr, dict(k="par_point", a=a, b=b, c=c, d=d, sq=L > 0, t0=t0, show=[f"x = {xt}", f"y = {yt}", f"t = {t0}"]), "parametric_point")


def par_t(r, L):
    a, b, c, d = r.choice([2, 3, 4, 5, -2]), ri(r, -6, 6), ri(r, -4, 4), ri(r, -6, 6)
    need(c)
    t0 = ri(r, -2, 5)
    X = a * t0 + b
    xt, yt = lin(a, b, "t"), lin(c, d, "t") if L < 2 else join([coef(c, "t²"), num(d) if d else ""])
    y = c * t0 + d if L < 2 else c * t0 ** 2 + d
    prompt = f"A curve is defined by x = {xt} and y = {yt}. What is y when x = {X}?"
    steps = [f"Find t: {xt} = {X}, so t = {t0}.", f"Substitute t = {t0} into y: y = {y}."]
    wr = [(str(c * X + d), "substituted x in place of t"), (str(t0), "stopped at the value of t"), (str(y + c), "used t = " + str(t0 + 1))]
    return I(prompt, str(y), steps, wr, dict(k="par_t", a=a, b=b, c=c, d=d, sq=L == 2, X=X, show=[f"x = {xt}", f"y = {yt}", f"x = {X}?"]), "parametric_t")


def par_elim(r, L):
    h, m, c = ri(r, -5, 5), ri(r, -4, 5), ri(r, -6, 6)
    need(m not in (0, 1) and h)
    a = 1 if L == 0 else r.choice([1, 2])
    xt = lin(a, h, "t")
    yt = lin(m * a, c, "t")
    b = c - m * h
    prompt = f"x = {xt} and y = {yt}. Eliminate the parameter t and write y as a function of x in the form y = mx + b. What is b?"
    tx = lin(1, -h) if a == 1 else f"({lin(1, -h)})/{a}"
    steps = [f"Solve x = {xt} for t: t = {tx}.",
             f"Substitute into y = {yt}: y = {m * a}·{tx} {'+' if c >= 0 else '-'} {abs(c)} = {lin(m, b)}.", f"b = {b}."]
    wr = [(str(c), "used the constant from y(t) without substituting"), (str(c + m * h), "made a sign error with h"), (str(m), "gave the slope")]
    return I(prompt, str(b), steps, wr, dict(k="par_elim", a=a, h=h, ma=m * a, c=c, show=[f"x = {xt}", f"y = {yt}"]), "parametric_eliminate")


def par_land(r, L):
    vx = r.choice([20, 25, 30, 40, 50])
    if L == 0:
        k = ri(r, 1, 4)
        vy, h0, T = 16 * 2 * k, 0, 2 * k
    else:
        T, s = ri(r, 3, 6), ri(r, 1, 2)
        need(T > s)
        vy, h0 = 16 * (T - s), 16 * T * s
    yt = join([coef(-16, "t²"), coef(vy, "t"), num(h0) if h0 else ""])
    prompt = (f"A ball is thrown from {'the ground' if not h0 else f'{"an" if str(h0)[0] == "8" or h0 in (11, 18) else "a"} {h0}-foot platform'}. After t seconds its position in feet is x = {vx}t "
              f"(horizontal distance) and y = {yt} (height). How far does the ball travel horizontally before it hits the ground?")
    steps = [f"The ball lands when y = 0: {yt} = 0.", f"Factor: -16(t - {T})(t {'+' if h0 else '-'} {abs(-(h0 // (16 * T)) if h0 else 0)}) = 0" if h0 else f"Factor: -16t(t - {T}) = 0.",
             f"The landing time is t = {T} s, so x = {vx}·{T} = {vx * T} ft."]
    steps[1] = steps[1] if not h0 else f"Factor: -16(t - {T})(t + {h0 // (16 * T)}) = 0."
    wr = [(str(T), "gave the time instead of the distance"), (str(vx * T // 2), "used the time of the highest point"), (str(vx * vy // 16), "ignored the starting height") if h0 else (str(vx * (T + 1)), "added a second")]
    return I(prompt, str(vx * T), steps, wr, dict(k="par_land", vx=vx, vy=vy, h0=h0, show=[f"x = {vx}t", f"y = {yt}"]), "parametric_projectile")


def par_max(r, L):
    levels(L, 1, 2)
    k, h0 = ri(r, 1, 3), r.choice([0, 4, 5, 6, 8])
    vy = 32 * k
    vx = r.choice([15, 20, 30])
    yt = join([coef(-16, "t²"), coef(vy, "t"), num(h0) if h0 else ""])
    top = h0 + 16 * k * k
    prompt = f"A rocket's position after t seconds is x = {vx}t and y = {yt}, in feet. What is its maximum height?"
    steps = [f"y is a downward parabola in t; its vertex is at t = -b/(2a) = -{vy}/(2·(-16)) = {k}.", f"y({k}) = -16({k})² + {vy}({k}) + {h0} = {top}.", f"Maximum height: {top} ft."]
    wr = [(str(k), "gave the time of the maximum"), (str(vx * k), "gave the horizontal distance"), (str(-16 * k * k + vy * k), "left out the starting height") if h0 else (str(vy), "gave the starting vertical speed")]
    return I(prompt, str(top), steps, wr, dict(k="par_max", vy=vy, h0=h0, show=[f"y = {yt}"]), "parametric_max_height")


# ======================================================== A-SSE.A.1 interpreting expressions
THINGS = [("A town's population", "people"), ("The number of users of an app", "users"), ("The value of a rare coin", "dollars"), ("A bacteria culture", "cells")]


def ie_growth(r, L):
    rate = r.choice([F(2), F(3), F(4), F(5), F(6), F(8), F(35, 10), F(25, 10), F(45, 10), F(12)])
    A = r.choice([1200, 5000, 12000, 25000, 800, 150])
    thing = r.choice(THINGS)
    fac = 1 + rate / 100
    prompt = f"{thing[0]} is modeled by P(t) = {com(A)}({g(fac)})^t, where t is in years. By what percent does it grow each year?"
    steps = [f"The base {g(fac)} is the growth factor: {g(fac)} = 1 + {g(rate / 100)}.", f"The rate is {g(rate / 100)} = {pct(rate)} per year."]
    wr = [(pct(fac * 100), "gave the growth factor as a percent"), (pct(fac), "wrote the growth factor with a percent sign"), (pct(rate * 10), "misplaced the decimal point")]
    return I(prompt, pct(rate), steps, wr, dict(k="ie_growth", fac=str(fac), show=[f"{com(A)}({g(fac)})^t"]), "interpret_growth_rate")


def ie_decay(r, L):
    rate = r.choice([F(5), F(10), F(12), F(15), F(20), F(25), F(8), F(35, 10)])
    A = r.choice([25000, 32000, 18000, 900])
    fac = 1 - rate / 100
    what = r.choice(["The value of a car", "The amount of a medicine in the bloodstream", "The number of fish in a lake"])
    prompt = f"{what} is modeled by V(t) = {com(A)}({g(fac)})^t, where t is in years. By what percent does it decrease each year?"
    steps = [f"The decay factor is {g(fac)} = 1 - {g(rate / 100)}.", f"So it decreases by {g(rate / 100)} = {pct(rate)} each year."]
    wr = [(pct(fac * 100), "gave the percent that remains"), (pct(rate / 100), "did not convert the decimal to a percent"), (pct(rate * 10), "misplaced the decimal point")]
    return I(prompt, pct(rate), steps, wr, dict(k="ie_decay", fac=str(fac), show=[f"{com(A)}({g(fac)})^t"]), "interpret_decay_rate")


def ie_initial(r, L):
    A = r.choice([250, 1200, 3500, 40000, 75])
    fac = r.choice(["1.04", "1.08", "0.9", "0.75", "1.5"])
    thing = r.choice(THINGS)
    prompt = f"{thing[0]} is modeled by f(t) = {com(A)}({fac})^t, where t is years since 2020. What was the amount in 2020?"
    steps = [f"2020 corresponds to t = 0.", f"f(0) = {com(A)}({fac})⁰ = {com(A)}·1 = {com(A)}."]
    v1 = F(A) * F(fac)
    wr = [(com(v1), "used t = 1"), (fac, "gave the growth factor"), (com(A * 2), "doubled the starting amount")]
    return I(prompt, com(A), steps, wr, dict(k="ie_initial", A=A, show=[f"{com(A)}({fac})^t"]), "interpret_initial")


def ie_double(r, L):
    d = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    A = r.choice([100, 500, 2000, 80])
    half = r.random() < 0.5
    if half:
        prompt = f"The amount of a radioactive sample is A(t) = {com(A)}(1/2)^(t/{d}) grams after t years. What is the half-life in years?"
        steps = [f"Each time t increases by {d}, the exponent t/{d} increases by 1.", f"Then the amount is multiplied by 1/2, so the half-life is {d} years."]
    else:
        prompt = f"A population is P(t) = {com(A)}·2^(t/{d}) after t hours. How many hours does it take the population to double?"
        steps = [f"Each time t increases by {d}, the exponent t/{d} increases by 1.", f"Then P is multiplied by 2, so the doubling time is {d} hours."]
    wr = [(str(2 * d), "doubled the divisor"), (str(F(d, 2)) if d % 2 == 0 else str(d + 1), "halved the divisor"), (str(A // 2 if half else A * 2), "gave an amount instead of a time")]
    return I(prompt, str(d), steps, wr, dict(k="ie_double", d=d, show=[f"(t/{d})"]), "interpret_doubling")


def ie_monthly(r, L):
    levels(L, 2)
    rate = r.choice([4, 5, 6, 7, 8, 9, 10, 12])
    fac = 1 + F(rate, 100)
    m = float(fac) ** (1 / 12)
    p = (m - 1) * 100
    safe_round(p, 2)
    prompt = (f"An account's balance is B(t) = 2,000({g(fac)})^t after t years. Rewrite the expression to find the equivalent monthly growth rate. "
              "Give the monthly rate as a percent, rounded to the nearest hundredth of a percent.")
    steps = [f"({g(fac)})^t = (({g(fac)})^(1/12))^(12t).", f"({g(fac)})^(1/12) ≈ {m:.5f}.", f"The monthly rate is about {p:.2f}%."]
    wr = [(f"{rate / 12:.2f}%", "divided the annual rate by 12"), (f"{rate}%", "gave the annual rate"), (f"{m * 100:.2f}%", "gave the monthly growth factor as a percent")]
    return I(prompt, f"{p:.2f}%", steps, wr, dict(k="ie_monthly", fac=str(fac), show=[f"2,000({g(fac)})^t"]), "interpret_monthly")


def ie_quad(r, L):
    levels(L, 1, 2)
    if r.random() < 0.5:
        N, c = r.choice([200, 300, 120, 500]), r.choice([2, 4, 5, 10])
        p = ri(r, 3, 15)
        need(N - c * p > 0)
        prompt = f"A store's revenue is R = p({N} - {c}p) dollars when an item is priced at p dollars. The factor ({N} - {c}p) is the number of items sold. How many items are sold at a price of ${p}?"
        ans = N - c * p
        steps = [f"Items sold = {N} - {c}({p}) = {ans}.", f"(Revenue would be {p} · {ans} = {p * ans} dollars.)"]
        wr = [(str(p * ans), "gave the revenue"), (str(N), "gave the number sold at a price of $0"), (str(N - p), "left out the coefficient " + str(c))]
        return I(prompt, str(ans), steps, wr, dict(k="ie_items", N=N, c=c, p=p, show=[f"p({N} - {c}p)", f"${p}?"]), "interpret_factor")
    t, top = ri(r, 1, 4), r.choice([64, 70, 81, 100, 120])
    prompt = f"The height of a ball is h(t) = -16(t - {t})² + {top} feet after t seconds. What is the ball's maximum height?"
    steps = [f"(t - {t})² ≥ 0, so -16(t - {t})² ≤ 0, with 0 when t = {t}.", f"The maximum height is {top} ft, at t = {t} s."]
    wr = [(str(t), "gave the time of the maximum"), (str(top - 16), "evaluated at t = " + str(t + 1)), (str(16 * t), "multiplied the visible numbers")]
    return I(prompt, str(top), steps, wr, dict(k="ie_vertex", t=t, top=top, show=[f"-16(t - {t})² + {top}"]), "interpret_vertex")


@mc_only
def ie_meaning(r, L):
    A, fac = r.choice([(1500, "1.06"), (800, "1.12"), (20000, "0.92"), (4000, "1.03")])
    grow = F(fac) > 1
    rate = abs(F(fac) - 1) * 100
    ask = r.choice(["A", "fac"])
    expr = f"{com(A)}({fac})^t"
    if ask == "A":
        ans = "the amount at t = 0"
        wr = [(f"the {'growth' if grow else 'decay'} factor", "mixed up the parts"), ("the amount after one year", "used t = 1"), (f"the {'increase' if grow else 'decrease'} each year", "confused the starting amount with the change")]
        q = f"In f(t) = {expr}, what does {com(A)} represent?"
    else:
        ans = f"the amount is multiplied by {fac} each year"
        wr = [(f"the amount {'grows' if grow else 'falls'} by {fac} each year", "read the factor as an amount added"), (f"the amount {'grows' if grow else 'falls'} by {g(F(fac) * 100)}% each year", "read the factor as the percent"),
              ("the amount at t = 0", "mixed up the parts")]
        q = f"In f(t) = {expr}, what does the factor {fac} tell you?"
    steps = [f"In a·b^t, a = {com(A)} is the value when t = 0 and b = {fac} is the factor applied each year.", f"{'Growth' if grow else 'Decay'} of {g(rate)}% per year."]
    return I(q, ans, steps, wr, dict(k="fact", key=ans, show=[expr]), "interpret_meaning")


# ======================================================== A-REI.D.11 solving f(x) = g(x)
def fg_table(r, L):
    a, b = ri(r, -3, 2), ri(r, 0, 4)
    need(a < b)
    m, c = ri(r, -3, 3), ri(r, -4, 4)
    fq = {2: 1, 1: m - a - b, 0: c + a * b}
    ft, gt = poly(fq), lin(m, c) if (m or c) else "0"
    xs = list(range(a - 1, b + 2))
    need(len(xs) <= 7)
    fv = [x * x + fq[1] * x + fq[0] for x in xs]
    gv = [m * x + c for x in xs]
    prompt = f"f(x) = {ft} and g(x) = {gt}.\n{table(xs, [('f(x)', fv), ('g(x)', gv)])}\nUse the table to find every solution of f(x) = g(x)."
    ans = f"x = {a} and x = {b}"
    steps = [f"Look for x-values where the f(x) and g(x) rows match: at x = {a} both are {m * a + c}; at x = {b} both are {m * b + c}.",
             f"f - g = (x - ({a}))(x - {b}) is a quadratic, so there are no other solutions.", f"Solutions: {ans}."]
    wr = [(f"x = {a}", "found only one solution"), (f"x = {m * a + c} and x = {m * b + c}", "gave the y-values"), (f"x = {-a} and x = {-b}", "used the opposite signs")]
    return I(prompt, ans, steps, wr, dict(k="fg_quad", f=[1, fq[1], fq[0]], m=m, c=c, show=[ft, gt, ", ".join(str(v) for v in fv)]), "fg_table")


def fg_count(r, L):
    kind = r.choice(["quad", "abs", "exp"] if L else ["quad", "abs"])
    if kind == "quad":
        h, k = ri(r, -3, 3), ri(r, -4, 4)
        c = ri(r, -6, 6)
        ft, gt = vform(1, h, k), str(c)
        ans = 2 if c > k else (1 if c == k else 0)
        why = f"The parabola has its minimum {k} at x = {h}; the horizontal line y = {c} is {'above' if c > k else ('at' if c == k else 'below')} it."
    elif kind == "abs":
        h, k = ri(r, -3, 3), ri(r, -4, 4)
        c = ri(r, -6, 6)
        ft = f"|x {'-' if h >= 0 else '+'} {abs(h)}|" + (f" + {k}" if k > 0 else (f" - {-k}" if k < 0 else ""))
        gt = str(c)
        ans = 2 if c > k else (1 if c == k else 0)
        why = f"The V-shaped graph has its vertex at ({h}, {k}); y = {c} is {'above' if c > k else ('at' if c == k else 'below')} the vertex."
    else:
        b, k = r.choice([2, 3]), ri(r, -3, 3)
        c = ri(r, -5, 6)
        ft = f"{b}^x" + (f" + {k}" if k > 0 else (f" - {-k}" if k < 0 else ""))
        gt = str(c)
        ans = 1 if c > k else 0
        why = f"{ft} is always increasing and stays above its asymptote y = {k}; y = {c} is {'above' if c > k else 'not above'} the asymptote."
    prompt = f"f(x) = {ft} and g(x) = {gt}. Think about the graphs: how many solutions does f(x) = g(x) have?"
    steps = [why, f"So the graphs cross {ans} time{'s' if ans != 1 else ''}: {ans} solution{'s' if ans != 1 else ''}."]
    wr = [(str((ans + 1) % 3), "misjudged where the line sits"), (str(2 if ans != 2 else 1), "assumed two crossings"), (str(3), "counted the intercepts")]
    return I(prompt, str(ans), steps, wr, dict(k="fg_count", kind=kind, ft=ft, c=c, show=[f"f(x) = {ft}", f"g(x) = {gt}."]), "fg_count")


def fg_between(r, L):
    levels(L, 1, 2)
    b, c = r.choice([2, 3]), ri(r, 2, 12)
    f = lambda x: b ** x - (x + c)
    n = 0
    while f(n + 1) < 0:
        n += 1
    need(f(n) < 0 < f(n + 1))
    xs = list(range(max(0, n - 1), n + 3))
    prompt = (f"f(x) = {b}^x and g(x) = x + {c}. The graphs cross at one point with x > 0.\n"
              f"{table(xs, [('f(x)', [b ** x for x in xs]), ('g(x)', [x + c for x in xs])])}\n"
              "The x-coordinate of that point lies between two consecutive whole numbers. What is the smaller of the two?")
    steps = [f"At x = {n}: f = {b ** n} < g = {n + c}.", f"At x = {n + 1}: f = {b ** (n + 1)} > g = {n + 1 + c}.", f"f - g changes sign, so the solution is between {n} and {n + 1}. The smaller is {n}."]
    wr = [(str(n + 1), "gave the larger whole number"), (str(n - 1) if n else str(n + 2), "read the wrong rows"), (str(c), "gave the y-intercept of g")]
    return I(prompt, str(n), steps, wr, dict(k="fg_between", b=b, c=c, show=[f"{b}^x", f"x + {c}"]), "fg_between")


def fg_point(r, L):
    if L == 0 or r.random() < 0.5:
        a, b = ri(r, -4, 5), ri(r, -3, 3)
        need(a != 0)
        k = b + ri(r, 1, 4)
        x = (k - b) ** 2 - a
        ft = f"√(x {'+' if a >= 0 else '-'} {abs(a)})" + (f" + {b}" if b > 0 else (f" - {-b}" if b < 0 else ""))
        steps = [f"Set √(x {'+' if a >= 0 else '-'} {abs(a)}) {'+' if b >= 0 else '-'} {abs(b)} = {k}: √(x {'+' if a >= 0 else '-'} {abs(a)}) = {k - b}.", f"Square: x {'+' if a >= 0 else '-'} {abs(a)} = {(k - b) ** 2}, so x = {x}.", f"The graphs meet at ({x}, {k})."]
        chk = dict(k="fg_sqrt", a=a, b=b, kk=k)
        wr = [(f"({k}, {x})", "switched the coordinates"), (f"({k - b - a}, {k})", "did not square"), (f"({(k - b) ** 2 + a}, {k})", "made a sign error with the shift"),
              (f"({(k + b) ** 2 - a}, {k})", "made a sign error with the vertical shift"), (f"({x}, {k - b})", "gave √ of the shifted value as y")]
    else:
        base, a = r.choice([2, 3]), ri(r, -4, 4)
        k = ri(r, 1, 3 if base == 2 else 2)
        x = base ** k + a
        ft = f"log{'₂' if base == 2 else '₃'}(x {'-' if a >= 0 else '+'} {abs(a)})"
        steps = [f"Set {ft} = {k}.", f"Rewrite in exponential form: x {'-' if a >= 0 else '+'} {abs(a)} = {base}^{k} = {base ** k}, so x = {x}.", f"The graphs meet at ({x}, {k})."]
        chk = dict(k="fg_log", base=base, a=a, kk=k)
        wr = [(f"({k}, {x})", "switched the coordinates"), (f"({base * k + a}, {k})", "multiplied instead of raising to a power"), (f"({base ** k - a}, {k})", "made a sign error with the shift"),
              (f"({k ** base + a}, {k})", "switched the base and the exponent")]
    prompt = f"f(x) = {ft} and g(x) = {k}. At what point do the graphs of f and g intersect?"
    return I(prompt, f"({x}, {k})", steps, wr, dict(chk, show=[f"f(x) = {ft}", f"g(x) = {k}."]), "fg_point")


def fg_calc(r, L):
    levels(L, 2)
    b, c = r.choice([2, 3]), ri(r, 3, 9)
    lo, hi = 0.0, 10.0
    f = lambda x: b ** x - (c - x)
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    x = lo
    safe_round(x, 2)
    prompt = f"Use a graphing calculator (graph y = {b}^x and y = {c} - x and find the intersection) to solve {b}^x = {c} - x. Round to the nearest hundredth."
    steps = [f"Graph y₁ = {b}^x and y₂ = {c} - x; the increasing and decreasing graphs cross exactly once.", f"The intersection is at x ≈ {x:.2f} (check: {b}^{x:.2f} ≈ {b ** x:.2f} and {c} - {x:.2f} ≈ {c - x:.2f})."]
    wr = [(f"{x + 0.1:.2f}", "read the intersection inaccurately"), (f"{c - x:.2f}", "gave the y-coordinate"), (f"{math.log(c, b):.2f}", f"solved {b}^x = {c} instead")]
    return I(prompt, f"{x:.2f}", steps, wr, dict(k="fg_calc", b=b, c=c, show=[f"{b}^x = {c} - x"]), "fg_calculator")


def fg_towns(r, L):
    A0, d = r.choice([2000, 3000, 5000]), r.choice([100, 150, 200, 250])
    B0, gr = r.choice([1000, 1500, 2000]), r.choice([F(1, 10), F(8, 100), F(12, 100), F(15, 100)])
    need(B0 < A0)
    t = 0
    while not (B0 * (1 + gr) ** t > A0 + d * t):
        t += 1
        need(t <= 30)
    need(3 <= t <= 25)
    prompt = (f"Town A's population is A(t) = {com(A0)} + {d}t and Town B's is B(t) = {com(B0)}({g(1 + gr)})^t, where t is years from now. "
              "Make a table or graph both functions. After how many whole years will Town B first have more people than Town A?")
    steps = [f"t = {t - 1}: A = {com(A0 + d * (t - 1))}, B ≈ {com(round(B0 * float(1 + gr) ** (t - 1)))}; A is larger.",
             f"t = {t}: A = {com(A0 + d * t)}, B ≈ {com(round(B0 * float(1 + gr) ** t))}; B is larger.", f"Town B first passes Town A after {t} years."]
    wr = [(str(t - 1), "gave the last year Town A was larger"), (str(t + 1), "counted one year too many"), (str(round((A0 - B0) / d)), "treated both towns as linear")]
    return I(prompt, str(t), steps, wr, dict(k="fg_towns", A0=A0, d=d, B0=B0, gr=str(gr), show=[f"{com(A0)} + {d}t", f"{com(B0)}({g(1 + gr)})^t"]), "fg_context")


# ======================================================== S-IC.A.2 simulation and models
GAMES = [("a spinner", "lands on red", "red results"), ("a coin", "lands heads", "heads"), ("a basketball player", "makes a free throw", "made free throws"), ("a die", "shows a 6", "sixes")]


def sim_prop(r, L):
    N = r.choice([100, 200, 250, 500])
    k = ri(r, 1, 40)
    p = F(k, N)
    need((p * 1000).denominator == 1)
    obj, ev, unit = r.choice(GAMES)
    prompt = (f"To test a model for {obj}, a class simulated {N} sets of trials under the model. "
              f"In {k} of the {N} simulated sets, the number of {unit} was at least as extreme as the real result. "
              "What proportion of the simulated sets were at least as extreme? Give a decimal.")
    steps = [f"Proportion = {k}/{N}.", f"= {g(p)}."]
    wr = [(g(F(N - k, N)), "used the sets that were not as extreme"), (g(F(k, 100)), "divided by 100 instead of " + str(N)), (str(k), "gave the count instead of the proportion")]
    return I(prompt, g(p), steps, wr, dict(k="ratio", num=k, den=N, show=[f"{k} of the {N}"]), "simulation_proportion")


def sim_expected(r, L):
    n = r.choice([20, 40, 50, 60, 80, 100, 120])
    p = r.choice([F(1, 2), F(1, 4), F(1, 5), F(3, 10), F(2, 5), F(1, 6), F(3, 4)])
    need((n * p).denominator == 1)
    ptxt = r.choice([f"{g(p * 100)}%", num(p)]) if (p * 100).denominator == 1 else num(p)
    prompt = f"A model says a cereal box contains a prize with probability {ptxt}. Under this model, how many prizes would you expect in {n} boxes?"
    steps = [f"Expected count = n·p = {n} · {ptxt}.", f"= {n * p}."]
    wr = [(str(n - n * p), "counted boxes without prizes"), (str(n * p * 2), "doubled the probability"), (num(p), "gave the probability")]
    return I(prompt, str(n * p), steps, wr, dict(k="product", a=n, b=str(p), show=[ptxt, f"{n} boxes"]), "simulation_expected")


def sim_dot(r, L):
    vals = list(range(ri(r, 0, 3), ri(r, 0, 3) + 9))
    freqs = [ri(r, 0, 9) for _ in vals]
    total = sum(freqs)
    need(total >= 25)
    cut = r.choice(vals[3:-1])
    k = sum(f for v, f in zip(vals, freqs) if v >= cut)
    need(0 < k < total)
    p = F(k, total)
    prompt = (f"A simulation of a model was run {total} times. The table shows how often each result appeared.\n"
              f"Result: {', '.join(str(v) for v in vals)}\nFrequency: {', '.join(str(f) for f in freqs)}\n"
              f"What fraction of the simulated results were {cut} or more?")
    steps = [f"Add the frequencies for results {cut} and up: {' + '.join(str(f) for v, f in zip(vals, freqs) if v >= cut)} = {k}.",
             f"Fraction = {k}/{total}" + (f" = {num(p)}." if num(p) != f"{k}/{total}" else ".")]
    k2 = sum(f for v, f in zip(vals, freqs) if v > cut)
    wr = [(num(F(k2, total)), f"left out the result {cut} itself"), (num(F(total - k, total)), "counted the results below " + str(cut)), (num(F(k, len(vals))), "divided by the number of possible results")]
    return I(prompt, num(p), steps, wr, dict(k="dot_frac", vals=vals, freqs=freqs, cut=cut, show=[", ".join(str(f) for f in freqs)]), "simulation_dotplot")


@mc_only
def sim_decide(r, L):
    N = r.choice([100, 200, 500])
    k = r.choice([1, 2, 3, 4, 6, 15, 24, 30, 45, 60, 80]) * N // 100
    k = max(1, k)
    p = F(k, N)
    yes = "The model is consistent with the data: a result like this is not unusual under the model."
    no = "The model is doubtful: a result this extreme happened rarely (less than 5% of the time) under the model."
    ans = yes if p >= F(1, 20) else no
    other = no if ans == yes else yes
    prompt = (f"A student claims a coin is fair. In 50 flips it landed heads 32 times. A simulation of {N} sets of 50 fair flips gave 32 or more heads in {k} sets. "
              "Using a 5% cutoff, which conclusion is best?")
    steps = [f"Proportion of simulated sets at least as extreme: {k}/{N} = {g(p)}.", f"{g(p)} is {'at least' if p >= F(1, 20) else 'less than'} 0.05, so: {ans}"]
    wr = [(other, "compared with the cutoff the wrong way"), ("The simulation proves the coin is fair.", "treated a simulation as proof"), ("The coin is unfair because 32 is not exactly 25.", "expected the exact expected value every time")]
    return I(prompt, ans, steps, wr, dict(k="decide", num=k, den=N, key=ans, yes=yes, no=no, show=[f"in {k} sets"]), "simulation_decide")


def sim_sd(r, L):
    levels(L, 2)
    n, p = r.choice([(100, F(1, 2)), (64, F(1, 2)), (400, F(1, 2)), (100, F(1, 5)), (225, F(2, 5)), (144, F(1, 4)), (50, F(1, 2))])
    sd = math.sqrt(n * p * (1 - p))
    safe_round(sd, 2)
    prompt = f"Under a model, each of {n} trials succeeds with probability {num(p)}. The number of successes in a simulated set has standard deviation √(np(1 - p)). Find it, rounded to the nearest hundredth."
    steps = [f"np(1 - p) = {n}·{num(p)}·{num(1 - p)} = {g(n * p * (1 - p))}.", f"√{g(n * p * (1 - p))} ≈ {sd:.2f}."]
    wr = [(f"{n * p * (1 - p):.2f}", "forgot the square root"), (f"{math.sqrt(n * p):.2f}", "left out (1 - p)"), (f"{float(n * p):.2f}", "gave the mean")]
    return I(prompt, f"{sd:.2f}", steps, wr, dict(k="binsd", n=n, p=str(p), show=[f"{n} trials", num(p)]), "simulation_sd")


# ======================================================== S-IC.B.5 randomized experiments
def exp_diffmean(r, L):
    n = 5 if L == 0 else 6
    mt, mc = ri(r, 12, 30), ri(r, 8, 26)
    need(mt != mc)
    def grp(m):
        v = [m + ri(r, -4, 4) for _ in range(n - 1)]
        v.append(m * n - sum(v))
        need(min(v) > 0)
        return v
    t, c = grp(mt), grp(mc)
    what = r.choice([("plants", "new fertilizer", "standard fertilizer", "growth in cm"), ("students", "new study app", "no app", "quiz score gain"), ("runners", "new shoe", "old shoe", "seconds saved")])
    prompt = (f"{2 * n} {what[0]} were randomly assigned to two groups. {what[3].capitalize()}:\n{what[1].capitalize()}: {', '.join(map(str, t))}\n"
              f"{what[2].capitalize()}: {', '.join(map(str, c))}\nFind the difference in means ({what[1]} minus {what[2]}).")
    d = mt - mc
    steps = [f"Mean for {what[1]}: {sum(t)}/{n} = {mt}.", f"Mean for {what[2]}: {sum(c)}/{n} = {mc}.", f"Difference: {mt} - {mc} = {d}."]
    wr = [(str(-d), "subtracted in the wrong order"), (str(sum(t) - sum(c)), "subtracted the totals"), (str(sorted(t)[n // 2] - sorted(c)[n // 2]) if sorted(t)[n // 2] - sorted(c)[n // 2] != d else str(d + 1), "used another measure of center")]
    return I(prompt, str(d), steps, wr, dict(k="diffmean", t=t, c=c, show=[", ".join(map(str, t)), ", ".join(map(str, c))]), "experiment_diff_means")


def exp_diffprop(r, L):
    n = r.choice([20, 25, 40, 50])
    a, b = ri(r, 5, n - 3), ri(r, 3, n - 5)
    need(a > b)
    d = F(a, n) - F(b, n)
    need((d * 100).denominator == 1)
    prompt = (f"In a randomized experiment, {a} of {n} patients improved with a new treatment and {b} of {n} improved with a placebo. "
              "What is the difference in the proportions who improved (treatment minus placebo)? Give a decimal.")
    steps = [f"Treatment: {a}/{n} = {g(F(a, n))}. Placebo: {b}/{n} = {g(F(b, n))}.", f"Difference: {g(F(a, n))} - {g(F(b, n))} = {g(d)}."]
    wr = [(str(a - b), "subtracted the counts"), (g(F(a - b, 2 * n)), "divided by both groups combined"), (g(F(a, n)), "gave only the treatment proportion")]
    return I(prompt, g(d), steps, wr, dict(k="diffprop", a=a, b=b, n=n, show=[f"{a} of {n}", f"{b} of {n}"]), "experiment_diff_props")


def exp_rerand(r, L):
    k = r.choice([1, 2, 3, 4, 6, 8, 12, 18, 25, 31])
    N = r.choice([100, 200])
    k = k * N // 100
    d = r.choice([3, 4, 5, 6, 2.5])
    prompt = (f"An experiment found a difference in means of {d} points. The results were re-randomized into two groups {N} times; "
              f"{k} of the re-randomizations gave a difference of {d} or more. Estimate the probability of a difference this large by chance alone.")
    steps = [f"Probability ≈ {k}/{N}.", f"= {g(F(k, N))}."]
    wr = [(g(F(N - k, N)), "used the re-randomizations that were smaller"), (str(k), "gave the count"), (g(F(k, 1000)), "divided by the wrong total")]
    return I(prompt, g(F(k, N)), steps, wr, dict(k="ratio", num=k, den=N, show=[f"{k} of the re-randomizations", f"{N} times"]), "experiment_rerandomize")


@mc_only
def exp_decide(r, L):
    N = 100
    k = r.choice([0, 1, 2, 3, 4, 7, 12, 20, 35])
    p = F(k, N)
    yes = "Yes: a difference this large is unlikely by chance alone, so the treatment likely caused it."
    no = "No: a difference this large happens often by chance alone, so the evidence is weak."
    ans = yes if p < F(1, 20) else no
    other = no if ans == yes else yes
    prompt = (f"In a randomized experiment, a new reading program raised mean scores by 6 points over the usual program. In {N} re-randomizations of the same scores, "
              f"{k} gave a difference of 6 or more. Using a 5% cutoff, is the difference statistically significant?")
    steps = [f"Estimated probability by chance: {k}/{N} = {g(p)}.", f"{g(p)} is {'less than' if p < F(1, 20) else 'not less than'} 0.05. {ans}"]
    wr = [(other, "compared with the cutoff the wrong way"), ("Yes, because any positive difference is significant.", "ignored chance variation"), ("No, because re-randomization cannot be used with experiments.", "misunderstood the method")]
    return I(prompt, ans, steps, wr, dict(k="decide_lt", num=k, den=N, key=ans, yes=yes, no=no, show=[f"{k} gave a difference"]), "experiment_decide")


CONCEPTS = {
    "random_assign": ("Why do researchers randomly assign subjects to treatment groups?",
                      "To make the groups similar in every other way, so a difference in results can be blamed on the treatment",
                      [("To make sure every subject gets the treatment", "confused assignment with treatment"), ("So the results can be applied to everyone in the country", "confused random assignment with random sampling"),
                       ("To make the sample size larger", "confused randomization with replication")]),
    "control": ("What is the purpose of a control group in an experiment?",
                "To give a baseline to compare the treatment group with",
                [("To receive a larger dose of the treatment", "misread the role of the control"), ("To check that the researchers measured correctly", "confused control with checking"),
                 ("To make the experiment observational", "mixed up study types")]),
    "placebo": ("Why might a placebo be given to the control group?",
                "So both groups believe they are treated, and the placebo effect is the same in each",
                [("To save money on the treatment", "gave a cost reason"), ("To make the control group improve more", "misread the purpose"), ("Because placebos are a stronger treatment", "confused placebo with treatment")]),
    "causation": ("A study found that students who eat breakfast earn higher grades. The students chose whether to eat breakfast. What conclusion is justified?",
                  "There is an association, but the study cannot show that breakfast causes higher grades",
                  [("Eating breakfast causes higher grades", "treated an observational study as an experiment"), ("Higher grades cause students to eat breakfast", "reversed the direction of cause"),
                   ("There is no relationship between breakfast and grades", "ignored the association found")]),
    "voluntary": ("A website poll asked visitors to vote on a new law, and 80% of 2,000 voters opposed it. What is the main problem with reporting that 80% of residents oppose the law?",
                  "Voters chose to respond, so the sample is probably not representative",
                  [("2,000 is too small for any conclusion", "blamed the sample size"), ("80% is too high to be true", "judged the number instead of the method"), ("Online polls always have a 5% margin of error", "invented a fixed error")]),
    "small": ("An ad says \"4 out of 5 dentists recommend our toothpaste\" after asking 5 dentists who work for the company. What is the main problem?",
              "The sample is tiny and not chosen at random, and the dentists have a conflict of interest",
              [("4 out of 5 is less than 100%", "ignored how the data were collected"), ("Dentists cannot judge toothpaste", "dismissed the experts"), ("The fraction should be written as 80%", "focused on notation")]),
}


@mc_only
def concept_exp(r, L):
    key = r.choice(["random_assign", "control", "placebo"])
    q, a, wr = CONCEPTS[key]
    return I(q, a, ["Random assignment, a control group and a placebo let researchers compare treatments fairly.", f"Answer: {a}."], wr, dict(k="fact", key=a, show=[q]), "experiment_concept")


@mc_only
def concept_report(r, L):
    key = r.choice(["causation", "voluntary", "small"])
    q, a, wr = CONCEPTS[key]
    return I(q, a, ["Ask how the data were collected: who was measured, how they were chosen, and whether a treatment was assigned.", f"Answer: {a}."], wr, dict(k="fact", key=a, show=[q]), "report_concept")


# ======================================================== S-IC.B.6 evaluating reports
def rep_moe(r, L):
    p, m = ri(r, 38, 62), r.choice([2, 3, 4, 5])
    lo = r.random() < 0.5
    topic = r.choice(["support a new park", "favor a later school start", "plan to vote yes on a bond", "use the city bus weekly"])
    prompt = f"A news report says {p}% of residents {topic}, with a margin of error of ±{m}%. What is the {'lowest' if lo else 'highest'} plausible percent?"
    ans = p - m if lo else p + m
    steps = [f"The plausible interval is {p}% ± {m}%: {p - m}% to {p + m}%.", f"The {'lowest' if lo else 'highest'} plausible value is {ans}%."]
    wr = [(f"{p + m if lo else p - m}%", "gave the other end of the interval"), (f"{p}%", "ignored the margin of error"), (f"{p - 2 * m if lo else p + 2 * m}%", "doubled the margin of error")]
    return I(prompt, f"{ans}%", steps, wr, dict(k="moe_end", p=p, m=m, lo=lo, show=[f"{p}%", f"±{m}%"]), "report_margin")


@mc_only
def rep_majority(r, L):
    p, m = ri(r, 49, 58), r.choice([2, 3, 4, 5])
    yes = "Yes: every plausible value is above 50%."
    no = "No: some plausible values are 50% or below."
    ans = yes if p - m > 50 else no
    prompt = f"A poll finds {p}% of voters support a candidate, with a margin of error of ±{m}%. A headline says \"Most voters support the candidate.\" Is the headline justified?"
    steps = [f"Plausible interval: {p - m}% to {p + m}%.", f"The lower end is {p - m}%, which is {'above' if p - m > 50 else 'not above'} 50%. {ans}"]
    other = no if ans == yes else yes
    wr = [(other, "checked the wrong end of the interval"), (f"Yes: {p}% is more than 50%.", "ignored the margin of error"), ("No: polls can never support a claim.", "rejected all sampling")]
    return I(prompt, ans, steps, wr, dict(k="majority", p=p, m=m, key=ans, yes=yes, no=no, show=[f"{p}%", f"±{m}%"]), "report_majority")


def rep_change(r, L):
    a = r.choice([20, 25, 40, 50, 80, 120, 200, 250])
    pc = r.choice([-50, -40, -25, -20, -10, 10, 15, 20, 25, 40, 50, 60, 75])
    b = a + a * pc // 100
    need(a * pc % 100 == 0 and b > 0)
    what = r.choice(["reported bike thefts", "library visitors per day", "students in the robotics club", "monthly complaints"])
    prompt = f"A report says the number of {what} went from {a} to {b}. What is the percent change? (Use a negative number for a decrease.)"
    steps = [f"Change = {b} - {a} = {b - a}.", f"Percent change = {b - a}/{a} = {g(F(b - a, a))} = {pc}%."]
    wr = [(f"{g(F(b - a, b) * 100)}%", "divided by the new value"), (f"{b - a}%", "gave the change as a percent"), (f"{-pc}%", "got the sign wrong")]
    return I(prompt, f"{pc}%", steps, wr, dict(k="pctchange", a=a, b=b, show=[f"from {a} to {b}"]), "report_percent_change")


def rep_risk(r, L):
    x = r.choice([1, 2, 4, 5, 10])
    y = x + r.choice([1, 2, 3, 5]) * (x if x <= 2 else 1)
    need(y > x and (100 * (y - x)) % x == 0)
    per = r.choice([1000, 10000])
    ask = r.choice(["rel", "abs"]) if L else "abs"
    prompt = (f"A study reports that a side effect occurs in {x} of every {com(per)} people who do not take a medicine and {y} of every {com(per)} who do. "
              + ("A headline calls this a big increase in risk. By how many cases per " + com(per) + " people does the risk actually increase?" if ask == "abs" else "By what percent does the risk increase (relative increase)?"))
    if ask == "abs":
        ans, steps = str(y - x), [f"Absolute increase = {y} - {x}.", f"= {y - x} more case(s) per {com(per)} people."]
        wr = [(f"{100 * (y - x) // x}", "gave the relative increase as a number"), (str(y), "gave the new risk"), (str(x + y), "added the risks")]
    else:
        ans, steps = f"{100 * (y - x) // x}%", [f"Relative increase = ({y} - {x})/{x} = {g(F(y - x, x))}.", f"= {100 * (y - x) // x}%."]
        wr = [(f"{y - x}%", "gave the absolute increase as a percent"), (f"{g(F(y - x, y) * 100)}%", "divided by the new risk"), (f"{g(F(y, x) * 100)}%", "gave the ratio as a percent")]
    return I(prompt, ans, steps, wr, dict(k="risk", x=x, y=y, ask=ask, show=[f"{x} of every", f"{y} of every"]), "report_risk")


def rep_axis(r, L):
    a = ri(r, 40, 90)
    b = a + ri(r, 1, 6)
    start = a - ri(r, 1, 3)
    looks = F(b - start, a - start)
    actual = F(b - a, a) * 100
    safe_round(actual, 1)
    prompt = (f"A bar graph shows Brand A at {a} and Brand B at {b}, with the vertical axis starting at {start}, so Brand B's bar looks {g(looks, 2)} times as tall. "
              "By what percent is Brand B actually greater than Brand A? Round to the nearest tenth of a percent.")
    steps = [f"Actual difference: {b} - {a} = {b - a}.", f"Percent greater: {b - a}/{a} ≈ {float(F(b - a, a)):.4f} ≈ {float(actual):.1f}%.", "The truncated axis exaggerates the difference."]
    wr = [(f"{float(looks - 1) * 100:.1f}%", "used the bar heights from the truncated axis"), (f"{float(F(b - a, b) * 100):.1f}%", "divided by Brand B"), (f"{b - a}.0%", "gave the difference as a percent")]
    return I(prompt, f"{float(actual):.1f}%", steps, wr, dict(k="axis", a=a, b=b, show=[f"Brand A at {a}", f"Brand B at {b}"]), "report_truncated_axis")


# ======================================================== context word problems for every unit
def q_max_height(r, L):
    k, h0 = ri(r, 1, 3), r.choice([0, 3, 4, 5, 6])
    v = 32 * k
    ht = join([coef(-16, "t²"), coef(v, "t"), num(h0) if h0 else ""])
    who = r.choice(["A soccer ball is kicked", "A model rocket is launched", "A volleyball is served"])
    top = h0 + 16 * k * k
    prompt = f"{who} so that its height after t seconds is h(t) = {ht} feet. What is its maximum height, in feet?"
    steps = [f"The vertex is at t = -b/(2a) = -{v}/(2·(-16)) = {k} s.", f"h({k}) = -16({k})² + {v}({k}){f' + {h0}' if h0 else ''} = {top}.", f"Maximum height: {top} ft."]
    wr = [(str(k), "gave the time of the maximum"), (str(16 * k * k), "left out the starting height") if h0 else (str(v), "gave the starting speed"), (str(top + 16), "evaluated at the wrong time")]
    return I(prompt, str(top), steps, wr, dict(k="qmax", a=-16, b=v, c=h0, show=[ht]), "context_quadratic_height")


def q_land(r, L):
    T, s = ri(r, 2, 6), r.choice([0, 1, 2]) if L else 0
    need(T > s)
    v, h0 = 16 * (T - s), 16 * T * s
    ht = join([coef(-16, "t²"), coef(v, "t"), num(h0) if h0 else ""])
    prompt = f"A ball is thrown {'upward from the ground' if not h0 else f'from {"an" if str(h0)[0] == "8" or h0 in (11, 18) else "a"} {h0}-foot rooftop'}; its height after t seconds is h(t) = {ht} feet. After how many seconds does it hit the ground?"
    steps = [f"Solve {ht} = 0.", f"Factor: -16(t - {T})(t + {s}) = 0." if s else f"Factor: -16t(t - {T}) = 0.", f"The positive{' nonzero' if not s else ''} solution is t = {T} s."]
    wr = [(str(F(T - s, 2)) if (T - s) % 2 == 0 else g(F(T - s, 2)), "gave the time of the highest point"), (str(-s) if s else "0", "gave the other root"), (str(T + 1), "made an arithmetic error")]
    return I(prompt, str(T), steps, wr, dict(k="qroot", a=-16, b=v, c=h0, show=[ht]), "context_quadratic_landing")


def q_fence(r, L):
    wall = L > 0 and r.random() < 0.6
    if wall:
        j = ri(r, 3, 15)
        Fl = 8 * j
        area = Fl * Fl // 8
        prompt = f"A farmer has {Fl} feet of fence to make a rectangular pen against a barn wall (the wall is one side, so fence is needed on only three sides). What is the largest possible area, in square feet?"
        steps = [f"Let x be each side perpendicular to the wall; the side parallel is {Fl} - 2x.", f"A = x({Fl} - 2x) is greatest at x = {Fl // 4}.", f"A = {Fl // 4} · {Fl // 2} = {area} ft²."]
        wr = [(str((Fl // 4) ** 2), "fenced all four sides"), (str(Fl // 4), "gave the side length"), (str(Fl * Fl // 4), "used the wrong side lengths")]
    else:
        j = ri(r, 3, 20)
        Fl = 4 * j
        area = j * j
        prompt = f"A rectangle has a perimeter of {Fl} meters. What is the largest possible area, in square meters?"
        steps = [f"If one side is x, the other is {Fl // 2} - x, so A = x({Fl // 2} - x).", f"The vertex is at x = {j}, so the rectangle is a {j} by {j} square.", f"A = {area} m²."]
        wr = [(str(j), "gave the side length"), (str(Fl), "gave the perimeter"), (str((Fl // 2) ** 2), "squared half the perimeter")]
    return I(prompt, str(area), steps, wr, dict(k="fence", F=Fl, wall=wall, show=[f"{Fl} "]), "context_quadratic_fence")


def q_revenue(r, L):
    P, N, c = r.choice([10, 12, 15, 20]), r.choice([300, 400, 500, 600]), r.choice([10, 20, 25])
    x = F(N - c * P, 2 * c)
    need(x.denominator == 1 and 1 <= x <= 20)
    prompt = (f"A theater sells {N} tickets at ${P} each. For each $1 increase in price, it sells {c} fewer tickets, so revenue is R(x) = ({P} + x)({N} - {c}x) after x one-dollar increases. "
              "What ticket price gives the greatest revenue?")
    best = P + int(x)
    steps = [f"R is zero at x = -{P} and x = {N // c}; the vertex is halfway: x = (-{P} + {N // c})/2 = {x}.", f"Best price: ${P} + ${x} = ${best}.", f"Revenue: {best} · {N - c * int(x)} = ${best * (N - c * int(x)):,}."]
    wr = [(f"${x}", "gave the increase instead of the price"), (f"${N // c}", "used a zero instead of the vertex"), (f"${P}", "kept the original price")]
    return I(prompt, f"${best}", steps, wr, dict(k="revenue", P=P, N=N, c=c, show=[f"R(x) = ({P} + x)({N} - {c}x)"]), "context_quadratic_revenue")


def p_box_vol(r, L):
    Lg, Wd, x = r.choice([12, 16, 20, 24, 30]), r.choice([10, 12, 14, 18]), ri(r, 1, 4)
    need(Wd - 2 * x > 0)
    V = x * (Lg - 2 * x) * (Wd - 2 * x)
    prompt = (f"An open box is made from a {Lg} in. by {Wd} in. sheet of cardboard by cutting an x in. square from each corner and folding up the sides. "
              f"Its volume is V(x) = x({Lg} - 2x)({Wd} - 2x). Find the volume when x = {x}, in cubic inches.")
    steps = [f"V({x}) = {x}({Lg} - {2 * x})({Wd} - {2 * x}).", f"= {x} · {Lg - 2 * x} · {Wd - 2 * x} = {V} in³."]
    wr = [(str(x * (Lg - x) * (Wd - x)), "subtracted x only once from each side"), (str(Lg * Wd * x), "did not subtract the cut squares"), (str((Lg - 2 * x) * (Wd - 2 * x)), "gave the base area")]
    return I(prompt, str(V), steps, wr, dict(k="box", L=Lg, W=Wd, x=x, show=[f"x({Lg} - 2x)({Wd} - 2x)", f"x = {x}"]), "context_poly_box")


def p_box_solve(r, L):
    a, b = ri(r, 1, 4), ri(r, 2, 6)
    need(a != b)
    x = ri(r, 2, 8)
    V = x * (x + a) * (x + b)
    prompt = f"A storage bin is a box whose dimensions are x, x + {a} and x + {b} feet. Its volume is {V} cubic feet. Find x."
    steps = [f"x(x + {a})(x + {b}) = {V}.", f"Expand: {poly({3: 1, 2: a + b, 1: a * b, 0: -V})} = 0.", f"Test factors of {V}: x = {x} works ({x} · {x + a} · {x + b} = {V}); the remaining quadratic has no positive root, so x = {x} ft."]
    wr = [(str(x + a), "gave another dimension"), (str(round(V ** (1 / 3))), "took a cube root of the volume"), (str(x + 1), "made an arithmetic error")]
    return I(prompt, str(x), steps, wr, dict(k="boxsolve", a=a, b=b, V=V, show=[f"x + {a}", f"x + {b}", f"{V} cubic feet"]), "context_poly_dimensions")


def p_cube(r, L):
    levels(L, 1, 2)
    x, c = ri(r, 2, 9), ri(r, 1, 4)
    V = (x + c) ** 3
    prompt = f"Each edge of a cube is increased by {c} cm. The new cube has a volume of {V} cm³. How long was each edge of the original cube, in cm?"
    steps = [f"(x + {c})³ = {V}.", f"x + {c} = ∛{V} = {x + c}.", f"x = {x} cm."]
    wr = [(str(x + c), "gave the new edge length"), (str(x + 2 * c), "added instead of subtracting"), (str(V // 3 - c), "divided by 3 instead of taking a cube root")]
    return I(prompt, str(x), steps, wr, dict(k="cube", c=c, V=V, show=[f"by {c} cm", f"{V} cm³"]), "context_poly_cube")


SKID = [(F(f, 100), s) for f in (40, 50, 60, 75, 80) for s in range(20, 75, 5)]


def r_skid(r, L):
    f, s = r.choice(SKID)
    d = F(s * s) / (30 * f)
    need(d.denominator == 1 and d <= 400)
    prompt = f"Police estimate a car's speed from its skid marks with s = √(30fd), where s is speed in mph, f is the road's drag factor and d is the skid length in feet. On a road with f = {g(f)}, how long are the skid marks of a car going {s} mph?"
    steps = [f"{s} = √(30 · {g(f)} · d) = √({g(30 * f)}d).", f"Square both sides: {s * s} = {g(30 * f)}d.", f"d = {s * s}/{g(30 * f)} = {d} ft."]
    wr = [(g(F(s) / (30 * f)), "did not square the speed"), (g(F(s * s) * 30 * f), "multiplied instead of dividing"), (g(F(s * s, 30)), "left out the drag factor")]
    return I(prompt, str(d), steps, wr, dict(k="skid", f=str(f), s=s, show=["s = √(30fd)", f"f = {g(f)}", f"{s} mph"]), "context_radical_skid")


def r_horizon(r, L):
    k = ri(r, 1, 8)
    d = 3 * k
    h = 6 * k * k
    if r.random() < 0.5 or L == 0:
        prompt = f"The distance to the horizon is about d = √(1.5h) miles from a height of h feet. From what height is the horizon {d} miles away?"
        ans, steps = str(h), [f"{d} = √(1.5h).", f"{d * d} = 1.5h.", f"h = {d * d}/1.5 = {h} ft."]
        wr = [(g(F(d * d) * F(3, 2)), "multiplied by 1.5"), (str(d * d), "forgot the 1.5"), (g(F(d, 1) / F(3, 2)), "did not square")]
        chk = dict(k="horizon_h", d=d)
    else:
        prompt = f"The distance to the horizon is about d = √(1.5h) miles from a height of h feet. How far is the horizon from a lookout {h} feet high?"
        ans, steps = str(d), [f"d = √(1.5 · {h}) = √{int(F(3, 2) * h)}.", f"= {d} miles."]
        wr = [(str(int(F(3, 2) * h)), "did not take the square root"), (g(F(3, 2) * k), "took the square root too early"), (str(d * 2), "doubled the result")]
        chk = dict(k="horizon_d", h=h)
    return I(prompt, ans, steps, wr, dict(chk, show=["d = √(1.5h)", f"{d if chk['k'] == 'horizon_h' else h} "]), "context_radical_horizon")


def r_pendulum(r, L):
    levels(L, 1, 2)
    Lft = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    T = 2 * math.pi * math.sqrt(Lft / 32)
    safe_round(T, 2)
    prompt = f"A pendulum's period is T = 2π√(L/32) seconds, where L is its length in feet. Find the period of a {Lft}-foot pendulum, rounded to the nearest hundredth of a second."
    steps = [f"L/32 = {Lft}/32 = {g(F(Lft, 32))}.", f"√{g(F(Lft, 32))} ≈ {math.sqrt(Lft / 32):.4f}.", f"T ≈ 2π · {math.sqrt(Lft / 32):.4f} ≈ {T:.2f} s."]
    wr = [(f"{2 * math.pi * Lft / 32:.2f}", "forgot the square root"), (f"{math.pi * math.sqrt(Lft / 32):.2f}", "left out the 2"), (f"{2 * math.pi * math.sqrt(32 / Lft):.2f}", "inverted the fraction")]
    return I(prompt, f"{T:.2f}", steps, wr, dict(k="pendulum", L=Lft, show=["T = 2π√(L/32)", f"{Lft}-foot"]), "context_radical_pendulum")


WORK = [(3, 6), (4, 12), (6, 12), (10, 15), (12, 24), (20, 30), (6, 3), (12, 4), (2, 6), (5, 20), (9, 18), (8, 24)]


def w_work(r, L):
    a, b = r.choice(WORK)
    t = F(a * b, a + b)
    need(t.denominator == 1)
    who = r.choice([("Maya", "Jon", "paint a fence"), ("one pump", "a second pump", "fill a pool"), ("an old printer", "a new printer", "print the yearbooks")])
    if L == 2 and r.random() < 0.6:
        prompt = f"Working together, {who[0]} and {who[1]} can {who[2]} in {t} hours. Alone, {who[0]} takes {a} hours. How many hours would {who[1]} take alone?"
        steps = [f"1/{a} + 1/x = 1/{t}.", f"1/x = 1/{t} - 1/{a} = {num(F(1, int(t)) - F(1, a))}.", f"x = {b} hours."]
        wr = [(str(a - int(t)), "subtracted the times"), (str(a + int(t)), "added the times"), (num(F(a + int(t), 2)), "averaged the times")]
        return I(prompt, str(b), steps, wr, dict(k="work_other", a=a, t=int(t), show=[f"in {t} hours", f"takes {a} hours"]), "context_rational_work")
    prompt = f"Alone, {who[0]} can {who[2]} in {a} hours and {who[1]} can do it in {b} hours. How many hours does it take them working together?"
    steps = [f"Rates: 1/{a} + 1/{b} = {num(F(1, a) + F(1, b))} of the job per hour.", f"Time = 1 ÷ {num(F(1, a) + F(1, b))} = {t} hours."]
    wr = [(num(F(a + b, 2)), "averaged the times"), (str(a + b), "added the times"), (str(abs(a - b)), "subtracted the times")]
    return I(prompt, str(t), steps, wr, dict(k="work", a=a, b=b, show=[f"in {a} hours", f"in {b} hours"]), "context_rational_work")


def w_avgcost(r, L):
    Fc, v, x = r.choice([500, 1200, 2000, 3000]), r.choice([2, 4, 5, 8]), r.choice([50, 100, 200, 250, 400, 500])
    c = F(Fc, x) + v
    need(c.denominator == 1)
    prompt = f"A club spends ${com(Fc)} on a T-shirt design and ${v} per shirt. The average cost per shirt for x shirts is C(x) = ({com(Fc)} + {v}x)/x. How many shirts must they order for the average cost to be ${c}?"
    steps = [f"({com(Fc)} + {v}x)/x = {c}.", f"{com(Fc)} + {v}x = {c}x, so {com(Fc)} = {c - v}x.", f"x = {com(Fc)}/{c - v} = {x} shirts."]
    wr = [(str(Fc // int(c)), "ignored the per-shirt cost"), (str(Fc // v), "divided by the per-shirt cost"), (g(F(Fc, int(c) + v)), "added the per-shirt cost")]
    return I(prompt, str(x), steps, wr, dict(k="avgcost", F=Fc, v=v, c=int(c), show=[f"C(x) = ({com(Fc)} + {v}x)/x", f"${c}?"]), "context_rational_average_cost")


def w_mix(r, L):
    V, p, q = r.choice([10, 12, 20, 30, 40]), r.choice([10, 20, 25, 30]), r.choice([40, 50, 60])
    x = F(V * (q - p), 100 - q)
    need(x.denominator == 1 and q > p)
    prompt = f"A chemist has {V} liters of a {p}% acid solution. How many liters of pure acid must be added to make a {q}% solution? (Concentration = acid ÷ total.)"
    steps = [f"Acid now: {g(F(V * p, 100))} L. After adding x liters: ({g(F(V * p, 100))} + x)/({V} + x) = {g(F(q, 100))}.", f"{g(F(V * p, 100))} + x = {g(F(q * V, 100))} + {g(F(q, 100))}x, so {g(F(100 - q, 100))}x = {g(F(V * (q - p), 100))}.", f"x = {x} L."]
    wr = [(g(F(V * (q - p), 100)), "forgot that the total volume also grows"), (str(q - p), "subtracted the percents"), (g(F(V * (q - p), q)), "divided by the wrong amount")]
    return I(prompt, str(x), steps, wr, dict(k="mix", V=V, p=p, q=q, show=[f"{V} liters", f"{p}% acid", f"{q}% solution"]), "context_rational_mixture")


def w_inverse(r, L):
    n1, t1 = r.choice([(4, 6), (3, 8), (5, 12), (6, 10), (8, 9), (2, 15)])
    n2 = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    t2 = F(n1 * t1, n2)
    need(t2.denominator == 1 and n2 != n1)
    prompt = f"The time to paint a gym varies inversely with the number of painters. {n1} painters take {t1} hours. How many hours would {n2} painters take?"
    steps = [f"t = k/n, so k = {n1} · {t1} = {n1 * t1}.", f"t = {n1 * t1}/{n2} = {t2} hours."]
    wr = [(g(F(t1 * n2, n1)), "used direct variation"), (str(n1 * t1), "gave the constant k"), (str(t1 + n1 - n2), "changed the time by the change in painters")]
    return I(prompt, str(t2), steps, wr, dict(k="inverse", n1=n1, t1=t1, n2=n2, show=[f"{n1} painters take {t1} hours", f"{n2} painters"]), "context_rational_inverse")


def c_dish(r, L):
    w, d = ri(r, 2, 18) * 2, ri(r, 1, 9)
    p = F(w * w, 16 * d)
    need(p.denominator == 1 and 1 <= p <= 20)
    thing = r.choice([("satellite dish", "feet", "receiver"), ("solar cooker", "inches", "pot"), ("flashlight reflector", "centimeters", "bulb")])
    prompt = f"A {thing[0]} is a parabola in cross-section. It is {w} {thing[1]} wide and {d} {thing[1]} deep. How far from the bottom (vertex) should the {thing[2]} be placed, at the focus, in {thing[1]}?"
    steps = [f"Put the vertex at (0, 0): x² = 4py. The rim is at ({w // 2}, {d}).", f"({w // 2})² = 4p({d}), so {(w // 2) ** 2} = {4 * d}p.", f"p = {p} {thing[1]}."]
    wr = [(g(F(w * w, 4 * d)), "used the full width instead of half"), (g(F((w // 2) ** 2, d)), "forgot the 4 in x² = 4py"), (g(F(d * 4, 1)), "multiplied the depth by 4")]
    return I(prompt, str(p), steps, wr, dict(k="dish", w=w, d=d, show=[f"{w} {thing[1]} wide", f"{d} {thing[1]} deep"]), "context_conic_dish")


TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20)]


def c_tower(r, L):
    a, b, c = r.choice(TRIPLES)
    h, k = ri(r, -5, 5), ri(r, -5, 5)
    sx, sy = r.choice([1, -1]), r.choice([1, -1])
    if r.random() < 0.5:
        a, b = b, a
    x, y = h + sx * a, k + sy * b
    if L == 0:
        prompt = f"A cell tower is at ({h}, {k}) on a town map (units in miles). A house is at ({x}, {y}). How far is the house from the tower?"
        ans, steps = str(c), [f"d = √(({x} - ({h}))² + ({y} - ({k}))²) = √({a * a} + {b * b}).", f"= √{c * c} = {c} miles."]
        wr = [(str(a + b), "added the legs"), (str(c * c), "forgot the square root"), (str(abs(x - h) + abs(y - k) - 1), "estimated")]
        chk = dict(k="dist", p=[h, k], q=[x, y])
    else:
        prompt = f"A cell tower at ({h}, {k}) on a map (units in miles) reaches every point inside the circle where its signal ends. The house at ({x}, {y}) is exactly on that edge. Write the equation of the circle; what is r²?"
        ans, steps = str(c * c), [f"r = distance from ({h}, {k}) to ({x}, {y}) = √({a}² + {b}²) = {c}.", f"(x - h)² + (y - k)² = r² with r² = {c * c}."]
        wr = [(str(c), "gave r instead of r²"), (str((a + b) ** 2), "added the legs before squaring"), (str(h * h + k * k), "used the distance from the origin")]
        chk = dict(k="dist2", p=[h, k], q=[x, y])
    return I(prompt, ans, steps, wr, dict(chk, show=[f"({h}, {k})", f"({x}, {y})"]), "context_conic_tower")


def c_arch(r, L):
    H, W = ri(r, 8, 40), ri(r, 3, 15) * 2
    d = ri(r, 1, W // 2 - 1)
    need(0 < d < W // 2)
    y = F(H) * (1 - F(4 * d * d, W * W))
    need(y.denominator == 1)
    need(y > 0)
    prompt = f"A {r.choice(['bridge', 'tunnel entrance', 'park gateway'])} has a parabolic arch {H} meters high at the center and {W} meters wide at the base. How high is the arch {d} meter{'s' if d != 1 else ''} from the center?"
    steps = [f"With the top at (0, {H}) and base points (±{W // 2}, 0): y = {H} - ax², and 0 = {H} - a({W // 2})², so a = {num(F(H, (W // 2) ** 2))}.", f"y({d}) = {H} - {num(F(H, (W // 2) ** 2))}·{d * d} = {y} m."]
    wr = [(str(H - d), "subtracted the distance"), (g(F(H) * (1 - F(d, W // 2))), "treated the arch as two straight lines"), (str(H - d * d), "left out the coefficient a")]
    return I(prompt, str(y), steps, wr, dict(k="arch", H=H, W=W, d=d, show=[f"{H} meters high", f"{W} meters wide", f"{d} meter"]), "context_conic_arch")


def s_salary(r, L):
    S, R, n = r.choice([38000, 42000, 45000, 50000]), r.choice([1500, 2000, 2500, 1200]), ri(r, 5, 12)
    total = L > 0 and r.random() < 0.5
    if total:
        tot = n * (2 * S + (n - 1) * R) // 2
        prompt = f"A teacher's starting salary is ${com(S)}, with a raise of ${com(R)} each year. What are the total earnings over the first {n} years, in dollars?"
        ans, steps = com(tot), [f"Year {n} salary: {com(S)} + {n - 1}·{com(R)} = {com(S + (n - 1) * R)}.", f"Sum = {n}({com(S)} + {com(S + (n - 1) * R)})/2 = {com(tot)}."]
        wr = [(com(n * S), "left out the raises"), (com(n * (S + (n - 1) * R)), "used the last salary every year"), (com(n * (2 * S + n * R) // 2), "used n raises in the last year")]
        chk = dict(k="aseries", a=S, d=R, n=n)
    else:
        prompt = f"A job pays ${com(S)} the first year with a raise of ${com(R)} each year after. What is the salary in year {n}, in dollars?"
        ans, steps = com(S + (n - 1) * R), [f"aₙ = a₁ + (n - 1)d.", f"a_{n} = {com(S)} + {n - 1}·{com(R)} = {com(S + (n - 1) * R)}."]
        wr = [(com(S + n * R), "used n raises instead of n - 1"), (com(S * n), "multiplied the salary by n"), (com(S + (n - 2) * R), "used n - 2 raises")]
        chk = dict(k="aterm", a=S, d=R, n=n)
    return I(prompt, ans, steps, wr, dict(chk, show=[f"${com(S)}", f"${com(R)}"]), "context_sequence_salary")


def s_seats(r, L):
    a, d, n = ri(r, 12, 24), r.choice([2, 3, 4]), ri(r, 8, 20)
    tot = n * (2 * a + (n - 1) * d) // 2
    prompt = f"A theater's first row has {a} seats, and each row has {d} more seats than the row in front of it. How many seats are in {n} rows?"
    steps = [f"Row {n}: {a} + {n - 1}·{d} = {a + (n - 1) * d} seats.", f"Total = {n}({a} + {a + (n - 1) * d})/2 = {tot}."]
    wr = [(str(a + (n - 1) * d), "gave the seats in the last row"), (str(n * a), "left out the extra seats"), (str(n * (2 * a + n * d) // 2), "used n steps instead of n - 1")]
    return I(prompt, str(tot), steps, wr, dict(k="aseries", a=a, d=d, n=n, show=[f"has {a} seats", f"{d} more seats", f"{n} rows"]), "context_sequence_seats")


def s_geo(r, L):
    a, rr, n = r.choice([100, 200, 500, 50, 3]), r.choice([2, 3]), ri(r, 4, 8)
    need(a * rr ** (n - 1) <= 200000)
    what = r.choice([("A bacteria colony starts with", "cells", "multiplies by"), ("A video has", "views on day 1, and the number of new views", "multiplies by")])
    if what[1] == "cells":
        prompt = f"A bacteria colony has {com(a)} cells at hour 1, and the number of cells multiplies by {rr} every hour. How many cells are there at hour {n}?"
    else:
        prompt = f"A video gets {com(a)} new views on day 1, and each day's new views are {rr} times the day before. How many new views does it get on day {n}?"
    v = a * rr ** (n - 1)
    steps = [f"aₙ = a₁·r^(n - 1).", f"a_{n} = {com(a)}·{rr}^{n - 1} = {com(v)}."]
    wr = [(com(a * rr ** n), "used exponent n instead of n - 1"), (com(a + (n - 1) * rr), "treated it as arithmetic"), (com(a * rr * (n - 1)), "multiplied by r(n - 1)")]
    return I(prompt, com(v), steps, wr, dict(k="gterm", a=a, r=rr, n=n, show=[com(a), f"{rr} "]), "context_sequence_growth")


def s_ball(r, L):
    levels(L, 2)
    h, q = r.choice([6, 10, 12, 15, 20, 30]), r.choice([F(1, 2), F(2, 3), F(3, 4), F(3, 5), F(1, 3)])
    tot = h * (1 + q) / (1 - q)
    need(tot.denominator == 1)
    prompt = f"A ball is dropped from {h} feet. Each bounce reaches {num(q)} of the previous height. If it bounces forever, what total vertical distance does it travel, in feet?"
    steps = [f"Down {h} ft, then up and down each bounce: 2·({h}·({num(q)}) + {h}·({num(q)})² + …).", f"Infinite geometric sum: {h}·({num(q)})/(1 - {num(q)}) = {g(h * q / (1 - q))}.", f"Total = {h} + 2·{g(h * q / (1 - q))} = {tot} ft."]
    wr = [(g(h / (1 - q)), "counted each bounce only once"), (g(h * q / (1 - q)), "left out the first drop and the return trips"), (g(2 * h / (1 - q)), "doubled the first drop too")]
    return I(prompt, str(tot), steps, wr, dict(k="ball", h=h, q=str(q), show=[f"{h} feet", num(q)]), "context_sequence_ball")


def t_ferris(r, L):
    R, T = r.choice([20, 25, 30, 40, 50]), r.choice([4, 6, 8, 12])
    C = R + r.choice([2, 3, 5])
    t = r.choice([0, T // 4, T // 2, 3 * T // 4] + ([T // 6, T // 3] if L and T % 6 == 0 else []))
    hh = C - R * math.cos(2 * math.pi * t / T)
    need(abs(hh - round(hh)) < 1e-9)
    hh = round(hh)
    prompt = f"A rider's height on a Ferris wheel is h(t) = {C} - {R}cos(2πt/{T}) feet, t minutes after boarding. How high is the rider at t = {t} minutes?"
    ang = F(2 * t, T)
    at = "0" if ang == 0 else ("π" if ang == 1 else (f"{ang.numerator}π" if ang.denominator == 1 else f"{'' if ang.numerator == 1 else ang.numerator}π/{ang.denominator}"))
    steps = [f"2πt/{T} = 2π·{t}/{T} = {at}.", f"cos({at}) = {g(round(math.cos(2 * math.pi * t / T), 6))}.", f"h = {C} - {R}·({g(round(math.cos(2 * math.pi * t / T), 6))}) = {hh} ft."]
    wr = [(str(round(C + R * math.cos(2 * math.pi * t / T))), "added instead of subtracting"), (str(C + R), "gave the maximum height"), (str(C), "gave the center height")]
    wr = [w for w in wr if w[0] != str(hh)] + [(str(C - R), "gave the boarding height")]
    return I(prompt, str(hh), steps, wr, dict(k="ferris", C=C, R=R, T=T, t=t, show=[f"{C} - {R}cos(2πt/{T})", f"t = {t} minutes"]), "context_trig_ferris")


def t_temp(r, L):
    A, M = r.choice([8, 10, 12, 15, 18, 20]), r.choice([50, 55, 60, 65])
    ask = r.choice(["max", "min", "range"])
    prompt = f"The average high temperature in month m is T(m) = {A}sin((π/6)(m - 4)) + {M} °F. What is the {'highest average temperature' if ask == 'max' else ('lowest average temperature' if ask == 'min' else 'difference between the highest and lowest average temperatures')}?"
    ans = M + A if ask == "max" else (M - A if ask == "min" else 2 * A)
    steps = [f"sin ranges from -1 to 1, so T ranges from {M} - {A} = {M - A} to {M} + {A} = {M + A}.", f"Answer: {ans} °F."]
    wr = [(str(A), "gave the amplitude"), (str(M), "gave the midline"), (str(M + A if ask != "max" else M - A), "gave the other extreme"), (str(12), "gave the period")]
    return I(prompt, str(ans), steps, wr, dict(k="temp", A=A, M=M, ask=ask, show=[f"{A}sin((π/6)(m - 4)) + {M}"]), "context_trig_temperature")


def t_tide(r, L):
    k = r.choice([3, 4, 5, 6, 12])
    M, A = r.choice([8, 10, 12]), r.choice([2, 3, 4])
    prompt = f"The water depth at a dock is d(t) = {A}cos((π/{k})t) + {M} feet, t hours after midnight. How many hours pass between one high tide and the next?"
    steps = [f"Period = 2π ÷ (π/{k}).", f"= 2·{k} = {2 * k} hours."]
    wr = [(str(k), "used π/b instead of 2π/b"), (str(4 * k), "doubled the period"), (str(M + A), "gave the high-tide depth")]
    return I(prompt, str(2 * k), steps, wr, dict(k="tide", kk=k, show=[f"cos((π/{k})t)"]), "context_trig_tide")


def l_tickets(r, L):
    A, C = r.choice([12, 15, 18, 20, 25]), r.choice([5, 6, 8, 10])
    need(A > C)
    a, c = ri(r, 20, 150), ri(r, 20, 150)
    T, R = a + c, A * a + C * c
    event = r.choice(["school play", "basketball game", "science museum", "concert"])
    prompt = f"Adult tickets to a {event} cost ${A} and student tickets cost ${C}. {T} tickets were sold for a total of ${com(R)}. How many adult tickets were sold?"
    steps = [f"Let a = adult tickets and s = student tickets: a + s = {T} and {A}a + {C}s = {R}.", f"Substitute s = {T} - a: {A}a + {C}({T} - a) = {R}, so {A - C}a = {R - C * T}.", f"a = {a} adult tickets (and {c} student tickets)."]
    wr = [(str(c), "gave the number of student tickets"), (str(R // A), "divided the total by the adult price"), (str(T // 2), "split the tickets evenly")]
    return I(prompt, str(a), steps, wr, dict(k="tickets", A=A, C=C, T=T, R=R, show=[f"${A}", f"${C}", f"{T} tickets", f"${com(R)}"]), "context_linear_tickets")


def l_breakeven(r, L):
    Fc, v, p = r.choice([600, 900, 1200, 1500, 2400]), ri(r, 2, 9), ri(r, 10, 25)
    n = F(Fc, p - v)
    need(n.denominator == 1)
    what = r.choice([("bakery", "cakes"), ("club", "hoodies"), ("student business", "phone cases")])
    prompt = f"A {what[0]} spends ${com(Fc)} on equipment, and each of its {what[1]} costs ${v} to make and sells for ${p}. How many {what[1]} must it sell to break even (revenue = cost)?"
    steps = [f"Cost: C = {com(Fc)} + {v}n. Revenue: R = {p}n.", f"Set R = C: {p}n = {com(Fc)} + {v}n, so {p - v}n = {com(Fc)}.", f"n = {n} {what[1]}."]
    wr = [(g(F(Fc, p)), "ignored the cost per item"), (g(F(Fc, v)), "divided by the cost per item"), (g(F(Fc, p + v)), "added the price and the cost")]
    return I(prompt, str(n), steps, wr, dict(k="breakeven", F=Fc, v=v, p=p, show=[f"${com(Fc)}", f"${v} to make", f"sells for ${p}"]), "context_linear_breakeven")


def l_taxi(r, L):
    base, rate = r.choice([F(250, 100), F(3), F(350, 100), F(4), F(2)]), r.choice([F(150, 100), F(2), F(225, 100), F(250, 100), F(175, 100)])
    m1, m2 = ri(r, 2, 6), ri(r, 7, 15)
    f1, f2 = base + rate * m1, base + rate * m2
    ask = "base" if L else "rate"
    prompt = (f"A {m1}-mile taxi ride costs ${money(f1)} and a {m2}-mile ride costs ${money(f2)}. The fare is a linear function of distance. "
              f"What is the {'starting fee (the fare for 0 miles)' if ask == 'base' else 'cost per mile'}, in dollars?")
    steps = [f"Rate = ({money(f2)} - {money(f1)})/({m2} - {m1}) = {money(rate)} per mile.", f"Starting fee: {money(f1)} - {money(rate)}·{m1} = {money(base)}."]
    ans = money(base) if ask == "base" else money(rate)
    wr = [(money(rate) if ask == "base" else money(base), "found the other part of the fare"), (money(F(f1) / m1), "divided one fare by its distance"), (money(f2 - f1), "gave the change in fare")]
    return I(prompt, ans, steps, wr, dict(k="taxi", m1=m1, m2=m2, f1=str(f1), f2=str(f2), ask=ask, show=[f"{m1}-mile", f"{m2}-mile", money(f1), money(f2)]), "context_linear_taxi")


def money(v):
    v = F(v)
    return f"{float(v):.2f}"


# ======================================================== registry
# Families whose items are real-world context problems (tagged modeling + context-problem by build.py).
CONTEXTUAL = {"compare_plans", "parametric_projectile", "parametric_max_height", "fg_context"} | {n for n in (
    "interpret_growth_rate", "interpret_decay_rate", "interpret_initial", "interpret_doubling", "interpret_monthly", "interpret_factor", "interpret_vertex", "interpret_meaning",
    "simulation_proportion", "simulation_expected", "simulation_decide", "experiment_diff_means", "experiment_diff_props", "experiment_rerandomize", "experiment_decide",
    "report_margin", "report_majority", "report_percent_change", "report_risk", "report_truncated_axis", "report_concept")}
NEW_SKILLS = [
    # (unit, name, families, standards, id prefix)
    ("functions-transformations", "Comparing functions in different representations", [cmp_rate, cmp_max, cmp_cross, cmp_plans, cmp_zero], ["F-IF.C.9"], "a2-ft"),
    ("functions-transformations", "Parametric equations", [par_point, par_t, par_elim, par_land, par_max], ["F-IF.C.10"], "a2-ft"),
    ("linear-functions-systems", "Solving f(x) = g(x) with graphs and tables", [fg_table, fg_count, fg_between, fg_point, fg_calc, fg_towns], ["A-REI.D.11"], "a2-lfs"),
    ("exponential-logarithmic-functions", "Interpreting the structure of expressions", [ie_growth, ie_decay, ie_initial, ie_double, ie_monthly, ie_quad, ie_meaning], ["A-SSE.A.1a", "A-SSE.A.1b"], "a2-el"),
    ("probability-statistics", "Simulation and evaluating models", [sim_prop, sim_expected, sim_dot, sim_decide, sim_sd], ["S-IC.A.2"], "a2-ps"),
    ("probability-statistics", "Randomized experiments and comparing treatments", [exp_diffmean, exp_diffprop, exp_rerand, exp_decide, concept_exp], ["S-IC.B.5", "S-IC.B.3"], "a2-ps"),
    ("probability-statistics", "Evaluating reports based on data", [rep_moe, rep_majority, rep_change, rep_risk, rep_axis, concept_report], ["S-IC.B.6"], "a2-ps"),
]

# Context problems added to existing skills: unit -> (skill number, families, standards, id prefix)
CONTEXT = {
    "linear-functions-systems": (3, [l_tickets, l_breakeven, l_taxi], ["A-CED.A.3", "A-REI.C.6"], "a2-lfs"),
    "quadratic-functions-complex-numbers": (8, [q_max_height, q_land, q_fence, q_revenue], ["F-IF.B.4", "A-CED.A.1"], "a2-qc"),
    "polynomial-functions": (8, [p_box_vol, p_box_solve, p_cube], ["A-CED.A.1", "A-APR.B.3"], "a2-pf"),
    "radicals-rational-exponents": (5, [r_skid, r_horizon, r_pendulum], ["A-REI.A.2", "A-CED.A.4"], "a2-rr"),
    "rational-functions": (8, [w_work, w_avgcost, w_mix, w_inverse], ["A-CED.A.1", "A-REI.A.2"], "a2-rf"),
    "conic-sections": (2, [c_dish, c_arch], ["G-GPE.A.2"], "a2-cs"),
    "conic-sections#circle": (1, [c_tower], ["G-GPE.A.1"], "a2-cs"),
    "sequences-series": (8, [s_salary, s_seats, s_geo, s_ball], ["F-BF.A.2", "A-SSE.B.4"], "a2-ss"),
    "trigonometric-functions": (9, [t_ferris, t_temp, t_tide], ["F-TF.B.5", "F-IF.B.4"], "a2-tf"),
}
