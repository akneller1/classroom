"""Grade 7 audit #18 (2026-11-19): two cumulative Grade 7 practice tests in the MCAS style and a Grade 7 reference sheet.

artifacts/grade7-practice-test-{a,b}/exam.html and key.html: two sessions of 20 questions each, with the item types of the
    Grade 7 MCAS (multiple choice, select all that apply, short answer and a four-part constructed response).
    Session 1 (no calculator) covers The Number System and Expressions and Equations; Session 2 (calculator) covers Ratios
    and Proportional Relationships, Geometry, and Statistics and Probability. Selected-response and short-answer items come
    from the CP1 and Honors bank items whose main standard is a Grade 7 standard, spread over the skills; no item is in both
    tests. The constructed-response questions are written here, and their answers are recomputed by
    scripts/test-grade7-g3.cjs. The reference sheet is attached at the end of each test.
artifacts/grade7-reference-sheet/index.html: the formulas and conversions Grade 7 students use, written for this site.
print_g3.cjs turns the HTML into PDFs and card thumbnails. Deterministic. Usage (repository root):
    python3 tools/grade7-audit-20261119/g3_print.py && node tools/grade7-audit-20261119/print_g3.cjs"""
import html, json, os, random, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

SESSIONS = [('NS EE', 'Session 1 · No calculator'), ('RP G SP', 'Session 2 · Calculator allowed')]
PER_SESSION = {'multiple-choice': 12, 'select-all': 3, 'short-answer': 4}
DOMAIN = {'RP': 'Ratios and Proportional Relationships', 'NS': 'The Number System', 'EE': 'Expressions and Equations', 'G': 'Geometry', 'SP': 'Statistics and Probability'}


def frac(n, d):
    return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'


# Constructed response: written for these tests. Each part is worth 1 point. scripts/test-grade7-g3.cjs recomputes the answers.
CR = {
 'a': [
  dict(domain='EE', title='Saving plans', stem='Maya has $120 in savings and adds $15 each week. Leo has $40 and adds $25 each week.',
       parts=[('Write an expression for the amount Maya has after w weeks.', '120 + 15w'),
              ('Write and solve an equation to find after how many weeks Maya and Leo have the same amount.', '120 + 15w = 40 + 25w; w = 8'),
              ('How much money does each person have at that time?', '$240'),
              ('Write and solve an inequality to find the least whole number of weeks after which Leo has more than $300.', '40 + 25w > 300; w > 10.4, so 11 weeks')]),
  dict(domain='RP', title='Markup, sale and tax', stem='A store buys a jacket for $48 and marks the price up 75%. Later the jacket is on sale for 20% off, and a 6.25% sales tax is added at the register.',
       parts=[('What is the selling price before the sale?', '$84'),
              ('What is the sale price?', '$67.20'),
              ('What is the total cost with tax?', '$71.40'),
              ('By what percent is the total cost greater than the store’s cost of $48? Round to the nearest tenth of a percent.', '48.8%')])],
 'b': [
  dict(domain='NS', title='Temperature changes', stem='At 6:00 a.m. the temperature was −9°F. It rose 4°F each hour until noon, then fell 3°F each hour until 4:00 p.m.',
       parts=[('What was the temperature at noon?', '15°F'),
              ('What was the temperature at 4:00 p.m.?', '3°F'),
              ('Write an expression using integers for the total change from 6:00 a.m. to 4:00 p.m., and evaluate it.', '6(4) + 4(−3) = 12°F'),
              ('What is the difference between the highest and lowest temperatures of the day? Show it as the distance between two numbers on a number line.', '|15 − (−9)| = 24°F')]),
  dict(domain='G', title='A circular garden', stem='A circular garden has a radius of 6 feet. A path 2 feet wide goes around it. Use 3.14 for π.',
       parts=[('What is the area of the garden?', '113.04 square feet'),
              ('What is the area of the path alone?', '87.92 square feet'),
              ('Fencing goes around the outside edge of the path. How many feet of fencing are needed?', '50.24 feet'),
              ('On a scale drawing, 1 inch represents 4 feet. What is the diameter of the outside edge of the path on the drawing?', '4 inches')])],
}

CSS = '''
@page { size: letter; margin: 0.5in 0.55in; }
* { box-sizing: border-box; }
body { font-family: "Atkinson Hyperlegible", Inter, "DejaVu Sans", Arial, sans-serif; color: #14173a; font-size: 10.5pt; line-height: 1.4; margin: 0; }
h1 { font-size: 22pt; margin: 0 0 4px; } h3 { font-size: 12pt; margin: 8px 0 4px; } h2 { font-size: 14pt; margin: 0 0 6px; border-bottom: 2.5px solid #14173a; padding-bottom: 3px; }
.eyebrow { font-size: 9pt; letter-spacing: .12em; text-transform: uppercase; color: #3547f5; font-weight: 700; }
.name { display: flex; gap: 14px; margin: 10px 0 14px; } .name span { flex: 1; border-bottom: 1.5px solid #14173a; padding-bottom: 2px; } .name span:first-child { flex: 2.2; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 12px; } th, td { border: 1.5px solid #14173a; padding: 4px 7px; text-align: left; vertical-align: top; } th { background: #e2e6ff; }
.box { background: #e6e9f8; border-radius: 8px; padding: 8px 12px; margin: 8px 0; }
.section { break-before: page; }
ol.mc { padding-left: 24px; margin: 0; } ol.mc > li { break-inside: avoid; margin-bottom: 14px; }
.q { white-space: pre-wrap; }
.choices { display: grid; grid-template-columns: 1fr 1fr; gap: 3px 18px; margin-top: 4px; }
.choices div { break-inside: avoid; } .choices b { margin-right: 6px; }
.sel div { margin: 2px 0; } .sel span.bx { display: inline-block; width: 11px; height: 11px; border: 1.5px solid #14173a; margin-right: 7px; vertical-align: -1px; }
.blank { display: inline-block; min-width: 1.8in; border-bottom: 1.5px solid #14173a; height: 18px; margin-top: 4px; }
.tag { font-size: 8pt; color: #4a4f78; margin-left: 6px; font-weight: 700; letter-spacing: .04em; }
img.dg { max-width: 340px; max-height: 200px; display: block; margin: 5px 0; }
.cr { break-inside: avoid; margin: 0 0 12px; } .part { break-inside: avoid; margin: 8px 0 0; } .work { height: 1.05in; border-bottom: 1px dashed #9aa0c8; }
.ans { color: #c8102e; font-weight: 700; } .steps { margin: 3px 0 0 18px; padding: 0; color: #2b2f55; } .steps li { margin-bottom: 2px; }
.foot { font-size: 8.5pt; color: #4a4f78; margin-top: 10px; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; font-size: .92em; line-height: 1.05; margin: 0 2px; }
.fr span:first-child { border-bottom: 1.2px solid currentColor; padding: 0 2px; }
.ref h3 { margin: 8px 0 3px; border-bottom: 1.5px solid #9aa0c8; } .ref table { margin: 3px 0 6px; } .ref td, .ref th { font-size: 9.6pt; padding: 3px 6px; } .ref td:first-child { width: 34%; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 18px; }
'''


def esc(s):
    return html.escape(str(s), quote=False)


# ------------------------------------------------------------------------------------------------- reference sheet
def reference_html(standalone=True):
    F = frac
    body = f'''<div class="ref"><h2>Grade 7 Mathematics Reference Sheet</h2>
<div class="cols"><div>
<h3>Area</h3><table>
<tr><td>Rectangle</td><td>A = lw</td></tr>
<tr><td>Parallelogram</td><td>A = bh</td></tr>
<tr><td>Triangle</td><td>A = {F(1, 2)}bh</td></tr>
<tr><td>Trapezoid</td><td>A = {F(1, 2)}(b<sub>1</sub> + b<sub>2</sub>)h</td></tr>
<tr><td>Circle</td><td>A = πr<sup>2</sup></td></tr></table>
<h3>Circles</h3><table>
<tr><td>Circumference</td><td>C = πd = 2πr</td></tr>
<tr><td>Diameter</td><td>d = 2r</td></tr>
<tr><td>π</td><td>π ≈ 3.14 or π ≈ {F(22, 7)}</td></tr></table>
<h3>Volume and surface area</h3><table>
<tr><td>Right prism</td><td>V = Bh (B = area of the base)</td></tr>
<tr><td>Rectangular prism</td><td>V = lwh</td></tr>
<tr><td>Surface area</td><td>SA = the sum of the areas of all the faces</td></tr>
<tr><td>Cube</td><td>V = s<sup>3</sup>, SA = 6s<sup>2</sup></td></tr></table>
<h3>Angles</h3><table>
<tr><td>Complementary</td><td>measures add to 90°</td></tr>
<tr><td>Supplementary</td><td>measures add to 180°</td></tr>
<tr><td>Vertical angles</td><td>equal measures</td></tr>
<tr><td>Triangle</td><td>angle measures add to 180°</td></tr></table>
</div><div>
<h3>Percents and money</h3><table>
<tr><td>Percent</td><td>{F("part", "whole")} = {F("percent", 100)}</td></tr>
<tr><td>Percent of change</td><td>{F("amount of change", "original amount")} × 100%</td></tr>
<tr><td>Percent error</td><td>{F("|estimate − actual|", "actual")} × 100%</td></tr>
<tr><td>Simple interest</td><td>I = Prt (r as a decimal, t in years)</td></tr></table>
<h3>Proportional relationships</h3><table>
<tr><td>Equation</td><td>y = kx, where k = {F("y", "x")} is the constant of proportionality</td></tr>
<tr><td>Unit rate</td><td>the value of y when x = 1</td></tr></table>
<h3>Probability</h3><table>
<tr><td>Theoretical probability</td><td>P(event) = {F("number of favorable outcomes", "number of possible outcomes")}</td></tr>
<tr><td>Complement</td><td>P(not A) = 1 − P(A)</td></tr>
<tr><td>Independent events</td><td>P(A and B) = P(A) · P(B)</td></tr></table>
<h3>Conversions</h3><table>
<tr><td>Length</td><td>1 ft = 12 in. · 1 yd = 3 ft · 1 mi = 5,280 ft<br>1 m = 100 cm · 1 km = 1,000 m · 1 in. = 2.54 cm</td></tr>
<tr><td>Capacity</td><td>1 c = 8 fl oz · 1 pt = 2 c · 1 qt = 2 pt · 1 gal = 4 qt<br>1 L = 1,000 mL</td></tr>
<tr><td>Weight and mass</td><td>1 lb = 16 oz · 1 T = 2,000 lb<br>1 kg = 1,000 g</td></tr>
<tr><td>Time</td><td>1 h = 60 min · 1 yr = 52 weeks = 365 days</td></tr></table>
</div></div>
<p class="foot">Written for Mr. K’s Classroom to collect the formulas and conversions used in Grade 7. It is not the official MCAS reference sheet; check the Massachusetts DESE site for the sheet students receive on the test.</p></div>'''
    if not standalone:
        return body
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Grade 7 Reference Sheet · Mr. K’s Classroom</title>'
            f'<style>{CSS}</style></head><body><div class="eyebrow">Pre-Algebra · Reference</div><h1>Grade 7 Reference Sheet</h1>'
            '<p>Area, circle, volume and angle facts, percent and probability formulas, and unit conversions on one page. Keep it with your notes and use it on the practice tests.</p>'
            f'{body}</body></html>')


# ------------------------------------------------------------------------------------------------- tests
def domain(q):
    return q['standards'][0].split('.')[1] if q.get('standards') and q['standards'][0].startswith('7.') else None


# Items added after the tests were built (batch G4) stay out of the pools, so the published tests do not reshuffle.
LATER = re.compile(r'family: g7_(rewrite_meaning|rewrite_percent|polygon_angle|polygon_algebra|congruent_\w+|circle_figure|circle_area_figure|scale_drawing_figure|dot_plot_compare)\b')


def usable(q):
    if LATER.search(q.get('sourceNotes', '')):
        return False
    if q['level'] not in ('cp1', 'honors') or domain(q) is None or q['unit'] == 'nonlinear-functions-polynomials':
        return False
    if q['format'] == 'multiple-choice':
        return len(q['options']) == 4 and sum(o['correct'] for o in q['options']) == 1 and len(q['prompt']) >= 40 and not q['prompt'].startswith('Error analysis')
    if q['format'] == 'select-all':
        return 4 <= len(q['options']) <= 6 and 1 <= sum(o['correct'] for o in q['options']) < len(q['options'])
    if q['format'] == 'short-answer':
        a = str(q['answer'])
        return (len(a) <= 14 and len(q['prompt']) >= 30 and not q.get('diagram')
                and re.fullmatch(r'[-−]?\$?\d[\d.,/ ]*%?(?: [a-zA-Z.²³ ]+)?', a) is not None)
    return False


def pick(banks):
    rng = random.Random('grade7-mcas-practice')
    used = {'a': {}, 'b': {}}
    for doms, _ in SESSIONS:
        for fmt, n in PER_SESSION.items():
            pool = [q for _, q in lib.items(banks) if q['format'] == fmt and domain(q) in doms.split() and usable(q)]
            by = {}
            for q in sorted(pool, key=lambda q: q['id']):
                by.setdefault(q['skillId'], []).append(q)
            for v in by.values():
                rng.shuffle(v)
            skills = sorted(by)
            rng.shuffle(skills)
            for ex in ('a', 'b'):
                got, i = [], 0
                seen = {q['skillId'] for qs in used[ex].values() for q in qs}
                while len(got) < n:
                    sk = skills[i % len(skills)]; i += 1
                    # each skill once per test while unused skills remain, then repeats
                    if by[sk] and (sk not in seen or i > len(skills)):
                        got.append(by[sk].pop()); seen.add(sk)
                    if i > 50 * len(skills):
                        raise SystemExit(f'not enough {fmt} items for {doms}')
                used[ex].setdefault(doms, []).extend(got)
    return used


def item_html(q, n, key):
    d = q.get('diagram') or {}
    im = f'<img class="dg" src="../../{esc(d["spec"]["src"])}" alt="{esc(d["spec"].get("alt", ""))}">' if (d.get('spec') or {}).get('src') else ''
    kind = {'multiple-choice': 'Multiple choice', 'select-all': 'Select all that apply', 'short-answer': 'Short answer'}[q['format']]
    out = f'<li value="{n}"><div class="q">{esc(q["prompt"])}<span class="tag">{kind.upper()}</span></div>{im}'
    if q['format'] == 'multiple-choice':
        out += '<div class="choices">' + ''.join(f'<div><b>({"ABCD"[i]})</b>{esc(o["text"])}</div>' for i, o in enumerate(q['options'])) + '</div>'
    elif q['format'] == 'select-all':
        out += '<div class="sel">' + ''.join(f'<div><span class="bx"></span>{esc(o["text"])}</div>' for o in q['options']) + '</div>'
    else:
        out += '<div>Answer: <span class="blank"></span></div>' if not key else ''
    if key:
        out += f'<div class="ans">Answer: {esc(key_text(q))}</div><ol class="steps">' + ''.join(f'<li>{esc(s)}</li>' for s in q.get('solutionSteps', [])) + '</ol>'
    return out + '</li>'


def key_text(q):
    if q['format'] == 'multiple-choice':
        return '(' + 'ABCD'[[o['correct'] for o in q['options']].index(True)] + ') ' + str(q['answer'])
    if q['format'] == 'select-all':
        return '; '.join(o['text'] for o in q['options'] if o['correct'])
    return str(q['answer'])


def cr_html(c, n, key):
    out = f'<li value="{n}" class="cr"><div class="q"><b>{esc(c["title"])}.</b> {esc(c["stem"])}<span class="tag">CONSTRUCTED RESPONSE · 4 POINTS</span></div>'
    for i, (p, a) in enumerate(c['parts']):
        out += f'<div class="part"><div class="q"><b>({"abcd"[i]})</b> {esc(p)}</div>'
        out += f'<div class="ans">{esc(a)}</div>' if key else '<div class="work"></div>'
        out += '</div>'
    if key:
        out += '<div class="foot">Scoring: 1 point for each part with a correct answer and supporting work; give the point for a correct method with one arithmetic slip in part (c) or (d) when it follows from an earlier wrong answer.</div>'
    return out + '</li>'


def test_page(ex, items, names, key):
    title = f'Grade 7 Practice Test {ex.upper()}'
    P = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}{" · Teacher key" if key else ""}</title><style>{CSS}</style></head><body>']
    P.append(f'<div class="cover"><div class="eyebrow">Pre-Algebra · MCAS review</div><h1>{title}{" — Teacher Key" if key else ""}</h1>')
    if not key:
        P.append('<div class="name"><span>Name</span><span>Date</span><span>Period</span></div>')
    P.append('<table><tr><th>Session</th><th>Questions</th><th>Tools</th><th>Points</th></tr>'
             '<tr><td>1 · The Number System; Expressions and Equations</td><td>20 (1–20): 12 multiple choice, 3 select all, 4 short answer, 1 constructed response</td><td>No calculator; reference sheet</td><td>23</td></tr>'
             '<tr><td>2 · Ratios and Proportional Relationships; Geometry; Statistics and Probability</td><td>20 (21–40): 12 multiple choice, 3 select all, 4 short answer, 1 constructed response</td><td>Calculator; reference sheet</td><td>23</td></tr></table>')
    P.append('<div class="box"><b>How to give it.</b> Give one session per class period (about 60 minutes each, untimed for students who need it). '
             'The item types follow the Grade 7 MCAS: multiple choice (one answer), select all that apply (every correct choice and no wrong ones), short answer (a number or expression) and a four-part constructed response. '
             'Students may use the Grade 7 reference sheet at the end of this booklet in both sessions. This is a practice test written for this site, not a released MCAS test.</div>')
    if key:
        P.append('<div class="box"><b>Scoring.</b> Multiple choice, select all and short answer: 1 point each (select all is all-or-nothing). Constructed response: 4 points, 1 for each part. '
                 '46 points in all. Use the domain totals below to plan review.</div>')
        rows, n = '', 0
        for doms, _ in SESSIONS:
            for q in items[doms]:
                n += 1
                rows += f'<tr><td>{n}</td><td>{esc(key_text(q))}</td><td>{esc(DOMAIN[domain(q)])}</td><td>{esc(names.get(q["skillId"], ""))}</td><td>{esc(", ".join(q["standards"]))}</td></tr>'
            n += 1
            c = CR[ex][SESSIONS.index((doms, _))]
            rows += f'<tr><td>{n}</td><td>4-point constructed response</td><td>{esc(DOMAIN[c["domain"]])}</td><td>{esc(c["title"])}</td><td></td></tr>'
        P.append('<h2>Answer key</h2><table><tr><th>#</th><th>Key</th><th>Domain</th><th>Skill</th><th>Standards</th></tr>' + rows + '</table>')
    P.append('</div>')
    n = 0
    for si, (doms, head) in enumerate(SESSIONS):
        P.append(f'<div class="section"><h2>{esc(head)}</h2><ol class="mc">')
        for q in items[doms]:
            n += 1
            P.append(item_html(q, n, key))
        n += 1
        P.append(cr_html(CR[ex][si], n, key) + '</ol></div>')
    if not key:
        P.append('<div class="section">' + reference_html(False) + '</div>')
    P.append(f'<p class="foot">Mr. K’s Classroom · {title}{" · Teacher key" if key else ""}. Questions 1–19 and 21–39 come from the Pre-Algebra question banks, whose answer keys are recomputed in CI (verify_keys.py).</p></body></html>')
    return ''.join(P)


def main():
    banks = lib.load()
    for u in lib.UNITS:
        for q in banks[u]['questions']:
            q['unit'] = u
    js = ('const fs=require("fs"),vm=require("vm");const g={window:{}};for(const p of ["data.js","course-catalog.js"])vm.runInNewContext(fs.readFileSync(p,"utf8"),g);'
          'const C=g.window.MK_COURSE_CATALOG,o={};for(const u of %s)for(const s of C.getSkillRecords("prealgebra7",u))o[s.id]=s.name;console.log(JSON.stringify(o))') % json.dumps(lib.UNITS)
    names = json.loads(subprocess.run(['node', '-e', js], cwd=lib.ROOT, capture_output=True, text=True, check=True).stdout)
    used = pick(banks)
    ids = {ex: [q['id'] for doms, _ in SESSIONS for q in used[ex][doms]] for ex in used}
    assert not set(ids['a']) & set(ids['b']) and len(ids['a']) == len(ids['b']) == 38
    for ex in ('a', 'b'):
        out = os.path.join(lib.ROOT, 'artifacts', f'grade7-practice-test-{ex}')
        os.makedirs(out, exist_ok=True)
        for key in (False, True):
            open(os.path.join(out, 'key.html' if key else 'exam.html'), 'w', encoding='utf-8').write(test_page(ex, used[ex], names, key))
    out = os.path.join(lib.ROOT, 'artifacts', 'grade7-reference-sheet')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(reference_html(True))
    json.dump({'tests': ids, 'cr': CR}, open(os.path.join(os.path.dirname(__file__), 'practice-tests.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('practice tests: 38 bank items + 2 constructed response each; reference sheet written')


if __name__ == '__main__':
    main()
