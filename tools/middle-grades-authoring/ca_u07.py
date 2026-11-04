"""Calculus Unit 7 — Applications of Integrals (applications-integrals)."""
from hslib import *
import ca_u05 as C5

UNIT_ID = "applications-integrals"
ABBR = "aoi"
integ = C5.integ


def pw(e):
    s_ = T(e)
    return f"({s_})" if " " in s_ else s_


# ============================================================== S1 Interpreting definite integrals
@fam("012", mode="mc")
def s1_meaning(r, L):
    a, b = sorted(r.sample(range(0, 13), 2))
    ctxs = [("r(t)", "the rate water flows into a tank, in gallons per minute, t minutes after noon", "the total gallons of water that flow into the tank from t = {a} to t = {b} minutes", "gallons"),
            ("v(t)", "the velocity of a car in miles per hour, t hours after it leaves", "the car's change in position (displacement) from t = {a} to t = {b} hours", "miles"),
            ("P′(t)", "the rate of change of a population, in people per year", "the change in population from year {a} to year {b}", "people"),
            ("C′(x)", "the marginal cost, in dollars per item, of producing x items", "the additional cost of increasing production from {a} to {b} items", "dollars")]
    fn, desc, good_t, unit = pick(r, ctxs)
    good = good_t.format(a=a, b=b)
    var = "x" if fn.startswith("C") else "t"
    bad = [f"the rate at {var} = {b}", f"the average rate of change from {var} = {a} to {var} = {b}", f"the value of {fn.split('(')[0].rstrip('′')} at {var} = {b}"]
    opts = [(good, True)] + [(b_, False) for b_ in bad]
    r.shuffle(opts)
    return Q(f"{fn} is {desc}. What does ∫ from {a} to {b} {fn} d{var} represent (units: {unit})?", good, ["The integral of a rate gives the net amount accumulated.", good + "."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


@fam("012")
def s1_units(r, L):
    a, b = 0, rint(r, 2, 8)
    c2, c1 = rint(r, 1, 3), rint(r, 2, 12)
    rate = c2 * t ** 2 + c1 if L else c1 + c2 * t
    v = sp.integrate(rate, (t, a, b))
    return Q(f"Oil leaks from a tank at r(t) = {T(rate)} liters per hour. How many liters leak during the first {b} hours?", f"{T(v)} liters",
             [f"Total = ∫ from 0 to {b} ({T(rate)}) dt.", f"= {T(v)} liters."], [f"{T(rate.subs(t, b))} liters", f"{T(rate.subs(t, b) * b)} liters", f"{T(sp.Rational(v, b))} liters"],
             H(f"integrate(P('{T(rate)}'), (t, 0, {b}))"), why=["Used the rate at the end instead of the total", "Multiplied the final rate by the time", "Found the average rate"], tags=["modeling"])


# ============================================================== S2 Accumulation and net change
@fam("012")
def s2_net(r, L):
    A0 = rint(r, 20, 200)
    T_ = rint(r, 2, 6)
    rin = rint(r, 2, 9) * t + rint(r, 1, 10)
    if L == 0:
        v = A0 + sp.integrate(rin, (t, 0, T_))
        return Q(f"A reservoir holds {A0} thousand gallons at t = 0. Water flows in at r(t) = {T(rin)} thousand gallons per day. How much is in the reservoir at t = {T_} days?", f"{T(v)} thousand gallons",
                 [f"Amount = {A0} + ∫ from 0 to {T_} ({T(rin)}) dt.", f"= {A0} + {T(v - A0)} = {T(v)}."], [f"{T(v - A0)} thousand gallons", f"{T(A0 + rin.subs(t, T_))} thousand gallons", f"{T(A0 + rin.subs(t, T_) * T_)} thousand gallons"],
                 H(f"{A0} + integrate(P('{T(rin)}'), (t, 0, {T_}))"), why=["Forgot the initial amount", "Added the rate instead of the integral", "Multiplied the final rate by the time"], tags=["modeling"])
    rout = rint(r, 5, 30)
    v = A0 + sp.integrate(rin - rout, (t, 0, T_))
    return Q(f"A tank holds {A0} L at t = 0. Water enters at E(t) = {T(rin)} L/min and leaves at a constant {rout} L/min. How much water is in the tank at t = {T_} minutes?", f"{T(v)} L",
             [f"Amount = {A0} + ∫ from 0 to {T_} (E(t) - {rout}) dt.", f"= {T(v)} L."], [f"{T(A0 + sp.integrate(rin, (t, 0, T_)))} L", f"{T(sp.integrate(rin - rout, (t, 0, T_)))} L", f"{T(A0 + sp.integrate(rin, (t, 0, T_)) + rout * T_)} L"],
             H(f"{A0} + integrate(P('{T(rin)}') - {rout}, (t, 0, {T_}))"), why=["Ignored the outflow", "Forgot the initial amount", "Added the outflow"], tags=["modeling"])


# ============================================================== S3 Average value
@fam("012")
def s3_avg(r, L):
    kind = pick(r, ["poly"] if L == 0 else ["poly", "trig", "recip"] if L == 1 else ["trig", "exp", "poly"])
    if kind == "poly":
        f = polyx([rint(r, -3, 3, True) * 3, rint(r, -4, 4) * 2, rint(r, -6, 6)])
        a, b = sorted(r.sample(range(-2, 6), 2))
    elif kind == "trig":
        f = rint(r, 1, 6) * pick(r, [sp.sin(x), sp.cos(x)])
        a, b = pick(r, [(0, sp.pi), (0, sp.pi / 2), (0, sp.pi / 3)])
    elif kind == "recip":
        f = sp.Integer(rint(r, 1, 6)) / x
        a, b = 1, sp.E
    else:
        f = rint(r, 1, 4) * sp.exp(x)
        a, b = 0, pick(r, [1, 2])
    v = sp.simplify(sp.integrate(f, (x, a, b)) / (b - a))
    need(v != 0)
    w = [sp.simplify(sp.integrate(f, (x, a, b))), sp.simplify((f.subs(x, a) + f.subs(x, b)) / 2), sp.simplify((sp.integrate(f, x).subs(x, b) - sp.integrate(f, x).subs(x, a)) * (b - a))]
    wt = [T(z) for z in w]
    need(T(v) not in wt and len(set(wt)) == 3)
    return Q(f"Find the average value of f(x) = {T(f)} on [{T(a)}, {T(b)}].", T(v), ["f_avg = (1 ÷ (b - a)) ∫ from a to b f(x) dx.", f"∫ = {T(sp.simplify(sp.integrate(f, (x, a, b))))}; divide by {T(b - a)}.", f"= {T(v)}."], wt,
             H(f"integrate(P('{T(f)}'), (x, P('{T(a)}'), P('{T(b)}')))/(P('{T(b)}') - P('{T(a)}'))"), why=["Forgot to divide by b - a", "Averaged the endpoint values", "Multiplied by b - a"])


# ============================================================== S4 Motion and displacement
@fam("012")
def s4_disp(r, L):
    p, q = sorted(r.sample(range(1, 7), 2))
    v_ = sp.expand((t - p) * (t - q)) * pick(r, [1, 2, 3])
    T_ = rint(r, 1, 8)
    kind = pick(r, ["disp", "pos"]) if L else "disp"
    d = sp.integrate(v_, (t, 0, T_))
    if kind == "disp":
        return Q(f"A particle moves with velocity v(t) = {T(v_)} m/s. Find its displacement from t = 0 to t = {T_}.", f"{T(d)} m", [f"Displacement = ∫ from 0 to {T_} v(t) dt.", f"= {T(d)} m."],
                 [f"{T(sp.integrate(sp.Abs(v_), (t, 0, T_)))} m" if sp.integrate(sp.Abs(v_), (t, 0, T_)) != d else f"{T(d + 1)} m", f"{T(v_.subs(t, T_))} m", f"{T(sp.diff(v_, t).subs(t, T_))} m"],
                 H(f"integrate(P('{T(v_)}'), (t, 0, {T_}))"), why=["Found total distance instead", "Gave the velocity", "Gave the acceleration"], tags=["modeling"])
    s0 = rint(r, -10, 10)
    return Q(f"A particle moves with velocity v(t) = {T(v_)} m/s and is at s(0) = {s0} m. Find its position at t = {T_}.", f"{T(s0 + d)} m", [f"s({T_}) = s(0) + ∫ from 0 to {T_} v(t) dt.", f"= {s0} + {T(d)} = {T(s0 + d)} m."],
             [f"{T(d)} m", f"{T(s0 + v_.subs(t, T_))} m", f"{T(s0 - d)} m"], H(f"{s0} + integrate(P('{T(v_)}'), (t, 0, {T_}))"), why=["Forgot the initial position", "Added the velocity instead", "Subtracted the displacement"], tags=["modeling"])


# ============================================================== S5 Total distance
@fam("012")
def s5_total(r, L):
    p = rint(r, 1, 5)
    c = pick(r, [1, 2, 3, 4])
    v_ = c * (t - p) if L == 0 else c * (t - p) * (t - rint(r, p + 1, p + 4)) if r.random() < 0.6 else c * (t - p)
    T_ = rint(r, p + 1, p + 5)
    D_ = sp.integrate(sp.Abs(v_), (t, 0, T_))
    disp = sp.integrate(v_, (t, 0, T_))
    need(D_ != abs(disp))
    zs = sorted(z for z in sp.solve(v_, t) if 0 < z < T_)
    return Q(f"A particle moves with velocity v(t) = {T(v_)} ft/s. Find the total distance traveled from t = 0 to t = {T_}.", f"{T(D_)} ft",
             [f"v(t) = 0 at t = {', '.join(T(z) for z in zs)}.", "Total distance = ∫ |v(t)| dt: integrate on each piece and add absolute values.", f"= {T(D_)} ft."],
             [f"{T(disp)} ft", f"{T(abs(disp))} ft" if abs(disp) != disp else f"{T(D_ + 2)} ft", f"{T(abs(v_.subs(t, T_)) * T_)} ft"], H(f"integrate(Abs(P('{T(v_)}')), (t, 0, {T_}))"),
             why=["Found displacement instead", "Took the absolute value of the displacement", "Multiplied the final speed by the time"], tags=["modeling"])


# ============================================================== S6 Area between curves
@fam("012")
def s6_area(r, L):
    p, q = sorted(r.sample(range(-3, 5), 2))
    a_ = rint(r, 1, 3)
    if L < 2:
        top = rint(r, -3, 3) * x + rint(r, -6, 6)
        bot = sp.expand(top - (-a_ * (x - p) * (x - q)))
        f_, g_ = top, bot
    else:
        k_ = rint(r, 1, 2)
        bot = sp.expand(x ** 3 - k_ * x)
        top = sp.expand(bot + a_ * (x - p) * (x - q) * -1)
        f_, g_ = top, bot
    v = sp.integrate(f_ - g_, (x, p, q))
    need(v > 0)
    return Q(f"Find the area of the region bounded by y = {T(f_)} and y = {T(g_)}.", T(v),
             [f"Intersections: {T(f_)} = {T(g_)} at x = {p} and x = {q}.", f"On [{p}, {q}], y = {T(f_)} is on top.", f"Area = ∫ from {p} to {q} ((top) - (bottom)) dx = {T(v)}."],
             [T(-v), T(sp.integrate(f_ + g_, (x, p, q))) if sp.integrate(f_ + g_, (x, p, q)) not in (v, -v) else T(2 * v), T(sp.integrate(f_, (x, p, q))) if sp.integrate(f_, (x, p, q)) not in (v, -v) else T(v + 1)],
             PY("area_between", f=T(f_), g=T(g_)), why=["Subtracted top minus bottom in the wrong order", "Added the functions", "Integrated only the top curve"],
             diagram=area_fig(f_, g_, p, q) if L == 0 else None)


def area_fig(f_, g_, p, q):
    ff, gf = sp.lambdify(x, f_, "math"), sp.lambdify(x, g_, "math")
    xs = [p - 2 + (q - p + 4) * i / 300 for i in range(301)]
    ys = [ff(v) for v in xs] + [gf(v) for v in xs]
    lo, hi = math.floor(min(ys + [0])) - 1, math.ceil(max(ys + [0])) + 1
    if hi - lo > 24:
        return None
    span = max(hi - lo, q - p + 4)
    return {"alt": f"Graphs of y = {T(f_)} and y = {T(g_)} crossing at x = {p} and x = {q}.",
            "draw": curve_draw([(xs, [ff(v) for v in xs], "solid"), (xs, [gf(v) for v in xs], "dashed")], (p - 2, q + 2), (lo, hi), pts=[(p, f_.subs(x, p), ""), (q, f_.subs(x, q), "")], label_every=2 if span > 12 else 1)}


# ============================================================== S7 Volumes
@fam("012")
def s7_volume(r, L):
    kind = pick(r, ["disk"] if L == 0 else ["disk", "washer", "square"] if L == 1 else ["washer", "square", "semicircle", "disk_y"])
    b = rint(r, 1, 4)
    if kind == "disk":
        f = pick(r, [x, x ** 2, sp.sqrt(x), 2 * x, x + 1])
        v = sp.pi * sp.integrate(f ** 2, (x, 0, b))
        q = f"The region under y = {T(f)} from x = 0 to x = {b} is revolved about the x-axis. Find the volume."
        steps = ["Disk method: V = π∫ [f(x)]² dx.", f"V = π∫ from 0 to {b} ({T(f)})² dx = {T(v)}."]
        w = [T(sp.integrate(f ** 2, (x, 0, b))), T(sp.pi * sp.integrate(f, (x, 0, b))), T(2 * sp.pi * sp.integrate(f ** 2, (x, 0, b)))]
        code = f"pi*integrate(P('{T(f)}')**2, (x, 0, {b}))"
    elif kind == "washer":
        b = pick(r, [1, 2])
        f, g = (x, x ** 2) if b == 1 else (2 * x, x ** 2)
        v = sp.pi * sp.integrate(f ** 2 - g ** 2, (x, 0, b))
        q = f"The region between y = {T(f)} and y = {T(g)} (from x = 0 to x = {b}) is revolved about the x-axis. Find the volume."
        steps = ["Washer method: V = π∫ (R² - r²) dx.", f"R = {T(f)}, r = {T(g)}.", f"V = {T(v)}."]
        w = [T(sp.pi * sp.integrate((f - g) ** 2, (x, 0, b))), T(sp.pi * sp.integrate(f - g, (x, 0, b))), T(sp.integrate(f ** 2 - g ** 2, (x, 0, b)))]
        code = f"pi*integrate(P('{T(f)}')**2 - P('{T(g)}')**2, (x, 0, {b}))"
    elif kind in ("square", "semicircle"):
        f = pick(r, [x, sp.sqrt(x), 4 - x, x ** 2])
        if f == 4 - x:
            b = 4
        side = f
        A = side ** 2 if kind == "square" else sp.pi * side ** 2 / 8
        v = sp.integrate(A, (x, 0, b))
        q = f"A solid has base bounded by y = {T(f)}, the x-axis, and x = 0 to x = {b}. Cross sections perpendicular to the x-axis are {'squares' if kind == 'square' else 'semicircles'} with a side (diameter) in the base. Find the volume."
        steps = [f"Cross-section area A(x) = {'s²' if kind == 'square' else '(1/2)π(s/2)² = πs² ÷ 8'} with s = {T(f)}.", f"V = ∫ from 0 to {b} A(x) dx = {T(v)}."]
        w = [T(sp.pi * sp.integrate(f ** 2, (x, 0, b))) if kind == "square" else T(sp.pi * sp.integrate(f ** 2, (x, 0, b)) / 2), T(sp.integrate(f, (x, 0, b))), T(2 * v)]
        code = f"integrate(P('{T(f)}')**2, (x, 0, {b}))" if kind == "square" else f"integrate(pi*P('{T(f)}')**2/8, (x, 0, {b}))"
    else:
        hh = rint(r, 1, 4)
        v = sp.pi * sp.integrate(y, (y, 0, hh))
        q = f"The region bounded by y = x², the y-axis, and y = {hh} is revolved about the y-axis. Find the volume."
        steps = ["Disks perpendicular to the y-axis: radius x = √y.", f"V = π∫ from 0 to {hh} (√y)² dy = {T(v)}."]
        w = [T(sp.pi * sp.integrate(y ** 2, (y, 0, hh))), T(sp.pi * sp.integrate(x ** 4, (x, 0, sp.sqrt(hh)))), T(sp.integrate(y, (y, 0, hh)))]
        code = f"pi*integrate(y, (y, 0, {hh}))"
    need(T(v) not in w and len(set(w)) == 3)
    return Q(q, T(v), steps, w, H(code), why=["Forgot π (or used the wrong cross-section area)", "Did not square the radius", "Doubled or misused the formula"], tags=["modeling"])


# ============================================================== S8 Applied integral models
@fam("012")
def s8_model(r, L):
    kind = pick(r, ["rain", "traffic", "bacteria"])
    if kind == "rain":
        a_, b_ = rint(r, 1, 4), rint(r, 2, 8)
        R = sp.Rational(a_, 10) * t + sp.Rational(b_, 10)
        T_ = rint(r, 2, 12)
        v = sp.integrate(R, (t, 0, T_))
        return Q(f"Rain falls at R(t) = {D(F(a_, 10))}t + {D(F(b_, 10))} inches per hour. How much rain falls in the first {T_} hours?", f"{D(F(v.p, v.q))} inches",
                 [f"∫ from 0 to {T_} R(t) dt.", f"= {D(F(v.p, v.q))} inches."], [f"{D(F(R.subs(t, T_).p, R.subs(t, T_).q))} inches", f"{D(F((R.subs(t, T_) * T_).p, (R.subs(t, T_) * T_).q))} inches", f"{D(F((v / T_).p, (v / T_).q)) if (v / T_).q in (1, 2, 4, 5, 10, 20, 25, 50, 100) else D(F(b_ * T_, 10))} inches"],
                 H(f"integrate({a_}/Rational(10)*t + {b_}/Rational(10), (t, 0, {T_}))"), why=["Gave the final rate", "Multiplied the final rate by time", "Found the average rate"], tags=["modeling"])
    if kind == "traffic":
        c_ = rint(r, 20, 90)
        T_ = rint(r, 1, 4)
        Rf = c_ + 10 * sp.sin(sp.pi * t / 2) if L else c_ + 6 * t
        v = sp.integrate(Rf, (t, 0, T_))
        return Q(f"Cars pass a sensor at a rate of C(t) = {T(Rf)} cars per hour. How many cars pass in the first {T_} hours?" + (" Round to the nearest whole car." if L else ""),
                 (Rd(float(v), 0) + " cars") if L else f"{T(v)} cars", [f"∫ from 0 to {T_} C(t) dt.", f"≈ {Rd(float(v), 0) if L else T(v)} cars."],
                 [f"{Rd(float(Rf.subs(t, T_)), 0)} cars", f"{Rd(float(Rf.subs(t, T_) * T_), 0)} cars", f"{Rd(float(c_ * T_), 0)} cars" if Rd(float(c_ * T_), 0) != Rd(float(v), 0) else f"{Rd(float(v) + 5, 0)} cars"],
                 H(f"integrate(P('{T(Rf)}'), (t, 0, {T_}))", "round", places=0) if L else H(f"integrate(P('{T(Rf)}'), (t, 0, {T_}))"), why=["Gave the final rate", "Multiplied the final rate by time", "Ignored the changing part of the rate"], tags=["modeling"])
    N0, k_ = rint(r, 100, 900), pick(r, [sp.Rational(1, 10), sp.Rational(1, 5), sp.Rational(1, 4)])
    T_ = rint(r, 2, 8)
    rate = N0 * k_ * sp.exp(k_ * t)
    v = N0 + sp.integrate(rate, (t, 0, T_))
    return Q(f"A culture starts with {N0} bacteria and grows at N′(t) = {T(N0 * k_)}e^({D(F(k_.p, k_.q))}t) bacteria per hour. How many are present at t = {T_}? Round to the nearest whole number.", Rd(float(v), 0),
             [f"N({T_}) = {N0} + ∫ from 0 to {T_} N′(t) dt.", f"≈ {Rd(float(v), 0)}."], [Rd(float(v - N0), 0), Rd(float(N0 + rate.subs(t, T_)), 0), Rd(float(rate.subs(t, T_) * T_), 0)],
             H(f"{N0} + integrate(P('{T(N0 * k_)}e^({D(F(k_.p, k_.q))}t)'), (t, 0, {T_}))", "round", places=0), why=["Forgot the initial amount", "Added the final rate", "Multiplied the final rate by time"], tags=["modeling"])


SKILLS = {
    1: dict(name="Interpreting Definite Integrals in Context", std=["AP CHA-4.A", "AP CHA-4.B"], fams=[s1_meaning, s1_units], extra=[err_of(s1_units), open_of(s1_units)]),
    2: dict(name="Accumulation and Net Change", std=["AP CHA-4.E"], fams=[s2_net], extra=[err_of(s2_net), open_of(s2_net)]),
    3: dict(name="Average Value of a Function", std=["AP CHA-4.B"], fams=[s3_avg], extra=[err_of(s3_avg), open_of(s3_avg)]),
    4: dict(name="Motion and Displacement", std=["AP CHA-4.C"], fams=[s4_disp], extra=[err_of(s4_disp), open_of(s4_disp)]),
    5: dict(name="Total Distance Traveled", std=["AP CHA-4.C"], fams=[s5_total], extra=[err_of(s5_total), open_of(s5_total)]),
    6: dict(name="Area Between Curves", std=["AP CHA-5.A", "AP CHA-5.B"], fams=[s6_area], extra=[err_of(s6_area), open_of(s6_area)]),
    7: dict(name="Volumes of Solids", std=["AP CHA-5.C", "AP CHA-5.D"], fams=[s7_volume], extra=[err_of(s7_volume), open_of(s7_volume)]),
    8: dict(name="Integral Models in Applied Contexts", std=["AP CHA-4.E"], fams=[s8_model], extra=[err_of(s8_model), open_of(s8_model)]),
}
