"""Precalculus Unit 8 — Probability and statistics (probability)."""
from hslib import *

UNIT_ID = "probability"
ABBR = "prb"
COLORS = ["red", "blue", "green", "yellow", "white", "black"]


def fr(v):
    return T(sp.nsimplify(v))


def bag(r, k=3):
    cs = r.sample(COLORS, k)
    ns_ = [rint(r, 2, 9) for _ in cs]
    return cs, ns_


def bagtxt(cs, ns_):
    return ", ".join(f"{n} {c}" for c, n in zip(cs, ns_))


# ============================================================== S1 Probability, odds, distributions
@fam("012")
def s1_basic(r, L):
    cs, ns_ = bag(r)
    tot = sum(ns_)
    i = r.randrange(3)
    kind = pick(r, ["prob", "odds", "comp"]) if L else pick(r, ["prob", "comp"])
    if kind == "prob":
        v = sp.Rational(ns_[i], tot)
        return Q(f"A bag holds {bagtxt(cs, ns_)} marbles. One is drawn at random. Find P({cs[i]}).", fr(v), [f"Total = {tot}.", f"P({cs[i]}) = {ns_[i]}/{tot} = {fr(v)}." if False else f"P = {ns_[i]} ÷ {tot} = {fr(v)}."],
                 [fr(sp.Rational(ns_[i], tot - ns_[i])), fr(sp.Rational(tot - ns_[i], tot)), fr(sp.Rational(1, 3))], H(f"Rational({ns_[i]}, {tot})"), why=["Gave the odds instead of the probability", "Found the complement", "Assumed the colors are equally likely"])
    if kind == "comp":
        v = sp.Rational(tot - ns_[i], tot)
        return Q(f"A bag holds {bagtxt(cs, ns_)} marbles. One is drawn at random. Find P(not {cs[i]}).", fr(v), [f"P({cs[i]}) = {fr(sp.Rational(ns_[i], tot))}.", f"P(not {cs[i]}) = 1 - {fr(sp.Rational(ns_[i], tot))} = {fr(v)}."],
                 [fr(sp.Rational(ns_[i], tot)), fr(sp.Rational(tot - ns_[i], ns_[i])), fr(sp.Rational(2, 3))], H(f"1 - Rational({ns_[i]}, {tot})"), why=["Found P(event) instead", "Gave odds", "Assumed equally likely colors"])
    g = math.gcd(ns_[i], tot - ns_[i])
    ans = f"{ns_[i] // g} : {(tot - ns_[i]) // g}"
    return Q(f"A bag holds {bagtxt(cs, ns_)} marbles. One is drawn at random. What are the odds in favor of drawing {cs[i]}?", ans, ["Odds in favor = favorable : unfavorable.", f"{ns_[i]} : {tot - ns_[i]}.", f"Simplified: {ans}."],
             [f"{ns_[i] // math.gcd(ns_[i], tot)} : {tot // math.gcd(ns_[i], tot)}", f"{(tot - ns_[i]) // g} : {ns_[i] // g}", f"{ns_[i]} : {tot}" if math.gcd(ns_[i], tot) != 1 else f"{ns_[i] + 1} : {tot - ns_[i]}"],
             PY("odds", f=ns_[i], u=tot - ns_[i]), why=["Used favorable : total", "Gave the odds against", "Used favorable : total"])


@fam("012")
def s1_ev(r, L):
    k_ = 3 if L == 0 else 4
    xs = sorted(r.sample(range(0, 10), k_))
    ps = [rint(r, 1, 6) for _ in xs]
    tot = sum(ps)
    pr = [sp.Rational(p_, tot) for p_ in ps]
    need(tot in (10, 20, 5, 4, 8, 16, 25) or L)
    E = sum(a * b for a, b in zip(xs, pr))
    tbl = "; ".join(f"P(X = {a}) = {fr(b)}" for a, b in zip(xs, pr))
    if L == 2 and r.random() < 0.5:
        miss = r.randrange(k_)
        tbl = "; ".join(f"P(X = {a}) = {fr(b) if j != miss else 'p'}" for j, (a, b) in enumerate(zip(xs, pr)))
        return Q(f"A probability distribution has {tbl}. Find p.", fr(pr[miss]), ["The probabilities must sum to 1.", f"p = 1 - (sum of the others) = {fr(pr[miss])}."], [fr(1 - pr[miss] * 2) if 1 - 2 * pr[miss] > 0 else fr(pr[miss] / 2), fr(sum(pr) - pr[miss]), fr(sp.Rational(1, k_))],
                 H(f"1 - ({' + '.join(f'Rational({p_.p}, {p_.q})' for j, p_ in enumerate(pr) if j != miss)})"), why=["Made an arithmetic error", "Gave the sum of the others", "Assumed equal probabilities"])
    return Q(f"A random variable X has {tbl}. Find the expected value E(X).", fr(E), ["E(X) = Σ x·P(x).", " + ".join(f"{a}({fr(b)})" for a, b in zip(xs, pr)) + ".", f"E(X) = {fr(E)}."],
             [fr(sp.Rational(sum(xs), k_)), fr(sum(pr) * max(xs)), fr(sum(xs[j] * pr[(j + 1) % k_] for j in range(k_)))], H(" + ".join(f"{a}*Rational({b.p}, {b.q})" for a, b in zip(xs, pr))),
             why=["Averaged the values without weights", "Used only the largest value", "Paired values with the wrong probabilities"])


# ============================================================== S2 Independent / dependent
@fam("012")
def s2_draw(r, L):
    cs, ns_ = bag(r)
    tot = sum(ns_)
    i, j = r.randrange(3), r.randrange(3)
    repl = r.random() < 0.5 if L else True
    if repl:
        v = sp.Rational(ns_[i], tot) * sp.Rational(ns_[j], tot)
    else:
        v = sp.Rational(ns_[i], tot) * sp.Rational(ns_[j] - (1 if i == j else 0), tot - 1)
    alt = sp.Rational(ns_[i], tot) * sp.Rational(ns_[j] - (1 if i == j else 0), tot - 1) if repl else sp.Rational(ns_[i], tot) * sp.Rational(ns_[j], tot)
    need(v != alt or L == 0)
    return Q(f"A bag holds {bagtxt(cs, ns_)} marbles. Two are drawn {'with' if repl else 'without'} replacement. Find P(first {cs[i]}, then {cs[j]}).", fr(v),
             [f"P(first {cs[i]}) = {ns_[i]}/{tot}." if False else f"P(first {cs[i]}) = {fr(sp.Rational(ns_[i], tot))}.", f"P(second {cs[j]} | first {cs[i]}) = {fr(v / sp.Rational(ns_[i], tot))}" + (" (the first marble is returned)." if repl else " (one fewer marble)."), f"Multiply: {fr(v)}."],
             [fr(alt) if alt != v else fr(v * 2), fr(sp.Rational(ns_[i], tot) + sp.Rational(ns_[j], tot)), fr(sp.Rational(ns_[i], tot))], PY("draw2", ns=ns_, i=i, j=j, repl=repl),
             why=["Treated the draws as " + ("dependent" if repl else "independent"), "Added the probabilities", "Found only the first draw"])


@fam("012", mode="mc")
def s2_classify(r, L):
    items = [("rolling a 6 on a die, then flipping heads on a coin", "independent"), ("drawing two cards from a deck without replacement", "dependent"), ("drawing a card, replacing it, then drawing again", "independent"),
             ("choosing two students for different jobs from the same class", "dependent"), ("flipping a coin twice", "independent"), ("picking two pieces of fruit from a bowl and eating the first", "dependent"),
             ("spinning a spinner and then rolling a die", "independent"), ("selecting a president and then a vice president from a club", "dependent")]
    t, a = pick(r, items)
    opts = [("independent", a == "independent"), ("dependent", a == "dependent"), ("mutually exclusive", False), ("complementary", False)]
    return Q(f"Classify the events: {t}.", a, ["Events are independent if the first outcome does not change the probability of the second.", f"These events are {a}."], options=opts, chk=TXT(a), mode="mc")


# ============================================================== S3 Permutations and combinations
@fam("012")
def s3_count(r, L):
    n_ = rint(r, 5, 15)
    k_ = rint(r, 2, min(5, n_ - 1))
    kind = pick(r, ["perm", "comb"])
    ctx = {"perm": [f"In how many ways can {k_} runners finish first through {['', '', 'second', 'third', 'fourth', 'fifth'][k_]} in a race with {n_} runners?",
                    f"How many ways can a club of {n_} members choose " + {2: "a president and a vice president", 3: "a president, a vice president, and a secretary", 4: "a president, a vice president, a secretary, and a treasurer"}[k_] + "?" if k_ <= 4 else f"How many {k_}-letter arrangements can be made from {n_} different letters with no repeats?"],
           "comb": [f"How many ways can a committee of {k_} be chosen from {n_} people?", f"How many different {k_}-topping pizzas can be made from {n_} toppings?"]}[kind]
    q = pick(r, ctx)
    v = sp.ff(n_, k_) if kind == "perm" else sp.binomial(n_, k_)
    w = sp.binomial(n_, k_) if kind == "perm" else sp.ff(n_, k_)
    return Q(q, str(v), [f"Order {'matters' if kind == 'perm' else 'does not matter'}: use {'P' if kind == 'perm' else 'C'}({n_}, {k_}).", f"{'n!/(n - k)!' if False else ('n! ÷ (n - k)!' if kind == 'perm' else 'n! ÷ (k!(n - k)!)')}.", f"= {v}."],
             [str(w), str(n_ ** k_), str(n_ * k_)], H(f"{'ff' if False else ''}factorial({n_})/factorial({n_ - k_})" + ("" if kind == "perm" else f"/factorial({k_})")),
             why=["Used " + ("combinations" if kind == "perm" else "permutations"), "Allowed repetition", "Multiplied n by k"])


@fam("12")
def s3_prob(r, L):
    g, b = rint(r, 3, 9), rint(r, 3, 9)
    k_ = rint(r, 2, 4)
    j = rint(r, 0, k_)
    need(j <= g and k_ - j <= b)
    v = sp.binomial(g, j) * sp.binomial(b, k_ - j) / sp.binomial(g + b, k_)
    return Q(f"A group has {g} girls and {b} boys. A committee of {k_} is chosen at random. Find the probability that exactly {j} are girls. Give an exact fraction.", fr(v),
             [f"Favorable: C({g}, {j})·C({b}, {k_ - j}) = {sp.binomial(g, j) * sp.binomial(b, k_ - j)}.", f"Total: C({g + b}, {k_}) = {sp.binomial(g + b, k_)}.", f"P = {fr(v)}."],
             [fr(sp.Rational(g, g + b) ** j * sp.Rational(b, g + b) ** (k_ - j)), fr(sp.binomial(g, j) / sp.binomial(g + b, k_)), fr(sp.Rational(j, k_))],
             H(f"binomial({g}, {j})*binomial({b}, {k_ - j})/binomial({g + b}, {k_})"), why=["Treated the choices as independent with replacement", "Forgot to choose the boys", "Used j/k"])


# ============================================================== S4 Compound events
@fam("012")
def s4_or(r, L):
    tot = 100
    a, b = rint(r, 20, 60), rint(r, 20, 60)
    both = rint(r, max(0, a + b - tot) + 1, min(a, b) - 1)
    pa, pb, pab = sp.Rational(a, tot), sp.Rational(b, tot), sp.Rational(both, tot)
    v = pa + pb - pab
    return Q(f"In a survey of {tot} students, {a} play a sport, {b} play an instrument, and {both} do both. A student is chosen at random. Find P(sport or instrument).", fr(v),
             ["P(A or B) = P(A) + P(B) - P(A and B).", f"{fr(pa)} + {fr(pb)} - {fr(pab)}.", f"= {fr(v)}."], [fr(pa + pb), fr(pa * pb), fr(pa + pb - 2 * pab)],
             H(f"Rational({a}, {tot}) + Rational({b}, {tot}) - Rational({both}, {tot})"), why=["Forgot to subtract the overlap", "Multiplied the probabilities", "Subtracted the overlap twice"])


@fam("012")
def s4_table(r, L):
    rows, cols = ["9th", "10th"], ["cats", "dogs"]
    t = [[rint(r, 5, 40) for _ in range(2)] for _ in range(2)]
    i, j = rint(r, 0, 1), rint(r, 0, 1)
    tot = sum(map(sum, t))
    desc = f"9th graders: {t[0][0]} prefer cats, {t[0][1]} prefer dogs; 10th graders: {t[1][0]} prefer cats, {t[1][1]} prefer dogs."
    if L == 0:
        v = sp.Rational(t[i][j], tot)
        return Q(f"Survey results — {desc} One student is chosen at random. Find P({rows[i]} grader and prefers {cols[j]}).", fr(v), [f"Total = {tot}.", f"P = {t[i][j]} ÷ {tot} = {fr(v)}."],
                 [fr(sp.Rational(t[i][j], sum(t[i]))), fr(sp.Rational(t[i][j], t[0][j] + t[1][j])), fr(sp.Rational(sum(t[i]), tot) * sp.Rational(t[0][j] + t[1][j], tot)) if sp.Rational(sum(t[i]), tot) * sp.Rational(t[0][j] + t[1][j], tot) != v else fr(v + sp.Rational(1, tot))],
                 H(f"Rational({t[i][j]}, {tot})"), why=["Divided by the row total", "Divided by the column total", "Multiplied the marginal probabilities"])
    v = sp.Rational(t[i][j], t[0][j] + t[1][j]) if L == 2 else sp.Rational(t[i][j], sum(t[i]))
    q = f"P({rows[i]} grader | prefers {cols[j]})" if L == 2 else f"P(prefers {cols[j]} | {rows[i]} grader)"
    other = sp.Rational(t[i][j], sum(t[i])) if L == 2 else sp.Rational(t[i][j], t[0][j] + t[1][j])
    need(other != v)
    return Q(f"Survey results — {desc} Find {q}.", fr(v), ["Conditional probability: restrict to the given group.", f"P = {t[i][j]} ÷ {t[0][j] + t[1][j] if L == 2 else sum(t[i])} = {fr(v)}."],
             [fr(other), fr(sp.Rational(t[i][j], tot)), fr(sp.Rational(t[0][j] + t[1][j] if L < 2 else sum(t[i]), tot))], H(f"Rational({t[i][j]}, {t[0][j] + t[1][j] if L == 2 else sum(t[i])})"),
             why=["Conditioned on the wrong event", "Used the grand total", "Gave a marginal probability"])


# ============================================================== S5 Decision making
@fam("012")
def s5_game(r, L):
    cost = rint(r, 1, 10)
    prizes = [(rint(r, 5, 60), sp.Rational(1, pick(r, [4, 5, 8, 10, 20])))]
    if L:
        prizes.append((rint(r, 2, 10), sp.Rational(1, pick(r, [2, 4, 5]))))
    need(sum(p_ for _, p_ in prizes) < 1)
    E = sum(a * p_ for a, p_ in prizes) - cost
    desc = " and ".join(f"wins ${a} with probability {fr(p_)}" for a, p_ in prizes)
    if L == 2 and r.random() < 0.5:
        ans = "No, the expected value is negative" if E < 0 else "Yes, the expected value is nonnegative" if E > 0 else "It is a fair game"
        opts = [("No, the expected value is negative", E < 0), ("Yes, the expected value is nonnegative", E > 0), ("It is a fair game", E == 0), ("Yes, because a large prize is possible", False)]
        return Q(f"A game costs ${cost} to play. A player {desc}. Is it worth playing in the long run?", ans, [f"E = {' + '.join(f'{a}({fr(p_)})' for a, p_ in prizes)} - {cost} = {fr(E)}.", "Compare E with 0."],
                 options=opts, chk=PY("game", cost=cost, prizes=[[a, str(p_)] for a, p_ in prizes], ask="decide"), mode="mc", tags=["reasoning"])
    need((E * 100).q == 1 and ((E - cost) * 100).q == 1)
    mo = lambda v: ("-$" if v < 0 else "$") + Rd(float(abs(v)), 2)
    return Q(f"A game costs ${cost} to play. A player {desc} (prizes do not include the cost). Find the expected net gain per game, in dollars.", mo(E),
             [f"Expected winnings = {' + '.join(f'{a}({fr(p_)})' for a, p_ in prizes)} = {mo(E + cost)}.", f"Subtract the cost: {mo(E)}."],
             [mo(E - cost), mo(E + cost), mo(sp.Integer(sum(a for a, _ in prizes) - cost))],
             PY("game", cost=cost, prizes=[[a, str(p_)] for a, p_ in prizes], ask="ev"), why=["Subtracted the cost twice", "Forgot to subtract the cost", "Ignored the probabilities"], tags=["modeling"])


# ============================================================== S6 Data types and displays
@fam("012", mode="mc")
def s6_types(r, L):
    items = [("number of siblings", "quantitative, discrete"), ("height in centimeters", "quantitative, continuous"), ("favorite color", "categorical"), ("time to finish a race", "quantitative, continuous"),
             ("number of goals scored", "quantitative, discrete"), ("type of pet", "categorical"), ("zip code", "categorical"), ("temperature at noon", "quantitative, continuous"),
             ("number of texts sent in a day", "quantitative, discrete"), ("eye color", "categorical"), ("weight of a backpack", "quantitative, continuous"), ("jersey number", "categorical")]
    t, a = pick(r, items)
    opts = [(o, o == a) for o in ["categorical", "quantitative, discrete", "quantitative, continuous", "ordinal ranking only"]]
    return Q(f"Classify the variable: {t}.", a, ["Categorical data name groups; quantitative data are measured or counted numbers.", "Discrete data are counts; continuous data are measurements.", f"{t}: {a}."], options=opts, chk=TXT(a), mode="mc")


@fam("012", mode="mc")
def s6_display(r, L):
    items = [("compare the distribution of test scores for two classes, showing medians and quartiles", "side-by-side box plots"), ("show the relationship between hours studied and test score", "scatterplot"),
             ("show how a city's population changed each year", "line graph"), ("show the share of students choosing each lunch option", "bar graph"),
             ("show the shape of the distribution of 200 heights", "histogram"), ("show the five-number summary of a data set", "box plot")]
    t, a = pick(r, items)
    pool = ["side-by-side box plots", "scatterplot", "line graph", "bar graph", "histogram", "box plot"]
    others = [p_ for p_ in pool if p_ != a and not (a == "box plot" and p_ == "side-by-side box plots") and not (a == "side-by-side box plots" and p_ == "box plot")]
    r.shuffle(others)
    opts = [(a, True)] + [(o, False) for o in others[:3]]
    r.shuffle(opts)
    return Q(f"Which display is the best choice to {t}?", a, [f"A {a} fits this purpose best."], options=opts, chk=TXT(a), mode="mc")


@fam("012")
def s6_stats(r, L):
    n_ = pick(r, [5, 6, 7, 8])
    d = sorted(rint(r, 1, 40) for _ in range(n_))
    kind = pick(r, ["mean", "median", "range", "iqr"] if L else ["mean", "median", "range"])
    if kind == "mean":
        v = sp.Rational(sum(d), n_)
        need(v.q in (1, 2, 4, 5))
        return Q(f"Find the mean of {', '.join(map(str, r.sample(d, n_)))}.", D(F(v.p, v.q)), [f"Sum = {sum(d)}.", f"Mean = {sum(d)} ÷ {n_} = {D(F(v.p, v.q))}."],
                 [D(F(sp.Rational(d[(n_ - 1) // 2] + d[n_ // 2], 2).p, sp.Rational(d[(n_ - 1) // 2] + d[n_ // 2], 2).q)), D(F(sum(d), n_ - 1)) if F(sum(d), n_ - 1).denominator in (1, 2, 4, 5, 8) else str(sum(d)), str(sum(d))],
                 H(f"Rational({sum(d)}, {n_})"), why=["Gave the median", "Divided by n - 1" if F(sum(d), n_ - 1).denominator in (1, 2, 4, 5, 8) else "Gave the sum", "Gave the sum"])
    if kind == "median":
        m = sp.Rational(d[(n_ - 1) // 2] + d[n_ // 2], 2)
        shuffled = r.sample(d, n_)
        need(shuffled != d)
        mid_unsorted = sp.Rational(shuffled[(n_ - 1) // 2] + shuffled[n_ // 2], 2)
        return Q(f"Find the median of {', '.join(map(str, shuffled))}.", D(F(m.p, m.q)), ["Order the data.", f"{', '.join(map(str, d))}.", f"Median = {D(F(m.p, m.q))}."],
                 [D(F(mid_unsorted.p, mid_unsorted.q)) if mid_unsorted != m else D(F(m.p, m.q) + 1), D(F(sum(d), n_)) if F(sum(d), n_).denominator in (1, 2, 4, 5) else str(d[0]), str(d[n_ // 2]) if n_ % 2 == 0 and d[n_ // 2] != m else str(d[-1])],
                 PY("median", data=shuffled), why=["Did not order the data first", "Gave the mean", "Picked one middle value instead of averaging" if n_ % 2 == 0 else "Gave the maximum"])
    if kind == "range":
        return Q(f"Find the range of {', '.join(map(str, r.sample(d, n_)))}.", str(d[-1] - d[0]), ["Range = max - min.", f"{d[-1]} - {d[0]} = {d[-1] - d[0]}."], [str(d[-1]), f"{d[0]} to {d[-1]}" if False else str(d[-1] + d[0]), str(d[-2] - d[1])],
                 H(f"{max(d)} - {min(d)}"), why=["Gave the maximum", "Added the extremes", "Used the wrong values"])
    need(n_ % 2 == 0)
    lo, hi = d[: n_ // 2], d[n_ // 2:]
    q1 = sp.Rational(lo[(len(lo) - 1) // 2] + lo[len(lo) // 2], 2)
    q3 = sp.Rational(hi[(len(hi) - 1) // 2] + hi[len(hi) // 2], 2)
    v = q3 - q1
    return Q(f"Find the interquartile range of {', '.join(map(str, d))}.", D(F(v.p, v.q)), [f"Lower half {', '.join(map(str, lo))}: Q1 = {D(F(q1.p, q1.q))}.", f"Upper half {', '.join(map(str, hi))}: Q3 = {D(F(q3.p, q3.q))}.", f"IQR = {D(F(v.p, v.q))}."],
             [str(d[-1] - d[0]), D(F((q3 + q1).p, (q3 + q1).q)), D(F(q3.p, q3.q))], PY("iqr", data=d), why=["Gave the range", "Added the quartiles", "Gave Q3"])


# ============================================================== S7 Shapes of distributions
@fam("012", mode="mc")
def s7_shape(r, L):
    items = [("The mean is much greater than the median.", "skewed right"), ("The mean is much less than the median.", "skewed left"), ("The mean and median are about equal and the histogram is mound-shaped.", "symmetric"),
             ("Most data are at low values with a long tail toward high values (like household incomes).", "skewed right"), ("Most scores are high with a few very low scores (like an easy test).", "skewed left"),
             ("The histogram has two distinct peaks.", "bimodal")]
    t, a = pick(r, items)
    opts = [(o, o == a) for o in ["skewed right", "skewed left", "symmetric", "bimodal"]]
    return Q(f"Describe the shape of the distribution: {t}", a, ["The mean is pulled toward the tail.", f"Shape: {a}."], options=opts, chk=TXT(a), mode="mc")


@fam("012", mode="mc")
def s7_center(r, L):
    shape = pick(r, ["skewed right", "skewed left", "symmetric"])
    good = {"skewed right": "the median and IQR", "skewed left": "the median and IQR", "symmetric": "the mean and standard deviation"}[shape]
    opts = [(o, o == good) for o in ["the median and IQR", "the mean and standard deviation", "the mode only", "the range only"]]
    return Q(f"A distribution is {shape}. Which measures of center and spread best summarize it?", good, ["Skewed data and outliers pull the mean and standard deviation.", f"For {shape} data use {good}."], options=opts, chk=TXT(good), mode="mc")


@fam("012")
def s7_outlier(r, L):
    d = sorted(rint(r, 20, 40) for _ in range(7))
    lo, hi = d[:3], d[4:]
    q1, q3 = lo[1], hi[1]
    iqr = q3 - q1
    need(iqr > 0)
    big = q3 + int(1.5 * iqr) + rint(r, 2, 15)
    data = d + [big]
    data = sorted(data)
    n_ = len(data)
    L_, U_ = data[: n_ // 2], data[n_ // 2:]
    Q1 = sp.Rational(L_[1] + L_[2], 2)
    Q3 = sp.Rational(U_[1] + U_[2], 2)
    fence = Q3 + sp.Rational(3, 2) * (Q3 - Q1)
    need(big > fence and data[-2] <= fence)
    return Q(f"Data: {', '.join(map(str, data))}. Using the 1.5 × IQR rule, what is the upper fence, and which value is an outlier?", f"fence = {D(F(fence.p, fence.q))}; outlier {big}",
             [f"Q1 = {D(F(Q1.p, Q1.q))}, Q3 = {D(F(Q3.p, Q3.q))}, IQR = {D(F((Q3 - Q1).p, (Q3 - Q1).q))}.", f"Upper fence = Q3 + 1.5·IQR = {D(F(fence.p, fence.q))}.", f"{big} > {D(F(fence.p, fence.q))}, so {big} is an outlier."],
             [f"fence = {D(F((Q3 + Q3 - Q1).p, (Q3 + Q3 - Q1).q))}; outlier {big}", f"fence = {D(F(fence.p, fence.q))}; no outlier", f"fence = {D(F((data[-1] - data[0]) * 3, 2))}; outlier {big}"],
             PY("fence", data=data), why=["Used 1·IQR", "Did not compare the maximum with the fence", "Used the range"])


@fam("012")
def s7_meanmed(r, L):
    n_ = pick(r, [5, 6, 7, 8])
    d = sorted(rint(r, 10, 30) for _ in range(n_ - 1)) + [rint(r, 60, 120) * pick(r, [1, -1]) if L == 2 else rint(r, 60, 120)]
    d = sorted(d)
    mean = sp.Rational(sum(d), n_)
    med = sp.Rational(d[(n_ - 1) // 2] + d[n_ // 2], 2)
    need(mean.q in (1, 2, 4, 5, 8) and med != mean)
    dm = lambda v: D(F(v.p, v.q))
    ans = f"mean = {dm(mean)}; median = {dm(med)}"
    shape = "right" if mean > med else "left"
    return Q(f"Data: {', '.join(map(str, d))}. Find the mean and the median. Which is the better measure of center here?", ans + f"; the median (the data are skewed {shape})",
             [f"Mean = {sum(d)} ÷ {n_} = {dm(mean)}.", f"Median = {dm(med)}.", f"The extreme value pulls the mean, so the median is better."],
             [f"mean = {dm(med)}; median = {dm(mean)}; the mean (the data are symmetric)", ans + "; the mean (the data are skewed " + shape + ")", f"mean = {dm(mean)}; median = {d[n_ // 2]}; the median (the data are skewed {shape})" if d[n_ // 2] != med else f"mean = {dm(mean)}; median = {d[0]}; the median (the data are skewed {shape})"],
             PY("meanmed", data=d), why=["Switched the mean and median", "Chose the mean despite the outlier", "Did not average the two middle values" if n_ % 2 == 0 else "Did not order the data"])


# ============================================================== S8 Normal distributions
@fam("012")
def s8_empirical(r, L):
    mu, sd = rint(r, 40, 120), rint(r, 3, 15)
    k1, k2 = pick(r, [(-1, 1), (-2, 2), (-3, 3), (0, 1), (-1, 0), (0, 2), (-2, 0), (1, 2), (-2, -1), (-2, 1), (-1, 2)] if L else [(-1, 1), (-2, 2), (-3, 3)])
    emp = {(-1, 1): 68, (-2, 2): 95, (-3, 3): 99.7, (0, 1): 34, (-1, 0): 34, (0, 2): 47.5, (-2, 0): 47.5, (1, 2): 13.5, (-2, -1): 13.5, (-2, 1): 81.5, (-1, 2): 81.5}
    v = emp[(k1, k2)]
    a, b = mu + k1 * sd, mu + k2 * sd
    return Q(f"A normal distribution has mean {mu} and standard deviation {sd}. Use the empirical rule to estimate the percent of data between {a} and {b}.", f"{D(F(str(v)))}%",
             [f"{a} is {k1} SD and {b} is {k2} SD from the mean.", "68–95–99.7 rule: 34% from the mean to 1 SD, 13.5% from 1 to 2 SD.", f"≈ {D(F(str(v)))}%."],
             [f"{x_}%" for x_ in [D(F(str(w_))) for w_ in sorted({68, 95, 99.7, 34, 47.5, 13.5, 81.5, 50} - {v}, key=lambda z: abs(z - v))[:3]]], PY("empirical", k1=k1, k2=k2), why=["Used the wrong interval of the rule", "Used the wrong interval of the rule", "Used the wrong interval of the rule"])


@fam("012")
def s8_z(r, L):
    mu, sd = rint(r, 50, 120), rint(r, 4, 20)
    xv = mu + rint(r, -30, 30)
    z = sp.Rational(xv - mu, sd)
    if L < 2:
        return Q(f"Scores are normally distributed with mean {mu} and standard deviation {sd}. Find the z-score of {xv}. Round to the nearest hundredth.", Rd(F(z.p, z.q), 2),
                 ["z = (x - μ) ÷ σ.", f"({xv} - {mu}) ÷ {sd}.", f"z ≈ {Rd(F(z.p, z.q), 2)}."], [Rd(F(sd, xv - mu) if xv != mu else F(1), 2), Rd(F(xv - mu), 2), Rd(F(mu - xv, sd), 2) if xv != mu else "1.00"],
                 H(f"Rational({xv} - {mu}, {sd})", "round", places=2), why=["Divided σ by the difference", "Forgot to divide by σ", "Subtracted in the wrong order"])
    side = pick(r, ["below", "above"])
    pv = 0.5 * (1 + math.erf(float(z) / math.sqrt(2)))
    v = pv if side == "below" else 1 - pv
    return Q(f"Scores are normally distributed with mean {mu} and standard deviation {sd}. Find the probability that a randomly chosen score is {side} {xv}. Round to four decimal places.", Rd(v, 4),
             [f"z = ({xv} - {mu}) ÷ {sd} ≈ {Rd(F(z.p, z.q), 2)}.", f"Use normalcdf: P({'Z < z' if side == 'below' else 'Z > z'}).", f"≈ {Rd(v, 4)}."], [Rd(1 - v, 4), Rd(float(z), 4), Rd(abs(v - 0.5), 4)],
             H(f"(1 + erf(Rational({xv} - {mu}, {sd})/sqrt(2)))/2" if side == "below" else f"1 - (1 + erf(Rational({xv} - {mu}, {sd})/sqrt(2)))/2", "round", places=4), why=["Found the other tail", "Gave the z-score", "Subtracted 0.5"])


# ============================================================== S9 Binomial
@fam("012")
def s9_binom(r, L):
    n_ = rint(r, 3, 6) if L == 0 else rint(r, 5, 12)
    p = pick(r, [sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(3, 10), sp.Rational(1, 5), sp.Rational(3, 5)])
    k_ = rint(r, 0, n_)
    kind = "eq" if L < 2 else pick(r, ["eq", "atleast", "mean"])
    if kind == "mean":
        v = n_ * p
        return Q(f"A basketball player makes each free throw with probability {D(F(p.p, p.q))}, independently. In {n_} attempts, find the expected number of made free throws and the standard deviation (to the nearest hundredth).",
                 f"mean = {D(F(v.p, v.q))}; SD ≈ {Rd(math.sqrt(float(n_ * p * (1 - p))), 2)}", ["μ = np.", "σ = √(np(1 - p)).", f"μ = {D(F(v.p, v.q))}, σ ≈ {Rd(math.sqrt(float(n_ * p * (1 - p))), 2)}."],
                 [f"mean = {D(F(v.p, v.q))}; SD ≈ {Rd(float(n_ * p * (1 - p)), 2)}", f"mean = {D(F((n_ * (1 - p)).p, (n_ * (1 - p)).q))}; SD ≈ {Rd(math.sqrt(float(n_ * p * (1 - p))), 2)}", f"mean = {D(F(v.p, v.q))}; SD ≈ {Rd(math.sqrt(float(n_ * p)), 2)}"],
                 PY("binom_ms", n=n_, p=str(p)), why=["Forgot the square root for SD", "Used 1 - p for the mean", "Forgot the (1 - p) factor"], tags=["modeling"], mode="sa")
    if kind == "atleast":
        k_ = rint(r, 1, 2)
        v = 1 - sum(sp.binomial(n_, j) * p ** j * (1 - p) ** (n_ - j) for j in range(k_))
        return Q(f"Each item from a machine is defective with probability {D(F(p.p, p.q))}, independently. In a sample of {n_}, find P(at least {k_} defective). Round to four decimal places.", Rd(float(v), 4),
                 [f"P(X ≥ {k_}) = 1 - P(X ≤ {k_ - 1}).", f"Use the binomial formula for X = 0{', 1' if k_ == 2 else ''}.", f"≈ {Rd(float(v), 4)}."],
                 [Rd(float(1 - v), 4), Rd(float(sp.binomial(n_, k_) * p ** k_ * (1 - p) ** (n_ - k_)), 4), Rd(float(1 - (1 - p) ** n_ - (0 if k_ == 1 else 0) - (sp.binomial(n_, 1) * p * (1 - p) ** (n_ - 1) if k_ == 2 else p)), 4)],
                 H(f"1 - sum(binomial({n_}, j)*Rational({p.p}, {p.q})**j*(1 - Rational({p.p}, {p.q}))**({n_} - j) for j in range({k_}))", "round", places=4),
                 why=["Gave the complement", "Found P(X = k) only", "Made an error in the complement"], tags=["modeling"])
    v = sp.binomial(n_, k_) * p ** k_ * (1 - p) ** (n_ - k_)
    need(v > sp.Rational(1, 50))
    exact = L == 0
    ans = fr(v) if exact else Rd(float(v), 4)
    w1 = p ** k_ * (1 - p) ** (n_ - k_)
    w2 = sp.binomial(n_, k_) * p ** k_
    w3 = sp.binomial(n_, k_) * p ** (n_ - k_) * (1 - p) ** k_
    ws = [fr(w) if exact else Rd(float(w), 4) for w in (w1, w2, w3)]
    need(ans not in ws and len(set(ws)) == 3)
    return Q(f"A trial succeeds with probability {fr(p) if exact else D(F(p.p, p.q))}. In {n_} independent trials, find P(exactly {k_} successes)." + ("" if exact else " Round to four decimal places."), ans,
             ["P(X = k) = C(n, k)pᵏ(1 - p)ⁿ⁻ᵏ.", f"C({n_}, {k_}) = {sp.binomial(n_, k_)}.", f"P = {ans}."], ws,
             H(f"binomial({n_}, {k_})*Rational({p.p}, {p.q})**{k_}*(1 - Rational({p.p}, {p.q}))**{n_ - k_}", "expr" if exact else "round", **({} if exact else {"places": 4})),
             why=["Forgot C(n, k)", "Forgot the failure factor", "Switched p and 1 - p"])


@fam("012")
def s9_expect(r, L):
    p = pick(r, [sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 5), sp.Rational(1, 10), sp.Rational(3, 4), sp.Rational(2, 5), sp.Rational(3, 10)])
    n_ = rint(r, 2, 12) * p.q
    v = n_ * p
    need(v <= 30)
    ctx = pick(r, [f"A coin-like trial succeeds with probability {D(F(p.p, p.q))}. In {n_} independent trials, what is the expected number of successes?",
                   f"A basketball player makes {D(F(p.p * 100, p.q))}% of free throws. In {n_} attempts, how many makes are expected?",
                   f"Each seed sprouts with probability {D(F(p.p, p.q))}. If {n_} seeds are planted, how many are expected to sprout?"])
    steps = ["For a binomial distribution, μ = np.", f"{n_} × {D(F(p.p, p.q))} = {v}."]
    if L == 2:
        ctx += " Also explain why this is a binomial setting."
        steps = ["Binomial setting: a fixed number of independent trials, two outcomes, the same success probability each time.", f"n = {n_}, p = {D(F(p.p, p.q))}.", "For a binomial distribution, μ = np.", f"μ = {n_} × {D(F(p.p, p.q))}.", f"μ = {v}."]
    return Q(ctx, str(v), steps, [str(n_ - v) if n_ - v != v else str(v + 1), str(n_), str(round(float(sp.sqrt(n_ * p * (1 - p))), 2))],
             H(f"{n_}*Rational({p.p}, {p.q})"), why=["Used 1 - p", "Gave the number of trials", "Gave the standard deviation"], tags=["modeling"])


SKILLS = {
    1: dict(name="Probability, Odds, and Distributions", std=["S-CP.A.1", "S-MD.A.1"], fams=[s1_basic, s1_ev], extra=[err_of(s1_basic), open_of(s1_basic)]),
    2: dict(name="Independent and Dependent Events", std=["S-CP.A.2", "S-CP.B.8"], fams=[s2_draw, s2_classify], extra=[err_of(s2_draw), open_of(s2_draw)]),
    3: dict(name="Permutations and Combinations", std=["S-CP.B.9"], fams=[s3_count, s3_prob], extra=[err_of(s3_count), open_of(s3_count)]),
    4: dict(name="Compound Event Probabilities", std=["S-CP.B.7", "S-CP.A.4"], fams=[s4_or, s4_table], extra=[err_of(s4_or), open_of(s4_table)]),
    5: dict(name="Probability Models and Decision Making", std=["S-MD.B.5", "S-MD.B.7"], fams=[s5_game, s1_ev, reuse(s9_expect, (0, 1, 2), 'm')], extra=[err_of(s5_game), open_of(s5_game)]),
    6: dict(name="Data Types and Statistical Displays", std=["S-ID.A.1"], fams=[s6_types, s6_display, s6_stats], extra=[err_of(s6_stats), open_of(s6_stats)]),
    7: dict(name="Shapes of Distributions", std=["S-ID.A.2", "S-ID.A.3"], fams=[s7_shape, s7_center, s7_outlier, s7_meanmed], extra=[err_of(s7_outlier), open_of(s7_outlier)]),
    8: dict(name="Normal Distributions", std=["S-ID.A.4"], fams=[s8_empirical, s8_z], extra=[err_of(s8_z), open_of(s8_z)]),
    9: dict(name="Binomial Probabilities", std=["S-MD.A.3", "S-CP.B.9"], fams=[s9_binom, s9_expect, reuse(s9_expect, (2, 2, 2), 'h')], extra=[err_of(s9_binom), open_of(s9_binom)]),
}
