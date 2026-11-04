"""Grade 7 Unit 9 — Spatial Thinking (spatial-thinking)."""
from glib import *

UNIT_ID = "spatial-thinking"
ABBR = "spt"
POLY = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon"}


# ============================================================== S1 Points, Lines, Planes
@fam("012")
def s1_count(r, L):
    n = r.randint(3, 6) if L == 0 else r.randint(5, 12)
    kind = pick(r, ["lines", "segments"])
    v = n * (n - 1) // 2
    return Q(f"There are {n} points, and no three of them lie on the same line. How many different {kind} can be drawn using two of the points?", str(v),
             ["Each pair of points determines one " + kind[:-1] + ".", f"Each of the {n} points pairs with {n - 1} others: {n} × {n - 1} = {n * (n - 1)}.", f"Each {kind[:-1]} was counted twice: {n * (n - 1)} ÷ 2 = {v}."],
             [str(n * (n - 1)), str(n), str(n - 1)], V(f"{n}*({n} - 1)/2"), why=["Counted each pair twice", "Used one per point", ""], tags=["reasoning"])


@fam("012")
def s1_segment(r, L):
    a = r.randint(-10, 5)
    ab, bc = r.randint(2, 12), r.randint(2, 12)
    if L == 0:
        return Q(f"Points A, B, and C are on a line in that order. AB = {ab} and BC = {bc}. Find AC.", str(ab + bc), ["Segment Addition: AB + BC = AC.", f"AC = {ab} + {bc} = {ab + bc}."],
                 [str(abs(ab - bc)) if ab != bc else str(ab + bc + 1), str(ab * bc), str(ab)], V(f"{ab} + {bc}"), why=["Subtracted instead of adding", "Multiplied the lengths", ""])
    if L == 1:
        b = a + 2 * ab
        return Q(f"On a number line, A is at {a} and B is at {b}. What number is at the midpoint of AB?", str(a + ab), [f"Midpoint = (a + b) ÷ 2.", f"({a} + {b}) ÷ 2 = {a + ab}."],
                 [str(b - a), str(ab), str(a + b)], V(f"({a} + {b})/2"), why=["Found the length instead", "Found half the length", "Forgot to divide by 2"])
    x = r.randint(2, 9)
    p, q, c = r.randint(2, 5), r.randint(1, 9), r.randint(1, 9)
    tot = p * x + q + x + c
    return Q(f"B is between A and C. AB = {p}x + {q}, BC = x + {c}, and AC = {tot}. Find x.", f"x = {x}", [f"AB + BC = AC: {p}x + {q} + x + {c} = {tot}.", f"{p + 1}x + {q + c} = {tot}.", f"{p + 1}x = {tot - q - c}.", f"x = {x}."],
             [f"x = {N(F(tot - q - c, p))}", f"x = {N(F(tot, p + 1))}", f"x = {N(F(tot + q + c, p + 1))}"], EQ(f"{p}x + {q} + x + {c} = {tot}"), why=["Forgot the x in BC", "Forgot to subtract the constants", "Added the constants"],
             tags=["connections", "multistep"])


@fam("012", mode="mc")
def s1_terms(r, L):
    items = [("A ray", "has one endpoint and extends forever in one direction"), ("A segment", "has two endpoints"), ("A line", "extends forever in both directions"),
             ("A plane", "is a flat surface that extends forever"), ("Parallel lines", "are in the same plane and never intersect"), ("Skew lines", "are not in the same plane and never intersect"),
             ("Collinear points", "lie on the same line"), ("Coplanar points", "lie in the same plane")]
    k = r.randrange(len(items) if L else 4)
    t, d = items[k]
    others = [x[0] for x in items if x[0] != t]
    r.shuffle(others)
    opts = [(t, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"Which term matches the description: “___ {d}”?", t, [f"{t} {d}."], options=opts, chk=TXT(t), mode="mc")


# ============================================================== S2 Angle Relationships
@fam("012")
def s2_pair(r, L):
    a = r.randint(12, 168)
    kind = pick(r, ["complementary", "supplementary", "vertical"] if L == 0 else ["complementary", "supplementary", "vertical", "corresponding", "alternate interior", "same-side interior"])
    if kind == "complementary":
        a = r.randint(5, 85)
        v, t = 90 - a, f"Two angles are complementary. One measures {a}°. What is the other?"
    elif kind == "supplementary":
        v, t = 180 - a, f"Two angles are supplementary. One measures {a}°. What is the other?"
    elif kind == "vertical":
        v, t = a, f"Two lines intersect. One angle measures {a}°. What is the measure of its vertical angle?"
    elif kind == "same-side interior":
        v, t = 180 - a, f"Two parallel lines are cut by a transversal. One same-side interior angle measures {a}°. What is the other same-side interior angle?"
    else:
        v, t = a, f"Two parallel lines are cut by a transversal. One angle measures {a}°. What is the measure of its {kind} angle?"
    wr = [str(180 - v) if 180 - v != v else str(v + 10), str(90 - a) if 0 < 90 - a != v else str(abs(v - 10)), str(360 - a)]
    return Q(t, f"{v}°", [{"complementary": "Complementary angles add to 90°.", "supplementary": "Supplementary angles add to 180°.", "vertical": "Vertical angles are congruent.",
                           "corresponding": "Corresponding angles are congruent when lines are parallel.", "alternate interior": "Alternate interior angles are congruent when lines are parallel.",
                           "same-side interior": "Same-side interior angles are supplementary when lines are parallel."}[kind], f"The angle measures {v}°."],
             [w + "°" for w in wr], V(str(v)), why=["Used supplementary instead of the correct relationship", "Used complementary instead of the correct relationship", "Subtracted from 360°"])


@fam("12")
def s2_solve(r, L):
    x = r.randint(5, 30)
    a, b = r.randint(2, 5), r.randint(-10, 20)
    kind = pick(r, ["supplementary", "vertical", "complementary"])
    if kind == "vertical":
        c = r.randint(1, 4)
        need(c != a)
        d = a * x + b - c * x
        t = f"Two vertical angles measure ({a}x {sgn(b)})° and ({c}x {sgn(d)})°. Find x."
        eq = f"{a}x + {b} = {c}x + {d}"
    elif kind == "supplementary":
        c = 180 - (a * x + b)
        need(c > 0)
        t = f"Two supplementary angles measure ({a}x {sgn(b)})° and {c}°. Find x."
        eq = f"{a}x + {b} + {c} = 180"
    else:
        c = 90 - (a * x + b)
        need(0 < c < 90 and a * x + b > 0)
        t = f"Two complementary angles measure ({a}x {sgn(b)})° and {c}°. Find x."
        eq = f"{a}x + {b} + {c} = 90"
    need(M_solve(eq) == x)
    return Q(t, f"x = {x}", [{"vertical": "Vertical angles are equal.", "supplementary": "The angles add to 180°.", "complementary": "The angles add to 90°."}[kind], f"Equation: {eq}.", f"Solve: x = {x}.",
                             "Check that each angle measure is positive."], [f"x = {N(M_solve(eq.replace('= 180', '= 90'))) if kind == 'supplementary' else N(M_solve(eq) + 2)}", f"x = {a * x + b}", f"x = {x + 5}"],
             EQ(eq), why=["Used the wrong angle sum", "Gave the angle measure instead of x", ""], tags=["connections"])


def M_solve(eq, v="x"):
    import mathtext
    return F(mathtext.solve_linear(eq, v)[1])


@fam("2", mode="mc")
def s2_identify(r, L):
    pairs = [("∠1 and ∠5", "corresponding angles"), ("∠3 and ∠6", "alternate interior angles"), ("∠1 and ∠4", "vertical angles"), ("∠3 and ∠5", "same-side interior angles"), ("∠1 and ∠2", "a linear pair")]
    p, k = pick(r, pairs)
    others = [x[1] for x in pairs if x[1] != k]
    r.shuffle(others)
    opts = [(k, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    alt = ("Two parallel lines cut by a transversal. Top intersection: ∠1 upper left, ∠2 upper right, ∠3 lower left, ∠4 lower right. "
           "Bottom intersection: ∠5 upper left, ∠6 upper right, ∠7 lower left, ∠8 lower right.")
    return Q(f"In the figure, two parallel lines are cut by a transversal. Classify {p}.", k, ["Find where each angle sits: above or below each line, and left or right of the transversal.", f"{p} are {k}."],
             options=opts, chk=TXT(k), mode="mc", diagram={"alt": alt, "draw": transversal_draw()})


def transversal_draw():
    def draw(path):
        fig, ax = new_fig(5.5, 4.6)
        ax.plot([-3, 3], [1, 1], color="#1f4e9c", lw=2.2)
        ax.plot([-3, 3], [-1, -1], color="#1f4e9c", lw=2.2)
        ax.plot([-1.2, 1.2], [-2.4, 2.4], color="#b23a3a", lw=2.2)
        for (x, y), labs in (((0.5, 1), ("1", "2", "3", "4")), ((-0.5, -1), ("5", "6", "7", "8"))):
            for (dx, dy), t in zip(((-0.35, 0.3), (0.45, 0.3), (-0.45, -0.3), (0.35, -0.3)), labs):
                ax.text(x + dx, y + dy, t, fontsize=13, ha="center", va="center", fontweight="bold")
        ax.set_aspect("equal")
        ax.axis("off")
        save(fig, path)
    return draw


# ============================================================== S3 Classifying Polygons
@fam("012")
def s3_angle_sum(r, L):
    n = pick(r, list(POLY))
    if L == 0:
        return Q(f"What is the sum of the interior angle measures of a {POLY[n]}?", f"{(n - 2) * 180}°", [f"A {POLY[n]} has {n} sides.", f"Sum = (n - 2) × 180° = ({n} - 2) × 180°.", f"= {(n - 2) * 180}°."],
                 [f"{n * 180}°", f"{(n - 1) * 180}°", f"{360 * (n - 2) if n > 3 else 90}°"], V(f"({n} - 2)*180"), why=["Multiplied the number of sides by 180°", "Used n - 1 instead of n - 2", ""])
    if L == 1:
        v = F((n - 2) * 180, n)
        return Q(f"What is the measure of each interior angle of a regular {POLY[n]}?", f"{mixed(v)}°", [f"Sum = ({n} - 2) × 180° = {(n - 2) * 180}°.", f"Each angle = {(n - 2) * 180}° ÷ {n}.", f"= {mixed(v)}°."],
                 [f"{(n - 2) * 180}°", f"{mixed(F(360, n))}°", f"{mixed(F(n * 180, n - 2))}°"], V(f"({n} - 2)*180/{n}"), why=["Forgot to divide by the number of angles", "Found the exterior angle", "Divided the wrong way"])
    angs = [r.randint(80, 150) for _ in range(n - 1)]
    last = (n - 2) * 180 - sum(angs)
    need(0 < last < 180 and n <= 7)
    return Q(f"A {POLY[n]} has angles measuring {', '.join(str(a) + '°' for a in angs)}, and x°. Find x.", f"x = {last}", [f"Angle sum = ({n} - 2) × 180° = {(n - 2) * 180}°.", f"Known angles total {sum(angs)}°.",
                                                                                                               f"x = {(n - 2) * 180} - {sum(angs)} = {last}."],
             [f"x = {360 - sum(angs) if 360 - sum(angs) > 0 else last + 20}", f"x = {n * 180 - sum(angs)}", f"x = {last + 180}"], EQ(f"{' + '.join(map(str, angs))} + x = ({n} - 2)*180"),
             why=["Used 360° for the angle sum", "Used n × 180° for the angle sum", ""], tags=["multistep"])


@fam("012", mode="mc")
def s3_name(r, L):
    n = pick(r, list(POLY))
    others = [POLY[k] for k in POLY if k != n]
    r.shuffle(others)
    opts = [(POLY[n], True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"What is the name of a polygon with {n} sides?", POLY[n], [f"A polygon with {n} sides is a {POLY[n]}."], options=opts, chk=TXT(POLY[n]), mode="mc")


@fam("012")
def s3_triangle(r, L):
    a = r.randint(20, 120)
    b = r.randint(20, 150 - a)
    c = 180 - a - b
    need(c > 0)
    big = max(a, b, c)
    want = "obtuse" if big > 90 else "right" if big == 90 else "acute"
    if L == 0:
        b = 90 - a if a < 90 else b
    return Q(f"A triangle has angles {a}°, {b}°, and x°. Find x, then classify the triangle as acute, right, or obtuse.", f"x = {180 - a - b}, {('obtuse' if max(a, b, 180 - a - b) > 90 else 'right' if max(a, b, 180 - a - b) == 90 else 'acute')}",
             [f"x = 180 - {a} - {b} = {180 - a - b}.", "Acute: all angles less than 90°; right: one 90°; obtuse: one greater than 90°.", f"The triangle is {('obtuse' if max(a, b, 180 - a - b) > 90 else 'right' if max(a, b, 180 - a - b) == 90 else 'acute')}."],
             [f"x = {360 - a - b}, obtuse", f"x = {180 - a - b}, {'acute' if max(a, b, 180 - a - b) >= 90 else 'obtuse'}", f"x = {a + b}, obtuse"], PY("tri_classify", a=a, b=b),
             why=["Used 360° as the angle sum", "Misclassified the triangle", "Added the angles instead of subtracting"])


# ============================================================== S4 Draw a Diagram
@fam("012")
def s4_problem(r, L):
    kind = pick(r, ["fence", "handshake", "trees", "stairs"] if L else ["fence", "trees", "stairs"])
    if kind == "fence":
        n, g = r.randint(4, 15), r.randint(2, 10)
        return Q(f"A straight fence is {n * g} feet long with a post every {g} feet, including both ends. How many posts are there?", str(n + 1),
                 ["Draw a diagram: posts at 0, " + f"{g}, {2 * g}, …, {n * g} feet.", f"There are {n} gaps.", f"Posts = gaps + 1 = {n + 1}."], [str(n), str(n + 2), str(n * g)],
                 V(f"{n * g}/{g} + 1"), why=["Counted the gaps instead of the posts", "Counted one extra post", "Used the length"], tags=["reasoning"])
    if kind == "handshake":
        n = r.randint(5, 15)
        return Q(f"At a meeting, each of {n} people shakes hands once with every other person. How many handshakes are there?", str(n * (n - 1) // 2),
                 [f"Draw {n} points; each pair is one handshake.", f"Each person shakes {n - 1} hands: {n}({n - 1}) = {n * (n - 1)}.", f"Divide by 2 because each handshake was counted twice: {n * (n - 1) // 2}."],
                 [str(n * (n - 1)), str(n * n), str(n - 1)], V(f"{n}*({n} - 1)/2"), why=["Counted each handshake twice", "Squared the number of people", "Counted one person's handshakes"], tags=["reasoning"])
    if kind == "trees":
        n, g = r.randint(4, 12), r.randint(3, 9)
        return Q(f"Trees are planted in a row, {g} meters apart. There are {n} trees. How far is it from the first tree to the last tree?", f"{(n - 1) * g} meters",
                 ["Draw the row of trees.", f"{n} trees make {n - 1} gaps.", f"Distance = {n - 1} × {g} = {(n - 1) * g} meters."], [f"{n * g} meters", f"{(n + 1) * g} meters", f"{n + g} meters"],
                 V(f"({n} - 1)*{g}"), why=["Counted trees instead of gaps", "Counted one extra gap", "Added instead of multiplying"], tags=["reasoning"])
    up, down, start, steps_ = r.randint(3, 9), r.randint(1, 5), r.randint(1, 5), r.randint(3, 6)
    need(up > down)
    top = start + steps_ * (up - down)
    return Q(f"A snail starts {start} ft up a wall. Each day it climbs {up} ft and each night slides back {down} ft. How high is it after {steps_} full days and nights?", f"{top} feet",
             ["Draw the wall and mark each day and night.", f"Net gain per day: {up} - {down} = {up - down} ft.", f"{start} + {steps_} × {up - down} = {top} ft."],
             [f"{start + steps_ * up} feet", f"{steps_ * (up - down)} feet", f"{start + steps_ * (up + down)} feet"], V(f"{start} + {steps_}*({up} - {down})"),
             why=["Ignored the sliding back", "Forgot the starting height", "Added the slide"], tags=["reasoning", "modeling"])


@fam("12")
def s4_map(r, L):
    a, b = r.randint(2, 12), r.randint(2, 12)
    c = r.randint(1, min(a, b))
    return Q(f"Ana walks {a} blocks north, {b} blocks east, then {c} blocks south. How many blocks north of her start is she now?", f"{a - c} blocks",
             ["Draw a diagram with the moves.", "East-west moves do not change the north-south distance.", f"{a} - {c} = {a - c} blocks north."], [f"{a + c} blocks", f"{a + b - c} blocks", f"{a + b + c} blocks"],
             V(f"{a} - {c}"), why=["Added the south distance", "Included the east distance", "Added all the distances"], tags=["reasoning"])


# ============================================================== S5 Congruence
@fam("012")
def s5_corresponding(r, L):
    A, B, C = "ABC"
    D_, E, F_ = r.sample(list("DEFGHJKLMNPQRST"), 3)
    perm = r.sample([0, 1, 2], 3) if L == 2 else [0, 1, 2]
    left = "ABC"
    right = "".join([D_, E, F_][perm.index(i)] for i in range(3)) if False else D_ + E + F_
    sides = {"AB": r.randint(3, 15), "BC": r.randint(3, 15), "AC": r.randint(3, 15)}
    ang = {"A": r.randint(30, 90), "B": r.randint(30, 80)}
    q = pick(r, ["side", "angle"])
    if q == "side":
        s = pick(r, list(sides))
        img = right[left.index(s[0])] + right[left.index(s[1])]
        return Q(f"△ABC ≅ △{right}. AB = {sides['AB']}, BC = {sides['BC']}, and AC = {sides['AC']}. Find {img}.", str(sides[s]),
                 ["Corresponding parts of congruent triangles are congruent.", f"Match the order of the letters: {img} corresponds to {s}.", f"{img} = {sides[s]}."],
                 [str(v) for k, v in sides.items() if k != s] + [str(sum(sides.values()))], PY("congruent_part", left=left, right=right, sides=sides, target=img), why=["Matched the wrong pair of vertices"] * 2 + ["Added the sides"])
    t = pick(r, ["A", "B"])
    img = right[left.index(t)]
    c3 = 180 - ang["A"] - ang["B"]
    return Q(f"△ABC ≅ △{right}. m∠A = {ang['A']}° and m∠B = {ang['B']}°. Find m∠{img}.", f"{ang[t]}°", [f"∠{img} corresponds to ∠{t}.", f"m∠{img} = {ang[t]}°."],
             [f"{ang['B' if t == 'A' else 'A']}°", f"{c3}°", f"{180 - ang[t]}°"], V(str(ang[t])), why=["Matched the wrong angle", "Found the third angle", "Used the supplement"])


@fam("12")
def s5_solve(r, L):
    x = r.randint(2, 12)
    a, b = r.randint(2, 6), r.randint(-5, 10)
    v = a * x + b
    need(v > 0)
    return Q(f"△PQR ≅ △XYZ. PQ = {v} cm and XY = ({a}x {sgn(b)}) cm. Find x.", f"x = {x}", ["Corresponding sides are equal: PQ = XY.", f"{a}x {sgn(b)} = {v}.", f"x = {x}."],
             [f"x = {v}", f"x = {N(F(v + b, a))}", f"x = {N(F(v, a))}"], EQ(f"{a}x + {b} = {v}"), why=["Gave the side length instead of x", "Added the constant instead of subtracting", "Forgot the constant"], tags=["connections"])


@fam("012", mode="mc")
def s5_criteria(r, L):
    k = pick(r, ["SSS", "SAS", "ASA", "AAS"])
    desc = {"SSS": "all three pairs of corresponding sides are congruent", "SAS": "two pairs of sides and the included angles are congruent",
            "ASA": "two pairs of angles and the included sides are congruent", "AAS": "two pairs of angles and a non-included pair of sides are congruent"}
    opts = [(x, x == k) for x in ["SSS", "SAS", "ASA", "AAS"]]
    return Q(f"Two triangles are congruent because {desc[k]}. Which shortcut is used?", k, [f"{k}: {desc[k]}."], options=opts, chk=TXT(k), mode="mc")


# ============================================================== S6 Circles
@fam("012")
def s6_circumference(r, L):
    rad = r.randint(2, 20)
    given = pick(r, ["radius", "diameter"])
    d = 2 * rad
    gv = rad if given == "radius" else d
    if L == 0:
        return Q(f"A circle has a {given} of {gv} cm. Find its circumference in terms of π.", f"{d}π cm", ["C = πd = 2πr.", f"d = {d} cm.", f"C = {d}π cm."],
                 [f"{rad}π cm", f"{rad * rad}π cm", f"{4 * rad}π cm"], PY("pi_coef", k=d), why=["Used the radius instead of the diameter", "Found the area", "Doubled the diameter"])
    c = math.pi * d if L == 2 else 3.14 * d
    return Q(f"A circle has a {given} of {gv} m. Find its circumference. Use {'π' if L == 2 else '3.14 for π'} and round to the nearest tenth.", f"{Rd(c, 1)} m",
             ["C = πd.", f"d = {d}.", f"C = {'π' if L == 2 else '3.14'} × {d} ≈ {Rd(c, 1)} m."], [f"{Rd(c / 2, 1)} m", f"{Rd((math.pi if L == 2 else 3.14) * rad * rad, 1)} m", f"{Rd(c * 2, 1)} m"],
             AP(f"{'π' if L == 2 else '3.14'}*{d}", 1), why=["Used the radius as the diameter", "Found the area", "Doubled the diameter"])


@fam("012")
def s6_reverse(r, L):
    d = r.randint(3, 40)
    if L < 2:
        return Q(f"A circle has diameter {d} in. What is its radius?", f"{mixed(F(d, 2))} in.", ["The radius is half the diameter.", f"r = {d} ÷ 2 = {mixed(F(d, 2))} in."],
                 [f"{2 * d} in.", f"{d} in.", f"{mixed(F(d, 4))} in."], V(f"{d}/2"), why=["Doubled instead of halving", "Copied the diameter", "Divided by 4"])
    c = d
    return Q(f"A circle has circumference {c}π ft. What is its radius?", f"{mixed(F(c, 2))} ft", ["C = 2πr.", f"{c}π = 2πr.", f"r = {mixed(F(c, 2))} ft."],
             [f"{c} ft", f"{2 * c} ft", f"{mixed(F(c, 4))} ft"], V(f"{c}/2"), why=["Gave the diameter", "Doubled instead of halving", ""], tags=["reasoning"])


@fam("12")
def s6_central(r, L):
    angs = [r.randint(40, 120) for _ in range(2)]
    x = 360 - sum(angs)
    need(0 < x < 200)
    return Q(f"Three central angles of a circle divide it completely. Two measure {angs[0]}° and {angs[1]}°. What is the third?", f"{x}°", ["The central angles around a point add to 360°.", f"{360} - {angs[0]} - {angs[1]} = {x}°."],
             [f"{180 - sum(angs) if 180 > sum(angs) else x + 20}°", f"{sum(angs)}°", f"{x - 10}°"], V(f"360 - {angs[0]} - {angs[1]}"), why=["Used 180° instead of 360°", "Added the given angles", ""])


# ============================================================== S7 Constructions
@fam("012", mode="mc")
def s7_concept(r, L):
    items = [("A perpendicular bisector of a segment", "passes through the midpoint and forms right angles with the segment"),
             ("An angle bisector", "divides an angle into two congruent angles"),
             ("A compass", "is used to draw arcs and circles and to copy lengths"),
             ("A straightedge", "is used to draw straight segments, without measuring"),
             ("Every point on the perpendicular bisector of a segment", "is the same distance from both endpoints")]
    t, d = pick(r, items)
    others = [x[0] for x in items if x[0] != t]
    r.shuffle(others)
    opts = [(t, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"Complete the statement: “___ {d}.”", t, [f"{t} {d}."], options=opts, chk=TXT(t), mode="mc")


@fam("012")
def s7_bisect(r, L):
    kind = pick(r, ["angle", "segment"])
    if kind == "angle":
        a = r.randint(10, 85) * 2
        if L == 2:
            x = r.randint(3, 15)
            p, q = r.randint(2, 5), r.randint(1, 10)
            half = p * x + q
            return Q(f"Ray BD bisects ∠ABC. m∠ABD = ({p}x + {q})° and m∠ABC = {2 * half}°. Find x.", f"x = {x}", ["A bisector makes two equal angles.", f"m∠ABD = {2 * half} ÷ 2 = {half}.", f"{p}x + {q} = {half}.", f"x = {x}."],
                     [f"x = {N(F(2 * half - q, p))}", f"x = {half}", f"x = {N(F(half + q, p))}"], EQ(f"2({p}x + {q}) = {2 * half}"), why=["Forgot to halve the angle", "Gave the angle measure", "Added the constant"], tags=["connections"])
        return Q(f"Ray BD bisects ∠ABC, which measures {a}°. What is m∠ABD?", f"{a // 2}°", ["A bisector divides the angle into two congruent angles.", f"{a} ÷ 2 = {a // 2}°."],
                 [f"{a}°", f"{2 * a}°", f"{180 - a}°"], V(f"{a}/2"), why=["Did not divide the angle", "Doubled instead of halving", "Found the supplement"])
    s = r.randint(4, 30)
    return Q(f"Point M lies on the perpendicular bisector of segment AB. MA = {s} cm. What is MB?", f"{s} cm", ["Every point on the perpendicular bisector is equidistant from A and B.", f"MB = MA = {s} cm."],
             [f"{mixed(F(s, 2))} cm", f"{2 * s} cm", "90 cm"], V(str(s)), why=["Halved the distance", "Doubled the distance", "Confused the right angle with a length"])


# ============================================================== S8 Translations
@fam("012")
def s8_point(r, L):
    x, y = r.randint(-8, 8), r.randint(-8, 8)
    h, k = nz(r, -6, 6), nz(r, -6, 6)
    if L == 0:
        desc = f"{abs(h)} units {'right' if h > 0 else 'left'} and {abs(k)} units {'up' if k > 0 else 'down'}"
    else:
        desc = f"by the rule (x, y) → (x {sgn(h)}, y {sgn(k)})"
    return Q(f"Point P({x}, {y}) is translated {desc}. What are the coordinates of P′?", f"({x + h}, {y + k})",
             [f"Add {h} to the x-coordinate: {x} {sgn(h)} = {x + h}.", f"Add {k} to the y-coordinate: {y} {sgn(k)} = {y + k}.", f"P′({x + h}, {y + k})."],
             [f"({x + k}, {y + h})", f"({x - h}, {y - k})", f"({x + h}, {y - k})"], PY("point", x=str(x + h), y=str(y + k)),
             why=["Applied the horizontal and vertical shifts to the wrong coordinates", "Moved in the opposite directions", "Moved the wrong way vertically"])


@fam("12")
def s8_rule(r, L):
    x, y = r.randint(-8, 8), r.randint(-8, 8)
    h, k = nz(r, -7, 7), nz(r, -7, 7)
    return Q(f"A translation moves A({x}, {y}) to A′({x + h}, {y + k}). Write the rule for the translation.", f"(x, y) → (x {sgn(h)}, y {sgn(k)})",
             [f"Horizontal change: {x + h} - ({x}) = {h}.", f"Vertical change: {y + k} - ({y}) = {k}.", f"Rule: (x, y) → (x {sgn(h)}, y {sgn(k)})."],
             [f"(x, y) → (x {sgn(-h)}, y {sgn(-k)})", f"(x, y) → (x {sgn(k)}, y {sgn(h)})", f"(x, y) → (x {sgn(x + h)}, y {sgn(y + k)})" if (x + h, y + k) != (h, k) else f"(x, y) → (x {sgn(h + 1)}, y {sgn(k)})"],
             PY("trans_rule", p=[x, y], q=[x + h, y + k]), why=["Subtracted in the wrong order", "Switched the horizontal and vertical changes", "Used the image coordinates as the shifts"])


@fam("2")
def s8_vertices(r, L):
    pts = [(r.randint(-6, 0), r.randint(-6, 0))]
    pts.append((pts[0][0] + r.randint(2, 5), pts[0][1]))
    pts.append((pts[0][0] + r.randint(0, 4), pts[0][1] + r.randint(2, 5)))
    h, k = nz(r, -4, 6), nz(r, -4, 6)
    i = r.randrange(3)
    labs = "ABC"
    img = [(a + h, b + k) for a, b in pts]
    alt = f"Coordinate plane with triangle ABC at " + ", ".join(f"{l}({a}, {b})" for l, (a, b) in zip(labs, pts)) + "."
    return Q(f"Triangle ABC is translated {abs(h)} units {'right' if h > 0 else 'left'} and {abs(k)} units {'up' if k > 0 else 'down'}. What are the coordinates of {labs[i]}′?", f"({img[i][0]}, {img[i][1]})",
             [f"Read {labs[i]}({pts[i][0]}, {pts[i][1]}) from the graph.", f"Add {h} to x and {k} to y.", f"{labs[i]}′({img[i][0]}, {img[i][1]})."],
             [f"({pts[i][0] + k}, {pts[i][1] + h})", f"({pts[i][0] - h}, {pts[i][1] - k})", f"({pts[i][0] + h}, {pts[i][1]})"], PY("point", x=str(img[i][0]), y=str(img[i][1])),
             why=["Switched the shifts", "Moved the opposite way", "Forgot the vertical shift"], tags=["graph"],
             diagram={"alt": alt, "draw": plane_draw((-8, 8), (-8, 8), polys=[(pts, None, None, True)], points=[(a, b, l) for l, (a, b) in zip(labs, pts)])})


# ============================================================== S9 Symmetry and Rotations / S10 Rotations
@fam("012")
def s9_lines(r, L):
    kind = pick(r, [("regular " + POLY[n], n) for n in (3, 4, 5, 6, 8)] + [("rectangle (not a square)", 2), ("rhombus (not a square)", 2), ("isosceles triangle (not equilateral)", 1), ("parallelogram (not a rectangle or rhombus)", 0)])
    t, n = kind
    return Q(f"How many lines of symmetry does a {t} have?", str(n), [f"A line of symmetry folds the figure onto itself.", f"A {t} has {n} line{'s' if n != 1 else ''} of symmetry."],
             [str(n + 2), str(2 * n) if n else "2", str(max(n - 1, 0)) if n - 1 != n else "4"], PY("symmetry", shape=t), why=["Counted extra lines", "Counted diagonals and midlines twice", ""])


@fam("012")
def s9_order(r, L):
    n = pick(r, [3, 4, 5, 6, 8, 9, 10, 12])
    if L == 0:
        return Q(f"What is the smallest angle of rotation that maps a regular {POLY.get(n, str(n) + '-gon')} onto itself?", f"{mixed(F(360, n))}°", ["Divide 360° by the number of sides.", f"360° ÷ {n} = {mixed(F(360, n))}°."],
                 [f"{mixed(F(180, n))}°", f"{(n - 2) * 180}°", f"{n * 10}°"], V(f"360/{n}"), why=["Divided 180° instead of 360°", "Gave the angle sum", ""])
    deg = 360 // n * r.randint(1, n - 1) if 360 % n == 0 else None
    need(deg is not None)
    return Q(f"Does a rotation of {deg}° map a regular {POLY.get(n, str(n) + '-gon')} onto itself?", "Yes", [f"The smallest rotation is 360° ÷ {n} = {360 // n}°.", f"{deg}° is a multiple of {360 // n}°, so yes."],
             ["No"], PY("rot_sym", n=n, deg=deg), mode="sa", why=["Thought only the smallest angle works"]) if r.random() < 0.5 else \
        Q(f"Does a rotation of {deg + 360 // n // 2 if (360 // n) % 2 == 0 else deg + 1}° map a regular {POLY.get(n, str(n) + '-gon')} onto itself?", "No",
          [f"The smallest rotation is 360° ÷ {n} = {360 // n}°.", "Only multiples of that angle work.", "No."], ["Yes"], PY("rot_sym", n=n, deg=deg + 360 // n // 2 if (360 // n) % 2 == 0 else deg + 1), mode="sa",
          why=["Did not check that the angle is a multiple of 360° ÷ n"])


@fam("012", mode="mc")
def s9_angle_mc(r, L):
    n = pick(r, [3, 4, 5, 6, 8, 9, 10, 12])
    base = 360 // n
    good = base * r.randint(1, n - 1)
    bad = sorted({d for d in range(10, 360, 5) if (d * n) % 360} - {good})
    bads = r.sample(bad, 3)
    opts = [(f"{good}°", True)] + [(f"{d}°", False) for d in bads]
    r.shuffle(opts)
    return Q(f"Which rotation maps a regular {POLY[n]} onto itself?", f"{good}°", [f"Rotations that work are multiples of 360° ÷ {n} = {base}°.", f"{good}° = {good // base} × {base}°."],
             options=opts, chk=PY("rot_sym_opt", n=n), mode="mc", tags=["reasoning"])


def rot(x, y, d):
    return {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[d]


@fam("012")
def s10_point(r, L):
    x, y = nz(r, -8, 8), nz(r, -8, 8)
    need(abs(x) != abs(y))
    d = pick(r, [180] if L == 0 else [90, 180, 270])
    direc = "counterclockwise" if L < 2 else pick(r, ["counterclockwise", "clockwise"])
    dd = d if direc == "counterclockwise" else 360 - d
    nx, ny = rot(x, y, dd)
    w = [rot(x, y, 360 - dd) if dd != 180 else (x, -y), (y, x), (-x, y)]
    return Q(f"Point A({x}, {y}) is rotated {d}° {direc} about the origin. What are the coordinates of A′?", f"({nx}, {ny})",
             [{90: "90° counterclockwise: (x, y) → (-y, x).", 180: "180°: (x, y) → (-x, -y).", 270: "270° counterclockwise: (x, y) → (y, -x)."}[dd], f"A′({nx}, {ny})."],
             [f"({a}, {b})" for a, b in w], PY("point", x=str(nx), y=str(ny)), why=["Rotated in the wrong direction" if dd != 180 else "Reflected over the x-axis instead", "Switched the coordinates only", "Reflected over the y-axis instead"])


@fam("12")
def s10_describe(r, L):
    x, y = nz(r, -8, 8), nz(r, -8, 8)
    need(abs(x) != abs(y))
    d = pick(r, [90, 180, 270])
    nx, ny = rot(x, y, d)
    return Q(f"A({x}, {y}) is mapped to A′({nx}, {ny}) by a counterclockwise rotation about the origin. What is the angle of rotation?", f"{d}°",
             ["Test the rules: 90° (x, y) → (-y, x); 180° (x, y) → (-x, -y); 270° (x, y) → (y, -x).", f"The {d}° rule matches."], [f"{x}°" for x in (90, 180, 270, 360) if x != d][:3],
             PY("rot_angle", p=[x, y], q=[nx, ny]), why=["Matched the wrong rotation rule"] * 3)


SKILLS = {
    1: dict(name="Introduction to Geometry: Points, Lines, and Planes", std=["G-CO.A.1", "4.G.A.1"], fams=[s1_count, s1_segment, s1_terms], extra=[err_of(s1_segment), open_of(s1_segment)]),
    2: dict(name="Angle Relationships and Parallel Lines", std=["7.G.B.5", "8.G.A.5"], fams=[s2_pair, s2_solve, s2_identify], extra=[err_of(s2_pair), open_of(s2_pair), select_of(s2_pair)]),
    3: dict(name="Classifying Polygons", std=["8.G.A.5", "5.G.B.3"], fams=[s3_angle_sum, s3_name, s3_triangle], extra=[err_of(s3_angle_sum), open_of(s3_angle_sum)]),
    4: dict(name="Draw a Diagram", std=["MP.1", "MP.4"], fams=[s4_problem, s4_map], extra=[err_of(s4_problem), open_of(s4_problem)]),
    5: dict(name="Congruence", std=["8.G.A.2", "G-CO.B.7"], fams=[s5_corresponding, s5_solve, s5_criteria], extra=[err_of(s5_corresponding), open_of(s5_corresponding)]),
    6: dict(name="Circles", std=["7.G.B.4"], fams=[s6_circumference, s6_reverse, s6_central], extra=[err_of(s6_circumference), open_of(s6_circumference), select_of(s6_reverse)]),
    7: dict(name="Constructions", std=["G-CO.D.12", "7.G.A.2"], fams=[s7_concept, s7_bisect], extra=[err_of(s7_bisect), open_of(s7_bisect)]),
    8: dict(name="Translations", std=["8.G.A.1", "8.G.A.3"], fams=[s8_point, s8_rule, s8_vertices], extra=[err_of(s8_point), open_of(s8_point), select_of(s8_point)]),
    9: dict(name="Symmetry and Rotations", std=["4.G.A.3", "G-CO.A.3"], fams=[s9_lines, s9_order, s9_angle_mc], extra=[err_of(s9_lines), open_of(s9_lines)]),
    10: dict(name="Rotations", std=["8.G.A.1", "8.G.A.3"], fams=[s10_point, s10_describe], extra=[err_of(s10_point), open_of(s10_point), select_of(s10_point)]),
}
