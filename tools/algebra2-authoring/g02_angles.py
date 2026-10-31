from lib import Bank, graph
from mathlite import *
from geofig import Fig, transversal
import math, random, itertools

STD = {1: ["G-CO.C.9"], 2: ["G-CO.C.9"], 3: ["G-CO.A.1"], 4: ["G-CO.C.9"], 5: ["G-CO.C.9"], 6: ["G-CO.C.9"], 7: ["G-CO.C.9", "A-CED.A.1"], 8: ["G-CO.C.9"], 9: ["G-GPE.B.5"]}
B = Bank("angles-parallel-lines", "ap", STD, course="geometry", prefix="geo")
R = random.Random(202)

# transversal model: angles 1–4 at the upper line (1 upper-right, 2 upper-left, 3 lower-left, 4 lower-right), 5–8 likewise at the lower line
POS = {1: "a1", 2: "a2", 3: "a3", 4: "a4", 5: "b1", 6: "b2", 7: "b3", 8: "b4"}
def pair_type(i, j):
    i, j = sorted((i, j)); qi, qj = (i - 1) % 4 + 1, (j - 1) % 4 + 1; same = (i <= 4) == (j <= 4)
    if same:
        return "vertical angles" if abs(qi - qj) == 2 else "a linear pair"
    if qi == qj: return "corresponding angles"
    if {qi, qj} == {3, 1} and qi == 3 or (qi, qj) == (4, 2): return "alternate interior angles"
    if (qi, qj) in ((1, 3), (2, 4)): return "alternate exterior angles"
    if (qi, qj) in ((3, 2), (4, 1)): return "same-side interior angles"
    if (qi, qj) in ((2, 3), (1, 4)): return "same-side exterior angles"
    return "none"
def congruent(i, j):  # with parallel lines
    return ((i - 1) % 4 + 1) % 2 == ((j - 1) % 4 + 1) % 2
TYPES = ["corresponding angles", "alternate interior angles", "alternate exterior angles", "same-side interior angles", "vertical angles", "a linear pair", "same-side exterior angles"]
assert sorted((i, j) for i, j in itertools.combinations(range(1, 9), 2) if pair_type(i, j) == "none") == [(1, 6), (2, 5), (3, 8), (4, 7)]
num_fig = transversal(B, "numbered", {POS[k]: str(k) for k in range(1, 9)}, "Two parallel lines (marked with arrows) cut by a transversal. At the upper intersection angles 1 (upper right), 2 (upper left), 3 (lower left), 4 (lower right); at the lower intersection angles 5, 6, 7, 8 in the same positions.")
nonpar = None

# ---- Skill 1: complementary / supplementary ----
S = 1
for a in [23, 58, 71.5, 40, 89]:
    B.mc(S, "cp2", f"Find the complement of a {a:g}° angle.", f"{90 - a:g}°", [f"{180 - a:g}°", f"{a:g}°", f"{90 + a:g}°"], ["Complementary angles sum to 90°."], tags=["misconception"])
for a in [35, 112, 90, 147.5, 8]:
    B.mc(S, "cp2", f"Find the supplement of a {a:g}° angle.", f"{180 - a:g}°", [f"{90 - a:g}°" if a < 90 else f"{a - 90:g}°", f"{a:g}°", f"{360 - a:g}°"], ["Supplementary angles sum to 180°."], tags=["misconception"])
for e1, e2, kind in [("(2x + 10)°", "(3x - 5)°", 90), ("(4x - 8)°", "(x + 13)°", 180), ("(x + 25)°", "(2x - 7)°", 90), ("(5x)°", "(3x + 4)°", 180), ("(7x + 2)°", "(2x - 2)°", 180)]:
    p1, p2 = linp(e1), linp(e2); xv = (kind - (p1 + p2).c[0]) / (p1 + p2).c[1]
    assert p1(xv) > 0 and p2(xv) > 0
    B.sa(S, "cp1", f"Two angles measuring {e1} and {e2} are {'complementary' if kind == 90 else 'supplementary'}. Find x and both angles.", f"x = {fr(xv)}; {fr(p1(xv))}° and {fr(p2(xv))}°", [f"Sum = {kind}°.", f"x = {fr(xv)}."])
for k_, kind in [(2, 90), (3, 180), (4, 90), (5, 180)]:
    small = F(kind, k_ + 1)
    B.sa(S, "cp1", f"An angle is {k_} times its {'complement' if kind == 90 else 'supplement'}. Find the angle.", f"{fr(k_ * small)}°", [f"x + {k_}x = {kind}.", f"x = {fr(small)}; angle = {fr(k_ * small)}°."])
B.sa(S, "honors", "The supplement of an angle is 20° more than three times its complement. Find the angle.", "55°", ["180 - x = 3(90 - x) + 20 → 2x = 110."], tags=["challenge"])
assert 180 - 55 == 3 * (90 - 55) + 20
B.sa(S, "honors", "Show that for any acute angle, its supplement exceeds its complement by 90°.", "(180 - x) - (90 - x) = 90", ["Write both in terms of x and subtract."], tags=["reasoning"])
B.sel(S, "cp1", "Select ALL pairs of complementary angle measures.", ["30° and 60°", "45° and 45°", "12.5° and 77.5°"], ["90° and 90°", "40° and 140°", "60° and 60°"], ["Sum must be 90°."])
B.sel(S, "honors", "Select ALL statements that are always true.", ["The supplement of an acute angle is obtuse", "Complements of congruent angles are congruent", "Two right angles are supplementary"], ["Supplementary angles are adjacent", "Every angle has a complement", "Two acute angles are complementary"], ["Only angles < 90° have complements; supplementary angles need not share a side."], tags=["reasoning"])
B.orq(S, "cp1", "∠A and ∠B are supplementary; ∠B and ∠C are complementary; m∠A = 128°.", [("Find m∠B.", "52°"), ("Find m∠C.", "38°"), ("Is ∠A obtuse?", "Yes"), ("Find the supplement of ∠C.", "142°")], ["180 - 128.", "90 - 52.", "> 90°.", "180 - 38."])
B.mc(S, "cp1", "A student says the complement of 110° is -20°. What is correct?", "110° has no complement; only acute angles do", ["-20°", "20°", "70°"], ["Angle measures are positive."], tags=["error-analysis", "misconception"])

# ---- Skill 2: vertical angles and linear pairs ----
S = 2
for i, a in enumerate([48, 115, 72]):
    fg = Fig(3.8, 3.0); t = math.radians(a)
    P1, P2, P3, P4 = (3, 0), (3 * math.cos(t), 3 * math.sin(t)), (-3, 0), (-3 * math.cos(t), -3 * math.sin(t))
    fg.line(P3, P1, ext=0.0); fg.line(P4, P2, ext=0.0); fg.dot((0, 0), None)
    fg.angle((0, 0), P1, P2, f"{a}°", r=0.7); fg.angle((0, 0), P2, P3, "1", r=0.7); fg.angle((0, 0), P3, P4, "2", r=0.7); fg.angle((0, 0), P4, P1, "3", r=0.7)
    dg = fg.save(B, f"s02-cross-{i}", f"Two intersecting lines forming four angles: the labeled angle is {a}°, then going counterclockwise angles 1, 2, and 3.")
    B.orq(S, "cp2" if i == 0 else "cp1", "Two lines intersect as shown.", [("Find m∠1.", f"{180 - a}°"), ("Find m∠2.", f"{a}°"), ("Find m∠3.", f"{180 - a}°"), ("Name a pair of vertical angles.", "∠1 and ∠3 (or the given angle and ∠2)")],
          ["Linear pair with the given angle.", "Vertical to the given angle.", "Vertical to ∠1.", "Opposite angles."], diagram=dg, tags=["graph"])
    B.sel(S, "cp1", "Use the figure. Select ALL true statements.", [f"m∠2 = {a}°", "∠1 and ∠3 are vertical angles", "∠1 and ∠2 form a linear pair"], [f"m∠1 = {a}°", "∠2 and ∠3 are vertical angles", f"m∠3 = {90 - a if a < 90 else a - 90}°"], ["Vertical angles are congruent; linear pairs are supplementary."], diagram=dg, tags=["graph"])
for e1, e2, kind in [("(3x + 12)°", "(5x - 20)°", "vertical"), ("(2x + 30)°", "(4x)°", "linear"), ("(6x - 11)°", "(4x + 9)°", "vertical"), ("(x + 40)°", "(3x - 20)°", "linear"), ("(9x - 4)°", "(7x + 10)°", "vertical")]:
    p1, p2 = linp(e1), linp(e2)
    if kind == "vertical": xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]); ok = p1(xv) == p2(xv)
    else: xv = (180 - (p1 + p2).c[0]) / (p1 + p2).c[1]; ok = p1(xv) + p2(xv) == 180
    assert ok and 0 < p1(xv) < 180 and 0 < p2(xv) < 180
    B.sa(S, "cp1", f"Two angles are {'vertical angles' if kind == 'vertical' else 'a linear pair'} with measures {e1} and {e2}. Find x and the angle measures.", f"x = {fr(xv)}; {fr(p1(xv))}° and {fr(p2(xv))}°",
         ["Vertical angles are congruent." if kind == "vertical" else "A linear pair is supplementary.", f"x = {fr(xv)}."])
B.mc(S, "cp1", "Which must be true of a linear pair?", "The angles are adjacent and supplementary", ["The angles are congruent", "The angles are complementary", "The angles are vertical"], ["Adjacent with noncommon sides forming a line."])
B.mc(S, "cp1", "A student says any two supplementary angles form a linear pair. Which is a counterexample?", "Two non-adjacent angles of 100° and 80°", ["Two adjacent 90° angles on a line", "Angles of 120° and 60° sharing a side on a line", "There is none"], ["A linear pair must be adjacent."], tags=["misconception", "reasoning"])
B.sel(S, "honors", "Two lines intersect and one angle is 4 times another adjacent angle. Select ALL angle measures that appear.", ["36°", "144°"], ["45°", "90°", "135°", "72°"], ["x + 4x = 180 → x = 36; vertical angles repeat the two measures."], tags=["reasoning"])
B.orq(S, "honors", "Prove the Vertical Angles Theorem for ∠1 and ∠3 formed by intersecting lines (∠2 between them).", [("Relate ∠1 and ∠2.", "linear pair: m∠1 + m∠2 = 180°"), ("Relate ∠2 and ∠3.", "linear pair: m∠2 + m∠3 = 180°"), ("Combine.", "m∠1 + m∠2 = m∠2 + m∠3 (substitution/transitive)"), ("Conclude.", "m∠1 = m∠3 (subtraction), so ∠1 ≅ ∠3")], ["Linear Pair Postulate.", "Linear Pair Postulate.", "Both equal 180°.", "Subtract m∠2."], tags=["reasoning"])
B.sa(S, "cp2", "Two vertical angles: one measures 63°. Find the other.", "63°", ["Congruent."])
B.sa(S, "cp2", "Two angles form a linear pair; one is 141°. Find the other.", "39°", ["180 - 141."])

# ---- Skill 3: parallel and perpendicular lines ----
S = 3
for q, a, w in [("Two coplanar lines that never intersect are…", "parallel", ["perpendicular", "skew", "intersecting"]), ("Two lines that intersect at a right angle are…", "perpendicular", ["parallel", "skew", "oblique"]),
                ("Two noncoplanar lines that never intersect are…", "skew", ["parallel", "perpendicular", "concurrent"]), ("What does the symbol ∥ mean?", "is parallel to", ["is perpendicular to", "is congruent to", "is similar to"]),
                ("What does the symbol ⊥ mean?", "is perpendicular to", ["is parallel to", "is congruent to", "is a bisector of"]), ("Through a point not on a line, how many lines are parallel to the line?", "exactly one", ["none", "two", "infinitely many"])]:
    B.mc(S, "cp2", q, a, w, ["Definitions and the Parallel Postulate."])
for st, ok in [("If two coplanar lines are perpendicular to the same line, then they are parallel.", True), ("If two lines are parallel to the same line, then they are parallel to each other.", True), ("If two lines are perpendicular, they form four right angles.", True),
               ("If two lines do not intersect, they are parallel.", False), ("A line perpendicular to one of two parallel lines (in their plane) is perpendicular to the other.", True), ("Two lines perpendicular to the same plane are perpendicular to each other.", False)]:
    B.mc(S, "cp1" if ok else "honors", f"True or false: {st}", "True" if ok else "False", ["False" if ok else "True", "Only if the lines are horizontal", "Cannot be determined"], ["Use theorems about parallel and perpendicular lines." if ok else "Counterexample: skew lines do not intersect; two lines ⊥ to a plane are parallel."], tags=["reasoning"])
B.sel(S, "cp1", "Line m ⊥ line n at point P. Select ALL true statements.", ["Four right angles are formed at P", "Each angle at P measures 90°", "Adjacent angles at P are congruent"], ["m ∥ n", "m and n are skew", "Only one angle at P is 90°"], ["Perpendicular lines form four right angles."])
B.sel(S, "honors", "In a cube, edge AB is given. Select ALL edges that are perpendicular to AB and intersect it.", ["AD", "BC", "AE", "BF"], ["CG", "EF", "DC"], ["Edges meeting AB at A or B at right angles."], tags=["reasoning"])
B.orq(S, "cp1", "Lines a, b, c are coplanar. a ∥ b and c ⊥ a.", [("How is c related to b?", "c ⊥ b"), ("How many right angles are formed where c meets a and b?", "8"), ("If d ⊥ c also, how is d related to a?", "d ∥ a (or d = a)"), ("Draw a conclusion about a, b, d.", "all parallel (or coincide)")], ["Perpendicular Transversal Theorem.", "4 at each intersection.", "Two lines ⊥ same line are ∥.", "Transitive."], tags=["reasoning"])
B.sa(S, "cp1", "The distance between two parallel lines is measured along which kind of segment?", "a segment perpendicular to both lines", ["Shortest distance."])
B.sa(S, "cp2", "Name the relationship between the floor and ceiling lines along the same wall.", "parallel", ["They never meet and lie in one plane (the wall)."])
B.sa(S, "honors", "What is the distance between the lines y = 3 and y = -2?", "5", ["Vertical distance between horizontal lines."])
B.mc(S, "cp1", "Which statement is the Parallel Postulate?", "Through a point not on a line there is exactly one line parallel to the given line", ["Parallel lines form congruent angles", "All parallel lines are horizontal", "Two lines perpendicular to a third are parallel"], ["Euclid's fifth postulate (Playfair form)."])
B.mc(S, "cp2", "Two lines meet to form a 90° angle. What are they?", "perpendicular", ["parallel", "skew", "collinear"], ["Definition."])

# ---- Skills 4–6: identifying and using angle pairs ----
pairs = list(itertools.combinations(range(1, 9), 2)); R.shuffle(pairs)
cnt = {4: 0}
for i, j in pairs:
    t_ = pair_type(i, j)
    if t_ == "none": continue
    if t_ in ("vertical angles", "a linear pair") and cnt[4] > 4: continue
    if cnt[4] >= 14: break
    cnt[4] += 1
    B.mc(4, "cp2" if t_ in ("corresponding angles", "vertical angles", "a linear pair") else "cp1", f"Use the figure. ∠{i} and ∠{j} are…", t_, [x for x in TYPES if x != t_][:3],
         ["Corresponding: same position at each intersection. Alternate: opposite sides of the transversal. Interior: between the lines."], diagram=num_fig, tags=["graph"])
for kind in ["alternate interior angles", "corresponding angles", "same-side interior angles", "alternate exterior angles"]:
    right = [f"∠{i} and ∠{j}" for i, j in itertools.combinations(range(1, 9), 2) if pair_type(i, j) == kind]
    wrong = [f"∠{i} and ∠{j}" for i, j in itertools.combinations(range(1, 9), 2) if pair_type(i, j) != kind][:3]
    B.sel(4, "cp1", f"Use the figure. Select ALL pairs of {kind}.", right, R.sample(wrong + [f"∠{a} and ∠{b}" for a, b in [(1, 8), (2, 5)] if pair_type(a, b) != kind], 3), ["Locate each angle by intersection and position."], diagram=num_fig, tags=["graph"])
B.mc(4, "cp1", "What is a transversal?", "A line that intersects two or more coplanar lines at different points", ["A line parallel to two lines", "A line perpendicular to a plane", "The segment between two parallel lines"], ["Definition."])
B.orq(4, "cp1", "Use the figure.", [("Name the angle corresponding to ∠2.", "∠6"), ("Name the angle alternate interior to ∠4.", "∠6"), ("Name the angle alternate exterior to ∠1.", "∠7"), ("Name the angle same-side interior to ∠3.", "∠6")], ["Same position.", "Opposite sides, between the lines.", "Opposite sides, outside.", "Same side, between."], diagram=num_fig, tags=["graph"])
assert pair_type(2, 6) == "corresponding angles" and pair_type(4, 6) == "alternate interior angles" and pair_type(1, 7) == "alternate exterior angles" and pair_type(3, 6) == "same-side interior angles"
B.sa(4, "cp1", "Two lines cut by a transversal form 8 angles. How many pairs of corresponding angles are there?", "4", ["One pair for each position."])
B.sa(4, "honors", "Three parallel lines are cut by one transversal. How many angles are formed, and how many pairs of corresponding angles?", "12 angles; 12 pairs (4 positions × 3 pairs of lines)", ["Each pair of lines gives 4 corresponding pairs; there are C(3, 2) = 3 pairs."], tags=["challenge"])
for S, kinds in [(5, ["corresponding angles", "alternate interior angles"]), (6, ["alternate exterior angles", "same-side interior angles"])]:
    for kind in kinds:
        ex = [(i, j) for i, j in itertools.combinations(range(1, 9), 2) if pair_type(i, j) == kind]
        for k_, (i, j) in enumerate(ex[:3]):
            base = R.choice([47, 58, 63, 72, 115, 124, 131])
            # measure of angle i: angles 1,3,5,7 share one measure, 2,4,6,8 the other
            m_i = base if (i % 2 == 1) else 180 - base
            m_j = m_i if congruent(i, j) else 180 - m_i
            B.sa(S, "cp2" if k_ == 0 else "cp1", f"Use the figure (the lines are parallel). m∠{i} = {m_i}°. Find m∠{j} and name the relationship.", f"{m_j}°; {kind}",
                 [f"∠{i} and ∠{j} are {kind}.", "Congruent." if congruent(i, j) else "Supplementary (same-side interior/exterior)."], diagram=num_fig, tags=["graph"])
        e1, e2 = R.choice([("(3x + 15)°", "(5x - 25)°"), ("(4x - 10)°", "(2x + 30)°"), ("(6x + 2)°", "(8x - 18)°")])
        p1, p2 = linp(e1), linp(e2)
        if kind == "same-side interior angles":
            xv = (180 - (p1 + p2).c[0]) / (p1 + p2).c[1]
        else:
            xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
        assert 0 < p1(xv) < 180 and 0 < p2(xv) < 180
        B.sa(S, "cp1", f"Two parallel lines are cut by a transversal. A pair of {kind} measure {e1} and {e2}. Find x and both angles.", f"x = {fr(xv)}; {fr(p1(xv))}° and {fr(p2(xv))}°",
             ["Same-side interior angles are supplementary." if kind == "same-side interior angles" else f"{kind.capitalize()} are congruent.", f"x = {fr(xv)}."])
    B.mc(S, "cp1", f"If parallel lines are cut by a transversal, {kinds[0]} are…", "congruent" if kinds[0] != "same-side interior angles" else "supplementary", ["supplementary", "complementary", "always right angles"], ["Parallel line angle theorems."])
    B.mc(S, "cp1", f"If parallel lines are cut by a transversal, {kinds[1]} are…", "congruent" if kinds[1] != "same-side interior angles" else "supplementary", ["congruent" if kinds[1] == "same-side interior angles" else "supplementary", "complementary", "always acute"], ["Parallel line angle theorems."], tags=["misconception"])
for S in (5, 6):
    base = 66 if S == 5 else 109
    dg = transversal(B, f"s0{S}-values", {"a1": f"{base}°", "a3": "x°", "b2": "y°", "b4": "z°"}, f"Parallel lines cut by a transversal. Upper-right angle at the top intersection is {base}°; x is lower-left at the top; y upper-left and z lower-right at the bottom intersection.")
    B.orq(S, "cp1", "The lines are parallel.", [("Find x.", f"{base}"), ("Find y.", f"{180 - base}"), ("Find z.", f"{180 - base}"), ("Which relationship justifies y?", "y and x are same-side interior angles (supplementary)")],
          ["Vertical angles.", "x and y are same-side interior: 180 - x.", "z is vertical to y.", "Same-side Interior Angles Theorem."], diagram=dg, tags=["graph"])
    assert pair_type(3, 6) == "same-side interior angles"
B.sel(5, "honors", "Lines p ∥ q are cut by transversal t; m∠1 = 70° (upper right at p). Select ALL angles that measure 70°.", ["∠3", "∠5", "∠7"], ["∠2", "∠4", "∠6", "∠8"], ["Vertical (∠3), corresponding (∠5), and its vertical angle (∠7)."], diagram=num_fig, tags=["graph"])
B.sel(6, "honors", "Use the figure with parallel lines. Select ALL angles supplementary to ∠2.", ["∠1", "∠3", "∠5", "∠7"], ["∠4", "∠6", "∠8"], ["Odd-numbered angles share one measure and even-numbered the other; the two measures sum to 180°."], diagram=num_fig, tags=["graph"])
B.mc(5, "cp1", "A student says corresponding angles are always congruent. What condition is missing?", "The lines cut by the transversal must be parallel", ["The transversal must be perpendicular", "The angles must be acute", "Nothing is missing"], ["The theorem needs parallel lines."], tags=["misconception"])
B.mc(6, "honors", "Same-side interior angles measure (2x)° and (3x)° with parallel lines. Which is true?", "x = 36; the angles are 72° and 108°", ["x = 36; both are 108°", "x = 18; 36° and 54°", "No solution"], ["2x + 3x = 180."], tags=["multistep"])

# ---- Skill 7: algebraic angle relationships ----
S = 7
templates = [("vertical angles", "eq"), ("a linear pair", "sup"), ("corresponding angles (lines parallel)", "eq"), ("alternate interior angles (lines parallel)", "eq"), ("same-side interior angles (lines parallel)", "sup"), ("complementary angles", "comp"), ("alternate exterior angles (lines parallel)", "eq")]
made = 0
for (rel_, kind), (a1, b1, a2, b2) in zip(templates * 3, [(3, 8, 5, -20), (2, 14, 4, -2), (7, -6, 5, 14), (4, 9, 6, -11), (3, 12, 2, 18), (2, 5, 3, 10), (8, -12, 5, 21), (5, 3, 3, 25), (6, -4, 4, 12), (9, 1, 7, 15), (5, 10, 7, -6), (3, 4, 2, 26), (11, -7, 6, 33), (2, 16, 6, -8)]):
    e1 = f"({a1}x {'+' if b1 >= 0 else '-'} {abs(b1)})°"; e2 = f"({a2}x {'+' if b2 >= 0 else '-'} {abs(b2)})°"
    p1, p2 = linp(e1), linp(e2); tgt = {"sup": 180, "comp": 90}.get(kind)
    xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]) if kind == "eq" else (tgt - (p1 + p2).c[0]) / (p1 + p2).c[1]
    if not (0 < p1(xv) < 180 and 0 < p2(xv) < 180) or p1.c[1] == p2.c[1] and kind == "eq": continue
    if xv.denominator != 1: continue
    made += 1
    B.sa(S, "cp1" if made % 3 else "honors", f"Angles measuring {e1} and {e2} are {rel_}. Find x and the angle measures.", f"x = {fr(xv)}; {fr(p1(xv))}° and {fr(p2(xv))}°",
         [{"eq": "The angles are congruent: set the expressions equal.", "sup": "The angles are supplementary: sum = 180°.", "comp": "Sum = 90°."}[kind], f"x = {fr(xv)}.", "Substitute to find each angle."])
B.orq(S, "honors", "Parallel lines cut by a transversal form corresponding angles (4x + y)° and 110°, and same-side interior angles (3x - y)° and 110°.", [("Write an equation from the corresponding angles.", "4x + y = 110"), ("Write an equation from the same-side interior angles.", "3x - y = 70"), ("Solve the system.", "x = 180/7, y = 50/7"), ("Check by finding both angles.", "110° and 70°")],
      ["Congruent.", "Supplementary: 180 - 110.", "Add: 7x = 180.", "Substitute."], tags=["challenge"])
assert 4 * F(180, 7) + F(50, 7) == 110 and 3 * F(180, 7) - F(50, 7) == 70
B.orq(S, "honors", "Two parallel lines are cut by a transversal. Alternate interior angles measure (x² - 10)° and (3x + 18)°.", [("Write an equation.", "x² - 10 = 3x + 18"), ("Solve.", "x = 7 or x = -4"), ("Find the angle for each x.", "x = 7: 39°; x = -4: 6°"), ("Are both valid?", "Yes: both give positive measures less than 180°")], ["Congruent angles.", "x² - 3x - 28 = 0.", "Substitute.", "Check."], tags=["challenge"])
B.sel(S, "cp1", "Angles (3x + 5)° and (5x - 15)° are congruent. Select ALL true statements.", ["x = 10", "Each angle is 35°", "The angles could be vertical angles"], ["x = 2.5", "The angles are supplementary", "Each angle is 90°"], ["3x + 5 = 5x - 15 → x = 10."])
B.mc(S, "cp1", "A student solves same-side interior angles (2x + 20)° and (3x - 10)° by setting them equal and gets x = 30. What is wrong?", "Same-side interior angles are supplementary: 5x + 10 = 180, x = 34", ["Nothing", "They should be complementary", "x should be 20"], ["Equal only for alternate/corresponding pairs."], tags=["error-analysis"])
B.sa(S, "cp2", "Two vertical angles measure (x + 15)° and 50°. Find x.", "35", ["x + 15 = 50."])

# ---- Skill 8: proving lines parallel ----
S = 8
for m1, m2, rel_, ok in [(64, 64, "corresponding", True), (72, 108, "alternate interior", False), (85, 95, "same-side interior", True), (118, 118, "alternate exterior", True), (70, 70, "same-side interior", False), (101, 79, "corresponding", False)]:
    yes = (m1 == m2) if rel_ != "same-side interior" else (m1 + m2 == 180)
    assert yes == ok
    B.mc(S, "cp1", f"{rel_.capitalize()} angles formed by lines ℓ and m and a transversal measure {m1}° and {m2}°. Are ℓ and m parallel?", f"{'Yes' if ok else 'No'}, by the {'converse of the ' + rel_.title() + ' Angles Theorem' if ok else 'fact that the converse condition fails'}",
         [f"{'No' if ok else 'Yes'}, because the angles {'are' if not ok else 'are not'} congruent", "Cannot be determined without a diagram", f"{'Yes' if ok else 'No'}, because vertical angles are congruent"],
         ["Converse theorems: corresponding/alternate congruent, or same-side interior supplementary → parallel."])
for e1, e2, rel_ in [("(2x + 18)°", "(4x - 12)°", "corresponding"), ("(5x - 7)°", "(3x + 27)°", "alternate interior"), ("(3x + 20)°", "(2x + 10)°", "same-side interior")]:
    p1, p2 = linp(e1), linp(e2)
    xv = (180 - (p1 + p2).c[0]) / (p1 + p2).c[1] if rel_ == "same-side interior" else (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.sa(S, "cp1", f"{rel_.capitalize()} angles measure {e1} and {e2}. For what x are the lines parallel?", f"x = {fr(xv)}", [f"Set the angles {'supplementary' if 'same-side' in rel_ else 'congruent'}.", f"x = {fr(xv)}."])
    assert 0 < p1(xv) < 180
B.sel(S, "cp1", "Select ALL conditions that prove two lines cut by a transversal are parallel.", ["Corresponding angles are congruent", "Alternate interior angles are congruent", "Same-side interior angles are supplementary", "Both lines are perpendicular to the transversal"],
      ["Vertical angles are congruent", "Same-side interior angles are congruent (and not right)", "A linear pair is supplementary"], ["Converse theorems; vertical angles and linear pairs are always true and prove nothing."], tags=["reasoning"])
B.orq(S, "honors", "Given ∠1 ≅ ∠2, where ∠1 and ∠2 are alternate exterior angles for lines ℓ and m. Prove ℓ ∥ m.", [("Statement 2 and reason.", "∠1 ≅ ∠3; Vertical Angles Theorem (∠3 is vertical to ∠1)"), ("Statement 3 and reason.", "∠3 ≅ ∠2; Transitive Property"), ("What kind of angles are ∠3 and ∠2?", "corresponding angles"), ("Conclude.", "ℓ ∥ m; Converse of the Corresponding Angles Postulate")],
      ["Vertical angles.", "Transitive.", "Same position.", "Converse."], tags=["reasoning"])
B.orq(S, "cp1", "Use the figure. Which angle facts would show the lines are parallel?", [("A corresponding pair to check.", "∠1 and ∠5"), ("An alternate interior pair to check.", "∠4 and ∠6 (or ∠3 and ∠5)"), ("A same-side interior pair to check.", "∠3 and ∠6 (or ∠4 and ∠5)"), ("If m∠3 = 75° and m∠6 = 105°, are they parallel?", "Yes: same-side interior angles are supplementary")],
      ["Same position.", "Opposite sides, between.", "Same side, between.", "75 + 105 = 180."], diagram=num_fig, tags=["graph", "reasoning"])
assert pair_type(4, 6) == "alternate interior angles" and pair_type(3, 5) == "alternate interior angles" and pair_type(4, 5) == "same-side interior angles"
B.mc(S, "cp1", "Which theorem proves lines parallel when alternate interior angles are congruent?", "Converse of the Alternate Interior Angles Theorem", ["Alternate Interior Angles Theorem", "Vertical Angles Theorem", "Linear Pair Postulate"], ["Using the angle fact to conclude parallelism is a converse."], tags=["misconception"])
B.sa(S, "cp2", "If corresponding angles are congruent, what can you conclude about the lines?", "they are parallel", ["Converse of Corresponding Angles Postulate."])
B.sa(S, "honors", "Lines a and b are both perpendicular to line c in a plane. Which converse theorem proves a ∥ b?", "Converse of the Corresponding Angles Postulate (corresponding right angles are congruent)", ["All four corresponding angles are 90°."], tags=["reasoning"])

# ---- Skill 9: slopes ----
S = 9
for m in [F(2, 3), F(-4), F(1, 5), F(-3, 2), F(0)]:
    B.mc(S, "cp2", f"A line has slope {fr(m)}. What is the slope of a line parallel to it, and of a line perpendicular to it?", f"parallel {fr(m)}; perpendicular {'undefined' if m == 0 else fr(-1 / m)}",
         [f"parallel {fr(m)}; perpendicular {fr(-m)}", f"parallel {'undefined' if m == 0 else fr(-1 / m)}; perpendicular {fr(m)}", f"parallel {fr(-m) if m else '1'}; perpendicular {'0' if m else '1'}"], ["Parallel: equal slopes. Perpendicular: negative reciprocals (horizontal ⊥ vertical)."], tags=["misconception"])
for (m, b), (px, py), kind in [((2, -1), (3, 4), "parallel"), ((F(-1, 3), 5), (2, -3), "perpendicular"), ((F(3, 4), 0), (-4, 1), "perpendicular"), ((-5, 2), (0, 7), "parallel")]:
    mm = F(m) if kind == "parallel" else -1 / F(m); bb = py - mm * px
    B.sa(S, "cp1", f"Write an equation of the line through {pt(px, py)} that is {kind} to y = {pstr(P([F(b), F(m)]))}.", f"y = {pstr(P([bb, mm]))}", [f"Slope {fr(mm)}.", f"b = {py} - ({fr(mm)})({px}) = {fr(bb)}."])
for l1, l2, rel_ in [("y = 3x + 1", "6x - 2y = 8", "parallel"), ("y = -2x + 5", "x - 2y = 4", "perpendicular"), ("2x + 3y = 6", "3x + 2y = 6", "neither"), ("y = 4", "x = -1", "perpendicular"), ("y = (1/2)x", "y = 0.5x - 7", "parallel")]:
    B.mc(S, "cp1", f"Are the lines {l1} and {l2} parallel, perpendicular, or neither?", rel_, [r for r in ["parallel", "perpendicular", "neither", "the same line"] if r != rel_], ["Rewrite in slope-intercept form and compare slopes."])
for A_, B_, C_, D_ in [((0, 0), (4, 2), (1, 5), (5, 7)), ((1, 1), (3, 5), (-2, 4), (6, 0)), ((-3, 2), (1, 0), (2, 6), (4, 3))]:
    m1 = F(B_[1] - A_[1], B_[0] - A_[0]); m2 = F(D_[1] - C_[1], D_[0] - C_[0])
    rel_ = "parallel" if m1 == m2 else ("perpendicular" if m1 * m2 == -1 else "neither")
    B.sa(S, "cp1", f"Is line AB through A{pt(*A_)} and B{pt(*B_)} parallel, perpendicular, or neither to line CD through C{pt(*C_)} and D{pt(*D_)}?", f"{rel_} (slopes {fr(m1)} and {fr(m2)})", ["Compute both slopes and compare."])
dg = graph(B, "s09-lines", [(lambda v: 0.5 * v + 2, {}), (lambda v: -2 * v + 1, {"color": "#c0392b"}), (lambda v: 0.5 * v - 3, {"color": "#555555", "ls": "--"})], alt="Three lines: blue y = (1/2)x + 2, red y = -2x + 1, and gray dashed y = (1/2)x - 3.")
B.sel(S, "cp1", "Use the graph. Select ALL true statements.", ["The blue and dashed lines are parallel", "The red line is perpendicular to the blue line", "The red line is perpendicular to the dashed line"], ["The blue and red lines are parallel", "All three lines meet at one point"], ["Slopes 1/2, -2, 1/2: equal → parallel; product -1 → perpendicular."], diagram=dg, tags=["graph"])
B.orq(S, "honors", "Quadrilateral ABCD: A(0, 0), B(4, 1), C(5, 5), D(1, 4).", [("Find the slopes of AB and DC.", "1/4 and 1/4"), ("Find the slopes of BC and AD.", "4 and 4"), ("Is ABCD a parallelogram? Why?", "Yes: both pairs of opposite sides are parallel"), ("Are adjacent sides perpendicular?", "No: (1/4)(4) = 1, not -1")], ["Δy/Δx.", "Δy/Δx.", "Opposite slopes equal.", "Product of slopes."], tags=["connections"])
B.mc(S, "cp1", "A student says lines with slopes 3 and -3 are perpendicular. What is correct?", "Perpendicular slopes multiply to -1, so the perpendicular slope is -1/3", ["Correct", "They are parallel", "They are the same line"], ["3 · (-3) = -9 ≠ -1."], tags=["error-analysis", "misconception"])
B.sa(S, "honors", "Find k so the line through (1, k) and (4, 7) is perpendicular to y = 3x - 2.", "k = 8", ["Slope must be -1/3: (7 - k)/3 = -1/3 → 7 - k = -1."], tags=["challenge"])
B.sa(S, "cp2", "What is the slope of a line perpendicular to a vertical line?", "0", ["Horizontal."])

# ================= additions: generated variety =================
R2 = random.Random(2022)
skill_of = {"corresponding angles": 5, "alternate interior angles": 5, "alternate exterior angles": 6, "same-side interior angles": 6, "same-side exterior angles": 6, "vertical angles": 2, "a linear pair": 2}
allp = [(i, j) for i, j in itertools.combinations(range(1, 9), 2) if pair_type(i, j) != "none"]
for rep in range(2):
    for i, j in allp:
        t_ = pair_type(i, j); S_ = skill_of[t_]
        if S_ == 2 and rep == 1: continue
        base = R2.choice([38, 44, 52, 61, 67, 73, 79, 101, 108, 116, 123, 134, 142])
        m_i = base if i % 2 else 180 - base; m_j = m_i if congruent(i, j) else 180 - m_i
        if rep == 0:
            B.mc(S_, "cp2" if t_ in ("corresponding angles", "vertical angles") else "cp1", f"Use the figure (lines parallel). m∠{i} = {m_i}°. Find m∠{j}.", f"{m_j}°", [f"{180 - m_j}°", f"{90 - m_j if m_j < 90 else m_j - 90}°", f"{m_i + 10}°" if m_i + 10 != m_j else f"{m_i - 10}°"],
                 [f"∠{i} and ∠{j} are {t_}.", "Congruent." if congruent(i, j) else "Supplementary."], diagram=num_fig, tags=["graph"])
        elif R2.random() < 0.55:
            e1 = R2.choice(["(2x + 10)°", "(3x - 5)°", "(4x + 2)°", "(5x - 12)°"])
            p1 = linp(e1); xv = (m_i - p1.c[0]) / p1.c[1]
            B.sa(S_, "cp1" if xv.denominator == 1 else "honors", f"Use the figure (lines parallel). m∠{i} = {e1} and m∠{j} = {m_j}°. Find x.", f"x = {fr(xv)}",
                 [f"∠{i} and ∠{j} are {t_}, so m∠{i} = {m_i}°.", f"{e1.strip('°')} = {m_i} → x = {fr(xv)}."], diagram=num_fig, tags=["graph"])
alt_fig = transversal(B, "lettered", {"a1": "b", "a2": "a", "a3": "d", "a4": "c", "b1": "f", "b2": "e", "b3": "h", "b4": "g"}, "Two parallel lines cut by a steep transversal with angles lettered: at the upper intersection a (upper left), b (upper right), c (lower right), d (lower left); at the lower intersection e, f, g, h in the same positions.", slope_deg=75)
L2N = {"b": 1, "a": 2, "d": 3, "c": 4, "f": 5, "e": 6, "h": 7, "g": 8}
for x_, y_ in [("a", "e"), ("d", "f"), ("c", "e"), ("b", "h"), ("d", "e"), ("a", "g"), ("c", "f"), ("b", "g")]:
    t_ = pair_type(L2N[x_], L2N[y_])
    if t_ == "none": continue
    B.mc(4, "cp1", f"Use the lettered figure. ∠{x_} and ∠{y_} are…", t_, [k for k in TYPES if k != t_][:3], ["Locate each angle by intersection and position."], diagram=alt_fig, tags=["graph"])
B.sel(4, "honors", "Use the lettered figure. Select ALL angles congruent to ∠a.", ["∠c", "∠e", "∠g"], ["∠b", "∠d", "∠f", "∠h"], ["∠a ↔ position 2; congruent angles are in positions 2 and 4 at each line."], diagram=alt_fig, tags=["graph"])
for e1, e2, rel_, tgt in [("(3x + 7)°", "(2x + 18)°", "vertical", "eq"), ("(5x - 6)°", "(4x + 6)°", "a linear pair", "sup"), ("(x + 52)°", "(3x)°", "vertical", "eq"), ("(6x + 1)°", "(3x + 8)°", "a linear pair", "sup"), ("(7x - 20)°", "(4x + 13)°", "vertical", "eq"), ("(2x)°", "(8x)°", "a linear pair", "sup")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]) if tgt == "eq" else (180 - (p1 + p2).c[0]) / (p1 + p2).c[1]
    assert 0 < p1(xv) < 180 and 0 < p2(xv) < 180
    B.mc(2, "cp1", f"Angles measuring {e1} and {e2} are {'vertical angles' if rel_ == 'vertical' else rel_}. Find x.", f"x = {fr(xv)}", [f"x = {fr((p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]))}" if tgt == "sup" and p1.c[1] != p2.c[1] else f"x = {fr((180 - (p1 + p2).c[0]) / (p1 + p2).c[1])}", f"x = {fr(xv + 2)}", f"x = {fr(xv * 2)}"],
         ["Vertical angles are congruent; a linear pair is supplementary.", f"x = {fr(xv)}."], tags=["misconception"])
for e in ["(4x + 10)°", "(2x - 30)°", "(x + 35)°"]:
    p1 = linp(e)
    B.sa(1, "cp1", f"An angle measuring {e} is supplementary to a 95° angle. Find x.", f"x = {fr((85 - p1.c[0]) / p1.c[1])}", ["Supplementary angles sum to 180°: the angle is 85°.", "Solve."])
B.sel(1, "cp1", "∠1 and ∠2 are complementary, and ∠2 and ∠3 are complementary. Select ALL true statements.", ["∠1 ≅ ∠3", "∠1 and ∠3 are both acute"], ["∠1 and ∠3 are supplementary", "∠2 is obtuse"], ["Congruent Complements Theorem."], tags=["reasoning"])
for S_, items_ in [(3, [("In the coordinate plane, which line is parallel to the x-axis?", "y = 4", ["x = 4", "y = 4x", "y = -x"]), ("Which line is perpendicular to y = 2?", "x = -3", ["y = -2", "y = 2x", "y = x + 2"]),
                        ("Lines ℓ ∥ m and m ∥ n. How are ℓ and n related?", "ℓ ∥ n", ["ℓ ⊥ n", "ℓ and n are skew", "Cannot tell"]), ("Lines ℓ ⊥ m and m ⊥ n (all coplanar). How are ℓ and n related?", "ℓ ∥ n", ["ℓ ⊥ n", "ℓ = m", "ℓ and n intersect at 45°"]),
                        ("In a plane, how many lines can be drawn through a point P perpendicular to a given line?", "exactly one", ["none", "two", "infinitely many"]), ("Railroad rails are a model of…", "parallel lines", ["perpendicular lines", "skew lines", "intersecting lines"]),
                        ("Two walls of a room meet along a vertical edge. The two floor edges of those walls are…", "perpendicular lines", ["parallel lines", "skew lines", "the same line"]), ("A road overpass and the highway under it (not parallel) model…", "skew lines", ["parallel lines", "perpendicular lines", "collinear lines"])])]:
    for q, a, w in items_:
        B.mc(S_, "cp1", q, a, w, ["Use definitions of parallel, perpendicular, and skew lines."])
B.sel(3, "cp1", "Select ALL true statements about parallel lines in a plane.", ["They have no points in common", "They are everywhere the same distance apart", "A transversal perpendicular to one is perpendicular to the other"], ["They intersect at one point", "They must be horizontal"], ["Definition and Perpendicular Transversal Theorem."])
B.orq(3, "honors", "Lines y = x + 1 and y = x - 3.", [("Are they parallel? Why?", "Yes: both have slope 1"), ("Find the line through (0, 1) perpendicular to both.", "y = -x + 1"), ("Find where it meets y = x - 3.", "(2, -1)"), ("Find the distance between the parallel lines.", "2√2")], ["Equal slopes.", "Slope -1.", "-x + 1 = x - 3.", "Distance from (0, 1) to (2, -1)."], tags=["challenge", "connections"])
made = 0
for a1, b1, a2, b2 in itertools.product([2, 3, 4, 5, 7], [-9, 5, 12, 20], [1, 3, 6, 8], [-14, 4, 16, 30]):
    if made >= 8: break
    if R2.random() < 0.7: continue
    kind = R2.choice(["eq", "sup"])
    e1 = f"({a1}x {'+' if b1 >= 0 else '-'} {abs(b1)})°"; e2 = f"({a2}x {'+' if b2 >= 0 else '-'} {abs(b2)})°"; p1, p2 = linp(e1), linp(e2)
    if kind == "eq" and a1 == a2: continue
    xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]) if kind == "eq" else (180 - (p1 + p2).c[0]) / (p1 + p2).c[1]
    if xv.denominator != 1 or not (5 < p1(xv) < 175 and 5 < p2(xv) < 175): continue
    rel_ = R2.choice(["alternate interior angles", "corresponding angles", "alternate exterior angles"]) if kind == "eq" else "same-side interior angles"
    made += 1
    B.orq(7, "cp1" if made % 2 else "honors", f"Parallel lines are cut by a transversal. Two {rel_} measure {e1} and {e2}.", [("Write an equation.", f"{e1.strip('°()')} {'=' if kind == 'eq' else '+'} {e2.strip('°()')}{'' if kind == 'eq' else ' = 180'}"), ("Solve for x.", f"x = {fr(xv)}"), ("Find both angle measures.", f"{fr(p1(xv))}° and {fr(p2(xv))}°"), ("Check your answer.", "the angles are equal" if kind == "eq" else f"{fr(p1(xv))} + {fr(p2(xv))} = 180")],
          ["Congruent pair." if kind == "eq" else "Supplementary pair.", "Solve the linear equation.", "Substitute.", "Verify the relationship."])
B.sel(7, "cp1", "In the figure with parallel lines, m∠1 = (5x + 4)° and m∠5 = (6x - 9)°. Select ALL true statements.", ["x = 13", "m∠1 = 69°", "m∠2 = 111°"], ["x = 5", "m∠5 = 111°", "∠1 and ∠5 are supplementary"], ["∠1, ∠5 corresponding: 5x + 4 = 6x - 9."], diagram=num_fig, tags=["graph"])
B.mc(7, "honors", "In the figure with parallel lines, m∠3 = (2x + y)°, m∠5 = (4x - y)°, and m∠4 = 108°. Find x and y.", "x = 24, y = 24", ["x = 18, y = 36", "x = 30, y = 12", "x = 12, y = 48"], ["∠3 = 180 - 108 = 72°; ∠5 = 72° (alternate interior with ∠3).", "2x + y = 72 and 4x - y = 72 → x = 24, y = 24."], diagram=num_fig, tags=["challenge", "graph"])
assert pair_type(3, 5) == "alternate interior angles" and 2 * 24 + 24 == 72 and 4 * 24 - 24 == 72
for e1, e2 in [("(3x - 4)°", "(2x + 11)°"), ("(9x)°", "(5x + 32)°"), ("(4x + 6)°", "(6x - 14)°")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.mc(7, "cp2", f"Corresponding angles for parallel lines measure {e1} and {e2}. Find x.", f"x = {fr(xv)}", [f"x = {fr((180 - (p1 + p2).c[0]) / (p1 + p2).c[1])}", f"x = {fr(xv + 1)}", f"x = {fr(xv - 3)}"], ["Corresponding angles are congruent."])
for m_i, m_j, i, j in [(68, 68, 1, 5), (68, 112, 3, 6), (75, 75, 4, 6), (120, 60, 2, 8), (95, 95, 3, 5), (44, 136, 4, 5)]:
    t_ = pair_type(i, j); need_eq = congruent(i, j); ok = (m_i == m_j) if need_eq else (m_i + m_j == 180)
    B.mc(8, "cp1", f"Lines ℓ (top) and m (bottom) are cut by a transversal, numbered as in the figure. m∠{i} = {m_i}° and m∠{j} = {m_j}°. Is ℓ ∥ m?", "Yes" if ok else "No", ["No" if ok else "Yes", "Only if the transversal is perpendicular", "Cannot be determined"],
         [f"∠{i} and ∠{j} are {t_}.", f"Parallel if they are {'congruent' if need_eq else 'supplementary'}: {'yes' if ok else 'no'}."], diagram=num_fig, tags=["graph", "reasoning"])
for i, j, e1, e2 in [(2, 6, "(3x + 14)°", "(5x - 10)°"), (3, 5, "(7x - 3)°", "(4x + 24)°"), (4, 5, "(2x + 6)°", "(4x + 6)°"), (1, 7, "(10x - 15)°", "(8x + 5)°")]:
    p1, p2 = linp(e1), linp(e2); t_ = pair_type(i, j)
    xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1]) if congruent(i, j) else (180 - (p1 + p2).c[0]) / (p1 + p2).c[1]
    assert 0 < p1(xv) < 180
    B.sa(8, "cp1", f"Using the figure numbering, m∠{i} = {e1} and m∠{j} = {e2}. Find x so that the lines are parallel.", f"x = {fr(xv)}", [f"∠{i}, ∠{j}: {t_}.", "Congruent." if congruent(i, j) else "Supplementary.", f"x = {fr(xv)}."], diagram=num_fig, tags=["graph"])
B.sel(8, "honors", "Using the figure numbering, select ALL single facts that would prove ℓ ∥ m.", ["∠1 ≅ ∠5", "∠4 ≅ ∠6", "m∠3 + m∠6 = 180°", "∠1 ≅ ∠7"], ["∠1 ≅ ∠3", "m∠1 + m∠2 = 180°", "∠2 ≅ ∠4"], ["Pairs across the two intersections; ∠1≅∠3, ∠2≅∠4 and linear pairs are always true."], diagram=num_fig, tags=["reasoning"])
B.orq(8, "cp1", "Given: ∠4 ≅ ∠8 (figure numbering). Prove ℓ ∥ m.", [("What kind of angles are ∠4 and ∠8?", "corresponding angles"), ("State the theorem used.", "Converse of the Corresponding Angles Postulate"), ("Conclusion.", "ℓ ∥ m"), ("Name another pair now known congruent.", "∠3 ≅ ∠5 (alternate interior)")], ["Same position.", "Converse.", "Parallel.", "Parallel line theorems now apply."], diagram=num_fig, tags=["reasoning"])
assert pair_type(4, 8) == "corresponding angles"
B.sa(8, "cp1", "Same-side interior angles measure 87° and 93°. Are the lines parallel?", "Yes", ["87 + 93 = 180."])
B.sa(8, "cp1", "Alternate interior angles measure 41° and 49°. Are the lines parallel?", "No", ["They are not congruent."])
for (x1, y1, x2, y2), (x3, y3, x4, y4) in [((0, 1, 3, 7), (1, -2, 4, 4)), ((2, 2, 6, 0), (0, 0, 1, 2)), ((-1, 5, 3, 5), (0, 0, 2, 1)), ((1, 1, 2, 4), (-3, 0, 3, -2))]:
    m1, m2 = F(y2 - y1, x2 - x1), F(y4 - y3, x4 - x3)
    rel_ = "parallel" if m1 == m2 else ("perpendicular" if m1 * m2 == -1 else "neither")
    B.mc(9, "cp1", f"Line 1 passes through {pt(x1, y1)} and {pt(x2, y2)}; line 2 through {pt(x3, y3)} and {pt(x4, y4)}. Classify the lines.", rel_, [r for r in ["parallel", "perpendicular", "neither", "the same line"] if r != rel_], [f"Slopes {fr(m1)} and {fr(m2)}."])
B.sel(9, "cp1", "Select ALL lines perpendicular to y = (2/5)x - 1.", ["y = -(5/2)x + 3", "5x + 2y = 8", "y = -2.5x"], ["y = (5/2)x", "y = -(2/5)x", "2x - 5y = 1"], ["Perpendicular slope -5/2."])
B.mc(9, "honors", "For what k is 3x + ky = 6 perpendicular to y = 2x + 1?", "k = 6", ["k = -6", "k = 3/2", "k = -3/2"], ["Slope of 3x + ky = 6 is -3/k; need -3/k = -1/2 → k = 6."])
B.orq(9, "cp1", "Line ℓ: 2x - 3y = 12.", [("Find the slope of ℓ.", "2/3"), ("Write a parallel line through (0, 5).", "y = (2/3)x + 5"), ("Write a perpendicular line through (0, 5).", "y = -(3/2)x + 5"), ("Find where ℓ meets the y-axis.", "(0, -4)")], ["Solve for y.", "Same slope.", "Negative reciprocal.", "x = 0."])
B.sa(9, "honors", "Find the equation of the perpendicular bisector of the segment from (2, 1) to (6, 9).", "y = -(1/2)x + 7", ["Midpoint (4, 5); slope of segment 2.", "Perpendicular slope -1/2: y - 5 = -(1/2)(x - 4)."], tags=["challenge", "connections"])
B.sa(9, "cp1", "Are y = -4x + 1 and y = (1/4)x - 3 perpendicular?", "Yes", ["(-4)(1/4) = -1."])

for S_, cfgs in [(5, [(57, 58, "a2", "b2", "b4", "a4"), (71, 66, "a4", "b4", "b2", "b1"), (49, 70, "a3", "b1", "b3", "a1"), (63, 55, "a1", "b1", "b3", "b2"), (82, 72, "a2", "b4", "a4", "b3")]),
                 (6, [(64, 60, "a1", "b3", "b2", "a4"), (53, 68, "a3", "b2", "b4", "b1"), (77, 57, "a4", "b1", "b3", "b2"), (46, 65, "a2", "b4", "b3", "b1"), (69, 74, "a1", "b4", "b2", "a3")])]:
    for k_, (base, slope, gpos, p1_, p2_, p3_) in enumerate(cfgs):
        # geometry of transversal: positions 1,3 have measure = slope angle t; 2,4 have 180 - t
        val = lambda pos: slope if int(pos[1]) % 2 else 180 - slope
        lab = {gpos: f"{val(gpos)}°", p1_: "x°", p2_: "y°", p3_: "z°"}
        dg = transversal(B, f"s0{S_}-cfg-{k_}", lab, f"Parallel lines cut by a transversal; one angle is labeled {val(gpos)}° and three others are labeled x, y, z.", slope_deg=slope)
        num = lambda pos: (0 if pos[0] == "a" else 4) + int(pos[1])
        rels = [pair_type(num(gpos), num(q_)) for q_ in (p1_, p2_, p3_)]
        B.orq(S_, "cp1" if k_ % 2 == 0 else "honors", "The two lines are parallel. Use the figure.", [("Find x.", str(val(p1_))), ("Find y.", str(val(p2_))), ("Find z.", str(val(p3_))), ("Name the relationship between the given angle and x.", rels[0])],
              ["Angles in positions matching the given angle's parity are congruent; the others are supplementary.", f"{rels[0]}.", f"{rels[1]}.", f"{rels[2]}."], diagram=dg, tags=["graph"])
        others = [p_ for p_ in ["a1", "a2", "a3", "a4", "b1", "b2", "b3", "b4"] if p_ != gpos]
        B.sel(S_, "cp1", f"Use the numbered figure. The lines are parallel and m∠{num(gpos)} = {val(gpos)}°. Select ALL other angles that measure {val(gpos)}°.", [f"∠{num(p_)}" for p_ in others if val(p_) == val(gpos)], [f"∠{num(p_)}" for p_ in others if val(p_) != val(gpos)][:3],
              ["Congruent: vertical, corresponding, alternate interior/exterior."], diagram=num_fig, tags=["graph"])
B.sa(1, "cp2", "Find the complement of 54°.", "36°", ["90 - 54."])
B.sa(8, "cp2", "Corresponding angles measure 73° and 73°. Are the lines parallel?", "Yes", ["Converse of the Corresponding Angles Postulate."])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
