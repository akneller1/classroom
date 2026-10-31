"""Session-2 top-up for linear-functions-systems: appends items (IDs continue) to the session-1 bank."""
from lib import Bank, graph
from mathlite import *
import itertools

STD = {1: ["F-LE.A.2", "A-CED.A.2"], 2: ["F-IF.B.6"], 3: ["F-LE.A.2", "S-ID.B.6"], 4: ["A-REI.C.6", "A-REI.D.11"],
       5: ["A-REI.C.5", "A-REI.C.6"], 6: ["A-REI.D.12"], 7: ["A-CED.A.3"]}
U = "linear-functions-systems"
B = Bank.resume(U, "ls", STD, f"base/{U}.json", f"base/{U}.tags.json")  # session-1 bank (pristine copy) so reruns are idempotent
N0 = len(B.qs)
import s1_fixes; s1_fixes.apply(B)  # cosmetic notation fixes to session-1 items (see PROGRESS.md)


def line(m, b):
    return f"y = {pstr(P([F(b), F(m)]))}"


def std_form(a, b, c):
    t = pstr(P([0, a])) if a else ""
    yb = F(b)
    if yb: t += (" + " if yb > 0 and t else (" - " if yb < 0 and t else ("-" if yb < 0 else ""))) + (("" if abs(yb) == 1 else fr(abs(yb))) + "y")
    return f"{t} = {fr(c)}"


# ---- Skill 1 ----
for m, b in [(F(2, 3), -4), (-3, 5), (F(-1, 2), 1)]:
    x0 = 3; y0 = m * x0 + b
    cands = [line(m, b), f"y - {fr(y0)} = {frp(m) if '/' in fr(m) else fr(m)}(x - {x0})".replace("- -", "+ "), line(m, -b) if b else line(m, 1), line(-m, b), line(1 / m, b)]
    def ok(s_, m=m, b=b):
        lhs, rhs = s_.split(" = ")
        for xv in (1.7, -2.4):
            yv = peval(rhs, x=xv) - peval(lhs.replace("y", "0"))  # lhs is y or y ± c
            if not same(yv, float(m) * xv + float(b)): return False
        return True
    sel_auto(B, 1, "cp1", f"Select ALL equations of the line with slope {fr(m)} through (3, {fr(y0)}).", cands, ok, ["Point-slope and slope-intercept forms describe the same line.", f"b = {fr(y0)} - {fr(m)}(3) = {fr(b)}."])
B.orq(1, "honors", "Line L passes through (-2, 7) and (4, -2).", [("Find the slope.", "-3/2"), ("Write L in point-slope form.", "y - 7 = -(3/2)(x + 2)"), ("Write L in standard form with integer coefficients.", "3x + 2y = 8"), ("Find the x- and y-intercepts.", "(8/3, 0) and (0, 4)")],
      ["(-2 - 7)/(4 + 2).", "Use (-2, 7).", "Multiply by 2 and rearrange.", "Set y = 0, then x = 0."], tags=["multiple-representations"])
assert 3 * -2 + 2 * 7 == 8 and 3 * 4 + 2 * -2 == 8

# ---- Skill 2: slope and rate of change ----
for (x1, y1), (x2, y2) in [((-3, 4), (5, -2)), ((2, 2), (2, 9)), ((-1, 6), (7, 6)), ((0, -5), (4, 3))]:
    if x1 == x2: ans, wr = "undefined", ["0", "7", "-7"]
    else:
        m = F(y2 - y1, x2 - x1); ans = fr(m); wr = [fr(1 / m) if m else "undefined", fr(-m) if m else "1", fr(F(x2 - x1, y2 - y1)) if y2 != y1 and F(x2 - x1, y2 - y1) != m else fr(m + 1)]
    B.mc(2, "cp2", f"Find the slope of the line through {pt(x1, y1)} and {pt(x2, y2)}.", ans, wr, ["m = (y₂ - y₁)/(x₂ - x₁).", "Vertical lines have undefined slope; horizontal lines have slope 0."], tags=["misconception"])
sel_auto(B, 2, "cp1", "Select ALL lines parallel to 2x - 5y = 10.", ["y = (2/5)x + 7", "4x - 10y = 3", "y = (2/5)x", "y = -(5/2)x + 1", "y = (5/2)x - 2", "2x + 5y = 10"], lambda s_: s_ in ("y = (2/5)x + 7", "4x - 10y = 3", "y = (2/5)x"), ["Slope of 2x - 5y = 10 is 2/5.", "Parallel lines have equal slopes."])
sel_auto(B, 2, "cp1", "Select ALL lines perpendicular to y = -4x + 1.", ["y = (1/4)x", "x - 4y = 8", "y = 0.25x - 3", "y = 4x", "y = -(1/4)x", "4x + y = 2"], lambda s_: s_ in ("y = (1/4)x", "x - 4y = 8", "y = 0.25x - 3"), ["Perpendicular slopes are negative reciprocals: 1/4."])
for tbl, rate in [("t (h): 0, 2, 5; d (mi): 10, 130, 310", "60 mi/h"), ("x: 1, 4, 10; cost: $14, $26, $50", "$4 per item"), ("week: 0, 3, 8; height (cm): 12, 18.6, 29.6", "2.2 cm/week")]:
    B.orq(2, "cp1", f"Table — {tbl}.", [("Find the rate of change between the first two points.", rate), ("Find the rate between the last two points.", rate), ("Is the relationship linear?", "Yes, constant rate"), ("Find the starting (initial) value.", tbl.split("; ")[1].split(": ")[1].split(", ")[0])],
          ["Δy/Δx.", "Δy/Δx.", "Rates are equal.", "Value at the first input (0) or extrapolate."], tags=["multiple-representations"])
B.orq(2, "honors", "Average rate of change of f(x) = x² - 2x.", [("On [0, 2].", "0"), ("On [1, 4].", "3"), ("On [a, a + 1] in terms of a.", "2a - 1"), ("Why do these differ for f but not for a linear function?", "f is not linear, so its rate of change varies")],
      ["(0 - 0)/2.", "(8 - (-1))/3.", "((a + 1)² - 2(a + 1) - a² + 2a)/1.", "Linear functions have constant slope."], tags=["connections"])
B.mc(2, "cp1", "A student computes the slope through (2, 5) and (6, 1) as (6 - 2)/(1 - 5) = -1. What is wrong?", "The ratio is upside down; the slope is (1 - 5)/(6 - 2) = -1 — the answer is right by coincidence", ["Nothing is wrong", "The slope is 1", "The slope is -4"], ["Slope is Δy/Δx; here both give -1 only because |Δy| = |Δx|."], tags=["error-analysis"])
B.sa(2, "cp2", "What is the slope of y = 7?", "0", ["Horizontal line."])
B.sa(2, "cp1", "Find k so the line through (1, k) and (4, 10) has slope 2.", "k = 4", ["(10 - k)/3 = 2."])

# ---- Skill 3: writing linear models ----
for ctx, m, b, unit, q in [("A plant is 6 cm tall and grows 1.5 cm per week.", 1.5, 6, "week", 10), ("A tank has 500 L and drains 12 L per minute.", -12, 500, "minute", 20), ("A tutor charges $20 plus $35 per hour.", 35, 20, "hour", 3),
                           ("A car's odometer reads 24,000 mi and it is driven 1,100 mi per month.", 1100, 24000, "month", 6), ("A phone has 80% battery and loses 6% per hour.", -6, 80, "hour", 7)]:
    val = m * q + b
    B.orq(3, "cp1", ctx, [("Write a linear model.", f"y = {m:g}x + {b:g}".replace("+ -", "- ")), ("Interpret the slope.", f"{abs(m):g} per {unit} ({'increase' if m > 0 else 'decrease'})"), (f"Find y when x = {q}.", f"{val:g}"), ("Interpret the y-intercept.", f"starting value {b:g}")],
          ["Starting value + rate·x.", "Rate of change.", "Substitute.", "Value when x = 0."], tags=["modeling"])
for pts_, eq in [(((2, 50), (6, 90)), "y = 10x + 30"), (((0, 18), (5, 3)), "y = -3x + 18"), (((10, 4), (30, 9)), "y = 0.25x + 1.5"), (((1, 2.5), (4, 7)), "y = 1.5x + 1")]:
    (x1, y1), (x2, y2) = pts_; m = (y2 - y1) / (x2 - x1); b = y1 - m * x1
    assert eq == f"y = {m:g}x + {b:g}".replace("+ -", "- "), eq
    B.mc(3, "cp1", f"A linear model passes through ({x1}, {y1:g}) and ({x2}, {y2:g}). Which equation is it?", eq, [f"y = {1 / m:g}x + {b:g}", f"y = {m:g}x + {y1:g}", f"y = {-m:g}x + {b:g}"], ["Slope from the two points; then solve for b."], tags=["modeling"])
sel_auto(B, 3, "cp1", "A gym's cost is C = 25m + 50 (m months). Select ALL true statements.", ["The sign-up fee is $50", "The monthly rate is $25", "C(12) = 350", "After 6 months the cost is $200", "The monthly rate is $50", "C is exponential"],
         lambda s_: s_ in ("The sign-up fee is $50", "The monthly rate is $25", "C(12) = 350", "After 6 months the cost is $200"), ["Intercept 50, slope 25.", "25·12 + 50 = 350; 25·6 + 50 = 200."], tags=["modeling"])
B.orq(3, "honors", "Data: (1, 3.1), (2, 4.9), (3, 7.2), (4, 8.8), (5, 11.0).", [("Find the line through the first and last points.", "y = 1.975x + 1.125"), ("Use it to predict y at x = 8.", "16.925"), ("Is the trend linear? Explain.", "Roughly: differences are near 2 each step"),
      ("What does a residual measure?", "Actual y minus predicted y")], ["(11.0 - 3.1)/4 = 1.975.", "Substitute.", "Nearly constant first differences.", "Vertical distance from the line."], tags=["modeling"])
B.mc(3, "cp1", "Which situation is NOT well modeled by a linear function?", "A bacteria population that doubles every hour", ["Pay of $15 per hour", "Distance at a constant 50 mph", "Water level dropping 2 in per day"], ["Doubling is a constant ratio (exponential)."])
B.sa(3, "cp2", "A movie streaming service costs $11 per month. Write the total cost after m months.", "C = 11m", ["Rate × months."], tags=["modeling"])
B.sa(3, "honors", "Two plans: A charges $40 + $0.10/min; B charges $0.25/min. For how many minutes do they cost the same?", "≈ 266.7 minutes (about 267)", ["40 + 0.1m = 0.25m → 0.15m = 40."], tags=["modeling"])

# ---- Skill 4: systems by graphing and substitution ----
for (m1, b1), (m2, b2) in [((2, -3), (-1, 6)), ((F(1, 2), 1), (-2, 11)), ((3, 4), (3, -1)), ((-1, 5), (F(-1, 3), 1))]:
    if m1 == m2: ans = "no solution"; xs = None
    else:
        xs = F(b2 - b1) / (F(m1) - F(m2)); ys = F(m1) * xs + b1; ans = pt(xs, ys)
    B.mc(4, "cp1", f"Solve by substitution: {line(m1, b1)} and {line(m2, b2)}.", ans, [pt(ys, xs) if xs is not None and xs != ys else "infinitely many solutions", "infinitely many solutions" if xs is not None else pt(0, b1), pt(xs, F(m2) * xs + b1) if xs is not None else pt(1, 1)],
         ["Set the expressions for y equal.", "Solve for x, then substitute to find y.", "Parallel lines (same slope, different intercept) never meet."])
dg = graph(B, "s04-topup-graph-system", [(lambda v: 0.5 * v + 2, {}), (lambda v: -2 * v + 7, {"color": "#c0392b"})], points=[(2, 3, True, "(2, 3)")], alt="Blue line y = (1/2)x + 2 and red line y = -2x + 7 crossing at (2, 3).")
B.orq(4, "cp1", "The graph shows two lines.", [("Write the blue line's equation.", "y = (1/2)x + 2"), ("Write the red line's equation.", "y = -2x + 7"), ("Find the solution of the system.", "(2, 3)"), ("Verify algebraically.", "(1/2)(2) + 2 = 3 and -2(2) + 7 = 3")],
      ["Read the intercept and slope.", "Read the intercept and slope.", "Intersection point.", "Substitute into both."], diagram=dg, tags=["graph"])
sel_auto(B, 4, "cp1", "Select ALL systems with exactly one solution.", ["y = 2x + 1 and y = -x + 4", "y = 3x and x + y = 8", "2x + y = 5 and x - y = 1", "y = x + 2 and y = x - 3", "y = 2x + 1 and 4x - 2y = -2", "x = 3 and x = -1"],
         lambda s_: s_ in ("y = 2x + 1 and y = -x + 4", "y = 3x and x + y = 8", "2x + y = 5 and x - y = 1"), ["Different slopes → one solution.", "Same slope and intercept → infinitely many; same slope, different intercept → none."])
B.orq(4, "honors", "Solve: y = x² - 2x and y = x + 4.", [("Substitute.", "x² - 2x = x + 4"), ("Solve the quadratic.", "x = 4 or x = -1"), ("Find the points.", "(4, 8) and (-1, 3)"), ("How many intersection points are possible for a line and a parabola?", "0, 1, or 2")],
      ["Set equal.", "x² - 3x - 4 = (x - 4)(x + 1).", "Use y = x + 4.", "A quadratic has at most 2 real roots."], tags=["connections"])
B.mc(4, "cp1", "A student solves y = 3x - 2 and 2x + y = 8 and gets x = 2, then reports the solution as x = 2. What is missing?", "The y-value: the solution is (2, 4)", ["Nothing", "x = 6", "The solution is (4, 2)"], ["A solution of a system is an ordered pair."], tags=["error-analysis"])
B.sa(4, "cp1", "Solve by substitution: x = 2y + 1 and 3x - 4y = 9.", "(7, 3)", ["3(2y + 1) - 4y = 9 → 2y = 6."])
B.sa(4, "honors", "For what k does y = kx + 2 and y = 3x - 5 have no solution?", "k = 3", ["Same slope, different intercepts."], tags=["reasoning"])
B.sa(4, "cp2", "Is (1, 4) a solution of y = 2x + 2 and y = -x + 5?", "Yes", ["4 = 4 and 4 = 4."])

# ---- Skill 5: elimination ----
found = 0
import random
_combos = list(itertools.product([2, 3, 5], [1, -2, 4], [1, -3, 4], [3, 5, -1], [-2, 1, 3], [-1, 2, 4])); random.Random(22).shuffle(_combos)
for a1, b1, a2, b2, xs, ys in _combos:
    det = a1 * b2 - a2 * b1
    if det == 0 or found >= 6 or (a1 + b1 + a2 + b2 + xs + ys) % 4: continue
    found += 1
    c1, c2 = a1 * xs + b1 * ys, a2 * xs + b2 * ys
    e1, e2 = std_form(a1, b1, c1), std_form(a2, b2, c2)
    B.mc(5, "cp1", f"Solve by elimination: {e1} and {e2}.", pt(xs, ys), [pt(ys, xs) if xs != ys else pt(-xs, ys), pt(-xs, -ys), pt(xs, -ys)], ["Multiply one or both equations so a variable has opposite coefficients.", "Add to eliminate, solve, then back-substitute."])
sel_auto(B, 5, "cp1", "To eliminate y from 3x + 2y = 7 and 5x - 4y = 19, select ALL valid first steps.", ["Multiply the first equation by 2, then add", "Multiply the first by 4 and the second by 2, then add", "Multiply the second equation by 2, then add", "Multiply the second by 3, then add"],
         lambda s_: s_ in ("Multiply the first equation by 2, then add", "Multiply the first by 4 and the second by 2, then add"), ["The y-coefficients 4y and -4y cancel after doubling the first equation.", "4(2y) + 2(-4y) = 0 also works."])
B.orq(5, "cp1", "Tickets: adult $9, child $6. 300 tickets sold for $2,250.", [("Write the system.", "a + c = 300; 9a + 6c = 2250"), ("Eliminate a variable.", "Multiply the first by 6 and subtract: 3a = 450"), ("Solve.", "a = 150, c = 150"), ("Check.", "9(150) + 6(150) = 2250")], ["Count and value.", "6a + 6c = 1800.", "Back-substitute.", "Substitute."], tags=["modeling"])
B.orq(5, "honors", "Solve the 3×3 system: x + y + z = 6; 2x - y + z = 3; x + 2y - z = 2.", [("Eliminate z using equations 1 and 3.", "2x + 3y = 8"), ("Eliminate z using equations 2 and 3.", "3x + y = 5"), ("Solve the 2×2 system.", "x = 1, y = 2"), ("Find z.", "z = 3")], ["Add (1) and (3).", "Add (2) and (3).", "Elimination.", "Back-substitute."], tags=["challenge"])
assert 1 + 2 + 3 == 6 and 2 - 2 + 3 == 3 and 1 + 4 - 3 == 2
B.mc(5, "cp1", "Eliminating gives 0 = 5. What does this mean?", "The system has no solution (parallel lines)", ["The solution is (0, 5)", "Infinitely many solutions", "x = 5"], ["A false statement means inconsistent."])
B.mc(5, "cp1", "Eliminating gives 0 = 0. What does this mean?", "Infinitely many solutions (same line)", ["No solution", "The solution is (0, 0)", "x = 0"], ["A true statement with no variables means the equations are equivalent."])
B.sa(5, "honors", "A boat travels 36 mi downstream in 2 h and returns upstream in 3 h. Find the boat's speed and the current.", "boat 15 mph, current 3 mph", ["b + c = 18, b - c = 12.", "Add: 2b = 30."], tags=["modeling"])

# ---- Skill 6: linear inequalities and systems ----
for ineq, pred, cands in [("y ≤ -x + 4", lambda a, b: b <= -a + 4, ["(0, 0)", "(2, 2)", "(3, 2)", "(-1, 6)", "(5, -1)", "(4, 1)"]), ("2x - 3y > 6", lambda a, b: 2 * a - 3 * b > 6, ["(4, 0)", "(0, -3)", "(3, 0)", "(6, 1)", "(0, 0)", "(1, -2)"])]:
    sel_auto(B, 6, "cp1", f"Select ALL points that satisfy {ineq}.", cands, lambda s_, pred=pred: pred(*[int(t) for t in s_.strip("()").split(", ")]), ["Substitute; boundary points count only for ≤ or ≥."])
for sysd, pred, cands in [("y > x - 2 and y ≤ -2x + 4", lambda a, b: b > a - 2 and b <= -2 * a + 4, ["(0, 0)", "(1, 2)", "(2, 0)", "(-1, 5)", "(3, -1)", "(0, 4)"]), ("x + y < 5, x ≥ 0, y ≥ 1", lambda a, b: a + b < 5 and a >= 0 and b >= 1, ["(0, 1)", "(2, 2)", "(1, 3)", "(4, 1)", "(-1, 2)", "(3, 0)"])]:
    sel_auto(B, 6, "cp1", f"Select ALL solutions of the system {sysd}.", cands, lambda s_, pred=pred: pred(*[int(t) for t in s_.strip("()").split(", ")]), ["A solution must satisfy every inequality."])
dg = graph(B, "s06-topup-shade", [(lambda v: 2 * v - 1, {"ls": "--"})], shade=lambda X, Y: Y > 2 * X - 1, alt="A dashed line y = 2x - 1 with the region above it shaded.")
B.mc(6, "cp1", "Which inequality is graphed?", "y > 2x - 1", ["y ≥ 2x - 1", "y < 2x - 1", "y > -2x - 1"], ["Dashed boundary → strict inequality.", "Shading above → y >."], diagram=dg, tags=["graph"])
dg2 = graph(B, "s06-topup-shade2", [(lambda v: -0.5 * v + 3, {})], shade=lambda X, Y: Y <= -0.5 * X + 3, alt="A solid line y = -(1/2)x + 3 with the region below it shaded.")
B.mc(6, "cp1", "Which inequality is graphed?", "y ≤ -(1/2)x + 3", ["y < -(1/2)x + 3", "y ≥ -(1/2)x + 3", "y ≤ (1/2)x + 3"], ["Solid boundary → ≤ or ≥.", "Shading below → y ≤."], diagram=dg2, tags=["graph"])
B.orq(6, "cp1", "Graph x + 2y ≤ 8.", [("Write the boundary in slope-intercept form.", "y = -(1/2)x + 4"), ("Solid or dashed?", "solid"), ("Test (0, 0).", "0 ≤ 8: true"), ("Which side is shaded?", "the side containing the origin (below)")], ["Solve for y.", "≤ includes the line.", "Substitute.", "Shade the true side."], tags=["graph"])
B.orq(6, "honors", "A student budget: x hours tutoring ($15/h) and y hours retail ($12/h), with x + y ≤ 20 and earnings at least $270.", [("Write the earnings inequality.", "15x + 12y ≥ 270"), ("Is (10, 10) a solution?", "Yes: 20 ≤ 20 and 270 ≥ 270"), ("Is (5, 12) a solution?", "No: 219 < 270"), ("Find the minimum tutoring hours if y = 0.", "18")],
      ["Rate × hours.", "Check both.", "75 + 144 = 219.", "15x ≥ 270."], tags=["modeling"])
B.mc(6, "cp1", "When solving -3x + 6 > 12, a student gets x > -2. What is correct?", "x < -2 (flip the inequality when dividing by a negative)", ["x > -2", "x < 2", "x > 6"], ["-3x > 6 → x < -2."], tags=["error-analysis", "misconception"])
B.sa(6, "cp2", "Is (2, 1) a solution of y < x?", "Yes", ["1 < 2."])
B.sa(6, "cp1", "Write the inequality for the region above the solid line through (0, -2) with slope 3.", "y ≥ 3x - 2", ["Solid → ≥; above → y ≥."])

# ---- Skill 7: linear programming ----
LP = [("P = 4x + 3y", lambda x, y: 4 * x + 3 * y, [(0, 0), (0, 6), (3, 4), (5, 0)], "", "max"),
      ("C = 2x + 5y", lambda x, y: 2 * x + 5 * y, [(0, 8), (2, 4), (6, 0)], "", "min")]
for obj, f, verts, cons, kind in LP:
    vals = {v: f(*v) for v in verts}; best = (max if kind == "max" else min)(vals, key=vals.get)
    B.orq(7, "cp1", f"A feasible region has vertices {', '.join(pt(*v) for v in verts)}. Optimize {obj}.", [("Evaluate the objective at each vertex.", "; ".join(f"{pt(*v)}: {vals[v]}" for v in verts)), (f"Find the {kind}imum.", f"{vals[best]} at {pt(*best)}"),
          ("Why check only the vertices?", "A linear objective's optimum on a polygon occurs at a vertex"), ("Is the region bounded?", "Yes" if kind == "max" else "No (unbounded above)")],
          ["Substitute each vertex.", "Compare.", "Fundamental theorem of linear programming.", "Look at the region's shape."], tags=["modeling"])
for obj, f, verts, kind in [("P = 5x + 2y", lambda x, y: 5 * x + 2 * y, [(0, 0), (0, 5), (4, 3), (6, 0)], "max"), ("P = x + 4y", lambda x, y: x + 4 * y, [(0, 0), (0, 5), (4, 3), (6, 0)], "max"), ("C = 3x + y", lambda x, y: 3 * x + y, [(1, 6), (3, 2), (7, 1)], "min")]:
    vals = {v: f(*v) for v in verts}; best = (max if kind == "max" else min)(vals, key=vals.get)
    others = [v for v in verts if v != best]
    B.mc(7, "cp1", f"A feasible region has vertices {', '.join(pt(*v) for v in verts)}. Find the {kind}imum of {obj}.", f"{vals[best]} at {pt(*best)}", [f"{vals[v]} at {pt(*v)}" for v in others][:3], ["Evaluate the objective at every vertex and compare."])
sel_auto(B, 7, "cp1", "A bakery makes x cakes (2 h each) and y pies (1 h each) with at most 16 hours and at most 10 items. Select ALL feasible plans.", ["(4, 6)", "(6, 4)", "(0, 10)", "(8, 0)", "(7, 3)", "(5, 7)"],
         lambda s_: (lambda x, y: 2 * x + y <= 16 and x + y <= 10 and x >= 0 and y >= 0)(*[int(t) for t in s_.strip("()").split(", ")]), ["Check 2x + y ≤ 16 and x + y ≤ 10."], tags=["modeling"])
B.orq(7, "honors", "A farmer plants x acres of corn ($300 profit/acre) and y acres of soy ($200/acre) with x + y ≤ 100, x ≤ 60, and 2x + y ≤ 160.", [("List the vertices of the feasible region.", "(0, 0), (60, 0), (60, 40), (0, 100)"), ("Evaluate profit at each.", "0; 18,000; 26,000; 20,000"),
      ("Find the maximum profit.", "$26,000 at (60, 40)"), ("Which constraints are binding (equal) at the optimum?", "all three: x + y = 100, x = 60, 2x + y = 160")], ["Intersect boundary lines.", "Substitute.", "Largest.", "At (60, 40): 60 + 40 = 100, x = 60, 120 + 40 = 160."], tags=["modeling", "challenge"])
assert 300 * 60 + 200 * 40 == 26000 and 60 + 40 == 100 and 2 * 60 + 40 == 160
B.mc(7, "cp1", "In a linear programming problem, the constraints describe…", "the feasible region", ["the objective function", "the optimal value", "the slope of the objective"], ["Constraints are inequalities limiting the choices."])
B.sa(7, "cp1", "A company needs at least 30 units from machine A (5 units/h, $40/h) and machine B (3 units/h, $20/h), each running at most 6 h. Which vertex of the feasible region is (6, 0)? Is it feasible?", "Yes: 5(6) = 30 units", ["30 ≥ 30 and 6 ≤ 6."], tags=["modeling"])
B.sa(7, "honors", "Explain why an unbounded feasible region may have a minimum but no maximum for P = x + y with x, y ≥ 0.", "P grows without bound as x or y increases, but its least value occurs at a vertex", ["Objective increases in the unbounded direction."], tags=["reasoning"])

B.sel(3, "cp1", "A candle 30 cm tall burns 2.5 cm per hour. Select ALL true statements about h = 30 - 2.5t.", ["It burns out after 12 hours", "After 4 hours it is 20 cm tall", "The slope is -2.5 cm/h"], ["It burns out after 30 hours", "After 4 hours it is 10 cm tall", "The y-intercept is 2.5"], ["30 - 2.5t = 0 → t = 12.", "30 - 10 = 20."], tags=["modeling"])
B.sa(3, "honors", "A line of best fit for study hours h and score s is s = 4.2h + 61. Interpret the slope and predict the score for 6 hours. Is predicting for 30 hours reasonable?", "Each extra hour adds about 4.2 points; 86.2; no, 30 h is far outside the data (extrapolation)", ["Slope = rate.", "4.2(6) + 61 = 86.2.", "Predictions far outside the data are unreliable."], tags=["modeling", "reasoning"])
B.sel(6, "honors", "Select ALL systems whose solution region is empty.", ["y > x + 2 and y < x - 1", "x ≥ 4 and x < 2"], ["y > x and y < -x", "y ≥ 0 and x ≥ 0", "y < 3 and y > -3"], ["Parallel boundaries with shading facing away from each other; contradictory bounds."], tags=["reasoning"])
for obj, f, verts, kind in [("P = 2x + 3y", lambda x, y: 2 * x + 3 * y, [(0, 0), (0, 4), (3, 3), (5, 0)], "max"), ("C = 4x + 3y", lambda x, y: 4 * x + 3 * y, [(0, 10), (2, 4), (8, 0)], "min"), ("P = 6x + y", lambda x, y: 6 * x + y, [(0, 0), (0, 7), (2, 6), (4, 2), (5, 0)], "max")]:
    vals = {v: f(*v) for v in verts}; best = (max if kind == "max" else min)(vals, key=vals.get)
    B.sa(7, "cp1", f"Vertices of a feasible region: {', '.join(pt(*v) for v in verts)}. Find the {kind}imum of {obj} and where it occurs.", f"{vals[best]} at {pt(*best)}", ["Evaluate the objective at each vertex: " + "; ".join(f"{pt(*v)} → {vals[v]}" for v in verts) + "."])
B.sel(7, "cp1", "Constraints x ≥ 0, y ≥ 0, x + y ≤ 6, x ≤ 4. Select ALL vertices of the feasible region.", ["(0, 0)", "(4, 0)", "(4, 2)", "(0, 6)"], ["(6, 0)", "(2, 4)", "(4, 6)"], ["Intersections of boundary lines that satisfy all constraints.", "(6, 0) violates x ≤ 4."])
B.orq(7, "cp1", "A student sells bracelets ($4 profit) and necklaces ($6 profit). Each bracelet takes 1 h and each necklace 2 h; she has 16 h and materials for at most 10 items.", [("Write the constraints.", "x + 2y ≤ 16, x + y ≤ 10, x ≥ 0, y ≥ 0"), ("Find the vertices.", "(0, 0), (10, 0), (4, 6), (0, 8)"), ("Evaluate P = 4x + 6y.", "0, 40, 52, 48"), ("State the best plan.", "4 bracelets and 6 necklaces for $52")],
      ["Time and materials.", "Intersect x + 2y = 16 and x + y = 10.", "Substitute.", "Maximum."], tags=["modeling"])
assert 4 + 12 == 16 and 4 + 6 == 10 and 4 * 4 + 6 * 6 == 52

if __name__ == "__main__":
    p = B.write(); print(p, N0, "→", len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
