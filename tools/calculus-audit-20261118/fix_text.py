"""Calculus audit #13 and #19 (2026-11-18): notation clean-up, IVT wording and units for motion questions.

#13: no written coefficient 1 ("1y", "e^(-1x)", "(1k/n)", "1f(x)"); fraction coefficients in parentheses
     ("(507/50)e^(0.02t)"); no "+ -" or "- -"; "x" for the factor "(x - 0)"; cosⁿ(x) rather than cos(x)ⁿ;
     √(36 - x²); no "quadrant none" in exact-value steps.
#19: IVT counting questions ask how many solutions the theorem guarantees, and a zero count says the theorem
     guarantees none; motion questions give units for s and t, and velocity and acceleration keys carry units.
Every string field of every item (prompt, answer, steps, parts, options) is rewritten. Idempotent.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import lib

SUPS = '²³⁴⁵⁶⁷⁸⁹'


def notation(s):
    # written coefficient 1 before a letter: 1y, -1x, 1k/n, 1f(x), e^(1x)
    s = re.sub(r'(?<![\d.\w/)⁰-⁹^′″])(-?)1(?=[a-zA-Z])(?!n\))', r'\1', s)
    s = re.sub(r'e\^\((-?)x\)', lambda m: 'e^(-x)' if m.group(1) else 'e^x', s)
    s = s.replace('/(x).', '/x.').replace('/(x))', '/x)').replace('/(x) ', '/x ').replace('/(x)\n', '/x\n')
    s = re.sub(r'/\(x\)$', '/x', s)
    # fraction coefficient: 507/50e^(0.02t) -> (507/50)e^(0.02t); 5/2t² -> (5/2)t²
    s = re.sub(r'(?<![\w)(/.√])(\d+)/(\d+)(?=[a-zA-Z(])', r'(\1/\2)', s)
    # "+ -3" -> "+ (-3)", "x + -2" -> "x - 2", "- -4" -> "- (-4)"
    s = re.sub(r'([a-z]) \+ -(?=\d)', r'\1 - ', s)
    s = re.sub(r'\b(sin|cos|tan)\(\((x [+-] \d+)\)\)', r'\1(\2)', s)
    s = re.sub(r' \+ -(\d+(?:\.\d+)?)(?=[ )\].,;]|$)', r' + (-\1)', s)
    s = re.sub(r' \+ -(?=[a-zA-Z(\d])', ' - ', s)
    s = re.sub(r' - -(\d+(?:/\d+)?(?:\.\d+)?)', r' - (-\1)', s)
    s = re.sub(r'\((x [+-] )-(\d+/\d+)\)', lambda m: '(x ' + ('+' if m.group(1).strip().endswith('-') else '-') + ' ' + m.group(2) + ')', s)
    s = re.sub(r'\(x - \(-(\d+(?:/\d+)?)\)\)', r'(x + \1)', s)
    s = re.sub(r'\(x \+ \(-(\d+(?:/\d+)?)\)\)', r'(x - \1)', s)
    s = s.replace('common factor is (x - 0)', 'common factor is x').replace('common factor is (x + 0)', 'common factor is x')
    # trig powers: cos(x)⁵ -> cos⁵(x)
    s = re.sub(r'\b(sin|cos|tan|sec|csc|cot)\(x\)([' + SUPS + '])', r'\1\2(x)', s)
    s = s.replace('are squares with a side (diameter) in the base', 'are squares with a side in the base').replace('are semicircles with a side (diameter) in the base', 'are semicircles with a diameter in the base')
    # √(-x² + 36) -> √(36 - x²)
    s = re.sub(r'√\(-x² \+ (\d+)\)', r'√(\1 - x²)', s)
    return s


def quadrant(steps):
    out = []
    for st in steps:
        m = re.match(r'Reference angle:? (.+?); quadrant none \((?:on an )?axis\)\.$', st)
        if m:
            out.append(f'{m.group(1)} lies on an axis, so read the coordinates of its unit-circle point directly (no reference angle or quadrant sign is needed).')
            continue
        st = st.replace('; apply the quadrant sign.', '.')
        out.append(st)
    return out


IVT_Q = re.compile(r'By the Intermediate Value Theorem, what is the least number of solutions of f\(x\) = (\S+) on (\[[^\]]+\])\?')


def ivt(s):
    s = IVT_Q.sub(r'How many solutions of f(x) = \1 on \2 does the Intermediate Value Theorem guarantee?', s)
    s = re.sub(r'At least 0\.', 'So the IVT guarantees no solutions. (f could still equal that value somewhere between the table points; the theorem just does not promise it.)', s)
    s = re.sub(r'At least 1\.', 'So the IVT guarantees at least 1 solution.', s)
    s = re.sub(r'At least (\d+)\.', r'So the IVT guarantees at least \1 solutions.', s)
    return s


MOTION = 'A particle moves along a line with position s(t) = '


def motion(q):
    def fix_prompt(p):
        if 'meters at time t seconds' in p:
            return p
        return re.sub(r'(A particle moves along a line with position s\(t\) = [^.]*?) for t ≥ 0\.', r'\1 meters at time t seconds, for t ≥ 0.', p)

    def unit(p):
        m = re.search(r'Find the (velocity|acceleration) at t = ', p)
        return None if not m else ('m/s' if m.group(1) == 'velocity' else 'm/s²')

    def add(a, un):
        a = a.strip()
        return a + ' ' + un if re.fullmatch(r'-?[\d/.]+', a) else a

    if MOTION in q['prompt']:
        un = unit(q['prompt'])
        q['prompt'] = fix_prompt(q['prompt'])
        if un:
            old = q['answer']
            q['answer'] = add(old, un)
            for o in q.get('options', []):
                o['text'] = add(o['text'], un)
            q['solutionSteps'] = [re.sub(r'^([va]\(\S+\) = -?[\d/.]+)\.$', r'\1 ' + un + '.', s) for s in q['solutionSteps']]
            q['solutionSteps'] = [s.replace(f'The correct answer is {old},', f"The correct answer is {q['answer']},") for s in q['solutionSteps']]
    for p in q.get('parts', []):
        if MOTION in p.get('prompt', ''):
            un = unit(p['prompt'])
            p['prompt'] = fix_prompt(p['prompt'])
            if un:
                p['answer'] = add(p['answer'], un)
    if q.get('parts') and any(MOTION in p.get('prompt', '') for p in q['parts']):
        q['answer'] = '; '.join(f"({p.get('label') or chr(97 + i)}) {p['answer']}" for i, p in enumerate(q['parts']))
    return q


def walk(v, f):
    if isinstance(v, str):
        return f(v)
    if isinstance(v, list):
        return [walk(x, f) for x in v]
    if isinstance(v, dict):
        return {k: (x if k in ('id', 'skillId', 'level', 'format', 'standards', 'sourceNotes', 'diagram') else walk(x, f)) for k, x in v.items()}
    return v


# #18 (2026-11-18): Euler's method is a BC topic; say so wherever it is asked.
def euler_bc(s):
    return s if "(a BC topic)" in s else s.replace("Use Euler's method", "Use Euler's method (a BC topic)")


def fix(q):
    q = walk(q, lambda s: euler_bc(ivt(notation(s))))
    q['solutionSteps'] = quadrant(q['solutionSteps'])
    q = motion(q)
    return q


if __name__ == '__main__':
    banks = lib.load()
    for u, d in banks.items():
        d['questions'] = [fix(q) for q in d['questions']]
    lib.save(banks)

