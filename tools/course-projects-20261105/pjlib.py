"""Project builder: same format as the Algebra 1 / Geometry / Algebra 2 projects in artifacts/<course>-project-<slug>/.
Each project -> <slug>-{cp2,cp1,honors}.{docx,pdf,pptx}, <slug>-teacher-guide.{docx,pdf}, hero.png, index.html, thumbs/<folder>.jpg.
Fractions in text are written {num|den}: stacked (Office Math) in Word/PDF, num⁄den in PowerPoint and HTML."""
import copy, html, json, os, re, subprocess, shutil, tempfile
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor, Emu
from pptx import Presentation
from pptx.dml.color import RGBColor as PRGB
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches as PI, Pt as PPt

SITE = os.environ.get('SITE', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))
NAVY, BLUE, LIGHT = '1F3A5F', '2B6CB0', 'E8EEF5'
LEVELS = [('cp2', 'CP2', 'Guided', '2E7D4F'), ('cp1', 'CP1', 'Standard', '2B6CB0'), ('honors', 'Honors', 'Extension', '6B3FA0')]
LEVEL_BLURB = {'cp2': 'Guided version: step-by-step prompts, starter tables, sentence starters, and friendly numbers.',
               'cp1': 'Standard version: students set up and solve problems with less scaffolding.',
               'honors': 'Extension version: generalize, justify, and design with open-ended constraints.'}
COURSE_NAME = {'math6': '6th Grade Math', 'prealgebra7': 'Pre-Algebra (7th)', 'precalculus': 'Precalculus', 'calculus': 'Calculus'}
PROJECTS = []
FRAC = re.compile(r'\{([^{}|]+)\|([^{}|]+)\}')
SUP = str.maketrans('0123456789+-()x', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁽⁾ˣ')
SUB = str.maketrans('0123456789+-()x', '₀₁₂₃₄₅₆₇₈₉₊₋₍₎ₓ')


def flat(t):
    """{a|b} -> a⁄b for PowerPoint / HTML / plain text."""
    def f(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        if re.fullmatch(r'[0-9]+', a) and re.fullmatch(r'[0-9]+', b): return a.translate(SUP) + '⁄' + b.translate(SUB)
        wrap = lambda s: s if re.fullmatch(r'[\w.√π°′²³]+', s) else '(' + s + ')'
        return wrap(a) + '⁄' + wrap(b)
    return FRAC.sub(f, t)


def Q(text, answer, starter=None, fig=None, lines=None):
    return dict(text=text, answer=answer, starter=starter, fig=fig, lines=lines)


def project(**p):
    req = ['course', 'unit', 'unit_no', 'unit_name', 'slug', 'title', 'tagline', 'description', 'theme', 'product', 'accent', 'scenario', 'hero',
           'levels', 'overview', 'standards', 'pacing', 'materials', 'differ', 'watch', 'extensions', 'rubric_app', 'rubric_comm']
    for k in req: assert k in p, (p.get('slug'), k)
    for lv in ('cp2', 'cp1', 'honors'):
        L = p['levels'][lv]
        assert len(L['goals']) == 3 and len(L['parts']) == 3 and len(L['reflect']) == 2, (p['slug'], lv)
        for part in L['parts']: assert 2 <= len(part[2]) <= 4, (p['slug'], lv, part[0])
    p['folder'] = p['course'] + '-project-' + p['slug']
    PROJECTS.append(p)
    return p


# ---------------------------------------------------------------- images (rendered with Chromium)
HERO_CSS = """*{box-sizing:border-box;margin:0}body{width:1280px;height:800px;background:#fff;font-family:'DejaVu Sans',sans-serif;position:relative;overflow:hidden}
.scene{position:absolute;left:44px;top:150px;width:760px;height:570px;border:5px solid #1F3A5F;border-top:none;overflow:hidden}
.bar{position:absolute;left:40px;top:110px;width:770px;height:48px;background:#1F3A5F;color:#fff;font:700 27px 'DejaVu Sans';display:flex;align-items:center;justify-content:center;letter-spacing:.5px}
.ground{position:absolute;left:0;right:0;bottom:0;height:80px}
.e{position:absolute;line-height:1;font-family:'Noto Color Emoji'}
.cards{position:absolute;left:850px;top:40px;width:400px;display:flex;flex-direction:column;gap:22px}
.card{border:6px solid;border-radius:8px;overflow:hidden;background:#fff}
.card h3{color:#fff;font:700 31px 'DejaVu Sans';text-align:center;padding:16px 8px}
.card p{font:400 27px 'DejaVu Sans';color:#222;text-align:center;padding:14px 10px;line-height:1.25}"""
CARD_CSS = """*{box-sizing:border-box;margin:0}body{background:#fff;font-family:'DejaVu Sans',sans-serif}
.g{display:grid;grid-template-columns:repeat(var(--n),1fr);gap:16px 20px}
.c{border:4px solid;border-radius:6px;overflow:hidden}.c h3{color:#fff;font:700 24px 'DejaVu Sans';text-align:center;padding:10px 6px}
.c p{font:400 21px 'DejaVu Sans';color:#222;text-align:center;padding:9px 6px;border-top:1px solid #ddd}.c p:first-of-type{border-top:none}
.t{font:700 26px 'DejaVu Sans';color:#1F3A5F;text-align:center;margin-bottom:12px}"""


def hero_html(h):
    """h = dict(label, sky, ground, items=[(emoji, x, y, size)], cards=[(title, color, [lines])])"""
    items = ''.join('<div class="e" style="left:%dpx;top:%dpx;font-size:%dpx">%s</div>' % (x, y, s, e) for e, x, y, s in h['items'])
    cards = ''.join('<div class="card" style="border-color:#%s"><h3 style="background:#%s">%s</h3>%s</div>' % (
        c, c, html.escape(t), ''.join('<p>%s</p>' % html.escape(flat(l)) for l in lines)) for t, c, lines in h['cards'])
    return ('<html><head><meta charset="utf-8"><style>%s</style></head><body><div class="bar">%s</div>'
            '<div class="scene" style="background:%s"><div class="ground" style="background:%s"></div>%s</div><div class="cards">%s</div></body></html>') % (
        HERO_CSS, html.escape(h['label']), h['sky'], h['ground'], items, cards)


def cards_html(c):
    """c = dict(title, cols, items=[(name, color, [lines])])"""
    items = ''.join('<div class="c" style="border-color:#%s"><h3 style="background:#%s">%s</h3>%s</div>' % (
        col, col, html.escape(n), ''.join('<p>%s</p>' % html.escape(flat(l)) for l in lines)) for n, col, lines in c['items'])
    return '<html><head><meta charset="utf-8"><style>%s</style></head><body><div id="w" style="display:inline-block;padding:14px;width:1100px">%s<div class="g" style="--n:%d">%s</div></div></body></html>' % (
        CARD_CSS, ('<div class="t">%s</div>' % html.escape(c['title'])) if c.get('title') else '', c.get('cols', 3), items)


THUMB_CSS = """*{margin:0;box-sizing:border-box}body{width:720px;height:450px;background:#%s;position:relative;font-family:'DejaVu Sans',sans-serif;overflow:hidden}
.k{position:absolute;left:27px;top:31px;color:#fff;font:700 14.5px 'DejaVu Sans';letter-spacing:.3px}
h1{position:absolute;left:27px;top:140px;width:300px;color:#fff;font:700 33px 'DejaVu Sans';line-height:1.12}
.box{position:absolute;left:360px;top:67px;width:343px;height:312px;background:#fff;border-radius:12px;display:flex;align-items:center;justify-content:center}
.box img{width:326px}.foot{position:absolute;left:0;right:0;bottom:0;height:49px;background:#1F3A5F;color:#fff;font:400 15px 'DejaVu Sans';padding:15px 27px}"""


def render_images(jobs):
    """jobs: list of (html, out_png, selector or None, viewport (w,h)). Rendered in one browser."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for doc, out, sel, vp in jobs:
            pg = b.new_page(viewport={'width': vp[0], 'height': vp[1]})
            tmp = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8'); tmp.write(doc); tmp.close()
            pg.goto('file://' + tmp.name); pg.wait_for_timeout(150)
            if sel: pg.locator(sel).screenshot(path=out)
            else: pg.screenshot(path=out, type='jpeg' if out.endswith('.jpg') else 'png', **({'quality': 88} if out.endswith('.jpg') else {}))
            pg.close(); os.unlink(tmp.name)
        b.close()


def fig_png(fig, out):
    """Small matplotlib figures: ('numberline', lo, hi, step, label) | ('grid', xlo, xhi, ylo, yhi, label)."""
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    if fig[0] == 'numberline':
        _, lo, hi, step, label = fig
        f, ax = plt.subplots(figsize=(7.2, 1.25), dpi=150)
        ax.set_xlim(lo - step * 0.6, hi + step * 0.6); ax.set_ylim(-1, 1); ax.axis('off')
        ax.annotate('', xy=(hi + step * 0.6, 0), xytext=(lo - step * 0.6, 0), arrowprops=dict(arrowstyle='<->', lw=1.4, color='#222'))
        v = lo; n = 0
        while v <= hi + 1e-9:
            ax.plot([v, v], [-0.18, 0.18], color='#222', lw=1.2)
            ax.text(v, -0.55, ('%g' % round(v, 6)).replace('-', '−'), ha='center', va='center', fontsize=10)
            v += step; n += 1
        ax.text((lo + hi) / 2, 0.75, label, ha='center', fontsize=11, fontweight='bold', color='#1F3A5F')
    else:
        _, x0, x1, y0, y1, label = fig
        f, ax = plt.subplots(figsize=(4.2, 4.2 * (y1 - y0) / max(1, (x1 - x0)) if (y1 - y0) <= (x1 - x0) else 4.2), dpi=150)
        ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.grid(True, color='#cfd8e3', lw=0.7)
        ax.set_xticks(range(x0, x1 + 1)); ax.set_yticks(range(y0, y1 + 1))
        ax.tick_params(labelsize=7)
        ax.axhline(0, color='#222', lw=1.1); ax.axvline(0, color='#222', lw=1.1)
        ax.set_title(label, fontsize=10, fontweight='bold', color='#1F3A5F'); ax.set_aspect('equal')
    f.tight_layout(); f.savefig(out, facecolor='white'); plt.close(f)


# ---------------------------------------------------------------- Word helpers
M_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), fill); tcPr.append(sh)


def cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr(); m = OxmlElement('w:tcMar')
    for k, v in (('top', top), ('bottom', bottom), ('start', left), ('end', right)):
        e = OxmlElement('w:' + k); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa'); m.append(e)
    tcPr.append(m)


def borders(table, color='BFBFBF', size=4):
    tblPr = table._tbl.tblPr; b = OxmlElement('w:tblBorders')
    for k in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + k); e.set(qn('w:val'), 'single' if size else 'nil'); e.set(qn('w:sz'), str(size)); e.set(qn('w:color'), color); b.append(e)
    tblPr.append(b)


def runs(p, text, size=11, bold=False, italic=False, color=None):
    """Add text with {a|b} as stacked Office Math fractions."""
    pos = 0
    for m in FRAC.finditer(text):
        if m.start() > pos: _run(p, text[pos:m.start()], size, bold, italic, color)
        sz = str(int(size * 2))
        mr = lambda t: '<m:r><w:rPr><w:sz w:val="%s"/></w:rPr><m:t xml:space="preserve">%s</m:t></m:r>' % (sz, html.escape(t, quote=False))
        p._p.append(parse_xml('<m:oMath xmlns:m="%s" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><m:f><m:num>%s</m:num><m:den>%s</m:den></m:f></m:oMath>' % (
            M_NS, mr(m.group(1).strip()), mr(m.group(2).strip()))))
        pos = m.end()
    if pos < len(text): _run(p, text[pos:], size, bold, italic, color)
    return p


def _run(p, t, size, bold, italic, color):
    r = p.add_run(t); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = RGBColor.from_string(color)
    return r


def para(cell_or_doc, text='', size=11, bold=False, italic=False, color=None, align=None, after=4, before=0):
    p = cell_or_doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if align: p.alignment = align
    if text: runs(p, text, size, bold, italic, color)
    return p


def heading(doc, text, before=10, new_page=False):
    p = para(doc, text, 15, True, color=BLUE, after=6, before=before)
    if new_page: p.paragraph_format.page_break_before = True
    pPr = p._p.get_or_add_pPr(); bdr = OxmlElement('w:pBdr'); b = OxmlElement('w:bottom')
    for k, v in (('val', 'single'), ('sz', '8'), ('space', '1'), ('color', BLUE)): b.set(qn('w:' + k), v)
    bdr.append(b); pPr.append(bdr)
    return p


def bullet(doc, text, size=11):
    p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(2)
    runs(p, text, size); return p


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def answer_box(doc, height_in):
    t = doc.add_table(rows=1, cols=1); borders(t, 'A6A6A6', 6); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tr = t.rows[0]._tr; trPr = tr.get_or_add_trPr(); h = OxmlElement('w:trHeight'); h.set(qn('w:val'), str(int(height_in * 1440))); h.set(qn('w:hRule'), 'atLeast'); trPr.append(h)
    t.autofit = False; t.columns[0].width = Inches(6.9); t.rows[0].cells[0].width = Inches(6.9)
    para(doc, '', after=2)


def footer(doc, text):
    for s in doc.sections:
        p = s.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text); r.font.size = Pt(8); r.italic = True; r.font.color.rgb = RGBColor(0x80, 0x80, 0x80)


def new_doc():
    d = Document(); s = d.sections[0]
    s.page_width, s.page_height = Inches(8.5), Inches(11)
    s.top_margin = s.bottom_margin = Inches(0.6); s.left_margin = s.right_margin = Inches(0.8)
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
    return d


def banner(doc, p, right_title, right_fill, sub=None):
    t = doc.add_table(rows=1, cols=2); borders(t, 'FFFFFF', 0)
    t.autofit = False; t.columns[0].width, t.columns[1].width = Inches(4.7), Inches(2.2); a, b = t.rows[0].cells; a.width, b.width = Inches(4.7), Inches(2.2)
    shade(a, NAVY); shade(b, right_fill); cell_margins(a, 160, 160, 200, 160); cell_margins(b, 160, 160, 120, 120)
    a.paragraphs[0].text = ''
    runs(a.paragraphs[0], kicker(p).upper(), 9, True, color='BFD7F2')
    para(a, p['title'], 22, True, color='FFFFFF', after=2)
    para(a, sub or p['tagline'], 11, italic=True, color='E8EEF5', after=0)
    b.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    runs(b.paragraphs[0], right_title, 18, True, color='FFFFFF')
    para(b, '2–3 class periods', 9, color='FFFFFF', align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
    para(doc, '', after=2)


def kicker(p):
    return '%s · Unit %s: %s' % (COURSE_NAME[p['course']], p['unit_no'], p['unit_name'])


def short(p):
    return '%s · Unit %s' % (COURSE_NAME[p['course']], p['unit_no'])


def simple_table(doc, head, rows, widths, head_fill=BLUE, size=10, zebra=True, first_col_fill=None, spacer=True):
    t = doc.add_table(rows=1 + len(rows), cols=len(head)); borders(t, 'BFBFBF', 4); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.autofit = False
    for i, w in enumerate(widths): t.columns[i].width = Inches(w)
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]; shade(c, head_fill); c.width = Inches(widths[i]); c.paragraphs[0].text = ''
        runs(c.paragraphs[0], h, size, True, color='FFFFFF')
    for tr in t.rows:
        trPr = tr._tr.get_or_add_trPr(); cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true'); trPr.append(cs)
    hdr = OxmlElement('w:tblHeader'); hdr.set(qn('w:val'), 'true'); t.rows[0]._tr.get_or_add_trPr().append(hdr)
    for r, row in enumerate(rows):
        for i, v in enumerate(row):
            c = t.rows[r + 1].cells[i]; c.width = Inches(widths[i]); c.paragraphs[0].text = ''
            if first_col_fill and i == 0: shade(c, first_col_fill)
            elif zebra and r % 2 == 1: shade(c, 'F2F2F2')
            runs(c.paragraphs[0], v, size, bold=(first_col_fill is not None and i == 0))
    if spacer: para(doc, ' ', size=2, after=0)
    return t


RUBRIC_HEAD = ['Criteria', '4 – Exceeds', '3 – Meets', '2 – Approaching', '1 – Beginning']
RUBRIC_FIXED = [['Mathematical Accuracy', 'All calculations and solutions are correct; answers include units and are checked.', 'Nearly all work is correct; minor errors do not change conclusions.',
                 'Several errors; some conclusions are affected.', 'Many errors or missing work.'],
                ['Reasoning & Justification', 'Clear, complete explanations connect every answer to the situation; uses precise vocabulary.', 'Explanations are mostly clear and connected to the situation.',
                 'Explanations are brief or partly unclear.', 'Little or no explanation.']]


def rubric_rows(p):
    a, c = p['rubric_app'], p['rubric_comm']
    return RUBRIC_FIXED + [['Application & Design', a + ' Goes beyond the minimum with a creative, realistic choice.', a, 'Design is incomplete or only partly uses the math from the unit.', 'Design is missing or unrelated to the unit math.'],
                           ['Communication & Presentation', c + ' Polished, organized, and visually engaging.', c + ' Organized and easy to follow.', 'Product is missing required parts or is hard to follow.', 'Product is mostly missing.']]


def lines_in(t, width=100):
    import math
    n = math.ceil(max(1, len(flat(t))) / width)
    return n * 0.195 + (0.1 * min(n, t.count('{')) if '{' in t else 0)


def img_h(path, w):
    from PIL import Image
    a, b = Image.open(path).size
    return w * b / a


def student_docx(p, lv, out, imgs):
    L = p['levels'][lv]; lname = dict((a, b) for a, b, _, _ in LEVELS)[lv]; lcol = dict((a, d) for a, _, _, d in LEVELS)[lv]
    d = new_doc(); banner(d, p, lname, lcol)
    para(d, 'Name: ________________________________ Date: ______________ Period: ______', 10, after=6)
    heading(d, 'The Scenario', 4)
    for s in p['scenario']: para(d, s, 11, after=6)
    d.add_picture(imgs['hero'], width=Inches(4.2)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    heading(d, 'Learning Goals')
    for g in L['goals']: bullet(d, g)
    heading(d, 'Project Timeline')
    simple_table(d, ['When', 'What you will do'], [['Day %d' % (i + 1), pt[0]] for i, pt in enumerate(L['parts'])] + [['Final', p['product'] + ' + reflection']], [1.3, 5.6], spacer=False)
    n = 0
    box = {'cp2': 0.95, 'cp1': 1.05, 'honors': 1.1}[lv]
    for i, (title, intro, qs) in enumerate(L['parts']):
        heading(d, 'Part %d: %s' % (i + 1, title), 0, True)
        pp = para(d, '', after=6); runs(pp, 'Day %d · ' % (i + 1), 10.5, True, color=BLUE); runs(pp, intro, 10.5)
        if i == 0 and imgs.get('cards'): d.add_picture(imgs['cards'], width=Inches(5.6)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        fixed = 0.62 + lines_in(intro) + (img_h(imgs['cards'], 5.6) + 0.1 if (i == 0 and imgs.get('cards')) else 0)
        for k, q in enumerate(qs):
            fixed += lines_in(q['text']) + 0.18 + (0.27 if q.get('starter') else 0) + 0.16
            if q.get('fig'): fixed += img_h(imgs['fig%d' % (n + k + 1)], 5.4 if q['fig'][0] == 'numberline' else 2.8) + 0.1
        fit = max(0.45, min(box, (8.85 - fixed) / len(qs)))
        for q in qs:
            n += 1
            qp = para(d, '', after=3, before=4); runs(qp, '%d.  ' % n, 11, True, color=BLUE); runs(qp, q['text'], 11)
            if q.get('fig'): d.add_picture(imgs['fig%d' % n], width=Inches(5.4 if q['fig'][0] == 'numberline' else 2.8)); d.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            if q.get('starter'):
                sp = para(d, '', after=3); sp.paragraph_format.left_indent = Inches(0.3); runs(sp, 'Starter: ', 10, True, color='2E7D4F'); runs(sp, q['starter'], 10, italic=True)
            answer_box(d, q.get('lines') or fit)
    heading(d, 'Final Product: ' + p['product'], 0, True)
    para(d, 'Your final product must include:', 11, True, after=3)
    for f in L['final']: bullet(d, f)
    heading(d, 'Reflection')
    for j, (rq, _) in enumerate(L['reflect']):
        qp = para(d, '', after=3, before=4); runs(qp, 'R%d.  ' % (j + 1), 11, True, color=BLUE); runs(qp, rq, 11); answer_box(d, 1.2)
    heading(d, 'Scoring Rubric', 0, True)
    simple_table(d, RUBRIC_HEAD, rubric_rows(p), [1.3, 1.45, 1.4, 1.4, 1.35], size=9, zebra=False, first_col_fill='F2F2F2')
    footer(d, '%s Project · %s · %s · Editable – customize as needed' % (short(p), p['title'], lname))
    d.core_properties.title = '%s (%s)' % (p['title'], lname); d.core_properties.author = "Mr. K's Classroom"
    d.save(out)


def teacher_docx(p, out):
    d = new_doc(); banner(d, p, 'Teacher', p['accent'], 'Teacher Guide & Answer Keys')
    heading(d, 'Project Overview', 4)
    for s in p['overview']: para(d, s, 11, after=6)
    heading(d, 'Standards Addressed')
    for s in p['standards']: bullet(d, s)
    heading(d, 'Pacing (2–3 class periods)')
    simple_table(d, ['Day', 'Plan'], p['pacing'], [1.0, 5.9])
    heading(d, 'Materials')
    for s in p['materials']: bullet(d, s)
    heading(d, 'How the Three Versions Differ')
    simple_table(d, ['Level', 'What changes'], [[n, p['differ'][k]] for k, n, _, _ in LEVELS], [1.0, 5.9])
    heading(d, 'Watch For (Common Misconceptions)')
    for s in p['watch']: bullet(d, s)
    heading(d, 'Extension Ideas')
    for s in p['extensions']: bullet(d, s)
    for k, n, _, _ in LEVELS:
        L = p['levels'][k]; heading(d, 'Answer Key – ' + n, 0, True); num = 0
        for i, (title, _, qs) in enumerate(L['parts']):
            para(d, 'Part %d: %s' % (i + 1, title), 12, True, color=NAVY, after=3, before=6).paragraph_format.keep_with_next = True
            rows = []
            for q in qs: num += 1; rows.append([str(num), q['text'], q['answer']])
            simple_table(d, ['#', 'Task', 'Answer'], rows, [0.4, 3.1, 3.4], size=9.5)
        para(d, 'Reflection', 12, True, color=NAVY, after=3, before=6).paragraph_format.keep_with_next = True
        simple_table(d, ['#', 'Prompt', 'Look for'], [['R%d' % (j + 1), r, a] for j, (r, a) in enumerate(L['reflect'])], [0.4, 3.1, 3.4], size=9.5, spacer=False)
    footer(d, '%s Project · %s · Teacher Guide & Answer Keys' % (short(p), p['title']))
    d.core_properties.title = p['title'] + ' Teacher Guide'; d.core_properties.author = "Mr. K's Classroom"
    d.save(out)


# ---------------------------------------------------------------- PowerPoint
def rgb(h): return PRGB.from_string(h)


def tb(slide, x, y, w, h, text='', size=18, bold=False, color='222222', align=None, italic=False, anchor=None):
    s = slide.shapes.add_textbox(PI(x), PI(y), PI(w), PI(h)); tf = s.text_frame; tf.word_wrap = True
    if anchor: tf.vertical_anchor = anchor
    tf.paragraphs[0].text = ''
    if text != '':
        r = tf.paragraphs[0].add_run(); r.text = flat(text); f = r.font; f.size = PPt(size); f.bold = bold; f.italic = italic; f.color.rgb = rgb(color); f.name = 'Calibri'
        if align: tf.paragraphs[0].alignment = align
    return s


def add_par(shape, parts, size=16, space=8):
    """parts: list of (text, bold, color)"""
    tf = shape.text_frame; p = tf.paragraphs[0] if not tf.paragraphs[0].runs and len(tf.paragraphs) == 1 else tf.add_paragraph()
    p.space_after = PPt(space)
    for t, b, c in parts:
        r = p.add_run(); r.text = flat(t); r.font.size = PPt(size); r.font.bold = b; r.font.color.rgb = rgb(c); r.font.name = 'Calibri'
    return p


def rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line=None):
    s = slide.shapes.add_shape(shape, PI(x), PI(y), PI(w), PI(h)); s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    if line: s.line.color.rgb = rgb(line)
    else: s.line.fill.background()
    s.shadow.inherit = False
    return s


def frame(prs, p, title, lname, lcol):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, 13.333, 0.95, NAVY); rect(s, 0, 0.95, 13.333, 0.06, BLUE)
    tb(s, 0.35, 0.18, 10.5, 0.6, title, 26, True, 'FFFFFF')
    pill = rect(s, 11.45, 0.25, 1.4, 0.45, lcol, MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = pill.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER; r = tf.paragraphs[0].add_run(); r.text = lname; r.font.size = PPt(14); r.font.bold = True; r.font.color.rgb = rgb('FFFFFF')
    tb(s, 0.35, 7.05, 10, 0.35, '%s: %s · %s' % (short(p), p['unit_name'], p['title']), 10, False, '8C8C8C', italic=True)
    return s


def student_pptx(p, lv, out, imgs):
    L = p['levels'][lv]; lname = dict((a, b) for a, b, _, _ in LEVELS)[lv]; lcol = dict((a, d) for a, _, _, d in LEVELS)[lv]
    prs = Presentation(); prs.slide_width, prs.slide_height = PI(13.333), PI(7.5)
    s = prs.slides.add_slide(prs.slide_layouts[6]); rect(s, 0, 0, 13.333, 7.5, NAVY); rect(s, 0, 5.85, 13.333, 0.08, BLUE)
    tb(s, 0.6, 0.55, 6.6, 0.4, kicker(p).upper(), 12, True, 'BFD7F2')
    tb(s, 0.6, 1.05, 6.6, 1.6, p['title'], 40, True, 'FFFFFF')
    tb(s, 0.6, 3.0, 6.4, 1.2, p['tagline'], 18, False, 'E8EEF5')
    pill = rect(s, 0.6, 4.45, 1.9, 0.55, lcol, MSO_SHAPE.ROUNDED_RECTANGLE); tf = pill.text_frame; tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    r = tf.paragraphs[0].add_run(); r.text = lname + ' Project'; r.font.size = PPt(15); r.font.bold = True; r.font.color.rgb = rgb('FFFFFF')
    tb(s, 2.7, 4.5, 3, 0.5, '2–3 class periods', 14, False, 'E8EEF5')
    rect(s, 7.35, 0.55, 5.4, 4.95, 'FFFFFF', MSO_SHAPE.ROUNDED_RECTANGLE); s.shapes.add_picture(imgs['hero'], PI(7.55), PI(1.2), width=PI(5.0))
    tb(s, 0.6, 6.25, 12, 0.5, 'Name: ______________________________        Group: ______________________________', 14, False, 'E8EEF5')
    s = frame(prs, p, 'The Scenario', lname, lcol); box = tb(s, 0.6, 1.4, 6.3, 5.3)
    for t in p['scenario']: add_par(box, [(t, False, '222222')], 17, 12)
    s.shapes.add_picture(imgs['hero'], PI(7.2), PI(1.6), width=PI(5.7))
    s = frame(prs, p, 'Learning Goals & Timeline', lname, lcol)
    tb(s, 0.6, 1.35, 6, 0.5, 'Learning Goals', 20, True, BLUE); box = tb(s, 0.6, 1.9, 6.6, 4.8)
    for g in L['goals']: add_par(box, [('• ' + g, False, '222222')], 17, 12)
    tb(s, 7.7, 1.35, 5, 0.5, 'Timeline', 20, True, BLUE)
    rows = [('Day %d' % (i + 1), pt[0]) for i, pt in enumerate(L['parts'])] + [('Final', p['product'] + ' + reflection')]
    for i, (a, b) in enumerate(rows):
        y = 1.95 + i * 0.95; rect(s, 7.7, y, 1.3, 0.75, BLUE); rect(s, 9.0, y, 3.9, 0.75, 'EEF2F7')
        tb(s, 7.7, y, 1.3, 0.75, a, 15, True, 'FFFFFF', PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE); tb(s, 9.15, y, 3.75, 0.75, b, 14, False, '222222', anchor=MSO_ANCHOR.MIDDLE)
    n = 0
    for i, (title, intro, qs) in enumerate(L['parts']):
        s = frame(prs, p, 'Part %d: %s' % (i + 1, title), lname, lcol)
        pic = imgs.get('cards') if (i == 0 and imgs.get('cards')) else imgs['hero']
        width = 8.1; box = tb(s, 0.6, 1.3, width, 5.6)
        add_par(box, [('Day %d · ' % (i + 1), True, BLUE), (intro, False, '222222')], 16, 12)
        long_ = sum(len(q['text']) + len(q.get('starter') or '') for q in qs) > 700
        for q in qs:
            n += 1; add_par(box, [('%d.  ' % n, True, BLUE), (q['text'], False, '222222')], 14 if long_ else 16, 8)
            if q.get('starter'): add_par(box, [('Starter: ', True, '2E7D4F'), (q['starter'], False, '444444')], 13 if long_ else 14, 8)
        s.shapes.add_picture(pic, PI(8.95), PI(2.0), width=PI(4.1))
    s = frame(prs, p, 'Final Product: ' + p['product'], lname, lcol); tb(s, 0.6, 1.35, 10, 0.5, 'Your final product must include:', 18, True, BLUE); box = tb(s, 0.6, 1.95, 12, 4.8)
    for f in L['final']: add_par(box, [('☐  ' + f, False, '222222')], 17, 10)
    s = frame(prs, p, 'Scoring Rubric', lname, lcol)
    rows = [RUBRIC_HEAD] + rubric_rows(p); t = s.shapes.add_table(len(rows), 5, PI(0.4), PI(1.3), PI(12.5), PI(5.5)).table
    for j, w in enumerate([2.1, 2.7, 2.6, 2.6, 2.5]): t.columns[j].width = PI(w)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.cell(i, j); c.text = ''; r = c.text_frame.paragraphs[0].add_run(); r.text = v; r.font.size = PPt(10.5 if i else 12); r.font.bold = (i == 0 or j == 0)
            r.font.color.rgb = rgb('FFFFFF' if i == 0 else '222222'); c.fill.solid(); c.fill.fore_color.rgb = rgb(BLUE if i == 0 else ('EDEDED' if j == 0 else 'FFFFFF'))
    s = frame(prs, p, 'Reflection', lname, lcol); box = tb(s, 0.6, 1.4, 12, 5)
    for j, (rq, _) in enumerate(L['reflect']): add_par(box, [('R%d.  ' % (j + 1), True, BLUE), (rq, False, '222222')], 18, 14)
    prs.core_properties.title = '%s (%s)' % (p['title'], lname); prs.core_properties.author = "Mr. K's Classroom"
    prs.save(out)


# ---------------------------------------------------------------- index page + registry
def index_html(p):
    src = open(os.path.join(SITE, 'artifacts/algebra1-project-aquarium-keeper/index.html'), encoding='utf-8').read()
    style = src[src.index('<style>'):src.index('</style>') + 8]
    head = '<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">\n<title>%s · %s Project</title>\n%s</head><body><div class="wrap">\n' % (
        html.escape(p['title']), COURSE_NAME[p['course']], style.replace('#C0392B', '#' + p['accent']))
    e = html.escape
    hero = ('<header class="hero"><div><div class="kicker">%s · Project</div>\n<h1>%s</h1><p class="tag">%s</p>\n<div class="meta"><span class="pill">2–3 class periods</span>'
            '<span class="pill">CP2 · CP1 · Honors</span><span class="pill">%s</span></div></div>\n<img src="hero.png" alt="Project illustration for %s"></header>\n<p class="desc">%s</p>\n<section class="levels">') % (
        e(kicker(p)), e(p['title']), e(p['tagline']), e(p['theme']), e(p['title']), e(flat(' '.join(p['overview'][:1]))))
    cards = ''
    for k, n, _, col in LEVELS:
        f = p['slug'] + '-' + k
        cards += ('<article class="card"><h2 style="background:#%s">%s</h2><p>%s</p><div class="btns">\n<a class="btn primary" style="background:#%s;border-color:#%s" href="%s.pdf" target="_self">View / print PDF</a>\n'
                  '<a class="btn" style="color:#%s" href="%s.docx" download>Word (.docx), editable</a>\n<a class="btn" style="color:#%s" href="%s.pptx" download>PowerPoint (.pptx), editable</a></div></article>') % (
            col, n, LEVEL_BLURB[k], col, col, f, col, f, col, f)
    return head + hero + cards + '</section>\n\n</div>\n</body></html>\n'


def registry_entry(p):
    return dict(folder=p['folder'], slug=p['slug'], title=p['title'], tagline=p['tagline'], description=p['description'], theme=p['theme'], product=p['product'])


def soffice_pdf(paths, outdir):
    for i in range(0, len(paths), 12):
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir] + paths[i:i + 12], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=600)


def build(projects, site=SITE):
    jobs = []
    for p in projects:
        d = os.path.join(site, 'artifacts', p['folder']); os.makedirs(d, exist_ok=True)
        p['_dir'] = d; p['_img'] = {'hero': os.path.join(d, 'hero.png')}
        jobs.append((hero_html(p['hero']), p['_img']['hero'], None, (1280, 800)))
        if p.get('cards'):
            p['_img']['cards'] = os.path.join(tempfile.gettempdir(), p['folder'] + '-cards.png')
            jobs.append((cards_html(p['cards']), p['_img']['cards'], '#w', (1130, 900)))
    render_images(jobs)
    thumbs = []
    for p in projects:
        e = html.escape
        thumbs.append((('<html><head><meta charset="utf-8"><style>%s</style></head><body><div class="k">%s · UNIT %s · PROJECT</div><h1>%s</h1><div class="box"><img src="file://%s"></div>'
                       '<div class="foot">CP2 · CP1 · Honors &nbsp; | &nbsp; 2–3 days</div></body></html>') % (THUMB_CSS % p['accent'], e(COURSE_NAME[p['course']].upper()), p['unit_no'], e(p['title']), p['_img']['hero']),
                       os.path.join(site, 'thumbs', p['folder'] + '.jpg'), None, (720, 450)))
    render_images(thumbs)
    docs = []
    for p in projects:
        d = p['_dir']
        for lv in ('cp2', 'cp1', 'honors'):
            imgs = dict(p['_img']); n = 0
            for part in p['levels'][lv]['parts']:
                for q in part[2]:
                    n += 1
                    if q.get('fig'):
                        imgs['fig%d' % n] = os.path.join(tempfile.gettempdir(), '%s-%s-fig%d.png' % (p['folder'], lv, n)); fig_png(q['fig'], imgs['fig%d' % n])
            student_docx(p, lv, os.path.join(d, '%s-%s.docx' % (p['slug'], lv)), imgs)
            student_pptx(p, lv, os.path.join(d, '%s-%s.pptx' % (p['slug'], lv)), imgs)
            docs.append(os.path.join(d, '%s-%s.docx' % (p['slug'], lv)))
        teacher_docx(p, os.path.join(d, '%s-teacher-guide.docx' % p['slug'])); docs.append(os.path.join(d, '%s-teacher-guide.docx' % p['slug']))
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(index_html(p))
    by_dir = {}
    for x in docs: by_dir.setdefault(os.path.dirname(x), []).append(x)
    for dd, xs in by_dir.items(): soffice_pdf(xs, dd)


def H(label, sky, ground, top, bottom, cards):
    """Auto-laid-out hero scene: top row (smaller, upper area) and bottom row (larger, on the ground)."""
    items = []
    for row, y0, size in ((top, 70, 92), (bottom, 300, 122)):
        n = len(row)
        for i, e in enumerate(row):
            x = 50 + (i * (760 - 100 - size) / max(1, n - 1) if n > 1 else (760 - size) / 2 - 50)
            items.append((e, int(x), y0 + (18 if i % 2 else 0), size))
    return dict(label=label, sky=sky, ground=ground, items=items, cards=cards)
