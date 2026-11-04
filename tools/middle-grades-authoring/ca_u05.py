"""Calculus Unit 5 — Antiderivatives and Definite Integrals (antiderivatives-definite-integrals)."""
from hslib import *

UNIT_ID = "antiderivatives-definite-integrals"
ABBR = "int"


def integ(f, a=None, b=None, var="x"):
    ft = T(f)
    body = f"({ft})" if (" " in ft and not (ft.startswith("(") and ft.endswith(")"))) else ft
    return f"∫ {body} d{var}" if a is None else f"∫ from {T(a)} to {T(b)} {body} d{var}"


def build_g(r, L):
    """An integrand with an elementary antiderivative."""
    kinds = {0: ["poly", "power"], 1: ["poly", "root", "trig", "exp", "recip"], 2: ["trig2", "exp2", "mixed", "root2", "sec2"]}[L]
    k_ = pick(r, kinds)
    a, b, c = rint(r, 1, 6), rint(r, -6, 6, True), rint(r, 2, 5)
    if k_ == "poly":
        f = polyx([rint(r, -4, 4, True) * 3, rint(r, -6, 6) * 2, rint(r, -9, 9)])
    elif k_ == "power":
        n_ = rint(r, 2, 6)
        f = (n_ + 1) * a * x ** n_ + b
    elif k_ == "root":
        f = 3 * a * sp.sqrt(x) + sp.Integer(b) / x ** 2
    elif k_ == "trig":
        f = a * sp.cos(x) + b * sp.sin(x)
    elif k_ == "exp":
        f = a * sp.exp(x) + c * x
    elif k_ == "recip":
        f = sp.Integer(a) / x + b
    elif k_ == "trig2":
        f = a * sp.cos(c * x)
    elif k_ == "exp2":
        f = sp.exp(b * x) * a * abs(b)
    elif k_ == "mixed":
        f = sp.Integer(a) / x + sp.exp(c * x) * c + sp.sin(x)
    elif k_ == "root2":
        f = sp.Integer(a) / sp.sqrt(x) + x ** 3
    else:
        f = a * sp.sec(x) ** 2 - sp.Integer(b) / x
    return f, k_


RULE = {"poly": "Power rule: ∫ xⁿ dx = xⁿ⁺¹ ÷ (n + 1) + C.", "power": "Power rule term by term.", "root": "Rewrite √x = x^(1/2) and 1 ÷ x² = x⁻²; use the power rule.", "trig": "∫ cos x dx = sin x + C, ∫ sin x dx = -cos x + C.",
        "exp": "∫ eˣ dx = eˣ + C.", "recip": "∫ (1 ÷ x) dx = ln|x| + C.", "trig2": "∫ cos(kx) dx = (1 ÷ k)sin(kx) + C.", "exp2": "∫ e^(kx) dx = (1 ÷ k)e^(kx) + C.", "mixed": "Integrate term by term.",
        "root2": "1 ÷ √x = x^(-1/2).", "sec2": "∫ sec² x dx = tan x + C; ∫ (1 ÷ x) dx = ln|x| + C."}


def anti_text(F_):
    s = T(sp.expand(F_) if not F_.has(sp.log) else F_)
    s = re.sub(r"ln\(x\)", "ln|x|", s)
    return s + " + C"


import re


# ============================================================== S1 Antidifferentiation as inverse
@fam("012")
def s1_particular(r, L):
    f, k_ = build_g(r, 0 if L < 2 else 1)
    need(k_ not in ("root", "recip"))
    a = pick(r, [0, 1]) if k_ != "root" else 1
    b = rint(r, -10, 10)
    F_ = sp.integrate(f, x)
    Cc = b - F_.subs(x, a)
    ans = "F(x) = " + T(sp.expand(F_ + Cc) if not F_.has(sp.exp, sp.sin, sp.cos) else F_ + Cc)
    return Q(f"Find F(x) if F′(x) = {T(f)} and F({a}) = {b}.", ans, [f"Antidifferentiate: F(x) = {T(F_)} + C.", f"F({a}) = {T(F_.subs(x, a))} + C = {b}, so C = {T(Cc)}.", ans + "."],
             ["F(x) = " + T(F_ + b), "F(x) = " + T(sp.diff(f, x) + b), "F(x) = " + T(F_ - Cc) if Cc else "F(x) = " + T(F_ + 1)], PY("particular", f=T(f), a=a, b=b),
             why=["Added the initial value instead of solving for C", "Differentiated instead of integrating", "Made a sign error solving for C"])


@fam("012", mode="mc")
def s1_which(r, L):
    f, k_ = build_g(r, L)
    F_ = sp.integrate(f, x)
    good = anti_text(F_ + rint(r, -9, 9)).replace(" + C", "")
    bad = [T(sp.diff(f, x)), T(sp.integrate(f, x) * 2) if F_ != 0 else "x", T(sp.integrate(f, x).subs(x, 2 * x))]
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Which function is an antiderivative of f(x) = {T(f)}?", good, ["F is an antiderivative of f if F′(x) = f(x).", f"Differentiate each choice; ({good})′ = {T(f)}."], options=opts, chk=PY("is_anti", f=T(f)), mode="mc", tags=["reasoning"])


# ============================================================== S2 Basic antiderivatives
@fam("012")
def s2_indef(r, L):
    f, k_ = build_g(r, L)
    F_ = sp.integrate(f, x)
    ans = anti_text(F_)
    w = [T(sp.diff(f, x)) + " + C", anti_text(F_.subs(x, x) * 2) if not F_.has(sp.log) else anti_text(F_ + x), T(sp.expand(f * x)) + " + C"]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Find {integ(f)}.", ans, [RULE[k_], ans + "."], w, H(f"P('{T(f)}')", "anti"), why=["Differentiated instead of integrating", "Made an error with the coefficient", "Multiplied by x instead of using the power rule"])


# ============================================================== S3 Riemann sums
@fam("012")
def s3_riemann(r, L):
    f = rint(r, -2, 3, True) * x ** 2 + rint(r, -4, 4) * x + rint(r, 0, 9) if L else rint(r, 1, 3) * x + rint(r, 0, 6)
    a = rint(r, -2, 2)
    n_ = pick(r, [2, 3, 4] if L < 2 else [4, 5, 6])
    dx = pick(r, [1, 2]) if L == 0 else pick(r, [1, sp.Rational(1, 2), 2])
    b = a + n_ * dx
    kind = pick(r, ["left", "right", "mid"]) if L else pick(r, ["left", "right"])
    pts = [a + i * dx for i in range(n_)] if kind == "left" else [a + (i + 1) * dx for i in range(n_)] if kind == "right" else [a + (i + sp.Rational(1, 2)) * dx for i in range(n_)]
    v = sum(f.subs(x, p_) for p_ in pts) * dx
    oth = {"left": [a + (i + 1) * dx for i in range(n_)], "right": [a + i * dx for i in range(n_)], "mid": [a + i * dx for i in range(n_)]}[kind]
    w1 = sum(f.subs(x, p_) for p_ in oth) * dx
    w2 = sum(f.subs(x, p_) for p_ in pts)
    w3 = sp.integrate(f, (x, a, b))
    ws = [T(w1), T(w2) if dx != 1 else T(v + f.subs(x, pts[0])), T(w3)]
    need(T(v) not in ws and len(set(ws)) == 3)
    return Q(f"Approximate {integ(f, a, b)} using a {'left' if kind == 'left' else 'right' if kind == 'right' else 'midpoint'} Riemann sum with {n_} equal subintervals.", T(v),
             [f"Δx = ({T(b)} - {par(a)}) ÷ {n_} = {T(dx)}.", f"Sample points: {', '.join(T(p_) for p_ in pts)}.", f"Sum: Δx·[{' + '.join('f(' + T(p_) + ')' for p_ in pts)}] = {T(v)}."],
             ws, PY("riemann", f=T(f), a=str(a), b=str(b), n=n_, how=kind), why=["Used the wrong endpoints", "Forgot to multiply by Δx" if dx != 1 else "Added an extra rectangle", "Computed the exact integral"])


# ============================================================== S4 Riemann sums ↔ integrals
@fam("012", mode="mc")
def s4_convert(r, L):
    a = rint(r, -2, 3)
    w_ = rint(r, 1, 4)
    fn = pick(r, [("x²", lambda u: u ** 2), ("x³", lambda u: u ** 3), ("√x", lambda u: sp.sqrt(u)), ("sin(x)", lambda u: sp.sin(u)), ("eˣ", lambda u: sp.exp(u)), ("1/x", lambda u: 1 / u)])
    nm, g = fn
    if nm in ("√x", "1/x"):
        a = abs(a) + 1
    b = a + w_
    inner = f"{a} + {w_}k/n" if a else f"{w_}k/n"
    gtxt = {"x²": f"({inner})²", "x³": f"({inner})³", "√x": f"√({inner})", "sin(x)": f"sin({inner})", "eˣ": f"e^({inner})", "1/x": f"1/({inner})"}[nm]
    s_txt = f"lim (n → ∞) Σ (k = 1 to n) {gtxt} · ({w_}/n)"
    good = f"∫ from {a} to {b} {nm} dx"
    bad = [f"∫ from 0 to {w_} {nm} dx" if a else f"∫ from {w_} to {w_ * 2} {nm} dx", f"∫ from {a} to {a + 1} {nm} dx" if w_ != 1 else f"∫ from {a} to {a + 2} {nm} dx", f"∫ from {a} to {b} {nm.replace('x', '(x + ' + str(a) + ')') if a else nm + ' + 1'} dx"]
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Which definite integral equals {s_txt}?", good, [f"Δx = {w_}/n, so b - a = {w_}." if False else f"Δx = {w_} ÷ n, so b - a = {w_}.", f"xₖ = {a} + k·Δx, so a = {a} and f(x) = {nm}.", good + "."],
             options=opts, chk=PY("riemann_int", f=nm, a=a, w=w_), mode="mc")


# ============================================================== S5 Approximating from tables
@fam("012")
def s5_trap(r, L):
    xs = [0]
    for _ in range(3 if L == 0 else 4):
        xs.append(xs[-1] + (pick(r, [1, 2]) if L == 0 else pick(r, [1, 2, 3])))
    if L == 0:
        d = xs[1] - xs[0]
        xs = [i * d for i in range(4)]
    ys = [rint(r, 0, 30) for _ in xs]
    kind = pick(r, ["trap", "left", "right"]) if L else "trap"
    segs = list(zip(xs[:-1], xs[1:], ys[:-1], ys[1:]))
    v = {"trap": sum(sp.Rational((y0 + y1) * (x1 - x0), 2) for x0, x1, y0, y1 in segs), "left": sum(y0 * (x1 - x0) for x0, x1, y0, y1 in segs), "right": sum(y1 * (x1 - x0) for x0, x1, y0, y1 in segs)}[kind]
    tbl = "; ".join(f"f({a}) = {b}" for a, b in zip(xs, ys))
    nm = {"trap": "the trapezoidal rule", "left": "a left Riemann sum", "right": "a right Riemann sum"}[kind]
    w = [sum(y0 * (x1 - x0) for x0, x1, y0, y1 in segs) if kind != "left" else sum(y1 * (x1 - x0) for x0, x1, y0, y1 in segs), sum(ys) * (xs[1] - xs[0]), sum(sp.Rational(y0 + y1, 2) for x0, x1, y0, y1 in segs) if kind == "trap" else sp.Rational(sum(ys), 1)]
    ws = [T(z) for z in w]
    need(T(v) not in ws and len(set(ws)) == 3)
    return Q(f"Use {nm} with the subintervals in the table to approximate ∫ from {xs[0]} to {xs[-1]} f(x) dx. {tbl}.", T(v),
             ["Use each subinterval's own width.", {"trap": "Trapezoid area = width × (average of the two heights).", "left": "Height = left endpoint value.", "right": "Height = right endpoint value."}[kind], f"Sum = {T(v)}."],
             ws, PY("table_sum", xs=xs, ys=ys, how=kind), why=["Used the wrong endpoints", "Assumed equal widths" if L else "Added all heights", "Forgot the widths"])


# ============================================================== S6 Integrals from geometry
@fam("012")
def s6_geometry(r, L):
    kind = pick(r, ["linear", "abs"] if L == 0 else ["linear", "abs", "semi"] if L == 1 else ["semi", "quarter", "piece"])
    if kind == "linear":
        m, c = rint(r, -3, 3, True), rint(r, -6, 6)
        a, b = sorted(r.sample(range(-4, 6), 2))
        f = m * x + c
        v = sp.integrate(f, (x, a, b))
        steps = ["The region is made of trapezoids or triangles; area below the axis counts as negative.", f"= {T(v)}."]
        w = [T(abs(sp.integrate(sp.Abs(f), (x, a, b)))) if abs(sp.integrate(sp.Abs(f), (x, a, b))) != v else T(v + 1), T((f.subs(x, a) + f.subs(x, b)) * (b - a)), T(-v) if v else "1"]
    elif kind == "abs":
        k_ = rint(r, -3, 3)
        a, b = k_ - rint(r, 1, 4), k_ + rint(r, 1, 4)
        f = sp.Abs(x - k_)
        v = sp.Rational((k_ - a) ** 2 + (b - k_) ** 2, 2)
        steps = ["The graph is a V; the region is two triangles.", f"(1/2)({k_ - a})² + (1/2)({b - k_})² = {T(v)}."]
        w = [T((k_ - a) ** 2 + (b - k_) ** 2), T(sp.Rational((b - a) ** 2, 2)), T(sp.Rational((b - k_) ** 2 - (k_ - a) ** 2, 2)) if (b - k_) != (k_ - a) else T(v + 2)]
    elif kind in ("semi", "quarter"):
        R = rint(r, 1, 6)
        f = sp.sqrt(R * R - x ** 2)
        a, b = (-R, R) if kind == "semi" else pick(r, [(0, R), (-R, 0)])
        v = sp.pi * R * R / (2 if kind == "semi" else 4)
        steps = [f"y = √({R * R} - x²) is the upper half of a circle of radius {R}.", f"The region is a {'half' if kind == 'semi' else 'quarter'}-disk: area {T(v)}."]
        w = [T(sp.pi * R * R), T(sp.pi * R / (2 if kind == "semi" else 4)), T(2 * sp.pi * R)]
    else:
        R = rint(r, 1, 4)
        f = None
        c = rint(r, 1, 5)
        v = sp.pi * R * R / 2 + c * R
        integ_txt = f"∫ from {-R} to {R} (√({R * R} - x²) + {c}) dx"
        return Q(f"Use geometry to evaluate {integ_txt}.", T(v), [f"Split: ∫ √({R * R} - x²) dx over [-{R}, {R}] is a half-disk = {T(sp.pi * R * R / 2)}.", f"∫ {c} dx over an interval of length {2 * R} = {2 * c * R}.", f"Total = {T(sp.pi * R * R / 2 + 2 * c * R)}."],
                 [T(sp.pi * R * R + 2 * c * R), T(sp.pi * R * R / 2 + c), T(sp.pi * R * R / 2 + c * R)], H(f"integrate(P('√({R * R} - x²) + {c}'), (x, {-R}, {R}))"),
                 why=["Used a full disk", "Forgot to multiply the constant by the width", "Used half the width for the constant"]) if False else \
            Q(f"Use geometry to evaluate {integ_txt}.", T(sp.pi * R * R / 2 + 2 * c * R), [f"∫ √({R * R} - x²) dx over [-{R}, {R}] is a half-disk = {T(sp.pi * R * R / 2)}.", f"∫ {c} dx over an interval of length {2 * R} = {2 * c * R}.", f"Total = {T(sp.pi * R * R / 2 + 2 * c * R)}."],
              [T(sp.pi * R * R + 2 * c * R), T(sp.pi * R * R / 2 + c), T(sp.pi * R * R / 2 + c * R)], H(f"integrate(P('√({R * R} - x²) + {c}'), (x, {-R}, {R}))"),
              why=["Used a full disk", "Forgot to multiply the constant by the width", "Used half the width for the constant"])
    need(T(v) not in w and len(set(w)) == 3)
    return Q(f"Use geometry (areas) to evaluate {integ(f, a, b)}.", T(v), steps, w, H(f"integrate(P('{T(f)}'), (x, {a}, {b}))"),
             why=["Treated area below the axis as positive" if kind == "linear" else "Forgot the 1/2" if kind == "abs" else "Used the full disk", "Used a rectangle instead" if kind == "linear" else "Used one big triangle" if kind == "abs" else "Used the circumference formula", "Made a sign error" if kind != "semi" and kind != "quarter" else "Used the circumference"])


@fam("012")
def s6_graphs(r, L):
    pts = [(-4, rint(r, -3, 3))]
    for xv in (-2, 0, 2, 4):
        pts.append((xv, rint(r, -3, 3)))
    a, b = sorted(r.sample([-4, -2, 0, 2, 4], 2))
    v = sum(sp.Rational((y0 + y1) * (x1 - x0), 2) for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]) if x0 >= a and x1 <= b)
    tot_abs = sum(abs(sp.integrate((y0 + (y1 - y0) * (x - x0) / (x1 - x0)), (x, x0, x1))) if (y0 >= 0) == (y1 >= 0) else
                  sp.integrate(sp.Abs(y0 + (y1 - y0) * (x - x0) / (x1 - x0)), (x, x0, x1)) for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]) if x0 >= a and x1 <= b)
    need(tot_abs != abs(v))
    xs_, ys_ = [float(p_[0]) for p_ in pts], [float(p_[1]) for p_ in pts]
    return Q(f"The graph of f consists of line segments through the marked points. Evaluate ∫ from {a} to {b} f(x) dx.", T(v),
             ["Split the region into triangles and trapezoids.", "Regions below the x-axis count as negative.", f"Total = {T(v)}."],
             [T(tot_abs), T(-v) if v else "1", T(2 * v) if v else "2"], PY("pl_integral", pts=[list(p_) for p_ in pts], a=a, b=b),
             why=["Counted area below the axis as positive", "Made a sign error", "Forgot the 1/2 for triangles"],
             diagram={"alt": "Piecewise linear graph of f through " + ", ".join(f"({p_[0]}, {p_[1]})" for p_ in pts) + ".", "draw": curve_draw([(xs_, ys_, "solid")], (-5, 5), (-5, 5), pts=[(p_[0], p_[1], "") for p_ in pts], label_every=1)})


# ============================================================== S7 Properties
@fam("012")
def s7_props(r, L):
    a, b, c = sorted(r.sample(range(-3, 10), 3))
    A_, B_, G_ = rint(r, -12, 12, True), rint(r, -12, 12, True), rint(r, -12, 12, True)
    k_, m_ = rint(r, -4, 4, True), rint(r, -4, 4, True)
    kind = pick(r, ["add", "rev", "lin"] if L < 2 else ["lin", "add_lin", "split"])
    given = f"∫ from {a} to {b} f(x) dx = {A_}, ∫ from {b} to {c} f(x) dx = {B_}, and ∫ from {a} to {b} g(x) dx = {G_}"
    if kind == "add":
        q, v, w = f"∫ from {a} to {c} f(x) dx", A_ + B_, [A_ - B_, B_ - A_, A_ * B_]
    elif kind == "rev":
        q, v, w = f"∫ from {b} to {a} f(x) dx", -A_, [A_, B_, -B_]
    elif kind == "lin":
        q, v, w = f"∫ from {a} to {b} ({k_}f(x) {'+' if m_ > 0 else '-'} {abs(m_)}g(x)) dx", k_ * A_ + m_ * G_, [A_ + G_, k_ * A_ - m_ * G_, k_ * m_ * A_ * G_]
    elif kind == "add_lin":
        q, v, w = f"∫ from {a} to {c} {k_}f(x) dx", k_ * (A_ + B_), [k_ * A_ + B_, A_ + B_, k_ * (A_ - B_)]
    else:
        q, v, w = f"∫ from {a} to {b} (f(x) {'+' if k_ > 0 else '-'} {abs(k_)}) dx", A_ + k_ * (b - a), [A_ + k_, A_ * k_, A_ + k_ * (c - a)]
    need(v not in w and len(set(w)) == 3)
    return Q(f"Given {given}, find {q}.", str(v), ["Use additivity over adjacent intervals, reversal of limits (sign change), and linearity.", f"= {v}."], [str(z) for z in w], PY("int_props", a=a, b=b, c=c, A=A_, B=B_, G=G_, q=q),
             why=["Subtracted instead of adding (or reversed a sign)", "Applied the property incorrectly", "Multiplied the integrals"])


SKILLS = {
    1: dict(name="Antidifferentiation as the Inverse of Differentiation", std=["AP FUN-5.A"], fams=[s1_particular, s1_which], extra=[err_of(s1_particular), open_of(s1_particular)]),
    2: dict(name="Antiderivatives of Basic Functions", std=["AP FUN-6.C"], fams=[s2_indef], extra=[err_of(s2_indef), open_of(s2_indef)]),
    3: dict(name="Definite Integrals as Limits of Riemann Sums", std=["AP LIM-5.A", "AP LIM-5.B"], fams=[s3_riemann], extra=[err_of(s3_riemann), open_of(s3_riemann)]),
    4: dict(name="Converting Riemann Sums to Integral Notation", std=["AP LIM-5.C"], fams=[s4_convert, s3_riemann], extra=[err_of(s3_riemann), open_of(s3_riemann)]),
    5: dict(name="Approximating Definite Integrals", std=["AP LIM-5.A"], fams=[s5_trap], extra=[err_of(s5_trap), open_of(s5_trap)]),
    6: dict(name="Evaluating Integrals Using Geometry", std=["AP FUN-6.A"], fams=[s6_geometry, s6_graphs], extra=[err_of(s6_geometry), open_of(s6_geometry)]),
    7: dict(name="Properties of Definite Integrals", std=["AP FUN-6.B"], fams=[s7_props], extra=[err_of(s7_props), open_of(s7_props)]),
}
