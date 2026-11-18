"""Calculus audit #14 (2026-11-18): AP Review skills practice what their names say.

- Justifying Solutions with Definitions and Theorems (AP Review skill 06): the IVT-counting and MVT-value
  computations become justification items: choose or name the theorem or test that supports a conclusion,
  with find-the-mistake items whose student justification is incomplete.
- Calculus Notation and Written Explanations (AP Review skill 07): the integral-property computations become
  notation, units and written-interpretation items.
Deterministic (seeded by item id) and idempotent.
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lib
from fractions import Fraction as F
from author import fr, mc, record, error_item, open_set

NAMES = ['Ava', 'Ben', 'Chloe', 'Dev', 'Elena', 'Femi', 'Hiro', 'Isla', 'Kai', 'Lena', 'Marco', 'Nia', 'Omar', 'Priya', 'Quinn', 'Rosa', 'Sam', 'Tariq', 'Uma', 'Vic', 'Wren', 'Yusuf', 'Zoe']
JUST_STD = ['AP FUN-1.A', 'AP FUN-1.B', 'AP FUN-4.A']
NOTE_STD = ['AP CHA-3.A', 'AP CHA-4.B', 'AP CHA-4.E']

CONTEXTS = [  # quantity, symbol, unit, time unit, reading of a rate
    ('the temperature of a room', 'T', '°F', 'hours', 'the temperature'),
    ('the amount of water in a tank', 'W', 'gallons', 'minutes', 'the amount of water'),
    ('the height of a balloon', 'H', 'feet', 'seconds', 'the height'),
    ('the number of people in a park', 'P', 'people', 'hours', 'the number of people'),
    ('the volume of air in a tire', 'V', 'cubic inches', 'seconds', 'the volume of air'),
]


def unit_rate(u, t):
    return f'{u} per {t[:-1]}'


# ---------------------------------------------------------------- justification (skill 06)

def justify(rng, level):
    kind = rng.choice(['max', 'min', 'ivt', 'mvt', 'infl', 'sdt', 'evt'] if level != 'cp2' else ['max', 'min', 'ivt', 'mvt', 'sdt'])
    c = rng.choice([-3, -2, -1, 1, 2, 4])
    if kind in ('max', 'min'):
        word = 'maximum' if kind == 'max' else 'minimum'
        ch = 'positive to negative' if kind == 'max' else 'negative to positive'
        q = f'f is differentiable and f′({c}) = 0. Which statement justifies that f has a relative {word} at x = {c}?'
        right = f'f′ changes from {ch} at x = {c}'
        dis = [f'f′({c}) = 0', f'f′ changes from {"negative to positive" if kind == "max" else "positive to negative"} at x = {c}', f'f({c}) is the largest value in the table' if kind == 'max' else f'f({c}) = 0']
        theorem = 'the First Derivative Test'
        why = f'A zero of f′ is only a candidate. By the First Derivative Test, f has a relative {word} where f′ changes from {ch}.'
        wrong_student = f'f′({c}) = 0, so f has a relative {word} at x = {c}.'
        mistake = 'f′(c) = 0 alone does not show an extremum (f′ might not change sign). State that f′ changes sign.'
    elif kind == 'ivt':
        ctx = rng.choice(CONTEXTS)
        a, b = sorted(rng.sample(range(20, 90, 5), 2))
        m = rng.choice([v for v in range(a + 1, b) if v % 5])
        q = f'{ctx[1]}(t) is {ctx[0]}, in {ctx[2]}, t {ctx[3]} after a start time. {ctx[1]} is continuous on [0, 6], {ctx[1]}(0) = {a}, and {ctx[1]}(6) = {b}. Which statement justifies that {ctx[1]}(c) = {m} for some c in (0, 6)?'
        right = f'{ctx[1]} is continuous on [0, 6] and {m} is between {ctx[1]}(0) = {a} and {ctx[1]}(6) = {b}, so the Intermediate Value Theorem applies'
        dis = [f'{ctx[1]} is increasing on [0, 6], so it must pass {m}', f'By the Mean Value Theorem, {ctx[1]}′(c) = {m} for some c',
               f'{m} is the average of {ctx[1]}(0) and {ctx[1]}(6)']
        theorem = 'the Intermediate Value Theorem'
        why = 'The IVT needs continuity on the closed interval and a target value between the endpoint values; both hold.'
        wrong_student = f'{ctx[1]}(0) = {a} and {ctx[1]}(6) = {b}, so {ctx[1]}(c) = {m} for some c.'
        mistake = 'Left out the hypothesis. The IVT needs the function to be continuous on [0, 6].'
    elif kind == 'mvt':
        a, b = 0, rng.choice([2, 4, 5])
        fa, fb = rng.randint(-5, 5), rng.randint(6, 30)
        slope = fr(F(fb - fa, b))
        q = f'f is continuous on [{a}, {b}] and differentiable on ({a}, {b}), with f({a}) = {fa} and f({b}) = {fb}. Which conclusion is justified, and by what?'
        right = f'f′(c) = {slope} for some c in ({a}, {b}), by the Mean Value Theorem'
        dis = [f'f(c) = {slope} for some c in ({a}, {b}), by the Mean Value Theorem', f'f′(c) = {slope} for some c in ({a}, {b}), by the Intermediate Value Theorem',
               f'f′(c) = 0 for some c in ({a}, {b}), by the Mean Value Theorem']
        theorem = 'the Mean Value Theorem'
        why = f'The MVT hypotheses hold, and the average rate of change is ({fb} − {fa}) ÷ ({b} − {a}) = {slope}.'
        wrong_student = f'The average rate is {slope}, so f′(c) = {slope} for some c.'
        mistake = f'Left out the hypotheses. The MVT needs f continuous on [{a}, {b}] and differentiable on ({a}, {b}).'
    elif kind == 'infl':
        q = f'f is twice differentiable and f″({c}) = 0. Which statement justifies that the graph of f has a point of inflection at x = {c}?'
        right = f'f″ changes sign at x = {c}'
        dis = [f'f″({c}) = 0', f'f′({c}) = 0', f'f′ changes sign at x = {c}']
        theorem = 'the definition of a point of inflection'
        why = 'A point of inflection is where concavity changes, that is, where f″ changes sign; f″ = 0 alone is not enough.'
        wrong_student = f'f″({c}) = 0, so there is a point of inflection at x = {c}.'
        mistake = 'f″(c) = 0 alone does not show an inflection point (f″ might not change sign). State that f″ changes sign.'
    elif kind == 'sdt':
        s = rng.choice([-1, 1])
        v = rng.choice([2, 3, 5, 6]) * s
        word = 'minimum' if v > 0 else 'maximum'
        q = f'f′({c}) = 0 and f″({c}) = {v}. What can you conclude about x = {c}, and why?'
        right = f'f has a relative {word} at x = {c} by the Second Derivative Test, because f′({c}) = 0 and f″({c}) {">" if v > 0 else "<"} 0'
        other = 'maximum' if word == 'minimum' else 'minimum'
        dis = [f'f has a relative {other} at x = {c} by the Second Derivative Test, because f′({c}) = 0 and f″({c}) {">" if v > 0 else "<"} 0',
               f'f has a point of inflection at x = {c}, because f′({c}) = 0', f'No conclusion is possible without the sign of f′ near x = {c}']
        theorem = 'the Second Derivative Test'
        why = f'f″({c}) {">" if v > 0 else "<"} 0 means the graph is concave {"up" if v > 0 else "down"} at the critical number, so it is a relative {word}.'
        wrong_student = f'f″({c}) = {v}, so f has a relative {other} at x = {c}.'
        mistake = f'Reversed the test. f″ {">" if v > 0 else "<"} 0 means concave {"up" if v > 0 else "down"}, which gives a relative {word}.'
    else:
        a, b = sorted(rng.sample(range(-4, 8), 2))
        q = f'f is continuous on [{a}, {b}]. Which statement is justified?'
        right = f'f has an absolute maximum and an absolute minimum on [{a}, {b}], by the Extreme Value Theorem'
        dis = [f'f has a relative maximum in ({a}, {b}), by the Mean Value Theorem', f'f′(c) = 0 for some c in ({a}, {b}), by the Extreme Value Theorem',
               f'f(c) = 0 for some c in ({a}, {b}), by the Intermediate Value Theorem']
        theorem = 'the Extreme Value Theorem'
        why = 'A function continuous on a closed interval has an absolute maximum and minimum there (EVT). Nothing is known about f′ or its zeros.'
        wrong_student = f'f′(c) = 0 for some c in ({a}, {b}), so f has an absolute maximum.'
        mistake = 'Assumed f is differentiable. The EVT needs only continuity on the closed interval, and the maximum might be at an endpoint.'
    return dict(kind=kind, q=q, right=right, dis=dis, theorem=theorem, why=why, wrong=wrong_student, mistake=mistake)


def fixq(p):
    return p[:-1] + '.' if p.endswith('?') and ('Write a sentence' in p or 'Name the ' in p) else p


def justify_item(q, rng, name):
    slot = int(q['id'][-3:])
    if slot == 15:
        parts = []
        for _ in range(4):
            j = justify(rng, q['level'])
            parts.append((fixq(j['q'].replace('Which statement justifies', 'Write a sentence that justifies').replace('Which conclusion is justified, and by what?', 'State a conclusion and the theorem that justifies it.').replace('Which statement is justified?', 'State a conclusion and the theorem that justifies it.')),
                           j['right'], j['why']))
        return open_set(q, 'just_open', 'Justifying Solutions with Definitions and Theorems', parts)
    j = justify(rng, q['level'])
    if slot in (14, 16):
        return error_item(q, 'just_error', name, j['q'], j['wrong'].rstrip('.'), j['right'], j['mistake'], [j['why']], JUST_STD)
    if q['format'] == 'multiple-choice':
        return record(q, 'just_choose', j['q'], j['right'], [j['why'], 'Each other choice either names the wrong theorem or leaves out a condition the theorem needs.'],
                      fmt='multiple-choice', options=mc(rng, j['right'], j['dis']), standards=JUST_STD)
    prompt = j['q'].replace('Which statement justifies', 'Name the theorem, test or definition that justifies').replace('Which conclusion is justified, and by what?', 'Name the theorem that guarantees a value c with f′(c) equal to the average rate of change.').replace('Which statement is justified?', 'Name the theorem that guarantees f has an absolute maximum and minimum on this interval.').replace('What can you conclude about', 'Name the test that classifies')
    prompt = fixq(prompt)
    ans = j['theorem'][0].upper() + j['theorem'][1:]
    if ans.startswith('The '):
        ans = ans[4:]
    return record(q, 'just_name', prompt, ans, [j['why'], f'So the justification is {j["theorem"]}.'], standards=JUST_STD)


# ---------------------------------------------------------------- notation and written explanations (skill 07)

def notation(rng, level):
    ctx = rng.choice(CONTEXTS)
    name, S, u, tu, reading = ctx
    t0 = rng.choice([2, 3, 4, 5])
    v = rng.choice([-6, -4, -3, -2, 2, 3, 5, 8])
    kind = rng.choice(['deriv', 'units1', 'units2', 'integral', 'avg', 'note'] if level != 'cp2' else ['deriv', 'units1', 'integral', 'note'])
    rate = unit_rate(u, tu)
    if kind == 'deriv':
        dirn = 'increasing' if v > 0 else 'decreasing'
        q = f'{S}(t) is {name}, in {u}, t {tu} after a start time. Which sentence interprets {S}′({t0}) = {v}?'
        right = f'At t = {t0} {tu}, {reading} is {dirn} at {abs(v)} {rate}.'
        dis = [f'At t = {t0} {tu}, {reading} is {v} {u}.', f'From t = 0 to t = {t0}, {reading} changes by {v} {u}.',
               f'At t = {t0} {tu}, {reading} is {dirn} at {abs(v)} {tu[:-1]}s per {u.rstrip("s") if u.endswith("s") else u}.']
        why = f'{S}′({t0}) is a rate of change at one instant, in {rate}; its sign tells whether {reading} is increasing or decreasing.'
        short = (f'{S}(t) is {name}, in {u}, t {tu} after a start time. Write a sentence that interprets {S}′({t0}) = {v}, with units.', right)
        wrong = dis[0]
        mistake = f'Read {S}′({t0}) as a value of {S}. It is a rate of change, in {rate}.'
    elif kind == 'units1':
        q = f'{S}(t) is {name}, in {u}, t {tu} after a start time. What are the units of {S}′(t)?'
        right = rate
        dis = [u, f'{tu[:-1]}s per {u}', f'{u} per {tu[:-1]} per {tu[:-1]}']
        why = f'A derivative divides a change in {S} ({u}) by a change in t ({tu}).'
        short = (q, right)
        wrong = dis[0]
        mistake = f'Gave the units of {S}. The derivative is a rate: {u} per {tu[:-1]}.'
    elif kind == 'units2':
        q = f'{S}(t) is {name}, in {u}, t {tu} after a start time. What are the units of {S}″(t)?'
        right = f'{u} per {tu[:-1]} per {tu[:-1]}'
        dis = [rate, u, f'{tu[:-1]}s per {u}']
        why = f'{S}″ is the rate of change of {S}′ (in {rate}) per {tu[:-1]}.'
        short = (q, right)
        wrong = rate
        mistake = f'Gave the units of {S}′. The second derivative divides those units by {tu[:-1]}s once more.'
    elif kind == 'integral':
        a, b = sorted(rng.sample(range(0, 10), 2))
        q = f'r(t) is the rate at which {reading} changes, in {rate}, t {tu} after a start time. What does ∫ from {a} to {b} r(t) dt represent, and in what units?'
        right = f'The net change in {reading} from t = {a} to t = {b}, in {u}'
        dis = [f'The rate of change of {reading} at t = {b}, in {rate}', f'The amount of {reading.replace("the ", "")} at t = {b}, in {u}',
               f'The average rate of change of {reading} from t = {a} to t = {b}, in {rate}']
        why = f'Integrating a rate ({rate}) over time ({tu}) gives a net change in {u}; it is not the amount at t = {b} unless the amount at t = {a} is 0.'
        short = (q, right[0].upper() + right[1:])
        wrong = dis[1]
        mistake = f'Gave the amount at t = {b}. The integral of the rate is the net change from t = {a} to t = {b}.'
    elif kind == 'avg':
        a, b = sorted(rng.sample(range(0, 12), 2))
        q = f'Which expression gives the average value of {S}(t) on {a} ≤ t ≤ {b}?'
        right = f'(1/{b - a})∫ from {a} to {b} {S}(t) dt' if b - a != 1 else f'∫ from {a} to {b} {S}(t) dt'
        dis = [f'({S}({b}) − {S}({a}))/{b - a}', f'∫ from {a} to {b} {S}(t) dt' if b - a != 1 else f'(1/2)∫ from {a} to {b} {S}(t) dt',
               f'(1/{b - a})∫ from {a} to {b} {S}′(t) dt' if b - a != 1 else f'∫ from {a} to {b} {S}′(t) dt']
        why = f'Average value = (1/(b − a))∫ from a to b {S}(t) dt. ({S}({b}) − {S}({a}))/{b - a} is the average rate of change, a different quantity.'
        short = (f'Write an expression for the average value of {S}(t) on {a} ≤ t ≤ {b}.', right)
        wrong = dis[0]
        mistake = 'Wrote the average rate of change of S. The average value of S uses the integral of S divided by the length of the interval.'.replace('S', S)
    else:
        q = f'Which notation means "the rate at which {reading} changes with respect to t when t = {t0}"?'
        right = f'{S}′({t0})'
        dis = [f'{S}({t0})', f'∫ from 0 to {t0} {S}(t) dt', f'({S}({t0}) − {S}(0))/{t0}']
        why = f'The instantaneous rate of change at t = {t0} is the derivative evaluated there, {S}′({t0}) (also written d{S}/dt at t = {t0}).'
        short = (q.replace('Which notation means', 'Write the notation for'), right)
        wrong = dis[3 - 1]
        mistake = f'Wrote an accumulation. The rate at t = {t0} is the derivative {S}′({t0}).'
    return dict(q=q, right=right, dis=dis, why=why, short=short, wrong=wrong, mistake=mistake)


def notation_item(q, rng, name):
    slot = int(q['id'][-3:])
    if slot == 15:
        parts = []
        for _ in range(4):
            n = notation(rng, q['level'])
            parts.append((n['short'][0], n['short'][1], n['why']))
        return open_set(q, 'note_open', 'Calculus Notation and Written Explanations', parts)
    n = notation(rng, q['level'])
    if slot in (14, 16):
        return error_item(q, 'note_error', name, n['short'][0], n['wrong'].rstrip('.'), n['short'][1].rstrip('.'), n['mistake'], [n['why']], NOTE_STD)
    if q['format'] == 'multiple-choice':
        return record(q, 'note_choose', n['q'], n['right'], [n['why']], fmt='multiple-choice', options=mc(rng, n['right'], n['dis']), standards=NOTE_STD)
    return record(q, 'note_write', n['short'][0], n['short'][1], [n['why'], f'Answer: {n["short"][1]}'], standards=NOTE_STD)


def main():
    banks = lib.load()
    n = {'just': 0, 'note': 0}
    d = banks['ap-review']
    out = []
    def kind(q):
        fam = lib.family(q) or ''
        if q['skillId'] == 'ap-review-skill-06' and fam.startswith(('cal_s8_ivt', 'cal_s10_mvt', 'just_')):
            return 'just'
        if q['skillId'] == 'ap-review-skill-07' and fam.startswith(('cal_s7_props', 'note_')):
            return 'note'
    # no prompt repeats word for word inside a skill: compare with untouched items and the ones already written
    used = {(q['skillId'], q['prompt']) for q in d['questions'] if not kind(q)}
    for q in d['questions']:
        k = kind(q)
        if k:
            name = NAMES[(int(q['id'][-3:]) * 7) % len(NAMES)]
            for attempt in range(40):
                rng = random.Random('cal-audit-14-' + q['id'] + ('' if attempt == 0 else f'-{attempt}'))
                new = (justify_item if k == 'just' else notation_item)(q, rng, name)
                if (q['skillId'], new['prompt']) not in used:
                    break
            used.add((q['skillId'], new['prompt']))
            q = new
            n[k] += 1
        out.append(q)
    d['questions'] = out
    lib.save(banks)
    print(n)


if __name__ == '__main__':
    main()
