"""Statistics audit #3 and #6 (2026-11-18): tag every item with learning objectives from the AP Statistics framework
effective fall 2026 (codes APSTATS.<unit>.<topic>.<letter>), replacing the retired 2010 topic-outline codes
(APSTATS.I.A …). Topics the 2026 framework dropped are tagged APSTATS.BEYOND.<name>.
Rules: a default set per skill, refined by what the item asks (keywords in the prompt and answer). Deterministic."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib
from ap2026 import LO, BEYOND

MEAN = re.compile(r'\bμ|x̄|\bmeans?\b|\bt[-\s]?(?:test|interval|procedure|statistic|\*)|\bt =|\bdf\b|paired|degrees of freedom', re.I)
PROP = re.compile(r'\bp̂|\bp₀|\bp =|proportion|\bz[-\s]?(?:test|interval|statistic|\*)|percent', re.I)


def T(q):
    return (q['prompt'] + ' ' + lib.key_text(q) + ' ' + ' '.join(p.get('prompt', '') for p in q.get('parts', []))).lower()


def mean_or_prop(t, mean, prop):
    m, p = bool(MEAN.search(t)), bool(PROP.search(t))
    return mean if m and not p else prop if p and not m else (mean if t.count('mean') > t.count('proportion') else prop)


def tag(u, k, q):
    t = T(q)
    has = lambda *ws: any(re.search(w, t) for w in ws)
    if u == 'exploring-data':
        if k == 1:
            if has(r'categorical|quantitative|variable|discrete|continuous'):
                return ['1.2.B', '1.2.C']
            if has(r'bar (graph|chart)|pie'):
                return ['1.4.A', '1.3.B']
            return ['1.5.A', '1.6.A']
        if k == 2:
            return ['1.7.D'] if has(r'outlier|fence') else ['1.6.A', '1.6.B'] if has(r'claim|evidence|justify|support') else ['1.6.A']
        if k == 3:
            if has(r'convert|centimet|°f|inches to|units|each value|added to|multiplied|raise|bonus'):
                return ['1.7.C']
            if has(r'resistant|which measure|better describ|best describ|appropriate measure|skew'):
                return ['1.7.F']
            return ['1.7.B'] if has(r'standard deviation|\bsd\b|range|iqr|variab|spread|sₓ|variance') else ['1.7.A']
        if k == 4:
            if has(r'outlier|fence'):
                return ['1.7.D']
            if has(r'compar|both|two (classes|groups|boxplots|box plots)|parallel'):
                return ['1.9.B', '1.9.C'] if has(r'claim|evidence|justify|which statement') else ['1.9.B']
            if has(r'box ?plot|five-number'):
                return ['1.8.A', '1.8.B']
            return ['1.7.A']
        if k == 5:
            if has(r'z-?score') and not has(r'proportion|percent|probab|area|shaded'):
                return ['1.9.D', '1.9.E'] if has(r'compar|better|relative|which') else ['1.9.D']
            if has(r'68|95|99\.7|empirical'):
                return ['2.11.C']
            if has(r'percentile|top \d|lowest|highest|boundary|cutoff|what (score|value|height|time|weight)|slowest|fastest'):
                return ['2.11.E']
            if has(r'proportion|probab|percent|area|shaded|between|below|above'):
                return ['2.11.D']
            return ['2.11.A']
        if k == 6:
            return ['2.2.C', '2.1.B'] if has(r'associat|independ|evidence|relationship|claim') else ['2.2.A']
        if k == 7:
            return ['5.2.A'] if has(r'\br\b|correlation') else ['5.1.B']
        if k == 8:
            if has(r'residual'):
                return ['5.4.A']
            if has(r'interpret|meaning|means that|what does') or has(r'r²|coefficient of determination'):
                return ['5.5.B']
            if has(r'predict|ŷ at|estimate the'):
                return ['5.3.A']
            return ['5.5.A']
        if k == 9:
            if has(r'residual plot|pattern|curved|fan'):
                return ['5.4.C']
            if has(r'interpret'):
                return ['5.4.B']
            if has(r'residual'):
                return ['5.4.A']
            if has(r'log|transform|straighten|exponential model|power model'):
                return ['BEYOND.TRANS']
            return ['5.1.B', '5.4.C']
    if u == 'sampling-experimentation':
        return {1: ['1.2.A', '1.10.B'] if has(r'census') else ['1.2.A', '1.1.A'], 2: ['1.11.A', '1.11.B'] if has(r'why|better|appropriate|advantage|justify') else ['1.11.A'],
                3: ['1.12.A'], 4: ['1.10.C', '1.10.D'], 5: ['1.13.A'], 6: ['1.13.A'], 7: ['1.13.B', '1.13.C'] if has(r'why|better|appropriate|advantage|justify') else ['1.13.B'],
                8: ['1.10.E', '1.13.D']}[k]
    if u == 'anticipating-patterns':
        if k == 1:
            return ['2.3.A'] if has(r'simulat|toss|spin|roll|trials') else ['2.4.A']
        if k == 2:
            return ['2.5.A'] if has(r'mutually exclusive|disjoint') else ['2.7.A'] if has(r'\bor\b|union|independ|both|and') else ['2.4.A']
        if k == 3:
            return ['2.6.A', '2.7.A'] if has(r'independ') else ['2.6.A']
        if k == 4:
            return ['2.10.D'] if has(r'binomial') else ['2.3.A']
        if k == 5:
            return ['2.8.A'] if has(r'missing|valid|construct|distribution of') else ['2.9.A'] if has(r'mean|e\(x\)|expected|standard deviation|σ') else ['2.8.A']
        if k == 6:
            if has(r'y = |= \d+x|\d+x\b|x − \d|x \+ \d|linear transformation|bonus|per car|°f|convert|each .* by'):
                return ['BEYOND.LINRV']
            return ['2.9.B'] if has(r'interpret|meaning|means') else ['2.9.A']
        if k == 7:
            if has(r'geometric|first (success|6|prize|expert|hit)|until|first .* on the|within the first|more than \d+ (puzzles|tries|trials)'):
                return ['BEYOND.GEOM']
            if has(r'which .*binomial|binomial setting|is (this|x) binomial|why .*binomial|10%'):
                return ['2.10.A']
            if has(r'interpret'):
                return ['2.10.C']
            return ['2.10.B'] if has(r'mean|standard deviation|σ|expected') and not has(r'p\(x') else ['2.10.E']
        if k == 8:
            return ['BEYOND.COMB']
        if k == 9:
            if has(r'p̂₁ − p̂₂|p̂_1|difference (between|in) (the )?(two )?(sample )?proportions'):
                return ['3.9.A', '3.9.C']
            if has(r'x̄₁ − x̄₂|difference (between|in) (the )?(two )?(sample )?means'):
                return ['4.6.A', '4.6.C']
            if has(r'simulat|histogram|dot ?plot'):
                return ['2.12.A']
            pm = mean_or_prop(t, 'm', 'p')
            if has(r'condition|large counts|10%|normal because|approximately normal'):
                return ['4.1.B'] if pm == 'm' else ['3.2.B']
            if has(r'probab|p\(x̄|p\(p̂|interpret'):
                return ['4.1.C'] if pm == 'm' else ['3.2.C']
            return ['4.1.A'] if pm == 'm' else ['3.2.A']
        if k == 10:
            if has(r'unbiased|bias'):
                return ['3.1.A']
            if has(r'central limit|clt|skew'):
                return ['4.1.B']
            return ['2.12.A']
    if u == 'statistical-inference':
        pm = mean_or_prop(t, 'm', 'p')
        M = lambda m, p: m if pm == 'm' else p
        if k == 1:
            if has(r'margin of error|\bme\b|standard error|\bse\b'):
                return M(['4.2.E'], ['3.3.D'])
            return ['3.1.B']
        if k == 2:
            if has(r'condition|random|10%|large counts|normal'):
                return M(['4.2.C'], ['3.3.B'])
            if has(r'confidence level|\d+% confident|95% means|capture'):
                return M(['4.3.A'], ['3.4.A'])
            return M(['4.3.A'], ['3.4.A'])
        if k == 3:
            if has(r'sample size|how (large|many)|at most|no more than'):
                return ['3.3.D']
            if has(r'wider|narrower|width|increase|decrease|quadrupl|confidence level'):
                return ['3.4.C']
            if has(r'interpret|confident|claim|support|plausible'):
                return ['3.4.A', '3.4.B'] if has(r'claim|support|plausible|evidence') else ['3.4.A']
            if has(r'condition'):
                return ['3.3.B']
            return ['3.3.C']
        if k == 4:
            if has(r'\bt\*|critical value|degrees of freedom|\bdf\b|t distribution|t-distribution'):
                return ['4.2.A']
            if has(r'interpret|confident'):
                return ['4.3.A']
            if has(r'condition|robust|outlier|skew'):
                return ['4.2.C']
            if has(r'margin of error|standard error'):
                return ['4.2.E']
            return ['4.2.D']
        if k == 5:
            return M(['4.4.B'], ['3.5.B']) if has(r'h₀|hₐ|hypothes|null|alternative') else M(['4.4.A'], ['3.5.A'])
        if k == 6:
            if has(r'interpret|what does .*p-value|meaning|probability (of|that)'):
                return M(['4.5.B'], ['3.6.A'])
            if has(r'conclu|reject|evidence|α'):
                return M(['4.5.C'], ['3.7.B'])
            return M(['4.5.A'], ['3.7.A'])
        if k == 7:
            if has(r'condition'):
                return M(['4.4.C'], ['3.5.C'])
            if has(r'which test|appropriate|fits'):
                return M(['4.4.A'], ['3.5.A'])
            if has(r'conclu|reject|evidence'):
                return M(['4.5.C'], ['3.7.B'])
            return M(['4.5.A'], ['3.7.A'])
        if k == 8:
            if has(r'power|factor|increase|decrease|larger|smaller'):
                return ['3.8.C']
            if has(r'probability of (a )?type|p\(type|α|β ='):
                return ['3.8.B']
            if has(r'consequence|interpret|describe|in context|which error .* (serious|worse)'):
                return ['3.8.D']
            return ['3.8.A']
        if k == 9:
            if has(r'interval|confiden'):
                return ['3.11.A', '3.11.B'] if has(r'interpret|suggest|evidence|claim|above 0|contains 0|includes 0') else ['3.10.C', '3.10.D'] if has(r'construct|margin|standard error|calculat|find') else ['3.10.A', '3.10.B']
            if has(r'h₀|hₐ|hypothes'):
                return ['3.12.B']
            if has(r'condition|large counts|10%'):
                return ['3.12.C']
            if has(r'conclu|reject|evidence|interpret'):
                return ['3.13.B', '3.13.C']
            if has(r'p̂₁ − p̂₂|difference') and not has(r'test|p-value|z ='):
                return ['3.1.B']
            return ['3.13.A']
        if k == 10:
            paired = has(r'paired|before|after|matched|differences|same (students|subjects|people)')
            if has(r'interval|confiden'):
                return (['4.3.A'] if paired else ['4.8.A', '4.8.B']) if has(r'interpret|suggest|evidence|claim') else (['4.2.D'] if paired else ['4.7.C', '4.7.D'])
            if has(r'which (procedure|test)|appropriate|fits|calls for'):
                return ['4.4.A'] if paired else ['4.9.A']
            if has(r'h₀|hₐ|hypothes'):
                return ['4.4.B'] if paired else ['4.9.B']
            if has(r'condition'):
                return ['4.4.C'] if paired else ['4.9.C']
            if has(r'conclu|reject|evidence|interpret'):
                return ['4.5.C'] if paired else ['4.10.B', '4.10.C']
            return ['4.5.A'] if paired else ['4.10.A']
        if k in (11, 14):
            return ['BEYOND.SLOPE']
        if k == 12:
            return ['BEYOND.GOF']
        if k == 13:
            if has(r'expected count'):
                return ['3.15.A']
            if has(r'h₀|hₐ|hypothes'):
                return ['3.14.C']
            if has(r'condition|large counts|at least 5'):
                return ['3.14.D']
            if has(r'which test|homogeneity or independence|appropriate'):
                return ['3.14.B']
            if has(r'degrees of freedom|\bdf\b|chi-square distribution|skewed'):
                return ['3.14.A']
            if has(r'conclu|reject|evidence|interpret'):
                return ['3.15.C', '3.15.D']
            return ['3.15.B']
    raise ValueError((u, k, q['id']))


def main():
    banks = lib.load()
    n = 0
    for u, q in lib.items(banks):
        k = int(re.search(r'skill-(\d+)', q['skillId']).group(1))
        if 'batch S2' in q.get('sourceNotes', ''):
            # batch S2 items carry the objectives chosen when they were written (s2fill.py, s2frq.py)
            codes = [c.split('APSTATS.', 1)[1] for c in q['standards']]
        else:
            codes = tag(u, k, q)
        for c in codes:
            assert c in LO or c.split('.', 1)[1] in BEYOND, c
        q['standards'] = ['APSTATS.' + c for c in codes]
        n += 1
    lib.save(banks)
    print('retagged', n)


if __name__ == '__main__':
    main()
