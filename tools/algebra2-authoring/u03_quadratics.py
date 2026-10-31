from lib import *

STD = {1: ["F-IF.C.7a"], 2: ["F-IF.C.8a", "A-SSE.B.3a"], 3: ["A-SSE.A.2"], 4: ["A-REI.B.4a", "A-REI.B.4b"],
       5: ["A-REI.B.4b"], 6: ["N-CN.A.1", "N-CN.A.2"], 7: ["N-CN.C.7"], 8: ["F-IF.B.4", "A-CED.A.1"]}
B = Bank("quadratic-functions-complex-numbers", "qc", STD)
I = sp.I

def vtx(a, b, c):
    h = F(-b, 2*a); k = a*h*h + b*h + c; return h, k

# ---------------- Skill 1: graphing quadratics ----------------
S = 1
for a, b, c in [(1, -4, 3), (-1, 2, 8), (2, 8, 5), (1, 6, 9), (-2, 4, 1), (F(1, 2), -2, -1)]:
    h, k = vtx(a, b, c); f = sp.nsimplify(a)*x**2 + b*x + c
    B.sa(S, "cp2", f"For y = {fmt(f, x)}, find the vertex and the axis of symmetry.", f"vertex {pt(h, k)}; x = {num(h)}",
         [f"x = -b/(2a) = {-b}/(2·{num(a)}) = {num(h)}.", f"y = {num(k)} at that x.", f"Axis of symmetry: x = {num(h)}."])
for a, b, c in [(1, -2, -3), (-1, 0, 4), (2, -4, 0)]:
    f = a*x**2 + b*x + c; h, k = vtx(a, b, c)
    B.mc(S, "cp2", f"Does y = {fmt(f, x)} have a maximum or a minimum, and what is it?",
         f"{'Minimum' if a > 0 else 'Maximum'} of {num(k)}", [f"{'Maximum' if a > 0 else 'Minimum'} of {num(k)}", f"{'Minimum' if a > 0 else 'Maximum'} of {num(h)}", f"{'Minimum' if a > 0 else 'Maximum'} of {c}"],
         [f"a = {a} {'> 0: opens up → minimum' if a > 0 else '< 0: opens down → maximum'}.", f"The extreme value is the vertex y-coordinate, {num(k)}; {num(h)} is its x-coordinate."], tags=["misconception"])
for (a, h, k), pts in [((1, 2, -4), [(0, 0), (4, 0)]), ((-1, -1, 4), [(-3, 0), (1, 0)]), ((F(1, 2), 0, -2), [(-2, 0), (2, 0)])]:
    fn = lambda v, a=a, h=h, k=k: float(a)*(v - h)**2 + k
    dg = graph(B, f"s01-parab-{h}-{k}", [(fn, {})], points=[(h, k, True, pt(h, k))] + [(p[0], p[1]) for p in pts],
               alt=f"A parabola with vertex {pt(h, k)} opening {'up' if a > 0 else 'down'} and crossing the x-axis at {pts[0][0]} and {pts[1][0]}.")
    eq = f"y = {fmt(sp.nsimplify(a)*(x - h)**2 + k)}"
    B.mc(S, "cp1", "Which equation matches the graph?", eq,
         [f"y = {fmt(sp.nsimplify(a)*(x + h)**2 + k)}" if h else f"y = {fmt(sp.nsimplify(2*a)*x**2 + k)}", f"y = {fmt(sp.nsimplify(-a)*(x - h)**2 + k)}", f"y = {fmt(sp.nsimplify(a)*(x - h)**2 - k)}"],
         [f"Vertex {pt(h, k)} gives y = a(x - h)² + k.", f"Use an x-intercept to find a: a = {num(a)}."], diagram=dg, tags=["graph"])
B.sel(S, "cp1", "Select ALL true statements about y = -2x² + 8x - 6.", ["The graph opens down", "The vertex is (2, 2)", "The x-intercepts are 1 and 3", "The y-intercept is -6"],
      ["The axis of symmetry is x = -2", "The minimum value is 2"],
      ["a = -2 < 0.", "h = -8/(-4) = 2, k = -8 + 16 - 6 = 2.", "-2(x² - 4x + 3) = -2(x - 1)(x - 3).", "y(0) = -6.", "Axis is x = 2; 2 is a maximum."])
B.sa(S, "cp1", "A parabola has x-intercepts -3 and 5. What is its axis of symmetry?", "x = 1", ["The axis lies midway between the zeros: (-3 + 5)/2 = 1."])
B.sa(S, "cp1", "The point (6, 11) is on a parabola with axis of symmetry x = 2. Name another point on the parabola.", "(-2, 11)",
     ["6 is 4 units right of the axis.", "Reflect 4 units left: x = -2, same y."])
B.mc(S, "cp1", "Which change makes the graph of y = ax² narrower?", "Increasing |a|", ["Decreasing |a|", "Increasing c", "Changing the sign of a"],
     ["Larger |a| stretches vertically, making the parabola narrower."])
B.sa(S, "honors", "Find the quadratic with vertex (-1, 5) that passes through (1, -3). Write it in standard form.", "y = -2x² - 4x + 3",
     ["y = a(x + 1)² + 5; -3 = 4a + 5 → a = -2.", "Expand: -2(x² + 2x + 1) + 5 = -2x² - 4x + 3."])
B.sa(S, "honors", "For what values of c does y = x² - 6x + c have its vertex below the x-axis?", "c < 9",
     ["Vertex at x = 3: k = 9 - 18 + c = c - 9.", "c - 9 < 0 → c < 9."], tags=["reasoning"])
B.sa(S, "honors", "The parabola y = ax² + bx + c passes through (0, 4), has axis x = 3, and its minimum value is -5. Find a, b, c.", "a = 1, b = -6, c = 4",
     ["c = 4.", "Vertex (3, -5): y = a(x - 3)² - 5; at x = 0: 9a - 5 = 4 → a = 1.", "Expand: x² - 6x + 4."], tags=["challenge"])
B.orq(S, "honors", "f(x) = x² - 2x - 8 and g(x) = -x² + 2x + 8.",
      [("Find the vertex of each.", "f: (1, -9); g: (1, 9)"), ("How are the graphs related?", "g = -f: reflection over the x-axis"),
       ("Find the x-intercepts of both.", "-2 and 4 for both"), ("Find the area of the quadrilateral whose vertices are the two vertices and the two shared intercepts.", "54")],
      ["h = 1 for both; f(1) = -9, g(1) = 9.", "g(x) = -(x² - 2x - 8).", "(x - 4)(x + 2) = 0.", "Diagonals 6 (horizontal) and 18 (vertical) are perpendicular: area = ½·6·18 = 54."], tags=["connections"])

# ---------------- Skill 2: vertex and intercept forms ----------------
S = 2
for a, h, k in [(1, 3, -2), (-1, -2, 5), (2, 1, -8), (3, -1, 0), (-2, 4, 3)]:
    f = sp.expand(a*(x - h)**2 + k)
    B.sa(S, "cp2", f"Write y = {fmt(a*(x - h)**2 + k)} in standard form.", f"y = {fmt(f, x)}",
         [f"Square the binomial: (x - {h})² = {fmt(sp.expand((x - h)**2), x)}.".replace("- -", "+ "), "Distribute a and add k.", f"y = {fmt(f, x)}."])
for a, r1, r2 in [(1, 2, -5), (-1, 3, 7), (2, -1, 4), (-3, 0, 2)]:
    f = sp.expand(a*(x - r1)*(x - r2)); h = F(r1 + r2, 2); k = a*(h - r1)*(h - r2)
    B.sa(S, "cp1", f"For y = {fmt(a*(x - r1)*(x - r2))}, state the x-intercepts and the vertex.", f"x = {r1} and x = {r2}; vertex {pt(h, k)}",
         ["Intercept form y = a(x - p)(x - q) shows zeros p and q.", f"Vertex x = (p + q)/2 = {num(h)}.", f"y = {num(k)}."])
for a, b, c in [(1, 8, 10), (1, -6, 1), (2, -12, 7), (-1, 4, 2), (3, 6, -1)]:
    h, k = vtx(a, b, c)
    B.sa(S, "cp1", f"Write y = {fmt(a*x**2 + b*x + c, x)} in vertex form by completing the square.", f"y = {fmt(a*(x - sp.nsimplify(h))**2 + sp.nsimplify(k))}",
         [f"Factor {a} from the x-terms if needed, then add and subtract (b/2a)².", f"Vertex ({num(h)}, {num(k)}).", f"y = {fmt(a*(x - sp.nsimplify(h))**2 + sp.nsimplify(k))}."])
B.mc(S, "cp2", "Which form makes the x-intercepts easiest to read?", "y = -2(x - 1)(x + 5)", ["y = -2(x + 2)² + 18", "y = -2x² - 8x + 10", "All forms equally"],
     ["Intercept (factored) form shows zeros directly: 1 and -5.", "All three are the same function."])
B.sel(S, "cp1", "Select ALL equations equivalent to y = x² - 4x - 5.", ["y = (x - 5)(x + 1)", "y = (x - 2)² - 9", "y = (x + 1)(x - 5)"],
      ["y = (x - 2)² - 1", "y = (x + 5)(x - 1)", "y = (x - 4)² + 11"],
      ["(x - 5)(x + 1) = x² - 4x - 5.", "(x - 2)² - 9 = x² - 4x + 4 - 9.", "(x - 2)² - 1 = x² - 4x + 3; (x + 5)(x - 1) = x² + 4x - 5."])
B.mc(S, "cp1", "A student writes x² + 6x + 2 = (x + 3)² + 2. What is the error?", "Forgot to subtract 9: it equals (x + 3)² - 7",
     ["No error", "Should be (x + 6)² + 2", "Should be (x + 3)² + 11"], ["(x + 3)² = x² + 6x + 9, which adds 9.", "Subtract 9 to keep the expression equal: (x + 3)² - 7."], tags=["error-analysis"])
B.sa(S, "cp1", "Write the quadratic in intercept form with zeros -2 and 6 that passes through (2, -32).", "y = 2(x + 2)(x - 6)",
     ["y = a(x + 2)(x - 6).", "-32 = a(4)(-4) → a = 2."])
B.sa(S, "honors", "Convert y = -3x² + 12x - 5 to vertex form and state the range.", "y = -3(x - 2)² + 7; y ≤ 7",
     ["-3(x² - 4x) - 5 = -3[(x - 2)² - 4] - 5 = -3(x - 2)² + 7.", "Opens down with maximum 7."])
B.sa(S, "honors", "Write y = 2x² + 6x + 1 in vertex form.", "y = 2(x + 3/2)² - 7/2",
     ["2(x² + 3x) + 1 = 2[(x + 3/2)² - 9/4] + 1.", "= 2(x + 3/2)² - 9/2 + 1 = 2(x + 3/2)² - 7/2."])
B.mc(S, "honors", "y = a(x - 1)(x - 7) has a maximum value of 18. What is a?", "-2", ["2", "-1/2", "-18"],
     ["Vertex x = 4; y = a(3)(-3) = -9a.", "-9a = 18 → a = -2 (negative, so a maximum)."], tags=["challenge"])
B.orq(S, "honors", "f(x) = x² + bx + c has vertex (h, k).",
      [("Express h in terms of b.", "h = -b/2"), ("Express k in terms of b and c.", "k = c - b²/4"),
       ("If the vertex is (3, -4), find b and c.", "b = -6, c = 5"), ("Find the zeros in that case.", "x = 1 and x = 5")],
      ["h = -b/(2·1).", "k = f(h) = b²/4 - b²/2 + c.", "b = -6; -4 = c - 9 → c = 5.", "x² - 6x + 5 = (x - 1)(x - 5)."], tags=["challenge"])

# ---------------- Skill 3: factoring ----------------
S = 3
for r1, r2 in [(2, 5), (-3, 7), (-4, -6), (1, -9), (8, -2)]:
    f = sp.expand((x - r1)*(x - r2))
    B.sa(S, "cp2", f"Factor {fmt(f, x)}.", fmt(sp.factor(f)),
         [f"Find two numbers with product {r1*r2} and sum {-(r1 + r2)}: {-r1} and {-r2}.", f"{fmt(sp.factor(f))}."])
for e in [6*x**2 + 7*x - 3, 4*x**2 - 4*x - 15, 3*x**2 - 10*x + 8, 10*x**2 + 11*x - 6]:
    a, b, c = sp.Poly(e, x).all_coeffs()
    B.sa(S, "cp1", f"Factor completely: {fmt(e, x)}.", fmt(sp.factor(e)),
         [f"ac = {a*c}; find two factors of {a*c} that add to {b}.", "Split the middle term and factor by grouping.", f"{fmt(sp.factor(e))}."])
for e, ans_wrong in [(x**2 - 49, ["(x - 7)²", "(x + 7)²", "(x - 49)(x + 1)"]), (9*x**2 - 25, ["(9x - 5)(x + 5)", "(3x - 5)²", "(3x - 25)(3x + 1)"]),
                     (x**2 + 10*x + 25, ["(x + 5)(x - 5)", "(x + 10)(x + 1)", "(x + 25)(x + 1)"]), (4*x**2 - 12*x + 9, ["(4x - 3)(x - 3)", "(2x + 3)²", "(2x - 9)(2x - 1)"])]:
    B.mc(S, "cp2", f"Factor {fmt(e, x)}.", fmt(sp.factor(e)), ans_wrong, ["Recognize a special pattern: a² - b² = (a - b)(a + b) or a² ± 2ab + b² = (a ± b)².", f"{fmt(sp.factor(e))}."])
for e in [2*x**3 - 18*x, 3*x**2 + 12*x - 36, x**4 - 16, 5*x**3 + 10*x**2 - 40*x]:
    B.sa(S, "cp1", f"Factor completely: {fmt(e, x)}.", fmt(sp.factor(e)),
         ["Factor out the greatest common factor first.", "Then factor what remains; check whether any factor can be factored again.", f"{fmt(sp.factor(e))}."])
B.mc(S, "cp1", "A student factors 2x² - 8 as (2x - 4)(x + 2). What is correct?", "2(x - 2)(x + 2)", ["Correct as written", "(2x - 8)(x + 1)", "2(x - 4)²"],
     ["(2x - 4)(x + 2) = 2x² - 8 is true, but it is not completely factored: 2x - 4 = 2(x - 2).", "Complete factorization: 2(x - 2)(x + 2)."], tags=["error-analysis"])
B.sel(S, "cp1", "Select ALL expressions that are prime (cannot be factored over the integers).", ["x² + 4", "x² + x + 1", "2x² + 3x + 4"],
      ["x² - 4", "x² + 5x + 6", "4x² - 1"], ["Sum of squares x² + 4 does not factor over the reals.", "Discriminants of x² + x + 1 and 2x² + 3x + 4 are negative.", "The others are a difference of squares or factor as (x + 2)(x + 3)."])
for e, res in [(x**2*y**2 - 9, "(xy - 3)(xy + 3)"), (x**4 - 5*x**2 + 4, "(x - 1)(x + 1)(x - 2)(x + 2)"), (x**3 + 2*x**2 - 9*x - 18, "(x - 3)(x + 3)(x + 2)")]:
    assert sp.expand(sp.factor(e) - sp.parse_expr(res.replace("xy", "x*y"), transformations="all")) == 0
    B.sa(S, "honors", f"Factor completely: {fmt(e)}.", res,
         ["Look for structure: treat a group as a single variable (u-substitution) or group terms in pairs.", f"{res}."], tags=["challenge"])
B.sa(S, "honors", "Find all integers b so that x² + bx + 12 factors over the integers.", "b = ±7, ±8, ±13",
     ["Factor pairs of 12: (1, 12), (2, 6), (3, 4) and their negatives.", "Sums: ±13, ±8, ±7."], tags=["reasoning"])
B.orq(S, "honors", "Use the expression 3x³ - 12x² - 15x.",
      [("Factor out the GCF.", "3x(x² - 4x - 5)"), ("Factor completely.", "3x(x - 5)(x + 1)"),
       ("Solve 3x³ - 12x² - 15x = 0.", "x = 0, 5, -1"), ("Explain why dividing both sides by x first loses a solution.", "x = 0 is a solution; dividing by x assumes x ≠ 0")],
      ["GCF 3x.", "x² - 4x - 5 = (x - 5)(x + 1).", "Zero-product property.", "Division by a variable can discard x = 0."], tags=["error-analysis"])

# ---------------- Skill 4: square roots & completing the square ----------------
S = 4
for a, k in [(1, 49), (2, 50), (3, 75), (1, 20), (4, 9)]:
    sols = sp.solve(a*x**2 - k, x)
    B.sa(S, "cp2", f"Solve {a if a != 1 else ''}x² = {k}.", "x = ±" + fmt(sols[1] if sols[1] > 0 else sols[0]),
         [f"Divide by {a}: x² = {num(F(k, a))}." if a != 1 else "Take the square root of both sides.", "Include both the positive and negative roots.", "x = ±" + fmt(sols[1] if sols[1] > 0 else sols[0]) + "."])
for h, k in [(3, 16), (-2, 5), (1, 18), (-5, 0)]:
    sols = sp.solve((x - h)**2 - k, x); s = roots_txt(sols)
    B.sa(S, "cp2", f"Solve {fmt((x - h)**2)} = {k}.", s, ["Take square roots: x - h = ±√k.", f"Solutions: {s}."])
for b, c in [(6, -7), (-8, 3), (4, -1), (10, 13), (-2, -6)]:
    sols = sp.solve(x**2 + b*x + c, x); s = roots_txt(sols)
    B.sa(S, "cp1", f"Solve x² {'+' if b > 0 else '-'} {abs(b)}x {'+' if c > 0 else '-'} {abs(c)} = 0 by completing the square.", s,
         [f"Move the constant: x² {'+' if b > 0 else '-'} {abs(b)}x = {-c}.", f"Add (b/2)² = {b*b//4} to both sides: (x {'+' if b > 0 else '-'} {abs(b)//2})² = {-c + b*b//4}.",
          f"Take square roots and solve: {s}."])
for a, b, c in [(2, -8, 3), (3, 6, -1), (4, -4, -7)]:
    sols = sp.solve(a*x**2 + b*x + c, x); s = roots_txt(sols)
    B.sa(S, "honors", f"Solve {fmt(a*x**2 + b*x + c, x)} = 0 by completing the square. Give exact answers.", s,
         [f"Divide by {a} so the leading coefficient is 1.", "Move the constant, then add (b/2)² to both sides.", f"Square-root both sides and simplify: {s}."])
B.mc(S, "cp1", "A student solves x² = 36 and writes x = 6. What is missing?", "x = -6 is also a solution", ["Nothing", "x = 18", "x = ±36"],
     ["(-6)² = 36 too.", "Taking a square root of both sides of an equation gives ± solutions."], tags=["error-analysis"])
B.mc(S, "cp1", "What number completes the square for x² - 14x?", "49", ["196", "-49", "7"], ["(b/2)² = (-14/2)² = 49."])
B.sa(S, "cp1", "A square garden has area 72 ft². Find its side length exactly and to the nearest tenth.", "6√2 ft ≈ 8.5 ft",
     ["s² = 72 → s = √72 (length is positive).", "√72 = √(36·2) = 6√2 ≈ 8.49."], tags=["modeling"])
B.sa(S, "honors", "Solve x² + bx + c = 0 by completing the square to derive a formula for x in terms of b and c.", "x = (-b ± √(b² - 4c))/2",
     ["x² + bx = -c.", "x² + bx + b²/4 = b²/4 - c → (x + b/2)² = (b² - 4c)/4.", "x = -b/2 ± √(b² - 4c)/2."], tags=["connections", "challenge"])
B.orq(S, "honors", "An object is dropped from 144 ft; its height is h(t) = 144 - 16t².",
      [("When is it 80 ft high?", "t = 2 s"), ("When does it hit the ground?", "t = 3 s"), ("Why is the negative root rejected?", "Time cannot be negative here"),
       ("Find the average speed during the fall.", "48 ft/s")],
      ["16t² = 64 → t = 2.", "16t² = 144 → t = 3.", "t ≥ 0 after release.", "144 ft / 3 s."], tags=["modeling"])

# ---------------- Skill 5: quadratic formula & discriminant ----------------
S = 5
for a, b, c in [(1, 3, -10), (2, -3, -2), (1, -4, 1), (3, 5, 1), (1, 2, -1)]:
    sols = sp.solve(a*x**2 + b*x + c, x); d = b*b - 4*a*c
    s = roots_txt(sols)
    B.sa(S, "cp2" if sp.sqrt(d).is_integer else "cp1", f"Use the quadratic formula to solve {fmt(a*x**2 + b*x + c, x)} = 0.", s,
         [f"a = {a}, b = {b}, c = {c}; b² - 4ac = {d}.", f"x = ({-b} ± √{d})/{2*a}.", s + "."])
for a, b, c in [(1, -6, 9), (2, 3, 5), (1, 1, -6), (4, -12, 9), (3, -2, -1), (1, 0, 4)]:
    d = b*b - 4*a*c; kind = "two real solutions" if d > 0 else ("one real solution" if d == 0 else "two complex (non-real) solutions")
    B.mc(S, "cp2", f"Use the discriminant to describe the solutions of {fmt(a*x**2 + b*x + c, x)} = 0.", kind.capitalize(),
         [k.capitalize() for k in ["two real solutions", "one real solution", "two complex (non-real) solutions", "no solutions at all"] if k != kind][:3],
         [f"b² - 4ac = {b*b} - {4*a*c} = {d}.", "Positive → two real; zero → one real (double root); negative → two non-real complex conjugates."])
B.mc(S, "cp1", "A student applies the formula to 2x² - 5x + 1 = 0 and writes x = (-5 ± √17)/4. What is the error?", "The sign of b: it should be (5 ± √17)/4",
     ["The discriminant should be 33", "The denominator should be 2", "No error"], ["-b = -(-5) = 5."], tags=["error-analysis"])
for kq in [("x² + kx + 9 = 0 has exactly one real solution", "k = ±6", "k² - 36 = 0."), ("x² - 4x + k = 0 has two real solutions", "k < 4", "16 - 4k > 0."),
           ("kx² + 6x + 3 = 0 has no real solutions", "k > 3", "36 - 12k < 0 (and k ≠ 0).")]:
    B.sa(S, "honors" if "kx²" in kq[0] else "cp1", f"Find all k such that {kq[0]}.", kq[1], ["Use the discriminant b² - 4ac.", kq[2], kq[1] + "."], tags=["reasoning"])
B.sel(S, "cp1", "Select ALL equations with two distinct rational solutions.", ["x² - 5x + 6 = 0", "6x² + x - 2 = 0", "x² - 9 = 0"],
      ["x² - 2 = 0", "x² + 2x + 1 = 0", "x² + x + 1 = 0"], ["A perfect-square positive discriminant gives rational roots.", "1, 49, 36 are perfect squares; 8 is not; 0 gives one root; -3 gives complex."])
B.sa(S, "cp1", "A ball's height is h = -4.9t² + 20t + 1.5 (m). When does it land? Round to the nearest hundredth.", "t ≈ 4.15 s",
     ["Solve -4.9t² + 20t + 1.5 = 0.", "t = (-20 - √(400 + 29.4))/(-9.8) ≈ 4.155… → 4.15 (rounded to the nearest hundredth; the other root is negative)."], tags=["modeling"])
r = max(sp.solve(-4.9*t**2 + 20*t + 1.5, t)); assert abs(r - 4.1525) < 0.01, r
B.qs[-1]["answer"] = f"t ≈ {float(r):.2f} s"; B.qs[-1]["solutionSteps"][1] = f"t = (-20 - √(400 + 29.4))/(-9.8) ≈ {float(r):.3f}; reject the negative root."
B.sa(S, "honors", "Prove that if a and c have opposite signs, ax² + bx + c = 0 always has two real solutions.", "b² - 4ac > 0",
     ["If a and c have opposite signs, ac < 0, so -4ac > 0.", "b² ≥ 0, so b² - 4ac > 0."], tags=["reasoning", "challenge"])
B.sa(S, "honors", "The solutions of x² + bx + c = 0 are 3 + √2 and 3 - √2. Find b and c.", "b = -6, c = 7",
     ["Sum of roots = -b = 6 → b = -6.", "Product = c = 9 - 2 = 7."], tags=["connections"])
B.orq(S, "honors", "Consider f(x) = x² - 2x + k.",
      [("For what k does f have two x-intercepts?", "k < 1"), ("For k = 1 describe the graph.", "Vertex (1, 0) touches the x-axis"),
       ("For k = -3 find the zeros.", "x = 3 and x = -1"), ("For k = 5 solve f(x) = 0.", "x = 1 ± 2i")],
      ["4 - 4k > 0.", "f = (x - 1)².", "x² - 2x - 3 = (x - 3)(x + 1).", "x = (2 ± √(4 - 20))/2 = 1 ± 2i."], tags=["connections"])

# ---------------- Skill 6: complex numbers & arithmetic ----------------
S = 6
for z, w, op in [((3, 2), (1, -5), "+"), ((4, -1), (-2, 3), "-"), ((2, 3), (4, -1), "×"), ((1, -2), (3, 4), "×"), ((-5, 4), (5, 4), "+"), ((2, 1), (2, -1), "×")]:
    Z = z[0] + z[1]*I; W = w[0] + w[1]*I
    r = sp.expand(Z + W if op == "+" else (Z - W if op == "-" else Z*W))
    B.sa(S, "cp2" if op != "×" else "cp1", (f"Simplify ({fmt(Z)})({fmt(W)})." if op == "×" else f"Simplify ({fmt(Z)}) {op} ({fmt(W)})."), fmt(r),
         ["Combine real parts and imaginary parts separately." if op != "×" else "Use FOIL, then replace i² with -1.", f"Result: {fmt(r)}."])
for k, ans in [(2, "-1"), (3, "-i"), (4, "1"), (17, "i"), (26, "-1"), (99, "-i")]:
    B.mc(S, "cp2" if k < 10 else "cp1", f"Simplify i^{k}.", ans, [a for a in ["1", "-1", "i", "-i"] if a != ans],
         [f"Powers of i repeat every 4: i, -1, -i, 1.", f"{k} ÷ 4 leaves remainder {k % 4}, so i^{k} = i^{k % 4} = {ans}."])
for r in [-25, -12, -50]:
    B.sa(S, "cp2", f"Write √({r}) in terms of i.", fmt(sp.sqrt(r)), [f"√({r}) = √{-r}·√(-1) = {fmt(sp.sqrt(-r))}i.".replace("√1", "")])
for Z, W in [((3, 4), (1, 2)), ((5, -1), (2, 3)), ((1, 1), (1, -1))]:
    z = Z[0] + Z[1]*I; w = W[0] + W[1]*I; q = sp.simplify(sp.expand(z*sp.conjugate(w))/(sp.expand(w*sp.conjugate(w))))
    q = sp.nsimplify(sp.re(q)) + sp.nsimplify(sp.im(q))*I
    B.sa(S, "honors" if Z != (1, 1) else "cp1", f"Divide and write in a + bi form: ({fmt(z)})/({fmt(w)}).", fmt(q),
         [f"Multiply numerator and denominator by the conjugate {fmt(sp.conjugate(w))}.", f"Denominator: {fmt(sp.expand(w*sp.conjugate(w)))}.", f"Result: {fmt(q)}."])
B.mc(S, "cp1", "A student writes √(-4)·√(-9) = √36 = 6. What is correct?", "-6, because 2i·3i = 6i² = -6", ["6", "6i", "-6i"],
     ["√a·√b = √(ab) is not valid when both a and b are negative.", "Write each in terms of i first."], tags=["error-analysis", "misconception"])
B.sel(S, "cp1", "Select ALL true statements.", ["The conjugate of 3 - 7i is 3 + 7i", "(2 + i)(2 - i) = 5", "i² = -1"],
      ["The conjugate of 3 - 7i is -3 + 7i", "|3 + 4i| = 7", "√(-16) = -4"],
      ["Conjugate changes only the sign of the imaginary part.", "(2 + i)(2 - i) = 4 - i² = 5.", "|3 + 4i| = 5; √(-16) = 4i."])
B.sa(S, "honors", "Find real x and y with (2x - 3) + (y + 1)i = 7 - 4i.", "x = 5, y = -5", ["Equal complex numbers have equal real and imaginary parts.", "2x - 3 = 7 → x = 5; y + 1 = -4 → y = -5."])
B.sa(S, "honors", "Compute (1 + i)⁸.", "16", ["(1 + i)² = 2i.", "(2i)⁴ = 16i⁴ = 16."], tags=["challenge"])
B.orq(S, "honors", "Let z = 3 + 4i.",
      [("Find the conjugate z̄.", "3 - 4i"), ("Find z·z̄.", "25"), ("Find |z|.", "5"), ("Find 1/z in a + bi form.", "3/25 - 4i/25")],
      ["Negate the imaginary part.", "9 + 16 = 25.", "|z| = √25.", "1/z = z̄/(z z̄)."], tags=["connections"])

# ---------------- Skill 7: quadratic equations with complex solutions ----------------
S = 7
for a, b, c in [(1, 0, 16), (1, 2, 5), (1, -4, 13), (2, 0, 18), (1, 6, 10), (1, -2, 10)]:
    sols = sp.solve(a*x**2 + b*x + c, x); s = roots_txt(sols)
    B.sa(S, "cp2" if b == 0 else "cp1", f"Solve {fmt(a*x**2 + b*x + c, x)} = 0 over the complex numbers.", s,
         [f"Discriminant b² - 4ac = {b*b - 4*a*c} < 0.", "√(negative) = i·√(positive).", s + "."])
for a, b, c in [(2, -2, 5), (3, 2, 1), (4, 4, 5)]:
    sols = sp.solve(a*x**2 + b*x + c, x); s = roots_txt(sols)
    B.sa(S, "honors", f"Solve {fmt(a*x**2 + b*x + c, x)} = 0. Write the solutions in a + bi form.", s,
         [f"x = ({-b} ± √({b*b - 4*a*c}))/{2*a}.", "Separate real and imaginary parts.", s + "."])
B.mc(S, "cp1", "One solution of a quadratic with real coefficients is 4 - 3i. What is the other?", "4 + 3i", ["-4 + 3i", "-4 - 3i", "3 - 4i"],
     ["Non-real solutions of real-coefficient quadratics come in conjugate pairs."])
for r in [(2, 3), (-1, 1), (0, 5)]:
    z = r[0] + r[1]*I; p = sp.expand((x - z)*(x - sp.conjugate(z)))
    B.sa(S, "honors", f"Write a quadratic equation with integer coefficients whose solutions are {fmt(z)} and {fmt(sp.conjugate(z))}.", f"{fmt(p, x)} = 0",
         ["Sum of roots: " + fmt(2*r[0]) + "; product: " + fmt(r[0]**2 + r[1]**2) + ".", "x² - (sum)x + (product) = 0.", f"{fmt(p, x)} = 0."], tags=["challenge"])
B.mc(S, "cp1", "Which quadratic graph has no x-intercepts?", "y = x² + 4x + 7", ["y = x² + 4x + 4", "y = x² + 4x + 3", "y = -x² + 4x + 7"],
     ["No x-intercepts ↔ negative discriminant.", "16 - 28 = -12 < 0."], tags=["connections"])
dg = graph(B, "s07-no-zeros", [(lambda v: (v - 2)**2 + 1, {})], points=[(2, 1, True, "(2, 1)"), (1, 2), (3, 2)],
           alt="An upward parabola with vertex (2, 1), passing through (1, 2) and (3, 2); it never touches the x-axis.")
B.sa(S, "cp1", "The graph shows y = x² - 4x + 5. Explain what the graph tells you about the solutions of x² - 4x + 5 = 0, then find them.", "No real solutions; x = 2 ± i",
     ["The graph never meets the x-axis, so there are no real zeros.", "x = (4 ± √(16 - 20))/2 = 2 ± i."], diagram=dg, tags=["graph", "connections"])
B.sel(S, "cp1", "Select ALL equations with non-real solutions.", ["x² + 9 = 0", "x² - 2x + 2 = 0", "2x² + x + 1 = 0"], ["x² - 9 = 0", "x² - 2x + 1 = 0", "x² + x - 1 = 0"],
      ["Check b² - 4ac < 0: -36, -4, -7.", "The others give 36, 0, 5."])
B.mc(S, "honors", "A student solves x² + 6x + 13 = 0 and gets x = -3 ± 4i. What is the error?", "√(-16)/2 = 2i, so x = -3 ± 2i", ["No error; the answer is correct", "x = 3 ± 2i", "x = -3 ± 16i"],
     ["x = (-6 ± √(36 - 52))/2 = (-6 ± 4i)/2.", "Divide both terms by 2: -3 ± 2i."], tags=["error-analysis"])
B.orq(S, "honors", "Explore x² + 4 = 0 and x² - 4 = 0.",
      [("Solve x² - 4 = 0 by factoring.", "x = ±2"), ("Solve x² + 4 = 0.", "x = ±2i"),
       ("Factor x² + 4 over the complex numbers.", "(x - 2i)(x + 2i)"), ("Check your factorization by multiplying.", "x² - (2i)² = x² + 4")],
      ["(x - 2)(x + 2).", "x² = -4.", "Difference of squares with 2i.", "(2i)² = -4."], tags=["connections"])

# ---------------- Skill 8: quadratic modeling ----------------
S = 8
for v0, h0 in [(64, 0), (48, 6), (80, 4)]:
    tmax = F(v0, 32); hmax = -16*tmax**2 + v0*tmax + h0
    B.sa(S, "cp1", f"A ball is launched with h(t) = -16t² + {v0}t + {h0}".replace(" + 0", "") + " feet. Find the maximum height and when it occurs.", f"{num(hmax)} ft at t = {num(tmax)} s",
         [f"t = -b/(2a) = {v0}/32 = {num(tmax)}.", f"h({num(tmax)}) = {num(hmax)}."], tags=["modeling"])
B.mc(S, "cp2", "In h(t) = -16t² + 32t + 5, what does 5 represent?", "The initial height (5 ft)", ["The maximum height", "The time in the air", "The initial velocity"],
     ["h(0) = 5."], tags=["modeling"])
B.mc(S, "cp2", "A rectangle's length is 3 more than its width, and its area is 40 m². Which equation finds the width w?", "w(w + 3) = 40", ["w + (w + 3) = 40", "2w + 2(w + 3) = 40", "w² + 3 = 40"],
     ["Area = length × width."], tags=["modeling"])
B.sa(S, "cp2", "A rectangle's length is 3 more than its width, and its area is 40 m². Find the dimensions.", "5 m by 8 m",
     ["w² + 3w - 40 = 0 → (w + 8)(w - 5) = 0.", "w = 5 (positive), length 8."], tags=["modeling"])
B.sa(S, "cp1", "Profit is P(x) = -2x² + 120x - 1000 dollars for x items. Find the break-even quantities and the maximum profit.", "x = 10 and x = 50; $800 at x = 30",
     ["-2(x² - 60x + 500) = -2(x - 10)(x - 50).", "Vertex x = 30: P = -1800 + 3600 - 1000 = 800."], tags=["modeling"])
B.sa(S, "cp1", "A uniform walkway surrounds a 10 m by 6 m garden. Together they cover 140 m². How wide is the walkway?", "2 m",
     ["(10 + 2w)(6 + 2w) = 140.", "4w² + 32w + 60 = 140 → w² + 8w - 20 = 0 → (w + 10)(w - 2) = 0.", "w = 2 (width is positive)."], tags=["modeling"])
B.mc(S, "cp1", "Data: (0, 10), (1, 25), (2, 30), (3, 25), (4, 10). Which model fits exactly?", "y = -5x² + 20x + 10", ["y = 5x² + 20x + 10", "y = -5(x - 2)² + 10", "y = -10x² + 25x + 10"],
     ["Symmetric about x = 2 with maximum 30: y = a(x - 2)² + 30.", "At x = 0: 4a + 30 = 10 → a = -5.", "Expand: -5x² + 20x + 10."], tags=["modeling", "multiple-representations"])
B.sel(S, "cp1", "h(t) = -5t² + 30t models a ball's height in meters. Select ALL true statements.", ["The ball lands at t = 6 s", "The maximum height is 45 m", "The ball is at 25 m twice"],
      ["The maximum is at t = 6 s", "The ball starts at 30 m"], ["-5t(t - 6) = 0 → t = 0, 6.", "Vertex t = 3: h = 45.", "25 < 45, so two times (t = 1 and t = 5).", "Starts at h(0) = 0."], tags=["modeling"])
B.sa(S, "honors", "A theater charges $20 per ticket and sells 600 tickets. Each $1 increase loses 20 sales. What price maximizes revenue, and what is the maximum revenue?", "$25; $12,500",
     ["R(x) = (20 + x)(600 - 20x) = -20x² + 200x + 12000.", "Vertex x = 5 → price $25.", "R = 25·500 = 12,500."], tags=["modeling"])
B.sa(S, "honors", "Find two numbers whose sum is 30 and whose product is as large as possible. Then find two numbers whose difference is 30 and whose product is as small as possible.", "15 and 15; 15 and -15",
     ["Sum: P = x(30 - x), vertex x = 15 → 225.", "Difference: P = x(x - 30), vertex x = 15 → numbers 15 and -15, product -225."], tags=["challenge"])
B.orq(S, "honors", "A bridge arch is a parabola 40 m wide at the base and 16 m high at the center. Place the origin at the left base.",
      [("Write an equation for the arch.", "y = -0.04x(x - 40)"), ("How high is the arch 5 m from either base?", "7 m"),
       ("Can a 10-m-tall truck pass if its 8-m width is centered?", "Yes: at x = 16, y = 15.36 m"), ("Where is the arch exactly 12 m high?", "x = 10 and x = 30")],
      ["y = a x(x - 40); at (20, 16): 16 = a(20)(-20) → a = -0.04.", "y(5) = -0.04·5·(-35) = 7.", "Edge of the truck at x = 16: -0.04·16·(-24) = 15.36 > 10.",
       "-0.04x(x - 40) = 12 → x² - 40x + 300 = 0 → x = 10, 30."], tags=["modeling", "multistep"])
for v in [(5, 7), (16, 15.36)]:
    assert abs(-0.04*v[0]*(v[0] - 40) - v[1]) < 1e-9

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
