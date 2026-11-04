"""Precalculus Unit 5 — General Triangle Trigonometry (general-triangle-trigonometry)."""
from hslib import *

UNIT_ID = "general-triangle-trigonometry"
ABBR = "gtt"

pi = sp.pi


def rad(d):
    return d * math.pi / 180


def tri_ok(A, B):
    return 15 <= A <= 140 and 15 <= B <= 140 and A + B <= 160


def sides_from(A, B, c):
    C = 180 - A - B
    k_ = c / math.sin(rad(C))
    return k_ * math.sin(rad(A)), k_ * math.sin(rad(B)), C


# ============================================================== S1 Area and Law of Sines
@fam("012")
def s1_area(r, L):
    a, b = rint(r, 4, 30), rint(r, 4, 30)
    C = rint(r, 20, 150)
    v = 0.5 * a * b * math.sin(rad(C))
    if L == 2 and r.random() < 0.5:
        return Q(f"A triangle has area {Rd(v, 1)} cm². Two sides are {a} cm and {b} cm. Find the acute angle between them to the nearest degree.", f"{Rd(math.degrees(math.asin(min(1, 2 * float(Rd(v, 1)) / (a * b)))), 0)}°",
                 ["Area = (1/2)ab·sin C.", f"sin C = 2({Rd(v, 1)}) ÷ ({a} · {b}).", f"C ≈ {Rd(math.degrees(math.asin(min(1, 2 * float(Rd(v, 1)) / (a * b)))), 0)}°."],
                 [f"{Rd(math.degrees(math.asin(min(1, float(Rd(v, 1)) / (a * b)))), 0)}°", f"{Rd(180 - math.degrees(math.asin(min(1, 2 * float(Rd(v, 1)) / (a * b)))), 0)}°", f"{Rd(math.degrees(math.acos(min(1, 2 * float(Rd(v, 1)) / (a * b)))), 0)}°"],
                 H(f"asin(2*{Rd(v, 1)}/({a}*{b}))*180/pi", "deg", places=0), why=["Forgot the factor 1/2", "Gave the obtuse angle", "Used inverse cosine"], tags=["modeling"])
    need(C != 90)
    return Q(f"Find the area of a triangle with sides {a} cm and {b} cm and included angle {C}°. Round to the nearest tenth.", f"{Rd(v, 1)} cm²", ["Area = (1/2)ab·sin C.", f"(1/2)({a})({b})sin {C}°.", f"≈ {Rd(v, 1)} cm²."],
             [f"{Rd(a * b * math.sin(rad(C)), 1)} cm²", f"{Rd(0.5 * a * b * math.cos(rad(C)), 1) if math.cos(rad(C)) > 0 else Rd(0.5 * a * b, 1)} cm²", f"{Rd(0.5 * a * b * math.sin(C), 1) if 0.5 * a * b * math.sin(C) > 0 else Rd(0.5 * a * b * 0.9, 1)} cm²"],
             H(f"Rational(1, 2)*{a}*{b}*sin({C}*pi/180)", "round", places=1), why=["Forgot the 1/2", "Used cosine (or dropped the sine)", "Used radian mode on the calculator"],
             diagram={"alt": f"Triangle ABC with CA = {b} cm, CB = {a} cm, and angle C = {C}°.", "draw": obl_draw(math.sqrt(a * a + b * b - 2 * a * b * math.cos(rad(C))) if False else a, b, math.sqrt(a * a + b * b - 2 * a * b * math.cos(rad(C))), {"a": f"{a} cm", "b": f"{b} cm", "C": f"{C}°"})} if L == 0 else None)


@fam("012", mode="mc")
def s1_ratio(r, L):
    A, B = rint(r, 25, 100), rint(r, 25, 70)
    need(tri_ok(A, B))
    good = "a/sin A = b/sin B"
    opts = [(f"a/sin({A}°) = b/sin({B}°)", True), (f"a/sin({B}°) = b/sin({A}°)", False), (f"a/cos({A}°) = b/cos({B}°)", False), (f"a·sin({A}°) = b·sin({B}°)", False)]
    r.shuffle(opts)
    return Q(f"In triangle ABC, A = {A}° and B = {B}°. Which equation correctly relates sides a and b?", opts[[o[1] for o in opts].index(True)][0],
             ["The Law of Sines pairs each side with the sine of its opposite angle.", "a/sin A = b/sin B."], options=opts, chk=PY("los_rel", A=A, B=B), mode="mc")


# ============================================================== S2 Solving with the Law of Sines
@fam("012")
def s2_solve(r, L):
    A, B = rint(r, 20, 110), rint(r, 20, 80)
    need(tri_ok(A, B))
    a = rint(r, 5, 40)
    C = 180 - A - B
    ask = pick(r, ["b", "C"]) if L == 0 else pick(r, ["b", "c"])
    b = a * math.sin(rad(B)) / math.sin(rad(A))
    c = a * math.sin(rad(C)) / math.sin(rad(A))
    lab = {"A": f"{A}°", "B": f"{B}°", "a": str(a)}
    if ask == "C":
        return Q(f"In triangle ABC, A = {A}° and B = {B}°. Find angle C.", f"{C}°", ["The angles of a triangle sum to 180°.", f"C = 180° - {A}° - {B}° = {C}°."], [f"{180 - A}°", f"{90 - B}°" if B < 90 else f"{C + 10}°", f"{360 - A - B}°"],
                 H(f"(180 - {A} - {B})*pi/180"), why=["Subtracted only one angle", "Treated it as a right triangle", "Used 360°"])
    v = b if ask == "b" else c
    opp = B if ask == "b" else C
    return Q(f"In triangle ABC, A = {A}°, B = {B}°, and a = {a}. Find {ask} to the nearest tenth.", Rd(v, 1), ([f"C = 180° - {A}° - {B}° = {C}°."] if ask == "c" else []) + [f"{ask}/sin({opp}°) = {a}/sin({A}°).", f"{ask} = {a}·sin({opp}°)/sin({A}°)." if False else f"{ask} = {a}·sin({opp}°) ÷ sin({A}°).", f"{ask} ≈ {Rd(v, 1)}."],
             [Rd(a * math.sin(rad(A)) / math.sin(rad(opp)), 1), Rd(a * math.sin(rad(opp)) * math.sin(rad(A)), 1), Rd(a * math.sin(rad(180 - A - opp if ask == 'b' else B)) / math.sin(rad(A)), 1)],
             H(f"{a}*sin({opp}*pi/180)/sin({A}*pi/180)", "round", places=1), why=["Inverted the ratio", "Multiplied by sin A instead of dividing", "Used the wrong opposite angle"],
             diagram={"alt": f"Triangle ABC with angle A = {A}°, angle B = {B}°, and side a = {a}.", "draw": obl_draw(a, b, c, lab)} if L < 2 else None)


@fam("12")
def s2_angle(r, L):
    A = rint(r, 25, 80)
    a = rint(r, 10, 40)
    b = rint(r, 4, a - 1) if a > 5 else 3
    sB = b * math.sin(rad(A)) / a
    Bv = math.degrees(math.asin(sB))
    return Q(f"In triangle ABC, A = {A}°, a = {a}, and b = {b}. Find angle B to the nearest tenth of a degree. (Since b < a, there is exactly one triangle.)", f"{Rd(Bv, 1)}°",
             [f"sin B ÷ {b} = sin({A}°) ÷ {a}.", f"sin B = {b}·sin({A}°) ÷ {a} ≈ {Rd(sB, 4)}.", f"B ≈ {Rd(Bv, 1)}°."],
             [f"{Rd(math.degrees(math.asin(min(1, a * math.sin(rad(A)) / b))), 1) if a * math.sin(rad(A)) / b < 1 else Rd(Bv + 3, 1)}°", f"{Rd(180 - Bv, 1)}°", f"{Rd(math.asin(sB), 1)}°"],
             H(f"asin({b}*sin({A}*pi/180)/{a})*180/pi", "deg", places=1), why=["Inverted the ratio", "Gave the obtuse angle", "Left the answer in radians"])


# ============================================================== S3 Ambiguous case
@fam("012")
def s3_count(r, L):
    A = rint(r, 20, 120)
    b = rint(r, 6, 30)
    h_ = b * math.sin(rad(A))
    target = pick(r, [0, 1, 2]) if A < 90 else pick(r, [0, 1])
    if A >= 90:
        a = rint(r, max(1, b - 10), b) if target == 0 else rint(r, b + 1, b + 12)
    elif target == 0:
        a = rint(r, 1, max(1, math.floor(h_ - 0.01)))
    elif target == 2:
        need(math.floor(h_) + 1 < b)
        a = rint(r, math.floor(h_) + 1, b - 1)
    else:
        a = rint(r, b, b + 12)
    need(abs(a - h_) > 0.05)
    ans = str(target)
    return Q(f"How many triangles have A = {A}°, a = {a}, and b = {b}?", ans, [f"Height h = b·sin A = {b}·sin({A}°) ≈ {Rd(h_, 2)}." if A < 90 else f"A is obtuse, so a must be longer than b.",
                                                                        ("a < h: no triangle." if target == 0 else "h < a < b: two triangles." if target == 2 else "a ≥ b: one triangle.") if A < 90 else ("a ≤ b: no triangle." if target == 0 else "a > b: one triangle."), f"{ans} triangle{'s' if target != 1 else ''}."],
             [str(x_) for x_ in (0, 1, 2) if x_ != target] + ["infinitely many"], PY("ssa_count", A=A, a=a, b=b), why=["Compared a with b only", "Forgot the second (obtuse) possibility", "Thought SSA never determines a triangle"])


@fam("012")
def s3_two(r, L):
    A = rint(r, 20, 60)
    b = rint(r, 10, 30)
    h_ = b * math.sin(rad(A))
    need(math.floor(h_) + 1 < b)
    a = rint(r, math.floor(h_) + 1, b - 1)
    B1 = math.degrees(math.asin(b * math.sin(rad(A)) / a))
    B2 = 180 - B1
    need(A + B2 < 180 - 1)
    ans = f"B ≈ {Rd(B1, 1)}° or B ≈ {Rd(B2, 1)}°"
    return Q(f"Triangle ABC has A = {A}°, a = {a}, and b = {b}. Find both possible measures of angle B, to the nearest tenth of a degree.", ans,
             [f"sin B = {b}·sin({A}°) ÷ {a} ≈ {Rd(b * math.sin(rad(A)) / a, 4)}.", f"B₁ ≈ {Rd(B1, 1)}°.", f"B₂ = 180° - B₁ ≈ {Rd(B2, 1)}°; A + B₂ < 180°, so both work."],
             [f"B ≈ {Rd(B1, 1)}°", f"B ≈ {Rd(B1, 1)}° or B ≈ {Rd(90 + B1, 1)}°", f"B ≈ {Rd(B1, 1)}° or B ≈ {Rd(360 - B1, 1)}°"], PY("ssa_angles", A=A, a=a, b=b, places=1),
             why=["Missed the obtuse solution", "Added 90° instead of subtracting from 180°", "Subtracted from 360°"])


# ============================================================== S4 Law of Cosines
@fam("012")
def s4_side(r, L):
    a, b = rint(r, 4, 30), rint(r, 4, 30)
    C = rint(r, 20, 150)
    need(C != 90)
    c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(rad(C)))
    return Q(f"In triangle ABC, a = {a}, b = {b}, and C = {C}°. Find c to the nearest tenth.", Rd(c, 1), ["c² = a² + b² - 2ab·cos C.", f"c² = {a * a} + {b * b} - 2({a})({b})cos({C}°) ≈ {Rd(c * c, 2)}.", f"c ≈ {Rd(c, 1)}."],
             [Rd(math.sqrt(a * a + b * b + 2 * a * b * math.cos(rad(C))), 1), Rd(c * c, 1), Rd(math.sqrt(a * a + b * b), 1)], H(f"sqrt({a}**2 + {b}**2 - 2*{a}*{b}*cos({C}*pi/180))", "round", places=1),
             why=["Added 2ab·cos C", "Forgot the square root", "Ignored the angle (used the Pythagorean theorem)"],
             diagram={"alt": f"Triangle ABC with a = {a}, b = {b}, and angle C = {C}°.", "draw": obl_draw(a, b, c, {"a": str(a), "b": str(b), "C": f"{C}°", "c": "c"})} if L < 2 else None)


@fam("012")
def s4_angle(r, L):
    a, b, c = sorted(r.sample(range(4, 30), 3))
    need(a + b > c + 1)
    big = L >= 1 and r.random() < 0.6
    if big:
        Cv = math.degrees(math.acos((a * a + b * b - c * c) / (2 * a * b)))
        nm, s1_, s2_, op = "C", a, b, c
    else:
        Cv = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
        nm, s1_, s2_, op = "A", b, c, a
    return Q(f"A triangle has sides a = {a}, b = {b}, and c = {c}. Find angle {nm} to the nearest tenth of a degree.", f"{Rd(Cv, 1)}°",
             [f"cos {nm} = ({s1_}² + {s2_}² - {op}²) ÷ (2·{s1_}·{s2_}).", f"cos {nm} ≈ {Rd((s1_ ** 2 + s2_ ** 2 - op ** 2) / (2 * s1_ * s2_), 4)}.", f"{nm} ≈ {Rd(Cv, 1)}°."],
             [f"{Rd(math.degrees(math.acos(max(-1, min(1, (s1_ ** 2 + s2_ ** 2 + op ** 2) / (2 * s1_ * s2_))))) if abs((s1_ ** 2 + s2_ ** 2 + op ** 2) / (2 * s1_ * s2_)) <= 1 else Rd(180 - Cv, 1), 1) if False else Rd(180 - Cv, 1)}°", f"{Rd(math.acos((s1_ ** 2 + s2_ ** 2 - op ** 2) / (2 * s1_ * s2_)), 1)}°",
              f"{Rd(math.degrees(math.acos(max(-1, min(1, (s1_ ** 2 + op ** 2 - s2_ ** 2) / (2 * s1_ * op))))), 1)}°"], H(f"acos(Rational({s1_ ** 2 + s2_ ** 2 - op ** 2}, {2 * s1_ * s2_}))*180/pi", "deg", places=1),
             why=["Made a sign error (found the supplement)", "Left the answer in radians", "Used the wrong side as the opposite side"])


# ============================================================== S5 Heron's formula
@fam("012")
def s5_heron(r, L):
    if L == 0:
        a, b, c = pick(r, [(3, 4, 5), (5, 5, 6), (5, 5, 8), (6, 8, 10), (5, 12, 13), (13, 14, 15), (9, 10, 17), (7, 15, 20), (10, 13, 13), (8, 15, 17), (9, 12, 15), (11, 13, 20),
                           (13, 20, 21), (10, 10, 12), (4, 13, 15), (12, 16, 20), (7, 24, 25), (6, 25, 29), (10, 17, 21), (12, 17, 25), (15, 15, 18), (13, 13, 24), (16, 17, 17), (9, 15, 18) if False else (5, 29, 30)])
    else:
        a, b, c = sorted(r.sample(range(3, 25), 3))
    need(a + b > c)
    s_ = sp.Rational(a + b + c, 2)
    A2 = s_ * (s_ - a) * (s_ - b) * (s_ - c)
    v = math.sqrt(A2)
    exact = sp.sqrt(A2)
    if L == 0:
        need(exact.is_Rational)
    ans = T(exact) if exact.is_Rational else Rd(v, 1)
    return Q(f"Use Heron's formula to find the area of a triangle with sides {a}, {b}, and {c}." + ("" if exact.is_Rational else " Round to the nearest tenth."), ans + " units²",
             [f"s = ({a} + {b} + {c}) ÷ 2 = {T(s_) if s_.q == 1 else D(F(s_.p, s_.q))}.", "A = √(s(s - a)(s - b)(s - c)).", f"A ≈ {Rd(v, 1)} units²."],
             [(T(A2) if A2.is_Integer else Rd(float(A2), 1)) + " units²", Rd(math.sqrt(abs(float((a + b + c) * (a + b + c - a) * (a + b + c - b) * (a + b + c - c)))), 1) + " units²", Rd(v * 2, 1) + " units²"],
             H(f"(lambda s: sqrt(s*(s - {a})*(s - {b})*(s - {c})))(Rational({a + b + c}, 2))", "expr" if exact.is_Rational else "round", **({} if exact.is_Rational else {"places": 1})),
             why=["Forgot the square root", "Used the perimeter instead of the semiperimeter", "Doubled the area"])


@fam("012")
def s5_compare(r, L):
    a, b = rint(r, 5, 20), rint(r, 5, 20)
    C = rint(r, 30, 140)
    c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(rad(C)))
    v = 0.5 * a * b * math.sin(rad(C))
    return Q(f"A triangular plot has two sides of {a} m and {b} m with a {C}° angle between them. Find the length of the third side and the area. Round each to the nearest tenth.",
             f"side ≈ {Rd(c, 1)} m; area ≈ {Rd(v, 1)} m²", [f"Law of Cosines: c² = {a}² + {b}² - 2({a})({b})cos({C}°), so c ≈ {Rd(c, 1)} m.", f"Area = (1/2)({a})({b})sin({C}°) ≈ {Rd(v, 1)} m²."],
             [f"side ≈ {Rd(math.sqrt(a * a + b * b), 1)} m; area ≈ {Rd(v, 1)} m²", f"side ≈ {Rd(c, 1)} m; area ≈ {Rd(a * b * math.sin(rad(C)), 1)} m²", f"side ≈ {Rd(c * c, 1)} m; area ≈ {Rd(v, 1)} m²"],
             PY("side_area", a=a, b=b, C=C), why=["Used the Pythagorean theorem", "Forgot the 1/2 in the area", "Forgot the square root"], tags=["modeling"], mode="sa")


# ============================================================== S6 Deriving the laws
@fam("012", mode="mc")
def s6_derive(r, L):
    items = [("In triangle ABC, the altitude from C to side c has length h. Which expression equals h?", "b·sin A", ["b·cos A", "c·sin A", "a·sin A"]),
             ("Using the altitude h from C, b·sin A = h and a·sin B = h. Which equation follows?", "a/sin A = b/sin B", ["a·sin A = b·sin B", "a/sin B = b/sin A", "a + b = sin A + sin B"]),
             ("Place A at the origin and B at (c, 0). What are the coordinates of C?", "(b·cos A, b·sin A)", ["(a·cos A, a·sin A)", "(b·sin A, b·cos A)", "(c·cos A, c·sin A)"]),
             ("With C = (b·cos A, b·sin A) and B = (c, 0), the distance formula gives a² = (b·cos A - c)² + (b·sin A)². Which identity simplifies this?", "sin²A + cos²A = 1", ["sin A = cos(90° - A)", "tan A = sin A ÷ cos A", "sin(2A) = 2sin A cos A"]),
             ("Which equation is the Law of Cosines solved for cos C?", "cos C = (a² + b² - c²) ÷ (2ab)", ["cos C = (a² + b² + c²) ÷ (2ab)", "cos C = (c² - a² - b²) ÷ (2ab)", "cos C = (a² + b² - c²) ÷ (ab)"]),
             ("If C = 90°, the Law of Cosines c² = a² + b² - 2ab·cos C becomes which theorem?", "c² = a² + b²", ["c² = a² + b² - 2ab", "c² = a² - b²", "c = a + b"]),
             ("The triangle area formula (1/2)ab·sin C comes from Area = (1/2)(base)(height) with base a and height equal to:", "b·sin C", ["b·cos C", "a·sin C", "c·sin C"]),
             ("Why does the Law of Sines give two possible angles in the SSA case?", "sin θ = sin(180° - θ)", ["cos θ = cos(-θ)", "sin θ = cos(90° - θ)", "tan θ = tan(180° + θ)"])]
    i = r.randrange(len(items)) if L == 2 else r.randrange(6)
    qtxt, good, bad = items[i]
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    r.shuffle(opts)
    return Q(qtxt, good, [good + "."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


@fam("012")
def s6_height(r, L):
    b = rint(r, 5, 40)
    A = rint(r, 15, 80)
    hv = b * math.sin(rad(A))
    return Q(f"In triangle ABC, b = {b} and A = {A}°. Find the length of the altitude from C to side AB, to the nearest tenth.", Rd(hv, 1), ["The altitude forms a right triangle with hypotenuse b.", "h = b·sin A.", f"h ≈ {Rd(hv, 1)}."],
             [Rd(b * math.cos(rad(A)), 1), Rd(b / math.sin(rad(A)), 1), Rd(b * math.tan(rad(A)), 1)], H(f"{b}*sin({A}*pi/180)", "round", places=1), why=["Used cosine", "Divided by sin A", "Used tangent"])


# ============================================================== S7 Sum and difference identities
COMBOS = [(45, 30), (60, 45), (45, -30), (60, -45), (30, 45), (135, -30), (120, 45), (180, -45), (90, 45), (45, 90), (135, 60), (225, -60), (30, -45), (210, 45)]
EXT = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}


@fam("012")
def s7_exact(r, L):
    a_, b_ = pick(r, COMBOS)
    f = pick(r, ["sin", "cos"] if L == 0 else ["sin", "cos", "tan"])
    tot = a_ + b_
    need(tot % 90 != 0)
    v = sp.nsimplify(sp.radsimp(EXT[f](tot * pi / 180)))
    v = sp.radsimp(sp.expand(v))
    sgn = "+" if b_ > 0 else "-"
    steps = {"sin": f"sin(A {sgn} B) = sin A cos B {sgn} cos A sin B", "cos": f"cos(A {sgn} B) = cos A cos B {'-' if sgn == '+' else '+'} sin A sin B", "tan": f"tan(A {sgn} B) = (tan A {sgn} tan B) ÷ (1 {'-' if sgn == '+' else '+'} tan A tan B)"}[f]
    def tx(e):
        e = sp.radsimp(sp.expand(e))
        num, den = sp.fraction(sp.together(e))
        if den == 1:
            return T(e)
        nt = T(sp.expand(num))
        return (f"({nt})" if (" " in nt or "√" in nt) else nt) + f"/{den}"
    wsum = sp.radsimp(sp.expand(EXT[f](a_ * pi / 180) + EXT[f](b_ * pi / 180)))
    wsign = sp.radsimp(sp.expand(EXT[f](a_ * pi / 180 - abs(b_) * pi / 180 * (1 if b_ > 0 else -1)))) if f != "tan" or (a_ - b_) % 90 or (a_ - b_) % 180 == 0 else v + 1
    wneg = -v
    ws = [tx(w) for w in (wsum, wsign, wneg)]
    need(tx(v) not in ws and len(set(ws)) == 3)
    return Q(f"Use a sum or difference identity to find the exact value of {f}({tot}°) = {f}({a_}° {sgn} {abs(b_)}°).", tx(v), [steps + ".", f"Substitute exact values for {a_}° and {abs(b_)}°.", f"{f}({tot}°) = {tx(v)}."], ws,
             H(f"{f}({tot}*pi/180)"), why=["Added the function values (f(A + B) ≠ f(A) + f(B))", "Used the wrong sign in the identity", "Made a sign error"])


@fam("12")
def s7_given(r, L):
    (a1, b1, c1), (a2, b2, c2) = r.sample([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (4, 3, 5), (12, 5, 13)], 2)
    sa, ca = sp.Rational(a1, c1), sp.Rational(b1, c1)
    sb, cb = sp.Rational(a2, c2), sp.Rational(b2, c2)
    q2 = L == 2 and r.random() < 0.5
    if q2:
        ca = -ca
    f = pick(r, ["sin", "cos"])
    sgn = pick(r, ["+", "-"])
    s_ = 1 if sgn == "+" else -1
    v = sa * cb + s_ * ca * sb if f == "sin" else ca * cb - s_ * sa * sb
    return Q(f"sin α = {T(sa)} with α in quadrant {'II' if q2 else 'I'}, and cos β = {T(cb)} with β in quadrant I. Find {f}(α {sgn} β).", T(v),
             [f"cos α = {T(ca)}, sin β = {T(sb)} (Pythagorean identity and quadrant signs).", {"sin": f"sin(α {sgn} β) = sin α cos β {sgn} cos α sin β.", "cos": f"cos(α {sgn} β) = cos α cos β {'-' if sgn == '+' else '+'} sin α sin β."}[f], f"= {T(v)}."],
             [T(sa * cb - s_ * ca * sb) if f == "sin" else T(ca * cb + s_ * sa * sb), T(sa * cb + s_ * abs(ca) * sb) if (f == "sin" and q2) else T(-v), T(sa + cb) if f == "sin" else T(ca + cb)],
             H(f"{f}(asin(Rational({sa.p}, {sa.q})) if {0 if q2 else 1} else pi - asin(Rational({sa.p}, {sa.q})))".replace(")", ")", 1) if False else f"(lambda A, B: {f}(A {sgn} B))({'pi - ' if q2 else ''}asin(Rational({sa.p}, {sa.q})), acos(Rational({cb.p}, {cb.q})))"),
             why=["Used the wrong sign in the identity", "Ignored the quadrant sign" if q2 else "Made a sign error", "Added the given values"])


# ============================================================== S8 Rotations
@fam("012")
def s8_rotate(r, L):
    th = pick(r, [90, 180, 270, 45, 30, 60, 120, 135, -90, -45, 150]) if L else pick(r, [90, 270, -90, 45, 135, -270])
    px, py = rint(r, -6, 6), rint(r, -6, 6)
    need(px or py)
    t_ = th * pi / 180
    nx, ny = sp.radsimp(px * sp.cos(t_) - py * sp.sin(t_)), sp.radsimp(px * sp.sin(t_) + py * sp.cos(t_))
    ans = f"({T(nx)}, {T(ny)})"
    dirn = "counterclockwise" if th > 0 else "clockwise"
    w1 = f"({T(sp.radsimp(px * sp.cos(t_) + py * sp.sin(t_)))}, {T(sp.radsimp(-px * sp.sin(t_) + py * sp.cos(t_)))})"
    w2 = f"({T(sp.radsimp(px * sp.cos(t_) - py * sp.sin(t_)))}, {T(sp.radsimp(px * sp.sin(t_) - py * sp.cos(t_)))})"
    w3 = f"({T(ny)}, {T(nx)})"
    need(len({ans, w1, w2, w3}) == 4)
    return Q(f"Rotate the point ({px}, {py}) by {abs(th)}° {dirn} about the origin. Give exact coordinates.", ans,
             [f"Use x′ = x cos θ - y sin θ and y′ = x sin θ + y cos θ with θ = {th}°.", f"x′ = {T(nx)}, y′ = {T(ny)}.", ans + "."], [w1, w2, w3],
             H(f"(lambda c, s: [{px}*c - {py}*s, {px}*s + {py}*c])(cos({th}*pi/180), sin({th}*pi/180))", "point"), why=["Rotated in the opposite direction", "Made a sign error in y′", "Switched the coordinates"])


@fam("012")
def s8_matrix(r, L):
    th = pick(r, [90, 180, 270, 45, 30, 60, 120, 135, 150, 210, 300])
    t_ = th * pi / 180
    M = sp.Matrix([[sp.cos(t_), -sp.sin(t_)], [sp.sin(t_), sp.cos(t_)]])
    ans = mat_text(M)
    w = [mat_text(M.T), mat_text(sp.Matrix([[sp.sin(t_), -sp.cos(t_)], [sp.cos(t_), sp.sin(t_)]])), mat_text(sp.Matrix([[sp.cos(t_), sp.sin(t_)], [sp.sin(t_), sp.cos(t_)]]))]
    need(len({ans, *w}) == 4)
    return Q(f"Write the 2 × 2 matrix that rotates points {th}° counterclockwise about the origin. Give exact entries (rows separated by semicolons).", ans, ["R(θ) = [cos θ, -sin θ; sin θ, cos θ].", f"θ = {th}°.", ans + "."], w,
             H(f"Matrix([[cos({th}*pi/180), -sin({th}*pi/180)], [sin({th}*pi/180), cos({th}*pi/180)]])", "matrix"), why=["Used the clockwise matrix (transpose)", "Switched sine and cosine", "Dropped the negative sign"])


SKILLS = {
    1: dict(name="Triangle Area and the Law of Sines", std=["G-SRT.D.9", "G-SRT.D.10"], fams=[s1_area, s1_ratio], extra=[err_of(s1_area), open_of(s1_area)]),
    2: dict(name="Solving Triangles with the Law of Sines", std=["G-SRT.D.10", "G-SRT.D.11"], fams=[s2_solve, s2_angle], extra=[err_of(s2_solve), open_of(s2_solve)]),
    3: dict(name="The Ambiguous Case: Zero, One, or Two Triangles", std=["G-SRT.D.11"], fams=[s3_count, s3_two], extra=[err_of(s3_count), open_of(s3_count)]),
    4: dict(name="The Law of Cosines", std=["G-SRT.D.10", "G-SRT.D.11"], fams=[s4_side, s4_angle], extra=[err_of(s4_side), open_of(s4_side)]),
    5: dict(name="Triangle Area from Three Sides", std=["G-SRT.D.9"], fams=[s5_heron, s5_compare], extra=[err_of(s5_heron), open_of(s5_heron)]),
    6: dict(name="Deriving the Laws of Sines and Cosines", std=["G-SRT.D.10"], fams=[s6_derive, s6_height], extra=[err_of(s6_height), open_of(s6_height)]),
    7: dict(name="Sum and Difference Identities", std=["F-TF.C.9"], fams=[s7_exact, s7_given], extra=[err_of(s7_exact), open_of(s7_exact)]),
    8: dict(name="Rotations with Identities and Matrices", std=["F-TF.C.9", "N-VM.C.12"], fams=[s8_rotate, s8_matrix], extra=[err_of(s8_rotate), open_of(s8_rotate)]),
}
