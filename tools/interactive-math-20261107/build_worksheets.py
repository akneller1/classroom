"""Writes the Explore & Reflect worksheet and teacher key HTML for the 2026-11-07 Interactive Math tools,
then print_pdfs.cjs turns them into artifacts/<slug>/worksheet.pdf and teacher-key.pdf.

Same look as tools/interactive-math-20261105/build_worksheets.py, with the five-part sequence
Predict → Explore → Record → Explain → Apply, and a teacher-notes box in the key (intended discovery,
likely misconceptions, where answers can vary).

Fonts: fonts/*.ttf are the site's Atkinson Hyperlegible (regular) and Bricolage Grotesque (bold) glyphs recovered
from the existing Interactive Math PDFs (the build machine had no network). Characters they lack (for example ≈, ×, √, π)
fall back to Inter / DejaVu Sans.
Usage (repository root): python3 tools/interactive-math-20261107/build_worksheets.py"""
import base64, html, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from worksheets_content import W
M = json.load(open(os.path.join(HERE, 'manifest.json'), encoding='utf-8'))
COURSE = {'math6': '6th Grade Math', 'prealgebra7': 'Pre-Algebra (7th)', 'prealgebra': 'Pre-Algebra (8th)', 'precalculus': 'Precalculus', 'calculus': 'Calculus'}
OUT = os.path.join(HERE, 'worksheet-html')
os.makedirs(OUT, exist_ok=True)

def font(name, fam, weight):
    p = os.path.join(HERE, 'fonts', name)
    b = base64.b64encode(open(p, 'rb').read()).decode()
    return '@font-face{font-family:"%s";src:url(data:font/ttf;base64,%s) format("truetype");font-weight:%s;font-style:normal}' % (fam, b, weight)
FONTS = font('AtkinsonHyperlegible-Regular.ttf', 'Atkinson Hyperlegible', 400) + font('BricolageGrotesque96ptExtraBold-Bold.ttf', 'Bricolage Grotesque', '700 800')

def fmt(t):
    t = html.escape(t, quote=False)
    for _ in range(2):
        t = re.sub(r'\{([^{}]*?)/([^{}]*)\}', r'<span class="fr"><span class="fn">\1</span><span class="fd">\2</span></span>', t)
    t = re.sub(r'\^\{([^{}]*)\}', r'<sup>\1</sup>', t)
    t = re.sub(r'_\{([^{}]*)\}', r'<sub>\1</sub>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return t

BODY = '"Atkinson Hyperlegible", Inter, "DejaVu Sans", Arial, sans-serif'
DISP = '"Bricolage Grotesque", Inter, "DejaVu Sans", Arial, sans-serif'
CSS = '''
@page { size: letter; margin: 0.5in 0.6in 0.55in; }
* { box-sizing: border-box; }
body { margin: 0; font-family: %(B)s; color: #14173a; font-size: 11pt; line-height: 1.38; }
.top { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid #14173a; padding-bottom: 6px; margin-bottom: 9px; }
.eyebrow { font-family: %(D)s; font-weight: 700; font-size: 8.5pt; letter-spacing: .12em; text-transform: uppercase; color: #3547f5; }
h1 { font-family: %(D)s; font-weight: 800; font-size: 20pt; margin: 2px 0 0; line-height: 1.05; }
.kind { font-family: %(D)s; font-weight: 700; font-size: 11pt; color: #4a4f78; white-space: nowrap; }
.key-flag { display: inline-block; background: #e0334f; color: #fff; padding: 2px 10px; border-radius: 999px; font-size: 9pt; margin-left: 6px; letter-spacing: .06em; }
.name { display: flex; gap: 14px; font-size: 10pt; margin-bottom: 8px; }
.name span { flex: 1; border-bottom: 1.5px solid #14173a; padding-bottom: 2px; }
.name span:first-child { flex: 2.2; }
.dir { background: #e6e9f8; border-radius: 8px; padding: 6px 11px; font-size: 9.8pt; margin-bottom: 9px; }
section { margin-bottom: 10px; }
h2 { font-family: %(D)s; font-weight: 800; font-size: 13pt; margin: 0 0 4px; display: flex; gap: 8px; align-items: baseline; break-after: avoid; }
h2 .n { display: inline-grid; place-items: center; width: 22px; height: 22px; border-radius: 50%%; background: #3547f5; color: #fff; font-size: 10.5pt; flex: none; transform: translateY(-1px); }
h2 small { font-family: %(B)s; font-weight: 400; font-size: 9.5pt; color: #4a4f78; }
h3 { font-size: 10.5pt; margin: 6px 0 3px; break-after: avoid; }
.note { font-size: 9.5pt; color: #4a4f78; margin: 0 0 4px; }
ol { margin: 0; padding-left: 22px; }
ol li { margin-bottom: 5px; break-inside: avoid; }
.lines { margin-top: 1px; }
.lines div { border-bottom: 1px solid #9aa0c8; height: 21px; }
.ans { color: #c8102e; font-weight: 700; }
.lines .ans { display: block; border-bottom: 1px solid #9aa0c8; min-height: 21px; padding-top: 1px; font-size: 10.2pt; }
table { border-collapse: collapse; width: 100%%; font-size: 10pt; break-inside: avoid; margin-bottom: 4px; }
th, td { border: 1.5px solid #14173a; padding: 4px 6px; text-align: center; vertical-align: middle; }
th { background: #e2e6ff; font-family: %(D)s; font-weight: 700; }
td.blank { height: 27px; min-width: 56px; }
.rule { margin-bottom: 6px; break-inside: avoid; line-height: 1.95; }
.b { display: inline-block; min-width: 110px; border-bottom: 1.5px solid #14173a; text-align: center; line-height: 1.3; padding: 0 4px; }
.work { height: 58px; }
.apply .ans, .explore .ans { display: block; margin-top: 1px; }
.fr { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle; font-size: .88em; margin: 0 .1em; line-height: 1.12; }
.fr .fn { padding: 0 .2em .05em; border-bottom: .08em solid currentColor; }
.fr .fd { padding: .05em .2em 0; }
sup, sub { font-size: .7em; line-height: 0; }
.tn { border: 2px solid #c8102e; border-radius: 10px; padding: 8px 12px; margin: 10px 0 0; break-inside: avoid; font-size: 9.8pt; }
.tn h4 { margin: 0 0 3px; font-family: %(D)s; font-size: 10.5pt; color: #c8102e; }
.tn p { margin: 0 0 5px; } .tn ul { margin: 0 0 5px; padding-left: 18px; } .tn li { margin-bottom: 2px; }
.foot { margin-top: 8px; font-size: 8.5pt; color: #4a4f78; text-align: right; }
.pb { break-before: page; }
''' % {'B': BODY, 'D': DISP}

SPACING = json.load(open(os.path.join(HERE, 'spacing.json'))) if os.path.exists(os.path.join(HERE, 'spacing.json')) else {}

def page(t, key, level=None):
    w = W[t['slug']]
    lv = SPACING.get(t['slug'], 0) if level is None else level   # more writing space at higher levels (chosen by fit_spacing.cjs)
    ex = lambda base, kind: base + {'predict': lv >= 3, 'explore': lv >= 1, 'explain': 1 + (lv >= 2)}[kind]
    a = lambda s: '<span class="ans">' + fmt(s) + '</span>'
    lines = lambda n: '<div class="lines">' + '<div></div>' * n + '</div>'
    P = []
    P.append('<div class="top"><div><div class="eyebrow">' + html.escape(COURSE[t['course']] + ' · ' + t['unitName']) + '</div><h1>' + html.escape(t['title']) + '</h1></div>'
             '<div class="kind">Explore &amp; Reflect' + ('<span class="key-flag">TEACHER KEY</span>' if key else '') + '</div></div>')
    P.append('<div class="name"><span>Name</span><span>Date</span><span>Period</span></div>')
    P.append('<div class="dir">Open <b>' + html.escape(t['title']) + '</b> in your unit’s Interactive Math section on Mr. K’s Classroom (or use your teacher’s link). '
             'Answer Part 1 <b>before</b> you use the tool. Use the tool for Parts 2 and 3. Do Parts 4 and 5 on your own.</div>')
    s = '<section><h2><span class="n">1</span>Predict <small>before you touch the tool</small></h2><ol>'
    for q, ans, n in w['predict']:
        s += '<li>' + fmt(q) + ('<div class="lines">' + a(ans) + '</div>' if key else lines(ex(n, 'predict'))) + '</li>'
    P.append(s + '</ol></section>')
    s = '<section class="explore"><h2><span class="n">2</span>Explore <small>use the tool</small></h2><ol>'
    for q, ans, n in w['explore']:
        s += '<li>' + fmt(q) + ('<div class="lines">' + a(ans) + '</div>' if key else lines(ex(n, 'explore'))) + '</li>'
    P.append(s + '</ol></section>')
    s = '<section><h2><span class="n">3</span>Record <small>use the tool and fill in the table</small></h2>'
    for tb in w['record']:
        if tb.get('title'): s += '<h3>' + fmt(tb['title']) + '</h3>'
        if tb.get('note'): s += '<p class="note">' + fmt(tb['note']) + '</p>'
        s += '<table><thead><tr>' + ''.join('<th>' + fmt(h) + '</th>' for h in tb['head']) + '</tr></thead><tbody>'
        for r in tb['rows']:
            s += '<tr>' + ''.join(('<td class="blank">' + (a(c[1:]) if key else '') + '</td>') if c.startswith('?') else '<td>' + fmt(c) + '</td>' for c in r) + '</tr>'
        s += '</tbody></table>'
    P.append(s + '</section>')
    s = '<section class="' + ('pb' if w.get('break_before') == 'explain' else '') + '"><h2><span class="n">4</span>Explain <small>what did you discover?</small></h2><ol>'
    for frame, answers in w['rules']:
        bits = frame.split('___'); out = fmt(bits[0])
        for i, rest in enumerate(bits[1:]):
            out += '<span class="b">' + (a(answers[i]) if key else '&nbsp;') + '</span>' + fmt(rest)
        s += '<li class="rule">' + out + '</li>'
    q, ans, n = w['explain']
    s += '<li>' + fmt(q) + ('<div class="lines">' + a(ans) + '</div>' if key else lines(ex(n, 'explain'))) + '</li>'
    P.append(s + '</ol></section>')
    s = '<section class="apply' + (' pb' if w.get('break_before') == 'apply' else '') + '"><h2><span class="n">5</span>Apply <small>a new situation, no tool</small></h2><ol>'
    for q, ans in w['apply']:
        s += '<li>' + fmt(q) + (a(ans) if key else '<div class="work" style="height:' + str(58 + 22 * lv) + 'px"></div>') + '</li>'
    P.append(s + '</ol></section>')
    if key:
        tn = w['teacher']
        P.append('<div class="tn"><h4>Teacher notes</h4><p><b>Intended discovery:</b> ' + fmt(tn['discovery']) + '</p>'
                 '<p><b>Likely misconceptions:</b></p><ul>' + ''.join('<li>' + fmt(m) + '</li>' for m in tn['misconceptions']) + '</ul>'
                 '<p><b>Answers that can vary:</b> ' + fmt(tn['varies']) + '</p></div>')
    P.append('<div class="foot">Mr. K’s Classroom · ' + html.escape(t['title']) + (' · Teacher key' if key else '') + '</div>')
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>' + html.escape(t['title']) + '</title><style>' + FONTS + CSS + '</style></head><body>' + ''.join(P) + '</body></html>'

missing = [t['slug'] for t in M['tools'] if t['slug'] not in W]
if missing: sys.exit('No worksheet for: ' + ', '.join(missing))
only = sys.argv[1] if len(sys.argv) > 1 else None
level = int(sys.argv[2]) if len(sys.argv) > 2 else None
n = 0
for t in M['tools']:
    if only and t['slug'] != only and not t['slug'].startswith(only + '*'.strip('*')) : continue
    for key in (False, True):
        open(os.path.join(OUT, t['slug'] + ('-key' if key else '') + '.html'), 'w', encoding='utf-8').write(page(t, key, level)); n += 1
print('wrote', n, 'worksheet pages to', OUT)
