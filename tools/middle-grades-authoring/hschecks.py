"""Independent SymPy checks for the Precalculus and Calculus banks.

P(text) parses student-facing text (√, ∛, π, e, ∞, superscripts, ⁻¹ inverse trig, log bases with subscripts,
|…|, degrees, implicit multiplication) into SymPy. The `hs` check evaluates chk['code'] — the problem restated
in SymPy, usually applying an operation to the displayed text, e.g. diff(P('3x² - 5x'), x) — and compares it
with the answer parsed by P. Modes: expr, round, set, interval, matrix, vector, point, eqn (equation of a curve),
yesno/text. Nothing here imports the authoring families.
"""
import math, re
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
import checks_custom as C
from checks_custom import reg

X, Y, Tt, N_, K, H_, R_, TH, U = sp.symbols("x y t n k h r theta u", real=True)
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
SUP = {c: d for c, d in zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣⁿᵗ", "0123456789-xnt")}
SUB = {c: d for c, d in zip("₀₁₂₃₄₅₆₇₈₉", "0123456789")}
LOC = {"x": X, "y": Y, "t": Tt, "n": N_, "k": K, "h": H_, "r": R_, "θ": TH, "theta": TH, "u": U, "e": sp.E, "pi": sp.pi,
       "ln": sp.log, "log10": lambda a: sp.log(a, 10), "sqrt": sp.sqrt, "cbrt": lambda a: sp.real_root(a, 3), "Abs": sp.Abs,
       "asin": sp.asin, "acos": sp.acos, "atan": sp.atan, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc, "cot": sp.cot,
       "oo": sp.oo, "E": sp.E, "i": sp.I, "I": sp.I, "LOGB": lambda a, b: sp.log(a, b)}


def _bars(s):
    for _ in range(6):
        s2 = re.sub(r"\|([^|]+)\|", r"Abs(\1)", s)
        if s2 == s:
            break
        s = s2
    return s


def _roots(s):
    for sym, fn in (("√", "sqrt"), ("∛", "cbrt")):
        s = s.replace(sym + "(", fn + "(")
        s = re.sub(sym + r"(\d+(?:\.\d+)?|[a-zA-Zθ])", fn + r"(\1)", s)
    return s


def P(text):
    s = str(text).strip().replace("−", "-").replace("·", "*").replace("×", "*").replace("÷", "/").replace("π", " pi ").replace("∞", "oo").replace("′", "")
    s = re.sub(r"^[A-Za-z](?:⁻¹)?(?:\([A-Za-z]\))?\s*=\s*", "", s)  # y = …, f(x) = …
    s = re.sub(r"(sin|cos|tan)⁻¹", r"a\1", s)
    s = re.sub(r"log([₀₁₂₃₄₅₆₇₈₉]+)\(([^()]*(?:\([^()]*\))*[^()]*)\)", lambda m: f"LOGB({m.group(2)}, {''.join(SUB[c] for c in m.group(1))})", s)
    s = re.sub(r"\blog\(", "log10(", s)
    s = re.sub(r"ln\|([^|]+)\|", r"log(|\1|)", s)
    s = re.sub(r"ln(?=\()", "log", s)
    s = re.sub(r"(\d+(?:\.\d+)?)°", r"(\1*pi/180)", s)
    s = re.sub("[⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣⁿᵗ]+", lambda m: "**(" + "".join(SUP[c] for c in m.group(0)) + ")", s)
    s = _roots(_bars(s))
    s = re.sub(r"(?<=[0-9A-Za-z)])(asin|acos|atan)\(", r"*\1(", s)
    s = re.sub(r"(?<=[0-9B-Zb-z)])(sin|cos|tan)\(", r"*\1(", s)
    s = re.sub(r"(?<=[0-9)])(sin|cos|tan)\(", r"*\1(", s)
    s = re.sub(r"(?<=[0-9A-Za-z)])(sec|csc|cot|sqrt|cbrt|Abs|log10|log|LOGB|exp)\(", r"*\1(", s)
    s = s.replace("^", "**")
    s = re.sub(r"(?<![A-Za-z])e\*\*", "E**", s)
    return parse_expr(s, local_dict=dict(LOC), transformations=TR, evaluate=True)


def _num_eq(a, b, syms=None):
    a, b = sp.sympify(a), sp.sympify(b)
    if any(v in (sp.oo, -sp.oo, sp.zoo) for v in (a, b)):
        return a == b
    try:
        if sp.simplify(a - b) == 0:
            return True
    except Exception:
        pass
    fs = sorted((a.free_symbols | b.free_symbols), key=str)
    pts = [-2.43, -0.83, 0.37, 0.61, 1.13, 1.71, 2.29, 3.67]
    ok = 0
    for i, p in enumerate(pts):
        sub = {s_: sp.Float(p + 0.17 * j) for j, s_ in enumerate(fs)}
        try:
            va, vb = complex(sp.N(a.subs(sub), 30)), complex(sp.N(b.subs(sub), 30))
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if not (math.isfinite(abs(va)) and math.isfinite(abs(vb))):
            continue
        if abs(va - vb) > 1e-9 * max(1, abs(va), abs(vb)):
            return False
        ok += 1
    return ok >= 3


def strip_units(t):
    t = str(t).strip().rstrip(".")
    m0 = re.fullmatch(r"(-?[\d.,/]+) [A-Za-z][A-Za-z ]*", t)
    if m0:
        return m0.group(1).replace(",", "")
    t = re.sub(r"\s+[A-Za-z°]+[²³]?/[A-Za-z]+[²³]?$", "", t)
    t = re.sub(r"\s*(m/s²|m/s|ft/s²|ft/s|cm/s|cm³/s|cm²/s|ft³/min|ft²/s|in³/s|km/h|L/min|gal/min)\s*$", "", t)
    t = re.sub(r"\s*(square|cubic)?\s*(units?|feet|foot|ft|inches|in\.?|meters?|m|cm|km|miles?|mi|seconds?|s|hours?|minutes?|degrees|radians|lb|pounds|N|newtons|mph|km/h|people|dollars|gallons?|liters?|L|units²|ft²|m²|cm²|in²|ft³|m³|cm³|in³)\s*$", "", t)
    t = re.sub(r"\s*(per\s+[a-z]+|/(?:hr|h|min|sec|day|week|year|yr|month|gal|lb|oz|ft|mi|item|unit|person|hour|minute|second)s?)$", "", t)
    t = t.replace("$", "").replace(",", "")
    t = re.sub(r"%$", "/100", t)
    return t.strip()


def ns():
    d = {k: getattr(sp, k) for k in ("diff", "integrate", "limit", "solve", "solveset", "simplify", "expand", "factor", "Rational", "sqrt", "pi", "E", "oo", "sin", "cos", "tan", "asin", "acos",
                                      "atan", "log", "exp", "Matrix", "Interval", "Union", "S", "Abs", "Symbol", "symbols", "N", "nsimplify", "Eq", "series", "binomial", "factorial", "Piecewise",
                                      "sec", "csc", "cot", "re", "im", "I", "conjugate", "atan2", "floor", "ceiling", "summation", "Sum", "Mod", "acot", "Ropen" if False else "Integer", "together", "apart", "cancel", "degree", "Poly", "real_root")}
    d.update({"P": P, "x": X, "y": Y, "t": Tt, "n": N_, "k": K, "h": H_, "r": R_, "theta": TH, "u": U, "Reals": sp.S.Reals, "math": math,
              "ineq_set": lambda s, v=X: sp.solve_univariate_inequality(PREL(s, v), v, relational=False), "lp": lp, "gcd": sp.gcd, "eye": sp.eye, "Min": sp.Min, "Max": sp.Max, "erf": sp.erf, "sum": sum, "range": range, "P_matrix": lambda t: P_matrix(t), "sp_rem": lambda txt, a: sp.rem(P(txt), X - a, X)})
    return d


def lp(pa, pb, cons, goal):
    """Optimum of pa*x + pb*y over x ≥ 0, y ≥ 0 and a*x + b*y ≤ c: evaluate every feasible intersection of boundary lines."""
    lines = [(1, 0, 0), (0, 1, 0)] + [tuple(c_) for c_ in cons]
    pts = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            (a1, b1, c1), (a2, b2, c2) = lines[i], lines[j]
            d = a1 * b2 - a2 * b1
            if d == 0:
                continue
            px, py = sp.Rational(c1 * b2 - c2 * b1, d), sp.Rational(a1 * c2 - a2 * c1, d)
            if px >= 0 and py >= 0 and all(a * px + b * py <= c for a, b, c in cons):
                pts.append(pa * px + pb * py)
    return max(pts) if goal == "maximum" else min(pts)


def PREL(s, v=X):
    m = re.split(r"(≤|≥|<|>|=)", s)
    l, op, r_ = P(m[0]), m[1], P(m[2])
    return {"<": sp.Lt, ">": sp.Gt, "≤": sp.Le, "≥": sp.Ge, "=": sp.Eq}[op](l, r_)


def P_interval(t):
    t = str(t).strip()
    if t.lower() in ("no solution", "∅", "empty set"):
        return sp.S.EmptySet
    parts = [p.strip() for p in t.split("∪")]
    out = sp.S.EmptySet
    for p in parts:
        m = re.fullmatch(r"([\[(])\s*(.+?)\s*,\s*(.+?)\s*([\])])", p)
        if not m:
            raise ValueError("bad interval " + p)
        a, b = P(m.group(2)), P(m.group(3))
        if (a == -sp.oo and m.group(1) == "[") or (b == sp.oo and m.group(4) == "]") or not a < b:
            raise ValueError("infinity cannot be included / empty interval")
        out = sp.Union(out, sp.Interval(a, b, left_open=m.group(1) == "(", right_open=m.group(4) == ")"))
    return out


def P_matrix(t):
    t = str(t).strip()
    t = re.sub(r"^[A-Z]\s*=\s*", "", t)
    m = re.fullmatch(r"\[(.*)\]", t)
    rows = [[P(c) for c in row.split(",")] for row in m.group(1).split(";")]
    return sp.Matrix(rows)


def P_tuple(t, open_="(", close=")"):
    t = str(t).strip()
    m = re.fullmatch(re.escape(open_) + r"(.*)" + re.escape(close), t)
    if not m:
        raise ValueError("bad tuple " + t)
    depth, cur, out = 0, "", []
    for ch in m.group(1):
        if ch in "([⟨":
            depth += 1
        if ch in ")]⟩":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return [P(s) for s in out]


@reg
def hs(chk, text):
    try:
        want = eval(chk["code"], ns())
    except Exception as e:
        raise RuntimeError(f"check code failed: {chk['code']} ({e})")
    mode = chk.get("mode", "expr")
    t = str(text).strip()
    try:
        if mode == "expr":
            return _num_eq(P(strip_units(t)), want)
        if mode == "round":
            v = float(sp.N(want, 30))
            return C.round_text(v, chk["places"]) == strip_units(re.sub(r"^[A-Za-z]\s*=\s*", "", t)).rstrip("°")
        if mode == "deg":
            v = float(sp.N(want, 30))
            return C.round_text(v, chk.get("places", 1)) + "°" == re.sub(r"^[A-Za-zθ]\s*=\s*", "", t)
        if mode == "set":
            if t.lower() == "no solution":
                return len(list(want)) == 0
            items = [re.sub(r"^[A-Za-zθ]\s*=\s*", "", s.strip()) for s in re.split(r"\s+or\s+|,\s*(?![^()]*\))", t) if s.strip()]
            got = [P(strip_units(s)) for s in items]
            w = list(want)
            if len(got) != len(w):
                return False
            used = [False] * len(w)
            for g in got:
                hit = next((j for j, wv in enumerate(w) if not used[j] and _num_eq(g, wv)), None)
                if hit is None:
                    return False
                used[hit] = True
            return True
        if mode == "interval":
            return P_interval(t) == sp.sympify(want)
        if mode == "matrix":
            got = P_matrix(t)
            return got.shape == want.shape and all(_num_eq(a, b) for a, b in zip(got, want))
        if mode == "vector":
            got = P_tuple(t, "⟨", "⟩")
            return len(got) == len(want) and all(_num_eq(a, b) for a, b in zip(got, want))
        if mode == "point":
            got = P_tuple(t)
            return len(got) == len(want) and all(_num_eq(a, b) for a, b in zip(got, want))
        if mode == "anti":
            if not re.search(r"\+ C$", t):
                return False
            F_ = P(t[: t.rindex("+ C")].strip())
            return _num_eq(sp.diff(F_, X), want)
        if mode == "points":
            items = re.findall(r"\([^()]*(?:\([^()]*\)[^()]*)*\)", t)
            if re.sub(r"\([^()]*(?:\([^()]*\)[^()]*)*\)", "", t).replace(",", "").replace("and", "").strip():
                return False
            got = [P_tuple(s_) for s_ in items]
            w = [list(p_) for p_ in want]
            if len(got) != len(w):
                return False
            used = [False] * len(w)
            for g in got:
                hit = next((j for j, wv in enumerate(w) if not used[j] and len(g) == len(wv) and all(_num_eq(a_, b_) for a_, b_ in zip(g, wv))), None)
                if hit is None:
                    return False
                used[hit] = True
            return True
        if mode == "eqn":
            l, r_ = t.split("=")
            g = P(l) - P(r_)
            w = sp.sympify(want)
            ratio = sp.simplify(g / w)
            return ratio.is_number and ratio != 0 and len(ratio.free_symbols) == 0
        if mode == "text":
            return t == str(want)
    except Exception:
        return False
    raise ValueError("unknown hs mode " + mode)


@reg
def shift_desc(chk, text):
    """text describes the shift taking y = f(x) to y = f(x - h) + k."""
    h, k = chk["h"], chk["k"]
    m = re.fullmatch(r"(\d+) units? (right|left) and (\d+) units? (up|down)", str(text).strip())
    if not m:
        return False
    hh = int(m.group(1)) * (1 if m.group(2) == "right" else -1)
    kk = int(m.group(3)) * (1 if m.group(4) == "up" else -1)
    return hh == h and kk == k


@reg
def log_form(chk, text):
    """text is log_b(v) = e, equivalent to b^e = v."""
    m = re.fullmatch(r"log([₀₁₂₃₄₅₆₇₈₉]*)\((.+)\) = (-?\d+)", str(text).strip())
    if not m:
        return False
    b = int("".join(SUB[c] for c in m.group(1))) if m.group(1) else 10
    return b == chk["b"] and int(m.group(3)) == chk["e"] and _num_eq(P(m.group(2)), sp.Integer(chk["b"]) ** chk["e"]) and _num_eq(P(m.group(2)), sp.sympify(chk["v"]))


@reg
def asym(chk, text):
    """text is 'y - k = ±m(x - h)' (both asymptotes of a hyperbola)."""
    t = str(text).strip()
    if t.count("±") != 1 or t.count("=") != 1:
        return False
    h, k, m = sp.sympify(chk["h"]), sp.sympify(chk["k"]), sp.sympify(chk["m"])
    for sgn, ch in ((1, "+"), (-1, "-")):
        l, r_ = t.replace("±", ch if ch == "-" else "").split("=")
        g = P(l) - P(r_)
        w = (Y - k) - sgn * m * (X - h)
        ratio = sp.simplify(g / w)
        if not (ratio.is_number and ratio != 0):
            return False
    return True


@reg
def conic_type(chk, text):
    A, C = chk["A"], chk["C"]
    typ = "parabola" if A * C == 0 else "circle" if A == C else "ellipse" if A * C > 0 else "hyperbola"
    return str(text).strip() == typ


@reg
def period(chk, text):
    """Period of a single sinusoid/tangent a·f(bx) + d, computed from the parsed expression."""
    e = P(chk["expr"])
    fs = [f for f in e.atoms(sp.Function) if f.func in (sp.sin, sp.cos, sp.tan, sp.sec, sp.csc, sp.cot)]
    if len(fs) != 1:
        raise ValueError("period: expected one trig function")
    f = fs[0]
    b = sp.diff(f.args[0], X)
    base = sp.pi if f.func in (sp.tan, sp.cot) else 2 * sp.pi
    return _num_eq(P(strip_units(text)), base / abs(b))


@reg
def phase(chk, text):
    m = re.fullmatch(r"(.+?) (right|left)", str(text).strip())
    if not m:
        return False
    return _num_eq(P(m.group(1)) * (1 if m.group(2) == "right" else -1), sp.sympify(chk["c"]))


@reg
def deg_set(chk, text):
    f = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[chk["f"]]
    sols = sp.solveset(sp.Eq(f(X), sp.sympify(chk["v"])), X, sp.Interval.Ropen(0, 2 * sp.pi))
    want = sorted(C.round_text(float(sp.N(s_ * 180 / sp.pi, 30)), chk["places"]) + "°" for s_ in sols)
    got = sorted(re.sub(r"^x\s*[≈=]\s*", "", p_.strip()) for p_ in str(text).split(" or "))
    return got == want


@reg
def los_rel(chk, text):
    """'a/sin(A°) = b/sin(B°)' with each side over the sine of its OPPOSITE angle (checked numerically on a real triangle)."""
    A, B = math.radians(chk["A"]), math.radians(chk["B"])
    a, b = math.sin(A), math.sin(B)   # sides proportional to the sines of the opposite angles
    l, r_ = str(text).split("=")
    a_s, b_s = sp.Symbol("a_s"), sp.Symbol("b_s")
    sub = lambda s: s.replace("a", "a_s", 1) if False else s
    try:
        L = parse_expr(_roots(l.strip().replace("°", "*pi/180").replace("·", "*")).replace("a", "a_s", 1).replace("b", "b_s", 1) if False else l.strip().replace("°", "*pi/180").replace("·", "*"), local_dict={"a": a_s, "b": b_s, "sin": sp.sin, "cos": sp.cos, "pi": sp.pi}, transformations=TR)
        R = parse_expr(r_.strip().replace("°", "*pi/180").replace("·", "*"), local_dict={"a": a_s, "b": b_s, "sin": sp.sin, "cos": sp.cos, "pi": sp.pi}, transformations=TR)
    except Exception:
        return False
    v = sp.N((L - R).subs({a_s: a, b_s: b}))
    v2 = sp.N((L - R).subs({a_s: 2 * a, b_s: 2 * b}))
    return abs(v) < 1e-9 and abs(v2) < 1e-9


def _ssa(A, a, b):
    A_ = math.radians(A)
    s = b * math.sin(A_) / a
    out = []
    if s > 1 + 1e-12:
        return out
    B1 = math.asin(min(1.0, s))
    for B in {round(B1, 12), round(math.pi - B1, 12)}:
        if A_ + B < math.pi - 1e-9:
            out.append(math.degrees(B))
    return sorted(out)


@reg
def ssa_count(chk, text):
    return str(text).strip() == str(len(_ssa(chk["A"], chk["a"], chk["b"])))


@reg
def ssa_angles(chk, text):
    want = sorted(C.round_text(v, chk["places"]) + "°" for v in _ssa(chk["A"], chk["a"], chk["b"]))
    got = sorted(re.sub(r"^B\s*[≈=]\s*", "", p_.strip()) for p_ in str(text).split(" or "))
    return got == want


@reg
def side_area(chk, text):
    a, b, Cd = chk["a"], chk["b"], math.radians(chk["C"])
    c = math.sqrt(a * a + b * b - 2 * a * b * math.cos(Cd))
    A = 0.5 * a * b * math.sin(Cd)
    return str(text).strip() == f"side ≈ {C.round_text(c, 1)} m; area ≈ {C.round_text(A, 1)} m²"


@reg
def dims(chk, text):
    m = re.fullmatch(r"(\d+) × (\d+)", str(text).strip())
    return bool(m) and (int(m.group(1)), int(m.group(2))) == (chk["m"], chk["n"])


@reg
def prod_dims(chk, text):
    if chk["n"] != chk["p"]:
        return str(text).strip() == "not defined"
    return dims({"m": chk["m"], "n": chk["q"]}, text)


@reg
def data_entry(chk, text):
    return str(text).strip() == f"{chk['v']} {chk['item']} at the {chk['store']} store"


@reg
def aug(chk, text):
    return P_matrix(text) == eval(chk["code"], ns())


@reg
def rref_kind(chk, text):
    R = eval(chk["code"], ns())
    A, b = R[:, :-1], R[:, -1]
    ra, rab = A.rank(), R.rank()
    t = str(text).strip()
    if ra < rab:
        return t == "no solution"
    if ra < A.cols:
        return t == "infinitely many solutions"
    sol = A.solve(b)
    return t == "one solution: (" + ", ".join(str(v) for v in sol) + ")"


@reg
def two_step(chk, text):
    A = eval(chk["code"], ns())
    n = A.rows
    cnt = sum(1 for m in range(n) if A[chk["i"], m] and A[m, chk["j"]])
    return str(text).strip() == str(cnt)


@reg
def singular(chk, text):
    d = eval(chk["code"], ns()).det()
    t = str(text).strip()
    return t == ("A has no inverse, so X = A⁻¹B cannot be used" if d == 0 else "A has an inverse, so X = A⁻¹B gives the unique solution")


@reg
def vec_round(chk, text):
    m, th = chk["m"], math.radians(chk["th"])
    want = f"⟨{C.round_text(m * math.cos(th), chk['places'])}, {C.round_text(m * math.sin(th), chk['places'])}⟩"
    return str(text).strip() == want


@reg
def wind(chk, text):
    def v(m, bearing):
        return sp.Matrix([m * sp.sin(sp.rad(bearing)), m * sp.cos(sp.rad(bearing))])   # east, north components
    R = v(chk["s"], chk["h"]) + v(chk["w"], chk["d"])
    if chk["ask"] == "speed":
        return str(text).strip() == C.round_text(float(sp.N(R.norm(), 30)), 1) + " mph"
    b = float(sp.N(sp.atan2(R[0], R[1]) * 180 / sp.pi, 30)) % 360
    return str(text).strip() == C.round_text(b, 1) + "°"


@reg
def polar_pt(chk, text):
    got = P_tuple(str(text).strip())
    if len(got) != 2:
        return False
    rr, th = got
    xx, yy = chk["x"], chk["y"]
    if not _num_eq(rr, sp.sqrt(xx * xx + yy * yy)):
        return False
    want = float(sp.N(sp.atan2(yy, xx), 30)) % (2 * math.pi)
    if "places" in chk:
        return C.round_text(want, chk["places"]) == str(text).strip().rstrip(")").split(",")[1].strip()
    return _num_eq(th, sp.nsimplify(want, [sp.pi])) and 0 <= float(th) < 2 * math.pi


@reg
def trigform(chk, text):
    t = str(text).strip()
    m = re.fullmatch(r"(.*?)\(?cos\((.+?)\) \+ i·sin\((.+?)\)\)?", t)
    if not m or m.group(2) != m.group(3):
        return False
    rr = P(m.group(1)) if m.group(1) else sp.Integer(1)
    th = P(m.group(2))
    z = P(chk["z"])
    return _num_eq(rr * sp.cos(th), sp.re(z)) and _num_eq(rr * sp.sin(th), sp.im(z)) and 0 <= float(th) < 2 * math.pi and float(rr) > 0


def _dec(v):
    from fractions import Fraction
    v = sp.Rational(v)
    return C.round_text(float(v), 6).rstrip("0").rstrip(".") if v.q != 1 else str(int(v))


@reg
def odds(chk, text):
    g = math.gcd(chk["f"], chk["u"])
    return str(text).strip() == f"{chk['f'] // g} : {chk['u'] // g}"


@reg
def draw2(chk, text):
    from itertools import product, permutations
    balls = [c for c, n in enumerate(chk["ns"]) for _ in range(n)]
    tot = len(balls)
    if chk["repl"]:
        fav = sum(1 for a in balls for b in balls if a == chk["i"] and b == chk["j"])
        allc = tot * tot
    else:
        fav = sum(1 for ia, a in enumerate(balls) for ib, b in enumerate(balls) if ia != ib and a == chk["i"] and b == chk["j"])
        allc = tot * (tot - 1)
    return _num_eq(P(text), sp.Rational(fav, allc))


@reg
def game(chk, text):
    E = sum(a * sp.Rational(p_) for a, p_ in chk["prizes"]) - chk["cost"]
    t = str(text).strip()
    if chk["ask"] == "decide":
        return t == ("No, the expected value is negative" if E < 0 else "Yes, the expected value is nonnegative" if E > 0 else "It is a fair game")
    neg = t.startswith("-")
    t2 = t.lstrip("-").lstrip("$")
    return _num_eq(P(t2) * (-1 if neg else 1), E)


def _median(d):
    d = sorted(d)
    n = len(d)
    return sp.Rational(d[(n - 1) // 2] + d[n // 2], 2)


@reg
def median(chk, text):
    return _num_eq(P(text), _median(chk["data"]))


@reg
def iqr(chk, text):
    d = sorted(chk["data"])
    n = len(d)
    lo, hi = d[: n // 2], d[(n + 1) // 2:]
    return _num_eq(P(text), _median(hi) - _median(lo))


@reg
def fence(chk, text):
    d = sorted(chk["data"])
    n = len(d)
    lo, hi = d[: n // 2], d[(n + 1) // 2:]
    q1, q3 = _median(lo), _median(hi)
    f = q3 + sp.Rational(3, 2) * (q3 - q1)
    outs = [v for v in d if v > f]
    m = re.fullmatch(r"fence = ([\d.]+); outlier (\d+)", str(text).strip())
    return bool(m) and _num_eq(P(m.group(1)), f) and outs == [int(m.group(2))]


@reg
def empirical(chk, text):
    band = {1: sp.Rational(34), 2: sp.Rational(27, 2), 3: sp.Rational(47, 20)}   # percent in each 1-SD band from the mean
    def cum(k):  # percent from mean to k SD (signed)
        s = sum(band[j] for j in range(1, abs(k) + 1))
        return s if k >= 0 else -s
    want = cum(chk["k2"]) - cum(chk["k1"])
    t = str(text).strip().rstrip("%")
    return _num_eq(P(t), want)


@reg
def binom_ms(chk, text):
    n, p = chk["n"], sp.Rational(chk["p"])
    m = re.fullmatch(r"mean = ([\d.]+); SD ≈ ([\d.]+)", str(text).strip())
    return bool(m) and _num_eq(P(m.group(1)), n * p) and m.group(2) == C.round_text(float(sp.sqrt(n * p * (1 - p))), 2)


@reg
def meanmed(chk, text):
    d = sorted(chk["data"])
    mean = sp.Rational(sum(d), len(d))
    med = _median(d)
    m = re.fullmatch(r"mean = (-?[\d.]+); median = (-?[\d.]+); the (mean|median) \(the data are (skewed right|skewed left|symmetric)\)", str(text).strip())
    if not m:
        return False
    shape = "skewed right" if mean > med else "skewed left" if mean < med else "symmetric"
    best = "median" if shape != "symmetric" else "mean"
    return _num_eq(P(m.group(1)), mean) and _num_eq(P(m.group(2)), med) and m.group(3) == best and m.group(4) == shape


def _pos_eq(a, b):
    fs = sorted((a.free_symbols | b.free_symbols), key=str)
    for p in (0.37, 1.13, 2.29, 3.7, 5.3):
        sub = {s_: sp.Float(p + 0.41 * j) for j, s_ in enumerate(fs)}
        va, vb = complex(sp.N(a.subs(sub), 30)), complex(sp.N(b.subs(sub), 30))
        if abs(va - vb) > 1e-9 * max(1, abs(va)):
            return False
    return True


def _mul_count(e):
    n = 0
    for f in sp.Mul.make_args(e):
        if f.is_number:
            continue
        if f.is_Pow and f.exp.is_Integer and f.exp > 0:
            n += int(f.exp)
        else:
            n += 1
    return n


@reg
def factored(chk, text):
    e = P(chk["expr"])
    g = P(text)
    return _num_eq(g, e) and _mul_count(g) == _mul_count(sp.factor(e)) and _mul_count(g) > 1


@reg
def simp_rat(chk, text):
    m = re.fullmatch(r"(.+), x ≠ (-?\d+)", str(text).strip())
    if not m:
        return False
    want = sp.cancel(P(chk["num"]) / P(chk["den"]))
    return _num_eq(P(m.group(1)), want) and int(m.group(2)) == chk["a"] and sp.cancel(P(m.group(1)) - want) == 0


@reg
def log_expand(chk, text):
    a = P(chk.get("rev") or chk["src"])
    return _pos_eq(P(text), a)


@reg
def exact_approx(chk, text):
    m = re.fullmatch(r"x = (.+) ≈ (-?[\d.]+)", str(text).strip())
    if not m:
        return False
    want = eval(chk["code"], ns())
    return _num_eq(P(m.group(1)), want) and m.group(2) == C.round_text(float(sp.N(want, 30)), chk["places"])


def _lim_word(v):
    return "∞" if v == sp.oo else "-∞" if v == -sp.oo else v


def _ans_eq(text, v):
    t = str(text).strip()
    if t == "does not exist":
        return v is None
    if v is None:
        return False
    return _num_eq(P(t), v)


@reg
def pw_lim(chk, text):
    a = chk["a"]
    lv = chk["l"][0] * a + chk["l"][1]
    rv = chk["r"][0] * a + chk["r"][1]
    want = {"left": lv, "right": rv, "two": lv if lv == rv else None, "value": chk["fa"]}[chk["ask"]]
    return _ans_eq(text, sp.Integer(want) if want is not None else None)


@reg
def pw_formula(chk, text):
    a = chk["a"]
    lv = sp.limit(P(chk["f1"]), X, a, "-")
    rv = sp.limit(P(chk["f2"]), X, a, "+")
    want = {"left": lv, "right": rv, "two": lv if lv == rv else None}[chk["ask"]]
    return _ans_eq(text, want)


@reg
def va_check(chk, text):
    f = P(chk["f"])
    t = str(text).strip()
    if chk["ans_kind"] == "va":
        m = re.fullmatch(r"x = (-?\d+)", t)
        if not m:
            return False
        a = int(m.group(1))
        return sp.limit(f, X, a, "+") in (sp.oo, -sp.oo)
    m = re.fullmatch(r"y = (.+)", t)
    return bool(m) and _num_eq(P(m.group(1)), sp.limit(f, X, sp.oo)) and _num_eq(P(m.group(1)), sp.limit(f, X, -sp.oo))


@reg
def cont_check(chk, text):
    a = chk["a"]
    lv, rv = sp.limit(P(chk["f1"]), X, a, "-"), sp.limit(P(chk["f2"]), X, a, "+")
    ok = lv == rv == sp.sympify(chk["fa"])
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def disc_type(chk, text):
    f = P(chk["f"])
    a = chk["a"]
    lv, rv = sp.limit(f, X, a, "-"), sp.limit(f, X, a, "+")
    if any(v in (sp.oo, -sp.oo) for v in (lv, rv)):
        t = "infinite"
    elif lv != rv:
        t = "jump"
    else:
        t = "removable"   # f(a) undefined in every item of this family
    return str(text).strip() == t


@reg
def ivt_count(chk, text):
    xs, ys, k = chk["xs"], chk["ys"], chk["k"]
    n = sum(1 for i in range(len(xs) - 1) if (ys[i] - k) * (ys[i + 1] - k) < 0)
    return str(text).strip() == str(n)


@reg
def deflimit(chk, text):
    m = re.fullmatch(r"f\(x\) = (.+), a = (.+); value (.+)", str(text).strip())
    if not m:
        return False
    F_, a = P(m.group(1)), P(m.group(2))
    given = P(chk["expr"].replace("h", "H_SYM")).subs(sp.Symbol("H_SYM"), H_) if False else P(chk["expr"])
    L1 = sp.limit(given, H_, 0)
    # the given quotient must literally be (F(a + h) - F(a))/h: compare as functions of h
    q = (F_.subs(X, a + H_) - F_.subs(X, a)) / H_
    same = _num_eq(sp.simplify(q), sp.simplify(given))
    return same and _num_eq(P(m.group(3)), L1)


@reg
def diff_kind(chk, text):
    a = chk["a"]
    t = str(text).strip()
    if chk["pieces"]:
        l, r_ = P(chk["pieces"][0]).subs(X, a), P(chk["pieces"][1]).subs(X, a)
        kind = "not continuous, so not differentiable" if l != r_ else "?"
        return t == kind
    f = P(chk["f"])
    d = sp.diff(f, X)
    dl, dr = sp.limit(d, X, a, "-"), sp.limit(d, X, a, "+")
    if dl == dr and dl.is_finite:
        kind = "differentiable (and continuous)"
    elif dl.is_finite and dr.is_finite:
        kind = "continuous but not differentiable (corner)"
    else:
        kind = "continuous but not differentiable (cusp)"
    return t == kind


@reg
def mb(chk, text):
    m_ = re.fullmatch(r"m = (-?\d+), b = (-?\d+)", str(text).strip())
    if not m_:
        return False
    m, b = int(m_.group(1)), int(m_.group(2))
    f1 = chk["c2"] * X ** 2
    a = chk["a"]
    return f1.subs(X, a) == m * a + b and sp.diff(f1, X).subs(X, a) == m


@reg
def fp_extreme(chk, text):
    fp = chk["c"] * (X - chk["p"]) * (X - chk["q"])
    crit = [chk["p"], chk["q"]]
    want = [c for c in crit if (fp.subs(X, c - sp.Rational(1, 2)) > 0 and fp.subs(X, c + sp.Rational(1, 2)) < 0) == (chk["ask"] == "max")
            and fp.subs(X, c - sp.Rational(1, 2)) * fp.subs(X, c + sp.Rational(1, 2)) < 0]
    return str(text).strip() in [f"x = {c}" for c in want] and len(want) == 1


@reg
def value_units(chk, text):
    t = str(text).strip()
    if not t.endswith(" " + chk["unit"]):
        return False
    return _num_eq(P(t[: -len(chk["unit"])].strip()), eval(chk["code"], ns()))


@reg
def classify_crit(chk, text):
    f = P(chk["f"])
    a = chk["a"]
    d = sp.diff(f, X)
    l, r_ = d.subs(X, a - sp.Rational(1, 100)), d.subs(X, a + sp.Rational(1, 100))
    kind = "relative maximum" if l > 0 > r_ else "relative minimum" if l < 0 < r_ else "neither"
    return str(text).strip() == kind


@reg
def abs_ext(chk, text):
    f = P(chk["f"])
    a, b = chk["a"], chk["b"]
    xs = sp.symbols("xs", real=True)
    pts = {a, b} | {c for c in sp.solve(sp.diff(f, X), X) if c.is_real and a <= c <= b}
    vals = {c: f.subs(X, c) for c in pts}
    best = max(vals.values()) if chk["ask"] == "max" else min(vals.values())
    at = [c for c, v in vals.items() if v == best]
    m = re.fullmatch(r"(-?\d+) at x = (-?\d+)", str(text).strip())
    return bool(m) and len(at) == 1 and int(m.group(1)) == best and int(m.group(2)) == at[0]


def _speed(text, unit):
    t = str(text).strip()
    return P(t[: -len(unit)].strip()) if t.endswith(unit) else None


@reg
def ladder(chk, text):
    xx = sp.symbols("xx", positive=True)
    y_of_x = sp.sqrt(chk["L"] ** 2 - xx ** 2)
    dy = sp.diff(y_of_x, xx).subs(xx, chk["x"]) * chk["dx"]
    g = _speed(text, "ft/s")
    return g is not None and dy < 0 and _num_eq(g, -dy)


@reg
def cone(chk, text):
    hh = sp.symbols("hh", positive=True)
    V = sp.pi / 3 * (chk["R"] * hh / chk["H"]) ** 2 * hh
    rate = chk["dV"] / sp.diff(V, hh).subs(hh, chk["h"])
    g = _speed(text, "ft/min")
    return g is not None and _num_eq(g, rate)


@reg
def shadow(chk, text):
    xx, ss = sp.symbols("xx ss", positive=True)
    s_of_x = sp.solve(sp.Eq(chk["H"] / (xx + ss), chk["h"] / ss), ss)[0]
    rate = sp.diff(s_of_x, xx) * chk["v"]
    g = _speed(text, "ft/s")
    return g is not None and _num_eq(g, rate)


@reg
def opt(chk, text):
    k = chk["k"]
    t = str(text).strip()
    xx = sp.symbols("xx", positive=True)
    def crit_best(f, lo=0, hi=None, mode="max"):
        cs = [c for c in sp.solve(sp.diff(f, xx), xx) if c.is_real and c > lo and (hi is None or c < hi)]
        vals = [(f.subs(xx, c), c) for c in cs]
        return (max if mode == "max" else min)(vals, key=lambda p: p[0])
    if k == "fence":
        v, _ = crit_best(xx * (sp.Rational(chk["P"], 2) - xx), 0, sp.Rational(chk["P"], 2))
        return t == f"{v} m²"
    if k == "product":
        v, _ = crit_best(xx * (chk["S"] - xx), 0, chk["S"])
        return t == str(v)
    if k == "sum_sq":
        v, _ = crit_best(xx ** 2 + (chk["S"] - xx) ** 2, 0, chk["S"], "min")
        return t == str(v)
    if k == "river":
        v, _ = crit_best(2 * xx + chk["A"] / xx, 0, None, "min")
        g = _speed(t, "ft")
        return g is not None and _num_eq(g, v)
    if k == "box":
        v, c = crit_best(xx * (chk["S"] - 2 * xx) ** 2, 0, sp.Rational(chk["S"], 2))
        m = re.fullmatch(r"x = (.+) in; V = (.+) in³", t)
        return bool(m) and _num_eq(P(m.group(1)), c) and _num_eq(P(m.group(2)), v)
    if k == "can":
        _, c = crit_best(2 * sp.pi * xx ** 2 + 2 * chk["V"] * sp.pi / xx, 0, None, "min")
        g = _speed(t, "in")
        return g is not None and _num_eq(g, c)
    raise ValueError(k)


@reg
def closest(chk, text):
    xx = sp.symbols("xx", positive=True)
    D2 = (xx - chk["a"]) ** 2 + xx
    c = [v for v in sp.solve(sp.diff(D2, xx), xx) if v > 0][0]
    got = P_tuple(str(text).strip())
    return len(got) == 2 and _num_eq(got[0], c) and _num_eq(got[1], sp.sqrt(c))


@reg
def motion_int(chk, text):
    s = P(chk["s"])
    v = sp.diff(s, Tt)
    a = sp.diff(v, Tt)
    dom = sp.Interval(0, sp.oo)
    if chk["ask"] == "left":
        want = sp.solve_univariate_inequality(v < 0, Tt, relational=False).intersect(dom)
    else:
        want = sp.Union(sp.solve_univariate_inequality(v * a > 0, Tt, relational=False)).intersect(dom)
    try:
        got = P_interval(text)
    except Exception:
        return False
    return sp.simplify(got.symmetric_difference(want)).measure == 0 and got == want.intersect(sp.Interval.open(0, sp.oo)) or got == want


@reg
def marginal(chk, text):
    v = sp.diff(P(chk["R"]), X).subs(X, chk["q"])
    m = re.fullmatch(r"(-?[\d/.]+) dollars per item; revenue is (increasing|decreasing)", str(text).strip())
    return bool(m) and _num_eq(P(m.group(1)), v) and m.group(2) == ("increasing" if v > 0 else "decreasing")


@reg
def mvt(chk, text):
    f = P(chk["f"])
    a, b = chk["a"], chk["b"]
    ms = (f.subs(X, b) - f.subs(X, a)) / (b - a)
    cs = [c for c in sp.solve(sp.diff(f, X) - ms, X) if c.is_real and a < c < b]
    m = re.fullmatch(r"c = (.+)", str(text).strip())
    return bool(m) and len(cs) == 1 and _num_eq(P(m.group(1)), cs[0])


@reg
def particular(chk, text):
    f = P(chk["f"])
    g = P(text)
    return _num_eq(sp.diff(g, X), f) and _num_eq(g.subs(X, chk["a"]), chk["b"])


@reg
def is_anti(chk, text):
    return _num_eq(sp.diff(P(text), X), P(chk["f"]))


@reg
def riemann(chk, text):
    f = P(chk["f"])
    a, b, n = sp.Rational(chk["a"]), sp.Rational(chk["b"]), chk["n"]
    dx = (b - a) / n
    off = {"left": 0, "right": 1, "mid": sp.Rational(1, 2)}[chk["how"]]
    v = sp.Add(*[f.subs(X, a + (i + off) * dx) for i in range(n)]) * dx
    return _num_eq(P(text), v)


@reg
def riemann_int(chk, text):
    m = re.fullmatch(r"∫ from (-?\d+) to (-?\d+) (.+) dx", str(text).strip())
    if not m:
        return False
    g = P(chk["f"])
    a, w = chk["a"], chk["w"]
    gf = sp.lambdify(X, g, "math")
    n = 200000
    S = sum(gf(a + w * k / n) for k in range(1, n + 1)) * w / n   # right Riemann sum with a large n
    got = float(sp.N(sp.integrate(P(m.group(3)), (X, int(m.group(1)), int(m.group(2)))), 30))
    return abs(got - S) < 1e-3 * max(1, abs(S)) and int(m.group(1)) == a and int(m.group(2)) == a + w and _num_eq(P(m.group(3)), g)


@reg
def table_sum(chk, text):
    xs, ys = chk["xs"], chk["ys"]
    tot = 0
    for i in range(len(xs) - 1):
        wdt = xs[i + 1] - xs[i]
        tot += {"trap": sp.Rational(ys[i] + ys[i + 1], 2), "left": ys[i], "right": ys[i + 1]}[chk["how"]] * wdt
    return _num_eq(P(text), tot)


@reg
def pl_integral(chk, text):
    pts = chk["pts"]
    fpw = sp.Piecewise(*[((y0 + sp.Rational(y1 - y0, x1 - x0) * (X - x0)), X <= x1) for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:])])
    return _num_eq(P(text), sp.integrate(fpw, (X, chk["a"], chk["b"])))


@reg
def int_props(chk, text):
    # model f and g as concrete functions with the given integrals, then integrate the asked expression
    a, b, c = chk["a"], chk["b"], chk["c"]
    f = sp.Piecewise((sp.Rational(chk["A"], b - a), X < b), (sp.Rational(chk["B"], c - b), True))
    g = sp.Integer(chk["G"]) / (b - a)
    q = chk["q"]
    m = re.fullmatch(r"∫ from (-?\d+) to (-?\d+) (.+) dx", q)
    lo, hi, body = int(m.group(1)), int(m.group(2)), m.group(3)
    body = body.replace("f(x)", "FF").replace("g(x)", "GG")
    FF, GG = sp.symbols("FF GG")
    e = parse_expr(body.replace("·", "*"), local_dict={"FF": FF, "GG": GG}, transformations=TR)
    val = sp.integrate(e.subs({FF: f, GG: g}), (X, lo, hi))
    return _num_eq(P(text), val)


@reg
def ftc_net(chk, text):
    return _num_eq(P(text), chk["fb"] - chk["fa"])


@reg
def ftc_net2(chk, text):
    return _num_eq(P(text), chk["fa"] + chk["I"])


@reg
def ftc1(chk, text):
    g = P(chk["g"].replace("t", "x"))
    s_ = sp.Symbol("s_", real=True)
    G = sp.Integral(g.subs(X, s_), (s_, chk["a"], X))
    return _num_eq(P(text), sp.diff(G, X).doit()) if "∫" not in str(text) else False


def _pl(pts):
    return sp.Piecewise(*[((y0 + sp.Rational(y1 - y0, x1 - x0) * (X - x0)), X <= x1) for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:])])


@reg
def pl_value(chk, text):
    return _num_eq(P(text), _pl(chk["pts"]).subs(X, chk["at"]))


def _pl_sign_intervals(pts, sgn):
    """Independent: sample-free exact construction from each segment's linear formula."""
    pieces = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        lin = y0 + sp.Rational(y1 - y0, x1 - x0) * (X - x0)
        sol = sp.solveset(sgn * lin > 0, X, sp.Interval.open(x0, x1))
        pieces.append(sol)
    out = sp.Union(*pieces)
    for (xv, yv) in pts[1:-1]:
        if sgn * yv > 0:
            out = sp.Union(out, sp.FiniteSet(xv))
    return out


@reg
def g_inc(chk, text):
    want = _pl_sign_intervals(chk["pts"], 1)
    try:
        return P_interval(text) == want
    except Exception:
        return False


@reg
def g_max(chk, text):
    pts = chk["pts"]
    pos, neg = _pl_sign_intervals(pts, 1), _pl_sign_intervals(pts, -1)
    cands = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        lin = y0 + sp.Rational(y1 - y0, x1 - x0) * (X - x0)
        for z in sp.solveset(lin, X, sp.Interval(x0, x1)):
            e = sp.Rational(1, 1000)
            if -4 < z < 4 and pos.contains(z - e) == True and neg.contains(z + e) == True and z not in cands:
                cands.append(z)
    m = re.fullmatch(r"x = (.+)", str(text).strip())
    return bool(m) and len(cands) == 1 and _num_eq(P(m.group(1)), cands[0])


@reg
def area_between(chk, text):
    f, g = P(chk["f"]), P(chk["g"])
    xs = sorted(z for z in sp.solve(f - g, X) if z.is_real)
    tot = sum(abs(sp.integrate(f - g, (X, xs[i], xs[i + 1]))) for i in range(len(xs) - 1))
    return _num_eq(P(strip_units(text)), tot)


_YP, _YPP, _CC = sp.symbols("YP YPP C")
_yf = sp.Function("yf")


def _de_parse(de):
    """'xy′ = 2y' → expression E(x, y, YP, YPP) that must vanish."""
    s = de.replace("y″", " YPP ").replace("y′", " YP ").replace("T′", " YP ").replace("P′", " YP ")
    l, r_ = s.split("=")
    loc = dict(LOC)
    loc.update({"YP": _YP, "YPP": _YPP})
    def one(t):
        t = t.strip().replace("−", "-").replace("·", "*")
        t = _roots(_bars(t))
        t = re.sub("[⁰¹²³⁴⁵⁶⁷⁸⁹⁻ˣʸ]+", lambda m: "**(" + "".join({"ˣ": "x", "ʸ": "y"}.get(c, SUP.get(c, c)) for c in m.group(0)) + ")", t)
        t = t.replace("^", "**")
        t = re.sub(r"(?<![A-Za-z])e\*\*", "E**", t)
        return parse_expr(t, local_dict=loc, transformations=TR)
    return one(l) - one(r_)


def _residual(de, yexpr):
    E = _de_parse(de)
    return sp.simplify(E.subs({_YPP: sp.diff(yexpr, X, 2), _YP: sp.diff(yexpr, X)}).subs(Y, yexpr))


def _y_of(text):
    t = str(text).strip()
    m = re.fullmatch(r"y = (.+)", t)
    if not m:
        return None
    loc = dict(LOC); loc["C"] = _CC
    return P(m.group(1).replace("C", "(C)")).subs(sp.Symbol("C"), _CC) if "C" in m.group(1) else P(m.group(1))


@reg
def de_verify(chk, text):
    yexpr = _y_of(chk["sol"])
    ok = _residual(chk["de"], yexpr) == 0
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def de_general(chk, text):
    t = str(text).strip()
    if "C" not in t:
        return False
    if t.startswith("y = "):
        yexpr = _y_of(t)
        res = _residual(chk["de"], yexpr)
        fam_ok = sp.diff(yexpr, _CC) != 0
        return fam_ok and _num_eq(res.subs(_CC, sp.Rational(7, 3)), 0) and _num_eq(res.subs(_CC, sp.Rational(-5, 2)), 0)
    l, r_ = t.split("=")
    G = P(l) - P(r_.replace("C", "0"))   # implicit G(x, y) = C
    dydx = -sp.diff(G, X) / sp.diff(G, Y)
    E = _de_parse(chk["de"])
    yp = sp.solve(E, _YP)[0]
    return sp.simplify(dydx - yp) == 0


@reg
def de_ivp(chk, text):
    yexpr = _y_of(text)
    if yexpr is None or yexpr.has(_CC):
        return False
    return _residual(chk["de"], yexpr) == 0 and _num_eq(yexpr.subs(X, chk["x0"]), chk["y0"])


@reg
def de_ivp_val(chk, text):
    yf = sp.Function("yf")
    E = _de_parse(chk["de"]).subs({_YP: yf(X).diff(X), Y: yf(X)})
    sol = sp.dsolve(E, yf(X), ics={yf(chk["x0"]): chk["y0"]})
    v = float(sp.N(sol.rhs.subs(X, chk["at"]), 30))
    return str(text).strip() == C.round_text(v, chk["places"])


@reg
def euler(chk, text):
    f = P(chk["rhs"])
    h = sp.Rational(chk["h"])
    xv, yv = sp.Integer(chk["x0"]), sp.Integer(chk["y0"])
    for _ in range(chk["n"]):
        yv = yv + h * f.subs({X: xv, Y: yv})
        xv = xv + h
    return _num_eq(P(text), yv)


@reg
def newton(chk, text):
    yf = sp.Function("yf")
    k = sp.Rational(chk["k"])
    sol = sp.dsolve(sp.Eq(yf(Tt).diff(Tt), -k * (yf(Tt) - chk["Ta"])), yf(Tt), ics={yf(0): chk["T0"]})
    v = float(sp.N(sol.rhs.subs(Tt, chk["t"]), 30))
    return str(text).strip() == C.round_text(v, 1) + "°F"


@reg
def table_avg(chk, text):
    xs, ys = chk["xs"], chk["ys"]
    tot = sum(sp.Rational(ys[i] + ys[i + 1], 2) * (xs[i + 1] - xs[i]) for i in range(len(xs) - 1))
    return _num_eq(P(text), tot / (xs[-1] - xs[0]))


@reg
def de_k(chk, text):
    m = re.fullmatch(r"k = (-?\d+)", str(text).strip())
    if not m:
        return False
    yv = chk["c"] * sp.exp(chk["k"] * X)
    return sp.simplify(sp.diff(yv, X) - int(m.group(1)) * yv) == 0


@reg
def de_C(chk, text):
    m = re.fullmatch(r"C = (.+)", str(text).strip())
    return bool(m) and _num_eq(P(m.group(1)) * sp.exp(0), chk["y0"])
