"""Precalculus Unit 7 — Vectors and complex numbers (vectors)."""
from hslib import *

UNIT_ID = "vectors"
ABBR = "vec"
I = sp.I
M_ = sp.Matrix


def cx(z):
    z = sp.nsimplify(sp.expand(z))
    a, b = sp.re(z), sp.im(z)
    if b == 0:
        return T(a)
    ab = abs(b)
    if ab == 1:
        it = "i"
    elif ab.is_Integer or (ab.is_Pow and ab.exp == sp.Rational(1, 2)) or (ab.is_Mul and ab.as_coeff_Mul()[0].is_Integer):
        it = f"{T(ab)}i"
    else:
        it = f"({T(ab)})i"
    if a == 0:
        return ("-" if b < 0 else "") + it
    return f"{T(a)} {'-' if b < 0 else '+'} {it}"


def rcx(r, lo=-8, hi=8):
    return rint(r, lo, hi) + rint(r, lo, hi, True) * I


def vt(v):
    return vec_text([sp.nsimplify(c) for c in v])


# ============================================================== S1 Complex operations
@fam("012")
def s1_ops(r, L):
    z, w = rcx(r, -6, 6), rcx(r, -6, 6)
    op = pick(r, ["+", "-", "·"] if L == 0 else ["·", "÷", "-"] if L == 1 else ["÷", "·", "^"])
    if op == "÷":
        need(sp.im(w) != 0)
        v = sp.nsimplify(sp.expand(sp.radsimp(z / w)))
        need(all(c.q in (1, 2, 4, 5, 10, 13, 17, 25, 26) for c in (sp.re(v), sp.im(v))) or L == 2)
        q = f"({cx(z)}) ÷ ({cx(w)})"
        w_ = [cx(sp.re(z) / sp.re(w) + sp.im(z) / sp.im(w) * I) if sp.re(w) else cx(z * sp.conjugate(w)), cx(z * sp.conjugate(w)), cx(sp.nsimplify(sp.expand(z * sp.conjugate(w)) / (sp.re(w) ** 2 - sp.im(w) ** 2))) if sp.re(w) ** 2 != sp.im(w) ** 2 else cx(-v)]
        why = ["Divided the parts separately", "Forgot to divide by |w|²", "Used a² - b² in the denominator"]
        steps = [f"Multiply numerator and denominator by the conjugate {cx(sp.conjugate(w))}.", f"Denominator: {sp.re(w) ** 2 + sp.im(w) ** 2}.", f"= {cx(v)}."]
        code = f"P('{cx(z)}')/P('{cx(w)}')"
    elif op == "^":
        n_ = rint(r, 2, 3)
        v = sp.expand(z ** n_)
        q = f"({cx(z)}){str(n_).translate(SUP)}"
        w_ = [cx(sp.re(z) ** n_ + sp.im(z) ** n_ * I), cx(sp.re(z) ** n_ - sp.im(z) ** n_), cx(sp.expand(sp.conjugate(z) ** n_))]
        why = ["Raised each part to the power", "Treated i² as 1 or dropped the cross terms", "Used the conjugate"]
        steps = [f"Expand: ({cx(z)}){str(n_).translate(SUP)} using i² = -1.", f"= {cx(v)}."]
        code = f"P('{cx(z)}')**{n_}"
    else:
        v = sp.expand(z + w if op == "+" else z - w if op == "-" else z * w)
        q = f"({cx(z)}) {op} ({cx(w)})"
        if op == "·":
            w_ = [cx(sp.re(z) * sp.re(w) + sp.im(z) * sp.im(w) * I), cx(sp.expand(z * w) + 2 * sp.im(z) * sp.im(w)), cx(sp.expand(z * sp.conjugate(w)))]
            why = ["Multiplied only the matching parts", "Used i² = 1", "Used the conjugate of the second number"]
        else:
            w_ = [cx(sp.expand(z - w if op == "+" else z + w)), cx(sp.re(z) - sp.re(w) + (sp.im(z) + sp.im(w)) * I) if op == "-" else cx(sp.expand(z + w) + 1), cx(sp.expand(w - z)) if op == "-" else cx(sp.re(z) + sp.re(w))]
            why = ["Used the wrong operation", "Distributed the subtraction to only one part" if op == "-" else "Made an arithmetic error", "Subtracted in the wrong order" if op == "-" else "Dropped the imaginary part"]
        steps = ["Combine real parts and imaginary parts." if op != "·" else "Use FOIL and i² = -1.", f"= {cx(v)}."]
        code = f"P('{cx(z)}') {'*' if op == '·' else op} P('{cx(w)}')"
    need(cx(v) not in w_ and len(set(w_)) == 3)
    return Q(f"Simplify {q}. Write the answer in the form a + bi.", cx(v), steps, w_, H(code), why=why)


@fam("012")
def s1_quad(r, L):
    p, q_ = rint(r, -6, 6), rint(r, 1, 6) if L < 2 else rint(r, 1, 9)
    a_ = 1 if L == 0 else pick(r, [1, 2, 4]) if L == 1 else pick(r, [1, 2, 3])
    need(p != 0)
    roots = [sp.Rational(p, 1) + q_ * I, sp.Rational(p, 1) - q_ * I] if L < 2 else [sp.Rational(p, 2) + sp.sqrt(q_) * I / 2, sp.Rational(p, 2) - sp.sqrt(q_) * I / 2]
    f = sp.expand(a_ * (x - roots[0]) * (x - roots[1]))
    need(all(c.is_Rational for c in sp.Poly(f, x).all_coeffs()))
    ans = f"x = {cx(roots[0])} or x = {cx(roots[1])}"
    return Q(f"Solve {T(f)} = 0. Give exact solutions.", ans, ["Use the quadratic formula.", f"The discriminant is {T(sp.discriminant(f, x))} < 0, so the solutions are complex conjugates.", ans + "."],
             [f"x = {cx(-roots[0])} or x = {cx(-roots[1])}", f"x = {T(sp.re(roots[0]) + sp.im(roots[0]))} or x = {T(sp.re(roots[0]) - sp.im(roots[0]))}", "no solution"],
             H(f"solve(P('{T(f)}').subs(x, Symbol('w')), Symbol('w'))", "set"), why=["Made a sign error with -b", "Treated √(negative) as real", "Stopped at a negative discriminant"])


# ============================================================== S2 Complex plane
@fam("012")
def s2_plane(r, L):
    z, w = rcx(r, -8, 8), rcx(r, -8, 8)
    kind = pick(r, ["modulus", "distance", "midpoint"])
    if kind == "modulus":
        a, b = pick(r, [(3, 4), (5, 12), (6, 8), (8, 15), (7, 24), (9, 12)]) if L == 0 else (rint(r, -9, 9, True), rint(r, -9, 9, True))
        a, b = a * pick(r, [1, -1]), b * pick(r, [1, -1])
        z = a + b * I
        v = sp.sqrt(a * a + b * b)
        return Q(f"Find |{cx(z)}|.", T(v), ["|a + bi| = √(a² + b²).", f"√({a * a} + {b * b}) = {T(v)}."], [T(abs(a) + abs(b)), str(a * a + b * b), T(sp.sqrt(abs(a * a - b * b))) if a * a != b * b else T(v + 1)],
                 H(f"Abs(P('{cx(z)}'))"), why=["Added the parts", "Forgot the square root", "Subtracted the squares"])
    if kind == "distance":
        v = sp.sqrt(sp.re(z - w) ** 2 + sp.im(z - w) ** 2)
        return Q(f"Find the distance between {cx(z)} and {cx(w)} in the complex plane.", T(v), ["Distance = |z - w|.", f"z - w = {cx(z - w)}.", f"|z - w| = {T(v)}."],
                 [T(sp.sqrt(sp.re(z + w) ** 2 + sp.im(z + w) ** 2)), T(abs(sp.re(z - w)) + abs(sp.im(z - w))), str(sp.re(z - w) ** 2 + sp.im(z - w) ** 2)], H(f"Abs(P('{cx(z)}') - P('{cx(w)}'))"),
                 why=["Added instead of subtracting", "Added the differences without the Pythagorean theorem", "Forgot the square root"])
    m = (z + w) / 2
    return Q(f"Find the midpoint of {cx(z)} and {cx(w)} in the complex plane.", cx(m), ["Midpoint = (z + w) ÷ 2.", f"z + w = {cx(z + w)}.", f"Midpoint = {cx(m)}."], [cx(z + w), cx((z - w) / 2), cx(sp.re(m) + sp.im(m) * I * 2)],
             H(f"(P('{cx(z)}') + P('{cx(w)}'))/2"), why=["Forgot to divide by 2", "Subtracted", "Did not halve the imaginary part"])


# ============================================================== S3 Geometric vectors
@fam("012")
def s3_points(r, L):
    A, B = (rint(r, -8, 8), rint(r, -8, 8)), (rint(r, -8, 8), rint(r, -8, 8))
    need(A != B)
    v = (B[0] - A[0], B[1] - A[1])
    kind = pick(r, ["comp", "mag"]) if L else "comp"
    if kind == "comp":
        return Q(f"Find the component form of the vector from P({A[0]}, {A[1]}) to Q({B[0]}, {B[1]}).", vt(v), ["Component form = terminal - initial.", f"⟨{B[0]} - {par(A[0])}, {B[1]} - {par(A[1])}⟩.", vt(v) + "."],
                 [vt((-v[0], -v[1])), vt((A[0] + B[0], A[1] + B[1])), vt((v[1], v[0])) if v[0] != v[1] else vt((v[0] + 1, v[1]))], H(f"[{B[0]} - ({A[0]}), {B[1]} - ({A[1]})]", "vector"),
                 why=["Subtracted in the wrong order", "Added the coordinates", "Switched the components"])
    m = sp.sqrt(v[0] ** 2 + v[1] ** 2)
    return Q(f"Find the magnitude of the vector from P({A[0]}, {A[1]}) to Q({B[0]}, {B[1]}). Give an exact answer.", T(m), [f"PQ = {vt(v)}.", f"|PQ| = √({v[0]}² + {v[1]}²) = {T(m)}."],
             [T(abs(v[0]) + abs(v[1])), str(v[0] ** 2 + v[1] ** 2), T(sp.sqrt((A[0] + B[0]) ** 2 + (A[1] + B[1]) ** 2))], H(f"sqrt(({B[0]} - ({A[0]}))**2 + ({B[1]} - ({A[1]}))**2)"),
             why=["Added the components", "Forgot the square root", "Added the coordinates"])


@fam("012")
def s3_resultant(r, L):
    a, b = rint(r, 3, 40), rint(r, 3, 40)
    m = math.hypot(a, b)
    return Q(f"A boat heads due east at {a} km/h while the current flows due north at {b} km/h. Find the boat's resultant speed, to the nearest tenth.", f"{Rd(m, 1)} km/h",
             ["The vectors are perpendicular.", f"|R| = √({a}² + {b}²).", f"≈ {Rd(m, 1)} km/h."], [f"{a + b} km/h", f"{Rd(math.sqrt(abs(a * a - b * b)), 1)} km/h", f"{a * a + b * b} km/h"], H(f"sqrt({a}**2 + {b}**2)", "round", places=1),
             why=["Added the speeds", "Subtracted the squares", "Forgot the square root"], tags=["modeling"])


# ============================================================== S4 Algebraic vectors
@fam("012")
def s4_combo(r, L):
    u, v = (rint(r, -8, 8), rint(r, -8, 8)), (rint(r, -8, 8), rint(r, -8, 8))
    a_, b_ = (1, 1) if L == 0 else (rint(r, -4, 4, True), rint(r, -4, 4, True))
    if L == 0:
        b_ = pick(r, [1, -1])
    R = (a_ * u[0] + b_ * v[0], a_ * u[1] + b_ * v[1])
    expr = f"{'' if a_ == 1 else '-' if a_ == -1 else a_}u {'+' if b_ > 0 else '-'} {'' if abs(b_) == 1 else abs(b_)}v"
    w = [vt((a_ * u[0] - b_ * v[0], a_ * u[1] - b_ * v[1])), vt((a_ * u[0] + b_ * v[0], a_ * u[1] - b_ * v[1])) if b_ * v[1] else vt((R[0] + 1, R[1])), vt((u[0] + v[0], u[1] + v[1])) if (a_, b_) != (1, 1) else vt((u[0] * v[0], u[1] * v[1]))]
    need(vt(R) not in w and len(set(w)) == 3)
    return Q(f"u = {vt(u)} and v = {vt(v)}. Find {expr}.", vt(R), ["Multiply each vector by its scalar.", "Combine components.", vt(R) + "."], w, H(f"[{a_}*{u[0]} + {b_}*({v[0]}), {a_}*{u[1]} + {b_}*({v[1]})]", "vector"),
             why=["Used the wrong sign", "Made a sign error in one component", "Ignored the scalars" if (a_, b_) != (1, 1) else "Multiplied components"])


@fam("012")
def s4_from_polar(r, L):
    m = rint(r, 2, 30)
    th = rint(r, 5, 355) if L else pick(r, [30, 45, 60, 120, 135, 150, 210, 225, 240, 300, 315, 330])
    if L == 0:
        c, s_ = sp.cos(th * sp.pi / 180), sp.sin(th * sp.pi / 180)
        ans = vt((m * c, m * s_))
        return Q(f"A vector has magnitude {m} and direction angle {th}°. Write it in exact component form.", ans, ["v = ⟨|v|cos θ, |v|sin θ⟩.", f"⟨{m}cos {th}°, {m}sin {th}°⟩.", ans + "."],
                 [vt((m * s_, m * c)), vt((m * abs(c), m * abs(s_))), vt((c, s_))], H(f"[{m}*cos({th}*pi/180), {m}*sin({th}*pi/180)]", "vector"), why=["Switched sine and cosine", "Ignored the quadrant signs", "Forgot the magnitude"])
    a, b = m * math.cos(math.radians(th)), m * math.sin(math.radians(th))
    ans = f"⟨{Rd(a, 2)}, {Rd(b, 2)}⟩"
    return Q(f"A vector has magnitude {m} and direction angle {th}°. Write it in component form, rounding to the nearest hundredth.", ans, ["v = ⟨|v|cos θ, |v|sin θ⟩.", ans + "."],
             [f"⟨{Rd(b, 2)}, {Rd(a, 2)}⟩", f"⟨{Rd(m * math.cos(th), 2)}, {Rd(m * math.sin(th), 2)}⟩", f"⟨{Rd(abs(a), 2)}, {Rd(abs(b), 2)}⟩" if (a < 0 or b < 0) else f"⟨{Rd(a / m, 2)}, {Rd(b / m, 2)}⟩"],
             PY("vec_round", m=m, th=th, places=2), why=["Switched sine and cosine", "Used radian mode", "Ignored the signs" if (a < 0 or b < 0) else "Forgot the magnitude"])


# ============================================================== S5 Magnitude and direction
@fam("012")
def s5_dir(r, L):
    a, b = rint(r, -12, 12, True), rint(r, -12, 12, True)
    m = sp.sqrt(a * a + b * b)
    th = math.degrees(math.atan2(b, a)) % 360
    kind = pick(r, ["mag", "dir"]) if L else "mag"
    if kind == "mag":
        return Q(f"Find the magnitude of v = ⟨{a}, {b}⟩. Give an exact answer.", T(m), ["|v| = √(a² + b²).", f"√({a * a} + {b * b}) = {T(m)}."], [T(abs(a) + abs(b)), str(a * a + b * b), T(sp.sqrt(abs(a * a - b * b))) if a * a != b * b else T(m * 2)],
                 H(f"sqrt(({a})**2 + ({b})**2)"), why=["Added the components", "Forgot the square root", "Subtracted the squares"])
    raw = math.degrees(math.atan(b / a))
    return Q(f"Find the direction angle of v = ⟨{a}, {b}⟩, measured counterclockwise from the positive x-axis (0° ≤ θ < 360°), to the nearest tenth of a degree.", f"{Rd(th, 1)}°",
             [f"tan⁻¹({b}/{a}) ≈ {Rd(raw, 1)}°." if False else f"tan⁻¹({b} ÷ {a}) ≈ {Rd(raw, 1)}°.", f"v is in quadrant {1 if a > 0 and b > 0 else 2 if a < 0 < b else 3 if a < 0 and b < 0 else 4}; adjust the angle.", f"θ ≈ {Rd(th, 1)}°."],
             [f"{Rd(raw, 1)}°" if Rd(raw, 1) != Rd(th, 1) else f"{Rd(90 - th, 1)}°", f"{Rd(math.degrees(math.atan2(a, b)) % 360, 1)}°", f"{Rd((th + 180) % 360, 1)}°"], H(f"Mod(atan2({b}, {a})*180/pi, 360)", "deg", places=1),
             why=["Did not adjust for the quadrant", "Inverted the ratio", "Added 180° unnecessarily"])


@fam("12")
def s5_unit(r, L):
    a, b = pick(r, [(3, 4), (5, 12), (6, 8), (8, 15), (1, 1), (2, 1), (1, 3)])
    a, b = a * pick(r, [1, -1]), b * pick(r, [1, -1])
    m = sp.sqrt(a * a + b * b)
    ans = vt((a / m, b / m))
    return Q(f"Find the unit vector in the direction of v = ⟨{a}, {b}⟩. Give exact components.", ans, [f"|v| = {T(m)}.", "u = v ÷ |v|.", ans + "."], [vt((a / (abs(a) + abs(b)), b / (abs(a) + abs(b)))), vt((a / m ** 2, b / m ** 2)), vt((b / m, a / m))],
             H(f"[{a}/sqrt({a * a + b * b}), {b}/sqrt({a * a + b * b})]", "vector"), why=["Divided by the sum of the components", "Divided by |v|²", "Switched the components"])


# ============================================================== S6 Applications
@fam("012")
def s6_wind(r, L):
    sp_ = rint(r, 150, 550)
    hd = pick(r, [0, 90, 180, 270]) if L == 0 else rint(r, 0, 359)
    w_ = rint(r, 15, 80)
    wd = pick(r, [d for d in (0, 90, 180, 270) if d % 180 != hd % 180]) if L == 0 else rint(r, 0, 359)
    # bearings: measured clockwise from north; convert to standard angles
    def vec(m, bearing):
        a_ = math.radians(90 - bearing)
        return (m * math.cos(a_), m * math.sin(a_))
    p, wv = vec(sp_, hd), vec(w_, wd)
    R = (p[0] + wv[0], p[1] + wv[1])
    gs = math.hypot(*R)
    br = (90 - math.degrees(math.atan2(R[1], R[0]))) % 360
    ask = "speed" if L == 0 else pick(r, ["speed", "bearing"])
    ctx = f"A plane flies with airspeed {sp_} mph on a heading (bearing) of {hd}°. The wind blows at {w_} mph toward a bearing of {wd}°. "
    if ask == "speed":
        return Q(ctx + "Find the plane's ground speed, to the nearest tenth of a mph.", f"{Rd(gs, 1)} mph", ["Write each as a vector (components from the bearing).", f"Resultant ≈ ⟨{Rd(R[0], 2)}, {Rd(R[1], 2)}⟩.", f"Ground speed ≈ {Rd(gs, 1)} mph."],
                 [f"{sp_ + w_} mph", f"{Rd(math.sqrt(sp_ * sp_ + w_ * w_), 1)} mph" if Rd(math.sqrt(sp_ * sp_ + w_ * w_), 1) != Rd(gs, 1) else f"{sp_ - w_} mph", f"{sp_ - w_} mph" if sp_ - w_ != round(gs, 1) else f"{sp_} mph"],
                 PY("wind", s=sp_, h=hd, w=w_, d=wd, ask="speed"), why=["Added the speeds", "Assumed the vectors are perpendicular", "Subtracted the speeds"], tags=["modeling"])
    return Q(ctx + "Find the plane's true course (bearing of the resultant), to the nearest tenth of a degree.", f"{Rd(br, 1)}°", ["Write each as a vector.", f"Resultant ≈ ⟨{Rd(R[0], 2)}, {Rd(R[1], 2)}⟩.", f"Bearing ≈ {Rd(br, 1)}°."],
             [f"{hd}°", f"{Rd(math.degrees(math.atan2(R[1], R[0])) % 360, 1)}°", f"{Rd((br + 180) % 360, 1)}°"], PY("wind", s=sp_, h=hd, w=w_, d=wd, ask="bearing"),
             why=["Ignored the wind", "Gave the standard-position angle instead of the bearing", "Reversed the direction"], tags=["modeling"])


@fam("012")
def s6_force(r, L):
    f1, f2 = rint(r, 10, 90), rint(r, 10, 90)
    ang = rint(r, 20, 160)
    m = math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * math.cos(math.radians(ang)))
    return Q(f"Two forces of {f1} N and {f2} N act on an object with an angle of {ang}° between them. Find the magnitude of the resultant force, to the nearest tenth.", f"{Rd(m, 1)} N",
             ["|R|² = |F₁|² + |F₂|² + 2|F₁||F₂|cos θ (θ = angle between the forces).", f"|R| ≈ {Rd(m, 1)} N."],
             [f"{Rd(math.sqrt(f1 * f1 + f2 * f2 - 2 * f1 * f2 * math.cos(math.radians(ang))), 1)} N", f"{f1 + f2} N", f"{Rd(math.hypot(f1, f2), 1)} N"], H(f"sqrt({f1}**2 + {f2}**2 + 2*{f1}*{f2}*cos({ang}*pi/180))", "round", places=1),
             why=["Used the Law of Cosines with the wrong angle (minus sign)", "Added the magnitudes", "Assumed the forces are perpendicular"], tags=["modeling"])


# ============================================================== S7 Vector transformations with matrices
@fam("012")
def s7_matvec(r, L):
    A = M_([[rint(r, -4, 4) for _ in range(2)] for _ in range(2)])
    v = M_([rint(r, -6, 6), rint(r, -6, 6)])
    need(any(A) and any(v))
    R = A * v
    if L == 2:
        th = pick(r, [30, 45, 60, 120, 135, 150])
        A = M_([[sp.cos(th * sp.pi / 180), -sp.sin(th * sp.pi / 180)], [sp.sin(th * sp.pi / 180), sp.cos(th * sp.pi / 180)]])
        R = sp.simplify(A * v)
        return Q(f"Rotate v = {vt(v)} by {th}° counterclockwise using the rotation matrix. Give exact components.", vt(R), [f"R = {mat_text(A)}.", "Multiply R·v.", vt(R) + "."],
                 [vt(sp.simplify(A.T * v)), vt(sp.simplify(M_([[A[0, 0], A[0, 1]], [A[1, 0], -A[1, 1]]]) * v)), vt((R[1], R[0]))], H(f"list(Matrix([[cos({th}*pi/180), -sin({th}*pi/180)], [sin({th}*pi/180), cos({th}*pi/180)]])*Matrix({v.tolist()}))", "vector"),
                 why=["Rotated clockwise (used the transpose)", "Made a sign error", "Switched the components"])
    w = [vt(A.T * v), vt((A[0, 0] * v[0], A[1, 1] * v[1])), vt((R[1], R[0])) if R[0] != R[1] else vt((R[0] + 1, R[1]))]
    need(vt(R) not in w and len(set(w)) == 3)
    return Q(f"Find Av for A = {mat_text(A)} and v = {vt(v)}.", vt(R), ["Each component is a row of A dotted with v.", f"⟨{A[0, 0]}({v[0]}) + {A[0, 1]}({v[1]}), {A[1, 0]}({v[0]}) + {A[1, 1]}({v[1]})⟩.", vt(R) + "."],
             w, H(f"list(Matrix({A.tolist()})*Matrix({v.tolist()}))", "vector"), why=["Used columns instead of rows", "Used only the diagonal", "Switched the components"])


# ============================================================== S8 Dot products and projections
@fam("012")
def s8_dot(r, L):
    u, v = (rint(r, -9, 9), rint(r, -9, 9)), (rint(r, -9, 9), rint(r, -9, 9))
    need(any(u) and any(v))
    d = u[0] * v[0] + u[1] * v[1]
    kind = "dot" if L == 0 else pick(r, ["dot", "angle", "orth"])
    if kind == "dot":
        return Q(f"Find u · v for u = {vt(u)} and v = {vt(v)}.", str(d), ["u · v = u₁v₁ + u₂v₂.", f"({u[0]})({v[0]}) + ({u[1]})({v[1]}) = {d}."], [vt((u[0] * v[0], u[1] * v[1])), str(u[0] * v[1] + u[1] * v[0]), str(u[0] * v[0] - u[1] * v[1])],
                 H(f"{u[0]}*({v[0]}) + {u[1]}*({v[1]})"), why=["Left the answer as a vector", "Cross-multiplied the components", "Subtracted the products"])
    if kind == "orth":
        ans = "Yes" if d == 0 else "No"
        if r.random() < 0.5:
            v = (-u[1] * pick(r, [1, 2, -1]), u[0] * 1)
            v = (v[0], u[0] * (v[0] // -u[1]) if u[1] and v[0] % u[1] == 0 else u[0])
            d = u[0] * v[0] + u[1] * v[1]
            ans = "Yes" if d == 0 else "No"
        return Q(f"Are u = {vt(u)} and v = {vt(v)} orthogonal?", ans, [f"u · v = {d}.", "Orthogonal exactly when u · v = 0.", ans + "."], ["No" if ans == "Yes" else "Yes"],
                 H(f"'Yes' if {u[0]}*({v[0]}) + {u[1]}*({v[1]}) == 0 else 'No'", "text"), mode="sa", why=["Did not compute the dot product"])
    th = math.degrees(math.acos(d / (math.hypot(*u) * math.hypot(*v))))
    return Q(f"Find the angle between u = {vt(u)} and v = {vt(v)}, to the nearest tenth of a degree.", f"{Rd(th, 1)}°", ["cos θ = (u · v) ÷ (|u||v|).", f"u · v = {d}; |u| = {T(sp.sqrt(u[0] ** 2 + u[1] ** 2))}, |v| = {T(sp.sqrt(v[0] ** 2 + v[1] ** 2))}.", f"θ ≈ {Rd(th, 1)}°."],
             [f"{Rd(180 - th, 1)}°", f"{Rd(math.radians(th), 1)}°", f"{Rd(math.degrees(math.acos(max(-1, min(1, d / (u[0] ** 2 + u[1] ** 2 + v[0] ** 2 + v[1] ** 2))))), 1)}°"],
             H(f"acos(({d})/(sqrt({u[0] ** 2 + u[1] ** 2})*sqrt({v[0] ** 2 + v[1] ** 2})))*180/pi", "deg", places=1), why=["Made a sign error in the dot product", "Gave radians", "Divided by the sum of squares"])


@fam("12")
def s8_proj(r, L):
    u, v = (rint(r, -8, 8), rint(r, -8, 8)), (rint(r, -6, 6), rint(r, -6, 6))
    need(any(v) and any(u))
    d = u[0] * v[0] + u[1] * v[1]
    vv = v[0] ** 2 + v[1] ** 2
    pr = (sp.Rational(d, vv) * v[0], sp.Rational(d, vv) * v[1])
    need(d != 0)
    return Q(f"Find proj_v u for u = {vt(u)} and v = {vt(v)}.", vt(pr), ["proj_v u = ((u · v) ÷ |v|²)v.", f"u · v = {d}; |v|² = {vv}.", vt(pr) + "."],
             [vt((sp.Rational(d, u[0] ** 2 + u[1] ** 2) * u[0], sp.Rational(d, u[0] ** 2 + u[1] ** 2) * u[1])), vt((d * v[0] / sp.sqrt(vv), d * v[1] / sp.sqrt(vv))), vt((sp.Rational(d, vv) * u[0], sp.Rational(d, vv) * u[1]))],
             H(f"[Rational({d}, {vv})*{v[0]}, Rational({d}, {vv})*{v[1]}]", "vector"), why=["Projected v onto u", "Divided by |v| instead of |v|²", "Scaled u instead of v"])


# ============================================================== S9 Polar and rectangular
@fam("012")
def s9_convert(r, L):
    to_rect = r.random() < 0.5
    if to_rect:
        rr = rint(r, 1, 10) if L < 2 else rint(r, -6, 6, True)
        th = pick(r, [sp.pi / 6, sp.pi / 4, sp.pi / 3, 2 * sp.pi / 3, 3 * sp.pi / 4, 5 * sp.pi / 6, 7 * sp.pi / 6, 5 * sp.pi / 4, 4 * sp.pi / 3, 5 * sp.pi / 3, 7 * sp.pi / 4, 11 * sp.pi / 6, sp.pi / 2, sp.pi])
        X_, Y_ = sp.radsimp(rr * sp.cos(th)), sp.radsimp(rr * sp.sin(th))
        ans = f"({T(X_)}, {T(Y_)})"
        return Q(f"Convert the polar point ({rr}, {T(th)}) to rectangular coordinates. Give exact values.", ans, ["x = r cos θ, y = r sin θ.", f"x = {T(X_)}, y = {T(Y_)}.", ans + "."],
                 [f"({T(Y_)}, {T(X_)})" if X_ != Y_ else f"({T(-X_)}, {T(Y_)})", f"({T(abs(X_))}, {T(abs(Y_))})" if (X_ < 0 or Y_ < 0) else f"({T(-X_)}, {T(-Y_)})", f"({T(sp.cos(th))}, {T(sp.sin(th))})" if rr != 1 else f"({T(X_ + 1)}, {T(Y_)})"],
                 H(f"[{rr}*cos(P('{T(th)}')), {rr}*sin(P('{T(th)}'))]", "point"), why=["Switched sine and cosine", "Ignored the quadrant signs", "Forgot to multiply by r"])
    a, b = pick(r, [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 2), (-3, 0), (2, 2), (-2, 2)]) if L == 0 else (rint(r, -6, 6), rint(r, -6, 6))
    need(a or b)
    rr = sp.sqrt(a * a + b * b)
    th = sp.atan2(b, a) % (2 * sp.pi)
    if L == 0 or th in [k_ * sp.pi / 12 for k_ in range(24)]:
        need(sp.nsimplify(th / sp.pi).q in (1, 2, 3, 4, 6))
        ans = f"({T(rr)}, {T(sp.nsimplify(th))})"
        return Q(f"Convert ({a}, {b}) to polar coordinates (r, θ) with r > 0 and 0 ≤ θ < 2π. Give exact values.", ans, ["r = √(x² + y²).", f"r = {T(rr)}; θ is in the correct quadrant: {T(th)}.", ans + "."],
                 [f"({T(rr)}, {T(sp.Mod(th + sp.pi, 2 * sp.pi))})", f"({abs(a) + abs(b)}, {T(th)})", f"({T(rr)}, {T(sp.Mod(sp.atan(sp.Rational(b, a)) if a else sp.pi / 2, 2 * sp.pi))})" if a and sp.Mod(sp.atan(sp.Rational(b, a)), 2 * sp.pi) != th else f"({T(rr)}, {T(sp.pi / 2 - th) if sp.pi / 2 - th >= 0 else T(sp.Mod(sp.pi / 2 - th, 2 * sp.pi))})"],
                 PY("polar_pt", x=a, y=b), why=["Placed θ in the opposite quadrant", "Added the coordinates for r", "Used tan⁻¹ without adjusting the quadrant"])
    thd = float(th)
    ans = f"({T(rr)}, {Rd(thd, 3)})"
    return Q(f"Convert ({a}, {b}) to polar coordinates (r, θ) with r > 0 and 0 ≤ θ < 2π. Give r exactly and θ in radians to the nearest thousandth.", ans,
             ["r = √(x² + y²).", f"θ = tan⁻¹({b} ÷ {a}) adjusted to the correct quadrant ≈ {Rd(thd, 3)}." if a else f"θ ≈ {Rd(thd, 3)}.", ans + "."],
             [f"({T(rr)}, {Rd((thd + math.pi) % (2 * math.pi), 3)})", f"({abs(a) + abs(b)}, {Rd(thd, 3)})", f"({T(rr)}, {Rd(math.degrees(thd), 3)})"], PY("polar_pt", x=a, y=b, places=3),
             why=["Placed θ in the opposite quadrant", "Added the coordinates for r", "Gave degrees instead of radians"])


@fam("12")
def s9_trigform(r, L):
    a, b = pick(r, [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, sp.sqrt(3)), (-1, sp.sqrt(3)), (sp.sqrt(3), 1), (sp.sqrt(3), -1), (0, 2), (-2, 0)])
    k_ = rint(r, 1, 4)
    a, b = a * k_, b * k_
    rr = sp.sqrt(a * a + b * b)
    th = sp.atan2(b, a) % (2 * sp.pi)
    ans = f"{T(rr)}(cos({T(th)}) + i·sin({T(th)}))".replace("1(cos", "(cos") if rr != 1 else f"cos({T(th)}) + i·sin({T(th)})"
    w1 = ans.replace(T(th), T(sp.Mod(th + sp.pi, 2 * sp.pi)))
    w2 = ans.replace(T(rr) + "(", T(rr ** 2) + "(", 1) if rr != 1 else "2" + ans
    w3 = ans.replace(f"cos({T(th)})", f"cos({T(sp.Mod(sp.pi / 2 - th, 2 * sp.pi))})").replace(f"sin({T(th)})", f"sin({T(sp.Mod(sp.pi / 2 - th, 2 * sp.pi))})")
    need(len({ans, w1, w2, w3}) == 4)
    return Q(f"Write {cx(a + b * I)} in trigonometric (polar) form r(cos θ + i·sin θ) with 0 ≤ θ < 2π.", ans, [f"r = |z| = {T(rr)}.", f"θ = {T(th)} (check the quadrant).", ans + "."], [w1, w2, w3],
             PY("trigform", z=cx(a + b * I)), why=["Used the wrong quadrant", "Used r² for the modulus", "Measured θ from the y-axis"])


@fam("012")
def s5_triple(r, L):
    """Magnitudes that come out to 5, 10, or 13 in three styles (short, medium, worded), so equal answers occur at every
    difficulty third of a skill: Partner Check pairs two different problems with the same answer."""
    a, b, c = pick(r, [(3, 4, 5), (6, 8, 10), (5, 12, 13)] if L < 2 else [(6, 8, 10), (5, 12, 13)])
    if r.random() < 0.5:
        a, b = b, a
    a, b = a * pick(r, [1, -1]), b * pick(r, [1, -1])
    style = pick(r, ["short", "medium", "long"] if L < 2 else ["medium", "long"])
    alts = [str(abs(a) + abs(b)), str(c * c), str(abs(abs(a) - abs(b)))]
    why = ["Added the components", "Forgot the square root", "Subtracted the components"]
    if style == "long":
        p0 = (rint(r, -6, 6), rint(r, -6, 6))
        q0 = (p0[0] + a, p0[1] + b)
        who = pick(r, ["A drone", "A robot", "A boat", "A hiker"])
        return Q(f"{who} moves straight from ({p0[0]}, {p0[1]}) to ({q0[0]}, {q0[1]}) on a grid in kilometers. Find the magnitude of its displacement vector.", str(c),
                 [f"Displacement = terminal - initial = ⟨{q0[0]} - {par(p0[0])}, {q0[1]} - {par(p0[1])}⟩.", f"= ⟨{a}, {b}⟩.", f"|v| = √({a}² + {b}²) = √({a * a} + {b * b}).", f"= √{c * c} = {c}.", f"The distance is {c} km."], alts,
                 H(f"sqrt(({q0[0]} - ({p0[0]}))**2 + ({q0[1]} - ({p0[1]}))**2)"), why=why, tags=["modeling"])
    if style == "medium":
        k_ = rint(r, 2, 3)
        return Q(f"Let u = ⟨{a * k_}, {b * k_}⟩ and v = (1/{k_})u. Find |v|.", str(c), [f"v = (1/{k_})⟨{a * k_}, {b * k_}⟩ = ⟨{a}, {b}⟩.", "|v| = √(a² + b²).", f"√({a * a} + {b * b}) = √{c * c}.", f"|v| = {c}."],
                 [str(c * k_), str(c * c), str(abs(a) + abs(b))], H(f"sqrt(({a * k_}/{k_})**2 + ({b * k_}/{k_})**2)"), why=["Forgot to scale by 1/k", "Forgot the square root", "Added the components"])
    return Q(f"Find the magnitude of v = ⟨{a}, {b}⟩.", str(c), ["|v| = √(a² + b²).", f"√({a * a} + {b * b}) = {c}."], alts, H(f"sqrt(({a})**2 + ({b})**2)"), why=why)


SKILLS = {
    1: dict(name="Complex Number Operations and Quadratic Zeros", std=["N-CN.A.2", "N-CN.C.7"], fams=[s1_ops, s1_quad], extra=[err_of(s1_ops), open_of(s1_ops)]),
    2: dict(name="Distance, Midpoints, and Modulus in the Complex Plane", std=["N-CN.B.4", "N-CN.B.6"], fams=[s2_plane], extra=[err_of(s2_plane), open_of(s2_plane)]),
    3: dict(name="Geometric Vectors", std=["N-VM.A.1", "N-VM.A.2"], fams=[s3_points, s3_resultant, reuse(s5_triple, (0, 1, 2), 'g'), reuse(s5_triple, (0, 1, 2), 'gx')], extra=[err_of(s3_points), open_of(s3_points)]),
    4: dict(name="Algebraic Vectors and Components", std=["N-VM.B.4", "N-VM.B.5"], fams=[s4_combo, s4_from_polar], extra=[err_of(s4_combo), open_of(s4_combo)]),
    5: dict(name="Vector Magnitude and Direction", std=["N-VM.A.1", "N-VM.B.4b"], fams=[s5_dir, s5_unit, s5_triple, reuse(s5_triple, (0, 1, 2), 'x')], extra=[err_of(s5_dir), open_of(s5_dir)]),
    6: dict(name="Vector Applications in Geometry and Modeling", std=["N-VM.A.3"], fams=[s6_wind, s6_force], extra=[err_of(s6_force), open_of(s6_force)]),
    7: dict(name="Vector Transformations Using Matrices", std=["N-VM.C.11"], fams=[s7_matvec], extra=[err_of(s7_matvec), open_of(s7_matvec)]),
    8: dict(name="Dot Products and Projections", std=["N-VM.B.4", "N-VM.A.3"], fams=[s8_dot, s8_proj, reuse(s5_triple, (0, 1, 2), 'd')], extra=[err_of(s8_dot), open_of(s8_dot)]),
    9: dict(name="Polar and Rectangular Coordinates", std=["N-CN.B.4"], fams=[s9_convert, s9_trigform], extra=[err_of(s9_convert), open_of(s9_convert)]),
}
