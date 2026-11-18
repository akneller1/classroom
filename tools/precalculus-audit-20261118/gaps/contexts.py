"""Real-world context families for Precalculus audit item #5 (batch P4b).

Same contract as families.py. Each unit gets 9 context problems per level on one existing skill
(CONTEXT below); verify.py recomputes them from check data.
Rounded answers are written "≈ 12.3 ft" so the practice test grades them to the stated place.
"""
import math
from fractions import Fraction as F

from families import I, need, ri, nz, num, sup, mc_only  # noqa: F401
from core import safe_round, g  # noqa: E402

NAMES = ["Ava", "Ben", "Chloe", "Diego", "Emma", "Farah", "Gabe", "Hana", "Isaac", "Jada", "Kenji", "Leah", "Mateo", "Nia", "Omar", "Priya"]


def rd(v, dp):
    safe_round(v, dp)
    s = f"{v:.{dp}f}"
    return s


def money(v):
    return f"${v:,}"


def cash(v, dp):
    """Rounded dollars: ≈ $4,886.68 or ≈ $8,430."""
    safe_round(v, dp)
    return f"≈ ${v:,.{dp}f}" if v >= 0 else f"≈ -${-v:,.{dp}f}"


def usd(v):
    """Exact dollars: $190, -$7.60."""
    v = F(v)
    t = f"{abs(float(v)):,.2f}" if v.denominator != 1 else f"{abs(v.numerator):,}"
    return ("-$" if v < 0 else "$") + t


# ================================================================== equations-inequalities: systems (A-REI.C.6, A-CED.A.3)
def ctx_tickets(r, L):
    a, s = ri(r, 8, 18), ri(r, 3, 7)
    need(a > s)
    x, y = ri(r, 40, 300), ri(r, 40, 300)
    n, R = x + y, a * x + s * y
    ev = r.choice(["a school play", "a concert", "a basketball game", "a science fair"])
    prompt = f"Tickets for {ev} cost ${a} for adults and ${s} for students. {n} tickets were sold for a total of {money(R)}. How many adult tickets were sold?"
    steps = [f"Let a = adult tickets and s = student tickets: a + s = {n} and {a}a + {s}s = {R}.",
             f"Substitute s = {n} - a: {a}a + {s}({n} - a) = {R}, so {a - s}a = {R - s * n}.", f"a = {x} adult tickets."]
    wr = [(str(y), "found the number of student tickets"), (str(R // a), "divided the total by the adult price"),
          (str(n // 2), "split the tickets evenly"), (str(x + 10), "made an arithmetic slip")]
    return I(prompt, str(x), steps, wr, dict(k="ctx_tickets", a=a, s=s, n=n, R=R, show=[f"${a}", f"${s}", str(n), money(R)]), "ctx_tickets")


def ctx_invest(r, L):
    r1, r2 = r.choice([(3, 5), (2, 6), (4, 7), (3, 8), (5, 9), (2, 5)])
    x, y = 100 * ri(r, 10, 90), 100 * ri(r, 10, 90)
    P, Ivl = x + y, F(r1 * x + r2 * y, 100)
    need(Ivl.denominator == 1)
    who = r.choice(NAMES)
    prompt = (f"{who} invests {money(P)}, part at {r1}% simple annual interest and the rest at {r2}%. "
              f"After one year the total interest is {money(int(Ivl))}. How much was invested at {r1}%?")
    steps = [f"x + y = {P} and 0.0{r1}x + 0.0{r2}y = {int(Ivl)}." if r2 < 10 else "",
             f"Substitute y = {P} - x: 0.0{r1}x + 0.0{r2}({P} - x) = {int(Ivl)}, so -0.0{r2 - r1}x = {int(Ivl) - F(r2 * P, 100)}.",
             f"x = {money(x)}."]
    steps = [s for s in steps if s]
    wr = [(money(y), "found the amount at the other rate"), (money(P // 2), "split the money evenly"),
          (money(int(Ivl) * 100 // r1), "assumed all the money earned the first rate"), (money(x + 500), "made an arithmetic slip")]
    return I(prompt, money(x), steps, wr, dict(k="ctx_invest", r1=r1, r2=r2, P=P, I=int(Ivl), show=[money(P), f"{r1}%", f"{r2}%", money(int(Ivl))]), "ctx_invest")


def ctx_mixture(r, L):
    p1, p2 = r.choice([(10, 40), (20, 50), (15, 45), (10, 30), (25, 60), (5, 35)])
    x, y = 2 * ri(r, 2, 20), 2 * ri(r, 2, 20)
    n = x + y
    t = F(p1 * x + p2 * y, n)
    need(t.denominator == 1)
    thing = r.choice(["acid solution", "saline solution", "juice drink", "antifreeze mixture"])
    prompt = f"A chemist mixes a {p1}% {thing} with a {p2}% {thing} to make {n} liters of a {t}% {thing}. How many liters of the {p1}% {thing} are needed?"
    steps = [f"x + y = {n} and {p1}x + {p2}y = {t}({n}) = {t * n}.",
             f"Substitute y = {n} - x: {p1}x + {p2}({n} - x) = {t * n}, so {p1 - p2}x = {t * n - p2 * n}.", f"x = {x} liters."]
    wr = [(f"{y} liters", "found the amount of the other solution"), (f"{n // 2} liters", "split the volume evenly"),
          (f"{num(F(t * n, p1))} liters", "divided by the first percentage"), (f"{x + 2} liters", "made an arithmetic slip")]
    return I(prompt, f"{x} liters", steps, wr, dict(k="ctx_mixture", p1=p1, p2=p2, n=n, t=int(t), show=[f"{p1}%", f"{p2}%", f"{n} liters", f"{t}%"]), "ctx_mixture")


# ================================================================== functions: exponential models (F-LE.A.2, F-IF.C.8b)
def ctx_halflife(r, L):
    h = r.choice([5, 6, 8, 10, 12, 15, 20, 30])
    k = ri(r, 2, 5)
    A = r.choice([64, 80, 96, 128, 160, 192, 256, 320, 400, 512, 640, 800])
    rem = F(A, 2 ** k)
    need(rem.denominator == 1)
    sub = r.choice(["a medicine in the bloodstream", "a radioactive sample", "caffeine in the body"])
    unit = "mg" if sub != "a radioactive sample" else "g"
    tu = "hours" if sub != "a radioactive sample" else "days"
    prompt = f"The amount of {sub} has a half-life of {h} {tu}. Starting with {A} {unit}, how much remains after {h * k} {tu}?"
    steps = [f"{h * k} {tu} is {k} half-lives.", f"A = {A}(1/2)^{k} = {A}/{2 ** k} = {rem} {unit}."]
    wr = [(f"{num(F(A, 2 * k))} {unit}", "divided by 2 × the number of half-lives"), (f"{num(F(A, 2))} {unit}", "used only one half-life"),
          (f"{num(F(A, 2 ** (k - 1)))} {unit}", "counted one half-life too few"), (f"{num(F(A * (h * k - h), h * k))} {unit}" if (A * (h * k - h)) % (h * k) == 0 else f"{A - rem} {unit}", "subtracted instead of halving")]
    return I(prompt, f"{rem} {unit}", steps, wr, dict(k="ctx_halflife", A=A, h=h, t=h * k, show=[f"{h} {tu}", f"{A} {unit}", f"{h * k} {tu}"]), "ctx_halflife")


def ctx_compound(r, L):
    P = 500 * ri(r, 2, 20)
    rate = r.choice([2, 3, 4, 5, 6, 7])
    t = ri(r, 3, 15)
    n = r.choice([1, 4, 12]) if L > 0 else 1
    A = P * (1 + rate / 100 / n) ** (n * t)
    ans = cash(A, 2)
    nn = {1: "annually", 4: "quarterly", 12: "monthly"}[n]
    prompt = f"{money(P)} is deposited in an account that earns {rate}% annual interest compounded {nn}. What is the balance after {t} years? Round to the nearest cent."
    steps = [f"A = P(1 + r/n)^(nt) = {P}(1 + 0.0{rate}/{n})^({n} · {t})." if n > 1 else f"A = P(1 + r)^t = {P}(1.0{rate})^{t}.",
             f"A {ans}."]
    simple = P * (1 + rate / 100 * t)
    wr = [(cash(simple, 2) if abs(simple - A) > 0.01 else cash(A + 10, 2), "used simple interest"),
          (cash(P * (1 + rate / 100) ** t, 2) if n > 1 else cash(P * (1 + rate / 100) ** (t - 1), 2), "compounded the wrong number of times"),
          (cash(A - P, 2), "gave only the interest earned"),
          (cash(P * math.exp(rate / 100 * t), 2) if abs(P * math.exp(rate / 100 * t) - A) > 0.01 else cash(A - 10, 2), "used continuous compounding")]
    return I(prompt, ans, steps, wr, dict(k="ctx_compound", P=P, rate=rate, n=n, t=t, show=[money(P), f"{rate}%", nn, f"{t} years"]), "ctx_compound")


def ctx_depreciate(r, L):
    V = 1000 * ri(r, 15, 45)
    p = r.choice([8, 10, 12, 15, 18, 20])
    t = ri(r, 2, 8)
    A = V * (1 - p / 100) ** t
    ans = cash(A, 0)
    what = r.choice(["A car", "A delivery van", "A tractor", "A boat"])
    prompt = f"{what} bought for {money(V)} loses {p}% of its value each year. What is it worth after {t} years? Round to the nearest dollar."
    steps = [f"V = {V}(1 - 0.{p:02d})^{t} = {V}({1 - p / 100:g})^{t}.", f"V {ans}."]
    wr = [(cash(V * (1 - p / 100 * t), 0) if V * (1 - p / 100 * t) > 0 else cash(A + 500, 0), "subtracted the same amount each year"),
          (cash(V * (1 - p / 100) ** (t + 1), 0), "used one year too many"),
          (cash(V * (1 + p / 100) ** t, 0), "used growth instead of decay"), (cash(V * (1 - p / 100) ** (t - 1), 0), "used one year too few")]
    return I(prompt, ans, steps, wr, dict(k="ctx_depreciate", V=V, p=p, t=t, show=[money(V), f"{p}%", f"{t} years"]), "ctx_depreciate")


# ================================================================== trigonometric functions: sinusoidal models (F-TF.B.5)
def ctx_ferris(r, L):
    d = 2 * ri(r, 15, 70)
    c = d // 2 + ri(r, 2, 8)
    T = r.choice([4, 6, 8, 10, 12, 15, 20, 24, 30])
    rr = d // 2
    frac = r.choice([F(1, 4), F(1, 2), F(1, 6), F(1, 3), F(3, 4), F(2, 3)] if L > 0 else [F(1, 4), F(1, 2), F(3, 4)])
    t = frac * T
    need(t.denominator == 1)
    h = c - rr * math.cos(2 * math.pi * float(frac))
    hv = F(c) - rr * {F(1, 4): 0, F(1, 2): -1, F(1, 6): F(1, 2), F(1, 3): F(-1, 2), F(3, 4): 0, F(2, 3): F(-1, 2)}[frac]
    need(abs(float(hv) - h) < 1e-9)
    prompt = (f"A Ferris wheel {d} feet in diameter turns once every {T} minutes; its center is {c} feet above the ground. A rider boards at the bottom. "
              f"The height is h(t) = {c} - {rr} cos(2πt/{T}). How high is the rider after {t} minutes?")
    ang = 2 * frac
    at = "π" if ang == 1 else (f"{num(ang)}π" if ang.denominator == 1 else f"({num(ang)})π")
    steps = [f"2π({t})/{T} = {at}", f"h = {c} - {rr} cos({at}) = {num(hv)} feet."]
    steps[0] += "."
    wr = [(f"{num(F(c) + rr * {F(1, 4): 0, F(1, 2): -1, F(1, 6): F(1, 2), F(1, 3): F(-1, 2), F(3, 4): 0, F(2, 3): F(-1, 2)}[frac])} feet", "added instead of subtracting the cosine term"),
          (f"{c + rr} feet" if hv != c + rr else f"{c - rr} feet", "gave the top or bottom of the wheel"), (f"{c} feet" if hv != c else f"{c + rr} feet", "used the center height"),
          (f"{num(F(rr) * (1 - {F(1, 4): 0, F(1, 2): -1, F(1, 6): F(1, 2), F(1, 3): F(-1, 2), F(3, 4): 0, F(2, 3): F(-1, 2)}[frac]))} feet", "measured from the bottom of the wheel")]
    return I(prompt, f"{num(hv)} feet", steps, wr, dict(k="ctx_ferris", c=c, rr=rr, T=T, t=int(t), show=[f"{c} - {rr} cos(2πt/{T})", f"after {t} minutes"]), "ctx_ferris")


def ctx_tide(r, L):
    H = ri(r, 8, 18) + r.choice([0, F(1, 2)])
    Lw = ri(r, 1, 6) + r.choice([0, F(1, 2)])
    need(H > Lw)
    P = r.choice([6, F(25, 4), F(13, 2), 6])
    ask = r.choice(["amplitude", "midline", "period"])
    hh = f"{g(H)} feet"
    ll = f"{g(Lw)} feet"
    prompt = (f"At a harbor, high tide is {hh} and the next low tide, {g(P)} hours later, is {ll}. "
              f"The water depth is modeled by a sinusoidal function. What is the {ask} of the model?")
    amp, mid, per = (H - Lw) / 2, (H + Lw) / 2, 2 * P
    ans = {"amplitude": f"{g(amp)} feet", "midline": f"d = {g(mid)}", "period": f"{g(per)} hours"}[ask]
    steps = [f"Amplitude = ({g(H)} - {g(Lw)})/2 = {g(amp)}; midline = ({g(H)} + {g(Lw)})/2 = {g(mid)}.",
             f"High to low is half a cycle, so the period is 2 · {g(P)} = {g(per)} hours.", f"The {ask} is {ans}."]
    if ask == "amplitude":
        wr = [(f"{g(H - Lw)} feet", "used the full range"), (f"{g(mid)} feet", "gave the midline"), (f"{g(H)} feet", "used the high tide")]
    elif ask == "midline":
        wr = [(f"d = {g(amp)}", "gave the amplitude"), (f"d = {g(H - Lw)}", "used the range"), (f"d = {g(H)}", "used the high tide")]
    else:
        wr = [(f"{g(P)} hours", "used the time from high to low"), (f"{g(4 * P)} hours", "doubled twice"), (f"{g(P / 2)} hours", "halved the time")]
    return I(prompt, ans, steps, wr, dict(k="ctx_tide", H=str(H), L=str(Lw), P=str(P), ask=ask, show=[hh, ll, f"{g(P)} hours"]), "ctx_tide")


def ctx_daylight(r, L):
    M = F(ri(r, 26, 32), 2)
    m = F(ri(r, 16, 22), 2)
    need(M - m >= 3)
    city = r.choice(["Boston", "Seattle", "Chicago", "Denver", "Minneapolis", "Portland"])
    ask = r.choice(["amplitude", "average"]) if L < 2 else r.choice(["amplitude", "average", "value"])
    amp, mid = (M - m) / 2, (M + m) / 2
    prompt = (f"In {city} the longest day has {g(M)} hours of daylight and the shortest has {g(m)} hours. "
              f"Daylight is modeled by D(t) = A cos(2π(t - 172)/365) + C, with t the day of the year.")
    if ask == "amplitude":
        prompt += " Find A."
        ans = g(amp)
        wr = [(g(M - m), "used the full range"), (g(mid), "gave the midline"), (g(M), "used the maximum")]
    elif ask == "average":
        prompt += " Find C."
        ans = g(mid)
        wr = [(g(amp), "gave the amplitude"), (g(M - m), "used the range"), ("12", "assumed 12 hours")]
    else:
        prompt += " How many hours of daylight does the model give on day 263 (about 91 days after day 172)? Round to the nearest tenth."
        v = float(mid) + float(amp) * math.cos(2 * math.pi * 91 / 365)
        ans = "≈ " + rd(v, 1) + " hours"
        wr = [("≈ " + rd(float(mid) - float(amp) * math.cos(2 * math.pi * 91 / 365), 1) + " hours", "subtracted the cosine term"), (f"≈ {float(M):.1f} hours", "used the maximum"),
              ("≈ " + rd(float(mid) + float(amp) * math.cos(91 * math.pi / 180), 1) + " hours" if abs(math.cos(91 * math.pi / 180) - math.cos(2 * math.pi * 91 / 365)) > 0.01 else f"≈ {float(m):.1f} hours", "used degrees for the angle")]
    steps = [f"A = ({g(M)} - {g(m)})/2 = {g(amp)} and C = ({g(M)} + {g(m)})/2 = {g(mid)}."] + (
        [f"D(263) = {g(mid)} + {g(amp)} cos(2π · 91/365) ≈ {ans[2:]}."] if ask == "value" else [f"{'A' if ask == 'amplitude' else 'C'} = {ans}."])
    return I(prompt, ans, steps, wr, dict(k="ctx_daylight", M=str(M), m=str(m), ask=ask, show=[f"{g(M)} hours", f"{g(m)} hours"]), "ctx_daylight")


# ================================================================== triangle trigonometry: Law of Sines and Cosines (G-SRT.D.11)
def ctx_boats(r, L):
    v1, v2 = ri(r, 8, 30), ri(r, 8, 30)
    t = ri(r, 2, 4)
    ang = r.choice([35, 40, 50, 55, 65, 70, 80, 100, 110, 115, 125, 130])
    a, b = v1 * t, v2 * t
    d = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(ang)))
    ans = rd(d, 1)
    prompt = (f"Two boats leave the same dock at the same time. One travels at {v1} mi/h and the other at {v2} mi/h; the angle between their courses is {ang}°. "
              f"How far apart are they after {t} hours? Round to the nearest tenth of a mile.")
    steps = [f"After {t} hours the boats are {a} mi and {b} mi from the dock.",
             f"d² = {a}² + {b}² - 2({a})({b}) cos {ang}°.", f"d ≈ {ans} mi."]
    wr = [(f"≈ {rd(math.sqrt(a * a + b * b + 2 * a * b * math.cos(math.radians(ang))), 1)} mi", "added the 2ab cos C term"),
          (f"≈ {rd(math.sqrt(a * a + b * b), 1)} mi", "used the Pythagorean Theorem"),
          (f"≈ {rd(math.sqrt(v1 * v1 + v2 * v2 - 2 * v1 * v2 * math.cos(math.radians(ang))), 1)} mi", "used the speeds instead of the distances"),
          (f"≈ {rd(d + 2, 1)} mi", "made a rounding slip")]
    return I(prompt, f"≈ {ans} mi", steps, wr, dict(k="ctx_boats", a=a, b=b, ang=ang, show=[f"{v1} mi/h", f"{v2} mi/h", f"{ang}°", f"{t} hours"]), "ctx_boats")


def ctx_tunnel(r, L):
    a, b = 10 * ri(r, 20, 90), 10 * ri(r, 20, 90)
    C = ri(r, 30, 140)
    d = math.sqrt(a * a + b * b - 2 * a * b * math.cos(math.radians(C)))
    ans = rd(d, 0)
    prompt = (f"A surveyor stands at a point {a} m from one end of a planned tunnel and {b} m from the other end. "
              f"The angle between the two lines of sight is {C}°. How long will the tunnel be? Round to the nearest meter.")
    steps = [f"Law of Cosines: c² = {a}² + {b}² - 2({a})({b}) cos {C}°.", f"c ≈ {ans} m."]
    wr = [(f"≈ {rd(math.sqrt(a * a + b * b + 2 * a * b * math.cos(math.radians(C))), 0)} m", "added the 2ab cos C term"),
          (f"≈ {rd(math.sqrt(a * a + b * b), 0)} m", "used the Pythagorean Theorem"), (f"≈ {rd(a + b - d / 10, 0)} m", "estimated without the law"),
          (f"≈ {rd(math.sqrt(abs(a * a + b * b - 2 * a * b * math.cos(C))), 0)} m", "used radian mode")]
    return I(prompt, f"≈ {ans} m", steps, wr, dict(k="ctx_tunnel", a=a, b=b, C=C, show=[f"{a} m", f"{b} m", f"{C}°"]), "ctx_tunnel")


def ctx_sines(r, L):
    D = 10 * ri(r, 20, 120)
    A, B = ri(r, 30, 75), ri(r, 30, 75)
    C = 180 - A - B
    need(C >= 25)
    x = D * math.sin(math.radians(B)) / math.sin(math.radians(C))
    ans = rd(x, 0)
    prompt = (f"Two ranger stations are {D} m apart. From station A, a fire is spotted at an angle of {A}° to the line between the stations; "
              f"from station B the angle is {B}°. How far is the fire from station A? Round to the nearest meter.")
    steps = [f"The angle at the fire is 180° - {A}° - {B}° = {C}°.", f"Law of Sines: x/sin {B}° = {D}/sin {C}°.", f"x = {D} sin {B}°/sin {C}° ≈ {ans} m."]
    wr = [(f"≈ {rd(D * math.sin(math.radians(A)) / math.sin(math.radians(C)), 0)} m", "used the angle at A (that gives the distance from B)"),
          (f"≈ {rd(D * math.sin(math.radians(C)) / math.sin(math.radians(B)), 0)} m", "inverted the ratio"),
          (f"≈ {rd(D * math.sin(math.radians(B)), 0)} m", "forgot to divide by sin C"), (f"≈ {rd(x + 15, 0)} m", "made an arithmetic slip")]
    return I(prompt, f"≈ {ans} m", steps, wr, dict(k="ctx_sines", D=D, A=A, B=B, show=[f"{D} m", f"{A}°", f"{B}°"]), "ctx_sines")


# ================================================================== conics: parabolas (G-GPE.A.2)
def ctx_dish(r, L):
    p = r.choice([F(n, 2) for n in range(2, 20)])
    d = r.choice([F(n, 2) for n in range(1, 9)])
    w2 = 16 * p * d  # (w/2)² = 4pd
    w = math.isqrt(int(w2)) if F(w2).denominator == 1 else None
    need(w is not None and w * w == w2)
    what = r.choice(["satellite dish", "radio telescope reflector", "solar cooker"])
    prompt = (f"A {what} has a parabolic cross-section {w} inches wide and {g(d)} inches deep. "
              f"The receiver is placed at the focus. How far from the vertex is the receiver?")
    steps = [f"Put the vertex at the origin: x² = 4py passes through ({num(F(w, 2))}, {g(d)}).", f"({num(F(w, 2))})² = 4p({g(d)}), so p = {num(F(w * w, 4))}/{g(4 * d)} = {g(p)}.",
             f"The receiver is {g(p)} inches from the vertex."]
    wr = [(f"{g(F(w * w, 4) / d)} inches", "forgot the 4 in x² = 4py"), (f"{g(F(w * w, 16) / d * 2)} inches", "used the full width instead of half"),
          (f"{g(d)} inches", "used the depth"), (f"{g(4 * p)} inches", "gave 4p")]
    return I(prompt, f"{g(p)} inch" if p == 1 else f"{g(p)} inches", steps, wr, dict(k="ctx_dish", w=w, d=str(d), show=[f"{w} inches", f"{g(d)} inches"]), "ctx_dish")


def ctx_cable(r, L):
    D = 10 * ri(r, 5, 30)
    h0, H = ri(r, 5, 20), ri(r, 40, 120)
    x = r.choice([D // 2, D // 4, 3 * D // 4, D // 5, 2 * D // 5]) if L > 0 else D // 2
    need(x > 0)
    y = h0 + F(H - h0) * F(x, D) ** 2
    need(y.denominator <= 4)
    prompt = (f"The main cable of a suspension bridge hangs in a parabola. Its lowest point is {h0} m above the road at the center, "
              f"and it is {H} m above the road at the towers, {D} m on each side of the center. How high is the cable {x} m from the center?")
    a = F(H - h0, D * D)
    steps = [f"y = ax² + {h0}; at x = {D}: {H} = a({D})² + {h0}, so a = {num(a)}.", f"At x = {x}: y = {num(a)}({x})² + {h0} = {g(y)} m."]
    wr = [(f"{g(h0 + F(H - h0) * F(x, D))} m", "assumed the cable is straight"), (f"{g(F(H - h0) * F(x, D) ** 2)} m", "forgot the height at the center"),
          (f"{g(H - F(H - h0) * F(x, D) ** 2)} m", "measured down from the towers"), (f"{g(y + 1)} m", "made an arithmetic slip")]
    return I(prompt, f"{g(y)} m", steps, wr, dict(k="ctx_cable", D=D, h0=h0, H=H, x=x, show=[f"{h0} m", f"{H} m", f"{D} m", f"{x} m"]), "ctx_cable")


def ctx_reflector(r, L):
    k = r.choice([4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 6, 10, 14, 18])
    obj = r.choice(["flashlight reflector", "car headlight mirror", "spotlight mirror"])
    prompt = f"A cross-section of a {obj} is the parabola y = x²/{k}, measured in centimeters. Where should the bulb go: how far from the vertex is the focus?"
    p = F(k, 4)
    steps = [f"Write x² = {k}y as x² = 4py: 4p = {k}.", f"p = {g(p)} cm: the bulb goes {g(p)} cm from the vertex."]
    wr = [(f"{k} cm", "gave 4p"), (f"{g(F(k, 2))} cm", "divided by 2 instead of 4"), (f"{g(F(1, k))} cm", "used the coefficient 1/k"), (f"{g(4 * k)} cm", "multiplied by 4")]
    return I(prompt, f"{g(p)} cm", steps, wr, dict(k="ctx_reflector", kk=k, show=[f"x²/{k}"]), "ctx_reflector")


# ================================================================== matrices: multiplication (N-VM.C.8)
def ctx_cost(r, L):
    items = r.sample(["notebooks", "pens", "folders", "calculators", "binders"], 3)
    q = [ri(r, 2, 15) for _ in range(3)]
    pa = [ri(r, 1, 12) for _ in range(3)]
    pb = [ri(r, 1, 12) for _ in range(3)]
    need(pa != pb)
    which = r.choice([0, 1])
    store = ["Store A", "Store B"][which]
    tot = sum(x * y for x, y in zip(q, [pa, pb][which]))
    prompt = (f"A class orders {q[0]} {items[0]}, {q[1]} {items[1]} and {q[2]} {items[2]}: Q = [{q[0]}, {q[1]}, {q[2]}]. "
              f"Unit prices in dollars (rows Store A, Store B; columns in the same order): P = [{pa[0]}, {pa[1]}, {pa[2]}; {pb[0]}, {pb[1]}, {pb[2]}]. "
              f"The product P·Qᵀ gives each store's total. What is the total at {store}?")
    p = [pa, pb][which]
    steps = [f"Row {which + 1} of P times Q: {p[0]}({q[0]}) + {p[1]}({q[1]}) + {p[2]}({q[2]}).", f"= ${tot}."]
    other = sum(x * y for x, y in zip(q, [pa, pb][1 - which]))
    wr = [(f"${other}", "used the other store's row"), (f"${sum(p) * sum(q)}", "multiplied the sums"),
          (f"${sum(q) + sum(p)}", "added instead of multiplying"), (f"${tot + p[0]}", "made an arithmetic slip")]
    return I(prompt, f"${tot}", steps, wr, dict(k="ctx_cost", q=q, p=p, show=[f"Q = [{q[0]}, {q[1]}, {q[2]}]", f"{pa[0]}, {pa[1]}, {pa[2]}; {pb[0]}, {pb[1]}, {pb[2]}"]), "ctx_cost")


def ctx_points(r, L):
    teams = r.sample(["Eagles", "Hawks", "Lions", "Tigers", "Wolves", "Bears"], 2)
    w = [[ri(r, 0, 12) for _ in range(3)] for _ in range(2)]
    pts = r.choice([[3, 1, 0], [2, 1, 0], [3, 2, 1], [4, 2, 0]])
    t = r.choice([0, 1])
    tot = sum(a * b for a, b in zip(w[t], pts))
    prompt = (f"A league awards {pts[0]} points per win, {pts[1]} per tie and {pts[2]} per loss: V = [{pts[0]}; {pts[1]}; {pts[2]}]. "
              f"Records (columns wins, ties, losses): R = [{', '.join(map(str, w[0]))}; {', '.join(map(str, w[1]))}] for the {teams[0]} and the {teams[1]}. "
              f"Use R·V to find the {teams[t]}' points.")
    steps = [f"Row {t + 1} of R times V: {w[t][0]}({pts[0]}) + {w[t][1]}({pts[1]}) + {w[t][2]}({pts[2]}).", f"= {tot} points."]
    o = sum(a * b for a, b in zip(w[1 - t], pts))
    wr = [(f"{o} points", "used the other team's row"), (f"{sum(w[t])} points", "counted games instead of points"),
          (f"{sum(w[t]) * sum(pts)} points", "multiplied the sums"), (f"{tot + pts[0]} points", "made an arithmetic slip")]
    return I(prompt, f"{tot} points", steps, wr, dict(k="ctx_points", w=w[t], v=pts, show=[f"V = [{pts[0]}; {pts[1]}; {pts[2]}]", ", ".join(map(str, w[t])), teams[t]]), "ctx_points")


# ================================================================== vectors: applications (N-VM.A.3)
def ctx_plane(r, L):
    a = 10 * ri(r, 12, 60)
    w = 5 * ri(r, 2, 16)
    gs = math.hypot(a, w)
    ask = r.choice(["speed", "angle"]) if L > 0 else "speed"
    dirs = r.choice([("north", "east"), ("north", "west"), ("east", "south"), ("south", "west")])
    prompt = f"A plane flies with an airspeed of {a} mi/h heading due {dirs[0]}. A {w} mi/h wind blows toward the {dirs[1]}. "
    if ask == "speed":
        prompt += "What is the plane's ground speed? Round to the nearest tenth."
        ans = f"≈ {rd(gs, 1)} mi/h"
        wr = [(f"{a + w} mi/h", "added the speeds"), (f"{a - w} mi/h", "subtracted the speeds"), (f"≈ {rd(math.sqrt(a * a - w * w), 1)} mi/h", "subtracted the squares")]
        steps = [f"The velocities are perpendicular: ground speed = √({a}² + {w}²).", f"{ans}."]
    else:
        ang = math.degrees(math.atan(w / a))
        prompt += f"By how many degrees does the wind push the plane off its heading toward the {dirs[1]}? Round to the nearest tenth."
        ans = f"≈ {rd(ang, 1)}°"
        wr = [(f"≈ {rd(90 - ang, 1)}°", "measured from the wind's direction"), (f"≈ {rd(math.degrees(math.asin(w / a)), 1)}°" if abs(math.degrees(math.asin(w / a)) - ang) > 0.1 else f"≈ {rd(ang + 1, 1)}°", "used sine instead of tangent"),
              (f"≈ {rd(math.degrees(math.atan(a / w)), 1)}°", "inverted the ratio")]
        steps = [f"tan θ = {w}/{a}.", f"θ = tan⁻¹({w}/{a}) {ans}."]
    return I(prompt, ans, steps, wr, dict(k="ctx_plane", a=a, w=w, ask=ask, show=[f"{a} mi/h", f"{w} mi/h"]), "ctx_plane")


def ctx_forces(r, L):
    f1, f2 = 5 * ri(r, 4, 40), 5 * ri(r, 4, 40)
    ang = r.choice([30, 45, 60, 75, 90, 105, 120, 135]) if L > 0 else 90
    R = math.sqrt(f1 * f1 + f2 * f2 + 2 * f1 * f2 * math.cos(math.radians(ang)))
    ans = f"≈ {rd(R, 1)} N"
    prompt = f"Two tugboats pull a barge with forces of {f1} N and {f2} N. The angle between the ropes is {ang}°. What is the magnitude of the resultant force? Round to the nearest tenth."
    steps = [f"|R|² = {f1}² + {f2}² + 2({f1})({f2}) cos {ang}°.", f"|R| {ans}."]
    wr = [(f"{f1 + f2} N" if ang != 0 else f"≈ {rd(R + 3, 1)} N", "added the magnitudes"),
          (f"≈ {rd(math.sqrt(f1 * f1 + f2 * f2 - 2 * f1 * f2 * math.cos(math.radians(ang))), 1)} N" if ang != 90 else f"≈ {rd(R - 5, 1)} N", "used the angle of the triangle instead of the angle between the forces"),
          (f"≈ {rd(math.sqrt(f1 * f1 + f2 * f2), 1)} N" if ang != 90 else f"{abs(f1 - f2)} N", "ignored the angle" if ang != 90 else "subtracted the forces")]
    return I(prompt, ans, steps, wr, dict(k="ctx_forces", f1=f1, f2=f2, ang=ang, show=[f"{f1} N", f"{f2} N", f"{ang}°"]), "ctx_forces")


# ================================================================== probability: expected value (S-MD.B.5, S-MD.B.7)
def ctx_insurance(r, L):
    cost = 1000 * ri(r, 2, 30)
    p = r.choice([F(1, 50), F(1, 100), F(1, 200), F(1, 40), F(3, 100), F(1, 25)])
    prem = 10 * ri(r, 5, 60)
    ev = prem - p * cost
    need(ev.denominator == 1 and ev != 0)
    item = r.choice(["phone", "bicycle", "laptop", "car repair"])
    prompt = (f"An insurance company sells a one-year {item} policy for ${prem}. It pays ${cost:,} if a claim is made, which happens with probability {num(p)}. "
              f"What is the company's expected profit per policy?")
    ans = usd(ev)
    steps = [f"E = {prem} - ({num(p)})({cost}) = {prem} - {num(p * cost)}.", f"E = {ans} per policy."]
    wr = [(usd(prem), "ignored the payouts"), (usd(-p * cost), "ignored the premium"),
          (usd(prem + p * cost), "added the expected payout"), (usd(-ev), "took the customer's point of view")]
    return I(prompt, ans, steps, wr, dict(k="ctx_insurance", prem=prem, cost=cost, p=str(p), show=[f"${prem}", f"${cost:,}", num(p)]), "ctx_insurance")


def ctx_raffle(r, L):
    n = r.choice([200, 250, 400, 500, 1000])
    price = r.choice([1, 2, 5, 10])
    prizes = [(r.choice([100, 200, 250, 500]), 1), (r.choice([20, 25, 50]), r.choice([2, 4, 5]))]
    ev = F(sum(v * c for v, c in prizes), n) - price
    need(ev.denominator in (1, 2, 4, 5, 10, 20, 25, 50, 100))
    prompt = (f"A raffle sells {n} tickets at ${price} each. There is one ${prizes[0][0]} prize and {prizes[1][1]} prizes of ${prizes[1][0]}. "
              f"What is the expected value of buying one ticket?")
    gain = F(sum(v * c for v, c in prizes), n)
    ans = usd(ev)
    steps = [f"Expected winnings: ({prizes[0][0]} + {prizes[1][1]} · {prizes[1][0]})/{n} = {usd(gain)}.", f"Subtract the ticket price: {usd(gain)} - ${price} = {ans}.",
             f"The expected value is {ans} per ticket."]
    wr = [(usd(gain), "forgot the cost of the ticket"), (usd(F(prizes[0][0], n) - price), "counted only the top prize"),
          (usd(-price), "assumed the ticket never wins"), ("$0", "assumed the raffle is fair")]
    return I(prompt, ans, steps, wr, dict(k="ctx_raffle", n=n, price=price, prizes=prizes, show=[f"{n} tickets", f"${price}", f"${prizes[0][0]}", f"${prizes[1][0]}"]), "ctx_raffle")


# ================================================================== sequences and series: finite series (A-SSE.B.4)
def ctx_seats(r, L):
    a1, d, n = ri(r, 12, 30), ri(r, 2, 4), ri(r, 10, 30)
    ask = r.choice(["row", "total"]) if L > 0 else "total"
    an = a1 + (n - 1) * d
    S = n * (a1 + an) // 2
    prompt = f"A theater has {a1} seats in the first row, and each row has {d} more seats than the row in front of it. There are {n} rows. "
    if ask == "row":
        prompt += "How many seats are in the last row?"
        ans = f"{an} seats"
        steps = [f"a_n = a₁ + (n - 1)d = {a1} + ({n} - 1)({d}).", f"= {an} seats."]
        wr = [(f"{a1 + n * d} seats", "used n instead of n - 1"), (f"{S} seats", "found the total"), (f"{a1 * n} seats", "multiplied the first row by the number of rows")]
    else:
        prompt += "How many seats are there in all?"
        ans = f"{S} seats"
        steps = [f"Last row: {a1} + ({n} - 1)({d}) = {an}.", f"S = n(a₁ + a_n)/2 = {n}({a1} + {an})/2 = {S} seats."]
        wr = [(f"{an} seats", "gave the last row"), (f"{n * (a1 + a1 + n * d) // 2} seats", "used n instead of n - 1 for the last row"),
              (f"{a1 * n} seats", "ignored the extra seats per row"), (f"{n * (a1 + an)} seats", "forgot to divide by 2")]
    return I(prompt, ans, steps, wr, dict(k="ctx_seats", a1=a1, d=d, n=n, ask=ask, show=[f"{a1} seats", f"{d} more", f"{n} rows"]), "ctx_seats")


def ctx_salary(r, L):
    s = 1000 * ri(r, 32, 70)
    p = r.choice([2, 3, 4, 5])
    n = ri(r, 5, 20)
    S = s * ((1 + p / 100) ** n - 1) / (p / 100)
    ans = cash(S, 0)
    prompt = f"A job pays {money(s)} in the first year, with a {p}% raise each year after. What are the total earnings over {n} years? Round to the nearest dollar."
    steps = [f"The salaries form a geometric sequence with a₁ = {s} and r = 1.0{p}.", f"S = {s}(1.0{p}^{n} - 1)/(1.0{p} - 1).", f"S {ans}."]
    wr = [(cash(s * (1 + p / 100) ** (n - 1), 0), "gave the last year's salary"), (cash(s * n, 0), "ignored the raises"),
          (cash(s * ((1 + p / 100) ** (n + 1) - 1) / (p / 100), 0), "used n + 1 years"), (cash(s * n * (1 + p / 100 * (n - 1) / 2), 0), "treated the raises as arithmetic")]
    return I(prompt, ans, steps, wr, dict(k="ctx_salary", s=s, p=p, n=n, show=[money(s), f"{p}%", f"{n} years"]), "ctx_salary")


def ctx_bounce(r, L):
    h = r.choice([4, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25])
    rr = r.choice([F(1, 2), F(2, 3), F(3, 4), F(3, 5), F(4, 5), F(1, 3)])
    n = ri(r, 2, 4)
    ask = "total"
    if ask == "nth":
        v = h * rr ** n
        ans = f"{g(v)} ft" if (v * 100).denominator == 1 else f"≈ {rd(float(v), 2)} ft"
        prompt = f"A ball is dropped from {h} feet. Each bounce reaches {num(rr)} of the previous height. How high does it rise after bounce {n}? Round to the nearest hundredth of a foot if necessary."
        steps = [f"Heights form a geometric sequence: {h}({num(rr)})ⁿ.", f"{h}({num(rr)})^{n} = {ans.replace('≈ ', '')}."]
        wr = [(f"{g(h * rr ** (n - 1))} ft" if (h * rr ** (n - 1) * 100).denominator == 1 else f"≈ {rd(float(h * rr ** (n - 1)), 2)} ft", "counted one bounce too few"),
              (f"{g(h - n * h * (1 - rr) if h - n * h * (1 - rr) > 0 else h * rr)} ft", "subtracted the same amount each bounce"), (f"{g(h * rr)} ft", "used only one bounce")]
    else:
        tot = h + 2 * h * rr / (1 - rr)
        ans = f"{g(tot)} ft" if (tot * 100).denominator == 1 else f"≈ {rd(float(tot), 2)} ft"
        prompt = f"A ball is dropped from {h} feet. Each bounce reaches {num(rr)} of the previous height. If it bounces forever, what total vertical distance does it travel? Round to the nearest hundredth of a foot if necessary."
        steps = [f"Down {h} ft, then each rebound is travelled up and down: 2 · {h}({num(rr)})/(1 - {num(rr)}).", f"Total = {h} + {g(2 * h * rr / (1 - rr))} = {ans.replace('≈ ', '')}."]
        one = h / (1 - rr)
        wr = [((f"{g(one)} ft" if (one * 100).denominator == 1 else f"≈ {rd(float(one), 2)} ft"), "counted each rebound only once"),
              ((f"{g(2 * one)} ft" if (2 * one * 100).denominator == 1 else f"≈ {rd(float(2 * one), 2)} ft"), "doubled the first drop too"),
              ((f"{g(h * rr / (1 - rr))} ft" if (h * rr / (1 - rr) * 100).denominator == 1 else f"≈ {rd(float(h * rr / (1 - rr)), 2)} ft"), "left out the first drop")]
    return I(prompt, ans, steps, wr, dict(k="ctx_bounce", h=h, rr=str(rr), n=n, ask=ask, show=[f"{h} feet", num(rr)]), "ctx_bounce")


# unit#tag -> (skill index, families, standards, id prefix)
CONTEXT = {
    "equations-inequalities": (8, [ctx_tickets, ctx_invest, ctx_mixture], ["A-REI.C.6", "A-CED.A.3"], "pc-eqi"),
    "functions": (15, [ctx_halflife, ctx_compound, ctx_depreciate], ["F-LE.A.2", "F-IF.C.8b"], "pc-fun"),
    "trigonometric-functions": (8, [ctx_ferris, ctx_tide, ctx_daylight], ["F-TF.B.5", "F-IF.C.7e"], "pc-trg"),
    "general-triangle-trigonometry": (4, [ctx_boats, ctx_tunnel], ["G-SRT.D.11", "G-SRT.D.10"], "pc-gtt"),
    "general-triangle-trigonometry#sines": (2, [ctx_sines], ["G-SRT.D.11", "G-SRT.D.10"], "pc-gtt"),
    "conics": (2, [ctx_dish, ctx_cable, ctx_reflector], ["G-GPE.A.2"], "pc-con"),
    "matrices": (3, [ctx_cost, ctx_points], ["N-VM.C.8", "N-VM.C.6"], "pc-mat"),
    "vectors": (6, [ctx_plane, ctx_forces], ["N-VM.A.3"], "pc-vec"),
    "probability": (5, [ctx_insurance, ctx_raffle], ["S-MD.B.5", "S-MD.B.7"], "pc-prb"),
    "sequences-series-limits": (2, [ctx_seats, ctx_salary], ["A-SSE.B.4", "F-BF.A.2"], "pc-ssl"),
    "sequences-series-limits#infinite": (3, [ctx_bounce], ["A-SSE.B.4"], "pc-ssl"),
}
CONTEXTUAL = {f.__name__ for v in CONTEXT.values() for f in v[1]}
