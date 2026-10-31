from lib import Bank
from mathlite import *
from geofig import Fig
from fill import fill
import math, random

STD = {1: ["G-SRT.C.8"], 2: ["G-SRT.C.8"], 3: ["G-SRT.C.8"], 4: ["G-SRT.C.8"], 5: ["G-SRT.B.5"], 6: ["G-SRT.C.6", "G-SRT.C.7"], 7: ["G-SRT.C.8"], 8: ["G-SRT.C.8"], 9: ["G-SRT.C.8", "G-MG.A.1"], 10: ["G-SRT.C.8", "G-MG.A.1"]}
B = Bank("right-triangles-trigonometry", "rt", STD, course="geometry", prefix="geo")
R = random.Random(606)
sin, cos, tan, deg, rad_ = math.sin, math.cos, math.tan, math.degrees, math.radians
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (6, 8, 10), (9, 12, 15), (12, 16, 20), (15, 20, 25), (10, 24, 26)]
def lv(): return R.choice(["cp2", "cp1", "cp1", "honors"])
def d1(v): return f"{v:.1f}"
def d2(v): return f"{v:.2f}"
NFIG = [0]


def rt_fig(a, b, labs, ang=None, alt_extra=""):
    """Right triangle with right angle at C (origin), legs CB = a (horizontal) and CA = b (vertical). labs: dict 'a','b','c' → text."""
    NFIG[0] += 1
    C, Bv, A = (0.0, 0.0), (float(a), 0.0), (0.0, float(b))
    fg = Fig(3.8, 3.0); fg.poly([A, Bv, C]); fg.names([A, Bv, C], ["A", "B", "C"]); fg.angle(C, Bv, A, right=True, r=0.12 * max(a, b))
    cen = (a / 3, b / 3)
    if "a" in labs: fg.side(C, Bv, labs["a"], center=cen)
    if "b" in labs: fg.side(C, A, labs["b"], center=cen)
    if "c" in labs: fg.side(A, Bv, labs["c"], center=cen)
    if ang: fg.angle(Bv, A, C, ang, r=0.16 * max(a, b))
    return fg.save(B, f"rt-{NFIG[0]}", f"Right triangle ABC with the right angle at C; leg BC (bottom) labeled {labs.get('a', 'unlabeled')}, leg AC (left) labeled {labs.get('b', 'unlabeled')}, hypotenuse AB labeled {labs.get('c', 'unlabeled')}" + (f", angle B labeled {ang}" if ang else "") + f". {alt_extra}".rstrip())

# ---- Skill 1: Pythagorean theorem ----
for k_, (a, b, c) in enumerate(TRIPLES[:6]):
    hide = ["c", "a", "b"][k_ % 3]
    labs = {"a": str(a), "b": str(b), "c": str(c)}; labs[hide] = "x"
    sc = 6 / max(a, b)
    dg = rt_fig(a * sc, b * sc, labs)
    B.sa(1, "cp2" if hide == "c" else "cp1", "Find x in the right triangle.", str({"a": a, "b": b, "c": c}[hide]), ["a² + b² = c².", f"x = {({'a': a, 'b': b, 'c': c})[hide]}."], diagram=dg, tags=["graph"])
def mk_pyth():
    a, b = R.randint(2, 15), R.randint(2, 15)
    if R.random() < 0.5:
        B.sa(1, lv(), f"The legs of a right triangle are {a} and {b}. Find the hypotenuse in simplest radical form.", rad(a * a + b * b), [f"√({a}² + {b}²) = √{a * a + b * b}."])
    else:
        c = max(a, b) + R.randint(1, 8); leg = min(a, b)
        B.mc(1, lv(), f"A right triangle has hypotenuse {c} and one leg {leg}. Find the other leg.", rad(c * c - leg * leg), [rad(c * c + leg * leg), str(c - leg), rad(abs(c - leg))], ["Leg = √(c² - a²)."], tags=["misconception"])
def mk_pyth_app():
    a, b, c = R.choice(TRIPLES); k = R.choice([1, 2, 3])
    ctx = R.choice([(f"A {c * k}-ft ladder reaches {b * k} ft up a wall. How far is its base from the wall?", f"{a * k} ft"), (f"A TV screen is {a * k} in tall and {b * k} in wide. Find the diagonal.", f"{c * k} in"),
                    (f"You walk {a * k} blocks east and {b * k} blocks north. How far are you from the start (straight line)?", f"{c * k} blocks")])
    B.sa(1, lv(), ctx[0], ctx[1], ["Draw the right triangle and use a² + b² = c²."], tags=["modeling"])
def mk_pyth_orq():
    a, b, c = R.choice(TRIPLES)
    B.orq(1, lv(), f"A rectangle is {a} by {b}.", [("Find the diagonal.", str(c)), ("Find the perimeter.", str(2 * (a + b))), ("Find the area.", str(a * b)), ("How much shorter is walking the diagonal than two sides?", str(a + b - c))], ["Pythagorean theorem.", "2(l + w).", "lw.", "(a + b) - c."], tags=["modeling"])

# ---- Skill 2: converse ----
def mk_conv():
    if R.random() < 0.5:
        a, b, c = R.choice(TRIPLES); k = R.choice([1, 2])
        s = [a * k, b * k, c * k]
    else:
        s = sorted(R.sample(range(3, 25), 3))
        if s[0] + s[1] <= s[2]: raise AssertionError
    a, b, c = sorted(s); v = a * a + b * b - c * c; kind = "right" if v == 0 else ("acute" if v > 0 else "obtuse")
    if R.random() < 0.6:
        B.mc(2, lv(), f"A triangle has sides {a}, {b}, {c}. Is it acute, right, or obtuse?", kind, [k for k in ["acute", "right", "obtuse", "not a triangle"] if k != kind][:3], [f"{a}² + {b}² = {a * a + b * b}; {c}² = {c * c}.", "Equal → right; greater → acute; less → obtuse."])
    else:
        B.sa(2, lv(), f"Do {a}, {b}, {c} form a right triangle? Justify.", f"{'Yes' if v == 0 else 'No'}: {a}² + {b}² = {a * a + b * b} {'=' if v == 0 else '≠'} {c * c}", ["Converse of the Pythagorean Theorem."])
def mk_conv_sel():
    sets = [(5, 12, 13), (6, 7, 9), (9, 12, 15), (4, 5, 6), (8, 15, 17), (2, 3, 4), (7, 24, 25), (10, 10, 14)]
    pick = R.sample(sets, 5)
    if sum(a * a + b * b == c * c for a, b, c in pick) < 2 or sum(a * a + b * b != c * c for a, b, c in pick) < 1: raise AssertionError
    sel_auto(B, 2, lv(), "Select ALL side lengths that form right triangles.", [f"{a}, {b}, {c}" for a, b, c in pick], lambda s_: (lambda a, b, c: a * a + b * b == c * c)(*map(int, s_.split(", "))), ["Check a² + b² = c² with c the longest."])
def mk_conv_x():
    a, b, c = R.choice(TRIPLES)
    B.sa(2, lv(), f"For what whole-number values of x is a triangle with sides {a}, {b}, x (x the longest side) obtuse?", f"{c + 1} ≤ x ≤ {a + b - 1}", [f"Obtuse: x² > {a * a + b * b} → x > {c}.", f"Triangle inequality: x < {a + b}."], tags=["challenge"])

# ---- Skill 3: 45-45-90 ----
def mk_45():
    k = R.randint(2, 15)
    kind = R.choice(["leg", "hyp", "hyp_int"])
    if kind == "leg":
        B.sa(3, lv(), f"A 45°-45°-90° triangle has legs of length {k}. Find the hypotenuse.", f"{k}√2", ["Hypotenuse = leg·√2."])
    elif kind == "hyp":
        B.mc(3, lv(), f"A 45°-45°-90° triangle has hypotenuse {k}√2. Find each leg.", str(k), [f"{k}√2/2", str(2 * k), f"{k}/2"], ["Leg = hypotenuse/√2."])
    else:
        B.sa(3, lv(), f"A 45°-45°-90° triangle has hypotenuse {2 * k}. Find each leg.", f"{k}√2", [f"Leg = {2 * k}/√2 = {k}√2."])
def mk_45_app():
    s = R.randint(3, 20)
    B.mc(3, lv(), f"A square has side {s}. Find its diagonal.", f"{s}√2", [f"{s}√3", f"{2 * s}", f"{s}/√2"], ["The diagonal splits the square into two 45°-45°-90° triangles."], tags=["connections"])
dg = rt_fig(4, 4, {"a": "7", "b": "x", "c": "y"}, ang="45°")
B.orq(3, "cp1", "Use the figure.", [("Find x.", "7"), ("Find y.", "7√2"), ("What type of triangle is it?", "isosceles right (45°-45°-90°)"), ("Find the area.", "49/2")], ["Legs congruent.", "leg·√2.", "Two 45° angles.", "½·7·7."], diagram=dg, tags=["graph"])

# ---- Skill 4: 30-60-90 ----
def mk_30():
    s = R.randint(2, 14); kind = R.choice(["short", "hyp", "long"])
    if kind == "short":
        B.sa(4, lv(), f"In a 30°-60°-90° triangle the shorter leg is {s}. Find the longer leg and the hypotenuse.", f"{s}√3 and {2 * s}", ["Longer leg = short·√3; hypotenuse = 2·short."])
    elif kind == "hyp":
        B.mc(4, lv(), f"A 30°-60°-90° triangle has hypotenuse {2 * s}. Find the longer leg.", f"{s}√3", [str(s), f"{2 * s}√3", f"{s}√2"], ["Short leg = hyp/2; long = short·√3."], tags=["misconception"])
    else:
        B.sa(4, lv(), f"A 30°-60°-90° triangle has longer leg {3 * s}. Find the shorter leg and hypotenuse.", f"{s}√3 and {2 * s}√3", [f"Short = {3 * s}/√3 = {s}√3.", "Hypotenuse = 2·short."])
def mk_30_app():
    s = R.randint(2, 12) * 2
    B.mc(4, lv(), f"An equilateral triangle has side {s}. Find its height.", f"{s // 2}√3", [f"{s}√3", f"{s // 2}", f"{s}√2/2"], ["The altitude splits it into 30°-60°-90° triangles with short leg s/2."], tags=["connections"])
def mk_sp_sel():
    s = R.randint(2, 10)
    st = {f"The hypotenuse is {2 * s}": True, f"The longer leg is {s}√3": True, f"The area is {fr(F(s * s, 2))}√3": True, f"The longer leg is {2 * s}": False, f"The hypotenuse is {s}√3": False}
    B.sel(4, lv(), f"A 30°-60°-90° triangle has shorter leg {s}. Select ALL true statements.", [a for a, t in st.items() if t], [a for a, t in st.items() if not t], ["Ratios 1 : √3 : 2."])
dg = rt_fig(6 * 3 ** .5 / 1.5, 6 / 1.5, {"a": "x", "b": "6", "c": "y"}, ang="30°")
B.orq(4, "cp1", "Use the figure (angle B = 30°).", [("Which side is shortest?", "AC (opposite 30°)"), ("Find y.", "12"), ("Find x.", "6√3"), ("Find the perimeter.", "18 + 6√3")], ["Opposite the smallest angle.", "hyp = 2·short.", "long = short·√3.", "Sum."], diagram=dg, tags=["graph"])

# ---- Skill 5: geometric mean and altitudes ----
def mk_gm():
    a, b = R.choice([(2, 8), (4, 9), (3, 12), (1, 16), (5, 20), (6, 24), (2, 18), (4, 16), (3, 6), (5, 10), (2, 7)])
    kind = R.choice(["alt", "leg", "gm", "seg"])
    if kind == "alt":
        B.sa(5, lv(), f"The altitude to the hypotenuse divides it into segments {a} and {b}. Find the altitude.", rad(a * b), ["h = √(ab)."])
    elif kind == "leg":
        B.mc(5, lv(), f"The altitude to the hypotenuse divides it into segments {a} and {b}. Find the leg adjacent to the segment of length {a}.", rad(a * (a + b)), [rad(a * b), rad(b * (a + b)), rad(a * a + b * b)], ["Leg² = (adjacent segment)(hypotenuse)."], tags=["misconception"])
    elif kind == "gm":
        B.sa(5, lv(), f"Find the geometric mean of {a} and {b}.", rad(a * b), ["√(ab)."])
    else:
        h2 = a * b
        B.sa(5, lv(), f"The altitude to the hypotenuse is {rad(h2)} and one hypotenuse segment is {a}. Find the other segment.", str(b), [f"h² = {a}·x → x = {h2}/{a}."])
def mk_gm_orq():
    a, b = R.choice([(4, 9), (1, 9), (2, 8), (9, 16), (3, 12)])
    B.orq(5, lv(), f"In right △ABC with right angle C, altitude CD splits AB into AD = {a} and DB = {b}.", [("Find CD.", rad(a * b)), ("Find AC.", rad(a * (a + b))), ("Find BC.", rad(b * (a + b))), ("Verify AC² + BC² = AB².", f"{a * (a + b)} + {b * (a + b)} = {(a + b) ** 2}")], ["Geometric mean.", "Leg rule.", "Leg rule.", "Pythagorean check."])
    assert a * (a + b) + b * (a + b) == (a + b) ** 2

# ---- Skill 6: trig ratios ----
for k_, (a, b, c) in enumerate(TRIPLES[:4]):
    sc = 6 / max(a, b); dg = rt_fig(a * sc, b * sc, {"a": str(a), "b": str(b), "c": str(c)})
    B.orq(6, "cp1" if k_ else "cp2", "Use the right triangle.", [("Find sin A.", f"{a}/{c}"), ("Find cos A.", f"{b}/{c}"), ("Find tan A.", f"{a}/{b}"), ("Find sin B and compare with cos A.", f"sin B = {b}/{c} = cos A")], ["opposite/hypotenuse (BC opposite A).", "adjacent/hypotenuse.", "opposite/adjacent.", "Complementary angles."], diagram=dg, tags=["graph"])
def mk_ratio():
    a, b, c = R.choice(TRIPLES); fn = R.choice(["sin", "cos", "tan"]); ang = R.choice(["A", "B"])
    opp, adj = (a, b) if ang == "A" else (b, a)
    val = {"sin": F(opp, c), "cos": F(adj, c), "tan": F(opp, adj)}[fn]
    B.mc(6, lv(), f"Right △ABC has right angle C, BC = {a}, AC = {b}, AB = {c}. Find {fn} {ang}.", fr(val), [fr(F(adj, c)) if fn != "cos" else fr(F(opp, c)), fr(F(adj, opp)), fr(F(c, opp))], ["SOH-CAH-TOA.", f"Opposite {ang}: {opp}; adjacent: {adj}."], tags=["misconception"])
def mk_cofunc():
    t = R.randint(10, 80)
    B.mc(6, lv(), f"If sin {t}° = k, which also equals k?", f"cos {90 - t}°", [f"cos {t}°", f"tan {90 - t}°", f"sin {90 - t}°"], ["sin θ = cos(90° - θ)."])
def mk_ratio_sel():
    a, b, c = R.choice(TRIPLES)
    st = {f"sin A = {fr(F(a, c))}": True, f"cos B = {fr(F(a, c))}": True, f"tan B = {fr(F(b, a))}": True, f"tan A = {fr(F(b, a))}": a == b, f"sin B = {fr(F(a, c))}": a == b}
    B.sel(6, lv(), f"Right △ABC: right angle C, BC = {a}, AC = {b}, AB = {c}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Identify opposite/adjacent for each angle."])

# ---- Skill 7: missing sides ----
def mk_side():
    t = R.randint(15, 75); L_ = R.randint(5, 40); kind = R.choice(["opp_hyp", "adj_hyp", "opp_adj", "hyp_from_opp"])
    if kind == "opp_hyp":
        v = L_ * sin(rad_(t)); q = f"hypotenuse {L_}, angle {t}°. Find the side opposite the angle"; fn = f"x = {L_} sin {t}°"
    elif kind == "adj_hyp":
        v = L_ * cos(rad_(t)); q = f"hypotenuse {L_}, angle {t}°. Find the side adjacent to the angle"; fn = f"x = {L_} cos {t}°"
    elif kind == "opp_adj":
        v = L_ * tan(rad_(t)); q = f"adjacent leg {L_}, angle {t}°. Find the opposite leg"; fn = f"x = {L_} tan {t}°"
    else:
        v = L_ / sin(rad_(t)); q = f"opposite leg {L_}, angle {t}°. Find the hypotenuse"; fn = f"x = {L_}/sin {t}°"
    if R.random() < 0.5:
        B.sa(7, lv(), f"A right triangle has {q} (nearest tenth).", d1(v), [fn + ".", f"≈ {d1(v)}."])
    else:
        w = [L_ * cos(rad_(t)), L_ * tan(rad_(t)), L_ / cos(rad_(t)), L_ * sin(rad_(t)), L_ / sin(rad_(t))]
        B.mc(7, lv(), f"A right triangle has {q} (nearest tenth).", d1(v), [d1(x) for x in w if abs(x - v) > 0.05][:3], [fn + "."], tags=["misconception"])
def mk_side_fig():
    t = R.choice([25, 32, 40, 52, 58, 65]); hyp = R.randint(8, 20)
    a = hyp * cos(rad_(t)); b = hyp * sin(rad_(t))
    dg = rt_fig(a / hyp * 6, b / hyp * 6, {"c": str(hyp), "a": "x", "b": "y"}, ang=f"{t}°")
    B.orq(7, lv(), "Use the figure (angle B is marked).", [("Which ratio finds x?", f"cos {t}° = x/{hyp}"), ("Find x (nearest tenth).", d1(a)), ("Find y (nearest tenth).", d1(b)), ("Check with the Pythagorean theorem.", f"{d1(a)}² + {d1(b)}² ≈ {hyp}²")], ["x is adjacent to B.", f"{hyp} cos {t}°.", f"{hyp} sin {t}°.", "Sum of squares."], diagram=dg, tags=["graph"])

# ---- Skill 8: missing angles ----
def mk_angle():
    a, b = R.randint(3, 25), R.randint(3, 25); kind = R.choice(["tan", "sin", "cos"])
    if kind == "tan": v = deg(math.atan(a / b)); q = f"opposite leg {a} and adjacent leg {b}"; f_ = f"tan⁻¹({a}/{b})"
    elif kind == "sin":
        c = max(a, b) + R.randint(1, 10); v = deg(math.asin(min(a, b) / c)); q = f"opposite leg {min(a, b)} and hypotenuse {c}"; f_ = f"sin⁻¹({min(a, b)}/{c})"
    else:
        c = max(a, b) + R.randint(1, 10); v = deg(math.acos(min(a, b) / c)); q = f"adjacent leg {min(a, b)} and hypotenuse {c}"; f_ = f"cos⁻¹({min(a, b)}/{c})"
    if R.random() < 0.5:
        B.sa(8, lv(), f"A right triangle has {q} for angle θ. Find θ to the nearest tenth of a degree.", f"{d1(v)}°", [f"θ = {f_}."])
    else:
        B.mc(8, lv(), f"A right triangle has {q} for angle θ. Find θ (nearest degree).", f"{round(v)}°", [f"{round(90 - v)}°" if round(90 - v) != round(v) else f"{round(v) + 5}°", f"{round(v) + 7}°", f"{max(1, round(v) - 9)}°"], [f"θ = {f_}.", "The complement is the other acute angle."], tags=["misconception"])
def mk_angle_both():
    a, b, c = R.choice(TRIPLES)
    A_ = deg(math.atan(a / b))
    B.orq(8, lv(), f"Right △ABC: right angle C, BC = {a}, AC = {b}.", [("Find AB.", str(c)), ("Find m∠A (nearest tenth).", f"{d1(A_)}°"), ("Find m∠B.", f"{d1(90 - A_)}°"), ("Which ratio did you use for ∠A?", f"tan A = {a}/{b}")], ["Pythagorean theorem.", "tan⁻¹(opp/adj).", "90° - m∠A.", "Opposite over adjacent."])

# ---- Skill 9: elevation and depression ----
def mk_elev():
    t = R.randint(10, 70); d = R.randint(20, 300); kind = R.choice(["elev_height", "dep_dist", "elev_angle"])
    if kind == "elev_height":
        v = d * tan(rad_(t)); B.sa(9, lv(), f"From {d} ft away, the angle of elevation to the top of a building is {t}°. How tall is the building (nearest foot)?", f"{round(v)} ft", [f"h = {d} tan {t}°."], tags=["modeling"])
    elif kind == "dep_dist":
        h = R.randint(50, 900); v = h / tan(rad_(t))
        B.mc(9, lv(), f"From a {h}-ft cliff, the angle of depression to a boat is {t}°. How far is the boat from the base of the cliff (nearest foot)?", f"{round(v)} ft", [f"{round(h * tan(rad_(t)))} ft", f"{round(h / sin(rad_(t)))} ft", f"{round(h * sin(rad_(t)))} ft"], ["The angle of depression equals the angle of elevation from the boat (alternate interior angles).", f"d = {h}/tan {t}°."], tags=["modeling", "misconception"])
    else:
        h = R.randint(20, 200); v = deg(math.atan(h / d))
        B.sa(9, lv(), f"A {h}-ft tower is {d} ft away. Find the angle of elevation to its top (nearest tenth of a degree).", f"{d1(v)}°", [f"θ = tan⁻¹({h}/{d})."], tags=["modeling"])
def mk_elev_two():
    t1, t2 = sorted(R.sample(range(20, 70), 2)); d = R.randint(50, 200)
    # two observations along a line toward a tower: angles t1 (far) and t2 (near), separated by d
    h = d / (1 / tan(rad_(t1)) - 1 / tan(rad_(t2)))
    B.orq(9, "honors", f"Walking toward a tower, the angle of elevation changes from {t1}° to {t2}° over {d} ft.", [("Let x be the final distance. Write h in two ways.", f"h = x tan {t2}° and h = (x + {d}) tan {t1}°"), ("Find x (nearest foot).", f"{round(h / tan(rad_(t2)))} ft"), ("Find h (nearest foot).", f"{round(h)} ft"), ("Why does the angle increase?", "the horizontal distance decreases while the height is fixed")],
          ["Two right triangles share the height.", "Set equal and solve.", "Substitute.", "tan θ = h/x grows as x shrinks."], tags=["modeling", "challenge"])
def mk_elev_sel():
    st = {"The angle of depression from A to B equals the angle of elevation from B to A": True, "Both angles are measured from a horizontal line": True, "The angle of depression is measured from the vertical": False, "The angles of elevation and depression are complementary": False}
    B.sel(9, lv(), "Select ALL true statements about angles of elevation and depression.", [a for a, t in st.items() if t], [a for a, t in st.items() if not t], ["Alternate interior angles with horizontal lines."])

# ---- Skill 10: word problems ----
def mk_word():
    kind = R.choice(["ramp", "kite", "ladder", "plane", "shadow", "slide"])
    if kind == "ramp":
        h = R.choice([1.5, 2, 2.5, 3]); t = R.choice([4.8, 5, 6, 7]); L_ = h / sin(rad_(t))
        B.sa(10, lv(), f"A wheelchair ramp rises {h:g} ft at an angle of {t:g}°. How long is the ramp (nearest tenth of a foot)?", f"{d1(L_)} ft", [f"sin {t:g}° = {h:g}/L."], tags=["modeling"])
    elif kind == "kite":
        L_ = R.randint(50, 200); t = R.randint(30, 70); v = L_ * sin(rad_(t))
        B.sa(10, lv(), f"A kite string is {L_} ft long and makes a {t}° angle with the ground. How high is the kite (nearest foot)?", f"{round(v)} ft", [f"h = {L_} sin {t}°."], tags=["modeling"])
    elif kind == "ladder":
        L_ = R.randint(12, 30); t = R.randint(60, 80); v = L_ * cos(rad_(t))
        B.mc(10, lv(), f"A {L_}-ft ladder makes a {t}° angle with the ground. How far is its base from the wall (nearest tenth)?", f"{d1(v)} ft", [d1(L_ * sin(rad_(t))) + " ft", d1(L_ * tan(rad_(t))) + " ft", d1(L_ / cos(rad_(t))) + " ft"], [f"d = {L_} cos {t}°."], tags=["modeling", "misconception"])
    elif kind == "plane":
        alt = R.randint(2000, 9000); t = R.randint(3, 15); v = alt / sin(rad_(t))
        B.sa(10, lv(), f"A plane at {alt:,} ft begins a straight descent at {t}°. How far (along its path) does it fly to reach the ground (nearest 100 ft)?", f"{round(v, -2):,.0f} ft", [f"d = {alt}/sin {t}°."], tags=["modeling"])
    elif kind == "shadow":
        h = R.randint(10, 80); t = R.randint(25, 65)
        sh = h / tan(rad_(t))
        B.sa(10, lv(), f"A {h}-ft pole casts a {d1(sh)}-ft shadow. Find the sun's angle of elevation (nearest degree).", f"{t}°", [f"tan⁻¹({h}/{d1(sh)})."], tags=["modeling"])
    else:
        h = R.randint(4, 10); t = R.randint(30, 50); L_ = h / sin(rad_(t)); base = h / tan(rad_(t))
        B.orq(10, lv(), f"A slide has a {h}-ft ladder (vertical) and the slide makes a {t}° angle with the ground.", [("Find the slide's length (nearest tenth).", f"{d1(L_)} ft"), ("Find the horizontal distance it covers (nearest tenth).", f"{d1(base)} ft"), ("Which ratios did you use?", "sine and tangent"), ("If the angle increased, would the slide be shorter or longer?", "shorter")], ["sin = h/L.", "tan = h/d.", "SOH, TOA.", "L = h/sin θ decreases as θ increases."], tags=["modeling"])

def mk_pyth_sel():
    a, b, c = R.choice(TRIPLES)
    st = {f"The hypotenuse is {c}": True, f"{a}² + {b}² = {c}²": True, f"The area is {fr(F(a * b, 2))}": True, f"The hypotenuse is {a + b}": False, f"The perimeter is {a + b}": False}
    B.sel(1, lv(), f"A right triangle has legs {a} and {b}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Pythagorean theorem; area = ½ab."])
def mk_45_sel():
    k = R.randint(2, 12)
    st = {f"Each leg is {k}": True, f"The hypotenuse is {k}√2": True, f"The area is {fr(F(k * k, 2))}": True, f"The hypotenuse is {2 * k}": False, f"Each leg is {k}√2": False}
    B.sel(3, lv(), f"A 45°-45°-90° triangle has a leg of length {k}. Select ALL true statements.", [a for a, v in st.items() if v], [a for a, v in st.items() if not v], ["Ratios 1 : 1 : √2."])
def mk_gm_sel():
    a, b = R.choice([(4, 9), (1, 9), (2, 8), (9, 16), (3, 12), (1, 4)])
    st = {f"The altitude is {rad(a * b)}": True, f"The hypotenuse is {a + b}": True, f"The longer leg is {rad(b * (a + b))}": True, f"The altitude is {fr(F(a + b, 2))}": F(a + b, 2) ** 2 == a * b, f"The shorter leg is {rad(a * b)}": False}
    B.sel(5, lv(), f"The altitude to the hypotenuse of a right triangle splits it into {a} and {b}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Geometric mean relationships."])
def mk_word_sel():
    t = R.randint(20, 70); L_ = R.randint(10, 60)
    st = {f"The height is {L_} sin {t}°": True, f"The horizontal distance is {L_} cos {t}°": True, f"The height is {L_} cos {90 - t}°": True, f"The height is {L_} tan {t}°": False, f"The horizontal distance is {L_} sin {t}°": False}
    B.sel(10, lv(), f"A {L_}-m zip line makes a {t}° angle with the horizontal. Select ALL correct expressions.", [a for a, v in st.items() if v], [a for a, v in st.items() if not v], ["The zip line is the hypotenuse.", "sin θ = cos(90° - θ)."], tags=["modeling"])
makers = {1: [mk_pyth, mk_pyth, mk_pyth_app, mk_pyth_orq, mk_pyth_sel], 2: [mk_conv, mk_conv_sel, mk_conv_x], 3: [mk_45, mk_45, mk_45_app, mk_45_sel], 4: [mk_30, mk_30_app, mk_sp_sel], 5: [mk_gm, mk_gm, mk_gm_orq, mk_gm_sel], 6: [mk_ratio, mk_cofunc, mk_ratio_sel], 7: [mk_side, mk_side, mk_side, mk_side_fig], 8: [mk_angle, mk_angle, mk_angle_both], 9: [mk_elev, mk_elev, mk_elev, mk_elev, mk_elev, mk_elev_two, mk_elev_sel], 10: [mk_word, mk_word, mk_word, mk_word, mk_word_sel]}
for S_, ms in makers.items():
    fill(B, S_, 32, ms, R)

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
