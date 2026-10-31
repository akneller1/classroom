from lib import Bank, graph, clean
from mathlite import *
import random

STD = {1: ["A-APR.A.1"], 2: ["A-SSE.A.2", "A-APR.C.4"], 3: ["A-APR.D.6"], 4: ["A-APR.B.2"], 5: ["A-APR.B.3"],
       6: ["F-IF.C.7c"], 7: ["N-CN.C.9", "N-CN.C.8"], 8: ["A-CED.A.1", "A-APR.B.3"]}
B = Bank("polynomial-functions", "pf", STD)
R = random.Random(404)
ps = pstr

# ---------------- Skill 1: polynomial operations ----------------
S = 1
for a, b in [((3, -2, 5), (1, 4, -7)), ((2, 0, -1, 6), (-5, 3, 0, 2)), ((-4, 1, 9), (4, -6, -9)), ((1, -1, 1, -1), (2, 2, 0, 3))]:
    A, Bp = P.coeffs(*a), P.coeffs(*b)
    B.sa(S, "cp2", f"Add: ({A}) + ({Bp}).", ps(A + Bp), ["Group like terms (same exponent).", f"Combine coefficients: {A + Bp}."])
    B.sa(S, "cp2", f"Subtract: ({A}) - ({Bp}).", ps(A - Bp), ["Distribute the negative to every term of the second polynomial.", f"Combine like terms: {A - Bp}."])
for a, b, lvl in [((2, -3), (1, 5), "cp2"), ((3, 1), (2, -1, 4), "cp1"), ((1, -2), (1, 2, 4), "cp1"), ((2, 1, -1), (1, -3, 2), "cp1"), ((-1, 0, 2), (3, 1, -5), "honors")]:
    A, Bp = P.coeffs(*a), P.coeffs(*b)
    B.sa(S, lvl, f"Multiply and write in standard form: ({A})({Bp}).", ps(A * Bp),
         ["Multiply every term of the first factor by every term of the second.", f"Combine like terms: {A * Bp}."])
for poly, deg, name in [(P.coeffs(4, 0, -1, 7), 3, "cubic"), (P.coeffs(-2, 5), 1, "linear"), (P.coeffs(1, 0, 0, 0, -3), 4, "quartic"), (P.coeffs(6, -1, 0), 2, "quadratic")]:
    nterms = sum(1 for c in poly.c if c != 0); tn = {1: "monomial", 2: "binomial", 3: "trinomial"}[nterms]
    names = {1: "linear", 2: "quadratic", 3: "cubic", 4: "quartic", 5: "quintic"}
    other_t = "trinomial" if tn != "trinomial" else "binomial"
    B.mc(S, "cp2", f"Classify {poly} by degree and number of terms.", f"{name} {tn}",
         [f"{names[deg + 1]} {tn}", f"{name} {other_t}", f"{names.get(nterms, 'quintic')} {tn}" if nterms != deg else f"{names[max(1, deg - 1)]} {other_t}"],
         [f"Degree = highest exponent = {deg} → {name}.", f"{nterms} nonzero terms → {tn}."])
B.sa(S, "cp1", "Expand (x + 2)³.", ps(P.coeffs(1, 2) ** 3), ["(x + 2)² = x² + 4x + 4.", "Multiply by (x + 2) and combine: x³ + 6x² + 12x + 8."])
B.sa(S, "cp1", "Expand (2x - 1)³.", ps(P.coeffs(2, -1) ** 3), ["(2x - 1)² = 4x² - 4x + 1.", "Multiply by (2x - 1): 8x³ - 12x² + 6x - 1."])
B.mc(S, "cp1", "A student writes (x + 3)² = x² + 9. What is the correct expansion?", "x² + 6x + 9", ["x² + 9", "x² + 3x + 9", "2x + 6"],
     ["(x + 3)² = (x + 3)(x + 3).", "The middle term 2·3·x = 6x is missing from the student's answer."], tags=["error-analysis", "misconception"])
B.sel(S, "cp1", "Select ALL expressions that are polynomials.", ["3x⁴ - x + 2", "x²/5 + 1", "√7·x³ - x", "-8"],
      ["2/x + x", "x^(1/2) + 4", "3x⁻² + 1"],
      ["A polynomial has only whole-number exponents on the variable; coefficients may be any real numbers.", "2/x = 2x⁻¹, x^(1/2) and x⁻² are not allowed."], tags=["reasoning"])
B.sel(S, "cp1", "Let f(x) = 2x³ - 5x + 1 and g(x) = -2x³ + x² + 4. Select ALL true statements.", ["f + g has degree 2", "f - g has degree 3", "f·g has degree 6", "The constant term of f + g is 5"],
      ["f + g has degree 3", "f·g has degree 9"],
      ["f + g = x² - 5x + 5: the x³ terms cancel.", "f - g = 4x³ - x² - 5x - 3.", "Degrees add under multiplication: 3 + 3 = 6."], tags=["reasoning"])
B.mc(S, "cp1", "If f has degree 4 and g has degree 3, what is the degree of f·g?", "7", ["12", "4", "1"], ["Leading terms multiply: x⁴·x³ = x⁷."])
B.sa(S, "cp1", "Find the area of a rectangle with length 2x + 5 and width x - 3 as a polynomial.", ps(P.coeffs(2, 5) * P.coeffs(1, -3)), ["A = (2x + 5)(x - 3).", "= 2x² - 6x + 5x - 15 = 2x² - x - 15."], tags=["modeling"])
B.sa(S, "honors", "Find k so that (x² + kx + 3)(x - 2) has no x² term.", "k = 2", ["x² coefficient: -2 + k.", "-2 + k = 0 → k = 2."], tags=["reasoning"])
assert (P.coeffs(1, 2, 3) * P.coeffs(1, -2)).c[2] == 0
B.sa(S, "honors", "Expand (x + 1)(x - 1)(x² + 1)(x⁴ + 1).", "x⁸ - 1", ["(x + 1)(x - 1) = x² - 1.", "(x² - 1)(x² + 1) = x⁴ - 1; (x⁴ - 1)(x⁴ + 1) = x⁸ - 1."], tags=["challenge"])
assert P.roots([1, -1]) * P.coeffs(1, 0, 1) * P.coeffs(1, 0, 0, 0, 1) == P.coeffs(1, 0, 0, 0, 0, 0, 0, 0, -1)
B.sa(S, "honors", "Expand (x + y)³ and use it to find the coefficient of x²y.", "x³ + 3x²y + 3xy² + y³; coefficient 3", ["(x + y)² = x² + 2xy + y².", "Multiply by (x + y): x³ + 3x²y + 3xy² + y³."], tags=["connections"])
B.mc(S, "honors", "Polynomials are closed under which operations?", "Addition, subtraction, and multiplication", ["All four operations", "Addition only", "Addition and division"],
     ["Sum, difference, and product of polynomials are polynomials.", "A quotient such as 1/x is not."], tags=["reasoning"])
B.orq(S, "honors", "A box has dimensions x, x + 2, and 10 - 2x (inches).",
      [("Write the volume V(x) in standard form.", "V(x) = -2x³ + 6x² + 20x"), ("State the degree and leading coefficient.", "degree 3; leading coefficient -2"),
       ("Find V(3).", "60 in³"), ("What values of x make physical sense?", "0 < x < 5")],
      ["x(x + 2)(10 - 2x) = (x² + 2x)(10 - 2x) = -2x³ + 6x² + 20x.", "Highest power 3.", "V(3) = 3·5·4 = 60.", "All three dimensions must be positive: x > 0 and 10 - 2x > 0."], tags=["modeling"])
assert ps(P.coeffs(1, 0) * P.coeffs(1, 2) * P.coeffs(-2, 10)) == "-2x³ + 6x² + 20x"
B.orq(S, "cp1", "Let f(x) = x² - 3x + 2 and g(x) = x - 4.",
      [("Find f(x) + g(x).", "x² - 2x - 2"), ("Find f(x) - g(x).", "x² - 4x + 6"), ("Find f(x)·g(x).", ps(P.coeffs(1, -3, 2) * P.coeffs(1, -4))), ("Find (f·g)(1).", "0")],
      ["Combine like terms.", "Distribute the negative: -x + 4.", "Distribute and combine.", "f(1) = 0, so the product is 0."])

# ---------------- Skill 2: special products and factoring ----------------
S = 2
for a, b in [(1, 3), (2, 1), (1, 5), (3, 2), (4, 1)]:
    e = P([b ** 3, 0, 0, a ** 3]); ax = "x" if a == 1 else f"{a}x"
    B.sa(S, "cp1" if a == 1 else "honors" if a > 2 else "cp1", f"Factor the sum of cubes {e}.", f"({ax} + {b})({a*a if a > 1 else ''}x² - {a*b}x + {b*b})".replace("- 1x", "- x"),
         ["a³ + b³ = (a + b)(a² - ab + b²).", f"Here a = {ax}, b = {b}."])
    e2 = P([-b ** 3, 0, 0, a ** 3])
    B.sa(S, "cp1", f"Factor the difference of cubes {e2}.", f"({ax} - {b})({a*a if a > 1 else ''}x² + {a*b}x + {b*b})".replace("+ 1x", "+ x"),
         ["a³ - b³ = (a - b)(a² + ab + b²).", f"Here a = {ax}, b = {b}."])
    assert eqcheck(str(e2), f"({ax} - {b})({a*a}x^2 + {a*b}x + {b*b})")
for pol in [P.roots([3, -3]), P.roots([F(5, 2), F(-5, 2)], 4), P.roots([1, 1, -2, -2], 1) // P.roots([1, -2]) * 1]:
    pass
for desc in [(1, 0, -64), (9, 0, -49), (1, -10, 25), (4, 12, 9), (16, 0, -1)]:
    p = P.coeffs(*desc)
    B.mc(S, "cp2", f"Factor {p}.", factor_str(p), [factor_str(P.coeffs(desc[0], abs(desc[1]) + 1, desc[2])) if False else f"({ 'x' if desc[0]==1 else str(int(desc[0]**0.5))+'x'} - {int(abs(desc[2])**0.5)})²",
                                                   f"({'x' if desc[0]==1 else str(int(desc[0]**0.5))+'x'} + {int(abs(desc[2])**0.5)})²", f"({'x' if desc[0]==1 else str(int(desc[0]**0.5))+'x'} - {int(abs(desc[2])**0.5)})({'x' if desc[0]==1 else str(int(desc[0]**0.5))+'x'} + {abs(desc[2])})"],
         ["Check for a perfect-square trinomial a² ± 2ab + b² or a difference of squares a² - b².", f"{factor_str(p)}."])
for desc in [(1, 3, -4, -12), (2, -1, -18, 9), (1, -5, -1, 5), (3, 2, -12, -8), (1, 4, -9, -36)]:
    p = P.coeffs(*desc)
    B.sa(S, "cp1", f"Factor by grouping: {p}.", factor_str(p),
         ["Group the first two and last two terms; factor the GCF from each group.", "Factor out the common binomial, then factor any remaining difference of squares.", f"{factor_str(p)}."])
for desc in [(1, 0, -13, 0, 36), (1, 0, -5, 0, 4), (1, 0, 3, 0, -4), (2, 0, -10, 0, 8), (1, 0, -17, 0, 16)]:
    p = P.coeffs(*desc)
    B.sa(S, "honors", f"Factor completely over the integers: {p}.", factor_str(p),
         ["The expression is quadratic in form: let u = x².", "Factor the quadratic in u, then substitute back and factor any difference of squares.", f"{factor_str(p)}."], tags=["challenge"])
for desc in [(2, 0, -32, 0), (3, -3, -6, 0), (5, 0, 0, -40)]:
    p = P.coeffs(*desc)
    B.sa(S, "cp1", f"Factor completely: {p}.", factor_str(p), ["Factor out the GCF first.", "Factor the remaining polynomial using a special pattern.", f"{factor_str(p)}."])
B.mc(S, "cp1", "A student factors x³ - 27 as (x - 3)(x² - 3x + 9). What is the error?", "The middle sign should be +: (x - 3)(x² + 3x + 9)",
     ["No error", "It should be (x - 3)³", "It should be (x + 3)(x² - 3x + 9)"], ["a³ - b³ = (a - b)(a² + ab + b²).", "Check: (x - 3)(x² + 3x + 9) = x³ - 27."], tags=["error-analysis"])
B.mc(S, "cp1", "A student writes x³ + 8 = (x + 2)³. Which shows the error?", "(x + 2)³ = x³ + 6x² + 12x + 8, not x³ + 8", ["(x + 2)³ = x³ + 2", "The student is correct", "x³ + 8 cannot be factored"],
     ["Expanding (x + 2)³ produces middle terms.", "Correct: x³ + 8 = (x + 2)(x² - 2x + 4)."], tags=["error-analysis", "misconception"])
B.sel(S, "cp1", "Select ALL expressions that are factors of x⁴ - 81.", ["x - 3", "x + 3", "x² + 9"], ["x² - 3", "x - 9", "x² + 3x + 9"],
      ["x⁴ - 81 = (x² - 9)(x² + 9) = (x - 3)(x + 3)(x² + 9).", "x² + 9 is prime over the reals."])
B.sel(S, "honors", "Select ALL polynomials that have (x - 2) as a factor.", ["x³ - 8", "x² - 4", "x³ - 2x² + x - 2", "x⁴ - 16"], ["x³ + 8", "x² + 4", "x³ - 2x + 2"],
      ["(x - 2) is a factor exactly when the polynomial is 0 at x = 2.", "8 - 8 = 0; 4 - 4 = 0; 8 - 8 + 2 - 2 = 0; 16 - 16 = 0. The others give 16, 8, 6."], tags=["connections"])
for e in ["x³ - 8", "x² - 4", "x³ - 2x² + x - 2", "x⁴ - 16"]: assert abs(peval(e, x=2)) < 1e-12
B.sa(S, "honors", "Factor 8x³ + 27y³.", "(2x + 3y)(4x² - 6xy + 9y²)", ["8x³ = (2x)³ and 27y³ = (3y)³.", "Sum of cubes: (2x + 3y)((2x)² - (2x)(3y) + (3y)²)."])
B.sa(S, "honors", "Factor x⁶ - 64 completely over the integers.", "(x - 2)(x + 2)(x² + 2x + 4)(x² - 2x + 4)",
     ["Difference of squares first: (x³ - 8)(x³ + 8).", "Then difference and sum of cubes."], tags=["challenge"])
assert eqcheck("x^6 - 64", "(x - 2)(x + 2)(x^2 + 2x + 4)(x^2 - 2x + 4)")
B.sa(S, "honors", "Use the identity (a + b)(a² - ab + b²) = a³ + b³ to compute 11³ + 9³ without a calculator.", "2060", ["a + b = 20, a² - ab + b² = 121 - 99 + 81 = 103.", "20·103 = 2060."], tags=["connections"])
assert 11 ** 3 + 9 ** 3 == 2060
B.orq(S, "honors", "Prove the identity (x² + y²)² = (x² - y²)² + (2xy)² and use it.",
      [("Expand the left side.", "x⁴ + 2x²y² + y⁴"), ("Expand the right side.", "x⁴ - 2x²y² + y⁴ + 4x²y² = x⁴ + 2x²y² + y⁴"),
       ("Use x = 2, y = 1 to produce a Pythagorean triple.", "3, 4, 5"), ("Use x = 3, y = 2 to produce another.", "5, 12, 13")],
      ["Square the binomial.", "Both sides simplify to the same polynomial.", "x² - y² = 3, 2xy = 4, x² + y² = 5.", "x² - y² = 5, 2xy = 12, x² + y² = 13."], tags=["connections", "reasoning"])
B.orq(S, "cp1", "Use the polynomial 2x³ + 6x² - 8x - 24.",
      [("Factor out the GCF.", "2(x³ + 3x² - 4x - 12)"), ("Group the remaining terms.", "2[x²(x + 3) - 4(x + 3)]"), ("Factor completely.", factor_str(P.coeffs(2, 6, -8, -24))), ("List its zeros.", "x = -3, -2, 2")],
      ["GCF 2.", "Pairs: x³ + 3x² and -4x - 12.", "(x + 3)(x² - 4) = (x + 3)(x - 2)(x + 2).", "Set each factor to 0."])

# ---------------- Skill 3: long and synthetic division ----------------
S = 3
for num_, r, lvl in [((1, -4, 1, 6), 2, "cp2"), ((2, 3, -5, 4), -1, "cp1"), ((1, 0, -7, 6), 3, "cp2"), ((3, -10, 0, 8), 1, "cp1"), ((1, 2, -5, -6, 4), -2, "cp1"), ((2, 0, 0, -1), F(1, 2), "honors")]:
    N = P.coeffs(*num_); q, rem = N.divmod(P([-F(r), 1]))
    ans = ps(q) + ("" if rem.c[0] == 0 else f" + {fr(rem.c[0])}/({lin_factor(r)[1:-1]})" if rem.c[0] > 0 else f" - {fr(-rem.c[0])}/({lin_factor(r)[1:-1]})")
    B.sa(S, lvl, f"Use synthetic division to divide {N} by {lin_factor(r)[1:-1]}.", ans,
         [f"Write the coefficients {', '.join(fr(c) for c in N.desc())} and use {fr(r)}.", f"Bottom row: {', '.join(fr(c) for c in N.synth(F(r)))}.", f"Quotient {q}, remainder {fr(rem.c[0])}."])
for num_, den, lvl in [((1, 3, -2, 5), (1, 0, 1), "honors"), ((2, -3, 4, -1), (1, -1, 2), "honors"), ((6, 1, -5), (2, 1), "cp1"), ((4, 0, -9, 3), (2, -3), "cp1"), ((1, 0, 0, 0, -16), (1, 0, 4), "cp1")]:
    N, D = P.coeffs(*num_), P.coeffs(*den); q, rem = N.divmod(D)
    ans = ps(q) + ("" if rem == P([0]) else f" + ({rem})/({D})")
    B.sa(S, lvl, f"Use long division to divide {N} by {D}.", ans,
         ["Divide leading terms, multiply, subtract, bring down; repeat.", f"Quotient {q}; remainder {rem}.", f"Answer: {ans}."])
    assert N == q * D + rem
B.mc(S, "cp1", "To divide x³ - 5x + 2 by x - 3 with synthetic division, which row of coefficients should you use?", "1, 0, -5, 2",
     ["1, -5, 2", "1, 0, -5, 2, -3", "1, -3, -5, 2"], ["Include a 0 placeholder for the missing x² term."], tags=["misconception"])
B.mc(S, "cp1", "Which number do you use in synthetic division when dividing by x + 4?", "-4", ["4", "1/4", "-1/4"], ["x + 4 = x - (-4)."], tags=["misconception"])
B.mc(S, "cp1", "The synthetic-division bottom row for dividing a cubic by x - 2 is 3, -1, 4, 0. What is the quotient?", "3x² - x + 4", ["3x³ - x² + 4x", "3x² - x + 4 with remainder 2", "3x - 1 + 4"],
     ["The last number (0) is the remainder.", "The others are the coefficients of a quotient one degree lower."])
B.sel(S, "cp1", "When f(x) = x³ + 2x² - 5x - 6 is divided by x + 1, select ALL true statements.", ["The remainder is 0", "The quotient is x² + x - 6", "x + 1 is a factor of f(x)"],
      ["The remainder is -2", "The quotient is x² + 3x - 2"], ["Bottom row: 1, 1, -6, 0.", "Remainder 0 means x + 1 is a factor."])
assert P.coeffs(1, 2, -5, -6).divmod(P.coeffs(1, 1)) == (P.coeffs(1, 1, -6), P([0]))
B.mc(S, "honors", "A student divides 2x³ - 7x² + 5 by x - 3 and gets 2x² - x - 3 remainder -4. Is the student right?", "Yes: (x - 3)(2x² - x - 3) - 4 = 2x³ - 7x² + 5",
     ["No: the remainder should be 4", "No: the quotient should be 2x² - 13x + 39", "No: you cannot divide when a term is missing"], ["Check by multiplying back: 2x³ - x² - 3x - 6x² + 3x + 9 - 4."], tags=["error-analysis"])
assert P.coeffs(2, -7, 0, 5).divmod(P.coeffs(1, -3)) == (P.coeffs(2, -1, -3), P([-4]))
B.mc(S, "honors", "A student divides 2x³ + x² - 8x + 3 by 2x - 1 using synthetic division with 1/2 and gets bottom row 2, 2, -7, -1/2. What is the actual quotient?", "x² + x - 7/2, remainder -1/2",
     ["2x² + 2x - 7, remainder -1/2", "2x² + 2x - 7, remainder -1", "x² + x - 7/2, remainder -1/4"],
     ["Dividing by x - 1/2 gives 2x² + 2x - 7.", "Since 2x - 1 = 2(x - 1/2), divide that quotient by 2; the remainder stays -1/2."], tags=["error-analysis", "challenge"])
q, rr = P.coeffs(2, 1, -8, 3).divmod(P.coeffs(2, -1)); assert q == P.coeffs(1, 1, F(-7, 2)) and rr == P([F(-1, 2)])
B.sa(S, "honors", "When x³ + ax² - 4x + 4 is divided by x - 2, the remainder is 8. Find a.", "a = 1", ["Remainder = f(2) = 8 + 4a - 8 + 4 = 4a + 4.", "4a + 4 = 8 → a = 1."], tags=["connections"])
B.sa(S, "honors", "The volume of a box is x³ + 7x² + 14x + 8 and its height is x + 1. Find the area of its base.", ps(P.coeffs(1, 7, 14, 8) // P.coeffs(1, 1)),
     ["Base area = volume ÷ height.", "Synthetic division with -1: 1, 6, 8, 0 → x² + 6x + 8."], tags=["modeling"])
B.orq(S, "cp1", "Divide f(x) = x³ - 2x² - 13x - 10 by x + 2.",
      [("Write the synthetic-division row.", "1, -4, -5, 0"), ("State the quotient.", "x² - 4x - 5"), ("State the remainder.", "0"), ("Factor f(x) completely.", factor_str(P.coeffs(1, -2, -13, -10)))],
      ["Use -2 with coefficients 1, -2, -13, -10.", "Bottom row gives x² - 4x - 5.", "Last entry 0.", "x² - 4x - 5 = (x - 5)(x + 1)."])
assert P.coeffs(1, -2, -13, -10).synth(-2) == [1, -4, -5, 0]
B.orq(S, "honors", "Compare long division and synthetic division for (3x⁴ - 2x² + x - 5) ÷ (x - 1).",
      [("Write the dividend with all placeholder terms.", "3x⁴ + 0x³ - 2x² + x - 5"), ("Find the quotient.", ps(P.coeffs(3, 0, -2, 1, -5) // P.coeffs(1, -1))),
       ("Find the remainder.", fr((P.coeffs(3, 0, -2, 1, -5) % P.coeffs(1, -1)).c[0])), ("Why can't synthetic division be used directly for divisor x² - 1?", "Synthetic division only works for linear divisors x - c")],
      ["Missing x³ term gets 0.", "Bottom row 3, 3, 1, 2, -3.", "f(1) = 3 - 2 + 1 - 5 = -3.", "x² - 1 is quadratic; use long division (or divide by x - 1 then x + 1)."], tags=["reasoning"])
B.orq(S, "honors", "f(x) = 2x³ + 3x² - 11x - 6.",
      [("Show that x - 2 is a factor using synthetic division.", "Bottom row 2, 7, 3, 0: remainder 0"), ("Write the quotient.", "2x² + 7x + 3"),
       ("Factor f completely.", factor_str(P.coeffs(2, 3, -11, -6))), ("Solve f(x) = 0.", "x = -3, -1/2, 2")],
      ["2 | 2 3 -11 -6 → 2, 7, 3, 0.", "Quotient from the bottom row.", "2x² + 7x + 3 = (2x + 1)(x + 3).", "Zero-product property."])
assert P.coeffs(2, 3, -11, -6).synth(2) == [2, 7, 3, 0]
B.sa(S, "cp2", "Divide (6x³ - 9x² + 12x) by 3x.", "2x² - 3x + 4", ["Divide each term by 3x."])
B.sa(S, "cp2", "Divide (8x⁴ + 4x³ - 2x²) by 2x².", "4x² + 2x - 1", ["Divide each term by 2x²."])

# ---------------- Skill 4: remainder and factor theorems ----------------
S = 4
for desc, c, lvl in [((1, -3, 0, 5), 2, "cp2"), ((2, 1, -4, 7), -1, "cp2"), ((1, 0, -6, 2, 1), 3, "cp1"), ((3, -5, 2), -2, "cp2"), ((1, 1, 1, 1, 1), -2, "cp1"), ((4, 0, -3, 1), F(1, 2), "honors")]:
    f = P.coeffs(*desc); v = f(F(c))
    B.sa(S, lvl, f"Use the Remainder Theorem to find the remainder when f(x) = {f} is divided by {lin_factor(c)[1:-1]}.", fr(v),
         [f"The remainder equals f({fr(c)}).", f"f({fr(c)}) = {fr(v)}."])
for desc, c in [((1, -6, 11, -6), 3), ((1, 2, -5, -6), 4), ((2, -3, -3, 2), -1), ((1, 0, -7, 6), -3), ((1, 4, 1, -6), 2)]:
    f = P.coeffs(*desc); v = f(c); isf = v == 0
    B.mc(S, "cp1", f"Is {lin_factor(c)[1:-1]} a factor of f(x) = {f}?", f"{'Yes' if isf else 'No'}, because f({c}) = {fr(v)}",
         [f"{'No' if isf else 'Yes'}, because f({c}) = {fr(v)}", f"{'Yes' if not isf else 'No'}, because f({-c}) = {fr(f(-c))}", f"Yes, because the constant term is divisible by {abs(c)}"],
         [f"By the Factor Theorem, x - c is a factor exactly when f(c) = 0.", f"f({c}) = {fr(v)}."])
for desc, kr in [((1, "k", -4, 12), 3), ((2, -1, "k", 6), -2), ((1, -2, "k", 8), 2), (("k", 3, -2, -4), 1)]:
    # solve for k so that (x - kr) is a factor
    terms = list(desc); deg = len(terms) - 1
    base = sum((F(cf) * F(kr) ** (deg - i)) for i, cf in enumerate(terms) if cf != "k")
    kco = sum(F(kr) ** (deg - i) for i, cf in enumerate(terms) if cf == "k"); k = -base / kco
    shown = " + ".join(("k" if cf == "k" else str(cf)) + ("" if deg - i == 0 else ("x" + (sup(deg - i) if deg - i > 1 else ""))) for i, cf in enumerate(terms))
    shown = shown.replace("+ -", "- ").replace("kx", "kx").replace("1x³", "x³").replace(" 1x", " x")
    if shown.startswith("1x"): shown = shown[1:]
    B.sa(S, "honors" if desc[0] == "k" else "cp1", f"Find k so that {lin_factor(kr)[1:-1]} is a factor of {shown}.", f"k = {fr(k)}",
         [f"Factor Theorem: the polynomial must equal 0 at x = {kr}.", f"Substitute and solve the linear equation in k: k = {fr(k)}."], tags=["reasoning"])
    full = P([F(k) if cf == "k" else F(cf) for cf in reversed(terms)]); assert full(F(kr)) == 0
B.sel(S, "cp1", "f(1) = 0, f(-2) = 5, and f(3) = 0 for a polynomial f. Select ALL statements that must be true.", ["x - 1 is a factor of f(x)", "x - 3 is a factor of f(x)", "Dividing f(x) by x + 2 leaves remainder 5"],
      ["x + 1 is a factor of f(x)", "x + 2 is a factor of f(x)", "f has exactly two zeros"],
      ["Factor Theorem: f(c) = 0 ⇔ (x - c) is a factor.", "Remainder Theorem: f(-2) = remainder on division by x + 2.", "f could have more zeros we don't know about."], tags=["reasoning"])
B.sel(S, "cp1", "Select ALL factors of f(x) = x³ - 7x - 6.", ["x + 1", "x + 2", "x - 3"], ["x - 1", "x - 2", "x + 3"],
      ["Test values: f(-1) = 0, f(-2) = 0, f(3) = 0.", "f(1) = -12, f(2) = -12, f(-3) = -12."])
assert P.coeffs(1, 0, -7, -6).rational_roots()[0] == [-2, -1, 3]
B.mc(S, "cp1", "When p(x) is divided by x - 4, the quotient is x² + 1 and the remainder is 3. What is p(4)?", "3", ["0", "17", "4"], ["p(x) = (x - 4)(x² + 1) + 3.", "p(4) = 0 + 3."])
B.mc(S, "honors", "A student says: 'Since f(2) = 6, x - 6 is a factor.' What is the correct conclusion?", "Dividing by x - 2 leaves remainder 6; x - 2 is not a factor", ["x - 6 is a factor", "x + 2 is a factor", "f(6) = 2"],
     ["f(c) is the remainder when dividing by x - c.", "A nonzero remainder means x - 2 is not a factor."], tags=["error-analysis", "misconception"])
B.sa(S, "honors", "f(x) = x³ + ax² + bx - 6 has factors x - 1 and x + 2. Find a and b.", "a = 2, b = 3",
     ["f(1) = 1 + a + b - 6 = 0 → a + b = 5.", "f(-2) = -8 + 4a - 2b - 6 = 0 → 2a - b = 7.", "Solve: a = 4, b = 1?"], tags=["challenge"])
# fix with computed solution
import itertools
sol = [(a_, b_) for a_ in range(-20, 21) for b_ in range(-20, 21) if 1 + a_ + b_ - 6 == 0 and -8 + 4 * a_ - 2 * b_ - 6 == 0]
assert sol == [(4, 1)]
B.qs[-1]["answer"] = "a = 4, b = 1"; B.qs[-1]["solutionSteps"] = ["f(1) = 1 + a + b - 6 = 0 → a + b = 5.", "f(-2) = -8 + 4a - 2b - 6 = 0 → 2a - b = 7.", "Add: 3a = 12 → a = 4, b = 1."]
B.sa(S, "honors", "When f(x) is divided by x - 1 the remainder is 4, and when divided by x + 3 the remainder is -8. Find the remainder when f(x) is divided by (x - 1)(x + 3).", "3x + 1",
     ["The remainder has the form ax + b.", "a + b = 4 and -3a + b = -8.", "a = 3, b = 1."], tags=["challenge"])
B.orq(S, "cp1", "Let f(x) = x³ - 4x² + x + 6.",
      [("Evaluate f(-1).", "0"), ("What does that tell you?", "x + 1 is a factor"), ("Find the other factor by division.", "x² - 5x + 6"), ("List all zeros.", "x = -1, 2, 3")],
      ["-1 - 4 - 1 + 6 = 0.", "Factor Theorem.", "Synthetic division: 1, -5, 6, 0.", "(x + 1)(x - 2)(x - 3)."])
assert P.coeffs(1, -4, 1, 6).rational_roots()[0] == [-1, 2, 3]
B.orq(S, "honors", "Use p(x) = 2x⁴ - x³ - 8x² + x + 6.",
      [("Find p(1) and p(-1).", "p(1) = 0, p(-1) = 0"), ("Divide p by (x - 1)(x + 1) = x² - 1.", "2x² - x - 6"),
       ("Factor p completely.", factor_str(P.coeffs(2, -1, -8, 1, 6))), ("Find the remainder when p is divided by x - 3.", fr(P.coeffs(2, -1, -8, 1, 6)(3)))],
      ["Substitute.", "Long division (remainder 0).", "2x² - x - 6 = (2x + 3)(x - 2).", "Remainder Theorem: p(3)."], tags=["multistep"])
assert P.coeffs(2, -1, -8, 1, 6) % P.coeffs(1, 0, -1) == P([0])
B.sa(S, "cp2", "If f(5) = 0, name one factor of f(x).", "x - 5", ["Factor Theorem: f(c) = 0 means x - c is a factor."])
B.mc(S, "cp2", "The remainder when f(x) is divided by x + 3 equals which value?", "f(-3)", ["f(3)", "f(0)", "-3"], ["x + 3 = x - (-3), so the remainder is f(-3)."])

# ---------------- Skill 5: zeros and multiplicities ----------------
S = 5
for rs, a in [([2, 2, -1], 1), ([0, 0, 3], 1), ([-2, -2, -2, 1], 1), ([1, 4, 4], 2), ([F(1, 2), -3, -3], 2), ([0, 5, 5, 5], -1)]:
    f = P.roots(rs, a); from collections import Counter; cnt = Counter(rs)
    desc = "; ".join(f"{fr(r)} (multiplicity {m})" for r, m in sorted(cnt.items()))
    B.sa(S, "cp1" if len(cnt) > 1 else "cp2", f"List each zero of f(x) = {factor_str(f)} and its multiplicity.", desc,
         ["Set each factor equal to 0.", "The exponent on a factor is the multiplicity.", desc + "."])
    beh = "; ".join(f"x = {fr(r)}: {'crosses' if m % 2 else 'touches and turns'}" for r, m in sorted(cnt.items()))
    B.sa(S, "cp1", f"For f(x) = {factor_str(f)}, does the graph cross or touch the x-axis at each zero?", beh,
         ["Odd multiplicity → the graph crosses.", "Even multiplicity → the graph touches and turns around.", beh + "."], tags=["graph"])
for rs, a in [([1, -2, 3], 1), ([0, 2, -2], 2), ([-1, -1, 4], 1), ([3, 3], -1)]:
    f = P.roots(rs, a); rts, _ = f.rational_roots(); assert sorted(rts) == sorted(map(F, rs))
    B.sa(S, "cp2" if len(rs) < 3 else "cp1", f"Find the zeros of f(x) = {f}.", ", ".join(fr(r) for r in sorted(set(rs))),
         ["Factor (GCF, grouping, or rational roots).", f"f(x) = {factor_str(f)}.", "Set each factor to 0."])
for desc in [(1, -2, -5, 6), (2, -3, -11, 6), (1, 0, -3, 2), (3, -4, -17, 6), (1, -1, -8, 12)]:
    f = P.coeffs(*desc); rts, rest = f.rational_roots(); assert rest.deg == 0
    cand = sorted({F(s * p_, q_) for p_ in divisors(desc[-1]) for q_ in divisors(desc[0]) for s in (1, -1)})
    B.sa(S, "honors" if desc[0] > 1 else "cp1", f"Use the Rational Root Theorem to find all zeros of f(x) = {f}.", ", ".join(fr(r) for r in sorted(set(rts))),
         [f"Possible rational zeros ±p/q: {', '.join(fr(c) for c in cand if c > 0)} (and negatives).", "Test candidates; use synthetic division after the first zero.", f"f(x) = {factor_str(f)}."])
B.mc(S, "cp1", "Which list gives all possible rational zeros of 2x³ + x - 3?", "±1, ±3, ±1/2, ±3/2", ["±1, ±3", "±1, ±2, ±3", "±1/3, ±2/3, ±1, ±2"],
     ["p divides the constant 3: ±1, ±3.", "q divides the leading coefficient 2: ±1, ±2.", "p/q: ±1, ±3, ±1/2, ±3/2."])
B.sel(S, "cp1", "f(x) = x²(x - 3)³(x + 1). Select ALL true statements.", ["The degree of f is 6", "The graph touches the x-axis at x = 0", "The graph crosses the x-axis at x = 3", "f has 3 distinct real zeros"],
      ["The graph touches at x = 3", "The graph touches at x = -1", "f has 6 distinct real zeros"],
      ["2 + 3 + 1 = 6.", "Multiplicity 2 at 0 (even → touch), 3 at 3 (odd → cross), 1 at -1 (cross).", "Distinct zeros: 0, 3, -1."], tags=["graph"])
B.sel(S, "honors", "Select ALL numbers that could NOT be zeros of 3x⁴ - 5x² + 2x - 4 by the Rational Root Theorem.", ["3", "1/2", "4/3 · 3", "2/5"], ["2/3", "-4", "1/3"],
      ["Possible zeros are ±(1, 2, 4)/(1, 3).", "3, 1/2, 2/5 and 4 → wait: 4/3·3 = 4 IS possible."], tags=["reasoning"])
# replace the above with a clean version (dedupe guard prevents re-adding same prompt; patch in place)
q = B.qs[-1]
q["options"] = [{"text": t, "correct": c} for t, c in [("3", True), ("1/2", True), ("2/5", True), ("3/4", True), ("2/3", False), ("-4", False), ("1/3", False)]]
q["answer"] = ["3", "1/2", "2/5", "3/4"]
q["solutionSteps"] = ["Possible rational zeros are ±p/q with p | 4 and q | 3: ±1, ±2, ±4, ±1/3, ±2/3, ±4/3.", "3, 1/2, 2/5 and 3/4 are not on the list, so they cannot be zeros.", "2/3, -4 and 1/3 are on the list (being on the list does not make them zeros)."]
B.mc(S, "honors", "A degree-5 polynomial has zeros 2 (multiplicity 2) and -1 (multiplicity 1). How many other zeros (counted with multiplicity) must it have?", "2", ["0", "3", "5"], ["Total multiplicity = degree = 5.", "5 - 3 = 2 more (real or complex)."], tags=["connections"])
B.sa(S, "honors", "Write a polynomial in standard form with leading coefficient 1, zero -2 of multiplicity 2, and zero 1 of multiplicity 1.", ps(P.roots([-2, -2, 1])),
     ["f(x) = (x + 2)²(x - 1).", "(x² + 4x + 4)(x - 1) = x³ + 3x² - 4."])
B.orq(S, "honors", "f(x) = x⁴ - 2x³ - 3x² + 4x + 4.",
      [("List the possible rational zeros.", "±1, ±2, ±4"), ("Show that -1 and 2 are zeros.", "f(-1) = 0, f(2) = 0"),
       ("Factor f completely.", factor_str(P.coeffs(1, -2, -3, 4, 4))), ("Describe the behavior of the graph at each zero.", "touches at x = -1 and at x = 2")],
      ["p | 4, q | 1.", "Substitute.", "Divide out (x + 1) and (x - 2) twice.", "Both multiplicities are 2 (even)."], tags=["graph", "multistep"])
assert factor_str(P.coeffs(1, -2, -3, 4, 4)) == "(x + 1)²(x - 2)²"
B.orq(S, "cp1", "g(x) = x³ + x² - 9x - 9.",
      [("Factor by grouping.", "(x + 1)(x² - 9)"), ("Factor completely.", "(x + 1)(x - 3)(x + 3)"), ("List the zeros.", "x = -3, -1, 3"), ("What is the y-intercept?", "-9")],
      ["x²(x + 1) - 9(x + 1).", "Difference of squares.", "Zero-product property.", "g(0) = -9."])
B.mc(S, "cp2", "What are the zeros of f(x) = (x - 4)(x + 7)?", "4 and -7", ["-4 and 7", "4 and 7", "-28"], ["x - 4 = 0 → x = 4; x + 7 = 0 → x = -7."], tags=["misconception"])

# ---------------- Skill 6: graphing polynomial functions ----------------
S = 6
for desc in [(2, 0, -1), (-1, 3, 0, 2), (3, 0, 0, 0, -5), (-4, 1, 1, 1, 1, 1), (1, 0, 0, 0, 0, 0, 7), (-2, 1, 0)]:
    f = P.coeffs(*desc); d, a = f.deg, f.lead
    L = "+∞" if (a > 0) == (d % 2 == 0) else "-∞"; Rr = "+∞" if a > 0 else "-∞"
    ans = f"As x → -∞, f(x) → {L}; as x → +∞, f(x) → {Rr}"
    wrong = [f"As x → -∞, f(x) → {Rr}; as x → +∞, f(x) → {L}" if L != Rr else f"As x → -∞, f(x) → {'-∞' if L == '+∞' else '+∞'}; as x → +∞, f(x) → {Rr}",
             f"As x → -∞, f(x) → {'-∞' if L == '+∞' else '+∞'}; as x → +∞, f(x) → {'-∞' if Rr == '+∞' else '+∞'}",
             f"As x → -∞, f(x) → {L}; as x → +∞, f(x) → {'-∞' if Rr == '+∞' else '+∞'}"]
    B.mc(S, "cp2" if d <= 3 else "cp1", f"Describe the end behavior of f(x) = {f}.", ans, wrong,
         [f"Degree {d} ({'even' if d % 2 == 0 else 'odd'}), leading coefficient {fr(a)} ({'positive' if a > 0 else 'negative'}).", ans + "."])
graphs = [([-2, 1, 3], 1), ([-1, -1, 2], 1), ([0, 0, 3], -1), ([-3, 0, 2], F(1, 2)), ([-2, -2, 2, 2], F(1, 4)), ([-1, 1, 3], -1)]
for rs, a in graphs:
    f = P.roots(rs, a); fx = lambda v, f=f: f(float(v))
    from collections import Counter; cnt = Counter(rs)
    ys = [f(F(k, 10)) for k in range(-50, 51)]
    dg = graph(B, "s06-poly-" + "_".join(str(r).replace("-", "m") for r in rs) + ("n" if a < 0 else ""), [(fx, {})], xr=(-5, 5), yr=(-10, 10), step=1,
               points=[(r, 0) for r in cnt] + [(0, float(f(0)), True, f"(0, {fr(f(0))})")],
               alt=f"Graph of a polynomial with x-intercepts at {', '.join(fr(r) for r in sorted(cnt))}, y-intercept {fr(f(0))}, " + ", ".join(f"{'crossing' if m % 2 else 'touching'} at {fr(r)}" for r, m in sorted(cnt.items())) + ".")
    good = factor_str(f)
    wr = [factor_str(P.roots([-r for r in rs], a)), factor_str(P.roots(rs, -a)), factor_str(P.roots(sorted(set(rs)), a)) if len(set(rs)) < len(rs) else factor_str(P.roots(rs + [rs[0]], a))]
    B.mc(S, "cp1" if a in (1, -1) else "honors", "Which function could match the graph?", f"f(x) = {good}", [f"f(x) = {w}" for w in wr],
         ["Read the x-intercepts and whether the graph crosses (odd multiplicity) or touches (even).", "Check end behavior and the y-intercept to fix the leading coefficient.", f"f(x) = {good}; f(0) = {fr(f(0))}."], diagram=dg, tags=["graph"])
    if len(B.qs) % 2 == 0:
        B.sel(S, "cp1", "Select ALL features shown by the graph.", [f"x-intercept at {fr(r)}" for r in sorted(cnt)][:2] + [f"y-intercept {fr(f(0))}"],
              [f"x-intercept at {fr(max(cnt) + 1)}", f"y-intercept {fr(f(0) + 2)}"],
              ["Read where the graph meets each axis."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "What is the maximum number of turning points of a degree-5 polynomial?", "4", ["5", "6", "2"], ["A degree-n polynomial has at most n - 1 turning points."])
B.mc(S, "cp1", "A polynomial graph has 3 turning points. What is the least possible degree?", "4", ["3", "2", "5"], ["Turning points ≤ n - 1, so n ≥ 4."])
B.sel(S, "cp1", "f(x) = -x³ + 4x. Select ALL true statements.", ["f is an odd function", "f rises to the left", "f has zeros at -2, 0, and 2", "f has at most 2 turning points"],
      ["f rises to the right", "f is an even function"], ["f(-x) = x³ - 4x = -f(x).", "Odd degree, negative lead: up on the left, down on the right.", "-x(x - 2)(x + 2).", "Degree 3 → ≤ 2 turning points."])
B.sel(S, "honors", "Which statements are true for EVERY polynomial of odd degree? Select ALL.", ["It has at least one real zero", "Its ends go in opposite directions", "Its range is all real numbers"],
      ["It has an odd number of turning points", "It is an odd function", "It has exactly one real zero"],
      ["Opposite end behavior forces at least one x-axis crossing (Intermediate Value Theorem).", "x³ - x has 2 turning points; x³ + 1 is not odd; x³ - x has three zeros."], tags=["reasoning"])
B.sa(S, "cp1", "Use the Intermediate Value Theorem: f(x) = x³ - 2x - 5 has f(2) = -1 and f(3) = 16. What can you conclude?", "f has a real zero between x = 2 and x = 3",
     ["Polynomials are continuous.", "f changes sign on [2, 3], so f(c) = 0 for some c between 2 and 3."], tags=["reasoning"])
assert P.coeffs(1, 0, -2, -5)(2) == -1 and P.coeffs(1, 0, -2, -5)(3) == 16
B.sa(S, "honors", "Between which two consecutive integers is the positive zero of f(x) = x³ + x - 5?", "1 and 2", ["f(1) = -3 < 0, f(2) = 5 > 0.", "f is increasing, so there is exactly one real zero."], tags=["reasoning"])
f6 = P.roots([-3, 1, 1], 1)
dg = graph(B, "s06-table-sketch", [(lambda v: f6(float(v)), {})], xr=(-5, 4), yr=(-12, 18), step=2, points=[(-3, 0), (1, 0), (0, 3, True, "(0, 3)")],
           alt="Graph of a cubic rising to the right with x-intercepts -3 (crossing) and 1 (touching), y-intercept 3.")
B.orq(S, "honors", "The graph shows f(x) = (x + 3)(x - 1)².",
      [("Find the x-intercepts and their multiplicities.", "-3 (mult. 1), 1 (mult. 2)"), ("Find the y-intercept.", "3"), ("Describe the end behavior.", "down on the left, up on the right"),
       ("For what x is f(x) > 0?", "x > -3, x ≠ 1")],
      ["Set factors to 0.", "f(0) = 3·1 = 3.", "Degree 3, lead +1.", "Sign is positive right of -3 except at the touching zero x = 1."], diagram=dg, tags=["graph", "multiple-representations"])
B.orq(S, "cp1", "Sketch f(x) = x(x - 2)(x + 3) by hand.",
      [("List the zeros.", "-3, 0, 2"), ("State the end behavior.", "down on the left, up on the right"), ("Find f(-1) and f(1).", "f(-1) = 6, f(1) = -4"), ("Between which zeros is f negative?", "between 0 and 2 (and for x < -3)")],
      ["Set each factor to 0.", "Odd degree, positive lead.", "-1·(-3)·2 = 6; 1·(-1)·4 = -4.", "Test intervals."], tags=["graph"])
f7 = P.roots([0, 2, -3]); assert f7(-1) == 6 and f7(1) == -4
B.mc(S, "cp2", "Which polynomial rises on both ends?", "y = 2x⁴ - x", ["y = -x⁴ + 3", "y = x³ + 2", "y = -2x² + x"], ["Even degree with positive leading coefficient: both ends up."])

# ---------------- Skill 7: fundamental theorem of algebra ----------------
S = 7
for desc in [(1, 0, 0, -1), (2, -1, 0, 4, 3, 1), (1, 0, 0, 0, 16), (-3, 1, 2), (5, 0, 0, 0, 0, 0, 0, 1)]:
    f = P.coeffs(*desc)
    B.mc(S, "cp2", f"How many complex zeros (counting multiplicity) does f(x) = {f} have?", str(f.deg), [str(f.deg - 1), str(f.deg + 1), str(len([c for c in f.c if c]))],
         ["Fundamental Theorem of Algebra: a degree-n polynomial has exactly n complex zeros counted with multiplicity.", f"Degree {f.deg}."])
for zs in [(["2", "3i"], "x⁴ + 5x² - 36 has... "), ]:
    pass
cases = [([2], [(0, 3)]), ([-1], [(1, 2)]), ([], [(2, 1), (0, 1)]), ([3, -3], [(0, 2)]), ([1], [(-2, 1)])]
for reals, cplx in cases:
    f = P.roots(reals)
    for a_, b_ in cplx:
        f = f * P.coeffs(1, -2 * a_, a_ * a_ + b_ * b_)
    zs = [fr(r) for r in reals] + [(f"{a_} + {b_}i" if a_ else f"{b_}i").replace("1i", "i").replace(" + 1i", " + i") for a_, b_ in cplx]
    zs = [z if z != "1i" else "i" for z in zs]
    allz = [fr(r) for r in reals] + [w for a_, b_ in cplx for w in (((f"{a_} ± {b_}i" if a_ else f"±{b_}i").replace("± 1i", "± i").replace("±1i", "±i")),)]
    B.sa(S, "cp1" if len(cplx) == 1 and not cplx[0][0] else "honors", f"Write a polynomial of least degree with real coefficients, leading coefficient 1, and zeros {', '.join(zs)}.", ps(f),
         ["Non-real zeros of real polynomials come in conjugate pairs; include each conjugate.", "Multiply (x - a - bi)(x - a + bi) = x² - 2ax + (a² + b²).", f"f(x) = {ps(f)}."])
    B.sa(S, "cp1", f"Find all zeros of f(x) = {f}.", ", ".join(allz),
         [f"Factor: {factor_str(f)}.", "Solve any irreducible quadratic with the quadratic formula.", ", ".join(allz) + "."])
B.mc(S, "cp1", "A polynomial with real coefficients has zeros 4 and 2 - 5i. Which must also be a zero?", "2 + 5i", ["-2 + 5i", "-4", "5 - 2i"], ["Complex Conjugate Root Theorem."])
B.mc(S, "honors", "A polynomial with rational coefficients has zeros 3 and 1 + √2. What is the least possible degree?", "3", ["2", "4", "6"],
     ["Irrational conjugate 1 - √2 must also be a zero.", "Zeros 3, 1 + √2, 1 - √2 → degree 3."], tags=["reasoning"])
B.sa(S, "honors", "Write a polynomial with integer coefficients and leading coefficient 1 whose zeros include 1 + √2 and 3.", ps(P.coeffs(1, -2, -1) * P.coeffs(1, -3)),
     ["(x - 1 - √2)(x - 1 + √2) = x² - 2x - 1.", "Multiply by (x - 3): x³ - 5x² + 5x + 3."])
B.sel(S, "cp1", "A degree-4 polynomial with real coefficients has zeros 1 and 3i. Select ALL that must be true.", ["-3i is a zero", "It has at least 2 real zeros (with multiplicity)", "It has 4 complex zeros counted with multiplicity"],
      ["It has exactly one real zero", "-1 is a zero", "It has no other zeros"],
      ["Conjugate pair: 3i, -3i.", "4 zeros total; 2 are non-real, so the other 2 (counting 1) are real.", "The fourth zero is real but unknown."], tags=["reasoning"])
B.sel(S, "honors", "Select ALL possible combinations of zeros for a real cubic polynomial.", ["3 real zeros", "1 real and 2 non-real zeros", "1 real zero with multiplicity 3"],
      ["0 real and 3 non-real zeros", "2 real and 1 non-real zero"], ["Non-real zeros come in pairs, so the number of non-real zeros is even (0 or 2)."], tags=["reasoning"])
B.mc(S, "cp1", "Descartes: how many positive real zeros can f(x) = x⁴ - 3x³ + 2x² - x + 5 have?", "4, 2, or 0", ["4 only", "3 or 1", "1"],
     ["Sign changes: + - + - + → 4 changes.", "Possible positive zeros: 4, 2, or 0."], tags=["challenge"])
B.mc(S, "cp1", "A student says x² + 9 = 0 has no solutions, so the Fundamental Theorem of Algebra is false. What is wrong?", "It has two complex solutions, ±3i", ["Nothing; the theorem only applies to cubics", "x = ±3", "x = 9"],
     ["The theorem counts complex zeros, not only real ones."], tags=["misconception"])
B.orq(S, "honors", "f(x) = x⁴ - x³ - 2x² - 4x - 24 has a zero 2i.",
      [("Name another zero without calculation.", "-2i"), ("Find the quadratic factor with those zeros.", "x² + 4"),
       ("Divide to find the other quadratic factor.", ps(P.coeffs(1, -1, -2, -4, -24) // P.coeffs(1, 0, 4))), ("List all four zeros.", "2i, -2i, 3, -2")],
      ["Conjugate pair.", "(x - 2i)(x + 2i) = x² + 4.", "Long division.", "x² - x - 6 = (x - 3)(x + 2)."], tags=["multistep"])
assert P.coeffs(1, -1, -2, -4, -24) % P.coeffs(1, 0, 4) == P([0]) and P.coeffs(1, -1, -2, -4, -24) // P.coeffs(1, 0, 4) == P.coeffs(1, -1, -6)
B.orq(S, "cp1", "g(x) = x³ - 8.",
      [("How many complex zeros does g have?", "3"), ("Find the real zero.", "2"), ("Find the quadratic factor.", "x² + 2x + 4"), ("Find the non-real zeros.", "-1 ± i√3")],
      ["Degree 3.", "2³ = 8.", "Difference of cubes.", "x = (-2 ± √(4 - 16))/2."])
B.mc(S, "cp2", "According to the Fundamental Theorem of Algebra, every polynomial of degree n ≥ 1 has…", "at least one complex zero (exactly n counting multiplicity)", ["at least one real zero", "exactly n real zeros", "no more than n - 1 zeros"],
     ["The guarantee is about complex zeros."])
B.sa(S, "honors", "Find k so that x = 1 + i is a zero of x³ - 4x² + 6x + k.", "k = -4", ["(1 + i)² = 2i, (1 + i)³ = -2 + 2i.", "-2 + 2i - 8i + 6 + 6i + k = 4 + k = 0 → k = -4."], tags=["challenge"])
z = 1 + 1j; assert abs(z ** 3 - 4 * z ** 2 + 6 * z - 4) < 1e-12

# ---------------- Skill 8: polynomial equations and applications ----------------
S = 8
for desc in [(1, 0, -9, 0), (2, -8, 0), (1, -3, -10, 0), (1, 0, -10, 0, 9), (1, 2, -1, -2), (4, 0, -1, 0)]:
    f = P.coeffs(*desc); rts, rest = f.rational_roots(); assert rest.deg == 0
    B.sa(S, "cp2" if f.deg <= 3 and desc[-1] == 0 else "cp1", f"Solve {f} = 0.", ", ".join(f"x = {fr(r)}" for r in sorted(set(rts))),
         ["Factor completely.", f"{factor_str(f)} = 0.", "Set each factor equal to 0."])
for lhs, rhs in [((1, 0, 0), (0, 4, 0)), ((1, 0, 0, 0), (0, 16, 0)), ((2, 0, 0), (0, 0, 18)), ((1, 0, 0, 0, 0), (0, 0, 9, 0, 0))]:
    f = P.coeffs(*lhs) - P.coeffs(*rhs); rts, rest = f.rational_roots()
    ans = ", ".join(f"x = {fr(r)}" for r in sorted(set(rts)))
    B.mc(S, "cp1", f"Solve {P.coeffs(*lhs)} = {P.coeffs(*rhs)}.", ans,
         [", ".join(f"x = {fr(r)}" for r in sorted(set(rts)) if r != 0) or "x = 0", ", ".join(f"x = {fr(r)}" for r in sorted(set(rts)) if r >= 0), "no solution"],
         ["Move everything to one side; do not divide by a variable (that can lose x = 0).", f"{factor_str(f)} = 0.", ans + "."], tags=["misconception"])
for side, cut in [(12, 2), (20, 3), (16, 4)]:
    V = cut * (side - 2 * cut) ** 2
    B.sa(S, "cp1", f"Squares of side x are cut from the corners of a {side}-in by {side}-in sheet to form an open box. Write V(x) and find the volume when x = {cut}.",
         f"V(x) = x({side} - 2x)²; {V} in³", ["Base is (side - 2x) by (side - 2x), height x.", f"V({cut}) = {cut}·{side - 2 * cut}² = {V}."], tags=["modeling"])
B.sa(S, "honors", "A box with a square base and height 2 in. greater than the base edge has volume 96 in³. Find the base edge.", "4 in",
     ["x²(x + 2) = 96 → x³ + 2x² - 96 = 0.", "x = 4 works: 64 + 32 = 96.", "Quotient x² + 6x + 24 has no real zeros."], tags=["modeling"])
assert P.coeffs(1, 2, 0, -96)(4) == 0
B.sa(S, "honors", "The product of three consecutive integers is 210. Find them.", "5, 6, 7", ["n(n + 1)(n + 2) = 210.", "n³ + 3n² + 2n - 210 = 0; n = 5 works.", "The remaining quadratic has no real zeros."], tags=["modeling"])
assert P.coeffs(1, 3, 2, -210).rational_roots()[0] == [5]
B.sa(S, "honors", "Solve x³ - 3x² - 4x + 12 > 0.", "-2 < x < 2 or x > 3", ["Factor: (x - 3)(x - 2)(x + 2).", "Sign chart on intervals split by -2, 2, 3.", "Positive on (-2, 2) and (3, ∞)."], tags=["challenge"])
fpos = P.coeffs(1, -3, -4, 12); assert fpos(0) > 0 and fpos(F(5, 2)) < 0 and fpos(4) > 0 and fpos(-3) < 0
B.mc(S, "cp1", "A student solves x³ = 4x by dividing both sides by x and gets x = ±2. What was lost?", "x = 0", ["x = 4", "x = -4", "Nothing"], ["x³ - 4x = x(x - 2)(x + 2) = 0."], tags=["error-analysis"])
B.sel(S, "cp1", "Select ALL solutions of x⁴ - 5x² + 4 = 0.", ["-2", "-1", "1", "2"], ["4", "0", "5"], ["Quadratic in form: (x² - 1)(x² - 4) = 0."])
B.sel(S, "honors", "Select ALL real solutions of x³ + x² - 2x - 2 = 0.", ["-1", "√2", "-√2"], ["1", "2", "-2"], ["Group: x²(x + 1) - 2(x + 1) = (x + 1)(x² - 2)."])
for v in [-1, 2 ** 0.5, -(2 ** 0.5)]: assert abs(v ** 3 + v ** 2 - 2 * v - 2) < 1e-12
B.mc(S, "cp1", "Revenue is R(x) = -x³ + 12x² for x hundred units (0 ≤ x ≤ 12). Which x gives revenue of 0?", "x = 0 and x = 12", ["x = 12 only", "x = 6", "x = 0 only"], ["-x²(x - 12) = 0."], tags=["modeling"])
B.orq(S, "honors", "An open box is made from a 10 in × 16 in sheet by cutting squares of side x from each corner.",
      [("Write V(x) in factored form.", "V(x) = x(10 - 2x)(16 - 2x)"), ("State a reasonable domain.", "0 < x < 5"),
       ("Find V(2).", "144 in³"), ("Verify that x = 2 gives the maximum among whole-number cuts.", "V(1) = 112, V(2) = 144, V(3) = 120, V(4) = 64")],
      ["Base (10 - 2x)(16 - 2x), height x.", "10 - 2x > 0.", "2·6·12 = 144.", "Compare values."], tags=["modeling", "multistep"])
Vb = lambda v: v * (10 - 2 * v) * (16 - 2 * v); assert [Vb(i) for i in (1, 2, 3, 4)] == [112, 144, 120, 64]
B.orq(S, "cp1", "Solve 2x³ - x² - 18x + 9 = 0.",
      [("Group the terms.", "x²(2x - 1) - 9(2x - 1)"), ("Factor completely.", "(2x - 1)(x - 3)(x + 3)"), ("Solve.", "x = 1/2, 3, -3"), ("Check one solution.", "2(27) - 9 - 54 + 9 = 0 at x = 3")],
      ["Group pairs.", "Difference of squares.", "Zero-product property.", "Substitute x = 3."])
B.orq(S, "honors", "Find two polynomials with the same zeros but different graphs.",
      [("Write f with zeros -1, 2 and leading coefficient 1.", "f(x) = x² - x - 2"), ("Write g with the same zeros but g(0) = 6.", "g(x) = -3x² + 3x + 6"),
       ("Write h with the same distinct zeros but degree 3, touching at 2.", "h(x) = (x + 1)(x - 2)²"), ("Explain why zeros alone don't determine a polynomial.", "Leading coefficient and multiplicities can vary")],
      ["(x + 1)(x - 2).", "a(x + 1)(x - 2) with -2a = 6 → a = -3.", "Square the factor for an even multiplicity.", "Many polynomials share zeros."], tags=["reasoning"])
B.sa(S, "cp2", "Solve (x - 6)(x + 1)(2x - 5) = 0.", "x = 6, x = -1, x = 5/2", ["Zero-product property: set each factor to 0."])
B.sa(S, "cp2", "Solve x³ - 49x = 0.", "x = 0, x = 7, x = -7", ["x(x² - 49) = x(x - 7)(x + 7) = 0."])

# ================= Session 2b: format-balance additions (select-all, open-response, conceptual) =================
# Skill 1
for a, b in [((1, 3), (1, -5)), ((2, -1), (1, 4)), ((3, 2), (3, -2)), ((1, -4), (1, 0, 2))]:
    A, Bp = P.coeffs(*a), P.coeffs(*b); prod = A * Bp
    cands = [ps(prod), f"({Bp})({A})", ps(P.coeffs(*a[:1], 0) * Bp + P([a[-1]]) * Bp),
             ps(P([c for c in prod.c[:1]] + [0] * (len(prod.c) - 2) + [prod.lead])), ps(prod + P([0, 1])), ps(-prod)]
    sel_auto(B, 1, "cp1", f"Select ALL expressions equivalent to ({A})({Bp}).", cands, is_equiv(f"({A})({Bp})"),
             ["Multiply out and compare with each choice (or test a value of x).", f"({A})({Bp}) = {prod}.", "Multiplication is commutative, so reordering the factors keeps it equivalent."])
for f_, g_ in [((1, 0, -2), (2, -1)), ((3, -1, 4), (1, 2)), ((-1, 2, 0, 1), (1, 0, 3))]:
    f, g = P.coeffs(*f_), P.coeffs(*g_)
    B.orq(1, "cp1" if f.deg < 3 else "honors", f"Let f(x) = {f} and g(x) = {g}.",
          [("Find f(x) + g(x).", ps(f + g)), ("Find f(x) - g(x).", ps(f - g)), ("Find f(x)·g(x).", ps(f * g)), ("What is the degree of f·g, and why?", f"{(f * g).deg}: degrees add ({f.deg} + {g.deg})")],
          ["Combine like terms.", "Distribute the negative sign to every term of g.", "Distribute each term of f over g, then combine.", "Leading terms multiply, so degrees add."])
B.mc(1, "cp1", "Which product has degree 5?", "(x³ - 1)(x² + 4)", ["(x⁵ + 1) + (x² - 1)", "(x² + 1)(x² - 1)", "(x⁴ + x)(x⁴ - x)"], ["Degrees add when multiplying: 3 + 2 = 5.", "The sum in the first distractor has degree 5 but is not a product; the others have degree 4 and 8."])
B.sel(1, "honors", "f and g are polynomials of degree 4. Select ALL degrees that f + g could have.", ["4", "2", "0 (a nonzero constant)"], ["8", "5"],
      ["Leading terms can cancel, lowering the degree to anything ≤ 4.", "Example: (x⁴ + x²) + (-x⁴) = x².", "The sum can never exceed degree 4."], tags=["reasoning"])
# Skill 2
for target, cands in [("x^3 - 27", ["(x - 3)(x² + 3x + 9)", "(x - 3)³", "(x - 3)(x² - 3x + 9)", "-(3 - x)(x² + 3x + 9)", "(x + 3)(x² - 3x - 9)"]),
                      ("8x^3 + 1", ["(2x + 1)(4x² - 2x + 1)", "(2x + 1)³", "(2x + 1)(4x² + 2x + 1)", "(1 + 2x)(1 - 2x + 4x²)"]),
                      ("x^4 - 16", ["(x² - 4)(x² + 4)", "(x - 2)(x + 2)(x² + 4)", "(x - 2)²(x + 2)²", "(x² - 4)²", "(x - 2)(x + 2)(x - 2)(x + 2)"])]:
    sel_auto(B, 2, "cp1", f"Select ALL expressions equivalent to {target.replace('^3', '³').replace('^4', '⁴')}.", cands, is_equiv(target),
             ["Use the sum/difference of cubes or difference of squares pattern.", "Check each option by expanding or by substituting a test value such as x = 1."], tags=["error-analysis"])
# Skill 3
for desc, r in [((1, -3, -4, 12), 2), ((2, 1, -13, 6), -3), ((1, 0, -10, 3), 3), ((3, -2, 0, 5), 1)]:
    N = P.coeffs(*desc); q, rem = N.divmod(P([-r, 1])); rv = rem.c[0]
    st = [f"The quotient is {q}", f"The remainder is {fr(rv)}", f"{lin_factor(r)[1:-1]} is a factor of {N}" if rv == 0 else f"{lin_factor(r)[1:-1]} is not a factor of {N}",
          f"The quotient is {ps(P.coeffs(*N.synth(-r)[:-1]))}", f"The remainder is {fr(N(-r))}", f"The quotient has degree {N.deg}"]
    truth = [True, True, True, P.coeffs(*N.synth(-r)[:-1]) == q, N(-r) == rv, N.deg == q.deg]
    tt = dict(zip(reversed(st), reversed(truth)))
    B.sel(3, "cp1", f"({N}) ÷ ({lin_factor(r)[1:-1]}). Select ALL true statements.", [s_ for s_ in dict.fromkeys(st) if tt[s_]], [s_ for s_ in dict.fromkeys(st) if not tt[s_]],
          [f"Synthetic division with {r}: {', '.join(fr(c) for c in N.synth(r))}.", f"Quotient {q}, remainder {fr(rv)}.", f"Using {-r} instead of {r} is a common sign error."], tags=["misconception"])
for desc, d in [((1, 5, 2, -8), (1, 2)), ((2, -5, 0, 4), (1, -2)), ((1, 0, 0, 1), (1, 1))]:
    N, D = P.coeffs(*desc), P.coeffs(*d); q, rem = N.divmod(D)
    B.orq(3, "cp1", f"Divide {N} by {D}.",
          [("Set up synthetic division (number and coefficients).", f"{fr(-D.c[0])} | {', '.join(fr(c) for c in N.desc())}"), ("Write the bottom row.", ", ".join(fr(c) for c in N.synth(-D.c[0]))),
           ("Write the result as quotient + remainder/divisor.", ps(q) + ("" if rem == P([0]) else f" + {fr(rem.c[0])}/({D})")), ("Check by multiplying back.", f"({D})({q}) + {fr(rem.c[0])} = {N}")],
          ["Use the zero of the divisor.", "Bring down, multiply, add.", "Last entry is the remainder.", "Divisor × quotient + remainder = dividend."])
B.mc(3, "honors", "P(x) ÷ (x - 3) gives quotient Q(x) and remainder 7. Which equation is true?", "P(x) = (x - 3)Q(x) + 7", ["P(x) = (x - 3)Q(x) - 7", "Q(x) = (x - 3)P(x) + 7", "P(x) = Q(x) + 7/(x - 3)"], ["Division algorithm: dividend = divisor × quotient + remainder."], tags=["reasoning"])
B.sa(3, "honors", "Find the quotient when x⁵ - 1 is divided by x - 1.", "x⁴ + x³ + x² + x + 1", ["Synthetic division with 1: 1, 1, 1, 1, 1, 0."], tags=["connections"])
assert P.coeffs(1, 0, 0, 0, 0, -1) // P.coeffs(1, -1) == P.coeffs(1, 1, 1, 1, 1)
# Skill 4
for desc in [(1, -2, -5, 6), (1, 1, -10, 8), (2, -3, -8, -3), (1, -4, -7, 10)]:
    f = P.coeffs(*desc); rts = f.rational_roots()[0]; c = rts[-1]
    B.orq(4, "cp1" if desc[0] == 1 else "honors", f"Let f(x) = {f}.",
          [(f"Evaluate f({fr(c)}).", "0"), ("What does the Factor Theorem tell you?", f"{lin_factor(c)[1:-1]} is a factor"),
           ("Divide to find the quadratic factor.", ps(f // P([-c, 1]))), ("Find all zeros.", ", ".join(fr(r) for r in rts))],
          ["Substitute.", "f(c) = 0 ⇔ (x - c) is a factor.", "Synthetic division.", f"f(x) = {factor_str(f)}."])
    cands = [lin_factor(v)[1:-1] for v in sorted(set(rts) | {-r for r in rts} | {F(1)})]
    sel_auto(B, 4, "cp1", f"Select ALL binomials that are factors of {f}.", cands, lambda s, f=f: f(root_of(s)) == 0,
             ["x - c is a factor exactly when f(c) = 0.", f"f(x) = {factor_str(f)}."])
B.sel(4, "honors", "p(x) has remainder 0 when divided by x - 2 and remainder 3 when divided by x + 1. Select ALL true statements.", ["p(2) = 0", "p(-1) = 3", "(x - 2) is a factor of p(x)"],
      ["p(1) = 3", "(x + 1) is a factor of p(x)", "p(-2) = 0"], ["Remainder Theorem: remainder on division by x - c is p(c)."], tags=["reasoning"])
B.mc(4, "honors", "Without dividing, find the remainder when x¹⁰⁰ - 3x⁵⁰ + 2 is divided by x + 1.", "0", ["6", "-2", "2"], ["Remainder = f(-1) = 1 - 3 + 2 = 0."], tags=["challenge"])
# Skill 5
for rs, a in [([-2, 1, 3], 1), ([F(1, 2), -1, 4], 2), ([0, -3, -3], 1)]:
    f = P.roots(rs, a); cands = sorted(set([fr(r) for r in rs] + [fr(-r) for r in rs if r] + ["1"]), key=lambda v: float(F(v)))
    sel_auto(B, 5, "cp1" if a == 1 else "honors", f"Select ALL zeros of f(x) = {f}.", cands, is_zero_of(f),
             ["Test each value, or factor.", f"f(x) = {factor_str(f)}."])
B.orq(5, "honors", "A polynomial f has degree 4, leading coefficient -1, a zero of multiplicity 2 at x = 1, and simple zeros at x = -2 and x = 3.",
      [("Write f in factored form.", "f(x) = -(x - 1)²(x + 2)(x - 3)"), ("Find the y-intercept.", fr(-P.roots([1, 1, -2, 3])(0))),
       ("Describe the end behavior.", "down on both ends"), ("At which zero does the graph touch without crossing?", "x = 1")],
      ["Multiplicity → exponent.", "f(0) = -(1)(2)(-3) = 6.", "Even degree, negative lead.", "Even multiplicity."], tags=["graph"])
assert -P.roots([1, 1, -2, 3])(0) == 6
# Skill 6
for desc in [(1, 0, -4, 0), (-1, 0, 5, 0, -4), (2, -3, 0, 1)]:
    f = P.coeffs(*desc); d = f.deg; a = f.lead
    left = "rises" if (a > 0) == (d % 2 == 0) else "falls"; right = "rises" if a > 0 else "falls"
    cands = [f"The graph {left} to the left", f"The graph {right} to the right", f"It has at most {d - 1} turning points", f"The y-intercept is {fr(f(0))}",
             f"The graph {'falls' if left == 'rises' else 'rises'} to the left", f"It has at most {d} turning points", f"The y-intercept is {fr(f.c[1] if len(f.c) > 1 else 1)}" if f.c[1] != f(0) else f"The y-intercept is {fr(f(0) + 1)}"]
    B.sel(6, "cp1", f"Select ALL true statements about f(x) = {f}.", cands[:4], cands[4:],
          [f"Degree {d}, leading coefficient {fr(a)} → end behavior.", f"At most n - 1 = {d - 1} turning points.", f"f(0) = {fr(f(0))}."], tags=["graph"])
B.mc(6, "honors", "f(x) = (x - 2)³. Near x = 2, the graph…", "crosses the axis and flattens like a cubic", ["touches and turns", "crosses like a straight line", "has a vertical asymptote"],
     ["Odd multiplicity greater than 1 → crosses with a flattened (inflection) shape."], tags=["graph"])
# Skill 7
for reals, (ca, cb) in [([1], (0, 2)), ([-2], (1, 1)), ([3], (-1, 2))]:
    f = P.roots(reals) * P.coeffs(1, -2 * ca, ca * ca + cb * cb)
    zc = (f"{ca} + {cb}i" if ca else f"{cb}i").replace(" 1i", " i"); zcc = (f"{ca} - {cb}i" if ca else f"-{cb}i").replace(" 1i", " i")
    cands = [fr(reals[0]), zc, zcc, fr(-reals[0]), (f"{-ca} + {cb}i" if ca else f"{cb}").replace(" 1i", " i"), f"{cb}" if ca else f"{-cb}"]
    sel_auto(B, 7, "honors", f"Select ALL zeros of f(x) = {f}.", cands, is_zero_of(f),
             [f"f(x) = {factor_str(f)}.", "Solve the quadratic factor with the quadratic formula; non-real zeros come in conjugate pairs."])
B.orq(7, "honors", "A cubic with real coefficients and leading coefficient 1 has zeros 2 and 1 - 3i.",
      [("Name the third zero.", "1 + 3i"), ("Find the quadratic factor for the non-real zeros.", "x² - 2x + 10"), ("Write the cubic in standard form.", ps(P.coeffs(1, -2, 10) * P.coeffs(1, -2))), ("Find f(0).", fr((P.coeffs(1, -2, 10) * P.coeffs(1, -2))(0)))],
      ["Conjugate pair.", "x² - 2(1)x + (1 + 9).", "Multiply by (x - 2).", "Constant term."])
B.mc(7, "cp1", "How many non-real zeros does x⁴ - 1 have?", "2", ["0", "4", "1"], ["x⁴ - 1 = (x - 1)(x + 1)(x² + 1).", "Zeros 1, -1, i, -i."])
# Skill 8
for desc in [(1, -1, -6, 0), (1, 0, -13, 0, 36), (2, 1, -8, -4)]:
    f = P.coeffs(*desc); rts = sorted(set(f.rational_roots()[0]))
    cands = sorted(set([fr(r) for r in rts] + [fr(-r) for r in rts if -r not in rts] + ["0", "1"]), key=lambda v: float(F(v)))
    sel_auto(B, 8, "cp1", f"Select ALL solutions of {f} = 0.", cands, is_zero_of(f), ["Factor completely.", f"{factor_str(f)} = 0."])
for side, h in [(14, 3), (18, 2)]:
    V = lambda v, side=side: v * (side - 2 * v) ** 2
    best = max(range(1, side // 2), key=V)
    B.orq(8, "cp1", f"An open box is made by cutting x-inch squares from the corners of a {side}-inch square sheet.",
          [("Write V(x).", f"V(x) = x({side} - 2x)²"), ("Give the domain.", f"0 < x < {side // 2}"), (f"Find V({h}).", f"{V(h)} in³"), ("Which whole-number cut gives the largest volume?", f"x = {best} ({V(best)} in³)")],
          ["Height x, base (side - 2x) square.", "All dimensions positive.", f"{h}·{side - 2 * h}² = {V(h)}.", "Compare V(1), V(2), … ."], tags=["modeling"])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
