"""Builds the Interactive Math tool pages: artifacts/<slug>/index.html from src/<slug>.js and manifest.json.
Run from the repository root:  python3 tools/interactive-math-20261105/build.py"""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
M = json.load(open(os.environ.get('MANIFEST') or os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
M['tools'] = [t for t in M['tools'] if os.path.exists(os.path.join(HERE, 'src', t['slug'] + '.js'))]
COURSE = {'algebra': 'Algebra 1', 'algebra2': 'Algebra 2', 'geometry': 'Geometry'}
TPL = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · Mr. K's Classroom</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@500;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap">
<link rel="stylesheet" href="../interactive-math/lab.css?v={ver}">
</head><body><main id="app"></main><noscript><p style="padding:20px">This tool needs JavaScript.</p></noscript>
<script src="../interactive-math/lab.js?v={ver}"></script>
{extra}<script>
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
for t in M['tools']:
    src = open(os.path.join(HERE, 'src', t['slug'] + '.js'), encoding='utf-8').read()
    meta = json.dumps({'course': COURSE[t['course']], 'unit': t['unitName'], 'title': t['title'], 'intro': t['intro']}, ensure_ascii=False)
    out = os.path.join(ROOT, 'artifacts', t['slug'])
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(TPL.format(title=html.escape(t['title']), meta=meta, src=src, ver=VER, extra=''.join('<script src="../interactive-math/%s?v=%s"></script>\n' % (x, t.get('ver', VER)) for x in t.get('extra', []))))
print('built', len(M['tools']), 'tools')
