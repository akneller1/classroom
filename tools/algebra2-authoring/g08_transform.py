from lib import Bank, graph
PN={3:"triangle",4:"quadrilateral",5:"pentagon",6:"hexagon",8:"octagon",10:"decagon",12:"dodecagon"}
from mathlite import *
from fill import fill
import math, random

STD = {1: ["G-CO.A.4", "G-CO.A.5"], 2: ["G-CO.A.4", "G-CO.A.5"], 3: ["G-CO.A.4", "G-CO.A.5"], 4: ["G-CO.A.5"], 5: ["G-CO.B.6", "G-CO.B.7"], 6: ["G-SRT.A.1"], 7: ["G-SRT.A.2"], 8: ["G-CO.A.3"], 9: ["G-CO.B.6", "G-GPE.B.4"]}
B = Bank("transformations", "tf", STD, course="geometry", prefix="geo")
R = random.Random(808)
def lv(): return R.choice(["cp2", "cp1", "cp1", "honors"])
RULES = {"translation": None, "reflect x-axis": lambda p: (p[0], -p[1]), "reflect y-axis": lambda p: (-p[0], p[1]), "reflect y = x": lambda p: (p[1], p[0]), "reflect y = -x": lambda p: (-p[1], -p[0]),
         "rotate 90° ccw": lambda p: (-p[1], p[0]), "rotate 180°": lambda p: (-p[0], -p[1]), "rotate 270° ccw": lambda p: (p[1], -p[0])}
WORDS = {"reflect x-axis": "a reflection over the x-axis", "reflect y-axis": "a reflection over the y-axis", "reflect y = x": "a reflection over the line y = x", "reflect y = -x": "a reflection over the line y = -x",
         "rotate 90° ccw": "a rotation of 90° counterclockwise about the origin", "rotate 180°": "a rotation of 180° about the origin", "rotate 270° ccw": "a rotation of 270° counterclockwise (90° clockwise) about the origin"}
RULETXT = {"reflect x-axis": "(x, y) → (x, -y)", "reflect y-axis": "(x, y) → (-x, y)", "reflect y = x": "(x, y) → (y, x)", "reflect y = -x": "(x, y) → (-y, -x)", "rotate 90° ccw": "(x, y) → (-y, x)", "rotate 180°": "(x, y) → (-x, -y)", "rotate 270° ccw": "(x, y) → (y, -x)"}
def rp(): return (R.randint(-7, 7), R.randint(-7, 7))
def tri():
    while True:
        T = [rp() for _ in range(3)]
        if (T[1][0] - T[0][0]) * (T[2][1] - T[0][1]) != (T[2][0] - T[0][0]) * (T[1][1] - T[0][1]) and all(abs(c) <= 6 for p in T for c in p): return T
def sh(v, c): return v if c == 0 else f"{v} {'+' if c > 0 else '-'} {abs(c)}"
def tr_txt(a, b): return f"(x, y) → ({sh('x', a)}, {sh('y', b)})"
NF = [0]
def grid_fig(T, img, alt):
    NF[0] += 1
    xs = [p[0] for p in T + img]; ys = [p[1] for p in T + img]; m = max(max(map(abs, xs)), max(map(abs, ys)), 4) + 1
    return graph(B, f"grid-{NF[0]}", [(("seg", [p[0] for p in T + [T[0]]], [p[1] for p in T + [T[0]]]), {}), (("seg", [p[0] for p in img + [img[0]]], [p[1] for p in img + [img[0]]]), {"color": "#c0392b", "ls": "--"})],
                 xr=(-m, m), yr=(-m, m), points=[(p[0], p[1], True, n) for p, n in zip(T, "ABC")] + [(p[0], p[1], True, n + "′") for p, n in zip(img, "ABC")], alt=alt)

# ---- Skill 1: translations ----
def mk_tr():
    P_ = rp(); a, b = R.randint(-6, 6), R.randint(-6, 6)
    if a == 0 and b == 0: raise AssertionError
    k = R.random()
    if k < 0.4: B.sa(1, lv(), f"Translate P{pt(*P_)} by {tr_txt(a, b)}.", pt(P_[0] + a, P_[1] + b), ["Add to each coordinate."])
    elif k < 0.7: B.mc(1, lv(), f"A translation maps P{pt(*P_)} to P′{pt(P_[0] + a, P_[1] + b)}. Which rule describes it?", tr_txt(a, b), [tr_txt(-a, -b), tr_txt(b, a), tr_txt(a, -b) if b else tr_txt(a + 1, b)], ["Rule = image - preimage."], tags=["misconception"])
    else:
        T = tri(); img = [(p[0] + a, p[1] + b) for p in T]
        if R.random() < 0.5:
            dg = grid_fig(T, img, f"Triangle ABC (solid) and its translated image A′B′C′ (dashed) on a grid; A{pt(*T[0])}, A′{pt(*img[0])}.")
            B.orq(1, lv(), "The graph shows △ABC and its translation image △A′B′C′.", [("Write the translation rule.", tr_txt(a, b)), ("Find B′.", pt(*img[1])), ("How far did each point move?", rad(a * a + b * b)), ("Are the triangles congruent?", "Yes: translations are rigid motions")], ["A′ - A.", "Apply the rule.", "Length of the translation vector.", "Rigid motion."], diagram=dg, tags=["graph"])
        else:
            B.sa(1, lv(), f"△ABC has A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])}. Find the image vertices under {tr_txt(a, b)}.", ", ".join(pt(*p) for p in img), ["Add to every vertex."])
def mk_tr_sel():
    a, b = R.randint(-5, 5), R.randint(-5, 5); P_ = rp()
    cands = [pt(P_[0] + a, P_[1] + b), pt(P_[0] - a, P_[1] - b), pt(P_[0] + b, P_[1] + a)]
    st = {f"P′ = {cands[0]}": True, f"The vector is ⟨{a}, {b}⟩": True, "Every point moves the same distance": True, f"P′ = {cands[1]}": cands[1] == cands[0], "Orientation is reversed": False}
    B.sel(1, lv(), f"P{pt(*P_)} is translated by {tr_txt(a, b)}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Translations add a constant vector and preserve orientation."])

# ---- Skills 2 & 3: reflections and rotations ----
def mk_rule(kind_set, S_):
    def f():
        r = R.choice(kind_set); P_ = rp(); img = RULES[r](P_)
        if img == P_: raise AssertionError
        k = R.random()
        if k < 0.45:
            B.sa(S_, lv(), f"Find the image of P{pt(*P_)} under {WORDS[r]}.", pt(*img), [f"Rule: {RULETXT[r]}."])
        elif k < 0.75:
            others = [RULES[o](P_) for o in RULES if o not in ("translation", r)]
            B.mc(S_, lv(), f"Find the image of P{pt(*P_)} under {WORDS[r]}.", pt(*img), [pt(*o) for o in others if o != img][:3], [f"Rule: {RULETXT[r]}."], tags=["misconception"])
        else:
            T = tri(); im = [RULES[r](p) for p in T]
            dg = grid_fig(T, im, f"Triangle ABC (solid) and its image A′B′C′ (dashed) under a {'reflection' if 'reflect' in r else 'rotation'}; A{pt(*T[0])} maps to A′{pt(*im[0])}.")
            B.orq(S_, lv(), "The graph shows △ABC and its image.", [("Name the transformation.", WORDS[r]), ("Write the coordinate rule.", RULETXT[r]), ("Find C′.", pt(*im[2])), ("Is orientation preserved?", "No" if "reflect" in r else "Yes")], ["Compare A and A′.", "Coordinate rule.", "Apply the rule.", "Reflections reverse orientation; rotations keep it."], diagram=dg, tags=["graph"])
    return f
def mk_ref_line():
    P_ = rp(); line = R.choice(["x = 2", "x = -3", "y = 1", "y = -4", "x = 5"])
    v = int(line.split("= ")[1])
    img = (2 * v - P_[0], P_[1]) if line[0] == "x" else (P_[0], 2 * v - P_[1])
    if img == P_: raise AssertionError
    B.sa(2, lv(), f"Reflect P{pt(*P_)} over the line {line}.", pt(*img), ["The line is the perpendicular bisector of PP′.", f"Distance to the line is preserved."])
def mk_ref_sel():
    P_ = rp(); img = (P_[1], P_[0])
    if img == P_: raise AssertionError
    st = {f"P′ = {pt(*img)}": True, "The line y = x is the perpendicular bisector of PP′": True, "Distance to the line is preserved": True, f"P′ = {pt(-P_[0], -P_[1])}": False, "Orientation is preserved": False}
    B.sel(2, lv(), f"P{pt(*P_)} is reflected over y = x. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Swap coordinates; reflections reverse orientation."])
def mk_rot_center():
    P_ = rp(); C_ = (R.randint(-3, 3), R.randint(-3, 3)); r = R.choice(["rotate 90° ccw", "rotate 180°", "rotate 270° ccw"])
    rel = (P_[0] - C_[0], P_[1] - C_[1]); im = RULES[r](rel); img = (im[0] + C_[0], im[1] + C_[1])
    if C_ == (0, 0) or img == P_: raise AssertionError
    B.mc(3, "honors", f"Rotate P{pt(*P_)} {WORDS[r].split(' about')[0].replace('a rotation of ', '')} about C{pt(*C_)}.", pt(*img), [pt(*RULES[r](P_)), pt(img[0] + 1, img[1]), pt(*RULES[r](rel))], ["Translate so C is at the origin, rotate, translate back."], tags=["challenge"])
def mk_rot_angle():
    n = R.choice([3, 4, 5, 6, 8, 10, 12]); B.sa(3, lv(), f"What is the smallest positive angle of rotation that maps a regular {PN[n]} onto itself?", f"{fr(F(360, n))}°", ["360°/n."])

# ---- Skill 4: compositions ----
def mk_comp():
    P_ = rp(); r1, r2 = R.sample([k for k in RULES if k != "translation"], 2); a, b = R.randint(-5, 5), R.randint(-5, 5)
    kind = R.random()
    if kind < 0.5:
        img = RULES[r2](RULES[r1](P_))
        B.sa(4, lv(), f"Find the image of P{pt(*P_)} after {WORDS[r1]} followed by {WORDS[r2]}.", pt(*img), ["Apply the first transformation, then the second.", f"{RULETXT[r1]}, then {RULETXT[r2]}."])
    else:
        i1 = RULES[r1](P_); img = (i1[0] + a, i1[1] + b); alt = RULES[r1]((P_[0] + a, P_[1] + b))
        B.mc(4, lv(), f"Find the image of P{pt(*P_)} after {WORDS[r1]} followed by the translation {tr_txt(a, b)}.", pt(*img), [pt(*alt), pt(i1[0] - a, i1[1] - b), pt(*i1)], ["Order matters: transform first, then translate."], tags=["misconception"])
def mk_comp_id():
    pairs = [("reflect x-axis", "reflect y-axis", "a rotation of 180° about the origin"), ("rotate 90° ccw", "rotate 90° ccw", "a rotation of 180° about the origin"), ("reflect y = x", "reflect x-axis", "a rotation of 270° counterclockwise about the origin"),
             ("reflect x-axis", "reflect y = x", "a rotation of 90° counterclockwise about the origin"), ("rotate 180°", "rotate 180°", "the identity (no change)")]
    r1, r2, res = R.choice(pairs)
    P_ = (3, 1); assert RULES[r2](RULES[r1](P_)) == {"a rotation of 180° about the origin": (-3, -1), "a rotation of 270° counterclockwise about the origin": (1, -3), "a rotation of 90° counterclockwise about the origin": (-1, 3), "the identity (no change)": (3, 1)}[res]
    B.mc(4, lv(), f"{WORDS[r1].capitalize()} followed by {WORDS[r2]} is equivalent to which single transformation?", res, [x for x in ["a rotation of 180° about the origin", "a rotation of 90° counterclockwise about the origin", "a reflection over the line y = x", "a translation", "the identity (no change)", "a rotation of 270° counterclockwise about the origin"] if x != res][:3], ["Test a point such as (3, 1)."], tags=["reasoning"])
def mk_comp_orq():
    T = tri(); r = R.choice(["reflect x-axis", "reflect y-axis", "rotate 90° ccw"]); a, b = R.randint(-4, 4), R.randint(-4, 4)
    mid = [RULES[r](p) for p in T]; fin = [(p[0] + a, p[1] + b) for p in mid]
    B.orq(4, lv(), f"△ABC has A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])}. Apply {WORDS[r]}, then {tr_txt(a, b)}.", [("Find the vertices after the first step.", ", ".join(pt(*p) for p in mid)), ("Find the final vertices.", ", ".join(pt(*p) for p in fin)), ("Is the final triangle congruent to △ABC?", "Yes"), ("Would reversing the order give the same image?", "Not in general")],
          ["Apply the rule.", "Translate.", "Composition of rigid motions.", "Compositions are not commutative."])

# ---- Skill 5: rigid motions and congruence ----
def mk_rig():
    q = R.choice([("Which transformation is NOT a rigid motion?", "a dilation with scale factor 3", ["a translation", "a reflection", "a rotation"]), ("Rigid motions preserve…", "distance and angle measure", ["only angle measure", "only orientation", "only area"]),
                  ("Two figures are congruent exactly when…", "a sequence of rigid motions maps one onto the other", ["they have equal perimeters", "they have equal areas", "a dilation maps one onto the other"]),
                  ("Which property can a rigid motion change?", "orientation (for reflections)", ["side lengths", "angle measures", "area"]), ("Under a rigid motion, the image of a line is…", "a line", ["a curve", "a point", "a parallel line always"])])
    B.mc(5, lv(), q[0], q[1], q[2], ["Definition of rigid motion and congruence."])
def mk_rig_find():
    T = tri(); r = R.choice([k for k in RULES if k != "translation"]); a, b = R.randint(-3, 3), R.randint(-3, 3)
    img = [(RULES[r](p)[0] + a, RULES[r](p)[1] + b) for p in T]
    B.sa(5, "honors", f"△ABC has A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])}; △A′B′C′ has A′{pt(*img[0])}, B′{pt(*img[1])}, C′{pt(*img[2])}. Describe a sequence of rigid motions mapping △ABC to △A′B′C′.", f"{WORDS[r]}, then the translation {tr_txt(a, b)}" if (a, b) != (0, 0) else WORDS[r],
         ["Compare orientation to decide reflection vs. rotation.", "Then find the translation that matches one vertex."], tags=["challenge"])
def mk_rig_sel():
    d = lambda p, q: (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    T = tri(); r = R.choice(["reflect y-axis", "rotate 180°", "reflect y = x"]); img = [RULES[r](p) for p in T]
    st = {f"A′B′ = AB = {rad(d(T[0], T[1]))}": True, "△A′B′C′ ≅ △ABC": True, "m∠A′ = m∠A": True, f"A′B′ = {d(T[0], T[1])}": False, "The area doubles": False}
    B.sel(5, lv(), f"△ABC with A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])} undergoes {WORDS[r]}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Rigid motions preserve lengths, angles, and area."])

# ---- Skill 6: dilations ----
def mk_dil():
    k = R.choice([F(2), F(3), F(1, 2), F(1, 3), F(3, 2), F(5, 2)]); P_ = (R.randint(-6, 6) * 2, R.randint(-6, 6) * 2)
    kind = R.random()
    if kind < 0.4: B.sa(6, lv(), f"Dilate P{pt(*P_)} by scale factor {fr(k)} about the origin.", pt(k * P_[0], k * P_[1]), ["Multiply coordinates by k."])
    elif kind < 0.7:
        C_ = (R.randint(-3, 3), R.randint(-3, 3)); img = (C_[0] + k * (P_[0] - C_[0]), C_[1] + k * (P_[1] - C_[1]))
        B.mc(6, "honors", f"Dilate P{pt(*P_)} by scale factor {fr(k)} about C{pt(*C_)}.", pt(*img), [pt(k * P_[0], k * P_[1]), pt(C_[0] + k * P_[0], C_[1] + k * P_[1]), pt(P_[0] + k, P_[1] + k)], ["P′ = C + k(P - C)."], tags=["misconception"])
    else:
        L_ = R.randint(2, 12); B.sa(6, lv(), f"A segment of length {L_} is dilated by {fr(k)}. Find the image length and say whether it is an enlargement or reduction.", f"{fr(k * L_)}; {'enlargement' if k > 1 else 'reduction'}", ["Lengths scale by k."])
def mk_dil_k():
    P_ = (R.randint(1, 6), R.randint(1, 6)); k = R.choice([2, 3, 4, F(1, 2)])
    img = (k * P_[0], k * P_[1])
    B.mc(6, lv(), f"A dilation about the origin maps P{pt(*P_)} to P′{pt(*img)}. Find the scale factor.", fr(k), [fr(1 / F(k)), fr(img[0] - P_[0]), fr(F(k) * 2)], ["k = OP′/OP."])
def mk_dil_area():
    k = R.choice([2, 3, F(1, 2), F(3, 2)]); A_ = R.randint(4, 40)
    B.sa(6, lv(), f"A figure with area {A_} cm² is dilated by scale factor {fr(k)}. Find the new area.", f"{fr(F(k) ** 2 * A_)} cm²", ["Areas scale by k²."], tags=["misconception"])

# ---- Skill 7: similarity transformations ----
def mk_simtr():
    T = tri(); k = R.choice([2, 3]); r = R.choice(["reflect x-axis", "rotate 90° ccw", "rotate 180°"])
    img = [(k * RULES[r](p)[0], k * RULES[r](p)[1]) for p in T]
    if R.random() < 0.5:
        B.orq(7, lv(), f"△ABC: A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])}; △A′B′C′: A′{pt(*img[0])}, B′{pt(*img[1])}, C′{pt(*img[2])}.", [("Find the scale factor.", str(k)), ("Name the rigid motion involved.", WORDS[r]), ("Are the triangles similar?", "Yes"), ("Are they congruent?", "No (k ≠ 1)")], ["Compare side lengths.", "Compare orientation/position after undoing the dilation.", "Similarity transformation.", "Lengths change."])
    else:
        B.mc(7, lv(), f"A similarity transformation maps A{pt(*T[0])} to A′{pt(*img[0])} and B{pt(*T[1])} to B′{pt(*img[1])}. Which sequence could it be?", f"{WORDS[r]}, then a dilation by {k} about the origin", [f"a dilation by {k} only", f"{WORDS[r]} only", f"a dilation by {fr(F(1, k))}, then {WORDS[r]}"], ["Test both points."])
def mk_simtr_sel():
    st = {"Corresponding angles are congruent": True, "Corresponding sides are proportional": True, "Shape is preserved": True, "Size is always preserved": False, "Orientation is always preserved": False}
    keys = list(st); R.shuffle(keys)
    prompt = R.choice(["A dilation followed by a reflection maps △ABC to △DEF. Select ALL statements that must be true.", "A rotation followed by a dilation maps △PQR to △STU. Select ALL statements that must be true.", "A similarity transformation maps polygon ABCD to WXYZ. Select ALL statements that must be true."])
    B.sel(7, lv(), prompt, [k for k in keys if st[k]], [k for k in keys if not st[k]], ["Similarity transformations preserve angles and proportionality."])
def mk_simtr_aa():
    a, b = R.randint(30, 80), R.randint(30, 80)
    B.sa(7, lv(), f"Explain using similarity transformations why two triangles with angles {a}°, {b}°, {180 - a - b}° are similar.", "Dilate one triangle so a pair of corresponding sides match; then rigid motions map it onto the other (ASA), so a similarity transformation maps one to the other", ["AA follows from dilation + congruence."], tags=["reasoning"])

# ---- Skill 8: symmetry ----
def mk_sym():
    n = R.choice([3, 4, 5, 6, 8, 10]); kind = R.random()
    if kind < 0.5: B.sa(8, lv(), f"How many lines of symmetry does a regular {PN[n]} have?", str(n), ["A regular n-gon has n lines of symmetry."])
    else: B.mc(8, lv(), f"Which rotations (0° < θ ≤ 360°) map a regular {PN[n]} onto itself?", f"multiples of {fr(F(360, n))}°", [f"multiples of {fr(F(180, n))}°", "only 180°", f"multiples of {n}°"], ["Rotational symmetry of order n."])
def mk_sym_shape():
    shapes = [("rectangle (not square)", 2, "180°"), ("rhombus (not square)", 2, "180°"), ("square", 4, "90°"), ("isosceles trapezoid", 1, "none"), ("parallelogram (not rectangle or rhombus)", 0, "180°"), ("kite (not rhombus)", 1, "none"), ("equilateral triangle", 3, "120°")]
    sh, lines, rot = R.choice(shapes)
    if R.random() < 0.5:
        B.mc(8, lv(), f"How many lines of symmetry does a {sh} have?", str(lines), [str(x) for x in range(5) if x != lines][:3], ["Count the reflection lines."])
    else:
        B.mc(8, lv(), f"What is the smallest rotation (less than 360°) that maps a {sh} onto itself?", rot, [x for x in ["90°", "120°", "180°", "none"] if x != rot][:3], ["Rotational symmetry."])
def mk_sym_sel():
    q = R.choice([("Select ALL figures with exactly two lines of symmetry.", ["rectangle (not square)", "rhombus (not square)"], ["square", "isosceles trapezoid", "kite"]), ("Select ALL figures with 180° rotational symmetry.", ["parallelogram", "rectangle", "rhombus", "square"], ["kite", "isosceles trapezoid", "equilateral triangle"]),
                  ("Select ALL letters with a vertical line of symmetry.", ["A", "M", "T", "U"], ["F", "J", "N"]), ("Select ALL properties preserved (invariant) under any rigid motion.", ["length", "angle measure", "area", "parallelism"], ["position", "orientation (under reflections)"])])
    B.sel(8, lv(), q[0], q[1], q[2], ["Check each figure or property."])

# ---- Skill 9: coordinate proofs ----
def mk_cproof():
    kind = R.choice(["mid", "par", "rhombus", "right", "iso"])
    if kind == "mid":
        a, b, c = R.randint(1, 5) * 2, R.randint(1, 5) * 2, R.randint(1, 5) * 2
        B.orq(9, lv(), f"Use coordinates A(0, 0), B({2 * a}, 0), C({2 * b}, {2 * c}) to prove the Triangle Midsegment Theorem for midsegment DE (D on AC, E on BC).", [("Find D and E.", f"({b}, {c}) and ({a + b}, {c})"), ("Find the slope of DE.", "0 (horizontal)"), ("Compare DE with AB.", f"DE = {a}, AB = {2 * a}: DE = ½AB"), ("Conclude.", "DE ∥ AB and DE = ½AB")], ["Midpoint formula.", "Same y-coordinates.", "Lengths.", "Theorem verified."], tags=["reasoning"])
    elif kind == "par":
        a, b, c = R.randint(2, 6), R.randint(1, 4), R.randint(2, 6)
        B.orq(9, lv(), f"Parallelogram with A(0, 0), B({a}, 0), C({a + b}, {c}), D({b}, {c}). Prove the diagonals bisect each other.", [("Midpoint of AC.", pt(F(a + b, 2), F(c, 2))), ("Midpoint of BD.", pt(F(a + b, 2), F(c, 2))), ("What does equality show?", "the diagonals share their midpoint"), ("Conclude.", "they bisect each other")], ["Midpoint formula.", "Midpoint formula.", "Same point.", "Definition of bisect."], tags=["reasoning"])
    elif kind == "rhombus":
        B.mc(9, lv(), "To prove a parallelogram with vertices A(0, 0), B(5, 0), C(8, 4), D(3, 4) is a rhombus, which calculation suffices?", "Show AB = AD (both 5)", ["Show AC = BD", "Show AB ∥ DC", "Show the area is 20"], ["A parallelogram with two consecutive sides congruent is a rhombus.", "AB = 5; AD = √(9 + 16) = 5."], tags=["reasoning"])
    elif kind == "right":
        a, b = R.randint(2, 8), R.randint(2, 8)
        B.sa(9, lv(), f"Right △ with C(0, 0), A({2 * a}, 0), B(0, {2 * b}). Show the midpoint M of the hypotenuse is equidistant from all three vertices.", f"M({a}, {b}); MA = MB = MC = {rad(a * a + b * b)}", ["Midpoint of AB.", "Distance formula to each vertex."], tags=["reasoning"])
    else:
        a, h = R.randint(2, 7), R.randint(2, 9)
        B.sa(9, lv(), f"Isosceles △ with A({-a}, 0), B({a}, 0), C(0, {h}). Show CA = CB and find the reflection that maps the triangle onto itself.", f"CA = CB = {rad(a * a + h * h)}; reflection over the y-axis", ["Distance formula.", "(x, y) → (-x, y) swaps A and B and fixes C."], tags=["reasoning"])
def mk_cproof_place():
    q = R.choice([("Which placement is most convenient for a coordinate proof about a rectangle?", "(0, 0), (a, 0), (a, b), (0, b)", ["(1, 2), (5, 2), (5, 7), (1, 7)", "(a, b), (c, d), (e, f), (g, h)", "(0, 0), (a, a), (b, b), (c, c)"]),
                  ("Which vertices are general enough for a proof about any triangle?", "(0, 0), (2a, 0), (2b, 2c)", ["(0, 0), (4, 0), (2, 3)", "(0, 0), (a, 0), (0, a)", "(1, 1), (2, 2), (3, 3)"])])
    B.mc(9, lv(), q[0], q[1], q[2], ["Use variables for generality and place vertices on axes for simplicity.", "Using 2a, 2b, 2c avoids fractions in midpoints."], tags=["reasoning"])

makers = {1: [mk_tr, mk_tr, mk_tr_sel], 2: [mk_rule(["reflect x-axis", "reflect y-axis", "reflect y = x", "reflect y = -x"], 2), mk_ref_line, mk_ref_sel], 3: [mk_rule(["rotate 90° ccw", "rotate 180°", "rotate 270° ccw"], 3), mk_rot_center, mk_rot_angle],
          4: [mk_comp, mk_comp, mk_comp_id, mk_comp_orq], 5: [mk_rig, mk_rig_find, mk_rig_sel], 6: [mk_dil, mk_dil, mk_dil_k, mk_dil_area], 7: [mk_simtr, mk_simtr_sel, mk_simtr_aa], 8: [mk_sym, mk_sym_shape, mk_sym_sel], 9: [mk_cproof, mk_cproof, mk_cproof_place]}
for S_, ms in makers.items():
    fill(B, S_, 32, ms, R)

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
