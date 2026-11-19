"""Grade 7 audit G4 (2026-11-19): recompute the keys of the G4 figure items from the figure's alt text and the prompt,
independently of new_items.py. Usage (repository root): python3 tools/grade7-audit-20261119/verify_g4.py"""
import os, re, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(__file__))
import lib

PI = Fr(314, 100)
SIDES = {'triangle': 3, 'quadrilateral': 4, 'pentagon': 5}


def tenth(x):
    q = x * 10
    return str(Fr(int(q + Fr(1, 2)), 10).__float__())


def num(s):
    return Fr(s.replace(',', ''))


def check(q):
    fam = re.search(r'family: (\w+)', q['sourceNotes']).group(1)
    alt, p, a = q.get('diagram', {}).get('spec', {}).get('alt', ''), q['prompt'], q['answer']
    if fam in ('g7_polygon_angle', 'g7_polygon_algebra'):
        name = re.search(r'A (\w+) with', alt).group(1)
        labs = re.search(r'labelled (.*)\. Not drawn', alt).group(1).split(', ')
        total = (SIDES[name] - 2) * 180
        coef = sum(Fr(m.group(1) or 1) for l in labs for m in [re.match(r'(\d*)x', l)] if m)
        const = sum(Fr(re.sub(r'[^\d]', '', l.split('+')[1]) if '+' in l else (l.rstrip('°') if 'x' not in l else 0)) for l in labs)
        x = (total - const) / coef
        if fam == 'g7_polygon_angle':
            return a == f'x = {x}'
        vals = [(Fr(re.match(r'(\d*)x', l).group(1) or 1) * x + (Fr(re.sub(r'[^\d]', '', l.split('+')[1])) if '+' in l else 0)) for l in labs]
        return a == f'{max(vals)}°'
    if fam in ('g7_circle_figure', 'g7_circle_area_figure'):
        kind = re.search(r'A (circle|semicircle|quarter circle)', alt).group(1)
        L = num(re.search(r'(?:labelled|is a radius labelled) (?:[rd] = )?([\d.]+)', alt).group(1))
        r = L / 2 if (kind == 'semicircle' or 'diameter' in alt) else L
        if fam == 'g7_circle_figure':
            if 'second circle' in p:
                v = 3 * 2 * r / 2
                return a.startswith(str(v))
            if '10 full turns' in p:
                v = 2 * PI * r * 10
            elif kind == 'semicircle':
                v = PI * r + 2 * r
            elif kind == 'quarter circle':
                v = 2 * PI * r / 4 + 2 * r
            else:
                v = 2 * PI * r
        else:
            if 'twice this diameter' in p:
                v = PI * (2 * r) ** 2
            elif 'square with this semicircle' in p:
                v = PI * r * r / 2 + (2 * r) ** 2
            elif kind == 'semicircle':
                v = PI * r * r / 2
            elif kind == 'quarter circle':
                v = PI * r * r / 4
            else:
                v = PI * r * r
        got = num(a.split()[0])
        return abs(got - v) <= Fr(5, 100) and (('nearest tenth' not in p) or re.fullmatch(r'[\d,]+\.\d', a.split()[0]))
    if fam == 'g7_scale_drawing_figure':
        m = re.search(r': ([\d.]+) (in|cm)\.? long and ([\d.]+) (?:in|cm)\.? wide on the drawing\. Scale: 1 (?:in|cm)\.? : ([\d.]+) (ft|m)', alt)
        L, W, k = num(m.group(1)), num(m.group(3)), num(m.group(4))
        if 'area' in p:
            want = L * k * W * k
        elif 'perimeter' in p:
            want = 2 * (L + W) * k
        elif 'redrawn' in p:
            new = num(re.search(r': ([\d.]+) ft\. How', p.replace('1 in. : ', ': ')).group(1))
            want = L * k / new
        elif 'shorter side' in p:
            want = min(L, W) * k
        else:
            want = L * k
        return num(a.split()[0]) == want
    if fam == 'g7_dot_plot_compare':
        A = [int(x) for x in re.search(r'Class A: ([\d, ]+)\.', alt).group(1).split(', ')]
        B = [int(x) for x in re.search(r'Class B: ([\d, ]+)\.', alt).group(1).split(', ')]
        mean = lambda d: Fr(sum(d), len(d))
        med = lambda d: Fr(sorted(d)[len(d) // 2 - 1] + sorted(d)[len(d) // 2], 2)
        mad = lambda d: sum(abs(x - mean(d)) for x in d) / len(d)
        if 'median' in p:
            return num(a) == med(B) - med(A)
        if 'range' in p:
            ra, rb = max(A) - min(A), max(B) - min(B)
            return a == f'Class {"B" if rb > ra else "A"}, by {abs(rb - ra)}'
        if 'greater mean absolute deviation' in p:
            return a == f'Class {"B" if mad(B) > mad(A) else "A"}; MAD A = {float(mad(A)):g}, MAD B = {float(mad(B)):g}'
        if 'how many MADs' in p or 'multiple of the MAD' in p:
            k = (mean(B) - mean(A)) / mad(A)
            return a.split()[0] == f'{float(k):g}' and mad(A) == mad(B)
        return num(a) == mean(B) - mean(A)
    if fam in ('g7_congruent_marks', 'g7_congruent_algebra', 'g7_congruent_perimeter'):
        if q['format'] == 'multiple-choice':
            return 'BC' in p and a == 'EF'
        lab = re.search(r'Labels: (.*?)\.(?: Angles|$)', alt); ang = re.search(r'Angles: (.*)\.$', alt)
        sides = {k: v for v, k in (x.rsplit(' on side ', 1) for x in lab.group(1).split('; '))} if lab else {}
        angs = {k: v for v, k in (x.rsplit(' at ', 1) for x in ang.group(1).split('; '))} if ang else {}
        if 'How long is DE' in p:
            return a == sides['AB']
        if '∠E' in p:
            return a == angs['B']
        if 'perimeter' in p:
            return a == f'{num(sides["AB"].split()[0]) + num(sides["BC"].split()[0]) + num(sides["FD"].split()[0])} cm'
        if 'measure of ∠C' in p:
            m = re.match(r'\((\d+)x \+ (\d+)\)°', angs['A']); x = (num(angs['D'].rstrip('°')) - int(m.group(2))) / int(m.group(1))
            return a == f'x = {x}; m∠C = {180 - num(angs["D"].rstrip("°")) - num(angs["E"].rstrip("°"))}°'
        m = re.match(r'(\d+)x \+ (\d+)', sides['CA']); x = (num(sides['FD']) - int(m.group(2))) / int(m.group(1))
        return a == f'x = {x}'
    if fam in ('g7_rewrite_meaning', 'g7_rewrite_percent'):
        ok = [o for o in q['options'] if o['correct']]
        if len(ok) != 1 or ok[0]['text'] != a:
            return False
        if fam == 'g7_rewrite_percent':
            pct = int(re.search(r'(\d+)% (?:discount|markup)', p).group(1))
            f = 100 - pct if 'discount' in p else 100 + pct
            return a == f'{f / 100:g}p, so {f}% of p'
        return True
    raise SystemExit('no check for ' + fam)


def main():
    n = bad = 0
    for _, q in lib.items(lib.load()):
        if not re.search(r'family: g7_(polygon|circle|scale_drawing_figure|dot_plot|congruent|rewrite)', q.get('sourceNotes', '')):
            continue
        n += 1
        if not check(q):
            bad += 1
            print('MISMATCH', q['id'], q['prompt'][:80], '→', q['answer'])
    print(('FAIL' if bad else 'PASS'), f'{n} G4 keys recomputed from the figures and prompts ({bad} mismatches)')
    sys.exit(1 if bad or n < 45 else 0)


if __name__ == '__main__':
    main()
