from lib import Bank, graph
from mathlite import *
from geofig import Fig, tri_from_sides, tri_from_angles
import math, random, itertools

STD = {1: ["G-CO.C.10"], 2: ["G-CO.C.10"], 3: ["G-CO.C.10"], 4: ["G-CO.C.9", "G-C.A.3"], 5: ["G-CO.C.10", "G-C.A.3"], 6: ["G-CO.C.10"], 7: ["G-CO.C.10"], 8: ["G-CO.C.10", "A-CED.A.1"]}
B = Bank("triangle-relationships", "tr", STD, course="geometry", prefix="geo")
R = random.Random(404)
LET = ["ABC", "DEF", "PQR", "XYZ", "JKL", "RST", "MNO", "GHI"]


def ang_fmt(v): return f"{fr(v)}°"


# ---------------- Skill 1: isosceles and equilateral ----------------
S = 1
for k_, vert in enumerate([40, 36, 100, 64, 120, 22, 90, 58]):
    base = F(180 - vert, 2); L = R.choice(LET)
    if k_ % 2 == 0:
        B.sa(S, "cp2" if k_ < 4 else "cp1", f"△{L} is isosceles with {L[1]}{L[0]} ≅ {L[1]}{L[2]}. The vertex angle ∠{L[1]} measures {vert}°. Find each base angle.", ang_fmt(base), ["Base angles are congruent.", f"(180 - {vert})/2 = {fr(base)}."])
    else:
        B.mc(S, "cp1", f"An isosceles triangle has a base angle of {fr(base)}°. Find the vertex angle.", f"{vert}°", [f"{fr(base)}°", f"{fr(180 - base)}°", f"{fr(180 - 2 * vert) if 180 - 2 * vert > 0 else fr(base / 2)}°"], ["Vertex = 180 - 2·base."], tags=["misconception"])
for e1, e2 in [("(3x + 10)°", "(5x - 20)°"), ("(2x + 25)°", "(4x - 5)°"), ("(x + 32)°", "(3x - 8)°"), ("(6x - 7)°", "(4x + 13)°")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]); b = p1(xv); assert 0 < b < 90
    B.orq(S, "cp1", f"In isosceles △ABC with AB ≅ AC, m∠B = {e1} and m∠C = {e2}.", [("Write an equation.", f"{e1.strip('()°')} = {e2.strip('()°')}"), ("Find x.", fr(xv)), ("Find the base angles.", ang_fmt(b)), ("Find m∠A.", ang_fmt(180 - 2 * b))],
          ["Base Angles Theorem.", "Solve.", "Substitute.", "Triangle sum."])
for e1, e2, e3 in [("4x - 2", "2x + 10", "x + 8"), ("5x + 1", "3x + 9", "7x - 11"), ("2x + 6", "x + 11", "4x - 4")]:
    p1, p2, p3 = linp(e1), linp(e2), linp(e3); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    vals = [p(xv) for p in (p1, p2, p3)]; eq = vals[0] == vals[1] == vals[2]
    B.sa(S, "cp1" if not eq else "honors", f"△PQR has PQ = {e1}, QR = {e2}, PR = {e3}, and PQ = QR. Find x and classify the triangle by sides.", f"x = {fr(xv)}; sides {', '.join(fr(v) for v in vals)}; {'equilateral' if eq else 'isosceles'}", ["Set PQ = QR.", "Substitute into all three."])
for k_ in range(3):
    vert = R.choice([30, 50, 70, 80]); b = (180 - vert) // 2
    A, Bv, C = tri_from_angles(vert, b); fg = Fig(3.6, 3.0); fg.poly([A, Bv, C]); fg.names([A, Bv, C], ["A", "B", "C"])
    fg.ticks(A, Bv, 1, size=0.3); fg.ticks(A, C, 1, size=0.3); fg.angle(A, Bv, C, f"{vert}°", r=0.55); fg.angle(Bv, C, A, "x°", r=0.55); fg.angle(C, A, Bv, "y°", r=0.55)
    dg = fg.save(B, f"s01-iso-{k_}", f"Isosceles triangle ABC with AB and AC marked congruent; vertex angle A = {vert}°, base angles labeled x at B and y at C.")
    B.sel(S, "cp1", "Use the figure. Select ALL true statements.", [f"x = {b}", f"y = {b}", "x = y"], [f"x = {vert}", f"x + y = {vert}", f"y = {180 - vert}"], ["Base angles are congruent and sum with the vertex to 180°."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "Each angle of an equilateral triangle measures…", "60°", ["45°", "90°", "it depends on the side length"], ["Equilateral ⇔ equiangular."])
B.sel(S, "honors", "Select ALL true statements.", ["Every equilateral triangle is isosceles", "If two angles of a triangle are congruent, the sides opposite them are congruent", "An isosceles right triangle has base angles of 45°"], ["Every isosceles triangle is acute", "The vertex angle of an isosceles triangle is always the largest angle"], ["Converse of Base Angles Theorem.", "An isosceles triangle can have a 20° vertex angle."], tags=["reasoning"])
B.orq(S, "honors", "Prove the Base Angles Theorem: in △ABC with AB ≅ AC, ∠B ≅ ∠C.", [("Construct an auxiliary segment.", "Draw AM to the midpoint M of BC"), ("Name the congruent triangles and shortcut.", "△ABM ≅ △ACM by SSS"), ("Conclude.", "∠B ≅ ∠C by CPCTC"), ("What extra fact about AM follows?", "AM ⊥ BC and AM bisects ∠A")], ["Midpoint.", "AB ≅ AC, BM ≅ CM, AM shared.", "CPCTC.", "Congruent linear pair angles are right; CPCTC for ∠A halves."], tags=["reasoning"])
B.sa(S, "cp2", "An equilateral triangle has perimeter 39 cm. Find each side.", "13 cm", ["39/3."])
B.sa(S, "honors", "The vertex angle of an isosceles triangle is 3 times a base angle. Find all angles.", "36°, 36°, 108°", ["b + b + 3b = 180."])

# ---------------- Skill 2: triangle inequality ----------------
S = 2
for k_ in range(9):
    a, b, c = sorted(R.sample(range(2, 20), 3)); ok = a + b > c
    if k_ % 3 == 0: c = a + b; ok = False
    B.mc(S, "cp2" if k_ < 4 else "cp1", f"Can {a}, {b}, and {c} be the side lengths of a triangle?", "Yes" if ok else "No", ["No" if ok else "Yes", "Only if it is a right triangle", "Only if it is isosceles"],
         [f"Check the two shorter sides: {a} + {b} = {a + b} {'>' if ok else '≤'} {c}."], tags=["misconception"] if a + b == c else ())
for a, b in [(5, 9), (12, 7), (3.5, 8), (10, 10), (21, 13)]:
    B.sa(S, "cp1", f"Two sides of a triangle are {a:g} and {b:g}. Write an inequality for the third side x.", f"{abs(a - b):g} < x < {a + b:g}", ["Difference < third side < sum."])
for a, b in [(6, 11), (9, 14), (4, 15)]:
    cands = [str(v) for v in range(abs(a - b) - 1, a + b + 2, 2)]
    sel_auto(B, S, "cp1", f"Two sides of a triangle are {a} and {b}. Select ALL possible lengths of the third side.", cands[:7], lambda s_, a=a, b=b: abs(a - b) < int(s_) < a + b, ["|a - b| < c < a + b."])
for a, b in [(7, 12), (5, 5), (8, 20)]:
    lo, hi = abs(a - b), a + b
    B.sa(S, "cp1", f"Two sides of a triangle are {a} and {b}. How many whole-number lengths are possible for the third side?", str(hi - lo - 1), [f"{lo} < x < {hi}: integers {lo + 1} through {hi - 1}."])
B.orq(S, "honors", "A triangle has sides x, x + 3, and 15.", [("Write the three inequalities.", "x + x + 3 > 15; x + 15 > x + 3; x + 3 + 15 > x"), ("Which inequality restricts x?", "2x + 3 > 15"), ("Solve it.", "x > 6"), ("Which other inequalities are always true?", "the other two (18 > 0, 15 > 3)")], ["All three sums.", "Only one is not automatic.", "x > 6.", "They hold for every positive x."], tags=["challenge"])
B.mc(S, "cp1", "A student says 4, 6, 10 can form a triangle because 4 + 6 = 10. What is correct?", "No: the sum must be greater than 10; the points would be collinear", ["Correct", "Yes: it is a right triangle", "No: 4 + 10 > 6 fails"], ["Strict inequality."], tags=["error-analysis"])
B.sa(S, "cp1", "Towns A and B are 30 km and 45 km from town C. What are the possible distances between A and B (if not collinear)?", "between 15 km and 75 km", ["|45 - 30| < AB < 45 + 30."], tags=["modeling"])
B.sa(S, "honors", "The sides of a triangle are 2x + 1, 3x - 2, and 10. Find all x that work.", "11/5 < x < 13", ["2x + 1 + 3x - 2 > 10 → x > 11/5.", "2x + 1 + 10 > 3x - 2 → x < 13; 3x - 2 + 10 > 2x + 1 → x > -7.", "Combine (sides are then positive): 11/5 < x < 13."], tags=["challenge"])

# ---------------- Skill 3: ordering sides and angles ----------------
S = 3
for k_ in range(8):
    while True:
        a, b, c = R.sample(range(4, 25), 3)
        if a + b > c and a + c > b and b + c > a: break
    L = R.choice(LET); sides = {L[1] + L[2]: a, L[0] + L[2]: b, L[0] + L[1]: c}  # side opposite L[0] is L[1]L[2]
    opp = {L[1] + L[2]: L[0], L[0] + L[2]: L[1], L[0] + L[1]: L[2]}
    order = sorted(sides, key=sides.get)
    angs = " < ".join(f"∠{opp[sd]}" for sd in order)
    if k_ % 2:
        B.mc(S, "cp1", f"In △{L}, {', '.join(f'{k} = {v}' for k, v in sides.items())}. Order the angles from smallest to largest.", angs, [" < ".join(f"∠{opp[sd]}" for sd in order[::-1]), " < ".join(f"∠{sd[0]}" for sd in order) if len({sd[0] for sd in order}) == 3 else f"∠{L[0]} < ∠{L[1]} < ∠{L[2]}" if f"∠{L[0]} < ∠{L[1]} < ∠{L[2]}" != angs else f"∠{L[2]} < ∠{L[0]} < ∠{L[1]}", " < ".join(f"∠{opp[sd]}" for sd in [order[1], order[0], order[2]])],
             ["The largest angle is opposite the longest side.", f"Opposite angles of {', '.join(order)}."], tags=["misconception"])
    else:
        B.sa(S, "cp1", f"In △{L}, {', '.join(f'{k} = {v}' for k, v in sides.items())}. Name the largest and the smallest angle.", f"largest ∠{opp[order[2]]}; smallest ∠{opp[order[0]]}", ["Largest angle opposite the longest side."])
for k_ in range(6):
    A_, B_ = R.randint(30, 80), R.randint(20, 80); C_ = 180 - A_ - B_
    if C_ <= 0 or len({A_, B_, C_}) < 3: continue
    L = R.choice(LET); m = {L[0]: A_, L[1]: B_, L[2]: C_}
    oppside = {L[0]: L[1] + L[2], L[1]: L[0] + L[2], L[2]: L[0] + L[1]}
    order = sorted(m, key=m.get); ans = " < ".join(oppside[v] for v in order)
    B.sa(S, "cp2" if k_ < 3 else "cp1", f"In △{L}, m∠{L[0]} = {A_}° and m∠{L[1]} = {B_}°. List the sides from shortest to longest.", ans, [f"m∠{L[2]} = {C_}°.", "Shortest side is opposite the smallest angle."])
dg = None
A, Bv, C = tri_from_angles(70, 45, 6); fg = Fig(3.8, 3.0); fg.poly([A, Bv, C]); fg.names([A, Bv, C], ["A", "B", "C"]); fg.angle(A, Bv, C, "70°", r=0.5); fg.angle(Bv, C, A, "45°", r=0.6)
dg = fg.save(B, "s03-order", "Triangle ABC with angle A = 70° and angle B = 45°; angle C is not labeled.")
B.sel(S, "cp1", "Use the figure. Select ALL true statements.", ["m∠C = 65°", "BC is the longest side", "AC is the shortest side"], ["AB is the longest side", "AC is the longest side", "m∠C = 75°"], ["Angles 70°, 45°, 65°; sides opposite: BC, AC, AB."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "In a right triangle, which side is longest?", "the hypotenuse", ["the shorter leg", "the longer leg", "it depends"], ["Opposite the largest (90°) angle."])
B.orq(S, "honors", "In △ABC, m∠A = (2x + 5)°, m∠B = (3x - 10)°, m∠C = (x + 35)°.", [("Find x.", "25"), ("Find the angle measures.", "55°, 65°, 60°"), ("Order the sides from shortest to longest.", "BC < AB < AC"), ("Which side is longest?", "AC")], ["6x + 30 = 180.", "Substitute.", "Opposite ∠A (BC), ∠C (AB), ∠B (AC).", "Opposite the largest angle."], tags=["multistep"])
B.sel(S, "honors", "In △PQR, PQ > QR > PR. Select ALL statements that must be true.", ["m∠R > m∠P", "∠R is the largest angle", "∠Q is the smallest angle"], ["∠P is the largest angle", "m∠Q > 60°"], ["Angles opposite: PQ→R, QR→P, PR→Q."], tags=["reasoning"])
B.mc(S, "cp1", "A student says the longest side of △ABC is opposite its smallest angle. What is correct?", "The longest side is opposite the largest angle", ["Correct", "The longest side is adjacent to the largest angle", "Side lengths are unrelated to angles"], ["Triangle side–angle relationship."], tags=["error-analysis"])

# ---------------- Skill 4: perpendicular and angle bisectors ----------------
S = 4
for e1, e2, what in [("3x + 4", "5x - 6", "PA and PB, where P is on the perpendicular bisector of AB"), ("2x + 9", "4x - 3", "the distances from P to the sides of ∠A, where P is on its bisector"), ("x + 12", "3x - 2", "DA and DB, where D is on the perpendicular bisector of AB"), ("6x - 5", "4x + 3", "the distances from Q to the two sides of an angle, where Q is on the angle bisector")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.sa(S, "cp1", f"The lengths {e1} and {e2} are {what}. Find x and the length.", f"x = {fr(xv)}; {fr(p1(xv))}", ["Points on a perpendicular bisector are equidistant from the endpoints; points on an angle bisector are equidistant from the sides.", f"x = {fr(xv)}."])
for q, a, w in [("The point where the perpendicular bisectors of a triangle meet is the…", "circumcenter", ["incenter", "centroid", "orthocenter"]), ("The point where the angle bisectors of a triangle meet is the…", "incenter", ["circumcenter", "centroid", "orthocenter"]),
                ("Which center is equidistant from the three vertices?", "circumcenter", ["incenter", "centroid", "orthocenter"]), ("Which center is equidistant from the three sides?", "incenter", ["circumcenter", "centroid", "orthocenter"]),
                ("Where is the circumcenter of a right triangle?", "at the midpoint of the hypotenuse", ["at the right-angle vertex", "inside the triangle", "outside the triangle"]), ("Where is the circumcenter of an obtuse triangle?", "outside the triangle", ["inside the triangle", "on the longest side", "at a vertex"])]:
    B.mc(S, "cp1" if "right" in q or "obtuse" in q else "cp2", q, a, w, ["Concurrency of bisectors."])
for (A_, B_, C_) in [((0, 0), (8, 0), (0, 6)), ((0, 0), (6, 0), (2, 4)), ((-2, 0), (4, 0), (0, 6))]:
    # circumcenter
    ax, ay = A_; bx, by = B_; cx, cy = C_
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = F((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by), d)
    uy = F((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax), d)
    r2 = (ux - ax) ** 2 + (uy - ay) ** 2; assert r2 == (ux - bx) ** 2 + (uy - by) ** 2 == (ux - cx) ** 2 + (uy - cy) ** 2
    B.orq(S, "honors" if A_ != (0, 0) or C_ != (0, 6) else "cp1", f"Find the circumcenter of the triangle with vertices {pt(*A_)}, {pt(*B_)}, {pt(*C_)}.", [("Find the perpendicular bisector of the side on the x-axis.", f"x = {fr(F(ax + bx, 2))}"), ("Find the circumcenter.", pt(ux, uy)), ("Find the circumradius.", rad(r2) if r2.denominator == 1 else f"√({fr(r2)})"), ("Verify it is equidistant from all three vertices.", f"each distance² = {fr(r2)}")],
          ["Midpoint of the horizontal side; vertical line.", "Intersect with the perpendicular bisector of a second side (midpoint, negative-reciprocal slope).", "Distance to any vertex.", "Distance formula to each vertex."], tags=["connections"])
B.sel(S, "cp1", "P lies on the perpendicular bisector of segment AB. Select ALL statements that must be true.", ["PA = PB", "P is equidistant from A and B"], ["P is the midpoint of AB", "PA = AB", "P lies on AB"], ["Perpendicular Bisector Theorem."])
B.sel(S, "honors", "Select ALL true statements about triangle centers.", ["The incenter is always inside the triangle", "The circumcenter can lie outside the triangle", "The incenter is the center of the inscribed circle"], ["The circumcenter is always inside", "The incenter is equidistant from the vertices"], ["Incenter: equidistant from sides, always inside."], tags=["reasoning"])
B.mc(S, "honors", "A city wants a fire station equidistant from three towns. Which point should it use?", "the circumcenter of the triangle formed by the towns", ["the incenter", "the centroid", "the midpoint of the longest side"], ["Equidistant from vertices."], tags=["modeling"])
B.sa(S, "cp2", "D is on the bisector of ∠ABC and is 7 cm from side BA. How far is D from side BC?", "7 cm", ["Angle Bisector Theorem."])

# ---------------- Skill 5: medians, altitudes, centers ----------------
S = 5
for med in [12, 18, 7.5, 27, 21]:
    B.mc(S, "cp1", f"G is the centroid of △ABC and median AD = {med:g}. Find AG and GD.", f"AG = {2 * med / 3:g}, GD = {med / 3:g}", [f"AG = {med / 2:g}, GD = {med / 2:g}", f"AG = {med / 3:g}, GD = {2 * med / 3:g}", f"AG = {med:g}, GD = {med / 2:g}"], ["The centroid is 2/3 of the way from a vertex to the midpoint of the opposite side."], tags=["misconception"])
for gd in [4, 6.5, 9]:
    B.sa(S, "cp2", f"G is the centroid and GD = {gd:g} on median AD. Find AG and AD.", f"AG = {2 * gd:g}; AD = {3 * gd:g}", ["AG = 2·GD; AD = 3·GD."])
for e1, e2 in [("3x + 1", "x + 5"), ("4x - 2", "x + 3"), ("5x", "2x + 3")]:
    p1, p2 = linp(e1), linp(e2); xv = (2 * p2.c[0] - p1.c[0]) / (p1.c[1] - 2 * p2.c[1])
    if p1(xv) <= 0: continue
    B.sa(S, "cp1", f"G is the centroid of △ABC on median BE. BG = {e1} and GE = {e2}. Find x and BE.", f"x = {fr(xv)}; BE = {fr(p1(xv) + p2(xv))}", ["BG = 2·GE.", f"{e1} = 2({e2}) → x = {fr(xv)}."])
    assert p1(xv) == 2 * p2(xv)
for V in [((0, 0), (6, 0), (3, 9)), ((-2, 1), (4, 5), (7, -3)), ((1, 2), (5, 8), (9, -1))]:
    gx, gy = F(sum(p[0] for p in V), 3), F(sum(p[1] for p in V), 3)
    B.mc(S, "cp1", f"Find the centroid of the triangle with vertices {', '.join(pt(*p) for p in V)}.", pt(gx, gy), [pt(F(sum(p[0] for p in V), 2), F(sum(p[1] for p in V), 2)), pt(sum(p[0] for p in V), sum(p[1] for p in V)), pt(gx + 1, gy)], ["Average the vertices."])
for q, a, w in [("A median connects a vertex to…", "the midpoint of the opposite side", ["the opposite side at a right angle", "the incenter", "the midpoint of an adjacent side"]), ("An altitude is…", "a perpendicular segment from a vertex to the line containing the opposite side", ["a segment to the midpoint of a side", "an angle bisector", "a perpendicular bisector of a side"]),
                ("The medians of a triangle meet at the…", "centroid", ["orthocenter", "circumcenter", "incenter"]), ("The altitudes of a triangle meet at the…", "orthocenter", ["centroid", "incenter", "circumcenter"]), ("Which point is the balance point of a triangular plate?", "centroid", ["orthocenter", "circumcenter", "incenter"])]:
    B.mc(S, "cp2", q, a, w, ["Definitions of segments and points of concurrency."])
A, Bv, C = (1.0, 4.0), (0.0, 0.0), (6.0, 0.0)
fg = Fig(4.0, 3.0); fg.poly([A, Bv, C]); fg.names([A, Bv, C], ["A", "B", "C"])
D = ((Bv[0] + C[0]) / 2, 0.0); E = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2); G = ((A[0] + Bv[0] + C[0]) / 3, (A[1] + Bv[1] + C[1]) / 3)
fg.seg(A, D, lw=1.1); fg.seg(Bv, E, lw=1.1); fg.dot(D, "D", (0, -11)); fg.dot(E, "E", (9, 6)); fg.dot(G, "G", (10, 4)); fg.ticks(Bv, D, 1, 0.3); fg.ticks(D, C, 1, 0.3); fg.ticks(A, E, 2, 0.3); fg.ticks(E, C, 2, 0.3)
dg = fg.save(B, "s05-medians", "Triangle ABC with medians AD and BE meeting at G; tick marks show D is the midpoint of BC and E is the midpoint of AC.")
B.orq(S, "cp1", "In the figure, AD = 15 and BG = 8.", [("Name point G.", "the centroid"), ("Find AG.", "10"), ("Find GE.", "4"), ("Find BE.", "12")], ["Medians meet at the centroid.", "2/3 of 15.", "BG = 2·GE.", "8 + 4."], diagram=dg, tags=["graph"])
B.mc(S, "honors", "In which triangle does the orthocenter lie at a vertex?", "a right triangle", ["an acute triangle", "an obtuse triangle", "an equilateral triangle"], ["The legs are altitudes, meeting at the right angle."], tags=["reasoning"])
B.sel(S, "honors", "In an equilateral triangle, select ALL points that coincide.", ["centroid", "circumcenter", "incenter", "orthocenter"], ["the midpoint of a side"], ["Every median is also an altitude, angle bisector, and perpendicular bisector."], tags=["reasoning"])
B.sa(S, "honors", "Find the orthocenter of the triangle with vertices (0, 0), (6, 0), (2, 4).", "(2, 2)", ["Altitude from C: x = 2.", "Altitude from A ⊥ BC (slope -1): y = x.", "Intersection (2, 2)."], tags=["challenge"])

# ---------------- Skill 6: midsegments ----------------
S = 6
for k_, (base, mid_expr) in enumerate([("22", None), ("4x + 6", "x + 9"), ("3x - 1", "x + 4"), ("18.4", None), ("6x - 8", "2x + 3"), ("5x + 2", "3x - 2")]):
    if mid_expr is None:
        v = F(base)
        B.mc(S, "cp2", f"DE is a midsegment of △ABC parallel to BC, and BC = {base}. Find DE.", fr(v / 2), [fr(v * 2), fr(v), fr(v / 3)], ["Midsegment = half the third side."], tags=["misconception"])
    else:
        p1, p2 = linp(base), linp(mid_expr); xv = (2 * p2.c[0] - p1.c[0]) / (p1.c[1] - 2 * p2.c[1])
        if p1(xv) <= 0 or p2(xv) <= 0: continue
        B.sa(S, "cp1", f"DE is the midsegment parallel to BC in △ABC. BC = {base} and DE = {mid_expr}. Find x, BC, and DE.", f"x = {fr(xv)}; BC = {fr(p1(xv))}; DE = {fr(p2(xv))}", ["BC = 2·DE.", f"x = {fr(xv)}."])
        assert p1(xv) == 2 * p2(xv)
for V in [((0, 0), (8, 0), (2, 6)), ((-4, 2), (6, 4), (0, -6)), ((1, 1), (9, 3), (3, 7))]:
    (ax, ay), (bx, by), (cx, cy) = V
    D = (F(ax + bx, 2), F(ay + by, 2)); E = (F(ax + cx, 2), F(ay + cy, 2))
    sDE = (E[1] - D[1]) / (E[0] - D[0]) if E[0] != D[0] else None; sBC = F(cy - by, cx - bx) if cx != bx else None
    lenDE2 = (E[0] - D[0]) ** 2 + (E[1] - D[1]) ** 2; lenBC2 = (cx - bx) ** 2 + (cy - by) ** 2; assert lenBC2 == 4 * lenDE2 and sDE == sBC
    B.orq(S, "cp1", f"△ABC has A{pt(ax, ay)}, B{pt(bx, by)}, C{pt(cx, cy)}. D and E are midpoints of AB and AC.", [("Find D and E.", f"{pt(*D)} and {pt(*E)}"), ("Compare the slopes of DE and BC.", f"both {fr(sBC)}"), ("Compare DE and BC.", f"DE = {rad(lenDE2) if lenDE2.denominator == 1 else fr(lenDE2)}, BC = {rad(lenBC2)}: DE = ½BC"), ("What theorem does this verify?", "Triangle Midsegment Theorem")],
          ["Midpoint formula.", "Equal slopes → parallel.", "Distance formula.", "Midsegment is parallel to and half the third side."], tags=["connections"])
for P_ in [(10, 14, 18), (7, 9, 12), (24, 30, 36)]:
    B.sa(S, "cp1", f"A triangle has sides {P_[0]}, {P_[1]}, {P_[2]}. Find the perimeter of the triangle formed by its three midsegments.", fr(F(sum(P_), 2)), ["Each midsegment is half a side.", f"½·{sum(P_)}."])
B.sel(S, "cp1", "DE joins the midpoints of AB and AC in △ABC. Select ALL true statements.", ["DE ∥ BC", "DE = ½BC", "△ADE ~ △ABC"], ["DE ⊥ BC", "DE = BC", "D is the midpoint of BC"], ["Triangle Midsegment Theorem."])
B.mc(S, "honors", "In △ABC, DE ∥ BC with D on AB and DE = ½BC. Must D be the midpoint of AB?", "Yes: a line parallel to BC with half its length must cut AB at its midpoint", ["No", "Only if △ABC is isosceles", "Only if DE ⊥ AB"], ["△ADE ~ △ABC with scale ½, so AD = ½AB."], tags=["reasoning"])
B.sa(S, "cp2", "A midsegment of a triangle is 9 cm. How long is the parallel side?", "18 cm", ["Double."])
B.sa(S, "honors", "Midsegment DE ∥ BC has endpoints D(1, 3) and E(5, 5). B is (-1, 1). Find C.", "(7, 5)", ["D is the midpoint of AB → A = (3, 5).", "E is the midpoint of AC → C = (7, 5).", "Check BC = (8, 4) = 2·DE."], tags=["challenge"])

# ---------------- Skill 7: indirect proof and hinge ----------------
S = 7
for st, assume in [("A triangle has at most one obtuse angle.", "Assume a triangle has two obtuse angles."), ("If 3x + 5 ≠ 20, then x ≠ 5.", "Assume x = 5."), ("√2 is irrational.", "Assume √2 = a/b in lowest terms."), ("A triangle cannot have two right angles.", "Assume a triangle has two right angles."), ("If n² is even, then n is even.", "Assume n² is even and n is odd.")]:
    B.mc(S, "cp1", f"To prove '{st}' indirectly, what is the first step?", assume, ["Assume the hypothesis is false.", "Prove the converse.", "Give one example."] if "If" not in st else ["Assume the conclusion is true.", "Assume the hypothesis is false.", "Check one example."], ["Indirect proof: assume the conclusion is false and reach a contradiction."], tags=["reasoning"])
for (a1, b1, g1), (a2, b2, g2) in [((8, 10, 70), (8, 10, 55)), ((5, 7, 100), (5, 7, 120)), ((12, 12, 40), (12, 12, 41))]:
    longer = "first" if g1 > g2 else "second"
    B.mc(S, "cp1", f"Two triangles have sides {a1} and {b1} with included angles {g1}° and {g2}°. Which triangle has the longer third side?", f"the {longer} triangle", [f"the {'second' if longer == 'first' else 'first'} triangle", "they are equal", "cannot be determined"], ["Hinge Theorem: larger included angle → longer opposite side."])
    t1 = math.sqrt(a1 ** 2 + b1 ** 2 - 2 * a1 * b1 * math.cos(math.radians(g1))); t2 = math.sqrt(a2 ** 2 + b2 ** 2 - 2 * a2 * b2 * math.cos(math.radians(g2))); assert (t1 > t2) == (longer == "first")
for (s1, s2) in [((9, 9, 13), (9, 9, 11)), ((6, 8, 9), (6, 8, 12))]:
    big = "first" if s1[2] > s2[2] else "second"
    B.mc(S, "cp1", f"Two triangles have two pairs of congruent sides ({s1[0]}, {s1[1]}). Their third sides are {s1[2]} and {s2[2]}. Which triangle has the larger angle between the congruent sides?", f"the {big} triangle", [f"the {'second' if big == 'first' else 'first'} triangle", "they are equal", "cannot be determined"], ["Converse of the Hinge Theorem."])
for e_, rhs, opp in [("(3x + 10)°", 70, "<"), ("(2x - 6)°", 54, ">")]:
    p1 = linp(e_); xv = (rhs - p1.c[0]) / p1.c[1]
    B.sa(S, "honors", f"Triangles share two congruent sides. In the first, the included angle is {e_} and the third side is shorter than in the second, whose included angle is {rhs}°. Find the possible values of x.", f"{fr(-p1.c[0] / p1.c[1]) if -p1.c[0] / p1.c[1] > 0 else 0} < x < {fr(xv)}", [f"Converse of Hinge: {e_.strip('°')} < {rhs}.", f"Also the angle is positive: {e_.strip('°')} > 0."], tags=["challenge"])
B.orq(S, "honors", "Use indirect proof: In △ABC, if m∠A > m∠B, then BC > AC.", [("State the assumption.", "Assume BC ≤ AC"), ("Case BC = AC.", "Then △ABC is isosceles and m∠A = m∠B, contradiction"), ("Case BC < AC.", "Then m∠A < m∠B (larger side opposite larger angle), contradiction"), ("Conclude.", "BC > AC")], ["Negate the conclusion.", "Base Angles Theorem.", "Side–angle relationship.", "Both cases contradict the hypothesis."], tags=["reasoning"])
B.sel(S, "cp1", "Select ALL valid contradictions an indirect proof might reach.", ["an angle sum greater than 180° in a triangle", "a number that is both even and odd", "a statement that contradicts the given"], ["a true statement that agrees with the given", "an example that fits the assumption"], ["A contradiction is an impossible statement."], tags=["reasoning"])
B.mc(S, "cp2", "In an indirect proof you assume…", "the opposite of what you want to prove", ["what you want to prove", "the converse", "nothing"], ["Proof by contradiction."])
B.sa(S, "cp1", "Two friends open a pair of compasses with the same arm lengths: 30° and 50°. Which has the wider spread between the tips?", "the 50° opening", ["Hinge Theorem."], tags=["modeling"])

# ---------------- Skill 8: algebraic applications ----------------
S = 8
apps = [("In isosceles △ABC with AB = AC, AB = 4x - 3, AC = 2x + 9, BC = x + 5. Find the perimeter.", "4x - 3 = 2x + 9 → x = 6; sides 21, 21, 11", "53"),
        ("The perpendicular bisector of AB passes through P. PA = 7x - 4 and PB = 3x + 16. Find PA.", "7x - 4 = 3x + 16 → x = 5", "31"),
        ("G is the centroid; AG = 5x - 1 and GD = 2x + 1 on median AD. Find AD.", "5x - 1 = 2(2x + 1) → x = 3", "21"),
        ("A midsegment is 3x + 2 and the parallel side is 8x - 6. Find the midsegment.", "8x - 6 = 2(3x + 2) → x = 5", "17"),
        ("An exterior angle of an isosceles triangle at the vertex angle measures (5x + 10)°, and each base angle is (2x + 9)°. Find x.", "5x + 10 = 2(2x + 9) → x = 8", "8"),
        ("The angles of a triangle are (x + 10)°, (2x)°, and (3x - 10)°. Which side is longest?", "6x = 180 → x = 30; angles 40°, 60°, 80°", "the side opposite the 80° angle"),
        ("Two sides of a triangle are x + 2 and 2x - 1 and the third is 10. For which integer x is the triangle isosceles with base 10?", "x + 2 = 2x - 1 → x = 3, giving sides 5, 5, 10", "no such triangle (5 + 5 = 10)"),
        ("Point D on the bisector of ∠ABC is (2x + 1) cm from BA and (x + 6) cm from BC. Find the distance.", "2x + 1 = x + 6 → x = 5", "11 cm")]
for k_, (q, w, a) in enumerate(apps):
    B.sa(S, "cp1" if k_ < 5 else "honors", q, a, [w, "Check the result makes geometric sense." if k_ == 6 else "Substitute to find the requested value."], tags=["reasoning"] if k_ == 6 else ())
assert 4 * 6 - 3 == 2 * 6 + 9 and 7 * 5 - 4 == 3 * 5 + 16 and 5 * 3 - 1 == 2 * (2 * 3 + 1) and 8 * 5 - 6 == 2 * (3 * 5 + 2) and 5 * 8 + 10 == 2 * (2 * 8 + 9)
for k_ in range(6):
    x = R.randint(3, 12); c1, c2 = R.sample([2, 3, 4, 5, 6, 7], 2); k1 = R.randint(1, 15); val = c1 * x + k1; k2 = val - c2 * x
    e1 = f"{c1}x + {k1}"; e2 = f"{c2}x {'+' if k2 >= 0 else '-'} {abs(k2)}"
    ctx = R.choice(["the legs of an isosceles triangle", "the distances from a point on a perpendicular bisector to the segment's endpoints", "two sides of an equilateral triangle"])
    B.mc(S, "cp1", f"{e1} and {e2} are {ctx}. Find x.", f"x = {x}", [f"x = {x + 1}", f"x = {x - 1}", f"x = {val}"], [f"Set them equal: x = {x}."])
    assert linp(e1)(x) == linp(e2)(x)
B.sel(S, "honors", "In △ABC, AB = 3x, BC = x + 8, AC = 2x + 2, and x = 5. Select ALL true statements.", ["AB = 15 and BC = 13 and AC = 12", "∠C is the largest angle", "∠B is the smallest angle", "the triangle is valid"], ["∠A is the largest angle", "the triangle is isosceles"], ["Sides 15, 13, 12: largest angle opposite AB (∠C), smallest opposite AC (∠B)."])
B.orq(S, "honors", "△ABC has vertices A(0, 0), B(10, 0), C(4, 6).", [("Find the centroid.", "(14/3, 2)"), ("Find the midpoint of AB.", "(5, 0)"), ("Find the length of median from C.", "√37"), ("Find the distance from C to the centroid.", "(2/3)√37")], ["Average.", "Midpoint.", "√(1 + 36).", "2/3 of the median."], tags=["connections"])
B.orq(S, "cp1", "In △PQR, PQ = 2x + 3, QR = 3x - 1, PR = 4x - 9, and the perimeter is 47.", [("Find x.", "6"), ("Find the side lengths.", "15, 17, 15"), ("Classify by sides.", "isosceles"), ("Which angles are congruent?", "∠R and ∠Q (opposite the equal sides PQ and PR)")], ["9x - 7 = 47.", "Substitute.", "Two equal sides.", "Opposite angles."], tags=["multistep"])
assert 9 * 6 - 7 == 47

# ================= fill to target with randomized makers =================
from fill import fill
RF = random.Random(4044)
def lv(): return RF.choice(["cp2", "cp1", "cp1", "honors"])
def mk_iso_sa():
    vert = RF.randint(10, 160); b = F(180 - vert, 2); L = RF.choice(LET)
    if RF.random() < 0.5:
        B.sa(1, "cp2", f"Isosceles △{L} has vertex angle ∠{L[0]} = {vert}°. Find m∠{L[1]}.", ang_fmt(b), ["Base angles are congruent.", f"(180 - {vert})/2."])
    else:
        B.sa(1, "cp1", f"One base angle of an isosceles triangle measures {fr(b)}°. Find the other two angles.", f"{fr(b)}° and {vert}°", ["The other base angle is congruent; vertex = 180 - 2·base."])
def mk_iso_sel():
    b = RF.randint(20, 85); vert = 180 - 2 * b
    st = {f"The other base angle is {b}°": True, f"The vertex angle is {vert}°": True, "The triangle is acute" if max(b, vert) < 90 else ("The triangle is obtuse" if vert > 90 else "The triangle is right"): True,
          f"The vertex angle is {b}°": vert == b, f"The vertex angle is {180 - b}°": False}
    B.sel(1, lv(), f"An isosceles triangle has a base angle of {b}°. Select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Base angles congruent; angles sum to 180°."])
def mk_ineq():
    a, b = RF.randint(3, 20), RF.randint(3, 20); lo, hi = abs(a - b), a + b
    if RF.random() < 0.5:
        c = RF.choice([lo, hi, RF.randint(lo + 1, hi - 1) if hi - lo > 1 else hi, hi + RF.randint(1, 4)])
        ok = lo < c < hi
        B.mc(2, lv(), f"Is a triangle possible with sides {a}, {b}, and {c}?", "Yes" if ok else "No", ["No" if ok else "Yes", "Only if it is a right triangle", "Only if two sides are equal"], [f"Need {lo} < {c} < {hi}."])
    else:
        cands = sorted(set([lo, lo + 1, (lo + hi) // 2, hi - 1, hi, hi + 2]))
        if len([c for c in cands if lo < c < hi]) < 2: raise AssertionError
        sel_auto(B, 2, lv(), f"Two sides of a triangle measure {a} and {b}. Select ALL possible whole-number lengths of the third side.", [str(c) for c in cands], lambda s_: lo < int(s_) < hi, [f"{lo} < x < {hi}."])
def mk_order():
    while True:
        a_, b_ = RF.randint(20, 100), RF.randint(20, 100); c_ = 180 - a_ - b_
        if c_ > 0 and len({a_, b_, c_}) == 3: break
    L = RF.choice(LET); m = dict(zip(L, (a_, b_, c_))); opp = {L[0]: L[1] + L[2], L[1]: L[0] + L[2], L[2]: L[0] + L[1]}
    order = sorted(m, key=m.get)
    if RF.random() < 0.5:
        B.mc(3, lv(), f"In △{L}, m∠{L[0]} = {a_}° and m∠{L[1]} = {b_}°. Which side is longest?", opp[order[2]], [opp[v] for v in order[:2]] + ["all sides are equal"], [f"m∠{L[2]} = {c_}°.", "Longest side opposite the largest angle."])
    else:
        st = {f"{opp[order[2]]} is the longest side": True, f"{opp[order[0]]} is the shortest side": True, f"m∠{L[2]} = {c_}°": True, f"{opp[order[0]]} is the longest side": False, f"m∠{L[2]} = {180 - c_}°": False}
        B.sel(3, lv(), f"In △{L}, m∠{L[0]} = {a_}° and m∠{L[1]} = {b_}°. Select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Find the third angle; match sides to opposite angles."])
def mk_bis():
    x = RF.randint(2, 15); c1, c2 = RF.sample(range(2, 9), 2); k1 = RF.randint(1, 20); v = c1 * x + k1; k2 = v - c2 * x
    e1, e2 = f"{c1}x + {k1}", f"{c2}x {'+' if k2 >= 0 else '-'} {abs(k2)}"
    kind = RF.choice(["perp", "ang"])
    q = f"P is on the perpendicular bisector of AB with PA = {e1} and PB = {e2}." if kind == "perp" else f"P is on the bisector of ∠ABC and is {e1} units from BA and {e2} units from BC."
    if RF.random() < 0.5:
        B.sa(4, lv(), q + " Find x and the distance.", f"x = {x}; {v}", ["Equidistance property.", f"x = {x}."])
    else:
        B.orq(4, lv(), q, [("Which property applies?", "Perpendicular Bisector Theorem" if kind == "perp" else "Angle Bisector Theorem"), ("Write an equation.", f"{e1} = {e2}"), ("Solve for x.", f"x = {x}"), ("Find the distance.", str(v))], ["Points on the bisector are equidistant.", "Set equal.", "Solve.", "Substitute."])
def mk_centroid():
    gd = RF.choice([2, 3, 4, 5, 6, 7, 8, 9, 2.5, 3.5, 4.5]); L = RF.choice(["ABC", "PQR", "JKL"])
    kind = RF.choice(["AG", "GD", "AD"])
    given = {"AG": 2 * gd, "GD": gd, "AD": 3 * gd}
    ask = [k for k in ("AG", "GD", "AD") if k != kind]
    B.mc(5, lv(), f"G is the centroid of △ABC and AD is a median. If {kind} = {given[kind]:g}, find {ask[0]} and {ask[1]}.", f"{ask[0]} = {given[ask[0]]:g}, {ask[1]} = {given[ask[1]]:g}", [f"{ask[0]} = {given[ask[0]] / 2:g}, {ask[1]} = {given[ask[1]] / 2:g}", f"{ask[0]} = {given[ask[1]]:g}, {ask[1]} = {given[ask[0]]:g}", f"{ask[0]} = {given[kind]:g}, {ask[1]} = {given[kind]:g}"],
         ["AG : GD : AD = 2 : 1 : 3."], tags=["misconception"])
def mk_centroid_coord():
    V = [(RF.randint(-6, 9), RF.randint(-6, 9)) for _ in range(3)]
    if (V[1][0] - V[0][0]) * (V[2][1] - V[0][1]) == (V[2][0] - V[0][0]) * (V[1][1] - V[0][1]): raise AssertionError
    g = (F(sum(p[0] for p in V), 3), F(sum(p[1] for p in V), 3))
    B.sa(5, lv(), f"Find the centroid of the triangle with vertices {', '.join(pt(*p) for p in V)}.", pt(*g), ["Average the x- and y-coordinates."])
def mk_mid():
    v = RF.randint(4, 40)
    if RF.random() < 0.5:
        B.mc(6, lv(), f"DE is a midsegment of △ABC parallel to BC. If DE = {v}, find BC.", str(2 * v), [str(v // 2) if v % 2 == 0 else f"{v / 2:g}", str(v), str(3 * v)], ["BC = 2·DE."], tags=["misconception"])
    else:
        a, b, c = sorted(RF.sample(range(6, 40, 2), 3))
        if a + b <= c: raise AssertionError
        st = {f"The midsegment parallel to the {a}-side is {a // 2}": True, f"The midsegment triangle has perimeter {(a + b + c) // 2}": True, f"The midsegment parallel to the {c}-side is {c}": False, f"The midsegment triangle has perimeter {a + b + c}": False, f"The midsegment parallel to the {b}-side is {b // 2}": True}
        B.sel(6, lv(), f"A triangle has sides {a}, {b}, {c}. Select ALL true statements about its midsegments.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Each midsegment is half the parallel side."])
def mk_mid_coord():
    A_ = (RF.randint(-6, 6), RF.randint(-6, 6)); B_ = (RF.randint(-6, 6), RF.randint(-6, 6)); C_ = (RF.randint(-6, 6), RF.randint(-6, 6))
    if (B_[0] - A_[0]) * (C_[1] - A_[1]) == (C_[0] - A_[0]) * (B_[1] - A_[1]): raise AssertionError
    D = (F(A_[0] + B_[0], 2), F(A_[1] + B_[1], 2)); E = (F(A_[0] + C_[0], 2), F(A_[1] + C_[1], 2))
    B.orq(6, lv(), f"A{pt(*A_)}, B{pt(*B_)}, C{pt(*C_)}. D and E are the midpoints of AB and AC.", [("Find D.", pt(*D)), ("Find E.", pt(*E)), ("Find the slope of DE and of BC.", "undefined (both vertical)" if B_[0] == C_[0] else f"{fr(F(C_[1] - B_[1], C_[0] - B_[0]))} (both)"), ("How does DE compare with BC?", "DE ∥ BC and DE = ½BC")], ["Midpoint formula.", "Midpoint formula.", "Equal slopes.", "Midsegment Theorem."])
def mk_hinge():
    a, b = RF.randint(4, 15), RF.randint(4, 15); g1, g2 = RF.sample(range(20, 160, 5), 2)
    longer = "first" if g1 > g2 else "second"
    B.mc(7, lv(), f"△1 and △2 each have sides {a} and {b}. The included angles are {g1}° (△1) and {g2}° (△2). Which triangle has the longer third side?", f"△{1 if longer == 'first' else 2}", [f"△{2 if longer == 'first' else 1}", "they are equal", "cannot be determined"], ["Hinge Theorem."])
def mk_indirect():
    st = RF.choice([("an integer n is even if n² is even", "n is odd"), ("a triangle has at most one right angle", "a triangle has two right angles"), ("the shortest distance from a point to a line is the perpendicular segment", "a nonperpendicular segment is shorter"),
                    ("if x² ≠ 25 then x ≠ 5", "x = 5"), ("two lines perpendicular to the same line in a plane are parallel", "the two lines intersect"), ("a scalene triangle has no two congruent angles", "a scalene triangle has two congruent angles")])
    B.sa(7, lv(), f"Write the assumption for an indirect proof that {st[0]}.", f"Assume {st[1]}.", ["Assume the conclusion is false."], tags=["reasoning"])
def mk_alg():
    x = RF.randint(3, 15); kind = RF.choice(["iso", "med", "mid", "perp"])
    c1, c2 = RF.sample(range(2, 8), 2)
    if kind == "med":
        k2 = RF.randint(1, 10); ge = c2 * x + k2; ag = 2 * ge; k1 = ag - c1 * x
        e1, e2 = f"{c1}x {'+' if k1 >= 0 else '-'} {abs(k1)}", f"{c2}x + {k2}"
        B.sa(8, lv(), f"G is the centroid; AG = {e1} and GD = {e2} on median AD. Find AD.", str(3 * ge), ["AG = 2·GD.", f"x = {x}."]); assert linp(e1)(x) == 2 * linp(e2)(x)
    elif kind == "mid":
        k2 = RF.randint(1, 10); de = c2 * x + k2; bc = 2 * de; k1 = bc - c1 * x
        e1, e2 = f"{c1}x {'+' if k1 >= 0 else '-'} {abs(k1)}", f"{c2}x + {k2}"
        B.sa(8, lv(), f"Midsegment DE = {e2} is parallel to BC = {e1}. Find BC.", str(bc), ["BC = 2·DE.", f"x = {x}."]); assert linp(e1)(x) == 2 * linp(e2)(x)
    else:
        k1 = RF.randint(1, 20); v = c1 * x + k1; k2 = v - c2 * x
        e1, e2 = f"{c1}x + {k1}", f"{c2}x {'+' if k2 >= 0 else '-'} {abs(k2)}"
        ctx = "the legs of an isosceles triangle" if kind == "iso" else "PA and PB for a point P on the perpendicular bisector of AB"
        B.mc(8, lv(), f"{e1} and {e2} are {ctx}. Find the common length.", str(v), [str(x), str(v + c1), str(2 * v)], ["Set equal and solve.", f"x = {x}."])
for S_, makers in [(1, [mk_iso_sa, mk_iso_sel]), (2, [mk_ineq]), (3, [mk_order]), (4, [mk_bis]), (5, [mk_centroid, mk_centroid_coord]), (6, [mk_mid, mk_mid_coord]), (7, [mk_hinge, mk_indirect]), (8, [mk_alg])]:
    fill(B, S_, 32, makers, RF)

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
