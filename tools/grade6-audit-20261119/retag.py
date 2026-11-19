"""Grade 6 audit #9 and #10 (2026-11-19): standards tags say what each item practices.
 * Writing and Evaluating Algebraic Expressions: "write an expression for the phrase" is 6.EE.A.2a, naming a coefficient
   or term is 6.EE.A.2b, evaluating is 6.EE.A.2c; expressions for an unknown in a story add 6.EE.B.6. Any other item that
   asks for a coefficient, a constant term or the number of terms also carries 6.EE.A.2b.
 * Proportions: 7.RP.A.2c (equations for proportional relationships) is not what these items do. Deciding whether two
   ratios form a proportion is 7.RP.A.2a (marked as Grade 7 extension); solving one is 6.RP.A.3.
 * Comparing Data Displays: comparing two groups by a measure of center is 6.SP.B.5c with 7.SP.B.4 (extension);
   comparing two box plots is 6.SP.B.4 with 7.SP.B.4; finding one statistic of one data set is 6.SP.B.5c only.
 * Solving One-Variable Inequalities: solving px < q or x + p < q is 7.EE.B.4b (extension) with 6.EE.B.5.
Idempotent; items added by later batches carry their own tags."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

NEW = re.compile(r'-(g|h)\d{2}$')


def text(q):
    return ' '.join([q['prompt']] + [p.get('prompt', '') for p in q.get('parts', [])] + [o.get('text', '') for o in q.get('options', [])])


def tags_for(q):
    if NEW.search(q['id']):
        return None
    sk, t = q['skillId'], text(q)
    if sk == 'expressions-equations-skill-02':
        out = []
        if re.search(r'algebraic expression for the phrase', t):
            out.append('6.EE.A.2a')
        if re.search(r'Write an expression for', t):
            out += ['6.EE.A.2a', '6.EE.B.6']
        if re.search(r'coefficient|constant term|how many terms', t, re.I):
            out.append('6.EE.A.2b')
        if re.search(r'\bEvaluate\b', t):
            out.append('6.EE.A.2c')
        return list(dict.fromkeys(out)) or ['6.EE.A.2a']
    if sk == 'ratios-rates-percent-proportions-skill-05':
        return ['6.RP.A.3', '7.RP.A.2a'] if re.search(r'form a proportion', t) else ['6.RP.A.3']
    if sk == 'data-displays-skill-06':
        if re.search(r'box plots compare', t):
            return ['6.SP.B.4', '7.SP.B.4']
        if re.search(r'Group A|Team A|Class A', t):
            return ['6.SP.B.5c', '7.SP.B.4']
        return ['6.SP.B.5c']
    if sk == 'inequalities-skill-02':
        return ['6.EE.B.5', '7.EE.B.4b']
    if re.search(r'coefficient|constant term|how many terms', t, re.I) and '6.EE.A.2b' not in q['standards']:
        return q['standards'] + ['6.EE.A.2b']
    return None


def main():
    banks = lib.load()
    n = 0
    for u, q in lib.items(banks):
        t = tags_for(q)
        if t is not None and t != q['standards']:
            q['standards'] = t
            n += 1
    lib.save(banks)
    print('retagged:', n)


if __name__ == '__main__':
    main()
