"""2nd Grade Math audit (2026-11-19): small content fixes.

#10: "a closed shape with 6 straight angles" (or "straight corners"). A straight angle is 180 degrees, so the shape
items now say "6 angles".
#17: a plural after 1 (1 pets, 1 shells, 1 cubes)."""
import json, re
from lib import UNITS

ANGLES = re.compile(r'(\d) straight (?:angles|corners)')
ONE = re.compile(r'(?<![\d/,.$])1 (pet|shell|cube)s\b')


def fix_text(s):
    return ONE.sub(r'1 \1', ANGLES.sub(r'\1 angles', s))


def walk(v):
    if isinstance(v, str):
        return fix_text(v)
    if isinstance(v, list):
        return [walk(x) for x in v]
    if isinstance(v, dict):
        return {k: walk(x) for k, x in v.items()}
    return v


def run(o):
    for u in UNITS:
        for q in list(o.items(u)):
            fields = {}
            for f in ('prompt', 'answer', 'options', 'parts', 'solutionSteps'):
                if f in q and q[f] is not None:
                    new = walk(q[f])
                    if json.dumps(new) != json.dumps(q[f]):
                        fields[f] = new
            if fields:
                o.edit(q['id'], **fields)
