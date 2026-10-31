from lib import Bank
from mathlite import *
from geofig import Fig, tri_from_sides, tri_from_angles
import math, random, itertools

STD = {1: ["G-CO.C.10"], 2: ["G-CO.C.10"], 3: ["G-CO.B.7"], 4: ["G-CO.B.6", "G-CO.B.7"], 5: ["G-CO.B.8", "G-SRT.B.5"], 6: ["G-CO.B.8", "G-SRT.B.5"], 7: ["G-SRT.B.5"], 8: ["G-CO.B.7", "G-SRT.B.5"], 9: ["G-CO.C.10", "G-SRT.B.5"]}
B = Bank("triangle-congruence", "tc", STD, course="geometry", prefix="geo")
R = random.Random(303)
SIDES = {"AB": ("A", "B"), "BC": ("B", "C"), "CA": ("C", "A")}
INCL = {"A": ("AB", "CA"), "B": ("AB", "BC"), "C": ("BC", "CA")}


def criterion(sides, angles, right=None):
    """Congruence criterion implied by marked pairs (sides ⊂ {AB, BC, CA}, angles ⊂ {A, B, C})."""
    s, a = set(sides), set(angles) | ({right} if right else set())
    if right and len(s) >= 2:
        hyp = {"A": "BC", "B": "CA", "C": "AB"}[right]
        if hyp in s and len(s) == 2 and a == {right}: return "HL"
    if len(s) == 3: return "SSS"
    if len(s) == 2:
        for v, (s1, s2) in INCL.items():
            if {s1, s2} == s and v in a: return "SAS"
        if len(a) >= 2: return "SAS"  # two angles fix the third; included angle known
        if right and right in a: return "HL"
        return "SSA (not valid)"
    if len(s) == 1 and len(a) >= 2:
        sd = next(iter(s))
        if set(SIDES[sd]) <= a: return "ASA"
        return "AAS"
    if len(a) >= 2 and not s: return "AAA (not valid)"
    return "not enough information"


def pair_fig(name, sides, angles, right=None, shape=(5.0, 4.2, 3.4), flip=True, labels=("ABC", "DEF")):
    a, b, c = shape
    A, Bv, C = tri_from_sides(a, b, c)
    fg = Fig(5.6, 2.8)
    T1 = [A, Bv, C]
    off = 7.5
    T2 = [((-p[0] + a + off) if flip else p[0] + off, p[1]) for p in T1]
    for T, lab in ((T1, labels[0]), (T2, labels[1])):
        fg.poly(T); fg.names(T, list(lab))
        P_ = dict(zip("ABC", T))
        for k_, sd in enumerate(sorted(sides)):
            fg.ticks(P_[SIDES[sd][0]], P_[SIDES[sd][1]], n=k_ + 1, size=0.32)
        for k_, v in enumerate(sorted(angles)):
            o = [x for x in "ABC" if x != v]
            fg.angle(P_[v], P_[o[0]], P_[o[1]], None, n=k_ + 1, right=(v == right), r=0.45)
        if right and right not in angles:
            o = [x for x in "ABC" if x != right]; fg.angle(P_[right], P_[o[0]], P_[o[1]], right=True, r=0.45)
    corr = ", ".join(f"{labels[0][i]}↔{labels[1][i]}" for i in range(3))
    alt = f"Two triangles {labels[0]} and {labels[1]} ({corr}). Matching tick marks on " + (", ".join(f"{x} and the matching side" for x in sorted(sides)) or "no sides") + "; matching arcs at " + (", ".join(sorted(angles)) or "no angles") + (f"; right angles at {right} and its match" if right else "") + "."
    return fg.save(B, name, alt, schematic=True)


# ---------------- Skill 1: classifying triangles ----------------
S = 1
for a, b, c in [(5, 5, 5), (7, 7, 10), (6, 8, 11), (9, 12, 15), (4, 4, 4 * 2 ** .5), (10, 10, 17)]:
    s_kind = "equilateral" if a == b == c else ("isosceles" if len({a, b, round(c, 6)}) == 2 else "scalene")
    big = max(a, b, c); others = sorted([a, b, c])[:2]
    v = others[0] ** 2 + others[1] ** 2 - big ** 2
    a_kind = "right" if abs(v) < 1e-9 else ("acute" if v > 0 else "obtuse")
    ct = f"{c:g}" if c == int(c) else "4√2"
    B.mc(S, "cp1" if a_kind != "right" else "cp2", f"Classify a triangle with sides {a}, {b}, and {ct} by sides and by angles.", f"{s_kind}, {a_kind}", [f"{s_kind}, {'acute' if a_kind != 'acute' else 'obtuse'}", f"{'scalene' if s_kind != 'scalene' else 'isosceles'}, {a_kind}", f"{'isosceles' if s_kind == 'equilateral' else 'equilateral'}, {'right' if a_kind != 'right' else 'acute'}"],
         ["Compare side lengths for the side classification.", "Compare a² + b² with c² (c longest): =, >, < → right, acute, obtuse."])
for angs in [(60, 60, 60), (90, 45, 45), (110, 35, 35), (50, 60, 70), (30, 60, 90), (100, 50, 30)]:
    a_kind = "right" if 90 in angs else ("obtuse" if max(angs) > 90 else "acute")
    s_kind = "equilateral" if len(set(angs)) == 1 else ("isosceles" if len(set(angs)) == 2 else "scalene")
    B.sa(S, "cp2", f"A triangle has angles {angs[0]}°, {angs[1]}°, {angs[2]}°. Classify it by angles and by sides.", f"{a_kind}, {s_kind}", ["Largest angle decides acute/right/obtuse.", "Equal angles are opposite equal sides."])
for i, (a, b, c) in enumerate([(6, 6, 6), (5, 5, 8), (4, 6, 7.5)]):
    A, Bv, C = tri_from_sides(a, b, c); fg = Fig(3.6, 3.0); fg.poly([A, Bv, C]); fg.names([A, Bv, C], ["A", "B", "C"])
    if a == b == c:
        for P_, Q_ in ((A, Bv), (Bv, C), (C, A)): fg.ticks(P_, Q_, 1)
    elif a == b:
        fg.ticks(Bv, C, 1); fg.ticks(C, A, 1)
    dg = fg.save(B, f"s01-classify-{i}", "Triangle ABC with " + ("all three sides marked congruent." if a == b == c else ("sides BC and CA marked congruent." if a == b else "no congruence marks.")))
    kind = "equilateral" if a == b == c else ("isosceles" if a == b else "scalene")
    B.mc(S, "cp2", "Classify the triangle by its sides using the tick marks.", kind, [k for k in ["equilateral", "isosceles", "scalene", "right"] if k != kind][:3], ["Count congruent sides from the tick marks."], diagram=dg, tags=["graph"])
B.sel(S, "cp1", "Select ALL statements that are always true.", ["An equilateral triangle is isosceles", "An equilateral triangle is acute", "A right triangle has exactly one right angle"], ["An isosceles triangle is equilateral", "A scalene triangle cannot be right", "An obtuse triangle can have two obtuse angles"], ["Isosceles: at least two congruent sides.", "Angle sum 180° limits obtuse/right angles to one."], tags=["reasoning"])
B.sel(S, "honors", "Select ALL triangles that are obtuse.", ["sides 4, 5, 7", "sides 2, 3, 4", "angles 20°, 30°, 130°"], ["sides 5, 12, 13", "sides 6, 7, 8", "angles 50°, 60°, 70°"], ["Obtuse if c² > a² + b²: 49 > 41, 16 > 13."])
B.orq(S, "cp1", "Triangle PQR has PQ = 3x + 1, QR = 5x - 7, PR = 2x + 5.", [("For what x is PQ = QR?", "x = 4"), ("Find the side lengths for that x.", "13, 13, 13"), ("Classify the triangle.", "equilateral"), ("Is it acute, right, or obtuse?", "acute (all angles 60°)")], ["3x + 1 = 5x - 7.", "Substitute; PR = 13 too.", "All equal.", "Equiangular."])
assert 3 * 4 + 1 == 5 * 4 - 7 == 2 * 4 + 5
B.orq(S, "honors", "A triangle has sides 6, 8, and x (x the longest side).", [("For what x is it right?", "x = 10"), ("For what x is it acute?", "8 ≤ x < 10"), ("For what x is it obtuse?", "10 < x < 14"), ("Why must x < 14?", "Triangle inequality: x < 6 + 8")], ["x² = 36 + 64.", "x² < 100 with x the longest.", "x² > 100.", "Sum of two sides exceeds the third."], tags=["challenge"])
B.sa(S, "cp2", "How many congruent sides does a scalene triangle have?", "none", ["All sides different."])
B.mc(S, "cp1", "An isosceles right triangle has angles…", "45°, 45°, 90°", ["30°, 60°, 90°", "60°, 60°, 60°", "90°, 90°, 0°"], ["Two equal acute angles sum to 90°."])

# ---------------- Skill 2: angle sum and exterior angles ----------------
S = 2
for a, b in [(48, 77), (90, 33), (115, 22), (61.5, 58.5), (35, 35)]:
    B.sa(S, "cp2", f"Two angles of a triangle measure {a:g}° and {b:g}°. Find the third.", f"{180 - a - b:g}°", ["Triangle Angle Sum: 180°."])
for e1, e2, e3 in [("x°", "(2x)°", "(3x)°"), ("(x + 10)°", "(2x - 5)°", "(x + 15)°"), ("(4x - 3)°", "(3x + 8)°", "(2x + 4)°"), ("(5x)°", "(x + 30)°", "(2x + 6)°")]:
    tot = linp(e1) + linp(e2) + linp(e3); xv = (180 - tot.c[0]) / tot.c[1]
    vals = [linp(e)(xv) for e in (e1, e2, e3)]; assert all(v > 0 for v in vals)
    B.sa(S, "cp1", f"The angles of a triangle measure {e1}, {e2}, and {e3}. Find x and each angle.", f"x = {fr(xv)}; " + ", ".join(f"{fr(v)}°" for v in vals), ["Sum = 180°.", f"x = {fr(xv)}."])
for i, (r1, r2) in enumerate([(55, 70), (38, 97), (64, 64)]):
    A, Bv, C = tri_from_angles(180 - r1 - r2, r1, base=5); Cext = (C[0] + 2.2, 0)
    fg = Fig(4.4, 3.0); fg.poly([A, Bv, C]); fg.seg(C, Cext); fg.names([A, Bv, C], ["A", "B", "C"])
    fg.angle(Bv, C, A, f"{r1}°", r=0.55); fg.angle(A, Bv, C, f"{180 - r1 - r2}°", r=0.5); fg.angle(C, Cext, A, "x°", r=0.55)
    dg = fg.save(B, f"s02-ext-{i}", f"Triangle ABC with angle B = {r1}°, angle A = {180 - r1 - r2}°, and exterior angle x° at C formed by extending BC.")
    B.mc(S, "cp1", "Use the figure. Find x.", f"{180 - r2}", [f"{r2}", f"{180 - r1}", f"{r1}", f"{180 - r1 - r2}", f"{r1 + r2}"], ["Exterior angle = sum of the two remote interior angles.", f"{r1} + {180 - r1 - r2} = {180 - r2}."], diagram=dg, tags=["graph"])
for ext_, rem, e in [(130, 55, None), (98, 41, None), (145, 90, None)]:
    B.sa(S, "cp1", f"An exterior angle of a triangle measures {ext_}°. One remote interior angle is {rem}°. Find the other remote interior angle and the adjacent interior angle.", f"{ext_ - rem}° and {180 - ext_}°", ["Exterior Angle Theorem.", "Linear pair with the adjacent interior angle."])
for e1, e2, e3 in [("(2x + 10)°", "(x + 20)°", "(4x - 10)°"), ("(3x)°", "(x + 18)°", "(5x - 6)°")]:
    p1, p2, p3 = linp(e1), linp(e2), linp(e3); xv = (p3.c[0] - (p1 + p2).c[0]) / ((p1 + p2).c[1] - p3.c[1])
    assert p1(xv) + p2(xv) == p3(xv) and p3(xv) < 180
    B.sa(S, "cp1", f"An exterior angle measures {e3}; its remote interior angles measure {e1} and {e2}. Find x and the exterior angle.", f"x = {fr(xv)}; {fr(p3(xv))}°", ["Exterior angle = sum of remote interior angles.", f"x = {fr(xv)}."])
B.mc(S, "cp1", "A student says an exterior angle equals the adjacent interior angle. What is correct?", "It is supplementary to the adjacent angle and equals the sum of the two remote angles", ["Correct", "It equals 90°", "It equals the largest angle"], ["Exterior Angle Theorem."], tags=["error-analysis", "misconception"])
B.sel(S, "cp1", "Select ALL possible angle sets of a triangle.", ["90°, 45°, 45°", "100°, 40°, 40°", "1°, 1°, 178°"], ["90°, 90°, 0°", "60°, 60°, 70°", "120°, 70°, 10°"], ["Positive angles summing to 180°."])
B.sel(S, "honors", "Select ALL statements that must be true for any triangle.", ["The sum of the exterior angles (one per vertex) is 360°", "An exterior angle is larger than either remote interior angle", "At most one angle is obtuse"], ["Every exterior angle is obtuse", "The exterior angles are congruent"], ["Exterior angle sum: 3·180 - 180 = 360°."], tags=["reasoning"])
B.orq(S, "honors", "Prove the Triangle Angle Sum Theorem for △ABC using a line through B parallel to AC.", [("Name the angles formed at B along the parallel line.", "∠1, ∠ABC, ∠2 form a straight angle"), ("Relate ∠1 to an angle of the triangle.", "∠1 ≅ ∠A (alternate interior)"), ("Relate ∠2.", "∠2 ≅ ∠C (alternate interior)"), ("Conclude.", "m∠A + m∠ABC + m∠C = 180°")], ["Angles on a line sum to 180°.", "Parallel line theorems.", "Parallel line theorems.", "Substitution."], tags=["reasoning"])
B.sa(S, "cp2", "Each angle of an equiangular triangle measures?", "60°", ["180/3."])
B.sa(S, "honors", "The angles of a triangle are in the ratio 2 : 3 : 7. Find the largest angle.", "105°", ["12k = 180 → k = 15."])
B.sa(S, "cp1", "In a right triangle one acute angle is 4 times the other. Find both acute angles.", "18° and 72°", ["5x = 90."])

# ---------------- Skill 3: corresponding parts ----------------
S = 3
for stmt in ["△ABC ≅ △DEF", "△PQR ≅ △XYZ", "△JKL ≅ △MNO", "△RST ≅ △UVW"]:
    L1, L2 = stmt[1:4], stmt[-3:]
    i = R.randrange(3); j = (i + 1) % 3
    side1 = L1[i] + L1[j]; side2 = L2[i] + L2[j]; ang1 = L1[(i + 2) % 3]; ang2 = L2[(i + 2) % 3]
    B.mc(S, "cp2", f"{stmt}. Which side corresponds to {side1}?", side2, [L2[j] + L2[(j + 1) % 3], L2[(i + 2) % 3] + L2[i], side1[::-1]], ["Match letters in order."])
    B.mc(S, "cp2", f"{stmt}. Which angle corresponds to ∠{ang1}?", f"∠{ang2}", [f"∠{L2[i]}", f"∠{L2[j]}", f"∠{L1[i]}"], ["Same position in the statement."])
    B.sel(S, "cp1", f"{stmt}. Select ALL true congruence statements.", [f"{L1[0]}{L1[1]} ≅ {L2[0]}{L2[1]}", f"∠{L1[2]} ≅ ∠{L2[2]}", f"△{L1[1]}{L1[2]}{L1[0]} ≅ △{L2[1]}{L2[2]}{L2[0]}"], [f"{L1[0]}{L1[1]} ≅ {L2[1]}{L2[2]}", f"∠{L1[0]} ≅ ∠{L2[1]}", f"△{L1[1]}{L1[0]}{L1[2]} ≅ △{L2[0]}{L2[1]}{L2[2]}"], ["Corresponding parts keep the same letter positions; reordering both names the same way keeps the statement true."])
B.orq(S, "cp1", "△ABC ≅ △DEF with AB = 7, BC = 10, m∠A = 64°, m∠E = 48°.", [("Find DE.", "7"), ("Find EF.", "10"), ("Find m∠D.", "64°"), ("Find m∠C and m∠F.", "68° and 68°")], ["DE ↔ AB.", "EF ↔ BC.", "∠D ↔ ∠A.", "180 - 64 - 48."])
for e1, e2 in [("2x + 3", "x + 9"), ("4x - 5", "3x + 2")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.sa(S, "cp1", f"△KLM ≅ △RST. KL = {e1} and RS = {e2}. Find x and KL.", f"x = {fr(xv)}; KL = {fr(p1(xv))}", ["Corresponding sides are congruent.", f"x = {fr(xv)}."])
B.mc(S, "cp1", "△ABC ≅ △FED. A student says AB ≅ FD. What is correct?", "AB ≅ FE", ["AB ≅ ED", "AC ≅ FE", "Correct"], ["A↔F, B↔E, C↔D."], tags=["error-analysis"])
B.sa(S, "honors", "△ABC ≅ △CBA (same triangle, letters reordered). What must be true of △ABC?", "AB ≅ CB, so it is isosceles with vertex B", ["A↔C means AB ↔ CB."], tags=["reasoning", "challenge"])
B.sa(S, "cp2", "If △GHI ≅ △JKL, which angle is congruent to ∠H?", "∠K", ["Second letters correspond."])

# ---------------- Skill 4: rigid motions ----------------
S = 4
for q, a, w in [("Which transformation does NOT preserve congruence?", "dilation by 2", ["translation", "reflection", "rotation"]), ("Two figures are congruent if…", "a sequence of rigid motions maps one onto the other", ["they have the same area", "they have the same perimeter", "a dilation maps one onto the other"]),
                ("Which property is NOT preserved by a reflection?", "orientation (clockwise order of vertices)", ["side lengths", "angle measures", "area"]), ("A rotation of 180° about a point maps segment AB to A'B'. Which is true?", "A'B' = AB and A'B' ∥ AB", ["A'B' = 2AB", "A'B' ⊥ AB", "A'B' = AB/2"])]:
    B.mc(S, "cp1", q, a, w, ["Rigid motions preserve distance and angle measure."])
for P_, rule, img in [([(1, 2), (4, 2), (1, 6)], "(x, y) → (x + 3, y - 5)", [(4, -3), (7, -3), (4, 1)]), ([(2, 1), (5, 1), (5, 3)], "reflection over the y-axis", [(-2, 1), (-5, 1), (-5, 3)]),
                      ([(1, 1), (4, 1), (1, 3)], "rotation 90° counterclockwise about the origin", [(-1, 1), (-1, 4), (-3, 1)]), ([(0, 0), (3, 0), (0, 4)], "reflection over y = x", [(0, 0), (0, 3), (4, 0)])]:
    B.orq(S, "cp1", f"△ABC has A{pt(*P_[0])}, B{pt(*P_[1])}, C{pt(*P_[2])}. Apply {rule}.", [("Find A′.", pt(*img[0])), ("Find B′.", pt(*img[1])), ("Find C′.", pt(*img[2])), ("Is △A′B′C′ ≅ △ABC? Why?", "Yes: rigid motions preserve lengths and angles")],
          ["Apply the rule to each vertex.", "Same rule.", "Same rule.", "Rigid motions preserve congruence."], tags=["connections"])
    d = lambda p, q: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    assert all(d(P_[i], P_[j]) == d(img[i], img[j]) for i, j in itertools.combinations(range(3), 2))
B.sel(S, "cp1", "Select ALL rigid motions.", ["translation", "reflection", "rotation", "glide reflection"], ["dilation", "stretch", "shear"], ["Rigid motions preserve distance."])
B.sel(S, "honors", "△ABC is mapped to △A′B′C′ by a rotation followed by a translation. Select ALL statements that must be true.", ["△ABC ≅ △A′B′C′", "AB = A′B′", "m∠A = m∠A′", "the orientation is unchanged"], ["AB ∥ A′B′", "A′ = A"], ["Rotations and translations preserve orientation; parallelism to the original only for translations/180° rotations."], tags=["reasoning"])
B.sa(S, "cp1", "Describe a rigid motion that maps △ABC with A(1, 1), B(3, 1), C(1, 4) to A′(-1, 1), B′(-3, 1), C′(-1, 4).", "reflection over the y-axis", ["(x, y) → (-x, y)."])
B.sa(S, "honors", "Describe a sequence of rigid motions mapping A(0, 0), B(2, 0), C(0, 1) to A′(3, 3), B′(3, 5), C′(2, 3).", "rotate 90° counterclockwise about the origin, then translate (x, y) → (x + 3, y + 3)", ["Rotation: B(2, 0) → (0, 2), C(0, 1) → (-1, 0).", "Translate by (3, 3)."], tags=["challenge"])
B.mc(S, "cp2", "Which describes a translation?", "every point moves the same distance in the same direction", ["a flip over a line", "a turn about a point", "an enlargement"], ["Definition."])
B.sa(S, "cp1", "△RST ≅ △R′S′T′ by a reflection. RS = 9 and m∠T = 41°. Find R′S′ and m∠T′.", "9; 41°", ["Reflections preserve length and angle measure."])
B.orq(S, "honors", "Explain why SAS follows from rigid motions.", [("Map one vertex to its match.", "translate so A goes to D"), ("Align one congruent side.", "rotate so ray AB lies on ray DE; B lands on E since AB = DE"), ("Place the third vertex.", "reflect over DE if needed so C is on the same side as F"), ("Why does C land on F?", "∠A ≅ ∠D puts C on ray DF and AC = DF fixes the point")], ["Translation.", "Rotation.", "Reflection.", "Angle and length determine the point."], tags=["reasoning", "challenge"])

# ---------------- Skills 5–7: criteria from marked figures ----------------
cases = [({"AB", "BC", "CA"}, set(), None), ({"AB", "BC"}, {"B"}, None), ({"AB", "CA"}, {"A"}, None), ({"BC", "CA"}, {"C"}, None),
         ({"AB"}, {"A", "B"}, None), ({"BC"}, {"B", "C"}, None), ({"CA"}, {"A", "C"}, None),
         ({"AB"}, {"B", "C"}, None), ({"BC"}, {"A", "C"}, None), ({"CA"}, {"A", "B"}, None),
         ({"AB", "BC"}, {"A"}, None), ({"BC", "CA"}, {"B"}, None), (set(), {"A", "B", "C"}, None),
         ({"CA", "AB"}, set(), "A"), ({"BC", "AB"}, set(), "A"), ({"BC", "CA"}, set(), "A")]
bucket = {"SSS": 5, "SAS": 5, "ASA": 6, "AAS": 6, "HL": 7}
for k_, (sd, an, rt) in enumerate(cases):
    crit = criterion(sd, an, rt)
    shape = (5.0, 4.2, 3.4) if rt is None else (math.hypot(4, 3), 3.0, 4.0)
    dg = pair_fig(f"crit-{k_}", sd, an, rt, shape=shape)
    S_ = bucket.get(crit, 6 if "AAA" in crit else 5)
    choices = ["SSS", "SAS", "ASA", "AAS", "HL", "not enough information"]
    ans = crit if crit in bucket else "not enough information"
    B.mc(S_, "cp1" if crit in bucket else "honors", "Using only the marked information, which shortcut (if any) proves △ABC ≅ △DEF?", ans, [c for c in choices if c != ans][:3],
         [f"Marked: {len(sd)} pair(s) of sides and {len(an) + (1 if rt else 0)} pair(s) of angles.", "Check whether the angle is included between the sides (SAS) or the side between the angles (ASA)." if crit in ("SAS", "ASA") else ("SSA and AAA do not prove congruence." if crit not in bucket else f"Criterion: {crit}.")], diagram=dg, tags=["graph", "reasoning"])
for crit_, desc, S_ in [("SSS", "three pairs of congruent sides", 5), ("SAS", "two pairs of sides and the included angles congruent", 5), ("ASA", "two pairs of angles and the included sides congruent", 6), ("AAS", "two pairs of angles and a non-included pair of sides congruent", 6), ("HL", "right triangles with congruent hypotenuses and one pair of congruent legs", 7)]:
    B.mc(S_, "cp2", f"Which congruence shortcut uses {desc}?", crit_, [c for c in ["SSS", "SAS", "ASA", "AAS", "HL"] if c != crit_][:3], ["Name the parts in order around the triangle."])
B.sel(5, "cp1", "Select ALL combinations that do NOT guarantee congruence.", ["SSA", "AAA"], ["SSS", "SAS", "ASA", "AAS"], ["SSA (ambiguous case) and AAA (similar only) fail."], tags=["misconception"])
for sd, tri in [("AB = DE = 5, BC = EF = 7, AC = DF = 9", "SSS"), ("AB = DE = 4, ∠B ≅ ∠E, BC = EF = 6", "SAS"), ("AB = DE = 4, BC = EF = 6, ∠A ≅ ∠D", "none")]:
    B.mc(5, "cp1", f"In △ABC and △DEF: {sd}. Can you conclude △ABC ≅ △DEF? If so, by which shortcut?", f"Yes, {tri}" if tri != "none" else "No: SSA does not prove congruence", ["Yes, SAS" if tri != "SAS" else "Yes, SSS", "No: not enough information" if tri != "none" else "Yes, SAS", "Yes, ASA"], ["Identify the parts and whether the angle is included."])
for sd, tri in [("∠A ≅ ∠D, AB = DE, ∠B ≅ ∠E", "ASA"), ("∠A ≅ ∠D, ∠B ≅ ∠E, BC = EF", "AAS"), ("∠A ≅ ∠D, ∠B ≅ ∠E, ∠C ≅ ∠F", "none")]:
    B.mc(6, "cp1", f"In △ABC and △DEF: {sd}. Can you conclude △ABC ≅ △DEF? If so, by which shortcut?", f"Yes, {tri}" if tri != "none" else "No: AAA shows only similarity", ["Yes, AAS" if tri != "AAS" else "Yes, ASA", "No: not enough information" if tri != "none" else "Yes, ASA", "Yes, SAS"], ["Is the side between the two angles (ASA) or not (AAS)?"])
for hyp, leg in [(13, 5), (10, 6), (25, 7)]:
    other = int(math.isqrt(hyp * hyp - leg * leg))
    B.orq(7, "cp1", f"Right triangles ABC and DEF have right angles at C and F, AB = DE = {hyp}, and AC = DF = {leg}.", [("Which shortcut proves them congruent?", "HL"), ("Find BC.", str(other)), ("Find EF.", str(other)), ("Name another shortcut that now also applies.", "SSS (or SAS)")],
          ["Hypotenuse and leg of right triangles.", "Pythagorean theorem.", "Corresponding part.", "All sides known."])
B.sel(7, "cp1", "Select ALL conditions needed to use HL.", ["both triangles are right triangles", "the hypotenuses are congruent", "one pair of legs is congruent"], ["both pairs of acute angles are congruent", "the triangles are isosceles"], ["HL needs right triangles, hypotenuses, and one leg."])
B.mc(7, "cp1", "Why is HL valid even though it looks like SSA?", "In a right triangle, the Pythagorean theorem determines the third side, so SSS applies", ["Because the right angle is included", "Because all right triangles are congruent", "It is not valid"], ["c² = a² + b² fixes the other leg."], tags=["reasoning"])
B.mc(7, "cp2", "Right triangles have congruent hypotenuses and one pair of congruent acute angles. Which shortcut applies?", "AAS", ["HL", "SAS", "none"], ["Right angle + acute angle + hypotenuse (non-included)."], tags=["misconception"])
B.sa(7, "honors", "In right △PQR (right angle at Q) and right △STU (right angle at T), PR = SU = 2x + 1, PQ = 3x - 2, ST = x + 6. For what x are they congruent by HL, and what is PQ?", "x = 4; PQ = 10", ["Need PQ = ST: 3x - 2 = x + 6 → x = 4.", "Hypotenuses are already congruent."], tags=["challenge"])
B.sa(7, "cp1", "Two right triangles have legs 5 and 12 and 5 and 12. Which shortcuts prove them congruent?", "SAS (legs with the included right angle), also SSS/HL after finding the hypotenuse 13", ["The right angle is included between the legs."])
B.sel(6, "honors", "△ABC and △DEF have ∠A ≅ ∠D and ∠B ≅ ∠E. Select ALL additional facts that would prove congruence.", ["AB ≅ DE", "BC ≅ EF", "AC ≅ DF"], ["∠C ≅ ∠F", "The triangles have the same shape"], ["Any pair of corresponding sides works (ASA or AAS)."], tags=["reasoning"])
B.sel(5, "honors", "△ABC and △DEF have AB ≅ DE and BC ≅ EF. Select ALL additional facts that would prove congruence.", ["AC ≅ DF", "∠B ≅ ∠E"], ["∠A ≅ ∠D", "∠C ≅ ∠F", "∠A ≅ ∠E"], ["SSS or SAS with the included angle B; ∠A or ∠C gives SSA."], tags=["reasoning"])

# ---------------- Skill 8: CPCTC ----------------
S = 8
for given, crit, conc in [("AB ≅ CB and AD ≅ CD in kite ABCD with diagonal BD", "SSS", "∠A ≅ ∠C"), ("M is the midpoint of AE and of BD", "SAS", "AB ≅ ED"), ("AB ∥ DE, AB ≅ DE, and AE meets BD at M", "AAS (or ASA)", "AM ≅ EM")]:
    B.mc(S, "cp1", f"Given: {given}. After proving the triangles congruent by {crit}, which conclusion follows by CPCTC?", conc, ["The triangles are similar", "All angles are right angles", "The figure is a square"], ["CPCTC: corresponding parts of congruent triangles are congruent."])
B.orq(S, "cp1", "Given: AB ≅ CB, AD ≅ CD in kite ABCD. Prove ∠A ≅ ∠C.", [("Name the triangles and the shared side.", "△ABD and △CBD share BD"), ("Why is BD ≅ BD?", "Reflexive Property"), ("Which shortcut proves the triangles congruent?", "SSS"), ("Conclude ∠A ≅ ∠C.", "CPCTC")], ["Diagonal BD splits the kite.", "Shared side.", "Three pairs of sides.", "Corresponding angles."], tags=["reasoning"])
B.orq(S, "cp1", "To measure the width AB of a pond, a surveyor marks C, extends AC to D with CD = AC, and BC to E with CE = BC.", [("Which angles are congruent at C?", "∠ACB ≅ ∠DCE (vertical angles)"), ("Which shortcut proves △ACB ≅ △DCE?", "SAS"), ("What is DE in terms of AB?", "DE = AB"), ("Justify.", "CPCTC")], ["Vertical angles.", "Two sides and included angle.", "Corresponding sides.", "CPCTC."], tags=["modeling", "reasoning"])
for e1, e2, part in [("3x + 4", "5x - 8", "side"), ("(2x + 15)°", "(4x - 5)°", "angle")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.sa(S, "cp1", f"△ABC ≅ △DEF. The corresponding {part}s measure {e1} and {e2}. Find x.", f"x = {fr(xv)}", ["CPCTC: corresponding parts are equal.", f"x = {fr(xv)}."])
B.sel(S, "cp1", "△PQR ≅ △STU has been proved. Select ALL valid CPCTC conclusions.", ["PQ ≅ ST", "∠R ≅ ∠U", "QR ≅ TU"], ["PQ ≅ TU", "∠P ≅ ∠U", "PR ≅ ST"], ["Use the correspondence P↔S, Q↔T, R↔U."])
B.mc(S, "cp1", "A student uses CPCTC to prove two triangles are congruent. What is wrong?", "CPCTC can be used only after the triangles are proved congruent", ["Nothing", "CPCTC needs three pairs of sides", "CPCTC applies only to right triangles"], ["Order of reasoning."], tags=["error-analysis", "misconception"])
B.sa(S, "honors", "Given: AB ≅ AC and AD bisects ∠BAC (D on BC). Prove BD ≅ CD. List the shortcut and final reason.", "SAS (AB ≅ AC, ∠BAD ≅ ∠CAD, AD ≅ AD); then CPCTC", ["Bisector gives congruent angles; AD is shared."], tags=["reasoning"])
B.sa(S, "honors", "Using the same triangles, explain why AD ⊥ BC.", "∠ADB ≅ ∠ADC by CPCTC and they form a linear pair, so each is 90°", ["Congruent supplementary angles are right."], tags=["reasoning", "challenge"])
B.sa(S, "cp2", "What does CPCTC stand for?", "Corresponding Parts of Congruent Triangles are Congruent", ["Definition."])

# ---------------- Skill 9: proofs ----------------
S = 9
proofs = [("Given: AB ≅ CD, AB ∥ CD (ABCD with diagonal AC). Prove: △ABC ≅ △CDA.", ["AB ≅ CD — Given", "AB ∥ CD — Given", "∠BAC ≅ ∠DCA — Alternate Interior Angles Theorem", "AC ≅ CA — Reflexive Property", "△ABC ≅ △CDA — SAS"]),
          ("Given: M is the midpoint of PQ and of RS. Prove: △PMR ≅ △QMS.", ["M is the midpoint of PQ and RS — Given", "PM ≅ QM and RM ≅ SM — Definition of midpoint", "∠PMR ≅ ∠QMS — Vertical Angles Theorem", "△PMR ≅ △QMS — SAS"]),
          ("Given: ∠A ≅ ∠D, ∠ACB ≅ ∠DCE, C is the midpoint of AD. Prove: △ABC ≅ △DEC.", ["∠A ≅ ∠D — Given", "C is the midpoint of AD — Given", "AC ≅ DC — Definition of midpoint", "∠ACB ≅ ∠DCE — Given (or vertical angles)", "△ABC ≅ △DEC — ASA"]),
          ("Given: BD ⊥ AC, AB ≅ CB. Prove: △ABD ≅ △CBD.", ["BD ⊥ AC — Given", "∠ADB and ∠CDB are right angles — Definition of perpendicular", "AB ≅ CB — Given", "BD ≅ BD — Reflexive Property", "△ABD ≅ △CBD — HL"])]
for given, steps in proofs:
    parts = steps[:3] + ["; ".join(steps[3:])]
    B.orq(S, "cp1" if len(steps) == 4 else "honors", given, [(f"Step {k + 1}{' (final steps)' if k == 3 and len(steps) > 4 else ''}: statement and reason.", st) for k, st in enumerate(parts)],
          ["Begin with the givens.", "Translate definitions into congruent parts.", "Find the third pair (shared side, vertical angles, or parallel-line angles).", "Name the shortcut."], tags=["reasoning"])
for stmt, reason, wr in [("AC ≅ AC", "Reflexive Property", ["Symmetric Property", "Given", "CPCTC"]), ("∠1 ≅ ∠2 where ∠1 and ∠2 are vertical", "Vertical Angles Theorem", ["Linear Pair Postulate", "CPCTC", "Given"]),
                         ("If M is the midpoint of AB, then AM ≅ MB", "Definition of midpoint", ["Segment Addition Postulate", "Midpoint Theorem converse", "CPCTC"]), ("If BD bisects ∠ABC, then ∠ABD ≅ ∠DBC", "Definition of angle bisector", ["Angle Addition Postulate", "Vertical Angles Theorem", "Given"]),
                         ("If AB ∥ CD, then alternate interior angles are congruent", "Alternate Interior Angles Theorem", ["Converse of Alternate Interior Angles Theorem", "Corresponding Angles Postulate converse", "CPCTC"])]:
    B.mc(S, "cp1", f"Which reason justifies: {stmt}?", reason, wr, ["Match the statement to its definition, postulate, or theorem."], tags=["reasoning"])
B.sel(S, "cp1", "Select ALL reasons that can justify a pair of congruent angles in a triangle congruence proof.", ["Vertical Angles Theorem", "Alternate Interior Angles Theorem", "Definition of angle bisector", "All right angles are congruent"], ["Segment Addition Postulate", "Definition of midpoint"], ["Midpoints and segment addition give segments, not angles."])
B.sel(S, "honors", "Select ALL errors in this proof: 1) AB ≅ DE (Given) 2) ∠A ≅ ∠D (Given) 3) BC ≅ EF (Given) 4) △ABC ≅ △DEF (SAS).", ["The angle is not included between the sides", "The correct pattern is SSA, which is not a valid shortcut"], ["Step 1 needs the Reflexive Property", "Step 4 should say ASA"], ["∠A is not between AB and BC."], tags=["error-analysis"])
B.orq(S, "honors", "Write a flow proof: Given AB ∥ DE, C is the midpoint of BE (A–C–D and B–C–E collinear). Prove AB ≅ DE.", [("Angles from parallel lines.", "∠B ≅ ∠E (alternate interior)"), ("Segments from the midpoint.", "BC ≅ EC"), ("Third pair.", "∠ACB ≅ ∠DCE (vertical angles)"), ("Conclude.", "△ABC ≅ △DEC by ASA, so AB ≅ DE by CPCTC")], ["Parallel lines.", "Midpoint.", "Vertical angles.", "ASA then CPCTC."], tags=["reasoning", "challenge"])
B.sa(S, "cp2", "What is the last reason in a proof that two triangles are congruent by three pairs of sides?", "SSS", ["Name the shortcut."])
B.mc(S, "cp1", "In a two-column proof, what usually comes first?", "the given information", ["the conclusion", "CPCTC", "the Reflexive Property"], ["Start from what is known."])

# ================= additions: generated variety =================
R3 = random.Random(3033)
LETTERS = ["ABC", "DEF", "PQR", "STU", "JKL", "MNO", "XYZ", "GHI", "RST", "UVW"]
def facts_text(L1, L2, sd, an):
    m = dict(zip("ABC", L1)); n = dict(zip("ABC", L2)); out = []
    for x in sorted(sd): out.append(f"{m[x[0]]}{m[x[1]]} ≅ {n[x[0]]}{n[x[1]]}")
    for v in sorted(an): out.append(f"∠{m[v]} ≅ ∠{n[v]}")
    return out
combos = []
for ns in range(0, 4):
    for na in range(0, 4):
        if ns + na != 3: continue
        for sd in itertools.combinations(["AB", "BC", "CA"], ns):
            for an in itertools.combinations("ABC", na):
                combos.append((set(sd), set(an)))
R3.shuffle(combos)
choices = ["SSS", "SAS", "ASA", "AAS", "not enough information"]
per = {5: 0, 6: 0}
for k_, (sd, an) in enumerate(combos * 2):
    crit = criterion(sd, an); ans = crit if crit in bucket else "not enough information"
    S_ = 5 if ans in ("SSS", "SAS") else 6 if ans in ("ASA", "AAS") else (5 if "SSA" in crit else 6)
    if per[S_] >= 18: continue
    per[S_] += 1
    i1, i2 = R3.sample(range(len(LETTERS)), 2); L1, L2 = LETTERS[i1], LETTERS[i2]
    ft = facts_text(L1, L2, sd, an); R3.shuffle(ft)
    if k_ % 3 == 2:
        B.sa(S_, "cp1", f"In △{L1} and △{L2}: {'; '.join(ft)}. Which shortcut proves △{L1} ≅ △{L2}? Write 'none' if none applies.", ans if ans in bucket else "none", ["List the pairs in order around the triangle.", "Included angle → SAS; included side → ASA; non-included side → AAS; SSA/AAA → none."])
    else:
        B.mc(S_, "cp1" if ans in bucket else "honors", f"In △{L1} and △{L2}: {'; '.join(ft)}. Which shortcut (if any) proves △{L1} ≅ △{L2}?", ans, [c for c in choices if c != ans][:3],
             ["Check whether the angle is between the two sides (SAS) or the side is between the two angles (ASA).", f"Here: {crit}."], tags=["reasoning"])
for target, S_ in [("SAS", 5), ("ASA", 6), ("AAS", 6), ("SSS", 5)]:
    for base_s, base_a in ([({"AB"}, {"B"}), ({"BC"}, {"B"})] if target == "SAS" else [({"AB"}, {"A"}), ({"BC"}, {"C"})] if target == "ASA" else [({"BC"}, {"A"}), ({"AB"}, {"C"})] if target == "AAS" else [({"AB", "BC"}, set())]):
        i1, i2 = R3.sample(range(len(LETTERS)), 2); L1, L2 = LETTERS[i1], LETTERS[i2]
        extra = [(set(), {v}) for v in "ABC" if v not in base_a] + [({x}, set()) for x in ["AB", "BC", "CA"] if x not in base_s]
        right = [facts_text(L1, L2, e[0], e[1])[0] for e in extra if criterion(base_s | e[0], base_a | e[1]) == target]
        wrong = [facts_text(L1, L2, e[0], e[1])[0] for e in extra if criterion(base_s | e[0], base_a | e[1]) != target]
        if len(right) == 0 or len(wrong) == 0: continue
        given = "; ".join(facts_text(L1, L2, base_s, base_a))
        if len(right) >= 2:
            B.sel(S_, "honors", f"Given {given}. Select ALL additional facts that would let you prove △{L1} ≅ △{L2} by {target}.", right, wrong, [f"{target} needs the parts in the right order around the triangle."], tags=["reasoning"])
        else:
            B.mc(S_, "cp1", f"Given {given}. Which additional fact lets you prove △{L1} ≅ △{L2} by {target}?", right[0], wrong[:3], [f"{target} needs the parts in the right order around the triangle."], tags=["reasoning"])
# HL text items
for k_ in range(10):
    i1, i2 = R3.sample(range(len(LETTERS)), 2); L1, L2 = LETTERS[i1], LETTERS[i2]
    rv = R3.choice("ABC"); m = dict(zip("ABC", L1)); n = dict(zip("ABC", L2))
    o = [x for x in "ABC" if x != rv]; hyp = (m[o[0]] + m[o[1]], n[o[0]] + n[o[1]]); leg = (m[rv] + m[o[0]], n[rv] + n[o[0]]); ang = (m[o[0]], n[o[0]])
    kind = k_ % 5
    if kind == 0: info, ans = f"{hyp[0]} ≅ {hyp[1]} and {leg[0]} ≅ {leg[1]}", "HL"
    elif kind == 1: info, ans = f"{leg[0]} ≅ {leg[1]} and {m[rv]}{m[o[1]]} ≅ {n[rv]}{n[o[1]]}", "SAS (two legs with the included right angle)"
    elif kind == 2: info, ans = f"{hyp[0]} ≅ {hyp[1]} and ∠{ang[0]} ≅ ∠{ang[1]}", "AAS"
    elif kind == 3: info, ans = f"{leg[0]} ≅ {leg[1]} and ∠{ang[0]} ≅ ∠{ang[1]}", "ASA"
    else: info, ans = f"∠{ang[0]} ≅ ∠{ang[1]}", "not enough information"
    opts = ["HL", "SAS (two legs with the included right angle)", "AAS", "ASA", "not enough information"]
    B.mc(7, "cp1" if kind in (0, 1) else "honors", f"△{L1} and △{L2} are right triangles with right angles at {m[rv]} and {n[rv]}. Also {info}. Which shortcut proves them congruent?", ans, [x for x in opts if x != ans][:3],
         ["The right angles give one pair of congruent angles.", "Hypotenuse is opposite the right angle; legs touch it."], tags=["reasoning"])
for hyp, leg in [(17, 8), (29, 20), (41, 9), (15, 9), (26, 10)]:
    other = math.isqrt(hyp * hyp - leg * leg); assert other * other + leg * leg == hyp * hyp
    B.sa(7, "cp1", f"Right triangles RST and UVW (right angles at S and V) have RT = UW = {hyp} and RS = UV = {leg}. Explain why they are congruent and find ST.", f"HL; ST = {other}", ["Hypotenuse and a leg are congruent.", f"ST = √({hyp}² - {leg}²) = {other}."])
B.sel(7, "cp1", "Select ALL pairs of right triangles that must be congruent.", ["hypotenuse and one leg congruent", "both pairs of legs congruent", "hypotenuse and one acute angle congruent"], ["one pair of acute angles congruent", "both pairs of acute angles congruent"], ["HL, SAS (LL), AAS (HA); angles alone give similarity only."], tags=["reasoning"])
# Skill 1 generated
for k_ in range(8):
    while True:
        a, b, c = sorted(R3.sample(range(3, 20), 3))
        if a + b > c: break
    if k_ % 4 == 0: b = a
    v = a * a + b * b - c * c
    s_kind = "isosceles" if len({a, b, c}) < 3 else "scalene"; a_kind = "right" if v == 0 else ("acute" if v > 0 else "obtuse")
    B.mc(1, "cp1", f"Classify a triangle with sides {a}, {b}, {c} by sides and angles.", f"{s_kind}, {a_kind}", [f"{s_kind}, {x}" for x in ["acute", "right", "obtuse"] if x != a_kind][:2] + [f"{'scalene' if s_kind == 'isosceles' else 'isosceles'}, {a_kind}"],
         ["Count equal sides.", f"{a}² + {b}² = {a * a + b * b} vs {c}² = {c * c}."])
# Skill 2 generated
for k_ in range(6):
    A_ = R3.randint(25, 80); B_ = R3.randint(20, 150 - A_); ext = A_ + B_
    e = R3.choice(["(2x + 4)°", "(3x - 6)°", "(x + 15)°", "(5x - 10)°"]); p1 = linp(e); xv = (ext - p1.c[0]) / p1.c[1]
    B.sa(2, "cp1" if xv.denominator == 1 else "honors", f"The remote interior angles of an exterior angle measure {A_}° and {B_}°. The exterior angle measures {e}. Find x.", f"x = {fr(xv)}", [f"Exterior angle = {A_} + {B_} = {ext}°.", f"{e.strip('°')} = {ext} → x = {fr(xv)}."])
B.sel(2, "cp1", "In △ABC, m∠A = 40° and the exterior angle at C measures 115°. Select ALL true statements.", ["m∠B = 75°", "m∠ACB = 65°", "△ABC is acute"], ["m∠B = 115°", "m∠ACB = 75°", "△ABC is obtuse"], ["75 = 115 - 40; 180 - 115 = 65; all angles < 90."])
# Skill 3 generated
for k_ in range(7):
    L1, L2 = R3.sample(LETTERS, 2); perm = list(range(3)); R3.shuffle(perm)
    L2p = "".join(L2[i] for i in perm)
    i = R3.randrange(3); j = (i + 1) % 3
    if k_ % 2:
        B.mc(3, "cp1", f"△{L1} ≅ △{L2p}. Which segment is congruent to {L1[i]}{L1[j]}?", f"{L2p[i]}{L2p[j]}", [f"{L2p[j]}{L2p[(j + 1) % 3]}", f"{L2p[(i + 2) % 3]}{L2p[i]}", f"{L2[i]}{L2[j]}" if L2[i] + L2[j] != L2p[i] + L2p[j] and L2[j] + L2[i] != L2p[i] + L2p[j] else f"{L1[j]}{L1[i]}"], ["Match by position in the congruence statement."], tags=["misconception"])
    else:
        x = R3.randint(4, 15)
        c1, c2 = R3.randint(2, 6), R3.randint(1, 4)
        k1 = R3.randint(1, 12); val = c1 * x + k1; c3 = c2 if c2 != c1 else c2 + 1; k2 = val - c3 * x
        e1 = f"{c1}x + {k1}"; e2 = f"{c3}x {'+' if k2 >= 0 else '-'} {abs(k2)}"
        B.sa(3, "cp1", f"△{L1} ≅ △{L2p}. {L1[i]}{L1[j]} = {e1} and {L2p[i]}{L2p[j]} = {e2}. Find x and the length.", f"x = {x}; {val}", ["Corresponding sides are congruent.", f"{e1} = {e2} → x = {x}."])
        assert linp(e1)(x) == linp(e2)(x) == val
B.orq(3, "honors", "△ABC ≅ △DEF with AB = 2x + 1, DE = 3x - 4, BC = x + y, EF = 2y - 3.", [("Find x.", "5"), ("Find AB.", "11"), ("Write an equation for y.", "5 + y = 2y - 3"), ("Find y and BC.", "y = 8; BC = 13")], ["2x + 1 = 3x - 4.", "Substitute.", "BC = EF with x = 5.", "Solve."], tags=["multistep"])
# Skill 4 generated
rules = [("translation (x, y) → (x - 4, y + 2)", lambda p: (p[0] - 4, p[1] + 2)), ("reflection over the x-axis", lambda p: (p[0], -p[1])), ("rotation 180° about the origin", lambda p: (-p[0], -p[1])),
         ("rotation 90° clockwise about the origin", lambda p: (p[1], -p[0])), ("reflection over y = -x", lambda p: (-p[1], -p[0])), ("translation (x, y) → (x + 6, y - 1)", lambda p: (p[0] + 6, p[1] - 1))]
for nm, fn in rules:
    T = [(R3.randint(-5, 5), R3.randint(-5, 5)) for _ in range(3)]
    while abs((T[1][0] - T[0][0]) * (T[2][1] - T[0][1]) - (T[2][0] - T[0][0]) * (T[1][1] - T[0][1])) == 0: T = [(R3.randint(-5, 5), R3.randint(-5, 5)) for _ in range(3)]
    img = [fn(p) for p in T]; v = R3.randrange(3); lab = "ABC"[v]
    B.mc(4, "cp1", f"△ABC has A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])}. After a {nm}, where is {lab}′?", pt(*img[v]), [pt(img[v][1], img[v][0]) if img[v][1] != img[v][0] else pt(-img[v][0], img[v][1] + 1), pt(-img[v][0], -img[v][1]) if (-img[v][0], -img[v][1]) != img[v] else pt(img[v][0] + 1, img[v][1]), pt(*T[v])],
         [f"Apply the rule to {lab}{pt(*T[v])}."])
B.sel(4, "cp1", "△ABC ≅ △PQR by a rigid motion. Select ALL statements that must be true.", ["AB = PQ", "m∠C = m∠R", "the perimeters are equal", "the areas are equal"], ["AB ∥ PQ", "A = P"], ["Rigid motions preserve lengths, angles, perimeter, and area."])
# Skill 8 generated
for k_ in range(6):
    L1, L2 = R3.sample(LETTERS, 2); i = R3.randrange(3)
    x = R3.randint(5, 25); c1, c2 = R3.sample([2, 3, 4, 5, 6], 2); k1 = R3.randint(1, 20); val = c1 * x + k1; k2 = val - c2 * x
    if not 0 < val < 180: continue
    e1 = f"({c1}x + {k1})°"; e2 = f"({c2}x {'+' if k2 >= 0 else '-'} {abs(k2)})°"
    B.mc(8, "cp1", f"△{L1} ≅ △{L2}. m∠{L1[i]} = {e1} and m∠{L2[i]} = {e2}. Find m∠{L1[i]}.", f"{val}°", [f"{x}°", f"{180 - val}°", f"{val + c1}°"], ["CPCTC: corresponding angles are equal.", f"x = {x}."])
    assert linp(e1)(x) == linp(e2)(x)
B.orq(8, "honors", "Given: AB ≅ AD and ∠BAC ≅ ∠DAC (C on the bisector). Prove BC ≅ DC and that AC bisects ∠BCD.", [("Prove the triangles congruent.", "△ABC ≅ △ADC by SAS (AC ≅ AC)"), ("Conclude about BC and DC.", "BC ≅ DC by CPCTC"), ("Conclude about ∠BCA and ∠DCA.", "∠BCA ≅ ∠DCA by CPCTC"), ("State the final conclusion.", "AC bisects ∠BCD")], ["SAS.", "CPCTC.", "CPCTC.", "Definition of angle bisector."], tags=["reasoning"])
B.sel(8, "cp1", "After proving △JKL ≅ △MNP, select ALL statements justified by CPCTC.", ["JK ≅ MN", "∠L ≅ ∠P", "KL ≅ NP", "∠J ≅ ∠M"], ["JL ≅ NP", "∠K ≅ ∠P"], ["Correspondence J↔M, K↔N, L↔P."])
B.sa(8, "cp1", "△ABC ≅ △DEF, AB = 12, BC = 15, AC = 9. Find the perimeter of △DEF.", "36", ["Corresponding sides are equal."])
# Skill 9 generated: missing reasons
steps_bank = [("∠ABD ≅ ∠CBD", "BD bisects ∠ABC", "Definition of angle bisector"), ("AM ≅ MB", "M is the midpoint of AB", "Definition of midpoint"), ("∠1 ≅ ∠2", "∠1 and ∠2 are right angles", "All right angles are congruent"),
              ("XY ≅ XY", "XY is a shared side", "Reflexive Property"), ("∠3 ≅ ∠4", "∠3 and ∠4 are alternate interior angles and ℓ ∥ m", "Alternate Interior Angles Theorem"), ("AD ⊥ BC forms ∠ADB = 90°", "AD ⊥ BC", "Definition of perpendicular lines")]
for st_, ctx, rs in steps_bank:
    B.sa(9, "cp1", f"In a proof: given {ctx}, the statement '{st_}' is justified by which reason?", rs, ["Match the statement to a definition, postulate, or theorem."], tags=["reasoning"])
B.mc(9, "honors", "Which proof outline correctly proves △ABC ≅ △CDA when ABCD has AB ∥ CD and AD ∥ BC?", "Alternate interior angles give ∠BAC ≅ ∠DCA and ∠BCA ≅ ∠DAC; AC is shared; ASA", ["AB ≅ CD by definition; SSS", "∠B ≅ ∠D by vertical angles; AAS", "AC bisects both angles; SAS"], ["Two pairs of alternate interior angles with the included shared side."], tags=["reasoning"])
B.sel(9, "cp1", "Select ALL statements that are given-independent facts you can use in any triangle proof when they apply.", ["Reflexive Property for a shared side", "Vertical Angles Theorem", "Triangle Angle Sum Theorem"], ["CPCTC before proving congruence", "SSA"], ["Theorems and properties are always available; CPCTC needs congruence first."], tags=["reasoning"])

R4 = random.Random(3044)
B.sa(1, "cp2", "A triangle has a 90° angle. Classify it by its angles.", "right", ["One right angle."])
for k_ in range(4):
    L1, L2 = R4.sample(LETTERS, 2); v = R4.randrange(3)
    B.sa(3, "cp2", f"△{L1} ≅ △{L2}. Name the angle that corresponds to ∠{L1[v]}.", f"∠{L2[v]}", ["Same position in the statement."])
for k_, (nm, fn) in enumerate(rules[:6]):
    T = [(R4.randint(-6, 6), R4.randint(-6, 6)) for _ in range(3)]
    img = [fn(p_) for p_ in T]
    B.sa(4, "cp2" if "translation" in nm else "cp1", f"Point P{pt(*T[0])} undergoes a {nm}. Find P′.", pt(*img[0]), ["Apply the rule."])
B.mc(4, "cp2", "Which transformation flips a figure over a line?", "reflection", ["translation", "rotation", "dilation"], ["Definition."])
B.mc(4, "cp2", "Which transformation turns a figure about a fixed point?", "rotation", ["reflection", "translation", "dilation"], ["Definition."])
for k_ in range(3):
    L1, L2 = R4.sample(LETTERS, 2)
    B.mc(7, "cp2", f"△{L1} and △{L2} are right triangles. Their hypotenuses are congruent and one pair of legs is congruent. Which shortcut applies?", "HL", ["SSA", "AAA", "ASA"], ["Hypotenuse-Leg."])
for k_ in range(6):
    L1, L2 = R4.sample(LETTERS, 2); i = R4.randrange(3); j = (i + 1) % 3; val = R4.randint(5, 30)
    if k_ % 2:
        B.sa(8, "cp2", f"△{L1} ≅ △{L2} and {L1[i]}{L1[j]} = {val} cm. Find {L2[i]}{L2[j]}.", f"{val} cm", ["CPCTC."])
    else:
        B.sa(8, "cp2", f"△{L1} ≅ △{L2} and m∠{L1[i]} = {val + 30}°. Find m∠{L2[i]}.", f"{val + 30}°", ["CPCTC."])
B.mc(8, "cp1", "Which must come before using CPCTC in a proof?", "a statement that the two triangles are congruent", ["a statement that the triangles are similar", "the Reflexive Property", "a definition of midpoint"], ["CPCTC follows congruence."])
B.orq(8, "cp1", "Given: AB ∥ CD and AB ≅ CD, with AD and BC meeting at E. Prove E is the midpoint of AD.", [("Angle pairs from parallel lines.", "∠A ≅ ∠D and ∠B ≅ ∠C (alternate interior)"), ("Prove the triangles congruent.", "△ABE ≅ △DCE by ASA"), ("Corresponding parts.", "AE ≅ DE by CPCTC"), ("Conclude.", "E is the midpoint of AD")], ["Parallel lines.", "Side between the two angles.", "CPCTC.", "Definition of midpoint."], tags=["reasoning"])
for given, prove, crit_ in [("PQ ≅ RS, QR ≅ SP", "△PQR ≅ △RSP", "SSS (with PR ≅ RP)"), ("AB ⊥ BD, ED ⊥ BD, C is the midpoint of BD, ∠ACB ≅ ∠ECD", "△ABC ≅ △EDC", "ASA"), ("JK ∥ ML, JK ≅ ML", "△JKL ≅ △LMJ", "SAS (alternate interior angles, shared JL)"),
                             ("∠X ≅ ∠Z, WY bisects ∠XWZ... with Y on XZ", "△WXY ≅ △WZY", "AAS (shared WY)")]:
    given = given.replace("... with Y on XZ", " (Y on XZ)")
    B.mc(9, "cp1", f"Given {given}. Which shortcut proves {prove}?", crit_, [c for c in ["SSS (with PR ≅ RP)", "ASA", "SAS (alternate interior angles, shared JL)", "AAS (shared WY)", "HL"] if c != crit_][:3], ["Identify the three pairs, including shared sides and angle relationships."], tags=["reasoning"])
for k_, (st_, rs_) in enumerate([("Given", "the first statements"), ("CPCTC", "a conclusion about parts after congruence"), ("Reflexive Property", "a shared side or angle"), ("Vertical Angles Theorem", "angles across intersecting lines")]):
    B.mc(9, "cp2", f"Which reason is usually used for {rs_}?", st_, [x for x in ["Given", "CPCTC", "Reflexive Property", "Vertical Angles Theorem"] if x != st_], ["Common proof reasons."], tags=["reasoning"])

B.sa(8, "cp1", "△ABC ≅ △XYZ. m∠A = 50° and m∠B = 70°. Find m∠Z.", "60°", ["m∠C = 180 - 120 = 60°; ∠Z ↔ ∠C."])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
