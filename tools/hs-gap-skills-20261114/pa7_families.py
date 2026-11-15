"""Pre-Algebra (accelerated Grade 7) gap skill (2026-11-14): Comparing Two Populations (7.SP.B.3, 7.SP.B.4).

Data unit `data-analysis-probability`, new skill 09. Same item contract as calc_families.py:
I(prompt, answer, steps, wrongs, check, fam). Every data set is printed in the prompt, and the
check data lets verify.py recompute each answer and reject each distractor from the numbers alone.
"""
from fractions import Fraction as F
from calc_families import I, Reject, need, ri

CONTEXTS = [
    ("Two classes took the same quiz (points)", "Class A", "Class B", "points"),
    ("Two basketball players' points over several games", "Player A", "Player B", "points"),
    ("Daily high temperatures (°F) in two towns", "Town A", "Town B", "°F"),
    ("Minutes two groups of students spent reading each night", "Group A", "Group B", "minutes"),
    ("Heights (cm) of plants given two different fertilizers", "Fertilizer A", "Fertilizer B", "cm"),
    ("Number of push-ups done by students in two gym classes", "Class A", "Class B", "push-ups"),
    ("Wait times (minutes) at two coffee shops", "Shop A", "Shop B", "minutes"),
]
SIZES = [(6, 7), (8, 9), (10, 11)]  # data-set size by level index


def t(v):
    """Number text: integers plain, otherwise rounded to the nearest tenth."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    x = round(float(v) + 1e-9, 1)
    return str(int(x)) if x == int(x) else f"{x:.1f}"


def exact(v):
    return F(v).denominator == 1 or (F(v) * 10).denominator == 1


def lst(xs):
    return ", ".join(str(x) for x in xs)


def dataset(r, L, mean, spread):
    """Integer data set of the level's size whose mean is the integer `mean`."""
    n = r.choice(SIZES[L])
    for _ in range(200):
        dev = [r.randint(-spread, spread) for _ in range(n - 1)]
        last = -sum(dev)
        if abs(last) <= spread:
            xs = [mean + d for d in dev + [last]]
            if min(xs) > 0 and len(set(xs)) >= 3:
                r.shuffle(xs)
                return xs
    raise Reject()


def mean(xs):
    return F(sum(xs), len(xs))


def mad(xs):
    m = mean(xs)
    return sum(abs(x - m) for x in xs) / len(xs)


def median(xs):
    s, n = sorted(xs), len(xs)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def two(r, L, gap=None):
    ctx = r.choice(CONTEXTS)
    base = ri(r, 12, 60)
    spread = ri(r, 3, 6 + 2 * L)
    g = gap if gap is not None else ri(r, 2, 4 * spread)
    a = dataset(r, L, base + g, spread)
    b = dataset(r, L, base, spread)
    if r.random() < 0.5:
        a, b = b, a
    return ctx, a, b


def header(ctx, a, b):
    title, na, nb, _ = ctx
    return f"{title}:\n{na}: {lst(a)}\n{nb}: {lst(b)}"


# --------------------------------------------------------------------------- difference of means
def cmp_mean_diff(r, L):
    ctx, a, b = two(r, L)
    ma, mb = mean(a), mean(b)
    d = abs(ma - mb)
    need(d > 0 and median(a) != median(b) and abs(median(a) - median(b)) != d)
    title, na, nb, unit = ctx
    prompt = header(ctx, a, b) + f"\nWhat is the difference between the two means?"
    steps = [f"Mean of {na}: {sum(a)} ÷ {len(a)} = {t(ma)}.", f"Mean of {nb}: {sum(b)} ÷ {len(b)} = {t(mb)}.",
             f"Difference: {t(max(ma, mb))} − {t(min(ma, mb))} = {t(d)} {unit}."]
    wrongs = [(t(abs(median(a) - median(b))), "they found the difference of the medians, not the means"),
              (t(abs(sum(a) - sum(b))), "they subtracted the totals instead of the means"),
              (t(abs(max(a) - max(b))), "they compared only the largest values")]
    return I(prompt, t(d), steps, [w for w in wrongs if w[0] != t(d)], dict(k="meandiff", A=a, B=b), "cmp_mean_diff")


# --------------------------------------------------------------------------- MAD of one group
def cmp_mad(r, L):
    ctx, a, b = two(r, L)
    xs = r.choice([a, b])
    name = ctx[1] if xs is a else ctx[2]
    m, v = mean(xs), mad(xs)
    need(exact(v) and v > 0)
    devs = [abs(x - m) for x in xs]
    prompt = f"{ctx[0]}.\n{name}: {lst(xs)}\nThe mean is {t(m)}. Find the mean absolute deviation (MAD) of {name}."
    steps = [f"Distance of each value from the mean {t(m)}: {lst(t(d) for d in devs)}.",
             f"Sum of the distances: {t(sum(devs))}.", f"MAD = {t(sum(devs))} ÷ {len(xs)} = {t(v)}."]
    wrongs = [(t(sum(devs)), "they added the distances but did not divide by the number of values"),
              (t(F(max(xs) - min(xs), 2)), "they used half the range instead of the average distance from the mean"),
              ("0", "they averaged the signed deviations, which always add to 0")]
    return I(prompt, t(v), steps, [w for w in wrongs if w[0] != t(v)], dict(k="mad", A=xs), "cmp_mad")


# --------------------------------------------------------------------------- difference of means in MADs
def cmp_mads_apart(r, L):
    ctx = r.choice(CONTEXTS)
    title, na, nb, unit = ctx
    if L < 2:
        m_ = ri(r, 2, 8)
        k = F(r.choice([1, 2, 3, 4, 5, 6, 7]), 2) if L else F(ri(r, 1, 4))
        lo = ri(r, 20, 70)
        hi = lo + k * m_
        need(hi.denominator == 1)
        prompt = (f"{title}. The mean for {na} is {t(hi)} {unit} and the mean for {nb} is {lo} {unit}. "
                  f"Both groups have a mean absolute deviation (MAD) of {m_}.\nThe difference between the means is how many times the MAD?")
        steps = [f"Difference of means: {t(hi)} − {lo} = {t(hi - lo)}.", f"Divide by the MAD: {t(hi - lo)} ÷ {m_} = {t(k)}."]
        check = dict(k="ratio", hi=float(hi), lo=lo, mad=m_)
    else:
        ctx, a, b = two(r, L)
        ma, mb, va, vb = mean(a), mean(b), mad(a), mad(b)
        need(va == vb and exact(ma) and exact(mb))
        k = abs(ma - mb) / va
        need(exact(k) and k > 0)
        m_ = va
        prompt = header(ctx, a, b) + "\nBoth groups have the same mean absolute deviation. The difference between the means is how many times the MAD?"
        steps = [f"Means: {t(ma)} and {t(mb)}; difference {t(abs(ma - mb))}.", f"MAD of each group: {t(va)}.", f"{t(abs(ma - mb))} ÷ {t(va)} = {t(k)}."]
        check = dict(k="ratio_data", A=a, B=b)
        hi = max(ma, mb)
    wrongs = [(t(k * m_), "they gave the difference of the means but did not divide by the MAD"),
              (t(1 / k), "they divided the MAD by the difference instead of the difference by the MAD")]
    if k != 1:
        wrongs.append((t(k + 1), "they counted one extra MAD"))
    return I(prompt, t(k), steps, [w for w in wrongs if w[0] != t(k)], check, "cmp_mads_apart")


# --------------------------------------------------------------------------- difference of medians
def cmp_median_diff(r, L):
    ctx, a, b = two(r, L)
    da = abs(median(a) - median(b))
    need(da > 0 and abs(mean(a) - mean(b)) != da)
    _, na, nb, unit = ctx
    prompt = header(ctx, a, b) + "\nWhat is the difference between the two medians?"
    steps = [f"{na} in order: {lst(sorted(a))}; median {t(median(a))}.", f"{nb} in order: {lst(sorted(b))}; median {t(median(b))}.",
             f"Difference: {t(da)} {unit}."]
    wrongs = [(t(abs(F(a[len(a) // 2]) - F(b[len(b) // 2]))), "they took the middle value of each list without putting the data in order first"),
              (t(abs(mean(a) - mean(b))), "they found the difference of the means, not the medians"),
              (t(abs((max(a) - min(a)) - (max(b) - min(b)))), "they compared the ranges")]
    return I(prompt, t(da), steps, [w for w in wrongs if w[0] != t(da)], dict(k="mediandiff", A=a, B=b), "cmp_median_diff")


# --------------------------------------------------------------------------- inference from random samples
CLAIM_BIG = "The difference is large compared with the variability, so the populations likely differ."
CLAIM_SMALL = "The difference is small compared with the variability, so the samples overlap a lot and the populations may not differ."
CLAIM_MEAN = "Any difference in the means proves every member of one group scores higher."
CLAIM_SIZE = "No conclusion is possible, because the samples have different means."


def cmp_infer(r, L):
    title, na, nb, unit = r.choice(CONTEXTS)
    m_ = ri(r, 2, 6)
    k = r.choice([F(1, 2), F(1), F(3, 2), F(3), F(7, 2), F(4), F(5)])
    lo = ri(r, 20, 70)
    hi = lo + k * m_
    need(hi.denominator == 1)
    n = r.choice([20, 25, 30, 40])
    prompt = (f"Random samples of {n} were taken from two populations. {title}: the mean for {na} is {t(hi)} and the mean for {nb} is {lo}. "
              f"Each sample has a mean absolute deviation of about {m_}.\nWhich statement is best supported?")
    big = k >= 2
    ans = CLAIM_BIG if big else CLAIM_SMALL
    steps = [f"Difference of means: {t(hi - lo)}, which is {t(k)} times the MAD of {m_}.",
             "A difference of about 2 or more MADs means the distributions overlap very little." if big else
             "A difference of less than 2 MADs means the distributions overlap a lot."]
    wrongs = [(CLAIM_SMALL if big else CLAIM_BIG, "they did not compare the difference with the MAD"),
              (CLAIM_MEAN, "a difference in centers does not say anything about every individual"),
              (CLAIM_SIZE, "random samples are exactly what let us compare populations")]
    return I(prompt, ans, steps, wrongs, dict(k="claim", hi=float(hi), lo=lo, mad=m_, big=CLAIM_BIG, small=CLAIM_SMALL), "cmp_infer")


SKILLS = {
    ("prealgebra7", "data-analysis-probability", "Comparing Two Populations"):
        ([cmp_mean_diff, cmp_mad, cmp_mads_apart, cmp_median_diff, cmp_infer], ["7.SP.B.3", "7.SP.B.4"]),
}
NEW_UNITS = {}
