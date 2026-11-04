"""Grade 7 Unit 6 — Ratios, Proportions, and Percentages (ratios-proportions-percentages)."""
from glib import *

UNIT_ID = "ratios-proportions-percentages"
ABBR = "rpp"


def cross(eq):
    """a/b = c/d  ->  (a)*(d) = (b)*(c): same solutions when b, d ≠ 0; avoids dividing by the unknown."""
    l, r_ = eq.split(" = ")
    a, b = l.split("/")
    c, d = r_.split("/")
    return f"({a})*({d}) = ({b})*({c})"


def pct(x):
    """Percent text from a Fraction value (0.35 -> '35%')."""
    return D(F(x) * 100) + "%"


# ============================================================== S1 Ratios and Unit Rates
@fam("012")
def s1_simplify(r, L):
    g = r.randint(2, 9)
    a, b = r.randint(1, 12), r.randint(1, 12)
    need(math.gcd(a, b) == 1 and a != b)
    thing = pick(r, [("boys", "girls"), ("cats", "dogs"), ("red marbles", "blue marbles"), ("wins", "losses")])
    if L == 2:
        c = r.randint(1, 12)
        tot = g * (a + b + c)
        need(math.gcd(math.gcd(a, b), c) == 1 and math.gcd(a, a + b + c) == 1)
        return Q(f"A bag has {g * a} red, {g * b} blue, and {g * c} green marbles. Write the ratio of red marbles to all marbles in simplest form, as a:b.", f"{a}:{a + b + c}",
                 [f"Total marbles: {tot}.", f"Ratio red to total: {g * a}:{tot}.", f"Divide by the GCF {g}: {a}:{a + b + c}."], [f"{a}:{b}", f"{g * a}:{tot}", f"{a}:{b + c}"],
                 PY("ratio", a=str(g * a), b=str(tot)), why=["Compared red to blue instead of red to all", "Did not simplify", "Compared red to the other colors"])
    return Q(f"A club has {g * a} {thing[0]} and {g * b} {thing[1]}. Write the ratio of {thing[0]} to {thing[1]} in simplest form, as a:b.", f"{a}:{b}",
             [f"Ratio: {g * a}:{g * b}.", f"GCF of {g * a} and {g * b} is {g}.", f"Simplest form: {a}:{b}."], [f"{b}:{a}", f"{g * a}:{g * b}" if L else f"{a}:{a + b}", f"{a}:{a + b}" if L else f"{g * a}:{g * b}"],
             PY("ratio", a=str(g * a), b=str(g * b)), why=["Reversed the order of the ratio", "Did not simplify", "Compared a part to the whole"])


@fam("012")
def s1_unit_rate(r, L):
    u = r.randint(2, 12)
    if L == 0:
        rate = r.randint(3, 25)
        tot = rate * u
        ctx = pick(r, [(f"A car travels {tot} miles in {u} hours.", "miles per hour"), (f"{name(r)} earns ${tot} in {u} hours.", "dollars per hour"), (f"A printer prints {tot} pages in {u} minutes.", "pages per minute")])
        return Q(f"{ctx[0]} What is the unit rate in {ctx[1]}?", f"{rate} {ctx[1]}", [f"Divide: {tot} ÷ {u}.", f"Unit rate = {rate} {ctx[1]}."],
                 [f"{tot * u} {ctx[1]}", f"{N(F(u, tot))} {ctx[1]}", f"{tot - u} {ctx[1]}"], V(f"{tot} ÷ {u}"), why=["Multiplied instead of dividing", "Divided in the wrong order", "Subtracted instead of dividing"])
    price = F(r.randint(100, 900), 100) * u
    need(is_term(price / u))
    if L == 1:
        return Q(f"A {u}-pack of juice boxes costs ${Rd(price, 2)}. What is the price per juice box?", f"${Rd(price / u, 2)}", [f"Divide: {Rd(price, 2)} ÷ {u}.", f"= ${Rd(price / u, 2)} per box."],
                 [f"${Rd(price * u, 2)}", f"${Rd(price - u, 2)}", f"${Rd(price / u * 10, 2)}"], V(f"{D(price)} ÷ {u}"), why=["Multiplied instead of dividing", "Subtracted instead of dividing", "Misplaced the decimal point"])
    a, b = rfr(r), rfr(r)
    rate = a / b
    return Q(f"A snail crawls {mixed(a)} feet in {N(b)} hour. What is its speed in feet per hour?", f"{mixed(rate)} feet per hour",
             [f"Unit rate = {mixed(a)} ÷ {N(b)}.", f"Multiply by the reciprocal: {N(a)} × {N(1 / b)} = {N(rate)}.", f"= {mixed(rate)} feet per hour."],
             [f"{mixed(a * b)} feet per hour", f"{mixed(b / a)} feet per hour", f"{mixed(a + b)} feet per hour"], V(f"({N(a)}) ÷ ({N(b)})"),
             why=["Multiplied instead of dividing", "Divided in the wrong order", "Added the quantities"], tags=["challenge"])


def rfr(r):
    d = pick(r, [2, 3, 4, 5, 8])
    return F(r.randint(1, d - 1), d)


@fam("012", mode="mc")
def s1_better(r, L):
    n1, n2 = r.sample([4, 6, 8, 10, 12, 16, 18, 24], 2)
    p1 = F(r.randint(150, 500), 100) * n1 / 4
    p2 = F(r.randint(150, 500), 100) * n2 / 4
    p1, p2 = F(round(p1 * 100), 100), F(round(p2 * 100), 100)
    u1, u2 = p1 / n1, p2 / n2
    need(abs(u1 - u2) > F(1, 100))
    a, b = f"{n1} ounces for ${Rd(p1, 2)}", f"{n2} ounces for ${Rd(p2, 2)}"
    ans = a if u1 < u2 else b
    opts = [(a, u1 < u2), (b, u2 < u1), ("They cost the same per ounce", False), ("Not enough information", False)]
    return Q(f"Which is the better buy: {a} or {b}?", ans, [f"Unit prices: ${Rd(u1, 3)} per ounce and ${Rd(u2, 3)} per ounce.", "The lower unit price is the better buy.", f"Better buy: {ans}."],
             options=opts, chk=PY("better_buy", deals={a: [str(p1), str(n1)], b: [str(p2), str(n2)]}), mode="mc", tags=["modeling"])


# ============================================================== S2 Proportions
@fam("012")
def s2_solve(r, L):
    a, b = r.randint(1, 12), r.randint(2, 15)
    need(math.gcd(a, b) == 1 and a != b)
    k = r.randint(2, 9) if L < 2 else F(r.randint(3, 15), 2)
    x = a * k
    v = pick(r, ["x", "n", "m"])
    pos = r.randrange(4) if L else 0
    vals = [F(a), F(b), F(x), F(b * k)]
    show = [N(t) if i != pos else v for i, t in enumerate(vals)]
    need(all("/" not in s for s in show))
    eq = f"{show[0]}/{show[1]} = {show[2]}/{show[3]}"
    ans = vals[pos]
    return Q(f"Solve the proportion: {eq}", f"{v} = {N(ans)}", ["Use cross products (or find the scale factor).", f"Cross products are equal.", f"Solve for {v}: {v} = {N(ans)}.", "Check: the cross products match."],
             [f"{v} = {N(vals[pos] + (vals[(pos + 2) % 4] - vals[(pos + 1) % 4]) if True else 0)}", f"{v} = {N(vals[pos] * 2)}", f"{v} = {N(vals[(pos + 1) % 4] * vals[(pos + 2) % 4] / vals[(pos + 3) % 4])}"],
             EQ(cross(eq), v), why=["Added the difference instead of multiplying by the scale factor", "", "Multiplied the wrong pair of terms"])


@fam("012")
def s2_is_prop(r, L):
    a, b = r.randint(1, 9), r.randint(2, 12)
    k = r.randint(2, 6)
    c, d = a * k, b * k + (0 if r.random() < 0.5 else pick(r, [1, -1, 2]))
    ok = a * d == b * c
    return Q(f"Do the ratios {a}/{b} and {c}/{d} form a proportion?", "Yes" if ok else "No", [f"Cross products: {a} × {d} = {a * d} and {b} × {c} = {b * c}.", f"They are {'equal' if ok else 'not equal'}.", "Yes" if ok else "No"],
             ["No" if ok else "Yes"], PY("is_prop", a=a, b=b, c=c, d=d), mode="sa", why=["Compared differences instead of cross products"])


@fam("012")
def s2_context(r, L):
    a, b = r.randint(2, 9), r.randint(2, 12)
    k = r.randint(3, 12)
    ctx = pick(r, [(f"A recipe uses {a} cups of flour for {b} muffins. How many cups are needed for {b * k} muffins?", f"{a * k} cups", f"{a}/{b} = c/{b * k}", "c", a * k),
                   (f"A car uses {a} gallons of gas to go {b * 10} miles. How many gallons does it need to go {b * 10 * k} miles?", f"{a * k} gallons", f"{a}/{b * 10} = g/{b * 10 * k}", "g", a * k),
                   (f"On a map, {a} cm represents {b} km. How many km do {a * k} cm represent?", f"{b * k} km", f"{a}/{b} = {a * k}/d", "d", b * k)])
    t, ans, eq, v, val = ctx
    unit = ans.split(" ", 1)[1]
    return Q(t, ans, [f"Set up a proportion: {eq}.", "Find the scale factor or use cross products.", f"{v} = {val}.", f"Answer: {ans}."], [f"{val + a} {unit}" if val + a != val else f"{val + 1} {unit}", f"{N(F(val, k * k)) if k > 1 else val + 2} {unit}", f"{b * k + a if unit != 'km' else a * k} {unit}"],
             PY("eq_val", eq=cross(eq), var=v), why=["Added instead of multiplying", "", "Set up the proportion incorrectly"], tags=["modeling"])


# ============================================================== S3 Similar Figures and Scale Drawings
@fam("012")
def s3_similar(r, L):
    a, b = r.randint(3, 12), r.randint(3, 12)
    need(a != b)
    k = r.randint(2, 4) if L < 2 else F(r.randint(3, 9), 2)
    c, d = a * k, b * k
    need(F(d).denominator == 1 and F(c).denominator == 1)
    fig = pick(r, ["rectangles", "triangles"])
    alt = f"Two similar {fig}. The smaller has sides {a} and {b}; the larger has corresponding sides {N(c)} and x."
    pts1 = [(0, 0), (b, 0), (b, a), (0, a)] if fig == "rectangles" else [(0, 0), (b, 0), (0, a)]
    return Q(f"The {fig} are similar. The small one has sides {a} cm and {b} cm. The corresponding sides of the large one are {N(c)} cm and x cm. Find x.", f"x = {N(d)}",
             [f"Scale factor = {N(c)} ÷ {a} = {N(k)}.", f"x = {b} × {N(k)}.", f"x = {N(d)} cm."], [f"x = {N(b + c - a)}", f"x = {N(F(a * b, c))}", f"x = {N(c)}"], EQ(cross(f"{a}/{b} = {N(c)}/x")),
             why=["Added the difference instead of multiplying by the scale factor", "Set up the proportion upside down", "Copied the given side"], tags=["connections"])


@fam("012")
def s3_scale(r, L):
    s_in = pick(r, [F(1), F(1, 2), F(1, 4), F(2)]) if L else F(1)
    s_ft = r.randint(2, 20)
    m = F(r.randint(2, 12)) + (pick(r, [F(1, 2), F(1, 4), F(0)]) if L else 0)
    actual = m / s_in * s_ft
    need(actual.denominator <= 4)
    what = pick(r, ["room", "garden", "bridge", "park"])
    return Q(f"A scale drawing uses the scale {mixed(s_in)} in. : {s_ft} ft. A {what} is {mixed(m)} in. long on the drawing. How long is the actual {what}?", f"{mixed(actual)} feet",
             [f"Scale: {mixed(s_in)} in. represents {s_ft} ft, so 1 in. represents {mixed(s_ft / s_in)} ft.", f"x = {mixed(m)} × {mixed(s_ft / s_in)}.", f"x = {mixed(actual)} feet."],
             [f"{mixed(m * s_ft * s_in)} feet" if m * s_ft * s_in != actual else f"{mixed(actual + 1)} feet", f"{mixed(m + s_ft)} feet", f"{mixed(m / s_ft)} feet"],
             V(f"({N(m)}) * {s_ft} ÷ ({N(s_in)})"), why=["Multiplied by the drawing length of the scale instead of dividing", "Added instead of multiplying", "Divided instead of multiplying"], tags=["modeling"])


@fam("12")
def s3_factor(r, L):
    a = r.randint(2, 12)
    k = pick(r, [2, 3, 4, F(1, 2), F(1, 3), F(3, 2)])
    b = a * k
    need(F(b).denominator == 1)
    return Q(f"A figure is enlarged or reduced so that a {a}-inch side becomes {N(b)} inches. What is the scale factor?", N(k), [f"Scale factor = new length ÷ original length.", f"= {N(b)} ÷ {a} = {N(k)}."],
             [N(1 / k), N(b - a), N(b + a)], V(f"{N(b)} ÷ {a}"), why=["Divided in the wrong order", "Subtracted instead of dividing", "Added the lengths"])


# ============================================================== S4 Probability
@fam("012")
def s4_simple(r, L):
    cols = r.sample(["red", "blue", "green", "yellow", "purple"], 3)
    ns = [r.randint(1, 9) for _ in cols]
    tot = sum(ns)
    i = r.randrange(3)
    if L == 0:
        v = F(ns[i], tot)
        return Q(f"A bag has {', '.join(f'{n} {c}' for n, c in zip(ns, cols))} marbles. One marble is picked at random. What is P({cols[i]})? Write a fraction in simplest form.", N(v),
                 [f"Total marbles: {tot}.", f"Favorable: {ns[i]}.", f"P({cols[i]}) = {ns[i]}/{tot} = {N(v)}."], [N(F(ns[i], tot - ns[i])), N(F(tot - ns[i], tot)), f"{ns[i]}/{tot + 1}"],
                 PY("frac_simplest", expr=f"{ns[i]}/{tot}", mixed=False), why=["Compared favorable to unfavorable outcomes (odds)", "Found the probability of NOT picking the color", ""])
    if L == 1:
        v = 1 - F(ns[i], tot)
        return Q(f"A bag has {', '.join(f'{n} {c}' for n, c in zip(ns, cols))} marbles. One is picked at random. What is P(not {cols[i]})? Write a fraction in simplest form.", N(v),
                 [f"P({cols[i]}) = {ns[i]}/{tot}.", f"P(not {cols[i]}) = 1 - {ns[i]}/{tot}.", f"= {N(v)}."], [N(F(ns[i], tot)), N(F(tot - ns[i], ns[i])), N(F(1, 3)) if N(v) != "1/3" else N(F(2, 3))],
                 PY("frac_simplest", expr=f"1 - {ns[i]}/{tot}", mixed=False), why=["Found P(the color) instead of P(not the color)", "Computed odds", "Assumed the colors are equally likely"])
    p = F(ns[i], tot)
    return Q(f"A spinner lands on {cols[i]} with probability {N(p)}. In {tot * 10} spins, about how many times would you expect it to land on {cols[i]}?", str(int(p * tot * 10)),
             [f"Expected number = P × number of trials.", f"{N(p)} × {tot * 10} = {int(p * tot * 10)}."], [str(ns[i]), str(tot * 10 - int(p * tot * 10)), str(int(p * tot * 10) * 2)],
             V(f"{N(p)}*{tot * 10}"), why=["Used the count instead of multiplying by the number of trials", "Found the expected number of other outcomes", ""], tags=["modeling"])


@fam("012")
def s4_die(r, L):
    ev = pick(r, [("an even number", [2, 4, 6]), ("a number greater than 4", [5, 6]), ("a prime number", [2, 3, 5]), ("a multiple of 3", [3, 6]), ("a number less than 3", [1, 2])])
    t, fav = ev
    v = F(len(fav), 6)
    if L == 2:
        v2 = 1 - v
        return Q(f"A number cube (1–6) is rolled. What is the probability of NOT rolling {t}? Write a percent rounded to the nearest whole percent.", Rd(v2 * 100, 0) + "%",
                 [f"Outcomes for {t}: {', '.join(map(str, fav))} ({len(fav)} of 6).", f"P(not) = 1 - {len(fav)}/6 = {N(v2)}.", f"{N(v2)} ≈ {Rd(v2 * 100, 0)}%."],
                 [Rd(v * 100, 0) + "%", f"{6 - len(fav)}%", Rd(v2 * 10, 0) + "%"], AP(f"(1 - {len(fav)}/6)*100", 0), why=["Found P(event) instead of P(not event)", "Wrote the count as a percent", "Multiplied by 10 instead of 100"])
    return Q(f"A number cube (1–6) is rolled. What is P({t})? Write a fraction in simplest form.", N(v), [f"Favorable outcomes: {', '.join(map(str, fav))}.", f"P = {len(fav)}/6 = {N(v)}."],
             [N(F(len(fav), 6 - len(fav))), f"{len(fav)}/6" if f"{len(fav)}/6" != N(v) else N(F(len(fav), 5)), N(1 - v)], PY("frac_simplest", expr=f"{len(fav)}/6", mixed=False),
             why=["Compared favorable to unfavorable outcomes", "Did not simplify", "Found the complement"])


@fam("12", mode="mc")
def s4_likely(r, L):
    p = F(r.randint(0, 10), 10)
    word = "impossible" if p == 0 else "certain" if p == 1 else "unlikely" if p < F(1, 2) else "likely" if p > F(1, 2) else "equally likely as not"
    labels = ["impossible", "unlikely", "equally likely as not", "likely", "certain"]
    opts = [(word, True)] + [(w, False) for w in r.sample([l for l in labels if l != word], 3)]
    r.shuffle(opts)
    return Q(f"An event has probability {D(p)}. How would you describe it?", word, ["0 is impossible, 1 is certain, 0.5 is equally likely as not.", f"{D(p)} is {word}."], options=opts,
             chk=PY("likelihood", p=str(p)), mode="mc")


# ============================================================== S5 Fractions, Decimals, Percentages
@fam("012")
def s5_convert(r, L):
    x = F(r.randint(1, 99), 100) if L == 0 else pick(r, [F(n, d) for d in (8, 20, 25, 40, 50) for n in range(1, d)]) if L == 1 else pick(r, [F(r.randint(101, 350), 100), F(r.randint(1, 9), 1000), F(1, 3), F(2, 3)])
    form = pick(r, ["f2p", "d2p", "p2d", "p2f"])
    if form == "f2p" or not is_term(x):
        pt = Rd(x * 100, 1) + "%" if not is_term(x * 100) else pct(x)
        ex = f"{N(x)}*100"
        return Q(f"Write {N(x)} as a percent." + (" Round to the nearest tenth of a percent." if not is_term(x * 100) else ""), pt, [f"{N(x)} = {D(x, 4) if not is_term(x) else D(x)}.", "Multiply by 100 and add %.", f"{pt}."],
                 [D(x, 3) + "%" if not is_term(x) else D(x) + "%", (Rd(x * 1000, 1) if not is_term(x * 1000) else D(x * 1000)) + "%", (Rd(100 / x, 1) if not is_term(100 / x) else D(100 / x)) + "%"],
                 AP(ex, 1) if not is_term(x * 100) else V(ex), why=["Forgot to multiply by 100", "Multiplied by 1,000", "Divided instead of multiplying"])
    if form == "d2p":
        return Q(f"Write {D(x)} as a percent.", pct(x), [f"Move the decimal point two places to the right.", f"{D(x)} = {pct(x)}."], [D(x / 10) + "%" if is_term(x / 10) else D(x) + "%", D(x * 10) + "%", D(x) + "%"],
                 V(f"{D(x)}*100"), why=["Moved the decimal point the wrong way", "Moved the decimal point only one place", "Kept the decimal and added %"])
    if form == "p2d":
        return Q(f"Write {pct(x)} as a decimal.", D(x), [f"Divide by 100 (move the decimal point two places left).", f"{pct(x)} = {D(x)}."], [D(x * 100), D(x / 10), D(x * 10)],
                 V(f"{D(x * 100)}/100"), why=["Did not divide by 100", "Moved the decimal point three places", "Moved the decimal point only one place"])
    return Q(f"Write {pct(x)} as a fraction in simplest form.", N(x), [f"{pct(x)} = {D(x * 100)}/100.", "Simplify.", f"= {N(x)}."], [f"{D(x * 100)}/100" if D(x * 100).isdigit() and N(x) != f"{D(x * 100)}/100" else N(x * 10), N(1 / x), N(x * 10)],
             PY("frac_simplest", expr=f"{D(x * 100)}/100", mixed=True), why=["Did not simplify", "Flipped the fraction", "Used the wrong power of 10"])


@fam("12", mode="mc")
def s5_greatest(r, L):
    vals = r.sample([F(n, d) for d in (4, 5, 8, 10, 20) for n in range(1, d)], 4)
    need(len(set(vals)) == 4)
    kinds = ["f", "d", "p", "f"]
    r.shuffle(kinds)
    txt = [N(v) if k == "f" else D(v) if k == "d" else pct(v) for v, k in zip(vals, kinds)]
    best = txt[vals.index(max(vals))]
    return Q("Which value is greatest?", best, ["Convert each to a decimal.", ", ".join(f"{t} = {D(v)}" for t, v in zip(txt, vals)) + ".", f"Greatest: {best}."], options=[(t, t == best) for t in txt],
             chk=PY("extreme_pct", items=txt), mode="mc")


# ============================================================== S6 / S7 percent problems
@fam("012")
def s6_percent(r, L):
    p = pick(r, [10, 20, 25, 50, 75]) if L == 0 else r.randint(2, 19) * 5 if L == 1 else pick(r, [F(25, 2), F(35, 2), 120, 150, 175, F(5, 2), 8])
    w = r.randint(2, 30) * pick(r, [4, 8, 20])
    part = F(p) * w / 100
    need(part.denominator == 1 or (L == 2 and is_term(part)))
    kind = pick(r, ["part", "whole", "percent"]) if L else "part"
    if kind == "part":
        return Q(f"What is {D(F(p))}% of {w}?", D(part), [f"Write a proportion: {D(F(p))}/100 = n/{w}.", f"n = {D(F(p))} × {w} ÷ 100.", f"n = {D(part)}."],
                 [D(F(p) * w), D(w / F(p)) if is_term(w / F(p)) else D(part + 1), D(F(p) * w / 10)], V(f"{D(F(p))}/100*{w}"),
                 why=["Did not divide by 100", "Divided by the percent", "Divided by 10 instead of 100"])
    if kind == "whole":
        need(part > 0)
        return Q(f"{D(part)} is {D(F(p))}% of what number?", D(F(w)), [f"Proportion: {D(F(p))}/100 = {D(part)}/n.", f"n = {D(part)} × 100 ÷ {D(F(p))}.", f"n = {w}."],
                 [D(part * F(p) / 100), D(part * F(p)), D(part + F(p))], PY("conds", vars=["n"], conds=[f"{D(F(p))}/100*n = {D(part)}"]),
                 why=["Found the percent of the part instead of the whole", "Multiplied by the percent", "Added the numbers"])
    return Q(f"What percent of {w} is {D(part)}?", D(F(p)) + "%", [f"Proportion: n/100 = {D(part)}/{w}.", f"n = {D(part)} × 100 ÷ {w}.", f"n = {D(F(p))}%."],
             [D(F(w * 100) / part) + "%" if is_term(F(w * 100) / part) else D(part) + "%", D(F(p) / 100) + "%", D(part) + "%"], V(f"{D(part)}/{w}*100"),
             why=["Divided in the wrong order", "Forgot to multiply by 100", "Used the part as the percent"])


@fam("012")
def s6_context(r, L):
    p = pick(r, [10, 15, 20, 25, 30, 40, 60]) if L < 2 else pick(r, [12, 35, 45, 65, 85])
    w = r.randint(2, 20) * 20
    part = F(p * w, 100)
    need(part.denominator == 1)
    ctx = pick(r, [(f"{p}% of the {w} students in a school walk to school. How many students walk?", D(part), "students"),
                   (f"A team won {D(part)} of its {w} games. What percent of its games did it win?", f"{p}%", "%"),
                   (f"{D(part)} students, which is {p}% of the grade, signed up for band. How many students are in the grade?", str(w), "students")])
    t, ans, u = ctx
    which = 0 if ans == D(part) and u == "students" and "walk" in t else 1 if "%" in ans else 2
    chk = [V(f"{p}/100*{w}"), V(f"{D(part)}/{w}*100"), PY("conds", vars=["n"], conds=[f"{p}/100*n = {D(part)}"])][which]
    wr = [[str(p * w), str(w - int(part)), str(int(part) // 10)], [f"{D(part)}%", f"{w - int(part)}%" if w - int(part) <= 100 else f"{100 - p + 5}%", f"{D(F(w, int(part)))}%"],
          [str(int(part) * p // 100) if int(part) * p // 100 else "1", str(int(part) + p), str(int(part) * p)]][which]
    return Q(t, ans, ["Identify the part, the whole, and the percent.", "Use the proportion: part divided by whole equals percent divided by 100.", f"Answer: {ans}."], wr, chk, why=["Used the wrong operation", "", ""], tags=["modeling"])


@fam("012")
def s7_equation(r, L):
    p = pick(r, [5, 10, 20, 25, 40, 50, 80]) if L == 0 else r.randint(1, 19) * 5 if L == 1 else pick(r, [F(15, 2), F(45, 2), 115, 140, 250, 3])
    w = r.randint(2, 40) * 4
    part = F(p) * w / 100
    need(is_term(part))
    pd = D(F(p) / 100)
    if r.random() < 0.5 or L == 0:
        eq = f"n = {pd} × {w}"
        return Q(f"Write and solve an equation: What is {D(F(p))}% of {w}?", f"n = {D(part)}", [f"Write the percent as a decimal: {D(F(p))}% = {pd}.", f"Equation: {eq}.", f"n = {D(part)}."],
                 [f"n = {D(F(p) * w)}", f"n = {D(w / F(p) * 100) if is_term(w / F(p) * 100) else D(part + 2)}", f"n = {D(part * 10)}"], PY("conds", vars=["n"], conds=[f"n = {D(F(p))}/100*{w}"]),
                 why=["Did not change the percent to a decimal", "Divided instead of multiplying", "Misplaced the decimal point"])
    eq = f"{D(part)} = {pd}n"
    return Q(f"Write and solve an equation: {D(part)} is {D(F(p))}% of what number?", f"n = {w}", [f"Equation: {eq}.", f"Divide both sides by {pd}.", f"n = {w}."],
             [f"n = {D(part * F(p) / 100)}", f"n = {D(part * F(p))}", f"n = {D(part / F(p))}" if is_term(part / F(p)) else f"n = {w + 10}"], EQ(eq, "n"),
             why=["Multiplied instead of dividing", "Did not change the percent to a decimal", "Divided by the percent without converting"])


@fam("12")
def s7_context(r, L):
    p = pick(r, [15, 18, 20, 22, 25])
    bill = F(r.randint(1500, 8000), 100)
    tip = bill * p / 100
    nm = name(r)
    return Q(f"{nm}'s restaurant bill is ${Rd(bill, 2)}. {nm} leaves a {p}% tip. How much is the tip, to the nearest cent?", f"${Rd(tip, 2)}",
             [f"Tip = {D(F(p, 100))} × {Rd(bill, 2)}.", f"= {D(tip) if is_term(tip) else Rd(tip, 4)}.", f"≈ ${Rd(tip, 2)}."], [f"${Rd(bill * p, 2)}", f"${Rd(bill + tip, 2)}", f"${Rd(tip * 10, 2)}"],
             AP(f"{D(bill)}*{p}/100", 2), why=["Did not change the percent to a decimal", "Gave the total instead of the tip", "Misplaced the decimal point"], tags=["modeling"])


# ============================================================== S8 Percent of Change
@fam("012")
def s8_change(r, L):
    old = r.randint(2, 40) * pick(r, [5, 10, 20])
    p = pick(r, [10, 20, 25, 50]) if L == 0 else r.randint(1, 18) * 5 if L == 1 else pick(r, [F(25, 2), 8, 35, 120, 150, 3])
    up = r.random() < 0.6 or L == 0
    new = old * (1 + F(p) / 100) if up else old * (1 - F(p) / 100)
    need(is_term(new) and new > 0)
    if L < 2 or r.random() < 0.6:
        diff = abs(new - old)
        return Q(f"A value changes from {D(F(old))} to {D(new)}. Find the percent of change and say whether it is an increase or a decrease.", f"{D(F(p))}% {'increase' if up else 'decrease'}",
                 [f"Amount of change: |{D(new)} - {old}| = {D(diff)}.", f"Divide by the ORIGINAL amount: {D(diff)} ÷ {old} = {D(diff / old)}.", f"{D(F(p))}% {'increase' if up else 'decrease'}."],
                 [f"{D(F(p))}% {'decrease' if up else 'increase'}", f"{Rd(diff / new * 100, 1) if not is_term(diff / new * 100) else D(diff / new * 100)}% {'increase' if up else 'decrease'}", f"{D(diff)}% {'increase' if up else 'decrease'}"],
                 PY("pct_change", old=str(old), new=D(new)), why=["Called the change the wrong direction", "Divided by the new amount instead of the original", "Used the amount of change as the percent"])
    return Q(f"A price of ${D(F(old))} is {'increased' if up else 'decreased'} by {D(F(p))}%. What is the new price?", f"${Rd(new, 2)}",
             [f"Change: {D(F(p))}% of {old} = {D(F(p) * old / 100)}.", f"{'Add' if up else 'Subtract'}: {old} {'+' if up else '-'} {D(F(p) * old / 100)}.", f"New price: ${Rd(new, 2)}."],
             [f"${Rd(old * (1 - F(p) / 100) if up else old * (1 + F(p) / 100), 2)}", f"${Rd(F(p) * old / 100, 2)}", f"${Rd(old + F(p), 2)}"], AP(f"{old}*(1 {'+' if up else '-'} {D(F(p))}/100)", 2),
             why=["Changed in the wrong direction", "Gave only the amount of change", "Added the percent as dollars"])


# ============================================================== S9 Markup and Discount
@fam("012")
def s9_discount(r, L):
    price = F(r.randint(8, 120)) + (pick(r, [F(0), F(99, 100), F(1, 2)]) if L else 0)
    d = pick(r, [10, 20, 25, 50]) if L == 0 else pick(r, [15, 30, 35, 40, 60])
    sale = price * (1 - F(d, 100))
    if L == 2:
        tax = pick(r, [5, 6, F(25, 4), 8])
        tot = sale * (1 + F(tax) / 100)
        return Q(f"A ${Rd(price, 2)} jacket is on sale for {d}% off. Sales tax of {D(F(tax))}% is added to the sale price. What is the final cost, to the nearest cent?", f"${Rd(tot, 2)}",
                 [f"Discount: {d}% of {Rd(price, 2)} = {Rd(price * d / 100, 2) if not is_term(price * d / 100) else D(price * d / 100)}.", f"Sale price: {D(sale) if is_term(sale) else Rd(sale, 4)}.",
                  f"Tax: {D(F(tax))}% of the sale price.", f"Final cost: ${Rd(tot, 2)}."],
                 [f"${Rd(price * (1 - F(d, 100) + F(tax) / 100), 2)}", f"${Rd(sale, 2)}", f"${Rd(price * (1 + F(tax) / 100), 2)}"], AP(f"{D(price)}*(1 - {d}/100)*(1 + {D(F(tax))}/100)", 2),
                 why=["Combined the discount and tax percents into one change", "Forgot the tax", "Forgot the discount"], tags=["multistep", "modeling"])
    return Q(f"A ${Rd(price, 2)} item is on sale for {d}% off. What is the sale price?", f"${Rd(sale, 2)}",
             [f"Discount: {d}% × {Rd(price, 2)} = ${Rd(price * d / 100, 2)}.", f"Sale price: {Rd(price, 2)} - {Rd(price * d / 100, 2)}.", f"= ${Rd(sale, 2)}."],
             [f"${Rd(price * d / 100, 2)}", f"${Rd(price * (1 + F(d, 100)), 2)}", f"${Rd(price - d, 2)}"], AP(f"{D(price)}*(1 - {d}/100)", 2),
             why=["Gave the discount instead of the sale price", "Added the discount", "Subtracted the percent as dollars"])


@fam("012")
def s9_markup(r, L):
    cost = F(r.randint(5, 80))
    m = pick(r, [20, 25, 40, 50, 100]) if L < 2 else pick(r, [35, 65, 120, 150])
    sell = cost * (1 + F(m, 100))
    if L == 0 or r.random() < 0.5:
        return Q(f"A store buys an item for ${D(cost)} and marks it up {m}%. What is the selling price?", f"${Rd(sell, 2)}", [f"Markup: {m}% of {D(cost)} = {D(cost * m / 100)}.", f"Selling price: {D(cost)} + {D(cost * m / 100)}.", f"= ${Rd(sell, 2)}."],
                 [f"${Rd(cost * m / 100, 2)}", f"${Rd(cost * (1 - F(m, 100)), 2)}" if m < 100 else f"${Rd(cost * m, 2)}", f"${Rd(cost + m, 2)}"], AP(f"{D(cost)}*(1 + {m}/100)", 2),
                 why=["Gave only the markup", "Subtracted the markup", "Added the percent as dollars"])
    return Q(f"An item that costs the store ${D(cost)} sells for ${Rd(sell, 2)}. What is the percent markup?", f"{m}%", [f"Markup amount: {Rd(sell, 2)} - {D(cost)} = {D(sell - cost)}.", f"Percent = {D(sell - cost)} ÷ {D(cost)} × 100.", f"= {m}%."],
             [f"{Rd((sell - cost) / sell * 100, 1)}%" if not is_term((sell - cost) / sell * 100) else f"{D((sell - cost) / sell * 100)}%", f"{D(sell - cost)}%", f"{D(sell / cost * 100)}%"],
             PY("pct_change", old=D(cost), new=D(sell), bare=True), why=["Divided by the selling price instead of the cost", "Used the dollar markup as the percent", "Gave the selling price as a percent of cost"])


# ============================================================== S10 Tables
@fam("012")
def s10_missing(r, L):
    k = r.randint(2, 12) if L < 2 else F(r.randint(3, 15), 2)
    xs = sorted(r.sample(range(1, 12), 4))
    ys = [k * x for x in xs]
    need(all(F(y).denominator == 1 for y in ys))
    i = r.randrange(1, 4)
    shown_y = [N(y) if j != i else "?" for j, y in enumerate(ys)]
    alt = "Ratio table. x: " + ", ".join(map(str, xs)) + ". y: " + ", ".join(shown_y) + "."
    return Q(f"The table shows a proportional relationship (x: {', '.join(map(str, xs))}; y: {', '.join(shown_y)}). What is the missing y-value?", N(ys[i]),
             [f"Constant of proportionality: {N(ys[0])} ÷ {xs[0]} = {N(k)}.", f"y = {N(k)} × {xs[i]}.", f"y = {N(ys[i])}."],
             [N(ys[i - 1] + (xs[i] - xs[i - 1])), N(ys[i] + k), N(F(xs[i], 1) / k) if (F(xs[i]) / k).denominator == 1 else N(ys[i] - 1)], V(f"{N(ys[0])}/{xs[0]}*{xs[i]}"),
             why=["Added the change in x to y (additive thinking)", "", "Divided instead of multiplying"], tags=["multiple-representations"],
             diagram={"alt": alt, "draw": table_img([["x"] + [str(x) for x in xs], ["y"] + shown_y])} if L else None)


@fam("012")
def s10_is_prop(r, L):
    k = r.randint(2, 9)
    xs = sorted(r.sample(range(1, 12), 4))
    b = 0 if r.random() < 0.5 else r.randint(1, 5)
    ys = [k * x + b for x in xs]
    ok = b == 0
    return Q(f"Is the relationship proportional? x: {', '.join(map(str, xs))}; y: {', '.join(map(str, ys))}", "Yes" if ok else "No",
             ["Find y ÷ x for each pair.", ", ".join(f"{y}/{x}" for x, y in zip(xs, ys)) + ".", "Proportional only if every ratio is the same." + (" They are." if ok else " They are not.")],
             ["No" if ok else "Yes"], PY("prop_table", xs=xs, ys=ys), mode="sa", why=["Checked only that y increases"])


@fam("12")
def s10_constant(r, L):
    k = F(r.randint(2, 30), pick(r, [1, 2, 4]))
    xs = sorted(r.sample(range(2, 12), 3))
    ys = [k * x for x in xs]
    need(all(is_term(y) for y in ys))
    return Q(f"A table shows x: {', '.join(map(str, xs))} and y: {', '.join(D(y) for y in ys)}. Write an equation y = kx for the relationship.", f"y = {D(k) if is_term(k) else N(k)}x",
             ["k = y ÷ x for any pair.", f"k = {D(ys[0])} ÷ {xs[0]} = {D(k)}.", f"y = {D(k)}x."], [f"y = {N(1 / k)}x", f"y = x + {D(ys[0] - xs[0])}", f"y = {D(ys[0])}x"], PY("linear_rule", pts=[[x, str(y)] for x, y in zip(xs, ys)]),
             why=["Divided x by y", "Used a constant difference instead of a ratio", "Used a y-value as the constant"], tags=["multiple-representations"])


SKILLS = {
    1: dict(name="Ratios and Unit Rates", std=["6.RP.A.1", "6.RP.A.2", "7.RP.A.1"], fams=[s1_simplify, s1_unit_rate, s1_better], extra=[err_of(s1_unit_rate), open_of(s1_unit_rate), err_of(s1_simplify)]),
    2: dict(name="Proportions", std=["7.RP.A.2", "7.RP.A.3"], fams=[s2_solve, s2_is_prop, s2_context], extra=[err_of(s2_solve), open_of(s2_solve), select_of(s2_solve)]),
    3: dict(name="Similar Figures and Scale Drawings", std=["7.G.A.1"], fams=[s3_similar, s3_scale, s3_factor], extra=[err_of(s3_scale), open_of(s3_scale)]),
    4: dict(name="Probability", std=["7.SP.C.5", "7.SP.C.7a"], fams=[s4_simple, s4_die, s4_likely], extra=[err_of(s4_simple), open_of(s4_simple)]),
    5: dict(name="Fractions, Decimals, and Percentages", std=["6.RP.A.3c", "7.NS.A.2d"], fams=[s5_convert, s5_greatest], extra=[err_of(s5_convert), open_of(s5_convert), select_of(s5_convert)]),
    6: dict(name="Proportions and Percentages", std=["6.RP.A.3c", "7.RP.A.3"], fams=[s6_percent, s6_context], extra=[err_of(s6_percent), open_of(s6_percent), select_of(s6_percent)]),
    7: dict(name="Percentages and Equations", std=["7.RP.A.3", "7.EE.B.3"], fams=[s7_equation, s7_context], extra=[err_of(s7_equation), open_of(s7_equation)]),
    8: dict(name="Percent of Change", std=["7.RP.A.3"], fams=[s8_change], extra=[err_of(s8_change), open_of(s8_change)]),
    9: dict(name="Markup and Discount", std=["7.RP.A.3"], fams=[s9_discount, s9_markup], extra=[err_of(s9_discount), open_of(s9_discount)]),
    10: dict(name="Tables", std=["7.RP.A.2a", "7.RP.A.2b"], fams=[s10_missing, s10_is_prop, s10_constant], extra=[err_of(s10_missing), open_of(s10_constant)]),
}
