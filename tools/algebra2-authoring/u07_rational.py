from lib import Bank, graph
from mathlite import *
from collections import Counter
import math, random, itertools

STD = {1: ["A-APR.D.6"], 2: ["A-APR.D.7"], 3: ["A-APR.D.7"], 4: ["A-REI.A.2"], 5: ["A-REI.A.2"], 6: ["F-IF.C.7d"], 7: ["F-IF.C.7d"], 8: ["A-CED.A.1", "A-CED.A.2"]}
B = Bank("rational-functions", "rf", STD)
R = random.Random(707)


wrap = wrapd
rs = rats


def ratval(N, D, v):
    return N(F(v)) / D(F(v))


def chk_same(N1, D1, N2, D2, avoid=()):
    for v in (F(7, 3), F(-11, 4), F(13, 5), F(-2, 7), F(19, 6)):
        if D1(v) == 0 or D2(v) == 0: continue
        assert N1(v) * D2(v) == N2(v) * D1(v), (N1, D1, N2, D2)


# ---------------- Skill 1: simplifying ----------------
S = 1
cases = [([2], [3], [-3], 1, 1), ([-5], [1], [-1], 1, 1), ([4], [0], [-4], 1, 1), ([F(1, 2)], [3], [-1], 2, 2), ([-2, 2], [0], [3], 1, 1), ([1], [-6, 6], [2], 1, 3),
         ([3], [], [-3, 0], 2, 1), ([-1], [-4], [4, 2], 1, 1)]
for com, nr, dr, a, d in cases:
    N, D = P.roots(com + nr, a), P.roots(com + dr, d); Ns, Ds = reduce_rat(P.roots(nr, a), P.roots(dr, d))
    chk_same(N, D, Ns, Ds)
    excl = sorted(set(com + dr))
    B.sa(S, "cp1" if len(com) == 1 else "honors", f"Simplify ({N})/({D}) and state the excluded values.", f"{rs(Ns, Ds)}; x ≠ {', '.join(fr(v) for v in excl)}",
         [f"Factor: {rs(N, D)}.", "Divide out common factors.", f"Excluded values come from the ORIGINAL denominator: x ≠ {', '.join(fr(v) for v in excl)}."])
for N, D, ans in [(P.coeffs(1, -3), P.coeffs(-1, 3), "-1"), (P.coeffs(-2, 8), P.coeffs(1, -8, 16), "-2/(x - 4)"), (P.coeffs(5, -15, 0), P.coeffs(10, 0), "(x - 3)/2"), (P.coeffs(-1, 0, 9), P.coeffs(1, -3), "-(x + 3)")]:
    num, den = ans.split("/") if "/" in ans else (ans, "1")
    B.sa(S, "cp1", f"Simplify ({N})/({D}).", ans, [f"Factor: {rs(N, D)}.", "Note that (a - b) = -(b - a); divide out common factors.", f"Result: {ans}."])
    for v in (F(7, 3), F(-11, 4)): assert same(float(ratval(N, D, v)), peval(ans, x=float(v)))
B.sa(S, "honors", "Simplify (x³ - 8)/(x² - 4).", "(x² + 2x + 4)/(x + 2)", ["x³ - 8 = (x - 2)(x² + 2x + 4); x² - 4 = (x - 2)(x + 2).", "Cancel (x - 2); x ≠ ±2."])
chk_same(P.coeffs(1, 0, 0, -8), P.coeffs(1, 0, -4), P.coeffs(1, 2, 4), P.coeffs(1, 2))
B.sa(S, "honors", "Simplify (x³ + 27)/(x² - 3x + 9).", "x + 3", ["Sum of cubes: (x + 3)(x² - 3x + 9).", "x² - 3x + 9 is never 0 for real x, so no excluded values."])
chk_same(P.coeffs(1, 0, 0, 27), P.coeffs(1, -3, 9), P.coeffs(1, 3), P([1]))
B.mc(S, "cp1", "A student simplifies (x + 6)/(x + 2) to 3 by canceling the x's and dividing 6 by 2. What is correct?", "It is already simplified; you can only cancel common FACTORS", ["3", "x + 3", "6/2 = 3, so the answer is 3x"],
     ["x is a term, not a factor, of x + 6.", "Check x = 1: 7/3 ≠ 3."], tags=["error-analysis", "misconception"])
B.mc(S, "cp1", "Which expression equals (x - 5)/(5 - x) for x ≠ 5?", "-1", ["1", "0", "x - 5"], ["5 - x = -(x - 5)."], tags=["misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions equivalent to (x² - 9)/(x² + x - 6) for x ≠ -3, 2.", ["(x - 3)/(x - 2)", "(3 - x)/(2 - x)", "(x - 3)/(x + 2)", "-(x - 3)/(x - 2)", "(x + 3)/(x - 2)", "1 - 1/(x - 2)"],
         lambda s_: is_equiv("(x - 3)/(x - 2)")(s_), ["(x - 3)(x + 3)/((x + 3)(x - 2)).", "(3 - x)/(2 - x) = (x - 3)/(x - 2); 1 - 1/(x - 2) = (x - 3)/(x - 2)."])
sel_auto(B, S, "honors", "f(x) = (x² - 4)/(x² - 3x + 2). Select ALL true statements.", ["f(x) = (x + 2)/(x - 1) for x ≠ 2", "x = 1 is excluded", "x = 2 is excluded", "f(0) = -2", "f(2) = 4", "x = -2 is excluded"],
         lambda s_: s_ in ("f(x) = (x + 2)/(x - 1) for x ≠ 2", "x = 1 is excluded", "x = 2 is excluded", "f(0) = -2"), ["(x - 2)(x + 2)/((x - 1)(x - 2)).", "Both zeros of the original denominator are excluded; f(2) is undefined.", "f(0) = -4/2 = -2."])
B.orq(S, "cp1", "Consider (2x² - 8x)/(x² - 16).", [("Factor the numerator.", "2x(x - 4)"), ("Factor the denominator.", "(x - 4)(x + 4)"), ("Simplify.", "2x/(x + 4)"), ("State all excluded values.", "x ≠ 4, x ≠ -4")],
      ["GCF 2x.", "Difference of squares.", "Cancel (x - 4).", "Zeros of the original denominator."])
B.orq(S, "honors", "Write a rational expression that simplifies to (x + 1)/(x - 3) and has excluded values 3 and 5.", [("Choose the extra common factor.", "x - 5"), ("Write the unsimplified expression.", "(x² - 4x - 5)/(x² - 8x + 15)"),
      ("Verify by simplifying.", "((x + 1)(x - 5))/((x - 3)(x - 5)) = (x + 1)/(x - 3)"), ("Evaluate the original at x = 0.", "-1/3")],
      ["A common factor that is 0 at x = 5.", "Multiply out.", "Cancel.", "-5/15."], tags=["reasoning"])
assert P.roots([-1, 5]) == P.coeffs(1, -4, -5) and P.roots([3, 5]) == P.coeffs(1, -8, 15)
B.sa(S, "cp2", "Simplify 12x³/(18x).", "2x²/3, x ≠ 0", ["Divide coefficients 12/18 = 2/3 and x³/x = x²."])
B.sa(S, "cp2", "Simplify (4x + 8)/(x + 2).", "4, x ≠ -2", ["4(x + 2)/(x + 2)."])
B.mc(S, "cp2", "What value is excluded from the domain of 5/(x - 7)?", "7", ["-7", "5", "0"], ["The denominator cannot be 0."])

# ---------------- Skill 2: multiplying and dividing ----------------
S = 2
mcases = [((P.roots([2]), P.roots([-3])), (P.roots([-3, 1]), P.roots([2, 5]))), ((P.roots([0], 3), P.roots([4])), (P.roots([4, -4]), P.roots([0, 0], 6))), ((P.roots([-1, 1]), P.roots([3, 0])), (P.roots([0, 0]), P.roots([1, 2]))),
          ((P.roots([5, -2]), P.roots([1])), (P.roots([1, 3]), P.roots([-2, 3]))), ((P.coeffs(2, 6), P.coeffs(1, -1)), (P.coeffs(1, -1, 0), P.coeffs(4, 12)))]
for (N1, D1), (N2, D2) in mcases:
    N, D = N1 * N2, D1 * D2
    Nn, Dd = reduce_rat(N, D)
    chk_same(N, D, Nn, Dd)
    B.sa(S, "cp1", f"Multiply and simplify: {rs(N1, D1, False)} · {rs(N2, D2, False)}.", rs(Nn, Dd), ["Factor every numerator and denominator.", "Divide out common factors.", f"Result: {rs(Nn, Dd)}."])
dcases = [((P.roots([3]), P.roots([-2])), (P.roots([3, -3]), P.roots([-2, 1]))), ((P.coeffs(1, 0, -1), P.coeffs(2, 0)), (P.coeffs(1, 1), P.coeffs(4, 0, 0))), ((P.roots([-4, 2]), P.roots([5])), (P.roots([2]), P.roots([5, -5]))),
          ((P.coeffs(3, -6), P.coeffs(1, 3)), (P.coeffs(1, -2), P.coeffs(1, 0, -9))), ((P.roots([1, 1]), P.roots([0])), (P.roots([1]), P.roots([0, 0])))]
for (N1, D1), (N2, D2) in dcases:
    N, D = N1 * D2, D1 * N2
    Nn, Dd = reduce_rat(N, D)
    chk_same(N, D, Nn, Dd)
    B.sa(S, "cp1" if N.deg <= 3 else "honors", f"Divide and simplify: {rs(N1, D1, False)} ÷ {rs(N2, D2, False)}.", rs(Nn, Dd), ["Multiply by the reciprocal of the divisor.", "Factor and divide out common factors.", f"Result: {rs(Nn, Dd)}."])
B.mc(S, "cp1", "What is the first step to divide (x + 1)/x ÷ (x² - 1)/x²?", "Multiply by the reciprocal: (x + 1)/x · x²/(x² - 1)", ["Cross-multiply", "Find a common denominator", "Cancel x + 1 with x² - 1 immediately"], ["Division by a fraction = multiplication by its reciprocal."])
B.mc(S, "cp1", "A student simplifies (x/3)·(6/x²) and writes 2x. What is the correct result?", "2/x", ["2x", "x/2", "2"], ["6x/(3x²) = 2/x."], tags=["error-analysis"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to (x² - 1)/(x + 2) · (x + 2)/(x - 1) for allowed x.", ["x + 1", "(x + 1)(x - 1)/(x - 1)", "(x² - 1)/(x - 1)", "x - 1", "1", "(x + 1)/(x + 2)"], is_equiv("x + 1"),
         ["(x - 1)(x + 1)(x + 2)/((x + 2)(x - 1)) = x + 1."])
sel_auto(B, S, "honors", "The product (x² - 4x)/(x² - 9) · (x + 3)/(x² - 16) is simplified. Select ALL excluded values.", ["3", "-3", "4", "-4", "0", "16"],
         lambda s_: s_ in ("3", "-3", "4", "-4"), ["Excluded values come from every original denominator: x² - 9 and x² - 16.", "0 is allowed (it zeros only a numerator)."], tags=["misconception"])
B.sa(S, "honors", "Simplify ((x² - x - 6)/(x² - 4)) ÷ ((x² - 9)/(x² + x - 6)).", "1", ["(x - 3)(x + 2)/((x - 2)(x + 2)) · (x + 3)(x - 2)/((x - 3)(x + 3)).", "Everything cancels: 1 (x ≠ ±2, ±3)."], tags=["challenge"])
chk_same(P.coeffs(1, -1, -6) * P.coeffs(1, 1, -6), P.coeffs(1, 0, -4) * P.coeffs(1, 0, -9), P([1]), P([1]))
B.sa(S, "honors", "Simplify the complex fraction (1 + 1/x)/(1 - 1/x²).", "x/(x - 1)", ["Multiply numerator and denominator by x²: (x² + x)/(x² - 1).", "x(x + 1)/((x - 1)(x + 1)) = x/(x - 1)."], tags=["challenge"])
assert same(peval("(1 + 1/x)/(1 - 1/x^2)", x=2.7), peval("x/(x - 1)", x=2.7))
B.sa(S, "honors", "Simplify (2/x - 3/y)/(4/x² - 9/y²).", "xy/(2y + 3x)", ["Multiply by x²y²: (2xy² - 3x²y)/(4y² - 9x²).", "xy(2y - 3x)/((2y - 3x)(2y + 3x))."], tags=["challenge"])
assert same(peval("(2/x - 3/y)/(4/x^2 - 9/y^2)", x=1.3, y=2.9), peval("x*y/(2*y + 3*x)", x=1.3, y=2.9))
B.orq(S, "cp1", "Compute (x² + 5x + 6)/(x² - 1) · (x - 1)/(x + 3).", [("Factor all parts.", "(x + 2)(x + 3)/((x - 1)(x + 1)) · (x - 1)/(x + 3)"), ("Cancel common factors.", "(x + 2)/(x + 1)"), ("List excluded values.", "x ≠ 1, -1, -3"), ("Evaluate at x = 2.", "4/3")],
      ["Factor.", "Cancel (x + 3), (x - 1).", "All original denominators.", "4/3."])
B.orq(S, "honors", "A rectangle has area (x² - 9)/(x + 1) and length (x + 3)/(x² - 1).", [("Write the width as a quotient.", "(x² - 9)/(x + 1) ÷ (x + 3)/(x² - 1)"), ("Simplify the width.", "(x - 3)(x - 1)"), ("Expand it.", "x² - 4x + 3"), ("Find the width when x = 5.", "8")],
      ["Width = area ÷ length.", "Multiply by the reciprocal and cancel (x + 3), (x + 1).", "FOIL.", "2·4."], tags=["modeling"])
chk_same(P.coeffs(1, 0, -9) * P.coeffs(1, 0, -1), P.coeffs(1, 1) * P.coeffs(1, 3), P.coeffs(1, -4, 3), P([1]))
B.sa(S, "cp2", "Multiply (3/x)·(x²/9).", "x/3, x ≠ 0", ["3x²/(9x) = x/3."])
B.sa(S, "cp2", "Divide (5/x) ÷ (10/x³).", "x²/2, x ≠ 0", ["5/x · x³/10 = x²/2."])
B.mc(S, "cp2", "What is the reciprocal of (x - 2)/(x + 5)?", "(x + 5)/(x - 2)", ["(x - 2)/(x + 5)", "-(x - 2)/(x + 5)", "(2 - x)/(x + 5)"], ["Swap numerator and denominator."])

# ---------------- Skill 3: adding and subtracting ----------------
S = 3
acases = [((3, 0), (5, 1), "+"), ((2, 1), (1, -1), "-"), ((4, 2), (-1, -2), "+"), ((1, 3), (2, 0), "-"), ((5, -1), (3, -1), "+"), ((x_ := 7, 4), (2, 4), "-")]
for (a, p), (b, q), op in acases:
    D1, D2 = P.roots([p]), P.roots([q])
    if p == q:
        N = P([a + b if op == "+" else a - b]); D = D1
    else:
        N = P([a]) * D2 + (P([b]) if op == "+" else P([-b])) * D1; D = D1 * D2
    ans = rs(*reduce_rat(N, D))
    for v in (F(7, 3), F(-9, 5)):
        lhs = F(a) / D1(v) + (F(b) if op == "+" else -F(b)) / D2(v); assert lhs == N(v) / D(v)
    B.sa(S, "cp2" if p == q else "cp1", f"Simplify {a}/{wrap(factor_str(D1))} {op} {b}/{wrap(factor_str(D2))}.", ans, ["Find the least common denominator.", "Rewrite each fraction over the LCD and combine numerators.", f"Result: {ans}."])
for (n1, d1), (n2, d2), op in [((P([1]), P.roots([2, -2])), (P([1]), P.roots([2])), "+"), ((P.coeffs(1, 0), P.roots([-1, 3])), (P([2]), P.roots([3])), "-"), ((P([3]), P.coeffs(1, 0, -1)), (P([1]), P.coeffs(1, 1)), "-"),
                               ((P.coeffs(1, 1), P.coeffs(1, -5, 6)), (P([2]), P.coeffs(1, -2)), "+"), ((P.coeffs(2, 0), P.coeffs(1, 0, -9)), (P([1]), P.coeffs(1, 3)), "-")]:
    D = d1; extra = d1 // d2; assert d1 % d2 == P([0])
    N = n1 + (n2 * extra if op == "+" else -(n2 * extra))
    Nn, Dd = reduce_rat(N, D)
    chk_same(N, D, Nn, Dd)
    ans = rs(Nn, Dd)
    B.sa(S, "cp1" if N.deg < 2 else "honors", f"Simplify {wrapn(pstr(n1))}/{wrapd(pstr(d1))} {op} {wrapn(pstr(n2))}/{wrapd(pstr(d2))}.", ans, [f"Factor denominators; LCD = {factor_str(D)}.", "Rewrite, combine numerators, then simplify.", f"Result: {ans}."])
B.mc(S, "cp1", "A student writes 1/x + 1/y = 2/(x + y). What is correct?", "(x + y)/(xy)", ["2/(x + y)", "2/(xy)", "1/(x + y)"], ["LCD xy: y/(xy) + x/(xy)."], tags=["error-analysis", "misconception"])
B.mc(S, "cp1", "A student simplifies 5/(x - 2) - (x + 3)/(x - 2) and gets (8 - x)/(x - 2). What is the correct result?", "(2 - x)/(x - 2) = -1", ["(8 - x)/(x - 2)", "(x + 8)/(x - 2)", "1"], ["Subtract the WHOLE numerator: 5 - (x + 3) = 2 - x.", "(2 - x)/(x - 2) = -1."], tags=["error-analysis"])
B.mc(S, "cp1", "What is the LCD of 1/(x² - 4) and 3/(x² + 4x + 4)?", "(x - 2)(x + 2)²", ["(x² - 4)(x² + 4x + 4)", "(x - 2)(x + 2)", "x + 2"], ["Factor: (x - 2)(x + 2) and (x + 2)².", "Use each factor to its highest power."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to 2/x + 3/(x + 1).", ["(5x + 2)/(x(x + 1))", "(5x + 2)/(x² + x)", "5/(2x + 1)", "(2x + 2 + 3x)/(x² + x)", "5/(x² + x)", "(5x + 3)/(x(x + 1))"], is_equiv("2/x + 3/(x + 1)"),
         ["LCD x(x + 1): (2(x + 1) + 3x)/(x(x + 1)) = (5x + 2)/(x² + x)."])
B.sa(S, "honors", "Simplify 1/(x - 1) - 2/(x² - 1) + 1/(x + 1).", "2/(x + 1)", ["LCD (x - 1)(x + 1).", "(x + 1) - 2 + (x - 1) = 2x - 2 = 2(x - 1).", "2(x - 1)/((x - 1)(x + 1))."], tags=["challenge"])
assert same(peval("1/(x - 1) - 2/(x^2 - 1) + 1/(x + 1)", x=3.3), peval("2/(x + 1)", x=3.3))
B.sa(S, "honors", "Find A and B so that (5x - 1)/((x - 1)(x + 2)) = A/(x - 1) + B/(x + 2).", "A = 4/3, B = 11/3", ["5x - 1 = A(x + 2) + B(x - 1).", "x = 1: 4 = 3A; x = -2: -11 = -3B."], tags=["challenge", "connections"])
assert same(peval("(5x - 1)/((x - 1)(x + 2))", x=2.2), peval("(4/3)/(x - 1) + (11/3)/(x + 2)", x=2.2))
B.orq(S, "cp1", "Simplify 3/(x + 2) + x/(x - 2).", [("Find the LCD.", "(x + 2)(x - 2)"), ("Rewrite the numerators over the LCD.", "3(x - 2) + x(x + 2)"), ("Simplify the numerator.", "x² + 5x - 6"), ("Write the final answer in factored form.", "(x + 6)(x - 1)/((x + 2)(x - 2))")],
      ["Product of the distinct factors.", "Multiply each numerator by the missing factor.", "3x - 6 + x² + 2x.", "Factor."])
assert P.coeffs(1, 5, -6) == P.roots([-6, 1])
B.orq(S, "honors", "Two workers paint a room: one in x hours, the other in x + 2 hours.", [("Write each worker's rate.", "1/x and 1/(x + 2)"), ("Write their combined rate as one fraction.", "(2x + 2)/(x(x + 2))"), ("Find the combined rate when x = 4.", "5/12 room per hour"), ("How long do they take together when x = 4?", "12/5 = 2.4 hours")],
      ["Rate = 1 job per time.", "LCD x(x + 2).", "10/24.", "Reciprocal of the rate."], tags=["modeling"])
B.sa(S, "cp2", "Simplify 4/x + 7/x.", "11/x", ["Same denominator: add numerators."])
B.sa(S, "cp2", "Simplify 9/(2x) - 3/(2x).", "3/x", ["6/(2x) = 3/x."])

# ---------------- Skill 4: solving rational equations ----------------
S = 4
found = 0
for a, p, b, q, c in itertools.product([1, 2, 3, 4, 6], [-3, -1, 1, 2, 4], [1, 2, 3, 5], [-4, -2, 0, 3], [1, 2]):
    if p == q or found >= 11: continue
    poly = P([a]) * P.roots([q]) + P([b]) * P.roots([p]) - P([c]) * P.roots([p, q])
    rts, rest = poly.rational_roots()
    if rest.deg != 0 or not rts or len(set(rts)) < 2 or any(r in (p, q) for r in rts) or any(abs(r) > 12 or F(r).denominator > 2 for r in rts): continue
    if R.random() < 0.6: continue
    found += 1
    for r in rts: assert F(a) / (r - p) + F(b) / (r - q) == c
    eq = f"{a}/{wrap(lin_factor(p))} + {b}/{wrap(lin_factor(q))} = {c}"
    B.sa(S, "cp1" if all(F(r).denominator == 1 for r in rts) else "honors", f"Solve {eq}.", " or ".join(f"x = {fr(r)}" for r in sorted(set(rts))),
         [f"Multiply both sides by the LCD {lin_factor(p)}{lin_factor(q)}.", f"Simplify to {pstr(-poly if poly.lead < 0 else poly)} = 0.", "Solve and check that no solution makes a denominator 0."])
for eq, ans, steps in [("3/x = 6/(x + 4)", "x = 4", ["Cross-multiply: 3x + 12 = 6x.", "x = 4."]), ("x/(x - 2) = 3/5", "x = -3", ["5x = 3x - 6 → x = -3."]), ("2/(x + 1) = (x - 1)/4", "x = 3 or x = -3", ["x² - 1 = 8 → x² = 9."]),
                       ("1/x + 1/(2x) = 1/4", "x = 6", ["LCD 4x: 4 + 2 = x."]), ("x/3 - 4/x = 1/3", "x = 4 or x = -3", ["Multiply by 3x: x² - 12 = x → x² - x - 12 = 0."]), ("5/(x - 3) = (x + 2)/(x - 3) + 1", "no solution", ["5 = x + 2 + x - 3 → x = 3.", "x = 3 makes a denominator 0: extraneous."])]:
    B.sa(S, "cp2" if "Cross" in steps[0] else "cp1", f"Solve {eq}.", ans, steps)
for eq, sols in [("3/x = 6/(x + 4)", [4]), ("x/(x - 2) = 3/5", [-3]), ("2/(x + 1) = (x - 1)/4", [3, -3]), ("1/x + 1/(2x) = 1/4", [6]), ("x/3 - 4/x = 1/3", [4, -3])]:
    l, r = eq.split(" = ")
    for v in sols: assert same(peval(l, x=v), peval(r, x=v))
B.mc(S, "cp1", "What should you multiply both sides of 2/x + 1/(x - 3) = 4 by?", "x(x - 3)", ["x + x - 3", "4x", "(x - 3)²"], ["Use the LCD of all denominators."])
sel_auto(B, S, "cp1", "Select ALL solutions of x + 6/x = 5.", ["2", "3", "-2", "-3", "6", "0"], lambda s_: s_ != "0" and same(int(s_) + 6 / int(s_), 5), ["x² - 5x + 6 = 0 → x = 2 or 3."])
sel_auto(B, S, "honors", "Select ALL solutions of 8/(x² - 1) = 1.", ["3", "-3", "1", "-1", "√8"], lambda s_: s_ in ("3", "-3"), ["x² - 1 = 8 → x² = 9.", "±1 are excluded."])
B.orq(S, "cp1", "Solve 1/(x - 2) + 1/(x + 2) = 4/(x² - 4).", [("Find the LCD.", "(x - 2)(x + 2)"), ("Clear denominators.", "(x + 2) + (x - 2) = 4"), ("Solve.", "x = 2"), ("Check and state the solution.", "x = 2 makes a denominator 0: no solution")],
      ["x² - 4 = (x - 2)(x + 2).", "Multiply every term by the LCD.", "2x = 4.", "Extraneous."], tags=["error-analysis"])
B.orq(S, "honors", "Solve x/(x - 3) - 2/(x + 1) = 12/(x² - 2x - 3).", [("Factor the right-side denominator.", "(x - 3)(x + 1)"), ("Clear denominators.", "x(x + 1) - 2(x - 3) = 12"), ("Solve the quadratic.", "x = 3 or x = -2"), ("State the solution.", "x = -2")],
      ["x² - 2x - 3.", "Multiply by the LCD.", "x² - x - 6 = 0.", "x = 3 is extraneous."], tags=["multistep"])
assert same(-2 / (-5) - 2 / (-1), 12 / (4 + 4 - 3))

# ---------------- Skill 5: excluded values and extraneous solutions ----------------
S = 5
for N, D in [(P.coeffs(1, 2), P.coeffs(1, -5, 6)), (P.coeffs(3, 0), P.coeffs(1, 0, -16)), (P.coeffs(1, -1), P.coeffs(2, 3, -2)), (P([7]), P.coeffs(1, 0, 4)), (P.coeffs(1, 0, 0), P.coeffs(1, -6, 9, 0))]:
    ex = sorted(set(D.rational_roots()[0]))
    ans = "none" if not ex else ", ".join(f"x = {fr(v)}" for v in ex)
    B.sa(S, "cp2" if D.deg < 3 else "cp1", f"State the excluded values of ({N})/({D}).", ans, [f"Set the denominator {D} equal to 0.", f"{factor_str(D)} = 0" + ("; it has no real zeros." if not ex else "."), f"Excluded: {ans}."])
for eq, ans, steps, lvl in [("x/(x - 4) = 4/(x - 4) + 3", "no solution (x = 4 is extraneous)", ["x = 4 + 3(x - 4) → x = 4.", "x = 4 makes the denominator 0."], "cp1"),
                            ("x²/(x - 1) = 1/(x - 1)", "x = -1 (x = 1 is extraneous)", ["x² = 1 → x = ±1.", "x = 1 is excluded."], "cp1"),
                            ("6/(x² - 9) = 1/(x - 3)", "no solution (x = 3 is extraneous)", ["6 = x + 3 → x = 3.", "x = 3 is excluded."], "cp1"),
                            ("2/(x + 1) + 1 = (x + 3)/(x + 1)", "all real numbers except x = -1", ["2 + (x + 1) = x + 3 is always true.", "Every allowed x works; x ≠ -1."], "honors"),
                            ("(2x)/(x - 3) = 6/(x - 3) + x", "x = 2 (x = 3 is extraneous)", ["2x = 6 + x(x - 3) → x² - 5x + 6 = 0 → x = 2 or 3.", "x = 3 is excluded."], "honors"),
                            ("1/(x - 5) + 1/(x + 5) = 10/(x² - 25)", "no solution (x = 5 is extraneous)", ["(x + 5) + (x - 5) = 10 → x = 5.", "x = 5 is excluded."], "cp1")]:
    B.sa(S, lvl, f"Solve {eq}. Identify any extraneous solutions.", ans, steps, tags=["error-analysis"])
assert same(2 * 2 / (2 - 3), 6 / (2 - 3) + 2) and same((-1) ** 2 / (-2), 1 / (-2))
B.mc(S, "cp1", "Why must you check solutions of rational equations?", "Multiplying by an expression containing x can introduce values that make a denominator 0", ["Rational equations have no real solutions", "Calculators round incorrectly", "Cross-multiplying is invalid"], ["Clearing denominators can add solutions that are excluded values."], tags=["reasoning"])
B.mc(S, "cp1", "A student solving an equation with denominators x - 2 and x + 1 obtains x = 2 after clearing denominators. What should the student conclude?", "x = 2 is extraneous; check the original equation", ["x = 2 is the answer", "The equation has two solutions", "x = -2 is the answer"], ["x = 2 makes a denominator 0."], tags=["error-analysis"])
sel_auto(B, S, "cp1", "Select ALL excluded values of (x + 1)/(x² - x - 12).", ["4", "-3", "-1", "3", "-4", "12"], lambda s_: s_ in ("4", "-3"), ["x² - x - 12 = (x - 4)(x + 3).", "A zero of the numerator (-1) is allowed."], tags=["misconception"])
B.sel(S, "honors", "Select ALL equations that have an extraneous solution when solved by clearing denominators.", ["4/(x² - 4) = 1/(x - 2)", "x/(x - 3) = 3/(x - 3) + 2", "x²/(x + 2) = 4/(x + 2)"], ["x/4 = 3/x", "2/x = 1/(x + 1)", "1/(x - 1) = 2"],
      ["4 = x + 2 → x = 2 (excluded).", "x = 3 + 2x - 6 → x = 3 (excluded).", "x² = 4 → x = ±2; -2 is excluded.", "The others give x = ±2√3, x = -2, x = 3/2 — all allowed."], tags=["reasoning"])
B.orq(S, "honors", "Let f(x) = (x² - 1)/(x - 1).", [("State the excluded value.", "x = 1"), ("Simplify f.", "x + 1"), ("Solve f(x) = 2.", "no solution: x = 1 is excluded"), ("Describe the graph of f.", "the line y = x + 1 with a hole at (1, 2)")],
      ["Denominator 0.", "Cancel (x - 1).", "x + 1 = 2 → x = 1, excluded.", "Removable discontinuity."], tags=["connections", "graph"])
B.sa(S, "cp2", "Find the excluded value of 4/(2x + 6).", "x = -3", ["2x + 6 = 0."])
B.sa(S, "cp1", "Solve 3/(x - 1) = 3/(x - 1) + 2 and explain.", "no solution", ["Subtracting gives 0 = 2, a false statement."])

# ---------------- Skill 6: asymptotes ----------------
S = 6
acases = [(P.coeffs(1), P.roots([3]), ), (P.coeffs(2, 1), P.roots([-1])), (P.coeffs(3, 0, 0), P.roots([2, -2])), (P.coeffs(1, -4), P.roots([-5, 1])), (P.coeffs(5, 0), P.coeffs(1, 0, 1)), (P.coeffs(1, 0, 0), P.coeffs(1, -1)),
          (P.roots([2, -1]), P.roots([2, 3])), (P.coeffs(-4, 0, 1), P.coeffs(2, -3, -2)), (P.coeffs(1, 0, 0, 0), P.coeffs(1, 0, -4))]
for t in acases:
    N, D = t[0], t[1]
    nr = Counter(N.rational_roots()[0]); dr = Counter(D.rational_roots()[0]); holes = sorted((nr & dr).keys()); vas = sorted(set(dr) - set(holes))
    if N.deg < D.deg: ha = "y = 0"
    elif N.deg == D.deg: ha = f"y = {fr(N.lead / D.lead)}"
    else: ha = "none" + (f" (slant asymptote y = {pstr(N // D)})" if N.deg == D.deg + 1 else "")
    va = ", ".join(f"x = {fr(v)}" for v in vas) or "none"
    hs = "" if not holes else "; hole at " + ", ".join(pt(h, ratval(N // P.roots([h]), D // P.roots([h]), h)) for h in holes)
    ans = f"VA: {va}; HA: {ha}{hs}"
    lvl = "honors" if ("slant" in ha or holes or N.deg > D.deg) else ("cp1" if D.deg > 1 else "cp2")
    B.sa(S, lvl, f"Find all vertical and horizontal asymptotes of f(x) = ({N})/({D})." + (" Note any holes." if holes else ""), ans,
         ["Factor and cancel common factors (canceled factors give holes).", "Vertical asymptotes at remaining zeros of the denominator.", "Compare degrees for the horizontal asymptote.", ans + "."])
for nd, dd, ha in [(1, 2, "y = 0"), (2, 2, "y = ratio of leading coefficients"), (3, 2, "no horizontal asymptote")]:
    B.mc(S, "cp1", f"If the numerator has degree {nd} and the denominator has degree {dd}, what is the horizontal asymptote?", ha, [h for h in ["y = 0", "y = ratio of leading coefficients", "no horizontal asymptote", "y = 1"] if h != ha][:3], ["Bottom-heavy → y = 0; equal → ratio; top-heavy → none."])
B.mc(S, "cp1", "A student says f(x) = (x - 2)/((x - 2)(x + 5)) has vertical asymptotes x = 2 and x = -5. What is correct?", "Only x = -5; x = 2 is a hole", ["Correct as stated", "Only x = 2", "No vertical asymptotes"], ["Common factors give holes, not asymptotes."], tags=["error-analysis", "misconception"])
B.mc(S, "honors", "Can a graph cross its horizontal asymptote?", "Yes; a horizontal asymptote describes end behavior only", ["Never", "Only if the degree is 1", "Only at x = 0"], ["Example: y = x/(x² + 1) crosses y = 0 at x = 0."], tags=["reasoning", "misconception"])
sel_auto(B, S, "cp1", "f(x) = (2x + 6)/(x² - 9). Select ALL true statements.", ["VA x = 3", "Hole at x = -3", "HA y = 0", "VA x = -3", "HA y = 2", "f has an x-intercept at -3"],
         lambda s_: s_ in ("VA x = 3", "Hole at x = -3", "HA y = 0"), ["2(x + 3)/((x - 3)(x + 3)) = 2/(x - 3).", "Degree 1 < 2 → y = 0.", "x = -3 is a hole, so not an intercept."])
sel_auto(B, S, "honors", "Select ALL functions with horizontal asymptote y = 3.", ["y = (3x + 1)/(x - 2)", "y = (6x² - 1)/(2x² + 5)", "y = 3 + 1/x", "y = 3x/(x² + 1)", "y = (x + 3)/(x - 1)", "y = (3x³)/(x² + 1)"],
         lambda s_: s_ in ("y = (3x + 1)/(x - 2)", "y = (6x² - 1)/(2x² + 5)", "y = 3 + 1/x"), ["Equal degrees: ratio of leading coefficients.", "3x/(x² + 1) → 0; (x + 3)/(x - 1) → 1; 3x³/(x² + 1) has none."])
B.sa(S, "honors", "Write a rational function with VA x = 2 and x = -1, HA y = 4, and x-intercept 0.", "f(x) = 4x²/((x - 2)(x + 1)) (one answer)", ["Denominator (x - 2)(x + 1); equal degrees with leading ratio 4.", "Numerator 4x² has zero at 0."], tags=["reasoning"])
B.orq(S, "honors", "f(x) = (x² + x - 6)/(x - 1).", [("Find the vertical asymptote.", "x = 1"), ("Is there a horizontal asymptote?", "No (numerator degree is larger)"), ("Find the slant asymptote.", "y = x + 2"), ("Find the x-intercepts.", "x = -3 and x = 2")],
      ["Denominator zero, no cancellation.", "Degree 2 > 1.", "Divide: x² + x - 6 = (x - 1)(x + 2) - 4.", "(x + 3)(x - 2) = 0."], tags=["challenge"])
assert P.coeffs(1, 1, -6).divmod(P.coeffs(1, -1)) == (P.coeffs(1, 2), P([-4]))
B.orq(S, "cp1", "f(x) = 3/(x + 2) - 1.", [("Find the vertical asymptote.", "x = -2"), ("Find the horizontal asymptote.", "y = -1"), ("State the domain.", "x ≠ -2"), ("State the range.", "y ≠ -1")],
      ["x + 2 = 0.", "Shifted down 1.", "Exclude the VA.", "Exclude the HA value."])

# ---------------- Skill 7: graphing ----------------
S = 7
gcases = [(1, 2, 1, "y = 1/(x - 2) + 1"), (-2, -1, 0, "y = -2/(x + 1)"), (3, 0, -2, "y = 3/x - 2"), (1, -3, 2, "y = 1/(x + 3) + 2"), (-1, 1, -1, "y = -1/(x - 1) - 1")]
for a, h, k, nm in gcases:
    fn = lambda v, a=a, h=h, k=k: a / (v - h) + k if abs(v - h) > 1e-9 else float("nan")
    dg = graph(B, f"s07-hyp-{a}-{h}-{k}".replace("-", "m").replace("s07mhypm", "s07-hyp-"), [(fn, {})], xr=(-7, 7), yr=(-7, 7), vlines=[h], hlines=[k], points=[(h + 1, a + k), (h - 1, -a + k)],
               alt=f"Graph of a hyperbola-shaped rational function with dashed asymptotes x = {h} and y = {k}, passing through ({h + 1}, {a + k}) and ({h - 1}, {k - a}).")
    B.orq(S, "cp1", f"The graph shows {nm}.", [("Find the vertical asymptote.", f"x = {h}"), ("Find the horizontal asymptote.", f"y = {k}"), ("State the domain and range.", f"x ≠ {h}; y ≠ {k}"), ("Name one point on the graph.", f"({h + 1}, {a + k})")],
          ["Denominator zero.", "Vertical shift k.", "Exclude asymptote values.", f"x = {h + 1}: y = {a}/1 + {k}."], diagram=dg, tags=["graph"])
    wr = [f"y = {a}/(x {'+' if h >= 0 else '-'} {abs(h)}) + {k}".replace("/(x + 0)", "/x").replace("/(x - 0)", "/x"), f"y = {a}/(x - {h}) - {k}".replace("- -", "+ ").replace("(x - 0)", "x").replace("(x - -", "(x + "), f"y = {-a}/(x - {h}) + {k}".replace("(x - 0)", "x").replace("(x - -", "(x + ")]
    wr = [w.replace("+ -", "- ").replace("1/", "1/").replace("y = 1/", "y = 1/").replace(" + 0", "").replace(" - 0", "") for w in wr]
    B.mc(S, "cp1", "Which equation matches the graph?", nm, [w for w in wr if w != nm] + [nm.replace("y = ", "y = 2·") if a == 1 else nm.replace(str(abs(a)), str(abs(a) + 1), 1)], ["Asymptotes give h and k.", f"The point ({h + 1}, {a + k}) gives a = {a}."], diagram=dg, tags=["graph"])
for N, D, nm in [(P.coeffs(1, 0), P.roots([-2, 2]), "y = x/(x² - 4)"), (P.coeffs(2, -2), P.coeffs(1, 3), "y = (2x - 2)/(x + 3)"), (P.roots([1, 3]), P.roots([1]) * P.coeffs(1, 0) * 1, "y = (x² - 4x + 3)/(x² - x)")]:
    nrt = Counter(N.rational_roots()[0]); drt = Counter(D.rational_roots()[0]); holes = sorted((nrt & drt).keys())
    xi = sorted(set(nrt) - set(holes)); yi = "none" if D(0) == 0 else fr(N(0) / D(0)); vas = sorted(set(drt) - set(holes))
    ha = "y = 0" if N.deg < D.deg else f"y = {fr(N.lead / D.lead)}"
    dg = graph(B, "s07-rat-" + str(len(B.qs)), [(lambda v, N=N, D=D: N(float(v)) / D(float(v)) if abs(D(float(v))) > 1e-9 else float("nan"), {})], xr=(-7, 7), yr=(-7, 7), vlines=vas, hlines=[0 if N.deg < D.deg else float(N.lead / D.lead)],
               points=[(r, 0) for r in xi] + [(h_, float(ratval(N // P.roots([h_]), D // P.roots([h_]), h_)), False) for h_ in holes], alt=f"Graph of {nm} with dashed asymptotes " + ", ".join(f"x = {fr(v)}" for v in vas) + f" and {ha}" + (", and an open circle (hole)" if holes else "") + ".")
    B.orq(S, "honors" if holes or D.deg > 1 else "cp1", f"Analyze {nm} (graph shown).", [("Find the x-intercept(s).", ", ".join(fr(v) for v in xi) or "none"), ("Find the y-intercept.", yi), ("Find the vertical asymptote(s).", ", ".join(f"x = {fr(v)}" for v in vas)),
          ("Find the horizontal asymptote" + (" and the hole." if holes else "."), ha + ("; hole at " + ", ".join(pt(h_, ratval(N // P.roots([h_]), D // P.roots([h_]), h_)) for h_ in holes) if holes else ""))],
          ["Zeros of the simplified numerator.", "Evaluate at 0 if defined.", "Zeros of the simplified denominator.", "Degree comparison; canceled factors give holes."], diagram=dg, tags=["graph", "multistep"])
sel_auto(B, S, "cp1", "Select ALL points on the graph of y = 4/(x - 1).", ["(2, 4)", "(3, 2)", "(-1, -2)", "(5, 1)", "(0, 4)", "(1, 4)"], lambda s_: (lambda u, w: u != 1 and same(4 / (u - 1), w))(*[int(t) for t in s_.strip("()").split(", ")]), ["Substitute each x."])
sel_auto(B, S, "honors", "y = (x + 1)/(x - 2). Select ALL true statements about the graph.", ["It crosses the x-axis at (-1, 0)", "Its y-intercept is (0, -1/2)", "It approaches y = 1 as x → ±∞", "It is above y = 1 for x > 2", "It has a hole at x = 2", "It crosses y = 1 at x = 0"],
         lambda s_: s_ in ("It crosses the x-axis at (-1, 0)", "Its y-intercept is (0, -1/2)", "It approaches y = 1 as x → ±∞", "It is above y = 1 for x > 2"), ["(x + 1)/(x - 2) = 1 + 3/(x - 2).", "For x > 2, 3/(x - 2) > 0; it never equals 1."])
B.mc(S, "cp1", "How is y = 1/(x + 4) - 3 related to y = 1/x?", "Shifted left 4 and down 3", ["Shifted right 4 and down 3", "Shifted left 4 and up 3", "Shifted right 3 and down 4"], ["(x + 4) → left 4; -3 → down 3."], tags=["misconception"])
B.sa(S, "cp1", "Describe the end behavior of y = (2x² - 1)/(x² + 3).", "y → 2 as x → ±∞", ["Equal degrees: ratio 2/1."])
B.sa(S, "honors", "For y = 1/(x - 3)², describe the behavior near x = 3.", "y → +∞ from both sides", ["The squared denominator is positive on both sides of 3."], tags=["reasoning"])

# ---------------- Skill 8: variation and modeling ----------------
S = 8
for kind, x1, y1, x2 in [("inversely", 4, 9, 6), ("inversely", 10, 3, 5), ("directly", 3, 12, 7), ("inversely", F(1, 2), 8, 2), ("jointly with x and z", (2, 3), 30, (5, 4))]:
    if kind == "directly":
        k = F(y1, x1); y2 = k * x2; eqn = f"y = {fr(k)}x"
    elif kind == "inversely":
        k = F(y1) * x1; y2 = k / x2; eqn = f"y = {fr(k)}/x"
    else:
        k = F(y1, x1[0] * x1[1]); y2 = k * x2[0] * x2[1]; eqn = f"y = {fr(k)}xz"
    if kind.startswith("jointly"):
        prompt = f"y varies jointly with x and z. y = {y1} when x = {x1[0]} and z = {x1[1]}. Find y when x = {x2[0]} and z = {x2[1]}."
    else:
        prompt = f"y varies {kind} with x, and y = {y1} when x = {fr(x1)}. Write the equation and find y when x = {fr(x2)}."
    B.sa(S, "cp2" if kind != "jointly with x and z" else "cp1", prompt, f"{eqn}; y = {fr(y2)}", [f"Find k: {'k = xy' if kind == 'inversely' else 'k = y/x' if kind == 'directly' else 'k = y/(xz)'} = {fr(k)}.", f"y = {fr(y2)}."])
sel_auto(B, S, "cp1", "Select ALL equations that show inverse variation.", ["y = 5/x", "xy = 12", "y = 0.4/x", "y = 5x", "y = x/5", "y = 5 - x", "x = 3/y"], lambda s_: s_ in ("y = 5/x", "xy = 12", "y = 0.4/x", "x = 3/y"), ["Inverse variation: xy = k (k ≠ 0)."])
B.mc(S, "cp1", "Which table shows inverse variation?", "x: 1, 2, 4; y: 12, 6, 3", ["x: 1, 2, 4; y: 3, 6, 12", "x: 1, 2, 4; y: 12, 10, 6", "x: 1, 2, 4; y: 12, 6, 0"], ["The product xy is constant (12)."], tags=["multiple-representations"])
B.mc(S, "cp1", "If y varies inversely with x and x is tripled, what happens to y?", "y is divided by 3", ["y is tripled", "y decreases by 3", "y stays the same"], ["xy = k: tripling x forces y to one-third."], tags=["reasoning"])
B.sa(S, "cp1", "Two pipes fill a tank in 6 h and 3 h. How long together?", "2 hours", ["1/6 + 1/3 = 1/2 tank per hour.", "Time = 2 hours."], tags=["modeling"])
B.sa(S, "cp1", "One printer takes 4 h and together with a second they take 1.5 h. How long does the second take alone?", "2.4 hours", ["1/4 + 1/t = 2/3 → 1/t = 5/12.", "t = 12/5."], tags=["modeling"])
assert same(1 / 4 + 1 / 2.4, 1 / 1.5)
B.sa(S, "honors", "A boat goes 24 mi upstream and 24 mi back in 5 h total. Its speed in still water is 10 mph. Find the current's speed.", "2 mph", ["24/(10 - c) + 24/(10 + c) = 5.", "480 = 5(100 - c²) → c² = 4."], tags=["modeling", "challenge"])
assert same(24 / 8 + 24 / 12, 5)
B.sa(S, "honors", "How many liters of pure acid must be added to 10 L of a 20% solution to make a 50% solution?", "6 L", ["(2 + x)/(10 + x) = 0.5.", "2 + x = 5 + 0.5x → x = 6."], tags=["modeling"])
B.sa(S, "cp1", "The average cost of producing x items is C(x) = (500 + 4x)/x. Find C(100) and the horizontal asymptote, and interpret it.", "$9; y = 4: average cost approaches $4 per item", ["C(100) = 900/100.", "Degrees equal: 4/1."], tags=["modeling"])
B.orq(S, "cp1", "The intensity of light varies inversely with the square of the distance: I = k/d². I = 40 lux at d = 3 m.", [("Find k.", "360"), ("Find I at d = 6 m.", "10 lux"), ("What happens to I when d doubles?", "It is divided by 4"), ("At what distance is I = 90 lux?", "2 m")],
      ["k = 40·9.", "360/36.", "(2d)² = 4d².", "d² = 4."], tags=["modeling"])
B.orq(S, "honors", "A student averages 72 on 5 tests. She hopes to raise her average to 85 by scoring 100 on the remaining tests.", [("Write the average after x more 100s.", "A(x) = (360 + 100x)/(5 + x)"), ("Find A(5).", "86"), ("How many 100s are needed to reach 85?", "x = 13/3, so 5 tests"),
      ("What value does A(x) approach as x grows?", "100")],
      ["Total points over total tests.", "860/10.", "360 + 100x = 425 + 85x → 15x = 65.", "Ratio of leading coefficients."], tags=["modeling", "multistep"])
B.orq(S, "cp1", "Working together, Ana and Ben clean a garage in 3 hours. Ana alone takes 5 hours.", [("Write Ana's rate.", "1/5 garage per hour"), ("Write an equation for Ben's time t.", "1/5 + 1/t = 1/3"), ("Solve for t.", "7.5 hours"), ("Check your answer.", "1/5 + 2/15 = 3/15 + 2/15 = 1/3")],
      ["Rate = 1/time.", "Rates add.", "1/t = 2/15.", "Substitute."], tags=["modeling"])
B.sa(S, "cp2", "y varies inversely with x; y = 2 when x = 15. Find k.", "k = 30", ["k = xy."])
B.mc(S, "cp2", "Which equation models 'y varies directly with x²'?", "y = kx²", ["y = k/x²", "y = x²/k + 1", "y = kx + 2"], ["Direct variation with x²."])

# ================= additions: format balance =================
LV = ["cp2", "cp1", "honors"]
# Skill 1
for com, nr, dr in [([3], [-2], [1]), ([-4], [0], [4]), ([5], [2, -2], [0]), ([1], [-7], [7])]:
    N, D = P.roots(com + nr), P.roots(com + dr); Ns, Ds = reduce_rat(P.roots(nr), P.roots(dr)); good = rs(Ns, Ds)
    wr = [rs(*reduce_rat(P.roots([-v for v in nr]), P.roots(dr))), rs(*reduce_rat(P.roots(nr), P.roots([-v for v in dr]))), rs(*reduce_rat(P.roots(dr), P.roots(nr))) if P.roots(nr).deg else f"{factor_str(P.roots(dr))}", rs(P.roots(nr), P.roots(dr + [-com[0]])), rs(P.roots(nr + [-com[0]]), P.roots(dr))]
    B.mc(1, "cp1", f"Simplify ({N})/({D}).", good, wr, [f"Factor: {rs(N, D)}.", f"Cancel {lin_factor(com[0])}: {good}.", "Only common factors cancel, not common terms."])
for N, D, tgt, cands in [(P.roots([2, 5]), P.roots([5, -1]), "(x - 2)/(x + 1)", ["(x - 2)/(x + 1)", "(2 - x)/(-x - 1)", "(x - 2)/(x - 1)", "-2/1", "1 - 3/(x + 1)", "(x + 2)/(x + 1)"]),
                         (P.coeffs(1, 0, -16), P.coeffs(-1, 4), "-(x + 4)", ["-(x + 4)", "-x - 4", "x + 4", "(x + 4)/(-1)", "4 - x", "-x + 4"])]:
    sel_auto(B, 1, "honors", f"Select ALL expressions equivalent to ({N})/({D}) where defined.", cands, is_equiv(tgt), [f"{rs(N, D)} simplifies to {tgt}.", "Check each option by simplifying or substituting a value."])
B.sa(1, "cp1", "Simplify (x² + 2x - 15)/(x² - 9) and state the excluded values.", "(x + 5)/(x + 3); x ≠ ±3", ["(x + 5)(x - 3)/((x - 3)(x + 3))."])
chk_same(P.coeffs(1, 2, -15), P.coeffs(1, 0, -9), P.coeffs(1, 5), P.coeffs(1, 3))
B.orq(1, "honors", "f(x) = (x² - 2x - 8)/(x² - 16) and g(x) = (x + 2)/(x + 4).", [("Simplify f.", "(x + 2)/(x + 4)"), ("State the domains of f and g.", "f: x ≠ ±4; g: x ≠ -4"), ("Are f and g the same function? Explain.", "No: f is undefined at x = 4 but g(4) = 3/4"), ("Find f(0) and g(0).", "1/2 and 1/2")],
      ["(x - 4)(x + 2)/((x - 4)(x + 4)).", "Excluded values of each original form.", "Equal formulas, different domains.", "8/16 and 2/4."], tags=["reasoning"])
# Skill 2
for (N1, D1), (N2, D2), op in [((P.roots([1]), P.roots([2])), (P.roots([2, -3]), P.roots([1, 4])), "·"), ((P.roots([0]), P.roots([5])), (P.roots([0, 0]), P.roots([5, -5])), "÷"), ((P.roots([-2, 2]), P.roots([3])), (P.roots([2]), P.roots([3, 0])), "÷")]:
    N, D = (N1 * N2, D1 * D2) if op == "·" else (N1 * D2, D1 * N2); Nn, Dd = reduce_rat(N, D); good = rs(Nn, Dd)
    wr = [rs(*reduce_rat(N1 * D2, D1 * N2)) if op == "·" else rs(*reduce_rat(N1 * N2, D1 * D2)), rs(*reduce_rat(Nn * P.roots([0]) if Nn.deg < 2 else Nn, Dd)) if Nn.deg < 2 else rs(Dd, Nn), rs(Dd, Nn) if Nn.deg > 0 else f"-{good}"]
    B.mc(2, "cp1", f"Simplify {rs(N1, D1, False)} {op} {rs(N2, D2, False)}.", good, wr, ["Multiply by the reciprocal when dividing." if op == "÷" else "Multiply numerators and denominators.", "Factor and cancel.", f"Result: {good}."])
sel_auto(B, 2, "cp1", "Select ALL expressions equal to (x² - 4)/x ÷ (x + 2)/x².", ["x(x - 2)", "x² - 2x", "(x² - 4)/x · x²/(x + 2)", "(x - 2)/x", "(x + 2)x", "x - 2"], is_equiv("x*(x - 2)"), ["(x - 2)(x + 2)/x · x²/(x + 2) = x(x - 2)."])
B.orq(2, "cp1", "Simplify (x² - 25)/(x² + 3x) · (x + 3)/(x - 5).", [("Factor every part.", "(x - 5)(x + 5)/(x(x + 3)) · (x + 3)/(x - 5)"), ("Cancel common factors.", "(x + 5)/x"), ("State the excluded values.", "x ≠ 0, -3, 5"), ("Evaluate at x = 5 if possible.", "Undefined: 5 is excluded")],
      ["Difference of squares; GCF x.", "Cancel (x - 5), (x + 3).", "All original denominators (and the second numerator is not a divisor, so only denominators).", "Excluded."], tags=["misconception"])
B.sa(2, "cp1", "Multiply (x + 4)/(x - 3) · (x² - 9)/(x² + 4x).", "(x + 3)/x", ["(x + 4)/(x - 3) · (x - 3)(x + 3)/(x(x + 4))."])
chk_same(P.coeffs(1, 4) * P.coeffs(1, 0, -9), P.coeffs(1, -3) * P.coeffs(1, 4, 0), P.coeffs(1, 3), P.coeffs(1, 0))
B.sa(2, "honors", "Simplify (x³ - 1)/(x² - 1) ÷ (x² + x + 1)/(x + 1).", "1", ["(x - 1)(x² + x + 1)/((x - 1)(x + 1)) · (x + 1)/(x² + x + 1)."], tags=["challenge"])
chk_same(P.coeffs(1, 0, 0, -1) * P.coeffs(1, 1), P.coeffs(1, 0, -1) * P.coeffs(1, 1, 1), P([1]), P([1]))
# Skill 3
for (a, p), (b, q) in [((2, 3), (1, -2)), ((3, -1), (2, 1)), ((1, 4), (4, 0))]:
    N = P([a]) * P.roots([q]) + P([b]) * P.roots([p]); D = P.roots([p, q]); good = rs(*reduce_rat(N, D))
    wr = [f"{a + b}/({pstr(P.roots([p]) + P.roots([q]))})", f"{a + b}/{wrapd(factor_str(D))}", rs(*reduce_rat(P([a]) * P.roots([p]) + P([b]) * P.roots([q]), D))]
    B.mc(3, "cp1", f"Simplify {a}/{wrapd(lin_factor(p) if p else 'x')} + {b}/{wrapd(lin_factor(q) if q else 'x')}.", good, wr, ["LCD is the product of the two denominators.", "Multiply each numerator by the OTHER denominator, then add.", f"Result: {good}."], tags=["misconception"])
sel_auto(B, 3, "honors", "Select ALL expressions equal to 1/(x - 2) - 1/(x + 2).", ["4/(x² - 4)", "4/((x - 2)(x + 2))", "0", "-4/(x² - 4)", "2/(x² - 4)", "(x + 2 - x + 2)/(x² - 4)"], is_equiv("1/(x - 2) - 1/(x + 2)"), ["LCD (x - 2)(x + 2): ((x + 2) - (x - 2))/(x² - 4) = 4/(x² - 4)."])
B.orq(3, "cp1", "Simplify x/(x - 1) - 1/(x + 1).", [("Find the LCD.", "(x - 1)(x + 1)"), ("Write the combined numerator.", "x(x + 1) - (x - 1)"), ("Simplify the numerator.", "x² + 1"), ("Write the answer.", "(x² + 1)/((x - 1)(x + 1))")],
      ["Product of distinct factors.", "Subtract the whole second numerator.", "x² + x - x + 1.", "x² + 1 does not factor over the reals."], tags=["error-analysis"])
B.sa(3, "honors", "Simplify 1/(x + h) - 1/x and then divide the result by h.", "-1/(x(x + h))", ["(x - (x + h))/(x(x + h)) = -h/(x(x + h)).", "Divide by h."], tags=["connections", "challenge"])
assert same((1 / (2.3 + 0.7) - 1 / 2.3) / 0.7, -1 / (2.3 * 3.0))
B.sa(3, "cp1", "Simplify 2/(3x) + 5/(6x²).", "(4x + 5)/(6x²)", ["LCD 6x²: 4x/(6x²) + 5/(6x²)."])
B.mc(3, "cp2", "What is the LCD of 1/(4x) and 1/(6x²)?", "12x²", ["24x³", "10x²", "2x"], ["LCM of 4 and 6 is 12; highest power x²."])
# Skill 4
B.mc(4, "cp1", "Solve 4/(x + 1) = 2/(x - 3).", "x = 7", ["x = -5", "x = 1", "x = 3"], ["4(x - 3) = 2(x + 1) → 2x = 14."])
assert 4 / 8 == 2 / 4
B.mc(4, "cp1", "Solve x - 8/x = 2.", "x = 4 or x = -2", ["x = 4", "x = -4 or x = 2", "x = 8"], ["x² - 2x - 8 = 0 → (x - 4)(x + 2) = 0."])
xv = F(8, 5); assert 3 / (xv - 2) + 2 / (xv + 2) == F(10) / (xv * xv - 4)
B.mc(4, "honors", "Solve 3/(x - 2) + 2/(x + 2) = 10/(x² - 4).", "x = 8/5", ["x = 2", "no solution", "x = -8/5"], ["Multiply by (x - 2)(x + 2): 3(x + 2) + 2(x - 2) = 10.", "5x + 2 = 10 → x = 8/5, which is allowed."])
sel_auto(B, 4, "cp1", "Select ALL solutions of 2/x + 1/(x - 1) = 2.", ["2", "1/2", "1", "0", "-1/2", "-2"], lambda s_: s_ not in ("0", "1") and same(2 / float(F(s_)) + 1 / (float(F(s_)) - 1), 2), ["Multiply by x(x - 1): 2(x - 1) + x = 2x(x - 1).", "2x² - 5x + 2 = 0 → x = 2 or 1/2."])
B.orq(4, "cp1", "Solve x/(x + 2) + 1/x = 1.", [("Find the LCD.", "x(x + 2)"), ("Clear denominators.", "x² + x + 2 = x² + 2x"), ("Solve.", "x = 2"), ("Check.", "2/4 + 1/2 = 1 ✓")], ["Product.", "Multiply each term.", "x = 2.", "Substitute."])
assert same(2 / 4 + 1 / 2, 1)
B.sa(4, "cp2", "Solve 6/x = 3/4.", "x = 8", ["Cross-multiply: 3x = 24."])
for v in ((-1 + 61 ** 0.5) / 2, (-1 - 61 ** 0.5) / 2): assert same((v + 1) / 5, 3 / v)
B.sa(4, "cp1", "Solve (x + 1)/5 = 3/x. Give exact solutions.", "x = (-1 ± √61)/2", ["x² + x = 15 → x² + x - 15 = 0.", "Quadratic formula."])
# Skill 5
for N, D in [(P.coeffs(1, 0), P.roots([4, -1])), (P.coeffs(1, 3), P.roots([-3, 6])), (P([2]), P.coeffs(1, 0, -1, 0))]:
    ex = sorted(set(D.rational_roots()[0])); zs = sorted(set(N.rational_roots()[0]))
    cands = sorted(set([fr(v) for v in ex] + [fr(-v) for v in ex if -v not in ex] + [fr(v) for v in zs] + ["2"]), key=lambda t: float(F(t)))
    sel_auto(B, 5, "cp1", f"Select ALL excluded values of ({N})/({D}).", cands, lambda s_, D=D: D(F(s_)) == 0, [f"Solve {pstr(D)} = 0: {factor_str(D)} = 0.", "Zeros of the numerator are not excluded."], tags=["misconception"])
B.mc(5, "cp1", "Solve 2x/(x - 1) = 2/(x - 1) + 1.", "no solution", ["x = 1", "x = 2", "x = -1"], ["2x = 2 + (x - 1) → x = 1.", "x = 1 is excluded, so there is no solution."], tags=["error-analysis"])
B.mc(5, "cp1", "Solve (x + 3)/(x - 3) = 6/(x - 3) + 2.", "x = 3 is extraneous; no solution", ["x = 3", "x = 9", "x = -3"], ["x + 3 = 6 + 2x - 6 → x = 3.", "x = 3 is excluded."], tags=["error-analysis"])
B.mc(5, "honors", "Which equation has an extraneous solution?", "x/(x + 2) = -2/(x + 2)", ["x/(x + 2) = 2/(x + 2)", "x/2 = 2/x", "1/x = 1/2"], ["x = -2 makes the denominator 0."], tags=["reasoning"])
B.orq(5, "cp1", "Solve 1 + 4/(x - 2) = x/(x - 2).", [("State the excluded value.", "x = 2"), ("Clear denominators.", "x - 2 + 4 = x"), ("Simplify.", "2 = 0"), ("State the solution set.", "no solution")],
      ["x - 2 ≠ 0.", "Multiply by x - 2.", "False statement.", "No x works."])
B.orq(5, "honors", "Solve x/(x - 4) - 4/(x + 4) = 32/(x² - 16).", [("Find the LCD and excluded values.", "(x - 4)(x + 4); x ≠ ±4"), ("Clear denominators.", "x(x + 4) - 4(x - 4) = 32"), ("Solve.", "x = ±4"), ("State the solution set.", "no solution (both are extraneous)")],
      ["Factor x² - 16.", "Multiply every term.", "x² + 16 = 32 → x² = 16.", "Both excluded."], tags=["challenge", "error-analysis"])
B.sa(5, "cp1", "State the domain of f(x) = (x + 5)/(x² - 25).", "all real numbers except x = 5 and x = -5", ["x² - 25 = 0 → x = ±5."])
B.sa(5, "cp1", "Solve x/(x + 1) = 2 - 1/(x + 1).", "no solution (x = -1 is extraneous)", ["x = 2(x + 1) - 1 → x = -1.", "x = -1 is excluded."], tags=["error-analysis"])
# Skill 6
for N, D in [(P([4]), P.coeffs(1, -6)), (P.coeffs(3, 1), P.coeffs(2, -1)), (P.coeffs(1, 0, 0, 2), P.coeffs(1, 0, 1)), (P.coeffs(-6, 0, 0), P.coeffs(3, 0, -12)), (P.coeffs(1, 1), P.coeffs(1, 0, -1))]:
    holes = sorted(set(N.rational_roots()[0]) & set(D.rational_roots()[0])); vas = sorted(set(D.rational_roots()[0]) - set(holes))
    ha = "y = 0" if N.deg < D.deg else (f"y = {fr(N.lead / D.lead)}" if N.deg == D.deg else "none")
    ans = f"VA {', '.join(f'x = {fr(v)}' for v in vas) or 'none'}; HA {ha}"
    wr = [f"VA {', '.join(f'x = {fr(-v)}' for v in vas) or 'none'}; HA {ha}", f"VA {', '.join(f'x = {fr(v)}' for v in vas) or 'none'}; HA {'y = 1' if ha != 'y = 1' else 'y = 0'}", f"VA {', '.join(f'x = {fr(v)}' for v in sorted(set(D.rational_roots()[0]) | set(N.rational_roots()[0])))}; HA {ha}"]
    B.mc(6, "cp1" if D.deg == 1 else "honors", f"Which describes the asymptotes of f(x) = ({N})/({D})?", ans, wr, ["Vertical: zeros of the simplified denominator.", "Horizontal: compare degrees.", ans + "."])
sel_auto(B, 6, "cp1", "Select ALL functions with a vertical asymptote at x = 2.", ["y = 1/(x - 2)", "y = x/(x² - 4)", "y = 3/(2 - x) + 1", "y = (x - 2)/(x² - 4)", "y = 1/(x + 2)", "y = (x - 2)/(x + 1)"],
         lambda s_: s_ in ("y = 1/(x - 2)", "y = x/(x² - 4)", "y = 3/(2 - x) + 1"), ["Denominator 0 at x = 2 AND the factor does not cancel.", "(x - 2)/(x² - 4) has a hole at x = 2."])
B.orq(6, "cp1", "f(x) = (2x - 1)/(x + 3).", [("Find the vertical asymptote.", "x = -3"), ("Find the horizontal asymptote.", "y = 2"), ("Find the x-intercept.", "(1/2, 0)"), ("Find the y-intercept.", "(0, -1/3)")], ["x + 3 = 0.", "2/1.", "2x - 1 = 0.", "f(0)."])
B.sa(6, "cp2", "Find the vertical asymptote of y = 5/(x + 7).", "x = -7", ["x + 7 = 0."])
# Skill 7
for a, h, k in [(2, 1, -1), (-3, -2, 1), (1, 4, 0)]:
    nm = f"y = {a}/(x {'-' if h > 0 else '+'} {abs(h)}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}"
    xint = h - F(a, k) if k else None; yint = F(a, -h) + k
    B.sa(7, "cp1", f"Find the intercepts of {nm}.", f"x-intercept {'none' if xint is None else pt(xint, 0)}; y-intercept {pt(0, yint)}", ["Set y = 0 and solve for x.", "Set x = 0."])
    if xint is not None: assert F(a) / (xint - h) + k == 0
    st = {f"x = {h} is a vertical asymptote": True, f"y = {k} is a horizontal asymptote": True, f"The y-intercept is {pt(0, yint)}": True, f"x = {-h} is a vertical asymptote": False, f"y = {a} is a horizontal asymptote": a == k, f"The domain is all real numbers": False}
    B.sel(7, "cp1", f"Select ALL true statements about the graph of {nm}.", [s_ for s_, t_ in st.items() if t_], [s_ for s_, t_ in st.items() if not t_], ["Asymptotes x = h, y = k.", "Evaluate at x = 0."], tags=["graph"])
B.mc(7, "honors", "Which function's graph has a hole at x = 1 and a vertical asymptote at x = -1?", "y = (x - 1)/(x² - 1)", ["y = (x + 1)/(x² - 1)", "y = 1/(x² - 1)", "y = (x - 1)/(x + 1)²"], ["(x - 1)/((x - 1)(x + 1)) cancels (x - 1)."])
B.mc(7, "cp1", "In which quadrants does the graph of y = -4/x lie?", "II and IV", ["I and III", "I and II", "III and IV"], ["Negative a: x > 0 gives y < 0; x < 0 gives y > 0."])
B.sa(7, "cp2", "Name the asymptotes of y = 1/x + 5.", "x = 0 and y = 5", ["Shifted up 5."])
B.sa(7, "honors", "Write a rational function whose graph has VA x = 3, HA y = -2, and passes through (4, 0).", "y = 2/(x - 3) - 2", ["y = a/(x - 3) - 2; 0 = a - 2 → a = 2."], tags=["reasoning"])
# Skill 8
for k_, d_ in [(120, 8), (75, 3), (36, 4)]:
    B.sa(8, "cp1", f"The time t to travel a fixed distance varies inversely with speed s. At {k_ // d_ if k_ % d_ == 0 else F(k_, d_)} mph the trip takes {d_} h. How long at {2 * k_ // d_} mph?", f"{fr(F(d_, 2))} h", ["t = k/s with k = st.", f"k = {k_}; t = {k_}/{2 * k_ // d_}."], tags=["modeling"])
B.sel(8, "cp1", "y varies inversely with x and y = 6 when x = 4. Select ALL true statements.", ["k = 24", "y = 3 when x = 8", "y = 12 when x = 2", "xy is constant"], ["y = 6/4·x", "y = 10 when x = 0", "k = 1.5"], ["k = 24.", "24/8 = 3, 24/2 = 12.", "x = 0 is not allowed."])
B.mc(8, "cp1", "A team mixes 20% and 50% solutions to get 12 L of 30% solution. How many liters of 50% solution?", "4 L", ["8 L", "6 L", "3 L"], ["0.2(12 - x) + 0.5x = 3.6 → 0.3x = 1.2."], tags=["modeling"])
B.mc(8, "honors", "A plane flies 600 mi with the wind and 480 mi against it in the same time. Its airspeed is 270 mph. What is the wind speed?", "30 mph", ["40 mph", "20 mph", "60 mph"], ["600/(270 + w) = 480/(270 - w).", "600(270 - w) = 480(270 + w) → 1080w = 32400."], tags=["modeling", "challenge"])
assert same(600 / 300, 480 / 240)
B.sa(8, "cp1", "Average cost: C(x) = (2000 + 15x)/x. How many items make the average cost $25?", "200 items", ["2000 + 15x = 25x → x = 200."], tags=["modeling"])
B.orq(8, "honors", "Pipe A fills a pool in 10 h; drain B empties it in 15 h.", [("Write each rate (A positive, B negative).", "1/10 and -1/15"), ("Find the net rate with both open.", "1/30 pool per hour"), ("How long to fill with both open?", "30 hours"), ("What if B could empty it in 10 h?", "Never fills (net rate 0)")],
      ["Rate = 1/time.", "1/10 - 1/15.", "Reciprocal.", "1/10 - 1/10 = 0."], tags=["modeling"])
B.sa(8, "cp2", "z varies jointly with x and y; z = 24 when x = 2 and y = 3. Find k.", "k = 4", ["k = z/(xy) = 24/6."])

B.sel(2, "honors", "Select ALL true statements about (x² - 9)/(x + 1) ÷ (x - 3)/(x + 1).", ["It simplifies to x + 3", "x = -1 is excluded", "x = 3 is excluded"], ["x = -3 is excluded", "It simplifies to (x + 3)/(x + 1)²"],
      ["(x - 3)(x + 3)/(x + 1) · (x + 1)/(x - 3) = x + 3.", "Exclude zeros of both denominators AND of the divisor's numerator (x = 3)."], tags=["misconception"])
B.sel(3, "cp1", "Select ALL expressions whose LCD is x(x + 2).", ["1/x + 1/(x + 2)", "3/(x² + 2x) - 1/x", "x/(x + 2) + 5/x"], ["1/x² + 1/(x + 2)", "2/(x - 2) + 1/x"], ["The LCD uses each distinct factor to its highest power."])
B.mc(4, "cp1", "Which value is NOT a possible solution of 3/(x - 4) + 1/x = 2 before checking?", "4", ["1", "-2", "6"], ["x = 4 and x = 0 make denominators 0, so they can never be solutions."], tags=["reasoning"])
B.sel(5, "cp1", "Select ALL values that can never be solutions of 5/(x + 3) - 2/(x - 1) = 1/x.", ["-3", "1", "0"], ["3", "-1", "5"], ["Excluded values: zeros of every denominator."], tags=["reasoning"])
B.mc(5, "cp2", "Which value is excluded from the domain of x/(x + 9)?", "-9", ["9", "0", "1"], ["x + 9 = 0."])
B.sel(6, "honors", "f(x) = (x² - x - 2)/(x² - 4). Select ALL true statements.", ["f has a hole at x = 2", "f has a vertical asymptote x = -2", "f has a horizontal asymptote y = 1", "The hole is at (2, 3/4)"], ["f has a vertical asymptote x = 2", "The hole is at (2, 0)"],
      ["(x - 2)(x + 1)/((x - 2)(x + 2)) = (x + 1)/(x + 2).", "Hole: (x + 1)/(x + 2) at x = 2 is 3/4.", "Equal degrees: 1/1."])
B.mc(6, "honors", "What is the slant asymptote of y = (2x² + 3x - 1)/(x + 1)?", "y = 2x + 1", ["y = 2x", "y = 2x + 3", "y = 2"], ["Divide: 2x² + 3x - 1 = (x + 1)(2x + 1) - 2."], tags=["challenge"])
assert P.coeffs(2, 3, -1).divmod(P.coeffs(1, 1)) == (P.coeffs(2, 1), P([-2]))
B.sa(6, "cp1", "Find the horizontal asymptote of y = (4x - 7)/(2x + 1).", "y = 2", ["Equal degrees: 4/2."])
B.mc(7, "cp1", "Which graph feature does the factor (x - 3) produce in y = (x - 3)/((x - 3)(x + 1))?", "A hole at x = 3", ["A vertical asymptote at x = 3", "An x-intercept at 3", "A horizontal asymptote y = 3"], ["Canceled factor → hole."], tags=["misconception"])
B.sa(7, "cp1", "Find the hole of y = (x² - 4)/(x - 2).", "(2, 4)", ["Simplifies to x + 2; at x = 2, y = 4."])
B.mc(8, "cp1", "y varies inversely with x. When x = 5, y = 8. Which is y when x = 10?", "4", ["16", "2", "13"], ["k = 40; 40/10."])
B.sa(8, "cp1", "A car travels 300 mi. Write the time t as a function of speed r and find t at 60 mph.", "t = 300/r; 5 h", ["Distance = rate × time."], tags=["modeling"])
B.sa(8, "honors", "Jen can paint a fence in 6 h. With Max she takes 4 h. How long would Max take alone?", "12 h", ["1/6 + 1/m = 1/4 → 1/m = 1/12."], tags=["modeling"])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
