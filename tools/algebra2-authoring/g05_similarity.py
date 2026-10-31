from lib import Bank, graph
from mathlite import *
from geofig import Fig, tri_from_sides, tri_from_angles
from fill import fill
import math, random

STD = {1: ["G-SRT.B.5"], 2: ["G-SRT.A.2"], 3: ["G-SRT.A.1"], 4: ["G-SRT.A.3"], 5: ["G-SRT.B.5"], 6: ["G-SRT.B.5"], 7: ["G-SRT.B.4"], 8: ["G-MG.A.1", "G-SRT.B.5"], 9: ["G-SRT.B.4", "G-SRT.B.5"]}
B = Bank("similarity", "sm", STD, course="geometry", prefix="geo")
R = random.Random(505)
LET = ["ABC", "DEF", "PQR", "XYZ", "JKL", "RST", "MNO", "GHI"]
def lv(): return R.choice(["cp2", "cp1", "cp1", "honors"])
def nz(v): return fr(F(v).limit_denominator(1000))

# ---------- figures ----------
def sim_pair(name, sides, k, labels=("ABC", "DEF"), show=(True, True), unknown=None):
    a, b, c = sides; A, Bv, C = tri_from_sides(a, b, c)
    T1 = [A, Bv, C]; off = a + 3.0
    T2 = [(p[0] * k + off, p[1] * k) for p in T1]
    fg = Fig(5.6, 3.0)
    vals = {}
    for T, lab, sc, sh in ((T1, labels[0], 1, show[0]), (T2, labels[1], k, show[1])):
        fg.poly(T); fg.names(T, list(lab))
        P_ = dict(zip("ABC", T)); cen = (sum(p[0] for p in T) / 3, sum(p[1] for p in T) / 3)
        for sd, L_ in (("AB", c), ("BC", a), ("CA", b)):
            key = (lab, sd); txt = nz(L_ * sc)
            if unknown == key: txt = "x"
            elif not sh: continue
            fg.side(P_[sd[0]], P_[sd[1]], txt, center=cen)
    alt = f"Similar triangles {labels[0]} and {labels[1]} with correspondence {labels[0][0]}↔{labels[1][0]}, {labels[0][1]}↔{labels[1][1]}, {labels[0][2]}↔{labels[1][2]}; side lengths labeled" + (", one labeled x." if unknown else ".")
    return fg.save(B, name, alt)


def splitter(name, AD, DB, AE, EC, lab=("AD", "DB", "AE", "EC")):
    """Triangle ABC with DE ∥ BC, D on AB, E on AC (drawn true: AD/DB = AE/EC)."""
    assert F(AD) * EC == F(AE) * DB
    AB = AD + DB; AC = AE + EC; BC = 0.9 * max(AB, AC)
    A, Bv, C = tri_from_sides(BC, AC, AB)
    t = AD / AB; D = (A[0] + t * (Bv[0] - A[0]), A[1] + t * (Bv[1] - A[1])); E = (A[0] + t * (C[0] - A[0]), A[1] + t * (C[1] - A[1]))
    fg = Fig(4.2, 3.4); fg.poly([A, Bv, C]); fg.seg(D, E); fg.names([A, Bv, C], ["A", "B", "C"]); fg.dot(D, None); fg.dot(E, None)
    fg.text(D, "D", (-10, 4)); fg.text(E, "E", (10, 4)); fg.arrows(D, E); fg.arrows(Bv, C)
    cen = ((A[0] + Bv[0] + C[0]) / 3, (A[1] + Bv[1] + C[1]) / 3)
    fg.side(A, D, lab[0], center=cen); fg.side(D, Bv, lab[1], center=cen); fg.side(A, E, lab[2], center=cen); fg.side(E, C, lab[3], center=cen)
    return fg.save(B, name, f"Triangle ABC with segment DE parallel to BC (arrow marks), D on AB and E on AC; AD = {lab[0]}, DB = {lab[1]}, AE = {lab[2]}, EC = {lab[3]}.")


# ---------------- Skill 1: ratios and proportions ----------------
S = 1
def mk_prop():
    a, b, c = R.randint(2, 15), R.randint(2, 15), R.randint(2, 30)
    x = F(b * c, a)
    B.sa(1, lv(), f"Solve the proportion {a}/{b} = {c}/x.", f"x = {nz(x)}", ["Cross-multiply.", f"{a}x = {b * c}."])
def mk_prop_alg():
    x = R.randint(1, 12)
    m1, m2 = R.sample(range(2, 9), 2); k1 = R.randint(0, 9); val = (x + k1); k2 = F(val * m2, m1) - x
    if k2.denominator != 1: raise AssertionError
    e1 = f"(x + {k1})" if k1 else "x"; e2 = f"(x {'+' if k2 >= 0 else '-'} {abs(k2)})"
    B.sa(1, lv(), f"Solve {e1}/{m1} = {e2}/{m2}.", f"x = {x}", ["Cross-multiply and solve the linear equation."])
    assert F(x + k1, m1) == (x + k2) / m2
def mk_ratio_split():
    parts = R.sample(range(1, 8), R.choice([2, 3])); tot = sum(parts) * R.randint(2, 12)
    ctx = R.choice(["the angles of a triangle", "the sides of a triangle with perimeter", "a 60-ft board cut into pieces"])
    if ctx == "the angles of a triangle":
        if len(parts) != 3: raise AssertionError
        k = F(180, sum(parts)); B.mc(1, lv(), f"The angles of a triangle are in the ratio {' : '.join(map(str, parts))}. Find the largest angle.", f"{nz(k * max(parts))}°", [f"{nz(k * min(parts))}°", f"{nz(F(180, len(parts)))}°", f"{nz(k * max(parts) + 10)}°"], [f"{sum(parts)}k = 180 → k = {nz(k)}."])
    else:
        k = F(tot, sum(parts)); B.sa(1, lv(), f"A segment of length {tot} is divided in the ratio {' : '.join(map(str, parts))}. Find each part.", ", ".join(nz(k * p) for p in parts), [f"{sum(parts)}k = {tot}.", f"k = {nz(k)}."])
def mk_rate():
    items = R.randint(3, 12); cost = R.randint(5, 60); want = R.randint(2, 20)
    B.mc(1, lv(), f"{items} notebooks cost ${cost}. At the same rate, how much do {want} notebooks cost?", f"${nz(F(cost * want, items)) if F(cost * want, items).denominator == 1 else f'{cost * want / items:.2f}'}", [f"${cost * want / items + 1:.2f}", f"${cost + want}", f"${cost * items / want:.2f}"], ["Set up a proportion: cost/items."], tags=["modeling"])
def mk_prop_sel():
    a, b = R.randint(2, 9), R.randint(2, 9); k = R.randint(2, 5)
    cands = [f"{a * k}/{b * k}", f"{a * (k + 1)}/{b * (k + 1)}", f"{a + k}/{b + k}", f"{b}/{a}", f"{a * k}/{b}"]
    sel_auto(B, 1, lv(), f"Select ALL ratios equivalent to {a}/{b}.", cands, lambda s_: F(*map(int, s_.split("/"))) == F(a, b), ["Equivalent ratios: multiply both terms by the same number.", "Adding the same number does not keep the ratio."], tags=["misconception"])
B.orq(S, "cp1", "Use the proportion a/b = c/d with b, d ≠ 0.", [("Which product equality follows?", "ad = bc"), ("Is a/c = b/d also true (c ≠ 0)?", "Yes"), ("Is (a + b)/b = (c + d)/d true?", "Yes"), ("Is a/b = (a + c)/(b + d) true?", "Yes (when b + d ≠ 0)")], ["Cross products.", "Divide ad = bc by cd.", "Add 1 to both sides.", "Componendo: equal ratios combine."], tags=["reasoning", "challenge"])
B.sa(S, "cp2", "Write the ratio 18 : 24 in simplest form.", "3 : 4", ["Divide by 6."])

# ---------------- Skill 2: similar polygons ----------------
S = 2
for k_, (sides, k) in enumerate([((5, 4, 3.0), 2), ((6, 5, 4), 1.5), ((4, 6, 7), 0.5)]):
    dg = sim_pair(f"s02-pair-{k_}", sides, k, unknown=("DEF", "BC"))
    B.orq(S, "cp1", f"△ABC ~ △DEF as shown.", [("Find the scale factor from △ABC to △DEF.", nz(k)), ("Find x (side EF).", nz(sides[0] * k)), ("Find the perimeter of △DEF.", nz(sum(sides) * k)), ("Find the ratio of the perimeters.", f"{nz(k)} (same as the scale factor)")],
          ["Compare a pair of corresponding sides.", "EF = k·BC.", "Multiply each side.", "Perimeters scale by k."], diagram=dg, tags=["graph"])
def mk_poly_sim():
    k = R.choice([F(2), F(3), F(1, 2), F(3, 2), F(5, 2), F(4, 3)]); s1 = [R.randint(3, 14) for _ in range(4)]; L1, L2 = "ABCD", "EFGH"
    i = R.randrange(4); j = (i + 1) % 4
    if R.random() < 0.5:
        B.sa(2, lv(), f"Quadrilateral ABCD ~ EFGH with AB = {s1[0]}, BC = {s1[1]}, CD = {s1[2]}, DA = {s1[3]}, and EF = {nz(s1[0] * k)}. Find {L2[i]}{L2[j]}.", nz(s1[i] * k), [f"Scale factor {nz(k)}.", f"{L2[i]}{L2[j]} = {nz(k)}·{s1[i]}."])
    else:
        B.mc(2, lv(), f"Quadrilateral ABCD ~ EFGH with scale factor {nz(k)}. The perimeter of ABCD is {sum(s1)}. Find the perimeter of EFGH.", nz(sum(s1) * k), [nz(sum(s1) * k * k), nz(sum(s1) / k), nz(sum(s1) + k)], ["Perimeters scale by k (areas by k²)."], tags=["misconception"])
def mk_sim_check():
    a, b = R.randint(3, 12), R.randint(3, 12); k = R.choice([2, 3, F(3, 2)]); ok = R.random() < 0.5
    c, d = a * k, (b * k if ok else b * k + R.choice([1, 2, -1]))
    B.mc(2, lv(), f"Rectangle 1 is {a} by {b}. Rectangle 2 is {nz(c)} by {nz(d)}. Are they similar?", "Yes" if F(c, a) == F(d, b) else "No", ["No" if F(c, a) == F(d, b) else "Yes", "Only if both are squares", "Cannot be determined"], [f"Ratios {nz(F(c) / a)} and {nz(F(d) / b)}."])
def mk_sim_sel():
    L1, L2 = R.sample(LET, 2)
    st = {f"∠{L1[0]} ≅ ∠{L2[0]}": True, f"{L1[0]}{L1[1]}/{L2[0]}{L2[1]} = {L1[1]}{L1[2]}/{L2[1]}{L2[2]}": True, f"{L1[0]}{L1[2]}/{L2[0]}{L2[2]} = {L1[0]}{L1[1]}/{L2[0]}{L2[1]}": True, f"{L1[0]}{L1[1]} ≅ {L2[0]}{L2[1]}": False, f"∠{L1[1]} ≅ ∠{L2[2]}": False}
    B.sel(2, lv(), f"△{L1} ~ △{L2}. Select ALL statements that must be true.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Similar: corresponding angles congruent and corresponding sides proportional (not necessarily congruent)."])
B.mc(S, "cp1", "Which pair of figures must be similar?", "any two squares", ["any two rectangles", "any two rhombi", "any two isosceles triangles"], ["Squares: all angles 90° and all sides proportional."], tags=["reasoning"])

# ---------------- Skill 3: dilations ----------------
S = 3
def mk_dil_pt():
    k = R.choice([F(2), F(3), F(1, 2), F(1, 3), F(3, 2), F(-1), F(-2)]); P_ = (R.randint(-8, 8), R.randint(-8, 8))
    if R.random() < 0.6:
        B.sa(3, lv(), f"Dilate P{pt(*P_)} by scale factor {nz(k)} centered at the origin.", pt(k * P_[0], k * P_[1]), ["Multiply each coordinate by k."])
    else:
        C_ = (R.randint(-4, 4), R.randint(-4, 4)); img = (C_[0] + k * (P_[0] - C_[0]), C_[1] + k * (P_[1] - C_[1]))
        B.mc(3, "honors", f"Dilate P{pt(*P_)} by scale factor {nz(k)} centered at C{pt(*C_)}.", pt(*img), [pt(k * P_[0], k * P_[1]), pt(C_[0] + k * P_[0], C_[1] + k * P_[1]), pt(P_[0] + k * C_[0], P_[1] + k * C_[1])], ["P′ = C + k(P - C)."], tags=["misconception"])
def mk_dil_k():
    k = R.choice([F(2), F(3), F(1, 2), F(5, 2), F(2, 3), F(4)]); L_ = R.randint(2, 15)
    kind = "enlargement" if k > 1 else "reduction"
    B.mc(3, lv(), f"A segment of length {L_} is dilated to length {nz(k * L_)}. Find the scale factor and classify the dilation.", f"{nz(k)}; {kind}", [f"{nz(1 / k)}; {'reduction' if k > 1 else 'enlargement'}", f"{nz(k * L_ - L_)}; {kind}", f"{nz(k)}; {'reduction' if k > 1 else 'enlargement'}"], ["k = image/original.", "k > 1 enlarges; 0 < k < 1 reduces."])
def mk_dil_props():
    k = R.choice([2, 3, F(1, 2)])
    st = {"Angle measures are preserved": True, f"Lengths are multiplied by {nz(k)}": True, "A line not through the center maps to a parallel line": True, "Lengths are preserved": False, f"Area is multiplied by {nz(k)}": False}
    B.sel(3, lv(), f"A figure is dilated by scale factor {nz(k)} (center not on the figure). Select ALL true statements.", [a for a, t in st.items() if t], [a for a, t in st.items() if not t], ["Dilations preserve angles, scale lengths by k, areas by k²."])
def mk_dil_tri():
    k = R.choice([2, 3, F(1, 2)]); T = [(R.randint(-4, 4) * 2, R.randint(-4, 4) * 2) for _ in range(3)]
    if (T[1][0] - T[0][0]) * (T[2][1] - T[0][1]) == (T[2][0] - T[0][0]) * (T[1][1] - T[0][1]): raise AssertionError
    img = [(k * p[0], k * p[1]) for p in T]
    B.orq(3, lv(), f"Dilate △ABC with A{pt(*T[0])}, B{pt(*T[1])}, C{pt(*T[2])} by {nz(k)} about the origin.", [("Find A′.", pt(*img[0])), ("Find B′.", pt(*img[1])), ("Find C′.", pt(*img[2])), ("Compare A′B′ with AB.", f"A′B′ = {nz(k)}·AB")], ["Multiply coordinates by k.", "Same.", "Same.", "Dilation scales lengths by k."])
dg = graph(B, "s03-dilation", [(("seg", [0, 2, 1, 0], [0, 0, 2, 0]), {}), (("seg", [0, 6, 3, 0], [0, 0, 6, 0]), {"color": "#c0392b", "ls": "--"})], xr=(-1, 7), yr=(-1, 7), points=[(0, 0, True, "O"), (2, 0, True, "B"), (1, 2, True, "C"), (6, 0, True, "B′"), (3, 6, True, "C′")],
           alt="Triangle OBC with O(0, 0), B(2, 0), C(1, 2) and its dashed image OB′C′ with B′(6, 0), C′(3, 6).")
B.orq(S, "cp1", "The graph shows △OBC and its dilation △OB′C′ centered at O.", [("Find the scale factor.", "3"), ("Is it an enlargement or reduction?", "enlargement"), ("Compare the slopes of BC and B′C′.", "both -2: parallel"), ("Compare the areas.", "△OB′C′ has 9 times the area")], ["6/2.", "k > 1.", "Dilation maps lines to parallel lines.", "k²."], diagram=dg, tags=["graph"])

# ---------------- Skill 4: AA ----------------
S = 4
def mk_aa():
    a, b = R.randint(25, 85), R.randint(25, 85)
    if a + b >= 170: raise AssertionError
    c = 180 - a - b; L1, L2 = R.sample(LET, 2)
    ok = R.random() < 0.6
    a2, b2 = (a, c) if ok else (a, c + R.choice([-5, 5, 10]))
    if a2 + b2 >= 180: raise AssertionError
    B.mc(4, lv(), f"△{L1} has angles {a}° and {b}°. △{L2} has angles {a2}° and {b2}°. Are the triangles similar?", "Yes, by AA" if ok else "No", ["No" if ok else "Yes, by AA", "Yes, by SAS", "Cannot tell without side lengths"],
         [f"Third angle of △{L1}: {c}°.", "Two pairs of congruent angles → AA." if ok else f"Angles of △{L1}: {a}, {b}, {c}; △{L2}: {a2}, {b2}, {180 - a2 - b2} — not all match."])
def mk_aa_reason():
    sc = R.choice([("DE ∥ BC with D on AB and E on AC", "△ADE ~ △ABC (∠A shared, ∠ADE ≅ ∠ABC corresponding)"), ("two right triangles share an acute angle", "the triangles are similar (right angles and the shared angle)"),
                   ("AB and CD intersect at E with AC ∥ BD", "△AEC ~ △BED (vertical angles, alternate interior angles)"), ("both triangles are isosceles with vertex angle 40°", "they are similar (base angles 70°)"),
                   ("two equilateral triangles", "they are similar (all angles 60°)")])
    B.sa(4, lv(), f"Explain why the triangles are similar: {sc[0]}.", sc[1], ["Find two pairs of congruent angles (AA)."], tags=["reasoning"])
def mk_aa_x():
    k = R.choice([F(2), F(3, 2), F(5, 2), F(3), F(4, 3)]); s1, s2 = R.randint(3, 12), R.randint(3, 12)
    B.sa(4, lv(), f"△ABC ~ △DEF by AA. AB = {s1}, DE = {nz(s1 * k)}, BC = {s2}. Find EF.", nz(s2 * k), [f"Scale factor DE/AB = {nz(k)}.", f"EF = {nz(k)}·{s2}."])
B.sel(S, "cp1", "Select ALL pairs of triangles that must be similar.", ["two right isosceles triangles", "two triangles each with angles 50° and 60°", "two equilateral triangles"], ["two right triangles", "two isosceles triangles", "two triangles each with a 40° angle"], ["AA requires two pairs of congruent angles."])
A, Bv, C = tri_from_angles(50, 70, 6); t = 0.45; D = (A[0] + t * (Bv[0] - A[0]), A[1] + t * (Bv[1] - A[1])); E = (A[0] + t * (C[0] - A[0]), A[1] + t * (C[1] - A[1]))
fg = Fig(3.8, 3.2); fg.poly([A, Bv, C]); fg.seg(D, E); fg.names([A, Bv, C], ["A", "B", "C"]); fg.text(D, "D", (-10, 3)); fg.text(E, "E", (10, 3)); fg.arrows(D, E); fg.arrows(Bv, C)
dg = fg.save(B, "s04-aa", "Triangle ABC with segment DE parallel to BC (arrow marks), D on AB and E on AC.")
B.orq(S, "cp1", "In the figure, DE ∥ BC.", [("Which angle is shared?", "∠A"), ("Which angle is congruent to ∠ADE? Why?", "∠ABC: corresponding angles"), ("State the similarity.", "△ADE ~ △ABC"), ("Which postulate?", "AA")], ["Common vertex.", "Parallel lines.", "Order the vertices.", "Two angle pairs."], diagram=dg, tags=["graph"])

# ---------------- Skill 5: SAS and SSS similarity ----------------
S = 5
def mk_sss():
    s = sorted([R.randint(3, 12) for _ in range(3)])
    if s[0] + s[1] <= s[2]: raise AssertionError
    k = R.choice([F(2), F(3, 2), F(5, 2), F(1, 2), F(3)]); ok = R.random() < 0.55
    t = [x * k for x in s]
    if not ok: t[R.randrange(3)] += 1
    B.mc(5, lv(), f"Are triangles with sides {', '.join(map(str, s))} and {', '.join(nz(v) for v in t)} similar?", f"Yes, SSS~ with scale factor {nz(k)}" if ok else "No", ["No" if ok else f"Yes, SSS~ with scale factor {nz(k)}", "Yes, AA", "Only if they are right triangles"],
         ["Compare ratios of corresponding sides (shortest to shortest, etc.).", f"Ratios: {', '.join(nz(F(v) / x) for v, x in zip(t, s))}."])
def mk_sas():
    a, b = R.randint(3, 12), R.randint(3, 12); k = R.choice([F(2), F(3, 2), F(3), F(1, 2)]); ang = R.randint(30, 120); ok = R.random() < 0.6
    a2, b2 = a * k, b * k if ok else b * k + 1; ang2 = ang
    L1, L2 = R.sample(LET, 2)
    B.mc(5, lv(), f"In △{L1}, {L1[0]}{L1[1]} = {a}, {L1[0]}{L1[2]} = {b}, m∠{L1[0]} = {ang}°. In △{L2}, {L2[0]}{L2[1]} = {nz(a2)}, {L2[0]}{L2[2]} = {nz(b2)}, m∠{L2[0]} = {ang2}°. Are they similar?", "Yes, SAS~" if ok else "No",
         ["No" if ok else "Yes, SAS~", "Yes, SSS~", "Yes, AA"], ["Included angles congruent; check the side ratios.", f"{nz(F(a2) / a)} and {nz(F(b2) / b)}."])
def mk_sas_sel():
    a, b = R.randint(3, 10), R.randint(3, 10); L1, L2 = R.sample(LET, 2)
    st = {f"{L2[0]}{L2[1]} = {2 * a}, {L2[0]}{L2[2]} = {2 * b}, ∠{L2[0]} ≅ ∠{L1[0]}": True, f"{L2[0]}{L2[1]} = {3 * a}, {L2[0]}{L2[2]} = {3 * b}, ∠{L2[0]} ≅ ∠{L1[0]}": True,
          f"{L2[0]}{L2[1]} = {2 * a}, {L2[0]}{L2[2]} = {2 * b + 1}, ∠{L2[0]} ≅ ∠{L1[0]}": False, f"{L2[0]}{L2[1]} = {2 * a}, {L2[0]}{L2[2]} = {2 * b}, ∠{L2[1]} ≅ ∠{L1[0]}": False}
    B.sel(5, lv(), f"△{L1} has {L1[0]}{L1[1]} = {a}, {L1[0]}{L1[2]} = {b}. Select ALL descriptions of △{L2} that guarantee △{L1} ~ △{L2} by SAS~.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t], ["Proportional sides with the congruent INCLUDED angle."])
B.mc(S, "cp1", "Which is NOT a valid similarity shortcut?", "SSA~", ["AA", "SSS~", "SAS~"], ["The angle must be included."])

# ---------------- Skill 6: missing sides ----------------
S = 6
def mk_missing():
    k = R.choice([F(2), F(3, 2), F(5, 2), F(4, 3), F(3), F(5, 3)]); a, b = R.randint(3, 15), R.randint(3, 15); L1, L2 = R.sample(LET, 2)
    if R.random() < 0.5:
        B.sa(6, lv(), f"△{L1} ~ △{L2}. {L1[0]}{L1[1]} = {a}, {L2[0]}{L2[1]} = {nz(a * k)}, {L1[1]}{L1[2]} = {b}. Find {L2[1]}{L2[2]}.", nz(b * k), ["Set up a proportion of corresponding sides.", f"x = {nz(k)}·{b}."])
    else:
        B.mc(6, lv(), f"△{L1} ~ △{L2}. {L1[0]}{L1[1]} = {a}, {L2[0]}{L2[1]} = {nz(a * k)}, {L2[1]}{L2[2]} = {nz(b * k)}. Find {L1[1]}{L1[2]}.", str(b), [nz(b * k * k), nz(b * k / k + 1), nz(a * k)], ["Divide by the scale factor."], tags=["misconception"])
def mk_missing_alg():
    x = R.randint(2, 10); k = R.choice([2, 3]); a = R.randint(3, 9)
    c1 = R.randint(1, 4); k1 = R.randint(1, 8); side = c1 * x + k1
    B.sa(6, lv(), f"△ABC ~ △DEF with AB = {a}, DE = {a * k}, BC = {c1}x + {k1}, EF = {k * side}. Find x.", f"x = {x}", [f"Scale factor {k}.", f"{k}({c1}x + {k1}) = {k * side}."])
for k_, (sides, k) in enumerate([((6, 5, 4), F(3, 2)), ((5, 4, 3), F(5, 2))]):
    dg = sim_pair(f"s06-pair-{k_}", sides, k, unknown=("DEF", "CA"), show=(True, False))
    if k_ == 0: B.sa(S, "cp1", "△ABC ~ △DEF. DE = " + nz(sides[2] * k) + ". Find x (DF).", nz(sides[1] * k), ["Scale factor DE/AB.", "DF = k·AC."], diagram=dg, tags=["graph"])
    else: B.mc(S, "cp1", "△ABC ~ △DEF. EF = " + nz(sides[0] * k) + ". Find x (DF).", nz(sides[1] * k), [nz(sides[1] / k), nz(sides[1] + k), nz(sides[0] * k)], ["Scale factor EF/BC.", "DF = k·AC."], diagram=dg, tags=["graph"])

# ---------------- Skill 7: side-splitter ----------------
S = 7
for k_, (AD, DB, AE) in enumerate([(4, 6, 6), (6, 3, 8), (5, 10, 4)]):
    EC = F(AE * DB, AD)
    dg = splitter(f"s07-split-{k_}", AD, DB, AE, float(EC), lab=(str(AD), str(DB), str(AE), "x"))
    B.orq(S, "cp1", "In the figure, DE ∥ BC.", [("Write a proportion.", f"{AD}/{DB} = {AE}/x"), ("Find x.", nz(EC)), ("Find AC.", nz(AE + EC)), ("Which theorem did you use?", "Triangle Proportionality Theorem (Side-Splitter)")], ["AD/DB = AE/EC.", "Cross-multiply.", "AE + EC.", "A line parallel to one side divides the other two proportionally."], diagram=dg, tags=["graph"])
def mk_split():
    AD, DB = R.randint(2, 12), R.randint(2, 12); AE = R.randint(2, 15); EC = F(AE * DB, AD)
    if R.random() < 0.5:
        B.sa(7, lv(), f"In △ABC, DE ∥ BC with D on AB, E on AC. AD = {AD}, DB = {DB}, AE = {AE}. Find EC.", nz(EC), ["AD/DB = AE/EC."])
    else:
        ok = R.random() < 0.5; EC2 = EC if ok else EC + 1
        B.mc(7, lv(), f"D is on AB and E on AC with AD = {AD}, DB = {DB}, AE = {AE}, EC = {nz(EC2)}. Is DE ∥ BC?", "Yes" if ok else "No", ["No" if ok else "Yes", "Only if D and E are midpoints", "Cannot tell"], ["Converse of the Triangle Proportionality Theorem: check AD/DB = AE/EC.", f"{nz(F(AD, DB))} vs {nz(AE / EC2)}."])
def mk_split_alg():
    x = R.randint(2, 9); AD = R.randint(2, 8); DB = R.randint(2, 8); AE = AD * x; EC_ = DB * x
    c1 = R.randint(1, 3); k1 = AE - c1 * x
    B.sa(7, lv(), f"DE ∥ BC in △ABC. AD = {AD}, DB = {DB}, AE = {c1}x {'+' if k1 >= 0 else '-'} {abs(k1)}, EC = {EC_}. Find x.", f"x = {x}", ["AD/DB = AE/EC.", "Cross-multiply and solve."])
    assert F(AD, DB) == F(c1 * x + k1, EC_)
def mk_three_par():
    a, b = R.randint(2, 10), R.randint(2, 10); c = R.randint(2, 15)
    B.mc(7, lv(), f"Three parallel lines cut two transversals. On the first, the segments are {a} and {b}; on the second, the first segment is {c}. Find the second.", nz(F(b * c, a)), [nz(F(a * c, b)), nz(c + b - a) if c + b - a > 0 else nz(F(c, 2)), nz(F(a * b, c))], ["Parallel lines divide transversals proportionally."])

# ---------------- Skill 8: indirect measurement ----------------
S = 8
fg = Fig(5.0, 2.8); fg.seg((0, 0), (9, 0)); fg.seg((1, 0), (1, 1.2)); fg.seg((1, 1.2), (2.8, 0), ls="--", lw=1); fg.seg((5, 0), (5, 3.5)); fg.seg((5, 3.5), (9, 0), ls="--", lw=1)
fg.side((1, 0), (1, 1.2), "6 ft", center=(2, 0.5)); fg.side((1, 0), (2.8, 0), "4 ft", center=(1.5, 1)); fg.side((5, 0), (5, 3.5), "x", center=(6, 1)); fg.side((5, 0), (9, 0), "30 ft", center=(6, 2))
dg = fg.save(B, "s08-shadow", "A 6-ft person casts a 4-ft shadow; a tree of height x casts a 30-ft shadow; dashed sun rays are parallel.", schematic=True)
B.orq(S, "cp1", "Use the figure: the sun's rays are parallel.", [("Why are the triangles similar?", "AA: both have right angles and the sun's angle is the same"), ("Write a proportion.", "6/4 = x/30"), ("Find the tree's height.", "45 ft"), ("What assumption is made about the ground?", "it is level (both stand vertically on flat ground)")], ["Right angles and equal angles of elevation.", "height/shadow.", "x = 45.", "Vertical objects on level ground."], diagram=dg, tags=["modeling", "graph"])
def mk_shadow():
    h, s1 = R.randint(4, 7), R.randint(2, 9); S2 = R.randint(10, 60)
    B.sa(8, lv(), f"A {h}-ft post casts a {s1}-ft shadow. At the same time a building casts a {S2}-ft shadow. How tall is the building?", f"{nz(F(h * S2, s1))} ft", ["height/shadow ratios are equal (similar triangles)."], tags=["modeling"])
def mk_map():
    sc = R.choice([25, 50, 80, 100, 250]); d = R.choice([F(3, 2), F(4), F(7, 2), F(6), F(5, 4)])
    if R.random() < 0.5:
        B.mc(8, lv(), f"On a map, 1 cm represents {sc} km. Two cities are {nz(d)} cm apart. How far apart are they?", f"{nz(d * sc)} km", [f"{nz(d + sc)} km", f"{nz(F(sc) / d)} km", f"{nz(d * sc / 10)} km"], ["Multiply by the scale."], tags=["modeling"])
    else:
        real = R.randint(10, 90)
        B.sa(8, lv(), f"A scale drawing uses 1 in = 4 ft. A wall is {real} ft long. How long is it on the drawing?", f"{nz(F(real, 4))} in", ["Divide by 4."], tags=["modeling"])
def mk_mirror():
    eye = R.choice([5, F(11, 2), 6, F(9, 2)]); d1 = R.randint(2, 6); d2 = R.randint(10, 50)
    B.sa(8, lv(), f"A person whose eyes are {nz(eye)} ft high stands {d1} ft from a mirror on the ground and sees the top of a flagpole {d2} ft beyond the mirror. How tall is the flagpole?", f"{nz(F(eye) * d2 / d1)} ft", ["Angles of incidence and reflection are equal → similar right triangles.", f"{nz(eye)}/{d1} = h/{d2}."], tags=["modeling"])
def mk_model():
    k = R.choice([12, 24, 48, 64, 87]); real = R.randint(20, 300)
    B.mc(8, lv(), f"A model is built at a scale of 1 : {k}. The real object is {real} ft long. How long is the model (in inches)?", f"{nz(F(real * 12, k))} in", [f"{nz(F(real, k))} in", f"{nz(F(real * k, 12))} in", f"{real * k} in"], ["Model length = real ÷ k; convert feet to inches."], tags=["modeling"])

# ---------------- Skill 9: similarity in right triangles ----------------
S = 9
a_, b_ = 9.0, 4.0  # hypotenuse segments DB and AD; altitude CD = √(ab) makes ∠ACB a right angle
H = (0, 0); Ap = (-b_, 0); Bp = (a_, 0); Cp = (0, (a_ * b_) ** 0.5)
fg = Fig(4.6, 2.8); fg.poly([Ap, Bp, Cp]); fg.seg(Cp, H, lw=1.2); fg.names([Ap, Bp, Cp], ["A", "B", "C"]); fg.text(H, "D", (0, -11)); fg.angle(Cp, Ap, Bp, right=True, r=0.8); fg.angle(H, Bp, Cp, right=True, r=0.7)
fg.side(Ap, H, "4", center=Cp); fg.side(H, Bp, "9", center=Cp); fg.side(Cp, H, "h", center=Bp)
dg = fg.save(B, "s09-altitude", "Right triangle ABC with right angle at C and altitude CD to hypotenuse AB; AD = 4, DB = 9, CD = h.")
B.orq(S, "cp1", "In the figure, CD is the altitude to the hypotenuse.", [("Name the three similar triangles.", "△ACB ~ △ADC ~ △CDB"), ("Find h.", "6"), ("Find AC.", "2√13"), ("Find BC.", "3√13")], ["Altitude to the hypotenuse creates similar triangles.", "h² = 4·9.", "AC² = AD·AB = 4·13.", "BC² = DB·AB = 9·13."], diagram=dg, tags=["graph"])
def mk_geomean():
    a, b = R.choice([(2, 8), (3, 12), (4, 9), (1, 16), (5, 20), (2, 18), (3, 27), (4, 25), (6, 6), (2, 6), (3, 5)])
    g2 = a * b; g = rad(g2)
    if R.random() < 0.5:
        B.sa(9, lv(), f"Find the geometric mean of {a} and {b}.", g, ["√(ab)."])
    else:
        B.mc(9, lv(), f"The altitude to the hypotenuse of a right triangle divides it into segments of {a} and {b}. Find the altitude.", g, [rad(a + b), f"{nz(F(a + b, 2))}", rad(a * a + b * b)], ["Altitude = geometric mean of the segments."], tags=["misconception"])
def mk_leg():
    a, b = R.choice([(4, 5), (2, 6), (3, 9), (5, 4), (1, 8), (9, 7), (2, 16)]); hyp = a + b
    B.sa(9, lv(), f"In right △ABC (right angle at C), altitude CD meets AB with AD = {a} and DB = {b}. Find AC.", rad(a * hyp), ["Leg = geometric mean of the hypotenuse and the adjacent segment: AC² = AD·AB."])
def mk_rt_sel():
    a, b = R.choice([(4, 9), (1, 9), (3, 12), (2, 8)])
    st = {f"CD = {rad(a * b)}": True, f"AC = {rad(a * (a + b))}": True, f"BC = {rad(b * (a + b))}": True, f"CD = {nz(F(a + b, 2))}": F(a + b, 2) ** 2 == a * b, f"AB = {a * b}": a * b == a + b}
    B.sel(9, lv(), f"Right △ABC has right angle C and altitude CD with AD = {a}, DB = {b}. Select ALL true statements.", [k for k, t in st.items() if t], [k for k, t in st.items() if not t] + ["△ACD ≅ △CBD"], ["Geometric mean relationships."])

# ---------------- fill ----------------
makers = {1: [mk_prop, mk_prop_alg, mk_ratio_split, mk_rate, mk_prop_sel], 2: [mk_poly_sim, mk_sim_check, mk_sim_sel], 3: [mk_dil_pt, mk_dil_k, mk_dil_props, mk_dil_tri], 4: [mk_aa, mk_aa_reason, mk_aa_x],
          5: [mk_sss, mk_sas, mk_sas_sel], 6: [mk_missing, mk_missing_alg], 7: [mk_split, mk_split_alg, mk_three_par], 8: [mk_shadow, mk_map, mk_mirror, mk_model], 9: [mk_geomean, mk_leg, mk_rt_sel]}
for S_, ms in makers.items():
    fill(B, S_, 32, ms, R)

def mk_missing_orq():
    k = R.choice([F(2), F(3, 2), F(5, 2), F(3)]); s1 = sorted(R.sample(range(3, 14), 3))
    if s1[0] + s1[1] <= s1[2]: raise AssertionError
    B.orq(6, lv(), f"△ABC ~ △DEF with AB = {s1[0]}, BC = {s1[1]}, CA = {s1[2]}, and DE = {nz(s1[0] * k)}.", [("Find the scale factor.", nz(k)), ("Find EF.", nz(s1[1] * k)), ("Find FD.", nz(s1[2] * k)), ("Find the ratio of the areas.", nz(k * k))], ["DE/AB.", "k·BC.", "k·CA.", "Areas scale by k²."])
def mk_split_sel():
    AD, DB = R.randint(2, 9), R.randint(2, 9); AE = R.randint(2, 12); EC = F(AE * DB, AD)
    st = {f"EC = {nz(EC)}": True, f"AD/AB = AE/AC": True, f"DE/BC = {nz(F(AD, AD + DB))}": True, f"DE/BC = {nz(F(AD, DB))}": F(AD, DB) == F(AD, AD + DB), f"EC = {nz(F(AE * AD, DB))}": F(AE * AD, DB) == EC}
    B.sel(7, lv(), f"In △ABC, DE ∥ BC with AD = {AD}, DB = {DB}, AE = {AE}. Select ALL true statements.", [a for a, t in st.items() if t], [a for a, t in st.items() if not t] or ["DE = BC"], ["Side-Splitter and △ADE ~ △ABC."])
def mk_shadow_orq():
    h, s1, S2 = R.randint(4, 7), R.randint(2, 8), R.randint(12, 60); H = F(h * S2, s1)
    B.orq(8, lv(), f"A {h}-ft student casts a {s1}-ft shadow while a tower casts a {S2}-ft shadow.", [("Why are the triangles similar?", "AA: right angles and equal sun angles"), ("Write a proportion.", f"{h}/{s1} = x/{S2}"), ("Find the tower's height.", f"{nz(H)} ft"), ("How long is the tower's shadow when the student's is 3 ft?", f"{nz(F(3 * S2, s1))} ft")], ["AA.", "height/shadow.", "Solve.", "Shadows scale together."], tags=["modeling"])
for S_, ms in [(6, [mk_missing_orq]), (7, [mk_split_sel]), (8, [mk_shadow_orq]), (4, [mk_aa]), (5, [mk_sss])]:
    fill(B, S_, 36 if S_ in (6, 7, 8) else 34, ms, R)

if __name__ == "__main__":
    p = B.write(); print(p, len(B.qs))
    for k, v in B.counts().items(): print(k, {a: b for a, b in v.items() if a != "formats"}, v["formats"])
