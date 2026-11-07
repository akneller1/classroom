"""Builds the 2026-11-07 Interactive Math tool pages: artifacts/<slug>/index.html from src/<slug>.js and manifest.json.
Same page template as tools/interactive-math-20261105/build.py, plus lab-plus.js and the middle-school,
Precalculus and Calculus course names. Run from the repository root:
    python3 tools/interactive-math-20261107/build.py"""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
M = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
COURSE = {'algebra': 'Algebra 1', 'algebra2': 'Algebra 2', 'geometry': 'Geometry', 'math6': '6th Grade Math',
          'prealgebra7': 'Pre-Algebra (7th)', 'prealgebra': 'Pre-Algebra (8th)', 'precalculus': 'Precalculus', 'calculus': 'Calculus'}
TPL = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · Mr. K's Classroom</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap">
<link rel="stylesheet" href="../interactive-math/lab.css?v={labver}">
</head><body><main id="app"></main><noscript><p style="padding:20px">This tool needs JavaScript.</p></noscript>
<script src="../interactive-math/lab.js?v={labver}"></script>
<script src="../interactive-math/lab-plus.js?v={ver}"></script>
<script>
(function () {{
'use strict';
var L = Lab;
var P = L.layout({meta});
{src}
}})();
</script>
</body></html>
'''
VER = M.get('version', '1')
LABVER = M.get('labVersion', '20261105')
only = os.environ.get('ONLY')
n = 0
for t in M['tools']:
    if only and t['slug'] != only: continue
    src = open(os.path.join(HERE, 'src', t['slug'] + '.js'), encoding='utf-8').read()
    meta = json.dumps({'course': COURSE[t['course']], 'unit': t['unitName'], 'title': t['title'], 'intro': t['intro']}, ensure_ascii=False)
    out = os.path.join(ROOT, 'artifacts', t['slug'])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(TPL.format(title=html.escape(t['title']), meta=meta, src=src, ver=VER, labver=LABVER))
    n += 1
print('built', n, 'tools')
