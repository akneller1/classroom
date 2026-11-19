"""Statistics audit #12, #13 and #19 (2026-11-18). Idempotent text fixes.
#13: symbols capitalized at the start of a prompt (Σ for σ, X̄ for x̄, Ŷ, Z, P₀, B for b); "(4 dp)" shorthand;
     ^n exponents in solutions; "P-value" and "p-value" both used (now "p-value", as in the AP framework).
#12: six items whose keys come from technology (normalcdf) although the bank's convention is Table A say so in the
     prompt, and their steps no longer pair a rounded z with the unrounded probability.
#19: confidence-interval simulation items explain the count of captures instead of a fixed sentence."""
import math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib
from scipy import stats

WORD = {'1': 'one', '2': 'two', '3': 'three', '4': 'four'}
SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
CAPS = [('T* ', 't* '), ('P̂ = ', 'p̂ = '), ('D̄ = ', 'd̄ = '), ('S = ', 's = '), ('Σ = ', 'σ = '), ('X̄ = ', 'x̄ = '), ('Ŷ = ', 'ŷ = '), ('Z = ', 'z = '), ('P₀ = ', 'p₀ = '), ('B = ', 'b = ')]


def dp(s):
    s = re.sub(r' \(z to (\d) dp; (\d) dp\)\.?', lambda m: f'. Round z to {WORD[m.group(1)]} decimal places and the answer to {WORD[m.group(2)]}.', s)
    def r(m):
        end = m.group(2) or ''
        return (end if end else '') + f' Round to {WORD[m.group(1)]} decimal places.'
    s = re.sub(r' \((\d) dp\)([.?])?', r, s)
    s = re.sub(r'([.?])\. Round', r'\1 Round', s)
    return s


def pval(s):
    return re.sub(r'\bP-value', 'p-value', s)


def caret(s):
    return re.sub(r'\^(\d+)', lambda m: m.group(1).translate(SUP), s)


def walk(q, f):
    q['prompt'] = f(q['prompt'])
    if isinstance(q['answer'], str):
        q['answer'] = f(q['answer'])
    elif isinstance(q['answer'], list):
        q['answer'] = [f(a) for a in q['answer']]
    q['solutionSteps'] = [f(s) for s in q['solutionSteps']]
    for o in q.get('options', []):
        o['text'] = f(o['text'])
    for p in q.get('parts', []):
        p['prompt'] = f(p['prompt']); p['answer'] = f(p['answer'])


TECH = {
 'stat-u3-t3-012': (r'z = \(0\.5 − 0\.45\)/0\.0497 ≈ 1\.01; probability ≈ 0\.1574\.', 'z = (0.50 − 0.45)/0.0497 ≈ 1.005; normalcdf gives P(p̂ > 0.50) ≈ 0.1574. (Table A with z rounded to 1.01 gives 0.1562.)'),
 'stat-u3-t3-013': (r'z = \(0\.25 − 0\.3\)/0\.0290 ≈ -1\.73; probability ≈ 0\.0422\.', 'z = (0.25 − 0.30)/0.0290 ≈ −1.725; normalcdf gives P(p̂ < 0.25) ≈ 0.0422. (Table A with z rounded to −1.73 gives 0.0418.)'),
 'stat-u3-t3-014': (r'z = ±1\.65; probability ≈ 0\.9007\.', 'z = ±0.04/0.0243 ≈ ±1.648; normalcdf gives P(0.58 < p̂ < 0.66) ≈ 0.9007. (Table A with z rounded to ±1.65 gives 0.9011.)'),
 'stat-u3-t3-018': (r'^Probability ≈ 0\.8640\.$', 'z = (500.5 − 502)/0.8 = −1.875 and z = (503.0 − 502)/0.8 = 1.25; normalcdf gives ≈ 0.8640. (Table A with z rounded to −1.88 and 1.25 gives 0.8643.)'),
 'stat-u4-t2-014': (r'^p-value = P\(Z ≥ 2\.68\) ≈ 0\.0036\.$', 'p-value = P(Z ≥ 2.683) ≈ 0.0036 with normalcdf. (Table A with z rounded to 2.68 gives 0.0037.)'),
 'stat-u4-t2-016': (r'^p-value = 2P\(Z ≥ 1\.67\) ≈ 0\.0944\.$', 'p-value = 2P(Z ≥ 1.672) ≈ 0.0944 with normalcdf. (Table A with z rounded to 1.67 gives 0.0949.)'),
}


def capture(q):
    s = ' '.join(q['solutionSteps'])
    m = re.search(r'(\d+)/(\d+) = (\d+)%, close to the (\d+)% confidence level, as expected over many samples\.', s)
    if not m:
        return
    k, n, C = int(m.group(1)), int(m.group(2)), int(m.group(4)) / 100
    B = stats.binom(n, C)
    lo, hi = int(B.ppf(0.025)), int(B.ppf(0.975))
    exp = C * n
    verdict = (f'{k} is within the range chance usually gives ({lo} to {hi} of {n}), so the result is consistent with a {round(C * 100)}% method.'
               if lo <= k <= hi else
               f'{k} is outside the range chance usually gives ({lo} to {hi} of {n}), so this result would be unusual for a {round(C * 100)}% method.')
    new = (f'{k}/{n} = {round(100 * k / n)}% captured p. A {round(C * 100)}% method captures p about {round(C * 100)}% of the time in the long run, so we expect about '
           f'{exp:g} of {n} intervals to capture it; with only {n} intervals the count varies by chance. {verdict}')
    q['solutionSteps'] = [new if m.group(0) in st else st for st in q['solutionSteps']]


def main():
    banks = lib.load()
    for u, q in lib.items(banks):
        for a, b in CAPS:
            if q['prompt'].startswith(a):
                q['prompt'] = b + q['prompt'][len(a):]
        walk(q, dp)
        walk(q, pval)
        q['solutionSteps'] = [caret(s) for s in q['solutionSteps']]
        if q['id'] in TECH:
            if 'Use technology (normalcdf)' not in q['prompt']:
                q['prompt'] = q['prompt'].replace(' Round to four decimal places.', ' Use technology (normalcdf). Round to four decimal places.')
            pat, rep = TECH[q['id']]
            q['solutionSteps'] = [re.sub(pat, rep, st) for st in q['solutionSteps']]
            assert any(rep in st for st in q['solutionSteps']), q['id']
        capture(q)
    lib.save(banks)


if __name__ == '__main__':
    main()
