"""Grade 6 Unit 7 — Data Displays (data-displays)."""
from glib import *
from collections import Counter
import g7_u12 as S7, g7_u03 as D7

UNIT_ID = "data-displays"
ABBR = "dd"


# ============================================================== S1 Statistical Questions
STAT = ["How many hours do students in my class sleep on school nights?", "How tall are the players on the basketball team?", "How many pets do families on my street have?",
        "What are the daily high temperatures in our town this month?", "How long does it take students in our school to get to school?", "How many books did each sixth grader read this summer?"]
NONSTAT = ["How tall is the school flagpole?", "How many students are in Room 12 right now?", "What is the capital of France?", "How many days are in March?",
           "How old is my teacher?", "What time does school start today?"]


@fam("012", mode="mc")
def s1_which(r, L):
    ask = pick(r, ["is", "is not"])
    good = pick(r, STAT if ask == "is" else NONSTAT)
    bad = pick(r, NONSTAT if ask == "is" else STAT, 3)
    opts = [(good, True)] + [(b, False) for b in bad]
    r.shuffle(opts)
    return Q(f"Which question {ask} a statistical question?", good, ["A statistical question expects variability in the answers.", f"“{good}” {'has' if ask == 'is' else 'does not have'} variability in its answers."],
             options=opts, chk=PY("stat_q", want=ask), mode="mc", tags=["reasoning"])


@fam("012", mode="mc")
def s1_classify(r, L):
    q = pick(r, STAT + NONSTAT)
    ok = q in STAT
    ans = "statistical" if ok else "not statistical"
    opts = [("statistical", ok), ("not statistical", not ok)]
    return Q(f"Is this a statistical question? “{q}”", ans, ["Ask whether the answers will vary.", f"The answers {'vary' if ok else 'do not vary'}, so it is {ans}."], options=opts + [("cannot be decided", False)],
             chk=PY("stat_q1", q=q), mode="mc", tags=["reasoning"])


@fam("012")
def s1_answer(r, L):
    q = pick(r, STAT)
    n = pick(r, [5, 7, 9]) if L < 2 else pick(r, [6, 8, 10])
    xs = [r.randint(0, 12) for _ in range(n)]
    srt = sorted(xs)
    med = F(srt[n // 2]) if n % 2 else F(srt[n // 2 - 1] + srt[n // 2], 2)
    return Q(f"To answer the statistical question “{q}”, a student collected these data: {', '.join(map(str, xs))}. What is the median, a typical value?", D(med),
             ["A statistical question is answered with data that vary; a typical value summarizes them.", f"Order the data: {', '.join(map(str, srt))}.", f"Median = {D(med)}."],
             [D(F(xs[n // 2])) if F(xs[n // 2]) != med else D(med + 1), D(F(sum(xs), n)) if is_term(F(sum(xs), n)) and F(sum(xs), n) != med else D(med + F(1, 2)), str(max(xs) - min(xs))],
             PY("stat", data=[str(x) for x in xs], stat="median"), why=["Did not order the data first", "Gave the mean", "Gave the range"])


# ============================================================== S5 Mean Absolute Deviation
@fam("012")
def s5_mad(r, L):
    n = pick(r, [4, 5, 6, 8]) if L < 2 else pick(r, [5, 6, 8, 10])
    for _ in range(60):
        xs = [r.randint(1, 20) for _ in range(n)]
        m = F(sum(xs), n)
        if m.denominator == 1:
            break
    else:
        raise Reject()
    mad = sum(abs(x - m) for x in xs) / n
    need(is_term(mad) and mad.denominator <= 10)
    devs = [abs(x - m) for x in xs]
    return Q(f"Find the mean absolute deviation (MAD) of the data: {', '.join(map(str, xs))}", D(mad), [f"Mean = {sum(xs)} ÷ {n} = {N(m)}.", f"Distances from the mean: {', '.join(N(d) for d in devs)}.",
                                                                                                      f"Sum of distances = {N(sum(devs))}.", f"MAD = {N(sum(devs))} ÷ {n} = {D(mad)}."],
             [D(sum(devs)), N(m), D(F(max(xs) - min(xs)))], PY("stat", data=[str(x) for x in xs], stat="mad"), why=["Forgot to divide by the number of values", "Gave the mean", "Gave the range"], tags=["multistep"])


@fam("12", mode="mc")
def s5_compare(r, L):
    m = r.randint(10, 30)
    a = [m - 1, m, m, m + 1]
    b = [m - 6, m - 2, m + 2, m + 6]
    good = "Class B's scores are more spread out."
    opts = [(good, True), ("Class A's scores are more spread out.", False), ("Both classes have the same spread.", False), ("Class B has a greater mean.", False)]
    r.shuffle(opts)
    return Q(f"Class A's scores: {', '.join(map(str, a))}. Class B's scores: {', '.join(map(str, b))}. Both have mean {m}. Which statement is true?", good,
             [f"MAD of A = {D(F(2, 4))}; MAD of B = {D(F(16, 4))}.", "A greater MAD means the data are more spread out."], options=opts, chk=PY("mad_compare", a=a, b=b), mode="mc", tags=["reasoning"])


# ============================================================== S6 Comparing data displays
@fam("012", mode="mc")
def s6_center(r, L):
    a = sorted(r.randint(5, 30) for _ in range(7))
    b = sorted(r.randint(5, 30) for _ in range(7))
    st = pick(r, ["median", "range"])
    def med(x): return x[3]
    va, vb = (med(a), med(b)) if st == "median" else (a[-1] - a[0], b[-1] - b[0])
    need(va != vb)
    good = f"Team {'A' if va > vb else 'B'} has the greater {st}."
    opts = [(good, True), (f"Team {'B' if va > vb else 'A'} has the greater {st}.", False), (f"The teams have the same {st}.", False), ("The data cannot be compared.", False)]
    r.shuffle(opts)
    return Q(f"Points scored — Team A: {', '.join(map(str, a))}; Team B: {', '.join(map(str, b))}. Which statement is true?", good,
             [f"Team A {st}: {va}.", f"Team B {st}: {vb}.", good], options=opts, chk=PY("team_compare", a=a, b=b, st=st), mode="mc", tags=["reasoning"])


@fam("012")
def s6_diff(r, L):
    n = 5
    for _ in range(80):
        a = [r.randint(5, 30) for _ in range(n)]
        b = [r.randint(5, 30) for _ in range(n)]
        if sum(a) % n == 0 and sum(b) % n == 0 and sum(a) != sum(b):
            break
    else:
        raise Reject()
    ma, mb = sum(a) // n, sum(b) // n
    hi, lo = ("A", "B") if ma > mb else ("B", "A")
    return Q(f"Plant heights (cm) — Group A: {', '.join(map(str, a))}; Group B: {', '.join(map(str, b))}. How much greater is the mean height of Group {hi} than Group {lo}?", f"{abs(ma - mb)} cm",
             [f"Mean A = {sum(a)} ÷ {n} = {ma}.", f"Mean B = {sum(b)} ÷ {n} = {mb}.", f"Difference = {abs(ma - mb)} cm."],
             [f"{abs(sum(a) - sum(b))} cm", f"{abs(sorted(a)[2] - sorted(b)[2]) if sorted(a)[2] != sorted(b)[2] and abs(sorted(a)[2] - sorted(b)[2]) != abs(ma - mb) else abs(ma - mb) + 1} cm", f"{ma + mb} cm"],
             PY("mean_diff", a=a, b=b), why=["Compared the totals instead of the means", "Compared the medians", "Added the means"], tags=["multistep"])


# ============================================================== S7 Shape of distributions
def shaped(r, kind, lo=1, hi=20):
    """Dot-plot data with a clear shape (random counts that keep the shape)."""
    if kind == "symmetric":
        a, b, c = r.randint(0, 1), r.randint(1, 3), r.randint(3, 5)
        w = [a, b, c, c + r.randint(1, 3), c, b, a]
    else:
        w = sorted([r.randint(5, 8), r.randint(4, 6), r.randint(2, 4), r.randint(1, 3), r.randint(0, 2), r.randint(0, 1), 0], reverse=True)
        need(w[0] > w[1] > w[2] >= w[3])
        if kind == "skewed left":
            w = w[::-1]
    start = r.randint(lo, hi - 7 + 1)
    vals = [i for i, k in enumerate(w) for _ in range(k)]
    n = len(vals)
    med = F(vals[n // 2]) if n % 2 else F(vals[n // 2 - 1] + vals[n // 2], 2)
    gap = F(sum(vals), n) - med
    need(kind == "symmetric" or (gap >= F(1, 2) if kind == "skewed right" else gap <= -F(1, 2)))
    xs = []
    for i, k in enumerate(w):
        xs += [start + i] * k
    return xs, start


@fam("012", mode="mc")
def s7_shape(r, L):
    kind = pick(r, ["symmetric", "skewed right", "skewed left"])
    xs, start = shaped(r, kind)
    opts = [(k, k == kind) for k in ["symmetric", "skewed right", "skewed left"]] + [("no shape can be described", False)]
    alt = "Dot plot. " + ", ".join(f"{v}: {c}" for v, c in sorted(Counter(xs).items())) + "."
    return Q("Describe the shape of the data in the dot plot.", kind, ["Symmetric: the left and right halves are mirror images.", "Skewed right: a tail stretches to the right; skewed left: a tail stretches to the left.", f"This plot is {kind}."],
             options=opts, chk=PY("shape", data=xs), mode="mc", tags=["graph"], diagram={"alt": alt, "draw": dot_draw(xs, start - 1, start + 7)})


@fam("012")
def s7_peak(r, L):
    kind = pick(r, ["symmetric", "skewed right", "skewed left"])
    xs, start = shaped(r, kind)
    c = Counter(xs)
    pk = max(c, key=c.get)
    alt = "Dot plot. " + ", ".join(f"{v}: {n}" for v, n in sorted(c.items())) + "."
    return Q("At what value does the dot plot have its peak (the most dots)?", str(pk), ["The peak is the tallest column of dots.", f"The tallest column is at {pk}."],
             [str(c[pk]), str(max(xs)), str(sorted(xs)[len(xs) // 2]) if sorted(xs)[len(xs) // 2] != pk else str(pk + 1)], PY("stat", data=[str(x) for x in xs], stat="mode"),
             why=["Gave the number of dots instead of the value", "Gave the greatest value", "Gave the median"], tags=["graph"], diagram={"alt": alt, "draw": dot_draw(xs, start - 1, start + 7)})


# ============================================================== S8 Describing distributions
@fam("012", mode="mc")
def s8_best_center(r, L):
    base = [r.randint(20, 30) for _ in range(7)]
    out = r.randint(80, 150)
    xs = base + [out]
    good = "median, because the outlier pulls the mean"
    opts = [(good, True), ("mean, because it uses every value", False), ("range, because it shows the spread", False), ("mode, because it is always in the middle", False)]
    r.shuffle(opts)
    return Q(f"Data: {', '.join(map(str, xs))}. Which measure best describes the center?", good, [f"{out} is an outlier.", f"Mean ≈ {Rd(F(sum(xs), len(xs)), 1)}; median = {D((sorted(xs)[3] + sorted(xs)[4]) / F(2))}.",
                                                                                                 "The median is not affected much by the outlier."], options=opts, chk=PY("best_center", data=xs), mode="mc", tags=["reasoning"])


@fam("012")
def s8_outlier(r, L):
    base = sorted(r.randint(30, 60) for _ in range(9))
    out = pick(r, [r.randint(base[-1] + 40, base[-1] + 80), r.randint(1, max(2, base[0] - 25))])
    xs = sorted(base + [out])
    srt = xs
    q1, q3 = (srt[2] + 0), srt[7]
    def md(a):
        k = len(a)
        return F(a[k // 2]) if k % 2 else F(a[k // 2 - 1] + a[k // 2], 2)
    Q1, Q3 = md(srt[:5]), md(srt[5:])
    fence = [x for x in srt if x < Q1 - F(3, 2) * (Q3 - Q1) or x > Q3 + F(3, 2) * (Q3 - Q1)]
    need(fence == [out])
    return Q(f"Which value in the data set is an outlier? {', '.join(map(str, xs))}", str(out), ["An outlier is far from the rest of the data.", f"{out} is much {'greater' if out > base[-1] else 'less'} than the other values."],
             [str(base[0] if out > base[-1] else base[-1]), str(xs[len(xs) // 2]), str(base[-1] if out > base[-1] else base[0])], PY("outlier_iqr", data=xs),
             why=["Chose the value at the other end", "Chose the middle value", "Chose the nearest end of the main cluster"])


@fam("12")
def s8_describe(r, L):
    xs = sorted(r.randint(10, 40) for _ in range(9))
    f5 = [xs[0], (xs[1] + xs[2]) / F(2), xs[4], (xs[6] + xs[7]) / F(2), xs[-1]]
    return Q(f"Data: {', '.join(map(str, xs))}. Give the median and the interquartile range, separated by a comma.", f"{D(F(xs[4]))}, {D(f5[3] - f5[1])}",
             [f"Median: {xs[4]}.", f"Q1 = {D(f5[1])}, Q3 = {D(f5[3])}.", f"IQR = {D(f5[3] - f5[1])}."], [f"{D(F(xs[4]))}, {xs[-1] - xs[0]}", f"{D(F(sum(xs), 9)) if is_term(F(sum(xs), 9)) else xs[4] + 1}, {D(f5[3] - f5[1])}", f"{D(f5[1])}, {D(f5[3])}"],
             PY("med_iqr", data=xs), why=["Gave the range instead of the IQR", "Gave the mean instead of the median", "Gave the quartiles"], tags=["multistep"])


SKILLS = {
    1: dict(name="Statistical Questions", std=["6.SP.A.1"], fams=[s1_which, s1_classify, s1_answer], extra=[open_of(reuse(D7.s3_stat, (0, 0, 1), "o")), err_of(reuse(D7.s3_stat, (0, 0, 1), "e")), err_of(reuse(S7.s1_freq_text, (0, 0, 1), "e"))]),
    2: dict(name="Displaying Data on Dot Plots, Histograms, and Box Plots", std=["6.SP.B.4"], fams=[reuse(S7.s1_lineplot, (0, 0, 2)), reuse(S7.s1_table), reuse(S7.s2_read), reuse(S7.s1_freq_text)],
            extra=[err_of(reuse(S7.s1_table, (0, 1, 2), "e")), err_of(reuse(S7.s2_read, (0, 1, 2), "e"))]),
    3: dict(name="Mean and Median", std=["6.SP.B.5c"], fams=[reuse(D7.s3_stat, (0, 1, 1)), reuse(D7.s3_missing, (1, 1, 2))], extra=[err_of(reuse(D7.s3_stat, (0, 1, 1), "e")), open_of(reuse(D7.s3_stat, (0, 1, 1), "o"))]),
    4: dict(name="Range and Interquartile Range", std=["6.SP.B.5c"], fams=[reuse(S7.s2_summary, (1, 1, 1)), reuse(S7.s2_read, (0, 1, 2), "r"), s8_describe], extra=[err_of(reuse(S7.s2_summary, (1, 1, 1), "e")), open_of(reuse(S7.s2_summary, (1, 1, 1), "o"))]),
    5: dict(name="Mean Absolute Deviation", std=["6.SP.B.5c"], fams=[s5_mad, s5_compare], extra=[err_of(s5_mad), open_of(s5_mad)]),
    6: dict(name="Comparing Data Displays", std=["6.SP.B.4", "7.SP.B.3"], fams=[s6_center, reuse(S7.s2_compare, (2, 2, 2)), s6_diff], extra=[err_of(reuse(D7.s3_stat, (1, 1, 2), "c")), err_of(reuse(S7.s2_summary, (1, 1, 1), "c"))]),
    7: dict(name="Shape of Data Distributions", std=["6.SP.A.2", "6.SP.B.5d"], fams=[s7_shape, s7_peak], extra=[err_of(s7_peak), err_of(reuse(S7.s1_lineplot, (0, 0, 2), "e"))]),
    8: dict(name="Describing Distributions", std=["6.SP.B.5", "6.SP.A.2"], fams=[s8_best_center, s8_outlier, s8_describe], extra=[err_of(s8_outlier), open_of(s8_outlier)]),
}
