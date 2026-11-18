"""Calculus audit #11 (2026-11-18): AP learning-objective tags that match the items.

- Volumes (applications of integrals skill 07): CHA-5.D is the BC polar-area objective; cross sections are
  CHA-5.B and solids of revolution CHA-5.C.
- Area between curves (skill 06) is CHA-5.A only (CHA-5.B is volume by cross sections).
- Interpreting definite integrals in context (skill 01) is CHA-4.A and CHA-4.D (CHA-4.B is average value).
- Recognizing a limit as a derivative (derivatives skill 01) adds LIM-3.A.
- Extreme Value Theorem justifications add FUN-1.C.
Idempotent.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lib


def fix(q):
    s = list(q['standards'])
    sk = q['skillId']
    if sk == 'applications-integrals-skill-07':
        cross = 'cross section' in (q['prompt'] + str(q.get('parts', ''))).lower()
        revo = 'revolved' in (q['prompt'] + str(q.get('parts', ''))).lower()
        s = [x for x in s if x not in ('AP CHA-5.D', 'AP CHA-5.B', 'AP CHA-5.C')]
        s += (['AP CHA-5.B'] if cross else []) + (['AP CHA-5.C'] if revo or not cross else [])
    if sk == 'applications-integrals-skill-06':
        s = [x for x in s if x != 'AP CHA-5.B'] or ['AP CHA-5.A']
    if sk == 'applications-integrals-skill-01':
        s = [x for x in s if x != 'AP CHA-4.B']
        if 'AP CHA-4.D' not in s:
            s.append('AP CHA-4.D')
    if sk == 'derivatives-skill-01' and 'AP LIM-3.A' not in s:
        s.append('AP LIM-3.A')
    if 'Extreme Value Theorem' in q.get('answer', '') and 'AP FUN-1.C' not in s:
        s.append('AP FUN-1.C')
    out = []
    for x in s:
        if x not in out:
            out.append(x)
    q['standards'] = out
    return q


if __name__ == '__main__':
    banks = lib.load()
    for u, d in banks.items():
        d['questions'] = [fix(q) for q in d['questions']]
    lib.save(banks)
