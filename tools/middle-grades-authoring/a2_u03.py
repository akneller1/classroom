"""Algebra 2 Unit 3 — Quadratic Functions and Complex Numbers (quadratic-functions-complex-numbers). Top-up families."""
from hslib import *
import math
import pc_u02 as F2
import pc_u07 as V7
import ca_u01 as CA1

UNIT_ID = "quadratic-functions-complex-numbers"
ABBR = "qc"
cx = V7.cx
I = sp.I


def ri(r, a, b):
    return rint(r, a, b, True)


def sroot(p, d, q, sg):
    """Text of (p + sg·√d)/q in classroom form: 5 + √7, (-1 - √21)/2, -3 + 2√5."""
    sq = sp.sqrt(d)
    if sq.is_Integer:
        return T(sp.Rational(p + sg * int(sq), q))
    c, m = sq.as_coeff_Mul()
    c, m = int(c), int(m ** 2)
    if q < 0:
        p, q, sg = -p, -q, -sg
    g = math.gcd(math.gcd(abs(p), c), q)
    p, c, q = p // g, c // g, q // g
    rad = ("" if c == 1 else str(c)) + f"√{m}"
    body = (f"{p} {'+' if sg > 0 else '-'} {rad}" if p else ("" if sg > 0 else "-") + rad)
    return body if q == 1 else f"({body})/{q}"


def sroots(p, d, q):
    return " or ".join(f"x = {sroot(p, d, q, sg)}" for sg in (-1, 1))


def vform(a, h_, k_):
    s = "" if a == 1 else "-" if a == -1 else T(sp.nsimplify(a)) if sp.nsimplify(a).q == 1 else f"({T(sp.nsimplify(a))})"
    inner = "x" if h_ == 0 else f"(x {'-' if h_ > 0 else '+'} {T(abs(h_))})"
    body = f"{s}{inner}²" if inner != "x" else f"{s}x²"
    return body + ("" if k_ == 0 else f" {'+' if k_ > 0 else '-'} {T(abs(k_))}")


# ============================================================== S1 Graphing quadratic functions
@fam("012")
def s1_vertex(r, L):
    a = ri(r, -3, 3) if L else pick(r, [1, -1, 2])
    h_, k_ = rint(r, -6, 6), rint(r, -9, 9)
    if L == 0:
        need(a == 1 or True)
    f = sp.expand(a * (x - h_) ** 2 + k_)
    ans = f"({h_}, {k_})"
    b = f.coeff(x, 1)
    wr = [f"({-h_}, {k_})" if h_ else f"({h_}, {-k_})", f"({h_}, {T(f.subs(x, 0))})", f"({T(sp.Rational(-b, a))}, {T(f.subs(x, -b / a))})" if b else f"({k_}, {h_})"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Find the vertex of the parabola y = {T(f)}.", ans,
             [f"x = -b/(2a) = -({T(b)})/(2·{par(a)}) = {h_}.", f"y = {T(f.subs(x, h_))} when x = {h_}.", f"Vertex: {ans}."],
             wr, H(f"(lambda F: (solve(diff(F, x), x)[0], F.subs(x, solve(diff(F, x), x)[0])))(P('{T(f)}'))", "point"),
             why=["Forgot the negative sign in -b/(2a)", "Used the y-intercept as the y-coordinate", "Used -b/a instead of -b/(2a)"])


@fam("012")
def s1_features(r, L):
    a = ri(r, -3, 3)
    h_, k_ = rint(r, -6, 6), rint(r, -9, 9)
    f = sp.expand(a * (x - h_) ** 2 + k_)
    ask = pick(r, ["axis", "extreme", "yint"] if L else ["axis", "yint"])
    if ask == "axis":
        ans, code = f"x = {h_}", f"Eq(x, solve(diff(P('{T(f)}'), x)[0])).rhs"
        wr = [f"x = {-h_}" if h_ else "x = 1", f"y = {k_}", f"x = {k_}" if k_ != h_ else f"x = {h_ + 1}"]
        why = ["Forgot the negative sign in -b/(2a)", "Gave a horizontal line through the vertex", "Used the y-coordinate of the vertex"]
        q = f"Find the axis of symmetry of y = {T(f)}."
        st = [f"x = -b/(2a) = {h_}.", f"The axis of symmetry is {ans}."]
        chk = H(f"solve(diff(P('{T(f)}'), x), x)", "set")
    elif ask == "extreme":
        kind = "minimum" if a > 0 else "maximum"
        ans = str(k_)
        wr = [str(h_) if h_ != k_ else str(k_ + 1), str(-k_) if k_ else "1", T(f.subs(x, 0)) if f.subs(x, 0) != k_ else str(k_ - 1)]
        why = ["Gave the x-coordinate of the vertex", "Made a sign error", "Gave the y-intercept"]
        q = f"Does y = {T(f)} have a maximum or a minimum? Find that {kind} value."
        ans = f"{kind} {k_}"
        wr = [f"{kind} {w}" for w in wr]
        st = [f"a = {a} {'> 0, so the parabola opens up and has a minimum' if a > 0 else '< 0, so the parabola opens down and has a maximum'}.", f"The vertex is ({h_}, {k_}).", f"The {kind} value is {k_}."]
        chk = PY("extreme_word", expr=T(f))
    else:
        ans = f"(0, {T(f.subs(x, 0))})"
        wr = [f"({T(f.subs(x, 0))}, 0)", f"(0, {k_})" if k_ != f.subs(x, 0) else f"(0, {k_ + 1})", f"(0, {a})" if a != f.subs(x, 0) else "(0, 0)"]
        why = ["Switched the coordinates", "Used the vertex's y-coordinate", "Used the leading coefficient"]
        q = f"Find the y-intercept of y = {T(f)}."
        st = ["Set x = 0.", f"y = {T(f.subs(x, 0))}.", f"The y-intercept is {ans}."]
        chk = H(f"(0, P('{T(f)}').subs(x, 0))", "point")
    need(len(set(wr) | {ans}) == 4)
    return Q(q, ans, st, wr, chk, why=why)


# ============================================================== S2 Vertex and intercept forms
@fam("012")
def s2_to_vertex(r, L):
    a = 1 if L == 0 else pick(r, [1, 2, -1, 3, -2]) if L == 1 else pick(r, [2, -2, 3, -3, sp.Rational(1, 2)])
    h_ = rint(r, -6, 6) if (L < 2 or a == sp.Rational(1, 2)) else rint(r, -6, 6)
    k_ = rint(r, -12, 12)
    f = sp.expand(a * (x - h_) ** 2 + k_)
    need(all(c.q == 1 for c in sp.Poly(f, x).all_coeffs()))
    ans = "y = " + vform(a, h_, k_)
    wr = ["y = " + vform(a, -h_, k_) if h_ else "y = " + vform(a, h_, -k_ if k_ else 1), "y = " + vform(a, h_, f.subs(x, 0)) if f.subs(x, 0) != k_ else "y = " + vform(a, h_, k_ + a),
          "y = " + vform(1, h_, k_) if a != 1 else "y = " + vform(a, h_, k_ - h_ * h_ if h_ else k_ + 2)]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Write y = {T(f)} in vertex form y = a(x - h)² + k.", ans,
             [f"Factor {par(a)} from the x-terms if needed and complete the square.", f"h = -b/(2a) = {h_}, and k = y({h_}) = {k_}.", f"{ans}."],
             wr, H(f"y - P('{T(f)}')", "eqn"),
             why=["Used the wrong sign for h inside the parentheses", "Used the constant term as k", "Dropped the leading coefficient" if a != 1 else "Did not subtract the square that was added"])


@fam("012")
def s2_from_roots(r, L):
    p_, q_ = sorted(r.sample(range(-8, 9), 2))
    a = 1 if L == 0 else ri(r, -3, 3)
    if L == 0:
        f = sp.expand((x - p_) * (x - q_))
        q = f"Write a quadratic function in standard form with leading coefficient 1 and x-intercepts {p_} and {q_}."
    else:
        px = pick(r, [v for v in range(-6, 7) if v not in (p_, q_)])
        py = a * (px - p_) * (px - q_)
        f = sp.expand(a * (x - p_) * (x - q_))
        q = f"A parabola has x-intercepts {p_} and {q_} and passes through ({px}, {py}). Write its equation in standard form."
    ans = "y = " + T(f)
    wr = ["y = " + T(sp.expand((f.coeff(x, 2)) * (x + p_) * (x + q_))), "y = " + T(sp.expand(x ** 2 - (p_ + q_) * x - p_ * q_)), "y = " + T(sp.expand((x - p_) * (x - q_))) if a != 1 else "y = " + T(sp.expand(2 * (x - p_) * (x - q_)))]
    need(len(set(wr) | {ans}) == 4)
    return Q(q, ans,
             [f"Intercept form: y = a(x - {par(p_)})(x - {par(q_)}).".replace("- (-", "+ (").replace("(x + (", "(x + ").replace("))", ")"), "Find a from the extra point (or use a = 1)." if L else "a = 1.", f"Expand: {ans}."],
             wr, H(f"y - P('{T(f)}')", "eqn"),
             why=["Used factors (x + r) instead of (x - r)", "Made a sign error in the constant term", "Ignored the given point when finding a" if a != 1 else "Used the wrong leading coefficient"])


# ============================================================== S4 Square roots and completing the square
@fam("012")
def s4_sqrt(r, L):
    a = 1 if L == 0 else pick(r, [1, 2, 3, 4])
    h_ = rint(r, -7, 7)
    sq = pick(r, [1, 4, 9, 16, 25, 36, 49]) if L == 0 else pick(r, [2, 3, 5, 6, 7, 8, 12, 18, 20, 27, 4, 9])
    c = a * sq + (0 if L < 2 else rint(r, -9, 9))
    k_ = c - a * sq
    lhs = (f"{a if a != 1 else ''}(x {'-' if h_ > 0 else '+'} {abs(h_)})²" if h_ else f"{a if a != 1 else ''}x²") + (f" {'+' if k_ > 0 else '-'} {abs(k_)}" if k_ else "")
    lhs = lhs.replace("+ -", "- ")
    ans = sroots(h_, sq, 1)
    wr = [f"x = {sroot(h_, sq, 1, 1)}", sroots(-h_, sq, 1) if h_ else f"x = {T(sq)} or x = {T(-sq)}",
          " or ".join(f"x = {T(h_ + s_)}" for s_ in (sq, -sq)) if sq != 1 else f"x = {h_ + 2} or x = {h_ - 2}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve by taking square roots: {lhs} = {c}. Give exact answers.", ans,
             [f"Isolate the square: (x {'-' if h_ >= 0 else '+'} {abs(h_)})² = {sq}." if h_ else f"Isolate x²: x² = {sq}.", f"Take both square roots: x {'-' if h_ >= 0 else '+'} {abs(h_)} = ±{T(sp.sqrt(sq))}.".replace("x - 0", "x"), f"{ans}."],
             wr, H(f"solve(Eq(P('{lhs}'), {c}), x)", "set"),
             why=["Forgot the negative square root", "Used the wrong sign for the shift", "Did not take the square root"])


@fam("12")
def s4_complete(r, L):
    p_ = ri(r, -6, 6)
    m = pick(r, [2, 3, 5, 6, 7, 10, 11, 13])
    c = p_ * p_ - m
    f = x ** 2 + 2 * p_ * x + c
    ans = sroots(-p_, m, 1)
    wr = [sroots(p_, m, 1), sroots(-p_, -c if c < 0 else c + 1, 1), f"x = {sroot(-p_, m, 1, 1)}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Solve {T(f)} = 0 by completing the square. Give exact answers.", ans,
             [f"Move the constant: x² {'+' if p_ > 0 else '-'} {abs(2 * p_)}x = {-c}.", f"Add ({T(sp.Rational(2 * p_, 2))})² = {p_ * p_} to both sides: (x {'+' if p_ > 0 else '-'} {abs(p_)})² = {m}.", f"x = {-p_} ± √{m}.", f"{ans}."],
             wr, H(f"solve(P('{T(f)}'), x)", "set"),
             why=["Used the wrong sign for the shift", "Forgot to add the completing number to both sides", "Forgot the negative square root"])


# ============================================================== S5 Quadratic formula and discriminant
@fam("012")
def s5_disc(r, L):
    a, b = ri(r, -5, 5), rint(r, -9, 9)
    kind = pick(r, ["two", "one", "none"])
    if kind == "one":
        need(b % 2 == 0 and (b * b) % (4 * a) == 0)
        c = sp.Rational(b * b, 4 * a)
    elif kind == "two":
        c = rint(r, -9, 9)
        need(b * b - 4 * a * c > 0)
    else:
        c = rint(r, -9, 9)
        need(b * b - 4 * a * c < 0)
    f = a * x ** 2 + b * x + c
    D_ = b * b - 4 * a * c
    ans = {"two": "two real solutions", "one": "one real solution", "none": "two complex (non-real) solutions"}[kind]
    others = [v for v in ["two real solutions", "one real solution", "two complex (non-real) solutions"] if v != ans] + ["no solutions of any kind"]
    whys = {"two real solutions": "Thought any nonzero discriminant gives two real solutions", "one real solution": "Mixed up the discriminant cases",
            "two complex (non-real) solutions": "Made a sign error computing b² - 4ac", "no solutions of any kind": "Thought a negative discriminant means no solutions at all"}
    return Q(f"Use the discriminant to describe the solutions of {T(f)} = 0.", ans,
             [f"b² - 4ac = {par(b)}² - 4({a})({par(c)}) = {D_}.", f"{'Positive' if D_ > 0 else 'Zero' if D_ == 0 else 'Negative'} discriminant → {ans}."],
             others, PY("disc_word", expr=T(f)), why=[whys[o] for o in others])


@fam("012")
def s5_formula(r, L):
    a = 1 if L == 0 else pick(r, [1, 2, 3, -1, 2])
    b, c = rint(r, -9, 9), rint(r, -12, 12)
    D_ = b * b - 4 * a * c
    need(D_ > 0 and sp.sqrt(D_).is_Integer is False if L else D_ > 0 and not sp.sqrt(D_).is_Integer)
    f = a * x ** 2 + b * x + c
    ans = sroots(-b, D_, 2 * a)
    wr = [sroots(b, D_, 2 * a), sroots(-b, b * b + 4 * a * c, 2 * a) if b * b + 4 * a * c > 0 else "no real solution",
          " or ".join(f"x = {T(sp.radsimp(-b + sg * sp.sqrt(D_) / (2 * a)))}" for sg in (-1, 1))]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Use the quadratic formula to solve {T(f)} = 0. Give exact answers.", ans,
             ["x = (-b ± √(b² - 4ac))/(2a).", f"b² - 4ac = {D_}.", f"x = ({T(-b)} ± √{D_})/{2 * a}.", f"{ans}."],
             wr, H(f"solve(P('{T(f)}'), x)", "set"),
             why=["Used b instead of -b", "Made a sign error in -4ac", "Divided only the square root by 2a"])


# ============================================================== S6 Complex numbers
@fam("012")
def s6_ipow(r, L):
    n_ = rint(r, 5, 60) if L else rint(r, 2, 12)
    c = ri(r, -5, 5) if L == 2 else 1
    v = c * I ** n_
    ans = cx(v)
    rem = n_ % 4
    wr = [cx(-v), cx(c * I ** (n_ + 1)) if cx(c * I ** (n_ + 1)) != cx(-v) else cx(c * I ** (n_ + 3)), cx(c * n_) if c * n_ not in (v, -v) else cx(c * n_ + 1)]
    need(len(set(wr) | {ans}) == 4)
    term = f"i{str(n_).translate(SUP)}" if c == 1 else f"{c}i{str(n_).translate(SUP)}"
    return Q(f"Simplify {term}.", ans, [f"Powers of i repeat every 4: i¹ = i, i² = -1, i³ = -i, i⁴ = 1.", f"{n_} ÷ 4 leaves remainder {rem}, so i{str(n_).translate(SUP)} = i{str(rem).translate(SUP) if rem else '⁰'} = {cx(I ** rem)}.", f"{term} = {ans}."],
             wr, H(f"P('{term}')" if c == 1 else f"{c}*I**{n_}"), why=["Made a sign error in the cycle", "Used the wrong remainder", "Multiplied by the exponent"])


@fam("012")
def s6_sqrt_neg(r, L):
    a = pick(r, [4, 9, 16, 25, 36, 49, 64, 81, 100]) if L == 0 else pick(r, [8, 12, 18, 20, 27, 28, 32, 45, 50, 72])
    v = sp.sqrt(-a)
    if L == 2:
        b = pick(r, [2, 3, 5, 8, 12, 18])
        v = sp.expand(sp.sqrt(-a) * sp.sqrt(-b))
        need(sp.sqrt(a * b).is_Integer or True)
        txt = f"√-{a} · √-{b}"
        ans = T(v)
        wr = [T(sp.sqrt(a * b)), cx(sp.sqrt(a * b) * I), cx(-sp.sqrt(a * b) * I)]
        why = ["Multiplied under one radical first, which is not allowed with negative radicands", "Kept an i from only one factor", "Made a sign error with i²"]
        st = [f"√-{a} = i√{a} and √-{b} = i√{b}.", f"(i√{a})(i√{b}) = i²√{a * b} = {ans}."]
        code = f"(I*sqrt({a}))*(I*sqrt({b}))"
    else:
        txt = f"√-{a}"
        ans = cx(v)
        wr = [T(-sp.sqrt(a)), T(sp.sqrt(a)), cx(a * I)]
        why = ["Wrote √-a as -√a", "Dropped the i", "Did not take the square root"]
        st = ["√-a = i√a for a > 0.", f"√-{a} = i√{a} = {ans}."]
        code = f"sqrt(-{a})"
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Simplify {txt}.", ans, st, wr, H(code), why=why)


# ============================================================== S8 Quadratic modeling
@fam("012")
def s8_projectile(r, L):
    t1 = pick(r, [1, 2, 3, 4, 5]) if L < 2 else pick(r, [sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(5, 2), 1, 2, 3])
    v0 = 32 * t1
    h0 = pick(r, [0, 4, 6, 16, 20, 48, 64, 80])
    hmax = h0 + 16 * t1 ** 2
    f = f"h(t) = -16t² + {T(v0)}t" + (f" + {h0}" if h0 else "")
    ask = pick(r, ["time", "height"] if L < 2 else ["height", "ground"])
    if ask == "ground":
        disc = v0 * v0 + 64 * h0
        tg = (v0 + sp.sqrt(disc)) / 32
        need(sp.nsimplify(tg).is_Rational)
        return Q(f"A ball is launched upward. Its height in feet after t seconds is {f}. When does it hit the ground?", f"{T(sp.nsimplify(tg))} seconds",
                 [f"Set h(t) = 0: -16t² + {T(v0)}t + {h0} = 0.", "Solve with the quadratic formula and keep the positive root.", f"t = {T(sp.nsimplify(tg))} seconds."],
                 [f"{T(t1)} seconds", f"{T(2 * t1)} seconds", f"{T(sp.nsimplify((v0 - sp.sqrt(disc)) / -32))} seconds" if h0 else f"{T(t1 + 1)} seconds"],
                 H(f"max(solve(P('{f[6:]}'.replace('t', 'x')), x))"), why=["Gave the time of the maximum height", "Doubled the time to the top even though it started above the ground", "Kept the negative root's size"], tags=["modeling"])
    if ask == "time":
        return Q(f"A ball is launched upward. Its height in feet after t seconds is {f}. After how many seconds does it reach its maximum height?", f"{T(t1)} seconds",
                 [f"The maximum is at the vertex: t = -b/(2a) = -{T(v0)}/(2·(-16)).", f"t = {T(t1)}."],
                 [f"{T(2 * t1)} seconds", f"{T(sp.Rational(v0, 16))} seconds" if v0 != 32 * t1 * 2 else "1 seconds", f"{T(hmax)} seconds"],
                 H(f"solve(diff(P('{f[6:]}'.replace('t', 'x')), x), x)[0]"), why=["Gave the time it would return to the launch height", "Used -b/a instead of -b/(2a)", "Gave the maximum height"], tags=["modeling"])
    return Q(f"A ball is launched upward. Its height in feet after t seconds is {f}. What is its maximum height?", f"{T(hmax)} feet",
             [f"Vertex time: t = -{T(v0)}/(2·(-16)) = {T(t1)}.", f"h({T(t1)}) = -16({T(t1)})² + {T(v0)}({T(t1)})" + (f" + {h0}" if h0 else "") + f" = {T(hmax)}."],
             [f"{T(t1)} feet", f"{T(v0 * t1 + h0)} feet", f"{T(hmax - h0)} feet" if h0 else f"{T(hmax * 2)} feet"],
             H(f"(lambda F: F.subs(x, solve(diff(F, x), x)[0]))(P('{f[6:]}'.replace('t', 'x')))"), why=["Gave the time instead of the height", "Ignored the -16t² term", "Forgot the starting height" if h0 else "Doubled the height"], tags=["modeling"])


@fam("012")
def s8_rect(r, L):
    w = rint(r, 3, 15)
    d = rint(r, 2, 9)
    l = w + d
    A = w * l
    item = pick(r, ["garden", "patio", "poster", "rug", "pool cover"])
    return Q(f"A rectangular {item} is {d} feet longer than it is wide, and its area is {A} square feet. Find its width.", f"{w} feet",
             [f"Let w be the width: w(w + {d}) = {A}.", f"w² + {d}w - {A} = 0 → (w - {w})(w + {w + d}) = 0.", f"Width cannot be negative, so w = {w} feet."],
             [f"{l} feet", f"{-(w + d)} feet", f"{T(sp.sqrt(A).evalf(3)) if not sp.sqrt(A).is_Integer else sp.sqrt(A) + 1} feet"],
             H(f"[s_ for s_ in solve(x*(x + {d}) - {A}, x) if s_ > 0][0]"), why=["Gave the length instead of the width", "Kept the negative solution", "Took the square root of the area"], tags=["modeling"])


rr = lambda f, lv=(0, 0, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Graphing quadratic functions", fams=[s1_vertex, s1_features], extra=[err_of(s1_vertex), err_of(s1_features), open_of(s1_vertex)]),
    2: dict(name="Vertex and intercept forms", fams=[s2_to_vertex, s2_from_roots], extra=[err_of(s2_to_vertex), err_of(s2_from_roots), open_of(s2_to_vertex)]),
    3: dict(name="Factoring quadratic expressions", fams=[rr(CA1.s1_factor, (0, 0, 1))], extra=[err_of(rr(CA1.s1_factor, (0, 0, 1), "e")), open_of(rr(CA1.s1_factor, (0, 0, 1), "o")), select_of(rr(CA1.s1_factor, (0, 0, 1), "s"))]),
    4: dict(name="Solving by square roots and completing the square", fams=[s4_sqrt, s4_complete], extra=[err_of(s4_sqrt), err_of(s4_complete), open_of(s4_sqrt)]),
    5: dict(name="Quadratic formula and discriminant", fams=[s5_formula, s5_disc, rr(F2.s11_quad, (0, 0, 1))], extra=[err_of(s5_formula), err_of(s5_disc), open_of(s5_formula)]),
    6: dict(name="Complex numbers and arithmetic", fams=[rr(V7.s1_ops, (0, 1, 2)), s6_ipow, s6_sqrt_neg], extra=[err_of(rr(V7.s1_ops, (0, 1, 2), "e")), err_of(s6_ipow), open_of(rr(V7.s1_ops, (0, 1, 2), "o")), select_of(s6_ipow)]),
    7: dict(name="Quadratic equations with complex solutions", fams=[rr(V7.s1_quad, (0, 1, 2))], extra=[err_of(rr(V7.s1_quad, (0, 1, 2), "e")), open_of(rr(V7.s1_quad, (0, 1, 2), "o"))]),
    8: dict(name="Quadratic modeling applications", fams=[s8_projectile, s8_rect], extra=[err_of(s8_projectile), err_of(s8_rect), open_of(s8_rect)]),
}
