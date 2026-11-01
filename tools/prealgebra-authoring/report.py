"""Coverage and activity-compatibility reports for the Grade 8 banks.

Writes docs/prealgebra/COVERAGE.csv, ACTIVITY_COMPATIBILITY.csv and COMPATIBILITY_SUMMARY.md.
Activity limits are copied from the existing consumers (not new rules):
  worksheet-generator/menu/printables.js PR.MODES (maze/tarsia/color/partner/who/stations),
  worksheet-generator/algebra2-bank-native.js GB.buildDeck (games: MC; flashcards: SA+MC; showdown: all),
  approved-game-items.js (Connect 4 / Tic-Tac-Toe / Picture Reveal: text-only SA/MC; diagrams excluded).
The 'plain' length is an approximation of the printables' plain() text length."""
import csv, json, os, re
from collections import Counter, defaultdict
import vm_catalog

ROOT = os.environ.get("PA8_OUT", "/home/claude/work/pkg")
UNITS = ["real-numbers-exponents", "equations-expressions", "linear-functional-relationships", "systems-linear-equations",
         "patterns-bivariate-data", "congruence-similarity", "geometry-applications"]
LABEL = {"cp2": "Remedial", "cp1": "Standard", "honors": "Advanced"}
MODES = {"maze": (92, 14, False, True), "tarsia": (22, 12, False, True), "color": (170, 30, True, False), "partner": (170, 40, True, False),
         "who": (150, 30, True, True), "stations": (260, 60, True, False)}
VERB = re.compile(r"^(Solve|Simplify|Factor|Evaluate)\b")


def plain(s):
    return re.sub(r"\s+", " ", str(s)).strip()


def compat(q, pair_ok):
    fmt, fig = q["format"], bool(q.get("diagram"))
    ans = q["answer"] if isinstance(q["answer"], str) else ""
    out = {}
    for k, (pl, al, fig_ok, needs_mc) in MODES.items():
        ok = fmt in ("multiple-choice",) if needs_mc else fmt in ("short-answer", "multiple-choice")
        ok = ok and (fig_ok or not fig) and len(plain(q["prompt"])) <= pl and len(plain(ans)) <= al and ans
        if k == "maze":
            ok = ok and plain(ans).count(",") <= 2
        if k == "tarsia":
            ok = ok and bool(VERB.match(q["prompt"]))
        if k == "partner":
            ok = ok and pair_ok
        out[k] = bool(ok)
    out["games_c4_ttt_reveal"] = fmt == "multiple-choice" and not fig   # bank-native decks use MC; approved-game-items also excludes diagrams
    out["flashcards"] = fmt in ("short-answer", "multiple-choice")
    out["showdown"] = True
    out["worksheets_tests_planner"] = True
    out["readiness_check_autograde"] = fmt == "multiple-choice"
    out["error_analysis_printable"] = False   # requires generator steps marked with s.m; authored banks only have {t} steps
    return out


def main():
    cov_rows, comp_rows = [], []
    summ = defaultdict(Counter)
    for u in UNITS:
        bank = json.load(open(os.path.join(ROOT, "question-banks", "prealgebra", u + ".json"), encoding="utf-8"))
        checks = json.load(open(os.path.join(ROOT, "tools", "prealgebra-authoring", "out", u + ".checks.json"), encoding="utf-8"))
        tags = json.load(open(os.path.join(ROOT, "question-banks", "prealgebra", "meta", u + ".tags.json"), encoding="utf-8"))
        recs = {r["id"]: r for r in vm_catalog.records("prealgebra", u)}
        groups = defaultdict(set)
        for q in bank["questions"]:
            if q["format"] in ("short-answer", "multiple-choice") and isinstance(q["answer"], str):
                groups[(q["level"], re.sub(r"^[a-z]\s*=\s*", "", q["answer"].lower().replace(" ", "")))].add(q["prompt"])
        agg = defaultdict(lambda: [0, set()])
        for q in bank["questions"]:
            key = (q["skillId"], q["level"], q["format"])
            agg[key][0] += 1
            agg[key][1].add(checks[q["id"]]["family"])
            pk = (q["level"], re.sub(r"^[a-z]\s*=\s*", "", str(q["answer"]).lower().replace(" ", "")))
            c = compat(q, len(groups.get(pk, ())) > 1)
            comp_rows.append([u, q["id"], q["skillId"], LABEL[q["level"]], q["format"], "yes" if q.get("diagram") else "no",
                              ";".join(tags.get(q["id"], []))] + ["yes" if c[k] else "no" for k in sorted(c)])
            for k, v in c.items():
                summ[u][k] += v
            summ[u]["questions"] += 1
            summ[u]["error-analysis tagged"] += "error-analysis" in tags.get(q["id"], [])
        for (sid, lv, fmt), (n, fams) in sorted(agg.items(), key=lambda kv: (recs[kv[0][0]]["index"], ["cp2", "cp1", "honors"].index(kv[0][1]), kv[0][2])):
            cov_rows.append([u, sid, recs[sid]["name"], LABEL[lv], lv, fmt, n, len(fams)])
        # all-format family count per skill/level
    d = os.path.join(ROOT, "docs", "prealgebra")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "COVERAGE.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["unit", "skill_id", "skill_name", "difficulty", "internal_level", "format", "question_count", "problem_family_count"])
        w.writerows(cov_rows)
    keys = sorted(compat({"format": "short-answer", "answer": "", "prompt": ""}, False))
    with open(os.path.join(d, "ACTIVITY_COMPATIBILITY.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["unit", "question_id", "skill_id", "difficulty", "format", "diagram", "tags"] + keys)
        w.writerows(comp_rows)
    lines = ["# Activity compatibility summary (counts of questions)", "",
             "Derived from the limits in the existing consumers; see report.py header. 'partner' requires another question in the same unit and level with the same answer.", "",
             "| unit | questions | " + " | ".join(keys) + " | error-analysis tagged |", "|---|---:|" + "---:|" * (len(keys) + 1)]
    for u in UNITS:
        lines.append(f"| {u} | {summ[u]['questions']} | " + " | ".join(str(summ[u][k]) for k in keys) + f" | {summ[u]['error-analysis tagged']} |")
    tot = Counter()
    for u in UNITS:
        tot.update(summ[u])
    lines.append(f"| **total** | {tot['questions']} | " + " | ".join(str(tot[k]) for k in keys) + f" | {tot['error-analysis tagged']} |")
    open(os.path.join(d, "COMPATIBILITY_SUMMARY.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    # per skill/level totals and family counts
    sk = defaultdict(lambda: [0, set(), Counter()])
    for u in UNITS:
        checks = json.load(open(os.path.join(ROOT, "tools", "prealgebra-authoring", "out", u + ".checks.json")))
        for q in json.load(open(os.path.join(ROOT, "question-banks", "prealgebra", u + ".json")))["questions"]:
            e = sk[(q["skillId"])]
            e[0] += 1
            e[1].add(checks[q["id"]]["family"])
            e[2][q["level"]] += 1
    mins = min(v[0] for v in sk.values())
    fam_min = min(len(v[1]) for v in sk.values())
    lvl_min = min(min(v[2].values()) for v in sk.values())
    print("skills", len(sk), "min questions per skill", mins, "min per skill-level", lvl_min, "min families per skill", fam_min)


if __name__ == "__main__":
    main()
