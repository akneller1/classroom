"""Exact-arithmetic helpers used when sympy is unavailable (session 2+).
Fractions, univariate polynomials, radicals, plain-Unicode formatting, numeric checks."""
from fractions import Fraction as F
import math, cmath, re

SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(k):
    return str(k).translate(SUP)


def fr(v):
    """Fraction/int → 'a/b' text."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def frp(v):
    """Fraction text wrapped in parentheses when negative or fractional (for substitution)."""
    s = fr(v)
    return f"({s})" if ("/" in s or s.startswith("-")) else s


def dec(v, d=2):
    s = f"{float(v):.{d}f}"
    return s


def sqfree(n):
    """n = k²·m with m squarefree → (k, m)."""
    n = int(n); assert n >= 0
    k, m, p = 1, n, 2
    while p * p <= m:
        while m % (p * p) == 0:
            m //= p * p; k *= p
        p += 1
    return k, m


def rad(n, coef=1):
    """coef·√n simplified text."""
    k, m = sqfree(n); c = F(coef) * k
    if m == 1:
        return fr(c)
    cs = "" if c == 1 else ("-" if c == -1 else fr(c))
    return f"{cs}√{m}"


class P:
    """Univariate polynomial with Fraction coefficients; c[i] = coefficient of x^i."""

    def __init__(self, c=(0,), var="x"):
        if isinstance(c, dict):
            m = max(c) if c else 0; c = [c.get(i, 0) for i in range(m + 1)]
        c = [F(v) for v in c]
        while len(c) > 1 and c[-1] == 0:
            c.pop()
        self.c, self.v = c, var

    @classmethod
    def roots(cls, rs, a=1, var="x"):
        p = cls([a], var)
        for r in rs:
            p = p * cls([-F(r), 1], var)
        return p

    @classmethod
    def coeffs(cls, *desc, var="x"):
        return cls(list(reversed(desc)), var)

    def _co(self, o):
        return o if isinstance(o, P) else P([o], self.v)

    def __add__(self, o):
        o = self._co(o); n = max(len(self.c), len(o.c))
        return P([(self.c[i] if i < len(self.c) else 0) + (o.c[i] if i < len(o.c) else 0) for i in range(n)], self.v)
    __radd__ = __add__

    def __neg__(self):
        return P([-v for v in self.c], self.v)

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        o = self._co(o); r = [F(0)] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            for j, b in enumerate(o.c):
                r[i + j] += a * b
        return P(r, self.v)
    __rmul__ = __mul__

    def __pow__(self, k):
        r = P([1], self.v)
        for _ in range(k):
            r = r * self
        return r

    def __eq__(self, o):
        return self.c == self._co(o).c

    def __hash__(self):
        return hash(tuple(self.c))

    @property
    def deg(self):
        return len(self.c) - 1 if any(self.c) else -1

    @property
    def lead(self):
        return self.c[-1]

    def desc(self):
        return list(reversed(self.c))

    def __call__(self, v):
        r = 0
        for a in reversed(self.c):
            r = r * v + (a if not isinstance(v, (float, complex)) else complex(a) if isinstance(v, complex) else float(a))
        return r

    def divmod(self, d):
        q = [F(0)] * max(1, len(self.c) - len(d.c) + 1); r = list(self.c)
        while len(r) >= len(d.c) and any(r):
            k = len(r) - len(d.c); f = r[-1] / d.c[-1]; q[k] = f
            for i, b in enumerate(d.c):
                r[i + k] -= f * b
            r.pop()
            while len(r) > 1 and r[-1] == 0:
                r.pop()
        return P(q, self.v), P(r or [0], self.v)

    def __floordiv__(self, d):
        return self.divmod(d)[0]

    def __mod__(self, d):
        return self.divmod(d)[1]

    def deriv(self):
        return P([i * self.c[i] for i in range(1, len(self.c))] or [0], self.v)

    def synth(self, r):
        """Synthetic division rows: (bottom row incl. remainder)."""
        out, acc = [], F(0)
        for a in self.desc():
            acc = acc * r + a; out.append(acc)
        return out

    def rational_roots(self):
        """All rational roots with multiplicity (sorted)."""
        p, roots = P(self.c, self.v), []
        while p.deg > 0:
            if p.c[0] == 0:
                roots.append(F(0)); p = P(p.c[1:], self.v); continue
            den = [F(v).denominator for v in p.c]; L = math.lcm(*den)
            ints = [int(v * L) for v in p.c]
            a0, an = abs(ints[0]), abs(ints[-1]); found = None
            for q in divisors(an):
                for pp in divisors(a0):
                    for s in (1, -1):
                        r = F(s * pp, q)
                        if p(r) == 0:
                            found = r; break
                    if found is not None: break
                if found is not None: break
            if found is None:
                break
            roots.append(found); p = p // P([-found, 1], self.v)
        return sorted(roots), p

    def __str__(self):
        return pstr(self)

    def __repr__(self):
        return pstr(self)


def divisors(n):
    n = abs(int(n))
    return [d for d in range(1, n + 1) if n % d == 0] or [1]


X = P([0, 1])


def term(c, k, v="x"):
    c = F(c)
    if k == 0:
        return fr(c)
    vv = v + (sup(k) if k > 1 else "")
    if c == 1: return vv
    if c == -1: return "-" + vv
    s = fr(c)
    if "/" in s:
        return f"({s}){vv}" if not s.startswith("-") else f"-({s[1:]}){vv}"
    return s + vv


def pstr(p, v=None):
    v = v or p.v; out = ""
    for k in range(len(p.c) - 1, -1, -1):
        c = p.c[k]
        if c == 0: continue
        t = term(abs(c), k, v)
        if not out:
            out = ("-" + t) if c < 0 else t
        else:
            out += (" - " if c < 0 else " + ") + t
    return out or "0"


def lin_factor(r, v="x"):
    """Factor text for root r: (x - r) or (qx - p)."""
    r = F(r); p, q = r.numerator, r.denominator
    if p == 0: return v
    a = v if q == 1 else f"{q}{v}"
    return f"({a} {'-' if p > 0 else '+'} {abs(p)})"


def factor_str(poly, v=None):
    """Factor over the rationals into content × linear factors × leftover."""
    v = v or poly.v
    roots, rest = poly.rational_roots()
    # build linear factors with integer coefficients; track scalar
    scal = rest.lead if rest.deg == 0 else F(1)
    if rest.deg > 0:
        den = math.lcm(*[c.denominator for c in rest.c]); g = math.gcd(*[int(c * den) for c in rest.c])
        g = F(g, den) * (1 if rest.lead > 0 else -1)
        rest = P([c / g for c in rest.c], v); scal = g
    for r in roots:
        scal /= r.denominator if r != 0 else 1
    # each (q x - p) contributes factor q relative to (x - r): scal stays poly lead / prod q
    from collections import Counter
    cnt = Counter(roots); parts = []
    for r in sorted(cnt, key=lambda z: (z != 0, z)):
        f = lin_factor(r, v); m = cnt[r]
        parts.append(f + (sup(m) if m > 1 else ""))
    if rest.deg > 0:
        parts.append(f"({pstr(rest, v)})" if (roots or scal != 1) else pstr(rest, v))
    head = "" if scal == 1 else ("-" if scal == -1 else fr(scal))
    if not parts:
        return fr(scal)
    s = head + "".join(parts)
    # verify
    return s


def peval(expr, **vals):
    """Evaluate a plain-Unicode/text math string numerically (verification only)."""
    e = expr.replace("−", "-").replace("·", "*").replace("×", "*").replace("÷", "/").replace("π", "pi")
    e = e.replace("^", "**")
    e = re.sub(r"√\(", "sqrt(", e)
    e = re.sub(r"√(\d+|[a-z])", r"sqrt(\1)", e)
    e = re.sub(r"([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)", lambda m: "**(" + m.group(1).translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")) + ")", e)
    e = re.sub(r"(\d|\))\s*(?=[a-zA-Z(])", r"\1*", e)
    e = re.sub(r"\)\s*\(", ")*(", e)
    e = re.sub(r"(?<=[a-z])(?=\()", "", e)
    env = {k: getattr(cmath, k) for k in ("sqrt", "exp", "log", "sin", "cos", "tan", "pi", "e")}
    env.update({"i": 1j, "ln": cmath.log, "log": lambda z, b=10: cmath.log(z) / cmath.log(b), "abs": abs})
    env.update(vals)
    # implicit multiplication of variable followed by variable/paren
    for vname in vals:
        e = re.sub(rf"(?<![a-zA-Z]){vname}(?=[a-z(])", f"{vname}*", e)
    return eval(e, {"__builtins__": {}}, env)


def same(a, b, tol=1e-9):
    return abs(complex(a) - complex(b)) < tol * max(1, abs(complex(b)))


def eqcheck(s1, s2, var="x", pts=(-2.3, -0.7, 0.4, 1.9, 3.1)):
    """Assert two text expressions agree at sample points."""
    for p in pts:
        a, b = peval(s1, **{var: p}), peval(s2, **{var: p})
        assert same(a, b, 1e-7), (s1, s2, p, a, b)
    return True


def sel_auto(B, S, lvl, prompt, cands, pred, steps, tags=(), diagram=None):
    """Select-all whose correct options are decided by a computed predicate (verification built in)."""
    cands = list(dict.fromkeys(cands))
    right = [c for c in cands if pred(c)]; wrong = [c for c in cands if not pred(c)]
    return B.sel(S, lvl, prompt, right, wrong, steps, tags=tags, diagram=diagram)


def is_equiv(target, var="x"):
    return lambda s: all(same(peval(s, **{var: p}), peval(target, **{var: p}), 1e-7) for p in (-2.3, -0.7, 0.4, 1.9, 3.1))


def is_zero_of(f):
    return lambda s: abs(f(complex(peval(s)))) < 1e-9


def root_of(lin):
    """'x - 3' / '2x + 1' / 'x' → root as Fraction."""
    s = lin.replace(" ", "").strip("()")
    if s == "x": return F(0)
    a, b = re.match(r"^(\d*)x([+-]\d+)$", s).groups()
    return -F(int(b), int(a) if a else 1)


def pt(a, b):
    return f"({fr(a) if not isinstance(a, float) else dec(a)}, {fr(b) if not isinstance(b, float) else dec(b)})"


def lb(b):
    """'log₂' for integer bases, 'log_(1/2)' otherwise; base 10 → 'log'."""
    b = F(b)
    if b == 10: return "log"
    return "log" + str(b.numerator).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")) if b.denominator == 1 else f"log_({fr(b)})"


def reduce_rat(N, D):
    """Cancel common factors of N/D; return integer-coefficient (N', D') with D' having positive leading coefficient."""
    from collections import Counter
    nr, nrest = N.rational_roots(); dr, drest = D.rational_roots()
    cn, cd = Counter(nr), Counter(dr); com = cn & cd
    Nn = P.roots(list((cn - com).elements())) * nrest
    Dd = P.roots(list((cd - com).elements())) * drest
    den = math.lcm(*[c.denominator for c in Nn.c + Dd.c])
    Nn, Dd = Nn * den, Dd * den
    g = math.gcd(*[int(c) for c in Nn.c + Dd.c if c != 0])
    Nn, Dd = Nn * F(1, g), Dd * F(1, g)
    if Dd.lead < 0: Nn, Dd = -Nn, -Dd
    return Nn, Dd


_PROD = re.compile(r"^-?\d*(?:x[²³⁴]?|\([^()]+\)[²³⁴]?)+$")


def wrapn(s):
    """Numerator: parentheses only when it is a sum."""
    return s if (_PROD.match(s) or re.fullmatch(r"-?\d+", s)) else f"({s})"


def wrapd(s):
    """Denominator: no parentheses only for a single factor."""
    return s if re.fullmatch(r"x[²³⁴]?|\d+|\([^()]+\)[²³⁴]?", s) else f"({s})"


def rats(N, D, factored=True):
    n = factor_str(N) if factored else pstr(N); d = factor_str(D) if factored else pstr(D)
    if D == P([1]):
        return n[1:-1] if (n.startswith("(") and n.endswith(")") and n.count("(") == 1) else n
    return f"{wrapn(n)}/{wrapd(d)}"
