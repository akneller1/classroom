from lib import Bank, graph
from mathlite import *
from geofig import Fig
from fill import fill
import math, random

STD = {1: ["G-CO.C.11"], 2: ["G-CO.C.11"], 3: ["G-CO.C.11", "G-SRT.B.5"], 4: ["G-CO.C.11"], 5: ["G-CO.C.11"], 6: ["G-CO.C.11", "G-SRT.B.5"], 7: ["G-SRT.B.5"], 8: ["G-CO.C.11"], 9: ["G-GPE.B.4", "G-GPE.B.5", "G-GPE.B.7"]}
B = Bank("quadrilaterals-polygons", "qp", STD, course="geometry", prefix="geo")
R = random.Random(707)
def lv(): return R.choice(["cp2", "cp1", "cp1", "honors"])
NAMES = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon", 15: "15-gon", 18: "18-gon", 20: "20-gon"}


def quad_fig(name, P_, labels, marks=None, diag=False, alt=""):
    fg = Fig(4.2, 3.0); fg.poly(P_); fg.names(P_, list(labels))
    if diag: fg.seg(P_[0], P_[2], lw=1.0); fg.seg(P_[1], P_[3], lw=1.0)
    for m in (marks or []):
        kind, i, j, n = m
        if kind == "t": fg.ticks(P_[i], P_[j], n, size=0.28)
        if kind == "a": fg.arrows(P_[i], P_[j], n)
        if kind == "r": fg.angle(P_[i], P_[(i - 1) % 4], P_[(i + 1) % 4], right=True, r=0.45)
    return fg.save(B, name, alt)

# ---- Skill 1: polygon angles ----
def mk_int():
    n = R.choice([5, 6, 7, 8, 9, 10, 12, 15, 18, 20]); kind = R.choice(["sum", "each", "ext", "n_from_each", "n_from_ext"])
    if kind == "sum": B.mc(1, lv(), f"Find the sum of the interior angles of a {NAMES[n]}.", f"{180 * (n - 2)}°", [f"{180 * n}°", f"{180 * (n - 1)}°", "360°"], ["(n - 2)·180°."], tags=["misconception"])
    elif kind == "each": B.sa(1, lv(), f"Find the measure of each interior angle of a regular {NAMES[n]}.", f"{fr(F(180 * (n - 2), n))}°", ["(n - 2)·180°/n."])
    elif kind == "ext": B.sa(1, lv(), f"Find each exterior angle of a regular {NAMES[n]}.", f"{fr(F(360, n))}°", ["360°/n."])
    elif kind == "n_from_each": B.sa(1, lv(), f"Each interior angle of a regular polygon measures {fr(F(180 * (n - 2), n))}°. How many sides does it have?", str(n), [f"Exterior angle = 180 - {fr(F(180 * (n - 2), n))} = {fr(F(360, n))}°.", f"n = 360/{fr(F(360, n))}."])
    else: B.mc(1, lv(), f"Each exterior angle of a regular polygon is {fr(F(360, n))}°. How many sides?", str(n), [str(n + 1), str(n - 1), str(2 * n)], ["n = 360/exterior."])
def mk_int_alg():
    n = R.choice([4, 5, 6]); tot = 180 * (n - 2); x = R.randint(10, 40)
    cs = [R.randint(1, 4) for _ in range(n)]; base = [R.randint(10, 60) for _ in range(n - 1)]
    rest = tot - sum(c * x for c in cs) - sum(base)
    if rest <= 0: raise AssertionError
    base.append(rest); angs = [c * x + b for c, b in zip(cs, base)]
    if max(angs) >= 180: raise AssertionError
    exprs = ", ".join(f"({c}x + {b})°".replace("(1x", "(x") for c, b in zip(cs, base))
    B.sa(1, lv(), f"The angles of a {NAMES[n]} measure {exprs}. Find x.", f"x = {x}", [f"Sum = {tot}°.", f"{sum(cs)}x + {sum(base)} = {tot}."])
def mk_int_sel():
    n = R.choice([5, 6, 8, 10, 12])
    st = {f"Interior angle sum {180 * (n - 2)}°": True, f"Each exterior angle {fr(F(360, n))}°": True, "Exterior angle sum 360°": True, f"Interior angle sum {180 * n}°": False, f"Each interior angle {fr(F(360, n))}°": n == 4}
    B.sel(1, lv(), f"For a regular {NAMES[n]}, select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["(n - 2)·180°; exterior sum 360°."])
B.orq(1, "honors", "Explore whether a regular polygon can have interior angles of 150°, 155°, or 160°.", [("150°: number of sides?", "12"), ("155°: number of sides?", "not possible (360/25 = 14.4)"), ("160°: number of sides?", "18"), ("State a test.", "180 - angle must divide 360")], ["Exterior 30°.", "Exterior 25°.", "Exterior 20°.", "n = 360/exterior must be a whole number ≥ 3."], tags=["reasoning", "challenge"])

# ---- Skill 2: parallelograms ----
P_par = [(0, 0), (5, 0), (6.5, 3), (1.5, 3)]
dgp = quad_fig("s02-par", P_par, "ABCD", marks=[("a", 0, 1, 1), ("a", 3, 2, 1), ("a", 0, 3, 2), ("a", 1, 2, 2)], diag=True, alt="Parallelogram ABCD (AB ∥ DC and AD ∥ BC marked with arrows) with diagonals AC and BD.")
def mk_par():
    kind = R.choice(["side", "angle", "consec", "diag"])
    x = R.randint(3, 15); c1, c2 = R.sample(range(2, 8), 2)
    if kind == "side":
        k1 = R.randint(1, 15); v = c1 * x + k1; k2 = v - c2 * x
        B.sa(2, lv(), f"In parallelogram ABCD, AB = {c1}x + {k1} and CD = {c2}x {'+' if k2 >= 0 else '-'} {abs(k2)}. Find AB.", str(v), ["Opposite sides are congruent.", f"x = {x}."], diagram=dgp, tags=["graph"])
    elif kind == "angle":
        a = R.randint(40, 140); B.mc(2, lv(), f"In parallelogram ABCD, m∠A = {a}°. Find m∠B, m∠C, m∠D.", f"{180 - a}°, {a}°, {180 - a}°", [f"{a}°, {180 - a}°, {a}°", f"{180 - a}°, {180 - a}°, {a}°", f"{90 - a % 90}°, {a}°, {90 - a % 90}°"], ["Consecutive angles supplementary; opposite congruent."], diagram=dgp, tags=["graph"])
    elif kind == "consec":
        k1 = R.randint(5, 30); v = c1 * x + k1; k2 = 180 - v - c2 * x
        if not (0 < v < 180): raise AssertionError
        B.sa(2, lv(), f"In parallelogram ABCD, m∠A = ({c1}x + {k1})° and m∠B = ({c2}x {'+' if k2 >= 0 else '-'} {abs(k2)})°. Find m∠A.", f"{v}°", ["Consecutive angles are supplementary.", f"x = {x}."], diagram=dgp, tags=["graph"])
    else:
        k1 = R.randint(1, 10); v = c1 * x + k1; k2 = v - c2 * x
        B.sa(2, lv(), f"The diagonals of parallelogram ABCD meet at E. AE = {c1}x + {k1} and CE = {c2}x{(' + ' if k2 > 0 else ' - ') + str(abs(k2)) if k2 else ''}. Find AC.", str(2 * v), ["Diagonals bisect each other.", f"x = {x}; AC = 2·AE."], diagram=dgp, tags=["graph"])
def mk_par_sel():
    st = {"Opposite sides are congruent": True, "Opposite angles are congruent": True, "Diagonals bisect each other": True, "Consecutive angles are supplementary": True, "Diagonals are congruent": False, "Diagonals are perpendicular": False, "All sides are congruent": False}
    keys = R.sample(list(st), 6)
    if sum(st[k] for k in keys) < 2 or all(st[k] for k in keys): raise AssertionError
    B.sel(2, lv(), "Select ALL properties of every parallelogram." + R.choice(["", " (in general)"]), [k for k in keys if st[k]], [k for k in keys if not st[k]], ["Rectangles add congruent diagonals; rhombi add perpendicular diagonals."], tags=["misconception"])
B.orq(2, "honors", "Prove that opposite sides of parallelogram ABCD are congruent.", [("Draw a diagonal; name the triangles.", "AC: △ABC and △CDA"), ("Find congruent angles.", "∠BAC ≅ ∠DCA and ∠BCA ≅ ∠DAC (alternate interior)"), ("Prove the triangles congruent.", "ASA (AC shared)"), ("Conclude.", "AB ≅ CD and BC ≅ DA by CPCTC")], ["Diagonal.", "Parallel sides.", "ASA.", "CPCTC."], tags=["reasoning"])

# ---- Skill 3: proving parallelograms ----
def mk_prove():
    tests = [("both pairs of opposite sides are congruent", True), ("both pairs of opposite angles are congruent", True), ("the diagonals bisect each other", True), ("one pair of opposite sides is both congruent and parallel", True),
             ("one pair of opposite sides is parallel and the other pair is congruent", False), ("the diagonals are congruent", False), ("two pairs of consecutive sides are congruent", False), ("one pair of opposite sides is congruent", False), ("both pairs of opposite sides are parallel", True)]
    t, ok = R.choice(tests)
    B.mc(3, lv(), f"A quadrilateral has {t}. Must it be a parallelogram?", "Yes" if ok else "No", ["No" if ok else "Yes", "Only if it has a right angle", "Only if its diagonals are perpendicular"], ["Parallelogram tests: both pairs of opposite sides ∥ or ≅, both pairs of opposite angles ≅, diagonals bisect each other, or one pair ∥ and ≅." if ok else "Counterexample: an isosceles trapezoid or a kite."], tags=["reasoning"])
def mk_prove_x():
    x = R.randint(2, 12); c1, c2 = R.sample(range(2, 9), 2); k1 = R.randint(1, 15); v = c1 * x + k1; k2 = v - c2 * x
    which = R.choice(["opposite sides AB and CD", "the halves AE and EC of diagonal AC (E is the intersection)"])
    B.sa(3, lv(), f"For what x is ABCD a parallelogram if {which} measure {c1}x + {k1} and {c2}x {'+' if k2 >= 0 else '-'} {abs(k2)} (and the other pair matches likewise)?", f"x = {x}", ["Set the parts equal (opposite sides congruent or diagonals bisect each other).", f"x = {x}."])
def mk_prove_coord():
    a = (R.randint(-5, 2), R.randint(-5, 2)); u = (R.randint(2, 6), R.randint(-2, 2)); v = (R.randint(-2, 2), R.randint(2, 6)); ok = R.random() < 0.6
    A_ = a; B_ = (a[0] + u[0], a[1] + u[1]); D_ = (a[0] + v[0], a[1] + v[1]); C_ = (B_[0] + v[0] + (0 if ok else 1), B_[1] + v[1])
    mid1 = (F(A_[0] + C_[0], 2), F(A_[1] + C_[1], 2)); mid2 = (F(B_[0] + D_[0], 2), F(B_[1] + D_[1], 2))
    B.orq(3, lv(), f"A{pt(*A_)}, B{pt(*B_)}, C{pt(*C_)}, D{pt(*D_)}.", [("Find the midpoint of AC.", pt(*mid1)), ("Find the midpoint of BD.", pt(*mid2)), ("Do the diagonals bisect each other?", "Yes" if mid1 == mid2 else "No"), ("Is ABCD a parallelogram?", "Yes" if mid1 == mid2 else "No")], ["Midpoint formula.", "Midpoint formula.", "Compare.", "Diagonals bisect each other ⇔ parallelogram."], tags=["connections"])
B.sel(3, "honors", "Select ALL sets of information that prove ABCD is a parallelogram.", ["AB ∥ CD and AB ≅ CD", "AB ≅ CD and BC ≅ DA", "∠A ≅ ∠C and ∠B ≅ ∠D"], ["AB ∥ CD and BC ≅ DA", "AC ≅ BD", "AB ≅ BC and CD ≅ DA"], ["Isosceles trapezoids and kites are counterexamples to the others."], tags=["reasoning"])

# ---- Skill 4: rectangles ----
def mk_rect():
    kind = R.choice(["diag", "angle", "sides", "pyth"]); x = R.randint(2, 12); c1, c2 = R.sample(range(2, 9), 2)
    if kind == "diag":
        k1 = R.randint(1, 20); v = c1 * x + k1; k2 = v - c2 * x
        B.sa(4, lv(), f"In rectangle ABCD, AC = {c1}x + {k1} and BD = {c2}x {'+' if k2 >= 0 else '-'} {abs(k2)}. Find the length of each diagonal.", str(v), ["Diagonals of a rectangle are congruent.", f"x = {x}."])
    elif kind == "angle":
        a = R.randint(15, 75); B.mc(4, lv(), f"In rectangle ABCD, diagonal AC makes a {a}° angle with side AB. Find m∠CAD.", f"{90 - a}°", [f"{a}°", f"{180 - a}°", f"{2 * a}°"], ["∠BAD = 90°, so ∠CAD = 90° - ∠BAC."])
    elif kind == "sides":
        k1 = R.randint(5, 40); v = c1 * x + k1
        if v >= 90: raise AssertionError
        B.sa(4, lv(), f"In rectangle PQRS, diagonals meet at T. m∠PTQ = ({c1}x + {k1})°. If x = {x}, find m∠TPQ.", f"{fr(F(180 - v, 2))}°", ["Diagonals are congruent and bisect each other, so △PTQ is isosceles.", f"m∠PTQ = {v}°; base angles (180 - {v})/2."])
    else:
        a, b = R.choice([(6, 8), (5, 12), (9, 12), (8, 15), (7, 24)])
        B.sa(4, lv(), f"A rectangle is {a} by {b}. Find the length of a diagonal.", str(int(math.hypot(a, b))), ["Pythagorean theorem."])
def mk_rect_sel():
    st = {"All angles are right angles": True, "Diagonals are congruent": True, "Diagonals bisect each other": True, "Opposite sides are parallel": True, "Diagonals are perpendicular": False, "All sides are congruent": False}
    keys = R.sample(list(st), 5)
    if sum(st[k] for k in keys) < 2 or all(st[k] for k in keys): raise AssertionError
    B.sel(4, lv(), "Select ALL properties of every rectangle.", [k for k in keys if st[k]], [k for k in keys if not st[k]], ["A rectangle is a parallelogram with four right angles."])
B.mc(4, "cp1", "A parallelogram has congruent diagonals. What must it be?", "a rectangle", ["a rhombus", "a square", "a kite"], ["Theorem: a parallelogram with congruent diagonals is a rectangle."])

# ---- Skill 5: rhombi and squares ----
def mk_rhom():
    kind = R.choice(["perp", "bisect", "side", "angle"]); x = R.randint(3, 15)
    if kind == "perp":
        k1 = 90 - 5 * x if 90 - 5 * x > 0 else None
        if k1 is None: raise AssertionError
        B.sa(5, lv(), f"In rhombus ABCD, diagonals meet at E and m∠AEB = (5x + {k1})°. Find x.", f"x = {x}", ["Diagonals of a rhombus are perpendicular: 90°."])
    elif kind == "bisect":
        a = R.randint(20, 80); B.mc(5, lv(), f"In rhombus ABCD, m∠BAC = {a}°. Find m∠BAD and m∠ABC.", f"{2 * a}° and {180 - 2 * a}°", [f"{a}° and {180 - a}°", f"{2 * a}° and {2 * a}°", f"{90 - a}° and {90 + a}°"], ["Each diagonal bisects a pair of opposite angles.", "Consecutive angles are supplementary."])
    elif kind == "side":
        d1, d2 = R.choice([(6, 8), (10, 24), (16, 30), (12, 16), (14, 48)])
        B.sa(5, lv(), f"A rhombus has diagonals {d1} and {d2}. Find the side length and the area.", f"side {int(math.hypot(d1 / 2, d2 / 2))}; area {d1 * d2 // 2}", ["Half-diagonals are legs of a right triangle.", "Area = ½d₁d₂."])
    else:
        s = R.randint(3, 15); B.mc(5, lv(), f"A square has side {s}. Find the diagonal.", f"{s}√2", [f"{2 * s}", f"{s}√3", str(s * s)], ["45°-45°-90° triangle."])
def mk_rhom_sel():
    shape = R.choice(["rhombus", "square"])
    st = {"All sides are congruent": True, "Diagonals are perpendicular": True, "Diagonals bisect the angles": True, "Diagonals are congruent": shape == "square", "All angles are right angles": shape == "square", "Exactly one pair of parallel sides": False}
    B.sel(5, lv(), f"Select ALL properties of every {shape}.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["A square is both a rectangle and a rhombus."])
B.orq(5, "honors", "Rhombus ABCD has A(0, 0), B(5, 0), D(3, 4).", [("Find C.", "(8, 4)"), ("Verify all sides are 5.", "AB = BC = CD = DA = 5"), ("Find the slopes of the diagonals.", "AC: 1/2; BD: -2"), ("What do the slopes show?", "the diagonals are perpendicular")], ["C = B + D - A.", "Distance formula.", "Δy/Δx.", "Product -1."], tags=["connections"])

# ---- Skill 6: trapezoids ----
def mk_trap():
    kind = R.choice(["mid", "mid_alg", "iso_angle", "iso_diag", "base"])
    b1, b2 = R.randint(4, 30), R.randint(4, 30)
    if kind == "mid": B.mc(6, lv(), f"A trapezoid has bases {b1} and {b2}. Find its midsegment.", fr(F(b1 + b2, 2)), [str(b1 + b2), fr(F(abs(b1 - b2), 2)), fr(F(b1 * b2, b1 + b2))], ["Midsegment = average of the bases."], tags=["misconception"])
    elif kind == "base":
        m = F(b1 + b2, 2); B.sa(6, lv(), f"A trapezoid has midsegment {fr(m)} and one base {b1}. Find the other base.", str(b2), ["2·midsegment - base."])
    elif kind == "mid_alg":
        x = R.randint(2, 10); c1, c2 = R.randint(1, 4), R.randint(1, 4); k1, k2 = R.randint(1, 10), R.randint(1, 10); m = F(c1 * x + k1 + c2 * x + k2, 2)
        if (c1 + c2) % 2 or (k1 + k2) % 2: raise AssertionError
        mx = f"{(c1 + c2) // 2}x + {(k1 + k2) // 2}".replace("1x", "x") if (c1 + c2) // 2 == 1 else f"{(c1 + c2) // 2}x + {(k1 + k2) // 2}"
        B.sa(6, lv(), f"A trapezoid has bases {c1}x + {k1} and {c2}x + {k2}; its midsegment is {fr(m)}. Find x and the bases.", f"x = {x}; bases {c1 * x + k1} and {c2 * x + k2}", ["Midsegment = average of bases.", f"({c1 + c2}x + {k1 + k2})/2 = {fr(m)} → x = {x}."])
    elif kind == "iso_angle":
        a = R.randint(40, 85); B.sa(6, lv(), f"In isosceles trapezoid ABCD with bases AB and CD, m∠A = {a}°. Find m∠B, m∠C, m∠D.", f"{a}°, {180 - a}°, {180 - a}°", ["Base angles congruent; same-side interior angles supplementary."])
    else:
        x = R.randint(2, 12); c1, c2 = R.sample(range(2, 8), 2); k1 = R.randint(1, 20); v = c1 * x + k1; k2 = v - c2 * x
        B.sa(6, lv(), f"Isosceles trapezoid PQRS has diagonals PR = {c1}x + {k1} and QS = {c2}x {'+' if k2 >= 0 else '-'} {abs(k2)}. Find x.", f"x = {x}", ["Diagonals of an isosceles trapezoid are congruent."])
def mk_trap_sel():
    st = {"exactly one pair of parallel sides": True, "congruent legs (if isosceles)": True, "congruent diagonals (if isosceles)": True, "diagonals that bisect each other": False, "two pairs of parallel sides": False}
    B.sel(6, lv(), "Select ALL properties of a trapezoid (as defined with exactly one pair of parallel sides).", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Bisecting diagonals would make it a parallelogram."])
P_t = [(0, 0), (7, 0), (5, 3), (2, 3)]
dg = quad_fig("s06-trap", P_t, "ABCD", marks=[("a", 0, 1, 1), ("a", 3, 2, 1), ("t", 1, 2, 1), ("t", 3, 0, 1)], alt="Isosceles trapezoid ABCD with bases AB and DC (arrows) and congruent legs BC and AD (tick marks).")
B.orq(6, "cp1", "In the isosceles trapezoid, AB = 21, DC = 9, and m∠A = 60°.", [("Find the midsegment.", "15"), ("Find m∠B.", "60°"), ("Find m∠D.", "120°"), ("Find the leg length.", "12")], ["(21 + 9)/2.", "Base angles congruent.", "Supplementary to ∠A.", "Drop heights: horizontal run 6 with 60° → leg 12."], diagram=dg, tags=["graph"])

# ---- Skill 7: kites ----
def mk_kite():
    kind = R.choice(["angle", "side", "diag", "angle_alg"])
    if kind == "angle":
        a, b = R.randint(50, 150), R.randint(40, 120); c = 360 - a - 2 * b
        if not 0 < c < 180: raise AssertionError
        B.sa(7, lv(), f"Kite ABCD has ∠B ≅ ∠D (the angles between noncongruent sides). m∠A = {a}° and m∠B = {b}°. Find m∠C.", f"{c}°", ["One pair of opposite angles is congruent.", f"360 - {a} - 2·{b}."])
    elif kind == "side":
        d1a, d1b = R.choice([(3, 4), (5, 12), (6, 8), (8, 15)]); d2 = R.choice([(4, 3), (12, 5), (15, 8), (9, 12)])
        s1 = math.hypot(d1a, d2[0]); s2 = math.hypot(d1a, d2[1])
        B.sa(7, lv(), f"The diagonals of a kite are perpendicular. One diagonal is split into two {d1a}-unit halves; the other into {d2[0]} and {d2[1]}. Find the side lengths (nearest tenth if needed).", f"{s1:g} and {s2:g}" if s1 == int(s1) and s2 == int(s2) else f"{s1:.1f} and {s2:.1f}", ["Each side is a hypotenuse of a right triangle formed by half-diagonals."])
    elif kind == "diag":
        d1, d2 = R.randint(4, 20), R.randint(4, 20); B.mc(7, lv(), f"A kite has diagonals {d1} and {d2}. Find its area.", fr(F(d1 * d2, 2)), [str(d1 * d2), str(d1 + d2), fr(F(d1 * d2, 4))], ["Area = ½d₁d₂."])
    else:
        x = R.randint(5, 25); a = 2 * x + 10; b = 360 - 2 * (3 * x) - a
        if not 0 < b < 180 or 3 * x >= 180: raise AssertionError
        B.sa(7, lv(), f"In a kite, the congruent opposite angles each measure (3x)°, and the other two measure (2x + 10)° and {b}°. Find x.", f"x = {x}", [f"2(3x) + 2x + 10 + {b} = 360."])
def mk_kite_sel():
    st = {"Diagonals are perpendicular": True, "Two pairs of consecutive sides are congruent": True, "One diagonal bisects the other": True, "Exactly one pair of opposite angles is congruent": True, "Opposite sides are parallel": False, "Diagonals are congruent": False}
    keys = R.sample(list(st), 5)
    if sum(st[k] for k in keys) < 2 or all(st[k] for k in keys): raise AssertionError
    B.sel(7, lv(), "Select ALL properties of every kite (that is not a rhombus).", [k for k in keys if st[k]], [k for k in keys if not st[k]], ["Kite properties."])

# ---- Skill 8: classifying ----
def mk_class():
    descs = [("four right angles and four congruent sides", "square"), ("four right angles but adjacent sides not congruent", "rectangle"), ("four congruent sides and no right angles", "rhombus"), ("exactly one pair of parallel sides", "trapezoid"),
             ("two pairs of congruent consecutive sides, opposite sides not congruent", "kite"), ("both pairs of opposite sides parallel, no right angles, adjacent sides not congruent", "parallelogram")]
    d, a = R.choice(descs)
    B.mc(8, lv(), f"Give the most specific name for a quadrilateral with {d}.", a, [x for x in ["square", "rectangle", "rhombus", "parallelogram", "trapezoid", "kite"] if x != a][:3], ["Use the quadrilateral hierarchy."])
def mk_class_tf():
    stmts = [("Every square is a rhombus.", True), ("Every rhombus is a square.", False), ("Every rectangle is a parallelogram.", True), ("Every parallelogram is a rectangle.", False), ("Some rhombi are rectangles.", True), ("No trapezoid is a parallelogram (one-pair definition).", True), ("Every kite is a rhombus.", False), ("Every square is a kite.", True)]
    st, v = R.choice(stmts)
    B.mc(8, lv(), f"True or false: {st}", "True" if v else "False", ["False" if v else "True", "Sometimes", "Cannot be determined"], ["Use the definitions and the hierarchy."], tags=["reasoning"])
def mk_class_sel():
    q = R.choice([("Select ALL quadrilaterals whose diagonals are always perpendicular.", ["rhombus", "square", "kite"], ["rectangle", "isosceles trapezoid", "parallelogram"]), ("Select ALL quadrilaterals whose diagonals are always congruent.", ["rectangle", "square", "isosceles trapezoid"], ["rhombus", "kite", "parallelogram"]),
                  ("Select ALL quadrilaterals that are always parallelograms.", ["rectangle", "rhombus", "square"], ["kite", "trapezoid", "isosceles trapezoid"])])
    B.sel(8, lv(), q[0], q[1], q[2], ["Use the hierarchy and diagonal properties."])

# ---- Skill 9: coordinate plane ----
def mk_coord():
    shape = R.choice(["parallelogram", "rectangle", "rhombus", "square"])
    a = (R.randint(-4, 2), R.randint(-4, 2))
    u, v = R.choice({"rectangle": [((3, 0), (0, 2)), ((2, 1), (-2, 4)), ((4, 2), (-1, 2))], "square": [((2, 1), (-1, 2)), ((3, 0), (0, 3)), ((1, 3), (-3, 1))],
                     "rhombus": [((3, 4), (5, 0)), ((4, 3), (0, 5)), ((1, 2), (2, 1))], "parallelogram": [((4, 1), (1, 3)), ((5, 0), (2, 3)), ((3, 2), (1, 4))]}[shape])
    if u[0] * v[1] - u[1] * v[0] == 0: raise AssertionError
    A_ = a; B_ = (a[0] + u[0], a[1] + u[1]); D_ = (a[0] + v[0], a[1] + v[1]); C_ = (B_[0] + v[0], B_[1] + v[1])
    dot = u[0] * v[0] + u[1] * v[1]; eqs = u[0] ** 2 + u[1] ** 2 == v[0] ** 2 + v[1] ** 2
    kind = "square" if dot == 0 and eqs else "rectangle" if dot == 0 else "rhombus" if eqs else "parallelogram"
    B.orq(9, lv(), f"Classify ABCD with A{pt(*A_)}, B{pt(*B_)}, C{pt(*C_)}, D{pt(*D_)}.", [("Find AB and AD.", f"{rad(u[0] ** 2 + u[1] ** 2)} and {rad(v[0] ** 2 + v[1] ** 2)}"), ("Find the slopes of AB and AD.", f"{fr(F(u[1], u[0])) if u[0] else 'undefined'} and {fr(F(v[1], v[0])) if v[0] else 'undefined'}"), ("Are AB and AD perpendicular?", "Yes" if dot == 0 else "No"), ("Give the most specific name.", kind)],
          ["Distance formula.", "Δy/Δx.", "Product of slopes -1 (or horizontal/vertical).", "Parallelogram by construction; add right angles and/or equal sides."], tags=["connections"])
def mk_fourth():
    A_ = (R.randint(-5, 3), R.randint(-5, 3)); B_ = (A_[0] + R.randint(2, 6), A_[1] + R.randint(-2, 2)); C_ = (B_[0] + R.randint(-2, 2), B_[1] + R.randint(2, 6))
    D_ = (A_[0] + C_[0] - B_[0], A_[1] + C_[1] - B_[1])
    B.mc(9, lv(), f"Three vertices of parallelogram ABCD are A{pt(*A_)}, B{pt(*B_)}, C{pt(*C_)}. Find D.", pt(*D_), [pt(B_[0] + C_[0] - A_[0], B_[1] + C_[1] - A_[1]), pt(A_[0] + B_[0] - C_[0], A_[1] + B_[1] - C_[1]), pt(C_[0] - A_[0], C_[1] - A_[1])], ["D = A + C - B (diagonals share a midpoint)."])
def mk_area_coord():
    w, h = R.randint(2, 8), R.randint(2, 8); x0, y0 = R.randint(-5, 2), R.randint(-5, 2)
    B.sa(9, lv(), f"Find the perimeter and area of the rectangle with vertices {pt(x0, y0)}, {pt(x0 + w, y0)}, {pt(x0 + w, y0 + h)}, {pt(x0, y0 + h)}.", f"perimeter {2 * (w + h)}; area {w * h}", ["Side lengths from coordinates."])

makers = {1: [mk_int, mk_int, mk_int_alg, mk_int_sel], 2: [mk_par, mk_par, mk_par_sel], 3: [mk_prove, mk_prove_x, mk_prove_coord], 4: [mk_rect, mk_rect, mk_rect_sel], 5: [mk_rhom, mk_rhom, mk_rhom_sel], 6: [mk_trap, mk_trap, mk_trap_sel], 7: [mk_kite, mk_kite, mk_kite_sel], 8: [mk_class, mk_class_tf, mk_class_sel], 9: [mk_coord, mk_fourth, mk_area_coord]}
for S_, ms in makers.items():
    fill(B, S_, 32, ms, R)

# ---- property tables (letters vary) for select-all variety ----
QL = ["ABCD", "PQRS", "WXYZ", "JKLM", "EFGH", "MNOP", "RSTU"]
def stmts(L):
    a, b, c, d = L
    return {"opp_par1": f"{a}{b} ∥ {d}{c}", "opp_par2": f"{a}{d} ∥ {b}{c}", "opp_cong": f"{a}{b} ≅ {c}{d}", "cons_cong": f"{a}{b} ≅ {b}{c}", "opp_ang": f"∠{a} ≅ ∠{c}", "right": f"∠{a} is a right angle",
            "diag_cong": f"{a}{c} ≅ {b}{d}", "diag_perp": f"{a}{c} ⊥ {b}{d}", "diag_bis": f"{a}{c} and {b}{d} bisect each other", "diag_bisang": f"{a}{c} bisects ∠{a}", "legs_cong": f"{b}{c} ≅ {d}{a}"}
TRUTH = {"parallelogram": {"opp_par1", "opp_par2", "opp_cong", "opp_ang", "diag_bis", "legs_cong"}, "rectangle": {"opp_par1", "opp_par2", "opp_cong", "opp_ang", "diag_bis", "right", "diag_cong", "legs_cong"},
         "rhombus": {"opp_par1", "opp_par2", "opp_cong", "opp_ang", "diag_bis", "cons_cong", "diag_perp", "diag_bisang", "legs_cong"}, "square": {"opp_par1", "opp_par2", "opp_cong", "opp_ang", "diag_bis", "cons_cong", "diag_perp", "diag_bisang", "right", "diag_cong", "legs_cong"},
         "isosceles trapezoid (bases AB-type and DC-type)": {"opp_par1", "diag_cong", "legs_cong"}, "kite (vertex at the first letter, congruent sides meeting there)": {"diag_perp", "diag_bisang"}}
SK = {"parallelogram": 2, "rectangle": 4, "rhombus": 5, "square": 5, "isosceles trapezoid (bases AB-type and DC-type)": 6, "kite (vertex at the first letter, congruent sides meeting there)": 7}
def mk_prop_sel(shape):
    def f():
        L = R.choice(QL); st = stmts(L); keys = R.sample(list(st), 6); tr = TRUTH[shape]
        right = [st[k] for k in keys if k in tr]; wrong = [st[k] for k in keys if k not in tr]
        if len(right) < 2 or not wrong: raise AssertionError
        nm = shape.split(" (")[0]
        extra = f" with bases {L[0]}{L[1]} and {L[3]}{L[2]}" if "trapezoid" in shape else (f" with {L[0]}{L[1]} ≅ {L[0]}{L[3]} and {L[2]}{L[1]} ≅ {L[2]}{L[3]}" if "kite" in shape else "")
        B.sel(SK[shape], lv(), f"{L} is a{'n' if nm[0] in 'aeiou' else ''} {nm}{extra}. Select ALL statements that must be true.", right, wrong, [f"Use the properties of a {nm}."])
    return f
def mk_classify_props():
    combos = [("a parallelogram with congruent diagonals", "rectangle"), ("a parallelogram with perpendicular diagonals", "rhombus"), ("a parallelogram with congruent, perpendicular diagonals", "square"), ("a parallelogram with one right angle", "rectangle"),
              ("a parallelogram with two consecutive sides congruent", "rhombus"), ("a quadrilateral whose diagonals bisect each other", "parallelogram"), ("a quadrilateral whose diagonals are perpendicular bisectors of each other", "rhombus"),
              ("a quadrilateral with four congruent sides and one right angle", "square"), ("a rectangle with perpendicular diagonals", "square"), ("a rhombus with congruent diagonals", "square"), ("a quadrilateral with exactly one pair of parallel sides and congruent diagonals", "isosceles trapezoid"),
              ("a quadrilateral with two pairs of consecutive congruent sides and no parallel sides", "kite"), ("a quadrilateral with both pairs of opposite angles congruent", "parallelogram")]
    d, a = R.choice(combos)
    B.mc(8, lv(), f"What is the most specific name for {d}?", a, [x for x in ["square", "rectangle", "rhombus", "parallelogram", "isosceles trapezoid", "kite"] if x != a][:3], ["Apply the converse theorems and the hierarchy."], tags=["reasoning"])
def mk_which_shapes():
    props = [("diagonals that bisect each other", {"parallelogram", "rectangle", "rhombus", "square"}), ("four right angles", {"rectangle", "square"}), ("four congruent sides", {"rhombus", "square"}), ("perpendicular diagonals", {"rhombus", "square", "kite"}),
             ("congruent diagonals", {"rectangle", "square", "isosceles trapezoid"}), ("at least one pair of parallel sides", {"parallelogram", "rectangle", "rhombus", "square", "trapezoid", "isosceles trapezoid"})]
    pr, yes = R.choice(props); shapes = ["parallelogram", "rectangle", "rhombus", "square", "kite", "trapezoid", "isosceles trapezoid"]; pick = R.sample(shapes, 6)
    right = [x for x in pick if x in yes]; wrong = [x for x in pick if x not in yes]
    if len(right) < 2 or not wrong: raise AssertionError
    B.sel(8, lv(), f"Select ALL quadrilaterals that always have {pr}.", right, wrong, ["Use the quadrilateral hierarchy."])
def mk_class_coord():
    u, v = R.choice([((3, 0), (0, 2)), ((2, 1), (-1, 2)), ((3, 4), (5, 0)), ((4, 1), (1, 3)), ((1, 3), (-3, 1)), ((2, 2), (-3, 3))])
    a = (R.randint(-3, 3), R.randint(-3, 3)); P4 = [a, (a[0] + u[0], a[1] + u[1]), (a[0] + u[0] + v[0], a[1] + u[1] + v[1]), (a[0] + v[0], a[1] + v[1])]
    dot = u[0] * v[0] + u[1] * v[1]; eqs = u[0] ** 2 + u[1] ** 2 == v[0] ** 2 + v[1] ** 2
    kind = "square" if dot == 0 and eqs else "rectangle" if dot == 0 else "rhombus" if eqs else "parallelogram"
    B.mc(8, lv(), f"Classify the quadrilateral with vertices {', '.join(pt(*p) for p in P4)} as specifically as possible.", kind, [x for x in ["square", "rectangle", "rhombus", "parallelogram", "kite"] if x != kind][:3], ["Check side lengths and slopes."])
for shape in TRUTH:
    fill(B, SK[shape], 34 if SK[shape] != 5 else 36, [mk_prop_sel(shape)], R, max_tries=60)
fill(B, 8, 32, [mk_classify_props, mk_which_shapes, mk_class_coord], R)
fill(B, 3, 34, [mk_prove], R, max_tries=30)

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
