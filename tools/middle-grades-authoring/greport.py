"""Coverage, skill manifest and activity-compatibility reports for a built course.

Usage: python3 greport.py <courseId>
Reads question-banks/<course>/*.json (+ verify-summary.json) under MG_OUT and writes docs/<course>/:
  COVERAGE.md, COVERAGE.csv, ACTIVITY_COMPATIBILITY.md, SKILL_MANIFEST.json
Activity filters mirror worksheet-generator/menu/printables.js (PR.MODES) and the game adapters.
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gbuild

OUT = gbuild.OUT
LV = ["cp2", "cp1", "honors"]
LABEL = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}


def plain(s):
    return re.sub(r"\s+", " ", str(s))


def fam(q):
    m = re.search(r"family: ([^)]+)\)", q.get("sourceNotes", ""))
    return m.group(1) if m else "?"


def numval(a):
    m = re.fullmatch(r"(?:[A-Za-z]\s*=\s*)?([+-]?\d+(?:\.0+)?)", str(a).strip())
    return float(m.group(1)) if m else None


def activity_flags(q):
    fig = bool(q.get("diagram"))
    ans = q["answer"] if isinstance(q["answer"], str) else "; ".join(map(str, q["answer"]))
    p, f = plain(q["prompt"]), q["format"]
    sa_mc = f in ("short-answer", "multiple-choice")
    nv = numval(ans)
    return {
        "Showdown / worksheets / assessments / lesson plans / readiness check": True,
        "Flashcards (skill questions)": sa_mc,
        "Connect 4 / Tic-Tac-Toe / Picture Reveal (text-only MC)": f == "multiple-choice" and not fig,
        "Detective (MC)": f == "multiple-choice",
        "Escape Room numeric lock": nv is not None,
        "Escape Room cipher (integer 1–25)": nv is not None and nv == int(nv) and 1 <= nv <= 25,
        "Escape Room step-order (≥ 4 distinct steps)": len({s.lower() for s in q["solutionSteps"]}) >= 4,
        "Maze (MC; numbered rooms allowed for long prompts)": f == "multiple-choice" and len(plain(ans)) <= 14,
        "Color by Number (SA/MC, answer ≤ 30)": sa_mc and len(plain(ans)) <= 30,
        "Whodunnit (MC, answer ≤ 30)": f == "multiple-choice" and len(plain(ans)) <= 30,
        "Stations (SA/MC, answer ≤ 60)": sa_mc and len(plain(ans)) <= 60,
        "Partner Check (SA/MC, answer ≤ 40)": sa_mc and len(plain(ans)) <= 40,
        "Tarsia (MC, answer ≤ 12)": f == "multiple-choice" and len(plain(ans)) <= 12,
        "Error Analysis printable (authored error family)": fam(q).endswith("_error"),
        "Select-all": f == "select-all",
        "Open response (4 parts)": f == "open-response",
        "Diagram / graph": fig,
    }


def main(course):
    cat = gbuild.catalog(course)
    vs = json.load(open(os.path.join(OUT, "tools", "middle-grades-authoring", "out", course, "verify-summary.json")))
    ddir = os.path.join(OUT, "docs", course)
    os.makedirs(ddir, exist_ok=True)
    unit_rows, skill_rows, manifest = [], [], {"courseId": course, "units": []}
    act = defaultdict(lambda: defaultdict(Counter))
    totals = Counter()
    for ui, (uid, info) in enumerate(cat.items(), 1):
        bank = json.load(open(os.path.join(OUT, "question-banks", course, uid + ".json"), encoding="utf-8"))
        qs = bank["questions"]
        by = defaultdict(Counter)
        fams = defaultdict(set)
        fmt = defaultdict(Counter)
        for q in qs:
            by[q["skillId"]][q["level"]] += 1
            fams[(q["skillId"], q["level"])].add(fam(q).replace("_error", "").replace("_open", "").replace("_sel", ""))
            fmt[q["skillId"]][q["format"]] += 1
            for k, v in activity_flags(q).items():
                if v:
                    act[uid][q["level"]][k] += 1
        errs = vs["units"].get(uid, {}).get("errors", "n/a")
        lv = Counter(q["level"] for q in qs)
        unit_rows.append((ui, info["name"], uid, len(info["skills"]), lv["cp2"], lv["cp1"], lv["honors"], len(qs), "PASS" if errs == 0 else f"FAIL ({errs})"))
        totals.update({"skills": len(info["skills"]), "q": len(qs), **lv})
        mu = {"unitId": uid, "name": info["name"], "skills": []}
        for s in info["skills"]:
            c = by[s["id"]]
            nf = min(len(fams[(s["id"], l)]) for l in LV)
            skill_rows.append((uid, s["id"], s["name"], c["cp2"], c["cp1"], c["honors"], sum(c.values()), nf,
                               fmt[s["id"]]["short-answer"], fmt[s["id"]]["multiple-choice"], fmt[s["id"]]["select-all"] + fmt[s["id"]]["open-response"],
                               "PASS" if all(c[l] >= 12 for l in LV) and errs == 0 else "CHECK"))
            mu["skills"].append({"skillId": s["id"], "name": s["name"], "questions": dict(c)})
        manifest["units"].append(mu)
    L = [f"# {course} question-bank coverage", "",
         "Difficulty codes: `cp2` = Remedial, `cp1` = Standard, `honors` = Advanced. Validation = independent verifier (gverify.py) result for the unit.", "",
         "| Unit | Unit ID | Skills | CP2 (Remedial) | CP1 (Standard) | Honors (Advanced) | Total | Validation |", "|---|---|---:|---:|---:|---:|---:|---|"]
    L += [f"| {u}. {n} | `{i}` | {s} | {a} | {b} | {c} | {t} | {v} |" for u, n, i, s, a, b, c, t, v in unit_rows]
    L += [f"| **Total** | | **{totals['skills']}** | **{totals['cp2']}** | **{totals['cp1']}** | **{totals['honors']}** | **{totals['q']}** | |", "",
          "## Skill-by-skill coverage", "",
          "Families = distinct problem families (structures) available at the least-covered level; SA/MC/Extra = short-answer, multiple-choice, select-all + open-response counts.", "",
          "| Unit | Skill ID | Skill | CP2 | CP1 | Honors | Total | Families (min/level) | SA | MC | Extra | Status |", "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    L += [f"| `{u}` | `{i}` | {n} | {a} | {b} | {c} | {t} | {f} | {sa} | {mc} | {ex} | {st} |" for u, i, n, a, b, c, t, f, sa, mc, ex, st in skill_rows]
    open(os.path.join(ddir, "COVERAGE.md"), "w").write("\n".join(L) + "\n")
    with open(os.path.join(ddir, "COVERAGE.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["unitId", "skillId", "skill", "cp2", "cp1", "honors", "total", "min_families_per_level", "short_answer", "multiple_choice", "select_all_or_open", "status"])
        w.writerows(skill_rows)
    json.dump(manifest, open(os.path.join(ddir, "SKILL_MANIFEST.json"), "w"), indent=1, ensure_ascii=False)
    keys = list(activity_flags({"prompt": "", "answer": "", "format": "short-answer", "solutionSteps": ["a"]}).keys())
    A = [f"# {course} activity compatibility", "",
         "Counts of questions eligible for each activity by unit and level, using the same limits as the site's printables and game adapters.",
         "The end-to-end build results in VALIDATION_LOG.txt come from running the site's own generators on these banks.", ""]
    for uid in cat:
        A += [f"## {cat[uid]['name']} (`{uid}`)", "", "| Activity | Remedial | Standard | Advanced |", "|---|---:|---:|---:|"]
        A += [f"| {k} | {act[uid]['cp2'][k]} | {act[uid]['cp1'][k]} | {act[uid]['honors'][k]} |" for k in keys]
        A.append("")
    rd = vs.get("readiness", {})
    gaps = defaultdict(list)
    for k, v in rd.items():
        for need_ in ("cipher", "steps4", "mc_text"):
            if not v.get(need_):
                gaps[need_].append(k)
    A += ["## Per-skill readiness gaps", "",
          f"- Skill/levels with no bank item whose answer is an integer 1–25 (Escape Room falls back to the unit-aligned generator in `games/cipher-questions.js`, which already covers every {course} unit): {len(gaps['cipher'])} of {len(rd)}.",
          f"- Skill/levels with no solution of ≥ 4 distinct steps (step-order room): {len(gaps['steps4'])}.",
          f"- Skill/levels with no text-only multiple-choice item (Connect 4 / Tic-Tac-Toe / Picture Reveal): {len(gaps['mc_text'])}" + (": " + ", ".join(gaps["mc_text"]) if gaps["mc_text"] else "."), ""]
    open(os.path.join(ddir, "ACTIVITY_COMPATIBILITY.md"), "w").write("\n".join(A))
    print("\n".join(L[:len(unit_rows) + 7]))


if __name__ == "__main__":
    main(sys.argv[1])
