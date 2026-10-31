"""Session-2 top-up for functions-transformations: appends items (IDs continue) to the session-1 bank."""
from lib import Bank, graph, OUT
from mathlite import *
ps = pstr
import math

STD = {1: ["F-IF.A.2"], 2: ["F-IF.A.1", "F-IF.B.5"], 3: ["F-BF.A.1b", "F-BF.A.1c"],
       4: ["F-BF.B.4a", "F-BF.B.4c"], 5: ["F-BF.B.3"], 6: ["F-IF.C.7b"], 7: ["F-BF.B.3"],
       8: ["F-BF.A.1", "F-IF.B.4"]}
U = "functions-transformations"
B = Bank.resume(U, "ft", STD, f"base/{U}.json", f"base/{U}.tags.json")  # session-1 bank (pristine copy) so reruns are idempotent
N0 = len(B.qs)
import s1_fixes; s1_fixes.apply(B)  # cosmetic notation fixes to session-1 items (see PROGRESS.md)

# ---- Skill 1: function notation and evaluation ----
f = P.coeffs(1, -4, 3)
sel_auto(B, 1, "cp2", "f(x) = x² - 4x + 3. Select ALL true statements.", ["f(0) = 3", "f(1) = 0", "f(-1) = 8", "f(2) = -1", "f(3) = 3", "f(4) = 0"],
         lambda s_: (lambda a, b: f(int(a)) == int(b))(*re.match(r"f\((-?\d+)\) = (-?\d+)", s_).groups()), ["Substitute each input."])
B.orq(1, "honors", "Let f(x) = 2x² - x and g(x) = 3 - x.", [("Find f(a + 1) in expanded form.", "2a² + 3a + 1"), ("Find g(f(1)).", "2"),
      ("Find the difference quotient (f(x + h) - f(x))/h.", "4x + 2h - 1"), ("Solve f(x) = g(x).", "x = ±√6/2")], ["2(a + 1)² - (a + 1).", "f(1) = 1; g(1) = 2.", "(4xh + 2h² - h)/h.", "2x² - x = 3 - x → 2x² = 3 → x = ±√(3/2) = ±√6/2."], tags=["challenge"])
assert eqcheck("2(x + 1)^2 - (x + 1)", "2x^2 + 3x + 1")
B.mc(1, "cp1", "If f(x) = 3x - 7, which expression is f(x + 2)?", "3x - 1", ["3x - 5", "3x + 2", "3x - 7 + 2"], ["Replace x with (x + 2): 3(x + 2) - 7 = 3x - 1.", "f(x) + 2 = 3x - 5 is a different expression."], tags=["misconception"])

# ---- Skill 2: domain and range ----
for fx, dom, wr in [("f(x) = √(6 - 2x)", "x ≤ 3", ["x ≥ 3", "x ≤ 6", "all real numbers"]), ("f(x) = 5/(x² - 9)", "x ≠ ±3", ["x ≠ 3", "x > 3", "all real numbers"]), ("f(x) = √(x + 1)/(x - 4)", "x ≥ -1, x ≠ 4", ["x ≥ -1", "x ≠ 4", "x > 4"]),
                    ("f(x) = ∛(x - 7)", "all real numbers", ["x ≥ 7", "x ≠ 7", "x > 0"])]:
    B.mc(2, "cp1", f"What is the domain of {fx}?", dom, wr, ["Exclude inputs that make a denominator 0 or an even-root radicand negative.", f"Domain: {dom}."], tags=["misconception"])
sel_auto(B, 2, "cp1", "Select ALL functions whose range is y ≥ 0.", ["y = x²", "y = |x - 3|", "y = √x", "y = x² + 1", "y = -x²", "y = 2^x"], lambda s_: s_ in ("y = x²", "y = |x - 3|", "y = √x"),
         ["x² + 1 has range y ≥ 1; -x² has y ≤ 0; 2^x has y > 0 (0 not included)."], tags=["reasoning"])
B.orq(2, "honors", "f(x) = -2(x - 1)² + 8.", [("State the domain.", "all real numbers"), ("State the range.", "y ≤ 8"), ("For what x is f(x) ≥ 0?", "-1 ≤ x ≤ 3"), ("Restrict the domain so f is one-to-one and increasing.", "x ≤ 1")],
      ["Polynomial.", "Opens down, max 8.", "(x - 1)² ≤ 4.", "Left of the vertex."], tags=["connections"])
B.sa(2, "honors", "Find the domain of f(x) = √(x² - 5x + 6).", "x ≤ 2 or x ≥ 3", ["(x - 2)(x - 3) ≥ 0."], tags=["challenge"])

# ---- Skill 3: operations and composition ----
for fpoly, gpoly in [(P.coeffs(1, 0, 1), P.coeffs(2, -3)), (P.coeffs(3, 1), P.coeffs(1, 0, -2)), (P.coeffs(1, -1), P.coeffs(1, 2, 0))]:
    fg = sum((gpoly ** k) * fpoly.c[k] for k in range(len(fpoly.c))); gf = sum((fpoly ** k) * gpoly.c[k] for k in range(len(gpoly.c)))
    B.orq(3, "cp1", f"f(x) = {fpoly} and g(x) = {gpoly}.", [("Find (f ∘ g)(x).", ps(fg)), ("Find (g ∘ f)(x).", ps(gf)), ("Find (f ∘ g)(1).", fr(fg(1))), ("Is f ∘ g = g ∘ f?", "Yes" if fg == gf else "No")],
          ["Substitute g(x) into f.", "Substitute f(x) into g.", "Evaluate.", "Compare the expressions."])
sel_auto(B, 3, "honors", "f(x) = √x and g(x) = x - 4. Select ALL true statements.", ["(f ∘ g)(x) = √(x - 4)", "The domain of f ∘ g is x ≥ 4", "(g ∘ f)(9) = -1", "(g ∘ f)(x) = √x - 4", "(f ∘ g)(0) = -2", "The domain of g ∘ f is all real numbers"],
         lambda s_: s_ in ("(f ∘ g)(x) = √(x - 4)", "The domain of f ∘ g is x ≥ 4", "(g ∘ f)(9) = -1", "(g ∘ f)(x) = √x - 4"), ["Composition domains require each step to be defined.", "√(0 - 4) is not real; g ∘ f needs x ≥ 0."])
B.mc(3, "cp1", "h(x) = (2x + 1)³. Which f and g give h = f ∘ g?", "f(x) = x³, g(x) = 2x + 1", ["f(x) = 2x + 1, g(x) = x³", "f(x) = 2x³, g(x) = x + 1", "f(x) = x³ + 1, g(x) = 2x"], ["The inner function is applied first."], tags=["reasoning"])

# ---- Skill 4: inverses ----
for fx, inv in [("f(x) = (x + 3)/2", "f⁻¹(x) = 2x - 3"), ("f(x) = x³ - 1", "f⁻¹(x) = ∛(x + 1)"), ("f(x) = 4/(x - 1)", "f⁻¹(x) = 4/x + 1")]:
    B.sel(4, "cp1", f"Select ALL true statements about {fx} and its inverse.", [inv, "f(f⁻¹(x)) = x"], ["f⁻¹(x) = 1/f(x)", f"f⁻¹(x) = -{fx[7:]}"], ["Swap x and y and solve.", "f⁻¹ is not the reciprocal."], tags=["misconception"])
B.orq(4, "honors", "f(x) = (x - 2)² + 1 with domain x ≥ 2.", [("Find the range of f.", "y ≥ 1"), ("Find f⁻¹(x).", "f⁻¹(x) = 2 + √(x - 1)"), ("State the domain of f⁻¹.", "x ≥ 1"), ("Verify f⁻¹(f(5)).", "f(5) = 10; f⁻¹(10) = 2 + 3 = 5")],
      ["Vertex (2, 1), opening up.", "Swap and take the positive root.", "Domain of f⁻¹ = range of f.", "Composition gives back 5."], tags=["challenge"])
B.orq(4, "cp1", "Temperature conversion F = (9/5)C + 32.", [("Find the inverse function C(F).", "C = (5/9)(F - 32)"), ("Convert 212°F.", "100°C"), ("What does the inverse input represent?", "Fahrenheit temperature"), ("Find the temperature where F = C.", "-40°")],
      ["Solve for C.", "(5/9)(180).", "Roles swap.", "x = (9/5)x + 32."], tags=["modeling"])
B.mc(4, "cp1", "Which function does NOT have an inverse function on all real numbers?", "f(x) = x² + 1", ["f(x) = 2x - 5", "f(x) = x³", "f(x) = e^x"], ["x² + 1 fails the horizontal line test."])
B.sa(4, "cp2", "If f(3) = 8, what is f⁻¹(8)?", "3", ["Inverses swap inputs and outputs."])
B.sa(4, "honors", "Find the inverse of f(x) = (2x + 1)/(x - 3).", "f⁻¹(x) = (3x + 1)/(x - 2)", ["x(y - 3) = 2y + 1 → xy - 2y = 3x + 1."], tags=["challenge"])
assert same(peval("(3x + 1)/(x - 2)", x=peval("(2x + 1)/(x - 3)", x=5.3)), 5.3)

# ---- Skill 5: parent functions and transformations ----
for parent, g, desc, wr in [("y = |x|", "y = -|x + 2| + 3", "reflect over the x-axis, left 2, up 3", ["reflect over the y-axis, left 2, up 3", "reflect over the x-axis, right 2, up 3", "left 2, down 3"]),
                            ("y = x²", "y = 3(x - 1)² - 4", "vertical stretch by 3, right 1, down 4", ["vertical shrink by 1/3, right 1, down 4", "vertical stretch by 3, left 1, down 4", "horizontal stretch by 3, right 1, up 4"]),
                            ("y = √x", "y = √(-x) + 1", "reflect over the y-axis, up 1", ["reflect over the x-axis, up 1", "left 1, up 1", "reflect over the y-axis, down 1"]),
                            ("y = x³", "y = (1/2)(x + 4)³", "vertical shrink by 1/2, left 4", ["vertical stretch by 2, left 4", "vertical shrink by 1/2, right 4", "horizontal shrink by 1/2, left 4"]),
                            ("y = 1/x", "y = 1/(x - 3) - 2", "right 3, down 2", ["left 3, down 2", "right 3, up 2", "right 2, down 3"])]:
    B.mc(5, "cp1", f"Describe the transformations from {parent} to {g}.", desc, wr, ["Inside changes are horizontal (opposite sign); outside are vertical.", desc + "."], tags=["misconception"])
for a, h, k in [(2, -1, -3), (-1, 3, 2), (F(1, 2), 0, 1)]:
    fn = lambda v, a=a, h=h, k=k: float(a) * abs(v - h) + k
    eq = f"y = {'' if a == 1 else '-' if a == -1 else fr(a)}|{lin_factor(h)[1:-1] if h else 'x'}|{'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}"
    dg = graph(B, f"s05-topup-abs-{len(B.qs)}", [(fn, {})], points=[(h, k, True, pt(h, k)), (h + 2, float(2 * a + k))], alt=f"Graph of an absolute value function with vertex {pt(h, k)} {'opening up' if a > 0 else 'opening down'}, passing through ({h + 2}, {fr(2 * a + k)}).")
    B.orq(5, "cp1" if a in (1, -1) else "honors", "The graph shows a transformation of y = |x|.", [("Find the vertex.", pt(h, k)), ("Find the slope of the right branch.", fr(a)), ("Write the equation.", eq), ("State the range.", f"y ≥ {k}" if a > 0 else f"y ≤ {k}")],
          ["Read the corner point.", "Rise over run from the vertex.", "y = a|x - h| + k.", "From the vertex up or down."], diagram=dg, tags=["graph"])
sel_auto(B, 5, "cp1", "g(x) = f(x - 2) + 5. Select ALL true statements.", ["The graph of f moves right 2 and up 5", "If (1, 4) is on f, then (3, 9) is on g", "The domains differ by a shift of 2", "The graph moves left 2", "If (1, 4) is on f, then (-1, 9) is on g"],
         lambda s_: s_ in ("The graph of f moves right 2 and up 5", "If (1, 4) is on f, then (3, 9) is on g", "The domains differ by a shift of 2"), ["(x, y) → (x + 2, y + 5)."])
B.sel(5, "honors", "Select ALL transformations that change the y-intercept of y = x² + 1.", ["Shift up 2", "Vertical stretch by 3", "Shift right 1"], ["Reflection over the y-axis", "Horizontal stretch by 2"], ["y-intercept = f(0); even functions are unchanged by y-axis reflection and horizontal stretch at x = 0."], tags=["reasoning"])
B.sa(5, "honors", "The point (4, -2) is on y = f(x). Find the corresponding point on y = -3f(2x) + 1.", "(2, 7)", ["x → x/2: 4 → 2.", "y → -3y + 1: -2 → 7."], tags=["challenge"])

# ---- Skill 6: piecewise functions ----
pw = lambda v: v * v - 1 if v < 0 else (2 * v - 1 if v <= 3 else 5)
for i, (spec, fn, pts_, ev) in enumerate([("f(x) = { -x if x < 0; x² if 0 ≤ x < 2; 4 if x ≥ 2 }", lambda v: -v if v < 0 else (v * v if v < 2 else 4), [(0, 0, True), (2, 4, True)], [(-3, 3), (1, 1), (5, 4)]),
                                          ("f(x) = { x + 3 if x ≤ -1; -2x if x > -1 }", lambda v: v + 3 if v <= -1 else -2 * v, [(-1, 2, True), (-1, 2, False)], [(-4, -1), (0, 0), (2, -4)]),
                                          ("f(x) = { 2 if x < 1; x - 1 if x ≥ 1 }", lambda v: 2 if v < 1 else v - 1, [(1, 2, False), (1, 0, True)], [(-5, 2), (1, 0), (4, 3)])]):
    for xv, yv in ev: assert fn(xv) == yv
    B.orq(6, "cp1", f"{spec}.", [(f"Find f({ev[0][0]}).", str(ev[0][1])), (f"Find f({ev[1][0]}).", str(ev[1][1])), (f"Find f({ev[2][0]}).", str(ev[2][1])), ("Is f continuous at the breakpoint(s)?", "Yes" if i == 0 else ("Yes" if fn(-1) == -2 * -1 else "No") if i == 1 else "No")],
          ["Choose the piece whose condition the input satisfies.", "Evaluate.", "Evaluate.", "Compare the left and right values at each breakpoint."])
    B.sel(6, "cp1", f"{spec}. Select ALL true statements.", [f"f({ev[0][0]}) = {ev[0][1]}", f"f({ev[2][0]}) = {ev[2][1]}"], [f"f({ev[0][0]}) = {ev[0][1] + 1}", f"f({ev[1][0]}) = {ev[1][1] + 2}"], ["Check which piece applies."])
B.mc(6, "cp1", "Which is the absolute value function written piecewise?", "|x| = { -x if x < 0; x if x ≥ 0 }", ["|x| = { x if x < 0; -x if x ≥ 0 }", "|x| = { -x if x > 0; x if x ≤ 0 }", "|x| = { x² if x < 0; x if x ≥ 0 }"], ["For negative x, -x is positive."], tags=["connections"])
B.sa(6, "cp1", "A phone plan costs $30 for up to 2 GB and $10 per extra GB (or part). Find the cost for 4.3 GB.", "$60", ["Extra 2.3 GB rounds up to 3 GB.", "30 + 3(10) = 60."], tags=["modeling"])
B.sa(6, "honors", "Find k so f(x) = { kx + 1 if x < 2; x² - k if x ≥ 2 } is continuous.", "k = 1", ["2k + 1 = 4 - k → 3k = 3."], tags=["challenge"])
B.sa(6, "cp2", "f(x) = { 5 if x < 0; x² if x ≥ 0 }. Find f(-2) + f(3).", "14", ["5 + 9."])
B.orq(6, "honors", "Shipping costs $6 for packages under 2 lb, $9 for 2 lb up to 5 lb, and $9 + $1.50 per lb over 5 lb.", [("Write C(w) piecewise.", "C = 6 (0 < w < 2); 9 (2 ≤ w ≤ 5); 9 + 1.5(w - 5) (w > 5)"), ("Find C(1.5).", "$6"), ("Find C(8).", "$13.50"), ("Is C continuous at w = 5?", "Yes: both sides give 9")],
      ["Three pieces.", "First piece.", "9 + 4.5.", "Compare."], tags=["modeling"])
B.sa(6, "cp1", "Evaluate the greatest integer function ⌊-2.4⌋ + ⌊3.9⌋.", "0", ["⌊-2.4⌋ = -3; ⌊3.9⌋ = 3."])

# ---- Skill 7: even and odd functions ----
for fx, kind in [("f(x) = x⁶ - 2x²", "even"), ("f(x) = 4x³ + x", "odd"), ("f(x) = x² + 3x", "neither"), ("f(x) = |x| + 5", "even"), ("f(x) = x/(x² + 1)", "odd"), ("f(x) = (x - 1)²", "neither")]:
    B.mc(7, "cp1" if "/" in fx or "|" in fx else "cp2", f"Is {fx} even, odd, or neither?", kind.capitalize(), [k.capitalize() for k in ("even", "odd", "neither") if k != kind] + ["Both"], ["Compute f(-x) and compare with f(x) and -f(x)."])
    g = lambda s_, v: peval(s_.split("= ")[1].replace("|x|", "abs(x)"), x=v)
    a_, b_ = g(fx, 1.3), g(fx, -1.3)
    assert (kind == "even") == same(a_, b_) and (kind == "odd") == same(a_, -b_)
sel_auto(B, 7, "cp1", "Select ALL functions whose graphs are symmetric about the origin.", ["y = x³", "y = 1/x", "y = sin x", "y = x⁵ - x", "y = x²", "y = |x|", "y = x³ + 1"], lambda s_: s_ in ("y = x³", "y = 1/x", "y = sin x", "y = x⁵ - x"), ["Odd: f(-x) = -f(x); symmetric about the origin."])
sel_auto(B, 7, "honors", "f is even and g is odd. Select ALL statements that must be true.", ["f·g is odd", "g·g is even", "f + f is even", "f + g is even", "g(0) = 0 if defined", "f(0) = 0"],
         lambda s_: s_ in ("f·g is odd", "g·g is even", "f + f is even", "g(0) = 0 if defined"), ["(f·g)(-x) = f(x)(-g(x)).", "g(0) = -g(0) → g(0) = 0."], tags=["reasoning"])
B.orq(7, "cp1", "f(x) = x⁴ - 3x².", [("Find f(-x).", "x⁴ - 3x²"), ("Is f even, odd, or neither?", "even"), ("Describe its symmetry.", "symmetric about the y-axis"), ("If f(2) = 4, find f(-2).", "4")], ["Even powers.", "f(-x) = f(x).", "Even ↔ y-axis.", "Same value."])
B.orq(7, "honors", "Any function can be written as an even part plus an odd part: E(x) = (f(x) + f(-x))/2, O(x) = (f(x) - f(-x))/2. Let f(x) = x³ + 2x² - x + 5.", [("Find f(-x).", "-x³ + 2x² + x + 5"), ("Find E(x).", "2x² + 5"), ("Find O(x).", "x³ - x"), ("Check E + O.", "x³ + 2x² - x + 5")],
      ["Substitute -x.", "Average.", "Half the difference.", "Sum."], tags=["challenge"])
B.mc(7, "cp1", "A graph is symmetric about the origin. Which point must be on it if (3, -5) is?", "(-3, 5)", ["(-3, -5)", "(3, 5)", "(5, -3)"], ["Origin symmetry: (x, y) → (-x, -y)."], tags=["graph"])
B.sa(7, "cp2", "f is even and f(4) = 7. Find f(-4).", "7", ["f(-x) = f(x)."])
B.sa(7, "cp2", "g is odd and g(2) = -6. Find g(-2).", "6", ["g(-x) = -g(x)."])
B.sa(7, "honors", "Can a nonzero function be both even and odd? Explain.", "No: f(x) = f(-x) = -f(x) forces f(x) = 0", ["Even and odd together give 2f(x) = 0."], tags=["reasoning"])

# ---- Skill 8: modeling with functions ----
B.orq(8, "cp1", "A rectangle has perimeter 40 cm and width x cm.", [("Write the length in terms of x.", "20 - x"), ("Write the area A(x).", "A(x) = x(20 - x)"), ("State a reasonable domain.", "0 < x < 20"), ("Find the maximum area.", "100 cm² at x = 10")], ["P = 2(l + w).", "l·w.", "Both sides positive.", "Vertex of the parabola."], tags=["modeling"])
B.orq(8, "cp1", "A taxi charges $3.50 plus $2.25 per mile.", [("Write C(m).", "C(m) = 2.25m + 3.5"), ("Find C(8).", "$21.50"), ("How far for $30.50?", "12 miles"), ("Interpret the slope.", "$2.25 per mile")], ["Initial fee + rate.", "Substitute.", "Solve 2.25m = 27.", "Rate of change."], tags=["modeling"])
B.orq(8, "honors", "A ball's height is h(t) = -16t² + 48t + 6.", [("Find h(0) and interpret.", "6 ft: initial height"), ("When is the ball highest?", "t = 1.5 s"), ("Find the maximum height.", "42 ft"), ("When does it land (nearest hundredth)?", f"{(48 + (48 ** 2 + 4 * 16 * 6) ** .5) / 32:.2f} s")], ["Substitute 0.", "-b/(2a).", "h(1.5).", "Quadratic formula, positive root."], tags=["modeling"])
assert -16 * 1.5 ** 2 + 48 * 1.5 + 6 == 42
for desc, good, wr in [("A gym charges $40 to join plus $25 per month. Total cost after m months:", "C(m) = 25m + 40", ["C(m) = 40m + 25", "C(m) = 65m", "C(m) = 25(m + 40)"]),
                       ("A population of 500 doubles every 3 years. Population after t years:", "P(t) = 500·2^(t/3)", ["P(t) = 500 + 2t/3", "P(t) = 500·2^(3t)", "P(t) = 1000t/3"]),
                       ("A 2000-gallon tank drains at 40 gallons per minute. Gallons left after t minutes:", "V(t) = 2000 - 40t", ["V(t) = 40t - 2000", "V(t) = 2000(0.96)^t", "V(t) = 2000 - 40/t"])]:
    B.mc(8, "cp1", desc + " Which model is correct?", good, wr, ["Identify the starting value and how the quantity changes (constant difference or constant ratio)."], tags=["modeling"])
B.sel(8, "cp1", "The cost to produce x shirts is C(x) = 4x + 150 and revenue is R(x) = 10x. Select ALL true statements.", ["Profit is P(x) = 6x - 150", "Break-even is at 25 shirts", "Each shirt adds $6 profit"], ["Profit is P(x) = 14x + 150", "Break-even is at 15 shirts"],
      ["P = R - C.", "6x = 150 → x = 25."], tags=["modeling"])
B.sa(8, "honors", "A box with a square base and no top has volume 32 ft³. Write the surface area S as a function of the base edge x.", "S(x) = x² + 128/x", ["Height h = 32/x².", "S = x² + 4x·h = x² + 128/x."], tags=["modeling", "challenge"])
B.sa(8, "cp2", "A car travels at 55 mph. Write the distance d after t hours.", "d(t) = 55t", ["Distance = rate × time."], tags=["modeling"])
B.sa(8, "cp1", "Movie tickets cost $12 for adults and $8 for children. Write the total cost T(a, c) and find T(2, 3).", "T = 12a + 8c; $48", ["24 + 24."], tags=["modeling"])

B.sel(6, "cp1", "f(x) = { 3 - x if x < 1; 2x if x ≥ 1 }. Select ALL true statements.", ["f(0) = 3", "f(1) = 2", "f is continuous at x = 1"], ["f(1) = 3", "f(2) = 1", "f has a jump at x = 1"], ["Left value 3 - 1 = 2 equals right value 2(1) = 2."])
B.mc(6, "honors", "Which piecewise function has range y ≥ 0?", "f(x) = { -x if x < 0; x² if x ≥ 0 }", ["f(x) = { x if x < 0; x² if x ≥ 0 }", "f(x) = { -x if x < 0; -x² if x ≥ 0 }", "f(x) = { x - 1 if x < 0; x if x ≥ 0 }"], ["Check the outputs of each piece over its domain."], tags=["reasoning"])
B.sel(8, "cp1", "Select ALL situations best modeled by a linear function.", ["A plumber charges $60 plus $45 per hour", "A candle burns 0.5 in per hour", "Savings grow by $20 per week"], ["A population grows 3% per year", "A ball's height after it is thrown", "A car's value drops 15% per year"], ["Constant rate of change → linear."], tags=["modeling"])
B.orq(8, "honors", "A farmer has 120 m of fence to enclose a rectangular pen along a river (no fence on the river side).", [("Write the area A(x) where x is the side perpendicular to the river.", "A(x) = x(120 - 2x)"), ("State the domain.", "0 < x < 60"), ("Find the x that maximizes area.", "30 m"), ("Find the maximum area.", "1800 m²")],
      ["Parallel side 120 - 2x.", "Lengths positive.", "Vertex -b/(2a) = 120/4.", "30·60."], tags=["modeling", "challenge"])
B.mc(8, "cp1", "A phone's battery drops from 100% to 40% in 5 hours at a constant rate. Which function gives the battery level?", "B(t) = 100 - 12t", ["B(t) = 100 - 60t", "B(t) = 40 + 12t", "B(t) = 100(0.6)^t"], ["Rate = (40 - 100)/5 = -12 per hour."], tags=["modeling"])
B.sa(8, "honors", "A rental company charges C(d) = 45d + 0.2(m - 100d) for m miles over d days when m > 100d. Find the cost of a 3-day rental driven 450 miles.", "$165", ["Extra miles: 450 - 300 = 150.", "45(3) + 0.2(150) = 165."], tags=["modeling"])

if __name__ == "__main__":
    p = B.write(); print(p, N0, "→", len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
