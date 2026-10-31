from lib import *

STD = {1: ["F-IF.A.2"], 2: ["F-IF.A.1", "F-IF.B.5"], 3: ["F-BF.A.1b", "F-BF.A.1c"],
       4: ["F-BF.B.4a", "F-BF.B.4c"], 5: ["F-BF.B.3"], 6: ["F-IF.C.7b"], 7: ["F-BF.B.3"],
       8: ["F-BF.A.1", "F-IF.B.4"]}
B = Bank("functions-transformations", "ft", STD)

# ---------------- Skill 1: function notation & evaluation ----------------
S = 1
for a, b, c, k in [(2, -3, 1, -2), (-1, 4, 5, 3), (3, 0, -7, -1), (1, -6, 9, 4), (-2, 1, 0, -3)]:
    f = a*x**2 + b*x + c; v = f.subs(x, k)
    B.sa(S, "cp2", f"Let f(x) = {fmt(f, x)}. Find f({k}).", int(v),
         [f"Substitute {k} for every x: f({k}) = {a}({k})² + {b}({k}) + {c}.".replace("+ -", "- "),
          f"({k})² = {k*k}, so f({k}) = {a*k*k} + {b*k} + {c} = {v}."])
for a, k in [(-1, -3), (-2, -4), (-1, 5)]:
    f = a*x**2 + 1; v = f.subs(x, k); wrong = (-a*k*k) + 1
    B.mc(S, "cp2", f"If g(x) = {fmt(f, x)}, what is g({k})?", v, [wrong, a*k*2 + 1, -v],
         [f"Square the input first: ({k})² = {k*k}.", f"Then multiply by {a} and add 1: {a}·{k*k} + 1 = {v}.",
          "A common error is squaring the coefficient together with the input, which flips the sign."],
         tags=["misconception"])
# from a graph
dg = graph(B, "s01-graph-eval", [(lambda v: 0.5*(v-1)**2 - 3, {})], points=[(1, -3, True, "(1, -3)"), (3, -1), (-1, -1), (5, 5)],
           alt="Parabola opening up with vertex (1, -3), passing through (-1, -1), (3, -1), and (5, 5).")
for q, ans, st in [("f(3)", -1, "Locate x = 3 on the graph; the point is (3, -1)."),
                   ("f(5)", 5, "The point at x = 5 is (5, 5)."),
                   ("the values of x for which f(x) = -1", "x = -1 and x = 3", "Find where the graph has height -1: the points (-1, -1) and (3, -1).")]:
    B.sa(S, "cp2" if "values" not in q else "cp1", f"Use the graph of y = f(x). Find {q}.", ans,
         [st, "f(x) means the y-coordinate of the graph at that x-value."], diagram=dg, tags=["graph"])
# expressions as inputs
for f, inp in [(x**2 - 2*x, x + 3), (3*x**2 + x, 2*x), (x**2 + 4, x - 1), (2*x**2 - 5*x + 1, -x)]:
    r = sp.expand(f.subs(x, inp))
    B.sa(S, "cp1", f"Let f(x) = {fmt(f, x)}. Find and simplify f({fmt(inp, x)}).", fmt(r, x),
         [f"Replace every x in the rule with the whole expression ({fmt(inp, x)}).",
          "Expand any squared binomials first, then distribute coefficients.", f"Combine like terms: {fmt(r, x)}."])
# solve f(x) = k
for f, k in [(3*x - 7, 11), (x**2 - 5, 20), (2*x**2 + 3, 75), (-4*x + 9, -15), (x**2 + 2*x, 15)]:
    sols = sorted(sp.solve(sp.Eq(f, k), x)); txt = " or ".join(f"x = {s}" for s in sols)
    B.sa(S, "cp1", f"For f(x) = {fmt(f, x)}, find all x such that f(x) = {k}.", txt,
         [f"Set the rule equal to {k}: {fmt(f, x)} = {k}.", f"Solve: {txt}.",
          "Check by substituting each value back into f."])
# table composition
B.mc(S, "cp1", "The table shows values of h: h(-1) = 4, h(0) = 2, h(2) = -1, h(4) = 0. What is h(h(0))?", "-1",
     ["2", "0", "4"], ["Work from the inside out: h(0) = 2.", "Then h(h(0)) = h(2) = -1."], tags=["multiple-representations"])
B.mc(S, "cp1", "The table shows values of h: h(-1) = 4, h(0) = 2, h(2) = -1, h(4) = 0. For what input is h(x) = 0?", "x = 4",
     ["x = 0", "x = 2", "x = -1"], ["h(x) = 0 asks for the input whose output is 0.", "The table gives h(4) = 0, so x = 4."],
     tags=["misconception"])
# context
B.mc(S, "cp1", "C(m) gives the cost, in dollars, of a phone plan that uses m gigabytes of data. What does C(8) = 55 mean?",
     "Using 8 gigabytes of data costs $55.", ["Using 55 gigabytes costs $8.", "The cost rises $8 for every 55 gigabytes.",
     "Each gigabyte costs $55."], ["The input m is gigabytes and the output C(m) is cost.", "So C(8) = 55 pairs 8 GB with a cost of $55."],
     tags=["modeling"])
B.mc(S, "cp2", "T(h) is the temperature, in °F, h hours after sunrise. Which statement means 'Two hours after sunrise the temperature is 61°F'?",
     "T(2) = 61", ["T(61) = 2", "T = 2(61)", "2T = 61"], ["The input is the number of hours, 2.", "The output is the temperature, 61, so T(2) = 61."],
     tags=["modeling"])
# honors: difference quotient
for f in [x**2 + 3*x, 2*x**2 - x + 4, -x**2 + 5, x**3]:
    h = sp.Symbol("h"); dq = sp.simplify(sp.expand(f.subs(x, x + h) - f) / h)
    P = lambda e: fmt_terms(e, x, h)
    B.sa(S, "honors", f"For f(x) = {fmt(f, x)}, find and simplify the difference quotient (f(x + h) - f(x))/h, h ≠ 0.", P(dq),
         [f"f(x + h) = {P(f.subs(x, x + h))}.", f"f(x + h) - f(x) = {P(f.subs(x, x + h) - f)}.",
          f"Every term has a factor of h; divide by h: {P(dq)}."], tags=["challenge"])
B.mc(S, "honors", "A student says: 'If f(x) = x² + 1, then f(a + b) = f(a) + f(b).' Which value shows the claim is false?",
     "a = 1, b = 1: f(2) = 5 but f(1) + f(1) = 4", ["a = 0, b = 0: both sides equal 1",
     "a = 1, b = -1: both sides equal 2", "a = 2, b = 0: f(2) = 5 and f(2) + f(0) = 5"],
     ["Test a = 1, b = 1: f(2) = 4 + 1 = 5.", "f(1) + f(1) = 2 + 2 = 4, and 5 ≠ 4, so function notation does not distribute.",
      "Check the distractors: a = b = 0 gives 1 vs 2, a = 1, b = -1 gives 1 vs 4, a = 2, b = 0 gives 5 vs 6, so none of them is a correct description."],
     tags=["error-analysis", "reasoning"])
B.sel(S, "honors", "Let f(x) = 2x - 3. Select ALL statements that are true.",
      ["f(5) = 7", "f(x + 1) = 2x - 1", "f(a) = 0 when a = 3/2"], ["f(2x) = 2f(x)", "f(-x) = -f(x)"],
      ["f(5) = 10 - 3 = 7 (true).", "f(x + 1) = 2x + 2 - 3 = 2x - 1 (true).", "2a - 3 = 0 gives a = 3/2 (true).",
       "f(2x) = 4x - 3 but 2f(x) = 4x - 6 (false).", "f(-x) = -2x - 3 but -f(x) = -2x + 3 (false)."], tags=["reasoning"])
B.orq(S, "honors", "A ball's height in feet t seconds after it is thrown is H(t) = -16t² + 48t + 6.",
      [("Find H(0) and explain its meaning.", "6; the ball is released 6 ft above the ground"),
       ("Find H(1.5).", "42 ft"),
       ("Solve H(t) = 38.", "t = 1 or t = 2"),
       ("Explain why H(t) = 38 has two solutions in context.", "The ball passes 38 ft once going up (t = 1) and once coming down (t = 2)")],
      ["H(0) = 6.", "H(1.5) = -16(2.25) + 72 + 6 = -36 + 78 = 42.", "-16t² + 48t + 6 = 38 → -16t² + 48t - 32 = 0 → t² - 3t + 2 = 0 → t = 1, 2.",
       "A parabola opening down reaches each height below its maximum (42 ft) twice."], tags=["modeling", "multistep"])
B.orq(S, "cp1", "Let f(x) = x² - 4x and g(x) = 3 - x.",
      [("Find f(-1).", 5), ("Find g(f(-1)).", -2), ("Find f(a + 2) in simplest form.", "a² - 4"), ("Find all x with f(x) = 5.", "x = -1 or x = 5")],
      ["f(-1) = 1 + 4 = 5.", "g(5) = 3 - 5 = -2.", "f(a + 2) = a² + 4a + 4 - 4a - 8 = a² - 4.", "x² - 4x - 5 = 0 → (x - 5)(x + 1) = 0."], tags=["multistep"])

# ---------------- Skill 2: domain and range ----------------
S = 2
for expr, dom, st in [("√(x - 4)", "x ≥ 4", "The radicand must be nonnegative: x - 4 ≥ 0."),
                      ("1/(x + 6)", "all real x except x = -6", "The denominator cannot be 0: x + 6 ≠ 0."),
                      ("√(10 - 2x)", "x ≤ 5", "10 - 2x ≥ 0 gives x ≤ 5."),
                      ("∛(x + 1)", "all real numbers", "Cube roots of negative numbers are real, so there is no restriction."),
                      ("(x + 2)/(x² - 9)", "all real x except x = 3 and x = -3", "x² - 9 = 0 when x = ±3.")]:
    B.sa(S, "cp2", f"State the domain of f(x) = {expr}.", dom, [st, f"Domain: {dom}."])
for expr, rng, wrong, st in [("x² + 3", "y ≥ 3", ["y ≤ 3", "all real numbers", "y ≥ 0"], "x² ≥ 0, so x² + 3 ≥ 3."),
                             ("-2(x - 1)² + 5", "y ≤ 5", ["y ≥ 5", "y ≤ 1", "all real numbers"], "The parabola opens down with vertex (1, 5)."),
                             ("√x - 4", "y ≥ -4", ["y ≥ 4", "y ≥ 0", "x ≥ 0"], "√x ≥ 0, so √x - 4 ≥ -4."),
                             ("|x + 2| - 1", "y ≥ -1", ["y ≥ 2", "y ≥ -2", "y ≤ -1"], "|x + 2| ≥ 0, so the output is at least -1.")]:
    B.mc(S, "cp2", f"What is the range of f(x) = {expr}?", rng, wrong, [st, f"Range: {rng}."])
dg = graph(B, "s02-dr-graph", [(lambda v: v + 1 if v < 1 else np.nan, {"_dom": (-4, 1)}), (lambda v: -v + 4, {"_dom": (1, 5)})],
           points=[(-4, -3, True), (1, 2, False), (1, 3, True), (5, -1, True)],
           alt="A piecewise graph: a segment from the closed point (-4, -3) rising to an open point at (1, 2), then a segment from a closed point (1, 3) falling to the closed point (5, -1).")
B.mc(S, "cp1", "What is the domain of the function graphed?", "-4 ≤ x ≤ 5", ["-3 ≤ x ≤ 3", "-4 < x < 5", "-4 ≤ x < 1"],
     ["Read the x-values covered from left to right.", "The graph starts at the closed point x = -4 and ends at the closed point x = 5, with no gaps in x."],
     diagram=dg, tags=["graph"])
B.mc(S, "cp1", "What is the range of the function graphed?", "-3 ≤ y ≤ 3", ["-3 ≤ y < 2", "-1 ≤ y ≤ 3", "-3 < y ≤ 2"],
     ["The left piece covers -3 ≤ y < 2; the right piece covers -1 ≤ y ≤ 3.", "Together they cover every y from -3 to 3, including 3 (closed point at (1, 3))."],
     diagram=dg, tags=["graph"])
for expr, dom, steps in [("√(x - 2)/(x - 5)", "x ≥ 2, x ≠ 5", ["Radicand: x - 2 ≥ 0 → x ≥ 2.", "Denominator: x ≠ 5.", "Domain: [2, 5) ∪ (5, ∞)."]),
                         ("1/√(7 - x)", "x < 7", ["The radicand must be positive (it is in a denominator): 7 - x > 0.", "So x < 7, i.e. (-∞, 7)."]),
                         ("√(x² - 16)", "x ≤ -4 or x ≥ 4", ["x² - 16 ≥ 0 → (x - 4)(x + 4) ≥ 0.", "Sign test: true for x ≤ -4 or x ≥ 4."]),
                         ("(x - 1)/(x² + 4)", "all real numbers", ["x² + 4 ≥ 4 > 0, so the denominator is never 0.", "No restriction."])]:
    B.sa(S, "cp1", f"Find the domain of g(x) = {expr}. Write it in interval or inequality form.", dom, steps)
for expr, rng, steps in [("1/x + 2", "all real y except y = 2", ["1/x takes every real value except 0.", "Adding 2 shifts that missing value to 2."]),
                         ("2^x - 3", "y > -3", ["2^x > 0 for every x.", "So 2^x - 3 > -3."]),
                         ("-√(x + 1) + 6", "y ≤ 6", ["√(x + 1) ≥ 0, so -√(x + 1) ≤ 0.", "Add 6: y ≤ 6."])]:
    B.sa(S, "cp1", f"Find the range of h(x) = {expr}.", rng, steps)
B.sel(S, "cp1", "Select ALL functions whose domain is all real numbers.", ["f(x) = x³ - 2x", "f(x) = ∛(x - 9)", "f(x) = 1/(x² + 1)"],
      ["f(x) = √(x + 3)", "f(x) = 4/(x - 2)", "f(x) = √x + 1"],
      ["Polynomials and cube roots have no restrictions.", "x² + 1 is never zero.", "√(x + 3) needs x ≥ -3; 4/(x - 2) excludes 2; √x needs x ≥ 0."])
B.mc(S, "cp1", "A rental bike costs $6 plus $4 per hour, for up to 5 whole hours. The cost function is C(h) = 6 + 4h. Which is the most reasonable domain?",
     "{1, 2, 3, 4, 5}", ["all real numbers", "h ≥ 0", "{10, 14, 18, 22, 26}"],
     ["Only whole hours from 1 to 5 can be rented.", "The set {10, …, 26} is the range, not the domain."], tags=["modeling", "misconception"])
B.mc(S, "honors", "A student writes: 'The domain of f(x) = (x² - 9)/(x - 3) is all real numbers, because it simplifies to x + 3.' Which response is correct?",
     "Incorrect: x = 3 makes the original denominator 0, so the domain excludes 3.", ["Correct: simplified forms always have the same domain.",
     "Incorrect: the domain excludes both 3 and -3.", "Incorrect: the domain is x ≥ 3."],
     ["Domain is decided by the original rule.", "At x = 3 the expression is 0/0, undefined. The graph is the line y = x + 3 with a hole at (3, 6)."],
     tags=["error-analysis"])
for expr, rng, steps in [("(2x + 1)/(x - 3)", "all real y except y = 2", ["Solve y = (2x + 1)/(x - 3) for x: yx - 3y = 2x + 1 → x(y - 2) = 3y + 1.", "x = (3y + 1)/(y - 2) exists for every y except 2.", "Range: y ≠ 2."]),
                         ("x² - 6x + 11", "y ≥ 2", ["Complete the square: (x - 3)² + 2.", "Minimum value 2 at x = 3."]),
                         ("4/(x² + 1)", "0 < y ≤ 4", ["x² + 1 ≥ 1, so 0 < 4/(x² + 1) ≤ 4.", "y = 4 at x = 0; y approaches 0 but never reaches it."])]:
    B.sa(S, "honors", f"Determine the range of f(x) = {expr}. Justify algebraically.", rng, steps, tags=["challenge"])
B.sa(S, "honors", "Find a rule for a function whose domain is x ≥ 1 and whose range is y ≤ 2. (Many answers possible; give one and justify.)",
     "Example: f(x) = -√(x - 1) + 2", ["√(x - 1) needs x ≥ 1 and is ≥ 0.", "Negating gives values ≤ 0; adding 2 gives y ≤ 2.", "Any rule with these properties is acceptable."],
     tags=["challenge", "reasoning"])
B.orq(S, "honors", "A rectangular pen uses 40 m of fencing. Let w be the width in meters and A(w) the area.",
      [("Write A(w).", "A(w) = w(20 - w)"), ("State the domain in context.", "0 < w < 20"),
       ("Find the maximum area.", "100 m² at w = 10"), ("State the range in context.", "0 < A ≤ 100")],
      ["Length = (40 - 2w)/2 = 20 - w.", "Both dimensions must be positive: 0 < w < 20.", "A = -(w - 10)² + 100, so the maximum is 100.",
       "A approaches 0 near the endpoints but never equals 0 inside the domain."], tags=["modeling"])
B.sel(S, "honors", "f(x) = √(x - a) + b has domain x ≥ 3 and range y ≥ -2. Select ALL true statements.",
      ["a = 3", "b = -2", "f(7) = 0"], ["a = -3", "b = 2", "f(3) = 3"],
      ["Domain starts where x - a = 0, so a = 3.", "Range starts at b, so b = -2.", "f(7) = √4 - 2 = 0; f(3) = -2."])

# ---------------- Skill 3: operations & composition ----------------
S = 3
f1, g1 = x**2 - 1, 2*x + 3
for op, res, sym in [("(f + g)(x)", sp.expand(f1 + g1), "+"), ("(f - g)(x)", sp.expand(f1 - g1), "-"), ("(fg)(x)", sp.expand(f1 * g1), "·")]:
    B.sa(S, "cp2", f"Let f(x) = {fmt(f1, x)} and g(x) = {fmt(g1, x)}. Find {op}.", fmt(res, x),
         [f"{op} = ({fmt(f1, x)}) {sym} ({fmt(g1, x)}).", f"Simplify: {fmt(res, x)}."] if sym != "-" else
         [f"(f - g)(x) = ({fmt(f1, x)}) - ({fmt(g1, x)}).", "Distribute the negative to both terms of g.", f"= {fmt(res, x)}."])
for f, g, k in [(3*x - 1, x**2, 2), (x**2 + 1, x - 4, 1), (2*x, x**2 - 3, -2), (x**2 - x, 5 - x, 3)]:
    gv = g.subs(x, k); v = f.subs(x, gv)
    B.mc(S, "cp2", f"f(x) = {fmt(f, x)} and g(x) = {fmt(g, x)}. Find f(g({k})).", v,
         [g.subs(x, f.subs(x, k)), f.subs(x, k) * gv, f.subs(x, k) + gv],
         [f"Inside first: g({k}) = {gv}.", f"Then f({gv}) = {v}.", "Reversing the order gives g(f(k)), a different value."], tags=["misconception"])
for f, g in [(x**2 + 2, x - 3), (2*x + 5, x**2), (x**2 - x, 2*x + 1), (sp.sqrt(x), x + 4)]:
    fg = sp.expand(f.subs(x, g)); gf = sp.expand(g.subs(x, f))
    B.sa(S, "cp1", f"f(x) = {fmt(f, x)} and g(x) = {fmt(g, x)}. Find (f ∘ g)(x) and (g ∘ f)(x).",
         f"(f ∘ g)(x) = {fmt(fg, x if fg.is_polynomial(x) else None)}; (g ∘ f)(x) = {fmt(gf, x if gf.is_polynomial(x) else None)}",
         [f"(f ∘ g)(x) = f(g(x)) = f({fmt(g, x)}) = {fmt(fg, x if fg.is_polynomial(x) else None)}.",
          f"(g ∘ f)(x) = g(f(x)) = g({fmt(f, x)}) = {fmt(gf, x if gf.is_polynomial(x) else None)}.",
          "Composition is generally not commutative."])
B.mc(S, "cp1", "f(x) = x² - 4 and g(x) = x + 2. What is (f/g)(x), and what is its domain?", "x - 2, x ≠ -2",
     ["x - 2, all real numbers", "x + 2, x ≠ 2", "x - 2, x ≠ 2"],
     ["(f/g)(x) = (x² - 4)/(x + 2) = (x - 2)(x + 2)/(x + 2) = x - 2.", "g(-2) = 0, so -2 stays excluded from the domain."],
     tags=["misconception"])
dg = graph(B, "s03-two-graphs", [(lambda v: v - 1, {"color": "#1f4e9e"}), (lambda v: -0.5*v**2 + 3, {"color": "#b23a3a", "ls": "--"})],
           alt="Two graphs: f is the solid line y = x - 1. g is the dashed parabola y = -x²/2 + 3 with vertex (0, 3), passing through (2, 1) and (-2, 1).",
           points=[(0, 3), (2, 1), (-2, 1), (0, -1)])
for ex, v, st in [("f(g(2))", 0, "g(2) = 1, then f(1) = 0."), ("g(f(3))", 1, "f(3) = 2, then g(2) = 1."), ("(f + g)(0)", 2, "f(0) = -1 and g(0) = 3; sum 2.")]:
    B.sa(S, "cp1", f"The solid line is y = f(x); the dashed curve is y = g(x). Use the graph to find {ex}.", v,
         [st, "Read each value from the graph, working from the inside out for compositions."], diagram=dg, tags=["graph", "multiple-representations"])
B.mc(S, "cp1", "A store takes 15% off, then a $10 coupon is applied. If d(p) = 0.85p and c(p) = p - 10, which composition gives the final price of an item priced p?",
     "c(d(p)) = 0.85p - 10", ["d(c(p)) = 0.85p - 10", "d(c(p)) = 0.85p - 8.5", "c(d(p)) = 0.85(p - 10)"],
     ["The discount happens first, so d is the inside function.", "c(d(p)) = 0.85p - 10.", "d(c(p)) = 0.85(p - 10) = 0.85p - 8.5 applies the coupon first."], tags=["modeling"])
for f, g, dom in [("√(x - 1)", "x² + 1", "all real numbers"), ("1/(x - 2)", "x + 5", "x ≠ -3"), ("√x", "x - 9", "x ≥ 9")]:
    B.sa(S, "honors", f"f(x) = {f} and g(x) = {g}. Find the domain of (f ∘ g)(x).", dom,
         ["The domain of f ∘ g contains the x in the domain of g whose output g(x) lies in the domain of f.",
          {"all real numbers": "g(x) = x² + 1 ≥ 1, so x² + 1 - 1 = x² ≥ 0 always: f(g(x)) = |x|.",
           "x ≠ -3": "f(g(x)) = 1/(x + 5 - 2) = 1/(x + 3), so x ≠ -3.",
           "x ≥ 9": "f(g(x)) = √(x - 9), so x ≥ 9."}[dom]], tags=["challenge"])
for h, f, g in [("(3x - 1)²", "x²", "3x - 1"), ("√(x² + 7)", "√x", "x² + 7"), ("1/(2x + 5)", "1/x", "2x + 5"), ("2^(x - 4)", "2^x", "x - 4")]:
    B.mc(S, "honors", f"h(x) = {h}. Which pair satisfies h(x) = f(g(x))?", f"f(x) = {f}, g(x) = {g}",
         [f"f(x) = {g}, g(x) = {f}", f"f(x) = {h}, g(x) = x²" if f != "x²" else f"f(x) = {h}, g(x) = 3x", f"f(x) = x, g(x) = {f}"],
         [f"The inner step applied to x is {g}.", f"The outer step applied to that result is {f}.", f"Check: f(g(x)) = {h}."], tags=["reasoning"])
B.sel(S, "honors", "Let f(x) = 2x + 1 and g(x) = x². Select ALL true statements.",
      ["f(g(x)) = 2x² + 1", "g(f(x)) = 4x² + 4x + 1", "f(g(1)) = g(f(1)) - 6"], ["f(g(x)) = g(f(x)) for all x", "(fg)(x) = f(g(x))"],
      ["f(g(x)) = 2x² + 1 (true).", "g(f(x)) = (2x + 1)² = 4x² + 4x + 1 (true).",
       "f(g(1)) = f(1) = 3 and g(f(1)) = g(3) = 9, so f(g(1)) = 9 - 6 (true).",
       "The two compositions differ (e.g. at x = 1), and (fg)(x) = (2x + 1)x² is a product, not a composition."], tags=["reasoning"])
B.orq(S, "honors", "An oil spill spreads in a circle. The radius in meters after t hours is r(t) = 3t + 2, and the area of a circle is A(r) = πr².",
      [("Find (A ∘ r)(t).", "π(3t + 2)²"), ("Find the area after 4 hours (exact).", "196π m²"),
       ("Explain what (A ∘ r)(t) represents.", "The spill's area as a function of time"), ("When does the area reach 400π m²?", "t = 6 hours")],
      ["A(r(t)) = π(3t + 2)².", "r(4) = 14, A = 196π.", "Input time → radius → area.", "(3t + 2)² = 400 → 3t + 2 = 20 (positive) → t = 6."], tags=["modeling", "multistep"])

# ---------------- Skill 4: inverse functions ----------------
S = 4
for m, b in [(3, -5), (F(1, 2), 4), (-2, 7), (5, 1), (F(-2, 3), 2)]:
    mi = 1 / F(m); bi = -F(b) / F(m)
    B.sa(S, "cp2", f"Find the inverse of f(x) = {lin(m, b)}.", f"f⁻¹(x) = {lin(mi, bi)}",
         [f"Write y = {lin(m, b)} and swap x and y: x = {lin(m, b, 'y')}.",
          f"Solve for y: y = (x - ({num(F(b))}))/{num(F(m))}.", f"f⁻¹(x) = {lin(mi, bi)}."])
B.mc(S, "cp2", "If f(4) = 11, which must be true?", "f⁻¹(11) = 4", ["f⁻¹(4) = 11", "f⁻¹(11) = 1/4", "f(11) = 4"],
     ["An inverse swaps inputs and outputs.", "(4, 11) on f means (11, 4) on f⁻¹."], tags=["misconception"])
B.mc(S, "cp2", "A student says f⁻¹(x) means 1/f(x). For f(x) = x + 3, which shows the difference?",
     "f⁻¹(x) = x - 3, but 1/f(x) = 1/(x + 3)", ["They are equal for every x", "f⁻¹(x) = -x - 3", "f⁻¹(x) = 1/(x - 3)"],
     ["The -1 in f⁻¹ is notation for the inverse function, not an exponent.", "f⁻¹ undoes 'add 3', so f⁻¹(x) = x - 3."], tags=["misconception", "error-analysis"])
for f, inv, steps in [("x³ + 2", "∛(x - 2)", ["x = y³ + 2 → y³ = x - 2.", "y = ∛(x - 2)."]),
                      ("(x - 1)/4", "4x + 1", ["x = (y - 1)/4 → 4x = y - 1.", "y = 4x + 1."]),
                      ("2∛x - 3", "((x + 3)/2)³", ["x = 2∛y - 3 → ∛y = (x + 3)/2.", "Cube both sides: y = ((x + 3)/2)³."]),
                      ("5 - x³", "∛(5 - x)", ["x = 5 - y³ → y³ = 5 - x.", "y = ∛(5 - x)."])]:
    B.sa(S, "cp1", f"Find f⁻¹(x) for f(x) = {f}.", f"f⁻¹(x) = {inv}", ["Replace f(x) with y and swap x and y."] + steps)
for f, d, inv in [("x² + 1", "x ≥ 0", "√(x - 1), x ≥ 1"), ("(x - 3)²", "x ≥ 3", "√x + 3, x ≥ 0"), ("√(x + 2)", "x ≥ -2", "x² - 2, x ≥ 0")]:
    B.sa(S, "cp1", f"f(x) = {f} with domain {d}. Find f⁻¹(x) and state its domain.", f"f⁻¹(x) = {inv}",
         ["Swap x and y, then solve for y, keeping the branch that matches the restricted range of f.",
          f"The domain of f⁻¹ is the range of f."], tags=["challenge"])
B.sel(S, "cp1", "Select ALL functions that have an inverse that is also a function (on all real numbers).",
      ["f(x) = 2x - 9", "f(x) = x³", "f(x) = 2^x"], ["f(x) = x²", "f(x) = |x|", "f(x) = x⁴ - 1"],
      ["A function is invertible when it is one-to-one (passes the horizontal line test).",
       "Lines with nonzero slope, x³ and 2^x are one-to-one.", "x², |x| and x⁴ - 1 give the same output for x and -x."])
dg = graph(B, "s04-inverse-reflect", [(lambda v: 2*v - 2, {}), (lambda v: v, {"color": "gray", "ls": ":", "lw": 1.2})],
           points=[(0, -2, True, "(0, -2)"), (2, 2, True, "(2, 2)")],
           alt="The line y = 2x - 2 through (0, -2) and (2, 2), with the dotted line y = x for reference.")
B.mc(S, "cp1", "The solid line is the graph of f. Which point lies on the graph of f⁻¹?", "(-2, 0)", ["(0, 2)", "(2, -2)", "(0, -2)"],
     ["Reflect points of f across y = x by swapping coordinates.", "(0, -2) on f gives (-2, 0) on f⁻¹."], diagram=dg, tags=["graph"])
for f, g, res in [("3x - 6", "x/3 + 2", True), ("x³ - 1", "∛x + 1", False), ("(x + 4)/5", "5x - 4", True), ("2x + 1", "x/2 - 1", False)]:
    B.mc(S, "cp1", f"Are f(x) = {f} and g(x) = {g} inverses? Use composition.",
         "Yes: f(g(x)) = x and g(f(x)) = x" if res else "No: f(g(x)) ≠ x",
         ["No: f(g(x)) ≠ x" if res else "Yes: f(g(x)) = x and g(f(x)) = x", "Only if their graphs intersect", "Yes, because both are functions"],
         ["Inverses satisfy f(g(x)) = x and g(f(x)) = x.",
          {"3x - 6": "f(g(x)) = 3(x/3 + 2) - 6 = x; g(f(x)) = (3x - 6)/3 + 2 = x.",
           "x³ - 1": "f(g(x)) = (∛x + 1)³ - 1, which is not x (try x = 1: 2³ - 1 = 7). The inverse of x³ - 1 is ∛(x + 1).",
           "(x + 4)/5": "f(g(x)) = (5x - 4 + 4)/5 = x; g(f(x)) = 5·(x + 4)/5 - 4 = x.",
           "2x + 1": "f(g(x)) = 2(x/2 - 1) + 1 = x - 1 ≠ x. The inverse is (x - 1)/2."}[f]], tags=["reasoning"])
B.mc(S, "cp1", "A taxi charges C(m) = 2.5m + 4 dollars for m miles. What does C⁻¹(19) represent?",
     "The number of miles you can ride for $19 (6 miles)", ["The cost of a 19-mile ride ($51.50)", "The cost per mile", "1/C(19)"],
     ["C⁻¹ takes a cost and returns miles.", "2.5m + 4 = 19 → m = 6."], tags=["modeling"])
B.sa(S, "honors", "Find the inverse of f(x) = (2x + 1)/(x - 3) and state the domain and range of f⁻¹.",
     "f⁻¹(x) = (3x + 1)/(x - 2); domain x ≠ 2, range y ≠ 3",
     ["Swap: x = (2y + 1)/(y - 3) → xy - 3x = 2y + 1.", "y(x - 2) = 3x + 1 → y = (3x + 1)/(x - 2).",
      "Domain of f⁻¹ = range of f: x ≠ 2. Range of f⁻¹ = domain of f: y ≠ 3."], tags=["challenge"])
B.sa(S, "honors", "f(x) = x² - 4x + 1 with domain x ≥ 2. Find f⁻¹(x).", "f⁻¹(x) = 2 + √(x + 3), x ≥ -3",
     ["Complete the square: f(x) = (x - 2)² - 3.", "Swap and solve: (y - 2)² = x + 3 → y - 2 = ±√(x + 3).",
      "Since y ≥ 2 (the original domain), take +: y = 2 + √(x + 3)."], tags=["challenge"])
B.mc(S, "honors", "Which function is its own inverse?", "f(x) = 6 - x", ["f(x) = x + 6", "f(x) = 6x", "f(x) = x² + 6"],
     ["Check f(f(x)) = x.", "f(f(x)) = 6 - (6 - x) = x.", "The graph y = 6 - x is perpendicular to y = x, so reflecting it over y = x leaves it unchanged."],
     tags=["reasoning"])
B.sel(S, "honors", "f is one-to-one with f(2) = 5, f(5) = -1, and f(-1) = 0. Select ALL true statements.",
      ["f⁻¹(5) = 2", "f⁻¹(f⁻¹(-1)) = 2", "f(f⁻¹(0)) = 0"], ["f⁻¹(0) = 0", "f⁻¹(-1) = -1"],
      ["f⁻¹(5) = 2.", "f⁻¹(-1) = 5, then f⁻¹(5) = 2.", "f(f⁻¹(a)) = a for every a in the range of f.",
       "f⁻¹(0) = -1, not 0; f⁻¹(-1) = 5, not -1."], tags=["reasoning"])
B.orq(S, "honors", "Converting temperature: F(c) = 1.8c + 32 converts °C to °F.",
      [("Find F⁻¹(f).", "F⁻¹(f) = (f - 32)/1.8"), ("Convert 77°F to °C.", "25°C"),
       ("Verify F(F⁻¹(f)) = f.", "1.8·(f - 32)/1.8 + 32 = f"), ("At what temperature are the readings equal?", "-40°")],
      ["Swap and solve: c = (f - 32)/1.8.", "(77 - 32)/1.8 = 25.", "The composition simplifies to f.", "1.8c + 32 = c → 0.8c = -32 → c = -40."],
      tags=["modeling"])

# ---------------- Skill 5: parent functions & transformations ----------------
S = 5
for parent, rule, desc in [("x²", "(x - 3)² + 2", "right 3, up 2"), ("|x|", "|x + 4| - 1", "left 4, down 1"),
                           ("√x", "√(x - 5)", "right 5"), ("x³", "x³ - 6", "down 6"), ("1/x", "1/(x + 2) + 3", "left 2, up 3")]:
    wrongs = {"right 3, up 2": ["left 3, up 2", "right 3, down 2", "right 2, up 3"],
              "left 4, down 1": ["right 4, down 1", "left 4, up 1", "left 1, down 4"],
              "right 5": ["left 5", "down 5", "up 5"], "down 6": ["right 6", "up 6", "left 6"],
              "left 2, up 3": ["right 2, up 3", "left 2, down 3", "right 3, up 2"]}[desc]
    B.mc(S, "cp2", f"Describe how the graph of g(x) = {rule} relates to the parent graph y = {parent}.", f"Translate {desc}",
         [f"Translate {w}" for w in wrongs],
         ["A change inside with the input, (x - h), shifts horizontally by h (opposite of the sign shown).",
          "A change outside, + k, shifts vertically by k.", f"So: {desc}."], tags=["misconception"])
for h, k, a in [(2, -3, 1), (-1, 4, -1), (0, -5, 2), (3, 0, F(1, 2))]:
    rule = fmt(sp.nsimplify(a)*(x - h)**2 + k)
    B.sa(S, "cp2", f"What is the vertex of g(x) = {rule}?", pt(h, k),
         [f"g is the graph of y = x² translated so the vertex moves from (0, 0) to (h, k).", f"Vertex: {pt(h, k)}."])
dg = graph(B, "s05-abs-transform", [(lambda v: -2*abs(v - 1) + 4, {})], points=[(1, 4, True, "(1, 4)"), (3, 0), (-1, 0)],
           alt="An upside-down V with vertex (1, 4) passing through (-1, 0) and (3, 0).")
B.mc(S, "cp1", "The graph shows a transformation of y = |x|. Which equation matches it?", "y = -2|x - 1| + 4",
     ["y = 2|x - 1| + 4", "y = -2|x + 1| + 4", "y = -½|x - 1| + 4"],
     ["The vertex is (1, 4), so y = a|x - 1| + 4.", "Use (3, 0): 0 = a·2 + 4 → a = -2.", "Negative a: opens down; |a| = 2: steeper than the parent."],
     diagram=dg, tags=["graph"])
for orig, a, b, h, k in [((2, 6), -1, 1, 0, 0), ((2, 6), 1, 2, 0, 0), ((2, 6), 3, 1, -1, 2), ((-4, 1), 1, 1, 3, -5), ((-4, 1), F(1, 2), 1, 0, 4)]:
    # g(x) = a f(b(x - h)) + k ; image of (p, q) is (p/b + h, a q + k)
    p, q = orig; ip = F(p) / b + h; iq = a * q + k
    rule = ("" if a == 1 else ("-" if a == -1 else (f"({num(a)})" if isinstance(a, F) else num(a)))) + "f(" + ("" if b == 1 else str(b)) + ("x" if h == 0 else f"(x {'-' if h > 0 else '+'} {abs(h)})") + ")" + ("" if k == 0 else f" {'+' if k > 0 else '-'} {abs(k)}")
    B.sa(S, "cp1", f"The point {pt(p, q)} is on the graph of y = f(x). What point must be on the graph of y = {rule}?", pt(ip, iq),
         [f"The input to f must be {p}: set the expression inside f equal to {p} and solve, giving x = {num(ip)}.",
          f"y-coordinate: {num(a)}·{q} + {k} = {num(iq)}.", f"Image point: {pt(ip, iq)}."])
B.sel(S, "cp1", "g(x) = -3(x + 2)² - 1. Select ALL true statements about g compared with y = x².",
      ["It is reflected over the x-axis", "It is vertically stretched by a factor of 3", "Its vertex is (-2, -1)"],
      ["It is translated 2 units right", "It is vertically compressed by a factor of 1/3", "Its maximum value is 2"],
      ["a = -3: reflection and a vertical stretch by 3.", "(x + 2) → left 2; -1 → down 1; vertex (-2, -1).", "Maximum value is -1, not 2."])
for desc, ans, wrong in [("y = √x reflected over the y-axis, then shifted up 3", "y = √(-x) + 3", ["y = -√x + 3", "y = √(x + 3)", "y = -√(x - 3)"]),
                         ("y = x³ stretched vertically by 2 and shifted left 1", "y = 2(x + 1)³", ["y = 2(x - 1)³", "y = (2x + 1)³", "y = 2x³ - 1"]),
                         ("y = |x| compressed horizontally by a factor of 1/3, then shifted down 2", "y = |3x| - 2", ["y = |x/3| - 2", "y = (1/3)|x| - 2", "y = |3x - 2|"])]:
    B.mc(S, "cp1", f"Write the equation: {desc}.", ans, wrong,
         ["Reflection over the y-axis replaces x with -x; over the x-axis negates the output.",
          "Horizontal compression by 1/k replaces x with kx.", f"Result: {ans}."])
B.mc(S, "honors", "A student says y = (2x - 6)² is y = (2x)² shifted right 6. What is the correct horizontal shift?",
     "Right 3, because (2x - 6)² = (2(x - 3))²", ["Right 6, as the student said", "Left 3", "Right 12"],
     ["Factor the coefficient of x: 2x - 6 = 2(x - 3).", "The shift is the h in (x - h): right 3."], tags=["error-analysis", "misconception"])
B.mc(S, "honors", "The graph of y = f(x) has domain [-2, 6] and range [1, 9]. What are the domain and range of y = -2f(x/2) + 1?",
     "Domain [-4, 12], range [-17, -1]", ["Domain [-1, 3], range [-17, -1]", "Domain [-4, 12], range [3, 19]", "Domain [-2, 6], range [-17, -1]"],
     ["x/2 must be in [-2, 6], so x ∈ [-4, 12].", "f(x/2) ∈ [1, 9] → -2f ∈ [-18, -2] → +1 gives [-17, -1]."], tags=["challenge"])
B.sa(S, "honors", "Order matters: Start with y = x². (a) Stretch vertically by 3 then shift up 2. (b) Shift up 2 then stretch vertically by 3. Write both equations.",
     "(a) y = 3x² + 2; (b) y = 3x² + 6", ["(a) Stretch: 3x²; then add 2: 3x² + 2.", "(b) Add 2: x² + 2; then multiply all outputs by 3: 3x² + 6.",
     "Vertical stretches act on the shift that came before them."], tags=["reasoning"])
B.orq(S, "honors", "Let g(x) = -½(x - 4)² + 8 be a transformation of f(x) = x².",
      [("List the transformations in a valid order.", "Compress vertically by ½, reflect over the x-axis, shift right 4, shift up 8"),
       ("State the vertex and axis of symmetry.", "Vertex (4, 8); x = 4"), ("Find the x-intercepts.", "x = 0 and x = 8"),
       ("State the range.", "y ≤ 8")],
      ["Scale/reflect first, then translate.", "Vertex from (h, k) = (4, 8).", "-½(x - 4)² + 8 = 0 → (x - 4)² = 16 → x = 0, 8.", "Opens down from y = 8."],
      tags=["multistep"])
dg2 = graph(B, "s05-sqrt-transform", [(lambda v: -np.sqrt(v + 3) + 2 if v >= -3 else np.nan, {"_dom": (-3, 6)})],
            points=[(-3, 2, True, "(-3, 2)"), (1, 0), (6, -1)],
            alt="A square-root shaped curve starting at (-3, 2) and decreasing through (1, 0) and (6, -1).")
B.sa(S, "honors", "The graph shows y = a√(x - h) + k. Find a, h, and k.", "a = -1, h = -3, k = 2",
     ["The starting point is (h, k) = (-3, 2).", "Use (1, 0): 0 = a√4 + 2 → a = -1.", "Check (6, -1): -√9 + 2 = -1 ✓."], diagram=dg2, tags=["graph", "challenge"])

# ---------------- Skill 6: piecewise functions ----------------
S = 6
pw = "f(x) = { x² - 1 if x < 2;  3x - 4 if x ≥ 2 }"
for k, v, piece in [(-3, 8, "x² - 1"), (2, 2, "3x - 4"), (5, 11, "3x - 4"), (0, -1, "x² - 1")]:
    B.sa(S, "cp2", f"{pw}. Find f({k}).", v, [f"{k} {'<' if k < 2 else '≥'} 2, so use {piece}.", f"f({k}) = {v}."])
B.mc(S, "cp2", "g(x) = { -x if x ≤ 0;  x + 1 if x > 0 }. A student finds g(0) = 1. What was the error?",
     "x = 0 belongs to the first piece, so g(0) = 0", ["None; g(0) = 1", "g(0) is undefined", "Both pieces apply, so g(0) = 0 and 1"],
     ["The inequality x ≤ 0 includes 0.", "g(0) = -0 = 0."], tags=["error-analysis"])
dg = graph(B, "s06-step", [(lambda v: 2 if v < -1 else np.nan, {"_dom": (-6, -1)}), (lambda v: -v if v < 3 else np.nan, {"_dom": (-1, 3)}), (lambda v: 1, {"_dom": (3, 6)})],
           points=[(-1, 2, False), (-1, 1, True), (3, -3, False), (3, 1, True)],
           alt="Piecewise graph: horizontal ray y = 2 for x < -1 ending in an open point at (-1, 2); a segment of y = -x from a closed point (-1, 1) to an open point (3, -3); a horizontal ray y = 1 starting at a closed point (3, 1).")
B.mc(S, "cp1", "Which rule matches the graph?", "f(x) = { 2 if x < -1;  -x if -1 ≤ x < 3;  1 if x ≥ 3 }",
     ["f(x) = { 2 if x ≤ -1;  -x if -1 < x ≤ 3;  1 if x > 3 }", "f(x) = { 2 if x < -1;  x if -1 ≤ x < 3;  1 if x ≥ 3 }",
      "f(x) = { -1 if x < 2;  -x if -1 ≤ x < 3;  3 if x ≥ 1 }"],
     ["Closed points belong to their piece; open points do not.", "At x = -1 the closed point is on y = -x; at x = 3 the closed point is on y = 1.",
      "The middle piece falls with slope -1 through (0, 0), so it is -x."], diagram=dg, tags=["graph"])
for k, v in [(-1, 1), (3, 1), (0, 0)]:
    B.sa(S, "cp1", f"Use the graph of the piecewise function. Find f({k}).", v,
         ["Use the closed (filled) point at that x-value.", f"f({k}) = {v}."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "A parking garage charges $5 for the first hour or less and $3 for each additional hour or part of an hour, up to $20 per day. How much does 3 hours 10 minutes cost?",
     "$14", ["$11", "$14.50", "$20"], ["First hour: $5.", "Remaining 2 h 10 min rounds up to 3 additional hours: 3·$3 = $9.", "Total $14, which is under the $20 cap."], tags=["modeling"])
for a, b, c in [(1, 4, 2), (2, -1, 3)]:
    # f = { ax + b, x<c ; x^2 + k , x>=c } find k for continuity
    kk = a*c + b - c*c
    B.sa(S, "cp1", f"f(x) = {{ {lin(a, b)} if x < {c};  x² + k if x ≥ {c} }}. Find k so that the graph has no break at x = {c}.", kk,
         [f"The pieces must agree at x = {c}.", f"{a}({c}) + {b} = {a*c + b} and {c}² + k = {c*c} + k.", f"{c*c} + k = {a*c + b} → k = {kk}."], tags=["reasoning"])
B.sa(S, "cp1", "Write |x - 3| as a piecewise function.", "{ -(x - 3) if x < 3;  x - 3 if x ≥ 3 }",
     ["|u| = u when u ≥ 0 and -u when u < 0.", "x - 3 ≥ 0 when x ≥ 3."])
B.sa(S, "honors", "Solve f(x) = 5 for f(x) = { x² + 1 if x < 0;  2x - 3 if x ≥ 0 }.", "x = -2 or x = 4",
     ["Piece 1: x² + 1 = 5 → x = ±2; only x = -2 satisfies x < 0.", "Piece 2: 2x - 3 = 5 → x = 4, which satisfies x ≥ 0.",
      "Always check each solution against its piece's condition."], tags=["challenge"])
B.sa(S, "honors", "Find a and b so that f(x) = { ax + 1 if x < 1;  x² + b if 1 ≤ x < 3;  4x - a if x ≥ 3 } has no breaks.", "a = 3/2, b = 3/2",
     ["At x = 1 the pieces must match: a(1) + 1 = 1² + b → a = b.", "At x = 3: 3² + b = 4(3) - a → a + b = 3.",
      "Substitute a = b: 2a = 3 → a = b = 3/2.", "Check: at x = 1 both give 2.5; at x = 3 both give 10.5."], tags=["challenge"])
B.orq(S, "honors", "A cell plan charges $30 for up to 5 GB, then $8 per GB (charged by exact usage) above 5 GB, up to a cap of 15 GB.",
      [("Write C(g) as a piecewise function for 0 ≤ g ≤ 15.", "C(g) = { 30 if 0 ≤ g ≤ 5;  30 + 8(g - 5) if 5 < g ≤ 15 }"),
       ("Find C(3) and C(9.5).", "$30 and $66"), ("What usage costs $90?", "12.5 GB"), ("State the range.", "30 ≤ C ≤ 110")],
      ["Flat $30, then $8 for each GB over 5.", "C(9.5) = 30 + 8(4.5) = 66.", "30 + 8(g - 5) = 90 → g = 12.5.", "C(15) = 30 + 80 = 110."], tags=["modeling"])
B.sel(S, "honors", "f(x) = { x + 2 if x < 0;  2 - x² if x ≥ 0 }. Select ALL true statements.",
      ["f is continuous at x = 0", "f(x) = 0 at exactly two x-values", "The maximum value of f is 2"],
      ["f is increasing for all x", "The range is all real numbers"],
      ["Both pieces give 2 at x = 0.", "x + 2 = 0 → x = -2; 2 - x² = 0 → x = √2 (x ≥ 0).", "f ≤ 2 everywhere and equals 2 at x = 0.",
       "f decreases for x > 0; range is y ≤ 2."])

# ---------------- Skill 7: even and odd ----------------
S = 7
for f, kind, st in [(x**4 - 3*x**2 + 1, "even", "Only even powers appear, so f(-x) = f(x)."),
                    (x**3 - 5*x, "odd", "Only odd powers appear, so f(-x) = -f(x)."),
                    (x**2 + x, "neither", "f(-x) = x² - x, which is neither f(x) nor -f(x)."),
                    (2*x**5 + x, "odd", "f(-x) = -2x⁵ - x = -f(x)."),
                    (x**3 + 1, "neither", "f(-x) = -x³ + 1, neither f(x) nor -f(x).")]:
    B.mc(S, "cp2", f"Is f(x) = {fmt(f, x)} even, odd, or neither?", kind.capitalize(), [k.capitalize() for k in ["even", "odd", "neither", "both"] if k != kind],
         ["Compute f(-x) and compare.", st])
for desc, kind in [("symmetric about the y-axis", "even"), ("symmetric about the origin", "odd")]:
    B.mc(S, "cp2", f"A graph is {desc}. Which statement must be true for every x in its domain?",
         "f(-x) = f(x)" if kind == "even" else "f(-x) = -f(x)", ["f(-x) = -f(x)" if kind == "even" else "f(-x) = f(x)", "f(x) = -f(x)", "f(x + 1) = f(x)"],
         [f"{'Y-axis symmetry' if kind == 'even' else 'Origin symmetry'} defines an {kind} function."])
dg = graph(B, "s07-odd-graph", [(lambda v: 0.25*v**3 - 2*v, {})], points=[(2, -2, True, "(2, -2)"), (-2, 2)],
           alt="A cubic curve symmetric about the origin, passing through (-2, 2), (0, 0) and (2, -2).")
B.mc(S, "cp1", "The graph shown passes through (2, -2) and is symmetric about the origin. What is f(-2)?", "2", ["-2", "0", "4"],
     ["Origin symmetry: f(-x) = -f(x).", "f(-2) = -f(2) = 2."], diagram=dg, tags=["graph"])
for f, kind in [("|x| + x²", "even"), ("x/(x² + 1)", "odd"), ("√(x² + 4)", "even"), ("(x - 1)²", "neither"), ("x·|x|", "odd")]:
    B.sa(S, "cp1", f"Determine algebraically whether f(x) = {f} is even, odd, or neither.", kind,
         ["Substitute -x for x and simplify.", {"even": "f(-x) = f(x).", "odd": "f(-x) = -f(x).", "neither": "f(-x) = (x + 1)², not f(x) or -f(x)."}[kind]])
B.sel(S, "cp1", "Select ALL odd functions.", ["f(x) = x³", "f(x) = 1/x", "f(x) = -4x"], ["f(x) = x² + 2", "f(x) = x + 3", "f(x) = |x|"],
      ["Odd functions satisfy f(-x) = -f(x); they pass through the origin if defined at 0.", "x + 3 fails: f(0) = 3 ≠ 0."])
B.mc(S, "cp1", "A student says f(x) = x³ + x² is odd because it has an odd power. What is correct?",
     "It is neither; f(-x) = -x³ + x² ≠ -f(x)", ["It is odd", "It is even, since x² is even", "It is both even and odd"],
     ["Test with f(-x): -x³ + x².", "-f(x) = -x³ - x², so not odd; not equal to f(x) either."], tags=["error-analysis"])
B.sa(S, "honors", "f is even and g is odd. Is h(x) = f(x)·g(x) even, odd, or neither? Prove it.", "odd",
     ["h(-x) = f(-x)g(-x) = f(x)·(-g(x)) = -h(x).", "So h is odd."], tags=["reasoning", "challenge"])
B.sa(S, "honors", "If f is odd and defined at 0, what is f(0)? Explain.", "0", ["f(-0) = -f(0) → f(0) = -f(0) → 2f(0) = 0.", "So f(0) = 0."], tags=["reasoning"])
B.sel(S, "honors", "f is odd and g is even (both defined for all x). Select ALL that must be even.", ["g(f(x))", "f(x)·f(x)", "g(x) + g(x)"],
      ["f(g(x)) + f(x)", "f(x) + g(x)"],
      ["g(f(-x)) = g(-f(x)) = g(f(x)).", "f(-x)² = f(x)².", "Sum of even functions is even.", "f(x) + g(x) and f(g(x)) + f(x) fail in general (try f = x, g = x²)."], tags=["challenge"])
B.orq(S, "honors", "Let p(x) = ax³ + bx² + cx + d.",
      [("What conditions make p even?", "a = 0 and c = 0"), ("What conditions make p odd?", "b = 0 and d = 0"),
       ("Can p be both even and odd? Explain.", "Only p(x) = 0"), ("Write any function as even part + odd part using f(x) and f(-x).", "f(x) = [f(x) + f(-x)]/2 + [f(x) - f(-x)]/2")],
      ["p(-x) = -ax³ + bx² - cx + d.", "Even needs the odd-degree coefficients to vanish; odd needs the even-degree ones to vanish.",
       "Both → all coefficients 0.", "The first bracket is even and the second is odd."], tags=["challenge", "connections"])

# ---------------- Skill 8: modeling with functions ----------------
S = 8
for fixed, rate, k in [(25, 0.15, 300), (40, 0.2, 180), (12, 2.5, 18)]:
    v = fixed + rate*k
    B.sa(S, "cp2", f"A service charges ${fixed} plus ${rate} per unit. Write a cost function C(u) and find C({k}).",
         f"C(u) = {fixed} + {rate}u; C({k}) = ${v:g}", [f"Fixed part {fixed}, rate {rate} per unit: C(u) = {fixed} + {rate}u.", f"C({k}) = {fixed} + {rate}({k}) = {v:g}."], tags=["modeling"])
B.mc(S, "cp2", "Which type of function best models a population that doubles every 6 years?", "Exponential", ["Linear", "Quadratic", "Absolute value"],
     ["Constant multiplication over equal time intervals is exponential growth."], tags=["modeling"])
B.mc(S, "cp2", "A table of (x, y): (0, 3), (1, 7), (2, 11), (3, 15). Which model fits?", "y = 4x + 3", ["y = 3x + 4", "y = 3·4^x", "y = x² + 3"],
     ["The y-values increase by 4 each step, so the model is linear with slope 4.", "The y-intercept is 3."], tags=["multiple-representations"])
B.mc(S, "cp1", "Table: (0, 2), (1, 6), (2, 18), (3, 54). Which model fits?", "y = 2·3^x", ["y = 4x + 2", "y = 3·2^x", "y = 2x² + 2"],
     ["Each y is 3 times the previous one, so it is exponential with factor 3.", "Starting value 2."], tags=["multiple-representations"])
B.mc(S, "cp1", "Table: (0, 1), (1, 3), (2, 9), (3, 19), (4, 33). Which model fits?", "y = 2x² + 1", ["y = 3^x", "y = 8x + 1", "y = x² + 2x + 1"],
     ["First differences 2, 6, 10, 14; second differences constant 4 → quadratic with a = 2.", "y-intercept 1; check x = 1: 2 + 1 = 3 ✓."], tags=["multiple-representations"])
B.sa(S, "cp1", "A phone loses value: it costs $900 new and is worth $450 after 2 years. Assuming linear depreciation, write V(t) and find when it is worth $0.",
     "V(t) = 900 - 225t; t = 4 years", ["Slope = (450 - 900)/2 = -225 per year.", "V(t) = 900 - 225t = 0 → t = 4."], tags=["modeling"])
B.sa(S, "cp1", "A rectangle has perimeter 50 cm. Write the area A as a function of the width w, and give the width that maximizes area.",
     "A(w) = w(25 - w); w = 12.5 cm", ["Length = 25 - w.", "A(w) = 25w - w² has its vertex at w = 25/2 = 12.5."], tags=["modeling"])
B.sa(S, "cp1", "A box is made from a 20 in by 20 in sheet by cutting x-in squares from each corner and folding. Write V(x) and state its domain.",
     "V(x) = x(20 - 2x)²; 0 < x < 10", ["Base side 20 - 2x, height x.", "Both must be positive: 0 < x < 10."], tags=["modeling"])
B.mc(S, "cp1", "Revenue R(p) = p(400 - 10p) for ticket price p dollars. What price maximizes revenue?", "$20", ["$40", "$10", "$4,000"],
     ["R(p) = -10p² + 400p.", "Vertex: p = -400/(2·-10) = 20.", "The maximum revenue is R(20) = $4,000, which is not the price."], tags=["modeling", "misconception"])
B.sa(S, "honors", "A rancher fences a rectangular field along a river (no fence on the river side) with 600 m of fence. Find the dimensions that maximize the area.",
     "150 m by 300 m (300 m parallel to the river); area 45,000 m²", ["Let x be each side perpendicular to the river: parallel side = 600 - 2x.",
     "A = x(600 - 2x) = -2x² + 600x, vertex at x = 150.", "Parallel side = 300; A = 45,000."], tags=["modeling", "challenge"])
B.sa(S, "honors", "A cylinder can must hold 500 cm³. Write its surface area S as a function of radius r alone.", "S(r) = 2πr² + 1000/r",
     ["V = πr²h = 500 → h = 500/(πr²).", "S = 2πr² + 2πrh = 2πr² + 2πr·500/(πr²) = 2πr² + 1000/r."], tags=["modeling", "challenge"])
B.orq(S, "honors", "A bakery sells 200 loaves a day at $4. For each $0.25 increase in price, it sells 10 fewer loaves.",
      [("Let n be the number of $0.25 increases. Write revenue R(n).", "R(n) = (4 + 0.25n)(200 - 10n)"),
       ("Find the n that maximizes revenue.", "n = 2"), ("What is the best price and the maximum revenue?", "$4.50; $810"),
       ("State a reasonable domain for n.", "0 ≤ n ≤ 20, n a whole number")],
      ["Price 4 + 0.25n, loaves 200 - 10n.", "R(n) = -2.5n² + 10n + 800, vertex at n = -10/(2·-2.5) = 2.", "Price $4.50, 180 loaves → $810.",
       "Loaves cannot be negative: n ≤ 20."], tags=["modeling", "multistep"])
B.orq(S, "honors", "Two plans: Plan A costs $20 per month plus $0.10 per text; Plan B costs $35 per month with unlimited texts.",
      [("Write A(t) and B(t) for t texts.", "A(t) = 20 + 0.10t; B(t) = 35"), ("When do they cost the same?", "150 texts"),
       ("Which is cheaper for 400 texts, and by how much?", "Plan B, by $25"), ("Write the piecewise function for the cheaper cost.", "{ 20 + 0.1t if t ≤ 150;  35 if t > 150 }")],
      ["Linear vs constant.", "20 + 0.1t = 35 → t = 150.", "A(400) = 60 vs 35.", "Choose the smaller value on each interval."], tags=["modeling", "connections"])
B.sel(S, "honors", "Data: (1, 5), (2, 9), (3, 15), (4, 23), (5, 33). Select ALL true statements.",
      ["Second differences are constant", "A quadratic model fits exactly", "The model gives y = 0 at no real x"],
      ["A linear model fits exactly", "An exponential model with constant ratio fits exactly"],
      ["First differences 4, 6, 8, 10; second differences 2.", "Fit: y = x² + x + 3 (check x = 1: 5 ✓, x = 5: 33 ✓).", "Discriminant 1 - 12 < 0, so no real zeros.",
       "Ratios 9/5, 15/9 are not constant."], tags=["modeling", "multiple-representations"])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, v)
