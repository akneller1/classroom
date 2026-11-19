"""Statistics audit #16 and #17 (2026-11-18): printable AP Statistics practice exams and the tables and formula sheet.

#17 artifacts/statistics-tables-formulas/index.html: Table A (standard Normal, area to the left of z), Table B
    (t critical values) and Table C (chi-square critical values), computed here with scipy, and a formula sheet with the
    formulas students use on the AP Statistics exam (descriptive statistics, probability, sampling distributions and
    inference), written for this site. Linked from every Statistics unit.
#16 artifacts/statistics-ap-practice-exam-{a,b}/exam.html and key.html in the current AP Statistics format:
    Section I, 42 multiple-choice questions in 90 minutes; Section II, 4 free-response questions in 90 minutes, the third
    a complete inference problem. Multiple choice comes from the CP1 and Honors bank items, spread over the units and skills
    and leaving out the topics no longer in the AP course; no item is in both exams. The free-response questions are batch S2
    problems. The tables and formula sheet are attached at the end of each exam.
print_s3.cjs turns the HTML into PDFs and card thumbnails. Deterministic. Usage (repository root):
    python3 tools/statistics-audit-20261118/s3_print.py && node tools/statistics-audit-20261118/print_s3.cjs"""
import html, os, random, re, sys
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
import lib

QUOTA = [('exploring-data', 12), ('sampling-experimentation', 7), ('anticipating-patterns', 9), ('statistical-inference', 14)]
BEYOND_SKILLS = {'anticipating-patterns-skill-08', 'statistical-inference-skill-11', 'statistical-inference-skill-12', 'statistical-inference-skill-14'}
FRQ = {'a': ['stat-u1-s02-honors-f01', 'stat-u2-s07-honors-f01', 'stat-u4-s07-honors-f01', 'stat-u3-s09-honors-f01'],
       'b': ['stat-u1-s08-honors-f01', 'stat-u2-s04-honors-f01', 'stat-u4-s09-honors-f01', 'stat-u3-s10-honors-f01']}
FRQ_TOPIC = ['Exploring data', 'Collecting data', 'Inference (complete the four steps)', 'Probability and sampling distributions']
UNIT_NAME = {'exploring-data': 'Exploring Data', 'sampling-experimentation': 'Sampling and Experimentation', 'anticipating-patterns': 'Anticipating Patterns', 'statistical-inference': 'Statistical Inference'}
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
ol.mc { padding-left: 24px; margin: 0; } ol.mc > li { break-inside: avoid; margin-bottom: 12px; }
.q { white-space: pre-wrap; }
.choices { display: grid; grid-template-columns: 1fr 1fr; gap: 3px 18px; margin-top: 4px; }
.choices div { break-inside: avoid; } .choices b { margin-right: 6px; }
img.dg { max-width: 360px; max-height: 210px; display: block; margin: 5px 0; }
.frq { break-before: page; } .frq .q { margin-bottom: 6px; } .part { break-inside: avoid; margin: 10px 0 0; } .work { height: 1.35in; border-bottom: 1px dashed #9aa0c8; }
.ans { color: #c8102e; font-weight: 700; } .steps { margin: 3px 0 0 18px; padding: 0; color: #2b2f55; } .steps li { margin-bottom: 2px; }
.foot { font-size: 8.5pt; color: #4a4f78; margin-top: 10px; }
table.num { font-size: 7.6pt; line-height: 1.15; margin: 4px 0; } table.num th, table.num td { padding: 1.5px 3px; text-align: right; border-width: 1px; } table.num th { text-align: center; }
.tables .pg { break-before: page; } .tables .pg:first-child { break-before: auto; }
.fs h3 { margin: 10px 0 3px; border-bottom: 1.5px solid #9aa0c8; } .fs table td, .fs table th { font-size: 9.5pt; padding: 3px 6px; } .fs p { margin: 3px 0; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 18px; }
'''


def esc(s):
    return html.escape(str(s), quote=False)


# ------------------------------------------------------------------------------------------------- tables (#17)
def table_a():
    rows = []
    for half in ('neg', 'pos'):
        zs = [-(3.4 - i / 10) for i in range(35)] if half == 'neg' else [i / 10 for i in range(35)]
        body = ''
        for z in zs:
            cells = []
            for h in range(10):
                zz = z - h / 100 if half == 'neg' else z + h / 100
                cells.append(f'{stats.norm.cdf(round(zz, 2)):.4f}')
            lab = f'−{abs(z):.1f}' if half == 'neg' else f'{z:.1f}'
            body += f'<tr><th>{lab}</th>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
        head = '<tr><th>z</th>' + ''.join(f'<th>.0{h}</th>' for h in range(10)) + '</tr>'
        rows.append(f'<table class="num"><thead>{head}</thead><tbody>{body}</tbody></table>')
    return rows


TAIL = [0.25, 0.20, 0.15, 0.10, 0.05, 0.025, 0.02, 0.01, 0.005, 0.0025, 0.001, 0.0005]


def table_b():
    dfs = list(range(1, 31)) + [40, 50, 60, 80, 100, 1000]
    head = '<tr><th>df \\ p</th>' + ''.join(f'<th>{p:g}</th>' for p in TAIL) + '</tr>'
    body = ''
    for d in dfs:
        body += f'<tr><th>{d}</th>' + ''.join(f'<td>{stats.t.isf(p, d):.3f}</td>' for p in TAIL) + '</tr>'
    body += '<tr><th>∞ (z*)</th>' + ''.join(f'<td>{stats.norm.isf(p):.3f}</td>' for p in TAIL) + '</tr>'
    conf = '<tr><th>Confidence C</th>' + ''.join(f'<td>{round(100 * (1 - 2 * p), 1):g}%</td>' for p in TAIL) + '</tr>'
    return f'<table class="num"><thead>{head}</thead><tbody>{body}{conf}</tbody></table>'


def table_c():
    dfs = list(range(1, 31)) + [40, 50, 60, 80, 100]
    head = '<tr><th>df \\ p</th>' + ''.join(f'<th>{p:g}</th>' for p in TAIL) + '</tr>'
    body = ''.join(f'<tr><th>{d}</th>' + ''.join(f'<td>{stats.chi2.isf(p, d):.2f}</td>' for p in TAIL) + '</tr>' for d in dfs)
    return f'<table class="num"><thead>{head}</thead><tbody>{body}</tbody></table>'


FORMULAS = '''<div class="fs"><h2>Formulas for AP Statistics</h2>
<div class="cols"><div>
<h3>I. Descriptive statistics</h3>
<p>x̄ = Σxᵢ / n</p><p>sₓ = √( Σ(xᵢ − x̄)² / (n − 1) )</p>
<p>ŷ = a + bx, with ȳ = a + b·x̄</p><p>r = (1/(n − 1)) Σ ((xᵢ − x̄)/sₓ)((yᵢ − ȳ)/s_y)</p><p>b = r · s_y / sₓ</p>
<h3>II. Probability and distributions</h3>
<p>P(A ∪ B) = P(A) + P(B) − P(A ∩ B)</p><p>P(A | B) = P(A ∩ B) / P(B)</p>
<table><tr><th>Random variable</th><th>Mean</th><th>Standard deviation</th></tr>
<tr><td>Discrete X</td><td>μ_X = Σ xᵢ·P(xᵢ)</td><td>σ_X = √( Σ (xᵢ − μ_X)² P(xᵢ) )</td></tr>
<tr><td>Binomial X (n, p)</td><td>μ_X = np</td><td>σ_X = √( np(1 − p) )</td></tr>
<tr><td>Geometric X (beyond AP)</td><td>μ_X = 1/p</td><td>σ_X = √(1 − p)/p</td></tr></table>
<p>Binomial: P(X = x) = C(n, x) pˣ(1 − p)ⁿ⁻ˣ</p>
</div><div>
<h3>III. Sampling distributions and inference</h3>
<p>Standardized test statistic = (statistic − parameter) / (standard error of the statistic)</p>
<p>Confidence interval: statistic ± (critical value)(standard error of the statistic)</p>
<p>Chi-square statistic: χ² = Σ (observed − expected)² / expected</p>
<table><tr><th>Statistic</th><th>Mean</th><th>Standard deviation</th></tr>
<tr><td>p̂</td><td>p</td><td>√( p(1 − p)/n )</td></tr>
<tr><td>x̄</td><td>μ</td><td>σ/√n</td></tr>
<tr><td>p̂₁ − p̂₂</td><td>p₁ − p₂</td><td>√( p₁(1 − p₁)/n₁ + p₂(1 − p₂)/n₂ )</td></tr>
<tr><td>x̄₁ − x̄₂</td><td>μ₁ − μ₂</td><td>√( σ₁²/n₁ + σ₂²/n₂ )</td></tr></table>
<table><tr><th>Statistic</th><th>Standard error</th></tr>
<tr><td>p̂</td><td>√( p̂(1 − p̂)/n )</td></tr>
<tr><td>p̂₁ − p̂₂ (interval)</td><td>√( p̂₁(1 − p̂₁)/n₁ + p̂₂(1 − p̂₂)/n₂ )</td></tr>
<tr><td>p̂₁ − p̂₂ (test of p₁ = p₂)</td><td>√( p̂_c(1 − p̂_c)(1/n₁ + 1/n₂) ), p̂_c = (x₁ + x₂)/(n₁ + n₂)</td></tr>
<tr><td>x̄</td><td>s/√n</td></tr>
<tr><td>x̄₁ − x̄₂</td><td>√( s₁²/n₁ + s₂²/n₂ )</td></tr>
<tr><td>b (slope; beyond AP)</td><td>SE_b = s / (sₓ√(n − 1)), s = √( Σ(yᵢ − ŷᵢ)²/(n − 2) )</td></tr></table>
</div></div>
<p class="foot">Written for Mr. K’s Classroom to match the formulas students use on the AP Statistics exam. It is not the official College Board formula sheet; check the current Course and Exam Description for the exact sheet students receive.</p></div>'''


def tables_html(standalone=True):
    a_neg, a_pos = table_a()
    t = (f'<div class="tables"><div class="pg"><h2>Table A · Standard Normal probabilities (area to the left of z)</h2>{a_neg}</div>'
         f'<div class="pg"><h2>Table A (continued) · Standard Normal probabilities</h2>{a_pos}</div>'
         f'<div class="pg"><h2>Table B · t distribution critical values (upper-tail probability p)</h2>{table_b()}'
         '<p class="foot">Use the row for the degrees of freedom; t* for confidence level C is in the column with p = (1 − C)/2. If the exact df is not listed, use the next smaller df.</p></div>'
         f'<div class="pg"><h2>Table C · χ² critical values (upper-tail probability p)</h2>{table_c()}</div>'
         f'<div class="pg">{FORMULAS}</div></div>')
    if not standalone:
        return t
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Statistics Tables and Formula Sheet · Mr. K’s Classroom</title>'
            f'<style>{CSS}</style></head><body><div class="eyebrow">Statistics · Reference</div><h1>Tables A–C and Formula Sheet</h1>'
            '<p>Table A (standard Normal), Table B (t) and Table C (chi-square), with every value computed for this site, and the formulas used in AP Statistics. Print it double-sided and keep it with your notes.</p>'
            f'{t}</body></html>')


# ------------------------------------------------------------------------------------------------- exams (#16)
def pick_mc(banks):
    rng = random.Random('stat-ap-exams')
    used = {'a': [], 'b': []}
    for u, n in QUOTA:
        pool = [q for q in banks[u]['questions'] if q['format'] == 'multiple-choice' and q['level'] in ('cp1', 'honors') and q['skillId'] not in BEYOND_SKILLS
                and not any('BEYOND' in s for s in q.get('standards', [])) and not q['prompt'].startswith('Error analysis') and len(q['prompt']) >= 70
                and len(q['options']) == 4]
        by = {}
        for q in sorted(pool, key=lambda q: q['id']):
            by.setdefault(q['skillId'], []).append(q)
        for v in by.values():
            rng.shuffle(v)
        skills = sorted(by)
        for ex in ('a', 'b'):
            got, i = [], 0
            while len(got) < n:
                sk = skills[i % len(skills)]; i += 1
                if by[sk]:
                    got.append((u, by[sk].pop()))
            used[ex] += got
    return used


def mc_html(q, n, key=False):
    letters = 'ABCD'
    ch = ''.join(f'<div><b>({letters[i]})</b>{esc(o["text"])}</div>' for i, o in enumerate(q['options']))
    d = q.get('diagram') or {}
    im = f'<img class="dg" src="../../{esc(d["spec"]["src"])}" alt="{esc(d["spec"].get("alt", ""))}">' if (d.get('spec') or {}).get('src') else ''
    out = f'<li value="{n}"><div class="q">{esc(q["prompt"])}</div>{im}<div class="choices">{ch}</div>'
    if key:
        right = letters[[o['correct'] for o in q['options']].index(True)]
        out += f'<div class="ans">Answer: ({right}) {esc(q["answer"])}</div><ol class="steps">' + ''.join(f'<li>{esc(s)}</li>' for s in q['solutionSteps']) + '</ol>'
    return out + '</li>'


def frq_html(q, n, key=False):
    stem = q['prompt'].split('). ', 1)[1]
    stem = stem.replace(' Use the four steps: State, Plan, Do, Conclude.', '')
    out = f'<div class="frq">{"<h2>Section II · Free response · 90 minutes</h2><p>Answer all four questions. Show your work and explain your reasoning in context. Question 3 is a complete inference problem.</p>" if n == 1 else ""}<h3>Question {n} · {FRQ_TOPIC[n - 1]}</h3><div class="q">{esc(stem)}</div>'
    steps = q['solutionSteps']
    for p in q['parts']:
        out += f'<div class="part"><div class="q"><b>({p["label"]})</b> {esc(p["prompt"])}</div>'
        if key:
            mine = [s for s in steps if s.startswith(f'({p["label"]})')]
            out += f'<div class="ans">{esc(p["answer"])}</div><ol class="steps">' + ''.join(f'<li>{esc(s[4:])}</li>' for s in mine) + '</ol>'
        else:
            out += '<div class="work"></div>'
        out += '</div>'
    if key:
        out += f'<p class="ans">{esc(steps[-1])}</p>'
    return out + '</div>'


def exam_page(ex, mcs, frqs, names, key):
    title = f'AP Statistics Practice Exam {ex.upper()}'
    pts = [int(re.search(r'Total: (\d+)', q['solutionSteps'][-1]).group(1)) for q in frqs]
    P = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}{" · Teacher key" if key else ""}</title><style>{CSS}</style></head><body>']
    P.append(f'<div class="cover"><div class="eyebrow">Statistics · AP review</div><h1>{title}{" — Teacher Key and Scoring Guide" if key else ""}</h1>')
    if not key:
        P.append('<div class="name"><span>Name</span><span>Date</span><span>Period</span></div>')
    P.append('<table><tr><th>Section</th><th>Questions</th><th>Time</th><th>Weight</th></tr>'
             '<tr><td>I · Multiple choice</td><td>42 (1–42)</td><td>90 minutes</td><td>50%</td></tr>'
             '<tr><td>II · Free response</td><td>4 (1–4); question 3 is a complete inference problem</td><td>90 minutes</td><td>50%</td></tr></table>')
    P.append('<div class="box"><b>Timing notes.</b> The whole exam takes 3 hours. To give it over two class periods, do Section I one day and Section II the next. '
             'A graphing calculator is allowed throughout. Students use Tables A–C and the formula sheet at the end of this booklet. '
             'Topics that are no longer in the AP course (geometric distributions, combining random variables, chi-square goodness of fit and inference for slope) are not tested.</div>')
    if not key:
        P.append('<ul><li>Multiple choice: circle one answer. There is no penalty for guessing.</li><li>Free response: show your work, name the procedure you use, check its conditions, and give every conclusion in context.</li></ul>')
    else:
        P.append('<div class="box"><b>Scoring guide.</b> Section I: 1 point for each correct answer (42 points). Section II: score each part with the notes below '
                 f'({", ".join(str(p) for p in pts)} points; {sum(pts)} in all). To weight the two sections equally, compute '
                 f'<b>composite = {round(50 / 42, 3)} × (multiple-choice points) + {round(50 / sum(pts), 3)} × (free-response points)</b>, out of 100. '
                 'This is a practice estimate, not an official AP score conversion.</div>')
        rows = ''
        for n, (u, q) in enumerate(mcs, 1):
            right = 'ABCD'[[o['correct'] for o in q['options']].index(True)]
            rows += f'<tr><td>{n}</td><td>{right}</td><td>{esc(UNIT_NAME[u])}</td><td>{esc(names.get(q["skillId"], ""))}</td><td>{esc(", ".join(s.replace("APSTATS.", "") for s in q.get("standards", [])))}</td></tr>'
        P.append('<h2>Multiple-choice answers</h2><table><tr><th>#</th><th>Key</th><th>Unit</th><th>Skill</th><th>AP objectives</th></tr>' + rows + '</table>')
    P.append('</div>')
    P.append('<div class="section"><h2>Section I · Multiple choice · 90 minutes</h2><ol class="mc">' + ''.join(mc_html(q, n, key) for n, (u, q) in enumerate(mcs, 1)) + '</ol></div>')
    P += [frq_html(q, n, key) for n, q in enumerate(frqs, 1)]
    if not key:
        P.append('<div class="section">' + tables_html(False) + '</div>')
    P.append(f'<p class="foot">Mr. K’s Classroom · {title}{" · Teacher key" if key else ""}. Items come from the Statistics question banks, whose answer keys are recomputed in CI (verify_keys.py).</p>')
    P.append('</body></html>')
    return ''.join(P)


def main():
    banks = lib.load()
    import json, subprocess
    js = ('const fs=require("fs"),vm=require("vm");const g={window:{}};for(const p of ["data.js","course-catalog.js"])vm.runInNewContext(fs.readFileSync(p,"utf8"),g);'
          'const C=g.window.MK_COURSE_CATALOG,o={};for(const u of %s)for(const s of C.getSkillRecords("statistics",u))o[s.id]=s.name;console.log(JSON.stringify(o))') % json.dumps(lib.UNITS)
    names = json.loads(subprocess.run(['node', '-e', js], cwd=lib.ROOT, capture_output=True, text=True, check=True).stdout)
    byid = {q['id']: q for _, q in lib.items(banks)}
    mcs = pick_mc(banks)
    ids_a, ids_b = {q['id'] for _, q in mcs['a']}, {q['id'] for _, q in mcs['b']}
    assert not ids_a & ids_b and len(ids_a) == len(ids_b) == 42
    for ex in ('a', 'b'):
        frqs = [byid[i] for i in FRQ[ex]]
        out = os.path.join(lib.ROOT, 'artifacts', f'statistics-ap-practice-exam-{ex}')
        os.makedirs(out, exist_ok=True)
        for key in (False, True):
            open(os.path.join(out, 'key.html' if key else 'exam.html'), 'w', encoding='utf-8').write(exam_page(ex, mcs[ex], frqs, names, key))
    out = os.path.join(lib.ROOT, 'artifacts', 'statistics-tables-formulas')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(tables_html(True))
    json.dump({ex: [q['id'] for _, q in mcs[ex]] + FRQ[ex] for ex in mcs}, open(os.path.join(os.path.dirname(__file__), 'exams.json'), 'w'), indent=1)
    print('exams: 42 MC + 4 FRQ each; tables and formula sheet written')


if __name__ == '__main__':
    main()
