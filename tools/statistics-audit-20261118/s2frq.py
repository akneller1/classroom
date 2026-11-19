"""Statistics audit #2 (2026-11-18, batch S2): one AP-style free-response problem per skill and level (41 × 3 = 123).
Each problem has a context, four parts that build on each other, at least one part that asks students to justify or
explain, and scoring notes with points for each part. Inference problems that carry out a full procedure use the four
steps (State, Plan, Do, Conclude). CP2 parts carry a short reminder of the formula or method to use; Honors parts ask for
one more step (a follow-up, a comparison or a reverse problem). Every number is computed here."""
import math
import statistics as st
from scipy import stats
from s2common import wt, QUANT, PROP, f, g, pct, table_a, tstar, ZSTAR, mean_sd, phrase_list

T = {}


def frq(unit, k):
    def deco(fn):
        T[(unit, k)] = fn
        return fn
    return deco


def P(prompt, answer, sol, pts, score):
    return (prompt, answer, sol, pts, score)


def cue(lv, text):
    return f' ({text})' if lv == 'cp2' else ''


def quartiles(v):
    v = sorted(v)
    n = len(v)
    lo, hi = v[:n // 2], v[(n + 1) // 2:]
    return v[0], st.median(lo), st.median(v), st.median(hi), v[-1]


def data(rng, lv, mu, sd, dp, n, skew=False):
    step = 10 ** -dp
    vals = [round(round(rng.gauss(mu, sd * 0.8) / step) * step, dp) for _ in range(n)]
    if skew:
        vals[-1] = round(max(vals) + 2.2 * sd, dp)
    if dp == 0:
        vals = [int(v) for v in vals]
    return sorted(vals)


@frq(1, 1)
def variables_displays(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice([q for q in QUANT if q[5] == 0 and q[3] < 400])
    vals = data(rng, lv, mu, sd, 0, {'cp2': 12, 'cp1': 15, 'honors': 18}[lv], skew=True)
    stems = {s: [] for s in range(vals[0] // 10, vals[-1] // 10 + 1)}
    for v in vals:
        stems[v // 10].append(v % 10)
    plot = '; '.join(f'{s} | {"".join(map(str, l))}'.rstrip() for s, l in sorted(stems.items()))
    stem = f'The {var} ({unit}) for a random sample of {len(vals)} {pop}: {phrase_list(vals, 0)}.'
    parts = [
        P('Is the variable categorical or quantitative? If quantitative, is it discrete or continuous? Explain.' + cue(lv, 'ask whether an average makes sense'),
          'Quantitative; continuous (a measurement that can take any value in an interval)',
          'The values are numerical measurements for which an average makes sense, so the variable is quantitative; a time, weight or length can take any value in an interval, so it is continuous.',
          1, 'Quantitative with a correct reason, and continuous.'),
        P('Make a stem-and-leaf plot of the data, using tens as stems. List each stem with its leaves.' + cue(lv, 'the stem is the tens digit and the leaf is the ones digit; keep empty stems'),
          plot, f'Split each value into tens (stem) and ones (leaf): {plot}. Keep the empty stems so the gap shows, and include a key such as {vals[0] // 10} | {vals[0] % 10} = {vals[0]} {unit}.',
          1, 'All stems in order (including any empty stems), leaves in order, and a key.'),
        P('Describe the shape of the distribution and identify any value that appears to be an outlier.',
          f'Skewed right, with a possible high outlier at {vals[-1]}',
          f'Most values cluster together, with a long tail toward the high values: the largest value, {vals[-1]}, is separated from the rest by a gap.',
          1, 'Skewed right (or right tail) and the high value identified.'),
        P('A classmate says a histogram with only two bins would show this distribution better than your stem plot. Do you agree? Justify your answer.',
          'No: two bins hide the shape and the gap before the outlier; the stem plot keeps every value',
          'With two bins nearly all detail of the shape is lost, including the gap before the outlier, while a stem plot shows each individual value.'
          + (' A histogram with more bins (about 5–8 here) would be a reasonable alternative.' if lv != 'cp2' else ''),
          1, 'Disagrees with a reason about lost detail (shape, gaps or outliers hidden).'),
    ]
    return stem, parts, ['1.2.B', '1.2.C', '1.5.A', '1.6.A'], var


@frq(1, 2)
def describe_distribution(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice([q for q in QUANT if q[5] <= 1])
    dp = 0 if sd >= 5 else 1
    n = {'cp2': 11, 'cp1': 13, 'honors': 15}[lv]
    vals = data(rng, lv, mu, sd, dp, n, skew=True)
    mn, q1, md, q3, mx = quartiles(vals)
    iqr = q3 - q1
    lf, uf = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outs = [v for v in vals if v < lf or v > uf]
    m, s = mean_sd(vals)
    stem = f'The {var} ({unit}) for a random sample of {n} {pop}: {phrase_list(vals, dp)}.'
    parts = [
        P('Find the five-number summary.' + cue(lv, 'Q1 and Q3 are the medians of the lower and upper halves; leave out the median when n is odd'),
          f'Min = {g(mn)}, Q1 = {g(q1)}, Median = {g(md)}, Q3 = {g(q3)}, Max = {g(mx)}',
          f'n = {n}; the median is the {(n + 1) // 2}th value, {g(md)}. Q1 = {g(q1)} and Q3 = {g(q3)} are the medians of the lower and upper halves.',
          1, 'All five values correct.'),
        P('Use the 1.5 × IQR rule to determine whether there are any outliers. Show the fences.',
          ('Outliers: ' + ', '.join(g(v) for v in outs)) if outs else 'No outliers',
          f'IQR = {g(q3)} − {g(q1)} = {g(round(iqr, 4))}. Fences: {g(q1)} − 1.5({g(round(iqr, 4))}) = {g(round(lf, 4))} and {g(q3)} + 1.5({g(round(iqr, 4))}) = {g(round(uf, 4))}. '
          + (f'{", ".join(g(v) for v in outs)} {"is" if len(outs) == 1 else "are"} outside the fences.' if outs else 'No value is outside the fences.'),
          1, 'Correct fences with the comparison stated.'),
        P('Describe the distribution: shape, center, spread and outliers, in context.',
          f'Skewed right; median {g(md)} {unit}; IQR {g(round(iqr, 4))} {unit}' + (f'; outlier(s) {", ".join(g(v) for v in outs)}' if outs else ''),
          f'The distribution of {var} is skewed right (mean {f(m, 2)} > median {g(md)}), centered at a median of about {g(md)} {unit}, with an IQR of {g(round(iqr, 4))} {unit}'
          + (f' and a high outlier at {g(outs[-1])} {unit}.' if outs else '.'),
          2, '1 point for shape and outliers; 1 point for center and spread with numbers, in context.'),
        P('Which measure of center better describes a typical value here, the mean or the median? Justify your answer.',
          'The median, because the distribution is skewed (the mean is pulled toward the high values)',
          f'The mean ({f(m, 2)}) is pulled up by the long right tail' + (' and the outlier' if outs else '') + f', while the median ({g(md)}) is resistant.',
          1, 'Median, with skewness or the outlier as the reason.'),
    ]
    return stem, parts, ['1.7.A', '1.7.D', '1.6.A', '1.7.F'], f'{var} n={n}'


@frq(1, 3)
def mean_sd_frq(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice([q for q in QUANT if q[5] <= 1])
    dp = 0 if sd >= 5 else 1
    n = {'cp2': 6, 'cp1': 7, 'honors': 8}[lv]
    vals = data(rng, lv, mu, sd, dp, n)
    m, s = mean_sd(vals)
    md = st.median(vals)
    add = round(sd * 2, dp)
    stem = f'The {var} ({unit}) for {n} randomly chosen {pop}: {phrase_list(vals, dp)}.'
    parts = [
        P('Find the mean and the median. Round the mean to two decimal places.' + cue(lv, 'mean = sum ÷ n; the median is the middle of the ordered values'),
          f'Mean ≈ {f(m, 2)}; median = {g(md)}', f'Sum = {g(round(sum(vals), 4))}, so x̄ = {g(round(sum(vals), 4))}/{n} ≈ {f(m, 2)}. Median = {g(md)} (average of the two middle values when n is even).',
          1, 'Both correct.'),
        P('Find the sample standard deviation. Round to two decimal places.' + cue(lv, 's = √(Σ(x − x̄)²/(n − 1))'),
          f(s, 2), f'Σ(x − x̄)² ≈ {f(sum((v - m) ** 2 for v in vals), 3)}; s = √({f(sum((v - m) ** 2 for v in vals), 3)}/{n - 1}) ≈ {f(s, 2)}.', 1, 'Correct value (n − 1 in the denominator).'),
        P('Interpret the standard deviation in context.',
          f'The {var} typically varies by about {f(s, 2)} {unit} from the mean of {f(m, 2)} {unit}',
          f'The {var} of these {pop} typically differs from the mean of about {f(m, 2)} {unit} by about {f(s, 2)} {unit}.', 1, 'Typical distance from the mean, with units and context.'),
        P(f'Suppose the largest value had been recorded as {g(round(max(vals) + add, dp))} instead of {g(max(vals))}. Which of the mean, median and standard deviation would change? Explain.'
          + (' Then give the new mean.' if lv == 'honors' else ''),
          'The mean and standard deviation increase; the median does not change' + (f'; new mean ≈ {f(m + add / n, 2)}' if lv == 'honors' else ''),
          f'The mean uses every value, so it rises by {g(add)}/{n}' + (f' to about {f(m + add / n, 2)}' if lv == 'honors' else '') + '; the largest value moves farther from the mean, so s increases; the middle value(s) are unchanged, so the median stays at ' + g(md) + '.',
          1, 'All three correct with a reason (resistance of the median).'),
    ]
    return stem, parts, ['1.7.A', '1.7.B', '1.7.F'], f'{var} n={n}'


@frq(1, 4)
def compare_boxplots(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice([q for q in QUANT if q[5] == 0])
    g1, g2 = 'Last year', 'This year'

    def summ(shift, spread):
        q1 = round(mu - 0.6 * sd * spread + shift)
        md = round(mu + shift)
        q3 = round(mu + 0.7 * sd * spread + shift)
        return (round(q1 - 1.2 * sd * spread), q1, md, q3, round(q3 + 1.4 * sd * spread))
    a, b = summ(0, 1.0), summ(round(0.5 * sd), 1.6)
    b = b[:4] + (b[3] + round(3.2 * (b[3] - b[1])) if lv != 'cp2' else b[4],)
    fb = (b[1] - 1.5 * (b[3] - b[1]), b[3] + 1.5 * (b[3] - b[1]))
    stem = (f'Random samples of {pop} were taken last year and this year, and the {var} ({unit}) was recorded. Five-number summaries (Min, Q1, Median, Q3, Max): '
            f'last year {", ".join(map(str, a))}; this year {", ".join(map(str, b))}.')
    out_b = b[4] > fb[1]
    parts = [
        P('Find the IQR for each year.' + cue(lv, 'IQR = Q3 − Q1'), f'Last year: {a[3] - a[1]}; this year: {b[3] - b[1]}', f'Last year: {a[3]} − {a[1]} = {a[3] - a[1]}. This year: {b[3]} − {b[1]} = {b[3] - b[1]}.', 1, 'Both IQRs correct.'),
        P('Is this year’s maximum an outlier? Show the upper fence.', f'{"Yes" if out_b else "No"}: upper fence {g(fb[1])}',
          f'Upper fence = Q3 + 1.5 × IQR = {b[3]} + 1.5({b[3] - b[1]}) = {g(fb[1])}; the maximum {b[4]} is {"above" if out_b else "not above"} it.', 1, 'Correct fence and decision.'),
        P('Compare the two distributions (center and spread) in context.',
          f'This year has the higher median ({b[2]} vs {a[2]}) and more variability (IQR {b[3] - b[1]} vs {a[3] - a[1]})',
          f'The median {var} is higher this year ({b[2]} vs {a[2]} {unit}), and this year’s values are more spread out (IQR {b[3] - b[1]} vs {a[3] - a[1]} {unit}; range {b[4] - b[0]} vs {a[4] - a[0]}).',
          2, '1 point for center with comparative language; 1 point for spread, both with numbers and context.'),
        P(f'About what percent of this year’s sample had a value greater than {b[1]}? Explain how you know' + ('. Then say whether more than half of this year’s sample exceeded last year’s median.' if lv == 'honors' else '.'),
          'About 75%' + (f'; yes, since this year’s median ({b[2]}) is above {a[2]}' if lv == 'honors' else ''),
          f'{b[1]} is this year’s Q1, and about 75% of the values are above Q1.' + (f' This year’s median ({b[2]}) exceeds last year’s ({a[2]}), so more than half of this year’s sample is above it.' if lv == 'honors' else ''),
          1, 'About 75% with the quartile reason' + (' and the comparison of medians.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['1.8.A', '1.7.D', '1.9.B', '1.9.C'], var


PAIRS7 = [('hours studied', 'quiz score (out of 100)', 'students', 52, 4.0, 4, (0, 10), 0),
          ('outside temperature (°F)', 'hot drinks sold', 'days at a café', 140, -1.6, 7, (20, 80), 0),
          ('age of a car (years)', 'resale value (thousands of dollars)', 'used cars of one model', 29, -2.1, 1.4, (1, 12), 1),
          ('minutes of practice per day', 'free throws made out of 50', 'basketball players', 18, 0.42, 2.5, (10, 60), 0),
          ('hours of sleep the night before', 'reaction time (milliseconds)', 'volunteers', 330, -11, 9, (3, 12), 0)]


@frq(1, 5)
def normal_model(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    d = max(dp, 1)
    x1 = round(mu + rng.choice([1.3, 1.6, -1.2, 0.9]) * sd, d)
    z1 = (x1 - mu) / sd
    pa = round(1 - table_a(z1), 4)
    perc = rng.choice([0.90, 0.80, 0.25, 0.10])
    zp = round(stats.norm.ppf(perc), 2)
    xp = mu + zp * sd
    stem = f'The {var} is approximately Normal with mean {g(mu)} {unit} and standard deviation {g(sd)} {unit}.'
    mu2, sd2 = round(mu * 1.1, 1), round(sd * 1.3, 2)
    x2 = round(mu2 + (z1 + rng.choice([-0.4, 0.4])) * sd2, d)
    z2 = (x2 - mu2) / sd2
    parts = [
        P(f'Find the z-score of a value of {g(x1)} {unit}. Round to two decimal places.' + cue(lv, 'z = (x − μ)/σ'),
          f(z1, 2), f'z = ({g(x1)} − {g(mu)})/{g(sd)} ≈ {f(z1, 2)}.', 1, 'Correct z-score.'),
        P(f'What proportion of {pop} have a value greater than {g(x1)} {unit}? Use Table A (round z to two decimal places). Round to four decimal places.',
          f(pa, 4), f'P(X > {g(x1)}) = P(Z > {f(z1, 2)}) = 1 − {f(table_a(z1), 4)} = {f(pa, 4)}.', 1, 'Correct area with the direction shown (a sketch or notation).'),
        P(f'Find the value at the {round(perc * 100)}th percentile. Round to two decimal places.' + cue(lv, 'find z with area to its left, then x = μ + zσ'),
          f(xp, 2), f'From Table A, the z with area {g(perc)} to its left is about {f(zp, 2)}. x = {g(mu)} + ({f(zp, 2)})({g(sd)}) ≈ {f(xp, 2)} {unit}.', 1, 'Correct z and value.'),
        P(f'A second population has mean {g(mu2)} and SD {g(sd2)}. Which is relatively higher in its own group: {g(x1)} in the first or {g(x2)} in the second? Justify with z-scores.',
          f'{"The first" if z1 > z2 else "The second"} ({f(max(z1, z2), 2)} vs {f(min(z1, z2), 2)} standard deviations)',
          f'z₁ = {f(z1, 2)}; z₂ = ({g(x2)} − {g(mu2)})/{g(sd2)} ≈ {f(z2, 2)}. The larger z-score is relatively higher: the {"first" if z1 > z2 else "second"} value.',
          1, 'Both z-scores and a comparison.'),
    ]
    return stem, parts, ['1.9.D', '2.11.D', '2.11.E', '1.9.E'], f'{var}'


@frq(1, 6)
def two_way(rng, lv):
    rv, rows, cv, cols = rng.choice([('grade', ['Juniors', 'Seniors'], 'plans after graduation', ['College', 'Work', 'Undecided']),
                                     ('age group', ['Under 30', '30–49', '50 and over'], 'main news source', ['Online', 'TV']),
                                     ('school', ['North', 'South'], 'transportation', ['Bus', 'Car', 'Walk'])])
    t = [[rng.randint(15, 70) for _ in cols] for _ in rows]
    N = sum(map(sum, t))
    rt = [sum(r) for r in t]
    ct = [sum(t[r][c] for r in range(len(rows))) for c in range(len(cols))]
    table = '; '.join(f'{rows[r]}: ' + ', '.join(f'{cols[c]} {t[r][c]}' for c in range(len(cols))) for r in range(len(rows)))
    stem = f'A survey of {N} randomly selected people records {rv} and {cv}. Counts — {table}.'
    cond = [[t[r][0] / rt[r] for r in range(len(rows))]]
    c0 = cols[0]
    spread = max(cond[0]) - min(cond[0])
    assoc = spread > 0.08
    parts = [
        P(f'What proportion of all people surveyed chose {c0}? Round to three decimal places.' + cue(lv, 'use the column total over the table total'),
          f(ct[0] / N, 3), f'{ct[0]}/{N} ≈ {f(ct[0] / N, 3)}.', 1, 'Correct marginal proportion.'),
        P(f'For each {rv}, find the proportion who chose {c0}. Round to three decimal places.',
          '; '.join(f'{rows[r]}: {f(cond[0][r], 3)}' for r in range(len(rows))),
          ' '.join(f'{rows[r]}: {t[r][0]}/{rt[r]} ≈ {f(cond[0][r], 3)}.' for r in range(len(rows))), 1, 'All conditional proportions correct (row totals used).'),
        P(f'Do these data suggest an association between {rv} and {cv}? Justify your answer using part (b).',
          ('Yes' if assoc else 'Not much') + f': the conditional proportions range from {f(min(cond[0]), 3)} to {f(max(cond[0]), 3)}',
          f'If there were no association, the proportion choosing {c0} would be about the same for every {rv}. They differ by {f(spread, 3)}, which ' + ('suggests an association.' if assoc else 'is small, so there is little evidence of an association.'),
          1, 'Decision supported by comparing conditional proportions.'),
        P(f'Describe a graph that would display the conditional distributions of {cv} for each {rv}' + ('' if lv == 'cp2' else ' and explain why it is better than a bar graph of counts') + '.',
          f'A segmented (stacked) bar graph with one 100% bar per {rv}' + ('' if lv == 'cp2' else ', because the groups have different totals'),
          f'One bar per {rv}, each scaled to 100% and split into the {cv} categories.' + ('' if lv == 'cp2' else f' Counts are misleading because the {rv} groups have different totals ({", ".join(map(str, rt))}).'),
          1, 'Segmented/side-by-side relative frequency bars' + ('.' if lv == 'cp2' else ' with the reason about unequal totals.')),
    ]
    return stem, parts, ['2.2.A', '2.2.B', '2.2.C', '2.1.A'], f'{rv} {cv}'


def bivar(rng, lv, n):
    x = sorted(rng.sample(range(1, 20), n))
    b, a = rng.choice([(2.5, 10), (-1.8, 60), (3.2, 5), (-2.2, 70), (1.5, 20)])
    y = [round(a + b * xi + rng.gauss(0, 3), 1) for xi in x]
    return x, y


@frq(1, 7)
def scatter_corr(rng, lv):
    xn, yn, subj, a, b, noise, (lo, hi), ydp = rng.choice(PAIRS7)
    n = {'cp2': 7, 'cp1': 8, 'honors': 9}[lv]
    x = sorted(rng.sample(range(lo, hi + 1), n))
    y = [round(a + b * xi + rng.gauss(0, noise), ydp) for xi in x]
    if ydp == 0:
        y = [int(v) for v in y]
    r = stats.pearsonr(x, y)[0]
    pos = r > 0
    strength = 'strong' if abs(r) >= 0.8 else 'moderate' if abs(r) >= 0.5 else 'weak'
    stem = f'Data for {n} randomly chosen {subj}. x = {xn}: {", ".join(map(str, x))}. y = {yn}: {", ".join(g(v) for v in y)}.'
    parts = [
        P('Describe the association shown by a scatterplot of the data (direction, form, strength).' + cue(lv, 'plot the points first, then describe the overall pattern'),
          f'{strength.capitalize()}, {"positive" if pos else "negative"}, linear', f'As {xn} increases, {yn} tends to {"increase" if pos else "decrease"}; the points follow a roughly linear pattern ({strength}).',
          1, 'Direction, form and strength, in context.'),
        P('Use technology to find the correlation r. Round to three decimal places.', f(r, 3), f'LinReg (or 2-Var Stats) gives r ≈ {f(r, 3)}.', 1, 'Correct r.'),
        P('Interpret r in context.', f'A {strength}, {"positive" if pos else "negative"} linear association between {xn} and {yn}',
          f'r ≈ {f(r, 3)} indicates a {strength}, {"positive" if pos else "negative"} linear relationship between {xn} and {yn}.', 1, 'Strength and direction of the linear relationship, in context.'),
        P(f'A student concludes that changing the {xn.split(" (")[0]} causes the {yn.split(" (")[0]} to change. Is this conclusion justified? Explain.'
          + (' Also say what would happen to r if x were measured in different units.' if lv == 'honors' else ''),
          'No: these are observational data, so other variables could explain the association' + ('; r would not change' if lv == 'honors' else ''),
          'Correlation alone does not show causation: the data were observed, not produced by random assignment, so a confounding variable could explain the pattern.'
          + (' r has no units, so changing units leaves it unchanged.' if lv == 'honors' else ''), 1, 'Not justified, with the observational-study reason' + (' and r unchanged.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['5.1.B', '5.2.A', '5.1.C'], xn


@frq(1, 8)
def lsrl_summary(rng, lv):
    xn, yn, xb, sx, yb, sy, r = rng.choice([('hours studied', 'test score', 4.2, 1.6, 78.0, 9.5, 0.74), ('square footage (hundreds)', 'price (thousands of dollars)', 18.0, 4.5, 320.0, 70.0, 0.86),
                                            ('outside temperature (°F)', 'heating bill (dollars)', 41.0, 12.0, 140.0, 35.0, -0.88), ('arm span (cm)', 'height (cm)', 168.0, 9.0, 170.0, 8.5, 0.93),
                                            ('minutes of exercise per day', 'resting pulse (bpm)', 35.0, 15.0, 72.0, 8.0, -0.61)])
    b = r * sy / sx
    a = yb - round(b, 3) * xb
    x0 = round(xb + rng.choice([-1, 1]) * sx * 0.8, 1)
    yhat = round(a, 2) + round(b, 3) * x0
    subj = 'houses' if 'square' in xn else 'adults' if 'arm' in xn or 'exercise' in xn else 'homes' if 'heating' in yn else 'students'
    stem = f'For a random sample of {subj}, x = {xn} and y = {yn}: x̄ = {g(xb)}, s_x = {g(sx)}, ȳ = {g(yb)}, s_y = {g(sy)}, r = {g(r)}.'
    eq = 'ŷ = ' + lin(round(a, 2), round(b, 3))
    parts = [
        P('Find the slope of the least-squares regression line. Round to three decimal places.' + cue(lv, 'b = r·s_y/s_x'),
          f(b, 3), f'b = r(s_y/s_x) = {g(r)}({g(sy)}/{g(sx)}) ≈ {f(b, 3)}.', 1, 'Correct slope.'),
        P('Find the y-intercept and write the equation of the line.' + cue(lv, 'the line passes through (x̄, ȳ), so a = ȳ − b·x̄'),
          eq, f'a = ȳ − b·x̄ = {g(yb)} − ({f(b, 3)})({g(xb)}) ≈ {f(a, 2)}, so {eq}.', 1, 'Correct intercept and equation in terms of ŷ.'),
        P('Interpret the slope in context.', f'For each additional 1 unit of {xn}, the predicted {yn} {"increases" if b > 0 else "decreases"} by about {f(abs(b), 3)}',
          f'Each 1-unit increase in {xn} is associated with a predicted {"increase" if b > 0 else "decrease"} of about {f(abs(b), 3)} in {yn}.', 1, 'Predicted change in y per unit of x, in context.'),
        P(f'Predict the {yn} for x = {g(x0)}, and find r². Interpret r² in context.',
          f'ŷ ≈ {f(yhat, 2)}; r² ≈ {f(r * r, 3)}',
          f'ŷ = {lin(round(a, 2), round(b, 3), "(" + g(x0) + ")").replace(g(round(b, 3)) + "(", g(abs(round(b, 3))) + "(") } ≈ {f(yhat, 2)}. r² = ({g(r)})² ≈ {f(r * r, 3)}: about {f(100 * r * r, 1)}% of the variation in {yn} is accounted for by the linear model with {xn}.',
          1, 'Prediction and the r² interpretation.'),
    ]
    return stem, parts, ['5.5.A', '5.5.B', '5.3.A'], xn


@frq(1, 9)
def residuals_frq(rng, lv):
    xn, yn, a, b, xs = rng.choice([('age of a car (years)', 'price (thousands of dollars)', 28.4, -2.15, [3, 4, 5, 6, 7]), ('hours of sleep', 'reaction time (ms)', 320.0, -12.5, [5, 6, 7, 8]),
                                   ('height (in)', 'weight (lb)', -180.0, 4.8, [64, 66, 68, 70]), ('distance (miles)', 'delivery time (minutes)', 9.0, 3.1, [2, 3, 4, 5, 6])])
    x0 = rng.choice(xs)
    yhat = a + b * x0
    res = round(rng.choice([-1, 1]) * abs(b) * rng.choice([0.6, 0.9, 1.3]), 2)
    y0 = round(yhat + res, 2)
    pattern = rng.choice(['random', 'curved'])
    far = x0 * 4 if x0 < 20 else x0 + 30
    stem = f'A least-squares line for predicting y = {yn} from x = {xn} is ŷ = {lin(a, b)}.'
    sub = f'{g(a)} {"+" if b >= 0 else "−"} {g(abs(b))}({g(x0)})'
    parts = [
        P(f'Find the predicted {yn} for x = {g(x0)}.' + cue(lv, 'substitute x into the equation'), f(yhat, 2), f'ŷ = {sub} = {f(yhat, 2)}.', 1, 'Correct prediction.'),
        P(f'The actual value for that observation is y = {g(y0)}. Find the residual.' + cue(lv, 'residual = actual − predicted'), f(res, 2),
          f'Residual = y − ŷ = {g(y0)} − {f(yhat, 2)} = {f(res, 2)}.'.replace('− −', '+ '), 1, 'Correct residual with the sign.'),
        P('Interpret the residual in context.', f'The actual {yn} was {f(abs(res), 2)} {"above" if res > 0 else "below"} the value predicted by the line',
          f'The observed {yn} is {f(abs(res), 2)} {"greater" if res > 0 else "less"} than predicted for x = {g(x0)}.', 1, 'Direction and size relative to the prediction, in context.'),
        P(f'A residual plot shows {"random scatter around 0" if pattern == "random" else "a clear curved pattern"}. Is a linear model appropriate? Justify your answer.'
          + (f' Would it be reasonable to predict y for x = {g(far)}? Explain.' if lv == 'honors' else ''),
          ('Yes: random scatter means no leftover pattern' if pattern == 'random' else 'No: the curved pattern shows the relationship is not linear')
          + ('; no, that is extrapolation far beyond the data' if lv == 'honors' else ''),
          ('Random scatter with no pattern means a line captures the form.' if pattern == 'random' else 'A curved residual pattern means a line misses the form; a nonlinear model would fit better.')
          + (f' x = {g(far)} is far outside the observed x-values, so the prediction is an unreliable extrapolation.' if lv == 'honors' else ''),
          1, 'Correct decision with the residual-plot reason' + (' and extrapolation.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['5.3.A', '5.4.A', '5.4.B', '5.4.C'], xn


@frq(2, 1)
def pop_sample_frq(rng, lv):
    from s2fill import STUDIES
    desc, pop, samp, stat, par = rng.choice(STUDIES)
    stem = desc
    parts = [
        P('Identify the population and the sample.', f'Population: {pop.lower()}; sample: {samp.lower()}',
          'The population is the whole group of interest; the sample is the part actually measured.', 1, 'Both identified correctly.'),
        P('Identify the parameter of interest and the statistic that estimates it.' + cue(lv, 'a parameter describes the population; a statistic describes the sample'),
          f'Parameter: {par}; statistic: {stat}', f'The parameter is {par}; the statistic {stat} comes from the sample.', 1, 'Both correct and distinguished.'),
        P('Explain why the researchers used a sample instead of a census.', 'A census would cost too much time or money (or destroy the items tested)',
          'Measuring every individual would be expensive or slow' + (', and testing can use up the items.' if 'tests' in desc or 'weighs' in desc else '.'), 1, 'A practical reason.'),
        P('Would a different random sample give the same statistic? Explain what this means for using the statistic as an estimate.'
          + (' Describe one way to make the estimate less variable.' if lv != 'cp2' else ''),
          'No; statistics vary from sample to sample (sampling variability)' + ('; a larger random sample reduces the variability' if lv != 'cp2' else ''),
          'Different random samples contain different individuals, so the statistic would change; the estimate is not exactly the parameter.' + (' Larger samples give statistics that vary less.' if lv != 'cp2' else ''),
          1, 'Sampling variability explained' + ('; larger sample.' if lv != 'cp2' else '.')),
    ]
    return stem, parts, ['1.2.A', '1.10.B', '3.1.B'], desc[:30]


@frq(2, 2)
def sampling_frq(rng, lv):
    grades = [('freshmen', rng.choice([400, 450, 500])), ('sophomores', rng.choice([380, 420, 460])), ('juniors', rng.choice([350, 400])), ('seniors', rng.choice([330, 370]))]
    N = sum(n for _, n in grades)
    n = rng.choice([80, 100, 120]) if lv != 'cp2' else 100
    raw = [n * k / N for _, k in grades]
    alloc = [int(r) for r in raw]
    for i in sorted(range(4), key=lambda i: raw[i] - alloc[i], reverse=True)[:n - sum(alloc)]:
        alloc[i] += 1
    topic = rng.choice(['how many hours they work per week', 'how they get to school', 'whether they want a later start time', 'how much they spend on lunch'])
    stem = f'A high school has {N:,} students: ' + ', '.join(f'{k} {name}' for name, k in grades) + f'. The principal wants to survey {n} students about {topic}.'
    parts = [
        P(f'Describe how to select a simple random sample of {n} students.' + cue(lv, 'number the students, then use a random number generator'),
          f'Number students 1–{N:,}; use a random number generator to pick {n} different numbers; survey those students',
          f'Get a list of all {N:,} students, label them 1 to {N:,}, generate random integers from 1 to {N:,} ignoring repeats until {n} different labels are chosen, and survey those students.',
          1, 'Labels, random selection without repeats, and how many.'),
        P(f'Describe a stratified random sample of {n} students using grade as the strata, with each grade represented in proportion to its size. How many from each grade?',
          '; '.join(f'{name}: {a}' for (name, _), a in zip(grades, alloc)),
          'Take an SRS within each grade. ' + '; '.join(f'{name}: {n} × {k}/{N:,} ≈ {f(r, 1)}' for (name, k), r in zip(grades, raw)) + '. Rounding so the total is ' + str(n) + ': '
          + ', '.join(f'{a} {name}' for (name, _), a in zip(grades, alloc)) + '.', 1, 'Separate SRS within each grade and correct proportions.'),
        P('Explain one advantage of the stratified sample over the simple random sample here.',
          'If answers differ by grade, stratifying guarantees every grade is represented and gives a more precise estimate',
          f'Students in different grades may answer differently about {topic}; stratifying by grade ensures each grade is represented and reduces variability.',
          1, 'Advantage linked to grades differing.'),
        P('The principal instead randomly selects 4 homerooms and surveys every student in them. Name this method and give one drawback.',
          'Cluster sample; homerooms may not represent the whole school (for example, if homerooms are grouped by grade)',
          'Choosing whole groups at random is cluster sampling. If homerooms are organized by grade, the chosen homerooms might miss some grades, so the estimate could be more variable.',
          1, 'Cluster sample named and a valid drawback.'),
    ]
    return stem, parts, ['1.11.A', '1.11.B'], topic


@frq(2, 3)
def bias_frq(rng, lv):
    org, topic, q, d, why = rng.choice([
        ('the student council', 'extending the school day', '"Wouldn’t you agree that a longer school day would hurt students’ after-school jobs?"', 'underestimate the support for a longer day',
         'The question is leading: it suggests a reason to oppose the plan, so more people will say they oppose it.'),
        ('a city', 'building a new skate park', '"Do you support a modern skate park that keeps kids active and off the streets?"', 'overestimate the support for the park',
         'The question is leading: its wording praises the park, so more people will say they support it.'),
        ('a gym', 'how often adults exercise', '"How many days did you exercise last week?"', 'overestimate how often adults exercise',
         'People like to look healthy, so many will overstate how often they exercise (social desirability).')])
    sent, back = rng.choice([(500, 140), (800, 230), (600, 150)])
    stem = f'{org[0].upper() + org[1:]} wants to learn about {topic} among residents. It mails a survey to {sent} randomly chosen addresses from a list of homeowners, asking {q} Only {back} surveys come back.'
    parts = [
        P('Identify a source of response bias in the question and explain how it would affect the estimate.' + cue(lv, 'look at the wording and at how people like to answer'),
          f'Response bias; the results are likely to {d}', f'{why} The results would {d}.', 1, 'Source of response bias and its direction.'),
        P('Identify a source of undercoverage and explain why it could bias the results.', 'Renters are left out because the list has only homeowners',
          f'Residents who rent are not on the list. If renters differ (for example, they may be younger or have different incomes), their views on {topic} may differ and the results will be biased.',
          1, 'Renters left out with a plausible link to the responses.'),
        P('Calculate the response rate and explain why nonresponse could be a problem.', f'{f(back / sent * 100, 1)}%',
          f'{back}/{sent} = {f(back / sent * 100, 1)}%. People who return the survey may care more about {topic} than those who do not, so the respondents may not represent the population.',
          1, 'Rate and the reason nonresponders may differ.'),
        P('Describe two changes that would reduce the bias.' + (' Explain why a larger sample alone would not fix it.' if lv == 'honors' else ''),
          'Use neutral or anonymous questions; sample from a list of all residents; follow up with nonrespondents' + ('; a larger sample has the same bias' if lv == 'honors' else ''),
          'Ask a neutral question (anonymously), use a sampling frame of all residents (renters included), and follow up with people who do not respond.' + (' Bias is systematic, so a larger sample would repeat it with less variability.' if lv == 'honors' else ''),
          1, 'Two valid changes' + (' and the explanation.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['1.12.A', '1.11.B'], topic


@frq(2, 4)
def obs_exp_frq(rng, lv):
    x, y, better, conf, units = rng.choice([('drinking green tea', 'blood pressure', 'lower blood pressure', 'overall diet and exercise habits', 'adults'),
                                            ('playing a musical instrument', 'math grades', 'higher math grades', 'family income', 'students'),
                                            ('using a standing desk', 'back pain', 'less back pain', 'type of job', 'office workers'),
                                            ('eating breakfast', 'test scores', 'higher test scores', 'amount of sleep', 'students')])
    n = rng.choice([400, 600, 1200])
    stem = f'Researchers survey {n:,} randomly selected {units} and find that those who report {x} tend to have {better} than those who do not.'
    parts = [
        P('Is this an observational study or an experiment? Explain.', 'Observational study, because no treatment was imposed',
          f'The researchers only recorded whether people reported {x}; they did not assign it.', 1, 'Correct type with reason.'),
        P('Identify the explanatory and response variables.', f'Explanatory: {x}; response: {y}', f'{x[0].upper() + x[1:]} may help explain differences in {y}.', 1, 'Both correct.'),
        P(f'Explain how {conf} could be a confounding variable.', f'{conf[0].upper() + conf[1:]} could be related to {x} and also affect {y}',
          f'{units[0].upper() + units[1:]} who report {x} may differ in {conf}, and {conf} could itself affect {y}, so we cannot tell which one explains the difference.',
          1, 'Linked to both variables.'),
        P(f'Outline an experiment that could show whether {x} causes {better}.' + cue(lv, 'random assignment, treatment and control, response') + (' Explain how your design handles the confounding variable.' if lv == 'honors' else ''),
          f'Randomly assign volunteers to {x} or a control group, keep everything else the same, and compare {y}',
          f'Recruit volunteers, randomly assign half to {x} and half to a control condition for several weeks, then compare {y}. Random assignment balances {conf} between the groups.',
          1, 'Random assignment, two groups and the response compared' + ('; balancing of the confounder explained.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['1.10.C', '1.10.D', '1.13.A', '1.13.D'], x


@frq(2, 5)
def experiment_frq(rng, lv):
    from s2fill import FACTORS
    f1, f1s, f2, f2s, units, resp = rng.choice(FACTORS)
    a, b = rng.choice([2, 3]), rng.choice([2, 3])
    reps = rng.choice([5, 6, 8])
    N = a * b * reps
    stem = f'A researcher plans an experiment with {N} {units} to see how the {f1} ({a} levels) and the {f2} ({b} levels) affect the {resp}.'
    parts = [
        P('Identify the experimental units, the factors and the response variable.', f'Units: {units}; factors: {f1} and {f2}; response: {resp}',
          f'Experimental units: the {N} {units}. Factors: {f1} and {f2}. Response: {resp}.', 1, 'All three identified.'),
        P('How many treatments are there? How many units get each treatment?' + cue(lv, 'treatments = levels × levels'), f'{a * b} treatments; {reps} units each',
          f'{a} × {b} = {a * b} treatments; {N}/{a * b} = {reps} units per treatment.', 1, 'Both numbers.'),
        P(f'Describe how to randomly assign the {N} {units} to the treatments.', f'Label 1–{N}, randomly choose {reps} for treatment 1, {reps} of the rest for treatment 2, and so on',
          f'Label the {units} 1 to {N}. Use a random number generator to pick {reps} different labels for the first treatment, then {reps} of the remaining labels for the next, until all treatments are filled.',
          1, 'Labels, random selection without repeats, equal groups.'),
        P('Explain the purpose of replication in this experiment.' + (' Then name one variable you would keep constant and why.' if lv != 'cp2' else ''),
          'Replication (several units per treatment) lets us see whether differences are larger than chance variation' + ('; e.g., keep the location constant to reduce variability' if lv != 'cp2' else ''),
          'With several units per treatment, natural variation among units averages out, so a real treatment effect can be distinguished from chance.' + (' Keeping other conditions the same reduces variability in the response.' if lv != 'cp2' else ''),
          1, 'Purpose of replication' + (' and a controlled variable.' if lv != 'cp2' else '.')),
    ]
    return stem, parts, ['1.13.A', '1.13.B'], f1


@frq(2, 6)
def blinding_frq(rng, lv):
    trt, who, resp = rng.choice([('a new allergy medicine', 'adults with seasonal allergies', 'number of sneezing episodes'), ('a herbal sleep aid', 'adults with insomnia', 'hours of sleep'),
                                 ('a pain-relief cream', 'runners with sore knees', 'pain rating'), ('a memory supplement', 'older adults', 'score on a memory test')])
    n = rng.choice([60, 80, 100])
    stem = f'A company tests {trt}. It recruits {n} {who}, randomly assigns half to the new product and half to an identical-looking placebo, and measures the {resp} after four weeks.'
    parts = [
        P('Why is a placebo group needed?', 'To control for the placebo effect, so any difference can be attributed to the product',
          'Subjects may improve simply because they believe they are treated; the placebo group experiences that too, so only the active ingredient differs.', 1, 'Placebo effect and comparison.'),
        P('Describe what it would mean for this experiment to be double-blind.' + cue(lv, 'think about the subjects and the people who measure the response'),
          'Neither the subjects nor the people measuring the response know who got which treatment',
          'Subjects do not know their group, and the staff who measure and record the response do not know either.', 1, 'Both groups named.'),
        P('Explain why double-blinding matters here.', 'Knowing the treatment could change how subjects report or how staff measure the response',
          f'The {resp} could be influenced by expectations, so knowledge of the treatment could bias the results.', 1, 'Explains how knowledge could bias the response.'),
        P('Suppose instead the subjects chose whether to take the product. Explain why the results could not show cause and effect.',
          'Self-selection: people who choose the product may differ in ways that affect the response (confounding)',
          f'Without random assignment, those who choose {trt} may differ (for example, in how severe their symptoms are), so differences could be due to that variable.',
          1, 'Confounding from self-selection.'),
    ]
    return stem, parts, ['1.13.A', '1.13.C', '1.13.D'], trt


@frq(2, 7)
def design_frq(rng, lv):
    trt, units, block, resp = rng.choice([('two brands of running shoes', 'runners', 'experience level (beginner or experienced)', '5-km time'),
                                          ('two study apps', 'students', 'grade level (juniors or seniors)', 'test score'),
                                          ('two seed varieties', 'garden plots', 'soil type (sandy or clay)', 'yield')])
    n = rng.choice([40, 60, 80])
    stem = f'A researcher wants to compare {trt} using {n} {units}. The {resp} is the response. The researcher thinks {block} may affect the {resp}.'
    parts = [
        P('Describe a completely randomized design for this experiment.', f'Randomly assign {n // 2} {units} to each treatment and compare the mean {resp}',
          f'Label the {n} {units}, randomly select {n // 2} for the first treatment, give the rest the second, and compare the mean {resp}.', 1, 'Random assignment of all units to two equal groups.'),
        P(f'Describe a randomized block design using {block.split(" (")[0]} as blocks.' + cue(lv, 'form the blocks first, then randomize within each block'),
          f'Separate {units} by {block.split(" (")[0]}, then randomly assign treatments within each block',
          f'Split the {units} into blocks by {block.split(" (")[0]}; within each block, randomly assign half to each treatment; compare treatments within blocks.', 1, 'Blocks formed then randomization within blocks.'),
        P('Explain why the block design is likely to be better.', f'It removes variability due to {block.split(" (")[0]}, so treatment differences are easier to detect',
          f'Since {block.split(" (")[0]} affects the {resp}, comparing within blocks removes that source of variation and gives more precise comparisons.', 1, 'Reduced variability explanation.'),
        P('Could a matched pairs design be used? Describe one and say when it would be best.' + (' Explain how to handle order effects.' if lv == 'honors' else ''),
          'Yes: pair similar units (or give each unit both treatments in random order) and compare differences',
          f'Pair {units} that are as similar as possible and randomly assign one of each pair to each treatment (or give each unit both, in random order); best when units vary a lot.'
          + (' Randomizing the order prevents an order effect from favoring one treatment.' if lv == 'honors' else ''), 1, 'Valid matched pairs description' + (' with order effect.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['1.13.B', '1.13.C'], trt


@frq(2, 8)
def scope_frq(rng, lv):
    sel = rng.choice([True, False])
    units = rng.choice(['adults', 'students'])
    pop = 'all adults in a county' if units == 'adults' else 'all students at a large university'
    how = f'randomly selects 200 {units} from {pop}' if sel else f'recruits 200 {units} who answer an advertisement'
    trt, ctl, grp, resp = rng.choice([('a daily 20-minute walk', 'no change in routine', 'walking', 'mood score'), ('a meditation app', 'a podcast app', 'meditation', 'stress score')])
    stem = f'A researcher {how}, then randomly assigns half to {trt} and half to {ctl}. After six weeks, the {grp} group has a significantly better mean {resp}.'
    parts = [
        P('Was there random selection? Was there random assignment?', f'Random selection: {"yes" if sel else "no"}; random assignment: yes',
          f'The {units} were {"chosen at random" if sel else "volunteers"}; the treatments were assigned at random.', 1, 'Both correct.'),
        P(f'Can the researcher conclude that {trt} caused the better {resp}? Justify.', 'Yes, because of random assignment',
          'Random assignment creates comparable groups, so a significant difference can be attributed to the treatment.', 1, 'Yes with random assignment.'),
        P('To what population can the results be generalized? Justify.' + cue(lv, 'random selection is what allows generalizing'),
          f'{pop[0].upper() + pop[1:]}' if sel else f'Only {units} like those who volunteered',
          f'Because the {units} were randomly selected from {pop}, the results generalize to it.' if sel else f'Volunteers were not randomly selected, so the results apply only to {units} like these volunteers.',
          1, 'Correct scope with reason.'),
        P('Explain what "significantly better" means in this context.' + (' What would change about your answers if the participants had chosen their own treatment?' if lv == 'honors' else ''),
          'The difference is larger than would be likely from random assignment alone if the treatment had no effect' + ('; then no cause-and-effect conclusion' if lv == 'honors' else ''),
          'A difference this large would rarely occur by chance (from the random assignment) if the treatment had no effect.' + (' Without random assignment, confounding could explain the difference.' if lv == 'honors' else ''),
          1, 'Chance-variation explanation' + (' and the self-selection point.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['1.10.E', '1.13.D'], how


@frq(3, 1)
def lln_frq(rng, lv):
    p = rng.choice([0.7, 0.75, 0.8, 0.65])
    name = rng.choice(['Maya', 'Jordan', 'Sam', 'Priya'])
    n1 = rng.choice([20, 25])
    made = round(n1 * p) - rng.choice([2, 3])
    stem = f'{name} makes {pct(p)} of free throws in the long run. In one practice, {name} shoots {n1} free throws and makes {made}.'
    parts = [
        P('Find the relative frequency of made shots in this practice.', g(round(made / n1, 4)), f'{made}/{n1} = {g(round(made / n1, 4))}.', 1, 'Correct value.'),
        P(f'Does this practice show that {name}’s true rate has dropped below {g(p)}? Explain.', 'No: short runs vary a lot; the long-run rate is about the many-trial proportion',
          f'With only {n1} shots, the proportion can easily differ from {g(p)} by chance; the long-run rate describes many shots.', 1, 'Short-run variability.'),
        P(f'About how many of the next 200 free throws would you expect {name} to make?' + cue(lv, 'expected count = n × p'), g(200 * p), f'200 × {g(p)} = {g(200 * p)}.', 1, 'Correct expected count.'),
        P(f'After missing 3 in a row, {name} says, "I’m due to make the next one." Is this reasoning correct? Explain using the law of large numbers.',
          'No: shots are independent; the probability is still about ' + g(p) + '; the law of large numbers is about the long run, not correcting short runs',
          f'Each shot still has probability about {g(p)}. The law of large numbers says the proportion approaches {g(p)} over many shots because the early results are swamped, not because misses are made up.',
          1, 'Rejects the "due" reasoning with independence and the long-run meaning.'),
    ]
    return stem, parts, ['2.3.A'], name


@frq(3, 2)
def rules_frq(rng, lv):
    a_n, b_n = rng.choice([('plays a sport', 'is in the band'), ('has a part-time job', 'takes an AP class'), ('owns a dog', 'owns a cat')])
    pa, pb = rng.choice([(0.45, 0.30), (0.40, 0.35), (0.52, 0.28)])
    pab = rng.choice([0.12, 0.135, 0.10])
    stem = f'For a randomly chosen student at a large school, let A = the student {a_n} and B = the student {b_n}. P(A) = {g(pa)}, P(B) = {g(pb)}, P(A and B) = {g(pab)}.'
    union = pa + pb - pab
    indep = abs(pa * pb - pab) < 1e-9
    parts = [
        P('Find P(A or B).' + cue(lv, 'P(A or B) = P(A) + P(B) − P(A and B)'), g(round(union, 4)), f'{g(pa)} + {g(pb)} − {g(pab)} = {g(round(union, 4))}.', 1, 'Correct.'),
        P('Find the probability that the student does neither.', g(round(1 - union, 4)), f'1 − {g(round(union, 4))} = {g(round(1 - union, 4))}.', 1, 'Complement used.'),
        P('Are A and B mutually exclusive? Justify.', 'No, because P(A and B) is not 0', f'P(A and B) = {g(pab)} ≠ 0, so a student can be in both.', 1, 'Correct with the joint probability.'),
        P('Are A and B independent? Justify.' + (' Then find P(B | A).' if lv == 'honors' else ''),
          ('Yes' if indep else 'No') + f': P(A)P(B) = {g(round(pa * pb, 4))}' + (' = ' if indep else ' ≠ ') + f'P(A and B) = {g(pab)}' + (f'; P(B | A) ≈ {f(pab / pa, 4)}' if lv == 'honors' else ''),
          f'Independent events satisfy P(A and B) = P(A)P(B). {g(pa)} × {g(pb)} = {g(round(pa * pb, 4))}, ' + ('which equals' if indep else 'which is not equal to') + f' {g(pab)}.'
          + (f' P(B | A) = {g(pab)}/{g(pa)} ≈ {f(pab / pa, 4)}.' if lv == 'honors' else ''), 1, 'Correct check' + (' and the conditional probability.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['2.7.A', '2.4.A', '2.5.A'], a_n


@frq(3, 3)
def conditional_frq(rng, lv):
    test, units, cond, has = rng.choice([('a screening test', 'patients', 'have the condition', 'has the condition'), ('a spam filter', 'emails', 'are spam', 'is spam'),
                                         ('an airport metal detector', 'travelers', 'carry metal', 'carries metal')])
    prev = rng.choice([0.02, 0.05, 0.1])
    sens, spec = rng.choice([(0.95, 0.90), (0.9, 0.95), (0.98, 0.92)])
    N = 10000
    pos_true = round(prev * N * sens)
    neg_grp = round((1 - prev) * N)
    pos_false = round(neg_grp * (1 - spec))
    ppos = (pos_true + pos_false) / N
    ppv = pos_true / (pos_true + pos_false)
    stem = (f'Of the {units} checked by {test}, {pct(prev)} {cond}. It flags {pct(sens)} of the {units} that {cond} and correctly clears {pct(spec)} of those that do not. '
            f'Imagine {N:,} {units}.')
    parts = [
        P(f'How many of the {N:,} {units} {cond} and are flagged?' + cue(lv, f'{N:,} × {g(prev)} × {g(sens)}'), str(pos_true),
          f'{N:,} × {g(prev)} = {round(prev * N):,} {cond}; {g(sens)} of them are flagged: {pos_true:,}.', 1, 'Correct count.'),
        P(f'Find the probability that a randomly chosen one of these {units} is flagged.', g(round(ppos, 4)),
          f'False alarms: {neg_grp:,} × {g(round(1 - spec, 2))} = {pos_false:,}. P(flagged) = ({pos_true:,} + {pos_false:,})/{N:,} = {g(round(ppos, 4))}.', 1, 'Both true and false alarms used.'),
        P(f'Given that one of the {units} is flagged, find the probability that it {has}. Round to four decimal places.', f(ppv, 4),
          f'P({has.split(" ", 1)[1]} | flagged) = {pos_true:,}/{pos_true + pos_false:,} ≈ {f(ppv, 4)}.', 1, 'Correct conditional probability.'),
        P('Explain why this probability is much lower than the accuracy of the test suggests.', f'Only {pct(prev)} {cond}, so false alarms from the large group that does not outnumber or rival the true alarms',
          f'Only {pct(prev)} {cond}; even a small false-alarm rate applied to the much larger group that does not produces many false alarms.', 1, 'Base-rate explanation.'),
    ]
    return stem, parts, ['2.6.A'], test


@frq(3, 4)
def simulation_frq(rng, lv):
    p, ev, k, n = rng.choice([(0.2, 'a cereal box contains a prize', 2, 5), (0.3, 'a customer buys a dessert', 3, 6), (0.4, 'a player wins a round', 3, 5)])
    trials = 40
    hits = round(trials * (1 - stats.binom.cdf(k - 1, n, p))) + rng.choice([-2, 1, 2])
    stem = f'The probability that {ev} is {g(p)}. We want to estimate the probability that at least {k} of the next {n} trials are successes.'
    d = round(p * 10)
    parts = [
        P('Describe how to use random digits 0–9 to simulate one trial.' + cue(lv, 'assign digits so the success probability is right'),
          f'Digits 0–{d - 1} = success; {d}–9 = failure', f'{d} of the 10 digits gives probability {d}/10 = {g(p)}: let 0–{d - 1} be a success.', 1, 'Correct assignment.'),
        P(f'Describe how to carry out one repetition of the simulation and what to record.', f'Read {n} digits; count successes; record whether the count is at least {k}',
          f'Take {n} random digits (repeats allowed), count how many are 0–{d - 1}, and record whether there were at least {k}.', 1, 'Trial length and what to record.'),
        P(f'In {trials} repetitions, {hits} had at least {k} successes. Estimate the probability.', g(round(hits / trials, 3)), f'{hits}/{trials} = {g(round(hits / trials, 3))}.', 1, 'Correct estimate.'),
        P('How could you make the estimate more reliable? Explain.' + (f' Compare it with the exact binomial probability.' if lv == 'honors' else ''),
          'Run many more repetitions; by the law of large numbers the estimate gets closer to the true probability' + (f'; exact ≈ {f(1 - stats.binom.cdf(k - 1, n, p), 4)}' if lv == 'honors' else ''),
          'More repetitions reduce the variability of the estimate.' + (f' Exact: P(X ≥ {k}) for Binomial({n}, {g(p)}) ≈ {f(1 - stats.binom.cdf(k - 1, n, p), 4)}.' if lv == 'honors' else ''),
          1, 'More repetitions with reason' + (' and the exact value.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['2.3.A', '2.10.D'], ev


@frq(3, 5)
def discrete_frq(rng, lv):
    name, subj, xs, ps = rng.choice([('number of pets', 'a randomly chosen household', [0, 1, 2, 3, 4], [0.28, 0.35, 0.22, 0.10, 0.05]),
                                     ('number of cars owned', 'a randomly chosen family', [0, 1, 2, 3], [0.08, 0.34, 0.41, 0.17]),
                                     ('number of AP classes taken', 'a randomly chosen senior', [0, 1, 2, 3, 4], [0.30, 0.20, 0.25, 0.15, 0.10])])
    i = rng.randrange(1, len(xs))
    k = ps[i]
    shown = ', '.join(f'P(X = {x}) = {"k" if j == i else g(p)}' for j, (x, p) in enumerate(zip(xs, ps)))
    mu = sum(x * p for x, p in zip(xs, ps))
    sd = math.sqrt(sum((x - mu) ** 2 * p for x, p in zip(xs, ps)))
    ge2 = sum(p for x, p in zip(xs, ps) if x >= 2)
    stem = f'Let X = the {name} for {subj}. {shown}.'
    parts = [
        P('Find k.' + cue(lv, 'the probabilities add to 1'), g(k), f'k = 1 − (sum of the others) = {g(k)}.', 1, 'Correct k.'),
        P('Find P(X ≥ 2).', g(round(ge2, 4)), 'Add the probabilities for X = 2 and above: ' + ' + '.join(g(p) for x, p in zip(xs, ps) if x >= 2) + f' = {g(round(ge2, 4))}.', 1, 'Correct.'),
        P('Find the mean of X.', g(round(mu, 4)), 'E(X) = Σ x·P(x) = ' + ' + '.join(f'{x}({g(p)})' for x, p in zip(xs, ps)) + f' = {g(round(mu, 4))}.', 1, 'Correct mean.'),
        P('Interpret the mean in context.' + (f' Is X = {xs[-1]} unusual? Justify with the standard deviation.' if lv == 'honors' else ''),
          f'Over many randomly chosen cases, the average {name} is about {g(round(mu, 2))}' + (f'; X = {xs[-1]} is about {f((xs[-1] - mu) / sd, 2)} SDs above the mean' if lv == 'honors' else ''),
          f'If we chose many at random, the average {name} would be about {g(round(mu, 2))} (the mean need not be a possible value).'
          + (f' SD ≈ {f(sd, 3)}, so X = {xs[-1]} is about {f((xs[-1] - mu) / sd, 2)} SDs above the mean: uncommon (probability {g(ps[-1])}) but not extreme.' if lv == 'honors' else ''),
          1, 'Long-run average interpretation' + (' and the SD comparison.' if lv == 'honors' else '.')),
    ]
    return stem, parts, ['2.8.A', '2.9.A', '2.9.B'], name


@frq(3, 6)
def ev_sd_frq(rng, lv):
    cost = rng.choice([5, 10])
    prizes = rng.choice([[(100, 0.01), (20, 0.05), (5, 0.2)], [(50, 0.02), (10, 0.1), (2, 0.3)]])
    vals = [v for v, _ in prizes] + [0]
    probs = [p for _, p in prizes] + [round(1 - sum(p for _, p in prizes), 4)]
    mu = sum(v * p for v, p in zip(vals, probs))
    sd = math.sqrt(sum((v - mu) ** 2 * p for v, p in zip(vals, probs)))
    stem = f'A fundraiser game costs ${cost} to play. Prizes: ' + ', '.join(f'${v} with probability {g(p)}' for v, p in prizes) + f', otherwise $0. Let W = the prize won.'
    loss = round(cost - mu, 4)
    parts = [
        P('Find E(W), in dollars.' + cue(lv, 'Σ w·P(w)'), g(round(mu, 4)), ' + '.join(f'{v}({g(p)})' for v, p in zip(vals, probs)) + f' = {g(round(mu, 4))}.', 1, 'Correct.'),
        P('Find the standard deviation of W. Round to two decimal places.', f(sd, 2), f'Var(W) = Σ (w − μ)² P(w) ≈ {f(sd * sd, 3)}; SD ≈ {f(sd, 2)}.', 1, 'Correct.'),
        P(f'Let N = W − {cost}, the player’s net gain. Find the mean and standard deviation of N.', f'Mean {g(round(mu - cost, 4))}; SD {f(sd, 2)}',
          f'Subtracting a constant shifts the mean: {g(round(mu, 4))} − {cost} = {g(round(mu - cost, 4))}; the SD is unchanged, {f(sd, 2)}.', 1, 'Both, with the SD unchanged.'),
        P('Should the school expect to make money from this game? Justify.' + (' Estimate the school’s profit from 500 plays.' if lv != 'cp2' else ''),
          ('Yes' if mu < cost else 'No') + f': players lose {money(loss)} per play on average' + (f'; about {money(500 * loss)}' if lv != 'cp2' else ''),
          f'E(N) = {g(round(mu - cost, 4))}, so in the long run the school gains about {money(loss)} per play.' + (f' 500 × {money(loss)} = {money(500 * loss)}.' if lv != 'cp2' else ''),
          1, 'Decision from E(N)' + (' and the estimate.' if lv != 'cp2' else '.')),
    ]
    return stem, parts, ['2.9.A', '2.9.B', 'BEYOND.LINRV'], str(cost)


@frq(3, 7)
def binomial_frq(rng, lv):
    who, prop, p = rng.choice(PROP)
    p = round(p, 2)
    n = {'cp2': 10, 'cp1': 15, 'honors': 20}[lv]
    k = round(n * p)
    pk = stats.binom.pmf(k, n, p)
    mu, sd = n * p, math.sqrt(n * p * (1 - p))
    geo = (1 - p) ** 2 * p
    hi = min(n, k + round(2 * sd) + 1)
    ph = 1 - stats.binom.cdf(hi - 1, n, p)
    stem = f'About {pct(p)} of {who} {prop}. A random sample of {n} is selected. Let X = the number in the sample who {prop}.'
    d = (P(f'Now they are chosen one at a time. Find the probability that the first two chosen do not {prop} and the third does (a geometric setting; beyond the 2026 AP course). Round to four decimal places.',
           f(geo, 4), f'P = (1 − p)(1 − p)p = ({g(round(1 - p, 2))})²({g(p)}) ≈ {f(geo, 4)}.', 1, 'Correct product of independent probabilities.') if lv != 'cp2' else
         P(f'Would it be unusual to get X ≥ {hi}? Justify with a probability.', ('Yes' if ph < 0.05 else 'No') + f': P(X ≥ {hi}) ≈ {f(ph, 4)}',
           f'P(X ≥ {hi}) = 1 − binomcdf({n}, {g(p)}, {hi - 1}) ≈ {f(ph, 4)}; ' + ('this is below 0.05, so it would be unusual.' if ph < 0.05 else 'this is not small, so it would not be unusual.'),
           1, 'Correct probability with a judgment.'))
    parts = [
        P('Explain why X is a binomial random variable.' + cue(lv, 'check: two outcomes, independent trials, fixed n, same p'),
          f'Two outcomes (yes/no), independent trials (sample < 10% of a large population), fixed n = {n}, same p = {g(p)}',
          f'Each one either does or does not; trials are independent because {n} is less than 10% of the population; n = {n} is fixed; p = {g(p)} for each.', 1, 'All four conditions.'),
        P(f'Find P(X = {k}). Round to four decimal places.', f(pk, 4), f'C({n}, {k})({g(p)}){sup(k)}({g(round(1 - p, 2))}){sup(n - k)} ≈ {f(pk, 4)}.', 1, 'Correct probability.'),
        P('Find the mean and standard deviation of X.', f'Mean {g(round(mu, 2))}; SD {f(sd, 3)}', f'μ = np = {g(round(mu, 2))}; σ = √(np(1 − p)) ≈ {f(sd, 3)}.', 1, 'Both correct.'),
        d,
    ]
    return stem, parts, ['2.10.A', '2.10.E', '2.10.B'] + (['BEYOND.GEOM'] if lv != 'cp2' else []), who


@frq(3, 8)
def combine_frq(rng, lv):
    m1, s1, m2, s2, x_desc, y_desc, t_desc, u, plus = rng.choice([
        (28, 4, 12, 3, 'X = the time to drive to the airport', 'Y = the time to get through security', 'T = X + Y, the total time', 'minutes', True),
        (350, 20, 50, 8, 'X = the weight of a full box of cereal', 'Y = the weight of the empty box', 'T = X − Y, the weight of the cereal', 'grams', False),
        (12, 1.5, 9, 1.2, 'X = the time to make a pizza', 'Y = the time to bake it', 'T = X + Y, the total time', 'minutes', True)])
    mean = m1 + m2 if plus else m1 - m2
    sd = math.sqrt(s1 ** 2 + s2 ** 2)
    lim = round(mean + 1.2 * sd)
    z = (lim - mean) / sd
    pr = round(1 - table_a(z), 4)
    op = '+' if plus else '−'
    stem = (f'{x_desc} is Normal with mean {g(m1)} and SD {g(s1)} {u}; {y_desc} is Normal with mean {g(m2)} and SD {g(s2)} {u}. X and Y are independent. '
            f'Let {t_desc}. (Beyond AP topic: combining random variables.)')
    parts = [
        P('Find the mean of T.' + cue(lv, 'means add or subtract'), g(mean), f'{g(m1)} {op} {g(m2)} = {g(mean)} {u}.', 1, 'Correct.'),
        P('Find the standard deviation of T. Round to three decimal places.', f(sd, 3), f'Var(T) = {g(s1)}² + {g(s2)}² = {g(s1 ** 2 + s2 ** 2)}; SD ≈ {f(sd, 3)}.', 1, 'Variances added.'),
        P(f'Find P(T > {lim}). Use Table A (round z to two decimal places). Round to four decimal places.', f(pr, 4),
          f'T is Normal (a combination of independent Normals). z = ({lim} − {g(mean)})/{f(sd, 3)} ≈ {f(z, 2)}; P = 1 − {f(table_a(z), 4)} = {f(pr, 4)}.', 1, 'Normal model, z and area.'),
        P('Explain why the variances add even though T is a difference.' if not plus else 'Explain why you cannot simply add the standard deviations.',
          'Variability from each independent source adds; subtracting does not cancel spread' if not plus else 'Only variances add for independent variables; SDs do not',
          'Var(X − Y) = Var(X) + Var(Y): the uncertainty in each part contributes, whichever way they are combined.' if not plus else f'√({g(s1)}² + {g(s2)}²) ≈ {f(sd, 3)}, which is less than {g(s1)} + {g(s2)} = {g(s1 + s2)}; the SD is the square root of the summed variances.',
          1, 'Correct reason.'),
    ]
    return stem, parts, ['BEYOND.COMB'], x_desc


@frq(3, 9)
def sampling_dist_frq(rng, lv):
    who, prop, p = rng.choice(PROP)
    p = round(p, 2)
    n = rng.choice([100, 150, 200, 250])
    sd = math.sqrt(p * (1 - p) / n)
    v = round(p + rng.choice([0.05, 0.06, -0.05]), 2)
    z = (v - p) / sd
    pr = round(1 - table_a(z), 4) if v > p else table_a(z)
    word = 'greater' if v > p else 'less'
    stem = f'Suppose {pct(p)} of {who} {prop}. Let p̂ be the proportion who do in a random sample of {n}.'
    parts = [
        P('Find the mean and standard deviation of the sampling distribution of p̂.' + cue(lv, 'μ = p; σ = √(p(1 − p)/n)'), f'Mean {g(p)}; SD {f(sd, 4)}',
          f'μ_p̂ = {g(p)}; σ_p̂ = √({g(p)}({g(round(1 - p, 2))})/{n}) ≈ {f(sd, 4)}.', 1, 'Both correct.'),
        P('Justify that the sampling distribution is approximately Normal.', f'np = {g(n * p)} and n(1 − p) = {g(round(n * (1 - p), 2))} are both at least 10',
          f'Large Counts: {n}({g(p)}) = {g(n * p)} ≥ 10 and {n}({g(round(1 - p, 2))}) = {g(round(n * (1 - p), 2))} ≥ 10.', 1, 'Both counts.'),
        P(f'Find P(p̂ {">" if v > p else "<"} {g(v)}). Use Table A (round z to two decimal places). Round to four decimal places.', f(pr, 4),
          f'z = ({g(v)} − {g(p)})/{f(sd, 4)} ≈ {f(z, 2)}; P = {f(pr, 4)}.', 1, 'z and area.'),
        P(f'A random sample of {n} gives p̂ = {g(v)}. Would this be convincing evidence that the true proportion is {word} than {g(p)}? Justify using part (c).',
          ('Yes' if pr < 0.05 else 'No') + f': if p = {g(p)}, a result this extreme has probability {f(pr, 4)}',
          f'If p = {g(p)}, a sample proportion this far {"above" if v > p else "below"} it happens with probability {f(pr, 4)}, ' + ('which is small (below 0.05), so it would be convincing evidence.' if pr < 0.05 else 'which is not small, so it would not be convincing.'),
          1, 'Decision linked to the probability.'),
    ]
    return stem, parts, ['3.2.A', '3.2.B', '3.2.C'], who


@frq(3, 10)
def clt_frq(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = rng.choice([36, 40, 50, 64])
    se = sd / math.sqrt(n)
    v = round(mu + 1.4 * se, max(dp, 1) + 1)
    z = (v - mu) / se
    pr = round(1 - table_a(z), 4)
    stem = f'The {var} is strongly skewed to the right with mean {g(mu)} and SD {g(sd)} {unit}. A random sample of {n} {pop} is selected.'
    parts = [
        P('Find the mean and standard deviation of the sampling distribution of x̄.' + cue(lv, 'σ_x̄ = σ/√n'), f'Mean {g(mu)}; SD {f(se, 4)}', f'μ_x̄ = {g(mu)}; σ_x̄ = {g(sd)}/√{n} ≈ {f(se, 4)}.', 1, 'Both.'),
        P('Describe the shape of the sampling distribution of x̄. Justify.', f'Approximately Normal by the central limit theorem, since n = {n} ≥ 30',
          f'Even though the population is skewed, n = {n} ≥ 30, so the CLT says x̄ is approximately Normal.', 1, 'Normal with CLT and n.'),
        P(f'Find P(x̄ > {g(v)}). Use Table A (round z to two decimal places). Round to four decimal places.', f(pr, 4), f'z = ({g(v)} − {g(mu)})/{f(se, 4)} ≈ {f(z, 2)}; P = {f(pr, 4)}.', 1, 'Correct.'),
        P(f'How would the standard deviation of x̄ change if the sample size were {4 * n}? Explain.' + (' Would P(x̄ > ' + g(v) + ') increase or decrease?' if lv == 'honors' else ''),
          f'It would be halved, to {f(se / 2, 4)}' + ('; the probability would decrease' if lv == 'honors' else ''),
          f'σ_x̄ = σ/√n; 4 times the sample size divides it by √4 = 2: {f(se / 2, 4)}.' + (' A narrower distribution puts less area beyond the same value above the mean.' if lv == 'honors' else ''),
          1, 'Halved with reason.'),
    ]
    return stem, parts, ['4.1.A', '4.1.B', '4.1.C'], var


# ====================================================================== Unit 4
def four_step_note(lv):
    return ' Use the four steps: State, Plan, Do, Conclude.' if lv != 'cp2' else ''


@frq(4, 1)
def ci_basics_frq(rng, lv):
    who, prop, p = rng.choice(PROP)
    n = rng.choice([400, 500, 600])
    ph = round(p + 0.02, 2)
    c = 0.95
    se = math.sqrt(ph * (1 - ph) / n)
    me = 1.96 * se
    lo, hi = round(ph - me, 3), round(ph + me, 3)
    claim = round(ph - me - 0.02, 2)
    stem = f'A 95% confidence interval for the proportion of {who} {wt(who)} {prop}, from a random sample of {n}, is ({f(lo, 3)}, {f(hi, 3)}).'
    parts = [
        P('Find the point estimate and the margin of error.' + cue(lv, 'midpoint and half-width'), f'p̂ = {f((lo + hi) / 2, 3)}; ME = {f((hi - lo) / 2, 3)}',
          f'p̂ = ({f(lo, 3)} + {f(hi, 3)})/2 = {f((lo + hi) / 2, 3)}; ME = ({f(hi, 3)} − {f(lo, 3)})/2 = {f((hi - lo) / 2, 3)}.', 1, 'Both.'),
        P('Find the standard error of p̂. Round to four decimal places.', f(se, 4), f'SE = ME/z* = {f((hi - lo) / 2, 3)}/1.96 ≈ {f(se, 4)} (or √(p̂(1 − p̂)/n)).', 1, 'Correct.'),
        P('Interpret the interval in context.', f'We are 95% confident that the interval from {f(lo, 3)} to {f(hi, 3)} captures the true proportion of {who} {wt(who)} {prop}',
          f'We are 95% confident that the interval from {f(lo, 3)} to {f(hi, 3)} captures the proportion of all {who} {wt(who)} {prop}.', 1, 'Confidence, parameter, context.'),
        P(f'A news report claims that only {g(claim)} of {who} {prop}. Does the interval support this claim? Justify.', f'No: {g(claim)} is below the interval, so it is not a plausible value',
          f'All plausible values in the interval are above {g(claim)}, so the claim is not supported.', 1, 'Decision based on whether the value is in the interval.'),
    ]
    return stem, parts, ['3.3.D', '3.4.A', '3.4.B'], who


@frq(4, 2)
def conf_level_frq(rng, lv):
    who, prop, p = rng.choice(PROP)
    n = rng.choice([80, 120, 300])
    x = round(n * p) + 2
    N = rng.choice(['3,000', '12,000', '50,000'])
    stem = f'A random sample of {n} from {N} {who} finds {x} who {prop}. A researcher builds a 90% confidence interval for the proportion.'
    ok = x >= 10 and n - x >= 10
    parts = [
        P('Check the conditions for the interval.' + cue(lv, 'random, 10% and Large Counts'), f'Random sample; {n} < 10% of {N}; {x} and {n - x} are both ≥ 10' if ok else 'Large Counts fails',
          f'Random: stated. 10%: {n} is less than 10% of {N}. Large Counts: {x} successes and {n - x} failures, both at least 10.', 1, 'All three conditions.'),
        P('Explain what "90% confidence" means in this context.', f'If we took many random samples of {n} and built an interval from each, about 90% would capture the true proportion',
          'The confidence level describes the method: about 90% of intervals made this way capture the parameter.', 1, 'Capture rate of the method.'),
        P('How would a 99% interval from the same data compare? Explain.', 'Wider, because it needs a larger critical value (z* = 2.576 vs 1.645)',
          'Higher confidence requires a larger z*, so the margin of error and the width increase.', 1, 'Wider with z*.'),
        P('A student says "there is a 90% probability that the true proportion is in our interval." Explain why this is not correct.' + (' Then give a correct statement.' if lv != 'cp2' else ''),
          'Once computed, the interval either captures p or it does not; the 90% refers to the method',
          'The parameter is fixed, so a specific interval contains it or not. The 90% is the long-run capture rate of the procedure.', 1, 'Method vs single interval.'),
    ]
    return stem, parts, ['3.3.B', '3.4.A', '3.4.C'], who


@frq(4, 3)
def one_prop_interval_frq(rng, lv):
    who, prop, p = rng.choice(PROP)
    n = rng.choice([250, 300, 400, 500])
    x = round(n * p) + rng.choice([-4, 3, 6])
    c = {'cp2': 0.95, 'cp1': rng.choice([0.90, 0.95]), 'honors': rng.choice([0.90, 0.99])}[lv]
    zs = ZSTAR[c]
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    lo, hi = ph - zs * se, ph + zs * se
    stem = f'In a random sample of {n} {who}, {x} {prop}. Construct and interpret a {round(c * 100)}% confidence interval for the proportion of all {who} {wt(who)} {prop}.' + four_step_note(lv)
    parts = [
        P('State: identify the parameter and the confidence level.', f'p = the proportion of all {who} {wt(who)} {prop}; {round(c * 100)}% confidence',
          f'p = the true proportion of all {who} {wt(who)} {prop}; confidence level {round(c * 100)}%.', 1, 'Parameter in context.'),
        P('Plan: name the procedure and check the conditions.' + cue(lv, 'random; 10%; at least 10 successes and failures'), f'One-sample z interval for p; random; n < 10% of the population; {x} and {n - x} ≥ 10',
          f'One-sample z interval for a proportion. Random sample; {n} is less than 10% of all {who}; {x} successes and {n - x} failures are both at least 10.', 2, '1 point for the procedure; 1 point for all conditions.'),
        P('Do: compute the interval. Round the endpoints to three decimal places.', f'({f(lo, 3)}, {f(hi, 3)})',
          f'p̂ = {x}/{n} = {g(round(ph, 4))}; SE ≈ {f(se, 4)}; z* = {zs}. {g(round(ph, 4))} ± {zs}({f(se, 4)}) = ({f(lo, 3)}, {f(hi, 3)}).', 2, '1 point for p̂, SE and z*; 1 point for the interval.'),
        P('Conclude: interpret the interval in context.' + (' Does it give convincing evidence that more than half do? Justify.' if lv == 'honors' else ''),
          f'We are {round(c * 100)}% confident the interval from {f(lo, 3)} to {f(hi, 3)} captures the proportion of all {who} {wt(who)} {prop}'
          + ('' if lv != 'honors' else ('; yes, every value is above 0.5' if lo > 0.5 else '; no, values at or below 0.5 are plausible')),
          f'We are {round(c * 100)}% confident that the interval from {f(lo, 3)} to {f(hi, 3)} captures the true proportion.' + ('' if lv != 'honors' else (' All plausible values exceed 0.5.' if lo > 0.5 else ' 0.5 or less is plausible.')),
          1, 'Interpretation in context.'),
    ]
    return stem, parts, ['3.3.A', '3.3.B', '3.3.C', '3.4.A'], who


@frq(4, 4)
def t_interval_frq(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = {'cp2': 25, 'cp1': rng.choice([15, 20]), 'honors': rng.choice([12, 16])}[lv]
    d = max(dp, 1)
    xb = round(mu + 0.15 * sd, d)
    s = round(sd, d + 1)
    c = 0.95 if lv != 'honors' else 0.90
    ts = tstar(c, n - 1)
    se = s / math.sqrt(n)
    lo, hi = xb - ts * se, xb + ts * se
    stem = (f'A random sample of {n} {pop} has mean {g(xb)} {unit} and SD {g(s)} {unit} for the {var}. A dot plot of the sample shows no strong skew or outliers. '
            f'Construct and interpret a {round(c * 100)}% confidence interval for the mean.' + four_step_note(lv))
    parts = [
        P('State: identify the parameter.', f'μ = the mean {var} for all {pop}', f'μ = the true mean {var} of all {pop}; {round(c * 100)}% confidence.', 1, 'Parameter in context.'),
        P('Plan: name the procedure and check the conditions.' + cue(lv, 'random; 10%; Normal/large sample'), 'One-sample t interval; random; 10%; no strong skew or outliers with n < 30',
          f'One-sample t interval for μ. Random sample; {n} is less than 10% of all {pop}; n = {n} < 30, but the sample shows no strong skew or outliers.', 2, '1 point procedure; 1 point conditions.'),
        P('Do: compute the interval. Round the endpoints to two decimal places.', f'({f(lo, 2)}, {f(hi, 2)})',
          f'df = {n - 1}; t* = {f(ts, 3)}; SE = {g(s)}/√{n} ≈ {f(se, 4)}. {g(xb)} ± {f(ts, 3)}({f(se, 4)}) = ({f(lo, 2)}, {f(hi, 2)}).', 2, '1 point for df/t*/SE; 1 point for the interval.'),
        P('Conclude: interpret the interval in context.', f'We are {round(c * 100)}% confident the interval from {f(lo, 2)} to {f(hi, 2)} {unit} captures the mean {var} of all {pop}',
          f'We are {round(c * 100)}% confident that the interval from {f(lo, 2)} to {f(hi, 2)} {unit} captures μ.', 1, 'Interpretation in context.'),
    ]
    return stem, parts, ['4.2.B', '4.2.C', '4.2.D', '4.3.A'], var


@frq(4, 5)
def hypotheses_frq(rng, lv):
    who, prop, p0 = rng.choice(PROP)
    p0 = round(p0, 2)
    pv = rng.choice([0.012, 0.034, 0.081, 0.21])
    stem = f'Records from last year show that {pct(p0)} of {who} {prop}. A researcher believes the proportion has increased this year and plans a significance test using a random sample.'
    parts = [
        P('Define the parameter and state the hypotheses.' + cue(lv, 'hypotheses are about p, not p̂'), f'p = proportion of all {who} {wt(who)} {prop} this year; H₀: p = {g(p0)}; Hₐ: p > {g(p0)}',
          f'p = the true proportion this year. H₀: p = {g(p0)}; Hₐ: p > {g(p0)}.', 1, 'Parameter and both hypotheses.'),
        P('Explain why the alternative hypothesis is one-sided.', 'The researcher suspects an increase, stated before seeing the data',
          'The research question is about an increase only, so Hₐ uses >.', 1, 'Reason tied to the question.'),
        P(f'The test gives a p-value of {g(pv)}. Interpret this p-value in context.', f'If p = {g(p0)}, the probability of a sample proportion at least as large as the one observed is {g(pv)}',
          f'Assuming the true proportion is still {g(p0)}, there is a {g(pv)} probability of getting a sample proportion as large as or larger than the observed one by chance.', 1, 'Assumes H₀, "at least as extreme", context.'),
        P('What conclusion should the researcher make at α = 0.05? Justify.' + (' Which type of error could the researcher have made?' if lv != 'cp2' else ''),
          ('Reject H₀: convincing evidence of an increase' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence of an increase')
          + ('' if lv == 'cp2' else ('; Type I error possible' if pv < 0.05 else '; Type II error possible')),
          f'{g(pv)} {"<" if pv < 0.05 else ">"} 0.05, so ' + ('reject H₀.' if pv < 0.05 else 'fail to reject H₀.') + ('' if lv == 'cp2' else (' Rejecting a true H₀ would be a Type I error.' if pv < 0.05 else ' Failing to reject a false H₀ would be a Type II error.')),
          1, 'Comparison with α and conclusion in context.'),
    ]
    return stem, parts, ['3.5.B', '3.6.A', '3.7.B'], who


@frq(4, 6)
def pvalue_frq(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = rng.choice([20, 25, 30])
    d = max(dp, 1)
    xb = round(mu - 0.5 * sd, d)
    s = round(sd, d + 1)
    t = (xb - mu) / (s / math.sqrt(n))
    pv = stats.t.cdf(t, n - 1)
    stem = f'A company claims the mean {var} is {g(mu)} {unit}. A random sample of {n} {pop} gives x̄ = {g(xb)} and s = {g(s)}. Test H₀: μ = {g(mu)} against Hₐ: μ < {g(mu)}.'
    parts = [
        P('Calculate the test statistic.' + cue(lv, 't = (x̄ − μ₀)/(s/√n)'), f(t, 2), f't = ({g(xb)} − {g(mu)})/({g(s)}/√{n}) ≈ {f(t, 2)}, df = {n - 1}.', 1, 'Correct t.'),
        P('Find the p-value. Use technology. Round to four decimal places.', f(pv, 4), f'P(t < {f(t, 2)}) with df = {n - 1} ≈ {f(pv, 4)}.', 1, 'Correct p-value.'),
        P('Interpret the p-value in context.', f'If the mean were {g(mu)}, the probability of a sample mean of {g(xb)} or lower is {f(pv, 4)}',
          f'Assuming μ = {g(mu)}, there is a {f(pv, 4)} probability of getting x̄ ≤ {g(xb)} by chance in a random sample of {n}.', 1, 'Assumes H₀, direction, context.'),
        P('Is there convincing evidence against the claim at α = 0.05? Justify.', ('Yes' if pv < 0.05 else 'No') + f': p-value {"<" if pv < 0.05 else ">"} 0.05',
          f'{f(pv, 4)} {"<" if pv < 0.05 else ">"} 0.05, so ' + (f'reject H₀: convincing evidence the mean {var} is less than {g(mu)}.' if pv < 0.05 else 'fail to reject H₀.'), 1, 'Decision with justification in context.'),
    ]
    return stem, parts, ['4.5.A', '4.5.B', '4.5.C'], var


@frq(4, 7)
def one_prop_test_frq(rng, lv):
    who, prop, p0 = rng.choice(PROP)
    p0 = round(p0, 2)
    n = rng.choice([200, 300, 400])
    x = round(n * p0) + rng.choice([12, 15, 18])
    ph = x / n
    se = math.sqrt(p0 * (1 - p0) / n)
    z = (ph - p0) / se
    pv = round(1 - table_a(z), 4)
    stem = (f'In past years {pct(p0)} of {who} {prop}. A random sample of {n} this year finds {x} who {prop}. Is there convincing evidence at α = 0.05 that the proportion has increased?'
            + four_step_note(lv))
    parts = [
        P('State: hypotheses and parameter.', f'H₀: p = {g(p0)}; Hₐ: p > {g(p0)}, where p = the proportion of all {who} {wt(who)} {prop} this year',
          f'p = true proportion this year. H₀: p = {g(p0)}; Hₐ: p > {g(p0)}; α = 0.05.', 1, 'Hypotheses with the parameter defined.'),
        P('Plan: name the test and check the conditions.' + cue(lv, 'use p₀ in the Large Counts check'), f'One-sample z test for p; random; 10%; np₀ = {g(n * p0)} and n(1 − p₀) = {g(round(n * (1 - p0), 2))} ≥ 10',
          f'One-sample z test for a proportion. Random sample; {n} < 10% of the population; {n}({g(p0)}) = {g(n * p0)} and {n}({g(round(1 - p0, 2))}) = {g(round(n * (1 - p0), 2))} are both at least 10.', 2, '1 point test; 1 point conditions.'),
        P('Do: find the test statistic and p-value. Use Table A (round z to two decimal places).', f'z ≈ {f(z, 2)}; p-value ≈ {f(pv, 4)}',
          f'p̂ = {g(round(ph, 4))}; z = ({g(round(ph, 4))} − {g(p0)})/√({g(p0)}({g(round(1 - p0, 2))})/{n}) ≈ {f(z, 2)}; p-value = P(Z > {f(z, 2)}) = {f(pv, 4)}.', 2, '1 point z; 1 point p-value.'),
        P('Conclude: state your conclusion in context, and justify it with the p-value.', ('Reject H₀: convincing evidence that the proportion has increased' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence of an increase'),
          f'Because {f(pv, 4)} {"<" if pv < 0.05 else ">"} α = 0.05, we {"reject" if pv < 0.05 else "fail to reject"} H₀. There {"is" if pv < 0.05 else "is not"} convincing evidence that the proportion of {who} {wt(who)} {prop} has increased.',
          1, 'Comparison with α and conclusion about p in context.'),
    ]
    return stem, parts, ['3.5.A', '3.5.C', '3.7.A', '3.7.B'], who


@frq(4, 8)
def errors_frq(rng, lv):
    ctx, h0, ha, c1, c2 = rng.choice([
        ('A factory tests whether the mean fill of its bottles is less than 500 mL.', 'μ = 500', 'μ < 500', 'the machine is stopped and adjusted when it is filling correctly', 'customers get underfilled bottles and the factory does not fix the machine'),
        ('A school tests whether a new reading program raises the proportion of students reading at grade level above 0.60.', 'p = 0.60', 'p > 0.60', 'the school adopts a program that does not help', 'the school passes up a program that really helps'),
        ('A health agency tests whether the proportion of contaminated wells exceeds 0.05.', 'p = 0.05', 'p > 0.05', 'the agency spends money on clean-up that is not needed', 'contaminated wells go untreated'),
    ])
    stem = ctx + f' H₀: {h0}; Hₐ: {ha}.'
    parts = [
        P('Describe a Type I error in context.' + cue(lv, 'rejecting a true H₀'), f'Concluding {ha} when in fact {h0}', f'A Type I error is rejecting H₀ when it is true: concluding {ha} when really {h0}.', 1, 'Correct in context.'),
        P('Describe a Type II error in context.', f'Failing to conclude {ha} when it is true', f'Failing to reject H₀ when Hₐ is true: missing that {ha}.', 1, 'Correct in context.'),
        P('Give a consequence of each error. Which is more serious here? Justify.', f'Type I: {c1}; Type II: {c2}',
          f'Type I: {c1}. Type II: {c2}. A reasonable argument either way, tied to these consequences, earns credit.', 1, 'Both consequences and a justified choice.'),
        P('Describe two ways to increase the power of the test.' + (' Explain how one of them affects the probability of a Type I error.' if lv != 'cp2' else ''),
          'Increase the sample size; use a larger α' + ('; a larger α also increases P(Type I error)' if lv != 'cp2' else ''),
          'Larger n reduces variability, and a larger α makes rejection easier; both raise power.' + (' But α is the probability of a Type I error, so increasing α makes that error more likely.' if lv != 'cp2' else ''),
          1, 'Two valid ways' + (' and the α trade-off.' if lv != 'cp2' else '.')),
    ]
    return stem, parts, ['3.8.A', '3.8.C', '3.8.D'], ctx[:30]


@frq(4, 9)
def two_prop_frq(rng, lv):
    g1, g2, verb = rng.choice([('a reminder text', 'no reminder', 'showed up for their appointment'), ('the new website design', 'the old design', 'made a purchase'),
                               ('a free sample', 'no sample', 'bought the product')])
    n1, n2 = rng.choice([(200, 200), (250, 240), (180, 220)])
    p1, p2 = rng.choice([(0.62, 0.52), (0.18, 0.11), (0.45, 0.38)])
    x1, x2 = round(n1 * p1), round(n2 * p2)
    ph1, ph2 = x1 / n1, x2 / n2
    pc = (x1 + x2) / (n1 + n2)
    se = math.sqrt(pc * (1 - pc) * (1 / n1 + 1 / n2))
    z = (ph1 - ph2) / se
    pv = round(1 - table_a(z), 4)
    stem = (f'In a randomized experiment, {n1} customers got {g1} and {n2} got {g2}. {x1} and {x2} of them, respectively, {verb}. '
            f'Do the data give convincing evidence at α = 0.05 that {g1} increases the proportion who {verb.split(" ")[0]}…?').replace(f'who {verb.split(" ")[0]}…', 'with this outcome') + four_step_note(lv)
    parts = [
        P('State: define the parameters and give the hypotheses.', f'H₀: p₁ − p₂ = 0; Hₐ: p₁ − p₂ > 0 (p₁ = {g1}, p₂ = {g2})',
          f'p₁ and p₂ = the true proportions who {verb} with {g1} and with {g2}. H₀: p₁ = p₂; Hₐ: p₁ > p₂.', 1, 'Parameters and hypotheses.'),
        P('Plan: name the test and check the conditions.' + cue(lv, 'use the pooled proportion for Large Counts'), f'Two-sample z test for p₁ − p₂; random assignment; all counts ≥ 10',
          f'Two-sample z test for a difference in proportions. Random assignment; pooled p̂ = {g(round(pc, 4))}; n₁p̂, n₁(1 − p̂), n₂p̂, n₂(1 − p̂) are all at least 10.', 2, '1 point test; 1 point conditions.'),
        P('Do: find the test statistic and p-value. Use Table A (round z to two decimal places).', f'z ≈ {f(z, 2)}; p-value ≈ {f(pv, 4)}',
          f'p̂₁ = {g(round(ph1, 4))}, p̂₂ = {g(round(ph2, 4))}, pooled {g(round(pc, 4))}; SE ≈ {f(se, 4)}; z ≈ {f(z, 2)}; p-value = P(Z > {f(z, 2)}) = {f(pv, 4)}.', 2, '1 point z; 1 point p-value.'),
        P('Conclude: state your conclusion in context, and justify it with the p-value.' + (' Can we say the treatment caused the difference? Explain.' if lv == 'honors' else ''),
          ('Reject H₀: convincing evidence' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence') + f' that {g1} increases the proportion' + ('; yes, because of random assignment' if lv == 'honors' else ''),
          f'{f(pv, 4)} {"<" if pv < 0.05 else ">"} 0.05, so we {"reject" if pv < 0.05 else "fail to reject"} H₀.' + (' Random assignment allows a cause-and-effect conclusion.' if lv == 'honors' else ''),
          1, 'Conclusion in context.'),
    ]
    return stem, parts, ['3.12.A', '3.12.B', '3.13.A', '3.13.C'], g1


@frq(4, 10)
def paired_frq(rng, lv):
    who, what, diff, n = rng.choice([('students', 'their reading scores before and after a tutoring program', 'after − before', 12),
                                     ('runners', 'their 5-km times (seconds) in old shoes and in new shoes', 'old − new', 10),
                                     ('typists', 'their typing speeds (words per minute) on two keyboards, A and B', 'B − A', 14)])
    db = round(rng.choice([2.1, 3.4, 1.8, 4.2]), 1)
    sd = round(rng.choice([3.5, 4.8, 2.9]), 2)
    t = db / (sd / math.sqrt(n))
    pv = stats.t.sf(t, n - 1)
    stem = (f'A random sample of {n} {who} records {what}. The differences ({diff}) have mean d̄ = {g(db)} and standard deviation s_d = {g(sd)}, and a dot plot of the differences shows no strong skew or outliers. '
            'Is there convincing evidence at α = 0.05 that the true mean difference is positive?' + four_step_note(lv))
    parts = [
        P('State: define the parameter and give the hypotheses.', f'μ_d = true mean difference ({diff}); H₀: μ_d = 0; Hₐ: μ_d > 0', f'μ_d = the true mean of the differences ({diff}) for all {who}. H₀: μ_d = 0; Hₐ: μ_d > 0.', 1, 'Parameter and hypotheses.'),
        P('Plan: explain why a paired t test is appropriate and check the conditions.' + cue(lv, 'the same individuals are measured twice'), 'Paired t test: each individual gives two related values; random; 10%; differences show no strong skew',
          f'Each of the {who} gives two measurements, so analyze the differences. Random sample; {n} is less than 10% of all {who}; n = {n} < 30, but the differences show no strong skew or outliers.', 2, '1 point paired reason; 1 point conditions.'),
        P('Do: find the test statistic and p-value. Use technology for the p-value.', f't ≈ {f(t, 2)}; p-value ≈ {f(pv, 4)}',
          f't = {g(db)}/({g(sd)}/√{n}) ≈ {f(t, 2)}, df = {n - 1}; p-value = P(t > {f(t, 2)}) ≈ {f(pv, 4)}.', 2, '1 point t and df; 1 point p-value.'),
        P('Conclude: state your conclusion in context, and justify it with the p-value.', ('Reject H₀: convincing evidence of a positive mean difference' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence of a positive mean difference'),
          f'{f(pv, 4)} {"<" if pv < 0.05 else ">"} 0.05, so we {"reject" if pv < 0.05 else "fail to reject"} H₀: there {"is" if pv < 0.05 else "is not"} convincing evidence that the mean difference ({diff}) is positive for all {who}.', 1, 'Conclusion in context.'),
    ]
    return stem, parts, ['4.4.A', '4.4.C', '4.5.A', '4.5.C'], what


@frq(4, 11)
def slope_ci_frq(rng, lv):
    x, y = rng.choice([('hours studied', 'test score'), ('advertising spending ($100s)', 'weekly sales ($1000s)'), ('fertilizer (g)', 'plant height (cm)')])
    n = rng.choice([15, 20, 25])
    b = rng.choice([2.6, 1.4, 0.75])
    se = round(b * rng.choice([0.3, 0.35, 0.45]), 3)
    a = round(rng.uniform(10, 50), 2)
    ts = tstar(0.95, n - 2)
    lo, hi = b - ts * se, b + ts * se
    stem = (f'Computer output for a regression of y = {y} on x = {x} for a random sample of n = {n}: intercept {g(a)}, slope b = {g(b)}, SE_b = {g(se)}. '
            'Construct a 95% confidence interval for the slope (Beyond AP: regression inference).' + four_step_note(lv))
    parts = [
        P('State: define the parameter.', f'β = the slope of the true regression line relating {y} to {x}', f'β = the true slope for all individuals: the mean change in {y} per unit of {x}.', 1, 'Parameter in context.'),
        P('Plan: name the procedure and list the conditions.' + cue(lv, 'LINER: linear, independent, Normal residuals, equal SD, random'), 't interval for the slope; linear, independent, Normal residuals, equal variance, random',
          'A t interval for the slope. Conditions: linear form (residual plot), independent observations (10%), Normal residuals, equal spread (residual plot), random sample.', 1, 'Procedure and conditions.'),
        P('Do: compute the interval. Round to three decimal places.', f'({f(lo, 3)}, {f(hi, 3)})', f'df = {n - 2}; t* = {f(ts, 3)}; {g(b)} ± {f(ts, 3)}({g(se)}) = ({f(lo, 3)}, {f(hi, 3)}).', 2, '1 point for df and t*; 1 point for the interval.'),
        P('Conclude: interpret the interval, and say whether it gives evidence of a positive linear relationship.', f'We are 95% confident the true slope is between {f(lo, 3)} and {f(hi, 3)}; ' + ('yes, 0 is not in the interval' if lo > 0 else 'no, 0 is plausible'),
          f'We are 95% confident that each additional unit of {x} is associated with an increase of between {f(lo, 3)} and {f(hi, 3)} in mean {y}. ' + ('All values are positive.' if lo > 0 else 'The interval contains 0.'),
          2, '1 point interpretation; 1 point decision about 0.'),
    ]
    return stem, parts, ['BEYOND.SLOPE'], x


@frq(4, 12)
def gof_frq(rng, lv):
    cats, props, ctx = rng.choice([(['bus', 'car', 'walk', 'bike'], [0.30, 0.40, 0.20, 0.10], 'how students get to school'), (['red', 'blue', 'green', 'yellow'], [0.25, 0.25, 0.25, 0.25], 'candy colors in a bag'),
                                   (['A', 'B', 'C', 'D or F'], [0.20, 0.35, 0.30, 0.15], 'grades in a course')])
    n = 200
    exps = [n * p for p in props]
    obs = [round(e + d) for e, d in zip(exps, rng.choice([[8, -10, 6, -4], [-9, 12, -6, 3], [5, -3, -6, 4]]))]
    obs[-1] = n - sum(obs[:-1])
    chi = sum((o - e) ** 2 / e for o, e in zip(obs, exps))
    df = len(cats) - 1
    pv = stats.chi2.sf(chi, df)
    stem = (f'A claim says the distribution of {ctx} is ' + ', '.join(f'{c} {pct(p)}' for c, p in zip(cats, props)) + f'. A random sample of {n} gives ' + ', '.join(f'{c} {o}' for c, o in zip(cats, obs))
            + '. Test the claim at α = 0.05 (Beyond AP: chi-square goodness of fit).' + four_step_note(lv))
    parts = [
        P('State: give the hypotheses.', 'H₀: the claimed distribution is correct; Hₐ: it is not', 'H₀: ' + ', '.join(f'p_{c} = {g(p)}' for c, p in zip(cats, props)) + '. Hₐ: at least one proportion differs.', 1, 'Both hypotheses.'),
        P('Plan: name the test and check the conditions.' + cue(lv, 'expected counts must all be at least 5'), f'Chi-square GOF test; random; expected counts ' + ', '.join(g(e) for e in exps) + ' all ≥ 5',
          'Chi-square goodness-of-fit test. Random sample; expected counts (n × claimed proportion) ' + ', '.join(g(e) for e in exps) + ' are all at least 5.', 1, 'Test and expected counts.'),
        P('Do: find the chi-square statistic, df and p-value. Round χ² to two decimal places.', f'χ² ≈ {f(chi, 2)}; df = {df}; p-value ≈ {f(pv, 4)}',
          'χ² = Σ (O − E)²/E = ' + ' + '.join(f'({o} − {g(e)})²/{g(e)}' for o, e in zip(obs, exps)) + f' ≈ {f(chi, 2)}; df = {df}; p-value ≈ {f(pv, 4)}.', 2, '1 point χ²; 1 point df and p-value.'),
        P('Conclude: state your conclusion in context, and justify it with the p-value.', ('Reject H₀: convincing evidence the claim is wrong' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence against the claim'),
          f'{f(pv, 4)} {"<" if pv < 0.05 else ">"} 0.05, so we {"reject" if pv < 0.05 else "fail to reject"} H₀ about {ctx}.', 1, 'Conclusion in context.'),
    ]
    return stem, parts, ['BEYOND.GOF'], ctx


@frq(4, 13)
def chisq_frq(rng, lv):
    rv, rows, cv, cols = rng.choice([('grade', ['Freshmen', 'Sophomores', 'Juniors'], 'favorite lunch', ['Pizza', 'Salad', 'Sandwich']),
                                     ('age group', ['Under 30', '30–49', '50+'], 'preferred news source', ['Online', 'TV', 'Print'])])
    t = [[rng.randint(18, 60) for _ in cols] for _ in rows]
    N = sum(map(sum, t))
    rt = [sum(r) for r in t]
    ct = [sum(t[r][c] for r in range(3)) for c in range(3)]
    exp = [[rt[r] * ct[c] / N for c in range(3)] for r in range(3)]
    chi = sum((t[r][c] - exp[r][c]) ** 2 / exp[r][c] for r in range(3) for c in range(3))
    pv = stats.chi2.sf(chi, 4)
    table = '; '.join(f'{rows[r]}: ' + ', '.join(f'{cols[c]} {t[r][c]}' for c in range(3)) for r in range(3))
    stem = f'A random sample of {N} people is classified by {rv} and {cv}. Counts — {table}. Is there convincing evidence of an association at α = 0.05?' + four_step_note(lv)
    parts = [
        P('State: give the hypotheses.', f'H₀: no association between {rv} and {cv}; Hₐ: there is an association', f'H₀: {rv} and {cv} are independent; Hₐ: they are not.', 1, 'Hypotheses in context.'),
        P(f'Plan: name the test and check the conditions. Find the expected count for {rows[0]} and {cols[0]}.' + cue(lv, 'expected = row total × column total ÷ table total'),
          f'Chi-square test for independence; random; expected counts ≥ 5 (e.g., {f(exp[0][0], 2)})',
          f'Chi-square test for independence. Random sample; expected count for {rows[0]}/{cols[0]} = {rt[0]} × {ct[0]}/{N} ≈ {f(exp[0][0], 2)}; the smallest expected count is {f(min(map(min, exp)), 2)} ≥ 5.',
          2, '1 point test; 1 point conditions with the expected count.'),
        P('Do: find χ², df and the p-value. Use technology.', f'χ² ≈ {f(chi, 2)}; df = 4; p-value ≈ {f(pv, 4)}', f'χ² ≈ {f(chi, 2)}; df = (3 − 1)(3 − 1) = 4; p-value ≈ {f(pv, 4)}.', 1, 'All three.'),
        P('Conclude: state your conclusion in context, and justify it with the p-value.', ('Reject H₀: convincing evidence of an association' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence of an association'),
          f'{f(pv, 4)} {"<" if pv < 0.05 else ">"} 0.05, so we {"reject" if pv < 0.05 else "fail to reject"} H₀ about {rv} and {cv}.', 1, 'Conclusion in context.'),
    ]
    return stem, parts, ['3.14.B', '3.14.C', '3.15.A', '3.15.B', '3.15.D'], rv


@frq(4, 14)
def slope_test_frq(rng, lv):
    x, y, sign = rng.choice([('hours of sleep', 'reaction time (ms)', -1), ('practice time (min)', 'free-throw percentage', 1), ('temperature (°F)', 'ice cream sales', 1),
                             ('age of a car (years)', 'resale value ($1000s)', -1)])
    n = rng.choice([12, 15, 20])
    b = sign * rng.choice([4.2, 1.15, 2.8])
    se = round(abs(b) * rng.choice([0.35, 0.45, 0.6]), 3)
    t = b / se
    pv = 2 * stats.t.sf(abs(t), n - 2)
    stem = (f'Regression output for y = {y} on x = {x}, from a random sample of n = {n}: slope b = {g(b)}, SE_b = {g(se)}. Is there convincing evidence of a linear relationship at α = 0.05? '
            '(Beyond AP: regression inference.)' + four_step_note(lv))
    parts = [
        P('State: give the hypotheses.', 'H₀: β = 0; Hₐ: β ≠ 0', f'β = the true slope relating {y} to {x}. H₀: β = 0; Hₐ: β ≠ 0.', 1, 'Hypotheses with β defined.'),
        P('Plan: name the test and list the conditions.' + cue(lv, 'LINER'), 't test for the slope; linear, independent, Normal residuals, equal SD, random', 'A t test for the slope; check the residual plot for linearity and equal spread, the residuals for Normality, and random sampling.', 1, 'Test and conditions.'),
        P('Do: compute t, df and the p-value. Use technology.', f't ≈ {f(t, 2)}; df = {n - 2}; p-value ≈ {f(pv, 4)}', f't = {g(b)}/{g(se)} ≈ {f(t, 2)}; df = {n} − 2 = {n - 2}; p-value = 2P(t ≥ {f(abs(t), 2)}) ≈ {f(pv, 4)}.', 2, '1 point t and df; 1 point p-value.'),
        P('Conclude: state your conclusion in context, and justify it with the p-value.', ('Reject H₀: convincing evidence of a linear relationship' if pv < 0.05 else 'Fail to reject H₀: not convincing evidence of a linear relationship'),
          f'{f(pv, 4)} {"<" if pv < 0.05 else ">"} 0.05, so we {"reject" if pv < 0.05 else "fail to reject"} H₀: there {"is" if pv < 0.05 else "is not"} convincing evidence of a linear relationship between {x} and {y}.', 1, 'Conclusion in context.'),
    ]
    return stem, parts, ['BEYOND.SLOPE'], x


def lin(a, b, x='x'):
    s = f'{g(a)} + {g(b)}{x}' if b >= 0 else f'{g(a)} − {g(abs(b))}{x}'
    return s


def sup(n):
    return str(n).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))


def money(v):
    return f'${v:,.2f}' if abs(v - round(v)) > 1e-9 else f'${round(v):,}'
