"""Calculus Unit 4 — Applications of Derivatives (applications-derivatives)."""
from hslib import *
import ca_u02 as C2
import ca_u03 as C3

UNIT_ID = "applications-derivatives"
ABBR = "app"


def rr(f, lv=(0, 1, 2), tag="m"):
    g = reuse(f, lv, tag)
    g.__name__ = "cal_" + f.__name__ + tag
    return g


def cubic_from_crit(r, L):
    """f with f′ = c·3(x - p)(x - q), integer coefficients."""
    p, q = sorted(r.sample(range(-4, 5), 2))
    c = pick(r, [1, -1]) * (1 if L == 0 else pick(r, [1, 2]))
    fp = 3 * c * (x - p) * (x - q)
    f = sp.integrate(sp.expand(fp), x)
    need(all(v.is_Integer for v in sp.Poly(f, x).all_coeffs()[:-1]) or True)
    f = sp.expand(2 * f) if any(not v.is_Integer for v in sp.Poly(f, x).all_coeffs()) else f
    f = f + rint(r, -5, 5)
    fp = sp.diff(f, x)
    need(all(v.is_Integer for v in sp.Poly(f, x).all_coeffs()))
    return f, fp, p, q, c


# ============================================================== S1 Interpreting derivatives
@fam("012", mode="mc")
def s1_meaning(r, L):
    ctxs = [("C(x)", "the cost in dollars of producing x items", "dollars per item", "the cost increases by about ${v} for the next item when {a} items are produced"),
            ("P(t)", "a town's population t years after 2020", "people per year", "the population is changing at {v} people per year in year {a} after 2020"),
            ("V(t)", "the volume of water in a tank, in gallons, after t minutes", "gallons per minute", "the volume is changing at {v} gallons per minute at t = {a} minutes"),
            ("T(h)", "the temperature in °F at h hours after noon", "°F per hour", "the temperature is changing at {v} °F per hour at {a} hours after noon"),
            ("s(t)", "a car's distance in miles after t hours", "miles per hour", "the car's speed is {v} miles per hour at t = {a} hours")]
    fn, desc, unit, good_t = pick(r, ctxs)
    a, v = rint(r, 2, 40), rint(r, -30, 60, True)
    good = good_t.format(v=v, a=a)
    bad = [f"{fn[0]}({a}) = {v}, so the value of the quantity is {v} at {a}", f"the quantity changes by {v} {unit.split(' per ')[0]} over the whole interval from 0 to {a}", f"the average rate of change from 0 to {a} is {v} {unit}"]
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q(f"{fn} is {desc}. Interpret {fn[0]}′({a}) = {v}.", good, [f"{fn[0]}′ is an instantaneous rate of change in {unit}.", good + "."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


@fam("012")
def s1_value(r, L):
    a_, b_ = rint(r, 1, 4), rint(r, 10, 80)
    tt = rint(r, 1, 6)
    kind = pick(r, ["cost", "temp"])
    if kind == "cost":
        f = sp.Rational(a_, 100) * x ** 2 + b_ * x + rint(r, 200, 900)
        v = sp.diff(f, x).subs(x, tt * 10)
        return Q(f"C(x) = {T(f)} is the cost in dollars to produce x items. Find C′({tt * 10}) and include units.", f"{D(F(v.p, v.q))} dollars per item",
                 [f"C′(x) = {T(sp.diff(f, x))}.", f"C′({tt * 10}) = {D(F(v.p, v.q))}.", "Units: dollars per item."], [f"{D(F(f.subs(x, tt * 10).p, f.subs(x, tt * 10).q))} dollars", f"{D(F(v.p, v.q))} items per dollar", f"{D(F((f.subs(x, tt * 10) / (tt * 10)).p, (f.subs(x, tt * 10) / (tt * 10)).q)) if (f.subs(x, tt * 10) / (tt * 10)).q in (1, 2, 4, 5, 10, 20, 25, 50, 100) else b_} dollars per item"],
                 PY("value_units", code=f"diff(P('{T(f)}'), x).subs(x, {tt * 10})", unit="dollars per item"), why=["Evaluated C instead of C′", "Inverted the units", "Found the average cost"], tags=["modeling"])
    f = -a_ * t ** 2 + rint(r, 2, 12) * t + rint(r, 50, 80)
    v = sp.diff(f, t).subs(t, tt)
    return Q(f"The temperature h hours after noon is T(h) = {T(f.subs(t, x)).replace('x', 'h')} °F. Find T′({tt}) and include units.", f"{v} °F per hour", [f"T′(h) = {T(sp.diff(f, t).subs(t, x)).replace('x', 'h')}.", f"T′({tt}) = {v}.", "Units: °F per hour."],
             [f"{f.subs(t, tt)} °F", f"{v} hours per °F", f"{T(sp.Rational(f.subs(t, tt) - f.subs(t, 0), tt))} °F per hour"], PY("value_units", code=f"diff(P('{T(f)}'), t).subs(t, {tt})", unit="°F per hour"),
             why=["Evaluated T instead of T′", "Inverted the units", "Found the average rate from noon"], tags=["modeling"])


# ============================================================== S2 Critical points
@fam("012")
def s2_crit(r, L):
    f, fp, p, q, c = cubic_from_crit(r, L)
    ans = f"x = {p} or x = {q}"
    w = [f"x = {-p} or x = {-q}" if (p, q) != (-q, -p) else f"x = {p}", " or ".join(f"x = {T(v)}" for v in sorted(sp.solve(sp.diff(f, x, 2), x))) or "x = 0", f"x = {p} or x = {q} or x = 0" if 0 not in (p, q) else f"x = {p + q}"]
    need(ans not in w)
    return Q(f"Find the critical numbers of f(x) = {T(f)}.", ans, [f"f′(x) = {T(fp)}.", "Set f′(x) = 0 (f′ is defined everywhere).", ans + "."], w, H(f"solve(diff(P('{T(f)}'), x), x)", "set"),
             why=["Made sign errors when factoring", "Set f″ = 0 instead", "Added x = 0 without reason"])


@fam("12")
def s2_classify(r, L):
    f, fp, p, q, c = cubic_from_crit(r, L)
    v = pick(r, [p, q])
    f2 = sp.diff(f, x, 2).subs(x, v)
    kind = "relative maximum" if f2 < 0 else "relative minimum"
    opts = [(o, o == kind) for o in ["relative maximum", "relative minimum", "neither", "point of inflection"]]
    return Q(f"f(x) = {T(f)} has a critical number at x = {v}. Use the second derivative test to classify it.", kind, [f"f″(x) = {T(sp.diff(f, x, 2))}.", f"f″({v}) = {f2}.", f"f″ {'<' if f2 < 0 else '>'} 0, so a {kind}."],
             options=opts, chk=PY("classify_crit", f=T(f), a=v), mode="mc")


# ============================================================== S3 Increasing / decreasing
@fam("012")
def s3_intervals(r, L):
    f, fp, p, q, c = cubic_from_crit(r, L)
    ask = pick(r, ["inc", "dec"])
    out, mid = f"(-∞, {p}) ∪ ({q}, ∞)", f"({p}, {q})"
    pos_out = c > 0
    ans = (out if pos_out else mid) if ask == "inc" else (mid if pos_out else out)
    other = mid if ans == out else out
    return Q(f"On what interval(s) is f(x) = {T(f)} {'increasing' if ask == 'inc' else 'decreasing'}?", ans, [f"f′(x) = {T(fp)} = {T(sp.factor(fp))}.", "Make a sign chart using the critical numbers.", f"f is {'increasing' if ask == 'inc' else 'decreasing'} where f′ is {'positive' if ask == 'inc' else 'negative'}: {ans}."],
             [other, f"({p}, ∞)", f"(-∞, {q})"], H(f"ineq_set('{T(fp)} {'>' if ask == 'inc' else '<'} 0')", "interval"), why=["Reversed the sign chart", "Used only one critical number", "Used only one critical number"])


# ============================================================== S4 Extrema
@fam("012")
def s4_absolute(r, L):
    f, fp, p, q, c = cubic_from_crit(r, L)
    a, b = p - rint(r, 0, 2), q + rint(r, 0, 2)
    if L == 0:
        a, b = p - 1, q + 1
    ask = pick(r, ["max", "min"])
    cands = {v: f.subs(x, v) for v in {a, b, p, q}}
    best = max(cands.values()) if ask == "max" else min(cands.values())
    at = sorted(v for v, w in cands.items() if w == best)
    need(len(at) == 1)
    ans = f"{best} at x = {at[0]}"
    other = min(cands.values()) if ask == "max" else max(cands.values())
    loc = f.subs(x, p if (c > 0) == (ask == "max") else q)
    w = [f"{other} at x = {[v for v, w_ in cands.items() if w_ == other][0]}", f"{loc} at x = {p if (c > 0) == (ask == 'max') else q}" if loc != best else f"{best} at x = {at[0] + 1}", f"{best + 1} at x = {at[0]}"]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Find the absolute {'maximum' if ask == 'max' else 'minimum'} of f(x) = {T(f)} on [{a}, {b}]. Give the value and where it occurs.", ans,
             [f"Critical numbers: {p}, {q}.", "Evaluate f at the critical numbers and the endpoints: " + ", ".join(f"f({v}) = {w_}" for v, w_ in sorted(cands.items())) + ".", f"Absolute {'max' if ask == 'max' else 'min'}: {ans}."],
             w, PY("abs_ext", f=T(f), a=a, b=b, ask=ask), why=["Found the other extreme", "Ignored the endpoints", "Made an arithmetic error"])


# ============================================================== S5 Concavity and inflection
@fam("012")
def s5_concave(r, L):
    if L < 2:
        f, fp, p, q, c = cubic_from_crit(r, L)
        f2 = sp.diff(f, x, 2)
        ip = sp.solve(f2, x)[0]
        ask = pick(r, ["ip", "up"])
    else:
        a_, b_ = r.sample(range(-3, 4), 2)
        f2 = 12 * (x - a_) * (x - b_)
        f = sp.integrate(sp.integrate(sp.expand(f2), x), x) + rint(r, -4, 4) * x
        need(all(v.is_Integer for v in sp.Poly(f, x).all_coeffs()))
        ask = pick(r, ["ip2", "up2"])
    if ask == "ip":
        ans = f"x = {T(ip)}"
        return Q(f"Find the x-coordinate of the inflection point of f(x) = {T(f)}.", ans, [f"f″(x) = {T(f2)}.", "Set f″ = 0; f″ changes sign there.", ans + "."],
                 [f"x = {p}", f"x = {T(-ip)}" if ip else "x = 1", f"x = {q}"], H(f"solve(diff(P('{T(f)}'), x, 2), x)[0]"), why=["Gave a critical number", "Made a sign error", "Gave a critical number"])
    if ask == "up":
        up = f"({T(ip)}, ∞)" if sp.Poly(f2, x).LC() > 0 else f"(-∞, {T(ip)})"
        dn = f"(-∞, {T(ip)})" if up.startswith("(" + T(ip)) else f"({T(ip)}, ∞)"
        return Q(f"On what interval is f(x) = {T(f)} concave up?", up, [f"f″(x) = {T(f2)}.", "Concave up where f″ > 0.", up + "."], [dn, f"({p}, {q})", f"(-∞, {p}) ∪ ({q}, ∞)"],
                 H(f"ineq_set('{T(f2)} > 0')", "interval"), why=["Reversed the sign of f″", "Used f′ instead of f″", "Used f′ instead of f″"])
    lo, hi = sorted([a_, b_])
    if ask == "ip2":
        ans = f"x = {lo} or x = {hi}"
        return Q(f"Find the x-coordinates of all inflection points of f(x) = {T(f)}.", ans, [f"f″(x) = {T(sp.expand(f2))} = 12(x - {a_})(x - {b_}).".replace("- -", "+ "), "f″ changes sign at both zeros.", ans + "."],
                 [f"x = {-lo} or x = {-hi}", f"x = {T(sp.Rational(lo + hi, 2))}", " or ".join(f"x = {T(v)}" for v in sorted(sp.solve(sp.diff(f, x), x), key=lambda z: complex(z).real) if v.is_real)[:60] or "x = 0"],
                 H(f"solve(diff(P('{T(f)}'), x, 2), x)", "set"), why=["Made sign errors", "Averaged the zeros", "Used f′ = 0"])
    ans = f"(-∞, {lo}) ∪ ({hi}, ∞)"
    return Q(f"On what interval(s) is f(x) = {T(f)} concave up?", ans, [f"f″(x) = {T(sp.expand(f2))}.", "f″ > 0 outside the zeros.", ans + "."], [f"({lo}, {hi})", f"({hi}, ∞)", f"(-∞, {lo})"],
             H(f"ineq_set('{T(sp.expand(f2))} > 0')", "interval"), why=["Reversed the sign chart", "Used only one zero", "Used only one zero"])


# ============================================================== S6 Related rates
@fam("012")
def s6_related(r, L):
    kind = pick(r, ["circle", "ladder", "sphere", "square"] if L < 2 else ["ladder", "cone", "sphere", "shadow"])
    if kind == "circle":
        rad, dr = rint(r, 2, 20), rint(r, 1, 6)
        v = 2 * sp.pi * rad * dr
        return Q(f"A circle's radius grows at {dr} cm/s. How fast is the area changing when the radius is {rad} cm? Give an exact answer.", f"{T(v)} cm²/s", ["A = πr².", "dA/dt = 2πr·dr/dt." if False else "A′ = 2πr·r′.", f"= 2π({rad})({dr}) = {T(v)} cm²/s."],
                 [f"{T(sp.pi * rad * rad * dr)} cm²/s", f"{T(2 * sp.pi * dr)} cm²/s", f"{T(sp.pi * rad * dr)} cm²/s"], H(f"diff(pi*r**2, r).subs(r, {rad})*{dr}"), why=["Multiplied the area by the rate", "Forgot to substitute r", "Forgot the 2"], tags=["modeling"])
    if kind == "square":
        s_, ds = rint(r, 2, 15), rint(r, 1, 5)
        v = 2 * s_ * ds
        return Q(f"Each side of a square increases at {ds} in/min. How fast is the area increasing when a side is {s_} in?", f"{v} in²/min", ["A = s².", "A′ = 2s·s′.", f"= 2({s_})({ds}) = {v} in²/min."],
                 [f"{s_ * s_ * ds} in²/min", f"{2 * ds} in²/min", f"{s_ * ds} in²/min"], H(f"2*{s_}*{ds}"), why=["Multiplied the area by the rate", "Forgot to substitute s", "Forgot the 2"], tags=["modeling"])
    if kind == "sphere":
        rad, dr = rint(r, 2, 12), rint(r, 1, 4)
        v = 4 * sp.pi * rad ** 2 * dr
        return Q(f"A balloon's radius increases at {dr} cm/s. How fast is its volume increasing when the radius is {rad} cm? Give an exact answer.", f"{T(v)} cm³/s", ["V = (4/3)πr³.", "V′ = 4πr²·r′.", f"= 4π({rad})²({dr}) = {T(v)} cm³/s."],
                 [f"{T(sp.Rational(4, 3) * sp.pi * rad ** 2 * dr)} cm³/s", f"{T(4 * sp.pi * rad * dr)} cm³/s", f"{T(sp.Rational(4, 3) * sp.pi * rad ** 3 * dr)} cm³/s"],
                 H(f"diff(Rational(4, 3)*pi*r**3, r).subs(r, {rad})*{dr}"), why=["Forgot to bring down the 3", "Used r instead of r²", "Multiplied the volume by the rate"], tags=["modeling"])
    if kind == "ladder":
        a_, b_, c_ = pick(r, [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (7, 24, 25)])
        dx = rint(r, 1, 4)
        v = -sp.Rational(a_ * dx, b_)
        return Q(f"A {c_}-ft ladder leans against a wall. The bottom slides away at {dx} ft/s. How fast is the top sliding down when the bottom is {a_} ft from the wall?", f"{T(abs(v))} ft/s",
                 [f"x² + y² = {c_}²; when x = {a_}, y = {b_}.", "2x·x′ + 2y·y′ = 0, so y′ = -x·x′ ÷ y.", f"y′ = -({a_})({dx}) ÷ {b_} = {T(v)}; it slides down at {T(abs(v))} ft/s."],
                 [f"{T(sp.Rational(b_ * dx, a_))} ft/s", f"{dx} ft/s", f"{T(sp.Rational(a_ * dx, c_))} ft/s"], PY("ladder", L=c_, x=a_, dx=dx), why=["Inverted the ratio x ÷ y", "Assumed the top moves at the same rate", "Divided by the ladder length"], tags=["modeling"])
    if kind == "cone":
        H_, R_ = pick(r, [(10, 5), (12, 4), (9, 3), (8, 4), (12, 6)])
        dV, hh = rint(r, 2, 10), rint(r, 2, H_ - 1)
        k_ = sp.Rational(R_, H_)
        v = dV / (sp.pi * k_ ** 2 * hh ** 2)
        return Q(f"Water pours into an inverted cone (height {H_} ft, top radius {R_} ft) at {dV} ft³/min. How fast is the water level rising when the water is {hh} ft deep? Give an exact answer.", f"{T(v)} ft/min",
                 [f"r = ({T(k_)})h, so V = (1/3)π({T(k_)})²h³.", f"V′ = π({T(k_)})²h²·h′.", f"h′ = {dV} ÷ (π·{T(k_ ** 2)}·{hh * hh}) = {T(v)} ft/min."],
                 [f"{T(dV / (sp.pi * k_ * hh ** 2))} ft/min", f"{T(3 * v)} ft/min", f"{T(dV / (sp.pi * hh ** 2))} ft/min"], PY("cone", H=H_, R=R_, dV=dV, h=hh), why=["Did not square the ratio r ÷ h", "Forgot the 1/3 cancels with 3", "Ignored the cone shape (used a cylinder)"], tags=["modeling"])
    ht, hp, sp_ = rint(r, 12, 20), rint(r, 5, 6), rint(r, 3, 6)
    v = sp.Rational(hp * sp_, ht - hp)
    return Q(f"A {hp}-ft person walks away from a {ht}-ft lamppost at {sp_} ft/s. How fast is the length of their shadow growing?", f"{T(v)} ft/s",
             [f"Similar triangles: {ht} ÷ (x + s) = {hp} ÷ s, so s = {hp}x ÷ {ht - hp}.", f"s′ = ({hp} ÷ {ht - hp})·x′.", f"s′ = {T(v)} ft/s."], [f"{T(sp.Rational(ht * sp_, ht - hp))} ft/s", f"{sp_} ft/s", f"{T(sp.Rational(hp * sp_, ht))} ft/s"],
             PY("shadow", H=ht, h=hp, v=sp_), why=["Found the rate of the shadow's tip", "Assumed the shadow grows at walking speed", "Used the wrong similar-triangle ratio"], tags=["modeling"])


# ============================================================== S7 Optimization
@fam("012")
def s7_opt(r, L):
    kind = pick(r, ["fence", "product"] if L == 0 else ["fence", "box", "river", "sum_sq"] if L == 1 else ["box", "river", "can", "dist"])
    if kind == "fence":
        P_ = rint(r, 10, 90) * 4
        v = (P_ // 4) ** 2
        return Q(f"A rectangle has perimeter {P_} m. What is the largest possible area?", f"{v} m²", [f"Perimeter: 2x + 2y = {P_}, so y = {P_ // 2} - x.", f"A = x({P_ // 2} - x); A′ = {P_ // 2} - 2x = 0 gives x = {P_ // 4}.", f"A = {v} m²."],
                 [f"{(P_ // 2) ** 2} m²", f"{P_ // 4} m²", f"{(P_ // 4) * (P_ // 4 + 2)} m²"], PY("opt", k="fence", P=P_), why=["Used half the perimeter squared", "Gave the side length", "Did not use a square"], tags=["modeling"])
    if kind == "product":
        s_ = rint(r, 6, 60) * 2
        return Q(f"Two positive numbers have sum {s_}. What is the largest possible product?", str((s_ // 2) ** 2), [f"P = x({s_} - x).", f"P′ = {s_} - 2x = 0, x = {s_ // 2}.", f"P = {(s_ // 2) ** 2}."],
                 [str(s_ * s_), str(s_ // 2), str((s_ // 2 - 1) * (s_ // 2 + 1))], PY("opt", k="product", S=s_), why=["Squared the sum", "Gave a number instead of the product", "Did not use equal numbers"], tags=["modeling"])
    if kind == "sum_sq":
        s_ = rint(r, 4, 40) * 2
        return Q(f"Two numbers have sum {s_}. What is the smallest possible value of the sum of their squares?", str(2 * (s_ // 2) ** 2), [f"S = x² + ({s_} - x)².", f"S′ = 4x - {2 * s_} = 0, x = {s_ // 2}.", f"S = {2 * (s_ // 2) ** 2}."],
                 [str((s_ // 2) ** 2), str(s_ * s_), str(s_ // 2)], PY("opt", k="sum_sq", S=s_), why=["Forgot to add both squares", "Squared the sum", "Gave a number instead of S"], tags=["modeling"])
    if kind == "river":
        A_ = rint(r, 2, 40) * 200
        xv = sp.sqrt(sp.Rational(A_, 2))
        need(xv.is_Integer)
        return Q(f"A farmer fences a rectangular area of {A_} ft² along a river (no fence on the river side). What is the least amount of fencing needed?", f"{T(4 * xv)} ft",
                 [f"Let x = side perpendicular to the river; the parallel side is {A_} ÷ x.", f"F = 2x + {A_} ÷ x; F′ = 2 - {A_} ÷ x² = 0, x = {T(xv)}.", f"F = {T(4 * xv)} ft."],
                 [f"{T(4 * sp.sqrt(A_))} ft", f"{T(2 * xv)} ft", f"{T(3 * xv)} ft"], PY("opt", k="river", A=A_), why=["Fenced all four sides of a square", "Gave a side length", "Counted the river side"], tags=["modeling"])
    if kind == "box":
        s_ = rint(r, 3, 12) * 6
        xv = sp.Rational(s_, 6)
        V = xv * (s_ - 2 * xv) ** 2
        return Q(f"Equal squares are cut from the corners of a {s_}-in by {s_}-in sheet, and the sides are folded up to make an open box. What cut size gives the largest volume, and what is that volume?", f"x = {T(xv)} in; V = {T(V)} in³",
                 [f"V = x({s_} - 2x)².", f"V′ = ({s_} - 2x)({s_} - 6x) = 0, so x = {T(xv)} (x = {s_ // 2} gives V = 0).", f"V = {T(V)} in³."],
                 [f"x = {s_ // 4} in; V = {T(sp.Rational(s_, 4) * (s_ - s_ // 2) ** 2)} in³", f"x = {s_ // 2} in; V = 0 in³", f"x = {T(xv)} in; V = {T(xv * (s_ - xv) ** 2)} in³"], PY("opt", k="box", S=s_),
                 why=["Guessed a quarter of the side", "Used the endpoint that gives zero volume", "Subtracted only one cut from each side"], tags=["modeling"], mode="sa")
    if kind == "can":
        Vv = pick(r, [16, 54, 128, 250, 432])
        rv = sp.cbrt(sp.Rational(Vv, 2))
        need(rv.is_Integer)
        hv = 2 * rv
        return Q(f"A closed cylindrical can must hold {Vv}π in³. What radius minimizes the surface area?", f"{T(rv)} in", [f"h = {Vv} ÷ r².", f"S = 2πr² + 2πrh = 2πr² + {2 * Vv}π ÷ r.", f"S′ = 4πr - {2 * Vv}π ÷ r² = 0, r³ = {Vv // 2}, r = {T(rv)} in."],
                 [f"{T(hv)} in", f"{T(sp.cbrt(Vv))} in", f"{T(sp.sqrt(Vv))} in"], PY("opt", k="can", V=Vv), why=["Gave the height", "Solved r³ = V", "Used a square root"], tags=["modeling"])
    px = rint(r, 2, 9)
    xv = sp.Rational(2 * px - 1, 2)
    d = sp.sqrt((xv - px) ** 2 + xv)
    return Q(f"Find the point on the curve y = √x closest to ({px}, 0).", f"({T(xv)}, {T(sp.sqrt(xv))})", [f"Minimize D² = (x - {px})² + x.", f"(D²)′ = 2(x - {px}) + 1 = 0, x = {T(xv)}.", f"Point: ({T(xv)}, {T(sp.sqrt(xv))})."],
             [f"({px}, {T(sp.sqrt(px))})", f"({T(sp.Rational(px, 2))}, {T(sp.sqrt(sp.Rational(px, 2)))})", f"(0, 0)"], PY("closest", a=px), why=["Used the point directly above", "Halved the x-coordinate", "Chose the origin"], tags=["modeling"])


# ============================================================== S8 Rectilinear motion
@fam("012")
def s8_motion(r, L):
    p, q = sorted(r.sample(range(1, 9), 2))
    c = rint(r, 1, 2)
    v = c * 3 * (t - p) * (t - q)
    s_ = sp.integrate(sp.expand(v), t) + rint(r, -5, 10)
    need(all(cf.is_Integer for cf in sp.Poly(s_, t).all_coeffs()))
    ask = pick(r, ["rest", "vel", "acc"] if L == 0 else ["rest", "left", "speedup"] if L == 1 else ["speedup", "left", "acc"])
    st = f"A particle moves along a line with position s(t) = {T(s_)} for t ≥ 0."
    if ask == "rest":
        ans = f"t = {p} or t = {q}"
        return Q(st + " When is the particle at rest?", ans, [f"v(t) = s′(t) = {T(sp.expand(v))}.", "At rest when v(t) = 0.", ans + "."], [f"t = {T(sp.Rational(p + q, 2))}", f"t = 0", f"t = {p}"],
                 H(f"solve(diff(P('{T(s_)}'), t), t)", "set"), why=["Set a(t) = 0", "Set s(t) = s(0)", "Missed a time"], tags=["modeling"])
    if ask == "vel":
        tt = rint(r, 0, 9)
        return Q(st + f" Find the velocity at t = {tt}.", str(v.subs(t, tt)), [f"v(t) = {T(sp.expand(v))}.", f"v({tt}) = {v.subs(t, tt)}."], [str(s_.subs(t, tt)), str(sp.diff(v, t).subs(t, tt)), str(-v.subs(t, tt)) if v.subs(t, tt) else "1"],
                 H(f"diff(P('{T(s_)}'), t).subs(t, {tt})"), why=["Gave the position", "Gave the acceleration", "Made a sign error"], tags=["modeling"])
    if ask == "acc":
        tt = rint(r, 0, 9)
        a_ = sp.diff(v, t).subs(t, tt)
        return Q(st + f" Find the acceleration at t = {tt}.", str(a_), [f"a(t) = s″(t) = {T(sp.diff(v, t))}.", f"a({tt}) = {a_}."], [str(v.subs(t, tt)), str(s_.subs(t, tt)), str(sp.diff(v, t, 2) * tt)],
                 H(f"diff(P('{T(s_)}'), t, 2).subs(t, {tt})"), why=["Gave the velocity", "Gave the position", "Differentiated three times"], tags=["modeling"])
    if ask == "left":
        ans = f"({p}, {q})"
        return Q(st + " On what time interval is the particle moving left (velocity negative)?", ans, [f"v(t) = {T(sp.expand(v))} = {3 * c}(t - {p})(t - {q}).", "v < 0 between the zeros.", ans + "."],
                 [f"[0, {p}) ∪ ({q}, ∞)", f"({T(sp.Rational(p + q, 2))}, ∞)", f"(0, {q})"], PY("motion_int", s=T(s_), ask="left"), why=["Reversed the sign chart", "Used where a(t) > 0", "Ignored the first zero"], tags=["modeling"])
    m = sp.Rational(p + q, 2)
    ans = f"({p}, {T(m)}) ∪ ({q}, ∞)"
    return Q(st + " On what time interval(s) is the particle speeding up?", ans, [f"v(t) = {3 * c}(t - {p})(t - {q}); a(t) = {T(sp.diff(v, t))}.", "Speeding up when v and a have the same sign.", f"Same sign on {ans}."],
             [f"({T(m)}, ∞)", f"({p}, {q})", f"[0, {p}) ∪ ({T(m)}, {q})"], PY("motion_int", s=T(s_), ask="speedup"), why=["Used only a(t) > 0", "Used only v(t) < 0", "Chose where v and a have opposite signs"], tags=["modeling"])


# ============================================================== S9 Rates of change in context
@fam("012")
def s9_rates(r, L):
    kind = pick(r, ["avg_inst", "marginal", "growth"])
    if kind == "avg_inst":
        a_ = rint(r, 1, 4)
        f = a_ * t ** 2 + rint(r, 1, 9) * t
        t1, t2 = sorted(r.sample(range(0, 8), 2))
        ask = pick(r, ["avg", "inst"])
        if ask == "avg":
            v = sp.Rational(f.subs(t, t2) - f.subs(t, t1), t2 - t1)
            return Q(f"A tank holds V(t) = {T(f)} liters after t minutes. Find the average rate of change of V from t = {t1} to t = {t2}, in liters per minute.", f"{T(v)} L/min",
                     [f"(V({t2}) - V({t1})) ÷ ({t2} - {t1}).", f"= ({f.subs(t, t2)} - {f.subs(t, t1)}) ÷ {t2 - t1} = {T(v)}."], [f"{T(sp.diff(f, t).subs(t, t2))} L/min", f"{f.subs(t, t2) - f.subs(t, t1)} L/min", f"{T(sp.diff(f, t).subs(t, t1))} L/min"],
                     H(f"(P('{T(f)}').subs(t, {t2}) - P('{T(f)}').subs(t, {t1}))/({t2} - {t1})"), why=["Found the instantaneous rate at the end", "Forgot to divide by the time", "Found the instantaneous rate at the start"], tags=["modeling"])
        return Q(f"A tank holds V(t) = {T(f)} liters after t minutes. Find the instantaneous rate of change of V at t = {t2}.", f"{sp.diff(f, t).subs(t, t2)} L/min", [f"V′(t) = {T(sp.diff(f, t))}.", f"V′({t2}) = {sp.diff(f, t).subs(t, t2)} L/min."],
                 [f"{f.subs(t, t2)} L/min", f"{T(sp.Rational(f.subs(t, t2), t2)) if t2 else 1} L/min", f"{sp.diff(f, t, 2)} L/min"], H(f"diff(P('{T(f)}'), t).subs(t, {t2})"), why=["Gave V instead of V′", "Found the average rate from 0", "Used V″"], tags=["modeling"])
    if kind == "marginal":
        p0, k_ = rint(r, 40, 120), rint(r, 1, 5)
        R = p0 * x - sp.Rational(k_, 10) * x ** 2
        q_ = rint(r, 2, 30) * 10
        need(sp.diff(R, x).subs(x, q_) != 0)
        v = sp.diff(R, x).subs(x, q_)
        return Q(f"Revenue from selling x items is R(x) = {T(R)} dollars. Find the marginal revenue R′({q_}) and interpret its sign.", f"{T(v)} dollars per item; revenue is {'increasing' if v > 0 else 'decreasing'}",
                 [f"R′(x) = {T(sp.diff(R, x))}.", f"R′({q_}) = {T(v)}.", f"R′ {'>' if v > 0 else '<'} 0, so revenue is {'increasing' if v > 0 else 'decreasing'} at that level."],
                 [f"{T(R.subs(x, q_))} dollars per item; revenue is increasing", f"{T(v)} dollars per item; revenue is {'decreasing' if v > 0 else 'increasing'}", f"{T(-v)} dollars per item; revenue is {'decreasing' if v > 0 else 'increasing'}"],
                 PY("marginal", R=T(R), q=q_), why=["Evaluated R instead of R′", "Misread the sign", "Made a sign error"], tags=["modeling"], mode="sa")
    P0, k_ = rint(r, 100, 900), pick(r, [sp.Rational(1, 50), sp.Rational(1, 20), sp.Rational(3, 100), sp.Rational(1, 25)])
    tt = rint(r, 1, 20)
    v = P0 * k_ * sp.exp(k_ * tt)
    return Q(f"A population is P(t) = {P0}e^({D(F(k_.p, k_.q))}t). How fast is it growing at t = {tt}? Round to the nearest tenth.", f"{Rd(float(v), 1)} per unit time" if False else Rd(float(v), 1),
             [f"P′(t) = {T(P0 * k_)}e^({D(F(k_.p, k_.q))}t).", f"P′({tt}) ≈ {Rd(float(v), 1)}."], [Rd(float(P0 * sp.exp(k_ * tt)), 1), Rd(float(P0 * k_), 1), Rd(float(P0 * k_ * tt), 1)],
             H(f"diff(P('{P0}e^({D(F(k_.p, k_.q))}t)'), t).subs(t, {tt})", "round", places=1), why=["Gave P instead of P′", "Forgot the exponential factor", "Treated the growth as linear"], tags=["modeling"])


# ============================================================== S10 Mean Value Theorem
@fam("012")
def s10_mvt(r, L):
    if L == 0:
        a_, b_ = rint(r, -3, 3, True), rint(r, -6, 6)
        f = a_ * x ** 2 + b_ * x + rint(r, -5, 5)
        lo, hi = sorted(r.sample(range(-4, 7), 2))
        c = sp.Rational(lo + hi, 2)
    else:
        f = x ** 3 + rint(r, -3, 3) * x
        lo, hi = 0, rint(r, 1, 4) * pick(r, [1, 3])
        ms = sp.Rational(f.subs(x, hi) - f.subs(x, lo), hi - lo)
        cs = [v for v in sp.solve(sp.diff(f, x) - ms, x) if v.is_real and lo < v < hi]
        need(len(cs) == 1)
        c = cs[0]
    ms = sp.Rational(f.subs(x, hi) - f.subs(x, lo), hi - lo)
    ans = f"c = {T(c)}"
    return Q(f"Find the value of c guaranteed by the Mean Value Theorem for f(x) = {T(f)} on [{lo}, {hi}].", ans, [f"Average rate: (f({hi}) - f({lo})) ÷ ({hi} - {lo}) = {T(ms)}.", f"Solve f′(c) = {T(ms)}.", f"{ans} (in the open interval)."],
             [f"c = {T(ms)}", f"c = {T(-c) if c else 1}", f"c = {T(sp.Rational(hi - lo, 2))}" if sp.Rational(hi - lo, 2) != c else f"c = {T(c + 1)}"], PY("mvt", f=T(f), a=lo, b=hi),
             why=["Gave the average rate instead of c", "Made a sign error", "Used half the interval length"])


@fam("012", mode="mc")
def s10_hyp(r, L):
    a, b = sorted(r.sample(range(-4, 6), 2))
    items = [(f"f(x) = |x| on [{min(a, -1)}, {max(b, 1)}]", "No: f is not differentiable at x = 0"), (f"f(x) = 1/x on [{min(a, -1)}, {max(b, 1)}]", "No: f is not continuous at x = 0"),
             (f"f(x) = x² on [{a}, {b}]", "Yes: f is continuous on the closed interval and differentiable on the open interval"),
             (f"f(x) = √x on [0, {max(b, 1)}]", "Yes: f is continuous on the closed interval and differentiable on the open interval")]
    st, good = pick(r, items)
    opts = [(o, o == good) for o in ["Yes: f is continuous on the closed interval and differentiable on the open interval", "No: f is not differentiable at x = 0", "No: f is not continuous at x = 0", "No: f(a) must equal f(b)"]]
    return Q(f"Does the Mean Value Theorem apply to {st}?", good, ["MVT needs continuity on [a, b] and differentiability on (a, b).", good + "."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


SKILLS = {
    1: dict(name="Interpreting Derivatives in Context", std=["AP CHA-3.A"], fams=[s1_meaning, s1_value], extra=[err_of(s1_value), open_of(s1_value)]),
    2: dict(name="Analyzing Function Behavior with Derivatives", std=["AP FUN-4.A"], fams=[s2_crit, s2_classify], extra=[err_of(s2_crit), open_of(s2_crit)]),
    3: dict(name="Increasing and Decreasing Intervals", std=["AP FUN-4.A"], fams=[s3_intervals], extra=[err_of(s3_intervals), open_of(s3_intervals)]),
    4: dict(name="Relative and Absolute Extrema", std=["AP FUN-4.A"], fams=[s4_absolute, s2_classify], extra=[err_of(s4_absolute), open_of(s4_absolute)]),
    5: dict(name="Concavity and Inflection Points", std=["AP FUN-4.A"], fams=[s5_concave], extra=[err_of(s5_concave), open_of(s5_concave)]),
    6: dict(name="Related Rates", std=["AP CHA-3.D", "AP CHA-3.E"], fams=[s6_related], extra=[err_of(s6_related), open_of(s6_related)]),
    7: dict(name="Optimization", std=["AP FUN-4.B", "AP FUN-4.C"], fams=[s7_opt], extra=[err_of(s7_opt), open_of(s7_opt)]),
    8: dict(name="Rectilinear Motion: Position, Velocity, and Acceleration", std=["AP CHA-3.B", "AP CHA-3.C"], fams=[s8_motion], extra=[err_of(s8_motion), open_of(s8_motion)]),
    9: dict(name="Rates of Change in Applied Contexts", std=["AP CHA-3.A", "AP CHA-1.A"], fams=[s9_rates], extra=[err_of(s9_rates), open_of(s9_rates)]),
    10: dict(name="The Mean Value Theorem", std=["AP FUN-1.B"], fams=[s10_mvt, s10_hyp], extra=[err_of(s10_mvt), open_of(s10_mvt)]),
    11: dict(name="Midterm Review", std=["AP LIM-1.E", "AP FUN-3.A", "AP FUN-4.A"], fams=[rr(C2.s3_algebra), rr(C3.s3_rule), rr(C3.s6_tangent), rr(s3_intervals), rr(s4_absolute)],
             extra=[err_of(rr(C3.s3_rule, tag="e")), open_of(rr(s2_crit, tag="o"))]),
}
