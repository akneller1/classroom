"""Algebra 2 Unit 9 — Conic Sections (conic-sections). Top-up families (mostly the verified Precalculus conic families)."""
from hslib import *
import pc_u03 as C3

UNIT_ID = "conic-sections"
ABBR = "cs"


@fam("012")
def s6_circle_general(r, L):
    h_, k_ = rint(r, -7, 7), rint(r, -7, 7)
    rad = rint(r, 1, 9)
    need(h_ or k_)
    e = sp.expand((x - h_) ** 2 + (y - k_) ** 2 - rad ** 2)
    sq = C3.sq
    ans = f"{sq('x', h_)} + {sq('y', k_)} = {rad * rad}"
    wr = [f"{sq('x', -h_)} + {sq('y', -k_)} = {rad * rad}", f"{sq('x', h_)} + {sq('y', k_)} = {-e.subs({x: 0, y: 0})}" if -e.subs({x: 0, y: 0}) != rad * rad else f"{sq('x', h_)} + {sq('y', k_)} = {rad}",
          f"{sq('x', h_)} + {sq('y', k_)} = {rad}"]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Write {T(e)} = 0 in standard form by completing the square.", ans,
             ["Group the x-terms and the y-terms and move the constant to the right.", f"Complete each square: add {h_ * h_} and {k_ * k_} to both sides.", f"{ans}."],
             wr, H(f"P('{T(e)}')", "eqn"), why=["Used the wrong signs inside the squares", "Forgot to add the completing numbers to the right side", "Wrote r instead of r²"])


@fam("012")
def s6_circle_center(r, L):
    h_, k_ = rint(r, -8, 8), rint(r, -8, 8)
    rad = rint(r, 1, 10)
    need(h_ or k_)
    e = sp.expand((x - h_) ** 2 + (y - k_) ** 2 - rad ** 2)
    ask = pick(r, ["center", "radius"])
    if ask == "center":
        ans = f"({h_}, {k_})"
        wr = [f"({-h_}, {-k_})", f"({2 * h_}, {2 * k_})" if (h_, k_) != (0, 0) else "(1, 1)", f"({k_}, {h_})" if h_ != k_ else f"({h_}, {-k_})"]
        why = ["Used the opposite signs of the center", "Used the x- and y-coefficients without dividing by -2", "Switched the coordinates"]
        chk = PY("circle_part", e=T(e), part="center")
    else:
        ans = str(rad)
        wr = [str(rad * rad), str(-e.subs({x: 0, y: 0})) if -e.subs({x: 0, y: 0}) not in (rad, rad * rad) else str(rad + 1), str(rad * 2)]
        why = ["Gave r² instead of r", "Used the constant term without completing the square", "Doubled the radius"]
        chk = PY("circle_part", e=T(e), part="radius")
    need(len(set(wr) | {ans}) == 4)
    return Q(f"Find the {ask} of the circle {T(e)} = 0.", ans,
             ["Complete the square for x and for y.", f"(x - {h_})² + (y - {k_})² = {rad * rad}.".replace("- -", "+ "), f"The {ask} is {ans}."], wr, chk, why=why)


@fam("012", mode="sa")
def s7_classify(r, L):
    A_, C_ = pick(r, [(1, 1), (2, 3), (3, -2), (0, 4), (4, 0), (-5, 2), (5, 5), (1, 4), (9, 4), (-1, 1), (1, 0), (0, -3), (3, 3), (4, -9), (2, 2)])
    D_, E_, F_ = rint(r, -8, 8), rint(r, -8, 8), rint(r, -20, 20)
    if A_ == 0 or C_ == 0:
        need((A_ == 0 and D_ != 0) or (C_ == 0 and E_ != 0))
        typ = "parabola"
    elif A_ == C_:
        typ = "circle"
    elif A_ * C_ > 0:
        typ = "ellipse"
    else:
        typ = "hyperbola"
    e = A_ * x ** 2 + C_ * y ** 2 + D_ * x + E_ * y + F_
    others = [c_ for c_ in ["circle", "parabola", "ellipse", "hyperbola"] if c_ != typ]
    whys = {"circle": "Thought any equation with x² and y² is a circle", "parabola": "Looked only at the linear terms", "ellipse": "Ignored that the squared terms have opposite signs" if typ == "hyperbola" else "Thought unequal coefficients always give an ellipse",
            "hyperbola": "Thought different coefficients make a hyperbola"}
    return Q(f"Classify the conic {T(e)} = 0 as a circle, parabola, ellipse, or hyperbola. (Assume it is not degenerate.)", typ,
             ["Compare the coefficients of x² and y².", "Only one squared term: parabola. Equal coefficients: circle. Same sign: ellipse. Opposite signs: hyperbola.", f"It is a {typ}."],
             others, PY("conic_type", A=A_, C=C_), why=[whys[o] for o in others], mode="sa")


rr = lambda f, lv=(0, 1, 1), tag="": reuse(f, lv, "a2" + tag)
g01 = lambda f, tag="": reuse(f, (0, 1, 1), "a2" + tag)
SKILLS = {
    1: dict(name="Circles in standard form", fams=[rr(C3.s1_read), rr(C3.s1_write), rr(C3.s_short_circle)], extra=[err_of(rr(C3.s1_write, tag="e")), err_of(rr(C3.s1_read, tag="e")), open_of(rr(C3.s1_read, tag="o"))]),
    2: dict(name="Parabolas and focus-directrix form", fams=[rr(C3.s2_features), rr(C3.s2_write), rr(C3.s_short_parab)], extra=[err_of(rr(C3.s2_features, tag="e")), err_of(rr(C3.s2_write, tag="e")), open_of(rr(C3.s2_features, tag="o"))]),
    3: dict(name="Ellipses and their equations", fams=[rr(C3.s3_features), rr(C3.s4_write), rr(C3.s_short_ell)], extra=[err_of(rr(C3.s3_features, tag="e")), err_of(rr(C3.s4_write, tag="e")), open_of(rr(C3.s3_features, tag="o"))]),
    4: dict(name="Hyperbolas and their equations", fams=[rr(C3.s5_features), rr(C3.s6_write), rr(C3.s_short_hyp)], extra=[err_of(rr(C3.s5_features, tag="e")), err_of(rr(C3.s6_write, tag="e")), open_of(rr(C3.s5_features, tag="o"))]),
    5: dict(name="Graphing conic sections", fams=[g01(C3.s1_graph), g01(C3.s2_graph), g01(C3.s3_graph), g01(C3.s5_graph), rr(C3.s1_read, tag="g"), rr(C3.s3_features, tag="g"), rr(C3.s5_features, tag="g"), rr(C3.s2_features, tag="g")],
            extra=[err_of(rr(C3.s1_read, tag="e5")), err_of(rr(C3.s3_features, tag="e5")), open_of(rr(C3.s1_read, tag="o5"))]),
    6: dict(name="Converting equations to standard form", fams=[s6_circle_general, s6_circle_center, rr(C3.s2_general, (1, 1, 2))], extra=[err_of(s6_circle_general), err_of(s6_circle_center), open_of(s6_circle_center)]),
    7: dict(name="Identifying conics from equations", fams=[rr(C3.s6_classify, (0, 1, 2)), s7_classify], extra=[err_of(s7_classify), open_of(s7_classify)]),
}
