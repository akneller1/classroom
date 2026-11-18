"""Precalculus audit #9: N-CN.B.4 is about complex numbers in polar form. Polar-coordinate and polar-equation items
(vectors skills 09 and 10) are tagged with AP Precalculus topics 3.13 and 3.14 instead; items that write a complex
number in trigonometric form keep N-CN.B.4. Idempotent."""
import re
from lib import load, save, items

banks = load()
n = 0
for _, q in items(banks):
    if q['skillId'] not in ('vectors-skill-09', 'vectors-skill-10') or 'N-CN.B.4' not in q['standards']:
        continue
    text = q['prompt'] + ' ' + ' '.join(p.get('prompt', '') for p in q.get('parts', []))
    if re.search(r'trigonometric \(polar\) form|i·sin|\bi\b', text):
        continue
    keep = [s for s in q['standards'] if s != 'N-CN.B.4']
    graph = re.search(r'petals|maximum distance|rose|cardioid|limaçon|Graph', text)
    add = ['APPC.3.14'] if graph and q['skillId'] == 'vectors-skill-10' else ['APPC.3.13']
    q['standards'] = keep + [a for a in add if a not in keep]
    n += 1
save(banks)
print('retagged', n)
