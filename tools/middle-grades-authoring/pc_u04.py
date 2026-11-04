"""Precalculus Unit 4 — Trigonometric Functions (trigonometric-functions)."""
from hslib import *

UNIT_ID = "trigonometric-functions"
ABBR = "trg"

pi = sp.pi
SPECIAL = [sp.Rational(i, 12) * 2 * pi for i in range(12)] + [sp.Rational(i, 8) * 2 * pi for i in (1, 3, 5, 7)]
SPECIAL = sorted(set(SPECIAL), key=lambda a: float(a))
FN = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc, "cot": sp.cot}


def deg(a):
    return sp.nsimplify(a * 180 / pi)


def ang(a, degrees):
    return f"{T(deg(a))}°" if degrees else T(a)


def quad(a):
    a = float(a) % (2 * math.pi)
    for q_, (lo, hi) in enumerate([(0, math.pi / 2), (math.pi / 2, math.pi), (math.pi, 3 * math.pi / 2), (3 * math.pi / 2, 2 * math.pi)], 1):
        if lo < a < hi:
            return q_
    return 0


def ref(a):
    a = sp.Mod(a, 2 * pi)
    q_ = quad(a)
    return {1: a, 2: pi - a, 3: a - pi, 4: 2 * pi - a}.get(q_, a)


# ============================================================== S1 Unit circle
@fam("012")
def s1_point(r, L):
    a = pick(r, SPECIAL[1:])
    need(quad(a) or L == 0)
    if L == 2:
        a = a + pick(r, [-2, 2]) * pi
    degrees = L == 0 or (L == 1 and r.random() < 0.5)
    c_, s_ = sp.cos(a), sp.sin(a)
    ans = f"({T(c_)}, {T(s_)})"
    return Q(f"Find the coordinates of the point where the terminal side of θ = {ang(a, degrees)} intersects the unit circle.", ans,
             ["On the unit circle the point is (cos θ, sin θ).", f"Reference angle: {ang(ref(a), degrees)}; quadrant {quad(a) or 'none (axis)'}.", f"({T(c_)}, {T(s_)})."],
             [f"({T(s_)}, {T(c_)})" if s_ != c_ else f"({T(-c_)}, {T(s_)})", f"({T(abs(c_))}, {T(abs(s_))})" if (c_ < 0 or s_ < 0) else f"({T(-c_)}, {T(-s_)})", f"({T(-c_)}, {T(s_)})" if c_ else f"({T(c_)}, {T(-s_)})"],
             H(f"(lambda A: [cos(A), sin(A)])(P('{ang(a, degrees)}'))", "point"), why=["Switched sine and cosine", "Ignored the quadrant signs", "Used the wrong sign for one coordinate"])


@fam("012")
def s1_ref(r, L):
    a = pick(r, [v for v in SPECIAL if quad(v) in (2, 3, 4)])
    if L == 2:
        a = a + pick(r, [2, -2]) * pi
    degrees = L < 2 and r.random() < 0.6
    rf = ref(a)
    return Q(f"Find the reference angle for θ = {ang(a, degrees)}.", ang(rf, degrees), ["The reference angle is the acute angle between the terminal side and the x-axis.", f"θ is in quadrant {quad(a)}.", f"Reference angle: {ang(rf, degrees)}."],
             [ang(pi / 2 - rf, degrees), ang(sp.Mod(a, 2 * pi) - pi / 2, degrees) if sp.Mod(a, 2 * pi) - pi / 2 != rf else ang(rf + pi / 6, degrees), ang(pi - sp.Mod(a, 2 * pi), degrees) if pi - sp.Mod(a, 2 * pi) > 0 and pi - sp.Mod(a, 2 * pi) != rf else ang(2 * rf, degrees)],
             H(f"(lambda A: acos(Abs(cos(A))))(P('{ang(a, degrees)}'))", "expr"), why=["Measured to the y-axis", "Subtracted 90° (π/2)", "Subtracted from 180° (π) in the wrong quadrant"])


# ============================================================== S2 Exact values
@fam("012")
def s2_exact(r, L):
    fns = ["sin", "cos", "tan"] if L == 0 else ["sin", "cos", "tan", "sec", "csc", "cot"]
    f = pick(r, fns)
    a = pick(r, SPECIAL)
    if L == 2:
        a = a + pick(r, [-2, 2, 4]) * pi if r.random() < 0.6 else -a
    v = FN[f](a)
    need(v.is_finite and v not in (sp.zoo,))
    degrees = L == 0 or (L == 1 and r.random() < 0.5)
    rf = ref(a)
    alt = FN[{"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan", "sec": "csc", "csc": "sec"}[f]](a)
    w = [T(-v) if v else "1", T(alt) if alt.is_finite and alt != v else T(v + 1), T(1 / v) if v and 1 / v != v and 1 / v != -v else T(2 * v + 1)]
    return Q(f"Find the exact value of {f}({ang(a, degrees)}).", T(v), [f"Reference angle {ang(rf, degrees)}; quadrant {quad(a) or 'none (on an axis)'}.", f"{f}({ang(rf, degrees)}) = {T(abs(v))}; apply the quadrant sign.", f"{f}({ang(a, degrees)}) = {T(v)}."],
             w, H(f"{f}(P('{ang(a, degrees)}'))"), why=["Used the wrong sign for the quadrant", "Used the cofunction", "Used the reciprocal function"])


# ============================================================== S3 Radian measure
@fam("012")
def s3_convert(r, L):
    a = pick(r, SPECIAL[1:] + [sp.Rational(k_, 12) * pi for k_ in (13, 15, 17, 19, 21, 23)] + [sp.Rational(k_, 9) * pi for k_ in (1, 2, 4, 5, 7)])
    if L == 2:
        a = -a if r.random() < 0.5 else a + 2 * pi
    to_rad = r.random() < 0.5
    if to_rad:
        return Q(f"Convert {T(deg(a))}° to radians. Give an exact answer in terms of π.", T(a), ["Multiply by π/180.", f"{T(deg(a))} · π/180 = {T(a)}."], [T(deg(a) * 180 / pi) if False else T(deg(a) * pi / 360), T(sp.Rational(180, 1) / deg(a)) + "π" if deg(a) else "π", T(a / 2)],
                 H(f"P('{T(deg(a))}°')"), why=["Divided by 360 instead of 180", "Inverted the conversion factor", "Halved the angle"])
    return Q(f"Convert {T(a)} radians to degrees.", f"{T(deg(a))}°", ["Multiply by 180/π.", f"{T(a)} · 180/π = {T(deg(a))}°."], [f"{D(F(int((deg(a) / 2).p), int((deg(a) / 2).q)))}°", f"{T(deg(a) * 2)}°", f"{D(F(int((a / pi).p), int((a / pi).q))) if (a / pi).q in (1, 2, 4, 5, 10) else Rd(float(a / pi), 2)}°"],
             H(f"P('{T(a)}')"), why=["Multiplied by 90/π", "Multiplied by 360/π", "Dropped the π and kept the coefficient"])


@fam("012")
def s3_coterminal(r, L):
    degrees = L < 2
    if degrees:
        a = rint(r, -720, 1080)
        need(a % 360 != 0)
        v = a % 360
        return Q(f"Find the angle between 0° and 360° that is coterminal with {a}°.", f"{v}°", ["Add or subtract multiples of 360°.", f"{a}° {'-' if a > 360 else '+'} {abs((a - v) // 360)}(360°) = {v}°."],
                 [f"{(a + 180) % 360}°", f"{360 - v}°", f"{abs(a) % 180}°" if abs(a) % 180 != v else f"{(v + 90) % 360}°"], H(f"({a} - 360*floor(Rational({a}, 360)))*pi/180"),
                 why=["Added 180° instead of 360°", "Subtracted from 360°", "Used 180° multiples"])
    a = sp.Rational(rint(r, -30, 40, True), pick(r, [3, 4, 6])) * pi
    v = sp.Mod(a, 2 * pi)
    need(a != v and v != 0)
    return Q(f"Find the angle in [0, 2π) that is coterminal with {T(a)}.", T(v), ["Add or subtract multiples of 2π.", f"{T(a)} → {T(v)}."], [T(sp.Mod(a + pi, 2 * pi)), T(2 * pi - v), T(sp.Mod(a, pi))],
             H(f"P('{T(a)}') - 2*pi*floor(P('{T(a)}')/(2*pi))"), why=["Added π instead of 2π", "Subtracted from 2π", "Used multiples of π"])


# ============================================================== S4 Arc length and sector area
@fam("012")
def s4_arc(r, L):
    rad = rint(r, 2, 15)
    a = pick(r, SPECIAL[1:] + [sp.Rational(5, 4) * pi, sp.Rational(2, 5) * pi])
    kind = pick(r, ["arc", "sector"])
    degrees = L >= 1 and r.random() < 0.6
    gv = f"{T(deg(a))}°" if degrees else f"{T(a)} radians"
    if L == 2 and r.random() < 0.5:
        s_ = rad * a
        return Q(f"An arc of length {T(s_)} units has a central angle of {gv}. Find the radius of the circle.", f"{rad} units", ["s = rθ with θ in radians.", f"θ = {T(a)}.", f"r = s/θ = {rad}."],
                 [f"{T(s_ * a)} units", f"{T(sp.nsimplify(s_ / deg(a)))} units", f"{2 * rad} units"], H(f"P('{T(s_)}')/P('{T(deg(a))}°')" if degrees else f"P('{T(s_)}')/P('{T(a)}')"),
                 why=["Multiplied by θ", "Used degrees in the formula", "Gave the diameter"], tags=["modeling"])
    if kind == "arc":
        v = rad * a
        return Q(f"A circle has radius {rad} cm. Find the exact length of the arc intercepted by a central angle of {gv}.", f"{T(v)} cm", [("Convert to radians: θ = " + T(a) + ". ") if degrees else "θ is in radians.", "s = rθ.", f"s = {rad} · {T(a)} = {T(v)} cm."],
                 [f"{T(rad * deg(a))} cm", f"{T(rad * rad * a / 2)} cm", f"{T(2 * rad * a)} cm"], H(f"{rad}*P('{T(deg(a))}°')" if degrees else f"{rad}*P('{T(a)}')"),
                 why=["Used degrees in s = rθ", "Found the sector area", "Used the diameter"])
    v = sp.Rational(1, 2) * rad ** 2 * a
    return Q(f"A circle has radius {rad} in. Find the exact area of the sector with central angle {gv}.", f"{T(v)} in²", [("Convert to radians: θ = " + T(a) + ". ") if degrees else "θ is in radians.", "A = (1/2)r²θ.", f"A = (1/2)({rad})²({T(a)}) = {T(v)} in²."],
             [f"{T(rad ** 2 * a)} in²", f"{T(rad * a)} in²", f"{T(sp.Rational(1, 2) * rad ** 2 * deg(a))} in²"], H(f"Rational(1, 2)*{rad}**2*P('{T(deg(a))}°')" if degrees else f"Rational(1, 2)*{rad}**2*P('{T(a)}')"),
             why=["Forgot the 1/2", "Found the arc length", "Used degrees in the formula"])


@fam("12")
def s4_round(r, L):
    rad = rint(r, 3, 40)
    d = rint(r, 15, 330)
    v = rad * d * math.pi / 180
    return Q(f"A sprinkler sprays water {rad} ft and rotates through {d}°. Find the length of the arc it covers, to the nearest tenth of a foot.", f"{Rd(v, 1)} ft",
             ["Convert to radians: θ = " + f"{d}π/180.", f"s = rθ = {rad} · {d}π/180.", f"s ≈ {Rd(v, 1)} ft."], [f"{Rd(rad * d, 1)} ft", f"{Rd(rad * rad * d * math.pi / 360, 1)} ft", f"{Rd(rad * d / 180, 1)} ft"],
             H(f"{rad}*{d}*pi/180", "round", places=1), why=["Used degrees in s = rθ", "Found the sector area", "Forgot the π"], tags=["modeling"])


# ============================================================== S5 Right triangle applications
@fam("012")
def s5_side(r, L):
    A_ = rint(r, 15, 75)
    known = rint(r, 5, 60)
    kind = pick(r, ["opp_from_adj", "opp_from_hyp", "adj_from_hyp", "hyp_from_opp"])
    rad_ = A_ * math.pi / 180
    if kind == "opp_from_adj":
        v, fn, lab = known * math.tan(rad_), "tan", {"CB": f"{known} m", "AC": "x", "B": f"{A_}°"}
        code = f"{known}*tan({A_}*pi/180)"
        w = [known * math.sin(rad_), known / math.tan(rad_), known * math.cos(rad_)]
        ctx = f"From a point {known} m from the base of a tower, the angle of elevation to the top is {A_}°. How tall is the tower, to the nearest tenth of a meter?"
    elif kind == "opp_from_hyp":
        v, lab = known * math.sin(rad_), {"AB": f"{known} ft", "AC": "x", "B": f"{A_}°"}
        code = f"{known}*sin({A_}*pi/180)"
        w = [known * math.cos(rad_), known * math.tan(rad_), known / math.sin(rad_)]
        ctx = f"A {known}-ft ladder leans against a wall, making a {A_}° angle with the ground. How high up the wall does it reach, to the nearest tenth of a foot?"
    elif kind == "adj_from_hyp":
        v, lab = known * math.cos(rad_), {"AB": f"{known} ft", "CB": "x", "B": f"{A_}°"}
        code = f"{known}*cos({A_}*pi/180)"
        w = [known * math.sin(rad_), known / math.cos(rad_), known * math.tan(rad_)]
        ctx = f"A {known}-ft ramp makes a {A_}° angle with the ground. How far does it extend horizontally, to the nearest tenth of a foot?"
    else:
        v, lab = known / math.sin(rad_), {"AC": f"{known} ft", "AB": "x", "B": f"{A_}°"}
        code = f"{known}/sin({A_}*pi/180)"
        w = [known * math.sin(rad_), known / math.cos(rad_), known / math.tan(rad_)]
        ctx = f"A kite is flying {known} ft above the ground and its string makes a {A_}° angle with the ground. How long is the string, to the nearest tenth of a foot?"
    unit = "m" if "m" in lab.get("CB", "") else "ft"
    need(len({Rd(v, 1)} | {Rd(z, 1) for z in w}) == 4)
    return Q(ctx if L else ctx.split(", to the nearest")[0].replace(" How", " How") + (" Round to the nearest tenth." if True else ""), f"{Rd(v, 1)} {unit}",
             ["Label the sides relative to the given angle.", "Choose the ratio that links the known side and the unknown side (SOH-CAH-TOA).", f"x ≈ {Rd(v, 1)} {unit}."], [f"{Rd(z, 1)} {unit}" for z in w],
             H(code, "round", places=1), why=["Used the wrong trigonometric ratio", "Used the wrong ratio (or inverted it)", "Set up the equation incorrectly"], tags=["modeling"],
             diagram={"alt": "Right triangle with " + ", ".join(f"{k_ if k_ not in ('A', 'B') else 'angle ' + k_} labeled {v_}" for k_, v_ in lab.items()) + ".", "draw": tri_draw(lab)} if L < 2 else None)


@fam("012")
def s5_angle(r, L):
    a, b = rint(r, 3, 40), rint(r, 3, 40)
    need(a != b)
    v = math.degrees(math.atan2(a, b))
    return Q(f"A ramp rises {a} ft over a horizontal distance of {b} ft. Find the angle the ramp makes with the ground, to the nearest tenth of a degree.", f"{Rd(v, 1)}°",
             [f"tan θ = opposite ÷ adjacent = {a}/{b}.", f"θ = tan⁻¹({a}/{b}).", f"θ ≈ {Rd(v, 1)}°."], [f"{Rd(math.degrees(math.atan2(b, a)), 1)}°", f"{Rd(math.degrees(math.asin(min(a, b) / max(a, b))), 1)}°", f"{Rd(math.atan2(a, b), 1)}°"],
             H(f"atan(Rational({a}, {b}))*180/pi", "deg", places=1), why=["Inverted the ratio", "Used inverse sine", "Left the answer in radians"], tags=["modeling"])


# ============================================================== S6 Amplitude and period
def sinus(A, B, C, D_, f="sin"):
    inner = B * (x - C)
    return A * FN[f](inner) + D_


@fam("012")
def s6_ap(r, L):
    A = sp.Rational(rint(r, -6, 6, True), 1 if L < 2 else pick(r, [1, 2]))
    B = pick(r, [1, 2, 3, 4, sp.Rational(1, 2), sp.Rational(1, 3)] if L else [1, 2, 3, 4])
    f = pick(r, ["sin", "cos"] if L < 2 else ["sin", "cos", "tan"])
    D_ = rint(r, -3, 3) if L else 0
    e = A * FN[f](B * x) + D_
    ask = "period" if f == "tan" else pick(r, ["amplitude", "period"])
    if ask == "amplitude":
        return Q(f"Find the amplitude of y = {T(e)}.", T(abs(A)), ["The amplitude of y = a·sin(bx) + d (or cos) is |a|.", f"|{T(A)}| = {T(abs(A))}."], [T(A) if A < 0 else T(2 * A), T(2 * pi / B), T(abs(A) + D_) if D_ else T(abs(A) / 2)],
                 H(f"(lambda E: (maximum(E, x) - minimum(E, x))/2)(P('{T(e)}'))" if False else f"Abs(Rational({A.p}, {A.q}))"), why=["Kept the negative sign", "Gave the period", "Added the vertical shift"])
    per = (pi if f == "tan" else 2 * pi) / B
    return Q(f"Find the period of y = {T(e)}.", T(per), [f"The period of {'tan(bx) is π ÷ |b|' if f == 'tan' else 'sin(bx) and cos(bx) is 2π ÷ |b|'}.", f"b = {T(B)}.", f"Period = {T(per)}."],
             [T(2 * pi * B), T((2 * pi if f == "tan" else pi) / B), T(abs(A))], PY("period", expr=T(e)), why=["Multiplied by b instead of dividing", "Used the wrong base period", "Gave the amplitude"])


# ============================================================== S7 / S8 sine and cosine graphs
def graph_q(r, L, f):
    A = rint(r, -3, 3, True)
    B = pick(r, [1, 2, sp.Rational(1, 2)])
    D_ = rint(r, -1, 1) if L else 0
    need(abs(A) + abs(D_) <= 4)
    e = A * FN[f](B * x) + D_
    fn = sp.lambdify(x, e, "math")
    xmax = float(2 * pi / B) * (2 if B == 2 else 1)
    opts = [(f"y = {T(e)}", True), (f"y = {T(A * FN[f](x / B if B != 1 else 2 * x) + D_)}", False), (f"y = {T(-A * FN[f](B * x) + D_)}", False),
            (f"y = {T(A * FN['cos' if f == 'sin' else 'sin'](B * x) + D_)}", False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q("Which equation matches the graph?", f"y = {T(e)}", [f"Midline y = {D_}; amplitude {abs(A)}.", f"Period {T(2 * pi / B)}, so b = {T(B)}.", f"At x = 0 the graph is {'on the midline' if f == 'sin' else ('at a maximum' if A > 0 else 'at a minimum')}, so it is a {'sine' if f == 'sin' else 'cosine'} graph" + (" reflected over the midline." if A < 0 else ".")],
             options=opts, chk=H(f"P('{T(e)}')"), mode="mc",
             diagram={"alt": f"Graph of a sinusoid over 0 ≤ x ≤ {T(sp.nsimplify(xmax / math.pi))}π with midline y = {D_}, amplitude {abs(A)}, period {T(2 * pi / B)}, and {'value ' + str(D_) + ' at x = 0' if f == 'sin' else 'value ' + str(A + D_) + ' at x = 0'}"
                             + (f", decreasing at x = 0" if (f == "sin" and A < 0) else (f", increasing at x = 0" if f == "sin" else "")) + ".",
                      "draw": trig_draw(fn, 0, xmax, -4, 4, 2 if B != sp.Rational(1, 2) else 1)})


@fam("012")
def s7_features(r, L):
    A = rint(r, -5, 5, True)
    B = pick(r, [1, 2, 3, sp.Rational(1, 2)])
    C = pick(r, [0, pi / 4, pi / 3, pi / 6, -pi / 4, pi / 2]) if L else 0
    D_ = rint(r, -4, 4)
    e = A * sp.sin(B * (x - C)) + D_
    etxt = f"{T(A) if abs(A) != 1 else ('-' if A < 0 else '')}sin({T(B) if B != 1 else ''}{'(' if C else ''}{T(x - C) if C else 'x'}{')' if C else ''}) {'+' if D_ >= 0 else '-'} {abs(D_)}".replace("sin((", "sin((") if (C or D_) else f"y = {T(e)}"
    etxt = etxt if etxt.startswith("y") else "y = " + etxt
    ask = pick(r, ["max", "min", "midline", "shift"] if C else ["max", "min", "midline"])
    if ask == "max":
        return Q(f"Find the maximum value of {etxt}.", str(abs(A) + D_), ["Maximum = d + |a|.", f"{D_} + {abs(A)} = {abs(A) + D_}."], [str(A + D_) if A < 0 else str(abs(A)), str(D_ - abs(A)), str(abs(A) * 2 + D_)],
                 H(f"{D_} + Abs({A})"), why=["Ignored the reflection sign" if A < 0 else "Ignored the vertical shift", "Gave the minimum", "Doubled the amplitude"])
    if ask == "min":
        return Q(f"Find the minimum value of {etxt}.", str(D_ - abs(A)), ["Minimum = d - |a|.", f"{D_} - {abs(A)} = {D_ - abs(A)}."], [str(-abs(A)) if D_ else str(-abs(A) - 1), str(D_ + abs(A)), str(D_ - 2 * abs(A))],
                 H(f"{D_} - Abs({A})"), why=["Ignored the vertical shift", "Gave the maximum", "Doubled the amplitude"])
    if ask == "midline":
        return Q(f"Find the equation of the midline of {etxt}.", f"y = {D_}", ["The midline is y = d.", f"y = {D_}."], [f"y = {A}", f"y = {D_ + abs(A)}", f"y = {-D_}" if D_ else "y = 1"],
                 H(f"y - {D_}", "eqn"), why=["Used the amplitude", "Gave the maximum", "Used the opposite sign"])
    return Q(f"Find the phase shift of {etxt}.", f"{T(abs(C))} {'right' if C > 0 else 'left'}", ["y = a·sin(b(x - c)) + d has phase shift c.", f"c = {T(C)}.", f"Shift {T(abs(C))} {'right' if C > 0 else 'left'}."],
             [f"{T(abs(C))} {'left' if C > 0 else 'right'}", f"{T(abs(C * B))} {'right' if C > 0 else 'left'}" if B != 1 else f"{T(abs(C) * 2)} {'right' if C > 0 else 'left'}", f"{abs(D_) if D_ else 1} up"],
             PY("phase", c=str(C)), why=["Used the wrong direction", "Multiplied by b", "Gave the vertical shift"])


@fam("012")
def s7_graph(r, L):
    return graph_q(r, L, "sin")


@fam("012")
def s8_graph(r, L):
    return graph_q(r, L, "cos")


@fam("012")
def s8_write(r, L):
    A = rint(r, 1, 6)
    per = pick(r, [2 * pi, pi, 4 * pi, pi / 2, 6 * pi] if L < 2 else [12, 24, 10, 4])
    D_ = rint(r, -5, 8)
    B = 2 * pi / per
    ctx = L == 2
    e = A * sp.cos(B * x) + D_
    if ctx:
        q = f"A buoy bobs so that its height in feet is at a maximum of {D_ + A} at t = 0 and a minimum of {D_ - A}, completing one cycle every {per} seconds. Write a cosine model h(t)."
        ans = "h(t) = " + T(e.subs(x, t))
        w = ["h(t) = " + T((A * sp.cos(per * t / (2 * pi)) + D_)), "h(t) = " + T(2 * A * sp.cos(B * t) + D_), "h(t) = " + T(A * sp.sin(B * t) + D_)]
        return Q(q, ans, [f"Amplitude = ({D_ + A} - {par(D_ - A)})/2 = {A}.", f"Midline = ({D_ + A} + {par(D_ - A)})/2 = {D_}.", f"b = 2π/{per} = {T(B)}.", ans + "."], w,
                 H(f"P('{T(e.subs(x, t))}'.replace('t', 'x'))" if False else f"{A}*cos(2*pi/{per}*t) + {D_}"), why=["Used b = period ÷ (2π)", "Used the full height difference as the amplitude", "Used sine, which starts at the midline"], tags=["modeling"])
    q = f"Write an equation of the form y = a·cos(bx) + d with amplitude {A}, period {T(per)}, and midline y = {D_}. (Use a > 0.)"
    ans = "y = " + T(e)
    return Q(q, ans, ["a = amplitude.", f"b = 2π/period = {T(B)}.", "d = midline.", ans + "."], ["y = " + T(A * sp.cos(per * x / (2 * pi)) + D_ if per != 2 * pi else A * sp.cos(2 * x) + D_), "y = " + T(D_ * sp.cos(B * x) + A) if D_ not in (A, 0) else "y = " + T(A * sp.cos(B * x) - D_ if D_ else A * sp.cos(B * x) + 1),
                                                                         "y = " + T(A * sp.cos(B * x - D_))], H(f"{A}*cos(2*pi/({T(per).replace('π', '*pi') if 'π' in T(per) else T(per)})*x) + {D_}".replace("(*pi", "(pi")),
             why=["Used b = period ÷ (2π)", "Switched the amplitude and midline", "Put the midline inside the cosine"])


# ============================================================== S9 Solving trig equations
@fam("012")
def s9_solve(r, L):
    f = pick(r, ["sin", "cos", "tan"])
    vals = {"sin": [sp.Rational(1, 2), -sp.Rational(1, 2), sp.sqrt(2) / 2, -sp.sqrt(2) / 2, sp.sqrt(3) / 2, -sp.sqrt(3) / 2, 1, -1, 0],
            "cos": [sp.Rational(1, 2), -sp.Rational(1, 2), sp.sqrt(2) / 2, -sp.sqrt(2) / 2, sp.sqrt(3) / 2, -sp.sqrt(3) / 2, 1, -1, 0],
            "tan": [1, -1, sp.sqrt(3), -sp.sqrt(3), sp.sqrt(3) / 3, -sp.sqrt(3) / 3, 0]}[f]
    v = pick(r, vals)
    a = rint(r, 1, 3) if L else 1
    c = rint(r, -4, 4) if L else 0
    rhs = sp.nsimplify(a * v + c)
    lhs = T(a * FN[f](x) + c)
    sols = sorted(sp.solveset(sp.Eq(FN[f](x), v), x, sp.Interval.Ropen(0, 2 * pi)), key=float)
    if L == 2 and r.random() < 0.5:
        # quadratic in the function: (f - v)(f - w) = 0
        w2 = pick(r, [vv for vv in vals if vv != v and abs(vv) <= 1 or f == "tan" and vv != v])
        pexpr = sp.expand((y - v) * (y - w2))
        need(all(cf.is_Rational for cf in sp.Poly(pexpr, y).all_coeffs()))
        sols = sorted(set(sp.solveset(sp.Eq(FN[f](x), v), x, sp.Interval.Ropen(0, 2 * pi))) | set(sp.solveset(sp.Eq(FN[f](x), w2), x, sp.Interval.Ropen(0, 2 * pi))), key=float)
        eq = T(pexpr).replace("y²", f"{f}²(x)").replace("y", f"{f}(x)") + " = 0"
        code = f"[s_ for v_ in solve(P('{T(pexpr)}'), y) for s_ in solveset(Eq({f}(x), v_), x, Interval.Ropen(0, 2*pi))]"
    else:
        eq = f"{lhs} = {T(rhs)}"
        code = f"[s_ for s_ in solveset(Eq(P('{lhs}'), P('{T(rhs)}')), x, Interval.Ropen(0, 2*pi))]"
    need(0 < len(sols) <= 4)
    ans = " or ".join(f"x = {T(s_)}" for s_ in sols)
    w1 = " or ".join(f"x = {T(s_)}" for s_ in sols[:1]) if len(sols) > 1 else f"x = {T(sols[0] + pi)}" if sols[0] + pi < 2 * pi else f"x = {T(sols[0] - pi)}"
    w2_ = " or ".join(f"x = {T(sp.Mod(-s_, 2 * pi))}" for s_ in sols)
    w3 = " or ".join(f"x = {T(s_ + pi / 6)}" for s_ in sols) if f != "tan" else " or ".join(f"x = {T(sp.Mod(pi / 2 - s_, 2 * pi))}" for s_ in sols)
    if w2_ == ans or sorted(w2_.split(" or ")) == sorted(ans.split(" or ")):
        w2_ = " or ".join(f"x = {T(sp.Mod(s_ + pi / 2, 2 * pi))}" for s_ in sols)
    return Q(f"Solve {eq} for 0 ≤ x < 2π.", ans, (["Factor as a quadratic in " + f + "(x)."] if "²" in eq else [f"Isolate {f}(x): {f}(x) = {T(v)}."]) + ["Use reference angles and the quadrant signs.", f"Solutions in [0, 2π): {', '.join(T(s_) for s_ in sols)}."],
             [w1, w2_, w3], H(code, "set"), why=["Missed solutions in other quadrants", "Used the wrong quadrants", "Used the wrong reference angle"])


# ============================================================== S10 Inverse trig
@fam("012")
def s10_inverse(r, L):
    f = pick(r, ["sin", "cos", "tan"])
    vals = [sp.Rational(1, 2), -sp.Rational(1, 2), sp.sqrt(2) / 2, -sp.sqrt(2) / 2, sp.sqrt(3) / 2, -sp.sqrt(3) / 2, 1, -1, 0] if f != "tan" else [1, -1, sp.sqrt(3), -sp.sqrt(3), sp.sqrt(3) / 3, -sp.sqrt(3) / 3, 0]
    v = pick(r, vals)
    a = {"sin": sp.asin, "cos": sp.acos, "tan": sp.atan}[f](v)
    degrees = L == 0 and r.random() < 0.5
    other = sp.Mod(pi - a, 2 * pi) if f == "sin" else (2 * pi - a if f == "cos" else a + pi)
    w = [ang(other, degrees) if other != a else ang(a + pi, degrees), ang(sp.Mod(a, 2 * pi), degrees) if sp.Mod(a, 2 * pi) != a else ang(-a, degrees) if a else ang(pi, degrees),
         ang({"sin": sp.acos, "cos": sp.asin, "tan": lambda z: sp.acot(z) if z else pi / 2}[f](v), degrees)]
    need(ang(a, degrees) not in w)
    return Q(f"Find the exact value of {f}⁻¹({T(v)})" + (" in degrees." if degrees else " in radians."), ang(a, degrees),
             [f"The range of {f}⁻¹ is {'[-π/2, π/2]' if f == 'sin' else '[0, π]' if f == 'cos' else '(-π/2, π/2)'}.", f"Find the angle in that range whose {f} is {T(v)}.", f"{f}⁻¹({T(v)}) = {ang(a, degrees)}."],
             w, H(f"{'a' + f}(P('{T(v)}'))" + ("*180/pi" if degrees else ""), "expr") if not degrees else H(f"{'a' + f}(P('{T(v)}'))*180/pi", "deg", places=0),
             why=["Chose an angle outside the principal range", "Gave a coterminal angle outside the range", "Used the wrong inverse function"])


@fam("12")
def s10_compose(r, L):
    a_, b_, c_ = pick(r, [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (4, 3, 5), (12, 5, 13)])
    inner = pick(r, ["sin", "cos", "tan"])
    outer = pick(r, [f_ for f_ in ["sin", "cos", "tan"] if f_ != inner])
    arg = {"sin": sp.Rational(a_, c_), "cos": sp.Rational(b_, c_), "tan": sp.Rational(a_, b_)}[inner]
    if L == 2 and r.random() < 0.5:
        arg = -arg
    th = {"sin": sp.asin, "cos": sp.acos, "tan": sp.atan}[inner](arg)
    v = sp.simplify(FN[outer](th))
    return Q(f"Find the exact value of {outer}({inner}⁻¹({T(arg)})).", T(v), [f"Let θ = {inner}⁻¹({T(arg)}); draw a right triangle (θ in the principal range).", f"The sides are {a_}, {b_}, {c_}.", f"{outer} θ = {T(v)}."],
             [T(-v), T(1 / v), T(arg)], H(f"{outer}({'a' + inner}(P('{T(arg)}')))"), why=["Used the wrong sign for the quadrant", "Used the reciprocal ratio", "Gave the original ratio"])


# ============================================================== S11 Principal values and technology
@fam("012")
def s11_tech(r, L):
    f = pick(r, ["sin", "cos", "tan"])
    v = sp.Rational(rint(r, -95, 95, True), 100) if f != "tan" else sp.Rational(rint(r, -400, 400, True), 100)
    degrees = r.random() < 0.5
    a = {"sin": math.asin, "cos": math.acos, "tan": math.atan}[f](float(v))
    if L < 2:
        val = math.degrees(a) if degrees else a
        txt = (Rd(val, 1) + "°") if degrees else Rd(val, 3)
        return Q(f"Use a calculator to find {f}⁻¹({D(F(v.p, v.q))}) " + ("in degrees, to the nearest tenth." if degrees else "in radians, to the nearest thousandth."), txt,
                 [f"Set the calculator to {'degree' if degrees else 'radian'} mode.", f"{f}⁻¹({D(F(v.p, v.q))}) ≈ {txt}."],
                 [(Rd(a, 1) + "°") if degrees else Rd(math.degrees(a), 3), (Rd(180 - math.degrees(a), 1) + "°") if degrees else Rd(math.pi - a, 3), (Rd(math.degrees({"sin": math.acos, "cos": math.asin, "tan": lambda z: math.pi / 2 - math.atan(z)}[f](float(v))), 1) + "°") if degrees else Rd({"sin": math.acos, "cos": math.asin, "tan": lambda z: math.pi / 2 - math.atan(z)}[f](float(v)), 3)],
                 H(f"a{f}({v})*180/pi", "deg", places=1) if degrees else H(f"a{f}({v})", "round", places=3), why=["Used the wrong calculator mode", "Gave the second-quadrant angle instead of the principal value", "Used the wrong inverse function"])
    need(f != "tan" and abs(v) < 1)
    sols = sorted(math.degrees(s_) % 360 for s_ in ({"sin": [a, math.pi - a], "cos": [a, -a]}[f]))
    ans = " or ".join(f"x ≈ {Rd(s_, 1)}°" for s_ in sols)
    return Q(f"Solve {f}(x) = {D(F(v.p, v.q))} for 0° ≤ x < 360°. Round to the nearest tenth of a degree.", ans,
             [f"Principal value: {f}⁻¹({D(F(v.p, v.q))}) ≈ {Rd(math.degrees(a), 1)}°.", f"{'sin' if f == 'sin' else 'cos'} is {'positive' if v > 0 else 'negative'} in quadrants {('I and II' if v > 0 else 'III and IV') if f == 'sin' else ('I and IV' if v > 0 else 'II and III')}.",
              f"Solutions: {', '.join(Rd(s_, 1) + '°' for s_ in sols)}."],
             [f"x ≈ {Rd(math.degrees(a), 1)}°", " or ".join(f"x ≈ {Rd(s_, 1)}°" for s_ in sorted([(math.degrees(a)) % 360, (180 + math.degrees(a)) % 360])),
              " or ".join(f"x ≈ {Rd(s_, 1)}°" for s_ in sorted([math.degrees(a) % 360, (360 - math.degrees(a)) % 360] if f == "sin" else [math.degrees(a) % 360, (180 - math.degrees(a)) % 360]))],
             PY("deg_set", f=f, v=str(v), places=1), why=["Gave only the principal value", "Added 180° (the tangent rule)", "Used the other function's symmetry"])


SKILLS = {
    1: dict(name="Unit Circle and Circular Functions", std=["F-TF.A.2", "F-TF.A.3"], fams=[s1_point, s1_ref], extra=[err_of(s1_point), open_of(s1_point), err_of(s1_ref)]),
    2: dict(name="Exact Trigonometric Values", std=["F-TF.A.3"], fams=[s2_exact], extra=[err_of(s2_exact), open_of(s2_exact)]),
    3: dict(name="Angles and Radian Measure", std=["F-TF.A.1"], fams=[s3_convert, s3_coterminal], extra=[err_of(s3_convert), open_of(s3_convert)]),
    4: dict(name="Arc Length and Sector Area", std=["G-C.B.5"], fams=[s4_arc, s4_round], extra=[err_of(s4_arc), open_of(s4_arc)]),
    5: dict(name="Right Triangle Applications", std=["G-SRT.C.8"], fams=[s5_side, s5_angle], extra=[err_of(s5_side), open_of(s5_side)]),
    6: dict(name="Amplitude and Period", std=["F-TF.B.5", "F-IF.C.7e"], fams=[s6_ap], extra=[err_of(s6_ap), open_of(s6_ap)]),
    7: dict(name="Sine Functions and Graphs", std=["F-TF.B.5", "F-IF.C.7e"], fams=[s7_features, s7_graph], extra=[err_of(s7_features), open_of(s7_features)]),
    8: dict(name="Cosine Functions and Graphs", std=["F-TF.B.5", "F-IF.C.7e"], fams=[s8_write, s8_graph], extra=[err_of(s8_write), open_of(s8_write)]),
    9: dict(name="Solving Trigonometric Equations", std=["F-TF.B.7"], fams=[s9_solve], extra=[err_of(s9_solve), open_of(s9_solve)]),
    10: dict(name="Inverse Trigonometric Functions and Graphs", std=["F-TF.B.6", "F-TF.B.7"], fams=[s10_inverse, s10_compose], extra=[err_of(s10_inverse), open_of(s10_inverse)]),
    11: dict(name="Principal Values and Technology", std=["F-TF.B.7"], fams=[s11_tech], extra=[err_of(s11_tech), open_of(s11_tech)]),
}
