#!/usr/bin/env python3
"""Build the four expanded Statistics banks.

Usage:
  python3 scripts/authoring/build_expanded_banks.py <reference_pack_dir> <output_root>

Reads the 275-question baseline from <reference_pack_dir>/question-banks/statistics/,
applies the recorded corrections (CORRECTIONS below), appends the new authored items,
writes <output_root>/question-banks/statistics/<unit>.json, PNG assets to
<output_root>/question-banks/assets/statistics/, and the verification sidecar to
<output_root>/scripts/verification/checks.json.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REF, OUT = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(OUT, "question-banks", "statistics"), exist_ok=True)
os.makedirs(os.path.join(OUT, "question-banks", "assets", "statistics"), exist_ok=True)
os.makedirs(os.path.join(OUT, "scripts", "verification"), exist_ok=True)

import plots
plots.OUT = os.path.join(OUT, "question-banks", "assets", "statistics")
import common as C
import u1, u2, u3, u4, u5_topup, u6_breadth, u7_tarsia, u8_partner_error_b, u9_escape, u10_mc

for m in (u1, u2, u3, u4, u5_topup, u6_breadth, u7_tarsia, u8_partner_error_b, u9_escape, u10_mc):
    m.build()

# Corrections to baseline items: the normalized open responses carried rubric
# criteria in place of part answers ("See rubric." at the top level).
CORRECTIONS = {
    "stat-u1-t1-046": (["Period 2: 38, 44.5, 49.5, 54, 62; Period 5: 35, 41, 45, 54, 96 (common scale about 30–100 seconds)",
                        "Period 2 fences 30.25 and 68.25: no outliers. Period 5 fences 21.5 and 73.5: 96 is an outlier and is plotted separately",
                        "Period 2 is roughly symmetric; Period 5 is skewed right with a high outlier. Period 5 has a lower median (45 vs 49.5 s) and a larger IQR (13 vs 9.5 s)",
                        "Period 5, because its median time (45 s) is lower; the median is appropriate because Period 5 is skewed with an outlier"], None),
    "stat-u1-t3-031": (["Strong, positive, linear association between shoe size and height with no clear outliers (r ≈ 0.995)",
                        "ŷ ≈ 48.09 + 2.072x; each 1-size increase in shoe size is associated with about a 2.07-inch increase in predicted height",
                        "Yes, if the residual plot shows random scatter around 0 with no curved pattern",
                        "ŷ ≈ 48.09 + 2.072(11.5) ≈ 71.9 in; it is only a prediction (typical error about s), and one class may not represent the population the thief comes from"], None),
    "stat-u2-t1-019": (["Number the students 1–22,000 and use a random number generator to select 500 different numbers (ignore repeats); survey those students",
                        "Separate the students by class year and take an SRS from each year (for example 125 per year, or proportional to class size)",
                        "Spending is likely similar within a class year but different between years, so stratifying reduces the variability of the estimate",
                        "Voluntary response/nonresponse bias: early responders may differ (e.g., more engaged students who buy more books), so the mean could be overestimated"],
                       "(a) SRS by labels and random numbers; (b) SRS within each class year; (c) less variability because strata are internally similar; (d) voluntary response bias with a stated direction"),
    "stat-u2-t2-023": (["Randomly assign 25 of the 50 volunteers to the new formula and 25 to the old (e.g., numbered slips drawn from a hat); compare hair-quality ratings",
                        "Block by gender: randomly assign 15 women to each formula and 10 men to each formula; compare formulas within each block",
                        "Gender is expected to affect the response, so comparing within blocks removes that variability and makes a formula difference easier to detect",
                        "Random assignment allows a cause-and-effect conclusion about the formulas, but without random selection the results apply only to volunteers like these"],
                       "(a) completely randomized 25/25; (b) block by gender, randomize within; (c) blocking reduces variability due to gender; (d) causal conclusion for similar volunteers only"),
    "stat-u3-t1-023": (["Bus 0.60 (late 0.25, not late 0.35); No bus 0.40 (late 0.06, not late 0.34)", "P(late) = 0.25 + 0.06 = 0.31",
                        "P(bus | late) = 0.25/0.31 ≈ 0.806", "Not independent: P(late | bus) = 0.25/0.60 ≈ 0.417 ≠ P(late) = 0.31"], None),
    "stat-u3-t2-028": (["E(X) = 1.95; over many weekdays the dealership averages about 1.95 cars sold per day", "σ_X = √1.2475 ≈ 1.117",
                        "Mean $1,075; SD = 500(1.117) ≈ $558.5", "Mean 2.95; SD = √(1.2475 + 1) ≈ 1.499, assuming X and Y are independent"], None),
    "stat-u4-t1-023": (["Random sample; 1,200 is less than 10% of all U.S. adults; 504 successes and 696 failures are both at least 10",
                        "0.42 ± 1.96√(0.42·0.58/1200) = 0.42 ± 0.028 → (0.392, 0.448); we are 95% confident the interval captures the proportion of all U.S. adults who say major changes are needed",
                        "If many random samples were taken and an interval built from each, about 95% of the intervals would capture the true proportion",
                        "Yes: every plausible value in the interval is below 0.5"], None),
    "stat-u4-t2-023": (["H₀: μ = 29 vs Hₐ: μ > 29, where μ is the true mean lifetime (hours) of the new batteries; α = 0.05",
                        "One-sample t test. Random: SRS. 10%: 15 < 10% of all batteries. Normal: n < 30 but the data show no strong skew or outliers",
                        "x̄ ≈ 30.36 h, sₓ ≈ 1.547 h, t ≈ 3.41, df = 14, P-value ≈ 0.0021",
                        "Because 0.0021 < 0.05, reject H₀: convincing evidence the mean lifetime exceeds 29 hours. A Type I error would be concluding the mean exceeds 29 hours when it actually does not"],
                       "(a) H₀: μ = 29, Hₐ: μ > 29; (b) one-sample t, conditions met; (c) t ≈ 3.41, df 14, P ≈ 0.0021; (d) reject H₀; Type I error described"),
    "stat-u4-t3-013": (["p̂_CC = 46/520 ≈ 0.088; p̂_CPR = 27/535 ≈ 0.050",
                        "Random assignment; 46, 474, 27, 508 are all at least 10. (0.0885 − 0.0505) ± 1.96(0.0156) → (0.007, 0.069)",
                        "We are 95% confident the interval from 0.007 to 0.069 captures the true difference in survival rates (CC − CPR); 95% of intervals made this way capture the true difference",
                        "Yes: the entire interval is above 0, so CC instructions appear to give a higher survival rate"],
                       "(a) 0.088 and 0.050; (b) conditions met, (0.007, 0.069); (c) interpretation in context; (d) yes, 0 is not in the interval"),
}
CORRECTION_LOG = []

units = ["exploring-data", "sampling-experimentation", "anticipating-patterns", "statistical-inference"]
summary = {}
for u in units:
    bank = json.load(open(os.path.join(REF, "question-banks", "statistics", u + ".json"), encoding="utf-8"))
    for q in bank["questions"]:
        if q["id"] in CORRECTIONS:
            answers, top = CORRECTIONS[q["id"]]
            assert len(answers) == len(q["parts"])
            for p, a in zip(q["parts"], answers):
                p["answer"] = a
            if top:
                q["answer"] = top
            CORRECTION_LOG.append(q["id"] + ": part answers replaced (were rubric criteria)" + ("; top-level answer replaced (was 'See rubric.')" if top else ""))
    base = len(bank["questions"])
    bank["questions"].extend(C.ITEMS[u])
    with open(os.path.join(OUT, "question-banks", "statistics", u + ".json"), "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)
        f.write("\n")
    summary[u] = (base, len(C.ITEMS[u]))

with open(os.path.join(OUT, "scripts", "verification", "checks.json"), "w", encoding="utf-8") as f:
    json.dump(C.CHECKS, f, ensure_ascii=False, indent=1)
with open(os.path.join(OUT, "scripts", "verification", "corrections.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(CORRECTION_LOG) + "\n")
for u, (b, n) in summary.items():
    print(f"{u}: baseline {b} + new {n} = {b + n}")
print("checks:", len(C.CHECKS), "images:", len(plots.DRAWN), "corrections:", len(CORRECTION_LOG))
