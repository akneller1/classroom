"""Precalculus audit #9: replace the 14 magnitude-only items (family g6_s5_tripled) in "Dot Products and Projections"
with dot-product problems, keeping each item's id, level and format. Idempotent: only items still in that family change."""
import math, random, re
from fractions import Fraction as F
from lib import load, save, items

NOTE = ("Original Claude-authored item (family: {fam}). Answer recomputed from the printed problem by "
        "tools/precalculus-audit-20261118/pc_verify.py. Teacher reviewed 2026-11-18.")


def v(a, b):
    return f"⟨{a}, {b}⟩"


def work(r, lv):
    while True:
        a, b, c, d = r.randint(-8, 12), r.randint(-8, 12), r.randint(1, 15), r.randint(-6, 10)
        W = a * c + b * d
        if W > 0 and a and b and d and len({W, a * c - b * d, abs(W) + 1, a * d + b * c}) == 4:
            break
    p = f"A constant force F = {v(a, b)} newtons pushes a crate along the displacement d = {v(c, d)} meters. Find the work done, W = F · d, in joules."
    steps = [f"W = F · d = ({a})({c}) + ({b})({d}).", f"= {a * c} + ({b * d}) = {W}.", f"The work done is {W} J."]
    wrong = [(f"{a * c - b * d} J", "subtracted the products"), (f"{a * d + b * c} J", "multiplied the wrong components"), (f"{round(math.hypot(a, b) * math.hypot(c, d), 1)} J", "multiplied the magnitudes")]
    return p, f"{W} J", steps, wrong, "dot_work"


def angle(r, lv):
    while True:
        a, b, c, d = [r.randint(-9, 9) for _ in range(4)]
        if (a or b) and (c or d) and a * d - b * c:
            t = math.degrees(math.acos((a * c + b * d) / (math.hypot(a, b) * math.hypot(c, d))))
            x = t * 10
            if abs(x - int(x) - 0.5) > 0.05 and 5 < t < 175:
                break
    p = f"Two boats leave a dock with velocity vectors {v(a, b)} and {v(c, d)} (km/h). Find the angle between their paths, to the nearest tenth of a degree."
    dot, m1, m2 = a * c + b * d, math.hypot(a, b), math.hypot(c, d)
    steps = [f"u · v = ({a})({c}) + ({b})({d}) = {dot}.", f"|u| = √{a * a + b * b} ≈ {m1:.4f} and |v| = √{c * c + d * d} ≈ {m2:.4f}.",
             f"cos θ = {dot}/({m1:.4f} · {m2:.4f}) ≈ {dot / (m1 * m2):.4f}, so θ ≈ {t:.1f}°."]
    wrong = [(f"{180 - t:.1f}°", "used the supplement of the angle"), (f"{math.degrees(math.asin(max(-1, min(1, dot / (m1 * m2))))):.1f}°", "used inverse sine instead of inverse cosine"),
             (f"{t + 1:.1f}°", "rounded the cosine too early")]
    return p, f"{t:.1f}°", steps, wrong, "dot_angle"


def ortho(r, lv):
    while True:
        a, c, d = r.randint(-9, 9), r.randint(-9, 9), r.randint(-9, 9)
        if a and c and d and (a * c) % d == 0 and -a * c // d not in (0,):
            k = -a * c // d
            if abs(k) <= 20 and len({k, -k, a * c, d}) == 4:
                break
    p = f"Find k so that the vectors {v(a, 'k')} and {v(c, d)} are orthogonal."
    steps = [f"Orthogonal vectors have dot product 0: ({a})({c}) + k({d}) = 0.", f"{a * c} + {d}k = 0, so k = {-a * c}/{d} = {k}."]
    wrong = [(f"k = {-k}", "made a sign error"), (f"k = {a * c}", "did not divide by the other component"), (f"k = {d}", "copied a component")]
    return p, f"k = {k}", steps, wrong, "dot_orthogonal"


def comp(r, lv):
    vs = [(3, 4), (4, 3), (-3, 4), (5, 12), (12, 5), (-6, 8), (8, -6), (0, 5), (5, 0)]
    while True:
        a, b = r.randint(-9, 9), r.randint(-9, 9)
        c, d = r.choice(vs)
        m = int(math.hypot(c, d))
        val = F(a * c + b * d, m)
        if (a or b) and val != 0 and len({val, -val, a * c + b * d}) == 3:
            break
    s = str(val) if val.denominator == 1 else f"{val.numerator}/{val.denominator}"
    p = f"A rope pulls on a sled with force u = {v(a, b)} newtons. Find the scalar projection (component) of u in the direction v = {v(c, d)}: comp_v u = (u · v)/|v|."
    steps = [f"u · v = ({a})({c}) + ({b})({d}) = {a * c + b * d}.", f"|v| = √({c}² + {d}²) = {m}.", f"comp_v u = {a * c + b * d}/{m} = {s}."]
    wrong = [(str(a * c + b * d), "did not divide by |v|"), (str(-val) if val.denominator == 1 else f"{-val.numerator}/{val.denominator}", "made a sign error"),
             (str(F(a * c + b * d, m * m)) if F(a * c + b * d, m * m).denominator > 1 else str(F(a * c + b * d, m * m)), "divided by |v|² (that gives the projection's scale factor)")]
    return p, s, steps, wrong, "dot_component"


FAMS = {'cp2': [work, ortho, comp], 'cp1': [work, ortho, comp, angle], 'honors': [angle, comp, work, ortho]}
banks = load()
r = random.Random('pc-audit-9')
changed = 0
for f, q in items(banks):
    if q['skillId'] != 'vectors-skill-08' or 'family: g6_s5_tripled' not in q.get('sourceNotes', ''):
        continue
    fns = FAMS[q['level']]
    p, ans, steps, wrong, fam = fns[changed % len(fns)](r, q['level'])
    q['prompt'], q['answer'], q['solutionSteps'] = p, ans, steps
    if q['format'] == 'multiple-choice':
        opts = [{'text': ans, 'correct': True}] + [{'text': w, 'correct': False} for w, _ in wrong[:3]]
        assert len({o['text'] for o in opts}) == 4, opts
        r.shuffle(opts)
        q['options'] = opts
    q['standards'] = ['N-VM.B.4', 'N-VM.A.3']  # as the skill's other dot-product items
    q['sourceNotes'] = NOTE.format(fam=fam)
    changed += 1
save(banks)
print('replaced', changed)
