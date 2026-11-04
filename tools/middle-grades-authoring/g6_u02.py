"""Grade 6 Unit 2 — Operations of Fractions and Decimals (fractions-decimals-operations)."""
from glib import *
import g7_u04 as X7, g7_u03 as D7

UNIT_ID = "fractions-decimals-operations"
ABBR = "fdo"


def rf(r, dens=(2, 3, 4, 5, 6, 8, 10, 12)):
    d = pick(r, dens)
    return F(r.randint(1, d - 1), d)


def div_item(a, b, sa, sb, ctx=None):
    v = a / b
    st = [f"Keep {sa}, change ÷ to ×, and use the reciprocal of {sb}: {N(1 / b)}." if b.denominator > 1 or b.numerator > 1 else f"Multiply by the reciprocal of {sb}.",
          f"{N(a)} × {N(1 / b)} = {N(v)}.", "Simplify (rename as a mixed number if needed).", f"Answer: {mixed(v)}."]
    wr = [mixed(a * b), mixed(b / a), mixed(F(a.numerator * b.denominator, 1) / F(a.denominator * b.numerator, 1) * 0 + F(a.numerator // b.numerator if b.numerator and a.numerator % b.numerator == 0 else a.numerator + 1, max(1, a.denominator // b.denominator if b.denominator and a.denominator % b.denominator == 0 else a.denominator + b.denominator)))]
    why = ["Multiplied without using the reciprocal", "Flipped the first fraction instead of the second", "Divided numerators and denominators separately"]
    return Q(ctx or f"Divide. Write the answer in simplest form: {sa} ÷ {sb}", mixed(v), st, wr, PY("frac_simplest", expr=f"({N(a)}) ÷ ({N(b)})"), why=why, tags=["modeling"] if ctx else [])


# ============================================================== S1 Dividing Fractions
@fam("012")
def s1_div(r, L):
    a, b = rf(r, (2, 3, 4, 5, 6, 8) if L == 0 else (2, 3, 4, 5, 6, 8, 9, 10, 12)), rf(r, (2, 3, 4, 5, 6, 8) if L == 0 else (2, 3, 4, 5, 6, 8, 9, 10, 12))
    need(a != b)
    if L == 0:
        need(a.denominator == b.denominator or b.numerator == 1)
    return div_item(a, b, N(a), N(b))


@fam("012")
def s1_context(r, L):
    a, b = rf(r, (2, 3, 4, 6, 8)), rf(r, (2, 3, 4, 6, 8))
    need((a / b).denominator <= 4 and a != b)
    nm = name(r)
    t = pick(r, [f"{nm} has {N(a)} of a pizza and shares it so each person gets {N(b)} of a pizza. How many servings is that?",
                 f"A ribbon is {N(a)} yard long. How many {N(b)}-yard pieces can be cut from it?",
                 f"{nm} walked {N(a)} mile in {N(b)} hour. What is {nm}'s speed in miles per hour?"])
    return div_item(a, b, N(a), N(b), ctx=t)


@fam("12", mode="mc")
def s1_model(r, L):
    a, b = rf(r, (2, 3, 4, 6)), rf(r, (2, 3, 4, 6, 8, 12))
    need(b < a)
    good = f"How many {N(b)}s are in {N(a)}?"
    opts = [(good, True), (f"How many {N(a)}s are in {N(b)}?", False), (f"What is {N(b)} of {N(a)}?", False), (f"What is {N(a)} more than {N(b)}?", False)]
    r.shuffle(opts)
    return Q(f"Which question does {N(a)} ÷ {N(b)} answer?", good, ["a ÷ b asks how many groups of size b fit into a.", f"{N(a)} ÷ {N(b)} = {mixed(a / b)}."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


# ============================================================== S2 Whole numbers and fractions
@fam("012")
def s2_div(r, L):
    w = F(r.randint(2, 12))
    f_ = rf(r, (2, 3, 4, 5, 6, 8) if L < 2 else (3, 5, 7, 9, 10, 12))
    if r.random() < 0.6:
        return div_item(w, f_, N(w), N(f_))
    return div_item(f_, w, N(f_), N(w))


@fam("012")
def s2_context(r, L):
    w = r.randint(2, 12)
    f_ = rf(r, (2, 3, 4, 8))
    nm = name(r)
    if r.random() < 0.5:
        return div_item(F(w), f_, str(w), N(f_), ctx=f"{nm} has {w} cups of trail mix. Each bag holds {N(f_)} cup. How many bags can {nm} fill?")
    return div_item(f_, F(w), N(f_), str(w), ctx=f"{N(f_)} of a pan of brownies is shared equally among {w} friends. What fraction of the whole pan does each friend get?")


# ============================================================== S3 Mixed numbers
@fam("012")
def s3_div(r, L):
    a = F(r.randint(1, 5)) + rf(r, (2, 3, 4, 5, 8))
    b = (F(r.randint(1, 3)) + rf(r, (2, 3, 4))) if L else rf(r, (2, 3, 4, 8))
    need(a != b)
    return div_item(a, b, mixed(a), mixed(b))


@fam("12")
def s3_context(r, L):
    a = F(r.randint(3, 12)) + pick(r, [F(1, 2), F(1, 4), F(3, 4)])
    b = F(r.randint(1, 2)) + pick(r, [F(1, 2), F(1, 4), F(1, 3)])
    nm = name(r)
    return div_item(a, b, mixed(a), mixed(b), ctx=f"A board is {mixed(a)} feet long. {nm} cuts it into pieces that are each {mixed(b)} feet long. How many pieces are there (including a partial piece as a fraction)?")


# ============================================================== S4 Dividing Multi-Digit Numbers
@fam("012")
def s4_divide(r, L):
    d = r.randint(3, 9) if L == 0 else r.randint(12, 48)
    q = r.randint(20, 200) if L < 2 else r.randint(100, 999)
    rem = 0 if L == 0 else r.randint(0, d - 1)
    n = d * q + rem
    if L == 2 and rem:
        v = F(n, d)
        need(is_term(v))
        return Q(f"Divide. Write the quotient as a decimal: {n:,} ÷ {d}", D(v), [f"Divide: {n} ÷ {d} = {q} R{rem}.", f"Continue dividing by writing zeros after the decimal point.", f"{n:,} ÷ {d} = {D(v)}."],
                 [f"{q}.{rem}", D(v * 10), str(q)], V(f"{n} ÷ {d}"), why=["Wrote the remainder as the decimal part", "Misplaced the decimal point", "Dropped the remainder"])
    ans = f"{q} R{rem}" if rem else str(q)
    return Q(f"Divide: {n:,} ÷ {d}" + (" (write any remainder as R)" if L else ""), ans, ["Use long division: divide, multiply, subtract, bring down.", f"{d} × {q} = {d * q}" + (f", remainder {rem}" if rem else "") + ".", f"Answer: {ans}."],
             [f"{q + 1}" + (f" R{rem}" if rem else ""), f"{q} R{rem + 1}" if rem else str(q * 10), f"{q - 1} R{rem + d}" if rem else str(q - 1)], PY("long_div", n=n, d=d),
             why=["Made a subtraction error in one step", "Made an error in the last step", "Did not finish dividing"])


@fam("012")
def s4_context(r, L):
    d = r.randint(12, 60)
    q = r.randint(10, 99)
    rem = r.randint(1, d - 1)
    n = d * q + rem
    kind = pick(r, ["up", "down"])
    if kind == "up":
        return Q(f"{n:,} students are going on a trip. Each bus holds {d} students. How many buses are needed?", str(q + 1),
                 [f"{n:,} ÷ {d} = {q} R{rem}.", f"The remaining {rem} students still need a bus.", f"{q + 1} buses."], [str(q), f"{q} R{rem}", str(q + 2)], PY("conds", vars=["b"], conds=[f"b*{d} ≥ {n}", f"(b - 1)*{d} < {n}"]),
                 why=["Ignored the remainder", "Gave the remainder instead of interpreting it", ""], tags=["modeling", "reasoning"])
    return Q(f"A factory packs {n:,} eggs into cartons of {d}. How many full cartons can it pack?", str(q), [f"{n:,} ÷ {d} = {q} R{rem}.", "Only full cartons count, so drop the remainder.", f"{q} full cartons."],
             [str(q + 1), f"{q} R{rem}", str(rem)], PY("conds", vars=["c"], conds=[f"c*{d} ≤ {n}", f"(c + 1)*{d} > {n}"]), why=["Rounded up instead of down", "Gave the remainder form", "Gave the remainder"], tags=["modeling"])


# ============================================================== S5 / S6 decimals
def rd(r, lo, hi, pl):
    while True:
        v = F(r.randint(int(lo * 10 ** pl), int(hi * 10 ** pl)), 10 ** pl)
        if (v * 10 ** pl) % 10:
            return v


@fam("012")
def s5_addsub(r, L):
    a, b = rd(r, 1, 999 if L else 99, r.randint(1, 3)), rd(r, 1, 999 if L else 99, r.randint(1, 3))
    op = pick(r, ["+", "-"])
    if op == "-" and a < b:
        a, b = b, a
    if L == 2:
        c = rd(r, 1, 99, 2)
        e = f"{D(a)} {op} {D(b)} + {D(c)}"
        v = (a + b if op == "+" else a - b) + c
    else:
        e = f"{D(a)} {op} {D(b)}"
        v = a + b if op == "+" else a - b
    sa, sb = D(a).split("."), D(b).split(".")
    mis = F(int(sa[0] + (sa[1] if len(sa) > 1 else "")) + (1 if op == "+" else -1) * int(sb[0] + (sb[1] if len(sb) > 1 else "")), 10 ** max(len(sa[1]) if len(sa) > 1 else 0, len(sb[1]) if len(sb) > 1 else 0))
    return Q(f"{'Compute' if L == 2 else 'Add' if op == '+' else 'Subtract'}: {e}", D(v), ["Line up the decimal points.", "Write zeros so the numbers have the same number of decimal places.", f"{'Add' if op == '+' else 'Subtract'} as with whole numbers.", f"Answer: {D(v)}."],
             [D(mis) if mis != v and mis > 0 else D(v + F(1, 10)), D(v * 10), D(a - b if op == "+" else a + b)], V(e), why=["Lined up the last digits instead of the decimal points", "Misplaced the decimal point", "Used the wrong operation"])


@fam("012")
def s6_muldiv(r, L):
    if r.random() < 0.5:
        a, b = rd(r, 1, 50, r.randint(1, 2)), rd(r, 0.1, 20 if L else 9, 1)
        v = a * b
        e = f"{D(a)} × {D(b)}"
        dp = len(D(a).split(".")[1]) + len(D(b).split(".")[1])
        wr = [D(v * 10), D(v / 10), D(F(int(D(a).replace(".", "")) * int(D(b).replace(".", "")), 10 ** max(len(D(a).split(".")[1]), len(D(b).split(".")[1]))))]
        st = ["Multiply as whole numbers.", f"Count decimal places in the factors: {dp}.", f"Place the decimal point {dp} places from the right: {D(v)}."]
        why = ["Placed the decimal point one place too far right", "Placed the decimal point one place too far left", "Counted decimal places from only one factor"]
    else:
        b = rd(r, 0.2, 9, 1 if L < 2 else 2)
        q = rd(r, 1, 90, 1) if L else F(r.randint(2, 90))
        a = b * q
        need(is_term(a))
        v = q
        e = f"{D(a)} ÷ {D(b)}"
        k = 10 ** len(D(b).split(".")[1])
        st = [f"Multiply the divisor and the dividend by {k} to make the divisor a whole number.", f"{D(a * k)} ÷ {D(b * k)}.", f"Divide: {D(v)}."]
        wr = [D(v / 10), D(v * 10), D(a / b / k) if is_term(a / b / k) else D(v + 1)]
        why = ["Moved the decimal point only in the divisor", "Moved the decimal point one extra place", "Moved the decimal point the wrong way"]
    need(all(norm_key(w) != norm_key(D(v)) for w in wr))
    return Q(f"Compute: {e}", D(v), st, wr, V(e), why=why)


@fam("012")
def s6_context(r, L):
    p, n = rd(r, 0.5, 9, 2), r.randint(2, 12) if L < 2 else rd(r, 1, 9, 1)
    nm = name(r)
    if r.random() < 0.5:
        tot = p * n
        return Q(f"Apples cost ${Rd(p, 2)} per pound. {nm} buys {D(F(n))} pounds. How much does {nm} pay, to the nearest cent?", f"${Rd(tot, 2)}", [f"{Rd(p, 2)} × {D(F(n))} = {D(tot)}.", f"≈ ${Rd(tot, 2)}."],
                 [f"${Rd(tot * 10, 2)}", f"${Rd(p + F(n), 2)}", f"${Rd(tot / 10, 2)}"], AP(f"{D(p)}*{D(F(n))}", 2), why=["Misplaced the decimal point", "Added instead of multiplying", "Misplaced the decimal point"], tags=["modeling"])
    tot = p * r.randint(2, 9)
    k = tot / p
    return Q(f"{nm} spent ${Rd(tot, 2)} on notebooks that cost ${Rd(p, 2)} each. How many notebooks did {nm} buy?", D(k), [f"{Rd(tot, 2)} ÷ {Rd(p, 2)}.", f"Multiply both by 100: {D(tot * 100)} ÷ {D(p * 100)} = {D(k)}."],
             [D(k * 10), D(tot - p), D(tot * p) if is_term(tot * p) else D(k + 1)], V(f"{D(tot)} ÷ {D(p)}"), why=["Misplaced the decimal point", "Subtracted instead of dividing", "Multiplied instead of dividing"], tags=["modeling"])


# ============================================================== S7 LCM and GCF
@fam("012")
def s7_lcm(r, L):
    a, b = r.sample(range(2, 16 if L < 2 else 30), 2)
    need(math.gcd(a, b) not in (a, b))
    l_ = a * b // math.gcd(a, b)
    if L == 2 and r.random() < 0.5:
        return Q(f"Hot dogs come in packs of {a} and buns in packs of {b}. What is the least number of each you can buy to have the same number of hot dogs and buns?", str(l_),
                 [f"Find the LCM of {a} and {b}.", f"Multiples of {a}: {', '.join(str(a * i) for i in range(1, 5))}, …", f"LCM = {l_}."], [str(a * b) if a * b != l_ else str(l_ * 2), str(math.gcd(a, b)), str(a + b)],
                 PY("lcm", nums=[a, b]), why=["Multiplied the numbers", "Found the GCF", "Added the numbers"], tags=["modeling"])
    return Q(f"Find the least common multiple (LCM) of {a} and {b}.", str(l_), [f"List multiples of {max(a, b)}: {', '.join(str(max(a, b) * i) for i in range(1, 5))}, …", f"The first one that is also a multiple of {min(a, b)} is {l_}."],
             [str(a * b) if a * b != l_ else str(l_ * 2), str(math.gcd(a, b)), str(max(a, b))], PY("lcm", nums=[a, b]), why=["Multiplied the numbers", "Found the GCF instead", "Gave the greater number"])


@fam("012")
def s7_which(r, L):
    a, b = r.sample(range(4, 40), 2)
    g = math.gcd(a, b)
    need(g > 1)
    kind = pick(r, ["gcf", "lcm"])
    if kind == "gcf":
        return Q(f"{a} red flowers and {b} white flowers are split into identical bouquets with none left over. What is the greatest number of bouquets?", str(g),
                 ["Each bouquet count must divide both numbers.", f"GCF of {a} and {b} = {g}."], [str(a * b // g), str(min(a, b)), str(a + b)], PY("gcf", nums=[a, b]), why=["Found the LCM", "Gave the smaller number", "Added the numbers"], tags=["modeling"])
    return Q(f"One light blinks every {a} seconds and another every {b} seconds. They blink together now. In how many seconds will they next blink together?", str(a * b // g),
             ["Find the LCM.", f"LCM of {a} and {b} = {a * b // g}."], [str(g), str(a * b) if a * b != a * b // g else str(a + b), str(a + b)], PY("lcm", nums=[a, b]), why=["Found the GCF", "Multiplied the numbers", "Added the numbers"], tags=["modeling"])


# ============================================================== S8 Distributive property and products of decimals
@fam("012")
def s8_factor_sum(r, L):
    g = r.randint(2, 12)
    p, q = r.randint(1, 12), r.randint(1, 12)
    need(math.gcd(p, q) == 1 and p != q)
    a, b = g * p, g * q
    need(a <= 100 and b <= 100)
    return Q(f"Use the GCF and the Distributive Property to write {a} + {b} as a product.", f"{g}({p} + {q})", [f"GCF of {a} and {b} is {g}.", f"{a} = {g} × {p} and {b} = {g} × {q}.", f"{a} + {b} = {g}({p} + {q})."],
             [f"{p}({g} + {q})" if p > 1 else f"{g}({p} + {q + 1})", f"{[d for d in range(1, g) if g % d == 0][-1]}({a // [d for d in range(1, g) if g % d == 0][-1]} + {b // [d for d in range(1, g) if g % d == 0][-1]})" if g > 2 else f"1({a} + {b})", f"{g}({p}{q})"],
             PY("factored", expr=f"{a} + {b}", gcf=g, vars=["x"]), why=["Factored out the wrong number", "Factored out a common factor that is not the greatest", ""])


@fam("012")
def s8_decimal_dist(r, L):
    a = r.randint(2, 9)
    b, c = rd(r, 1, 20, 1), rd(r, 1, 20, 1 if L < 2 else 2)
    e = f"{a}({D(b)} + {D(c)})"
    v = a * (b + c)
    return Q(f"Use the Distributive Property to evaluate {e}.", D(v), [f"{a} × {D(b)} + {a} × {D(c)}.", f"= {D(a * b)} + {D(a * c)}.", f"= {D(v)}."],
             [D(a * b + c), D(b + a * c), D(a + b + c)], V(e), why=["Multiplied only the first term", "Multiplied only the second term", "Added instead of multiplying"])


SKILLS = {
    1: dict(name="Dividing Fractions", std=["6.NS.A.1"], fams=[s1_div, s1_context, s1_model], extra=[err_of(s1_div), open_of(s1_div), select_of(s1_div)]),
    2: dict(name="Dividing Whole Numbers and Fractions", std=["6.NS.A.1"], fams=[s2_div, s2_context], extra=[err_of(s2_div), open_of(s2_div), select_of(s2_div)]),
    3: dict(name="Dividing Mixed Numbers and Fractions", std=["6.NS.A.1"], fams=[s3_div, s3_context], extra=[err_of(s3_div), open_of(s3_div), select_of(s3_div)]),
    4: dict(name="Dividing Multi-Digit Numbers", std=["6.NS.B.2"], fams=[s4_divide, s4_context], extra=[err_of(s4_divide), open_of(s4_divide)]),
    5: dict(name="Adding and Subtracting Multi-Digit Decimals", std=["6.NS.B.3"], fams=[s5_addsub, reuse(D7.s1_cost, (1, 1, 2))], extra=[err_of(s5_addsub), open_of(s5_addsub), select_of(s5_addsub)]),
    6: dict(name="Multiplying and Dividing Multi-Digit Decimals", std=["6.NS.B.3"], fams=[s6_muldiv, s6_context], extra=[err_of(s6_muldiv), open_of(s6_muldiv), select_of(s6_muldiv)]),
    7: dict(name="Least Common Multiple and Greatest Common Factor", std=["6.NS.B.4"], fams=[s7_lcm, s7_which, reuse(X7.s3_gcf, (0, 1, 1))], extra=[err_of(s7_lcm), open_of(s7_lcm), select_of(s7_lcm)]),
    8: dict(name="The Distributive Property and Products of Decimals", std=["6.NS.B.4", "6.NS.B.3"], fams=[s8_factor_sum, s8_decimal_dist], extra=[err_of(s8_decimal_dist), open_of(s8_decimal_dist), select_of(s8_decimal_dist)]),
}
