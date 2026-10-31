"""Wording-only fixes found in the Oct 31 audit (no answers change mathematically). Idempotent; run after unit scripts."""
import json, glob, re
REP = [(r"\b(\d*1)th\b(?<!11th)", None), ("Take the 3th root", "Take the cube root"), ("Take the 2th root", "Take the square root"),
       ("(1 + 0.03/1)^(1t)", "(1 + 0.03)^t"), ("and 1√", "and √"), ("and -1√", "and -√"), ("1√50 = 5√2", "√50 = 5√2"), (" in in.", " in inches"), ("(measurements in in.)", "(measurements in inches)")]
def ordfix(t):
    return re.sub(r"\b(\d+)th\b", lambda m: m.group(1) + ("th" if m.group(1)[-2:] in ("11", "12", "13") else {"1": "st", "2": "nd", "3": "rd"}.get(m.group(1)[-1], "th")), t)
def fix(t):
    if not isinstance(t, str): return t
    t = ordfix(t)
    for a, b in REP[1:]: t = t.replace(a, b)
    return t
n = 0
for f in glob.glob("out/question-banks/*/*.json"):
    d = json.load(open(f)); before = json.dumps(d, ensure_ascii=False)
    for q in d["questions"]:
        q["prompt"] = fix(q["prompt"]); q["answer"] = [fix(a) for a in q["answer"]] if isinstance(q["answer"], list) else fix(q["answer"])
        q["solutionSteps"] = [fix(s) for s in q["solutionSteps"]]
        for o in q.get("options", []): o["text"] = fix(o["text"])
        for p in q.get("parts", []): p["prompt"] = fix(p["prompt"]); p["answer"] = fix(p["answer"])
    after = json.dumps(d, ensure_ascii=False)
    if after != before:
        n += 1; json.dump(d, open(f, "w"), ensure_ascii=False, indent=1); print("fixed", f)
print(n, "files changed")
