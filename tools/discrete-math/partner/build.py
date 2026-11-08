#!/usr/bin/env python3
"""Build the Discrete Math partner checks.
  artifacts/discrete-<unit>-partner-check-<1|2>/worksheet.pdf  (6 pages: CP2 A, CP2 B, CP1 A, CP1 B, Honors A, Honors B)
  artifacts/discrete-partner-checks/teacher-key.pdf               (open teacher key, matching the current site)
  thumbs/discrete-<unit>-partner-check-<n>.jpg                     (720 × 450, rendered from page 1)
  tools/discrete-math/partner/pairs.json                           (every pair with its verified answer)
Every pair is re-solved from its printed text by pairs.verify() before anything is written."""
import os, sys, json, html, subprocess, io
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from pairs import UNITS, make_pairs, verify

NAMES = {'speaking-mathematically': 'Speaking Mathematically', 'compound-statements-logic': 'The Logic of Compound Statements', 'number-theory-proof': 'Elementary Number Theory and Methods of Proof',
         'sequences-induction-recursion': 'Sequences, Mathematical Induction, and Recursion', 'set-theory': 'Set Theory', 'properties-relations': 'Properties of Relations',
         'counting-probability': 'Counting and Probability', 'graphs-trees': 'Theory of Graphs and Trees', 'election-theory': 'Election Theory', 'linear-programming': 'Linear Programming'}
LEVEL_NAME = {'cp2': 'CP2', 'cp1': 'CP1', 'honors': 'Honors'}
CONV = ('Answer conventions: sets in roster form with elements in increasing order, ∅ for the empty set; truth columns as T/F strings in standard row order '
        '(TT, TF, FT, FF; with r: TTT, TTF, ..., FFF); fractions in lowest terms; ordered pairs as (x, y).')
CSS = """
@page{size:Letter;margin:0.5in 0.55in}
*{box-sizing:border-box}
body{font-family:'DejaVu Sans',Arial,sans-serif;color:#1d2433;margin:0;font-size:11.5pt}
.page{page-break-after:always;position:relative;height:9.9in}
.page:last-child{page-break-after:auto}
.eyebrow{font-size:8.5pt;letter-spacing:.08em;color:#55607a;text-transform:uppercase}
h1{font-size:17pt;color:#1f4e9a;margin:2px 0 8px;font-weight:700;max-width:6.3in}
.badge{position:absolute;right:0;top:0;width:52px;height:52px;border-radius:50%;background:#1f4e9a;color:#fff;font-size:24pt;font-weight:700;display:flex;align-items:center;justify-content:center}
.names{display:flex;gap:18px;font-size:10pt;margin:6px 0 10px}.names span{flex:1;border-bottom:1px solid #777;padding-bottom:2px}
.dir{border:1px solid #c9d3e6;background:#f5f8fd;border-radius:6px;padding:7px 10px;font-size:9.5pt;margin-bottom:10px}
.dir em{color:#55607a}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.box{border:1.2px solid #8aa0c8;border-radius:7px;min-height:2.38in;position:relative;padding:8px 10px 36px 10px}
.num{position:absolute;top:-1px;left:-1px;background:#1f4e9a;color:#fff;font-size:9pt;font-weight:700;padding:1px 6px;border-radius:6px 0 6px 0}
.q{margin-top:12px;line-height:1.35}
.ans{position:absolute;left:10px;right:10px;bottom:8px;display:flex;justify-content:space-between;font-size:9pt}
.ans b{font-weight:700}.ans .line{display:inline-block;width:1.5in;border-bottom:1px solid #444}
.foot{position:absolute;bottom:0;left:0;right:0;display:flex;justify-content:space-between;font-size:8pt;color:#6a7286}
table.key{width:100%;border-collapse:collapse;font-size:8.6pt;margin-bottom:10px;table-layout:fixed}
table.key col.n{width:4%}table.key col.p{width:39%}table.key col.a{width:18%}
table.key td{word-wrap:break-word}
table.key th,table.key td{border:1px solid #b9c3d6;padding:3px 5px;vertical-align:top}
table.key th{background:#eef3fa;text-align:left}
h2{font-size:11.5pt;color:#1f4e9a;margin:8px 0 4px}
.keyhead{font-size:9pt;color:#55607a;margin-bottom:6px}
"""


def page(unit_no, unit, set_no, level, side, pairs):
    title = '%s · Partner Check %d' % (NAMES[unit], set_no)
    boxes = ''.join('<div class="box"><span class="num">%d</span><div class="q">%s</div><div class="ans"><span><b>Answer:</b> <span class="line"></span></span><span>Match? ☐ Yes ☐ No</span></div></div>'
                    % (i + 1, html.escape(p[side])) for i, p in enumerate(pairs))
    return ('<div class="page"><div class="badge">%s</div><div class="eyebrow">Discrete Math ■ Unit %d ■ %s ■ Level %s</div><h1>%s</h1>'
            '<div class="names"><span>Name:</span><span>Partner\'s name:</span><span>Date:</span></div>'
            '<div class="dir"><b>Directions:</b> Work alone on your own problems. Partner %s has different problems with the same answers. After each problem, compare answers; if they differ, find the mistake together.<br><em>%s</em></div>'
            '<div class="grid">%s</div><div class="foot"><span>Discrete Math Partner Check ■ Unit %d ■ Set %d ■ %s</span><span>Partner %s</span></div></div>') % (
        side, unit_no, html.escape(NAMES[unit].upper()), LEVEL_NAME[level], html.escape(title), 'B' if side == 'A' else 'A', html.escape(CONV), boxes, unit_no, set_no, LEVEL_NAME[level], side)


def render(html_text, out_pdf):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.set_content('<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (CSS, html_text), wait_until='load')
        pg.pdf(path=out_pdf, format='Letter', print_background=True, prefer_css_page_size=True)
        b.close()


def thumb(pdf, out_jpg):
    from PIL import Image
    tmp = out_jpg + '.png'
    subprocess.run(['pdftoppm', '-r', '80', '-png', '-f', '1', '-l', '1', '-singlefile', pdf, tmp[:-4]], check=True)
    img = Image.open(tmp).convert('RGB')
    img.thumbnail((680, 420))
    canvas = Image.new('RGB', (720, 450), '#f3f6fb')
    canvas.paste(img, ((720 - img.width) // 2, (450 - img.height) // 2))
    canvas.save(out_jpg, quality=82, optimize=True)
    os.remove(tmp)


def main():
    allpairs = {}
    key_html = ['<div class="page"><div class="eyebrow">Discrete Math ■ Teacher key</div><h1>Partner Checks: Teacher Answer Key</h1>'
                '<div class="keyhead">Each row lists Partner A\'s problem, Partner B\'s problem and the shared answer. Every pair was solved independently from its printed text by the build script (tools/discrete-math/partner). %s</div>' % html.escape(CONV)]
    rows_on_page = 0
    for ui, unit in enumerate(UNITS, 1):
        for s in (1, 2):
            pages = []
            for L in ('cp2', 'cp1', 'honors'):
                P = verify(make_pairs(unit, L, s), unit, L)
                assert all(p.get('checked') == 2 for p in P), (unit, s, L)
                allpairs['%s|%d|%s' % (unit, s, L)] = P
                pages.append(page(ui, unit, s, L, 'A', P))
                pages.append(page(ui, unit, s, L, 'B', P))
                tbl = '<h2>Unit %d · %s · Partner Check %d · %s</h2><table class="key"><colgroup><col class="n"><col class="p"><col class="p"><col class="a"></colgroup><tr><th>#</th><th>Partner A</th><th>Partner B</th><th>Answer</th></tr>%s</table>' % (
                    ui, html.escape(NAMES[unit]), s, LEVEL_NAME[L], ''.join('<tr><td>%d</td><td>%s</td><td>%s</td><td><b>%s</b></td></tr>' % (i + 1, html.escape(p['A']), html.escape(p['B']), html.escape(p['answer'])) for i, p in enumerate(P)))
                if rows_on_page >= 2:
                    key_html.append('</div><div class="page">')
                    rows_on_page = 0
                key_html.append(tbl)
                rows_on_page += 1
            folder = os.path.join(ROOT, 'artifacts/discrete-%s-partner-check-%d' % (unit, s))
            os.makedirs(folder, exist_ok=True)
            pdf = os.path.join(folder, 'worksheet.pdf')
            render(''.join(pages), pdf)
            thumb(pdf, os.path.join(ROOT, 'thumbs/discrete-%s-partner-check-%d.jpg' % (unit, s)))
            print('built', pdf)
    key_html.append('</div>')
    kdir = os.path.join(ROOT, 'artifacts/discrete-partner-checks')
    os.makedirs(kdir, exist_ok=True)
    plain = os.path.join(HERE, 'teacher-key-unencrypted.pdf')
    render(''.join(key_html), plain)
    __import__('shutil').copyfile(plain, os.path.join(kdir, 'teacher-key.pdf'))
    os.remove(plain)
    json.dump(allpairs, open(os.path.join(HERE, 'pairs.json'), 'w'), ensure_ascii=False, indent=1)
    print('pairs', sum(len(v) for v in allpairs.values()))


if __name__ == '__main__':
    main()
