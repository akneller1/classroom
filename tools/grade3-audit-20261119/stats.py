"""Print template-reuse shares for the overlay as built (for the audit doc)."""
import collections, sys
from lib import load_base, Overlay, mask
import fixes, importlib
o = Overlay(*load_base()); fixes.run(o)
for m in sys.argv[1:]: importlib.import_module(m).run(o)
Q = list(o.items())
def share(L, lo):
    low = {q['skillId'] + '|' + mask(q['prompt']) for q in Q if q['level'] in lo}
    xs = [q for q in Q if q['level'] == L]
    return sum(q['skillId'] + '|' + mask(q['prompt']) in low for q in xs), len(xs)
print('honors', share('honors', ['cp2', 'cp1']), 'cp1', share('cp1', ['cp2']), 'total', len(Q))
print(collections.Counter(q['format'] for q in Q))
