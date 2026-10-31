from lib import Bank, graph
from mathlite import *
from fill import fill
from geofig import Fig
import math, random

STD = {1: ["G-GPE.B.7", "G-MG.A.1"], 2: ["G-MG.A.1", "G-SRT.C.8"], 3: ["G-MG.A.1"], 4: ["G-GMD.A.1", "G-C.B.5"], 5: ["G-C.B.5", "G-MG.A.1"], 6: ["G-MG.A.1", "G-GMD.B.4"],
       7: ["G-GMD.A.1", "G-GMD.A.3"], 8: ["G-GMD.A.3"], 9: ["G-GMD.A.3", "G-MG.A.1"], 10: ["G-MG.A.1", "G-GMD.A.3"]}
B = Bank("area-surface-area-volume", "asv", STD, course="geometry", prefix="geo")
R = random.Random(1010)
def lv(): return R.choice(["cp2", "cp1", "cp1", "honors"])
NF = [0]
def nm(s): NF[0] += 1; return f"{s}-{NF[0]}"
def pit(v):
    v = F(v)
    if v == 0: return "0"
    if v == 1: return "π"
    if v.denominator == 1: return f"{v.numerator}π"
    return f"{'' if v.numerator == 1 else v.numerator}π/{v.denominator}"
def ap(v, extra=0): return f"{float(v) * math.pi + float(extra):.2f}"
def pia(v, u=""): return f"{pit(v)} ≈ {ap(v)}{(' ' + u) if u else ''}"
U = ["cm", "in.", "ft", "m", "mm", "yd"]
def un(): return R.choice(U)
DV = (math.cos(math.radians(35)) * 0.55, math.sin(math.radians(35)) * 0.55)
def add(p, q, k=1.0): return (p[0] + k * q[0], p[1] + k * q[1])

# ---------- solid drawings (drawn to proportion from the given dimensions) ----------
def box_fig(l, w, h, lab, name, alt):
    s = 4.0 / max(l, w * 0.7, h); L, W, H = l * s, w * s, h * s; d = (DV[0] * W, DV[1] * W)
    fg = Fig(4.0, 3.2); A, B_, C, D = (0, 0), (L, 0), (L, H), (0, H)
    fg.poly([A, B_, C, D]); fg.seg(D, add(D, d)); fg.seg(C, add(C, d)); fg.seg(B_, add(B_, d)); fg.seg(add(D, d), add(C, d)); fg.seg(add(C, d), add(B_, d))
    for e in ((A, add(A, d)), (add(A, d), add(B_, d)), (add(A, d), add(D, d))): fg.seg(*e, ls="--", lw=1.1)
    fg.side(A, B_, lab[0], center=(L / 2, H)); fg.side(B_, add(B_, d), lab[1], center=(0, H)); fg.side(A, D, lab[2], center=(L, H / 2))
    return fg.save(B, nm(name), alt)
def cyl_fig(r, h, lab, name, alt, cone=False, hemi=False, cone_top=None):
    s = 3.0 / max(r * 2, h, 1); R_, H = r * s, h * s; e = 0.28 * R_
    fg = Fig(3.4, 3.6); fg.ellipse((0, 0), R_, e, half="bottom"); fg.ellipse((0, 0), R_, e, ls="--", half="top", lw=1.1)
    if cone:
        fg.seg((-R_, 0), (0, H)); fg.seg((R_, 0), (0, H)); fg.seg((0, 0), (0, H), ls="--", lw=1.1); fg.seg((0, 0), (R_, 0), lw=1.1)
        fg.angle((0, 0), (0, H), (R_, 0), right=True, r=0.25); fg.side((0, 0), (R_, 0), lab[0], center=(0, H)); fg.side((0, 0), (0, H), lab[1], center=(R_, 0), dist=12)
        if len(lab) > 2 and lab[2]: fg.side((R_, 0), (0, H), lab[2], center=(-R_, 0))
    else:
        fg.ellipse((0, H), R_, e); fg.seg((-R_, 0), (-R_, H)); fg.seg((R_, 0), (R_, H)); fg.seg((0, H), (R_, H), lw=1.1); fg.dot((0, H)); fg.side((0, H), (R_, H), lab[0], center=(0, 0)); fg.side((R_, 0), (R_, H), lab[1], center=(0, H / 2))
        if hemi:
            t = [math.radians(v) for v in range(0, 181, 4)]; fg.ax.plot([R_ * math.cos(v) for v in t], [H + R_ * math.sin(v) for v in t], color="black", lw=1.6); fg.pts.append((0, H + R_))
        if cone_top:
            ch = cone_top * s; fg.seg((-R_, H), (0, H + ch)); fg.seg((R_, H), (0, H + ch)); fg.seg((0, H), (0, H + ch), ls="--", lw=1.1); fg.side((0, H), (0, H + ch), lab[2], center=(R_, H), dist=12)
    return fg.save(B, nm(name), alt)
def sphere_fig(r, lab, name, alt, hemi=False):
    fg = Fig(3.2, 3.2 if not hemi else 2.4); t = [math.radians(v) for v in range(0, 361 if not hemi else 181, 3)]
    fg.ax.plot([3 * math.cos(v) for v in t], [3 * math.sin(v) for v in t], color="black", lw=1.6); fg.pts += [(-3, -3 if not hemi else -1), (3, 3)]
    fg.ellipse((0, 0), 3, 0.8, half="bottom"); fg.ellipse((0, 0), 3, 0.8, ls="--" if not hemi else "-", half="top", lw=1.1)
    fg.dot((0, 0)); fg.seg((0, 0), (3, 0), lw=1.1); fg.side((0, 0), (3, 0), lab, center=(0, -2) if hemi else (0, 3))
    return fg.save(B, nm(name), alt)
def pyr_fig(b, h, lab, name, alt, slant=None):
    s = 3.6 / max(b, h); Bb, H = b * s, h * s; d = (DV[0] * Bb, DV[1] * Bb)
    A, B_, C, D = (0, 0), (Bb, 0), add((Bb, 0), d), add((0, 0), d); M = add((Bb / 2, 0), d, 0.5); T = (M[0], M[1] + H)
    fg = Fig(3.6, 3.6); fg.seg(A, B_); fg.seg(B_, C); fg.seg(A, T); fg.seg(B_, T); fg.seg(C, T)
    for e in ((A, D), (D, C), (D, T)): fg.seg(*e, ls="--", lw=1.1)
    fg.seg(M, T, ls="--", lw=1.1); fg.dot(M); fg.side(A, B_, lab[0], center=T); fg.text(add(M, (0, H * 0.4)), lab[1], off=(18, 0), size=10)
    if slant:
        mid = ((A[0] + B_[0]) / 2, 0); fg.seg(mid, T, ls=":", lw=1.1); fg.side(mid, T, slant, center=B_, dist=11)
    return fg.save(B, nm(name), alt)
def triprism_fig(a, b, L, lab, name, alt):
    s = 3.6 / max(a, b, L * 0.6); A_, B_ = a * s, b * s; d = (DV[0] * L * s, DV[1] * L * s)
    P0, P1, P2 = (0, 0), (A_, 0), (0, B_); fg = Fig(4.0, 3.2)
    fg.poly([P0, P1, P2]); fg.seg(P1, add(P1, d)); fg.seg(P2, add(P2, d)); fg.seg(add(P1, d), add(P2, d)); fg.seg(P0, add(P0, d), ls="--", lw=1.1); fg.seg(add(P0, d), add(P1, d), ls="--", lw=1.1); fg.seg(add(P0, d), add(P2, d), ls="--", lw=1.1)
    fg.angle(P0, P1, P2, right=True, r=0.35); fg.side(P0, P1, lab[0], center=P2); fg.side(P0, P2, lab[1], center=P1); fg.side(P1, add(P1, d), lab[2], center=P2)
    return fg.save(B, nm(name), alt)

# =============== Skill 1: perimeter and area of polygons ===============
def mk_rect():
    l, w = R.randint(3, 25), R.randint(2, 18); u = un(); k = R.random()
    if l == w: raise ValueError
    if k < 0.35:
        B.mc(1, lv(), f"A rectangle is {l} {u} by {w} {u}. Find its area.", f"{l * w} {u}²", [f"{2 * (l + w)} {u}²", f"{l + w} {u}²", f"{l * w * 2} {u}²"], ["A = lw."], tags=["misconception"])
    elif k < 0.65:
        B.sa(1, lv(), f"A rectangle has area {l * w} {u}² and length {l} {u}. Find its perimeter.", f"{2 * (l + w)} {u}", [f"w = {l * w} ÷ {l} = {w}.", f"P = 2({l} + {w})."])
    else:
        d = R.randint(1, 9); w2 = R.randint(3, 15); P_ = 2 * (2 * w2 + d)
        B.orq(1, lv(), f"A rectangle's length is {d} {u} more than its width, and its perimeter is {P_} {u}.", [("Write an equation.", f"2w + 2(w + {d}) = {P_}"), ("Find the width.", f"{w2} {u}"), ("Find the length.", f"{w2 + d} {u}"), ("Find the area.", f"{w2 * (w2 + d)} {u}²")], ["P = 2l + 2w.", "Solve.", "w + d.", "A = lw."])
def mk_para():
    h, o, s_ = R.choice([(3, 4, 5), (4, 3, 5), (12, 5, 13), (5, 12, 13), (8, 6, 10), (6, 8, 10), (15, 8, 17), (8, 15, 17)]); b = R.randint(o + 2, o + 14); u = un()
    s = 3.6 / (b + o); P0, P1, P2, P3 = (0, 0), (b * s, 0), ((b + o) * s, h * s), (o * s, h * s); fg = Fig(4.2, 2.8); fg.poly([P0, P1, P2, P3])
    Hf = (o * s, 0); fg.seg(P3, Hf, ls="--", lw=1.1); fg.angle(Hf, P1, P3, right=True, r=0.3)
    fg.side(P0, P1, f"{b} {u}", center=P2); fg.side(P0, P3, f"{s_} {u}", center=P1); fg.text(((o * s), h * s / 2), f"{h} {u}", off=(14, 0), size=9.5)
    d_ = fg.save(B, nm("para"), f"Parallelogram with base {b} {u}, slanted side {s_} {u}, and dashed height {h} {u}.")
    if R.random() < 0.5:
        B.mc(1, lv(), "Find the area of the parallelogram.", f"{b * h} {u}²", [f"{b * s_} {u}²", f"{fr(F(b * h, 2))} {u}²", f"{2 * (b + s_)} {u}²"], ["A = base × height (the perpendicular height, not the slanted side)."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(1, lv(), "Use the parallelogram.", [("Find the area.", f"{b * h} {u}²"), ("Find the perimeter.", f"{2 * (b + s_)} {u}"), ("Which length is NOT used for the area?", f"the slanted side, {s_} {u}"), ("If the slanted side were the base, what height would give the same area?", f"{fr(F(b * h, s_))} {u}")], ["bh.", "2(b + side).", "Height must be perpendicular to the base.", f"{b * h} ÷ {s_}."], diagram=d_, tags=["diagram"])
def shoelace(P_): return F(abs(sum(P_[i][0] * P_[(i + 1) % len(P_)][1] - P_[(i + 1) % len(P_)][0] * P_[i][1] for i in range(len(P_)))), 2)
def mk_coord_poly():
    n = R.choice([3, 4, 4, 5]);
    while True:
        P_ = [(R.randint(-6, 6), R.randint(-6, 6)) for _ in range(n)]; c = (sum(p[0] for p in P_) / n, sum(p[1] for p in P_) / n)
        P_.sort(key=lambda p: math.atan2(p[1] - c[1], p[0] - c[0]))
        if len(set(P_)) == n and shoelace(P_) >= 8 and all(abs((P_[(i + 1) % n][0] - P_[i][0]) * (P_[(i + 2) % n][1] - P_[i][1]) - (P_[(i + 2) % n][0] - P_[i][0]) * (P_[(i + 1) % n][1] - P_[i][1])) > 0 for i in range(n)): break
    A_ = shoelace(P_); L = "ABCDE"[:n]
    d_ = graph(B, nm("cpoly"), [(("seg", [p[0] for p in P_ + [P_[0]]], [p[1] for p in P_ + [P_[0]]]), {})], xr=(-7, 7), yr=(-7, 7), points=[(p[0], p[1], True, l) for p, l in zip(P_, L)], alt=f"Polygon {L} with vertices " + ", ".join(f"{l}{pt(*p)}" for p, l in zip(P_, L)) + ".")
    B.sa(1, R.choice(["cp1", "honors"]), f"Find the area of polygon {L} shown on the grid.", f"{fr(A_)} square units", ["Enclose the polygon in a rectangle and subtract the right triangles outside it (or use the shoelace formula).", f"Area = {fr(A_)}."], diagram=d_, tags=["graph"])
def mk_rect_sel():
    A_ = R.choice([24, 36, 48, 60, 72, 30, 40]); good = [(a, A_ // a) for a in range(1, int(A_ ** 0.5) + 1) if A_ % a == 0 and a > 1]
    if len(good) < 2: raise ValueError
    gs = R.sample(good, 2); bad = [(gs[0][0] + 1, gs[0][1]), (gs[1][0], gs[1][1] - 1), (2, A_ // 4)]
    bad = [b for b in bad if b[0] * b[1] != A_]
    st = [f"{a} by {b}" for a, b in gs]; perims = {f"{a} by {b}": 2 * (a + b) for a, b in gs}
    B.sel(1, lv(), f"Select ALL rectangles with area {A_} square units.", st, [f"{a} by {b}" for a, b in bad], ["Multiply length × width.", "Different rectangles can share an area but have different perimeters: " + ", ".join(f"{k}: P = {v}" for k, v in perims.items()) + "."], tags=["concept"])
def mk_sq_diag():
    d = R.randint(2, 20); A_ = F(d * d, 2)
    B.sa(1, "honors", f"A square has a diagonal of length {d}. Find its area and its side length.", f"area {fr(A_)}; side {rad(A_) if A_.denominator == 1 else rad(2 * d * d, F(1, 2))}", ["Side = d/√2, so area = d²/2.", "Side = √(area)."], tags=["challenge"])

# =============== Skill 2: triangles, trapezoids, regular polygons ===============
def mk_tri():
    b, h = R.randint(3, 20), R.randint(2, 16); u = un(); obt = R.random() < 0.4; k = R.random()
    s = 3.6 / max(b + (3 if obt else 0), h); top = ((b + R.randint(1, 3)) * s, h * s) if obt else (R.uniform(0.2, 0.8) * b * s, h * s)
    fg = Fig(4.0, 3.0); fg.poly([(0, 0), (b * s, 0), top]); foot = (top[0], 0)
    if obt: fg.seg((b * s, 0), foot, ls="--", lw=1.1)
    fg.seg(top, foot, ls="--", lw=1.1); fg.angle(foot, (0, 0) if obt else (b * s, 0), top, right=True, r=0.3)
    fg.side((0, 0), (b * s, 0), f"{b} {u}", center=top); fg.text((top[0], top[1] / 2), f"{h} {u}", off=(15, 0), size=9.5)
    d_ = fg.save(B, nm("tri"), f"Triangle with base {b} {u} and {'height drawn outside the triangle to the extended base' if obt else 'dashed height'} {h} {u}.")
    A_ = F(b * h, 2)
    if k < 0.6:
        B.mc(2, lv(), "Find the area of the triangle.", f"{fr(A_)} {u}²", [f"{b * h} {u}²", f"{b + h} {u}²", f"{fr(A_ / 2)} {u}²"], ["A = ½bh." + (" The height of an obtuse triangle may fall outside it." if obt else "")], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.sa(2, lv(), f"A triangle has area {fr(A_)} {u}² and base {b} {u}. Find its height.", f"{h} {u}", [f"½·{b}·h = {fr(A_)} → h = {h}."])
def mk_trap():
    b1, b2, h = R.randint(3, 14), R.randint(5, 22), R.randint(2, 12); u = un()
    if b1 >= b2: raise ValueError
    s = 3.6 / max(b2, h); off = (b2 - b1) * s * R.uniform(0.2, 0.8); P_ = [(0, 0), (b2 * s, 0), (off + b1 * s, h * s), (off, h * s)]
    fg = Fig(4.0, 2.8); fg.poly(P_); fg.seg((off, h * s), (off, 0), ls="--", lw=1.1); fg.angle((off, 0), (b2 * s, 0), (off, h * s), right=True, r=0.3)
    fg.side(P_[0], P_[1], f"{b2} {u}", center=P_[2]); fg.side(P_[2], P_[3], f"{b1} {u}", center=P_[0]); fg.text((off, h * s / 2), f"{h} {u}", off=(-14, 0), size=9.5)
    d_ = fg.save(B, nm("trap"), f"Trapezoid with bases {b1} {u} and {b2} {u} and height {h} {u}.")
    A_ = F((b1 + b2) * h, 2)
    if R.random() < 0.5:
        B.mc(2, lv(), "Find the area of the trapezoid.", f"{fr(A_)} {u}²", [f"{(b1 + b2) * h} {u}²", f"{b2 * h} {u}²", f"{fr(F(b1 + b2, 2) + h)} {u}²"], ["A = ½(b₁ + b₂)h."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(2, lv(), "Use the trapezoid.", [("Find the midsegment length.", f"{fr(F(b1 + b2, 2))} {u}"), ("Find the area.", f"{fr(A_)} {u}²"), ("Explain the formula using two copies of the trapezoid.", f"Two copies form a parallelogram with base {b1 + b2} and height {h}; the trapezoid is half of it"), (f"If the area stayed {fr(A_)} {u}² but the height doubled, what would the sum of the bases be?", f"{fr(F(b1 + b2, 2))} {u}")], ["½(b₁ + b₂).", "midsegment × h.", "Rotate a copy 180°.", "A = ½(sum)(2h)."], diagram=d_, tags=["diagram", "reasoning"])
def mk_equil():
    s_ = R.randint(2, 16); A_ = F(s_ * s_, 4)
    B.mc(2, lv(), f"Find the exact area of an equilateral triangle with side {s_}.", rad(3, A_), [rad(3, F(s_ * s_, 2)), fr(F(s_ * s_, 2)), rad(3, F(s_, 2))], ["Height = (s√3)/2.", "A = ½ · s · (s√3)/2 = (s²√3)/4."], tags=["misconception"])
def mk_regpoly():
    k = R.random()
    if k < 0.35:
        s_ = R.randint(2, 12); A_ = F(3 * s_ * s_, 2); a_ = rad(3, F(s_, 2))
        B.orq(2, lv(), f"A regular hexagon has side length {s_}.", [("Find the perimeter.", str(6 * s_)), ("Find the apothem.", a_), ("Find the area using A = ½aP.", rad(3, A_)), ("Check: how many equilateral triangles make up the hexagon?", f"6, each with area {rad(3, F(s_ * s_, 4))}")], ["6s.", "Apothem = height of an equilateral triangle: (s√3)/2.", "½ · apothem · perimeter.", "Six congruent equilateral triangles."], tags=["reasoning"])
    elif k < 0.7:
        n = R.choice([5, 6, 8, 9, 10, 12]); s_ = R.randint(2, 12); a_ = s_ / (2 * math.tan(math.pi / n)); A_ = 0.5 * a_ * n * s_
        name = {5: "pentagon", 6: "hexagon", 8: "octagon", 9: "nonagon", 10: "decagon", 12: "dodecagon"}[n]
        B.orq(2, "honors", f"A regular {name} has side length {s_}.", [("Find the central angle.", f"{fr(F(360, n))}°"), ("Find the apothem to the nearest hundredth.", f"{a_:.2f}"), ("Find the perimeter.", str(n * s_)), ("Find the area to the nearest tenth.", f"{A_:.1f}")], [f"360° ÷ {n}.", f"tan({fr(F(180, n))}°) = ({fr(F(s_, 2))})/a.", f"{n} × {s_}.", "½aP."], tags=["challenge"])
    else:
        n = R.choice([5, 6, 8, 10]); s_ = R.randint(3, 15); a_ = R.randint(2, 20); A_ = F(a_ * n * s_, 2)
        B.sa(2, lv(), f"A regular polygon with {n} sides has side length {s_} and apothem {a_} (values given for practice). Find its area using A = ½aP.", fr(A_), [f"P = {n} · {s_} = {n * s_}.", f"A = ½ · {a_} · {n * s_} = {fr(A_)}."])
def mk_kite():
    d1, d2 = R.randint(4, 24), R.randint(4, 24); shp = R.choice(["rhombus", "kite"])
    if shp == "rhombus" and (d1 % 2 or d2 % 2): raise ValueError
    B.mc(2, lv(), f"A {shp} has diagonals of lengths {d1} and {d2}. Find its area.", fr(F(d1 * d2, 2)), [str(d1 * d2), str(2 * (d1 + d2)), fr(F(d1 * d2, 4))], ["Diagonals are perpendicular: A = ½d₁d₂."], tags=["misconception"])
def mk_area_sel():
    b, h = R.randint(4, 14), R.randint(3, 12)
    st = {f"A triangle with base {b} and height {h} has area {fr(F(b * h, 2))}": True, f"A parallelogram with base {b} and height {h} has area {b * h}": True, f"A trapezoid with bases {b} and {b + 2} and height {h} has area {(b + 1) * h}": True, f"A triangle with base {b} and height {h} has area {b * h}": False, f"A rhombus with diagonals {b} and {h} has area {b * h}": False}
    B.sel(2, lv(), f"Select ALL true statements (base {b}, height {h}).", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Triangle ½bh; parallelogram bh; trapezoid ½(b₁ + b₂)h; rhombus ½d₁d₂."], tags=["concept"])

# =============== Skill 3: composite figures ===============
def mk_L():
    W, H = R.randint(8, 20), R.randint(8, 18); w, h = R.randint(2, W - 3), R.randint(2, H - 3); u = un()
    s = 3.6 / max(W, H); P_ = [(0, 0), (W * s, 0), (W * s, (H - h) * s), ((W - w) * s, (H - h) * s), ((W - w) * s, H * s), (0, H * s)]
    fg = Fig(3.8, 3.6); fg.poly(P_, fill="#dddddd"); c = (W * s / 3, H * s / 3)
    fg.side(P_[0], P_[1], f"{W}", center=c); fg.side(P_[5], P_[0], f"{H}", center=(W * s, 0)); fg.side(P_[3], P_[4], f"{h}", center=(W * s, H * s)); fg.side(P_[2], P_[3], f"{w}", center=(W * s, H * s))
    d_ = fg.save(B, nm("L"), f"L-shaped figure ({u}): bottom {W}, left side {H}; a {w}-by-{h} rectangle is missing from the upper right corner.")
    A_ = W * H - w * h; Per = 2 * (W + H)
    if R.random() < 0.5:
        B.orq(3, lv(), f"The shaded L-shape is measured in {u}.", [("Find the area by subtraction.", f"{W}·{H} − {w}·{h} = {A_} {u}²"), ("Find the area by splitting into two rectangles.", f"{W}·{H - h} + {W - w}·{h} = {A_} {u}²"), ("Find the perimeter.", f"{Per} {u}"), ("Why does the perimeter equal that of the full rectangle?", "The notch's two inner edges replace the two removed outer edges of equal total length")], ["Big rectangle − missing rectangle.", "Add the parts.", "Add all six sides.", "Lengths shift but don't change."], diagram=d_, tags=["diagram", "reasoning"])
    else:
        B.sel(3, lv(), f"Select ALL expressions equal to the shaded area (in {u}²).", [f"{W}·{H} − {w}·{h}", f"{W}·{H - h} + {W - w}·{h}", f"{W - w}·{H} + {w}·{H - h}"], [f"{W}·{H} + {w}·{h}", f"{W}·{H - h} + {W}·{h}"], ["Subtract the notch or split the L into two non-overlapping rectangles."], diagram=d_, tags=["diagram", "concept"])
def mk_semi_rect():
    l, w = R.randint(6, 20), R.randrange(4, 16, 2); r = F(w, 2); u = un()
    s = 3.4 / (l + w / 2); fg = Fig(4.2, 2.6); fg.poly([(0, 0), (l * s, 0), (l * s, w * s), (0, w * s)])
    t = [math.radians(v) for v in range(-90, 91, 3)]; fg.ax.plot([l * s + r * s * math.cos(v) for v in t], [w * s / 2 + r * s * math.sin(v) for v in t], color="black", lw=1.6); fg.pts.append((l * s + r * s, w * s / 2))
    fg.seg((l * s, 0), (l * s, w * s), ls="--", lw=1.0); fg.side((0, 0), (l * s, 0), f"{l} {u}", center=(0, w * s)); fg.side((0, 0), (0, w * s), f"{w} {u}", center=(l * s, 0))
    d_ = fg.save(B, nm("semirect"), f"Figure made of a {l}-by-{w} {u} rectangle with a semicircle of diameter {w} {u} on its right side.")
    Ar = l * w; As = r * r / 2; arc = r
    B.orq(3, lv(), "The figure is a rectangle with a semicircle on one end.", [("Find the area of the rectangle.", f"{Ar} {u}²"), ("Find the area of the semicircle.", f"{pia(As)} {u}²"), ("Find the total area.", f"{Ar} + {pit(As)} ≈ {ap(As, Ar)} {u}²"), ("Find the perimeter of the figure.", f"{2 * l + w} + {pit(arc)} ≈ {ap(arc, 2 * l + w)} {u}")], ["lw.", "½πr² with r = d/2.", "Add.", "Three sides of the rectangle plus half the circumference (the dashed side is inside)."], diagram=d_, tags=["diagram"])
def mk_shaded():
    k = R.random()
    if k < 0.35:
        s_ = R.randrange(4, 24, 2); r = F(s_, 2)
        B.sa(3, lv(), f"A circle is inscribed in a square with side {s_}. Find the exact area of the region inside the square but outside the circle.", f"{s_ * s_} − {pit(r * r)} ≈ {s_ * s_ - float(r * r) * math.pi:.2f}", ["Square − circle; the circle's diameter equals the side.", f"{s_}² − π({fr(r)})²."])
    elif k < 0.7:
        R1, r1 = sorted(R.sample(range(2, 15), 2), reverse=True)
        fg = Fig(3.2, 3.2); t = [math.radians(v) for v in range(0, 361, 3)]
        fg.ax.fill([R1 * math.cos(v) for v in t] + [r1 * math.cos(v) for v in reversed(t)], [R1 * math.sin(v) for v in t] + [r1 * math.sin(v) for v in reversed(t)], color="#dddddd", lw=0)
        fg.circle((0, 0), R1); fg.circle((0, 0), r1); fg.dot((0, 0)); fg.seg((0, 0), (R1 * 0.7071, R1 * 0.7071), lw=1.1); fg.seg((0, 0), (-r1, 0), lw=1.1)
        fg.text((R1 * 0.35, R1 * 0.35), str(R1), off=(-8, 8), size=9.5); fg.text((-r1 / 2, 0), str(r1), off=(0, 8), size=9.5)
        d_ = fg.save(B, nm("ring"), f"Two concentric circles with radii {R1} and {r1}; the ring between them is shaded.")
        B.mc(3, lv(), "Find the area of the shaded ring.", pia(R1 * R1 - r1 * r1), [pia((R1 - r1) ** 2), pia(2 * (R1 - r1)), pia(R1 * R1 + r1 * r1)], ["π(R² − r²) — not π(R − r)²."], diagram=d_, tags=["diagram", "misconception"])
    else:
        l, w = R.randint(8, 20), R.randint(6, 14); b, h = R.randint(2, l - 2), R.randint(2, w - 1)
        B.sa(3, lv(), f"A {l}-by-{w} rectangular garden has a triangular patio with base {b} and height {h} inside it. Find the area of the garden not covered by the patio.", fr(l * w - F(b * h, 2)), [f"{l}·{w} − ½·{b}·{h}."], tags=["application"])
def mk_comp_app():
    n = R.randint(2, 4); r = R.randint(2, 6); s_ = 2 * r * n
    B.orq(3, "honors", f"{n} congruent circles of radius {r} fit side by side inside a rectangle measuring {s_} by {2 * r}, each touching the rectangle and its neighbors.", [("Find the rectangle's area.", str(s_ * 2 * r)), ("Find the total area of the circles.", pit(n * r * r)), ("Find the area of the rectangle not covered by circles.", f"{s_ * 2 * r} − {pit(n * r * r)} ≈ {s_ * 2 * r - n * r * r * math.pi:.2f}"), ("What percent of the rectangle is covered?", f"{100 * math.pi / 4:.1f}% (π/4, for any n and r)")], ["length × width.", f"{n}πr².", "Subtract.", f"{pit(n * r * r)} ÷ {s_ * 2 * r} = π/4."], tags=["challenge"])

# =============== Skill 4: circumference and area of circles ===============
def mk_circ():
    r = R.randint(1, 20); u = un(); k = R.random(); usediam = R.random() < 0.4; given = f"diameter {2 * r} {u}" if usediam else f"radius {r} {u}"
    if k < 0.35:
        B.mc(4, lv(), f"A circle has {given}. Find its area.", f"{pia(r * r)} {u}²", [f"{pia(2 * r)} {u}²", f"{pia(4 * r * r)} {u}²", f"{pia(r)} {u}²" if r != 1 else f"{pia(8)} {u}²"], ["A = πr²." + (" Use r = d/2." if usediam else "")], tags=["misconception"])
    elif k < 0.6:
        B.mc(4, lv(), f"A circle has {given}. Find its circumference.", f"{pia(2 * r)} {u}", [f"{pia(r * r)} {u}" if r != 2 else f"{pia(8)} {u}", f"{pia(r)} {u}", f"{pia(4 * r)} {u}"], ["C = 2πr = πd."], tags=["misconception"])
    else:
        B.orq(4, lv(), f"A circle has circumference {pit(2 * r)} {u}.", [("Find the diameter.", f"{2 * r} {u}"), ("Find the radius.", f"{r} {u}"), ("Find the area.", f"{pia(r * r)} {u}²"), ("Write the area in terms of C.", "A = C²/(4π)")], ["C = πd.", "d/2.", "πr².", "r = C/(2π)."])
def mk_circ_rev():
    r = R.randint(2, 20); k = R.random()
    if k < 0.5: B.sa(4, lv(), f"A circle has area {pit(r * r)} square units. Find its circumference.", pit(2 * r), [f"r² = {r * r} → r = {r}.", f"C = 2π({r})."])
    else:
        d = R.randint(14, 30); n = R.randint(10, 500)
        B.sa(4, lv(), f"A bicycle wheel has diameter {d} in. How far does the bike travel (in feet) when the wheel turns {n} times? Round to the nearest foot.", f"{round(d * math.pi * n / 12)} ft", [f"One turn = πd = {d}π in.", f"{n} turns = {n * d}π in. ≈ {d * math.pi * n:.1f} in. ÷ 12."], tags=["application"])
def mk_circ_sel():
    r = R.randint(2, 12)
    st = {f"C = {pit(2 * r)}": True, f"A = {pit(r * r)}": True, f"d = {2 * r}": True, f"A = {pit(2 * r)}": r == 2, "Doubling r doubles the area": False, "Doubling r doubles the circumference": True}
    B.sel(4, lv(), f"A circle has radius {r}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["C = 2πr; A = πr²; area scales by the square of the radius."], tags=["concept"])
def mk_circ_derive():
    n = R.choice([8, 12, 16, 24])
    B.mc(4, "honors", f"A circle of radius r is cut into {n} equal sectors that are rearranged into a shape close to a parallelogram. What are the approximate base and height of that shape?", "base πr (half the circumference), height r", ["base 2πr, height r", "base πr, height 2r", "base r, height πr²"], ["Half of the arcs form each long side: πr.", "The height is a radius, so A ≈ πr · r = πr²."], tags=["reasoning"])

# =============== Skill 5: arc length and sector area applications ===============
def mk_pizza():
    d = R.choice([10, 12, 14, 16, 18, 20]); n = R.choice([6, 8, 10, 12]); r = F(d, 2)
    B.orq(5, lv(), f"A {d}-inch pizza is cut into {n} equal slices.", [("Find the central angle of each slice.", f"{fr(F(360, n))}°"), ("Find the area of one slice.", f"{pia(r * r / n)} in.²"), ("Find the length of crust on one slice.", f"{pia(2 * r / n)} in."), ("Find the perimeter of one slice.", f"{d} + {pit(2 * r / n)} ≈ {ap(2 * r / n, d)} in.")], ["360° ÷ n.", "πr² ÷ n.", "2πr ÷ n.", "Two radii + crust."], tags=["application"])
def mk_sprinkler():
    r = R.randint(5, 30); th = R.choice([45, 60, 90, 120, 135, 150, 180, 210, 240, 270]); A_ = F(th * r * r, 360)
    if R.random() < 0.6:
        B.sa(5, lv(), f"A lawn sprinkler sprays {r} ft and rotates through {th}°. What area does it water?", f"{pia(A_)} ft²", [f"({th}/360)·π·{r}²."], tags=["application"])
    else:
        B.mc(5, lv(), f"A sprinkler sprays {r} ft through {th}°. Which expression gives the length of the outer edge of the wet region?", f"({th}/360)·2π·{r}", [f"({th}/360)·π·{r}²", f"{th}·{r}", f"({th}/180)·π·{r}²"], ["Arc length = (θ/360)·2πr."], tags=["application", "misconception"])
def mk_wiper():
    R1, r1 = R.randint(18, 30), R.randint(4, 10); th = R.choice([90, 100, 110, 120, 135, 150]); A_ = F(th * (R1 * R1 - r1 * r1), 360)
    B.orq(5, "honors", f"A windshield wiper blade runs from {r1} in. to {R1} in. from the pivot and sweeps {th}°.", [("Find the area swept by the outer end's sector.", f"{pia(F(th * R1 * R1, 360))} in.²"), ("Find the inner sector area (not cleaned).", f"{pia(F(th * r1 * r1, 360))} in.²"), ("Find the area cleaned.", f"{pia(A_)} in.²"), ("How far does the blade's tip travel per sweep?", f"{pia(F(th * R1, 180))} in.")], ["(θ/360)πR².", "(θ/360)πr².", "Subtract.", "Arc length."], tags=["application", "challenge"])
def mk_clock():
    r = R.randint(3, 14); t = R.choice([5, 10, 15, 20, 25, 30, 40, 45, 50]); L = F(t * r, 30)
    B.sa(5, lv(), f"The minute hand of a clock is {r} cm long. How far does its tip travel in {t} minutes?", f"{pia(L)} cm", [f"{t} min = {t}/60 of a revolution = {6 * t}°.", f"({t}/60)·2π·{r}."], tags=["application"])
def mk_track():
    l, r = R.randint(50, 120), R.randint(20, 40)
    B.orq(5, lv(), f"A running track has two straight sides of {l} m and two semicircular ends with inner radius {r} m.", [("Find the inner lap distance.", f"{2 * l} + {pit(2 * r)} ≈ {ap(2 * r, 2 * l)} m"), ("A lane is 1 m farther out. Find its lap distance.", f"{2 * l} + {pit(2 * (r + 1))} ≈ {ap(2 * (r + 1), 2 * l)} m"), ("How much longer is the outer lap?", f"{pit(2)} ≈ {ap(2)} m"), ("Find the area enclosed by the inner lap.", f"{2 * r * l} + {pit(r * r)} ≈ {ap(r * r, 2 * r * l)} m²")], ["Two semicircles make one circle.", "Use r + 1.", "2π(r + 1) − 2πr = 2π, independent of r.", "Rectangle + circle."], tags=["application", "reasoning"])
def mk_app_sel():
    r = R.randint(3, 12); th = R.choice([60, 90, 120, 180])
    st = {f"The arc length is {pit(F(th * r, 180))}": True, f"The sector area is {pit(F(th * r * r, 360))}": True, f"The sector is {fr(F(th, 360))} of the circle": True, f"The sector area is {pit(F(th * r, 180))}": F(th * r * r, 360) == F(th * r, 180), f"The arc length is {pit(F(th * r * r, 360))}": F(th * r * r, 360) == F(th * r, 180)}
    if sum(not v for v in st.values()) < 1: raise ValueError
    B.sel(5, lv(), f"A fan blade sweeps a {th}° sector of radius {r} in. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Arc = (θ/360)2πr; area = (θ/360)πr²."], tags=["application", "concept"])

# =============== Skill 6: nets and surface area of prisms and pyramids ===============
def mk_box_sa():
    l, w, h = R.randint(2, 15), R.randint(2, 12), R.randint(2, 14); u = un(); SA = 2 * (l * w + l * h + w * h)
    d_ = box_fig(l, w, h, (f"{l} {u}", f"{w} {u}", f"{h} {u}"), "box", f"Rectangular prism {l} {u} long, {w} {u} deep, {h} {u} high.")
    if R.random() < 0.5:
        B.mc(6, lv(), "Find the surface area of the prism.", f"{SA} {u}²", [f"{l * w * h} {u}²", f"{l * w + l * h + w * h} {u}²", f"{2 * (l + w) * h} {u}²"], ["SA = 2lw + 2lh + 2wh."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(6, lv(), "Use the rectangular prism.", [("How many faces does its net have?", "6"), ("Find the lateral area.", f"{2 * (l + w) * h} {u}²"), ("Find the area of the two bases.", f"{2 * l * w} {u}²"), ("Find the total surface area.", f"{SA} {u}²")], ["Rectangular prism.", "Perimeter of base × height.", "2lw.", "Lateral + bases."], diagram=d_, tags=["diagram"])
def mk_tri_prism():
    a, b, c = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15)]); L = R.randint(3, 20); u = un()
    SA = a * b + (a + b + c) * L
    d_ = triprism_fig(a, b, L, (f"{a}", f"{b}", f"{L}"), "triprism", f"Right triangular prism; the bases are right triangles with legs {a} and {b} {u}; the prism length is {L} {u}.")
    B.orq(6, lv(), f"Measurements are in {u}.", [("Find the hypotenuse of the base.", f"{c} {u}"), ("Find the area of both bases.", f"{a * b} {u}²"), ("Find the lateral area.", f"{(a + b + c) * L} {u}²"), ("Find the surface area.", f"{SA} {u}²")], ["Pythagorean Theorem.", "2 · ½ab.", "Perimeter × length.", "Add."], diagram=d_, tags=["diagram"])
def mk_pyr_sa():
    k_ = R.randint(1, 4); b, h, l = 6 * k_, 4 * k_, 5 * k_
    if R.random() < 0.5: b, h, l = 10 * k_, 12 * k_, 13 * k_
    u = un(); LA = 2 * b * l; SA = b * b + LA
    d_ = pyr_fig(b, h, (f"{b}", f"h = {h}"), "pyr", f"Square pyramid with base edge {b} {u} and height {h} {u}; the slant height is dotted.", slant="ℓ")
    B.orq(6, lv(), f"Square pyramid; measurements in {u}.", [("Find the slant height ℓ.", f"{l} {u}"), ("Find the area of one triangular face.", f"{b * l // 2} {u}²"), ("Find the lateral area.", f"{LA} {u}²"), ("Find the surface area.", f"{SA} {u}²")], [f"ℓ² = h² + ({b // 2})².", "½ · base · ℓ.", "4 faces.", "Add the base."], diagram=d_, tags=["diagram"])
def mk_net_sel():
    k = R.choice(["triprism", "sqpyr", "cube", "hexprism"])
    if k == "triprism": st = {"2 triangles and 3 rectangles": True, "5 faces": True, "9 edges": True, "6 vertices": True, "4 triangles": False, "8 vertices": False}; nmx = "a triangular prism"
    elif k == "sqpyr": st = {"1 square and 4 triangles": True, "5 faces": True, "8 edges": True, "5 vertices": True, "2 squares": False, "6 vertices": False}; nmx = "a square pyramid"
    elif k == "cube": st = {"6 congruent squares": True, "12 edges": True, "8 vertices": True, "6 faces": True, "4 squares and 2 rectangles that are not squares": False, "10 edges": False}; nmx = "a cube"
    else: st = {"2 hexagons and 6 rectangles": True, "8 faces": True, "18 edges": True, "12 vertices": True, "6 faces": False, "2 hexagons and 6 triangles": False}; nmx = "a hexagonal prism"
    B.sel(6, lv(), f"Select ALL true statements about {nmx} and its net.", [x for x, v in st.items() if v], [x for x, v in st.items() if not v], ["Count faces, edges and vertices; Euler: F + V − E = 2."], tags=["concept"])
def mk_cube_net():
    s_ = R.randint(2, 15); k = R.random()
    if k < 0.5:
        B.sa(6, lv(), f"The net of a cube has total area {6 * s_ * s_} square units. Find the edge length and the cube's volume.", f"edge {s_}; volume {s_ ** 3}", [f"6s² = {6 * s_ * s_} → s = {s_}.", "V = s³."])
    else:
        l, w, h = R.randint(2, 10), R.randint(2, 10), R.randint(2, 10)
        B.mc(6, lv(), f"A box with no top is {l} by {w} on the bottom and {h} tall. How much cardboard does its net use?", str(l * w + 2 * l * h + 2 * w * h), [str(2 * (l * w + l * h + w * h)), str(l * w * h), str(l * w + l * h + w * h)], ["One base only: lw + 2lh + 2wh."], tags=["application", "misconception"])
def mk_cyl_sa():
    r, h = R.randint(1, 12), R.randint(2, 20)
    B.orq(6, "honors", f"A cylinder (a 'circular prism') has radius {r} and height {h}.", [("Describe its net.", "two circles and a rectangle"), ("What is the rectangle's length? Why?", f"{pit(2 * r)}: it wraps around the circumference"), ("Find the lateral area.", pit(2 * r * h)), ("Find the total surface area.", pia(2 * r * h + 2 * r * r))], ["Unroll the side.", "C = 2πr.", "2πrh.", "2πrh + 2πr²."], tags=["challenge"])

# =============== Skill 7: volume ===============
def mk_vol_prism():
    k = R.random(); u = un()
    if k < 0.5:
        l, w, h = R.randint(2, 15), R.randint(2, 12), R.randint(2, 14)
        d_ = box_fig(l, w, h, (f"{l} {u}", f"{w} {u}", f"{h} {u}"), "vbox", f"Rectangular prism {l} by {w} by {h} {u}.")
        B.mc(7, lv(), "Find the volume of the prism.", f"{l * w * h} {u}³", [f"{2 * (l * w + l * h + w * h)} {u}³", f"{l + w + h} {u}³", f"{fr(F(l * w * h, 3))} {u}³"], ["V = Bh = lwh."], diagram=d_, tags=["diagram", "misconception"])
    else:
        a, b = R.randint(3, 12), R.randint(3, 12); L = R.randint(3, 20); V = F(a * b, 2) * L
        d_ = triprism_fig(a, b, L, (str(a), str(b), str(L)), "vtri", f"Right triangular prism with legs {a} and {b} {u} and length {L} {u}.")
        B.sa(7, lv(), f"Find the volume of the triangular prism (measurements in {u}).", f"{fr(V)} {u}³", [f"B = ½·{a}·{b} = {fr(F(a * b, 2))}.", f"V = B·{L}."], diagram=d_, tags=["diagram"])
def mk_vol_cyl():
    r, h = R.randint(1, 12), R.randint(2, 20); u = un(); V = r * r * h
    d_ = cyl_fig(r, h, (f"{r}", f"{h}"), "cyl", f"Cylinder with radius {r} {u} and height {h} {u}.")
    if R.random() < 0.55:
        B.mc(7, lv(), f"Find the volume of the cylinder (in {u}).", f"{pia(V)} {u}³", [f"{pia(2 * r * h)} {u}³", f"{pia(F(V, 3))} {u}³", f"{pia(4 * r * r * h)} {u}³"], ["V = πr²h."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.sa(7, lv(), f"A cylinder has volume {pit(V)} {u}³ and radius {r} {u}. Find its height.", f"{h} {u}", [f"π·{r}²·h = {pit(V)} → h = {h}."])
def mk_vol_cone():
    r, h, l = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 5, 13), (4, 3, 5)]); u = un(); V = F(r * r * h, 3)
    d_ = cyl_fig(r, h, (f"{r}", f"{h}", ""), "cone", f"Cone with radius {r} {u} and height {h} {u}.", cone=True)
    if R.random() < 0.5:
        B.mc(7, lv(), f"Find the volume of the cone (in {u}).", f"{pia(V)} {u}³", [f"{pia(r * r * h)} {u}³", f"{pia(F(r * r * l, 3))} {u}³", f"{pia(F(r * h, 3))} {u}³"], ["V = ⅓πr²h — use the height, not the slant height."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(7, lv(), f"Use the cone (measurements in {u}).", [("Find the slant height.", f"{l} {u}"), ("Find the volume.", f"{pia(V)} {u}³"), ("Find the volume of a cylinder with the same base and height.", f"{pia(r * r * h)} {u}³"), ("Compare.", "The cone has ⅓ the volume of the cylinder")], ["Pythagorean Theorem.", "⅓πr²h.", "πr²h.", "Ratio 1 : 3."], diagram=d_, tags=["diagram"])
def mk_vol_pyr():
    b, h = R.randint(2, 15), R.randint(3, 18); u = un(); V = F(b * b * h, 3)
    d_ = pyr_fig(b, h, (f"{b}", f"{h}"), "vpyr", f"Square pyramid with base edge {b} {u} and height {h} {u}.")
    if R.random() < 0.5:
        B.sa(7, lv(), f"Find the volume of the square pyramid (in {u}).", f"{fr(V)} {u}³", ["V = ⅓Bh.", f"⅓·{b}²·{h}."], diagram=d_, tags=["diagram"])
    else:
        B.sa(7, "honors", f"A square pyramid has volume {fr(V)} {u}³ and height {h} {u}. Find its base edge.", f"{b} {u}", [f"⅓·s²·{h} = {fr(V)} → s² = {b * b}.", f"s = {b}."], tags=["challenge"])
def mk_vol_sel():
    V = R.choice([24, 36, 48, 60, 72, 84, 96, 108, 120, 144, 180, 192, 216, 240]); opts = []
    for _ in range(40):
        l, w = R.randint(1, 12), R.randint(1, 12)
        if V % (l * w) == 0 and l <= w: opts.append(("prism", l, w, V // (l * w)))
        if (3 * V) % (l * l) == 0 and l > 1: opts.append(("pyramid", l, l, 3 * V // (l * l)))
    good = list({f"a {k} with base {a} by {b} and height {h}": 1 for k, a, b, h in opts}.keys())
    if len(good) < 3: raise ValueError
    gs = R.sample(good, 3); bad = [f"a square pyramid with base 3 by 3 and height {V // 9 if V % 9 == 0 else V // 3}", f"a prism with base 2 by 3 and height {V // 3}"]
    def vol(s):
        w_ = s.split(); a, b, h = int(w_[-6]), int(w_[-4]), int(w_[-1]); return F(a * b * h, 3) if "pyramid" in s else a * b * h
    bad = [x for x in bad if vol(x) != V]
    if not bad: raise ValueError
    assert all(vol(g) == V for g in gs)
    B.sel(7, lv(), f"Select ALL solids with volume {V} cubic units.", gs, bad, ["Prism: V = Bh. Pyramid: V = ⅓Bh."], tags=["concept"])
def mk_vol_orq():
    r = R.randint(1, 9); h = 2 * r
    B.orq(7, R.choice(["cp1", "honors"]), f"A cylinder, a cone, and a sphere each have radius {r}; the cylinder and cone have height {h} (= 2r).", [("Find the cylinder's volume.", pit(r * r * h)), ("Find the cone's volume.", pit(F(r * r * h, 3))), ("Find the sphere's volume.", pit(F(4 * r ** 3, 3))), ("Write the ratio cone : sphere : cylinder.", "1 : 2 : 3")], ["πr²h.", "⅓πr²h.", "(4/3)πr³.", f"Divide each by {pit(F(2 * r ** 3, 3))}."], tags=["reasoning"])
def mk_vol_find():
    r, h = R.randint(2, 10), R.randint(3, 15); kind = R.choice(["cone", "cylinder"]); V = F(r * r * h, 3) if kind == "cone" else F(r * r * h)
    B.orq(7, lv(), f"A {kind} has volume {pit(V)} cubic units and height {h}.", [("Write the volume formula.", "V = ⅓πr²h" if kind == "cone" else "V = πr²h"), ("Substitute the known values.", f"{pit(V)} = {'⅓' if kind == 'cone' else ''}π·r²·{h}"), ("Solve for r.", str(r)), ("Find the base area.", pit(r * r))], ["Formula.", "Substitute.", f"r² = {r * r}.", "πr²."])
def mk_cavalieri():
    r, h = R.randint(2, 9), R.randint(3, 15)
    B.mc(7, lv(), f"A right cylinder and an oblique cylinder both have radius {r} and height {h}. How do their volumes compare?", f"They are equal ({pit(r * r * h)}) by Cavalieri's Principle", ["The oblique cylinder is larger because its side is longer", "The oblique cylinder is smaller because it leans", "It cannot be determined"], ["Same cross-sectional area at every height and same height ⇒ same volume."], tags=["concept"])

# =============== Skill 8: spheres ===============
def mk_sphere():
    r = R.randint(1, 15); u = un(); SA = 4 * r * r; V = F(4 * r ** 3, 3); d_ = sphere_fig(r, f"{r} {u}", "sph", f"Sphere with radius {r} {u}.")
    k = R.random()
    if k < 0.35:
        B.mc(8, lv(), "Find the volume of the sphere.", f"{pia(V)} {u}³", [f"{pia(SA)} {u}³", f"{pia(4 * r ** 3)} {u}³", f"{pia(F(4 * r * r, 3))} {u}³"], ["V = (4/3)πr³."], diagram=d_, tags=["diagram", "misconception"])
    elif k < 0.6:
        B.mc(8, lv(), "Find the surface area of the sphere.", f"{pia(SA)} {u}²", [f"{pia(r * r)} {u}²", f"{pia(2 * r * r)} {u}²", f"{pia(V)} {u}²" if V != SA else f"{pia(8 * r * r)} {u}²"], ["SA = 4πr²."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(8, lv(), "Use the sphere.", [("Find the area of a great circle.", f"{pia(r * r)} {u}²"), ("Find the surface area.", f"{pia(SA)} {u}²"), ("Find the volume.", f"{pia(V)} {u}³"), ("How many great circles' areas equal the surface area?", "4")], ["πr².", "4πr².", "(4/3)πr³.", "4πr² ÷ πr²."], diagram=d_, tags=["diagram"])
def mk_sphere_rev():
    r = R.choice([3, 6, 9, 12, 15, 2, 4, 5]); k = R.random()
    if k < 0.5:
        V = F(4 * r ** 3, 3); B.sa(8, lv(), f"A sphere has volume {pit(V)} cubic units. Find its radius.", str(r), [f"(4/3)πr³ = {pit(V)} → r³ = {r ** 3}.", f"r = {r}."])
    else:
        B.sa(8, lv(), f"A sphere has surface area {pit(4 * r * r)} square units. Find its volume.", pit(F(4 * r ** 3, 3)), [f"4πr² = {pit(4 * r * r)} → r = {r}.", "V = (4/3)πr³."])
def mk_hemi():
    r = R.randint(2, 12); d_ = sphere_fig(r, str(r), "hemi", f"Hemisphere with radius {r}.", hemi=True)
    B.orq(8, lv(), "The solid is a hemisphere.", [("Find its volume.", pia(F(2 * r ** 3, 3))), ("Find the curved surface area.", pia(2 * r * r)), ("Find the area of the flat base.", pia(r * r)), ("Find the total surface area.", pia(3 * r * r))], ["Half of (4/3)πr³.", "Half of 4πr².", "πr².", "2πr² + πr²."], diagram=d_, tags=["diagram"])
def mk_sph_sel():
    r = R.randint(2, 9)
    st = {f"Its volume is {pit(F(4 * r ** 3, 3))}": True, f"Its surface area is {pit(4 * r * r)}": True, "Doubling the radius multiplies the volume by 8": True, "Doubling the radius doubles the surface area": False, f"Its volume is {pit(4 * r ** 3)}": False}
    B.sel(8, lv(), f"A sphere has radius {r}. Select ALL true statements.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["V = (4/3)πr³; SA = 4πr²; scale by k³ and k²."], tags=["concept"])
def mk_sph_app():
    k = R.random()
    if k < 0.5:
        r = R.randint(2, 6)
        B.orq(8, "honors", f"A cylinder holds a ball of radius {r} snugly (the ball touches the top, bottom and side).", [("Find the cylinder's volume.", pit(2 * r ** 3)), ("Find the ball's volume.", pit(F(4 * r ** 3, 3))), ("What fraction of the cylinder does the ball fill?", "2/3"), ("Find the empty volume.", pit(F(2 * r ** 3, 3)))], [f"πr²(2r).", "(4/3)πr³.", "Archimedes' ratio.", "Subtract."], tags=["challenge"])
    else:
        d = R.choice([22, 24, 9, 7, 30]); r = F(d, 2); V = F(4, 3) * r ** 3
        B.sa(8, lv(), f"A ball has diameter {d} cm. Find its volume to the nearest cubic centimeter.", f"{round(float(V) * math.pi)} cm³", [f"r = {fr(r)}.", f"(4/3)π({fr(r)})³ ≈ {float(V) * math.pi:.1f}."], tags=["application"])

# =============== Skill 9: composite solids ===============
def mk_silo():
    r, h = R.randint(2, 10), R.randint(5, 25); u = R.choice(["ft", "m"])
    d_ = cyl_fig(r, h, (f"{r}", f"{h}"), "silo", f"Silo: cylinder with radius {r} {u} and height {h} {u} topped by a hemisphere of radius {r} {u}.", hemi=True)
    Vc, Vh = r * r * h, F(2 * r ** 3, 3)
    B.orq(9, lv(), f"A silo is a cylinder topped by a hemisphere ({u}).", [("Find the cylinder's volume.", f"{pia(Vc)} {u}³"), ("Find the hemisphere's volume.", f"{pia(Vh)} {u}³"), ("Find the total volume.", f"{pia(Vc + Vh)} {u}³"), ("Find the outer surface area, excluding the floor.", f"{pia(2 * r * h + 2 * r * r)} {u}²")], ["πr²h.", "(2/3)πr³.", "Add.", "2πrh + 2πr²."], diagram=d_, tags=["diagram", "application"])
def mk_cone_cyl():
    r, ch, l = R.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (4, 3, 5), (8, 6, 10)]); h = R.randint(3, 15)
    d_ = cyl_fig(r, h, (f"{r}", f"{h}", f"{ch}"), "conecyl", f"Cylinder of radius {r} and height {h} with a cone of height {ch} on top.", cone_top=ch)
    Vc, Vk = r * r * h, F(r * r * ch, 3)
    if R.random() < 0.5:
        B.mc(9, lv(), "Find the total volume of the solid.", pia(Vc + Vk), [pia(Vc + r * r * ch), pia(Vc), pia(F(Vc + r * r * ch, 3))], ["Cylinder πr²h plus cone ⅓πr²h."], diagram=d_, tags=["diagram", "misconception"])
    else:
        B.orq(9, "honors", "Use the solid (a cylinder with a cone on top).", [("Find the cone's slant height.", str(l)), ("Find the cone's lateral area.", pit(r * l)), ("Find the cylinder's lateral area plus its bottom.", pit(2 * r * h + r * r)), ("Find the total surface area.", pia(r * l + 2 * r * h + r * r))], ["Pythagorean Theorem.", "πrℓ.", "2πrh + πr².", "The shared circle is not on the surface."], diagram=d_, tags=["diagram", "challenge"])
def mk_hole():
    s_ = R.randint(6, 16); r = R.randint(1, s_ // 2 - 1); h = s_
    B.orq(9, lv(), f"A cube with edge {s_} cm has a cylindrical hole of radius {r} cm drilled straight through the centers of two opposite faces.", [("Find the cube's volume.", f"{s_ ** 3} cm³"), ("Find the volume removed.", f"{pia(r * r * h)} cm³"), ("Find the remaining volume.", f"{s_ ** 3} − {pit(r * r * h)} ≈ {s_ ** 3 - r * r * h * math.pi:.2f} cm³"), ("What percent of the cube remains?", f"{100 * (1 - r * r * h * math.pi / s_ ** 3):.1f}%")], ["s³.", "πr²h with h = edge.", "Subtract.", "Remaining ÷ original."], tags=["application"])
def mk_icecream():
    r = R.randint(2, 5); h = R.randint(6, 14)
    Vk, Vh = F(r * r * h, 3), F(2 * r ** 3, 3)
    B.sa(9, lv(), f"An ice cream cone (radius {r} cm, height {h} cm) is filled and topped with a hemisphere of ice cream of the same radius. Find the total volume of ice cream.", pia(Vk + Vh, "cm³"), [f"Cone: ⅓π·{r}²·{h} = {pit(Vk)}.", f"Hemisphere: (2/3)π·{r}³ = {pit(Vh)}."], tags=["application"])
def mk_comp_sel():
    r, h = R.randint(2, 8), R.randint(3, 12)
    st = {f"πr²h + (2/3)πr³ with r = {r}, h = {h}": True, f"{pit(r * r * h + F(2 * r ** 3, 3))}": True, f"πr²h + (4/3)πr³ with r = {r}, h = {h}": False, f"{pit(r * r * h)}": False, f"π·{r}²·{h} + ½·(4/3)π·{r}³": True}
    B.sel(9, lv(), f"A capsule-shaped tank is a cylinder (r = {r}, h = {h}) with a hemisphere on ONE end. Select ALL correct expressions for its volume.", [k for k, v in st.items() if v], [k for k, v in st.items() if not v], ["Cylinder + half a sphere."], tags=["concept"])
def mk_box_pyr():
    s_ = R.randint(3, 12); h = R.randint(3, 12)
    B.sa(9, lv(), f"A storage building is a cube with edge {s_} m topped by a square pyramid with the same base and height {h} m. Find its volume.", f"{fr(s_ ** 3 + F(s_ * s_ * h, 3))} m³", [f"Cube: {s_ ** 3}.", f"Pyramid: ⅓·{s_}²·{h} = {fr(F(s_ * s_ * h, 3))}."], tags=["application"])

# =============== Skill 10: effects of scale factor ===============
def mk_scale():
    k = R.choice([2, 3, 4, 5, F(1, 2), F(1, 3), F(3, 2), F(2, 3)]); A_ = R.randint(2, 30) * (k.denominator ** 3 if isinstance(k, F) else 1); kk = F(k)
    q = R.random()
    if q < 0.35:
        B.mc(10, lv(), f"Two similar solids have scale factor {fr(kk)} (new : old). The old surface area is {A_}. Find the new surface area.", fr(A_ * kk * kk), [fr(A_ * kk), fr(A_ * kk ** 3), fr(A_ * 2 * kk)], ["Areas scale by k²."], tags=["misconception"])
    elif q < 0.7:
        B.mc(10, lv(), f"Two similar solids have scale factor {fr(kk)} (new : old). The old volume is {A_}. Find the new volume.", fr(A_ * kk ** 3), [fr(A_ * kk), fr(A_ * kk * kk), fr(A_ * 3 * kk)], ["Volumes scale by k³."], tags=["misconception"])
    else:
        B.orq(10, lv(), f"Figure B is a dilation of solid A with scale factor {fr(kk)}.", [("Ratio of corresponding edges?", fr(kk)), ("Ratio of surface areas?", fr(kk * kk)), ("Ratio of volumes?", fr(kk ** 3)), (f"If A has volume {A_}, find B's volume.", fr(A_ * kk ** 3))], ["k.", "k².", "k³.", "Multiply by k³."])
def mk_scale_rev():
    a, b = R.sample(range(1, 7), 2); q = R.random()
    if q < 0.5:
        B.orq(10, "honors", f"Two similar cylinders have volumes {a ** 3 * 8}π and {b ** 3 * 8}π.", [("Find the ratio of volumes.", f"{fr(F(a ** 3, b ** 3))}"), ("Find the scale factor.", fr(F(a, b))), ("Find the ratio of surface areas.", fr(F(a * a, b * b))), (f"If the smaller has height {min(a, b) * 3}, find the larger's height.", str(max(a, b) * 3))], ["Simplify.", "Cube root.", "Square the scale factor.", "Multiply by the scale factor."], tags=["challenge"])
    else:
        B.sa(10, lv(), f"Two similar figures have areas {a * a * 5} and {b * b * 5}. Find the ratio of their perimeters.", f"{a // math.gcd(a, b)}:{b // math.gcd(a, b)}", [f"Area ratio {a * a}:{b * b}.", f"Square root: {a}:{b}, which simplifies to {a // math.gcd(a, b)}:{b // math.gcd(a, b)}."])
def mk_dim_change():
    sol = R.choice(["cylinder", "cone", "rectangular prism", "sphere"]); k = R.choice([2, 3, F(1, 2)])
    if sol == "sphere":
        B.mc(10, lv(), f"The radius of a sphere is multiplied by {fr(k)}. By what factor does its volume change?", fr(F(k) ** 3), [fr(F(k)), fr(F(k) ** 2), fr(3 * F(k))], ["Volume ∝ r³."], tags=["misconception"])
    elif sol == "rectangular prism":
        B.mc(10, lv(), f"Only the height of a rectangular prism is multiplied by {fr(k)}. By what factor does its volume change?", fr(F(k)), [fr(F(k) ** 3), fr(F(k) ** 2), "It does not change"], ["V = lwh is linear in h; this is not a similarity transformation."], tags=["misconception"])
    else:
        B.mc(10, lv(), f"Only the radius of a {sol} is multiplied by {fr(k)}; the height is unchanged. By what factor does its volume change?", fr(F(k) ** 2), [fr(F(k)), fr(F(k) ** 3), fr(F(k) ** 2 / 3)], ["V ∝ r² when h is fixed."], tags=["misconception"])
def mk_scale_sel():
    k = R.choice([2, 3, 4])
    st = {f"Perimeters multiply by {k}": True, f"Areas multiply by {k * k}": True, f"Volumes multiply by {k ** 3}": True, f"Volumes multiply by {k * k}": False, f"Areas multiply by {k}": False, "Angle measures stay the same": True}
    B.sel(10, lv(), f"A solid is dilated by scale factor {k}. Select ALL true statements.", [x for x, v in st.items() if v], [x for x, v in st.items() if not v], ["Lengths × k, areas × k², volumes × k³; angles are preserved."], tags=["concept"])
def mk_scale_app():
    k = R.choice([2, 3, 4, 5]); c = R.randint(2, 20)
    q = R.random()
    if q < 0.5:
        B.sa(10, lv(), f"A model is built at 1 : {k * 10} scale. The model uses {c} cm² of paint. How much paint (in cm²) would the real object need?", f"{c * (k * 10) ** 2} cm²", [f"Areas scale by {k * 10}² = {(k * 10) ** 2}."], tags=["application"])
    else:
        B.sa(10, lv(), f"A small statue weighs {c} lb. A similar statue of the same material is {k} times as tall. How much does it weigh?", f"{c * k ** 3} lb", [f"Weight ∝ volume, which scales by {k}³ = {k ** 3}."], tags=["application"])

makers = {1: [mk_rect, mk_para, mk_coord_poly, mk_rect_sel, mk_sq_diag], 2: [mk_tri, mk_trap, mk_equil, mk_regpoly, mk_kite, mk_area_sel], 3: [mk_L, mk_L, mk_semi_rect, mk_shaded, mk_comp_app],
          4: [mk_circ, mk_circ, mk_circ_rev, mk_circ_sel, mk_circ_derive], 5: [mk_pizza, mk_sprinkler, mk_wiper, mk_clock, mk_track, mk_app_sel], 6: [mk_box_sa, mk_tri_prism, mk_pyr_sa, mk_net_sel, mk_cube_net, mk_cyl_sa],
          7: [mk_vol_prism, mk_vol_cyl, mk_vol_cone, mk_vol_pyr, mk_vol_sel, mk_vol_sel, mk_cavalieri, mk_vol_orq, mk_vol_find], 8: [mk_sphere, mk_sphere, mk_sphere_rev, mk_hemi, mk_sph_sel, mk_sph_app], 9: [mk_silo, mk_cone_cyl, mk_hole, mk_icecream, mk_comp_sel, mk_box_pyr],
          10: [mk_scale, mk_scale, mk_scale_rev, mk_dim_change, mk_scale_sel, mk_scale_app]}
for S_, ms in makers.items():
    fill(B, S_, 32, ms, R)

if __name__ == "__main__":
    for q in B.qs:
        q["prompt"] = q["prompt"].replace("in..", "in.")
        for p_ in q.get("parts", []): p_["prompt"] = p_["prompt"].replace("in..", "in.")
        if "diagram" in q: q["diagram"]["spec"]["alt"] = q["diagram"]["spec"]["alt"].replace("in..", "in.")
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
