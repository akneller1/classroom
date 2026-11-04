"""Independent verification of the Grade 7 / Grade 6 banks.

Usage: python3 gverify.py <courseId> [unit-id ...]
Reuses the Grade 8 verifier's truth tests (mathtext.py parser + checks_custom.py) plus gchecks.py,
none of which import the authoring families. In addition to the Grade 8 checks it verifies:
  * every skillId exists in MK_COURSE_CATALOG for the unit, level codes, required fields;
  * every item has >= 1 solution step; prompts never mention a figure without a diagram;
  * near-duplicates within a skill (same prompt with numbers removed AND same answer and options);
  * out-of-grade notation (logarithms, complex numbers, radicals of negatives, etc.);
  * activity readiness per skill/level: cipher-eligible integer 1–25, >= 4-step solution, text-only MC.
Writes docs/<course>/VERIFICATION_REPORT.md and tools/middle-grades-authoring/out/<course>/verify-summary.json.
"""
import json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, "..", "prealgebra-authoring"))
import gbuild
os.environ.setdefault("PA8_REPO", gbuild.REPO)
import verify as Vf          # Grade 8 verifier (truth, distinct_key, display_check, texts_of)
import gchecks  # noqa: F401  registers Grade 6/7 checks
Vf.REPO = gbuild.REPO
OUT = gbuild.OUT
FORBID = re.compile(r"\blog|\bln\b|√-|\bi²|complex|derivative|matrix|sin⁻¹|cos⁻¹|tan⁻¹")
FIG = re.compile(r"(?<!is )\bshown\b|\bthe (graph|figure|diagram|plot) (below|above|shows)\b", re.I)


def num_answer(q):
    if not isinstance(q["answer"], str):
        return None
    t = re.sub(r"^[a-z]\s*=\s*", "", q["answer"].strip())
    return int(t) if re.fullmatch(r"\d+", t) else None


def verify_unit(course, uid, skills, allp):
    bank = json.load(open(os.path.join(OUT, "question-banks", course, uid + ".json"), encoding="utf-8"))
    checks = json.load(open(os.path.join(OUT, "tools", "middle-grades-authoring", "out", course, uid + ".checks.json"), encoding="utf-8"))
    errs, stats = [], Counter()
    ready = defaultdict(Counter)
    near = {}
    pairs = defaultdict(set)
    assert bank["courseId"] == course and bank["unitId"] == uid
    for q in bank["questions"]:
        c = checks[q["id"]]
        chk = c["q"]
        stats["questions"] += 1
        stats[q["level"]] += 1
        if q["skillId"] not in skills:
            errs.append((q["id"], "unknown skillId", q["skillId"]))
        if q["level"] not in ("cp2", "cp1", "honors"):
            errs.append((q["id"], "bad level", q["level"]))
        if not q["solutionSteps"] or not all(str(s).strip() for s in q["solutionSteps"]):
            errs.append((q["id"], "missing solution steps", ""))
        if FORBID.search(q["prompt"]):
            errs.append((q["id"], "out-of-grade notation", q["prompt"][:80]))
        if FIG.search(q["prompt"]) and not q.get("diagram"):
            errs.append((q["id"], "refers to a figure that is not attached", q["prompt"][:80]))
        if q.get("diagram"):
            src = os.path.join(OUT, q["diagram"]["spec"]["src"])
            if not os.path.exists(src):
                errs.append((q["id"], "diagram file missing", src))
        stats["check:" + (chk["kind"] if chk else "none") + (":" + chk["fn"] if chk and chk["kind"] == "py" else "")] += 1
        try:
            if q["format"] == "short-answer":
                if not Vf.truth(chk, q["answer"]):
                    errs.append((q["id"], "answer fails check", q["answer"]))
            elif q["format"] in ("multiple-choice", "select-all"):
                flags = [o["correct"] for o in q["options"]]
                if len({o["text"] for o in q["options"]}) != len(q["options"]):
                    errs.append((q["id"], "duplicate option text", [o["text"] for o in q["options"]]))
                calc = [bool(Vf.truth(chk, o["text"])) for o in q["options"]]
                if flags != calc:
                    errs.append((q["id"], "option truth mismatch", list(zip([o["text"] for o in q["options"]], flags, calc))))
                keys = [Vf.distinct_key(chk, o["text"]) for o in q["options"]]
                if q["format"] == "multiple-choice":
                    if len(set(keys)) != len(keys):
                        errs.append((q["id"], "options not distinct after simplification", [o["text"] for o in q["options"]]))
                    if sum(flags) != 1:
                        errs.append((q["id"], "MC must have exactly one correct", flags))
                    elif q["answer"] != [o["text"] for o in q["options"] if o["correct"]][0]:
                        errs.append((q["id"], "answer text differs from correct option", q["answer"]))
                    else:
                        stats["mcpos%d" % flags.index(True)] += 1
                elif sum(flags) < 2 or all(flags):
                    errs.append((q["id"], "select-all needs >=2 correct and >=1 incorrect", flags))
            elif q["format"] == "open-response":
                if len(q["parts"]) < 4:
                    errs.append((q["id"], "open-response needs >= 4 parts", len(q["parts"])))
                for i, (p, pc) in enumerate(zip(q["parts"], c["parts"])):
                    if pc is None:
                        stats["or-part-unchecked"] += 1
                    elif not Vf.truth(pc, str(p["answer"])):
                        errs.append((q["id"], f"part {i + 1} fails check", p["answer"]))
                    else:
                        stats["or-part-checked"] += 1
        except Exception as e:  # a check that cannot run is a failure, never a pass
            errs.append((q["id"], "check crashed: " + repr(e), q["answer"]))
        pk = " ".join(q["prompt"].lower().split()) + "|" + str(q.get("diagram", {}).get("spec", {}).get("alt", "")) + "|" + \
            "|".join(p["prompt"] for p in q.get("parts", [])) + "|" + "|".join(sorted(o["text"] for o in q.get("options", [])))
        if pk in allp and allp[pk] != q["id"]:
            errs.append((q["id"], "duplicate prompt of " + allp[pk], q["prompt"][:80]))
        allp.setdefault(pk, q["id"])
        nk = (q["skillId"], re.sub(r"\d+", "#", pk), str(q["answer"]), tuple(sorted(re.findall(r"\d+", pk))))
        if nk in near:
            errs.append((q["id"], "near-duplicate of " + near[nk], q["prompt"][:80]))
        near.setdefault(nk, q["id"])
        rk = (q["skillId"], q["level"])
        n = num_answer(q)
        if n is not None and 1 <= n <= 25 and not re.search(r"which of the following|select all|which graph", q["prompt"], re.I):
            ready[rk]["cipher"] += 1
        if len({s.lower() for s in q["solutionSteps"]}) >= 4:
            ready[rk]["steps4"] += 1
        if q["format"] == "multiple-choice" and not q.get("diagram"):
            ready[rk]["mc_text"] += 1
        if q["format"] in ("multiple-choice", "short-answer") and not q.get("diagram") and isinstance(q["answer"], str):
            pairs[(q["skillId"], q["level"], re.sub(r"^[a-z]\s*=\s*", "", q["answer"].lower().replace(" ", "")))].add(q["id"])
        if "error-analysis" in q["sourceNotes"] or q["id"] in ():
            pass
    for bad in Vf.display_check(bank["questions"]):
        errs.append((bad[0], "display: " + bad[2], bad[1]))
    groups = {k: v for k, v in pairs.items() if len(v) > 1}
    stats["partner-answer-groups"] = len(groups)
    return errs, stats, ready


def main(course, units=None):
    cat = gbuild.catalog(course)
    units = units or list(cat.keys())
    allp, summary, total = {}, {}, 0
    lines = [f"# {course} independent verification report", ""]
    readiness = {}
    for u in units:
        if not os.path.exists(os.path.join(OUT, "question-banks", course, u + ".json")):
            print(u, "NOT BUILT")
            continue
        skills = {s["id"] for s in cat[u]["skills"]}
        errs, stats, ready = verify_unit(course, u, skills, allp)
        total += len(errs)
        summary[u] = {"errors": len(errs), **stats}
        for (sk, lv), cnt in ready.items():
            readiness[f"{sk}|{lv}"] = dict(cnt)
        print(u, "errors:", len(errs), "q:", stats["questions"])
        for e in errs[:30]:
            print("   ", e)
        lines += [f"## {u}", "", f"- Questions: {stats['questions']}; verification failures: {len(errs)}",
                  "- Check methods: " + ", ".join(f"{k[6:]} {v}" for k, v in sorted(stats.items()) if k.startswith("check:")),
                  f"- Multiple-choice correct positions A/B/C/D: {stats['mcpos0']}/{stats['mcpos1']}/{stats['mcpos2']}/{stats['mcpos3']}",
                  f"- Open-response parts checked: {stats['or-part-checked']}; unchecked: {stats['or-part-unchecked']}",
                  f"- Partner Check answer-sharing groups: {stats['partner-answer-groups']}", ""]
        if errs:
            lines += ["Failures:", ""] + [f"- {e[0]}: {e[1]}" for e in errs] + [""]
    od = os.path.join(OUT, "tools", "middle-grades-authoring", "out", course)
    os.makedirs(od, exist_ok=True)
    json.dump({"units": summary, "readiness": readiness}, open(os.path.join(od, "verify-summary.json"), "w"), indent=1)
    if set(units) == set(cat.keys()):
        os.makedirs(os.path.join(OUT, "docs", course), exist_ok=True)
        open(os.path.join(OUT, "docs", course, "VERIFICATION_REPORT.md"), "w").write("\n".join(lines))
    print("TOTAL ERRORS", total)
    return total


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2:] or None) else 0)
