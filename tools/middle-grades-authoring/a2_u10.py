"""Algebra 2 Unit 10 — Trigonometric Functions (trigonometric-functions). Top-up families."""
from hslib import *
import math
import pc_u04 as P4

UNIT_ID = "trigonometric-functions"
ABBR = "tf"
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]
QUAD = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}
QWORD = {1: "Quadrant I", 2: "Quadrant II", 3: "Quadrant III", 4: "Quadrant IV"}


# ============================================================== S6 Trigonometric identities
@fam("012")
def s6_pyth(r, L):
    a, b, c = pick(r, TRIPLES)
    if r.random() < 0.5:
        a, b = b, a
    q = pick(r, [1, 2, 3, 4]) if L else pick(r, [1, 2])
    sx, sy = QUAD[q]
    cosv, sinv = sp.Rational(sx * a, c), sp.Rational(sy * b, c)
    given = pick(r, ["sin", "cos"])
    ask = pick(r, ["cos", "tan"] if given == "sin" else ["sin", "tan"])
    gv = sinv if given == "sin" else cosv
    want = {"sin": sinv, "cos": cosv, "tan": sinv / cosv}[ask]
    ans = T(want)
    wr = [T(-want), T(1 / want), T({"sin": cosv, "cos": sinv, "tan": cosv / sinv}[ask])]
    need(len(set(wr) | {ans}) == 4)
    return Q(f"If {given} θ = {T(gv)} and θ is in {QWORD[q]}, find {ask} θ.", ans,
             [f"Use sin²θ + cos²θ = 1: {'cos' if given == 'sin' else 'sin'}²θ = 1 - ({T(gv)})² = {T(1 - gv ** 2)}.",
              f"In {QWORD[q]}, cos θ is {'positive' if sx > 0 else 'negative'} and sin θ is {'positive' if sy > 0 else 'negative'}.", f"{ask} θ = {ans}."],
             wr, PY("trig_from", given=given, gv=str(gv), q=q, ask=ask),
             why=["Used the wrong sign for the quadrant", "Took the reciprocal", "Switched sine and cosine"])


@fam("012", mode="mc")
def s6_simplify(r, L):
    items = [("sin²θ + cos²θ", "1"), ("1 - sin²θ", "cos²θ"), ("1 - cos²θ", "sin²θ"), ("sin θ ÷ cos θ", "tan θ"), ("tan θ · cos θ", "sin θ"),
             ("(1 - cos²θ) ÷ sin θ", "sin θ"), ("cos²θ - 1", "-sin²θ"), ("sin²θ - 1", "-cos²θ"), ("(sin²θ + cos²θ) ÷ cos θ", "1 ÷ cos θ"), ("tan θ ÷ sin θ", "1 ÷ cos θ")]
    if L == 0:
        items = items[:5]
    e, v = pick(r, items)
    others = [w for w in ["1", "cos²θ", "sin²θ", "tan θ", "sin θ", "-sin²θ", "-cos²θ", "1 ÷ cos θ", "cos θ", "0"] if w != v]
    r.shuffle(others)
    opts = [(v, True)] + [(o, False) for o in others[:3]]
    return Q(f"Simplify {e}.", v, ["Use sin²θ + cos²θ = 1 and tan θ = sin θ ÷ cos θ.", f"{e} = {v}."], options=opts, chk=PY("trig_ident", e=e), mode="mc")


# ============================================================== S9 Trigonometric modeling
@fam("012")
def s9_model(r, L):
    lo, hi = pick(r, [(2, 42), (5, 65), (3, 53), (10, 90), (1, 31), (4, 44)])
    per = pick(r, [8, 10, 12, 20, 24, 30])
    mid, amp = sp.Rational(lo + hi, 2), sp.Rational(hi - lo, 2)
    ctx = pick(r, ["A Ferris wheel seat's height", "The water depth at a pier", "A buoy's height above the sea floor"])
    unit = "feet"
    tunit = "seconds" if "Ferris" in ctx else "hours"
    ask = pick(r, ["amp", "mid", "per"] if L < 2 else ["amp", "mid", "b"])
    q0 = f"{ctx} varies sinusoidally between {lo} and {hi} {unit}, repeating every {per} {tunit}."
    if ask == "amp":
        return Q(q0 + " What is the amplitude of the model?", f"{T(amp)} {unit}", ["Amplitude = (max - min) ÷ 2.", f"({hi} - {lo}) ÷ 2 = {T(amp)}."],
                 [f"{hi - lo} {unit}", f"{T(mid)} {unit}", f"{per} {unit}"], H(f"Rational({hi} - {lo}, 2)"), why=["Forgot to divide by 2", "Gave the midline value", "Used the period"], tags=["modeling"])
    if ask == "mid":
        return Q(q0 + " What is the equation of the midline?", f"y = {T(mid)}", ["Midline = (max + min) ÷ 2.", f"({hi} + {lo}) ÷ 2 = {T(mid)}."],
                 [f"y = {T(amp)}", f"y = {hi + lo}", f"y = {T(sp.Rational(per, 2))}"], H(f"y - Rational({hi} + {lo}, 2)", "eqn"), why=["Gave the amplitude", "Forgot to divide by 2", "Used half the period"], tags=["modeling"])
    if ask == "per":
        return Q(q0 + " What is the period of the model?", f"{per} {tunit}", ["The period is the time for one full cycle.", f"The pattern repeats every {per} {tunit}."],
                 [f"{per // 2} {tunit}", f"{T(amp)} {tunit}", f"{per * 2} {tunit}"], H(f"{per}"), why=["Used half a cycle", "Gave the amplitude", "Doubled the period"], tags=["modeling"])
    b = 2 * sp.pi / per
    return Q(q0 + f" In a model y = a cos(bt) + d with t in {tunit}, what is b?", T(b), ["b = 2π ÷ period.", f"b = 2π ÷ {per} = {T(b)}."],
             [T(sp.Rational(per, 2) * sp.pi) if False else T(per * sp.pi / 2), T(sp.Rational(1, per)), T(sp.pi / per)], H(f"2*pi/{per}"),
             why=["Divided the period by 2π", "Used 1 over the period", "Used π instead of 2π"], tags=["modeling"])


VALS = {"sin": [(sp.Rational(1, 2), "1/2"), (sp.sqrt(2) / 2, "(√2)/2"), (sp.sqrt(3) / 2, "(√3)/2"), (1, "1"), (0, "0"), (-1, "-1"), (-sp.Rational(1, 2), "-1/2"), (-sp.sqrt(2) / 2, "-(√2)/2"), (-sp.sqrt(3) / 2, "-(√3)/2")],
        "cos": [(sp.Rational(1, 2), "1/2"), (sp.sqrt(2) / 2, "(√2)/2"), (sp.sqrt(3) / 2, "(√3)/2"), (1, "1"), (0, "0"), (-1, "-1"), (-sp.Rational(1, 2), "-1/2"), (-sp.sqrt(2) / 2, "-(√2)/2"), (-sp.sqrt(3) / 2, "-(√3)/2")],
        "tan": [(1, "1"), (-1, "-1"), (sp.sqrt(3), "√3"), (-sp.sqrt(3), "-√3"), (sp.sqrt(3) / 3, "(√3)/3"), (0, "0")]}


@fam("012")
def s7_basic(r, L):
    fn = pick(r, ["sin", "cos", "tan"] if L else ["sin", "cos"])
    v, vt = pick(r, VALS[fn])
    k_ = 1 if L < 2 else pick(r, [1, 2, 3])
    deg = L == 0
    F_ = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[fn]
    sols = sorted(sp.solveset(sp.Eq(F_(x), v), x, sp.Interval.Ropen(0, 2 * sp.pi)), key=float)
    fmt_ = (lambda a: f"{T(a * 180 / sp.pi)}°") if deg else (lambda a: T(a))
    if k_ == 1:
        eq = f"{fn}(x) = {vt}" if deg else f"{fn} x = {vt}"
        lhs = f"{k_}"
    else:
        need(fn != "tan" or True)
        eq = f"{k_}{fn}(x) {'+' if v * 0 == 0 else ''} = {vt}"
    need(k_ == 1)
    eq = f"{fn}(x) = {vt}"
    dom = "0° ≤ x < 360°" if deg else "0 ≤ x < 2π"
    ans = " or ".join(f"x = {fmt_(s_)}" for s_ in sols)
    ref = sp.asin(abs(v)) if fn == "sin" else sp.acos(abs(v)) if fn == "cos" else sp.atan(abs(v))
    wr = [f"x = {fmt_(sols[0])}", " or ".join(f"x = {fmt_(s_)}" for s_ in sorted({ref, sp.pi - ref} if fn != "sin" else {ref, 2 * sp.pi - ref}, key=float)) if ref not in (0, sp.pi / 2) else f"x = {fmt_(sols[0] + sp.pi / 2)}",
          " or ".join(f"x = {fmt_(s_)}" for s_ in sorted({ref, ref + sp.pi}, key=float))]
    need(len(set(wr) | {ans}) == 4 and len(sols) >= 1)
    return Q(f"Solve {eq} for {dom}.", ans,
             [f"The reference angle is {fmt_(ref)}.", f"{fn} is {'positive' if v > 0 else 'negative' if v < 0 else 'zero'} in the quadrants that give {ans.replace(' or ', ', ')}.", f"{ans}."],
             wr, PY("trig_solutions", func=fn, v=vt, deg=deg), why=["Gave only one solution", "Used the quadrants for a different function", "Added π to the reference angle without checking the quadrants"])


rr = lambda f, lv=(0, 1, 1), tag="": reuse(f, lv, "a2" + tag)
SKILLS = {
    1: dict(name="Angles in degrees and radians", fams=[rr(P4.s3_convert), rr(P4.s3_coterminal)], extra=[err_of(rr(P4.s3_convert, tag="e")), err_of(rr(P4.s3_coterminal, tag="e")), open_of(rr(P4.s3_convert, tag="o"))]),
    2: dict(name="Unit circle coordinates", fams=[rr(P4.s1_point), rr(P4.s1_ref), rr(P4.s1_point, (1, 1, 2), "b"), rr(P4.s2_exact, tag="u")], extra=[err_of(rr(P4.s1_point, tag="e")), err_of(rr(P4.s1_ref, tag="e")), open_of(rr(P4.s1_point, tag="o"))]),
    3: dict(name="Sine, cosine, and tangent", fams=[rr(P4.s2_exact), rr(P4.s5_side), rr(P4.s5_angle)], extra=[err_of(rr(P4.s2_exact, tag="e")), err_of(rr(P4.s5_side, tag="e")), open_of(rr(P4.s2_exact, tag="o"))]),
    4: dict(name="Graphs of sine and cosine", fams=[rr(P4.s7_features), rr(P4.s7_graph), rr(P4.s8_graph)], extra=[err_of(rr(P4.s7_features, tag="e")), open_of(rr(P4.s7_features, tag="o"))]),
    5: dict(name="Amplitude, period, and phase shift", fams=[rr(P4.s6_ap), rr(P4.s8_write)], extra=[err_of(rr(P4.s6_ap, tag="e")), err_of(rr(P4.s8_write, tag="e")), open_of(rr(P4.s6_ap, tag="o"))]),
    6: dict(name="Trigonometric identities", fams=[s6_pyth, s6_simplify], extra=[err_of(s6_pyth), open_of(s6_pyth)]),
    7: dict(name="Solving trigonometric equations", fams=[rr(P4.s9_solve), s7_basic], extra=[err_of(rr(P4.s9_solve, tag="e")), err_of(s7_basic), open_of(s7_basic)]),
    8: dict(name="Inverse trigonometric functions", fams=[rr(P4.s10_inverse), rr(P4.s10_compose, (1, 1, 2))], extra=[err_of(rr(P4.s10_inverse, tag="e")), open_of(rr(P4.s10_inverse, tag="o"))]),
    9: dict(name="Trigonometric modeling", fams=[s9_model], extra=[err_of(s9_model), open_of(s9_model)]),
}
