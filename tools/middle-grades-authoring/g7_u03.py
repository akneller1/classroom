"""Grade 7 Unit 3 — Decimals and Equations (decimals-equations)."""
from glib import *
from g7_u02 import M_solve

UNIT_ID = "decimals-equations"
ABBR = "deq"
VARS = ["x", "n", "y", "m", "k", "a", "t", "p"]


def rdec(r, lo, hi, places):
    """Random terminating decimal with exactly `places` places (last digit nonzero)."""
    while True:
        v = F(r.randint(int(lo * 10 ** places), int(hi * 10 ** places)), 10 ** places)
        if (v * 10 ** places) % 10:
            return v


# ============================================================== S1 Rounding and Estimating
@fam("012")
def s1_round(r, L):
    x = rdec(r, 1, 999, 3)
    place = pick(r, [1, F(1, 10)]) if L == 0 else pick(r, [F(1, 10), F(1, 100)]) if L == 1 else pick(r, [F(1, 100), 10])
    q = math.floor(x / place + F(1, 2)) * place
    tr = math.floor(x / place) * place
    nm = {1: "whole number", F(1, 10): "tenth", F(1, 100): "hundredth", 10: "ten"}[place]
    pl = {1: 0, F(1, 10): 1, F(1, 100): 2, 10: 0}[place]
    ans = Rd(q, pl)
    wr = [Rd(tr if tr != q else q + place, pl), Rd(q + place if tr != q + place else q - place, pl), D(x)[: D(x).index(".") + pl + 1] + "0" if pl else D(x).split(".")[0][:-1] + "0", Rd(x, pl + 1)]
    return Q(f"Round {D(x)} to the nearest {nm}.", ans, [f"Underline the {nm}s digit.", "Look at the digit to its right: 5 or more rounds up, less than 5 stays the same.", f"Rounded: {ans}."],
             wr, PY("round_place", expr=f"{x.numerator}/{x.denominator}", place=str(place)), why=["Truncated instead of rounding" if tr != q else "", "Rounded in the wrong direction", "", "Rounded to the wrong place"])


@fam("012")
def s1_estimate(r, L):
    k = 2 if L < 2 else 3
    ts = [rdec(r, 2, 60 if L else 20, 2) for _ in range(k)]
    op = pick(r, ["+", "-"]) if L < 2 else "+"
    if op == "-":
        ts.sort(reverse=True)
    rs = [math.floor(t + F(1, 2)) for t in ts]
    est = sum(rs) if op == "+" else rs[0] - rs[1]
    exact = sum(ts) if op == "+" else ts[0] - ts[1]
    tr = [math.floor(t) for t in ts]
    trv = sum(tr) if op == "+" else tr[0] - tr[1]
    e = f" {op} ".join(D(t) for t in ts)
    return Q(f"Estimate by rounding each number to the nearest whole number: {e}", str(est), [f"Round: {', '.join(map(str, rs))}.", f"Compute: {est}.", f"Exact value {D(exact)} is close to {est}."],
             [D(exact), str(trv) if trv != est else str(est + 1), str(est + 10)], PY("est", terms=[D(t) for t in ts], place=1, op=op),
             why=["Computed the exact value instead of estimating", "Truncated instead of rounding", ""])


@fam("12")
def s1_cost(r, L):
    ps = [rdec(r, 1, 20, 2) for _ in range(3)]
    tot = sum(ps)
    nm = name(r)
    rs = [math.floor(p + F(1, 2)) for p in ps]
    return Q(f"{nm} buys items costing ${Rd(ps[0], 2)}, ${Rd(ps[1], 2)}, and ${Rd(ps[2], 2)}. Round each price to the nearest dollar to estimate the total in dollars.", f"${sum(rs)}",
             [f"Round: ${rs[0]}, ${rs[1]}, ${rs[2]}.", f"Add: ${sum(rs)}."], [f"${Rd(tot, 2)}", f"${sum(math.floor(p) for p in ps)}" if sum(math.floor(p) for p in ps) != sum(rs) else f"${sum(rs) + 1}", f"${sum(rs) + 3}"],
             PY("est", terms=[D(p) for p in ps], place=1, op="+"), why=["Found the exact total", "Dropped the cents instead of rounding", ""], tags=["modeling"])


# ============================================================== S2 Estimating products and quotients
@fam("012")
def s2_product(r, L):
    a, b = rdec(r, 2, 20 if L < 2 else 60, 1), rdec(r, 2, 12, 1)
    ra, rb = math.floor(a + F(1, 2)), math.floor(b + F(1, 2))
    need(ra * rb != math.floor(a) * math.floor(b))
    return Q(f"Estimate {D(a)} × {D(b)} by rounding each factor to the nearest whole number.", str(ra * rb), [f"{D(a)} ≈ {ra} and {D(b)} ≈ {rb}.", f"{ra} × {rb} = {ra * rb}."],
             [D(a * b), str(math.floor(a) * math.floor(b)), str(ra + rb), str(ra * rb * 10)], PY("est", terms=[D(a), D(b)], place=1, op="*"),
             why=["Found the exact product", "Truncated instead of rounding", "Added instead of multiplying", "Misplaced the decimal point"])


@fam("012", mode="mc")
def s2_best(r, L):
    b = rdec(r, 2, 9, 1)
    a = b * r.randint(4, 30) + rdec(r, 0, 1, 1) - F(1, 2)
    need(a > 0)
    q = a / b
    cands = [F(round(float(q))) * F(10) ** k for k in (-2, -1, 0, 1)]
    best = min(cands, key=lambda c: abs(c - q))
    opts = [(D(c), c == best) for c in cands]
    r.shuffle(opts)
    return Q(f"Which is the best estimate of {D(a)} ÷ {D(b)}?", D(best), [f"Use compatible numbers near {D(a)} and {D(b)}.", f"The quotient is about {D(best)}.", "Check the size: the divisor goes into the dividend about that many times."],
             options=opts, chk=PY("best_est", expr=f"{D(a)} ÷ {D(b)}", opts=[D(c) for c in cands]), mode="mc", tags=["reasoning"])


@fam("012")
def s2_compat(r, L):
    b = r.randint(3, 9)
    k = r.randint(4, 20) if L < 2 else r.randint(20, 90)
    a = b * k + pick(r, [F(3, 10), F(-4, 10), F(2, 10), F(-1, 10), F(6, 10)])
    bb = b + (pick(r, [F(1, 10), F(-2, 10)]) if L else 0)
    need(round(float(a / bb)) == k)
    return Q(f"Use compatible numbers to estimate {D(a)} ÷ {D(bb)}.", str(k), [f"Choose numbers that divide easily: {b * k} ÷ {b}.", f"{b * k} ÷ {b} = {k}.", f"So {D(a)} ÷ {D(bb)} ≈ {k}."],
             [str(k * 10), D(F(k, 10)), str(k + b)], PY("near", expr=f"{D(a)} ÷ {D(bb)}", tol="0.5"), why=["Misplaced the decimal point", "Misplaced the decimal point", ""])


@fam("2")
def s2_over_under(r, L):
    a, b = rdec(r, 3, 15, 1), rdec(r, 3, 15, 1)
    need(a % 1 and b % 1)
    ra, rb = math.ceil(a), math.ceil(b)
    return Q(f"Mia estimates {D(a)} × {D(b)} by rounding both factors up to {ra} × {rb}. Is her estimate an overestimate or an underestimate?", "overestimate",
             ["Both factors were rounded up.", "Rounding both factors up makes the product larger than the exact product.", f"{ra * rb} > {D(a * b)}, so it is an overestimate."],
             ["underestimate", "exact"], PY("over_under", exact=D(a * b), est=str(ra * rb)), mode="sa", tags=["reasoning"], why=["Thought rounding up makes the product smaller", ""])


# ============================================================== S3 Mean, Median, Mode
def dataset(r, L, n=None):
    n = n or (r.randint(5, 7) if L == 0 else r.randint(6, 9))
    if L == 0:
        xs = [F(r.randint(1, 30)) for _ in range(n)]
    elif L == 1:
        xs = [rdec(r, 1, 20, 1) for _ in range(n)]
    else:
        xs = [F(r.randint(40, 100)) for _ in range(n)]
    return xs


@fam("012")
def s3_stat(r, L):
    xs = dataset(r, L)
    st = pick(r, ["mean", "median", "mode", "range"])
    s = sorted(xs)
    n = len(s)
    if st == "mode":
        from collections import Counter
        x = r.choice(xs)
        xs = xs + [x]
        s = sorted(xs)
        c = Counter(xs)
        top = max(c.values())
        modes = sorted(v for v, k in c.items() if k == top)
        need(len(modes) == 1)
        v = modes[0]
        ans = D(v)
        wr = [D(s[len(s) // 2]), D(max(xs)), D(sum(xs) / len(xs)) if is_term(sum(xs) / len(xs)) else D(s[0])]
        why = ["Gave the median", "Gave the greatest value", "Gave the mean"]
    elif st == "mean":
        tot = sum(xs)
        need(is_term(tot / n) and (tot / n).denominator <= 100)
        v = tot / n
        ans = D(v)
        wr = [D(s[n // 2]), D(tot), D(tot / (n - 1)) if is_term(tot / (n - 1)) else D(v + 1)]
        why = ["Gave the middle value", "Forgot to divide by the number of values", "Divided by the wrong count"]
    elif st == "median":
        v = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
        ans = D(v)
        mid_unsorted = xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2
        wr = [D(mid_unsorted) if mid_unsorted != v else D(s[0]), D(sum(xs) / n) if is_term(sum(xs) / n) else D(s[-1]), D(s[n // 2]) if n % 2 == 0 and s[n // 2] != v else D(v + 1)]
        why = ["Did not order the data first", "Gave the mean", "Took one middle value instead of averaging the two middle values"]
    else:
        v = s[-1] - s[0]
        ans = D(v)
        wr = [D(s[-1]), D(xs[-1] - xs[0]) if xs[-1] - xs[0] != v else D(v + 1), D(s[-1] + s[0])]
        why = ["Gave the greatest value", "Subtracted the last value listed from the first", "Added instead of subtracting"]
    return Q(f"Find the {st} of the data: {', '.join(D(x) for x in xs)}", ans, [f"Order the data: {', '.join(D(x) for x in s)}.",
                                                                             {"mean": f"Add the values ({D(sum(xs))}) and divide by {len(xs)}.", "median": "Find the middle value (average the two middle values if there is an even count).",
                                                                              "mode": "Find the value that occurs most often.", "range": "Subtract the least value from the greatest."}[st], f"The {st} is {ans}."],
             wr, PY("stat", data=[D(x) for x in xs], stat=st), why=why)


@fam("12")
def s3_missing(r, L):
    n = r.randint(4, 6)
    xs = [r.randint(60, 100) for _ in range(n - 1)]
    m = r.randint(72, 95)
    last = m * n - sum(xs)
    need(0 <= last <= 100)
    nm = name(r)
    return Q(f"{nm}'s first {n - 1} test scores are {', '.join(map(str, xs))}. What score does {nm} need on test {n} to have a mean of exactly {m}?", str(last),
             [f"Total needed: {m} × {n} = {m * n}.", f"Current total: {sum(xs)}.", f"Needed score: {m * n} - {sum(xs)} = {last}.", f"Check: ({sum(xs)} + {last}) ÷ {n} = {m}."],
             [str(m), str(m * (n - 1) - sum(xs) + m) if m * (n - 1) - sum(xs) + m != last else str(last + 5), str(abs(m * (n - 1) - sum(xs)))], PY("conds", vars=["s"], conds=[f"({' + '.join(map(str, xs))} + s) ÷ {n} = {m}"]),
             why=["Assumed the needed score equals the mean", "", "Used the wrong number of tests"], tags=["multistep", "reasoning"])


@fam("2", mode="mc")
def s3_outlier(r, L):
    xs = [r.randint(20, 35) for _ in range(6)]
    out = r.randint(80, 120)
    data = xs + [out]
    mean_without = sum(xs) / 6
    mean_with = sum(data) / 7
    opts = [("The mean increases more than the median.", True), ("The median increases more than the mean.", False), ("Both stay the same.", False), ("The mean decreases.", False)]
    r.shuffle(opts)
    return Q(f"The data {', '.join(map(str, xs))} gets one more value, {out}. How does the outlier affect the mean and median?", "The mean increases more than the median.",
             [f"Mean without: about {Rd(mean_without, 1)}; with: about {Rd(mean_with, 1)}.", "The median moves at most one position.", "Outliers pull the mean much more than the median."],
             options=opts, chk=PY("outlier_effect", base=xs, new=out), mode="mc", tags=["reasoning"])


# ============================================================== S4 Using Formulas
@fam("012")
def s4_eval(r, L):
    forms = []
    rt, t = r.randint(25, 70), r.randint(2, 6)
    forms.append((f"Use d = rt to find the distance traveled at {rt} miles per hour for {t} hours.", f"{rt}*{t}", f"{rt * t} miles", [f"{rt + t} miles", f"{N(F(rt, t))} miles", f"{rt * t * 2} miles"],
                  ["Added instead of multiplying", "Divided instead of multiplying", ""]))
    l, w = r.randint(3, 20), r.randint(2, 15)
    forms.append((f"Use P = 2l + 2w to find the perimeter of a rectangle with l = {l} cm and w = {w} cm.", f"2*{l} + 2*{w}", f"{2 * l + 2 * w} cm", [f"{l * w} cm", f"{l + w} cm", f"{2 * l + w} cm"],
                  ["Found the area instead", "Added only two sides", "Doubled only the length"]))
    if L:
        c = r.randint(-10, 40) * 5
        forms.append((f"Use F = 1.8C + 32 to convert {c}°C to degrees Fahrenheit.", f"1.8*({c}) + 32", f"{D(F(9, 5) * c + 32)}°F", [f"{D(F(9, 5) * (c + 32))}°F", f"{D(F(9, 5) * c)}°F", f"{c + 32}°F"],
                      ["Added 32 before multiplying", "Forgot to add 32", "Forgot to multiply by 1.8"]))
        b, h = r.randint(4, 20), r.randint(3, 14)
        forms.append((f"Use A = (1/2)bh to find the area of a triangle with b = {b} in. and h = {h} in.", f"1/2*{b}*{h}", f"{N(F(b * h, 2))} square inches", [f"{b * h} square inches", f"{b + h} square inches", f"{N(F(b + h, 2))} square inches"],
                      ["Forgot to multiply by 1/2", "Added instead of multiplying", ""]))
    if L == 2:
        p, rr, yy = r.randint(5, 40) * 100, pick(r, [F(2), F(5, 2), F(3), F(4), F(9, 2)]), r.randint(2, 6)
        forms.append((f"Use I = prt to find the simple interest on ${p} at {D(rr)}% per year for {yy} years.", f"{p}*{D(rr)}/100*{yy}", f"${D(p * rr / 100 * yy)}",
                      [f"${D(p * rr * yy)}", f"${D(p * rr / 100)}", f"${D(p + p * rr / 100 * yy)}"], ["Did not change the percent to a decimal", "Forgot to multiply by the time", "Gave the total amount instead of the interest"]))
    t_, ex, ans, wr, why = pick(r, forms)
    return Q(t_, ans, ["Write the formula.", "Substitute the given values.", "Evaluate using the order of operations.", f"Answer: {ans}."], wr, V(ex), why=why, tags=["modeling"])


@fam("12")
def s4_solve_formula(r, L):
    rt, t = r.randint(25, 70), r.randint(2, 6)
    d = rt * t
    return Q(f"A train travels {d} miles in {t} hours. Use d = rt to find its rate in miles per hour.", f"{rt} miles per hour",
             [f"{d} = r × {t}.", f"Divide both sides by {t}.", f"r = {rt}."], [f"{d * t} miles per hour", f"{d - t} miles per hour", f"{N(F(t, d))} miles per hour"], EQ(f"{d} = r*{t}", "r"),
             why=["Multiplied instead of dividing", "Subtracted instead of dividing", "Divided in the wrong order"], tags=["modeling"])


# ============================================================== S5 / S6 decimal equations
def dec_eq(r, L, kind):
    v = pick(r, VARS)
    pl = 1 if L == 0 else 2
    x = rdec(r, 0.5, 40, pl) * (pick(r, [1, -1]) if L == 2 else 1)
    if kind == "add":
        a = rdec(r, 0.5, 30, pl)
        if r.random() < 0.5:
            eq, b = f"{v} + {D(a)} = {D(x + a)}", x + a
            wr, why = [x + 2 * a, x + a, -x], ["Added instead of subtracting", "Gave the right side", "Made a sign error"]
        else:
            eq, b = f"{v} - {D(a)} = {D(x - a)}", x - a
            wr, why = [x - 2 * a, x - a, -x], ["Subtracted instead of adding", "Gave the right side", "Made a sign error"]
        st = ["Use the inverse operation on both sides.", f"Line up decimal points when adding or subtracting.", f"{v} = {D(x)}."]
    else:
        a = rdec(r, 0.2, 9, 1) if L < 2 else rdec(r, 0.2, 9, 2)
        need(a != 1)
        if r.random() < 0.5:
            eq = f"{D(a)}{v} = {D(a * x)}"
            wr, why = [a * x - a, a * a * x, x * 10], ["Subtracted instead of dividing", "Multiplied instead of dividing", "Misplaced the decimal point"]
            st = [f"Divide both sides by {D(a)}.", f"Move the decimal point to divide by a whole number.", f"{v} = {D(x)}."]
        else:
            x = x * a
            need(is_term(x / a))
            eq = f"{v}/{D(a)} = {D(x / a)}"
            wr, why = [x / a / a, x / a + a, x / 10], ["Divided instead of multiplying", "Added instead of multiplying", "Misplaced the decimal point"]
            st = [f"Multiply both sides by {D(a)}.", f"{v} = {D(x / a)} × {D(a)}.", f"{v} = {D(x)}."]
    need(all(is_term(w) for w in wr) and is_term(x))
    return Q(f"Solve: {eq}", f"{v} = {D(x)}", st + ["Check by substituting into the original equation."], [f"{v} = {D(w)}" for w in wr], EQ(eq, v), why=why)


@fam("012")
def s5_solve(r, L):
    return dec_eq(r, L, "add")


@fam("012")
def s6_solve(r, L):
    return dec_eq(r, L, "mul")


@fam("012")
def s5_context(r, L):
    nm = name(r)
    a, x = rdec(r, 1, 40, 2), rdec(r, 1, 60, 2)
    ctx = [(f"After buying a snack for ${Rd(a, 2)}, {nm} has ${Rd(x, 2)}. Solve m - {Rd(a, 2)} = {Rd(x, 2)} to find m, the money {nm} started with.", f"m - {D(a)} = {D(x)}", "m", x + a),
           (f"A plant grew {D(a)} cm and is now {D(x + a)} cm tall. Solve h + {D(a)} = {D(x + a)} to find h, its original height.", f"h + {D(a)} = {D(x + a)}", "h", x)]
    t, eq, v, sol = pick(r, ctx)
    money_ = "$" in t
    fmt = (lambda z: Rd(z, 2)) if money_ else D
    return Q(t, f"{v} = {fmt(sol)}", ["Use the inverse operation.", f"{v} = {fmt(sol)}.", "Check by substituting."], [f"{v} = {fmt(abs(sol - 2 * a))}", f"{v} = {fmt(sol + a)}", f"{v} = {fmt(sol * 10)}"],
             EQ(eq, v), why=["Used the same operation instead of the inverse", "", "Misplaced the decimal point"], tags=["modeling"])


@fam("012")
def s6_context(r, L):
    p, n = rdec(r, 1, 9, 2), r.randint(3, 12)
    nm = name(r)
    if r.random() < 0.5:
        return Q(f"{nm} paid ${Rd(p * n, 2)} for {n} pounds of apples. Solve {n}c = {Rd(p * n, 2)} to find the cost per pound.", f"${Rd(p, 2)}",
                 [f"Divide both sides by {n}.", f"c = {Rd(p * n, 2)} ÷ {n} = {Rd(p, 2)}."], [f"${Rd(p * n * n, 2)}", f"${Rd(p * n - n, 2)}", f"${Rd(p * 10, 2)}"], EQ(f"{n}c = {D(p * n)}", "c"),
                 why=["Multiplied instead of dividing", "Subtracted instead of dividing", "Misplaced the decimal point"], tags=["modeling"])
    g = rdec(r, 2, 6, 1)
    return Q(f"Gas costs ${Rd(p, 2)} per gallon. {nm} spent ${Rd(p * g, 2)}. Solve {Rd(p, 2)}g = {Rd(p * g, 2)} to find g, the number of gallons.", f"g = {D(g)}",
             [f"Divide both sides by {Rd(p, 2)}.", f"g = {D(g)}."], [f"g = {D(g * 10)}", f"g = {Rd(p * g * p, 2)}", f"g = {Rd(p * g - p, 2)}"], EQ(f"{D(p)}g = {D(p * g)}", "g"),
             why=["Misplaced the decimal point", "Multiplied instead of dividing", "Subtracted instead of dividing"], tags=["modeling"])


# ============================================================== S7 Metric system
MET = {"km": 1000, "m": 1, "cm": F(1, 100), "mm": F(1, 1000), "kg": 1000, "g": 1, "mg": F(1, 1000), "L": 1, "mL": F(1, 1000)}
NAMES_ = {"km": "kilometers", "m": "meters", "cm": "centimeters", "mm": "millimeters", "kg": "kilograms", "g": "grams", "mg": "milligrams", "L": "liters", "mL": "milliliters"}
FAM = [["km", "m", "cm", "mm"], ["kg", "g", "mg"], ["L", "mL"]]


@fam("012")
def s7_convert(r, L):
    grp = pick(r, FAM)
    a, b = r.sample(grp, 2)
    if L == 0:
        need(MET[a] > MET[b])
        x = F(r.randint(2, 90))
    else:
        x = rdec(r, 0.1, 90, 2) if L == 1 else rdec(r, 0.01, 900, 3)
    f_ = F(MET[a]) / F(MET[b])
    v = x * f_
    need(is_term(v) and v.denominator <= 10 ** 5)
    u = NAMES_[b]
    return Q(f"Convert {D(x)} {NAMES_[a]} to {u}.", f"{dtext(v)} {u}", [f"1 {NAMES_[a][:-1]} = {dtext(f_)} {u}.", f"{'Multiply' if f_ > 1 else 'Divide'} by {dtext(f_ if f_ > 1 else 1 / f_)}.", f"{D(x)} {NAMES_[a]} = {dtext(v)} {u}."],
             [f"{dtext(x / f_)} {u}", f"{dtext(v * 10)} {u}", f"{dtext(v / 10)} {u}"], V(f"{D(x)}*{D(f_)}"), why=["Multiplied and divided the wrong way", "Moved the decimal point one place too many", "Moved the decimal point one place too few"])


@fam("012", mode="mc")
def s7_unit(r, L):
    items = [("the length of a pencil", "cm"), ("the mass of a paper clip", "g"), ("the distance between two cities", "km"), ("the amount of water in a bathtub", "L"),
             ("the mass of a car", "kg"), ("the amount of medicine in a dropper", "mL"), ("the thickness of a coin", "mm"), ("the height of a door", "m")]
    t, u = pick(r, items)
    grp = [g for g in FAM if u in g][0]
    others = [x for g in FAM for x in g if x != u]
    r.shuffle(others)
    same = [x for x in grp if x != u]
    cand = list(dict.fromkeys(same + others))
    opts = [(NAMES_[u], True)] + [(NAMES_[x], False) for x in cand[:3]]
    r.shuffle(opts)
    return Q(f"Which metric unit is most reasonable for {t}?", NAMES_[u], [f"Compare the size of the object with the size of each unit.", f"The best unit is {NAMES_[u]}."], options=opts, chk=TXT(NAMES_[u]), mode="mc")


@fam("12")
def s7_compare(r, L):
    grp = pick(r, FAM[:2])
    a, b = r.sample(grp, 2)
    x = rdec(r, 0.1, 50, 2)
    y = x * F(MET[a]) / F(MET[b]) + pick(r, [F(1), F(-1), F(10), F(-10)]) * F(MET[a]) / F(MET[b]) / 100
    need(is_term(y) and y > 0)
    va, vb = x * MET[a], y * MET[b]
    ans = "<" if va < vb else ">" if va > vb else "="
    return Q(f"Compare using <, >, or =: {D(x)} {a} ___ {D(y)} {b}", ans, [f"Convert to the same unit: {D(x)} {a} = {D(x * F(MET[a]) / F(MET[b]))} {b}.", f"Compare {D(x * F(MET[a]) / F(MET[b]))} {b} and {D(y)} {b}.", f"So {ans}."],
             [x for x in "<>=" if x != ans], PY("cmp", a=f"{D(x)}*{D(F(MET[a]))}", b=f"{D(y)}*{D(F(MET[b]))}"), mode="sa", why=["Compared the numbers without converting units", ""])


@fam("2")
def s7_multi(r, L):
    n, x = r.randint(3, 12), r.randint(150, 900)
    tot = n * x
    return Q(f"A recipe uses {x} mL of milk per batch. How many liters of milk are needed for {n} batches?", f"{D(F(tot, 1000))} L",
             [f"{n} × {x} mL = {tot} mL.", "1 L = 1,000 mL.", f"{tot} ÷ 1,000 = {D(F(tot, 1000))} L."], [f"{tot} L", f"{D(F(tot, 100))} L", f"{D(F(x, 1000))} L"], V(f"{n}*{x}/1000"),
             why=["Did not convert milliliters to liters", "Divided by 100 instead of 1,000", "Forgot to multiply by the number of batches"], tags=["modeling", "multistep"])


SKILLS = {
    1: dict(name="Rounding and Estimating", std=["5.NBT.A.4", "7.EE.B.3"], fams=[s1_round, s1_estimate, s1_cost], extra=[err_of(s1_round), open_of(s1_round), err_of(s1_estimate)]),
    2: dict(name="Estimating Decimal Products and Quotients", std=["7.EE.B.3", "6.NS.B.3"], fams=[s2_product, s2_best, s2_compat, s2_over_under], extra=[err_of(s2_product), open_of(s2_product)]),
    3: dict(name="Mean, Median, and Mode", std=["6.SP.B.5c", "6.SP.A.3"], fams=[s3_stat, s3_missing, s3_outlier], extra=[err_of(s3_stat), open_of(s3_stat), select_of(s3_stat)]),
    4: dict(name="Using Formulas", std=["7.EE.B.4", "6.EE.A.2c"], fams=[s4_eval, s4_solve_formula], extra=[err_of(s4_eval), open_of(s4_eval)]),
    5: dict(name="Solving Equations by Adding or Subtracting Decimals", std=["7.EE.B.4", "6.EE.B.7"], fams=[s5_solve, s5_context], extra=[err_of(s5_solve), open_of(s5_solve), select_of(s5_solve)]),
    6: dict(name="Solving Equations by Multiplying or Dividing Decimals", std=["7.EE.B.4", "6.EE.B.7"], fams=[s6_solve, s6_context], extra=[err_of(s6_solve), open_of(s6_solve), select_of(s6_solve)]),
    7: dict(name="Using the Metric System", std=["5.MD.A.1", "6.RP.A.3d"], fams=[s7_convert, s7_unit, s7_compare, s7_multi], extra=[err_of(s7_convert), open_of(s7_convert), select_of(s7_convert)]),
}
