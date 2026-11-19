"""Behavior of implicitly defined relations (AP Calculus FUN-4.D and FUN-4.E, Topic 5.12).

Adds six short-answer items per level to applications-derivatives-skill-02 (critical numbers), so the two learning
objectives that had no question-bank practice are covered:
  - s2_impl_h  horizontal tangents of x² ± xy + y² = c   (FUN-4.D: critical points of implicit relations)
  - s2_impl_v  vertical tangents of the same curves       (FUN-4.D)
  - s2_impl_b  sign of dy/dx and d²y/dx² at a point on a circle or ellipse, and what they say about the curve (FUN-4.E)
Every answer is computed with exact fractions and checked (point on the curve, numerator or denominator of dy/dx zero,
second derivative from the implicit formula) before it is written. Short answer only, so the AP practice exams, which
draw multiple-choice items, are unchanged. Idempotent: items whose ids already exist are replaced.

Run from the repository root: python3 tools/calculus-audit-20261118/implicit_behavior.py
"""
import json, os, sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(__file__))
import lib

UNIT, SKILL = 'applications-derivatives', 'applications-derivatives-skill-02'
NOTE = ('Original Claude-authored item (family: {fam}). Calculus audit 2026-11-18 follow-up (FUN-4.D/E had no practice); '
        'answer computed with exact arithmetic in tools/calculus-audit-20261118/implicit_behavior.py.')


def num(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f'{v.numerator}/{v.denominator}'


def pt(a, b):
    return f'({num(a)}, {num(b)})'


def tangents(s, a, kind):
    """x² + s·xy + y² = 3a² with s = ±1. dy/dx = -(2x + s·y)/(s·x + 2y)."""
    c = 3 * a * a
    sign = '+' if s == 1 else '-'
    curve = f'x² {sign} xy + y² = {c}'
    f = lambda x, y: x * x + s * x * y + y * y
    N = lambda x, y: 2 * x + s * y          # dy/dx = -N/D
    D = lambda x, y: s * x + 2 * y
    if kind == 'h':   # N = 0: y = -2x/s = -2s·x
        pts = [(a, -2 * s * a), (-a, 2 * s * a)]
        for x, y in pts:
            assert f(x, y) == c and N(x, y) == 0 and D(x, y) != 0
        rel, cond = f'y = {"-" if s == 1 else ""}2x', 'numerator'
        sub = f'x² {sign} x({"-" if s == 1 else ""}2x) + ({"-" if s == 1 else ""}2x)² = 3x² = {c}, so x = ±{a}'
    else:             # D = 0: x = -2s·y
        pts = [(-2 * s * a, a), (2 * s * a, -a)]
        for x, y in pts:
            assert f(x, y) == c and D(x, y) == 0 and N(x, y) != 0
        rel, cond = f'x = {"-" if s == 1 else ""}2y', 'denominator'
        sub = f'({"-" if s == 1 else ""}2y)² {sign} ({"-" if s == 1 else ""}2y)y + y² = 3y² = {c}, so y = ±{a}'
    word = 'horizontal' if kind == 'h' else 'vertical'
    other = 'denominator' if kind == 'h' else 'numerator'
    prompt = f'The curve {curve} defines y implicitly as a relation in x. Find every point on the curve where the tangent line is {word}.'
    answer = f'{pt(*pts[0])} and {pt(*pts[1])}'
    steps = [f'Differentiate implicitly: 2x {sign} (y + x·y′) + 2y·y′ = 0, so y′ = -(2x {sign} y)/({"x + 2y" if s == 1 else "2y - x"}).',
             f'A {word} tangent needs the {cond} to be 0 while the {other} is not: {rel}.',
             f'Substitute into the curve: {sub}.',
             f'Points: {answer}. At each point the {other} of y′ is not 0.']
    return prompt, answer, steps, ['AP FUN-4.D'], ['multistep']


def behavior(A, B, x0, y0):
    """A·x² + B·y² = c at (x0, y0). y′ = -A·x/(B·y); y″ = -A·c/(B²·y³)."""
    c = A * x0 * x0 + B * y0 * y0
    d1 = F(-A * x0, B * y0)
    d2 = F(-A * c, B * B * y0 ** 3)
    # independent check of y″ by the quotient rule: y″ = -A(B·y - B·x·y′)/(B·y)²
    assert d2 == F(-A, 1) * (B * y0 - B * x0 * d1) / (B * y0) ** 2
    lhs = ('x²' if A == 1 else f'{A}x²') + ' + ' + ('y²' if B == 1 else f'{B}y²')
    inc = 'increasing' if d1 > 0 else 'decreasing'
    cc = 'concave up' if d2 > 0 else 'concave down'
    prompt = (f'The curve {lhs} = {c} passes through {pt(x0, y0)}. Find dy/dx and d²y/dx² at that point, then say whether '
              f'y is increasing or decreasing and whether the curve is concave up or concave down there.')
    answer = f'dy/dx = {num(d1)}, d²y/dx² = {num(d2)}; {inc}, {cc}'
    a2, b2 = ('2x' if A == 1 else f'{2 * A}x'), ('2y' if B == 1 else f'{2 * B}y')
    k1, k2 = F(A, B), F(-A * c, B * B)          # y′ = -k1·x/y, y″ = k2/y³
    yp = ('-x/y' if k1 == 1 else f'-x/({num(1 / k1)}y)' if k1.numerator == 1 else f'-{num(k1)}x/y')
    ypp = (f'-{num(-k2)}/y³' if k2.denominator == 1 else f'-{k2.numerator * -1}/({k2.denominator}y³)')
    steps = [f'Differentiate implicitly: {a2} + {b2}·y′ = 0, so y′ = {yp}.',
             f'At {pt(x0, y0)}: y′ = {num(d1)}.',
             f'Differentiate y′ again and substitute y′ and {lhs} = {c}: y″ = {ypp}.',
             f'At {pt(x0, y0)}: y″ = {num(d2)}.',
             f'y′ {"> 0" if d1 > 0 else "< 0"}, so y is {inc}; y″ {"> 0" if d2 > 0 else "< 0"}, so the curve is {cc} there.']
    return prompt, answer, steps, ['AP FUN-4.E'], ['reasoning']


PLAN = {
    'cp2':    [('s2_impl_h', tangents, (1, 1, 'h')), ('s2_impl_h', tangents, (1, 2, 'h')),
               ('s2_impl_v', tangents, (1, 3, 'v')), ('s2_impl_v', tangents, (1, 4, 'v')),
               ('s2_impl_b', behavior, (1, 1, 3, 4)), ('s2_impl_b', behavior, (1, 1, -6, 8))],
    'cp1':    [('s2_impl_h', tangents, (1, 5, 'h')), ('s2_impl_h', tangents, (1, 6, 'h')),
               ('s2_impl_v', tangents, (1, 7, 'v')), ('s2_impl_v', tangents, (1, 8, 'v')),
               ('s2_impl_b', behavior, (1, 1, 5, -12)), ('s2_impl_b', behavior, (1, 1, -8, -15))],
    'honors': [('s2_impl_h', tangents, (-1, 2, 'h')), ('s2_impl_h', tangents, (-1, 3, 'h')),
               ('s2_impl_v', tangents, (-1, 4, 'v')), ('s2_impl_v', tangents, (-1, 5, 'v')),
               ('s2_impl_b', behavior, (1, 4, 2, 1)), ('s2_impl_b', behavior, (1, 4, 4, -1))],
}


def main():
    banks, tags = lib.load(), lib.tags()
    qs, meta = banks[UNIT]['questions'], tags[UNIT]
    new = []
    for level, plan in PLAN.items():
        for k, (fam, fn, args) in enumerate(plan, 1):
            prompt, answer, steps, std, tg = fn(*args)
            qid = f'cal-app-s02-{level}-i{k:03d}'
            new.append({'id': qid, 'skillId': SKILL, 'level': level, 'format': 'short-answer', 'prompt': prompt,
                        'answer': answer, 'solutionSteps': steps, 'standards': std, 'sourceNotes': NOTE.format(fam=fam)})
            meta[qid] = tg
    ids = {q['id'] for q in new}
    qs[:] = [q for q in qs if q['id'] not in ids]
    last = max(i for i, q in enumerate(qs) if q['skillId'] == SKILL)
    qs[last + 1:last + 1] = new
    others = {q['prompt'] for q in qs if q['id'] not in ids}
    assert len({q['prompt'] for q in new}) == len(new) and not any(q['prompt'] in others for q in new), 'duplicate prompt'
    lib.save(banks)
    f = os.path.join(lib.BANKS, 'meta', UNIT + '.tags.json')
    raw = open(f, encoding='utf-8').read()
    # the tag files are written with indent=0 and no final newline (tools/calculus-audit-20261118/add_topics.py)
    open(f, 'w', encoding='utf-8').write(json.dumps(meta, ensure_ascii=False, indent=0) + ('\n' if raw.endswith('\n') else ''))
    print(f'{len(new)} implicit-relation items in {SKILL} (FUN-4.D, FUN-4.E)')


if __name__ == '__main__':
    main()
