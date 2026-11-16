"""Shared item contract for the 2026-11-16 audit gap skills.

A family is a function fn(r, L) → I(prompt, answer, steps, wrongs, check, fam) where r is a seeded
random.Random and L is the level index (0 Support/cp2, 1 Standard/cp1, 2 Advanced/honors).
`wrongs` is a list of (wrong answer text, why a student would give it); `check` is plain data that
verify.py uses to recompute the answer without importing the families. `check["show"]` lists text
that must be printed in the prompt, so the verifier works only from what students see.
Raise Reject to discard a draw (the builder simply draws again).
"""
from fractions import Fraction as F


class Reject(Exception):
    pass


def need(cond):
    if not cond:
        raise Reject()


def ri(r, lo, hi):
    return r.randint(lo, hi)


def g(v, dp=4):
    """Decimal text with trailing zeros removed: 7.5, 24, 0.75."""
    s = f"{float(v):.{dp}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def exact(v, dp=2):
    """True when v has at most dp decimal places."""
    return (F(v) * 10 ** dp).denominator == 1


def safe_round(v, dp):
    """Reject values that sit too close to a rounding boundary."""
    x = abs(float(v)) * 10 ** dp
    need(abs(x - int(x) - 0.5) > 0.02)


def W(ans, *pairs):
    """Distinct wrong answers, none equal to the keyed answer."""
    out, seen = [], {ans}
    for t, why in pairs:
        if t not in seen:
            seen.add(t)
            out.append((t, why))
    return out


def I(prompt, answer, steps, wrongs, check, fam):
    return dict(prompt=prompt, answer=answer, steps=steps, wrongs=W(answer, *wrongs), check=check, fam=fam)


def levels(L, *ok):
    need(L in ok)
