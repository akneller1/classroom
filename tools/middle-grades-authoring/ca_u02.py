"""Calculus Unit 2 — Limits and Continuity (limits-continuity)."""
from hslib import *

UNIT_ID = "limits-continuity"
ABBR = "lim"


def lim(a, side=""):
    return f"lim (x → {T(a) if a not in (sp.oo, -sp.oo) else ('∞' if a == sp.oo else '-∞')}{side})"


def poly(r, deg, lo=-5, hi=5):
    return polyx([rint(r, lo, hi, True)] + [rint(r, lo, hi) for _ in range(deg)])


# ============================================================== S1 Notation and interpretation
@fam("012")
def s1_sub(r, L):
    a = rint(r, -4, 4)
    f = poly(r, 2 if L == 0 else 3) if L < 2 else pick(r, [sp.sqrt(x + rint(r, 5, 12)) * rint(r, 1, 3), (x ** 2 + rint(r, 1, 6)) / (x + rint(r, 6, 9))])
    v = sp.nsimplify(f.subs(x, a))
    need(v.is_finite)
    ft = T(f) if not isinstance(f, sp.Mul) or not any(isinstance(a_, sp.Pow) and a_.exp == -1 for a_ in f.args) else T(f)
    return Q(f"Evaluate {lim(a)} ({ft}).", T(v), ["The function is continuous at x = " + str(a) + ", so substitute.", f"= {T(v)}."], [T(f.subs(x, -a)) if f.subs(x, -a) != v else T(v + 1), T(sp.nsimplify(f.subs(x, a + 1))), "does not exist"],
             H(f"limit(P('{ft}'), x, {a})"), why=["Substituted the opposite value", "Substituted the wrong value", "Thought a limit must be undefined"])


@fam("012", mode="mc")
def s1_meaning(r, L):
    a, Lv = rint(r, -5, 5), rint(r, -9, 9)
    items = [(f"{lim(a)} f(x) = {Lv}", f"As x gets close to {a} from both sides, f(x) gets close to {Lv}.",
              [f"f({a}) = {Lv}.", f"As f(x) gets close to {a}, x gets close to {Lv}.", f"f(x) = {Lv} for every x near {a}."]),
             (f"{lim(a, '⁺')} f(x) = {Lv}", f"As x approaches {a} from the right, f(x) approaches {Lv}.",
              [f"As x approaches {a} from the left, f(x) approaches {Lv}.", f"f({a}) = {Lv} and f is increasing.", f"The two-sided limit at {a} equals {Lv}."]),
             (f"{lim(sp.oo)} f(x) = {Lv}", f"The graph of f has a horizontal asymptote y = {Lv} as x → ∞.",
              [f"The graph of f has a vertical asymptote x = {Lv}.", f"f(x) = {Lv} for large x.", f"f is never equal to {Lv}."]),
             (f"{lim(a)} f(x) = ∞", f"f(x) increases without bound as x approaches {a}, so x = {a} is a vertical asymptote.",
              [f"f({a}) = ∞.", f"y = {a} is a horizontal asymptote.", f"The limit equals a very large number."])]
    st, good, bad = pick(r, items if L else items[:2])
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q(f"Which statement best describes {st}?", good, ["A limit describes the value f(x) approaches, not necessarily f(a).", good], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


# ============================================================== S2 Graphs and tables
def pw_graph(r):
    a = rint(r, -3, 3)
    m1, b1 = rint(r, -2, 2), rint(r, -3, 3)
    m2, b2 = rint(r, -2, 2), rint(r, -3, 3)
    left = m1 * (a) + b1
    right = m2 * (a) + b2
    fa = pick(r, [left, right, rint(r, -4, 4)])
    need(abs(left) <= 5 and abs(right) <= 5 and abs(fa) <= 5 and all(abs(m1 * v + b1) <= 6 for v in (-6, a)) and all(abs(m2 * v + b2) <= 6 for v in (a, 6)))
    return a, (m1, b1), (m2, b2), left, right, fa


@fam("012")
def s2_graph(r, L):
    a, (m1, b1), (m2, b2), lv, rv, fa = pw_graph(r)
    need(lv != rv or fa != lv or L == 0)
    ask = pick(r, ["left", "right", "two", "value"])
    xl = [-6 + (a + 6) * i / 100 for i in range(101)]
    xr = [a + (6 - a) * i / 100 for i in range(101)]
    curves = [(xl, [m1 * v + b1 for v in xl], "solid"), (xr, [m2 * v + b2 for v in xr], "solid")]
    pts = [(a, lv, "", fa != lv), (a, rv, "", fa != rv)] + ([(a, fa, "")] if fa not in (lv, rv) else [])
    pts = [(a, lv, "", True), (a, rv, "", True)]
    pts = [p_ for p_ in pts if p_[1] != fa] + [(a, fa, "")]
    alt = f"Graph of f made of two rays meeting near x = {a}: from the left the graph approaches ({a}, {lv}); from the right it approaches ({a}, {rv}); the solid point is ({a}, {fa})."
    two = str(lv) if lv == rv else "does not exist"
    if ask == "left":
        q, ans, w = f"{lim(a, '⁻')} f(x)", str(lv), [str(rv) if rv != lv else str(lv + 1), str(fa) if fa != lv else str(fa - 1), "does not exist"]
    elif ask == "right":
        q, ans, w = f"{lim(a, '⁺')} f(x)", str(rv), [str(lv) if rv != lv else str(rv + 1), str(fa) if fa != rv else str(fa - 1), "does not exist"]
    elif ask == "two":
        q, ans = f"{lim(a)} f(x)", two
        w = [str(lv) if two == "does not exist" else "does not exist", str(rv) if two == "does not exist" else str(fa) if fa != lv else str(lv + 1), str(fa) if (two == "does not exist" and fa not in (lv, rv)) else str(lv + rv) if str(lv + rv) not in (two, str(lv), str(rv)) else str(lv - 1)]
    else:
        q, ans, w = f"f({a})", str(fa), [str(lv) if lv != fa else str(rv) if rv != fa else str(fa + 1), "does not exist", str(rv) if rv not in (fa, lv) else str(fa + 2)]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Use the graph of f to find {q}.", ans, ["Open circles show where the graph approaches; the solid dot shows the function value.", f"From the left: {lv}. From the right: {rv}. f({a}) = {fa}.", f"{q} = {ans}."],
             w, PY("pw_lim", a=a, l=[m1, b1], r=[m2, b2], fa=fa, ask=ask), why=["Read the wrong side", "Confused the function value with the limit", "Misjudged whether the limit exists"],
             diagram={"alt": alt, "draw": curve_draw(curves, (-6, 6), (-6, 6), pts=pts, label_every=1)})


@fam("012")
def s2_table(r, L):
    a = rint(r, -3, 3)
    kind = pick(r, ["rational", "sinx"] if L else ["rational"])
    if kind == "rational":
        c = rint(r, -5, 5)
        need(c != a)
        f = (x ** 2 - (a + c) * x + a * c) / (x - a)   # = x - c
        ft = f"({T(sp.expand(x ** 2 - (a + c) * x + a * c))})/({T(x - a)})"
        Lv = a - c
    else:
        k_ = rint(r, 2, 5)
        a = 0
        f = sp.sin(k_ * x) / x
        ft = f"sin({k_}x)/x"
        Lv = k_
    hs_ = [sp.Rational(-1, 10), sp.Rational(-1, 100), sp.Rational(-1, 1000), sp.Rational(1, 1000), sp.Rational(1, 100), sp.Rational(1, 10)]
    rows = "; ".join(f"f({D(F(int((a + h_).p), int((a + h_).q)))}) ≈ {Rd(float(f.subs(x, a + h_)), 4)}" for h_ in hs_)
    return Q(f"For f(x) = {ft}, a table gives {rows}. Estimate {lim(a)} f(x).", str(Lv), ["Look at the values as x gets closer to " + str(a) + " from both sides.", f"They approach {Lv}.", f"{lim(a)} f(x) = {Lv}."],
             ["does not exist", "0" if Lv != 0 else "1", Rd(float(f.subs(x, a + sp.Rational(1, 10))), 4)], H(f"limit(P('{ft}'), x, {a})"), why=["Thought 0/0 means the limit does not exist", "Used f(a) = 0/0 as 0", "Used a value too far from a"])


# ============================================================== S3 Algebraic limits
@fam("012")
def s3_algebra(r, L):
    kind = pick(r, ["factor"] if L == 0 else ["factor", "rational", "cubic"] if L == 1 else ["root", "trig", "complex", "cubic"])
    a = rint(r, -5, 5, True)
    if kind == "factor":
        c = rint(r, -6, 6)
        need(c != a)
        kk = pick(r, [1, 2]) if L else 1
        num, den = sp.expand((x - a) * (x - c)), sp.expand((x - a) * kk)
        ft = f"({T(num)})/({T(den)})"
        v = sp.Rational(a - c, kk)
        steps = [f"Direct substitution gives 0/0." if False else "Direct substitution gives 0 ÷ 0, an indeterminate form.", f"Factor and cancel (x - {a}).".replace("- -", "+ "), "Substitute into what remains."]
    elif kind == "rational":
        c, d = rint(r, -6, 6), rint(r, -6, 6)
        need(len({a, c, d}) == 3)
        num, den = sp.expand((x - a) * (x - c)), sp.expand((x - a) * (x - d))
        ft = f"({T(num)})/({T(den)})"
        v = sp.Rational(a - c, a - d)
        steps = ["0 ÷ 0: factor both.", f"Cancel (x - {a}).".replace("- -", "+ "), "Substitute."]
    elif kind == "cubic":
        num = sp.expand(x ** 3 - a ** 3)
        den = x - a
        ft = f"({T(num)})/({T(den)})"
        v = sp.Integer(3 * a * a)
        steps = ["0 ÷ 0: use the difference (or sum) of cubes.", f"x³ - a³ = (x - a)(x² + ax + a²).", "Cancel and substitute: 3a²."]
    elif kind == "root":
        d = pick(r, [1, 2, 3, 4])
        c = d * d - a
        ft = f"(√(x + {c}) - {d})/({T(x - a)})" if c >= 0 else f"(√(x - {-c}) - {d})/({T(x - a)})"
        need(c != 0)
        v = sp.Rational(1, 2 * d)
        steps = ["0 ÷ 0: multiply by the conjugate.", "The numerator becomes x - a; cancel.", f"Substitute: 1 ÷ (2·{d})."]
    elif kind == "trig":
        k_, m_ = rint(r, 1, 6), rint(r, 1, 6)
        need(k_ != m_)
        ft = pick(r, [f"sin({k_}x)/({m_}x)", f"(1 - cos(x))/x", f"tan({k_}x)/({m_}x)"])
        a = 0
        v = sp.Integer(0) if ft.startswith("(1 - cos") else sp.Rational(k_, m_)
        steps = ["Use lim (x → 0) sin(x) ÷ x = 1 (and lim (x → 0) (1 - cos x) ÷ x = 0).", "Rewrite to match the special limit.", "Evaluate."]
    else:
        ft = f"(1/x - 1/{a})/(x - {a})".replace("- -", "+ ") if a > 0 else f"(1/x + 1/{-a})/(x + {-a})"
        need(abs(a) > 1)
        v = sp.Rational(-1, a * a)
        steps = ["0 ÷ 0: combine the fractions in the numerator.", f"(a - x) ÷ (ax) over (x - a) simplifies to -1 ÷ (ax).", f"Substitute: -1 ÷ {a * a}."]
    vstr = T(v)
    return Q(f"Evaluate {lim(a)} {ft}.", vstr, steps + [f"= {vstr}."], ["does not exist", "0" if v != 0 else "1", T(v * 2) if v else "∞"], H(f"limit(P('{ft}'), x, {a})"),
             why=["Stopped at 0 ÷ 0", "Treated 0 ÷ 0 as 0" if v != 0 else "Treated 0 ÷ 0 as 1", "Made an algebra error"])


def P_(t):
    import hschecks
    return hschecks.P(t)


# ============================================================== S4 One-sided limits
@fam("012")
def s4_piece(r, L):
    a = rint(r, -3, 3)
    f1 = rint(r, -3, 3) * x + rint(r, -6, 6) if L == 0 else sp.Integer(rint(r, -2, 2)) * x ** 2 + rint(r, -5, 5)
    f2 = rint(r, -3, 3) * x + rint(r, -6, 6)
    if r.random() < 0.4:
        f2 = f2 - f2.subs(x, a) + f1.subs(x, a)
    lv, rv = f1.subs(x, a), f2.subs(x, a)
    ask = pick(r, ["left", "right", "two"])
    two = T(lv) if lv == rv else "does not exist"
    pw = f"f(x) = {T(f1)} for x < {a}, and f(x) = {T(f2)} for x ≥ {a}"
    ans = {"left": T(lv), "right": T(rv), "two": two}[ask]
    q = {"left": lim(a, "⁻"), "right": lim(a, "⁺"), "two": lim(a)}[ask] + " f(x)"
    w = {"left": [T(rv) if rv != lv else T(lv + 1), "does not exist", T(lv + rv)], "right": [T(lv) if rv != lv else T(rv - 1), "does not exist", T(lv + rv) if lv + rv != rv else T(rv + 2)],
         "two": ["does not exist" if lv == rv else T(lv), T(lv + 1) if lv == rv else T(rv), T(lv + rv) if lv == rv else T((lv + rv) / 2)]}[ask]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"{pw}. Find {q}.", ans, ["Left-hand limit uses the piece for x < a; right-hand uses x ≥ a.", f"Left: {T(lv)}. Right: {T(rv)}.", "The two-sided limit exists only if they are equal." if ask == "two" else f"{q} = {ans}."],
             w, PY("pw_formula", a=a, f1=T(f1), f2=T(f2), ask=ask), why=["Used the wrong piece", "Thought the limit does not exist" if ans != "does not exist" else "Gave one side only", "Combined the two sides"])


@fam("12")
def s4_infinite(r, L):
    a = rint(r, -4, 4)
    k_ = rint(r, -6, 6, True)
    pw = pick(r, [1, 2])
    side = pick(r, ["⁻", "⁺"])
    ft = f"{k_}/({T(x - a)})" + ("²" if pw == 2 else "") if pw == 2 else f"{k_}/({T(x - a)})"
    ft = f"{k_}/({T(x - a)})²" if pw == 2 else f"{k_}/({T(x - a)})"
    sgn = (1 if k_ > 0 else -1) * (1 if (pw == 2 or side == "⁺") else -1)
    ans = "∞" if sgn > 0 else "-∞"
    return Q(f"Evaluate {lim(a, side)} {ft}.", ans, [f"As x → {a}{side}, the denominator → 0 {'through positive values' if pw == 2 or side == '⁺' else 'through negative values'}.", f"The numerator is {k_}.", f"So the limit is {ans}."],
             ["-∞" if ans == "∞" else "∞", "0", "does not exist" if True else ""], H(f"limit(P('{ft}'), x, {a}, '{'-' if side == '⁻' else '+'}')"),
             why=["Got the sign wrong", "Thought a zero denominator gives 0", "Did not analyze the sign"])


# ============================================================== S5 Behavior (limits at infinity)
@fam("012")
def s5_infty(r, L):
    dn = rint(r, 1, 3)
    dd = rint(r, 1, 3)
    if L == 0:
        dd = dn
    an, ad = rint(r, -6, 6, True), rint(r, 1, 6)
    num = an * x ** dn + rint(r, -5, 5) * x ** max(0, dn - 1) + rint(r, -9, 9)
    den = ad * x ** dd + rint(r, -5, 5)
    ft = f"({T(num)})/({T(den)})"
    to = pick(r, [sp.oo, -sp.oo]) if L == 2 else sp.oo
    v = sp.limit(num / den, x, to)
    ans = T(v) if v not in (sp.oo, -sp.oo) else ("∞" if v == sp.oo else "-∞")
    return Q(f"Evaluate {lim(to)} {ft}.", ans, ["Compare the degrees of the numerator and denominator.", "Equal degrees: ratio of leading coefficients. Bottom-heavy: 0. Top-heavy: ±∞.", f"= {ans}."],
             [T(sp.Rational(an, ad)) if T(sp.Rational(an, ad)) != ans else "0", "0" if ans != "0" else "∞", T(sp.Rational(num.subs(x, 0), den.subs(x, 0))) if den.subs(x, 0) and T(sp.Rational(num.subs(x, 0), den.subs(x, 0))) not in (ans, T(sp.Rational(an, ad))) else "does not exist"],
             H(f"limit(P('{ft}'), x, {'oo' if to == sp.oo else '-oo'})"), why=["Used the leading-coefficient ratio when degrees differ" if dn != dd else "Made an error with the degrees", "Thought every limit at infinity is 0", "Used the constant terms"])


@fam("012")
def s5_asym(r, L):
    a = rint(r, -5, 5)
    b = rint(r, -5, 5)
    m = rint(r, 1, 6)
    num, den = m * x + b, x - a
    need(num.subs(x, a) != 0)
    ft = f"({T(num)})/({T(den)})"
    ask = pick(r, ["va", "ha"])
    if ask == "va":
        return Q(f"Use limits to find the vertical asymptote of f(x) = {ft}.", f"x = {a}", [f"As x → {a}, the denominator → 0 and the numerator → {T(num.subs(x, a))}.", f"So {lim(a, '⁺')} f(x) = ±∞.", f"Vertical asymptote x = {a}."],
                 [f"y = {m}", f"x = {-a}" if a else "x = 1", f"x = {T(sp.Rational(-b, m))}"], PY("va_check", f=ft, ans_kind="va"), why=["Gave the horizontal asymptote", "Made a sign error", "Used the zero of the numerator"])
    return Q(f"Use limits to find the horizontal asymptote of f(x) = {ft}.", f"y = {m}", [f"{lim(sp.oo)} f(x) = {m}.", f"{lim(-sp.oo)} f(x) = {m}.", f"Horizontal asymptote y = {m}."],
             [f"x = {a}", f"y = {T(sp.Rational(b, -a))}" if a and sp.Rational(b, -a) != m else "y = 0", f"y = {m * a + b}" if m * a + b != m else f"y = {m + 1}"], PY("va_check", f=ft, ans_kind="ha"), why=["Gave the vertical asymptote", "Used the constants", "Substituted a"])


# ============================================================== S6 Continuity
@fam("012")
def s6_k(r, L):
    a = rint(r, -3, 3)
    f1 = rint(r, -3, 3, True) * x + rint(r, -6, 6) if L < 2 else rint(r, -2, 2, True) * x ** 2 + rint(r, -4, 4) * x
    c2 = rint(r, -3, 3, True)
    kv = f1.subs(x, a) - c2 * a
    if L == 0:
        st = f"f(x) = {T(f1)} for x < {a}, and f(x) = {T(c2 * x)} + k for x ≥ {a}".replace("+ k", "+ k")
        ans = f"k = {T(kv)}"
        code = f"solve(P('{T(f1)}').subs(x, {a}) - ({c2}*{a} + k), k)[0]"
        w = [f"k = {T(-kv)}" if kv else "k = 1", f"k = {T(f1.subs(x, a))}", f"k = {T(f1.subs(x, a) + c2 * a)}"]
    else:
        kc = rint(r, -3, 3, True)
        # f2 = k*x + kc ; continuity: k*a + kc = f1(a)
        need(a != 0)
        kv = sp.Rational(f1.subs(x, a) - kc, a)
        st = f"f(x) = {T(f1)} for x < {a}, and f(x) = kx {'+' if kc > 0 else '-'} {abs(kc)} for x ≥ {a}"
        ans = f"k = {T(kv)}"
        code = f"solve(P('{T(f1)}').subs(x, {a}) - (k*{a} + {kc}), k)[0]"
        w = [f"k = {T(-kv)}" if kv else "k = 1", f"k = {T(f1.subs(x, a) - kc)}", f"k = {T(sp.Rational(f1.subs(x, a) + kc, a))}"]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Find the value of k that makes f continuous everywhere: {st}.", ans, ["Both pieces must have the same value at x = " + str(a) + ".", "Set the left piece at a equal to the right piece at a.", ans + "."], w,
             H(code), why=["Made a sign error", "Forgot the x-term of the right piece" if L == 0 else "Forgot to divide by a", "Added instead of subtracting"])


@fam("012")
def s6_check(r, L):
    a = rint(r, -3, 3)
    f1 = rint(r, -3, 3) * x + rint(r, -5, 5)
    kind = pick(r, ["cont", "jump", "hole"])
    if kind == "cont":
        f2, fa = f1 + rint(r, -2, 2, True) * (x - a), f1.subs(x, a)
    elif kind == "jump":
        f2, fa = f1 + rint(r, -4, 4, True), f1.subs(x, a)
    else:
        f2, fa = f1, f1.subs(x, a) + rint(r, -3, 3, True)
    st = f"f(x) = {T(f1)} for x < {a}; f({a}) = {T(fa)}; f(x) = {T(sp.expand(f2))} for x > {a}"
    ans = "Yes" if kind == "cont" else "No"
    reason = {"cont": "all three conditions hold", "jump": "the one-sided limits differ", "hole": f"the limit {T(f1.subs(x, a))} does not equal f({a})"}[kind]
    return Q(f"Is f continuous at x = {a}? {st}.", ans, [f"Left limit: {T(f1.subs(x, a))}. Right limit: {T(f2.subs(x, a))}. f({a}) = {T(fa)}.", f"Continuous requires the limit to exist and equal f({a}).", f"{ans}: {reason}."],
             ["No" if ans == "Yes" else "Yes"], PY("cont_check", a=a, f1=T(f1), f2=T(sp.expand(f2)), fa=str(fa)), mode="sa", why=["Checked only that f(a) is defined"])


# ============================================================== S7 Types of discontinuity
@fam("012")
def s7_type(r, L):
    a = rint(r, -4, 4)
    kind = pick(r, ["removable", "jump", "infinite"])
    if kind == "removable":
        c = rint(r, -5, 5)
        need(c != a)
        ft = f"f(x) = ({T(sp.expand((x - a) * (x - c)))})/({T(x - a)})"
    elif kind == "infinite":
        c = rint(r, -5, 5)
        need(c != a)
        ft = f"f(x) = ({T(x - c)})/({T(x - a)})"
    else:
        ft = f"f(x) = (|{T(x - a)}|)/({T(x - a)})" if a else "f(x) = (|x|)/x"
    opts = [(o, o == kind) for o in ["removable", "jump", "infinite", "no discontinuity"]]
    return Q(f"Classify the discontinuity of {ft} at x = {a}.", kind, ["Find the one-sided limits at x = " + str(a) + ".", {"removable": "The limit exists (the factor cancels): removable.", "jump": "The one-sided limits are -1 and 1: jump.", "infinite": "The function grows without bound: infinite."}[kind]],
             options=opts, chk=PY("disc_type", f=ft.split("= ", 1)[1], a=a), mode="mc")


@fam("012")
def s7_hole(r, L):
    a, c = r.sample(range(-6, 7), 2)
    m = rint(r, 1, 4)
    num = sp.expand(m * (x - a) * (x - c))
    c2 = c + rint(r, 1, 3)
    need(c2 != a)
    den = sp.expand((x - a) * (x - c2) if L else (x - a))
    ft = f"({T(num)})/({T(den)})"
    v = sp.Rational(m * (a - c), 1) / ((a - c2) if L else 1)
    ans = f"({a}, {T(v)})"
    return Q(f"f(x) = {ft} has a removable discontinuity. Give its location as a point (x, y), where y is the limit there.", ans, [f"Factor: the common factor is (x - {a}).".replace("- -", "+ "), "Cancel it and substitute x = " + str(a) + ".", ans + "."],
             [f"({a}, 0)", f"({c}, 0)", f"({-a}, {T(v)})" if a else f"(1, {T(v)})"], H(f"[{a}, limit(P('{ft}'), x, {a})]", "point"), why=["Assumed the y-value is 0", "Used a zero of the numerator", "Made a sign error"])


# ============================================================== S8 Theorems requiring continuity
@fam("012")
def s8_ivt(r, L):
    xs = sorted(r.sample(range(0, 10), 4))
    ys = [rint(r, -8, 8) for _ in xs]
    k_ = rint(r, -6, 6)
    need(k_ not in ys)
    cnt = sum(1 for i in range(3) if (ys[i] - k_) * (ys[i + 1] - k_) < 0)
    tbl = "; ".join(f"f({a}) = {b}" for a, b in zip(xs, ys))
    return Q(f"f is continuous on [{xs[0]}, {xs[-1]}] with {tbl}. By the Intermediate Value Theorem, what is the least number of solutions of f(x) = {k_} on [{xs[0]}, {xs[-1]}]?", str(cnt),
             [f"Look for consecutive table values on opposite sides of {k_}.", f"There {'is' if cnt == 1 else 'are'} {cnt} such interval{'s' if cnt != 1 else ''}.", f"At least {cnt}."],
             [str(cnt + 1), str(max(0, cnt - 1)) if cnt else "3", "4" if cnt != 4 else "2"], PY("ivt_count", xs=xs, ys=ys, k=k_), why=["Counted an extra crossing", "Missed a crossing", "Counted every interval"], tags=["reasoning"])


@fam("012", mode="mc")
def s8_theorem(r, L):
    a, b = sorted(r.sample(range(-5, 8), 2))
    items = [(f"f is continuous on [{a}, {b}]. Which theorem guarantees f has an absolute maximum and minimum on [{a}, {b}]?", "Extreme Value Theorem", ["Intermediate Value Theorem", "Mean Value Theorem", "Squeeze Theorem"]),
             (f"f is continuous on [{a}, {b}], f({a}) < 0, and f({b}) > 0. Which theorem guarantees a zero in ({a}, {b})?", "Intermediate Value Theorem", ["Extreme Value Theorem", "Mean Value Theorem", "Squeeze Theorem"]),
             (f"f(x) = 1/(x - {T(sp.Rational(a + b, 2))}) on [{a}, {b}]. Why does the Extreme Value Theorem not apply?", "f is not continuous on the interval", ["The interval is not closed", "f is not differentiable everywhere", "f has no zeros"]),
             (f"-|x| ≤ g(x) ≤ |x| for all x near 0. Which theorem gives lim (x → 0) g(x) = 0?", "Squeeze Theorem", ["Intermediate Value Theorem", "Extreme Value Theorem", "Mean Value Theorem"])]
    qtxt, good, bad = pick(r, items)
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    r.shuffle(opts)
    return Q(qtxt, good, [f"{good}."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


SKILLS = {
    1: dict(name="Limit Notation and Interpretation", std=["AP LIM-1.A", "AP LIM-1.B"], fams=[s1_sub, s1_meaning], extra=[err_of(s1_sub), open_of(s1_sub)]),
    2: dict(name="Estimating Limits from Graphs and Tables", std=["AP LIM-1.C", "AP LIM-1.D"], fams=[s2_graph, s2_table], extra=[err_of(s2_table), open_of(s2_table)]),
    3: dict(name="Evaluating Limits Algebraically", std=["AP LIM-1.E"], fams=[s3_algebra], extra=[err_of(s3_algebra), open_of(s3_algebra)]),
    4: dict(name="One-Sided and Two-Sided Limits", std=["AP LIM-1.C", "AP LIM-1.D"], fams=[s4_piece, s4_infinite], extra=[err_of(s4_piece), open_of(s4_piece)]),
    5: dict(name="Using Limits to Describe Function Behavior", std=["AP LIM-2.D"], fams=[s5_infty, s5_asym], extra=[err_of(s5_infty), open_of(s5_infty)]),
    6: dict(name="Continuity on an Interval", std=["AP LIM-2.A", "AP LIM-2.B"], fams=[s6_k, s6_check], extra=[err_of(s6_k), open_of(s6_k)]),
    7: dict(name="Points and Types of Discontinuity", std=["AP LIM-2.A", "AP LIM-2.C"], fams=[s7_type, s7_hole], extra=[err_of(s7_hole), open_of(s7_hole)]),
    8: dict(name="Applying Theorems Requiring Continuity", std=["AP FUN-1.A"], fams=[s8_ivt, s8_theorem], extra=[err_of(s8_ivt), open_of(s8_ivt)]),
}
