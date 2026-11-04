"""Grade 7 Unit 10 — Area and Volume (area-volume)."""
from glib import *

UNIT_ID = "area-volume"
ABBR = "arv"


def PI(L):
    return ("π", "π") if L == 2 else ("3.14", "3.14 for π")


# ============================================================== S1 Parallelograms
@fam("012")
def s1_area(r, L):
    b, h = r.randint(3, 20), r.randint(2, 15)
    s = r.randint(h + 1, h + 6)
    if L == 2:
        b, h = F(r.randint(5, 40), 2), F(r.randint(4, 20), 2)
    off = 2
    pts = [(0, 0), (float(b), 0), (float(b) + off, float(h)), (off, float(h))]
    alt = f"Parallelogram with base {N(b) if F(b).denominator == 1 else D(b)} units, slanted side {s} units, and a dashed height of {D(F(h))} units."
    A = F(b) * F(h)
    return Q(f"Find the area of the parallelogram. Base = {D(F(b))} m, height = {D(F(h))} m, slanted side = {s} m.", f"{D(A)} m²",
             ["A = bh (use the perpendicular height, not the slanted side).", f"A = {D(F(b))} × {D(F(h))}.", f"A = {D(A)} m²."],
             [f"{D(F(b) * s)} m²", f"{D(A / 2)} m²", f"{D(2 * (F(b) + s))} m²"], V(f"{D(F(b))}*{D(F(h))}"),
             why=["Used the slanted side as the height", "Divided by 2 as if it were a triangle", "Found the perimeter"], tags=["connections"],
             diagram={"alt": alt, "draw": poly_draw(pts, side_labels=[(0, D(F(b))), (1, str(s))], extra_lines=[((off, float(h)), (off, 0), D(F(h)), True)])} if L < 2 else None)


@fam("012")
def s1_missing(r, L):
    b, h = r.randint(3, 20), r.randint(2, 15)
    A = b * h
    what = pick(r, ["base", "height"])
    known = h if what == "base" else b
    v = b if what == "base" else h
    return Q(f"A parallelogram has area {A} in² and {'height' if what == 'base' else 'base'} {known} inches. Find its {what}.", f"{v} inches",
             [f"A = bh, so {A} = {what[0]} × {known}." if False else f"{A} = {known} × {what}.", f"Divide: {A} ÷ {known}.", f"{what} = {v} inches."],
             [f"{A * known} inches", f"{A - known} inches", f"{N(F(A, 2 * known))} inches"], V(f"{A}/{known}"), why=["Multiplied instead of dividing", "Subtracted instead of dividing", "Divided by 2 as if it were a triangle"])


# ============================================================== S2 Triangles and Trapezoids
@fam("012")
def s2_triangle(r, L):
    b, h = r.randint(3, 24), r.randint(2, 18)
    A = F(b * h, 2)
    pts = [(0, 0), (b, 0), (r.randint(1, b - 1) if b > 2 else 1, h)]
    alt = f"Triangle with base {b} units and a dashed height of {h} units drawn from the top vertex to the base."
    return Q(f"Find the area of a triangle with base {b} cm and height {h} cm.", f"{D(A)} cm²", ["A = (1/2)bh.", f"A = (1/2)({b})({h}).", f"A = {D(A)} cm²."],
             [f"{b * h} cm²", f"{b + h} cm²", f"{D(A / 2)} cm²"], V(f"1/2*{b}*{h}"), why=["Forgot to multiply by 1/2", "Added the base and height", "Divided by 2 twice"],
             diagram={"alt": alt, "draw": poly_draw(pts, side_labels=[(0, str(b))], extra_lines=[(pts[2], (pts[2][0], 0), str(h), True)])} if L == 0 else None)


@fam("012")
def s2_trapezoid(r, L):
    b1, b2, h = r.randint(3, 15), r.randint(4, 20), r.randint(2, 12)
    need(b1 != b2)
    if L == 2:
        b1, b2 = F(2 * b1 + 1, 2), b2
    A = (F(b1) + b2) * h / 2
    sh = r.randint(0, 3)
    pts = [(0, 0), (float(b2), 0), (sh + float(b1), h), (sh, h)] if b2 > b1 else [(0, 0), (float(b2), 0), (float(b2), h), (0, h)]
    return Q(f"Find the area of a trapezoid with bases {D(F(b1))} ft and {b2} ft and height {h} ft.", f"{D(A)} ft²",
             ["A = (1/2)(b₁ + b₂)h.", f"A = (1/2)({D(F(b1))} + {b2})({h}).", f"A = (1/2)({D(F(b1) + b2)})({h}) = {D(A)} ft²."],
             [f"{D((F(b1) + b2) * h)} ft²", f"{D(F(b1) * b2 * h / 2)} ft²", f"{D(F(b1) + b2 + h)} ft²"], V(f"1/2*({D(F(b1))} + {b2})*{h}"),
             why=["Forgot to multiply by 1/2", "Multiplied the bases instead of adding", "Added all the dimensions"],
             diagram={"alt": f"Trapezoid with parallel bases {D(F(b1))} and {b2} and height {h}.", "draw": poly_draw(pts, side_labels=[(0, str(b2)), (2, D(F(b1)))], extra_lines=[((sh + 0.2, h), (sh + 0.2, 0), str(h), True)])} if L == 1 and b2 > b1 else None)


@fam("2")
def s2_missing(r, L):
    b1, b2, h = r.randint(3, 15), r.randint(4, 20), r.randint(2, 12) * 2
    A = (b1 + b2) * h // 2
    return Q(f"A trapezoid has area {A} m² and bases {b1} m and {b2} m. Find its height.", f"{h} meters", [f"{A} = (1/2)({b1} + {b2})h.", f"{A} = {N(F(b1 + b2, 2))}h.", f"h = {A} ÷ {N(F(b1 + b2, 2))} = {h} meters."],
             [f"{N(F(A, b1 + b2))} meters", f"{N(F(2 * A, b1 * b2))} meters", f"{A - b1 - b2} meters"], EQ(f"{A} = 1/2*({b1} + {b2})*h", "h"),
             why=["Forgot the 1/2", "Multiplied the bases", "Subtracted the bases"], tags=["multistep"])


# ============================================================== S3 Area of Circles
@fam("012")
def s3_area(r, L):
    rad = r.randint(2, 15)
    given = pick(r, ["radius", "diameter"]) if L else "radius"
    gv = rad if given == "radius" else 2 * rad
    if r.random() < 0.4:
        return Q(f"A circle has a {given} of {gv} cm. Find its area in terms of π.", f"{rad * rad}π cm²", ["A = πr².", f"r = {rad}.", f"A = π({rad})² = {rad * rad}π cm²."],
                 [f"{2 * rad}π cm²", f"{4 * rad * rad}π cm²", f"{rad}π cm²"], PY("pi_coef", k=rad * rad),
                 why=["Multiplied the radius by 2 instead of squaring it", "Used the diameter as the radius", "Did not square the radius"])
    pv, pt_ = PI(L)
    A = (math.pi if L == 2 else 3.14) * rad * rad
    return Q(f"A circle has a {given} of {gv} cm. Find its area. Use {pt_} and round to the nearest tenth.", f"{Rd(A, 1)} cm²",
             ["A = πr².", f"r = {rad}.", f"A = {pv} × {rad}² ≈ {Rd(A, 1)} cm²."], [f"{Rd((math.pi if L == 2 else 3.14) * 2 * rad, 1)} cm²",
                                                                                                     f"{Rd((math.pi if L == 2 else 3.14) * 4 * rad * rad, 1)} cm²", f"{Rd((math.pi if L == 2 else 3.14) * rad, 1)} cm²"],
             AP(f"{pv}*{rad}^2", 1), why=["Found the circumference", "Used the diameter as the radius", "Did not square the radius"])


@fam("12")
def s3_composite(r, L):
    w = r.randint(2, 10) * 2
    l = r.randint(w, 30)
    rad = w // 2
    A = l * w + math.pi * rad * rad / 2
    return Q(f"A figure is a rectangle {l} m by {w} m with a semicircle attached to one {w}-m side. Find the total area. Use π and round to the nearest tenth.", f"{Rd(A, 1)} m²",
             [f"Rectangle: {l} × {w} = {l * w}.", f"Semicircle radius = {rad}: (1/2)π({rad})² ≈ {Rd(math.pi * rad * rad / 2, 2)}.", f"Total ≈ {Rd(A, 1)} m²."],
             [f"{Rd(l * w + math.pi * rad * rad, 1)} m²", f"{Rd(l * w + math.pi * w * w / 2, 1)} m²", f"{Rd(l * w + math.pi * rad, 1)} m²"],
             AP(f"{l}*{w} + π*{rad}^2/2", 1), why=["Used a full circle instead of a semicircle", "Used the diameter as the radius", "Used the circumference formula"], tags=["multistep", "connections"])


@fam("2")
def s3_reverse(r, L):
    rad = r.randint(2, 15)
    return Q(f"A circle has an area of {rad * rad}π in². What is its diameter?", f"{2 * rad} inches", [f"πr² = {rad * rad}π, so r² = {rad * rad}.", f"r = {rad}.", f"d = 2r = {2 * rad} inches."],
             [f"{rad} inches", f"{N(F(rad * rad, 2))} inches", f"{rad * rad} inches"], V(f"2*√{rad * rad}"), why=["Gave the radius", "Halved the area", "Did not take the square root"], tags=["reasoning"])


# ============================================================== S4 Space Figures
SOLIDS = {"triangular prism": (5, 6, 9), "rectangular prism": (6, 8, 12), "pentagonal prism": (7, 10, 15), "hexagonal prism": (8, 12, 18),
          "triangular pyramid": (4, 4, 6), "square pyramid": (5, 5, 8), "pentagonal pyramid": (6, 6, 10), "hexagonal pyramid": (7, 7, 12)}


@fam("012")
def s4_count(r, L):
    s = pick(r, list(SOLIDS))
    f, v, e = SOLIDS[s]
    what = pick(r, ["faces", "vertices", "edges"])
    val = {"faces": f, "vertices": v, "edges": e}[what]
    others = [x for x in (f, v, e) if x != val] + [val + 2]
    return Q(f"How many {what} does a {s} have?", str(val), ["Faces are flat surfaces, edges are segments where faces meet, and vertices are corners.", f"A {s} has {f} faces, {v} vertices, and {e} edges.",
                                                            f"Check with Euler's formula: F + V - E = {f} + {v} - {e} = 2."],
             [str(o) for o in others], PY("solid_count", solid=s, what=what), why=["Counted a different part", "Counted a different part", "Miscounted"])


@fam("012", mode="mc")
def s4_name(r, L):
    descs = [("two congruent circular bases and a curved surface", "cylinder"), ("one circular base and one vertex", "cone"), ("all points the same distance from the center", "sphere"),
             ("two congruent triangular bases and three rectangular faces", "triangular prism"), ("one square base and four triangular faces", "square pyramid"),
             ("six congruent square faces", "cube")]
    d, s = pick(r, descs)
    others = [x[1] for x in descs if x[1] != s]
    r.shuffle(others)
    opts = [(s, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"Which solid has {d}?", s, [f"A {s} has {d}."], options=opts, chk=TXT(s), mode="mc")


@fam("2")
def s4_euler(r, L):
    f, v = r.randint(5, 12), r.randint(5, 12)
    e = f + v - 2
    return Q(f"A polyhedron has {f} faces and {v} vertices. How many edges does it have?", str(e), ["Euler's formula: F + V - E = 2.", f"{f} + {v} - E = 2.", f"E = {e}."],
             [str(f + v), str(f + v + 2), str(abs(f - v) + 2)], EQ(f"{f} + {v} - x = 2"), why=["Forgot to subtract 2", "Added 2 instead of subtracting", ""], tags=["reasoning"])


# ============================================================== S5 Surface Area of Prisms and Cylinders
@fam("012")
def s5_prism(r, L):
    l, w, h = r.randint(2, 15), r.randint(2, 12), r.randint(2, 10)
    sa = 2 * (l * w + l * h + w * h)
    return Q(f"Find the surface area of a rectangular prism {l} cm long, {w} cm wide, and {h} cm high.", f"{sa} cm²",
             ["SA = 2lw + 2lh + 2wh.", f"2({l})({w}) + 2({l})({h}) + 2({w})({h}).", f"= {2 * l * w} + {2 * l * h} + {2 * w * h} = {sa} cm²."],
             [f"{l * w * h} cm²", f"{l * w + l * h + w * h} cm²", f"{2 * l * w + l * h + w * h} cm²"], V(f"2*({l}*{w} + {l}*{h} + {w}*{h})"),
             why=["Found the volume", "Counted each face only once", "Doubled only the bases"], tags=["connections"],
             diagram={"alt": f"Rectangular prism labelled length {l}, width {w}, height {h}.", "draw": box3d_draw(l, w, h)} if L == 0 else None)


@fam("012")
def s5_cylinder(r, L):
    rad, h = r.randint(2, 10), r.randint(2, 15)
    pv, pt_ = PI(L)
    p = math.pi if L == 2 else 3.14
    sa = 2 * p * rad * rad + 2 * p * rad * h
    if L == 0:
        return Q(f"Find the surface area of a cylinder with radius {rad} in. and height {h} in. Write the answer in terms of π.", f"{2 * rad * rad + 2 * rad * h}π in²",
                 ["SA = 2πr² + 2πrh.", f"2π({rad})² + 2π({rad})({h}).", f"= {2 * rad * rad}π + {2 * rad * h}π = {2 * rad * rad + 2 * rad * h}π in²."],
                 [f"{rad * rad * h}π in²", f"{rad * rad + 2 * rad * h}π in²", f"{2 * rad * h}π in²"], PY("pi_coef", k=2 * rad * rad + 2 * rad * h),
                 why=["Found the volume", "Counted only one base", "Found only the lateral area"])
    return Q(f"Find the surface area of a cylinder with radius {rad} cm and height {h} cm. Use {pt_} and round to the nearest tenth.", f"{Rd(sa, 1)} cm²",
             ["SA = 2πr² + 2πrh.", f"= 2({pv})({rad})² + 2({pv})({rad})({h}).", f"≈ {Rd(sa, 1)} cm²."],
             [f"{Rd(p * rad * rad * h, 1)} cm²", f"{Rd(p * rad * rad + 2 * p * rad * h, 1)} cm²", f"{Rd(2 * p * rad * h, 1)} cm²"],
             AP(f"2*{pv}*{rad}^2 + 2*{pv}*{rad}*{h}", 1), why=["Found the volume", "Counted only one base", "Found only the lateral area"],
             diagram={"alt": f"Cylinder with radius {rad} and height {h}.", "draw": cyl_draw(str(rad), str(h))} if L == 1 else None)


@fam("2")
def s5_tri_prism(r, L):
    a, b, c = pick(r, [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15)])
    h = r.randint(4, 15)
    sa = a * b + (a + b + c) * h
    return Q(f"A triangular prism has right-triangle bases with legs {a} and {b} and hypotenuse {c} (in meters). The prism is {h} m long. Find its surface area.", f"{sa} m²",
             [f"Two bases: 2 × (1/2)({a})({b}) = {a * b}.", f"Three rectangles: ({a} + {b} + {c}) × {h} = {(a + b + c) * h}.", f"SA = {a * b} + {(a + b + c) * h} = {sa} m²."],
             [f"{a * b * h // 2} m²", f"{a * b // 2 + (a + b + c) * h} m²", f"{2 * a * b + (a + b + c) * h} m²"], V(f"2*(1/2*{a}*{b}) + ({a} + {b} + {c})*{h}"),
             why=["Found the volume", "Counted only one base", "Forgot the 1/2 in the triangle area"], tags=["multistep"])


# ============================================================== S6 SA of Pyramids, Cones, Spheres
@fam("012")
def s6_pyramid(r, L):
    s, l = r.randint(3, 14), r.randint(4, 15)
    sa = s * s + 2 * s * l
    return Q(f"A square pyramid has base edge {s} ft and slant height {l} ft. Find its surface area.", f"{sa} ft²",
             [f"Base: {s}² = {s * s}.", f"Four triangles: 4 × (1/2)({s})({l}) = {2 * s * l}.", f"SA = {s * s} + {2 * s * l} = {sa} ft²."],
             [f"{s * s + 4 * s * l} ft²", f"{2 * s * l} ft²", f"{N(F(s * s * l, 3))} ft²"], V(f"{s}^2 + 4*(1/2*{s}*{l})"),
             why=["Forgot the 1/2 in each triangle", "Left out the base", "Found the volume (using slant height)"])


@fam("012")
def s6_sphere(r, L):
    rad = r.randint(2, 12)
    if L == 0:
        return Q(f"Find the surface area of a sphere with radius {rad} cm. Write the answer in terms of π.", f"{4 * rad * rad}π cm²", ["SA = 4πr².", f"4π({rad})² = {4 * rad * rad}π cm²."],
                 [f"{rad * rad}π cm²", f"{8 * rad}π cm²", f"{N(F(4 * rad ** 3, 3))}π cm²"], PY("pi_coef", k=4 * rad * rad),
                 why=["Forgot the 4", "Multiplied the radius by 2 instead of squaring", "Found the volume"])
    pv, pt_ = PI(L)
    p = math.pi if L == 2 else 3.14
    return Q(f"Find the surface area of a sphere with diameter {2 * rad} m. Use {pt_} and round to the nearest tenth.", f"{Rd(4 * p * rad * rad, 1)} m²",
             [f"r = {rad}.", "SA = 4πr².", f"4 × {pv} × {rad}² ≈ {Rd(4 * p * rad * rad, 1)} m²."], [f"{Rd(16 * p * rad * rad, 1)} m²", f"{Rd(p * rad * rad, 1)} m²", f"{Rd(4 / 3 * p * rad ** 3, 1)} m²"],
             AP(f"4*{pv}*{rad}^2", 1), why=["Used the diameter as the radius", "Forgot the 4", "Found the volume"])


@fam("12")
def s6_cone(r, L):
    rad, l = r.randint(2, 10), r.randint(5, 18)
    need(l > rad)
    pv, pt_ = PI(L)
    p = math.pi if L == 2 else 3.14
    sa = p * rad * rad + p * rad * l
    return Q(f"Find the surface area of a cone with radius {rad} in. and slant height {l} in. Use {pt_} and round to the nearest tenth.", f"{Rd(sa, 1)} in²",
             ["SA = πr² + πrl.", f"= {pv}({rad})² + {pv}({rad})({l}).", f"≈ {Rd(sa, 1)} in²."], [f"{Rd(p * rad * l, 1)} in²", f"{Rd(2 * p * rad * rad + 2 * p * rad * l, 1)} in²", f"{Rd(p * rad * rad * l / 3, 1)} in²"],
             AP(f"{pv}*{rad}^2 + {pv}*{rad}*{l}", 1), why=["Left out the base", "Used the cylinder formula", "Found the volume"])


# ============================================================== S7 Volume of Prisms and Cylinders
@fam("012")
def s7_prism(r, L):
    l, w, h = r.randint(2, 15), r.randint(2, 12), r.randint(2, 12)
    if L == 2:
        l = F(2 * l + 1, 2)
    v = F(l) * w * h
    return Q(f"Find the volume of a rectangular prism {D(F(l))} in. long, {w} in. wide, and {h} in. high.", f"{D(v)} in³", ["V = lwh.", f"V = {D(F(l))} × {w} × {h}.", f"V = {D(v)} in³."],
             [f"{D(2 * (F(l) * w + F(l) * h + w * h))} in³", f"{D(F(l) + w + h)} in³", f"{D(F(l) * w)} in³"], V(f"{D(F(l))}*{w}*{h}"),
             why=["Found the surface area", "Added the dimensions", "Found only the base area"], diagram={"alt": f"Rectangular prism {D(F(l))} by {w} by {h}.", "draw": box3d_draw(D(F(l)), w, h)} if L == 1 else None)


@fam("012")
def s7_cylinder(r, L):
    rad, h = r.randint(2, 10), r.randint(2, 15)
    if L == 0:
        return Q(f"Find the volume of a cylinder with radius {rad} ft and height {h} ft. Write the answer in terms of π.", f"{rad * rad * h}π ft³", ["V = πr²h.", f"V = π({rad})²({h}).", f"V = {rad * rad * h}π ft³."],
                 [f"{2 * rad * h}π ft³", f"{4 * rad * rad * h}π ft³", f"{rad * h}π ft³"], PY("pi_coef", k=rad * rad * h), why=["Multiplied the radius by 2 instead of squaring", "Used the diameter as the radius", "Did not square the radius"])
    pv, pt_ = PI(L)
    p = math.pi if L == 2 else 3.14
    return Q(f"A can has diameter {2 * rad} cm and height {h} cm. Find its volume. Use {pt_} and round to the nearest tenth.", f"{Rd(p * rad * rad * h, 1)} cm³",
             [f"r = {2 * rad} ÷ 2 = {rad}.", "V = πr²h.", f"V = {pv}({rad})²({h}) ≈ {Rd(p * rad * rad * h, 1)} cm³."],
             [f"{Rd(p * 4 * rad * rad * h, 1)} cm³", f"{Rd(2 * p * rad * h, 1)} cm³", f"{Rd(p * rad * rad * h / 3, 1)} cm³"],
             AP(f"{pv}*{rad}^2*{h}", 1), why=["Used the diameter as the radius", "Used the lateral area formula", "Used the cone formula"], tags=["modeling"])


@fam("12")
def s7_missing(r, L):
    l, w, h = r.randint(2, 15), r.randint(2, 12), r.randint(2, 12)
    v = l * w * h
    return Q(f"A rectangular prism has volume {v} m³, length {l} m, and width {w} m. Find its height.", f"{h} meters", [f"V = lwh: {v} = {l} × {w} × h.", f"{v} = {l * w}h.", f"h = {v} ÷ {l * w} = {h} meters."],
             [f"{v - l - w} meters", f"{N(F(v, l + w))} meters", f"{v * l * w} meters"], EQ(f"{v} = {l}*{w}*h", "h"), why=["Subtracted instead of dividing", "Added the dimensions", "Multiplied instead of dividing"])


# ============================================================== S8 Volume of Pyramids, Cones, Spheres
@fam("012")
def s8_pyramid(r, L):
    s, h = r.randint(2, 12), r.randint(3, 15)
    v = F(s * s * h, 3)
    return Q(f"Find the volume of a square pyramid with base edge {s} cm and height {h} cm.", f"{mixed(v)} cm³" if v.denominator > 1 else f"{N(v)} cm³",
             ["V = (1/3)Bh.", f"B = {s}² = {s * s}.", f"V = (1/3)({s * s})({h}) = {mixed(v)} cm³."], [f"{s * s * h} cm³", f"{mixed(F(s * h, 3))} cm³", f"{mixed(F(s * s * h, 2))} cm³"],
             V(f"1/3*{s}^2*{h}"), why=["Forgot the 1/3", "Did not square the base edge", "Used 1/2 instead of 1/3"])


@fam("012")
def s8_cone(r, L):
    rad, h = r.randint(2, 10), r.randint(3, 15)
    if L == 0:
        need((rad * rad * h) % 3 == 0)
        return Q(f"Find the volume of a cone with radius {rad} in. and height {h} in. Write the answer in terms of π.", f"{rad * rad * h // 3}π in³", ["V = (1/3)πr²h.", f"V = (1/3)π({rad})²({h}).", f"V = {rad * rad * h // 3}π in³."],
                 [f"{rad * rad * h}π in³", f"{N(F(2 * rad * h, 3))}π in³" if (2 * rad * h) % 3 == 0 else f"{2 * rad * h}π in³", f"{N(F(rad * rad * h, 2))}π in³" if rad * rad * h % 2 == 0 else f"{rad * rad * h * 3}π in³"],
                 PY("pi_coef", k=rad * rad * h // 3), why=["Forgot the 1/3", "Did not square the radius", "Used 1/2 instead of 1/3"])
    pv, pt_ = PI(L)
    p = math.pi if L == 2 else 3.14
    v = p * rad * rad * h / 3
    return Q(f"Find the volume of a cone with radius {rad} m and height {h} m. Use {pt_} and round to the nearest tenth.", f"{Rd(v, 1)} m³", ["V = (1/3)πr²h.", f"= (1/3)({pv})({rad})²({h}).", f"≈ {Rd(v, 1)} m³."],
             [f"{Rd(3 * v, 1)} m³", f"{Rd(p * rad * h / 3 * 2, 1)} m³", f"{Rd(v * 4, 1)} m³"], AP(f"1/3*{pv}*{rad}^2*{h}", 1),
             why=["Forgot the 1/3", "Did not square the radius", "Used the diameter as the radius"], diagram={"alt": f"Cone with radius {rad} and height {h}.", "draw": cyl_draw(str(rad), str(h), "cone")} if L == 1 else None)


@fam("012")
def s8_sphere(r, L):
    rad = pick(r, [3, 6, 9, 12]) if L == 0 else r.randint(2, 12)
    if L == 0:
        return Q(f"Find the volume of a sphere with radius {rad} cm. Write the answer in terms of π.", f"{4 * rad ** 3 // 3}π cm³", ["V = (4/3)πr³.", f"V = (4/3)π({rad})³ = (4/3)π({rad ** 3}).", f"V = {4 * rad ** 3 // 3}π cm³."],
                 [f"{4 * rad * rad}π cm³", f"{rad ** 3}π cm³", f"{4 * rad ** 3}π cm³"], PY("pi_coef", k=4 * rad ** 3 // 3),
                 why=["Found the surface area", "Forgot the 4/3", "Forgot to divide by 3"])
    pv, pt_ = PI(L)
    p = math.pi if L == 2 else 3.14
    v = 4 * p * rad ** 3 / 3
    return Q(f"Find the volume of a ball with radius {rad} in. Use {pt_} and round to the nearest tenth.", f"{Rd(v, 1)} in³", ["V = (4/3)πr³.", f"= (4/3)({pv})({rad})³.", f"≈ {Rd(v, 1)} in³."],
             [f"{Rd(4 * p * rad * rad, 1)} in³", f"{Rd(p * rad ** 3, 1)} in³", f"{Rd(4 * p * 8 * rad ** 3 / 3, 1)} in³"], AP(f"4/3*{pv}*{rad}^3", 1),
             why=["Found the surface area", "Forgot the 4/3", "Used the diameter as the radius"])


@fam("2", mode="mc")
def s8_compare(r, L):
    rad, h = r.randint(2, 8), r.randint(3, 12)
    opts = [("The cylinder's volume is 3 times the cone's.", True), ("The cone's volume is 3 times the cylinder's.", False), ("They have the same volume.", False), ("The cylinder's volume is 2 times the cone's.", False)]
    r.shuffle(opts)
    return Q(f"A cone and a cylinder both have radius {rad} and height {h}. How do their volumes compare?", "The cylinder's volume is 3 times the cone's.",
             [f"Cylinder: π({rad})²({h}) = {rad * rad * h}π.", f"Cone: (1/3)π({rad})²({h}) = {mixed(F(rad * rad * h, 3))}π.", "The cylinder holds 3 times as much."], options=opts,
             chk=PY("cone_cyl", rad=rad, h=h), mode="mc", tags=["reasoning"])


SKILLS = {
    1: dict(name="Area of Parallelograms", std=["6.G.A.1"], fams=[s1_area, s1_missing], extra=[err_of(s1_area), open_of(s1_missing)]),
    2: dict(name="Area of Triangles and Trapezoids", std=["6.G.A.1"], fams=[s2_triangle, s2_trapezoid, s2_missing], extra=[err_of(s2_trapezoid), open_of(s2_triangle), select_of(s2_triangle)]),
    3: dict(name="Area of Circles", std=["7.G.B.4"], fams=[s3_area, s3_composite, s3_reverse], extra=[err_of(s3_area), open_of(s3_area)]),
    4: dict(name="Space Figures", std=["7.G.A.3", "6.G.A.4"], fams=[s4_count, s4_name, s4_euler], extra=[err_of(s4_count), open_of(s4_count)]),
    5: dict(name="Surface Area of Prisms and Cylinders", std=["7.G.B.6", "6.G.A.4"], fams=[s5_prism, s5_cylinder, s5_tri_prism], extra=[err_of(s5_prism), open_of(s5_prism)]),
    6: dict(name="Surface Area of Pyramids, Cones, and Spheres", std=["7.G.B.6", "G-GMD.A.3"], fams=[s6_pyramid, s6_sphere, s6_cone], extra=[err_of(s6_pyramid), open_of(s6_pyramid)]),
    7: dict(name="Volumes of Prisms and Cylinders", std=["7.G.B.6", "8.G.C.9"], fams=[s7_prism, s7_cylinder, s7_missing], extra=[err_of(s7_prism), open_of(s7_prism), select_of(s7_prism)]),
    8: dict(name="Volume of Pyramids, Cones, and Spheres", std=["8.G.C.9"], fams=[s8_pyramid, s8_cone, s8_sphere, s8_compare], extra=[err_of(s8_pyramid), open_of(s8_pyramid)]),
}
