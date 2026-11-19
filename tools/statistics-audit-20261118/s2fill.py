"""Statistics audit #20 (2026-11-18, batch S2): item families that bring every skill-and-level set to at least 24 items.
Each family takes a seeded random generator and a level and returns one item in context. CP2 versions are one or two
steps, CP1 two or three, Honors multi-step (a reverse problem, a comparison or a follow-up interpretation).
Conceptual families draw from scenario tables written for this batch; numeric families compute every value with scipy."""
import math
from scipy import stats
from s2common import wt, QUANT, PROP, f, g, pct, table_a, tstar, ZSTAR, mean_sd, phrase_list

FAM = {}


def fam(unit, k):
    def deco(fn):
        FAM.setdefault((unit, k), []).append(fn)
        return fn
    return deco


def R(**d):
    return d


# ====================================================================== Unit 1: Exploring Data
@fam(1, 2)
def shape_from_summary(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    kind = rng.choice(['right', 'left', 'sym'])
    med = mu
    mean = mu + {'right': 0.35, 'left': -0.35, 'sym': 0.02}[kind] * sd
    key = {'right': 'Skewed right', 'left': 'Skewed left', 'sym': 'Roughly symmetric'}[kind]
    d = max(dp, 1)
    p = (f'For a sample of {pop}, the {var} has mean {f(mean, d)} {unit} and median {f(med, d)} {unit}. '
         'Which shape is the distribution most likely to have?')
    why = {'right': 'The mean is pulled toward the long tail; here the mean is greater than the median, so the tail is on the right.',
           'left': 'The mean is pulled toward the long tail; here the mean is less than the median, so the tail is on the left.',
           'sym': 'The mean and median are almost equal, which is what we expect when the distribution is roughly symmetric.'}[kind]
    steps = [f'Compare the mean ({f(mean, d)}) with the median ({f(med, d)}).', why, f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.6.A', '1.7.F'],
             wrong=['Skewed right', 'Skewed left', 'Roughly symmetric', 'Bimodal'])


@fam(1, 2)
def outlier_resistance(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = rng.choice([8, 10, 12])
    big = rng.choice(['much larger', 'much smaller'])
    p = (f'A data set gives the {var} for {n} {pop}. One value is recorded wrongly and is {big} than all the others. '
         'Which pair of summary statistics is least affected by this error?')
    key = 'Median and IQR'
    steps = ['An extreme value pulls the mean, standard deviation and range toward it.',
             'The median and IQR depend only on the middle of the ordered data, so one extreme value barely changes them.',
             'Answer: the median and IQR are resistant.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.7.F'],
             wrong=['Mean and standard deviation', 'Mean and range', 'Range and standard deviation'])


@fam(1, 3)
def center_spread_data(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = {'cp2': rng.choice([5, 6]), 'cp1': rng.choice([6, 7]), 'honors': rng.choice([7, 8])}[lv]
    step = 10 ** -dp
    vals = sorted(round(rng.gauss(mu, sd) / step) * step for _ in range(n))
    vals = [round(v, dp) for v in vals]
    m, s = mean_sd(vals)
    data = phrase_list(vals, dp)
    intro = f'The {var} ({unit}) for a random sample of {n} {pop}: {data}.'
    if lv == 'cp2':
        rng_v = round(vals[-1] - vals[0], dp)
        if rng.random() < 0.5:
            p = intro + ' Find the mean. Round to two decimal places.'
            ans = f(m, 2)
            steps = [f'Add the values: sum = {f(sum(vals), dp)}.', f'Divide by n = {n}: x̄ = {f(sum(vals), dp)}/{n} ≈ {ans} {unit}.']
        else:
            p = intro + f' Find the range. Round to {dp} decimal places.' if dp else intro + ' Find the range.'
            ans = f(rng_v, dp)
            steps = ['Range = maximum − minimum.', f'{f(vals[-1], dp)} − {f(vals[0], dp)} = {ans} {unit}.']
        return R(fmt='short-answer', prompt=p, answer=ans, steps=steps, codes=['1.7.A'] if 'mean' in p else ['1.7.B'])
    if lv == 'cp1':
        p = intro + ' Find the sample standard deviation. Round to two decimal places.'
        dev = sum((v - m) ** 2 for v in vals)
        steps = [f'Mean: x̄ = {f(sum(vals), dp)}/{n} ≈ {f(m, 3)}.',
                 f'Sum of squared deviations: Σ(x − x̄)² ≈ {f(dev, 3)}.',
                 f'Divide by n − 1 = {n - 1} and take the square root: s = √({f(dev, 3)}/{n - 1}) ≈ {f(s, 2)} {unit}.']
        return R(fmt='short-answer', prompt=p, answer=f(s, 2), steps=steps, codes=['1.7.B'])
    a, b = rng.choice([(32, 1.8), (0, 60), (0, 2.54), (5, 0.5), (0, 1000)])
    b = rng.choice([1.5, 2, 2.5, 0.5])
    a = rng.choice([10, 20, -5, 3])
    p = (intro + f' Each value is converted with y = {g(a)} + {g(b)}x. Find the standard deviation of the converted values. '
         'Round to two decimal places.')
    steps = [f'Sample standard deviation of the original values: s ≈ {f(s, 4)}.',
             f'Adding {g(a)} shifts every value but does not change the spread; multiplying by {g(b)} multiplies the spread by {g(b)}.',
             f's_y = {g(b)} × {f(s, 4)} ≈ {f(b * s, 2)}.']
    return R(fmt='short-answer', prompt=p, answer=f(b * s, 2), steps=steps, codes=['1.7.B', '1.7.C'])


@fam(1, 3)
def choose_center(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    shape = rng.choice(['strongly skewed to the right', 'skewed to the left with two low outliers', 'roughly symmetric with no outliers'])
    sym = shape.startswith('roughly')
    key = 'Mean and standard deviation' if sym else 'Median and IQR'
    p = f'A histogram of the {var} for a sample of {pop} is {shape}. Which measures of center and spread best describe it?'
    steps = ['The mean and standard deviation are pulled by skewness and outliers; the median and IQR are resistant.',
             ('With a roughly symmetric shape and no outliers, the mean and standard deviation use every value and describe it well.' if sym
              else 'With skewness or outliers, the median and IQR describe the typical value and spread better.'),
             f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.7.F'],
             wrong=['Mean and IQR', 'Median and standard deviation', 'Mean and standard deviation', 'Median and IQR'])


@fam(1, 7)
def describe_r(rng, lv):
    pairs = [('hours studied', 'test score', 1), ('outside temperature', 'heating bill', -1), ('age of a car', 'resale value', -1),
             ('height', 'arm span', 1), ('minutes of exercise per week', 'resting pulse', -1), ('square footage of a house', 'price', 1),
             ('hours of screen time', 'hours of sleep', -1), ('shoe size', 'height', 1), ('price of a ticket', 'tickets sold', -1)]
    x, y, sign = rng.choice(pairs)
    mag = rng.choice([0.92, 0.85, 0.55, 0.47, 0.12, 0.08])
    r = sign * mag
    strength = 'strong' if mag >= 0.8 else 'moderate' if mag >= 0.4 else 'weak'
    direction = 'positive' if r > 0 else 'negative'
    key = f'A {strength}, {direction} linear association'
    p = f'For a sample of students, the correlation between {x} and {y} is r = {f(r, 2)}. Which description fits?'
    wrong = [f'A {s}, {d} linear association' for s in ['strong', 'moderate', 'weak'] for d in ['positive', 'negative']]
    rng.shuffle(wrong)
    steps = [f'The sign of r gives the direction: r {"> 0" if r > 0 else "< 0"}, so the association is {direction}.',
             f'|r| = {f(mag, 2)} is {"close to 1" if strength == "strong" else "in the middle range" if strength == "moderate" else "close to 0"}, so the linear association is {strength}.',
             f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['5.2.A'], wrong=wrong)


@fam(1, 7)
def r_units(rng, lv):
    a = rng.choice([('heights', 'inches', 'centimeters'), ('weights', 'pounds', 'kilograms'), ('temperatures', 'degrees Fahrenheit', 'degrees Celsius'),
                    ('distances', 'miles', 'kilometers'), ('times', 'minutes', 'seconds')])
    r = rng.choice([0.64, -0.71, 0.82, -0.38, 0.45])
    p = (f'The correlation between two variables is r = {f(r, 2)}. The {a[0]} were recorded in {a[1]}; a student converts them to '
         f'{a[2]} and recomputes the correlation. What is the new value of r?')
    steps = ['Correlation has no units: it is computed from standardized values (z-scores).',
             'Changing units multiplies and/or shifts every value, which leaves the z-scores (and so r) unchanged.',
             f'r = {f(r, 2)}.']
    return R(fmt='short-answer', prompt=p, answer=f(r, 2), steps=steps, codes=['5.2.A'])


# ====================================================================== Unit 2: Sampling and Experimentation
STUDIES = [
    ('A school newspaper surveys 120 randomly chosen students from the 1,800 students at the school and finds that 41% would buy a yearbook.',
     'All 1,800 students at the school', 'The 120 students surveyed', '41%', 'the proportion of all 1,800 students who would buy a yearbook'),
    ('A quality inspector tests 50 randomly chosen light bulbs from a shipment of 4,000 and finds a mean life of 1,180 hours.',
     'All 4,000 bulbs in the shipment', 'The 50 bulbs tested', '1,180 hours', 'the mean life of all 4,000 bulbs'),
    ('A city selects 400 households at random from its 52,000 households and finds that 63% recycle every week.',
     'All 52,000 households in the city', 'The 400 households selected', '63%', 'the proportion of all households that recycle every week'),
    ('A farmer weighs 30 randomly chosen pumpkins from a field of 2,500 and finds a mean weight of 14.2 pounds.',
     'All 2,500 pumpkins in the field', 'The 30 pumpkins weighed', '14.2 pounds', 'the mean weight of all pumpkins in the field'),
    ('A researcher contacts 1,000 randomly chosen adults in a state; 58% say they exercise at least three times a week.',
     'All adults in the state', 'The 1,000 adults contacted', '58%', 'the proportion of all adults in the state who exercise at least three times a week'),
    ('A coffee chain records the wait time of 80 randomly chosen orders from last month’s 24,000 orders; the mean is 4.6 minutes.',
     'All 24,000 orders from last month', 'The 80 orders recorded', '4.6 minutes', 'the mean wait time of all last month’s orders'),
    ('A biologist tags 60 randomly caught trout from a lake and finds that 15% carry a parasite.',
     'All trout in the lake', 'The 60 trout caught', '15%', 'the proportion of all trout in the lake that carry the parasite'),
    ('An airline checks 200 randomly chosen bags from the 9,000 bags checked on one day; 3% are overweight.',
     'All 9,000 bags checked that day', 'The 200 bags checked', '3%', 'the proportion of the day’s bags that are overweight'),
    ('A teacher asks 25 randomly chosen students from the 600 in her grade how many hours they slept last night; the mean is 6.8 hours.',
     'All 600 students in the grade', 'The 25 students asked', '6.8 hours', 'the mean hours of sleep last night for all 600 students'),
]


@fam(2, 1)
def population_sample(rng, lv):
    desc, pop, samp, stat, par = rng.choice(STUDIES)
    ask = rng.choice(['population', 'sample']) if lv != 'honors' else rng.choice(['population', 'sample', 'parameter'])
    if ask == 'population':
        p, key, wrong = desc + ' What is the population?', pop, [samp, 'The ' + stat + ' found in the study', 'Everyone who reads the results']
        steps = ['The population is the entire group we want information about.', f'Here that is: {pop.lower()}.']
    elif ask == 'sample':
        p, key, wrong = desc + ' What is the sample?', samp, [pop, 'The ' + stat + ' found in the study', 'Everyone who reads the results']
        steps = ['The sample is the part of the population we actually collect data from.', f'Here that is: {samp.lower()}.']
    else:
        p = desc + ' Which describes the parameter of interest?'
        key = par[0].upper() + par[1:]
        wrong = [f'The value {stat} found in the sample', samp, pop]
        steps = ['A parameter is a number that describes the population; a statistic describes the sample.',
                 f'The parameter is {par}; the value {stat} is a statistic that estimates it.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.2.A'], wrong=wrong)


@fam(2, 1)
def parameter_or_statistic(rng, lv):
    desc, pop, samp, stat, par = rng.choice(STUDIES)
    p = desc + f' Is the value {stat} a parameter or a statistic?'
    key = 'A statistic, because it describes the sample'
    steps = ['Ask whether the number comes from the whole population or only from the sample.',
             f'{stat} was computed from {samp[0].lower() + samp[1:]}, so it is a statistic.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.2.A'],
             wrong=['A parameter, because it describes the population', 'A parameter, because the sample was random',
                    'A statistic, because it describes the population'])


CENSUS = [('The principal records the attendance of every student enrolled at the school.', 'Census'),
          ('A town counts every streetlight it owns to plan repairs.', 'Census'),
          ('A coach measures the vertical jump of all 14 players on the team.', 'Census'),
          ('A company asks 300 of its 12,000 customers, chosen at random, to rate its service.', 'Sample survey'),
          ('A news site polls 1,200 randomly selected registered voters before an election.', 'Sample survey'),
          ('A store manager checks the price tag on every item in one aisle of 85 items.', 'Census'),
          ('A health department tests the water at 20 randomly chosen homes in a city of 30,000 homes.', 'Sample survey')]


@fam(2, 1)
def census_or_sample(rng, lv):
    desc, key = rng.choice(CENSUS)
    extra = '' if lv == 'cp2' else ' (Assume the group named is the whole population of interest.)'
    p = desc + ' Is this a census or a sample survey?' + extra
    steps = ['A census collects data from every individual in the population; a sample survey uses part of it.',
             f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.10.B'],
             wrong=['Census', 'Sample survey', 'Experiment', 'Observational study of a convenience sample'])


METHODS = [
    ('A principal puts the names of all 1,200 students in a computer, assigns each a number, and uses a random number generator to choose 60 different numbers.', 'Simple random sample'),
    ('A researcher separates a city’s voters into Democrats, Republicans and independents and randomly selects 100 voters from each group.', 'Stratified random sample'),
    ('A school randomly selects 5 of its 40 homerooms and surveys every student in those homerooms.', 'Cluster sample'),
    ('A store manager picks a random number from 1 to 20, starts with that customer, and then surveys every 20th customer.', 'Systematic random sample'),
    ('A reporter interviews the first 30 people who walk past her outside a coffee shop.', 'Convenience sample'),
    ('A website asks visitors to click a link if they want to answer a survey about the site.', 'Voluntary response sample'),
    ('A farmer divides an orchard into its 4 varieties of apple tree and randomly chooses 10 trees of each variety to inspect.', 'Stratified random sample'),
    ('An airline randomly selects 8 of its 150 flights on a day and surveys every passenger on those 8 flights.', 'Cluster sample'),
    ('A teacher numbers the 32 students in her class and uses a table of random digits to choose 6 of them.', 'Simple random sample'),
    ('A factory picks a random starting point among the first 50 phones off the line and then inspects every 50th phone.', 'Systematic random sample'),
    ('A radio host asks listeners to call in to give their opinion of a new law.', 'Voluntary response sample'),
    ('A survey company randomly selects 20 apartment buildings in a city and interviews every household in them.', 'Cluster sample'),
]


@fam(2, 2)
def name_method(rng, lv):
    desc, key = rng.choice(METHODS)
    p = desc + ' Which sampling method is this?'
    others = ['Simple random sample', 'Stratified random sample', 'Cluster sample', 'Systematic random sample', 'Convenience sample', 'Voluntary response sample']
    wrong = [o for o in others if o != key]
    rng.shuffle(wrong)
    reason = {'Simple random sample': 'every group of that size has the same chance to be chosen',
              'Stratified random sample': 'the population is split into similar groups (strata) and a random sample is taken from every group',
              'Cluster sample': 'the population is split into groups (clusters), some clusters are chosen at random, and everyone in them is used',
              'Systematic random sample': 'a random start is followed by every kth individual',
              'Convenience sample': 'individuals who are easy to reach are chosen, with no random selection',
              'Voluntary response sample': 'people choose themselves by responding to a general invitation'}[key]
    steps = ['Look at how individuals are chosen: is chance used, and is the population split into groups first?',
             f'Here {reason}.', f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.11.A'], wrong=wrong)


@fam(2, 2)
def strata_allocation(rng, lv):
    names = rng.choice([('freshmen', 'sophomores', 'juniors', 'seniors'), ('full-time workers', 'part-time workers', 'seasonal workers', 'contract workers'),
                        ('downtown stores', 'north-side stores', 'south-side stores', 'east-side stores'), ('beginners', 'intermediate players', 'advanced players', 'experts')])
    unit = rng.choice([25, 50])
    k = rng.choice([4, 5, 8, 10])
    shares = rng.choice([(6, 5, 5, 4), (4, 4, 3, 1), (7, 6, 4, 3), (3, 3, 2, 2), (5, 4, 4, 2)])
    tot_share = sum(shares)
    n_sample = k * tot_share
    sizes = [s * unit * k for s in shares]  # so each stratum size is divisible
    N = sum(sizes)
    i = rng.randrange(4)
    ans = shares[i] * k
    who = {'freshmen': 'students', 'full-time workers': 'employees', 'downtown stores': 'stores', 'beginners': 'club members'}[names[0]]
    p = (f'A population of {N:,} {who} is made up of {sizes[0]:,} {names[0]}, {sizes[1]:,} {names[1]}, {sizes[2]:,} {names[2]} and {sizes[3]:,} {names[3]}. '
         f'A stratified random sample of {n_sample} is allocated in proportion to the size of each group. How many {names[i]} are in the sample?')
    steps = [f'Fraction of the population in the {names[i]} group: {sizes[i]:,}/{N:,} = {g(sizes[i] / N)}.',
             f'Multiply by the sample size: {g(sizes[i] / N)} × {n_sample} = {ans}.',
             f'Then choose {ans} {names[i]} at random from that group.']
    return R(fmt='short-answer', prompt=p, answer=str(ans), steps=steps, codes=['1.11.B'])


BIAS = [
    ('A phone survey calls only landline numbers to estimate the proportion of adults who use streaming services.', 'Undercoverage', 'underestimate'),
    ('A survey mailed to 2,000 randomly chosen residents about a new tax gets back only 410 replies.', 'Nonresponse bias', None),
    ('A survey asks, "Don’t you agree that the beautiful old library should be saved from demolition?"', 'Response bias from a leading question', 'overestimate'),
    ('A teacher asks students to raise their hands if they cheated on a test.', 'Response bias from a sensitive question', 'underestimate'),
    ('A TV show asks viewers to text in whether they support a new stadium.', 'Voluntary response bias', None),
    ('A gym surveys people at the gym at 6 a.m. to estimate how often adults in the town exercise.', 'Bias from a convenience sample', 'overestimate'),
    ('An online poll about internet access is posted on a website, so only people already online can answer.', 'Undercoverage', 'overestimate'),
    ('A health survey asks adults how many servings of vegetables they eat, and many report more than they really eat.', 'Response bias', 'overestimate'),
    ('A survey of a town’s residents uses a list of homeowners, leaving out renters.', 'Undercoverage', None),
    ('Of 500 randomly selected parents asked about school lunches, 340 never answer the email.', 'Nonresponse bias', None),
    ('A survey about a town’s bus service is handed out only to people riding the bus.', 'Bias from a convenience sample', 'overestimate'),
    ('An interviewer in uniform asks drivers whether they always obey the speed limit.', 'Response bias', 'overestimate'),
    ('A magazine invites readers to mail in their opinion about a celebrity scandal.', 'Voluntary response bias', None),
    ('A survey of college students’ study habits uses the list of students living in campus housing only.', 'Undercoverage', None),
    ('Of 1,000 randomly chosen voters called in the afternoon, 620 do not pick up.', 'Nonresponse bias', None),
    ('A survey asks, "How much did you donate to charity last year?" in a face-to-face interview.', 'Response bias', 'overestimate'),
]
BIAS_FIX = [
    ('A survey asks, "Don’t you agree the city should fix the dangerous potholes on Main Street?"', 'Reword the question neutrally, e.g., "Should the city spend money repairing Main Street?"'),
    ('A phone survey calls only landlines to study streaming habits.', 'Include cell phone numbers in the sampling frame'),
    ('A mailed survey gets back only 25% of the forms.', 'Follow up with people who did not respond'),
    ('A school asks students to raise their hands if they have ever cheated.', 'Use anonymous written responses'),
    ('A website asks visitors to vote on whether the town needs a new library.', 'Take a random sample of all residents instead of letting people choose to respond'),
    ('A reporter surveys shoppers at one mall on a weekday morning about local spending.', 'Use a random sample of residents from a list of all households'),
    ('A survey of workers’ opinions about the boss is collected in person by the boss.', 'Have a third party collect anonymous responses'),
    ('A survey of a town’s households uses a list of homeowners only.', 'Use a list that includes renters as well as homeowners'),
]


@fam(2, 3)
def bias_fix(rng, lv):
    desc, key = rng.choice(BIAS_FIX)
    others = [b for d, b in BIAS_FIX if b != key]
    rng.shuffle(others)
    wrong = ['Increase the sample size without changing anything else'] + others[:2]
    p = desc + ' Which change would best reduce the bias?'
    steps = ['First identify the source of bias: who is selected, who responds, or how people answer.',
             'A larger sample does not remove bias; the fix must address that source.', f'Answer: {key[0].lower() + key[1:]}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.12.A', '1.11.B'], wrong=wrong)


@fam(2, 3)
def name_bias(rng, lv):
    desc, key, _ = rng.choice(BIAS)
    p = desc + ' Which type of bias is most likely?'
    pool = ['Undercoverage', 'Nonresponse bias', 'Response bias', 'Voluntary response bias', 'Bias from a convenience sample',
            'Response bias from a leading question', 'Response bias from a sensitive question']
    base = key.split(' from ')[0] if key.startswith('Response bias') else key
    wrong = [w for w in pool if not w.startswith(base.split()[0]) and w != key]
    rng.shuffle(wrong)
    expl = {'Undercoverage': 'some members of the population have no chance of being chosen',
            'Nonresponse bias': 'many people chosen for the sample do not respond, and they may differ from those who do',
            'Response bias': 'people give answers that are not true, for example to look good',
            'Voluntary response bias': 'people choose themselves, and those with strong opinions are more likely to respond',
            'Bias from a convenience sample': 'the people who are easy to reach are not representative of the population',
            'Response bias from a leading question': 'the wording pushes people toward one answer',
            'Response bias from a sensitive question': 'people are unlikely to admit to the behavior in public'}[key]
    steps = ['Decide whether the problem is who is selected (undercoverage, convenience, voluntary response), who answers (nonresponse) or how they answer (response bias).',
             f'Here {expl}.', f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.12.A'], wrong=wrong)


@fam(2, 3)
def bias_direction(rng, lv):
    desc, key, d = rng.choice([b for b in BIAS if b[2]])
    target = {'underestimate': 'too low', 'overestimate': 'too high'}[d]
    p = desc + ' Is the estimate from this survey more likely to be too high or too low? Choose the best answer.'
    ans = f'Too {target.split()[1]}, because of {key[0].lower() + key[1:]}'
    other = 'low' if target.endswith('high') else 'high'
    wrong = [f'Too {other}, because of {key[0].lower() + key[1:]}', 'Neither, because a large sample removes bias',
             'Neither, because random selection removes all bias']
    steps = [f'Identify the bias: {key.lower()}.',
             f'Think about who is missed or how answers are distorted: it pushes the estimate {target}.',
             'A larger sample does not fix bias; it only reduces variability.']
    return R(fmt='multiple-choice', prompt=p, answer=ans, steps=steps, codes=['1.12.A'], wrong=wrong)


OBS = [
    ('Researchers ask 2,000 adults how much coffee they drink and measure their blood pressure.', 'Observational study', 'amount of coffee', 'blood pressure'),
    ('A teacher randomly assigns half her students to use flashcards and half to use a practice app, then compares quiz scores.', 'Experiment', 'study method', 'quiz score'),
    ('Doctors review records of 5,000 patients to compare heart disease rates for smokers and nonsmokers.', 'Observational study', 'smoking status', 'heart disease'),
    ('A farmer randomly assigns 40 plots to two fertilizers and measures the corn yield of each plot.', 'Experiment', 'type of fertilizer', 'corn yield'),
    ('A study follows 800 teenagers for three years and records their screen time and their grades.', 'Observational study', 'screen time', 'grades'),
    ('Volunteers are randomly assigned to sleep 5 or 8 hours, then take a reaction-time test.', 'Experiment', 'hours of sleep', 'reaction time'),
    ('A survey compares the reading scores of students who own an e-reader with those who do not.', 'Observational study', 'owning an e-reader', 'reading score'),
    ('A company randomly shows half of its website visitors a green button and half a blue button and records who clicks.', 'Experiment', 'button color', 'whether the visitor clicks'),
    ('Researchers compare the asthma rates of children living near highways with those living farther away.', 'Observational study', 'distance from a highway', 'asthma'),
    ('Mice are randomly assigned to a high-sugar or normal diet, and their weight gain is measured after 6 weeks.', 'Experiment', 'diet', 'weight gain'),
]


@fam(2, 4)
def obs_or_exp(rng, lv):
    desc, key, ex, resp = rng.choice(OBS)
    if lv == 'honors' and rng.random() < 0.5:
        p = desc + ' Can this study show that the ' + ex + ' causes a change in ' + resp + '?'
        ans = ('Yes, because the treatments were randomly assigned' if key == 'Experiment'
               else 'No, because no treatment was assigned, so other variables could explain the association')
        wrong = (['No, because the sample was not large enough', 'No, because experiments can never show cause and effect',
                  'Yes, because the association is strong'] if key == 'Experiment' else
                 ['Yes, because the sample is large', 'Yes, because the association is strong', 'Yes, because the data are numerical'])
        steps = [f'This is {"an experiment" if key == "Experiment" else "an observational study"}.',
                 'Only a randomized experiment can show cause and effect, because random assignment balances other variables between groups.',
                 f'Answer: {ans[0].lower() + ans[1:]}.']
        return R(fmt='multiple-choice', prompt=p, answer=ans, steps=steps, codes=['1.10.C', '1.13.D'], wrong=wrong)
    p = desc + ' Is this an observational study or an experiment?'
    steps = ['In an experiment, the researchers impose a treatment; in an observational study they only measure.',
             ('The researchers assigned the treatments, so it is an experiment.' if key == 'Experiment'
              else 'Nobody was assigned a treatment; the researchers only recorded what happened, so it is an observational study.')]
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.10.C', '1.10.D'],
             wrong=['Observational study', 'Experiment', 'Census', 'Sample survey'])


@fam(2, 4)
def explanatory_response(rng, lv):
    desc, key, ex, resp = rng.choice(OBS)
    ask = rng.choice(['explanatory', 'response'])
    ans = ex if ask == 'explanatory' else resp
    p = desc + f' What is the {ask} variable?'
    other = resp if ask == 'explanatory' else ex
    wrong = [other, 'the number of subjects', 'the researchers’ conclusion']
    ans = ans[0].upper() + ans[1:]
    wrong = [w[0].upper() + w[1:] for w in wrong]
    steps = ['The explanatory variable may help explain or predict changes in the response variable.',
             f'Explanatory: {ex}; response: {resp}.']
    return R(fmt='multiple-choice', prompt=p, answer=ans, steps=steps, codes=['1.2.A'], wrong=wrong)


FACTORS = [('brand of fertilizer', 'brands', 'watering schedule', 'schedules', 'tomato plants', 'yield'),
           ('type of music', 'types', 'volume level', 'volume levels', 'students', 'number of words recalled'),
           ('dose of a drug', 'doses', 'time of day it is taken', 'times', 'patients', 'blood pressure'),
           ('oven temperature', 'temperatures', 'baking time', 'baking times', 'batches of cookies', 'taste rating'),
           ('type of paper', 'types', 'wing design', 'designs', 'paper airplanes', 'flight distance'),
           ('amount of sunlight', 'amounts', 'type of soil', 'soil types', 'bean plants', 'height after 3 weeks')]


@fam(2, 5)
def count_treatments(rng, lv):
    f1, f1s, f2, f2s, units, resp = rng.choice(FACTORS)
    a, b = rng.choice([2, 3, 4]), rng.choice([2, 3])
    reps = rng.choice([4, 5, 6, 8])
    if lv == 'cp2':
        p = (f'An experiment uses {units} to study {a} {f1s} ({f1}) and {b} {f2s} ({f2}). Every combination is a treatment. How many treatments are there?')
        ans = a * b
        steps = [f'Each of the {a} levels of {f1} is combined with each of the {b} levels of {f2}.', f'{a} × {b} = {ans} treatments.']
    else:
        p = (f'An experiment uses {units} to study {a} {f1s} ({f1}) and {b} {f2s} ({f2}), with {reps} {units} randomly assigned to each treatment. '
             'How many experimental units are needed?')
        ans = a * b * reps
        steps = [f'Treatments: {a} × {b} = {a * b} combinations of the two factors.',
                 f'Replication: {reps} units per treatment.', f'{a * b} × {reps} = {ans} {units}.']
    return R(fmt='short-answer', prompt=p, answer=str(ans), steps=steps, codes=['1.13.A'])


@fam(2, 5)
def experiment_parts(rng, lv):
    f1, f1s, f2, f2s, units, resp = rng.choice(FACTORS)
    ask = rng.choice(['units', 'response', 'factor'])
    p = f'An experiment randomly assigns {units} to combinations of {f1} and {f2} and measures the {resp}. '
    if ask == 'units':
        p += 'What are the experimental units?'
        ans, wrong = units[0].upper() + units[1:], [resp[0].upper() + resp[1:], f'The levels of {f1}', 'The researchers']
    elif ask == 'response':
        p += 'What is the response variable?'
        ans, wrong = resp[0].upper() + resp[1:], [units[0].upper() + units[1:], f1[0].upper() + f1[1:], 'The treatments']
    else:
        p += 'Which list gives the factors?'
        ans, wrong = f'{f1[0].upper() + f1[1:]} and {f2}', [f'{units[0].upper() + units[1:]} and {resp}', f'{resp[0].upper() + resp[1:]} only', f'{units[0].upper() + units[1:]} only']
    steps = ['Experimental units receive the treatments; factors are the explanatory variables the researchers set; the response is what is measured.',
             f'Units: {units}. Factors: {f1}, {f2}. Response: {resp}.']
    return R(fmt='multiple-choice', prompt=p, answer=ans, steps=steps, codes=['1.13.A'], wrong=wrong)


@fam(2, 5)
def design_diagram_counts(rng, lv):
    units, total, trts = rng.choice([('volunteers', 60, ['Drug A', 'Drug B', 'Placebo']), ('plots of land', 48, ['Fertilizer X', 'Fertilizer Y']),
                                     ('students', 90, ['App', 'Flashcards', 'Textbook']), ('dogs', 40, ['Diet 1', 'Diet 2', 'Diet 3', 'Diet 4']),
                                     ('batteries', 72, ['Brand A', 'Brand B', 'Brand C']), ('tomato plants', 36, ['Red light', 'Blue light'])])
    resp = {'volunteers': 'Compare blood pressure', 'plots of land': 'Compare yield', 'students': 'Compare test scores', 'dogs': 'Compare weight gain',
            'batteries': 'Compare hours of use', 'tomato plants': 'Compare plant height'}[units]
    per = total // len(trts)
    p = (f'The diagram shows the design of a completely randomized experiment with {total} {units}. '
         'How many experimental units are assigned to each treatment?')
    steps = [f'The {total} {units} are split at random into {len(trts)} equal groups, one for each treatment.',
             f'{total} ÷ {len(trts)} = {per} {units} per treatment.']
    spec = {'kind': 'crd', 'units': units, 'total': total, 'groups': [(t, per) for t in trts], 'response': resp}
    return R(fmt='short-answer', prompt=p, answer=str(per), steps=steps, codes=['1.13.B'], design=spec)


CONFOUND = [
    ('Students who eat breakfast have higher grades than students who skip it.', 'Family income, which may affect both eating breakfast and grades'),
    ('Cities with more police officers have more crimes.', 'City population, which increases both the number of officers and the number of crimes'),
    ('People who carry a lighter are more likely to get lung cancer.', 'Smoking, which is linked to carrying a lighter and to lung cancer'),
    ('Ice cream sales and drowning deaths rise together.', 'Hot weather, which increases both ice cream sales and swimming'),
    ('Students who take music lessons score higher on math tests.', 'Parents’ education, which may affect both music lessons and math scores'),
    ('Patients who chose a new surgery recovered faster than those who chose the standard surgery.', 'Overall health, since healthier patients may choose the new surgery and also recover faster'),
    ('Houses with swimming pools have higher electricity bills.', 'House size, since larger houses are more likely to have pools and use more electricity'),
    ('Children with bigger shoe sizes have higher reading scores.', 'Age, since older children have bigger feet and read better'),
    ('Towns with more churches have more bars.', 'Town population, since bigger towns have more of both'),
    ('People who take vitamins report fewer colds.', 'Overall health habits, since people who take vitamins may also sleep and exercise more'),
    ('Students who sit in the front row earn higher grades.', 'Motivation, since motivated students may choose the front row and also study more'),
    ('Hospitals with more doctors have more patient deaths.', 'Hospital size, since larger hospitals have more doctors and more patients'),
]


@fam(2, 6)
def name_confounder(rng, lv):
    obs, key = rng.choice(CONFOUND)
    others = [c[1] for c in CONFOUND if c[1] != key]
    rng.shuffle(others)
    p = 'An observational study finds: ' + obs + ' Which is the most plausible confounding variable?'
    steps = ['A confounding variable is related to the explanatory variable and also affects the response, so its effect cannot be separated.',
             f'Here: {key[0].lower() + key[1:]}.', 'Only a randomized experiment would balance it between groups.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.A', '1.10.D'], wrong=others)


BLIND = [
    ('Neither the patients nor the nurses who measure their pain know who received the real drug.', 'Double-blind'),
    ('The subjects do not know which energy drink they got, but the researcher who times their run does know.', 'Single-blind'),
    ('The judges tasting the cookies do not know which recipe each came from, but the bakers who serve them do not interact with the judges or record results.', 'Single-blind'),
    ('Everyone in the study, including the subjects and the doctors who evaluate them, knows which treatment each subject received.', 'Not blind'),
    ('Students do not know whether their practice app has the new feature, and the teacher who grades their tests does not know either.', 'Double-blind'),
    ('Dogs are fed one of two diets; the vet who weighs the dogs is told which diet each dog ate.', 'Not blind'),
    ('Patients receive either acupuncture or a sham treatment and are not told which; the therapist who gives it knows, but a separate nurse who records pain does not.', 'Double-blind'),
    ('Runners know which shoe they are wearing, but the timers who record their times do not.', 'Single-blind'),
    ('Volunteers know whether they drank caffeinated coffee, and so does the person who scores their memory test.', 'Not blind'),
    ('Plants get either a new fertilizer or water in identical bottles, and the gardener who measures growth does not know which.', 'Single-blind'),
]


@fam(2, 6)
def blinding(rng, lv):
    desc, key = rng.choice(BLIND)
    p = 'In an experiment: ' + desc + ' How is this experiment best described?'
    steps = ['Single-blind: either the subjects or the people who evaluate them do not know the treatment. Double-blind: neither knows.',
             f'Here: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.A'],
             wrong=['Double-blind', 'Single-blind', 'Not blind', 'Matched pairs'])


@fam(2, 6)
def random_assignment_confounding(rng, lv):
    trt, units, var = rng.choice([('a new teaching method', 'students', 'prior achievement'), ('a heart medicine', 'patients', 'age'), ('a new fertilizer', 'plots', 'soil quality'),
                                  ('an energy drink', 'athletes', 'fitness level'), ('a reading app', 'children', 'reading at home'), ('a sleep routine', 'adults', 'stress at work')])
    p = f'In an experiment on {trt}, the researchers randomly assign the {units} to the treatment and control groups. How does random assignment help with a variable such as {var}?'
    key = f'It tends to balance {var} between the groups, so it is not confounded with the treatment'
    steps = [f'If {units} chose their own group, {var} could differ between the groups and also affect the response.',
             f'Random assignment makes the groups similar on average in {var} (and other variables), so differences in the response can be attributed to {trt}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.A', '1.13.D'],
             wrong=[f'It removes all variation in {var}', f'It makes the results generalize to all {units}', 'It makes the experiment double-blind'])


@fam(2, 6)
def placebo_purpose(rng, lv):
    who, trt = rng.choice([('patients with headaches', 'a new pain reliever'), ('adults with trouble sleeping', 'a herbal sleep aid'),
                           ('students before a test', 'an energy supplement'), ('athletes', 'a recovery drink'), ('people with allergies', 'a new nasal spray')])
    p = f'An experiment on {trt} for {who} gives one group a placebo that looks identical. Why use a placebo group?'
    key = 'To separate the effect of the treatment from the effect of simply receiving a treatment'
    steps = ['People can improve just because they believe they are being treated (the placebo effect).',
             'A placebo group experiences everything except the active treatment, so a difference between groups can be attributed to the treatment.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.A'],
             wrong=['To make the groups larger so the study has more power', 'To make sure the subjects were randomly selected',
                    'To remove the need for random assignment'])


DESIGNS = [
    ('Each of 20 runners runs one mile in each of two shoe types on different days, with the order decided by a coin flip.', 'Matched pairs design'),
    ('Volunteers are separated into men and women, and within each group they are randomly assigned to two diets.', 'Randomized block design'),
    ('Sixty plants are randomly assigned to three fertilizers, 20 per fertilizer.', 'Completely randomized design'),
    ('Twins are split so that one twin gets each of two tutoring programs, chosen at random.', 'Matched pairs design'),
    ('Fields are grouped by soil type, and within each soil type the plots are randomly assigned to two seed varieties.', 'Randomized block design'),
    ('Ninety students are randomly assigned to study with music, with white noise or in silence.', 'Completely randomized design'),
    ('Each driver tests both braking systems in a random order on a closed track.', 'Matched pairs design'),
    ('Patients are grouped by age (under 50, 50 and over), and within each age group they are randomly assigned to a drug or a placebo.', 'Randomized block design'),
    ('Forty students are paired by their last test score, and a coin flip decides which student in each pair uses the new app.', 'Matched pairs design'),
    ('Seventy-five volunteers are randomly assigned to one of three exercise plans.', 'Completely randomized design'),
    ('Cows are separated by breed, and within each breed they are randomly assigned to two feeds.', 'Randomized block design'),
    ('Each of 18 tasters rates both cola recipes, in an order decided at random.', 'Matched pairs design'),
    ('Sixty cookies are randomly assigned to be baked at 325°F, 350°F or 375°F.', 'Completely randomized design'),
    ('Classrooms are grouped by grade level, and within each grade the classrooms are randomly assigned to a new or old curriculum.', 'Randomized block design'),
]


@fam(2, 7)
def why_pairs(rng, lv):
    units, trt, var = rng.choice([('runners', 'two brands of shoes', 'natural running ability'), ('typists', 'two keyboards', 'typing skill'), ('drivers', 'two brake designs', 'reaction time'),
                                  ('students', 'two study methods', 'prior knowledge'), ('tasters', 'two recipes', 'personal taste')])
    p = f'An experiment compares {trt} by having each of the {units} use both, in random order. Why is this matched pairs design better than a completely randomized design here?'
    key = f'Each unit serves as its own control, so differences in {var} do not hide the treatment effect'
    steps = [f'{units[0].upper() + units[1:]} differ a lot in {var}, which adds variability to the response.',
             'Comparing the two treatments within the same unit removes that variability, so a treatment difference is easier to detect.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.C'],
             wrong=['It needs no random assignment', f'It lets the results generalize to all {units}', 'It makes the study double-blind'])



@fam(2, 7)
def name_design(rng, lv):
    desc, key = rng.choice(DESIGNS)
    p = desc + ' Which design is this?'
    steps = ['Completely randomized: all units are randomly assigned to treatments. Randomized block: units are first grouped by a variable, then randomized within each block. '
             'Matched pairs: units come in similar pairs (or each unit gets both treatments in random order).',
             f'Answer: {key.lower()}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.B'],
             wrong=['Completely randomized design', 'Randomized block design', 'Matched pairs design', 'Stratified random sample'])


@fam(2, 7)
def design_diagram_name(rng, lv):
    kind = rng.choice(['crd', 'block', 'pairs'])
    if kind == 'crd':
        units, total, trts = rng.choice([('students', 80, ['Method A', 'Method B']), ('mice', 45, ['Diet 1', 'Diet 2', 'Diet 3']), ('volunteers', 120, ['Drug', 'Placebo']),
                                         ('plants', 36, ['Red light', 'Blue light', 'White light']), ('patients', 50, ['New cream', 'Placebo cream']), ('athletes', 60, ['Drink A', 'Drink B', 'Water'])])
        spec = {'kind': 'crd', 'units': units, 'total': total, 'groups': [(t, total // len(trts)) for t in trts], 'response': 'Compare the response'}
        key = 'Completely randomized design'
    elif kind == 'block':
        units, blocks, trts = rng.choice([('patients', [('Men', 40), ('Women', 60)], ['Drug', 'Placebo']), ('plots', [('Sandy soil', 24), ('Clay soil', 24)], ['Seed A', 'Seed B']),
                                          ('students', [('Juniors', 50), ('Seniors', 50)], ['App', 'Textbook']), ('cows', [('Holstein', 30), ('Jersey', 20)], ['Feed X', 'Feed Y']),
                                          ('volunteers', [('Under 40', 44), ('40 and over', 36)], ['Program', 'Control']), ('cars', [('Compact', 16), ('SUV', 16)], ['Additive', 'No additive'])])
        spec = {'kind': 'block', 'units': units, 'blocks': blocks, 'treatments': trts, 'response': 'Compare within each block'}
        key = 'Randomized block design'
    else:
        units, n, trts = rng.choice([('runners', 20, ['Shoe A', 'Shoe B']), ('drivers', 30, ['Brake 1', 'Brake 2']), ('typists', 16, ['Keyboard A', 'Keyboard B']),
                                     ('tasters', 24, ['Recipe 1', 'Recipe 2']), ('gamers', 18, ['Mouse A', 'Mouse B']), ('swimmers', 12, ['Suit A', 'Suit B'])])
        spec = {'kind': 'pairs', 'units': units, 'n': n, 'treatments': trts, 'response': 'Compare the differences'}
        key = 'Matched pairs design'
    p = f'A researcher plans an experiment with {spec.get("total", spec.get("n", sum(n for _, n in spec.get("blocks", []))))} {units}. Which experimental design does the diagram show?'
    steps = ['Look at how units reach the treatments: randomized all together, randomized within blocks, or each unit (or pair) gets both treatments in random order.',
             {'crd': 'All units are randomly assigned to the treatment groups in one step, so it is completely randomized.',
              'block': 'Units are first split into blocks and then randomized within each block, so it is a randomized block design.',
              'pairs': 'Each unit receives both treatments in a random order and the differences are compared, so it is a matched pairs design.'}[kind]]
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.B'],
             wrong=['Completely randomized design', 'Randomized block design', 'Matched pairs design', 'Stratified random sample'], design=spec)


@fam(2, 7)
def why_block(rng, lv):
    var, units = rng.choice([('gender', 'patients'), ('soil type', 'plots'), ('grade level', 'students'), ('age group', 'volunteers'), ('breed size', 'dogs')])
    p = f'An experiment blocks its {units} by {var} before randomly assigning treatments. What is the main benefit of blocking?'
    key = f'It reduces variability in the response caused by {var}, making treatment differences easier to detect'
    steps = [f'Units in the same block are similar in {var}, so differences within a block come mostly from the treatments.',
             'Comparing treatments within blocks removes the variation between blocks, which makes the comparison more precise.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.13.C'],
             wrong=[f'It lets the results generalize to all values of {var}', 'It replaces the need for random assignment', 'It makes the study double-blind'])


SCOPE = [
    ('Researchers randomly select 500 adults in a state and randomly assign each to a morning or evening workout plan.', True, True),
    ('A teacher randomly assigns the 30 students in her class to two review methods.', False, True),
    ('A poll randomly selects 1,000 voters in a city and records their age and opinion of a new law.', True, False),
    ('Volunteers who answered a newspaper ad are randomly assigned to a new diet or their usual diet.', False, True),
    ('A researcher surveys the first 200 shoppers at a mall about their sleep and exercise habits.', False, False),
    ('A school randomly selects 120 of its students and compares the GPAs of those who play sports with those who do not.', True, False),
    ('A company randomly selects 300 of its 5,000 customers and randomly assigns half to receive a discount email.', True, True),
]


@fam(2, 8)
def scope_of_inference(rng, lv):
    desc, sel, asg = rng.choice(SCOPE)
    key = {(True, True): 'Cause and effect, for the whole population sampled', (False, True): 'Cause and effect, but only for subjects like those in the study',
           (True, False): 'An association that generalizes to the population, but not cause and effect',
           (False, False): 'An association for these individuals only; neither generalization nor cause and effect'}[(sel, asg)]
    p = desc + ' Which conclusion does this design support?'
    wrong = [v for k, v in {(True, True): 'Cause and effect, for the whole population sampled', (False, True): 'Cause and effect, but only for subjects like those in the study',
                            (True, False): 'An association that generalizes to the population, but not cause and effect',
                            (False, False): 'An association for these individuals only; neither generalization nor cause and effect'}.items() if v != key]
    steps = [f'Random selection? {"Yes" if sel else "No"}: {"results generalize to the population" if sel else "results apply only to individuals like these"}.',
             f'Random assignment? {"Yes" if asg else "No"}: {"differences can be attributed to the treatment (cause and effect)" if asg else "only an association can be concluded"}.',
             f'Answer: {key[0].lower() + key[1:]}.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.10.E', '1.13.D'], wrong=wrong)


@fam(2, 8)
def association_causation(rng, lv):
    x, y = rng.choice([('hours of TV watched', 'body weight'), ('number of books at home', 'reading score'), ('coffee consumption', 'lifespan'),
                       ('owning a pet', 'blood pressure'), ('taking vitamin D supplements', 'number of colds'), ('using a standing desk', 'productivity')])
    r = rng.choice([0.42, 0.58, -0.37, -0.51, 0.64])
    p = (f'A large observational study finds a correlation of r = {f(r, 2)} between {x} and {y}. A headline says "{x[0].upper() + x[1:]} affects {y}." '
         'What is the best response?')
    key = 'The study shows an association, but other variables could explain it, so it cannot show cause and effect'
    steps = ['The data come from an observational study: no treatment was randomly assigned.',
             'Other (confounding) variables might explain the association, so the headline’s causal claim is not supported.']
    return R(fmt='multiple-choice', prompt=p, answer=key, steps=steps, codes=['1.10.E', '5.2.A'],
             wrong=['The headline is right because r is not 0', 'The headline is right because the study is large',
                    'The study shows no association because |r| is less than 0.8'])


# ====================================================================== Unit 3: Anticipating Patterns
@fam(3, 1)
def relative_frequency(rng, lv):
    who, prop, p = rng.choice(PROP)
    n = rng.choice([40, 50, 80, 120, 200, 250])
    k = round(n * p + rng.choice([-3, -2, -1, 1, 2, 3]))
    q = (f'In a random sample of {n} {who}, {k} {prop}. What is the relative frequency of this outcome? '
         'Round to three decimal places if needed.')
    ans = g(round(k / n, 3))
    steps = ['Relative frequency = (number of times the outcome occurs) ÷ (number of trials).', f'{k}/{n} = {ans}.']
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['2.3.A'])


@fam(3, 1)
def law_large_numbers(rng, lv):
    ev, p = rng.choice([('a free throw is made', 0.7), ('a die shows a 6', 1 / 6), ('a coin lands heads', 0.5),
                        ('a seed sprouts', 0.85), ('a spinner lands on red', 0.25)])
    n1, n2 = rng.choice([(10, 1000), (20, 2000), (25, 5000)])
    q = (f'The probability that {ev} is {g(round(p, 3))}. One student records {n1} trials and another records {n2:,} trials. '
         'Which statement about the proportion of trials in which the outcome happens is correct?')
    key = f'The proportion from {n2:,} trials is more likely to be close to {g(round(p, 3))}'
    steps = ['The law of large numbers says the relative frequency settles down near the true probability as the number of trials grows.',
             f'So the {n2:,}-trial proportion is more likely to be close to {g(round(p, 3))}; short runs vary much more.']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['2.3.A'],
             wrong=[f'The proportion from {n1} trials is more likely to be close to {g(round(p, 3))}', f'Both proportions will equal {g(round(p, 3))} exactly',
                    'After a run of failures, a success becomes more likely'])


@fam(3, 2)
def or_rule(rng, lv):
    a_name, b_name = rng.choice([('plays a sport', 'is in a club'), ('owns a cat', 'owns a dog'), ('takes Spanish', 'takes art'),
                                 ('drinks coffee', 'drinks tea'), ('has a job', 'plays an instrument'), ('rides the bus', 'eats school lunch')])
    pa, pb = rng.choice([0.45, 0.5, 0.35, 0.6, 0.3]), rng.choice([0.25, 0.4, 0.2, 0.3, 0.55])
    pab = round(rng.choice([0.1, 0.15, 0.05, 0.12, 0.2]) * (1 if min(pa, pb) > 0.2 else 0.5), 2)
    if pab >= min(pa, pb):
        pab = round(min(pa, pb) / 2, 2)
    ans = round(pa + pb - pab, 2)
    if ans >= 1 or pab <= 0:
        return None
    who = rng.choice(['student at a large school', 'teenager in a town', 'member of a youth center'])
    q = f'For a randomly chosen {who}, P(A) = {g(pa)} where A = {a_name}, P(B) = {g(pb)} where B = {b_name}, and P(A and B) = {g(pab)}. Find P(A or B).'
    steps = ['General addition rule: P(A or B) = P(A) + P(B) − P(A and B).',
             f'{g(pa)} + {g(pb)} − {g(pab)} = {g(ans)}.']
    if lv == 'honors':
        q = q.replace('Find P(A or B).', 'Find the probability that the person is in neither group.')
        ans2 = round(1 - ans, 2)
        steps = steps + [f'Neither = 1 − P(A or B) = 1 − {g(ans)} = {g(ans2)}.']
        ans = ans2
    return R(fmt='short-answer', prompt=q, answer=g(ans), steps=steps, codes=['2.7.A', '2.4.A'])


@fam(3, 2)
def and_independent(rng, lv):
    ev1, p1 = rng.choice([('a free throw is made', 0.8), ('a flight is on time', 0.85), ('a seed sprouts', 0.9), ('a light bulb lasts a year', 0.95)])
    k = {'cp2': 2, 'cp1': 3, 'honors': rng.choice([4, 5])}[lv]
    ans = round(p1 ** k, 4)
    q = f'The probability that {ev1} is {g(p1)}, and outcomes are independent. Find the probability that this happens {k} times in a row. Round to four decimal places.'
    steps = ['For independent events, P(A and B and …) is the product of the probabilities.', f'{g(p1)}{str(k).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))} = {f(ans, 4)}.']
    if lv == 'honors':
        q = q.replace(f'happens {k} times in a row', f'fails at least once in {k} tries')
        ans = round(1 - p1 ** k, 4)
        steps = steps + [f'At least one failure is the complement of {k} successes: 1 − {f(p1 ** k, 4)} = {f(ans, 4)}.']
    return R(fmt='short-answer', prompt=q, answer=f(ans, 4), steps=steps, codes=['2.7.A'])


TWOWAY = [('grade', ['Juniors', 'Seniors'], 'lunch choice', ['Hot lunch', 'Packed lunch']),
          ('age group', ['Under 30', '30 and over'], 'news source', ['Online', 'TV']),
          ('pet owned', ['Dog', 'Cat'], 'home type', ['House', 'Apartment']),
          ('class', ['Morning', 'Afternoon'], 'result', ['Passed', 'Did not pass']),
          ('gender', ['Female', 'Male'], 'favorite season', ['Summer', 'Winter'])]


@fam(3, 3)
def conditional_table(rng, lv):
    rv, rows, cv, cols = rng.choice(TWOWAY)
    t = [[rng.randint(12, 60) for _ in cols] for _ in rows]
    i, j = rng.randrange(2), rng.randrange(2)
    col_tot, row_tot, N = t[0][j] + t[1][j], sum(t[i]), sum(map(sum, t))
    table = '; '.join(f'{rows[r]}: {cols[0]} {t[r][0]}, {cols[1]} {t[r][1]}' for r in range(2))
    head = f'A survey classifies people by {rv} and {cv}. Counts — {table}. '
    if lv == 'cp2' or (lv == 'cp1' and rng.random() < 0.5):
        q = head + f'For a randomly chosen person, find P({cols[j]} | {rows[i]}). Round to three decimal places.'
        ans = round(t[i][j] / row_tot, 3)
        steps = [f'Given {rows[i]}, use only that row: total {t[i][0]} + {t[i][1]} = {row_tot}.', f'P = {t[i][j]}/{row_tot} ≈ {f(ans, 3)}.']
        return R(fmt='short-answer', prompt=q, answer=f(ans, 3), steps=steps, codes=['2.6.A', '2.2.A'])
    if lv == 'cp1':
        q = head + f'For a randomly chosen person, find P({rows[i]} | {cols[j]}). Round to three decimal places.'
        ans = round(t[i][j] / col_tot, 3)
        steps = [f'Given {cols[j]}, use only that column: total {t[0][j]} + {t[1][j]} = {col_tot}.', f'P = {t[i][j]}/{col_tot} ≈ {f(ans, 3)}.']
        return R(fmt='short-answer', prompt=q, answer=f(ans, 3), steps=steps, codes=['2.6.A', '2.2.A'])
    c1, c2 = t[i][j] / row_tot, col_tot / N
    key = (f'No: P({cols[j]} | {rows[i]}) ≈ {f(c1, 3)} but P({cols[j]}) ≈ {f(c2, 3)}' if abs(c1 - c2) >= 0.0005 else
           f'Yes: P({cols[j]} | {rows[i]}) = P({cols[j]}) ≈ {f(c2, 3)}')
    q = head + f'Are the events "{rows[i]}" and "{cols[j]}" independent? Choose the answer with the correct justification.'
    wrong = [f'Yes: P({cols[j]} | {rows[i]}) ≈ {f(c1, 3)} is less than 0.5', f'No: the events can both happen to the same person',
             f'Yes: P({rows[i]} and {cols[j]}) ≈ {f(t[i][j] / N, 3)} is not 0', f'No: P({cols[j]} | {rows[i]}) ≈ {f(c1 + 0.05, 3)} but P({cols[j]}) ≈ {f(c2, 3)}']
    steps = [f'P({cols[j]} | {rows[i]}) = {t[i][j]}/{row_tot} ≈ {f(c1, 3)}.', f'P({cols[j]}) = {col_tot}/{N} ≈ {f(c2, 3)}.',
             'Independent events have P(A | B) = P(A). ' + ('These differ, so the events are not independent.' if abs(c1 - c2) >= 0.0005 else 'These are equal, so the events are independent.')]
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['2.6.A', '2.7.A'], wrong=wrong)


@fam(3, 3)
def conditional_formula(rng, lv):
    a, b = rng.choice([('a student has a job', 'a student has a car'), ('an email is spam', 'an email has a link'), ('a patient tests positive', 'a patient has the flu'),
                       ('a shopper buys bread', 'a shopper buys milk'), ('a flight is late', 'it is raining')])
    pb = rng.choice([0.4, 0.5, 0.25, 0.6, 0.35])
    pab = round(pb * rng.choice([0.3, 0.4, 0.6, 0.2]), 3)
    ans = round(pab / pb, 3)
    q = f'In a study, the probability that {b} is {g(pb)}, and the probability that {a} and {b} is {g(pab)}. Find the probability that {a}, given that {b}. Round to three decimal places.'
    steps = ['P(A | B) = P(A and B) / P(B).', f'{g(pab)}/{g(pb)} = {f(ans, 3)}.']
    return R(fmt='short-answer', prompt=q, answer=f(ans, 3), steps=steps, codes=['2.6.A'])


@fam(3, 4)
def simulation_assign(rng, lv):
    p, ev = rng.choice([(0.3, 'a customer wins a prize'), (0.6, 'a free throw is made'), (0.2, 'a seed fails to sprout'),
                        (0.45, 'a voter supports the measure'), (0.75, 'a flight is on time')])
    k = round(p * 10)
    key = f'Let digits 0–{k - 1} represent "{ev}" and {k}–9 represent "not"'
    q = f'The probability that {ev} is {g(p)}. Which assignment of random digits 0–9 correctly simulates one trial?'
    wrong = [f'Let digits 0–{k} represent "{ev}" and {k + 1}–9 represent "not"', f'Let digits 1–{k} represent "{ev}" and 0 and {k + 1}–9 represent "not"' if k < 9 else 'Let digit 0 represent "not"',
             'Let even digits represent the outcome and odd digits represent "not"']
    if p == 0.5:
        pass
    steps = [f'There are 10 equally likely digits, so {g(p)} of them is {k} digits.', f'Digits 0–{k - 1} are {k} digits, so they give probability {k}/10 = {g(p)}.']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['2.3.A'], wrong=wrong)


@fam(3, 4)
def simulation_estimate(rng, lv):
    ev, trials = rng.choice([('at least 2 of 5 customers win a prize', 50), ('a family with 3 children has at least 2 girls', 40),
                             ('a player makes 4 free throws in a row', 60), ('all 3 lights on a commute are green', 80), ('a cereal buyer collects all 4 prizes in 6 boxes', 100)])
    hits = rng.randint(int(trials * 0.2), int(trials * 0.7))
    q = f'A class runs {trials} trials of a simulation, and in {hits} of them {ev}. What is the estimated probability? Round to two decimal places.'
    ans = round(hits / trials, 2)
    steps = ['Estimated probability = (number of trials in which the event happened) ÷ (number of trials).', f'{hits}/{trials} = {f(ans, 2)}.']
    if lv == 'honors':
        q += ' (A larger number of trials would make this estimate less variable.)'
    return R(fmt='short-answer', prompt=q, answer=f(ans, 2), steps=steps, codes=['2.3.A'])


DISTS = [('number of pets in a household', [0, 1, 2, 3], [0.3, 0.4, 0.2, 0.1]), ('number of cars in a family', [0, 1, 2, 3], [0.1, 0.35, 0.4, 0.15]),
         ('number of goals a team scores in a game', [0, 1, 2, 3, 4], [0.15, 0.3, 0.3, 0.15, 0.1]), ('number of texts received in an hour', [0, 1, 2, 3], [0.25, 0.35, 0.25, 0.15]),
         ('number of defective parts in a box', [0, 1, 2], [0.7, 0.2, 0.1]), ('number of siblings of a student', [0, 1, 2, 3, 4], [0.2, 0.4, 0.25, 0.1, 0.05])]


def dist_text(xs, ps):
    return ', '.join(f'P(X = {x}) = {g(p)}' for x, p in zip(xs, ps))


@fam(3, 6)
def expected_value(rng, lv):
    name, xs, ps = rng.choice(DISTS)
    mu = sum(x * p for x, p in zip(xs, ps))
    var = sum((x - mu) ** 2 * p for x, p in zip(xs, ps))
    q = f'X = {name}. {dist_text(xs, ps)}. '
    if lv == 'cp2':
        q += 'Find the expected value E(X).'
        ans = g(round(mu, 4))
        steps = ['E(X) = Σ x·P(x).', ' + '.join(f'{x}({g(p)})' for x, p in zip(xs, ps)) + f' = {ans}.']
    elif lv == 'cp1':
        q += 'Find the standard deviation of X. Round to three decimal places.'
        ans = f(math.sqrt(var), 3)
        steps = [f'E(X) = {g(round(mu, 4))}.', 'Var(X) = Σ (x − μ)² P(x) = ' + ' + '.join(f'({x} − {g(round(mu, 4))})²({g(p)})' for x, p in zip(xs, ps)) + f' = {g(round(var, 4))}.',
                 f'SD = √{g(round(var, 4))} ≈ {ans}.']
    else:
        a, b = rng.choice([(5, 2), (10, 3), (-2, 4), (20, 1.5)])
        q += f'A new variable is Y = {g(a)} + {g(b)}X. Find the standard deviation of Y. Round to three decimal places.'
        ans = f(b * math.sqrt(var), 3)
        steps = [f'E(X) = {g(round(mu, 4))} and Var(X) = {g(round(var, 4))}, so SD(X) ≈ {f(math.sqrt(var), 4)}.',
                 f'Adding {g(a)} does not change the spread; multiplying by {g(b)} multiplies the SD by {g(b)}.', f'SD(Y) = {g(b)} × {f(math.sqrt(var), 4)} ≈ {ans}.']
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['2.9.A'] if lv != 'honors' else ['BEYOND.LINRV'])


@fam(3, 6)
def fair_game(rng, lv):
    cost = rng.choice([2, 3, 5])
    prizes = rng.choice([[(20, 0.05), (5, 0.2)], [(10, 0.1), (2, 0.3)], [(50, 0.02), (10, 0.1)], [(25, 0.04), (4, 0.25)]])
    ev = sum(v * p for v, p in prizes)
    net = round(ev - cost, 2)
    desc = ' and '.join(f'${v} with probability {g(p)}' for v, p in prizes)
    q = f'A school game costs ${cost} to play. A player wins {desc}; otherwise nothing. Find the expected net gain per play, in dollars.'
    steps = [f'Expected winnings: {" + ".join(f"{v}({g(p)})" for v, p in prizes)} = {g(round(ev, 2))}.',
             f'Net gain = expected winnings − cost = {g(round(ev, 2))} − {cost} = {g(net)}.',
             'A negative value means the school earns that much per play in the long run.']
    return R(fmt='short-answer', prompt=q, answer=g(net), steps=steps, codes=['2.9.A', '2.9.B'])


@fam(3, 7)
def binomial_prob(rng, lv):
    who, prop, p = rng.choice(PROP)
    p = round(p, 2)
    n = {'cp2': rng.choice([5, 6, 8]), 'cp1': rng.choice([10, 12, 15]), 'honors': rng.choice([20, 25, 30])}[lv]
    k = max(1, min(n - 1, round(n * p) + rng.choice([-1, 0, 1])))
    if lv == 'cp2':
        ans = stats.binom.pmf(k, n, p)
        q = f'About {pct(p)} of {who} {prop}. In a random sample of {n}, find the probability that exactly {k} {prop}. Round to four decimal places.'
        steps = [f'X ~ Binomial(n = {n}, p = {g(p)}): fixed n, independent trials, two outcomes, same p.',
                 f'P(X = {k}) = C({n}, {k}) × {g(p)}{str(k).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))} × {g(round(1 - p, 2))}{str(n - k).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))} ≈ {f(ans, 4)}.']
    elif lv == 'cp1':
        ans = stats.binom.cdf(k, n, p)
        q = f'About {pct(p)} of {who} {prop}. In a random sample of {n}, find the probability that at most {k} {prop}. Use technology (binomcdf). Round to four decimal places.'
        steps = [f'X ~ Binomial(n = {n}, p = {g(p)}).', f'P(X ≤ {k}) = binomcdf({n}, {g(p)}, {k}) ≈ {f(ans, 4)}.']
    else:
        ans = 1 - stats.binom.cdf(k - 1, n, p)
        q = f'About {pct(p)} of {who} {prop}. In a random sample of {n}, find the probability that at least {k} {prop}. Use technology. Round to four decimal places.'
        steps = [f'X ~ Binomial(n = {n}, p = {g(p)}).', f'P(X ≥ {k}) = 1 − P(X ≤ {k - 1}).', f'1 − binomcdf({n}, {g(p)}, {k - 1}) ≈ {f(ans, 4)}.']
    return R(fmt='short-answer', prompt=q, answer=f(ans, 4), steps=steps, codes=['2.10.E'])


@fam(3, 7)
def binomial_mean_sd(rng, lv):
    who, prop, p = rng.choice(PROP)
    p = round(p, 2)
    n = rng.choice([40, 50, 60, 80, 100, 150, 200])
    mu, sd = n * p, math.sqrt(n * p * (1 - p))
    if lv == 'cp2':
        q = f'About {pct(p)} of {who} {prop}. X is the number in a random sample of {n} that do. Find the mean of X.'
        ans = g(round(mu, 2))
        steps = ['For a binomial random variable, μ = np.', f'μ = {n} × {g(p)} = {ans}.']
    else:
        q = f'About {pct(p)} of {who} {prop}. X is the number in a random sample of {n} that do. Find the standard deviation of X. Round to two decimal places.'
        ans = f(sd, 2)
        steps = ['For a binomial random variable, σ = √(np(1 − p)).', f'σ = √({n} × {g(p)} × {g(round(1 - p, 2))}) = √{g(round(n * p * (1 - p), 4))} ≈ {ans}.']
        if lv == 'honors':
            lo, hi = math.ceil(mu - sd), math.floor(mu + sd)
            pr = stats.binom.cdf(hi, n, p) - stats.binom.cdf(lo - 1, n, p)
            q = (f'About {pct(p)} of {who} {prop}. X is the number in a random sample of {n} that do. Find the probability that X is within one standard deviation '
                 'of its mean. Use technology. Round to four decimal places.')
            ans = f(pr, 4)
            steps = [f'μ = np = {g(round(mu, 2))}; σ = √(np(1 − p)) ≈ {f(sd, 3)}.', f'Within one SD: {f(mu - sd, 3)} ≤ X ≤ {f(mu + sd, 3)}, so X = {lo} to {hi} (X is a whole number).',
                     f'P({lo} ≤ X ≤ {hi}) = binomcdf({n}, {g(p)}, {hi}) − binomcdf({n}, {g(p)}, {lo - 1}) ≈ {ans}.']
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['2.10.B'])


@fam(3, 8)
def combine_mean_sd(rng, lv):
    a, b, total = rng.choice([('the time to drive to the store', 'the time spent shopping', 'total trip time'), ('the weight of an empty box', 'the weight of its contents', 'total weight'),
                              ('the weight of a bag of flour', 'the weight of a bag of sugar', 'total weight of the two bags'), ('the length of part A', 'the length of part B', 'length of the assembly')])
    m1, s1 = rng.choice([(15, 3), (20, 4), (8, 1.5), (30, 5)])
    m2, s2 = rng.choice([(25, 6), (12, 2), (40, 8), (18, 2.5)])
    sd = math.sqrt(s1 ** 2 + s2 ** 2)
    if lv == 'cp2':
        q = f'Let X = {a} (mean {g(m1)}) and Y = {b} (mean {g(m2)}). Find the mean of the {total}, X + Y.'
        ans = g(m1 + m2)
        steps = ['Means always add: E(X + Y) = E(X) + E(Y).', f'{g(m1)} + {g(m2)} = {ans}.']
    else:
        q = f'Let X = {a} (mean {g(m1)}, SD {g(s1)}) and Y = {b} (mean {g(m2)}, SD {g(s2)}), with X and Y independent. Find the SD of the {total}, X + Y. Round to two decimal places.'
        ans = f(sd, 2)
        steps = ['For independent random variables, variances add (standard deviations do not).',
                 f'Var(X + Y) = {g(s1)}² + {g(s2)}² = {g(s1 ** 2 + s2 ** 2)}.', f'SD = √{g(s1 ** 2 + s2 ** 2)} ≈ {ans}.']
        if lv == 'honors':
            q = q.replace(f'the {total}, X + Y. Round', 'the difference X − Y. Round')
            steps[0] = 'For independent random variables, Var(X − Y) = Var(X) + Var(Y): variances add even for a difference.'
            steps[1] = f'Var(X − Y) = {g(s1)}² + {g(s2)}² = {g(s1 ** 2 + s2 ** 2)}.'
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['BEYOND.COMB'])


@fam(3, 8)
def combine_normal_prob(rng, lv):
    m1, s1, m2, s2 = rng.choice([(12, 2, 9, 1.5), (30, 4, 25, 3), (60, 5, 55, 6), (100, 8, 90, 6)])
    names = rng.choice([('Ana’s commute', 'Ben’s commute', 'minutes'), ('a large bag of rice', 'a small bag of rice', 'ounces'),
                        ('the first runner’s time', 'the second runner’s time', 'seconds')])
    sd = math.sqrt(s1 ** 2 + s2 ** 2)
    z = (0 - (m1 - m2)) / sd
    ans = round(1 - table_a(z), 4) if lv != 'cp2' else None
    q = (f'{names[0][0].upper() + names[0][1:]} is Normal with mean {g(m1)} and SD {g(s1)} {names[2]}; {names[1]} is Normal with mean {g(m2)} and SD {g(s2)} {names[2]}, independent. '
         f'Find the probability that {names[0]} is longer than {names[1]}. Use Table A (round z to two decimal places). Round to four decimal places.')
    D = m1 - m2
    steps = [f'D = X − Y has mean {g(m1)} − {g(m2)} = {g(D)} and SD √({g(s1)}² + {g(s2)}²) ≈ {f(sd, 4)}.',
             f'P(D > 0): z = (0 − {g(D)})/{f(sd, 4)} ≈ {f(z, 2)}.', f'P(Z > {f(z, 2)}) = 1 − {f(table_a(z), 4)} = {f(round(1 - table_a(z), 4), 4)}.']
    return R(fmt='short-answer', prompt=q, answer=f(round(1 - table_a(z), 4), 4), steps=steps, codes=['BEYOND.COMB'])


@fam(3, 10)
def sd_xbar_n(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = rng.choice([16, 25, 36, 49, 64, 100])
    se = sd / math.sqrt(n)
    if lv == 'cp2':
        q = f'The {var} has mean {g(mu)} {unit} and SD {g(sd)} {unit}. For random samples of {n}, find the standard deviation of the sample mean x̄. Round to three decimal places.'
        ans = f(se, 3)
        steps = ['σ_x̄ = σ/√n.', f'{g(sd)}/√{n} = {g(sd)}/{g(math.sqrt(n))} ≈ {ans} {unit}.']
    elif lv == 'cp1':
        m = rng.choice([4, 9])
        q = (f'The {var} has SD {g(sd)} {unit}. A sample of {n} gives σ_x̄ = {f(se, 3)} {unit}. What is σ_x̄ if the sample size is multiplied by {m}? '
             'Round to three decimal places.')
        ans = f(se / math.sqrt(m), 3)
        steps = [f'σ_x̄ = σ/√n, so multiplying n by {m} divides σ_x̄ by √{m} = {g(math.sqrt(m))}.', f'{f(se, 3)}/{g(math.sqrt(m))} ≈ {ans} {unit}.']
    else:
        target = round(se / 2, 4)
        q = (f'The {var} has SD {g(sd)} {unit}. What sample size is needed so that the standard deviation of x̄ is {g(target)} {unit}?')
        ans = str(4 * n)
        steps = ['Solve σ/√n = target for n: n = (σ/target)².', f'n = ({g(sd)}/{g(target)})² = {g(round((sd / target) ** 2, 2))}.',
                 f'n = {4 * n} (halving σ_x̄ needs four times the sample size).']
        if abs((sd / target) ** 2 - 4 * n) > 0.6:
            return None
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['4.1.A'])


@fam(3, 10)
def bias_variability(rng, lv):
    scen = rng.choice([
        ('Estimator A is centered on the parameter with a large spread; estimator B is centered on the parameter with a small spread.', 'B, because it is unbiased and less variable'),
        ('Estimator A is centered on the parameter with a small spread; estimator B is centered above the parameter with a small spread.', 'A, because it is unbiased and has low variability'),
        ('Estimator A is centered below the parameter with a small spread; estimator B is centered on the parameter with a small spread.', 'B, because it is unbiased and has low variability'),
        ('Two unbiased estimators use samples of size 50 and 500 from the same population.', 'The one with n = 500, because larger samples reduce variability'),
    ])
    desc, key = scen
    q = 'Simulated sampling distributions are shown for two estimators of a parameter. ' + desc + ' Which estimator is better?'
    wrong = ['A, because a larger spread captures the parameter more often', 'Neither, because both are biased', 'The one with n = 50, because smaller samples are less biased',
             'B, because it is unbiased and less variable', 'A, because it is unbiased and has low variability']
    wrong = [w for w in wrong if w != key]
    steps = ['A good estimator is unbiased (its sampling distribution is centered on the parameter) and has low variability (small spread).',
             'Sample size affects variability, not bias.', f'Answer: {key[0].lower() + key[1:]}.']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['3.1.A'], wrong=wrong)


@fam(3, 10)
def clt_condition(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    shape = rng.choice(['strongly skewed to the right', 'skewed to the left', 'roughly Normal'])
    n = rng.choice([8, 12, 40, 60])
    normal_ok = shape == 'roughly Normal' or n >= 30
    key = 'Yes' if normal_ok else 'No'
    q = f'The distribution of the {var} is {shape}. Is the sampling distribution of x̄ for random samples of size {n} approximately Normal?'
    ans = (f'Yes, because {"the population is Normal" if shape == "roughly Normal" else f"n = {n} ≥ 30 (central limit theorem)"}' if normal_ok
           else f'No, because the population is skewed and n = {n} is small')
    steps = ['x̄ is approximately Normal if the population is Normal, or if n is large (n ≥ 30) by the central limit theorem.',
             f'Shape: {shape}; n = {n}.', f'Answer: {ans[0].lower() + ans[1:]}.']
    wrong = ['Yes, because x̄ is always Normal', f'No, because n = {n} is less than 100', 'Yes, because the sample is random',
             f'No, because the population is skewed and n = {n} is small', f'Yes, because n = {n} ≥ 30 (central limit theorem)']
    wrong = [w for w in wrong if w != ans]
    return R(fmt='multiple-choice', prompt=q, answer=ans, steps=steps, codes=['4.1.B'], wrong=wrong)


# ====================================================================== Unit 4: Inference
@fam(4, 1)
def ci_estimate_me(rng, lv):
    who, prop, p = rng.choice(PROP)
    c = rng.choice([0.90, 0.95, 0.99])
    n = rng.choice([200, 300, 400, 500, 800])
    ph = round(p + rng.choice([-0.03, 0.02, 0.01, -0.01]), 2)
    me = round(ZSTAR[c] * math.sqrt(ph * (1 - ph) / n), 3)
    lo, hi = round(ph - me, 3), round(ph + me, 3)
    ask = {'cp2': 'point', 'cp1': rng.choice(['point', 'me']), 'honors': 'me'}[lv] if lv != 'cp2' else rng.choice(['point', 'me'])
    q = f'A {round(c * 100)}% confidence interval for the proportion of {who} {wt(who)} {prop} is ({f(lo, 3)}, {f(hi, 3)}). '
    if ask == 'point':
        q += 'What is the point estimate p̂?'
        ans = f((lo + hi) / 2, 3)
        steps = ['The interval is p̂ ± ME, so p̂ is the midpoint.', f'p̂ = ({f(lo, 3)} + {f(hi, 3)})/2 = {ans}.']
    else:
        q += 'What is the margin of error?'
        ans = f((hi - lo) / 2, 3)
        steps = ['The interval is p̂ ± ME, so ME is half the width.', f'ME = ({f(hi, 3)} − {f(lo, 3)})/2 = {ans}.']
        if lv == 'honors':
            q = q.replace('What is the margin of error?', f'It was computed from a random sample of {n}. What sample size would give a margin of error half as large, at the same confidence level?')
            ans = str(4 * n)
            steps.append(f'ME = z*√(p̂(1 − p̂)/n) shrinks with √n, so halving it needs 4 times the sample size: 4 × {n} = {4 * n}.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['3.3.D', '3.1.B'])


@fam(4, 1)
def standard_error_p(rng, lv):
    who, prop, p = rng.choice(PROP)
    n = rng.choice([100, 150, 250, 400, 600])
    x = round(n * p) + rng.choice([-4, -2, 3, 5])
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    q = f'In a random sample of {n} {who}, {x} {prop}. Find the standard error of p̂. Round to four decimal places.'
    steps = [f'p̂ = {x}/{n} = {g(round(ph, 4))}.', f'SE = √(p̂(1 − p̂)/n) = √({g(round(ph, 4))} × {g(round(1 - ph, 4))}/{n}) ≈ {f(se, 4)}.']
    return R(fmt='short-answer', prompt=q, answer=f(se, 4), steps=steps, codes=['3.3.D'])


@fam(4, 3)
def one_prop_interval(rng, lv):
    who, prop, p = rng.choice(PROP)
    c = rng.choice([0.90, 0.95, 0.99])
    n = rng.choice([150, 200, 250, 400, 500])
    x = round(n * p) + rng.choice([-3, 2, 4, -5])
    ph = x / n
    zs = ZSTAR[c]
    se = math.sqrt(ph * (1 - ph) / n)
    me = zs * se
    lo, hi = ph - me, ph + me
    q = f'In a random sample of {n} {who}, {x} {prop}. '
    if lv == 'cp2':
        q += f'Find the margin of error for a {round(c * 100)}% confidence interval for p (z* = {zs}). Round to three decimal places.'
        ans = f(me, 3)
        steps = [f'p̂ = {x}/{n} = {g(round(ph, 4))}.', f'SE = √({g(round(ph, 4))}({g(round(1 - ph, 4))})/{n}) ≈ {f(se, 4)}.', f'ME = z* × SE = {zs} × {f(se, 4)} ≈ {ans}.']
    else:
        q += f'Construct a {round(c * 100)}% confidence interval for the proportion of all {who} {wt(who)} {prop}. Round the endpoints to three decimal places.'
        ans = f'({f(lo, 3)}, {f(hi, 3)})'
        steps = [f'Conditions: random sample; {x} successes and {n - x} failures are both at least 10.',
                 f'p̂ = {g(round(ph, 4))}; SE = √(p̂(1 − p̂)/n) ≈ {f(se, 4)}; z* = {zs}.', f'p̂ ± z*·SE = {g(round(ph, 4))} ± {f(me, 4)} = {ans}.']
        if lv == 'honors':
            steps.append(f'Interpretation: we are {round(c * 100)}% confident that the interval from {f(lo, 3)} to {f(hi, 3)} captures the true proportion of {who} {wt(who)} {prop}.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['3.3.C'])


@fam(4, 3)
def sample_size_p(rng, lv):
    who, prop, p = rng.choice(PROP)
    c = rng.choice([0.90, 0.95, 0.99])
    me = rng.choice([0.02, 0.03, 0.04, 0.05])
    zs = ZSTAR[c]
    guess = 0.5 if lv != 'honors' else round(p, 2)
    nn = (zs / me) ** 2 * guess * (1 - guess)
    ans = math.ceil(nn - 1e-9)
    q = (f'A researcher wants to estimate the proportion of {who} {wt(who)} {prop} within a margin of error of {g(me)} at {round(c * 100)}% confidence (z* = {zs}). '
         + ('Use p* = 0.5. ' if lv != 'honors' else f'A pilot study suggests p is about {g(guess)}. Use it as p*. ')
         + 'What is the smallest sample size needed?')
    steps = ['Solve z*√(p*(1 − p*)/n) ≤ ME for n: n ≥ (z*/ME)² p*(1 − p*).', f'n ≥ ({zs}/{g(me)})² × {g(guess)} × {g(round(1 - guess, 2))} ≈ {f(nn, 2)}.',
             f'Round up: n = {ans}.']
    return R(fmt='short-answer', prompt=q, answer=str(ans), steps=steps, codes=['3.4.C'])


@fam(4, 4)
def t_interval(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = rng.choice([10, 12, 15, 20, 25, 30])
    c = rng.choice([0.90, 0.95, 0.99])
    xb = round(mu + rng.choice([-0.3, 0.2, 0.1]) * sd, max(dp, 1))
    s = round(sd * rng.choice([0.9, 1.1, 1.0]), max(dp, 1) + 1)
    ts = tstar(c, n - 1)
    se = s / math.sqrt(n)
    me = ts * se
    q = f'A random sample of {n} {pop} has mean {g(xb)} {unit} and standard deviation {g(s)} {unit} for the {var}. '
    if lv == 'cp2':
        q += f'What critical value t* is used for a {round(c * 100)}% confidence interval for μ? Round to three decimal places.'
        ans = f(ts, 3)
        steps = [f'df = n − 1 = {n - 1}.', f't* for {round(c * 100)}% confidence with df = {n - 1} (Table B or invT) = {ans}.']
    else:
        q += f'Construct a {round(c * 100)}% confidence interval for the mean {var}. Round the endpoints to two decimal places.'
        ans = f'({f(xb - me, 2)}, {f(xb + me, 2)})'
        steps = [f'df = {n - 1}; t* = {f(ts, 3)}.', f'SE = s/√n = {g(s)}/√{n} ≈ {f(se, 4)}.', f'x̄ ± t*·SE = {g(xb)} ± {f(ts, 3)}({f(se, 4)}) = {g(xb)} ± {f(me, 4)} = {ans}.']
        if lv == 'honors':
            steps.insert(0, f'Conditions: random sample; n = {n}' + (' ≥ 30, so the CLT applies.' if n >= 30 else ' < 30, so we need the sample data to show no strong skew or outliers.'))
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['4.2.D'])


@fam(4, 4)
def t_df_width(rng, lv):
    n = rng.choice([8, 12, 18, 24, 40])
    c1, c2 = rng.choice([(0.90, 0.99), (0.95, 0.99), (0.90, 0.95)])
    ctx = rng.choice(['battery lives', 'commute times', 'reaction times', 'test scores'])
    q = (f'Two one-sample t intervals are built from the same random sample of {n} {ctx}: a {round(c1 * 100)}% interval and a {round(c2 * 100)}% interval. '
         'Which statement is true?')
    key = f'The {round(c2 * 100)}% interval is wider because it uses a larger t*'
    steps = [f'Both use df = {n - 1} and the same SE = s/√n.', f'Higher confidence needs a larger t*: t* = {f(tstar(c1, n - 1), 3)} for {round(c1 * 100)}% and {f(tstar(c2, n - 1), 3)} for {round(c2 * 100)}%.',
             f'So the {round(c2 * 100)}% interval is wider.']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['4.3.C'],
             wrong=[f'The {round(c1 * 100)}% interval is wider because it uses a larger t*', 'Both intervals have the same width because they use the same data',
                    f'The {round(c2 * 100)}% interval is narrower because it is more confident'])


HYP = [('the proportion of {who} {wt(who)} {prop}', 'p', 'has changed from', '≠'), ('the proportion of {who} {wt(who)} {prop}', 'p', 'is now greater than', '>'),
       ('the proportion of {who} {wt(who)} {prop}', 'p', 'is now less than', '<')]


@fam(4, 5)
def write_hypotheses(rng, lv):
    who, prop, p0 = rng.choice(PROP)
    p0 = round(p0, 2)
    word, sym = rng.choice([('has changed from', '≠'), ('is greater than', '>'), ('is less than', '<')])
    q = f'Last year {pct(p0)} of {who} {prop}. A researcher wants to test whether the proportion this year {word} {g(p0)}. Which hypotheses are correct?'
    key = f'H₀: p = {g(p0)}; Hₐ: p {sym} {g(p0)}'
    others = [s for s in ['≠', '>', '<'] if s != sym]
    wrong = [f'H₀: p = {g(p0)}; Hₐ: p {others[0]} {g(p0)}', f'H₀: p̂ = {g(p0)}; Hₐ: p̂ {sym} {g(p0)}', f'H₀: p {sym} {g(p0)}; Hₐ: p = {g(p0)}']
    steps = ['Hypotheses are about the population parameter p, never the statistic p̂.', f'H₀ states no change: p = {g(p0)}. Hₐ states the researcher’s claim: p {sym} {g(p0)}.']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['3.5.B'], wrong=wrong)


@fam(4, 5)
def hypotheses_mean(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    word, sym = rng.choice([('is different from', '≠'), ('is more than', '>'), ('is less than', '<')])
    m0 = g(mu)
    q = f'A company claims the mean {var} is {m0} {unit}. A consumer group suspects the true mean {word} {m0}. Which hypotheses should it test?'
    key = f'H₀: μ = {m0}; Hₐ: μ {sym} {m0}'
    others = [s for s in ['≠', '>', '<'] if s != sym]
    wrong = [f'H₀: μ = {m0}; Hₐ: μ {others[0]} {m0}', f'H₀: x̄ = {m0}; Hₐ: x̄ {sym} {m0}', f'H₀: μ {sym} {m0}; Hₐ: μ = {m0}']
    steps = ['Hypotheses describe the population mean μ.', f'H₀: μ = {m0} (the claim); Hₐ: μ {sym} {m0} (what the group suspects).']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['4.4.B'], wrong=wrong)


@fam(4, 7)
def one_prop_z_stat(rng, lv):
    who, prop, p0 = rng.choice(PROP)
    p0 = round(p0, 2)
    n = rng.choice([150, 200, 300, 400, 500])
    x = round(n * p0) + rng.choice([-14, -9, 8, 12, 15])
    ph = x / n
    se = math.sqrt(p0 * (1 - p0) / n)
    z = (ph - p0) / se
    sym = '>' if ph > p0 else '<'
    q = f'Test H₀: p = {g(p0)} against Hₐ: p {sym} {g(p0)}, where p is the proportion of {who} {wt(who)} {prop}. In a random sample of {n}, {x} {prop}. '
    if lv == 'cp2':
        q += 'Find the test statistic z. Round to two decimal places.'
        ans = f(z, 2)
        steps = [f'p̂ = {x}/{n} = {g(round(ph, 4))}.', f'Standard deviation under H₀: √({g(p0)} × {g(round(1 - p0, 2))}/{n}) ≈ {f(se, 4)}.', f'z = ({g(round(ph, 4))} − {g(p0)})/{f(se, 4)} ≈ {ans}.']
    else:
        pv = table_a(z) if sym == '<' else round(1 - table_a(z), 4)
        q += 'Find the p-value. Use Table A (round z to two decimal places). Round to four decimal places.'
        ans = f(pv, 4)
        steps = [f'p̂ = {g(round(ph, 4))}; z = ({g(round(ph, 4))} − {g(p0)})/√({g(p0)}({g(round(1 - p0, 2))})/{n}) ≈ {f(z, 2)}.',
                 f'p-value = P(Z {sym} {f(z, 2)}) = {ans}.']
        if lv == 'honors':
            steps.append(f'At α = 0.05: {"reject H₀; there is convincing evidence" if pv < 0.05 else "fail to reject H₀; there is not convincing evidence"} that the proportion of {who} {wt(who)} {prop} is {"greater" if sym == ">" else "less"} than {g(p0)}.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['3.7.A'])


@fam(4, 7)
def one_mean_t_stat(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n = rng.choice([12, 16, 20, 25, 36])
    d = max(dp, 1)
    xb = round(mu + rng.choice([-0.5, -0.4, 0.45, 0.6]) * sd, d)
    s = round(sd, d + 1)
    t = (xb - mu) / (s / math.sqrt(n))
    sym = '>' if xb > mu else '<'
    q = f'Test H₀: μ = {g(mu)} against Hₐ: μ {sym} {g(mu)} for the {var} ({unit}). A random sample of {n} {pop} has x̄ = {g(xb)} and s = {g(s)}. '
    if lv in ('cp2', 'cp1'):
        q += 'Find the test statistic t. Round to two decimal places.'
        ans = f(t, 2)
        steps = [f'SE = s/√n = {g(s)}/√{n} ≈ {f(s / math.sqrt(n), 4)}.', f't = (x̄ − μ₀)/SE = ({g(xb)} − {g(mu)})/{f(s / math.sqrt(n), 4)} ≈ {ans}.', f'df = {n - 1}.']
    else:
        pv = stats.t.sf(abs(t), n - 1)
        q += 'Find the p-value. Use technology (tcdf). Round to four decimal places.'
        ans = f(pv, 4)
        steps = [f't = ({g(xb)} − {g(mu)})/({g(s)}/√{n}) ≈ {f(t, 3)}, df = {n - 1}.', f'p-value = P(t {sym} {f(t, 3)}) with df = {n - 1} ≈ {ans}.',
                 f'At α = 0.05: {"reject H₀" if pv < 0.05 else "fail to reject H₀"}.']
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['4.5.A'])


@fam(4, 7)
def shaded_pvalue(rng, lv):
    z = rng.choice([1.2, 1.5, 1.8, 2.1, 2.4])
    alt = rng.choice(['>', '<', '≠'])
    q = f'A one-proportion z test gives z = {"−" if alt == "<" else ""}{g(z)}. The shaded area under the standard Normal curve is the p-value. Which alternative hypothesis was used?'
    key = {'>': 'Hₐ: p > p₀', '<': 'Hₐ: p < p₀', '≠': 'Hₐ: p ≠ p₀'}[alt]
    steps = ['The p-value is the area in the direction of Hₐ, beyond the observed test statistic.',
             {'>': 'Only the right tail is shaded, so Hₐ: p > p₀.', '<': 'Only the left tail is shaded, so Hₐ: p < p₀.', '≠': 'Both tails are shaded, so the test is two-sided: Hₐ: p ≠ p₀.'}[alt]]
    zz = -z if alt == '<' else z
    spec = {'kind': 'normal', 'shade': {'>': 'right', '<': 'left', '≠': 'both'}[alt], 'a': zz, 'label': f'z = {g(zz)}' if alt != '≠' else f'z = ±{g(z)}'}
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['3.6.A'], wrong=['Hₐ: p > p₀', 'Hₐ: p < p₀', 'Hₐ: p ≠ p₀', 'H₀: p = p₀'], normal=spec)


@fam(4, 10)
def two_sample_t_stat(rng, lv):
    var, unit, pop, mu, sd, dp = rng.choice(QUANT)
    n1, n2 = rng.choice([(20, 25), (30, 30), (15, 18), (40, 35)])
    d = max(dp, 1)
    x1, x2 = round(mu + 0.3 * sd, d), round(mu - 0.1 * sd, d)
    s1, s2 = round(sd, d), round(sd * 1.15, d)
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    t = (x1 - x2) / se
    q = (f'Two independent random samples compare the {var} ({unit}) for two groups of {pop}: Group 1 has n = {n1}, x̄ = {g(x1)}, s = {g(s1)}; '
         f'Group 2 has n = {n2}, x̄ = {g(x2)}, s = {g(s2)}. ')
    if lv == 'cp2':
        q += 'Find the standard error of x̄₁ − x̄₂. Round to three decimal places.'
        ans = f(se, 3)
        steps = ['SE = √(s₁²/n₁ + s₂²/n₂).', f'√({g(s1)}²/{n1} + {g(s2)}²/{n2}) ≈ {ans}.']
    else:
        q += 'Find the two-sample t statistic for H₀: μ₁ = μ₂. Round to two decimal places.'
        ans = f(t, 2)
        steps = [f'SE = √({g(s1)}²/{n1} + {g(s2)}²/{n2}) ≈ {f(se, 4)}.', f't = (x̄₁ − x̄₂ − 0)/SE = ({g(x1)} − {g(x2)})/{f(se, 4)} ≈ {ans}.']
        if lv == 'honors':
            steps.append(f'Conservative df = min({n1}, {n2}) − 1 = {min(n1, n2) - 1}; technology uses a larger df.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['4.10.A'])


@fam(4, 10)
def paired_or_two(rng, lv):
    scen = rng.choice([
        ('Each of 15 students takes a reading test before and after a summer program.', 'Paired t procedure, because each student gives two related measurements'),
        ('Twenty randomly chosen men and 20 randomly chosen women report their hours of sleep.', 'Two-sample t procedure, because the two groups are independent'),
        ('Twelve cars are each driven with two fuel additives in random order, and gas mileage is recorded.', 'Paired t procedure, because each car gives two related measurements'),
        ('Thirty plants are randomly assigned, 15 to each of two fertilizers, and their heights are compared.', 'Two-sample t procedure, because the two groups are independent'),
        ('A store compares prices of the same 25 items at two supermarkets.', 'Paired t procedure, because the same items are priced at both stores'),
        ('Random samples of 40 seniors and 40 juniors report their weekly work hours.', 'Two-sample t procedure, because the two groups are independent'),
    ])
    desc, key = scen
    q = desc + ' Which procedure should be used to compare the means?'
    other = 'Two-sample t procedure, because the two groups are independent' if key.startswith('Paired') else 'Paired t procedure, because each subject gives two related measurements'
    steps = ['Paired data come from the same individuals (or matched pairs) measured twice; independent samples come from separate groups.',
             f'Answer: {key[0].lower() + key[1:]}.']
    return R(fmt='multiple-choice', prompt=q, answer=key, steps=steps, codes=['4.4.A', '4.9.A'],
             wrong=[other, 'One-proportion z procedure, because there are two groups', 'Chi-square test, because there are two variables'])


@fam(4, 11)
def slope_interval(rng, lv):
    x, y, sign = rng.choice([('hours studied', 'test score', 1), ('advertising spending', 'weekly sales', 1), ('car age', 'resale value', -1), ('fertilizer amount', 'plant height', 1), ('practice time', 'free-throw percentage', 1)])
    n = rng.choice([12, 15, 20, 25])
    b = sign * rng.choice([2.4, 1.6, 0.85, 3.2, 0.45])
    se = round(abs(b) * rng.choice([0.25, 0.3, 0.4]), 3)
    c = rng.choice([0.90, 0.95, 0.99])
    ts = tstar(c, n - 2)
    lo, hi = b - ts * se, b + ts * se
    q = f'A regression of {y} on {x} for a random sample of n = {n} gives slope b = {g(b)} with SE_b = {g(se)}. '
    if lv == 'cp2':
        q += f'How many degrees of freedom does a confidence interval for the slope use?'
        ans = str(n - 2)
        steps = ['Inference for the slope uses df = n − 2.', f'df = {n} − 2 = {n - 2}.']
    else:
        q += f'Construct a {round(c * 100)}% confidence interval for the true slope β. Round the endpoints to three decimal places.'
        ans = f'({f(lo, 3)}, {f(hi, 3)})'
        steps = [f'df = n − 2 = {n - 2}; t* = {f(ts, 3)}.', f'b ± t*·SE_b = {g(b)} ± {f(ts, 3)}({g(se)}) = {g(b)} ± {f(ts * se, 4)}.', f'Interval: {ans}.']
        if lv == 'honors':
            steps.append('Zero is ' + ('not ' if lo > 0 or hi < 0 else '') + 'in the interval, so a slope of 0 is ' + ('not ' if lo > 0 or hi < 0 else '') + 'plausible.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['BEYOND.SLOPE'])


@fam(4, 12)
def gof_expected(rng, lv):
    cats, props = rng.choice([(['red', 'orange', 'yellow', 'green'], [0.3, 0.2, 0.2, 0.3]), (['bus', 'car', 'walk', 'bike'], [0.25, 0.4, 0.25, 0.1]),
                              (['A', 'B', 'C', 'D', 'F'], [0.15, 0.3, 0.35, 0.15, 0.05]), (['spring', 'summer', 'fall', 'winter'], [0.25, 0.25, 0.25, 0.25])])
    n = rng.choice([80, 120, 200, 240, 300])
    i = rng.randrange(len(cats))
    exp = n * props[i]
    if lv == 'cp2':
        q = f'A claim says the categories {", ".join(cats)} occur with proportions {", ".join(g(p) for p in props)}. In a goodness-of-fit test with n = {n}, what is the expected count for "{cats[i]}"?'
        ans = g(round(exp, 2))
        steps = ['Expected count = n × (claimed proportion).', f'{n} × {g(props[i])} = {ans}.']
        return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['BEYOND.GOF'])
    exps = [n * p for p in props]
    obs = [max(1, round(e + rng.choice([-6, -3, 0, 4, 7]))) for e in exps]
    obs[-1] = n - sum(obs[:-1])
    if obs[-1] <= 0:
        return None
    chi = sum((o - e) ** 2 / e for o, e in zip(obs, exps))
    q = (f'A claim says the categories {", ".join(cats)} occur with proportions {", ".join(g(p) for p in props)}. A random sample of {n} gives observed counts '
         f'{", ".join(map(str, obs))}. Find the chi-square statistic. Round to two decimal places.')
    ans = f(chi, 2)
    steps = ['Expected counts: ' + ', '.join(g(round(e, 2)) for e in exps) + '.', 'χ² = Σ (O − E)²/E = ' + ' + '.join(f'({o} − {g(round(e, 2))})²/{g(round(e, 2))}' for o, e in zip(obs, exps)) + f' ≈ {ans}.',
             f'df = {len(cats)} − 1 = {len(cats) - 1}.']
    if lv == 'honors':
        pv = stats.chi2.sf(chi, len(cats) - 1)
        steps.append(f'p-value ≈ {f(pv, 4)}, so {"reject H₀: the distribution differs from the claim" if pv < 0.05 else "fail to reject H₀: no convincing evidence against the claim"} at α = 0.05.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['BEYOND.GOF'])


@fam(4, 13)
def expected_two_way(rng, lv):
    rv, rows, cv, cols = rng.choice(TWOWAY)
    t = [[rng.randint(15, 70) for _ in cols] for _ in rows]
    i, j = rng.randrange(2), rng.randrange(2)
    R_, C_, N = sum(t[i]), t[0][j] + t[1][j], sum(map(sum, t))
    e = R_ * C_ / N
    table = '; '.join(f'{rows[r]}: {cols[0]} {t[r][0]}, {cols[1]} {t[r][1]}' for r in range(2))
    q = f'A chi-square test for independence uses these counts of {rv} and {cv} — {table}. Find the expected count for {rows[i]} and {cols[j]}. Round to two decimal places.'
    steps = ['Expected count = (row total × column total)/table total.', f'Row total {R_}, column total {C_}, table total {N}.', f'({R_} × {C_})/{N} ≈ {f(e, 2)}.']
    if lv == 'honors':
        exp = [[sum(t[r]) * (t[0][c] + t[1][c]) / N for c in range(2)] for r in range(2)]
        chi = sum((t[r][c] - exp[r][c]) ** 2 / exp[r][c] for r in range(2) for c in range(2))
        steps.append(f'All expected counts are at least 5, so the Large Counts condition holds; χ² ≈ {f(chi, 2)} with df = (2 − 1)(2 − 1) = 1.')
    return R(fmt='short-answer', prompt=q, answer=f(e, 2), steps=steps, codes=['3.15.A'])


@fam(4, 13)
def chisq_df_pvalue(rng, lv):
    r, c = rng.choice([(2, 3), (3, 3), (2, 4), (3, 4), (4, 3)])
    df = (r - 1) * (c - 1)
    chi = round(rng.uniform(3, 16), 2)
    pv = stats.chi2.sf(chi, df)
    who = rng.choice(['grade level and favorite lunch', 'age group and news source', 'region and preferred phone brand', 'class period and study habit'])
    if lv == 'cp2':
        q = f'A chi-square test for independence between {who} uses a two-way table with {r} rows and {c} columns. How many degrees of freedom does it have?'
        ans = str(df)
        steps = ['df = (rows − 1)(columns − 1).', f'({r} − 1)({c} − 1) = {df}.']
    else:
        q = f'A chi-square test for independence between {who} uses a table with {r} rows and {c} columns and gives χ² = {g(chi)}. Find the p-value. Use technology (χ²cdf). Round to four decimal places.'
        ans = f(pv, 4)
        steps = [f'df = ({r} − 1)({c} − 1) = {df}.', f'p-value = P(χ² ≥ {g(chi)}) with df = {df} ≈ {ans}.']
        if lv == 'honors':
            steps.append(f'At α = 0.05: {"reject H₀ — convincing evidence of an association" if pv < 0.05 else "fail to reject H₀ — no convincing evidence of an association"}.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['3.15.B'])


@fam(4, 14)
def slope_t_stat(rng, lv):
    x, y, sign = rng.choice([('hours of sleep', 'reaction time', -1), ('temperature', 'ice cream sales', 1), ('study time', 'quiz score', 1), ('engine size', 'fuel economy', -1), ('years of experience', 'salary', 1)])
    n = rng.choice([10, 14, 18, 22, 30])
    b = sign * rng.choice([1.8, 2.3, 0.62, 0.9, 4.1])
    se = round(abs(b) * rng.choice([0.4, 0.5, 0.7, 0.9]), 3)
    t = b / se
    q = f'A regression of {y} on {x} for a random sample of n = {n} gives b = {g(b)} and SE_b = {g(se)}. '
    if lv == 'cp2':
        q += 'Find the t statistic for H₀: β = 0. Round to two decimal places.'
        ans = f(t, 2)
        steps = ['t = (b − 0)/SE_b.', f'{g(b)}/{g(se)} ≈ {ans}.']
    else:
        pv = 2 * stats.t.sf(abs(t), n - 2)
        q += 'Find the p-value for H₀: β = 0 against Hₐ: β ≠ 0. Use technology. Round to four decimal places.'
        ans = f(pv, 4)
        steps = [f't = {g(b)}/{g(se)} ≈ {f(t, 3)}, df = n − 2 = {n - 2}.', f'p-value = 2P(t ≥ {f(abs(t), 3)}) ≈ {ans}.']
        if lv == 'honors':
            steps.append(f'At α = 0.05: {"reject H₀ — convincing evidence of a linear relationship" if pv < 0.05 else "fail to reject H₀ — no convincing evidence of a linear relationship"} between {x} and {y}.')
    return R(fmt='short-answer', prompt=q, answer=ans, steps=steps, codes=['BEYOND.SLOPE'])


# #9: the design-diagram families are listed twice so that diagrams make up a larger share of the new items
FAM[(2, 5)].append(design_diagram_counts)
FAM[(2, 7)].append(design_diagram_name)
FAM[(4, 7)].append(shaded_pvalue)
