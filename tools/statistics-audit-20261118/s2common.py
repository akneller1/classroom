"""Shared helpers and contexts for Statistics audit batch S2 (2026-11-18).
Every number in a generated item is computed here with Python and scipy; prompts state the rounding and the Normal-table
convention used by the banks (z rounded to two decimal places for Table A; t and chi-square values from technology)."""
import math
from decimal import Decimal, ROUND_HALF_UP
from scipy import stats

NOTE = ('Original Claude-authored item (family: {fam}). Statistics audit 2026-11-18, batch S2; key computed with scipy in '
        'tools/statistics-audit-20261118/s2fill.py or s2frq.py.')
LEVELS = ['cp2', 'cp1', 'honors']
UNIT_NO = {'exploring-data': 1, 'sampling-experimentation': 2, 'anticipating-patterns': 3, 'statistical-inference': 4}
UNIT_OF = {v: k for k, v in UNIT_NO.items()}
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')


def f(v, d=4):
    """Fixed decimals (halves rounded away from zero) with a true minus sign."""
    s = str(Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))
    if s.startswith('-') and float(s) == 0:
        s = s[1:]
    return s.replace('-', '−')


def g(v):
    """Short form for parameters (no trailing zeros)."""
    s = f'{v:.6f}'.rstrip('0').rstrip('.')
    return s.replace('-', '−')


def wt(who):
    """Relative pronoun for a PROP population."""
    return 'that' if who.split()[0] in ('seeds', 'flights', 'phones') else 'who'


def pct(p):
    return g(round(p * 100, 4)) + '%'


def table_a(z):
    """P(Z < z) from Table A: z rounded to two decimal places, area to four."""
    return round(stats.norm.cdf(round(z, 2)), 4)


def tstar(conf, df):
    return stats.t.ppf(1 - (1 - conf) / 2, df)  # exact t* (the banks' convention); shown to three decimals


ZSTAR = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}


def mc(rng, key, wrong):
    opts = [key] + [w for w in dict.fromkeys(wrong) if w != key][:3]
    assert len(opts) == 4, (key, wrong)
    rng.shuffle(opts)
    return [{'text': o, 'correct': o == key} for o in opts]


def skill_id(unit_no, k):
    return f'{UNIT_OF[unit_no]}-skill-{k:02d}'


def item(qid, unit_no, k, level, fmt, prompt, answer, steps, codes, fam, rng=None, wrong=None, diagram=None, extra=None):
    assert len(steps) >= 2, qid
    q = {'id': qid, 'skillId': skill_id(unit_no, k), 'level': level, 'format': fmt, 'prompt': prompt, 'answer': answer,
         'solutionSteps': steps, 'standards': ['APSTATS.' + c for c in codes], 'sourceNotes': NOTE.format(fam=fam)}
    if fmt == 'multiple-choice':
        q['options'] = mc(rng, answer, wrong)
    if diagram:
        q['diagram'] = diagram
    if extra:
        q.update(extra)
    return q


# Quantitative contexts: variable, unit, population, mean, SD, decimals for data values
QUANT = [
    ('battery life of a brand of phone', 'hours', 'phones of this brand', 18.0, 2.5, 1),
    ('time students spend on homework per night', 'minutes', 'students at a large high school', 52.0, 14.0, 0),
    ('weight of a bag of chips filled by a machine', 'grams', 'bags filled by the machine', 283.0, 4.0, 1),
    ('one-way commute time of workers in a city', 'minutes', 'workers in the city', 27.0, 9.0, 0),
    ('sleep teenagers get on a school night', 'hours', 'teenagers in the state', 7.1, 1.2, 1),
    ('height of adult women in a country', 'inches', 'adult women in the country', 64.2, 2.8, 1),
    ('amount of soda dispensed into a 12-ounce cup', 'ounces', 'cups filled by the dispenser', 11.8, 0.3, 2),
    ('length of a song on a streaming chart', 'minutes', 'songs on the chart', 3.4, 0.6, 2),
    ('reaction time of drivers to a brake light', 'milliseconds', 'licensed drivers', 240.0, 35.0, 0),
    ('daily water use of a household', 'gallons', 'households in the town', 310.0, 60.0, 0),
    ('weight of a newborn baby at a hospital', 'pounds', 'babies born at the hospital', 7.5, 1.1, 1),
    ('price of a used textbook online', 'dollars', 'used textbooks listed online', 42.0, 11.0, 2),
    ('resting pulse rate of adults', 'beats per minute', 'adults in the region', 72.0, 9.0, 0),
    ('diameter of a bolt from a factory', 'millimeters', 'bolts made by the factory', 12.0, 0.08, 2),
    ('delivery time of a pizza chain', 'minutes', 'deliveries by the chain', 31.0, 6.0, 0),
    ('score on a state reading test', 'points', 'students who took the test', 500.0, 100.0, 0),
]

# Proportion contexts: who, has the property (verb phrase), true proportion
PROP = [
    ('adults in a city', 'own an electric or hybrid car', 0.14),
    ('students at a large high school', 'have a part-time job', 0.32),
    ('households in a county', 'have a pet dog', 0.38),
    ('voters in a state', 'support a new park tax', 0.55),
    ('customers of an online store', 'return at least one item a year', 0.22),
    ('teenagers in the country', 'say they get enough sleep', 0.27),
    ('seeds of a tomato variety', 'sprout within a week', 0.85),
    ('flights at an airport', 'leave on time', 0.78),
    ('adults in a town', 'read a printed newspaper weekly', 0.18),
    ('phones made at a plant', 'have a cosmetic defect', 0.06),
    ('students in a district', 'walk or bike to school', 0.24),
    ('patients at a clinic', 'miss their appointment', 0.12),
    ('visitors to a museum', 'are from out of state', 0.41),
    ('drivers in a state', 'wear a seat belt', 0.91),
    ('employees at a large company', 'work from home at least one day a week', 0.46),
    ('library members', 'borrow an e-book in a month', 0.35),
]


def phrase_list(vals, d):
    return ', '.join(f(v, d) for v in vals)


def mean_sd(vals):
    n = len(vals)
    m = sum(vals) / n
    s = math.sqrt(sum((v - m) ** 2 for v in vals) / (n - 1))
    return m, s
