"""2nd Grade Math audit #15: add the number-line plot items built and checked by plots.cjs (plots.json)."""
import json, os


def run(o):
    items = json.load(open(os.path.join(os.path.dirname(__file__), 'plots.json'), encoding='utf-8'))
    for it in items:
        unit = it.pop('unit')
        same = [q for q in o.items(unit) if q['skillId'] == it['skillId']]
        std = max((q['standards'] for q in same), key=lambda s: sum(1 for q in same if q['standards'] == s))
        q = {k: it[k] for k in ('id', 'skillId', 'level', 'format', 'prompt', 'answer', 'solutionSteps')}
        q.update({'standards': std, 'sourceNotes': it['sourceNotes'], 'plot': it['plot'], 'courseId': 'grade2'})
        o.add(unit, q)
