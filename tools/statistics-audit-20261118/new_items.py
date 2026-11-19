"""Statistics audit #6 and #11 (2026-11-18): new items.
#6  Sampling distributions of a difference, p̂₁ − p̂₂ and x̄₁ − x̄₂ (AP topics 3.9 and 4.6): 8 per level in
    Anticipating Patterns skill 9. Values computed with scipy.
#11 Choosing the inference procedure: 8 per level, filed under the skill of the correct procedure.
Items are appended once (ids ending -d## and -c##); rerunning rebuilds them in place. Deterministic."""
import math, os, random, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib
from scipy import stats

NOTE = 'Original Claude-authored item (family: {fam}). Statistics audit 2026-11-18; key computed with scipy and re-checked by tools/statistics-audit-20261118/verify_keys.py.'


def f(v, d=4):
    s = f'{v:.{d}f}'
    return s.replace('-', '−')


def mc(rng, key, wrong):
    opts = [key] + [w for w in dict.fromkeys(wrong) if w != key][:3]
    assert len(opts) == 4, (key, wrong)
    rng.shuffle(opts)
    return [{'text': o, 'correct': o == key} for o in opts]


def item(qid, skill, level, fmt, prompt, answer, steps, std, fam, rng=None, wrong=None):
    q = {'id': qid, 'skillId': skill, 'level': level, 'format': fmt, 'prompt': prompt, 'answer': answer, 'solutionSteps': steps,
         'standards': std, 'sourceNotes': NOTE.format(fam=fam)}
    if fmt == 'multiple-choice':
        q['options'] = mc(rng, answer, wrong)
    return q


# ------------------------------------------------------------ #6 differences
PROPS = [('students', 'walk to school', 0.30, 0.22, 'East High', 'West High'),
         ('adults', 'own an electric car', 0.12, 0.08, 'Springfield', 'Riverton'),
         ('seeds', 'sprout', 0.85, 0.78, 'Brand A', 'Brand B'),
         ('students', 'have a part-time job', 0.40, 0.25, 'the senior class', 'the junior class'),
         ('patients', 'arrive late', 0.18, 0.10, 'North Clinic', 'South Clinic'),
         ('subscribers', 'cancel within a year', 0.25, 0.20, 'Service A', 'Service B')]
MEANS = [('battery life (hours)', 'Brand A batteries', 'Brand B batteries', 12.0, 2.0, 11.0, 1.5),
         ('commute time (minutes)', 'City A workers', 'City B workers', 28.0, 9.0, 24.0, 8.0),
         ('apple weight (grams)', 'Orchard A apples', 'Orchard B apples', 160.0, 12.0, 150.0, 15.0),
         ('reaction time (ms)', 'gamers', 'non-gamers', 240.0, 30.0, 260.0, 35.0),
         ('daily screen time (minutes)', 'ninth graders', 'twelfth graders', 280.0, 60.0, 250.0, 70.0),
         ('fill weight (grams)', 'boxes from Machine 1', 'boxes from Machine 2', 510.0, 6.0, 505.0, 8.0)]


def diff_items(level, rng):
    out = []
    sk = 'anticipating-patterns-skill-09'
    cp = PROPS[:]; rng.shuffle(cp); cm = MEANS[:]; rng.shuffle(cm)
    n = 0
    for i in range(4):
        noun, verb, p1, p2, g1, g2 = cp[i]
        n1, n2 = {'cp2': [(200, 150), (160, 140)], 'cp1': [(120, 100), (300, 250)], 'honors': [(150, 150), (250, 220)]}[level][i % 2]
        mu, sd = p1 - p2, math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
        ctx = f'In {g1}, {round(p1 * 100)}% of {noun} {verb}; in {g2}, {round(p2 * 100)}% do. Independent random samples of {n1} from {g1} and {n2} from {g2} are taken, and D = p̂₁ − p̂₂ (p̂₁ from {g1}).'
        kind = ['mean', 'sd', 'cond', 'prob'][(i + {'cp2': 0, 'cp1': 1, 'honors': 2}[level]) % 4] if level != 'cp2' else ['mean', 'sd', 'sd', 'cond'][i]
        n += 1
        qid = f'stat-u3-s09-{level}-d{n:02d}'
        fam = 'audit_diff_props'
        std = ['APSTATS.3.9.A'] if kind in ('mean', 'sd') else ['APSTATS.3.9.B'] if kind == 'cond' else ['APSTATS.3.9.C']
        fmt = 'multiple-choice' if i % 2 == 0 else 'short-answer'
        if kind == 'mean':
            ans = f(mu, 2)
            out.append(item(qid, sk, level, fmt, ctx + ' What is the mean of the sampling distribution of D?', ans,
                            ['The sampling distribution of p̂₁ − p̂₂ is centered at p₁ − p₂.', f'μ_D = {p1:g} − {p2:g} = {ans}.'], std, fam, rng,
                            [f(p2 - p1, 2), f(p1 + p2, 2), f((p1 + p2) / 2, 2)]))
        elif kind == 'sd':
            ans = f(sd, 4)
            wrong = [f(math.sqrt(p1 * (1 - p1) / n1) + math.sqrt(p2 * (1 - p2) / n2), 4), f(math.sqrt(abs(p1 * (1 - p1) / n1 - p2 * (1 - p2) / n2)), 4), f(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2, 4)]
            out.append(item(qid, sk, level, fmt, ctx + ' Find the standard deviation of the sampling distribution of D. Round to four decimal places.', ans,
                            ['For independent samples the variances add: σ_D = √(p₁(1 − p₁)/n₁ + p₂(1 − p₂)/n₂).',
                             f'σ_D = √({p1:g}·{1 - p1:g}/{n1} + {p2:g}·{1 - p2:g}/{n2}) = √{p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2:.6f} ≈ {ans}.'], std, fam, rng, wrong))
        elif kind == 'cond':
            c = [n1 * p1, n1 * (1 - p1), n2 * p2, n2 * (1 - p2)]
            ans = 'Yes; all four expected counts are at least 10'
            steps = ['Large Counts for two proportions: n₁p₁, n₁(1 − p₁), n₂p₂ and n₂(1 − p₂) must all be at least 10.',
                     f'{n1}({p1:g}) = {c[0]:g}, {n1}({1 - p1:g}) = {c[1]:g}, {n2}({p2:g}) = {c[2]:g}, {n2}({1 - p2:g}) = {c[3]:g}.',
                     'All are at least 10 (and each sample is less than 10% of its population), so D is approximately Normal.']
            assert min(c) >= 10
            out.append(item(qid, sk, level, 'multiple-choice', ctx + ' Is the sampling distribution of D approximately Normal? Choose the best answer.', ans, steps, std, fam, rng,
                            ['No; the two samples have different sizes', 'No; the two proportions are not equal', 'Yes; both samples are at least 30']))
        else:
            d0 = rng.choice([0.0, 0.02]) if mu > 0.04 else 0.0
            pr = stats.norm.sf((d0 - mu) / sd)
            ans = f(pr, 4)
            out.append(item(qid, sk, level, 'short-answer', ctx + f' Find the probability that D is greater than {d0:g}, that is, that the {g1} sample proportion is larger{" by more than " + format(d0, "g") if d0 else ""}. Use technology. Round to four decimal places.', ans,
                            [f'μ_D = {mu:.2f} and σ_D = √({p1:g}·{1 - p1:g}/{n1} + {p2:g}·{1 - p2:g}/{n2}) ≈ {sd:.4f}; Large Counts holds, so D is approximately Normal.',
                             f'z = ({d0:g} − {mu:.2f})/{sd:.4f} ≈ {(d0 - mu) / sd:.3f}.'.replace('-', '−'), f'P(D > {d0:g}) = P(Z > {(d0 - mu) / sd:.3f}) ≈ {ans}.'.replace('-', '−')], std, fam))
    for i in range(4):
        var, g1, g2, m1, s1, m2, s2 = cm[i]
        n1, n2 = {'cp2': [(40, 35), (50, 45)], 'cp1': [(36, 40), (60, 50)], 'honors': [(45, 50), (32, 30)]}[level][i % 2]
        mu, sd = m1 - m2, math.sqrt(s1 * s1 / n1 + s2 * s2 / n2)
        ctx = f'For {g1}, {var} has mean {m1:g} and SD {s1:g}; for {g2}, the mean is {m2:g} and the SD is {s2:g}. Independent random samples of {n1} from {g1} and {n2} from {g2} are taken, and D = x̄₁ − x̄₂ ({g1} minus {g2}).'
        kind = ['mean', 'sd', 'sd', 'cond'][i] if level == 'cp2' else ['mean', 'sd', 'cond', 'prob'][(i + {'cp1': 1, 'honors': 2}[level]) % 4]
        n += 1
        qid = f'stat-u3-s09-{level}-d{n:02d}'
        fam = 'audit_diff_means'
        std = ['APSTATS.4.6.A'] if kind in ('mean', 'sd') else ['APSTATS.4.6.B'] if kind == 'cond' else ['APSTATS.4.6.C']
        fmt = 'multiple-choice' if i % 2 == 1 else 'short-answer'
        if kind == 'mean':
            ans = f(mu, 1)
            out.append(item(qid, sk, level, fmt, ctx + ' What is the mean of the sampling distribution of D?', ans,
                            ['The sampling distribution of x̄₁ − x̄₂ is centered at μ₁ − μ₂.', f'μ_D = {m1:g} − {m2:g} = {ans}.'], std, fam, rng,
                            [f(-mu, 1), f(m1 + m2, 1), f(mu / 2, 1)]))
        elif kind == 'sd':
            ans = f(sd, 3)
            wrong = [f(s1 / math.sqrt(n1) + s2 / math.sqrt(n2), 3), f(math.sqrt(s1 * s1 + s2 * s2), 3), f(abs(s1 / math.sqrt(n1) - s2 / math.sqrt(n2)), 3)]
            out.append(item(qid, sk, level, fmt, ctx + ' Find the standard deviation of the sampling distribution of D. Round to three decimal places.', ans,
                            ['For independent samples the variances add: σ_D = √(σ₁²/n₁ + σ₂²/n₂).', f'σ_D = √({s1:g}²/{n1} + {s2:g}²/{n2}) = √{s1 * s1 / n1 + s2 * s2 / n2:.4f} ≈ {ans}.'], std, fam, rng, wrong))
        elif kind == 'cond':
            ans = 'Yes; both samples have at least 30 observations, so the Central Limit Theorem applies'
            if min(n1, n2) < 30:
                n1, n2 = 40, 35
                ctx = re.sub(r'samples of \d+ from', f'samples of {n1} from', ctx, count=1); ctx = re.sub(r'and \d+ from', f'and {n2} from', ctx, count=1)
            out.append(item(qid, sk, level, 'multiple-choice', ctx + ' The shapes of the two population distributions are unknown. Is the sampling distribution of D approximately Normal?', ans,
                            ['The populations\' shapes are unknown, so use the Central Limit Theorem for each sample mean.', f'n₁ = {n1} and n₂ = {n2} are both at least 30, so x̄₁ and x̄₂ are approximately Normal.',
                             'A difference of independent, approximately Normal sample means is approximately Normal.'], std, fam, rng,
                            ['No; the populations must be known to be Normal', 'No; the two samples have different sizes', 'Yes; the two population SDs are similar']))
        else:
            pr = stats.norm.sf((0 - mu) / sd) if mu > 0 else stats.norm.cdf((0 - mu) / sd)
            sign = '>' if mu > 0 else '<'
            ans = f(pr, 4)
            out.append(item(qid, sk, level, 'short-answer', ctx + f' Find P(D {sign} 0). Use technology. Round to four decimal places.', ans,
                            [f'μ_D = {mu:g} and σ_D = √({s1:g}²/{n1} + {s2:g}²/{n2}) ≈ {sd:.3f}; both samples are large, so D is approximately Normal.',
                             f'z = (0 − {mu:g})/{sd:.3f} ≈ {-mu / sd:.3f}.'.replace('-', '−'), f'P(D {sign} 0) ≈ {ans}.'], std, fam))
    return out


# ------------------------------------------------------------ #11 choosing the procedure
P = {'1pz_int': ('One-proportion z interval', 3, ['APSTATS.3.3.A']), '1pz_test': ('One-proportion z test', 7, ['APSTATS.3.5.A']),
     '1t_int': ('One-sample t interval for a mean', 4, ['APSTATS.4.2.B']), '1t_test': ('One-sample t test for a mean', 7, ['APSTATS.4.4.A']),
     '2pz_int': ('Two-proportion z interval', 9, ['APSTATS.3.10.A']), '2pz_test': ('Two-proportion z test', 9, ['APSTATS.3.12.A']),
     '2t_int': ('Two-sample t interval for a difference in means', 10, ['APSTATS.4.7.A']), '2t_test': ('Two-sample t test for a difference in means', 10, ['APSTATS.4.9.A']),
     'pt_test': ('Paired t test for a mean difference', 10, ['APSTATS.4.4.A']), 'pt_int': ('Paired t interval for a mean difference', 10, ['APSTATS.4.2.B']),
     'chi_ind': ('Chi-square test for independence', 13, ['APSTATS.3.14.B']), 'chi_hom': ('Chi-square test for homogeneity', 13, ['APSTATS.3.14.B'])}
SCEN = [
 ('A random sample of 400 voters is asked whether they support a new park. Estimate the proportion of all voters who support it.', '1pz_int', ['1pz_test', '1t_int', '2pz_int'], 'one categorical variable (support: yes/no) from one sample, and the goal is to estimate, so a one-proportion z interval'),
 ('A company claims 90% of its packages arrive on time. A random sample of 250 packages is checked to see whether the true rate is lower.', '1pz_test', ['1pz_int', '1t_test', 'chi_ind'], 'one categorical variable (on time or not) from one sample, testing a claimed value, so a one-proportion z test'),
 ('A random sample of 30 bags of chips is weighed to estimate the mean weight of all bags from the factory.', '1t_int', ['1pz_int', '1t_test', '2t_int'], 'one quantitative variable (weight) from one sample, estimating μ with σ unknown, so a one-sample t interval'),
 ('A random sample of 25 lightbulbs is tested to decide whether the mean lifetime is less than the advertised 1,000 hours.', '1t_test', ['1t_int', '1pz_test', 'pt_test'], 'one quantitative variable from one sample, testing a claimed mean, so a one-sample t test'),
 ('Random samples of 300 juniors and 280 seniors are asked whether they have a driver\'s license. Estimate the difference in the proportions with a license.', '2pz_int', ['2pz_test', '2t_int', 'chi_hom'], 'one categorical variable compared across two independent groups, estimating p₁ − p₂, so a two-proportion z interval'),
 ('In a randomized experiment, 200 patients get a new vaccine and 200 get a placebo. Researchers test whether the infection rate is lower with the vaccine.', '2pz_test', ['2pz_int', '2t_test', '1pz_test'], 'a categorical response (infected or not) in two randomly assigned groups, testing for a difference, so a two-proportion z test'),
 ('Random samples of 40 workers from each of two cities record commute time. Estimate how much longer the mean commute is in City A.', '2t_int', ['2t_test', 'pt_int', '2pz_int'], 'a quantitative variable in two independent samples, estimating μ₁ − μ₂, so a two-sample t interval'),
 ('Students are randomly assigned to study with music (35 students) or in silence (35 students). Test whether the mean quiz score differs.', '2t_test', ['2t_int', 'pt_test', '2pz_test'], 'a quantitative response in two randomly assigned, independent groups, testing for a difference, so a two-sample t test'),
 ('Twenty runners each run a mile in old shoes and in new shoes (in random order). Test whether the new shoes lower the mean time.', 'pt_test', ['2t_test', '1t_int', '2pz_test'], 'each runner gives two related measurements, so analyze the differences with a paired t test'),
 ('Fifteen students take a reading test before and after a summer program. Estimate the mean improvement.', 'pt_int', ['2t_int', 'pt_test', '1pz_int'], 'before and after scores on the same students are paired, and the goal is to estimate, so a paired t interval'),
 ('A random sample of 500 adults is classified by age group (3 groups) and preferred news source (4 sources). Is there an association between age group and news source?', 'chi_ind', ['chi_hom', '2pz_test', '1pz_test'], 'one sample classified on two categorical variables, asking about association, so a chi-square test for independence'),
 ('Separate random samples of customers from three stores record their payment method (cash, card, phone). Do the distributions of payment method differ among the stores?', 'chi_hom', ['chi_ind', '2pz_test', '2t_test'], 'separate samples from several populations compared on one categorical variable, so a chi-square test for homogeneity'),
 ('A random sample of 60 apples from an orchard is weighed. Is there convincing evidence that the mean weight is more than 150 g?', '1t_test', ['1t_int', '1pz_test', '2t_test'], 'one quantitative variable, one sample, testing a claimed mean, so a one-sample t test'),
 ('A random sample of 1,000 phone users reports whether they use a screen-time limit. Estimate the proportion of all phone users who do.', '1pz_int', ['1pz_test', '1t_int', 'chi_ind'], 'one categorical variable from one sample, estimating p, so a one-proportion z interval'),
 ('Two randomly assigned groups of 50 plants get Fertilizer A or B, and researchers record whether each plant flowers. Estimate the difference in flowering rates.', '2pz_int', ['2pz_test', '2t_int', 'chi_ind'], 'a categorical response in two independent groups, estimating p₁ − p₂, so a two-proportion z interval'),
 ('Twelve sets of identical twins are split so one twin uses a tutoring app and the other does not; both take the same test. Test whether the app raises mean scores.', 'pt_test', ['2t_test', '2pz_test', '1t_int'], 'twins form matched pairs, so analyze the 12 differences with a paired t test'),
 ('Random samples of 45 cars of Model X and 50 cars of Model Y record gas mileage. Test whether the mean mileage differs.', '2t_test', ['pt_test', '2t_int', '2pz_test'], 'a quantitative variable in two independent samples, testing for a difference, so a two-sample t test'),
 ('A school randomly samples 120 students from each grade, 9 through 12, and records each student\'s favorite lunch (4 options). Do the grades differ in their lunch preferences?', 'chi_hom', ['chi_ind', '1pz_test', '2pz_test'], 'separate random samples from each grade compared on one categorical variable, so a chi-square test for homogeneity'),
 ('A random sample of 800 shoppers records both whether they used a coupon and which day of the week they shopped. Is coupon use related to the day?', 'chi_ind', ['chi_hom', '2t_test', '1pz_int'], 'one sample classified on two categorical variables, so a chi-square test for independence'),
 ('A random sample of 18 coffee shops records the price of a latte. Estimate the mean price of a latte in the city.', '1t_int', ['1t_test', '2t_int', '1pz_int'], 'one quantitative variable from one sample, estimating μ, so a one-sample t interval'),
 ('A coin is flipped 500 times to test whether it lands heads more than half the time.', '1pz_test', ['1pz_int', '2pz_test', 'chi_hom'], 'one categorical outcome (heads or not), testing p = 0.5, so a one-proportion z test'),
 ('Random samples of 30 bus riders and 30 car commuters report commute time. Estimate the difference in mean commute time.', '2t_int', ['pt_int', '2t_test', '2pz_int'], 'two independent groups and a quantitative variable, estimating μ₁ − μ₂, so a two-sample t interval'),
 ('Twenty-five patients have blood pressure measured before and after a month on a new diet. Estimate the mean change.', 'pt_int', ['2t_int', 'pt_test', '1pz_int'], 'two measurements on the same patients are paired, estimating the mean difference, so a paired t interval'),
 ('In a randomized experiment, 150 volunteers use a reminder app and 150 do not; researchers record whether each took a daily vitamin all month. Test whether the app raises the proportion.', '2pz_test', ['2pz_int', '1pz_test', '2t_test'], 'a categorical response in two randomly assigned groups, testing for a difference, so a two-proportion z test'),
]


def proc_items(level, rng):
    out = []
    order = list(range(len(SCEN)))
    random.Random('stat-audit-11').shuffle(order)  # one shuffle shared by the levels, so no scenario repeats
    start = {'cp2': 0, 'cp1': 8, 'honors': 16}[level]
    picks = [SCEN[i] for i in order[start:start + 8]]
    for n, (ctx, key, wrong, why) in enumerate(picks, 1):
        name, k, std = P[key]
        qid = f'stat-u4-s{k:02d}-{level}-c{n:02d}'
        steps = ['Ask: how many samples or groups, is the variable categorical or quantitative, are the data paired, and is the goal to estimate (interval) or to test a claim (test)?',
                 f'Here: {why}.', f'Procedure: {name.lower()}.']
        prompt = ('Which inference procedure fits this situation? ' if level != 'honors' else 'Choose the inference procedure that fits, considering the design and the goal. ') + ctx
        out.append(item(qid, f'statistical-inference-skill-{k:02d}', level, 'multiple-choice', prompt, name, steps, std, 'audit_choose_procedure', rng, [P[w][0] for w in wrong]))
    return out


def main():
    banks = lib.load()
    new = []
    for level in ('cp2', 'cp1', 'honors'):
        new += diff_items(level, random.Random('stat-audit-6-' + level))
        new += proc_items(level, random.Random('stat-audit-11-' + level))
    unit_of = {'anticipating': 'anticipating-patterns', 'statistical': 'statistical-inference'}
    for u, d in banks.items():
        d['questions'] = [q for q in d['questions'] if not re.search(r'-(d|c)\d\d$', q['id']) or 'Statistics audit 2026-11-18' not in q.get('sourceNotes', '')]
    ids = {q['id'] for u, d in banks.items() for q in d['questions']}
    for q in new:
        assert q['id'] not in ids, q['id']
        u = next(v for k, v in unit_of.items() if q['skillId'].startswith(k))
        banks[u]['questions'].append(q)
    lib.save(banks)
    import json
    added = os.path.join(os.path.dirname(__file__), 'added.json')
    ids = sorted(set(json.load(open(added)) if os.path.exists(added) else []) | {q['id'] for q in new})
    json.dump(ids, open(added, 'w'), indent=0)
    print('new items', len(new))


if __name__ == '__main__':
    main()
