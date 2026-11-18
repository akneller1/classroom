"""Question families for Precalculus audit item #6 (batch P4c): more question types in repetitive skills.

replace.py swaps the excess items of a skill's most common template for items from these families (same id,
level and format). Same contract as families.py; verify.py recomputes every answer from check data.
"""
import math
from fractions import Fraction as F

from families import I, Reject, need, ri, nz, num, sup, coef, join, poly, mc_only, lf, surd, cx, polar_rect, trig, special  # noqa: F401
from contexts import rd, NAMES  # noqa: F401
from core import g  # noqa: E402


def pt(x, y):
    return f"({num(x)}, {num(y)})"


def lin_eq(m, b):
    return "y = " + (join([coef(m, "x") if m else "", num(b) if b else ""]) if (m or b) else "0")


def mat(rows):
    return "[" + "; ".join(", ".join(num(v) for v in r) for r in rows) + "]"


# ================================================================== matrices-05: reduced row-echelon form
def rref_free(r, L):
    a, b, c, d = ri(r, -6, 6), ri(r, -9, 9), ri(r, -6, 6), ri(r, -9, 9)
    need(a != 0 and c != 0)
    t = nz(r, -5, 5)
    R = f"[1, 0, {a}, {b}; 0, 1, {c}, {d}; 0, 0, 0, 0]"
    x, y = b - a * t, d - c * t
    prompt = (f"The reduced row-echelon form of a system's augmented matrix (variables x, y, z) is {R}. "
              f"The system has infinitely many solutions. Find the solution with z = {t}.")
    ans = f"({x}, {y}, {t})"
    steps = [f"Row 1: x + {a}z = {b}, so x = {b} - ({a})({t}) = {x}.", f"Row 2: y + {c}z = {d}, so y = {d} - ({c})({t}) = {y}.", f"The solution is {ans}."]
    wr = [(f"({b}, {d}, {t})", "ignored the z terms"), (f"({b + a * t}, {d + c * t}, {t})", "added instead of subtracting the z terms"),
          (f"({y}, {x}, {t})", "swapped x and y"), ("no solution", "read the zero row as a contradiction")]
    return I(prompt, ans, steps, wr, dict(k="rref_free", a=a, b=b, c=c, d=d, t=t, show=[R, f"z = {t}"]), "rref_free")


@mc_only
def rref_count(r, L):
    kind = r.choice(["one", "none", "many"])
    a, b, c, d, e = (ri(r, -7, 7) for _ in range(5))
    if kind == "one":
        R = f"[1, 0, 0, {a}; 0, 1, 0, {b}; 0, 0, 1, {c}]"
        ans = f"exactly one solution, ({a}, {b}, {c})"
    elif kind == "none":
        k = nz(r, -6, 6)
        R = f"[1, 0, {a}, {b}; 0, 1, {c}, {d}; 0, 0, 0, {k}]"
        ans = "no solution"
    else:
        R = f"[1, 0, {a}, {b}; 0, 1, {c}, {d}; 0, 0, 0, 0]"
        ans = "infinitely many solutions"
    prompt = f"A calculator gives the reduced row-echelon form {R} for a system in x, y and z. How many solutions does the system have?"
    steps = [{"one": "Each variable has a leading 1, and there is no contradictory row.", "none": "The last row says 0 = a nonzero number, a contradiction.",
              "many": "The last row is all zeros, so z is free."}[kind], f"The system has {ans}."]
    pool = [f"exactly one solution, ({a}, {b}, {c})" if kind != "one" else f"exactly one solution, ({b}, {d}, {e})", "no solution", "infinitely many solutions",
            "exactly one solution, (0, 0, 0)"]
    wr = [(p, "misread the last row") for p in pool if p != ans]
    return I(prompt, ans, steps, wr, dict(k="rref_count", kind=kind, R=R, show=[R]), "rref_count")


def rref_aug(r, L):
    n = 2 if L == 0 else 3
    rows = [[nz(r, -6, 6) for _ in range(n)] + [ri(r, -12, 12)] for _ in range(n)]
    vs = ["x", "y", "z"][:n]
    eqs = [join([coef(row[j], vs[j]) for j in range(n)]) + f" = {row[n]}" for row in rows]
    sysx = "; ".join(eqs)
    prompt = f"Write the augmented matrix for the system {sysx}."
    ans = mat(rows)
    steps = ["Each equation is a row: the coefficients of " + ", ".join(vs) + ", then the constant.", f"{ans}."]
    wr = [(mat([row[:n] for row in rows]), "left out the constants"), (mat([[-v for v in row[:n]] + [row[n]] for row in rows]), "changed the signs of the coefficients"),
          (mat([row[:n] + [-row[n]] for row in rows]) if any(row[n] for row in rows) else mat([[row[n]] + row[:n] for row in rows]), "moved the constants to the left side"),
          (mat([[row[n]] + row[:n] for row in rows]), "put the constants first")]
    return I(prompt, ans, steps, wr, dict(k="rref_aug", rows=rows, show=[sysx]), "rref_aug")


# ================================================================== functions-07: transformations of points
def tr_reverse(r, L):
    a = r.choice([1, 2, 3, -1, -2]) if L > 0 else 1
    h, k = nz(r, -6, 6), nz(r, -6, 6)
    x0, y0 = ri(r, -6, 6), ri(r, -6, 6)
    X, Y = x0 + h, a * y0 + k
    inner = lf(-h)
    lead = "" if a == 1 else ("-" if a == -1 else str(a))
    gtxt = f"y = {lead}f({inner}) " + (f"+ {k}" if k > 0 else f"- {-k}")
    prompt = f"The point ({X}, {Y}) is on the graph of {gtxt}. What point must be on the graph of y = f(x)?"
    ans = pt(x0, y0)
    steps = [f"Undo the horizontal shift: x = {X} - ({h}) = {x0}.", f"Undo the vertical change: y = ({Y} - ({k}))/{a} = {y0}." if a != 1 else f"Undo the vertical shift: y = {Y} - ({k}) = {y0}.", f"The point is {ans}."]
    wr = [(pt(X + h, a * Y + k), "applied the transformation again instead of undoing it"), (pt(X - h, Y + k), "undid the shifts in the wrong directions"),
          (pt(x0, Y - k), "forgot to divide by the stretch factor") if a != 1 else (pt(X + h, Y - k), "undid the horizontal shift the wrong way"),
          (pt(y0, x0), "swapped the coordinates")]
    return I(prompt, ans, steps, wr, dict(k="tr_reverse", a=a, h=h, kk=k, P=[X, Y], show=[gtxt, f"({X}, {Y})"]), "tr_reverse")


def tr_reflect(r, L):
    x0, y0 = nz(r, -8, 8), nz(r, -8, 8)
    k = ri(r, -5, 5) if L > 0 else 0
    kind = r.choice(["-f(x)", "f(-x)", "-f(-x)"])
    gtxt = "y = " + kind + ("" if k == 0 else (f" + {k}" if k > 0 else f" - {-k}"))
    X = -x0 if "f(-x)" in kind else x0
    Y = (-y0 if kind.startswith("-") else y0) + k
    prompt = f"If ({x0}, {y0}) is a point on the graph of y = f(x), which point is on the graph of {gtxt}?"
    ans = pt(X, Y)
    steps = [{"-f(x)": "y = -f(x) reflects over the x-axis: (x, y) → (x, -y).", "f(-x)": "y = f(-x) reflects over the y-axis: (x, y) → (-x, y).",
              "-f(-x)": "y = -f(-x) reflects over both axes: (x, y) → (-x, -y)."}[kind] + (f" Then shift {'up' if k > 0 else 'down'} {abs(k)}." if k else ""), f"The point is {ans}."]
    wr = [(pt(x0 if X == -x0 else -x0, (y0 if Y - k == -y0 else -y0) + k), "reflected over the other axis"), (pt(x0, y0 + k), "did not reflect"),
          (pt(X, Y - 2 * k) if k else pt(-x0, -y0) if (X, Y) != (-x0, -y0) else pt(y0, x0), "shifted the wrong way" if k else "reflected over both axes"),
          (pt(y0, x0), "swapped the coordinates")]
    return I(prompt, ans, steps, wr, dict(k="tr_reflect", kind=kind, kk=k, P=[x0, y0], show=[gtxt, f"({x0}, {y0})"]), "tr_reflect")


def tr_stretch(r, L):
    b = F(r.choice([2, 3, 4])) if L == 0 else r.choice([F(2), F(3), F(4), F(1, 2), F(1, 3)])
    x0 = nz(r, -4, 4) * (b.numerator if L < 2 else 1)
    y0 = ri(r, -9, 9)
    k = ri(r, -5, 5) if L == 2 else 0
    X = F(x0) / F(b)
    bt = num(b) if not isinstance(b, F) or F(b).denominator == 1 else f"({num(b)})"
    gtxt = f"y = f({bt}x)" + ("" if k == 0 else (f" + {k}" if k > 0 else f" - {-k}"))
    prompt = f"The graph of {gtxt} is a horizontal {'compression' if b > 1 else 'stretch'} of y = f(x){' followed by a vertical shift' if k else ''}. Where does the point ({x0}, {y0}) of y = f(x) move?"
    ans = pt(X, y0 + k)
    steps = [f"y = f({bt}x) changes x-coordinates by the factor 1/{bt}: {x0} ÷ {num(b)} = {num(X)}." + (f" Then add {k} to y." if k else ""), f"The point is {ans}."]
    wr = [(pt(F(x0) * F(b), y0 + k), "multiplied the x-coordinate by the factor"), (pt(x0, F(y0) * F(b) + k), "stretched the y-coordinate"),
          (pt(X, y0), "forgot the vertical shift") if k else (pt(x0, y0), "did not change the point"), (pt(X, y0 * 2 + k), "made an arithmetic slip")]
    return I(prompt, ans, steps, wr, dict(k="tr_stretch", b=str(F(b)), kk=k, P=[x0, y0], show=[gtxt, f"({x0}, {y0})"]), "tr_stretch")


# ================================================================== conics-06: hyperbolas
def sq(t, h):
    return f"({t} - {h})²" if h > 0 else (f"({t} + {-h})²" if h < 0 else f"{t}²")


def hyp_asym(r, L):
    h, k = ri(r, -6, 6), ri(r, -6, 6)
    a, b = ri(r, 1, 7), ri(r, 1, 7)
    need(a != b)
    hor = r.choice([True, False])
    slope = F(b, a) if hor else F(a, b)
    v = pt(h + a, k) if hor else pt(h, k + a)
    prompt = f"A hyperbola has center ({h}, {k}), a vertex at {v}, and asymptotes with slopes ±{num(slope)}. Write its standard-form equation."
    ans = (f"{sq('x', h)}/{a * a} - {sq('y', k)}/{b * b} = 1" if hor else f"{sq('y', k)}/{a * a} - {sq('x', h)}/{b * b} = 1")
    steps = [f"The vertex is {a} unit{'s' if a > 1 else ''} from the center {'horizontally' if hor else 'vertically'}, so a = {a}.",
             f"Asymptote slope = {'b/a' if hor else 'a/b'} = {num(slope)}, so b = {b}.", f"{ans}."]
    wr = [((f"{sq('x', h)}/{b * b} - {sq('y', k)}/{a * a} = 1" if hor else f"{sq('y', k)}/{b * b} - {sq('x', h)}/{a * a} = 1"), "swapped a and b"),
          ((f"{sq('y', k)}/{a * a} - {sq('x', h)}/{b * b} = 1" if hor else f"{sq('x', h)}/{a * a} - {sq('y', k)}/{b * b} = 1"), "used the wrong transverse axis"),
          ((f"{sq('x', h)}/{a} - {sq('y', k)}/{b} = 1" if hor else f"{sq('y', k)}/{a} - {sq('x', h)}/{b} = 1") if a * b > 1 else (f"{sq('x', -h)}/{a * a} - {sq('y', -k)}/{b * b} = 1"), "forgot to square a and b" if a * b > 1 else "used the wrong signs for the center"),
          ((f"{sq('x', h)}/{a * a} + {sq('y', k)}/{b * b} = 1" if hor else f"{sq('y', k)}/{a * a} + {sq('x', h)}/{b * b} = 1"), "wrote an ellipse")]
    return I(prompt, ans, steps, wr, dict(k="hyp_asym", h=h, kk=k, a=a, b=b, hor=hor, show=[f"({h}, {k})", v, f"±{num(slope)}"]), "hyp_asym")


def hyp_foci(r, L):
    trip = r.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (8, 15, 17), (2, 3, None), (1, 2, None), (3, 1, None)])
    a, b, c = trip
    h, k = ri(r, -5, 5), ri(r, -5, 5)
    hor = r.choice([True, False])
    eq = f"{sq('x', h)}/{a * a} - {sq('y', k)}/{b * b} = 1" if hor else f"{sq('y', k)}/{a * a} - {sq('x', h)}/{b * b} = 1"
    if c is None:
        need(L > 0)
        cc = a * a + b * b
        ct = surd(1, cc)
        f1, f2 = ((f"({h} + {ct}, {k})", f"({h} - {ct}, {k})") if hor else (f"({h}, {k} + {ct})", f"({h}, {k} - {ct})"))
        ans = f"{f1} and {f2}"
        c_txt = ct
    else:
        f1, f2 = (pt(h + c, k), pt(h - c, k)) if hor else (pt(h, k + c), pt(h, k - c))
        ans = f"{f1} and {f2}"
        c_txt = str(c)
    prompt = f"Find the foci of the hyperbola {eq}."
    steps = [f"c² = a² + b² = {a * a} + {b * b} = {a * a + b * b}, so c = {c_txt}.", f"The foci are {c_txt} units from the center ({h}, {k}) along the {'horizontal' if hor else 'vertical'} axis: {ans}."]
    cw = math.isqrt(abs(a * a - b * b)) if math.isqrt(abs(a * a - b * b)) ** 2 == abs(a * a - b * b) and a != b else None
    wr = []
    if c is not None:
        wr.append(((f"{pt(h, k + c)} and {pt(h, k - c)}" if hor else f"{pt(h + c, k)} and {pt(h - c, k)}"), "used the wrong axis"))
        if cw:
            wr.append(((f"{pt(h + cw, k)} and {pt(h - cw, k)}" if hor else f"{pt(h, k + cw)} and {pt(h, k - cw)}"), "used c² = a² - b² as for an ellipse"))
        wr.append(((f"{pt(h + a, k)} and {pt(h - a, k)}" if hor else f"{pt(h, k + a)} and {pt(h, k - a)}"), "gave the vertices"))
        wr.append(((f"{pt(-h + c, -k)} and {pt(-h - c, -k)}" if hor else f"{pt(-h, -k + c)} and {pt(-h, -k - c)}") if (h or k) else (f"{pt(h + c * c, k)} and {pt(h - c * c, k)}" if hor else f"{pt(h, k + c * c)} and {pt(h, k - c * c)}"), "used the wrong center" if (h or k) else "forgot the square root"))
    else:
        wr.append(((f"({h}, {k} + {c_txt}) and ({h}, {k} - {c_txt})" if hor else f"({h} + {c_txt}, {k}) and ({h} - {c_txt}, {k})"), "used the wrong axis"))
        wr.append(((f"{pt(h + a, k)} and {pt(h - a, k)}" if hor else f"{pt(h, k + a)} and {pt(h, k - a)}"), "gave the vertices"))
        wr.append(((f"{pt(h + a * a + b * b, k)} and {pt(h - a * a - b * b, k)}" if hor else f"{pt(h, k + a * a + b * b)} and {pt(h, k - a * a - b * b)}"), "forgot the square root"))
    return I(prompt, ans, steps, wr, dict(k="hyp_foci", h=h, kk=k, a=a, b=b, hor=hor, show=[eq]), "hyp_foci")


# ================================================================== sequences-02: finite series
def ser_find_n(r, L):
    a1, d = ri(r, -9, 12), nz(r, -4, 6)
    n = ri(r, 5, 25)
    S = n * (2 * a1 + (n - 1) * d) // 2
    need(S > 0 and (2 * a1 + (n - 1) * d) * n % 2 == 0)
    a2, a3 = a1 + d, a1 + 2 * d
    prompt = f"How many terms of the arithmetic series {a1} + {a2} + {a3} + … must be added to get a sum of {S}?".replace("+ -", "- ")
    steps = [f"S_n = n/2 · [2({a1}) + (n - 1)({d})] = {S}.", f"Solve the quadratic in n; the positive whole-number solution is n = {n}."]
    wr = [(str(n + 1), "was off by one"), (str(S // a3 if a3 else n + 2), "divided the sum by a term"), (str(2 * n), "forgot to divide by 2"), (str(n - 1), "was off by one")]
    return I(prompt, str(n), steps, wr, dict(k="ser_find_n", a1=a1, d=d, S=S, show=[f"{S}"]), "ser_find_n")


def ser_first_last(r, L):
    a1, an, n = ri(r, -20, 30), ri(r, -20, 90), ri(r, 6, 40)
    S = F(n * (a1 + an), 2)
    need(S.denominator == 1)
    prompt = f"An arithmetic series has {n} terms. The first term is {a1} and the last term is {an}. Find the sum."
    steps = [f"S = n(a₁ + a_n)/2 = {n}({a1} + {an})/2.", f"= {S}."]
    wr = [(str(n * (a1 + an)), "forgot to divide by 2"), (num(F(a1 + an, 2)), "averaged the first and last terms only"),
          (num(F((n - 1) * (a1 + an), 2)), "used n - 1 terms"), (str(a1 + an), "added the first and last terms")]
    return I(prompt, num(S), steps, wr, dict(k="ser_first_last", a1=a1, an=an, n=n, show=[f"{n} terms", f"{a1}", f"{an}"]), "ser_first_last")


def ser_geo_formula(r, L):
    a1 = nz(r, -6, 8)
    q = r.choice([2, 3, -2, -3, F(1, 2)] if L > 0 else [2, 3])
    n = ri(r, 4, 9 if abs(F(q)) == 2 else 7)
    S = a1 * (1 - F(q) ** n) / (1 - F(q))
    need(abs(S) < 10 ** 6)
    prompt = f"A geometric series has a₁ = {a1} and common ratio r = {num(q)}. Find the sum of its first {n} terms."
    steps = [f"S_n = a₁(1 - rⁿ)/(1 - r) = {a1}(1 - ({num(q)})^{n})/(1 - ({num(q)})).", f"= {num(S)}."]
    wr = [(num(a1 * F(q) ** (n - 1)), "found the nth term instead of the sum"), (num(a1 * (1 - F(q) ** (n + 1)) / (1 - F(q))), "used n + 1 terms"),
          (num(a1 * (1 - F(q) ** n)), "forgot to divide by 1 - r"), (num(a1 * n), "multiplied the first term by n")]
    return I(prompt, num(S), steps, wr, dict(k="ser_geo_formula", a1=a1, q=str(F(q)), n=n, show=[f"a₁ = {a1}", f"r = {num(q)}", f"first {n} terms"]), "ser_geo_formula")


# ================================================================== probability-04: compound events
def pr_die_or(r, L):
    evs = [("an even number", {2, 4, 6}), ("an odd number", {1, 3, 5}), ("a number greater than 4", {5, 6}), ("a number less than 3", {1, 2}),
           ("a prime number", {2, 3, 5}), ("a multiple of 3", {3, 6}), ("a 6", {6}), ("a number greater than 2", {3, 4, 5, 6})]
    (n1, A), (n2, B) = r.sample(evs, 2)
    need(A != B)
    p = F(len(A | B), 6)
    prompt = f"A fair number cube is rolled once. Find P({n1} or {n2})."
    steps = [f"P(A) = {len(A)}/6, P(B) = {len(B)}/6, P(A and B) = {len(A & B)}/6.", f"P(A or B) = {len(A)}/6 + {len(B)}/6 - {len(A & B)}/6 = {num(p)}."]
    wr = [(num(F(len(A) + len(B), 6)) if len(A) + len(B) <= 6 else num(F(len(A) * len(B), 36)), "did not subtract the overlap" if len(A) + len(B) <= 6 else "multiplied the probabilities"),
          (num(F(len(A & B), 6)) if A & B else "0", "found P(A and B)"), (num(F(len(A) * len(B), 36)), "multiplied the probabilities"), (num(1 - p) if p != 1 else "5/6", "found the complement")]
    return I(prompt, num(p), steps, wr, dict(k="pr_die_or", A=sorted(A), B=sorted(B), show=[n1, n2]), "pr_die_or")


def pr_cards_or(r, L):
    evs = [("a heart", 13, "suit"), ("a red card", 26, "color"), ("a king", 4, "rank"), ("a face card", 12, "face"), ("an ace", 4, "ace"), ("a spade", 13, "suit2")]
    (n1, c1, t1), (n2, c2, t2) = r.sample(evs, 2)
    def overlap(x, y):
        s = {x, y}
        if s == {"suit", "color"}:
            return 13
        if s == {"suit", "rank"} or s == {"suit", "ace"} or s == {"suit2", "rank"} or s == {"suit2", "ace"}:
            return 1
        if s == {"suit", "face"} or s == {"suit2", "face"}:
            return 3
        if s == {"color", "rank"} or s == {"color", "ace"}:
            return 2
        if s == {"color", "face"}:
            return 6
        if s == {"rank", "face"}:
            return 4
        if s == {"suit2", "color"} or s == {"suit", "suit2"} or s == {"rank", "ace"} or s == {"face", "ace"}:
            return 0
        raise Reject()
    o = overlap(t1, t2)
    p = F(c1 + c2 - o, 52)
    prompt = f"One card is drawn from a standard 52-card deck. Find P({n1} or {n2})."
    steps = [f"There are {c1} cards that are {n1[2:] if n1.startswith('a ') else n1[3:]}, {c2} that are {n2[2:] if n2.startswith('a ') else n2[3:]}, and {o} that are both.",
             f"P = ({c1} + {c2} - {o})/52 = {num(p)}."]
    wr = [(num(F(c1 + c2, 52)) if o else num(F(c1 * c2, 52 * 52)), "did not subtract the overlap" if o else "multiplied the probabilities"), (num(F(o, 52)) if o else num(F(c1, 52)), "found P(A and B)" if o else "used only one event"),
          (num(F(c1 * c2, 2704)), "multiplied the probabilities"), (num(1 - p), "found the complement")]
    return I(prompt, num(p), steps, wr, dict(k="pr_cards_or", e1=t1, e2=t2, show=[n1, n2]), "pr_cards_or")


# ================================================================== general-triangle-trigonometry-05: area from three sides
HERON = [(3, 4, 5), (5, 5, 6), (5, 5, 8), (6, 8, 10), (5, 12, 13), (13, 14, 15), (9, 10, 17), (10, 13, 13), (7, 15, 20), (8, 15, 17), (13, 20, 21), (11, 13, 20),
         (10, 17, 21), (12, 17, 25), (15, 15, 24), (17, 25, 28), (20, 21, 29), (25, 25, 14), (4, 13, 15), (9, 12, 15)]


def heron_cost(r, L):
    a, b, c = r.choice(HERON)
    k = r.choice([2, 3, 4, 5, 10])
    a, b, c = a * k, b * k, c * k
    s = F(a + b + c, 2)
    A2 = s * (s - a) * (s - b) * (s - c)
    A = math.isqrt(int(A2))
    need(A * A == A2)
    price = r.choice([2, 3, 4, 5, 6, 8, 12])
    tot = A * price
    what = r.choice(["sod", "fertilizer", "paving stones", "mulch"])
    prompt = f"A triangular garden has sides of {a} ft, {b} ft and {c} ft. Covering it with {what} costs ${price} per square foot. What is the total cost?"
    steps = [f"s = ({a} + {b} + {c})/2 = {s}.", f"Area = √({s}({s} - {a})({s} - {b})({s} - {c})) = {A} ft².", f"Cost = {A} · {price} = ${tot:,}."]
    wr = [(f"${(a + b + c) * price:,}", "used the perimeter"), (f"${A:,}", "gave the area, not the cost"), (f"${int(s) * price:,}", "used the semiperimeter"),
          (f"${a * b // 2 * price:,}", "used ½ab as if the triangle were right")]
    return I(prompt, f"${tot:,}", steps, wr, dict(k="heron_cost", s=[a, b, c], price=price, show=[f"{a} ft", f"{b} ft", f"{c} ft", f"${price}"]), "heron_cost")


def heron_height(r, L):
    a, b, c = r.choice(HERON)
    k = r.choice([1, 2, 3])
    a, b, c = sorted([a * k, b * k, c * k])
    s = F(a + b + c, 2)
    A2 = s * (s - a) * (s - b) * (s - c)
    A = math.isqrt(int(A2))
    need(A * A == A2)
    h = F(2 * A, c)
    prompt = f"A triangle has sides {a}, {b} and {c}. Use Heron's formula to find its area, then find the height to the longest side. Give the height."
    steps = [f"s = {s}; area = √({s} · {s - a} · {s - b} · {s - c}) = {A}.", f"Area = ½ · {c} · h, so h = 2({A})/{c} = {num(h)}."]
    wr = [(num(F(A, c)), "forgot the ½ in the area formula"), (str(A), "gave the area"), (num(F(2 * A, a)), "used the shortest side as the base"),
          (num(F(2 * A, b)) if F(2 * A, b) != h else num(h + 1), "used the middle side as the base")]
    return I(prompt, num(h), steps, wr, dict(k="heron_height", s=[a, b, c], show=[f"{a}, {b} and {c}"]), "heron_height")


# ================================================================== general-triangle-trigonometry-03: the ambiguous case
def amb_height(r, L):
    A = ri(r, 20, 70)
    b = ri(r, 6, 25)
    h = b * math.sin(math.radians(A))
    a = ri(r, max(2, int(h) - 3), b + 3)
    need(abs(a - h) > 0.3)
    n = 0 if a < h else (2 if a < b else 1)
    prompt = f"For triangle data A = {A}°, a = {a}, b = {b}, find the height h = b sin A (to the nearest tenth) and say how many triangles are possible."
    hh = rd(h, 1)
    word = {0: "no triangle", 1: "one triangle", 2: "two triangles"}[n]
    ans = f"h ≈ {hh}; {word}"
    steps = [f"h = {b} sin {A}° ≈ {hh}.", {0: f"a = {a} < h, so the side cannot reach: no triangle.", 1: f"a = {a} ≥ b = {b}, so one triangle.",
                                            2: f"h < a = {a} < b = {b}, so two triangles."}[n]]
    others = [w for w in ("no triangle", "one triangle", "two triangles") if w != word]
    wr = [(f"h ≈ {hh}; {others[0]}", "compared the wrong lengths"), (f"h ≈ {hh}; {others[1]}", "compared the wrong lengths"),
          (f"h ≈ {rd(b * math.cos(math.radians(A)), 1)}; {word}", "used cosine for the height"), (f"h ≈ {rd(a * math.sin(math.radians(A)), 1)}; {word}", "used side a for the height")]
    return I(prompt, ans, steps, wr, dict(k="amb_height", A=A, a=a, b=b, show=[f"A = {A}°", f"a = {a}", f"b = {b}"]), "amb_height")


def amb_second(r, L):
    A = ri(r, 20, 60)
    b = ri(r, 8, 25)
    h = b * math.sin(math.radians(A))
    a = ri(r, int(h) + 1, b - 1)
    need(h < a < b)
    B1 = math.degrees(math.asin(b * math.sin(math.radians(A)) / a))
    B2 = 180 - B1
    need(A + B2 < 179)
    safe = rd(B2, 1)
    prompt = f"Triangle ABC has A = {A}°, a = {a} and b = {b}, so two triangles are possible. Find the obtuse value of B to the nearest tenth of a degree."
    steps = [f"sin B = {b} sin {A}°/{a}, so the acute angle is B ≈ {rd(B1, 1)}°.", f"The obtuse angle is 180° - {rd(B1, 1)}° ≈ {safe}°."]
    wr = [(f"≈ {rd(B1, 1)}°", "gave the acute angle"), (f"≈ {rd(180 - A - B1, 1)}°", "found angle C instead"), (f"≈ {rd(90 + B1, 1)}°", "added 90° instead of subtracting from 180°")]
    return I(prompt, f"≈ {safe}°", steps, wr, dict(k="amb_second", A=A, a=a, b=b, show=[f"A = {A}°", f"a = {a}", f"b = {b}"]), "amb_second")


# ================================================================== equations-inequalities-10/11: feasible regions and linear programming
def lp_region(r, L):
    """x ≥ 0, y ≥ 0, a1x + b1y ≤ c1, a2x + b2y ≤ c2 with an integer crossing point."""
    X, Y = ri(r, 1, 6), ri(r, 1, 6)
    a1, b1 = ri(r, 1, 4), ri(r, 2, 6)
    a2, b2 = ri(r, 2, 6), ri(r, 1, 4)
    need(a1 * b2 != a2 * b1 and F(a1, b1) < F(a2, b2))
    c1, c2 = a1 * X + b1 * Y, a2 * X + b2 * Y
    return X, Y, (a1, b1, c1), (a2, b2, c2)


def lp_txt(l1, l2):
    return f"x ≥ 0, y ≥ 0, {coef(l1[0], 'x')} + {coef(l1[1], 'y')} ≤ {l1[2]}, {coef(l2[0], 'x')} + {coef(l2[1], 'y')} ≤ {l2[2]}"


def corners(l1, l2, X, Y):
    yint = min(F(l1[2], l1[1]), F(l2[2], l2[1]))
    xint = min(F(l1[2], l1[0]), F(l2[2], l2[0]))
    return [(F(0), F(0)), (F(0), yint), (F(X), F(Y)), (xint, F(0))]


def lp_axis_corner(r, L):
    X, Y, l1, l2 = lp_region(r, L)
    cs = corners(l1, l2, X, Y)
    which = r.choice(["y", "x"])
    P = cs[1] if which == "y" else cs[3]
    need(P[0].denominator == 1 and P[1].denominator == 1)
    reg = lp_txt(l1, l2)
    prompt = f"The feasible region {reg} has a corner on the {which}-axis other than the origin. Find it."
    ans = pt(*P)
    steps = [f"On the {which}-axis, {'x' if which == 'y' else 'y'} = 0. Each slanted line meets it at " +
             (f"y = {num(F(l1[2], l1[1]))} and y = {num(F(l2[2], l2[1]))}" if which == "y" else f"x = {num(F(l1[2], l1[0]))} and x = {num(F(l2[2], l2[0]))}") + ".",
             f"Both constraints must hold, so take the smaller value: {ans}."]
    big = (F(0), max(F(l1[2], l1[1]), F(l2[2], l2[1]))) if which == "y" else (max(F(l1[2], l1[0]), F(l2[2], l2[0])), F(0))
    wr = [(pt(*big), "took the larger intercept"), (pt(X, Y), "gave the corner where the slanted lines meet"), (pt(P[1], P[0]), "swapped the coordinates"),
          (pt(0, l1[2]) if which == "y" else pt(l1[2], 0), "used the constant without dividing")]
    return I(prompt, ans, steps, wr, dict(k="lp_axis_corner", l1=list(l1), l2=list(l2), which=which, show=[reg]), "lp_axis_corner")


def lp_max(r, L):
    X, Y, l1, l2 = lp_region(r, L)
    cs = corners(l1, l2, X, Y)
    need(all(c[0].denominator == 1 and c[1].denominator == 1 for c in cs))
    p, q = ri(r, 1, 9), ri(r, 1, 9)
    vals = [p * c[0] + q * c[1] for c in cs]
    best = max(vals)
    who = cs[vals.index(best)]
    reg = lp_txt(l1, l2)
    listed = ", ".join(pt(*c) for c in cs)
    prompt = f"The feasible region {reg} has corners {listed}. Find the maximum value of P = {p}x + {q}y on the region."
    steps = ["Evaluate P at each corner: " + "; ".join(f"P{pt(*c)} = {num(v)}" for c, v in zip(cs, vals)) + ".", f"The maximum is {num(best)}, at {pt(*who)}."]
    srt = sorted(set(vals))
    wr = [(num(srt[-2]) if len(srt) > 1 else num(best + 1), "picked the wrong corner"), (pt(*who), "gave the corner instead of the value"),
          (num(p * X + q * Y) if p * X + q * Y != best else num(best + p), "assumed the slanted-line corner is always best"), (num(srt[0]), "found the minimum")]
    return I(prompt, num(best), steps, wr, dict(k="lp_max", corners=[[int(c[0]), int(c[1])] for c in cs], p=p, q=q, show=[listed, f"P = {p}x + {q}y"]), "lp_max")


@mc_only
def lp_in_region(r, L):
    X, Y, l1, l2 = lp_region(r, L)
    reg = lp_txt(l1, l2)
    def inside(x, y):
        return x >= 0 and y >= 0 and l1[0] * x + l1[1] * y <= l1[2] and l2[0] * x + l2[1] * y <= l2[2]
    pts = [(x, y) for x in range(-1, 9) for y in range(-1, 9)]
    good = [p for p in pts if inside(*p) and p != (0, 0)]
    bad = [p for p in pts if not inside(*p)]
    need(good and len(bad) >= 3)
    P = r.choice(good)
    outs = r.sample([p for p in bad if abs(p[0] - X) + abs(p[1] - Y) <= 5] or bad, 3) if len([p for p in bad if abs(p[0] - X) + abs(p[1] - Y) <= 5]) >= 3 else r.sample(bad, 3)
    prompt = f"Which point lies in the feasible region {reg}?"
    steps = [f"Test {pt(*P)}: {l1[0]}({P[0]}) + {l1[1]}({P[1]}) = {l1[0] * P[0] + l1[1] * P[1]} ≤ {l1[2]} and {l2[0]}({P[0]}) + {l2[1]}({P[1]}) = {l2[0] * P[0] + l2[1] * P[1]} ≤ {l2[2]}, with x, y ≥ 0.",
             "Each other choice breaks at least one inequality."]
    wr = [(pt(*o), "did not check every inequality") for o in outs]
    return I(prompt, pt(*P), steps, wr, dict(k="lp_in_region", l1=list(l1), l2=list(l2), show=[reg]), "lp_in_region")


# ================================================================== probability-08: normal distributions
def norm_x(r, L):
    mu, sd = ri(r, 40, 90), ri(r, 3, 15)
    z = r.choice([F(1), F(2), F(-1), F(-2), F(3, 2), F(-3, 2), F(1, 2), F(5, 2), F(-1, 2)])
    x = mu + z * sd
    need(x.denominator <= 2)
    what = r.choice(["Test scores", "Heights of plants (cm)", "Commute times (min)", "Battery lives (h)"])
    prompt = f"{what} are normally distributed with mean {mu} and standard deviation {sd}. What value has a z-score of {num(z)}?"
    steps = [f"x = μ + zσ = {mu} + ({num(z)})({sd}).", f"x = {g(x)}."]
    wr = [(g(mu - z * sd), "subtracted zσ"), (g(mu + z), "added z without multiplying by σ"), (g(F(mu, sd) + z), "divided the mean by σ"), (g(mu * z), "multiplied the mean by z")]
    return I(prompt, g(x), steps, wr, dict(k="norm_x", mu=mu, sd=sd, z=str(z), show=[f"mean {mu}", f"deviation {sd}", num(z)]), "norm_x")


def norm_count(r, L):
    mu, sd = ri(r, 40, 90), ri(r, 3, 12)
    N = r.choice([200, 400, 500, 1000, 600, 800, 2000])
    k = r.choice([1, 2, 3]) if L > 0 else r.choice([1, 2])
    lo, hi = mu - k * sd, mu + k * sd
    pct = {1: F(68, 100), 2: F(95, 100), 3: F(997, 1000)}[k]
    cnt = pct * N
    need(cnt.denominator == 1)
    prompt = f"The weights of {N} packages are normally distributed with mean {mu} oz and standard deviation {sd} oz. About how many packages weigh between {lo} oz and {hi} oz?"
    steps = [f"{lo} and {hi} are {k} standard deviation{'s' if k > 1 else ''} from the mean, so about {g(pct * 100)}% of the data lie between them.", f"{g(pct * 100)}% of {N} = {cnt}."]
    other = {1: F(95, 100), 2: F(68, 100), 3: F(95, 100)}[k]
    wr = [(str(int(other * N)) if (other * N).denominator == 1 else str(N // 2), "used the wrong percent from the empirical rule"), (str(N // 2), "assumed half the packages"),
          (str(int(pct * N / 2)) if (pct * N / 2).denominator == 1 else str(N), "took only one side of the mean"), (str(N - int(cnt)), "found how many are outside the interval")]
    return I(prompt, str(cnt), steps, wr, dict(k="norm_count", mu=mu, sd=sd, N=N, kk=k, show=[f"{N}", f"mean {mu}", f"deviation {sd}", f"{lo} oz", f"{hi} oz"]), "norm_count")


# ================================================================== general-triangle-trigonometry-08: rotations
def rot_entry(r, L):
    th = r.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330])
    pos = r.choice([(1, 1), (1, 2), (2, 1), (2, 2)])
    (c, kc), (s, ks) = trig(th)
    val = {(1, 1): (c, kc), (1, 2): (-s, ks), (2, 1): (s, ks), (2, 2): (c, kc)}[pos]
    ans = surd(*val)
    prompt = f"R(θ) = [cos θ, -sin θ; sin θ, cos θ] rotates points θ counterclockwise. Find the exact entry in row {pos[0]}, column {pos[1]} of R({th}°)."
    steps = [f"Row {pos[0]}, column {pos[1]} is {['cos θ', '-sin θ', 'sin θ', 'cos θ'][(pos[0] - 1) * 2 + pos[1] - 1]}.", f"At θ = {th}°: {ans}."]
    alt = {(1, 1): (s, ks), (1, 2): (s, ks), (2, 1): (-s, ks), (2, 2): (s, ks)}[pos]
    wr = [(surd(*alt), "used the wrong entry formula"), (surd(-val[0], val[1]) if val[0] != 0 else "1", "used the wrong sign"),
          (surd(*(c, kc)) if (c, kc) != val else surd(*(s, ks)), "mixed up sine and cosine"), (surd(*trig(th + 90)[0]) if surd(*trig(th + 90)[0]) != ans else "2", "used the wrong angle")]
    return I(prompt, ans, steps, wr, dict(k="rot_entry", th=th, pos=list(pos), show=[f"R({th}°)", f"row {pos[0]}, column {pos[1]}"]), "rot_entry")


@mc_only
def rot_find_angle(r, L):
    x, y = nz(r, -7, 7), nz(r, -7, 7)
    th = r.choice([90, 180, 270])
    X, Y = {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[th]
    need((X, Y) != (x, y))
    prompt = f"A rotation about the origin takes ({x}, {y}) to ({X}, {Y}). Which counterclockwise angle does it use?"
    steps = [{90: "(x, y) → (-y, x) is a 90° rotation.", 180: "(x, y) → (-x, -y) is a 180° rotation.", 270: "(x, y) → (y, -x) is a 270° rotation."}[th], f"The angle is {th}°."]
    wr = [(f"{t}°", "used the wrong rotation rule") for t in (90, 180, 270, 45) if t != th]
    return I(prompt, f"{th}°", steps, wr, dict(k="rot_find_angle", P=[x, y], Q=[X, Y], show=[f"({x}, {y})", f"({X}, {Y})"]), "rot_find_angle")


# ================================================================== general-triangle-trigonometry-06: deriving the laws
def derive_coords(r, L):
    b, A = ri(r, 5, 30), ri(r, 20, 160)
    x, y = b * math.cos(math.radians(A)), b * math.sin(math.radians(A))
    xs, ys = rd(x, 1), rd(y, 1)
    prompt = (f"Place triangle ABC with A at the origin and side AB on the positive x-axis. If b = AC = {b} and A = {A}°, "
              f"then C = (b cos A, b sin A). Find the coordinates of C to the nearest tenth.")
    ans = f"({xs}, {ys})"
    steps = [f"x = {b} cos {A}° ≈ {xs}.", f"y = {b} sin {A}° ≈ {ys}.", f"C ≈ {ans}."]
    wr = [(f"({ys}, {xs})", "swapped sine and cosine"), (f"({rd(b * math.cos(A), 1)}, {rd(b * math.sin(A), 1)})", "used radian mode"),
          (f"({rd(-x, 1)}, {ys})" if abs(x) > 0.05 else f"({ys}, {ys})", "used the wrong sign for cosine"), (f"({rd(x / b, 1)}, {rd(y / b, 1)})", "left out b")]
    return I(prompt, ans, steps, wr, dict(k="derive_coords", b=b, A=A, show=[f"b = AC = {b}", f"A = {A}°"]), "derive_coords")


def derive_area(r, L):
    b, c, A = ri(r, 5, 30), ri(r, 5, 30), ri(r, 20, 160)
    h = b * math.sin(math.radians(A))
    area = 0.5 * c * h
    ans = rd(area, 1)
    prompt = (f"In triangle ABC, c = AB = {c}, b = AC = {b} and A = {A}°. The altitude from C to line AB is h = b sin A. "
              f"Use it to find the area of the triangle to the nearest tenth.")
    steps = [f"h = {b} sin {A}° ≈ {rd(h, 2)}.", f"Area = ½ · {c} · h ≈ {ans}."]
    wr = [(rd(c * h, 1), "forgot the ½"), (rd(abs(0.5 * c * b * math.cos(math.radians(A))), 1) if abs(math.cos(math.radians(A))) > 0.05 else rd(area + 3, 1), "used cosine for the height"),
          (rd(h, 1), "gave the height"), (rd(0.5 * b * c, 1), "used ½bc without the sine")]
    return I(prompt, ans, steps, wr, dict(k="derive_area", b=b, c=c, A=A, show=[f"c = AB = {c}", f"b = AC = {b}", f"A = {A}°"]), "derive_area")


# ================================================================== equations-inequalities-01: writing linear equations
def line_point_slope(r, L):
    m = r.choice([F(n) for n in range(-6, 7) if n] + ([F(1, 2), F(-2, 3), F(3, 4), F(-1, 3)] if L > 0 else []))
    x0, y0 = ri(r, -8, 8), ri(r, -9, 9)
    b = y0 - m * x0
    need(b.denominator == 1 or L > 0)
    prompt = f"Write an equation in slope-intercept form for the line with slope {num(m)} that passes through ({x0}, {y0})."
    ans = lin_eq(m, b)
    steps = [f"y - ({y0}) = {num(m)}(x - ({x0})).", f"y = {num(m)}x + ({num(-m * x0)}) + ({y0}), so {ans}."]
    wr = [(lin_eq(m, y0 + m * x0), "used x + x₀ instead of x - x₀"), (lin_eq(m, y0), "used the y-coordinate as the intercept"),
          (lin_eq(-1 / m, y0 + x0 / m), "used the perpendicular slope"), (lin_eq(x0, y0), "used the point as slope and intercept")]
    return I(prompt, ans, steps, wr, dict(k="line_point_slope", m=str(m), P=[x0, y0], show=[num(m), f"({x0}, {y0})"]), "line_point_slope")


def line_table(r, L):
    m, b = nz(r, -6, 6), ri(r, -9, 9)
    x0, dx = ri(r, -4, 2), r.choice([1, 2])
    xs = [x0 + dx * i for i in range(4)]
    ys = [m * x + b for x in xs]
    tab = "x: " + ", ".join(map(str, xs)) + "\ny: " + ", ".join(map(str, ys))
    prompt = f"The table shows points on a line.\n{tab}\nWrite the equation of the line in slope-intercept form."
    ans = lin_eq(m, b)
    steps = [f"Slope = ({ys[1]} - ({ys[0]}))/({xs[1]} - ({xs[0]})) = {m}.", f"b = y - mx = {ys[0]} - ({m})({xs[0]}) = {b}, so {ans}."]
    wr = [(lin_eq(m * dx, b) if dx > 1 else lin_eq(m, ys[0]), "used the change in y without dividing by the change in x" if dx > 1 else "used the first y-value as the intercept"),
          (lin_eq(F(1, m), b), "inverted the slope"), (lin_eq(-m, b), "used the wrong sign for the slope"), (lin_eq(m, ys[0]) if ys[0] != b else lin_eq(m, b + m), "used the first y-value as the intercept")]
    return I(prompt, ans, steps, wr, dict(k="line_table", xs=xs, ys=ys, show=[", ".join(map(str, ys))]), "line_table")


def line_intercepts(r, L):
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    m = F(-b, a)
    prompt = f"A line has x-intercept {a} and y-intercept {b}. Write its equation in slope-intercept form."
    ans = lin_eq(m, b)
    steps = [f"It passes through ({a}, 0) and (0, {b}): slope = ({b} - 0)/(0 - ({a})) = {num(m)}.", f"{ans}."]
    wr = [(lin_eq(F(b, a), b), "lost the negative sign of the slope"), (lin_eq(F(-a, b), b), "inverted the slope"), (lin_eq(m, a), "used the x-intercept as b"),
          (lin_eq(F(a, b), a), "swapped the intercepts")]
    return I(prompt, ans, steps, wr, dict(k="line_intercepts", a=a, b=b, show=[f"x-intercept {a}", f"y-intercept {b}"]), "line_intercepts")


# ================================================================== probability-07: shapes of distributions
@mc_only
def stat_skew(r, L):
    mean, med = ri(r, 30, 90), ri(r, 30, 90)
    need(abs(mean - med) >= 4)
    what = r.choice(["household incomes", "home prices", "test scores", "commute times", "ages at a concert"])
    prompt = f"A distribution of {what} has mean {mean} and median {med}. What is the most likely shape?"
    ans = "skewed right" if mean > med else "skewed left"
    steps = [f"The mean is pulled toward the tail: mean {'>' if mean > med else '<'} median.", f"So the distribution is most likely {ans}."]
    wr = [("skewed left" if ans == "skewed right" else "skewed right", "reversed the rule"), ("symmetric", "ignored the gap between mean and median"), ("uniform", "confused shape with spread")]
    return I(prompt, ans, steps, wr, dict(k="stat_skew", mean=mean, med=med, show=[f"mean {mean}", f"median {med}"]), "stat_skew")


def stat_remove(r, L):
    n = ri(r, 5, 8)
    data = sorted(ri(r, 10, 40) for _ in range(n - 1))
    out = ri(r, 80, 150)
    data.append(out)
    mean_all = F(sum(data), n)
    mean_wo = F(sum(data) - out, n - 1)
    need((mean_all - mean_wo).denominator == 1 or (mean_all - mean_wo) * 10 % 1 == 0 or True)
    diff = mean_all - mean_wo
    dtxt = ", ".join(map(str, data))
    prompt = f"Data: {dtxt}. By how much does the mean decrease when the outlier {out} is removed? Round to the nearest tenth."
    ans = rd(float(diff), 1)
    steps = [f"Mean with {out}: {sum(data)}/{n} ≈ {rd(float(mean_all), 2)}.", f"Mean without it: {sum(data) - out}/{n - 1} ≈ {rd(float(mean_wo), 2)}.", f"Decrease ≈ {ans}."]
    wr = [(rd(float(mean_all), 1), "gave the original mean"), (rd(float(F(out, n)), 1), "divided the outlier by n"), (rd(float(mean_wo), 1), "gave the new mean"), (rd(float(diff) * 2, 1), "made an arithmetic slip")]
    return I(prompt, f"≈ {ans}", [s for s in steps], [("≈ " + w, why) for w, why in wr], dict(k="stat_remove", data=data, out=out, show=[dtxt]), "stat_remove")


# ================================================================== sequences-01: sequences
def seq_two_terms(r, L):
    a1, d = ri(r, -15, 15), nz(r, -7, 7)
    i, j = sorted(r.sample(range(2, 12), 2))
    t = ri(r, 12, 40)
    ai, aj = a1 + (i - 1) * d, a1 + (j - 1) * d
    at = a1 + (t - 1) * d
    prompt = f"An arithmetic sequence has a_{i} = {ai} and a_{j} = {aj}. Find a_{t}."
    steps = [f"d = ({aj} - ({ai}))/({j} - {i}) = {d}.", f"a₁ = {ai} - ({i} - 1)({d}) = {a1}.", f"a_{t} = {a1} + ({t} - 1)({d}) = {at}."]
    wr = [(str(a1 + t * d), "used t instead of t - 1"), (str(ai + (t - 1) * d), "started from a_i as if it were the first term"),
          (str(a1 + (t - 1) * (aj - ai)), "forgot to divide by the number of steps"), (str(at - d), "was off by one term")]
    return I(prompt, str(at), steps, wr, dict(k="seq_two_terms", a1=a1, d=d, t=t, i=i, j=j, show=[f"a_{i} = {ai}", f"a_{j} = {aj}", f"a_{t}"]), "seq_two_terms")


def seq_recursive(r, L):
    a1 = ri(r, -5, 8)
    m = r.choice([1, 2, 3, -1, -2]) if L > 0 else 1
    c = nz(r, -6, 6)
    n = ri(r, 4, 6)
    seq = [a1]
    for _ in range(n - 1):
        seq.append(m * seq[-1] + c)
    need(abs(seq[-1]) < 2000)
    rule = (f"a_n = {'' if m == 1 else ('-' if m == -1 else str(m))}a_(n - 1) " + (f"+ {c}" if c > 0 else f"- {-c}"))
    prompt = f"A sequence is defined by a₁ = {a1} and {rule} for n ≥ 2. Find a_{n}."
    steps = ["Apply the rule repeatedly: " + ", ".join(f"a_{i + 1} = {v}" for i, v in enumerate(seq)) + ".", f"a_{n} = {seq[-1]}."]
    wr = [(str(seq[-2]), "stopped one term early"), (str(m * seq[-1] + c), "went one term too far"), (str(a1 + (n - 1) * c), "ignored the multiplier") if m != 1 else (str(a1 + n * c), "used n instead of n - 1"),
          (str(seq[-1] + 1), "made an arithmetic slip")]
    return I(prompt, str(seq[-1]), steps, wr, dict(k="seq_recursive", a1=a1, m=m, c=c, n=n, show=[f"a₁ = {a1}", rule]), "seq_recursive")


# ================================================================== vectors-07: matrix transformations of vectors
def vt_compose(r, L):
    A = [[ri(r, -3, 3) for _ in range(2)] for _ in range(2)]
    B = [[ri(r, -3, 3) for _ in range(2)] for _ in range(2)]
    v = [ri(r, -5, 5), ri(r, -5, 5)]
    need(any(v) and A != B)
    Av = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
    BAv = [B[0][0] * Av[0] + B[0][1] * Av[1], B[1][0] * Av[0] + B[1][1] * Av[1]]
    Bv = [B[0][0] * v[0] + B[0][1] * v[1], B[1][0] * v[0] + B[1][1] * v[1]]
    ABv = [A[0][0] * Bv[0] + A[0][1] * Bv[1], A[1][0] * Bv[0] + A[1][1] * Bv[1]]
    need(ABv != BAv)
    vt = f"⟨{v[0]}, {v[1]}⟩"
    prompt = f"A = {mat(A)} and B = {mat(B)}. The vector v = {vt} is transformed by A and then by B. Find the result."
    ans = f"⟨{BAv[0]}, {BAv[1]}⟩"
    steps = [f"First Av = ⟨{Av[0]}, {Av[1]}⟩.", f"Then B(Av) = {ans}."]
    wr = [(f"⟨{ABv[0]}, {ABv[1]}⟩", "applied B first"), (f"⟨{Av[0]}, {Av[1]}⟩", "applied only A"), (f"⟨{Bv[0]}, {Bv[1]}⟩", "applied only B"),
          (f"⟨{BAv[1]}, {BAv[0]}⟩", "swapped the components")]
    return I(prompt, ans, steps, wr, dict(k="vt_compose", A=A, B=B, v=v, show=[mat(A), mat(B), vt]), "vt_compose")


@mc_only
def vt_which_matrix(r, L):
    opts = {"reflects vectors over the x-axis": "[1, 0; 0, -1]", "reflects vectors over the y-axis": "[-1, 0; 0, 1]", "reflects vectors over the line y = x": "[0, 1; 1, 0]",
            "rotates vectors 90° counterclockwise": "[0, -1; 1, 0]", "rotates vectors 180°": "[-1, 0; 0, -1]", "doubles the length of every vector": "[2, 0; 0, 2]"}
    desc = r.choice(list(opts))
    ans = opts[desc]
    prompt = f"Which matrix {desc}?"
    steps = ["Find where ⟨1, 0⟩ and ⟨0, 1⟩ go; those images are the columns of the matrix.", f"The matrix is {ans}."]
    wr = [(m_, "chose the matrix for a different transformation") for d_, m_ in opts.items() if m_ != ans]
    r.shuffle(wr)
    return I(prompt, ans, steps, wr[:4], dict(k="vt_which_matrix", desc=desc, show=[desc]), "vt_which_matrix")


# ================================================================== sequences-03: infinite geometric series
def inf_decimal(r, L):
    k = r.choice([1, 2]) if L > 0 else 1
    if k == 1:
        dgt = ri(r, 1, 8)
        val = F(dgt, 9)
        txt = f"0.{dgt}{dgt}{dgt}…"
        series = f"{dgt}/10 + {dgt}/100 + {dgt}/1000 + …"
        r_ = "1/10"
    else:
        dg = ri(r, 10, 98)
        need(dg % 11)
        val = F(dg, 99)
        txt = f"0.{dg}{dg}{dg}…"
        series = f"{dg}/100 + {dg}/10000 + …"
        r_ = "1/100"
    prompt = f"Write the repeating decimal {txt} as a fraction in lowest terms by treating it as the infinite geometric series {series}."
    a1 = F(int(txt[2:2 + k]), 10 ** k)
    steps = [f"a₁ = {num(a1)} and r = {r_}.", f"S = a₁/(1 - r) = ({num(a1)})/(1 - {r_}) = {num(val)}."]
    wr = [(num(a1), "gave only the first term"), (num(F(int(txt[2:2 + k]), 10 ** k - 10 ** (k - 1))) if k == 2 else num(F(int(txt[2]), 10)), "used the wrong denominator"),
          (num(a1 / (1 + F(1, 10 ** k))), "used 1 + r in the denominator"), (num(F(int(txt[2:2 + k]), 10 ** k + 1)), "used the wrong denominator")]
    return I(prompt, num(val), steps, wr, dict(k="inf_decimal", rep=txt[2:2 + k], show=[txt]), "inf_decimal")


def inf_find(r, L):
    q = r.choice([F(1, 2), F(1, 3), F(2, 3), F(1, 4), F(3, 4), F(-1, 2), F(-1, 3), F(1, 5), F(2, 5)])
    a1 = nz(r, -12, 18)
    S = a1 / (1 - q)
    ask = r.choice(["a1", "r"]) if L > 0 else "a1"
    if ask == "a1":
        prompt = f"An infinite geometric series has common ratio {num(q)} and sum {num(S)}. Find its first term."
        ans = str(a1)
        steps = [f"S = a₁/(1 - r), so a₁ = S(1 - r) = {num(S)}(1 - ({num(q)})).", f"a₁ = {a1}."]
        wr = [(num(S * q), "multiplied by r instead of 1 - r"), (num(S / (1 - q)), "divided by 1 - r"), (num(S * (1 + q)), "used 1 + r"), (num(S - q), "subtracted r from the sum")]
    else:
        prompt = f"An infinite geometric series has first term {a1} and sum {num(S)}. Find the common ratio."
        ans = num(q)
        steps = [f"S = a₁/(1 - r): {num(S)} = {a1}/(1 - r), so 1 - r = {num(F(a1) / S)}.", f"r = {num(q)}."]
        wr = [(num(1 - q), "gave 1 - r"), (num(F(a1) / S), "gave 1 - r"), (num(-q), "made a sign error"), (num(S / a1), "divided the sum by the first term")]
    return I(prompt, ans, steps, wr, dict(k="inf_find", a1=a1, q=str(q), ask=ask, show=[num(S)]), "inf_find")


# ================================================================== matrices-07: inverses
def inv_singular_k(r, L):
    a, b, d = nz(r, -6, 6), nz(r, -6, 6), nz(r, -6, 6)
    k = F(a * d, b)
    need(k.denominator == 1 and k != 0)
    pos = r.choice(["c", "a"])
    if pos == "c":
        M = f"[{a}, {b}; k, {d}]"
        ans = k
        steps = [f"det = {a}({d}) - {b}k = {a * d} - {b}k.", f"Not invertible when det = 0: k = {num(k)}."]
    else:
        M = f"[k, {b}; {num(k)}, {d}]"
        ans = F(b * k, d)
        need(ans.denominator == 1)
        steps = [f"det = {d}k - {b}({num(k)}).", f"det = 0 when k = {num(ans)}."]
    prompt = f"For what value of k does A = {M} have no inverse?"
    wr = [(num(-ans), "made a sign error"), (num(F(1, ans)) if ans else "1", "inverted the value"), ("0", "set k = 0"), (num(ans + 1), "made an arithmetic slip")]
    return I(prompt, num(ans), steps, wr, dict(k="inv_singular_k", M=M, show=[M]), "inv_singular_k")


def inv_solve_entry(r, L):
    """Use A⁻¹ to solve Ax = b; ask for one coordinate."""
    while True:
        A = [[ri(r, -5, 5) for _ in range(2)] for _ in range(2)]
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        if det in (1, -1, 2, -2) and all(A[0] + A[1]):
            break
    x, y = ri(r, -6, 6), ri(r, -6, 6)
    bv = [A[0][0] * x + A[0][1] * y, A[1][0] * x + A[1][1] * y]
    need(any(bv))
    which = r.choice(["x", "y"])
    prompt = f"A = {mat(A)}. Find A⁻¹ and use it to solve A[x; y] = [{bv[0]}; {bv[1]}]. What is {which}?"
    inv = [[F(A[1][1], det), F(-A[0][1], det)], [F(-A[1][0], det), F(A[0][0], det)]]
    ans = x if which == "x" else y
    steps = [f"det A = {det}; A⁻¹ = {mat(inv)}.", f"[x; y] = A⁻¹[{bv[0]}; {bv[1]}] = [{x}; {y}].", f"{which} = {ans}."]
    wr = [(str(y if which == "x" else x), "gave the other variable"), (str(-ans) if ans else "1", "made a sign error in the inverse"),
          (str(ans * det) if det not in (1,) else str(ans + 2), "forgot to divide by the determinant"), (str(bv[0] if which == "x" else bv[1]), "read the constant as the answer")]
    return I(prompt, str(ans), steps, wr, dict(k="inv_solve_entry", A=A, b=bv, which=which, show=[mat(A), f"[{bv[0]}; {bv[1]}]"]), "inv_solve_entry")


# ================================================================== functions-10: variation
def var_combined(r, L):
    k = r.choice([F(n) for n in range(1, 13)] + [F(1, 2), F(3, 2)])
    x1, z1 = ri(r, 1, 10), ri(r, 1, 10)
    y1 = k * x1 / z1
    x2, z2 = ri(r, 1, 12), ri(r, 1, 12)
    y2 = k * x2 / z2
    need(y1.denominator <= 4 and y2.denominator <= 4 and (x1, z1) != (x2, z2))
    prompt = f"y varies directly with x and inversely with z. y = {num(y1)} when x = {x1} and z = {z1}. Find y when x = {x2} and z = {z2}."
    steps = [f"y = kx/z: {num(y1)} = k({x1})/{z1}, so k = {num(k)}.", f"y = {num(k)}({x2})/{z2} = {num(y2)}."]
    wr = [(num(k * x2 * z2), "made y vary directly with z too"), (num(k * z2 / x2), "swapped the direct and inverse parts"), (num(k), "gave the constant k"),
          (num(y1 * x2 / x1), "ignored the change in z")]
    return I(prompt, num(y2), steps, wr, dict(k="var_combined", x1=x1, z1=z1, y1=str(y1), x2=x2, z2=z2, show=[num(y1), f"x = {x2}", f"z = {z2}"]), "var_combined")


def var_k(r, L):
    kind = r.choice(["directly", "inversely", "jointly"]) if L > 0 else r.choice(["directly", "inversely"])
    x, z = ri(r, 2, 12), ri(r, 2, 9)
    k = r.choice([F(n) for n in range(2, 13)] + [F(1, 2), F(2, 3), F(5, 2)])
    y = k * x if kind == "directly" else (k / x if kind == "inversely" else k * x * z)
    need(y.denominator <= 3)
    if kind == "jointly":
        prompt = f"y varies jointly with x and z, and y = {num(y)} when x = {x} and z = {z}. Find the constant of variation k."
        steps = [f"y = kxz: {num(y)} = k({x})({z}).", f"k = {num(y)}/{x * z} = {num(k)}."]
        wr = [(num(y * x * z), "multiplied instead of dividing"), (num(y / x), "divided by x only"), (num(y / z), "divided by z only"), (num(F(x * z) / y), "inverted k")]
    else:
        prompt = f"y varies {kind} with x, and y = {num(y)} when x = {x}. Find the constant of variation k."
        steps = [f"y = {'kx' if kind == 'directly' else 'k/x'}: {num(y)} = {'k(' + str(x) + ')' if kind == 'directly' else 'k/' + str(x)}.", f"k = {num(k)}."]
        wr = [(num(y * x) if kind == "directly" else num(y / x), "used the other kind of variation"), (num(F(x) / y) if kind == "directly" else num(F(1) / (y * x)), "inverted k"),
              (num(y), "gave y"), (num(k + 1), "made an arithmetic slip")]
    return I(prompt, num(k), steps, wr, dict(k="var_k", kind=kind, x=x, z=z, y=str(y), show=[num(y), f"x = {x}"]), "var_k")


# ================================================================== general-triangle-trigonometry-01: area with the sine
def area_parallelogram(r, L):
    a, b, t = ri(r, 4, 30), ri(r, 4, 30), ri(r, 25, 155)
    A = a * b * math.sin(math.radians(t))
    ans = rd(A, 1)
    prompt = f"A parallelogram has sides {a} cm and {b} cm with an angle of {t}° between them. Find its area to the nearest tenth."
    steps = [f"The diagonal splits it into two congruent triangles, each with area ½ · {a} · {b} · sin {t}°.", f"Area = {a} · {b} · sin {t}° ≈ {ans} cm²."]
    wr = [(f"≈ {rd(A / 2, 1)} cm²", "found the area of one triangle"), (f"{a * b} cm²", "multiplied the sides without the sine"),
          (f"≈ {rd(abs(a * b * math.cos(math.radians(t))), 1)} cm²", "used cosine"), (f"≈ {rd(abs(a * b * math.sin(t)), 1)} cm²", "used radian mode")]
    return I(prompt, f"≈ {ans} cm²", steps, wr, dict(k="area_parallelogram", a=a, b=b, t=t, show=[f"{a} cm", f"{b} cm", f"{t}°"]), "area_parallelogram")


def area_isosceles(r, L):
    s, t = ri(r, 4, 25), r.choice([30, 45, 60, 120, 135, 150] if L < 2 else list(range(20, 161, 5)))
    need(t != 90)
    A = 0.5 * s * s * math.sin(math.radians(t))
    ans = rd(A, 1)
    prompt = f"An isosceles triangle has two sides of {s} m that meet at a {t}° angle. Find its area to the nearest tenth."
    steps = [f"Area = ½ · {s} · {s} · sin {t}°.", f"≈ {ans} m²."]
    wr = [(f"≈ {rd(2 * A, 1)} m²", "forgot the ½"), (f"≈ {rd(abs(0.5 * s * s * math.cos(math.radians(t))), 1)} m²" if abs(math.cos(math.radians(t))) > 0.01 else f"≈ {rd(A + 4, 1)} m²", "used cosine"),
          (f"{num(F(s * s, 2))} m²", "left out the sine"), (f"≈ {rd(0.5 * s * math.sin(math.radians(t)), 1)} m²", "used only one side")]
    return I(prompt, f"≈ {ans} m²", steps, wr, dict(k="area_isosceles", s=s, t=t, show=[f"{s} m", f"{t}°"]), "area_isosceles")


# ================================================================== matrices-09: transformations with matrices
def mt_point(r, L):
    kind = r.choice(["90", "180", "270", "x", "y"])
    M = {"90": [[0, -1], [1, 0]], "180": [[-1, 0], [0, -1]], "270": [[0, 1], [-1, 0]], "x": [[1, 0], [0, -1]], "y": [[-1, 0], [0, 1]]}[kind]
    name = {"90": "a rotation of 90° counterclockwise", "180": "a rotation of 180°", "270": "a rotation of 270° counterclockwise", "x": "a reflection over the x-axis", "y": "a reflection over the y-axis"}[kind]
    x, y = nz(r, -9, 9), nz(r, -9, 9)
    need(abs(x) != abs(y))
    X, Y = M[0][0] * x + M[0][1] * y, M[1][0] * x + M[1][1] * y
    prompt = f"The matrix {mat(M)} represents {name}. Multiply to find the image of ({x}, {y})."
    steps = [f"{mat(M)}[{x}; {y}] = [{M[0][0]}({x}) + {M[0][1]}({y}); {M[1][0]}({x}) + {M[1][1]}({y})].", f"The image is ({X}, {Y})."]
    wr = [(pt(Y, X), "swapped the coordinates"), (pt(-X, -Y), "used the opposite transformation"), (pt(x, y), "did not change the point"), (pt(M[0][0] * x + M[1][0] * y, M[0][1] * x + M[1][1] * y), "multiplied by columns instead of rows")]
    return I(prompt, pt(X, Y), steps, wr, dict(k="mt_point", M=M, P=[x, y], show=[mat(M), f"({x}, {y})"]), "mt_point")


def mt_dilate(r, L):
    k = r.choice([2, 3, F(1, 2), -1, 4])
    V = [[ri(r, -6, 6) for _ in range(3)] for _ in range(2)]
    need(all(any(c) for c in zip(*V)))
    W = [[F(k) * v for v in row] for row in V]
    kt = num(k)
    prompt = f"The vertices of a triangle are the columns of {mat(V)}. Find the vertex matrix of its image under the dilation [{kt}, 0; 0, {kt}]."
    ans = mat(W)
    steps = [f"Multiplying by {kt}I multiplies every coordinate by {kt}.", f"{ans}."]
    wr = [(mat([[v + F(k) for v in row] for row in V]), "added the scale factor"), (mat([[F(k) * v for v in V[0]], V[1]]), "scaled only the x-coordinates"),
          (mat([[v / F(k) for v in row] for row in V]), "divided by the scale factor"), (mat([V[1], V[0]]), "swapped the rows")]
    return I(prompt, ans, steps, wr, dict(k="mt_dilate", kk=str(F(k)), V=V, show=[mat(V), f"[{kt}, 0; 0, {kt}]"]), "mt_dilate")


# skill -> families used to replace the excess of its most common template
VARIETY = {
    "matrices-skill-05": [rref_free, rref_count, rref_aug],
    "functions-skill-07": [tr_reverse, tr_reflect, tr_stretch],
    "conics-skill-06": [hyp_asym, hyp_foci],
    "sequences-series-limits-skill-02": [ser_find_n, ser_first_last, ser_geo_formula],
    "probability-skill-04": [pr_die_or, pr_cards_or],
    "general-triangle-trigonometry-skill-05": [heron_cost, heron_height],
    "general-triangle-trigonometry-skill-03": [amb_height, amb_second],
    "equations-inequalities-skill-10": [lp_axis_corner, lp_in_region],
    "equations-inequalities-skill-11": [lp_max, lp_axis_corner],
    "probability-skill-08": [norm_x, norm_count],
    "general-triangle-trigonometry-skill-08": [rot_entry, rot_find_angle],
    "general-triangle-trigonometry-skill-06": [derive_coords, derive_area],
    "equations-inequalities-skill-01": [line_point_slope, line_table, line_intercepts],
    "probability-skill-07": [stat_skew, stat_remove],
    "sequences-series-limits-skill-01": [seq_two_terms, seq_recursive],
    "vectors-skill-07": [vt_compose, vt_which_matrix],
    "sequences-series-limits-skill-03": [inf_decimal, inf_find],
    "matrices-skill-07": [inv_singular_k, inv_solve_entry],
    "functions-skill-10": [var_combined, var_k],
    "general-triangle-trigonometry-skill-01": [area_parallelogram, area_isosceles],
    "matrices-skill-09": [mt_point, mt_dilate],
}
