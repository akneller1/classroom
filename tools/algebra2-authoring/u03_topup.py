"""Session-2 top-up for quadratic-functions-complex-numbers: appends items (IDs continue) to the session-1 bank."""
from lib import Bank, graph
from mathlite import *
import cmath

STD = {1: ["F-IF.C.7a"], 2: ["F-IF.C.8a", "A-SSE.B.3a"], 3: ["A-SSE.A.2"], 4: ["A-REI.B.4a", "A-REI.B.4b"],
       5: ["A-REI.B.4b"], 6: ["N-CN.A.1", "N-CN.A.2"], 7: ["N-CN.C.7"], 8: ["F-IF.B.4", "A-CED.A.1"]}
U = "quadratic-functions-complex-numbers"
B = Bank.resume(U, "qc", STD, f"base/{U}.json", f"base/{U}.tags.json")  # session-1 bank (pristine copy) so reruns are idempotent
N0 = len(B.qs)
import s1_fixes; s1_fixes.apply(B)  # cosmetic notation fixes to session-1 items (see PROGRESS.md)


def vtx(a, b, c):
    h = F(-b, 2 * a); return h, a * h * h + b * h + c


def cx(z):
    """complex → 'a + bi' text with exact small rationals."""
    a, b = F(z.real).limit_denominator(1000), F(z.imag).limit_denominator(1000)
    if b == 0: return fr(a)
    bi = ("" if abs(b) == 1 else fr(abs(b))) + "i"
    if a == 0: return ("-" if b < 0 else "") + bi
    return f"{fr(a)} {'-' if b < 0 else '+'} {bi}"


# ---- Skill 1: graphing quadratics ----
for a, b, c in [(1, -6, 5), (-2, 8, -3), (F(1, 2), 2, -4), (3, 0, -12)]:
    f = P([c, b, a]); h, k = vtx(a, b, c); rts = sorted(f.rational_roots()[0])
    cands = [f"vertex {pt(h, k)}", f"axis x = {fr(h)}", f"y-intercept {fr(c)}", f"opens {'up' if a > 0 else 'down'}", f"vertex {pt(-h, k)}" if h else f"vertex {pt(h, -k)}", f"opens {'down' if a > 0 else 'up'}", f"axis x = {fr(-h)}" if h else "axis y = 0"]
    truth = [True, True, True, True, False, False, False]
    B.sel(1, "cp2" if a == 1 else "cp1", f"y = {f}. Select ALL true statements.", [c_ for c_, t_ in zip(cands, truth) if t_], [c_ for c_, t_ in zip(cands, truth) if not t_], ["h = -b/(2a); k = f(h).", "y-intercept = c; sign of a sets the direction."])
for a, h, k in [(1, -2, -1), (-1, 1, 4), (2, 0, -2)]:
    fn = lambda v, a=a, h=h, k=k: a * (v - h) ** 2 + k
    eq = f"y = {'' if a == 1 else '-' if a == -1 else a}{'x²' if h == 0 else f'(x {chr(45) if h > 0 else chr(43)} {abs(h)})²'}{'' if k == 0 else (' + ' if k > 0 else ' - ') + str(abs(k))}"
    dg = graph(B, f"s01-topup-{len(B.qs)}", [(fn, {})], points=[(h, k, True, pt(h, k)), (h + 1, a + k), (h - 1, a + k)], alt=f"A parabola with vertex {pt(h, k)} opening {'up' if a > 0 else 'down'}, passing through ({h - 1}, {a + k}) and ({h + 1}, {a + k}).")
    B.orq(1, "cp2" if abs(a) == 1 else "cp1", "Use the graph of the parabola.", [("Find the vertex.", pt(h, k)), ("Find the axis of symmetry.", f"x = {h}"), ("Find the range.", f"y ≥ {k}" if a > 0 else f"y ≤ {k}"), ("Write the equation in vertex form.", eq)],
          ["Turning point.", "Vertical line through the vertex.", "From the vertex up or down.", "Use a second point to find a."], diagram=dg, tags=["graph"])
B.sa(1, "honors", "A parabola has vertex (3, -8) and one x-intercept at 5. Find the other x-intercept and the equation.", "x = 1; y = 2(x - 3)² - 8", ["Symmetric about x = 3: 3 - 2 = 1.", "0 = 4a - 8 → a = 2."], tags=["reasoning"])
B.sa(1, "cp2", "Does y = -3x² + 2 have a maximum or minimum? What is it?", "maximum 2", ["a < 0 → maximum at the vertex (0, 2)."])
B.mc(1, "honors", "For y = ax² + bx + c with a > 0 and b > 0, where is the vertex?", "left of the y-axis (x < 0)", ["right of the y-axis", "on the y-axis", "cannot be determined"], ["h = -b/(2a) < 0."], tags=["reasoning"])

# ---- Skill 2: vertex and intercept forms ----
for a, r1, r2 in [(1, -1, 5), (-2, 0, 4), (3, -3, 1)]:
    f = P.roots([r1, r2], a); h = F(r1 + r2, 2); k = f(h)
    vf = f"y = {'' if a == 1 else '-' if a == -1 else a}(x {'-' if h > 0 else '+'} {fr(abs(h))})² {'+' if k >= 0 else '-'} {fr(abs(k))}".replace("(x - 0)", "x").replace("(x + 0)", "x")
    sf = f"y = {f}"; inf = f"y = {'' if a == 1 else '-' if a == -1 else a}{lin_factor(r1)}{lin_factor(r2)}".replace("(x - 0)", "x")
    B.sel(2, "cp1", f"Select ALL equations for the parabola with x-intercepts {r1} and {r2} and leading coefficient {a}.", [sf, vf, inf], [f"y = {'' if a == 1 else '-' if a == -1 else a}{lin_factor(-r1)}{lin_factor(-r2)}".replace("(x - 0)", "x"), vf.replace(f"{fr(abs(k))}", f"{fr(abs(k) + 1)}")],
          ["Standard, vertex, and intercept forms describe the same parabola.", "Check zeros and the vertex."], tags=["multiple-representations"])
    for s_ in (sf, vf, inf): assert eqcheck(s_.split("= ")[1].replace("²", "^2"), str(f).replace("²", "^2"))
B.orq(2, "cp1", "Rewrite y = x² + 10x + 21 three ways.", [("Factor into intercept form.", "y = (x + 3)(x + 7)"), ("Complete the square for vertex form.", "y = (x + 5)² - 4"), ("Find the vertex and zeros.", "(-5, -4); -3 and -7"), ("Which form shows the y-intercept directly? Give it.", "standard form; 21")],
      ["Factor pairs of 21.", "(10/2)² = 25.", "Read from each form.", "c = 21."], tags=["multiple-representations"])
B.orq(2, "honors", "y = a(x - h)² + k passes through (0, 5), (1, 0), and (5, 0).", [("Find h.", "3"), ("Write y = a(x - 1)(x - 5) and find a.", "a = 1"), ("Find k.", "-4"), ("Write vertex form.", "y = (x - 3)² - 4")], ["Midpoint of the zeros.", "5 = a(-1)(-5).", "f(3) = (2)(-2).", "Combine."], tags=["challenge"])
B.mc(2, "cp2", "Which equation is in vertex form?", "y = 2(x - 1)² + 3", ["y = 2x² - 4x + 5", "y = 2(x - 1)(x - 3)", "y = (2x - 1)² + 3x"], ["Vertex form: a(x - h)² + k."])
B.sa(2, "cp2", "Write y = (x - 4)(x + 2) in standard form.", "y = x² - 2x - 8", ["FOIL."])
B.sa(2, "cp1", "Find the vertex of y = -(x - 6)(x + 2).", "(2, 16)", ["h = (6 - 2)/2 = 2; y = -(−4)(4) = 16."])

# ---- Skill 3: factoring ----
for e, tgt in [(P.coeffs(2, 5, -12), "(2x - 3)(x + 4)"), (P.coeffs(9, 0, -16), "(3x - 4)(3x + 4)"), (P.coeffs(6, -11, 3), "(3x - 1)(2x - 3)")]:
    cands = [tgt, tgt.replace("-", "@").replace("+", "-").replace("@", "+"), tgt.split(")(")[1][:-1].join(["(", ")"]) + tgt.split(")(")[0] + ")", f"({str(e)})"]
    sel_auto(B, 3, "cp1", f"Select ALL expressions equivalent to {e}.", cands + [f"(x + {abs(e.c[0])})(x - 1)"], is_equiv(str(e).replace("²", "^2")), ["Multiply out each option to check.", "Order of factors does not matter."])
B.orq(3, "honors", "Factor 4x⁴ - 37x² + 9 completely.", [("Substitute u = x².", "4u² - 37u + 9"), ("Factor in u.", "(4u - 1)(u - 9)"), ("Substitute back.", "(4x² - 1)(x² - 9)"), ("Factor completely.", "(2x - 1)(2x + 1)(x - 3)(x + 3)")], ["Quadratic in form.", "ac = 36: -1 and -36.", "u = x².", "Differences of squares."], tags=["challenge"])
assert eqcheck("4x^4 - 37x^2 + 9", "(2x - 1)(2x + 1)(x - 3)(x + 3)")
B.mc(3, "cp2", "What is the GCF of 6x² - 18x?", "6x", ["6", "3x", "x"], ["6x(x - 3)."])
B.mc(3, "cp1", "A student factors x² - 5x - 14 as (x - 2)(x + 7). What is correct?", "(x - 7)(x + 2)", ["(x - 2)(x + 7)", "(x + 7)(x + 2)", "(x - 14)(x + 1)"], ["Need product -14 and sum -5: -7 and 2."], tags=["error-analysis"])
B.sa(3, "cp2", "Factor x² + 9x + 20.", "(x + 4)(x + 5)", ["4·5 = 20, 4 + 5 = 9."])
B.sa(3, "cp2", "Factor x² - 81.", "(x - 9)(x + 9)", ["Difference of squares."])

# ---- Skill 4: square roots and completing the square ----
for b, c in [(4, -12), (-6, 2), (8, 11), (-10, 18)]:
    k = b * b // 4 - c; h = -b // 2
    sols = f"x = {fr(h)} ± {rad(k)}" if k > 0 and math.isqrt(k) ** 2 != k else (f"x = {h - math.isqrt(k)} or x = {h + math.isqrt(k)}" if k > 0 else f"x = {fr(h)} ± {rad(-k)}i")
    B.orq(4, "cp1" if k > 0 else "honors", f"Solve x² {'+' if b > 0 else '-'} {abs(b)}x {'+' if c > 0 else '-'} {abs(c)} = 0 by completing the square.", [("Move the constant.", f"x² {'+' if b > 0 else '-'} {abs(b)}x = {-c}"), ("Add (b/2)² to both sides.", f"(x {'+' if b > 0 else '-'} {abs(b) // 2})² = {k}"), ("Take square roots.", f"x {'+' if b > 0 else '-'} {abs(b) // 2} = ±{rad(abs(k))}{'' if k > 0 else 'i'}".replace("±1i", "±i")), ("Solve.", sols)],
          ["Isolate x-terms.", f"(b/2)² = {b * b // 4}.", "± root.", "Isolate x."])
    for r_ in (complex(h, 0) + cmath.sqrt(k), complex(h, 0) - cmath.sqrt(k)): assert abs(r_ * r_ + b * r_ + c) < 1e-9
sel_auto(B, 4, "cp1", "Select ALL solutions of (x - 3)² = 25.", ["8", "-2", "28", "-22", "2", "-8"], lambda s_: (int(s_) - 3) ** 2 == 25, ["x - 3 = ±5."])
sel_auto(B, 4, "honors", "Select ALL solutions of 2(x + 1)² - 7 = 11.", ["2", "-4", "-1 + 3", "-1 - 3", "4", "-2"], lambda s_: same(2 * (peval(s_) + 1) ** 2 - 7, 11), ["(x + 1)² = 9 → x = -1 ± 3."])
B.mc(4, "cp1", "Which value of c makes x² - 7x + c a perfect square trinomial?", "49/4", ["49", "7/2", "-49/4"], ["c = (b/2)² = (7/2)²."])
B.sa(4, "cp2", "Solve x² - 64 = 0.", "x = ±8", ["x² = 64."])
B.sa(4, "honors", "Solve 3x² + 12x - 2 = 0 by completing the square. Give exact solutions.", "x = -2 ± √42/3", ["x² + 4x = 2/3 → (x + 2)² = 14/3.", "x = -2 ± √(14/3) = -2 ± √42/3."], tags=["challenge"])
for r_ in (-2 + (42 ** .5) / 3, -2 - (42 ** .5) / 3): assert abs(3 * r_ * r_ + 12 * r_ - 2) < 1e-9

# ---- Skill 5: quadratic formula and discriminant ----
for a, b, c in [(2, 3, -2), (1, -4, 2), (3, -2, 5), (4, 4, 1), (5, 1, -3)]:
    d = b * b - 4 * a * c
    kind = "two real" if d > 0 else ("one real" if d == 0 else "two non-real")
    rat = d >= 0 and math.isqrt(d) ** 2 == d
    st = {f"The discriminant is {d}": True, f"There are {kind} solutions": True, "The solutions are rational": rat and d >= 0, "The graph crosses the x-axis twice": d > 0, f"The discriminant is {b * b + 4 * a * c}": b * b + 4 * a * c == d, "The graph does not meet the x-axis": d < 0}
    right = [s_ for s_, t_ in st.items() if t_]; wrong = [s_ for s_, t_ in st.items() if not t_]
    B.sel(5, "cp1", f"For {P.coeffs(a, b, c)} = 0, select ALL true statements.", right, wrong, [f"b² - 4ac = {b * b} - {4 * a * c} = {d}.", "Positive: 2 real (rational if a perfect square); 0: 1 real; negative: 2 non-real."])
B.orq(5, "cp1", "Solve 2x² - 6x + 3 = 0 with the quadratic formula.", [("Identify a, b, c.", "a = 2, b = -6, c = 3"), ("Find the discriminant.", "12"), ("Write the exact solutions.", "x = (3 ± √3)/2"), ("Approximate to the nearest hundredth.", f"{(3 - 3 ** .5) / 2:.2f} and {(3 + 3 ** .5) / 2:.2f}")],
      ["Read coefficients.", "36 - 24.", "(6 ± 2√3)/4.", "Calculator."])
B.orq(5, "honors", "For x² + kx + 4 = 0:", [("Write the discriminant in terms of k.", "k² - 16"), ("For what k is there exactly one real solution?", "k = ±4"), ("For what k are there two real solutions?", "k < -4 or k > 4"), ("For k = 2, find the solutions.", "x = -1 ± i√3")],
      ["b² - 4ac.", "= 0.", "> 0.", "(-2 ± √(-12))/2."], tags=["challenge"])
B.mc(5, "cp1", "Which expression is the quadratic formula?", "x = (-b ± √(b² - 4ac))/(2a)", ["x = -b ± √(b² - 4ac)/(2a)", "x = (b ± √(b² - 4ac))/(2a)", "x = (-b ± √(b² + 4ac))/(2a)"], ["The whole numerator is divided by 2a."], tags=["misconception"])
B.sa(5, "cp2", "Find the discriminant of x² + 6x + 9.", "0", ["36 - 36."])
B.sa(5, "cp2", "How many real solutions does x² + 1 = 0 have?", "0", ["Discriminant -4 < 0."])
B.sa(5, "cp1", "Solve x² - 2x - 4 = 0 exactly.", "x = 1 ± √5", ["(2 ± √20)/2."])
B.sa(5, "honors", "The sum of the roots of 3x² + bx + 12 = 0 is 5. Find b and the product of the roots.", "b = -15; product 4", ["Sum = -b/a = 5 → b = -15.", "Product = c/a = 4."], tags=["connections"])

# ---- Skill 6: complex numbers ----
for z, w in [(2 + 3j, 1 - 4j), (-1 + 2j, 3 + 1j), (4 - 1j, 4 + 1j)]:
    B.orq(6, "cp1", f"Let z = {cx(z)} and w = {cx(w)}.", [("Find z + w.", cx(z + w)), ("Find z - w.", cx(z - w)), ("Find zw.", cx(z * w)), ("Find z/w in a + bi form.", cx(z / w))],
          ["Add real and imaginary parts.", "Subtract each part.", "FOIL; i² = -1.", "Multiply by the conjugate of w."])
sel_auto(B, 6, "cp1", "Select ALL expressions equal to -1.", ["i²", "i⁶", "i¹⁰", "i⁴", "i³", "(-i)²", "i¹⁰⁰"], lambda s_: {"i²": -1, "i⁶": -1, "i¹⁰": -1, "i⁴": 1, "i³": None, "(-i)²": -1, "i¹⁰⁰": 1}[s_] == -1, ["Powers of i cycle i, -1, -i, 1."])
B.mc(6, "cp2", "What is the conjugate of -5 + 2i?", "-5 - 2i", ["5 - 2i", "5 + 2i", "-5 + 2i"], ["Change the sign of the imaginary part."], tags=["misconception"])
B.sa(6, "honors", "Find |6 - 8i| and the distance between 1 + 2i and 4 - 2i in the complex plane.", "10; 5", ["√(36 + 64).", "|3 - 4i| = 5."], tags=["connections"])
B.sa(6, "cp2", "Simplify (5 - 2i) - (3 - 7i).", "2 + 5i", ["5 - 3 = 2; -2 + 7 = 5."])

# ---- Skill 7: complex solutions ----
for a, b, c in [(1, -2, 5), (1, 4, 13), (2, 2, 5), (1, 0, 49), (9, -6, 2)]:
    d = b * b - 4 * a * c; r1 = (-b + cmath.sqrt(d)) / (2 * a); r2 = r1.conjugate()
    cands = [cx(r1), cx(r2), cx(-r1), cx(complex(r1.imag, r1.real)), cx(complex(-b / (2 * a), 0))]
    sel_auto(B, 7, "cp1" if a == 1 else "honors", f"Select ALL solutions of {P.coeffs(a, b, c)} = 0.", cands, lambda s_, a=a, b=b, c=c: abs(a * complex(peval(s_)) ** 2 + b * complex(peval(s_)) + c) < 1e-9, ["Quadratic formula with a negative discriminant.", "Solutions are complex conjugates."])
for zs, poly in [(("3i", "-3i"), "x² + 9"), (("1 + i", "1 - i"), "x² - 2x + 2"), (("-2 + 5i", "-2 - 5i"), "x² + 4x + 29")]:
    B.mc(7, "cp1", f"Which quadratic has solutions {zs[0]} and {zs[1]}?", f"{poly} = 0", [f"{poly.replace('+ 9', '- 9').replace('- 2x', '+ 2x').replace('+ 4x', '- 4x')} = 0", f"{poly.replace('+ 2', '- 2').replace('+ 29', '+ 21').replace('+ 9', '+ 3')} = 0", "x² + 1 = 0" if "3i" not in zs[0] else "x² + 6 = 0"], ["(x - z)(x - z̄) = x² - 2Re(z)x + |z|²."])
    for z in zs: assert abs(peval(poly, x=complex(peval(z)))) < 1e-9
B.orq(7, "honors", "f(x) = x² - 6x + 13.", [("Find the vertex.", "(3, 4)"), ("Does the graph cross the x-axis? Why?", "No: the vertex is above the axis and it opens up"), ("Find the zeros.", "3 ± 2i"), ("Relate the vertex to the zeros.", "Real part 3 = vertex x; imaginary part 2 = √(k/a)")],
      ["h = 3, k = 9 - 18 + 13.", "Minimum value 4 > 0.", "(6 ± √(36 - 52))/2.", "x = h ± i√(k/a)."], tags=["connections", "challenge"])
B.orq(7, "cp1", "Solve 4x² + 25 = 0.", [("Isolate x².", "x² = -25/4"), ("Take square roots.", "x = ±√(-25/4)"), ("Write in terms of i.", "x = ±(5/2)i"), ("Check one solution.", "4(-25/4) + 25 = 0")], ["Subtract, divide.", "±.", "√(-1) = i.", "Substitute."])
B.mc(7, "cp2", "How many complex solutions does every quadratic equation have (counting repeats)?", "2", ["1", "0", "It depends on the discriminant"], ["Degree 2 → 2 solutions counting multiplicity."])
B.sa(7, "cp2", "Solve x² = -36.", "x = ±6i", ["√(-36) = 6i."])
B.sa(7, "cp1", "Solve x² + 2x + 10 = 0.", "x = -1 ± 3i", ["(-2 ± √(-36))/2."])
B.sa(7, "honors", "Solve x² + (1 - i)x - i = 0 by factoring.", "x = -1 or x = i", ["(x + 1)(x - i) = x² + (1 - i)x - i."], tags=["challenge"])
assert abs((-1) ** 2 + (1 - 1j) * -1 - 1j) < 1e-12 and abs(1j ** 2 + (1 - 1j) * 1j - 1j) < 1e-12

# ---- Skill 8: modeling ----
for v0, h0 in [(96, 0), (40, 5), (64, 80)]:
    tmax = F(v0, 32); hmax = -16 * tmax ** 2 + v0 * tmax + h0
    land = (v0 + (v0 * v0 + 64 * h0) ** .5) / 32
    B.orq(8, "cp1", f"A ball is thrown upward: h(t) = -16t² + {v0}t{'' if h0 == 0 else f' + {h0}'} (feet).", [("Find the initial height.", f"{h0} ft"), ("When does it reach maximum height?", f"t = {fr(tmax)} s"), ("Find the maximum height.", f"{fr(hmax)} ft"), ("When does it hit the ground (nearest hundredth)?", f"t ≈ {land:.2f} s")],
          ["h(0).", "-b/(2a).", "h at the vertex.", "Quadratic formula, positive root."], tags=["modeling"])
for P_, A_ in [(40, 96), (34, 60), (26, 40)]:
    disc = (P_ / 2) ** 2 - 4 * A_; w = (P_ / 2 - disc ** .5) / 2; l = P_ / 2 - w
    B.sa(8, "cp1", f"A rectangle has perimeter {P_} m and area {A_} m². Find its dimensions.", f"{w:g} m by {l:g} m", [f"l + w = {P_ // 2}, lw = {A_}.", f"w² - {P_ // 2}w + {A_} = 0."], tags=["modeling"])
    assert w * l == A_ and 2 * (w + l) == P_
B.mc(8, "cp1", "Revenue R(p) = p(200 - 4p) for price p dollars. What price maximizes revenue?", "$25", ["$50", "$200", "$12.50"], ["Zeros 0 and 50; vertex at p = 25."], tags=["modeling"])
B.mc(8, "cp1", "In h(t) = -4.9t² + 14.7t + 2, what does -4.9 represent?", "Half the acceleration due to gravity (m/s²)", ["Initial velocity", "Initial height", "Maximum height"], ["-½g with g = 9.8 m/s²."], tags=["modeling"])
B.sel(8, "cp1", "h(t) = -16t² + 32t + 48. Select ALL true statements.", ["The initial height is 48 ft", "The maximum height is 64 ft", "The object lands at t = 3 s"], ["The maximum is at t = 2 s", "The object lands at t = 1 s"], ["Vertex t = 1: h = 64.", "-16(t² - 2t - 3) = -16(t - 3)(t + 1)."], tags=["modeling"])
B.sel(8, "honors", "Select ALL situations that a quadratic model fits well.", ["Height of a thrown ball over time", "Area of a square vs. side length", "Revenue when each price increase loses customers"], ["A savings account with 4% interest", "Distance at a constant speed"], ["Quadratic: product of two linear quantities or constant acceleration."], tags=["modeling"])
B.orq(8, "honors", "A rectangular garden against a wall uses 60 ft of fencing on three sides.", [("Write the area in terms of the width x.", "A = x(60 - 2x)"), ("Find the width that maximizes area.", "15 ft"), ("Find the maximum area.", "450 ft²"), ("For what widths is the area at least 400 ft²?", "10 ≤ x ≤ 20")],
      ["Length 60 - 2x.", "Vertex 60/4.", "15·30.", "x(60 - 2x) ≥ 400 → x² - 30x + 200 ≤ 0."], tags=["modeling", "challenge"])
B.orq(8, "cp1", "The table shows (x, y): (0, 3), (1, 6), (2, 7), (3, 6), (4, 3).", [("Where is the vertex?", "(2, 7)"), ("Write the model in vertex form.", "y = -(x - 2)² + 7"), ("Predict y at x = 5.", "-2"), ("Find the zeros (nearest tenth).", f"{2 - 7 ** .5:.1f} and {2 + 7 ** .5:.1f}")],
      ["Symmetry of the outputs.", "Use (0, 3): 3 = 4a + 7 → a = -1.", "-(9) + 7.", "(x - 2)² = 7."], tags=["modeling", "multiple-representations"])
B.sa(8, "cp1", "The product of two consecutive positive even integers is 168. Find them.", "12 and 14", ["n(n + 2) = 168 → n² + 2n - 168 = 0 → (n + 14)(n - 12) = 0."])
B.sa(8, "honors", "A 10 in × 8 in photo has a uniform border; the total area is 120 in². Find the border width.", "1 in", ["(10 + 2x)(8 + 2x) = 120 → 4x² + 36x - 40 = 0 → x² + 9x - 10 = 0.", "x = 1 (positive root)."], tags=["modeling"])
assert (10 + 2) * (8 + 2) == 120
B.sa(8, "cp2", "A ball's height is h(t) = -16t² + 64. When does it hit the ground?", "t = 2 s", ["16t² = 64."])
B.sa(8, "cp2", "A square has area 81 cm². What is its side length?", "9 cm", ["√81; length is positive."])

B.sel(8, "cp2", "A square garden's side is increased by 2 m, giving area 64 m². Select ALL true statements.", ["The new side is 8 m", "The original side was 6 m", "The original area was 36 m²"], ["The original side was 8 m", "The area increased by 4 m²"], ["(s + 2)² = 64 → s + 2 = 8.", "64 - 36 = 28."], tags=["modeling"])

if __name__ == "__main__":
    p = B.write(); print(p, N0, "→", len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
