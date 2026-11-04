"""Calculus Unit 8 — Differential Equations (differential-equations)."""
from hslib import *

UNIT_ID = "differential-equations"
ABBR = "deq"


# ============================================================== S1 Functions defined by rates
@fam("012", mode="mc")
def s1_model(r, L):
    items = [("The rate of change of a population P with respect to time t is proportional to P.", "P′ = kP", ["P′ = kt", "P = kP′", "P′ = P + k"]),
             ("The rate at which a cup of coffee cools is proportional to the difference between its temperature T and the room temperature 70°F.", "T′ = k(T - 70)", ["T′ = kT - 70", "T′ = k(70T)", "T = k(T′ - 70)"]),
             ("The rate of change of y with respect to x is proportional to the square root of y.", "y′ = k√y", ["y′ = √(ky)", "y = k√(y′)", "y′ = k√x"]),
             ("The amount A of a drug in the bloodstream decreases at a rate proportional to A.", "A′ = -kA (k > 0)", ["A′ = kt (k > 0)", "A′ = -k (k > 0)", "A = -kA′ (k > 0)"]),
             ("A rumor spreads at a rate proportional to the product of the number who have heard it, N, and the number who have not, 1000 - N.", "N′ = kN(1000 - N)", ["N′ = k(1000 - N)", "N′ = kN + 1000", "N′ = k(N - 1000)"])]
    st, good, bad = pick(r, items)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q(f"Which differential equation models this statement? {st}", good, ["“Proportional to” means equal to a constant k times the quantity.", good + "."], options=opts, chk=TXT(good), mode="mc", tags=["modeling"])


@fam("012")
def s1_slope(r, L):
    a_, b_ = rint(r, -4, 4, True), rint(r, -4, 4, True)
    rhs = pick(r, [a_ * x + b_ * y, x * y, x ** 2 - y, a_ * x - y ** 2, (x + y) / 2]) if L else a_ * x + b_ * y
    px, py = rint(r, -3, 3), rint(r, -3, 3)
    v = rhs.subs({x: px, y: py})
    return Q(f"For y′ = {T(rhs)}, find the slope of the solution curve through ({px}, {py}).", T(v), [f"Substitute x = {px}, y = {py} into y′.", f"y′ = {T(v)}."],
             [T(rhs.subs({x: py, y: px})), T(v + 1) if True else "", str(py)], H(f"P('{T(rhs)}').subs({{x: {px}, y: {py}}})"), why=["Switched x and y", "Made an arithmetic error", "Gave the y-coordinate"])


# ============================================================== S2 Verifying solutions
@fam("012")
def s2_verify(r, L):
    k_ = rint(r, -4, 4, True)
    good = r.random() < 0.5
    kind = pick(r, ["exp", "poly", "second"] if L else ["exp", "poly"])
    if kind == "exp":
        de = f"y′ = {k_}y"
        sol = f"y = {rint(r, 2, 9)}e^({k_ if good else k_ + pick(r, [1, -1])}x)".replace("^(1x)", "^x").replace("^(-1x)", "^(-x)")
        code = ("y′ - {k}y", k_)
    elif kind == "poly":
        de = "xy′ = 2y" if good or True else ""
        c = rint(r, 2, 9)
        sol = f"y = {c}x²" if good else f"y = {c}x³"
        code = None
    else:
        m = rint(r, 1, 4)
        de = f"y″ + {m * m}y = 0"
        sol = f"y = sin({m}x)" if good else f"y = sin({m + 1}x)"
        code = None
    ans = "Yes" if good else "No"
    return Q(f"Is {sol} a solution of {de}?", ans, ["Differentiate the proposed solution.", "Substitute into the equation and check whether both sides match.", ans + "."], ["No" if good else "Yes"],
             PY("de_verify", de=de, sol=sol), mode="sa", why=["Did not substitute to check"])


@fam("012")
def s2_findk(r, L):
    a_, b_ = r.sample([-3, -2, -1, 1, 2, 3, 4], 2)
    need(a_ != -b_)
    if L == 2 and r.random() < 0.5:
        # Euler equation: y = xᵏ, x²y″ + p·xy′ + q·y = 0 → k² + (p - 1)k + q = 0
        p2 = -(a_ + b_) + 1
        q_ = a_ * b_
        de = f"x²y″ {'+' if p2 >= 0 else '-'} {abs(p2)}xy′ {'+' if q_ >= 0 else '-'} {abs(q_)}y = 0".replace(" 1xy′", " xy′").replace(" 1y ", " y ").replace(" + 0xy′", "").replace(" - 0xy′", "")
        ans = f"k = {min(a_, b_)} or k = {max(a_, b_)}"
        return Q(f"Find all values of k for which y = xᵏ (x > 0) is a solution of {de}.", ans, ["y′ = kxᵏ⁻¹, y″ = k(k - 1)xᵏ⁻².", f"k(k - 1) + {p2}k + {q_} = 0.", ans + "."],
                 [f"k = {-max(a_, b_)} or k = {-min(a_, b_)}", f"k = {min(a_, b_)}", f"k = {p2} or k = {q_}" if {p2, q_} != {a_, b_} else f"k = {a_ + 1} or k = {b_ + 1}"],
                 H(f"solve(k*(k - 1) + ({p2})*k + ({q_}), k)", "set"), why=["Made sign errors", "Missed a root", "Used the coefficients as roots"])
    p_, q_ = -(a_ + b_), a_ * b_
    de = f"y″ {'+' if p_ >= 0 else '-'} {abs(p_)}y′ {'+' if q_ >= 0 else '-'} {abs(q_)}y = 0".replace(" 1y′", " y′").replace(" 1y ", " y ")
    ans = f"k = {min(a_, b_)} or k = {max(a_, b_)}"
    return Q(f"Find all values of k for which y = e^(kx) is a solution of {de}.", ans, ["y′ = ke^(kx), y″ = k²e^(kx).", f"k² {'+' if p_ >= 0 else '-'} {abs(p_)}k {'+' if q_ >= 0 else '-'} {abs(q_)} = 0.", ans + "."],
             [f"k = {-max(a_, b_)} or k = {-min(a_, b_)}", f"k = {min(a_, b_)}", f"k = {p_} or k = {q_}" if {p_, q_} != {a_, b_} else f"k = {a_ + 1} or k = {b_ + 1}"], H(f"solve(k**2 + ({p_})*k + ({q_}), k)", "set"), why=["Made sign errors in the factors", "Missed a root", "Used the coefficients as roots"])


# ============================================================== S3 Estimating (Euler's method)
@fam("012")
def s3_euler(r, L):
    a_, b_ = rint(r, -3, 3, True), rint(r, -2, 2, True)
    rhs = a_ * x + b_ * y if L < 2 else x * y + a_
    x0, y0 = rint(r, -2, 2), rint(r, -3, 3)
    hh = sp.Rational(pick(r, [sp.Rational(1, 2), 1, sp.Rational(1, 10)] if L else [1, sp.Rational(1, 2)]))
    n_ = 2 if L < 2 else 3
    xs, ys = [sp.Integer(x0)], [sp.Integer(y0)]
    for _ in range(n_):
        ys.append(ys[-1] + hh * rhs.subs({x: xs[-1], y: ys[-1]}))
        xs.append(xs[-1] + hh)
    ans = D(F(ys[-1].p, ys[-1].q)) if ys[-1].q in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100, 1000) else T(ys[-1])
    wrong1 = ys[-2]
    wrong2 = y0 + n_ * hh * rhs.subs({x: x0, y: y0})
    dd = lambda v: D(F(v.p, v.q)) if v.q in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100, 1000) else T(v)
    return Q(f"Use Euler's method with step size {T(hh) if hh.q == 1 else D(F(hh.p, hh.q))} and {n_} steps to approximate y({T(xs[-1]) if xs[-1].q == 1 else D(F(xs[-1].p, xs[-1].q))}) for y′ = {T(rhs)}, y({x0}) = {y0}.", ans,
             [f"yₙ₊₁ = yₙ + h·f(xₙ, yₙ)."] + [f"Step {i + 1}: y ≈ {dd(ys[i + 1])} at x = {dd(sp.nsimplify(xs[i + 1]))}." for i in range(n_)],
             [dd(wrong1), dd(wrong2), dd(ys[-1] - hh * rhs.subs({x: xs[-1], y: ys[-1]})) if (ys[-1] - hh * rhs.subs({x: xs[-1], y: ys[-1]})) != ys[-1] else dd(ys[-1] + 1)],
             PY("euler", rhs=T(rhs), x0=x0, y0=y0, h=str(hh), n=n_), why=["Stopped one step early", "Used the initial slope for every step", "Made an error updating the slope"])


# ============================================================== S4 Separating variables
@fam("012", mode="mc")
def s4_separate(r, L):
    k_ = rint(r, 2, 6)
    items = [(f"y′ = {k_}xy", f"(1/y) dy = {k_}x dx", [f"y dy = {k_}x dx", f"dy = {k_}xy dx", f"(1/x) dx = {k_}y dy"]),
             (f"y′ = x/y", "y dy = x dx", ["(1/y) dy = x dx", "x dy = y dx", "dy = (x/y) dx"]),
             (f"y′ = {k_}x²/y²", f"y² dy = {k_}x² dx", [f"(1/y²) dy = {k_}x² dx", f"y dy = {k_}x dx", f"dy = {k_}x² dx"]),
             (f"y′ = e^(x - y)", "eʸ dy = eˣ dx", ["e^(-y) dy = eˣ dx", "dy = e^(x - y) dx", "eˣ dy = eʸ dx"]),
             (f"y′ = {k_}y cos(x)", f"(1/y) dy = {k_}cos(x) dx", [f"y dy = {k_}cos(x) dx", f"(1/cos(x)) dy = {k_}y dx", f"dy = {k_}cos(x) dx"])]
    de, good, bad = pick(r, items)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q(f"Which shows the variables of {de} correctly separated?", good, ["Get all y terms with dy and all x terms with dx.", good + "."], options=opts, chk=TXT(good), mode="mc")


# ============================================================== S5 Solving separable equations
@fam("012")
def s5_general(r, L):
    kind = pick(r, ["exp", "circle", "xexp"] if L < 2 else ["exp", "circle", "xexp", "inv"])
    if kind == "exp":
        k_ = rint(r, -12, 12, True)
        de = f"y′ = {k_}y" if abs(k_) != 1 else ("y′ = y" if k_ == 1 else "y′ = -y")
        e_ = {1: "x", -1: "-x"}.get(k_, f"{k_}x")
        ans = f"y = Ce^({e_})".replace("^(x)", "ˣ")
        w = [f"y = e^({e_}) + C".replace("^(x)", "ˣ"), f"y = Cx{str(abs(k_)).translate(SUP)}" if abs(k_) > 1 else "y = Cx", f"y = Ce^({ {1: '-x', -1: 'x'}.get(k_, str(-k_) + 'x') })".replace("^(x)", "ˣ").replace(" ", "")]
        steps = [f"Separate: (1/y) dy = {k_} dx.", f"ln|y| = {k_}x + C₁.", ans + "."]
    elif kind == "circle":
        a_, b_ = rint(r, 1, 9), rint(r, 1, 9)
        sgn = pick(r, [1, -1])
        g = math.gcd(a_, b_)
        a_, b_ = a_ // g, b_ // g
        frac_ = f"{'-' if sgn < 0 else ''}{'' if a_ == 1 else a_}x/({'' if b_ == 1 else b_}y)" if b_ != 1 else f"{'-' if sgn < 0 else ''}{'' if a_ == 1 else a_}x/y"
        de = f"y′ = {frac_}"
        lhs = f"{'' if b_ == 1 else b_}y² {'+' if sgn < 0 else '-'} {'' if a_ == 1 else a_}x²"
        ans = f"{lhs} = C"
        w = [f"{'' if b_ == 1 else b_}y² {'-' if sgn < 0 else '+'} {'' if a_ == 1 else a_}x² = C", f"{'' if a_ == 1 else a_}y² {'+' if sgn < 0 else '-'} {'' if b_ == 1 else b_}x² = C" if a_ != b_ else f"y {'+' if sgn < 0 else '-'} x = C", f"y = {'-' if sgn < 0 else ''}{T(sp.Rational(a_, 2 * b_))}x² + C" if True else ""]
        steps = [f"Separate: {'' if b_ == 1 else b_}y dy = {'-' if sgn < 0 else ''}{'' if a_ == 1 else a_}x dx.", "Integrate both sides and multiply by 2.", ans + "."]
    elif kind == "xexp":
        m = rint(r, 2, 5)
        c = rint(r, -5, 5, True)
        coef = c * m
        de = f"y′ = {coef}x{str(m - 1).translate(SUP) if m > 2 else ''}y"
        ans = f"y = Ce^({'' if c == 1 else '-' if c == -1 else c}x{str(m).translate(SUP)})"
        w = [f"y = e^({'' if c == 1 else '-' if c == -1 else c}x{str(m).translate(SUP)}) + C", f"y = Ce^({coef}x{str(m).translate(SUP)})", f"y = C{'' if c == 1 else '-' if c == -1 else c}x{str(m).translate(SUP)}"]
        steps = [f"Separate: (1/y) dy = {coef}x{str(m - 1).translate(SUP) if m > 2 else ''} dx.", f"ln|y| = {'' if c == 1 else '-' if c == -1 else c}x{str(m).translate(SUP)} + C₁.", ans + "."]
    else:
        k_ = rint(r, 1, 12)
        de = f"y′ = {k_ if k_ > 1 else ''}y²"
        ans = f"y = -1/({k_ if k_ > 1 else ''}x + C)"
        w = [f"y = 1/({k_ if k_ > 1 else ''}x + C)", f"y = (1/3)y³ + C" if False else f"y = -1/({k_ if k_ > 1 else ''}x) + C", f"y = Ce^({k_ if k_ > 1 else ''}x)"]
        steps = [f"Separate: y⁻² dy = {k_} dx.", f"-1/y = {k_}x + C.", ans + "."]
    need(ans not in w and len(set(w)) == 3)
    return Q(f"Find the general solution of {de}.", ans, steps, w, PY("de_general", de=de), why=["Added C instead of multiplying (or placed C incorrectly)", "Integrated incorrectly", "Made a sign error or skipped a step"])


# ============================================================== S6 Initial conditions
@fam("012")
def s6_particular(r, L):
    kind = pick(r, ["exp", "exp_val"] if L == 0 else ["exp", "exp_val", "circle", "logistic_like"] if L == 1 else ["exp_val", "circle", "x_rhs", "newton"])
    if kind in ("exp", "exp_val"):
        k_ = rint(r, -3, 3, True)
        y0 = rint(r, 2, 20)
        if kind == "exp":
            ans = f"y = {y0}e^({k_}x)".replace("^(1x)", "^x").replace("^(-1x)", "^(-x)")
            return Q(f"Solve y′ = {k_}y with y(0) = {y0}.", ans, [f"General: y = Ce^({k_}x).", f"y(0) = C = {y0}.", ans + "."],
                     [f"y = e^({k_}x) + {y0 - 1}".replace("^(1x)", "^x").replace("^(-1x)", "^(-x)"), f"y = {k_}e^({y0}x)", f"y = {y0}e^({-k_}x)".replace("^(1x)", "^x").replace("^(-1x)", "^(-x)")],
                     PY("de_ivp", de=f"y′ = {k_}y", x0=0, y0=y0), why=["Added the constant", "Switched k and the initial value", "Made a sign error"])
        xb = rint(r, 1, 4)
        v = y0 * math.exp(k_ * xb)
        need(0.01 < v < 1e7)
        return Q(f"y′ = {k_}y and y(0) = {y0}. Find y({xb}), rounded to the nearest hundredth.", Rd(v, 2), [f"y = {y0}e^({k_}x).", f"y({xb}) = {y0}e^({k_ * xb}) ≈ {Rd(v, 2)}."],
                 [Rd(y0 + k_ * xb, 2), Rd(y0 * math.exp(k_) * xb, 2), Rd(math.exp(k_ * xb), 2)], PY("de_ivp_val", de=f"y′ = {k_}y", x0=0, y0=y0, at=xb, places=2), why=["Used linear growth", "Multiplied by x outside the exponent", "Forgot the initial value"])
    if kind == "circle":
        x0, y0 = rint(r, 1, 5), rint(r, 1, 5)
        C_ = y0 * y0 + x0 * x0
        ans = f"y = √({C_} - x²)"
        return Q(f"Solve y′ = -x/y with y({x0}) = {y0}.", ans, ["y dy = -x dx, so y² = -x² + C.", f"{y0}² = -{x0}² + C, C = {C_}.", f"y > 0 at the start, so {ans}."],
                 [f"y = √({y0 * y0 - x0 * x0} + x²)" if y0 * y0 - x0 * x0 > 0 else f"y = √(x² + {C_})", f"y = -√({C_} - x²)", f"y = √({C_}) - x"], PY("de_ivp", de="y′ = -x/y", x0=x0, y0=y0),
                 why=["Used the wrong sign for x²", "Chose the negative branch", "Took the square root term by term"])
    if kind == "x_rhs":
        a_, b_ = rint(r, 1, 4), rint(r, -5, 5)
        x0, y0 = 0, rint(r, -6, 6)
        ans = f"y = {T(sp.Rational(a_, 2) * x ** 2 + b_ * x + y0)}"
        return Q(f"Solve y′ = {T(a_ * x + b_)} with y(0) = {y0}.", ans, [f"y = ∫ ({T(a_ * x + b_)}) dx = {T(sp.Rational(a_, 2) * x ** 2 + b_ * x)} + C.", f"y(0) = C = {y0}.", ans + "."],
                 [f"y = {T(a_ * x ** 2 + b_ * x + y0)}", f"y = {T(sp.Rational(a_, 2) * x ** 2 + b_ * x)}", f"y = {T(a_ * x + b_ + y0)}"], PY("de_ivp", de=f"y′ = {T(a_ * x + b_)}", x0=0, y0=y0),
                 why=["Forgot to divide by 2", "Forgot the constant", "Did not integrate"])
    if kind == "logistic_like":
        k_ = rint(r, 1, 3)
        y0 = rint(r, 2, 9)
        ans = f"y = {y0}e^({k_}x²)".replace("^(1x²)", "^(x²)")
        return Q(f"Solve y′ = {2 * k_}xy with y(0) = {y0}.", ans, [f"(1/y) dy = {2 * k_}x dx.", f"ln|y| = {k_}x² + C₁, so y = Ce^({k_}x²).", f"C = {y0}: {ans}."],
                 [f"y = {y0}e^({2 * k_}x²)", f"y = e^({k_}x²) + {y0 - 1}".replace("^(1x²)", "^(x²)"), f"y = {y0}e^({k_}x)".replace("^(1x)", "^x")], PY("de_ivp", de=f"y′ = {2 * k_}xy", x0=0, y0=y0),
                 why=["Forgot to divide by 2 when integrating", "Added the constant", "Integrated x as x"])
    Ta, T0, kk = rint(r, 60, 75), rint(r, 150, 200), pick(r, [sp.Rational(1, 10), sp.Rational(1, 20), sp.Rational(1, 5)])
    tt = rint(r, 2, 15)
    v = Ta + (T0 - Ta) * math.exp(-float(kk) * tt)
    return Q(f"A drink cools by T′ = -{D(F(kk.p, kk.q))}(T - {Ta}) (minutes, °F) from T(0) = {T0}. Find T({tt}), rounded to the nearest tenth.", f"{Rd(v, 1)}°F",
             [f"T - {Ta} = Ce^(-{D(F(kk.p, kk.q))}t); C = {T0 - Ta}.", f"T({tt}) = {Ta} + {T0 - Ta}e^(-{D(F((kk * tt).p, (kk * tt).q))}) ≈ {Rd(v, 1)}°F."],
             [f"{Rd(T0 * math.exp(-float(kk) * tt), 1)}°F", f"{Rd((T0 - Ta) * math.exp(-float(kk) * tt), 1)}°F", f"{Rd(T0 - float(kk) * (T0 - Ta) * tt, 1)}°F"], PY("newton", Ta=Ta, T0=T0, k=str(kk), t=tt),
             why=["Ignored the room temperature", "Forgot to add the room temperature back", "Used a constant cooling rate"], tags=["modeling"])


@fam("012")
def s_pair_slope(r, L):
    """Slopes from a differential equation that come out to 2, 4, or 6, in short and worded styles, so equal answers
    occur in every difficulty third (Partner Check pairs different problems with equal answers)."""
    target = pick(r, [2, 4, 6])
    a_, b_ = rint(r, -4, 4, True), rint(r, -4, 4, True)
    for _ in range(60):
        px, py = rint(r, -5, 5), rint(r, -5, 5)
        if a_ * px + b_ * py == target:
            break
    else:
        raise Reject()
    rhs = a_ * x + b_ * y
    style = pick(r, ["short", "long"])
    if style == "short":
        return Q(f"For y′ = {T(rhs)}, find the slope of the solution curve through ({px}, {py}).", str(target), [f"Substitute x = {px}, y = {py}.", f"y′ = {target}."],
                 [str(a_ * py + b_ * px) if a_ * py + b_ * px != target else str(target + 1), str(py), str(-target)], H(f"P('{T(rhs)}').subs({{x: {px}, y: {py}}})"),
                 why=["Switched x and y", "Gave the y-coordinate", "Made a sign error"])
    return Q(f"A slope field is drawn for y′ = {T(rhs)}. A solution curve passes through ({px}, {py}). What is the slope of the segment drawn at that point, and is the curve rising there?" if False else
             f"A slope field is drawn for y′ = {T(rhs)}. What is the slope of the segment drawn at ({px}, {py})?", str(target),
             ["Each slope-field segment has slope y′ evaluated at its point.", f"y′ = {a_}({px}) + {par(b_)}({py})" if True else "", f"= {a_ * px} + {par(b_ * py)}.", f"Slope = {target}."],
             [str(a_ * py + b_ * px) if a_ * py + b_ * px != target else str(target + 1), str(py), str(-target)], H(f"P('{T(rhs)}').subs({{x: {px}, y: {py}}})"),
             why=["Switched x and y", "Gave the y-coordinate", "Made a sign error"])


@fam("012", mode="mc")
def s_short_k(r, L):
    kind = pick(r, ["find_k", "rate0", "find_C"])
    k_ = rint(r, -9, 9, True)
    c_ = rint(r, 2, 12)
    if kind == "find_k":
        e_ = {1: "x", -1: "-x"}.get(k_, f"{k_}x")
        return Q(f"y = {c_}e^({e_}) is a solution of y′ = ky. Find k.", f"k = {k_}", [f"y′ = {T(c_ * k_)}e^({e_}) = {k_}·y.", f"k = {k_}."], [f"k = {c_}", f"k = {c_ * k_}", f"k = {-k_}"],
                     PY("de_k", c=c_, k=k_), why=["Used the coefficient", "Used the product of the constants", "Made a sign error"])
    if kind == "rate0":
        y0 = rint(r, 2, 20)
        return Q(f"y′ = {k_}y and y(0) = {y0}. Find y′(0).", str(k_ * y0), [f"y′(0) = {k_}·y(0).", f"= {k_}({y0}) = {k_ * y0}."], [str(y0), str(k_ + y0), str(k_)],
                     H(f"{k_}*{y0}"), why=["Gave y(0)", "Added instead of multiplying", "Gave k"])
    y0 = rint(r, 2, 30)
    return Q(f"The general solution of y′ = {k_}y is y = Ce^({ {1: 'x', -1: '-x'}.get(k_, str(k_) + 'x') }). Find C if y(0) = {y0}.".replace(" ", " "), f"C = {y0}",
             ["Substitute x = 0: y(0) = Ce⁰ = C.", f"C = {y0}."], [f"C = {y0 * k_}", f"C = {T(sp.Rational(y0, k_))}", f"C = {y0 - k_}"], PY("de_C", y0=y0), why=["Multiplied by k", "Divided by k", "Subtracted k"])


SKILLS = {
    1: dict(name="Functions Defined by Their Rates of Change", std=["AP FUN-7.A"], fams=[s1_model, s1_slope, s_pair_slope, mc_of(s1_slope)], extra=[err_of(s1_slope), open_of(s1_slope)]),
    2: dict(name="Verifying Solutions to Differential Equations", std=["AP FUN-7.B"], fams=[s2_verify, s2_findk, s_short_k], extra=[err_of(s2_findk), open_of(s2_findk)]),
    3: dict(name="Estimating Solutions to Differential Equations", std=["AP FUN-7.C"], fams=[s3_euler, s1_slope, reuse(s_pair_slope, (0, 1, 2), 'e'), mc_of(s3_euler)], extra=[err_of(s3_euler), open_of(s3_euler)]),
    4: dict(name="Separating Variables", std=["AP FUN-7.D"], fams=[s4_separate, reuse(s5_general, (0, 1, 2), "s")], extra=[err_of(reuse(s5_general, (0, 1, 2), "se")), open_of(reuse(s5_general, (0, 1, 2), "so"))]),
    5: dict(name="Solving Separable Differential Equations", std=["AP FUN-7.D"], fams=[s5_general, reuse(s_short_k, (0, 1, 2), 'g')], extra=[err_of(s5_general), open_of(s5_general)]),
    6: dict(name="Initial Conditions and Particular Solutions", std=["AP FUN-7.E", "AP FUN-7.F"], fams=[s6_particular, reuse(s_pair_slope, (0, 1, 2), 'p'), reuse(s_short_k, (0, 1, 2), 'i')], extra=[err_of(s6_particular), open_of(s6_particular)]),
}
