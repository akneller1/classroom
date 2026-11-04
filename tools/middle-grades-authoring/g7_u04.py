"""Grade 7 Unit 4 — Factors, Fractions, and Exponents (factors-fractions-exponents)."""
from glib import *

UNIT_ID = "factors-fractions-exponents"
ABBR = "ffe"


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def pf_text(n):
    out, d = [], 2
    while n > 1:
        e = 0
        while n % d == 0:
            n //= d
            e += 1
        if e:
            out.append(f"{d}{sup(e) if e > 1 else ''}")
        d += 1
    return " · ".join(out)


# ============================================================== S1 Divisibility and Factors
@fam("012")
def s1_divisible(r, L):
    d = pick(r, [2, 3, 5, 10] if L == 0 else [3, 4, 6, 9] if L == 1 else [4, 6, 8, 9, 12])
    n = r.randint(100, 999) if L < 2 else r.randint(1000, 99999)
    if r.random() < 0.55:
        n = n - n % d
    ok = n % d == 0
    rule = {2: "the last digit is even", 3: "the sum of the digits is divisible by 3", 5: "the last digit is 0 or 5", 10: "the last digit is 0",
            4: "the last two digits form a number divisible by 4", 6: "it is divisible by both 2 and 3", 9: "the sum of the digits is divisible by 9",
            8: "the last three digits form a number divisible by 8", 12: "it is divisible by both 3 and 4"}[d]
    return Q(f"Is {n:,} divisible by {d}?", "Yes" if ok else "No", [f"Divisibility rule: a number is divisible by {d} if {rule}.", f"Digit sum of {n:,} is {sum(map(int, str(n)))}." if d in (3, 9, 6, 12) else f"Check the rule for {n:,}.",
                                                                    f"So {n:,} {'is' if ok else 'is not'} divisible by {d}."], ["No" if ok else "Yes"], PY("divides", n=n, d=d), mode="sa",
             why=["Applied the wrong divisibility rule"])


@fam("012")
def s1_factor_list(r, L):
    n = pick(r, [12, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48] if L < 2 else [56, 60, 64, 72, 80, 84, 90, 96, 100])
    fs = factors(n)
    if L == 0:
        return Q(f"List all the factors of {n}.", ", ".join(map(str, fs)), ["Find factor pairs: " + ", ".join(f"{a} × {n // a}" for a in fs if a * a <= n) + ".", f"Factors: {', '.join(map(str, fs))}."],
                 [", ".join(map(str, fs[1:-1])), ", ".join(map(str, fs + [2 * n])), ", ".join(map(str, [f for f in fs if f % 2 == 0]))], PY("set_eq", items=[str(f) for f in fs]),
                 why=["Left out 1 and the number itself", "Included a multiple, not a factor", "Listed only the even factors"])
    return Q(f"How many factors does {n} have?", str(len(fs)), ["Find all factor pairs: " + ", ".join(f"{a} × {n // a}" for a in fs if a * a <= n) + ".", f"Count: {len(fs)} factors."],
             [str(len(fs) - 2), str(len([a for a in fs if a * a <= n])), str(len(fs) + 1)], PY("num_factors", n=n), why=["Did not count 1 and the number itself", "Counted factor pairs instead of factors", ""])


@fam("012", mode="mc")
def s1_prime(r, L):
    pool = list(range(2, 60 if L == 0 else 120))
    pr = [p for p in pool if is_prime(p)]
    co = [c for c in pool if not is_prime(c) and c > 1 and (L == 0 or c % 2 and c % 5)]
    ask = pick(r, ["prime", "composite"])
    if ask == "prime":
        good = pick(r, pr)
        bad = pick(r, co, 3)
    else:
        good = pick(r, co)
        bad = pick(r, pr, 3)
    opts = [(str(good), True)] + [(str(b), False) for b in bad]
    r.shuffle(opts)
    return Q(f"Which number is {ask}?", str(good), ["A prime number has exactly two factors: 1 and itself.", f"{good} {'has only factors 1 and ' + str(good) if ask == 'prime' else '= ' + pf_text(good)}."],
             options=opts, chk=PY("prime_q", want=ask), mode="mc")


@fam("2")
def s1_digit(r, L):
    a, b = r.randint(1, 9), r.randint(0, 9)
    d = pick(r, [3, 9])
    good = [k for k in range(10) if (a + b + k) % d == 0]
    need(len(good) == 1)
    return Q(f"What digit can replace ■ so that {a}{b}■ is divisible by {d}? (Only one digit works.)", str(good[0]),
             [f"Digit sum: {a} + {b} + ■ must be divisible by {d}.", f"{a + b} + {good[0]} = {a + b + good[0]}.", f"The digit is {good[0]}."],
             [str((good[0] + 3) % 10), str((good[0] + 1) % 10), str(a + b)], PY("missing_digit", a=a, b=b, d=d), why=["Made an addition error", "", ""], tags=["reasoning"])


# ============================================================== S2 Exponents
@fam("012")
def s2_eval(r, L):
    if L == 0:
        b, e = r.randint(2, 10), r.randint(2, 4)
        need(b ** e < 10000)
        t = f"{b}{sup(e)}"
        wr = [str(b * e), str(e ** b) if e ** b != b ** e else str(b ** e + 1), str(b ** (e - 1))]
        why = ["Multiplied the base by the exponent", "Switched the base and the exponent", "Multiplied one too few times"]
    elif L == 1:
        b, e = nz(r, -6, 6), r.randint(2, 4)
        need(b < 0)
        t = pick(r, [f"({b}){sup(e)}", f"-{abs(b)}{sup(e)}"])
        v = M_ev(t)
        wr = [str(-v), str(b * e), str(abs(b) ** e if v != abs(b) ** e else -abs(b) ** e)]
        why = ["Applied the negative sign incorrectly", "Multiplied the base by the exponent", ""]
    else:
        a, b, e = r.randint(2, 5), r.randint(2, 4), r.randint(2, 3)
        t = pick(r, [f"{a}{sup(e)} + {b}{sup(2)}", f"(-{a}){sup(e)} - {b}{sup(2)}", f"({a} × {b}){sup(2)} - {a}{sup(2)}", f"(1/{a}){sup(e)}"])
        v = M_ev(t)
        wr = [N(M_ev(t.replace(sup(e), f"*{e}").replace(sup(2), "*2"))), N(-v), N(v + 1)]
        why = ["Multiplied by the exponent instead of using repeated multiplication", "Made a sign error", ""]
    v = M_ev(t)
    return Q(f"Evaluate: {t}", N(v), ["An exponent tells how many times to use the base as a factor.", f"{t} = {N(v)}."], wr, V(t), why=why)


def M_ev(e):
    import mathtext
    return mathtext.ev(e)


@fam("012")
def s2_write(r, L):
    b = r.randint(2, 9) if L < 2 else pick(r, ["x", "y", "a"])
    e = r.randint(3, 6)
    prod = " · ".join([str(b)] * e)
    if L == 1:
        c = r.randint(2, 9)
        need(c != b)
        f2 = r.randint(2, 3)
        prod = " · ".join([str(b)] * e + [str(c)] * f2)
        ans = f"{b}{sup(e)} · {c}{sup(f2)}"
        return Q(f"Write using exponents: {prod}", ans, ["Count how many times each base is a factor.", f"{b} appears {e} times and {c} appears {f2} times.", f"{ans}."],
                 [f"{b * c}{sup(e + f2)}", f"{e}{sup(b)} · {f2}{sup(c)}", f"{b}{sup(e + f2)}"], V(prod.replace("·", "*")), why=["Multiplied the bases and added the exponents", "Switched bases and exponents", "Used one base"])
    ans = f"{b}{sup(e)}"
    return Q(f"Write using an exponent: {prod}", ans, [f"The base {b} is a factor {e} times.", f"{prod} = {ans}."], [f"{e}{b}" if L == 2 else f"{e}{sup(b)}", f"{b}{sup(e - 1)}", f"{b}{sup(e + 1)}"],
             EQV(prod.replace("·", "*"), [b]) if L == 2 else V(prod.replace("·", "*")), why=["Wrote multiplication instead of an exponent", "Miscounted the factors", "Miscounted the factors"])


@fam("12")
def s2_context(r, L):
    k = r.randint(3, 7)
    b = pick(r, [2, 3])
    return Q(f"A bacteria colony {'doubles' if b == 2 else 'triples'} every hour. Starting with 1 cell, how many cells are there after {k} hours?", f"{b ** k:,}",
             [f"After each hour multiply by {b}.", f"After {k} hours: {b}{sup(k)}.", f"{b}{sup(k)} = {b ** k:,}."], [str(b * k), f"{b ** (k + 1):,}", f"{b ** (k - 1):,}"], V(f"{b}^{k}"),
             why=["Multiplied by the number of hours", "Counted one extra hour", "Counted one hour too few"], tags=["modeling"])


# ============================================================== S3 Prime factorization and GCF
@fam("012")
def s3_pf(r, L):
    ps = [2, 3, 5, 7] if L < 2 else [2, 3, 5, 7, 11, 13]
    k = r.randint(2, 3) if L == 0 else r.randint(3, 5)
    n = 1
    for _ in range(k):
        n *= pick(r, ps)
    need(12 <= n <= (100 if L == 0 else 1000 if L == 1 else 5000) and not is_prime(n))
    ans = pf_text(n)
    f1 = [d for d in factors(n) if 1 < d < n]
    a = pick(r, f1)
    return Q(f"Write the prime factorization of {n:,} using exponents.", ans, ["Divide by primes repeatedly (a factor tree).", f"{n} = {a} × {n // a}, then factor each until all factors are prime.", f"{n} = {ans}."],
             [f"{a} · {n // a}", pf_text(n).replace(" · ", " · ", 1) + " · 1", pf_text(n * 2)], PY("prime_fact", n=n), why=["Stopped before all factors were prime", "", "Made a division error"])


def gcd(a, b):
    return math.gcd(a, b)


@fam("012")
def s3_gcf(r, L):
    g = r.randint(2, 12) if L < 2 else r.randint(4, 18)
    a, b = r.randint(2, 9), r.randint(2, 9)
    need(gcd(a, b) == 1 and a != b)
    if L == 2:
        c = r.randint(2, 9)
        need(gcd(gcd(a, b), c) == 1 and c not in (a, b))
        x, y, z = g * a, g * b, g * c
        return Q(f"Find the GCF of {x}, {y}, and {z}.", str(g), [f"{x} = {pf_text(x)}, {y} = {pf_text(y)}, {z} = {pf_text(z)}.", "Multiply the prime factors common to all three.", f"GCF = {g}."],
                 [str(g * a * b * c), str(min(x, y, z)), str(gcd(x, y)) if gcd(x, y) != g else str(g * 2)], V(str(math.gcd(math.gcd(x, y), z))) if False else PY("gcf", nums=[x, y, z]),
                 why=["Found a common multiple instead", "Gave the least number", "Found the GCF of only two numbers"])
    x, y = g * a, g * b
    lcm = x * y // g
    return Q(f"Find the greatest common factor (GCF) of {x} and {y}.", str(g), [f"Factors of {x}: {', '.join(map(str, factors(x)))}.", f"Factors of {y}: {', '.join(map(str, factors(y)))}.", f"The greatest common factor is {g}."],
             [str(lcm), str(min(x, y)), str([d for d in factors(g) if d < g][-1]) if g > 1 else "1"], PY("gcf", nums=[x, y]), why=["Found the least common multiple", "Gave the smaller number", "Gave a common factor that is not the greatest"])


@fam("12")
def s3_gcf_word(r, L):
    g = r.randint(3, 12)
    a, b = r.randint(2, 8), r.randint(2, 8)
    need(gcd(a, b) == 1 and a != b)
    x, y = g * a, g * b
    return Q(f"A teacher has {x} pencils and {y} erasers. She makes identical kits with no supplies left over. What is the greatest number of kits she can make?", str(g),
             ["The number of kits must divide both amounts.", f"Find the GCF of {x} and {y}.", f"GCF = {g}, so {g} kits (each with {a} pencils and {b} erasers)."],
             [str(x * y // g), str(x + y), str(a + b)], PY("gcf", nums=[x, y]), why=["Found the least common multiple", "Added the amounts", "Gave the number of items in one kit"], tags=["modeling"])


# ============================================================== S4 Simplifying fractions
@fam("012")
def s4_simplify(r, L):
    g = r.randint(2, 12)
    a, b = r.randint(1, 12), r.randint(2, 15)
    need(gcd(a, b) == 1 and a < b)
    n, d = a * g, b * g
    part = [k for k in factors(g) if 1 < k < g]
    wr = [f"{n // part[0]}/{d // part[0]}" if part else f"{a + 1}/{b}", f"{n - g}/{d - g}" if n > g else f"{a}/{b + 1}", f"{b}/{a}" if a > 1 else f"{a}/{b * 2}"]
    return Q(f"Write {n}/{d} in simplest form.", f"{a}/{b}", [f"GCF of {n} and {d} is {g}.", f"Divide numerator and denominator by {g}.", f"{n}/{d} = {a}/{b}."], wr,
             PY("frac_simplest", expr=f"{n}/{d}"), why=["Divided by a common factor that is not the greatest", "Subtracted the same number from top and bottom", "Flipped the fraction"])


@fam("012")
def s4_equiv(r, L):
    a, b = r.randint(1, 9), r.randint(2, 12)
    need(gcd(a, b) == 1 and a < b)
    k = r.randint(2, 9)
    if r.random() < 0.5:
        st = f"{a}/{b} = ?/{b * k}"
        ans = a * k
        wr = [a + b * k - b, b * k, a * k + 1]
    else:
        st = f"{a}/{b} = {a * k}/?"
        ans = b * k
        wr = [b + a * k - a, a * k * a, b * k + k]
    return Q(f"Find the value of n that makes the fractions equivalent: {st.replace('?', 'n')}", str(ans), [f"The denominator (or numerator) was multiplied by {k}.", f"Multiply the other part by {k} too.", f"Missing number: {ans}."],
             [str(w) for w in wr], PY("missing_frac", st=st), why=["Added instead of multiplying", "", ""])


@fam("2")
def s4_algebraic(r, L):
    g = r.randint(2, 6)
    a, b = r.randint(1, 7), r.randint(2, 9)
    need(gcd(a, b) == 1)
    e1, e2 = r.randint(2, 5), r.randint(1, 3)
    need(e1 > e2)
    num, den = f"{a * g}x{sup(e1)}", f"{b * g}x{sup(e2) if e2 > 1 else ''}"
    de = e1 - e2
    ans = f"{a if a > 1 else ''}x{sup(de) if de > 1 else ''}/{b}"
    return Q(f"Simplify. Assume x ≠ 0. ({num})/({den})", ans, [f"Divide the coefficients by their GCF {g}: {a * g}/{b * g} = {a}/{b}.", f"Cancel common factors of x: x{sup(e1)} ÷ x{sup(e2) if e2 > 1 else ''} = x{sup(de) if de > 1 else ''}.", f"Result: {ans}."],
             [f"{a if a > 1 else ''}x{sup(e1 // e2) if e1 // e2 > 1 else ''}/{b}", f"{a * g}x{sup(de) if de > 1 else ''}/{b}", f"{a if a > 1 else ''}x{sup(e1 + e2)}/{b}"],
             EQV(f"({num})/({den})"), why=["Divided the exponents instead of subtracting", "Simplified only the denominator coefficient", "Added the exponents"])


@fam("12", mode="mc")
def s4_which_equiv(r, L):
    a, b = r.randint(1, 7), r.randint(2, 9)
    need(gcd(a, b) == 1 and a < b)
    k1, k2 = r.sample(range(2, 8), 2)
    good = f"{a * k1}/{b * k1}"
    bad = [f"{a + k2}/{b + k2}", f"{a * k2}/{b * k2 + 1}", f"{b * k1}/{a * k1}" if a > 1 else f"{a * k1}/{b * k1 + k1}"]
    opts = [(good, True)] + [(x, False) for x in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Which fraction is equivalent to {a}/{b}?", good, [f"Multiply numerator and denominator by the same number: {a} × {k1} and {b} × {k1}.", f"{good} = {a}/{b}."], options=opts,
             chk=V(f"{a}/{b}"), mode="mc", tags=["misconception"])


# ============================================================== S5 Rational Numbers
@fam("012")
def s5_to_fraction(r, L):
    if L == 0:
        x = F(r.randint(1, 99), 100)
    elif L == 1:
        x = -F(r.randint(1, 999), 1000) * pick(r, [1, 1, 5])
    else:
        x = F(r.randint(1, 9), 1) + F(r.randint(1, 99), 100)
        x = -x if r.random() < 0.5 else x
    need(x.denominator > 1)
    ans = N(x)
    t = D(x)
    den = 10 ** len(t.split(".")[1])
    raw = f"{int(abs(x) * den) * (1 if x > 0 else -1)}/{den}"
    return Q(f"Write {t} as a fraction in simplest form.", ans, [f"{t} = {raw}.", f"Simplify by dividing by the GCF.", f"{t} = {ans}."],
             [raw if raw != ans else f"{x.numerator}/{x.denominator * 10}", N(-x), f"{x.denominator}/{x.numerator}" if abs(x.numerator) > 1 else f"1/{x.denominator * 10}"],
             PY("frac_simplest", expr=f"{x.numerator}/{x.denominator}", mixed=False), why=["Did not simplify", "Dropped the negative sign" if x < 0 else "Made a sign error", "Flipped the fraction"])


@fam("012", mode="mc")
def s5_classify(r, L):
    pool = [(str(r.randint(2, 40)), "natural number"), ("0", "whole number"), (str(-r.randint(2, 40)), "integer"),
            (f"{r.randint(1, 9)}/{r.randint(11, 19)}", "rational number"), (f"-{r.randint(1, 9)}.{r.randint(1, 9)}", "rational number"), (f"√{pick(r, [2, 3, 5, 7, 10, 11])}", "irrational number")]
    num, kind = pick(r, pool if L else pool[:4])
    labels = ["natural number", "whole number", "integer", "rational number", "irrational number"]
    opts = [(l, l == kind) for l in labels if l != "irrational number" or L]
    if len(opts) > 4:
        bad = [o for o in opts if not o[1]]
        r.shuffle(bad)
        opts = [o for o in opts if o[1]] + bad[:3]
    r.shuffle(opts)
    return Q(f"What is the most specific set that {num} belongs to?", kind, ["Natural ⊂ whole ⊂ integers ⊂ rational numbers; irrational numbers are separate.", f"{num} is best described as a {kind}."],
             options=opts, chk=PY("classify", num=num), mode="mc")


@fam("012")
def s5_order(r, L):
    k = 4
    vals = set()
    while len(vals) < k:
        vals.add(F(nz(r, -9, 9), pick(r, [2, 4, 5, 8, 10])) if L else F(r.randint(1, 19), pick(r, [2, 4, 5, 10])))
    vals = sorted(vals)
    txt = [N(v) if r.random() < 0.5 or not is_term(v) else D(v) for v in vals]
    shown = txt[:]
    r.shuffle(shown)
    need(shown != txt)
    by_abs = [t for _, t in sorted(zip(vals, txt), key=lambda p: abs(p[0]))]
    return Q(f"Order from least to greatest: {', '.join(shown)}", ", ".join(txt), ["Write each number as a decimal to compare.", ", ".join(f"{t} = {D(v)}" for t, v in zip(txt, vals)) + ".", f"Least to greatest: {', '.join(txt)}."],
             [", ".join(txt[::-1]), ", ".join(by_abs) if by_abs != txt else ", ".join(txt[1:] + txt[:1]), ", ".join(sorted(txt))], PY("order", items=txt),
             why=["Ordered from greatest to least", "Ordered by distance from zero", "Ordered the digits as text"])


@fam("2")
def s5_between(r, L):
    a = F(r.randint(1, 8), 9)
    b = a + F(1, 9)
    m = (a + b) / 2
    return Q(f"Find a rational number exactly halfway between {N(a)} and {N(b)}.", N(m), [f"Average the two numbers: ({N(a)} + {N(b)}) ÷ 2.", f"= {N(a + b)} ÷ 2 = {N(m)}."],
             [N(a + b), N(F(a.numerator + b.numerator, a.denominator + b.denominator)), N(m + F(1, 18))], V(f"({N(a)} + {N(b)})/2"),
             why=["Forgot to divide by 2", "Added numerators and denominators", ""], tags=["reasoning"])


# ============================================================== S6 Irrational Numbers
@fam("012", mode="mc")
def s6_which(r, L):
    irr = [f"√{n}" for n in (2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15)] + ["π"]
    rat = [f"√{n * n}" for n in range(2, 13)] + [f"{r.randint(1, 9)}/{r.randint(2, 9)}", f"0.{r.randint(1, 9)}{r.randint(1, 9)}", str(-r.randint(2, 30))]
    ask = pick(r, ["irrational", "rational"]) if L else "irrational"
    good = pick(r, irr if ask == "irrational" else rat)
    bad = pick(r, rat if ask == "irrational" else irr, 3)
    opts = [(good, True)] + [(b, False) for b in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Which number is {ask}?", good, ["A rational number can be written as a ratio of two integers; its decimal ends or repeats.", "Square roots of numbers that are not perfect squares are irrational.", f"{good} is {ask}."],
             options=opts, chk=PY("is_" + ask), mode="mc")


@fam("012")
def s6_between(r, L):
    n = r.randint(3, 140 if L else 80)
    s = math.isqrt(n)
    need(s * s != n)
    return Q(f"Between which two consecutive whole numbers is √{n}?", f"{s} and {s + 1}", [f"{s}² = {s * s} and {s + 1}² = {(s + 1) ** 2}.", f"{s * s} < {n} < {(s + 1) ** 2}.", f"So √{n} is between {s} and {s + 1}."],
             [f"{s - 1} and {s}", f"{s + 1} and {s + 2}", f"{n // 2} and {n // 2 + 1}"], PY("between_ints", num=f"√{n}"), why=["Chose a pair one too low", "Chose a pair one too high", "Divided by 2 instead of taking a square root"])


@fam("12")
def s6_estimate(r, L):
    n = r.randint(3, 99)
    s = math.isqrt(n)
    need(s * s != n)
    v = math.sqrt(n)
    ans = Rd(v, 1)
    return Q(f"Estimate √{n} to the nearest tenth.", ans, [f"√{n} is between {s} and {s + 1}.", f"Test tenths: {Rd(v, 1)}² ≈ {Rd(float(ans) ** 2, 2)}.", f"√{n} ≈ {ans}."],
             [Rd(n / 2, 1), Rd(v + 0.3, 1), f"{s}.{n - s * s}" if n - s * s < 10 else Rd(v - 0.3, 1)], PY("sqrt_tenth", n=n), why=["Divided by 2 instead of taking the square root", "", "Used the remainder as the decimal"])


@fam("2")
def s6_order(r, L):
    ns = r.sample([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20], 2)
    items = [f"√{ns[0]}", f"√{ns[1]}", pick(r, ["π", "3.1"]), N(F(r.randint(5, 30), 4))]
    vals = {"π": math.pi}
    import mathtext
    def val(t):
        return math.pi if t == "π" else float(mathtext.ev(t))
    need(len({round(val(t), 6) for t in items}) == 4)
    srt = sorted(items, key=val)
    shown = items[:]
    r.shuffle(shown)
    need(shown != srt)
    return Q(f"Order from least to greatest: {', '.join(shown)}", ", ".join(srt), ["Approximate each number as a decimal.", ", ".join(f"{t} ≈ {Rd(val(t), 2)}" for t in srt) + ".", f"Order: {', '.join(srt)}."],
             [", ".join(srt[::-1]), ", ".join(sorted(items)), ", ".join(srt[1:] + srt[:1])], PY("order", items=items), why=["Ordered from greatest to least", "Ordered as text", ""])


# ============================================================== S7 / S8 Exponent rules
@fam("012")
def s7_product(r, L):
    if L == 0:
        b, m, n = r.randint(2, 9), r.randint(2, 6), r.randint(2, 6)
        t = f"{b}{sup(m)} · {b}{sup(n)}"
        ans = f"{b}{sup(m + n)}"
        wr = [f"{b}{sup(m * n)}", f"{b * b}{sup(m + n)}", f"{b}{sup(abs(m - n)) if m != n else sup(1)}"]
        return Q(f"Simplify. Write your answer as a power: {t}", ans, ["When multiplying powers with the same base, add the exponents.", f"{m} + {n} = {m + n}.", f"{t} = {ans}."], wr,
                 PY("power_form", base=str(b), expr=t.replace("·", "*")), why=["Multiplied the exponents", "Multiplied the bases", "Subtracted the exponents"])
    v = pick(r, ["x", "y", "a", "m"])
    c1, c2 = r.randint(2, 9), r.randint(2, 9)
    m, n = r.randint(1, 7), r.randint(2, 7)
    if L == 2:
        w = pick(r, ["y", "b"])
        need(w != v)
        p, q = r.randint(1, 5), r.randint(1, 5)
        t = f"({c1}{v}{sup(m) if m > 1 else ''}{w}{sup(p) if p > 1 else ''})({c2}{v}{sup(n)}{w}{sup(q) if q > 1 else ''})"
        ans = f"{c1 * c2}{v}{sup(m + n)}{w}{sup(p + q)}"
        wr = [f"{c1 + c2}{v}{sup(m + n)}{w}{sup(p + q)}", f"{c1 * c2}{v}{sup(m * n)}{w}{sup(p * q) if p * q > 1 else ''}", f"{c1 * c2}{v}{sup(m + n)}{w}{sup(p * q) if p * q > 1 else ''}"]
        return Q(f"Simplify: {t}", ans, ["Multiply the coefficients.", "Add the exponents of each base.", f"{c1} · {c2} = {c1 * c2}; {v}: {m} + {n}; {w}: {p} + {q}.", f"{ans}."], wr, EQV(t, [v, w]),
                 why=["Added the coefficients", "Multiplied the exponents", "Multiplied some exponents"])
    t = f"{c1}{v}{sup(m) if m > 1 else ''} · {c2}{v}{sup(n)}"
    ans = f"{c1 * c2}{v}{sup(m + n)}"
    return Q(f"Simplify: {t}", ans, ["Multiply the coefficients.", "Add the exponents.", f"{ans}."], [f"{c1 + c2}{v}{sup(m + n)}", f"{c1 * c2}{v}{sup(m * n) if m * n > 1 else ''}", f"{c1 * c2}{v}{sup(m + n + 1)}"],
             EQV(t.replace("·", "*"), [v]), why=["Added the coefficients", "Multiplied the exponents", ""])


@fam("012")
def s8_quotient(r, L):
    if L == 0:
        b, m, n = r.randint(2, 9), r.randint(5, 12), r.randint(1, 4)
        t = f"{b}{sup(m)} ÷ {b}{sup(n)}"
        ans = f"{b}{sup(m - n)}"
        return Q(f"Simplify. Write your answer as a power: {t}", ans, ["When dividing powers with the same base, subtract the exponents.", f"{m} - {n} = {m - n}.", f"{t} = {ans}."],
                 [f"{b}{sup(m + n)}", f"1{sup(m - n)}", f"{b}{sup(m // n) if m // n > 1 and m // n != m - n else sup(m - n + 1)}"], PY("power_form", base=str(b), expr=f"{b}^{m} ÷ {b}^{n}".replace("^", "**").replace("**", "^")) if False else
                 PY("power_form", base=str(b), expr=t), why=["Added the exponents", "Divided the bases", "Divided the exponents"])
    if L == 1:
        v = pick(r, ["x", "y", "n"])
        c, k = r.randint(2, 9), r.randint(2, 6)
        m, n = r.randint(4, 10), r.randint(1, 3)
        num, den = f"{c * k}{v}{sup(m)}", f"{k}{v}{sup(n) if n > 1 else ''}"
        ans = f"{c}{v}{sup(m - n) if m - n > 1 else ''}"
        return Q(f"Simplify. Assume {v} ≠ 0. ({num})/({den})", ans, ["Divide the coefficients.", "Subtract the exponents.", f"{ans}."],
                 [f"{c}{v}{sup(m + n)}", f"{c * k * k}{v}{sup(m - n) if m - n > 1 else ''}", f"{c}{v}{sup(m // n) if m // n > 1 else ''}" if m // n != m - n else f"{c + 1}{v}{sup(m - n)}"],
                 EQV(f"({num})/({den})", [v]), why=["Added the exponents", "Multiplied the coefficients", "Divided the exponents"])
    b = r.randint(2, 6)
    kind = pick(r, ["zero", "neg", "mixed"])
    if kind == "zero":
        t = f"{b}{sup(r.randint(2, 9))} ÷ {b}{sup(r.randint(2, 9))}"
        e1, e2 = [int(s.translate(str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789"))) for s in re.findall("[⁰¹²³⁴⁵⁶⁷⁸⁹]+", t)]
        need(e1 == e2 or True)
        t = f"{b}{sup(e1)} ÷ {b}{sup(e1)}"
        return Q(f"Evaluate: {t}", "1", [f"Subtract exponents: {b}{sup(0)}.", "Any nonzero number to the zero power is 1."], ["0", str(b), f"{b ** e1}"], V(t),
                 why=["Thought a zero exponent gives 0", "Thought a zero exponent gives the base", ""])
    m, n = r.randint(1, 4), r.randint(5, 8)
    t = f"{b}{sup(m)} ÷ {b}{sup(n)}"
    v = F(1, b ** (n - m))
    return Q(f"Evaluate: {t}. Write your answer as a fraction.", N(v), [f"Subtract exponents: {m} - {n} = {m - n}.", f"{b}{sup(m - n)} = 1/{b}{sup(n - m)}.", f"= {N(v)}."],
             [str(-b ** (n - m)), N(F(-1, b ** (n - m))), str(b ** (n - m))], V(t), why=["Wrote the negative exponent as a negative number", "Made the answer negative", "Flipped the answer"])


@fam("12")
def s7_numeric(r, L):
    b = pick(r, [2, 3, 10])
    m, n = r.randint(1, 4), r.randint(1, 3)
    t = f"{b}{sup(m)} · {b}{sup(n)}"
    v = b ** (m + n)
    return Q(f"Evaluate: {t}", f"{v:,}", [f"Add exponents: {b}{sup(m + n)}.", f"{b}{sup(m + n)} = {v:,}."], [f"{b ** (m * n):,}", f"{(b * b) ** (m + n):,}", f"{b ** m + b ** n:,}"], V(t.replace("·", "*")),
             why=["Multiplied the exponents", "Multiplied the bases", "Added the powers instead of multiplying"])


@fam("2", mode="mc")
def s8_power_of_power(r, L):
    v = pick(r, ["x", "y"])
    a, b = r.randint(2, 5), r.randint(2, 4)
    c = r.randint(2, 3)
    t = f"({c}{v}{sup(a)}){sup(b)}"
    ans = f"{c ** b}{v}{sup(a * b)}"
    opts = [(ans, True), (f"{c * b}{v}{sup(a * b)}", False), (f"{c ** b}{v}{sup(a + b)}", False), (f"{c}{v}{sup(a * b)}", False)]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    return Q(f"Simplify: {t}", ans, [f"Raise the coefficient to the power: {c}{sup(b)} = {c ** b}.", f"Multiply exponents: {a} × {b} = {a * b}.", f"{ans}."], options=opts, chk=EQV(t, [v]), mode="mc")


# ============================================================== S9 Scientific Notation
def sci_txt(m, e):
    return f"{D(m)} × 10{sup(e)}"


@fam("012")
def s9_to_sci(r, L):
    m = rdig(r, 2 if L == 0 else 3)
    e = r.randint(3, 9) if L == 0 else pick(r, list(range(-7, -1)) + list(range(4, 12)))
    x = m * F(10) ** e
    std = dtext(x) if e > 0 else D(x)
    ans = sci_txt(m, e)
    return Q(f"Write {std} in scientific notation.", ans, ["Move the decimal point so there is one nonzero digit to its left.", f"The decimal moves {abs(e)} places {'left' if e > 0 else 'right'}.", f"{std} = {ans}."],
             [sci_txt(m, -e), sci_txt(m * 10, e - 1), sci_txt(m, e + 1)], PY("sci_form", expr=f"{m.numerator}/{m.denominator}*10^({e})".replace("^", "^")),
             why=["Used the wrong sign on the exponent", "Left the first factor greater than 10", "Miscounted the places"])


def rdig(r, k):
    d = [r.randint(1, 9)] + [r.randint(0, 9) for _ in range(k - 2)] + [r.randint(1, 9)]
    return F(int("".join(map(str, d))), 10 ** (k - 1))


@fam("012")
def s9_to_std(r, L):
    m = rdig(r, 3)
    e = r.randint(3, 8) if L == 0 else pick(r, [-5, -4, -3, -2, 4, 5, 6, 7])
    x = m * F(10) ** e
    std = dtext(x) if e > 0 else D(x)
    return Q(f"Write {sci_txt(m, e)} in standard form.", std, [f"Move the decimal point {abs(e)} places to the {'right' if e > 0 else 'left'}.", f"{sci_txt(m, e)} = {std}."],
             [dtext(m * F(10) ** -e) if e < 0 else D(m * F(10) ** -e), dtext(m * F(10) ** (e + 1)) if e > 0 else D(m * F(10) ** (e + 1)), dtext(m * F(10) ** (e - 1)) if e > 1 else D(m * F(10) ** (e - 1))],
             V(f"{D(m)} * 10^({e})".replace("^", "^")), why=["Moved the decimal point the wrong way", "Moved one place too many", "Moved one place too few"])


@fam("2")
def s9_multiply(r, L):
    a, b = rdig(r, 2), rdig(r, 2)
    e1, e2 = r.randint(2, 8), r.randint(-6, 6)
    p = a * b
    e = e1 + e2
    if p >= 10:
        p, e = p / 10, e + 1
    t = f"({sci_txt(a, e1)})({sci_txt(b, e2)})"
    ans = sci_txt(p, e)
    return Q(f"Multiply. Write the answer in scientific notation: {t}", ans, [f"Multiply the first factors: {D(a)} × {D(b)} = {D(a * b)}.", f"Add the exponents: {e1} + {par(e2)} = {e1 + e2}.",
                                                                         f"Adjust so the first factor is between 1 and 10: {ans}." if a * b >= 10 else f"Result: {ans}."],
             [sci_txt(a * b, e1 + e2) if a * b >= 10 else sci_txt(p, e1 * e2), sci_txt(p, e1 * e2) if e1 * e2 != e else sci_txt(p, e + 2), sci_txt(a + b, e1 + e2) if a + b < 10 else sci_txt(p, e - 1)],
             PY("sci_form", expr=f"{D(a)}*10^({e1})*{D(b)}*10^({e2})"), why=["Did not adjust the first factor to be less than 10", "Multiplied the exponents", "Added the first factors"])


@fam("12", mode="mc")
def s9_compare(r, L):
    ms = [rdig(r, 2) for _ in range(4)]
    es = [r.randint(-4, 8) for _ in range(4)]
    vals = [m * F(10) ** e for m, e in zip(ms, es)]
    need(len(set(vals)) == 4)
    txt = [sci_txt(m, e) for m, e in zip(ms, es)]
    big = txt[vals.index(max(vals))]
    opts = [(t, t == big) for t in txt]
    return Q("Which number is greatest?", big, ["Compare the powers of 10 first.", "If the powers are equal, compare the first factors.", f"Greatest: {big}."], options=opts,
             chk=PY("extreme", items=txt, max=True), mode="mc")


@fam("12")
def s9_context(r, L):
    m, e = rdig(r, 2), r.randint(5, 9)
    obj = pick(r, ["miles to a planet", "people in a region", "grains of sand in a bucket", "stars in a galaxy section"])
    x = m * F(10) ** e
    return Q(f"There are about {dtext(x)} {obj}. Write this number in scientific notation.", sci_txt(m, e), ["Place the decimal after the first nonzero digit.", f"Count the places moved: {e}.", f"{sci_txt(m, e)}."],
             [sci_txt(m * 10, e - 1), sci_txt(m, e - 1), sci_txt(m, -e)], PY("sci_form", expr=f"{D(m)}*10^({e})"), why=["First factor not between 1 and 10", "Miscounted the places", "Used a negative exponent for a large number"],
             tags=["modeling"])


# ============================================================== S10 Cube Roots
@fam("012")
def s10_eval(r, L):
    k = r.randint(1, 10) if L < 2 else nz(r, -10, 10)
    n = k ** 3
    if L == 1 and r.random() < 0.4:
        a, b = r.randint(1, 5), r.randint(2, 6)
        t = f"∛{a ** 3} + ∛{b ** 3}"
        return Q(f"Evaluate: {t}", str(a + b), [f"∛{a ** 3} = {a} and ∛{b ** 3} = {b}.", f"{a} + {b} = {a + b}."], [str(round((a ** 3 + b ** 3) ** (1 / 3), 2)), str(F(a ** 3 + b ** 3, 3)) if (a ** 3 + b ** 3) % 3 == 0 else str(a + b + 1), str(a * b)],
                     V(t), why=["Added inside the cube root", "Divided by 3", "Multiplied instead of adding"])
    t = f"∛({n})" if n < 0 else f"∛{n}"
    return Q(f"Evaluate: {t}", str(k), [f"Find the number that, used as a factor three times, gives {n}.", f"{par(k)} × {par(k)} × {par(k)} = {n}.", f"{t} = {k}."],
             [N(F(n, 3)) if n % 3 == 0 else str(n // 3), str(-k), str(k * k)], V(t), why=["Divided by 3 instead of taking the cube root", "Made a sign error", ""])


@fam("012")
def s10_solve(r, L):
    k = r.randint(2, 10) if L < 2 else nz(r, -6, 6)
    c = 1 if L == 0 else r.randint(2, 5)
    eq = f"x{sup(3)} = {k ** 3}" if c == 1 else f"{c}x{sup(3)} = {c * k ** 3}"
    return Q(f"Solve: {eq}", f"x = {k}", ["Divide by the coefficient if needed." if c > 1 else "Take the cube root of both sides.", "Take the cube root of both sides." if c > 1 else f"∛{k ** 3} = {k}.", f"x = {k}."],
             [f"x = {N(F(k ** 3, 3))}" if k ** 3 % 3 == 0 else f"x = {k ** 3 // 3}", f"x = {-k}", f"x = {k * k}"], PY("roots_match", eq=eq), why=["Divided by 3 instead of taking the cube root", "Gave a sign error", ""])


@fam("12")
def s10_context(r, L):
    k = r.randint(2, 12)
    return Q(f"A cube-shaped box has a volume of {k ** 3:,} cubic inches. How long is each edge?", f"{k} inches", [f"V = s³, so s = ∛{k ** 3}.", f"{k}³ = {k ** 3}.", f"Each edge is {k} inches."],
             [f"{N(F(k ** 3, 3)) if k ** 3 % 3 == 0 else k ** 3 // 3} inches", f"{round(k ** 1.5, 1)} inches", f"{k * k} inches"], V(f"∛{k ** 3}"), why=["Divided the volume by 3", "Took a square root", ""], tags=["modeling"])


SKILLS = {
    1: dict(name="Divisibility and Factors", std=["6.NS.B.4", "4.OA.B.4"], fams=[s1_divisible, s1_factor_list, s1_prime, s1_digit], extra=[err_of(s1_factor_list), open_of(s1_factor_list)]),
    2: dict(name="Exponents", std=["6.EE.A.1"], fams=[s2_eval, s2_write, s2_context], extra=[err_of(s2_eval), open_of(s2_eval), select_of(s2_eval)]),
    3: dict(name="Prime Factorization and Greatest Common Factor", std=["6.NS.B.4"], fams=[s3_pf, s3_gcf, s3_gcf_word], extra=[err_of(s3_gcf), open_of(s3_gcf), err_of(s3_pf)]),
    4: dict(name="Simplifying Fractions", std=["4.NF.A.1", "6.NS.B.4"], fams=[s4_simplify, s4_equiv, s4_algebraic, s4_which_equiv], extra=[err_of(s4_simplify), open_of(s4_simplify), select_of(s4_simplify)]),
    5: dict(name="Rational Numbers", std=["7.NS.A.2d", "6.NS.C.6"], fams=[s5_to_fraction, s5_classify, s5_order, s5_between], extra=[err_of(s5_to_fraction), open_of(s5_to_fraction)]),
    6: dict(name="Irrational Numbers", std=["8.NS.A.1", "8.NS.A.2"], fams=[s6_which, s6_between, s6_estimate, s6_order], extra=[err_of(s6_between), open_of(s6_between)]),
    7: dict(name="Exponents and Multiplication", std=["8.EE.A.1"], fams=[s7_product, s7_numeric], extra=[err_of(s7_product), open_of(s7_product), select_of(s7_product)]),
    8: dict(name="Exponents and Division", std=["8.EE.A.1"], fams=[s8_quotient, s8_power_of_power], extra=[err_of(s8_quotient), open_of(s8_quotient)]),
    9: dict(name="Scientific Notation", std=["8.EE.A.3", "8.EE.A.4"], fams=[s9_to_sci, s9_to_std, s9_multiply, s9_compare, s9_context], extra=[err_of(s9_to_sci), open_of(s9_to_std), err_of(s9_to_std)]),
    10: dict(name="Cube Roots", std=["8.EE.A.2"], fams=[s10_eval, s10_solve, s10_context], extra=[err_of(s10_eval), open_of(s10_eval), select_of(s10_eval)]),
}
