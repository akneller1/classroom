"""Grade 6 Unit 6 — Geometry (geometry)."""
from glib import *
import g7_u10 as V7, g7_u01 as A7

UNIT_ID = "geometry"
ABBR = "geo"


# ============================================================== S1 Special quadrilaterals
@fam("012")
def s1_quad(r, L):
    kind = pick(r, ["rectangle", "square", "rhombus", "kite"]) if L < 2 else pick(r, ["rhombus", "kite", "parallelogram"])
    if kind in ("rectangle", "square"):
        l = r.randint(2, 20)
        w = l if kind == "square" else r.randint(2, 20)
        A = l * w
        return Q(f"Find the area of a {kind} with {'side' if kind == 'square' else 'length ' + str(l) + ' cm and width'} {w} cm.", f"{A} cm²", [f"A = {'s²' if kind == 'square' else 'lw'}.", f"A = {l} × {w} = {A} cm²."],
                 [f"{2 * (l + w)} cm²", f"{l + w} cm²", f"{2 * l * w} cm²"], V(f"{l}*{w}"), why=["Found the perimeter", "Added the dimensions", "Doubled the area"])
    if kind == "parallelogram":
        b, h = F(r.randint(5, 40), 2), r.randint(2, 15)
        return Q(f"A parallelogram has base {mixed(b)} in. and height {h} in. Find its area.", f"{mixed(b * h)} in²", ["A = bh.", f"A = {mixed(b)} × {h} = {mixed(b * h)} in²."],
                 [f"{mixed(b * h / 2)} in²", f"{mixed(2 * (b + h))} in²", f"{mixed(b + h)} in²"], V(f"{N(b)}*{h}"), why=["Divided by 2 as for a triangle", "Found the perimeter", "Added base and height"])
    d1, d2 = r.randint(2, 20), r.randint(2, 20)
    A = F(d1 * d2, 2)
    return Q(f"A {kind} has diagonals of {d1} m and {d2} m. Find its area.", f"{mixed(A)} m²", [f"A {kind} splits into triangles; A = (d₁ × d₂) ÷ 2.", f"A = ({d1} × {d2}) ÷ 2 = {mixed(A)} m²."],
             [f"{d1 * d2} m²", f"{d1 + d2} m²", f"{2 * (d1 + d2)} m²"], V(f"{d1}*{d2}/2"), why=["Forgot to divide by 2", "Added the diagonals", "Found a perimeter-like sum"], tags=["connections"])


# ============================================================== S2 Right triangles
@fam("012")
def s2_right(r, L):
    a, b = r.randint(2, 20), r.randint(2, 20)
    if L == 2:
        a = F(2 * a + 1, 2)
    A = F(a) * b / 2
    pts = [(0, 0), (float(b), 0), (0, float(a))]
    return Q(f"A right triangle has legs {mixed(F(a))} ft and {b} ft. Find its area.", f"{mixed(A)} ft²", ["The legs are the base and the height.", f"A = (1/2)({mixed(F(a))})({b}).", f"A = {mixed(A)} ft²."],
             [f"{mixed(F(a) * b)} ft²", f"{mixed(F(a) + b)} ft²", f"{mixed(A / 2)} ft²"], V(f"1/2*{N(F(a))}*{b}"), why=["Forgot the 1/2", "Added the legs", "Divided by 2 twice"],
             diagram={"alt": f"Right triangle with legs {mixed(F(a))} and {b}.", "draw": poly_draw(pts, side_labels=[(0, str(b)), (2, mixed(F(a)))], right_angles=[0])} if L == 0 else None)


@fam("12")
def s2_half_rect(r, L):
    l, w = r.randint(3, 20), r.randint(3, 20)
    return Q(f"A rectangle {l} cm by {w} cm is cut along a diagonal into two right triangles. What is the area of one triangle?", f"{mixed(F(l * w, 2))} cm²",
             [f"Rectangle area: {l} × {w} = {l * w}.", "The diagonal splits it into two congruent triangles.", f"One triangle: {l * w} ÷ 2 = {mixed(F(l * w, 2))} cm²."],
             [f"{l * w} cm²", f"{mixed(F(l * w, 4))} cm²", f"{l + w} cm²"], V(f"{l}*{w}/2"), why=["Forgot to halve", "Halved twice", "Added the sides"], tags=["reasoning"])


# ============================================================== S3 All triangles
@fam("12")
def s3_missing(r, L):
    b, h = r.randint(2, 20), r.randint(2, 20)
    A = F(b * h, 2)
    return Q(f"A triangle has area {mixed(A)} m² and base {b} m. Find its height.", f"{h} m", [f"A = (1/2)bh, so {mixed(A)} = (1/2)({b})h.", f"{mixed(A)} = {N(F(b, 2))}h.", f"h = {h} m."],
             [f"{mixed(A / b)} m", f"{mixed(2 * A * b)} m", f"{mixed(A - b)} m"], EQ(f"{N(A)} = 1/2*{b}*h", "h"), why=["Forgot the 1/2", "Multiplied instead of dividing", "Subtracted instead of dividing"], tags=["reasoning"])


# ============================================================== S4 Composite polygons
@fam("012")
def s4_lshape(r, L):
    W, H = r.randint(6, 16), r.randint(6, 16)
    w, h = r.randint(2, W - 2), r.randint(2, H - 2)
    A = W * H - w * h
    pts = [(0, 0), (W, 0), (W, H - h), (W - w, H - h), (W - w, H), (0, H)]
    alt = f"L-shaped figure: a {W} by {H} rectangle with a {w} by {h} rectangle removed from the top-right corner. Labelled sides: bottom {W}, left {H}, notch width {w}, notch height {h}."
    return Q(f"Find the area of the L-shaped figure. The outer rectangle is {W} m by {H} m, and a {w} m by {h} m corner piece is cut out.", f"{A} m²",
             [f"Outer rectangle: {W} × {H} = {W * H}.", f"Cut-out: {w} × {h} = {w * h}.", f"Area = {W * H} - {w * h} = {A} m².", "(Or split into two rectangles and add.)"],
             [f"{W * H} m²", f"{W * H + w * h} m²", f"{2 * (W + H)} m²"], V(f"{W}*{H} - {w}*{h}"), why=["Forgot to subtract the cut-out", "Added the cut-out", "Found the perimeter"], tags=["multistep", "connections"],
             diagram={"alt": alt, "draw": poly_draw(pts, side_labels=[(0, str(W)), (5, str(H)), (2, str(w)), (3, str(h))])})


@fam("012")
def s4_house(r, L):
    w, h, t = r.randint(4, 16), r.randint(3, 12), r.randint(2, 8)
    A = w * h + F(w * t, 2)
    pts = [(0, 0), (w, 0), (w, h), (F(w, 2), h + t), (0, h)]
    alt = f"Pentagon shaped like a house: a {w} by {h} rectangle with a triangle of base {w} and height {t} on top."
    return Q(f"A figure is a rectangle {w} ft wide and {h} ft tall with a triangle on top (base {w} ft, height {t} ft). Find its total area.", f"{mixed(A)} ft²",
             [f"Rectangle: {w} × {h} = {w * h}.", f"Triangle: (1/2)({w})({t}) = {mixed(F(w * t, 2))}.", f"Total: {mixed(A)} ft²."],
             [f"{w * h + w * t} ft²", f"{w * (h + t)} ft²", f"{mixed(F(w * (h + t), 2))} ft²"], V(f"{w}*{h} + 1/2*{w}*{t}"), why=["Forgot the 1/2 for the triangle", "Treated the whole shape as a rectangle", "Treated the whole shape as a triangle"],
             tags=["multistep"], diagram={"alt": alt, "draw": poly_draw(pts, side_labels=[(0, str(w)), (1, str(h))], extra_lines=[((F(w, 2), h + t), (F(w, 2), h), str(t), True)])} if L else None)


# ============================================================== S5 Volume of right rectangular prisms
@fam("012")
def s5_volume(r, L):
    if L == 0:
        l, w, h = F(r.randint(2, 12)), F(r.randint(2, 10)), F(r.randint(2, 10))
    else:
        l, w, h = [F(r.randint(2, 9)) + pick(r, [F(0), F(1, 2), F(1, 4)]) for _ in range(3)]
        need(any(x.denominator > 1 for x in (l, w, h)))
    v = l * w * h
    return Q(f"Find the volume of a rectangular prism {mixed(l)} in. long, {mixed(w)} in. wide, and {mixed(h)} in. tall.", f"{mixed(v)} in³", ["V = lwh.", f"V = {mixed(l)} × {mixed(w)} × {mixed(h)}.", f"V = {mixed(v)} in³."],
             [f"{mixed(l + w + h)} in³", f"{mixed(2 * (l * w + l * h + w * h))} in³", f"{mixed(l * w)} in³"], V(f"{N(l)}*{N(w)}*{N(h)}"), why=["Added the dimensions", "Found the surface area", "Found only the base area"],
             diagram={"alt": f"Rectangular prism {mixed(l)} by {mixed(w)} by {mixed(h)}.", "draw": box3d_draw(mixed(l), mixed(w), mixed(h))} if L == 1 else None)


@fam("12")
def s5_cubes(r, L):
    l, w, h = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
    s = F(1, 2) if L == 1 else pick(r, [F(1, 2), F(1, 3), F(1, 4)])
    n = int(l / s * w / s * h / s)
    return Q(f"How many cubes with edge {N(s)} inch fill a box {l} in. by {w} in. by {h} in.?", str(n), [f"Along each edge: {l} ÷ {N(s)} = {int(l / s)}, {w} ÷ {N(s)} = {int(w / s)}, {h} ÷ {N(s)} = {int(h / s)}.", f"{int(l / s)} × {int(w / s)} × {int(h / s)} = {n} cubes.",
                                                                                                    f"Check: {n} × ({N(s)})³ = {l * w * h} in³."],
             [str(l * w * h), str(int(l * w * h / s)), str(int(l * w * h / s / s))], V(f"({l}*{w}*{h})/({N(s)})^3"), why=["Counted 1-inch cubes", "Divided by the edge length only once", "Divided by the edge length only twice"], tags=["reasoning"])


@fam("2")
def s5_missing(r, L):
    l, w = F(r.randint(2, 9)) + F(1, 2), F(r.randint(2, 8))
    h = F(r.randint(2, 9))
    v = l * w * h
    return Q(f"A box has volume {mixed(v)} cm³, length {mixed(l)} cm, and width {mixed(w)} cm. Find its height.", f"{mixed(h)} cm", [f"V = lwh: {mixed(v)} = {mixed(l)} × {mixed(w)} × h.", f"{mixed(v)} = {mixed(l * w)}h.", f"h = {mixed(h)} cm."],
             [f"{mixed(v - l - w)} cm", f"{mixed(v / l)} cm", f"{mixed(v * l * w)} cm"], EQ(f"{N(v)} = {N(l)}*{N(w)}*h", "h"), why=["Subtracted instead of dividing", "Divided by only one dimension", "Multiplied instead of dividing"])


# ============================================================== S6 / S7 Polygons on the coordinate plane
@fam("012")
def s6_fourth(r, L):
    x1, y1 = r.randint(-7, 2), r.randint(-7, 2)
    w, h = r.randint(2, 6), r.randint(2, 6)
    pts = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
    i = r.randrange(4)
    given = [p for k, p in enumerate(pts) if k != i]
    x, y = pts[i]
    return Q(f"Three vertices of a rectangle are {', '.join(f'({a}, {b})' for a, b in given)}. What are the coordinates of the fourth vertex?", f"({x}, {y})",
             ["Opposite sides of a rectangle are parallel to the axes here.", "The missing vertex shares its x-coordinate with one vertex and its y-coordinate with another.", f"({x}, {y})."],
             [f"({y}, {x})", f"({-x}, {y})", f"({x}, {-y})" if y else f"({x + 1}, {y})"], PY("point", x=str(x), y=str(y)), why=["Switched the coordinates", "Used the wrong sign", "Used the wrong sign"], tags=["reasoning"])


@fam("012")
def s6_side(r, L):
    x1, y1 = r.randint(-8, 3), r.randint(-8, 3)
    if r.random() < 0.5:
        x2, y2 = x1 + r.randint(2, 9), y1
    else:
        x2, y2 = x1, y1 + r.randint(2, 9)
    d = abs(x2 - x1) + abs(y2 - y1)
    alt = f"Coordinate plane with segment AB from ({x1}, {y1}) to ({x2}, {y2})."
    return Q(f"Polygon side AB goes from A({x1}, {y1}) to B({x2}, {y2}). How long is side AB?", f"{d} units", ["The side is horizontal or vertical, so subtract the coordinates that change.", f"|{x2 if x1 != x2 else y2} - ({x1 if x1 != x2 else y1})| = {d}."],
             [f"{abs(abs(x2) - abs(x1)) + abs(abs(y2) - abs(y1))} units" if abs(abs(x2) - abs(x1)) + abs(abs(y2) - abs(y1)) != d else f"{d + 1} units", f"{abs(x2 + x1) + abs(y2 + y1)} units", f"{d * 2} units"],
             PY("absval", expr=f"|{x2} - ({x1})| + |{y2} - ({y1})|"), why=["Subtracted the absolute values", "Added the coordinates", ""], tags=["graph"],
             diagram={"alt": alt, "draw": plane_draw((-9, 9), (-9, 9), polys=[([(x1, y1), (x2, y2)], None, None, False)], points=[(x1, y1, "A"), (x2, y2, "B")])} if L == 0 else None)


@fam("012")
def s7_area_grid(r, L):
    x1, y1 = r.randint(-7, 0), r.randint(-7, 0)
    w, h = r.randint(2, 8), r.randint(2, 8)
    if L == 2 and r.random() < 0.5:
        pts = [(x1, y1), (x1 + w, y1), (x1, y1 + h)]
        A = F(w * h, 2)
        what = "area"
        alt = f"Right triangle with vertices " + ", ".join(f"({a}, {b})" for a, b in pts) + "."
        return Q(f"Find the area of the triangle with vertices {', '.join(f'({a}, {b})' for a, b in pts)}.", f"{mixed(A)} units²", [f"Base = {w}, height = {h} (horizontal and vertical legs).", f"A = (1/2)({w})({h}) = {mixed(A)}."],
                 [f"{w * h} units²", f"{w + h} units²", f"{mixed(A / 2)} units²"], V(f"{w}*{h}/2"), why=["Forgot the 1/2", "Added the legs", "Halved twice"], tags=["graph"],
                 diagram={"alt": alt, "draw": plane_draw((-8, 9), (-8, 9), polys=[(pts, None, None, True)], points=[(a, b, "") for a, b in pts])})
    pts = [(x1, y1), (x1 + w, y1), (x1 + w, y1 + h), (x1, y1 + h)]
    what = pick(r, ["area", "perimeter"])
    v = w * h if what == "area" else 2 * (w + h)
    u = "units²" if what == "area" else "units"
    alt = "Rectangle with vertices " + ", ".join(f"({a}, {b})" for a, b in pts) + "."
    return Q(f"Find the {what} of the rectangle with vertices {', '.join(f'({a}, {b})' for a, b in pts)}.", f"{v} {u}", [f"Width = {w}, height = {h}.", f"{what.capitalize()} = {'w × h' if what == 'area' else '2(w + h)'} = {v}."],
             [f"{2 * (w + h) if what == 'area' else w * h} {u}", f"{w + h} {u}", f"{v + 2} {u}"], V(f"{w}*{h}" if what == "area" else f"2*({w} + {h})"),
             why=["Found the wrong measure", "Added only two sides", ""], tags=["graph"], diagram={"alt": alt, "draw": plane_draw((-8, 9), (-8, 9), polys=[(pts, None, None, True)])} if L == 1 else None)


# ============================================================== S8 Nets and surface area
@fam("012")
def s8_cube(r, L):
    s = r.randint(2, 12) if L < 2 else F(r.randint(3, 15), 2)
    sa = 6 * F(s) * s
    return Q(f"A cube has edges of {mixed(F(s))} cm. Its net has 6 squares. What is the surface area?", f"{mixed(sa)} cm²", ["A cube's net is 6 congruent squares.", f"One face: {mixed(F(s))} × {mixed(F(s))} = {mixed(F(s) * s)}.", f"SA = 6 × {mixed(F(s) * s)} = {mixed(sa)} cm²."],
             [f"{mixed(F(s) ** 3)} cm²", f"{mixed(4 * F(s) * s)} cm²", f"{mixed(6 * F(s))} cm²"], V(f"6*({N(F(s))})^2"), why=["Found the volume", "Counted only 4 faces", "Did not square the edge"])


@fam("012", mode="mc")
def s8_net_faces(r, L):
    solids = [("square pyramid", "1 square and 4 triangles"), ("triangular prism", "2 triangles and 3 rectangles"), ("rectangular prism", "6 rectangles"), ("triangular pyramid", "4 triangles"),
              ("cube", "6 squares"), ("pentagonal prism", "2 pentagons and 5 rectangles")]
    s, f_ = pick(r, solids)
    others = [x[1] for x in solids if x[0] != s]
    r.shuffle(others)
    opts = [(f_, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"Which shapes make up a net of a {s}?", f_, [f"A {s} has these faces: {f_}."], options=opts, chk=PY("net_faces", solid=s), mode="mc")


@fam("12")
def s8_tri_prism(r, L):
    b, h = r.randint(3, 10), r.randint(2, 8)
    s1, s2 = r.randint(h + 1, 14), r.randint(h + 1, 14)
    ln = r.randint(4, 15)
    sa = b * h + (b + s1 + s2) * ln
    return Q(f"A triangular prism's net has two triangles (base {b} cm, height {h} cm) and three rectangles that are {ln} cm long and {b} cm, {s1} cm, and {s2} cm wide. Find the surface area.", f"{sa} cm²",
             [f"Two triangles: 2 × (1/2)({b})({h}) = {b * h}.", f"Rectangles: {ln} × ({b} + {s1} + {s2}) = {(b + s1 + s2) * ln}.", f"SA = {sa} cm²."],
             [f"{N(F(b * h, 2)) if b * h % 2 == 0 else b * h + 1} cm²" if False else f"{F(b * h, 2) + (b + s1 + s2) * ln} cm²", f"{2 * b * h + (b + s1 + s2) * ln} cm²", f"{b * h + 3 * b * ln} cm²"],
             V(f"2*(1/2*{b}*{h}) + {ln}*({b} + {s1} + {s2})"), why=["Counted only one triangle", "Forgot the 1/2 for the triangles", "Used the same width for all three rectangles"], tags=["multistep"])


SKILLS = {
    1: dict(name="Area of Special Quadrilaterals", std=["6.G.A.1"], fams=[s1_quad, reuse(V7.s1_area, (0, 0, 1)), reuse(V7.s2_trapezoid, (0, 1, 2))], extra=[err_of(s1_quad), open_of(s1_quad), select_of(s1_quad)]),
    2: dict(name="Area of Right Triangles", std=["6.G.A.1"], fams=[s2_right, s2_half_rect], extra=[err_of(s2_right), open_of(s2_right)]),
    3: dict(name="Area of All Triangles", std=["6.G.A.1"], fams=[reuse(V7.s2_triangle), s3_missing], extra=[err_of(reuse(V7.s2_triangle, (0, 1, 2), "e")), open_of(reuse(V7.s2_triangle, (1, 1, 2), "o")), select_of(reuse(V7.s2_triangle, (1, 1, 2), "s"))]),
    4: dict(name="Area of Polygons Through Composition and Decomposition", std=["6.G.A.1"], fams=[s4_lshape, s4_house], extra=[err_of(s4_house), err_of(s4_lshape)]),
    5: dict(name="Volume of Right Rectangular Prisms", std=["6.G.A.2"], fams=[s5_volume, s5_cubes, s5_missing], extra=[err_of(s5_volume), open_of(s5_volume), select_of(s5_volume)]),
    6: dict(name="Polygons on the Coordinate Plane", std=["6.G.A.3"], fams=[s6_fourth, s6_side, reuse(A7.s12_quadrant, (0, 1, 1))], extra=[err_of(s6_fourth), open_of(s6_side)]),
    7: dict(name="Perimeter and Area of Polygons on the Coordinate Plane", std=["6.G.A.3", "6.NS.C.8"], fams=[s7_area_grid, reuse(A7.s12_rect, (2, 2, 2))], extra=[err_of(s7_area_grid), open_of(reuse(A7.s12_rect, (2, 2, 2), "o"))]),
    8: dict(name="Nets and Surface Area", std=["6.G.A.4"], fams=[s8_cube, s8_net_faces, s8_tri_prism, reuse(V7.s5_prism)], extra=[err_of(s8_cube), open_of(s8_cube)]),
}
