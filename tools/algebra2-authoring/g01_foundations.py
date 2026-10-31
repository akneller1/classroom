from lib import Bank
from mathlite import *
from geofig import Fig, transversal
import math

STD = {1: ["G-CO.A.1"], 2: ["G-CO.A.1"], 3: ["G-CO.A.1", "G-GPE.B.6"], 4: ["G-CO.A.1", "G-GPE.B.6"], 5: ["G-CO.A.1"], 6: ["G-CO.A.1", "G-CO.C.9"], 7: ["G-GPE.B.4", "G-GPE.B.6", "G-GPE.B.7"], 8: ["G-CO.D.12", "G-CO.C.9"]}
B = Bank("foundations-geometry", "fg", STD, course="geometry", prefix="geo")
sq = math.sqrt

# ---- scene figure: plane M with points; line through A,B; line ℓ meeting plane at C ----
fg = Fig(4.6, 3.4)
fg.poly([(0, 0), (6, 0), (7.5, 2.5), (1.5, 2.5)]); fg.text((6.6, 0.4), "M", size=11)
A_, B_, D_, E_ = (1.5, 0.5), (4.6, 0.9), (4.4, 2.0), (5.6, 0.45)
fg.line(A_, B_, ext=0.25); fg.dot(A_, "A", (-8, 8)); fg.dot(B_, "B", (6, 9)); fg.dot(D_, "D", (0, 9)); fg.dot(E_, "E", (8, -6))
C_ = (3.0, 1.75); top = (3.0, 4.2); bot = (3.0, -1.4)
fg.ray(C_, top); fg.seg(C_, (3.0, 0.0), ls="--", lw=1.2); fg.ray((3.0, 0.0), bot)
fg.dot(C_, "C", (-9, -7)); fg.dot((3.0, 3.4), "F", (9, 0)); fg.text(top, "ℓ", (9, -4))
fg.dot((6.8, 3.6), "G", (8, 0))
scene = fg.save(B, "s01-scene", "Plane M contains points A, B, D, E, and C. Line AB lies in plane M; C is not on line AB. A vertical line ℓ passes through F and C and meets plane M only at C (its part below C is hidden behind the plane and drawn dashed). Point G is above the plane, not on any drawn line.", schematic=True)
S = 1
for q, ans, wr, lvl in [("Name the intersection of line ℓ and plane M.", "point C", ["line AB", "point F", "plane M"], "cp2"),
                        ("Which point is NOT in plane M?", "F", ["A", "D", "E"], "cp2"),
                        ("How many points are needed to name plane M using points?", "3 noncollinear points", ["2 points", "3 collinear points", "4 points"], "cp2"),
                        ("Are points A, B, and C collinear?", "No", ["Yes", "Only if F is included", "Cannot be determined"], "cp1"),
                        ("Name a point that is coplanar with A, B, and E.", "D", ["F", "G", "No such point"], "cp1"),
                        ("Which describes points F and C?", "collinear (on line ℓ)", ["not collinear", "both in plane M", "the same point"], "cp1")]:
    B.mc(S, lvl, "Use the figure. " + q, ans, wr, ["Points in the parallelogram lie in plane M; line ℓ passes through the plane only at C."], diagram=scene, tags=["graph"])
B.sel(S, "cp1", "Use the figure. Select ALL true statements.", ["Line AB lies in plane M", "Line ℓ intersects plane M at C", "A, B, and D are coplanar", "Any two points are collinear"], ["F lies in plane M", "A, B, and C are collinear", "G lies on line ℓ"],
      ["Two points always determine a line.", "F and G are not in the plane."], diagram=scene, tags=["graph"])
B.sel(S, "honors", "Use the figure. Select ALL sets of three points that lie in plane M.", ["A, B, D", "A, B, E", "C, D, E"], ["A, F, C", "F, G, D", "A, B, G"],
      ["Only A, B, C, D, E are in plane M.", "Any three points are coplanar in SOME plane, but F and G are not in plane M."], diagram=scene, tags=["reasoning", "misconception"])
for q, ans, wr in [("What is the intersection of two distinct planes?", "a line", ["a point", "a plane", "a segment"]), ("Through any two points there is exactly one…", "line", ["plane", "segment of length 1", "ray"]),
                   ("Through any three noncollinear points there is exactly one…", "plane", ["line", "point", "angle"]), ("If two distinct lines intersect, they intersect in exactly one…", "point", ["line", "plane", "segment"]),
                   ("Which term is undefined in geometry?", "point", ["segment", "ray", "angle"]), ("What do we call lines that do not intersect and are not coplanar?", "skew lines", ["parallel lines", "perpendicular lines", "collinear lines"])]:
    B.mc(S, "cp2" if "undefined" in q or "two points" in q else "cp1", q, ans, wr, ["Postulates about points, lines, and planes."])
B.sel(S, "cp1", "Select ALL undefined terms of geometry.", ["point", "line", "plane"], ["segment", "ray", "angle", "midpoint"], ["Point, line, and plane are described, not defined; the others are defined from them."])
B.sel(S, "honors", "In a rectangular box with top face ABCD and bottom face EFGH (A above E, B above F, C above G, D above H), select ALL pairs of skew lines.", ["AB and CG", "AD and BF", "EF and DH"], ["AB and DC", "AE and BF", "AB and BF"], ["Skew: not parallel and not intersecting.", "AB ∥ DC, AE ∥ BF, AB meets BF at B."], tags=["reasoning"])
B.orq(S, "cp1", "A rectangular box has top face ABCD and bottom face EFGH, with A above E, B above F, C above G, D above H.", [("Name a line parallel to AB.", "DC (or EF, HG)"), ("Name a line that intersects AB.", "AD (or BC, AE, BF)"), ("Name a line skew to AB.", "CG (or DH, EH, FG)"), ("Name the intersection of planes ABCD and BCGF.", "line BC")],
      ["Parallel edges.", "Edges sharing a vertex.", "Neither parallel nor intersecting.", "Shared edge."], tags=["reasoning"])
B.orq(S, "honors", "Explain each postulate with an example from a classroom.", [("Two points determine a line.", "e.g. a string stretched between two thumbtacks"), ("Three noncollinear points determine a plane.", "e.g. a tripod stand never wobbles"), ("Two planes meet in a line.", "e.g. a wall meets the floor along an edge"), ("Why does a four-legged table sometimes wobble?", "four points need not be coplanar")],
      ["Examples vary.", "Examples vary.", "Examples vary.", "Three points always determine a plane; a fourth may not lie in it."], tags=["reasoning", "connections"])
B.sa(S, "cp2", "How many lines pass through two distinct points?", "exactly one", ["Postulate."])
B.sa(S, "cp1", "Can three points be noncoplanar? Explain.", "No; any three points lie in at least one plane", ["Collinear points lie in infinitely many planes; noncollinear in exactly one."], tags=["reasoning"])
B.sa(S, "honors", "How many planes are determined by 4 points, no three collinear and not all coplanar?", "4", ["Each choice of 3 points gives a plane: C(4, 3) = 4."], tags=["challenge"])
B.sa(S, "cp1", "Name the intersection of a line and a plane if the line is not in the plane and not parallel to it.", "a single point", ["The line pierces the plane once."])

# ---- Skill 2: segments, rays, notation ----
S = 2
fg = Fig(4.6, 1.6); P = [(0, 0), (2, 0), (3.5, 0), (6, 0)]
fg.line(P[0], P[3], ext=0.15)
for p, n in zip(P, "PQRS"): fg.dot(p, n, (0, 10))
lineQ = fg.save(B, "s02-line-pqrs", "A line with points P, Q, R, S in that order from left to right.")
for q, ans, wr, lvl in [("Which ray is opposite to ray QP?", "ray QR (or QS)", ["ray RQ", "ray PQ", "ray SP"], "cp1"), ("Name the segment between Q and R.", "QR", ["ray QR", "line QR", "QS"], "cp2"),
                        ("Are rays QR and QS the same ray?", "Yes: both start at Q and go through R and S", ["No: they end at different points", "No: S is farther", "Only if QR = RS"], "cp1"),
                        ("Are rays RQ and QR the same ray?", "No: they have different endpoints and directions", ["Yes: same two letters", "Yes: they share segment QR", "Only on a number line"], "cp1"),
                        ("Which point lies on ray RP?", "Q", ["S", "no other points", "only R"], "cp1"), ("What is the intersection of ray QP and ray QS?", "point Q", ["segment QS", "line PS", "ray QS"], "honors")]:
    B.mc(S, lvl, "Use the figure. " + q, ans, wr, ["A ray is named by its endpoint first and continues through the second point.", "Opposite rays share an endpoint and point in opposite directions."], diagram=lineQ, tags=["graph", "misconception"])
B.sel(S, "cp1", "Use the figure. Select ALL names for the same line.", ["line PS", "line QR", "line SP", "line RQ"], ["ray PS", "segment PS"], ["A line may be named by any two of its points in either order."], diagram=lineQ, tags=["graph"])
B.sel(S, "cp1", "Use the figure. Select ALL true statements.", ["PQ is part of PS", "Ray QS contains R", "QR and RS share point R"], ["Ray RQ contains S", "Line PQ and line RS are different lines"], ["All four points are collinear."], diagram=lineQ, tags=["graph"])
for sym, name, wr in [("AB with a bar over it", "segment AB", ["line AB", "ray AB", "the length of AB"]), ("AB (no symbol)", "the length (distance) from A to B", ["segment AB", "line AB", "ray AB"]),
                      ("AB with a one-headed arrow", "ray AB", ["line AB", "segment AB", "ray BA"]), ("AB with a two-headed arrow", "line AB", ["ray AB", "segment AB", "plane AB"])]:
    B.mc(S, "cp2", f"In geometric notation, what does {sym} represent?", name, wr, ["Bar → segment; arrow → ray; double arrow → line; no symbol → length."])
B.sel(S, "honors", "Select ALL true statements about rays.", ["A ray has exactly one endpoint", "Opposite rays form a line", "Ray AB and ray BA overlap in segment AB"], ["Ray AB and ray BA are the same", "A ray has a measurable length", "Opposite rays are always parallel"], ["Rays extend infinitely in one direction."], tags=["reasoning"])
B.orq(S, "cp1", "Points J, K, L lie on a line in that order.", [("Name two opposite rays with endpoint K.", "KJ and KL"), ("Name a segment with endpoint J.", "JK or JL"), ("Is K on ray LJ?", "Yes"), ("Is J on ray KL?", "No")], ["Same endpoint, opposite directions.", "Bar notation.", "Ray LJ starts at L through K and J.", "Ray KL goes away from J."])
B.orq(S, "honors", "Count figures determined by 5 collinear points A, B, C, D, E.", [("How many different segments?", "10"), ("How many different lines?", "1"), ("How many different rays (endpoint among the points)?", "8"), ("Explain the ray count.", "Each interior point has 2 rays, each end point 1: 3·2 + 2·1")],
      ["C(5, 2).", "All collinear.", "Count by endpoint.", "Interior points start rays in both directions."], tags=["challenge"])
B.sa(S, "cp2", "What is the endpoint of ray MN?", "M", ["The first letter names the endpoint."])
B.sa(S, "cp1", "Points A, B, C are collinear with B between A and C. Name two opposite rays.", "BA and BC", ["They share endpoint B."])
B.sa(S, "cp2", "How many endpoints does a segment have?", "2", ["A segment has two endpoints."])
B.sa(S, "cp1", "Name the figure formed by two opposite rays.", "a line", ["Together they extend in both directions."])
B.sa(S, "honors", "How many segments are determined by 6 points, no three collinear?", "15", ["C(6, 2) = 15."], tags=["challenge"])
B.sa(S, "cp1", "Explain the difference between ray PQ and ray QP.", "Ray PQ starts at P toward Q; ray QP starts at Q toward P", ["Endpoint and direction differ."])
B.mc(S, "cp1", "Which is a correct name for a plane containing noncollinear points X, Y, Z?", "plane XYZ", ["line XYZ", "plane XY", "ray XYZ"], ["Name a plane with three noncollinear points or one script letter."])
B.mc(S, "cp2", "Which figure has no endpoints?", "line", ["segment", "ray", "half-line with an endpoint"], ["Lines extend in both directions."])

# ---- Skill 3: measuring and adding segments ----
S = 3
for a, b, c, ab_e, bc_e, ac_v in [(2, 5, None, "2x + 5", "3x - 1", 39), (1, 4, None, "x + 4", "4x - 6", 33), (3, -2, None, "3x - 2", "x + 10", 40), (5, 0, None, "5x", "2x + 8", 50), (4, 3, None, "4x + 3", "6x - 7", 76)]:
    # solve AB + BC = AC
    pa, pb = linp(ab_e), linp(bc_e); tot = pa + pb; xv = (ac_v - tot.c[0]) / tot.c[1]
    B.sa(S, "cp1", f"B is between A and C. AB = {ab_e}, BC = {bc_e}, and AC = {ac_v}. Find x, AB, and BC.", f"x = {fr(xv)}; AB = {fr(pa(xv))}; BC = {fr(pb(xv))}", ["Segment Addition Postulate: AB + BC = AC.", f"{pstr(tot)} = {ac_v} → x = {fr(xv)}.", "Substitute to find each length."])
    assert pa(xv) + pb(xv) == ac_v and pa(xv) > 0 and pb(xv) > 0
for a_, b_ in [(-7, 4), (-3.5, 6), (2, 11), (-12, -5)]:
    B.sa(S, "cp2", f"On a number line, P is at {a_:g} and Q is at {b_:g}. Find PQ.", f"{abs(b_ - a_):g}", ["Distance = |difference of coordinates|."])
for AB, BC in [(7, 12), (3.5, 8.25)]:
    B.mc(S, "cp2", f"B is between A and C with AB = {AB:g} and BC = {BC:g}. Find AC.", f"{AB + BC:g}", [f"{BC - AB:g}", f"{AB * BC:g}", f"{(AB + BC) / 2:g}"], ["AC = AB + BC."])
for AC, AB in [(30, 11), (18.6, 7.9)]:
    B.mc(S, "cp2", f"B is between A and C with AC = {AC:g} and AB = {AB:g}. Find BC.", f"{AC - AB:.1f}".rstrip("0").rstrip("."), [f"{AC + AB:g}", f"{AB:g}", f"{AC / 2:g}"], ["BC = AC - AB."])
fg = Fig(4.6, 1.6); pts = [(0, 0), (3, 0), (5, 0), (9, 0)]
fg.seg(pts[0], pts[3])
for p_, n_ in zip(pts, "WXYZ"): fg.dot(p_, n_, (0, 10))
fg.side(pts[0], pts[1], "2x", dist=-12); fg.side(pts[1], pts[2], "x + 2", dist=-12); fg.side(pts[2], pts[3], "3x - 2", dist=-12); fg.text((4.5, 0), "WZ = 36", (0, 26))
dg = fg.save(B, "s03-wxyz", "Segment WZ with points X and Y between; WX = 2x, XY = x + 2, YZ = 3x - 2, and WZ = 36.", schematic=True)
B.orq(S, "cp1", "Use the figure.", [("Write an equation.", "2x + (x + 2) + (3x - 2) = 36"), ("Solve for x.", "x = 6"), ("Find WX, XY, YZ.", "12, 8, 16"), ("Find WY.", "20")], ["Segment addition.", "6x = 36.", "Substitute.", "WX + XY."], diagram=dg, tags=["graph"])
B.sel(S, "cp1", "M is between L and N. Select ALL statements that must be true.", ["LM + MN = LN", "LN > LM", "L, M, N are collinear"], ["LM = MN", "LM > MN", "LN = LM - MN"], ["Betweenness requires collinearity and gives LM + MN = LN."], tags=["misconception"])
B.sel(S, "honors", "A, B, C are collinear with AB = 5 and BC = 9. Select ALL possible values of AC.", ["14", "4"], ["9", "45", "5"], ["If B is between: 14. If A is between B and C: AC = 9 - 5 = 4. C cannot be between since BC > AB."], tags=["reasoning", "challenge"])
B.mc(S, "cp1", "A student says that if AB = BC then B must be between A and C. What is wrong?", "A, B, C might not be collinear (B could be off the line)", ["Nothing", "B must be the endpoint", "AB must be larger"], ["Equal distances do not guarantee collinearity."], tags=["error-analysis", "misconception"])
B.sa(S, "honors", "On a number line, A = -4 and C = 14. Find the coordinate of B on AC with AB : BC = 1 : 2.", "2", ["B is 1/3 of the way: -4 + (18/3)."], tags=["challenge"])
B.sa(S, "cp1", "Points D, E, F are collinear with E between D and F. DF = 5x - 3, DE = 2x + 4, EF = 14. Find DF.", "32", ["2x + 4 + 14 = 5x - 3 → x = 7.", "5(7) - 3 = 32."])
assert 2 * 7 + 4 + 14 == 5 * 7 - 3
B.sa(S, "cp1", "A road trip from A to C passes through B. AB is 2.4 times BC, and AC = 170 mi. Find AB.", "120 mi", ["2.4x + x = 170 → x = 50."], tags=["modeling"])
B.sa(S, "cp2", "Are segments with lengths 6 cm and 60 mm congruent?", "Yes", ["60 mm = 6 cm."])
B.mc(S, "honors", "AB = 3x + 1, BC = 2x, AC = 4x + 7, with B between A and C. Which is true?", "x = 6 and AC = 31", ["x = 8 and AC = 39", "x = 6 and AC = 25", "No solution"], ["5x + 1 = 4x + 7."], tags=["multistep"])

# ---- Skill 4: midpoints and bisectors ----
S = 4
for e1, e2 in [("4x - 3", "2x + 11"), ("5x + 2", "8x - 13"), ("x + 9", "3x - 5"), ("7x - 10", "4x + 5")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.sa(S, "cp1", f"M is the midpoint of AB. AM = {e1} and MB = {e2}. Find x and AB.", f"x = {fr(xv)}; AB = {fr(2 * p1(xv))}", ["A midpoint makes AM = MB.", f"{e1} = {e2} → x = {fr(xv)}.", f"AB = 2·AM = {fr(2 * p1(xv))}."])
    assert p1(xv) == p2(xv) and p1(xv) > 0
for a_, b_ in [(-6, 10), (3, 14), (-9, -2), (-5.5, 7.5)]:
    B.mc(S, "cp2", f"On a number line, the endpoints of a segment are {a_:g} and {b_:g}. Find the midpoint.", f"{(a_ + b_) / 2:g}", [f"{(b_ - a_) / 2:g}", f"{a_ + b_:g}", f"{(b_ - a_):g}"], ["Average the coordinates."], tags=["misconception"])
for m_, a_ in [(4, -3), (-2, 5), (7.5, 1)]:
    B.sa(S, "cp1", f"On a number line, M = {m_:g} is the midpoint of AB and A = {a_:g}. Find B.", f"{2 * m_ - a_:g}", ["B = 2M - A."])
B.sel(S, "cp1", "Line ℓ bisects segment CD at point K. Select ALL true statements.", ["CK = KD", "K is the midpoint of CD", "CD = 2CK"], ["ℓ is perpendicular to CD", "CK = CD", "ℓ must pass through C"], ["A bisector passes through the midpoint; perpendicularity is not required."], tags=["misconception"])
B.mc(S, "cp1", "Which is a perpendicular bisector of AB?", "A line through the midpoint of AB that forms right angles with AB", ["Any line through A", "Any line through the midpoint", "A line parallel to AB"], ["Two conditions: midpoint and perpendicular."])
B.orq(S, "cp1", "On a number line A = -8 and B = 12.", [("Find AB.", "20"), ("Find the midpoint M.", "2"), ("Find the midpoint of AM.", "-3"), ("Find the point P with AP : PB = 3 : 1.", "7")], ["|12 - (-8)|.", "(−8 + 12)/2.", "(−8 + 2)/2.", "-8 + (3/4)(20)."])
B.orq(S, "honors", "M is the midpoint of AB and N is the midpoint of AM. AB = 6x + 4, NM = x + 3.", [("Express AM in terms of x.", "3x + 2"), ("Write an equation relating NM and AM.", "2(x + 3) = 3x + 2"), ("Solve for x.", "x = 4"), ("Find AB and NB.", "AB = 28; NB = 21")], ["Half of AB.", "N is the midpoint of AM.", "2x + 6 = 3x + 2.", "NB = NM + MB = 7 + 14."], tags=["challenge"])
B.mc(S, "cp1", "A student says: 'P is on AB and AP = 5, so P is the midpoint.' What is missing?", "PB must also equal 5 (AB = 10)", ["Nothing", "AP must be 10", "P must be outside AB"], ["Midpoint requires AP = PB."], tags=["error-analysis"])
B.sa(S, "cp2", "M is the midpoint of segment XY and XM = 9. Find XY.", "18", ["XY = 2·XM."])
B.sa(S, "cp2", "Segment RS = 25. Its midpoint is T. Find RT.", "12.5", ["Half of 25."])
B.sa(S, "honors", "On a number line, A = a and B = b. Write the coordinate of the point 1/4 of the way from A to B.", "a + (b - a)/4 = (3a + b)/4", ["Start at A and move 1/4 of AB."], tags=["connections"])
B.sel(S, "honors", "Select ALL objects that can bisect a segment.", ["a point", "a line", "a ray", "a plane"], ["another whole segment that does not pass through the midpoint", "a parallel line"], ["Any figure passing through the midpoint (and not containing the segment) bisects it."], tags=["reasoning"])
B.sa(S, "cp1", "M is the midpoint of PQ with PM = 3x + 7 and PQ = 10x - 2. Find x.", "x = 4", ["PQ = 2PM: 10x - 2 = 6x + 14 → 4x = 16."])
assert 10 * 4 - 2 == 2 * (3 * 4 + 7)

# ---- Skill 5: angles and classification ----
S = 5
for d, kind in [(37, "acute"), (90, "right"), (128, "obtuse"), (180, "straight"), (89.5, "acute"), (91, "obtuse")]:
    B.mc(S, "cp2", f"Classify an angle measuring {d:g}°.", kind, [k for k in ["acute", "right", "obtuse", "straight"] if k != kind][:3], ["acute < 90° < obtuse < 180°; right = 90°; straight = 180°."])
for i, (ang, lab) in enumerate([(35, "35°"), (120, "x°"), (90, None)]):
    fg = Fig(3.6, 2.6); V = (0, 0); A1 = (4, 0); A2 = (4 * math.cos(math.radians(ang)), 4 * math.sin(math.radians(ang)))
    fg.ray(V, A1); fg.ray(V, A2); fg.dot(V, "Q", (-6, -10)); fg.dot((3, 0), "R", (0, -11)); fg.dot((3 * math.cos(math.radians(ang)), 3 * math.sin(math.radians(ang))), "P", (-8, 6))
    fg.angle(V, A1, A2, lab, right=(ang == 90))
    dg = fg.save(B, f"s05-angle-{i}", f"Angle PQR with vertex Q, rays QP and QR, measuring {ang}° ({'marked with a right-angle box' if ang == 90 else 'labeled ' + lab}).")
    kind = "acute" if ang < 90 else ("right" if ang == 90 else "obtuse")
    B.orq(S, "cp2", "Use the figure.", [("Name the vertex.", "Q"), ("Give two names for the angle.", "∠PQR and ∠RQP (or ∠Q)"), ("Classify the angle.", kind), ("Name its sides.", "rays QP and QR")], ["Shared endpoint.", "Vertex in the middle.", "Compare with 90°.", "The two rays."], diagram=dg, tags=["graph"])
B.mc(S, "cp1", "A student names an angle ∠QPR when the vertex is Q. What is wrong?", "The vertex letter must be in the middle: ∠PQR", ["Nothing", "Angles are named with two letters", "The vertex goes last"], ["Middle letter = vertex."], tags=["error-analysis"])
B.sel(S, "cp1", "Select ALL acute angle measures.", ["12°", "45°", "89°"], ["90°", "91°", "135°", "180°"], ["Acute: between 0° and 90°."])
B.sel(S, "honors", "∠1 is obtuse and ∠2 is acute. Select ALL statements that must be true.", ["m∠1 > m∠2", "m∠1 + m∠2 > 90°", "m∠1 - m∠2 > 0°"], ["m∠1 + m∠2 = 180°", "m∠1 + m∠2 < 180°", "m∠1 = 2·m∠2"], ["Obtuse > 90° > acute.", "The sum could exceed 180° (e.g. 170° + 80°)."], tags=["reasoning"])
B.sa(S, "cp1", "∠ABC is a right angle and m∠ABC = (4x + 10)°. Find x.", "x = 20", ["4x + 10 = 90."])
B.sa(S, "cp1", "∠DEF is a straight angle with m∠DEF = (3x - 6)°. Find x.", "x = 62", ["3x - 6 = 180."])
B.sa(S, "honors", "For what values of x is an angle measuring (2x + 10)° obtuse?", "40 < x < 85", ["90 < 2x + 10 < 180."], tags=["reasoning"])
B.sa(S, "cp2", "How many degrees are in a right angle?", "90°", ["Definition."])
B.mc(S, "cp1", "The hands of a clock show 4:00. What kind of angle do they form?", "obtuse (120°)", ["acute (60°)", "right (90°)", "straight"], ["Each hour mark is 30°; 4 × 30 = 120."], tags=["modeling"])
B.mc(S, "honors", "At 3:30, what is the angle between the clock hands?", "75°", ["90°", "60°", "105°"], ["Minute hand at 180°; hour hand at 90 + 15 = 105°.", "180 - 105 = 75."], tags=["challenge", "modeling"])
B.sa(S, "cp2", "Classify a 179° angle.", "obtuse", ["Between 90° and 180°."])
B.sa(S, "cp1", "Two angles are congruent. One measures 47°. What is the measure of the other?", "47°", ["Congruent angles have equal measures."])

# ---- Skill 6: angle addition and bisectors ----
S = 6
for a_, b_, tot in [("(2x + 5)°", "(3x - 10)°", 120), ("(x + 20)°", "(4x)°", 95), ("(5x - 4)°", "(2x + 11)°", 112), ("(6x)°", "(x + 18)°", 102)]:
    pa, pb = linp(a_), linp(b_)
    xv = (tot - (pa + pb).c[0]) / (pa + pb).c[1]
    B.sa(S, "cp1", f"Point D is in the interior of ∠ABC. m∠ABD = {a_}, m∠DBC = {b_}, m∠ABC = {tot}°. Find x and each angle.", f"x = {fr(xv)}; m∠ABD = {fr(pa(xv))}°; m∠DBC = {fr(pb(xv))}°", ["Angle Addition Postulate.", f"x = {fr(xv)}."])
    assert pa(xv) + pb(xv) == tot and pa(xv) > 0 and pb(xv) > 0
for e1, e2 in [("(3x + 8)°", "(5x - 12)°"), ("(x + 30)°", "(3x - 6)°"), ("(7x - 9)°", "(4x + 15)°")]:
    p1, p2 = linp(e1), linp(e2); xv = (p2.c[0] - p1.c[0]) / (p1.c[1] - p2.c[1])
    B.sa(S, "cp1", f"Ray BD bisects ∠ABC. m∠ABD = {e1} and m∠DBC = {e2}. Find m∠ABC.", f"{fr(2 * p1(xv))}°", ["A bisector forms two congruent angles.", f"x = {fr(xv)}.", "Double one half."])
    assert p1(xv) == p2(xv) > 0
for i, (a1, a2) in enumerate([(30, 45), (52, 38)]):
    fg = Fig(3.8, 3.0); V = (0, 0); pts_ = [(4 * math.cos(math.radians(t)), 4 * math.sin(math.radians(t))) for t in (0, a1, a1 + a2)]
    for p_ in pts_: fg.ray(V, p_)
    fg.dot(V, "B", (-8, -8));
    for p_, n_ in zip(pts_, "ADC"): fg.text(p_, n_, (8, 6))
    fg.angle(V, pts_[0], pts_[1], f"{a1}°", r=0.9); fg.angle(V, pts_[1], pts_[2], "x°", r=1.3)
    dg = fg.save(B, f"s06-add-{i}", f"Angle ABC split by ray BD: angle ABD = {a1}°, angle DBC = x°, and the whole angle ABC = {a1 + a2}° (stated in the question).")
    B.mc(S, "cp2", f"Use the figure. m∠ABC = {a1 + a2}°. Find x.", str(a2), [str(a1 + a2 + a1), str(a1), str(180 - a1 - a2)], ["m∠ABD + m∠DBC = m∠ABC."], diagram=dg, tags=["graph"])
B.sel(S, "cp1", "Ray QS bisects ∠PQR and m∠PQR = 84°. Select ALL true statements.", ["m∠PQS = 42°", "∠PQS ≅ ∠SQR", "m∠PQS + m∠SQR = 84°"], ["m∠PQS = 84°", "∠PQS is obtuse", "QS ⊥ QP"], ["Bisector halves the angle."])
B.orq(S, "honors", "Rays BD and BE trisect ∠ABC (A–D–E–C in order). m∠ABD = (2x + 4)°, m∠DBE = (3x - 6)°.", [("Find x.", "x = 10"), ("Find m∠ABD.", "24°"), ("Find m∠ABC.", "72°"), ("Find m∠ABE.", "48°")], ["Trisect: three congruent angles: 2x + 4 = 3x - 6.", "Substitute.", "3·24.", "2·24."], tags=["challenge"])
B.orq(S, "cp1", "∠AOC and ∠COB form a straight angle AOB. m∠AOC = (5x + 2)°, m∠COB = (3x + 18)°.", [("Write an equation.", "5x + 2 + 3x + 18 = 180"), ("Solve for x.", "x = 20"), ("Find each angle.", "102° and 78°"), ("If OD bisects ∠COB, find m∠AOD.", "141°")], ["Straight angle = 180°.", "8x = 160.", "Substitute.", "102 + 39."])
B.mc(S, "cp1", "A student says ray BD bisects ∠ABC because D is in the interior of ∠ABC. What is wrong?", "D must also make ∠ABD ≅ ∠DBC", ["Nothing", "D must be on BC", "A bisector must be perpendicular"], ["Interior is not enough."], tags=["error-analysis"])
B.sa(S, "cp2", "Ray BD bisects ∠ABC, which measures 130°. Find m∠ABD.", "65°", ["Half of 130."])
B.sa(S, "cp2", "m∠ABD = 22° and m∠DBC = 49°, with D in the interior of ∠ABC. Find m∠ABC.", "71°", ["Add."])
B.sa(S, "honors", "OM bisects ∠AOB, and ON bisects ∠AOM. If m∠NOB = 81°, find m∠AOB.", "108°", ["Let m∠AOB = 4t: m∠NOB = 3t = 81 → t = 27."], tags=["challenge"])
B.sa(S, "cp1", "∠1 and ∠2 make up a right angle. m∠1 = 3m∠2. Find both.", "m∠1 = 67.5°, m∠2 = 22.5°", ["4m∠2 = 90."])
B.sel(S, "honors", "Select ALL true statements about angle bisectors.", ["Every angle has exactly one bisector", "The bisector of a straight angle is perpendicular to its sides", "Each half of a bisected obtuse angle is acute"], ["Each half of a bisected acute angle is obtuse", "A bisector always meets the opposite side at its midpoint"], ["Half of an angle < 180° is < 90°."], tags=["reasoning"])
B.sa(S, "cp1", "D is in the interior of ∠ABC. m∠ABC = 98° and m∠ABD is 14° more than m∠DBC. Find m∠DBC.", "42°", ["2t + 14 = 98."])
B.mc(S, "cp2", "D is in the interior of ∠XYZ. Which equation must be true?", "m∠XYD + m∠DYZ = m∠XYZ", ["m∠XYD = m∠DYZ", "m∠XYD + m∠XYZ = 180°", "m∠XYD - m∠DYZ = 90°"], ["Angle Addition Postulate."])

# ---- Skill 7: distance and midpoint on the coordinate plane ----
S = 7
for (x1, y1), (x2, y2) in [((1, 2), (4, 6)), ((-3, 5), (5, -1)), ((0, -7), (12, -2)), ((-4, -4), (2, 4)), ((2, 3), (7, 3)), ((-6, 1), (-1, -11))]:
    d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2; d = rad(d2)
    B.sa(S, "cp2" if math.isqrt(d2) ** 2 == d2 else "cp1", f"Find the distance between {pt(x1, y1)} and {pt(x2, y2)}.", d, ["d = √((x₂ - x₁)² + (y₂ - y₁)²).", f"= √{d2} = {d}."])
    B.sa(S, "cp2", f"Find the midpoint of the segment from {pt(x1, y1)} to {pt(x2, y2)}.", pt(F(x1 + x2, 2), F(y1 + y2, 2)), ["Average the x-coordinates and the y-coordinates."])
for (mx, my), (ax, ay) in [((2, -1), (-3, 4)), ((0, 5), (6, 1)), ((F(7, 2), 2), (1, -3))]:
    bx, by = 2 * F(mx) - ax, 2 * F(my) - ay
    B.mc(S, "cp1", f"M{pt(mx, my)} is the midpoint of AB and A = {pt(ax, ay)}. Find B.", pt(bx, by), [pt((F(mx) + ax) / 2, (F(my) + ay) / 2), pt(F(mx) - ax, F(my) - ay), pt(ax - F(mx), ay - F(my))], ["B = 2M - A for each coordinate."], tags=["misconception"])
for (A, Bv, C) in [((0, 0), (6, 0), (3, 4)), ((1, 1), (4, 5), (8, 2))]:
    ab, bc, ca = [((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) for p, q in ((A, Bv), (Bv, C), (C, A))]
    per = sum(sq(v) for v in (ab, bc, ca))
    kind = "isosceles" if len({ab, bc, ca}) < 3 else "scalene"
    B.orq(S, "cp1", f"Triangle with vertices A{pt(*A)}, B{pt(*Bv)}, C{pt(*C)}.", [("Find AB.", rad(ab)), ("Find BC.", rad(bc)), ("Find CA.", rad(ca)), ("Classify by sides; is it right?", f"{kind}; {'right' if sorted([ab, bc, ca])[2] == sorted([ab, bc, ca])[0] + sorted([ab, bc, ca])[1] else 'not right'}")],
          ["Distance formula.", "Distance formula.", "Distance formula.", "Compare lengths; check Pythagorean relation."])
B.sel(S, "cp1", "Select ALL points that are 5 units from (1, 1).", ["(4, 5)", "(6, 1)", "(-2, -3)", "(1, -4)"], ["(5, 5)", "(4, 4)", "(3, 3)"], ["Check (Δx)² + (Δy)² = 25."])
B.sel(S, "honors", "Segment PQ has endpoints P(-2, 3) and Q(6, -1). Select ALL true statements.", ["The midpoint is (2, 1)", "PQ = 4√5", "The point 1/4 of the way from P is (0, 2)"], ["PQ = 80", "The midpoint is (4, -2)"], ["Midpoint average; √(64 + 16) = √80 = 4√5; P + (1/4)(8, -4)."])
B.mc(S, "cp1", "A student computes the distance from (1, 2) to (4, 6) as √(3 + 4) = √7. What is wrong?", "The differences must be squared: √(9 + 16) = 5", ["Nothing", "Add the coordinates", "Use (4 - 1)(6 - 2)"], ["d = √((Δx)² + (Δy)²)."], tags=["error-analysis"])
B.sa(S, "honors", "Find k so that the distance from (2, k) to (5, 3) is 5.", "k = -1 or k = 7", ["9 + (3 - k)² = 25 → (3 - k)² = 16."], tags=["challenge"])
B.sa(S, "honors", "Find the point P that divides the segment from A(-1, 2) to B(11, 8) in the ratio 2 : 1.", "(7, 6)", ["P = A + (2/3)(B - A) = (-1 + 8, 2 + 4)."], tags=["connections"])
B.sa(S, "cp1", "Find the perimeter of the triangle with vertices (0, 0), (8, 0), (0, 6).", "24", ["Sides 8, 6, 10."])
B.mc(S, "cp2", "Which formula gives the midpoint of (x₁, y₁) and (x₂, y₂)?", "((x₁ + x₂)/2, (y₁ + y₂)/2)", ["((x₂ - x₁)/2, (y₂ - y₁)/2)", "(x₁ + x₂, y₁ + y₂)", "((x₁ + y₁)/2, (x₂ + y₂)/2)"], ["Average each coordinate."])

# ---- Skill 8: reasoning and constructions ----
S = 8
for step_, why, wr in [("Open the compass to the length of AB and mark it on a ray from C.", "copying a segment", ["bisecting a segment", "copying an angle", "constructing a perpendicular through a point"]),
                       ("From A and B, draw arcs with the same radius (more than half AB) above and below AB; connect the intersections.", "constructing the perpendicular bisector of AB", ["copying segment AB", "bisecting an angle", "constructing a parallel line"]),
                       ("From vertex V draw an arc crossing both sides; from those points draw equal arcs that meet; draw a ray from V through the meeting point.", "bisecting an angle", ["copying an angle", "constructing a perpendicular bisector", "constructing an equilateral triangle"]),
                       ("Draw a circle centered at A through B and a circle centered at B through A; connect A and B to an intersection point.", "constructing an equilateral triangle", ["bisecting AB", "copying angle A", "constructing a square"]),
                       ("Copy the angle formed by a transversal at one line onto the transversal at a point P; the new side is…", "a line through P parallel to the first line", ["a perpendicular to the transversal", "the angle bisector", "the midpoint of the transversal"])]:
    B.mc(S, "cp1", f"Which construction is described? {step_}", why, wr, ["Compass-and-straightedge constructions."])
for cond, conv, inv, contra in [("If an angle is a right angle, then it measures 90°.", "If an angle measures 90°, then it is a right angle.", "If an angle is not a right angle, then it does not measure 90°.", "If an angle does not measure 90°, then it is not a right angle."),
                                ("If M is the midpoint of AB, then AM = MB.", "If AM = MB, then M is the midpoint of AB.", "If M is not the midpoint of AB, then AM ≠ MB.", "If AM ≠ MB, then M is not the midpoint of AB.")]:
    B.orq(S, "cp1", f"Conditional: {cond}", [("Write the converse.", conv), ("Write the inverse.", inv), ("Write the contrapositive.", contra), ("Which of these is always equivalent to the original?", "the contrapositive")],
          ["Swap hypothesis and conclusion.", "Negate both.", "Swap and negate.", "A conditional and its contrapositive have the same truth value."], tags=["reasoning"])
B.mc(S, "honors", "For the second conditional, the converse 'If AM = MB, then M is the midpoint of AB' is…", "false: M could be off segment AB", ["true", "the contrapositive", "a definition"], ["M equidistant from A and B lies on the perpendicular bisector, not necessarily on AB."], tags=["reasoning"])
for seq, nxt in [("3, 7, 11, 15, …", "19"), ("2, 6, 18, 54, …", "162"), ("1, 4, 9, 16, …", "25"), ("1, 1, 2, 3, 5, …", "8")]:
    B.sa(S, "cp2", f"Use inductive reasoning to find the next term: {seq}", nxt, ["Identify the pattern."])
B.mc(S, "cp1", "Which is an example of deductive reasoning?", "All squares are rectangles; ABCD is a square; so ABCD is a rectangle.", ["The last 5 days were sunny, so tomorrow will be sunny.", "Every odd number I tried is prime, so all odd numbers are prime.", "The pattern 2, 4, 8 continues with 16."], ["Deductive: from general statements to a specific certain conclusion."])
B.mc(S, "cp1", "Find a counterexample to: 'If x² = 25, then x = 5.'", "x = -5", ["x = 5", "x = 25", "x = 0"], ["(-5)² = 25 but -5 ≠ 5."])
B.sel(S, "cp1", "Select ALL valid conclusions from: 'If a figure is a square, then it has four right angles' and 'Figure F is a square.'", ["F has four right angles", "F has four sides"], ["Any figure with four right angles is a square", "F is a rhombus but not a square"], ["Law of Detachment.", "F has four sides because it is a square."], tags=["reasoning"])
B.sel(S, "honors", "Select ALL biconditionals that are true.", ["An angle is right if and only if it measures 90°", "A point is a midpoint of AB if and only if it lies on AB and AM = MB", "Two angles are supplementary if and only if their measures sum to 180°"], ["An angle is acute if and only if it measures 45°", "A figure is a rectangle if and only if it is a square"], ["Both the conditional and its converse must be true."], tags=["reasoning"])
B.orq(S, "honors", "Prove: If m∠1 + m∠2 = 90° and m∠1 = 30°, then m∠2 = 60°.", [("Statement 1 and reason.", "m∠1 + m∠2 = 90°; given"), ("Statement 2 and reason.", "m∠1 = 30°; given"), ("Statement 3 and reason.", "30° + m∠2 = 90°; substitution"), ("Statement 4 and reason.", "m∠2 = 60°; subtraction property of equality")], ["Givens.", "Givens.", "Substitute.", "Subtract 30."], tags=["reasoning"])
B.mc(S, "cp1", "Which property justifies: if AB = CD and CD = EF, then AB = EF?", "Transitive Property of Equality", ["Reflexive Property", "Symmetric Property", "Substitution of a definition"], ["a = b and b = c → a = c."])
B.mc(S, "cp2", "Which property says AB = AB?", "Reflexive Property", ["Symmetric Property", "Transitive Property", "Addition Property"], ["Anything equals itself."])
B.sa(S, "cp1", "Use the Law of Syllogism: If p then q; if q then r. What follows?", "If p, then r", ["Chain the conditionals."])
B.sa(S, "cp2", "Name the tools used in classical geometric constructions.", "compass and straightedge", ["No measuring marks allowed."])

# ================= additions: generated variety =================
import itertools
V = {"A": (0, 0, 1), "B": (1, 0, 1), "C": (1, 1, 1), "D": (0, 1, 1), "E": (0, 0, 0), "F": (1, 0, 0), "G": (1, 1, 0), "H": (0, 1, 0)}
EDGES = [a + b for a, b in itertools.combinations("ABCDEFGH", 2) if sum(abs(V[a][i] - V[b][i]) for i in range(3)) == 1]
def rel(e1, e2):
    if set(e1) & set(e2): return "intersecting"
    d1 = tuple(V[e1[1]][i] - V[e1[0]][i] for i in range(3)); d2 = tuple(V[e2[1]][i] - V[e2[0]][i] for i in range(3))
    if any(abs(a) for a, b in zip(d1, d2) if a and b): return "parallel"
    return "skew"
BOX = "a rectangular box with top face ABCD and bottom face EFGH (A above E, B above F, C above G, D above H)"
for e, kind, lvl in [("AB", "parallel", "cp1"), ("BF", "skew", "honors"), ("EH", "intersecting", "cp1"), ("CD", "skew", "honors")]:
    others = [x for x in EDGES if x != e]; right = [x for x in others if rel(e, x) == kind]; wrong = [x for x in others if rel(e, x) != kind][:4]
    B.sel(1, lvl, f"In {BOX}, select ALL edges that are {kind} to edge {e}.", right, wrong, ["Parallel: same direction, no shared point. Intersecting: share a vertex. Skew: neither."], tags=["reasoning"])
for e1, e2 in [("AB", "GH"), ("AE", "CD"), ("BC", "FG"), ("DH", "BC")]:
    k = rel(e1, e2)
    B.mc(1, "cp1", f"In {BOX}, how are edges {e1} and {e2} related?", k, [x for x in ["parallel", "intersecting", "skew", "perpendicular and intersecting"] if x != k][:3], ["Check for a shared vertex, then for matching direction."])
import random
R = random.Random(11)
for trial in range(5):
    letters = R.sample("JKLMNPQ", 5); pos = {c: i for i, c in enumerate(letters)}
    a, b, c = letters[1], letters[3], letters[0]
    on = lambda P_, Q_, X_: (pos[X_] - pos[P_]) * (pos[Q_] - pos[P_]) >= 0
    cands = [f"{x} is on ray {a}{b}" for x in letters if x not in (a, b)] + [f"{x} is on ray {b}{a}" for x in letters if x not in (a, b)]
    pred = lambda s_: on(*(s_.split(" is on ray ")[1][0], s_.split(" is on ray ")[1][1], s_[0]))
    picked = cands[:3] + cands[3:6]
    if sum(map(pred, picked)) >= 2 and sum(map(pred, picked)) < 6:
        sel_auto(B, 2, "cp1", f"Points {', '.join(letters)} lie on a line in that order. Select ALL true statements.", picked, pred, ["A ray contains its endpoint and every point on the side of the second letter."])
for n_ in (4, 6, 7):
    B.mc(2, "cp1", f"How many different segments are determined by {n_} points on a line?", str(n_ * (n_ - 1) // 2), [str(n_ - 1), str(n_ * (n_ - 1)), str(n_)], ["Each pair of points gives a segment: C(n, 2)."])
for a_, b_, c_ in [(-5, 3, 9), (2, 7, -4), (-8, -1, 6)]:
    pts_ = {"A": a_, "B": b_, "C": c_}
    st = {f"AB = {abs(b_ - a_)}": True, f"BC = {abs(c_ - b_)}": True, f"AC = {abs(c_ - a_)}": True, f"AB = {abs(b_ + a_)}": abs(b_ + a_) == abs(b_ - a_), f"B is between A and C": min(a_, c_) < b_ < max(a_, c_), f"A is between B and C": min(b_, c_) < a_ < max(b_, c_)}
    B.sel(3, "cp1", f"On a number line A = {a_}, B = {b_}, C = {c_}. Select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Distance = |difference|; between means the coordinate lies between the others."])
for AB, BC in [(4, 10), (7.5, 2.5), (12, 12)]:
    B.sa(3, "honors" if AB != BC else "cp1", f"A, B, C are collinear, AB = {AB:g}, BC = {BC:g}. List every possible value of AC.", ", ".join(f"{v:g}" for v in sorted({AB + BC, abs(AB - BC)} - ({0} if AB == BC else set()))) + (" (or 0 if A and C coincide)" if AB == BC else ""),
         ["Either B is between A and C (sum) or not (difference)."], tags=["reasoning"])
B.orq(3, "cp1", "A 12-ft board is cut into three pieces in the ratio 1 : 2 : 3.", [("Write an equation.", "x + 2x + 3x = 12"), ("Find x.", "2"), ("Find each length.", "2 ft, 4 ft, 6 ft"), ("Check.", "2 + 4 + 6 = 12")], ["Segment addition.", "6x = 12.", "Multiply.", "Sum."], tags=["modeling"])
for a_, b_ in [(-12, 4), (5, 23), (-7.5, -1.5)]:
    m_ = (a_ + b_) / 2
    B.orq(4, "cp1", f"On a number line A = {a_:g} and B = {b_:g}.", [("Find the midpoint M.", f"{m_:g}"), ("Find AM.", f"{abs(m_ - a_):g}"), ("Find the midpoint of MB.", f"{(m_ + b_) / 2:g}"), ("Find the point 3/4 of the way from A to B.", f"{a_ + 0.75 * (b_ - a_):g}")], ["Average.", "Half of AB.", "Average M and B.", "A + (3/4)(B - A)."])
for mx, ax_ in [(3, -5), (-4, 6), (0.5, 2)]:
    B.mc(4, "cp1", f"M = {mx:g} is the midpoint of AB on a number line, and A = {ax_:g}. Find B.", f"{2 * mx - ax_:g}", [f"{(mx + ax_) / 2:g}", f"{mx - ax_:g}", f"{2 * ax_ - mx:g}"], ["B = 2M - A."], tags=["misconception"])
B.sel(4, "cp1", "M is the midpoint of ST and ST = 30. Select ALL true statements.", ["SM = 15", "MT = 15", "SM = MT"], ["SM = 30", "M is an endpoint of ST", "SM + MT = 15"], ["Midpoint halves the segment."])
B.sel(4, "honors", "Segment AB has midpoint M. Select ALL statements that must be true.", ["AM = ½AB", "M is on AB", "A and B are equidistant from M"], ["AM = AB", "M is the only point equidistant from A and B", "AB is perpendicular to any bisector"], ["The midpoint lies on the segment halfway between the endpoints.", "Every point of the perpendicular bisector is equidistant from A and B."])
for expr, lo, hi, kind in [("(3x)°", 0, 30, "acute"), ("(2x - 20)°", 55, 100, "obtuse"), ("(x + 40)°", 50, 50, "right")]:
    a_ = linp(expr)
    ans = f"x = {lo}" if lo == hi else f"{lo} < x < {hi}"
    B.sa(5, "honors" if lo != hi else "cp1", f"For what value(s) of x is an angle measuring {expr} {kind}?", ans, [f"{'0 < ' if kind == 'acute' else '90 < ' if kind == 'obtuse' else ''}{expr.strip('°')}{' < 90' if kind == 'acute' else ' < 180' if kind == 'obtuse' else ' = 90'}.", f"Solve: {ans}."], tags=["reasoning"])
    if lo != hi: assert a_(lo) == (0 if kind == "acute" else 90) and a_(hi) == (90 if kind == "acute" else 180)
for h_, m_ in [(2, 0), (6, 0), (9, 30), (1, 20)]:
    ang = abs(30 * h_ + 0.5 * m_ - 6 * m_); ang = min(ang, 360 - ang)
    kind = "acute" if ang < 90 else ("right" if ang == 90 else ("obtuse" if ang < 180 else "straight"))
    B.mc(5, "cp1" if m_ == 0 else "honors", f"At {h_}:{m_:02d}, what is the smaller angle between the clock hands, and how is it classified?", f"{ang:g}°, {kind}", [f"{ang + 30:g}°, {'obtuse' if ang + 30 > 90 else 'acute'}", f"{360 - ang:g}°, reflex", f"{30 * h_:g}°, {'acute' if 30 * h_ < 90 else 'obtuse' if 30 * h_ < 180 else 'straight'}"],
         ["Hour hand: 30° per hour plus 0.5° per minute; minute hand 6° per minute.", f"Difference {ang:g}°."], tags=["modeling"])
B.sel(5, "cp1", "Select ALL measures that describe obtuse angles.", ["91°", "135°", "179.9°"], ["90°", "180°", "45°", "200°"], ["Obtuse: strictly between 90° and 180°."])
B.sel(5, "honors", "Select ALL pairs that could be the measures of two acute angles whose sum is obtuse.", ["50° and 60°", "80° and 15°", "89° and 2°"], ["30° and 40°", "45° and 45°", "100° and 5°"], ["Each must be < 90° and the sum must be between 90° and 180°."], tags=["reasoning"])
for whole, ratio in [(120, (1, 2)), (90, (2, 3)), (150, (3, 7))]:
    a_, b_ = ratio; part = F(whole, a_ + b_)
    B.sa(6, "cp1", f"D is in the interior of ∠ABC with m∠ABC = {whole}°. m∠ABD : m∠DBC = {a_} : {b_}. Find both angles.", f"{fr(a_ * part)}° and {fr(b_ * part)}°", [f"{a_}k + {b_}k = {whole}.", f"k = {fr(part)}."])
for half in (17, 44.5, 63):
    B.mc(6, "cp2", f"Ray BD bisects ∠ABC and m∠ABD = {half:g}°. Find m∠ABC.", f"{2 * half:g}°", [f"{half / 2:g}°", f"{180 - half:g}°", f"{half:g}°"], ["Double the half."])
B.sel(6, "cp1", "∠AOB and ∠BOC are adjacent with m∠AOB = 40° and m∠BOC = 50°. Select ALL true statements.", ["m∠AOC = 90°", "∠AOC is a right angle", "OB is in the interior of ∠AOC"], ["OB bisects ∠AOC", "m∠AOC = 10°"], ["Adjacent angles add."])
B.orq(6, "honors", "Rays OA, OB, OC, OD are in order around O with m∠AOD = 160°, m∠AOB = m∠COD, and m∠BOC = 2·m∠AOB.", [("Write an equation with t = m∠AOB.", "t + 2t + t = 160"), ("Find t.", "40°"), ("Find m∠BOC.", "80°"), ("Find m∠AOC.", "120°")], ["Angle addition.", "4t = 160.", "2t.", "t + 2t."], tags=["challenge"])
for (x1, y1), (x2, y2), (x3, y3) in [((0, 0), (4, 0), (4, 3)), ((-1, 2), (3, 5), (6, 1)), ((2, -2), (5, 2), (-2, 1))]:
    d = lambda p_, q_: (p_[0] - q_[0]) ** 2 + (p_[1] - q_[1]) ** 2
    A_, B__, C_ = (x1, y1), (x2, y2), (x3, y3)
    st = {f"AB = {rad(d(A_, B__))}": True, f"BC = {rad(d(B__, C_))}": True, f"The midpoint of AC is {pt(F(x1 + x3, 2), F(y1 + y3, 2))}": True, f"AB = {d(A_, B__)}": False, f"The midpoint of AC is {pt(F(x3 - x1, 2), F(y3 - y1, 2))}": (x1, y1) == (0, 0)}
    B.sel(7, "cp1", f"A{pt(*A_)}, B{pt(*B__)}, C{pt(*C_)}. Select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Distance and midpoint formulas.", "Remember to take the square root."])
for P1, P2 in [((-3, 4), (5, 4)), ((2, -6), (2, 3)), ((-5, -5), (7, 0))]:
    B.mc(7, "cp2", f"Find the distance between {pt(*P1)} and {pt(*P2)}.", rad((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2), [rad((P1[0] + P2[0]) ** 2 + (P1[1] + P2[1]) ** 2), str(abs(P1[0] - P2[0]) + abs(P1[1] - P2[1])), str((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2)], ["d = √((Δx)² + (Δy)²)."], tags=["misconception"])
B.orq(7, "honors", "Quadrilateral with vertices P(1, 1), Q(5, 2), R(6, 6), S(2, 5).", [("Find PQ and RS.", "√17 and √17"), ("Find QR and SP.", "√17 and √17"), ("Find the midpoints of PR and QS.", "(3.5, 3.5) and (3.5, 3.5)"), ("What kind of quadrilateral is PQRS? Justify.", "rhombus: all sides equal (diagonals bisect each other)")],
      ["Distance formula.", "Distance formula.", "Midpoint formula.", "Equal sides → rhombus."], tags=["connections", "challenge"])
for c_ in [("If two angles form a linear pair, then they are supplementary.", "If two angles are supplementary, then they form a linear pair.", False),
           ("If a number is divisible by 4, then it is even.", "If a number is even, then it is divisible by 4.", False),
           ("If a triangle has three congruent sides, then it is equiangular.", "If a triangle is equiangular, then it has three congruent sides.", True)]:
    B.mc(8, "cp1", f"Conditional: {c_[0]} Is its converse true?", "Yes" if c_[2] else "No", ["Yes" if not c_[2] else "No", "Only for acute angles", "The converse is the same statement"],
         [f"Converse: {c_[1]}", "Look for a counterexample." if not c_[2] else "Equiangular triangles are equilateral."], tags=["reasoning"])
B.sel(8, "cp1", "Select ALL statements that are counterexamples to 'If x > 0, then x² > x'.", ["x = 1", "x = 1/2", "x = 0.9"], ["x = 2", "x = 5", "x = 10"], ["Need x > 0 with x² ≤ x: 0 < x ≤ 1."], tags=["reasoning"])
B.mc(8, "honors", "Which statement follows from: 'If an angle is a right angle, it measures 90°' and 'm∠K ≠ 90°'?", "∠K is not a right angle", ["∠K is acute", "∠K is obtuse", "∠K measures 0°"], ["Law of Contrapositive (modus tollens): not q → not p."], tags=["reasoning"])
B.orq(8, "cp1", "Justify each step: 2(x + 3) = 14.", [("2x + 6 = 14", "Distributive Property"), ("2x = 8", "Subtraction Property of Equality"), ("x = 4", "Division Property of Equality"), ("Check", "2(4 + 3) = 14")], ["Distribute.", "Subtract 6.", "Divide by 2.", "Substitute."], tags=["reasoning"])
B.orq(8, "honors", "Write a two-column proof: Given AB = CD. Prove AC = BD for collinear points A, B, C, D in that order.", [("Statement after the given.", "BC = BC; Reflexive Property"), ("Add.", "AB + BC = CD + BC; Addition Property"), ("Use segment addition.", "AC = AB + BC and BD = BC + CD"), ("Conclude.", "AC = BD; Substitution")], ["Reflexive.", "Add equals.", "Segment Addition Postulate.", "Substitute."], tags=["reasoning", "challenge"])
for q_, a_, w_ in [("Construct a line perpendicular to ℓ through a point P on ℓ. What is the first step?", "Draw arcs from P that cross ℓ at two points equidistant from P", ["Measure 90° with a protractor", "Draw any circle centered off ℓ", "Copy segment ℓ"]),
                   ("Which construction locates the midpoint of a segment?", "the perpendicular bisector", ["the angle bisector", "copying an angle", "a parallel through a point"])]:
    B.mc(8, "cp2", q_, a_, w_, ["Compass-and-straightedge constructions."])

B.sa(3, "cp1", "X, Y, Z are collinear with Y between X and Z. XY = 3a + 1, YZ = 2a + 4, XZ = 30. Find XY.", "16", ["5a + 5 = 30 → a = 5.", "XY = 16."])
assert 3 * 5 + 1 + 2 * 5 + 4 == 30
B.sa(5, "cp1", "∠P is acute and m∠P = (5x - 15)°. If x is a whole number, what is the greatest possible x?", "20", ["5x - 15 < 90 → x < 21."], tags=["reasoning"])
B.sa(6, "cp1", "Ray YW bisects ∠XYZ. m∠XYW = (4x - 7)° and m∠XYZ = (6x + 10)°. Find x and m∠XYZ.", "x = 12; 82°", ["2(4x - 7) = 6x + 10 → 2x = 24."])
assert 2 * (4 * 12 - 7) == 6 * 12 + 10
B.mc(6, "honors", "∠ABC is a straight angle and BD bisects it. BE bisects ∠DBC. Find m∠ABE.", "135°", ["45°", "90°", "120°"], ["m∠ABD = 90°, m∠DBE = 45°."], tags=["multistep"])

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
