"""1st Grade Math audit (2026-11-19): small content fixes.

#11: 16 telling-time items were also tagged 3.MD.A.1, a Grade 3 standard; they keep only 1.MD.B.3.
#12: telling-time skill 3 had 34, 32 and 36 items by level because six Standard items (IDs ...-cp1-...) had been
placed at Advanced. Two of them go back to Standard, so each level has 34.
#13: duplicates: m1-at-s04-cp2-023 repeated -014, and m1-dt-s02-cp2-015 and -023 repeated -004."""
from lib import UNITS


def run(o):
    for u in UNITS:
        for q in list(o.items(u)):
            if '3.MD.A.1' in (q.get('standards') or []):
                o.edit(q['id'], standards=[s for s in q['standards'] if s != '3.MD.A.1'])
    for qid in ('m1-tt-s03-cp1-002', 'm1-tt-s03-cp1-017'):
        o.edit(qid, level='cp1')
    o.edit('m1-at-s04-cp2-023', prompt='What is 8 − 4? Think: 4 + what makes 8?', answer='4', solutionSteps=['4 + 4 = 8.', 'So 8 − 4 = 4.'])
    o.meta_set('m1-at-s04-cp2-023', explanation='4 + 4 = 8, so 8 − 4 = 4.')
    for qid, b, m in (('m1-dt-s02-cp2-015', 1, 4), ('m1-dt-s02-cp2-023', 2, 1)):
        o.edit(qid, prompt=f'A tally row has {b} {"bundle" if b == 1 else "bundles"} of 5 and {m} more {"mark" if m == 1 else "marks"}. What number is that?', answer=str(5 * b + m),
               solutionSteps=['Count each bundle as 5, then add the extra marks.', f'{" + ".join(["5"] * b)} + {m} = {5 * b + m}.'])
        o.meta_set(qid, explanation=f'{" + ".join(["5"] * b)} + {m} = {5 * b + m}.')
