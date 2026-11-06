"""Writes the Explore & Reflect worksheet and teacher key HTML for every Interactive Math tool.
Then run print_pdfs.cjs to turn them into artifacts/<slug>/worksheet.pdf and teacher-key.pdf.
Usage (repository root): python3 tools/interactive-math-20261105/build_worksheets.py <fonts-css-file>"""
import html, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from worksheets import W
from worksheets_geometry import W as WG
W.update(WG)
M = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
COURSE = {'algebra': 'Algebra 1', 'algebra2': 'Algebra 2', 'geometry': 'Geometry'}
FONTS = open(sys.argv[1], encoding='utf-8').read() if len(sys.argv) > 1 else ''
OUT = os.path.join(HERE, 'worksheet-html')
os.makedirs(OUT, exist_ok=True)

def fmt(t):
    t = html.escape(t, quote=False)
    for _ in range(2):
        t = re.sub(r'\{([^{}]*?)/([^{}]*)\}', r'<span class="fr"><span class="fn">\1</span><span class="fd">\2</span></span>', t)
    t = re.sub(r'\^\{([^{}]*)\}', r'<sup>\1</sup>', t)
    t = re.sub(r'_\{([^{}]*)\}', r'<sub>\1</sub>', t)
    return t

CSS = '''
@page { size: letter; margin: 0.55in 0.6in 0.6in; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Atkinson Hyperlegible", Arial, sans-serif; color: #14173a; font-size: 11.5pt; line-height: 1.4; }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid #14173a; padding-bottom: 6px; margin-bottom: 10px; }
.eyebrow { font-family: "Bricolage Grotesque", Arial, sans-serif; font-weight: 700; font-size: 8.5pt; letter-spacing: .12em; text-transform: uppercase; color: #3547f5; }
h1 { font-family: "Bricolage Grotesque", Arial, sans-serif; font-weight: 800; font-size: 21pt; margin: 2px 0 0; line-height: 1.05; }
.kind { font-family: "Bricolage Grotesque", Arial, sans-serif; font-weight: 700; font-size: 11pt; color: #4a4f78; }
.key-flag { display: inline-block; background: #e0334f; color: #fff; padding: 2px 10px; border-radius: 999px; font-size: 9pt; margin-left: 6px; letter-spacing: .06em; }
.name { display: flex; gap: 14px; font-size: 10pt; margin-bottom: 8px; }
.name span { flex: 1; border-bottom: 1.5px solid #14173a; padding-bottom: 2px; }
.name span:first-child { flex: 2.2; }
.dir { background: #e6e9f8; border-radius: 8px; padding: 7px 11px; font-size: 10pt; margin-bottom: 10px; }
section { margin-bottom: 12px; }
h2 { font-family: "Bricolage Grotesque", Arial, sans-serif; font-weight: 800; font-size: 13pt; margin: 0 0 5px; display: flex; gap: 8px; align-items: baseline; break-after: avoid; }
h2 .n { display: inline-grid; place-items: center; width: 22px; height: 22px; border-radius: 50%; background: #3547f5; color: #fff; font-size: 10.5pt; flex: none; transform: translateY(-1px); }
h2 small { font-family: "Atkinson Hyperlegible", Arial, sans-serif; font-weight: 400; font-size: 9.5pt; color: #4a4f78; }
h3 { font-size: 10.5pt; margin: 8px 0 3px; break-after: avoid; }
.note { font-size: 9.5pt; color: #4a4f78; margin: 0 0 4px; }
ol { margin: 0; padding-left: 20px; }
ol li { margin-bottom: 6px; break-inside: avoid; }
.lines { margin-top: 2px; }
.lines div { border-bottom: 1px solid #9aa0c8; height: 20px; }
.ans { color: #c8102e; font-weight: 700; }
.lines .ans { display: block; border-bottom: 1px solid #9aa0c8; min-height: 20px; padding-top: 1px; font-size: 10.5pt; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; break-inside: avoid; margin-bottom: 4px; }
th, td { border: 1.5px solid #14173a; padding: 4px 6px; text-align: center; vertical-align: middle; }
th { background: #e2e6ff; font-family: "Bricolage Grotesque", Arial, sans-serif; font-weight: 700; }
td.blank { height: 26px; min-width: 60px; }
.rule { margin-bottom: 7px; break-inside: avoid; line-height: 1.9; }
.b { display: inline-block; min-width: 110px; border-bottom: 1.5px solid #14173a; text-align: center; line-height: 1.3; padding: 0 4px; }
.check li { margin-bottom: 4px; }
.work { height: 62px; }
.check .ans { display: block; margin-top: 2px; }
.fr { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; font-size: .88em; margin: 0 .1em; line-height: 1.12; }
.fr .fn { padding: 0 .2em .05em; border-bottom: .08em solid currentColor; }
.fr .fd { padding: .05em .2em 0; }
sup, sub { font-size: .7em; line-height: 0; }
.foot { margin-top: 10px; font-size: 8.5pt; color: #4a4f78; text-align: right; }
'''

def page(t, key):
    w = W[t['slug']]
    a = lambda s: '<span class="ans">' + fmt(s) + '</span>'
    parts = []
    parts.append('<div class="top"><div><div class="eyebrow">' + html.escape(COURSE[t['course']] + ' · ' + t['unitName']) + '</div><h1>' + html.escape(t['title']) + '</h1></div>'
                 '<div class="kind">Explore &amp; Reflect' + ('<span class="key-flag">TEACHER KEY</span>' if key else '') + '</div></div>')
    parts.append('<div class="name"><span>Name</span><span>Date</span><span>Period</span></div>')
    parts.append('<div class="dir">Open <b>' + html.escape(t['title']) + '</b> on Mr. K\'s Classroom: ' + html.escape(COURSE[t['course']]) + ' → ' + html.escape(t['unitName']) +
                 ' → Interactive Math. Answer Part 1 <b>before</b> you use the tool. Use the tool for Parts 2 and 3, then do Part 4 on your own.</div>')
    # 1 predict
    s = '<section><h2><span class="n">1</span>Predict <small>before you touch the tool</small></h2><ol>'
    for q, ans in w['predict']:
        s += '<li>' + fmt(q) + '<div class="lines">' + (a(ans) if key else '<div></div><div></div>') + '</div></li>'
    parts.append(s + '</ol></section>')
    # 2 explore
    s = '<section><h2><span class="n">2</span>Explore <small>use the tool and record what you see</small></h2>'
    for tb in w['explore']:
        s += '<h3>' + fmt(tb['title']) + '</h3>' + ('<p class="note">' + fmt(tb['note']) + '</p>' if tb.get('note') else '')
        s += '<table><thead><tr>' + ''.join('<th>' + fmt(h) + '</th>' for h in tb['head']) + '</tr></thead><tbody>'
        for r in tb['rows']:
            s += '<tr>' + ''.join(('<td class="blank">' + (a(c[1:]) if key else '') + '</td>') if c.startswith('?') else '<td>' + fmt(c) + '</td>' for c in r) + '</tr>'
        s += '</tbody></table>'
    parts.append(s + '</section>')
    # 3 rules
    s = '<section><h2><span class="n">3</span>Write the rule <small>fill in each blank from what you observed</small></h2><ol>'
    for frame, answers in w['rules']:
        bits = frame.split('___'); out = fmt(bits[0])
        for i, rest in enumerate(bits[1:]):
            out += '<span class="b">' + (a(answers[i]) if key else '&nbsp;') + '</span>' + fmt(rest)
        s += '<li class="rule">' + out + '</li>'
    parts.append(s + '</ol></section>')
    # 4 check
    s = '<section class="check"><h2><span class="n">4</span>Check <small>no tool: show your work</small></h2><ol>'
    for q, ans in w['check']:
        s += '<li>' + fmt(q) + (a(ans) if key else '<div class="work"></div>') + '</li>'
    parts.append(s + '</ol></section>')
    # 5 reflect
    q, ans = w['reflect']
    parts.append('<section><h2><span class="n">5</span>Reflect</h2><p style="margin:0 0 2px">' + fmt(q) + '</p><div class="lines">' + (a(ans) if key else '<div></div><div></div><div></div>') + '</div></section>')
    parts.append('<div class="foot">Mr. K\'s Classroom · ' + html.escape(t['title']) + (' · Teacher key' if key else '') + '</div>')
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>' + html.escape(t['title']) + '</title><style>' + FONTS + CSS + '</style></head><body>' + ''.join(parts) + '</body></html>'

missing = [t['slug'] for t in M['tools'] if t['slug'] not in W]
if missing: sys.exit('No worksheet for: ' + ', '.join(missing))
for t in M['tools']:
    for key in (False, True):
        open(os.path.join(OUT, t['slug'] + ('-key' if key else '') + '.html'), 'w', encoding='utf-8').write(page(t, key))
print('wrote', 2 * len(M['tools']), 'worksheet pages to', OUT)
