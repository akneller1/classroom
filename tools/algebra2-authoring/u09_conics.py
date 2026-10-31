from lib import Bank, graph
from mathlite import *
import math

STD = {1: ["G-GPE.A.1"], 2: ["G-GPE.A.2"], 3: ["G-GPE.A.3"], 4: ["G-GPE.A.3"], 5: ["G-GPE.A.1", "G-GPE.A.3"], 6: ["G-GPE.A.1", "A-SSE.B.3b"], 7: ["G-GPE.A.3"]}
B = Bank("conic-sections", "cs", STD)
sqr = math.sqrt


def sq(v, h):
    h = F(h)
    return f"{v}²" if h == 0 else f"({v} {'-' if h > 0 else '+'} {fr(abs(h))})²"


def lin(v, h):
    h = F(h)
    return v if h == 0 else f"({v} {'-' if h > 0 else '+'} {fr(abs(h))})"


def circ(h, k, r2):
    return f"{sq('x', h)} + {sq('y', k)} = {fr(r2)}"


def drop1(s):
    """drop '/1' denominators: '(y - 4)²/1' → '(y - 4)²'."""
    return re.sub(r"(²)/1(?=\s)", r"\1", s)


def rtxt(r2):
    return rad(r2) if F(r2).denominator == 1 else f"√({fr(r2)})"


def gen_form(A, C, D, E, Fc):
    """Ax² + Cy² + Dx + Ey + F = 0 text."""
    out = ""
    for c, t in [(A, "x²"), (C, "y²"), (D, "x"), (E, "y"), (Fc, "")]:
        c = F(c)
        if c == 0: continue
        mag = fr(abs(c)) if (abs(c) != 1 or t == "") else ""
        out += ("-" if c < 0 else "") + mag + t if not out else (" - " if c < 0 else " + ") + mag + t
    return out + " = 0"


# ---------------- Skill 1: circles ----------------
S = 1
for h, k, r in [(0, 0, 5), (2, -3, 4), (-1, 6, 3), (4, 0, 7), (-5, -2, 1), (F(1, 2), 3, 2)]:
    B.sa(S, "cp2", f"Write the equation of the circle with center {pt(h, k)} and radius {fr(r)}.", circ(h, k, F(r) ** 2), ["(x - h)² + (y - k)² = r².", f"r² = {fr(F(r) ** 2)}."])
for h, k, r2 in [(3, -1, 16), (-4, 2, 9), (0, 5, 20), (-2, -7, 12), (6, 0, 50)]:
    B.mc(S, "cp2" if math.isqrt(r2) ** 2 == r2 else "cp1", f"Find the center and radius of {circ(h, k, r2)}.", f"center {pt(h, k)}, radius {rtxt(r2)}",
         [f"center {pt(-h, -k)}, radius {rtxt(r2)}", f"center {pt(h, k)}, radius {r2}", f"center {pt(-h, -k)}, radius {r2}"], ["Compare with (x - h)² + (y - k)² = r².", "The radius is √(r²)."], tags=["misconception"])
for (h, k), (px, py) in [((1, 2), (4, 6)), ((-3, 0), (2, 12)), ((0, -4), (6, 4)), ((2, 2), (-1, 5))]:
    r2 = (px - h) ** 2 + (py - k) ** 2
    B.sa(S, "cp1", f"Write the equation of the circle with center {pt(h, k)} that passes through {pt(px, py)}.", circ(h, k, r2), [f"r² = ({px} - {h})² + ({py} - {k})² = {r2}.".replace("- -", "+ "), circ(h, k, r2) + "."])
for (x1, y1), (x2, y2) in [((-2, 1), (6, 7)), ((0, 0), (8, -6)), ((-5, 3), (1, -5)), ((3, 4), (3, -2))]:
    h, k = F(x1 + x2, 2), F(y1 + y2, 2); r2 = (F(x2) - h) ** 2 + (F(y2) - k) ** 2
    B.sa(S, "cp1", f"Write the equation of the circle with a diameter from {pt(x1, y1)} to {pt(x2, y2)}.", circ(h, k, r2), [f"Center = midpoint {pt(h, k)}.", f"r² = {fr(r2)} (half the diameter, squared)."])
for (h, k, r2), (px, py) in [((0, 0, 25), (3, 4)), ((1, -2, 9), (3, 0)), ((-2, 3, 16), (2, 7)), ((0, 0, 10), (3, 1))]:
    d2 = (px - h) ** 2 + (py - k) ** 2; ans = "on" if d2 == r2 else ("inside" if d2 < r2 else "outside")
    B.mc(S, "cp1", f"Is {pt(px, py)} inside, on, or outside the circle {circ(h, k, r2)}?", ans.capitalize(), [a.capitalize() for a in ["inside", "on", "outside"] if a != ans] + ["Cannot be determined"],
         [f"Distance² from center = {d2}.", f"Compare with r² = {r2}: {ans}."])
B.mc(S, "cp1", "A student says the radius of (x - 1)² + (y + 2)² = 36 is 36. What is correct?", "6", ["36", "18", "√6"], ["The equation shows r², so r = √36 = 6."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "Select ALL points on the circle (x - 2)² + (y + 1)² = 25.", ["(5, 3)", "(-3, -1)", "(2, 4)", "(6, -4)", "(7, 4)", "(2, -1)", "(0, 0)"],
         lambda s_: (lambda a, b: (a - 2) ** 2 + (b + 1) ** 2 == 25)(*[int(t) for t in s_.strip("()").split(", ")]), ["Substitute; the left side must equal 25."])
sel_auto(B, S, "honors", "Select ALL equations that represent a circle with radius 3.", ["x² + y² = 9", "(x + 1)² + y² = 9", "x² + (y - 4)² = 9", "x² + y² = 3", "2x² + 2y² = 18", "(x - 3)² + (y - 3)² = 3"],
         lambda s_: s_ in ("x² + y² = 9", "(x + 1)² + y² = 9", "x² + (y - 4)² = 9", "2x² + 2y² = 18"), ["Divide by any common leading coefficient; r² must be 9."])
B.sa(S, "honors", "Write the equation of the circle centered at (3, -2) and tangent to the x-axis.", "(x - 3)² + (y + 2)² = 4", ["Tangent to the x-axis: radius = |k| = 2."], tags=["reasoning"])
B.sa(S, "honors", "Find the equation of the circle through (0, 0), (6, 0), and (0, 8).", "(x - 3)² + (y - 4)² = 25", ["A right angle at the origin means the hypotenuse (6, 0)–(0, 8) is a diameter.", "Center (3, 4), radius 5."], tags=["challenge", "connections"])
B.orq(S, "cp1", "Circle C: (x + 3)² + (y - 1)² = 49.", [("State the center and radius.", "(-3, 1); 7"), ("Find the x-intercepts.", f"x = -3 ± 4√3"), ("Is (4, 1) on the circle?", "Yes"), ("Find the area and circumference.", "49π; 14π")],
      ["Read h, k, r².", "y = 0: (x + 3)² = 48.", "49 + 0 = 49.", "πr², 2πr."], tags=["multistep"])
assert abs((-3 + 4 * sqr(3) + 3) ** 2 + 1 - 49) < 1e-9
B.orq(S, "honors", "A cell tower at (2, 5) covers a radius of 10 miles (coordinates in miles).", [("Write the boundary equation.", "(x - 2)² + (y - 5)² = 100"), ("Is a home at (9, -2) covered?", "Yes: distance² = 98 < 100"), ("Is a home at (-6, -1) covered?", "Yes: distance² = 100, on the boundary"), ("Write an inequality for the coverage region.", "(x - 2)² + (y - 5)² ≤ 100")],
      ["Circle equation.", "49 + 49.", "64 + 36.", "Inside or on."], tags=["modeling"])
B.sa(S, "cp2", "What is the equation of the circle with center at the origin and radius 8?", "x² + y² = 64", ["r² = 64."])

# ---------------- Skill 2: parabolas ----------------
S = 2
for h, k, p, ax in [(0, 0, 2, "v"), (0, 0, -3, "h"), (1, -2, 1, "v"), (-3, 4, F(1, 2), "h"), (2, 5, -2, "v"), (0, -1, F(-1, 4), "h")]:
    if ax == "v":
        eq = f"{sq('x', h)} = {fr(4 * F(p)) if 4 * F(p) != 1 else ''}{lin('y', k)}"; focus = pt(h, F(k) + p); dirx = f"y = {fr(F(k) - p)}"; opens = "up" if p > 0 else "down"
    else:
        eq = f"{sq('y', k)} = {fr(4 * F(p)) if 4 * F(p) != 1 else ''}{lin('x', h)}"; focus = pt(F(h) + p, k); dirx = f"x = {fr(F(h) - p)}"; opens = "right" if p > 0 else "left"
    eq = eq.replace("= -1(", "= -(").replace("= -1x", "= -x").replace("= -1y", "= -y")
    B.sa(S, "cp1" if (h or k) else "cp2", f"For the parabola {eq}, find the vertex, focus, and directrix, and the direction it opens.", f"vertex {pt(h, k)}; focus {focus}; directrix {dirx}; opens {opens}",
         [f"Match the form {'(x - h)² = 4p(y - k)' if ax == 'v' else '(y - k)² = 4p(x - h)'}: 4p = {fr(4 * F(p))}, p = {fr(p)}.", f"Focus is p units from the vertex inside the curve; directrix is p units on the other side."])
for (fx, fy), dline, eq in [((0, 3), "y = -3", "x² = 12y"), ((2, 0), "x = -2", "y² = 8x"), ((1, 4), "y = 2", "(x - 1)² = 4(y - 3)"), ((-2, -1), "x = 4", "(y + 1)² = -12(x - 1)"), ((0, -1), "y = 1", "x² = -4y")]:
    B.sa(S, "cp1" if fx or fy and "(" in eq else "cp2", f"Write the equation of the parabola with focus {pt(fx, fy)} and directrix {dline}.", eq,
         ["The vertex is halfway between the focus and the directrix.", "p = signed distance from vertex to focus; use (x - h)² = 4p(y - k) or (y - k)² = 4p(x - h)."])
# verify focus-directrix equations numerically
for (fx, fy), dline, eq in [((1, 4), "y = 2", (1, 3, 1, "v")), ((-2, -1), "x = 4", (1, -1, -3, "h"))]:
    h, k, p, ax = eq
    for t in (-2, 0.5, 3):
        if ax == "v":
            X = h + t; Y = k + t * t / (4 * p); d1 = sqr((X - fx) ** 2 + (Y - fy) ** 2); d2 = abs(Y - float(dline.split("= ")[1]))
        else:
            Y = k + t; X = h + t * t / (4 * p); d1 = sqr((X - fx) ** 2 + (Y - fy) ** 2); d2 = abs(X - float(dline.split("= ")[1]))
        assert abs(d1 - d2) < 1e-9
for eq, ans in [("y = (1/8)x²", "focus (0, 2); directrix y = -2"), ("y = -(1/4)x²", "focus (0, -1); directrix y = 1"), ("x = (1/12)y²", "focus (3, 0); directrix x = -3"), ("y = 2x²", "focus (0, 1/8); directrix y = -1/8")]:
    B.mc(S, "cp1", f"Find the focus and directrix of {eq}.", ans, [ans.replace("focus (0, ", "focus (").replace("focus (3, 0)", "focus (0, 3)") if "x =" in eq else ans.replace("(0, ", "(1, ").replace("y = ", "x = "), ans.replace("directrix y = -", "directrix y = ").replace("directrix y = 1", "directrix y = -1").replace("directrix x = -3", "directrix x = 3"),
         {"y = (1/8)x²": "focus (0, 8); directrix y = -8", "y = -(1/4)x²": "focus (0, -4); directrix y = 4", "x = (1/12)y²": "focus (12, 0); directrix x = -12", "y = 2x²": "focus (0, 2); directrix y = -2"}[eq]],
         ["Rewrite as x² = 4py (or y² = 4px).", "p = 1/(4a) where a is the coefficient."], tags=["misconception"])
B.mc(S, "cp1", "Which way does (y - 2)² = -6(x + 1) open?", "Left", ["Right", "Up", "Down"], ["y is squared → opens left/right; 4p = -6 < 0 → left."])
B.mc(S, "cp2", "What is the vertex of (x + 4)² = 8(y - 3)?", "(-4, 3)", ["(4, -3)", "(4, 3)", "(-4, -3)"], ["h = -4, k = 3."], tags=["misconception"])
sel_auto(B, S, "cp1", "x² = -16y. Select ALL true statements.", ["The vertex is (0, 0)", "The focus is (0, -4)", "The directrix is y = 4", "The parabola opens down", "The focus is (0, -16)", "The parabola opens left"],
         lambda s_: s_ in ("The vertex is (0, 0)", "The focus is (0, -4)", "The directrix is y = 4", "The parabola opens down"), ["4p = -16 → p = -4."])
B.sa(S, "honors", "Derive the equation of the parabola with focus (0, p) and directrix y = -p.", "x² = 4py", ["√(x² + (y - p)²) = |y + p|.", "Square: x² + y² - 2py + p² = y² + 2py + p² → x² = 4py."], tags=["reasoning", "challenge"])
B.sa(S, "honors", "A satellite dish is a parabola 4 ft across and 0.5 ft deep. Where is the receiver (focus) placed?", "2 ft above the vertex", ["Model x² = 4py through (2, 0.5): 4 = 2p → p = 2."], tags=["modeling"])
B.orq(S, "cp1", "Parabola: (x - 2)² = 12(y + 1).", [("Find the vertex.", "(2, -1)"), ("Find p.", "3"), ("Find the focus and directrix.", "(2, 2); y = -4"), ("Find the length of the latus rectum (focal width).", "12")],
      ["h = 2, k = -1.", "4p = 12.", "Up 3 / down 3.", "|4p|."])
B.orq(S, "honors", "A flashlight reflector is a parabola with focus 1.5 cm from the vertex.", [("Write the equation with vertex at the origin, opening up.", "x² = 6y"), ("How deep is the reflector if it is 8 cm wide?", "8/3 cm"), ("Where is the directrix?", "y = -1.5"), ("Why is the bulb placed at the focus?", "Light from the focus reflects parallel to the axis")],
      ["4p = 6.", "x = 4: 16 = 6y.", "y = -p.", "Reflective property."], tags=["modeling"])
B.sa(S, "cp2", "Write the equation of the parabola with vertex (0, 0) and focus (0, 5).", "x² = 20y", ["p = 5; 4p = 20."])

# ---------------- Skill 3: ellipses ----------------
S = 3
for h, k, a2, b2, horiz in [(0, 0, 25, 9, True), (0, 0, 16, 36, False), (2, -1, 49, 24, True), (-3, 4, 10, 1, True), (1, 2, 4, 13, False), (0, -5, 100, 64, True)]:
    a, b = max(a2, b2), min(a2, b2); c2 = a - b
    xd, yd = (a2, b2)
    eq = drop1(f"{sq('x', h)}/{a2} + {sq('y', k)}/{b2} = 1")
    if horiz:
        ver = f"{pt(h - sqr(a), k) if sqr(a).is_integer() else f'({fr(h)} ± {rad(a)}, {fr(k)})'}"
        vtx = f"({fr(h)} ± {rad(a)}, {fr(k)})"; foc = f"({fr(h)} ± {rad(c2)}, {fr(k)})"
    else:
        vtx = f"({fr(h)}, {fr(k)} ± {rad(a)})"; foc = f"({fr(h)}, {fr(k)} ± {rad(c2)})"
    vtx = vtx.replace("(0 ± ", "(±").replace(", 0 ± ", ", ±"); foc = foc.replace("(0 ± ", "(±").replace(", 0 ± ", ", ±")
    B.sa(S, "cp1" if (h or k) else "cp2", f"For the ellipse {eq}, find the center, vertices, and foci.", f"center {pt(h, k)}; vertices {vtx}; foci {foc}",
         [f"a² = {a} (larger denominator, {'x' if horiz else 'y'}-direction), b² = {b}.", f"c² = a² - b² = {c2}.", "Vertices ±a and foci ±c along the major axis."])
for (h, k), a, b, horiz in [((0, 0), 5, 3, True), ((0, 0), 6, 2, False), ((1, -2), 4, 3, True), ((-2, 3), 5, 4, False)]:
    eq = f"{sq('x', h)}/{(a if horiz else b) ** 2} + {sq('y', k)}/{(b if horiz else a) ** 2} = 1"
    B.sa(S, "cp1", f"Write the equation of the ellipse with center {pt(h, k)}, a {'horizontal' if horiz else 'vertical'} major axis of length {2 * a}, and minor axis of length {2 * b}.", eq,
         [f"a = {a}, b = {b}.", f"The larger denominator goes under the {'x' if horiz else 'y'}-term."])
for vtx, foc, eq in [("(±5, 0)", "(±4, 0)", "x²/25 + y²/9 = 1"), ("(0, ±13)", "(0, ±12)", "x²/25 + y²/169 = 1"), ("(±10, 0)", "(±6, 0)", "x²/100 + y²/64 = 1")]:
    B.mc(S, "cp1", f"An ellipse centered at the origin has vertices {vtx} and foci {foc}. Which is its equation?", eq,
         [eq.replace("x²/", "X").replace("y²/", "x²/").replace("X", "y²/"), eq.replace("/9 ", "/16 ").replace("/169", "/144").replace("/64", "/36"), eq.replace("/25 + y²/9", "/25 + y²/41").replace("/25 + y²/169", "/25 + y²/313").replace("/64 =", "/136 =")],
         ["b² = a² - c².", "The larger denominator goes with the major axis."], tags=["misconception"])
B.mc(S, "cp1", "A student uses c² = a² + b² for an ellipse. What is correct?", "c² = a² - b²", ["c² = a² + b²", "c = a - b", "c² = b² - a²"], ["For an ellipse the foci are inside, so c < a: c² = a² - b².", "c² = a² + b² is for hyperbolas."], tags=["error-analysis", "misconception"])
sel_auto(B, S, "cp1", "x²/36 + y²/20 = 1. Select ALL true statements.", ["The major axis is horizontal", "The vertices are (±6, 0)", "The foci are (±4, 0)", "The co-vertices are (0, ±2√5)", "The foci are (±√56, 0)", "The major axis is vertical"],
         lambda s_: s_ in ("The major axis is horizontal", "The vertices are (±6, 0)", "The foci are (±4, 0)", "The co-vertices are (0, ±2√5)"), ["a² = 36, b² = 20, c² = 16.", "√20 = 2√5."])
B.sa(S, "honors", "Find the eccentricity e = c/a of x²/169 + y²/144 = 1.", "5/13", ["c² = 169 - 144 = 25."], tags=["connections"])
B.sa(S, "honors", "The Earth's orbit: a ≈ 149.6 million km and e ≈ 0.0167. Find the distance between the Sun (a focus) and the center (nearest 0.1 million km).", f"{149.6 * 0.0167:.1f} million km", ["c = ae."], tags=["modeling"])
B.sa(S, "honors", "A whispering gallery is an ellipse 40 m long and 30 m wide. How far from the center is each focus (exact and nearest tenth)?", f"5√7 ≈ {5 * sqr(7):.1f} m", ["a = 20, b = 15, c² = 400 - 225 = 175."], tags=["modeling"])
B.orq(S, "cp1", "Ellipse: (x - 3)²/16 + (y + 2)²/25 = 1.", [("Find the center.", "(3, -2)"), ("Is the major axis horizontal or vertical?", "vertical"), ("Find the vertices.", "(3, 3) and (3, -7)"), ("Find the foci.", "(3, 1) and (3, -5)")],
      ["h = 3, k = -2.", "25 > 16 under y.", "a = 5.", "c² = 9."])
B.orq(S, "honors", "Derive the standard form for an ellipse with foci (±c, 0) and sum of distances 2a.", [("Write the distance condition.", "√((x + c)² + y²) + √((x - c)² + y²) = 2a"), ("After isolating and squaring twice, what form appears?", "(a² - c²)x² + a²y² = a²(a² - c²)"),
      ("Substitute b² = a² - c².", "b²x² + a²y² = a²b²"), ("Divide to get standard form.", "x²/a² + y²/b² = 1")], ["Definition.", "Algebra.", "Define b.", "Divide by a²b²."], tags=["reasoning", "challenge"])
B.sa(S, "cp2", "Find the vertices of x²/49 + y²/9 = 1.", "(±7, 0)", ["a² = 49 under x."])

# ---------------- Skill 4: hyperbolas ----------------
S = 4
for h, k, a2, b2, horiz in [(0, 0, 16, 9, True), (0, 0, 25, 144, False), (2, -3, 9, 16, True), (-1, 2, 4, 5, False), (0, 4, 36, 64, True), (3, 0, 1, 8, False)]:
    c2 = a2 + b2; a, b = sqr(a2), sqr(b2)
    eq = drop1(f"{sq('x', h)}/{a2} - {sq('y', k)}/{b2} = 1" if horiz else f"{sq('y', k)}/{a2} - {sq('x', h)}/{b2} = 1")
    if horiz:
        vtx = f"({fr(h)} ± {rad(a2)}, {fr(k)})"; foc = f"({fr(h)} ± {rad(c2)}, {fr(k)})"; slope = f"±{rad(b2)}/{rad(a2)}" if not (a.is_integer() and b.is_integer()) else f"±{fr(F(int(b), int(a)))}"
    else:
        vtx = f"({fr(h)}, {fr(k)} ± {rad(a2)})"; foc = f"({fr(h)}, {fr(k)} ± {rad(c2)})"; slope = f"±{rad(a2)}/{rad(b2)}" if not (a.is_integer() and b.is_integer()) else f"±{fr(F(int(a), int(b)))}"
    vtx = vtx.replace("(0 ± ", "(±").replace(", 0 ± ", ", ±"); foc = foc.replace("(0 ± ", "(±").replace(", 0 ± ", ", ±")
    asy = f"y {'-' if k > 0 else '+'} {abs(k)} = {slope}{lin('x', h)}".replace("y + 0", "y").replace("y - 0", "y")
    B.sa(S, "cp1" if (h or k) else "cp2", f"For the hyperbola {eq}, find the center, vertices, foci, and asymptotes.", f"center {pt(h, k)}; vertices {vtx}; foci {foc}; asymptotes {asy}",
         [f"a² = {a2} (positive term), b² = {b2}.", f"c² = a² + b² = {c2}.", f"Asymptote slopes {slope}."])
for (h, k), a, c, horiz in [((0, 0), 3, 5, True), ((0, 0), 12, 13, False), ((2, 1), 4, 5, True), ((-3, -2), 1, 2, False)]:
    b2 = c * c - a * a
    eq = drop1(f"{sq('x', h)}/{a * a} - {sq('y', k)}/{b2} = 1" if horiz else f"{sq('y', k)}/{a * a} - {sq('x', h)}/{b2} = 1")
    B.sa(S, "cp1", f"Write the equation of the hyperbola with center {pt(h, k)}, {'horizontal' if horiz else 'vertical'} transverse axis, a = {a}, and c = {c}.", eq, ["b² = c² - a².", f"b² = {b2}."])
for eq, asy in [("x²/9 - y²/16 = 1", "y = ±(4/3)x"), ("y²/4 - x²/25 = 1", "y = ±(2/5)x"), ("x²/36 - y²/36 = 1", "y = ±x"), ("y²/49 - x² = 1", "y = ±7x")]:
    wr = {"y = ±(4/3)x": ["y = ±(3/4)x", "y = ±(16/9)x", "y = ±4x"], "y = ±(2/5)x": ["y = ±(5/2)x", "y = ±(4/25)x", "y = ±2x"], "y = ±x": ["y = ±6x", "y = ±36x", "y = 0"], "y = ±7x": ["y = ±(1/7)x", "y = ±49x", "y = ±x"]}[asy]
    B.mc(S, "cp1", f"Find the asymptotes of {eq}.", asy, wr, ["Set the right side to 0 and solve for y.", f"{asy}."], tags=["misconception"])
B.mc(S, "cp1", "In a hyperbola, how are a, b, and c related?", "c² = a² + b²", ["c² = a² - b²", "c = a + b", "a² = b² + c²"], ["Foci are farther from the center than the vertices."])
B.mc(S, "cp1", "Which way does y²/9 - x²/4 = 1 open?", "Up and down", ["Left and right", "Up only", "It is an ellipse"], ["The positive term is y² → vertical transverse axis."], tags=["misconception"])
sel_auto(B, S, "cp1", "x²/64 - y²/36 = 1. Select ALL true statements.", ["The vertices are (±8, 0)", "The foci are (±10, 0)", "The asymptotes are y = ±(3/4)x", "It opens left and right", "The foci are (±2√7, 0)", "The asymptotes are y = ±(4/3)x"],
         lambda s_: s_ in ("The vertices are (±8, 0)", "The foci are (±10, 0)", "The asymptotes are y = ±(3/4)x", "It opens left and right"), ["a = 8, b = 6, c = 10.", "Slopes ±b/a = ±6/8."])
B.sa(S, "honors", "Write the equation of the hyperbola with vertices (0, ±3) and asymptotes y = ±(3/2)x.", "y²/9 - x²/4 = 1", ["Vertical: a = 3; slope a/b = 3/2 → b = 2."], tags=["reasoning"])
B.sa(S, "honors", "Two stations 10 mi apart (foci at (±5, 0)) find that a ship is always 6 mi closer to one station. Write the hyperbola the ship lies on.", "x²/9 - y²/16 = 1", ["Difference of distances 2a = 6 → a = 3.", "c = 5 → b² = 16."], tags=["modeling", "challenge"])
B.orq(S, "cp1", "Hyperbola: (y - 1)²/16 - (x + 2)²/9 = 1.", [("Find the center.", "(-2, 1)"), ("Find the vertices.", "(-2, 5) and (-2, -3)"), ("Find the foci.", "(-2, 6) and (-2, -4)"), ("Find the asymptotes.", "y - 1 = ±(4/3)(x + 2)")],
      ["h = -2, k = 1.", "a = 4 vertically.", "c² = 25.", "slope a/b."])
B.orq(S, "honors", "Compare x²/16 + y²/9 = 1 and x²/16 - y²/9 = 1.", [("Name each conic.", "ellipse; hyperbola"), ("Find c for each.", "√7; 5"), ("Which has asymptotes? Give them.", "the hyperbola: y = ±(3/4)x"), ("Do they share vertices?", "Yes, (±4, 0)")],
      ["Sign between terms.", "c² = 16 - 9 vs 16 + 9.", "Only hyperbolas.", "a = 4 in both."], tags=["connections"])
B.sa(S, "cp2", "Find the vertices of x²/25 - y²/4 = 1.", "(±5, 0)", ["a² = 25 under the positive x-term."])

# ---------------- Skill 5: graphing conics (diagrams) ----------------
S = 5
gl = [("circle", (lambda X, Y: (X - 1) ** 2 + (Y + 2) ** 2 - 9), "(x - 1)² + (y + 2)² = 9", ["(x + 1)² + (y - 2)² = 9", "(x - 1)² + (y + 2)² = 3", "(x - 1)²/9 + (y + 2)²/4 = 1"], [(1, -2, True, "(1, -2)")], "a circle centered at (1, -2) with radius 3"),
      ("ellipse", (lambda X, Y: X ** 2 / 16 + Y ** 2 / 4 - 1), "x²/16 + y²/4 = 1", ["x²/4 + y²/16 = 1", "x²/16 - y²/4 = 1", "x² + y² = 16"], [(4, 0), (-4, 0), (0, 2), (0, -2)], "an ellipse centered at the origin through (±4, 0) and (0, ±2)"),
      ("ellipse", (lambda X, Y: (X + 1) ** 2 / 4 + (Y - 1) ** 2 / 25 - 1), "(x + 1)²/4 + (y - 1)²/25 = 1", ["(x + 1)²/25 + (y - 1)²/4 = 1", "(x - 1)²/4 + (y + 1)²/25 = 1", "(y - 1)²/25 - (x + 1)²/4 = 1"], [(-1, 6), (-1, -4), (1, 1), (-3, 1)], "a vertical ellipse centered at (-1, 1) through (-1, 6), (-1, -4), (1, 1), (-3, 1)"),
      ("hyperbola", (lambda X, Y: X ** 2 / 4 - Y ** 2 / 9 - 1), "x²/4 - y²/9 = 1", ["y²/4 - x²/9 = 1", "x²/9 - y²/4 = 1", "x²/4 + y²/9 = 1"], [(2, 0), (-2, 0)], "a hyperbola opening left and right with vertices (±2, 0) and dashed asymptotes y = ±(3/2)x"),
      ("hyperbola", (lambda X, Y: (Y - 1) ** 2 / 4 - (X - 2) ** 2 / 4 - 1), "(y - 1)²/4 - (x - 2)²/4 = 1", ["(x - 2)²/4 - (y - 1)²/4 = 1", "(y + 1)²/4 - (x + 2)²/4 = 1", "(x - 2)² + (y - 1)² = 4"], [(2, 3), (2, -1)], "a hyperbola opening up and down with center (2, 1), vertices (2, 3) and (2, -1)"),
      ("parabola", (lambda X, Y: (X - 1) ** 2 - 4 * (Y + 2)), "(x - 1)² = 4(y + 2)", ["(y + 2)² = 4(x - 1)", "(x + 1)² = 4(y - 2)", "(x - 1)² = -4(y + 2)"], [(1, -2, True, "(1, -2)"), (1, -1, True, "F")], "an upward parabola with vertex (1, -2) and focus (1, -1)"),
      ("parabola", (lambda X, Y: (Y) ** 2 + 8 * (X - 2)), "y² = -8(x - 2)", ["y² = 8(x - 2)", "x² = -8(y - 2)", "y² = -8(x + 2)"], [(2, 0, True, "(2, 0)"), (0, 0, True, "F")], "a parabola opening left with vertex (2, 0) and focus (0, 0)")]
for i, (kind, Fn, eq, wr, pts_, desc) in enumerate(gl):
    curves = [(("implicit", Fn), {})]
    if eq == "x²/4 - y²/9 = 1": curves += [(lambda v: 1.5 * v, {"color": "#888888", "lw": 1, "ls": "--"}), (lambda v: -1.5 * v, {"color": "#888888", "lw": 1, "ls": "--"})]
    if eq.startswith("(y - 1)²/4 - (x - 2)²/4"): curves += [(lambda v: v - 1, {"color": "#888888", "lw": 1, "ls": "--"}), (lambda v: -v + 3, {"color": "#888888", "lw": 1, "ls": "--"})]
    dg = graph(B, f"s05-{kind}-{i}", curves, xr=(-7, 7), yr=(-7, 7), points=pts_, alt=f"Graph of {desc}.")
    for p_ in pts_:
        if len(p_) < 4 or p_[3] not in ("F",) and kind != "circle": assert abs(Fn(p_[0], p_[1])) < 1e-9 or kind == "circle", (eq, p_)
    B.mc(S, "cp1", "Which equation matches the graph?", eq, wr, [f"The graph is {'a ' if kind != 'ellipse' else 'an '}{kind}.", "Read the center/vertex and key points, then match the denominators or p."], diagram=dg, tags=["graph"])
    B.sa(S, "cp1" if kind in ("circle", "parabola") else "honors", f"Identify the conic in the graph and give {'its center and radius' if kind == 'circle' else 'its center' if kind in ('ellipse', 'hyperbola') else 'its vertex and focus'}.",
         {"circle": "circle; center (1, -2), radius 3", "ellipse": "ellipse; center " + ("(0, 0)" if i == 1 else "(-1, 1)"), "hyperbola": "hyperbola; center " + ("(0, 0)" if i == 3 else "(2, 1)"),
          "parabola": "parabola; vertex (1, -2), focus (1, -1)" if i == 5 else "parabola; vertex (2, 0), focus (0, 0)"}[kind], ["Read the key points from the graph."], diagram=dg, tags=["graph"])
for eq, cands, pred in [("x²/9 + y²/25 = 1", ["(3, 0)", "(0, 5)", "(-3, 0)", "(0, -5)", "(5, 0)", "(0, 3)"], lambda a, b: a * a / 9 + b * b / 25 == 1),
                        ("x² - y² = 16", ["(4, 0)", "(-4, 0)", "(5, 3)", "(5, -3)", "(0, 4)", "(3, 5)"], lambda a, b: a * a - b * b == 16),
                        ("(x - 2)² = 8(y - 1)", ["(2, 1)", "(6, 3)", "(-2, 3)", "(10, 9)", "(2, 3)", "(6, 1)"], lambda a, b: (a - 2) ** 2 == 8 * (b - 1))]:
    sel_auto(B, S, "cp1", f"Select ALL points on the graph of {eq}.", cands, lambda s_, pred=pred: pred(*[int(t) for t in s_.strip("()").split(", ")]), ["Substitute each point."])
B.orq(S, "cp1", "Sketch x²/25 + y²/9 = 1.", [("Plot the center.", "(0, 0)"), ("Plot the vertices.", "(±5, 0)"), ("Plot the co-vertices.", "(0, ±3)"), ("Find and plot the foci.", "(±4, 0)")], ["Origin.", "a = 5.", "b = 3.", "c² = 16."], tags=["graph"])
B.orq(S, "cp1", "Sketch y²/16 - x²/9 = 1.", [("Plot the vertices.", "(0, ±4)"), ("Draw the central box corners.", "(±3, ±4)"), ("Write the asymptotes.", "y = ±(4/3)x"), ("Which way do the branches open?", "up and down")], ["a = 4 vertical.", "±b, ±a.", "Diagonals of the box.", "Positive y-term."], tags=["graph"])
B.orq(S, "honors", "Sketch (x + 2)² + (y - 3)² = 16 and (x + 2)²/16 + (y - 3)²/4 = 1 on the same axes.", [("Shared center.", "(-2, 3)"), ("Circle's x-extent.", "-6 ≤ x ≤ 2"), ("Ellipse's y-extent.", "1 ≤ y ≤ 5"), ("Where do the two curves meet?", "(-6, 3) and (2, 3)")],
      ["Same h, k.", "r = 4.", "b = 2 vertically.", "Both pass through (h ± 4, k)."], tags=["graph", "connections"])
B.mc(S, "honors", "Which conic's graph is NOT the graph of a function and has two separate branches?", "Hyperbola", ["Parabola y = x²", "Circle", "Ellipse"], ["A hyperbola has two disconnected branches."], tags=["reasoning"])
B.sa(S, "cp2", "What are the x-intercepts of x²/36 + y²/4 = 1?", "(±6, 0)", ["Set y = 0."])
B.sa(S, "cp1", "Find the y-intercepts of (x - 3)² + y² = 25.", "(0, ±4)", ["x = 0: 9 + y² = 25."])

# ---------------- Skill 6: converting to standard form ----------------
S = 6
for h, k, r2 in [(2, -3, 16), (-1, 4, 9), (5, 0, 7), (-3, -2, 1), (0, 6, 36), (4, 1, 20)]:
    D, E, Fc = -2 * h, -2 * k, h * h + k * k - r2
    for t in (0.3, 2.1): X, Y = h + sqr(r2) * math.cos(t), k + sqr(r2) * math.sin(t); assert abs(X * X + Y * Y + D * X + E * Y + Fc) < 1e-9
    B.sa(S, "cp1" if h and k else "cp2", f"Write {gen_form(1, 1, D, E, Fc)} in standard form. Find the center and radius.", f"{circ(h, k, r2)}; center {pt(h, k)}, radius {rtxt(r2)}",
         ["Group x-terms and y-terms; move the constant.", f"Complete each square: add {h * h} and {k * k}.", circ(h, k, r2) + "."])
for (h, k, a2, b2), A, C in [((1, -2, 9, 4), 4, 9), ((-3, 1, 16, 25), 25, 16), ((2, 0, 4, 1), 1, 4)]:
    D, E, Fc = -2 * A * h, -2 * C * k, A * h * h + C * k * k - A * a2  # scale: A(x-h)²+C(y-k)²=A*a2 with A*a2 = C*b2
    assert A * a2 == C * b2
    for t in (0.3, 2.1): X, Y = h + sqr(a2) * math.cos(t), k + sqr(b2) * math.sin(t); assert abs(A * X * X + C * Y * Y + D * X + E * Y + Fc) < 1e-9
    B.sa(S, "honors", f"Write {gen_form(A, C, D, E, Fc)} in standard form and identify the conic.", drop1(f"{sq('x', h)}/{a2} + {sq('y', k)}/{b2} = 1; ellipse"),
         ["Group and factor out the x² and y² coefficients.", "Complete the squares (add the scaled amounts to both sides).", "Divide by the constant to get 1 on the right."])
for (h, k, a2, b2, horiz), A, C in [((0, 0, 4, 9, True), 9, -4), ((1, 2, 9, 16, False), -9, 16), ((-2, 1, 1, 4, True), 4, -1)]:
    rhs = A * a2 if horiz else C * a2
    assert rhs == (-C * b2 if horiz else -A * b2)
    D, E, Fc = -2 * A * h, -2 * C * k, A * h * h + C * k * k - rhs
    eq = drop1(f"{sq('x', h)}/{a2} - {sq('y', k)}/{b2} = 1" if horiz else f"{sq('y', k)}/{a2} - {sq('x', h)}/{b2} = 1")
    for t in (0.4, 1.3):  # parametric point on the hyperbola must satisfy the general form
        X, Y = (h + sqr(a2) * math.cosh(t), k + sqr(b2) * math.sinh(t)) if horiz else (h + sqr(b2) * math.sinh(t), k + sqr(a2) * math.cosh(t))
        assert abs(A * X * X + C * Y * Y + D * X + E * Y + Fc) < 1e-7
    B.sa(S, "honors", f"Write {gen_form(A, C, D, E, Fc)} in standard form and identify the conic.", eq + "; hyperbola", ["Group, factor, complete the squares.", "Divide so the right side is 1; the positive term determines the direction."])
for h, k, p4, vert in [(1, -2, 8, True), (-3, 1, -4, False), (2, 3, -12, True), (0, -1, 6, False)]:
    if vert:
        D, E, Fc = -2 * h, -p4, h * h + p4 * k; eq = f"{sq('x', h)} = {p4}{lin('y', k)}"; A_, C_ = 1, 0
    else:
        E, D, Fc = -2 * k, -p4, k * k + p4 * h; eq = f"{sq('y', k)} = {p4}{lin('x', h)}"; A_, C_ = 0, 1
    B.sa(S, "cp1", f"Write {gen_form(A_, C_, D, E, Fc)} in standard form and find the vertex.", f"{eq}; vertex {pt(h, k)}", ["Keep the squared variable's terms on one side; complete the square.", "Factor the coefficient of the linear term on the other side."])
B.mc(S, "cp1", "To complete the square for x² - 10x, what number do you add?", "25", ["100", "-25", "5"], ["(b/2)² = (-5)² = 25."])
B.mc(S, "cp1", "To complete the square in 4(x² + 6x) + y² = 0, how much must be added to the right side?", "36", ["9", "144", "6"], ["4(x² + 6x) + y² = 0 → 4(x² + 6x + 9) + y² = 36.", "Adding 9 inside the parentheses adds 4·9 = 36 to the left side."], tags=["error-analysis"])
B.mc(S, "honors", "A student rewrites x² + y² - 6x + 4y + 20 = 0 as (x - 3)² + (y + 2)² = -7. What does this mean?", "The equation has no real graph (r² < 0)", ["A circle of radius √7", "A circle of radius -7", "A single point"], ["r² must be ≥ 0; r² = 0 gives a point, r² < 0 gives no graph."], tags=["reasoning"])
assert 9 + 4 - 20 == -7
sel_auto(B, S, "cp1", "Select ALL steps that are part of rewriting x² + y² + 8x - 2y - 8 = 0 in standard form.", ["Group: (x² + 8x) + (y² - 2y) = 8", "Add 16 and 1 to both sides", "(x + 4)² + (y - 1)² = 25", "Divide every term by 8", "(x - 4)² + (y + 1)² = 25", "Add 64 and 4 to both sides"],
         lambda s_: s_ in ("Group: (x² + 8x) + (y² - 2y) = 8", "Add 16 and 1 to both sides", "(x + 4)² + (y - 1)² = 25"), ["(8/2)² = 16 and (-2/2)² = 1; 8 + 17 = 25."])
B.orq(S, "cp1", "Rewrite x² + y² - 4x + 10y + 13 = 0.", [("Group the terms.", "(x² - 4x) + (y² + 10y) = -13"), ("Complete both squares.", "(x - 2)² + (y + 5)² = 16"), ("Find the center and radius.", "(2, -5); 4"), ("Find the y-intercepts.", "(0, -5 ± 2√3)")],
      ["Move 13.", "Add 4 and 25.", "Read.", "x = 0: 4 + (y + 5)² = 16 → y = -5 ± 2√3."])
assert abs(4 + (2 * sqr(3)) ** 2 - 16) < 1e-9
B.orq(S, "honors", "Rewrite 9x² - 4y² - 54x - 16y + 29 = 0.", [("Group and factor.", "9(x² - 6x) - 4(y² + 4y) = -29"), ("Complete the squares.", "9(x - 3)² - 4(y + 2)² = 36"), ("Write in standard form.", "(x - 3)²/4 - (y + 2)²/9 = 1"), ("Identify the conic and its center.", "hyperbola; (3, -2)")],
      ["Factor 9 and -4.", "Add 81 and subtract 16.", "Divide by 36.", "Opposite signs."], tags=["challenge"])
assert -29 + 81 - 16 == 36
B.sa(S, "cp2", "Write x² + y² - 2x - 8 = 0 in standard form.", "(x - 1)² + y² = 9", ["Add 1 to both sides."])

# ---------------- Skill 7: identifying conics ----------------
S = 7
for eq, kind in [("x² + y² - 4x + 6y - 3 = 0", "circle"), ("4x² + 9y² - 16x + 18y - 11 = 0", "ellipse"), ("x² - y² + 2x - 4y - 7 = 0", "hyperbola"), ("y² - 8x + 2y + 9 = 0", "parabola"),
                 ("3x² + 3y² - 12 = 0", "circle"), ("2x² - 5y² + 10 = 0", "hyperbola"), ("x² + 4x - y + 1 = 0", "parabola"), ("5x² + y² - 20 = 0", "ellipse"), ("-x² + 4y² - 8y = 0", "hyperbola"), ("6x² + 6y² + 12x = 0", "circle")]:
    B.mc(S, "cp2" if kind in ("circle", "parabola") else "cp1", f"Identify the conic: {eq}.", kind.capitalize(), [k.capitalize() for k in ["circle", "ellipse", "hyperbola", "parabola"] if k != kind],
         ["Compare the x² and y² coefficients A and C.", "A = C → circle; same sign, different → ellipse; opposite signs → hyperbola; one is 0 → parabola."])
for A, Bc, C, kind in [(1, 2, 1, "parabola"), (2, 1, 3, "ellipse"), (1, 4, 1, "hyperbola"), (3, 0, -2, "hyperbola"), (1, -6, 9, "parabola")]:
    disc = Bc * Bc - 4 * A * C
    B.sa(S, "honors", f"Use the discriminant B² - 4AC to classify {A if A != 1 else ''}x² + {Bc if Bc != 1 else ''}xy + {C if C != 1 else ''}y² + 3x - y + 2 = 0.".replace("+ 0xy ", "").replace("+ -", "- "), f"B² - 4AC = {disc}; {kind}",
         ["B² - 4AC < 0 → ellipse (or circle); = 0 → parabola; > 0 → hyperbola.", f"{Bc}² - 4({A})({C}) = {disc}."], tags=["challenge"])
sel_auto(B, S, "cp1", "Select ALL equations whose graphs are ellipses (not circles).", ["x²/9 + y²/4 = 1", "4x² + y² = 16", "2x² + 3y² - 6 = 0", "x² + y² = 9", "x²/4 - y²/9 = 1", "y = x² + 1"],
         lambda s_: s_ in ("x²/9 + y²/4 = 1", "4x² + y² = 16", "2x² + 3y² - 6 = 0"), ["Same sign, different coefficients after standard form."])
sel_auto(B, S, "cp1", "Select ALL equations whose graphs are hyperbolas.", ["x² - y² = 1", "y²/16 - x²/9 = 1", "xy = 4", "x² + y² = 1", "y = 2x²", "x² + 2y² = 8"],
         lambda s_: s_ in ("x² - y² = 1", "y²/16 - x²/9 = 1", "xy = 4"), ["Opposite-sign squared terms, or xy = k (rotated hyperbola)."], tags=["challenge"])
B.mc(S, "cp1", "A student says 3x² + 3y² - 6x = 12 is an ellipse because the coefficients are not 1. What is correct?", "Circle: A = C", ["Ellipse", "Hyperbola", "Parabola"], ["Divide by 3: x² + y² - 2x = 4 → (x - 1)² + y² = 5."], tags=["error-analysis", "misconception"])
B.mc(S, "honors", "Which plane slice of a double cone produces a hyperbola?", "A plane parallel to the cone's axis, cutting both nappes", ["A plane perpendicular to the axis", "A plane parallel to a side (generator)", "A plane tilted slightly from horizontal"], ["Perpendicular → circle; tilted → ellipse; parallel to a generator → parabola; cutting both nappes → hyperbola."], tags=["connections"])
B.orq(S, "cp1", "Classify and describe each: (a) x² + y² = 49, (b) x²/49 + y² = 1, (c) x²/49 - y² = 1, (d) y = x²/49.", [("(a)", "circle, radius 7"), ("(b)", "ellipse, vertices (±7, 0)"), ("(c)", "hyperbola, vertices (±7, 0)"), ("(d)", "parabola, vertex (0, 0)")],
      ["Equal coefficients.", "Different positive denominators.", "Subtraction.", "Only one squared variable."])
B.orq(S, "honors", "Explore Ax² + Cy² = 36 for different A and C.", [("A = C = 4: classify.", "circle, radius 3"), ("A = 4, C = 9: classify.", "ellipse"), ("A = 4, C = -9: classify.", "hyperbola"), ("A = 4, C = 0: describe the graph.", "two vertical lines x = ±3")],
      ["x² + y² = 9.", "x²/9 + y²/4 = 1.", "x²/9 - y²/4 = 1.", "4x² = 36 → degenerate."], tags=["reasoning"])
B.sa(S, "cp2", "Identify the conic: y = 3x² - 2x + 1.", "parabola", ["Only x is squared."])
B.sa(S, "cp1", "Identify the conic: 9y² - x² - 18y = 0.", "hyperbola", ["x² and y² coefficients have opposite signs."])

# ================= additions: format balance =================
B.sel(1, "cp1", "Circle (x + 4)² + (y - 3)² = 25. Select ALL true statements.", ["The center is (-4, 3)", "The radius is 5", "The circle passes through the origin"], ["The center is (4, -3)", "The radius is 25", "The circle is tangent to the y-axis"],
      ["h = -4, k = 3, r = 5.", "(0 + 4)² + (0 - 3)² = 25 ✓."])
B.sa(1, "cp1", "Find the radius of the circle centered at (2, -1) that passes through (5, 3).", "5", ["√(9 + 16)."])
for h, k, p_, vert in [(0, 0, 3, True), (2, -1, -1, False), (-3, 2, 2, True), (1, 1, F(1, 2), False)]:
    eqv = f"{sq('x', h)} = {fr(4 * p_)}{lin('y', k)}" if vert else f"{sq('y', k)} = {fr(4 * p_)}{lin('x', h)}"
    good = pt(h, F(k) + p_) if vert else pt(F(h) + p_, k)
    wr = [pt(h, F(k) - p_) if vert else pt(F(h) - p_, k), pt(h, F(k) + 4 * F(p_)) if vert else pt(F(h) + 4 * F(p_), k), pt(F(h) + p_, k) if vert else pt(h, F(k) + p_)]
    B.mc(2, "cp1", f"Find the focus of {eqv}.", good, wr, [f"4p = {fr(4 * F(p_))} → p = {fr(p_)}.", "The focus is p units from the vertex in the direction the parabola opens.", "Using 4p instead of p, or the wrong axis, are common errors."], tags=["misconception"])
for eqv, st in [("(y + 3)² = 8(x - 1)", {"The vertex is (1, -3)": True, "The focus is (3, -3)": True, "The directrix is x = -1": True, "It opens right": True, "The focus is (1, -1)": False, "It opens up": False}),
                ("x² = -2(y - 4)", {"The vertex is (0, 4)": True, "The focus is (0, 7/2)": True, "The directrix is y = 9/2": True, "It opens down": True, "The focus is (0, 2)": False, "The directrix is y = 6": False})]:
    B.sel(2, "cp1", f"{eqv}. Select ALL true statements.", [k_ for k_, t_ in st.items() if t_], [k_ for k_, t_ in st.items() if not t_], ["Find 4p, then p.", "Focus and directrix are p units on either side of the vertex."])
B.orq(2, "cp1", "A parabola has vertex (3, 1) and focus (3, -2).", [("Which way does it open?", "down"), ("Find p.", "-3"), ("Write its equation.", "(x - 3)² = -12(y - 1)"), ("Write the directrix.", "y = 4")], ["Focus below vertex.", "-2 - 1.", "4p = -12.", "1 + 3."])
for a2, b2, horiz in [(25, 16, True), (9, 25, False), (100, 36, True), (13, 4, True)]:
    c2 = max(a2, b2) - min(a2, b2); eq = f"x²/{a2} + y²/{b2} = 1"
    good = (f"(±{rad(c2)}, 0)" if a2 > b2 else f"(0, ±{rad(c2)})")
    wr = [f"(±{rad(a2 + b2)}, 0)" if a2 > b2 else f"(0, ±{rad(a2 + b2)})", f"(0, ±{rad(c2)})" if a2 > b2 else f"(±{rad(c2)}, 0)", f"(±{rad(max(a2, b2))}, 0)" if a2 > b2 else f"(0, ±{rad(max(a2, b2))})"]
    B.mc(3, "cp1", f"Find the foci of {eq}.", good, wr, ["Ellipse: c² = a² - b² (larger minus smaller).", "Foci lie on the major axis."], tags=["misconception"])
for eq, st in [("x²/16 + y²/49 = 1", {"The major axis is vertical": True, "The vertices are (0, ±7)": True, "The co-vertices are (±4, 0)": True, "The foci are (0, ±√33)": True, "The foci are (±√65, 0)": False, "The major axis has length 7": False}),
               ("(x - 1)²/9 + (y + 2)²/5 = 1", {"The center is (1, -2)": True, "The foci are (3, -2) and (-1, -2)": True, "The vertices are (4, -2) and (-2, -2)": True, "The center is (-1, 2)": False, "The minor axis has length 5": False})]:
    B.sel(3, "cp1", f"{eq}. Select ALL true statements.", [k_ for k_, t_ in st.items() if t_], [k_ for k_, t_ in st.items() if not t_], ["Identify a², b²; c² = a² - b².", "Axis lengths are 2a and 2b."])
for (h, k), a, b, horiz in [((0, 0), 13, 5, True), ((2, -1), 5, 3, False)]:
    c = int(sqr(a * a - b * b)); eqe = f"{sq('x', h)}/{(a if horiz else b) ** 2} + {sq('y', k)}/{(b if horiz else a) ** 2} = 1"
    B.orq(3, "honors" if h else "cp1", f"An ellipse has center {pt(h, k)}, a {'horizontal' if horiz else 'vertical'} major axis, a = {a}, and b = {b}.", [("Write the equation.", eqe), ("Find c.", str(c)),
          ("Find the foci.", f"{pt(h - c, k)} and {pt(h + c, k)}" if horiz else f"{pt(h, k + c)} and {pt(h, k - c)}"), ("Find the eccentricity.", fr(F(c, a)))], ["Standard form.", "c² = a² - b².", "Along the major axis.", "e = c/a."])
B.sa(3, "cp1", "Write the equation of the ellipse with vertices (0, ±6) and co-vertices (±2, 0).", "x²/4 + y²/36 = 1", ["a = 6 vertical, b = 2."])
for a2, b2, horiz in [(9, 16, True), (16, 9, False), (4, 21, True), (64, 36, False)]:
    c2 = a2 + b2; eq = f"x²/{a2} - y²/{b2} = 1" if horiz else f"y²/{a2} - x²/{b2} = 1"
    good = f"(±{rad(c2)}, 0)" if horiz else f"(0, ±{rad(c2)})"
    wr = [f"(±{rad(abs(a2 - b2))}, 0)" if horiz else f"(0, ±{rad(abs(a2 - b2))})", f"(0, ±{rad(c2)})" if horiz else f"(±{rad(c2)}, 0)", f"(±{rad(a2)}, 0)" if horiz else f"(0, ±{rad(a2)})"]
    B.mc(4, "cp1", f"Find the foci of {eq}.", good, wr, ["Hyperbola: c² = a² + b².", "Foci lie on the transverse axis (the positive term's variable)."], tags=["misconception"])
for eq, st in [("y²/36 - x²/64 = 1", {"It opens up and down": True, "The vertices are (0, ±6)": True, "The foci are (0, ±10)": True, "The asymptotes are y = ±(3/4)x": True, "The asymptotes are y = ±(4/3)x": False, "The vertices are (±8, 0)": False}),
               ("(x + 1)²/4 - (y - 3)²/12 = 1", {"The center is (-1, 3)": True, "The vertices are (1, 3) and (-3, 3)": True, "The foci are (3, 3) and (-5, 3)": True, "The asymptote slopes are ±√3": True, "The foci are (-1, 7) and (-1, -1)": False, "It opens up and down": False})]:
    B.sel(4, "cp1", f"{eq}. Select ALL true statements.", [k_ for k_, t_ in st.items() if t_], [k_ for k_, t_ in st.items() if not t_], ["a² is under the positive term; c² = a² + b².", "Asymptote slope ±b/a (horizontal) or ±a/b (vertical)."])
B.orq(4, "honors", "A hyperbola has foci (0, ±5) and vertices (0, ±4).", [("Find a and c.", "a = 4, c = 5"), ("Find b.", "3"), ("Write the equation.", "y²/16 - x²/9 = 1"), ("Write the asymptotes.", "y = ±(4/3)x")], ["Read from the points.", "b² = c² - a².", "Vertical transverse axis.", "±a/b."])
B.sa(4, "cp1", "Write the equation of the hyperbola with vertices (±2, 0) and foci (±3, 0).", "x²/4 - y²/5 = 1", ["a = 2, c = 3, b² = 5."])
g2 = [("circle", (lambda X, Y: (X + 2) ** 2 + (Y - 1) ** 2 - 16), "(x + 2)² + (y - 1)² = 16", "a circle with center (-2, 1) and radius 4", [(-2, 1, True, "(-2, 1)")], [("Center?", "(-2, 1)"), ("Radius?", "4"), ("Write the equation.", "(x + 2)² + (y - 1)² = 16"), ("Is (2, 1) on the circle?", "Yes")]),
      ("ellipse", (lambda X, Y: X ** 2 / 9 + (Y + 1) ** 2 / 25 - 1), "x²/9 + (y + 1)²/25 = 1", "a vertical ellipse centered at (0, -1) through (0, 4), (0, -6), (±3, -1)", [(0, 4), (0, -6), (3, -1), (-3, -1)], [("Center?", "(0, -1)"), ("Vertices?", "(0, 4) and (0, -6)"), ("Write the equation.", "x²/9 + (y + 1)²/25 = 1"), ("Foci?", "(0, 3) and (0, -5)")]),
      ("hyperbola", (lambda X, Y: Y ** 2 / 9 - X ** 2 / 16 - 1), "y²/9 - x²/16 = 1", "a hyperbola opening up and down with vertices (0, ±3) and dashed asymptotes y = ±(3/4)x", [(0, 3), (0, -3)], [("Which way does it open?", "up and down"), ("Vertices?", "(0, ±3)"), ("Asymptotes?", "y = ±(3/4)x"), ("Write the equation.", "y²/9 - x²/16 = 1")])]
for i, (kind, Fn, eq, desc, pts_, parts) in enumerate(g2):
    curves = [(("implicit", Fn), {})] + ([(lambda v: 0.75 * v, {"color": "#888888", "lw": 1, "ls": "--"}), (lambda v: -0.75 * v, {"color": "#888888", "lw": 1, "ls": "--"})] if kind == "hyperbola" else [])
    for p_ in pts_:
        if kind != "circle": assert abs(Fn(p_[0], p_[1])) < 1e-9
    dg = graph(B, f"s05-more-{kind}-{i}", curves, xr=(-8, 8), yr=(-8, 8), points=pts_, alt=f"Graph of {desc}.")
    B.orq(5, "cp1", "Use the graph of the conic.", parts, ["Read the center and key points.", "Use the standard form for this conic."], diagram=dg, tags=["graph"])
    B.sel(5, "cp1", "Select ALL statements that describe the graph.", [f"It is a{'n' if kind[0] in 'aeiou' else ''} {kind}", f"Its equation is {eq}"], [f"It is a parabola", f"Its equation is {eq.replace('= 16', '= 4').replace('/25', '/5').replace('/9 - ', '/3 - ')}"], ["Identify the shape, then check the key points."], diagram=dg, tags=["graph"])
B.mc(5, "cp1", "Which feature do ellipses and hyperbolas both have?", "Two foci", ["Asymptotes", "A directrix only", "Exactly one vertex"], ["Both are defined using two foci (sum vs difference of distances)."], tags=["connections"])
for h, k, r2 in [(3, -4, 4), (-5, 1, 10), (0, -3, 25), (6, 2, 8)]:
    D, E, Fc = -2 * h, -2 * k, h * h + k * k - r2
    B.mc(6, "cp1", f"Find the center and radius of {gen_form(1, 1, D, E, Fc)}.", f"center {pt(h, k)}, radius {rtxt(r2)}", [f"center {pt(-h, -k)}, radius {rtxt(r2)}", f"center {pt(h, k)}, radius {rtxt(-Fc) if -Fc > 0 else rtxt(r2 + 1)}", f"center {pt(D, E)}, radius {rtxt(r2)}"],
         ["Complete the square in x and y.", f"(x - h)² + (y - k)² = {r2}."], tags=["misconception"])
B.sel(6, "cp1", "x² + y² + 6x - 8y = 0. Select ALL true statements.", ["The center is (-3, 4)", "The radius is 5", "The circle passes through the origin"], ["The center is (3, -4)", "The radius is 25", "The radius is 0"], ["(x + 3)² + (y - 4)² = 25.", "No constant term → (0, 0) satisfies it."])
B.sel(6, "honors", "Select ALL equations that represent a real circle (positive radius).", ["x² + y² - 2x - 3 = 0", "x² + y² + 4y = 0", "2x² + 2y² - 8 = 0"], ["x² + y² + 2x + 5 = 0", "x² + y² - 4x + 4 = 0", "x² - y² = 9"],
      ["Complete squares: r² = 4, 4, 4.", "x² + y² + 2x + 5 = 0 → r² = -4; x² + y² - 4x + 4 = 0 → r² = 0 (a point); x² - y² is a hyperbola."], tags=["reasoning"])
B.orq(6, "honors", "Rewrite 4x² + y² + 16x - 6y + 9 = 0.", [("Group and factor.", "4(x² + 4x) + (y² - 6y) = -9"), ("Complete the squares.", "4(x + 2)² + (y - 3)² = 16"), ("Standard form.", "(x + 2)²/4 + (y - 3)²/16 = 1"), ("Identify the conic and its vertices.", "ellipse; (-2, 7) and (-2, -1)")],
      ["Factor 4.", "Add 16 and 9.", "Divide by 16.", "a = 4 vertical."])
assert -9 + 16 + 9 == 16
B.sa(6, "cp1", "Write y² - 4y - 4x = 0 in standard form.", "(y - 2)² = 4(x + 1)", ["(y - 2)² - 4 = 4x."])
B.sa(6, "cp1", "Write x² + 6x - 8y + 1 = 0 in standard form and find the vertex.", "(x + 3)² = 8(y + 1); vertex (-3, -1)", ["(x + 3)² - 9 + 1 = 8y."])
for eq, kind in [("x² = 4y - y²", "circle"), ("y² = 9 - 4x²", "ellipse"), ("y² = x² + 4", "hyperbola"), ("x = y² - 6y", "parabola")]:
    B.mc(7, "cp1", f"Identify the conic: {eq}.", kind.capitalize(), [k.capitalize() for k in ["circle", "ellipse", "hyperbola", "parabola"] if k != kind], ["Move all terms to one side first.", "Then compare the x² and y² coefficients."], tags=["misconception"])
B.sel(7, "cp1", "Select ALL equations whose graph is a parabola.", ["y = x² - 3x", "x = 2y² + 1", "y² - 4x + 2y = 0"], ["x² + y² = 4", "x² - 4y² = 4", "4x² + y² = 4"], ["Exactly one variable is squared."])
B.sel(7, "honors", "For Ax² + Cy² + Dx + Ey + F = 0 (no xy-term), select ALL correct classification rules.", ["A = C ≠ 0 → circle (if real)", "AC > 0, A ≠ C → ellipse (if real)", "AC < 0 → hyperbola", "AC = 0 (one of A, C zero) → parabola"], ["A > C → hyperbola", "D = E → circle"],
      ["Classification depends on the signs and equality of A and C."], tags=["reasoning"])
B.orq(7, "cp1", "Classify by rearranging: (a) x² + y² = 6x, (b) y = 4 - x², (c) 4y² = 36 + 9x², (d) 2x² + 8y² = 32.", [("(a)", "circle"), ("(b)", "parabola"), ("(c)", "hyperbola"), ("(d)", "ellipse")], ["A = C.", "One square.", "4y² - 9x² = 36.", "Same sign, different."])
B.sa(7, "cp1", "Identify the conic: 16x² + 16y² - 32x = 0.", "circle", ["A = C = 16."])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
