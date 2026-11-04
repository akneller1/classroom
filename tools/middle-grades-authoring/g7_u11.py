"""Grade 7 Unit 11 — Right Triangles in Algebra (right-triangles-algebra)."""
from glib import *

UNIT_ID = "right-triangles-algebra"
ABBR = "rta"
TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20), (15, 20, 25), (20, 21, 29), (9, 40, 41)]


def rad_text(k, n):
    """k√n simplified text (n square-free assumed by caller)."""
    return (f"{k}√{n}" if k != 1 else f"√{n}") if n != 1 else str(k)


def simp_sqrt(n):
    k, m = 1, n
    for d in range(2, int(n ** 0.5) + 1):
        while m % (d * d) == 0:
            m //= d * d
            k *= d
    return k, m


# ============================================================== S1 Square Roots and Irrational Numbers
@fam("012")
def s1_eval(r, L):
    k = r.randint(2, 15) if L < 2 else r.randint(2, 30)
    if L == 0:
        t = f"√{k * k}"
        return Q(f"Find the principal square root: {t}", str(k), [f"{k} × {k} = {k * k}.", f"So {t} = {k}."], [str(k * k // 2) if k * k % 2 == 0 else str(k + 1), str(k * k), str(-k)], V(t),
                 why=["Divided by 2 instead of taking the square root", "Squared instead", "Gave the negative root"])
    if L == 1:
        a, b = r.randint(2, 12), r.randint(2, 12)
        t = pick(r, [f"√{a * a} + √{b * b}", f"√{a * a} × √{b * b}", f"-√{a * a}"])
        v = M_ev(t)
        return Q(f"Simplify: {t}", N(v), ["Find each square root first.", f"√{a * a} = {a}" + (f", √{b * b} = {b}." if str(b * b) in t else "."), f"Result: {N(v)}."],
                 [N(math.isqrt(a * a + b * b)) if "+" in t and math.isqrt(a * a + b * b) ** 2 == a * a + b * b else N(v + 1), N(-v), N(v * 2)], V(t),
                 why=["Combined under one square root", "Made a sign error", ""])
    a, b = r.randint(2, 9), r.randint(2, 9)
    t = f"√({a * a} × {b * b})" if r.random() < 0.5 else f"√({a * a}/{b * b})"
    v = M_ev(t)
    return Q(f"Simplify: {t}", N(v), ["The square root of a product (or quotient) is the product (or quotient) of the square roots.", f"√{a * a} = {a} and √{b * b} = {b}.", f"Result: {N(v)}."],
             [N(F(a * a) * b * b) if "×" in t else N(F(a * a, b * b)), N(F(a + b)) if "×" in t else N(F(a, b * b)), N(v * 2)], V(t), why=["Did not take the square root", "Took only one square root", ""])


def M_ev(e):
    import mathtext
    return mathtext.ev(e)


@fam("012")
def s1_estimate(r, L):
    n = r.randint(2, 200)
    s = math.isqrt(n)
    need(s * s != n)
    near = s if n - s * s < (s + 1) ** 2 - n else s + 1
    need(n - s * s != (s + 1) ** 2 - n)
    return Q(f"√{n} is closest to which whole number?", str(near), [f"{s}² = {s * s} and {s + 1}² = {(s + 1) ** 2}.", f"{n} is closer to {near * near}.", f"√{n} ≈ {near}."],
             [str(s + s + 1 - near), str(n // 2), str(near * 2)], PY("closest_int", n=n), why=["Chose the farther whole number", "Divided by 2", ""])


@fam("12", mode="mc")
def s1_classify(r, L):
    sq = [k * k for k in range(2, 16)]
    nsq = [n for n in range(2, 120) if math.isqrt(n) ** 2 != n]
    ask = pick(r, ["rational", "irrational"])
    good = f"√{pick(r, sq if ask == 'rational' else nsq)}"
    bad = [f"√{x}" for x in pick(r, nsq if ask == "rational" else sq, 3)]
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q(f"Which square root is {ask}?", good, ["The square root of a perfect square is rational.", "The square root of a whole number that is not a perfect square is irrational.", f"{good} is {ask}."],
             options=opts, chk=PY("is_" + ask), mode="mc")


@fam("2")
def s1_simplify(r, L):
    k, m = r.randint(2, 7), pick(r, [2, 3, 5, 6, 7])
    n = k * k * m
    return Q(f"Simplify √{n}.", f"{k}√{m}", [f"Find the greatest perfect-square factor: {n} = {k * k} × {m}.", f"√{n} = √{k * k} × √{m}.", f"= {k}√{m}."],
             [f"{m}√{k}", f"{k * k}√{m}", f"{k}√{m * k}" if m * k != m else f"{k + 1}√{m}"], V(f"√{n}"), why=["Switched the factors", "Did not take the square root of the perfect square", "Chose a factor that is not a perfect square"])


# ============================================================== S2 Pythagorean Theorem
@fam("012")
def s2_hyp(r, L):
    if L == 2:
        a, b = r.randint(2, 12), r.randint(2, 12)
        c2 = a * a + b * b
        k, m = simp_sqrt(c2)
        ans = rad_text(k, m) if m != 1 else str(k)
        return Q(f"A right triangle has legs {a} and {b}. Find the exact length of the hypotenuse in simplest radical form.", ans, [f"c² = {a}² + {b}² = {a * a} + {b * b} = {c2}.", f"c = √{c2}.", f"c = {ans}."],
                 [str(a + b), f"√{a * b}" if a * b != c2 else str(c2), str(c2)], V(f"√({a}^2 + {b}^2)"), why=["Added the legs", "Multiplied the legs", "Forgot the square root"])
    a, b, c = pick(r, TRIPLES)
    k = r.randint(1, 3) if L else 1
    a, b, c = a * k, b * k, c * k
    what = "hyp" if L == 0 else pick(r, ["hyp", "leg"])
    pts = [(0, 0), (b, 0), (0, a)]
    if what == "hyp":
        return Q(f"A right triangle has legs {a} cm and {b} cm. How long is the hypotenuse?", f"{c} cm", [f"a² + b² = c².", f"{a}² + {b}² = {a * a} + {b * b} = {c * c}.", f"c = √{c * c} = {c} cm."],
                 [f"{a + b} cm", f"{c * c} cm", f"{N(F(a + b, 2))} cm"], V(f"√({a}^2 + {b}^2)"), why=["Added the legs", "Forgot the square root", "Averaged the legs"],
                 diagram={"alt": f"Right triangle with legs {a} and {b} and hypotenuse c.", "draw": poly_draw(pts, side_labels=[(0, str(b)), (1, "c"), (2, str(a))], right_angles=[0])} if L == 0 else None)
    return Q(f"A right triangle has hypotenuse {c} in. and one leg {a} in. How long is the other leg?", f"{b} in.", [f"a² + b² = c², so b² = c² - a².", f"b² = {c * c} - {a * a} = {b * b}.", f"b = {b} in."],
             [f"{N(M_ev(f'√({c}^2 + {a}^2)')) if False else Rd(math.sqrt(c * c + a * a), 1)} in.", f"{c - a} in.", f"{b * b} in."], V(f"√({c}^2 - {a}^2)"),
             why=["Added the squares instead of subtracting", "Subtracted the lengths", "Forgot the square root"])


@fam("012")
def s2_converse(r, L):
    a, b, c = pick(r, TRIPLES)
    if r.random() < 0.5:
        c = c + pick(r, [1, -1, 2])
    ok = a * a + b * b == c * c
    return Q(f"Can the side lengths {a}, {b}, and {c} form a right triangle?", "Yes" if ok else "No", [f"Check a² + b² = c² with the longest side as c.", f"{a}² + {b}² = {a * a + b * b}; {c}² = {c * c}.",
                                                                                                    f"{'Equal, so yes' if ok else 'Not equal, so no'}."], ["No" if ok else "Yes"], PY("right_tri", sides=[a, b, c]), mode="sa",
             why=["Did not square the side lengths"])


@fam("012")
def s2_context(r, L):
    a, b, c = pick(r, TRIPLES[:6])
    ctx = pick(r, [(f"A {c}-foot ladder leans against a wall. Its base is {a} feet from the wall. How high up the wall does the ladder reach?", f"{b} feet", f"√({c}^2 - {a}^2)"),
                   (f"A rectangular field is {a} m by {b} m. How long is the diagonal path across it?", f"{c} meters", f"√({a}^2 + {b}^2)"),
                   (f"A boat sails {a} km east and then {b} km north. How far is it from its starting point?", f"{c} km", f"√({a}^2 + {b}^2)")])
    t, ans, ex = ctx
    u = ans.split(" ", 1)[1]
    return Q(t, ans, ["Draw the right triangle and label the legs and hypotenuse.", "Use a² + b² = c².", f"{ans}."], [f"{a + b} {u}", f"{N(M_ev(ex)) if False else c + a} {u}", f"{c * c} {u}"],
             V(ex), why=["Added the lengths", "Combined the wrong sides", "Forgot the square root"], tags=["modeling"])


# ============================================================== S3 Distance and Midpoint
@fam("012")
def s3_distance(r, L):
    a, b, c = pick(r, TRIPLES[:5]) if L < 2 else (r.randint(1, 9), r.randint(1, 9), None)
    x1, y1 = r.randint(-6, 6), r.randint(-6, 6)
    sx, sy = pick(r, [1, -1]), pick(r, [1, -1])
    x2, y2 = x1 + sx * a, y1 + sy * b
    d2 = a * a + b * b
    k, m = simp_sqrt(d2)
    ans = rad_text(k, m) if m != 1 else str(k)
    return Q(f"Find the distance between ({x1}, {y1}) and ({x2}, {y2})." + (" Give an exact answer in simplest radical form." if L == 2 else ""), ans,
             ["d = √((x₂ - x₁)² + (y₂ - y₁)²).", f"= √(({x2} - {par(x1)})² + ({y2} - {par(y1)})²) = √({a * a} + {b * b}).", f"= √{d2} = {ans}."],
             [str(a + b), f"√{abs(a * a - b * b)}" if a != b else "0", str(d2)], V(f"√(({x2} - ({x1}))^2 + ({y2} - ({y1}))^2)"),
             why=["Added the coordinate differences", "Subtracted the squares", "Forgot the square root"])


@fam("012")
def s3_midpoint(r, L):
    x1, y1 = r.randint(-9, 9), r.randint(-9, 9)
    x2, y2 = r.randint(-9, 9), r.randint(-9, 9)
    if L == 0:
        need((x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0)
    mx, my = F(x1 + x2, 2), F(y1 + y2, 2)
    need((x1, y1) != (x2, y2))
    if L == 2 and r.random() < 0.5:
        return Q(f"M({D(mx)}, {D(my)}) is the midpoint of AB. A is ({x1}, {y1}). Find B.", f"({x2}, {y2})", ["Midpoint: M = ((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2).", f"x₂ = 2({D(mx)}) - {par(x1)} = {x2}.", f"y₂ = 2({D(my)}) - {par(y1)} = {y2}."],
                 [f"({D((x1 + mx) / 2)}, {D((y1 + my) / 2)})", f"({D(mx - x1)}, {D(my - y1)})", f"({D(2 * mx + x1)}, {D(2 * my + y1)})"], PY("point", x=f"2*{D(mx)} - ({x1})", y=f"2*{D(my)} - ({y1})"),
                 why=["Found the midpoint of A and M", "Subtracted instead of doubling", "Added A instead of subtracting"], tags=["reasoning"])
    return Q(f"Find the midpoint of the segment with endpoints ({x1}, {y1}) and ({x2}, {y2}).", f"({D(mx)}, {D(my)})", ["Average the x-coordinates and average the y-coordinates.", f"x: ({x1} + {par(x2)}) ÷ 2 = {D(mx)}.", f"y: ({y1} + {par(y2)}) ÷ 2 = {D(my)}."],
             [f"({x1 + x2}, {y1 + y2})", f"({D(F(x2 - x1, 2))}, {D(F(y2 - y1, 2))})", f"({D(my)}, {D(mx)})"], PY("point", x=f"({x1} + ({x2}))/2", y=f"({y1} + ({y2}))/2"),
             why=["Forgot to divide by 2", "Subtracted instead of adding", "Switched the coordinates"])


# ============================================================== S4 Write a Proportion
@fam("012")
def s4_shadow(r, L):
    h, s = r.randint(4, 7), r.randint(2, 9)
    k = r.randint(3, 12)
    T, S = h * k, s * k
    if L == 2:
        h, s = F(2 * h + 1, 2), s
        T = h * k
    nm = name(r)
    return Q(f"{nm} is {D(F(h))} ft tall and casts a {s}-ft shadow. At the same time, a tree casts a {S}-ft shadow. How tall is the tree?", f"{D(F(T))} feet",
             [f"Write a proportion: height ÷ shadow is the same for both.", f"{D(F(h))}/{s} = t/{S}.", f"t = {D(F(h))} × {S} ÷ {s} = {D(F(T))} feet."],
             [f"{D(F(h) + S - s)} feet", f"{D(F(S) * s / F(h))} feet", f"{D(F(h) * S)} feet"], EQ(f"{D(F(h))}*{S} = {s}*t", "t"),
             why=["Added the difference instead of using a proportion", "Set up the proportion upside down", "Forgot to divide by the person's shadow"], tags=["modeling"])


@fam("012")
def s4_rate(r, L):
    a, b = r.randint(2, 12), r.randint(2, 9)
    k = r.randint(2, 10) if L < 2 else F(r.randint(5, 25), 2)
    ctx = pick(r, [(f"{a} notebooks cost ${b * 3}. At the same rate, how much do {N(F(a) * k) if (F(a) * k).denominator == 1 else None} notebooks cost?", "dollars"),
                   (f"A machine makes {a} parts in {b} minutes. How many parts does it make in {N(F(b) * k)} minutes?", "parts")])
    t, unit = ctx
    need("None" not in t and (F(b) * k).denominator == 1)
    if unit == "dollars":
        v = F(b * 3) * k
        ans = f"${D(v)}"
        ex = f"{b * 3}*{N(F(a) * k)}/{a}"
    else:
        v = F(a) * k
        need(v.denominator == 1)
        ans = f"{D(v)} parts"
        ex = f"{a}*{N(F(b) * k)}/{b}"
    return Q(t, ans, ["Write a proportion comparing the same quantities in the same order.", "Cross multiply or use the scale factor.", f"Answer: {ans}."],
             [f"${D(v + 3)}" if unit == "dollars" else f"{D(v + b)} parts", f"${D(v * 2)}" if unit == "dollars" else f"{D(v * 2)} parts", f"${D(v / k * 1)}" if unit == "dollars" else f"{a} parts"],
             V(ex), why=["Added instead of multiplying", "", "Did not scale up"], tags=["modeling"])


# ============================================================== S5 Special Right Triangles
@fam("012")
def s5_45(r, L):
    a = r.randint(2, 15)
    if L == 0 or r.random() < 0.5:
        return Q(f"In a 45°-45°-90° triangle, each leg is {a}. Find the hypotenuse.", f"{a}√2", ["In a 45°-45°-90° triangle, hypotenuse = leg × √2.", f"Hypotenuse = {a}√2."],
                 [f"{a}√3", f"{2 * a}", f"{a}"], V(f"{a}√2"), why=["Used the 30°-60°-90° ratio", "Doubled the leg", "Thought all sides are equal"])
    return Q(f"In a 45°-45°-90° triangle, the hypotenuse is {a}√2. Find the length of each leg.", str(a), ["hypotenuse = leg × √2.", f"{a}√2 = leg × √2.", f"leg = {a}."],
             [f"{a}√2", f"{2 * a}", f"{N(F(a, 2))}√2"], V(str(a)), why=["Copied the hypotenuse", "Doubled instead of dividing", "Halved the hypotenuse"])


@fam("012")
def s5_30(r, L):
    s = r.randint(2, 12)
    what = pick(r, ["hyp", "long"]) if L < 2 else pick(r, ["hyp", "long", "short_from_hyp", "short_from_long"])
    if what == "hyp":
        return Q(f"In a 30°-60°-90° triangle, the shorter leg is {s}. Find the hypotenuse.", str(2 * s), ["hypotenuse = 2 × shorter leg.", f"= 2 × {s} = {2 * s}."],
                 [f"{s}√3", f"{s}√2", str(s + 2)], V(f"2*{s}"), why=["Found the longer leg", "Used the 45°-45°-90° ratio", ""])
    if what == "long":
        return Q(f"In a 30°-60°-90° triangle, the shorter leg is {s}. Find the longer leg.", f"{s}√3", ["longer leg = shorter leg × √3.", f"= {s}√3."],
                 [str(2 * s), f"{s}√2", f"{2 * s}√3"], V(f"{s}√3"), why=["Found the hypotenuse", "Used the 45°-45°-90° ratio", "Doubled before multiplying by √3"])
    if what == "short_from_hyp":
        return Q(f"In a 30°-60°-90° triangle, the hypotenuse is {2 * s}. Find the longer leg.", f"{s}√3", [f"shorter leg = {2 * s} ÷ 2 = {s}.", f"longer leg = {s}√3."],
                 [f"{2 * s}√3", str(s), f"{s}√2"], V(f"{s}√3"), why=["Multiplied the hypotenuse by √3", "Gave the shorter leg", "Used the 45°-45°-90° ratio"], tags=["multistep"])
    return Q(f"In a 30°-60°-90° triangle, the longer leg is {s}√3. Find the hypotenuse.", str(2 * s), [f"shorter leg = {s}√3 ÷ √3 = {s}.", f"hypotenuse = 2 × {s} = {2 * s}."],
             [f"{2 * s}√3", str(s), f"{s}√2"], V(f"2*{s}"), why=["Doubled the longer leg", "Gave the shorter leg", "Used the 45°-45°-90° ratio"], tags=["multistep"])


# ============================================================== S6 Trig ratios
@fam("012")
def s6_ratio(r, L):
    a, b, c = pick(r, TRIPLES)
    fn = pick(r, ["sin", "cos", "tan"])
    v = {"sin": F(a, c), "cos": F(b, c), "tan": F(a, b)}[fn]
    return Q(f"In right triangle ABC, ∠C is the right angle, BC = {a}, AC = {b}, and AB = {c}. Find {fn} A as a fraction in simplest form.", N(v),
             [f"For ∠A: opposite = BC = {a}, adjacent = AC = {b}, hypotenuse = AB = {c}.", {"sin": "sin = opposite ÷ hypotenuse.", "cos": "cos = adjacent ÷ hypotenuse.", "tan": "tan = opposite ÷ adjacent."}[fn],
              f"{fn} A = {N(v)}."], [N(1 / v), N({"sin": F(b, c), "cos": F(a, c), "tan": F(b, a)}[fn]), N({"sin": F(a, b), "cos": F(b, a), "tan": F(a, c)}[fn])],
             PY("trig_ratio", f=fn, opp=a, adj=b, hyp=c), why=["Flipped the ratio", "Used the sides for angle B instead of angle A", "Used the wrong pair of sides"],
             diagram={"alt": f"Right triangle ABC with right angle at C. BC = {a} (opposite A), AC = {b} (adjacent to A), AB = {c}.",
                      "draw": poly_draw([(0, 0), (b, 0), (b, a)], side_labels=[(0, str(b)), (1, str(a)), (2, str(c))], vert_labels=[(0, "A"), (1, "C"), (2, "B")], right_angles=[1])} if L == 0 else None)


@fam("12")
def s6_side(r, L):
    ang = r.randint(15, 75)
    h = r.randint(5, 40)
    fn = pick(r, ["sin", "cos", "tan"])
    if fn == "tan":
        t = f"In a right triangle, an acute angle measures {ang}° and the side adjacent to it is {h} m. Find the side opposite the angle, to the nearest tenth."
        v = h * math.tan(math.radians(ang))
        st = [f"tan {ang}° = opposite ÷ adjacent.", f"opposite = {h} × tan {ang}°.", f"≈ {Rd(v, 1)} m."]
    else:
        t = f"In a right triangle, an acute angle measures {ang}° and the hypotenuse is {h} m. Find the side {'opposite' if fn == 'sin' else 'adjacent to'} the angle, to the nearest tenth."
        v = h * (math.sin if fn == "sin" else math.cos)(math.radians(ang))
        st = [f"{fn} {ang}° = {'opposite' if fn == 'sin' else 'adjacent'} ÷ hypotenuse.", f"side = {h} × {fn} {ang}°.", f"≈ {Rd(v, 1)} m."]
    other = {"sin": math.cos, "cos": math.sin, "tan": lambda x: 1 / math.tan(x)}[fn]
    return Q(t, f"{Rd(v, 1)} m", st, [f"{Rd(h * other(math.radians(ang)), 1)} m", f"{Rd(h / (math.sin if fn == 'sin' else math.cos if fn == 'cos' else math.tan)(math.radians(ang)), 1)} m", f"{Rd(v + 1, 1)} m"],
             PY("trig_side", f=fn, ang=ang, known=h, mode="mult"), why=["Used the wrong trig ratio", "Divided instead of multiplying", ""])


@fam("012", mode="mc")
def s6_which(r, L):
    fn = pick(r, ["sine", "cosine", "tangent"])
    d = {"sine": "opposite ÷ hypotenuse", "cosine": "adjacent ÷ hypotenuse", "tangent": "opposite ÷ adjacent"}
    opts = [(d[fn], True)] + [(d[x], False) for x in d if x != fn] + [("hypotenuse ÷ opposite", False)]
    r.shuffle(opts)
    return Q(f"For an acute angle in a right triangle, which ratio defines the {fn}?", d[fn], ["SOH-CAH-TOA.", f"{fn} = {d[fn]}."], options=opts, chk=TXT(d[fn]), mode="mc")


# ============================================================== S7 Angles of Elevation and Depression
@fam("012")
def s7_height(r, L):
    ang = r.randint(20, 70)
    d = r.randint(10, 200)
    eye = r.randint(4, 6) if L == 2 else 0
    v = d * math.tan(math.radians(ang)) + eye
    extra = f" {name(r)}'s eyes are {eye} ft above the ground." if eye else ""
    return Q(f"From a point {d} ft from the base of a building, the angle of elevation to the top is {ang}°.{extra} How tall is the building, to the nearest foot?", f"{Rd(v, 0)} feet",
             ["Draw a right triangle: the horizontal distance is adjacent to the angle; the height is opposite.", f"tan {ang}° = h ÷ {d}.", f"h = {d} × tan {ang}° ≈ {Rd(v - eye, 1)}." + (f" Add {eye} ft for eye level." if eye else ""), f"≈ {Rd(v, 0)} feet."],
             [f"{Rd(d * math.sin(math.radians(ang)) + eye, 0)} feet", f"{Rd(d / math.tan(math.radians(ang)) + eye, 0)} feet", f"{Rd(v - eye, 0) if eye else Rd(d * math.cos(math.radians(ang)), 0)} feet"],
             PY("trig_side", f="tan", ang=ang, known=d, mode="mult", add=eye, places=0), why=["Used sine instead of tangent", "Divided instead of multiplying", "Forgot the eye height" if eye else "Used cosine"],
             tags=["modeling"])


@fam("012")
def s7_depression(r, L):
    ang = r.randint(10, 60)
    h = r.randint(20, 300)
    v = h / math.tan(math.radians(ang))
    return Q(f"From the top of a {h}-ft lighthouse, the angle of depression to a boat is {ang}°. How far is the boat from the base of the lighthouse, to the nearest foot?", f"{Rd(v, 0)} feet",
             ["The angle of depression equals the angle of elevation from the boat (alternate interior angles).", f"tan {ang}° = {h} ÷ d.", f"d = {h} ÷ tan {ang}°.", f"≈ {Rd(v, 0)} feet."],
             [f"{Rd(h * math.tan(math.radians(ang)), 0)} feet", f"{Rd(h / math.sin(math.radians(ang)), 0)} feet", f"{Rd(h * math.cos(math.radians(ang)), 0)} feet"],
             PY("trig_side", f="tan", ang=ang, known=h, mode="div", places=0), why=["Multiplied instead of dividing", "Found the line-of-sight distance", "Used cosine"], tags=["modeling"])


@fam("12")
def s7_angle(r, L):
    a, b, c = pick(r, TRIPLES)
    ang = math.degrees(math.atan2(a, b))
    return Q(f"A ramp rises {a} ft over a horizontal distance of {b} ft. What is its angle of elevation, to the nearest degree?", f"{Rd(ang, 0)}°",
             ["tan θ = rise ÷ run.", f"tan θ = {a} ÷ {b}.", f"θ = tan⁻¹({a} ÷ {b}) ≈ {Rd(ang, 0)}°." if False else f"Use the inverse tangent key: θ ≈ {Rd(ang, 0)}°."],
             [f"{Rd(90 - ang, 0)}°", f"{Rd(math.degrees(math.asin(min(1, a / c))) + 3, 0)}°", f"{Rd(a / b * 100, 0)}°"], PY("trig_angle", opp=a, adj=b), why=["Found the other acute angle", "", "Used the slope as degrees"],
             tags=["modeling"])


SKILLS = {
    1: dict(name="Square Roots and Irrational Numbers", std=["8.EE.A.2", "8.NS.A.2"], fams=[s1_eval, s1_estimate, s1_classify, s1_simplify], extra=[err_of(s1_eval), open_of(s1_eval)]),
    2: dict(name="The Pythagorean Theorem", std=["8.G.B.7", "8.G.B.6"], fams=[s2_hyp, s2_converse, s2_context], extra=[err_of(s2_hyp), open_of(s2_hyp), select_of(s2_hyp)]),
    3: dict(name="Distance and Midpoint Formulas", std=["8.G.B.8", "G-GPE.B.7"], fams=[s3_distance, s3_midpoint], extra=[err_of(s3_distance), open_of(s3_midpoint), select_of(s3_midpoint)]),
    4: dict(name="Write a Proportion", std=["7.RP.A.2c", "7.RP.A.3"], fams=[s4_shadow, s4_rate], extra=[err_of(s4_shadow), open_of(s4_rate)]),
    5: dict(name="Special Right Triangles", std=["G-SRT.C.6", "8.G.B.7"], fams=[s5_45, s5_30], extra=[err_of(s5_45), open_of(s5_30), err_of(s5_30)]),
    6: dict(name="Sine, Cosine, and Tangent Ratios", std=["G-SRT.C.6", "G-SRT.C.8"], fams=[s6_ratio, s6_side, s6_which], extra=[err_of(s6_ratio), open_of(s6_ratio)]),
    7: dict(name="Angles of Elevation and Depression", std=["G-SRT.C.8"], fams=[s7_height, s7_depression, s7_angle], extra=[err_of(s7_height), open_of(s7_depression)]),
}
