"""Tiny propositional-logic engine used to compute every truth-table key.
Syntax: variables are single lowercase letters; operators ¬ ∧ ∨ → ↔ ⊕ and parentheses.
Precedence (high→low): ¬, ∧, ∨ and ⊕, →, ↔.  → and ↔ are right-associative."""
import itertools

OPS = {'∧': 3, '∨': 2, '⊕': 2, '→': 1, '↔': 0}


def tokenize(s):
    out = []
    for ch in s.replace('~', '¬').replace('->', '→'):
        if ch.isspace():
            continue
        out.append(ch)
    return out


def parse(s):
    toks = tokenize(s)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def eat(t=None):
        tok = toks[pos[0]]
        if t is not None and tok != t:
            raise ValueError('expected %s got %s in %s' % (t, tok, s))
        pos[0] += 1
        return tok

    def primary():
        t = peek()
        if t == '¬':
            eat()
            return ('not', primary())
        if t == '(':
            eat('(')
            e = expr(0)
            eat(')')
            return e
        if t in ('T', 'F'):
            eat()
            return ('const', t == 'T')
        if t and t.isalpha():
            eat()
            return ('var', t)
        raise ValueError('bad token %r in %s' % (t, s))

    def expr(minp):
        left = primary()
        while True:
            t = peek()
            if t not in OPS or OPS[t] < minp:
                break
            p = OPS[t]
            eat()
            right = expr(p if t in '→↔' else p + 1)
            left = (t, left, right)
        return left

    e = expr(0)
    if pos[0] != len(toks):
        raise ValueError('trailing tokens in ' + s)
    return e


def ev(e, env):
    k = e[0]
    if k == 'var':
        return env[e[1]]
    if k == 'const':
        return e[1]
    if k == 'not':
        return not ev(e[1], env)
    a, b = ev(e[1], env), ev(e[2], env)
    return {'∧': a and b, '∨': a or b, '⊕': a != b, '→': (not a) or b, '↔': a == b}[k]


def variables(s):
    return sorted({c for c in s if c.isalpha() and c.islower()})


def rows(vs):
    """Standard order: all T first (TT, TF, FT, FF for two variables)."""
    return [dict(zip(vs, vals)) for vals in itertools.product([True, False], repeat=len(vs))]


def column(s, vs=None):
    vs = vs or variables(s)
    e = parse(s)
    return [ev(e, r) for r in rows(vs)]


def colstr(s, vs=None):
    return ''.join('T' if b else 'F' for b in column(s, vs))


def equivalent(a, b):
    vs = sorted(set(variables(a)) | set(variables(b)))
    return column(a, vs) == column(b, vs)


def tautology(s):
    return all(column(s))


def contradiction(s):
    return not any(column(s))


def valid(premises, conclusion):
    vs = sorted(set().union(*[set(variables(p)) for p in premises + [conclusion]]))
    ps = [parse(p) for p in premises]
    c = parse(conclusion)
    for r in rows(vs):
        if all(ev(p, r) for p in ps) and not ev(c, r):
            return False, r
    return True, None


def table_text(vs, cols):
    """Render a truth table with tbl{} mini-syntax: header row then rows."""
    head = '&&'.join(vs + [c for c in cols])
    body = []
    for r in rows(vs):
        cells = ['T' if r[v] else 'F' for v in vs] + ['T' if ev(parse(c), r) else 'F' for c in cols]
        body.append('&&'.join(cells))
    return 'tbl{' + ' ;; '.join([head] + body) + '}'
