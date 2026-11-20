"""3rd Grade Math audit (2026-11-19): small content fixes.

#15: a plural after 1 (1 pets, 1 sections, 1 strings, 1 square units, 1 parts, 1 rolls).
#16: true/false items whose "The correct answer is 0" choice is not a mistake a student would make. (The 0 choices in
the 0-and-1 facts and same-perimeter items are real mistakes and stay.)"""


def opts(o, qid, old, new):
    cur = o.cur(qid, 'options')
    assert any(x['text'] == old for x in cur), (qid, old)
    return [dict(x, text=new) if x['text'] == old else x for x in cur]


def run(o):
    # #15
    o.edit('m3-dv-s02-honors-004', answer='1 string', solutionSteps=['40 ÷ 8 = 5 strings and 40 ÷ 10 = 4 strings.', '5 − 4 = 1 string.'])
    o.meta_set('m3-dv-s02-honors-004', explanation='5 − 4 = 1 string.')
    o.edit('m3-gd-s01-cp2-005', options=opts(o, 'm3-gd-s01-cp2-005', '1 pets', '1 pet'))
    o.edit('m3-gd-s02-cp2-003', answer='1 pet')
    o.edit('m3-gd-s02-cp1-009', options=opts(o, 'm3-gd-s02-cp1-009', '1 pets', '1 pet'))
    o.edit('m3-ps-s03-honors-010', answer='1 square unit', options=opts(o, 'm3-ps-s03-honors-010', '1 square units', '1 square unit'),
           solutionSteps=['A: 35. B: 36.', 'The difference is 1 square unit.'])
    for qid in ('m3-uf-s02-cp2-003', 'm3-uf-s02-cp2-017'):
        p = o.cur(qid, 'prompt')
        o.edit(qid, prompt=p.replace('paints 1 sections', 'paints 1 section'), solutionSteps=['The whole has 2 equal parts; 1 is painted.', '1/2.'])
    o.edit('m3-uf-s02-honors-009', options=opts(o, 'm3-uf-s02-honors-009', '1/8, because 1 parts are white', '1/8, because 1 part is white'))
    o.edit('m3-uf-s02-honors-015', options=opts(o, 'm3-uf-s02-honors-015', '1/4, because 1 parts are white', '1/4, because 1 part is white'))
    # #16
    o.edit('m3-as-s01-cp2-028', options=opts(o, 'm3-as-s01-cp2-028', 'False. The correct answer is 0 pages.', 'False. The correct answer is 36 pages.'))
    o.edit('m3-ec-s03-cp1-028', options=opts(o, 'm3-ec-s03-cp1-028', 'False. The correct answer is 0.', 'False. The correct answer is 12.'))
    o.edit('m3-ec-s03-honors-028', options=opts(o, 'm3-ec-s03-honors-028', 'False. The correct answer is 0.', 'False. The correct answer is 64.'))
