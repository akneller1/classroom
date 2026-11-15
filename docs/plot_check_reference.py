"""Reference checker for the provisional `format: "plot"` item type.
Codex: port check(plot, response) to JS; every item ships testVectors that this function passes.
Responses are what the widget records after snapping to the grid (integers, or tick values on a number line).
Returns (ok: bool, code: str|None). Codes map to plot.feedback messages."""
from fractions import Fraction as Fr

def F(v):
    return Fr(str(v)) if not isinstance(v, Fr) else v

def on_curve(kind, t, x, y):
    x, y = F(x), F(y)
    a, h, k = (F(t.get("a", 1)), F(t.get("h", 0)), F(t.get("k", 0)))
    if kind == "line": return y == F(t["m"]) * x + F(t["b"])
    if kind == "abs": return y == a * abs(x - h) + k
    if kind == "parabola": return y == a * (x - h) ** 2 + k
    if kind == "sqrt":
        if x < h: return False
        r = x - h; s = Fr(int(r ** 0.5 + 0.5)) if r.denominator == 1 else None
        return s is not None and s * s == r and y == a * s + k
    if kind == "cbrt":
        r = x - h; c = round(abs(float(r)) ** (1 / 3)) * (1 if r >= 0 else -1)
        return Fr(c) ** 3 == r and y == a * c + k
    if kind == "exponential": return x.denominator == 1 and y == F(t["a"]) * F(t["b"]) ** int(x)
    raise ValueError(kind)

def check(plot, resp):
    tool, t = plot["tool"], plot["target"]
    if tool == "number-line-point":
        want = sorted(F(v) for v in t["values"]); got = sorted(F(v) for v in resp["values"])
        if got == want: return True, None
        if len(got) != len(want): return False, "count"
        return False, "position"
    if tool == "points":
        want = {(F(x), F(y)) for x, y in t["points"]}; got = {(F(x), F(y)) for x, y in resp["points"]}
        if got == want: return True, None
        if {(y, x) for x, y in got} == want: return False, "swapped-coordinates"
        return False, "position"
    if tool == "number-line-inequality":
        if "between" in t:  # compound
            if resp.get("between") != t["between"]: return False, "and-or"
            for side in ("left", "right"):
                if F(resp[side]["value"]) != F(t[side]["value"]): return False, "boundary"
                if resp[side]["closed"] != t[side]["closed"]: return False, "closed-open"
            return True, None
        if F(resp["boundary"]) != F(t["boundary"]): return False, "boundary"
        if resp["direction"] != t["direction"]: return False, "direction"
        if resp["closed"] != t["closed"]: return False, "closed-open"
        return True, None
    if tool in ("line", "exponential"):
        p, q = resp["points"]
        if tuple(p) == tuple(q): return False, "same-point"
        if all(on_curve(tool, t, *pt) for pt in (p, q)): return True, None
        if tool == "line":
            m = (F(q[1]) - F(p[1])) / (F(q[0]) - F(p[0])) if F(q[0]) != F(p[0]) else None
            if m is not None and m == F(t["m"]): return False, "intercept"
            if m is not None and m == -F(t["m"]): return False, "slope-sign"
            if m is not None and F(t["m"]) != 0 and m == 1 / F(t["m"]): return False, "slope-reciprocal"
            return False, "slope"
        return False, "points-off-curve"
    if tool in ("abs", "parabola", "sqrt", "cbrt"):
        (ax, ay), (bx, by) = resp["anchor"], resp["point"]
        h, k = F(t["h"]), F(t["k"])
        if (F(ax), F(ay)) != (h, k):
            if (F(ax), F(ay)) == (-h, k): return False, "h-sign"
            if (F(ax), F(ay)) == (h, -k): return False, "k-sign"
            if (F(ax), F(ay)) == (k, h): return False, "swapped-hk"
            return False, "anchor"
        if F(bx) == h: return False, "same-x"
        if on_curve(tool, t, bx, by): return True, None
        neg = dict(t, a=-F(t.get("a", 1)))
        if on_curve(tool, neg, bx, by): return False, "a-sign"
        return False, "stretch"
    if tool == "region":
        p, q = resp["points"]
        if not all(on_curve("line", t, *pt) for pt in (p, q)) or tuple(p) == tuple(q): return False, "boundary-line"
        strict = t["op"] in ("<", ">")
        up = t["op"] in (">", ">=", "≥")
        if resp["dashed"] != strict: return False, "dashed-solid"
        if resp["shade"] != ("above" if up else "below"): return False, "shade-side"
        return True, None
    if tool == "system":
        for line_t, line_r in zip(t["lines"], resp["lines"]):
            ok, code = check({"tool": "line", "target": line_t}, {"points": line_r})
            if not ok: return False, "line-" + code
        if tuple(F(v) for v in resp["solution"]) != tuple(F(v) for v in t["solution"]): return False, "solution"
        return True, None
    raise ValueError(tool)
