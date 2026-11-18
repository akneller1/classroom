"""Tiny unicode-math -> python evaluator for independent answer checks (no sympy)."""
import re, math, cmath

SUP = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺', '0123456789-+')
SUB = str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')
FUNCS = {'sin', 'cos', 'tan', 'csc', 'sec', 'cot', 'ln', 'log', 'sqrt', 'cbrt', 'abs', 'asin', 'acos', 'atan', 'exp'}


class ParseError(Exception):
    pass


def norm(s):
    s = str(s)
    s = s.replace('−', '-').replace('–', '-').replace('·', '*').replace('×', '*').replace('÷', '/')
    s = s.replace('⋅', '*').replace(' ', ' ').replace(' ', ' ')
    # inverse trig
    s = re.sub(r'(sin|cos|tan)⁻¹', r'a\1', s)
    s = re.sub(r'(sin|cos|tan)\^\(-1\)', r'a\1', s)
    # superscripts -> ^(..)
    s = re.sub(r'([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)', lambda m: '^(' + m.group(1).translate(SUP) + ')', s)
    # log bases: log₂ x, log_2(x), log_(1/2)(x)
    s = re.sub(r'log([₀₁₂₃₄₅₆₇₈₉]+)', lambda m: 'log_(' + m.group(1).translate(SUB) + ')', s)
    s = re.sub(r'log_(\d+(?:\.\d+)?)', r'log_(\1)', s)
    s = s.replace('√', ' sqrt ').replace('∛', ' cbrt ').replace('π', ' pi ')
    return s


def tokenize(s):
    toks = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1; continue
        m = re.match(r'\d+(?:,\d{3})+(?!\d)(?:\.\d+)?|\d*\.\d+|\d+', s[i:])
        if m:
            toks.append(('num', m.group(0).replace(',', ''))); i += len(m.group(0)); continue
        if s.startswith('log_', i):
            toks.append(('logb', None)); i += 4; continue
        m = re.match(r'[A-Za-z]+', s[i:])
        if m:
            w = m.group(0)
            # split into known function names / single-letter variables
            j = 0
            while j < len(w):
                for f in sorted(FUNCS | {'pi'}, key=len, reverse=True):
                    if w.startswith(f, j):
                        toks.append(('fn' if f != 'pi' else 'const', f)); j += len(f); break
                else:
                    toks.append(('var', w[j])); j += 1
            i += len(w); continue
        if c in '+-*/^(),|[]{}':
            toks.append(('op', c)); i += 1; continue
        if c == '!':
            toks.append(('op', '!')); i += 1; continue
        raise ParseError('char %r in %r' % (c, s))
    return toks


class P:
    def __init__(self, toks, env):
        self.t = toks; self.i = 0; self.env = env; self.absdepth = 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def take(self, v=None):
        k = self.peek()
        if v is not None and k[1] != v:
            raise ParseError('expected %s got %s' % (v, k))
        self.i += 1
        return k

    def expr(self):
        v = self.term()
        while self.peek()[1] in ('+', '-'):
            op = self.take()[1]
            w = self.term()
            v = v + w if op == '+' else v - w
        return v

    def starts_atom(self):
        k, v = self.peek()
        if k in ('num', 'var', 'fn', 'const', 'logb'):
            return True
        if k == 'op' and v in '([{':
            return True
        if k == 'op' and v == '|' and self.absdepth == 0:
            return True
        return False

    def term(self):
        v = self.unary()
        while True:
            k, op = self.peek()
            if op in ('*', '/'):
                self.take()
                w = self.unary()
                v = v * w if op == '*' else v / w
            elif self.starts_atom():  # implicit multiplication
                w = self.power()
                v = v * w
            else:
                return v

    def unary(self):
        if self.peek()[1] == '-':
            self.take(); return -self.unary()
        if self.peek()[1] == '+':
            self.take(); return self.unary()
        return self.power()

    def power(self):
        b = self.postfix()
        if self.peek()[1] == '^':
            self.take()
            e = self.unary()
            if isinstance(b, float) and b < 0 and isinstance(e, float) and e != int(e):
                from fractions import Fraction
                fr = Fraction(e).limit_denominator(12)
                if fr.denominator % 2 == 1:
                    r = abs(b) ** float(fr)
                    return r if fr.numerator % 2 == 0 else -r
            return b ** e
        return b

    def postfix(self):
        v = self.atom()
        while self.peek()[1] == '!':
            self.take(); v = math.factorial(int(round(v.real if isinstance(v, complex) else v)))
        return v

    def func_arg(self):
        # function argument: parenthesised group, or a tight atom chain like 2x, √7, x
        if self.peek()[1] in ('(', '[', '{'):
            return self.power()
        # unparenthesised: take power (e.g. sin x, √x, √7, log 5)
        return self.power()

    def atom(self):
        k, v = self.take()
        if k == 'num':
            return float(v)
        if k == 'const':
            return math.pi
        if k == 'var':
            if v not in self.env:
                raise ParseError('unknown var ' + v)
            return self.env[v]
        if k == 'op' and v in '([{':
            close = {'(': ')', '[': ']', '{': '}'}[v]
            e = self.expr()
            self.take(close)
            return e
        if k == 'op' and v == '|':
            self.absdepth += 1
            e = self.expr()
            self.absdepth -= 1
            self.take('|')
            return abs(e)
        if k == 'logb':
            base = self.atom()  # (b)
            arg = self.func_arg()
            return clog(arg) / clog(base)
        if k == 'fn':
            # power on function name: sin²x
            pw = None
            if self.peek()[1] == '^':
                self.take(); pw = self.atom()
            arg = self.func_arg()
            r = apply(v, arg)
            return r ** pw if pw is not None else r
        raise ParseError('unexpected %s %s' % (k, v))


def clog(x):
    if isinstance(x, complex) or x <= 0:
        return cmath.log(x)
    return math.log(x)


def apply(f, a):
    real = not isinstance(a, complex)
    if f == 'sqrt':
        return math.sqrt(a) if real and a >= 0 else cmath.sqrt(a)
    if f == 'cbrt':
        return math.copysign(abs(a) ** (1 / 3), a) if real else a ** (1 / 3)
    if f == 'abs':
        return abs(a)
    if f == 'ln':
        return clog(a)
    if f == 'log':
        return clog(a) / math.log(10)
    if f == 'exp':
        return cmath.exp(a) if not real else math.exp(a)
    m = cmath if not real else math
    if f in ('sin', 'cos', 'tan'):
        return getattr(m, f)(a)
    if f == 'csc':
        return 1 / m.sin(a)
    if f == 'sec':
        return 1 / m.cos(a)
    if f == 'cot':
        return 1 / m.tan(a)
    if f in ('asin', 'acos', 'atan'):
        return getattr(m, f)(a)
    raise ParseError(f)


def ev(s, env=None):
    env = dict(env or {})
    env.setdefault('i', 1j)
    env.setdefault('e', math.e)
    toks = tokenize(norm(s))
    p = P(toks, env)
    v = p.expr()
    if p.i != len(toks):
        raise ParseError('trailing %s in %r' % (toks[p.i:], s))
    return v


def close(a, b, tol=1e-6):
    try:
        return abs(a - b) <= tol * max(1, abs(a), abs(b))
    except TypeError:
        return False
