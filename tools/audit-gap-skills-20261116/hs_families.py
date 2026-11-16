"""High-school gap skills (2026-11-16).

Algebra 2, polynomial-functions: "Binomial Theorem and Pascal's Triangle" (A-APR.C.5).
Precalculus, functions: "Solving Exponential and Logarithmic Equations" (F-LE.A.4, F-BF.B.5).
Calculus, fundamental-theorem-calculus: "Integration Using Long Division and Completing the Square" (AP FUN-6.D).
"""
import math
from fractions import Fraction as F
from core import I, Reject, need, ri, g, W, levels, safe_round
from fmt import sup, num, coef, join, poly

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def sub(n):
    return str(n).translate(SUB)


def ordinal(n):
    return {1: "1st", 2: "2nd", 3: "3rd"}.get(n, f"{n}th")


# ---------------------------------------------------------------- binomial theorem
def binom(r, L, big=False):
    if L == 0:
        a, b, n = 1, r.choice([-3, -2, -1, 1, 2, 3]), r.choice([3, 4])
    elif L == 1:
        a, b, n = r.choice([1, 1, 2, 3]), r.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5]), r.choice([3, 4, 5])
        need(not (a > 1 and n == 5))
    else:
        a, b, n = r.choice([1, 2, 3, 4]), r.choice([-5, -3, -2, -1, 1, 2, 3, 5]), r.choice([4, 5, 6])
        need(not (a > 2 and n > 4) and not (a == 2 and n == 6))
    if big:
        n += r.choice([0, 1, 2])
    return a, b, n, f"({poly({1: a, 0: b})}){sup(n)}"


def expand(a, b, n, cf=math.comb):
    return {n - k: cf(n, k) * a ** (n - k) * b ** k for k in range(n + 1)}


def b_expand(r, L):
    a, b, n, e = binom(r, L)
    prompt = f"Use the Binomial Theorem to expand {e}."
    ans = poly(expand(a, b, n))
    wr = [(poly({n: a ** n, 0: b ** n}), "raised each term to the power and left out the middle terms"),
          (poly(expand(a, b, n, lambda n_, k: 1)), "left out the binomial coefficients from Pascal's triangle"),
          (poly(expand(a, abs(b), n)) if b < 0 else poly(expand(a, -b, n)), "made a sign error; the signs follow the powers of the second term"),
          (poly({n - k: math.comb(n, k) * b ** k for k in range(n + 1)}), f"did not raise the coefficient {a} to the powers of the first term")
          if a != 1 else (poly({n - k: math.comb(n, k) * (b if k else 1) for k in range(n + 1)}), f"did not raise {num(b)} to increasing powers")]
    row = ", ".join(str(math.comb(n, k)) for k in range(n + 1))
    steps = [f"Row {n} of Pascal's triangle gives the coefficients {row}.", f"Multiply each coefficient by decreasing powers of {coef(a, 'x')} and increasing powers of {num(b)}.", f"{e} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="ident", var="x", e=e, show=[e]), "binomial_expand")


def b_coef(r, L):
    a, b, n, e = binom(r, L, big=L > 0)
    p = ri(r, 1, n - 1)
    k = n - p
    c = math.comb(n, k) * a ** p * b ** k
    prompt = f"Find the coefficient of x{sup(p) if p > 1 else ''} in the expansion of {e}."
    ans = str(c)
    wr = [(str(a ** p * b ** k), "left out the binomial coefficient"), (str(math.comb(n, k)), "gave only the binomial coefficient"), (str(math.comb(n, k) * a ** p * abs(b) ** k * (-1 if c > 0 else 1)), "made a sign error"),
          (str(math.comb(n, k) * a ** k * b ** p), "switched the exponents on the two terms"), (str(math.comb(n, k) * b ** k), f"did not raise {a} to the power {p}")]
    steps = [f"The x{sup(p) if p > 1 else ''} term is {sub(n)}C{sub(k)} · ({coef(a, 'x')}){sup(p)} · ({num(b)}){sup(k)}.", f"{math.comb(n, k)} · {a ** p} · {num(b ** k)} = {c}."]
    return I(prompt, ans, steps, wr, dict(k="coefOf", e=e, p=p, show=[e, f"coefficient of x{sup(p) if p > 1 else ''} in"]), "binomial_coefficient")


def b_term(r, L):
    a, b, n, e = binom(r, L, big=L > 0)
    idx = ri(r, 2, n)
    k = idx - 1
    p = n - k
    c = math.comb(n, k) * a ** p * b ** k
    t = lambda c_, p_: coef(c_, "x" + (sup(p_) if p_ > 1 else "")) if p_ > 0 else num(c_)
    prompt = f"Find the {ordinal(idx)} term in the expansion of {e}, written in descending powers of x."
    ans = t(c, p)
    wr = [(t(a ** p * b ** k, p), "left out the binomial coefficient"), (t(math.comb(n, idx) * a ** (n - idx) * b ** idx, n - idx) if idx <= n else t(c, p + 1), f"used k = {idx}; the {ordinal(idx)} term uses k = {idx - 1}"),
          (t(-c, p), "made a sign error"), (t(math.comb(n, k) * a ** p * b ** k, k), "put the wrong exponent on x")]
    steps = [f"The {ordinal(idx)} term uses k = {k}: {sub(n)}C{sub(k)} · ({coef(a, 'x')}){sup(p)} · ({num(b)}){sup(k)}.", f"{math.comb(n, k)} · {coef(a ** p, 'x' + (sup(p) if p > 1 else ''))} · {num(b ** k)} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="termOf", e=e, idx=idx, show=[e, f"the {ordinal(idx)} term"]), "binomial_term")


def b_pascal(r, L):
    n = ri(r, 3, 6) if L == 0 else ri(r, 4, 8) if L == 1 else ri(r, 6, 9)
    row = lambda m: ", ".join(str(math.comb(m, k)) for k in range(m + 1))
    style = r.choice([0, 1])
    prompt = (f"Write row {n} of Pascal's triangle (the row that begins 1, {n})." if style == 0 else f"List the coefficients, in order, of the expansion of (a + b){sup(n)}.")
    ans = row(n)
    wr = [(row(n - 1), f"gave row {n - 1}"), (row(n + 1), f"gave row {n + 1}"), (", ".join(str(2 ** k) for k in range(n + 1)), "doubled each entry instead of adding the two entries above"),
          (", ".join(["1"] + [str(n)] * (n - 1) + ["1"]), f"repeated {n} instead of adding the two entries above")]
    steps = ["Each entry is the sum of the two entries above it; every row begins and ends with 1.", f"Row {n - 1}: {row(n - 1)}.", f"Row {n}: {ans}."]
    return I(prompt, ans, steps, wr, dict(k="pascal", n=n, show=[f"row {n} " if style == 0 else f"(a + b){sup(n)}"]), "pascal_row")


def b_choose(r, L):
    n = ri(r, 4, 7) if L == 0 else ri(r, 5, 10) if L == 1 else ri(r, 8, 13)
    k = ri(r, 1 if L == 0 else 2, n - 1)
    c = math.comb(n, k)
    prompt = f"Evaluate the binomial coefficient {sub(n)}C{sub(k)}."
    ans = str(c)
    wr = [(str(math.perm(n, k)), "counted ordered arrangements (did not divide by k!)"), (str(n * k), "multiplied n by k"), (str(math.comb(n, k - 1) if math.comb(n, k - 1) != c else math.comb(n + 1, k)), "used the neighboring entry of Pascal's triangle"), (str(n ** k), "raised n to the power k")]
    steps = [f"{sub(n)}C{sub(k)} = {n}! ÷ ({k}! · {n - k}!).", f"= {math.perm(n, min(k, n - k))} ÷ {math.factorial(min(k, n - k))} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="choose", n=n, kk=k, show=[f"{sub(n)}C{sub(k)}"]), "binomial_choose")


def b_sum(r, L):
    levels(L, 1, 2)
    a, b, n, e = binom(r, L)
    need(a + b not in (0, 1))
    prompt = f"What is the sum of the coefficients in the expansion of {e}? (Hint: substitute x = 1.)"
    ans = str((a + b) ** n)
    wr = [(str(2 ** n), "used 2ⁿ, which is the sum only for (x + 1)ⁿ"), (str(a ** n + b ** n), "added only the first and last coefficients"), (str(n * (a + b)), "multiplied by the exponent instead of raising to the power"), (str((abs(a) + abs(b)) ** n), "ignored the sign of the second term")]
    steps = ["Substituting x = 1 makes every power of x equal 1, leaving the sum of the coefficients.", f"({num(a)} + {num(b)}){sup(n)} = ({a + b}){sup(n)} = {ans}." if b > 0 else f"({num(a)} - {num(-b)}){sup(n)} = ({a + b}){sup(n)} = {ans}."]
    return I(prompt, ans, steps, wr, dict(k="sumCoef", e=e, show=[e]), "binomial_coefficient_sum")


# ---------------------------------------------------------------- exponential / log equations
def lin(a, b, v="x"):
    return poly({1: a, 0: b}, v)


def pw(base, ex):
    return f"{base}ˣ" if ex == "x" else f"{base}^({ex})"


def x_same(r, L):
    if L < 2:
        b = r.choice([2, 3, 4, 5] if L == 0 else [2, 3, 5, 7])
        a = 1 if L == 0 else r.choice([1, 2, 3])
        c = r.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        m = ri(r, 2, 6 if b == 2 else 4 if b == 3 else 3)
        x = F(m - c, a)
        need(x != 0)
        eq = f"{pw(b, lin(a, c))} = {b ** m}"
        steps = [f"Write {b ** m} as a power of {b}: {b ** m} = {b}{sup(m)}.", f"The bases match, so {lin(a, c)} = {m}.", f"x = {num(x)}."]
        wr = [(f"x = {num(F(m + c, a))}", "moved the constant with the wrong sign"), (f"x = {num(F(b ** m - c, a))}", f"set the exponent equal to {b ** m} instead of rewriting {b ** m} as a power of {b}"), (f"x = {m}", "set x equal to the exponent and ignored the rest of the expression"), (f"x = {num(F(b ** m, b) - c)}", f"divided {b ** m} by {b} instead of using exponents")]
    else:
        b, (p, q) = r.choice([(2, (2, 3)), (3, (2, 3)), (2, (1, 3)), (3, (1, 2)), (5, (1, 2)), (2, (2, 5)), (2, (3, 4))])
        c, d = r.choice([-3, -2, -1, 1, 2, 3]), r.choice([-4, -2, -1, 1, 2, 4, 5])
        # (b^p)^(x + c) = (b^q)^(x + d)  →  p(x + c) = q(x + d)
        x = F(q * d - p * c, p - q)
        need(x.denominator in (1, 2) and x != 0 and c != d)
        eq = f"{pw(b ** p, lin(1, c))} = {pw(b ** q, lin(1, d))}"
        steps = [f"Write both sides with base {b}: {b}^({p}({lin(1, c)})) = {b}^({q}({lin(1, d)})).", f"Set the exponents equal: {lin(p, p * c)} = {lin(q, q * d)}.", f"x = {num(x)}."]
        wr = [(f"x = {num(F(d - c, 1))}" if d != c else "x = 0", "set the exponents equal without first rewriting with a common base"), (f"x = {num(-x)}", "made a sign error when solving"), (f"x = {num(F(q * d - p * c, p + q))}", "added the x-terms instead of subtracting"), ("no solution", "decided the equation could not be solved because the bases differ")]
    ans = f"x = {num(x)}"
    return I(f"Solve {eq}.", ans, steps, wr, dict(k="solve", eq=eq, var="x", show=[eq]), "exp_same_base")


def x_log(r, L):
    b = r.choice([2, 3, 5, 7] if L < 2 else [1.5, 2, 3, 4, 6, 1.08])
    A = 1 if L == 0 else r.choice([2, 3, 4, 5, 6])
    N = ri(r, 12, 400)
    need(N % A == 0 if L < 2 else True)
    need(A != b)
    ratio = N / A
    x = math.log(ratio) / math.log(b)
    need(abs(x - round(x)) > 1e-6 and 0.3 < abs(x) < 60)
    safe_round(x, 3)
    lhs = (f"{A}·" if A != 1 else "") + (f"({g(b)})ˣ" if b != int(b) else f"{int(b)}ˣ")
    eq = f"{lhs} = {N}"
    ans = f"x ≈ {x:.3f}"
    rt = g(ratio, 6)
    steps = ([f"Divide by {A}: {g(b)}ˣ = {rt}."] if A != 1 else []) + [f"Take a logarithm of both sides: x · ln({g(b)}) = ln({rt}).", f"x = ln({rt}) ÷ ln({g(b)}) ≈ {x:.3f}."]
    wr = [(f"x ≈ {ratio / b:.3f}", f"divided by the base {g(b)} instead of taking a logarithm"), (f"x ≈ {math.log(ratio):.3f}", f"did not divide by ln({g(b)})"), (f"x ≈ {math.log(b) / math.log(ratio):.3f}", "divided the logarithms in the wrong order"),
          (f"x ≈ {math.log(N) / math.log(A * b):.3f}" if A != 1 else f"x ≈ {math.log10(ratio):.3f}", f"multiplied {A} by the base before taking logarithms" if A != 1 else "took a common logarithm of one side only")]
    return I(f"Solve {eq}. Round to the nearest thousandth.", ans, steps, wr, dict(k="solve", eq=eq, var="x", dp=3, show=[eq]), "exp_take_logs")


def x_e(r, L):
    k = r.choice([1, 2, 3] if L == 0 else [2, 3, 0.5, 0.2, 4] if L == 1 else [0.5, 0.25, 0.04, 1.5, -0.5, -0.2, 3])
    A = 1 if L == 0 else r.choice([2, 3, 4, 5, 10])
    c = 0 if L < 2 else r.choice([-9, -6, -4, 3, 5, 8])
    N = ri(r, 5, 90)
    ratio = F(N - c, A)
    need(ratio > 0 and ratio != 1)
    x = math.log(ratio) / k
    need(0.05 < abs(x) < 60)
    safe_round(x, 3)
    ex = "x" if k == 1 else f"({g(k)}x)" if True else ""
    et = "e^x" if k == 1 else f"e^({g(k)}x)"
    lhs = (f"{A}" if A != 1 else "") + et + (f" + {c}" if c > 0 else f" - {-c}" if c < 0 else "")
    eq = f"{lhs} = {N}"
    ans = f"x ≈ {x:.3f}"
    rt = num(ratio) if ratio.denominator == 1 else f"({num(ratio)})"
    steps = ([f"Isolate the exponential: {et} = {num(ratio)}."] if (A != 1 or c) else []) + [f"Take the natural logarithm of both sides: {'x' if k == 1 else g(k) + 'x'} = ln{rt if rt.startswith('(') else '(' + rt + ')'}.", f"x ≈ {x:.3f}."]
    wr = [(f"x ≈ {math.log(float(ratio)):.3f}", f"did not divide by {g(k)}") if k != 1 else (f"x ≈ {float(ratio) / math.e:.3f}", "divided by e instead of taking a natural logarithm"),
          (f"x ≈ {math.log10(float(ratio)) / k:.3f}", "used the common logarithm instead of the natural logarithm"),
          (f"x ≈ {math.log(N) / k:.3f}" if (A != 1 or c) else f"x ≈ {math.log(float(ratio)) * 2:.3f}", "took the logarithm before isolating the exponential" if (A != 1 or c) else "doubled the logarithm"),
          (f"x ≈ {float(ratio) / k:.3f}", "dropped the exponential without taking a logarithm")]
    return I(f"Solve {eq}. Round to the nearest thousandth.", ans, steps, wr, dict(k="solve", eq=eq, var="x", dp=3, show=[eq]), "exp_natural_base")


def logt(b, arg):
    return f"ln({arg})" if b == "e" else f"log({arg})" if b == 10 else f"log{sub(b)}({arg})"


def x_logeq(r, L):
    b = r.choice([2, 3, 4, 5, 10] if L < 2 else [2, 3, 5, 10])
    a = 1 if L == 0 else r.choice([1, 2, 3, 5])
    c = r.choice([-7, -5, -3, -2, -1, 1, 2, 3, 4, 6])
    m = ri(r, 1, 6 if b == 2 else 4 if b == 3 else 3 if b < 10 else 2)
    A = 1 if L < 2 else r.choice([2, 3])
    k = 0 if L == 0 else r.choice([0, 0, -3, -1, 1, 2, 5])
    x = F(b ** m - c, a)
    need(x != 0 and x.denominator in (1, 2, 3, 5))
    rhs = A * m + k
    lhs = (f"{A}" if A != 1 else "") + logt(b, lin(a, c)) + (f" + {k}" if k > 0 else f" - {-k}" if k < 0 else "")
    eq = f"{lhs} = {rhs}"
    ans = f"x = {num(x)}"
    steps = ([f"Isolate the logarithm: {logt(b, lin(a, c))} = {m}."] if (A != 1 or k) else []) + [f"Rewrite in exponential form: {lin(a, c)} = {b}{sup(m)} = {b ** m}.", f"x = {num(x)}."]
    wr = [(f"x = {num(F(b * m - c, a))}", f"multiplied {b} by {m} instead of raising {b} to the power {m}"), (f"x = {num(F(m ** b - c, a))}" if m ** b < 10 ** 6 else "x = 1", "switched the base and the exponent"), (f"x = {num(F(b ** m + c, a))}", "moved the constant with the wrong sign"),
          (f"x = {num(F(b ** rhs - c, a))}" if (A != 1 or k) and 0 < rhs < 9 else f"x = {num(F(m - c, a))}", "did not isolate the logarithm first" if (A != 1 or k) else "dropped the logarithm without rewriting in exponential form")]
    return I(f"Solve {eq}.", ans, steps, wr, dict(k="solve", eq=eq, var="x", show=[eq]), "log_to_exponential")


def x_logsum(r, L):
    levels(L, 1, 2)
    b = r.choice([2, 3, 4, 5, 6, 10])
    m = ri(r, 1, 5 if b == 2 else 3 if b < 5 else 2)
    V = b ** m
    pairs = [(p, V // p) for p in range(1, V + 1) if V % p == 0 and p != V // p]
    need(pairs)
    p, q = r.choice(pairs)          # x = p is the solution, x = -q is extraneous
    d = q - p                        # log(x) + log(x + d) = m  →  x² + dx − V = 0
    need(d != 0 and p <= 200)
    eq = f"{logt(b, 'x')} + {logt(b, lin(1, d))} = {m}"
    ans = f"x = {p}"
    steps = [f"Combine the logarithms: {logt(b, 'x(' + lin(1, d) + ')')} = {m}.", f"Rewrite in exponential form: x({lin(1, d)}) = {b}{sup(m)} = {V}, so {poly({2: 1, 1: d, 0: -V})} = 0.",
             f"Factor: (x - {p})(x + {q}) = 0, so x = {p} or x = -{q}.", f"x = -{q} makes {logt(b, 'x')} undefined, so the only solution is x = {p}."]
    wr = [(f"x = {p} or x = -{q}", f"kept the extraneous solution x = -{q}, which makes a logarithm undefined"), (f"x = {num(F(V - d, 2))}", "added the arguments instead of multiplying them"), (f"x = -{q}", "kept the extraneous solution and rejected the valid one"), (f"x = {q}", "made a sign error when factoring")]
    return I(f"Solve {eq}.", ans, steps, wr, dict(k="solve", eq=eq, var="x", show=[eq]), "log_sum_extraneous")


def x_quad(r, L):
    levels(L, 2)
    u1 = ri(r, 2, 9)
    u2 = r.choice([x for x in [-5, -4, -3, -2, -1, 2, 3, 4, 5, 6, 7] if x != u1])
    s, pr = u1 + u2, u1 * u2
    eq = f"{join(['e^(2x)', coef(-s, 'e^x'), num(pr)])} = 0"
    need(s != 0)
    if u2 > 0:
        lo, hi = sorted([u1, u2])
        ans = f"x = ln({lo}) or x = ln({hi})"
    else:
        ans = f"x = ln({u1})"
    fac = f"(e^x - {u1})(e^x {'- ' + str(u2) if u2 > 0 else '+ ' + str(-u2)}) = 0"
    steps = [f"Let u = e^x. Then {poly({2: 1, 1: -s, 0: pr}, 'u')} = 0.", f"Factor: {fac}, so e^x = {u1} or e^x = {u2}.",
             (f"Both values are positive, so {ans}." if u2 > 0 else f"e^x is never negative, so e^x = {u2} has no solution. The only solution is {ans}.")]
    wr = [(f"x = {min(u1, u2)} or x = {max(u1, u2)}", "solved for u = e^x but did not solve for x"), ((f"x = ln({u1}) or x = ln({u2})") if u2 < 0 else f"x = ln({u1 + u2})", "kept a value that requires the logarithm of a negative number" if u2 < 0 else "added the two values of e^x"),
          (f"x = e^({u1})" if u2 < 0 else f"x = e^({min(u1, u2)}) or x = e^({max(u1, u2)})", "raised e to the values instead of taking natural logarithms"), (f"x = ln({abs(pr)})", "used the constant term as the value of e^x")]
    return I(f"Solve {eq}. Give exact solutions.", ans, steps, wr, dict(k="solve", eq=eq, var="x", exact=True, show=[eq]), "exp_quadratic_form")


APPS = [("A town's population is modeled by P(t) = {A}e^({k}t), where t is the number of years after 2020.", "{A}e^({k}t)", "the population reaches {N}", "years", "e"),
        ("An investment is worth V(t) = {A}({b})^t dollars after t years.", "{A}({b})^t", "the investment is worth {N} dollars", "years", "b"),
        ("A sample of a radioactive substance has mass M(t) = {A}e^({k}t) grams after t days.", "{A}e^({k}t)", "{N} grams remain", "days", "e-"),
        ("A bacteria culture has N(t) = {A}({b})^t cells after t hours.", "{A}({b})^t", "the culture has {N} cells", "hours", "b")]


def x_app(r, L):
    levels(L, 1, 2)
    sent, form, when, unit, kind = r.choice(APPS)
    if kind == "e":
        A, k = r.choice([500, 1200, 2500, 8000]), r.choice([0.02, 0.03, 0.045, 0.06])
        N = int(A * r.choice([1.5, 2, 2.5, 3]))
        t = math.log(N / A) / k
        f = dict(A=A, k=g(k), N=N)
    elif kind == "e-":
        A, k = r.choice([80, 120, 200, 500]), -r.choice([0.03, 0.05, 0.08, 0.12])
        N = int(A * r.choice([0.5, 0.25, 0.4, 0.1]))
        t = math.log(N / A) / k
        f = dict(A=A, k=g(k), N=N)
    else:
        A, b = r.choice([400, 1500, 2000, 5000]), r.choice([1.04, 1.05, 1.08, 1.12, 1.5, 2])
        N = int(A * r.choice([1.5, 2, 3, 4]))
        t = math.log(N / A) / math.log(b)
        f = dict(A=A, b=g(b), N=N)
    safe_round(t, 1)
    need(0.5 < t < 150)
    eq = f"{form.format(**f)} = {N}"
    prompt = f"{sent.format(**f)} Solve {eq} to find when {when.format(**f)}. Round to the nearest tenth."
    ans = f"t ≈ {t:.1f} {unit}"
    ratio = g(N / A)
    steps = [f"Divide by {A}: {form.format(**f).replace(str(A), '', 1)} = {ratio}.", (f"Take natural logarithms: {f['k']}t = ln({ratio})." if kind.startswith("e") else f"Take logarithms: t · ln({f['b']}) = ln({ratio})."), f"t ≈ {t:.1f} {unit}."]
    base = math.e ** float(f["k"]) if kind.startswith("e") else float(f["b"])
    w = [(N / A / (abs(float(f["k"])) if kind.startswith("e") else base), "divided instead of taking a logarithm"), (abs(math.log(N / A)), "did not divide by the growth constant" if kind.startswith("e") else "did not divide by the logarithm of the base"),
         (abs(math.log(N)) / abs(math.log(base)), f"took the logarithm before dividing by {A}"), (abs(math.log10(N / A)) / abs(math.log(base)), "mixed common and natural logarithms")]
    wr = [(f"t ≈ {v:.1f} {unit}", why) for v, why in w if abs(v - t) > 0.15]
    return I(prompt, ans, steps, wr, dict(k="solve", eq=eq, var="t", dp=1, unit=unit, show=[f"Solve {eq} "]), "exp_application")


# ---------------------------------------------------------------- calculus: long division, completing the square
def divide(cs, d):
    """Divide the polynomial with coefficient list cs (highest power first) by (x + d): quotient list, remainder."""
    out = [cs[0]]
    for c in cs[1:]:
        out.append(c - d * out[-1])
    return out[:-1], out[-1]


def plist(cs):
    n = len(cs) - 1
    return poly({n - i: c for i, c in enumerate(cs)})


def ratfun(r, L):
    deg = 1 if L == 0 else 2 if L == 1 else r.choice([2, 3])
    d = r.choice([1, 2, 3, 4] if L < 2 else [1, 2, 3, 5])
    q = [r.choice([1, 2, 3] if i == 0 else [-4, -3, -2, -1, 1, 2, 3, 4, 5]) for i in range(deg)]
    if deg > 1 and L < 2:
        q[0] = 1
    rem = r.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
    cs = [q[0]] + [q[i] + d * q[i - 1] for i in range(1, deg)] + [rem + d * q[-1]]
    need(all(c != 0 for c in cs))
    qq, rr = divide(cs, d)
    assert qq == q and rr == rem
    return cs, d, q, rem, f"({plist(cs)})/(x + {d})"


def rterm(rem, den, first=False):
    return f"{rem}/({den})" if rem > 0 else f"-{-rem}/({den})"


def lnterm(c, inner):
    return coef(c, f"ln|{inner}|")


def integ(q):
    n = len(q)
    return {n - i: F(c, n - i) for i, c in enumerate(q)}


def c_div_rewrite(r, L):
    levels(L, 0, 1)
    cs, d, q, rem, e = ratfun(r, L)
    ans = join([plist(q), rterm(rem, f"x + {d}")])
    q2, r2 = divide(cs, -d)
    wr = [(join([plist(q), rterm(-rem, f"x + {d}")]), "made a sign error on the remainder"), (plist(q), "left out the remainder"), (join([plist(q2), rterm(r2, f"x + {d}")]) if r2 else plist(q2), f"divided by x - {d} instead of x + {d}")]
    if len(q) > 1:
        wr.append((join([plist(q), str(rem)]), "wrote the remainder without dividing it by the divisor"))
    steps = [f"Divide {plist(cs)} by x + {d}: the quotient is {plist(q)} and the remainder is {rem}.", f"{e} = {ans}.", f"Check: ({plist(q)})(x + {d}) {'+ ' + str(rem) if rem > 0 else '- ' + str(-rem)} = {plist(cs)}."]
    return I(f"Use long division to rewrite {e} as a polynomial plus a proper fraction.", ans, steps, wr, dict(k="ident", var="x", e=e, show=[e]), "division_rewrite")


def c_div_int(r, L):
    cs, d, q, rem, e = ratfun(r, L)
    P = integ(q)
    ans = join([poly(P), lnterm(rem, f"x + {d}")]) + " + C"
    wr = [(poly(P) + " + C", "left out the integral of the remainder term"), (join([poly(P), lnterm(-rem, f"x + {d}")]) + " + C", "made a sign error on the logarithm term"), (join([plist(q), lnterm(rem, f"x + {d}")]) + " + C", "did not integrate the polynomial part"),
          (join([poly(P), rterm(rem, f"x + {d}")]) + " + C", "did not integrate the remainder term")]
    steps = [f"Divide first: {e} = {join([plist(q), rterm(rem, f'x + {d}')])}.", f"Integrate the polynomial part: {poly(P)}.", f"∫ {rterm(rem, f'x + {d}')} dx = {lnterm(rem, f'x + {d}')}.", f"∫ {e} dx = {ans}."]
    return I(f"Find ∫ {e} dx.", ans, steps, wr, dict(k="anti", g=e, show=[f"∫ {e} dx"]), "division_integral")


def c_div_def(r, L):
    levels(L, 1, 2)
    cs, d, q, rem, e = ratfun(r, L)
    lo = r.choice([0, 1])
    hi = lo + r.choice([1, 2, 3, 4])
    P = integ(q)
    pv = sum(c * (F(hi) ** p - F(lo) ** p) for p, c in P.items())
    ratio = F(hi + d, lo + d)
    need(pv != 0)
    lt = f"ln({num(ratio)})"
    ans = join([num(pv), coef(rem, lt)])
    wr = [(num(pv), "left out the logarithm term"), (join([num(pv), coef(-rem, lt)]), "made a sign error on the logarithm term"), (join([num(pv), coef(rem, f"ln({hi + d})")]), "did not subtract the value at the lower limit") if lo + d != 1 else (join([num(pv), coef(rem, f"ln({hi})")]), "used ln|x| instead of ln|x + d|"),
          (join([num(sum(c * (F(hi) ** (p - 1) - F(lo) ** (p - 1)) for p, c in {len(q) - i: c for i, c in enumerate(q)}.items())), coef(rem, lt)]), "evaluated the quotient instead of its antiderivative")]
    Ft = join([poly(P), lnterm(rem, f"x + {d}")])
    steps = [f"Divide first: {e} = {join([plist(q), rterm(rem, f'x + {d}')])}.", f"An antiderivative is {Ft}.", f"Evaluate from {lo} to {hi}: the polynomial part gives {num(pv)} and the logarithm part gives {coef(rem, f'(ln({hi + d}) - ln({lo + d}))')}.", f"The value is {ans}."]
    return I(f"Evaluate ∫ from {lo} to {hi} {e} dx.", ans, steps, wr, dict(k="defint", g=e, lo=lo, hi=hi, show=[f"∫ from {lo} to {hi} {e} dx"]), "division_definite")


def square(r, L):
    h = r.choice([-4, -3, -2, -1, 1, 2, 3, 4] if L else [-3, -2, -1, 1, 2, 3])
    a = r.choice([1, 2, 3] if L == 0 else [2, 3, 4, 5] if L == 1 else [2, 3, 4, 5, 6, 7])
    return h, a, poly({2: 1, 1: 2 * h, 0: h * h + a * a})


def c_sq_rewrite(r, L):
    levels(L, 0, 1)
    h, a, q = square(r, L)
    ans = f"({lin(1, h)})² + {a * a}"
    c = h * h + a * a
    wr = [(f"({lin(1, h)})² + {c}", f"did not subtract {h * h} after adding it to complete the square"), (f"({lin(1, 2 * h)})² + {a * a}", "did not halve the coefficient of x"), (f"({lin(1, h)})² - {a * a}", "made a sign error on the constant"), (f"({lin(1, -h)})² + {a * a}", "made a sign error inside the square")]
    steps = [f"Half of {2 * h} is {h}, and ({h})² = {h * h}.", f"{q} = ({poly({2: 1, 1: 2 * h, 0: h * h})}) + {c} - {h * h}.", f"= {ans}."]
    return I(f"Complete the square: {q}.", ans, steps, wr, dict(k="ident", var="x", e=q, show=[q]), "square_rewrite")


def atan_ans(k, h, a):
    inner = lin(1, h) if a == 1 else f"({lin(1, h)})/{a}"
    return coef(F(k, a), f"tan⁻¹({inner})") + " + C"


def c_atan(r, L):
    h, a, q = square(r, L)
    k = 1 if L == 0 else r.choice([1, 1, 2, 3, 4, 6])
    e = f"{k}/({q})"
    ans = atan_ans(k, h, a)
    wr = [(coef(k, f"tan⁻¹({lin(1, h) if a == 1 else '(' + lin(1, h) + ')/' + str(a)})") + " + C" if a != 1 else coef(k, f"tan⁻¹(x)") + " + C", f"left out the factor 1/{a}" if a != 1 else "did not shift the argument"),
          (coef(k, f"ln|{q}|") + " + C", "treated the integrand as u′/u, but the numerator is not the derivative of the denominator"), (coef(F(k, a), f"tan⁻¹({lin(1, h)})") + " + C" if a != 1 else coef(k, f"tan⁻¹({lin(1, -h)})") + " + C", f"did not divide the argument by {a}" if a != 1 else "made a sign error inside the argument"),
          (coef(F(k, a * a), f"tan⁻¹({'(' + lin(1, h) + ')/' + str(a * a)})") + " + C", f"used a = {a * a} instead of a = {a}")]
    steps = [f"Complete the square: {q} = ({lin(1, h)})² + {a * a}.", f"Use ∫ 1/(u² + a²) du = (1/a)tan⁻¹(u/a) + C with u = {lin(1, h)} and a = {a}.", f"∫ {e} dx = {ans}."]
    return I(f"Find ∫ {e} dx.", ans, steps, wr, dict(k="anti", g=e, show=[f"∫ {e} dx"]), "square_arctan")


def pifrac(v):
    v = F(v)
    n, d = v.numerator, v.denominator
    top = "π" if n == 1 else f"{n}π"
    return top if d == 1 else f"{top}/{d}"


def c_atan_def(r, L):
    levels(L, 1, 2)
    h, a, q = square(r, L)
    k = r.choice([1, 2, 3, 4, 6])
    span = r.choice(["01", "m11", "m10"])
    lo, hi, mult = {"01": (-h, -h + a, F(1, 4)), "m11": (-h - a, -h + a, F(1, 2)), "m10": (-h - a, -h, F(1, 4))}[span]
    e = f"{k}/({q})"
    v = F(k, a) * mult
    ans = pifrac(v)
    wr = [(pifrac(F(k) * mult), f"left out the factor 1/{a}") if a != 1 else (pifrac(v * 2), "used tan⁻¹(1) = π/2"), (pifrac(v * 2), "used π/2 for tan⁻¹(1); tan⁻¹(1) = π/4"), (num(F(k, a) * (1 if span != "m11" else 2)), "evaluated tan⁻¹ as 1 at u = 1 instead of π/4"), (pifrac(v / 2), "halved the result"), (pifrac(F(k, a * a) * mult), f"divided by a² = {a * a} instead of a = {a}")]
    u = lambda x: num(F(x + h, a))
    steps = [f"Complete the square: {q} = ({lin(1, h)})² + {a * a}.", f"An antiderivative is {atan_ans(k, h, a).replace(' + C', '')}.", f"At x = {hi}, u = {u(hi)}; at x = {lo}, u = {u(lo)}.", f"{coef(F(k, a), '(tan⁻¹(' + u(hi) + ') - tan⁻¹(' + u(lo) + '))')} = {ans}."]
    return I(f"Evaluate ∫ from {lo} to {hi} {e} dx.", ans, steps, wr, dict(k="defint", g=e, lo=lo, hi=hi, show=[f"∫ from {lo} to {hi} {e} dx"]), "square_arctan_definite")


def c_asin(r, L):
    levels(L, 2)
    h = r.choice([-2, -1, 1, 2])
    a = r.choice([3, 4, 5, 6])
    k = r.choice([1, 1, 2, 3, 5])
    # a² − (x + h)² = −x² − 2hx + (a² − h²)
    q = poly({2: -1, 1: -2 * h, 0: a * a - h * h})
    e = f"{k}/√({q})"
    ans = coef(k, f"sin⁻¹(({lin(1, h)})/{a})") + " + C"
    wr = [(coef(F(k, a), f"sin⁻¹(({lin(1, h)})/{a})") + " + C", f"included a factor 1/{a}, which belongs to the tan⁻¹ formula"), (coef(F(k, a), f"tan⁻¹(({lin(1, h)})/{a})") + " + C", "used the tan⁻¹ formula; the square root calls for sin⁻¹"),
          (coef(k, f"sin⁻¹({lin(1, h)})") + " + C", f"did not divide the argument by {a}"), (coef(k, f"sin⁻¹(({lin(1, -h)})/{a})") + " + C", "made a sign error when completing the square")]
    steps = [f"Complete the square: {q} = {a * a} - ({lin(1, h)})².", f"Use ∫ 1/√(a² - u²) du = sin⁻¹(u/a) + C with u = {lin(1, h)} and a = {a}.", f"∫ {e} dx = {ans}."]
    return I(f"Find ∫ {e} dx.", ans, steps, wr, dict(k="anti", g=e, show=[f"∫ {e} dx"]), "square_arcsin")


SKILLS = {
    ("algebra2", "polynomial-functions", "Binomial Theorem and Pascal's Triangle"): dict(fns=[b_expand, b_coef, b_term, b_pascal, b_choose, b_sum], stds=["A-APR.C.5"], prefix="a2-pf"),
    ("precalculus", "functions", "Solving Exponential and Logarithmic Equations"): dict(fns=[x_same, x_log, x_e, x_logeq, x_logsum, x_quad, x_app], stds=["F-LE.A.4", "F-BF.B.5"], prefix="pc-fun"),
    ("calculus", "fundamental-theorem-calculus", "Integration Using Long Division and Completing the Square"): dict(fns=[c_div_rewrite, c_div_int, c_div_def, c_sq_rewrite, c_atan, c_atan_def, c_asin], stds=["AP FUN-6.D"], prefix="cal-ftc"),
}
