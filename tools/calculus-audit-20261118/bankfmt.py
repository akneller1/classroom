"""Print sympy expressions in the Calculus bank's text style: 3x² - 2x + 5, e^(2x), √(x + 1), ln(x), 5/2, (1/3)x³."""
import re
import sympy as sp

SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')
x, t = sp.symbols('x t')


def _num(v):
    v = sp.nsimplify(v)
    if v.is_Integer:
        return str(int(v))
    if v.is_Rational:
        return f'{v.p}/{v.q}'
    return bt(v)


def bt(e, var_order=None):
    """Bank text for a sympy expression."""
    e = sp.sympify(e)
    if e.is_Number:
        return _num(e)
    if e is sp.pi:
        return 'π'
    if e is sp.E:
        return 'e'
    if e.is_Symbol:
        return str(e)
    if e.is_Add:
        terms = e.as_ordered_terms()
        out = ''
        for i, term in enumerate(terms):
            c, rest = term.as_coeff_Mul()
            neg = c < 0
            s = bt(-term if neg else term)
            if i == 0:
                out = ('-' if neg else '') + s
            else:
                out += (' - ' if neg else ' + ') + s
        return out
    if e.is_Mul:
        c, rest = e.as_coeff_Mul()
        if c < 0:
            return '-' + bt(-e)
        exps = [f for f in sp.Mul.make_args(e) if isinstance(f, sp.exp) or (f.is_Pow and f.base is sp.E)]
        if exps:
            others = sp.Mul(*[f for f in sp.Mul.make_args(e) if f not in exps])
            os_ = '' if others == 1 else bt(others)
            if others.is_Add or (others.is_Mul and sp.fraction(others)[1] != 1) or (others.is_Rational and not others.is_Integer):
                os_ = f'({os_})'
            return os_ + ''.join(bt(f) for f in exps)
        num, den = sp.fraction(e)
        if den != 1:
            ns, ds = bt(num), bt(den)
            if not (num.is_Atom or (num.is_Mul and not num.is_Add) or num.is_Pow or num.is_Function):
                ns = f'({ns})'
            if not (den.is_Atom or den.is_Function):
                ds = f'({ds})'
            if num == 1 and not den.is_Atom:
                return f'1/{ds}'
            return f'{ns}/{ds}'
        parts = []
        if c != 1:
            parts.append(_num(c) if c.is_Integer else f'({_num(c)})')
        factors = sorted(sp.Mul.make_args(rest), key=lambda f: (0 if f.is_Pow and f.base.is_Symbol or f.is_Symbol else 1, str(f)))
        for f in factors:
            s = bt(f)
            if f.is_Add:
                s = f'({s})'
            parts.append(s)
        return ''.join(parts)
    if e.is_Pow:
        b, p = e.base, e.exp
        if b is sp.E:
            if p.is_Integer and p > 0:
                return 'e' + str(p).translate(SUP)
            ps = bt(p)
            return 'e^x' if ps == 'x' else f'e^({ps})'
        if p == sp.Rational(1, 2):
            return f'√{bt(b)}' if (b.is_Symbol or (b.is_Integer and b > 0)) else f'√({bt(b)})'
        if p == -1:
            bs = bt(b)
            return f'1/{bs}' if (b.is_Symbol or b.is_Function) else f'1/({bs})'
        if p.is_Integer and p < 0:
            return f'1/{bt(b ** (-p))}' if b.is_Symbol else f'1/({bt(b ** (-p))})'
        bs = bt(b)
        if not (b.is_Symbol or (b.is_Integer and b >= 0) or b.is_Function):
            bs = f'({bs})'
        if p.is_Integer:
            if b.is_Function and b.func in (sp.sin, sp.cos, sp.tan, sp.sec, sp.csc, sp.cot):
                return f'{b.func.__name__}{str(p).translate(SUP)}({bt(b.args[0])})'
            return bs + str(p).translate(SUP)
        return f'{bs}^({bt(p)})'
    if isinstance(e, sp.exp):
        if e.args[0].is_Integer and e.args[0] > 0:
            return 'e' + str(e.args[0]).translate(SUP)
        ps = bt(e.args[0])
        return 'e^x' if ps == 'x' else f'e^({ps})'
    if isinstance(e, sp.log):
        return f'ln({bt(e.args[0])})'
    if isinstance(e, sp.Abs):
        return f'|{bt(e.args[0])}|'
    if e.is_Function:
        name = {'asin': 'sin⁻¹', 'acos': 'cos⁻¹', 'atan': 'tan⁻¹'}.get(e.func.__name__, e.func.__name__)
        return f'{name}({bt(e.args[0])})'
    return str(e)


def val(e):
    """A value: exact if rational or simple, otherwise exact text."""
    e = sp.nsimplify(sp.simplify(e)) if sp.sympify(e).is_number else e
    return bt(e)
