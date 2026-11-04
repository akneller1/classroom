"""Precalculus Unit 3 — Conics (conics)."""
from hslib import *
import re

UNIT_ID = "conics"
ABBR = "con"

X, Y = x, y


def sq(var, c):
    """(x - c)² text, x² when c = 0."""
    return f"{var}²" if c == 0 else f"({var} {'-' if c > 0 else '+'} {abs(c)})²"


def hk(r, lo=-5, hi=5):
    return rint(r, lo, hi), rint(r, lo, hi)


def win(h, k, ext):
    e = max(6, int(math.ceil(ext)) + 2)
    lo_x, hi_x = min(-2, h - e), max(2, h + e)
    lo_y, hi_y = min(-2, k - e), max(2, k + e)
    s = max(hi_x - lo_x, hi_y - lo_y)
    return (lo_x, lo_x + s), (lo_y, lo_y + s)


# ============================================================== S1 Circles
@fam("012")
def s1_read(r, L):
    h, k = hk(r)
    rad = rint(r, 2, 7)
    if L < 2:
        st = f"{sq('x', h)} + {sq('y', k)} = {rad ** 2}"
    else:
        D_, E_, F_ = -2 * h, -2 * k, h * h + k * k - rad * rad
        st = T(x ** 2 + y ** 2 + D_ * x + E_ * y + F_) + " = 0"
    ask = pick(r, ["center", "radius"]) if L else "center"
    if ask == "center":
        return Q(f"Find the center of the circle {st}.", f"({h}, {k})", (["Complete the square in x and in y."] if L == 2 else []) + ["Standard form: (x - h)² + (y - k)² = r².", f"Center (h, k) = ({h}, {k})."],
                 [f"({-h}, {-k})" if (h or k) else "(1, 1)", f"({k}, {h})" if h != k else f"({h}, {-k})", f"({h}, {-k})" if k else f"({-h}, {k})"], H(f"[{h}, {k}]", "point") if L < 2 else H(f"(lambda E: [-diff(E, x).subs({{x: 0, y: 0}})/2, -diff(E, y).subs({{x: 0, y: 0}})/2])(P('{st.split(' = ')[0]}'))", "point"),
                 why=["Used the signs shown in the equation", "Switched x and y", "Made a sign error on one coordinate"], diagram=None)
    return Q(f"Find the radius of the circle {st}.", str(rad), (["Complete the square in x and in y."] if L == 2 else []) + [f"r² = {rad ** 2}.", f"r = {rad}."],
             [str(rad ** 2), str(2 * rad), str(rad * rad // 2) if rad * rad // 2 != rad else str(rad + 1)], H(f"(lambda E: sqrt(diff(E, x).subs({{x: 0, y: 0}})**2/4 + diff(E, y).subs({{x: 0, y: 0}})**2/4 - E.subs({{x: 0, y: 0}})))(P('{st.split(' = ')[0]}'))" if L == 2 else f"sqrt({rad ** 2})"),
             why=["Gave r² instead of r", "Gave the diameter", "Halved r²"])


@fam("012")
def s1_write(r, L):
    h, k = hk(r)
    if L == 0 or r.random() < 0.5:
        rad = rint(r, 1, 9) if L < 2 else pick(r, [2, 3, 5, 6, 7])
        rr = rad ** 2 if L < 2 else rad
        rtxt = str(rad) if L < 2 else f"√{rad}"
        ans = f"{sq('x', h)} + {sq('y', k)} = {rr}"
        return Q(f"Write the standard-form equation of the circle with center ({h}, {k}) and radius {rtxt}.", ans, ["(x - h)² + (y - k)² = r².", f"h = {h}, k = {k}, r² = {rr}.", ans + "."],
                 [f"{sq('x', -h)} + {sq('y', -k)} = {rr}" if (h or k) else f"x² + y² = {rr + 1}", f"{sq('x', h)} + {sq('y', k)} = {rad if L < 2 else rad * rad}", f"{sq('x', -h)} + {sq('y', -k)} = {rad if L < 2 else rad * rad}" if (h or k) else f"x² + y² = {2 * rr}"],
                 H(f"(x - {h})**2 + (y - {k})**2 - {rr}", "eqn"), why=["Used the wrong signs for the center", "Used r instead of r²" if L < 2 else "Squared √r incorrectly", "Wrong signs and forgot to square r"])
    px, py = h + pick(r, [3, -3, 4, -4, 5, -5, 0]), k + pick(r, [4, -4, 3, -3, 0, 2])
    rr = (px - h) ** 2 + (py - k) ** 2
    need(rr > 0)
    ans = f"{sq('x', h)} + {sq('y', k)} = {rr}"
    return Q(f"Write the standard-form equation of the circle with center ({h}, {k}) that passes through ({px}, {py}).", ans, [f"r² = ({px} - {par(h)})² + ({py} - {par(k)})² = {rr}.", ans + "."],
             [f"{sq('x', h)} + {sq('y', k)} = {T(sp.sqrt(rr))}" if sp.sqrt(rr).is_Integer else f"{sq('x', h)} + {sq('y', k)} = √{rr}", f"{sq('x', -h)} + {sq('y', -k)} = {rr}" if (h or k) else f"x² + y² = {rr + 2}", f"{sq('x', px)} + {sq('y', py)} = {rr}"],
             H(f"(x - {h})**2 + (y - {k})**2 - (({px} - {h})**2 + ({py} - {k})**2)", "eqn"), why=["Used r instead of r²", "Used the wrong signs for the center", "Used the point as the center"])


@fam("01")
def s1_graph(r, L):
    h, k = hk(r, -4, 4)
    rad = rint(r, 2, 5)
    xr, yr = win(h, k, rad)
    ans = f"{sq('x', h)} + {sq('y', k)} = {rad * rad}"
    opts = [(ans, True), (f"{sq('x', -h)} + {sq('y', -k)} = {rad * rad}", False), (f"{sq('x', h)} + {sq('y', k)} = {rad}", False), (f"{sq('x', k)} + {sq('y', h)} = {rad * rad}", False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q("Which equation matches the circle shown?", ans, [f"Center from the graph: ({h}, {k}).", f"Radius: {rad}.", ans + "."], options=opts, chk=H(f"(x - {h})**2 + (y - {k})**2 - {rad * rad}", "eqn"), mode="mc",
             diagram={"alt": f"A circle on a coordinate grid with center ({h}, {k}) and radius {rad}.", "draw": curve_draw(conic_curves("circle", h, k, rad), xr, yr, pts=[(h, k, "")])})


# ============================================================== S2 Parabolas
@fam("012")
def s2_features(r, L):
    h, k = hk(r)
    p = sp.Rational(rint(r, -4, 4, True), 1 if L == 0 else pick(r, [1, 2]))
    vert = r.random() < 0.5
    if vert:
        st = f"{sq('x', h)} = {T(4 * p)}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}"
        focus, directrix = (h, k + p), f"y = {T(k - p)}"
    else:
        st = f"{sq('y', k)} = {T(4 * p)}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}"
        focus, directrix = (h + p, k), f"x = {T(h - p)}"
    ask = pick(r, ["vertex", "focus", "directrix"] if L else ["vertex", "focus"])
    steps = [f"4p = {T(4 * p)}, so p = {T(p)}.", f"Vertex ({h}, {k}); the parabola opens {('up' if p > 0 else 'down') if vert else ('right' if p > 0 else 'left')}."]
    if ask == "vertex":
        return Q(f"Find the vertex of the parabola {st}.", f"({h}, {k})", steps, [f"({-h}, {-k})" if (h or k) else "(1, 0)", f"({k}, {h})" if h != k else f"({h}, {k + 1})", f"({T(focus[0])}, {T(focus[1])})"],
                 H(f"[{h}, {k}]", "point"), why=["Used the signs shown in the equation", "Switched the coordinates", "Gave the focus"])
    if ask == "focus":
        wf = (h, k + 4 * p) if vert else (h + 4 * p, k)
        wd = (h, k - p) if vert else (h - p, k)
        return Q(f"Find the focus of the parabola {st}.", f"({T(focus[0])}, {T(focus[1])})", steps + [f"The focus is p = {T(p)} units from the vertex along the axis: ({T(focus[0])}, {T(focus[1])})."],
                 [f"({T(wf[0])}, {T(wf[1])})", f"({T(wd[0])}, {T(wd[1])})", f"({h}, {k})"], H(f"[{h} + {0 if vert else 1}*({4 * p})/4, {k} + {1 if vert else 0}*({4 * p})/4]", "point"),
                 why=["Used 4p instead of p", "Moved the wrong direction (toward the directrix)", "Gave the vertex"])
    wd = f"{'y' if vert else 'x'} = {T((k if vert else h) + p)}"
    return Q(f"Find the directrix of the parabola {st}.", directrix, steps + [f"The directrix is p units on the other side of the vertex: {directrix}."],
             [wd, f"{'x' if vert else 'y'} = {T((h if vert else k) - p)}", f"{'y' if vert else 'x'} = {T((k if vert else h) - 4 * p)}"], H(f"{'y' if vert else 'x'} - ({(k if vert else h)} - ({4 * p})/4)", "eqn"),
             why=["Put the directrix on the focus side", "Used the wrong variable", "Used 4p instead of p"])


@fam("012")
def s2_write(r, L):
    h, k = hk(r)
    p = rint(r, -3, 3, True)
    vert = r.random() < 0.5
    if vert:
        f_, d_ = (h, k + p), f"y = {k - p}"
        ans = f"{sq('x', h)} = {4 * p}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}"
        expr = (x - h) ** 2 - 4 * p * (y - k)
        w = [f"{sq('x', h)} = {p}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}", f"{sq('x', h)} = {-4 * p}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}",
             f"{sq('y', k)} = {4 * p}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}"]
    else:
        f_, d_ = (h + p, k), f"x = {h - p}"
        ans = f"{sq('y', k)} = {4 * p}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}"
        expr = (y - k) ** 2 - 4 * p * (x - h)
        w = [f"{sq('y', k)} = {p}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}", f"{sq('y', k)} = {-4 * p}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}",
             f"{sq('x', h)} = {4 * p}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}"]
    w = [re.sub(r"= (-?)1([(xy])", r"= \1\2", s_) for s_ in w]
    if L == 0:
        given = f"vertex ({h}, {k}) and focus ({f_[0]}, {f_[1]})"
    elif L == 1:
        given = f"focus ({f_[0]}, {f_[1]}) and directrix {d_}"
    else:
        given = f"vertex ({h}, {k}) and directrix {d_}"
    fx_, fy_ = f_
    code = f"(x - {fx_})**2 + (y - {fy_})**2 - ({'y' if vert else 'x'} - ({(k - p) if vert else (h - p)}))**2"
    return Q(f"Write the standard-form equation of the parabola with {given}.", ans, ["A parabola is the set of points equidistant from the focus and the directrix.", f"The vertex is halfway between them: ({h}, {k}); p = {p}.",
                                                                                     "Use (x - h)² = 4p(y - k) for a vertical axis or (y - k)² = 4p(x - h) for a horizontal axis.", ans + "."],
             w, H(code, "eqn"), why=["Used p instead of 4p", "Used the wrong sign for p", "Used the wrong axis orientation"])


@fam("12")
def s2_general(r, L):
    h, k = hk(r)
    p = rint(r, -3, 3, True)
    e = sp.expand((x - h) ** 2 - 4 * p * (y - k))
    need(h != 0)
    st = T(e) + " = 0"
    st = st.replace("y²", "y²")
    return Q(f"Find the vertex of the parabola {st}.", f"({h}, {k})", ["Complete the square in x.", f"(x - {h})² = {4 * p}(y - {k})." .replace("- -", "+ "), f"Vertex: ({h}, {k})."],
             [f"({-h}, {-k})" if k else f"({-h}, 1)", f"({h}, {T(sp.expand(e).subs({x: h, y: 0}) / (4 * p))})" if True else "", f"({k}, {h})" if k != h else f"({h}, {-k})"],
             H(f"(lambda E: [solve(diff(E, x), x)[0], solve(E.subs(x, solve(diff(E, x), x)[0]), y)[0]])(P('{T(e)}'))", "point"), why=["Made sign errors", "Forgot to divide by 4p", "Switched the coordinates"])


@fam("01")
def s2_graph(r, L):
    h, k = hk(r, -4, 4)
    p = pick(r, [1, -1, sp.Rational(1, 2), sp.Rational(-1, 2)])
    vert = r.random() < 0.5
    xr, yr = win(h, k, 5)
    ans = f"{sq('x', h)} = {T(4 * p)}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}" if vert else f"{sq('y', k)} = {T(4 * p)}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}"
    w1 = ans.replace(f"= {T(4 * p)}", f"= {T(-4 * p)}")
    w2 = f"{sq('y', k)} = {T(4 * p)}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}" if vert else f"{sq('x', h)} = {T(4 * p)}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}"
    w3 = (f"{sq('x', -h)} = {T(4 * p)}{'(y - ' + str(-k) + ')' if -k > 0 else '(y + ' + str(k) + ')' if k > 0 else 'y'}" if vert else f"{sq('y', -k)} = {T(4 * p)}{'(x - ' + str(-h) + ')' if -h > 0 else '(x + ' + str(h) + ')' if h > 0 else 'x'}")
    opts = [(ans, True), (w1, False), (w2, False), (w3, False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    code = f"(x - {h})**2 - 4*({p})*(y - {k})" if vert else f"(y - {k})**2 - 4*({p})*(x - {h})"
    return Q("Which equation matches the parabola shown? The vertex is marked.", ans, [f"Vertex: ({h}, {k}).", f"It opens {('up' if p > 0 else 'down') if vert else ('right' if p > 0 else 'left')}.",
                                                                                     f"Check another point to find 4p = {T(4 * p)}."], options=opts, chk=H(code, "eqn"), mode="mc",
             diagram={"alt": f"A parabola with vertex ({h}, {k}) opening {('up' if p > 0 else 'down') if vert else ('right' if p > 0 else 'left')}, passing through ({T(h + 2) if vert else T(h + p)}, {T(k + p) if vert else T(k + 2)}).",
                      "draw": curve_draw(conic_curves("parabola", h, k, p, vertical=vert), xr, yr, pts=[(h, k, ""), ((h + 2, k + 4 / (4 * p)) if vert else (h + 4 / (4 * p), k + 2)) + ("",)])})


# ============================================================== Ellipse / hyperbola helpers
def ell_eq(h, k, A2, B2):
    """(x - h)²/A2 + (y - k)²/B2 = 1 where A2 under x."""
    return f"{sq('x', h)}/{A2} + {sq('y', k)}/{B2} = 1"


def hyp_eq(h, k, A2, B2, vertical):
    return f"{sq('y', k)}/{A2} - {sq('x', h)}/{B2} = 1" if vertical else f"{sq('x', h)}/{A2} - {sq('y', k)}/{B2} = 1"


def ell_params(r, L):
    trip = pick(r, [(5, 4, 3), (5, 3, 4), (10, 8, 6), (13, 12, 5), (13, 5, 12), (10, 6, 8), (17, 15, 8), (25, 24, 7)] if L == 0 else
                [(5, 4, 3), (5, 3, 4), (10, 8, 6), (13, 12, 5), (13, 5, 12), (3, 2, sp.sqrt(5)), (4, 2, 2 * sp.sqrt(3)), (6, 4, 2 * sp.sqrt(5)), (4, 3, sp.sqrt(7))])
    a, b, c = trip
    need(a <= 13)
    return sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)


# ============================================================== S3 Ellipse features
@fam("012")
def s3_features(r, L):
    a, b, c = ell_params(r, L)
    h, k = (0, 0) if L == 0 and r.random() < 0.4 else hk(r)
    vert = r.random() < 0.5
    A2, B2 = (b * b, a * a) if vert else (a * a, b * b)
    st = ell_eq(h, k, A2, B2)
    ask = pick(r, ["vertices", "foci", "major"])
    V = [(h, k + a), (h, k - a)] if vert else [(h + a, k), (h - a, k)]
    Fo = [(h, k + c), (h, k - c)] if vert else [(h + c, k), (h - c, k)]
    Cv = [(h + b, k), (h - b, k)] if vert else [(h, k + b), (h, k - b)]
    steps = [f"The larger denominator ({a * a}) is under {'y' if vert else 'x'}, so the major axis is {'vertical' if vert else 'horizontal'}.", f"a = {T(a)}, b = {T(b)}."]
    if ask == "vertices":
        return Q(f"Find the vertices (endpoints of the major axis) of the ellipse {st}.", pts_text(V), steps + [f"Vertices: {pts_text(V)}."],
                 [pts_text(Cv), pts_text(Fo), pts_text([(h, k + a * a), (h, k - a * a)] if vert else [(h + a * a, k), (h - a * a, k)])], H(f"{[[str(p_[0]), str(p_[1])] for p_ in V]}".replace("'", ""), "points"),
                 why=["Gave the co-vertices", "Gave the foci", "Used a² instead of a"])
    if ask == "foci":
        wc = sp.sqrt(a * a + b * b)
        return Q(f"Find the foci of the ellipse {st}.", pts_text(Fo), steps + [f"c² = a² - b² = {a * a} - {b * b} = {c * c}.", f"c = {T(c)}.", f"Foci: {pts_text(Fo)}."],
                 [pts_text([(h, k + wc), (h, k - wc)] if vert else [(h + wc, k), (h - wc, k)]), pts_text(V), pts_text([(h + c, k), (h - c, k)] if vert else [(h, k + c), (h, k - c)])],
                 H(f"[[{h} + {0 if vert else 1}*sqrt({a * a} - {b * b}), {k} + {1 if vert else 0}*sqrt({a * a} - {b * b})], [{h} - {0 if vert else 1}*sqrt({a * a} - {b * b}), {k} - {1 if vert else 0}*sqrt({a * a} - {b * b})]]", "points"),
                 why=["Used c² = a² + b² (hyperbola rule)", "Gave the vertices", "Placed the foci on the minor axis"])
    return Q(f"Find the length of the major axis of the ellipse {st}.", T(2 * a), steps + [f"Major axis length = 2a = {T(2 * a)}."], [T(a), T(2 * b), T(a * a)],
             H(f"2*sqrt(max({A2}, {B2}))"), why=["Gave a instead of 2a", "Used the minor axis", "Used a²"])


@fam("01")
def s3_graph(r, L):
    a, b, c = ell_params(r, 0)
    need(a <= 6)
    h, k = hk(r, -3, 3)
    vert = r.random() < 0.5
    A2, B2 = (b * b, a * a) if vert else (a * a, b * b)
    xr, yr = win(h, k, a)
    ans = ell_eq(h, k, A2, B2)
    opts = [(ans, True), (ell_eq(h, k, B2, A2), False), (ell_eq(-h, -k, A2, B2) if (h or k) else ell_eq(h, k, A2 + 1, B2), False), (ell_eq(h, k, b if vert else a, a if vert else b), False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q("Which equation matches the ellipse shown?", ans, [f"Center: ({h}, {k}).", f"Horizontal semi-axis {T(b if vert else a)}, vertical semi-axis {T(a if vert else b)}.", ans + "."], options=opts,
             chk=H(f"(x - {h})**2/{A2} + (y - {k})**2/{B2} - 1", "eqn"), mode="mc",
             diagram={"alt": f"An ellipse centered at ({h}, {k}) with horizontal semi-axis {T(b if vert else a)} and vertical semi-axis {T(a if vert else b)}.", "draw": curve_draw(conic_curves("ellipse", h, k, a, b, vert), xr, yr, pts=[(h, k, "")])})


# ============================================================== S4 Writing ellipse equations
@fam("012")
def s4_write(r, L):
    a, b, c = ell_params(r, L)
    h, k = (0, 0) if L == 0 and r.random() < 0.4 else hk(r)
    vert = r.random() < 0.5
    A2, B2 = (b * b, a * a) if vert else (a * a, b * b)
    ans = ell_eq(h, k, A2, B2)
    V = [(h, k + a), (h, k - a)] if vert else [(h + a, k), (h - a, k)]
    Fo = [(h, k + c), (h, k - c)] if vert else [(h + c, k), (h - c, k)]
    Cv = [(h + b, k), (h - b, k)] if vert else [(h, k + b), (h, k - b)]
    if L == 0 or r.random() < 0.5:
        given = f"vertices {pts_text(V)} and co-vertices {pts_text(Cv)}"
        steps = [f"Center ({h}, {k}) is the midpoint of the vertices.", f"a = {T(a)}, b = {T(b)}.", f"The major axis is {'vertical' if vert else 'horizontal'}, so a² goes under {'y' if vert else 'x'}.", ans + "."]
    else:
        given = f"vertices {pts_text(V)} and foci {pts_text(Fo)}"
        steps = [f"Center ({h}, {k}); a = {T(a)}, c = {T(c)}.", f"b² = a² - c² = {a * a} - {c * c} = {b * b}.", ans + "."]
    w2 = ell_eq(h, k, (b * b if vert else a * a), (a * a + c * c if vert else b * b)) if "foci" in given else ell_eq(h, k, b if vert else a, a if vert else b)
    return Q(f"Write the standard-form equation of the ellipse with {given}.", ans, steps, [ell_eq(h, k, B2, A2), w2 if w2 != ans else ell_eq(h, k, A2, B2 + 1), ell_eq(-h, -k, A2, B2) if (h or k) else ell_eq(0, 0, A2 * 4, B2 * 4)],
             H(f"(x - {h})**2/{A2} + (y - {k})**2/{B2} - 1", "eqn"), why=["Put a² under the wrong variable", "Found b² incorrectly (or used a and b, not a² and b²)", "Used the wrong signs for the center (or the full axis lengths)"])


@fam("012")
def s4_ecc(r, L):
    a, b, c = ell_params(r, 1)
    e = c / a
    return Q(f"An ellipse has major axis length {T(2 * a)} and minor axis length {T(2 * b)}. Find its eccentricity e = c/a. Give an exact answer.", T(sp.nsimplify(e)),
             [f"a = {T(a)}, b = {T(b)}.", f"c = √(a² - b²) = {T(c)}.", f"e = c/a = {T(sp.nsimplify(e))}."], [T(sp.nsimplify(b / a)), T(sp.nsimplify(sp.sqrt(a * a + b * b) / a)), T(sp.nsimplify(a / c))],
             H(f"sqrt(({a})**2 - ({b})**2)/({a})"), why=["Used b/a", "Used c² = a² + b²", "Inverted the ratio"])


# ============================================================== Hyperbola params
def hyp_params(r, L):
    a, b, c = pick(r, [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13), (8, 15, 17)] if L == 0 else
                   [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (1, 2, sp.sqrt(5)), (2, 1, sp.sqrt(5)), (2, 3, sp.sqrt(13)), (3, 2, sp.sqrt(13)), (1, 1, sp.sqrt(2))])
    return sp.nsimplify(a), sp.nsimplify(b), sp.nsimplify(c)


# ============================================================== S5 Hyperbola features
@fam("012")
def s5_features(r, L):
    a, b, c = hyp_params(r, L)
    h, k = (0, 0) if L == 0 and r.random() < 0.4 else hk(r)
    vert = r.random() < 0.5
    st = hyp_eq(h, k, a * a, b * b, vert)
    V = [(h, k + a), (h, k - a)] if vert else [(h + a, k), (h - a, k)]
    Fo = [(h, k + c), (h, k - c)] if vert else [(h + c, k), (h - c, k)]
    ask = pick(r, ["vertices", "foci", "asym"])
    steps = [f"The positive term contains {'y' if vert else 'x'}, so the transverse axis is {'vertical' if vert else 'horizontal'}.", f"a = {T(a)}, b = {T(b)}."]
    if ask == "vertices":
        return Q(f"Find the vertices of the hyperbola {st}.", pts_text(V), steps + [f"Vertices: {pts_text(V)}."],
                 [pts_text([(h + a, k), (h - a, k)] if vert else [(h, k + a), (h, k - a)]), pts_text(Fo), pts_text([(h, k + b), (h, k - b)] if vert else [(h + b, k), (h - b, k)])],
                 H(f"{[[str(p_[0]), str(p_[1])] for p_ in V]}".replace("'", ""), "points"), why=["Used the wrong axis", "Gave the foci", "Used b instead of a"])
    if ask == "foci":
        wc = sp.sqrt(abs(a * a - b * b))
        return Q(f"Find the foci of the hyperbola {st}.", pts_text(Fo), steps + [f"c² = a² + b² = {a * a} + {b * b} = {c * c}.", f"c = {T(c)}.", f"Foci: {pts_text(Fo)}."],
                 [pts_text([(h, k + wc), (h, k - wc)] if vert else [(h + wc, k), (h - wc, k)]) if wc else pts_text([(h, k)]), pts_text(V), pts_text([(h + c, k), (h - c, k)] if vert else [(h, k + c), (h, k - c)])],
                 H(f"[[{h} + {0 if vert else 1}*sqrt({a * a} + {b * b}), {k} + {1 if vert else 0}*sqrt({a * a} + {b * b})], [{h} - {0 if vert else 1}*sqrt({a * a} + {b * b}), {k} - {1 if vert else 0}*sqrt({a * a} + {b * b})]]", "points"),
                 why=["Used c² = a² - b² (ellipse rule)", "Gave the vertices", "Placed the foci on the wrong axis"])
    m = a / b if vert else b / a
    yk = "y" if k == 0 else f"y {'-' if k > 0 else '+'} {abs(k)}"
    xh = "x" if h == 0 else f"(x {'-' if h > 0 else '+'} {abs(h)})"
    mt = T(m)
    mtxt = ("" if m == 1 else (f"({mt})" if "/" in mt else mt))
    ans = f"{yk} = ±{mtxt}{xh}"
    wm = T(1 / m)
    wtxt = ("" if 1 / m == 1 else (f"({wm})" if "/" in wm else wm))
    w = [f"{yk} = ±{wtxt}{xh}", f"{yk} = ±{T(m * m) if m * m != 1 else ''}{xh}", f"{yk} = ±{mtxt}{'x' if h == 0 else f'(x {chr(43) if h > 0 else chr(45)} {abs(h)})'}" if h else f"{yk} = ±{T(m + 1)}x"]
    need(m != 1 and len({ans, *w}) == 4)
    return Q(f"Find the equations of the asymptotes of the hyperbola {st}.", ans, steps + [f"Slopes ±{'a/b' if vert else 'b/a'} = ±{T(m)} through the center ({h}, {k}).", ans + "."], w,
             PY("asym", h=h, k=k, m=str(m)), why=["Inverted the slope", "Used the ratio of a² and b²", "Used the wrong sign for the center" if h else "Made an arithmetic error"])


@fam("01")
def s5_graph(r, L):
    a, b, c = hyp_params(r, 0)
    need(a <= 5 and b <= 5)
    h, k = hk(r, -3, 3)
    vert = r.random() < 0.5
    xr, yr = win(h, k, max(a, b) + 2)
    ans = hyp_eq(h, k, a * a, b * b, vert)
    opts = [(ans, True), (hyp_eq(h, k, a * a, b * b, not vert), False), (hyp_eq(h, k, b * b, a * a, vert), False), (hyp_eq(-h, -k, a * a, b * b, vert) if (h or k) else hyp_eq(h, k, a, b, vert), False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    code = f"(y - {k})**2/{a * a} - (x - {h})**2/{b * b} - 1" if vert else f"(x - {h})**2/{a * a} - (y - {k})**2/{b * b} - 1"
    return Q("Which equation matches the hyperbola shown? The dashed lines are its asymptotes.", ans, [f"Center ({h}, {k}); it opens {'up and down' if vert else 'left and right'}.", f"a = {T(a)} (center to vertex), b = {T(b)} (from the asymptote slope).", ans + "."],
             options=opts, chk=H(code, "eqn"), mode="mc",
             diagram={"alt": f"A hyperbola centered at ({h}, {k}) opening {'up and down' if vert else 'left and right'} with vertices {pts_text([(h, k + a), (h, k - a)] if vert else [(h + a, k), (h - a, k)])} and asymptote slopes ±{T(a / b if vert else b / a)}.",
                      "draw": curve_draw(conic_curves("hyperbola", h, k, a, b, vert), xr, yr, pts=[(h, k, "")] + [(p_[0], p_[1], "") for p_ in ([(h, k + a), (h, k - a)] if vert else [(h + a, k), (h - a, k)])])})


# ============================================================== S6 Writing hyperbola equations
@fam("012")
def s6_write(r, L):
    a, b, c = hyp_params(r, L)
    h, k = (0, 0) if L == 0 and r.random() < 0.4 else hk(r)
    vert = r.random() < 0.5
    V = [(h, k + a), (h, k - a)] if vert else [(h + a, k), (h - a, k)]
    Fo = [(h, k + c), (h, k - c)] if vert else [(h + c, k), (h - c, k)]
    ans = hyp_eq(h, k, a * a, b * b, vert)
    kind = pick(r, ["foci", "asym"]) if L else "foci"
    if kind == "foci":
        given = f"vertices {pts_text(V)} and foci {pts_text(Fo)}"
        steps = [f"Center ({h}, {k}); a = {T(a)}, c = {T(c)}.", f"b² = c² - a² = {c * c} - {a * a} = {b * b}.", ans + "."]
        w2 = hyp_eq(h, k, a * a, c * c + a * a, vert)
    else:
        m = a / b if vert else b / a
        given = f"vertices {pts_text(V)} and asymptote slopes ±{T(m)}"
        steps = [f"Center ({h}, {k}); a = {T(a)}.", f"Slope = {'a/b' if vert else 'b/a'} = {T(m)}, so b = {T(b)}.", ans + "."]
        w2 = hyp_eq(h, k, a * a, (a / m) ** 2 if not vert else (a * m) ** 2, vert)
    code = f"(y - {k})**2/{a * a} - (x - {h})**2/{b * b} - 1" if vert else f"(x - {h})**2/{a * a} - (y - {k})**2/{b * b} - 1"
    w = [hyp_eq(h, k, a * a, b * b, not vert), w2 if w2 != ans else hyp_eq(h, k, b * b, a * a, vert), ell_eq(h, k, a * a, b * b) if not vert else ell_eq(h, k, b * b, a * a)]
    return Q(f"Write the standard-form equation of the hyperbola with {given}.", ans, steps, w, H(code, "eqn"),
             why=["Put the positive term on the wrong variable", "Found b² incorrectly", "Wrote an ellipse (used + instead of -)"])


@fam("012", mode="mc")
def s6_classify(r, L):
    A_, C_ = pick(r, [(1, 1), (2, 3), (3, -2), (0, 4), (4, 0), (-5, 2), (5, 5), (1, 4)])
    D_, E_, F_ = rint(r, -8, 8), rint(r, -8, 8), rint(r, -20, 20)
    need(A_ or C_)
    e = A_ * x ** 2 + C_ * y ** 2 + D_ * x + E_ * y + F_
    if A_ == 0 or C_ == 0:
        need((A_ == 0 and D_ != 0) or (C_ == 0 and E_ != 0))
        typ = "parabola"
    elif A_ == C_:
        typ = "circle"
    elif A_ * C_ > 0:
        typ = "ellipse"
    else:
        typ = "hyperbola"
    opts = [(c_, c_ == typ) for c_ in ["circle", "parabola", "ellipse", "hyperbola"]]
    return Q(f"Classify the conic {T(e)} = 0. (Assume it is not degenerate.)", typ, ["Compare the coefficients of x² and y².", "Only one squared term: parabola. Equal coefficients: circle. Same sign: ellipse. Opposite signs: hyperbola.", f"It is a {typ}."],
             options=opts, chk=PY("conic_type", A=A_, C=C_), mode="mc")


# ============================================================== Short numeric facts (Tarsia / Partner Check friendly)
@fam("012", mode="mc")
def s_short_parab(r, L):
    h, k = hk(r)
    p = rint(r, -9, 9, True)
    vert = r.random() < 0.5
    ask = pick(r, ["p", "latus", "vertex"])
    st = f"{sq('x', h)} = {4 * p}{'(y - ' + str(k) + ')' if k > 0 else '(y + ' + str(-k) + ')' if k < 0 else 'y'}" if vert else f"{sq('y', k)} = {4 * p}{'(x - ' + str(h) + ')' if h > 0 else '(x + ' + str(-h) + ')' if h < 0 else 'x'}"
    if ask == "vertex":
        return Q(f"Find the vertex of the parabola {st}.", f"({h}, {k})", ["(x - h)² = 4p(y - k) and (y - k)² = 4p(x - h) have vertex (h, k).", f"Vertex: ({h}, {k})."],
                 [f"({-h}, {-k})" if (h or k) else "(1, 0)", f"({k}, {h})" if h != k else f"({h}, {k + 1})", f"({h}, {-k})" if k else f"({h + 1}, {k})"], H(f"[{h}, {k}]", "point"),
                 why=["Used the signs shown in the equation", "Switched the coordinates", "Made a sign error"])
    if ask == "p":
        return Q(f"Find the distance from the vertex to the focus of {st}.", str(abs(p)), [f"4p = {4 * p}, so p = {p}.", f"Distance = |p| = {abs(p)}."], [str(abs(4 * p)), str(abs(2 * p)), str(p * p) if p * p != abs(p) else str(abs(p) + 1)],
                 H(f"Abs(Rational({4 * p}, 4))"), why=["Used 4p", "Used 2p", "Squared p"])
    return Q(f"Find the length of the latus rectum (the focal chord perpendicular to the axis) of {st}.", str(abs(4 * p)), ["The latus rectum has length |4p|.", f"|{4 * p}| = {abs(4 * p)}."], [str(abs(p)), str(abs(2 * p)), str(abs(8 * p))],
             H(f"Abs({4 * p})"), why=["Used p", "Used 2p", "Used 8p"])


@fam("012", mode="mc")
def s_short_ell(r, L):
    a, b, c = ell_params(r, pick(r, [0, 1]))
    if a <= 5:
        m_ = rint(r, 1, 3)
        a, b, c = a * m_, b * m_, c * m_
    h, k = hk(r)
    vert = r.random() < 0.5
    A2, B2 = (b * b, a * a) if vert else (a * a, b * b)
    st = ell_eq(h, k, A2, B2)
    ask = pick(r, ["c", "minor", "foci_dist", "center"])
    if ask == "center":
        return Q(f"Find the center of the ellipse {st}.", f"({h}, {k})", ["The center is (h, k).", f"Center: ({h}, {k})."], [f"({-h}, {-k})" if (h or k) else "(1, 1)", f"({k}, {h})" if h != k else f"({h}, {k + 1})", f"({h}, {-k})" if k else f"({h + 1}, {k})"],
                 H(f"[{h}, {k}]", "point"), why=["Used the signs shown in the equation", "Switched the coordinates", "Made a sign error"])
    if ask == "c":
        return Q(f"Find c, the distance from the center to each focus, for {st}.", T(c), ["c² = a² - b².", f"c² = {a * a} - {b * b} = {c * c}, c = {T(c)}."], [T(sp.sqrt(a * a + b * b)), str(a * a - b * b), T(a - b)],
                 H(f"sqrt(Abs({A2} - {B2}))"), why=["Added a² and b²", "Forgot the square root", "Subtracted a and b"])
    if ask == "minor":
        return Q(f"Find the length of the minor axis of {st}.", T(2 * b), ["The smaller denominator is b².", f"b = {T(b)}, so the minor axis is 2b = {T(2 * b)}."], [T(b), T(2 * a), T(b * b)], H(f"2*sqrt(Min({A2}, {B2}))"),
                 why=["Gave b instead of 2b", "Gave the major axis", "Used b²"])
    return Q(f"Find the distance between the foci of {st}.", T(2 * c), ["c² = a² - b².", f"c = {T(c)}, distance = 2c = {T(2 * c)}."], [T(c), T(2 * sp.sqrt(a * a + b * b)), T(2 * a)], H(f"2*sqrt(Abs({A2} - {B2}))"),
             why=["Gave c instead of 2c", "Added a² and b²", "Gave the major axis length"])


@fam("012", mode="mc")
def s_short_hyp(r, L):
    a, b, c = hyp_params(r, pick(r, [0, 1]))
    if c <= 5:
        m_ = rint(r, 1, 3)
        a, b, c = a * m_, b * m_, c * m_
    h, k = hk(r)
    vert = r.random() < 0.5
    st = hyp_eq(h, k, a * a, b * b, vert)
    ask = pick(r, ["c", "trans", "foci_dist", "center"])
    if ask == "center":
        return Q(f"Find the center of the hyperbola {st}.", f"({h}, {k})", ["The center is (h, k).", f"Center: ({h}, {k})."], [f"({-h}, {-k})" if (h or k) else "(1, 1)", f"({k}, {h})" if h != k else f"({h}, {k + 1})", f"({h}, {-k})" if k else f"({h + 1}, {k})"],
                 H(f"[{h}, {k}]", "point"), why=["Used the signs shown in the equation", "Switched the coordinates", "Made a sign error"])
    if ask == "c":
        return Q(f"Find c, the distance from the center to each focus, for {st}.", T(c), ["c² = a² + b².", f"c² = {a * a} + {b * b} = {c * c}, c = {T(c)}."], [T(sp.sqrt(abs(a * a - b * b))) if a != b else "0", str(a * a + b * b), T(a + b)],
                 H(f"sqrt({a * a} + {b * b})"), why=["Subtracted (ellipse rule)", "Forgot the square root", "Added a and b"])
    if ask == "trans":
        return Q(f"Find the length of the transverse axis of {st}.", T(2 * a), ["a² is under the positive term.", f"a = {T(a)}, so the length is 2a = {T(2 * a)}."], [T(a), T(2 * b), T(a * a)], H(f"2*sqrt({a * a})"),
                 why=["Gave a instead of 2a", "Used b", "Used a²"])
    return Q(f"Find the distance between the foci of {st}.", T(2 * c), ["c² = a² + b².", f"c = {T(c)}, distance = 2c = {T(2 * c)}."], [T(c), T(2 * sp.sqrt(abs(a * a - b * b))) if a != b else "0", T(2 * a)], H(f"2*sqrt({a * a} + {b * b})"),
             why=["Gave c instead of 2c", "Subtracted (ellipse rule)", "Gave the transverse axis length"])


@fam("012", mode="mc")
def s_short_circle(r, L):
    h, k = hk(r)
    rad = rint(r, 1, 19)
    st = f"{sq('x', h)} + {sq('y', k)} = {rad ** 2}"
    ask = pick(r, ["radius", "diameter", "center", "center"])
    if ask == "center":
        return Q(f"Find the center of the circle {st}.", f"({h}, {k})", ["(x - h)² + (y - k)² = r² has center (h, k).", f"Center: ({h}, {k})."], [f"({-h}, {-k})" if (h or k) else "(1, 1)", f"({k}, {h})" if h != k else f"({h}, {k + 1})", f"({h}, {-k})" if k else f"({h + 1}, {k})"],
                 H(f"[{h}, {k}]", "point"), why=["Used the signs shown in the equation", "Switched the coordinates", "Made a sign error"])
    v = rad if ask == "radius" else 2 * rad
    return Q(f"Find the {ask} of the circle {st}.", str(v), [f"r² = {rad ** 2}, so r = {rad}.", f"{ask.capitalize()}: {v}."], [str(rad ** 2), str(v * 2) if ask == "radius" else str(rad), str(rad * rad // 2 if rad * rad // 2 not in (v,) else rad + 3)],
             H(f"{'1' if ask == 'radius' else '2'}*sqrt({rad ** 2})"), why=["Gave r² instead", "Doubled (or halved) incorrectly", "Halved r²"])


@fam("2", mode="sa")
def s_pair_radius(r, L):
    """Honors items whose answers repeat (5, 10, 13) so Partner Check can pair different problems with equal answers."""
    h, k = hk(r)
    need(h and k)
    rad = pick(r, [5, 10, 13])
    D_, E_, F_ = -2 * h, -2 * k, h * h + k * k - rad * rad
    st = T(x ** 2 + y ** 2 + D_ * x + E_ * y + F_) + " = 0"
    return Q(f"Find the radius of the circle {st}.", str(rad), ["Group x-terms and y-terms; complete each square.", f"(x - {h})² + (y - {k})² = {rad * rad}.".replace("- -", "+ "), f"r² = {rad * rad}.", f"r = {rad}."],
             [str(rad * rad), str(2 * rad), str(abs(F_)) if abs(F_) not in (rad, rad * rad, 2 * rad) else str(rad + 1)],
             H(f"(lambda E: sqrt(diff(E, x).subs({{x: 0, y: 0}})**2/4 + diff(E, y).subs({{x: 0, y: 0}})**2/4 - E.subs({{x: 0, y: 0}})))(P('{st.split(' = ')[0]}'))"),
             why=["Gave r² instead of r", "Gave the diameter", "Used the constant term"])


@fam("2", mode="sa")
def s_pair_parab(r, L):
    """Honors: focal distance |p| in {5, 10, 13}; repeated answers let Partner Check pair problems."""
    h, k = hk(r)
    p = pick(r, [5, 10, 13]) * pick(r, [1, -1])
    vert = r.random() < 0.5
    e = sp.expand((x - h) ** 2 - 4 * p * (y - k)) if vert else sp.expand((y - k) ** 2 - 4 * p * (x - h))
    st = T(e) + " = 0"
    return Q(f"Find the distance from the vertex to the focus of the parabola {st}.", str(abs(p)), [f"Complete the square in {'x' if vert else 'y'}.", f"Standard form: {'(x - h)² = 4p(y - k)' if vert else '(y - k)² = 4p(x - h)'} with 4p = {4 * p}.", f"p = {p}.", f"Distance = |p| = {abs(p)}."],
             [str(abs(4 * p)), str(abs(2 * p)), str(abs(p) + 1)], H(f"Abs(Rational({4 * p}, 4))"), why=["Used 4p", "Used 2p", "Made an arithmetic error"])


@fam("2", mode="sa")
def s_pair_ell(r, L):
    """Honors: semi-major axis a in {5, 10, 13} from the foci and minor axis."""
    a, b, c = pick(r, [(5, 4, 3), (5, 3, 4), (10, 8, 6), (10, 6, 8), (13, 12, 5), (13, 5, 12)])
    h, k = hk(r)
    vert = r.random() < 0.5
    Fo = [(h, k + c), (h, k - c)] if vert else [(h + c, k), (h - c, k)]
    return Q(f"An ellipse has foci {pts_text(Fo)} and a minor axis of length {2 * b}. Find a, the length of the semi-major axis.", str(a),
             [f"Center ({h}, {k}); c = {c}.", f"b = {2 * b} ÷ 2 = {b}.", f"a² = b² + c² = {b * b} + {c * c} = {a * a}.", f"a = {a}."], [str(a * a), str(2 * a), str(b + c)],
             H(f"sqrt({b}**2 + {c}**2)"), why=["Forgot the square root", "Gave the major-axis length", "Added b and c"])


SKILLS = {
    1: dict(name="Circles and Their Equations", std=["G-GPE.A.1"], fams=[s1_read, s1_write, s1_graph, s_short_circle, reuse(s_short_circle, (0, 1, 2), 'b'), reuse(s_pair_radius, (2, 2, 2), 'a'), reuse(s_pair_radius, (2, 2, 2), 'a2')], extra=[err_of(s1_write), open_of(s1_read), err_of(s1_read)]),
    2: dict(name="Parabolas: Focus, Directrix, and Standard Form", std=["G-GPE.A.2"], fams=[s2_features, s2_write, s2_general, s2_graph, s_short_parab, reuse(s_short_parab, (0, 1, 2), 'b'), s_pair_parab, reuse(s_pair_parab, (2, 2, 2), 'b2')], extra=[err_of(s2_features), open_of(s2_features), err_of(s2_write)]),
    3: dict(name="Ellipses: Graphs, Vertices, and Foci", std=["G-GPE.A.3"], fams=[s3_features, s3_graph, s_short_ell, reuse(s_short_ell, (0, 1, 2), 'b')], extra=[err_of(s3_features), open_of(s3_features)]),
    4: dict(name="Writing Equations of Ellipses", std=["G-GPE.A.3"], fams=[s4_write, s4_ecc, reuse(s_short_ell, (0, 1, 2), 'w'), reuse(s_short_parab, (0, 1, 2), 'w'), s_pair_ell, reuse(s_pair_ell, (2, 2, 2), 'c2')], extra=[err_of(s4_write), open_of(s4_write)]),
    5: dict(name="Hyperbolas: Graphs and Key Features", std=["G-GPE.A.3"], fams=[s5_features, s5_graph, s_short_hyp, reuse(s_short_hyp, (0, 1, 2), 'b')], extra=[err_of(s5_features), open_of(s5_features)]),
    6: dict(name="Writing Equations of Hyperbolas", std=["G-GPE.A.3"], fams=[s6_write, s6_classify, reuse(s_short_hyp, (0, 1, 2), 'w'), reuse(s_short_circle, (0, 1, 2), 'w')], extra=[err_of(s6_write), open_of(s6_write)]),
}
