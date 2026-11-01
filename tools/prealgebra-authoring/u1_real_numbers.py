"""Unit 1 — Real Numbers and Exponents (real-numbers-exponents)."""
from lib import *

UNIT_ID = "real-numbers-exponents"
ABBR = "rne"

SMALL_DEN = [2, 3, 4, 5, 6, 8, 10]


def rfrac(r, dens=SMALL_DEN, lo=1, hi=11, neg=True, proper=False):
    while True:
        d = pick(r, dens)
        n = r.randint(lo, hi if not proper else d - 1) * (pick(r, [1, -1]) if neg else 1)
        x = F(n, d)
        if x.denominator != 1:
            return x


# ======================================================================= S1 Rational numbers
SETS = ["natural number", "whole number", "integer", "rational number", "irrational number"]


@fam("01", mode="mc")
def s1_classify(r, L):
    pool0 = [(str(r.randint(2, 40)), "natural number"), ("0", "whole number"), (str(-r.randint(2, 30)), "integer"),
             (N(rfrac(r)), "rational number"), (D(F(r.randint(11, 99), 10) * pick(r, [1, -1])), "rational number")]
    sq = pick(r, [4, 9, 16, 25, 36, 49, 64, 81, 100])
    k = pick(r, [2, 3, 4, 5])
    pool1 = [(f"√{sq}", "natural number"), (f"-√{sq}", "integer"), (f"√{pick(r, [2, 3, 5, 6, 7, 10, 11, 13, 15])}", "irrational number"),
             (rep_text(F(r.randint(1, 8), 9)), "rational number"), (f"{r.randint(2, 9)}π", "irrational number"),
             (f"{k * r.randint(3, 12)}/{k}", "natural number"), (f"{-k * r.randint(3, 9)}/{k}", "integer"), (f"0/{k}", "whole number")]
    num, want = pick(r, pool0 if L == 0 else pool1 + pool0[3:])
    steps = {"natural number": [f"{num} simplifies to a counting number (1, 2, 3, …).", "Natural numbers are the most specific set that contains it."],
             "whole number": [f"{num} = 0, which is a whole number but not a natural (counting) number."],
             "integer": [f"{num} simplifies to a negative whole number, so it is an integer but not a whole number."],
             "rational number": [f"{num} can be written as a fraction of integers, but it is not an integer.", "So the most specific set is the rational numbers."],
             "irrational number": [f"{num} cannot be written as a ratio of two integers: its decimal never ends or repeats."]}[want]
    return P(f"Which is the most specific classification of {num}?", want, steps,
             options=[(s_, s_ == want) for s_ in SETS], chk=chk_py("classify", num=num), tags=["reasoning"], mode="mc")


@fam("01")
def s1_between_ints(r, L):
    if L == 0:
        x = F(r.randint(5, 40), pick(r, [2, 3, 4, 5])) * pick(r, [1, -1])
        need(x.denominator != 1)
        num = N(x)
    else:
        x = F(r.randint(-60, 60), pick(r, [3, 6, 7, 8, 9]))
        need(x.denominator != 1)
        num = pick(r, [N(x), D(F(r.randint(-999, 999), 100)) if r.random() < 0.5 else N(x)])
        x = F(num) if "/" not in num else x
        need(x.denominator != 1)
    lo = math.floor(x)
    ans = f"{lo} and {lo + 1}"
    wrong = [f"{lo + 1} and {lo + 2}", f"{lo - 1} and {lo}", f"{-lo - 1} and {-lo}"]
    steps = [f"{num} = {rep_text(x) if x.denominator not in (2, 4, 5, 8, 10, 20, 25, 50, 100) else D(x)} as a decimal.",
             f"It is greater than {lo} and less than {lo + 1}."]
    if x < 0:
        steps.append("For negative numbers, the integer to the left on the number line is the smaller one.")
    return P(f"Between which two consecutive integers does {num} lie on a number line?", ans, steps, wrong,
             chk_py("between_ints", num=num), tags=["misconception"] if x < 0 else [])


@fam("012")
def s1_quotient(r, L):
    kind = pick(r, ["mixed", "dec", "int"] if L < 2 else ["mixed", "dec", "pct"])
    if kind == "mixed":
        w, d = r.randint(1, 6), pick(r, [3, 4, 5, 6, 8])
        n = r.randint(1, d - 1)
        need(math.gcd(n, d) == 1)
        neg = L > 0 and r.random() < 0.6
        x = (w + F(n, d)) * (-1 if neg else 1)
        shown = ("-" if neg else "") + f"{w} {n}/{d}"
        wrong = [N((w * n + d) * (-1 if neg else 1) * F(1, d)) if (w * n + d) % d else N(F(w + n, d)),
                 N(F(w + n, d) * (-1 if neg else 1)), N(-x)]
        steps = [f"{w} {n}/{d} = ({w} · {d} + {n})/{d} = {N(abs(x))}.", f"So {shown} = {N(x)}, a ratio of two integers."]
    elif kind == "dec":
        places = 2 if L == 0 else 3
        k = r.randint(11, 10 ** places - 1)
        need(k % 10)
        x = F(k, 10 ** places) * (pick(r, [1, -1]) if L else 1)
        need(x.denominator != 1)
        shown = D(x)
        wrong = [N(F(k, 10 ** (places - 1)) * (1 if x > 0 else -1)), f"{abs(k) if x > 0 else -abs(k)}/{10 ** places}" if math.gcd(k, 10) == 1 else N(F(10 ** places, k)),
                 N(1 / x) if abs(x) < 1 else N(-x)]
        steps = [f"{shown} = {'-' if x < 0 else ''}{k}/{10 ** places}.", f"Simplify: {N(x)}."]
    elif kind == "int":
        v = nz(r, -40, 40)
        x = F(v)
        shown = str(v)
        return P(f"Which fraction shows that {v} is a rational number?", f"{v * 3}/3",
                 [f"Any integer n equals n/1, so {v} = {v}/1 = {v * 3}/3."],
                 [f"{v}/0", f"3/{v * 3}", f"{v + 3}/3"], chk_val(str(v)), mode="mc", tags=["reasoning"])
    else:
        p = pick(r, [12.5, 37.5, 62.5, 87.5, 2.5, 7.5, 0.4, 0.8])
        x = F(str(p)) / 100
        shown = f"{p}%"
        wrong = [N(F(str(p)) / 10), N(1 / x), N(F(str(p)).limit_denominator(100) / 1000)]
        steps = [f"{p}% = {p}/100 = {D(x)}.", f"{D(x)} = {N(x)} in simplest form."]
        return P(f"Write {shown} as a ratio of two integers in simplest form.", N(x), steps, wrong,
                 chk_py("frac_text", expr=D(x)), tags=["connections"])
    return P(f"Write {shown} as a ratio of two integers in simplest form.", N(x), steps, wrong,
             chk_py("frac_text", expr=N(x)))


@fam("12", mode="mc")
def s1_between_rational(r, L):
    a = F(r.randint(1, 7), r.randint(5, 12)) * (pick(r, [1, -1]) if L == 2 else 1)
    b = a + F(1, r.randint(6, 15))
    need(a.denominator != 1 and b.denominator != 1)
    if L == 2 and r.random() < 0.5:
        a, b = -b, -a
    lo, hi = N(a), N(b)
    med = F(a.numerator + b.numerator, a.denominator + b.denominator)
    good = (a + b) / 2 if L == 1 else med
    need(a < good < b)
    outs = [F(abs(a.numerator) + abs(b.numerator), abs(a.denominator) * 2) * (1 if a > 0 else -1),
            b + F(1, 20), a - F(1, 30), F(a.numerator + 1, a.denominator + 1) if a > 0 else a - F(1, 4), (a + b)]
    wrong = [N(o) for o in outs if not (a < o < b)]
    steps = [f"Find a common denominator: {lo} = {N(a)} and {hi} = {N(b)}.",
             f"{N(good)} ≈ {D(good, 4)} is greater than {lo} ≈ {D(a, 4)} and less than {hi} ≈ {D(b, 4)}."]
    if L == 2:
        steps.append("Adding the numerators and adding the denominators (the mediant) always gives a number between two positive fractions.")
    return P(f"Which number lies between {lo} and {hi}?", N(good), steps, wrong,
             chk_py("strictly_between", lo=lo, hi=hi), tags=["reasoning"], mode="mc")


@fam("012")
def s1_order(r, L):
    for _ in range(50):
        if L == 0:
            vals = [F(r.randint(-9, 9), pick(r, [2, 4, 5])) for _ in range(3)] + [F(r.randint(-9, 9), 10)]
        elif L == 1:
            base = F(r.randint(-9, 9), 10)
            vals = [base + F(r.randint(-5, 5), pick(r, [8, 20, 40])) for _ in range(3)] + [base]
        else:
            vals = [-F(r.randint(1, 9), pick(r, [3, 6, 9, 11])) for _ in range(2)] + [-F(r.randint(1, 9), 10), F(r.randint(-8, 8), pick(r, [12, 7]))]
        if len(set(vals)) == 4:
            break
    need(len(set(vals)) == 4)
    texts = []
    for i, v in enumerate(vals):
        texts.append(D(v) if is_term(v) and (i % 2 == 1 or v.denominator == 1) else (rep_text(v) if (L == 2 and i == 3) else N(v)))
    need(len(set(texts)) == 4 and all(not t.endswith("/1") for t in texts))
    desc = L == 2 and r.random() < 0.4
    srt = [t for _, t in sorted(zip(vals, texts), reverse=desc)]
    absord = [t for _, t in sorted(zip([abs(v) for v in vals], texts), reverse=desc)]
    rev = srt[::-1]
    shuffled = texts[:]
    r.shuffle(shuffled)
    need(shuffled != srt)
    ans = ", ".join(srt)
    wrong = [", ".join(absord), ", ".join(rev), ", ".join(srt[1:2] + srt[:1] + srt[2:])]
    word = "greatest to least" if desc else "least to greatest"
    steps = ["Write each number as a decimal: " + "; ".join(f"{t} = {D(v, 4) if not is_term(v) else D(v)}" for t, v in zip(texts, vals)) + ".",
             f"Order from {word}: {ans}."]
    if any(v < 0 for v in vals):
        steps.append("Among negative numbers, the one farther from 0 is smaller.")
    return P(f"Order from {word}: " + "; ".join(shuffled) + ".", ans, steps, wrong,
             chk_py("order", items=texts, desc=desc), tags=["misconception", "multiple-representations"])


@fam("2")
def s1_fraction_of_way(r, L):
    a = r.randint(-9, 2)
    b = a + pick(r, [4, 5, 6, 8, 10])
    fr_ = F(r.randint(1, 7), pick(r, [3, 4, 5, 8]))
    need(fr_ < 1)
    v = a + fr_ * (b - a)
    ans = N(v)
    wrong = [N(fr_ * (b - a)), N(b - fr_ * (b - a)), N(a + fr_ * b)]
    steps = [f"The distance from {a} to {b} is {b} - ({a}) = {b - a}.", f"{N(fr_)} of {b - a} is {N(fr_ * (b - a))}.",
             f"Start at {a} and move right {N(fr_ * (b - a))}: {a} + {N(fr_ * (b - a))} = {ans}."]
    return P(f"Point P is {N(fr_)} of the way from {a} to {b} on a number line. What rational number is at P?", ans, steps, wrong,
             chk_val(f"{a} + ({N(fr_)})({b} - ({a}))"), tags=["reasoning", "multistep"])


@fam("2")
def s1_mean_between(r, L):
    a, b = rfrac(r, [3, 4, 6, 8]), rfrac(r, [5, 10, 12])
    need(a != b)
    lo, hi = min(a, b), max(a, b)
    m = (lo + hi) / 2
    wrong = [N(lo + hi), N((lo.numerator + hi.numerator) * F(1, lo.denominator + hi.denominator)) if False else N((hi - lo) / 2), N(hi - lo)]
    steps = [f"The number halfway between two numbers is their mean: ({N(lo)} + {N(hi)}) ÷ 2.",
             f"{N(lo)} + {N(hi)} = {N(lo + hi)}, and {N(lo + hi)} ÷ 2 = {N(m)}."]
    return P(f"What rational number is exactly halfway between {N(lo)} and {N(hi)} on a number line?", N(m), steps, wrong,
             chk_val(f"({N(lo)} + {N(hi)})/2"), tags=["reasoning"])


@fam("012", mode="mc")
def s1_set_statement(r, L):
    stmts = [("Every integer is a rational number.", True), ("Every rational number is an integer.", False),
             ("Every whole number is a natural number.", False), ("Every natural number is a whole number.", True),
             ("A repeating decimal is irrational.", False), ("Every terminating decimal is rational.", True),
             ("Some fractions are irrational.", False), ("Zero is a rational number.", True),
             ("A negative number cannot be rational.", False), ("Every rational number can be written as a terminating decimal.", False)]
    t = [s for s in stmts if s[1]]
    f_ = [s for s in stmts if not s[1]]
    true_one = pick(r, t)
    falses = pick(r, f_, 3)
    opts = falses + [true_one]
    r.shuffle(opts)
    return P("Which statement about rational numbers is true?", true_one[0],
             [f"\"{true_one[0]}\" is true.", "Each other statement has a counterexample, such as 1/2 (rational, not an integer), 0 (whole, not natural), 0.333… (repeating, rational) or -3 (negative and rational)."],
             options=opts, chk={"kind": "text", "accept": [true_one[0]]}, tags=["reasoning", "misconception"], mode="mc")


def x_select_rational(r, L):
    rats = [rep_text(F(r.randint(1, 10), 11)), f"√{pick(r, [16, 25, 49, 81, 121])}", N(rfrac(r)), D(F(-r.randint(101, 999), 100)),
            f"-{r.randint(2, 30)}", "0"]
    irrs = [f"√{pick(r, [2, 3, 5, 7, 10, 15])}", "π", f"{r.randint(1, 4)}.1010010001… (pattern never repeats)", f"√{pick(r, [20, 30, 40, 50])}"]
    a = pick(r, rats, 3 if L < 2 else 2)
    b = pick(r, irrs, 2 if L < 2 else 3)
    opts = [(x, True) for x in a] + [(x, False) for x in b]
    return P("Select ALL rational numbers.", None,
             ["A rational number can be written as a ratio of two integers; terminating and repeating decimals and perfect-square roots are rational."] +
             [f"{x}: {'rational' if c else 'irrational'}." for x, c in opts], options=opts, chk=chk_py("is_rational"), tags=["reasoning"])


s1_select = fam("012")(x_select_rational)


@fam("012")
def s1_open(r, L):
    a, b = rfrac(r, [4, 5, 8]), F(r.randint(1, 9), 11)
    w = r.randint(2, 5)
    parts = [(f"Classify {-w * 2} using the most specific set: natural number, whole number, integer, or rational number.", "integer", chk_py("classify", num=str(-w * 2))),
             (f"Write {D(a)} as a fraction in simplest form.", N(a), chk_py("frac_text", expr=D(a))),
             (f"Write {N(b)} as a decimal.", rep_text(b), chk_py("dec_text", expr=N(b))),
             (f"Which is greater, {D(a)} or {N(b)}?", D(a) if a > b else N(b), chk_py("extreme", items=[D(a), N(b)], max=True))]
    need(a != b)
    return P("Answer each part about rational numbers.", None,
             [f"{-w * 2} is a negative whole number, so it is an integer.", f"{D(a)} = {N(a)}.",
              f"Divide {b.numerator} by 11: the block repeats.", f"Compare decimals: {D(a)} and {rep_text(b)}."],
             parts=parts, tags=["multiple-representations"])


@fam("12")
def s1_error(r, L):
    k = r.randint(1, 9)
    blk = f"{k}{r.randint(0, 9)}"
    need(blk[0] != blk[1])
    x = F(int(blk), 99)
    shown = rep_text(x)
    wrong = [N(F(int(blk), 100)), N(F(int(blk), 90)), N(F(int(blk[0]), int(blk[1])))]
    return P(f"Jordan wrote {shown} as {N(F(int(blk), 100))}, saying \"the digits {blk} are hundredths.\" What fraction in simplest form actually equals {shown}?",
             N(x), [f"{N(F(int(blk), 100))} = {D(F(int(blk), 100))} terminates, so it cannot equal a repeating decimal.",
                    f"Let n = {shown}. Then 100n = {blk}.{blk}{blk}…, and 100n - n = {blk}.", f"99n = {blk}, so n = {blk}/99 = {N(x)}."],
             wrong, chk_py("frac_text", expr=f"{blk}/99"), tags=["error-analysis", "misconception"])


# ======================================================================= S2 Operations with rational numbers
def opstr(op):
    return {"+": "+", "-": "-", "*": "·", "/": "÷"}[op]


def apply(a, b, op):
    return {"+": a + b, "-": a - b, "*": a * b, "/": a / b}[op]


def ptxt(x):
    s = N(x)
    return f"({s})" if x < 0 else s


@fam("012")
def s2_frac_addsub(r, L):
    dens = [[2, 4, 8], [3, 4, 6, 8, 12], [3, 5, 6, 9, 10, 12, 15]][L]
    a, b = rfrac(r, dens, neg=L > 0), rfrac(r, dens, neg=True)
    op = pick(r, ["+", "-"])
    v = apply(a, b, op)
    expr = f"{N(a)} {op} {ptxt(b)}"
    if L == 2:
        c = rfrac(r, dens)
        expr = f"{expr} - {ptxt(c)}"
        v = v - c
    wrong = [N(F(a.numerator + (b.numerator if op == "+" else -b.numerator), a.denominator + b.denominator)) if a.denominator + b.denominator else "0",
             N(apply(a, -b, op)), N(-v)]
    steps = [f"Rewrite with a common denominator and keep track of signs.", f"{expr} = {N(v)}."]
    return P(f"Evaluate: {expr}", N(v), steps, wrong, chk_val(expr), tags=["misconception"] if L else [])


@fam("012")
def s2_frac_muldiv(r, L):
    a, b = rfrac(r, [2, 3, 4, 5, 6, 8], neg=L > 0), rfrac(r, [2, 3, 4, 5, 9], neg=True)
    op = pick(r, ["*", "/"])
    v = apply(a, b, op)
    expr = f"{N(a)} {opstr(op)} {ptxt(b)}" if op == "/" else f"({N(a)})({N(b)})"
    if L == 2:
        c = rfrac(r, [2, 3, 4])
        expr = f"{expr} {opstr('*')} {ptxt(c)}" if op == "*" else f"({expr}) · {ptxt(c)}"
        v *= c
    wrong = [N(a * b if op == "/" else a / b), N(-v), N(F(a.numerator * b.denominator, a.denominator * b.numerator) if op == "*" else a * b * -1)]
    steps = (["To divide, multiply by the reciprocal of the divisor."] if op == "/" else ["Multiply numerators and multiply denominators."]) + \
            ["The product or quotient of two numbers with different signs is negative; same signs gives positive.", f"{expr} = {N(v)}."]
    return P(f"Evaluate: {expr}", N(v), steps, wrong, chk_val(expr), tags=["misconception"])


@fam("012")
def s2_decimal(r, L):
    a = F(r.randint(-99, 99), 10) if L == 0 else F(r.randint(-999, 999), 100)
    b = F(nz(r, -60, 60), 10)
    op = pick(r, ["+", "-", "*", "/"])
    if op == "/":
        q = F(nz(r, -12, 12)) if L < 2 else F(nz(r, -40, 40), 4)
        a = q * b
    v = apply(a, b, op)
    need(is_term(v) and a != 0)
    expr = f"{D(a)} {opstr(op) if op != '*' else '×'} {('(' + D(b) + ')') if b < 0 else D(b)}"
    wrong = [D(-v), D(apply(a, -b, op)) if op in "+-" else D(v * 10), D(v / 10) if op in "*/" else D(abs(a) + abs(b))]
    return P(f"Evaluate: {expr}", D(v), [f"Compute {D(abs(a))} {opstr(op)} {D(abs(b))} and apply the sign rules.", f"{expr} = {D(v)}."],
             wrong, chk_val(expr.replace("×", "*")), tags=["misconception"] if b < 0 else [])


@fam("12")
def s2_order_ops(r, L):
    a, b, c = rfrac(r, [2, 3, 4]), rfrac(r, [2, 3, 5]), rfrac(r, [2, 4, 6])
    form = pick(r, ["a*b+c", "(a+b)*c", "a-b/c", "a/(b-c)"])
    try:
        v = {"a*b+c": a * b + c, "(a+b)*c": (a + b) * c, "a-b/c": a - b / c, "a/(b-c)": a / (b - c)}[form]
    except ZeroDivisionError:
        raise Reject()
    expr = {"a*b+c": f"({N(a)})({N(b)}) + {ptxt(c)}", "(a+b)*c": f"({N(a)} + {ptxt(b)}) · {ptxt(c)}",
            "a-b/c": f"{N(a)} - {ptxt(b)} ÷ {ptxt(c)}", "a/(b-c)": f"{N(a)} ÷ ({N(b)} - {ptxt(c)})"}[form]
    wrongv = {"a*b+c": a * (b + c), "(a+b)*c": a + b * c, "a-b/c": (a - b) / c, "a/(b-c)": a / b - c}[form]
    need(wrongv != v)
    return P(f"Evaluate: {expr}", N(v), ["Follow the order of operations: grouping first, then multiplication and division, then addition and subtraction.", f"{expr} = {N(v)}."],
             [N(wrongv), N(-v), N(v + 1)], chk_val(expr), tags=["multistep", "misconception"])


@fam("012")
def s2_context(r, L):
    nm = pick(r, NAMES)
    k = pick(r, ["temp", "dive", "recipe", "money"] if L else ["temp", "dive", "money"])
    if k == "temp":
        t0, ch, h = r.randint(-8, 10), F(r.randint(-25, -5), 10) if L else -r.randint(2, 4), r.randint(3, 6)
        v = t0 + ch * h
        need(is_term(v))
        return P(f"At 6 p.m. the temperature was {t0}°F. It changed by {D(ch)}°F each hour for {h} hours. What was the temperature then?",
                 f"{D(v)}°F", [f"Total change: {h} × ({D(ch)}) = {D(ch * h)}°F.", f"{t0} + ({D(ch * h)}) = {D(v)}°F."],
                 [f"{D(t0 - ch * h)}°F", f"{D(ch * h)}°F", f"{D(-v)}°F"], chk_val(f"{t0} + {h}*({D(ch)})"), tags=["modeling"])
    if k == "dive":
        d0 = -r.randint(10, 40)
        rate = F(r.randint(3, 9), 2)
        t = r.randint(2, 8)
        v = d0 - rate * t if L else d0 + rate * t
        word = "descends" if L else "rises"
        return P(f"A diver is at {d0} feet (below sea level). She {word} {D(rate)} feet per minute for {t} minutes. What is her new elevation?",
                 f"{D(v)} feet", [f"Change: {'-' if L else '+'}{D(rate)} × {t} = {'-' if L else ''}{D(rate * t)} feet.", f"{d0} {'-' if L else '+'} {D(rate * t)} = {D(v)} feet."],
                 [f"{D(d0 + (rate * t if L else -rate * t))} feet", f"{D(-v)} feet", f"{D(rate * t)} feet"],
                 chk_val(f"{d0} {'-' if L else '+'} {D(rate)}*{t}"), tags=["modeling"])
    if k == "recipe":
        need_ = F(r.randint(2, 7), pick(r, [3, 4]))
        scale = F(r.randint(3, 7), 2)
        v = need_ * scale
        need(v.denominator != 1)
        return P(f"A recipe uses {N(need_)} cup of flour per batch. How many cups are needed for {N(scale)} batches? Give the answer as a fraction or mixed number.",
                 f"{N(v)} cups", [f"Multiply: {N(need_)} × {N(scale)} = {N(v)}."],
                 [f"{N(need_ + scale)} cups", f"{N(need_ / scale)} cups", f"{N(scale / need_)} cups"],
                 chk_val(f"({N(need_)})({N(scale)})"), tags=["modeling"])
    bal = F(r.randint(2000, 9000), 100)
    spent = [F(r.randint(500, 3000), 100) for _ in range(2 + L)]
    v = bal - sum(spent)
    txt = ", ".join(money(s) for s in spent)
    return P(f"{nm} had {money(bal)} in an account and made purchases of {txt}. What is the new balance? (A negative balance means the account is overdrawn.)",
             money(v), [f"Total spent: {money(sum(spent))}.", f"{money(bal)} - {money(sum(spent))} = {money(v)}."],
             [money(bal + sum(spent)), money(-v), money(sum(spent))], chk_val(f"{D(bal)} - ({' + '.join(D(s) for s in spent)})"), tags=["modeling"])


@fam("2")
def s2_missing(r, L):
    a = rfrac(r, [3, 4, 5, 6])
    x = rfrac(r, [2, 3, 5, 7])
    op = pick(r, ["*", "+", "/"])
    if op == "*":
        rhs = a * x
        eq = f"({N(a)})n = {N(rhs)}"
        wrong = [N(rhs * a), N(-x), N(rhs - a)]
    elif op == "+":
        rhs = a + x
        eq = f"n + {ptxt(a)} = {N(rhs)}"
        wrong = [N(rhs + a), N(-x), N(a - rhs)]
    else:
        need(x != 0)
        rhs = x / a
        eq = f"n ÷ {ptxt(a)} = {N(rhs)}"
        wrong = [N(rhs / a), N(-x), N(rhs + a)]
    return P(f"Find the rational number n that makes the equation true: {eq}", N(x),
             ["Undo the operation with its inverse.", f"n = {N(x)}.", "Check by substituting into the original equation."],
             wrong, {"kind": "eq", "eq": eq, "var": "n"}, tags=["reasoning"])


@fam("1")
def s2_open_sign(r, L):
    a, b = rfrac(r, [2, 3, 4, 5]), rfrac(r, [2, 3, 4, 5])
    need(a < 0 or b < 0)
    v = a * b
    return P(f"Without computing, is the product ({N(a)})({N(b)}) positive, negative, or zero?", "positive" if v > 0 else "negative",
             ["Count the negative factors: an even number gives a positive product, an odd number a negative product."],
             ["negative" if v > 0 else "positive", "zero", "cannot be determined"],
             chk_py("sign_of", expr=f"({N(a)})({N(b)})"), tags=["reasoning"])


@fam("012")
def s2_error(r, L):
    a, b = F(r.randint(1, 5), pick(r, [3, 4, 5])), F(r.randint(1, 5), pick(r, [6, 7, 8, 9]))
    need(a.denominator != b.denominator and a.denominator != 1 and b.denominator != 1)
    wrongv = F(-a.numerator - b.numerator, a.denominator + b.denominator)
    v = -a - b
    return P(f"Casey evaluated -{N(a)} - {N(b)} this way: \"-{a.numerator} - {b.numerator} = -{a.numerator + b.numerator} and {a.denominator} + {b.denominator} = {a.denominator + b.denominator}, so the answer is {N(wrongv)}.\" What is the correct value?",
             N(v), ["Casey added the denominators; fractions must have a common denominator before adding numerators.",
                    f"-{N(a)} - {N(b)} = {N(-a)} + ({N(-b)}) = {N(v)}."],
             [N(wrongv), N(-a + b), N(a + b)], chk_val(f"-{N(a)} - {N(b)}"), tags=["error-analysis", "misconception"])


@fam("012")
def s2_open(r, L):
    t = [r.randint(-6, 3) + F(r.randint(-9, 9), 10) for _ in range(4)]
    need(len(set(t)) == 4)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
    tot = sum(t)
    mean = tot / 4
    need(is_term(mean))
    hi, lo = max(t), min(t)
    return P("The low temperatures (°C) for four days were: " + ", ".join(f"{d} {D(x)}" for d, x in zip(days, t)) + ".", None,
             [f"Range: {D(hi)} - ({D(lo)}) = {D(hi - lo)}.", f"Sum: {D(tot)}.", f"Mean: {D(tot)} ÷ 4 = {D(mean)}.", f"Change: {D(t[3])} - ({D(t[0])}) = {D(t[3] - t[0])}."],
             parts=[("Find the difference between the highest and lowest temperatures.", f"{D(hi - lo)}°C", chk_val(f"{D(hi)} - ({D(lo)})")),
                    ("Find the sum of the four temperatures.", f"{D(tot)}°C", chk_val(" + ".join(f"({D(x)})" for x in t))),
                    ("Find the mean temperature.", f"{D(mean)}°C", chk_val("(" + " + ".join(f"({D(x)})" for x in t) + ")/4")),
                    ("Find the change from Monday to Thursday.", f"{D(t[3] - t[0])}°C", chk_val(f"{D(t[3])} - ({D(t[0])})"))],
             tags=["modeling", "multistep"])


# ======================================================================= S3 Converting fractions and decimals
@fam("01")
def s3_frac_to_term(r, L):
    d = pick(r, [2, 4, 5, 8, 20, 25] if L == 0 else [8, 16, 40, 125, 50, 32])
    n = r.randint(1, 3 * d)
    x = F(n, d)
    need(x.denominator == d and x.denominator != 1)
    neg = L == 1 and r.random() < 0.4
    x = -x if neg else x
    shown = N(x) if L == 0 or r.random() < 0.6 or abs(x) < 1 else ("-" if neg else "") + f"{abs(x.numerator) // d} {abs(x.numerator) % d}/{d}"
    need(not shown.endswith(" 0/" + str(d)))
    wrong = [D(F(d, abs(x.numerator)) * (-1 if neg else 1)) if is_term(F(d, abs(x.numerator))) else D(x * 10),
             f"{'-' if neg else ''}{abs(x.numerator)}.{d}", D(x / 10)]
    return P(f"Write {shown} as a decimal.", D(x), [f"Divide the numerator by the denominator: {abs(x.numerator)} ÷ {d} = {D(abs(x))}.",
                                                  f"So {shown} = {D(x)}."], wrong, chk_py("dec_text", expr=N(x)))


@fam("01")
def s3_dec_to_frac(r, L):
    places = pick(r, [1, 2]) if L == 0 else pick(r, [2, 3])
    k = r.randint(1, 10 ** places * (1 if L == 0 else 3))
    need(k % 10)
    x = F(k, 10 ** places) * (pick(r, [1, -1]) if L else 1)
    need(x.denominator != 1)
    wrong = [f"{'-' if x < 0 else ''}{k}/{10 ** (places + 1)}", N(F(10 ** places, k)), N(x * 10) if (x * 10).denominator != 1 else N(x + 1)]
    return P(f"Write {D(x)} as a fraction in simplest form{' (use an improper fraction)' if abs(x) > 1 else ''}.", N(x),
             [f"{D(abs(x))} = {k}/{10 ** places}.", f"Divide numerator and denominator by {math.gcd(k, 10 ** places)}: {N(abs(x))}."] + (["Keep the negative sign."] if x < 0 else []),
             wrong, chk_py("frac_text", expr=D(x)))


@fam("12")
def s3_frac_to_rep(r, L):
    d = pick(r, [3, 6, 9, 11, 12, 15] if L == 1 else [7, 11, 12, 13 if False else 27, 22, 33, 18])
    n = r.randint(1, 2 * d)
    x = F(n, d)
    need(not is_term(x) and x.denominator == d)
    neg = L == 2 and r.random() < 0.3
    x = -x if neg else x
    ans = rep_text(x)
    alt = rep_text(x + F(1, 100)) if not is_term(x + F(1, 100)) else D(x + F(1, 100))
    wrong = [D(x, 2), alt, rep_text(F(d, n)) if not is_term(F(d, n)) else D(F(d, n))]
    return P(f"Write {N(x)} as a decimal. If it repeats, state the repeating block.", ans,
             [f"Divide {abs(x.numerator)} by {d}. The remainders begin to repeat, so the digits repeat.", f"{N(x)} = {ans}."],
             wrong, chk_py("dec_text", expr=N(x)), tags=["misconception"])


@fam("12")
def s3_rep_to_frac(r, L):
    if L == 1:
        x = F(r.randint(1, 8), 9) + r.randint(0, 3)
    else:
        kind = pick(r, ["two", "delay"])
        if kind == "two":
            x = F(r.randint(10, 98), 99)
        else:
            x = F(r.randint(1, 9), 10) + F(r.randint(1, 8), 90)
    need(not is_term(x))
    shown = rep_text(x)
    blk = shown.split("(")[1].split(" ")[0]
    wrong = [N(F(int(blk), 10 ** len(blk)) + math.floor(x)), N(F(int(blk), 10 ** len(blk) - 1) / 10 + math.floor(x)) if L == 2 else N(F(int(blk), 10)), N(x + F(1, 9))]
    steps = [f"Let n = {shown}.", f"Multiply by a power of 10 so the repeating parts line up, then subtract to remove the repeating part.", f"n = {N(x)}."]
    return P(f"Write {shown} as a fraction in simplest form.", N(x), steps, wrong, chk_py("frac_text", expr=N(x)), tags=["reasoning"] if L == 2 else [])


@fam("012")
def s3_compare(r, L):
    f_ = rfrac(r, [3, 4, 6, 7, 8, 9] if L else [2, 4, 5, 8], neg=L == 2, proper=True)
    d = f_ + F(pick(r, [-3, -2, -1, 1, 2, 3]), 100 if L else 10)
    need(is_term(d) and d != f_)
    ds = D(d)
    ans = N(f_) if f_ > d else ds
    wrong = [ds if ans == N(f_) else N(f_), "They are equal.", "Cannot be determined"]
    return P(f"Which number is greater: {N(f_)} or {ds}?", ans, [f"{N(f_)} = {rep_text(f_)}.", f"Compare with {ds}: the greater is {ans}."],
             wrong, chk_py("extreme", items=[N(f_), ds], max=True), tags=["multiple-representations"])


@fam("2", mode="mc")
def s3_which_terminates(r, L):
    want = r.random() < 0.5
    good = [F(r.randint(1, 30), pick(r, [8, 16, 20, 25, 40, 80, 125]))] if want else [F(r.randint(1, 30), pick(r, [6, 12, 15, 30, 45, 21]))]
    need(good[0].denominator != 1 and is_term(good[0]) == want)
    bad = []
    while len(bad) < 3:
        x = F(r.randint(1, 30), pick(r, [6, 12, 15, 30, 45, 21, 14, 18, 24]) if want else pick(r, [8, 16, 20, 25, 40, 80, 125, 50]))
        if x.denominator != 1 and is_term(x) != want and x not in bad:
            bad.append(x)
    q = "Which fraction has a terminating decimal form?" if want else "Which fraction has a repeating (non-terminating) decimal form?"
    opts = [(f"{x.numerator}/{x.denominator}", x == good[0]) for x in bad + good]
    r.shuffle(opts)
    return P(q, f"{good[0].numerator}/{good[0].denominator}",
             ["Write each fraction in simplest form and factor the denominator.",
              "A fraction in simplest form terminates exactly when its denominator has no prime factors other than 2 and 5.",
              f"{N(good[0])}: denominator {good[0].denominator} = {'·'.join(map(str, pf(good[0].denominator)))}."],
             options=opts, chk=chk_py("terminates", want=want), tags=["reasoning"], mode="mc")


def pf(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out or [1]


@fam("012")
def s3_context(r, L):
    nm = pick(r, NAMES)
    k = pick(r, ["inch", "cup", "score"])
    if k == "inch":
        x = F(r.randint(1, 15), 16) + r.randint(0, 3)
        need(x.denominator in (4, 8, 16))
        return P(f"{nm} measured a board as {N(x) if x < 1 else f'{x.numerator // x.denominator} {x.numerator % x.denominator}/{x.denominator}'} inches. A digital caliper shows decimals. What decimal should it show?",
                 f"{D(x)} inches", [f"{x.numerator % x.denominator}/{x.denominator} = {D(F(x.numerator % x.denominator, x.denominator))}.", f"Total: {D(x)} inches."],
                 [f"{x.numerator % x.denominator}.{x.denominator} inches", f"{D(x / 10)} inches", f"{D(F(x.denominator, 100) + x.numerator // x.denominator)} inches"],
                 chk_py("dec_text", expr=N(x)), tags=["modeling"])
    if k == "cup":
        dec = pick(r, [F(1, 4), F(3, 4), F(5, 8), F(3, 8), F(1, 8)]) + r.randint(0, 2)
        return P(f"A scale shows {D(dec)} cups of rice. Write this amount as a fraction or improper fraction in simplest form.", f"{N(dec)} cups",
                 [f"{D(dec)} = {N(dec)}."], [f"{N(dec * 10)} cups", f"{N(1 / dec)} cups", f"{N(dec + F(1, 10))} cups"], chk_py("frac_text", expr=D(dec)), tags=["modeling"])
    made, tries = r.randint(5, 20), pick(r, [24, 30, 36, 40, 45])
    need(made < tries)
    x = F(made, tries)
    ans = rep_text(x) if not is_term(x) else D(x)
    return P(f"{nm} made {made} of {tries} free throws. Write the fraction made as a decimal{'' if is_term(x) else ' (show the repeating block)'}.",
             ans, [f"{made}/{tries} = {N(x)}.", f"{N(x)} = {ans}."], [D(F(tries, made), 3), f"0.{made}", D(x, 1)], chk_py("dec_text", expr=f"{made}/{tries}"), tags=["modeling"])


@fam("012")
def s3_select(r, L):
    target = F(r.randint(1, 7), pick(r, [4, 5, 8]))
    need(target.denominator != 1)
    good = [N(target), D(target), N(target * 3).replace("/", "/") if False else f"{target.numerator * 3}/{target.denominator * 3}"]
    bad = [D(target / 10), f"{target.numerator}.{target.denominator}", N(target + F(1, 100)) if L else D(target + F(1, 10))]
    opts = [(g, True) for g in good] + [(b, False) for b in bad]
    return P(f"Select ALL values equal to {D(target)}.", None, [f"{D(target)} = {N(target)} = {good[2]}.", "The others have different values."],
             options=opts, chk=chk_py("rep_dec", expr=D(target)), tags=["multiple-representations"])


@fam("12")
def s3_open(r, L):
    x = F(r.randint(1, 9), 10) + F(r.randint(1, 8), 90)
    need(not is_term(x))
    shown = rep_text(x)
    t10, t100 = x * 10, x * 100
    return P(f"Follow the steps to write n = {shown} as a fraction.", None,
             ["Multiplying by 10 moves the nonrepeating digit left of the decimal point.", "Multiplying by 100 moves one repeating digit as well.",
              "The repeating parts cancel when subtracting.", f"Simplify: {N(x)}."],
             parts=[("What is 10n written as a decimal?", rep_text(t10), chk_py("dec_text", expr=f"10*({N(x)})")),
                    ("What is 100n written as a decimal?", rep_text(t100), chk_py("dec_text", expr=f"100*({N(x)})")),
                    ("Subtract: what is 100n - 10n?", D(t100 - t10), chk_val(f"90*({N(x)})")),
                    ("Solve for n and write it in simplest form.", N(x), chk_py("frac_text", expr=N(x)))],
             tags=["reasoning", "multistep"])


# ======================================================================= S4 Identifying irrational numbers
NONSQ = [2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 32, 40, 45, 50, 60, 72, 80, 90, 99]
SQ = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]


def rat_pool(r, L):
    pool = [f"√{pick(r, SQ)}", rep_text(F(r.randint(1, 10), pick(r, [3, 9, 11]))), N(rfrac(r)), D(F(r.randint(-999, 999), 100)),
            f"-√{pick(r, SQ[1:])}", f"√({pick(r, [4, 9, 16, 25])}/{pick(r, [49, 81, 121])})", f"∛{pick(r, [8, 27, 64, 125])}"]
    if L == 2:
        a = pick(r, [2, 3, 7])
        pool.append(f"√{a} · √{a}")
    return [p for p in pool if p not in ("0", "-0")]


def irr_pool(r, L):
    pool = [f"√{pick(r, NONSQ)}", "π", f"{r.randint(0, 5)}.{pick(r, ['1010010001', '1213141516', '1234567891'])}… (pattern never repeats)",
            f"-√{pick(r, NONSQ)}", f"{r.randint(2, 9)} + √{pick(r, NONSQ)}", f"{r.randint(2, 6)}π"]
    if L:
        pool.append(f"∛{pick(r, [2, 4, 9, 10, 20])}")
    return pool


@fam("012", mode="sa")
def s4_classify(r, L):
    rp, ip = rat_pool(r, L), irr_pool(r, L)
    num = pick(r, rp + ip)
    ans = "rational" if num in rp else "irrational"
    why = {"rational": "It can be written as a ratio of two integers (its decimal terminates or repeats).",
           "irrational": "It cannot be written as a ratio of two integers; its decimal never terminates or repeats."}[ans]
    return P(f"Is {num} rational or irrational?", ans, [why], ["irrational" if ans == "rational" else "rational"],
             chk_py("rat_or_irr", num=num), tags=["reasoning"], mode="sa")


@fam("012", mode="mc")
def s4_which(r, L):
    want_irr = r.random() < 0.6
    if want_irr:
        good = pick(r, irr_pool(r, L))
        bad = pick(r, rat_pool(r, L), 3)
    else:
        good = pick(r, rat_pool(r, L))
        bad = pick(r, irr_pool(r, L), 3)
    need(len({good, *bad}) == 4)
    opts = [(b, False) for b in bad] + [(good, True)]
    r.shuffle(opts)
    return P(f"Which number is {'irrational' if want_irr else 'rational'}?", good,
             [f"{good} is {'irrational' if want_irr else 'rational'}.", "Perfect-square roots, fractions, terminating decimals and repeating decimals are rational; non-perfect-square roots, π and non-repeating non-terminating decimals are irrational."],
             options=opts, chk=chk_py("is_irrational" if want_irr else "is_rational"), tags=["reasoning"], mode="mc")


@fam("12", mode="sa")
def s4_perfect_between(r, L):
    n = pick(r, NONSQ + [s + 1 for s in SQ[2:]])
    lo = math.isqrt(n)
    need(lo * lo != n)
    return P(f"√{n} is irrational. Between which two consecutive whole numbers does it lie?", f"{lo} and {lo + 1}",
             [f"{lo}² = {lo * lo} and {lo + 1}² = {(lo + 1) ** 2}.", f"{lo * lo} < {n} < {(lo + 1) ** 2}, so {lo} < √{n} < {lo + 1}."],
             [f"{lo - 1} and {lo}", f"{lo + 1} and {lo + 2}", f"{n // 2} and {n // 2 + 1}"], chk_py("between_ints", num=f"√{n}"), mode="any")


@fam("12")
def s4_count_irr(r, L):
    rs, irs = pick(r, rat_pool(r, L), r.randint(2, 4)), pick(r, irr_pool(r, L), r.randint(1, 3))
    nums = rs + irs
    r.shuffle(nums)
    need(len(set(nums)) == len(nums))
    c = len(irs)
    return P("How many of these numbers are irrational? " + "; ".join(nums), str(c),
             [f"{x}: {'irrational' if x in irs else 'rational'}." for x in nums], [str(c + 1), str(c - 1), str(len(nums) - c)],
             chk_py("count_irr", items=nums), tags=["reasoning"])


@fam("2", mode="mc")
def s4_side_length(r, L):
    a = pick(r, [n for n in range(2, 60) if math.isqrt(n) ** 2 != n])
    b = pick(r, SQ[2:12])
    opts = [(f"A square with area {a} square units", True), (f"A square with area {b} square units", False),
            (f"A square with perimeter {4 * a} units", False), (f"A square with area {4 * b} square units", False)]
    r.shuffle(opts)
    return P("For which square is the side length an irrational number?", f"A square with area {a} square units",
             [f"Side = √(area). √{a} is irrational because {a} is not a perfect square.", f"√{b} = {math.isqrt(b)}, √{4 * b} = {math.isqrt(4 * b)}, and perimeter {4 * a} gives side {a}."],
             options=opts, chk=chk_py("square_side_irr"), tags=["reasoning", "connections"], mode="mc")


@fam("012")
def s4_select(r, L):
    rats = pick(r, rat_pool(r, L), 3)
    irrs = pick(r, irr_pool(r, L), 3 if L else 2)
    need(len(set(rats + irrs)) == len(rats + irrs))
    opts = [(x, False) for x in rats] + [(x, True) for x in irrs]
    return P("Select ALL irrational numbers.", None, ["Irrational numbers cannot be written as a ratio of integers."] + [f"{x}: {'irrational' if c else 'rational'}." for x, c in opts],
             options=opts, chk=chk_py("is_irrational"), tags=["reasoning"])


@fam("012")
def s4_error(r, L):
    n = pick(r, NONSQ)
    m = pick(r, SQ[2:])
    opts = [(f"No. {n} is not a perfect square, so √{n} is irrational.", True), (f"Yes. Any square root of a whole number is rational.", False),
            (f"Yes. √{n} can be written as a fraction with denominator 1.", False), (f"No. All square roots are irrational.", False)]
    r.shuffle(opts)
    return P(f"Riley says √{n} is rational because {n} is a whole number. Is Riley correct?", opts[[c for _, c in opts].index(True)][0],
             [f"√{n} ≈ {D(F(repr(math.sqrt(n))), 3)}; its decimal never ends or repeats.", f"A counterexample to \"all square roots are irrational\": √{m} = {math.isqrt(m)}.",
              "Putting √n over a denominator of 1 does not make a ratio of two integers, because √n itself is not an integer."],
             options=opts, chk={"kind": "text", "accept": [f"No. {n} is not a perfect square, so √{n} is irrational."]}, tags=["error-analysis", "misconception"], mode="mc")


@fam("012")
def s4_open(r, L):
    a, b, c, d = pick(r, SQ[2:]), pick(r, NONSQ), F(r.randint(1, 8), 9), r.randint(1, 4)
    parts = [(f"Is √{a} rational or irrational?", "rational", chk_py("rat_or_irr", num=f"√{a}")),
             (f"Is √{b} rational or irrational?", "irrational", chk_py("rat_or_irr", num=f"√{b}")),
             (f"Is {rep_text(c)} rational or irrational?", "rational", chk_py("rat_or_irr", num=rep_text(c))),
             (f"Is {d}π rational or irrational?", "irrational", chk_py("rat_or_irr", num=f"{d}π"))]
    return P("Classify each number as rational or irrational.", None,
             [f"√{a} = {math.isqrt(a)}.", f"{b} is not a perfect square.", "A repeating decimal is rational.", "A nonzero rational multiple of π is irrational."],
             parts=parts, tags=["reasoning"])


# ======================================================================= S5 Properties of irrational numbers
ASN = ["always rational", "always irrational", "sometimes rational and sometimes irrational"]


@fam("012", mode="sa")
def s5_result_type(r, L):
    n = pick(r, [2, 3, 5, 6, 7, 10, 11])
    a, b = r.randint(2, 9), r.randint(2, 9)
    exprs = [(f"{a} + √{n}", "irrational"), (f"{a}√{n}", "irrational"), (f"√{n} · √{n}", "rational"), (f"(√{n})²", "rational"), (f"{a}π", "irrational")]
    if L:
        exprs += [(f"√{n} - √{n}", "rational"), (f"√{n} · √{n * a * a}", "rational"), (f"√{n * b * b} ÷ √{n}", "rational"),
                  (f"{a}√{n} + {b}√{n}", "irrational"), (f"√{n} + {a}/{b}", "irrational")]
    e, ans = pick(r, exprs)
    return P(f"Is the value of {e} rational or irrational?", ans,
             [f"Simplify or reason about {e}.", f"The value is {ans}."], ["irrational" if ans == "rational" else "rational"],
             chk_py("rat_or_irr", num=e), tags=["reasoning"], mode="sa")


STMTS = [("the sum of two rational numbers", 0), ("the product of two rational numbers", 0),
         ("the sum of a rational number and an irrational number", 1), ("the product of a nonzero rational number and an irrational number", 1),
         ("the sum of two irrational numbers", 2), ("the product of two irrational numbers", 2), ("the difference of two irrational numbers", 2),
         ("the quotient of two nonzero rational numbers", 0)]


@fam("12", mode="mc")
def s5_always(r, L):
    s, k = pick(r, STMTS)
    opts = [(x, i == k) for i, x in enumerate(ASN)] + [("never a real number", False)]
    ex = {0: "Rational numbers are closed under these operations.", 1: f"Example: 3 + √2 and 3√2 are irrational; if the result were rational, solving for the irrational number would make it rational.",
          2: "√2 · √2 = 2 is rational, but √2 · √3 = √6 is irrational; √2 + (-√2) = 0, but √2 + √2 = 2√2."}[k]
    return P(f"Complete the statement: {s[0].upper() + s[1:]} is ___.", ASN[k], [ex], options=opts,
             chk={"kind": "text", "accept": [ASN[k]]}, tags=["reasoning"], mode="mc")


@fam("12", mode="mc")
def s5_counterexample(r, L):
    op = pick(r, ["product", "sum"])
    n = pick(r, [2, 3, 5, 7])
    k = pick(r, [2, 3])
    if op == "product":
        good = f"√{n} · √{n * k * k}"
        bad = [f"√{n} · √{n + 1}", f"{k} · √{n}", f"√{n} + √{n}"]
        claim = "the product of two irrational numbers can be rational"
    else:
        good = f"(√{n} + {k}) + (-√{n})"
        bad = [f"√{n} + √{n}", f"√{n} + {k}", f"√{n} · √{n + 1}"]
        claim = "the sum of two irrational numbers can be rational"
    opts = [(b, False) for b in bad] + [(good, True)]
    r.shuffle(opts)
    return P(f"Which example shows that {claim}?", good,
             [f"{good}: both numbers are irrational and the result simplifies to a rational number.", "The other choices either use a rational number or give an irrational result."],
             options=opts, chk=chk_py("irr_counterexample", op=op), tags=["reasoning", "challenge"], mode="mc")


@fam("012")
def s5_simplify(r, L):
    n = pick(r, [2, 3, 5, 6, 7])
    a, b = r.randint(2, 6), r.randint(2, 6)
    forms = [(f"√{n} · √{n}", F(n)), (f"(√{n * a * a})²", F(n * a * a)), (f"√{n * a * a} · √{n}", F(a * n)), (f"√{a * a * n} ÷ √{n}", F(a))] if L < 2 else \
            [(f"({a}√{n})²", F(a * a * n)), (f"(√{n} + {a})(√{n} - {a})", F(n - a * a)), (f"{a}√{n} · {b}√{n}", F(a * b * n)), (f"(√{n * b * b} ÷ √{n})²", F(b * b))]
    e, v = pick(r, forms)
    wrong = [N(v * 2), f"√{n * 2}" if L == 0 else N(v + 2 * a), N(-v)]
    return P(f"Simplify: {e}", N(v), [f"Use √m · √m = m and √m · √k = √(mk).", f"{e} = {N(v)}."], wrong, chk_val(e), tags=["connections"])


@fam("012", mode="mc")
def s5_irrational_between(r, L):
    lo = r.randint(2, 9)
    hi = lo + 1
    good = pick(r, [f"√{n}" for n in range(lo * lo + 1, hi * hi) if math.isqrt(n) ** 2 != n])
    bad = [f"√{(hi + 1) ** 2 - 2}", f"√{lo * lo}", f"{lo}.5", f"√{hi * hi + 3}", f"{hi}π"]
    r.shuffle(bad)
    bad = bad[:3]
    need(len(bad) == 3)
    opts = [(b, False) for b in bad] + [(good, True)]
    r.shuffle(opts)
    return P(f"Which number is irrational AND between {lo} and {hi}?", good,
             [f"{lo}² = {lo * lo} and {hi}² = {hi * hi}, so √n is between {lo} and {hi} when {lo * lo} < n < {hi * hi}.", f"{good} qualifies and is not a perfect square root."],
             options=opts, chk=chk_py("strictly_between", lo=str(lo), hi=str(hi), irrational=True), tags=["reasoning"], mode="mc")


@fam("2")
def s5_solve_for(r, L):
    n = pick(r, [2, 3, 5, 7])
    k = r.randint(2, 5)
    e = f"√{n} · x = {k * n}"
    return P(f"What value of x makes {e} true? Is x rational or irrational?", f"x = {k}√{n}, irrational",
             [f"x = {k * n} ÷ √{n} = {k * n}√{n} ÷ {n} = {k}√{n}.", f"{k}√{n} is a nonzero rational number times an irrational number, so it is irrational."],
             [f"x = {k}, rational", f"x = {k * n}√{n}, irrational", f"x = {k}√{n}, rational"], chk_py("value_and_type", expr=f"{k * n} ÷ √{n}"), tags=["challenge"])


@fam("012")
def s5_select(r, L):
    n = pick(r, [2, 3, 5, 7])
    k = r.randint(2, 4)
    rat = [f"√{n} · √{n}", f"√{n * k * k} ÷ √{n}", f"(√{n} + {k}) - √{n}", f"(√{n * k * k})²"]
    irr = [f"{k} + √{n}", f"{k}√{n}", f"√{n} + √{n}", f"√{n} · √{n + 1}" if n + 1 not in (4, 8) else f"√{n} · √{n + 3}", f"{k}π"]
    a, b = pick(r, rat, 3), pick(r, irr, 3)
    opts = [(x, True) for x in a] + [(x, False) for x in b]
    return P("Select ALL expressions whose value is rational.", None, [f"{x}: {'rational' if c else 'irrational'}." for x, c in opts],
             options=opts, chk=chk_py("is_rational"), tags=["reasoning"])


@fam("012")
def s5_open(r, L):
    n = pick(r, [2, 3, 5, 6, 7])
    a = r.randint(2, 6)
    parts = [(f"Is {a} + √{n} rational or irrational?", "irrational", chk_py("rat_or_irr", num=f"{a} + √{n}")),
             (f"Is {a}√{n} rational or irrational?", "irrational", chk_py("rat_or_irr", num=f"{a}√{n}")),
             (f"Is √{n} · √{n} rational or irrational?", "rational", chk_py("rat_or_irr", num=f"√{n} · √{n}")),
             (f"Is √{n} + (-√{n}) rational or irrational?", "rational", chk_py("rat_or_irr", num=f"√{n} + (-√{n})"))]
    return P(f"Use √{n} (an irrational number) to answer each part.", None,
             ["Rational plus irrational is irrational.", "A nonzero rational times an irrational is irrational.", f"√{n} · √{n} = {n}.", "Opposites add to 0."],
             parts=parts, tags=["reasoning"])


# ======================================================================= S6 Comparing and ordering irrational numbers
@fam("012")
def s6_compare(r, L):
    n = pick(r, NONSQ[:20] + [40, 50, 60, 70, 80, 90])
    s = math.sqrt(n)
    if L == 0:
        other = F(math.floor(s * 10) + pick(r, [-2, -1, 1, 2]), 10)
    elif L == 1:
        other = F(round(s * 4) + pick(r, [-1, 1]), 4)
    else:
        m = n + pick(r, [-3, -2, 2, 3])
        need(m > 1)
        a = pick(r, [2, 3])
        need(n % (a * a) != 0)
        left, right = f"{a}√{n}", f"√{a * a * n + pick(r, [-5, 5])}"
        lv, rv = a * s, math.sqrt(a * a * n + (int(right[1:]) - a * a * n))
        ans = left if lv > rv else right
        return P(f"Which is greater: {left} or {right}?", ans,
                 [f"Write {left} as one square root: {a}√{n} = √({a * a} · {n}) = √{a * a * n}.", f"Compare √{a * a * n} with {right}: the larger radicand gives the larger value."],
                 [right if ans == left else left, "They are equal.", "Cannot be determined without a calculator"], chk_py("extreme", items=[left, right], max=True), tags=["reasoning"])
    os_ = D(other) if L == 0 else N(other)
    need(abs(float(other) - s) > 0.02)
    ans = f"√{n}" if s > other else os_
    return P(f"Which is greater: √{n} or {os_}?", ans,
             [f"Square both: (√{n})² = {n} and ({os_})² = {N(other * other) if L else D(other * other)}.", f"The greater square belongs to the greater positive number: {ans}."],
             [os_ if ans != os_ else f"√{n}", "They are equal.", "Cannot be determined"], chk_py("extreme", items=[f"√{n}", os_], max=True))


@fam("012")
def s6_order(r, L):
    for _ in range(60):
        ns = pick(r, NONSQ[:22], 2)
        items = [f"√{ns[0]}", f"√{ns[1]}", D(F(r.randint(10, 60), 10)), "π" if L else N(F(r.randint(5, 30), 4))]
        if L == 2:
            items[2] = f"{pick(r, [2, 3])}√{pick(r, [2, 3, 5])}"
            items.append(rep_text(F(r.randint(10, 50), 9)))
        vals = [fval(t) for t in items]
        if len({round(v, 3) for v in vals}) == len(vals) and min(abs(a - b) for i, a in enumerate(vals) for b in vals[i + 1:]) > 0.04 and len(set(items)) == len(items):
            break
    else:
        raise Reject()
    srt = [t for _, t in sorted(zip(vals, items))]
    shown = items[:]
    r.shuffle(shown)
    need(shown != srt)
    ans = ", ".join(srt)
    wrong = [", ".join(srt[::-1]), ", ".join(sorted(items, key=lambda t: (len(t), t))), ", ".join(srt[1:2] + srt[:1] + srt[2:])]
    return P("Order from least to greatest: " + "; ".join(shown) + ".", ans,
             ["Approximate each value: " + "; ".join(f"{t} ≈ {D(F(repr(v)), 2)}" for t, v in zip(items, vals)) + ".", f"Least to greatest: {ans}."],
             wrong, chk_py("order", items=items), tags=["multiple-representations"])


def numline_draw(points, lo, hi, step=1):
    def draw(path):
        fig, ax = new_fig(7, 1.9)
        ax.plot([lo - 0.3, hi + 0.3], [0, 0], color="black", lw=1.5)
        ax.annotate("", xy=(hi + 0.45, 0), xytext=(hi + 0.3, 0), arrowprops=dict(arrowstyle="-|>", color="black"))
        ax.annotate("", xy=(lo - 0.45, 0), xytext=(lo - 0.3, 0), arrowprops=dict(arrowstyle="-|>", color="black"))
        v = lo
        while v <= hi + 1e-9:
            ax.plot([v, v], [-0.12, 0.12], color="black", lw=1.2)
            ax.text(v, -0.3, D(F(v).limit_denominator(100)) if v != int(v) else str(int(v)), ha="center", va="top", fontsize=12)
            v += step
        sub = step / 10
        v = lo
        while v <= hi + 1e-9:
            ax.plot([v, v], [-0.06, 0.06], color="black", lw=0.6)
            v += sub
        for lab, x in points:
            ax.plot([x], [0], "o", color="#1f4e9c", ms=8)
            ax.text(x, 0.3, lab, ha="center", va="bottom", fontsize=14, fontweight="bold")
        ax.set_xlim(lo - 0.6, hi + 0.6)
        ax.set_ylim(-0.8, 0.8)
        ax.axis("off")
        save(fig, path)
    return draw


@fam("012", mode="mc")
def s6_numberline(r, L):
    lo = r.randint(1, 7)
    hi = lo + 2
    n = pick(r, [k for k in range(lo * lo + 1, hi * hi) if math.isqrt(k) ** 2 != k])
    s = math.sqrt(n)
    others = []
    cands = [lo + 0.15, lo + 0.5, lo + 0.85, lo + 1.15, lo + 1.5, lo + 1.85]
    r.shuffle(cands)
    for c in cands:
        if abs(c - s) > 0.22 and all(abs(c - o) > 0.22 for o in others):
            others.append(c)
        if len(others) == 3:
            break
    need(len(others) == 3)
    pts = sorted(others + [s])
    labels = "ABCD"
    lab = labels[pts.index(s)]
    plist = [(labels[i], p) for i, p in enumerate(pts)]
    alt = f"Number line from {lo} to {hi} with tick marks every 0.1. Points " + ", ".join(f"{l} at about {D(F(repr(p)), 2)}" for l, p in plist) + "."
    opts = [(f"Point {l}", l == lab) for l in labels]
    return P(f"Which point on the number line best represents √{n}?", f"Point {lab}",
             [f"{math.isqrt(n)}² = {math.isqrt(n) ** 2} and {math.isqrt(n) + 1}² = {(math.isqrt(n) + 1) ** 2}, so √{n} is between {math.isqrt(n)} and {math.isqrt(n) + 1}.",
              f"√{n} ≈ {D(F(repr(s)), 2)}, which is point {lab}."],
             options=opts, chk=chk_py("numline_point", n=n, pts={l: p for l, p in plist}),
             diagram={"draw": numline_draw(plist, lo, hi), "alt": alt}, tags=["graph", "multiple-representations"], mode="mc")


@fam("12")
def s6_count_between(r, L):
    a = pick(r, NONSQ[:15])
    b = pick(r, [k for k in range(a + 15, 160) if math.isqrt(k) ** 2 != k])
    c = sum(1 for k in range(0, 20) if math.sqrt(a) < k < math.sqrt(b))
    return P(f"How many whole numbers are between √{a} and √{b}?", str(c),
             [f"√{a} is between {math.isqrt(a)} and {math.isqrt(a) + 1}; √{b} is between {math.isqrt(b)} and {math.isqrt(b) + 1}.",
              f"The whole numbers from {math.isqrt(a) + 1} to {math.isqrt(b)} are between them: {c} numbers."],
             [str(c + 1), str(c - 1), str(b - a - 1)], chk_py("count_whole_between", a=a, b=b), tags=["reasoning"])


@fam("2")
def s6_greatest_n(r, L):
    t = F(r.randint(31, 99), 10)
    need(t.denominator != 1)
    nmax = math.ceil(t * t) - 1
    return P(f"What is the greatest whole number n such that √n < {D(t)}?", str(nmax),
             [f"Square both sides (both positive): n < {D(t)}² = {D(t * t)}.", f"The greatest whole number less than {D(t * t)} is {nmax}."],
             [str(nmax + 1), str(math.floor(t) ** 2), str(int(t * 2))], chk_py("greatest_n_sqrt_lt", t=D(t)), tags=["reasoning", "challenge"])


@fam("012")
def s6_select(r, L):
    n = pick(r, [20, 30, 40, 50, 60, 70, 80])
    s = math.sqrt(n)
    cand = [f"√{n + 3}", D(F(math.floor(s * 10) + 2, 10)), f"{math.ceil(s)}", f"√{n - 5}", D(F(math.floor(s * 10) - 1, 10)), f"{math.floor(s)}.5" if math.floor(s) + 0.5 < s else f"{math.floor(s)}"]
    opts = [(c, fval(c) > s) for c in cand]
    need(sum(c for _, c in opts) >= 2 and sum(not c for _, c in opts) >= 1 and len(set(cand)) == 6)
    return P(f"Select ALL numbers greater than √{n}.", None, [f"√{n} ≈ {D(F(repr(s)), 3)}."] + [f"{t} ≈ {D(F(repr(fval(t))), 3)}." for t, _ in opts],
             options=opts, chk=chk_py("predicate", op="gt", than=f"√{n}"))


@fam("012")
def s6_open(r, L):
    n = pick(r, [k for k in range(10, 90) if math.isqrt(k) ** 2 != k])
    lo = math.isqrt(n)
    s = math.sqrt(n)
    t = Rd(s, 1)
    parts = [(f"Between which two consecutive whole numbers is √{n}?", f"{lo} and {lo + 1}", chk_py("between_ints", num=f"√{n}")),
             (f"Is √{n} closer to {lo} or to {lo + 1}?", str(lo if s - lo < lo + 1 - s else lo + 1), chk_py("closer_int", n=n)),
             (f"Estimate √{n} to the nearest tenth.", t, {"kind": "approx", "expr": f"√{n}", "places": 1}),
             (f"Order from least to greatest: √{n}, {lo}.5, {t}.", None, None)]
    trio = [f"√{n}", f"{lo}.5", t]
    need(len({round(fval(x), 6) for x in trio}) == 3)
    srt = ", ".join(x for _, x in sorted((fval(x), x) for x in trio))
    parts[3] = (parts[3][0], srt, chk_py("order", items=trio))
    return P(f"Use estimation to compare √{n} with other numbers.", None,
             [f"{lo}² = {lo * lo} < {n} < {(lo + 1) ** 2} = {lo + 1}².", f"{n} is closer to {lo * lo if n - lo * lo < (lo + 1) ** 2 - n else (lo + 1) ** 2}.",
              f"√{n} ≈ {D(F(repr(s)), 3)} ≈ {t}.", f"Order: {srt}."], parts=parts, tags=["multistep"])


# ======================================================================= S7 Evaluating and approximating roots
@fam("012")
def s7_evaluate(r, L):
    forms = [("sq", pick(r, SQ)), ("cb", pick(r, [8, 27, 64, 125, 1000]))] if L == 0 else \
            [("sqf", (pick(r, [1, 4, 9, 16, 25, 36, 49]), pick(r, [4, 9, 25, 49, 64, 81, 100]))), ("cbneg", pick(r, [8, 27, 64, 125, 216, 343])),
             ("sqdec", pick(r, [F(4, 100), F(9, 100), F(16, 100), F(25, 100), F(49, 100), F(81, 100), F(144, 100)]))] if L == 1 else \
            [("cbf", (pick(r, [1, 8, 27, 64]), pick(r, [125, 216, 343, 1000]))), ("mix", (pick(r, SQ[1:8]), pick(r, [8, 27, 64, 125]))), ("sqdec", pick(r, [F(1, 10000) * k * k for k in (12, 15, 25, 3)]))]
    k, v = pick(r, forms)
    if k == "sq":
        e, val, wrong = f"√{v}", F(math.isqrt(v)), [str(v // 2), str(v * v), str(-math.isqrt(v))]
    elif k == "cb":
        c = round(v ** (1 / 3))
        e, val, wrong = f"∛{v}", F(c), [str(v // 3), str(c * c), str(math.isqrt(v)) if math.isqrt(v) ** 2 == v else str(c + 1)]
    elif k == "sqf":
        e, val = f"√({v[0]}/{v[1]})", F(math.isqrt(v[0]), math.isqrt(v[1]))
        need(val.denominator != 1)
        wrong = [N(F(v[0], 2 * v[1]) if v[0] % 2 == 0 else F(v[0], v[1])), N(1 / val), N(val * val)]
    elif k == "cbneg":
        c = round(v ** (1 / 3))
        e, val, wrong = f"∛(-{v})", F(-c), [str(c), "undefined", str(-v // 3)]
    elif k == "sqdec":
        e, val = f"√{D(v)}", root_frac(v)
        wrong = [D(v / 2), D(val / 10), D(val * 10)]
    elif k == "cbf":
        e, val = f"∛({v[0]}/{v[1]})", F(round(v[0] ** (1 / 3)), round(v[1] ** (1 / 3)))
        wrong = [N(F(v[0], 3 * v[1]) if v[0] % 3 == 0 else F(v[0], v[1])), N(1 / val) if val else "0", N(val * val)]
    else:
        a, b = v
        e, val = f"√{a} + ∛{b}", F(math.isqrt(a) + round(b ** (1 / 3)))
        wrong = [str(math.isqrt(a + b)) if math.isqrt(a + b) ** 2 == a + b else str(a + b), str(math.isqrt(a) * round(b ** (1 / 3))), str(int(val) + 1)]
    wrong = [w for w in wrong if w != N(val)] + [str(int(val) + 2)]
    return P(f"Evaluate: {e}", D(val) if (k == "sqdec") else N(val),
             [f"{e} = {N(val) if k != 'sqdec' else D(val)} because {('(' + N(val) + ')') if val < 0 or val.denominator != 1 else N(val)}{'³' if 'cb' in k or k == 'mix' and False else '²' if k in ('sq', 'sqf', 'sqdec') else '³'} = {N(val ** (3 if k in ('cb', 'cbneg', 'cbf') else 2)) if k != 'mix' else '…'}." if k != "mix" else
              f"√{v[0]} = {math.isqrt(v[0])} and ∛{v[1]} = {round(v[1] ** (1 / 3))}; add: {N(val)}."],
             wrong, chk_val(e), tags=["misconception"] if k in ("cbneg", "sqdec") else [])


def root_frac(v):
    n, d = math.isqrt(v.numerator), math.isqrt(v.denominator)
    assert n * n == v.numerator and d * d == v.denominator
    return F(n, d)


@fam("01")
def s7_between(r, L):
    if L == 0 or r.random() < 0.5:
        n = pick(r, [k for k in range(5, 200) if math.isqrt(k) ** 2 != k])
        e, lo = f"√{n}", math.isqrt(n)
        why = f"{lo}² = {lo * lo} < {n} < {(lo + 1) ** 2} = {lo + 1}²."
    else:
        n = pick(r, [k for k in range(10, 900) if round(k ** (1 / 3)) ** 3 != k])
        lo = round(n ** (1 / 3))
        lo = lo if lo ** 3 < n else lo - 1
        e = f"∛{n}"
        why = f"{lo}³ = {lo ** 3} < {n} < {(lo + 1) ** 3} = {lo + 1}³."
    return P(f"Between which two consecutive whole numbers is {e}?", f"{lo} and {lo + 1}", [why],
             [f"{lo + 1} and {lo + 2}", f"{lo - 1} and {lo}", f"{n // 2} and {n // 2 + 1}" if n // 2 != lo else f"{lo + 2} and {lo + 3}"], chk_py("between_ints", num=e))


@fam("12")
def s7_approx(r, L):
    n = pick(r, [k for k in range(2, 150) if math.isqrt(k) ** 2 != k])
    places = 1 if L == 1 else pick(r, [1, 2])
    s = math.sqrt(n)
    ans = Rd(s, places)
    word = "tenth" if places == 1 else "hundredth"
    wrong = [Rd(s + 10 ** -places, places), Rd(n / 2, places), Rd(s - 10 ** -places, places)]
    return P(f"Approximate √{n} to the nearest {word}.", ans,
             [f"{math.isqrt(n)}² = {math.isqrt(n) ** 2} and {math.isqrt(n) + 1}² = {(math.isqrt(n) + 1) ** 2}.",
              f"Test decimals: {ans}² ≈ {Rd(float(ans) ** 2, 3)}; √{n} ≈ {Rd(s, 4)}, which rounds to {ans}."],
             wrong, {"kind": "approx", "expr": f"√{n}", "places": places})


@fam("012")
def s7_solve(r, L):
    if L == 0:
        k = r.randint(2, 15)
        eq, n, c = f"x² = {k * k}", 2, str(k * k)
        ans = f"x = {k} or x = -{k}"
        wrong = [f"x = {k}", f"x = {k * k // 2}" if k % 2 == 0 else f"x = {k * 2}", f"x = -{k}"]
    elif L == 1:
        if r.random() < 0.5:
            k = r.randint(2, 10)
            eq, n, c = f"x³ = {'-' if k % 2 else ''}{k ** 3}", 3, f"{'-' if k % 2 else ''}{k ** 3}"
            v = -k if k % 2 else k
            ans = f"x = {v}"
            wrong = [f"x = {-v}", f"x = {v} or x = {-v}", f"x = {k ** 3 // 3}" if k ** 3 % 3 == 0 else f"x = {k * 3}"]
        else:
            m = pick(r, NONSQ[:12])
            eq, n, c = f"x² = {m}", 2, str(m)
            ans = f"x = √{m} or x = -√{m}"
            wrong = [f"x = √{m}", f"x = {m // 2} or x = -{m // 2}", f"x = {m * m} or x = -{m * m}"]
    else:
        a = pick(r, [2, 3, 4, 5])
        k = r.randint(2, 9)
        b = r.randint(1, 20)
        if r.random() < 0.5:
            eq = f"{a}x² + {b} = {a * k * k + b}"
            n, c = 2, str(k * k)
            ans = f"x = {k} or x = -{k}"
            wrong = [f"x = {k}", f"x = {a * k * k} or x = -{a * k * k}", f"x = {k * k} or x = -{k * k}"]
        else:
            eq = f"x³ ÷ {a} = {N(F(-k ** 3, a))}" if (k ** 3) % a else f"{a}x³ = -{a * k ** 3}"
            n, c = 3, str(-k ** 3)
            ans = f"x = -{k}"
            wrong = [f"x = {k}", f"x = {k} or x = -{k}", f"x = -{k * a}"]
    return P(f"Solve: {eq}", ans, [f"Isolate the power, then take the {'square' if n == 2 else 'cube'} root.",
                                   "A positive number has two square roots (±); a number has exactly one real cube root." if n == 2 else "A cube root keeps the sign of the number.",
                                   ans + "."], wrong, chk_py("pm_sol", n=n, c=c), tags=["misconception"])


@fam("012")
def s7_context(r, L):
    k = pick(r, ["square", "cube", "approx"] if L else ["square", "cube"])
    if k == "square":
        s = r.randint(4, 25)
        return P(f"A square patio has an area of {s * s} square feet. What is the side length?", f"{s} feet",
                 [f"Side = √{s * s} = {s} feet, since {s}² = {s * s}."], [f"{s * s // 4} feet", f"{s * s // 2} feet", f"{s * 2} feet"], chk_val(f"√{s * s}"), tags=["modeling"])
    if k == "cube":
        s = r.randint(2, 12)
        return P(f"A cube-shaped box has a volume of {s ** 3} cubic centimeters. What is the length of one edge?", f"{s} cm",
                 [f"Edge = ∛{s ** 3} = {s} cm, since {s}³ = {s ** 3}."], [f"{s ** 3 // 3} cm" if s ** 3 % 3 == 0 else f"{s * 3} cm", f"{s * s} cm", f"{s ** 3 // 6 if s ** 3 % 6 == 0 else s + 1} cm"],
                 chk_val(f"∛{s ** 3}"), tags=["modeling"])
    a = pick(r, [k for k in range(20, 400) if math.isqrt(k) ** 2 != k])
    ans = Rd(math.sqrt(a), 1)
    return P(f"A square garden has an area of {a} square meters. Find the side length to the nearest tenth of a meter.", f"{ans} m",
             [f"Side = √{a}.", f"√{a} ≈ {Rd(math.sqrt(a), 3)} ≈ {ans} m."], [f"{Rd(a / 4, 1)} m", f"{Rd(a / 2, 1)} m", f"{Rd(math.sqrt(a) + 0.1, 1)} m"],
             {"kind": "approx", "expr": f"√{a}", "places": 1}, tags=["modeling"])


@fam("2")
def s7_estimate_reverse(r, L):
    t = F(r.randint(21, 99), 10)
    need(t.denominator != 1)
    lo, hi = math.floor(t * t), math.ceil(t * t)
    c = pick(r, [n for n in range(lo - 3, hi + 4) if Rd(math.sqrt(n), 1) == D(t)] or [None])
    need(c is not None)
    cands = [n for n in range(int(t * t) - 8, int(t * t) + 9) if n > 0]
    opts_ = [c] + [n for n in cands if Rd(math.sqrt(n), 1) != D(t)][:0]
    bad = []
    for n in [c - 6, c + 6, c + 3 if Rd(math.sqrt(c + 3), 1) != D(t) else c + 9, c - 3 if Rd(math.sqrt(c - 3), 1) != D(t) else c - 9, int(t * 10), int(t * 2)]:
        if n > 0 and Rd(math.sqrt(n), 1) != D(t) and n not in bad and n != c:
            bad.append(n)
    need(len(bad) >= 3)
    opts = [(str(n), False) for n in bad[:3]] + [(str(c), True)]
    r.shuffle(opts)
    return P(f"For which whole number n does √n round to {D(t)} (to the nearest tenth)?", str(c),
             [f"{D(t)}² = {D(t * t)}, so n should be close to {D(t * t)}.", f"√{c} ≈ {Rd(math.sqrt(c), 3)}, which rounds to {D(t)}."],
             options=opts, chk=chk_py("sqrt_rounds_to", t=D(t)), tags=["reasoning", "challenge"], mode="mc")


@fam("012")
def s7_error(r, L):
    a, b = pick(r, [(9, 16), (36, 64), (16, 9), (25, 144), (64, 36), (81, 144)])
    s = math.isqrt(a + b)
    opts = [(f"{s}", True), (f"{math.isqrt(a) + math.isqrt(b)}", False), (f"{a + b}", False), (f"{math.isqrt(a) * math.isqrt(b)}", False)]
    return P(f"Kim wrote √({a} + {b}) = √{a} + √{b} = {math.isqrt(a)} + {math.isqrt(b)} = {math.isqrt(a) + math.isqrt(b)}. What is the correct value of √({a} + {b})?",
             f"{s}", ["The square root of a sum is not the sum of the square roots.", f"Add first: {a} + {b} = {a + b}.", f"√{a + b} = {s}."],
             options=[(t, c) for t, c in [opts[i] for i in seed_perm(r)]], chk=chk_val(f"√({a} + {b})"), tags=["error-analysis", "misconception"], mode="mc")


def seed_perm(r):
    p = [0, 1, 2, 3]
    r.shuffle(p)
    return p


@fam("012")
def s7_open(r, L):
    s = r.randint(3, 12)
    c = r.randint(2, 6)
    n = pick(r, [k for k in range(20, 120) if math.isqrt(k) ** 2 != k])
    return P("Answer each part about roots.", None,
             [f"{s}² = {s * s}.", f"{c}³ = {c ** 3}.", f"√{n} ≈ {Rd(math.sqrt(n), 3)}.", f"x² = {s * s} has two solutions."],
             parts=[(f"Evaluate √{s * s}.", str(s), chk_val(f"√{s * s}")), (f"Evaluate ∛{c ** 3}.", str(c), chk_val(f"∛{c ** 3}")),
                    (f"Approximate √{n} to the nearest tenth.", Rd(math.sqrt(n), 1), {"kind": "approx", "expr": f"√{n}", "places": 1}),
                    (f"Solve x² = {s * s}.", f"x = {s} or x = -{s}", chk_py("pm_sol", n=2, c=str(s * s)))], tags=["multistep"])


# ======================================================================= S8 Negative exponents
@fam("012")
def s8_evaluate(r, L):
    if L == 0:
        b, e = r.randint(2, 10), r.randint(1, 3)
        need(b ** e <= 1000)
        expr = f"{b}{sup(-e)}"
        v = F(1, b ** e)
        wrong = [str(-b ** e), N(F(-b * e)), N(F(1, b * e)) if b * e != b ** e else str(b ** e)]
    elif L == 1:
        kind = pick(r, ["neg", "frac", "coef"])
        if kind == "neg":
            b, e = -r.randint(2, 6), r.randint(2, 3)
            expr, v = f"({b}){sup(-e)}", F(1, b ** e)
            wrong = [N(-v), str(b ** e), N(F(1, b * e))]
        elif kind == "frac":
            p, q = r.randint(1, 4), r.randint(2, 5)
            need(math.gcd(p, q) == 1)
            e = r.randint(1, 3)
            expr, v = f"({p}/{q}){sup(-e)}", F(q, p) ** e
            wrong = [N(F(p, q) ** e), N(-F(q, p) ** e), N(F(q, p) * e)]
        else:
            c, b, e = r.randint(2, 9), r.randint(2, 5), r.randint(1, 3)
            expr, v = f"{c} · {b}{sup(-e)}", F(c, b ** e)
            wrong = [N(F(1, (c * b) ** e)), N(F(-c * b ** e)), N(F(c * b ** e))]
    else:
        b1, b2 = r.randint(2, 5), r.randint(2, 4)
        e1, e2 = r.randint(1, 3), r.randint(1, 2)
        expr = f"{b1}{sup(-e1)} + {b2}{sup(-e2)}"
        v = F(1, b1 ** e1) + F(1, b2 ** e2)
        wrong = [N(F(1, b1 ** e1 + b2 ** e2)), N(-F(b1 ** e1 + b2 ** e2)), N(F(1, b1 ** e1) * F(1, b2 ** e2))]
    return P(f"Evaluate: {expr}", N(v), ["A negative exponent means a reciprocal: a⁻ⁿ = 1/aⁿ (a ≠ 0).", f"{expr} = {N(v)}."], wrong, chk_val(expr),
             tags=["misconception"])


@fam("012")
def s8_rewrite(r, L):
    vs = pick(r, ["x", "y", "a", "m", "n"])
    if L == 0:
        e = r.randint(1, 6)
        expr, ans = f"{vs}{sup(-e)}", f"1/{vs}{sup(e)}"
        wrong = [f"-{vs}{sup(e)}", f"{vs}{sup(e)}", f"1/{vs}{sup(-e)}"]
    elif L == 1:
        c, e = r.randint(2, 9), r.randint(2, 5)
        if r.random() < 0.5:
            expr, ans = f"{c}{vs}{sup(-e)}", f"{c}/{vs}{sup(e)}"
            wrong = [f"1/({c}{vs}{sup(e)})", f"-{c}{vs}{sup(e)}", f"{c}{vs}{sup(e)}"]
        else:
            expr, ans = f"1 ÷ {vs}{sup(-e)}", f"{vs}{sup(e)}"
            wrong = [f"1/{vs}{sup(e)}", f"-{vs}{sup(e)}", f"{vs}{sup(-e)}"]
    else:
        c, d, e, f_ = r.randint(2, 9), r.randint(2, 9), r.randint(1, 4), r.randint(1, 4)
        need(math.gcd(c, d) == 1)
        expr, ans = f"{c}x{sup(-e)}{pw('y', f_)} ÷ {d}", f"{c}{pw('y', f_)}/({d}{pw('x', e)})"
        wrong = [f"{c}{pw('x', e)}{pw('y', f_)}/{d}", f"{c}/({d}{pw('x', e)}{pw('y', f_)})", f"-{c}{pw('x', e)}{pw('y', f_)}/{d}"]
        vs = None
    vars_ = ["x", "y"] if vs is None else [vs]
    return P(f"Rewrite {expr} using only positive exponents.", ans, ["Move a factor with a negative exponent across the fraction bar and make the exponent positive.",
                                                                    "Only the factor with the negative exponent moves; coefficients with positive exponents stay." if L else f"{expr} = {ans}."],
             wrong, chk_py("pos_exp_equiv", expr=expr, vars=vars_), tags=["misconception"])


@fam("012")
def s8_as_power(r, L):
    b = r.randint(2, 6)
    e = r.randint(1, 4)
    need(b ** e <= 1300)
    if L < 2:
        shown = f"1/{b ** e}"
        ans = f"{b}{sup(-e)}"
        wrong = [f"{b}{sup(e)}", f"-{b}{sup(e)}", f"{b ** e}{sup(-1)}" if e > 1 else f"{b}{sup(-2)}"]
        q = f"Write {shown} as a power of {b} with an integer exponent."
    else:
        shown = f"{b ** e}"
        ans = f"(1/{b}){sup(-e)}"
        wrong = [f"(1/{b}){sup(e)}", f"-(1/{b}){sup(e)}", f"(1/{b}){sup(-e - 1)}"]
        q = f"Write {shown} as a power of 1/{b} with an integer exponent."
    return P(q, ans, [f"{b}{sup(e)} = {b ** e}, so {shown} = {ans}." if L < 2 else f"(1/{b})⁻ⁿ = {b}ⁿ, so {b ** e} = {ans}."],
             wrong, chk_py("power_form", expr=shown, base=f"{b}" if L < 2 else f"1/{b}"), tags=["reasoning"] if L == 2 else [])


@fam("01", mode="sa")
def s8_pattern(r, L):
    b = r.randint(2, 5)
    k = r.randint(1, 3) if L == 0 else r.randint(2, 4)
    seq = [b ** 2, b, 1] + [F(1, b ** j) for j in range(1, k + 1)]
    shown = ", ".join(f"{b}{sup(2 - i)} = {N(v)}" for i, v in enumerate(seq[:-1]))
    target = 2 - (len(seq) - 1)
    return P(f"Continue the pattern (each step divides by {b}): {shown}, {b}{sup(target)} = ?", N(seq[-1]),
             [f"Each time the exponent decreases by 1, divide by {b}.", f"{N(seq[-2])} ÷ {b} = {N(seq[-1])}."],
             [str(-b ** -target), N(F(1, b * -target)), N(seq[-2])], chk_val(f"{b}^({target})"), tags=["reasoning"], mode="any")


@fam("2")
def s8_find_exp(r, L):
    b = pick(r, [2, 3, 5, 10])
    e = -r.randint(1, 4)
    t = F(b) ** e
    neg_frac = r.random() < 0.4
    if neg_frac:
        tshown = f"(1/{b}){sup('n')}".replace("ⁿ", "") if False else None
    return P(f"Find the integer n: {b}ⁿ = {N(t)}", f"n = {e}", [f"{N(t)} = 1/{b ** -e} = 1/{b}{sup(-e)} = {b}{sup(e)}.", f"So n = {e}."],
             [f"n = {-e}", f"n = {N(F(1, -e))}", f"n = {e * b}"], chk_py("exp_solve", base=str(b), target=N(t)), tags=["reasoning"])


@fam("2", mode="mc")
def s8_greatest(r, L):
    cands = [f"2{sup(-3)}", f"(-2){sup(-2)}", f"3{sup(-1)}", f"(1/2){sup(-1)}", f"4{sup(-2)}", f"(-3){sup(-1)}", f"(1/3){sup(-2)}", f"5{sup(0)}"]
    items = pick(r, cands, 4)
    vals = [fval(t) for t in items]
    need(len(set(vals)) == 4)
    want_max = r.random() < 0.6
    good = items[vals.index(max(vals) if want_max else min(vals))]
    return P(f"Which expression has the {'greatest' if want_max else 'least'} value?", good,
             ["Evaluate each: " + "; ".join(f"{t} = {N(F(v).limit_denominator(1000))}" for t, v in zip(items, vals)) + "."],
             options=[(t, t == good) for t in items], chk=chk_py("extreme", items=items, max=want_max), tags=["reasoning"], mode="mc")


@fam("012")
def s8_error(r, L):
    b, e = r.randint(2, 6), r.randint(2, 3)
    wrongv = -b ** e
    return P(f"Lee says {b}{sup(-e)} = {wrongv} because \"the negative exponent makes the number negative.\" What is the correct value of {b}{sup(-e)}?",
             N(F(1, b ** e)), ["A negative exponent indicates a reciprocal, not a negative number.", f"{b}{sup(-e)} = 1/{b}{sup(e)} = {N(F(1, b ** e))}."],
             [str(wrongv), N(F(-1, b ** e)), N(F(1, b * e))], chk_val(f"{b}^(-{e})"), tags=["error-analysis", "misconception"])


@fam("012")
def s8_select(r, L):
    b = pick(r, [2, 3, 4])
    e = pick(r, [2, 3]) if b != 4 else 2
    t = F(1, b ** e)
    good = [f"{b}{sup(-e)}", f"1/{b}{sup(e)}", f"(1/{b}){sup(e)}", f"({b ** e}){sup(-1)}"]
    bad = [f"-{b}{sup(e)}", f"{b}{sup(e)}", f"(-{b}){sup(-e - 1)}", f"{b * e}{sup(-1)}"]
    opts = [(g, True) for g in pick(r, good, 3)] + [(x, False) for x in pick(r, bad, 3)]
    return P(f"Select ALL expressions equal to {N(t)}.", None, [f"{N(t)} = 1/{b ** e}."] + [f"{x} = {N(F(Fv(x)).limit_denominator(10000))}." for x, _ in opts],
             options=opts, chk=chk_val(N(t)), tags=["multiple-representations"])


def Fv(x):
    return fval(x)


@fam("012")
def s8_open(r, L):
    b = r.randint(2, 5)
    return P(f"Use the pattern of powers of {b}.", None,
             [f"{b}² = {b * b}; divide by {b} each step.", f"{b}⁰ = 1.", f"{b}⁻¹ = 1/{b}.", f"{b}⁻² = 1/{b * b}."],
             parts=[(f"Evaluate {b}².", str(b * b), chk_val(f"{b}^2")), (f"Evaluate {b}⁰.", "1", chk_val(f"{b}^0")),
                    (f"Evaluate {b}⁻¹.", f"1/{b}", chk_val(f"{b}^(-1)")), (f"Evaluate {b}⁻².", f"1/{b * b}", chk_val(f"{b}^(-2)"))], tags=["reasoning"])


# ======================================================================= S9 Operations with negative exponents
@fam("012")
def s9_numeric(r, L):
    b = r.randint(2, 5)
    e1, e2 = r.randint(-6, 4), r.randint(-6, 4)
    op = pick(r, ["*", "/", "pow"])
    if op == "*":
        expr, v, ew = f"{b}{sup(e1)} · {b}{sup(e2)}", F(b) ** (e1 + e2), e1 * e2
    elif op == "/":
        expr, v, ew = f"{b}{sup(e1)} ÷ {b}{sup(e2)}", F(b) ** (e1 - e2), e1 + e2
    else:
        e2 = pick(r, [-2, -1, 2, 3])
        expr, v, ew = f"({b}{sup(e1)}){sup(e2)}", F(b) ** (e1 * e2), e1 + e2
    need(e1 < 0 or e2 < 0)
    need(abs(v.numerator) <= 3000 and v.denominator <= 3000)
    wrong = [N(F(b) ** ew) if abs(ew) <= 8 else N(v * b), N(F(b * b) ** ((e1 + e2) if op != "pow" else e1)) if abs(e1 + e2) < 5 else N(-v), N(-v)]
    return P(f"Simplify and evaluate: {expr}", N(v),
             [{"*": "Same base, multiply: add the exponents.", "/": "Same base, divide: subtract the exponents.", "pow": "Power of a power: multiply the exponents."}[op],
              f"{expr} = {b}{sup({'*': e1 + e2, '/': e1 - e2, 'pow': e1 * e2}[op])} = {N(v)}."], wrong, chk_val(expr), tags=["misconception"])


@fam("012")
def s9_variable(r, L):
    v = pick(r, ["x", "y", "a", "b", "n"])
    e1, e2 = nz(r, -7, 6), nz(r, -7, 6)
    op = pick(r, ["*", "/", "pow"])
    if op == "*":
        expr, res = f"{v}{sup(e1)} · {v}{sup(e2)}", e1 + e2
    elif op == "/":
        expr, res = f"{v}{sup(e1)} ÷ {v}{sup(e2)}", e1 - e2
    else:
        e2 = pick(r, [-3, -2, -1, 2, 3])
        expr, res = f"({v}{sup(e1)}){sup(e2)}", e1 * e2
    need((e1 < 0 or e2 < 0) and res != 0 and abs(res) <= 21)
    ans = f"{v}{sup(res)}" if res > 0 else f"1/{v}{sup(-res)}"
    wr = {"*": [e1 * e2, e1 - e2], "/": [e1 + e2, e1 * e2 if e2 != 0 else e1], "pow": [e1 + e2, e1 - e2]}[op]
    wrong = [(f"{v}{sup(w)}" if w > 0 else f"1/{v}{sup(-w)}") if w else "1" for w in wr] + [f"{v}{sup(-res)}" if -res > 0 else f"1/{v}{sup(res)}"]
    return P(f"Simplify {expr}. Write the answer with a positive exponent.", ans, [f"Exponent: {res}.", f"{v}{sup(res)} = {ans}." if res < 0 else f"Result: {ans}."],
             wrong, chk_py("pos_exp_equiv", expr=expr, vars=[v]), tags=["misconception"])


@fam("12")
def s9_coef(r, L):
    a, b = r.randint(2, 6), r.randint(2, 6)
    e1, e2 = nz(r, -5, 5), nz(r, -5, 5)
    form = pick(r, ["prod", "quot", "pow"])
    if form == "prod":
        expr = f"({a}x{sup(e1)})({b}x{sup(e2)})"
        c, res = F(a * b), e1 + e2
    elif form == "quot":
        expr = f"{a * b}x{sup(e1)} ÷ ({b}x{sup(e2)})"
        c, res = F(a), e1 - e2
    else:
        e2 = pick(r, [-2, 2, -1])
        expr = f"({a}x{sup(e1)}){sup(e2)}"
        c, res = F(a) ** e2, e1 * e2
    need(e1 < 0 or e2 < 0 or c.denominator != 1)
    if res == 0:
        ans = N(c)
    elif res > 0:
        ans = f"{N(c) if c != 1 else ''}x{sup(res)}" if c.denominator == 1 else f"x{sup(res)}/{c.denominator}" if c.numerator == 1 else f"{c.numerator}x{sup(res)}/{c.denominator}"
    else:
        ans = f"{N(c)}/x{sup(-res)}" if c.denominator == 1 else f"{c.numerator}/({c.denominator}x{sup(-res)})"
    wrong = [ans.replace(sup(abs(res)), sup(abs(res) + 1)) if res else N(c + 1), f"{N(c * 2)}x{sup(abs(res))}" if c.denominator == 1 else f"x{sup(abs(res) + 2)}", f"-{ans}"]
    return P(f"Simplify {expr}. Use only positive exponents.", ans, ["Multiply or divide the coefficients; apply the exponent rules to the powers of x.", f"Result: {ans}."],
             wrong, chk_py("pos_exp_equiv", expr=expr, vars=["x"]), tags=["multistep"])


@fam("2")
def s9_missing(r, L):
    e1, k = nz(r, -6, 6), nz(r, -6, 6)
    form = pick(r, ["prod", "quot", "pow"])
    if form == "prod":
        tgt = e1 + k
        shown, tmpl = f"x{sup(e1)} · xᵏ = x{sup(tgt)}", f"x^({e1})*x^K"
    elif form == "quot":
        tgt = e1 - k
        shown, tmpl = f"x{sup(e1)} ÷ xᵏ = x{sup(tgt)}", f"x^({e1})/x^K"
    else:
        need(abs(e1 * k) <= 24)
        tgt = e1 * k
        shown, tmpl = f"(x{sup(e1)})ᵏ = x{sup(tgt)}", f"(x^({e1}))^K"
    need(tgt != 0 and (e1 < 0 or k < 0 or tgt < 0))
    wrong = [f"k = {-k}", f"k = {tgt}", f"k = {tgt + e1}"]
    return P(f"Find the integer k that makes the equation true for x ≠ 0: {shown}", f"k = {k}",
             [{"prod": f"{e1} + k = {tgt}", "quot": f"{e1} - k = {tgt}", "pow": f"{e1} · k = {tgt}"}[form] + ".", f"k = {k}."],
             wrong, chk_py("missing_exp", template=tmpl, target=f"x^({tgt})"), tags=["reasoning", "challenge"])


@fam("2")
def s9_two_var(r, L):
    p, q, s = nz(r, -4, 4), nz(r, -4, 4), pick(r, [-2, -1, 2])
    expr = f"(a{sup(p)}b{sup(q)}){sup(s)}"
    pa, pb = p * s, q * s
    num = "".join(pw(v, e) for v, e in (("a", pa), ("b", pb)) if e > 0) or "1"
    den = "".join(f"{v}{sup(-e) if e != -1 else ''}" for v, e in (("a", pa), ("b", pb)) if e < 0)
    ans = num if not den else f"{num}/{den}" if len(den) <= 2 or den.count("a") + den.count("b") == 1 else f"{num}/({den})"
    need("/" in ans or True)
    wrong = [f"{pw('a', abs(p + s))}{pw('b', abs(q + s))}" if p + s and q + s else f"{pw('a', abs(pa) + 1)}{pw('b', abs(pb))}",
             (f"{den}/{num}" if num != "1" else den) if den else f"1/{num}" if len(num) <= 2 else f"1/({num})",
             f"{pw('a', abs(pa))}{pw('b', abs(pb))}" if (pa < 0 or pb < 0) else f"1/({pw('a', pa)}{pw('b', pb)})"]
    return P(f"Simplify {expr} using only positive exponents.", ans, ["Raise each factor to the outside power: multiply exponents.", f"a{sup(pa)}b{sup(pb)} = {ans}."],
             wrong, chk_py("pos_exp_equiv", expr=expr, vars=["a", "b"]), tags=["challenge"])


@fam("012")
def s9_error(r, L):
    e1, e2 = -r.randint(2, 5), r.randint(2, 6)
    ans_e = e1 + e2
    need(ans_e != 0 and e1 * e2 != ans_e)
    corr = f"x{sup(ans_e)}" if ans_e > 0 else f"1/x{sup(-ans_e)}"
    return P(f"Mia simplified x{sup(e1)} · x{sup(e2)} as x{sup(e1 * e2)}. What is the correct simplified form (positive exponents)?", corr,
             ["Mia multiplied the exponents; when multiplying powers with the same base, add the exponents.", f"{e1} + {e2} = {ans_e}, so the product is {corr}."],
             [f"1/x{sup(-e1 * e2)}", f"x{sup(-ans_e)}" if -ans_e > 0 else f"1/x{sup(ans_e)}", f"x{sup(e2 - e1)}"], chk_py("pos_exp_equiv", expr=f"x^({e1})*x^({e2})", vars=["x"]),
             tags=["error-analysis", "misconception"])


@fam("012")
def s9_select(r, L):
    k = -r.randint(4, 8)
    good = [f"x{sup(k + 2)} · x{sup(-2)}", f"(x{sup(k // 2 if k % 2 == 0 else -1)}){sup(2 if k % 2 == 0 else -k)}", f"x{sup(2)} ÷ x{sup(2 - k)}", f"1/x{sup(-k)}"]
    bad = [f"x{sup(-k)}", f"-x{sup(-k)}", f"x{sup(k + 2)} · x{sup(2)}", f"(x{sup(-2)}){sup(-k // 2 if k % 2 == 0 else -k)}" if False else f"x{sup(k)} · x{sup(-k)}"]
    import mathtext as MT
    ok = [g for g in good if all(MT.same(MT.ev(g, {"x": F(t)}), F(t) ** k) for t in (2, 3))]
    need(len(ok) >= 3)
    opts = [(g, True) for g in ok[:3]] + [(b, False) for b in bad[:3]]
    return P(f"Select ALL expressions equivalent to x{sup(k)} (x ≠ 0).", None, ["Use the product, quotient and power rules to simplify each choice."],
             options=opts, chk={"kind": "equiv", "expr": f"x^({k})", "vars": ["x"], "strip": False}, tags=["multiple-representations"])


@fam("012")
def s9_open(r, L):
    a, b = r.randint(-5, -2), r.randint(2, 6)
    return P(f"Let A = x{sup(a)} and B = x{sup(b)} (x ≠ 0). Write each answer as a single power of x.", None,
             [f"Add: {a} + {b}.", f"Subtract: {a} - {b}.", f"Multiply: {a} · 2.", f"Subtract: {b} - {a}."],
             parts=[("A · B", f"x{sup(a + b)}" if a + b else "1", {"kind": "equiv", "expr": f"x^({a})*x^({b})", "vars": ["x"]}),
                    ("A ÷ B", f"x{sup(a - b)}", {"kind": "equiv", "expr": f"x^({a})/x^({b})", "vars": ["x"]}),
                    ("A²", f"x{sup(2 * a)}", {"kind": "equiv", "expr": f"(x^({a}))^2", "vars": ["x"]}),
                    ("B ÷ A", f"x{sup(b - a)}", {"kind": "equiv", "expr": f"x^({b})/x^({a})", "vars": ["x"]})], tags=["multistep"])


# ======================================================================= S10 Scientific notation
def sci_of(v):
    v = F(v)
    e = 0
    while abs(v) >= 10:
        v /= 10
        e += 1
    while abs(v) < 1:
        v *= 10
        e -= 1
    return D(v), e


def std(v):
    v = F(v)
    if v.denominator == 1:
        return f"{v.numerator:,}"
    return D(v)


@fam("012")
def s10_to_sci(r, L):
    big = r.random() < 0.5
    digs = r.randint(12, 99) if L == 0 else r.randint(101, 999)
    need(digs % 10)
    e = r.randint(4, 9) if big else -r.randint(2, 7)
    v = F(digs) * F(10) ** (e - (len(str(digs)) - 1))
    m, ee = sci_of(v)
    ans = sci(m, ee)
    wrong = [sci(m, -ee), sci(m, ee + 1), sci(D(F(m) * 10), ee - 1) if L else sci(str(digs), ee - len(str(digs)) + 1)]
    return P(f"Write {std(v)} in scientific notation.", ans, [f"Move the decimal point so one nonzero digit is to its left: {m}.",
                                                           f"The decimal point moved {abs(ee)} places, so the exponent is {ee}.", f"{std(v)} = {ans}."],
             wrong, chk_py("sci_form", expr=str(v)), tags=["misconception"])


@fam("012")
def s10_to_std(r, L):
    m = F(r.randint(11, 99), 10) if L == 0 else F(r.randint(101, 999), 100)
    need(m.denominator != 1)
    e = nz(r, -6, 8) if L else pick(r, [2, 3, 4, 5, -2, -3])
    v = m * F(10) ** e
    wrong = [std(m * F(10) ** -e), std(m * F(10) ** (e + 1)), std(m * F(10) ** (e - 1))]
    return P(f"Write {sci(D(m), e)} in standard form.", std(v), [f"Move the decimal point {abs(e)} places {'right' if e > 0 else 'left'}.", f"{sci(D(m), e)} = {std(v)}."],
             wrong, chk_val(f"{D(m)}*10^({e})"))


@fam("012")
def s10_compare_times(r, L):
    a, b = r.randint(2, 9), r.randint(1, 9)
    e1, e2 = r.randint(5, 12), r.randint(2, 6)
    need(e1 - e2 >= 2 and a % b == 0)
    q = F(a, b) * F(10) ** (e1 - e2)
    ctx = pick(r, ["A star is about {A} kilometers away and a planet is about {B} kilometers away.", "Country A has a population of about {A} people and city B has about {B} people.",
                   "One computer does about {A} operations per second and another does about {B}."])
    p = ctx.format(A=sci(a, e1), B=sci(b, e2)) + " How many times greater is the first number than the second?"
    if L == 0:
        p = f"How many times greater is {sci(a, e1)} than {sci(b, e2)}?"
    return P(p, std(q), [f"Divide: ({a} ÷ {b}) × 10{sup(e1)}⁻{sup(e2)[0] if False else ''} = {a // b} × 10{sup(e1 - e2)}." .replace("⁻", "", 1),
                         f"{a // b} × 10{sup(e1 - e2)} = {std(q)}."],
             [std(q * 10), std(F(a - b) * F(10) ** (e1 - e2)), std(F(a, b) * F(10) ** (e1 + e2)) if e1 + e2 <= 15 else std(q / 10)],
             chk_py("sci_or_std", expr=f"({a}*10^{e1})/({b}*10^{e2})"), tags=["modeling"] if L else [])


@fam("12")
def s10_estimate(r, L):
    big = r.random() < 0.6
    v = F(r.randint(1001, 9899)) * (F(10) ** r.randint(1, 4) if big else F(1, 10 ** r.randint(6, 9)))
    lead = int(str(sci_of(v)[0])[0])
    need(not str(sci_of(v)[0]).startswith("9.5") and not str(sci_of(v)[0]).startswith("9.6"))
    m, e = sci_of(v)
    d = math.floor(F(m) + F(1, 2))
    need(d < 10)
    ans = sci(d, e)
    return P(f"Estimate {std(v)} as a single digit times an integer power of 10.", ans,
             [f"{std(v)} ≈ {sci(m, e)}.", f"Round {m} to {d}: about {ans}."],
             [sci(d, -e), sci(d + 1 if d < 9 else d - 1, e), sci(d, e + 1)], chk_py("single_digit_est", expr=str(v)), tags=["modeling"])


@fam("2")
def s10_normalize(r, L):
    m = F(r.randint(11, 999), pick(r, [10, 100]))
    need(m >= 10 or m < 1)
    e = nz(r, -8, 9)
    v = m * F(10) ** e
    mm, ee = sci_of(v)
    ans = sci(mm, ee)
    return P(f"The number {D(m)} × 10{sup(e)} is not in scientific notation. Rewrite it in scientific notation.", ans,
             [f"{D(m)} = {mm} × 10{sup(ee - e)}.", f"Add exponents: 10{sup(ee - e)} · 10{sup(e)} = 10{sup(ee)}.", ans],
             [sci(mm, e - (ee - e)), sci(mm, e), sci(D(m), ee)], chk_py("sci_form", expr=f"{D(m)}*10^({e})"), tags=["reasoning", "misconception"])


@fam("012")
def s10_context(r, L):
    ctx = pick(r, [("The diameter of a red blood cell is about {X} meter.", -6, "meter"), ("The mass of a grain of sand is about {X} gram.", -4, "gram"),
                   ("The distance from Earth to the Sun is about {X} kilometers.", 8, "kilometers"), ("A large stadium sold about {X} tickets this season.", 6, "tickets")])
    m = F(r.randint(11, 99), 10)
    v = m * F(10) ** ctx[1]
    if r.random() < 0.5:
        return P(ctx[0].format(X=std(v)) + " Write this number in scientific notation.", sci(D(m), ctx[1]),
                 [f"{std(v)} = {sci(D(m), ctx[1])}."], [sci(D(m), -ctx[1]), sci(D(m), ctx[1] + 1), sci(D(m * 10), ctx[1])],
                 chk_py("sci_form", expr=str(v)), tags=["modeling"])
    return P(ctx[0].format(X=sci(D(m), ctx[1])) + " Write this number in standard form.", std(v),
             [f"Move the decimal point {abs(ctx[1])} places {'right' if ctx[1] > 0 else 'left'}."], [std(m * F(10) ** -ctx[1]), std(v * 10), std(v / 10)],
             chk_val(f"{D(m)}*10^({ctx[1]})"), tags=["modeling"])


@fam("012")
def s10_error(r, L):
    m = F(r.randint(11, 99), 10)
    e = -r.randint(3, 7)
    v = m * F(10) ** e
    return P(f"Noah wrote {std(v)} = {sci(D(m), -e)}. What is the correct scientific notation?", sci(D(m), e),
             [f"{std(v)} is less than 1, so the exponent must be negative.", f"Move the decimal point {-e} places right: {sci(D(m), e)}."],
             [sci(D(m), -e), sci(D(m), e + 1), sci(D(m * 10), e - 1)], chk_py("sci_form", expr=str(v)), tags=["error-analysis", "misconception"])


@fam("012")
def s10_select(r, L):
    good = [sci(D(F(r.randint(11, 99), 10)), nz(r, -9, 9)) for _ in range(3)] + [sci(str(r.randint(1, 9)), nz(r, -9, 9))]
    bad = [f"{r.randint(11, 99)} × 10{sup(r.randint(2, 8))}", f"{D(F(r.randint(1, 9), 10))} × 10{sup(r.randint(2, 8))}", f"{D(F(r.randint(11, 99), 10))} × 100", f"{r.randint(2, 9)}{sup(r.randint(3, 8))}"]
    opts = [(g, True) for g in pick(r, good, 3)] + [(b, False) for b in pick(r, bad, 3)]
    need(len({o[0] for o in opts}) == 6)
    return P("Select ALL numbers that are written in scientific notation.", None,
             ["Scientific notation is a × 10ⁿ with 1 ≤ a < 10 and n an integer."], options=opts, chk=chk_py("is_sci_notation"), tags=["reasoning"])


@fam("012")
def s10_open(r, L):
    a, b = F(r.randint(11, 99), 10), F(r.randint(11, 99), 10)
    e1, e2 = r.randint(5, 9), -r.randint(3, 6)
    va, vb = a * F(10) ** e1, b * F(10) ** e2
    return P(f"Number A is {std(va)} and number B is {std(vb)}.", None,
             [f"A = {sci(D(a), e1)}.", f"B = {sci(D(b), e2)}.", "A is greater than 1 and B is less than 1.", f"Exponent difference {e1} - ({e2}) = {e1 - e2}."],
             parts=[("Write A in scientific notation.", sci(D(a), e1), chk_py("sci_form", expr=str(va))),
                    ("Write B in scientific notation.", sci(D(b), e2), chk_py("sci_form", expr=str(vb))),
                    ("Which number is greater, A or B?", "A", chk_py("letter_greater", A=str(va), B=str(vb))),
                    ("What is the difference of the exponents of 10 (exponent of A minus exponent of B)?", str(e1 - e2), chk_val(f"{e1} - ({e2})"))],
             tags=["multiple-representations"])


# ======================================================================= S11 Operations in scientific notation
def rnd_sci(r, digits=2):
    m = F(r.randint(10 ** (digits - 1), 10 ** digits - 1), 10 ** (digits - 1))
    return m


@fam("012")
def s11_multiply(r, L):
    a, b = (F(r.randint(2, 4)), F(r.randint(2, 3))) if L == 0 else (rnd_sci(r), rnd_sci(r))
    e1, e2 = nz(r, -8, 9), nz(r, -8, 9)
    v = a * b * F(10) ** (e1 + e2)
    need(is_term(v))
    m, e = sci_of(v)
    need(len(m) <= 6)
    ans = sci(m, e)
    wrong = [sci(D(a * b) if a * b < 10 else m, e1 * e2) if abs(e1 * e2) < 30 else sci(m, -e), sci(D(a * b), e1 + e2) if a * b >= 10 else sci(m, e + 1), sci(D(a + b) if a + b < 10 else m, e1 + e2 + (0 if a + b < 10 else 2))]
    return P(f"Multiply. Write the answer in scientific notation: ({sci(D(a), e1)})({sci(D(b), e2)})", ans,
             [f"Multiply the decimals: {D(a)} × {D(b)} = {D(a * b)}.", f"Add the exponents: {e1} + ({e2}) = {e1 + e2}.", f"Adjust so the first factor is between 1 and 10: {ans}."],
             wrong, chk_py("sci_form", expr=f"({D(a)}*10^({e1}))*({D(b)}*10^({e2}))"), tags=["misconception"] if a * b >= 10 else [])


@fam("012")
def s11_divide(r, L):
    q = F(r.randint(1, 9)) if L == 0 else rnd_sci(r)
    b = F(r.randint(2, 4)) if L == 0 else rnd_sci(r)
    a = q * b
    need(is_term(a) and len(D(a)) <= 6)
    e1, e2 = nz(r, -6, 12), nz(r, -6, 8)
    v = a / b * F(10) ** (e1 - e2)
    m, e = sci_of(v)
    ans = sci(m, e)
    am, ae = sci_of(a * F(10) ** e1)
    wrong = [sci(m, e1 + e2) if e1 + e2 != e else sci(m, -e), sci(m, e + 1), sci(D(F(am) * F(sci_of(b)[0])) if F(am) * F(sci_of(b)[0]) < 10 else m, e - 2)]
    return P(f"Divide. Write the answer in scientific notation: ({sci(am, ae)}) ÷ ({sci(sci_of(b)[0], e2)})", ans,
             [f"Divide the decimals: {am} ÷ {sci_of(b)[0]} = {D(F(am) / F(sci_of(b)[0]))}.", f"Subtract the exponents: {ae} - ({e2}) = {ae - e2}.", f"Adjust: {ans}."],
             wrong, chk_py("sci_form", expr=f"({am}*10^({ae}))/({sci_of(b)[0]}*10^({e2}))"), tags=["misconception"])


@fam("12")
def s11_addsub(r, L):
    a, b = rnd_sci(r), rnd_sci(r)
    e1 = r.randint(3, 9)
    e2 = e1 - pick(r, [0, 1, 2])
    op = pick(r, ["+", "-"])
    v = a * F(10) ** e1 + (1 if op == "+" else -1) * b * F(10) ** e2
    need(v > 0)
    m, e = sci_of(v)
    ans = sci(m, e)
    naive = a + b if op == "+" else a - b
    wrong = [sci(D(naive), e1 + e2) if 1 <= naive < 10 else sci(m, e + 1), sci(D(naive), e1) if 1 <= naive < 10 and e1 != e2 else sci(m, e - 1), sci(m, e1 + e2)]
    return P(f"{'Add' if op == '+' else 'Subtract'}. Write the answer in scientific notation: ({sci(D(a), e1)}) {op} ({sci(D(b), e2)})", ans,
             [f"Rewrite with the same power of 10: {sci(D(b), e2)} = {sci(D(b * F(10) ** (e2 - e1)), e1)}." if e1 != e2 else "The powers of 10 already match.",
              f"{D(a)} {op} {D(b * F(10) ** (e2 - e1))} = {D(a + (1 if op == '+' else -1) * b * F(10) ** (e2 - e1))}.", f"Result: {ans}."],
             wrong, chk_py("sci_form", expr=f"{D(a)}*10^({e1}) {op} {D(b)}*10^({e2})"), tags=["misconception"])


@fam("012")
def s11_context(r, L):
    k = pick(r, ["people", "light", "bacteria"])
    if k == "people":
        pop = F(r.randint(11, 99), 10)
        per = r.randint(2, 9)
        e = r.randint(5, 8)
        v = pop * per * F(10) ** (e + 2)
        m, ee = sci_of(v)
        return P(f"A state has about {sci(D(pop), e)} people. Each person uses about {per} × 10² liters of water per day. About how many liters are used per day? Use scientific notation.",
                 f"{sci(m, ee)} liters", [f"({D(pop)} × {per}) × 10{sup(e)}⁺² = {D(pop * per)} × 10{sup(e + 2)}.".replace("⁺²", " · 10²"), f"= {sci(m, ee)} liters."],
                 [f"{sci(D(pop * per) if pop * per < 10 else m, e * 2)} liters", f"{sci(m, ee - 2)} liters", f"{sci(m, ee + 1)} liters"],
                 chk_py("sci_form", expr=f"{D(pop)}*10^{e}*{per}*100"), tags=["modeling"])
    if k == "light":
        dist = F(r.randint(15, 60), 10) * (2 if r.random() < 0.5 else 1)
        e = r.randint(8, 12)
        speed = F(3)
        t = dist / speed * F(10) ** (e - 5)
        need(is_term(t))
        m, ee = sci_of(t)
        return P(f"Light travels about 3 × 10⁵ kilometers per second. How many seconds does light take to travel {sci(D(dist), e)} kilometers? Use scientific notation.",
                 f"{sci(m, ee)} seconds", [f"Time = distance ÷ speed = ({D(dist)} ÷ 3) × 10{sup(e)}⁻⁵.".replace("⁻⁵", " ÷ 10⁵"), f"= {sci(m, ee)} seconds."],
                 [f"{sci(m, e + 5 - 1 if False else ee + 10 - 2 * 5 + 1)} seconds" if False else f"{sci(m, e + 5)} seconds", f"{sci(D(dist * 3) if dist * 3 < 10 else m, ee + 1)} seconds", f"{sci(m, ee - 1)} seconds"],
                 chk_py("sci_form", expr=f"({D(dist)}*10^{e})/(3*10^5)"), tags=["modeling"])
    c = r.randint(2, 9)
    e = r.randint(3, 6)
    k2 = r.randint(2, 4)
    v = F(c) * F(10) ** e * 2 ** k2
    m, ee = sci_of(v)
    return P(f"A culture starts with {sci(c, e)} bacteria and doubles every hour. How many bacteria are there after {k2} hours? Use scientific notation.",
             f"{sci(m, ee)} bacteria", [f"Multiply by 2 for each hour: {c} × 2{sup(k2)} = {c * 2 ** k2}.", f"{c * 2 ** k2} × 10{sup(e)} = {sci(m, ee)}."],
             [f"{sci(D(F(c * 2 * k2)) if c * 2 * k2 < 10 else sci_of(F(c * 2 * k2))[0], e + (0 if c * 2 * k2 < 10 else 1))} bacteria", f"{sci(m, ee + k2)} bacteria", f"{sci(c, e + k2)} bacteria"],
             chk_py("sci_form", expr=f"{c}*10^{e}*2^{k2}"), tags=["modeling"])


@fam("2")
def s11_missing(r, L):
    a = rnd_sci(r)
    x = F(r.randint(2, 9))
    e1, ex = nz(r, -6, 8), nz(r, -6, 8)
    prod = a * x * F(10) ** (e1 + ex)
    pm, pe = sci_of(prod)
    need(len(pm) <= 5)
    return P(f"Find the missing number in scientific notation: (?) × ({sci(D(a), e1)}) = {sci(pm, pe)}", sci(D(x), ex),
             [f"Divide: ({sci(pm, pe)}) ÷ ({sci(D(a), e1)}).", f"{pm} ÷ {D(a)} = {D(F(pm) / a)} and the exponents give the rest.", f"The missing factor is {sci(D(x), ex)}."],
             [sci(D(x), -ex), sci(D(x), pe + e1), sci(D(x), ex + 1)], chk_py("sci_form", expr=f"({pm}*10^({pe}))/({D(a)}*10^({e1}))"), tags=["reasoning", "challenge"])


@fam("012")
def s11_error(r, L):
    a, b = r.randint(2, 4), r.randint(2, 4)
    e1, e2 = r.randint(2, 6), r.randint(2, 6)
    need(e1 * e2 != e1 + e2)
    v = F(a * b) * F(10) ** (e1 + e2)
    m, e = sci_of(v)
    return P(f"Ari computed ({sci(a, e1)})({sci(b, e2)}) = {sci(a * b, e1 * e2)} by multiplying the exponents. What is the correct product in scientific notation?",
             sci(m, e), ["When multiplying powers of 10, add the exponents.", f"{a} × {b} = {a * b}; 10{sup(e1)} · 10{sup(e2)} = 10{sup(e1 + e2)}.", f"Result: {sci(m, e)}."],
             [sci(a * b, e1 * e2) if a * b < 10 else sci(sci_of(F(a * b))[0], e1 * e2 + 1), sci(a + b, e1 + e2), sci(m, e + 1)],
             chk_py("sci_form", expr=f"{a}*10^{e1}*{b}*10^{e2}"), tags=["error-analysis", "misconception"])


@fam("012")
def s11_open(r, L):
    a, b = rnd_sci(r), rnd_sci(r)
    e1, e2 = r.randint(5, 9), r.randint(2, 4)
    va, vb = a * F(10) ** e1, b * F(10) ** e2
    pr, qu = va * vb, va / vb
    need(is_term(qu) and len(sci_of(qu)[0]) <= 7)
    s1, s2 = va + vb, va - vb
    return P(f"Let A = {sci(D(a), e1)} and B = {sci(D(b), e2)}. Write each answer in scientific notation.", None,
             ["Multiply decimals, add exponents.", "Divide decimals, subtract exponents.", "Match powers of 10 before adding.", "Match powers of 10 before subtracting."],
             parts=[("A × B", sci(*sci_of(pr)), chk_py("sci_form", expr=f"{D(a)}*10^{e1}*{D(b)}*10^{e2}")),
                    ("A ÷ B", sci(*sci_of(qu)), chk_py("sci_form", expr=f"({D(a)}*10^{e1})/({D(b)}*10^{e2})")),
                    ("A + B", sci(*sci_of(s1)), chk_py("sci_form", expr=f"{D(a)}*10^{e1}+{D(b)}*10^{e2}")),
                    ("A - B", sci(*sci_of(s2)), chk_py("sci_form", expr=f"{D(a)}*10^{e1}-{D(b)}*10^{e2}"))], tags=["multistep"])


S = "8.NS.A.1"
SKILLS = {
    1: dict(name="Rational numbers", std=["8.NS.A.1"], fams=[s1_classify, s1_between_ints, s1_quotient, s1_between_rational, s1_order, s1_fraction_of_way, s1_mean_between],
            extra=[s1_select, s1_open, s1_error, s1_set_statement]),
    2: dict(name="Operations with rational numbers", std=["7.NS.A.1", "7.NS.A.2", "7.NS.A.3"], fams=[s2_frac_addsub, s2_frac_muldiv, s2_decimal, s2_order_ops, s2_context, s2_missing, s2_open_sign],
            extra=[s2_error, s2_open]),
    3: dict(name="Converting fractions and decimals", std=["8.NS.A.1", "7.NS.A.2.D"], fams=[s3_frac_to_term, s3_dec_to_frac, s3_frac_to_rep, s3_rep_to_frac, s3_compare, s3_which_terminates, s3_context],
            extra=[s3_select, s3_open, s1_error]),
    4: dict(name="Identifying irrational numbers", std=["8.NS.A.1"], fams=[s4_classify, s4_which, s4_perfect_between, s4_count_irr, s4_side_length],
            extra=[s4_select, s4_error, s4_open]),
    5: dict(name="Properties of irrational numbers", std=["8.NS.A.1", "N-RN.B.3"], fams=[s5_result_type, s5_always, s5_counterexample, s5_simplify, s5_irrational_between, s5_solve_for],
            extra=[s5_select, s5_open]),
    6: dict(name="Comparing and ordering irrational numbers", std=["8.NS.A.2"], fams=[s6_compare, s6_order, s6_numberline, s6_count_between, s6_greatest_n],
            extra=[s6_select, s6_open]),
    7: dict(name="Evaluating and approximating square and cube roots", std=["8.EE.A.2", "8.NS.A.2"], fams=[s7_evaluate, s7_between, s7_approx, s7_solve, s7_context, s7_estimate_reverse],
            extra=[s7_error, s7_open]),
    8: dict(name="Negative exponents", std=["8.EE.A.1"], fams=[s8_evaluate, s8_rewrite, s8_as_power, s8_pattern, s8_find_exp, s8_greatest],
            extra=[s8_error, s8_select, s8_open]),
    9: dict(name="Operations with negative exponents", std=["8.EE.A.1"], fams=[s9_numeric, s9_variable, s9_coef, s9_missing, s9_two_var],
            extra=[s9_error, s9_select, s9_open]),
    10: dict(name="Scientific notation", std=["8.EE.A.3"], fams=[s10_to_sci, s10_to_std, s10_compare_times, s10_estimate, s10_normalize, s10_context],
             extra=[s10_error, s10_select, s10_open]),
    11: dict(name="Operations with numbers in scientific notation", std=["8.EE.A.4"], fams=[s11_multiply, s11_divide, s11_addsub, s11_context, s11_missing],
             extra=[s11_error, s11_open]),
}
