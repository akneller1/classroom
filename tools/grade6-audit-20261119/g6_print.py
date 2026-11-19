"""Grade 6 audit #14 (2026-11-19): two cumulative Grade 6 practice tests in the MCAS style and a Grade 6 reference sheet.
(Adapted from tools/grade7-audit-20261119/g3_print.py.)

artifacts/grade6-practice-test-{a,b}/exam.html and key.html: two sessions of 20 questions each, with the item types of the
    Grade 6 MCAS (multiple choice, select all that apply, short answer and a four-part constructed response).
    Session 1 covers The Number System and Expressions and Equations; Session 2 covers Ratios
    and Proportional Relationships, Geometry, and Statistics and Probability. Selected-response and short-answer items come
    from the CP1 and Honors bank items whose main standard is a Grade 6 standard, spread over the skills; no item is in both
    tests. The constructed-response questions are written here, and their answers are recomputed by
    scripts/test-grade6-c.cjs. The reference sheet is attached at the end of each test.
artifacts/grade6-reference-sheet/index.html: the formulas and conversions Grade 6 students use, written for this site.
print_g6.cjs turns the HTML into PDFs and card thumbnails. Deterministic. Usage (repository root):
    python3 tools/grade6-audit-20261119/g6_print.py && node tools/grade6-audit-20261119/print_g6.cjs
No calculator in either session, as on the Grade 6 MCAS."""
import html, json, os, random, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

SESSIONS = [('NS EE', 'Session 1 · No calculator'), ('RP G SP', 'Session 2 · No calculator')]
PER_SESSION = {'multiple-choice': 12, 'select-all': 3, 'short-answer': 4}
DOMAIN = {'RP': 'Ratios and Proportional Relationships', 'NS': 'The Number System', 'EE': 'Expressions and Equations', 'G': 'Geometry', 'SP': 'Statistics and Probability'}


def frac(n, d):
    return f'<span class="fr"><span>{n}</span><span>{d}</span></span>'


# Constructed response: written for these tests. Each part is worth 1 point. scripts/test-grade6-c.cjs recomputes the answers.
CR = {
 'a': [
  dict(domain='EE', title='Dog-walking business', stem='Nia charges a $5 sign-up fee and $8 for each walk.',
       parts=[('Write an equation for the total cost c of w walks.', 'c = 8w + 5'),
              ('Which variable is the independent variable? Explain.', 'w, the number of walks'),
              ('Use your equation to find the cost of 7 walks.', '$61'),
              ('A customer paid $85. How many walks did the customer get?', '10 walks')]),
  dict(domain='RP', title='Paint mixture', stem='A paint color uses 3 cups of blue paint for every 5 cups of white paint.',
       parts=[('What is the ratio of blue paint to the total amount of paint?', '3 : 8'),
              ('How many cups of white paint are needed with 12 cups of blue paint?', '20 cups'),
              ('What percent of the mixture is blue paint?', '37.5%'),
              ('Ana wants 40 cups of the mixture in all. How many cups of blue paint does she need?', '15 cups')])],
 'b': [
  dict(domain='NS', title='Map of a park', stem='On a coordinate map of a park, each unit is 10 meters. The gate is at (−6, 4), the fountain is at (5, 4) and the playground is at (5, −3).',
       parts=[('How many meters is it from the gate to the fountain?', '110 meters'),
              ('How many meters is it from the fountain to the playground?', '70 meters'),
              ('A bench is at the reflection of the gate across the x-axis. What are its coordinates?', '(−6, −4)'),
              ('How many meters is the walk gate → fountain → playground?', '180 meters')]),
  dict(domain='G', title='A storage box', stem='A storage box is a rectangular prism 2 1/2 feet long, 2 feet wide and 1 1/2 feet tall.',
       parts=[('What is the volume of the box?', '7 1/2 cubic feet'),
              ('What is the area of the bottom of the box?', '5 square feet'),
              ('What is the surface area of the box?', '23 1/2 square feet'),
              ('How many cubes with edges of 1/2 foot fill the box?', '60 cubes')])],
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
    body = f'''<div class="ref"><h2>Grade 6 Mathematics Reference Sheet</h2>
<div class="cols"><div>
<h3>Area</h3><table>
<tr><td>Rectangle</td><td>A = lw</td></tr>
<tr><td>Square</td><td>A = s<sup>2</sup></td></tr>
<tr><td>Parallelogram</td><td>A = bh</td></tr>
<tr><td>Triangle</td><td>A = {F(1, 2)}bh</td></tr>
<tr><td>Trapezoid</td><td>A = {F(1, 2)}(b<sub>1</sub> + b<sub>2</sub>)h</td></tr></table>
<h3>Volume and surface area</h3><table>
<tr><td>Rectangular prism</td><td>V = lwh = Bh (B = area of the base)</td></tr>
<tr><td>Cube</td><td>V = s<sup>3</sup></td></tr>
<tr><td>Surface area</td><td>SA = the sum of the areas of all the faces (use a net)</td></tr></table>
<h3>Coordinate plane</h3><table>
<tr><td>Distance, same x or same y</td><td>subtract the other coordinates; across an axis, add the absolute values</td></tr>
<tr><td>Reflection across the x-axis</td><td>(x, y) → (x, −y)</td></tr>
<tr><td>Reflection across the y-axis</td><td>(x, y) → (−x, y)</td></tr></table>
</div><div>
<h3>Ratios, rates and percents</h3><table>
<tr><td>Unit rate</td><td>for a : b, the unit rate is {F("a", "b")} per one unit of the second quantity</td></tr>
<tr><td>Percent</td><td>{F("part", "whole")} = {F("percent", 100)}</td></tr>
<tr><td>Whole from a part</td><td>whole = part ÷ {F("percent", 100)}</td></tr></table>
<h3>Statistics</h3><table>
<tr><td>Mean</td><td>{F("sum of the values", "number of values")}</td></tr>
<tr><td>Median</td><td>the middle value of the ordered data</td></tr>
<tr><td>Range</td><td>maximum − minimum</td></tr>
<tr><td>Interquartile range</td><td>IQR = Q3 − Q1</td></tr>
<tr><td>Mean absolute deviation</td><td>{F("sum of the distances from the mean", "number of values")}</td></tr></table>
<h3>Conversions</h3><table>
<tr><td>Length</td><td>1 ft = 12 in. · 1 yd = 3 ft · 1 mi = 5,280 ft<br>1 m = 100 cm · 1 km = 1,000 m</td></tr>
<tr><td>Capacity</td><td>1 c = 8 fl oz · 1 pt = 2 c · 1 qt = 2 pt · 1 gal = 4 qt<br>1 L = 1,000 mL</td></tr>
<tr><td>Weight and mass</td><td>1 lb = 16 oz · 1 T = 2,000 lb<br>1 kg = 1,000 g</td></tr>
<tr><td>Time</td><td>1 h = 60 min · 1 min = 60 s</td></tr></table>
</div></div>
<p class="foot">Written for Mr. K’s Classroom to collect the formulas and conversions used in Grade 6. It is not the official MCAS reference sheet; check the Massachusetts DESE site for the sheet students receive on the test.</p></div>'''
    if not standalone:
        return body
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Grade 6 Reference Sheet · Mr. K’s Classroom</title>'
            f'<style>{CSS}</style></head><body><div class="eyebrow">6th Grade Math · Reference</div><h1>Grade 6 Reference Sheet</h1>'
            '<p>Area, volume and coordinate-plane facts, ratio, percent and statistics formulas, and unit conversions on one page. Keep it with your notes and use it on the practice tests.</p>'
            f'{body}</body></html>')


# ------------------------------------------------------------------------------------------------- tests
def domain(q):
    return q['standards'][0].split('.')[1] if q.get('standards') and q['standards'][0].startswith('6.') else None


# Items added after the tests are built can be listed here so the published tests do not reshuffle.
LATER = re.compile(r'family: g6_later_none\b')


def usable(q):
    if LATER.search(q.get('sourceNotes', '')):
        return False
    if q['level'] not in ('cp1', 'honors') or domain(q) is None:
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
    rng = random.Random('grade6-mcas-practice')
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
    title = f'Grade 6 Practice Test {ex.upper()}'
    P = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}{" · Teacher key" if key else ""}</title><style>{CSS}</style></head><body>']
    P.append(f'<div class="cover"><div class="eyebrow">6th Grade Math · MCAS review</div><h1>{title}{" — Teacher Key" if key else ""}</h1>')
    if not key:
        P.append('<div class="name"><span>Name</span><span>Date</span><span>Period</span></div>')
    P.append('<table><tr><th>Session</th><th>Questions</th><th>Tools</th><th>Points</th></tr>'
             '<tr><td>1 · The Number System; Expressions and Equations</td><td>20 (1–20): 12 multiple choice, 3 select all, 4 short answer, 1 constructed response</td><td>No calculator; reference sheet</td><td>23</td></tr>'
             '<tr><td>2 · Ratios and Proportional Relationships; Geometry; Statistics and Probability</td><td>20 (21–40): 12 multiple choice, 3 select all, 4 short answer, 1 constructed response</td><td>No calculator; reference sheet</td><td>23</td></tr></table>')
    P.append('<div class="box"><b>How to give it.</b> Give one session per class period (about 60 minutes each, untimed for students who need it). '
             'The item types follow the Grade 6 MCAS, and as on that test, calculators are not used: multiple choice (one answer), select all that apply (every correct choice and no wrong ones), short answer (a number or expression) and a four-part constructed response. '
             'Students may use the Grade 6 reference sheet at the end of this booklet in both sessions. This is a practice test written for this site, not a released MCAS test.</div>')
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
    P.append(f'<p class="foot">Mr. K’s Classroom · {title}{" · Teacher key" if key else ""}. Questions 1–19 and 21–39 come from the 6th Grade Math question banks, whose answer keys are recomputed in CI (verify_keys.py).</p></body></html>')
    return ''.join(P)


def main():
    banks = lib.load()
    for u in lib.UNITS:
        for q in banks[u]['questions']:
            q['unit'] = u
    js = ('const fs=require("fs"),vm=require("vm");const g={window:{}};for(const p of ["data.js","course-catalog.js"])vm.runInNewContext(fs.readFileSync(p,"utf8"),g);'
          'const C=g.window.MK_COURSE_CATALOG,o={};for(const u of %s)for(const s of C.getSkillRecords("math6",u))o[s.id]=s.name;console.log(JSON.stringify(o))') % json.dumps(lib.UNITS)
    names = json.loads(subprocess.run(['node', '-e', js], cwd=lib.ROOT, capture_output=True, text=True, check=True).stdout)
    used = pick(banks)
    ids = {ex: [q['id'] for doms, _ in SESSIONS for q in used[ex][doms]] for ex in used}
    assert not set(ids['a']) & set(ids['b']) and len(ids['a']) == len(ids['b']) == 38
    for ex in ('a', 'b'):
        out = os.path.join(lib.ROOT, 'artifacts', f'grade6-practice-test-{ex}')
        os.makedirs(out, exist_ok=True)
        for key in (False, True):
            open(os.path.join(out, 'key.html' if key else 'exam.html'), 'w', encoding='utf-8').write(test_page(ex, used[ex], names, key))
    out = os.path.join(lib.ROOT, 'artifacts', 'grade6-reference-sheet')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(reference_html(True))
    json.dump({'tests': ids, 'cr': CR}, open(os.path.join(os.path.dirname(__file__), 'practice-tests.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('practice tests: 38 bank items + 2 constructed response each; reference sheet written')


if __name__ == '__main__':
    main()
