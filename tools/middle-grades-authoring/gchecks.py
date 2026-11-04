"""Grade 6/7 custom independent checks, registered into the Grade 8 verifier's CUSTOM table.
Each check(chk, text) -> bool re-derives correctness from the data shown to students.
These functions never import the authoring families."""
import math, re
from fractions import Fraction as F
import mathtext as M
import checks_custom as C
from checks_custom import reg

REL = re.compile(r"(≤|≥|<|>|≠|=)")
OPS = {"<": lambda a, b: a < b, ">": lambda a, b: a > b, "≤": lambda a, b: a <= b, "≥": lambda a, b: a >= b,
       "=": lambda a, b: a == b, "≠": lambda a, b: a != b}


def _rel_fn(s, var):
    parts = REL.split(s)
    if len(parts) != 3:
        raise M.ParseError("not a single relation: " + s)
    l, op, r = parts
    return lambda v: OPS[op](M.ev(l, {var: v}), M.ev(r, {var: v}))


def _samples(extra=()):
    pts = {F(k, 4) for k in range(-160, 161)} | {F(k) for k in range(-200, 201, 5)}
    for e in extra:
        pts |= {e, e + F(1, 1000), e - F(1, 1000)}
    return sorted(pts)


@reg
def ineq(chk, text):
    """text (e.g. 'x > -3', 'n ≤ 4') has exactly the same solution set as chk['ineq'] (sampled, incl. boundaries)."""
    var = chk.get("var", "x")
    try:
        g = _rel_fn(chk["ineq"], var)
        t = str(text).replace(" ", " ")
        nums = [F(x) for x in re.findall(r"-?\d+(?:\.\d+)?(?:/\d+)?", t)]
        h = _rel_fn(t, var)
        return all(g(v) == h(v) for v in _samples([F(n) for n in nums] + [F(chk["b"])] if "b" in chk else nums))
    except (M.ParseError, ZeroDivisionError, ValueError, KeyError, TypeError):
        return False


@reg
def cmp(chk, text):
    """text is the symbol <, >, or = that makes  a ? b  true."""
    a, b = M.ev(chk["a"]), M.ev(chk["b"])
    s = str(text).strip()
    return s in OPS and s in "<>=" and OPS[s](a, b) and sum(OPS[o](a, b) for o in "<>=") == 1


@reg
def point(chk, text):
    try:
        x, y = M.parse_point(text)
        return M.same(x, M.ev(chk["x"])) and M.same(y, M.ev(chk["y"]))
    except Exception:
        return False


def _isprime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


@reg
def prime_fact(chk, text):
    """text is a product of primes (powers allowed) equal to n, e.g. '2³ · 3 · 5'."""
    t = str(text).replace("×", "·")
    fs = [s.strip() for s in t.split("·")]
    prod = 1
    for s in fs:
        m = re.fullmatch(r"(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹]*)", s)
        if not m or not _isprime(int(m.group(1))):
            return False
        e = int("".join(M.SUP2[c] for c in m.group(2))) if m.group(2) else 1
        prod *= int(m.group(1)) ** e
    return prod == chk["n"]


@reg
def ratio(chk, text):
    """text 'a:b' (or 'a to b') in simplest whole-number form equal to chk a:b (scaled)."""
    m = re.fullmatch(r"\s*(\d+)\s*(?::|to)\s*(\d+)\s*", str(text))
    if not m:
        return False
    a, b = int(m.group(1)), int(m.group(2))
    A, B = M.ev(chk["a"]), M.ev(chk["b"])
    if b == 0 or B == 0 or F(a, b) != F(A) / F(B):
        return False
    return (not chk.get("simplest", True)) or math.gcd(a, b) == 1


@reg
def round_place(chk, text):
    """text equals expr rounded (half up) to the nearest chk['place'] (e.g. 10, 100, 0.1)."""
    try:
        v = F(M.ev(chk["expr"]))
        p = F(chk["place"])
        q = math.floor(v / p + F(1, 2)) * p
        return M.same(M.val(text), q)
    except Exception:
        return False


@reg
def claims(chk, text):
    """Select-all of 'problem → answer' claims: true exactly when the embedded check accepts the shown answer."""
    import verify as Vf
    sub = chk["table"].get(str(text))
    if sub is None:
        return False
    ans = str(text).rsplit(" → ", 1)[1]
    return bool(Vf.truth(sub, ans))


@reg
def any_of(chk, text):
    """True if any of the listed checks accepts text (used when two forms are both correct)."""
    import verify as Vf
    return any(Vf.truth(c, text) for c in chk["checks"])


@reg
def set_eq(chk, text):
    """Comma-separated list equal (as a set of values) to chk['items'] values."""
    try:
        got = sorted(M.val(s) for s in C.split_list(text))
        want = sorted(M.ev(s) for s in chk["items"])
        return len(got) == len(want) and all(M.same(a, b) for a, b in zip(got, want))
    except Exception:
        return False


@reg
def seq_eq(chk, text):
    """Comma-separated list equal in order to chk['items'] values."""
    try:
        got = [M.val(s) for s in C.split_list(text)]
        want = [M.ev(s) for s in chk["items"]]
        return len(got) == len(want) and all(M.same(a, b) for a, b in zip(got, want))
    except Exception:
        return False


@reg
def stat(chk, text):
    """Statistic of the data list shown: mean, median, mode, range, iqr, mad, q1, q3, min, max."""
    xs = sorted(F(x) for x in chk["data"])
    n = len(xs)

    def med(a):
        k = len(a)
        return a[k // 2] if k % 2 else (a[k // 2 - 1] + a[k // 2]) / 2
    lo, hi = (xs[: n // 2], xs[(n + 1) // 2:])
    mean = sum(xs) / n
    s = chk["stat"]
    if s == "mode":
        from collections import Counter
        c = Counter(xs)
        top = max(c.values())
        modes = sorted(v for v, k in c.items() if k == top)
        if top == 1:
            return str(text).strip().lower() in ("no mode", "none")
        try:
            got = sorted(M.val(t) for t in C.split_list(text))
        except Exception:
            return False
        return got == modes
    v = {"mean": mean, "median": med(xs), "range": xs[-1] - xs[0], "q1": med(lo), "q3": med(hi),
         "iqr": med(hi) - med(lo), "min": xs[0], "max": xs[-1],
         "mad": sum(abs(x - mean) for x in xs) / n}[s]
    try:
        if "places" in chk:
            return C.round_text(v, chk["places"]) == M.strip_units(text)
        return M.same(M.val(text), v)
    except Exception:
        return False


@reg
def frac_simplest(chk, text):
    """text is a fraction (or integer/mixed number if allowed) in simplest form equal to expr."""
    t = str(text).strip()
    m = re.fullmatch(r"(-?)(\d+)/(\d+)", t)
    want = F(M.ev(chk["expr"]))
    if m:
        a, b = int(m.group(2)), int(m.group(3))
        return math.gcd(a, b) == 1 and b != 1 and F(int(m.group(1) + m.group(2)), b) == want
    mm = re.fullmatch(r"(-?)(\d+) (\d+)/(\d+)", t)
    if mm and chk.get("mixed", True):
        w, a, b = int(mm.group(2)), int(mm.group(3)), int(mm.group(4))
        return 0 < a < b and math.gcd(a, b) == 1 and (-1 if mm.group(1) else 1) * (w + F(a, b)) == want
    if re.fullmatch(r"-?\d+", t):
        return F(int(t)) == want
    return False


@reg
def poly_std(chk, text):
    """Polynomial text equivalent to expr AND written with like terms combined (no repeated monomial)."""
    t = str(text)
    if not C.CUSTOM.get("_noop"):
        pass
    try:
        vs = chk.get("vars", ["x"])
        pts = [{v: F(p + 2 * j + 1, 3 + j) for j, v in enumerate(vs)} for p in (1, 2, 4, 7, 11)]
        if not all(M.same(M.ev(t, e), M.ev(chk["expr"], e)) for e in pts):
            return False
    except Exception:
        return False
    if "(" in t:
        return False
    mons = re.findall(r"([A-Za-z](?:[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?(?:[A-Za-z](?:[⁰¹²³⁴⁵⁶⁷⁸⁹]+)?)*)", t.replace(" ", ""))
    terms = re.split(r"(?<=[^\s^])\s*[+-]\s*(?=\S)", t.replace(" ", ""))
    sigs = [re.sub(r"^[-+]?[\d./]*", "", s) for s in terms if s]
    return len(sigs) == len(set(sigs))


@reg
def linear_rule(chk, text):
    """'y = mx + b' text whose graph passes through all chk['pts']."""
    try:
        rhs = M.strip_lhs(text)
        return all(M.same(M.ev(rhs, {"x": F(x)}), F(y)) for x, y in chk["pts"])
    except Exception:
        return False


@reg
def sci(chk, text):
    return C.CUSTOM["sci_form"](chk, text)


@reg
def est(chk, text):
    """Estimate: round each shown operand half-up to chk['place'] then combine with chk['op'] ('+','-','*')."""
    p = F(chk["place"])
    rs = [math.floor(F(M.ev(t)) / p + F(1, 2)) * p for t in chk["terms"]]
    v = rs[0]
    for x in rs[1:]:
        v = v + x if chk["op"] == "+" else v - x if chk["op"] == "-" else v * x
    try:
        return M.same(M.val(text), v)
    except Exception:
        return False


def _rules(seq):
    """Candidate next terms from patterns that fit every shown term."""
    s = [F(x) for x in seq]
    out = []
    d = [b - a for a, b in zip(s, s[1:])]
    if len(set(d)) == 1:
        out.append(("arith", s[-1] + d[0]))
    if all(x != 0 for x in s):
        q = [b / a for a, b in zip(s, s[1:])]
        if len(set(q)) == 1:
            out.append(("geom", s[-1] * q[0]))
    if len(d) >= 3:
        d2 = [b - a for a, b in zip(d, d[1:])]
        if len(set(d2)) == 1 and d2[0] != 0:
            out.append(("quad", s[-1] + d[-1] + d2[0]))
    if len(s) >= 4 and all(s[i] == s[i - 1] + s[i - 2] for i in range(2, len(s))):
        out.append(("fib", s[-1] + s[-2]))
    if len(d) >= 4 and len(set(d[0::2])) == 1 and len(set(d[1::2])) == 1 and d[0] != d[1]:
        out.append(("alt", s[-1] + (d[0] if len(d) % 2 == 0 else d[1])))
    return out


@reg
def next_term(chk, text):
    """Answer is the next term (or the next chk['k'] terms) under the unique simple pattern fitting the terms shown."""
    seq = list(chk["seq"])
    k = chk.get("k", 1)
    got = [M.val(t) for t in C.split_list(text)] if k > 1 else [M.val(text)]
    want = []
    for _ in range(k):
        rs = {v for _, v in _rules(seq)}
        if len(rs) != 1:
            return False
        v = rs.pop()
        want.append(v)
        seq.append(v)
    return len(got) == k and all(M.same(a, b) for a, b in zip(got, want))


@reg
def nth_term(chk, text):
    """Term number chk['n'] of an arithmetic or quadratic pattern determined by the terms shown."""
    s = [F(x) for x in chk["seq"]]
    while len(s) < chk["n"]:
        rs = {v for _, v in _rules(s)}
        if len(rs) != 1:
            return False
        s.append(rs.pop())
    try:
        return M.same(M.val(text), s[chk["n"] - 1])
    except Exception:
        return False


@reg
def rule_fits(chk, text):
    """Expression in n that reproduces every shown term (term number n = 1, 2, 3, ...)."""
    try:
        e = M.strip_lhs(text)
        return all(M.same(M.ev(e, {chk.get("var", "n"): F(i + 1)}), F(v)) for i, v in enumerate(chk["seq"]))
    except Exception:
        return False


@reg
def repeat_pos(chk, text):
    blk = chk["block"]
    return str(text).strip() == blk[(chk["n"] - 1) % len(blk)]


@reg
def quadrant(chk, text):
    x, y = M.ev(chk["x"]), M.ev(chk["y"])
    t = str(text).strip()
    if x == 0 and y == 0:
        want = "origin"
    elif x == 0:
        want = "y-axis"
    elif y == 0:
        want = "x-axis"
    else:
        want = {(1, 1): "Quadrant I", (-1, 1): "Quadrant II", (-1, -1): "Quadrant III", (1, -1): "Quadrant IV"}[(1 if x > 0 else -1, 1 if y > 0 else -1)]
    return t.lower() == want.lower() or t.lower() == ("on the " + want).lower()


def abs_eval(e):
    """Evaluate an expression containing |…| absolute-value bars (bars classified as opening/closing by context)."""
    s = str(e).replace("−", "-")
    out, depth = [], 0
    prev = ""
    for ch in s:
        if ch == "|":
            if depth == 0 or prev == "" or prev in "+-*×÷([":
                out.append("ABS(")
                depth += 1
                prev = "("
                continue
            out.append(")")
            depth -= 1
            prev = ")"
            continue
        out.append(ch)
        if not ch.isspace():
            prev = ch
    t = "".join(out)
    # innermost-first evaluation of ABS(...)
    pat = re.compile(r"ABS\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
    for _ in range(20):
        m = pat.search(t)
        if not m:
            break
        inner = M.ev(m.group(1)) if "ABS" not in m.group(1) else None
        if inner is None:
            break
        v = abs(inner)
        t = t[:m.start()] + "(" + (str(v.numerator) + "/" + str(v.denominator) if isinstance(v, F) else repr(v)) + ")" + t[m.end():]
    return M.ev(t)


@reg
def absval(chk, text):
    try:
        return M.same(M.val(M.strip_units(text) if not str(text).strip().startswith("-") else text), abs_eval(chk["expr"]))
    except Exception:
        try:
            return M.same(M.ev(M.strip_units(text)), abs_eval(chk["expr"]))
        except Exception:
            return False


@reg
def cmp_abs(chk, text):
    a, b = abs_eval(chk["a"]), abs_eval(chk["b"])
    s = str(text).strip()
    return s in ("<", ">", "=") and OPS[s](a, b)


@reg
def budget(chk, text):
    ok = sum(F(p) for p in chk["prices"]) <= chk["budget"]
    return str(text) == ("Yes" if ok else "No")


CLAIMS = {
    "The sum of two integers is always greater than either integer.": lambda a, b: a + b > a and a + b > b,
    "The product of two integers is always greater than either integer.": lambda a, b: a * b > a and a * b > b,
    "The difference of two integers is always less than the first integer.": lambda a, b: a - b < a,
    "The square of an integer is always greater than the integer.": lambda a, b: a * a > a,
}


@reg
def counter(chk, text):
    """Option is a counterexample (makes the claim false)."""
    nums = [int(x) for x in re.findall(r"-?\d+", str(text))]
    a, b = (nums + nums)[:2]
    return not CLAIMS[chk["claim"]](a, b)


@reg
def factored(chk, text):
    """'k(… )' equivalent to expr where k is the greatest common factor (the bracket has no common factor)."""
    t = str(text).strip()
    m = re.fullmatch(r"(-?\d*)\((.+)\)", t)
    if not m:
        return False
    vs = chk.get("vars", ["x"])
    try:
        pts = [{v: F(p + 2 * j + 1, 3 + j) for j, v in enumerate(vs)} for p in (1, 2, 4, 7)]
        if not all(M.same(M.ev(t, e), M.ev(chk["expr"], e)) for e in pts):
            return False
    except Exception:
        return False
    k = int(m.group(1)) if m.group(1) not in ("", "-") else (1 if m.group(1) == "" else -1)
    return abs(k) == chk["gcf"] and _coef_gcd(m.group(2)) == 1


def _coef_gcd(s):
    terms = re.split(r"\s[+-]\s", s.strip())
    g = 0
    for tm in terms:
        mm = re.match(r"-?(\d*)", tm.strip())
        c = int(mm.group(1)) if mm.group(1) else 1
        g = math.gcd(g, c)
    return g


def _truth_at(rel, var, v):
    return _rel_fn(rel, var)(F(v))


@reg
def is_solution(chk, text):
    """'Yes'/'No': does value v satisfy the relation (equation or inequality)?"""
    ok = _truth_at(chk["rel"], chk.get("var", "x"), M.ev(chk["v"]))
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def conds(chk, text):
    """Values listed in the answer (in chk['vars'] order) satisfy every condition shown in the problem."""
    nums = re.findall(r"-?\d+(?:\.\d+)?(?:/\d+)?", M.strip_units(str(text)).replace(",", " , ") if False else str(text))
    vs = chk["vars"]
    if len(nums) != len(vs):
        return False
    env = {v: F(n) for v, n in zip(vs, nums)}
    try:
        for c in chk["conds"]:
            l, op, r_ = REL.split(c)
            if not OPS[op](M.ev(l, env), M.ev(r_, env)):
                return False
        return True
    except Exception:
        return False


@reg
def ray_match(chk, text):
    """Option names a number-line graph whose set equals the inequality's solution set."""
    g = chk["graphs"].get(str(text))
    if g is None:
        return False
    x0, d, closed = F(g[0]), g[1], g[2]
    fn = _rel_fn(chk["ineq"], chk.get("var", "x"))
    for v in _samples([x0]):
        inside = (v > x0 if d == "+" else v < x0) or (closed and v == x0)
        if inside != fn(v):
            return False
    return True


@reg
def eq_same(chk, text):
    """Answer is an equation with the same (single) solution as chk['eq'] and uses the variable."""
    var = chk.get("var", "x")
    if var not in str(text) or "=" not in str(text):
        return False
    try:
        a, b = M.solve_linear(str(text), var), M.solve_linear(chk["eq"], var)
        if chk.get("strict_lhs") and str(text).replace(" ", "").startswith(var + "=") and chk.get("not_solved", True):
            return False
        return a[0] == "one" and b[0] == "one" and M.same(a[1], b[1])
    except Exception:
        return False


@reg
def missing_num(chk, text):
    try:
        s = chk["st"].replace("?", "(" + str(text).strip() + ")")
        l, r_ = s.split("=")
        return M.same(M.ev(l), M.ev(r_))
    except Exception:
        return False


@reg
def classify_eq(chk, text):
    st = chk["st"]
    if re.search(r"[a-z]", st):
        want = "open"
    else:
        l, r_ = st.split("=")
        want = "true" if M.same(M.ev(l), M.ev(r_)) else "false"
    return str(text).strip() == want


@reg
def max_int(chk, text):
    """Greatest integer satisfying the inequality."""
    try:
        n = int(str(text).strip())
    except ValueError:
        return False
    f = _rel_fn(chk["ineq"], chk.get("var", "x"))
    return f(F(n)) and not f(F(n + 1))


@reg
def min_int(chk, text):
    try:
        n = int(str(text).strip())
    except ValueError:
        return False
    f = _rel_fn(chk["ineq"], chk.get("var", "x"))
    return f(F(n)) and not f(F(n - 1))


@reg
def best_est(chk, text):
    """Option is the listed choice closest to the exact value."""
    exact = M.ev(chk["expr"])
    vals = {o: M.ev(o) for o in chk["opts"]}
    best = min(vals, key=lambda o: abs(float(vals[o]) - float(exact)))
    return str(text) == best and sum(1 for o in vals if abs(abs(float(vals[o]) - float(exact)) - abs(float(vals[best]) - float(exact))) < 1e-12) == 1


@reg
def near(chk, text):
    try:
        return abs(float(M.val(text)) - float(M.ev(chk["expr"]))) <= float(chk["tol"]) * max(1.0, 1.0)
    except Exception:
        return False


@reg
def over_under(chk, text):
    e, x = M.ev(chk["est"]), M.ev(chk["exact"])
    want = "overestimate" if e > x else "underestimate" if e < x else "exact"
    return str(text).strip() == want


@reg
def outlier_effect(chk, text):
    def med(a):
        a = sorted(a)
        k = len(a)
        return F(a[k // 2]) if k % 2 else F(a[k // 2 - 1] + a[k // 2], 2)
    b = [F(x) for x in chk["base"]]
    n = b + [F(chk["new"])]
    dm = sum(n) / len(n) - sum(b) / len(b)
    dmed = med(n) - med(b)
    t = str(text)
    truth = {"The mean increases more than the median.": dm > dmed and dm > 0, "The median increases more than the mean.": dmed > dm,
             "Both stay the same.": dm == 0 and dmed == 0, "The mean decreases.": dm < 0}
    return truth.get(t, False)


@reg
def divides(chk, text):
    return str(text).strip() == ("Yes" if chk["n"] % chk["d"] == 0 else "No")


@reg
def num_factors(chk, text):
    n = chk["n"]
    return str(text).strip() == str(sum(1 for d in range(1, n + 1) if n % d == 0))


@reg
def prime_q(chk, text):
    try:
        n = int(str(text).strip())
    except ValueError:
        return False
    return _isprime(n) if chk["want"] == "prime" else (n > 1 and not _isprime(n))


@reg
def missing_digit(chk, text):
    t = str(text).strip()
    return t.isdigit() and len(t) == 1 and (chk["a"] + chk["b"] + int(t)) % chk["d"] == 0


@reg
def gcf(chk, text):
    try:
        g = int(str(text).strip())
    except ValueError:
        return False
    return g > 0 and all(n % g == 0 for n in chk["nums"]) and not any(all(n % h == 0 for n in chk["nums"]) for h in range(g + 1, min(chk["nums"]) + 1))


@reg
def lcm(chk, text):
    try:
        m = int(str(text).replace(",", "").strip())
    except ValueError:
        return False
    return m > 0 and all(m % n == 0 for n in chk["nums"]) and not any(all(k % n == 0 for n in chk["nums"]) for k in range(1, m))


@reg
def missing_frac(chk, text):
    try:
        s = chk["st"].replace("?", str(text).strip())
        l, r_ = s.split("=")
        return M.same(M.ev(l), M.ev(r_))
    except Exception:
        return False


@reg
def sqrt_tenth(chk, text):
    return C.round_text(math.sqrt(chk["n"]), 1) == str(text).strip()


@reg
def size_claim(chk, text):
    v, ref = M.ev(chk["expr"]), M.ev(chk["ref"])
    t = str(text)
    want = "less than" if v < ref else "greater than" if v > ref else "equal to"
    return t.startswith(want + " ")


@reg
def better_buy(chk, text):
    unit = {k: F(v[0]) / F(v[1]) for k, v in chk["deals"].items()}
    best = min(unit, key=unit.get)
    return str(text) == best and len(set(unit.values())) == len(unit)


@reg
def is_prop(chk, text):
    ok = chk["a"] * chk["d"] == chk["b"] * chk["c"]
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def eq_val(chk, text):
    """Answer value (units allowed) solves the linear equation chk['eq'] for chk['var']."""
    try:
        sol = M.solve_linear(chk["eq"], chk.get("var", "x"))
        return sol[0] == "one" and M.same(M.val(text), sol[1])
    except Exception:
        return False


@reg
def likelihood(chk, text):
    p = F(chk["p"])
    want = "impossible" if p == 0 else "certain" if p == 1 else "unlikely" if p < F(1, 2) else "likely" if p > F(1, 2) else "equally likely as not"
    return str(text) == want


@reg
def extreme_pct(chk, text):
    def v(t):
        return M.ev(t.replace("%", "")) / 100 if t.endswith("%") else M.ev(t)
    vals = {t: v(t) for t in chk["items"]}
    m = max(vals.values())
    return str(text) in vals and vals[str(text)] == m and list(vals.values()).count(m) == 1


@reg
def pct_change(chk, text):
    old, new = M.ev(chk["old"]), M.ev(chk["new"])
    p = abs(new - old) / old * 100
    t = str(text).strip()
    m = re.fullmatch(r"(\d+(?:\.\d+)?)%(?:\s+(increase|decrease))?", t)
    if not m:
        return False
    if F(m.group(1)) != p:
        return False
    if chk.get("bare"):
        return m.group(2) is None
    return m.group(2) == ("increase" if new > old else "decrease")


@reg
def prop_table(chk, text):
    rs = {F(y, x) for x, y in zip(chk["xs"], chk["ys"])}
    return str(text).strip() == ("Yes" if len(rs) == 1 else "No")


@reg
def formula(chk, text):
    """'v = expr' solves the original formula for v: for sampled values of the other variables, substituting
    expr for v makes the original formula true."""
    t = str(text)
    m = re.fullmatch(r"\s*([A-Za-z])\s*=\s*(.+)", t)
    if not m or m.group(1) != chk["target"]:
        return False
    rhs = m.group(2)
    if chk["target"] in re.sub(r"π", "", rhs):
        return False
    l, r_ = chk["orig"].split("=")
    others = [v for v in chk["vars"] if v != chk["target"]]
    try:
        for k in range(4):
            env = {v: F(2 + 3 * j + k, 1 + (j + k) % 3) for j, v in enumerate(others)}
            env[chk["target"]] = M.ev(rhs, env)
            if not M.same(M.ev(l, env), M.ev(r_, env)):
                return False
        return True
    except Exception:
        return False


@reg
def interest_cmp(chk, text):
    p, rt, t = F(chk["p"]), F(chk["rate"], 100), chk["t"]
    s, c = p * rt * t, p * (1 + rt) ** t - p
    want = "Compound interest earns more." if c > s else "Simple interest earns more." if s > c else "They earn the same amount."
    return str(text) == want


@reg
def is_func(chk, text):
    xs = [p[0] for p in chk["pts"]]
    ok = all(len({tuple(q) for q in chk["pts"] if q[0] == x}) == 1 for x in xs)
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def func_claim(chk, text):
    xs = [p[0] for p in chk["pts"]]
    ys = [p[1] for p in chk["pts"]]
    ok = len(set(xs)) == len(xs)
    t = str(text)
    truth = {"Yes, it passes the vertical line test.": ok, "No, two points lie on the same vertical line.": not ok,
             "Yes, because no two points share a y-value.": False, "No, because the points are not on a line.": False}
    return truth.get(t, False)


def _rel2(s, x, y):
    l, op, r_ = REL.split(s)
    env = {"x": F(x), "y": F(y)}
    return OPS[op](M.ev(l, env), M.ev(r_, env))


@reg
def is_sol2(chk, text):
    ok = _rel2(chk["eq"], M.ev(chk["x"]), M.ev(chk["y"]))
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def sys_point(chk, text):
    ok = all(_rel2(e, M.ev(chk["x"]), M.ev(chk["y"])) for e in chk["eqs"])
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def sys_count(chk, text):
    s = M.solve_system(*chk["eqs"])
    want = {"one": "exactly one solution", "none": "no solution", "all": "infinitely many solutions"}[s[0]]
    return str(text) == want


@reg
def slope_type(chk, text):
    (x1, y1), (x2, y2) = chk["p"], chk["q"]
    want = "undefined" if x1 == x2 else "zero" if y1 == y2 else "positive" if (y2 - y1) * (x2 - x1) > 0 else "negative"
    return str(text) == want


@reg
def corr_type(chk, text):
    xs, ys = chk["xs"], chk["ys"]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    rr = sxy / math.sqrt(sxx * syy)
    want = "positive correlation" if rr > 0.6 else "negative correlation" if rr < -0.6 else "no correlation" if abs(rr) < 0.3 else "?"
    return str(text) == want


@reg
def shade_match(chk, text):
    """Option inequality has exactly the graphed region (boundary y = mx + b, given op) — sampled on a grid."""
    m, b, op = F(chk["m"]), F(chk["b"]), chk["op"]
    try:
        for x in range(-6, 7):
            for k in range(-24, 25):
                y = F(k, 2)
                if _rel2(str(text), x, y) != OPS[op](y, m * x + b):
                    return False
        return True
    except Exception:
        return False


@reg
def boundary_rule(chk, text):
    op = chk["op"]
    want = f"{'solid' if op in ('≤', '≥') else 'dashed'} line, shade {'above' if op in ('>', '≥') else 'below'}"
    return str(text) == want


@reg
def tri_classify(chk, text):
    a, b = chk["a"], chk["b"]
    c = 180 - a - b
    big = max(a, b, c)
    want = f"x = {c}, " + ("obtuse" if big > 90 else "right" if big == 90 else "acute")
    return str(text).strip() == want


@reg
def congruent_part(chk, text):
    left, right, tgt = chk["left"], chk["right"], chk["target"]
    src = "".join(left[right.index(ch)] for ch in tgt)
    val = chk["sides"].get(src) or chk["sides"].get(src[::-1])
    try:
        return M.same(M.val(text), F(val))
    except Exception:
        return False


@reg
def pi_coef(chk, text):
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?(?:/\d+)?)π(?:\s+\S.*)?\s*", str(text))
    return bool(m) and F(m.group(1)) == F(chk["k"])


@reg
def trans_rule(chk, text):
    m = re.fullmatch(r"\(x, y\) → \(x ([+-]) (\d+), y ([+-]) (\d+)\)", str(text).strip())
    if not m:
        return False
    h = int(m.group(2)) * (1 if m.group(1) == "+" else -1)
    k = int(m.group(4)) * (1 if m.group(3) == "+" else -1)
    (x, y), (a, b) = chk["p"], chk["q"]
    return x + h == a and y + k == b


SYM = {"regular triangle": 3, "regular quadrilateral": 4, "regular pentagon": 5, "regular hexagon": 6, "regular octagon": 8, "rectangle (not a square)": 2,
       "rhombus (not a square)": 2, "isosceles triangle (not equilateral)": 1, "parallelogram (not a rectangle or rhombus)": 0}


@reg
def symmetry(chk, text):
    return str(text).strip() == str(SYM[chk["shape"]])


@reg
def rot_sym(chk, text):
    ok = (chk["deg"] * chk["n"]) % 360 == 0
    return str(text).strip() == ("Yes" if ok else "No")


@reg
def rot_angle(chk, text):
    (x, y), (a, b) = chk["p"], chk["q"]
    for d, f in ((90, lambda x, y: (-y, x)), (180, lambda x, y: (-x, -y)), (270, lambda x, y: (y, -x))):
        if f(x, y) == (a, b):
            return str(text).strip() == f"{d}°"
    return False


@reg
def rot_sym_opt(chk, text):
    d = int(str(text).strip().rstrip("°"))
    return 0 < d < 360 and (d * chk["n"]) % 360 == 0


@reg
def solid_count(chk, text):
    s = chk["solid"]
    n = {"triangular": 3, "rectangular": 4, "square": 4, "pentagonal": 5, "hexagonal": 6}[s.split()[0]]
    if s.endswith("prism"):
        f, v, e = n + 2, 2 * n, 3 * n
    else:
        f, v, e = n + 1, n + 1, 2 * n
    return str(text).strip() == str({"faces": f, "vertices": v, "edges": e}[chk["what"]])


@reg
def cone_cyl(chk, text):
    cyl = F(chk["rad"] ** 2 * chk["h"])
    cone = cyl / 3
    truth = {"The cylinder's volume is 3 times the cone's.": cyl == 3 * cone, "The cone's volume is 3 times the cylinder's.": cone == 3 * cyl,
             "They have the same volume.": cone == cyl, "The cylinder's volume is 2 times the cone's.": cyl == 2 * cone}
    return truth.get(str(text), False)


@reg
def closest_int(chk, text):
    n = chk["n"]
    try:
        k = int(str(text).strip())
    except ValueError:
        return False
    return all(abs(k * k - n) < abs(j * j - n) for j in range(0, n + 2) if j != k)


@reg
def right_tri(chk, text):
    a, b, c = sorted(chk["sides"])
    return str(text).strip() == ("Yes" if a * a + b * b == c * c else "No")


@reg
def trig_ratio(chk, text):
    o, a, h = chk["opp"], chk["adj"], chk["hyp"]
    want = {"sin": F(o, h), "cos": F(a, h), "tan": F(o, a)}[chk["f"]]
    try:
        return M.same(M.val(text), want)
    except Exception:
        return False


@reg
def trig_side(chk, text):
    f = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[chk["f"]](math.radians(chk["ang"]))
    v = chk["known"] * f if chk["mode"] == "mult" else chk["known"] / f
    v += chk.get("add", 0)
    return C.round_text(v, chk.get("places", 1)) == M.strip_units(text)


@reg
def trig_angle(chk, text):
    v = math.degrees(math.atan(chk["opp"] / chk["adj"]))
    return C.round_text(v, 0) == M.strip_units(str(text)).rstrip("°")


@reg
def count_ge(chk, text):
    return str(text).strip() == str(sum(1 for v in chk["data"] if v >= chk["k"]))


@reg
def count_gt(chk, text):
    return str(text).strip() == str(sum(1 for v in chk["data"] if v > chk["k"]))


@reg
def box_read(chk, text):
    a = chk["five"]
    v = {"median": a[2], "q1": a[1], "q3": a[3], "iqr": a[3] - a[1], "range": a[4] - a[0]}[chk["stat"]]
    return str(text).strip() == str(v)


@reg
def box_compare(chk, text):
    a, b, q = chk["a"], chk["b"], chk["q"]
    va, vb = (a[2], b[2]) if q == "median" else (a[3] - a[1], b[3] - b[1])
    word = "median" if q == "median" else "interquartile range"
    truth = {f"Class A has the greater {word}.": va > vb, f"Class B has the greater {word}.": vb > va, f"The classes have the same {word}.": va == vb, "The plots cannot be compared.": False}
    return truth.get(str(text), False)


@reg
def dice_prob(chk, text):
    ev = chk["event"]
    outs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    if ev == "doubles":
        k = sum(1 for a, b in outs if a == b)
    else:
        s = int(re.search(r"\d+", ev).group(0))
        k = sum(1 for a, b in outs if a + b == s)
    return C.CUSTOM["frac_simplest"]({"expr": f"{k}/36", "mixed": False}, text)


@reg
def bag_prob(chk, text):
    R, B, rep = chk["red"], chk["blue"], chk["repl"]
    t = R + B
    p = F(R, t) * (F(R, t) if rep else F(R - 1, t - 1))
    return C.CUSTOM["frac_simplest"]({"expr": f"{p.numerator}/{p.denominator}", "mixed": False}, text) if p else str(text).strip() == "0"


@reg
def coin_prob(chk, text):
    from itertools import product
    outs = list(product("HT", repeat=chk["n"]))
    if chk["mode"] == "exactly":
        k = sum(1 for o in outs if o.count("H") == chk["k"])
    else:
        k = sum(1 for o in outs if "H" in o)
    return C.CUSTOM["frac_simplest"]({"expr": f"{k}/{len(outs)}", "mixed": False}, text)


@reg
def seq_type(chk, text):
    s = [F(x) for x in chk["seq"]]
    d = {b - a for a, b in zip(s, s[1:])}
    q = {b / a for a, b in zip(s, s[1:])} if all(s) else set()
    want = "arithmetic" if len(d) == 1 and len(q) != 1 else "geometric" if len(q) == 1 and len(d) != 1 else "both arithmetic and geometric" if len(d) == 1 else "neither"
    return str(text) == want


@reg
def graph_choice(chk, text):
    return chk["graphs"].get(str(text)) == chk["f"]


@reg
def is_linear_fn(chk, text):
    rhs = str(text).split("=", 1)[1]
    vals = [abs_eval(rhs.replace("x", f"({x})")) for x in range(-3, 4)]
    d = [b - a for a, b in zip(vals, vals[1:])]
    lin_ = len(set(d)) == 1
    return lin_ if chk["want"] == "linear" else not lin_


@reg
def growth_decay(chk, text):
    b = F(chk["b"])
    return str(text) == ("exponential growth" if b > 1 else "exponential decay" if 0 < b < 1 else "?")


def _terms(p):
    t = str(p).replace(" - ", " + -").split(" + ")
    return [x.strip() for x in t if x.strip()]


@reg
def poly_degree(chk, text):
    best = 0
    for t in _terms(chk["p"]):
        deg = 0
        for v, e in re.findall(r"([a-z])([⁰¹²³⁴⁵⁶⁷⁸⁹]*)", t):
            deg += int("".join(M.SUP2[c] for c in e)) if e else 1
        best = max(best, deg)
    return str(text).strip() == str(best)


@reg
def poly_terms(chk, text):
    n = len(_terms(chk["p"]))
    return str(text) == {1: "monomial", 2: "binomial", 3: "trinomial"}.get(n, "polynomial")


@reg
def freq_most(chk, text):
    fr = chk["fr"]
    m = max(fr)
    return fr.count(m) == 1 and str(text) == chk["cats"][fr.index(m)]
