"""Grade 7 Unit 12 — Data Analysis and Probability (data-analysis-probability)."""
from glib import *
from collections import Counter

UNIT_ID = "data-analysis-probability"
ABBR = "dap"


def med(a):
    a = sorted(a)
    k = len(a)
    return F(a[k // 2]) if k % 2 else F(a[k // 2 - 1] + a[k // 2], 2)


def five(a):
    a = sorted(a)
    n = len(a)
    return [F(a[0]), med(a[: n // 2]), med(a), med(a[(n + 1) // 2:]), F(a[-1])]


# ============================================================== S1 Frequency tables, line plots, histograms
@fam("012")
def s1_table(r, L):
    cats = pick(r, [["0–9", "10–19", "20–29", "30–39"], ["0–4", "5–9", "10–14", "15–19", "20–24"], ["50–59", "60–69", "70–79", "80–89", "90–99"]])
    fr = [r.randint(1, 12) for _ in cats]
    i = r.randrange(len(cats))
    kind = pick(r, ["count", "total", "atleast"]) if L else pick(r, ["count", "total"])
    alt = "Histogram. Intervals " + ", ".join(f"{c}: {f}" for c, f in zip(cats, fr)) + "."
    diag = {"alt": alt, "draw": bar_draw(cats, fr, ylabel="Frequency", hist=True, ystep=1)}
    if kind == "count":
        return Q(f"The histogram shows test data. How many values are in the interval {cats[i]}?", str(fr[i]), [f"Read the height of the bar for {cats[i]}.", f"It is {fr[i]}."],
                 [str(fr[(i + 1) % len(fr)]), str(sum(fr)), str(fr[i] + 1)], V(str(fr[i])), why=["Read the neighboring bar", "Gave the total", "Misread the scale"], diagram=diag, tags=["graph"])
    if kind == "total":
        return Q("The histogram shows data. How many values are in the data set altogether?", str(sum(fr)), ["Add the heights of all the bars.", " + ".join(map(str, fr)) + f" = {sum(fr)}."],
                 [str(len(fr)), str(max(fr)), str(sum(fr) - fr[0])], V(" + ".join(map(str, fr))), why=["Counted the bars instead of the values", "Gave the tallest bar", "Left out a bar"], diagram=diag, tags=["graph"])
    k = sum(fr[i:])
    return Q(f"The histogram shows data. How many values are in the interval {cats[i]} or higher?", str(k), [f"Add the bars from {cats[i]} up: " + " + ".join(map(str, fr[i:])) + f" = {k}."],
             [str(sum(fr[i + 1:])), str(sum(fr[: i + 1])), str(fr[i])], V(" + ".join(map(str, fr[i:]))), why=["Left out the starting interval", "Added the wrong side", "Used only one bar"], diagram=diag, tags=["graph"])


@fam("012")
def s1_lineplot(r, L):
    lo = r.randint(0, 5)
    vals = [r.randint(lo, lo + 6) for _ in range(r.randint(10, 16))]
    c = Counter(vals)
    q = pick(r, ["mode", "count", "range"]) if L < 2 else pick(r, ["mean_r", "median"])
    alt = "Line plot (dot plot). " + ", ".join(f"{v}: {c[v]} dot{'s' if c[v] != 1 else ''}" for v in range(lo, lo + 7)) + "."
    diag = {"alt": alt, "draw": dot_draw(vals, lo, lo + 6)}
    if q == "mode":
        top = max(c.values())
        need(list(c.values()).count(top) == 1)
        m = [v for v in c if c[v] == top][0]
        return Q("The line plot shows the number of books students read. What is the mode?", str(m), ["The mode is the value with the most dots.", f"{m} has {top} dots."],
                 [str(top), str(max(vals)), str(int(med(vals))) if med(vals).denominator == 1 and med(vals) != m else str(m + 1)], PY("stat", data=[str(v) for v in vals], stat="mode"),
                 why=["Gave the number of dots instead of the value", "Gave the greatest value", "Gave the median"], diagram=diag, tags=["graph"])
    if q == "count":
        k = r.randint(lo + 1, lo + 5)
        n = sum(1 for v in vals if v >= k)
        return Q(f"The line plot shows the number of books students read. How many students read at least {k} books?", str(n), [f"Count the dots at {k} and above.", f"{n} students."],
                 [str(sum(1 for v in vals if v > k)), str(len(vals) - n), str(len(vals))], PY("count_ge", data=vals, k=k), why=["Did not include the value itself", "Counted the other side", "Counted all students"],
                 diagram=diag, tags=["graph"])
    if q == "range":
        return Q("The line plot shows the number of books students read. What is the range?", str(max(vals) - min(vals)), ["Range = greatest - least.", f"{max(vals)} - {min(vals)} = {max(vals) - min(vals)}."],
                 [str(max(vals)), str(len(vals)), str(max(c.values()))], PY("stat", data=[str(v) for v in vals], stat="range"), why=["Gave the greatest value", "Counted the dots", "Gave the tallest column"], diagram=diag, tags=["graph"])
    return Q("The line plot shows the number of books students read. What is the median?", D(med(vals)), [f"There are {len(vals)} values.", "Find the middle value (average the two middle values if needed).", f"Median = {D(med(vals))}."],
             [D(sum(vals) / F(len(vals))) if is_term(sum(vals) / F(len(vals))) and sum(vals) / F(len(vals)) != med(vals) else D(med(vals) + 1), str(lo + 3), D(med(vals) - F(1, 2))],
             PY("stat", data=[str(v) for v in vals], stat="median"), why=["Gave the mean", "Used the middle of the number line", "Took the wrong middle value"], diagram=diag, tags=["graph"])


@fam("012")
def s1_freq_text(r, L):
    cats = pick(r, [["0–9", "10–19", "20–29", "30–39"], ["50–59", "60–69", "70–79", "80–89", "90–99"], ["1–5", "6–10", "11–15", "16–20"]])
    fr = [r.randint(1, 15) for _ in cats]
    tab = "; ".join(f"{c}: {f}" for c, f in zip(cats, fr))
    kind = pick(r, ["below", "most", "total"]) if L else pick(r, ["most", "total"])
    if kind == "most":
        need(fr.count(max(fr)) == 1)
        ans = cats[fr.index(max(fr))]
        others = [c for c in cats if c != ans]
        return Q(f"A frequency table shows the number of values in each interval: {tab}. Which interval has the most values?", ans, ["Compare the frequencies.", f"The greatest frequency is {max(fr)}, for {ans}."],
                 others, PY("freq_most", cats=cats, fr=fr), why=["Chose an interval that does not have the greatest frequency"] * len(others))
    if kind == "total":
        return Q(f"A frequency table shows the number of values in each interval: {tab}. How many values are there in all?", str(sum(fr)), ["Add all the frequencies.", " + ".join(map(str, fr)) + f" = {sum(fr)}."],
                 [str(len(cats)), str(max(fr)), str(sum(fr) - fr[-1])], V(" + ".join(map(str, fr))), why=["Counted the intervals", "Gave the greatest frequency", "Left out an interval"])
    i = r.randrange(1, len(cats))
    k = sum(fr[:i])
    return Q(f"A frequency table shows the number of values in each interval: {tab}. How many values are less than the start of the interval {cats[i]}?", str(k), [f"Add the frequencies of the intervals before {cats[i]}.", " + ".join(map(str, fr[:i])) + f" = {k}."],
             [str(sum(fr[: i + 1])), str(sum(fr[i:])), str(fr[i - 1])], V(" + ".join(map(str, fr[:i]))), why=["Included the interval itself", "Added the wrong side", "Used only one interval"])


# ============================================================== S2 Box-and-whisker
@fam("012")
def s2_summary(r, L):
    n = r.randint(7, 11)
    vals = sorted(r.randint(10, 60) for _ in range(n))
    st = pick(r, ["median", "q1", "q3", "iqr"] if L else ["median", "min", "max", "range"])
    f5 = five(vals)
    v = {"median": f5[2], "q1": f5[1], "q3": f5[3], "iqr": f5[3] - f5[1], "min": f5[0], "max": f5[4], "range": f5[4] - f5[0]}[st]
    nm = {"median": "median", "q1": "lower quartile (Q1)", "q3": "upper quartile (Q3)", "iqr": "interquartile range", "min": "minimum", "max": "maximum", "range": "range"}[st]
    return Q(f"Data: {', '.join(map(str, vals))}. Find the {nm}.", D(v), ["Order the data (already ordered).", f"Median = {D(f5[2])}; Q1 = {D(f5[1])} (median of the lower half); Q3 = {D(f5[3])} (median of the upper half).", f"The {nm} is {D(v)}."],
             [D(x) for x in {f5[2], f5[1], f5[3], f5[3] - f5[1], f5[4] - f5[0]} - {v}][:3], PY("stat", data=[str(x) for x in vals], stat=st), why=["Gave a different part of the five-number summary"] * 3)


@fam("012")
def s2_read(r, L):
    a = sorted(r.sample(range(2, 19), 5))
    a = [5 * x for x in a]
    st = pick(r, ["median", "q1", "q3", "iqr", "range"])
    v = {"median": a[2], "q1": a[1], "q3": a[3], "iqr": a[3] - a[1], "range": a[4] - a[0]}[st]
    nm = {"median": "median", "q1": "lower quartile", "q3": "upper quartile", "iqr": "interquartile range", "range": "range"}[st]
    alt = f"Box-and-whisker plot on a scale from 0 to 100: minimum {a[0]}, lower quartile {a[1]}, median {a[2]}, upper quartile {a[3]}, maximum {a[4]}."
    return Q(f"Use the box-and-whisker plot. What is the {nm}?", str(v), ["The box runs from the lower quartile to the upper quartile; the line inside is the median.", "The whiskers reach the minimum and maximum.", f"The {nm} is {v}."],
             [str(x) for x in {a[2], a[1], a[3], a[3] - a[1], a[4] - a[0]} - {v}][:3], PY("box_read", five=a, stat=st), why=["Read a different part of the plot"] * 3,
             diagram={"alt": alt, "draw": box_draw(a, 0, 100, 5)}, tags=["graph"])


@fam("2", mode="mc")
def s2_compare(r, L):
    a = sorted(r.sample(range(10, 90), 5))
    b = sorted(r.sample(range(10, 90), 5))
    need(abs(a[2] - b[2]) >= 8 and abs((a[3] - a[1]) - (b[3] - b[1])) >= 8)
    q = pick(r, ["median", "iqr"])
    va, vb = (a[2], b[2]) if q == "median" else (a[3] - a[1], b[3] - b[1])
    good = f"Class {'A' if va > vb else 'B'} has the greater {'median' if q == 'median' else 'interquartile range'}."
    bad = f"Class {'B' if va > vb else 'A'} has the greater {'median' if q == 'median' else 'interquartile range'}."
    opts = [(good, True), (bad, False), (f"The classes have the same {'median' if q == 'median' else 'interquartile range'}.", False), ("The plots cannot be compared.", False)]
    r.shuffle(opts)
    alt = f"Two box plots. Class A: min {a[0]}, Q1 {a[1]}, median {a[2]}, Q3 {a[3]}, max {a[4]}. Class B: min {b[0]}, Q1 {b[1]}, median {b[2]}, Q3 {b[3]}, max {b[4]}."
    return Q(f"The box plots compare test scores for two classes. Which statement is true?", good, [f"Class A: {'median ' + str(a[2]) if q == 'median' else 'IQR ' + str(a[3] - a[1])}.", f"Class B: {'median ' + str(b[2]) if q == 'median' else 'IQR ' + str(b[3] - b[1])}.", good],
             options=opts, chk=PY("box_compare", a=a, b=b, q=q), mode="mc", tags=["graph", "reasoning"], diagram={"alt": alt, "draw": box_draw(a, 0, 100, 10, second=b, names=("Class A", "Class B"))})


# ============================================================== S3 Stem and leaf
def stem_text(vals):
    by = {}
    for v in sorted(vals):
        by.setdefault(v // 10, []).append(v % 10)
    return "; ".join(f"{s} | {' '.join(map(str, ls))}" for s, ls in sorted(by.items()))


@fam("012")
def s3_stat(r, L):
    n = r.randint(8, 13)
    vals = sorted(r.randint(12, 79) for _ in range(n))
    st = pick(r, ["median", "range", "mode", "min"]) if L < 2 else pick(r, ["median", "iqr", "mean"])
    if st == "mode":
        vals = sorted(vals + [r.choice(vals)])
        c = Counter(vals)
        need(list(c.values()).count(max(c.values())) == 1)
    if st == "mean":
        need(is_term(sum(vals) / F(len(vals))) and (sum(vals) / F(len(vals))).denominator <= 10)
    s = stem_text(vals)
    f5 = five(vals)
    v = {"median": f5[2], "range": f5[4] - f5[0], "mode": F(Counter(vals).most_common(1)[0][0]), "min": f5[0], "iqr": f5[3] - f5[1], "mean": sum(vals) / F(len(vals))}[st]
    return Q(f"The stem-and-leaf plot (key: 3 | 4 means 34) shows ages: {s}. Find the {st if st != 'iqr' else 'interquartile range'}{' (least value)' if st == 'min' else ''}.", D(v),
             ["Read each value: stem is the tens digit, leaf is the ones digit.", f"Values: {', '.join(map(str, vals))}.", f"The {st} is {D(v)}."],
             [D(x) for x in ({f5[2], f5[4] - f5[0], f5[0], f5[4], F(vals[len(vals) // 2])} - {v})][:3], PY("stat", data=[str(x) for x in vals], stat=st),
             why=["Found a different statistic"] * 3, tags=["multiple-representations"])


@fam("12")
def s3_count(r, L):
    vals = sorted(r.randint(12, 79) for _ in range(r.randint(9, 14)))
    k = r.randint(30, 60)
    n = sum(1 for v in vals if v > k)
    return Q(f"The stem-and-leaf plot (key: 3 | 4 means 34) shows scores: {stem_text(vals)}. How many scores are greater than {k}?", str(n), ["Read each value from the plot.", f"Count the values greater than {k}.", f"{n} scores."],
             [str(sum(1 for v in vals if v >= k)) if sum(1 for v in vals if v >= k) != n else str(n + 1), str(len(vals) - n), str(len(vals))], PY("count_gt", data=vals, k=k),
             why=["Included values equal to the number", "Counted the other side", "Counted all values"])


# ============================================================== S4 Counting outcomes & theoretical probability
@fam("012")
def s4_count(r, L):
    a, b, c = r.randint(2, 6), r.randint(2, 5), r.randint(2, 4)
    if L == 0:
        return Q(f"A café offers {a} sandwiches and {b} drinks. How many different sandwich-and-drink meals are possible?", str(a * b), ["Use the Counting Principle: multiply the number of choices.", f"{a} × {b} = {a * b}."],
                 [str(a + b), str(a * b * 2), str(max(a, b))], V(f"{a}*{b}"), why=["Added instead of multiplying", "", ""])
    if L == 1:
        return Q(f"An outfit has {a} shirts, {b} pants, and {c} pairs of shoes to choose from. How many outfits are possible?", str(a * b * c), ["Counting Principle.", f"{a} × {b} × {c} = {a * b * c}."],
                 [str(a + b + c), str(a * b + c), str(a * b)], V(f"{a}*{b}*{c}"), why=["Added instead of multiplying", "Added the last choice", "Left out a choice"])
    kind = pick(r, ["code", "plate", "norepeat", "menu"])
    if kind == "plate":
        nl, nd = r.randint(1, 3), r.randint(2, 4)
        v = 26 ** nl * 10 ** nd
        return Q(f"A license plate has {nl} letter{'s' if nl > 1 else ''} (A–Z) followed by {nd} digits (0–9). Letters and digits may repeat. How many plates are possible?", f"{v:,}",
                 ["Counting Principle: multiply the choices for each position.", f"26{sup(nl) if nl > 1 else ''} × 10{sup(nd)}.", f"= {v:,}."], [f"{26 * nl + 10 * nd:,}", f"{26 ** nl + 10 ** nd:,}", f"{36 ** (nl + nd):,}"],
                 V(f"26^{nl}*10^{nd}"), why=["Multiplied choices by the number of positions", "Added instead of multiplying", "Let every position be any letter or digit"])
    if kind == "norepeat":
        k = r.randint(3, 5)
        v = math.perm(10, k)
        return Q(f"A {k}-digit code uses digits 0–9, and no digit may repeat. How many codes are possible?", f"{v:,}", [f"10 choices, then 9, then 8, and so on for {k} positions.", " × ".join(str(10 - i) for i in range(k)) + f" = {v:,}."],
                 [f"{10 ** k:,}", f"{math.comb(10, k):,}", f"{10 * k}"], V("*".join(str(10 - i) for i in range(k))), why=["Allowed digits to repeat", "Treated order as not mattering", "Multiplied 10 by the number of digits"])
    if kind == "menu":
        a, b, c, d = r.randint(3, 8), r.randint(2, 6), r.randint(2, 5), r.randint(2, 4)
        return Q(f"A meal deal has {a} mains, {b} sides, {c} drinks, and {d} desserts. A meal includes one of each. How many different meals are possible?", str(a * b * c * d),
                 ["Counting Principle.", f"{a} × {b} × {c} × {d} = {a * b * c * d}."], [str(a + b + c + d), str(a * b * c), str(a * b + c * d)], V(f"{a}*{b}*{c}*{d}"), why=["Added instead of multiplying", "Left out a category", ""])
    k = r.randint(3, 4)
    return Q(f"A code uses {k} digits (0–9), and digits may repeat. How many codes are possible?", f"{10 ** k:,}", [f"Each position has 10 choices.", f"10{sup(k)} = {10 ** k:,}."],
             [str(10 * k), f"{10 * 9 * 8 * (7 if k == 4 else 1):,}", str(9 ** k)], V(f"10^{k}"), why=["Multiplied 10 by the number of digits", "Did not allow repeats", "Left out the digit 0"])


@fam("012")
def s4_prob(r, L):
    if L == 0:
        n = pick(r, [6, 8, 10])
        k = r.randint(1, n - 1)
        return Q(f"A spinner has {n} equal sections numbered 1 to {n}. What is P(a number less than or equal to {k})? Write a fraction in simplest form.", N(F(k, n)),
                 [f"Favorable outcomes: 1 to {k}, which is {k}.", f"P = {k}/{n} = {N(F(k, n))}."], [N(F(k - 1, n)) if k > 1 else N(F(k + 1, n)), N(F(n - k, n)) if F(n - k, n) != F(k, n) else N(F(k, n + 1)), f"{k}/{n + 1}"],
                 PY("frac_simplest", expr=f"{k}/{n}", mixed=False), why=["Did not include the number itself", "Found the complement", "Used the wrong total"])
    if r.random() < 0.5:
        n = r.randint(2, 4)
        kind = pick(r, ["exactly", "atleast"])
        k = r.randint(1, n)
        cnt = math.comb(n, k) if kind == "exactly" else 2 ** n - 1
        t = f"exactly {k} head{'s' if k > 1 else ''}" if kind == "exactly" else "at least one head"
        return Q(f"A fair coin is tossed {n} times. What is P({t})? Write a fraction in simplest form.", N(F(cnt, 2 ** n)), [f"There are 2{sup(n)} = {2 ** n} equally likely outcomes.", f"Outcomes with {t}: {cnt}.", f"P = {cnt}/{2 ** n} = {N(F(cnt, 2 ** n))}."],
                 [N(F(1, 2 ** n)), N(F(k, n)) if F(k, n) != F(cnt, 2 ** n) else N(F(1, n + 1)), N(F(cnt, 2 * n)) if F(cnt, 2 * n) != F(cnt, 2 ** n) and F(cnt, 2 * n) <= 1 else N(F(cnt + 1, 2 ** n))],
                 PY("coin_prob", n=n, mode=kind, k=k), why=["Counted only one outcome", "Assumed the numbers of heads are equally likely", "Used 2n instead of 2 to the n as the number of outcomes"])
    s = pick(r, [(7, "a sum of 7", 6), (8, "a sum of 8", 5), (10, "a sum of 10", 3), (12, "a sum of 12", 1), (5, "a sum of 5", 4), (0, "doubles", 6)])
    _, t, k = s
    return Q(f"Two number cubes are rolled. What is P({t})? Write a fraction in simplest form.", N(F(k, 36)), ["There are 6 × 6 = 36 equally likely outcomes.", f"Count the outcomes with {t}: {k}.", f"P = {k}/36 = {N(F(k, 36))}."],
             [N(F(k, 12)), N(F(1, 11)), N(F(k, 6))], PY("dice_prob", event=t), why=["Used 12 as the number of outcomes", "Counted the possible sums as equally likely", "Used only one die"])


# ============================================================== S5 Independent and dependent events
@fam("012")
def s5_indep(r, L):
    a = pick(r, [F(1, 2), F(1, 3), F(1, 6), F(1, 4)])
    t1 = {F(1, 2): "heads on a coin", F(1, 3): "a 1 or 2 on a number cube", F(1, 6): "a 6 on a number cube", F(1, 4): "red on a 4-color spinner"}[a]
    b = pick(r, [F(1, 2), F(1, 6), F(1, 4), F(1, 3)])
    t2 = {F(1, 2): "an even number on a number cube", F(1, 6): "a 3 on a number cube", F(1, 4): "blue on a 4-color spinner", F(1, 3): "a number greater than 4 on a number cube"}[b]
    need(t1 != t2)
    return Q(f"Find the probability of getting {t1} and {t2}. Write a fraction.", N(a * b), ["The events are independent.", f"P(A and B) = P(A) × P(B) = {N(a)} × {N(b)}.", f"= {N(a * b)}."],
             [N(a + b), N(a * b * 2), N((a + b) / 2)], PY("frac_simplest", expr=f"{N(a)}*{N(b)}", mixed=False), why=["Added the probabilities", "", "Averaged the probabilities"])


@fam("012")
def s5_bag(r, L):
    red, blue = r.randint(2, 8), r.randint(2, 8)
    tot = red + blue
    repl = L == 0 or r.random() < 0.4
    p = F(red, tot) * (F(red, tot) if repl else F(red - 1, tot - 1))
    return Q(f"A bag has {red} red and {blue} blue marbles. You draw a marble, {'replace it' if repl else 'do NOT replace it'}, and draw again. What is P(red, then red)? Write a fraction in simplest form.", N(p),
             [f"P(first red) = {red}/{tot}.", f"P(second red) = {red}/{tot}." if repl else f"After removing a red marble: {red - 1}/{tot - 1}.", f"P = {red}/{tot} × {(red if repl else red - 1)}/{(tot if repl else tot - 1)} = {N(p)}."],
             [N(F(red, tot) ** 2) if not repl else N(F(red, tot) * F(red - 1, tot - 1)), N(F(red, tot) * 2) if F(red, tot) * 2 <= 1 else N(F(red, tot)), N(F(red, tot) + F(red - 1, tot - 1))],
             PY("bag_prob", red=red, blue=blue, repl=repl), why=["Treated the draws as with replacement" if not repl else "Treated the draws as without replacement", "Added instead of multiplying", "Added the probabilities"])


@fam("12", mode="mc")
def s5_classify(r, L):
    items = [("Rolling a number cube and flipping a coin", "independent"), ("Drawing two cards from a deck without replacing the first", "dependent"),
             ("Drawing a marble, replacing it, and drawing again", "independent"), ("Choosing a student, then choosing a second student from those left", "dependent"),
             ("Spinning a spinner twice", "independent"), ("Picking two socks from a drawer at the same time", "dependent")]
    t, k = pick(r, items)
    opts = [("independent", k == "independent"), ("dependent", k == "dependent"), ("mutually exclusive", False), ("impossible", False)]
    return Q(f"Are the events independent or dependent? {t}.", k, ["Events are dependent if the first outcome changes the probabilities for the second.", f"These events are {k}."], options=opts, chk=TXT(k), mode="mc")


# ============================================================== S6 Permutations and combinations
@fam("012")
def s6_perm(r, L):
    n = r.randint(4, 10)
    k = r.randint(2, 3) if L < 2 else r.randint(2, 4)
    kind = pick(r, ["perm", "comb"]) if L else "perm"
    pr = math.perm(n, k)
    co = math.comb(n, k)
    prod = " × ".join(str(n - i) for i in range(k))
    if kind == "perm":
        return Q(f"In how many ways can 1st, 2nd{', and 3rd' if k == 3 else ''}{', 3rd, and 4th' if k == 4 else ''} place be awarded among {n} runners?", str(pr),
                 ["Order matters, so this is a permutation.", f"{n}P{k} = {prod}.", f"= {pr}."], [str(co), str(n ** k), str(n * k)], V(prod.replace("×", "*")),
                 why=["Treated it as a combination (order does not matter)", "Allowed the same runner twice", "Multiplied n by k"])
    return Q(f"How many different {k}-person committees can be chosen from {n} people?", str(co), ["Order does not matter, so this is a combination.", f"{n}C{k} = ({prod}) ÷ {k}! = {pr} ÷ {math.factorial(k)}.", f"= {co}."],
             [str(pr), str(n * k), str(math.comb(n, k - 1) if math.comb(n, k - 1) != co else co + 1)], V(f"({prod.replace('×', '*')})/{math.factorial(k)}"),
             why=["Treated it as a permutation (order matters)", "Multiplied n by k", "Chose one too few people"])


@fam("012")
def s6_arrange(r, L):
    n = r.randint(3, 7)
    return Q(f"In how many different orders can {n} books be placed on a shelf?", f"{math.factorial(n):,}", [f"{n} choices for the first spot, {n - 1} for the next, and so on.", f"{n}! = {' × '.join(str(i) for i in range(n, 0, -1))} = {math.factorial(n):,}."],
             [str(n * n), str(n * (n - 1)), f"{2 ** n}"], V("*".join(str(i) for i in range(n, 0, -1))), why=["Squared the number of books", "Stopped after two places", ""])


# ============================================================== S7 Experimental probability
@fam("012")
def s7_exp(r, L):
    trials = pick(r, [20, 25, 40, 50, 60, 80, 100])
    hits = r.randint(2, trials - 2)
    ev = pick(r, ["the spinner landed on blue", "a free throw went in", "the bus was late", "a seed sprouted"])
    p = F(hits, trials)
    if L == 0 or r.random() < 0.5:
        return Q(f"In {trials} trials, {ev} {hits} times. What is the experimental probability? Write a fraction in simplest form.", N(p), ["Experimental probability = number of times the event happened ÷ number of trials.", f"{hits}/{trials} = {N(p)}."],
                 [N(F(trials - hits, trials)), N(F(hits, trials - hits)), f"{hits}/{trials + 1}"], PY("frac_simplest", expr=f"{hits}/{trials}", mixed=False), why=["Found the complement", "Compared successes to failures", "Used the wrong total"])
    m = pick(r, [200, 300, 500, 1000])
    need((p * m).denominator == 1)
    return Q(f"In {trials} trials, {ev} {hits} times. Predict how many times it will happen in {m} trials.", str(int(p * m)), [f"Experimental probability = {N(p)}.", f"{N(p)} × {m} = {int(p * m)}."],
             [str(hits * m), str(m - int(p * m)), str(hits + m - trials)], V(f"{hits}/{trials}*{m}"), why=["Multiplied the count by the new number of trials", "Predicted the complement", "Added the extra trials"], tags=["modeling"])


@fam("12", mode="mc")
def s7_compare(r, L):
    n = pick(r, [10, 20, 30])
    k = r.randint(0, n)
    opts = [("Experimental probability gets closer to theoretical probability as the number of trials increases.", True), ("Experimental probability always equals theoretical probability.", False),
            ("More trials make experimental probability less reliable.", False), ("Theoretical probability changes after each trial.", False)]
    r.shuffle(opts)
    return Q(f"A fair coin is tossed {n} times and lands heads {k} times. Which statement about the experimental and theoretical probabilities is true?", opts[[o[1] for o in opts].index(True)][0],
             [f"Theoretical P(heads) = 1/2; experimental = {k}/{n}.", "They often differ for small numbers of trials.", "With many trials, the experimental probability tends to approach 1/2."], options=opts,
             chk=TXT("Experimental probability gets closer to theoretical probability as the number of trials increases."), mode="mc", tags=["reasoning"])


# ============================================================== S8 Random samples and surveys
@fam("012", mode="mc")
def s8_bias(r, L):
    good = pick(r, ["Choose 50 students at random from the full school roster.", "Number every household and use a random number generator to pick 100.", "Survey every 10th person on an alphabetical list of all members."])
    bad = r.sample(["Ask the first 30 students who arrive at basketball practice.", "Survey only your friends.", "Post an online poll that people can choose to answer.",
                    "Ask people leaving a pizza shop about their favorite food.", "Survey students in one honors class about homework load."], 3)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q("A school wants to know students' favorite lunch. Which sampling method is most likely to give a representative (unbiased) sample?", good,
             ["A random sample gives every member of the population an equal chance to be chosen.", "Convenience and voluntary samples are biased."], options=opts, chk=TXT(good), mode="mc", tags=["reasoning"])


@fam("012")
def s8_predict(r, L):
    n = pick(r, [20, 25, 40, 50, 80])
    k = r.randint(2, n - 2)
    pop = pick(r, [400, 500, 600, 800, 1000, 1200])
    need((F(k, n) * pop).denominator == 1)
    t = pick(r, ["prefer pizza", "walk to school", "own a pet", "play an instrument"])
    return Q(f"In a random sample of {n} students, {k} {t}. Predict how many of the school's {pop} students {t}.", str(int(F(k, n) * pop)),
             [f"Sample proportion: {k}/{n}.", f"Proportion: {k}/{n} = x/{pop}.", f"x = {k} × {pop} ÷ {n} = {int(F(k, n) * pop)}."],
             [str(k * pop // n * 2 if k * pop // n * 2 <= pop else k), str(pop - int(F(k, n) * pop)), str(k + pop - n)], V(f"{k}/{n}*{pop}"),
             why=["", "Predicted the students who do NOT", "Added the population difference"], tags=["modeling"])


SKILLS = {
    1: dict(name="Frequency Tables, Line Plots, and Histograms", std=["6.SP.B.4", "6.SP.B.5a"], fams=[s1_table, s1_lineplot, s1_freq_text], extra=[err_of(s1_table), err_of(s1_lineplot), err_of(s1_freq_text), open_of(s1_freq_text)]),
    2: dict(name="Box-and-Whisker Plots", std=["6.SP.B.4", "6.SP.B.5c"], fams=[s2_summary, s2_read, s2_compare], extra=[err_of(s2_summary), open_of(s2_summary)]),
    3: dict(name="Stem and Leaf Plots", std=["6.SP.B.4", "6.SP.B.5c"], fams=[s3_stat, s3_count], extra=[err_of(s3_stat), open_of(s3_stat)]),
    4: dict(name="Counting Outcomes and Theoretical Probability", std=["7.SP.C.7a", "7.SP.C.8b"], fams=[s4_count, s4_prob], extra=[err_of(s4_count), open_of(s4_count), select_of(s4_count)]),
    5: dict(name="Independent and Dependent Events", std=["7.SP.C.8a", "S-CP.A.2"], fams=[s5_indep, s5_bag, s5_classify], extra=[err_of(s5_bag), open_of(s5_bag)]),
    6: dict(name="Permutations and Combinations", std=["S-CP.B.9", "7.SP.C.8b"], fams=[s6_perm, s6_arrange], extra=[err_of(s6_perm), open_of(s6_perm), select_of(s6_perm)]),
    7: dict(name="Experimental Probability", std=["7.SP.C.6", "7.SP.C.7b"], fams=[s7_exp, s7_compare], extra=[err_of(s7_exp), open_of(s7_exp)]),
    8: dict(name="Random Samples and Surveys", std=["7.SP.A.1", "7.SP.A.2"], fams=[s8_bias, s8_predict], extra=[err_of(s8_predict), open_of(s8_predict)]),
}
