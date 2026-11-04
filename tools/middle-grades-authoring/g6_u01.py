"""Grade 6 Unit 1 — Ratios, Rate, Percent and Proportions (ratios-rates-percent-proportions)."""
from glib import *
import g7_u06 as R7, g7_u03 as D7, g7_u05 as F7

UNIT_ID = "ratios-rates-percent-proportions"
ABBR = "rrp"


# ============================================================== S1 Ratios
@fam("012")
def s1_language(r, L):
    a, b = r.sample(range(1, 10), 2)
    k = r.randint(2, 8)
    things = pick(r, [("cups of flour", "cups of sugar"), ("red tiles", "blue tiles"), ("dogs", "cats"), ("boys", "girls"), ("apples", "oranges")])
    if L == 0:
        return Q(f"For every {a} {things[0]} there are {b} {things[1]}. If there are {a * k} {things[0]}, how many {things[1]} are there?", str(b * k),
                 [f"The ratio is {a} : {b}.", f"{a * k} ÷ {a} = {k}, so multiply both parts by {k}.", f"{b} × {k} = {b * k} {things[1]}."],
                 [str(a * k + (b - a)), str(a * k * b), str(b + k)], V(f"{b}*{a * k}/{a}"), why=["Added the difference instead of multiplying (additive thinking)", "Multiplied by the wrong number", "Added instead of multiplying"])
    if L == 1:
        tot = (a + b) * k
        return Q(f"The ratio of {things[0]} to {things[1]} is {a} : {b}. There are {tot} in all. How many {things[0]} are there?", str(a * k),
                 [f"Total parts: {a} + {b} = {a + b}.", f"Each part is {tot} ÷ {a + b} = {k}.", f"{things[0].capitalize()}: {a} × {k} = {a * k}."],
                 [str(N(F(tot * a, b))) if (tot * a) % b == 0 else str(b * k), str(tot // 2) if tot % 2 == 0 else str(a * k + 1), str(b * k)], V(f"{tot}/({a} + {b})*{a}"),
                 why=["Used the ratio of the parts as if it were part to whole", "Split the total in half", "Found the other quantity"])
    c = r.randint(1, 9)
    need(c not in (a, b))
    tot = (a + b + c) * k
    return Q(f"A mix has red, blue, and green beads in the ratio {a} : {b} : {c}. There are {tot} beads in all. How many more blue beads than red beads are there?", str((b - a) * k) if b > a else str((a - b) * k),
             [f"Total parts: {a + b + c}.", f"Each part = {tot} ÷ {a + b + c} = {k}.", f"Red {a * k}, blue {b * k}.", f"Difference: {abs(b - a) * k}."],
             [str(abs(b - a)), str(b * k), str(abs(b - a) * k + k)], V(f"abs_diff_{abs(b - a)}*{k}".replace(f"abs_diff_{abs(b - a)}", str(abs(b - a)))), why=["Gave the difference in parts, not beads", "Gave the number of blue beads", ""],
             tags=["multistep"])


@fam("012", mode="mc")
def s1_which_ratio(r, L):
    a, b = r.sample(range(2, 12), 2)
    t = pick(r, [("wins", "losses", "games played"), ("girls", "boys", "students")])
    kind = pick(r, ["part-part", "part-whole"]) if L else "part-part"
    good = f"{a} : {b}" if kind == "part-part" else f"{a} : {a + b}"
    bad = [f"{b} : {a}", f"{a} : {a + b}" if kind == "part-part" else f"{a} : {b}", f"{a + b} : {a}"]
    opts = [(good, True)] + [(x, False) for x in bad]
    need(len({o[0] for o in opts}) == 4)
    r.shuffle(opts)
    q = f"A team has {a} {t[0]} and {b} {t[1]}. Which ratio compares {t[0]} to {'' + t[1] if kind == 'part-part' else t[2]}?"
    return Q(q, good, ["Write the quantities in the order the words give.", f"{t[0]} : {t[1] if kind == 'part-part' else t[2]} = {good}."], options=opts,
             chk=PY("ratio_pair", a=a, b=b if kind == "part-part" else a + b), mode="mc")


# ============================================================== S2 Unit Rate
@fam("012")
def s2_rate_use(r, L):
    u = r.randint(2, 9)
    rate = r.randint(3, 20)
    m = r.randint(2, 12)
    ctx = pick(r, [("A printer prints {t} pages in {u} minutes. At this rate, how many pages does it print in {m} minutes?", "pages"),
                   ("{nm} earns ${t} for {u} hours of work. At this rate, how much does {nm} earn in {m} hours?", "dollars"),
                   ("A car travels {t} miles on {u} gallons of gas. How far can it travel on {m} gallons?", "miles")])
    t, unit = ctx
    v = rate * m
    ans = f"${v}" if unit == "dollars" else f"{v} {unit}"
    return Q(t.format(t=rate * u, u=u, m=m, nm=name(r)), ans, [f"Unit rate: {rate * u} ÷ {u} = {rate} per one.", f"Multiply: {rate} × {m} = {v}.", f"Answer: {ans}."],
             [f"${rate * u * m}" if unit == "dollars" else f"{rate * u * m} {unit}", f"${rate * u + m - u}" if unit == "dollars" else f"{rate * u + m - u} {unit}", f"${rate + m}" if unit == "dollars" else f"{rate + m} {unit}"],
             V(f"{rate * u}/{u}*{m}"), why=["Multiplied the total by the new amount without finding the unit rate", "Added the difference instead of using the rate", "Added the rate and the amount"], tags=["modeling"])


# ============================================================== S3 Equivalent Ratios and Tables
@fam("012")
def s3_equiv(r, L):
    a, b = r.sample(range(1, 12), 2)
    k = r.randint(2, 9)
    pos = r.randrange(2)
    st = f"{a} : {b} = {a * k} : ?" if pos else f"{a} : {b} = ? : {b * k}"
    ans = b * k if pos else a * k
    return Q(f"Find the missing number to make equivalent ratios: {st}", str(ans), [f"The known term was multiplied by {k}.", f"Multiply the other term by {k}.", f"Missing number: {ans}."],
             [str((b if pos else a) + a * k - a if pos else a + b * k - b), str(ans + k), str(k)], PY("ratio_missing", a=a, b=b, pos=pos, k=k), why=["Added instead of multiplying", "", "Gave the scale factor"])


@fam("012", mode="mc")
def s3_table_equiv(r, L):
    a, b = r.sample(range(1, 10), 2)
    ks = sorted(r.sample(range(2, 9), 3))
    rows = [[(a * k, b * k) for k in ks], [(a * ks[0], b * ks[0]), (a * ks[1], b * ks[1] + a), (a * ks[2], b * ks[2])],
            [(a + k, b + k) for k in ks], [(a * k, b + k) for k in ks]]
    r.shuffle(rows)
    labs = "ABCD"
    tables = {f"Table {l}": rw for l, rw in zip(labs, rows)}
    good = [t for t, rw in tables.items() if all(F(x, y) == F(a, b) for x, y in rw)]
    need(len(good) == 1)
    desc = " ".join(f"{t}: " + ", ".join(f"({x}, {y})" for x, y in rw) + "." for t, rw in tables.items())
    return Q(f"Which table shows only ratios equivalent to {a} : {b}? {desc}", good[0], ["Equivalent ratios come from multiplying both parts by the same number.", f"Check each pair against {a} : {b}.", f"Only {good[0]} works."],
             options=[(t, t == good[0]) for t in tables], chk=PY("ratio_tables", a=a, b=b, tables=tables), mode="mc", tags=["multiple-representations"])


# ============================================================== S4 Comparing Ratios
@fam("012")
def s4_compare(r, L):
    a1, b1 = r.randint(1, 6), r.randint(2, 9)
    a2, b2 = r.randint(1, 6), r.randint(2, 9)
    need(F(a1, a1 + b1) != F(a2, a2 + b2) and (a1, b1) != (a2, b2))
    t = pick(r, [("juice", "water", "fruitier"), ("blue paint", "white paint", "bluer")])
    ans = "Mix A" if F(a1, b1) > F(a2, b2) else "Mix B"
    return Q(f"Mix A uses {a1} cups of {t[0]} for every {b1} cups of {t[1]}. Mix B uses {a2} cups of {t[0]} for every {b2} cups of {t[1]}. Which mix is {t[2]}?", ans,
             [f"Compare {t[0]} to {t[1]}: {a1}/{b1} and {a2}/{b2}.", f"Use a common denominator or unit rates: {Rd(F(a1, b1), 3)} and {Rd(F(a2, b2), 3)}.", f"{ans} has more {t[0]} per cup of {t[1]}."],
             ["Mix B" if ans == "Mix A" else "Mix A", "They are the same"], PY("mix_compare", a=[a1, b1], b=[a2, b2]), mode="sa", why=["Compared only the amounts of one ingredient", ""], tags=["reasoning"])


# ============================================================== S6 Percent and Rates per 100 / S7 Fraction as a Percent
@fam("012")
def s6_grid(r, L):
    n = r.randint(1, 99)
    what = pick(r, ["percent", "decimal", "fraction"]) if L else "percent"
    if what == "percent":
        return Q(f"{n} of the 100 squares on a grid are shaded. What percent of the grid is shaded?", f"{n}%", ["Percent means “per hundred.”", f"{n} out of 100 = {n}%."],
                 [f"{100 - n}%", f"{D(F(n, 100))}%", f"{n * 10}%"], V(str(n)), why=["Found the unshaded part", "Wrote the decimal with a percent sign", "Multiplied by 10"])
    if what == "decimal":
        return Q(f"{n} of 100 squares are shaded. Write the shaded part as a decimal.", D(F(n, 100)), ["n out of 100 = n hundredths.", f"{n} hundredths = {D(F(n, 100))}."],
                 [D(F(n, 10)), str(n), D(F(100 - n, 100))], V(f"{n}/100"), why=["Wrote tenths instead of hundredths", "Did not divide by 100", "Found the unshaded part"])
    return Q(f"{n} of 100 squares are shaded. Write the shaded part as a fraction in simplest form.", N(F(n, 100)), [f"{n}/100.", "Simplify.", f"{N(F(n, 100))}."],
             [f"{n}/100" if N(F(n, 100)) != f"{n}/100" else f"{n}/10", N(F(100 - n, 100)), N(F(100, n)) if 100 % n == 0 else f"100/{n}"], PY("frac_simplest", expr=f"{n}/100", mixed=False),
             why=["Did not simplify", "Found the unshaded part", "Flipped the fraction"])


@fam("012")
def s6_rate100(r, L):
    p = r.randint(1, 19) * 5 if L < 2 else r.randint(1, 99)
    w = pick(r, [20, 40, 50, 200, 300, 400]) if L else 100
    v = F(p * w, 100)
    need(v.denominator == 1)
    ctx = pick(r, ["of the students in a school ride the bus", "of the seats in a theater are filled", "of the songs on a playlist are pop songs"])
    return Q(f"{p}% {ctx}. If there are {w} in all, how many is that?", D(v), [f"{p}% = {p} per 100.", f"{p}/100 × {w} = {D(v)}." if w != 100 else f"{p} out of 100 = {p}."],
             [str(p), D(F(p * w, 10)), str(w - int(v))], V(f"{p}/100*{w}"), why=["Gave the percent instead of the amount", "Divided by 10 instead of 100", "Found the other part"], tags=["modeling"])


@fam("012")
def s7_to_percent(r, L):
    d = pick(r, [2, 4, 5, 10, 20, 25, 50]) if L == 0 else pick(r, [4, 5, 8, 20, 25, 40, 50]) if L == 1 else pick(r, [3, 6, 8, 12, 16, 40, 80])
    n = r.randint(1, d - 1)
    x = F(n, d)
    pv = x * 100
    if is_term(pv):
        ans = D(pv) + "%"
        chk = V(f"{n}/{d}*100")
    else:
        ans = Rd(pv, 1) + "%"
        chk = AP(f"{n}/{d}*100", 1)
    return Q(f"Write {n}/{d} as a percent." + (" Round to the nearest tenth of a percent." if not is_term(pv) else ""), ans,
             [f"Make the denominator 100, or divide: {n} ÷ {d} = {D(x) if is_term(x) else Rd(x, 4)}.", "Multiply by 100 and write %.", f"{n}/{d} = {ans}."],
             [f"{n}%", f"{d}%", f"{Rd(F(d, n) * 100, 1) if not is_term(F(d, n) * 100) else D(F(d, n) * 100)}%"], chk, why=["Used the numerator as the percent", "Used the denominator as the percent", "Divided in the wrong order"])


@fam("12")
def s7_context(r, L):
    d = pick(r, [20, 25, 40, 50])
    n = r.randint(1, d - 1)
    nm = name(r)
    return Q(f"{nm} answered {n} out of {d} questions correctly. What percent is that?", f"{D(F(n * 100, d))}%", [f"{n}/{d} = {D(F(n, d))}.", f"{D(F(n, d))} × 100 = {D(F(n * 100, d))}%."],
             [f"{n}%", f"{D(F((d - n) * 100, d))}%", f"{D(F(n, d))}%"], V(f"{n}/{d}*100"), why=["Used the count as the percent", "Found the percent missed", "Forgot to multiply by 100"], tags=["modeling"])


# ============================================================== S8 Ratio and Measurement Units
@fam("12")
def s8_rate_units(r, L):
    a = r.randint(2, 30)
    kind = pick(r, ["ft-s", "in-ft", "min-h"])
    if kind == "ft-s":
        return Q(f"A toy car travels {a} feet per second. How many feet does it travel per minute?", f"{a * 60} feet", ["1 minute = 60 seconds.", f"{a} × 60 = {a * 60} feet per minute."],
                 [f"{N(F(a, 60))} feet", f"{a + 60} feet", f"{a * 100} feet"], V(f"{a}*60"), why=["Divided instead of multiplying", "Added instead of multiplying", "Used 100 seconds per minute"])
    if kind == "in-ft":
        return Q(f"A plant grows {a * 12} inches in a year. How many feet is that?", f"{a} feet", ["12 inches = 1 foot.", f"{a * 12} ÷ 12 = {a} feet."],
                 [f"{a * 144} feet", f"{a * 12 - 12} feet", f"{N(F(a * 12, 3))} feet"], V(f"{a * 12}/12"), why=["Multiplied instead of dividing", "Subtracted 12", "Used 3 inches per foot"])
    return Q(f"A machine fills {a} bottles per minute. How many bottles does it fill in {r.randint(2, 4)} hours?" if False else f"A machine fills {a} bottles per minute. How many bottles does it fill in one hour?",
             f"{a * 60} bottles", ["1 hour = 60 minutes.", f"{a} × 60 = {a * 60} bottles."], [f"{a * 100} bottles", f"{a + 60} bottles", f"{N(F(a, 60))} bottles"], V(f"{a}*60"),
             why=["Used 100 minutes per hour", "Added instead of multiplying", "Divided instead of multiplying"])


SKILLS = {
    1: dict(name="Ratios", std=["6.RP.A.1"], fams=[s1_language, s1_which_ratio, reuse(R7.s1_simplify)], extra=[err_of(s1_language), open_of(s1_language), select_of(reuse(R7.s1_simplify, (0, 0, 1), "b"))]),
    2: dict(name="Unit Rate", std=["6.RP.A.2", "6.RP.A.3b"], fams=[reuse(R7.s1_unit_rate, (0, 1, 1)), s2_rate_use, reuse(R7.s1_better)], extra=[err_of(s2_rate_use), open_of(s2_rate_use)]),
    3: dict(name="Equivalent Ratios and Tables", std=["6.RP.A.3a"], fams=[s3_equiv, s3_table_equiv, reuse(R7.s10_missing, (0, 1, 1))], extra=[err_of(s3_equiv), open_of(s3_equiv), select_of(s3_equiv)]),
    4: dict(name="Comparing Ratios", std=["6.RP.A.3a", "6.RP.A.3b"], fams=[s4_compare, reuse(R7.s1_better, (0, 1, 2), "c"), reuse(R7.s10_is_prop)], extra=[err_of(reuse(R7.s1_unit_rate, (0, 1, 1), "c")), open_of(s4_compare)]),
    5: dict(name="Proportions", std=["6.RP.A.3", "7.RP.A.2c"], fams=[reuse(R7.s2_solve, (0, 1, 1)), reuse(R7.s2_context), reuse(R7.s2_is_prop)], extra=[err_of(reuse(R7.s2_solve, (0, 1, 1), "e")), open_of(reuse(R7.s2_context, (0, 1, 2), "o"))]),
    6: dict(name="Percent and Rates per 100", std=["6.RP.A.3c"], fams=[s6_grid, s6_rate100, reuse(R7.s6_percent, (0, 0, 1))], extra=[err_of(s6_rate100), open_of(s6_grid), select_of(s6_rate100)]),
    7: dict(name="A Fraction as a Percent", std=["6.RP.A.3c"], fams=[s7_to_percent, s7_context, reuse(R7.s5_greatest)], extra=[err_of(s7_to_percent), open_of(s7_to_percent), select_of(s7_to_percent)]),
    8: dict(name="Ratio and Measurement Units", std=["6.RP.A.3d"], fams=[reuse(D7.s7_convert, (0, 1, 1)), reuse(F7.s5_convert, (0, 1, 1)), s8_rate_units, reuse(F7.s5_multi, (2, 2, 2))],
            extra=[err_of(reuse(F7.s5_convert, (0, 1, 1), "e")), open_of(reuse(D7.s7_convert, (0, 1, 1), "o"))]),
}
