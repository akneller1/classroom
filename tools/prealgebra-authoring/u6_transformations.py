"""Unit 6 — Congruence and Similarity (congruence-similarity)."""
from lib import *

UNIT_ID = "congruence-similarity"
ABBR = "cgs"


# ---------------------------------------------------------------- transformation helpers (authoring side)
def rot(p, deg):           # counterclockwise about origin, deg in {90, 180, 270}
    x, y = p
    return {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[deg % 360]


def refl(p, axis):
    x, y = p
    return {"x-axis": (x, -y), "y-axis": (-x, y), "y = x": (y, x), "y = -x": (-y, -x)}[axis]


def refl_line(p, kind, c):
    x, y = p
    return (2 * c - x, y) if kind == "x" else (x, 2 * c - y)


def trans(p, a, b):
    return (p[0] + a, p[1] + b)


def dil(p, k, c=(0, 0)):
    return (c[0] + k * (p[0] - c[0]), c[1] + k * (p[1] - c[1]))


def rot_name(deg):
    return {90: "rotation 90° counterclockwise about the origin", 180: "rotation 180° about the origin", 270: "rotation 90° clockwise about the origin"}[deg]


def tr_name(a, b):
    parts = []
    if a:
        parts.append(f"{abs(a)} unit{'s' if abs(a) != 1 else ''} {'right' if a > 0 else 'left'}")
    if b:
        parts.append(f"{abs(b)} unit{'s' if abs(b) != 1 else ''} {'up' if b > 0 else 'down'}")
    return "translation " + " and ".join(parts)


def dil_name(k):
    return f"dilation with scale factor {N(k)} centered at the origin"


def refl_name(axis):
    return f"reflection over the {axis}" if "axis" in axis else f"reflection over the line {axis}"


def poly(r, n=3, box=(-6, 6), quadrant=None):
    for _ in range(200):
        lo, hi = box
        if quadrant == 1:
            pts = [(r.randint(1, hi), r.randint(1, hi)) for _ in range(n)]
        else:
            pts = [(r.randint(lo, hi), r.randint(lo, hi)) for _ in range(n)]
        if len(set(pts)) < n:
            continue
        area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
        if abs(area) < 6:
            continue
        if n == 4:
            # convex & simple: sort by angle around centroid
            cx, cy = sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4
            pts.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        return pts
    raise Reject()


LET = "ABCDEFGH"


def plabel(pts, prime=False, start=0):
    return ", ".join(f"{LET[start + i]}{chr(8242) if prime else ''}{pt(*p)}" for i, p in enumerate(pts))


def fig_draw(pre, img=None, win=None, labels=True, extra_lines=(), start=0, img2=None):
    allp = list(pre) + list(img or []) + list(img2 or [])
    m = max(6, max(abs(float(v)) for p in allp for v in p) + 1)
    m = int(math.ceil(m))
    win = win or (-m, m)

    def draw(path):
        fig, ax = new_fig(6.3, 6.3)
        grid_axes(ax, win, win, 1, label_every=1 if m <= 8 else 2)
        for kind, c in extra_lines:
            if kind == "x":
                ax.plot([c, c], list(win), color="#7b3fa0", lw=1.6, ls=":")
            elif kind == "y":
                ax.plot(list(win), [c, c], color="#7b3fa0", lw=1.6, ls=":")
            elif kind == "y=x":
                ax.plot(list(win), list(win), color="#7b3fa0", lw=1.6, ls=":")
        for shape, col, ls, prime in ((pre, COLORS[0], "-", False), (img, COLORS[1], "--", True), (img2, COLORS[2], "-.", "2")):
            if not shape:
                continue
            xs = [float(p[0]) for p in shape] + [float(shape[0][0])]
            ys = [float(p[1]) for p in shape] + [float(shape[0][1])]
            ax.plot(xs, ys, color=col, lw=2.2, ls=ls)
            ax.fill(xs, ys, color=col, alpha=0.10)
            if labels:
                cx, cy = sum(xs[:-1]) / len(shape), sum(ys[:-1]) / len(shape)
                for i, p in enumerate(shape):
                    dx, dy = float(p[0]) - cx, float(p[1]) - cy
                    d = math.hypot(dx, dy) or 1
                    lab = LET[start + i] + ("′" if prime is True else "″" if prime == "2" else "")
                    ax.text(float(p[0]) + 0.45 * dx / d, float(p[1]) + 0.45 * dy / d, lab, ha="center", va="center", fontsize=13, fontweight="bold", color=col)
        save(fig, path)
    return draw


def alt_of(pre, img=None, img2=None, name="Triangle"):
    s = f"{name} {''.join(LET[:len(pre)])} with " + plabel(pre)
    if img:
        s += f"; image {''.join(c + '′' for c in LET[:len(pre)])} with " + plabel(img, True)
    if img2:
        s += "; second image with " + ", ".join(f"{LET[i]}″{pt(*p)}" for i, p in enumerate(img2))
    return s + "."


def random_transform(r, kinds=("translation", "reflection", "rotation", "dilation")):
    k = pick(r, kinds)
    if k == "translation":
        a, b = nz(r, -6, 6), r.randint(-6, 6)
        return k, tr_name(a, b), (lambda p: trans(p, a, b)), ("t", a, b)
    if k == "reflection":
        ax_ = pick(r, ["x-axis", "y-axis", "y = x"])
        return k, refl_name(ax_), (lambda p: refl(p, ax_)), ("r", ax_)
    if k == "rotation":
        d = pick(r, [90, 180, 270])
        return k, rot_name(d), (lambda p: rot(p, d)), ("o", d)
    kk = pick(r, [F(2), F(3), F(1, 2)])
    return k, dil_name(kk), (lambda p: dil(p, kk)), ("d", N(kk))


# ======================================================================= S1 Identifying transformations
@fam("012", mode="mc")
def s1_name_graph(r, L):
    k, name, f, spec = random_transform(r)
    pre = poly(r, 3, (-5, 5) if k != "dilation" else (-3, 3))
    if k == "dilation" and spec[1] == "1/2":
        pre = [(2 * x, 2 * y) for x, y in pre]
    img = [f(p) for p in pre]
    need(all(abs(v) <= 9 for p in img for v in p) and set(img) != set(pre))
    kinds = ["translation", "reflection", "rotation", "dilation"]
    opts = [(kk, kk == k) for kk in kinds]
    return P("Triangle ABC is mapped to triangle A′B′C′ as shown. Which type of transformation is it?", k,
             [{"translation": "Every point slides the same distance in the same direction; orientation is unchanged.", "reflection": "The figure is flipped over a line; orientation is reversed.",
               "rotation": "The figure turns about a point; orientation is kept.", "dilation": "The figure changes size but keeps its shape."}[k], f"It is a {name}."],
             options=opts, chk=chk_py("xf_type", pre=pre, img=img), diagram={"draw": fig_draw(pre, img), "alt": alt_of(pre, img)}, tags=["graph"], mode="mc")


@fam("012")
def s1_name_coords(r, L):
    k, name, f, spec = random_transform(r, ("translation", "reflection", "rotation") if L < 2 else ("translation", "reflection", "rotation", "dilation"))
    pre = poly(r, 3, (-5, 5) if k != "dilation" else (-3, 3))
    img = [f(p) for p in pre]
    need(set(img) != set(pre))
    others = [refl_name("x-axis"), refl_name("y-axis"), rot_name(180), rot_name(90), tr_name(3, -2), dil_name(F(2)), refl_name("y = x"), rot_name(270)]
    wrong = [o for o in others if o != name]
    r.shuffle(wrong)
    return P(f"Triangle ABC has vertices {plabel(pre)}. Its image has vertices {plabel(img, True)}. Describe the single transformation precisely.", name,
             ["Compare each vertex with its image.", f"The rule matches a {name}."], wrong, chk_py("xf_maps", pre=pre, img=img, show=[pt(*img[0])]), tags=["reasoning"])


@fam("012", mode="sa")
def s1_congruent(r, L):
    k, name, f, spec = random_transform(r)
    ans = "yes" if k != "dilation" or spec[1] == "1" else "no"
    return P(f"A figure undergoes a {name}. Is the image always congruent to the original figure? Answer yes or no.", ans,
             ["Translations, reflections and rotations are rigid motions: they preserve lengths and angle measures.", "A dilation with scale factor other than 1 changes lengths, so the image is similar but not congruent."],
             ["no" if ans == "yes" else "yes"], chk_py("xf_congruent", name=name), tags=["reasoning"], mode="sa")


@fam("12", mode="mc")
def s1_properties(r, L):
    k = pick(r, ["translation", "reflection", "rotation", "dilation"])
    good = {"translation": "Lengths, angles and orientation are all preserved.", "reflection": "Lengths and angles are preserved, but orientation is reversed.",
            "rotation": "Lengths, angles and orientation are all preserved.", "dilation": "Angles are preserved, but lengths are multiplied by the scale factor."}[k]
    opts = [("Lengths, angles and orientation are all preserved.", k in ("translation", "rotation")), ("Lengths and angles are preserved, but orientation is reversed.", k == "reflection"),
            ("Angles are preserved, but lengths are multiplied by the scale factor.", k == "dilation"), ("Lengths are preserved, but angles change.", False)]
    return P(f"Which statement is true about every {k}?", good, [good], options=opts, chk=chk_py("xf_property", k=k), tags=["reasoning"], mode="mc")


@fam("012")
def s1_error(r, L):
    pre = poly(r, 3, (1, 6), quadrant=1)
    img = [refl(p, "y-axis") for p in pre]
    opts = [(refl_name("y-axis"), True), (refl_name("x-axis"), False), (rot_name(90), False), (tr_name(-2 * pre[0][0], 0), False)]
    r.shuffle(opts)
    return P(f"Triangle ABC {plabel(pre)} maps to A′B′C′ {plabel(img, True)}. Jada says it is a {refl_name('x-axis')} because \"the triangle flipped.\" Which transformation is it actually?",
             refl_name("y-axis"), ["x-coordinates changed sign while y-coordinates stayed the same: (x, y) → (-x, y).", "That is a reflection over the y-axis (left-right flip)."],
             options=opts, chk=chk_py("xf_maps", pre=pre, img=img), tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s1_select(r, L):
    pre = poly(r, 3, (-5, 5))
    stm = [(rot_name(180), True), (refl_name("x-axis"), True), (tr_name(2, 0), True), (dil_name(F(2)), False), (dil_name(F(1, 2)), False), ("a stretch that doubles only the x-coordinates", False)]
    return P("Select ALL transformations that always produce an image congruent to the original figure.", None, ["Rigid motions (translations, reflections, rotations) preserve size and shape."],
             options=stm, chk=chk_py("xf_congruent_any"), tags=["reasoning"])


@fam("012")
def s1_open(r, L):
    pre = poly(r, 3, (-4, 4))
    a, b = nz(r, -4, 4), nz(r, -4, 4)
    img = [trans(p, a, b) for p in pre]
    return P(f"Triangle ABC {plabel(pre)} maps to A′B′C′ {plabel(img, True)}.", None, ["Compare A and A′.", "Same shift for every vertex.", "Rigid motion.", "Rule."],
             parts=[("Which type of transformation is it?", "translation", chk_py("xf_type", pre=pre, img=img)), ("How far right (+) or left (-) does each point move?", str(a), chk_val(str(a))),
                    ("How far up (+) or down (-) does each point move?", str(b), chk_val(str(b))),
                    ("Is A′B′C′ congruent to ABC? Answer yes or no.", "yes", {"kind": "text", "accept": ["yes"]})], tags=["graph"])


# ======================================================================= S2 Rotations
@fam("012")
def s2_point(r, L):
    p = (nz(r, -7, 7), nz(r, -7, 7))
    d = pick(r, [180, 90, 270] if L else [180, 90])
    img = rot(p, d)
    wrong = [pt(*rot(p, 360 - d)) if d != 180 else pt(p[0], -p[1]), pt(*refl(p, "y = x")), pt(-p[0], p[1])]
    return P(f"Point P{pt(*p)} is rotated {rot_name(d)[9:]}. What are the coordinates of P′?", pt(*img),
             [{90: "90° counterclockwise: (x, y) → (-y, x).", 180: "180°: (x, y) → (-x, -y).", 270: "90° clockwise: (x, y) → (y, -x)."}[d], f"P′{pt(*img)}."], wrong,
             chk_py("xf_point", p=list(p), desc=rot_name(d)), tags=["misconception"])


@fam("012")
def s2_figure_vertex(r, L):
    pre = poly(r, 3, (-5, 5))
    d = pick(r, [90, 180, 270])
    img = [rot(p, d) for p in pre]
    k = r.randint(0, 2)
    return P(f"Triangle ABC with vertices {plabel(pre)} is rotated {rot_name(d)[9:]}. What are the coordinates of {LET[k]}′?", pt(*img[k]),
             [f"Apply the rule to {LET[k]}{pt(*pre[k])}.", f"{LET[k]}′{pt(*img[k])}."], [pt(*rot(pre[k], 360 - d)) if d != 180 else pt(-pre[k][0], pre[k][1]), pt(*refl(pre[k], "y = x")), pt(*img[(k + 1) % 3])],
             chk_py("xf_point", p=list(pre[k]), desc=rot_name(d)), diagram={"draw": fig_draw(pre), "alt": alt_of(pre)} if L == 0 else None, tags=["graph"] if L == 0 else [])


@fam("12")
def s2_identify_angle(r, L):
    pre = poly(r, 3, (-5, 5))
    d = pick(r, [90, 180, 270])
    img = [rot(p, d) for p in pre]
    return P(f"Triangle ABC {plabel(pre)} is rotated about the origin to A′B′C′ {plabel(img, True)}. Describe the rotation (angle and direction).", rot_name(d),
             ["Test the rotation rules on one vertex, then confirm with the others.", rot_name(d) + "."], [rot_name(x) for x in (90, 180, 270) if x != d] + [refl_name("y = x")],
             chk_py("xf_maps", pre=pre, img=img), diagram={"draw": fig_draw(pre, img), "alt": alt_of(pre, img)} if L == 1 else None, tags=["reasoning", "graph"] if L == 1 else ["reasoning"])


@fam("012", mode="mc")
def s2_property(r, L):
    pre = poly(r, 3, (-5, 5))
    d = pick(r, [90, 180, 270])
    i, j = 0, 1
    ln = math.dist(pre[i], pre[j])
    q = pick(r, ["length", "angle"])
    if q == "length":
        good = f"A′B′ = AB"
        opts = [(good, True), ("A′B′ = 2AB", False), ("A′B′ is half of AB", False), ("A′B′ depends on the angle of rotation", False)]
    else:
        good = "∠A′ has the same measure as ∠A"
        opts = [(good, True), ("∠A′ is 90° more than ∠A", False), ("∠A′ and ∠A are supplementary", False), ("∠A′ is twice ∠A", False)]
    r.shuffle(opts)
    return P(f"Triangle ABC is rotated {rot_name(d)[9:]} to form A′B′C′. Which statement must be true?", good, ["Rotations are rigid motions: they preserve lengths and angle measures."],
             options=opts, chk={"kind": "text", "accept": [good]}, tags=["reasoning"], mode="mc")


@fam("2")
def s2_reverse(r, L):
    p = (nz(r, -7, 7), nz(r, -7, 7))
    d = pick(r, [90, 270])
    img = rot(p, d)
    return P(f"After a {rot_name(d)}, the image of point Q is Q′{pt(*img)}. What were the coordinates of Q?", pt(*p),
             ["Undo the rotation with the opposite rotation.", f"{rot_name(360 - d)} of Q′ gives Q{pt(*p)}."], [pt(*rot(img, d)), pt(-img[0], -img[1]), pt(*img[::-1])],
             chk_py("xf_preimage", img=list(img), desc=rot_name(d)), tags=["reasoning", "challenge"])


@fam("012")
def s2_error(r, L):
    p = (r.randint(1, 7), r.randint(1, 7))
    need(p[0] != p[1])
    img = rot(p, 90)
    return P(f"Ray rotated P{pt(*p)} 90° counterclockwise about the origin and got {pt(p[1], -p[0])}. What is the correct image?", pt(*img),
             ["Ray used the clockwise rule (x, y) → (y, -x).", f"Counterclockwise: (x, y) → (-y, x) = {pt(*img)}."], [pt(p[1], -p[0]), pt(-p[0], -p[1]), pt(p[1], p[0])],
             chk_py("xf_point", p=list(p), desc=rot_name(90)), tags=["error-analysis", "misconception"])


@fam("012")
def s2_select(r, L):
    p = (nz(r, -6, 6), nz(r, -6, 6))
    need(abs(p[0]) != abs(p[1]))
    img = rot(p, 180)
    stm = [(rot_name(180), True), (f"rotation 180° clockwise about the origin", True), (f"{refl_name('x-axis')} followed by a {refl_name('y-axis')}", True),
           (rot_name(90), False), (refl_name("y = x"), False), (refl_name("x-axis"), False)]
    return P(f"Point P{pt(*p)} maps to P′{pt(*img)}. Select ALL transformations (or sequences) that map P to P′.", None, ["180° in either direction gives (-x, -y); so do two reflections over the axes."],
             options=stm, chk=chk_py("xf_point_any", p=list(p), img=list(img)), tags=["reasoning"])


@fam("012")
def s2_open(r, L):
    pre = poly(r, 3, (-4, 4))
    img = [rot(p, 90) for p in pre]
    return P(f"Rotate triangle ABC {plabel(pre)} 90° counterclockwise about the origin.", None, ["(x, y) → (-y, x).", "Apply to B.", "Apply to C.", "Rigid motion."],
             parts=[("Find A′.", pt(*img[0]), chk_py("xf_point", p=list(pre[0]), desc=rot_name(90))), ("Find B′.", pt(*img[1]), chk_py("xf_point", p=list(pre[1]), desc=rot_name(90))),
                    ("Find C′.", pt(*img[2]), chk_py("xf_point", p=list(pre[2]), desc=rot_name(90))),
                    ("How does the length A′B′ compare with AB?", "They are equal.", {"kind": "text", "accept": ["They are equal."]})], tags=["graph"])


# ======================================================================= S3 Reflections
@fam("012")
def s3_point(r, L):
    p = (nz(r, -7, 7), nz(r, -7, 7))
    if L < 2:
        ax_ = pick(r, ["x-axis", "y-axis"] if L == 0 else ["x-axis", "y-axis", "y = x"])
        img, name = refl(p, ax_), refl_name(ax_)
        wrong = [pt(*refl(p, "y-axis" if ax_ == "x-axis" else "x-axis")), pt(-p[0], -p[1]), pt(p[1], p[0]) if ax_ != "y = x" else pt(-p[1], -p[0])]
    else:
        kind, c = pick(r, ["x", "y"]), nz(r, -4, 4)
        img = refl_line(p, kind, c)
        name = f"reflection over the line {kind} = {c}"
        wrong = [pt(-p[0], p[1]) if kind == "x" else pt(p[0], -p[1]), pt(c - p[0], p[1]) if kind == "x" else pt(p[0], c - p[1]), pt(p[0] + 2 * c, p[1]) if kind == "x" else pt(p[0], p[1] + 2 * c)]
    need(img != p)
    return P(f"Point P{pt(*p)} is reflected over the {name[19:]}. What are the coordinates of P′?", pt(*img),
             ["The line of reflection is the perpendicular bisector of PP′: P′ is the same distance from the line on the other side.", f"P′{pt(*img)}."], wrong,
             chk_py("xf_point", p=list(p), desc=name), tags=["misconception"])


@fam("012")
def s3_figure(r, L):
    pre = poly(r, 3, (-5, 5))
    ax_ = pick(r, ["x-axis", "y-axis"] if L == 0 else ["x-axis", "y-axis", "y = x"])
    img = [refl(p, ax_) for p in pre]
    q = pick(r, ["vertex", "line"])
    if q == "vertex":
        k = r.randint(0, 2)
        return P(f"Triangle ABC {plabel(pre)} is reflected over the {ax_ if 'axis' in ax_ else 'line ' + ax_}. What are the coordinates of {LET[k]}′?", pt(*img[k]),
                 [f"Apply the reflection rule to {LET[k]}{pt(*pre[k])}."], [pt(*refl(pre[k], "y-axis" if ax_ != "y-axis" else "x-axis")), pt(-pre[k][0], -pre[k][1]), pt(pre[k][1], pre[k][0]) if ax_ != "y = x" else pt(-pre[k][1], -pre[k][0])],
                 chk_py("xf_point", p=list(pre[k]), desc=refl_name(ax_)), tags=["reasoning"])
    return P("Triangle ABC is reflected to form A′B′C′, as shown. What is the line of reflection?", ax_ if "axis" in ax_ else f"the line {ax_}",
             ["Each vertex and its image are the same distance from the line, on opposite sides."], [a if "axis" in a else f"the line {a}" for a in ["x-axis", "y-axis", "y = x", "y = -x"] if a != ax_][:3],
             chk_py("refl_line_name", pre=pre, img=img), diagram={"draw": fig_draw(pre, img), "alt": alt_of(pre, img)}, tags=["graph"])


@fam("12")
def s3_vertical_line(r, L):
    pre = poly(r, 3, (-3, 5))
    c = nz(r, -2, 3)
    kind = pick(r, ["x", "y"])
    img = [refl_line(p, kind, c) for p in pre]
    need(all(abs(v) <= 9 for p in img for v in p))
    return P(f"Triangle ABC {plabel(pre)} is reflected to A′B′C′ {plabel(img, True)}. What is the equation of the line of reflection?", f"{kind} = {c}",
             [f"The midpoint of A and A′ is {pt(*[(a + b) / 2 for a, b in zip(pre[0], img[0])])}; every midpoint lies on the line {kind} = {c}."],
             [f"{kind} = {-c}", f"{'y' if kind == 'x' else 'x'} = {c}", f"{kind} = {2 * c}"], chk_py("refl_line_eq", pre=pre, img=img), tags=["reasoning"])


@fam("012", mode="mc")
def s3_orientation(r, L):
    good = "The order of the vertices reverses (clockwise becomes counterclockwise)."
    opts = [(good, True), ("The figure becomes larger.", False), ("The angle measures change.", False), ("The side lengths change.", False)]
    r.shuffle(opts)
    shape = pick(r, ["triangle PQR", "quadrilateral WXYZ", "triangle DEF"])
    ax_ = pick(r, ["x-axis", "y-axis", "line y = x"])
    return P(f"{shape.capitalize()} is reflected over the {ax_}. Which statement describes how the image differs from the original?", good,
             ["Reflections preserve lengths and angles but reverse orientation."], options=opts, chk={"kind": "text", "accept": [good]}, tags=["reasoning"], mode="mc")


@fam("012")
def s3_error(r, L):
    p = (nz(r, -6, 6), nz(r, -6, 6))
    need(abs(p[0]) != abs(p[1]))
    return P(f"Eli reflected P{pt(*p)} over the x-axis and wrote P′{pt(-p[0], p[1])}. What is the correct image?", pt(p[0], -p[1]),
             ["Reflecting over the x-axis keeps x and changes the sign of y.", f"P′{pt(p[0], -p[1])}. Eli reflected over the y-axis instead."], [pt(-p[0], p[1]), pt(-p[0], -p[1]), pt(p[1], p[0])],
             chk_py("xf_point", p=list(p), desc=refl_name("x-axis")), tags=["error-analysis", "misconception"])


@fam("012")
def s3_select(r, L):
    p = (nz(r, -6, 6), nz(r, -6, 6))
    need(abs(p[0]) != abs(p[1]))
    img = (p[0], -p[1])
    stm = [(refl_name("x-axis"), True), (f"{rot_name(180)} followed by a {refl_name('y-axis')}", True), (f"{refl_name('y-axis')} followed by a {rot_name(180)}", True),
           (refl_name("y-axis"), False), (rot_name(180), False), (refl_name("y = x"), False)]
    return P(f"Select ALL transformations (or sequences) that map P{pt(*p)} to P′{pt(*img)}.", None, ["Apply each rule in order and compare with P′."], options=stm,
             chk=chk_py("xf_point_any", p=list(p), img=list(img)), tags=["reasoning"])


@fam("012")
def s3_open(r, L):
    pre = poly(r, 3, (-4, 4))
    img = [refl(p, "y-axis") for p in pre]
    return P(f"Reflect triangle ABC {plabel(pre)} over the y-axis.", None, ["(x, y) → (-x, y).", "Same rule.", "Same rule.", "Distance to the axis is kept."],
             parts=[("Find A′.", pt(*img[0]), chk_py("xf_point", p=list(pre[0]), desc=refl_name("y-axis"))), ("Find B′.", pt(*img[1]), chk_py("xf_point", p=list(pre[1]), desc=refl_name("y-axis"))),
                    ("Find C′.", pt(*img[2]), chk_py("xf_point", p=list(pre[2]), desc=refl_name("y-axis"))),
                    ("How far is A′ from the y-axis?", str(abs(pre[0][0])), chk_val(str(abs(pre[0][0]))))], tags=["graph"])


# ======================================================================= S4 Translations
@fam("012")
def s4_point(r, L):
    p = (r.randint(-7, 7), r.randint(-7, 7))
    a, b = nz(r, -6, 6), nz(r, -6, 6)
    desc = tr_name(a, b) if L < 2 else f"translation (x, y) → (x {'+' if a > 0 else '-'} {abs(a)}, y {'+' if b > 0 else '-'} {abs(b)})"
    img = trans(p, a, b)
    return P(f"Point P{pt(*p)} is moved by the {desc}. What are the coordinates of P′?", pt(*img),
             [f"Add {a} to x and {b} to y.", f"P′{pt(*img)}."], [pt(p[0] + b, p[1] + a), pt(p[0] - a, p[1] - b), pt(p[0] + a, p[1] - b)], chk_py("xf_point", p=list(p), desc=tr_name(a, b)),
             tags=["misconception"])


@fam("012")
def s4_rule(r, L):
    pre = poly(r, 3, (-5, 4))
    a, b = nz(r, -5, 5), nz(r, -5, 5)
    img = [trans(p, a, b) for p in pre]
    if L == 0:
        p = f"Triangle ABC is translated so that A{pt(*pre[0])} moves to A′{pt(*img[0])}. Describe the translation."
    else:
        p = f"Triangle ABC {plabel(pre)} is translated to A′B′C′ {plabel(img, True)}. Write the translation rule in the form (x, y) → (x + a, y + b)."
    ans = tr_name(a, b) if L == 0 else f"(x, y) → (x {'+' if a > 0 else '-'} {abs(a)}, y {'+' if b > 0 else '-'} {abs(b)})"
    wr = [tr_name(b, a), tr_name(-a, -b), tr_name(a, -b)] if L == 0 else [f"(x, y) → (x {'+' if b > 0 else '-'} {abs(b)}, y {'+' if a > 0 else '-'} {abs(a)})", f"(x, y) → (x {'-' if a > 0 else '+'} {abs(a)}, y {'-' if b > 0 else '+'} {abs(b)})", f"(x, y) → (x {'+' if a > 0 else '-'} {abs(a)}, y {'-' if b > 0 else '+'} {abs(b)})"]
    return P(p, ans, [f"Change in x: {a}; change in y: {b}.", ans], wr, chk_py("xf_maps", pre=pre[:1] if L == 0 else pre, img=img[:1] if L == 0 else img), tags=["reasoning"])


@fam("012")
def s4_figure(r, L):
    pre = poly(r, 4 if L else 3, (-4, 4))
    a, b = nz(r, -4, 4), nz(r, -4, 4)
    img = [trans(p, a, b) for p in pre]
    k = r.randint(0, len(pre) - 1)
    name = "Quadrilateral ABCD" if len(pre) == 4 else "Triangle ABC"
    return P(f"{name} (shown) is translated {tr_name(a, b)[12:]}. What are the coordinates of {LET[k]}′?", pt(*img[k]),
             [f"{LET[k]} is at {pt(*pre[k])}.", f"Move {tr_name(a, b)[12:]}: {LET[k]}′{pt(*img[k])}."], [pt(pre[k][0] + b, pre[k][1] + a), pt(pre[k][0] - a, pre[k][1] - b), pt(*img[(k + 1) % len(pre)])],
             chk_py("xf_point", p=list(pre[k]), desc=tr_name(a, b)), diagram={"draw": fig_draw(pre), "alt": alt_of(pre, name=name.split()[0])}, tags=["graph"])


@fam("2")
def s4_compose(r, L):
    p = (r.randint(-5, 5), r.randint(-5, 5))
    a1, b1, a2, b2 = [nz(r, -5, 5) for _ in range(4)]
    img = trans(trans(p, a1, b1), a2, b2)
    return P(f"Point P{pt(*p)} is translated {tr_name(a1, b1)[12:]}, then {tr_name(a2, b2)[12:]}. What single translation has the same result, and where is the final image?",
             f"{tr_name(a1 + a2, b1 + b2) if a1 + a2 or b1 + b2 else 'no movement'}; {pt(*img)}",
             [f"Add the horizontal moves: {a1} + {paren(a2)} = {a1 + a2}; vertical: {b1} + {paren(b2)} = {b1 + b2}.", f"Image: {pt(*img)}."],
             [f"{tr_name(a1 - a2 if a1 != a2 else 1, b1 - b2 if b1 != b2 else 1)}; {pt(p[0] + a1 - a2, p[1] + b1 - b2)}", f"{tr_name(a1 + a2 if a1 + a2 else 1, b1 + b2)}; {pt(img[1], img[0])}" if img[0] != img[1] else f"{tr_name(a1 + a2 + 1, b1 + b2)}; {pt(img[0] + 1, img[1])}",
              f"{tr_name(a1 * a2, b1 * b2)}; {pt(p[0] + a1 * a2, p[1] + b1 * b2)}"], chk_py("compose_translation", p=list(p), moves=[[a1, b1], [a2, b2]]), tags=["challenge"])


@fam("012")
def s4_error(r, L):
    p = (r.randint(-5, 5), r.randint(-5, 5))
    a, b = nz(r, -5, 5), nz(r, -5, 5)
    need(a != b)
    return P(f"Liv translated P{pt(*p)} {tr_name(a, b)[12:]} and wrote P′{pt(p[0] + b, p[1] + a)}. What is the correct image?", pt(p[0] + a, p[1] + b),
             ["Horizontal moves change x; vertical moves change y. Liv switched them.", f"P′{pt(p[0] + a, p[1] + b)}."], [pt(p[0] + b, p[1] + a), pt(p[0] - a, p[1] - b), pt(p[0] + a, p[1] - b)],
             chk_py("xf_point", p=list(p), desc=tr_name(a, b)), tags=["error-analysis", "misconception"])


@fam("012")
def s4_select(r, L):
    pre = poly(r, 3, (-4, 4))
    a, b = nz(r, -4, 4), nz(r, -4, 4)
    img = [trans(p, a, b) for p in pre]
    stm = [(f"A′B′ = AB", True), ("Triangle A′B′C′ is congruent to triangle ABC.", True), (f"Every point moves {tr_name(a, b)[12:]}.", True),
           ("Triangle A′B′C′ is larger than triangle ABC.", False), ("The orientation of the vertices is reversed.", False), (f"Every point moves {tr_name(b, a)[12:]}.", a == b)]
    need(not stm[5][1])
    return P(f"Triangle ABC is translated {tr_name(a, b)[12:]} to form A′B′C′. Select ALL true statements.", None, ["Translations are rigid motions that keep orientation."], options=stm,
             chk=chk_py("translation_stmt", a=a, b=b), tags=["reasoning"])


@fam("012")
def s4_open(r, L):
    pre = poly(r, 3, (-4, 4))
    a, b = nz(r, -4, 4), nz(r, -4, 4)
    img = [trans(p, a, b) for p in pre]
    return P(f"Translate triangle ABC {plabel(pre)} using the rule (x, y) → (x {'+' if a > 0 else '-'} {abs(a)}, y {'+' if b > 0 else '-'} {abs(b)}).", None,
             ["Apply to A.", "Apply to B.", "Apply to C.", "Describe."],
             parts=[("Find A′.", pt(*img[0]), chk_py("xf_point", p=list(pre[0]), desc=tr_name(a, b))), ("Find B′.", pt(*img[1]), chk_py("xf_point", p=list(pre[1]), desc=tr_name(a, b))),
                    ("Find C′.", pt(*img[2]), chk_py("xf_point", p=list(pre[2]), desc=tr_name(a, b))), ("Describe the translation in words.", tr_name(a, b), chk_py("xf_maps", pre=pre, img=img))],
             tags=["graph"])


# ======================================================================= S5 Dilations
@fam("012")
def s5_point(r, L):
    k = pick(r, [F(2), F(3)] if L == 0 else [F(2), F(3), F(1, 2), F(3, 2), F(1, 3)])
    p = (nz(r, -6, 6) * k.denominator, nz(r, -6, 6) * k.denominator)
    img = dil(p, k)
    need(all(abs(v) <= 18 for v in img))
    return P(f"Point P{pt(*p)} is dilated with scale factor {N(k)} centered at the origin. What are the coordinates of P′?", pt(*img),
             [f"Multiply each coordinate by {N(k)}.", f"P′{pt(*img)}."], [pt(p[0] + k, p[1] + k), pt(p[0] / k, p[1] / k), pt(img[0], p[1])], chk_py("xf_point", p=list(p), desc=dil_name(k)),
             tags=["misconception"])


@fam("012")
def s5_scale_factor(r, L):
    k = pick(r, [F(2), F(3), F(1, 2), F(5, 2), F(1, 3), F(3, 2)] if L else [F(2), F(3), F(1, 2)])
    pre = [(x * k.denominator, y * k.denominator) for x, y in poly(r, 3, (-3, 3))]
    img = [dil(p, k) for p in pre]
    need(all(abs(v) <= 12 for p in img for v in p))
    return P(f"Triangle ABC {plabel(pre)} is dilated about the origin to A′B′C′ {plabel(img, True)}. What is the scale factor?", N(k),
             [f"Divide an image coordinate by the matching original coordinate: {N(img[0][0] if pre[0][0] else img[0][1])} ÷ {N(pre[0][0] if pre[0][0] else pre[0][1])} = {N(k)}."],
             [N(1 / k), N(k + 1), N(k * 2)], chk_py("dil_factor", pre=pre, img=img), diagram={"draw": fig_draw(pre, img), "alt": alt_of(pre, img)} if L == 1 else None,
             tags=["reasoning", "graph"] if L == 1 else ["reasoning"])


@fam("012", mode="mc")
def s5_enlarge(r, L):
    k = pick(r, [F(1, 3), F(1, 2), F(3, 4), F(3, 2), F(2), F(5, 2), F(4)])
    want = "enlargement" if k > 1 else "reduction"
    opts = [("enlargement", want == "enlargement"), ("reduction", want == "reduction"), ("congruent copy", False), ("reflection", False)]
    return P(f"A figure is dilated with scale factor {N(k)}. Is the image an enlargement, a reduction, or a congruent copy?", want,
             ["Scale factor greater than 1 → enlargement; between 0 and 1 → reduction; exactly 1 → congruent."], options=opts, chk=chk_py("enlarge_word", k=N(k)), tags=["reasoning"], mode="mc")


@fam("12")
def s5_measure(r, L):
    k = pick(r, [F(2), F(3), F(1, 2), F(3, 2), F(5, 2)])
    side = r.randint(2, 12) * 2
    q = pick(r, ["length", "perimeter", "angle"] if L == 1 else ["length", "perimeter", "area", "angle"])
    if q == "length":
        orig = side
        v, wr = k * side, [side + k, side / k, side]
        p = f"A side of a triangle is {side} cm. After a dilation with scale factor {N(k)}, how long is the image side?"
        units = " cm"
    elif q == "perimeter":
        per = side * 3 + 2
        orig = per
        v, wr = k * per, [per + k, per / k, k * k * per]
        p = f"A triangle has perimeter {per} cm. What is the perimeter of its image after a dilation with scale factor {N(k)}?"
        units = " cm"
    elif q == "area":
        ar = side * 3
        orig = ar
        v, wr = k * k * ar, [k * ar, ar + k, ar / k]
        p = f"A rectangle has area {ar} square cm. What is the area of its image after a dilation with scale factor {N(k)}?"
        units = " square cm"
    else:
        ang = r.randint(30, 110)
        orig = ang
        v, wr = F(ang), [k * ang, ang / k, 180 - ang]
        p = f"An angle of a triangle measures {ang}°. What does the matching angle measure after a dilation with scale factor {N(k)}?"
        units = "°"
    return P(p, f"{N(v) if v.denominator == 1 else D(v)}{units}", [{"length": "Lengths are multiplied by the scale factor.", "perimeter": "Perimeter is a length: multiply by the scale factor.",
                                                                    "area": "Area is multiplied by the square of the scale factor.", "angle": "Dilations preserve angle measures."}[q]],
             [f"{N(w) if F(w).denominator == 1 else D(F(w)) if is_term(F(w)) else N(F(w))}{units}" for w in wr], chk_py("dil_measure", q=q, k=N(k), orig=orig), tags=["reasoning"])


@fam("2")
def s5_center(r, L):
    c = (r.randint(-3, 3), r.randint(-3, 3))
    k = pick(r, [F(2), F(3), F(1, 2)])
    p = (c[0] + nz(r, -4, 4) * 2, c[1] + nz(r, -4, 4) * 2)
    img = dil(p, k, c)
    return P(f"Point P{pt(*p)} is dilated with scale factor {N(k)} centered at C{pt(*c)}. What are the coordinates of P′?", pt(*img),
             [f"Vector from C to P: ({p[0] - c[0]}, {p[1] - c[1]}).", f"Multiply by {N(k)} and add to C: {pt(*img)}."], [pt(*dil(p, k)), pt(p[0] * k - c[0], p[1] * k - c[1]), pt(c[0] + (p[0] - c[0]) / k, c[1] + (p[1] - c[1]) / k)],
             chk_py("dil_center", p=list(p), c=list(c), k=N(k)), tags=["challenge"])


@fam("012")
def s5_error(r, L):
    p = (r.randint(1, 6), r.randint(1, 6))
    k = pick(r, [2, 3])
    return P(f"Sam dilated P{pt(*p)} by scale factor {k} centered at the origin and wrote P′{pt(p[0] + k, p[1] + k)}. What is the correct image?", pt(k * p[0], k * p[1]),
             ["A dilation multiplies coordinates by the scale factor; Sam added it.", f"P′{pt(k * p[0], k * p[1])}."], [pt(p[0] + k, p[1] + k), pt(k * p[0], p[1]), pt(p[0], k * p[1])],
             chk_py("xf_point", p=list(p), desc=dil_name(F(k))), tags=["error-analysis", "misconception"])


@fam("012")
def s5_select(r, L):
    k = pick(r, [F(2), F(3), F(1, 2)])
    stm = [("Corresponding angles are congruent.", True), (f"Each image side is {N(k)} times as long as the original side.", True), ("The image is similar to the original.", True),
           ("The image is congruent to the original.", False), (f"The image area is {N(k)} times the original area.", False), ("Corresponding angles are multiplied by the scale factor.", False)]
    return P(f"A triangle is dilated with scale factor {N(k)} centered at the origin. Select ALL true statements.", None, ["Dilations preserve angles; lengths scale by k; areas scale by k²."], options=stm,
             chk=chk_py("dil_stmt", k=N(k)), tags=["reasoning"])


@fam("012")
def s5_open(r, L):
    k = pick(r, [F(2), F(3)])
    pre = poly(r, 3, (-3, 3))
    img = [dil(p, k) for p in pre]
    return P(f"Dilate triangle ABC {plabel(pre)} by scale factor {N(k)} centered at the origin.", None, ["Multiply.", "Multiply.", "Multiply.", "Similar, not congruent."],
             parts=[("Find A′.", pt(*img[0]), chk_py("xf_point", p=list(pre[0]), desc=dil_name(k))), ("Find B′.", pt(*img[1]), chk_py("xf_point", p=list(pre[1]), desc=dil_name(k))),
                    ("Find C′.", pt(*img[2]), chk_py("xf_point", p=list(pre[2]), desc=dil_name(k))),
                    ("Is A′B′C′ congruent or similar (but not congruent) to ABC?", "similar", {"kind": "text", "accept": ["similar"]})], tags=["graph"])


# ======================================================================= S6 Sequences of transformations
SEQ_TF = [("t", None), ("r", "x-axis"), ("r", "y-axis"), ("o", 90), ("o", 180), ("o", 270)]


def tf_apply(spec, p):
    if spec[0] == "t":
        return trans(p, spec[1], spec[2])
    if spec[0] == "r":
        return refl(p, spec[1])
    if spec[0] == "o":
        return rot(p, spec[1])
    return dil(p, spec[1])


def tf_name(spec):
    return {"t": lambda: tr_name(spec[1], spec[2]), "r": lambda: refl_name(spec[1]), "o": lambda: rot_name(spec[1]), "d": lambda: dil_name(spec[1])}[spec[0]]()


def rand_tf(r, allow_d=False):
    k = pick(r, ["t", "r", "o"] + (["d"] if allow_d else []))
    if k == "t":
        return ("t", nz(r, -5, 5), nz(r, -5, 5))
    if k == "r":
        return ("r", pick(r, ["x-axis", "y-axis", "y = x"]))
    if k == "o":
        return ("o", pick(r, [90, 180, 270]))
    return ("d", pick(r, [F(2), F(1, 2)]))


@fam("012")
def s6_apply(r, L):
    p = (nz(r, -5, 5), nz(r, -5, 5))
    t1, t2 = rand_tf(r, L == 2), rand_tf(r)
    need(t1[0] != t2[0])
    if t1[0] == "d" and t1[1] == F(1, 2):
        p = (2 * p[0], 2 * p[1])
    img = tf_apply(t2, tf_apply(t1, p))
    rev = tf_apply(t1, tf_apply(t2, p))
    return P(f"Point P{pt(*p)} undergoes a {tf_name(t1)}, followed by a {tf_name(t2)}. What are the final coordinates?", pt(*img),
             [f"After the first: {pt(*tf_apply(t1, p))}.", f"After the second: {pt(*img)}."], [pt(*rev) if rev != img else pt(img[0] + 1, img[1]), pt(*tf_apply(t1, p)), pt(*tf_apply(t2, p))],
             chk_py("xf_seq", p=list(p), descs=[tf_name(t1), tf_name(t2)]), tags=["multistep"])


@fam("012", mode="sa")
def s6_cong_or_sim(r, L):
    t1, t2 = rand_tf(r, True), rand_tf(r, True)
    has_d = "d" in (t1[0], t2[0])
    ans = "similar" if has_d else "congruent"
    return P(f"A figure undergoes a {tf_name(t1)}, then a {tf_name(t2)}. Is the final image congruent to the original, or similar but not congruent?", ans,
             ["A sequence of rigid motions gives a congruent image.", "Including a dilation (scale factor ≠ 1) gives a similar, not congruent, image."],
             ["congruent" if has_d else "similar"], chk_py("seq_congruent", descs=[tf_name(t1), tf_name(t2)]), tags=["reasoning"], mode="sa")


@fam("12", mode="mc")
def s6_find_sequence(r, L):
    pre = poly(r, 3, (1, 5), quadrant=1)
    t1 = ("r", pick(r, ["x-axis", "y-axis"]))
    t2 = ("t", nz(r, -4, 4), nz(r, -4, 4))
    img = [tf_apply(t2, tf_apply(t1, p)) for p in pre]
    good = f"a {tf_name(t1)} followed by a {tf_name(t2)}"
    other_ax = "y-axis" if t1[1] == "x-axis" else "x-axis"
    bad = [f"a {refl_name(other_ax)} followed by a {tf_name(t2)}", f"a {tf_name(t2)} followed by a {tf_name(t1)}", f"a {rot_name(180)} followed by a {tf_name(t2)}"]
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return P("Which sequence maps triangle ABC onto triangle A′B′C′ (shown)?", good, ["Check each sequence on all three vertices, in order."], options=opts,
             chk=chk_py("seq_maps", pre=pre, img=img), diagram={"draw": fig_draw(pre, img), "alt": alt_of(pre, img)}, tags=["graph", "challenge"], mode="mc")


@fam("2")
def s6_order_matters(r, L):
    p = (r.randint(1, 5), r.randint(1, 5))
    a = nz(r, -4, 4)
    t1, t2 = ("r", "x-axis"), ("t", 0, a)
    i1 = tf_apply(t2, tf_apply(t1, p))
    i2 = tf_apply(t1, tf_apply(t2, p))
    need(i1 != i2)
    return P(f"P{pt(*p)} is reflected over the x-axis and then translated {tr_name(0, a)[12:]}. Q is the image if the same two transformations are done in the reverse order. How far apart are the two images?",
             f"{abs(i1[1] - i2[1])} units", [f"First order: {pt(*i1)}. Reverse order: {pt(*i2)}.", f"Distance: {abs(i1[1] - i2[1])} units."], ["0 units", f"{abs(a)} units", f"{abs(i1[1] - i2[1]) + 1} units"],
             chk_py("order_distance", p=list(p), a=a), tags=["challenge", "reasoning"])


@fam("012")
def s6_error(r, L):
    p = (r.randint(1, 6), r.randint(1, 6))
    a = nz(r, -4, 4)
    good = tf_apply(("o", 180), trans(p, a, 0))
    wrong = trans(tf_apply(("o", 180), p), a, 0)
    need(good != wrong)
    return P(f"P{pt(*p)} is translated {tr_name(a, 0)[12:]} and then rotated 180° about the origin. Dee rotated first and then translated, getting {pt(*wrong)}. What is the correct final image?",
             pt(*good), [f"Translate first: {pt(*trans(p, a, 0))}.", f"Then rotate 180°: {pt(*good)}. Order matters."], [pt(*wrong), pt(*trans(p, a, 0)), pt(-p[0], -p[1])],
             chk_py("xf_seq", p=list(p), descs=[tr_name(a, 0), rot_name(180)]), tags=["error-analysis", "misconception"])


@fam("012")
def s6_select(r, L):
    stm = [(f"a {refl_name('x-axis')} followed by a {tr_name(3, 1)}", True), (f"a {rot_name(90)} followed by a {refl_name('y-axis')}", True), (f"a {tr_name(-2, 4)} followed by a {rot_name(180)}", True),
           (f"a {dil_name(F(2))} followed by a {tr_name(1, 1)}", False), (f"a {rot_name(180)} followed by a {dil_name(F(1, 2))}", False), (f"a {dil_name(F(3))} followed by a {refl_name('y-axis')}", False)]
    return P("Select ALL sequences that always produce an image CONGRUENT to the original figure.", None, ["Only sequences of rigid motions guarantee congruence."], options=stm,
             chk=chk_py("seq_congruent_text"), tags=["reasoning"])


@fam("012")
def s6_open(r, L):
    p = (r.randint(1, 5), r.randint(1, 5))
    a, b = nz(r, -3, 3), nz(r, -3, 3)
    q1 = refl(p, "y-axis")
    q2 = trans(q1, a, b)
    q3 = dil(q2, F(2))
    return P(f"Point P{pt(*p)} goes through three steps: reflect over the y-axis, translate {tr_name(a, b)[12:]}, then dilate by scale factor 2 about the origin.", None,
             ["(x, y) → (-x, y).", "Add.", "Multiply by 2.", "Dilation changes size."],
             parts=[("Image after step 1?", pt(*q1), chk_py("xf_point", p=list(p), desc=refl_name("y-axis"))), ("Image after step 2?", pt(*q2), chk_py("xf_point", p=list(q1), desc=tr_name(a, b))),
                    ("Image after step 3?", pt(*q3), chk_py("xf_point", p=list(q2), desc=dil_name(F(2)))),
                    ("Is a figure that goes through these steps congruent or similar to the original?", "similar", chk_py("seq_congruent", descs=[refl_name("y-axis"), tr_name(a, b), dil_name(F(2))]))],
             tags=["multistep"])


# ======================================================================= S7 Triangle angle sum
def tri_draw(angles, labels, show, sides=None):
    """Triangle with given angles (deg) at vertices A, B, C; `show` texts placed inside each corner."""
    A, B = math.radians(angles[0]), math.radians(angles[1])
    base = 6.0
    # place A at origin, B at (base, 0); C from angles
    tC = base * math.sin(B) / math.sin(math.pi - A - B)
    C = (tC * math.cos(A), tC * math.sin(A))
    P_ = [(0.0, 0.0), (base, 0.0), C]

    def draw(path):
        fig, ax = new_fig(6, 4.6)
        xs = [p[0] for p in P_] + [0.0]
        ys = [p[1] for p in P_] + [0.0]
        ax.plot(xs, ys, color="#1f4e9c", lw=2.4)
        cx, cy = sum(p[0] for p in P_) / 3, sum(p[1] for p in P_) / 3
        for (x, y), lab, s in zip(P_, labels, show):
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy)
            ax.text(x + 0.35 * dx / d, y + 0.35 * dy / d, lab, fontsize=14, fontweight="bold", ha="center", va="center")
            if s:
                ax.text(x - 0.9 * dx / d, y - 0.9 * dy / d, s, fontsize=13, ha="center", va="center", color="#b23a3a")
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(0.0, -0.9, "Not drawn to scale", fontsize=9, color="gray")
        save(fig, path)
    return draw


@fam("012")
def s7_missing(r, L):
    a, b = r.randint(25, 100), r.randint(20, 100)
    c = 180 - a - b
    need(c >= 15)
    if L == 0:
        return P(f"Two angles of a triangle measure {a}° and {b}°. What is the measure of the third angle?", f"{c}°", [f"The angles of a triangle sum to 180°.", f"180 - {a} - {b} = {c}."],
                 [f"{360 - a - b}°", f"{a + b}°", f"{abs(a - b)}°"], chk_py("angle_sum_missing", known=[a, b]), tags=["misconception"],
                 diagram={"draw": tri_draw([a, b, c], "ABC", [f"{a}°", f"{b}°", "?"]), "alt": f"Triangle ABC with angle A = {a}°, angle B = {b}°, angle C unknown."} if r.random() < 0.5 else None)
    k = pick(r, ["iso", "right"])
    if k == "iso":
        top = r.randint(20, 140)
        need((180 - top) % 2 == 0)
        return P(f"An isosceles triangle has a vertex angle of {top}°. What is the measure of each base angle?", f"{(180 - top) // 2}°",
                 [f"The two base angles are equal: 2x + {top} = 180.", f"x = {(180 - top) // 2}."], [f"{180 - top}°", f"{top}°", f"{(360 - top) // 2}°"],
                 chk_py("iso_base", top=top), tags=["reasoning"])
    a = r.randint(15, 75)
    return P(f"A right triangle has one acute angle of {a}°. What is the other acute angle?", f"{90 - a}°", ["The acute angles of a right triangle sum to 90°.", f"90 - {a} = {90 - a}."],
             [f"{180 - a}°", f"{a}°", f"{180 - 90 - a + 10}°"], chk_py("angle_sum_missing", known=[90, a]), tags=["reasoning"])


@fam("012")
def s7_algebra(r, L):
    for _ in range(50):
        x = r.randint(5, 40)
        p1, q1 = r.randint(1, 3), r.randint(-10, 20)
        p2, q2 = r.randint(1, 4), r.randint(-10, 20)
        a1, a2 = p1 * x + q1, p2 * x + q2
        a3 = 180 - a1 - a2
        if a1 > 5 and a2 > 5 and a3 > 5:
            break
    else:
        raise Reject()
    if L == 0:
        e1, e2 = f"{a1}", f"{lin((1, 'x'), (0, ''))}"
        x = 180 - a1 - a2
        expr = [str(a1), str(a2), "x"]
        ans = f"x = {x}"
        steps = [f"{a1} + {a2} + x = 180.", f"x = {x}."]
        tri = [a1, a2, x]
    elif L == 1:
        expr = [lin((p1, 'x'), (q1, '')), lin((p2, 'x'), (q2, '')), str(a3)]
        ans = f"x = {x}"
        steps = [f"({expr[0]}) + ({expr[1]}) + {a3} = 180.", f"{p1 + p2}x + {q1 + q2 + a3} = 180, so x = {x}."]
        tri = [a1, a2, a3]
    else:
        p3 = r.randint(1, 3)
        q3 = a3 - p3 * x
        expr = [lin((p1, 'x'), (q1, '')), lin((p2, 'x'), (q2, '')), lin((p3, 'x'), (q3, ''))]
        big = max(a1, a2, a3)
        ans = f"{big}°"
        steps = [f"({expr[0]}) + ({expr[1]}) + ({expr[2]}) = 180.", f"{p1 + p2 + p3}x + {q1 + q2 + q3} = 180, so x = {x}.", f"Angles: {a1}°, {a2}°, {a3}°; largest {big}°."]
        tri = [a1, a2, a3]
        return P(f"The angles of a triangle measure ({expr[0]})°, ({expr[1]})°, and ({expr[2]})°. What is the measure of the largest angle?", ans, steps,
                 [f"{x}°", f"{min(a1, a2, a3)}°", f"{sorted([a1, a2, a3])[1]}°"], chk_py("tri_alg_largest", exprs=expr), tags=["multistep"])
    return P(f"The angles of a triangle measure {expr[0]}°, {expr[1]}°, and {expr[2]}°. Find x.", ans, steps, [f"x = {x + 1}", f"x = {360 - sum(tri) + x}" if 360 - sum(tri) + x != x else f"x = {x + 2}", f"x = {x * 2}"],
             {"kind": "eq", "eq": f"{expr[0]} + {expr[1]} + {expr[2]} = 180"}, diagram={"draw": tri_draw(tri, "ABC", [f"{e}°" for e in expr]), "alt": f"Triangle with angles labeled {expr[0]}°, {expr[1]}°, {expr[2]}°."},
             tags=["multistep"])


@fam("12")
def s7_exterior(r, L):
    a, b = r.randint(25, 80), r.randint(25, 80)
    need(a + b < 170)
    q = pick(r, ["ext", "remote"])
    if q == "ext":
        return P(f"Two interior angles of a triangle measure {a}° and {b}°. What is the measure of the exterior angle at the third vertex?", f"{a + b}°",
                 ["An exterior angle equals the sum of the two remote interior angles.", f"{a} + {b} = {a + b}."], [f"{180 - a - b}°", f"{360 - a - b}°", f"{abs(a - b)}°"],
                 chk_py("exterior", known=[a, b]), tags=["reasoning"])
    return P(f"An exterior angle of a triangle measures {a + b}°. One remote interior angle measures {a}°. What is the other remote interior angle?", f"{b}°",
             [f"Exterior angle = sum of remote interior angles: {a} + x = {a + b}.", f"x = {b}."], [f"{180 - a - b}°", f"{180 - a}°", f"{a + b + a}°"], chk_py("exterior_remote", ext=a + b, a=a),
             tags=["reasoning"])


@fam("2", mode="mc")
def s7_possible(r, L):
    good = None
    for _ in range(20):
        a, b, c = r.randint(20, 120), r.randint(20, 120), r.randint(20, 120)
        if a + b + c == 180:
            good = (a, b, c)
            break
    need(good)
    bad = [(a, b, c + 10), (90, 90, r.randint(1, 30)), (a + 5, b + 5, c)]
    opts = [(f"{x}°, {y}°, {z}°", (x + y + z) == 180) for x, y, z in [good] + bad]
    r.shuffle(opts)
    return P("Which set of angle measures could be the angles of a triangle?", f"{good[0]}°, {good[1]}°, {good[2]}°", ["The three angles must add to exactly 180°."],
             options=opts, chk=chk_py("angle_set_ok"), tags=["reasoning"], mode="mc")


@fam("012")
def s7_error(r, L):
    a, b = r.randint(30, 80), r.randint(30, 80)
    need(a + b < 170)
    return P(f"Two angles of a triangle are {a}° and {b}°. Mel says the third angle is {360 - a - b}° because \"angles add to 360°.\" What is the correct third angle?", f"{180 - a - b}°",
             ["The interior angles of a triangle sum to 180°, not 360°.", f"180 - {a} - {b} = {180 - a - b}."], [f"{360 - a - b}°", f"{a + b}°", f"{90 - a + b}°" if 90 - a + b > 0 else f"{a}°"],
             chk_py("angle_sum_missing", known=[a, b]), tags=["error-analysis", "misconception"])


@fam("012")
def s7_select(r, L):
    sets = []
    while len(sets) < 3:
        a, b = r.randint(20, 100), r.randint(20, 100)
        if 180 - a - b > 5:
            sets.append(((a, b, 180 - a - b), True))
    for _ in range(3):
        a, b, c = r.randint(20, 100), r.randint(20, 100), r.randint(20, 100)
        if a + b + c == 180:
            c += 7
        sets.append(((a, b, c), False))
    opts = [(f"{x}°, {y}°, {z}°", ok) for (x, y, z), ok in sets]
    need(len({o[0] for o in opts}) == 6)
    return P("Select ALL sets of measures that could be the three angles of a triangle.", None, ["The sum must be 180°."], options=opts, chk=chk_py("angle_set_ok"), tags=["reasoning"])


@fam("012")
def s7_open(r, L):
    a = r.randint(30, 70)
    b = r.randint(30, 70)
    c = 180 - a - b
    return P(f"In triangle PQR, ∠P = {a}° and ∠Q = {b}°. Side QR is extended past R to make an exterior angle at R.", None, ["Sum 180°.", "Linear pair.", "Remote interior sum.", "Compare."],
             parts=[("Find ∠R.", f"{c}°", chk_py("angle_sum_missing", known=[a, b])), ("Find the exterior angle at R.", f"{a + b}°", chk_py("exterior", known=[a, b])),
                    (f"What is ∠P + ∠Q?", f"{a + b}°", chk_val(f"{a} + {b}")), ("Which is larger: the exterior angle at R or ∠P?", "the exterior angle at R", {"kind": "text", "accept": ["the exterior angle at R"]})],
             tags=["reasoning"])


# ======================================================================= S8 Similar triangles
def sim_draw(s1, s2, labels1="ABC", labels2="DEF", show1=None, show2=None):
    def tri_pts(s, ox):
        a, b, c = s   # a opposite A etc: use side lengths BC=a, CA=b, AB=c
        Ax, Ay = 0.0, 0.0
        Bx, By = c, 0.0
        cosA = (b * b + c * c - a * a) / (2 * b * c)
        Cx, Cy = b * cosA, b * math.sqrt(max(0.0, 1 - cosA * cosA))
        return [(Ax + ox, Ay), (Bx + ox, By), (Cx + ox, Cy)]

    def draw(path):
        k = max(max(s1), max(s2))
        sc = 5.0 / k
        t1 = tri_pts([v * sc for v in s1], 0)
        t2 = tri_pts([v * sc for v in s2], max(p[0] for p in t1) + 1.5)
        fig, ax = new_fig(8.4, 4.2)
        for tri, labs, show, col in ((t1, labels1, show1, COLORS[0]), (t2, labels2, show2, COLORS[1])):
            xs = [p[0] for p in tri] + [tri[0][0]]
            ys = [p[1] for p in tri] + [tri[0][1]]
            ax.plot(xs, ys, color=col, lw=2.2)
            cx, cy = sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3
            for (x, y), l in zip(tri, labs):
                dx, dy = x - cx, y - cy
                d = math.hypot(dx, dy)
                ax.text(x + 0.3 * dx / d, y + 0.3 * dy / d, l, fontsize=13, fontweight="bold", ha="center", va="center")
            if show:
                # sides: opposite vertex i -> between the other two
                for i in range(3):
                    if show[i]:
                        p, q = tri[(i + 1) % 3], tri[(i + 2) % 3]
                        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                        dx, dy = mx - cx, my - cy
                        d = math.hypot(dx, dy) or 1
                        ax.text(mx + 0.35 * dx / d, my + 0.35 * dy / d, show[i], fontsize=12, color="#b23a3a", ha="center", va="center")
        ax.set_aspect("equal")
        ax.axis("off")
        save(fig, path)
    return draw


def sim_tri(r):
    for _ in range(100):
        s = sorted([r.randint(3, 12) for _ in range(3)])
        if s[0] + s[1] > s[2] + 1:
            return s
    raise Reject()


@fam("012")
def s8_missing_side(r, L):
    s = sim_tri(r)
    k = pick(r, [F(2), F(3), F(3, 2), F(1, 2), F(5, 2)] if L else [F(2), F(3)])
    t = [k * v for v in s]
    need(all(v.denominator == 1 for v in t))
    i = r.randint(0, 2)
    j = (i + 1) % 3
    names1, names2 = ["BC", "CA", "AB"], ["EF", "FD", "DE"]
    show1 = [str(v) for v in s]
    show2 = [N(v) if m != i else "x" for m, v in enumerate(t)]
    show2[(i + 2) % 3] = ""
    return P(f"Triangle ABC ~ triangle DEF. AB = {s[2]}, BC = {s[0]}, CA = {s[1]}, and {names2[j]} = {N(t[j])}. Find x = {names2[i]}.", N(t[i]),
             [f"Scale factor = {names2[j]} ÷ {names1[j]} = {N(t[j])} ÷ {s[j]} = {N(k)}.", f"x = {N(k)} × {s[i]} = {N(t[i])}."],
             [N(s[i] + t[j] - s[j]), N(s[i] / k), N(t[j] * s[j] / s[i]) if t[j] * s[j] / s[i] != t[i] else N(t[i] + 1)], chk_py("sim_side", s=s, known=[j, N(t[j])], ask=i),
             diagram={"draw": sim_draw(s, [float(v) for v in t], show1=show1, show2=show2), "alt": f"Triangle ABC with sides BC = {s[0]}, CA = {s[1]}, AB = {s[2]}; similar triangle DEF with {names2[j]} = {N(t[j])} and {names2[i]} = x."},
             tags=["graph"])


@fam("012", mode="sa")
def s8_aa(r, L):
    a, b = r.randint(30, 80), r.randint(30, 80)
    need(a + b < 170)
    sim = r.random() < 0.5
    if sim:
        d, e = (180 - a - b, a) if L else (a, b)
    else:
        d, e = a, b + pick(r, [-6, 6, 10])
        need(d + e < 175)
    ans = "yes" if sim else "no"
    return P(f"Triangle 1 has angles of {a}° and {b}°. Triangle 2 has angles of {d}° and {e}°. Are the triangles similar? Answer yes or no.", ans,
             [f"Find each third angle: {180 - a - b}° and {180 - d - e}°.", "Triangles with two pairs of congruent angles are similar (AA)." if sim else "The angle sets do not match, so they are not similar."],
             ["no" if sim else "yes"], chk_py("aa_similar", t1=[a, b], t2=[d, e]), tags=["reasoning"], mode="sa")


@fam("012")
def s8_shadow(r, L):
    h1 = r.randint(4, 7) if L == 0 else F(r.randint(9, 15), 2)
    s1 = r.randint(2, 9)
    k = r.randint(3, 9)
    s2 = s1 * k
    h2 = h1 * k
    obj = pick(r, ["flagpole", "tree", "building", "light pole"])
    return P(f"A {D(F(h1))}-foot person casts a {s1}-foot shadow. At the same time, a {obj} casts a {s2}-foot shadow. How tall is the {obj}?", f"{D(F(h2))} feet",
             ["The sun's rays make similar right triangles (AA).", f"{D(F(h1))}/{s1} = h/{s2}, so h = {D(F(h1))} × {k} = {D(F(h2))}."],
             [f"{D(F(h1) + s2 - s1)} feet", f"{D(F(s2 * s1, h1))} feet" if is_term(F(s2 * s1, h1)) else f"{s2} feet", f"{s2 + 1} feet"], chk_py("shadow", h1=D(F(h1)), s1=s1, s2=s2), tags=["modeling"])


@fam("12")
def s8_scale_perimeter(r, L):
    s = sim_tri(r)
    k = pick(r, [F(2), F(3), F(3, 2), F(5, 2)])
    per = sum(s)
    return P(f"Triangle ABC has sides {s[0]}, {s[1]} and {s[2]}. A similar triangle has its shortest side equal to {N(k * s[0])}. What is the perimeter of the larger triangle?", N(k * per),
             [f"Scale factor = {N(k * s[0])} ÷ {s[0]} = {N(k)}.", f"Perimeter = {N(k)} × {per} = {N(k * per)}."], [N(per + k * s[0] - s[0]), N(k * k * per), N(per * k + 1)],
             chk_py("sim_perimeter", s=s, short=N(k * s[0])), tags=["multistep"])


@fam("2", mode="mc")
def s8_nested(r, L):
    ab, ad = r.randint(3, 8), r.randint(2, 6)
    de = r.randint(2, 9)
    bc = F(de * (ab + ad), ab)
    need(bc.denominator == 1 or is_term(bc))
    good = D(bc) if bc.denominator != 1 else N(bc)
    cands = [good, N(de + ad), D(F(de * ab, ab + ad)) if is_term(F(de * ab, ab + ad)) else N(F(de * ab, ab + ad)), N(de * 2)]
    need(len(set(cands)) == 4)
    opts = [(c, i == 0) for i, c in enumerate(cands)]
    r.shuffle(opts)
    return P(f"In triangle ACE, segment BD is parallel to side CE, with B on AC and D on AE. AB = {ab}, BC = {ad}, and BD = {de}. Find CE.", good,
             ["BD ∥ CE makes triangle ABD ~ triangle ACE (corresponding angles are congruent).", f"CE/BD = AC/AB = {ab + ad}/{ab}.", f"CE = {de} × {ab + ad} ÷ {ab} = {good}."],
             options=opts, chk=chk_py("nested_sim", ab=ab, bc=ad, bd=de), tags=["challenge"], mode="mc")


@fam("012")
def s8_error(r, L):
    s = sim_tri(r)
    k = r.randint(2, 3)
    i = 2
    return P(f"Triangle ABC ~ triangle DEF with AB = {s[2]}, BC = {s[0]}, and DE = {k * s[2]}. To find EF, Kai added {k * s[2] - s[2]} to BC and got {s[0] + k * s[2] - s[2]}. What is EF?", str(k * s[0]),
             ["Similar figures are related by multiplication (a scale factor), not by adding a constant.", f"Scale factor {k * s[2]} ÷ {s[2]} = {k}; EF = {k} × {s[0]} = {k * s[0]}."],
             [str(s[0] + k * s[2] - s[2]), str(s[0] * k + 1), str(k * s[2])], chk_py("sim_side", s=s, known=[2, str(k * s[2])], ask=0), tags=["error-analysis", "misconception"])


@fam("012")
def s8_select(r, L):
    s = sim_tri(r)
    k = pick(r, [2, 3])
    good = [f"{k * s[0]}, {k * s[1]}, {k * s[2]}", f"{s[0] * 10}, {s[1] * 10}, {s[2] * 10}", f"{N(F(s[0], 2))}, {N(F(s[1], 2))}, {N(F(s[2], 2))}"]
    bad = [f"{s[0] + 2}, {s[1] + 2}, {s[2] + 2}", f"{k * s[0]}, {k * s[1]}, {k * s[2] + 1}", f"{s[2]}, {s[1]}, {s[0] + 1}"]
    opts = [(g, True) for g in good] + [(b, False) for b in bad]
    need(len({o[0] for o in opts}) == 6)
    return P(f"A triangle has sides {s[0]}, {s[1]}, and {s[2]}. Select ALL side-length sets for triangles similar to it.", None, ["Similar triangles have all sides multiplied by the same scale factor."],
             options=opts, chk=chk_py("sim_set", s=s), tags=["reasoning"])


@fam("012")
def s8_open(r, L):
    s = sim_tri(r)
    k = pick(r, [2, 3])
    return P(f"Triangle ABC ~ triangle DEF. BC = {s[0]}, CA = {s[1]}, AB = {s[2]}, and DE = {k * s[2]}.", None, ["DE ÷ AB.", "Multiply.", "Multiply.", "Angles equal."],
             parts=[("Find the scale factor from ABC to DEF.", str(k), chk_val(f"{k * s[2]}/{s[2]}")), ("Find EF.", str(k * s[0]), chk_py("sim_side", s=s, known=[2, str(k * s[2])], ask=0)),
                    ("Find FD.", str(k * s[1]), chk_py("sim_side", s=s, known=[2, str(k * s[2])], ask=1)),
                    ("If ∠A = 50°, what is ∠D?", "50°", {"kind": "text", "accept": ["50°"]})], tags=["multistep"])


# ======================================================================= S9 Parallel lines cut by a transversal
POS = ["1", "2", "3", "4", "5", "6", "7", "8"]   # 1 upper-left, 2 upper-right, 3 lower-left, 4 lower-right at top line; 5-8 same at bottom line


def angle_at(n, theta):
    """Measure of numbered angle when the transversal makes acute angle theta with the parallels (opening upper-right)."""
    return theta if int(n) in (2, 3, 6, 7) else 180 - theta


def para_draw(theta, show, labels=True):
    def draw(path):
        fig, ax = new_fig(6.3, 5.2)
        ax.plot([-5, 5], [1.5, 1.5], color="black", lw=2)
        ax.plot([-5, 5], [-1.5, -1.5], color="black", lw=2)
        ax.annotate("", xy=(5.3, 1.5), xytext=(5, 1.5), arrowprops=dict(arrowstyle="-|>"))
        ax.annotate("", xy=(5.3, -1.5), xytext=(5, -1.5), arrowprops=dict(arrowstyle="-|>"))
        ax.text(5.4, 1.5, "m", fontsize=13, va="center", style="italic")
        ax.text(5.4, -1.5, "n", fontsize=13, va="center", style="italic")
        t = math.radians(theta)
        dx, dy = math.cos(t), math.sin(t)
        L_ = 4.2
        x0 = 1.5 / math.tan(t)
        ax.plot([-x0 - L_ * dx * 0.6, x0 + L_ * dx * 0.6], [-1.5 - L_ * dy * 0.6, 1.5 + L_ * dy * 0.6], color="#1f4e9c", lw=2)
        ax.text(x0 + L_ * dx * 0.6 + 0.2, 1.5 + L_ * dy * 0.6, "t", fontsize=13, style="italic", color="#1f4e9c")
        # numbered positions around each intersection
        for (cx, cy), base in (((x0, 1.5), 0), ((-x0, -1.5), 4)):
            # directions: 1 upper-left (between line-left and transversal-up), 2 upper-right, 3 lower-left, 4 lower-right
            mids = {1: (math.pi + t) / 2 + 0, 2: t / 2, 3: math.pi + t / 2, 4: (2 * math.pi + math.pi + t) / 2}
            mids[1] = (t + math.pi) / 2
            mids[4] = (math.pi + t + 2 * math.pi) / 2
            for k, a in mids.items():
                n = str(base + k)
                txt = show.get(n, n if labels else "")
                if txt:
                    ax.text(cx + 0.75 * math.cos(a), cy + 0.6 * math.sin(a), txt, fontsize=12, ha="center", va="center", color="#b23a3a" if n in show else "black")
        ax.set_xlim(-6, 6)
        ax.set_ylim(-4.2, 4.2)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(-5.8, -4, "Lines m and n are parallel.", fontsize=10, color="gray")
        save(fig, path)
    return draw


REL = {("1", "5"): "corresponding", ("2", "6"): "corresponding", ("3", "7"): "corresponding", ("4", "8"): "corresponding",
       ("3", "6"): "alternate interior", ("4", "5"): "alternate interior", ("1", "8"): "alternate exterior", ("2", "7"): "alternate exterior",
       ("3", "5"): "same-side interior", ("4", "6"): "same-side interior", ("1", "4"): "vertical", ("2", "3"): "vertical", ("5", "8"): "vertical", ("6", "7"): "vertical",
       ("1", "2"): "linear pair", ("3", "4"): "linear pair"}


@fam("012")
def s9_find_angle(r, L):
    theta = r.randint(35, 80) if r.random() < 0.5 else r.randint(100, 145)
    theta = theta if theta < 90 else 180 - theta
    a, b = pick(r, list(REL.keys()))
    if r.random() < 0.5:
        a, b = b, a
    va, vb = angle_at(a, theta), angle_at(b, theta)
    return P(f"In the figure, lines m and n are parallel and t is a transversal. ∠{a} measures {va}°. What is the measure of ∠{b}?", f"{vb}°",
             [f"∠{a} and ∠{b} are {REL.get((a, b)) or REL.get((b, a))} angles.", "They are congruent." if va == vb else "They are supplementary.", f"∠{b} = {vb}°."],
             [f"{180 - vb}°", f"{90 - vb if vb < 90 else vb - 90}°", f"{360 - vb}°"], chk_py("para_angle", theta=theta, n=b),
             diagram={"draw": para_draw(theta, {a: f"{va}°"}, labels=True), "alt": f"Parallel lines m (top) and n (bottom) cut by transversal t. Angles 1-4 at line m and 5-8 at line n, numbered upper-left, upper-right, lower-left, lower-right. ∠{a} = {va}°."},
             tags=["graph"])


@fam("012", mode="mc")
def s9_relationship(r, L):
    a, b = pick(r, list(REL.keys()))
    rel = REL[(a, b)]
    kinds = ["corresponding", "alternate interior", "alternate exterior", "same-side interior", "vertical", "linear pair"]
    others = [k for k in kinds if k != rel]
    r.shuffle(others)
    opts = [(f"{rel} angles" if rel != "linear pair" else "a linear pair", True)] + [(f"{k} angles" if k != "linear pair" else "a linear pair", False) for k in others[:3]]
    r.shuffle(opts)
    return P(f"In the figure (m ∥ n), how are ∠{a} and ∠{b} related?", opts[[c for _, c in opts].index(True)][0],
             ["Use the positions: same corner at each intersection → corresponding; between the lines on opposite sides of t → alternate interior; and so on."], options=opts,
             chk=chk_py("para_rel", a=a, b=b), diagram={"draw": para_draw(60, {}), "alt": "Parallel lines m (top) and n (bottom) cut by transversal t; angles 1-4 at m and 5-8 at n numbered upper-left, upper-right, lower-left, lower-right."},
             tags=["graph"], mode="mc")


@fam("12")
def s9_algebra(r, L):
    theta = r.randint(40, 80)
    a, b = pick(r, [k for k in REL if REL[k] not in ("vertical",)])
    va, vb = angle_at(a, theta), angle_at(b, theta)
    x = r.randint(5, 30)
    p1 = r.randint(2, 5)
    q1 = va - p1 * x
    p2 = r.randint(1, 4)
    q2 = vb - p2 * x
    e1, e2 = lin((p1, 'x'), (q1, '')), lin((p2, 'x'), (q2, ''))
    rel = "congruent" if va == vb else "supplementary"
    eq = f"{e1} = {e2}" if va == vb else f"{e1} + {e2} = 180"
    need(not (va == vb and p1 == p2))
    return P(f"Lines m and n are parallel. ∠{a} = ({e1})° and ∠{b} = ({e2})°. Find x.", f"x = {x}",
             [f"∠{a} and ∠{b} are {REL[(a, b)]} angles, so they are {rel}.", f"{eq}, so x = {x}."], [f"x = {x + 1}", f"x = {N(F(180 - q1 - q2, p1 + p2))}" if va == vb else f"x = {N(F(q2 - q1, p1 - p2)) if p1 != p2 else x + 3}", f"x = {x * 2}"],
             chk_py("para_alg", theta=theta, a=a, b=b, e=[e1, e2]), tags=["multistep"])


@fam("2")
def s9_triangle_link(r, L):
    a = r.randint(40, 75)
    b = r.randint(35, 70)
    need(a + b < 160)
    return P(f"A triangle has one side on line m. Its other two sides meet line n (parallel to m) at a vertex. The angles at the base on line m are {a}° and {b}°. Using alternate interior angles, what is the angle at the vertex on line n?",
             f"{180 - a - b}°", [f"Alternate interior angles at the top vertex equal {a}° and {b}°.", f"Those with the vertex angle form a straight angle: 180 - {a} - {b} = {180 - a - b}° (this proves the triangle sum)."],
             [f"{a + b}°", f"{360 - a - b}°", f"{abs(a - b)}°"], chk_py("angle_sum_missing", known=[a, b]), tags=["connections", "challenge"])


@fam("012")
def s9_error(r, L):
    theta = r.randint(40, 75)
    return P(f"Lines m and n are parallel. ∠3 = {theta}°. Ana says ∠5 = {theta}° because \"interior angles are equal.\" What is ∠5?", f"{180 - theta}°",
             ["∠3 and ∠5 are same-side interior angles, which are supplementary (not congruent).", f"∠5 = 180 - {theta} = {180 - theta}°."], [f"{theta}°", f"{90 - theta}°" if theta < 90 else "90°", f"{360 - theta}°"],
             chk_py("para_angle", theta=theta, n="5"), diagram={"draw": para_draw(theta, {"3": f"{theta}°"}), "alt": f"Parallel lines m and n with transversal t; ∠3 = {theta}°."}, tags=["error-analysis", "misconception", "graph"])


@fam("012")
def s9_select(r, L):
    theta = r.randint(40, 80)
    eq = [n for n in POS if angle_at(n, theta) == theta]
    ne = [n for n in POS if angle_at(n, theta) != theta]
    ref = pick(r, eq)
    goods = pick(r, [n for n in eq if n != ref], 3)
    bads = pick(r, ne, 3)
    opts = [(f"∠{n}", True) for n in goods] + [(f"∠{n}", False) for n in bads]
    return P(f"Lines m and n are parallel. Select ALL angles congruent to ∠{ref}.", None, ["Vertical, corresponding, alternate interior and alternate exterior angles are congruent."], options=opts,
             chk=chk_py("para_congruent", theta=theta, ref=ref), diagram={"draw": para_draw(theta, {}), "alt": "Parallel lines m (top) and n (bottom) cut by transversal t; angles 1-8 numbered as in the standard figure."}, tags=["graph"])


@fam("012")
def s9_open(r, L):
    theta = r.randint(40, 80)
    return P(f"Lines m and n are parallel and ∠2 = {theta}°.", None, ["Linear pair.", "Corresponding.", "Alternate interior.", "Same-side interior."],
             parts=[("Find ∠1.", f"{angle_at('1', theta)}°", chk_py("para_angle", theta=theta, n="1")), ("Find ∠6.", f"{angle_at('6', theta)}°", chk_py("para_angle", theta=theta, n="6")),
                    ("Find ∠7.", f"{angle_at('7', theta)}°", chk_py("para_angle", theta=theta, n="7")), ("Find ∠5.", f"{angle_at('5', theta)}°", chk_py("para_angle", theta=theta, n="5"))],
             diagram={"draw": para_draw(theta, {"2": f"{theta}°"}), "alt": f"Parallel lines m and n with transversal t; ∠2 = {theta}°."}, tags=["graph"])


SKILLS = {
    1: dict(name="Identifying transformations", std=["8.G.A.1", "8.G.A.2"], fams=[s1_name_graph, s1_name_coords, s1_congruent, s1_properties], extra=[s1_error, s1_select, s1_open]),
    2: dict(name="Rotations and their properties", std=["8.G.A.1", "8.G.A.3"], fams=[s2_point, s2_figure_vertex, s2_identify_angle, s2_property, s2_reverse], extra=[s2_error, s2_select, s2_open]),
    3: dict(name="Reflections and their properties", std=["8.G.A.1", "8.G.A.3"], fams=[s3_point, s3_figure, s3_vertical_line, s3_orientation], extra=[s3_error, s3_select, s3_open]),
    4: dict(name="Translations and their properties", std=["8.G.A.1", "8.G.A.3"], fams=[s4_point, s4_rule, s4_figure, s4_compose], extra=[s4_error, s4_select, s4_open]),
    5: dict(name="Dilations and their properties", std=["8.G.A.3", "8.G.A.4"], fams=[s5_point, s5_scale_factor, s5_enlarge, s5_measure, s5_center], extra=[s5_error, s5_select, s5_open]),
    6: dict(name="Sequences of transformations: congruence and similarity", std=["8.G.A.2", "8.G.A.4"], fams=[s6_apply, s6_cong_or_sim, s6_find_sequence, s6_order_matters], extra=[s6_error, s6_select, s6_open]),
    7: dict(name="Sum of the angles in a triangle", std=["8.G.A.5"], fams=[s7_missing, s7_algebra, s7_exterior, s7_possible], extra=[s7_error, s7_select, s7_open]),
    8: dict(name="Similar triangles", std=["8.G.A.4", "8.G.A.5"], fams=[s8_missing_side, s8_aa, s8_shadow, s8_scale_perimeter, s8_nested], extra=[s8_error, s8_select, s8_open]),
    9: dict(name="Parallel lines cut by a transversal", std=["8.G.A.5"], fams=[s9_find_angle, s9_relationship, s9_algebra, s9_triangle_link], extra=[s9_error, s9_select, s9_open]),
}
