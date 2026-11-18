"""Independent verifier for the Precalculus audit gap skills (batch P4).

For every item recorded in out/checks.json it:
  1. confirms the parameters it uses are printed in the prompt (check["show"]),
  2. recomputes the answer from those parameters with its own formulas (complex arithmetic, math.comb, …) and
     compares it with the keyed answer read back from the display text by ../mathx.py,
  3. requires every multiple-choice distractor and every find-the-mistake student answer to be wrong,
  4. requires every open-response part to be right,
  5. checks structure: exactly one correct option, four distinct options, the student answer printed in the prompt.
It never imports families.py.

Usage: python3 tools/precalculus-audit-20261118/gaps/verify.py   → prints TOTAL ERRORS n
"""
import cmath, json, math, os, re, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
import mathx  # noqa: E402

D = math.pi / 180


def ev(t, **env):
    t = t.replace("√", "√").strip()
    return complex(mathx.ev(t, env or None))


def same(a, b, tol=1e-7):
    return abs(complex(a) - complex(b)) <= tol * max(1, abs(complex(b)))


def cis(r, deg):
    return r * cmath.exp(1j * deg * D)


def roots_list(text):
    """'x = 2 or x = -3' / 'θ = π/3 or θ = 5π/3' → sorted values."""
    parts = [p.strip() for p in re.split(r"\s+or\s+", text)]
    vals = []
    for p in parts:
        m = re.match(r"^[xθ]\s*=\s*(.+)$", p)
        if not m:
            return None
        vals.append(ev(m.group(1)).real)
    return sorted(vals)


def fn_check(text, f, xs):
    """Display-text expression in x equals f at every sample point."""
    try:
        return all(same(ev(text, x=x), f(x), 1e-6) for x in xs)
    except Exception:
        return False


# ------------------------------------------------------------------ expected answers, from the check data only
def expect(c):
    """Return a predicate on the answer text."""
    k = c["k"]
    if k == "ra_simplify":
        a, p, q, s = c["a"], c["p"], c["q"], c["s"]
        f = lambda x: (a * x * x + a * (p + q) * x + a * p * q) / (x * x + (p + s) * x + p * s)
        xs = [x for x in (0.37, 1.91, -2.43, 5.17) if abs(x + p) > 1e-3 and abs(x + s) > 1e-3]
        return lambda t: fn_check(t, f, xs)
    if k == "ra_add":
        a, b, p, q = c["a"], c["b"], c["p"], c["q"]
        f = lambda x: a / (x + p) + b / (x + q)
        return lambda t: fn_check(t, f, [0.37, 1.91, -2.43, 7.17])
    if k == "pf_coef":
        A, B = c["top"]
        p, q = c["p"], c["q"]
        # residue at x = p of (Ax + B)/((x - p)(x - q))
        val = (A * p + B) / (p - q) if c["ask"] == "A" else (A * q + B) / (q - p)
        return lambda t: same(ev(t), val)
    if k == "ra_excluded":
        roots = sorted([c["p"], c["q"]])
        return lambda t: roots_list(t) is not None and len(roots_list(t)) == 2 and all(abs(u - v) < 1e-9 for u, v in zip(roots_list(t), roots))
    if k == "ra_value":
        p, q, x0 = c["p"], c["q"], c["x0"]
        val = ((x0 * x0 - p * p) / (x0 + q)) / ((x0 - p) / (x0 + q))
        return lambda t: same(ev(t), val)
    if k == "inv_table":
        ans = c["xs"][c["ys"].index(c["v"])]
        return lambda t: same(ev(t), ans)
    if k == "inv_restrict_value":
        a, h, kk, cc = c["a"], c["h"], c["kk"], c["c"]
        root = math.sqrt((cc - kk) / a)
        ans = h + root if c["side"] == ">=" else h - root
        return lambda t: same(ev(t), ans)
    if k == "inv_rational":
        a, b, cc = c["a"], c["b"], c["c"]
        v = float(Fraction(c["v"]))
        ans = (cc * v + b) / (v - a)  # solve (ax + b)/(x - c) = v
        return lambda t: same(ev(t), ans)
    if k == "inv_compose":
        m, b = c["m"], c["b"]
        # f(g(x)) = x for all x  ⇔  k = m (both the linear and the cube-root case)
        def ok(t):
            kv = ev(t).real
            g = (lambda x: ((x - b) / kv) ** (1 / 3) if (x - b) / kv >= 0 else -((-(x - b) / kv) ** (1 / 3))) if c["cube"] else (lambda x: (x - b) / kv)
            f = (lambda x: m * x ** 3 + b) if c["cube"] else (lambda x: m * x + b)
            return all(abs(f(g(x)) - x) < 1e-6 for x in (-3.3, 0.7, 4.1, 11.9))
        return ok
    if k == "inv_which_restrict":
        return lambda t: t.strip() == f"x ≥ {c['h']}"
    if k == "cj_product":
        z = complex(c["a"], c["b"])
        return lambda t: same(ev(t), z * z.conjugate())
    if k == "cj_quotient":
        z = complex(*c["t"]) / complex(*c["d"])
        return lambda t: same(ev(t), z)
    if k == "cj_modq":
        z1, z2 = complex(*c["z1"]), complex(*c["z2"])
        val = abs(z1 / z2) if c["op"] == "÷" else abs(z1 * z2)
        return lambda t: same(ev(t), val)
    if k == "cj_recip":
        return lambda t: same(ev(t), 1 / complex(c["a"], c["b"]))
    if k == "cj_solve":
        z = complex(c["a"], c["b"])
        return lambda t: same(ev(t), z + z.conjugate() if c["which"] == "sum" else z - z.conjugate())
    if k == "pol_mult":
        return lambda t: same(ev(t), cis(c["r"][0], c["t"][0]) * cis(c["r"][1], c["t"][1]))
    if k == "pol_div":
        return lambda t: same(ev(t), cis(c["r"][0], c["t"][0]) / cis(c["r"][1], c["t"][1]))
    if k == "dm_power":
        return lambda t: same(ev(t), cis(c["r"], c["t"]) ** c["n"])
    if k == "dm_rect_power":
        z = complex(c["a"], c["b"])
        if c["sq3"]:
            # the base is 1 ± √3 i, -1 + √3 i, √3 ± i: the part shown with 3 in the data is √3
            z = complex(math.copysign(math.sqrt(3), c["a"]) if abs(c["a"]) == 3 else c["a"], math.copysign(math.sqrt(3), c["b"]) if abs(c["b"]) == 3 else c["b"])
        return lambda t: same(ev(t), z ** c["n"], 1e-6)
    if k == "dm_modulus":
        return lambda t: same(ev(t), abs(complex(c["a"], c["b"])) ** c["n"], 1e-9)
    if k == "dm_root":
        n = c["n"]
        roots = [cis(c["R"] ** (1 / n), (c["T"] + 360 * j) / n) for j in range(n)]
        best = min(roots, key=lambda z: (cmath.phase(z) % (2 * math.pi)) if abs(cmath.phase(z) % (2 * math.pi)) > 1e-9 else 99)
        return lambda t: same(ev(t), best, 1e-9) and same(ev(t) ** n, cis(c["R"], c["T"]), 1e-6)
    if k == "lim_classify":
        ratio = c["a"] / abs(c["b"])
        name = ("a limaçon with an inner loop" if ratio < 1 else "a cardioid" if ratio == 1 else "a dimpled limaçon" if ratio < 2 else "a convex limaçon")
        return lambda t: t == name
    if k == "lim_max":
        a, b = c["a"], c["b"]
        m = max(abs(a + b * math.cos(th / 1000)) for th in range(0, 6284))
        return lambda t: same(ev(t), m, 1e-5)
    if k == "lim_value":
        f = math.cos if c["fn"] == "cos" else math.sin
        return lambda t: same(ev(t), c["a"] + c["b"] * f(c["deg"] * D), 1e-9)
    if k in ("lim_pole", "lim_pole2"):
        f = math.cos if c["fn"] == "cos" else math.sin
        sols = sorted(j * math.pi / 12 for j in range(24) if abs(c["a"] + c["b"] * f(j * math.pi / 12)) < 1e-9)
        return lambda t: roots_list(t) is not None and len(roots_list(t)) == len(sols) and all(abs(u - v) < 1e-9 for u, v in zip(roots_list(t), sols))
    if k == "lim_symmetry":
        return lambda t: t == ("the polar axis (the x-axis)" if c["fn"] == "cos" else "the line θ = π/2 (the y-axis)")
    if k == "bn_coef":
        n, kk, a, b = c["n"], c["kk"], c["a"], c["b"]
        # coefficient of xᵏ in (ax + b)ⁿ by expanding the polynomial product directly
        coeffs = [1]
        for _ in range(n):
            nxt = [0] * (len(coeffs) + 1)
            for i, v in enumerate(coeffs):
                nxt[i] += v * b
                nxt[i + 1] += v * a
            coeffs = nxt
        return lambda t: same(ev(t), coeffs[kk])
    if k == "bn_term":
        n, tt, a, b = c["n"], c["t"], c["a"], c["b"]
        coeffs = [1]
        for _ in range(n):
            nxt = [0] * (len(coeffs) + 1)
            for i, v in enumerate(coeffs):
                nxt[i] += v * b
                nxt[i + 1] += v * a
            coeffs = nxt
        p = n - (tt - 1)  # descending powers: term t has x^(n - t + 1)
        return lambda t: fn_check(t, lambda x: coeffs[p] * x ** p, [1.3, -0.7, 2.1])
    if k == "bn_pascal":
        row = [1]
        for _ in range(c["n"]):
            row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
        return lambda t: same(ev(t), row[c["kk"]])
    if k == "bn_sum":
        return lambda t: same(ev(t), (c["a"] + c["b"]) ** c["n"])
    if k == "bn_expand":
        a, b, n = c["a"], c["b"], c["n"]
        return lambda t: fn_check(t, lambda x: (a * x + b) ** n, [1.3, -0.7, 2.1, 0.4, -1.9])
    if k == "cn_onesided":
        m1, b1, m2, b2 = c["p"]
        x = c["c"] + (-1e-9 if c["side"] == "-" else 1e-9)
        val = m1 * x + b1 if x < c["c"] else m2 * x + b2
        return lambda t: t != "does not exist" and same(ev(t), val, 1e-6)
    if k == "cn_param":
        cc, a, b = c["c"], c["a"], c["b"]
        return lambda t: abs(cc * cc + a - (ev(t).real * cc + b)) < 1e-9
    if k == "cn_removable":
        p, q = c["p"], c["q"]
        h = 1e-7
        val = (((p + h) ** 2 - (p + q) * (p + h) + p * q) / h)
        return lambda t: not t.startswith("no value") and same(ev(t), val, 1e-5)
    if k == "cn_infinite":
        a, cc, pw = c["a"], c["c"], c["pw"]
        x = cc + (1e-9 if c["side"] == "+" else -1e-9)
        v = a / (x - cc) ** pw
        return lambda t: t == ("∞" if v > 0 else "-∞")
    if k == "cn_exists":
        m1, b1, m2, b2 = c["p"]
        l1, l2 = m1 * c["c"] + b1, m2 * c["c"] + b2
        if l1 == l2:
            return lambda t: not t.startswith("The limit does not") and re.fullmatch(r"-?\d+", t) is not None and same(ev(t), l1)
        return lambda t: t == "The limit does not exist."
    return expect_context(c)


def numtext(t):
    """'≈ $4,886.68' / '38.75 m' / '-$7.60' / '12 hours' -> (value, decimals, rounded?)."""
    t = t.strip()
    approx = t.startswith("≈")
    t = t.lstrip("≈ ").replace("$", "").replace(",", "")
    m = re.match(r"^(-?\d+(?:\.(\d+))?)(?:\s*(?:°|%|[a-zA-Z][a-zA-Z/²³ ]*))?$", t)
    if not m:
        m2 = re.match(r"^d = (-?\d+(?:\.\d+)?)$", t)
        if not m2:
            raise ValueError(t)
        return float(m2.group(1)), None, approx
    return float(m.group(1)), len(m.group(2) or ""), approx


def approx_is(val, dp):
    def ok(t):
        v, d, ap = numtext(t)
        return ap and d == dp and abs(v - round(val, dp)) < 10 ** (-dp) / 2 + 1e-9 and abs(val - v) <= 0.5 * 10 ** (-dp) + 1e-9
    return ok


def exact_is(val, unit=None):
    def ok(t):
        v, _, ap = numtext(t)
        return (not ap) and abs(v - val) < 1e-9 and (unit is None or t.strip().endswith(unit))
    return ok


def maybe_rounded(val, dp, unit):
    """Exact when the value terminates within dp places, otherwise ≈ rounded."""
    if abs(round(val, dp) - val) < 1e-12:
        return exact_is(val, unit)
    return approx_is(val, dp)


def expect_context(c):
    k = c["k"]
    if k == "ctx_tickets":
        a, s_, n, R = c["a"], c["s"], c["n"], c["R"]
        return exact_is((R - s_ * n) / (a - s_))
    if k == "ctx_invest":
        x = (c["I"] - c["r2"] / 100 * c["P"]) / ((c["r1"] - c["r2"]) / 100)
        return exact_is(round(x, 6))
    if k == "ctx_mixture":
        n, t = c["n"], c["t"]
        return exact_is(n * (c["p2"] - t) / (c["p2"] - c["p1"]), "liters")
    if k == "ctx_halflife":
        return exact_is(c["A"] * 0.5 ** (c["t"] / c["h"]))
    if k == "ctx_compound":
        return approx_is(c["P"] * (1 + c["rate"] / 100 / c["n"]) ** (c["n"] * c["t"]), 2)
    if k == "ctx_depreciate":
        return approx_is(c["V"] * (1 - c["p"] / 100) ** c["t"], 0)
    if k == "ctx_ferris":
        return exact_is(round(c["c"] - c["rr"] * math.cos(2 * math.pi * c["t"] / c["T"]), 9), "feet")
    if k == "ctx_tide":
        H, Lw, P = (float(Fraction(c[x])) for x in ("H", "L", "P"))
        val = {"amplitude": (H - Lw) / 2, "midline": (H + Lw) / 2, "period": 2 * P}[c["ask"]]
        return exact_is(val)
    if k == "ctx_daylight":
        M, m = float(Fraction(c["M"])), float(Fraction(c["m"]))
        if c["ask"] == "value":
            return approx_is((M + m) / 2 + (M - m) / 2 * math.cos(2 * math.pi * (263 - 172) / 365), 1)
        return exact_is((M - m) / 2 if c["ask"] == "amplitude" else (M + m) / 2)
    if k in ("ctx_boats", "ctx_tunnel"):
        a, b = c["a"], c["b"]
        C = math.radians(c["ang"] if k == "ctx_boats" else c["C"])
        return approx_is(math.sqrt(a * a + b * b - 2 * a * b * math.cos(C)), 1 if k == "ctx_boats" else 0)
    if k == "ctx_sines":
        A, B = math.radians(c["A"]), math.radians(c["B"])
        return approx_is(c["D"] * math.sin(B) / math.sin(math.pi - A - B), 0)
    if k == "ctx_dish":
        w, d = c["w"], float(Fraction(c["d"]))
        return exact_is((w / 2) ** 2 / (4 * d), "inch") if (w / 2) ** 2 / (4 * d) == 1 else exact_is((w / 2) ** 2 / (4 * d), "inches")
    if k == "ctx_cable":
        D, h0, H, x = c["D"], c["h0"], c["H"], c["x"]
        return exact_is(h0 + (H - h0) * x * x / (D * D), "m")
    if k == "ctx_reflector":
        return exact_is(c["kk"] / 4, "cm")
    if k == "ctx_cost":
        return exact_is(sum(a * b for a, b in zip(c["q"], c["p"])))
    if k == "ctx_points":
        return exact_is(sum(a * b for a, b in zip(c["w"], c["v"])), "points")
    if k == "ctx_plane":
        a, w = c["a"], c["w"]
        return approx_is(math.hypot(a, w), 1) if c["ask"] == "speed" else approx_is(math.degrees(math.atan2(w, a)), 1)
    if k == "ctx_forces":
        f1, f2, t = c["f1"], c["f2"], math.radians(c["ang"])
        return approx_is(abs(complex(f1, 0) + f2 * complex(math.cos(t), math.sin(t))), 1)
    if k == "ctx_insurance":
        return exact_is(c["prem"] - float(Fraction(c["p"])) * c["cost"])
    if k == "ctx_raffle":
        return exact_is(sum(v * n for v, n in c["prizes"]) / c["n"] - c["price"])
    if k == "ctx_seats":
        a1, d, n = c["a1"], c["d"], c["n"]
        rows = [a1 + d * i for i in range(n)]
        return exact_is(rows[-1] if c["ask"] == "row" else sum(rows), "seats")
    if k == "ctx_salary":
        return approx_is(sum(c["s"] * (1 + c["p"] / 100) ** i for i in range(c["n"])), 0)
    if k == "ctx_bounce":
        h, rr = c["h"], float(Fraction(c["rr"]))
        if c["ask"] == "nth":
            return maybe_rounded(h * rr ** c["n"], 2, "ft")
        return maybe_rounded(h + 2 * sum(h * rr ** i for i in range(1, 400)), 2, "ft")
    return expect_variety(c)


def tuple_is(vals, tol=1e-9):
    def ok(t):
        m = re.fullmatch(r"\((.+)\)", t.strip())
        if not m:
            return False
        parts = [p.strip() for p in m.group(1).split(",")]
        return len(parts) == len(vals) and all(abs(ev(p).real - v) <= tol for p, v in zip(parts, vals))
    return ok


def matrix_is(rows):
    def ok(t):
        m = re.fullmatch(r"\[(.+)\]", t.strip())
        if not m:
            return False
        got = [[ev(x.strip()).real for x in row.split(",")] for row in m.group(1).split(";")]
        return len(got) == len(rows) and all(len(a) == len(b) and all(abs(x - y) < 1e-9 for x, y in zip(a, b)) for a, b in zip(got, rows))
    return ok


def line_is(m, b):
    def ok(t):
        if not t.startswith("y = "):
            return False
        return fn_check(t[4:], lambda x: m * x + b, [0.0, 1.7, -2.3])
    return ok


def eq_set(text):
    """'(x + 4)²/16 - (y - 1)²/49 = 1' -> a function of (x, y) that is 0 on the curve."""
    lhs = text.split("=")[0]
    return lambda x, y: ev(lhs, x=x, y=y).real - 1


def expect_variety(c):
    k = c["k"]
    if k == "rref_free":
        a, b, cc, d, t = c["a"], c["b"], c["c"], c["d"], c["t"]
        # x + az = b, y + cz = d, z = t
        return tuple_is([b - a * t, d - cc * t, t])
    if k == "rref_count":
        rows = [[float(Fraction(v)) for v in r.split(",")] for r in c["R"].strip("[]").split(";")]
        last = rows[-1]
        if all(abs(v) < 1e-12 for v in last[:-1]) and abs(last[-1]) > 1e-12:
            return lambda t: t == "no solution"
        if all(abs(v) < 1e-12 for v in last):
            return lambda t: t == "infinitely many solutions"
        sol = (int(rows[0][3]), int(rows[1][3]), int(rows[2][3]))
        return lambda t: t == f"exactly one solution, ({sol[0]}, {sol[1]}, {sol[2]})"
    if k == "rref_aug":
        return matrix_is(c["rows"])
    if k == "tr_reverse":
        a, h, kk = c["a"], c["h"], c["kk"]
        X, Y = c["P"]
        # g(x) = a·f(x - h) + k; (X, Y) on g  =>  f(X - h) = (Y - k)/a
        return tuple_is([X - h, (Y - kk) / a])
    if k == "tr_reflect":
        x0, y0 = c["P"]
        kind, kk = c["kind"], c["kk"]
        X = -x0 if "f(-x)" in kind else x0
        Y = (-y0 if kind.startswith("-") else y0) + kk
        # check: g(X) = ±f(±X) + k with f(x0) = y0
        return tuple_is([X, Y])
    if k == "tr_stretch":
        b = float(Fraction(c["b"]))
        x0, y0 = c["P"]
        return tuple_is([x0 / b, y0 + c["kk"]])
    if k == "hyp_asym":
        h, kk, a, b, hor = c["h"], c["kk"], c["a"], c["b"], c["hor"]
        def ok(t):
            f = eq_set(t)
            v = (h + a, kk) if hor else (h, kk + a)
            far = (h + a * 3, kk + b * math.sqrt(8)) if hor else (h + b * math.sqrt(8), kk + a * 3)   # on the curve: (3a)²/a² - 8 = 1
            return abs(f(*v)) < 1e-9 and abs(f(*far)) < 1e-9 and "+" not in t.split("=")[0].replace("x +", "").replace("y +", "")
        return ok
    if k == "hyp_foci":
        h, kk, a, b, hor = c["h"], c["kk"], c["a"], c["b"], c["hor"]
        cc = math.sqrt(a * a + b * b)
        want = sorted([(h + cc, kk), (h - cc, kk)] if hor else [(h, kk + cc), (h, kk - cc)])
        def ok(t):
            parts = t.split(" and ")
            if len(parts) != 2:
                return False
            got = []
            for p in parts:
                m = re.fullmatch(r"\((.+), (.+)\)", p.strip())
                if not m:
                    return False
                got.append((ev(m.group(1)).real, ev(m.group(2)).real))
            return all(abs(u[0] - v[0]) < 1e-9 and abs(u[1] - v[1]) < 1e-9 for u, v in zip(sorted(got), want))
        return ok
    if k == "ser_find_n":
        a1, d, S = c["a1"], c["d"], c["S"]
        n, tot = 0, 0
        while tot != S and n < 500:
            tot += a1 + n * d
            n += 1
        return exact_is(n)
    if k == "ser_first_last":
        return exact_is(c["n"] * (c["a1"] + c["an"]) / 2)
    if k == "ser_geo_formula":
        q = float(Fraction(c["q"]))
        return lambda t: same(ev(t), sum(c["a1"] * q ** i for i in range(c["n"])), 1e-9)
    if k == "pr_die_or":
        return lambda t: same(ev(t), len(set(c["A"]) | set(c["B"])) / 6)
    if k == "pr_cards_or":
        deck = [(rk, st) for rk in range(1, 14) for st in "HDCS"]
        test = {"suit": lambda x: x[1] == "H", "suit2": lambda x: x[1] == "S", "color": lambda x: x[1] in "HD", "rank": lambda x: x[0] == 13,
                "face": lambda x: x[0] in (11, 12, 13), "ace": lambda x: x[0] == 1}
        n = sum(1 for x in deck if test[c["e1"]](x) or test[c["e2"]](x))
        return lambda t: same(ev(t), n / 52)
    if k in ("heron_cost", "heron_height"):
        a, b, cc = c["s"]
        s_ = (a + b + cc) / 2
        A = math.sqrt(s_ * (s_ - a) * (s_ - b) * (s_ - cc))
        if k == "heron_cost":
            return lambda t: same(ev(t.replace("$", "").replace(",", "")), A * c["price"], 1e-9)
        return lambda t: same(ev(t), 2 * A / max(a, b, cc), 1e-9)
    if k == "amb_height":
        A, a, b = c["A"], c["a"], c["b"]
        h = b * math.sin(math.radians(A))
        n = 0 if a < h else (1 if a >= b else 2)
        word = {0: "no triangle", 1: "one triangle", 2: "two triangles"}[n]
        def ok(t):
            m = re.fullmatch(r"h ≈ (\d+\.\d); (.+)", t)
            return bool(m) and abs(float(m.group(1)) - h) <= 0.05 + 1e-9 and m.group(2) == word
        return ok
    if k == "amb_second":
        A, a, b = c["A"], c["a"], c["b"]
        B1 = math.degrees(math.asin(b * math.sin(math.radians(A)) / a))
        return approx_is(180 - B1, 1)
    if k == "lp_axis_corner":
        l1, l2 = c["l1"], c["l2"]
        if c["which"] == "y":
            return tuple_is([0, min(l1[2] / l1[1], l2[2] / l2[1])])
        return tuple_is([min(l1[2] / l1[0], l2[2] / l2[0]), 0])
    if k == "lp_max":
        best = max(c["p"] * x + c["q"] * y for x, y in c["corners"])
        return exact_is(best)
    if k == "lp_in_region":
        l1, l2 = c["l1"], c["l2"]
        def ok(t):
            m = re.fullmatch(r"\((-?\d+), (-?\d+)\)", t)
            if not m:
                return False
            x, y = int(m.group(1)), int(m.group(2))
            return x >= 0 and y >= 0 and l1[0] * x + l1[1] * y <= l1[2] and l2[0] * x + l2[1] * y <= l2[2]
        return ok
    if k == "norm_x":
        return exact_is(c["mu"] + float(Fraction(c["z"])) * c["sd"])
    if k == "norm_count":
        return exact_is({1: 0.68, 2: 0.95, 3: 0.997}[c["kk"]] * c["N"])
    if k == "rot_entry":
        th = math.radians(c["th"])
        R = [[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]]
        return lambda t: same(ev(t), R[c["pos"][0] - 1][c["pos"][1] - 1], 1e-9) or (abs(R[c["pos"][0] - 1][c["pos"][1] - 1]) < 1e-12 and t == "0")
    if k == "rot_find_angle":
        (x, y), (X, Y) = c["P"], c["Q"]
        ang = round(math.degrees(math.atan2(X * y - x * Y, x * X + y * Y) * -1)) % 360
        ang = round(math.degrees(math.atan2(x * Y - y * X, x * X + y * Y))) % 360
        return lambda t: t == f"{ang}°"
    if k == "derive_coords":
        b, A = c["b"], math.radians(c["A"])
        return lambda t: tuple_is([round(b * math.cos(A), 1), round(b * math.sin(A), 1)], 1e-6)(t) and abs(b * math.cos(A) - round(b * math.cos(A), 1)) <= 0.05
    if k == "derive_area":
        return lambda t: abs(ev(t).real - 0.5 * c["c"] * c["b"] * math.sin(math.radians(c["A"]))) <= 0.05 + 1e-9 and re.fullmatch(r"-?\d+\.\d", t) is not None
    if k == "line_point_slope":
        m = float(Fraction(c["m"]))
        x0, y0 = c["P"]
        return line_is(m, y0 - m * x0)
    if k == "line_table":
        xs, ys = c["xs"], c["ys"]
        m = (ys[-1] - ys[0]) / (xs[-1] - xs[0])
        return line_is(m, ys[0] - m * xs[0])
    if k == "line_intercepts":
        a, b = c["a"], c["b"]
        return line_is(-b / a, b)
    if k == "stat_skew":
        return lambda t: t == ("skewed right" if c["mean"] > c["med"] else "skewed left")
    if k == "stat_remove":
        d = c["data"]
        return approx_is(sum(d) / len(d) - (sum(d) - c["out"]) / (len(d) - 1), 1)
    if k == "seq_two_terms":
        return exact_is(c["a1"] + (c["t"] - 1) * c["d"])
    if k == "seq_recursive":
        a = c["a1"]
        for _ in range(c["n"] - 1):
            a = c["m"] * a + c["c"]
        return exact_is(a)
    if k == "vt_compose":
        A, B, v = c["A"], c["B"], c["v"]
        Av = [A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1]]
        w = [B[0][0] * Av[0] + B[0][1] * Av[1], B[1][0] * Av[0] + B[1][1] * Av[1]]
        return lambda t: t == f"⟨{w[0]}, {w[1]}⟩"
    if k == "vt_which_matrix":
        e1, e2 = {"reflects vectors over the x-axis": ((1, 0), (0, -1)), "reflects vectors over the y-axis": ((-1, 0), (0, 1)),
                  "reflects vectors over the line y = x": ((0, 1), (1, 0)), "rotates vectors 90° counterclockwise": ((0, 1), (-1, 0)),
                  "rotates vectors 180°": ((-1, 0), (0, -1)), "doubles the length of every vector": ((2, 0), (0, 2))}[c["desc"]]
        # columns are the images of ⟨1, 0⟩ and ⟨0, 1⟩
        return matrix_is([[e1[0], e2[0]], [e1[1], e2[1]]])
    if k == "inf_decimal":
        rep = c["rep"]
        val = int(rep) / (10 ** len(rep) - 1)
        return lambda t: same(ev(t), val, 1e-12) and "/" in t and math.gcd(*(int(x) for x in t.split("/"))) == 1
    if k == "inf_find":
        q, a1 = float(Fraction(c["q"])), c["a1"]
        return lambda t: same(ev(t), a1 if c["ask"] == "a1" else q, 1e-12)
    if k == "inv_singular_k":
        M = c["M"].strip("[]").replace("k", "K")
        def ok(t):
            kv = ev(t).real
            rows = [[kv if x.strip() == "K" else float(Fraction(x.strip())) for x in r.split(",")] for r in M.split(";")]
            return abs(rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]) < 1e-9
        return ok
    if k == "inv_solve_entry":
        A, b = c["A"], c["b"]
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        x = (b[0] * A[1][1] - A[0][1] * b[1]) / det
        y = (A[0][0] * b[1] - A[1][0] * b[0]) / det
        return exact_is(x if c["which"] == "x" else y)
    if k == "var_combined":
        kk = float(Fraction(c["y1"])) * c["z1"] / c["x1"]
        return lambda t: same(ev(t), kk * c["x2"] / c["z2"], 1e-12)
    if k == "var_k":
        y, x, z = float(Fraction(c["y"])), c["x"], c["z"]
        return lambda t: same(ev(t), {"directly": y / x, "inversely": y * x, "jointly": y / (x * z)}[c["kind"]], 1e-12)
    if k == "area_parallelogram":
        return approx_is(c["a"] * c["b"] * math.sin(math.radians(c["t"])), 1)
    if k == "area_isosceles":
        return approx_is(0.5 * c["s"] ** 2 * math.sin(math.radians(c["t"])), 1)
    if k == "mt_point":
        M, (x, y) = c["M"], c["P"]
        return tuple_is([M[0][0] * x + M[0][1] * y, M[1][0] * x + M[1][1] * y])
    if k == "mt_dilate":
        kk = float(Fraction(c["kk"]))
        return matrix_is([[kk * v for v in row] for row in c["V"]])
    if k.startswith("adv_"):
        return expect_advanced(c)
    return expect_selectall(c)


def expect_advanced(c):
    k = c["k"]
    if k == "adv_lp_area":
        (a1, b1, c1), (a2, b2, c2) = c["l1"], c["l2"]
        # area of {x, y ≥ 0, both constraints} by a fine grid of trapezoids in x
        def top(x):
            return max(0.0, min((c1 - a1 * x) / b1, (c2 - a2 * x) / b2))
        xs = min(c1 / a1, c2 / a2)
        n = 20000
        area = sum((top(xs * i / n) + top(xs * (i + 1) / n)) / 2 * xs / n for i in range(n))
        return lambda t: abs(ev(t).real - area) < 1e-3
    if k == "adv_amb_range":
        h = c["b"] * math.sin(math.radians(c["A"]))
        def ok(t):
            m = re.fullmatch(r"(.+) < a < (\d+)", t)
            return bool(m) and abs(ev(m.group(1)).real - h) < 1e-9 and int(m.group(2)) == c["b"]
        return ok
    if k == "adv_heron_consec":
        x = (c["P"] - 3) / 3
        a, b, cc = x, x + 1, x + 2
        s_ = (a + b + cc) / 2
        return approx_is(math.sqrt(s_ * (s_ - a) * (s_ - b) * (s_ - cc)), 1)
    if k == "adv_norm_between":
        # empirical-rule areas between whole standard deviations, from 68-95-99.7
        band = {0: 34, 1: 13.5, 2: 2.35}
        lo, hi = c["k1"], c["k2"]
        p = sum(band[abs(z) if z >= 0 else abs(z) - 1] for z in range(lo, hi))
        return lambda t: t.endswith("%") and abs(float(t[:-1]) - p) < 1e-9
    if k == "adv_two_angles":
        d, a, b = c["d"], math.radians(c["a"]), math.radians(c["b"])
        # solve h = x tan b = (x + d) tan a
        x = d * math.tan(a) / (math.tan(b) - math.tan(a))
        return approx_is(x * math.tan(b), 0)
    raise KeyError(k)


def expect_selectall(c):
    """Predicate: is this select-all choice a correct one?"""
    k = c["k"]
    if k == "sa_even":
        def even(t):
            f = t.split("=", 1)[1]
            return all(abs(ev(f, x=x) - ev(f, x=-x)) < 1e-9 for x in (0.7, 1.3, 2.9))
        return even
    if k == "sa_coterminal":
        return lambda t: (int(t.rstrip("°")) - c["d"]) % 360 == 0
    if k == "sa_orthogonal":
        a, b = c["v"]
        return lambda t: (lambda u: a * u[0] + b * u[1] == 0)([int(x) for x in t.strip("⟨⟩").split(",")])
    if k == "sa_invertible":
        def inv(t):
            (p_, q_), (r_, s_) = [[int(x) for x in row.split(",")] for row in t.strip("[]").split(";")]
            return p_ * s_ - q_ * r_ != 0
        return inv
    if k == "sa_ellipse":
        def ell(t):
            def co(v):
                m = re.search(r"(^|[+-] |-)(\d*)" + v, t)
                if not m:
                    return 0
                sign = -1 if m.group(1).strip().startswith("-") else 1
                return sign * (int(m.group(2)) if m.group(2) else 1)
            A, C = co("x²"), co("y²")
            return A * C > 0 and A != C
        return ell
    if k == "sa_ineq":
        m, b, op = c["m"], c["b"], c["op"]
        def ok(t):
            x, y = (int(v) for v in t.strip("()").split(","))
            rhs = m * x + b
            return {"<": y < rhs, ">": y > rhs, "≤": y <= rhs, "≥": y >= rhs}[op]
        return ok
    if k == "sa_acute":
        def acute(t):
            a, b, cc = sorted(int(v) for v in t.split(","))
            return a + b > cc and a * a + b * b > cc * cc
        return acute
    if k == "sa_mutex":
        E = {"an even number": {2, 4, 6}, "an odd number": {1, 3, 5}, "a number greater than 4": {5, 6}, "a number less than 3": {1, 2}, "a 6": {6},
             "a prime number": {2, 3, 5}, "a multiple of 3": {3, 6}, "a 1": {1}, "a number greater than 3": {4, 5, 6}}
        def mx(t):
            m = re.fullmatch(r"rolling (.+) and rolling (.+)", t)
            return not (E[m.group(1)] & E[m.group(2)])
        return mx
    if k == "sa_geometric":
        def geo(t):
            terms = [Fraction(x.strip()) for x in t.rstrip(", …").split(",")]
            return all(terms) and len({terms[i + 1] / terms[i] for i in range(len(terms) - 1)}) == 1
        return geo
    raise KeyError(k)


def right(pred, text):
    try:
        return bool(pred(text))
    except Exception:
        return False


def main():
    checks = json.load(open(os.path.join(HERE, "out", "checks.json"), encoding="utf-8"))
    items = {}
    for f in os.listdir(os.path.join(ROOT, "question-banks", "precalculus")):
        if f.endswith(".json"):
            for q in json.load(open(os.path.join(ROOT, "question-banks", "precalculus", f), encoding="utf-8"))["questions"]:
                items[q["id"]] = q
    errors, n = [], 0
    for qid, c in checks.items():
        q = items.get(qid)
        if q is None:
            errors.append(f"{qid}: not in the banks")
            continue
        n += 1
        if q["format"] == "select-all":
            pred = expect(c)
            for o in q["options"]:
                if right(pred, o["text"]) != o["correct"]:
                    errors.append(f"{qid}: choice {o['text']!r} is marked {o['correct']}")
            if q["answer"] != [o["text"] for o in q["options"] if o["correct"]] or len(q["answer"]) < 2 or len(q["options"]) != 6:
                errors.append(f"{qid}: answer list, at least 2 correct and 6 choices")
            continue
        if q["format"] == "open-response":
            for i, (part, pc) in enumerate(zip(q["parts"], c["parts"])):
                for s in pc.get("show", []):
                    if s not in part["prompt"]:
                        errors.append(f"{qid} part {i}: {s!r} not printed")
                if not right(expect(pc), part["answer"]):
                    errors.append(f"{qid} part {i}: answer {part['answer']!r} is wrong")
            continue
        for s in c.get("show", []):
            if s not in q["prompt"]:
                errors.append(f"{qid}: {s!r} not printed")
        pred = expect(c)
        if not right(pred, q["answer"]):
            errors.append(f"{qid}: answer {q['answer']!r} is wrong ({q['prompt'][:80]!r})")
        if q["format"] == "multiple-choice":
            opts = q["options"]
            if len(opts) != 4 or len({o["text"] for o in opts}) != 4:
                errors.append(f"{qid}: needs four distinct options")
            if [o["text"] for o in opts if o["correct"]] != [q["answer"]]:
                errors.append(f"{qid}: exactly one correct option, equal to the answer")
            for o in opts:
                if not o["correct"] and right(pred, o["text"]):
                    errors.append(f"{qid}: distractor {o['text']!r} is also right")
        if "student" in c:
            if right(pred, c["student"]):
                errors.append(f"{qid}: the student answer {c['student']!r} is right")
            if f"answer: {c['student']}\n" not in q["prompt"]:
                errors.append(f"{qid}: the student answer is not printed")
    for e in errors[:60]:
        print(e)
    print(f"checked {n} items")
    print(f"TOTAL ERRORS {len(errors)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
