"""Shared helpers for authoring Calculus bank items: exact formatting in the bank's text style and item records."""
from fractions import Fraction as F
import random, re

SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
NOTE = 'Original Claude-authored item (family: {fam}). Calculus audit 2026-11-18; answer computed with exact arithmetic in tools/calculus-audit-20261118 and re-checked by verify_keys.py.'


def fr(v):
    """A number in bank style: integers plain, fractions a/b, negatives with a leading '-'."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f'{v.numerator}/{v.denominator}'


def par(v):
    """A number ready to follow an operator: negatives in parentheses."""
    s = fr(v)
    return f'({s})' if s.startswith('-') else s


def term(c, p, var='x'):
    c = F(c)
    mag = abs(c)
    if p == 0:
        body = fr(mag)
    else:
        co = '' if mag == 1 else (fr(mag) if mag.denominator == 1 else f'({fr(mag)})')
        body = co + var + ('' if p == 1 else str(p).translate(SUP))
    return body


def poly(coeffs, var='x'):
    """coeffs: {power: coefficient}. Returns '3x² - 2x + 5'."""
    out = ''
    for p in sorted(coeffs, reverse=True):
        c = F(coeffs[p])
        if c == 0:
            continue
        t = term(c, p, var)
        if not out:
            out = ('-' if c < 0 else '') + t
        else:
            out += (' - ' if c < 0 else ' + ') + t
    return out or '0'


def peval(coeffs, x):
    return sum(F(c) * F(x) ** p for p, c in coeffs.items())


def pint(coeffs):
    return {p + 1: F(c) / (p + 1) for p, c in coeffs.items() if c}


def pdiff(coeffs):
    return {p - 1: F(c) * p for p, c in coeffs.items() if p > 0 and c}


def interval(a, b):
    def e(v):
        return '∞' if v == 'oo' else ('-∞' if v == '-oo' else fr(v))
    return f'({e(a)}, {e(b)})'


def union(parts):
    return ' ∪ '.join(parts) if parts else 'none'


def mc(rng, correct, distractors):
    """Four options, one correct, deduplicated, shuffled with the given rng."""
    seen, opts = {correct}, [correct]
    for d in distractors:
        if d not in seen:
            seen.add(d)
            opts.append(d)
        if len(opts) == 4:
            break
    if len(opts) < 4:
        raise ValueError('not enough distinct distractors for ' + correct)
    rng.shuffle(opts)
    return [{'text': o, 'correct': o == correct} for o in opts]


def record(base, fam, prompt, answer, steps, fmt='short-answer', options=None, parts=None, diagram=None, standards=None):
    q = {'id': base['id'], 'skillId': base['skillId'], 'level': base['level'], 'format': fmt, 'prompt': prompt, 'answer': answer}
    if options:
        q['options'] = options
    if parts:
        q['parts'] = parts
    if diagram:
        q['diagram'] = diagram
    q['solutionSteps'] = steps
    q['standards'] = standards or base['standards']
    q['sourceNotes'] = NOTE.format(fam=fam)
    return q


def error_item(base, fam, name, problem, student, key, mistake, work, standards=None):
    prompt = f"{name} answered this problem incorrectly.\n{problem}\n{name}'s answer: {student}\nIdentify the mistake and give the correct answer."
    steps = ['Mistake: ' + mistake] + work + [f'The correct answer is {key}, not {student}.']
    return record(base, fam, prompt, key, steps, standards=standards)


def open_set(base, fam, skill_name, parts):
    """parts: list of (prompt, answer, step) tuples."""
    labels = 'abcd'
    return record(base, fam, f'Practice set ({skill_name}): answer each part and show your work.',
                  '; '.join(f'({labels[i]}) {a}' for i, (_, a, _) in enumerate(parts)),
                  [f'({labels[i]}) {s}' for i, (_, _, s) in enumerate(parts)], fmt='open-response',
                  parts=[{'label': labels[i], 'prompt': p, 'answer': a} for i, (p, a, _) in enumerate(parts)])
