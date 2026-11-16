"""Display-text helpers and an independent numeric evaluator for the 2026-11-14 HS gap skills.

The site's question banks show math as plain text (x², e^(2x), ln(x), √(x² + 1), sin⁻¹(x), π).
`val(text, **vars)` evaluates that *displayed* text with NumPy, so the verifier checks exactly what
students see. It never imports the families that wrote the text.
"""
import math, re
from fractions import Fraction as F
import numpy as np

SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
UNSUP = {v: k for k, v in zip("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")}


def sup(n):
    return str(n).translate(SUP)


def num(v):
    """Integer or fraction text: 3, -2, 3/4, -(5/2) is written -5/2."""
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def coef(c, var, first=False):
    """Coefficient in front of a variable part: 1 → '', -1 → '-', 2 → '2', 1/2 → '(1/2)'."""
    c = F(c)
    if c == 1:
        s = var
    elif c == -1:
        s = "-" + var
    elif c.denominator == 1:
        s = f"{c.numerator}{var}"
    else:
        s = f"({num(abs(c))}){var}" if c > 0 else f"-({num(abs(c))}){var}"
    return s


def join(terms):
    """Join signed term strings: ['3x²', '-2x', '5'] → '3x² - 2x + 5'."""
    out = ""
    for t in terms:
        if not t or t in ("0",):
            continue
        if not out:
            out = t
        elif t.startswith("-"):
            out += " - " + t[1:]
        else:
            out += " + " + t
    return out or "0"


def poly(cs, var="x"):
    """cs: {power: coefficient} → text, highest power first."""
    terms = []
    for p in sorted(cs, reverse=True):
        c = F(cs[p])
        if c == 0:
            continue
        if p == 0:
            terms.append(num(c))
        elif p == 1:
            terms.append(coef(c, var))
        else:
            terms.append(coef(c, var + sup(p)))
    return join(terms)


def paren(t):
    return t if re.fullmatch(r"[\w²³⁴⁵⁶⁷⁸⁹√π.]+", t) else f"({t})"


# ------------------------------------------------------------------ evaluator
FUN = {"ASIN": np.arcsin, "ACOS": np.arccos, "ATAN": np.arctan, "SIN": np.sin, "COS": np.cos, "TAN": np.tan,
       "SEC": lambda z: 1 / np.cos(z), "CSC": lambda z: 1 / np.sin(z), "COT": lambda z: 1 / np.tan(z),
       "EXP": np.exp, "LOG": np.log, "SQRT": np.sqrt, "ABS": np.abs, "PI": math.pi}


def to_py(t):
    s = t.replace("−", "-").replace("·", "*").replace("×", "*").replace("÷", "/").replace("′", "'")
    s = s.replace(" ", "")
    for a, b in (("sin⁻¹", "ASIN"), ("cos⁻¹", "ACOS"), ("tan⁻¹", "ATAN")):
        s = s.replace(a, b)
    # sin²(u) → (SIN(u))**2 (one level of nested parentheses inside)
    s = re.sub(r"(sin|cos|tan|sec|csc|cot)([²³⁴])\(((?:[^()]|\([^()]*\))*)\)",
               lambda m: f"({m.group(1)}({m.group(3)}))^{UNSUP[m.group(2)]}", s)
    for a, b in (("sin", "SIN"), ("cos", "COS"), ("tan", "TAN"), ("sec", "SEC"), ("csc", "CSC"), ("cot", "COT"), ("ln", "LOG")):
        s = s.replace(a, b)
    s = s.replace("π", "(PI)")
    s = re.sub(r"e\^\(", "EXP(", s)
    s = re.sub(r"e\^([a-z0-9])", r"EXP(\1)", s)
    s = re.sub(r"\be\b", "EXP(1)", s)
    s = re.sub(r"√\(", "SQRT(", s)
    s = re.sub(r"√([a-z0-9.]+)", r"SQRT(\1)", s)
    s = re.sub(r"LOG\|([^|]+)\|", r"LOG(ABS(\1))", s)
    s = re.sub(r"\|([^|]+)\|", r"ABS(\1)", s)
    # superscript powers
    s = re.sub(r"([⁻]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)", lambda m: "^(" + "".join(UNSUP[c] for c in m.group(1)) + ")", s)
    s = s.replace("^", "**")
    # implicit multiplication: after digit / lowercase variable / ')' and before '(' / variable / function
    s = re.sub(r"(?<=[0-9a-z)])(?=[(a-zA-Z])", "*", s)
    return s


def val(text, **v):
    env = dict(FUN)
    env.update(v)
    return eval(to_py(text), {"__builtins__": {}}, env)


def close(a, b, tol=1e-6):
    a, b = complex(a), complex(b)
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def dnum(f, x0, h=1e-5):
    """Central-difference derivative of a Python function (4th-order)."""
    return (-f(x0 + 2 * h) + 8 * f(x0 + h) - 8 * f(x0 - h) + f(x0 - 2 * h)) / (12 * h)
