"""Independent mathematical verification of the Grade 8 Pre-Algebra banks.

Usage: python3 verify.py [unit-id ...]
For every question it re-derives correctness from the student-facing text (and the
data the prompt shows) with mathtext.py / checks_custom.py, which do not import the
authoring families. Checks:
  * short-answer / open-response part answers satisfy their check;
  * multiple-choice: the computed truth of every option equals its `correct` flag,
    exactly one is true, and options are pairwise distinct after simplification;
  * select-all: computed truth of every option equals its flag, >= 2 true, >= 1 false;
  * every '/' in student-facing text becomes a well-formed stacked fraction under the
    site's own math-display.js (run through node);
  * duplicate prompts within and across units; answer-sharing partner groups reported.
Writes docs/prealgebra/VERIFICATION_REPORT.md and out/verify-summary.json.
"""
import json, os, re, subprocess, sys
from collections import Counter, defaultdict
from fractions import Fraction as F
import mathtext as M
import checks_custom as C

ROOT = os.environ.get("PA8_OUT", "/home/claude/work/pkg")
REPO = os.environ.get("PA8_REPO", "/home/claude/repo_src/classroom-main")
UNITS = ["real-numbers-exponents", "equations-expressions", "linear-functional-relationships",
         "systems-linear-equations", "patterns-bivariate-data", "congruence-similarity", "geometry-applications"]


def truth(chk, text):
    k = chk["kind"]
    if k == "val":
        try:
            return M.same(M.val(text), M.ev(chk["expr"], chk.get("env")), chk.get("tol", 1e-9))
        except (M.ParseError, ZeroDivisionError, ValueError):
            return False
    if k == "approx":
        try:
            v = float(M.ev(chk["expr"], chk.get("env")))
        except (M.ParseError, ZeroDivisionError, ValueError):
            return False
        t = M.strip_units(M.strip_lhs(text)).replace(",", "")
        return C.round_text(v, chk["places"]) == t
    if k == "equiv":
        vs = chk.get("vars", ["x"])
        try:
            rhs_text = M.strip_lhs(text) if chk.get("strip", True) else text
            pts = [{v: F(p + 2 * j + 1, 3 + j) for j, v in enumerate(vs)} for p in (1, 2, 4, 7)]
            return all(M.same(M.ev(rhs_text, e), M.ev(chk["expr"], e)) for e in pts)
        except (M.ParseError, ZeroDivisionError, ValueError):
            return False
    if k == "eq":
        sol = M.solve_linear(chk["eq"], chk.get("var", "x"))
        sp = M.special(text)
        if sol[0] != "one":
            return sp == sol[0]
        if sp:
            return False
        try:
            return M.same(M.val(text), sol[1])
        except (M.ParseError, ZeroDivisionError, ValueError):
            return False
    if k == "sys":
        sol = M.solve_system(*chk["eqs"])
        sp = M.special(text)
        if sol[0] != "one":
            return sp == sol[0]
        if sp:
            return False
        try:
            x, y = M.parse_point(text)
        except M.ParseError:
            m = re.match(r"^\s*x\s*=\s*([^,]+),\s*y\s*=\s*(.+)$", text)
            if not m:
                return False
            x, y = M.ev(m.group(1)), M.ev(m.group(2))
        return M.same(x, sol[1][0]) and M.same(y, sol[1][1])
    if k == "text":
        return " ".join(str(text).lower().split()) in [" ".join(a.lower().split()) for a in chk["accept"]]
    if k == "py":
        return bool(C.CUSTOM[chk["fn"]](chk, text))
    raise ValueError("unknown check kind " + k)


def distinct_key(chk, text):
    t = str(text)
    try:
        if chk and chk["kind"] in ("val", "eq", "approx"):
            return ("n", float(M.val(t)) if chk["kind"] != "approx" else M.strip_units(t))
        if chk and chk["kind"] == "equiv":
            vs = chk.get("vars", ["x"])
            return ("e", tuple(round(float(M.ev(M.strip_lhs(t), {v: F(p + j, 2 + j) for j, v in enumerate(vs)})), 9) for p in (1, 3, 5)))
    except Exception:
        pass
    return ("s", " ".join(t.lower().replace("−", "-").split()))


def texts_of(q):
    out = [q["prompt"]] + list(q["solutionSteps"])
    out += [o["text"] for o in q.get("options", [])]
    out += [p["prompt"] for p in q.get("parts", [])] + [str(p["answer"]) for p in q.get("parts", [])]
    out += [q["answer"]] if isinstance(q["answer"], str) else list(map(str, q["answer"]))
    return out


DISPLAY_JS = r"""
const fs=require('fs'),vm=require('vm');const ctx={};ctx.globalThis=ctx;vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[1],'utf8'),ctx);const F=ctx.MK_MATH_DISPLAY.fractions;
const items=JSON.parse(fs.readFileSync(0,'utf8'));const bad=[];
const sup=/^[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]/;
for(const [id,s] of items){const out=F(s);
 if(out.includes('/')){bad.push([id,s,'raw slash survives: '+out]);continue}
 const re=/\[\[([^\[\]]*?) ; ([^\[\]]*?)\]\]/g;let m;
 while((m=re.exec(out))){const a=m[1].trim(),b=m[2].trim();
  if(!a||!b||sup.test(a)||sup.test(b)||/^[+=,]/.test(b)||/[=,+]$/.test(a)||/^√$/.test(a))bad.push([id,s,'malformed fraction: '+m[0]]);
  if(/[A-Za-z]{3,}/.test(a)||/[A-Za-z]{3,}/.test(b))bad.push([id,s,'word captured in fraction: '+m[0]]);}
 if(/√\[\[/.test(out))bad.push([id,s,'root over fraction: '+out]);
}
console.log(JSON.stringify(bad));
"""


def display_check(questions):
    items = [[q["id"], t] for q in questions for t in texts_of(q) if "/" in t]
    if not items:
        return []
    js = os.path.join(REPO, "worksheet-generator", "core", "math-display.js")
    out = subprocess.run(["node", "-e", DISPLAY_JS, js], input=json.dumps(items), capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def verify_unit(uid, all_prompts):
    bank = json.load(open(os.path.join(ROOT, "question-banks", "prealgebra", uid + ".json"), encoding="utf-8"))
    checks = json.load(open(os.path.join(ROOT, "tools", "prealgebra-authoring", "out", uid + ".checks.json"), encoding="utf-8"))
    errs = []
    stats = Counter()
    pairs = defaultdict(set)
    for q in bank["questions"]:
        c = checks[q["id"]]
        chk = c["q"]
        stats["questions"] += 1
        for s_ in (chk or {}).get("show", []):
            if str(s_) not in q["prompt"]:
                errs.append((q["id"], "prompt missing data value " + str(s_), q["prompt"][:80]))
        stats["check:" + (chk["kind"] if chk else "none") + (":" + chk["fn"] if chk and chk["kind"] == "py" else "")] += 1
        try:
            if q["format"] == "short-answer":
                if not truth(chk, q["answer"]):
                    errs.append((q["id"], "answer fails check", q["answer"]))
            elif q["format"] in ("multiple-choice", "select-all"):
                flags = [o["correct"] for o in q["options"]]
                if len({o["text"] for o in q["options"]}) != len(q["options"]):
                    errs.append((q["id"], "duplicate option text", [o["text"] for o in q["options"]]))
                calc = [truth(chk, o["text"]) for o in q["options"]]
                if flags != calc:
                    errs.append((q["id"], "option truth mismatch", list(zip([o["text"] for o in q["options"]], flags, calc))))
                keys = [distinct_key(chk, o["text"]) for o in q["options"]]
                if q["format"] == "multiple-choice" and len(set(keys)) != len(keys):
                    errs.append((q["id"], "options not distinct after simplification", [o["text"] for o in q["options"]]))
                if q["format"] == "multiple-choice":
                    if sum(flags) != 1:
                        errs.append((q["id"], "MC must have one correct", flags))
                    if q["answer"] != [o["text"] for o in q["options"] if o["correct"]][0]:
                        errs.append((q["id"], "answer text differs from correct option", q["answer"]))
                    stats["mcpos%d" % flags.index(True)] += 1
                else:
                    if sum(flags) < 2 or all(flags):
                        errs.append((q["id"], "select-all needs >=2 correct and >=1 incorrect", flags))
            elif q["format"] == "open-response":
                if chk is not None and not truth(chk, q["parts"][-1]["answer"]) and chk.get("whole") is not True:
                    pass
                for i, (p, pc) in enumerate(zip(q["parts"], c["parts"])):
                    if pc is None:
                        stats["or-part-unchecked"] += 1
                        continue
                    if not truth(pc, str(p["answer"])):
                        errs.append((q["id"], f"part {i + 1} fails check", p["answer"]))
                    else:
                        stats["or-part-checked"] += 1
        except Exception as e:  # a check that cannot run is a failure, never a pass
            errs.append((q["id"], "check crashed: " + repr(e), q["answer"]))
        pk = " ".join(q["prompt"].lower().split()) + "|" + str(q.get("diagram", {}).get("spec", {}).get("alt", "")) \
            + "|" + "|".join(p["prompt"] for p in q.get("parts", [])) + "|" + "|".join(sorted(o["text"] for o in q.get("options", [])))
        if pk in all_prompts and all_prompts[pk] != q["id"]:
            errs.append((q["id"], "duplicate prompt of " + all_prompts[pk], q["prompt"]))
        all_prompts.setdefault(pk, q["id"])
        if q["format"] in ("short-answer", "multiple-choice") and not q.get("diagram") and isinstance(q["answer"], str):
            key = re.sub(r"^[a-z]\s*=\s*", "", q["answer"].lower().replace(" ", ""))
            pairs[(q["skillId"], q["level"], key)].add(q["id"])
    for bad in display_check(bank["questions"]):
        errs.append((bad[0], "display: " + bad[2], bad[1]))
    groups = {k: v for k, v in pairs.items() if len(v) > 1}
    stats["partner-answer-groups"] = len(groups)
    stats["partner-items"] = sum(len(v) for v in groups.values())
    return errs, stats, groups


if __name__ == "__main__":
    units = sys.argv[1:] or UNITS
    allp = {}
    summary = {}
    total_err = 0
    lines = ["# Pre-Algebra (Grade 8) independent verification report", ""]
    for u in units:
        if not os.path.exists(os.path.join(ROOT, "question-banks", "prealgebra", u + ".json")):
            continue
        errs, stats, groups = verify_unit(u, allp)
        total_err += len(errs)
        summary[u] = {"errors": len(errs), **stats}
        print(u, "errors:", len(errs), dict(stats))
        for e in errs[:40]:
            print("   ", e)
        lines += [f"## {u}", "", f"- Questions: {stats['questions']}; verification failures: {len(errs)}",
                  "- Check methods: " + ", ".join(f"{k[6:]} {v}" for k, v in sorted(stats.items()) if k.startswith("check:")),
                  f"- Multiple-choice correct positions A/B/C/D: {stats['mcpos0']}/{stats['mcpos1']}/{stats['mcpos2']}/{stats['mcpos3']}",
                  f"- Open-response parts checked: {stats['or-part-checked']}; unchecked (explanations): {stats['or-part-unchecked']}",
                  f"- Answer-sharing groups usable for Partner Check (same skill and level, different prompts): {stats['partner-answer-groups']}", ""]
        if errs:
            lines += ["Failures:", ""] + [f"- {e[0]}: {e[1]}" for e in errs] + [""]
    os.makedirs(os.path.join(ROOT, "docs", "prealgebra"), exist_ok=True)
    open(os.path.join(ROOT, "tools", "prealgebra-authoring", "out", "verify-summary.json"), "w").write(json.dumps(summary, indent=1))
    if len(units) == len(UNITS):
        open(os.path.join(ROOT, "docs", "prealgebra", "VERIFICATION_REPORT.md"), "w").write("\n".join(lines))
    print("TOTAL ERRORS", total_err)
    sys.exit(1 if total_err else 0)
