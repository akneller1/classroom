"""Custom independent checks used by verify.py. Each CUSTOM[name](chk, text) -> bool
decides whether `text` is a correct response. These functions do not import the
authoring families; they recompute from the data shown in the prompt."""
import math, re
from fractions import Fraction as F
import mathtext as M

CUSTOM = {}


def reg(f):
    CUSTOM[f.__name__] = f
    return f


def round_text(v, places):
    q = F(repr(float(v))) if not isinstance(v, F) else v
    m = 10 ** places
    r = math.floor(abs(q) * m + F(1, 2))
    r = r if q >= 0 else -r
    if places == 0:
        return str(r)
    s = f"{abs(r):0{places + 1}d}"
    return ("-" if r < 0 else "") + s[:-places] + "." + s[-places:]


# ---------------------------------------------------------------- repeating decimals
REP = re.compile(r"^\s*(-?)(\d+)\.(\d+)…\s*\((?:the digits? )?(\d+) repeats?\)\s*$")


def rep_value(text):
    m = REP.match(str(text))
    if not m:
        return None
    sign, ip, shown, block = m.groups()
    # nonrepeating prefix: shortest p such that shown[p:] is consistent with block repeated
    for p in range(len(shown)):
        tail = shown[p:]
        if len(tail) >= len(block) and (block * (len(tail) // len(block) + 2)).startswith(tail):
            nonrep = shown[:p]
            v = F(int(ip)) + (F(int(nonrep), 10 ** p) if nonrep else 0) + F(int(block), (10 ** len(block) - 1) * 10 ** p)
            return -v if sign else v
    return None


def any_value(text):
    v = rep_value(text)
    if v is not None:
        return v
    return M.val(text)


@reg
def rep_dec(chk, text):
    """text (repeating or terminating decimal or fraction) equals value of chk['expr']."""
    try:
        return M.same(any_value(text), M.ev(chk["expr"]))
    except Exception:
        return False


@reg
def dec_text(chk, text):
    """text must be a decimal numeral (terminating or repeating notation) equal to expr."""
    t = M.strip_units(str(text).strip()) if not REP.match(str(text).strip()) else str(text).strip()
    if "/" in t:
        return False
    if not (REP.match(t) or re.fullmatch(r"-?\d+(\.\d+)?", t)):
        return False
    return rep_dec(chk, t)


@reg
def frac_text(chk, text):
    """text must be a fraction/integer in simplest form equal to expr."""
    t = M.strip_units(str(text).strip())
    m = re.fullmatch(r"(-?)(\d+)/(\d+)", t)
    if m:
        if math.gcd(int(m.group(2)), int(m.group(3))) != 1 or int(m.group(3)) == 1:
            return False
    elif not re.fullmatch(r"-?\d+", t):
        return False
    return rep_dec(chk, t)


# ---------------------------------------------------------------- symbolic a + b√n (+ π) arithmetic
def sqf(n):
    """n = k² · s with s squarefree; return (k, s)."""
    k, s, p = 1, n, 2
    while p * p <= s:
        while s % (p * p) == 0:
            s //= p * p
            k *= p
        p += 1
    return k, s


class Sym:
    """Finite sum of coefficient * basis; basis () is 1, ('r', n) is √n (n squarefree), ('c', n) ∛n, ('pi',)."""

    def __init__(self, d=None):
        self.d = {k: v for k, v in (d or {}).items() if v != 0}

    @staticmethod
    def q(x):
        return Sym({(): F(x)})

    def __add__(self, o):
        d = dict(self.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) + v
        return Sym(d)

    def __neg__(self):
        return Sym({k: -v for k, v in self.d.items()})

    def __mul__(self, o):
        out = Sym()
        for k1, v1 in self.d.items():
            for k2, v2 in o.d.items():
                out = out + Sym(_mulb(k1, k2, v1 * v2))
        return out

    def rational(self):
        return all(k == () for k in self.d)

    def value(self):
        tot = 0.0
        for k, v in self.d.items():
            tot += float(v) * _bval(k)
        return tot


def _bval(k):
    if k == ():
        return 1.0
    if k[0] == "r":
        return math.sqrt(k[1])
    if k[0] == "c":
        return k[1] ** (1 / 3)
    if k[0] == "pi":
        return math.pi * (_bval(k[1]) if len(k) > 1 else 1.0)
    raise ValueError(k)


def _mulb(a, b, c):
    if a == ():
        return {b: c}
    if b == ():
        return {a: c}
    if a[0] == "r" and b[0] == "r":
        k, s = sqf(a[1] * b[1])
        return {(() if s == 1 else ("r", s)): c * k}
    if a[0] == "pi" or b[0] == "pi":
        other = b if a[0] == "pi" else a
        if other[0] == "pi":
            return {("pi2",): c}
        return {("pi", other): c}
    return {("mix", a, b): c}


def sym_root(v, n):
    if not v.rational():
        raise ValueError("root of irrational unsupported")
    x = v.d.get((), F(0))
    if n == 2:
        if x < 0:
            raise ValueError
        p, q = x.numerator * x.denominator, x.denominator
        k, s = sqf(p)
        return Sym({(() if s == 1 else ("r", s)): F(k, q)})
    sign = -1 if x < 0 else 1
    p, q = abs(x.numerator) * x.denominator ** 2, x.denominator
    k, s, t = 1, p, 2
    while t ** 3 <= s:
        while s % (t ** 3) == 0:
            s //= t ** 3
            k *= t
        t += 1
    return Sym({(() if s == 1 else ("c", s)): F(sign * k, q)})


class SParser(M.Parser):
    def expr(self):
        v = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            w = self.term()
            v = v + w if op == "+" else v + (-w)
        return v

    def term(self):
        v = self.unary()
        while True:
            tok = self.peek()
            if tok == "*":
                self.take()
                v = v * self.unary()
            elif tok in ("/", "DIV"):
                self.take()
                w = self.unary()
                if w.rational():
                    v = v * Sym.q(1 / w.d[()])
                elif len(w.d) == 1 and list(w.d)[0][0] == "r":
                    (k, c), = w.d.items()
                    v = v * Sym({k: F(1, k[1]) / c})
                else:
                    raise ValueError("division unsupported")
            elif self.starts_primary(tok):
                v = v * self.pw()
            else:
                return v

    def unary(self):
        if self.peek() == "-":
            self.take()
            return -self.unary()
        return self.pw()

    def starts_primary(self, tok):
        return tok is not None and tok not in ("DIV", "/") and (tok[0].isdigit() or tok[0] == "." or tok.isalpha() or tok in ("(", "√", "∛", "π", "["))

    def pw(self):
        b = self.primary()
        if self.peek() == "^":
            self.take()
            neg = False
            while self.peek() in ("-", "+"):
                neg ^= self.take() == "-"
            e = self.pw()
            e = -e if neg else e
            assert e.rational() and e.d.get((), F(0)).denominator == 1
            n = int(e.d.get((), 0))
            out = Sym.q(1)
            if n < 0:
                assert b.rational()
                return Sym.q(b.d[()] ** n)
            for _ in range(n):
                out = out * b
            return out
        return b

    def primary(self):
        tok = self.take()
        if tok in ("(", "["):
            v = self.expr()
            self.take(")" if tok == "(" else "]")
            return v
        if tok == "√":
            return sym_root(self.pw(), 2)
        if tok == "∛":
            return sym_root(self.pw(), 3)
        if tok == "π":
            return Sym({("pi",): F(1)})
        if tok[0].isdigit() or tok[0] == ".":
            return Sym.q(F(tok))
        raise ValueError("unexpected " + str(tok))


NONREP = re.compile(r"^\s*-?\d+\.\d+…\s*\((?:the )?pattern (?:continues but )?never repeats\)\s*$")


def sym(text):
    """Symbolic value of a number written in the bank's notation. Returns ('q', Fraction) or ('irr', float)."""
    t = str(text).strip()
    rv = rep_value(t)
    if rv is not None:
        return ("q", rv)
    if NONREP.match(t):
        return ("irr", float(re.match(r"\s*(-?\d+\.\d+)", t).group(1)))
    p = SParser(M.tokenize(t), {})
    v = p.expr()
    if p.peek() is not None:
        raise ValueError("trailing")
    if v.rational():
        return ("q", v.d.get((), F(0)))
    return ("irr", v.value())


def num_value(text):
    k, v = sym(text)
    return float(v)


@reg
def is_rational(chk, text):
    return sym(text)[0] == "q"


@reg
def is_irrational(chk, text):
    return sym(text)[0] == "irr"


@reg
def rat_or_irr(chk, text):
    t = str(text).strip().lower()
    want = "rational" if sym(chk["num"])[0] == "q" else "irrational"
    return t == want


@reg
def classify(chk, text):
    """Most specific set among natural, whole, integer, rational, irrational."""
    k, v = sym(chk["num"])
    if k == "irr":
        want = "irrational number"
    elif v.denominator != 1:
        want = "rational number"
    elif v > 0:
        want = "natural number"
    elif v == 0:
        want = "whole number"
    else:
        want = "integer"
    return str(text).strip().lower() == want


@reg
def between_ints(chk, text):
    m = re.match(r"^\s*(-?\d+)\s+and\s+(-?\d+)\s*$", str(text))
    if not m:
        return False
    a, b = int(m.group(1)), int(m.group(2))
    v = num_value(chk["num"])
    return b == a + 1 and a < v < b


@reg
def strictly_between(chk, text):
    lo, hi = num_value(chk["lo"]), num_value(chk["hi"])
    v = num_value(text)
    ok = lo < v < hi
    if chk.get("irrational"):
        ok = ok and sym(text)[0] == "irr"
    return ok


def split_list(text):
    return [s.strip() for s in re.split(r",\s+(?![^()]*\))", str(text))]


@reg
def order(chk, text):
    """text lists exactly the given numbers in ascending (or descending) order."""
    items = split_list(text)
    given = chk["items"]
    if sorted(items) != sorted(given):
        return False
    vals = [num_value(s) for s in items]
    if chk.get("desc"):
        return all(a > b for a, b in zip(vals, vals[1:]))
    return all(a < b for a, b in zip(vals, vals[1:]))


@reg
def extreme(chk, text):
    """text is the greatest (or least) of chk['items']."""
    vals = {s: num_value(s) for s in chk["items"]}
    if str(text) not in vals:
        return False
    target = max(vals.values()) if chk.get("max", True) else min(vals.values())
    return abs(vals[str(text)] - target) < 1e-12 and sum(1 for v in vals.values() if abs(v - target) < 1e-12) == 1


@reg
def terminates(chk, text):
    k, v = sym(text)
    if k != "q":
        return False
    d = v.denominator
    for p in (2, 5):
        while d % p == 0:
            d //= p
    return (d == 1) == chk.get("want", True)


@reg
def predicate(chk, text):
    """Generic numeric predicate on the value of text: chk['op'] in lt, gt, le, ge with chk['than'] text."""
    v, w = num_value(text), num_value(chk["than"])
    return {"lt": v < w, "gt": v > w, "le": v <= w, "ge": v >= w}[chk["op"]]


@reg
def pm_sol(chk, text):
    """Solutions of x^n = c: text like 'x = 9 or x = -9', 'x = ±√7' or 'x = 4'."""
    n, c = chk["n"], M.ev(chk["c"])
    t = str(text).replace("−", "-")
    sols = []
    for part in re.split(r"\s+or\s+", t):
        part = M.strip_lhs(part)
        if part.startswith("±"):
            v = M.ev(part[1:])
            sols += [v, -v if M.is_exact(v) else -float(v)]
        else:
            sols.append(M.ev(part))
    real = []
    if n % 2 == 0:
        r = M.root(F(c), 2) if n == 2 else float(c) ** (1 / n)
        real = [r, -r if M.is_exact(r) else -float(r)] if c > 0 else ([F(0)] if c == 0 else [])
    else:
        real = [M.root(F(c), 3)]
    if len(sols) != len(real):
        return False
    used = [False] * len(real)
    for s in sols:
        hit = [i for i, r in enumerate(real) if not used[i] and M.same(s, r)]
        if not hit:
            return False
        used[hit[0]] = True
    return True


SCI = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*×\s*10([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)\s*$")


def sci_parts(text):
    m = SCI.match(M.strip_units(str(text)))
    if not m:
        return None
    e = int("".join(M.SUP2[c] for c in m.group(2)))
    return F(m.group(1)), e


@reg
def sci_form(chk, text):
    """text is in scientific notation (1 <= |m| < 10) and equals expr."""
    p = sci_parts(text)
    if not p:
        return False
    m, e = p
    if not (1 <= abs(m) < 10):
        return False
    return M.same(m * F(10) ** e, M.ev(chk["expr"]))


@reg
def sci_or_std(chk, text):
    """Accept standard or scientific form equal to expr (scientific must be normalised)."""
    p = sci_parts(text)
    if p:
        return sci_form(chk, text)
    try:
        return M.same(M.val(text), M.ev(chk["expr"]))
    except Exception:
        return False


@reg
def single_digit_est(chk, text):
    """text is d × 10^e with single nonzero digit d nearest to the value (rounded to 1 significant figure)."""
    p = sci_parts(text)
    if not p:
        return False
    m, e = p
    v = M.ev(chk["expr"])
    if m.denominator != 1 or not (1 <= m <= 9):
        return False
    e0 = math.floor(math.log10(float(v)))
    lead = F(v) / F(10) ** e0
    d = math.floor(lead + F(1, 2))
    if d == 10:
        d, e0 = 1, e0 + 1
    return m == d and e == e0


@reg
def exp_solve(chk, text):
    """n such that base^n = target (integer n)."""
    try:
        n = int(M.strip_lhs(text))
    except ValueError:
        return False
    return M.same(M.power(M.ev(chk["base"]), F(n)), M.ev(chk["target"]))


@reg
def missing_exp(chk, text):
    """Integer k so that the expression template (with K replaced by k) is equivalent to target."""
    try:
        k = int(M.strip_lhs(text).replace("−", "-"))
    except ValueError:
        return False
    vs = chk.get("vars", ["x"])
    expr = chk["template"].replace("K", f"({k})")
    for p in (2, 3, 5):
        env = {v: F(p + j, 1 + j) for j, v in enumerate(vs)}
        if not M.same(M.ev(expr, env), M.ev(chk["target"], env)):
            return False
    return True


@reg
def pos_exp_equiv(chk, text):
    """Equivalent to expr AND written without negative or zero exponents."""
    t = str(text)
    if "⁻" in t or "⁰" in t or "^-" in t:
        return False
    vs = chk.get("vars", ["x"])
    try:
        for p in (2, 3, 7):
            env = {v: F(p + j, 1 + 2 * j) for j, v in enumerate(vs)}
            if not M.same(M.ev(M.strip_lhs(t), env), M.ev(chk["expr"], env)):
                return False
        return True
    except Exception:
        return False


@reg
def sign_of(chk, text):
    v = M.ev(chk["expr"])
    want = "positive" if v > 0 else "negative" if v < 0 else "zero"
    return str(text).strip().lower() == want


@reg
def count_irr(chk, text):
    try:
        return int(text) == sum(1 for x in chk["items"] if sym(x)[0] == "irr")
    except ValueError:
        return False


@reg
def square_side_irr(chk, text):
    m = re.match(r"A square with (area|perimeter) (\d+)", str(text))
    a = int(m.group(2))
    side = sym(f"√{a}") if m.group(1) == "area" else ("q", F(a, 4))
    return side[0] == "irr"


@reg
def irr_counterexample(chk, text):
    """Both operands irrational and the result rational."""
    t = str(text)
    if chk["op"] == "product":
        parts = [p.strip() for p in t.split("·")]
        if len(parts) != 2:
            return False
    else:
        m = re.match(r"^\((.+)\) \+ \((.+)\)$", t)
        parts = [m.group(1), m.group(2)] if m else re.split(r"\s\+\s", t, maxsplit=1)
        if len(parts) != 2:
            return False
    try:
        return all(sym(p)[0] == "irr" for p in parts) and sym(t)[0] == "q"
    except Exception:
        return False


@reg
def value_and_type(chk, text):
    m = re.match(r"^x = (.+), (rational|irrational)$", str(text))
    if not m:
        return False
    try:
        val_ok = abs(num_value(m.group(1)) - num_value(chk["expr"])) < 1e-9
        kind = sym(m.group(1))[0]
    except Exception:
        return False
    return val_ok and ((kind == "q") == (m.group(2) == "rational"))


@reg
def count_whole_between(chk, text):
    lo, hi = math.sqrt(chk["a"]), math.sqrt(chk["b"])
    return str(text).strip() == str(sum(1 for k in range(0, 1000) if lo < k < hi))


@reg
def greatest_n_sqrt_lt(chk, text):
    t = F(chk["t"])
    n = int(text)
    return n * n >= 0 and F(n) < t * t and not F(n + 1) < t * t


@reg
def closer_int(chk, text):
    s = math.sqrt(chk["n"])
    lo = math.floor(s)
    want = lo if s - lo < lo + 1 - s else lo + 1
    return str(text).strip() == str(want)


@reg
def numline_point(chk, text):
    m = re.match(r"Point ([A-D])$", str(text))
    s = math.sqrt(chk["n"])
    best = min(chk["pts"].items(), key=lambda kv: abs(kv[1] - s))[0]
    return bool(m) and m.group(1) == best and abs(chk["pts"][best] - s) < 0.02


@reg
def sqrt_rounds_to(chk, text):
    return round_text(math.sqrt(int(text)), 1) == chk["t"]


@reg
def power_form(chk, text):
    """text is base^(integer) with the requested base and equals expr."""
    t = str(text).strip()
    m = re.match(r"^(\(1/\d+\)|\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)$", t)
    if not m:
        return False
    if m.group(1).strip("()") != chk["base"]:
        return False
    return M.same(M.ev(t), M.ev(chk["expr"]))


@reg
def is_sci_notation(chk, text):
    p = sci_parts(text)
    return bool(p) and 1 <= abs(p[0]) < 10


@reg
def letter_greater(chk, text):
    a, b = M.ev(chk["A"]), M.ev(chk["B"])
    return str(text).strip() == ("A" if a > b else "B")


# ---------------------------------------------------------------- equations
def sol_set(eq, var="x"):
    return M.solve_linear(eq, var)


@reg
def err_steps(chk, text):
    """Steps: list of equations. First error = first step whose solution set differs from the previous step's."""
    var = chk.get("var", "x")
    seq = [chk["orig"]] + chk["steps"]
    sets = []
    for e in seq:
        s = sol_set(e.split(":", 1)[-1].strip() if e.startswith("Step") else e, var)
        sets.append(s)

    def same_set(a, b):
        return a[0] == b[0] and (a[0] != "one" or M.same(a[1], b[1]))
    first = next((i for i in range(1, len(sets)) if not same_set(sets[i - 1], sets[i])), None)
    t = str(text).strip()
    if t.lower().startswith("there is no error"):
        return first is None
    m = re.match(r"^Step (\d+)$", t)
    return bool(m) and first is not None and int(m.group(1)) == first


@reg
def model_eq(chk, text):
    """text is a linear equation in chk['var'] whose unique solution equals the value of chk['expr']."""
    var = chk.get("var", "x")
    t = str(text)
    if t.count("=") != 1 or not re.search(r"(?<![A-Za-z])" + var + r"(?![A-Za-z])", t):
        return False
    try:
        s = M.solve_linear(t, var)
    except Exception:
        return False
    return s[0] == "one" and M.same(s[1], M.ev(chk["expr"]))


@reg
def num_solutions(chk, text):
    s = M.solve_linear(chk["eq"], chk.get("var", "x"))
    want = {"one": "one solution", "none": "no solution", "all": "infinitely many solutions"}[s[0]]
    return str(text).strip().lower() == want


@reg
def param_value(chk, text):
    """Value of parameter (replacing 'K' in chk['eq']) that gives the requested solution type."""
    try:
        k = M.val(text)
    except Exception:
        return False
    eq = chk["eq"].replace("K", f"({M.F(k) if M.is_exact(k) else k})")
    try:
        s = M.solve_linear(eq, chk.get("var", "x"))
    except Exception:
        return False
    return s[0] == chk["want"]


class _Fn:
    def __init__(self, expr, var):
        self.toks = M.tokenize(expr)
        self.var = var

    def __call__(self, x):
        p = M.Parser(self.toks, {self.var: x})
        return p.expr()


def scan_roots(eq, var, lo=-40.0, hi=40.0, step=0.01):
    l, r = M.eq_sides(eq)
    fl, fr = _Fn(l, var), _Fn(r, var)

    def f(x):
        try:
            return float(fl(x)) - float(fr(x))
        except (ZeroDivisionError, ValueError, OverflowError):
            return float("nan")
    roots = []
    n = int((hi - lo) / step)
    prev_x, prev = lo, f(lo)
    for i in range(1, n + 1):
        x = lo + i * step
        v = f(x)
        if v == v and prev == prev:
            if v == 0 or abs(v) < 1e-10:
                roots.append(x)
            elif prev * v < 0:
                a, b = prev_x, x
                for _ in range(60):
                    m = (a + b) / 2
                    fm = f(m)
                    if (f(a) < 0) == (fm < 0):
                        a = m
                    else:
                        b = m
                roots.append((a + b) / 2)
        prev_x, prev = x, v
    # tangency (double) roots: local minima of |f| close to 0
    out = []
    for x in sorted(roots):
        if not out or abs(x - out[-1]) > 1e-4:
            out.append(x)
    return out, f


@reg
def roots_match(chk, text):
    """All real solutions found by scanning equal the solutions listed in text ('x = a or x = b', 'no real solution')."""
    var = chk.get("var", "x")
    roots, f = scan_roots(chk["eq"], var, chk.get("lo", -40.0), chk.get("hi", 40.0))
    for extra in chk.get("tangent", []):   # double roots supplied for re-checking by substitution
        if abs(f(float(M.ev(extra)))) < 1e-9 and all(abs(float(M.ev(extra)) - r) > 1e-4 for r in roots):
            roots.append(float(M.ev(extra)))
    t = str(text).replace("−", "-").strip()
    if t.lower() in ("no real solution", "no real solutions", "no solution"):
        return not roots
    vals = []
    for part in re.split(r"\s+or\s+", t):
        part = M.strip_lhs(part.strip())
        if part.startswith("±"):
            v = float(M.ev(part[1:]))
            vals += [v, -v]
        else:
            vals.append(float(M.ev(part)))
    if len(vals) != len(roots):
        return False
    return all(any(abs(v - r) < 1e-6 for r in roots) for v in vals) and all(abs(f(v)) < 1e-7 for v in vals)


@reg
def sqrt_reverse(chk, text):
    try:
        v = M.val(text)
    except Exception:
        return False
    return M.same(M.root(F(v), chk["index"]) if (chk["index"] == 3 or v >= 0) else -1, F(chk["k"]))


@reg
def sqrt_sq_ne(chk, text):
    x = M.val(text)
    return not M.same(M.root(F(x) * F(x), 2), x)


@reg
def power_and_value(chk, text):
    m = re.match(r"^(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+) = (-?[\d,]+(?:/\d+)?)$", str(text).strip())
    if not m or m.group(1) != chk["base"]:
        return False
    v = M.ev(chk["expr"])
    return M.same(M.ev(m.group(1) + m.group(2)), v) and M.same(M.ev(m.group(3)), v)


@reg
def k_makes_solution(chk, text):
    try:
        k = M.val(text)
    except Exception:
        return False
    x = M.ev(chk["x"])
    l, r = M.eq_sides(chk["eq"])
    return M.same(M.ev(l, {"x": x}), M.ev(r.replace("k", f"({k})"), {"x": x}))


def _eqv(e1, e2, var="x"):
    a, b = M.solve_linear(e1, var), M.solve_linear(e2, var)
    return a[0] == b[0] and (a[0] != "one" or M.same(a[1], b[1]))


@reg
def same_solution(chk, text):
    try:
        return _eqv(chk["eq"], str(text), chk.get("var", "x"))
    except Exception:
        return False


@reg
def x_and_longest(chk, text):
    m = re.match(r"^x = (-?\d+); longest side (\d+) cm$", str(text))
    if not m:
        return False
    s = M.solve_linear(chk["eq"])
    if s[0] != "one" or not M.same(s[1], M.ev(m.group(1))):
        return False
    lengths = [M.ev(t, {"x": s[1]}) for t in chk["sides"]]
    return M.same(max(lengths), M.ev(m.group(2)))


@reg
def completes_type(chk, text):
    s = M.solve_linear(f"{chk['left']} = {text}")
    return s[0] == chk["want"]


@reg
def is_type(chk, text):
    return M.solve_linear(str(text))[0] == chk["want"]


@reg
def count_real_roots(chk, text):
    roots, _ = scan_roots(chk["eq"], chk.get("var", "x"))
    try:
        return int(text) == len(roots)
    except ValueError:
        return False


@reg
def exp_eq(chk, text):
    try:
        x = M.val(text)
    except Exception:
        return False
    if not (M.is_exact(x) and x.denominator == 1):
        return False
    return M.same(M.power(M.ev(chk["base"]), x + chk["shift"]), M.ev(chk["target"]))


@reg
def has_roots(chk, text):
    """Equation text has exactly the listed real roots."""
    want = sorted(float(M.ev(t)) for t in chk["roots"])
    roots, _ = scan_roots(str(text), "x")
    return len(roots) == len(want) and all(abs(a - b) < 1e-6 for a, b in zip(sorted(roots), want))


# ---------------------------------------------------------------- functions / lines (unit 3, also used by 4)
def pairs_of(text):
    return [(M.ev(a), M.ev(b)) for a, b in re.findall(r"\(\s*([^,()]+?)\s*,\s*([^,()]+?)\s*\)", str(text))]


def is_func_pairs(pairs):
    seen = {}
    for a, b in pairs:
        if a in seen and seen[a] != b:
            return False
        seen[a] = b
    return True


@reg
def is_function_pairs(chk, text):
    want = "yes" if is_func_pairs([(F(a), F(b)) for a, b in chk["pairs"]]) else "no"
    return str(text).strip().lower() == want


@reg
def is_function_set(chk, text):
    return is_func_pairs(pairs_of(text))


@reg
def is_function_any(chk, text):
    t = str(text).strip()
    if t.startswith("{"):
        return is_func_pairs(pairs_of(t))
    if re.match(r"^x\s*=", t):
        return False
    if re.match(r"^y\s*=", t):
        return True
    raise ValueError("unknown relation " + t)


def rhs_fn(text):
    t = str(text).strip()
    m = re.match(r"^(?:[A-Za-z]|f\(x\))\s*=\s*(.+)$", t)
    body = m.group(1) if m else t
    return lambda x: M.ev(body, {"x": F(x) if not isinstance(x, float) else x})


@reg
def rule_fits(chk, text):
    if not re.match(r"^\s*(y|f\(x\))\s*=", str(text)):
        return False
    try:
        f = rhs_fn(text)
        return all(M.same(f(M.ev(a)), M.ev(b)) for a, b in chk["pts"])
    except Exception:
        return False


@reg
def domain_range(chk, text):
    vals = sorted({p[0] if chk["which"] == "domain" else p[1] for p in chk["pairs"]})
    got = [M.ev(t) for t in re.findall(r"-?\d+", str(text))]
    return got == vals and str(text).strip().startswith("{")


@reg
def vlt_choice(chk, text):
    m = re.match(r"Graph ([A-D])$", str(text))
    kinds = chk["kinds"]
    passes = [k == "line" for k in kinds]   # non-vertical line is the only graph passing the vertical line test
    return bool(m) and passes["ABCD".index(m.group(1))] and sum(passes) == 1


def eq_holds(eq, x, y):
    l, r = M.eq_sides(eq)
    env = {"x": x, "y": y}
    return M.same(M.ev(l, env), M.ev(r, env))


@reg
def on_graph(chk, text):
    x, y = M.parse_point(text)
    return eq_holds(chk["eq"], x, y)


def pw_value(pts, x):
    pts = [(F(a), F(b)) for a, b in pts]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (F(x) - x0) / (x1 - x0)
    raise ValueError("outside")


@reg
def read_value(chk, text):
    f = chk["f"]
    x = F(chk["x"])
    v = M.ev(f[1]) * x + M.ev(f[2]) if f[0] == "lin" else pw_value(f[1], x)
    try:
        return M.same(M.val(text), v)
    except Exception:
        return False


def line_eq_fn(eq):
    """Return (m, b) for an equation in x, y (non-vertical) by evaluating it."""
    l, r = M.eq_sides(eq)
    g = lambda x, y: M.ev(l, {"x": x, "y": y}) - M.ev(r, {"x": x, "y": y})
    c = g(F(0), F(0))
    a = g(F(1), F(0)) - c
    b = g(F(0), F(1)) - c
    return -a / b, -c / b


@reg
def panel_line(chk, text):
    m = re.match(r"Graph ([A-D])$", str(text))
    want = line_eq_fn(chk["eq"])
    hits = [M.same(M.ev(a), want[0]) and M.same(M.ev(b), want[1]) for a, b in chk["lines"]]
    return bool(m) and sum(hits) == 1 and hits["ABCD".index(m.group(1))]


@reg
def table_linear(chk, text):
    pts = sorted(zip([F(x) for x in chk["xs"]], [F(y) for y in chk["ys"]]))
    rates = {(b[1] - a[1]) / (b[0] - a[0]) for a, b in zip(pts, pts[1:])}
    return str(text).strip().lower() == ("linear" if len(rates) == 1 else "nonlinear")


def eq_is_linear(t):
    t = str(t)
    if re.search(r"[²³ˣʰ√]|/x|xy|\^", t):
        return False
    l, r = M.eq_sides(t)
    if "y" not in t:
        return False
    try:
        g = lambda x, y: M.ev(l, {"x": x, "y": y}) - M.ev(r, {"x": x, "y": y})
        c = g(F(0), F(0))
        a, b = g(F(1), F(0)) - c, g(F(0), F(1)) - c
        return b != 0 and all(M.same(g(F(x), F(y)), a * x + b * y + c) for x, y in [(2, 3), (5, -1), (-3, 7)])
    except Exception:
        return False


@reg
def eq_linear(chk, text):
    return eq_is_linear(text) == chk["want"]


@reg
def panel_kind(chk, text):
    m = re.match(r"Graph ([A-D])$", str(text))
    lin_ = [k == "line" or k.endswith("_l") for k in chk["kinds"]]
    want = [x if chk["want"] == "linear" else not x for x in lin_]
    return bool(m) and sum(want) == 1 and want["ABCD".index(m.group(1))]


@reg
def rule_linear(chk, text):
    rule = chk["rule"]
    lhs, rhs = rule.split("=", 1)
    v = (re.findall(r"[a-z]", rhs.replace("π", "")) or ["h"])[0]
    body = rhs.replace("ʰ", f"^{v}")
    xs = [F(1), F(2), F(3), F(4)]
    ys = [M.ev(body, {v: x}) for x in xs]
    d = [float(b) - float(a) for a, b in zip(ys, ys[1:])]
    lin_ = max(d) - min(d) < 1e-9
    return str(text).strip().lower() == ("linear" if lin_ else "nonlinear")


@reg
def makes_linear(chk, text):
    ys = [str(text) if y == "?" else y for y in chk["ys"]]
    try:
        pts = sorted(zip([M.ev(str(x)) for x in chk["xs"]], [M.val(str(y)) for y in ys]))
    except Exception:
        return False
    rates = {(b[1] - a[1]) / (b[0] - a[0]) for a, b in zip(pts, pts[1:])}
    return len(rates) == 1


@reg
def slope_of(chk, text):
    pts = [(M.ev(str(a)), M.ev(str(b))) for a, b in chk["pts"]]
    (x1, y1), (x2, y2) = pts[0], pts[1]
    m = (y2 - y1) / (x2 - x1)
    if any(not M.same(b - y1, m * (a - x1)) for a, b in pts):
        return False
    try:
        return M.same(M.val(text), m)
    except Exception:
        return False


@reg
def slope_kind(chk, text):
    (x1, y1), (x2, y2) = chk["pts"]
    want = "undefined" if x1 == x2 else "zero" if y1 == y2 else "positive" if (y2 - y1) * (x2 - x1) > 0 else "negative"
    return str(text).strip() == want


@reg
def missing_y(chk, text):
    k = M.val(text)
    m, (x1, y1), x = M.ev(chk["m"]), chk["p"], chk["x"]
    return M.same((k - y1) / (x - x1), m)


@reg
def intercept_of(chk, text):
    (x1, y1), (x2, y2) = [(M.ev(str(a)), M.ev(str(b))) for a, b in chk["pts"]]
    m = (y2 - y1) / (x2 - x1)
    try:
        return M.same(M.val(text), y1 - m * x1)
    except Exception:
        return False


@reg
def pair_slope(chk, text):
    ps = pairs_of(text)
    (x1, y1), (x2, y2) = ps
    return x1 != x2 and M.same((y2 - y1) / (x2 - x1), M.ev(chk["m"]))


@reg
def line_through(chk, text):
    t = str(text)
    if not re.match(r"^\s*y\s*=", t):
        return False
    try:
        f = rhs_fn(t)
        pts = [(M.ev(str(a)), M.ev(str(b))) for a, b in chk["pts"]]
        ok = all(M.same(f(a), b) for a, b in pts)
        slope = f(F(1)) - f(F(0))
        lin_ = M.same(f(F(5)) - f(F(0)), 5 * slope)
        if "m" in chk:
            ok = ok and M.same(slope, M.ev(chk["m"]))
        return ok and lin_ and (len(pts) >= 2 or "m" in chk)
    except Exception:
        return False


@reg
def intercept_pt(chk, text):
    x, y = M.parse_point(text)
    if chk["which"] == "x" and y != 0:
        return False
    if chk["which"] == "y" and x != 0:
        return False
    return eq_holds(chk["eq"], x, y)


@reg
def compare_lines(chk, text):
    A, B = [tuple(M.ev(v) for v in chk[k]) for k in ("A", "B")]
    if chk["q"] == "steeper":
        want = "Line A" if abs(A[0]) > abs(B[0]) else "Line B" if abs(B[0]) > abs(A[0]) else "They are the same"
    else:
        want = "Line A" if A[1] > B[1] else "Line B" if B[1] > A[1] else "They are the same"
    return str(text) == want


@reg
def slope_int_statement(chk, text):
    m = re.match(r"^(Yes|No)\. The slope is (-?[\d/]+) and the y-intercept is (-?[\d/]+)\.$", str(text))
    if not m:
        return False
    return M.same(M.ev(m.group(2)), M.ev(chk["m"])) and M.same(M.ev(m.group(3)), M.ev(chk["b"])) and m.group(1) == "No"


@reg
def line_statement(chk, text):
    m, b = M.ev(chk["m"]), M.ev(chk["b"])
    t = str(text)
    g = re.match(r"^The slope is (-?[\d/]+)\.$", t)
    if g:
        return M.same(M.ev(g.group(1)), m)
    g = re.match(r"^The y-intercept is (-?[\d/]+)\.$", t)
    if g:
        return M.same(M.ev(g.group(1)), b)
    g = re.match(r"^The line passes through (\(.+\))\.$", t)
    if g:
        x, y = M.parse_point(g.group(1))
        return M.same(m * x + b, y)
    g = re.match(r"^The line (rises|falls) from left to right\.$", t)
    if g:
        return (g.group(1) == "rises") == (m > 0)
    raise ValueError(t)


@reg
def predict_linear(chk, text):
    (x1, y1), (x2, y2) = [(F(a), F(b)) for a, b in chk["pts"]]
    return M.same(M.val(text), y1 + (y2 - y1) / (x2 - x1) * (F(chk["x"]) - x1))


@reg
def table_matches(chk, text):
    m = re.match(r"^x: (.+); y: (.+)$", str(text))
    xs = [M.ev(t) for t in m.group(1).split(", ")]
    ys = [M.ev(t) for t in m.group(2).split(", ")]
    return all(eq_holds(chk["eq"], x, y) for x, y in zip(xs, ys))


def seg_kinds(pts):
    return [("increasing" if b[1] > a[1] else "decreasing" if b[1] < a[1] else "constant", a[0], b[0]) for a, b in zip(pts, pts[1:])]


@reg
def pw_interval(chk, text):
    m = re.match(r"^from x = (-?\d+) to x = (-?\d+)$", str(text))
    if not m:
        return False
    a, b = int(m.group(1)), int(m.group(2))
    return any(k == chk["seg"] and x0 == a and x1 == b for k, x0, x1 in seg_kinds(chk["pts"]))


@reg
def pw_interval_ctx(chk, text):
    m = re.match(r"^from (\d+) to (\d+) " + chk["unit"] + "$", str(text))
    if not m:
        return False
    a, b = int(m.group(1)), int(m.group(2))
    ks = [s for s in seg_kinds(chk["pts"]) if s[0] == chk["seg"]]
    return len(ks) == 1 and ks[0][1] == a and ks[0][2] == b


@reg
def pw_extreme(chk, text):
    ys = [p[1] for p in chk["pts"]]
    tgt = max(ys) if chk["which"] == "maximum" else min(ys)
    if chk["q"] == "value":
        return M.same(M.val(text), F(tgt))
    xs = [p[0] for p in chk["pts"] if p[1] == tgt]
    return len(xs) == 1 and M.same(M.val(text), F(xs[0]))


@reg
def trend_of(chk, text):
    m = M.ev(chk["m"])
    return str(text) == ("increasing" if m > 0 else "decreasing" if m < 0 else "constant")


@reg
def max_ctx(chk, text):
    m = re.match(r"^(\d+) feet at (\d+) seconds$", str(text))
    top = max(chk["pts"], key=lambda p: p[1])
    return bool(m) and int(m.group(1)) == top[1] and int(m.group(2)) == top[0]


@reg
def pw_claim(chk, text):
    """Truth of statements about the segment from x=a to x=b."""
    k = [s[0] for s in seg_kinds(chk["pts"]) if s[1] == chk["a"] and s[2] == chk["b"]][0]
    t = str(text)
    if t.startswith("No. The function decreases"):
        return k == "decreasing"
    if t.startswith("No. The function is constant"):
        return k == "constant"
    if t.startswith("Yes."):
        return k == "increasing"
    raise ValueError(t)


@reg
def rate_with_units(chk, text):
    m = re.match(r"^(-?[\d./]+)\s+(.+)$", str(text).strip())
    return bool(m) and M.same(M.ev(m.group(1)), M.ev(chk["m"])) and m.group(2) == chk["units"]


@reg
def faster_rate(chk, text):
    a_name, a_rate = chk["A"]
    b_name, pts = chk["B"]
    (x1, y1), (x2, y2) = pts[0], pts[1]
    b_rate = F(y2 - y1, x2 - x1)
    want = a_name if a_rate > b_rate else b_name if b_rate > a_rate else "They read at the same rate"
    return str(text) == want


def _stmt_money(m, b, t, unit):
    g = re.match(r"^The \w[\w ]* (?:earns|rises) \$?(\d+)(?: cm)? (?:for each car|each hour)\.$", t)
    if g:
        return int(g.group(1)) == m
    g = re.match(r"^The [\w ]+ (?:started the day with|starts with) \$?(\d+)(?: cm of water)?(?: in the register)?\.$", t)
    if g:
        return int(g.group(1)) == b
    g = re.match(r"^After (\d+) (?:cars|hours), there is \$(\d+)\.$|^After (\d+) hours the level is (\d+) cm\.$", t)
    if g:
        n, v = (g.group(1), g.group(2)) if g.group(1) else (g.group(3), g.group(4))
        return m * int(n) + b == int(v)
    if "decreas" in t:
        return m < 0
    raise ValueError(t)


@reg
def register_stmt(chk, text):
    return _stmt_money(chk["m"], chk["b"], str(text), "$")


@reg
def register_stmt2(chk, text):
    return _stmt_money(chk["m"], chk["b"], str(text), "cm")


STORY_SHAPES = {}


@reg
def story_graph(chk, text):
    m = re.match(r"Graph ([A-D])$", str(text))
    return bool(m) and chk["order"]["ABCD".index(m.group(1))] == chk["k"]


@reg
def io_statement(chk, text):
    g = re.match(r"^For (\d+) (\w+), the value is (\d+) (\w+)\.$", str(text))
    if not g:
        return False
    x, xu, y, yu = int(g.group(1)), g.group(2), int(g.group(3)), g.group(4)
    m, b = chk["rule"]
    return xu == chk["xu"] and yu == chk["yu"] and m * x + b == y


@reg
def flat_duration(chk, text):
    flats = [b[0] - a[0] for a, b in zip(chk["pts"], chk["pts"][1:]) if a[1] == b[1]]
    return len(flats) == 1 and M.same(M.val(text), F(flats[0]))


@reg
def piecewise_eval(chk, text):
    (m1, b1), (m2, b2) = [(M.ev(a), M.ev(b)) for a, b in chk["pieces"]]
    x = F(chk["x"])
    v = m1 * x + b1 if x < chk["c"] else m2 * x + b2
    return M.same(M.val(text), v)


@reg
def piecewise_point(chk, text):
    x, y = M.parse_point(text)
    (m1, b1), (m2, b2) = [(M.ev(a), M.ev(b)) for a, b in chk["pieces"]]
    return M.same(y, m1 * x + b1 if x < chk["c"] else m2 * x + b2)


@reg
def story_endpoint(chk, text):
    t = v = 0
    for rate, dur in chk["r"]:
        t += dur
        v += rate * dur
    x, y = M.parse_point(text)
    return M.same(x, F(t)) and M.same(y, F(v))


@reg
def story_segments(chk, text):
    g = re.match(r"^(\d+) segments; (?:segment (\d+) is horizontal|none are horizontal)$", str(text))
    if not g:
        return False
    n = len(chk["rates"])
    flat = [i + 1 for i, rt in enumerate(chk["rates"]) if rt == 0]
    if int(g.group(1)) != n:
        return False
    return (g.group(2) is None and not flat) or (g.group(2) is not None and flat == [int(g.group(2))])


@reg
def step_cost(chk, text):
    h = F(chk["h"])
    return M.same(M.val(text), F(chk["rate"] * math.ceil(h)))


@reg
def same_line(chk, text):
    try:
        m, b = line_eq_fn(str(text))
    except Exception:
        return False
    return M.same(m, M.ev(chk["m"])) and M.same(b, M.ev(chk["b"]))


# ---------------------------------------------------------------- systems (unit 4)
@reg
def slope_int_text(chk, text):
    g = re.match(r"^slope (-?[\d/]+), y-intercept (-?[\d/]+)$", str(text))
    if not g:
        return False
    m, b = line_eq_fn(chk["eq"])
    return M.same(M.ev(g.group(1)), m) and M.same(M.ev(g.group(2)), b)


@reg
def sys_count(chk, text):
    s = M.solve_system(*chk["eqs"])
    want = {"one": ["one solution", "exactly one solution"], "none": ["no solution"], "all": ["infinitely many solutions"]}[s[0]]
    return str(text).strip() in want


@reg
def sys_ctx_pair(chk, text):
    s = M.solve_system(*chk["eqs"])
    if s[0] != "one":
        return False
    pat = re.escape(chk["fmt"]).replace(r"\{x\}", r"(-?[\d./]+)").replace(r"\{y\}", r"(-?[\d./]+)")
    g = re.match("^" + pat + "$", str(text))
    return bool(g) and M.same(M.ev(g.group(1)), s[1][0]) and M.same(M.ev(g.group(2)), s[1][1])


@reg
def eq_has_point(chk, text):
    x, y = [F(v) for v in chk["p"]]
    return eq_holds(str(text), x, y) and not M.solve_system(str(text), "x = 1000")[0] == "all"


@reg
def eq_has_point_bq(chk, text):
    t = str(text).replace("b", "x").replace("q", "y")
    x, y = [F(v) for v in chk["p"]]
    l, r = M.eq_sides(t)
    return eq_holds(t, x, y) and M.same(M.ev(r), F(chk["total"]))


@reg
def sys_var(chk, text):
    s = M.solve_system(*chk["eqs"])
    if s[0] != "one":
        return False
    v = s[1][0] if chk["var"] == "x" else s[1][1]
    try:
        return M.same(M.val(text), v)
    except Exception:
        return False


@reg
def elim_step(chk, text):
    (a1, b1), (a2, b2) = chk["e1"], chk["e2"]
    t = str(text)
    k1 = k2 = 1
    op = "add"
    g = re.match(r"^Multiply the first equation by (-?\d+) and the second by (-?\d+), then add\.$", t)
    if g:
        k1, k2 = int(g.group(1)), int(g.group(2))
    elif re.match(r"^Multiply the first equation by (-?\d+), then add\.$", t):
        k1 = int(re.match(r"^Multiply the first equation by (-?\d+)", t).group(1))
    elif re.match(r"^Multiply the second equation by (-?\d+), then add\.$", t):
        k2 = int(re.match(r"^Multiply the second equation by (-?\d+)", t).group(1))
    elif t == "Add the equations." or t == "Add the equations as they are.":
        pass
    elif t.startswith("Subtract the equations"):
        op = "sub"
    elif re.match(r"^Multiply both equations by (\d+), then add\.$", t):
        k1 = k2 = int(re.match(r"^Multiply both equations by (\d+)", t).group(1))
    else:
        raise ValueError(t)
    sgn = 1 if op == "add" else -1
    return k1 * a1 + sgn * k2 * a2 == 0 or k1 * b1 + sgn * k2 * b2 == 0


@reg
def sys_statement(chk, text):
    s = M.solve_system(*chk["eqs"])
    t = str(text)
    g = re.match(r"^([xy]) = (.+)$", t)
    if g:
        return s[0] == "one" and M.same(M.ev(g.group(2)), s[1][0 if g.group(1) == "x" else 1])
    g = re.match(r"^The point (\(.+\)) satisfies both equations\.$", t)
    if g:
        x, y = M.parse_point(g.group(1))
        return all(eq_holds(e, x, y) for e in chk["eqs"])
    if t == "The system has no solution.":
        return s[0] == "none"
    raise ValueError(t)


@reg
def sys_param(chk, text):
    k = M.val(text)
    e2 = chk["e2"].replace("kx", f"({k})x").replace("k", f"({k})")
    return M.solve_system(chk["e1"], e2)[0] == chk["want"]


@reg
def sys_pair_type(chk, text):
    try:
        return M.solve_system(chk["e1"], str(text))[0] == chk["want"]
    except Exception:
        return False


@reg
def sys_text_type(chk, text):
    e1, e2 = str(text).split(" and ")
    return M.solve_system(e1, e2)[0] == chk["want"]


@reg
def cheaper_plan(chk, text):
    (f1, r1), (f2, r2), v = chk["A"], chk["B"], chk["v"]
    a, b = f1 + r1 * v, f2 + r2 * v
    return str(text) == ("Gym A" if a < b else "Gym B" if b < a else "They cost the same")


@reg
def sys_model(chk, text):
    e1, e2 = str(text).split(" and ")
    s = M.solve_system(e1, e2)
    x0, y0 = chk["sol"]
    p1, p2 = chk["money"]
    if s[0] != "one" or not (M.same(s[1][0], F(x0)) and M.same(s[1][1], F(y0))):
        return False
    # must contain a count equation x + y = n and the money equation with the given prices
    return any(M.same(M.ev(M.eq_sides(e)[1]), F(p1 * x0 + p2 * y0)) and eq_holds(e, F(x0), F(y0)) for e in (e1, e2))


# ---------------------------------------------------------------- bivariate data (unit 5)
import statistics


def _r(xs, ys):
    return statistics.correlation([float(x) for x in xs], [float(y) for y in ys])


def _nonlinear(xs, ys):
    import numpy as np
    x, y = np.array(xs, float), np.array(ys, float)
    def r2(deg):
        p = np.polyfit(x, y, deg)
        res = ((y - np.polyval(p, x)) ** 2).sum()
        return 1 - res / ((y - y.mean()) ** 2).sum()
    return r2(2) - r2(1) > 0.3


def _assoc(xs, ys):
    if _nonlinear(xs, ys):
        return "curve"
    rr = _r(xs, ys)
    return "pos" if rr > 0.6 else "neg" if rr < -0.6 else "none" if abs(rr) < 0.35 else "weak"


@reg
def scatter_match(chk, text):
    m = re.match(r"Graph ([A-D])$", str(text))
    want = sorted(map(tuple, chk["pts"]))
    hits = [sorted(map(tuple, p)) == want for p in chk["panels"]]
    return bool(m) and sum(hits) == 1 and hits["ABCD".index(m.group(1))]


@reg
def row_point(chk, text):
    x, y = M.parse_point(text)
    k = chk["k"]
    return x == chk["xs"][k] and y == chk["ys"][k]


@reg
def axis_intervals(chk, text):
    n = int(text)
    return n * chk["step"] >= chk["hi"] and (n - 1) * chk["step"] < chk["hi"]


@reg
def in_dataset(chk, text):
    x, y = M.parse_point(text)
    return (x, y) in [(F(a), F(b)) for a, b in zip(chk["xs"], chk["ys"])]


@reg
def min_max(chk, text):
    g = re.match(r"^(-?\d+) and (-?\d+)$", str(text))
    return bool(g) and int(g.group(1)) == min(chk["vals"]) and int(g.group(2)) == max(chk["vals"])


@reg
def assoc_dir(chk, text):
    a = _assoc(chk["xs"], chk["ys"])
    return str(text).strip() == {"pos": "positive", "neg": "negative", "none": "none"}.get(a, "?")


@reg
def outlier_pt(chk, text):
    import numpy as np
    xs, ys = np.array(chk["xs"], float), np.array(chk["ys"], float)
    p = np.polyfit(xs, ys, 1)
    res = np.abs(ys - np.polyval(p, xs))
    i = int(res.argmax())
    srt = sorted(res)
    x, y = M.parse_point(text)
    return srt[-1] > 2 * srt[-2] and float(x) == xs[i] and float(y) == ys[i]


@reg
def count_above(chk, text):
    return int(text) == sum(1 for y in chk["ys"] if y > chk["t"])


@reg
def lookup_y(chk, text):
    ys = [b for a, b in zip(chk["xs"], chk["ys"]) if a == chk["x"]]
    return len(ys) == 1 and M.same(M.val(text), F(ys[0]))


@reg
def cluster_stmt(chk, text):
    t = str(text)
    g = re.match(r"^A cluster of points with x from (\d+) to (\d+)$", t)
    if g:
        lo, hi = int(g.group(1)), int(g.group(2))
        inside = sum(1 for x in chk["xs"] if lo <= x <= hi)
        return inside >= 0.6 * len(chk["xs"])
    if t.startswith("No clusters"):
        return False
    g = re.match(r"^A single outlier at (\(.+\))$", t)
    if g:
        x, y = M.parse_point(g.group(1))
        return (int(x), int(y)) in zip(chk["xs"], chk["ys"])
    raise ValueError(t)


@reg
def trend_word(chk, text):
    rr = _r(chk["xs"], chk["ys"])
    return str(text) == ("increase" if rr > 0.6 else "decrease" if rr < -0.6 else "?")


@reg
def scatter_stmt(chk, text):
    t = str(text)
    xs, ys = chk["xs"], chk["ys"]
    g = re.match(r"^The greatest (.+) is (-?\d+)\.$", t)
    if g and g.group(1) == chk["yl"]:
        return int(g.group(2)) == max(ys)
    g = re.match(r"^The least (.+) is (-?\d+)\.$", t)
    if g and g.group(1) == chk["xl"]:
        return int(g.group(2)) == min(xs)
    g = re.match(r"^The association is (positive|negative)\.$", t)
    if g:
        return {"pos": "positive", "neg": "negative"}.get(_assoc(xs, ys)) == g.group(1)
    g = re.match(r"^There are (\d+) data points\.$", t)
    if g:
        return int(g.group(1)) == len(xs)
    raise ValueError(t)


@reg
def assoc_type(chk, text):
    a = _assoc(chk["xs"], chk["ys"])
    return str(text) == {"pos": "positive linear association", "neg": "negative linear association", "none": "no association", "curve": "nonlinear association"}.get(a, "?")


@reg
def assoc_word(chk, text):
    a = _assoc(chk["xs"], chk["ys"])
    if chk["L"] == 2:
        want = {"pos": "positive linear", "neg": "negative linear", "none": "none", "curve": "nonlinear"}.get(a)
    else:
        want = {"pos": "positive", "neg": "negative", "none": "no association"}.get(a)
    return str(text) == want


@reg
def stronger(chk, text):
    ra, rb = abs(_r(*chk["A"])), abs(_r(*chk["B"]))
    return str(text) == ("Plot A" if ra > rb + 0.1 else "Plot B" if rb > ra + 0.1 else "?")


@reg
def assoc_claim(chk, text):
    a = _assoc(chk["xs"], chk["ys"])
    t = str(text)
    if t.startswith("No. The points fall"):
        return a == "neg"
    if t.startswith("No. There is no association"):
        return a == "none"
    if t.startswith("Yes"):
        return False if "positive" in t and a != "pos" else a == "pos" and "positive" in t
    raise ValueError(t)


@reg
def assoc_is(chk, text):
    g = re.match(r"^x: (.+); y: (.+)$", str(text))
    xs = [int(v) for v in g.group(1).split(", ")]
    ys = [int(v) for v in g.group(2).split(", ")]
    return {"pos": "positive", "neg": "negative", "none": "none"}.get(_assoc(xs, ys)) == chk["want"]


@reg
def table_linear2(chk, text):
    d = [b - a for a, b in zip(chk["ys"], chk["ys"][1:])]
    return str(text) == ("linear" if len(set(d)) == 1 else "nonlinear")


@reg
def fit_meaning(chk, text):
    m, b = M.ev(chk["m"]), M.ev(chk["b"])
    t = str(text)
    g = re.match(r"^The (.+) changes by (-?[\d/]+) for each 1 increase in (.+)\.$", t)
    if g:
        return g.group(1) == chk["yl"] and g.group(3) == chk["xl"] and M.same(M.ev(g.group(2)), m)
    g = re.match(r"^The (?:predicted )?(.+) is (-?[\d/]+) when (.+) is 0\.$", t)
    if g:
        return g.group(1) == chk["yl"] and g.group(3) == chk["xl"] and M.same(M.ev(g.group(2)), b)
    raise ValueError(t)


@reg
def best_fit(chk, text):
    import numpy as np
    m, b = line_eq_fn(str(text))
    xs, ys = np.array(chk["xs"], float), np.array(chk["ys"], float)
    sse = ((ys - float(m) * xs - float(b)) ** 2).sum()
    p = np.polyfit(xs, ys, 1)
    best = ((ys - np.polyval(p, xs)) ** 2).sum()
    return sse <= best * 1.35 + 1


@reg
def fit_stmt(chk, text):
    m, b = M.ev(chk["m"]), M.ev(chk["b"])
    t = str(text)
    g = re.match(r"^For x = (-?\d+), the predicted y is (-?[\d/]+)\.$", t)
    if g:
        return M.same(m * int(g.group(1)) + b, M.ev(g.group(2)))
    g = re.match(r"^The predicted y increases by (-?[\d/]+) for each 1 increase in x\.$", t)
    if g:
        return M.same(M.ev(g.group(1)), m)
    g = re.match(r"^When x = 0, the predicted y is (-?[\d/]+)\.$", t)
    if g:
        return M.same(M.ev(g.group(1)), b)
    raise ValueError(t)


def _tw(t):
    a, b, c, d = t
    return {"row": a + b, "row2": c + d, "col": a + c, "col2": b + d, "grand": a + b + c + d, "cell": d}


@reg
def twoway_cell(chk, text):
    return int(text) == _tw(chk["t"])[chk["q"]]


@reg
def twoway_layout(chk, text):
    g = re.match(r"^.+?: (\d+), (\d+) \| .+?: (\d+), (\d+) \(columns", str(text))
    return bool(g) and [int(x) for x in g.groups()] == chk["t"]


@reg
def twoway_stmt(chk, text):
    a, b, c, d = chk["t"]
    (r1, r2), (c1, c2) = chk["g"]
    t = str(text)
    g = re.match(r"^The (.+) row total is (\d+)\.$", t)
    if g:
        return int(g.group(2)) == (a + b if g.group(1) == r1 else c + d)
    g = re.match(r'^The "(.+)" column total is (\d+)\.$', t)
    if g:
        return int(g.group(2)) == (a + c if g.group(1) == c1 else b + d)
    g = re.match(r"^The grand total is (\d+)\.$", t)
    if g:
        return int(g.group(1)) == a + b + c + d
    raise ValueError(t)


@reg
def relfreq(chk, text):
    a, b, c, d = chk["t"]
    v = {"joint": F(a, a + b + c + d), "row": F(a, a + b), "col": F(a, a + c), "row2": F(c, c + d)}[chk["q"]]
    if chk["pct"]:
        return str(text) == round_text(v * 100, 1) + "%"
    try:
        return frac_text({"expr": f"{v.numerator}/{v.denominator}"}, text)
    except Exception:
        return False


@reg
def twoway_assoc(chk, text):
    a, b, c, d = chk["t"]
    diff = abs(F(a, a + b) - F(c, c + d))
    t = str(text)
    if t.startswith("Yes, because ") and "% of" in t:
        return diff >= F(1, 5)
    if t.startswith("No, because about the same percent"):
        return diff <= F(1, 10)
    return False


@reg
def greater_group(chk, text):
    a, b, c, d = chk["t"]
    f1, f2 = F(a, a + b), F(c, c + d)
    return str(text) == (chk["names"][0] if f1 > f2 else chk["names"][1] if f2 > f1 else "They are equal")


@reg
def rf_stmt(chk, text):
    a, b, c, d = chk["t"]
    (r1, r2), (c1, c2) = chk["g"]
    t = str(text)
    g = re.match(r'^Among (.+), the relative frequency of "(.+)" is (\d+/\d+|\d+)\.$', t)
    if g:
        grp = g.group(1)
        v = F(a, a + b) if grp == r1 else F(c, c + d)
        return M.same(M.ev(g.group(3)), v)
    g = re.match(r"^Among all people, the relative frequency of (.+) who (.+) is (\d+/\d+|\d+)\.$", t)
    if g:
        return M.same(M.ev(g.group(3)), F(a, a + b + c + d))
    raise ValueError(t)


# ---------------------------------------------------------------- transformations & geometry (unit 6)
TRIG = {0: (1, 0), 90: (0, 1), 180: (-1, 0), 270: (0, -1), 45: None}


def _rotf(deg):
    c, s = TRIG[deg % 360]
    return lambda p: (c * p[0] - s * p[1], s * p[0] + c * p[1])


def _reflf(phi2):
    """Reflection across a line through the origin making angle phi with the x-axis; phi2 = 2*phi in degrees."""
    c, s = TRIG[phi2 % 360]
    return lambda p: (c * p[0] + s * p[1], s * p[0] - c * p[1])


def parse_xf(desc):
    t = str(desc).strip()
    t = re.sub(r"^an? ", "", t)
    m = re.match(r"^(.*?) followed by (?:an? )?(.*)$", t)
    if m:
        f1, f2 = parse_xf(m.group(1)), parse_xf(m.group(2))
        return lambda p: f2(f1(p))
    m = re.match(r"^translation (.+)$", t)
    if m and "→" not in t:
        dx = dy = 0
        for n, d in re.findall(r"(\d+) units? (right|left|up|down)", m.group(1)):
            n = int(n)
            dx += n if d == "right" else -n if d == "left" else 0
            dy += n if d == "up" else -n if d == "down" else 0
        return lambda p: (p[0] + dx, p[1] + dy)
    m = re.match(r"^(?:translation )?\(x, y\) → \(x ([+-]) (\d+), y ([+-]) (\d+)\)$", t)
    if m:
        dx = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
        dy = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
        return lambda p: (p[0] + dx, p[1] + dy)
    m = re.match(r"^reflection over the (x-axis|y-axis|line y = x|line y = -x|line ([xy]) = (-?\d+))$", t)
    if m:
        w = m.group(1)
        if w == "x-axis":
            return _reflf(0)
        if w == "y-axis":
            return _reflf(180)
        if w == "line y = x":
            return _reflf(90)
        if w == "line y = -x":
            return _reflf(270)
        c = int(m.group(3))
        return (lambda p: (2 * c - p[0], p[1])) if m.group(2) == "x" else (lambda p: (p[0], 2 * c - p[1]))
    m = re.match(r"^rotation (90|180|270)° ?(clockwise|counterclockwise)? about the origin$", t)
    if m:
        d = int(m.group(1))
        return _rotf(-d if m.group(2) == "clockwise" else d)
    m = re.match(r"^dilation with scale factor (\S+) centered at the origin$", t)
    if m:
        k = M.ev(m.group(1))
        return lambda p: (k * p[0], k * p[1])
    raise ValueError("cannot parse transformation: " + t)


def _pts(lst):
    return [(F(a), F(b)) for a, b in lst]


@reg
def xf_maps(chk, text):
    try:
        f = parse_xf(text)
    except ValueError:
        return False
    return all(tuple(F(v) for v in f(p)) == q for p, q in zip(_pts(chk["pre"]), _pts(chk["img"])))


def _classify(pre, img):
    pre, img = _pts(pre), _pts(img)
    d = lambda a, b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    r2 = d(img[0], img[1]) / d(pre[0], pre[1])
    if r2 != 1:
        return "dilation"
    vec = {(q[0] - p[0], q[1] - p[1]) for p, q in zip(pre, img)}
    if len(vec) == 1:
        return "translation"
    cross = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return "rotation" if (cross(*pre) > 0) == (cross(*img) > 0) else "reflection"


@reg
def xf_type(chk, text):
    return str(text) == _classify(chk["pre"], chk["img"])


RIGID = ("translation", "reflection", "rotation")


@reg
def xf_congruent(chk, text):
    rigid = not chk["name"].startswith("dilation") or re.search(r"scale factor 1 ", chk["name"])
    return str(text) == ("yes" if rigid else "no")


@reg
def xf_property(chk, text):
    k = chk["k"]
    t = str(text)
    keeps_len = k in RIGID
    keeps_or = k in ("translation", "rotation", "dilation")
    if t == "Lengths, angles and orientation are all preserved.":
        return keeps_len and keeps_or
    if t == "Lengths and angles are preserved, but orientation is reversed.":
        return keeps_len and not keeps_or
    if t == "Angles are preserved, but lengths are multiplied by the scale factor.":
        return not keeps_len
    return False


@reg
def xf_congruent_any(chk, text):
    t = str(text)
    if t.startswith("dilation") or "stretch" in t:
        return False
    return t.split()[0] in RIGID


@reg
def xf_point(chk, text):
    try:
        q = M.parse_point(text)
    except M.ParseError:
        return False
    p = tuple(F(v) for v in chk["p"])
    out = parse_xf(chk["desc"])(p)
    return M.same(q[0], out[0]) and M.same(q[1], out[1])


@reg
def xf_preimage(chk, text):
    q = M.parse_point(text)
    out = parse_xf(chk["desc"])(q)
    return tuple(F(v) for v in out) == tuple(F(v) for v in chk["img"])


@reg
def xf_point_any(chk, text):
    try:
        f = parse_xf(text)
    except ValueError:
        return False
    out = f(tuple(F(v) for v in chk["p"]))
    return tuple(out) == tuple(F(v) for v in chk["img"])


@reg
def refl_line_name(chk, text):
    t = str(text)
    t = t if t.startswith("the line") else "the " + t
    try:
        f = parse_xf("reflection over " + t)
    except ValueError:
        return False
    return all(tuple(f(p)) == q for p, q in zip(_pts(chk["pre"]), _pts(chk["img"])))


@reg
def refl_line_eq(chk, text):
    try:
        f = parse_xf("reflection over the line " + str(text))
    except ValueError:
        return False
    return all(tuple(f(p)) == q for p, q in zip(_pts(chk["pre"]), _pts(chk["img"])))


@reg
def compose_translation(chk, text):
    m = re.match(r"^(.+); (\(.+\))$", str(text))
    if not m:
        return False
    p = tuple(F(v) for v in chk["p"])
    q = p
    for a, b in chk["moves"]:
        q = (q[0] + a, q[1] + b)
    try:
        single = parse_xf(m.group(1)) if m.group(1) != "no movement" else (lambda z: z)
    except ValueError:
        return False
    return tuple(single(p)) == q and M.parse_point(m.group(2)) == q


@reg
def translation_stmt(chk, text):
    t = str(text)
    if t in ("A′B′ = AB", "Triangle A′B′C′ is congruent to triangle ABC."):
        return True
    if t in ("Triangle A′B′C′ is larger than triangle ABC.", "The orientation of the vertices is reversed."):
        return False
    g = re.match(r"^Every point moves (.+)\.$", t)
    if g:
        f = parse_xf("translation " + g.group(1))
        return f((0, 0)) == (chk["a"], chk["b"])
    raise ValueError(t)


@reg
def dil_factor(chk, text):
    k = M.val(text)
    return all(M.same(k * a, c) and M.same(k * b, d) for (a, b), (c, d) in zip(_pts(chk["pre"]), _pts(chk["img"])))


@reg
def enlarge_word(chk, text):
    k = M.ev(chk["k"])
    return str(text) == ("enlargement" if k > 1 else "reduction" if 0 < k < 1 else "congruent copy")


@reg
def dil_measure(chk, text):
    k = M.ev(chk["k"])
    t = M.strip_units(str(text).replace("°", ""))
    v = M.ev(t)
    o = F(chk["orig"])
    want = {"length": k * o, "perimeter": k * o, "area": k * k * o, "angle": o}[chk["q"]]
    return M.same(v, want)


@reg
def dil_center(chk, text):
    q = M.parse_point(text)
    k = M.ev(chk["k"])
    (px, py), (cx, cy) = [tuple(F(v) for v in z) for z in (chk["p"], chk["c"])]
    # check: C, P, P' collinear with CP' = k·CP (vector form)
    return M.same(q[0] - cx, k * (px - cx)) and M.same(q[1] - cy, k * (py - cy))


@reg
def dil_stmt(chk, text):
    k = M.ev(chk["k"])
    t = str(text)
    if t in ("Corresponding angles are congruent.", "The image is similar to the original."):
        return True
    if t == "The image is congruent to the original.":
        return k == 1
    if t == "Corresponding angles are multiplied by the scale factor.":
        return False
    g = re.match(r"^Each image side is (\S+) times as long as the original side\.$", t)
    if g:
        return M.same(M.ev(g.group(1)), k)
    g = re.match(r"^The image area is (\S+) times the original area\.$", t)
    if g:
        return M.same(M.ev(g.group(1)), k * k)
    raise ValueError(t)


@reg
def xf_seq(chk, text):
    q = M.parse_point(text)
    p = tuple(F(v) for v in chk["p"])
    for d in chk["descs"]:
        p = parse_xf(d)(p)
    return M.same(q[0], p[0]) and M.same(q[1], p[1])


def _is_rigid(desc):
    return not str(desc).lstrip("a ").startswith("dilation") or bool(re.search(r"scale factor 1 ", desc))


@reg
def seq_congruent(chk, text):
    rigid = all(_is_rigid(re.sub(r"^an? ", "", d)) for d in chk["descs"])
    return str(text) == ("congruent" if rigid else "similar")


@reg
def seq_maps(chk, text):
    return xf_maps(chk, text)


@reg
def seq_congruent_text(chk, text):
    parts = re.split(r" followed by ", re.sub(r"^an? ", "", str(text)))
    return all(_is_rigid(re.sub(r"^an? ", "", p)) for p in parts)


@reg
def order_distance(chk, text):
    p = tuple(F(v) for v in chk["p"])
    a = chk["a"]
    f1 = parse_xf(f"reflection over the x-axis followed by a translation {abs(a)} units {'up' if a > 0 else 'down'}")
    f2 = parse_xf(f"translation {abs(a)} units {'up' if a > 0 else 'down'} followed by a reflection over the x-axis")
    q1, q2 = f1(p), f2(p)
    dist = math.hypot(float(q1[0] - q2[0]), float(q1[1] - q2[1]))
    return abs(float(M.val(text)) - dist) < 1e-9


@reg
def angle_sum_missing(chk, text):
    return M.same(M.val(str(text).replace("°", "")), F(180 - sum(chk["known"])))


@reg
def iso_base(chk, text):
    x = M.val(str(text).replace("°", ""))
    return M.same(2 * x + chk["top"], F(180))


@reg
def tri_alg_largest(chk, text):
    s = M.solve_linear(" + ".join(f"({e})" for e in chk["exprs"]) + " = 180")
    vals = [M.ev(e, {"x": s[1]}) for e in chk["exprs"]]
    return M.same(M.val(str(text).replace("°", "")), max(vals))


@reg
def exterior(chk, text):
    # exterior angle = 180 - third interior angle
    third = 180 - sum(chk["known"])
    return M.same(M.val(str(text).replace("°", "")), F(180 - third))


@reg
def exterior_remote(chk, text):
    x = M.val(str(text).replace("°", ""))
    third = 180 - chk["a"] - x
    return M.same(180 - third, F(chk["ext"]))


@reg
def angle_set_ok(chk, text):
    vals = [int(v) for v in re.findall(r"(\d+)°", str(text))]
    return len(vals) == 3 and all(v > 0 for v in vals) and sum(vals) == 180


@reg
def sim_side(chk, text):
    s = [F(v) for v in chk["s"]]
    j, val = chk["known"]
    k = M.ev(val) / s[j]
    return M.same(M.val(text), k * s[chk["ask"]])


@reg
def aa_similar(chk, text):
    t1 = sorted(chk["t1"] + [180 - sum(chk["t1"])])
    t2 = sorted(chk["t2"] + [180 - sum(chk["t2"])])
    return str(text) == ("yes" if t1 == t2 else "no")


@reg
def shadow(chk, text):
    h = M.val(text)
    return M.same(h / F(chk["s2"]), M.ev(chk["h1"]) / F(chk["s1"]))


@reg
def sim_perimeter(chk, text):
    s = sorted(F(v) for v in chk["s"])
    k = M.ev(chk["short"]) / s[0]
    return M.same(M.val(text), k * sum(s))


@reg
def nested_sim(chk, text):
    ce = M.val(text)
    return M.same(ce / F(chk["bd"]), F(chk["ab"] + chk["bc"], chk["ab"]))


@reg
def sim_set(chk, text):
    vals = sorted(M.ev(v) for v in str(text).split(", "))
    s = sorted(F(v) for v in chk["s"])
    k = vals[0] / s[0]
    return all(M.same(a, k * b) for a, b in zip(vals, s))


def _para_measure(theta, n):
    """Angle n at the intersection of a horizontal line with a transversal rising at theta degrees.
    Rays: right 0°, transversal-up theta, left 180°, transversal-down 180+theta. Quadrant of n: 1 UL, 2 UR, 3 LL, 4 LR."""
    q = (int(n) - 1) % 4
    rays = {0: (theta, 180), 1: (0, theta), 2: (180, 180 + theta), 3: (180 + theta, 360)}[q]
    return rays[1] - rays[0]


@reg
def para_angle(chk, text):
    return M.same(M.val(str(text).replace("°", "")), F(_para_measure(chk["theta"], chk["n"])))


@reg
def para_rel(chk, text):
    a, b = int(chk["a"]), int(chk["b"])
    qa, qb = (a - 1) % 4, (b - 1) % 4
    same_int = (a <= 4) == (b <= 4)
    up = lambda q: q in (0, 1)
    left = lambda q: q in (0, 2)
    interior = lambda n: (n <= 4 and not up((n - 1) % 4)) or (n > 4 and up((n - 1) % 4))
    if same_int:
        rel = "vertical" if qa + qb == 3 else "linear pair"
    elif qa == qb:
        rel = "corresponding"
    elif interior(a) and interior(b):
        rel = "alternate interior" if left(qa) != left(qb) else "same-side interior"
    elif not interior(a) and not interior(b):
        rel = "alternate exterior" if left(qa) != left(qb) else "same-side exterior"
    else:
        rel = "other"
    t = str(text)
    return t == (f"{rel} angles" if rel != "linear pair" else "a linear pair")


@reg
def para_alg(chk, text):
    va, vb = _para_measure(chk["theta"], chk["a"]), _para_measure(chk["theta"], chk["b"])
    x = M.val(text)
    e1, e2 = [M.ev(e, {"x": x}) for e in chk["e"]]
    return M.same(e1, F(va)) and M.same(e2, F(vb))


@reg
def para_congruent(chk, text):
    n = str(text).replace("∠", "")
    return _para_measure(chk["theta"], n) == _para_measure(chk["theta"], chk["ref"])


# ---------------------------------------------------------------- geometry applications (unit 7)
@reg
def is_right(chk, text):
    s = sorted(M.ev(v) for v in chk["sides"])
    return str(text) == ("yes" if s[0] ** 2 + s[1] ** 2 == s[2] ** 2 else "no")


@reg
def is_right_set(chk, text):
    s = sorted(M.ev(v) for v in str(text).split(", "))
    return s[0] ** 2 + s[1] ** 2 == s[2] ** 2


@reg
def pyth_var(chk, text):
    x = M.val(text)
    leg = x + chk["k"]
    return leg > 0 and chk["a"] ** 2 + leg ** 2 == chk["c"] ** 2


@reg
def diag_stmt(chk, text):
    d = math.sqrt(chk["a"] ** 2 + chk["b"] ** 2)
    t = str(text)
    g = re.match(r"^The diagonal is (\d+) ft\.$", t)
    if g:
        return abs(d - int(g.group(1))) < 1e-9
    g = re.match(r"^The diagonal is shorter than (\d+) ft\.$", t)
    if g:
        return d < int(g.group(1))
    g = re.match(r"^The diagonal squared equals (\d+)\.$", t)
    if g:
        return int(g.group(1)) == chk["a"] ** 2 + chk["b"] ** 2
    raise ValueError(t)


@reg
def pyth_eq(chk, text):
    try:
        s = scan_roots(str(text).replace("h", "x"), "x", 0.0, 200.0)[0]
    except Exception:
        return False
    return len(s) == 1 and abs(s[0] ** 2 + chk["leg"] ** 2 - chk["hyp"] ** 2) < 1e-6


def _space(d):
    return math.sqrt(sum(v * v for v in d))


@reg
def rod_fits(chk, text):
    fits = chk["rod"] <= _space(chk["dims"])
    t = str(text)
    g = re.match(r"^(Yes|No), because the longest segment inside the box is about ([\d.]+) in\.$", t)
    if g:
        return (g.group(1) == "Yes") == fits and round_text(_space(chk["dims"]), 1) == g.group(2)
    return False


@reg
def rod_fits_yn(chk, text):
    return str(text) == ("yes" if chk["rod"] <= _space(chk["dims"]) else "no")


@reg
def box_stmt(chk, text):
    l, w, h = chk["dims"]
    t = str(text)
    g = re.match(r"^The bottom-face diagonal squared is (\d+)\.$", t)
    if g:
        return int(g.group(1)) == l * l + w * w
    g = re.match(r"^The space diagonal is ([\d.]+)\.$", t)
    if g:
        return abs(float(g.group(1)) - _space(chk["dims"])) < 1e-9
    g = re.match(r"^The space diagonal squared is (\d+)\.$", t)
    if g:
        return int(g.group(1)) == l * l + w * w + h * h
    raise ValueError(t)


def _d(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])


@reg
def dist(chk, text):
    try:
        return abs(float(M.val(text)) - _d(chk["p"], chk["q"])) < 1e-9
    except Exception:
        return False


@reg
def dist_round(chk, text):
    return M.strip_units(str(text)) == round_text(_d(chk["p"], chk["q"]), chk["places"])


@reg
def perim(chk, text):
    p = chk["pts"]
    tot = sum(_d(p[i], p[(i + 1) % 3]) for i in range(3))
    return abs(float(M.val(text)) - tot) < 1e-9


@reg
def dist_k(chk, text):
    k = M.val(text)
    return k > chk["gt"] and abs(_d(chk["p"], (float(k), chk["y2"])) - chk["d"]) < 1e-9


@reg
def closer(chk, text):
    da, db = _d(chk["o"], chk["a"]), _d(chk["o"], chk["b"])
    t = str(text)
    if t.startswith("("):
        p = M.parse_point(t)
        target = chk["a"] if da < db else chk["b"]
        return [float(v) for v in p] == [float(v) for v in target]
    return False


@reg
def dist_is(chk, text):
    p = M.parse_point(text)
    return abs(_d(chk["o"], [float(v) for v in p]) - chk["d"]) < 1e-9


@reg
def vol_compare(chk, text):
    r_, h = chk["r"], chk["h"]
    t = str(text)
    if chk["q"] == "cone_clyl" or chk["q"] == "cone_cyl":
        cyl, cone = math.pi * r_ * r_ * h, math.pi * r_ * r_ * h / 3
        g = re.match(r"^The cylinder's volume is (\d+) times the cone's volume\.$", t)
        if g:
            return abs(cyl - int(g.group(1)) * cone) < 1e-9
        g = re.match(r"^The cone's volume is (\d+) times the cylinder's volume\.$", t)
        if g:
            return abs(cone - int(g.group(1)) * cyl) < 1e-9
        if t == "They have the same volume.":
            return False
        raise ValueError(t)
    sph, cyl = 4 / 3 * math.pi * r_ ** 3, math.pi * r_ * r_ * 2 * r_
    if t == "The sphere's volume equals the cylinder's volume.":
        return abs(sph - cyl) < 1e-9
    g = re.match(r"^The sphere's volume is (\S+) of the cylinder's volume\.$", t)
    if g:
        return abs(sph - float(M.ev(g.group(1))) * cyl) < 1e-9
    raise ValueError(t)


@reg
def vol_stmt(chk, text):
    r_, h = chk["r"], chk["h"]
    vols = {"cylinder": math.pi * r_ * r_ * h, "cone": math.pi * r_ * r_ * h / 3, "sphere": 4 / 3 * math.pi * r_ ** 3}
    g = re.match(r"^The (cylinder|cone|sphere)'s volume is (.+)\.$", str(text))
    return abs(float(M.ev(g.group(2))) - vols[g.group(1)]) < 1e-9


@reg
def solve_dim(chk, text):
    v = M.val(text)
    env = {k: F(x) for k, x in chk["known"].items()}
    env[chk["var"]] = v
    return v > 0 and abs(float(M.ev(chk["formula"], env)) - float(M.ev(chk["V"]))) < 1e-9


@reg
def scale_vol(chk, text):
    k = chk["k"]
    base = math.pi * 2 * 2 * 3
    new = math.pi * (2 * k) ** 2 * 3 if chk["q"] == "radius" else math.pi * 4 * 3 * k
    g = re.match(r"^It is multiplied by (\d+)\.$", str(text))
    if g:
        return abs(new - int(g.group(1)) * base) < 1e-9
    return str(text) == "It does not change." and abs(new - base) < 1e-9


@reg
def cyl_vol_is(chk, text):
    g = re.match(r"^radius (\S+), height (\S+)$", str(text))
    r_, h = M.ev(g.group(1)), M.ev(g.group(2))
    return r_ * r_ * h == chk["V"]


@reg
def composite_h(chk, text):
    h1 = M.val(text)
    r_, h2 = chk["r"], chk["h2"]
    total = math.pi * r_ * r_ * float(h1) + math.pi * r_ * r_ * h2 / 3
    return abs(total - float(M.ev(chk["V"]))) < 1e-9


@reg
def capsule_stmt(chk, text):
    r_, h = chk["r"], chk["h"]
    parts = {"cylinder part": math.pi * r_ * r_ * h, "hemisphere part": 2 / 3 * math.pi * r_ ** 3}
    parts["total"] = sum(parts.values())
    g = re.match(r"^The (cylinder part|hemisphere part|total) is (.+)\.$", str(text))
    return abs(float(M.ev(g.group(2))) - parts[g.group(1)]) < 1e-9
