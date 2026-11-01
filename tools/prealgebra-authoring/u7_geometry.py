"""Unit 7 — Geometry (geometry-applications): Pythagorean theorem, distance, volume."""
from lib import *

UNIT_ID = "geometry-applications"
ABBR = "geo"

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (6, 8, 10), (9, 12, 15), (12, 16, 20), (20, 21, 29), (9, 40, 41), (10, 24, 26), (15, 20, 25), (12, 35, 37)]
UNITS = ["cm", "in.", "ft", "m"]


def unit_word(u):
    return {"cm": "centimeters", "in.": "inches", "ft": "feet", "m": "meters"}[u]


# ---------------------------------------------------------------- drawings
def right_tri_draw(a, b, c, labels, right_at="C"):
    """Right triangle with legs a (vertical), b (horizontal); labels for (leg a, leg b, hypotenuse)."""
    def draw(path):
        fig, ax = new_fig(5.6, 4.4)
        s = 5.0 / max(a, b)
        A, B_, C = (0, a * s), (b * s, 0), (0, 0)
        ax.plot([A[0], B_[0], C[0], A[0]], [A[1], B_[1], C[1], A[1]], color="#1f4e9c", lw=2.4)
        q = 0.35
        ax.plot([0, q, q], [q, q, 0], color="black", lw=1.2)
        ax.text(-0.25, a * s / 2, labels[0], ha="right", va="center", fontsize=14, color="#b23a3a")
        ax.text(b * s / 2, -0.3, labels[1], ha="center", va="top", fontsize=14, color="#b23a3a")
        ax.text(b * s / 2 + 0.25, a * s / 2 + 0.25, labels[2], ha="left", va="bottom", fontsize=14, color="#b23a3a")
        ax.set_aspect("equal")
        ax.set_xlim(-1.5, b * s + 1.5)
        ax.set_ylim(-1.0, a * s + 0.8)
        ax.axis("off")
        save(fig, path)
    return draw


def cyl_draw(r_lab, h_lab, kind="cylinder", show_diam=False):
    from matplotlib.patches import Ellipse

    def draw(path):
        fig, ax = new_fig(4.6, 5.0)
        R, H, e = 1.6, 3.2, 0.45
        if kind in ("cylinder", "cone"):
            ax.add_patch(Ellipse((0, 0), 2 * R, 2 * e, fill=False, lw=2, color="#1f4e9c", ls="-"))
        if kind == "cylinder":
            ax.add_patch(Ellipse((0, H), 2 * R, 2 * e, fill=False, lw=2, color="#1f4e9c"))
            ax.plot([-R, -R], [0, H], color="#1f4e9c", lw=2)
            ax.plot([R, R], [0, H], color="#1f4e9c", lw=2)
            top = H
        elif kind == "cone":
            ax.plot([-R, 0, R], [0, H, 0], color="#1f4e9c", lw=2)
            top = H
        if kind in ("cylinder", "cone"):
            ax.plot([0, 0], [0, H], color="#b23a3a", lw=1.5, ls="--")
            ax.text(0.12, H / 2, h_lab, fontsize=13, color="#b23a3a", va="center")
            if show_diam:
                ax.plot([-R, R], [0, 0], color="#2e7d32", lw=1.6)
                ax.text(0, -0.25, r_lab, fontsize=13, color="#2e7d32", ha="center", va="top")
            else:
                ax.plot([0, R], [0, 0], color="#2e7d32", lw=1.6)
                ax.text(R / 2, -0.25, r_lab, fontsize=13, color="#2e7d32", ha="center", va="top")
        else:  # sphere
            from matplotlib.patches import Circle
            ax.add_patch(Circle((0, 1.6), R, fill=False, lw=2, color="#1f4e9c"))
            ax.add_patch(Ellipse((0, 1.6), 2 * R, 2 * e, fill=False, lw=1, ls="--", color="#1f4e9c"))
            if show_diam:
                ax.plot([-R, R], [1.6, 1.6], color="#2e7d32", lw=1.6)
                ax.text(0, 1.75, r_lab, fontsize=13, color="#2e7d32", ha="center", va="bottom")
            else:
                ax.plot([0, R], [1.6, 1.6], color="#2e7d32", lw=1.6)
                ax.text(R / 2, 1.75, r_lab, fontsize=13, color="#2e7d32", ha="center", va="bottom")
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-1.0, 4.0)
        ax.set_aspect("equal")
        ax.axis("off")
        save(fig, path)
    return draw


def box_draw(l, w, h, diag=True):
    def draw(path):
        fig, ax = new_fig(5.6, 4.6)
        L_, W_, H_ = 3.6, 1.6, 2.2
        dx, dy = W_ * 0.6, W_ * 0.45
        f = [(0, 0), (L_, 0), (L_, H_), (0, H_)]
        b = [(x + dx, y + dy) for x, y in f]
        for poly_ in (f,):
            ax.plot([p[0] for p in poly_] + [poly_[0][0]], [p[1] for p in poly_] + [poly_[0][1]], color="#1f4e9c", lw=2)
        ax.plot([b[1][0], b[2][0], b[3][0]], [b[1][1], b[2][1], b[3][1]], color="#1f4e9c", lw=2)
        ax.plot([b[0][0], b[1][0]], [b[0][1], b[1][1]], color="#1f4e9c", lw=1.2, ls="--")
        ax.plot([b[0][0], b[3][0]], [b[0][1], b[3][1]], color="#1f4e9c", lw=1.2, ls="--")
        for i in (1, 2, 3):
            ax.plot([f[i][0], b[i][0]], [f[i][1], b[i][1]], color="#1f4e9c", lw=2)
        ax.plot([f[0][0], b[0][0]], [f[0][1], b[0][1]], color="#1f4e9c", lw=1.2, ls="--")
        if diag:
            ax.plot([f[0][0], b[2][0]], [f[0][1], b[2][1]], color="#b23a3a", lw=2)
        ax.text(L_ / 2, -0.3, l, ha="center", va="top", fontsize=13)
        ax.text(L_ + dx / 2 + 0.15, dy / 2 - 0.05, w, ha="left", va="center", fontsize=13)
        ax.text(-0.2, H_ / 2, h, ha="right", va="center", fontsize=13)
        ax.text(-1.1, -0.85, "Not drawn to scale", fontsize=9, color="gray")
        ax.set_xlim(-1.2, L_ + dx + 1.0)
        ax.set_ylim(-0.9, H_ + dy + 0.4)
        ax.set_aspect("equal")
        ax.axis("off")
        save(fig, path)
    return draw


# ======================================================================= S1 Pythagorean theorem and converse
@fam("012")
def s1_hyp(r, L):
    a, b, c = pick(r, TRIPLES[:6] if L == 0 else TRIPLES)
    u = pick(r, UNITS)
    if L == 2 or (L == 1 and r.random() < 0.4):
        a, b = r.randint(2, 12), r.randint(2, 12)
        s = a * a + b * b
        need(math.isqrt(s) ** 2 != s)
        exact = r.random() < 0.5
        ans = f"√{s} {u}" if exact else f"{Rd(math.sqrt(s), 1)} {u}"
        return P(f"A right triangle has legs {a} {u} and {b} {u}. Find the length of the hypotenuse" + (" in simplest radical form (exact value)." if exact else ", rounded to the nearest tenth."),
                 ans, [f"c² = {a}² + {b}² = {a * a} + {b * b} = {s}.", f"c = √{s}" + ("" if exact else f" ≈ {Rd(math.sqrt(s), 3)} ≈ {Rd(math.sqrt(s), 1)}") + f" {u}."],
                 [f"{a + b} {u}", f"{s} {u}", f"√{abs(a * a - b * b)} {u}" if exact and a != b else f"{Rd(math.sqrt(abs(a * a - b * b)) if a != b else s / 2, 1)} {u}"],
                 chk_val(f"√({a}^2 + {b}^2)") if exact else {"kind": "approx", "expr": f"√({a}^2 + {b}^2)", "places": 1}, tags=["misconception"],
                 diagram={"draw": right_tri_draw(a, b, 0, [f"{a} {u}", f"{b} {u}", "c"]), "alt": f"Right triangle with legs {a} {u} and {b} {u}; hypotenuse c."} if L == 1 else None)
    k = pick(r, [1, 1, 2]) if L == 0 else 1
    a, b, c = a * k, b * k, c * k
    return P(f"A right triangle has legs {a} {u} and {b} {u}. What is the length of the hypotenuse?", f"{c} {u}",
             [f"c² = {a}² + {b}² = {a * a + b * b}.", f"c = √{a * a + b * b} = {c} {u}."], [f"{a + b} {u}", f"{a * a + b * b} {u}", f"{math.isqrt(abs(b * b - a * a)) if math.isqrt(abs(b * b - a * a)) ** 2 == abs(b * b - a * a) else c + 1} {u}"],
             chk_val(f"√({a}^2 + {b}^2)"), diagram={"draw": right_tri_draw(a, b, c, [f"{a} {u}", f"{b} {u}", "c"]), "alt": f"Right triangle with legs {a} {u} and {b} {u}; hypotenuse c."} if L == 0 else None,
             tags=["misconception"])


@fam("012")
def s1_leg(r, L):
    a, b, c = pick(r, TRIPLES if L else TRIPLES[:6])
    u = pick(r, UNITS)
    if L == 2:
        c = r.randint(6, 20)
        a = r.randint(2, c - 2)
        s = c * c - a * a
        need(math.isqrt(s) ** 2 != s)
        return P(f"A right triangle has hypotenuse {c} {u} and one leg {a} {u}. Find the other leg to the nearest tenth.", f"{Rd(math.sqrt(s), 1)} {u}",
                 [f"b² = {c}² - {a}² = {s}.", f"b = √{s} ≈ {Rd(math.sqrt(s), 1)} {u}."], [f"{Rd(math.sqrt(c * c + a * a), 1)} {u}", f"{c - a} {u}", f"{Rd(s / 2, 1)} {u}"],
                 {"kind": "approx", "expr": f"√({c}^2 - {a}^2)", "places": 1}, tags=["misconception"])
    return P(f"A right triangle has a hypotenuse of {c} {u} and a leg of {a} {u}. Find the length of the other leg.", f"{b} {u}",
             [f"b² = {c}² - {a}² = {c * c} - {a * a} = {b * b}.", f"b = {b} {u}."], [f"{Rd(math.sqrt(c * c + a * a), 1)} {u}", f"{c - a} {u}", f"{b * b} {u}"],
             chk_val(f"√({c}^2 - {a}^2)"), diagram={"draw": right_tri_draw(a, b, c, [f"{a} {u}", "b", f"{c} {u}"]), "alt": f"Right triangle with one leg {a} {u}, other leg b, hypotenuse {c} {u}."},
             tags=["misconception", "graph"])


@fam("012", mode="sa")
def s1_converse(r, L):
    if r.random() < 0.5:
        a, b, c = pick(r, TRIPLES)
        if L == 2:
            k = F(r.randint(1, 4), 2)
            a, b, c = a * k, b * k, c * k
    else:
        a, b = r.randint(3, 15), r.randint(3, 15)
        c = math.isqrt(a * a + b * b) + pick(r, [0, 1])
        need(a * a + b * b != c * c and c > max(a, b))
    sides = [a, b, c]
    r.shuffle(sides)
    ans = "yes" if a * a + b * b == c * c else "no"
    sh = ", ".join(D(F(s)) for s in sides)
    return P(f"Can the side lengths {sh} form a right triangle? Answer yes or no.", ans,
             [f"Test the longest side as the hypotenuse: {D(F(a))}² + {D(F(b))}² = {D(F(a) ** 2 + F(b) ** 2)} and {D(F(c))}² = {D(F(c) ** 2)}.",
              "Equal → right triangle (converse of the Pythagorean theorem)." if ans == "yes" else "Not equal → not a right triangle."],
             ["no" if ans == "yes" else "yes"], chk_py("is_right", sides=[D(F(s)) for s in sides]), tags=["reasoning"], mode="sa")


@fam("12", mode="mc")
def s1_which_right(r, L):
    good = pick(r, TRIPLES)
    bads = []
    while len(bads) < 3:
        a, b = r.randint(3, 20), r.randint(3, 20)
        c = math.isqrt(a * a + b * b) + 1
        if (a, b, c) not in bads and a * a + b * b != c * c:
            bads.append((a, b, c))
    opts = [(", ".join(map(str, t)), t == good) for t in [good] + bads]
    r.shuffle(opts)
    return P("Which set of side lengths forms a right triangle?", ", ".join(map(str, good)), [f"{good[0]}² + {good[1]}² = {good[0] ** 2 + good[1] ** 2} = {good[2]}²."], options=opts,
             chk=chk_py("is_right_set"), tags=["reasoning"], mode="mc")


@fam("2")
def s1_missing_var(r, L):
    a, b, c = pick(r, TRIPLES)
    k = r.randint(1, 4)
    return P(f"A right triangle has legs {a} and x + {k}, and hypotenuse {c}. Find x.", f"x = {b - k}", [f"{a}² + (x + {k})² = {c}².", f"(x + {k})² = {c * c - a * a}, so x + {k} = {b} (length is positive).", f"x = {b - k}."],
             [f"x = {b}", f"x = {b + k}", f"x = {c - a - k}"], chk_py("pyth_var", a=a, k=k, c=c), tags=["challenge"])


@fam("012")
def s1_error(r, L):
    a, b, c = pick(r, TRIPLES[:6])
    return P(f"A right triangle has a leg of {a} and a hypotenuse of {c}. Tara found the other leg by computing √({a}² + {c}²) ≈ {Rd(math.sqrt(a * a + c * c), 1)}. What is the correct length of the other leg?", str(b),
             ["Tara treated the hypotenuse as a leg. The hypotenuse is the longest side: a² + b² = c².", f"b = √({c}² - {a}²) = √{b * b} = {b}."],
             [Rd(math.sqrt(a * a + c * c), 1), str(c - a), str(c + a)], chk_val(f"√({c}^2 - {a}^2)"), tags=["error-analysis", "misconception"])


@fam("012")
def s1_select(r, L):
    goods = pick(r, TRIPLES, 3)
    bads = []
    while len(bads) < 3:
        a, b = r.randint(3, 15), r.randint(3, 15)
        c = math.isqrt(a * a + b * b) + 1
        if a * a + b * b != c * c and (a, b, c) not in bads:
            bads.append((a, b, c))
    opts = [(", ".join(map(str, t)), True) for t in goods] + [(", ".join(map(str, t)), False) for t in bads]
    need(len({o[0] for o in opts}) == 6)
    return P("Select ALL sets of side lengths that form right triangles.", None, ["Check whether the squares of the two shorter sides add to the square of the longest side."], options=opts,
             chk=chk_py("is_right_set"), tags=["reasoning"])


@fam("012")
def s1_open(r, L):
    a, b, c = pick(r, TRIPLES)
    return P(f"Triangle PQR has PQ = {a}, QR = {b}, and PR = {c}.", None, ["Longest side.", "Square.", "Compare.", "Converse."],
             parts=[("Which side is longest (could be the hypotenuse)?", "PR", {"kind": "text", "accept": ["PR"]}), (f"Find PQ² + QR².", str(a * a + b * b), chk_val(f"{a}^2 + {b}^2")),
                    ("Find PR².", str(c * c), chk_val(f"{c}^2")), ("Is triangle PQR a right triangle? Answer yes or no.", "yes", chk_py("is_right", sides=[str(a), str(b), str(c)]))], tags=["reasoning"])


# ======================================================================= S2 2D applications
@fam("012")
def s2_ladder(r, L):
    a, b, c = pick(r, TRIPLES[:8])
    q = pick(r, ["height", "base"]) if L else "height"
    if L == 2:
        c = r.randint(10, 30)
        b = r.randint(2, c // 2)
        s = c * c - b * b
        need(math.isqrt(s) ** 2 != s)
        return P(f"A {c}-foot ladder leans against a wall. Its base is {b} feet from the wall. How high up the wall does it reach? Round to the nearest tenth of a foot.", f"{Rd(math.sqrt(s), 1)} feet",
                 [f"h² + {b}² = {c}².", f"h = √{s} ≈ {Rd(math.sqrt(s), 1)} feet."], [f"{Rd(math.sqrt(c * c + b * b), 1)} feet", f"{c - b} feet", f"{Rd(s / 2, 1)} feet"],
                 {"kind": "approx", "expr": f"√({c}^2 - {b}^2)", "places": 1}, tags=["modeling"])
    return P(f"A {c}-foot ladder leans against a wall with its base {b} feet from the wall. How high up the wall does the ladder reach?" if q == "height" else
             f"A {c}-foot ladder reaches {a} feet up a wall. How far is the base of the ladder from the wall?", f"{a} feet" if q == "height" else f"{b} feet",
             [f"The wall, ground and ladder form a right triangle with hypotenuse {c}.", f"{'h' if q == 'height' else 'd'} = √({c}² - {b if q == 'height' else a}²) = {a if q == 'height' else b} feet."],
             [f"{c - (b if q == 'height' else a)} feet", f"{Rd(math.sqrt(c * c + (b if q == 'height' else a) ** 2), 1)} feet", f"{c + (b if q == 'height' else a)} feet"],
             chk_val(f"√({c}^2 - {b if q == 'height' else a}^2)"),
             diagram={"draw": right_tri_draw(a, b, c, ["h" if q == "height" else f"{a} ft", f"{b} ft" if q == "height" else "d", f"{c} ft"]), "alt": f"Ladder of length {c} ft forming the hypotenuse of a right triangle with the wall and the ground."} if L == 0 else None,
             tags=["modeling"])


@fam("012")
def s2_rect_diag(r, L):
    a, b, c = pick(r, TRIPLES)
    k = pick(r, ["tv", "field", "door"])
    if k == "tv":
        p = f"A TV screen is {b} inches wide and {a} inches tall. TV sizes are measured along the diagonal. What is the size of the TV?"
        ans = f"{c} inches"
    elif k == "field":
        p = f"A rectangular field is {b} meters long and {a} meters wide. How long is the path straight across the field from one corner to the opposite corner?"
        ans = f"{c} meters"
    else:
        a2 = r.randint(3, 9)
        b2 = r.randint(2, 6)
        s = a2 * a2 + b2 * b2
        need(math.isqrt(s) ** 2 != s)
        return P(f"A doorway is {a2} feet tall and {b2} feet wide. What is the length of its diagonal, to the nearest tenth of a foot? (Would a {Rd(math.sqrt(s) + 0.3, 1)}-foot-wide flat panel fit through diagonally?)",
                 f"{Rd(math.sqrt(s), 1)} feet", [f"d² = {a2}² + {b2}² = {s}.", f"d ≈ {Rd(math.sqrt(s), 1)} feet, so a {Rd(math.sqrt(s) + 0.3, 1)}-foot panel would not fit."],
                 [f"{a2 + b2} feet", f"{Rd(math.sqrt(abs(a2 * a2 - b2 * b2)), 1)} feet", f"{s} feet"], {"kind": "approx", "expr": f"√({a2}^2 + {b2}^2)", "places": 1}, tags=["modeling", "reasoning"])
    return P(p, ans, [f"The diagonal is the hypotenuse: √({a}² + {b}²) = √{c * c} = {c}."], [f"{a + b} {ans.split()[1]}", f"{c * c} {ans.split()[1]}", f"{b - a if b > a else c + 2} {ans.split()[1]}"],
             chk_val(f"√({a}^2 + {b}^2)"), tags=["modeling"])


@fam("012")
def s2_walk(r, L):
    a, b, c = pick(r, TRIPLES)
    nm = pick(r, NAMES)
    if L == 0:
        return P(f"{nm} walks {a} blocks north and then {b} blocks east. How far is {nm} from the starting point in a straight line?", f"{c} blocks",
                 [f"The path makes a right angle: d = √({a}² + {b}²) = {c}."], [f"{a + b} blocks", f"{c * c} blocks", f"{abs(b - a)} blocks"], chk_val(f"√({a}^2 + {b}^2)"), tags=["modeling"])
    e = r.randint(1, 4)
    return P(f"{nm} walks {a + e} km north, {b} km east, then {e} km south. How far is {nm} from the start in a straight line?", f"{c} km",
             [f"Net north: {a + e} - {e} = {a} km; east {b} km.", f"d = √({a}² + {b}²) = {c} km."], [f"{a + b + 2 * e} km", f"{Rd(math.sqrt((a + e) ** 2 + b * b), 1)} km", f"{c + e} km"],
             chk_val(f"√(({a + e} - {e})^2 + {b}^2)"), tags=["modeling", "multistep"])


@fam("12")
def s2_isosceles_height(r, L):
    a, b, c = pick(r, TRIPLES)
    base = 2 * b
    area = b * a
    q = pick(r, ["height", "area"]) if L == 2 else "height"
    if q == "height":
        return P(f"An isosceles triangle has two sides of {c} cm and a base of {base} cm. What is its height?", f"{a} cm",
                 [f"The height splits the base into halves of {b} cm, forming a right triangle with hypotenuse {c}.", f"h = √({c}² - {b}²) = {a} cm."],
                 [f"{Rd(math.sqrt(c * c - base * base), 1) if c > base else c - b} cm", f"{c - b} cm", f"{Rd(math.sqrt(c * c + b * b), 1)} cm"], chk_val(f"√({c}^2 - ({base}/2)^2)"), tags=["modeling", "connections"])
    return P(f"An isosceles triangle has two sides of {c} cm and a base of {base} cm. What is its area?", f"{area} square cm",
             [f"Height = √({c}² - {b}²) = {a} cm.", f"Area = (1/2)({base})({a}) = {area} square cm."], [f"{base * a} square cm", f"{b * c} square cm", f"{base * c // 2} square cm"],
             chk_val(f"(1/2)*{base}*√({c}^2 - {b}^2)"), tags=["modeling", "multistep"])


@fam("2")
def s2_ramp(r, L):
    rise = F(r.randint(1, 4) * 6, 12) if False else r.randint(2, 5)
    run = rise * 12
    L_ = math.sqrt(rise * rise + run * run)
    return P(f"A wheelchair ramp must rise 1 inch for every 12 inches of horizontal length. A ramp rises {rise} feet. How long is the ramp surface, to the nearest tenth of a foot?", f"{Rd(L_, 1)} feet",
             [f"Horizontal length: 12 × {rise} = {run} feet.", f"Ramp = √({rise}² + {run}²) ≈ {Rd(L_, 1)} feet."], [f"{run} feet", f"{rise + run} feet", f"{Rd(math.sqrt(run * run - rise * rise), 1)} feet"],
             {"kind": "approx", "expr": f"√({rise}^2 + (12*{rise})^2)", "places": 1}, tags=["modeling", "challenge"])


@fam("012")
def s2_error(r, L):
    a, b, c = pick(r, TRIPLES[:6])
    return P(f"A rectangle is {b} m by {a} m. Rae says the diagonal is {a + b} m because \"you walk along both sides.\" How long is the diagonal?", f"{c} m",
             ["The diagonal is a straight path, shorter than going along two sides.", f"d = √({a}² + {b}²) = {c} m."], [f"{a + b} m", f"{c * c} m", f"{abs(b - a)} m"],
             chk_val(f"√({a}^2 + {b}^2)"), tags=["error-analysis", "misconception"])


@fam("012")
def s2_select(r, L):
    a, b, c = pick(r, TRIPLES[:6])
    stm = [(f"The diagonal is {c} ft.", True), (f"The diagonal is shorter than {a + b} ft.", True), (f"The diagonal squared equals {a * a + b * b}.", True),
           (f"The diagonal is {a + b} ft.", False), (f"The diagonal is {c * c} ft.", False), (f"The diagonal is shorter than {b} ft.", c < b)]
    need(not stm[5][1])
    return P(f"A rectangular garden is {b} ft long and {a} ft wide. Select ALL true statements about its diagonal.", None, [f"d = √({a}² + {b}²) = {c}."], options=stm,
             chk=chk_py("diag_stmt", a=a, b=b), tags=["modeling"])


@fam("012")
def s2_open(r, L):
    a, b, c = pick(r, TRIPLES[:8])
    return P(f"A kite string is {c} feet long and is pulled tight. The kite is directly above a point {b} feet from the person holding the string.", None,
             ["Hypotenuse.", "Leg.", "Pythagorean theorem.", "Compare."],
             parts=[("Which length is the hypotenuse of the right triangle?", f"the string, {c} feet", {"kind": "text", "accept": [f"the string, {c} feet"]}),
                    ("Write the equation for the kite's height h.", f"h² + {b}² = {c}²", chk_py("pyth_eq", leg=b, hyp=c)),
                    ("Find the height h.", f"{a} feet", chk_val(f"√({c}^2 - {b}^2)")), ("Is the height more or less than the string length?", "less", {"kind": "text", "accept": ["less"]})],
             tags=["modeling"])


# ======================================================================= S3 3D applications
BOXES = [(2, 3, 6, 7), (1, 4, 8, 9), (2, 6, 9, 11), (6, 6, 7, 11), (4, 4, 7, 9), (3, 4, 12, 13), (2, 10, 11, 15), (1, 2, 2, 3), (2, 4, 4, 6), (6, 9, 2, 11), (8, 9, 12, 17), (4, 5, 20, 21)]


@fam("012")
def s3_box_diag(r, L):
    l, w, h, d = pick(r, BOXES)
    u = pick(r, ["in.", "cm", "ft"])
    if L == 2 and r.random() < 0.6:
        l, w, h = r.randint(2, 12), r.randint(2, 10), r.randint(2, 10)
        s = l * l + w * w + h * h
        need(math.isqrt(s) ** 2 != s)
        return P(f"A rectangular box is {l} {u} long, {w} {u} wide and {h} {u} tall. Find the length of the longest rod that fits inside (the space diagonal), to the nearest tenth.",
                 f"{Rd(math.sqrt(s), 1)} {u}", [f"Floor diagonal² = {l}² + {w}² = {l * l + w * w}.", f"Space diagonal = √({l * l + w * w} + {h}²) = √{s} ≈ {Rd(math.sqrt(s), 1)} {u}."],
                 [f"{Rd(math.sqrt(l * l + w * w), 1)} {u}", f"{l + w + h} {u}", f"{Rd(math.sqrt(l * l + w * w) + h, 1)} {u}"], {"kind": "approx", "expr": f"√({l}^2 + {w}^2 + {h}^2)", "places": 1},
                 tags=["multistep"])
    return P(f"A rectangular box is {l} {u} by {w} {u} by {h} {u}. What is the length of the diagonal from a bottom corner to the opposite top corner?", f"{d} {u}",
             [f"Bottom diagonal: √({l}² + {w}²) = √{l * l + w * w}.", f"Space diagonal: √({l * l + w * w} + {h}²) = √{d * d} = {d} {u}."],
             [f"{l + w + h} {u}", f"{Rd(math.sqrt(l * l + w * w), 1)} {u}", f"{d * d} {u}"], chk_val(f"√({l}^2 + {w}^2 + {h}^2)"),
             diagram={"draw": box_draw(f"{l} {u}", f"{w} {u}", f"{h} {u}"), "alt": f"Rectangular box {l} {u} long, {w} {u} wide, {h} {u} tall, with the space diagonal drawn from a bottom front corner to the opposite top back corner."} if L < 2 else None,
             tags=["multistep", "graph"] if L < 2 else ["multistep"])


@fam("012")
def s3_cone_slant(r, L):
    a, b, c = pick(r, TRIPLES)
    q = pick(r, ["slant", "height", "radius"]) if L else "slant"
    if q == "slant":
        return P(f"A cone has radius {a} cm and height {b} cm. What is its slant height?", f"{c} cm", ["Radius, height and slant height form a right triangle (slant height is the hypotenuse).", f"l = √({a}² + {b}²) = {c} cm."],
                 [f"{a + b} cm", f"{Rd(math.sqrt(abs(b * b - a * a)), 1)} cm", f"{c * c} cm"], chk_val(f"√({a}^2 + {b}^2)"), tags=["connections"],
                 diagram={"draw": cyl_draw(f"r = {a} cm", f"h = {b} cm", "cone"), "alt": f"Cone with radius {a} cm and height {b} cm."} if L == 0 else None)
    if q == "height":
        return P(f"A cone has slant height {c} cm and radius {a} cm. What is its height?", f"{b} cm", [f"h = √({c}² - {a}²) = {b} cm."], [f"{c - a} cm", f"{Rd(math.sqrt(c * c + a * a), 1)} cm", f"{c + a} cm"],
                 chk_val(f"√({c}^2 - {a}^2)"), tags=["connections"])
    d = 2 * a
    return P(f"A cone has a base diameter of {d} in. and a slant height of {c} in. What is its height?", f"{b} in.",
             [f"Radius = {d} ÷ 2 = {a} in.", f"h = √({c}² - {a}²) = {b} in."], [f"{Rd(math.sqrt(c * c - d * d), 1) if c > d else c - a} in.", f"{c - a} in.", f"{Rd(math.sqrt(c * c + a * a), 1)} in."],
             chk_val(f"√({c}^2 - ({d}/2)^2)"), tags=["connections", "misconception"])


@fam("12")
def s3_pyramid(r, L):
    a, b, c = pick(r, TRIPLES)
    s = 2 * a
    return P(f"A square pyramid has base edge {s} m and height {b} m. Find the slant height (from the top to the midpoint of a base edge).", f"{c} m",
             [f"Half the base edge: {a} m.", f"Slant height = √({a}² + {b}²) = {c} m."], [f"{Rd(math.sqrt(s * s + b * b), 1)} m", f"{a + b} m", f"{c + a} m"], chk_val(f"√(({s}/2)^2 + {b}^2)"),
             tags=["connections", "multistep"])


@fam("2", mode="mc")
def s3_fits(r, L):
    l, w, h = r.randint(4, 12), r.randint(3, 9), r.randint(3, 9)
    dd = math.sqrt(l * l + w * w + h * h)
    rod = round(dd + pick(r, [-1.5, -0.6, 0.6, 1.5]), 1)
    fits = rod <= dd
    good = f"{'Yes' if fits else 'No'}, because the longest segment inside the box is about {Rd(dd, 1)} in."
    opts = [(good, True), (f"{'No' if fits else 'Yes'}, because the longest segment inside the box is about {Rd(dd, 1)} in.", False),
            (f"Yes, because {rod} < {l + w + h}.", False), (f"No, because {rod} > {max(l, w, h)}.", False)]
    r.shuffle(opts)
    return P(f"Will a {rod}-inch straight rod fit entirely inside a closed box that is {l} in. × {w} in. × {h} in.?", good,
             [f"Longest segment = space diagonal = √({l}² + {w}² + {h}²) ≈ {Rd(dd, 2)} in.", "It fits only if the rod is no longer than that."],
             options=opts, chk=chk_py("rod_fits", dims=[l, w, h], rod=rod), tags=["reasoning", "challenge"], mode="mc")


@fam("012")
def s3_error(r, L):
    l, w, h, d = pick(r, BOXES)
    return P(f"Nate says the longest diagonal of a {l} × {w} × {h} box is √({l}² + {w}²) ≈ {Rd(math.sqrt(l * l + w * w), 1)}. What is the length of the space diagonal?", str(d),
             ["Nate found only the diagonal of the bottom face.", f"Use all three dimensions: √({l}² + {w}² + {h}²) = {d}."], [Rd(math.sqrt(l * l + w * w), 1), str(l + w + h), str(d + h)],
             chk_val(f"√({l}^2 + {w}^2 + {h}^2)"), tags=["error-analysis", "misconception"])


@fam("012")
def s3_select(r, L):
    l, w, h, d = pick(r, BOXES)
    bd2 = l * l + w * w
    stm = [(f"The bottom-face diagonal squared is {bd2}.", True), (f"The space diagonal is {d}.", True), (f"The space diagonal squared is {d * d}.", True),
           (f"The space diagonal is {l + w + h}.", l + w + h == d), (f"The space diagonal squared is {bd2}.", h == 0), (f"The space diagonal is {Rd(math.sqrt(bd2), 1)}.", False)]
    need(not stm[3][1])
    return P(f"A box measures {l} × {w} × {h}. Select ALL true statements.", None, [f"Bottom diagonal² = {bd2}; space diagonal² = {bd2} + {h * h} = {d * d}."], options=stm,
             chk=chk_py("box_stmt", dims=[l, w, h]), tags=["multistep"])


@fam("012")
def s3_open(r, L):
    l, w, h, d = pick(r, BOXES)
    return P(f"A shipping box is {l} ft long, {w} ft wide and {h} ft tall.", None, ["Bottom diagonal.", "Square root.", "Space diagonal.", "Compare."],
             parts=[("Find the square of the bottom-face diagonal.", str(l * l + w * w), chk_val(f"{l}^2 + {w}^2")),
                    ("Find the bottom-face diagonal to the nearest tenth.", Rd(math.sqrt(l * l + w * w), 1), {"kind": "approx", "expr": f"√({l}^2 + {w}^2)", "places": 1}),
                    ("Find the space diagonal.", f"{d} ft", chk_val(f"√({l}^2 + {w}^2 + {h}^2)")),
                    (f"Would a {d - 1}-foot pole fit inside? Answer yes or no.", "yes", chk_py("rod_fits_yn", dims=[l, w, h], rod=d - 1))], tags=["multistep"])


# ======================================================================= S4 Distance between points
def dist_pts(r, L, triple=True):
    for _ in range(100):
        x1, y1 = r.randint(-7, 7), r.randint(-7, 7)
        if triple:
            a, b, c = pick(r, TRIPLES[:5])
            if r.random() < 0.5:
                a, b = b, a
            x2, y2 = x1 + a * pick(r, [1, -1]), y1 + b * pick(r, [1, -1])
        else:
            x2, y2 = r.randint(-7, 7), r.randint(-7, 7)
        if max(abs(x2), abs(y2)) <= 9 and (x1, y1) != (x2, y2) and x1 != x2 and y1 != y2:
            return (x1, y1), (x2, y2)
    raise Reject()


@fam("012")
def s4_integer(r, L):
    p, q = dist_pts(r, L)
    dx, dy = q[0] - p[0], q[1] - p[1]
    d = math.isqrt(dx * dx + dy * dy)
    drw = plane_draw(xr=(-10, 10), yr=(-10, 10), points=[(p[0], p[1], pt(*p)), (q[0], q[1], pt(*q))], label_every=2)
    return P(f"Find the distance between {pt(*p)} and {pt(*q)}." if L else "Find the distance between the two labeled points on the coordinate plane.", f"{d} units",
             [f"Horizontal leg: |{q[0]} - {paren(p[0])}| = {abs(dx)}. Vertical leg: |{q[1]} - {paren(p[1])}| = {abs(dy)}.", f"d = √({abs(dx)}² + {abs(dy)}²) = {d} units."],
             [f"{abs(dx) + abs(dy)} units", f"{d * d} units", f"{Rd(math.sqrt(abs(dx * dx - dy * dy)), 1)} units" if dx * dx != dy * dy else f"{d + 1} units"], chk_py("dist", p=list(p), q=list(q)),
             diagram={"draw": drw, "alt": f"Coordinate plane with points {pt(*p)} and {pt(*q)} labeled."} if L == 0 else None, tags=["graph"] if L == 0 else [])


@fam("12")
def s4_irrational(r, L):
    p, q = dist_pts(r, L, triple=False)
    s = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
    need(math.isqrt(s) ** 2 != s)
    exact = L == 2 and r.random() < 0.5
    return P(f"Find the distance between {pt(*p)} and {pt(*q)}" + (". Give the exact value." if exact else ", rounded to the nearest tenth."), f"√{s} units" if exact else f"{Rd(math.sqrt(s), 1)} units",
             [f"d² = ({q[0]} - {paren(p[0])})² + ({q[1]} - {paren(p[1])})² = {s}.", f"d = √{s}" + ("" if exact else f" ≈ {Rd(math.sqrt(s), 1)}") + " units."],
             [f"{abs(q[0] - p[0]) + abs(q[1] - p[1])} units", f"{s} units", f"{Rd(math.sqrt(s) + 1, 1)} units"],
             chk_py("dist", p=list(p), q=list(q)) if exact else chk_py("dist_round", p=list(p), q=list(q), places=1), tags=["misconception"])


@fam("12")
def s4_perimeter(r, L):
    a, b, c = pick(r, TRIPLES[:5])
    p0 = (r.randint(-6, 0), r.randint(-6, 0))
    pts_ = [p0, (p0[0] + b, p0[1]), (p0[0], p0[1] + a)]
    need(all(abs(v) <= 9 for p in pts_ for v in p))
    per = a + b + c
    return P(f"Find the perimeter of the triangle with vertices {pt(*pts_[0])}, {pt(*pts_[1])}, and {pt(*pts_[2])}.", f"{per} units",
             [f"Horizontal side {b}, vertical side {a}.", f"Slanted side = √({a}² + {b}²) = {c}.", f"Perimeter = {a} + {b} + {c} = {per} units."],
             [f"{a + b} units", f"{2 * (a + b)} units", f"{a * b // 2} units"], chk_py("perim", pts=[list(p) for p in pts_]), tags=["multistep"],
             diagram={"draw": plane_draw(xr=(-10, 10), yr=(-10, 10), polys=[(pts_, None, None, True)], points=[(p[0], p[1], pt(*p)) for p in pts_], label_every=2), "alt": f"Triangle with vertices {pt(*pts_[0])}, {pt(*pts_[1])}, {pt(*pts_[2])}."} if L == 1 else None)


@fam("2")
def s4_reverse(r, L):
    a, b, c = pick(r, TRIPLES[:5])
    x1, y1 = r.randint(-4, 4), r.randint(-4, 4)
    k = x1 + a
    return P(f"The distance between ({x1}, {y1}) and (k, {y1 + b}) is {c} units, and k > {x1}. Find k.", f"k = {k}",
             [f"(k - {paren(x1)})² + {b}² = {c}².", f"(k - {paren(x1)})² = {a * a}, so k - {paren(x1)} = {a} (k > {x1}).", f"k = {k}."],
             [f"k = {x1 - a}", f"k = {x1 + c}", f"k = {a}"], chk_py("dist_k", p=[x1, y1], y2=y1 + b, d=c, gt=x1), tags=["challenge", "reasoning"])


@fam("012", mode="mc")
def s4_closer(r, L):
    o = (r.randint(-3, 3), r.randint(-3, 3))
    P1 = (o[0] + r.randint(-6, 6), o[1] + r.randint(-6, 6))
    P2 = (o[0] + r.randint(-6, 6), o[1] + r.randint(-6, 6))
    d1 = (P1[0] - o[0]) ** 2 + (P1[1] - o[1]) ** 2
    d2 = (P2[0] - o[0]) ** 2 + (P2[1] - o[1]) ** 2
    need(d1 != d2 and d1 and d2)
    good = f"{pt(*P1)}" if d1 < d2 else f"{pt(*P2)}"
    opts = [(pt(*P1), d1 < d2), (pt(*P2), d2 < d1), ("They are the same distance", False), ("Cannot be determined", False)]
    return P(f"Which point is closer to {pt(*o)}: {pt(*P1)} or {pt(*P2)}?", good, [f"Squared distances: {d1} and {d2}.", f"The smaller is closer: {good}."], options=opts,
             chk=chk_py("closer", o=list(o), a=list(P1), b=list(P2)), tags=["reasoning"], mode="mc")


@fam("012")
def s4_error(r, L):
    p, q = dist_pts(r, 0)
    dx, dy = abs(q[0] - p[0]), abs(q[1] - p[1])
    return P(f"Gia found the distance between {pt(*p)} and {pt(*q)} as {dx} + {dy} = {dx + dy}. What is the correct distance?", str(math.isqrt(dx * dx + dy * dy)),
             ["Adding the legs gives the path along the grid, not the straight-line distance.", f"d = √({dx}² + {dy}²) = {math.isqrt(dx * dx + dy * dy)}."],
             [str(dx + dy), str(dx * dx + dy * dy), str(abs(dx - dy)) if dx != dy else str(dx + 1)], chk_py("dist", p=list(p), q=list(q)), tags=["error-analysis", "misconception"])


@fam("012")
def s4_select(r, L):
    a, b, c = pick(r, TRIPLES[:4])
    o = (r.randint(-3, 3), r.randint(-3, 3))
    goods = [(o[0] + a, o[1] + b), (o[0] - b, o[1] + a), (o[0] + c, o[1])]
    bads = [(o[0] + a, o[1] + a), (o[0] + b, o[1] + b), (o[0] + a + 1, o[1] + b)]
    opts = [(pt(*g), True) for g in goods] + [(pt(*x), False) for x in bads]
    need(len({o_[0] for o_ in opts}) == 6)
    return P(f"Select ALL points that are exactly {c} units from {pt(*o)}.", None, ["Compute each distance with the Pythagorean theorem."], options=opts,
             chk=chk_py("dist_is", o=list(o), d=c), tags=["reasoning"])


@fam("012")
def s4_open(r, L):
    p, q = dist_pts(r, 0)
    dx, dy = q[0] - p[0], q[1] - p[1]
    return P(f"Find the distance between A{pt(*p)} and B{pt(*q)}.", None, ["Horizontal change.", "Vertical change.", "Sum of squares.", "Root."],
             parts=[("Find the horizontal distance |x₂ - x₁|.", str(abs(dx)), chk_val(str(abs(dx)))), ("Find the vertical distance |y₂ - y₁|.", str(abs(dy)), chk_val(str(abs(dy)))),
                    ("Find AB².", str(dx * dx + dy * dy), chk_val(f"({dx})^2 + ({dy})^2")), ("Find AB.", str(math.isqrt(dx * dx + dy * dy)), chk_py("dist", p=list(p), q=list(q)))], tags=["multistep"])


# ======================================================================= S5 Volume of cylinders, cones, spheres
def vol_ans(coef, exact, unit):
    """coef: Fraction multiple of π. Exact text 'kπ' or rounded with π ≈ 3.14 to tenth."""
    if exact:
        return f"{N(coef) if coef != 1 else ''}π cubic {unit}"
    return f"{Rd(F(coef) * F('3.14'), 1)} cubic {unit}"


def vol_chk(coef, exact):
    return chk_val(f"({N(coef)})π") if exact else {"kind": "approx", "expr": f"({N(coef)})*3.14", "places": 1}


INSTR = {True: " Give your answer in terms of π.", False: " Use 3.14 for π and round to the nearest tenth."}


@fam("012")
def s5_cylinder(r, L):
    rad, h = r.randint(2, 9), r.randint(2, 15)
    u = pick(r, ["inches", "centimeters", "feet"])
    exact = r.random() < 0.5
    use_d = L >= 1 and r.random() < 0.5
    coef = F(rad * rad * h)
    dim = f"a diameter of {2 * rad}" if use_d else f"a radius of {rad}"
    wr = [vol_ans(F(4 * rad * rad * h) if use_d else F(2 * rad * h), exact, u), vol_ans(F(rad * h), exact, u), vol_ans(F(rad * rad * h, 3), exact, u)]
    return P(f"A cylinder has {dim} {u} and a height of {h} {u}. Find its volume.{INSTR[exact]}", vol_ans(coef, exact, u),
             ([f"Radius = {2 * rad} ÷ 2 = {rad} {u}."] if use_d else []) + [f"V = πr²h = π({rad})²({h}) = {N(coef)}π" + ("" if exact else f" ≈ {Rd(coef * F('3.14'), 1)}") + f" cubic {u}."],
             wr, vol_chk(coef, exact), diagram={"draw": cyl_draw(f"{'d' if use_d else 'r'} = {2 * rad if use_d else rad}", f"h = {h}", "cylinder", use_d), "alt": f"Cylinder with {dim} {u} and height {h} {u}."} if L == 0 else None,
             tags=["misconception"] if use_d else [])


@fam("012")
def s5_cone(r, L):
    rad, h = r.randint(2, 9), 3 * r.randint(1, 5) if L == 0 else r.randint(2, 15)
    u = pick(r, ["inches", "centimeters", "meters"])
    exact = r.random() < 0.5
    coef = F(rad * rad * h, 3)
    use_d = L >= 1 and r.random() < 0.4
    dim = f"diameter {2 * rad}" if use_d else f"radius {rad}"
    wr = [vol_ans(F(rad * rad * h), exact, u), vol_ans(F(4 * rad * rad * h, 3) if use_d else F(rad * h, 3), exact, u), vol_ans(F(2 * rad * h, 3), exact, u)]
    return P(f"A cone has {dim} {u} and height {h} {u}. Find its volume.{INSTR[exact]}", vol_ans(coef, exact, u),
             ([f"r = {rad}."] if use_d else []) + [f"V = (1/3)πr²h = (1/3)π({rad})²({h}) = {N(coef)}π" + ("" if exact else f" ≈ {Rd(coef * F('3.14'), 1)}") + f" cubic {u}."],
             wr, vol_chk(coef, exact), diagram={"draw": cyl_draw(f"r = {rad}", f"h = {h}", "cone"), "alt": f"Cone with radius {rad} {u} and height {h} {u}."} if L == 0 else None, tags=["misconception"])


@fam("012")
def s5_sphere(r, L):
    rad = r.randint(1, 9) * (1 if L < 2 else 1)
    u = pick(r, ["inches", "centimeters", "feet"])
    exact = r.random() < 0.5
    use_d = L >= 1 and r.random() < 0.5
    coef = F(4 * rad ** 3, 3)
    dim = f"diameter {2 * rad}" if use_d else f"radius {rad}"
    wr = [vol_ans(F(4 * (2 * rad) ** 3, 3) if use_d else F(4 * rad * rad, 3), exact, u), vol_ans(F(rad ** 3), exact, u), vol_ans(F(4 * rad ** 2), exact, u)]
    return P(f"A sphere has {dim} {u}. Find its volume.{INSTR[exact]}", vol_ans(coef, exact, u),
             ([f"r = {rad}."] if use_d else []) + [f"V = (4/3)πr³ = (4/3)π({rad})³ = {N(coef)}π" + ("" if exact else f" ≈ {Rd(coef * F('3.14'), 1)}") + f" cubic {u}."],
             wr, vol_chk(coef, exact), diagram={"draw": cyl_draw(f"{'d' if use_d else 'r'} = {2 * rad if use_d else rad}", "", "sphere", use_d), "alt": f"Sphere with {dim} {u}."} if L == 0 else None,
             tags=["misconception"] if use_d else [])


@fam("12", mode="mc")
def s5_compare(r, L):
    rad, h = r.randint(2, 8), r.randint(3, 12)
    q = pick(r, ["cone_cyl", "sphere_cyl"])
    if q == "cone_cyl":
        good = "The cylinder's volume is 3 times the cone's volume."
        opts = [(good, True), ("The cone's volume is 3 times the cylinder's volume.", False), ("They have the same volume.", False), ("The cylinder's volume is 2 times the cone's volume.", False)]
        p = f"A cone and a cylinder both have radius {rad} cm and height {h} cm. How do their volumes compare?"
    else:
        good = "The sphere's volume is 2/3 of the cylinder's volume."
        opts = [(good, True), ("The sphere's volume equals the cylinder's volume.", False), ("The sphere's volume is 1/3 of the cylinder's volume.", False), ("The sphere's volume is 3/2 of the cylinder's volume.", False)]
        p = f"A sphere of radius {rad} cm fits exactly inside a cylinder of radius {rad} cm and height {2 * rad} cm. How do their volumes compare?"
    r.shuffle(opts)
    return P(p, good, ["Compare the formulas: V(cone) = (1/3)πr²h; V(cylinder) = πr²h; V(sphere) = (4/3)πr³.", good], options=opts, chk=chk_py("vol_compare", q=q, r=rad, h=h), tags=["reasoning", "connections"], mode="mc")


@fam("012")
def s5_context(r, L):
    k = pick(r, ["can", "ball", "cone"])
    if k == "can":
        d, h = pick(r, [6, 8, 10]), r.randint(8, 16)
        coef = F((d // 2) ** 2 * h)
        return P(f"A soup can is {h} cm tall with a diameter of {d} cm. How much soup can it hold? Use 3.14 for π and round to the nearest tenth of a cubic centimeter.", f"{Rd(coef * F('3.14'), 1)} cubic centimeters",
                 [f"r = {d // 2} cm.", f"V = π({d // 2})²({h}) ≈ {Rd(coef * F('3.14'), 1)} cubic cm."], [f"{Rd(F(d * d * h) * F('3.14'), 1)} cubic centimeters", f"{Rd(F(d * h) * F('3.14'), 1)} cubic centimeters", f"{Rd(coef, 1)} cubic centimeters"],
                 {"kind": "approx", "expr": f"3.14*({d}/2)^2*{h}", "places": 1}, tags=["modeling", "misconception"])
    if k == "ball":
        d = pick(r, [6, 9, 12, 24])
        rad = F(d, 2)
        coef = F(4, 3) * rad ** 3
        return P(f"A ball has a diameter of {d} inches. Find its volume in terms of π.", f"{N(coef)}π cubic inches", [f"r = {N(rad)} in.", f"V = (4/3)π({N(rad)})³ = {N(coef)}π cubic inches."],
                 [f"{N(F(4, 3) * d ** 3)}π cubic inches", f"{N(4 * rad ** 2)}π cubic inches", f"{N(rad ** 3)}π cubic inches"], chk_val(f"(4/3)π({N(rad)})^3"), tags=["modeling", "misconception"])
    rad, h = r.randint(1, 4), r.randint(3, 9)
    coef = F(rad * rad * h, 3)
    return P(f"A paper cone cup has radius {rad} in. and height {h} in. About how many cubic inches of water does it hold? Use 3.14 for π and round to the nearest tenth.", f"{Rd(coef * F('3.14'), 1)} cubic inches",
             [f"V = (1/3)π({rad})²({h}) ≈ {Rd(coef * F('3.14'), 1)}."], [f"{Rd(F(rad * rad * h) * F('3.14'), 1)} cubic inches", f"{Rd(F(rad * h, 3) * F('3.14'), 1)} cubic inches", f"{Rd(coef, 1)} cubic inches"],
             {"kind": "approx", "expr": f"(1/3)*3.14*{rad}^2*{h}", "places": 1}, tags=["modeling"])


@fam("012")
def s5_error(r, L):
    d, h = 2 * r.randint(2, 6), r.randint(3, 12)
    rad = d // 2
    return P(f"A cylinder has diameter {d} m and height {h} m. Ike computed V = π({d})²({h}) = {d * d * h}π cubic meters. What is the correct volume in terms of π?", f"{rad * rad * h}π cubic meters",
             ["Ike used the diameter as the radius.", f"r = {rad}: V = π({rad})²({h}) = {rad * rad * h}π cubic meters."], [f"{d * d * h}π cubic meters", f"{d * h}π cubic meters", f"{N(F(rad * rad * h, 3))}π cubic meters"],
             chk_val(f"π({rad})^2*{h}"), tags=["error-analysis", "misconception"])


@fam("012")
def s5_select(r, L):
    rad, h = r.randint(2, 6), r.randint(2, 9)
    stm = [(f"The cylinder's volume is {rad * rad * h}π.", True), (f"The cone's volume is {N(F(rad * rad * h, 3))}π.", True), (f"The sphere's volume is {N(F(4 * rad ** 3, 3))}π.", True),
           (f"The cone's volume is {rad * rad * h}π.", False), (f"The sphere's volume is {4 * rad ** 2}π.", False), (f"The cylinder's volume is {2 * rad * h}π.", 2 * rad * h == rad * rad * h)]
    need(not stm[5][1])
    return P(f"A cylinder and a cone each have radius {rad} and height {h}; a sphere has radius {rad}. Select ALL true statements (volumes in cubic units).", None,
             ["V(cylinder) = πr²h; V(cone) = (1/3)πr²h; V(sphere) = (4/3)πr³."], options=stm, chk=chk_py("vol_stmt", r=rad, h=h), tags=["reasoning"])


@fam("012")
def s5_open(r, L):
    rad, h = r.randint(2, 6), 3 * r.randint(1, 4)
    return P(f"A cylinder, a cone and a sphere all have radius {rad} cm. The cylinder and cone have height {h} cm.", None, ["πr²h.", "(1/3)πr²h.", "(4/3)πr³.", "Rounded with 3.14."],
             parts=[("Volume of the cylinder (in terms of π)?", f"{rad * rad * h}π cubic centimeters", chk_val(f"π*{rad}^2*{h}")),
                    ("Volume of the cone (in terms of π)?", f"{N(F(rad * rad * h, 3))}π cubic centimeters", chk_val(f"(1/3)π*{rad}^2*{h}")),
                    ("Volume of the sphere (in terms of π)?", f"{N(F(4 * rad ** 3, 3))}π cubic centimeters", chk_val(f"(4/3)π*{rad}^3")),
                    ("Volume of the cylinder using 3.14 for π, to the nearest tenth?", f"{Rd(F(rad * rad * h) * F('3.14'), 1)} cubic centimeters", {"kind": "approx", "expr": f"3.14*{rad}^2*{h}", "places": 1})],
             tags=["multistep"])


# ======================================================================= S6 Solving for a missing dimension
@fam("012")
def s6_cyl_height(r, L):
    rad, h = r.randint(2, 8), r.randint(2, 15)
    coef = rad * rad * h
    q = pick(r, ["h", "r"]) if L else "h"
    if q == "h":
        return P(f"A cylinder has volume {coef}π cubic cm and radius {rad} cm. What is its height?", f"{h} cm", [f"{coef}π = π({rad})²h = {rad * rad}πh.", f"h = {coef} ÷ {rad * rad} = {h} cm."],
                 [f"{N(F(coef, rad))} cm", f"{N(F(coef, 2 * rad))} cm" if F(coef, 2 * rad) != h else f"{h + 1} cm", f"{N(F(coef, rad * rad * 3))} cm" if F(coef, 3 * rad * rad) != h else f"{h * 3} cm"],
                 chk_py("solve_dim", formula="π*r^2*h", known={"r": rad}, var="h", V=f"{coef}π"), tags=["reasoning"])
    return P(f"A cylinder has volume {coef}π cubic in. and height {h} in. What is its radius?", f"{rad} in.", [f"r² = {coef} ÷ {h} = {rad * rad}.", f"r = {rad} in."],
             [f"{rad * rad} in.", f"{2 * rad} in.", f"{N(F(coef, h * 2))} in." if F(coef, 2 * h) != rad else f"{rad + 1} in."], chk_py("solve_dim", formula="π*r^2*h", known={"h": h}, var="r", V=f"{coef}π"),
             tags=["reasoning"])


@fam("012")
def s6_cone(r, L):
    rad, h = r.randint(2, 8), 3 * r.randint(1, 5)
    coef = F(rad * rad * h, 3)
    q = pick(r, ["h", "r"]) if L else "h"
    if q == "h":
        return P(f"A cone has volume {N(coef)}π cubic cm and radius {rad} cm. What is its height?", f"{h} cm", [f"{N(coef)}π = (1/3)π({rad})²h.", f"h = 3 × {N(coef)} ÷ {rad * rad} = {h} cm."],
                 [f"{N(coef / (rad * rad))} cm", f"{N(3 * coef / rad)} cm", f"{h * 3} cm"], chk_py("solve_dim", formula="(1/3)*π*r^2*h", known={"r": rad}, var="h", V=f"{N(coef)}π"), tags=["reasoning", "misconception"])
    return P(f"A cone has volume {N(coef)}π cubic cm and height {h} cm. What is its radius?", f"{rad} cm", [f"r² = 3 × {N(coef)} ÷ {h} = {rad * rad}.", f"r = {rad} cm."],
             [f"{rad * rad} cm", f"{N(coef / h)} cm" if coef / h != rad else f"{rad + 2} cm", f"{2 * rad} cm"], chk_py("solve_dim", formula="(1/3)*π*r^2*h", known={"h": h}, var="r", V=f"{N(coef)}π"), tags=["reasoning"])


@fam("12")
def s6_sphere(r, L):
    rad = pick(r, [3, 6, 9, 12]) if L == 1 else r.randint(2, 10)
    coef = F(4 * rad ** 3, 3)
    q = pick(r, ["r", "d"]) if L == 2 else "r"
    ans = f"{rad if q == 'r' else 2 * rad} cm"
    return P(f"A sphere has volume {N(coef)}π cubic cm. What is its {'radius' if q == 'r' else 'diameter'}?", ans,
             [f"(4/3)πr³ = {N(coef)}π, so r³ = {N(coef)} × 3 ÷ 4 = {rad ** 3}.", f"r = ∛{rad ** 3} = {rad}" + ("" if q == "r" else f"; diameter = {2 * rad}") + " cm."],
             [f"{2 * rad if q == 'r' else rad} cm", f"{rad ** 3} cm", f"{N(coef * 3 / 4 / rad) if coef * 3 / 4 / rad != rad else rad + 1} cm"],
             chk_py("solve_dim", formula="(4/3)*π*r^3" if q == "r" else "(4/3)*π*(d/2)^3", known={}, var="r" if q == "r" else "d", V=f"{N(coef)}π"), tags=["challenge"])


@fam("012")
def s6_context(r, L):
    k = pick(r, ["tank", "glass"])
    if k == "tank":
        rad, h = r.randint(2, 6), r.randint(3, 10)
        V = F(rad * rad * h) * F("3.14")
        return P(f"A cylindrical tank holds {D(V)} cubic feet of water and has a radius of {rad} feet. Using 3.14 for π, how tall is the tank?", f"{h} feet",
                 [f"{D(V)} = 3.14({rad})²h = {D(F('3.14') * rad * rad)}h.", f"h = {D(V)} ÷ {D(F('3.14') * rad * rad)} = {h} feet."],
                 [f"{D(V / (F('3.14') * rad))} feet" if is_term(V / (F('3.14') * rad)) else f"{h + 2} feet", f"{h * rad} feet", f"{h + 1} feet"],
                 chk_py("solve_dim", formula="3.14*r^2*h", known={"r": rad}, var="h", V=D(V)), tags=["modeling"])
    rad, h = r.randint(2, 4), r.randint(6, 12)
    V = rad * rad * h
    return P(f"A cylindrical glass must hold {V}π cubic cm of juice. Its base has radius {rad} cm. What is the least height it can have?", f"{h} cm",
             [f"πr²h = {V}π → {rad * rad}h = {V}.", f"h = {h} cm."], [f"{N(F(V, rad))} cm", f"{N(F(V * 3, rad * rad))} cm", f"{h - 1} cm"], chk_py("solve_dim", formula="π*r^2*h", known={"r": rad}, var="h", V=f"{V}π"),
             tags=["modeling"])


@fam("2", mode="mc")
def s6_scale(r, L):
    k = pick(r, [2, 3])
    q = pick(r, ["radius", "height"])
    good = f"It is multiplied by {k * k}." if q == "radius" else f"It is multiplied by {k}."
    opts = [(f"It is multiplied by {k}.", q == "height"), (f"It is multiplied by {k * k}.", q == "radius"), (f"It is multiplied by {k ** 3}.", False), ("It does not change.", False)]
    return P(f"If the {q} of a cylinder is multiplied by {k} and the other dimension stays the same, what happens to the volume?", good,
             [f"V = πr²h. {'The radius is squared' if q == 'radius' else 'The height appears to the first power'}, so the volume is multiplied by {k * k if q == 'radius' else k}."],
             options=opts, chk=chk_py("scale_vol", q=q, k=k), tags=["reasoning", "challenge"], mode="mc")


@fam("012")
def s6_error(r, L):
    rad, h = r.randint(2, 6), 3 * r.randint(1, 4)
    coef = F(rad * rad * h, 3)
    return P(f"A cone has volume {N(coef)}π cubic in. and radius {rad} in. Bo divided {N(coef)} by {rad * rad} and said the height is {N(coef / (rad * rad))} in. What is the correct height?", f"{h} in.",
             ["Bo forgot the 1/3 in the cone formula.", f"h = 3 × {N(coef)} ÷ {rad * rad} = {h} in."], [f"{N(coef / (rad * rad))} in.", f"{N(coef / rad)} in.", f"{h + 3} in."],
             chk_py("solve_dim", formula="(1/3)*π*r^2*h", known={"r": rad}, var="h", V=f"{N(coef)}π"), tags=["error-analysis", "misconception"])


@fam("012")
def s6_select(r, L):
    rad, h = r.randint(2, 5), r.randint(2, 9)
    V = rad * rad * h
    opts = [(f"radius {rad}, height {h}", True), (f"radius {rad * 2}, height {N(F(h, 4))}" if F(h, 4).denominator == 1 else f"radius 1, height {V}", True), (f"radius 1, height {V}" if F(h, 4).denominator == 1 else f"radius {rad}, height {h}", None),
            (f"radius {h}, height {rad}", rad == h), (f"radius {rad}, height {2 * h}", False), (f"radius {rad + 1}, height {h}", False)]
    # rebuild deterministic set without duplicates
    opts = [(f"radius {rad}, height {h}", True), (f"radius 1, height {V}", True), (f"radius {rad * 2}, height {N(F(h, 4))}", True),
            (f"radius {rad}, height {2 * h}", False), (f"radius {rad + 1}, height {h}", False), (f"radius {h}, height {rad}", rad == h)]
    need(not opts[5][1] and F(h, 4).denominator == 1 or not opts[5][1])
    return P(f"Select ALL cylinders (dimensions in cm) with volume {V}π cubic cm.", None, ["Compute r²h for each choice."], options=opts, chk=chk_py("cyl_vol_is", V=V), tags=["reasoning"])


@fam("012")
def s6_open(r, L):
    rad, h = r.randint(2, 6), r.randint(3, 10)
    V = rad * rad * h
    return P(f"A cylinder has volume {V}π cubic cm and height {h} cm.", None, ["Write the formula.", "Divide.", "Square root.", "Diameter."],
             parts=[("Write an equation using V = πr²h.", f"{V}π = πr²({h})", {"kind": "text", "accept": [f"{V}π = πr²({h})"]}),
                    ("Find r².", str(rad * rad), chk_val(f"{V}/{h}")), ("Find r.", f"{rad} cm", chk_py("solve_dim", formula="π*r^2*h", known={"h": h}, var="r", V=f"{V}π")),
                    ("Find the diameter.", f"{2 * rad} cm", chk_val(f"2*√({V}/{h})"))], tags=["multistep"])


# ======================================================================= S7 Composite solids
def comp_draw(kind, labels):
    from matplotlib.patches import Ellipse, Arc

    def draw(path):
        fig, ax = new_fig(4.8, 5.6)
        R, H, e = 1.5, 2.6, 0.4
        ax.add_patch(Ellipse((0, 0), 2 * R, 2 * e, fill=False, lw=2, color="#1f4e9c"))
        ax.plot([-R, -R], [0, H], color="#1f4e9c", lw=2)
        ax.plot([R, R], [0, H], color="#1f4e9c", lw=2)
        ax.add_patch(Ellipse((0, H), 2 * R, 2 * e, fill=False, lw=1.5, ls="--", color="#1f4e9c"))
        if kind == "cone_top":
            ax.plot([-R, 0, R], [H, H + 1.8, H], color="#1f4e9c", lw=2)
            ax.plot([0, 0], [H, H + 1.8], color="#b23a3a", lw=1.2, ls="--")
            ax.text(0.1, H + 0.9, labels[2], color="#b23a3a", fontsize=12)
        else:  # hemisphere top
            ax.add_patch(Arc((0, H), 2 * R, 2 * R, theta1=0, theta2=180, lw=2, color="#1f4e9c"))
        ax.plot([0, R], [0, 0], color="#2e7d32", lw=1.5)
        ax.text(R / 2, -0.2, labels[0], color="#2e7d32", ha="center", va="top", fontsize=12)
        ax.plot([R + 0.25, R + 0.25], [0, H], color="#b23a3a", lw=1.2)
        ax.text(R + 0.35, H / 2, labels[1], color="#b23a3a", fontsize=12, va="center")
        ax.set_xlim(-2.4, 3.2)
        ax.set_ylim(-1.0, H + 2.2)
        ax.set_aspect("equal")
        ax.axis("off")
        save(fig, path)
    return draw


@fam("012")
def s7_cyl_cone(r, L):
    rad, h1, h2 = r.randint(2, 6), r.randint(3, 12), 3 * r.randint(1, 4)
    coef = F(rad * rad * h1) + F(rad * rad * h2, 3)
    exact = L == 0 or r.random() < 0.5
    u = "cm"
    return P(f"A solid is a cylinder (radius {rad} cm, height {h1} cm) with a cone (same radius, height {h2} cm) on top. Find the total volume.{INSTR[exact]}",
             f"{N(coef)}π cubic centimeters" if exact else f"{Rd(coef * F('3.14'), 1)} cubic centimeters",
             [f"Cylinder: π({rad})²({h1}) = {rad * rad * h1}π.", f"Cone: (1/3)π({rad})²({h2}) = {N(F(rad * rad * h2, 3))}π.", f"Total: {N(coef)}π" + ("" if exact else f" ≈ {Rd(coef * F('3.14'), 1)}") + " cubic cm."],
             [f"{rad * rad * (h1 + h2)}π cubic centimeters" if exact else f"{Rd(F(rad * rad * (h1 + h2)) * F('3.14'), 1)} cubic centimeters",
              f"{N(F(rad * rad * (h1 + h2), 3))}π cubic centimeters" if exact else f"{Rd(F(rad * rad * (h1 + h2), 3) * F('3.14'), 1)} cubic centimeters",
              f"{N(F(rad * rad * h1) - F(rad * rad * h2, 3))}π cubic centimeters" if exact else f"{Rd((F(rad * rad * h1) - F(rad * rad * h2, 3)) * F('3.14'), 1)} cubic centimeters"],
             chk_val(f"π*{rad}^2*{h1} + (1/3)π*{rad}^2*{h2}") if exact else {"kind": "approx", "expr": f"3.14*{rad}^2*{h1} + (1/3)*3.14*{rad}^2*{h2}", "places": 1},
             diagram={"draw": comp_draw("cone_top", [f"{rad} cm", f"{h1} cm", f"{h2} cm"]), "alt": f"Cylinder of radius {rad} cm and height {h1} cm topped by a cone of height {h2} cm."}, tags=["multistep", "graph"])


@fam("012")
def s7_silo(r, L):
    rad, h = r.randint(2, 6), r.randint(4, 15)
    coef = F(rad * rad * h) + F(2 * rad ** 3, 3)
    exact = r.random() < 0.6
    return P(f"A grain silo is a cylinder (radius {rad} m, height {h} m) topped by a hemisphere with the same radius. Find its volume.{INSTR[exact]}",
             f"{N(coef)}π cubic meters" if exact else f"{Rd(coef * F('3.14'), 1)} cubic meters",
             [f"Cylinder: {rad * rad * h}π.", f"Hemisphere: (1/2)(4/3)π({rad})³ = {N(F(2 * rad ** 3, 3))}π.", f"Total {N(coef)}π cubic m."],
             [f"{N(F(rad * rad * h) + F(4 * rad ** 3, 3))}π cubic meters" if exact else f"{Rd((F(rad * rad * h) + F(4 * rad ** 3, 3)) * F('3.14'), 1)} cubic meters",
              f"{rad * rad * h}π cubic meters" if exact else f"{Rd(F(rad * rad * h) * F('3.14'), 1)} cubic meters",
              f"{N(F(rad * rad * h) + F(2 * rad ** 2, 3))}π cubic meters" if exact else f"{Rd((F(rad * rad * h) + F(2 * rad ** 2, 3)) * F('3.14'), 1)} cubic meters"],
             chk_val(f"π*{rad}^2*{h} + (1/2)*(4/3)π*{rad}^3") if exact else {"kind": "approx", "expr": f"3.14*{rad}^2*{h} + (2/3)*3.14*{rad}^3", "places": 1},
             diagram={"draw": comp_draw("hemi", [f"{rad} m", f"{h} m"]), "alt": f"Cylinder of radius {rad} m and height {h} m topped by a hemisphere."} if L < 2 else None, tags=["modeling", "multistep"])


@fam("12")
def s7_subtract(r, L):
    R, h = r.randint(3, 7), 3 * r.randint(1, 4)
    rad = r.randint(1, R - 1)
    k = pick(r, ["cone_hole", "cyl_hole"])
    if k == "cone_hole":
        coef = F(R * R * h) - F(R * R * h, 3)
        p = f"A cone (radius {R} in., height {h} in.) is carved out of a cylinder with the same radius and height. What volume of material remains? Give your answer in terms of π."
        steps = [f"Cylinder {R * R * h}π; cone {N(F(R * R * h, 3))}π.", f"Remaining: {N(coef)}π cubic in."]
        e = f"π*{R}^2*{h} - (1/3)π*{R}^2*{h}"
        wr = [F(R * R * h, 3), F(R * R * h) + F(R * R * h, 3), F(R * R * h)]
    else:
        coef = F(R * R * h - rad * rad * h)
        p = f"A cylindrical pipe has outer radius {R} in., inner radius {rad} in., and length {h} in. What is the volume of the material in the pipe? Give your answer in terms of π."
        steps = [f"Outer {R * R * h}π - inner {rad * rad * h}π.", f"= {N(coef)}π cubic in."]
        e = f"π*{R}^2*{h} - π*{rad}^2*{h}"
        wr = [F((R - rad) ** 2 * h), F(R * R * h + rad * rad * h), F(R * R * h)]
    return P(p, f"{N(coef)}π cubic inches", steps, [f"{N(w)}π cubic inches" for w in wr], chk_val(e), tags=["multistep", "misconception"])


@fam("2")
def s7_missing(r, L):
    rad, h1, h2 = r.randint(2, 5), r.randint(3, 9), 3 * r.randint(1, 4)
    coef = F(rad * rad * h1) + F(rad * rad * h2, 3)
    return P(f"A cylinder of radius {rad} cm topped by a cone of the same radius has total volume {N(coef)}π cubic cm. The cone is {h2} cm tall. How tall is the cylinder?", f"{h1} cm",
             [f"Cone volume: (1/3)π({rad})²({h2}) = {N(F(rad * rad * h2, 3))}π.", f"Cylinder: {N(coef)}π - {N(F(rad * rad * h2, 3))}π = {rad * rad * h1}π.", f"h = {rad * rad * h1} ÷ {rad * rad} = {h1} cm."],
             [f"{N(coef / (rad * rad))} cm", f"{h1 + h2} cm", f"{N((coef - rad * rad * h2) / (rad * rad))} cm" if (coef - rad * rad * h2) / (rad * rad) != h1 else f"{h1 + 1} cm"],
             chk_py("composite_h", r=rad, h2=h2, V=f"{N(coef)}π"), tags=["challenge", "reasoning"])


@fam("012")
def s7_error(r, L):
    rad, h1, h2 = r.randint(2, 5), r.randint(3, 9), 3 * r.randint(1, 3)
    good = F(rad * rad * h1) + F(rad * rad * h2, 3)
    return P(f"A cylinder (radius {rad}, height {h1}) has a cone (same radius, height {h2}) on top. Jin found the volume as π({rad})²({h1 + h2}) = {rad * rad * (h1 + h2)}π. What is the correct volume in terms of π?",
             f"{N(good)}π", ["Jin treated the whole solid as one cylinder; the cone holds only 1/3 of a cylinder with the same base and height.", f"{rad * rad * h1}π + {N(F(rad * rad * h2, 3))}π = {N(good)}π."],
             [f"{rad * rad * (h1 + h2)}π", f"{N(F(rad * rad * (h1 + h2), 3))}π", f"{rad * rad * h1}π"], chk_val(f"π*{rad}^2*{h1} + (1/3)π*{rad}^2*{h2}"), tags=["error-analysis", "misconception"])


@fam("012")
def s7_select(r, L):
    rad, h = r.randint(2, 5), r.randint(3, 9)
    cyl, hemi = F(rad * rad * h), F(2 * rad ** 3, 3)
    stm = [(f"The cylinder part is {N(cyl)}π.", True), (f"The hemisphere part is {N(hemi)}π.", True), (f"The total is {N(cyl + hemi)}π.", True),
           (f"The hemisphere part is {N(2 * hemi)}π.", False), (f"The total is {N(cyl + 2 * hemi)}π.", False), (f"The cylinder part is {N(F(rad * rad * h, 3))}π.", False)]
    return P(f"A capsule-shaped tank is a cylinder (radius {rad}, height {h}) with a hemisphere on one end. Select ALL true statements (volumes in cubic units).", None,
             ["Hemisphere = half of (4/3)πr³."], options=stm, chk=chk_py("capsule_stmt", r=rad, h=h), tags=["multistep"])


@fam("012")
def s7_open(r, L):
    rad, h1, h2 = r.randint(2, 5), r.randint(3, 9), 3 * r.randint(1, 3)
    return P(f"An ice cream cone is modeled as a cone (radius {rad} cm, height {h2} cm) with a hemisphere of ice cream (radius {rad} cm) on top.", None,
             ["Cone formula.", "Hemisphere.", "Add.", "Approximate."],
             parts=[("Volume of the cone in terms of π?", f"{N(F(rad * rad * h2, 3))}π cubic centimeters", chk_val(f"(1/3)π*{rad}^2*{h2}")),
                    ("Volume of the hemisphere in terms of π?", f"{N(F(2 * rad ** 3, 3))}π cubic centimeters", chk_val(f"(2/3)π*{rad}^3")),
                    ("Total volume in terms of π?", f"{N(F(rad * rad * h2, 3) + F(2 * rad ** 3, 3))}π cubic centimeters", chk_val(f"(1/3)π*{rad}^2*{h2} + (2/3)π*{rad}^3")),
                    ("Total volume using 3.14 for π, to the nearest tenth?", f"{Rd((F(rad * rad * h2, 3) + F(2 * rad ** 3, 3)) * F('3.14'), 1)} cubic centimeters",
                     {"kind": "approx", "expr": f"3.14*((1/3)*{rad}^2*{h2} + (2/3)*{rad}^3)", "places": 1})], tags=["modeling", "multistep"])


SKILLS = {
    1: dict(name="Pythagorean theorem and its converse", std=["8.G.B.6", "8.G.B.7"], fams=[s1_hyp, s1_leg, s1_converse, s1_which_right, s1_missing_var], extra=[s1_error, s1_select, s1_open]),
    2: dict(name="Two-dimensional applications of the Pythagorean theorem", std=["8.G.B.7"], fams=[s2_ladder, s2_rect_diag, s2_walk, s2_isosceles_height, s2_ramp], extra=[s2_error, s2_select, s2_open]),
    3: dict(name="Three-dimensional applications of the Pythagorean theorem", std=["8.G.B.7"], fams=[s3_box_diag, s3_cone_slant, s3_pyramid, s3_fits], extra=[s3_error, s3_select, s3_open]),
    4: dict(name="Distance between points using the Pythagorean theorem", std=["8.G.B.8"], fams=[s4_integer, s4_irrational, s4_perimeter, s4_reverse, s4_closer], extra=[s4_error, s4_select, s4_open]),
    5: dict(name="Volume of cylinders, cones, and spheres", std=["8.G.C.9"], fams=[s5_cylinder, s5_cone, s5_sphere, s5_compare, s5_context], extra=[s5_error, s5_select, s5_open]),
    6: dict(name="Solving for a missing dimension", std=["8.G.C.9", "8.EE.A.2"], fams=[s6_cyl_height, s6_cone, s6_sphere, s6_context, s6_scale], extra=[s6_error, s6_select, s6_open]),
    7: dict(name="Volume of composite solids", std=["8.G.C.9"], fams=[s7_cyl_cone, s7_silo, s7_subtract, s7_missing], extra=[s7_error, s7_select, s7_open]),
}
