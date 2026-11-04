"""Grade 7 Unit 5 — Operations with Fractions (operations-fractions)."""
from glib import *

UNIT_ID = "operations-fractions"
ABBR = "opf"
DENS = [2, 3, 4, 5, 6, 8, 10, 12]


def rfrac(r, dens=DENS, proper=True, neg=False):
    d = pick(r, dens)
    n = r.randint(1, d - 1) if proper else r.randint(d + 1, 4 * d)
    x = F(n, d)
    need(x.denominator == d or not proper)
    return -x if neg and r.random() < 0.5 else x


def M(x):
    """Answer text: simplest fraction or mixed number."""
    return mixed(x)


# ============================================================== S1 Comparing and Ordering
@fam("012")
def s1_compare(r, L):
    a, b = rfrac(r, neg=L == 2), rfrac(r, neg=L == 2)
    need(a != b and a.denominator != b.denominator)
    if L == 1 and r.random() < 0.5:
        sb = D(b) if is_term(b) else N(b)
    else:
        sb = N(b)
    ans = "<" if a < b else ">"
    cd = a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)
    return Q(f"Compare using <, >, or =: {N(a)} ___ {sb}", ans, [f"Use a common denominator of {cd}.", f"{N(a)} = {a.numerator * cd // a.denominator}/{cd} and {N(b)} = {b.numerator * cd // b.denominator}/{cd}.", f"So {N(a)} {ans} {sb}."],
             [x for x in "<>=" if x != ans], PY("cmp", a=N(a), b=sb), mode="sa", why=["Compared only the denominators", ""])


@fam("012")
def s1_order(r, L):
    vals = set()
    while len(vals) < 4:
        vals.add(rfrac(r, neg=L == 2))
    vals = sorted(vals)
    txt = [N(v) if (L == 0 or r.random() < 0.6 or not is_term(v)) else D(v) for v in vals]
    shown = txt[:]
    r.shuffle(shown)
    need(shown != txt and len(set(txt)) == 4)
    by_den = [t for _, t in sorted(zip(vals, txt), key=lambda p: (p[0].denominator, p[0].numerator))]
    return Q(f"Order from least to greatest: {', '.join(shown)}", ", ".join(txt), ["Rewrite with a common denominator or as decimals.", ", ".join(f"{t} = {D(v, 3) if not is_term(v) else D(v)}" for t, v in zip(txt, vals)) + ".", f"Order: {', '.join(txt)}."],
             [", ".join(txt[::-1]), ", ".join(by_den) if by_den != txt else ", ".join(txt[1:] + txt[:1]), ", ".join(sorted(txt))], PY("order", items=txt),
             why=["Ordered from greatest to least", "Ordered by the size of the denominators", "Compared as text"])


@fam("12", mode="mc")
def s1_between(r, L):
    a = rfrac(r)
    b = a + F(1, a.denominator)
    need(b < 1)
    good = (a + b) / 2
    bad = [a - F(1, 2 * a.denominator), b + F(1, 2 * a.denominator), F(a.numerator + 1, a.denominator + 1)]
    need(all(not (a < x < b) for x in bad) and len({good, *bad}) == 4 and all(x > 0 for x in bad))
    opts = [(N(good), True)] + [(N(x), False) for x in bad]
    r.shuffle(opts)
    return Q(f"Which number is between {N(a)} and {N(b)}?", N(good), [f"Rewrite with denominator {2 * a.denominator}: {N(a)} = {2 * a.numerator}/{2 * a.denominator}, {N(b)} = {2 * b.numerator}/{2 * a.denominator}.",
                                                                      f"{N(good)} is between them."], options=opts, chk=PY("strictly_between", lo=N(a), hi=N(b)), mode="mc", tags=["reasoning"])


# ============================================================== S2 Fractions and Decimals
@fam("012")
def s2_to_decimal(r, L):
    d = pick(r, [2, 4, 5, 8, 10, 20, 25] if L == 0 else [3, 6, 9, 11, 12, 8, 16, 40] if L == 1 else [7, 11, 12, 15, 18, 27, 33])
    n = r.randint(1, d - 1) if L < 2 else r.randint(d + 1, 3 * d)
    x = F(n, d)
    need(x.denominator == d or L == 2)
    ans = rep_text(x)
    wr = [D(F(d, n)) if is_term(F(d, n)) else rep_text(F(d, n)), f"{n}.{d}", rep_text(x * 10)]
    return Q(f"Write {N(x)} as a decimal. If it repeats, show the repeating digits.", ans, [f"Divide {n} by {d}.", f"{n} ÷ {d} = {ans}.", "The division " + ("ends." if is_term(x) else "repeats.")],
             wr, PY("rep_dec", expr=N(x)), why=["Divided the denominator by the numerator", "Wrote the numerator and denominator as a decimal", "Misplaced the decimal point"])


@fam("012")
def s2_to_fraction(r, L):
    if L < 2:
        x = F(r.randint(1, 999), 1000) if L else F(r.randint(1, 99), 100)
        need(x.denominator < (1000 if L else 100) or r.random() < 0.3)
        t = D(x)
        raw = F(int(t.split(".")[1]), 10 ** len(t.split(".")[1]))
        return Q(f"Write {t} as a fraction in simplest form.", N(x), [f"{t} = {raw.numerator if False else int(t.split('.')[1])}/{10 ** len(t.split('.')[1])}.", "Divide numerator and denominator by their GCF.", f"{t} = {N(x)}."],
                 [f"{int(t.split('.')[1])}/{10 ** len(t.split('.')[1])}" if f"{int(t.split('.')[1])}/{10 ** len(t.split('.')[1])}" != N(x) else f"{x.numerator}/{x.denominator * 10}",
                  f"{x.denominator}/{x.numerator}" if x.numerator > 1 else f"1/{x.denominator + 1}", f"{int(t.split('.')[1])}/{10 ** (len(t.split('.')[1]) + 1)}"],
                 PY("frac_simplest", expr=N(x), mixed=False), why=["Did not simplify", "Flipped the fraction", "Used the wrong power of 10"])
    a = r.randint(1, 9)
    x = F(a, 9) if r.random() < 0.5 else F(r.randint(10, 98), 99)
    need(x.denominator in (3, 9, 11, 33, 99))
    t = rep_text(x)
    return Q(f"Write the repeating decimal {t} as a fraction in simplest form.", N(x), ["Let n equal the decimal.", "Multiply by 10 (one repeating digit) or 100 (two repeating digits) and subtract n.", f"Solve and simplify: {N(x)}."],
             [N(x * 9 / 10), N(F(x.numerator * 10, x.denominator * 10 + 1)), N(x + F(1, 10))], PY("frac_simplest", expr=N(x), mixed=False),
             why=["Wrote the digits over a power of 10", "", ""], tags=["reasoning"])


@fam("12", mode="mc")
def s2_terminates(r, L):
    good = pick(r, [F(n, d) for d in (8, 16, 20, 25, 40, 50, 80) for n in (1, 3, 7, 9) if math.gcd(n, d) == 1])
    bad = r.sample([F(n, d) for d in (3, 6, 7, 9, 11, 12, 15) for n in (1, 2, 4, 5) if math.gcd(n, d) == 1], 3)
    ask = "terminating"
    opts = [(N(good), True)] + [(N(b), False) for b in bad]
    r.shuffle(opts)
    return Q("Which fraction is equal to a terminating decimal?", N(good), ["A fraction in simplest form terminates only if its denominator has no prime factors other than 2 and 5.",
                                                                           f"{N(good)} = {D(good)}."], options=opts, chk=PY("terminates"), mode="mc", tags=["reasoning"])


# ============================================================== S3 Adding and Subtracting Fractions
@fam("012")
def s3_addsub(r, L):
    if L == 0:
        d = pick(r, DENS)
        a, b = F(r.randint(1, d - 1), d), F(r.randint(1, d - 1), d)
        op = pick(r, ["+", "-"])
        if op == "-" and a < b:
            a, b = b, a
        need(a != b)
        sa, sb = N(a) if a.denominator == d else f"{a.numerator * d // a.denominator}/{d}", N(b) if b.denominator == d else f"{b.numerator * d // b.denominator}/{d}"
        sa, sb = f"{int(a * d)}/{d}", f"{int(b * d)}/{d}"
    elif L == 1:
        a, b = rfrac(r), rfrac(r)
        need(a.denominator != b.denominator)
        op = pick(r, ["+", "-"])
        sa, sb = N(a), N(b)
    else:
        a = F(r.randint(1, 6)) + rfrac(r)
        b = F(r.randint(1, 5)) + rfrac(r)
        need(a.denominator != b.denominator or r.random() < 0.3)
        op = pick(r, ["+", "-"])
        if op == "-" and a < b:
            a, b = b, a
        sa, sb = M(a), M(b)
    v = a + b if op == "+" else a - b
    need(v != 0)
    na, nb = a.numerator * (1 if True else 1), b.numerator
    nd = F(int(a * a.denominator) + (1 if op == "+" else -1) * int(b * b.denominator), a.denominator + b.denominator) if a.denominator + b.denominator else F(0)
    wr = [M(nd) if nd != v and nd > 0 else M(v + 1), M(a - b if op == "+" else a + b), M(v * 2)]
    if L == 0:
        wr[0] = f"{int((a + b if op == '+' else a - b) * a.denominator)}/{2 * a.denominator}" if a.denominator == b.denominator else wr[0]
    cd = a.denominator * b.denominator // math.gcd(a.denominator, b.denominator)
    return Q(f"{'Add' if op == '+' else 'Subtract'}. Write the answer in simplest form: {sa} {op} {sb}", M(v),
             [f"Use a common denominator: {cd}." if a.denominator != b.denominator else "The denominators are already the same.", f"{'Add' if op == '+' else 'Subtract'} the numerators and keep the denominator.",
              "Rename improper fractions as mixed numbers when needed." if L == 2 else "Simplify if possible.", f"Answer: {M(v)}."],
             wr, PY("frac_simplest", expr=f"({N(a)}) {op} ({N(b)})"), why=["Added (or subtracted) both the numerators and the denominators" if L else "Added the denominators too", "Used the wrong operation", ""])


@fam("012")
def s3_context(r, L):
    nm = name(r)
    a = F(r.randint(1, 3)) + rfrac(r, [2, 4, 8]) if L else rfrac(r, [4, 8])
    b = rfrac(r, [2, 3, 4, 8]) + (F(r.randint(1, 2)) if L == 2 else 0)
    ctx = pick(r, [("walked {a} miles in the morning and {b} miles in the afternoon. How many miles did {nm} walk in all?", "+"),
                   ("had {a} cups of flour and used {b} cups. How many cups are left?", "-"),
                   ("needs a board {a} feet long and cuts {b} feet off a longer board. How much longer is the needed board than the piece cut?", "-")])
    t, op = ctx
    if op == "-" and a <= b:
        a, b = b + rfrac(r, [2, 4]), a
    v = a + b if op == "+" else a - b
    need(v > 0)
    return Q(f"{nm} " + t.format(a=M(a), b=M(b), nm=nm), M(v), [f"Write the expression: {M(a)} {op} {M(b)}.", "Use a common denominator.", f"Result: {M(v)}."],
             [M(a - b if op == "+" else a + b), M(F(a.numerator + b.numerator, a.denominator + b.denominator)), M(v + F(1, 2))], PY("frac_simplest", expr=f"({N(a)}) {op} ({N(b)})"),
             why=["Used the wrong operation", "Added numerators and denominators", ""], tags=["modeling"])


@fam("2")
def s3_missing(r, L):
    a, s = rfrac(r), rfrac(r, [6, 8, 10, 12])
    x = s - a
    need(x > 0)
    return Q(f"What fraction n makes the equation true? {N(a)} + n = {N(s)}", M(x), [f"n = {N(s)} - {N(a)}.", "Use a common denominator and subtract.", f"n = {M(x)}."],
             [M(s + a), M(F(s.numerator - a.numerator, abs(s.denominator - a.denominator) or 1)) if s.numerator > a.numerator else M(x + F(1, s.denominator)), M(x * 2)],
             PY("frac_simplest", expr=f"{N(s)} - {N(a)}"), why=["Added instead of subtracting", "Subtracted numerators and denominators", ""], tags=["reasoning"])


# ============================================================== S4 Multiplying and Dividing Fractions
@fam("012")
def s4_muldiv(r, L):
    op = pick(r, ["×", "÷"])
    if L == 0:
        a, b = rfrac(r), rfrac(r) if op == "×" else F(r.randint(2, 6))
    elif L == 1:
        a, b = rfrac(r), rfrac(r)
    else:
        a = F(r.randint(1, 4)) + rfrac(r)
        b = F(r.randint(1, 3)) + rfrac(r) if r.random() < 0.7 else -rfrac(r)
    v = a * b if op == "×" else a / b
    sa, sb = M(a), (f"({M(b)})" if b < 0 else M(b))
    if op == "×":
        wr = [M(a / b), M(F(a.numerator * b.numerator, a.denominator + b.denominator)) if a.denominator + b.denominator else M(v + 1), M(F(int(a) * int(b)) + (a - int(a)) * (b - int(b))) if L == 2 else M(a + b)]
        why = ["Divided instead of multiplying", "Added the denominators", "Multiplied whole parts and fraction parts separately" if L == 2 else "Added instead of multiplying"]
        st = ["Rewrite mixed numbers as improper fractions." if L == 2 else "Multiply numerators and multiply denominators.", f"{N(a)} × {N(b)} = {N(v)}.", "Simplify (cross-cancel when possible).", f"Answer: {M(v)}."]
    else:
        wr = [M(F(1) / v), M(a * b), M(F(a.numerator, b.numerator) / F(a.denominator, b.denominator)) if F(a.numerator, b.numerator) / F(a.denominator, b.denominator) != v else M(v + 1)]
        why = ["Flipped the first fraction instead of the second", "Multiplied without using the reciprocal", ""]
        st = ["Rewrite mixed numbers as improper fractions." if L == 2 else "Keep the first fraction.", f"Multiply by the reciprocal of {N(b)}: {N(1 / b)}.", f"{N(a)} × {N(1 / b)} = {N(v)}.", f"Answer: {M(v)}."]
    return Q(f"{'Multiply' if op == '×' else 'Divide'}. Write the answer in simplest form: {sa} {op} {sb}", M(v), st, wr, PY("frac_simplest", expr=f"({N(a)}) {'*' if op == '×' else '÷'} ({N(b)})"), why=why)


@fam("012")
def s4_context(r, L):
    nm = name(r)
    if r.random() < 0.5:
        tot = F(r.randint(2, 8)) + (rfrac(r, [2, 4]) if L else 0)
        each = rfrac(r, [2, 3, 4, 8])
        v = tot / each
        need(v.denominator == 1 or L == 2)
        return Q(f"{nm} has {M(tot)} pounds of trail mix and puts {M(each)} pound in each bag. How many bags can {nm} fill?", M(v),
                 [f"Divide: {M(tot)} ÷ {M(each)}.", f"Multiply by the reciprocal: {N(tot)} × {N(1 / each)}.", f"= {M(v)} bags."], [M(tot * each), M(each / tot), M(v + 1)],
                 PY("frac_simplest", expr=f"({N(tot)}) ÷ ({N(each)})"), why=["Multiplied instead of dividing", "Divided in the wrong order", ""], tags=["modeling"])
    a = rfrac(r, [2, 3, 4, 5])
    b = F(r.randint(2, 6) * a.denominator) if L == 0 else F(r.randint(2, 9)) + rfrac(r, [2, 4])
    v = a * b
    return Q(f"A recipe calls for {M(b)} cups of water. {nm} makes {N(a)} of the recipe. How many cups of water are needed?", M(v),
             [f"Find {N(a)} of {M(b)}: multiply.", f"{N(a)} × {N(b)} = {N(v)}.", f"= {M(v)} cups."], [M(b / a), M(b - a), M(v + F(1, 2))], PY("frac_simplest", expr=f"({N(a)}) * ({N(b)})"),
             why=["Divided instead of multiplying", "Subtracted instead of multiplying", ""], tags=["modeling"])


@fam("12", mode="mc")
def s4_estimate(r, L):
    a = rfrac(r, [8, 10, 12])
    b = F(r.randint(10, 40))
    v = a * b
    opts = [("less than " + N(b), True), ("greater than " + N(b), False), ("equal to " + N(b), False), ("cannot be determined", False)]
    r.shuffle(opts)
    return Q(f"Without calculating, is {N(a)} × {N(b)} greater than, less than, or equal to {N(b)}?", "less than " + N(b),
             [f"{N(a)} is less than 1.", "Multiplying a positive number by a number less than 1 gives a smaller product.", f"({N(a)} × {N(b)} = {M(v)})"],
             options=opts, chk=PY("size_claim", expr=f"{N(a)}*{N(b)}", ref=N(b)), mode="mc", tags=["reasoning"])


# ============================================================== S5 Customary units
CUST = {"length": [("miles", 5280 * 12), ("yards", 36), ("feet", 12), ("inches", 1)], "capacity": [("gallons", 128), ("quarts", 32), ("pints", 16), ("cups", 8), ("fluid ounces", 1)],
        "weight": [("tons", 32000), ("pounds", 16), ("ounces", 1)]}


@fam("012")
def s5_convert(r, L):
    kind = pick(r, list(CUST))
    units = CUST[kind] if L == 2 else [u for u in CUST[kind] if u[0] not in ("miles", "tons")]
    (a, fa), (b, fb) = r.sample(units, 2)
    need(F(fa, fb) <= 1760 * 3 if L < 2 else True)
    x = F(r.randint(2, 12)) if L == 0 else F(r.randint(1, 9)) + pick(r, [F(1, 2), F(1, 4), F(3, 4)])
    if L == 0:
        need(fa > fb)
    v = x * fa / fb
    need(v.denominator <= 16 and (L > 0 or v.denominator == 1))
    return Q(f"Convert {M(x)} {a} to {b}.", f"{M(v)} {b}", [f"1 {a[:-1] if not a.startswith('fluid') else 'fluid ounce'} = {M(F(fa, fb))} {b}." if fa > fb else f"1 {b[:-1]} = {M(F(fb, fa))} {a}.",
                                                          f"{'Multiply' if fa > fb else 'Divide'}: {M(x)} {'×' if fa > fb else '÷'} {M(F(fa, fb) if fa > fb else F(fb, fa))}.", f"= {M(v)} {b}."],
             [f"{M(x * fb / fa)} {b}", f"{M(v + 1)} {b}", f"{M(x)} {b}"], V(f"({N(x)})*{fa}/{fb}"), why=["Multiplied and divided the wrong way", "", "Did not convert"])


@fam("12")
def s5_compare(r, L):
    a, b = r.randint(2, 9), r.randint(10, 40)
    x = a * 12
    ans = "<" if x < b * 1 * 12 // 12 * 12 // 12 * 1 else ">"
    ft, inch = a, b + r.randint(-6, 6) + 12 * (a - 1)
    v1, v2 = ft * 12, inch
    need(v1 != v2)
    ans = "<" if v1 < v2 else ">"
    return Q(f"Compare using <, >, or =: {ft} feet ___ {inch} inches", ans, [f"{ft} feet = {ft} × 12 = {v1} inches.", f"Compare {v1} inches and {inch} inches.", f"{ft} feet {ans} {inch} inches."],
             [x for x in "<>=" if x != ans], PY("cmp", a=f"{ft}*12", b=str(inch)), mode="sa", why=["Compared without converting units", ""])


@fam("2")
def s5_multi(r, L):
    gal = r.randint(2, 5)
    cup = pick(r, [F(1, 2), F(3, 4), F(1)])
    n = gal * 16 / cup
    need(n.denominator == 1)
    return Q(f"How many {M(cup)}-cup servings are in {gal} gallons of juice?", f"{int(n)} servings", [f"1 gallon = 16 cups, so {gal} gallons = {gal * 16} cups.", f"{gal * 16} ÷ {M(cup)} = {int(n)}.", f"{int(n)} servings."],
             [f"{M(gal * 16 * cup)} servings", f"{M(gal * 4 / cup)} servings", f"{M(gal / cup)} servings"], V(f"{gal}*16 ÷ {N(cup)}"),
             why=["Multiplied instead of dividing", "Used 4 cups per gallon", "Did not convert gallons to cups"], tags=["multistep", "modeling"])


# ============================================================== S6 / S7 fraction equations
VARS = ["x", "n", "y", "m", "k"]


@fam("012")
def s6_solve(r, L):
    v = pick(r, VARS)
    a, x = rfrac(r), rfrac(r) if L < 2 else rfrac(r) + F(r.randint(1, 3))
    if L == 0:
        d = pick(r, DENS)
        a, x = F(r.randint(1, d - 1), d), F(r.randint(1, d - 1), d)
    op = pick(r, ["+", "-"])
    rhs = x + a if op == "+" else x - a
    need(rhs != 0 and (L == 2 or rhs > 0))
    eq = f"{v} {op} {N(a)} = {N(rhs)}"
    sol = x
    return Q(f"Solve: {eq}", f"{v} = {M(sol)}", [f"{'Subtract' if op == '+' else 'Add'} {N(a)} on both sides.", "Use a common denominator.", f"{v} = {M(sol)}.", "Check by substituting."],
             [f"{v} = {M(rhs + a if op == '+' else rhs - a)}", f"{v} = {M(rhs)}", f"{v} = {M(-sol)}"], EQ(eq, v), why=["Used the same operation instead of the inverse", "Gave the right side", "Made a sign error"])


@fam("012")
def s6_context(r, L):
    nm = name(r)
    a, x = rfrac(r, [2, 4, 8]) + F(r.randint(0, 2)), rfrac(r, [2, 4, 8]) + F(r.randint(1, 3))
    return Q(f"{nm}'s puppy gained {M(a)} pounds this month and now weighs {M(x + a)} pounds. Solve w + {M(a)} = {M(x + a)} to find w, its weight last month.", f"w = {M(x)}",
             [f"Subtract {M(a)} from both sides.", f"w = {M(x + a)} - {M(a)}.", f"w = {M(x)}."], [f"w = {M(x + 2 * a)}", f"w = {M(x + a)}", f"w = {M(x + F(1, 4))}"], EQ(f"w + {N(a)} = {N(x + a)}", "w"),
             why=["Added instead of subtracting", "Gave the current weight", ""], tags=["modeling"])


@fam("012")
def s7_solve(r, L):
    v = pick(r, VARS)
    c = rfrac(r, [2, 3, 4, 5, 6, 8])
    if L == 2 and r.random() < 0.5:
        c = -c
    x = F(r.randint(1, 12) * c.denominator) if L == 0 else rfrac(r) + F(r.randint(0, 4))
    rhs = c * x
    eq = f"({N(c)}){v} = {N(rhs)}" if c.numerator != 1 or L else f"{v}/{c.denominator} = {N(rhs)}"
    return Q(f"Solve: {eq}", f"{v} = {M(x)}", [f"Multiply both sides by the reciprocal of {N(c)}, which is {N(1 / c)}.", f"{v} = {N(rhs)} × {N(1 / c)}.", f"{v} = {M(x)}.", "Check by substituting."],
             [f"{v} = {M(rhs * c)}", f"{v} = {M(rhs - c)}", f"{v} = {M(-x)}"], EQ(eq, v), why=["Multiplied by the fraction instead of its reciprocal", "Subtracted instead of dividing", "Made a sign error"])


@fam("012")
def s7_context(r, L):
    c = rfrac(r, [2, 3, 4, 5, 8])
    x = F(r.randint(2, 15) * c.denominator)
    nm = name(r)
    return Q(f"{nm} has read {N(c)} of a book, which is {int(c * x)} pages. Solve ({N(c)})p = {int(c * x)} to find p, the total number of pages.", f"p = {int(x)}",
             [f"Multiply both sides by {N(1 / c)}.", f"p = {int(c * x)} × {N(1 / c)}.", f"p = {int(x)}."], [f"p = {M(c * x * c)}", f"p = {M(c * x - c)}", f"p = {int(c * x) * c.denominator}"],
             EQ(f"({N(c)})p = {int(c * x)}", "p"), why=["Multiplied by the fraction instead of its reciprocal", "Subtracted the fraction", "Multiplied by the denominator only"], tags=["modeling"])


# ============================================================== S8 Powers of products and quotients
@fam("012")
def s8_numeric(r, L):
    a = rfrac(r, [2, 3, 4, 5]) if L < 2 else -rfrac(r, [2, 3, 5])
    e = r.randint(2, 3) if L < 2 else r.randint(2, 4)
    t = f"({N(a)}){sup(e)}"
    v = a ** e
    return Q(f"Evaluate: {t}", N(v), [f"Raise the numerator and the denominator to the power {e}.", f"{a.numerator}{sup(e)} = {a.numerator ** e} and {a.denominator}{sup(e)} = {a.denominator ** e}." if a > 0 else "A negative base with an even exponent is positive; with an odd exponent it is negative.",
                                     f"{t} = {N(v)}."], [N(F(a.numerator ** e, a.denominator)), N(F(a.numerator * e, a.denominator * e)) if a.numerator * e != a.denominator * e else N(v + 1), N(-v)],
             V(t), why=["Raised only the numerator to the power", "Multiplied by the exponent", "Made a sign error"])


@fam("012")
def s8_product(r, L):
    v = pick(r, ["x", "y", "m"])
    c, e = r.randint(2, 5), r.randint(2, 3)
    if L == 0:
        t = f"({c}{v}){sup(e)}"
        ans = f"{c ** e}{v}{sup(e)}"
        wr = [f"{c}{v}{sup(e)}", f"{c * e}{v}{sup(e)}", f"{c ** e}{v}"]
        why = ["Did not raise the coefficient to the power", "Multiplied the coefficient by the exponent", "Did not raise the variable to the power"]
    elif L == 1:
        k = r.randint(2, 4)
        t = f"({c}{v}{sup(k)}){sup(e)}"
        ans = f"{c ** e}{v}{sup(k * e)}"
        wr = [f"{c ** e}{v}{sup(k + e)}", f"{c * e}{v}{sup(k * e)}", f"{c}{v}{sup(k * e)}"]
        why = ["Added the exponents", "Multiplied the coefficient by the exponent", "Did not raise the coefficient"]
    else:
        w = "y" if v != "y" else "x"
        t = f"({v}/{c}){sup(e)}" if r.random() < 0.5 else f"(-{c}{v}{w}{sup(2)}){sup(e)}"
        if "/" in t:
            ans = f"{v}{sup(e)}/{c ** e}"
            wr = [f"{v}{sup(e)}/{c}", f"{v}{sup(e)}/{c * e}", f"{v}/{c ** e}"]
        else:
            ans = f"{'-' if e % 2 else ''}{c ** e}{v}{sup(e)}{w}{sup(2 * e)}"
            wr = [f"{'' if e % 2 else '-'}{c ** e}{v}{sup(e)}{w}{sup(2 * e)}", f"{'-' if e % 2 else ''}{c ** e}{v}{sup(e)}{w}{sup(2 + e)}", f"{'-' if e % 2 else ''}{c}{v}{sup(e)}{w}{sup(2 * e)}"]
        why = ["Raised only the numerator" if "/" in t else "Made a sign error", "Multiplied by the exponent" if "/" in t else "Added the exponents", "Did not raise the variable" if "/" in t else "Did not raise the coefficient"]
    vars_ = sorted(set(re.findall(r"[a-z]", t)))
    return Q(f"Simplify: {t}", ans, ["Raise each factor inside the parentheses to the power.", "Multiply exponents when raising a power to a power.", f"{t} = {ans}."], wr, EQV(t, vars_), why=why)


@fam("12")
def s8_area(r, L):
    a = rfrac(r, [2, 3, 4, 5])
    return Q(f"A square has side length {N(a)} meter. What is its area?", f"{N(a * a)} square meters", [f"Area = s².", f"({N(a)})² = {a.numerator ** 2}/{a.denominator ** 2}.", f"= {N(a * a)} square meters."],
             [f"{N(a * 2)} square meters", f"{N(F(a.numerator ** 2, a.denominator))} square meters", f"{N(4 * a)} square meters"], V(f"({N(a)})^2"),
             why=["Multiplied by 2 instead of squaring", "Squared only the numerator", "Found the perimeter"], tags=["connections"])


SKILLS = {
    1: dict(name="Comparing and Ordering Rational Numbers", std=["7.NS.A.2d", "6.NS.C.7a"], fams=[s1_compare, s1_order, s1_between], extra=[err_of(s1_order), open_of(s1_compare)]),
    2: dict(name="Fractions and Decimals", std=["7.NS.A.2d"], fams=[s2_to_decimal, s2_to_fraction, s2_terminates], extra=[err_of(s2_to_decimal), open_of(s2_to_decimal), err_of(s2_to_fraction)]),
    3: dict(name="Adding and Subtracting Fractions", std=["5.NF.A.1", "7.NS.A.1d"], fams=[s3_addsub, s3_context, s3_missing], extra=[err_of(s3_addsub), open_of(s3_addsub), select_of(s3_addsub)]),
    4: dict(name="Multiplying and Dividing Fractions", std=["6.NS.A.1", "7.NS.A.2"], fams=[s4_muldiv, s4_context, s4_estimate], extra=[err_of(s4_muldiv), open_of(s4_muldiv), select_of(s4_muldiv)]),
    5: dict(name="Using Customary Units of Measurement", std=["5.MD.A.1", "6.RP.A.3d"], fams=[s5_convert, s5_compare, s5_multi], extra=[err_of(s5_convert), open_of(s5_convert), select_of(s5_convert)]),
    6: dict(name="Solving Equations by Adding or Subtracting Fractions", std=["7.EE.B.4a", "7.NS.A.1"], fams=[s6_solve, s6_context], extra=[err_of(s6_solve), open_of(s6_solve), select_of(s6_solve)]),
    7: dict(name="Solving Equations by Multiplying Fractions", std=["7.EE.B.4a", "7.NS.A.2"], fams=[s7_solve, s7_context], extra=[err_of(s7_solve), open_of(s7_solve), select_of(s7_solve)]),
    8: dict(name="Powers of Products and Quotients", std=["8.EE.A.1"], fams=[s8_numeric, s8_product, s8_area], extra=[err_of(s8_product), open_of(s8_numeric), select_of(s8_numeric)]),
}
