from lib import Bank, graph
from mathlite import *
import math

STD = {1: ["F-LE.A.1", "F-LE.A.2"], 2: ["F-IF.C.7e", "F-BF.B.3"], 3: ["F-BF.B.4a", "F-LE.A.4"], 4: ["F-LE.A.4"], 5: ["F-LE.A.4"],
       6: ["F-LE.A.4", "A-SSE.B.3c"], 7: ["F-LE.A.4"], 8: ["F-LE.B.5", "A-SSE.B.3c", "F-IF.C.8b"]}
B = Bank("exponential-logarithmic-functions", "el", STD)
L, ln, e = math.log10, math.log, math.e


def r2(v, d=2):
    return f"{v:,.{d}f}"


# ---------------- Skill 1: growth and decay ----------------
S = 1
for a, b in [(500, 1.04), (1200, 0.85), (80, 2), (3000, 0.5), (45, 1.125), (10000, 0.92)]:
    g = b > 1; pct = round(abs(b - 1) * 100, 2)
    B.mc(S, "cp2", f"y = {a:g}({b:g})^t. Is this growth or decay, and at what percent rate per unit time?", f"{'Growth' if g else 'Decay'}, {pct:g}%",
         [f"{'Decay' if g else 'Growth'}, {pct:g}%", f"{'Growth' if g else 'Decay'}, {b * 100:g}%", f"{'Growth' if g else 'Decay'}, {round(b * 100 - 100 if g else 100 - b * 100, 2) + 10:g}%"],
         [f"b = {b:g} {'> 1 → growth' if g else '< 1 → decay'}.", f"Rate = |b - 1| = {pct:g}%."])
for a, r, t, g in [(250, 6, 5, True), (18000, 15, 4, False), (1500, 3.5, 10, True), (90, 20, 3, False), (64000, 8, 7, False), (12, 50, 6, True)]:
    b = 1 + r / 100 if g else 1 - r / 100; v = a * b ** t
    B.sa(S, "cp1" if t > 3 else "cp2", f"A quantity starts at {a:,} and {'grows' if g else 'decays'} by {r:g}% per year. Write a model and find its value after {t} years (nearest hundredth).",
         f"y = {a:g}({b:g})^t; {r2(v)}", [f"Growth/decay factor b = 1 {'+' if g else '-'} {r / 100:g} = {b:g}.", f"y({t}) = {a:g}({b:g})^{t} ≈ {r2(v)}."], tags=["modeling"])
for pts_, (a, b) in [(((0, 3), (1, 6)), (3, 2)), (((0, 200), (2, 50)), (200, 0.5)), (((1, 12), (3, 108)), (4, 3)), (((2, 20), (4, 5)), (80, 0.5)), (((1, 15), (2, 22.5)), (10, 1.5))]:
    (x1, y1), (x2, y2) = pts_
    assert abs(a * b ** x1 - y1) < 1e-9 and abs(a * b ** x2 - y2) < 1e-9
    B.sa(S, "cp1" if x1 else "cp2", f"Write an exponential function y = ab^x through {pt(x1, y1) if isinstance(y1, int) else f'({x1}, {y1:g})'} and {f'({x2}, {y2:g})'}.", f"y = {a:g}({b:g})^x",
         [f"Divide: b{'' if x2 - x1 == 1 else '^' + str(x2 - x1)} = {y2:g}/{y1:g} → b = {b:g}.", f"a = {y1:g}/{b:g}{'' if x1 == 1 else '^' + str(x1)} = {a:g}." if x1 else f"a = {y1:g} (the value at x = 0)."])
B.mc(S, "cp1", "Which table shows exponential growth?", "x: 0, 1, 2, 3; y: 5, 10, 20, 40", ["x: 0, 1, 2, 3; y: 5, 10, 15, 20", "x: 0, 1, 2, 3; y: 40, 20, 10, 5", "x: 0, 1, 2, 3; y: 5, 6, 9, 14"],
     ["Exponential: constant ratio between consecutive outputs (here ×2).", "Constant differences → linear; ratio ½ → decay."], tags=["multiple-representations"])
B.mc(S, "cp1", "A population triples every 4 years. Which model gives the population after t years?", "P = P₀·3^(t/4)", ["P = P₀·3^(4t)", "P = P₀·(4/3)^t", "P = 3P₀·t/4"],
     ["After t years there are t/4 tripling periods."])
B.mc(S, "honors", "Which is the equivalent monthly growth rate of 12% annual growth (nearest hundredth of a percent)?", f"{(1.12 ** (1 / 12) - 1) * 100:.2f}%", ["1.00%", "12.00%", f"{(1.12 ** 12 - 1) * 100:.2f}%"],
     ["Monthly factor = 1.12^(1/12) ≈ " + f"{1.12 ** (1 / 12):.5f}.", "Not 12%/12 = 1%, because growth compounds."], tags=["challenge", "misconception"])
sel_auto(B, S, "cp1", "Select ALL functions that model exponential decay.", ["y = 4(0.7)^x", "y = 0.5(1/3)^x", "y = 100(1.02)^(-x)", "y = 3(2)^x", "y = 2(0.9)^(-x)", "y = -5x + 8", "y = 7(5/4)^x"],
         lambda s: s in ("y = 4(0.7)^x", "y = 0.5(1/3)^x", "y = 100(1.02)^(-x)"), ["Decay when the effective base is between 0 and 1 (and a > 0).", "(1.02)^(-x) = (1/1.02)^x; (0.9)^(-x) = (1/0.9)^x is growth.", "-5x + 8 is linear."])
sel_auto(B, S, "cp1", "y = 2400(0.88)^t models a car's value. Select ALL true statements.", ["The initial value is $2400", "The value drops 12% per year", "After 1 year the value is $2112", "The value drops by 88% per year", "The value is never 0", "After 2 years the value is $1824"],
         lambda s: s in ("The initial value is $2400", "The value drops 12% per year", "After 1 year the value is $2112", "The value is never 0"), ["a = 2400, b = 0.88 = 1 - 0.12.", "2400(0.88) = 2112; 2400(0.88)² = 1858.56, not 1824 (that is linear decrease).", "Exponential decay approaches but never reaches 0."], tags=["modeling", "misconception"])
assert abs(2400 * 0.88 - 2112) < 1e-9 and abs(2400 * 0.88 ** 2 - 1858.56) < 1e-9
B.sa(S, "honors", "Bacteria double every 20 minutes. Starting with 50, how many after 3 hours?", "25,600", ["3 hours = 180 min = 9 doublings.", "50·2⁹ = 25,600."], tags=["modeling"])
B.sa(S, "honors", "A substance has a half-life of 8 days. What percent remains after 30 days (nearest tenth)?", f"{100 * 0.5 ** (30 / 8):.1f}%", ["Remaining fraction = (1/2)^(30/8).", f"≈ {0.5 ** (30 / 8):.4f}."], tags=["modeling"])
B.orq(S, "cp1", "A town of 8,000 grows 2.5% per year.", [("Write a model.", "P = 8000(1.025)^t"), ("Find the population after 10 years (nearest whole).", f"{round(8000 * 1.025 ** 10):,}"),
                                                       ("What is the growth factor?", "1.025"), ("How does this differ from adding 200 people per year?", "Exponential growth adds more each year; linear adds a constant 200")],
      ["a = 8000, b = 1.025.", f"8000(1.025)^10 ≈ {8000 * 1.025 ** 10:.1f}.", "1 + 0.025.", "Percent change vs constant change."], tags=["modeling", "connections"])
B.orq(S, "honors", "Data: (0, 64), (1, 48), (2, 36), (3, 27).", [("Show the data are exponential.", "Each ratio is 3/4"), ("Write the model.", "y = 64(0.75)^x"), ("Find y when x = 5.", f"{64 * 0.75 ** 5:g}"), ("Find the percent decrease per step.", "25%")],
      ["48/64 = 36/48 = 27/36 = 0.75.", "a = 64, b = 0.75.", "64·0.75⁵.", "1 - 0.75."], tags=["multiple-representations"])
B.orq(S, "cp1", "Compare f(t) = 100 + 20t and g(t) = 100(1.15)^t.", [("Find f(5) and g(5) (nearest whole).", f"200 and {round(100 * 1.15 ** 5)}"), ("Find f(10) and g(10).", f"300 and {round(100 * 1.15 ** 10)}"),
      ("Which is larger at t = 2?", "f: 140 vs 132.25"), ("Which eventually exceeds the other? Why?", "g; exponential growth eventually outpaces linear growth")],
      ["Substitute.", "Substitute.", "100(1.15)² = 132.25.", "Constant ratio beats constant difference."], tags=["connections", "reasoning"])
assert abs(100 * 1.15 ** 2 - 132.25) < 1e-9
B.sa(S, "cp2", "Find the initial value and growth factor of y = 7(1.3)^x.", "initial value 7; growth factor 1.3", ["a = 7, b = 1.3."])
B.sa(S, "cp2", "A $20,000 car loses 10% of its value each year. Write a model for its value V after t years.", "V = 20000(0.9)^t", ["Decay factor 1 - 0.10 = 0.9."], tags=["modeling"])

# ---------------- Skill 2: graphing exponential functions ----------------
S = 2
gspecs = [(1, 2, 0, 0), (1, 0.5, 0, 0), (2, 2, 0, -3), (1, 3, -1, 0), (-1, 2, 0, 4), (3, 0.5, 2, 1)]
for a, b, h, k in gspecs:
    fn = lambda v, a=a, b=b, h=h, k=k: a * b ** (v - h) + k
    eq = f"y = {'' if a == 1 else '-' if a == -1 else a}({b:g})^{'x' if h == 0 else f'(x - {h})' if h > 0 else f'(x + {-h})'}{'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}"
    eq = eq.replace("(2)^", "2^").replace("(3)^", "3^")
    yint = fn(0); p2 = (h + 1, a * b + k)
    dg = graph(B, f"s02-exp-{a}-{b:g}-{h}-{k}".replace(".", "p").replace("--", "-m"), [(fn, {})], xr=(-5, 5), yr=(-6, 10), step=1, hlines=[k],
               points=[(0, yint, True, None), (h, a + k, True, pt(h, a + k)), p2], alt=f"Graph of an exponential function with horizontal asymptote y = {k}, passing through {pt(h, a + k)} and ({p2[0]}, {p2[1]:g}).")
    rng_ = f"y > {k}" if a > 0 else f"y < {k}"
    B.orq(S, "cp1" if (h or k) else "cp2", f"The graph shows {eq}.", [("State the horizontal asymptote.", f"y = {k}"), ("State the domain and range.", f"all real numbers; {rng_}"),
          ("Find the y-intercept.", f"{yint:g}" if abs(yint - round(yint, 4)) < 1e-9 else f"{yint:.3f}"), ("Increasing or decreasing?", "increasing" if (a > 0) == (b > 1) else "decreasing")],
          ["The asymptote is y = k.", "Exponentials accept every x; outputs stay on one side of the asymptote.", "Substitute x = 0.", "b > 1 rises (if a > 0); a reflection or 0 < b < 1 reverses."], diagram=dg, tags=["graph"])
    wrong = [eq.replace(f"({b:g})", f"({1 / b:g})").replace(f"{b:g}^", f"{1 / b:g}^") if b != 1 else eq + " + 1", eq.replace(" - 3", " + 3").replace(" + 4", " - 4").replace(" + 1", " - 1") if k else eq + " + 1",
             eq.replace("(x - 2)", "(x + 2)").replace("(x + 1)", "(x - 1)") if h else (eq.replace("y = ", "y = -") if a > 0 else eq.replace("y = -", "y = "))]
    B.mc(S, "cp1", "Which equation matches the graph?", eq, wrong, [f"Asymptote y = {k}; the point {pt(h, a + k)} fixes h and a.", f"The next point ({p2[0]}, {p2[1]:g}) shows the base {b:g}."], diagram=dg, tags=["graph"])
for b_, desc in [("2", "translate left 3"), ("0.5", "reflect over the x-axis and shift up 2")]:
    pass
for f_, g_, d in [("2^x", "2^(x + 3)", "shift left 3"), ("3^x", "3^x - 5", "shift down 5"), ("(1/2)^x", "-(1/2)^x", "reflect over the x-axis"), ("4^x", "4^(-x)", "reflect over the y-axis"),
                  ("e^x", "2e^(x - 1)", "vertical stretch by 2, shift right 1"), ("5^x", "5^(x - 2) + 4", "shift right 2, up 4")]:
    wr = {"shift left 3": ["shift right 3", "shift up 3", "shift down 3"], "shift down 5": ["shift left 5", "shift up 5", "shift right 5"],
          "reflect over the x-axis": ["reflect over the y-axis", "shift down 1", "vertical compression"], "reflect over the y-axis": ["reflect over the x-axis", "shift left 1", "no change"],
          "vertical stretch by 2, shift right 1": ["vertical stretch by 2, shift left 1", "horizontal stretch by 2, shift right 1", "shift up 2, shift right 1"], "shift right 2, up 4": ["shift left 2, up 4", "shift right 2, down 4", "shift up 2, right 4"]}[d]
    B.mc(S, "cp2" if "," not in d else "cp1", f"Describe the transformation from f(x) = {f_} to g(x) = {g_}.", d, wr, ["Inside the exponent: horizontal changes (opposite sign); outside: vertical changes.", d + "."])
sel_auto(B, S, "cp1", "Select ALL features shared by y = 2^x and y = 5^x.", ["y-intercept (0, 1)", "horizontal asymptote y = 0", "domain all real numbers", "range y > 0", "passes through (1, 2)", "decreasing"],
         lambda s: s in ("y-intercept (0, 1)", "horizontal asymptote y = 0", "domain all real numbers", "range y > 0"), ["b⁰ = 1 for every base.", "(1, b) differs; both increase."])
sel_auto(B, S, "honors", "f(x) = -3(2)^(x + 1) + 6. Select ALL true statements.", ["The asymptote is y = 6", "The range is y < 6", "f(0) = 0", "f is decreasing", "The range is y > 6", "f(-1) = 6"],
         lambda s: s in ("The asymptote is y = 6", "The range is y < 6", "f(0) = 0", "f is decreasing"), ["k = 6; reflection makes outputs < 6.", "f(0) = -3·2 + 6 = 0.", "f(-1) = -3 + 6 = 3."])
B.sa(S, "cp1", "Find the y-intercept and asymptote of y = 4(0.5)^x - 2.", "y-intercept 2; asymptote y = -2", ["y(0) = 4 - 2 = 2.", "k = -2."])
B.sa(S, "honors", "An exponential y = ab^x + k has asymptote y = 3 and passes through (0, 5) and (1, 7). Find a, b, k.", "a = 2, b = 2, k = 3", ["k = 3; a + 3 = 5 → a = 2.", "2b + 3 = 7 → b = 2."], tags=["challenge"])
B.mc(S, "honors", "For which value of b is y = b^x NOT an exponential function?", "b = 1", ["b = 1/2", "b = 3", "b = e"], ["1^x = 1 is constant (linear), so b ≠ 1 is required."], tags=["reasoning"])
B.mc(S, "cp1", "The graph of y = 2^x is translated so its asymptote is y = -4. Which could be the new function?", "y = 2^x - 4", ["y = 2^(x - 4)", "y = 2^(x + 4)", "y = -4·2^x"], ["Only a vertical shift moves the horizontal asymptote."], tags=["misconception"])
B.sa(S, "cp1", "Compare the average rates of change of y = 3^x on [0, 1] and [2, 3].", "2 and 18", ["(3 - 1)/1 = 2; (27 - 9)/1 = 18."], tags=["reasoning"])
B.sa(S, "cp2", "What is the horizontal asymptote of y = 7^x + 1?", "y = 1", ["k = 1."])

# ---------------- Skill 3: inverse relationship ----------------
S = 3
for b, ex, val in [(2, 5, 32), (3, 4, 81), (10, -2, F(1, 100)), (5, 0, 1), (4, F(1, 2), 2), (F(1, 3), -2, 9), (7, 1, 7), (8, F(2, 3), 4)]:
    B.sa(S, "cp2" if isinstance(ex, int) and ex >= 0 else "cp1", f"Write {frp(b)}^{frp(ex)} = {fr(val)} in logarithmic form.", f"{lb(b)}({fr(val)}) = {fr(ex)}",
         ["b^y = x ⇔ log_b(x) = y.", f"Base {fr(b)}, exponent {fr(ex)}, result {fr(val)}."])
    assert abs(float(b) ** float(ex) - float(val)) < 1e-12
for b, x_, y_ in [(6, 36, 2), (2, F(1, 8), -3), (10, 1000, 3), (9, 3, F(1, 2)), (5, 1, 0), (16, 8, F(3, 4))]:
    B.sa(S, "cp2" if y_ >= 0 and isinstance(y_, int) else "cp1", f"Write {lb(b)}({fr(x_)}) = {fr(y_)} in exponential form.", f"{b}^{frp(y_)} = {fr(x_)}", ["log_b(x) = y ⇔ b^y = x."])
    assert abs(b ** float(y_) - float(x_)) < 1e-12
for f_, inv in [("y = 3^x", "y = log₃(x)"), ("y = log₅(x)", "y = 5^x"), ("y = e^x", "y = ln(x)"), ("y = 2^(x - 1)", "y = log₂(x) + 1"), ("y = log(x) + 2", "y = 10^(x - 2)"), ("y = 4^x + 3", "y = log₄(x - 3)")]:
    wr = {"y = log₃(x)": ["y = x³", "y = 3/x", "y = log_x(3)"], "y = 5^x": ["y = x⁵", "y = log_x(5)", "y = 5x"], "y = ln(x)": ["y = 1/e^x", "y = log(x)", "y = e^(-x)"],
          "y = log₂(x) + 1": ["y = log₂(x - 1)", "y = log₂(x) - 1", "y = 2^(x + 1)"], "y = 10^(x - 2)": ["y = 10^x + 2", "y = 10^(x + 2)", "y = log(x - 2)"], "y = log₄(x - 3)": ["y = log₄(x) - 3", "y = log₄(x + 3)", "y = 4^(x - 3)"]}[inv]
    B.mc(S, "cp1" if "+" in f_ or "-" in f_ else "cp2", f"Find the inverse of {f_}.", inv, wr, ["Swap x and y, then solve for y.", f"Inverse: {inv}."])
for b in (2, 3, 0.5):
    fn = lambda v, b=b: b ** v; gn = lambda v, b=b: math.log(v) / math.log(b) if v > 0 else float("nan")
    dg = graph(B, f"s03-inverse-{b:g}".replace(".", "p"), [(fn, {}), (gn, {"color": "#c0392b"}), (lambda v: v, {"color": "#888888", "lw": 1, "ls": "--"})], xr=(-5, 9), yr=(-5, 9), step=1,
               points=[(0, 1), (1, 0), (1, b), (b, 1)], alt=f"Blue curve y = {b:g}^x and red curve y = log base {b:g} of x, reflections of each other across the dashed line y = x; points (0, 1), (1, 0), (1, {b:g}), ({b:g}, 1).")
    B.sel(S, "cp1", f"The graph shows y = {b:g}^x (blue) and y = {lb(b)}(x) (red). Select ALL true statements.", ["The graphs are reflections across y = x", "The red graph has a vertical asymptote x = 0", "(1, 0) is on the red graph", f"({b:g}, 1) is on the red graph"],
          ["The red graph has a horizontal asymptote y = 0", "(0, 1) is on the red graph", "Both graphs have domain all real numbers"],
          ["Inverse functions reflect across y = x, swapping coordinates.", "log has domain x > 0 and vertical asymptote x = 0.", f"(0, 1) and (1, {b:g}) are on the exponential graph."], diagram=dg, tags=["graph", "connections"])
B.mc(S, "cp1", "Simplify 5^(log₅ 12).", "12", ["5", "60", "log₅ 12"], ["b^(log_b x) = x because exponentials and logs are inverses."])
B.mc(S, "cp1", "Simplify log₇(7^(2x)).", "2x", ["7", "14x", "x²"], ["log_b(b^y) = y."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to x for x > 0.", ["10^(log x)", "ln(e^x)", "e^(ln x)", "log₂(2^x)", "log(x)·10", "e^x·ln(e)", "ln(x)·e"],
         lambda s: s in ("10^(log x)", "ln(e^x)", "e^(ln x)", "log₂(2^x)"), ["Compositions of inverse functions give back x.", "e^x·ln(e) = e^x; log(x)·10 and ln(x)·e are not x."])
B.sa(S, "honors", "f(x) = 2^(x + 3) - 1. Find f⁻¹(x) and its domain.", "f⁻¹(x) = log₂(x + 1) - 3; domain x > -1", ["x = 2^(y + 3) - 1 → x + 1 = 2^(y + 3).", "y + 3 = log₂(x + 1)."], tags=["challenge"])
B.orq(S, "honors", "Let f(x) = 3^x and g(x) = log₃(x).", [("Find f(2) and g(9).", "9 and 2"), ("Find g(f(4)).", "4"), ("State the domain and range of g.", "x > 0; all real numbers"), ("Explain why g(-3) is undefined.", "No power of 3 equals -3")],
      ["3² = 9 and log₃ 9 = 2.", "Inverses undo each other.", "Swap the domain and range of f.", "3^y > 0 for all y."], tags=["reasoning"])
B.sa(S, "cp2", "Write 10³ = 1000 in logarithmic form.", "log(1000) = 3", ["Common log: base 10."])

# ---------------- Skill 4: logarithm properties ----------------
S = 4
for expr, ans, lvl in [("log₂(8x)", "3 + log₂ x", "cp2"), ("log(x³y)", "3log x + log y", "cp1"), ("ln(x²/y⁵)", "2ln x - 5ln y", "cp1"), ("log₃(9/x)", "2 - log₃ x", "cp2"),
                       ("log(√x/(10y))", "(1/2)log x - 1 - log y", "honors"), ("ln(e³x⁴)", "3 + 4ln x", "cp1"), ("log₅(25x²y)", "2 + 2log₅ x + log₅ y", "cp1"), ("log(x(x + 1)²)", "log x + 2log(x + 1)", "honors")]:
    B.sa(S, lvl, f"Expand {expr}. Assume variables are positive.", ans, ["Product → sum; quotient → difference; power → coefficient.", f"Simplify logs of known powers: {ans}."])
for expr, ans, lvl in [("log 4 + log 25", "2", "cp2"), ("log₂ 40 - log₂ 5", "3", "cp2"), ("3log x + log y", "log(x³y)", "cp1"), ("2ln x - ln(x + 1)", "ln(x²/(x + 1))", "cp1"),
                       ("(1/2)log₃ x + 2log₃ y - log₃ z", "log₃(y²√x/z)", "honors"), ("log₆ 9 + log₆ 4", "2", "cp1"), ("ln 6 - ln 2 + ln 5", "ln 15", "cp1"), ("4log₂ x - 2log₂ y", "log₂(x⁴/y²)", "cp1")]:
    B.sa(S, lvl, f"Condense into a single logarithm (or evaluate): {expr}.", ans, ["Coefficients become exponents; sums become products; differences become quotients.", f"Result: {ans}."])
assert abs(L(4) + L(25) - 2) < 1e-12 and abs(math.log2(40) - math.log2(5) - 3) < 1e-12 and abs(math.log(9, 6) + math.log(4, 6) - 2) < 1e-12
for lhs, val in [("log₂ 5 ≈ 2.32 and log₂ 3 ≈ 1.58. Estimate log₂ 15.", "3.90"), ("log₂ 5 ≈ 2.32 and log₂ 3 ≈ 1.58. Estimate log₂(5/3).", "0.74"), ("log₂ 5 ≈ 2.32 and log₂ 3 ≈ 1.58. Estimate log₂ 45.", "5.48"), ("log₂ 5 ≈ 2.32 and log₂ 3 ≈ 1.58. Estimate log₂ 0.6.", "-0.74")]:
    B.sa(S, "cp1", lhs, val, ["Write the argument as products/quotients/powers of 3 and 5 (and 2).", f"Combine the given values: ≈ {val}."])
B.mc(S, "cp1", "A student writes log(x + y) = log x + log y. What is correct?", "log(x + y) cannot be split; log(xy) = log x + log y", ["The student is correct", "log(x + y) = log x · log y", "log(x + y) = (log x)(y)"], ["The product rule is about the log of a product, not a sum."], tags=["error-analysis", "misconception"])
B.mc(S, "cp1", "A student writes log₂(x³) = (log₂ x)³. What is correct?", "3log₂ x", ["(log₂ x)³", "log₂(3x)", "3 + log₂ x"], ["Power rule: log_b(x^n) = n·log_b x."], tags=["error-analysis"])
B.mc(S, "cp1", "Which equals (log 50)/(log 5)?", "log₅ 50", ["log 10", "log 45", "10"], ["Change of base: log_b a = log a / log b.", "Quotient of logs ≠ log of quotient."], tags=["misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to log₂ 12.", ["log₂ 3 + log₂ 4", "2 + log₂ 3", "log₂ 24 - 1", "log 12/log 2", "log₂ 6 + 1", "log₂ 3 · log₂ 4", "log₂ 10 + log₂ 2", "(log₂ 3)(2)"],
         lambda s: abs({"log₂ 3 + log₂ 4": math.log2(3) + 2, "2 + log₂ 3": 2 + math.log2(3), "log₂ 24 - 1": math.log2(24) - 1, "log 12/log 2": L(12) / L(2), "log₂ 6 + 1": math.log2(6) + 1,
                        "log₂ 3 · log₂ 4": math.log2(3) * 2, "log₂ 10 + log₂ 2": math.log2(10) + 1, "(log₂ 3)(2)": 2 * math.log2(3)}[s] - math.log2(12)) < 1e-9,
         ["12 = 3·4 = 2²·3 = 24/2 = 6·2.", "log₂ 3 · log₂ 4 = 2log₂ 3 ≠ log₂ 12; log₂ 10 + log₂ 2 = log₂ 20."])
sel_auto(B, S, "honors", "Select ALL true identities (b > 0, b ≠ 1, x, y > 0).", ["log_b(xy) = log_b x + log_b y", "log_b(x/y) = log_b x - log_b y", "log_b(x^n) = n·log_b x", "log_b(1/x) = -log_b x", "log_b(x + y) = log_b x · log_b y", "log_b x / log_b y = log_b(x - y)", "(log_b x)^n = n·log_b x"],
         lambda s: s in ("log_b(xy) = log_b x + log_b y", "log_b(x/y) = log_b x - log_b y", "log_b(x^n) = n·log_b x", "log_b(1/x) = -log_b x"), ["The three properties follow from exponent rules.", "1/x = x⁻¹ gives -log_b x."], tags=["reasoning"])
B.sa(S, "honors", "Prove log_b(x/y) = log_b x - log_b y using exponents.", "Let m = log_b x and n = log_b y; then x/y = b^m/b^n = b^(m - n)", ["x = b^m, y = b^n.", "x/y = b^(m - n), so log_b(x/y) = m - n."], tags=["reasoning", "challenge"])
B.orq(S, "cp1", "Use log 2 ≈ 0.301 and log 3 ≈ 0.477.", [("Estimate log 6.", "0.778"), ("Estimate log 18.", "1.255"), ("Estimate log 1.5.", "0.176"), ("Estimate log 5 (hint: 10/2).", "0.699")],
      ["log 2 + log 3.", "log 2 + 2log 3.", "log 3 - log 2.", "1 - log 2."])
B.orq(S, "honors", "Simplify and evaluate: log₄ 8 + log₄ 2 - 2log₄ 1/2... read as log₄ 8 + log₄ 2 - 2log₄(1/2).", [("Condense the first two terms.", "log₄ 16 = 2"), ("Simplify 2log₄(1/2).", "-1"), ("Evaluate the whole expression.", "3"), ("Check with change of base.", "1.5 + 0.5 + 1 = 3")],
      ["8·2 = 16 = 4².", "log₄(1/4) = -1.", "2 - (-1).", "log₄ 8 = 3/2, log₄ 2 = 1/2, log₄(1/2) = -1/2."])
B.qs[-1]["prompt"] = "Simplify and evaluate log₄ 8 + log₄ 2 - 2log₄(1/2)."
B.sa(S, "cp2", "Expand log₇(5x).", "log₇ 5 + log₇ x", ["Product rule."])

# ---------------- Skill 5: evaluating logarithms ----------------
S = 5
for b, x_ in [(2, 32), (3, 81), (5, F(1, 25)), (10, F(1, 1000)), (4, 2), (27, 3), (8, 4), (F(1, 2), 8), (9, F(1, 27)), (16, F(1, 2))]:
    v = F(round(math.log(float(x_)) / math.log(float(b)) * 12), 12)
    assert abs(float(b) ** float(v) - float(x_)) < 1e-9
    B.sa(S, "cp2" if v.denominator == 1 and v > 0 else "cp1", f"Evaluate {lb(b)}({fr(x_)}).", fr(v), [f"Ask: {frp(b)} to what power equals {fr(x_)}?", f"Write both as powers of a common base: the exponent is {fr(v)}."])
for x_ in (50, 0.25, 7, 1234):
    B.sa(S, "cp1", f"Use a calculator to evaluate log({x_:g}) to four decimal places.", f"{L(x_):.4f}", ["Common log = base 10."])
for b, x_ in [(3, 20), (2, 10), (7, 100), (5, 0.4)]:
    v = math.log(x_) / math.log(b)
    B.sa(S, "cp1", f"Use the change-of-base formula to evaluate {lb(b)}({x_:g}) to three decimal places.", f"{v:.3f}", [f"{lb(b)}({x_:g}) = log({x_:g})/log({b}) = ln({x_:g})/ln({b}).", f"≈ {v:.3f}."])
for x_ in (math.e ** 4, 1, 1 / math.e):
    pass
B.mc(S, "cp2", "Evaluate ln(e⁵).", "5", ["e⁵", "1/5", "5e"], ["ln and e^x are inverses."])
B.mc(S, "cp2", "Evaluate log 1.", "0", ["1", "10", "undefined"], ["10⁰ = 1."])
B.mc(S, "cp1", "Between which two integers is log₃ 50?", "3 and 4", ["2 and 3", "4 and 5", "16 and 17"], ["3³ = 27 < 50 < 81 = 3⁴."], tags=["reasoning"])
B.mc(S, "cp1", "Evaluate log₂(-8).", "Undefined (not a real number)", ["-3", "3", "1/3"], ["2^y > 0 for every real y, so the argument must be positive."], tags=["misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions equal to -2.", ["log₃(1/9)", "log(0.01)", "log₂(1/4)", "ln(e^(-2))", "log₅(-25)", "log₄ 16", "log_(1/2)(4)", "log₉(1/3)"],
         lambda s: {"log₃(1/9)": -2, "log(0.01)": -2, "log₂(1/4)": -2, "ln(e^(-2))": -2, "log₅(-25)": None, "log₄ 16": 2, "log_(1/2)(4)": -2, "log₉(1/3)": -0.5}[s] == -2,
         ["Rewrite each as a power of its base.", "log₅(-25) is undefined; log₄ 16 = 2; log₉(1/3) = -1/2."])
sel_auto(B, S, "honors", "Select ALL true inequalities.", ["log₂ 9 > 3", "log₃ 8 < 2", "log 500 < 3", "ln 10 > 2", "log₄ 60 > 3", "log₅ 0.2 > 0"],
         lambda s: {"log₂ 9 > 3": math.log2(9) > 3, "log₃ 8 < 2": math.log(8, 3) < 2, "log 500 < 3": L(500) < 3, "ln 10 > 2": ln(10) > 2, "log₄ 60 > 3": math.log(60, 4) > 3, "log₅ 0.2 > 0": math.log(0.2, 5) > 0}[s],
         ["Compare each argument with a power of the base: 2³ = 8 < 9, 3² = 9 > 8, 10³ = 1000 > 500, e² ≈ 7.39 < 10.", "4³ = 64 > 60; log₅ 0.2 = -1."], tags=["reasoning"])
B.sa(S, "honors", "Evaluate log₂(log₃ 81).", "2", ["log₃ 81 = 4.", "log₂ 4 = 2."], tags=["challenge"])
B.sa(S, "honors", "Evaluate log₂ 3 · log₃ 4 · log₄ 8.", "3", ["Change of base: (ln 3/ln 2)(ln 4/ln 3)(ln 8/ln 4) = ln 8/ln 2.", "log₂ 8 = 3."], tags=["challenge"])
assert abs(math.log2(3) * math.log(4, 3) * math.log(8, 4) - 3) < 1e-9
B.orq(S, "cp1", "Explore log₅ 125.", [("Write 125 as a power of 5.", "5³"), ("Evaluate log₅ 125.", "3"), ("Evaluate log₅ √125.", "3/2"), ("Evaluate log₅(1/125).", "-3")],
      ["125 = 5·5·5.", "Exponent 3.", "√125 = 5^(3/2).", "5^(-3)."])
B.orq(S, "honors", "pH = -log[H⁺].", [("Find the pH when [H⁺] = 10⁻⁴.", "4"), ("Find [H⁺] when pH = 7.", "10⁻⁷ mol/L"), ("How many times more acidic is pH 3 than pH 5?", "100"), ("Find the pH when [H⁺] = 3.2 × 10⁻⁵ (nearest hundredth).", f"{-L(3.2e-5):.2f}")],
      ["-log 10⁻⁴.", "[H⁺] = 10^(-pH).", "10⁻³/10⁻⁵.", "-log(3.2 × 10⁻⁵)."], tags=["modeling"])
B.sa(S, "cp2", "Evaluate log₄ 64.", "3", ["4³ = 64."])

# ---------------- Skill 6: solving exponential equations ----------------
S = 6
for eq, ans, steps, lvl in [("2^x = 64", "x = 6", ["64 = 2⁶."], "cp2"), ("3^(x + 1) = 81", "x = 3", ["81 = 3⁴ → x + 1 = 4."], "cp2"), ("4^x = 32", "x = 5/2", ["2^(2x) = 2⁵ → 2x = 5."], "cp1"),
                            ("9^(2x - 1) = 27^x", "x = 2", ["3^(4x - 2) = 3^(3x) → x = 2."], "cp1"), ("(1/2)^x = 16", "x = -4", ["2^(-x) = 2⁴."], "cp1"), ("5^(x²) = 625", "x = ±2", ["5^(x²) = 5⁴ → x² = 4."], "honors"),
                            ("8^(x + 2) = 4^(x - 1)", "x = -8", ["2^(3x + 6) = 2^(2x - 2) → x = -8."], "cp1"), ("e^(2x) = e^(x + 5)", "x = 5", ["2x = x + 5."], "cp2")]:
    B.sa(S, lvl, f"Solve {eq}.", ans, ["Rewrite both sides with a common base.", *steps, "Set the exponents equal and solve."])
assert 8 ** (-6) == 4 ** (-9) and abs(9 ** 3 - 27 ** 2) < 1e-9
for b, c, k in [(3, 20, 1), (2, 50, 1), (1.05, 2, 1), (10, 7.3, 1), (6, 100, 2), (4, 0.3, 1)]:
    v = math.log(c) / (k * math.log(b))
    lhs = f"{b:g}^{'x' if k == 1 else f'({k}x)'}"
    B.sa(S, "cp1", f"Solve {lhs} = {c:g}. Round to the nearest thousandth.", f"x ≈ {v:.3f}", ["Take the log of both sides.", f"{'' if k == 1 else str(k)}x·log({b:g}) = log({c:g}).", f"x = log({c:g})/({'' if k == 1 else str(k)}log {b:g}) ≈ {v:.3f}."])
for a, b, k, c in [(3, 2, 1, 50), (5, 1.08, 1, 20), (2, 10, 1, 7), (100, 0.9, 1, 40)]:
    v = math.log(c / a) / math.log(b)
    B.sa(S, "cp1", f"Solve {a}({b:g})^x = {c}. Round to the nearest hundredth.", f"x ≈ {v:.2f}", ["Divide by a first.", f"({b:g})^x = {c / a:g}.", f"x = log({c / a:g})/log({b:g}) ≈ {v:.2f}."])
for eq, ans, steps, chk in [("e^x = 12", f"x = ln 12 ≈ {ln(12):.3f}", ["Take ln."], None), ("2e^(3x) - 5 = 9", f"x = (ln 7)/3 ≈ {ln(7) / 3:.3f}", ["e^(3x) = 7.", "3x = ln 7."], None),
                            ("3^x = 2^(x + 1)", f"x = ln 2/(ln 3 - ln 2) ≈ {ln(2) / (ln(3) - ln(2)):.3f}", ["x ln 3 = (x + 1) ln 2.", "x(ln 3 - ln 2) = ln 2."], None),
                            ("e^(2x) - 5e^x + 6 = 0", "x = ln 2 or x = ln 3", ["Let u = e^x: u² - 5u + 6 = 0 → u = 2 or 3.", "x = ln 2, ln 3."], None),
                            ("4^x - 3·2^x - 4 = 0", "x = 2", ["Let u = 2^x: u² - 3u - 4 = 0 → u = 4 or -1.", "2^x = -1 is impossible; x = 2."], None)]:
    B.sa(S, "honors", f"Solve {eq}.", ans, steps, tags=["challenge"] if "u" in steps[0] else ())
assert abs(3 ** (ln(2) / (ln(3) - ln(2))) - 2 ** (ln(2) / (ln(3) - ln(2)) + 1)) < 1e-9 and 4 ** 2 - 3 * 4 - 4 == 0
B.mc(S, "cp1", "A student solves 3·2^x = 24 by writing 6^x = 24. What is the error?", "3·2^x ≠ 6^x; divide by 3 first: 2^x = 8, x = 3", ["No error", "Should be 2^x = 21", "Should be 3^x = 12"], ["Only the 2 is raised to x."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL equations with solution x = 3.", ["2^x = 8", "3^(x - 1) = 9", "4^x = 8^2", "10^x = 1000", "5^x = 15", "e^x = 3", "(1/2)^x = 1/8"],
         lambda s: abs(peval(s.split(" = ")[0].replace("^", "**").replace("e**x", "exp(x)"), x=3) - peval(s.split(" = ")[1].replace("^", "**"))) < 1e-9, ["Substitute x = 3 into each equation."])
sel_auto(B, S, "honors", "Select ALL equations equivalent to 5^x = 30.", ["x = log₅ 30", "x = log 30/log 5", "x = ln 30/ln 5", "x = 30/5", "x = log(30/5)", "x log 5 = log 30", "x = log 30 - log 5"],
         lambda s: s in ("x = log₅ 30", "x = log 30/log 5", "x = ln 30/ln 5", "x log 5 = log 30"), ["Take a log of both sides; change of base."])
B.orq(S, "cp1", "Solve 7^(x - 2) = 50.", [("Take the common log of both sides.", "(x - 2)log 7 = log 50"), ("Solve for x exactly.", "x = 2 + log 50/log 7"), ("Approximate x to the nearest thousandth.", f"{2 + L(50) / L(7):.3f}"), ("Check by substitution.", f"7^{L(50) / L(7):.3f} ≈ 50")],
      ["Power rule.", "Divide, add 2.", "Calculator.", "Substitute."])
B.orq(S, "honors", "Solve 2^(2x) - 6·2^x + 8 = 0.", [("Substitute u = 2^x.", "u² - 6u + 8 = 0"), ("Solve for u.", "u = 2 or u = 4"), ("Solve for x.", "x = 1 or x = 2"), ("Why must u be positive?", "2^x > 0 for all x")],
      ["(2^x)² = 2^(2x).", "(u - 2)(u - 4).", "2^x = 2, 2^x = 4.", "Exponentials are positive."], tags=["challenge"])

# ---------------- Skill 7: solving logarithmic equations ----------------
S = 7
for eq, ans, steps, lvl in [("log₂ x = 5", "x = 32", ["x = 2⁵."], "cp2"), ("log₃(x + 4) = 2", "x = 5", ["x + 4 = 9."], "cp2"), ("log(2x - 1) = 2", "x = 101/2", ["2x - 1 = 100."], "cp1"),
                            ("ln x = 3", f"x = e³ ≈ {e ** 3:.3f}", ["x = e³."], "cp1"), ("log₅(3x) = log₅(x + 8)", "x = 4", ["One-to-one: 3x = x + 8."], "cp1"), ("2log₄ x = 3", "x = 8", ["log₄ x = 3/2 → x = 4^(3/2)."], "cp1"),
                            ("log₆ x + log₆(x - 5) = 2", "x = 9", ["log₆(x(x - 5)) = 2 → x² - 5x - 36 = 0 → x = 9 or -4.", "x = -4 makes the argument negative; reject it."], "honors"),
                            ("log₂(x + 1) - log₂(x - 2) = 2", "x = 3", ["(x + 1)/(x - 2) = 4 → x + 1 = 4x - 8.", "x = 3; check: arguments positive."], "honors"),
                            ("log x + log(x + 21) = 2", "x = 4", ["x² + 21x - 100 = 0 → (x + 25)(x - 4) = 0.", "Reject x = -25."], "honors"),
                            ("ln(x - 2) + ln(x + 1) = ln 4", "x = 3", ["(x - 2)(x + 1) = 4 → x² - x - 6 = 0 → x = 3 or -2.", "Reject x = -2."], "honors")]:
    B.sa(S, lvl, f"Solve {eq}.", ans, ["Isolate the log or combine logs into one.", "Rewrite in exponential form (or use one-to-one).", *steps])
assert abs(math.log(9, 6) + math.log(4, 6) - 2) < 1e-12 and abs(L(4) + L(25) - 2) < 1e-12 and abs(ln(1) + ln(4) - ln(4)) < 1e-12
for b, c, k, h in [(3, 4, 1, 0), (2, -1, 1, 3), (10, 1, 2, -5), (5, 2, 3, 1)]:
    xv = F(b ** c if c >= 0 else F(1, b ** -c) - h, 1) if False else (F(b) ** c - h) / k
    arg = f"{'' if k == 1 else k}x{'' if h == 0 else (' + ' if h > 0 else ' - ') + str(abs(h))}"
    B.mc(S, "cp1", f"Solve {lb(b)}({arg}) = {c}.", f"x = {fr(xv)}", [f"x = {fr((F(c) * b - h) / k)}", f"x = {fr((F(b) ** c + h) / k)}", f"x = {fr((F(c) ** b - h) / k)}"],
         [f"Exponential form: {arg} = {b}^{frp(c)} = {fr(F(b) ** c)}.", f"x = {fr(xv)}."])
    assert k * xv + h == F(b) ** c
B.mc(S, "cp1", "A student solves log₃ x + log₃(x - 8) = 2 and gets x = 9 and x = -1. Which is correct?", "x = 9 only; x = -1 makes log₃ x undefined", ["Both", "x = -1 only", "Neither"], ["Logs require positive arguments.", "Check: log₃ 9 + log₃ 1 = 2 + 0 ✓."], tags=["error-analysis"])
B.mc(S, "cp1", "What is the domain restriction for log(x - 4) + log(x + 1)?", "x > 4", ["x > -1", "x > -4", "all real numbers"], ["Both arguments must be positive: x > 4 and x > -1."])
sel_auto(B, S, "cp1", "Select ALL solutions of log₂(x² - 9) = 4.", ["5", "-5", "√7", "3", "-3", "25"], lambda s: (lambda v: v * v - 9 > 0 and abs(math.log2(v * v - 9) - 4) < 1e-9)(peval(s).real),
         ["x² - 9 = 16 → x² = 25 → x = ±5.", "Both give argument 16 > 0."])
sel_auto(B, S, "honors", "Select ALL equations whose solution set is empty.", ["log₂(x) = log₂(x - 3)", "log(x) + log(x - 3) = log(-2)", "ln(x + 1) = ln(2x + 1) for x < 0 only", "log₃(x - 5) = -1", "ln x = 0"],
         lambda s: s in ("log₂(x) = log₂(x - 3)", "log(x) + log(x - 3) = log(-2)"), ["x = x - 3 is impossible; log(-2) is undefined.", "log₃(x - 5) = -1 → x = 16/3; ln x = 0 → x = 1."], tags=["reasoning"])
B.qs[-1]["options"] = [o for o in B.qs[-1]["options"] if "only" not in o["text"]]
B.sa(S, "honors", "Solve log₄(x + 3) + log₄(x - 3) = 2.", "x = 5", ["(x + 3)(x - 3) = 16 → x² = 25.", "x = -5 makes both arguments negative."])
B.orq(S, "cp1", "Solve log₃(x + 2) + log₃ x = 1.", [("Combine the logs.", "log₃(x(x + 2)) = 1"), ("Rewrite in exponential form.", "x² + 2x = 3"), ("Solve the quadratic.", "x = 1 or x = -3"), ("Check and state the answer.", "x = 1 (x = -3 is extraneous)")],
      ["Product rule.", "3¹ = 3.", "(x + 3)(x - 1) = 0.", "Arguments must be positive."], tags=["multistep"])
B.orq(S, "honors", "The Richter magnitude is M = log(A/A₀).", [("If M = 5, how many times A₀ is A?", "100,000"), ("How many times stronger is an M 7 quake than an M 5 quake?", "100"), ("Solve M = log(A/A₀) for A.", "A = A₀·10^M"),
      ("A quake is 50 times stronger than an M 4.2 quake. Find its magnitude (nearest tenth).", f"{4.2 + L(50):.1f}")],
      ["10⁵.", "10^(7 - 5).", "Exponential form.", "M = 4.2 + log 50."], tags=["modeling"])
B.sa(S, "cp2", "Solve log₇ x = 2.", "x = 49", ["7² = 49."])
B.sa(S, "cp2", "Solve log x = -1.", "x = 1/10", ["10⁻¹."])

# ---------------- Skill 8: compound interest and models ----------------
S = 8
for P_, r, n_, t in [(1000, 5, 12, 10), (2500, 3.5, 4, 6), (800, 7, 1, 15), (15000, 4.25, 365, 5), (5000, 6, 2, 8)]:
    A = P_ * (1 + r / 100 / n_) ** (n_ * t)
    nm = {1: "annually", 2: "semiannually", 4: "quarterly", 12: "monthly", 365: "daily"}[n_]
    B.sa(S, "cp1", f"${P_:,} is invested at {r:g}% interest compounded {nm} for {t} years. Find the balance.", f"${r2(A)}",
         [f"A = P(1 + r/n)^(nt) = {P_}(1 + {r / 100:g}/{n_})^({n_}·{t}).", f"A ≈ ${r2(A)}."], tags=["modeling"])
for P_, r, t in [(1000, 4, 10), (3000, 6.5, 7), (500, 2.5, 20)]:
    A = P_ * e ** (r / 100 * t)
    B.sa(S, "cp1", f"${P_:,} is invested at {r:g}% compounded continuously for {t} years. Find the balance.", f"${r2(A)}", [f"A = Pe^(rt) = {P_}e^({r / 100:g}·{t}).", f"≈ ${r2(A)}."], tags=["modeling"])
for r, n_ in [(6, 12), (8, 4), (3, 1), (5, None)]:
    t = (math.log(2) / (n_ * math.log(1 + r / 100 / n_))) if n_ else math.log(2) / (r / 100)
    B.sa(S, "honors" if n_ is None else "cp1", f"How long to double money at {r}% compounded {'continuously' if n_ is None else {1: 'annually', 4: 'quarterly', 12: 'monthly'}[n_]}? Round to the nearest tenth of a year.", f"≈ {t:.1f} years",
         ["Set A = 2P and divide by P.", (f"2 = (1 + {r / 100:g}/{n_})^({n_}t)" if n_ else f"2 = e^({r / 100:g}t)"), f"Use logs: t ≈ {t:.1f}."], tags=["modeling"])
for half, frac, ask in [(5730, 0.25, "how old"), (30, 0.1, "how long until 10% remains"), (8, 0.5, "how long until half remains")]:
    t = half * math.log(frac) / math.log(0.5)
    B.sa(S, "cp1" if half != 5730 else "honors", f"A substance has a half-life of {half:,} years. {ask.capitalize()} {'is a sample with 25% of its carbon-14' if half == 5730 else ''}?".replace(" ?", "?"), f"{t:,.0f} years" if t > 100 else f"{t:.1f} years",
         [f"Remaining fraction = (1/2)^(t/{half}).", f"(1/2)^(t/{half}) = {frac:g} → t = {half}·log({frac:g})/log(0.5).", f"t ≈ {t:,.1f}."], tags=["modeling"])
B.mc(S, "cp1", "Which gives more money after 1 year at 6%: monthly or continuous compounding?", "Continuous (slightly more)", ["Monthly", "They are equal", "Depends on the principal"], ["(1 + 0.06/12)¹² ≈ 1.06168; e^0.06 ≈ 1.06184."], tags=["reasoning"])
assert (1 + 0.06 / 12) ** 12 < e ** 0.06
B.mc(S, "cp1", "In A = 2000(1.015)^(4t), what is the annual interest rate if compounding is quarterly?", "6%", ["1.5%", "15%", "4%"], ["r/4 = 0.015 → r = 0.06."])
B.mc(S, "honors", "What is the effective annual yield of 8% compounded quarterly (nearest hundredth)?", f"{((1.02) ** 4 - 1) * 100:.2f}%", ["8.00%", "2.00%", f"{(e ** 0.08 - 1) * 100:.2f}%"], ["(1 + 0.08/4)⁴ - 1."], tags=["challenge"])
sel_auto(B, S, "cp1", "$1,000 grows to A = 1000(1.04)^t. Select ALL true statements.", ["The annual growth rate is 4%", "After 2 years the balance is $1,081.60", "The balance doubles in about 17.7 years", "The balance grows by $40 every year", "After 2 years the balance is $1,080"],
         lambda s: s in ("The annual growth rate is 4%", "After 2 years the balance is $1,081.60", "The balance doubles in about 17.7 years"), ["1000(1.04)² = 1081.60.", f"t = ln 2/ln 1.04 ≈ {ln(2) / ln(1.04):.1f}.", "Interest grows each year (exponential), not a constant $40."], tags=["modeling"])
B.orq(S, "cp1", "Newton's law of cooling: T(t) = 70 + 130e^(-0.05t) (°F, t in minutes).", [("Find the initial temperature.", "200°F"), ("Find T(10) (nearest tenth).", f"{70 + 130 * e ** -0.5:.1f}°F"),
      ("When is T = 100°F (nearest tenth of a minute)?", f"{-math.log(30 / 130) / 0.05:.1f} min"), ("What temperature does T approach?", "70°F")],
      ["e⁰ = 1.", "Substitute.", "130e^(-0.05t) = 30 → t = -ln(3/13)/0.05.", "The exponential term approaches 0."], tags=["modeling"])
B.orq(S, "honors", "A town's population was 12,000 in 2015 and 15,000 in 2020, growing exponentially.", [("Find the annual growth factor (nearest ten-thousandth).", f"{1.25 ** 0.2:.4f}"), ("Write a model P(t), t years after 2015.", "P = 12000(1.25)^(t/5)"),
      ("Predict the 2030 population (nearest whole).", f"{round(12000 * 1.25 ** 3):,}"), ("In what year will it reach 30,000?", f"{2015 + math.ceil(5 * math.log(2.5) / math.log(1.25))}")],
      ["b⁵ = 1.25.", "Grows by 25% every 5 years.", "12000·1.25³.", f"(1.25)^(t/5) = 2.5 → t ≈ {5 * math.log(2.5) / math.log(1.25):.1f}."], tags=["modeling", "multistep"])
B.sa(S, "cp2", "Which formula is used for interest compounded continuously?", "A = Pe^(rt)", ["Continuous compounding uses e."])

# ================= additions: format balance =================
B.sel(1, "honors", "Select ALL situations that are modeled by exponential functions.", ["A balance earning 3% interest compounded yearly", "A drug amount that halves every 6 hours", "A bacteria count that triples every day"],
      ["A taxi fare of $3 plus $2 per mile", "The area of a square with side s", "A car traveling at a constant 60 mph"], ["Exponential: constant percent (ratio) change per equal time step.", "The others are linear or quadratic."], tags=["modeling"])
B.orq(1, "honors", "A $30,000 car depreciates 15% per year; a $22,000 car depreciates 8% per year.", [("Write both models.", "A = 30000(0.85)^t; B = 22000(0.92)^t"), ("Find both values after 3 years (nearest dollar).", f"${round(30000 * 0.85 ** 3):,} and ${round(22000 * 0.92 ** 3):,}"),
      ("After how many whole years is the first car worth less?", str(next(t for t in range(1, 30) if 30000 * 0.85 ** t < 22000 * 0.92 ** t))), ("Solve exactly for when they are equal.", f"t = ln(22/30)/ln(0.85/0.92) ≈ {math.log(22 / 30) / math.log(0.85 / 0.92):.2f}")],
      ["b = 1 - r.", "Substitute t = 3.", "Compare year by year.", "Divide and take ln."], tags=["modeling", "challenge"])
for a, b, h, k, nm in [(1, 2, 2, 0, "y = 2^(x - 2)"), (-1, 3, 0, 2, "y = -3^x + 2"), (1, 0.5, 0, -1, "y = (0.5)^x - 1"), (4, 0.5, 0, 0, "y = 4(0.5)^x")]:
    fn = lambda v, a=a, b=b, h=h, k=k: a * b ** (v - h) + k
    cands = [f"({x0}, {fn(x0):g})" for x0 in (-1, 0, 1, 2)] + [f"(0, {fn(0) + 1:g})", f"(1, {fn(-1):g})" if fn(-1) != fn(1) else "(1, 9)"]
    sel_auto(B, 2, "cp1", f"Select ALL points on the graph of {nm}.", cands, lambda s_, fn=fn: (lambda u, w: abs(fn(u) - w) < 1e-9)(*[float(t) for t in s_.strip("()").split(", ")]), ["Substitute each x-coordinate."], tags=["graph"])
B.sel(3, "cp1", "Select ALL true statements about f(x) = log₂ x.", ["Its domain is x > 0", "Its range is all real numbers", "It is the inverse of y = 2^x", "f(8) = 3"], ["f(0) = 1", "It has a horizontal asymptote y = 0", "f(-2) = -1"],
      ["Logs need positive inputs; outputs are all reals.", "f(8) = 3 because 2³ = 8.", "log₂ 0 and log₂(-2) are undefined; the asymptote is vertical (x = 0)."])
B.orq(3, "cp1", "Let f(x) = log₃(x - 1) + 2.", [("State the domain.", "x > 1"), ("State the vertical asymptote.", "x = 1"), ("Find f(10).", "4"), ("Find f⁻¹(x).", "f⁻¹(x) = 3^(x - 2) + 1")],
      ["x - 1 > 0.", "Shift of x = 0 right 1.", "log₃ 9 + 2.", "Swap and solve."], tags=["connections"])
B.mc(4, "honors", "If log_b 2 = m and log_b 3 = n, which equals log_b 72?", "3m + 2n", ["6mn", "m³ + n²", "5m + n"], ["72 = 2³·3².", "log_b 72 = 3log_b 2 + 2log_b 3."], tags=["challenge"])
B.orq(4, "honors", "Let a = log 2 and b = log 3. Write in terms of a and b.", [("log 12", "2a + b"), ("log 0.75", "b - 2a"), ("log 15 (use 15 = 30/2)", "1 + b - a"), ("log₂ 3", "b/a")],
      ["12 = 2²·3.", "3/4.", "log 30 = 1 + log 3; subtract log 2.", "Change of base."], tags=["challenge"])
B.sel(5, "cp1", "Select ALL values that equal 1/2.", ["log₄ 2", "log₉ 3", "log 10^(1/2)", "ln √e"], ["log₂ 4", "log 5", "log₁₀₀ 50"], ["Each is the exponent that turns the base into the argument: 4^(1/2) = 2, 9^(1/2) = 3.", "log₂ 4 = 2; log 5 ≈ 0.699; log₁₀₀ 50 ≈ 0.849."])
B.mc(5, "honors", "Which is larger: log₃ 10 or log₄ 15?", f"log₃ 10 (≈ {math.log(10, 3):.3f} vs {math.log(15, 4):.3f})", [f"log₄ 15 (≈ {math.log(15, 4):.3f} vs {math.log(10, 3):.3f})", "They are equal", "Cannot be determined"], ["Change of base."], tags=["reasoning"])
B.mc(6, "cp1", "Which first step solves 4·3^x = 36 most directly?", "Divide both sides by 4", ["Take log of both sides", "Write 12^x = 36", "Subtract 4"], ["Isolate the exponential: 3^x = 9 → x = 2."], tags=["misconception"])
B.sel(6, "cp1", "Select ALL equations that can be solved by rewriting with a common base.", ["8^x = 32", "9^(x + 1) = 27", "(1/4)^x = 64"], ["5^x = 12", "3^x = 10", "2^x = 7"], ["8, 32 are powers of 2; 9, 27 of 3; 1/4, 64 of 2 (or 4).", "12, 10, 7 are not powers of those bases."])
B.mc(6, "honors", "Solve 2^(x + 1) = 3^(x - 1) to the nearest hundredth.", f"x ≈ {(L(3) + L(2)) / (L(3) - L(2)):.2f}", [f"x ≈ {(L(3) - L(2)) / (L(3) + L(2)):.2f}", "x = 1", f"x ≈ {L(3) / L(2):.2f}"],
     ["(x + 1)log 2 = (x - 1)log 3.", "x(log 3 - log 2) = log 3 + log 2."])
for b, c in [(2, 3), (6, 2), (3, -2), (10, 0.5)]:
    xv = b ** c
    sel_auto(B, 7, "cp2" if isinstance(c, int) and c > 0 else "cp1", f"Select ALL correct ways to solve {lb(b)}(x) = {c:g}.", [f"x = {b}^{c:g}", f"x = {xv:g}", f"x = {c:g}^{b}", f"x = {b}·{c:g}", f"x = {c:g}/{b}", f"{b}^{c:g} = x"],
             lambda s_: abs(peval(s_.replace("x = ", "").replace(" = x", "").replace("^", "**").replace("·", "*")) - xv) < 1e-9, ["log_b x = c ⇔ x = b^c."])
for eq, sols, cands in [("log₂ x + log₂(x - 2) = 3", [4], ["4", "-2", "2", "8"]), ("log(x + 3) = log(2x - 1)", [4], ["4", "-3", "1/2", "2"]), ("ln(x²) = ln(9)", [3, -3], ["3", "-3", "9", "0"])]:
    B.mc(7, "cp1", f"Solve {eq}.", ", ".join(f"x = {v}" for v in sols) if len(sols) == 1 else "x = 3 or x = -3",
         [f"x = {c}" for c in cands if int(F(c)) not in sols and c not in ("3", "-3")][:2] + (["x = 4 or x = -2"] if "-2" in cands else ["no solution"]),
         ["Combine or use one-to-one property; then solve.", "Reject values that make any argument ≤ 0."], tags=["error-analysis"])
B.orq(7, "honors", "Solve log₅(x + 1) + log₅(x - 3) = 1.", [("State the domain.", "x > 3"), ("Combine and rewrite in exponential form.", "(x + 1)(x - 3) = 5"), ("Solve the quadratic.", "x = 4 or x = -2"), ("State the solution.", "x = 4")],
      ["Both arguments must be positive: x > 3.", "x² - 2x - 3 = 5 → x² - 2x - 8 = 0.", "(x - 4)(x + 2) = 0.", "x = -2 is outside the domain."], tags=["multistep"])
assert (4 + 1) * (4 - 3) == 5
B.sa(7, "honors", "Solve (log x)² - 3log x + 2 = 0.", "x = 10 or x = 100", ["Let u = log x: u² - 3u + 2 = 0 → u = 1 or 2.", "x = 10 or 100."], tags=["challenge"])
B.sa(7, "cp1", "Solve 3 + log₂(x - 5) = 7.", "x = 21", ["log₂(x - 5) = 4 → x - 5 = 16."])
B.sa(7, "cp1", "Solve 2ln x = ln 36.", "x = 6", ["ln x² = ln 36 → x² = 36, x > 0."])
for P_, r, n_, T in [(2000, 5, 12, 3000), (500, 8, 4, 1000), (10000, 3, 1, 15000)]:
    t = math.log(T / P_) / (n_ * math.log(1 + r / 100 / n_))
    B.orq(8, "cp1", f"${P_:,} is invested at {r}% compounded {({1: 'annually', 4: 'quarterly', 12: 'monthly'})[n_]}.", [("Write the balance formula.", f"A = {P_}(1 + {r / 100:g}/{n_})^({n_}t)"),
          ("Find the balance after 5 years (nearest cent).", f"${r2(P_ * (1 + r / 100 / n_) ** (n_ * 5))}"), (f"When does the balance reach ${T:,}? (nearest tenth of a year)", f"{t:.1f} years"), ("Find the interest earned in the first 5 years.", f"${r2(P_ * (1 + r / 100 / n_) ** (n_ * 5) - P_)}")],
          ["A = P(1 + r/n)^(nt).", "Substitute t = 5.", "Divide by P, take logs.", "A - P."], tags=["modeling"])
B.sel(8, "cp1", "Select ALL expressions that give the balance of $1,000 at 6% after t years.", ["1000(1.06)^t (annual)", "1000(1.005)^(12t) (monthly)", "1000e^(0.06t) (continuous)"], ["1000(1.6)^t (annual)", "1000(1 + 0.06t) (annual)", "1000(1.06)^(12t) (monthly)"],
      ["Annual: r = 0.06; monthly: 0.06/12 = 0.005 for 12t periods; continuous: e^(rt).", "1000(1 + 0.06t) is simple interest."], tags=["misconception"])
B.sel(8, "honors", "A colony is modeled by N = 500e^(0.2t). Select ALL true statements.", ["The initial size is 500", f"N(5) ≈ {500 * e:.0f}", f"It doubles in about {ln(2) / 0.2:.2f} units of time", "The continuous growth rate is 20%"],
      ["It grows by exactly 20% each unit of time", "N(5) = 1000"], [f"N(5) = 500e ≈ {500 * e:.1f}.", "Doubling: e^(0.2t) = 2.", f"Per unit time the factor is e^0.2 ≈ {e ** 0.2:.4f} (about 22.1%)."], tags=["challenge"])
B.mc(8, "cp1", "A $900 laptop loses 20% of its value each year. About how much is it worth after 4 years?", f"${900 * 0.8 ** 4:.2f}", ["$180.00", f"${900 * 0.2 ** 4:.2f}", "$720.00"], ["900(0.8)⁴."], tags=["modeling"])
B.mc(8, "cp2", "In A = P(1 + r/n)^(nt), what does n represent?", "The number of times interest is compounded per year", ["The number of years", "The interest rate", "The principal"], ["n = compounding periods per year."])
B.sa(8, "honors", "Find the continuous rate that doubles an investment in 9 years (nearest hundredth of a percent).", f"{ln(2) / 9 * 100:.2f}%", ["2 = e^(9r) → r = ln 2/9."], tags=["modeling"])
B.sa(8, "cp1", "A radioactive sample of 80 g has a half-life of 12 days. How much remains after 30 days (nearest tenth)?", f"{80 * 0.5 ** (30 / 12):.1f} g", ["80(1/2)^(30/12)."], tags=["modeling"])
B.sa(8, "honors", "A 98°F drink cools by T = 40 + 58e^(-kt). After 10 minutes it is 70°F. Find k (nearest thousandth).", f"k ≈ {-ln(30 / 58) / 10:.3f}", ["30 = 58e^(-10k).", "k = -ln(30/58)/10."], tags=["modeling", "challenge"])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
