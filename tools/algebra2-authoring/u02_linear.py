from lib import *

STD = {1: ["F-LE.A.2", "A-CED.A.2"], 2: ["F-IF.B.6"], 3: ["F-LE.A.2", "S-ID.B.6"], 4: ["A-REI.C.6", "A-REI.D.11"],
       5: ["A-REI.C.5", "A-REI.C.6"], 6: ["A-REI.D.12"], 7: ["A-CED.A.3"]}
B = Bank("linear-functions-systems", "ls", STD)

def slope(p, q): return F(q[1] - p[1], q[0] - p[0])

# ---------------- Skill 1: linear equations in multiple forms ----------------
S = 1
for p, q in [((1, 3), (4, 9)), ((-2, 5), (2, -3)), ((0, -4), (6, 0)), ((-3, -1), (3, 3)), ((2, 7), (5, 7))]:
    m = slope(p, q); b = p[1] - m*p[0]
    B.sa(S, "cp2", f"Write the equation in slope-intercept form of the line through {pt(*p)} and {pt(*q)}.", f"y = {lin(m, b)}",
         [f"m = ({q[1]} - {p[1]})/({q[0]} - {p[0]}) = {num(m)}.", f"Use b = y - mx with {pt(*p)}: b = {p[1]} - ({num(m)})({p[0]}) = {num(b)}.", f"y = {lin(m, b)}."])
for A_, B_, C_ in [(2, 3, 12), (4, -2, 8), (-5, 10, 30), (3, 4, -24)]:
    m = F(-A_, B_); b = F(C_, B_)
    B.mc(S, "cp2", f"Rewrite {A_}x + {B_}y = {C_} in slope-intercept form.".replace("+ -", "- "), f"y = {lin(m, b)}",
         [f"y = {lin(-m, b)}", f"y = {lin(m, -b)}", f"y = {lin(F(A_, B_), F(C_, A_))}"],
         [f"Subtract {A_}x: {B_}y = {-A_}x + {C_}.", f"Divide every term by {B_}: y = {lin(m, b)}."])
for m, p in [(2, (3, -1)), (F(-1, 2), (4, 6)), (-3, (-2, 5))]:
    B.sa(S, "cp2", f"Write the point-slope equation of the line with slope {num(m)} through {pt(*p)}.",
         f"y - ({p[1]}) = {num(m)}(x - ({p[0]}))".replace("- (-", "+ (").replace("(+", "("),
         ["Point-slope form: y - y₁ = m(x - x₁).", f"Substitute m = {num(m)}, (x₁, y₁) = {pt(*p)}."])
for A_, B_, C_ in [(3, -4, 12), (5, 2, -20), (-2, 6, 18)]:
    xi, yi = F(C_, A_), F(C_, B_)
    B.sa(S, "cp1", f"Find the x- and y-intercepts of {A_}x + {B_}y = {C_}.".replace("+ -", "- "), f"x-intercept {pt(xi, 0)}, y-intercept {pt(0, yi)}",
         [f"Set y = 0: {A_}x = {C_} → x = {num(xi)}.", f"Set x = 0: {B_}y = {C_} → y = {num(yi)}."])
for m, b in [(F(2, 3), F(-5, 3)), (F(-3, 4), F(7, 2)), (F(1, 5), -2)]:
    # standard form with integer coefficients A>0
    den = sp.ilcm(m.denominator, b.denominator); A_ = -m*den; Bc = den; C_ = b*den
    if A_ < 0: A_, Bc, C_ = -A_, -Bc, -C_
    g = sp.igcd(sp.igcd(int(A_), int(Bc)), int(C_)); A_, Bc, C_ = int(A_/g), int(Bc/g), int(C_/g)
    B.sa(S, "cp1", f"Write y = {lin(m, b)} in standard form Ax + By = C with integers and A > 0.", f"{A_}x + {Bc}y = {C_}".replace("+ -", "- "),
         [f"Multiply by {den} to clear fractions.", "Move the x-term to the left side.", f"Make A positive: {A_}x + {Bc}y = {C_}".replace("+ -", "- ") + "."])
for p, m_, kind in [((2, -1), (3, 1), "parallel"), ((-4, 3), (2, 5), "perpendicular"), ((6, 0), (-1, 4), "perpendicular"), ((0, 7), (F(1, 2), 1), "parallel")]:
    mm = F(m_[0], m_[1]) if not isinstance(m_[0], F) else m_[0]
    ms = mm if kind == "parallel" else -1/mm
    b = p[1] - ms*p[0]
    B.mc(S, "cp1", f"Find the line through {pt(*p)} that is {kind} to y = {lin(mm, 2)}.", f"y = {lin(ms, b)}",
         [f"y = {lin(-1/mm if kind == 'parallel' else mm, p[1] - (-1/mm if kind == 'parallel' else mm)*p[0])}", f"y = {lin(-ms, p[1] + ms*p[0])}", f"y = {lin(ms, p[0] - ms*p[1])}"],
         [f"{'Parallel lines share the slope' if kind == 'parallel' else 'Perpendicular slopes are negative reciprocals'}: m = {num(ms)}.",
          f"b = {p[1]} - ({num(ms)})({p[0]}) = {num(b)}.", f"y = {lin(ms, b)}."])
B.sel(S, "cp1", "Select ALL equations that represent the same line as y = -2x + 6.",
      ["2x + y = 6", "y - 2 = -2(x - 2)", "x/3 + y/6 = 1"], ["y = 2x - 6", "y - 6 = -2(x - 6)", "x + 2y = 6"],
      ["2x + y = 6 → y = -2x + 6.", "y - 2 = -2x + 4 → y = -2x + 6.", "Intercept form with intercepts (3, 0) and (0, 6) matches.",
       "y - 6 = -2(x - 6) gives y = -2x + 18; x + 2y = 6 has slope -1/2."])
dg = graph(B, "s01-line-read", [(lambda v: -0.75*v + 3, {})], points=[(0, 3, True, "(0, 3)"), (4, 0, True, "(4, 0)")],
           alt="A line falling from left to right through (0, 3) and (4, 0).")
B.sa(S, "cp1", "Write the equation of the graphed line in standard form with integer coefficients.", "3x + 4y = 12",
     ["Slope = (0 - 3)/(4 - 0) = -3/4; y-intercept 3.", "y = -3/4x + 3 → multiply by 4: 4y = -3x + 12 → 3x + 4y = 12."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "A student writes the line through (2, 5) with slope 3 as y - 2 = 3(x - 5). What went wrong?",
     "The coordinates were swapped; it should be y - 5 = 3(x - 2)", ["Nothing; the equation is correct", "The slope should be -3", "It should be y + 5 = 3(x + 2)"],
     ["In y - y₁ = m(x - x₁), y₁ goes with y and x₁ goes with x.", "The point (2, 5) has x₁ = 2, y₁ = 5."], tags=["error-analysis"])
B.sa(S, "honors", "Find k so that the lines kx + 2y = 7 and 3x - 6y = 1 are perpendicular.", "k = 4",
     ["Slope of kx + 2y = 7: -k/2. Slope of 3x - 6y = 1: 3/6 = 1/2.", "Perpendicular: (-k/2)(1/2) = -1 → -k/4 = -1 → k = 4."], tags=["challenge"])
B.sa(S, "honors", "Find k so that the lines kx + 2y = 7 and 3x - 6y = 1 are parallel.", "k = -1",
     ["Parallel needs equal slopes: -k/2 = 1/2 → k = -1.", "Check they are not the same line: -x + 2y = 7 vs x - 2y = -1/3 → different intercepts."], tags=["challenge"])
B.sa(S, "honors", "The line through (a, 4) and (3, a) has slope -2. Find a.", "a = 2",
     ["(a - 4)/(3 - a) = -2 → a - 4 = -6 + 2a → a = 2.", "Check: (2 - 4)/(3 - 2) = -2 ✓."], tags=["challenge"])
B.mc(S, "honors", "Which line is the perpendicular bisector of the segment from (-2, 1) to (4, 5)?", "y = -3/2x + 9/2",
     ["y = 2/3x + 7/3", "y = -3/2x + 3", "y = 3/2x + 3/2"],
     ["Midpoint (1, 3); segment slope 4/6 = 2/3.", "Perpendicular slope -3/2.", "y - 3 = -3/2(x - 1) → y = -3/2x + 9/2."], tags=["connections"])
B.orq(S, "honors", "Line ℓ passes through A(0, 6) and B(8, 0).",
      [("Write ℓ in slope-intercept, point-slope (using B) and standard form.", "y = -3/4x + 6; y = -3/4(x - 8); 3x + 4y = 24"),
       ("Find the area of the triangle formed by ℓ and the axes.", "24"), ("Find the distance from the origin to ℓ.", "4.8"),
       ("Write the line through the origin perpendicular to ℓ and find where it meets ℓ.", "y = 4/3x; (2.88, 3.84)")],
      ["m = -6/8 = -3/4.", "Legs 6 and 8: area = 24.", "Hypotenuse 10; height to hypotenuse = 2·24/10 = 4.8.", "4/3x = -3/4x + 6 → 25/12 x = 6 → x = 2.88, y = 3.84."],
      tags=["connections", "multistep"])

# ---------------- Skill 2: slope and rate of change ----------------
S = 2
for p, q in [((1, 2), (5, 10)), ((-3, 4), (1, -4)), ((2, -6), (2, 5)), ((0, 3), (7, 3)), ((-5, -2), (5, 2))]:
    if p[0] == q[0]:
        B.mc(S, "cp2", f"What is the slope of the line through {pt(*p)} and {pt(*q)}?", "undefined", ["0", "11", "-11"],
             ["The run is 2 - 2 = 0; division by 0 is undefined.", "The line is vertical: x = 2."], tags=["misconception"])
    else:
        m = slope(p, q)
        B.mc(S, "cp2", f"What is the slope of the line through {pt(*p)} and {pt(*q)}?", num(m),
             [num(1/m) if m != 0 else "undefined", num(-m) if m != 0 else "1", num(F(q[0] - p[0] + 1, 1) if m == 0 else -1/m)],
             [f"m = (y₂ - y₁)/(x₂ - x₁) = ({q[1]} - {p[1]})/({q[0]} - {p[0]}).", f"m = {num(m)}."])
for f, a, b in [(x**2, 1, 4), (x**2 - 3*x, -1, 2), (2**x, 0, 3), (x**3, -2, 1)]:
    r = F(int(f.subs(x, b) - f.subs(x, a)), b - a)
    B.sa(S, "cp1", f"Find the average rate of change of f(x) = {fmt(f, x)} from x = {a} to x = {b}.", num(r),
         [f"f({b}) = {f.subs(x, b)} and f({a}) = {f.subs(x, a)}.", f"(f({b}) - f({a}))/({b} - ({a})) = {num(r)}."])
B.sa(S, "cp2", "A car's odometer reads 12,450 mi at 9 AM and 12,618 mi at 12 PM. Find the average rate of change and its units.", "56 miles per hour",
     ["Change in miles: 168.", "Change in time: 3 hours.", "168/3 = 56 mi/h."], tags=["modeling"])
B.mc(S, "cp1", "The table shows a water tank: t = 0, 5, 10, 15 min; volume = 600, 520, 440, 360 L. Interpret the rate of change.",
     "The tank loses 16 liters per minute", ["The tank gains 16 liters per minute", "The tank loses 80 liters per minute", "The tank loses 5 liters per minute"],
     ["Each 5 minutes the volume drops by 80 L.", "-80/5 = -16 L/min; negative means draining."], tags=["modeling", "multiple-representations"])
dg = graph(B, "s02-piecewise-rate", [(lambda v: 2*v if v <= 2 else (4 if v <= 5 else 4 - 2*(v - 5)), {"_dom": (0, 7)})],
           xr=(0, 8), yr=(0, 8), points=[(0, 0), (2, 4), (5, 4), (7, 0)],
           alt="Distance from home (miles, vertical) versus time (hours, horizontal): rises from (0, 0) to (2, 4), constant to (5, 4), then falls to (7, 0).")
for q, a, st in [("during the first 2 hours", "2 mi/h away from home", "(4 - 0)/(2 - 0) = 2."),
                 ("from t = 2 to t = 5", "0 mi/h (not moving)", "The distance stays 4."),
                 ("from t = 5 to t = 7", "-2 mi/h (returning home)", "(0 - 4)/(7 - 5) = -2."),
                 ("over the whole trip, t = 0 to t = 7", "0 mi/h", "Start and end at distance 0: (0 - 0)/7 = 0, even though the person moved.")]:
    B.sa(S, "cp1" if "whole" not in q else "honors", f"The graph shows distance from home (miles) versus time (hours). Find the rate of change {q}.", a,
         [st, "Rate of change = change in distance / change in time."], diagram=dg, tags=["graph", "modeling"])
B.sel(S, "cp1", "Select ALL lines with negative slope.", ["2x + 5y = 1", "y = -x/3 + 4", "the line through (-1, 4) and (3, -2)"],
      ["y = 7", "x - y = 3", "the line through (0, 0) and (-2, -6)"],
      ["2x + 5y = 1 → m = -2/5.", "m = -1/3.", "(-2 - 4)/(3 + 1) = -3/2.", "y = 7 has m = 0; x - y = 3 has m = 1; (-6 - 0)/(-2 - 0) = 3."])
B.mc(S, "cp1", "A student finds the slope through (2, 7) and (6, 3) as (3 - 7)/(2 - 6) = 1. What is the error?",
     "The x-values were subtracted in the opposite order; the slope is -1", ["No error", "Should be (6 - 2)/(3 - 7) = -1", "Slope must be positive"],
     ["Numerator and denominator must subtract in the same order.", "(3 - 7)/(6 - 2) = -4/4 = -1."], tags=["error-analysis"])
B.mc(S, "honors", "Runner A: d = 5t (meters, seconds). Runner B's data: t = 2, d = 12; t = 6, d = 36. Who is faster and by how much?",
     "Runner B, by 1 m/s", ["Runner A, by 1 m/s", "Runner B, by 6 m/s", "They run at the same speed"],
     ["A's rate is 5 m/s.", "B's rate is (36 - 12)/(6 - 2) = 6 m/s.", "6 - 5 = 1."], tags=["multiple-representations"])
B.sa(S, "honors", "For f(x) = x², find the average rate of change on [a, a + h] in terms of a and h.", "2a + h",
     ["((a + h)² - a²)/h = (2ah + h²)/h = 2a + h."], tags=["challenge", "connections"])
B.sa(S, "honors", "The average rate of change of g(x) = x² + bx on [1, 3] is 10. Find b.", "b = 6",
     ["g(3) - g(1) = (9 + 3b) - (1 + b) = 8 + 2b.", "(8 + 2b)/2 = 10 → b = 6."], tags=["challenge"])
B.orq(S, "honors", "World population (billions): 1960: 3.0, 1980: 4.4, 2000: 6.1, 2020: 7.8.",
      [("Find the average rate of change from 1960 to 1980.", "0.07 billion per year"), ("Find it from 2000 to 2020.", "0.085 billion per year"),
       ("Is a linear model appropriate? Explain.", "Not exactly; the rates are not constant"), ("Use the 2000–2020 rate to estimate 2030.", "8.65 billion")],
      ["1.4/20 = 0.07.", "1.7/20 = 0.085.", "The rates differ (0.07, 0.085, 0.085), so growth is not perfectly linear.", "7.8 + 10(0.085) = 8.65."], tags=["modeling"])

# ---------------- Skill 3: writing linear models ----------------
S = 3
for fixed, rate, unit, item in [(45, 12, "hour", "a plumber's bill"), (150, -6, "week", "the balance on a gift card"), (2.5, 1.75, "mile", "a taxi fare")]:
    B.sa(S, "cp2", f"{item.capitalize()} starts at ${fixed} and changes by ${rate} per {unit}. Write a linear model y in terms of x {unit}s.",
         f"y = {lin(sp.nsimplify(rate), sp.nsimplify(fixed))}".replace("y = ", "y = "),
         ["The starting value is the y-intercept and the constant change per unit is the slope.", f"y = {rate}x + {fixed}".replace("+ -", "- ")], tags=["modeling"])
for p, q, ctx in [((2, 230), (5, 335), ("months", "dollars saved")), ((10, 68), (30, 52), ("minutes", "°F of cooling coffee")),
                  ((100, 40), (250, 70), ("miles", "dollars of rental cost"))]:
    m = slope(p, q); b = p[1] - m*p[0]
    B.sa(S, "cp1", f"After {p[0]} {ctx[0]} there were {p[1]} {ctx[1]}; after {q[0]} {ctx[0]}, {q[1]}. Assuming a linear relationship, write the model and interpret the slope.",
         f"y = {lin(m, b)}; slope {num(m)} {ctx[1].split(' ')[0]} per {ctx[0][:-1]}",
         [f"m = ({q[1]} - {p[1]})/({q[0]} - {p[0]}) = {num(m)}.", f"b = {p[1]} - {num(m)}·{p[0]} = {num(b)}.", f"Slope means the change in {ctx[1]} for each 1 additional {ctx[0][:-1]}."], tags=["modeling"])
B.mc(S, "cp2", "A gym charges a $50 sign-up fee and $25 per month. Which equation models total cost C after m months?", "C = 25m + 50",
     ["C = 50m + 25", "C = 75m", "C = 25(m + 50)"], ["One-time fee → intercept 50.", "Monthly charge → slope 25."], tags=["modeling"])
B.mc(S, "cp1", "In the model h = -0.6t + 48 for the height (cm) of a burning candle after t hours, what does 48 represent?",
     "The candle's initial height", ["The rate at which the candle burns", "The time when the candle burns out", "The height after 1 hour"],
     ["48 is the value of h when t = 0."], tags=["modeling"])
B.sa(S, "cp1", "Using h = -0.6t + 48 for a candle's height (cm) after t hours, when does the candle burn out?", "80 hours",
     ["Set h = 0: -0.6t + 48 = 0.", "t = 48/0.6 = 80."], tags=["modeling"])
B.mc(S, "cp1", "Data roughly follow ŷ = 2.4x + 15. For x = 10 the observed value is 41. What is the residual?", "2", ["-2", "39", "41"],
     ["Predicted: 2.4(10) + 15 = 39.", "Residual = observed - predicted = 41 - 39 = 2."], tags=["modeling", "connections"])
B.sel(S, "cp1", "A line of best fit for hours studied (x) and test score (y) is ŷ = 4.5x + 62. Select ALL valid interpretations.",
      ["Each extra hour is associated with about 4.5 more points", "A student who studies 0 hours is predicted to score about 62", "The model predicts 80.0 for 4 hours"],
      ["Studying causes scores to rise by exactly 4.5", "Every student who studies 4 hours scores 80", "The model is valid for 40 hours of study"],
      ["Slope: predicted change per hour.", "Intercept: predicted score at x = 0.", "4.5(4) + 62 = 80.",
       "Correlation does not prove causation; predictions are averages; 40 hours is far outside the data (and predicts 242)."], tags=["modeling", "reasoning"])
B.sa(S, "honors", "A company's revenue was $2.1 million in 2018 and $3.3 million in 2024. Write a linear model with x = years since 2018 and predict when revenue reaches $5 million.",
     "R = 0.2x + 2.1; x = 14.5 (mid-2032)", ["m = (3.3 - 2.1)/6 = 0.2 million per year.", "0.2x + 2.1 = 5 → x = 14.5."], tags=["modeling"])
B.mc(S, "honors", "Celsius and Kelvin: 0°C = 273.15 K and 100°C = 373.15 K. Which statement is true?", "K = C + 273.15, so the slope is 1",
     ["K = 2.7315C", "K = 1.8C + 273.15", "K = C - 273.15"], ["Slope: (373.15 - 273.15)/100 = 1.", "Intercept 273.15."], tags=["connections"])
B.orq(S, "honors", "A tree is 1.2 m tall when planted and 3.0 m tall 4 years later.",
      [("Write a linear model for height h after t years.", "h = 0.45t + 1.2"), ("Predict the height at 10 years.", "5.7 m"),
       ("When will it be 6 m tall?", "t ≈ 10.7 years"), ("Give one reason the model may fail for t = 50.", "Growth slows as trees mature; linear growth cannot continue indefinitely")],
      ["m = 1.8/4 = 0.45.", "0.45(10) + 1.2 = 5.7.", "(6 - 1.2)/0.45 = 10.67.", "Extrapolation far beyond data is unreliable."], tags=["modeling"])

# ---------------- Skill 4: systems by graphing and substitution ----------------
S = 4
def sys_txt(a1, b1, c1, a2, b2, c2):
    return f"{a1}x + {b1}y = {c1} and {a2}x + {b2}y = {c2}".replace("+ -", "- ").replace("1x", "x").replace("1y", "y").replace(" -x", " -x")
for (m1, b1), (m2, b2) in [((2, -1), (-1, 5)), ((F(1, 2), 3), (-2, -2)), ((3, 4), (1, 0)), ((-1, 6), (F(1, 3), 2))]:
    xs = F(b2 - b1, 1) / (m1 - m2); ys = m1*xs + b1
    B.sa(S, "cp2", f"Solve by substitution: y = {lin(m1, b1)} and y = {lin(m2, b2)}.", pt(xs, ys),
         [f"Set the expressions equal: {lin(m1, b1)} = {lin(m2, b2)}.", f"Solve: x = {num(xs)}.", f"y = {lin(m1, b1).replace('x', '(' + num(xs) + ')')} = {num(ys)}.", "Check in the other equation."])
for x0, y0, a, c, d, e in [(2, 3, 2, 3, 1, -4), (-1, 4, 3, 1, -2, 5), (5, -2, 1, 4, 3, -1)]:
    # y = a x + (y0 - a x0) ; c x + d y = c x0 + d y0
    bb = y0 - a*x0; rhs = c*x0 + d*y0
    B.sa(S, "cp2", f"Solve the system: y = {lin(a, bb)} and {c}x + {d}y = {rhs}.".replace("+ -", "- ").replace(" 1x", " x").replace("+ 1y", "+ y"), pt(x0, y0),
         [f"Substitute y = {lin(a, bb)} into the second equation.", f"{c}x + {d}({lin(a, bb)}) = {rhs} → x = {x0}.".replace("+ -", "- "), f"Then y = {y0}."])
dg = graph(B, "s04-graph-system", [(lambda v: -v + 4, {}), (lambda v: 0.5*v - 2, {"color": "#b23a3a", "ls": "--"})], points=[(4, 0, True, "(4, 0)")],
           alt="Solid line y = -x + 4 and dashed line y = x/2 - 2 intersecting at (4, 0).")
B.mc(S, "cp2", "Use the graph to find the solution of the system y = -x + 4 and y = ½x - 2.", "(4, 0)", ["(0, 4)", "(0, -2)", "(2, 2)"],
     ["The solution is the intersection point.", "Check: -4 + 4 = 0 and ½·4 - 2 = 0."], diagram=dg, tags=["graph"])
for eqs, ans, st in [(("y = 3x - 2", "6x - 2y = 4"), "infinitely many solutions", "Substituting gives 6x - 6x + 4 = 4, a true statement: the lines coincide."),
                     (("y = -2x + 1", "4x + 2y = 7"), "no solution", "Substituting gives 4x - 4x + 2 = 7 → 2 = 7, false: parallel lines."),
                     (("x = 2y + 1", "3x - 6y = 3"), "infinitely many solutions", "3(2y + 1) - 6y = 3 → 3 = 3.")]:
    B.mc(S, "cp1", f"How many solutions does the system {eqs[0]} and {eqs[1]} have?", ans.capitalize(),
         [w for w in ["Exactly one solution", "No solution", "Infinitely many solutions", "Exactly two solutions"] if w.lower() != ans][:3], [st], tags=["reasoning"])
for (q, l), sols in [(("y = x² - 4", "y = 3x"), [(-1, -3), (4, 12)]), (("y = x² + 2x", "y = x + 6"), [(-3, 3), (2, 8)]),
                     (("y = -x² + 5", "y = 2x + 2"), [(-3, -4), (1, 4)]), (("x² + y² = 25", "y = x + 1"), [(-4, -3), (3, 4)])]:
    B.sa(S, "cp1" if "²+" not in q else "honors", f"Solve the system: {q} and {l}.", " and ".join(pt(*s) for s in sols),
         ["Substitute the linear expression for y into the other equation.", "Solve the resulting quadratic by factoring.",
          f"Back-substitute to find y: {', '.join(pt(*s) for s in sols)}."], tags=["connections"])
B.mc(S, "cp1", "Tickets: adults $12, students $7. 150 tickets sold for $1,400. How many adult tickets?", "70", ["80", "116", "50"],
     ["a + s = 150 and 12a + 7s = 1400.", "s = 150 - a → 12a + 1050 - 7a = 1400 → 5a = 350 → a = 70.", "80 is the number of student tickets."], tags=["modeling"])
B.sa(S, "cp1", "Two gyms: Gym A costs $40 to join plus $20/month; Gym B costs $10/month plus $100 to join. After how many months do they cost the same, and what is the cost?",
     "6 months; $160", ["40 + 20m = 100 + 10m → 10m = 60 → m = 6.", "Cost: 40 + 120 = 160."], tags=["modeling"])
B.sa(S, "honors", "For what value of k does the system y = 2x + k and y = x² have exactly one solution?", "k = -1",
     ["x² = 2x + k → x² - 2x - k = 0.", "One solution when the discriminant is 0: 4 + 4k = 0 → k = -1 (the line is tangent at (1, 1))."], tags=["challenge", "connections"])
B.sa(S, "honors", "Find a and b so that (2, -1) is the solution of ax + by = 7 and bx - ay = 4.", "a = 18/5, b = 1/5",
     ["Substitute x = 2, y = -1: 2a - b = 7 and 2b + a = 4.", "From the first, b = 2a - 7; substitute: 2(2a - 7) + a = 4 → 5a = 18 → a = 18/5.",
      "b = 36/5 - 35/5 = 1/5.", "Check: 2(18/5) - 1/5 = 35/5 = 7 ✓; 2/5 + 18/5 = 4 ✓."], tags=["challenge"])
B.orq(S, "honors", "Use the system y = x² - 2x - 3 and y = x + 1.",
      [("Sketch-level: how many intersection points do you expect, and why?", "Two; the line crosses the parabola"),
       ("Solve algebraically.", "(-1, 0) and (4, 5)"), ("Verify one solution in both equations.", "At (4, 5): 16 - 8 - 3 = 5 and 4 + 1 = 5"),
       ("For what values of c does y = x + c miss the parabola?", "c < -21/4")],
      ["The line passes through (-1, 0), a point on the parabola, and is not tangent.", "x² - 3x - 4 = 0 → x = 4, -1.", "Both equations give 5.",
       "x² - 3x - 3 - c = 0 has no real roots when 9 + 4(3 + c) < 0 → c < -21/4."], tags=["connections", "challenge"])

# ---------------- Skill 5: systems by elimination ----------------
S = 5
for (a1, b1, a2, b2), (x0, y0) in [((2, 3, 4, -3), (2, 1)), ((5, 2, 3, -2), (1, -3)), ((3, 4, 5, 4), (-2, 3)), ((4, -1, 2, 3), (3, 5)), ((7, 2, 3, 2), (0, -4))]:
    c1, c2 = a1*x0 + b1*y0, a2*x0 + b2*y0
    B.sa(S, "cp2", f"Solve by elimination: {sys_txt(a1, b1, c1, a2, b2, c2)}.", pt(x0, y0),
         [("The y-coefficients are opposites, so add the equations to eliminate y." if b1 == -b2 else
           "The y-coefficients are equal, so subtract the equations to eliminate y." if b1 == b2 else
           f"Multiply the first equation by {abs(b2 // b1)} so the y-coefficients become opposites, then add."),
          f"Solve for x: x = {x0}.", f"Substitute x = {x0} into either equation to get y = {y0}."])
for (a1, b1, a2, b2), (x0, y0) in [((3, 2, 2, 5), (4, -1)), ((5, -3, 4, 2), (3, 2)), ((6, 5, 4, 3), (-2, 4)), ((2, 7, 3, -4), (5, 1))]:
    c1, c2 = a1*x0 + b1*y0, a2*x0 + b2*y0
    B.sa(S, "cp1", f"Solve by elimination: {sys_txt(a1, b1, c1, a2, b2, c2)}.", pt(x0, y0),
         [f"Multiply the equations so the x-coefficients match: ×{a2} and ×{a1}.", "Subtract to eliminate x and solve for y.", f"y = {y0}; back-substitute to get x = {x0}."])
B.mc(S, "cp1", "When eliminating, a student gets 0 = 0. What does this mean?", "The equations describe the same line: infinitely many solutions",
     ["The solution is (0, 0)", "There is no solution", "The student made an error"], ["0 = 0 is always true, so every point on one line satisfies both."], tags=["reasoning"])
B.mc(S, "cp1", "Solve: 2x + 3y = 6 and 4x + 6y = 15.", "No solution", ["(3, 0)", "Infinitely many solutions", "(0, 2)"],
     ["Double the first: 4x + 6y = 12.", "Subtract from the second: 0 = 3, false → parallel lines."])
B.mc(S, "cp1", "A student solves 3x + 2y = 10 and x - 2y = 6 by adding and writes 4x = 4. What went wrong?",
     "The right sides were added incorrectly; 4x = 16, so x = 4", ["Should have subtracted; 2x = 4", "Nothing; x = 1", "Should multiply first; x = 2"],
     ["Adding: (3x + x) + (2y - 2y) = 10 + 6 → 4x = 16.", "x = 4, y = -1."], tags=["error-analysis"])
for (eqs, ans) in [(("x + y + z = 6", "2x - y + z = 3", "x + 2y - z = 2"), (1, 2, 3)),
                   (("x - y + 2z = 5", "2x + y - z = 1", "x + y + z = 6"), (1, 2, 3)),
                   (("2x + y - z = 3", "x - y + z = 0", "3x + 2y + z = 8"), (1, 2, 1))]:
    xx, yy, zz = sp.symbols("x y z")
    sol = sp.solve([sp.parse_expr(e.replace("=", "-(") + ")", transformations="all") for e in eqs], [xx, yy, zz])
    assert (sol[xx], sol[yy], sol[zz]) == ans, (eqs, sol)
    B.sa(S, "honors", f"Solve the 3 × 3 system: {eqs[0]}, {eqs[1]}, {eqs[2]}.", f"({ans[0]}, {ans[1]}, {ans[2]})",
         ["Eliminate one variable from two different pairs of equations to get a 2 × 2 system.", "Solve the 2 × 2 system.", "Back-substitute for the third variable and check in all three."],
         tags=["challenge"])
B.sa(S, "cp1", "A chemist mixes a 10% acid solution with a 40% acid solution to make 30 L of 20% solution. How many liters of each?",
     "20 L of 10% and 10 L of 40%", ["x + y = 30 and 0.10x + 0.40y = 6.", "Multiply the first by 0.10: 0.10x + 0.10y = 3; subtract: 0.30y = 3 → y = 10.", "x = 20."], tags=["modeling"])
B.sa(S, "cp1", "A boat goes 36 km downstream in 2 h and returns upstream in 3 h. Find the boat's speed in still water and the current's speed.",
     "15 km/h boat, 3 km/h current", ["b + c = 18 and b - c = 12.", "Add: 2b = 30 → b = 15; c = 3."], tags=["modeling"])
B.sa(S, "honors", "Find the quadratic y = ax² + bx + c through (1, 2), (-1, 6), and (2, 3).", "y = x² - 2x + 3",
     ["a + b + c = 2, a - b + c = 6, 4a + 2b + c = 3.", "Subtract the first two: 2b = -4 → b = -2.", "a + c = 4 and 4a + c = 7 → 3a = 3 → a = 1, c = 3."], tags=["connections", "challenge"])
B.sel(S, "honors", "Consider ax + 2y = 4 and 3x + 6y = b. Select ALL true statements.",
      ["If a = 1 and b = 12, there are infinitely many solutions", "If a = 1 and b ≠ 12, there is no solution", "If a ≠ 1, there is exactly one solution"],
      ["If a = 1 there is always exactly one solution", "If b = 0 there is no solution for any a"],
      ["Multiply the first by 3: 3ax + 6y = 12.", "Same slopes iff 3a = 3 → a = 1; then same line iff b = 12.", "a ≠ 1: different slopes → one solution, for any b."], tags=["reasoning"])
B.orq(S, "honors", "A café sells small coffees for $2 and large for $3.50. One morning it sold 120 coffees for $315.",
      [("Write a system.", "s + l = 120 and 2s + 3.5l = 315"), ("Solve by elimination.", "s = 70, l = 50"),
       ("Check your answer in context.", "70 + 50 = 120 and 140 + 175 = 315"), ("If revenue had been $320, explain why the answer is impossible.", "l = 53.33 is not a whole number")],
      ["Two unknowns, two facts.", "Multiply the first by 2 and subtract: 1.5l = 75 → l = 50.", "Substitute both values.", "1.5l = 80 → l = 160/3."], tags=["modeling"])

# ---------------- Skill 6: linear inequalities & systems ----------------
S = 6
for ineq, pts_in, pts_out in [("y > 2x - 1", ["(0, 0)", "(1, 3)"], ["(2, 3)", "(0, -1)"]), ("y ≤ -x + 3", ["(0, 0)", "(1, 2)"], ["(3, 1)", "(4, 0)"]),
                              ("3x + 2y ≥ 6", ["(2, 0)", "(4, 1)"], ["(0, 0)", "(1, 1)"])]:
    B.sel(S, "cp2", f"Select ALL points that are solutions of {ineq}.", pts_in, pts_out,
          ["Substitute each point and check the inequality.", "Points on the boundary count only when the inequality includes equality."])
for ineq, line, shade in [("y < 3x + 1", "dashed", "below"), ("y ≥ -½x + 2", "solid", "above"), ("x > -2", "dashed", "to the right"), ("y ≤ 4", "solid", "below")]:
    B.mc(S, "cp2", f"How is the graph of {ineq} drawn?", f"{line.capitalize()} boundary, shaded {shade}",
         [f"{('Solid' if line == 'dashed' else 'Dashed')} boundary, shaded {shade}", f"{line.capitalize()} boundary, shaded {({'below': 'above', 'above': 'below', 'to the right': 'to the left'}[shade])}",
          f"{('Solid' if line == 'dashed' else 'Dashed')} boundary, shaded {({'below': 'above', 'above': 'below', 'to the right': 'to the left'}[shade])}"],
         ["Strict inequalities (< or >) use a dashed line; ≤ or ≥ use a solid line.", f"Shade {shade} because of the direction of the inequality."])
dg = graph(B, "s06-system-ineq", [(lambda v: v + 1, {}), (lambda v: -2*v + 4, {"ls": "--"})],
           shade=lambda X, Y: (Y <= X + 1) & (Y > -2*X + 4), alt="Solid line y = x + 1 and dashed line y = -2x + 4 crossing at (1, 2). The region below the solid line and above the dashed line is shaded.",
           points=[(1, 2, False, "(1, 2)")])
B.mc(S, "cp1", "Which system is shown by the graph?", "y ≤ x + 1 and y > -2x + 4", ["y ≥ x + 1 and y > -2x + 4", "y ≤ x + 1 and y < -2x + 4", "y < x + 1 and y ≥ -2x + 4"],
     ["Solid line y = x + 1 with shading below → y ≤ x + 1.", "Dashed line y = -2x + 4 with shading above → y > -2x + 4."], diagram=dg, tags=["graph"])
B.sel(S, "cp1", "Using the graphed system, select ALL points in the solution region.", ["(3, 1)", "(4, 4)", "(2, 3)"], ["(0, 0)", "(1, 2)", "(-1, 5)"],
      ["(3, 1): 1 ≤ 4 ✓ and 1 > -2 ✓.", "(4, 4): 4 ≤ 5 ✓ and 4 > -4 ✓.", "(2, 3): 3 ≤ 3 ✓ and 3 > 0 ✓.", "(1, 2) is on the dashed line, so it is excluded; (0, 0) fails y > 4; (-1, 5) fails y ≤ 0."],
      diagram=dg, tags=["graph"])
for ineq, ans in [("-3x + 2y > 8", "y > (3/2)x + 4"), ("4x - 5y ≥ 10", "y ≤ (4/5)x - 2"), ("x - 2y < -6", "y > (1/2)x + 3")]:
    B.sa(S, "cp1", f"Solve {ineq} for y.", ans,
         ["Isolate the y-term.", "If you divide by a negative number, reverse the inequality sign." if "-5y" in ineq or "-2y" in ineq else "Divide by a positive coefficient; the sign stays the same.", ans])
B.mc(S, "cp1", "A student rewrites -2y > 6x - 4 as y > -3x + 2. What is the error?", "The sign should reverse: y < -3x + 2",
     ["No error", "It should be y > 3x - 2", "It should be y < 3x + 2"], ["Dividing by -2 reverses the inequality."], tags=["error-analysis"])
B.sa(S, "cp1", "Write an inequality: Concert tickets cost $15 (lawn) and $40 (seat). A family can spend at most $200. Use x lawn and y seat tickets.",
     "15x + 40y ≤ 200, x ≥ 0, y ≥ 0", ["Total cost is 15x + 40y.", "'At most' means ≤.", "Counts can't be negative."], tags=["modeling"])
B.sa(S, "honors", "Find the area of the region defined by y ≥ 0, y ≤ x, and x + y ≤ 6.", "9",
     ["Vertices: (0, 0), (6, 0), and the intersection of y = x with x + y = 6, which is (3, 3).", "Triangle with base 6 and height 3: area = ½·6·3 = 9."], tags=["challenge", "connections"])
B.sa(S, "honors", "Write a system of inequalities whose solution is the square with vertices (1, 1), (4, 1), (4, 4), (1, 4) (including its boundary).",
     "1 ≤ x ≤ 4 and 1 ≤ y ≤ 4", ["Vertical sides x = 1, x = 4; horizontal sides y = 1, y = 4.", "Include the boundary with ≤."], tags=["reasoning"])
B.mc(S, "honors", "Which system has no solution?", "y > 2x + 3 and y < 2x - 1", ["y > 2x + 3 and y > 2x - 1", "y < 2x + 3 and y > 2x - 1", "y ≥ x and y ≤ -x"],
     ["Parallel boundaries with y above the upper line and below the lower line cannot both hold.", "The others overlap (the last includes the origin)."], tags=["reasoning"])
B.orq(S, "honors", "A student needs at least 10 hours of study per week (x hours math, y hours history), with at least twice as much math as history, and no more than 15 total hours.",
      [("Write the system.", "x + y ≥ 10, x + y ≤ 15, x ≥ 2y, x ≥ 0, y ≥ 0"), ("Is (8, 4) a solution?", "Yes"),
       ("Is (6, 4) a solution? Which constraint fails?", "No; x ≥ 2y fails"), ("Find the maximum possible history hours.", "5 hours (x = 10, y = 5)")],
      ["Translate each condition.", "(8, 4): 12 total, 8 ≥ 8 ✓.", "6 < 8.", "Maximize y on x = 2y with x + y ≤ 15: 3y ≤ 15 → y = 5."], tags=["modeling"])

# ---------------- Skill 7: linear programming ----------------
S = 7
def lp(cons, obj, maximize=True):
    """Vertex search over integer-free feasible polygon. cons: list of (a,b,c) meaning a x + b y <= c."""
    import itertools
    verts = []
    for (a1, b1, c1), (a2, b2, c2) in itertools.combinations(cons, 2):
        det = a1*b2 - a2*b1
        if det == 0: continue
        xv = F(c1*b2 - c2*b1, det); yv = F(a1*c2 - a2*c1, det)
        if all(a*xv + b*yv <= c for a, b, c in cons): verts.append((xv, yv))
    verts = sorted(set(verts))
    vals = [(obj[0]*v[0] + obj[1]*v[1], v) for v in verts]
    best = max(vals) if maximize else min(vals)
    return verts, vals, best
problems = [
 ("x ≥ 0, y ≥ 0, x + y ≤ 8, 2x + y ≤ 12", [(-1, 0, 0), (0, -1, 0), (1, 1, 8), (2, 1, 12)], (3, 2), True, "P = 3x + 2y"),
 ("x ≥ 0, y ≥ 0, x + 2y ≤ 10, 3x + y ≤ 15", [(-1, 0, 0), (0, -1, 0), (1, 2, 10), (3, 1, 15)], (2, 5), True, "P = 2x + 5y"),
 ("x ≥ 1, y ≥ 2, x + y ≤ 7", [(-1, 0, -1), (0, -1, -2), (1, 1, 7)], (4, 1), True, "P = 4x + y"),
 ("x ≥ 0, y ≥ 0, x + y ≥ 4, x + 3y ≥ 6, x ≤ 6, y ≤ 6", [(-1, 0, 0), (0, -1, 0), (-1, -1, -4), (-1, -3, -6), (1, 0, 6), (0, 1, 6)], (5, 3), False, "C = 5x + 3y"),
]
for txt, cons, obj, mx, name in problems:
    verts, vals, best = lp(cons, obj, mx)
    vtxt = ", ".join(pt(*v) for v in verts)
    B.sa(S, "cp1", f"Find the {'maximum' if mx else 'minimum'} of {name} subject to {txt}.", f"{num(best[0])} at {pt(*best[1])}",
         [f"Graph the constraints; the vertices of the feasible region are {vtxt}.",
          "Evaluate the objective at each vertex: " + "; ".join(f"{pt(*v)} → {num(val)}" for val, v in vals) + ".",
          f"The {'largest' if mx else 'smallest'} value is {num(best[0])}."])
    B.sa(S, "cp2", f"List the vertices of the feasible region for {txt}.", vtxt,
         ["Find each intersection of two boundary lines.", "Keep only the intersection points that satisfy every constraint.", vtxt])
B.mc(S, "cp2", "In linear programming, where does the maximum of a linear objective over a bounded feasible region occur?", "At a vertex of the region",
     ["At the center of the region", "Where the objective equals 0", "At the origin"],
     ["Level lines of a linear objective slide across the region and leave it last at a corner (vertex)."])
B.mc(S, "cp2", "A bakery makes muffins (x) and cakes (y). Each muffin needs 1 cup of flour, each cake 3 cups, and 30 cups are available. Which is the flour constraint?",
     "x + 3y ≤ 30", ["3x + y ≤ 30", "x + 3y ≥ 30", "x + y ≤ 30"], ["Flour used = 1·x + 3·y.", "Available limits usage: ≤ 30."], tags=["modeling"])
B.orq(S, "cp1", "A farmer plants corn (x acres) and soybeans (y acres) on at most 100 acres. Corn needs 2 labor hours/acre and soybeans 1; at most 160 labor hours are available. Profit is $300/acre for corn and $200/acre for soybeans.",
      [("Write the constraints.", "x + y ≤ 100, 2x + y ≤ 160, x ≥ 0, y ≥ 0"), ("Find the vertices of the feasible region.", "(0, 0), (80, 0), (60, 40), (0, 100)"),
       ("Write the profit function.", "P = 300x + 200y"), ("Find the maximum profit.", "$26,000 at (60, 40)")],
      ["Land and labor constraints plus nonnegativity.", "x + y = 100 and 2x + y = 160 meet at (60, 40).",
       "P(0,0) = 0, P(80,0) = 24,000, P(60,40) = 26,000, P(0,100) = 20,000.", "Maximum at (60, 40)."], tags=["modeling"])
v, vals, best = lp([(-1, 0, 0), (0, -1, 0), (1, 1, 100), (2, 1, 160)], (300, 200))
assert best[0] == 26000
B.sa(S, "honors", "Maximize P = 2x + 2y subject to x ≥ 0, y ≥ 0, x + y ≤ 6, x + 3y ≤ 12. Explain why the answer is not unique.",
     "Maximum 12, attained at every point of the segment from (6, 0) to (3, 3)",
     ["Vertices: (0, 0), (6, 0), (3, 3), (0, 4).", "P = 12 at (6, 0) and at (3, 3).", "The objective is parallel to the edge x + y = 6, so every point on that edge gives 12."], tags=["challenge", "reasoning"])
B.sa(S, "honors", "For the region x ≥ 0, y ≥ 0, x + y ≤ 8, 2x + y ≤ 12, what values of k make P = kx + y maximized at (4, 4)?", "1 ≤ k ≤ 2",
     ["At (4, 4) the binding edges have slopes -1 (x + y = 8) and -2 (2x + y = 12).", "The level line y = -kx + P must have slope between those: -2 ≤ -k ≤ -1.", "So 1 ≤ k ≤ 2."], tags=["challenge"])
# verify and correct the last item
v, vals, best = lp([(-1, 0, 0), (0, -1, 0), (-1, -1, -6), (-2, -1, -8)], (4, 5), False)
assert best == (24, (6, 0)), best
B.mc(S, "honors", "Minimize C = 4x + 5y subject to x ≥ 0, y ≥ 0, x + y ≥ 6, 2x + y ≥ 8. What is the minimum?", "24 at (6, 0)",
     ["28 at (2, 4)", "40 at (0, 8)", "30 at (0, 6)"],
     ["The region is unbounded; its vertices are (0, 8), (2, 4), (6, 0).", "C(0, 8) = 40, C(2, 4) = 28, C(6, 0) = 24.",
      "C grows as you move further into the region, so the minimum is at a vertex: 24 at (6, 0). (0, 6) is not in the region: 2·0 + 6 < 8."], tags=["challenge"])
B.orq(S, "honors", "A company makes chairs (x) and tables (y). Each chair needs 2 h of carpentry and 1 h of finishing; each table needs 3 h of carpentry and 3 h of finishing. Up to 120 h of carpentry and 90 h of finishing are available. Profit: $40 per chair, $70 per table.",
      [("Write all constraints.", "2x + 3y ≤ 120, x + 3y ≤ 90, x ≥ 0, y ≥ 0"), ("Find the vertices.", "(0, 0), (60, 0), (30, 20), (0, 30)"),
       ("Find the maximum profit.", "$2,600 at (30, 20)"), ("If table profit rose to $90, does the best plan change?", "No: (30, 20) gives $3,000, still the maximum")],
      ["Carpentry and finishing limits.", "2x + 3y = 120 and x + 3y = 90 → x = 30, y = 20.", "P: 0, 2400, 2600, 2100.", "New P: 0, 2400, 3000, 2700 → still (30, 20)."],
      tags=["modeling", "multistep"])
v, vals, best = lp([(-1, 0, 0), (0, -1, 0), (2, 3, 120), (1, 3, 90)], (40, 70)); assert best == (2600, (30, 20))
v, vals, best = lp([(-1, 0, 0), (0, -1, 0), (2, 3, 120), (1, 3, 90)], (40, 90)); assert best == (3000, (30, 20))

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
