"""Calculus audit #17 (2026-11-18): two AP Calculus AB-style practice exams.

Each exam follows the AB exam layout:
  Section I  Part A  30 multiple choice, no calculator, 60 minutes
             Part B  15 multiple choice, graphing calculator required for some, 45 minutes
  Section II Part A   2 free response, graphing calculator, 30 minutes
             Part B   4 free response, no calculator, 60 minutes
Part A multiple choice and every free-response problem come from the published Calculus banks (CP1 and Honors items;
no item appears in both exams). Part B uses the bank's calculator-active multiple-choice items and adds
calculator-active items written here, whose answers and wrong options are computed numerically with sympy.
Writes artifacts/calculus-ap-practice-exam-{a,b}/exam.html and key.html; print_exams.cjs turns them into PDFs.
Deterministic: rerunning gives the same exams. Usage (repository root): python3 tools/calculus-audit-20261118/exams.py
"""
import html, json, os, random, re, sys
import sympy as sp
sys.path.insert(0, os.path.dirname(__file__))
import lib

x, t = sp.symbols('x t')
QUOTA = [('limits-continuity', 3), ('derivatives', 6), ('applications-derivatives', 7), ('antiderivatives-definite-integrals', 4),
         ('fundamental-theorem-calculus', 4), ('applications-integrals', 3), ('differential-equations', 3)]
FRQ = {'a': (['cal-aoi-s02-honors-015', 'cal-aoi-s05-honors-015'], ['cal-ftc-s02-honors-015', 'cal-app-s05-honors-015', 'cal-deq-s04-honors-015', 'cal-app-s06-honors-015']),
       'b': (['cal-apr-s05-honors-015', 'cal-aoi-s07-honors-015'], ['cal-apr-s03-honors-015', 'cal-der-s07-honors-015', 'cal-apr-s04-honors-015', 'cal-der-s09-honors-015'])}
UNIT_NAME = {'limits-continuity': 'Limits and Continuity', 'derivatives': 'Derivatives', 'applications-derivatives': 'Applications of Derivatives',
             'antiderivatives-definite-integrals': 'Antiderivatives and Definite Integrals', 'fundamental-theorem-calculus': 'Fundamental Theorem of Calculus',
             'applications-integrals': 'Applications of Integrals', 'differential-equations': 'Differential Equations', 'ap-review': 'AP Review', 'precalculus-review': 'Precalculus Review'}


def d3(v):
    return f'{float(v):.3f}'


# ---------------------------------------------------------------- calculator-active multiple choice written here
def c_integral(rng):
    f, fs, a, b = rng.choice([(sp.exp(-x ** 2), 'e^(−x²)', 0, 2), (sp.sin(x ** 2), 'sin(x²)', 0, 2), (sp.sqrt(1 + x ** 3), '√(1 + x³)', 0, 2),
                              (sp.cos(sp.sqrt(x)), 'cos(√x)', 0, 3), (sp.log(1 + x ** 2), 'ln(1 + x²)', 1, 3), (1 / (1 + x ** 4), '1/(1 + x⁴)', 0, 2)])
    val = sp.Integral(f, (x, a, b)).evalf(12)
    dis = [f.subs(x, b) - f.subs(x, a), (b - a) * f.subs(x, b), sp.Integral(f, (x, a, b + 1)).evalf(12)]  # F confused with f, one right rectangle, wrong upper limit
    return (f'What is the value of ∫ from {a} to {b} {fs} dx?', d3(val), [d3(v.evalf()) for v in dis],
            [f'{fs} has no elementary antiderivative: use the calculator’s numerical integration.', f'∫ from {a} to {b} {fs} dx ≈ {d3(val)}.'])


def c_distance(rng):
    v, vs, T = rng.choice([(t * sp.cos(t), 't·cos(t)', 3), (sp.exp(t / 2) * sp.sin(t) - 1, 'e^(t/2)·sin(t) − 1', 4), (t ** 2 - 2 * sp.sqrt(t + 1) - 1, 't² − 2√(t + 1) − 1', 3),
                           (2 * sp.sin(t ** 2), '2sin(t²)', 2.5)])
    T = sp.nsimplify(T)
    dist = sp.Integral(sp.Abs(v), (t, 0, T)).evalf(12)
    disp = sp.Integral(v, (t, 0, T)).evalf(12)
    return (f'A particle moves along a line with velocity v(t) = {vs} for 0 ≤ t ≤ {T}. What is the total distance the particle travels in that time?',
            d3(dist), [d3(disp), d3(v.subs(t, T).evalf()), d3(dist / T)],
            ['Total distance = ∫ from 0 to ' + str(T) + ' |v(t)| dt (enter the absolute value in the calculator).', f'≈ {d3(dist)}. (The displacement ∫ v dt ≈ {d3(disp)} is a different quantity.)'])


def c_average(rng):
    f, fs, a, b = rng.choice([(sp.sqrt(x) * sp.cos(x), '√x·cos(x)', 0, 2), (x * sp.exp(-x / 2), 'x·e^(−x/2)', 0, 5), (sp.log(x) ** 2, '(ln x)²', 1, 4), (sp.atan(x), 'arctan(x)', 0, 3)])
    I = sp.Integral(f, (x, a, b)).evalf(12)
    return (f'What is the average value of f(x) = {fs} on the interval [{a}, {b}]?', d3(I / (b - a)), [d3(I), d3((f.subs(x, a) + f.subs(x, b)).evalf() / 2), d3(f.subs(x, sp.Rational(a + b, 2)).evalf())],
            [f'Average value = (1/({b} − {a}))∫ from {a} to {b} f(x) dx.', f'= {d3(I)}/{b - a} ≈ {d3(I / (b - a))}.'])


def c_mvt(rng):
    f, fs, a, b = rng.choice([(sp.exp(x) - 3 * x, 'eˣ − 3x', 0, 2), (x ** 3 - 2 * x + sp.sin(x), 'x³ − 2x + sin(x)', 0, 2), (sp.log(x + 1) * x, 'x·ln(x + 1)', 0, 3), (sp.sqrt(x) + x ** 2 / 4, '√x + x²/4', 1, 4)])
    m = (f.subs(x, b) - f.subs(x, a)) / (b - a)
    c = sp.nsolve(sp.diff(f, x) - m, x, (a + b) / 2)
    assert a < c < b
    return (f'f(x) = {fs}. For what value of c in ({a}, {b}) does f′(c) equal the average rate of change of f on [{a}, {b}]?', d3(c),
            [d3(sp.Rational(a + b, 2)), d3(m.evalf()), d3(b - (c - a))],
            [f'Average rate of change: (f({b}) − f({a}))/({b} − {a}) ≈ {d3(m.evalf())}.', f'Solve f′(c) = {d3(m.evalf())} with the calculator: c ≈ {d3(c)}.'])


def c_area(rng):
    f, fs, g, gs = rng.choice([(sp.cos(x), 'cos(x)', x ** 2, 'x²'), (sp.exp(-x ** 2), 'e^(−x²)', x ** 2 - 1, 'x² − 1'), (4 - x ** 2, '4 − x²', sp.exp(x) - 1, 'eˣ − 1'), (2 * sp.cos(x), '2cos(x)', x ** 2 - 1, 'x² − 1'), (sp.sqrt(x + 3), '√(x + 3)', x ** 2 - 1, 'x² − 1')])
    rs = []
    for s0 in (-2.5, -1.5, -0.7, 0.7, 1.5, 2.5):
        try:
            r = float(sp.nsolve(f - g, x, s0))
            if all(abs(r - q) > 1e-6 for q in rs):
                rs.append(r)
        except Exception:
            pass
    rs.sort()
    a, b = rs[0], rs[-1]
    A = sp.Integral(f - g, (x, a, b)).evalf(12)
    return (f'What is the area of the region enclosed by the graphs of y = {fs} and y = {gs}?', d3(A),
            [d3(sp.Integral(f, (x, a, b)).evalf(12)), d3(A / 2), d3(sp.Integral(f + g, (x, a, b)).evalf(12))],
            [f'The curves meet at x ≈ {a:.3f} and x ≈ {b:.3f} (calculator intersect).', f'Area = ∫ from {a:.3f} to {b:.3f} [{fs} − ({gs})] dx ≈ {d3(A)}.'])


def c_accum(rng):
    r, rs, A0, T, unit = rng.choice([(20 + 15 * sp.sin(t / 2), '20 + 15sin(t/2)', 100, 6, 'gallons'), (50 * sp.exp(-t / 4), '50e^(−t/4)', 30, 5, 'people'), (8 + t * sp.cos(t), '8 + t·cos(t)', 40, 4, 'cubic feet'), (12 * sp.sqrt(t) * sp.exp(-t / 3), '12√t·e^(−t/3)', 25, 5, 'liters'), (30 + 10 * sp.cos(t ** 2 / 4), '30 + 10cos(t²/4)', 60, 3, 'gallons')])
    I = sp.Integral(r, (t, 0, T)).evalf(12)
    return (f'Material enters a container at a rate of r(t) = {rs} {unit} per hour, with t in hours. At t = 0 the container holds {A0} {unit}. To the nearest thousandth, how many {unit} does it hold at t = {T}?',
            d3(A0 + I), [d3(I), d3(A0 + r.subs(t, T).evalf()), d3(A0 + T * r.subs(t, 0))],
            [f'Amount = {A0} + ∫ from 0 to {T} r(t) dt.', f'∫ from 0 to {T} r(t) dt ≈ {d3(I)}, so the amount ≈ {d3(A0 + I)} {unit}.'])


def c_deriv(rng):
    f, fs, a = rng.choice([(x ** x, 'xˣ', 2), (sp.sin(x) ** 2 * sp.exp(x / 3), 'sin²(x)·e^(x/3)', 1), (sp.log(x ** 2 + 1) / x, 'ln(x² + 1)/x', 2), (sp.sqrt(x) * sp.atan(x), '√x·arctan(x)', 3)])
    d = sp.diff(f, x).subs(x, a).evalf(12)
    return (f'f(x) = {fs}. What is f′({a})?', d3(d), [d3(f.subs(x, a).evalf()), d3(sp.diff(f, x, 2).subs(x, a).evalf()), d3(((f.subs(x, a + 1) - f.subs(x, a))).evalf())],
            [f'Use the calculator’s numerical derivative at x = {a}.', f'f′({a}) ≈ {d3(d)}.'])


CALC = [c_integral, c_distance, c_average, c_mvt, c_area, c_accum, c_deriv]


def mc_from(prompt, ans, dis, rng):
    opts = [ans] + [d for d in dict.fromkeys(dis) if d != ans]
    pad = 1
    while len(opts) < 4:
        cand = d3(float(ans) + pad * 0.5 * (1 if pad % 2 else -1)); pad += 1
        if cand not in opts:
            opts.append(cand)
    opts = opts[:4]
    vals = [float(o) for o in opts]
    assert all(abs(p - q) > 0.0015 for i, p in enumerate(vals) for q in vals[i + 1:]), (prompt, opts)
    rng.shuffle(opts)
    return [{'text': o, 'correct': o == ans} for o in opts]


def build():
    banks = lib.load()
    tags = lib.tags()
    calc_ids = {i for u in tags for i, v in tags[u].items() if 'calculator-active' in v}
    names = json.loads(os.popen("node -e \"require('./course-catalog.js');const C=globalThis.MK_COURSE_CATALOG,o={};for(const u of require('./question-banks/manifest.json').banks.filter(b=>b.courseId==='calculus'))C.getSkillRecords('calculus',u.unitId).forEach(s=>o[s.id]=s.name);console.log(JSON.stringify(o))\"").read())
    allq = {q['id']: (u, q) for u, d in banks.items() for q in d['questions']}
    used = set()
    exams = {}
    for ex in 'ab':
        rng = random.Random('cal-audit-17-' + ex)
        partA = []
        for u, n in QUOTA:
            pool = [q for q in banks[u]['questions'] if q['format'] == 'multiple-choice' and q['level'] in ('cp1', 'honors') and q['id'] not in calc_ids and q['id'] not in used
                    and not re.search(r'Round|calculator|Hint:', q['prompt'])]
            skills = sorted({q['skillId'] for q in pool})
            rng.shuffle(skills)
            picks = []
            for s in (skills * 3):
                if len(picks) == n:
                    break
                cand = [q for q in pool if q['skillId'] == s and q not in picks and q['prompt'] not in {p['prompt'] for p in picks}]
                if cand:
                    picks.append(rng.choice(cand))
            used.update(q['id'] for q in picks)
            partA += [(u, q) for q in picks]
        bank_calc = sorted(i for i in calc_ids if i in allq and allq[i][1]['format'] == 'multiple-choice')
        fams, half = set(), []
        for i in bank_calc:  # at most two bank calculator items per exam, from different families
            fam = lib.family(allq[i][1])
            if i not in used and fam not in fams and len(half) < 2:
                fams.add(fam); half.append(i)
        partB = [allq[i] for i in half]
        used.update(half)
        k = 0
        seen = set()
        while len(partB) < 15:
            fn = CALC[k % len(CALC)]; k += 1
            for attempt in range(30):
                p, ans, dis, steps = fn(random.Random(f'cal-audit-17-{ex}-{k}-{attempt}'))
                if p not in seen and p not in exams.get('a', {}).get('prompts', set()):
                    break
            else:
                continue  # every version of this template is used: try the next one
            seen.add(p)
            q = {'id': f'cal-exam-{ex}-calc-{len(partB) + 1:02d}', 'skillId': None, 'prompt': p, 'answer': ans, 'options': mc_from(p, ans, dis, rng), 'solutionSteps': steps, 'standards': []}
            partB.append(('calculator', q))
        rng.shuffle(partA)
        fa, fb = FRQ[ex]
        exams[ex] = {'A': partA, 'B': partB, 'FA': [allq[i] for i in fa], 'FB': [allq[i] for i in fb], 'prompts': seen}
    return exams, names


# ---------------------------------------------------------------- HTML
CSS = '''
@page { size: letter; margin: 0.55in 0.6in; }
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
img.dg { max-width: 330px; max-height: 210px; display: block; margin: 5px 0; }
.frq { break-before: page; } .frq .q { margin-bottom: 6px; } .part { break-inside: avoid; margin: 10px 0 0; } .work { height: 1.45in; border-bottom: 1px dashed #9aa0c8; }
.ans { color: #c8102e; font-weight: 700; } .steps { margin: 3px 0 0 18px; padding: 0; color: #2b2f55; } .steps li { margin-bottom: 2px; }
.foot { font-size: 8.5pt; color: #4a4f78; margin-top: 10px; }
.cover li { margin-bottom: 4px; }
'''


def esc(s):
    return html.escape(str(s), quote=False)


def img(q):
    d = q.get('diagram') or {}
    s = (d.get('spec') or {}).get('src')
    return f'<img class="dg" src="../../{esc(s)}" alt="{esc(d["spec"].get("alt", ""))}">' if s else ''


def mc_html(q, n, key=False, names=None):
    letters = 'ABCD'
    ch = ''.join(f'<div><b>({letters[i]})</b><span class="choices-t">{esc(o["text"])}</span></div>' for i, o in enumerate(q['options']))
    out = f'<li value="{n}"><div class="q">{esc(q["prompt"])}</div>{img(q)}<div class="choices">{ch}</div>'
    if key:
        right = letters[[o['correct'] for o in q['options']].index(True)]
        out += f'<div class="ans">Answer: ({right}) {esc(q["answer"])}</div><ol class="steps solution">' + ''.join(f'<li>{esc(s)}</li>' for s in q['solutionSteps']) + '</ol>'
    return out + '</li>'


def frq_html(q, n, key=False, head=''):
    stem = q['prompt'].split('). ', 1)[1] if q['prompt'].startswith('Free response') else q['prompt']
    out = f'<div class="frq">{head}<h3>Question {n}</h3><div class="q">{esc(stem)}</div>{img(q)}'
    steps = q['solutionSteps']
    for p in q['parts']:
        out += f'<div class="part"><div class="q"><b>({p["label"]})</b> {esc(p["prompt"])}</div>'
        if key:
            mine = [s for s in steps if s.startswith(f'({p["label"]})')]
            out += f'<div class="ans">{esc(p["answer"])}</div><ol class="steps solution">' + ''.join(f'<li>{esc(s[4:])}</li>' for s in mine) + '</ol>'
        else:
            out += '<div class="work"></div>'
        out += '</div>'
    if key:
        out += f'<p class="ans">{esc(steps[-1])}</p>'
    return out + '</div>'


def page(ex, E, names, key):
    title = f'AP Calculus AB Practice Exam {ex.upper()}'
    fr_pts = [int(re.search(r'Total: (\d+)', q['solutionSteps'][-1]).group(1)) for _, q in E['FA'] + E['FB']]
    P = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}{" · Teacher key" if key else ""}</title><style>{CSS}</style></head><body>']
    P.append(f'<div class="cover"><div class="eyebrow">Calculus · AP Review</div><h1>{title}{" — Teacher Key and Scoring Guide" if key else ""}</h1>')
    if not key:
        P.append('<div class="name"><span>Name</span><span>Date</span><span>Period</span></div>')
    P.append('<table><tr><th>Section</th><th>Part</th><th>Questions</th><th>Time</th><th>Calculator</th><th>Weight</th></tr>'
             '<tr><td rowspan="2">I · Multiple choice</td><td>A</td><td>30 (1–30)</td><td>60 minutes</td><td>Not allowed</td><td rowspan="2">50%</td></tr>'
             '<tr><td>B</td><td>15 (31–45)</td><td>45 minutes</td><td>Graphing calculator required for some questions</td></tr>'
             '<tr><td rowspan="2">II · Free response</td><td>A</td><td>2 (1–2)</td><td>30 minutes</td><td>Graphing calculator required for some parts</td><td rowspan="2">50%</td></tr>'
             f'<tr><td>B</td><td>4 (3–6)</td><td>60 minutes</td><td>Not allowed</td></tr></table>')
    P.append('<div class="box"><b>Timing notes.</b> The whole exam takes 3 hours 15 minutes. To give it over two class periods, do Section I '
             '(105 minutes, with a short break between Part A and Part B) one day and Section II (90 minutes) the next. In Section II, students may keep '
             'working on Part A questions during Part B, but without a calculator. A calculator answer should be correct to three decimal places unless the question says otherwise.</div>')
    if not key:
        P.append('<ul><li>Multiple choice: circle one answer. There is no penalty for guessing.</li><li>Free response: show all your work. Justify answers with '
                 'calculus, not only calculator results, and give units where the question has a context.</li><li>Unless a question says otherwise, the domain of a function '
                 'is all real numbers for which it is defined.</li></ul>')
    else:
        mcpts = 45
        P.append('<div class="box"><b>Scoring guide.</b> Section I: 1 point for each correct answer (45 points). Section II: score each part with the notes below '
                 f'({", ".join(str(p) for p in fr_pts)} points; {sum(fr_pts)} in all). To weight the sections equally like the AP exam, compute '
                 f'<b>composite = 1.2 × (multiple-choice points) + {round(54 / sum(fr_pts), 3)} × (free-response points)</b>, out of 108. '
                 'This is a practice estimate, not an official AP score conversion.</div>')
        rows = ''
        for n, (u, q) in enumerate(E['A'] + E['B'], 1):
            right = 'ABCD'[[o['correct'] for o in q['options']].index(True)]
            topic = names.get(q.get('skillId'), 'Calculator-active (written for this exam)') if q.get('skillId') else 'Calculator-active (written for this exam)'
            rows += f'<tr><td>{n}</td><td>{right}</td><td>{esc(UNIT_NAME.get(u, "Calculator-active"))}</td><td>{esc(topic)}</td><td>{esc(", ".join(s.replace("AP ", "") for s in q.get("standards", [])))}</td></tr>'
        P.append('<h2>Multiple-choice answers</h2><table><tr><th>#</th><th>Key</th><th>Unit</th><th>Skill</th><th>AP objectives</th></tr>' + rows + '</table>')
    P.append('</div>')
    P.append('<div class="section"><h2>Section I, Part A · Multiple choice · No calculator · 60 minutes</h2><ol class="mc">' + ''.join(mc_html(q, n, key) for n, (u, q) in enumerate(E['A'], 1)) + '</ol></div>')
    P.append('<div class="section"><h2>Section I, Part B · Multiple choice · Graphing calculator allowed · 45 minutes</h2><ol class="mc">' + ''.join(mc_html(q, n, key) for n, (u, q) in enumerate(E['B'], 31)) + '</ol></div>')
    P += [frq_html(q, n, key, '<h2>Section II, Part A · Free response · Graphing calculator allowed · 30 minutes</h2><p>Answer each part. Show the setup you enter in the calculator.</p>' if n == 1 else '')
          for n, (u, q) in enumerate(E['FA'], 1)]
    P += [frq_html(q, n, key, '<h2>Section II, Part B · Free response · No calculator · 60 minutes</h2><p>Show all your work and justify your answers.</p>' if n == 3 else '')
          for n, (u, q) in enumerate(E['FB'], 3)]
    P.append(f'<p class="foot">Mr. K’s Classroom · {title}{" · Teacher key" if key else ""}. Items come from the Calculus question banks; calculator questions 31–45 were checked numerically.</p>')
    P.append('<script src="../../worksheet-generator/core/math-display.js?v=g8-audit-20261119"></script></body></html>')
    return ''.join(P)


def main():
    exams, names = build()
    for ex, E in exams.items():
        out = os.path.join(lib.ROOT, 'artifacts', f'calculus-ap-practice-exam-{ex}')
        os.makedirs(out, exist_ok=True)
        for key in (False, True):
            open(os.path.join(out, 'key.html' if key else 'exam.html'), 'w', encoding='utf-8').write(page(ex, E, names, key))
        print(ex, len(E['A']), len(E['B']), len(E['FA']), len(E['FB']))


if __name__ == '__main__':
    main()
