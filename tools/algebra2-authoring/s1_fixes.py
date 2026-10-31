"""Cosmetic notation fixes for session-1 items (IDs, answers' meaning and structure unchanged).
Applied by the uNN_topup.py scripts right after Bank.resume()."""
import re


def _fix(t):
    if not isinstance(t, str): return t
    t = re.sub(r"([xy]) - \(-(\d+)\)", r"\1 + \2", t)
    t = re.sub(r"([xy]) ([-+]) \((\d+)\)", r"\1 \2 \3", t)
    t = re.sub(r"/(-?\d+/\d+)(?=[.\s;,]|$)", r"/(\1)", t)
    t = re.sub(r"/(-\d+)(?=[.\s;,]|$)", r"/(\1)", t)
    t = re.sub(r"= (-?)(\d+/\d+)\(", lambda m: f"= {m.group(1)}({m.group(2)})(", t)
    t = re.sub(r"(?<![\w)/(])(-?)(\d+)/(\d+)([xy])\b", lambda m: f"{m.group(1)}({m.group(2)}/{m.group(3)}){m.group(4)}", t)
    return t


def apply(bank):
    n = 0
    for q in bank.qs:
        before = repr(q)
        q["prompt"] = _fix(q["prompt"]); q["solutionSteps"] = [_fix(s) for s in q["solutionSteps"]]
        q["answer"] = [_fix(a) for a in q["answer"]] if isinstance(q["answer"], list) else _fix(q["answer"])
        for o in q.get("options", []): o["text"] = _fix(o["text"])
        for p in q.get("parts", []): p["prompt"] = _fix(p["prompt"]); p["answer"] = _fix(p["answer"])
        n += repr(q) != before
    return n
