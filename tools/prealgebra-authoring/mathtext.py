"""Independent reader for the student-facing math text (verification only).

Written separately from the authoring helpers: it parses the strings exactly as a
student sees them (unicode superscripts, √, ∛, π, ·, ×, ÷, implicit multiplication,
a/b fractions, mixed numbers, thousands commas) and evaluates them with exact
Fractions where possible.
"""
import math, re
from fractions import Fraction as F

SUPS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
SUP2 = {c: d for c, d in zip(SUPS, "0123456789-")}


class ParseError(Exception):
    pass


def _prep(s):
    s = str(s).replace("−", "-").replace("–", "-").replace("×", "*").replace("·", "*").replace("÷", " DIV ")
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)
    # superscript runs -> ^(..)
    s = re.sub("[" + SUPS + "]+", lambda m: "^(" + "".join(SUP2[c] for c in m.group(0)) + ")", s)
    s = re.sub(r"(\d+) (\d+)/(\d+)", r"(\1+\2/\3)", s)   # mixed number 2 1/3
    return s


TOK = re.compile(r"\s*(DIV|\d+\.\d+|\d+|\.\d+|[A-Za-z]|π|√|∛|\^|\*|/|\+|-|\(|\)|\[|\])")


def tokenize(s):
    s = _prep(s)
    pos, out = 0, []
    while pos < len(s):
        if s[pos].isspace():
            pos += 1
            continue
        m = TOK.match(s, pos)
        if not m:
            raise ParseError(f"bad char {s[pos]!r} in {s!r}")
        out.append(m.group(1))
        pos = m.end()
    return out


def is_exact(v):
    return isinstance(v, F)


def _num(v):
    return v if isinstance(v, (F, float)) else F(v)


def mul(a, b):
    return a * b if is_exact(a) and is_exact(b) else float(a) * float(b)


def div(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b if is_exact(a) and is_exact(b) else float(a) / float(b)


def add(a, b):
    return a + b if is_exact(a) and is_exact(b) else float(a) + float(b)


def power(a, b):
    if is_exact(b) and b.denominator == 1:
        if is_exact(a):
            if a == 0 and b < 0:
                raise ZeroDivisionError
            return a ** int(b)
        return float(a) ** int(b)
    return float(a) ** float(b)


def root(a, n):
    if is_exact(a):
        if n == 3:
            s = -1 if a < 0 else 1
            num = round(abs(a.numerator) ** (1 / 3))
            den = round(a.denominator ** (1 / 3))
            for nn in (num - 1, num, num + 1):
                for dd in (den - 1, den, den + 1):
                    if nn >= 0 and dd > 0 and F(nn, dd) ** 3 == abs(a):
                        return s * F(nn, dd)
            return s * abs(float(a)) ** (1 / 3)
        if a < 0:
            raise ValueError("sqrt of negative")
        num, den = math.isqrt(a.numerator), math.isqrt(a.denominator)
        if num * num == a.numerator and den * den == a.denominator:
            return F(num, den)
        return math.sqrt(a)
    if n == 3:
        return math.copysign(abs(a) ** (1 / 3), a)
    return math.sqrt(a)


class Parser:
    def __init__(self, toks, env):
        self.t, self.i, self.env = toks, 0, env

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self, x=None):
        tok = self.peek()
        if x is not None and tok != x:
            raise ParseError(f"expected {x} got {tok}")
        self.i += 1
        return tok

    def expr(self):
        v = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            w = self.term()
            v = add(v, w) if op == "+" else add(v, mul(F(-1), w))
        return v

    def starts_primary(self, tok):
        return tok is not None and tok != "DIV" and (tok[0].isdigit() or tok[0] == "." or tok.isalpha() or tok in ("(", "√", "∛", "π", "["))

    def term(self):
        v = self.unary()
        while True:
            tok = self.peek()
            if tok == "*":
                self.take()
                v = mul(v, self.unary())
            elif tok == "DIV":
                self.take()
                v = div(v, self.unary())
            elif self.starts_primary(tok):
                v = mul(v, self.frac())
            else:
                return v

    def unary(self):
        if self.peek() == "-":
            self.take()
            return mul(F(-1), self.unary())
        if self.peek() == "+":
            self.take()
            return self.unary()
        return self.frac()

    def frac(self):
        """A stacked fraction binds its neighbouring atoms (as the site's display does)."""
        v = self.pw()
        while self.peek() == "/":
            self.take()
            if self.peek() == "-":
                self.take()
                v = div(v, mul(F(-1), self.pw()))
            else:
                v = div(v, self.pw())
        return v

    def pw(self):
        b = self.primary()
        if self.peek() == "^":
            self.take()
            neg = False
            while self.peek() in ("-", "+"):
                neg ^= self.take() == "-"
            e = self.pw()
            return power(b, mul(F(-1), e) if neg else e)
        return b

    def primary(self):
        tok = self.take()
        if tok is None:
            raise ParseError("unexpected end")
        if tok in ("(", "["):
            v = self.expr()
            self.take(")" if tok == "(" else "]")
            return v
        if tok == "√":
            return root(self.pw(), 2)
        if tok == "∛":
            return root(self.pw(), 3)
        if tok == "π":
            return math.pi
        if tok[0].isdigit() or tok[0] == ".":
            return F(tok)
        if tok.isalpha():
            if tok == "DIV" or tok not in self.env:
                raise ParseError(f"unknown variable {tok}")
            return self.env[tok]
        raise ParseError(f"unexpected {tok}")


def ev(s, env=None):
    p = Parser(tokenize(s), env or {})
    v = p.expr()
    if p.peek() is not None:
        raise ParseError(f"trailing {p.peek()} in {s!r}")
    return v


def same(a, b, tol=1e-9):
    if is_exact(a) and is_exact(b):
        return a == b
    return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(a)), abs(float(b)))


UNIT_WORDS = r"(?:square|cubic|sq\.?|cu\.?)?\s*(?:units?|feet|foot|ft|inches|inch|in|yards?|yd|miles?|mi|meters?|m|centimeters?|cm|millimeters?|mm|kilometers?|km|degrees|°C|°F|°|dollars|hours?|minutes?|seconds?|people|students|cups|gallons?|pounds?|liters?|L|mL|ounces?|oz|games?|tickets?|items?|books?|days?|weeks?|years?|points?|songs?)[²³]?"


def strip_units(s):
    s = str(s).strip().rstrip(".")
    s = re.sub(r"^(?:about|approximately|≈)\s*", "", s)
    s = s.replace("$", "")
    for _ in range(3):
        s2 = re.sub(r"\s*\b" + UNIT_WORDS + r"\s*$", "", s)
        s2 = re.sub(r"\s*°[CF]?\s*$", "", s2)
        s2 = re.sub(r"(?<=[\d⁰¹²³⁴⁵⁶⁷⁸⁹)π])\s*%\s*$", "", s2)
        s2 = re.sub(r"(?<=[\d⁰¹²³⁴⁵⁶⁷⁸⁹)π])\s+[a-zA-Z]{2,}(?:\s+[a-zA-Z]+)*[²³]?\s*$", "", s2)
        if s2 == s:
            break
        s = s2
    return s.strip()


def strip_lhs(s):
    """'x = 5' -> '5'; 'f(3) = 7' -> '7'."""
    s = str(s).strip()
    m = re.match(r"^[A-Za-z](?:\([^)]*\))?\s*=\s*(.+)$", s)
    return m.group(1) if m else s


def val(s):
    return ev(strip_units(strip_lhs(s)))


def lin1(fn, var="x"):
    """Treat fn (callable of one Fraction) as linear; return (slope, intercept, is_linear)."""
    f0, f1, f2, f5 = fn(F(0)), fn(F(1)), fn(F(2)), fn(F(5))
    m = f1 - f0 if is_exact(f1) and is_exact(f0) else float(f1) - float(f0)
    lin = same(add(f2, mul(F(-1), f1)), m) and same(add(f5, mul(F(-1), f0)), mul(F(5), m))
    return m, f0, lin


def eq_sides(eq):
    parts = eq.split("=")
    if len(parts) != 2:
        raise ParseError(f"not one equation: {eq}")
    return parts[0], parts[1]


def solve_linear(eq, var="x"):
    """Return ('one', value) | ('none',) | ('all',) by evaluating LHS - RHS at sample points."""
    l, r = eq_sides(eq)
    fn = lambda v: add(ev(l, {var: v}), mul(F(-1), ev(r, {var: v})))
    m, b, ok = lin1(fn, var)
    if not ok:
        raise ParseError("not linear: " + eq)
    if same(m, 0):
        return ("all",) if same(b, 0) else ("none",)
    return ("one", div(mul(F(-1), b), m))


def solve_system(e1, e2):
    rows = []
    for e in (e1, e2):
        l, r = eq_sides(e)
        g = lambda x, y: add(ev(l, {"x": x, "y": y}), mul(F(-1), ev(r, {"x": x, "y": y})))
        c = g(F(0), F(0))
        a = add(g(F(1), F(0)), mul(F(-1), c))
        b = add(g(F(0), F(1)), mul(F(-1), c))
        if not same(g(F(3), F(7)), add(add(mul(F(3), a), mul(F(7), b)), c)):
            raise ParseError("system equation not linear")
        rows.append((a, b, mul(F(-1), c)))
    (a1, b1, c1), (a2, b2, c2) = rows
    det = add(mul(a1, b2), mul(F(-1), mul(a2, b1)))
    if same(det, 0):
        # parallel or same line: check proportional constants
        if same(add(mul(a1, c2), mul(F(-1), mul(a2, c1))), 0) and same(add(mul(b1, c2), mul(F(-1), mul(b2, c1))), 0):
            return ("all",)
        return ("none",)
    x = div(add(mul(c1, b2), mul(F(-1), mul(c2, b1))), det)
    y = div(add(mul(a1, c2), mul(F(-1), mul(a2, c1))), det)
    return ("one", (x, y))


def parse_point(s):
    m = re.match(r"^\s*\(\s*([^,]+?)\s*,\s*([^,]+?)\s*\)\s*$", str(s))
    if not m:
        raise ParseError("not a point: " + str(s))
    return ev(m.group(1)), ev(m.group(2))


def special(s):
    t = str(s).lower().strip().rstrip(".")
    if t in ("no solution", "no solutions"):
        return "none"
    if t in ("infinitely many solutions", "infinitely many", "all real numbers"):
        return "all"
    return None
