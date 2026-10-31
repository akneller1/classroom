from lib import Bank, graph
from mathlite import *
from fill import fill
from geofig import Fig, tri_from_sides
import math, random

STD = {1: ["G-C.A.2", "G-CO.A.1"], 2: ["G-C.A.2"], 3: ["G-C.A.2", "G-C.A.3"], 4: ["G-C.A.2"], 5: ["G-C.A.2", "G-C.A.4"], 6: ["G-C.A.2"], 7: ["G-C.B.5"], 8: ["G-C.A.2"], 9: ["G-GPE.A.1", "G-GPE.B.4"]}
B = Bank("circles", "ci", STD, course="geometry", prefix="geo")
R = random.Random(909)
def lv(): return R.choice(["cp2", "cp1", "cp1", "honors"])
NF = [0]
def nm(s): NF[0] += 1; return f"{s}-{NF[0]}"
def cp(deg, r=3.0, c=(0.0, 0.0)): return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))
def pit(v):
    v = F(v)
    if v == 1: return "π"
    if v.denominator == 1: return f"{v.numerator}π"
    return f"{'' if v.numerator == 1 else v.numerator}π/{v.denominator}"
def dg(v): return f"{fr(v)}°"
def ang_at(P_, X, Y):
    a = math.atan2(X[1] - P_[1], X[0] - P_[0]); b = math.atan2(Y[1] - P_[1], Y[0] - P_[0]); d = abs(a - b) % (2 * math.pi)
    return math.degrees(min(d, 2 * math.pi - d))
def inter(P1, P2, Q1, Q2):
    d1 = (P2[0] - P1[0], P2[1] - P1[1]); d2 = (Q2[0] - Q1[0], Q2[1] - Q1[1]); den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-9: raise ValueError
    t = ((Q1[0] - P1[0]) * d2[1] - (Q1[1] - P1[1]) * d2[0]) / den
    return (P1[0] + t * d1[0], P1[1] + t * d1[1])
def arc_lab(fg, a1, a2, txt, r=3.0):
    """Label the arc from a1 counter-clockwise to a2 (degrees)."""
    m = a1 + ((a2 - a1) % 360) / 2; fg.text(cp(m, r * 1.2), txt, size=9.5)
def near_pt(P_, Y, r=3.0):
    """First point where segment P→Y meets the circle x² + y² = r²."""
    dx, dy = Y[0] - P_[0], Y[1] - P_[1]; a = dx * dx + dy * dy; b = 2 * (P_[0] * dx + P_[1] * dy); c = P_[0] ** 2 + P_[1] ** 2 - r * r
    t = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a); return (P_[0] + t * dx, P_[1] + t * dy)
def lin_expr(a, b): return f"{'' if a == 1 else a}x {'+' if b >= 0 else '-'} {abs(b)}" if b else f"{'' if a == 1 else a}x"
def solve_lin(a, b, c, d):
    """a x + b = c x + d → x (Fraction)"""
    if a == c: raise ValueError
    return F(d - b, a - c)

# =============== Skill 1: parts of a circle ===============
def parts_fig():
    while True:
        t = [R.randrange(0, 360, 5) for _ in range(5)]
        a = sorted(t)
        if min((a[(i + 1) % 5] - a[i]) % 360 for i in range(5)) >= 30: break
    tb, ta, tc, te, tf = t
    if min(abs(((tb + 180) - x) % 360) for x in (ta, tc, te, tf)) < 25 or min(abs(((tb + 180) - x + 180) % 360 - 180) for x in (ta, tc, te, tf)) < 25: raise AssertionError
    if abs(((ta - tc) % 360) - 180) < 30: raise AssertionError
    O = (0, 0); Pb, Pd = cp(tb), cp(tb + 180); Pa, Pc, Pe, Pf = cp(ta), cp(tc), cp(te), cp(tf)
    u = (-math.sin(math.radians(tf)), math.cos(math.radians(tf))); G = (Pf[0] + 2.6 * u[0], Pf[1] + 2.6 * u[1])
    fg = Fig(4.0, 3.6); fg.circle(O, 3); fg.seg(Pb, Pd); fg.seg(Pa, Pc); fg.seg(O, Pe); fg.seg(Pf, G)
    for P_, n_ in ((O, "O"), (Pb, "B"), (Pd, "D"), (Pa, "A"), (Pc, "C"), (Pe, "E"), (Pf, "F"), (G, "G")):
        d = math.hypot(*P_) or 1; fg.dot(P_, n_, off=(11 * P_[0] / d, 11 * P_[1] / d) if P_ != O else (-9, -9))
    return fg.save(B, nm("parts"), "Circle with center O. Segment BD passes through O; segment AC joins two points of the circle; segment OE joins the center to the circle; segment FG touches the circle only at F.")
def mk_parts():
    d_ = parts_fig(); k = R.random()
    if k < 0.3:
        B.orq(1, lv(), "Use the figure of circle O.", [("Name a radius.", "OE (also OB or OD)"), ("Name a diameter.", "BD"), ("Name a chord that is not a diameter.", "AC"), ("Name the tangent segment and the point of tangency.", "FG; point F")], ["A radius joins O to the circle.", "A diameter is a chord through O.", "A chord joins two points of the circle.", "A tangent meets the circle at exactly one point."], diagram=d_, tags=["diagram"])
    elif k < 0.55:
        B.sel(1, lv(), "Select ALL segments in the figure that are chords of circle O.", ["BD", "AC"], ["OE", "FG", "OB"], ["A chord has both endpoints on the circle; a diameter is a chord."], diagram=d_, tags=["diagram", "misconception"])
    elif k < 0.75:
        B.mc(1, lv(), "In the figure, which term best describes segment FG?", "tangent segment", ["chord", "secant", "radius"], ["FG meets the circle only at F."], diagram=d_, tags=["diagram"])
    else:
        r_ = R.randint(3, 15) + R.choice([0, F(1, 2)])
        B.orq(1, lv(), f"In the figure, OE = {fr(r_)}.", [("Find OB.", fr(r_)), ("Find BD.", fr(2 * r_)), ("Can chord AC be longer than BD? Explain.", "No; a diameter is the longest chord"), ("Find the circumference.", f"{pit(2 * r_)}")], ["All radii are congruent.", "d = 2r.", "Diameter is the longest chord.", "C = 2πr."], diagram=d_, tags=["diagram"])
def mk_rd_alg():
    a, c = R.randint(1, 3), R.randint(3, 7); x = R.randint(2, 12); b = R.randint(-4, 9)
    if c == 2 * a: raise ValueError
    r_ = a * x + b; d = 2 * r_ - c * x
    if r_ <= 0: raise ValueError
    assert solve_lin(2 * a, 2 * b, c, d) == x
    if R.random() < 0.5:
        B.sa(1, lv(), f"In circle P, radius PA = {lin_expr(a, b)} and diameter BC = {lin_expr(c, d)}. Find x and the diameter.", f"x = {x}; BC = {2 * r_}", [f"Diameter = 2 · radius: {lin_expr(c, d)} = 2({lin_expr(a, b)}).", f"x = {x}, so BC = {2 * r_}."])
    else:
        B.mc(1, lv(), f"In circle P, radius PA = {lin_expr(a, b)} and diameter BC = {lin_expr(c, d)}. What is x?", str(x), [fr(solve_lin(a, b, c, d)) if a != c else str(x + 1), str(x + 2), str(2 * x)], ["Set the diameter equal to twice the radius."], tags=["misconception"])
CIRC_ST = [("Every diameter is a chord", True), ("Every chord is a diameter", False), ("All radii of a circle are congruent", True), ("A secant line intersects a circle in exactly one point", False),
           ("A tangent line intersects a circle in exactly one point", True), ("The longest chord of a circle is a diameter", True), ("Concentric circles have the same center", True), ("A semicircle measures 360°", False),
           ("A major arc measures more than 180°", True), ("Two circles are congruent when their radii are congruent", True), ("A radius is a chord", False), ("A minor arc measures more than 180°", False)]
def mk_circ_sel():
    r_ = R.randint(2, 20); pool = R.sample(CIRC_ST, 4)
    st = pool + [(f"The diameter is {2 * r_}", True), (f"A chord of length {2 * r_ + R.randint(1, 5)} is possible", False)]
    if sum(v for _, v in st) < 2 or all(v for _, v in st): raise AssertionError
    R.shuffle(st)
    B.sel(1, lv(), f"Circle O has radius {r_}. Select ALL true statements.", [s for s, v in st if v], [s for s, v in st if not v], ["Apply the definitions of chord, diameter, radius, secant, tangent and arcs."], tags=["concept"])
def mk_arc_name():
    m1 = R.randrange(40, 170, 10); t0 = R.randrange(0, 360, 10)
    fg = Fig(3.8, 3.4); fg.circle((0, 0), 3); A_, B_ = cp(t0), cp(t0 + m1); C_ = cp(t0 + m1 + (360 - m1) / 2); fg.seg((0, 0), A_); fg.seg((0, 0), B_)
    for P_, n_ in ((A_, "A"), (B_, "B"), (C_, "C")): fg.dot(P_, n_, off=(11 * P_[0] / 3, 11 * P_[1] / 3))
    fg.dot((0, 0), "O", off=(-9, -9)); fg.angle((0, 0), A_, B_, f"{m1}°")
    d_ = fg.save(B, nm("arcname"), f"Circle O with points A, B and C; central angle AOB measures {m1}° and C lies on the larger arc from A to B.")
    if R.random() < 0.6:
        B.orq(1, lv(), "Use the figure.", [("Name the minor arc with endpoints A and B.", "arc AB"), ("Name the major arc with endpoints A and B.", "arc ACB"), ("Find m(arc AB).", f"{m1}°"), ("Find m(arc ACB).", f"{360 - m1}°")], ["Minor arcs use two letters.", "Major arcs use three letters.", "Equal to the central angle.", "360° − minor arc."], diagram=d_, tags=["diagram"])
    else:
        B.mc(1, lv(), f"Which arc in the figure measures {360 - m1}°?", "arc ACB", ["arc AB", "arc AC", "arc BA"], ["The major arc is named with three letters."], diagram=d_, tags=["diagram"])
def mk_arc_class():
    m = R.choice(list(range(20, 360, 10)))
    kind = "minor arc" if m < 180 else "semicircle" if m == 180 else "major arc"
    B.mc(1, lv(), f"An arc of a circle measures {m}°. Classify it.", kind, [k for k in ("minor arc", "semicircle", "major arc", "central angle") if k != kind], ["Minor < 180° = semicircle < major."])

# =============== Skill 2: central angles and arcs ===============
def mk_central_fig():
    while True:
        a = [R.randrange(30, 150, 5) for _ in range(3)]
        if sum(a) < 330: break
    a.append(360 - sum(a)); t0 = R.randrange(0, 90, 5); ang = [t0, t0 + a[0], t0 + a[0] + a[1], t0 + a[0] + a[1] + a[2]]
    fg = Fig(3.9, 3.6); fg.circle((0, 0), 3); P_ = [cp(t) for t in ang]
    for p, n_ in zip(P_, "ABCD"): fg.seg((0, 0), p); fg.dot(p, n_, off=(11 * p[0] / 3, 11 * p[1] / 3))
    fg.dot((0, 0), "O", off=(-10, -9))
    for i in range(3): fg.angle((0, 0), P_[i], P_[i + 1], f"{a[i]}°", r=0.7)
    d_ = fg.save(B, nm("central"), f"Circle O with radii OA, OB, OC, OD in counterclockwise order; ∠AOB = {a[0]}°, ∠BOC = {a[1]}°, ∠COD = {a[2]}°.")
    k = R.random()
    if k < 0.55:
        B.orq(2, lv(), "Use the central angles in the figure.", [("Find m(arc AB).", f"{a[0]}°"), ("Find m(arc ABC).", f"{a[0] + a[1]}°"), ("Find m(arc DA).", f"{a[3]}°"), ("Find m(arc BCD) and m(arc BAD).", f"{a[1] + a[2]}°; {360 - a[1] - a[2]}°")], ["Arc = central angle.", "Arc Addition Postulate.", "360° minus the rest.", "Minor and major arcs sum to 360°."], diagram=d_, tags=["diagram"])
    elif k < 0.8:
        B.sa(2, lv(), "Find m∠DOA in the figure.", f"{a[3]}°", [f"360 − ({a[0]} + {a[1]} + {a[2]}) = {a[3]}."], diagram=d_, tags=["diagram"])
    else:
        B.mc(2, lv(), "Find m(arc ACD) in the figure, the major arc from A to D through B and C.", f"{a[0] + a[1] + a[2]}°", [f"{a[3]}°", f"{a[1] + a[2]}°", f"{360 - a[0]}°"], ["Add the three arcs: AB + BC + CD."], diagram=d_, tags=["diagram"])
def mk_central_alg():
    x = R.randint(5, 25); co = [R.randint(1, 5) for _ in range(3)]; b = [R.randrange(-20, 30, 2) for _ in range(2)]
    b.append(360 - sum(c * x for c in co) - sum(b)); v = [c * x + bb for c, bb in zip(co, b)]
    if min(v) < 30 or max(v) > 200 or abs(b[2]) > 80: raise ValueError
    assert sum(v) == 360 and F(360 - sum(b), sum(co)) == x
    ex = [f"({lin_expr(c, bb)})°" for c, bb in zip(co, b)]
    t0 = R.randrange(0, 90, 5); ang = [t0, t0 + v[0], t0 + v[0] + v[1]]
    fg = Fig(3.9, 3.6); fg.circle((0, 0), 3); P_ = [cp(t) for t in ang]
    for p, n_ in zip(P_, "PQR"): fg.seg((0, 0), p); fg.dot(p, n_, off=(11 * p[0] / 3, 11 * p[1] / 3))
    fg.dot((0, 0), "O", off=(-10, -9))
    for i in range(3): fg.angle((0, 0), P_[i], P_[(i + 1) % 3], ex[i], r=0.75)
    d_ = fg.save(B, nm("centalg"), f"Circle O divided by radii OP, OQ, OR into central angles {ex[0]}, {ex[1]}, {ex[2]}.")
    if R.random() < 0.6:
        B.orq(2, lv(), "The three central angles in the figure fill the circle.", [("Write an equation.", f"{ex[0]} + {ex[1]} + {ex[2]} = 360°".replace("°", "")), ("Solve for x.", str(x)), ("Find m(arc PQ).", f"{v[0]}°"), ("Find m(arc PRQ).", f"{360 - v[0]}°")], ["The central angles around O sum to 360°.", "Combine like terms.", "Substitute.", "Major arc = 360° − minor arc."], diagram=d_, tags=["diagram"])
    else:
        B.sa(2, lv(), "The central angles in the figure fill the circle. Find x and m(arc QR).", f"x = {x}; {v[1]}°", ["Sum to 360°.", "Substitute."], diagram=d_, tags=["diagram"])
def mk_arc_sel():
    th = R.randrange(20, 170, 5)
    st = {f"m(arc AB) = {th}°": True, "arc AB ≅ arc CD": True, "chord AB ≅ chord CD": True, f"m(arc CD) = {180 - th}°": False, f"The major arc from C to D measures {360 - th}°": True, "AB ∥ CD": False}
    B.sel(2, lv(), f"A, B, C, D lie on ⊙O and ∠AOB ≅ ∠COD with m∠AOB = {th}°. Select ALL statements that must be true.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["In the same circle, congruent central angles have congruent arcs and congruent chords.", "Nothing forces the chords to be parallel."], tags=["concept"])
def mk_arc_app():
    k = R.random()
    if k < 0.35:
        p = R.choice([5, 10, 12.5, 15, 20, 25, 30, 35, 40, 45]); v = F(p) * 360 / 100 if isinstance(p, int) else F(25, 2) * 360 / 100
        B.sa(2, lv(), f"In a circle graph, a category is {p}% of the data. What central angle does its sector have?", f"{fr(v)}°", [f"{p}% of 360° = {fr(v)}°."], tags=["application"])
    elif k < 0.7:
        h1, h2 = sorted(R.sample(range(1, 13), 2)); v = min(30 * (h2 - h1), 360 - 30 * (h2 - h1))
        if v == 0: raise ValueError
        B.mc(2, lv(), f"The numbers on a clock face are equally spaced. What is the measure of the smaller arc from the {h1} to the {h2}?", f"{v}°", [f"{360 - v}°" if v != 180 else "90°", f"{v // 2}°", f"{12 * (h2 - h1)}°"], ["Each hour mark is 360° ÷ 12 = 30° apart."], tags=["application"])
    else:
        n = R.choice([5, 6, 8, 9, 10, 12, 15, 18]); s = R.randint(2, n // 2)
        B.sa(2, lv(), f"A wheel has {n} equally spaced spokes. Find the arc measure between spokes that are {s} apart.", f"{fr(F(360 * s, n))}°", [f"360° ÷ {n} = {fr(F(360, n))}° per gap; × {s}."], tags=["application"])

# =============== Skill 3: inscribed angles ===============
def insc_fig(m, extra=None, label_arc=True, ang_lab=None):
    t0 = R.randrange(200, 340, 5); A_, C_ = cp(t0), cp(t0 + m); tb = t0 + m + (360 - m) * R.uniform(0.3, 0.7)
    B_ = cp(tb); fg = Fig(3.8, 3.6); fg.circle((0, 0), 3); fg.seg(B_, A_); fg.seg(B_, C_)
    for P_, n_ in ((A_, "A"), (B_, "B"), (C_, "C")): fg.dot(P_, n_, off=(11 * P_[0] / 3, 11 * P_[1] / 3))
    fg.dot((0, 0), "O", off=(-8, -8), filled=True)
    if label_arc: arc_lab(fg, t0, t0 + m, label_arc if isinstance(label_arc, str) else f"{m}°")
    if ang_lab: fg.angle(B_, A_, C_, ang_lab, r=0.55)
    if extra: extra(fg, t0)
    return fg
def mk_insc():
    m = R.randrange(40, 264, 4) if R.random() < 0.8 else R.randrange(41, 179, 2) * 2
    if m == 180: raise ValueError
    k = R.random()
    if k < 0.4:
        fg = insc_fig(m); d_ = fg.save(B, nm("insc"), f"Inscribed angle ABC in circle O intercepts arc AC, labeled {m}°.")
        B.mc(3, lv(), "Find m∠ABC.", dg(F(m, 2)), [f"{m}°", dg(180 - F(m, 2)), dg(360 - m)], ["An inscribed angle is half its intercepted arc."], diagram=d_, tags=["diagram", "misconception"])
    elif k < 0.7:
        fg = insc_fig(m, label_arc=False, ang_lab=dg(F(m, 2))); d_ = fg.save(B, nm("insc"), f"Inscribed angle ABC in circle O measures {fr(F(m, 2))}° and intercepts arc AC.")
        B.sa(3, lv(), "Find m(arc AC) and the central angle m∠AOC.", f"{m}°; {m}°", ["Arc = 2 × inscribed angle.", "The central angle equals its arc."], diagram=d_, tags=["diagram"])
    else:
        if m >= 180: raise ValueError
        def ex(fg, t0):
            td = t0 + m + R.randrange(30, 360 - m - 20, 5); D_ = cp(td); fg.seg(D_, cp(t0)); fg.seg(D_, cp(t0 + m)); fg.dot(D_, "D", off=(11 * D_[0] / 3, 11 * D_[1] / 3))
            E_ = cp(t0 + m / 2); fg.seg(E_, cp(t0)); fg.seg(E_, cp(t0 + m)); fg.dot(E_, "E", off=(11 * E_[0] / 3, 11 * E_[1] / 3))
        fg = insc_fig(m, extra=ex); d_ = fg.save(B, nm("insc"), f"Circle O with points A, C and arc AC labeled {m}°; B and D lie on the major arc and E lies on minor arc AC; angles ABC, ADC and AEC are drawn.")
        B.orq(3, "honors", "Use the figure.", [("Find m∠ABC.", dg(F(m, 2))), ("Find m∠ADC. Why?", f"{dg(F(m, 2))}; it intercepts the same arc"), ("Find m∠AEC.", dg(180 - F(m, 2))), ("What is m∠ABC + m∠AEC? What does that show about ABCE?", "180°; it is a cyclic quadrilateral (opposite angles supplementary)")], ["½ arc AC.", "Inscribed angles on the same arc are congruent.", f"∠AEC intercepts the major arc {360 - m}°.", "Opposite angles of an inscribed quadrilateral."], diagram=d_, tags=["diagram", "challenge"])
def mk_insc_alg():
    a, c = R.randint(1, 4), R.randint(2, 9); x = R.randint(4, 20); b = R.randint(-10, 20)
    ang = a * x + b; arc = 2 * ang; d = arc - c * x
    if not (10 < ang < 170) or c == 2 * a: raise ValueError
    assert solve_lin(2 * a, 2 * b, c, d) == x
    B.sa(3, lv(), f"Inscribed ∠PQR = ({lin_expr(a, b)})° intercepts arc PR = ({lin_expr(c, d)})°. Find x and m(arc PR).", f"x = {x}; {arc}°", [f"2({lin_expr(a, b)}) = {lin_expr(c, d)}.", f"x = {x}."])
def mk_semi():
    a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]); s = R.randint(1, 3); a, b, c = a * s, b * s, c * s
    k = R.random()
    if k < 0.5:
        A_, Bv, C_ = cp(180), cp(0), None; th = math.degrees(math.atan2(b, a)); C_ = cp(180 - 2 * math.degrees(math.atan2(a, b)))
        fg = Fig(3.8, 3.4); fg.circle((0, 0), 3); fg.seg(A_, Bv); fg.seg(A_, C_); fg.seg(C_, Bv); fg.dot((0, 0), "O", off=(0, -10))
        for P_, n_ in ((A_, "A"), (Bv, "B"), (C_, "C")): fg.dot(P_, n_, off=(11 * P_[0] / 3, 11 * P_[1] / 3))
        fg.side(A_, C_, str(a), center=(0, 0)); fg.side(C_, Bv, str(b), center=(0, 0))
        d_ = fg.save(B, nm("semi"), f"Triangle ABC inscribed in circle O with AB through O; AC = {a}, CB = {b}.")
        B.orq(3, lv(), "AB is a diameter of circle O.", [("Find m∠ACB. Why?", "90°; it is inscribed in a semicircle"), ("Find AB.", str(c)), ("Find the radius.", fr(F(c, 2))), ("Find the circumference.", pit(c))], ["Inscribed angle on a 180° arc.", "Pythagorean Theorem.", "r = d/2.", "C = πd."], diagram=d_, tags=["diagram"])
    else:
        x = R.randrange(20, 70, 2)
        B.mc(3, lv(), f"△ABC is inscribed in a circle with AB a diameter. If m∠A = {x}°, find m∠B.", f"{90 - x}°", [f"{180 - x}°", f"{x}°", f"{2 * x}°"], ["∠C = 90° (inscribed in a semicircle), so ∠B = 90° − ∠A."])
def mk_cyclic():
    k = R.random()
    if k < 0.45:
        while True:
            a = [R.randrange(40, 140, 10) for _ in range(3)]
            if sum(a) < 320: break
        a.append(360 - sum(a)); t0 = R.randrange(0, 90, 5); ang = [t0, t0 + a[0], t0 + a[0] + a[1], t0 + a[0] + a[1] + a[2]]
        P_ = [cp(t) for t in ang]; fg = Fig(3.8, 3.6); fg.circle((0, 0), 3); fg.poly(P_)
        for p, n_ in zip(P_, "ABCD"): fg.dot(p, n_, off=(11 * p[0] / 3, 11 * p[1] / 3))
        for i in range(4): arc_lab(fg, ang[i], ang[(i + 1) % 4] if i < 3 else ang[0] + 360, f"{a[i]}°")
        A_ = F(a[1] + a[2], 2); Bq = F(a[2] + a[3], 2); C_ = F(a[3] + a[0], 2); D_ = F(a[0] + a[1], 2)
        for v, (i, j, l) in zip((A_, Bq, C_, D_), ((0, 1, 3), (1, 2, 0), (2, 3, 1), (3, 0, 2))): assert abs(ang_at(P_[i], P_[j], P_[l]) - float(v)) < 1e-6
        d_ = fg.save(B, nm("cyclic"), f"Quadrilateral ABCD inscribed in a circle; arcs AB = {a[0]}°, BC = {a[1]}°, CD = {a[2]}°, DA = {a[3]}°.")
        B.orq(3, lv(), "Use the arc measures in the figure.", [("Find m∠A.", dg(A_)), ("Find m∠C.", dg(C_)), ("Find m∠B and m∠D.", f"{dg(Bq)}; {dg(D_)}"), ("Check a property of inscribed quadrilaterals.", f"∠A + ∠C = {fr(A_ + C_)}° and ∠B + ∠D = {fr(Bq + D_)}°: opposite angles are supplementary")], ["∠A intercepts arc BCD.", "∠C intercepts arc DAB.", "Half the far arcs.", "Supplementary."], diagram=d_, tags=["diagram"])
    elif k < 0.75:
        x = R.randint(10, 40); a, c = R.randint(1, 3), R.randint(1, 3); b = R.randint(-10, 30); d = 180 - (a + c) * x - b
        A_ = a * x + b; C_ = c * x + d
        if not (20 < A_ < 160 and 20 < C_ < 160) or abs(d) > 120: raise ValueError
        B.sa(3, lv(), f"ABCD is inscribed in a circle with m∠A = ({lin_expr(a, b)})° and m∠C = ({lin_expr(c, d)})°. Find x and m∠C.", f"x = {x}; m∠C = {C_}°", ["Opposite angles of an inscribed quadrilateral are supplementary.", f"x = {x}."])
    else:
        q = R.choice(["rectangle", "square", "isosceles trapezoid", "rhombus that is not a square", "parallelogram that is not a rectangle", "kite with no right angles"])
        yes = q in ("rectangle", "square", "isosceles trapezoid")
        sh = R.sample(["rectangle", "square", "isosceles trapezoid"], 2) + R.sample(["rhombus that is not a square", "parallelogram that is not a rectangle", "kite with no right angles", "trapezoid that is not isosceles"], 2)
        B.sel(3, lv(), f"Select ALL shapes that can always be inscribed in a circle ({', '.join(sh)}).", [s for s in sh if s in ("rectangle", "square", "isosceles trapezoid")], [s for s in sh if s not in ("rectangle", "square", "isosceles trapezoid")], ["A quadrilateral is cyclic exactly when its opposite angles are supplementary."], tags=["concept"])
def mk_insc_sel():
    m = R.randrange(30, 170, 2)
    st = {f"m∠ABC = {fr(F(m, 2))}°": True, f"m∠AOC = {m}°": True, f"Any other inscribed angle intercepting arc AC measures {fr(F(m, 2))}°": True, f"m∠ABC = {m}°": False, f"m∠AOC = {fr(F(m, 2))}°": False, f"m∠BAC + m∠BCA = {180 - F(m, 2)}°": True}
    B.sel(3, lv(), f"Inscribed ∠ABC in ⊙O intercepts minor arc AC, and m(arc AC) = {m}°. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Inscribed angle = ½ arc; central angle = arc; triangle sum."], tags=["concept"])

# =============== Skill 4: angles from chords, secants, tangents ===============
def chord_inside():
    while True:
        a = [R.randrange(40, 130, 10) for _ in range(3)]
        if sum(a) < 320 and (a[0] + a[2]) % 2 == 0: break
    a.append(360 - sum(a)); t0 = R.randrange(0, 90, 5); ang = [t0, t0 + a[0], t0 + a[0] + a[1], t0 + a[0] + a[1] + a[2]]
    P_ = [cp(t) for t in ang]; E = inter(P_[0], P_[2], P_[1], P_[3]); v = F(a[0] + a[2], 2)
    assert abs(ang_at(E, P_[0], P_[1]) - float(v)) < 1e-6
    return a, ang, P_, E, v
def mk_chords_in():
    a, ang, P_, E, v = chord_inside(); fg = Fig(3.8, 3.6); fg.circle((0, 0), 3); fg.seg(P_[0], P_[2]); fg.seg(P_[1], P_[3])
    for p, n_ in zip(P_, "ABCD"): fg.dot(p, n_, off=(11 * p[0] / 3, 11 * p[1] / 3))
    fg.dot(E, "E", off=(10, -2)); arc_lab(fg, ang[0], ang[1], f"{a[0]}°"); arc_lab(fg, ang[2], ang[3], f"{a[2]}°")
    d_ = fg.save(B, nm("chordin"), f"Chords AC and BD intersect at E inside the circle; arc AB = {a[0]}°, arc CD = {a[2]}°.")
    k = R.random()
    if k < 0.45:
        B.mc(4, lv(), "Find m∠AEB.", dg(v), [dg(a[0] + a[2]), dg(F(abs(a[0] - a[2]), 2)) if a[0] != a[2] else "90°", dg(180 - v)], ["Vertex inside the circle: half the SUM of the intercepted arcs."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(4, lv(), "Use the figure.", [("Find m∠AEB.", dg(v)), ("Find m∠CED.", dg(v)), ("Find m∠BEC.", dg(180 - v)), ("Find m(arc BC) + m(arc DA).", f"{a[1] + a[3]}°")], ["½(arc AB + arc CD).", "Vertical angles.", "Linear pair.", "360° − the labeled arcs."], diagram=d_, tags=["diagram"])
def secants_out(tangent=False):
    if tangent:
        f = R.randrange(120, 260, 10); n = R.randrange(20, 120, 10)
        if f - n < 20 or f + n > 340: raise ValueError
        T = cp(0); X = cp(-n); Y = cp(f); P_ = inter(X, Y, T, (3, 1))
        if math.dist(P_, X) < 0.8 or math.hypot(*P_) > 9: raise ValueError
        assert math.dist(P_, X) < math.dist(P_, Y)
        v = F(f - n, 2); assert abs(ang_at(P_, T, Y) - float(v)) < 1e-6
        return f, n, (T, X, Y), P_, v, (0, -n, f)
    n = R.randrange(20, 100, 10); f = R.randrange(n + 20, 220, 10); s1 = R.randrange(40, 360 - n - f - 30, 10) if 360 - n - f - 30 > 40 else 0
    if not s1: raise ValueError
    s2 = 360 - n - f - s1
    if s2 < 30: raise ValueError
    tx1 = n / 2; ty1 = tx1 + s1; ty2 = ty1 + f; tx2 = -n / 2
    X1, Y1, Y2, X2 = cp(tx1), cp(ty1), cp(ty2), cp(tx2); P_ = inter(X1, Y1, X2, Y2)
    if math.hypot(*P_) < 3.2 or math.hypot(*P_) > 14 or math.dist(P_, X1) > math.dist(P_, Y1) or math.dist(P_, X2) > math.dist(P_, Y2): raise ValueError
    v = F(f - n, 2); assert abs(ang_at(P_, X1, X2) - float(v)) < 1e-6
    return f, n, (X1, Y1, Y2, X2), P_, v, (tx1, ty1, ty2, tx2)
def mk_secants():
    f, n, (X1, Y1, Y2, X2), P_, v, (tx1, ty1, ty2, tx2) = secants_out()
    fg = Fig(4.4, 3.4); fg.circle((0, 0), 3); fg.seg(P_, Y1); fg.seg(P_, Y2)
    for p, n_ in ((X1, "A"), (Y1, "B"), (Y2, "C"), (X2, "D"), (P_, "P")): fg.dot(p, n_, off=(11 * p[0] / math.hypot(*p), 11 * p[1] / math.hypot(*p)))
    arc_lab(fg, ty1, ty2, f"{f}°"); arc_lab(fg, tx2, tx1, f"{n}°", r=2.0)
    d_ = fg.save(B, nm("secants"), f"Two secants from external point P: one passes through A then B, the other through D then C. Far arc BC = {f}°, near arc AD = {n}°.")
    if R.random() < 0.5:
        B.mc(4, lv(), "Find m∠P.", dg(v), [dg(F(f + n, 2)), dg(f - n), dg(180 - v)], ["Vertex outside: half the DIFFERENCE of the intercepted arcs."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.sa(4, "honors", f"In the figure, suppose m∠P were unknown but known to be {fr(v)}° and only arc AD = {n}° were given. Find the far arc BC.", f"{f}°", [f"{fr(v)} = ½(BC − {n}) → BC = {f}°."], diagram=d_, tags=["diagram", "challenge"])
def mk_sec_tan():
    f, n, (T, X, Y), P_, v, _ = secants_out(True)
    fg = Fig(4.0, 3.6); fg.circle((0, 0), 3); fg.seg(P_, Y); fg.seg(P_, (3, -2.2) if P_[1] > 0 else (3, 2.2))
    fg.seg(P_, T)
    for p, n_ in ((T, "T"), (X, "A"), (Y, "B"), (P_, "P")): fg.dot(p, n_, off=(11 * p[0] / math.hypot(*p), 11 * p[1] / math.hypot(*p)))
    arc_lab(fg, 0, f, f"{f}°"); arc_lab(fg, -n, 0, f"{n}°", r=2.0)
    d_ = fg.save(B, nm("sectan"), f"Tangent PT and secant PAB from external point P; far arc TB = {f}°, near arc TA = {n}°.")
    B.orq(4, lv(), "PT is tangent to the circle at T.", [("Is the vertex inside, on, or outside the circle?", "outside"), ("Which arcs does ∠P intercept?", f"arc TB ({f}°) and arc TA ({n}°)"), ("Write the formula.", "m∠P = ½(far arc − near arc)"), ("Find m∠P.", dg(v))], ["P is outside.", "Far and near arcs.", "Outside-angle theorem.", f"½({f} − {n})."], diagram=d_, tags=["diagram"])
def mk_two_tan():
    m = R.randrange(90, 170, 5); h = math.radians(m / 2); T1, T2 = cp(m / 2), cp(-m / 2); P_ = (3 / math.cos(h), 0)
    v = 180 - m; assert abs(ang_at(P_, T1, T2) - v) < 1e-6
    fg = Fig(4.4, 3.2); fg.circle((0, 0), 3); fg.seg(P_, T1); fg.seg(P_, T2)
    for p, n_ in ((T1, "A"), (T2, "B"), (P_, "P")): fg.dot(p, n_, off=(11 * p[0] / math.hypot(*p), 11 * p[1] / math.hypot(*p)))
    fg.text((2.3, 0), f"{m}°", size=9.5); fg.dot((0, 0), "O", off=(-9, -8))
    d_ = fg.save(B, nm("twotan"), f"Tangent segments PA and PB from external point P; minor arc AB = {m}°.")
    if R.random() < 0.5:
        B.mc(4, lv(), "PA and PB are tangent to the circle. Find m∠APB.", f"{v}°", [dg(F(m, 2)), f"{m}°", f"{360 - m}°"], ["Major arc = 360° − m; ∠P = ½(major − minor) = 180° − minor arc."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(4, lv(), "PA and PB are tangent to the circle.", [("Find the major arc AB.", f"{360 - m}°"), ("Find m∠APB.", f"{v}°"), ("Find m∠AOB (O the center).", f"{m}°"), ("Explain why ∠APB + ∠AOB = 180°.", "∠OAP = ∠OBP = 90° in quadrilateral OAPB, whose angles sum to 360°")], ["360° − minor.", "½(major − minor).", "Central angle = arc.", "Tangent ⟂ radius."], diagram=d_, tags=["diagram", "reasoning"])
def mk_tan_chord():
    m = R.randrange(40, 320, 4)
    if m == 180: raise ValueError
    k = R.random()
    if k < 0.5:
        B.mc(4, lv(), f"A tangent and a chord meet at the point of tangency T. The chord's intercepted arc (inside the angle) measures {m}°. Find the angle between them.", dg(F(m, 2)), [f"{m}°", dg(180 - F(m, 2)), dg(360 - m)], ["Tangent–chord angle = ½ intercepted arc."], tags=["misconception"])
    else:
        x = R.randint(5, 30); c = R.randint(3, 9); ang = R.randrange(20, 170, 2); arc = 2 * ang; d = arc - c * x
        assert c * x + d == arc
        B.sa(4, lv(), f"A tangent–chord angle measures {ang}° and its intercepted arc measures ({lin_expr(c, d)})°. Find x.", str(x), [f"Arc = 2 × {ang}° = {arc}°.", f"{lin_expr(c, d)} = {arc} → x = {x}."])
def mk_ang_sel():
    kind = R.choice(["in", "out", "on"])
    vals = {"in": "half the sum of the intercepted arcs", "out": "half the difference of the intercepted arcs", "on": "half the intercepted arc"}
    nm_ = {"in": "two chords intersecting inside the circle", "out": "two secants meeting outside the circle", "on": "a tangent and a chord meeting on the circle"}
    B.mc(4, lv(), f"Which rule gives the angle formed by {nm_[kind]}?", vals[kind], [vals[k] for k in vals if k != kind] + ["equal to the intercepted arc"], ["Inside: ½(sum); on: ½(arc); outside: ½(difference)."], tags=["concept"])
def mk_ang_sel2():
    a, ang, P_, E, v = chord_inside()
    st = {f"m∠AEB = {fr(v)}°": True, f"m∠AED = {fr(180 - v)}°": True, f"m∠AEB = {a[0] + a[2]}°": False, f"m∠AEB = ½({a[0]}° + {a[2]}°)": True, f"m∠AED = {fr(F(a[1] + a[3], 2))}°": True, f"m∠AEB = ½({max(a[0], a[2])}° − {min(a[0], a[2])}°)": False}
    B.sel(4, lv(), f"Chords AC and BD meet at E inside a circle (points in order A, B, C, D). m(arc AB) = {a[0]}°, m(arc BC) = {a[1]}°, m(arc CD) = {a[2]}°. Select ALL true statements.", [k for k, v_ in st.items() if v_], [k for k, v_ in st.items() if not v_], ["Inside angles are half the sum of the arcs they and their vertical angles intercept.", f"arc DA = {a[3]}°."], tags=["concept"])

# =============== Skill 5: tangents and radii ===============
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20), (20, 21, 29), (9, 40, 41), (12, 35, 37)]
def tan_fig(r, t, d, labels):
    s = 3.0 / r; th = math.acos(r / d); T = cp(math.degrees(th)); P_ = (3.0 * d / r, 0)
    fg = Fig(4.4, 3.0); fg.circle((0, 0), 3); fg.seg((0, 0), T); fg.seg(T, P_); fg.seg((0, 0), P_, ls="--")
    fg.dot((0, 0), "O", off=(-9, -8)); fg.dot(T, "T", off=(0, 10)); fg.dot(P_, "P", off=(10, 0)); fg.angle(T, (0, 0), P_, right=True, r=0.6)
    lo, lt, lp = labels; fg.side((0, 0), T, lo, center=(1, -2)); fg.side(T, P_, lt, center=(0, 0)); fg.side((0, 0), P_, lp, center=T)
    return fg
def mk_tan_pyth():
    r, t, d = R.choice(TRIP); s_ = R.choice([1, 1, 2]); r, t, d = r * s_, t * s_, d * s_
    if R.random() < 0.5: r, t = t, r
    miss = R.choice(["r", "t", "d"]); lab = [str(r) if miss != "r" else "r", str(t) if miss != "t" else "x", str(d) if miss != "d" else "x"]
    ans = {"r": r, "t": t, "d": d}[miss]
    d_ = tan_fig(r, t, d, lab).save(B, nm("tan"), f"Circle O with tangent segment PT; OT = {lab[0]}, PT = {lab[1]}, OP = {lab[2]}; right angle at T.")
    if R.random() < 0.55:
        B.sa(5, lv(), f"PT is tangent to ⊙O at T. Find the unknown length ({'radius r' if miss == 'r' else 'x'}).", str(ans), ["A tangent is perpendicular to the radius at the point of tangency.", "Pythagorean Theorem in right △OTP."], diagram=d_, tags=["diagram"])
    else:
        B.mc(5, lv(), f"PT is tangent to ⊙O at T. Find the unknown length.", str(ans), [rad(r * r + t * t) if miss != "d" else str(r + t), str(abs(d - r) if miss == "t" else d + 1), rad(abs(d * d - t * t)) if miss != "r" else str(d - t)], ["∠OTP = 90°.", "Pythagorean Theorem."], diagram=d_, tags=["diagram", "misconception"])
def mk_tan_test():
    r, t, d = R.choice(TRIP); ok = R.random() < 0.5
    if not ok: d = d + R.choice([-1, 1])
    yes = r * r + t * t == d * d
    B.mc(5, lv(), f"In ⊙O, OT = {r} is a radius, PT = {t}, and OP = {d}. Is PT tangent to ⊙O at T?", f"{'Yes' if yes else 'No'}: {r}² + {t}² {'=' if yes else '≠'} {d}²", [f"{'No' if yes else 'Yes'}: {r}² + {t}² {'≠' if yes else '='} {d}²", "Yes: PT is shorter than OP", "Cannot be determined"], ["Converse: if OT² + PT² = OP², then ∠OTP = 90° and PT is tangent."], tags=["reasoning"])
def mk_tan_two():
    x = R.randint(2, 12); a, c = R.randint(1, 6), R.randint(1, 6)
    if a == c: raise ValueError
    b = R.randint(-5, 15); d = a * x + b - c * x; L = a * x + b
    if L <= 0: raise ValueError
    ang = R.randrange(30, 120, 5); h = math.radians(90 - ang / 2); T1, T2 = cp(math.degrees(h)), cp(-math.degrees(h)); P_ = (3 / math.cos(h), 0)
    assert abs(ang_at(P_, T1, T2) - ang) < 1e-6
    fg = Fig(4.4, 3.2); fg.circle((0, 0), 3); fg.seg(P_, T1); fg.seg(P_, T2); fg.seg((0, 0), T1); fg.seg((0, 0), T2)
    for p, n_ in ((T1, "A"), (T2, "B"), (P_, "P"), ((0, 0), "O")): fg.dot(p, n_, off=(11 * p[0] / (math.hypot(*p) or 1), 11 * p[1] / (math.hypot(*p) or 1)) if p != (0, 0) else (-9, 0))
    fg.side(P_, T1, lin_expr(a, b), center=(0, 0)); fg.side(P_, T2, lin_expr(c, d), center=(0, 0)); fg.angle(P_, T1, T2, f"{ang}°", r=0.5)
    d_ = fg.save(B, nm("twotan"), f"Tangent segments PA = {lin_expr(a, b)} and PB = {lin_expr(c, d)} from P to circle O; m∠APB = {ang}°.")
    B.orq(5, lv(), "PA and PB are tangent to ⊙O.", [("Solve for x.", str(x)), ("Find PA.", str(L)), ("Find m∠OAP.", "90°"), ("Find m∠AOB.", f"{180 - ang}°")], ["Tangent segments from the same external point are congruent.", "Substitute.", "Tangent ⟂ radius.", "Quadrilateral OAPB: 360° − 90° − 90° − ∠P."], diagram=d_, tags=["diagram"])
def mk_tan_circ():
    x, y, z = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
    a, b, c = y + z, x + z, x + y
    A_, Bv, C_ = tri_from_sides(a, b, c); per = a + b + c; s = per / 2
    I = ((a * A_[0] + b * Bv[0] + c * C_[0]) / per, (a * A_[1] + b * Bv[1] + c * C_[1]) / per); area = abs((Bv[0] - A_[0]) * (C_[1] - A_[1]) - (C_[0] - A_[0]) * (Bv[1] - A_[1])) / 2; r = area / s
    def foot(P1, P2):
        dx, dy = P2[0] - P1[0], P2[1] - P1[1]; t = ((I[0] - P1[0]) * dx + (I[1] - P1[1]) * dy) / (dx * dx + dy * dy); return (P1[0] + t * dx, P1[1] + t * dy)
    Fab, Fbc, Fca = foot(A_, Bv), foot(Bv, C_), foot(C_, A_)
    assert abs(math.dist(A_, Fab) - x) < 1e-6 and abs(math.dist(Bv, Fbc) - y) < 1e-6
    fg = Fig(4.2, 3.6); fg.poly([A_, Bv, C_]); fg.circle(I, r); fg.names([A_, Bv, C_], "ABC")
    for P_, n_ in ((Fab, "D"), (Fbc, "E"), (Fca, "F")): fg.dot(P_, n_, off=(8 * (P_[0] - I[0]) / r, 8 * (P_[1] - I[1]) / r))
    fg.side(A_, Fab, str(x), center=I); fg.side(Bv, Fbc, str(y), center=I); fg.side(C_, Fca, str(z), center=I)
    d_ = fg.save(B, nm("incirc"), f"Circle inscribed in triangle ABC, tangent at D on AB, E on BC, F on CA; AD = {x}, BE = {y}, CF = {z}.")
    if R.random() < 0.5:
        B.orq(5, lv(), "The circle is inscribed in △ABC.", [("Find AF.", str(x)), ("Find BD.", str(y)), ("Find AB.", str(c)), ("Find the perimeter of △ABC.", str(per))], ["Tangent segments from A are congruent.", "Tangent segments from B.", "AD + DB.", f"2({x} + {y} + {z})."], diagram=d_, tags=["diagram"])
    else:
        B.sa(5, "honors", f"A circle is inscribed in △ABC with AB = {c}, BC = {a}, CA = {b}. It touches AB at D. Find AD.", str(x), ["Let AD = AF = p, BD = BE = q, CE = CF = r.", f"p + q = {c}, q + r = {a}, p + r = {b} → p = s − BC = {fr(F(per, 2))} − {a} = {x}."], tags=["challenge"])
def mk_tan_sel():
    r, t, d = R.choice(TRIP)
    st = {"OT ⟂ PT": True, f"OP = {d}": True, f"PT = {t}": True, f"The shortest distance from P to the circle is {d - r}": True, f"PT = {d - r}": False, "∠OPT is a right angle": False, f"OP = {r + t}": False}
    B.sel(5, lv(), f"PT is tangent to ⊙O at T, OT = {r}, and PT = {t}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Tangent ⟂ radius; OP = √(r² + PT²).", "Nearest point of the circle lies on OP: OP − r."], tags=["concept"])

# =============== Skill 6: chords and distance from center ===============
CTRIP = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (8, 6, 10), (12, 5, 13), (15, 8, 17), (16, 12, 20), (20, 15, 25)]
def chord_fig(d, h, r, lab):
    s = 3.0 / r; yd = -d * s; xh = h * s; A_, B_ = (-xh, yd), (xh, yd); M = (0, yd)
    fg = Fig(3.8, 3.6); fg.circle((0, 0), 3); fg.seg(A_, B_); fg.seg((0, 0), M); fg.seg((0, 0), B_, ls="--")
    fg.dot((0, 0), "O", off=(0, 9)); fg.dot(A_, "A", off=(-9, -6)); fg.dot(B_, "B", off=(9, -6)); fg.dot(M, "M", off=(0, -10)); fg.angle(M, B_, (0, 0), right=True, r=0.5)
    ld, lh, lr = lab
    if ld: fg.text((0, yd / 2), ld, off=(-10, 0), size=9.5)
    if lh: fg.text(((xh) / 2, yd), lh, off=(0, -10), size=9.5)
    if lr: fg.side((0, 0), B_, lr, center=(-2, -1))
    return fg
def mk_chord_dist():
    d, h, r = R.choice(CTRIP); s_ = R.choice([1, 1, 2]); d, h, r = d * s_, h * s_, r * s_
    miss = R.choice(["chord", "d", "r"])
    lab = (str(d) if miss != "d" else "x", str(h) if miss != "chord" else "", str(r) if miss != "r" else "r")
    d_ = chord_fig(d, h, r, lab).save(B, nm("chord"), f"Circle O with chord AB; OM ⟂ AB at M; OM = {lab[0]}, MB = {lab[1] or 'unknown'}, OB = {lab[2]}.")
    if miss == "chord":
        B.orq(6, lv(), "OM ⟂ AB in ⊙O.", [("What does OM do to AB? Why?", "bisects it; a radius/diameter perpendicular to a chord bisects the chord"), ("Find MB.", str(h)), ("Find AB.", str(2 * h)), ("Would a chord closer to O be longer or shorter?", "longer")], ["Perpendicular from the center bisects a chord.", f"√({r}² − {d}²).", "AB = 2·MB.", "Chords nearer the center are longer."], diagram=d_, tags=["diagram"])
    else:
        ans = d if miss == "d" else r
        B.sa(6, lv(), f"OM ⟂ AB and AB = {2 * h}. Find the unknown {'distance x' if miss == 'd' else 'radius r'}.", str(ans), [f"MB = ½·AB = {h}.", "Pythagorean Theorem in △OMB."], diagram=d_, tags=["diagram"])
def mk_chord_cong():
    x = R.randint(2, 12); a, c = R.randint(2, 7), R.randint(1, 6)
    if a == c: raise ValueError
    b = R.randint(-6, 10); L = a * x + b; d = L - c * x; dist = R.randint(3, 12)
    if L <= 0: raise ValueError
    if R.random() < 0.6:
        B.sa(6, lv(), f"In ⊙O, chords AB and CD are each {dist} units from O. AB = {lin_expr(a, b)} and CD = {lin_expr(c, d)}. Find x and AB.", f"x = {x}; AB = {L}", ["Chords equidistant from the center are congruent.", f"x = {x}."])
    else:
        h2 = F(L, 2); r2 = h2 * h2 + dist * dist
        B.orq(6, "honors", f"In ⊙O, chords AB = {lin_expr(a, b)} and CD = {lin_expr(c, d)} are each {dist} units from O.", [("Solve for x.", str(x)), ("Find AB.", str(L)), ("Find the radius.", rad(r2) if r2.denominator == 1 else f"√({fr(r2)})"), ("Is CD equidistant for a reason or by chance?", "Congruent chords are equidistant from the center (and conversely)")], ["Set the chords equal.", "Substitute.", f"r² = ({fr(h2)})² + {dist}².", "Theorem and converse."], tags=["challenge"])
def mk_chord_bis():
    x = R.randint(2, 10); a, c = R.randint(2, 6), R.randint(1, 5)
    if a == c: raise ValueError
    b = R.randint(-5, 8); L = a * x + b; d = L - c * x; m = R.randrange(30, 150, 2)
    if L <= 0: raise ValueError
    B.orq(6, lv(), f"Diameter CD of ⊙O is perpendicular to chord AB at M, with AM = {lin_expr(a, b)} and MB = {lin_expr(c, d)}. D lies on minor arc AB and m(arc AD) = {m}°.", [("Find x.", str(x)), ("Find AB.", str(2 * L)), ("Find m(arc DB).", f"{m}°"), ("Find m(arc AB).", f"{2 * m}°" if 2 * m < 360 else f"{2 * m}°")], ["A diameter ⟂ a chord bisects the chord.", "AB = 2·AM.", "It also bisects the arc.", "Arc AD + arc DB."])
def mk_chord_par():
    pairs = [(13, 5, 12), (25, 7, 24), (25, 15, 20), (17, 8, 15), (10, 6, 8), (5, 3, 4), (15, 9, 12), (26, 10, 24)]
    r, d1, d2 = R.choice(pairs); c1, c2 = 2 * int(math.isqrt(r * r - d1 * d1)), 2 * int(math.isqrt(r * r - d2 * d2))
    assert (c1 // 2) ** 2 + d1 * d1 == r * r and (c2 // 2) ** 2 + d2 * d2 == r * r
    same = R.random() < 0.5
    B.sa(6, "honors", f"A circle has radius {r}. Parallel chords of lengths {c1} and {c2} lie on {'the same side' if same else 'opposite sides'} of the center. Find the distance between the chords.", str(abs(d2 - d1) if same else d1 + d2), [f"Distances from the center: √({r}² − {c1 // 2}²) = {d1} and √({r}² − {c2 // 2}²) = {d2}.", "Same side: subtract; opposite sides: add."], tags=["challenge"])
def mk_chord_sel():
    r = R.randint(5, 15); d1, d2 = sorted(R.sample(range(1, r), 2))
    l1, l2 = rad(4 * (r * r - d1 * d1)), rad(4 * (r * r - d2 * d2))
    st = {f"The chord {d1} units from O is longer": True, f"The chord {d2} units from O has length {l2}": True, f"Both chords are shorter than {2 * r}": True, f"The chord {d2} units from O is longer": False, f"The chord {d1} units from O has length {rad(r * r - d1 * d1)}": False}
    B.sel(6, lv(), f"⊙O has radius {r}. One chord is {d1} units from O and another is {d2} units from O. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Half-chord = √(r² − d²); chord = 2√(r² − d²).", "Closer to the center ⇒ longer; every chord ≤ diameter."], tags=["concept"])

# =============== Skill 7: arc length and sector area ===============
def sector_fig(th, rl, shade=True):
    fg = Fig(3.6, 3.4); fg.circle((0, 0), 3); A_, B_ = cp(0), cp(th)
    if shade:
        t = [math.radians(v) for v in [i * th / 40 for i in range(41)]]
        fg.ax.fill([0] + [3 * math.cos(v) for v in t], [0] + [3 * math.sin(v) for v in t], color="#cccccc", alpha=0.6, lw=0)
    fg.seg((0, 0), A_); fg.seg((0, 0), B_); fg.dot((0, 0), "O", off=(-9, -8)); fg.dot(A_, "A", off=(10, 0)); fg.dot(B_, "B", off=(10 * math.cos(math.radians(th)), 10 * math.sin(math.radians(th))))
    fg.angle((0, 0), A_, B_, f"{th}°", r=0.6); fg.side((0, 0), A_, rl, center=(0, 2))
    return fg
def mk_arc_len():
    th = R.choice([30, 40, 45, 60, 72, 80, 90, 100, 120, 135, 150, 210, 225, 240, 270, 300]); r = R.randint(2, 18)
    L = F(th * r, 180); k = R.random()
    if k < 0.4:
        d_ = sector_fig(th, str(r), shade=False).save(B, nm("arc"), f"Circle O with radius {r} and central angle AOB = {th}°.")
        B.mc(7, lv(), "Find the length of arc AB (the arc inside the marked angle).", f"{pit(L)} ≈ {float(L) * math.pi:.2f}", [f"{pit(F(th * r * r, 360))} ≈ {float(F(th * r * r, 360)) * math.pi:.2f}", f"{pit(F(th * r, 360))} ≈ {float(F(th * r, 360)) * math.pi:.2f}", f"{pit(2 * r - L) if 2 * r != L else pit(L * 2)} ≈ {float(2 * r - L) * math.pi:.2f}"], ["Arc length = (θ/360)·2πr."], diagram=d_, tags=["diagram", "misconception"])
    elif k < 0.7:
        B.sa(7, lv(), f"An arc has length {pit(L)} in a circle of radius {r}. Find the arc's measure.", f"{th}°", [f"{pit(L)} = (θ/360)·2π({r}).", f"θ = {th}°."])
    else:
        B.sa(7, lv(), f"A {th}° arc has length {pit(L)}. Find the radius of the circle.", str(r), [f"(θ/360)·2πr = {pit(L)} → r = {r}."])
def mk_sector():
    th = R.choice([30, 36, 45, 60, 72, 90, 120, 135, 144, 150, 180, 240, 270]); r = R.randint(2, 15)
    A_ = F(th * r * r, 360); L = F(th * r, 180)
    if R.random() < 0.6:
        d_ = sector_fig(th, str(r)).save(B, nm("sector"), f"Shaded sector AOB of a circle with radius {r} and central angle {th}°.")
        B.orq(7, lv(), "Use the shaded sector.", [("What fraction of the circle is shaded?", fr(F(th, 360))), ("Find the area of the sector.", f"{pit(A_)} ≈ {float(A_) * math.pi:.2f}"), ("Find the arc length AB.", f"{pit(L)} ≈ {float(L) * math.pi:.2f}"), ("Find the perimeter of the sector.", f"{2 * r} + {pit(L)} ≈ {2 * r + float(L) * math.pi:.2f}")], ["θ/360.", "(θ/360)·πr².", "(θ/360)·2πr.", "Two radii plus the arc."], diagram=d_, tags=["diagram"])
    else:
        B.sa(7, lv(), f"A sector of a circle with radius {r} has area {pit(A_)}. Find its central angle.", f"{th}°", [f"(θ/360)·π·{r}² = {pit(A_)}.", f"θ = {th}°."])
def mk_seg_area():
    th = R.choice([60, 90, 120]); r = R.choice([2, 4, 6, 8, 10, 12]); sec = F(th * r * r, 360)
    if th == 90: tri = F(r * r, 2); ex = f"{pit(sec)} − {fr(tri)}"; val = float(sec) * math.pi - float(tri)
    else: tri = F(r * r, 4); ex = f"{pit(sec)} − {rad(3, tri)}"; val = float(sec) * math.pi - float(tri) * math.sqrt(3)
    assert abs(val - (th / 360 * math.pi * r * r - 0.5 * r * r * math.sin(math.radians(th)))) < 1e-9
    B.orq(7, "honors", f"Chord AB cuts off a circular segment in ⊙O, radius {r}, with central angle ∠AOB = {th}°.", [("Find the sector area.", pit(sec)), ("Find the area of △AOB.", fr(tri) if th == 90 else rad(3, tri)), ("Find the exact area of the segment.", ex), ("Approximate it.", f"{val:.2f}")], ["(θ/360)πr².", "½r²·sin θ (or base × height ÷ 2).", "Sector − triangle.", "Calculator."], tags=["challenge"])
def mk_radian():
    th = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300, 315, 330]); v = F(th, 180)
    if R.random() < 0.5:
        B.mc(7, "honors", f"Convert {th}° to radians.", pit(v), [pit(F(th, 360)), pit(F(180, th)) if th != 180 else "2π", f"{th}π"], ["Multiply by π/180."], tags=["challenge"])
    else:
        r = R.randint(2, 12)
        B.sa(7, "honors", f"A central angle of {pit(v)} radians cuts an arc in a circle of radius {r}. Find the arc length.", pit(v * r), ["s = rθ (θ in radians)."], tags=["challenge"])
def mk_prop_sel():
    th, r = R.choice([30, 45, 60, 90, 120]), R.randint(3, 10)
    st = {"Doubling the radius doubles the arc length": True, "Doubling the radius doubles the sector area": False, "Doubling the central angle doubles the sector area": True, f"The arc length equals {pit(F(th * r, 180))}": True, f"The sector area equals {pit(F(th * r, 180))}": False, f"The sector area equals {pit(F(th * r * r, 360))}": True}
    B.sel(7, lv(), f"A sector has radius {r} and central angle {th}°. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Arc length is proportional to r and θ; area is proportional to r² and θ."], tags=["concept"])

# =============== Skill 8: segment relationships ===============
def seg_fig(kind, lab):
    fg = Fig(4.2, 3.4); fg.circle((0, 0), 3)
    if kind == "chords":
        P_ = [cp(t) for t in (150, 40, -40, 215)]; E = inter(P_[0], P_[2], P_[1], P_[3]); fg.seg(P_[0], P_[2]); fg.seg(P_[1], P_[3])
        for p, n_ in zip(P_, "ABCD"): fg.dot(p, n_, off=(11 * p[0] / 3, 11 * p[1] / 3))
        fg.dot(E, "E", off=(0, -11))
        for (X, Y), l in zip(((P_[0], E), (E, P_[2]), (P_[1], E), (E, P_[3])), lab): fg.side(X, Y, l, dist=9)
        alt = f"Chords AC and BD meet at E; AE = {lab[0]}, EC = {lab[1]}, BE = {lab[2]}, ED = {lab[3]}."
    elif kind == "secants":
        P_ = (5.6, 0.0); B1, B2 = cp(135), cp(-140); L1, L2 = near_pt(P_, B1), near_pt(P_, B2); fg.seg(P_, B1); fg.seg(P_, B2)
        for p, n_ in ((L1, "A"), (B1, "B"), (L2, "C"), (B2, "D"), (P_, "P")): fg.dot(p, n_, off=(10 * p[0] / math.hypot(*p), 10 * p[1] / math.hypot(*p)))
        fg.side(P_, L1, lab[0], center=(0, 0)); fg.side(L1, B1, lab[1], center=(0, -3)); fg.side(P_, L2, lab[2], center=(0, 0)); fg.side(L2, B2, lab[3], center=(0, 3))
        alt = f"Secants PAB and PCD from external point P; PA = {lab[0]}, AB = {lab[1]}, PC = {lab[2]}, CD = {lab[3]}."
    else:
        P_ = (6.0, 0.0); T = cp(math.degrees(math.acos(0.5))); B1 = cp(-160); L1 = near_pt(P_, B1)
        fg.seg(P_, T); fg.seg(P_, B1)
        for p, n_ in ((T, "T"), (L1, "A"), (B1, "B"), (P_, "P")): fg.dot(p, n_, off=(10 * p[0] / math.hypot(*p), 10 * p[1] / math.hypot(*p)))
        fg.side(P_, T, lab[0]); fg.side(P_, L1, lab[1], dist=-10); fg.side(L1, B1, lab[2], dist=-10)
        alt = f"Tangent PT and secant PAB from external point P; PT = {lab[0]}, PA = {lab[1]}, AB = {lab[2]}."
    return fg.save(B, nm("segs"), alt, schematic=True)
def mk_chord_seg():
    k = R.random()
    if k < 0.5:
        a, b = R.randint(2, 12), R.randint(2, 12); prod = a * b; divs = [d for d in range(2, prod) if prod % d == 0 and d not in (a, b)]
        if not divs: raise ValueError
        c = R.choice(divs); d = prod // c
        d_ = seg_fig("chords", [str(a), str(b), str(c), "x"])
        B.mc(8, lv(), "Find x.", str(d), [fr(F(a * c, b)) if b else "0", str(a + b - c), fr(F(b * c, a))], ["Intersecting chords: AE·EC = BE·ED.", f"{a}·{b} = {c}x → x = {d}."], diagram=d_, tags=["diagram", "misconception"])
    else:
        x = R.randint(2, 9); k_ = R.randint(1, 8); prod = x * (x + k_); divs = [d for d in range(2, prod) if prod % d == 0]
        c = R.choice(divs); d = prod // c
        if c == d: raise ValueError
        roots = [r_ for r_ in range(-30, 31) if r_ * (r_ + k_) == prod]; assert x in roots and len([r_ for r_ in roots if r_ > 0]) == 1
        d_ = seg_fig("chords", ["x", f"x + {k_}", str(c), str(d)])
        B.orq(8, lv(), "Chords AC and BD intersect at E.", [("Write an equation.", f"x(x + {k_}) = {c}·{d}"), ("Write it in standard form.", f"x² + {k_}x − {prod} = 0"), ("Solve for x.", f"x = {x} (reject {-x - k_})"), ("Find AC.", str(2 * x + k_))], ["Product of chord parts.", "Expand.", "Factor; lengths are positive.", "AE + EC."], diagram=d_, tags=["diagram"])
def mk_sec_seg():
    a, b = R.randint(2, 10), R.randint(2, 12); prod = a * (a + b)
    opts = [(c, prod // c - c) for c in range(2, prod) if prod % c == 0 and prod // c - c > 0 and c != a]
    if not opts: raise ValueError
    c, x = R.choice(opts); assert c * (c + x) == a * (a + b)
    d_ = seg_fig("secants", [str(a), str(b), str(c), "x"])
    if R.random() < 0.55:
        B.mc(8, lv(), "Find x.", str(x), [fr(F(a * b, c)), str(prod // c), str(a + b - c)], ["Secant–secant: PA·PB = PC·PD (outside part × whole).", f"{a}({a + b}) = {c}({c} + x) → x = {x}."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(8, lv(), "Two secants are drawn from P.", [("Find PB.", str(a + b)), ("Write the equation.", f"{a}·{a + b} = {c}({c} + x)"), ("Solve for x.", str(x)), ("Find PD.", str(c + x))], ["PA + AB.", "Outside × whole.", "Divide and subtract.", "PC + CD."], diagram=d_, tags=["diagram"])
def mk_tan_sec():
    t = R.randint(4, 15); sq = t * t; opts = [(a, sq // a - a) for a in range(1, t) if sq % a == 0 and sq // a - a > 0]
    if not opts: raise ValueError
    a, b = R.choice(opts); assert t * t == a * (a + b)
    k = R.random()
    if k < 0.45:
        d_ = seg_fig("tansec", ["x", str(a), str(b)])
        B.sa(8, lv(), "PT is tangent at T. Find x.", str(t), [f"PT² = PA·PB = {a}·{a + b} = {sq}.", f"x = {t}."], diagram=d_, tags=["diagram"])
    elif k < 0.75:
        d_ = seg_fig("tansec", [str(t), str(a), "x"])
        B.mc(8, lv(), "PT is tangent at T. Find x.", str(b), [fr(F(t * t - a * a, 1)) if t * t - a * a != b else str(b + 1), fr(F(t, a)) if F(t, a) != b else str(b + 2), str(sq // a)], ["Tangent–secant: PT² = PA·PB.", f"{t}² = {a}({a} + x) → x = {b}."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.sa(8, "honors", f"From P, a tangent of length {t} and a secant are drawn. The secant's external segment is x and its internal segment is {b}. Find x.", str(a), [f"{t}² = x(x + {b}).", f"x² + {b}x − {sq} = 0 → x = {a} (positive root)."], tags=["challenge"])
        assert a * a + b * a - sq == 0
def mk_seg_sel():
    kind = R.choice(["chords", "secants", "tansec"])
    if kind == "chords":
        st = {"AE·EC = BE·ED": True, "AE/BE = ED/EC": True, "AE + EC = BE + ED": False, "AE·BE = EC·ED": False}
    elif kind == "secants":
        st = {"PA·PB = PC·PD": True, "PA·(PA + AB) = PC·(PC + CD)": True, "PA·AB = PC·CD": False, "PB/PD = PC/PA": True, "PA + AB = PC + CD": False}
    else:
        st = {"PT² = PA·PB": True, "PT = √(PA·PB)": True, "PT² = PA·AB": False, "PT = PA + AB": False}
    lab = {"chords": ["AE", "EC", "BE", "ED"], "secants": ["PA", "AB", "PC", "CD"], "tansec": ["PT", "PA", "AB"]}[kind]
    d_ = seg_fig(kind, [""] * len(lab))
    B.sel(8, lv(), "Select ALL relationships that are true for the figure.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Chords: part × part. Secants: outside × whole. Tangent: tangent² = outside × whole."], diagram=d_, tags=["diagram", "concept"])

# =============== Skill 9: equations of circles ===============
def sq_term(v, h):
    if h == 0: return f"{v}²"
    return f"({v} {'-' if h > 0 else '+'} {abs(h)})²"
def ceq(h, k, r2): return f"{sq_term('x', h)} + {sq_term('y', k)} = {fr(r2)}"
def geq(h, k, r2):
    D, E, Fc = -2 * h, -2 * k, h * h + k * k - r2; s = "x² + y²"
    for c, v in ((D, "x"), (E, "y")):
        if c: s += f" {'+' if c > 0 else '-'} {'' if abs(c) == 1 else abs(c)}{v}"
    if Fc: s += f" {'+' if Fc > 0 else '-'} {abs(Fc)}"
    return s + " = 0"
def rtxt(r2): return rad(r2)
def mk_eq_write():
    h, k = R.randint(-9, 9), R.randint(-9, 9); r = R.randint(1, 12)
    if R.random() < 0.5:
        B.sa(9, lv(), f"Write the equation of the circle with center {pt(h, k)} and radius {r}.", ceq(h, k, r * r), ["(x − h)² + (y − k)² = r²."])
    else:
        B.mc(9, lv(), f"Which is the equation of the circle with center {pt(h, k)} and radius {r}?", ceq(h, k, r * r), [ceq(-h, -k, r * r) if (h, k) != (0, 0) else ceq(1, 1, r * r), ceq(h, k, r), ceq(-h, -k, r) if (h, k) != (0, 0) else ceq(0, 0, 2 * r)], ["Signs in the equation are opposite to the center's coordinates; the right side is r²."], tags=["misconception"])
def mk_eq_read():
    h, k = R.randint(-9, 9), R.randint(-9, 9); r2 = R.randint(2, 80)
    B.sa(9, lv(), f"Find the center and radius of {ceq(h, k, r2)}.", f"center {pt(h, k)}, radius {rtxt(r2)}", ["Match (x − h)² + (y − k)² = r².", f"r = √{r2}."])
def mk_eq_general():
    h, k = R.randint(-8, 8), R.randint(-8, 8); r = R.randint(1, 10)
    if h == 0 and k == 0: raise ValueError
    g = geq(h, k, r * r)
    if R.random() < 0.6:
        B.orq(9, R.choice(["cp1", "honors"]), f"Write {g} in standard form.", [("Group x-terms and y-terms; move the constant.", f"(x² {'-' if h > 0 else '+'} {abs(2 * h)}x) + (y² {'-' if k > 0 else '+'} {abs(2 * k)}y) = {r * r - h * h - k * k}".replace("+ 0x", "").replace("- 0x", "").replace("+ 0y", "").replace("- 0y", "")), ("Complete both squares (add the same amounts to the right side).", f"add {h * h} and {k * k}"), ("Write the standard form.", ceq(h, k, r * r)), ("State the center and radius.", f"{pt(h, k)}, r = {r}")], ["Rearrange.", "(half the coefficient)².", "Factor perfect squares.", "Read h, k, r."], tags=["challenge"])
    else:
        B.mc(9, lv(), f"What are the center and radius of {g}?", f"{pt(h, k)}, r = {r}", [f"{pt(-h, -k)}, r = {r}", f"{pt(h, k)}, r = {r * r}", f"{pt(2 * h, 2 * k)}, r = {r}"], ["Complete the square in x and y."], tags=["misconception"])
def mk_eq_point():
    h, k = R.randint(-6, 6), R.randint(-6, 6); dx, dy = R.randint(-8, 8), R.randint(-8, 8)
    if dx == 0 and dy == 0: raise ValueError
    r2 = dx * dx + dy * dy
    if R.random() < 0.5:
        B.sa(9, lv(), f"A circle has center {pt(h, k)} and passes through {pt(h + dx, k + dy)}. Write its equation.", ceq(h, k, r2), [f"r² = {dx}² + {dy}² = {r2}."])
    else:
        if dx % 2 or dy % 2: raise ValueError
        A_, B_ = (h - dx // 2, k - dy // 2), (h + dx // 2, k + dy // 2); r2b = F(r2, 4)
        B.orq(9, lv(), f"A diameter of a circle has endpoints {pt(*A_)} and {pt(*B_)}.", [("Find the center.", pt(h, k)), ("Find the radius.", rtxt(r2b) if r2b.denominator == 1 else fr(r2b)), ("Write the equation.", ceq(h, k, r2b)), (f"Does the circle pass through {pt(h + dy // 2, k - dx // 2)}?", "Yes")], ["Midpoint.", "Half the diameter (distance formula).", "Standard form.", f"({fr(F(dy, 2))})² + ({fr(F(-dx, 2))})² = {fr(r2b)}."])
def mk_eq_pos():
    h, k = R.randint(-4, 4), R.randint(-4, 4); r = R.choice([5, 10, 13]); pts = []
    trip = {5: [(3, 4), (0, 5), (4, 3)], 10: [(6, 8), (8, 6), (0, 10)], 13: [(5, 12), (12, 5), (0, 13)]}[r]
    on = R.choice(trip); sg = (R.choice([-1, 1]), R.choice([-1, 1]))
    P_on = (h + sg[0] * on[0], k + sg[1] * on[1]); P_in = (h + R.randint(-2, 2), k + R.randint(1, 3)); P_out = (h + r, k + R.randint(1, 4)); P_on2 = (h - r, k)
    st = {f"{pt(*P_on)} lies on the circle": True, f"{pt(*P_on2)} lies on the circle": True, f"{pt(*P_in)} lies inside the circle": True, f"{pt(*P_out)} lies on the circle": False, f"{pt(*P_in)} lies outside the circle": False}
    for s_, v in st.items():
        p = eval(s_.split(" lies")[0].replace("(", "(").replace(")", ")")); d2 = (p[0] - h) ** 2 + (p[1] - k) ** 2
        tru = (d2 == r * r) if "on the" in s_ else (d2 < r * r) if "inside" in s_ else (d2 > r * r)
        assert tru == v, s_
    B.sel(9, lv(), f"For the circle {ceq(h, k, r * r)}, select ALL true statements.", [k_ for k_, v in st.items() if v], [k_ for k_, v in st.items() if not v], ["Compare (x − h)² + (y − k)² with r²: equal → on, less → inside, greater → outside."], tags=["reasoning"])
def mk_eq_graph():
    h, k = R.randint(-4, 4), R.randint(-4, 4); r = R.randint(1, 4)
    m = max(abs(h) + r, abs(k) + r) + 1
    d_ = graph(B, nm("eqg"), [(("param", lambda t: h + r * np.cos(t), lambda t: k + r * np.sin(t), (0, 2 * math.pi)), {})], xr=(-m, m), yr=(-m, m), points=[(h, k, True, "C")], alt=f"Circle on a coordinate grid with center C{pt(h, k)} and radius {r}.")
    tp = (h + r, k)
    B.orq(9, lv(), "Use the graph of the circle.", [("Find the center.", pt(h, k)), ("Find the radius.", str(r)), ("Write the equation.", ceq(h, k, r * r)), ("Name the rightmost point of the circle.", pt(*tp))], ["Read the center.", "Count to the edge.", "Standard form.", "Center + (r, 0)."], diagram=d_, tags=["graph"])
def mk_eq_tan():
    a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)]); sx, sy = R.choice([-1, 1]), R.choice([-1, 1])
    if R.random() < 0.5: a, b = b, a
    h, k = R.randint(-4, 4), R.randint(-4, 4); P_ = (h + sx * a, k + sy * b); mr = F(sy * b, sx * a); mt = -1 / mr
    bint = P_[1] - mt * P_[0]
    assert mt * mr == -1
    B.orq(9, "honors", f"Point P{pt(*P_)} lies on the circle {ceq(h, k, c * c)}.", [("Verify P is on the circle.", f"{sx * a}² + {sy * b}² = {c * c}"), ("Find the slope of radius CP.", fr(mr)), ("Find the slope of the tangent line at P.", fr(mt)), ("Write the tangent line in slope-intercept form.", f"y = {fr(mt)}x {'+' if bint >= 0 else '−'} {fr(abs(bint))}")], ["Substitute.", "Rise over run from the center.", "Tangent ⟂ radius: negative reciprocal.", "Point-slope, then simplify."], tags=["challenge"])
def mk_eq_trans():
    h, k = R.randint(-5, 5), R.randint(-5, 5); r = R.randint(1, 9); a, b = R.randint(-6, 6), R.randint(-6, 6)
    if a == 0 and b == 0: raise ValueError
    s_ = R.choice([2, 3, F(1, 2)]) if R.random() < 0.4 else 1
    if s_ == 1:
        B.mc(9, lv(), f"The circle {ceq(h, k, r * r)} is translated {abs(a)} units {'right' if a > 0 else 'left'} and {abs(b)} units {'up' if b > 0 else 'down'}. Which is the image's equation?", ceq(h + a, k + b, r * r), [ceq(h - a, k - b, r * r), ceq(h + a, k + b, (r + 1) ** 2), ceq(h + b, k + a, r * r) if a != b else ceq(h, k, r * r)], ["Move the center; the radius is unchanged."])
    else:
        r2 = (s_ * r) ** 2
        B.sa(9, "honors", f"The circle {ceq(h, k, r * r)} is dilated by scale factor {fr(s_)} about its center. Write the image's equation and explain why all circles are similar.", f"{ceq(h, k, r2)}; any circle maps to any other by a translation (centers) and a dilation by the ratio of radii", ["The center is fixed; the radius is multiplied by the scale factor.", "Translation + dilation."], tags=["reasoning"])

import numpy as np
makers = {1: [mk_parts, mk_parts, mk_rd_alg, mk_circ_sel, mk_arc_name, mk_arc_class],
          2: [mk_central_fig, mk_central_fig, mk_central_alg, mk_arc_sel, mk_arc_app],
          3: [mk_insc, mk_insc, mk_insc_alg, mk_semi, mk_cyclic, mk_insc_sel],
          4: [mk_chords_in, mk_secants, mk_sec_tan, mk_two_tan, mk_tan_chord, mk_ang_sel, mk_ang_sel2],
          5: [mk_tan_pyth, mk_tan_pyth, mk_tan_test, mk_tan_two, mk_tan_circ, mk_tan_sel],
          6: [mk_chord_dist, mk_chord_dist, mk_chord_cong, mk_chord_bis, mk_chord_par, mk_chord_sel],
          7: [mk_arc_len, mk_sector, mk_sector, mk_seg_area, mk_radian, mk_prop_sel],
          8: [mk_chord_seg, mk_sec_seg, mk_tan_sec, mk_seg_sel],
          9: [mk_eq_write, mk_eq_read, mk_eq_general, mk_eq_point, mk_eq_point, mk_eq_pos, mk_eq_graph, mk_eq_tan, mk_eq_trans]}
for S_, ms in makers.items():
    fill(B, S_, 32, ms, R)

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
