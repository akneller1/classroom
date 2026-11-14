"""Calculus gap skills (2026-11-14): chain rule, implicit differentiation, derivatives of inverse
functions, L'Hôpital's Rule, integration by substitution.

Each family returns a dict:
  prompt, answer, steps, wrongs=[(text, misconception)], check={k: ..., data printed in the prompt}
L = 0 (CP2), 1 (CP1), 2 (Honors).
"""
from fractions import Fraction as F
from hsfmt import sup, num, coef, join, poly, paren


class Reject(Exception):
    pass


def need(c):
    if not c:
        raise Reject()


def ri(r, lo, hi, nz=False):
    while True:
        v = r.randint(lo, hi)
        if not (nz and v == 0):
            return v


def lin(a, b):
    return poly({1: a, 0: b})


def pw(base, n):
    """(base)ⁿ with ⁿ omitted for n = 1."""
    return f"({base})" if n == 1 else f"({base}){sup(n)}"


def I(prompt, answer, steps, wrongs, check, fam):
    ws, seen = [], {answer}
    for t, why in wrongs:
        if t not in seen:
            ws.append((t, why))
            seen.add(t)
    return dict(prompt=prompt, answer=answer, steps=steps, wrongs=ws, check=check, fam=fam)


# =================================================================== Chain rule
def ch_pow(r, L):
    if L == 0:
        a, b, n = ri(r, 2, 5), ri(r, -7, 7, True), ri(r, 3, 6)
        inner, dinner = lin(a, b), str(a)
        f = pw(inner, n)
        ans = f"{n * a}{pw(inner, n - 1)}"
        w = [(f"{n}{pw(inner, n - 1)}", "forgot to multiply by the derivative of the inside"),
             (f"{n * a}{pw(inner, n)}", "kept the same exponent"), (f"{n}{pw(str(a), n - 1)}", "differentiated the inside first, then applied the power rule to it")]
    elif L == 1:
        c, n = ri(r, -9, 9, True), ri(r, 3, 6)
        inner = poly({2: 1, 0: c})
        f = pw(inner, n)
        ans = f"{2 * n}x{pw(inner, n - 1)}"
        w = [(f"{n}{pw(inner, n - 1)}", "forgot to multiply by the derivative of the inside"),
             (f"{2 * n}x{pw(inner, n)}", "kept the same exponent"), (f"{n}x{pw(inner, n - 1)}", "used x instead of 2x for the derivative of the inside")]
    else:
        a, c = ri(r, 2, 6), ri(r, 1, 9)
        inner = poly({2: a, 0: c})
        if r.random() < 0.5:
            f = f"√({inner})"
            ans = f"{coef(a, 'x')}/√({inner})"
            w = [(f"1/(2√({inner}))", "forgot to multiply by the derivative of the inside"),
                 (f"{coef(2 * a, 'x')}/√({inner})", "forgot the 1/2 from the power rule"), (f"{coef(a, 'x')}√({inner})", "wrote the power as +1/2 instead of -1/2")]
        else:
            n = ri(r, 2, 4)
            f = f"1/{pw(inner, n)}"
            ans = f"-{2 * a * n}x/{pw(inner, n + 1)}"
            w = [(f"-{n}/{pw(inner, n + 1)}", "forgot to multiply by the derivative of the inside"),
                 (f"{2 * a * n}x/{pw(inner, n + 1)}", "lost the negative sign from the exponent"), (f"-{2 * a * n}x/{pw(inner, n - 1)}", "lowered the exponent instead of raising it")]
    return I(f"Find f′(x) for f(x) = {f}.", ans, ["Chain rule: f′(x) = (outer)′ evaluated at the inside, times (inside)′.", f"f′(x) = {ans}."], w,
             {"k": "deriv", "f": f}, "ch_pow")


def ch_fn(r, L):
    a = ri(r, 2, 6)
    if L == 0:
        k = r.choice(["sin", "cos", "exp"])
        if k == "sin":
            f, ans = f"sin({a}x)", f"{a}cos({a}x)"
            w = [(f"cos({a}x)", "forgot to multiply by the derivative of the inside"), (f"-{a}cos({a}x)", "used the derivative of cos"), (f"{a}sin({a}x)", "did not differentiate the outer function")]
        elif k == "cos":
            f, ans = f"cos({a}x)", f"-{a}sin({a}x)"
            w = [(f"-sin({a}x)", "forgot to multiply by the derivative of the inside"), (f"{a}sin({a}x)", "dropped the negative sign"), (f"-{a}cos({a}x)", "did not differentiate the outer function")]
        else:
            b = ri(r, -5, 5, True)
            f, ans = f"e^({lin(a, b)})", f"{a}e^({lin(a, b)})"
            w = [(f"e^({lin(a, b)})", "forgot to multiply by the derivative of the inside"), (f"{lin(a, b)}e^({lin(a - 1, b)})", "used the power rule on the exponent"), (f"{a}e^({a}x)", "dropped part of the exponent")]
    elif L == 1:
        c = ri(r, 1, 9)
        k = r.choice(["sin", "exp", "ln"])
        q = poly({2: 1, 0: c})
        if k == "sin":
            f, ans = f"sin({q})", f"2x cos({q})"
            w = [(f"cos({q})", "forgot to multiply by the derivative of the inside"), (f"cos(2x)", "differentiated the inside, then took cos of it"), (f"-2x cos({q})", "used the derivative of cos")]
        elif k == "exp":
            b = ri(r, -6, 6, True)
            q = poly({2: 1, 1: b})
            f, ans = f"e^({q})", f"({poly({1: 2, 0: b})})e^({q})"
            w = [(f"e^({q})", "forgot to multiply by the derivative of the inside"), (f"({q})e^({poly({2: 1, 1: b, 0: -1})})", "used the power rule on e"), (f"({poly({1: 2, 0: b})})e^({poly({1: 2, 0: b})})", "put the derivative of the inside in the exponent")]
        else:
            f, ans = f"ln({q})", f"2x/({q})"
            w = [(f"1/({q})", "forgot to multiply by the derivative of the inside"), (f"1/(2x)", "took 1 over the derivative of the inside"), (f"2x ln({q})", "multiplied instead of dividing")]
    else:
        k = r.choice(["esin", "lncos", "sinsq", "cossqrt"])
        if k == "esin":
            f, ans = f"e^(sin({a}x))", f"{a}cos({a}x)e^(sin({a}x))"
            w = [(f"e^(sin({a}x))", "forgot the derivative of the inside"), (f"cos({a}x)e^(sin({a}x))", "missed the innermost derivative"), (f"{a}e^(cos({a}x))", "differentiated inside the exponent only")]
        elif k == "lncos":
            f, ans = f"ln(cos({a}x))", f"-{a}tan({a}x)"
            w = [(f"1/cos({a}x)", "forgot the derivative of the inside"), (f"{a}tan({a}x)", "dropped the negative sign"), (f"-tan({a}x)", "missed the innermost derivative")]
        elif k == "sinsq":
            f, ans = f"sin²({a}x)", f"{2 * a}sin({a}x)cos({a}x)"
            w = [(f"2sin({a}x)cos({a}x)", "missed the innermost derivative"), (f"cos²({a}x)", "differentiated the inside only"), (f"{2 * a}sin({a}x)", "forgot the derivative of sin")]
        else:
            f, ans = f"cos({a}√x)", f"-{a}sin({a}√x)/(2√x)"
            w = [(f"-sin({a}√x)", "forgot the derivative of the inside"), (f"{a}sin({a}√x)/(2√x)", "dropped the negative sign"), (f"-{a}sin({a}√x)/√x", "forgot the 1/2 in the derivative of √x")]
    return I(f"Find f′(x) for f(x) = {f}.", ans, ["Chain rule: differentiate the outer function, keep the inside, then multiply by the derivative of the inside.", f"f′(x) = {ans}."], w,
             {"k": "deriv", "f": f}, "ch_fn")


def ch_table(r, L):
    a, ga, gpa, fpga = ri(r, -3, 4), ri(r, -4, 5), ri(r, -5, 6, True), ri(r, -6, 7, True)
    fpa, fga = ri(r, -6, 7, True), ri(r, -5, 6)
    need(ga != a and fpa != fpga and gpa != 1)
    if L < 2:
        ans = fpga * gpa
        p = (f"Let h(x) = f(g(x)). You know g({a}) = {ga}, g′({a}) = {gpa}, f′({a}) = {fpa}, and f′({ga}) = {fpga}. Find h′({a}).")
        st = [f"h′({a}) = f′(g({a})) · g′({a}).", f"= f′({ga}) · ({gpa}) = {ans}."]
        w = [(str(fpa * gpa), f"used f′({a}) instead of f′(g({a}))"), (str(fpga), "forgot to multiply by g′"), (str(fpga + gpa), "added instead of multiplying")]
        chk = {"k": "table", "kind": "fg", "fpga": fpga, "gpa": gpa}
    else:
        n = ri(r, 2, 4)
        ans = n * ga ** (n - 1) * gpa
        need(ga not in (0, 1))
        p = f"Let h(x) = (g(x)){sup(n)}. You know g({a}) = {ga} and g′({a}) = {gpa}. Find h′({a})."
        st = [f"h′(x) = {n}(g(x)){sup(n - 1) if n > 2 else ''} · g′(x).", f"h′({a}) = {n}({ga}){sup(n - 1) if n > 2 else ''}({gpa}) = {ans}."]
        w = [(str(n * ga ** (n - 1)), "forgot to multiply by g′"), (str(n * gpa ** (n - 1)), "used g′ inside the power"), (str(ga ** n * gpa), "did not lower the exponent")]
        chk = {"k": "table", "kind": "pow", "n": n, "ga": ga, "gpa": gpa}
    return I(p, str(ans), st, w, chk, "ch_table")


def ch_value(r, L):
    c, n, a = ri(r, -4, 4), ri(r, 2, 4) if L < 2 else ri(r, 3, 5), ri(r, -2, 2, True)
    q = poly({2: 1, 0: c}) if L > 0 else lin(ri(r, 2, 4), c)
    f = pw(q, n)
    # derivative value from the printed rule
    if L == 0:
        m = int(q.split("x")[0])
        inner_v = m * a + c
        ans = n * inner_v ** (n - 1) * m
        w = [(str(n * inner_v ** (n - 1)), "forgot the derivative of the inside"), (str(n * m * inner_v ** n), "kept the same exponent"), (str(inner_v ** n), "found f(a) instead of f′(a)")]
    else:
        inner_v = a * a + c
        ans = n * inner_v ** (n - 1) * 2 * a
        w = [(str(n * inner_v ** (n - 1)), "forgot the derivative of the inside"), (str(n * inner_v ** (n - 1) * 2), "used 2 instead of 2x for the inside's derivative"), (str(inner_v ** n), "found f(a) instead of f′(a)")]
    need(ans != 0 and abs(ans) < 5000)
    return I(f"Find f′({a}) for f(x) = {f}.", str(ans), ["Chain rule first, then substitute.", f"f′({a}) = {ans}."], w, {"k": "derivval", "f": f, "a": a}, "ch_value")


# =================================================================== Implicit differentiation
TRIPLES = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (0, 5, 5)]


def im_expr(r, L):
    if L == 0:
        a, b, c = ri(r, 1, 5), ri(r, 1, 5), ri(r, 10, 60)
        eq = f"{poly({2: a}, 'x')} + {poly({2: b}, 'y')} = {c}"
        k = F(a, b)
        def ratio(fr, top, bot):
            t = coef(fr.numerator, top)
            return f"-{t}/{bot}" if fr.denominator == 1 else f"-{t}/({fr.denominator}{bot})"
        ans = ratio(k, "x", "y")
        inv = F(b, a)
        w = [(ans[1:], "lost the negative sign"), (f"-{coef(k, 'x')}" if k.denominator == 1 else f"-{coef(k.numerator, 'x')}/{k.denominator}", "forgot to divide by y"),
             (ratio(inv, "y", "x"), "solved for dx/dy instead")]
        st = [f"Differentiate both sides: {2 * a}x + {2 * b}y(dy/dx) = 0.", f"dy/dx = {ans}."]
    elif L == 1:
        k = r.choice(["xy", "cubic"])
        c = ri(r, 3, 40)
        if k == "xy":
            eq = f"x² + xy + y² = {c}"
            ans = "-(2x + y)/(x + 2y)"
            w = [("-2x/(x + 2y)", "forgot the product rule on xy"), ("(2x + y)/(x + 2y)", "lost the negative sign"), ("-(2x + y)/(2y)", "differentiated xy as x(dy/dx) only")]
            st = ["2x + (y + x(dy/dx)) + 2y(dy/dx) = 0.", "(x + 2y)(dy/dx) = -(2x + y).", f"dy/dx = {ans}."]
        else:
            eq = f"x³ + y³ = {c}"
            ans = "-x²/y²"
            w = [("x²/y²", "lost the negative sign"), ("-x²", "forgot the dy/dx on the y³ term"), ("-y²/x²", "solved for dx/dy instead")]
            st = ["3x² + 3y²(dy/dx) = 0.", f"dy/dx = {ans}."]
    else:
        k = r.choice(["x2y", "ey", "siny", "xy2"])
        c = ri(r, 2, 30)
        if k == "x2y":
            eq = f"x²y + y³ = {c}"
            ans = "-2xy/(x² + 3y²)"
            w = [("-2x/(3y²)", "forgot the product rule on x²y"), ("2xy/(x² + 3y²)", "lost the negative sign"), ("-2xy/(3y²)", "dropped the x² dy/dx term")]
            st = ["2xy + x²(dy/dx) + 3y²(dy/dx) = 0.", f"dy/dx = {ans}."]
        elif k == "ey":
            eq = f"e^y + xy = {c}"
            ans = "-y/(e^y + x)"
            w = [("-y/e^y", "forgot the product rule on xy"), ("y/(e^y + x)", "lost the negative sign"), ("-(1 + y)/e^y", "differentiated xy as 1 + y")]
            st = ["e^y(dy/dx) + y + x(dy/dx) = 0.", f"dy/dx = {ans}."]
        elif k == "siny":
            eq = f"sin(y) + x² = {c}"
            ans = "-2x/cos(y)"
            w = [("2x/cos(y)", "lost the negative sign"), ("-2x", "forgot the dy/dx on sin(y)"), ("-2x cos(y)", "multiplied by cos(y) instead of dividing")]
            st = ["cos(y)(dy/dx) + 2x = 0.", f"dy/dx = {ans}."]
        else:
            eq = f"xy² - x² = {c}"
            ans = "(2x - y²)/(2xy)"
            w = [("2x/(2xy)", "forgot the y² term from the product rule"), ("(y² - 2x)/(2xy)", "flipped the signs"), ("(2x - y²)/(2y)", "dropped the x in 2xy(dy/dx)")]
            st = ["y² + 2xy(dy/dx) - 2x = 0.", f"dy/dx = {ans}."]
    return I(f"Use implicit differentiation to find dy/dx for {eq}.", ans, st, w, {"k": "implicit", "eq": eq}, "im_expr")


def im_slope(r, L):
    if L == 0:
        p, q, rr = r.choice(TRIPLES[:4])
        sx, sy = r.choice([1, -1]), r.choice([1, -1])
        x0, y0 = sx * p, sy * q
        eq = f"x² + y² = {rr * rr}"
        ans = F(-x0, y0)
        w = [(num(-ans), "lost the negative sign"), (num(F(-y0, x0)), "used -y/x"), (num(F(y0, x0)), "used the slope of the radius")]
        st = ["dy/dx = -x/y.", f"At ({x0}, {y0}): dy/dx = {num(ans)}."]
    elif L == 1:
        while True:
            x0, y0 = ri(r, -3, 3, True), ri(r, -3, 3, True)
            if x0 + 2 * y0 != 0:
                break
        c = x0 * x0 + x0 * y0 + y0 * y0
        eq = f"x² + xy + y² = {c}"
        ans = F(-(2 * x0 + y0), x0 + 2 * y0)
        need(ans != 0)
        w = [(num(-ans), "lost the negative sign"), (num(F(-2 * x0, x0 + 2 * y0)), "forgot the product rule on xy"), (num(F(-(x0 + 2 * y0), 2 * x0 + y0)), "flipped the fraction")]
        st = ["dy/dx = -(2x + y)/(x + 2y).", f"At ({x0}, {y0}): dy/dx = {num(ans)}."]
    else:
        x0, y0 = ri(r, -3, 3, True), ri(r, 1, 3)
        c = x0 * x0 * y0 + y0 ** 3
        eq = f"x²y + y³ = {c}"
        ans = F(-2 * x0 * y0, x0 * x0 + 3 * y0 * y0)
        w = [(num(-ans), "lost the negative sign"), (num(F(-2 * x0, 3 * y0 * y0)), "forgot the product rule on x²y"), (num(F(-2 * x0 * y0, 3 * y0 * y0)), "dropped the x² dy/dx term")]
        st = ["dy/dx = -2xy/(x² + 3y²).", f"At ({x0}, {y0}): dy/dx = {num(ans)}."]
    return I(f"Find the slope of the tangent line to {eq} at the point ({x0}, {y0}).", num(ans), st, w, {"k": "implicitval", "eq": eq, "x": x0, "y": y0}, "im_slope")


# =================================================================== Inverse functions
def inv_trig(r, L):
    a = ri(r, 2, 6)
    if L == 0:
        k = r.choice(["asin", "atan"])
        if k == "asin":
            f, ans = f"sin⁻¹({a}x)", f"{a}/√(1 - {a * a}x²)"
            w = [(f"1/√(1 - {a * a}x²)", "forgot the chain rule"), (f"{a}/(1 + {a * a}x²)", "used the arctangent rule"), (f"-{a}/√(1 - {a * a}x²)", "used the arccosine sign")]
        else:
            f, ans = f"tan⁻¹({a}x)", f"{a}/(1 + {a * a}x²)"
            w = [(f"1/(1 + {a * a}x²)", "forgot the chain rule"), (f"{a}/√(1 - {a * a}x²)", "used the arcsine rule"), (f"{a}sec²({a}x)", "differentiated tan instead of tan⁻¹")]
    elif L == 1:
        k = r.choice(["atan2", "asinx"])
        if k == "atan2":
            f, ans = "tan⁻¹(x²)", "2x/(1 + x⁴)"
            w = [("1/(1 + x⁴)", "forgot the chain rule"), ("2x/(1 + x²)", "did not square the inside"), ("2x/√(1 - x⁴)", "used the arcsine rule")]
        else:
            f, ans = f"sin⁻¹(x/{a})", f"1/√({a * a} - x²)"
            w = [(f"1/√(1 - x²)", "ignored the inside"), (f"{a}/√({a * a} - x²)", "multiplied by a instead of 1/a"), (f"1/({a * a} + x²)", "used the arctangent rule")]
    else:
        k = r.choice(["xatan", "asine"])
        if k == "xatan":
            f, ans = f"x tan⁻¹({a}x)", f"tan⁻¹({a}x) + {a}x/(1 + {a * a}x²)"
            w = [(f"{a}x/(1 + {a * a}x²)", "forgot the product rule"), (f"tan⁻¹({a}x) + x/(1 + {a * a}x²)", "forgot the chain rule"), (f"{a}/(1 + {a * a}x²)", "differentiated only tan⁻¹")]
        else:
            f, ans = "sin⁻¹(e^x)", "e^x/√(1 - e^(2x))"
            w = [("1/√(1 - e^(2x))", "forgot the chain rule"), ("e^x/√(1 - e^x)", "did not square e^x"), ("e^x/(1 + e^(2x))", "used the arctangent rule")]
    dom = "neg" if "e^x" in f else "small"
    return I(f"Find f′(x) for f(x) = {f}.", ans, [f"Use (sin⁻¹ u)′ = u′/√(1 - u²) or (tan⁻¹ u)′ = u′/(1 + u²).", f"f′(x) = {ans}."], w, {"k": "deriv", "f": f, "dom": dom}, "inv_trig")


def inv_point(r, L):
    for _ in range(50):
        b, c, a = ri(r, 1, 6), ri(r, -6, 6), ri(r, -2, 2)
        if L == 2:
            d = ri(r, 1, 3)
            f = poly({3: 1, 1: b, 0: c}) if r.random() < 0.5 else poly({5: 1, 3: d, 1: b, 0: c})
            cs = {3: 1, 1: b, 0: c} if f.count("⁵") == 0 else {5: 1, 3: d, 1: b, 0: c}
        else:
            f, cs = poly({3: 1, 1: b, 0: c}), {3: 1, 1: b, 0: c}
        fa = sum(v * a ** p for p, v in cs.items())
        fpa = sum(v * p * a ** (p - 1) for p, v in cs.items() if p)
        fpfa = sum(v * p * fa ** (p - 1) for p, v in cs.items() if p)
        if fa != a and fpa not in (0, 1) and fpfa != fpa:
            break
    ans = F(1, fpa)
    w = [(str(fpa), "forgot to take the reciprocal"), (num(F(1, fpfa)), f"evaluated f′ at {fa} instead of at {a}"), (num(-ans), "added a negative sign")]
    st = [f"f({a}) = {fa}, so f⁻¹({fa}) = {a}.", f"(f⁻¹)′({fa}) = 1/f′({a}) = 1/{fpa} = {num(ans)}."]
    return I(f"Let f(x) = {f}, which is one-to-one. Find (f⁻¹)′({fa}).", num(ans), st, w, {"k": "invpoint", "f": f, "b": fa}, "inv_point")


def inv_table(r, L):
    a, fa, fpa, fpfa = ri(r, -3, 5), ri(r, -4, 8), ri(r, -6, 7, True), ri(r, -6, 7, True)
    need(fa != a and abs(fpa) != 1 and fpa != fpfa)
    ans = F(1, fpa)
    p = f"f is differentiable and one-to-one with f({a}) = {fa}, f′({a}) = {fpa}, and f′({fa}) = {fpfa}. Let g be the inverse of f. Find g′({fa})."
    w = [(str(fpa), "forgot to take the reciprocal"), (num(F(1, fpfa)), f"used f′({fa}) instead of f′({a})"), (num(-ans), "added a negative sign")]
    return I(p, num(ans), [f"g({fa}) = {a}.", f"g′({fa}) = 1/f′(g({fa})) = 1/f′({a}) = {num(ans)}."], w, {"k": "invtable", "fpa": fpa}, "inv_table")


# =================================================================== L'Hôpital's Rule
def lh(r, L):
    a, b = ri(r, 2, 7), ri(r, 2, 7)
    if L == 0:
        k = r.choice(["sin", "exp", "ratio", "pow"])
        if k == "sin":
            need(a != b)
            e, at, ans = f"sin({a}x)/({b}x)", "0", F(a, b)
            w = [(num(F(b, a)), "flipped the ratio"), ("0", "substituted sin(0) = 0 only in the numerator"), ("1", "assumed sin(u)/u is always 1")]
        elif k == "exp":
            e, at, ans = f"(e^({a}x) - 1)/x", "0", F(a)
            w = [("1", "forgot the chain rule on e^(ax)"), ("0", "stopped at 0/0"), (num(F(1, a)), "flipped the ratio")]
        elif k == "ratio":
            c, d = ri(r, -9, 9), ri(r, -9, 9)
            need(a != b)
            e, at, ans = f"({poly({2: a, 1: c})} + 1)/({poly({2: b, 0: d})})", "∞", F(a, b)
            w = [(num(F(b, a)), "flipped the ratio"), ("0", "thought the larger constant term wins"), ("∞", "stopped at ∞/∞")]
        else:
            n = ri(r, 2, 4)
            e, at, ans = f"(x{sup(n)} - {a ** n})/(x - {a})", str(a), F(n * a ** (n - 1))
            w = [(str(n * a ** n), "used xⁿ instead of nxⁿ⁻¹"), (str(n), "forgot to substitute x"), ("0", "stopped at 0/0")]
    elif L == 1:
        k = r.choice(["lnx_inf", "xe", "tan", "expsin", "sqrt", "lnxa"])
        if k == "lnxa":
            e, at, ans = f"ln(x/{a})/(x - {a})", str(a), F(1, a)
            w = [("0", "stopped at 0/0"), (str(a), "flipped the result"), ("1", "forgot the chain rule on x/a")]
        elif k == "lnx_inf":
            e, at, ans = f"ln(x)/({a}x)", "∞", F(0)
            w = [(num(F(1, a)), "kept the 1/x"), ("∞", "stopped at ∞/∞"), (str(a), "differentiated incorrectly")]
        elif k == "xe":
            e, at, ans = f"x{sup(a)}/e^({b}x)", "∞", F(0)
            w = [("∞", "stopped at ∞/∞"), ("1", "thought the powers cancel"), (num(F(a, b)), "applied the rule only once")]
        elif k == "tan":
            need(a != b)
            e, at, ans = f"tan({a}x)/({b}x)", "0", F(a, b)
            w = [(num(F(b, a)), "flipped the ratio"), ("0", "stopped at 0/0"), (num(F(1, b)), "forgot the chain rule on tan")]
        elif k == "expsin":
            need(a != b)
            e, at, ans = f"(e^({a}x) - 1)/sin({b}x)", "0", F(a, b)
            w = [(num(F(b, a)), "flipped the ratio"), (num(F(1, b)), "forgot the chain rule on e^(ax)"), ("0", "stopped at 0/0")]
        else:
            e, at, ans = f"(√(x + {a * a}) - {a})/x", "0", F(1, 2 * a)
            w = [(num(F(1, a)), "forgot the 1/2 in the derivative of √"), ("0", "stopped at 0/0"), (str(2 * a), "flipped the result")]
    else:
        k = r.choice(["cos", "sinax3", "lnquad", "exp2", "tanax3"])
        if k == "cos":
            e, at, ans = f"(1 - cos({a}x))/x²", "0", F(a * a, 2)
            w = [(num(F(a, 2)), "forgot the chain rule the second time"), (str(a * a), "forgot the 1/2"), ("0", "applied the rule only once")]
        elif k == "sinax3":
            a = ri(r, 1, 4)
            e, at, ans = (f"(x - sin(x))/x³" if a == 1 else f"({a}x - sin({a}x))/x³"), "0", F(a ** 3, 6)
            w = [("0", "stopped too early"), (num(F(a ** 2, 6)) if a > 1 else "1/2", "missed a chain-rule factor or the 3 from (x³)′"), (num(F(a ** 3, 3)), "applied the rule only twice")]
        elif k == "tanax3":
            a = ri(r, 1, 4)
            e, at, ans = (f"(tan(x) - x)/x³" if a == 1 else f"(tan({a}x) - {a}x)/x³"), "0", F(a ** 3, 3)
            w = [("0", "stopped too early"), (num(F(a ** 3, 6)), "used the sine value by mistake"), (num(F(a ** 3, 1)), "forgot the 3 from (x³)′")]
        elif k == "exp2":
            e, at, ans = f"(e^({a}x) - 1 - {a}x)/x²", "0", F(a * a, 2)
            w = [(str(a * a), "forgot the 1/2"), (num(F(a, 2)), "missed a chain-rule factor"), ("0", "applied the rule only once")]
        else:
            e, at, ans = f"ln(1 + {a}x)/x", "0", F(a)
            w = [("1", "forgot the chain rule"), (num(F(1, a)), "flipped the ratio"), ("0", "stopped at 0/0")]
    p = f"Use L'Hôpital's Rule to evaluate lim (x → {at}) {e}."
    form = "∞/∞" if at == "∞" else "0/0"
    return I(p, num(ans), [f"Direct substitution gives {form}.", "Differentiate the numerator and the denominator separately (repeat if needed).", f"The limit is {num(ans)}."],
             w, {"k": "limit", "e": e, "at": at}, "lh")


def lh_check(r, L):
    a = ri(r, 2, 6)
    opts = [(f"sin({a}x)/x", "0", True), (f"(x² - {a * a})/(x - {a})", str(a), True), (f"(x + {a})/(x - {a})", str(a), False), (f"cos(x)/x", "0", False),
            (f"(e^x - 1)/x²", "0", True), (f"(x² + 1)/(x + {a})", str(a), False)]
    e, at, ok = r.choice(opts)
    p = f"Can L'Hôpital's Rule be applied directly to lim (x → {at}) {e}?"
    ans = "Yes, substitution gives 0/0." if ok else "No, substitution does not give 0/0 or ∞/∞."
    w = [("No, substitution does not give 0/0 or ∞/∞." if ok else "Yes, substitution gives 0/0.", "did not check the form first"),
         ("Yes, L'Hôpital's Rule works on any quotient.", "applied the rule without checking the form"), ("No, the rule only works for limits at ∞.", "misremembered when the rule applies")]
    return I(p, ans, ["Substitute first: the rule applies only to 0/0 or ∞/∞.", ans], w, {"k": "lhform", "e": e, "at": at}, "lh_check")


# =================================================================== Integration by substitution
def us_poly(r, L):
    c, n = ri(r, 1, 9), ri(r, 2, 6)
    q = poly({2: 1, 0: c})
    if L == 0:
        g = f"2x{pw(q, n)}"
        ans = f"(1/{n + 1}){pw(q, n + 1)} + C"
        w = [(f"{pw(q, n + 1)} + C", "forgot to divide by the new exponent"), (f"(1/{n + 1})x²{pw(q, n + 1)} + C", "integrated only part of the integrand"), (f"{n}{pw(q, n - 1)} + C", "differentiated instead of integrating")]
        st = [f"Let u = {q}, so du = 2x dx.", f"∫ u{sup(n)} du = (1/{n + 1})u{sup(n + 1)} + C.", f"= {ans}."]
    elif L == 1:
        g = f"x{pw(q, n)}"
        ans = f"(1/{2 * (n + 1)}){pw(q, n + 1)} + C"
        w = [(f"(1/{n + 1}){pw(q, n + 1)} + C", "forgot the 1/2 from du = 2x dx"), (f"(1/{2 * n}){pw(q, n)} + C", "did not raise the exponent"), (f"(x²/2)(1/{n + 1}){pw(q, n + 1)} + C", "integrated x separately")]
        st = [f"Let u = {q}, so x dx = (1/2) du.", f"(1/2)∫ u{sup(n)} du = (1/{2 * (n + 1)})u{sup(n + 1)} + C.", f"= {ans}."]
    else:
        a = ri(r, 2, 5)
        q = poly({3: 1, 0: c})
        g = f"x²{pw(q, n)}" if r.random() < 0.5 else f"x²/√({q})"
        if "√" in g:
            ans = f"(2/3)√({q}) + C"
            w = [(f"2√({q}) + C", "forgot the 1/3 from du = 3x² dx"), (f"(1/3)√({q}) + C", "forgot that ∫ u^(-1/2) du = 2u^(1/2)"), (f"(1/3)ln({q}) + C", "treated it like ∫ du/u")]
            st = [f"Let u = {q}, so x² dx = (1/3) du.", "(1/3)∫ u^(-1/2) du = (2/3)u^(1/2) + C.", f"= {ans}."]
        else:
            ans = f"(1/{3 * (n + 1)}){pw(q, n + 1)} + C"
            w = [(f"(1/{n + 1}){pw(q, n + 1)} + C", "forgot the 1/3 from du = 3x² dx"), (f"(1/{3 * n}){pw(q, n)} + C", "did not raise the exponent"), (f"(x³/3)(1/{n + 1}){pw(q, n + 1)} + C", "integrated x² separately")]
            st = [f"Let u = {q}, so x² dx = (1/3) du.", f"(1/3)∫ u{sup(n)} du = (1/{3 * (n + 1)})u{sup(n + 1)} + C.", f"= {ans}."]
    return I(f"Find ∫ {g} dx.", ans, st, w, {"k": "anti", "g": g}, "us_poly")


def us_fn(r, L):
    a = ri(r, 2, 7)
    if L == 0:
        k = r.choice(["cos", "sin", "exp"])
        if k == "cos":
            g, ans = f"cos({a}x)", f"(1/{a})sin({a}x) + C"
            w = [(f"sin({a}x) + C", "forgot to divide by the inside's derivative"), (f"{a}sin({a}x) + C", "multiplied instead of dividing"), (f"-(1/{a})sin({a}x) + C", "added a negative sign")]
        elif k == "sin":
            g, ans = f"sin({a}x)", f"-(1/{a})cos({a}x) + C"
            w = [(f"-cos({a}x) + C", "forgot to divide by the inside's derivative"), (f"(1/{a})cos({a}x) + C", "dropped the negative sign"), (f"-{a}cos({a}x) + C", "multiplied instead of dividing")]
        else:
            g, ans = f"e^({a}x)", f"(1/{a})e^({a}x) + C"
            w = [(f"e^({a}x) + C", "forgot to divide by the inside's derivative"), (f"{a}e^({a}x) + C", "multiplied instead of dividing"), (f"(1/({a}x + 1))e^({a}x + 1) + C", "used the power rule on e")]
    elif L == 1:
        c = ri(r, 1, 9)
        k = r.choice(["xexp", "frac", "xcos"])
        if k == "xexp":
            g, ans = "xe^(x²)", "(1/2)e^(x²) + C"
            w = [("e^(x²) + C", "forgot the 1/2"), ("2e^(x²) + C", "multiplied by 2 instead of dividing"), ("(x²/2)e^(x²) + C", "integrated x separately")]
        elif k == "frac":
            g, ans = f"2x/(x² + {c})", f"ln(x² + {c}) + C"
            w = [(f"2ln(x² + {c}) + C", "kept the 2"), (f"(1/2)ln(x² + {c}) + C", "divided by 2 again"), (f"x²ln(x² + {c}) + C", "integrated the numerator separately")]
        else:
            g, ans = f"x cos(x² + {c})", f"(1/2)sin(x² + {c}) + C"
            w = [(f"sin(x² + {c}) + C", "forgot the 1/2"), (f"-(1/2)sin(x² + {c}) + C", "used the derivative of cos"), (f"(x²/2)sin(x² + {c}) + C", "integrated x separately")]
    else:
        n = ri(r, 2, 4)
        k = r.choice(["sincos", "tan", "lnx"])
        if k == "sincos":
            g, ans = f"sin{sup(n)}(x)cos(x)" if n <= 4 else "", f"(1/{n + 1})sin{sup(n + 1)}(x) + C"
            need(n + 1 <= 4)
            w = [(f"sin{sup(n + 1)}(x) + C", "forgot to divide by the new exponent"), (f"-(1/{n + 1})cos{sup(n + 1)}(x) + C", "chose u = cos(x) without the negative sign"), (f"(1/{n + 1})sin{sup(n + 1)}(x)cos(x) + C", "left the cos(x) in")]
        elif k == "tan":
            g, ans = f"sin({a}x)/cos({a}x)", f"-(1/{a})ln|cos({a}x)| + C"
            w = [(f"-ln|cos({a}x)| + C", "forgot to divide by the inside's derivative"), (f"(1/{a})ln|cos({a}x)| + C", "dropped the negative sign"), (f"(1/{a})sec²({a}x) + C", "differentiated instead of integrating")]
        else:
            g, ans = f"(ln(x)){sup(n)}/x", f"(1/{n + 1})(ln(x)){sup(n + 1)} + C"
            w = [(f"(ln(x)){sup(n + 1)} + C", "forgot to divide by the new exponent"), (f"(1/{n + 1})(ln(x)){sup(n + 1)}/x + C", "left the 1/x in"), (f"{n}(ln(x)){sup(n - 1)}/x² + C", "differentiated instead of integrating")]
    return I(f"Find ∫ {g} dx.", ans, ["Choose u = the inside expression, so du appears in the integrand.", f"= {ans}."], w, {"k": "anti", "g": g}, "us_fn")


def us_def(r, L):
    if L < 2:
        c, n, b = ri(r, 0, 3), ri(r, 1, 3), ri(r, 1, 2)
        q = poly({2: 1, 0: c})
        g = f"2x{pw(q, n)}"
        top, bot = b * b + c, c
        ans = F(top ** (n + 1) - bot ** (n + 1), n + 1)
        w = [(num(F(top ** (n + 1), n + 1)), "forgot to subtract the lower limit"), (num(F(top ** (n + 1) + bot ** (n + 1), n + 1)), "added the value at the lower limit"),
             (num(top ** (n + 1) - bot ** (n + 1)), "forgot to divide by the new exponent")]
        st = [f"Let u = {q}. When x = 0, u = {bot}; when x = {b}, u = {top}.", f"∫ from {bot} to {top} u{sup(n)} du = [u{sup(n + 1)}/{n + 1}] = {num(ans)}."]
        p = f"Evaluate ∫ from 0 to {b} {g} dx."
        lo, hi = "0", str(b)
    else:
        k = r.choice(["xe", "cos"])
        if k == "xe":
            p, g, lo, hi, ans_t = "Evaluate ∫ from 0 to 1 xe^(x²) dx.", "xe^(x²)", "0", "1", "(e - 1)/2"
            w = [("e - 1", "forgot the 1/2"), ("e/2", "forgot to subtract the lower limit"), ("(e - 1)/4", "divided by 2 twice")]
            st = ["Let u = x², so x dx = (1/2) du; u runs from 0 to 1.", "(1/2)∫ from 0 to 1 e^u du = (e - 1)/2."]
            return I(p, ans_t, st, w, {"k": "defint", "g": g, "lo": lo, "hi": hi}, "us_def")
        a = ri(r, 2, 3)
        p, g, lo, hi = f"Evaluate ∫ from 0 to π/{2 * a} cos({a}x) dx.", f"cos({a}x)", "0", f"π/{2 * a}"
        ans = F(1, a)
        w = [("1", "forgot to divide by the inside's derivative"), (str(a), "multiplied instead of dividing"), (num(-ans), "used the wrong sign for the antiderivative")]
        st = [f"Let u = {a}x; u runs from 0 to π/2.", f"(1/{a})∫ from 0 to π/2 cos(u) du = (1/{a})(1 - 0) = {num(ans)}."]
    return I(p, num(ans), st, w, {"k": "defint", "g": g, "lo": lo, "hi": hi}, "us_def")


SKILLS = {
    ("calculus", "derivatives", "The Chain Rule"): ([ch_pow, ch_fn, ch_value, ch_table], ["AP FUN-3.C"]),
    ("calculus", "derivatives", "Implicit Differentiation"): ([im_expr, im_slope], ["AP FUN-3.D"]),
    ("calculus", "derivatives", "Derivatives of Inverse Functions"): ([inv_trig, inv_point, inv_table], ["AP FUN-3.E"]),
    ("calculus", "applications-derivatives", "L'Hôpital's Rule"): ([lh, lh_check], ["AP LIM-4.A"]),
    ("calculus", "fundamental-theorem-calculus", "Integration by Substitution"): ([us_poly, us_fn, us_def], ["AP FUN-6.D"]),
}
