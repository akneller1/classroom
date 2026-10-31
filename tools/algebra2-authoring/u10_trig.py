from lib import Bank, graph
from mathlite import *
import math

STD = {1: ["F-TF.A.1"], 2: ["F-TF.A.2"], 3: ["F-TF.A.2", "F-TF.C.8"], 4: ["F-IF.C.7e"], 5: ["F-IF.C.7e", "F-BF.B.3"], 6: ["F-TF.C.8"], 7: ["F-TF.B.7"], 8: ["F-TF.B.6", "F-TF.B.7"], 9: ["F-TF.B.5"]}
B = Bank("trigonometric-functions", "tf", STD)
pi, sin, cos, tan = math.pi, math.sin, math.cos, math.tan
EX = {0: ("0", "1"), 30: ("1/2", "√3/2"), 45: ("√2/2", "√2/2"), 60: ("√3/2", "1/2"), 90: ("1", "0")}
TAN = {0: "0", 30: "√3/3", 45: "1", 60: "√3", 90: "undefined"}


def rad_txt(deg):
    f = F(deg, 180)
    if f == 0: return "0"
    n, d = f.numerator, f.denominator
    num_ = ("π" if n == 1 else "-π" if n == -1 else f"{n}π")
    return num_ if d == 1 else f"{num_}/{d}"


def neg(s):
    return s[1:] if s.startswith("-") else ("0" if s == "0" else "-" + s)


def exact(deg):
    """(sin, cos, tan) exact strings for multiples of 30° or 45°."""
    d = deg % 360; q = d // 90; r = d % 90
    if d % 90 == 0:
        s, c = {0: ("0", "1"), 90: ("1", "0"), 180: ("0", "-1"), 270: ("-1", "0")}[d]
    else:
        ref = {0: r, 1: 90 - r, 2: r, 3: 90 - r}[q]
        s0, c0 = EX[ref]
        s = s0 if q in (0, 1) else neg(s0); c = c0 if q in (0, 3) else neg(c0)
    t = "undefined" if c == "0" else None
    if t is None:
        tv = math.tan(math.radians(d))
        t = {0: "0", 1: "1", -1: "-1"}.get(round(tv), None) if abs(tv - round(tv)) < 1e-9 else None
        if t is None:
            for txt, val in [("√3", 3 ** .5), ("-√3", -3 ** .5), ("√3/3", 3 ** .5 / 3), ("-√3/3", -3 ** .5 / 3)]:
                if abs(tv - val) < 1e-9: t = txt
    return s, c, t


for dd in range(-720, 721, 15):
    if dd % 30 and dd % 45: continue
    s_, c_, t_ = exact(dd)
    assert abs(peval(s_) - sin(math.radians(dd))) < 1e-9 and abs(peval(c_) - cos(math.radians(dd))) < 1e-9, dd


# ---------------- Skill 1: degrees and radians ----------------
S = 1
for d in [30, 135, 210, 300, -45, 480, 150, 270]:
    B.sa(S, "cp2" if 0 < d <= 360 else "cp1", f"Convert {d}° to radians.", rad_txt(d), ["Multiply by π/180.", f"{d}·π/180 = {rad_txt(d)}."])
for r_ in [F(2, 3), F(5, 4), F(7, 6), F(-1, 2), F(11, 6), F(3, 2)]:
    d = r_ * 180
    B.sa(S, "cp2" if r_ > 0 else "cp1", f"Convert {rad_txt(int(d))} to degrees.", f"{fr(d)}°", ["Multiply by 180/π.", f"{fr(r_)}·180 = {fr(d)}°."])
for d in [405, -60, 750, -390, 1000]:
    co = d % 360
    B.mc(S, "cp1", f"Find the coterminal angle between 0° and 360° for {d}°.", f"{co}°", [f"{(co + 180) % 360}°", f"{360 - co}°", f"{abs(d) % 180}°" if abs(d) % 180 != co else f"{co + 10}°"], ["Add or subtract multiples of 360°.", f"{d} - 360k = {co}."])
for r_, ans in [(1, "≈ 57.3°"), (2.5, f"≈ {2.5 * 180 / pi:.1f}°")]:
    B.sa(S, "cp1", f"Convert {r_:g} radian{'s' if r_ != 1 else ''} to degrees (nearest tenth).", ans, ["Multiply by 180/π."])
for r, th, ans in [(6, F(1, 3), "2π"), (10, F(3, 4), "15π/2"), (4, F(5, 6), "10π/3")]:
    B.sa(S, "cp1", f"Find the arc length on a circle of radius {r} cm cut by a central angle of {rad_txt(int(th * 180))}.", f"{ans} cm", ["s = rθ (θ in radians).", f"{r}·{rad_txt(int(th * 180))} = {ans}."], tags=["connections"])
    assert abs(r * th * pi - peval(ans.replace("π", "*pi") if ans[0] != "π" else ans)) < 1e-9
B.mc(S, "cp1", "A student computes the arc length for r = 5 and θ = 60° as s = 5·60 = 300. What is correct?", "Convert to radians first: s = 5·π/3 = 5π/3", ["300", "5π", "60π"], ["s = rθ requires θ in radians."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL angles coterminal with 45°.", ["405°", "-315°", "765°", "π/4 + 2π", "135°", "-45°", "225°"],
         lambda s_: (round(peval(s_.replace("°", "")) if "π" not in s_ else peval(s_) * 180 / pi) - 45) % 360 == 0, ["Coterminal angles differ by multiples of 360° (2π)."])
sel_auto(B, S, "cp1", "Select ALL angles that terminate in Quadrant II.", ["120°", "3π/4", "-200°", "5π/6", "300°", "-120°", "7π/4"],
         lambda s_: 90 < ((peval(s_.replace("°", "")) if "π" not in s_ else peval(s_).real * 180 / pi) % 360) < 180, ["Reduce to [0°, 360°) and check 90° < θ < 180°."])
B.orq(S, "cp1", "A wheel of radius 14 in. turns through 3 revolutions.", [("Find the angle in radians.", "6π"), ("Find the distance traveled.", "84π in."), ("Approximate the distance in feet (nearest tenth).", f"{84 * pi / 12:.1f} ft"), ("Find the angle in degrees.", "1080°")],
      ["1 rev = 2π.", "s = rθ.", "÷12.", "×180/π."], tags=["modeling"])
B.orq(S, "honors", "A sector of a circle has radius 9 and area 27π/2.", [("Write the sector area formula.", "A = (1/2)r²θ"), ("Solve for θ.", "θ = π/3"), ("Find the arc length.", "3π"), ("Find θ in degrees.", "60°")],
      ["θ in radians.", "27π/2 = (81/2)θ.", "s = rθ.", "×180/π."], tags=["challenge"])
assert abs(0.5 * 81 * pi / 3 - 27 * pi / 2) < 1e-9
B.sa(S, "cp2", "How many radians are in a full circle?", "2π", ["360° = 2π."])

# ---------------- Skill 2: unit circle ----------------
S = 2
for d in [30, 135, 240, 330, 90, 180, 225, 300, 120, 315]:
    s_, c_, _ = exact(d)
    B.sa(S, "cp2" if d <= 90 else "cp1", f"Give the coordinates of the point on the unit circle at θ = {rad_txt(d)}.", f"({c_}, {s_})", ["(x, y) = (cos θ, sin θ).", f"Reference angle and quadrant signs give ({c_}, {s_})."])
for d in [150, 210, 315, 120, 240, 60]:
    s_, c_, _ = exact(d)
    wr = [f"({s_}, {c_})", f"({neg(c_)}, {s_})", f"({c_}, {neg(s_)})"]
    B.mc(S, "cp1", f"Which point is on the unit circle at {d}°?", f"({c_}, {s_})", wr, ["x = cos θ, y = sin θ.", "Check signs by quadrant."], tags=["misconception"])
for d in [210, 135, 300, 480, -30, 225]:
    ref = d % 360; ref = min(ref % 180, 180 - ref % 180) if ref % 180 else 0
    B.sa(S, "cp1", f"Find the reference angle for {d}°.", f"{ref}°", ["Reference angle: acute angle to the x-axis.", f"{ref}°."])
B.mc(S, "cp1", "In which quadrant is sin θ < 0 and cos θ > 0?", "IV", ["I", "II", "III"], ["x > 0 and y < 0 → Quadrant IV."])
B.mc(S, "cp1", "A student says the point at π/3 is (√3/2, 1/2). What is correct?", "(1/2, √3/2)", ["(√3/2, 1/2)", "(-1/2, √3/2)", "(√2/2, √2/2)"], ["cos(π/3) = 1/2 is the x-coordinate."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL angles whose unit-circle point has y-coordinate 1/2.", ["30°", "150°", "π/6 + 2π", "390°", "60°", "210°", "330°"],
         lambda s_: abs(sin(peval(s_.replace("°", "")) * pi / 180 if "°" in s_ else peval(s_).real) - 0.5) < 1e-9, ["sin θ = 1/2 at 30° and 150° (plus multiples of 360°)."])
sel_auto(B, S, "honors", "Select ALL true statements.", ["cos(-θ) = cos θ", "sin(-θ) = -sin θ", "sin(π - θ) = sin θ", "cos(π - θ) = cos θ", "sin(θ + 2π) = sin θ", "cos(θ + π) = cos θ"],
         lambda s_: s_ in ("cos(-θ) = cos θ", "sin(-θ) = -sin θ", "sin(π - θ) = sin θ", "sin(θ + 2π) = sin θ"), ["Reflections on the unit circle: across x-axis (−θ), across y-axis (π − θ).", "cos(π − θ) = −cos θ, cos(θ + π) = −cos θ."], tags=["reasoning"])
B.orq(S, "cp1", "Use the unit circle for θ = 5π/4.", [("Name the quadrant.", "III"), ("Find the reference angle.", "π/4"), ("Find the coordinates.", "(-√2/2, -√2/2)"), ("Find tan θ.", "1")], ["Between π and 3π/2.", "5π/4 - π.", "Both negative.", "y/x."])
B.orq(S, "honors", "The terminal side of θ passes through (-5, 12).", [("Find r.", "13"), ("Find the point on the unit circle.", "(-5/13, 12/13)"), ("Find sin θ and cos θ.", "12/13 and -5/13"), ("Name the quadrant.", "II")], ["√(25 + 144).", "Divide by r.", "y/r, x/r.", "x < 0, y > 0."])
B.sa(S, "cp2", "What are the coordinates on the unit circle at θ = 0?", "(1, 0)", ["cos 0 = 1, sin 0 = 0."])

# ---------------- Skill 3: sine, cosine, tangent ----------------
S = 3
for d in [60, 135, 210, 300, 180, 270, 225, 330]:
    s_, c_, t_ = exact(d)
    B.mc(S, "cp1" if d > 90 else "cp2", f"Evaluate sin({rad_txt(d)}), cos({rad_txt(d)}), and tan({rad_txt(d)}).", f"sin = {s_}, cos = {c_}, tan = {t_}",
         [f"sin = {c_}, cos = {s_}, tan = {t_ if t_ in ('undefined', '0') else '1/(' + t_ + ')'}", f"sin = {neg(s_)}, cos = {c_}, tan = {neg(t_) if t_ != 'undefined' else '0'}", f"sin = {s_}, cos = {neg(c_)}, tan = {neg(t_) if t_ != 'undefined' else '1'}"],
         ["Use the reference angle and the quadrant signs.", f"tan = sin/cos = {t_}."])
for (opp, adj, hyp) in [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]:
    B.sa(S, "cp2", f"In a right triangle, the side opposite θ is {opp} and the hypotenuse is {hyp}. Find cos θ and tan θ.", f"cos θ = {adj}/{hyp}, tan θ = {opp}/{adj}", [f"Adjacent = √({hyp}² - {opp}²) = {adj}.", "cos = adj/hyp, tan = opp/adj."])
for sv, quad, cv, tv in [("3/5", "II", "-4/5", "-3/4"), ("-5/13", "III", "-12/13", "5/12"), ("-8/17", "IV", "15/17", "-8/15"), ("12/13", "I", "5/13", "12/5")]:
    B.sa(S, "cp1" if quad != "I" else "cp2", f"sin θ = {sv} and θ is in Quadrant {quad}. Find cos θ and tan θ.", f"cos θ = {cv}, tan θ = {tv}", ["cos²θ = 1 - sin²θ.", f"Quadrant {quad} fixes the sign of cos θ.", "tan θ = sin θ/cos θ."])
    assert abs(peval(sv) ** 2 + peval(cv) ** 2 - 1) < 1e-12 and abs(peval(sv) / peval(cv) - peval(tv)) < 1e-12
for tv, quad, sv, cv in [("-2", "II", "2√5/5", "-√5/5"), ("3/4", "III", "-3/5", "-4/5")]:
    B.sa(S, "honors", f"tan θ = {tv} and θ is in Quadrant {quad}. Find sin θ and cos θ.", f"sin θ = {sv}, cos θ = {cv}", ["Use a reference triangle with legs from tan θ.", "Apply the quadrant signs."])
    assert abs(peval(sv) ** 2 + peval(cv) ** 2 - 1) < 1e-12 and abs(peval(sv) / peval(cv) - peval(tv)) < 1e-12
for d in [20, 155, 290]:
    B.sa(S, "cp1", f"Use a calculator: sin({d}°), cos({d}°) to four decimal places.", f"{sin(math.radians(d)):.4f}, {cos(math.radians(d)):.4f}", ["Calculator in degree mode."])
B.mc(S, "cp1", "In which quadrants is tan θ positive?", "I and III", ["I and II", "II and IV", "I only"], ["tan = y/x is positive when x and y have the same sign."])
B.mc(S, "cp1", "Which expression is undefined?", "tan(π/2)", ["sin(π/2)", "cos(π)", "tan(π)"], ["tan = sin/cos and cos(π/2) = 0."])
B.mc(S, "honors", "Find sec(2π/3) and csc(2π/3).", "sec = -2, csc = 2√3/3", ["sec = 2, csc = 2√3/3", "sec = -1/2, csc = √3/2", "sec = -2, csc = √3/2"], ["sec = 1/cos = 1/(-1/2); csc = 1/sin = 2/√3."])
sel_auto(B, S, "cp1", "Select ALL expressions equal to -1/2.", ["sin(210°)", "cos(120°)", "sin(-30°)", "cos(240°)", "sin(150°)", "cos(60°)", "sin(330°)"], lambda s_: abs(peval(s_.replace("°", "*pi/180")) + 0.5) < 1e-9, ["Use reference angle 30° or 60° and quadrant signs."])
sel_auto(B, S, "honors", "θ is in Quadrant III. Select ALL statements that must be true.", ["sin θ < 0", "cos θ < 0", "tan θ > 0", "sec θ < 0", "csc θ > 0", "cot θ < 0"], lambda s_: s_ in ("sin θ < 0", "cos θ < 0", "tan θ > 0", "sec θ < 0"),
         ["x < 0 and y < 0 in Quadrant III.", "Reciprocals keep the sign."])
B.orq(S, "cp1", "A 20-ft ladder leans against a wall making a 70° angle with the ground.", [("Which ratio relates the height to the ladder?", "sin 70°"), ("Find the height (nearest tenth).", f"{20 * sin(math.radians(70)):.1f} ft"), ("Find the distance from the wall (nearest tenth).", f"{20 * cos(math.radians(70)):.1f} ft"), ("Check with the Pythagorean theorem.", "h² + d² = 400")],
      ["Opposite/hypotenuse.", "20 sin 70°.", "20 cos 70°.", "sin² + cos² = 1."], tags=["modeling"])
B.sa(S, "cp2", "Evaluate sin(π/2).", "1", ["Point (0, 1)."])

# ---------------- Skill 4: graphs of sine and cosine ----------------
S = 4
for nm, fn, wr, al in [("y = sin x", sin, ["y = cos x", "y = -sin x", "y = sin 2x"], "the sine curve through the origin, maximum 1 at π/2, minimum -1 at 3π/2"),
                       ("y = cos x", cos, ["y = sin x", "y = -cos x", "y = cos 2x"], "the cosine curve with maximum 1 at x = 0, zeros at ±π/2"),
                       ("y = -sin x", lambda v: -sin(v), ["y = sin x", "y = -cos x", "y = sin(-2x)"], "a reflected sine curve: minimum -1 at π/2, maximum 1 at 3π/2"),
                       ("y = -cos x", lambda v: -cos(v), ["y = cos x", "y = -sin x", "y = sin x - 1"], "a reflected cosine curve: minimum -1 at x = 0")]:
    dg = graph(B, f"s04-{nm.replace('y = ', '').replace(' ', '').replace('-', 'neg')}", [(fn, {})], xr=(-2 * pi, 2 * pi), yr=(-2, 2), step=pi / 2, alt=f"Graph of {al}, for -2π ≤ x ≤ 2π (tick marks every π/2).")
    B.mc(S, "cp2", "Which equation matches the graph? (x-axis ticks are every π/2.)", nm, wr, ["Check the y-intercept: sin starts at 0, cos at 1 (or -1 when reflected).", "Check where the first maximum occurs."], diagram=dg, tags=["graph"])
sel_auto(B, S, "cp1", "Select ALL true statements about y = sin x.", ["Its period is 2π", "Its range is -1 ≤ y ≤ 1", "It has zeros at multiples of π", "It is an odd function", "Its maximum is at x = 0", "Its period is π"],
         lambda s_: s_ in ("Its period is 2π", "Its range is -1 ≤ y ≤ 1", "It has zeros at multiples of π", "It is an odd function"), ["sin(x + 2π) = sin x; sin(-x) = -sin x; max at π/2."])
sel_auto(B, S, "cp1", "Select ALL true statements about y = cos x.", ["Its y-intercept is 1", "It is an even function", "Its zeros are at π/2 + kπ", "Its period is 2π", "Its minimum is at x = 0", "It is an odd function"],
         lambda s_: s_ in ("Its y-intercept is 1", "It is an even function", "Its zeros are at π/2 + kπ", "Its period is 2π"), ["cos 0 = 1; cos(-x) = cos x."])
for x0, f, ans in [("π/2", "sin", "1"), ("π", "cos", "-1"), ("3π/2", "sin", "-1"), ("2π", "cos", "1"), ("π/2", "cos", "0")]:
    B.sa(S, "cp2", f"Read from the graph of y = {f} x: what is y at x = {x0}?", ans, ["Use the key points 0, π/2, π, 3π/2, 2π."])
B.mc(S, "cp1", "On [0, 2π], where is y = sin x increasing?", "0 < x < π/2 and 3π/2 < x < 2π", ["0 < x < π", "π/2 < x < 3π/2", "π < x < 2π"], ["sin rises to its max at π/2, falls to its min at 3π/2, then rises."])
B.mc(S, "honors", "How is the graph of y = cos x related to y = sin x?", "cos x = sin(x + π/2): a shift left π/2", ["A reflection over the x-axis", "A shift right π", "A vertical shift of 1"], ["cos x = sin(x + π/2)."], tags=["connections"])
assert all(abs(cos(v) - sin(v + pi / 2)) < 1e-12 for v in (0.3, 1.7, 4.1))
B.orq(S, "cp1", "Use the graph of y = cos x on [0, 2π].", [("List the x-intercepts.", "π/2 and 3π/2"), ("Where is the maximum?", "x = 0 and x = 2π"), ("Where is the minimum?", "x = π"), ("On what interval is cos x < 0?", "π/2 < x < 3π/2")], ["Zeros of cos.", "y = 1.", "y = -1.", "Between the zeros."], tags=["graph"])
B.orq(S, "honors", "Compare y = sin x and y = cos x on [0, 2π].", [("Where do they intersect?", "π/4 and 5π/4"), ("Value at the first intersection.", "√2/2"), ("Where is sin x > cos x?", "π/4 < x < 5π/4"), ("Explain using a shift.", "cos is sin shifted left π/2")],
      ["tan x = 1.", "sin(π/4).", "Between intersections.", "Phase relationship."], tags=["connections", "challenge"])
B.sa(S, "cp1", "What is the y-intercept of y = 3 sin x?", "0", ["sin 0 = 0."])
B.sa(S, "cp2", "What is the maximum value of y = cos x?", "1", ["Range -1 to 1."])

# ---------------- Skill 5: amplitude, period, phase shift ----------------
S = 5
for a, b, c, d in [(3, 2, 0, 0), (-2, 1, 0, 1), (1, 4, 0, -3), (5, F(1, 2), 0, 0), (2, 3, F(1, 2), 0), (4, 2, F(1, 4), 1), (F(1, 2), 1, F(1, 3), -2), (3, F(1, 3), -1, 2)]:
    per = 2 / F(b)
    perT = rad_txt(int(per * 180))
    shift = F(c)  # c in units of π: y = a sin(b(x - cπ)) + d
    fx = f"{'' if a == 1 else '-' if a == -1 else fr(a)}sin({'' if b == 1 else fr(b)}{'x' if shift == 0 else ('(x - ' + rad_txt(int(shift * 180)) + ')' if shift > 0 else '(x + ' + rad_txt(int(-shift * 180)) + ')')}){'' if d == 0 else (' + ' if d > 0 else ' - ') + str(abs(d))}"
    ans = f"amplitude {fr(abs(F(a)))}; period {perT}; phase shift {('none' if shift == 0 else rad_txt(int(abs(shift) * 180)) + (' right' if shift > 0 else ' left'))}; midline y = {d}"
    B.sa(S, "cp1" if shift or d else "cp2", f"For y = {fx}, find the amplitude, period, phase shift, and midline.", ans, ["Compare with y = a sin(b(x - h)) + k.", f"Amplitude |a|, period 2π/|b| = {perT}.", "Phase shift h, midline y = k."])
for b, per in [(2, "π"), (4, "π/2"), (F(1, 2), "4π"), (3, "2π/3"), (pi, "2")]:
    bt = "π" if b == pi else fr(b) if not isinstance(b, F) or b.denominator == 1 else f"({fr(b)})"
    wr = {"π": ["4π", "2π", "π/2"], "π/2": ["8π", "4", "π/4"], "4π": ["π", "π/4", "2π"], "2π/3": ["6π", "3π/2", "π/3"], "2": ["2π²", "π", "1/2"]}[per]
    B.mc(S, "cp1", f"What is the period of y = cos({bt}x)?", per, wr, ["Period = 2π/|b|."], tags=["misconception"])
for (a, per, d, kind), eq in [((4, "π", 0, "sin"), "y = 4 sin(2x)"), ((2, "4π", 1, "cos"), "y = 2 cos(x/2) + 1"), ((3, "2π/3", -2, "sin"), "y = 3 sin(3x) - 2"), ((1, "π/2", 3, "cos"), "y = cos(4x) + 3")]:
    B.sa(S, "cp1", f"Write a {kind}e function with amplitude {a}, period {per}, and midline y = {d} (no phase shift).".replace("sine", "sine").replace("cose", "cosine").replace("sine function", "sine function"), eq, ["b = 2π/period.", "y = a·f(bx) + k."])
for i, (a, b, k, kind) in enumerate([(2, 2, 0, "sin"), (3, 1, 1, "cos"), (1, F(1, 2), -1, "sin")]):
    fn = (lambda v, a=a, b=b, k=k: a * sin(float(b) * v) + k) if kind == "sin" else (lambda v, a=a, b=b, k=k: a * cos(float(b) * v) + k)
    bt = "" if b == 1 else ("x/2" if b == F(1, 2) else f"{b}x")
    eq = f"y = {a if a != 1 else ''}{'sin' if kind == 'sin' else 'cos'}({bt or 'x'}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}".replace("(x/2)", "(x/2)")
    eq = eq.replace("(" + bt + ")", "(" + bt + ")") if bt else eq
    dg = graph(B, f"s05-wave-{i}", [(fn, {})], xr=(-2 * pi, 4 * pi) if b == F(1, 2) else (-pi, 2 * pi), yr=(-5, 5), step=pi / 2, hlines=[k] if k else [], alt=f"Graph of a {('sine' if kind == 'sin' else 'cosine')} wave with midline y = {k}, maximum {a + k}, minimum {k - a}, and period {fr(2 / F(b))}π (ticks every π/2).")
    per_txt = {2: "π", 1: "2π", F(1, 2): "4π"}[b]
    B.orq(S, "cp1", "Use the graph of the periodic function.", [("Find the midline.", f"y = {k}"), ("Find the amplitude.", str(a)), ("Find the period.", per_txt), ("Write an equation.", eq)],
          ["Halfway between max and min.", "Max minus midline.", "Length of one cycle.", f"{'Starts at the midline going up → sine' if kind == 'sin' else 'Starts at a maximum → cosine'}."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "A student says y = sin(2x - π) has phase shift π right. What is correct?", "π/2 right, since 2x - π = 2(x - π/2)", ["π right", "π/2 left", "2π right"], ["Factor b out first."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "y = -3cos(2x) + 1. Select ALL true statements.", ["The amplitude is 3", "The period is π", "The maximum value is 4", "The minimum value is -2", "The amplitude is -3", "The period is 4π"],
         lambda s_: s_ in ("The amplitude is 3", "The period is π", "The maximum value is 4", "The minimum value is -2"), ["Amplitude |a| = 3; max 1 + 3, min 1 - 3.", "Period 2π/2."])
B.sa(S, "honors", "Write a sine function with maximum 7, minimum -1, and period 6.", "y = 4 sin((π/3)x) + 3", ["Midline (7 + (-1))/2 = 3; amplitude 4.", "b = 2π/6 = π/3."], tags=["challenge"])
B.orq(S, "honors", "f(x) = 2sin(3x + π) - 1.", [("Rewrite in the form a sin(b(x - h)) + k.", "2sin(3(x + π/3)) - 1"), ("Find the period.", "2π/3"), ("Find the phase shift.", "π/3 left"), ("Find the range.", "-3 ≤ y ≤ 1")], ["Factor 3.", "2π/3.", "h = -π/3.", "-1 ± 2."], tags=["challenge"])
B.sa(S, "cp2", "Find the amplitude of y = 6 cos x.", "6", ["|a| = 6."])

# ---------------- Skill 6: identities ----------------
S = 6
for expr, ans in [("sin²θ + cos²θ", "1"), ("1 - cos²θ", "sin²θ"), ("sec²θ - 1", "tan²θ"), ("sin θ · csc θ", "1"), ("tan θ · cos θ", "sin θ"), ("(1 - sin²θ)/cos θ", "cos θ"), ("csc²θ - cot²θ", "1"), ("sin θ/tan θ", "cos θ")]:
    B.sa(S, "cp2" if expr.count(" ") < 4 else "cp1", f"Simplify {expr}.", ans, ["Use Pythagorean, reciprocal, or quotient identities.", f"Result: {ans}."])
    th = 0.73; env = {"sec": lambda v: 1 / cos(v), "csc": lambda v: 1 / sin(v), "cot": lambda v: 1 / tan(v)}
    e1 = expr.replace("sin²θ", "sin(θ)²").replace("cos²θ", "cos(θ)²").replace("sec²θ", "sec(θ)²").replace("csc²θ", "csc(θ)²").replace("cot²θ", "cot(θ)²").replace("tan²θ", "tan(θ)²")
    a1 = ans.replace("sin²θ", "sin(θ)²").replace("tan²θ", "tan(θ)²")
    f_ = lambda e: eval(re.sub(r"(sin|cos|tan|sec|csc|cot) θ", r"\1(θ)", e).replace("θ", "th").replace("²", "**2").replace("·", "*").replace("sin", "math.sin").replace("cos", "math.cos").replace("tan", "math.tan").replace("sec(", "SEC(").replace("csc(", "CSC(").replace("cot(", "COT("),
                        {"math": math, "th": th, "SEC": env["sec"], "CSC": env["csc"], "COT": env["cot"]})
    assert abs(f_(e1) - f_(a1)) < 1e-9, expr
for idt, steps in [("tan θ + cot θ = sec θ csc θ", ["Write in sin and cos: sin/cos + cos/sin = (sin² + cos²)/(sin cos).", "= 1/(sin cos) = sec θ csc θ."]),
                   ("(1 + cos θ)(1 - cos θ) = sin²θ", ["Expand: 1 - cos²θ.", "= sin²θ."]), ("cos θ/(1 - sin θ) = (1 + sin θ)/cos θ", ["Multiply by (1 + sin θ)/(1 + sin θ).", "cos(1 + sin)/(1 - sin²) = cos(1 + sin)/cos² = (1 + sin)/cos."]),
                   ("sec θ - cos θ = sin θ tan θ", ["1/cos - cos = (1 - cos²)/cos = sin²/cos.", "= sin·(sin/cos)."])]:
    B.sa(S, "honors", f"Verify the identity: {idt}.", "Verified (see steps)", steps, tags=["reasoning"])
for th in (0.4, 1.1, 2.3):
    assert abs(tan(th) + 1 / tan(th) - 1 / (cos(th) * sin(th))) < 1e-9 and abs(cos(th) / (1 - sin(th)) - (1 + sin(th)) / cos(th)) < 1e-9 and abs(1 / cos(th) - cos(th) - sin(th) * tan(th)) < 1e-9
B.mc(S, "cp1", "Which is a Pythagorean identity?", "1 + tan²θ = sec²θ", ["1 + sec²θ = tan²θ", "sin θ + cos θ = 1", "tan²θ - 1 = sec²θ"], ["Divide sin² + cos² = 1 by cos²θ."])
B.mc(S, "cp1", "A student writes sin²θ + cos²θ = (sin θ + cos θ)². What is wrong?", "(sin θ + cos θ)² = 1 + 2sin θ cos θ, not 1", ["Nothing", "It should be (sin θ - cos θ)²", "sin²θ means sin(θ²)"], ["Squaring a sum produces a middle term."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL expressions identically equal to cos²θ.", ["1 - sin²θ", "1/sec²θ", "cos θ · cos θ", "cot²θ·sin²θ", "1 + sin²θ", "cos(θ²)", "sec²θ - 1"],
         lambda s_: s_ in ("1 - sin²θ", "1/sec²θ", "cos θ · cos θ", "cot²θ·sin²θ"), ["Use Pythagorean and reciprocal/quotient identities.", "cos(θ²) is a different function; sec²θ - 1 = tan²θ."])
sel_auto(B, S, "honors", "Select ALL equations that are identities (true for every θ where defined).", ["sin(-θ) = -sin θ", "cos(2π - θ) = cos θ", "tan(θ + π) = tan θ", "sin θ + cos θ = 1", "sin 2θ = 2 sin θ", "sec θ = 1/sin θ"],
         lambda s_: s_ in ("sin(-θ) = -sin θ", "cos(2π - θ) = cos θ", "tan(θ + π) = tan θ"), ["Test θ = π/4 or θ = π/6 to reject non-identities.", "sec θ = 1/cos θ."], tags=["reasoning"])
B.orq(S, "cp1", "sin θ = 0.6 with θ in Quadrant I. Use identities.", [("Find cos θ.", "0.8"), ("Find tan θ.", "0.75"), ("Find sec θ.", "1.25"), ("Verify 1 + tan²θ = sec²θ.", "1 + 0.5625 = 1.5625")], ["√(1 - 0.36).", "0.6/0.8.", "1/0.8.", "Substitute."])
B.orq(S, "honors", "Simplify (sin θ + cos θ)² + (sin θ - cos θ)².", [("Expand the first square.", "1 + 2sin θ cos θ"), ("Expand the second square.", "1 - 2sin θ cos θ"), ("Add.", "2"), ("Check with θ = π/3.", "(√3/2 + 1/2)² + (√3/2 - 1/2)² = 2")], ["Pythagorean.", "Pythagorean.", "Middle terms cancel.", "Numeric check."], tags=["challenge"])
B.sa(S, "cp2", "Simplify cos θ · sec θ.", "1", ["Reciprocals."])

# ---------------- Skill 7: solving trig equations ----------------
S = 7
for eq, ans in [("2sin x - 1 = 0", "π/6, 5π/6"), ("2cos x + √3 = 0", "5π/6, 7π/6"), ("tan x = 1", "π/4, 5π/4"), ("sin x = -1", "3π/2"), ("√2 cos x - 1 = 0", "π/4, 7π/4"), ("tan x + √3 = 0", "2π/3, 5π/3"), ("2sin x + √3 = 0", "4π/3, 5π/3"), ("cos x = 0", "π/2, 3π/2")]:
    B.sa(S, "cp1" if "√" in eq else "cp2", f"Solve {eq} on [0, 2π).", ans, ["Isolate the trig function.", "Find the reference angle and the quadrants with the correct sign."])
    lhs, rhs = eq.split(" = ")
    for a_ in ans.split(", "):
        v = peval(a_).real
        val = peval(lhs.replace("sin x", f"sin({v})").replace("cos x", f"cos({v})").replace("tan x", f"tan({v})")).real
        assert abs(val - float(rhs)) < 1e-9, (eq, a_)
for eq, ans, steps in [("2sin²x - sin x - 1 = 0", "π/2, 7π/6, 11π/6", ["(2sin x + 1)(sin x - 1) = 0.", "sin x = 1 or sin x = -1/2."]), ("cos²x - cos x = 0", "π/2, 3π/2, 0", ["cos x(cos x - 1) = 0.", "cos x = 0 or 1."]),
                       ("2cos²x + 3cos x + 1 = 0", "2π/3, π, 4π/3", ["(2cos x + 1)(cos x + 1) = 0."]), ("sin 2x = 1 (use 0 ≤ x < 2π)", "π/4, 5π/4", ["2x = π/2 + 2πk.", "x = π/4 + πk."]),
                       ("tan²x - 3 = 0", "π/3, 2π/3, 4π/3, 5π/3", ["tan x = ±√3."]), ("2sin x cos x = cos x", "π/6, π/2, 5π/6, 3π/2", ["cos x(2sin x - 1) = 0 (do not divide by cos x)."])]:
    srt = ", ".join(sorted(ans.split(", "), key=lambda a_: peval(a_).real))
    B.sa(S, "honors", f"Solve {eq} on [0, 2π).", srt, steps + ["Solve each factor; list all solutions in [0, 2π)."], tags=["challenge"] if "2x" in eq else ())
    for a_ in ans.split(", "):
        v = peval(a_).real
        f = {"2sin²x - sin x - 1 = 0": 2 * sin(v) ** 2 - sin(v) - 1, "cos²x - cos x = 0": cos(v) ** 2 - cos(v), "2cos²x + 3cos x + 1 = 0": 2 * cos(v) ** 2 + 3 * cos(v) + 1,
             "sin 2x = 1 (use 0 ≤ x < 2π)": sin(2 * v) - 1, "tan²x - 3 = 0": tan(v) ** 2 - 3, "2sin x cos x = cos x": 2 * sin(v) * cos(v) - cos(v)}[eq]
        assert abs(f) < 1e-9, (eq, a_)
B.mc(S, "cp1", "How many solutions does sin x = 0.4 have on [0, 2π)?", "2", ["1", "0", "4"], ["sin x = 0.4 > 0 in Quadrants I and II."])
B.mc(S, "cp1", "A student solves 2sin x cos x = sin x by dividing by sin x. What is lost?", "Solutions where sin x = 0 (x = 0, π)", ["Nothing", "x = π/3", "Solutions where cos x = 0"], ["Factor instead: sin x(2cos x - 1) = 0."], tags=["error-analysis"])
B.sa(S, "cp1", "Find all solutions of cos x = 1/2 (general solution).", "x = π/3 + 2πk or x = 5π/3 + 2πk", ["Two solutions per period; add 2πk."])
B.sa(S, "cp1", "Solve sin x = 0.3 on [0, 2π) to the nearest hundredth.", f"x ≈ {math.asin(0.3):.2f}, {pi - math.asin(0.3):.2f}", ["x = sin⁻¹(0.3).", "Second solution π - x."])
sel_auto(B, S, "cp1", "Select ALL solutions of 2cos x = 1 on [0, 2π).", ["π/3", "5π/3", "2π/3", "4π/3", "π/6", "7π/3"], lambda s_: 0 <= peval(s_).real < 2 * pi and abs(2 * cos(peval(s_).real) - 1) < 1e-9, ["cos x = 1/2 in Quadrants I and IV.", "7π/3 is outside the interval."])
sel_auto(B, S, "honors", "Select ALL values in [0, 2π) that satisfy sin²x = 1/4.", ["π/6", "5π/6", "7π/6", "11π/6", "π/3", "2π/3"], lambda s_: abs(sin(peval(s_).real) ** 2 - 0.25) < 1e-9, ["sin x = ±1/2.", "Four angles with reference angle π/6."])
B.orq(S, "cp1", "Solve 4sin²x - 3 = 0 on [0, 2π).", [("Isolate sin²x.", "sin²x = 3/4"), ("Take square roots.", "sin x = ±√3/2"), ("Find the reference angle.", "π/3"), ("List all solutions.", "π/3, 2π/3, 4π/3, 5π/3")], ["Add 3, divide by 4.", "±.", "sin(π/3) = √3/2.", "Every quadrant."])
B.orq(S, "honors", "Solve cos 2x = -1/2 on [0, 2π).", [("Find the interval for 2x.", "0 ≤ 2x < 4π"), ("Solve for 2x.", "2π/3, 4π/3, 8π/3, 10π/3"), ("Solve for x.", "π/3, 2π/3, 4π/3, 5π/3"), ("How many solutions? Why?", "4: the period of cos 2x is π")],
      ["Double the interval.", "Two per revolution, two revolutions.", "Divide by 2.", "Twice as many cycles."], tags=["challenge"])
for v in (pi / 3, 2 * pi / 3, 4 * pi / 3, 5 * pi / 3): assert abs(cos(2 * v) + 0.5) < 1e-9

# ---------------- Skill 8: inverse trig ----------------
S = 8
for f, v, ans in [("sin⁻¹", "1/2", "π/6"), ("cos⁻¹", "-1/2", "2π/3"), ("tan⁻¹", "1", "π/4"), ("sin⁻¹", "-√2/2", "-π/4"), ("cos⁻¹", "0", "π/2"), ("tan⁻¹", "-√3", "-π/3"), ("sin⁻¹", "-1", "-π/2"), ("cos⁻¹", "√3/2", "π/6")]:
    fn = {"sin⁻¹": math.asin, "cos⁻¹": math.acos, "tan⁻¹": math.atan}[f]
    assert abs(fn(peval(v).real) - peval(ans).real) < 1e-9
    B.sa(S, "cp1" if "-" in v else "cp2", f"Evaluate {f}({v}) in radians.", ans, [f"Find the angle in the restricted range of {f} with the given value.", f"Range: {'[-π/2, π/2]' if f == 'sin⁻¹' else '[0, π]' if f == 'cos⁻¹' else '(-π/2, π/2)'}."])
for f, v in [("sin⁻¹", 0.75), ("cos⁻¹", -0.3), ("tan⁻¹", 4)]:
    fn = {"sin⁻¹": math.asin, "cos⁻¹": math.acos, "tan⁻¹": math.atan}[f]
    B.sa(S, "cp1", f"Evaluate {f}({v:g}) in degrees to the nearest tenth.", f"{math.degrees(fn(v)):.1f}°", ["Calculator in degree mode."])
B.mc(S, "cp1", "A student says sin⁻¹(1/2) = 5π/6 because sin(5π/6) = 1/2. What is correct?", "π/6; sin⁻¹ returns values in [-π/2, π/2]", ["5π/6", "π/6 and 5π/6", "2"], ["Inverse sine is a function with restricted range."], tags=["error-analysis", "misconception"])
B.mc(S, "cp1", "What does sin⁻¹ x mean?", "The angle whose sine is x", ["1/sin x", "sin(1/x)", "-sin x"], ["The -1 denotes the inverse function, not a reciprocal."], tags=["misconception"])
for expr, ans in [("sin(sin⁻¹(0.4))", "0.4"), ("cos⁻¹(cos(5π/3))", "π/3"), ("tan(sin⁻¹(3/5))", "3/4"), ("cos(tan⁻¹(2))", "√5/5"), ("sin⁻¹(sin(2π/3))", "π/3")]:
    v = {"sin(sin⁻¹(0.4))": math.sin(math.asin(0.4)), "cos⁻¹(cos(5π/3))": math.acos(cos(5 * pi / 3)), "tan(sin⁻¹(3/5))": tan(math.asin(0.6)), "cos(tan⁻¹(2))": cos(math.atan(2)), "sin⁻¹(sin(2π/3))": math.asin(sin(2 * pi / 3))}[expr]
    assert abs(v - peval(ans).real) < 1e-9
    B.sa(S, "honors" if "⁻¹(sin" in expr or "⁻¹(cos" in expr or "tan(" in expr or "cos(tan" in expr else "cp1", f"Evaluate {expr}.", ans, ["Work from the inside out; respect the restricted range.", "For compositions with a ratio, draw a reference triangle."])
sel_auto(B, S, "cp1", "Select ALL values in the range of y = cos⁻¹ x.", ["0", "π/2", "π", "3π/4", "-π/4", "3π/2", "2π"], lambda s_: 0 <= peval(s_).real <= pi + 1e-12, ["Range of cos⁻¹ is [0, π]."])
sel_auto(B, S, "honors", "Select ALL true statements about inverse trigonometric functions.", ["sin⁻¹(-x) = -sin⁻¹ x", "cos⁻¹(-x) = π - cos⁻¹ x", "tan⁻¹ x is defined for all real x", "sin⁻¹(2) is defined", "cos⁻¹ x = 1/cos x", "tan⁻¹(tan 3π/4) = 3π/4"],
         lambda s_: s_ in ("sin⁻¹(-x) = -sin⁻¹ x", "cos⁻¹(-x) = π - cos⁻¹ x", "tan⁻¹ x is defined for all real x"), ["Domains: sin⁻¹, cos⁻¹ need -1 ≤ x ≤ 1.", "tan⁻¹(tan 3π/4) = -π/4."], tags=["reasoning"])
B.orq(S, "cp1", "A ramp rises 3 ft over a horizontal run of 20 ft.", [("Which inverse function finds the angle?", "tan⁻¹"), ("Find the angle (nearest tenth of a degree).", f"{math.degrees(math.atan(3 / 20)):.1f}°"), ("Find the ramp length (nearest tenth).", f"{(9 + 400) ** .5:.1f} ft"), ("Find the angle using sin⁻¹ to check.", f"{math.degrees(math.asin(3 / (409 ** .5))):.1f}°")],
      ["opp/adj.", "tan⁻¹(0.15).", "√409.", "Same angle."], tags=["modeling"])
B.orq(S, "honors", "Let θ = cos⁻¹(-3/5).", [("In which quadrant is θ?", "II"), ("Find sin θ.", "4/5"), ("Find tan θ.", "-4/3"), ("Find sin(2θ) using 2 sin θ cos θ.", "-24/25")], ["Range [0, π], cos < 0.", "√(1 - 9/25).", "sin/cos.", "2(4/5)(-3/5)."], tags=["challenge"])
B.sa(S, "cp2", "Evaluate tan⁻¹(0).", "0", ["tan 0 = 0."])

# ---------------- Skill 9: trig modeling ----------------
S = 9
B.orq(S, "cp1", "A Ferris wheel of diameter 40 m has its center 25 m above the ground and turns once every 8 minutes. A rider starts at the bottom.", [("Find the amplitude and midline.", "20; y = 25"), ("Find b.", "π/4"), ("Write h(t).", "h(t) = -20cos((π/4)t) + 25"), ("Find h(2).", "25 m")],
      ["Half the diameter; center height.", "2π/8.", "Bottom start → -cos.", "-20cos(π/2) + 25."], tags=["modeling"])
B.orq(S, "cp1", "Daylight hours in a city vary from 9 h (min) to 15 h (max) over a 365-day year, with the maximum on day 172.", [("Find the amplitude.", "3"), ("Find the midline.", "y = 12"), ("Find b.", "2π/365"), ("Write a cosine model.", "D(t) = 3cos((2π/365)(t - 172)) + 12")],
      ["(15 - 9)/2.", "(15 + 9)/2.", "Period 365.", "Max at t = 172 → cos shifted right 172."], tags=["modeling"])
B.orq(S, "honors", "Tides: high tide 8 ft at 2:00 a.m., low tide 2 ft at 8:15 a.m.", [("Find the amplitude and midline.", "3; y = 5"), ("Find the period.", "12.5 h"), ("Write a model with t = hours after midnight.", "h(t) = 3cos((2π/12.5)(t - 2)) + 5"), ("Predict the height at 5:00 a.m. (nearest tenth).", f"{3 * cos(2 * pi / 12.5 * 3) + 5:.1f} ft")],
      ["Half the range; average.", "Twice 6.25 h.", "Max at t = 2.", "Substitute t = 5."], tags=["modeling", "challenge"])
for A_, per, k, kind, q in [(4, 12, 10, "sin", 3), (2, 24, 18, "cos", 6), (6, 10, 0, "sin", 7.5)]:
    b = 2 * pi / per; val = (A_ * (sin if kind == "sin" else cos)(b * q) + k)
    B.sa(S, "cp1", f"A quantity follows y = {A_}{kind}((π/{per // 2})t){'' if k == 0 else ' + ' + str(k)}. Find the maximum, minimum, period, and y at t = {q:g}.", f"max {A_ + k}, min {k - A_}, period {per}, y({q:g}) = {val:.2f}".replace("-0.00", "0.00"),
         ["Max/min: midline ± amplitude.", f"Period 2π/(π/{per // 2}) = {per}.", f"Substitute t = {q:g}."], tags=["modeling"])
B.mc(S, "cp1", "A spring oscillates between 4 cm and 16 cm above a table every 2 seconds. Which model fits if it starts at the top?", "y = 6cos(πt) + 10", ["y = 6sin(πt) + 10", "y = 12cos(2t) + 4", "y = 10cos(πt) + 6"], ["Amplitude 6, midline 10, period 2 → b = π.", "Starting at max → cosine."], tags=["modeling"])
B.mc(S, "cp1", "Which real-world quantity is best modeled by a periodic function?", "Average monthly temperature over several years", ["A car's value over time", "Total savings with deposits", "Population of a growing city"], ["Repeats in a regular cycle."], tags=["modeling"])
sel_auto(B, S, "cp1", "h(t) = 15sin((π/30)t) + 20 models a seat height (ft, t in s). Select ALL true statements.", ["The maximum height is 35 ft", "The period is 60 s", "The midline is h = 20", "At t = 0 the seat is at 20 ft", "The minimum height is 0 ft", "The period is 30 s"],
         lambda s_: s_ in ("The maximum height is 35 ft", "The period is 60 s", "The midline is h = 20", "At t = 0 the seat is at 20 ft"), ["Max 20 + 15, min 5.", "2π/(π/30) = 60."])
B.sa(S, "honors", "Sound: y = 0.02 sin(880πt). Find the frequency (cycles per second).", "440 Hz", ["Period 2π/(880π) = 1/440 s.", "Frequency = 1/period."], tags=["modeling", "connections"])
B.sa(S, "cp1", "A pendulum's angle is θ(t) = 12cos(πt) degrees. How long is one full swing cycle?", "2 s", ["2π/π."], tags=["modeling"])
B.sa(S, "honors", "Temperature T(t) = 10sin((π/12)(t - 8)) + 60 (t in hours after midnight). When is the temperature first 65°F?", "t = 10 (10:00 a.m.)", ["sin((π/12)(t - 8)) = 1/2.", "(π/12)(t - 8) = π/6 → t = 10."], tags=["modeling"])
assert abs(10 * sin(pi / 12 * 2) + 60 - 65) < 1e-9

# ================= additions: format balance =================
B.mc(2, "cp1", "Which angle has unit-circle point (-√3/2, -1/2)?", "7π/6", ["5π/6", "4π/3", "11π/6"], ["x < 0, y < 0 → Quadrant III; reference angle π/6."])
B.mc(3, "cp1", "If cos θ = -0.6 and sin θ > 0, find tan θ.", "-4/3", ["4/3", "-3/4", "0.8"], ["sin θ = 0.8 (Quadrant II).", "tan = 0.8/(-0.6)."])
B.sa(3, "honors", "Find the exact value of sin(π/12) using sin(π/3 - π/4).", "(√6 - √2)/4", ["sin(a - b) = sin a cos b - cos a sin b.", "(√3/2)(√2/2) - (1/2)(√2/2)."], tags=["challenge"])
assert abs(sin(pi / 12) - (6 ** .5 - 2 ** .5) / 4) < 1e-12
for a, b, k, kind in [(2, 1, 0, "sin"), (3, 1, 0, "cos"), (1, 2, 0, "sin"), (1, 1, 2, "cos"), (4, F(1, 2), 0, "sin"), (2, 1, -1, "cos")]:
    f = (lambda v, a=a, b=b, k=k: a * sin(float(b) * v) + k) if kind == "sin" else (lambda v, a=a, b=b, k=k: a * cos(float(b) * v) + k)
    bt = "x" if b == 1 else ("2x" if b == 2 else "x/2")
    eq = f"y = {a if a != 1 else ''}{kind}({bt}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}".replace("(x)", " x")
    B.mc(4, "cp2" if b == 1 and k == 0 else "cp1", f"What are the maximum and minimum values of {eq}?", f"max {a + k}, min {k - a}", [f"max {a}, min {-a}" if k else f"max {a + 1}, min {-a - 1}", f"max {a * 2 + k}, min {k - 2 * a}", f"max 1, min -1" if a != 1 or k else "max 2, min 0"], ["Midline ± amplitude."])
    cands = [x_ for x_ in ["0", "π/2", "π", "3π/2", "2π", "π/4", "4π"]]
    keyv = {x_: f(peval(x_).real) for x_ in cands}
    zeros = [x_ for x_, v in keyv.items() if abs(v - k) < 1e-9]
    if len(zeros) >= 2 and len(zeros) < len(cands):
        sel_auto(B, 4, "cp1", f"Select ALL x-values where {eq} crosses its midline y = {k}.", cands, lambda s_, f=f, k=k: abs(f(peval(s_).real) - k) < 1e-9, ["The graph meets the midline where the trig factor is 0."], tags=["graph"])
B.sa(4, "cp1", "On [0, 2π], how many times does y = sin x equal 0.5?", "2", ["Once rising (π/6) and once falling (5π/6)."], tags=["graph"])
for a, b, k, kind, h in [(5, 2, 3, "sin", 0), (F(1, 2), 1, -4, "cos", 0), (3, 4, 0, "cos", 0), (2, F(1, 3), 1, "sin", 0), (7, 3, -2, "cos", 0)]:
    bt = "x" if b == 1 else (f"{b}x" if isinstance(b, int) else "x/3")
    eq = f"y = {fr(a) if a != 1 else ''}{kind}({bt}){'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}"
    perT = rad_txt(int(2 / F(b) * 180))
    good = f"amplitude {fr(a)}, period {perT}, midline y = {k}"
    B.mc(5, "cp1", f"Identify the amplitude, period, and midline of {eq}.", good, [f"amplitude {fr(a)}, period {rad_txt(int(F(b) * 180)) if F(b) * 180 == int(F(b) * 180) else '6π'}, midline y = {k}", f"amplitude {fr(a + k) if k else fr(2 * a)}, period {perT}, midline y = 0" if k else f"amplitude {fr(2 * a)}, period {perT}, midline y = 0", f"amplitude {fr(a)}, period {perT}, midline y = {fr(a)}"],
         ["Amplitude |a|; period 2π/|b|; midline y = k."], tags=["misconception"])
for expr, good, wr in [("sin θ cot θ", "cos θ", ["sin²θ", "1", "tan θ"]), ("(sec²θ - 1)/sec²θ", "sin²θ", ["cos²θ", "tan²θ", "1"]), ("cos θ(sec θ - cos θ)", "sin²θ", ["0", "1 - cos θ", "cos²θ"]),
                       ("(1 - cos²θ)/(1 - sin²θ)", "tan²θ", ["1", "cot²θ", "sec²θ"]), ("csc θ - sin θ", "cos θ cot θ", ["0", "cos θ", "csc θ sin θ"]), ("tan²θ cos²θ + cos²θ", "1", ["sin²θ", "2cos²θ", "sec²θ"])]:
    th = 0.81
    vals = {"sin θ cot θ": sin(th) / tan(th), "(sec²θ - 1)/sec²θ": (1 / cos(th) ** 2 - 1) * cos(th) ** 2, "cos θ(sec θ - cos θ)": cos(th) * (1 / cos(th) - cos(th)), "(1 - cos²θ)/(1 - sin²θ)": (1 - cos(th) ** 2) / (1 - sin(th) ** 2), "csc θ - sin θ": 1 / sin(th) - sin(th), "tan²θ cos²θ + cos²θ": tan(th) ** 2 * cos(th) ** 2 + cos(th) ** 2}
    gv = {"cos θ": cos(th), "sin²θ": sin(th) ** 2, "tan²θ": tan(th) ** 2, "cos θ cot θ": cos(th) / tan(th), "1": 1}[good]
    assert abs(vals[expr] - gv) < 1e-9, expr
    B.mc(6, "cp1", f"Simplify {expr}.", good, wr, ["Rewrite in terms of sine and cosine.", "Apply Pythagorean identities."])
sel_auto(B, 6, "cp1", "Select ALL expressions identically equal to tan θ (where defined).", ["sin θ/cos θ", "sin θ sec θ", "1/cot θ", "sec θ/csc θ", "cos θ/sin θ", "sin θ cos θ"], lambda s_: s_ in ("sin θ/cos θ", "sin θ sec θ", "1/cot θ", "sec θ/csc θ"), ["Quotient and reciprocal identities."])
sel_auto(B, 6, "cp1", "Select ALL values of θ that show sin θ + cos θ = 1 is NOT an identity.", ["π/4", "π/6", "π/3", "0", "π/2"], lambda s_: abs(sin(peval(s_).real) + cos(peval(s_).real) - 1) > 1e-9, ["A counterexample is any θ where the equation fails.", "θ = 0 and π/2 happen to work."], tags=["reasoning"])
B.orq(6, "honors", "Verify (1 - sin θ)(sec θ + tan θ) = cos θ.", [("Rewrite sec θ + tan θ with sine and cosine.", "(1 + sin θ)/cos θ"), ("Multiply by (1 - sin θ).", "(1 - sin²θ)/cos θ"), ("Apply a Pythagorean identity.", "cos²θ/cos θ"), ("Simplify.", "cos θ")], ["1/cos + sin/cos.", "Difference of squares.", "1 - sin² = cos².", "Cancel."], tags=["reasoning"])
for th in (0.3, 1.2): assert abs((1 - sin(th)) * (1 / cos(th) + tan(th)) - cos(th)) < 1e-9
B.orq(6, "cp1", "Given cos θ = 5/13 with θ in Quadrant IV.", [("Find sin θ.", "-12/13"), ("Find tan θ.", "-12/5"), ("Find csc θ.", "-13/12"), ("Check sin²θ + cos²θ.", "144/169 + 25/169 = 1")], ["Pythagorean identity; sine negative.", "sin/cos.", "Reciprocal.", "Sum."])
B.sa(6, "cp1", "Simplify (1 + tan²θ)cos²θ.", "1", ["sec²θ · cos²θ = 1."])
B.sa(6, "honors", "Write sin θ tan θ + cos θ as a single trig function.", "sec θ", ["sin²/cos + cos = (sin² + cos²)/cos = 1/cos."])
for eq, good, wr in [("sin x = √2/2", "π/4, 3π/4", ["π/4, 7π/4", "π/4", "3π/4, 5π/4"]), ("cos x = -1", "π", ["0", "π, 2π", "3π/2"]), ("tan x = -1", "3π/4, 7π/4", ["π/4, 5π/4", "3π/4", "5π/4, 7π/4"]),
                     ("2cos x - 1 = 0", "π/3, 5π/3", ["π/3, 2π/3", "π/6, 11π/6", "2π/3, 4π/3"]), ("sin x + 1 = 0", "3π/2", ["π/2", "π", "3π/2, π/2"])]:
    B.mc(7, "cp1", f"Solve {eq} on [0, 2π).", good, wr, ["Isolate the function; use the unit circle and quadrant signs."], tags=["misconception"])
sel_auto(B, 7, "cp1", "Select ALL solutions of tan x = √3 on [0, 2π).", ["π/3", "4π/3", "2π/3", "5π/3", "π/6", "7π/6"], lambda s_: abs(tan(peval(s_).real) - 3 ** .5) < 1e-9, ["tan has period π: π/3 and π/3 + π."])
sel_auto(B, 7, "honors", "Select ALL solutions of sin x = cos x on [0, 2π).", ["π/4", "5π/4", "3π/4", "7π/4", "π/2", "0"], lambda s_: abs(sin(peval(s_).real) - cos(peval(s_).real)) < 1e-9, ["Divide by cos x (cos x ≠ 0 there): tan x = 1."])
B.orq(7, "cp1", "Solve 3tan x - √3 = 0.", [("Isolate tan x.", "tan x = √3/3"), ("Find the reference angle.", "π/6"), ("Solutions on [0, 2π).", "π/6, 7π/6"), ("General solution.", "x = π/6 + πk")], ["Divide by 3.", "tan(π/6) = √3/3.", "Quadrants I and III.", "Period π."])
B.sa(7, "cp1", "Solve 2sin x = 1 for 0° ≤ x < 360°.", "30°, 150°", ["sin x = 1/2."])
for f, v, good, wr in [("sin⁻¹", "√3/2", "π/3", ["2π/3", "π/6", "-π/3"]), ("cos⁻¹", "-√2/2", "3π/4", ["-π/4", "5π/4", "π/4"]), ("tan⁻¹", "√3/3", "π/6", ["π/3", "7π/6", "-π/6"]), ("sin⁻¹", "-1/2", "-π/6", ["7π/6", "11π/6", "π/6"]), ("cos⁻¹", "1", "0", ["2π", "π", "π/2"])]:
    fn = {"sin⁻¹": math.asin, "cos⁻¹": math.acos, "tan⁻¹": math.atan}[f]; assert abs(fn(peval(v).real) - peval(good).real) < 1e-9
    B.mc(8, "cp1", f"Evaluate {f}({v}).", good, wr, [f"The answer must lie in the range of {f}."], tags=["misconception"])
B.sel(8, "cp1", "Select ALL expressions that are undefined.", ["sin⁻¹(2)", "cos⁻¹(-1.5)"], ["tan⁻¹(100)", "sin⁻¹(-1)", "cos⁻¹(0)"], ["sin⁻¹ and cos⁻¹ need inputs in [-1, 1]; tan⁻¹ accepts all reals."])
B.sa(8, "cp1", "A 50-ft kite string makes a 30-ft-high kite. Find the angle of elevation (nearest degree).", f"{round(math.degrees(math.asin(0.6)))}°", ["sin θ = 30/50.", "θ = sin⁻¹(0.6)."], tags=["modeling"])
for (lo, hi, per, start, unit) in [(2, 18, 12, "max at t = 0", "hours"), (40, 90, 365, "min at t = 0", "days"), (10, 30, 4, "midline rising at t = 0", "seconds"), (0, 8, 10, "min at t = 0", "seconds"), (55, 85, 24, "max at t = 15", "hours"), (5, 25, 2, "midline rising at t = 0", "seconds")]:
    A_ = F(hi - lo, 2); k = F(hi + lo, 2); bt = rad_txt(int(F(2, per) * 180)) if F(2, per) * 180 == int(F(2, per) * 180) else f"2π/{per}"
    model = {"max at t = 0": f"y = {fr(A_)}cos(({bt})t) + {fr(k)}", "min at t = 0": f"y = -{fr(A_)}cos(({bt})t) + {fr(k)}", "midline rising at t = 0": f"y = {fr(A_)}sin(({bt})t) + {fr(k)}", "max at t = 15": f"y = {fr(A_)}cos(({bt})(t - 15)) + {fr(k)}"}[start]
    model = model.replace("+ 0", "").replace("((2π/2)t)", "(πt)").replace("((π)t)", "(πt)")
    B.orq(9, "cp1", f"A quantity varies periodically between {lo} and {hi} with period {per} {unit}, with a {start}.", [("Find the amplitude.", fr(A_)), ("Find the midline.", f"y = {fr(k)}"), ("Find b.", bt), ("Write a model.", model)],
          ["(max - min)/2.", "(max + min)/2.", "b = 2π/period.", "Choose sin or cos (and sign) from the starting point."], tags=["modeling"])
for scen, good, wr in [("A buoy bobs 1.5 ft above and below its rest level every 4 s, starting at rest level moving up.", "y = 1.5sin((π/2)t)", ["y = 1.5cos((π/2)t)", "y = 3sin(4t)", "y = 1.5sin(4πt)"]),
                       ("A light's brightness peaks at 900 lumens, dims to 100, and repeats every 6 s, starting at peak.", "y = 400cos((π/3)t) + 500", ["y = 900cos((π/3)t)", "y = 400sin((π/3)t) + 500", "y = 500cos(6t) + 400"]),
                       ("A piston moves between 2 cm and 14 cm, completing 5 cycles per second, starting at the lowest point.", "y = -6cos(10πt) + 8", ["y = 6cos(10πt) + 8", "y = -6cos(5t) + 8", "y = -12cos(10πt) + 2"]),
                       ("Monthly average temperature ranges from 30°F (January, t = 1) to 80°F (July, t = 7) with period 12.", "y = -25cos((π/6)(t - 1)) + 55", ["y = 25cos((π/6)(t - 1)) + 55", "y = -50cos((π/6)t) + 30", "y = -25cos(12t) + 55"])]:
    B.mc(9, "cp1", scen + " Which model fits?", good, wr, ["Amplitude = half the range; midline = average.", "b = 2π/period.", "Start at max → cos; at min → -cos; at midline rising → sin."], tags=["modeling"])
for i, (nm, f, st) in enumerate([("h(t) = 30sin((π/10)t) + 35", lambda t: 30 * sin(pi / 10 * t) + 35, {"The period is 20": True, "The maximum is 65": True, "h(5) = 65": True, "The minimum is 0": False, "The period is 10": False}),
                                 ("T(t) = -12cos((π/12)t) + 68", lambda t: -12 * cos(pi / 12 * t) + 68, {"The minimum 56 occurs at t = 0": True, "The period is 24": True, "T(12) = 80": True, "The amplitude is -12": False, "The midline is 12": False})]):
    B.sel(9, "cp1", f"{nm}. Select ALL true statements.", [k_ for k_, t_ in st.items() if t_], [k_ for k_, t_ in st.items() if not t_], ["Amplitude |a|, period 2π/b, midline k.", "Evaluate at the given times."], tags=["modeling"])
assert abs(30 * sin(pi / 2) + 35 - 65) < 1e-9 and abs(-12 * cos(pi) + 68 - 80) < 1e-9
for A_, per, k, q in [(3, 8, 5, 2), (10, 60, 50, 15), (2, 1, 0, F(1, 4)), (6, 24, 20, 18)]:
    v = A_ * sin(2 * pi / per * float(q)) + k; bt = rad_txt(int(F(2, per) * 180)) if F(2, per) * 180 == int(F(2, per) * 180) else f"2π/{per}"
    B.sa(9, "cp1", f"y = {A_}sin(({bt})t){'' if k == 0 else ' + ' + str(k)}. Find y when t = {fr(q)}.", f"{v:g}" if abs(v - round(v)) < 1e-9 else f"{v:.2f}", ["Substitute and evaluate."], tags=["modeling"])
B.sa(9, "honors", "A wheel of radius 2 ft rotates at 30 revolutions per minute. Write the height of a point on the rim above the axle, starting at the axle level rising, with t in seconds.", "y = 2sin(πt)", ["30 rpm = 0.5 rev/s → period 2 s.", "b = 2π/2 = π."], tags=["modeling"])

B.sa(1, "honors", "A car's wheel (radius 13 in.) turns at 600 rpm. Find the car's speed in miles per hour (nearest tenth).", f"{600 * 2 * pi * 13 * 60 / 63360:.1f} mph", ["Linear speed v = rω = 13·(600·2π) in/min.", "Convert: ×60 min/h ÷ 63,360 in/mi."], tags=["modeling", "challenge"])
B.sa(1, "honors", "Find the angle (in radians) swept by the minute hand of a clock in 25 minutes.", "5π/6", ["60 min = 2π.", "25/60·2π."])
B.sa(2, "honors", "Find all θ in [0, 2π) whose unit-circle point has x-coordinate equal to its y-coordinate.", "π/4, 5π/4", ["cos θ = sin θ → tan θ = 1."], tags=["reasoning"])
B.sa(5, "honors", "Write a cosine function with amplitude 2, period π/2, phase shift π/8 right, and midline y = -1.", "y = 2cos(4(x - π/8)) - 1", ["b = 2π/(π/2) = 4.", "h = π/8, k = -1."])
B.sa(5, "honors", "y = a sin(bx) + k has maximum 10 at x = π/6 and the next minimum -2 at x = π/2. Find a, b, k (a, b > 0).", "a = 6, b = 3, k = 4", ["Amplitude (10 - (-2))/2 = 6; midline 4.", "Half period π/2 - π/6 = π/3 → period 2π/3 → b = 3; check: sin(3·π/6) = 1."], tags=["challenge"])
assert abs(6 * sin(3 * pi / 6) + 4 - 10) < 1e-9 and abs(6 * sin(3 * pi / 2) + 4 + 2) < 1e-9
B.mc(9, "honors", "A Ferris wheel model is h(t) = -18cos((π/6)t) + 20. During one 12-minute ride cycle, for how many minutes is a rider above 29 m?", "4 minutes", ["6 minutes", "2 minutes", "8 minutes"], ["-18cos((π/6)t) > 9 → cos((π/6)t) < -1/2.", "(π/6)t between 2π/3 and 4π/3 → t from 4 to 8."], tags=["modeling", "challenge"])
assert abs(-18 * cos(pi / 6 * 4) + 20 - 29) < 1e-9

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
