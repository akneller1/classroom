"""Independent checks added for the Algebra 2 top-up (registered into the shared verifier).
Like hschecks.py, nothing here imports the authoring families: each check re-derives the answer
from the expression shown to the student."""
import re
import sympy as sp
from checks_custom import reg
import hschecks as HC

X = HC.X


@reg
def extreme_word(chk, text):
    """'minimum -3' / 'maximum 5' for the quadratic shown."""
    m = re.fullmatch(r"(minimum|maximum) (-?\d+(?:/\d+)?)", str(text).strip())
    if not m:
        return False
    f = HC.P(chk["expr"])
    a = sp.Poly(f, X).LC()
    v = f.subs(X, sp.solve(sp.diff(f, X), X)[0])
    return m.group(1) == ("minimum" if a > 0 else "maximum") and HC._num_eq(HC.P(m.group(2)), v)


@reg
def disc_word(chk, text):
    f = HC.P(chk["expr"])
    d = sp.discriminant(f, X)
    want = "two real solutions" if d > 0 else "one real solution" if d == 0 else "two complex (non-real) solutions"
    return str(text).strip() == want


@reg
def divres(chk, text):
    """'quotient, remainder R' for f ÷ d: checks f = d·q + R with deg R < deg d."""
    m = re.fullmatch(r"(.+), remainder (-?\d+)", str(text).strip())
    if not m:
        return False
    q, R = HC.P(m.group(1)), int(m.group(2))
    f, d = HC.P(chk["f"]), HC.P(chk["d"])
    return sp.expand(d * q + R - f) == 0


@reg
def multiplicity(chk, text):
    f, z = HC.P(chk["f"]), sp.Integer(chk["z"])
    k = 0
    while sp.expand(f).subs(X, z) == 0:
        f = sp.cancel(f / (X - z))
        k += 1
    return str(text).strip() == str(k)


@reg
def cross_touch(chk, text):
    f, z = HC.P(chk["f"]), sp.Integer(chk["z"])
    k = 0
    while sp.expand(f).subs(X, z) == 0:
        f = sp.cancel(f / (X - z))
        k += 1
    if k == 0:
        return False
    return str(text).strip() == ("touches (bounces)" if k % 2 == 0 else "crosses")


@reg
def end_behavior(chk, text):
    f = HC.P(chk["f"])
    w = lambda v: "∞" if v == sp.oo else "-∞"
    want = f"As x → ∞, f(x) → {w(sp.limit(f, X, sp.oo))}; as x → -∞, f(x) → {w(sp.limit(f, X, -sp.oo))}"
    return str(text).strip() == want


@reg
def pos_equiv(chk, text):
    """Equivalent to the expression shown for x > 0 (rational exponents and radicals)."""
    t = re.sub(r"^[A-Za-z]\s*=\s*", "", str(text).strip())
    return HC._pos_eq(HC.P(t), HC.P(chk["expr"]))


@reg
def extraneous_root(chk, text):
    """The candidate that does NOT satisfy the original equation."""
    m = re.fullmatch(r"x = (-?\d+)", str(text).strip())
    if not m:
        return False
    v = int(m.group(1))
    if v not in chk["cands"]:
        return False
    L, R = HC.P(chk["lhs"]), HC.P(chk["rhs"])
    return not HC._num_eq(L.subs(X, v), R.subs(X, v))


@reg
def growth_word(chk, text):
    m = re.fullmatch(r"(growth|decay), (\d+(?:\.\d+)?)%", str(text).strip())
    if not m:
        return False
    b = sp.nsimplify(chk["b"])
    return m.group(1) == ("growth" if b > 1 else "decay") and sp.nsimplify(m.group(2)) == abs(b - 1) * 100


@reg
def exp_form(chk, text):
    """text is b^e = v (superscript exponent), equivalent to log_b(v) = e."""
    m = re.fullmatch(r"(\d+)([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+) = (.+)", str(text).strip())
    if not m:
        return False
    b, e = int(m.group(1)), int(m.group(2).translate(str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789")))
    return b == chk["b"] and e == chk["e"] and HC._num_eq(HC.P(m.group(3)), sp.Integer(b) ** e)


@reg
def inverse_of(chk, text):
    t = re.sub(r"^f⁻¹\(x\)\s*=\s*", "", str(text).strip())
    F_, G_ = HC.P(chk["f"]), HC.P(t)
    return HC._num_eq(F_.subs(X, G_), X) and HC._num_eq(G_.subs(X, F_), X)


@reg
def approx_eq(chk, text):
    """'x ≈ 2.509': the value of chk['code'] rounded to chk['places']."""
    m = re.fullmatch(r"[a-zA-Z] ≈ (-?\d+(?:\.\d+)?)", str(text).strip())
    if not m:
        return False
    v = float(sp.N(eval(chk["code"], HC.ns()), 30))
    return HC.C.round_text(v, chk["places"]) == m.group(1)


@reg
def vas(chk, text):
    """'x = a and x = b': every vertical asymptote of the function shown (denominator zero, not removable)."""
    items = [s.strip() for s in str(text).split(" and ")]
    got = []
    for it in items:
        m = re.fullmatch(r"x = (-?\d+)", it)
        if not m:
            return False
        got.append(int(m.group(1)))
    f = sp.cancel(HC.P(chk["f"]))
    want = sorted(int(s) for s in sp.solve(sp.denom(sp.together(f)), X))
    return sorted(got) == want


N_ = HC.N_


def _seq_rhs(text):
    t = re.sub(r"^a[ₙn]\s*=\s*", "", str(text).strip())
    return HC.P(t)


@reg
def seq_expr(chk, text):
    if not re.match(r"^a[ₙn]\s*=", str(text).strip()):
        return False
    want = HC.P(chk["expr"])
    got = _seq_rhs(text)
    return all(sp.simplify(got.subs(N_, v) - want.subs(N_, v)) == 0 for v in range(1, 8))


@reg
def recur(chk, text):
    """Re-applies the recursive rule shown (aₙ = m·aₙ₋₁ + d) from a₁."""
    rule = chk["rule"].replace("aₙ = ", "").replace("aₙ₋₁", "*P")
    rule = re.sub(r"^\*P", "P", rule)
    rule = re.sub(r"^-\*P", "-P", rule)
    v = sp.Integer(chk["a1"])
    for _ in range(chk["k"] - 1):
        v = sp.sympify(rule.replace("P", f"({v})"))
    return str(text).strip() == str(v)


@reg
def sigma_eq(chk, text):
    m = re.fullmatch(r"Σ \(k = (-?\d+) to (\d+)\) \((.+)\)", str(text).strip())
    if not m:
        return False
    K = HC.K
    got = sp.summation(HC.P(m.group(3)), (K, int(m.group(1)), int(m.group(2))))
    want = sp.summation(sp.sympify(chk["expr"], locals={"k": K}), (K, chk["lo"], chk["hi"]))
    # the same terms in the same order: compare the first and last terms and the count
    ok_terms = int(m.group(2)) - int(m.group(1)) == chk["hi"] - chk["lo"] and \
        HC.P(m.group(3)).subs(K, int(m.group(1))) == sp.sympify(chk["expr"], locals={"k": K}).subs(K, chk["lo"])
    return ok_terms and got == want


@reg
def inf_geo(chk, text):
    a1, r = sp.nsimplify(chk["a1"]), sp.nsimplify(chk["r"])
    t = str(text).strip()
    if abs(r) >= 1:
        return t == "The series diverges (no sum)."
    try:
        return HC._num_eq(HC.P(t), a1 / (1 - r))
    except Exception:
        return False


@reg
def circle_part(chk, text):
    e = HC.P(chk["e"])
    a = sp.Poly(e, X, HC.Y).coeff_monomial(X ** 2)
    h = -sp.Poly(e, X, HC.Y).coeff_monomial(X) / (2 * a)
    k = -sp.Poly(e, X, HC.Y).coeff_monomial(HC.Y) / (2 * a)
    r2 = (h * h + k * k) - e.subs({X: 0, HC.Y: 0}) / a
    t = str(text).strip()
    if chk["part"] == "center":
        g = HC.P_tuple(t)
        return len(g) == 2 and HC._num_eq(g[0], h) and HC._num_eq(g[1], k)
    return HC._num_eq(HC.P(t), sp.sqrt(r2))


@reg
def trig_from(chk, text):
    gv, q = sp.nsimplify(chk["gv"]), chk["q"]
    sx, sy = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}[q]
    if chk["given"] == "sin":
        s, c = gv, sx * sp.sqrt(1 - gv ** 2)
    else:
        c, s = gv, sy * sp.sqrt(1 - gv ** 2)
    if sp.sign(s) not in (sy, 0) or sp.sign(c) not in (sx, 0):
        return False
    want = {"sin": s, "cos": c, "tan": s / c}[chk["ask"]]
    try:
        return HC._num_eq(HC.P(str(text)), want)
    except Exception:
        return False


@reg
def trig_ident(chk, text):
    TH = HC.TH
    conv = lambda t: HC.P(t.replace("sin²θ", "(sin(θ))²").replace("cos²θ", "(cos(θ))²").replace("sin θ", "sin(θ)").replace("cos θ", "cos(θ)").replace("tan θ", "tan(θ)"))
    try:
        return HC._num_eq(conv(chk["e"]), conv(str(text)))
    except Exception:
        return False


@reg
def trig_solutions(chk, text):
    F_ = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan}[chk["func"]]
    v = HC.P(chk["v"])
    want = sorted(sp.solveset(sp.Eq(F_(X), v), X, sp.Interval.Ropen(0, 2 * sp.pi)), key=float)
    items = [s.strip() for s in str(text).split(" or ")]
    got = []
    for it in items:
        m = re.fullmatch(r"x = (.+)", it)
        if not m:
            return False
        t = m.group(1)
        if chk["deg"] != t.endswith("°"):
            return False
        got.append(HC.P(t))
    if len(got) != len(want):
        return False
    return all(any(HC._num_eq(g, w) for g in got) for w in want)


@reg
def moe_interval(chk, text):
    m = re.fullmatch(r"(-?\d+(?:\.\d)?)% to (-?\d+(?:\.\d)?)%", str(text).strip())
    if not m:
        return False
    e = 100 / sp.sqrt(chk["n"])
    rt = lambda v: HC.C.round_text(float(sp.N(v, 30)), 1)
    return m.group(1) == rt(chk["p"] - e) and m.group(2) == rt(chk["p"] + e)


@reg
def pct_round(chk, text):
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)%", str(text).strip())
    if not m:
        return False
    v = float(sp.N(eval(chk["code"], HC.ns()), 30)) * 100
    return HC.C.round_text(v, chk["places"]) == m.group(1)
