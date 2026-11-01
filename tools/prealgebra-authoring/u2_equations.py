"""Unit 2 — Equations and Expressions (equations-expressions)."""
from lib import *

UNIT_ID = "equations-expressions"
ABBR = "eqx"


def eqtxt(A, B, C, D_, v="x"):
    return f"{lin((A, v), (B, ''))} = {lin((C, v), (D_, ''))}"


# ======================================================================= S1 Expressions with radical exponents
SQ = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
CB = [1, 8, 27, 64, 125, 216, 343, 512, 729, 1000]


@fam("012")
def s1_numeric(r, L):
    a, c = pick(r, SQ[1:]), pick(r, CB[1:6])
    b, e = r.randint(2, 5), pick(r, [2, 3])
    sa, cc = math.isqrt(a), round(c ** (1 / 3))
    forms = [(f"√{a} + {b}{sup(e)}", sa + b ** e, [sa + b * e, a + b ** e, sa * b ** e]),
             (f"{b}{sup(2)} - ∛{c}", b * b - cc, [2 * b - cc, b * b - c // 3 if c % 3 == 0 else b * b - c, b * b + cc])] if L == 0 else \
            [(f"{b} · ∛{c} - √{a}", b * cc - sa, [b * c - sa, b * cc + sa, cc - sa]),
             (f"(√{a}){sup(2)} ÷ {b}", F(a, b), [F(sa, b), F(a * a, b), F(2 * sa, b)]),
             (f"∛{c} · {b}{sup(2)} + √{a}", cc * b * b + sa, [cc * 2 * b + sa, cc * b * b * sa, cc * b * b - sa])] if L == 1 else \
            [(lambda t: (f"√({t[0]}{sup(2)} + {t[1]}{sup(2)})", F(t[2]), [F(t[0] + t[1]), F(t[0] ** 2 + t[1] ** 2), F(t[2] * t[2])]))(pick(r, [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20)])),
             (f"∛({b}{sup(6)})", F(b * b), [F(b ** 2 * b), F(b * 2), F(b ** 3)]),
             (f"√({b}{sup(4)}) + ∛({b}{sup(3)})", F(b * b + b), [F(b ** 4 + b ** 3), F(2 * b), F(b ** 2 * b)])]
    e_, v, wr = pick(r, forms)
    return P(f"Evaluate: {e_}", N(v), ["Evaluate roots and powers before adding, subtracting, multiplying or dividing (grouping symbols first).", f"{e_} = {N(v)}."],
             [N(w) for w in wr], chk_val(e_), tags=["misconception"] if L == 2 else [])


@fam("012")
def s1_substitute(r, L):
    x = r.randint(2, 9) * (pick(r, [1, -1]) if L == 2 else 1)
    if L == 0:
        a = pick(r, [k for k in SQ if k > x * x and math.isqrt(k) ** 2 == k] or [100])
        e_, v = f"√(x + {a - x})", F(math.isqrt(a))
        need(a - x > 0)
        wr = [F(math.isqrt(a)) + 1, F(x + math.isqrt(a - x)) if math.isqrt(a - x) ** 2 == a - x else F(a), F(a)]
    elif L == 1:
        t = pick(r, [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)])
        x = t[0]
        e_, v = f"√(x{sup(2)} + {t[1] ** 2})", F(t[2])
        wr = [F(x + t[1]), F(x * x + t[1] ** 2), F(x + t[1] ** 2)]
    else:
        c = pick(r, [2, 3, 4])
        e_, v = f"∛(x{sup(3)}) + √(x{sup(2)}) + {c}", F(x + abs(x) + c)
        wr = [F(2 * x + c), F(c), F(x * x + c)]
    return P(f"Evaluate {e_} when x = {x}.", N(v), [f"Substitute x = {x}: {e_.replace('x', paren(x))}.", f"= {N(v)}."] +
             (["Note √(x²) is never negative: √(x²) = |x|, while ∛(x³) = x."] if L == 2 else []),
             [N(w) for w in wr], chk_val(e_.replace("x", f"({x})")), tags=["misconception"] if L == 2 else [])


@fam("12")
def s1_simplify_var(r, L):
    v = pick(r, ["x", "y", "a", "m"])
    k, e = pick(r, [1, 2, 3, 4, 5, 6, 7, 9, 10]), r.randint(1, 5)
    if r.random() < 0.55:
        expr = f"√({k * k if k > 1 else ''}{v}{sup(2 * e)})"
        ans = f"{k if k > 1 else ''}{pw(v, e)}"
        wrong = [f"{k * k if k > 1 else ''}{pw(v, e)}" if k > 1 else f"{pw(v, 2 * e)}", f"{k if k > 1 else ''}{pw(v, e * e) if e > 1 else v + sup(2)}", f"{k if k > 1 else ''}{pw(v, 2 * e - 2) if e > 1 else v + sup(4)}"]
    else:
        kk = pick(r, [1, 2, 3, 4, 5]) * (pick(r, [1, -1]) if L == 2 else 1)
        expr = f"∛({kk ** 3 if abs(kk) > 1 else ('-' if kk < 0 else '')}{v}{sup(3 * e)})"
        ans = f"{kk if abs(kk) > 1 else ('-' if kk < 0 else '')}{pw(v, e)}"
        wrong = [f"{kk ** 3 if abs(kk) > 1 else ''}{pw(v, e)}", f"{kk if abs(kk) > 1 else ''}{pw(v, 3 * e - 3) if e > 1 else v + sup(3)}", f"{-kk if abs(kk) > 1 else ('' if kk < 0 else '-')}{pw(v, e)}"]
    return P(f"Simplify {expr}. Assume {v} > 0.", ans, ["Take the root of the coefficient and divide the exponent by the index of the root.", f"{expr} = {ans}."],
             wrong, {"kind": "equiv", "expr": expr, "vars": [v]}, tags=["connections"])


@fam("012")
def s1_inverse(r, L):
    n = r.randint(2, 30)
    forms = [(f"(√{n}){sup(2)}", F(n), [F(2 * n), F(n * n), F(n, 2)])] if L == 0 else \
            [(f"(∛{n}){sup(3)}", F(n), [F(3 * n), F(n ** 3), F(n, 3)]), (f"∛(({-n}){sup(3)})", F(-n), [F(n), F(-3 * n), F(n * n)])]
    if L == 2:
        k = r.randint(2, 12)
        typ = pick(r, ["sq", "cb"])
        if typ == "sq":
            return P(f"If √n = {k}, what is n?", f"n = {k * k}", [f"Square both sides: n = {k}² = {k * k}."], [f"n = {2 * k}", f"n = {k}", f"n = √{k}"],
                     chk_py("sqrt_reverse", k=k, index=2), tags=["reasoning"])
        return P(f"If ∛m = -{k}, what is m?", f"m = {-k ** 3}", [f"Cube both sides: m = (-{k})³ = {-k ** 3}."], [f"m = {k ** 3}", f"m = {-3 * k}", f"m = {-k * k}"],
                 chk_py("sqrt_reverse", k=-k, index=3), tags=["reasoning"])
    e_, v, wr = pick(r, forms)
    return P(f"Evaluate: {e_}", N(v), ["Squaring undoes a square root, and cubing undoes a cube root.", f"{e_} = {N(v)}."], [N(w) for w in wr], chk_val(e_))


@fam("12")
def s1_area_volume(r, L):
    k = r.randint(2, 9)
    e = r.randint(1, 3)
    v = pick(r, ["x", "y"])
    if r.random() < 0.5:
        return P(f"A square has area {k * k}{pw(v, 2 * e)} square units ({v} > 0). Write an expression for its side length.", f"{k}{pw(v, e)}",
                 [f"Side = √({k * k}{pw(v, 2 * e)}) = {k}{pw(v, e)}."], [f"{k * k}{pw(v, e)}", f"{k}{pw(v, 2 * e)}", f"{k * k // 2 if k % 2 == 0 else 2 * k}{pw(v, e)}"],
                 {"kind": "equiv", "expr": f"√({k * k}{pw(v, 2 * e)})", "vars": [v]}, tags=["modeling", "connections"])
    return P(f"A cube has volume {k ** 3}{pw(v, 3 * e)} cubic units ({v} > 0). Write an expression for the length of one edge.", f"{k}{pw(v, e)}",
             [f"Edge = ∛({k ** 3}{pw(v, 3 * e)}) = {k}{pw(v, e)}."], [f"{k ** 3}{pw(v, e)}", f"{k}{pw(v, 3 * e)}", f"{3 * k}{pw(v, e)}"],
             {"kind": "equiv", "expr": f"∛({k ** 3}{pw(v, 3 * e)})", "vars": [v]}, tags=["modeling", "connections"])


@fam("2", mode="mc")
def s1_abs_root(r, L):
    k = r.randint(2, 9)
    opts = [(f"x = -{k}", True), (f"x = {k}", False), ("x = 0", False), (f"x = {k * k}", False)]
    r.shuffle(opts)
    return P("For which value of x is √(x²) NOT equal to x?", f"x = -{k}",
             [f"√((-{k})²) = √{k * k} = {k}, which is not -{k}.", "For x ≥ 0, √(x²) = x. The principal square root is never negative."],
             options=opts, chk=chk_py("sqrt_sq_ne"), tags=["reasoning", "misconception"], mode="mc")


@fam("012")
def s1_error(r, L):
    a, b = pick(r, [(3, 4), (6, 8), (5, 12), (8, 6), (9, 12)])
    opts = [(str(math.isqrt(a * a + b * b)), True), (str(a + b), False), (str(a * a + b * b), False), (str(abs(a - b)), False)]
    r.shuffle(opts)
    return P(f"Pat simplified √({a}² + {b}²) as {a} + {b} = {a + b}. What is the correct value?", str(math.isqrt(a * a + b * b)),
             ["A square root does not distribute over addition.", f"{a}² + {b}² = {a * a} + {b * b} = {a * a + b * b}.", f"√{a * a + b * b} = {math.isqrt(a * a + b * b)}."],
             options=opts, chk=chk_val(f"√({a}^2 + {b}^2)"), tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s1_select(r, L):
    k = r.randint(2, 6)
    good = [f"√{k ** 4}", f"(√{k}){sup(4)}", f"∛({k}{sup(6)})", f"{k}{sup(2)}"]
    bad = [f"√{2 * k}", f"{k}{sup(3)}", f"∛{k * k}", f"2{sup(k)}" if 2 ** k != k * k else f"{2 * k}"]
    opts = [(g, True) for g in pick(r, good, 3)] + [(b, False) for b in pick(r, bad, 3)]
    return P(f"Select ALL expressions equal to {k * k}.", None, [f"√{k ** 4} = {k * k}; (√{k})⁴ = {k}² = {k * k}; ∛({k}⁶) = {k}² = {k * k}."],
             options=opts, chk=chk_val(str(k * k)), tags=["multiple-representations"])


@fam("012")
def s1_open(r, L):
    k = r.randint(2, 6)
    n = pick(r, [2, 3, 5, 6, 7])
    return P(f"Use the relationship between powers and roots.", None,
             [f"{k}² = {k * k}.", f"{k}³ = {k ** 3}.", "Squaring undoes the square root.", "√(x²) = |x|."],
             parts=[(f"Evaluate √{k * k}.", str(k), chk_val(f"√{k * k}")), (f"Evaluate ∛{k ** 3}.", str(k), chk_val(f"∛{k ** 3}")),
                    (f"Evaluate (√{n})².", str(n), chk_val(f"(√{n})^2")), (f"Evaluate √((-{k})²).", str(k), chk_val(f"√((-{k})^2)"))], tags=["reasoning"])


# ======================================================================= S2 Expressions with integer exponents
def mono(c, v, e):
    if e == 0:
        return N(c)
    cs = "" if c == 1 else "-" if c == -1 else N(c)
    return f"{cs}{pw(v, e)}"


@fam("012")
def s2_product(r, L):
    v = pick(r, ["x", "y", "a", "n"])
    a, b = r.randint(2, 7) * (pick(r, [1, -1]) if L else 1), r.randint(2, 6)
    e1, e2 = r.randint(1, 6), r.randint(1, 6)
    expr = f"({mono(a, v, e1)})({mono(b, v, e2)})"
    if L == 2:
        c, e3 = nz(r, -4, 4), r.randint(1, 3)
        expr += f"({mono(c, v, e3)})"
        a, e1 = a * c, e1 + e3
    ans = mono(a * b, v, e1 + e2)
    wrong = [mono(a * b, v, e1 * e2), mono(a + b, v, e1 + e2), mono(a * b, v, e1 + e2 + 1) if L < 2 else mono(-a * b, v, e1 + e2)]
    return P(f"Simplify: {expr}", ans, ["Multiply the coefficients and add the exponents of the same base.", f"{expr} = {ans}."], wrong,
             {"kind": "equiv", "expr": expr, "vars": [v], "strip": False}, tags=["misconception"])


@fam("012")
def s2_quotient(r, L):
    v = pick(r, ["x", "y", "b", "m"])
    q, d = r.randint(2, 8) * (pick(r, [1, -1]) if L else 1), r.randint(2, 6)
    e2 = r.randint(1, 5)
    e1 = e2 + r.randint(0 if L == 2 else 1, 6)
    expr = f"{mono(q * d, v, e1)} ÷ ({mono(d, v, e2)})" if L < 2 else f"{mono(q * d, v, e1)} ÷ ({mono(-d, v, e2)})"
    qq = q if L < 2 else -q
    ans = mono(qq, v, e1 - e2)
    wrong = [mono(qq, v, e1 + e2), mono(q * d - d, v, e1 - e2) if q * d - d else mono(qq * d, v, e1 - e2), mono(-qq, v, e1 - e2)]
    return P(f"Simplify: {expr}", ans, ["Divide the coefficients and subtract the exponents of the same base.", f"{expr} = {ans}." + (" Any nonzero number to the 0 power is 1." if e1 == e2 else "")],
             wrong, {"kind": "equiv", "expr": expr, "vars": [v], "strip": False}, tags=["misconception"])


@fam("012")
def s2_power(r, L):
    v = pick(r, ["x", "y", "a"])
    c, e, p = r.randint(2, 4) * (pick(r, [1, -1]) if L else 1), r.randint(1, 5), r.randint(2, 4 if L < 2 else 3)
    if L == 2:
        expr = f"({mono(c, 'a', e)}b{sup(2)}){sup(p)}" if False else f"({N(c)}{pw('a', e)}b){sup(p)}"
        ans = f"{N(c ** p)}{pw('a', e * p)}{pw('b', p)}"
        wrong = [f"{N(c * p)}{pw('a', e * p)}{pw('b', p)}", f"{N(c ** p)}{pw('a', e + p)}{pw('b', p)}", f"{N(c)}{pw('a', e * p)}{pw('b', p)}"]
        vars_ = ["a", "b"]
    else:
        expr = f"({mono(c, v, e)}){sup(p)}"
        ans = mono(c ** p, v, e * p)
        wrong = [mono(c * p, v, e * p), mono(c ** p, v, e + p), mono(c, v, e * p)]
        vars_ = [v]
    return P(f"Simplify: {expr}", ans, ["Raise every factor inside the parentheses to the power; multiply exponents.", f"{expr} = {ans}."], wrong,
             {"kind": "equiv", "expr": expr, "vars": vars_, "strip": False}, tags=["misconception"])


@fam("01")
def s2_zero(r, L):
    k = r.randint(2, 15)
    v = pick(r, ["x", "y", "n"])
    forms = [(f"{k}{v}⁰", str(k), [f"{k}{v}", "0", "1"]), (f"({k}{v})⁰", "1", [str(k), "0", f"{k}{v}"]), (f"{k}⁰ + {v}⁰", "2", ["1", f"{k} + {v}", "0"]),
             (f"-{k}⁰", "-1", ["1", "0", f"-{k}"])]
    e_, ans, wr = pick(r, forms)
    return P(f"Simplify {e_}. Assume {v} ≠ 0.", ans, ["Any nonzero base raised to the 0 power equals 1.", "The exponent applies only to the base right next to it unless there are parentheses.", f"{e_} = {ans}."],
             wr, {"kind": "equiv", "expr": e_, "vars": [v], "strip": False}, tags=["misconception"])


@fam("012")
def s2_evaluate(r, L):
    x = nz(r, -4, 4)
    a, b = r.randint(1, 5), r.randint(1, 6)
    if L == 0:
        x = abs(x) + 1
        expr = f"{a}x{sup(2)} + {b}"
    elif L == 1:
        expr = f"{a}x{sup(3)} - x{sup(2)}"
    else:
        y = nz(r, -3, 3)
        expr = f"x{sup(2)}y - {a}xy{sup(2)}"
        v = F(x * x * y - a * x * y * y)
        return P(f"Evaluate {expr} when x = {x} and y = {y}.", N(v), [f"Substitute with parentheses: {paren(x)}²({paren(y)}) - {a}({paren(x)})({paren(y)})².", f"= {N(v)}."],
                 [N(F(-x * x * y - a * x * y * y)), N(F(x * x * y + a * x * y * y)), N(F(2 * x * y - a * x * 2 * y))], chk_val(f"({x})^2*({y}) - {a}*({x})*({y})^2"), tags=["misconception"])
    f = (lambda t: a * t ** 2 + b) if L == 0 else (lambda t: a * t ** 3 - t ** 2)
    g = (lambda t: a * t * 2 + b) if L == 0 else (lambda t: a * t * 3 - t * 2)
    v = F(f(x))
    wr = [F(f(-x)), F(g(x)), v + 1]
    return P(f"Evaluate {expr} when x = {x}.", N(v), [f"Substitute x = {paren(x)} and evaluate powers first.", f"= {N(v)}."],
             [N(w) for w in wr], chk_val(expr.replace("x", f"({x})")), tags=["misconception"] if x < 0 else [])


@fam("12")
def s2_numeric_rules(r, L):
    b = r.randint(2, 3)
    e1, e2, e3 = r.randint(2, 6), r.randint(2, 6), r.randint(1, 5)
    need(e1 + e2 - e3 >= 0 and e1 + e2 - e3 <= 9)
    expr = f"{b}{sup(e1)} · {b}{sup(e2)} ÷ {b}{sup(e3)}"
    res = e1 + e2 - e3
    return P(f"Write {expr} as a single power of {b}, then evaluate.", f"{b}{sup(res)} = {b ** res}",
             [f"Add, then subtract exponents: {e1} + {e2} - {e3} = {res}.", f"{b}{sup(res)} = {b ** res}."],
             [f"{b}{sup(e1 * e2 - e3)} = {b ** (e1 * e2 - e3)}" if e1 * e2 - e3 <= 12 else f"{b}{sup(res + 1)} = {b ** (res + 1)}", f"{b}{sup(e1 + e2 + e3)} = {b ** (e1 + e2 + e3)}", f"{b * b}{sup(res)} = {b ** (2 * res)}"],
             chk_py("power_and_value", expr=expr, base=str(b)), tags=["multiple-representations"])


@fam("2")
def s2_missing_exp(r, L):
    p, k = r.randint(2, 5), r.randint(2, 6)
    form = pick(r, ["pow", "prod", "quot"])
    if form == "pow":
        shown, tmpl, tgt = f"(xᵏ){sup(p)} = x{sup(p * k)}", f"(x^K)^{p}", f"x^{p * k}"
    elif form == "prod":
        a = r.randint(1, 7)
        shown, tmpl, tgt = f"x{sup(a)} · xᵏ · x{sup(p)} = x{sup(a + k + p)}", f"x^{a}*x^K*x^{p}", f"x^{a + k + p}"
    else:
        a = k + r.randint(1, 8)
        shown, tmpl, tgt = f"x{sup(a)} ÷ xᵏ = x{sup(a - k)}", f"x^{a}/x^K", f"x^{a - k}"
    return P(f"Find the whole number k that makes the equation true for x ≠ 0: {shown}", f"k = {k}",
             ["Use the exponent rules to write an equation for k.", f"k = {k}."], [f"k = {k * p if form == 'pow' else k + 1}", f"k = {k + p}", f"k = {abs(k - p) if k != p else k + 2}"],
             chk_py("missing_exp", template=tmpl, target=tgt), tags=["reasoning"])


@fam("012")
def s2_error(r, L):
    k = r.randint(2, 9)
    e = 2 if L < 2 else pick(r, [2, 4])
    return P(f"Sam says -{k}{sup(e)} = {k ** e} because \"a negative number to an even power is positive.\" What is the value of -{k}{sup(e)}?", str(-k ** e),
             [f"The exponent applies only to {k}, not to the negative sign: -{k}{sup(e)} = -({k}{sup(e)}).", f"= -{k ** e}. Sam's reasoning applies to (-{k}){sup(e)} = {k ** e}."],
             [str(k ** e), str(-k * e), str(k * e)], chk_val(f"-{k}^{e}"), tags=["error-analysis", "misconception"])


@fam("012")
def s2_select(r, L):
    e = pick(r, [8, 12, 10, 6])
    good = [f"x{sup(e // 2)} · x{sup(e // 2)}", f"(x{sup(e // 2)}){sup(2)}", f"x{sup(e + 3)} ÷ x{sup(3)}", f"(x{sup(2)}){sup(e // 2)}"]
    bad = [f"x{sup(e // 2)} + x{sup(e // 2)}", f"x{sup(e - 2)} · x{sup(1)}", f"(x{sup(e - 2)}){sup(2)}", f"x{sup(2 * e)} ÷ x{sup(2)}"]
    opts = [(g, True) for g in pick(r, good, 3)] + [(b, False) for b in pick(r, bad, 3)]
    return P(f"Select ALL expressions equivalent to x{sup(e)}.", None, ["Apply the product, quotient and power rules to each choice; x⁴ + x⁴ = 2x⁴, not x⁸."],
             options=opts, chk={"kind": "equiv", "expr": f"x^{e}", "vars": ["x"], "strip": False}, tags=["misconception"])


@fam("012")
def s2_open(r, L):
    a, b = r.randint(2, 5), r.randint(2, 5)
    e1, e2 = r.randint(2, 5), r.randint(1, 4)
    return P(f"Let P = {a}x{sup(e1)} and Q = {b}x{sup(e2)}.", None, ["Multiply coefficients, add exponents.", "Divide coefficients, subtract exponents.", "Square each factor.", "Substitute x = 1."],
             parts=[("Simplify P · Q.", mono(a * b, "x", e1 + e2), {"kind": "equiv", "expr": f"{a}x^{e1}*{b}x^{e2}", "vars": ["x"]}),
                    ("Simplify P ÷ Q.", f"{N(F(a, b))}x{sup(e1 - e2)}" if e1 != e2 and F(a, b).denominator == 1 else f"{a}{pw('x', e1 - e2) if e1 > e2 else ''}/{b}" if e1 >= e2 else f"{a}/({b}{pw('x', e2 - e1)})",
                     {"kind": "equiv", "expr": f"({a}x^{e1}) DIV ({b}x^{e2})".replace("DIV", "÷"), "vars": ["x"]}),
                    ("Simplify P².", mono(a * a, "x", 2 * e1), {"kind": "equiv", "expr": f"({a}x^{e1})^2", "vars": ["x"]}),
                    ("Evaluate P + Q when x = 1.", str(a + b), chk_val(f"{a} + {b}"))], tags=["multistep"])


# ======================================================================= S3 Creating linear equations
@fam("012")
def s3_number_sentence(r, L):
    a, b = r.randint(2, 9), r.randint(1, 20)
    x = r.randint(-6, 15) if L else r.randint(1, 12)
    forms = [(f"{b} more than {a} times a number n is {a * x + b}.", f"{a}n + {b} = {a * x + b}", [f"{a}(n + {b}) = {a * x + b}", f"{b}n + {a} = {a * x + b}", f"{a}n = {a * x + b} + {b}"]),
             (f"{b} less than {a} times a number n is {a * x - b}.", f"{a}n - {b} = {a * x - b}", [f"{b} - {a}n = {a * x - b}", f"{a}(n - {b}) = {a * x - b}", f"{a}n + {b} = {a * x - b}"])]
    if L >= 1:
        forms.append((f"{a} times the sum of a number n and {b} is {a * (x + b)}.", f"{a}(n + {b}) = {a * (x + b)}", [f"{a}n + {b} = {a * (x + b)}", f"n + {a * b} = {a * (x + b)}", f"{a} + n + {b} = {a * (x + b)}"]))
    if L == 2:
        c = r.randint(2, 5)
        need(a != c)
        forms.append((f"{a} times a number n, decreased by {b}, equals {c} times the number increased by {a * x - b - c * x}.", None, None))
    s, ans, wr = pick(r, forms)
    if ans is None:
        d = a * x - b - c * x
        need(d > 0)
        ans = f"{a}n - {b} = {c}n + {d}"
        wr = [f"{a}(n - {b}) = {c}(n + {d})", f"{a}n - {b} = {c}(n + {d})", f"{b} - {a}n = {c}n + {d}"]
    return P(f"Write an equation for the sentence: \"{s}\"", ans,
             ["Translate word by word: 'times' means multiply, 'more than' means add, 'less than' subtracts from the quantity that follows, and 'is' means =.", f"Equation: {ans}. (Its solution is n = {x}.)"],
             wr, chk_py("model_eq", var="n", expr=str(x)), tags=["modeling", "misconception"], mc_prompt=f"Which equation represents the sentence? \"{s}\"")


@fam("012")
def s3_cost(r, L):
    fee, rate = r.randint(10, 60), r.randint(3, 25)
    n = r.randint(2, 15)
    tot = fee + rate * n
    item = pick(r, [("a gym", "joining fee", "per class", "c", "classes"), ("a phone plan", "activation fee", "per month", "m", "months"), ("a bike rental", "base fee", "per hour", "h", "hours")])
    if L == 2:
        disc = r.randint(2, 9)
        tot = fee + (rate - disc) * n
        need(rate - disc > 0)
        txt = f"{item[0].capitalize()} charges a ${fee} {item[1]} and ${rate} {item[2]}, but members get ${disc} off each {item[2][4:]}. A member paid ${tot} in total. Write an equation to find the number of {item[4]}, {item[3]}."
        ans = f"{fee} + {rate - disc}{item[3]} = {tot}"
        wr = [f"{fee} + {rate}{item[3]} - {disc} = {tot}", f"{fee - disc} + {rate}{item[3]} = {tot}", f"({fee} + {rate}){item[3]} - {disc} = {tot}"]
    else:
        txt = f"{item[0].capitalize()} charges a ${fee} {item[1]} plus ${rate} {item[2]}. The total cost was ${tot}. Write an equation to find the number of {item[4]}, {item[3]}."
        ans = f"{fee} + {rate}{item[3]} = {tot}"
        wr = [f"{fee}{item[3]} + {rate} = {tot}", f"({fee} + {rate}){item[3]} = {tot}", f"{rate}{item[3]} = {tot} + {fee}"]
    return P(txt, ans, [f"Total = fee + rate × {item[4]}.", f"{ans}. Solving gives {item[3]} = {n}."], wr, chk_py("model_eq", var=item[3], expr=str(n)), tags=["modeling"])


@fam("12")
def s3_perimeter(r, L):
    w = r.randint(3, 20)
    d = r.randint(2, 12)
    shape = pick(r, ["rect", "tri"]) if L == 2 else "rect"
    if shape == "rect":
        P_ = 2 * w + 2 * (w + d)
        return P(f"A rectangle's length is {d} cm more than its width w. Its perimeter is {P_} cm. Write an equation that can be used to find w.", f"2w + 2(w + {d}) = {P_}",
                 [f"Perimeter = 2(width) + 2(length) = 2w + 2(w + {d}).", f"Set equal to {P_}: 2w + 2(w + {d}) = {P_}. (w = {w})"],
                 [f"w + (w + {d}) = {P_}", f"2w + {d} = {P_}", f"w(w + {d}) = {P_}"], chk_py("model_eq", var="w", expr=str(w)), tags=["modeling", "connections"])
    a = r.randint(2, 4)
    P_ = w + a * w + (w + d)
    return P(f"A triangle has sides w, {a}w, and w + {d} inches. Its perimeter is {P_} inches. Write an equation to find w.", f"w + {a}w + (w + {d}) = {P_}",
             [f"Add the three sides and set equal to the perimeter.", f"w + {a}w + w + {d} = {P_}. (w = {w})"],
             [f"w · {a}w · (w + {d}) = {P_}", f"w + {a}w = {P_} + {d}", f"{a}w + {d} = {P_}"], chk_py("model_eq", var="w", expr=str(w)), tags=["modeling"])


@fam("12")
def s3_two_plans(r, L):
    f1, r1 = r.randint(10, 60), r.randint(2, 9)
    r2 = r1 + r.randint(1, 6)
    m = r.randint(3, 30)
    f2 = f1 + r1 * m - r2 * m
    need(f2 >= 0)
    lab = pick(r, [("rides", "r"), ("visits", "v"), ("months", "m")])
    v = lab[1]
    a1, a2 = f"{f1} + {r1}{v}", (f"{f2} + {r2}{v}" if f2 else f"{r2}{v}")
    return P(f"Plan A costs ${f1} plus ${r1} per {lab[0][:-1]}. Plan B costs {'$' + str(f2) + ' plus ' if f2 else ''}${r2} per {lab[0][:-1]}. Write an equation to find the number of {lab[0]}, {v}, for which the plans cost the same.",
             f"{a1} = {a2}", [f"Plan A: {a1}. Plan B: {a2}.", f"Same cost: {a1} = {a2}. (This gives {v} = {m}.)"],
             [f"{f1}{v} + {r1} = {f2}{v} + {r2}" if f2 else f"{f1}{v} + {r1} = {r2}", f"{f1} + {r2}{v} = {a2.replace(str(r2), str(r1), 1) if f2 else str(r1) + v}", f"{f1} + {r1}{v} + {a2} = 0"],
             chk_py("model_eq", var=v, expr=str(m)), tags=["modeling"])


@fam("2")
def s3_angles(r, L):
    x = r.randint(10, 40)
    a, b = r.randint(1, 3), r.randint(2, 4)
    c = r.randint(-15, 25)
    kind = pick(r, ["supp", "comp", "tri"])
    total = {"supp": 180, "comp": 90, "tri": 180}[kind]
    if kind == "tri":
        d = total - (a * x + c) - b * x
        need(d > 10)
        txt = f"The angles of a triangle measure ({lin((a, 'x'), (c, ''))})°, ({b}x)°, and {d}°. Write an equation to find x."
        ans = f"{lin((a, 'x'), (c, ''))} + {b}x + {d} = 180"
    else:
        d = total - (a * x + c) - b * x
        need(a * x + c > 0 and b * x + d > 0)
        txt = f"Two angles are {'supplementary' if kind == 'supp' else 'complementary'}. They measure ({lin((a, 'x'), (c, ''))})° and ({lin((b, 'x'), (d, ''))})°. Write an equation to find x."
        ans = f"{lin((a, 'x'), (c, ''))} + {lin((b, 'x'), (d, ''))} = {total}"
    wr = [ans.replace(f"= {total}", f"= {270 - total if kind != 'tri' else 360}"), ans.split(" + ")[0] + f" = {lin((b, 'x'), (d if kind != 'tri' else 0, ''))}", ans.replace(f"= {total}", "= 0")]
    return P(txt, ans, [f"{'Supplementary angles sum to 180°.' if kind == 'supp' else 'Complementary angles sum to 90°.' if kind == 'comp' else 'Triangle angles sum to 180°.'}", f"{ans}. (x = {x})"],
             wr, chk_py("model_eq", var="x", expr=str(x)), tags=["modeling", "connections"])


@fam("012")
def s3_write_solve(r, L):
    nm = pick(r, NAMES)
    save0, per = r.randint(20, 150), r.randint(5, 30)
    goal = save0 + per * r.randint(3, 20)
    w = (goal - save0) // per
    return P(f"{nm} has ${save0} saved and saves ${per} each week. Write and solve an equation to find how many weeks w until {nm} has ${goal}.",
             f"w = {w}", [f"Equation: {save0} + {per}w = {goal}.", f"{per}w = {goal - save0}, so w = {w} weeks."],
             [f"w = {goal // per}", f"w = {(goal + save0) // per}", f"w = {w + 1}"], {"kind": "eq", "eq": f"{save0} + {per}w = {goal}", "var": "w"}, tags=["modeling"])


@fam("012")
def s3_select(r, L):
    n = r.randint(3, 12)
    c, k = r.randint(2, 8), r.randint(5, 30)
    tot = c * n + k
    good = [f"{c}n + {k} = {tot}", f"{k} + {c}n = {tot}", f"{c}n = {tot} - {k}"]
    bad = [f"{c}(n + {k}) = {tot}", f"{k}n + {c} = {tot}", f"{c}n - {k} = {tot}"]
    opts = [(g, True) for g in good] + [(b, False) for b in bad]
    return P(f"A taxi charges ${k} plus ${c} per mile. A ride cost ${tot}. Select ALL equations that could be used to find the number of miles n.", None,
             [f"Cost = {k} + {c}n, and the cost is {tot}.", "Equivalent rearrangements of the same equation also work."], options=opts,
             chk=chk_py("model_eq", var="n", expr=str(n)), tags=["modeling", "multiple-representations"])


@fam("012")
def s3_open(r, L):
    a, b = r.randint(5, 20), r.randint(2, 8)
    n = r.randint(3, 15)
    tot = a + b * n
    return P(f"A streaming service charges a one-time ${a} setup fee plus ${b} per month.", None,
             ["Cost = setup + monthly rate × months.", f"Substitute m = {n}.", f"Set {a} + {b}m = {tot}.", "Solve."],
             parts=[("Write an expression for the cost of m months.", f"{a} + {b}m", {"kind": "equiv", "expr": f"{a} + {b}m", "vars": ["m"]}),
                    (f"Find the cost of {n} months.", f"${tot}", chk_val(f"{a} + {b}*{n}")),
                    (f"Write an equation for a total cost of ${tot + b}.", f"{a} + {b}m = {tot + b}", chk_py("model_eq", var="m", expr=str(n + 1))),
                    ("Solve your equation.", f"m = {n + 1}", {"kind": "eq", "eq": f"{a} + {b}m = {tot + b}", "var": "m"})], tags=["modeling", "multistep"])


# ======================================================================= helpers: equations with errors
def error_chain(r, A, B, C, D_, var="x"):
    """Correct chain for Ax + B = Cx + D (A != C) and a version with one error. Returns (orig, steps, first_bad, correct_solution)."""
    k = r.randint(1, 3)
    s1 = (A - C, B, D_)
    steps_ok = [f"{lin((A - C, var), (B, ''))} = {N(D_)}", f"{coef_text(A - C, var)} = {N(D_ - B)}", f"{var} = {N(F(D_ - B, A - C))}"]
    if k == 1:
        bad1 = f"{lin((A + C, var), (B, ''))} = {N(D_)}"
        need(A + C != 0)
        steps = [bad1, f"{coef_text(A + C, var)} = {N(D_ - B)}", f"{var} = {N(F(D_ - B, A + C))}"]
    elif k == 2:
        steps = [steps_ok[0], f"{coef_text(A - C, var)} = {N(D_ + B)}", f"{var} = {N(F(D_ + B, A - C))}"]
        need(B != 0)
    else:
        steps = steps_ok[:2] + [f"{var} = {N(F(A - C, D_ - B)) if D_ != B else N(D_ - B - (A - C))}"]
        need(D_ != B and F(A - C, D_ - B) != F(D_ - B, A - C))
    return steps, k, F(D_ - B, A - C)


# ======================================================================= S4 Variables on both sides
def both_sides(r, L):
    for _ in range(100):
        x = F(r.randint(-12, 12)) if L < 2 else F(r.randint(-30, 30), pick(r, [1, 2, 3, 4]))
        A, C = nz(r, -9, 9), nz(r, -9, 9)
        if L == 0:
            A, C = r.randint(2, 9), r.randint(1, 8)
            x = F(r.randint(1, 12))
        if A == C:
            continue
        B = r.randint(-20, 20)
        D_ = (A - C) * x + B
        if D_.denominator == 1 and abs(D_) < 120:
            return A, B, C, int(D_), x
    raise Reject()


@fam("012")
def s4_solve(r, L):
    A, B, C, D_, x = both_sides(r, L)
    if L == 2 and r.random() < 0.5:
        A, C = F(A, 2), F(C, 2)
        D_ = F(D_, 2)
        B = F(B, 2)
        need(A != C)
    eq = eqtxt(A, B, C, D_)
    return P(f"Solve: {eq}", f"x = {N(x)}", [f"Move the x-terms to one side: {lin((A - C, 'x'), (B, ''))} = {N(D_)}.", f"Undo the constant: {coef_text(A - C, 'x')} = {N(D_ - B)}.",
                                             f"Divide: x = {N(x)}.", "Check by substituting into both sides."],
             [f"x = {N(F(D_ - B, A + C))}" if A + C else f"x = {N(-x)}", f"x = {N(F(D_ + B, A - C))}", f"x = {N(-x)}"], {"kind": "eq", "eq": eq}, tags=["multistep"])


@fam("012")
def s4_context(r, L):
    nm1, nm2 = pick(r, NAMES, 2)
    s1, s2 = r.randint(20, 200), r.randint(0, 100)
    r1, r2 = r.randint(2, 15), r.randint(2, 15)
    need(r1 != r2)
    w = r.randint(2, 20)
    s2 = s1 + (r1 - r2) * w
    need(s2 >= 0 and s2 != s1)
    eq = f"{s1} + {r1}w = {s2} + {r2}w"
    return P(f"{nm1} has ${s1} and saves ${r1} per week. {nm2} has ${s2} and saves ${r2} per week. After how many weeks w will they have the same amount?",
             f"{w} weeks", [f"{eq}.", f"{r1 - r2}w = {s2 - s1}.", f"w = {w}."], [f"{w + 1} weeks", f"{abs(s2 - s1) // (r1 + r2) if (r1 + r2) else 1} weeks", f"{(s1 + s2) // max(r1, r2)} weeks"],
             {"kind": "eq", "eq": eq, "var": "w"}, tags=["modeling"])


@fam("01", mode="mc")
def s4_which_solution(r, L):
    A, B, C, D_, x = both_sides(r, L)
    eq = eqtxt(A, B, C, D_)
    cands = [x, -x, x + 1, x - 2, F(D_ - B, A + C) if A + C else x + 3, x + 2]
    seen = []
    for c_ in cands:
        if c_ not in seen:
            seen.append(c_)
    need(len(seen) >= 4)
    opts = [(f"x = {N(c_)}", c_ == x) for c_ in seen[:4]]
    r.shuffle(opts)
    return P(f"Which value of x is the solution of {eq}?", f"x = {N(x)}", [f"Substitute x = {N(x)}: left side = {N(A * x + B)}, right side = {N(C * x + D_)}.", "Only the solution makes both sides equal."],
             options=opts, chk={"kind": "eq", "eq": eq}, tags=["reasoning"], mode="mc")


@fam("2")
def s4_reverse(r, L):
    x = nz(r, -8, 8)
    A, C, B = r.randint(2, 9), r.randint(1, 8), r.randint(-15, 15)
    need(A != C)
    D_ = (A - C) * x + B
    eq_k = f"{lin((A, 'x'), (B, ''))} = {coef_text(C, 'x')} + k"
    k = D_
    return P(f"For what value of k is x = {x} the solution of {eq_k}?", f"k = {k}",
             [f"Substitute x = {x}: {A}({x}) + {B} = {C}({x}) + k.", f"{A * x + B} = {C * x} + k, so k = {k}."],
             [f"k = {A * x + B}", f"k = {-k}", f"k = {k + C}"], chk_py("k_makes_solution", eq=eq_k, x=str(x)), tags=["reasoning", "challenge"])


@fam("012")
def s4_error(r, L):
    A, B, C, D_, x = both_sides(r, max(L, 1))
    need(A > C)
    steps, k, sol = error_chain(r, A, B, C, D_)
    orig = eqtxt(A, B, C, D_)
    shown = "; ".join(f"Step {i + 1}: {s}" for i, s in enumerate(steps))
    opts = [(f"Step {i}", i == k) for i in (1, 2, 3)] + [("There is no error", False)]
    return P(f"A student solved {orig} as follows. {shown}. In which step did the student make the first error?", f"Step {k}",
             [{1: "Step 1: subtracting the x-term from both sides should subtract its coefficient, not add it.", 2: "Step 2: the constant must be subtracted from both sides, not added.",
               3: "Step 3: divide the constant by the coefficient of x, not the other way around."}[k], f"Correct solution: x = {N(sol)}."],
             options=opts, chk=chk_py("err_steps", orig=orig, steps=steps), tags=["error-analysis"], mode="mc")


@fam("012")
def s4_select(r, L):
    A, B, C, D_, x = both_sides(r, 1)
    eq = eqtxt(A, B, C, D_)
    good = [eqtxt(A - C, B, 0, D_), eqtxt(A - C, 0, 0, D_ - B), f"x = {N(x)}", eqtxt(2 * A, 2 * B, 2 * C, 2 * D_)]
    bad = [eqtxt(A + C, B, 0, D_) if A + C else eqtxt(A - C, B, 0, D_ + 1), eqtxt(A - C, 0, 0, D_ + B) if B else eqtxt(A - C, 0, 0, D_ + 2), f"x = {N(-x) if x else 1}"]
    opts = [(g, True) for g in good[:3]] + [(b, False) for b in bad]
    need(len({o[0] for o in opts}) == 6)
    return P(f"Select ALL equations that are equivalent to {eq} (have the same solution).", None,
             [f"The solution of {eq} is x = {N(x)}.", "Equivalent equations come from doing the same operation to both sides."],
             options=opts, chk=chk_py("same_solution", eq=eq), tags=["reasoning"])


@fam("012")
def s4_open(r, L):
    A, B, C, D_, x = both_sides(r, 1)
    eq = eqtxt(A, B, C, D_)
    return P(f"Solve {eq} step by step.", None, ["Collect x-terms.", "Collect constants.", "Divide.", "Substitute to check."],
             parts=[(f"Subtract {coef_text(C, 'x')} from both sides. Write the new equation.", f"{lin((A - C, 'x'), (B, ''))} = {D_}", chk_py("same_solution", eq=eq)),
                    ("Undo the constant term. Write the new equation.", f"{coef_text(A - C, 'x')} = {D_ - B}", chk_py("same_solution", eq=eq)),
                    ("Solve for x.", f"x = {N(x)}", {"kind": "eq", "eq": eq}),
                    ("Find the value of each side when x has this value.", N(A * x + B), chk_val(f"{A}*({N(x)}) + {B}"))], tags=["multistep"])


# ======================================================================= S5 Distributive property
@fam("012")
def s5_solve(r, L):
    if L == 0:
        a, b, x = r.randint(2, 6), r.randint(1, 9), F(r.randint(0, 12))
        eq = f"{a}(x + {b}) = {N(a * (x + b))}"
        wrong = [f"x = {N(a * (x + b) - b)}", f"x = {N(x + 1)}", f"x = {N(F(a * (x + b) - b, a))}"]
    elif L == 1:
        a, b, c, x = nz(r, -7, 7), nz(r, -9, 9), nz(r, -9, 9), F(r.randint(-10, 12))
        need(a + c != 0)
        v = a * (x + b) + c * x
        eq = f"{a}({lin((1, 'x'), (b, ''))}) {'+' if c > 0 else '-'} {coef_text(abs(c), 'x')} = {N(v)}"
        wrong = [f"x = {N(F(v - b, a + c))}", f"x = {N(-x)}", f"x = {N(x + 1)}"]
    else:
        a, b, c, d = nz(r, -7, 7), nz(r, -9, 9), nz(r, -6, 6), nz(r, -9, 9)
        need(a != c)
        x = F(r.randint(-20, 20), pick(r, [1, 2, 3]))
        k = a * (x + b) - c * (x + d)
        eq = f"{a}({lin((1, 'x'), (b, ''))}) = {c}({lin((1, 'x'), (d, ''))}) {'+' if k >= 0 else '-'} {N(abs(k))}"
        wrong = [f"x = {N(-x)}", f"x = {N(x + 1)}", f"x = {N(F(c * d + k - b, a - c))}"]
    return P(f"Solve: {eq}", f"x = {N(x)}", ["Distribute to remove the parentheses (multiply every term inside).", "Combine like terms, then solve the resulting equation.", f"x = {N(x)}."],
             wrong, {"kind": "eq", "eq": eq}, tags=["misconception"])


@fam("012")
def s5_context(r, L):
    n = r.randint(2, 9)
    p, t = r.randint(3, 12), r.randint(1, 6)
    tot = n * (p + t)
    if L == 2:
        c = r.randint(5, 25)
        tot += c
        return P(f"{n} friends each buy a concert ticket and pay a ${t} service fee per ticket. They also share one ${c} parking fee. The total is ${tot}. Solve {n}(x + {t}) + {c} = {tot} to find the ticket price x in dollars.",
                 f"x = {p}", [f"{n}(x + {t}) = {tot - c}.", f"x + {t} = {N(F(tot - c, n))}.", f"x = {p}."], [f"x = {p + t}", f"x = {N(F(tot, n) - t)}", f"x = {N(F(tot - c, n))}"],
                 {"kind": "eq", "eq": f"{n}(x + {t}) + {c} = {tot}"}, tags=["modeling"])
    return P(f"{n} students each buy a club shirt and pay ${t} of shipping per shirt; together they pay ${tot}. Solve {n}(x + {t}) = {tot} to find the price x of one shirt in dollars.",
             f"x = {p}", [f"Divide both sides by {n}: x + {t} = {p + t}.", f"x = {p}."], [f"x = {p + t}", f"x = {tot - n * t * 0 - t}", f"x = {N(F(tot - t, n))}"],
             {"kind": "eq", "eq": f"{n}(x + {t}) = {tot}"}, tags=["modeling"])


@fam("01")
def s5_distribute(r, L):
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    if L == 0:
        a = abs(a)
    e = f"{a}(x {'+' if b > 0 else '-'} {abs(b)})" if a > 0 else f"-{abs(a)}(x {'+' if b > 0 else '-'} {abs(b)})"
    ans = lin((a, "x"), (a * b, ""))
    return P(f"Use the distributive property to rewrite {e}.", ans, [f"Multiply each term inside by {a}: {a} · x and {a} · {paren(b)}.", f"= {ans}."],
             [lin((a, "x"), (b, "")), lin((a, "x"), (-a * b, "")), lin((a, "x"), (a + b, ""))], {"kind": "equiv", "expr": e, "vars": ["x"], "strip": False}, tags=["misconception"])


@fam("2")
def s5_fraction_coef(r, L):
    d = pick(r, [2, 3, 4, 5])
    x = F(r.randint(-12, 12))
    b = nz(r, -8, 8)
    need((x + b) % d == 0 if False else True)
    rhs = F(1, d) * (x + b) * r.randint(1, 1)
    eq = f"(1/{d})(x {'+' if b > 0 else '-'} {abs(b)}) = {N(rhs)}"
    return P(f"Solve: {eq}", f"x = {N(x)}", [f"Multiply both sides by {d}: x {'+' if b > 0 else '-'} {abs(b)} = {N(rhs * d)}.", f"x = {N(x)}."],
             [f"x = {N(rhs - b)}", f"x = {N(rhs * d + b)}", f"x = {N(F(1, d) * x)}" if F(1, d) * x != x else f"x = {N(x + 1)}"], {"kind": "eq", "eq": eq}, tags=["multistep"])


@fam("012")
def s5_error(r, L):
    a, b = r.randint(2, 7), r.randint(2, 9)
    x = r.randint(-5, 10)
    c = a * (x + b)
    wrong_x = c - b
    need(F(c - b, a) != x)
    steps = [f"{a}x + {b} = {c}", f"{a}x = {c - b}", f"x = {N(F(c - b, a))}"]
    orig = f"{a}(x + {b}) = {c}"
    opts = [("Step 1", True), ("Step 2", False), ("Step 3", False), ("There is no error", False)]
    return P(f"Jo solved {orig}. Step 1: {steps[0]}. Step 2: {steps[1]}. Step 3: {steps[2]}. In which step did Jo make the first error?", "Step 1",
             [f"Step 1 should distribute {a} to both terms: {a}x + {a * b} = {c}.", f"Correct: {a}x = {c - a * b}, so x = {x}."],
             options=opts, chk=chk_py("err_steps", orig=orig, steps=steps), tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s5_select(r, L):
    a, b = r.randint(2, 6), nz(r, -6, 6)
    e = f"{a}(x {'+' if b > 0 else '-'} {abs(b)})"
    good = [lin((a, "x"), (a * b, "")), f"{a}x {'+' if b > 0 else '-'} {abs(a * b)}", lin((a * b, ""), (a, "x")) if a * b > 0 else f"-{abs(a * b)} + {a}x", f"{a - 1}x + x {'+' if a * b > 0 else '-'} {abs(a * b)}"]
    bad = [lin((a, "x"), (b, "")), lin((a, "x"), (-a * b, "")), lin((a + b, "x"), (0, ""))]
    seen = []
    for g in good:
        if g not in seen:
            seen.append(g)
    opts = [(g, True) for g in seen[:3]] + [(x, False) for x in bad]
    need(len({o[0] for o in opts}) == len(opts))
    return P(f"Select ALL expressions equivalent to {e}.", None, [f"{e} = {lin((a, 'x'), (a * b, ''))}."], options=opts,
             chk={"kind": "equiv", "expr": e, "vars": ["x"], "strip": False}, tags=["multiple-representations"])


@fam("012")
def s5_open(r, L):
    a, b, c = r.randint(2, 5), r.randint(1, 6), r.randint(2, 5)
    x = r.randint(1, 9)
    tot = a * (x + b) + c * x
    eq = f"{a}(x + {b}) + {c}x = {tot}"
    return P(f"Solve {eq}.", None, ["Distribute.", "Combine like terms.", "Isolate x.", "Check."],
             parts=[("Distribute and write the new equation.", f"{a}x + {a * b} + {c}x = {tot}", chk_py("same_solution", eq=eq)),
                    ("Combine like terms.", f"{a + c}x + {a * b} = {tot}", chk_py("same_solution", eq=eq)),
                    ("Solve for x.", f"x = {x}", {"kind": "eq", "eq": eq}),
                    ("What is the value of the left side for this x?", str(tot), chk_val(f"{a}*({x} + {b}) + {c}*{x}"))], tags=["multistep"])


# ======================================================================= S6 Combining like terms
@fam("012")
def s6_solve(r, L):
    x = F(r.randint(-10, 12)) if L else F(r.randint(1, 12))
    a, b, c = r.randint(1, 8), r.randint(1, 6), r.randint(-9, 9)
    d = r.randint(-9, 9)
    if L == 0:
        terms = [(a, "x"), (c, ""), (b, "x")]
        rhs = (a + b) * x + c
        eq = f"{lin(terms[0])} {'+' if c >= 0 else '-'} {abs(c)} + {coef_text(b, 'x')} = {N(rhs)}" if False else f"{a}x + {abs(c)} + {b}x = {N((a + b) * x + abs(c))}"
        steps = [f"Combine like terms: {a + b}x + {abs(c)} = {N((a + b) * x + abs(c))}.", f"{a + b}x = {N((a + b) * x)}.", f"x = {N(x)}."]
    elif L == 1:
        b = -b
        need(a + b != 0)
        rhs = (a + b) * x + c + d
        eq = f"{a}x {'+' if c >= 0 else '-'} {abs(c)} - {abs(b)}x {'+' if d >= 0 else '-'} {abs(d)} = {N(rhs)}"
        steps = [f"Combine: {lin((a + b, 'x'), (c + d, ''))} = {N(rhs)}.", f"{coef_text(a + b, 'x')} = {N(rhs - c - d)}.", f"x = {N(x)}."]
    else:
        e = r.randint(1, 5)
        need(a + b != e)
        rhs_c = (a + b - e) * x + c - d
        eq = f"{a}x + {c} + {b}x = {e}x + {d} + {N(rhs_c)}".replace("+ -", "- ")
        steps = [f"Combine each side: {lin((a + b, 'x'), (c, ''))} = {lin((e, 'x'), (d + rhs_c, ''))}.", "Move x-terms to one side and constants to the other.", f"x = {N(x)}."]
    return P(f"Solve: {eq}", f"x = {N(x)}", steps, [f"x = {N(-x)}", f"x = {N(x + 1)}", f"x = {N(x * 2)}" if x else "x = 1"], {"kind": "eq", "eq": eq}, tags=["multistep"])


@fam("01")
def s6_simplify(r, L):
    a, b, c, d = nz(r, -9, 9), nz(r, -9, 9), r.randint(-12, 12), r.randint(-12, 12)
    if L == 0:
        a, b = abs(a), abs(b)
    e = f"{lin((a, 'x'), (c, ''))} + {lin((b, 'x'), (d, ''))}".replace("+ -", "- ")
    ans = lin((a + b, "x"), (c + d, ""))
    return P(f"Simplify by combining like terms: {e}", ans, [f"x-terms: {a} + ({b}) = {a + b}. Constants: {c} + ({d}) = {c + d}.", f"= {ans}."],
             [lin((a + b + c + d, "x")), lin((a - b, "x"), (c + d, "")), lin((a + b, "x"), (c - d, ""))], {"kind": "equiv", "expr": e, "vars": ["x"], "strip": False},
             tags=["misconception"])


@fam("012")
def s6_perimeter(r, L):
    x = r.randint(2, 12)
    a, b, c = r.randint(1, 4), r.randint(1, 9), r.randint(1, 3)
    if L == 0:
        P_ = 2 * (a * x + b) + 2 * x
        return P(f"A rectangle has length {lin((a, 'x'), (b, ''))} and width x (in feet). Its perimeter is {P_} feet. Find x.", f"x = {x}",
                 [f"Perimeter: 2({lin((a, 'x'), (b, ''))}) + 2x = {2 * a + 2}x + {2 * b}.", f"{2 * a + 2}x + {2 * b} = {P_}, so x = {x}."],
                 [f"x = {x + 1}", f"x = {N(F(P_ - b, a + 1))}", f"x = {N(F(P_, 2 * a + 2))}"], {"kind": "eq", "eq": f"2({lin((a, 'x'), (b, ''))}) + 2x = {P_}"}, tags=["modeling", "connections"])
    P_ = (a * x + b) + (c * x) + (x + 2 * b)
    sides = f"{lin((a, 'x'), (b, ''))}, {coef_text(c, 'x')}, and {lin((1, 'x'), (2 * b, ''))}"
    return P(f"A triangle has sides {sides} centimeters. The perimeter is {P_} cm. Find x and the length of the longest side.",
             f"x = {x}; longest side {max(a * x + b, c * x, x + 2 * b)} cm",
             [f"Add sides: {a + c + 1}x + {3 * b} = {P_}.", f"x = {x}.", f"Side lengths: {a * x + b}, {c * x}, {x + 2 * b} cm."],
             [f"x = {x + 1}; longest side {max(a * (x + 1) + b, c * (x + 1), x + 1 + 2 * b)} cm", f"x = {x}; longest side {min(a * x + b, c * x, x + 2 * b)} cm", f"x = {x - 1}; longest side {max(a * (x - 1) + b, c * (x - 1), x - 1 + 2 * b)} cm"],
             chk_py("x_and_longest", eq=f"{lin((a, 'x'), (b, ''))} + {c}x + {lin((1, 'x'), (2 * b, ''))} = {P_}", sides=[lin((a, 'x'), (b, '')), coef_text(c, 'x'), lin((1, 'x'), (2 * b, ''))]),
             tags=["modeling", "multistep"])


@fam("12")
def s6_consecutive(r, L):
    n = r.randint(-10, 40)
    k = pick(r, [3, 4]) if L == 2 else 3
    kind = pick(r, ["int", "even", "odd"]) if L == 2 else "int"
    if kind == "int":
        terms = [n + i for i in range(k)]
        expr = " + ".join(["n"] + [f"(n + {i})" for i in range(1, k)])
    else:
        n = 2 * (n // 2) + (1 if kind == "odd" else 0)
        terms = [n + 2 * i for i in range(k)]
        expr = " + ".join(["n"] + [f"(n + {2 * i})" for i in range(1, k)])
    s = sum(terms)
    word = {"int": "consecutive integers", "even": "consecutive even integers", "odd": "consecutive odd integers"}[kind]
    return P(f"The sum of {k} {word} is {s}. What is the least of these integers?", str(terms[0]),
             [f"Let n be the least: {expr} = {s}.", f"{k}n + {sum(t - n for t in terms)} = {s}, so n = {terms[0]}."],
             [str(terms[-1]), str(terms[1]), str(s // k)], {"kind": "eq", "eq": f"{expr} = {s}", "var": "n"}, tags=["modeling", "reasoning"])


@fam("012")
def s6_error(r, L):
    a, b, c = r.randint(2, 7), r.randint(2, 9), r.randint(2, 6)
    x = r.randint(1, 9)
    tot = a * x + b - c * x
    need(a != c and a - c != 0)
    orig = f"{a}x + {b} - {c}x = {tot}"
    steps = [f"{a + c}x + {b} = {tot}", f"{a + c}x = {tot - b}", f"x = {N(F(tot - b, a + c))}"]
    opts = [("Step 1", True), ("Step 2", False), ("Step 3", False), ("There is no error", False)]
    return P(f"Lin solved {orig}. Step 1: {steps[0]}. Step 2: {steps[1]}. Step 3: {steps[2]}. In which step did Lin make the first error?", "Step 1",
             [f"Step 1: {a}x - {c}x = {a - c}x, not {a + c}x (the subtraction belongs to {c}x).", f"Correct: {a - c}x + {b} = {tot}, so x = {x}."],
             options=opts, chk=chk_py("err_steps", orig=orig, steps=steps), tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s6_select(r, L):
    a, b, c = r.randint(2, 6), r.randint(1, 9), r.randint(1, 5)
    e = f"{a}x + {b} - {c}x + {2 * b}"
    tgt = lin((a - c, "x"), (3 * b, ""))
    good = [tgt, f"{3 * b} + {coef_text(a - c, 'x')}" if a - c > 0 else f"{3 * b} - {coef_text(c - a, 'x')}", f"{a}x - {c}x + {3 * b}"]
    bad = [lin((a + c, "x"), (3 * b, "")), lin((a - c + 3 * b, "x")), lin((a - c, "x"), (b, ""))]
    opts = [(g, True) for g in good] + [(x, False) for x in bad]
    need(len({o[0] for o in opts}) == 6)
    return P(f"Select ALL expressions equivalent to {e}.", None, [f"Combine x-terms: {a}x - {c}x = {coef_text(a - c, 'x')}. Constants: {b} + {2 * b} = {3 * b}."],
             options=opts, chk={"kind": "equiv", "expr": e, "vars": ["x"], "strip": False}, tags=["misconception"])


@fam("012")
def s6_open(r, L):
    x = r.randint(2, 10)
    a, b = r.randint(2, 5), r.randint(1, 8)
    pts = [a * x, x + b, 2 * x]
    tot = sum(pts)
    return P(f"In a game, Ana scored {a}x points, Ben scored x + {b} points, and Cy scored 2x points. Together they scored {tot} points.", None,
             ["Add the expressions.", "Combine like terms.", "Solve.", "Substitute."],
             parts=[("Write an equation for the total.", f"{a}x + x + {b} + 2x = {tot}", chk_py("model_eq", var="x", expr=str(x))),
                    ("Combine like terms.", f"{a + 3}x + {b} = {tot}", chk_py("model_eq", var="x", expr=str(x))),
                    ("Solve for x.", f"x = {x}", {"kind": "eq", "eq": f"{a + 3}x + {b} = {tot}"}),
                    ("How many points did Ana score?", str(a * x), chk_val(f"{a}*{x}"))], tags=["modeling", "multistep"])


# ======================================================================= S7 One, infinitely many, or no solutions
TYPES = ["one solution", "no solution", "infinitely many solutions"]


def make_typed(r, L, kind):
    a, b, c = nz(r, -6, 6), r.randint(-9, 9), nz(r, -5, 5)
    if L == 0:
        if kind == "one":
            c2 = a + pick(r, [1, 2, -1])
            return f"{lin((a, 'x'), (b, ''))} = {lin((c2, 'x'), (r.randint(-9, 9), ''))}"
        if kind == "none":
            return f"{lin((a, 'x'), (b, ''))} = {lin((a, 'x'), (b + nz(r, -5, 5), ''))}"
        return f"{lin((a, 'x'), (b, ''))} = {lin((b, ''), (a, 'x'))}"
    k = nz(r, -4, 4)
    inner = lin((1, "x"), (c, ""))
    left = f"{k}({inner}) {'+' if b >= 0 else '-'} {abs(b)}"
    lk, lc = k, k * c + b
    if kind == "one":
        m = lk + pick(r, [1, 2, 3, -1, -2])
        right = lin((m, "x"), (r.randint(-9, 9), ""))
    elif kind == "none":
        d = nz(r, -6, 6)
        right = lin((lk - 1, "x"), (lc + d, "")) + " + x" if L == 2 and lk != 1 else lin((lk, "x"), (lc + d, ""))
    else:
        right = lin((lk - 1, "x"), (lc, "")) + " + x" if L == 2 and lk != 1 else lin((lk, "x"), (lc, ""))
    return f"{left} = {right}"


@fam("012", mode="mc")
def s7_classify(r, L):
    kind = pick(r, ["one", "none", "all", "none", "all"])
    eq = make_typed(r, L, kind)
    want = {"one": TYPES[0], "none": TYPES[1], "all": TYPES[2]}[kind]
    return P(f"How many solutions does {eq} have?", want,
             ["Simplify both sides and compare.", {"one": "The x-coefficients differ, so there is exactly one solution.", "none": "Same x-coefficients, different constants: the equation is never true, so no solution.",
                                                    "all": "Both sides are identical, so every value of x works: infinitely many solutions."}[kind]],
             options=[(t, t == want) for t in TYPES] + [("exactly two solutions", False)], chk=chk_py("num_solutions", eq=eq), tags=["reasoning"], mode="mc")


@fam("012", mode="sa")
def s7_classify_sa(r, L):
    kind = pick(r, ["one", "none", "all"])
    eq = make_typed(r, L, kind)
    want = {"one": TYPES[0], "none": TYPES[1], "all": TYPES[2]}[kind]
    return P(f"Does the equation {eq} have one solution, no solution, or infinitely many solutions?", want,
             ["Simplify each side to the form ax + b.", f"Compare coefficients and constants: {want}."], [t for t in TYPES if t != want],
             chk_py("num_solutions", eq=eq), tags=["reasoning"], mode="sa")


@fam("12")
def s7_param(r, L):
    a, b = nz(r, -7, 7), r.randint(-9, 9)
    want = pick(r, ["none", "all"])
    if want == "none":
        d = b + nz(r, -6, 6)
        eq = f"{lin((a, 'x'), (b, ''))} = Kx {'+' if d >= 0 else '-'} {abs(d)}"
        return P(f"For what value of k does {eq.replace('K', 'k')} have no solution?", f"k = {a}",
                 [f"No solution happens when the x-coefficients match but the constants differ.", f"k = {a} (constants {b} and {d} differ)."],
                 [f"k = {-a}", f"k = {d}", f"k = {a + 1}"], chk_py("param_value", eq=eq, want="none"), tags=["reasoning"])
    eq = f"{lin((a, 'x'), (b, ''))} = {coef_text(a, 'x')} + K"
    return P(f"For what value of k does {eq.replace('K', 'k')} have infinitely many solutions?", f"k = {b}",
             ["Infinitely many solutions require identical sides.", f"The x-terms already match, so k = {b}."],
             [f"k = {-b}", f"k = {a}", f"k = {b + a}"], chk_py("param_value", eq=eq, want="all"), tags=["reasoning"])


@fam("2", mode="mc")
def s7_complete(r, L):
    a, b = r.randint(2, 6), r.randint(1, 9)
    want = pick(r, ["none", "all", "one"])
    base = f"{a}(x + {b}) = "
    opts_all = {"all": f"{a}x + {a * b}", "none": f"{a}x + {a * b + pick(r, [1, 2, 3])}", "one": f"{a + 1}x + {a * b}"}
    extra = f"{a}x - {a * b}" if want != "none" else f"{a + 2}x + {a * b + 1}"
    opts = [(opts_all[k], k == want) for k in ("all", "none", "one")]
    opts.append((extra, False))
    r.shuffle(opts)
    word = {"all": "infinitely many solutions", "none": "no solution", "one": "exactly one solution"}[want]
    goods = [t for t, c in opts if c]
    need(len(goods) == 1)
    return P(f"Which expression completes {base}___ so that the equation has {word}?", goods[0],
             [f"{base}{a}x + {a * b} after distributing.", {"all": "Identical sides → infinitely many.", "none": "Same x-coefficient, different constant → none.", "one": "Different x-coefficient → one solution."}[want]],
             options=opts, chk=chk_py("completes_type", left=f"{a}(x + {b})", want=want), tags=["reasoning", "challenge"], mode="mc")


@fam("2")
def s7_context(r, L):
    f1, rate = r.randint(10, 40), r.randint(3, 9)
    f2 = f1 + r.randint(5, 15)
    return P(f"Gym A charges ${f1} to join plus ${rate} per visit. Gym B charges ${f2} to join plus ${rate} per visit. For how many visits do the gyms cost the same?",
             "no solution", [f"{f1} + {rate}v = {f2} + {rate}v.", f"Subtract {rate}v: {f1} = {f2}, which is false. The costs are never equal."],
             ["one solution", "infinitely many solutions", f"{f2 - f1} visits"], chk_py("num_solutions", eq=f"{f1} + {rate}v = {f2} + {rate}v", var="v"), tags=["modeling", "reasoning"], mode="sa")


@fam("012")
def s7_error(r, L):
    a, b = r.randint(2, 6), r.randint(1, 9)
    eq = f"{a}(x + {b}) = {a}x + {a * b}"
    opts = [("No. The equation is true for every x, so it has infinitely many solutions.", True), ("Yes. 0 = 0 means x = 0 is the only solution.", False),
            ("Yes. Getting 0 = 0 means there is no solution.", False), ("No. The solution is x = 1.", False)]
    r.shuffle(opts)
    return P(f"Ty simplified {eq} to 0 = 0 and said \"the solution is x = 0.\" Is Ty correct?", "No. The equation is true for every x, so it has infinitely many solutions.",
             ["0 = 0 is a true statement that does not depend on x.", "Every value of x makes the original equation true: infinitely many solutions."],
             options=opts, chk={"kind": "text", "accept": ["No. The equation is true for every x, so it has infinitely many solutions."]}, tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s7_select(r, L):
    eqs = [(make_typed(r, max(L, 1), "none"), True), (make_typed(r, max(L, 1), "none"), True), (make_typed(r, 1, "one"), False),
           (make_typed(r, 1, "all"), False), (make_typed(r, 0, "none"), True), (make_typed(r, 0, "one"), False)]
    need(len({e for e, _ in eqs}) == 6)
    return P("Select ALL equations that have NO solution.", None, ["Simplify each side; no solution occurs when the x-coefficients match and the constants differ."],
             options=eqs, chk=chk_py("is_type", want="none"), tags=["reasoning"])


@fam("012")
def s7_open(r, L):
    a, b = r.randint(2, 6), r.randint(1, 9)
    return P(f"Complete the equation {a}x + {b} = ___ in different ways.", None,
             ["Different x-coefficient → one solution.", "Same coefficient, different constant → none.", "Identical → infinitely many.", "Solve."],
             parts=[(f"Classify {a}x + {b} = {a}x + {b + 3}.", "no solution", chk_py("num_solutions", eq=f"{a}x + {b} = {a}x + {b + 3}")),
                    (f"Classify {a}x + {b} = {b} + {a}x.", "infinitely many solutions", chk_py("num_solutions", eq=f"{a}x + {b} = {b} + {a}x")),
                    (f"Classify {a}x + {b} = {a + 1}x + {b}.", "one solution", chk_py("num_solutions", eq=f"{a}x + {b} = {a + 1}x + {b}")),
                    (f"Solve {a}x + {b} = {a + 1}x + {b}.", "x = 0", {"kind": "eq", "eq": f"{a}x + {b} = {a + 1}x + {b}"})], tags=["reasoning"])


# ======================================================================= S8 Solving exponent equations
@fam("012")
def s8_two_step(r, L):
    k = r.randint(2, 12)
    if L == 0:
        b = r.randint(1, 30)
        eq = f"x² + {b} = {k * k + b}"
        return P(f"Solve: {eq}", f"x = {k} or x = -{k}", [f"Subtract {b}: x² = {k * k}.", f"x = ±{k}."], [f"x = {k}", f"x = {k * k} or x = -{k * k}", f"x = {N(F(k * k + b, 2))}"],
                 chk_py("roots_match", eq=eq), tags=["misconception"])
    if L == 1:
        a = r.randint(2, 5)
        if r.random() < 0.5:
            eq = f"{a}x² = {a * k * k}"
            return P(f"Solve: {eq}", f"x = {k} or x = -{k}", [f"Divide by {a}: x² = {k * k}.", f"x = ±{k}."], [f"x = {k}", f"x = {N(F(a * k * k, 2))} or x = -{N(F(a * k * k, 2))}", f"x = {a * k} or x = -{a * k}"],
                     chk_py("roots_match", eq=eq))
        k = r.randint(2, 6)
        c = r.randint(1, 20)
        eq = f"x³ - {c} = {k ** 3 - c}" if k ** 3 - c >= 0 else f"x³ + {abs(k ** 3 - c) if False else c} = {k ** 3 + c}"
        return P(f"Solve: {eq}", f"x = {k}", [f"Isolate x³: x³ = {k ** 3}.", f"x = ∛{k ** 3} = {k}."], [f"x = {k} or x = -{k}", f"x = {k ** 3}", f"x = {N(F(k ** 3, 3))}"],
                 chk_py("roots_match", eq=eq), tags=["misconception"])
    a = r.randint(2, 4)
    m = pick(r, [2, 3, 5, 6, 7, 10])
    eq = f"{a}x² - {r.randint(1, 9)} = 0"
    c = int(eq.split(" - ")[1].split(" ")[0])
    eq = f"{a}x² - {a * m} = 0"
    return P(f"Solve: {eq}. Give exact answers.", f"x = √{m} or x = -√{m}", [f"{a}x² = {a * m}, so x² = {m}.", f"x = ±√{m} (irrational)."],
             [f"x = √{m}", f"x = {N(F(a * m, 2))} or x = -{N(F(a * m, 2))}", f"x = {m} or x = -{m}"], chk_py("roots_match", eq=eq), tags=["challenge"])


@fam("12")
def s8_no_real(r, L):
    a, b = r.randint(1, 5), r.randint(1, 30)
    eq = f"x² + {b} = {b - a * a if r.random() < 0.5 else b - a}" if L == 2 else f"x² = -{a * a}"
    return P(f"How many real solutions does {eq} have?", "0", ["A square of a real number is never negative.", "x² would have to be negative, so there is no real solution."],
             ["1", "2", "infinitely many"], chk_py("count_real_roots", eq=eq), tags=["reasoning"])


@fam("012")
def s8_context(r, L):
    kind = pick(r, ["square", "cube", "circle"] if L == 2 else ["square", "cube"])
    if kind == "square":
        s = r.randint(3, 20)
        extra = r.randint(5, 40)
        return P(f"A square mural has area A = s² square feet. If the mural plus a {extra} square-foot border panel covers {s * s + extra} square feet, solve s² + {extra} = {s * s + extra} for the side length s.",
                 f"s = {s}", [f"s² = {s * s}.", f"s = {s} (a length cannot be negative, so reject -{s})."], [f"s = {s * s}", f"s = {s} or s = -{s}", f"s = {N(F(s * s + extra, 2))}"],
                 chk_py("roots_match", eq=f"s² + {extra} = {s * s + extra}", var="s", lo=0.0), tags=["modeling"])
    if kind == "cube":
        s = r.randint(2, 10)
        n = r.randint(2, 6)
        return P(f"{n} identical cube-shaped boxes have a total volume of {n * s ** 3} cubic inches. Solve {n}e³ = {n * s ** 3} for the edge length e.",
                 f"e = {s}", [f"e³ = {s ** 3}.", f"e = {s}."], [f"e = {N(F(n * s ** 3, 3))}", f"e = {s ** 3}", f"e = {s * n}"],
                 chk_py("roots_match", eq=f"{n}e³ = {n * s ** 3}", var="e"), tags=["modeling"])
    k = r.randint(2, 9)
    return P(f"A circle's area is {k * k}π square cm. Solve πr² = {k * k}π for the radius r.", f"r = {k}",
             [f"Divide by π: r² = {k * k}.", f"r = {k} (radius is positive)."], [f"r = {k * k}", f"r = {N(F(k * k, 2))}", f"r = {2 * k}"],
             chk_py("roots_match", eq=f"πr² = {k * k}π", var="r", lo=0.0), tags=["modeling", "connections"])


@fam("12")
def s8_exponent_unknown(r, L):
    b = pick(r, [2, 3, 5, 10])
    n = r.randint(2, 6) if L == 1 else r.randint(-3, 6)
    need(abs(b ** abs(n)) <= 10000)
    if L == 1:
        eq = f"{b}ˣ = {b ** n}"
        return P(f"Solve: {eq}", f"x = {n}", [f"Write {b ** n} as a power of {b}: {b ** n} = {b}{sup(n)}.", f"Same base, so the exponents are equal: x = {n}."],
                 [f"x = {N(F(b ** n, b))}", f"x = {n + 1}", f"x = {b ** n - b}"], chk_py("exp_eq", base=str(b), shift=0, target=N(F(b) ** n)), tags=["challenge"])
    s = r.randint(1, 3)
    t = F(b) ** n
    return P(f"Solve: {b}ˣ⁺{sup(s)} = {N(t)}", f"x = {n - s}",
             [f"{N(t)} = {b}{sup(n)}.", f"So x + {s} = {n}, and x = {n - s}."], [f"x = {n + s}", f"x = {n}", f"x = {-n - s}"],
             chk_py("exp_eq", base=str(b), shift=s, target=N(t)), tags=["challenge"])


@fam("2")
def s8_shifted_square(r, L):
    k = r.randint(2, 9)
    h = nz(r, -6, 6)
    eq = f"(x {'+' if h > 0 else '-'} {abs(h)})² = {k * k}"
    s1, s2 = k - h, -k - h
    return P(f"Solve: {eq}", f"x = {s1} or x = {s2}", [f"Take square roots: x {'+' if h > 0 else '-'} {abs(h)} = {k} or x {'+' if h > 0 else '-'} {abs(h)} = -{k}.", f"x = {s1} or x = {s2}."],
             [f"x = {s1}", f"x = {k + h} or x = {-k + h}", f"x = {k * k - h}"], chk_py("roots_match", eq=eq), tags=["challenge"])


@fam("012")
def s8_error(r, L):
    k = r.randint(3, 12)
    b = r.randint(2, 20)
    eq = f"x² + {b} = {k * k + b}"
    opts = [(f"x = {k} or x = -{k}", True), (f"x = {k}", False), (f"x = {N(F(k * k, 2))}", False), (f"x = {k * k}", False)]
    r.shuffle(opts)
    return P(f"Ella solved {eq} and wrote only x = {k}. What is the complete solution?", f"x = {k} or x = -{k}",
             [f"x² = {k * k}.", f"Both {k}² and (-{k})² equal {k * k}, so x = {k} or x = -{k}."], options=opts, chk=chk_py("roots_match", eq=eq),
             tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s8_select(r, L):
    k = r.randint(2, 7)
    good = [f"x² = {k * k}", f"x² + 1 = {k * k + 1}", f"2x² = {2 * k * k}", f"x² - {k * k} = 0"]
    bad = [f"x³ = {k ** 3}", f"x² = -{k * k}", f"2x = {2 * k}", f"x² = {2 * k}"]
    opts = [(g, True) for g in pick(r, good, 3)] + [(b, False) for b in pick(r, bad, 3)]
    need(len({o[0] for o in opts}) == 6)
    return P(f"Select ALL equations whose solutions are exactly x = {k} and x = -{k}.", None, ["Isolate x² and take square roots; x³ has only one real root, and x² cannot be negative."],
             options=opts, chk=chk_py("has_roots", roots=[str(k), str(-k)]), tags=["reasoning"])


@fam("012")
def s8_open(r, L):
    k = r.randint(2, 8)
    c = r.randint(2, 5)
    m = pick(r, [2, 3, 5, 7])
    return P("Solve each equation. List all real solutions.", None, ["Square roots give ±.", "Cube roots give one real solution.", "Divide first.", "Leave irrational answers in radical form."],
             parts=[(f"x² = {k * k}", f"x = {k} or x = -{k}", chk_py("roots_match", eq=f"x² = {k * k}")),
                    (f"x³ = -{c ** 3}", f"x = -{c}", chk_py("roots_match", eq=f"x³ = -{c ** 3}")),
                    (f"{c}x² = {c * k * k}", f"x = {k} or x = -{k}", chk_py("roots_match", eq=f"{c}x² = {c * k * k}")),
                    (f"x² = {m}", f"x = √{m} or x = -√{m}", chk_py("roots_match", eq=f"x² = {m}"))], tags=["multistep"])


SKILLS = {
    1: dict(name="Expressions with radical exponents", std=["8.EE.A.2", "8.EE.A.1"], fams=[s1_numeric, s1_substitute, s1_simplify_var, s1_inverse, s1_area_volume, s1_abs_root],
            extra=[s1_error, s1_select, s1_open]),
    2: dict(name="Expressions with integer exponents", std=["8.EE.A.1"], fams=[s2_product, s2_quotient, s2_power, s2_zero, s2_evaluate, s2_numeric_rules, s2_missing_exp],
            extra=[s2_error, s2_select, s2_open]),
    3: dict(name="Creating linear equations", std=["8.EE.C.7", "A-CED.A.1"], fams=[s3_number_sentence, s3_cost, s3_perimeter, s3_two_plans, s3_angles, s3_write_solve],
            extra=[s3_select, s3_open]),
    4: dict(name="Solving equations with variables on both sides", std=["8.EE.C.7b"], fams=[s4_solve, s4_context, s4_which_solution, s4_reverse],
            extra=[s4_error, s4_select, s4_open]),
    5: dict(name="Solving equations using the distributive property", std=["8.EE.C.7b"], fams=[s5_solve, s5_context, s5_distribute, s5_fraction_coef],
            extra=[s5_error, s5_select, s5_open]),
    6: dict(name="Solving equations by combining like terms", std=["8.EE.C.7b"], fams=[s6_solve, s6_simplify, s6_perimeter, s6_consecutive],
            extra=[s6_error, s6_select, s6_open]),
    7: dict(name="One, infinitely many, or no solutions", std=["8.EE.C.7a"], fams=[s7_classify, s7_classify_sa, s7_param, s7_complete, s7_context],
            extra=[s7_error, s7_select, s7_open]),
    8: dict(name="Solving exponent equations", std=["8.EE.A.2"], fams=[s8_two_step, s8_no_real, s8_context, s8_exponent_unknown, s8_shifted_square],
            extra=[s8_error, s8_select, s8_open]),
}
