"""Question families for the Precalculus audit, batch P4 (2026-11-18): the standards-gap skills.

A family is fn(r, L) -> I(prompt, answer, steps, wrongs, check, fam), as in
tools/audit-gap-skills-20261116/core.py (L: 0 Support/cp2, 1 Standard/cp1, 2 Advanced/honors).
`check` holds the parameters; verify.py recomputes every answer, option and student answer from them with
its own formulas and confirms that check["show"] text is printed in the prompt.
Families marked mc_only have worded answers and appear only as multiple choice.
"""
import math, os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "audit-gap-skills-20261116"))
from core import I as _I, Reject, need, ri  # noqa: E402,F401
from fmt import sup, num, coef, join, poly  # noqa: E402


def I(prompt, answer, steps, wrongs, check, fam):
    """core.I, dropping distractors that could not be written exactly (None)."""
    return _I(prompt, answer, steps, [w for w in wrongs if w[0] is not None], check, fam)


def mc_only(fn):
    fn.mc_only = True
    return fn


def nz(r, lo, hi):
    v = 0
    while v == 0:
        v = r.randint(lo, hi)
    return v


def lf(c, k=1):
    """Linear factor x + c as text: x - 3, x + 2, x."""
    return "x" if c == 0 else (f"x + {c}" if c > 0 else f"x - {-c}")


# ------------------------------------------------------------------ surd / complex display
def surd(c, k):
    """c·√k with c a Fraction: 3, -2√3, (3√2)/2, -(√3)/2, 5/2."""
    c = F(c)
    if c == 0:
        return "0"
    if k == 1:
        return num(c)
    s = "-" if c < 0 else ""
    a = abs(c)
    root = f"√{k}"
    if a.denominator == 1:
        return s + ("" if a == 1 else str(a.numerator)) + root
    top = root if a.numerator == 1 else f"{a.numerator}{root}"
    return f"{s}({top})/{a.denominator}"


def imag(c, k):
    """Imaginary term c·√k·i in the bank's style: 3i, -i, 2√3i, (1/2)i, ((√3)/2)i."""
    c = F(c)
    if k == 1:
        if c == 1:
            return "i"
        if c == -1:
            return "-i"
        return (num(c) + "i") if c.denominator == 1 else (("-" if c < 0 else "") + f"({num(abs(c))})i")
    t = surd(abs(c), k)
    t = t if abs(c).denominator == 1 else f"({t})"
    return ("-" if c < 0 else "") + t + "i"


def cx(re_, im_, kre=1, kim=1):
    """a + bi text from real part re_·√kre and imaginary part im_·√kim."""
    parts = []
    if F(re_) != 0:
        parts.append(surd(re_, kre))
    if F(im_) != 0:
        parts.append(imag(im_, kim))
    return join(parts) if parts else "0"


def cxz(z):
    """Gaussian rational (Fraction re, Fraction im) as text."""
    return cx(z[0], z[1])


def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def zin(a, b):
    """Prompt text for a + bi with integer parts: 3 - 4i, -2 + i, 5i, 7."""
    return cx(a, b)


# exact (cos, sin) of special angles in degrees: ((c, k), (s, k)) meaning c·√k
TRIG = {0: ((1, 1), (0, 1)), 30: ((F(1, 2), 3), (F(1, 2), 1)), 45: ((F(1, 2), 2), (F(1, 2), 2)), 60: ((F(1, 2), 1), (F(1, 2), 3)),
        90: ((0, 1), (1, 1))}


def trig(deg):
    deg %= 360
    if deg <= 90:
        (c, kc), (s, ks) = TRIG[deg]
    elif deg <= 180:
        (c, kc), (s, ks) = TRIG[180 - deg]
        c = -F(c)
    elif deg <= 270:
        (c, kc), (s, ks) = TRIG[deg - 180]
        c, s = -F(c), -F(s)
    else:
        (c, kc), (s, ks) = TRIG[360 - deg]
        s = -F(s)
    return (F(c), kc), (F(s), ks)


def special(deg):
    return deg % 360 in {0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330}


def polar_rect(r, deg):
    """r(cos deg + i sin deg) as exact a + bi text (None when deg is not a special angle)."""
    if not special(deg):
        return None
    (c, kc), (s, ks) = trig(deg)
    return cx(F(r) * c, F(r) * s, kc, ks)


def ptext(r, deg):
    rr = num(r) if F(r).denominator == 1 else f"({num(r)})"
    return f"{rr}(cos {deg}° + i sin {deg}°)"


# ================================================================== functions: rational expressions (A-APR.D.6, D.7)
def ra_simplify(r, L):
    p, q, s = nz(r, -7, 7), nz(r, -7, 7), nz(r, -7, 7)
    need(len({p, q, s}) == 3)
    a = 1 if L < 2 else r.choice([2, 3])
    num_ = poly({2: a, 1: a * (p + q), 0: a * p * q})
    den = poly({2: 1, 1: p + s, 0: p * s})
    lead = "" if a == 1 else str(a)
    ans = f"{lead}({lf(q)})/({lf(s)})"
    prompt = f"Simplify ({num_})/({den}). State any restrictions separately; give only the simplified expression."
    steps = [f"Factor: numerator {lead}({lf(p)})({lf(q)}), denominator ({lf(p)})({lf(s)}).",
             f"Cancel the common factor ({lf(p)}) (x ≠ {-p}).", f"= {ans}."]
    wr = [(f"{lead}({lf(p)})/({lf(s)})", "cancelled the wrong factor"),
          (num(F(a * q, s)), "cancelled the x terms as if they were factors"),
          (f"{lead}({lf(q)})/({lf(p)})", "cancelled a factor from the numerator with the wrong factor of the denominator"),
          (f"{lead}({lf(-q)})/({lf(-s)})", "used the wrong signs when factoring")]
    return I(prompt, ans, steps, wr, dict(k="ra_simplify", a=a, p=p, q=q, s=s, show=[num_, den]), "ra_simplify")


def ra_add(r, L):
    a, b = nz(r, -6, 6), nz(r, -6, 6)
    p, q = nz(r, -6, 6), nz(r, -6, 6)
    need(p != q and a + b != 0)
    x0 = ri(r, -3, 3)
    need((x0 + p) * (x0 + q) != 0)
    op = "+" if L < 2 else r.choice(["+", "-"])
    b2 = b if op == "+" else -b
    A, B = a + b2, a * q + b2 * p
    need(A != 0 or B != 0)
    top = join([coef(A, "x") if A else "", num(B) if B else ""])
    ans = f"({top})/(({lf(p)})({lf(q)}))"
    bb = num(abs(b)) if b > 0 else f"({b})"
    prompt = f"Write as a single fraction: {a}/({lf(p)}) {op} {b}/({lf(q)}). Leave the denominator in factored form."
    if b < 0:
        prompt = f"Write as a single fraction: {a}/({lf(p)}) {op} ({b})/({lf(q)}). Leave the denominator in factored form."
    steps = [f"Common denominator: ({lf(p)})({lf(q)}).",
             f"Numerator: {a}({lf(q)}) {op} {bb}({lf(p)}) = {top}.", f"= {ans}."]
    wtop = join([coef(a + b2, "x") if a + b2 else "", num(a * p + b2 * q) if a * p + b2 * q else ""])
    wr = [(f"({num(a + b2)})/(2x + {p + q})" if p + q > 0 else f"({num(a + b2)})/(2x - {-(p + q)})", "added numerators and denominators"),
          (f"({num(a + b2)})/(({lf(p)})({lf(q)}))", "added the numerators without multiplying by the missing factors"),
          (f"({wtop})/(({lf(p)})({lf(q)}))", "multiplied each numerator by its own denominator's constant"),
          (f"({join([coef(a - b2, 'x') if a - b2 else '', num(a * q - b2 * p) if a * q - b2 * p else ''])})/(({lf(p)})({lf(q)}))", "used the wrong sign for the second fraction")]
    return I(prompt, ans, steps, wr, dict(k="ra_add", a=a, b=b2, p=p, q=q, show=[f"{a}/({lf(p)})", f"/({lf(q)})"]), "ra_add")


def pf_coef(r, L):
    """(Ax + B)/((x - p)(x - q)) = a/(x - p) + b/(x - q): find a."""
    a, b = nz(r, -6, 6), nz(r, -6, 6)
    p, q = ri(r, -5, 5), ri(r, -5, 5)
    need(p != q)
    A, B = a + b, -(a * q + b * p)
    need(A != 0)
    top = join([coef(A, "x"), num(B) if B else ""])
    den = poly({2: 1, 1: -(p + q), 0: p * q}) if L > 0 else f"({lf(-p)})({lf(-q)})"
    ask = r.choice(["A", "B"])
    ans = a if ask == "A" else b
    prompt = f"Find the partial fraction decomposition ({top})/({den}) = A/({lf(-p)}) + B/({lf(-q)}). What is {ask}?"
    steps = ([f"Factor the denominator: ({lf(-p)})({lf(-q)})."] if L > 0 else []) + [
        f"Multiply through: {top} = A({lf(-q)}) + B({lf(-p)}).",
        f"x = {p}: {num(A * p + B)} = A({p - q}), so A = {a}.",
        f"x = {q}: {num(A * q + B)} = B({q - p}), so B = {b}.", f"{ask} = {ans}."]
    other = b if ask == "A" else a
    wr = [(str(other), "gave the other constant"), (str(-ans), "made a sign error substituting the root"),
          (str(A), "used the coefficient of x"), (str(B if B != ans else A + 1), "used the constant term")]
    return I(prompt, str(ans), steps, wr, dict(k="pf_coef", top=(A, B), p=p, q=q, ask=ask, show=[top]), "pf_coef")


def ra_excluded(r, L):
    p, q, s = ri(r, -8, 8), ri(r, -8, 8), ri(r, -8, 8)
    need(p < q and p + q != 0 and s not in (p, q))
    den = poly({2: 1, 1: -(p + q), 0: p * q})
    prompt = f"For what values of x is ({lf(-s)})/({den}) undefined?"
    ans = f"x = {p} or x = {q}"
    steps = [f"The expression is undefined where the denominator is 0: {den} = ({lf(-p)})({lf(-q)}) = 0.", f"{ans}."]
    wr = [(f"x = {-p} or x = {-q}", "used the opposite signs of the factors"), (f"x = {s}", "set the numerator equal to 0"),
          (f"x = {p} or x = {q} or x = {s}", "included the zero of the numerator"), (f"x = {p * q}", "used the constant term")]
    return I(prompt, ans, steps, wr, dict(k="ra_excluded", p=p, q=q, s=s, show=[den]), "ra_excluded")


def ra_value(r, L):
    """Evaluate a complex fraction / rational expression after simplifying at a removable point? keep: divide."""
    p, q = nz(r, -6, 6), nz(r, -6, 6)
    need(p != q and p != -q)
    x0 = ri(r, -4, 6)
    need(x0 + q != 0 and x0 - p != 0 and x0 + p != 0)
    n1 = poly({2: 1, 0: -p * p})
    prompt = f"Simplify ({n1})/({lf(q)}) ÷ ({lf(-p)})/({lf(q)}), then evaluate the result at x = {x0}."
    ans = x0 + p
    steps = [f"Multiply by the reciprocal: ({n1})/({lf(q)}) · ({lf(q)})/({lf(-p)}).",
             f"{n1} = ({lf(-p)})({lf(p)}); cancel ({lf(-p)}) and ({lf(q)}): the result is {lf(p)}.",
             f"At x = {x0}: {x0} + ({p}) = {ans}."]
    wr = [(str(x0 - p), "factored the difference of squares with the wrong sign"),
          (num(F((x0 * x0 - p * p) * (x0 - p), (x0 + q) ** 2)), "multiplied instead of dividing"),
          (str(x0 * x0 - p * p), "dropped the denominators"), (str(ans + 1), "made an arithmetic slip")]
    return I(prompt, str(ans), steps, wr, dict(k="ra_value", p=p, q=q, x0=x0, show=[n1, f"x = {x0}"]), "ra_value")


# ================================================================== functions: verifying inverses (F-BF.B.4b–d)
def inv_table(r, L):
    x_0 = ri(r, -3, 0)
    xs = [x_0 + i for i in range(5)]
    m, b = nz(r, -4, 5), ri(r, -9, 9)
    if L == 2:
        a = r.choice([1, 2]) * r.choice([1, -1])
        ys = [a * x ** 3 + b for x in xs]
    else:
        ys = [m * x + b for x in xs]
    need(len(set(ys)) == len(ys))
    j = ri(r, 0, 4)
    v = ys[j]
    k = ri(r, 0, 4)
    rows = "x: " + ", ".join(map(str, xs)) + "\nf(x): " + ", ".join(map(str, ys))
    prompt = f"The table shows values of the one-to-one function f.\n{rows}\nFind f⁻¹({v})."
    steps = [f"f⁻¹({v}) is the input of f whose output is {v}.", f"From the table, f({xs[j]}) = {v}, so f⁻¹({v}) = {xs[j]}."]
    wr = [(str(ys[xs.index(v)]) if v in xs else str(ys[k] if ys[k] != xs[j] else ys[(k + 1) % 5]), "evaluated f instead of f⁻¹"),
          (num(F(1, v)) if v else "1", "took the reciprocal of the value"), (str(-xs[j]) if xs[j] else "1", "used the opposite of the input"),
          (str(xs[(j + 1) % 5]), "read the neighbouring column")]
    return I(prompt, str(xs[j]), steps, wr, dict(k="inv_table", xs=xs, ys=ys, v=v, show=[", ".join(map(str, ys))]), "inv_table")


def inv_restrict_value(r, L):
    h, k = ri(r, -6, 6), ri(r, -9, 9)
    n = ri(r, 1, 6)
    a = 1 if L < 2 else r.choice([2, 3])
    side = r.choice([">=", "<="]) if L > 0 else ">="
    c = k + a * n * n
    need(h != 0)
    inner = f"x - {h}" if h > 0 else f"x + {-h}"
    lead = "" if a == 1 else str(a)
    f = f"{lead}({inner})² " + (f"+ {k}" if k >= 0 else f"- {-k}")
    dom = f"x ≥ {h}" if side == ">=" else f"x ≤ {h}"
    ans = h + n if side == ">=" else h - n
    prompt = f"f(x) = {f} with domain {dom} has an inverse function. Find f⁻¹({c})."
    steps = [f"Solve f(x) = {c}: {lead}({inner})² = {c - k}" + (f", so ({inner})² = {n * n}" if a > 1 else "") + ".",
             f"{inner} = ±{n}, so x = {h + n} or x = {h - n}.",
             f"Only x = {ans} is in the domain {dom}, so f⁻¹({c}) = {ans}."]
    wr = [(str(2 * h - ans), "used the solution outside the restricted domain"), (str(n), "forgot to add back the horizontal shift"),
          (str(a * (c - h) ** 2 + k), "evaluated f instead of f⁻¹"), (num(F(c - k, a)), "did not take the square root"),
          (str(-ans) if ans else str(h + 2 * n), "made a sign error with the shift"), (str(ans + n), "added the root twice")]
    return I(prompt, str(ans), steps, wr, dict(k="inv_restrict_value", a=a, h=h, kk=k, side=side, c=c, show=[f, dom]), "inv_restrict_value")


def inv_rational(r, L):
    a, b, c = nz(r, -5, 5), ri(r, -9, 9), ri(r, -5, 5)
    need(-a * c - b != 0)  # not constant
    x0 = ri(r, -6, 6)
    need(x0 != c)
    v = F(a * x0 + b, x0 - c)
    need(v.denominator == 1 and v != a)
    f = f"({join([coef(a, 'x'), num(b) if b else ''])})/({lf(-c)})"
    prompt = f"f(x) = {f}. Find f⁻¹({num(v)})."
    steps = [f"Solve {f} = {num(v)}: {join([coef(a, 'x'), num(b) if b else ''])} = {num(v)}({lf(-c)}).",
             f"{coef(a - v, 'x')} = {num(-v * c - b)}, so x = {x0}.", f"f⁻¹({num(v)}) = {x0}."]
    fv = F(a * v + b, v - c) if v != c else None
    wr = [(num(fv) if fv is not None else "0", "evaluated f instead of f⁻¹"), (num(F(1, v)) if v else "1", "took the reciprocal of the output"),
          (str(-x0) if x0 else "1", "made a sign error when isolating x"), (str(x0 + 1), "made an arithmetic slip"),
          (str(x0 - 1), "made an arithmetic slip")]
    return I(prompt, str(x0), steps, wr, dict(k="inv_rational", a=a, b=b, c=c, v=str(v), show=[f]), "inv_rational")


def inv_compose(r, L):
    """f and g are inverses: f(g(x)) = x. Find the missing constant."""
    m = nz(r, -5, 5)
    need(abs(m) > 1)
    b = nz(r, -9, 9)
    if L == 2:
        f = f"{m}x³ " + (f"+ {b}" if b > 0 else f"- {-b}")
        g = f"∛((x {'-' if b > 0 else '+'} {abs(b)})/k)"
        ask_note = "Find k so that f(g(x)) = x for all x."
        ans = m
        steps = [f"f(g(x)) = {m}·(x {'-' if b > 0 else '+'} {abs(b)})/k {'+' if b > 0 else '-'} {abs(b)}.",
                 f"This equals x for all x only when {m}/k = 1.", f"k = {m}."]
    else:
        f = f"{m}x " + (f"+ {b}" if b > 0 else f"- {-b}")
        g = f"(x {'-' if b > 0 else '+'} {abs(b)})/k"
        ask_note = "Find k so that f(g(x)) = x for all x."
        ans = m
        steps = [f"f(g(x)) = {m}·(x {'-' if b > 0 else '+'} {abs(b)})/k {'+' if b > 0 else '-'} {abs(b)}.",
                 f"For this to equal x, the {m}/k must be 1 (then the constants cancel).", f"k = {m}."]
    prompt = f"f(x) = {f} and g(x) = {g}. {ask_note}"
    wr = [(num(F(1, m)), "used the reciprocal of the slope"), (str(-m), "changed the sign of the slope"), (str(b), "used the constant term"),
          (str(-b), "used the opposite of the constant term")]
    return I(prompt, str(ans), steps, wr, dict(k="inv_compose", m=m, b=b, cube=(L == 2), show=[f]), "inv_compose")


@mc_only
def inv_which_restrict(r, L):
    h, k = ri(r, -6, 6), ri(r, -9, 9)
    need(h != 0 and h != k and h != -k)
    inner = f"x - {h}" if h > 0 else f"x + {-h}"
    f = f"({inner})² " + (f"+ {k}" if k >= 0 else f"- {-k}")
    ans = f"x ≥ {h}"
    prompt = f"Which domain restriction makes f(x) = {f} one-to-one, so that its inverse is a function?"
    steps = [f"The graph is a parabola with vertex ({h}, {k}).", f"It is one-to-one on either side of the vertex, for example x ≥ {h}."]
    wr = [(f"x ≥ {-h}", "used the opposite of the shift"), (f"x ≥ {k}", "used the vertical shift"), ("x ≥ 0", "used the parent function's restriction"),
          (f"x ≥ {k - h}" if k - h not in (h, -h, k, 0) else f"x ≥ {h + 1 + abs(k)}", "combined the shifts")]
    return I(prompt, ans, steps, wr, dict(k="inv_which_restrict", h=h, kk=k, show=[f]), "inv_which_restrict")


# ================================================================== vectors: conjugates, moduli, quotients (N-CN.A.3)
def cj_product(r, L):
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    z = zin(a, b)
    zc = zin(a, -b)
    prompt = f"z = {z}. Find z · z̄, where z̄ is the complex conjugate of z."
    ans = a * a + b * b
    steps = [f"z̄ = {zc}.", f"z · z̄ = ({z})({zc}) = {a}² + {abs(b)}² = {ans}."]
    wr = [(str(a * a - b * b), "subtracted the squares"), (cx(a * a - b * b, 2 * a * b), "squared z instead"),
          (str(a * a + b * b + 2 * a * b), "added the cross terms"), (f"√{ans}" if math.isqrt(ans) ** 2 != ans else str(math.isqrt(ans)), "gave the modulus")]
    return I(prompt, str(ans), steps, wr, dict(k="cj_product", a=a, b=b, show=[z]), "cj_product")


def cj_quotient(r, L):
    c, d = nz(r, -5, 5), nz(r, -5, 5)
    if L == 0:
        p, q = ri(r, -6, 6), nz(r, -6, 6)
        w = (F(p), F(q))
    else:
        n = c * c + d * d
        p, q = F(ri(r, -9, 9), n if L == 2 else 1), F(nz(r, -9, 9), n if L == 2 else 1)
        w = (p, q)
    top = cmul(w, (F(c), F(d)))
    need(top[0].denominator == 1 and top[1].denominator == 1 and top[0] != 0 and top[1] != 0)
    zt, zb = zin(int(top[0]), int(top[1])), zin(c, d)
    ans = cxz(w)
    prompt = f"Divide ({zt}) ÷ ({zb}). Write the answer in the form a + bi."
    n = c * c + d * d
    nt = cmul((top[0], top[1]), (F(c), F(-d)))
    steps = [f"Multiply the numerator and denominator by the conjugate {zin(c, -d)}.",
             f"Denominator: {c}² + {abs(d)}² = {n}. Numerator: ({zt})({zin(c, -d)}) = {cx(nt[0], nt[1])}.",
             f"({cx(nt[0], nt[1])})/{n} = {ans}."]
    wr = [(cx(top[0] / c, top[1] / d), "divided the real parts and the imaginary parts separately"),
          (cxz((nt[0] / n, -nt[1] / n)), "used the wrong sign on the imaginary part"),
          (cxz(cmul((top[0], top[1]), (F(c), F(-d)))), "forgot to divide by the denominator"),
          (cxz((nt[0] / (c * c - d * d), nt[1] / (c * c - d * d))) if c * c != d * d else cxz((w[1], w[0])), "used c² − d² as the denominator")]
    return I(prompt, ans, steps, wr, dict(k="cj_quotient", t=[int(top[0]), int(top[1])], d=[c, d], show=[zt, zb]), "cj_quotient")


PYTH = [(3, 4), (5, 12), (8, 6), (6, 8), (4, 3), (12, 5), (8, 15), (0, 7), (5, 0), (9, 12), (12, 9), (7, 24), (2, 0), (0, 3)]


def cj_modq(r, L):
    a, b = r.choice(PYTH)
    c, d = r.choice(PYTH)
    need((a, b) != (c, d))
    a, b = a * r.choice([1, -1]), b * r.choice([1, -1])
    c, d = c * r.choice([1, -1]), d * r.choice([1, -1])
    m1, m2 = math.isqrt(a * a + b * b), math.isqrt(c * c + d * d)
    z1, z2 = zin(a, b), zin(c, d)
    op = "÷" if L > 0 else r.choice(["÷", "·"])
    ans = F(m1, m2) if op == "÷" else F(m1 * m2)
    prompt = f"Find |({z1}) {op} ({z2})|."
    steps = [f"|{z1}| = √({a}² + {b}²) = {m1} and |{z2}| = {m2}.",
             f"The modulus of a {'quotient' if op == '÷' else 'product'} is the {'quotient' if op == '÷' else 'product'} of the moduli: {m1} {op} {m2} = {num(ans)}."]
    wr = [(num(F(m1 * m2) if op == "÷" else F(m1, m2)), "used the wrong operation on the moduli"),
          (num(ans * ans), "forgot the square root"), (num(F(a * a + b * b, c * c + d * d) if op == '÷' else F(a * a + b * b + c * c + d * d)), "combined the squares"),
          (num(F(m1 + m2)), "added the moduli"), (num(F(abs(a) + abs(b), abs(c) + abs(d)) if op == "÷" else F((abs(a) + abs(b)) * (abs(c) + abs(d)))), "added the parts instead of finding moduli")]
    return I(prompt, num(ans), steps, wr, dict(k="cj_modq", z1=[a, b], z2=[c, d], op=op, show=[z1, z2]), "cj_modq")


def cj_recip(r, L):
    a, b = nz(r, -6, 6), nz(r, -6, 6)
    n = a * a + b * b
    z = zin(a, b)
    ans = cx(F(a, n), F(-b, n))
    prompt = f"Write 1/({z}) in the form a + bi."
    steps = [f"Multiply by the conjugate: (1 · ({zin(a, -b)}))/(({z})({zin(a, -b)})).",
             f"The denominator is {a}² + {abs(b)}² = {n}.", f"= {ans}."]
    wr = [(cx(F(1, a), F(1, b)), "took the reciprocal of each part"), (cx(F(a, n), F(b, n)), "did not change the sign of the imaginary part"),
          (cx(F(a, a * a - b * b), F(-b, a * a - b * b)) if a * a != b * b else cx(a, -b), "used a² − b² as the denominator"),
          (zin(a, -b), "forgot to divide by a² + b²"), (cx(F(-a, n), F(b, n)), "changed the sign of the real part too")]
    return I(prompt, ans, steps, wr, dict(k="cj_recip", a=a, b=b, show=[z]), "cj_recip")


def cj_solve(r, L):
    """z̄ given: find z, or z + z̄ / z − z̄."""
    a, b = nz(r, -9, 9), nz(r, -9, 9)
    z = zin(a, b)
    which = r.choice(["sum", "diff"]) if L > 0 else "sum"
    if which == "sum":
        ans = str(2 * a)
        prompt = f"z = {z}. Find z + z̄."
        steps = [f"z̄ = {zin(a, -b)}.", f"z + z̄ = 2 · {a} = {ans} (the imaginary parts cancel)."]
        wr = [(imag(2 * b, 1), "added the imaginary parts instead"), (cx(2 * a, 2 * b), "added z to itself"),
              (str(a * a + b * b), "multiplied z by z̄"), (str(a), "forgot to double the real part")]
    else:
        ans = imag(2 * b, 1)
        prompt = f"z = {z}. Find z - z̄."
        steps = [f"z̄ = {zin(a, -b)}.", f"z - z̄ = ({z}) - ({zin(a, -b)}) = {ans}."]
        wr = [(str(2 * a), "found z + z̄"), (imag(-2 * b, 1), "subtracted in the wrong order"),
              ("0", "thought a number minus its conjugate is 0"), (imag(b, 1), "forgot to double the imaginary part")]
    return I(prompt, ans, steps, wr, dict(k="cj_solve", a=a, b=b, which=which, show=[z]), "cj_solve")


# ================================================================== vectors: polar form, De Moivre (N-CN.B.5)
ANG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330]


def pol_mult(r, L):
    r1, r2 = ri(r, 1, 6), ri(r, 1, 5)
    t = r.choice([60, 90, 120, 150, 180, 210, 240, 270, 300, 30, 45, 135, 225, 315])
    t1 = ri(r, 5, t - 5) if t > 10 else ri(r, 5, 25)
    need(0 < t1 < t)
    t2 = t - t1
    need(t1 % 5 == 0)
    op = "·" if L == 0 else r.choice(["·", "÷"])
    if op == "÷":
        # quotient: (r1 r2 cis(t + t2)) ÷ (r2 cis t2) = r1 cis t
        za, zb = ptext(r1 * r2, t + t2), ptext(r2, t2)
        need(t + t2 < 360)
        R = F(r1)
        ans = polar_rect(R, t)
        prompt = f"Find ({za}) ÷ ({zb}). Write the answer in the form a + bi."
        steps = [f"Divide the moduli and subtract the angles: {r1 * r2}/{r2} = {r1}, {t + t2}° - {t2}° = {t}°.",
                 f"{ptext(r1, t)} = {ans}."]
        wr = [(polar_rect(F(r1 * r2 * r2), t), "multiplied the moduli"), (polar_rect(R, t + 2 * t2) if special(t + 2 * t2) else polar_rect(R, t + 180), "added the angles"),
              (polar_rect(R, -t), "subtracted the angles in the wrong order"), (polar_rect(R * 2, t), "doubled the modulus"), (polar_rect(R, 90 - t) if special(90 - t) and (90 - t) % 360 != t else polar_rect(R + 1, t), "swapped cosine and sine")]
        return I(prompt, ans, steps, wr, dict(k="pol_div", r=[r1 * r2, r2], t=[t + t2, t2], show=[za, zb]), "pol_div")
    za, zb = ptext(r1, t1), ptext(r2, t2)
    R = r1 * r2
    ans = polar_rect(R, t)
    prompt = f"Find ({za}) · ({zb}). Write the answer in the form a + bi."
    steps = [f"Multiply the moduli and add the angles: {r1} · {r2} = {R}, {t1}° + {t2}° = {t}°.", f"{ptext(R, t)} = {ans}."]
    wr = [(polar_rect(r1 + r2, t), "added the moduli"), (polar_rect(R, t + 180), "lost the sign of the angle's quadrant"),
          (polar_rect(R, 90 - t) if special(90 - t) and (90 - t) % 360 != t % 360 else polar_rect(R, t + 90), "swapped cosine and sine"),
          (polar_rect(R * 2, t), "doubled the modulus")]
    return I(prompt, ans, steps, wr, dict(k="pol_mult", r=[r1, r2], t=[t1, t2], show=[za, zb]), "pol_mult")


def dm_power(r, L):
    if L == 0:
        rr, n = ri(r, 1, 3), ri(r, 2, 4)
        t = r.choice([d for d in (15, 20, 30, 40, 45, 60, 75, 90) if special(d * n)])
        need(special(t * n))
        z = ptext(rr, t)
        R = rr ** n
        ans = polar_rect(R, t * n)
        prompt = f"Use De Moivre's Theorem to find ({z})^{n}. Write the answer in the form a + bi."
        steps = [f"[r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ): {rr}^{n} = {R}, {n} · {t}° = {t * n}°.", f"{ptext(R, (t * n))} = {ans}."]
        wr = [(polar_rect(rr * n, t * n), "multiplied the modulus by n"), (polar_rect(R, t), "did not multiply the angle"),
              (polar_rect(R, t + n) if special(t + n) else polar_rect(R, t * n + 180), "added n to the angle"), (polar_rect(R * 2, t * n), "doubled the modulus")]
        return I(prompt, ans, steps, wr, dict(k="dm_power", r=rr, t=t, n=n, show=[z]), "dm_power")
    base = r.choice([(1, 1, 2, 45, 2), (1, -1, 2, 315, 2), (-1, 1, 2, 135, 2), (1, 3, 2, 60, 1), (-1, 3, 2, 120, 1), (3, 1, 2, 30, 1), (3, -1, 2, 330, 1),
                     (0, 2, 2, 90, 0)])
    a, b, rr, t, kind = base
    n = ri(r, 3, 8 if L == 2 else 6)
    # z text and modulus
    if kind == 2:
        z = zin(a, b)
        mod = f"√2"
        R2 = F(2) ** n  # r² ^ n
        Rn_text = f"(√2)^{n}"
    elif kind == 1:
        z = cx(F(a, abs(a)) if abs(a) == 3 else a, F(b, abs(b)) if abs(b) == 3 else b, 3 if abs(a) == 3 else 1, 3 if abs(b) == 3 else 1)
        mod = "2"
        R2 = F(4) ** n
        Rn_text = f"2^{n}"
    else:
        z = zin(a, b)
        mod = "2"
        R2 = F(4) ** n
        Rn_text = f"2^{n}"
    # rⁿ = sqrt(R2): exact as c√k
    if R2.numerator == math.isqrt(R2.numerator) ** 2:
        rn, kk = F(math.isqrt(R2.numerator)), 1
    else:
        rn, kk = F(math.isqrt(R2.numerator // 2)), 2
    need(kk == 1 or special(t * n))
    (c, kc), (s, ks) = trig(t * n)
    # multiply rn·√kk by c√kc
    def mulk(coef_, k1, k2):
        if k1 == 1:
            return coef_, k2
        if k2 == 1:
            return coef_, k1
        if k1 == k2:
            return coef_ * k1, 1
        return coef_, k1 * k2
    re_, kre = mulk(rn * c, kk, kc)
    im_, kim = mulk(rn * s, kk, ks)
    need(kre in (1, 2, 3) and kim in (1, 2, 3))
    ans = cx(re_, im_, kre, kim)
    prompt = f"Use De Moivre's Theorem to find ({z})^{n}. Write the answer in the form a + bi."
    steps = [f"Polar form: |{z}| = {mod} and the angle is {t}°, so {z} = {mod}(cos {t}° + i sin {t}°).",
             f"({z})^{n} = {Rn_text}(cos {t * n}° + i sin {t * n}°) = {num(rn) if kk == 1 else surd(rn, 2)}(cos {t * n % 360}° + i sin {t * n % 360}°).",
             f"= {ans}."]
    def alt(dd):
        (c2, kc2), (s2, ks2) = trig(dd)
        r_, k1 = mulk(rn * c2, kk, kc2)
        i_, k2 = mulk(rn * s2, kk, ks2)
        return cx(r_, i_, k1, k2)
    wr = [(alt(t * n + 180), "used the wrong quadrant for the angle"), (alt(t), "did not multiply the angle by n"),
          (cx(re_ * 2, im_ * 2, kre, kim), "doubled the modulus"), (alt(90 - t * n) if (90 - t * n) % 360 != (t * n) % 360 else alt(t * n + 90), "swapped cosine and sine")]
    return I(prompt, ans, steps, wr, dict(k="dm_rect_power", a=a, b=b, sq3=(kind == 1), n=n, show=[z]), "dm_rect_power")


def dm_modulus(r, L):
    a, b = r.choice([(1, 1), (1, -1), (2, 2), (3, 4), (0, 2), (1, 2), (2, 1), (-3, 4), (6, 8), (2, -2)])
    n = ri(r, 2, 6 if L < 2 else 10)
    m2 = a * a + b * b
    val_ = F(m2) ** n
    need(val_.numerator < 10 ** 7)
    root = math.isqrt(val_.numerator)
    if root * root == val_.numerator:
        ans = str(root)
    else:
        # n odd, m2 not a square: √(m2ⁿ) = m2^((n - 1)/2)·√m2 (m2 here is 2, 5 or 8 = 4·2)
        sq = 1
        for p_ in range(2, 10):
            while m2 % (p_ * p_ * sq * sq) == 0 and p_ * p_ * sq * sq <= m2:
                sq *= p_
        ans = surd(m2 ** ((n - 1) // 2) * sq, m2 // (sq * sq))
    z = zin(a, b)
    prompt = f"Find |({z})^{n}|."
    steps = [f"|{z}| = √({a}² + {b}²) = √{m2}.", f"|zⁿ| = |z|ⁿ = (√{m2})^{n} = {ans}."]
    wr = [(str(m2 ** n), "forgot the square root"), (str(n * m2), "multiplied by n instead of raising to the power"),
          (str(abs(a) ** n + abs(b) ** n), "raised each part to the power and added"), (surd(n, m2) if math.isqrt(m2) ** 2 != m2 else str(n * math.isqrt(m2)), "multiplied the modulus by n")]
    return I(prompt, ans, steps, wr, dict(k="dm_modulus", a=a, b=b, n=n, show=[z]), "dm_modulus")


def dm_root(r, L):
    """The nth root of R(cos T + i sin T) with the smallest positive angle: r(cos(T/n) + i sin(T/n))."""
    n = r.choice([2, 3]) if L < 2 else r.choice([2, 3, 4])
    rr = ri(r, 1, 3)
    t = r.choice([d for d in (30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330) if special(d)])
    T = t * n
    need(T < 360 or L == 2)
    T %= 360
    need(T != 0)
    t0 = F(T, n)
    need(t0.denominator == 1 and special(int(t0)))
    t0 = int(t0)
    R = rr ** n
    z = ptext(R, T)
    ans = polar_rect(rr, t0)
    word = {2: "square", 3: "cube", 4: "fourth"}[n]
    prompt = f"The {word} roots of {z} are equally spaced around a circle. Find the root with the smallest positive angle. Write it in the form a + bi."
    steps = [f"Each root has modulus {R}^(1/{n}) = {rr}.",
             f"The smallest angle is {T}°/{n} = {t0}°; the others add multiples of {360 // n}°.", f"{ptext(rr, t0)} = {ans}."]
    wr = [(polar_rect(R, t0), "did not take the root of the modulus"), (polar_rect(rr, T) if T % 360 != t0 else polar_rect(rr, T + 180), "did not divide the angle"),
          (polar_rect(rr, t0 + 360 // n), "gave a different root"), (polar_rect(F(R, n), t0), "divided the modulus by n")]
    return I(prompt, ans, steps, wr, dict(k="dm_root", R=R, T=T, n=n, show=[z]), "dm_root")


# ================================================================== vectors: limaçons and cardioids (APPC.3.14)
def lim_text(a, b, fn):
    sb = f"+ {b}" if b > 0 else f"- {-b}"
    bb = "" if abs(b) == 1 else str(abs(b)) + " "
    return f"r = {a} {sb[0]} {bb}{fn} θ"


@mc_only
def lim_classify(r, L):
    kind = r.choice(["cardioid", "inner", "dimpled", "convex"])
    b = ri(r, 2, 6) * r.choice([1, -1])
    B = abs(b)
    if kind == "cardioid":
        a = B
    elif kind == "inner":
        a = ri(r, 1, B - 1)
    elif kind == "dimpled":
        a = ri(r, B + 1, 2 * B - 1)
    else:
        a = ri(r, 2 * B, 2 * B + 4)
    need(a > 0)
    fn = r.choice(["cos", "sin"])
    eq = lim_text(a, b, fn)
    names = {"cardioid": "a cardioid", "inner": "a limaçon with an inner loop", "dimpled": "a dimpled limaçon", "convex": "a convex limaçon"}
    ans = names[kind]
    prompt = f"Which best describes the graph of {eq}?"
    rule = {"cardioid": "a/|b| = 1", "inner": "a/|b| < 1", "dimpled": "1 < a/|b| < 2", "convex": "a/|b| ≥ 2"}[kind]
    steps = [f"For r = a ± b {fn} θ, compare a = {a} with |b| = {B}: {a}/{B} = {num(F(a, B))}.", f"Since {rule}, the graph is {ans}."]
    wr = [(names[k], "used the wrong ratio test") for k in names if k != kind] + [("a rose curve", "confused it with r = a cos(nθ)")]
    return I(prompt, ans, steps, wr, dict(k="lim_classify", a=a, b=b, show=[eq]), "lim_classify")


def lim_max(r, L):
    b = nz(r, -7, 7)
    a = ri(r, 1, 9)
    fn = r.choice(["cos", "sin"])
    eq = lim_text(a, b, fn)
    ans = a + abs(b)
    where = {("cos", 1): "θ = 0", ("cos", -1): "θ = π", ("sin", 1): "θ = π/2", ("sin", -1): "θ = 3π/2"}[(fn, 1 if b > 0 else -1)]
    prompt = f"What is the greatest distance from the pole to a point on the graph of {eq}?"
    steps = [f"{fn} θ ranges from -1 to 1, so |r| is greatest when {fn} θ = {'1' if b > 0 else '-1'} ({where}) or at the far side of an inner loop.",
             f"Greatest |r| = {a} + {abs(b)} = {ans}."]
    wr = [(str(abs(a - abs(b))) if abs(a - abs(b)) != ans else str(ans + 1), "subtracted instead of adding"), (str(a), "used only the constant"),
          (str(abs(b)), "used only the coefficient"), (str(2 * ans), "gave the width of the graph")]
    return I(prompt, str(ans), steps, wr, dict(k="lim_max", a=a, b=b, show=[eq]), "lim_max")


THETA = [("0", 0), ("π/6", 30), ("π/4", 45), ("π/3", 60), ("π/2", 90), ("2π/3", 120), ("3π/4", 135), ("5π/6", 150), ("π", 180),
         ("7π/6", 210), ("4π/3", 240), ("3π/2", 270), ("5π/3", 300), ("11π/6", 330)]


def lim_value(r, L):
    a, b = ri(r, 1, 8), nz(r, -8, 8)
    fn = r.choice(["cos", "sin"])
    lab, deg = r.choice(THETA if L > 0 else [t for t in THETA if t[1] % 90 == 0 or t[1] % 60 == 0 or t[1] % 30 == 0])
    (c, kc), (s, ks) = trig(deg)
    v, k = (c, kc) if fn == "cos" else (s, ks)
    val_ = F(b) * v
    if k == 1:
        ans = num(F(a) + val_)
    else:
        ans = join([str(a), surd(val_, k)])
    eq = lim_text(a, b, fn)
    prompt = f"For {eq}, find r when θ = {lab}."
    steps = [f"{fn}({lab}) = {surd(v, k)}.", f"r = {a} + ({b})({surd(v, k)}) = {ans}."]
    (c2, kc2), (s2, ks2) = trig(deg)
    ov, ok = (s2, ks2) if fn == "cos" else (c2, kc2)
    def make(vv, kk):
        return num(F(a) + F(b) * vv) if kk == 1 else join([str(a), surd(F(b) * vv, kk)])
    wr = [(make(ov, ok), f"used {'sin' if fn == 'cos' else 'cos'} instead of {fn}"), (make(-v, k), "used the wrong sign for the trig value"),
          (num(F(b) * v) if k == 1 else surd(F(b) * v, k), "dropped the constant term"), (num(F(a + b)), "treated the trig value as 1")]
    return I(prompt, ans, steps, wr, dict(k="lim_value", a=a, b=b, fn=fn, deg=deg, show=[eq, lab]), "lim_value")


def lim_pole(r, L):
    """r = a(1 ± cos θ) etc.: where does the graph pass through the pole?"""
    if L == 0:
        a = ri(r, 1, 8)
        fn = r.choice(["cos", "sin"])
        sg = r.choice([1, -1])
        eq = lim_text(a, sg * a, fn)
        ans = {("cos", 1): "θ = π", ("cos", -1): "θ = 0", ("sin", 1): "θ = 3π/2", ("sin", -1): "θ = π/2"}[(fn, sg)]
        prompt = f"For 0 ≤ θ < 2π, at what value of θ does the graph of {eq} pass through the pole?"
        steps = [f"Set r = 0: {fn} θ = {-sg}.", f"{ans}."]
        opp = {"θ = π": "θ = 0", "θ = 0": "θ = π", "θ = 3π/2": "θ = π/2", "θ = π/2": "θ = 3π/2"}
        wr = [(opp[ans], "set the trig value equal to the wrong sign"), ("θ = π/4" if fn == "cos" else "θ = π/6", "guessed a special angle"),
              ({"θ = π": "θ = 3π/2", "θ = 0": "θ = π/2", "θ = 3π/2": "θ = π", "θ = π/2": "θ = 0"}[ans], "used the other trig function"),
              ("θ = 2π", "gave an angle outside 0 ≤ θ < 2π")]
        return I(prompt, ans, steps, wr, dict(k="lim_pole", a=a, b=sg * a, fn=fn, show=[eq]), "lim_pole")
    b = r.choice([2, 4, 6, 8]) * r.choice([1, -1])
    a = abs(b) // 2
    fn = r.choice(["cos", "sin"])
    eq = lim_text(a, b, fn)
    target = F(-a, b)  # cos θ or sin θ = target (±1/2)
    if fn == "cos":
        sol = ("2π/3", "4π/3") if target < 0 else ("π/3", "5π/3")
        other = ("π/3", "5π/3") if target < 0 else ("2π/3", "4π/3")
        swap = ("7π/6", "11π/6") if target < 0 else ("π/6", "5π/6")
    else:
        sol = ("7π/6", "11π/6") if target < 0 else ("π/6", "5π/6")
        other = ("π/6", "5π/6") if target < 0 else ("7π/6", "11π/6")
        swap = ("2π/3", "4π/3") if target < 0 else ("π/3", "5π/3")
    ans = f"θ = {sol[0]} or θ = {sol[1]}"
    prompt = f"The graph of {eq} has an inner loop. For 0 ≤ θ < 2π, at what values of θ does it pass through the pole?"
    steps = [f"Set r = 0: {fn} θ = {num(target)}.", f"{ans}."]
    wr = [(f"θ = {other[0]} or θ = {other[1]}", "used the wrong sign"), (f"θ = {swap[0]} or θ = {swap[1]}", "solved for the other trig function"),
          (f"θ = {sol[0]}", "gave only one angle"), ("θ = π" if fn == "cos" else "θ = 3π/2", "treated it as a cardioid")]
    return I(prompt, ans, steps, wr, dict(k="lim_pole2", a=a, b=b, fn=fn, show=[eq]), "lim_pole2")


@mc_only
def lim_symmetry(r, L):
    a, b = ri(r, 1, 8), nz(r, -8, 8)
    fn = r.choice(["cos", "sin"])
    eq = lim_text(a, b, fn)
    ans = "the polar axis (the x-axis)" if fn == "cos" else "the line θ = π/2 (the y-axis)"
    prompt = f"The graph of {eq} is symmetric about which line?"
    steps = [f"{'cos(-θ) = cos θ, so replacing θ with -θ gives the same equation' if fn == 'cos' else 'sin(π - θ) = sin θ, so replacing θ with π - θ gives the same equation'}.",
             f"The graph is symmetric about {ans}."]
    wr = [("the line θ = π/2 (the y-axis)" if fn == "cos" else "the polar axis (the x-axis)", "mixed up the cosine and sine cases"),
          ("the line θ = π/4 (y = x)", "assumed symmetry about y = x"), ("the pole only (origin symmetry)", "confused it with a rose curve")]
    return I(prompt, ans, steps, wr, dict(k="lim_symmetry", fn=fn, show=[eq]), "lim_symmetry")


# ================================================================== sequences: the Binomial Theorem (A-APR.C.5)
def bin_text(a, b, n, var="x"):
    lead = "" if a == 1 else ("-" if a == -1 else str(a))
    return f"({lead}{var} {'+' if b > 0 else '-'} {abs(b)})^{n}"


def bn_coef(r, L):
    n = ri(r, 3, 6) if L == 0 else ri(r, 4, 8)
    a = 1 if L == 0 else r.choice([1, 2, 3, -1, -2])
    b = nz(r, -3, 3) if L < 2 else nz(r, -4, 4)
    k = ri(r, 1, n - 1)
    ans = math.comb(n, k) * a ** k * b ** (n - k)
    need(abs(ans) < 10 ** 6)
    e = bin_text(a, b, n)
    prompt = f"Find the coefficient of x{sup(k) if k > 1 else ''} in the expansion of {e}."
    steps = [f"The term with x{sup(k) if k > 1 else ''} is C({n}, {k})·({a}x){sup(k) if k > 1 else ''}·({b}){sup(n - k) if n - k > 1 else ''}.",
             f"C({n}, {k}) = {math.comb(n, k)}; {math.comb(n, k)} · {a ** k} · {b ** (n - k)} = {ans}."]
    wr = [(str(math.comb(n, k)), "gave only the binomial coefficient"), (str(math.comb(n, k) * b ** (n - k)), "forgot to raise the coefficient of x to the power"),
          (str(math.comb(n, k) * a ** (n - k) * b ** k), "swapped the powers of the two terms"), (str(-ans), "lost the sign of the negative term")]
    return I(prompt, str(ans), steps, wr, dict(k="bn_coef", a=a, b=b, n=n, kk=k, show=[e]), "bn_coef")


def bn_term(r, L):
    n = ri(r, 4, 7)
    a, b = r.choice([1, 2, 3]), nz(r, -3, 3)
    t = ri(r, 2, n)  # t-th term, k = t - 1 powers of the second term
    j = t - 1
    c = math.comb(n, j) * a ** (n - j) * b ** j
    p = n - j
    e = bin_text(a, b, n)
    ans = (coef(c, "x" + (sup(p) if p > 1 else "")) if p > 0 else str(c))
    ordn = {2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth"}[t]
    prompt = f"Find the {ordn} term of the expansion of {e}, written in descending powers of x."
    steps = [f"The {ordn} term uses k = {j}: C({n}, {j})({a if a != 1 else ''}x){sup(p) if p > 1 else ''}({b}){sup(j) if j > 1 else ''}.",
             f"C({n}, {j}) = {math.comb(n, j)}, so the term is {ans}."]
    j2 = j + 1 if j + 1 <= n else j - 1
    c2, p2 = math.comb(n, j2) * a ** (n - j2) * b ** j2, n - j2
    w2 = coef(c2, "x" + (sup(p2) if p2 > 1 else "")) if p2 > 0 else str(c2)
    w3 = coef(math.comb(n, j) * b ** j, "x" + (sup(p) if p > 1 else "")) if p > 0 else str(math.comb(n, j) * b ** j)
    w4 = coef(-c, "x" + (sup(p) if p > 1 else "")) if p > 0 else str(-c)
    w5 = coef(math.comb(n, j), "x" + (sup(p) if p > 1 else "")) if p > 0 else str(math.comb(n, j))
    wr = [(w2, "used k equal to the term number (off by one)"), (w3, "forgot to raise the coefficient of x"), (w4, "lost the sign"), (w5, "gave only the binomial coefficient")]
    return I(prompt, ans, steps, wr, dict(k="bn_term", a=a, b=b, n=n, t=t, show=[e]), "bn_term")


def bn_pascal(r, L):
    n = ri(r, 5, 12)
    k = ri(r, 2, n - 2)
    ans = math.comb(n, k)
    prompt = f"Row {n} of Pascal's triangle (starting with row 0: 1) gives the coefficients of (x + y)^{n}. What is the coefficient of x{sup(n - k)}y{sup(k)}?"
    steps = [f"The coefficient is C({n}, {k}) = {n}!/({k}! · {n - k}!).", f"= {ans}."]
    wr = [(str(math.comb(n - 1, k)), "used the previous row"), (str(math.comb(n, k - 1)), "was off by one in the row"),
          (str(n * k), "multiplied n and k"), (str(math.perm(n, k)), "used a permutation")]
    return I(prompt, str(ans), steps, wr, dict(k="bn_pascal", n=n, kk=k, show=[f"^{n}"]), "bn_pascal")


def bn_sum(r, L):
    n = ri(r, 3, 7)
    a, b = r.choice([1, 2, 3]), nz(r, -3, 3)
    need(a + b != 0)
    e = bin_text(a, b, n)
    ans = (a + b) ** n
    prompt = f"What is the sum of the coefficients in the expansion of {e}?"
    steps = [f"Substitute x = 1: the sum of the coefficients is ({a} + ({b}))^{n}.", f"= {a + b}^{n} = {ans}."]
    wr = [(str(2 ** n), "added the binomial coefficients only"), (str(a ** n + b ** n), "added only the first and last terms"),
          (str(n * (a + b)), "multiplied instead of raising to the power"), (str(n + 1), "counted the terms")]
    return I(prompt, str(ans), steps, wr, dict(k="bn_sum", a=a, b=b, n=n, show=[e]), "bn_sum")


def bn_expand(r, L):
    n = 3 if L == 0 else r.choice([3, 4])
    b = nz(r, -4, 4)
    a = 1 if L < 2 else r.choice([2, 3])
    e = bin_text(a, b, n)
    cs = {n - j: math.comb(n, j) * a ** (n - j) * b ** j for j in range(n + 1)}
    ans = poly(cs)
    prompt = f"Expand {e}."
    steps = [f"Use the coefficients from row {n} of Pascal's triangle: {', '.join(str(math.comb(n, j)) for j in range(n + 1))}.",
             "Terms: " + ", ".join(f"C({n}, {j})({a if a != 1 else ''}x){sup(n - j) if n - j > 1 else ''}({b}){sup(j) if j > 1 else ''}" for j in range(n + 1)) + ".",
             f"= {ans}."]
    wr = [(poly({n: a ** n, 0: b ** n}), "raised each term to the power"), (poly({n - j: math.comb(n, j) * a ** (n - j) * abs(b) ** j for j in range(n + 1)}), "lost the negative signs" if b < 0 else "ignored a sign"),
          (poly({n - j: a ** (n - j) * b ** j for j in range(n + 1)}), "left out the binomial coefficients"),
          (poly({n - j: math.comb(n, j) * a * b ** j for j in range(n + 1)}), "did not raise the coefficient of x")]
    return I(prompt, ans, steps, wr, dict(k="bn_expand", a=a, b=b, n=n, show=[e]), "bn_expand")


# ================================================================== sequences/limits: continuity and one-sided limits (F-IF.C.7b, 7d)
def piece(m1, b1, m2, b2, c, closed_left=False):
    f1 = join([coef(m1, "x") if m1 else "", num(b1) if b1 else ""]) if (m1 or b1) else "0"
    f2 = join([coef(m2, "x") if m2 else "", num(b2) if b2 else ""]) if (m2 or b2) else "0"
    return f"f(x) = {f1} if x < {c}; {f2} if x ≥ {c}"


def cn_onesided(r, L):
    c = ri(r, -4, 5)
    m1, b1, m2, b2 = nz(r, -4, 4), ri(r, -8, 8), nz(r, -4, 4), ri(r, -8, 8)
    L1, L2 = m1 * c + b1, m2 * c + b2
    need(L1 != L2)
    side = r.choice(["-", "+"])
    f = piece(m1, b1, m2, b2, c)
    ans = L1 if side == "-" else L2
    lab = "from the left" if side == "-" else "from the right"
    prompt = f"{f}. Find the limit of f(x) as x → {c}{'⁻' if side == '-' else '⁺'} ({lab})."
    steps = [f"As x → {c}{'⁻' if side == '-' else '⁺'}, x {'<' if side == '-' else '>'} {c}, so use the {'first' if side == '-' else 'second'} piece.",
             f"Substitute x = {c}: {ans}."]
    wr = [(str(L2 if side == "-" else L1), "used the other piece"), ("does not exist", "confused a one-sided limit with the two-sided limit"),
          (str(L1 + L2), "added the two pieces"), (str(ans + 1), "made an arithmetic slip")]
    return I(prompt, str(ans), steps, wr, dict(k="cn_onesided", c=c, p=[m1, b1, m2, b2], side=side, show=[f]), "cn_onesided")


def cn_param(r, L):
    """Find k so f is continuous: x² + a for x < c, kx + b for x ≥ c."""
    c = nz(r, -4, 4)
    a, b = ri(r, -9, 9), ri(r, -9, 9)
    k = F(c * c + a - b, c)
    need(k.denominator == 1 or L == 2)
    need(k != 0)
    f1 = join(["x²", num(a) if a else ""])
    f2 = join(["kx", num(b) if b else ""])
    f = f"f(x) = {f1} if x < {c}; {f2} if x ≥ {c}"
    prompt = f"{f}. Find the value of k that makes f continuous at x = {c}."
    steps = [f"Left limit: {c}² + ({a}) = {c * c + a}. Right value: k({c}) + ({b}).",
             f"Set them equal: {c}k = {c * c + a - b}, so k = {num(k)}."]
    wr = [(num(F(c * c + a + b, c)), "moved b to the wrong side"), (num(F(c * c + a - b)), "forgot to divide by x = c"),
          (num(F(c * c + a)), "used only the left limit"), (num(-k), "made a sign error")]
    return I(prompt, num(k), steps, wr, dict(k="cn_param", c=c, a=a, b=b, show=[f1, f2]), "cn_param")


def cn_removable(r, L):
    p, q = ri(r, -7, 7), ri(r, -7, 7)
    need(p != q and p != 0)
    num_ = poly({2: 1, 1: -(p + q), 0: p * q})
    f = f"f(x) = ({num_})/({lf(-p)})"
    ans = p - q
    prompt = f"{f} is undefined at x = {p}. What value should f({p}) be given to make f continuous there?"
    steps = [f"Factor: ({num_}) = ({lf(-p)})({lf(-q)}).", f"For x ≠ {p}, f(x) = {lf(-q)}, so the limit as x → {p} is {p} - ({q}) = {ans}.",
             f"Define f({p}) = {ans}."]
    wr = [("0", "substituted into the numerator only"), (str(p + q), "used the wrong sign in the factor"), (str(q), "gave the other zero"),
          ("no value; f has a vertical asymptote", "did not factor")]
    return I(prompt, str(ans), steps, wr, dict(k="cn_removable", p=p, q=q, show=[num_]), "cn_removable")


@mc_only
def cn_infinite(r, L):
    c = ri(r, -6, 6)
    a = nz(r, -9, 9)
    pw = 1 if L == 0 else r.choice([1, 2])
    side = r.choice(["-", "+"])
    d = lf(-c)
    f = f"{a}/" + (d if c == 0 else f"({d})") + (sup(2) if pw == 2 else "")
    sgn = (1 if a > 0 else -1) * (1 if side == "+" or pw == 2 else -1)
    ans = "∞" if sgn > 0 else "-∞"
    prompt = f"Find the limit of {f} as x → {c}{'⁻' if side == '-' else '⁺'}."
    steps = [f"As x → {c}{'⁻' if side == '-' else '⁺'}, the denominator approaches 0 through {'positive' if (side == '+' or pw == 2) else 'negative'} values.",
             f"The numerator is {a}, so the quotient grows without bound: {ans}."]
    wr = [("-∞" if ans == "∞" else "∞", "used the wrong sign of the denominator"), ("0", "thought dividing by a small number gives 0"),
          ("does not exist (the one-sided limits differ)", "described the two-sided limit"), (str(a), "used the numerator")]
    return I(prompt, ans, steps, wr, dict(k="cn_infinite", a=a, c=c, pw=pw, side=side, show=[f]), "cn_infinite")


@mc_only
def cn_exists(r, L):
    c = ri(r, -4, 5)
    m1, b1, m2 = nz(r, -4, 4), ri(r, -8, 8), nz(r, -4, 4)
    same = r.random() < 0.5
    L1 = m1 * c + b1
    b2 = L1 - m2 * c if same else L1 - m2 * c + nz(r, -3, 3)
    f = piece(m1, b1, m2, b2, c)
    L2 = m2 * c + b2
    ans = str(L1) if same else "The limit does not exist."
    prompt = f"{f}. What is the limit of f(x) as x → {c}?"
    steps = [f"Left: {L1}. Right: {L2}.", f"{'The one-sided limits agree, so the limit is ' + str(L1) if same else 'The one-sided limits differ, so the limit does not exist'}."]
    wr = [(str(L2) if not same else "The limit does not exist.", "checked only one side" if not same else "thought a piecewise function has no limit at the break"),
          (str(L1) if not same else str(L1 + 1), "used only the left piece" if not same else "made an arithmetic slip"),
          (str(L1 + L2), "added the one-sided limits"), ("0", "guessed 0")]
    return I(prompt, ans, steps, wr, dict(k="cn_exists", c=c, p=[m1, b1, m2, b2], show=[f]), "cn_exists")


# ------------------------------------------------------------------ the new skills
NEW_SKILLS = [
    ("functions", "Rational Expressions and Partial Fractions", [ra_simplify, ra_add, pf_coef, ra_excluded, ra_value], ["A-APR.D.7", "A-APR.D.6"], "pc-fun"),
    ("functions", "Verifying Inverses and Restricting Domains", [inv_table, inv_restrict_value, inv_rational, inv_compose, inv_which_restrict], ["F-BF.B.4b", "F-BF.B.4c", "F-BF.B.4d"], "pc-fun"),
    ("vectors", "Complex Conjugates, Moduli, and Quotients", [cj_product, cj_quotient, cj_modq, cj_recip, cj_solve], ["N-CN.A.3"], "pc-vec"),
    ("vectors", "Products, Powers, and Roots in Polar Form", [pol_mult, dm_power, dm_modulus, dm_root], ["N-CN.B.5"], "pc-vec"),
    ("vectors", "Limaçons and Cardioids", [lim_classify, lim_max, lim_value, lim_pole, lim_symmetry], ["APPC.3.14", "APPC.3.13"], "pc-vec"),
    ("sequences-series-limits", "The Binomial Theorem", [bn_coef, bn_term, bn_pascal, bn_sum, bn_expand], ["A-APR.C.5"], "pc-ssl"),
    ("sequences-series-limits", "Continuity and One-Sided Limits", [cn_onesided, cn_param, cn_removable, cn_infinite, cn_exists], ["F-IF.C.7b", "F-IF.C.7d"], "pc-ssl"),
]


from contexts import CONTEXT, CONTEXTUAL  # noqa: E402,F401  (contexts imports helpers from this module)
