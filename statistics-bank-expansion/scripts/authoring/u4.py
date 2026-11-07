from common import *

U = "statistical-inference"
EA, TB = "APSTATS.IV.A", "APSTATS.IV.B"


def iv(lo, hi, d=3):
    return f"({fmt(lo, d)}, {fmt(hi, d)})"


def mcs(k, level, rows, fam, std):
    for prompt, correct, wrongs, steps in rows:
        MC(U, k, level, prompt, correct, wrongs, steps, family=fam, std=std)


def ttail(t, df, alt):
    return {"gt": float(st.t.sf(t, df)), "lt": float(st.t.cdf(t, df)), "ne": float(2 * st.t.sf(abs(t), df))}[alt]


def ztail(z, alt):
    return {"gt": 1 - Phi(z), "lt": Phi(z), "ne": 2 * (1 - Phi(abs(z)))}[alt]


SYM = {"gt": ">", "lt": "<", "ne": "≠"}


def s01():
    k, sd_ = 1, [EA + ".1", EA + ".2"]
    for lv, x, n, ctx in [("cp2", 132, 400, "In a random sample of 400 teens, 132 said they read for fun weekly."),
                          ("cp2", 57, 150, "A random sample of 150 cars at a mall showed 57 were silver or gray.")]:
        ph = x / n
        se = math.sqrt(ph * (1 - ph) / n)
        SA(U, k, lv, ctx + " Find the point estimate p̂ and its standard error (four decimals).", f"p̂ = {fmt(ph, 4)}, SE ≈ {fmt(se, 4)}",
           [f"p̂ = {x}/{n} = {fmt(ph, 4)}.", f"SE = √(p̂(1 − p̂)/n) = √({fmt(ph, 4)}·{fmt(1 - ph, 4)}/{n}) ≈ {fmt(se, 4)}."],
           family="u4_point_se", std=sd_, check={"kind": "phat_se", "x": x, "n": n})
    MC(U, k, "cp2", "A 95% confidence interval for a population mean is (42.6, 48.2). What are the point estimate and the margin of error?",
       "Point estimate 45.4; margin of error 2.8", ["Point estimate 45.4; margin of error 5.6", "Point estimate 42.6; margin of error 48.2", "Point estimate 2.8; margin of error 45.4"],
       ["Point estimate = midpoint = (42.6 + 48.2)/2 = 45.4.", "Margin of error = half the width = (48.2 − 42.6)/2 = 2.8."], family="u4_me_from_ci", std=sd_,
       check={"kind": "me_from_ci", "lo": 42.6, "hi": 48.2, "skip_distractors": True})
    SA(U, k, "cp2", "A poll reports that 38% of adults favor a proposal, with a margin of error of 4 percentage points. Write the confidence interval as an interval of percents.", "34% to 42%",
       ["Interval = estimate ± margin of error.", "38% − 4% = 34%; 38% + 4% = 42%."], family="u4_interval_from_me", std=sd_)
    mcs(k, "cp2", [
        ("A confidence interval is built as",
         "point estimate ± margin of error", ["parameter ± statistic", "sample size ± standard deviation", "margin of error ± sample size"],
         ["Statistic ± (critical value)(standard error)."]),
        ("Which is a point estimate of the population mean μ?",
         "The sample mean x̄", ["The population SD σ", "The sample size n", "The margin of error"], ["x̄ is the single best guess for μ."]),
        ("The standard error of a statistic estimates",
         "how much the statistic typically varies from sample to sample", ["the error caused by bias", "the size of the population", "the difference between two samples' sizes"],
         ["SE is an estimate of the SD of the sampling distribution."]),
    ], "u4_ci_vocab", sd_)
    SEL(U, k, "cp2", "Select ALL statements that are true for a confidence interval for a proportion.",
        ["The interval is centered at p̂.", "The margin of error is the critical value times the standard error."],
        ["The interval is centered at p.", "The margin of error accounts for bias from a bad sample."],
        ["The interval is built around the sample statistic; ME covers sampling variability only."], family="u4_ci_sel", std=sd_)
    for lv, ph, n, c in [("cp1", 0.62, 500, 95), ("cp1", 0.18, 900, 99)]:
        se = math.sqrt(ph * (1 - ph) / n)
        me = ZSTAR[c] * se
        num_mc(U, k, lv, f"A random sample of {n} gives p̂ = {fmt(ph)}. Find the margin of error for a {c}% confidence interval (four decimals).", me,
               [se, ZSTAR[90 if c != 90 else 95] * se, ZSTAR[c] * ph * (1 - ph) / n], 4,
               [f"SE = √({fmt(ph)}·{fmt(1 - ph)}/{n}) ≈ {fmt(se, 5)}.", f"z* = {ZSTAR[c]}.", f"ME = {ZSTAR[c]}({fmt(se, 5)}) ≈ {fmt(me, 4)}."],
               family="u4_me_calc", std=sd_, check={"kind": "ci_prop_parts", "x": ph * n, "n": n, "conf": c, "verify_only": True, "expect": [ph, se, me], "tol": 1e-9})
    mcs(k, "cp1", [
        ("Two random samples from the same population give 95% intervals (0.41, 0.49) and (0.43, 0.47). What is the most likely explanation for the difference in width?",
         "The second sample was larger.", ["The second interval used a higher confidence level.", "The first sample was biased.", "The second sample had a larger p̂ near 0.5."],
         ["With the same confidence level, a narrower interval comes from a smaller SE, usually from a larger n."]),
        ("Which change increases the margin of error of a confidence interval for a proportion (other things equal)?",
         "Increasing the confidence level from 90% to 99%", ["Increasing the sample size", "Moving p̂ farther from 0.5", "Using a random sample instead of a convenience sample"],
         ["Higher confidence → larger z* → larger ME."]),
    ], "u4_me_factors", sd_)
    mcs(k, "honors", [
        ("A researcher reports a 95% CI for μ of (18.2, 23.8) from n = 25. If she had used n = 100 with a similar sample SD, the new interval would be about",
         "half as wide", ["one-fourth as wide", "twice as wide", "the same width"], ["Width ∝ 1/√n (with t* also slightly smaller); √4 = 2."]),
        ("A point estimator is unbiased with large variability, and another is slightly biased with very small variability. When might the biased estimator be preferred?",
         "When its typical distance from the parameter (bias plus spread) is smaller than the unbiased estimator's.", ["Never; unbiased estimators are always better.", "Only when the sample size is 1.", "When the parameter is unknown."],
         ["Good estimators have low bias AND low variability; overall accuracy matters."]),
    ], "u4_estimator_honors", sd_)
    SA(U, k, "honors", "A 90% confidence interval for p is (0.512, 0.588) from a random sample of n = 450. Find p̂ and the standard error used, then find the 99% interval from the same data (three decimals).",
       f"p̂ = 0.55; SE ≈ {fmt(0.038 / 1.645, 4)}; 99% CI ≈ {iv(0.55 - 2.576 * 0.038 / 1.645, 0.55 + 2.576 * 0.038 / 1.645)}",
       ["p̂ = midpoint = (0.512 + 0.588)/2 = 0.550.", "ME = 0.038 = 1.645·SE → SE = 0.038/1.645 ≈ 0.0231.", "99%: ME = 2.576 × 0.0231 ≈ 0.0595.", f"Interval ≈ {iv(0.55 - 2.576 * 0.038 / 1.645, 0.55 + 2.576 * 0.038 / 1.645)}."],
       family="u4_rescale_ci", std=sd_, check={"kind": "me_from_ci", "lo": 0.512, "hi": 0.588, "verify_only": True, "expect": [0.55, 0.038]})
    OR(U, k, "honors", "A random sample of 250 employees at a large company found that 85 work remotely at least once a week.",
       [("Identify the parameter of interest and the point estimate.", "p = proportion of all the company's employees who work remotely weekly; p̂ = 85/250 = 0.34"),
        ("Compute the standard error of p̂ (four decimals).", f"SE ≈ {fmt(math.sqrt(0.34 * 0.66 / 250), 4)}"),
        ("Compute the margin of error for 95% confidence (four decimals).", f"ME ≈ {fmt(1.96 * math.sqrt(0.34 * 0.66 / 250), 4)}"),
        ("Explain what the margin of error does NOT account for.", "Bias from undercoverage, nonresponse, or response errors; it covers only random sampling variability")],
       ["1 point each part."], family="u4_ci_parts_or", std=sd_, check={"kind": "ci_prop_parts", "x": 85, "n": 250, "conf": 95})


def s02():
    k, sd_ = 2, [EA + ".3", EA + ".4"]
    mcs(k, "cp2", [
        ("A 90% confidence interval for the mean weight of apples in an orchard is (148 g, 156 g). Which interpretation is correct?",
         "We are 90% confident the interval from 148 g to 156 g captures the true mean weight of all apples in the orchard.", ["90% of apples weigh between 148 g and 156 g.", "There is a 90% chance the sample mean is between 148 and 156 g.", "The true mean is 152 g."],
         ["Interpret about the parameter (true mean), in context."]),
        ("What does “95% confidence” describe?",
         "The method: about 95% of intervals built this way from repeated random samples would capture the parameter.", ["The chance the parameter changes.", "The percent of data in the interval.", "The percent of the population that was sampled."],
         ["Confidence level = long-run capture rate of the method."]),
        ("Which condition checks that the sampling distribution of p̂ is approximately Normal?",
         "Large counts: n·p̂ ≥ 10 and n(1 − p̂) ≥ 10", ["The 10% condition", "Random assignment", "The population is Normal"],
         ["The large counts condition supports the Normal approximation for p̂."]),
        ("Why do we check the 10% condition?",
         "To make sure observations are approximately independent when sampling without replacement.", ["To make sure the sample is random.", "To make sure p̂ is close to 0.5.", "To make the interval narrower."],
         ["n ≤ 10% of N keeps the SD formula accurate."]),
    ], "u4_interpret_basic", sd_)
    SA(U, k, "cp2", "A random sample of 80 students from a school of 1,400 found 26 who play an instrument. Check the Random, 10%, and Large Counts conditions for a confidence interval for p.",
       "Random: random sample. 10%: 80 < 140 (10% of 1,400). Large Counts: 26 and 54 are both at least 10. All conditions are met.",
       ["Random: stated random sample.", "10%: 10% of 1,400 = 140; 80 < 140.", "Large Counts: successes 26, failures 80 − 26 = 54, both ≥ 10."],
       family="u4_check_conditions", std=sd_)
    SEL(U, k, "cp2", "A 95% confidence interval for the proportion of voters who support a measure is (0.47, 0.55). Select ALL reasonable conclusions.",
        ["0.50 is a plausible value for the true proportion.", "We cannot be confident a majority supports the measure."],
        ["We are sure a majority supports the measure.", "95% of voters are between 47% and 55%."],
        ["Values inside the interval are plausible; since it includes values below and above 0.5, a majority is not established."], family="u4_ci_plausible_sel", std=sd_)
    mcs(k, "cp1", [
        ("A student says, “There is a 95% probability that the true mean is between 12.1 and 14.3.” What is wrong with this statement?",
         "After the interval is computed, the true mean is either in it or not; 95% describes the long-run success rate of the method.", ["Nothing is wrong.", "It should say 5% instead of 95%.", "The interval should be centered at the true mean."],
         ["Confidence describes the procedure, not a probability about this one fixed interval."]),
        ("A survey of 40 volunteers produced a 95% CI for the mean hours of sleep. Which condition is most clearly violated?",
         "Random sampling (volunteers are not a random sample)", ["10% condition", "The sample size is too large", "Large counts"],
         ["Without random selection, the interval may not describe the population."]),
        ("Data on 12 students' commute times show strong right skew and an outlier. Can a one-sample t interval be used safely?",
         "No; with n < 15, strong skew and outliers make t procedures unreliable.", ["Yes; t procedures are always robust.", "Yes, because n is at least 10.", "No, because σ is unknown."],
         ["For small n, the Normal/Large Sample condition requires no strong skew or outliers."]),
    ], "u4_conditions_cp1", sd_)
    SA(U, k, "cp1", "A 99% confidence interval for the proportion of defective parts is (0.021, 0.059). A manager claims the defect rate is 8%. Is the claim plausible? What about 4%?",
       "8% is not plausible (outside the interval); 4% is plausible (inside the interval).", ["Plausible values are those inside the interval.", "0.08 > 0.059, so 8% is not plausible.", "0.04 is between 0.021 and 0.059, so it is plausible."],
       family="u4_plausible", std=sd_)
    mcs(k, "honors", [
        ("If 100 different random samples each produce a 90% confidence interval for p, how many intervals would you expect to miss p?",
         "About 10", ["Exactly 10", "About 90", "None"], ["About 10% of 90% intervals miss the parameter, though the exact count varies."]),
        ("A researcher wants an interval that is narrower without reducing the confidence level. What can she do?",
         "Increase the sample size", ["Use a lower confidence level", "Use a nonrandom sample", "Report the point estimate only"],
         ["ME = z*·SE and SE shrinks as n grows."]),
        ("A 95% CI for a mean is (31.2, 36.4). A second researcher using the same data reports a 90% CI. Which interval could be hers?",
         "(31.6, 36.0)", ["(30.5, 37.1)", "(31.2, 36.4)", "(32.0, 37.2)"],
         ["A 90% interval from the same data has the same center (33.8) and is narrower.", "Only (31.6, 36.0) is centered at 33.8 and narrower."]),
    ], "u4_conf_honors", sd_)
    OR(U, k, "honors", "A random sample of 64 bags of chips had mean weight 28.6 g and SD 1.6 g. The label says 28.35 g. A 95% CI for μ is (28.20, 29.00).",
       [("Interpret the interval in context.", "We are 95% confident the interval from 28.20 to 29.00 g captures the true mean weight of all bags"),
        ("Interpret the confidence level.", "In repeated random samples of 64 bags, about 95% of intervals made this way would capture the true mean"),
        ("Does the interval give convincing evidence that the mean differs from the labeled 28.35 g? Explain.", "No; 28.35 g is inside the interval, so it is a plausible value"),
        ("Explain why the Normal/Large Sample condition is met even if bag weights are not Normal.", "n = 64 ≥ 30, so by the CLT the sampling distribution of x̄ is approximately Normal")],
       ["1 point each part."], family="u4_interpret_or", std=sd_, check={"kind": "ci_mean", "xbar": 28.6, "s": 1.6, "n": 64, "conf": 95, "tol": 0.01})


def s03():
    k, sd_ = 3, [EA + ".4"]
    for lv, x, n, c, ctx in [("cp2", 270, 600, 95, "In a random sample of 600 adults, 270 said they have a library card."),
                             ("cp2", 64, 200, 90, "In a random sample of 200 students, 64 said they skipped breakfast today."),
                             ("cp1", 418, 1100, 99, "In a random sample of 1,100 voters, 418 favored a new tax."),
                             ("cp1", 91, 350, 95, "A random sample of 350 smartphones showed 91 had a cracked screen.")]:
        ph = x / n
        me = ZSTAR[c] * math.sqrt(ph * (1 - ph) / n)
        key = iv(ph - me, ph + me)
        wr = [iv(ph - m, ph + m) for m in (math.sqrt(ph * (1 - ph) / n), ZSTAR[90 if c != 90 else 99] * math.sqrt(ph * (1 - ph) / n), ZSTAR[c] * ph * (1 - ph) / math.sqrt(n), 2 * me, ZSTAR[c] * math.sqrt(0.25 / n) * 1.5)]
        MC(U, k, lv, ctx + f" Construct a {c}% confidence interval for the population proportion (three decimals). Conditions have been checked.", key, wr,
           [f"p̂ = {x}/{n} = {fmt(ph, 4)}.", f"SE = √(p̂(1 − p̂)/n) ≈ {fmt(math.sqrt(ph * (1 - ph) / n), 5)}; z* = {ZSTAR[c]}.", f"{fmt(ph, 4)} ± {fmt(me, 4)} → {key}."],
           family="u4_ci_prop", std=sd_, check={"kind": "ci_prop", "x": x, "n": n, "conf": c})
    SA(U, k, "cp2", "A city planner wants a 95% confidence interval for the proportion of residents who bike, with margin of error at most 0.05. With no prior estimate, how many residents should be surveyed?",
       "385", ["Use p̂ = 0.5 (largest SE).", "n ≥ (1.96/0.05)² × 0.25 = 384.16.", "Round up: n = 385.", "Always round up so the margin of error is at most 0.05."],
       family="u4_sample_size", std=sd_, check={"kind": "samp_size", "conf": 95, "me": 0.05, "p": 0.5})
    MC(U, k, "cp2", "Which z* value is used for a 90% confidence interval?", "1.645", ["1.96", "2.576", "1.282"], ["The middle 90% of the standard Normal is between −1.645 and 1.645."], family="u4_zstar", std=sd_)
    MC(U, k, "cp2", "Why do we use p̂ = 0.5 when planning a sample size with no prior estimate?",
       "It gives the largest value of p̂(1 − p̂), so the sample is large enough no matter the true p.", ["Because most proportions are 0.5.", "It makes the interval narrower.", "It is required by the 10% condition."],
       ["p(1 − p) is maximized at p = 0.5 (0.25)."], family="u4_conservative_p", std=sd_)
    SA(U, k, "cp1", "A previous study found that about 22% of shoppers use a store app. How many shoppers should be surveyed to estimate the proportion within 0.03 with 90% confidence?",
       "516", ["Use p* = 0.22.", "n ≥ (1.645/0.03)² × 0.22 × 0.78 ≈ 515.95.", "Round up: n = 516.", "Using 0.5 instead would require 752 shoppers."],
       family="u4_sample_size", std=sd_, check={"kind": "samp_size", "conf": 90, "me": 0.03, "p": 0.22})
    MC(U, k, "cp1", "To cut the margin of error of a confidence interval for p in half, the sample size must be about",
       "multiplied by 4", ["multiplied by 2", "divided by 2", "multiplied by 0.5"], ["ME ∝ 1/√n."], family="u4_half_me", std=sd_)
    OR(U, k, "honors", "A random sample of 900 adults found 513 who said they had used a streaming service in the past week.",
       [("Check the conditions for a confidence interval for p.", "Random sample; 900 < 10% of all adults; 513 and 387 both ≥ 10"),
        ("Construct a 98% confidence interval for p (three decimals).", iv(0.57 - 2.326 * math.sqrt(0.57 * 0.43 / 900), 0.57 + 2.326 * math.sqrt(0.57 * 0.43 / 900))),
        ("Interpret the interval in context.", "We are 98% confident the interval captures the proportion of all adults who used a streaming service in the past week"),
        ("Based on the interval, is it plausible that half of adults used a streaming service? Explain.", "No; 0.50 is below the interval, so a majority is supported")],
       ["1 point each part; z* = 2.326."], family="u4_ci_prop_or", std=sd_, check={"kind": "ci_prop", "x": 513, "n": 900, "conf": 98})
    SA(U, k, "honors", "A pollster wants a margin of error of at most 2 percentage points with 99% confidence. How many people are needed if no prior estimate is available? How many if a pilot study suggests p ≈ 0.10?",
       "4,148 with p = 0.5; 1,493 with p = 0.10",
       ["n ≥ (2.576/0.02)² × 0.25 = 4,147.4 → 4,148.", "n ≥ (2.576/0.02)² × 0.10 × 0.90 = 1,493.0 → 1,493 (round up if not an integer).", "A good prior estimate far from 0.5 reduces the sample needed.", "If the true p turns out nearer 0.5, the smaller sample would give a larger ME."],
       family="u4_sample_size_compare", std=sd_, check={"kind": "samp_size", "conf": 99, "me": 0.02, "p": 0.5})
    MC(U, k, "honors", "A random sample of 15 students includes 3 who are vegetarian. Why shouldn't a one-proportion z interval be used?",
       "The large counts condition fails (3 successes < 10), so p̂'s sampling distribution is not approximately Normal.", ["The sample is too large.", "Proportions cannot be estimated from 15 students.", "The 10% condition requires n ≥ 30."],
       ["Need at least 10 successes and 10 failures."], family="u4_large_counts_fail", std=sd_)
    SA(U, k, "honors", "Error analysis. A student computes a 95% CI for p with x = 45, n = 120 as: p̂ = 0.375; SE = √(0.375 × 0.625) = 0.484; interval = 0.375 ± 1.96(0.484). Identify and fix the error, and give the correct interval (three decimals).",
       f"The SE must divide by n: SE = √(0.375·0.625/120) ≈ 0.0442; interval ≈ {iv(0.375 - 1.96 * math.sqrt(0.375 * 0.625 / 120), 0.375 + 1.96 * math.sqrt(0.375 * 0.625 / 120))}",
       ["p̂ = 45/120 = 0.375 is correct.", "SE = √(p̂(1 − p̂)/n) — the student forgot to divide by n.", "SE ≈ 0.0442; ME = 1.96 × 0.0442 ≈ 0.0866.", f"Interval ≈ {iv(0.375 - 1.96 * math.sqrt(0.375 * 0.625 / 120), 0.375 + 1.96 * math.sqrt(0.375 * 0.625 / 120))}."],
       family="u4_se_error", std=sd_, check={"kind": "ci_prop", "x": 45, "n": 120, "conf": 95})


def s04():
    k, sd_ = 4, [EA + ".6"]
    for lv, c, df in [("cp2", 95, 9), ("cp2", 90, 19), ("cp1", 99, 29)]:
        t = tstar(c, df)
        num_mc(U, k, lv, f"Find t* for a {c}% confidence interval with df = {df} (three decimals).", t, [ZSTAR[c], tstar(c, df + 5), tstar({90: 95, 95: 99, 99: 90}[c], df)], 3,
               [f"Use the t table or invT(area, df) with upper-tail area {fmt((1 - c / 100) / 2)} and df = {df}.", f"t* ≈ {fmt(t, 3)}."], family="u4_tstar", std=sd_, check={"kind": "tstar", "conf": c, "df": df})
    MC(U, k, "cp2", "A random sample of 16 students is used to build a t interval for a mean. How many degrees of freedom?", "15", ["16", "14", "17"], ["df = n − 1 = 15."], family="u4_df", std=sd_)
    MC(U, k, "cp2", "Why do we use t* instead of z* for a confidence interval for μ?",
       "Because σ is unknown and estimated by sₓ, which adds variability; t accounts for it.", ["Because the sample is always small.", "Because the population is skewed.", "Because t* is always smaller."],
       ["Replacing σ with sₓ makes the standardized statistic follow a t distribution."], family="u4_why_t", std=sd_)
    for lv, xb, s, n, c, ctx in [("cp2", 7.4, 1.2, 25, 95, "A random sample of 25 students slept a mean of 7.4 hours with SD 1.2 hours (no strong skew)."),
                                 ("cp1", 52.3, 8.6, 40, 90, "A random sample of 40 commuters had mean commute 52.3 minutes with SD 8.6 minutes."),
                                 ("cp1", 212, 18, 12, 99, "Twelve randomly chosen cereal boxes had mean weight 212 g and SD 18 g; a dotplot shows no outliers.")]:
        t = tstar(c, n - 1)
        me = t * s / math.sqrt(n)
        key = iv(xb - me, xb + me, 2)
        wr = [iv(xb - m, xb + m, 2) for m in (ZSTAR[c] * s / math.sqrt(n), t * s / n, t * s)]
        MC(U, k, lv, ctx + f" Construct a {c}% confidence interval for μ (two decimals).", key, wr,
           [f"df = {n - 1}, t* ≈ {fmt(t, 3)}.", f"SE = {fmt(s)}/√{n} ≈ {fmt(s / math.sqrt(n), 4)}.", f"{fmt(xb)} ± {fmt(me, 3)} → {key}."],
           family="u4_t_interval", std=sd_ + [EA + ".6"], check={"kind": "ci_mean", "xbar": xb, "s": s, "n": n, "conf": c})
    SEL(U, k, "cp1", "Select ALL true statements about t distributions.",
        ["They are symmetric and centered at 0.", "They have more area in the tails than the standard Normal.", "As df increases, they approach the standard Normal."],
        ["They are skewed right for small df.", "t* is smaller than z* for the same confidence level."],
        ["Heavier tails make t* > z* for the same confidence."], family="u4_t_props_sel", std=sd_)
    data = [14, 17, 12, 19, 21, 15, 16, 18, 13, 20]
    m, s = sum(data) / 10, sd(data)
    t = tstar(95, 9)
    SA(U, k, "honors", f"A random sample of 10 bird watchers' identification scores: {lst(data)}. A dotplot shows no strong skew or outliers. Construct a 95% t interval for the mean score (two decimals), showing x̄, sₓ, and t*.",
       f"x̄ = {fmt(m, 1)}, sₓ ≈ {fmt(s, 3)}, t* ≈ {fmt(t, 3)}; CI ≈ {iv(m - t * s / math.sqrt(10), m + t * s / math.sqrt(10), 2)}",
       [f"x̄ = {fmt(sum(data))}/10 = {fmt(m, 1)}.", f"sₓ ≈ {fmt(s, 3)} (n − 1 = 9).", f"t* (df 9) ≈ {fmt(t, 3)}.", f"{fmt(m, 1)} ± {fmt(t, 3)}({fmt(s, 3)}/√10) → {iv(m - t * s / math.sqrt(10), m + t * s / math.sqrt(10), 2)}."],
       family="u4_t_interval_data", std=sd_, check={"kind": "ci_mean_data", "data": data, "conf": 95})
    MC(U, k, "honors", "With n = 8, a t interval is built from data with one extreme outlier. Which is the best action?",
       "Investigate the outlier; if it is a valid value, t procedures are not reliable, so report the issue (or use another method).", ["Ignore it; t procedures are robust for any data.", "Use z* instead of t*.", "Increase the confidence level."],
       ["t procedures are not resistant; small samples with outliers violate the Normal condition."], family="u4_t_outlier", std=sd_)
    SA(U, k, "honors", "How large a sample is needed to estimate a mean within ±2 units with 95% confidence if a pilot study suggests σ ≈ 9? (Use z* = 1.96 for planning.)",
       "78", ["n ≥ (z*σ/ME)² = (1.96 × 9/2)² = 77.79.", "Round up: n = 78.", "Using t* in practice would make the actual ME slightly larger than planned.", "A pilot estimate of σ is required for planning."],
       family="u4_sample_size_mean", std=sd_, check={"kind": "samp_size_mean", "conf": 95, "me": 2, "sigma": 9})
    OR(U, k, "honors", "A random sample of 18 smartphones' battery lives (hours): x̄ = 14.2, s = 2.5. A boxplot shows no outliers and mild symmetry.",
       [("Identify the procedure and check conditions.", "One-sample t interval; random sample; 18 < 10% of all phones; n < 30 but no outliers or strong skew"),
        ("Find df and t* for 95% confidence.", f"df = 17; t* ≈ {fmt(tstar(95, 17), 3)}"),
        ("Construct the 95% interval (two decimals).", iv(14.2 - tstar(95, 17) * 2.5 / math.sqrt(18), 14.2 + tstar(95, 17) * 2.5 / math.sqrt(18), 2)),
        ("The maker advertises 15 hours. Is that plausible? Explain.", "Yes, if 15 is inside the interval (it is: upper limit ≈ 15.44), so the claim is plausible")],
       ["1 point each part."], family="u4_t_or", std=sd_, check={"kind": "ci_mean", "xbar": 14.2, "s": 2.5, "n": 18, "conf": 95})


def s05():
    k, sd_ = 5, [TB + ".1"]
    rows_cp2 = [
        ("A school says 30% of students walk to school. A teacher thinks the true proportion is lower. Which hypotheses?", "H₀: p = 0.30; Hₐ: p < 0.30",
         ["H₀: p < 0.30; Hₐ: p = 0.30", "H₀: p̂ = 0.30; Hₐ: p̂ < 0.30", "H₀: p = 0.30; Hₐ: p > 0.30"]),
        ("A juice machine is supposed to fill bottles with 16 oz on average. An inspector wants to know if it is miscalibrated in either direction. Which hypotheses?", "H₀: μ = 16; Hₐ: μ ≠ 16",
         ["H₀: μ ≠ 16; Hₐ: μ = 16", "H₀: x̄ = 16; Hₐ: x̄ ≠ 16", "H₀: μ = 16; Hₐ: μ > 16"]),
        ("A coach believes a new drill increases the mean number of free throws made out of 20 (currently 12). Which hypotheses?", "H₀: μ = 12; Hₐ: μ > 12",
         ["H₀: μ > 12; Hₐ: μ = 12", "H₀: μ = 12; Hₐ: μ < 12", "H₀: x̄ = 12; Hₐ: x̄ > 12"]),
    ]
    for p_, c_, w_ in rows_cp2:
        MC(U, k, "cp2", p_, c_, w_, ["Hypotheses are about parameters (p or μ).", "H₀ states no change (equality); Hₐ states what we suspect, in the direction of the suspicion."], family="u4_hypotheses", std=sd_)
    mcs(k, "cp2", [
        ("The null hypothesis in a significance test is",
         "the claim of “no effect” or “no difference” that we look for evidence against", ["the claim we hope to prove", "always a statement about a sample statistic", "the conclusion of the test"],
         ["We assume H₀ and ask whether the data give convincing evidence against it."]),
        ("Which is a correctly written alternative hypothesis?", "Hₐ: p > 0.6", ["Hₐ: p̂ > 0.6", "Hₐ: x̄ ≠ 50", "Hₐ: p = 0.6"],
         ["Hypotheses use parameters; Hₐ uses <, >, or ≠."]),
    ], "u4_hyp_vocab", sd_)
    SA(U, k, "cp2", "A website claims that 75% of its users are satisfied. A reviewer suspects the true proportion is less than 75%. Write the hypotheses and define the parameter.",
       "H₀: p = 0.75; Hₐ: p < 0.75, where p = the proportion of all the website's users who are satisfied",
       ["Parameter p: the true proportion of all users who are satisfied.", "H₀: p = 0.75 (the claim).", "Hₐ: p < 0.75 (the suspicion)."], family="u4_write_hyp", std=sd_)
    SEL(U, k, "cp2", "Select ALL correctly written pairs of hypotheses.",
        ["H₀: μ = 100; Hₐ: μ ≠ 100", "H₀: p = 0.4; Hₐ: p > 0.4"], ["H₀: x̄ = 100; Hₐ: x̄ > 100", "H₀: p > 0.4; Hₐ: p = 0.4"],
        ["Use parameters, an equality in H₀, and an inequality in Hₐ."], family="u4_hyp_sel", std=sd_)
    mcs(k, "cp1", [
        ("A researcher collects data, sees that p̂ = 0.62, and then decides to test Hₐ: p > 0.55. What is wrong?",
         "Hypotheses must be chosen before looking at the data, based on the research question.", ["Nothing is wrong.", "p̂ cannot be greater than 0.55.", "The alternative must always be two-sided."],
         ["Choosing Hₐ after seeing the data biases the test."]),
        ("When should a two-sided alternative be used?",
         "When the research question asks whether the parameter differs in either direction", ["Whenever the sample size is large", "When the data show a large effect", "When the P-value is small"],
         ["The direction of Hₐ comes from the question, not the data."]),
        ("A drug company tests whether a new drug lowers mean cholesterol more than 20 mg/dL, the reduction from the old drug. Let μ = mean reduction with the new drug. Which hypotheses?",
         "H₀: μ = 20; Hₐ: μ > 20", ["H₀: μ = 20; Hₐ: μ < 20", "H₀: μ > 20; Hₐ: μ = 20", "H₀: μ = 0; Hₐ: μ > 0"],
         ["“Lowers more” means a larger reduction: Hₐ: μ > 20."]),
    ], "u4_hyp_cp1", sd_)
    SA(U, k, "cp1", "A store manager wants to know whether the mean time customers wait in line has changed from last year's 4.5 minutes. Write the hypotheses, define the parameter, and say whether the test is one- or two-sided.",
       "H₀: μ = 4.5; Hₐ: μ ≠ 4.5, where μ = the true mean wait time this year; two-sided",
       ["“Changed” means either direction.", "μ = true mean wait time for all customers this year.", "H₀: μ = 4.5; Hₐ: μ ≠ 4.5 (two-sided)."], family="u4_write_hyp", std=sd_)
    mcs(k, "honors", [
        ("A test fails to reject H₀: μ = 50. Which statement is correct?",
         "The data did not give convincing evidence that μ differs from 50; μ = 50 is plausible but not proven.", ["The data prove μ = 50.", "The data prove μ ≠ 50.", "The test must have been done incorrectly."],
         ["We never accept or prove H₀."]),
        ("Why is H₀ always stated with an equality (such as p = 0.3) rather than an inequality?",
         "The test statistic and P-value are computed assuming one specific value of the parameter.", ["Because equalities are easier to reject.", "Because the alternative must be one-sided.", "Because sample statistics must equal parameters."],
         ["The null distribution requires a specific parameter value."]),
    ], "u4_hyp_honors", sd_)
    SA(U, k, "honors", "A city says the mean response time for ambulances is 8 minutes. A reporter believes responses are slower in one neighborhood. Write hypotheses for her test, and explain why a one-sided alternative is appropriate here but would be inappropriate if chosen after seeing that the sample mean was 9.1 minutes.",
       "H₀: μ = 8; Hₐ: μ > 8 (μ = true mean response time in that neighborhood). One-sided is appropriate because her suspicion (slower) was formed before collecting data; choosing it after seeing the data would bias the test toward rejection.",
       ["Parameter: μ = true mean ambulance response time in the neighborhood.", "Her prior suspicion is “slower,” so Hₐ: μ > 8.", "The direction must come from the question, not the observed x̄.", "Picking the side after seeing the data effectively halves the P-value unfairly."],
       family="u4_hyp_reason", std=sd_)
    OR(U, k, "honors", "For each situation, define the parameter and state hypotheses.",
       [("A candy maker claims 20% of candies are red; a customer suspects fewer are red.", "p = proportion of all candies that are red; H₀: p = 0.20, Hₐ: p < 0.20"),
        ("The mean battery life of a phone model is advertised as 18 hours; a tester wants to know if it is different.", "μ = mean battery life of all phones of this model; H₀: μ = 18, Hₐ: μ ≠ 18"),
        ("A school wants to know if more than half of its seniors plan to attend college out of state.", "p = proportion of all seniors planning out-of-state college; H₀: p = 0.5, Hₐ: p > 0.5"),
        ("A nutritionist suspects a brand's bars contain more than the labeled 200 calories on average.", "μ = mean calories of all bars of the brand; H₀: μ = 200, Hₐ: μ > 200")],
       ["1 point per part with parameter defined and correct direction."], family="u4_hyp_or", std=sd_)


def s06():
    k, sd_ = 6, [TB + ".1"]
    mcs(k, "cp2", [
        ("A test at α = 0.05 gives a P-value of 0.03. What is the decision?", "Reject H₀", ["Fail to reject H₀", "Accept H₀", "Accept Hₐ as proven"],
         ["P-value < α → reject H₀."]),
        ("A test at α = 0.01 gives a P-value of 0.04. What is the decision?", "Fail to reject H₀", ["Reject H₀", "Accept H₀", "Prove Hₐ"],
         ["0.04 > 0.01, so the result is not significant at the 1% level."]),
        ("A P-value is",
         "the probability, assuming H₀ is true, of getting a result at least as extreme as the one observed", ["the probability that H₀ is true", "the probability that Hₐ is true", "the significance level"],
         ["P-values are computed under the null model."]),
        ("A smaller P-value means",
         "stronger evidence against H₀", ["stronger evidence for H₀", "a larger effect size for sure", "a larger sample"], ["Small P-values mean the observed result would be rare if H₀ were true."]),
    ], "u4_pvalue_basic", sd_)
    for lv, z, alt in [("cp2", 1.88, "gt"), ("cp2", -2.15, "lt"), ("cp1", 2.41, "ne"), ("cp1", -1.32, "ne")]:
        pv = ztail(z, alt)
        num_mc(U, k, lv, f"A one-proportion z test of H₀: p = p₀ vs Hₐ: p {SYM[alt]} p₀ gives z = {fmt(z, 2)}. Find the P-value (four decimals).", pv,
               [ztail(z, {"gt": "ne", "lt": "ne", "ne": "gt" if z > 0 else "lt"}[alt]), 1 - pv, Phi(z) if alt == "gt" else 1 - Phi(z)], 4,
               ["P-value = " + {"gt": f"P(Z ≥ {fmt(z, 2)})", "lt": f"P(Z ≤ {fmt(z, 2)})", "ne": f"2P(Z ≥ {fmt(abs(z), 2)})"}[alt] + f" ≈ {fmt(pv, 4)}."],
               family="u4_p_from_z", std=sd_, bounds=(0, 1), check={"kind": "z_p_only", "z": z, "alt": alt})
    SA(U, k, "cp2", "A test of H₀: p = 0.5 vs Hₐ: p > 0.5 about whether most students prefer a later start time gives P-value = 0.012. Using α = 0.05, write a conclusion in context.",
       "Because 0.012 < 0.05, reject H₀. There is convincing evidence that more than half of all students prefer a later start time.",
       ["Compare the P-value with α: 0.012 < 0.05.", "Reject H₀.", "State the conclusion about the parameter in context, in terms of Hₐ."], family="u4_conclude", std=sd_)
    for lv, t, df, alt in [("cp1", 2.10, 14, "gt"), ("honors", -1.85, 22, "lt"), ("honors", 2.60, 9, "ne")]:
        pv = ttail(t, df, alt)
        num_mc(U, k, lv, f"A one-sample t test with df = {df} gives t = {fmt(t, 2)} for Hₐ: μ {SYM[alt]} μ₀. Find the P-value (four decimals).", pv,
               [ztail(t, alt), pv * 2 if alt != "ne" else pv / 2, 1 - pv], 4,
               [f"Use the t distribution with df = {df}.", "P-value = " + {"gt": f"P(t ≥ {fmt(t, 2)})", "lt": f"P(t ≤ {fmt(t, 2)})", "ne": f"2P(t ≥ {fmt(abs(t), 2)})"}[alt] + f" ≈ {fmt(pv, 4)}."],
               family="u4_p_from_t", std=sd_, bounds=(0, 1), check={"kind": "t_p_only", "t": t, "df": df, "alt": alt})
    MC(U, k, "cp1", "A study reports P-value = 0.08. Which conclusion is correct at α = 0.05?",
       "Fail to reject H₀; the evidence is not strong enough at the 5% level.", ["Reject H₀ because 0.08 is small.", "Accept H₀; it is true.", "The probability H₀ is true is 0.08."],
       ["0.08 > 0.05; and a P-value is not the probability H₀ is true."], family="u4_conclude_mc", std=sd_)
    SA(U, k, "cp1", "Interpret the P-value 0.034 in context: a test of H₀: μ = 30 vs Hₐ: μ > 30 for mean battery life (hours) gave x̄ = 31.4.",
       "Assuming the true mean battery life is 30 hours, there is a 0.034 probability of getting a sample mean of 31.4 hours or more by chance alone.",
       ["Start with “assuming H₀ is true (μ = 30)”.", "Describe the probability of a result at least as extreme (x̄ ≥ 31.4).", "Mention chance (sampling variability)."], family="u4_interpret_p", std=sd_)
    mcs(k, "honors", [
        ("A large study (n = 50,000) finds a statistically significant difference of 0.3 points on a 100-point test. What should you conclude?",
         "The difference is unlikely to be due to chance, but it may be too small to matter in practice.", ["The difference is large.", "The study must be flawed.", "A P-value cannot be small with such a small difference."],
         ["Statistical significance ≠ practical importance; huge n detects tiny effects."]),
        ("The same z statistic, z = 1.80, is obtained in two tests: one with Hₐ: p > p₀ and one with Hₐ: p ≠ p₀. How do the P-values compare?",
         "The two-sided P-value is twice the one-sided P-value.", ["They are equal.", "The one-sided P-value is twice the two-sided.", "They cannot be compared."],
         ["Two-sided counts both tails."]),
    ], "u4_pvalue_honors", sd_)
    OR(U, k, "honors", "A random sample of 64 students had mean sleep 6.7 hours with s = 1.2 hours. Test H₀: μ = 7 vs Hₐ: μ < 7 at α = 0.05.",
       [("Compute the test statistic and df.", "t = (6.7 − 7)/(1.2/√64) = −2.00; df = 63"),
        ("Find the P-value (four decimals).", f"≈ {fmt(ttail(-2.0, 63, 'lt'), 4)}"),
        ("State the conclusion in context.", "P-value < 0.05: reject H₀; convincing evidence the mean sleep of all students is less than 7 hours"),
        ("Interpret the P-value.", "If the true mean were 7 hours, the probability of a sample mean of 6.7 hours or less by chance is about 0.025")],
       ["1 point each part."], family="u4_test_or", std=sd_, check={"kind": "t_test", "xbar": 6.7, "mu0": 7, "s": 1.2, "n": 64, "alt": "lt"})


def s07():
    k, sd_ = 7, [TB + ".2", TB + ".4"]
    for lv, p0, x, n, alt, ctx in [("cp2", 0.5, 62, 100, "gt", "A coin is flipped 100 times and lands heads 62 times. Test H₀: p = 0.5 vs Hₐ: p > 0.5."),
                                   ("cp2", 0.25, 41, 200, "lt", "A school claims 25% of students bike. In an SRS of 200, 41 bike. Test H₀: p = 0.25 vs Hₐ: p < 0.25."),
                                   ("cp1", 0.70, 245, 330, "ne", "A college says 70% of its students receive aid. An SRS of 330 students finds 245 receive aid. Test H₀: p = 0.70 vs Hₐ: p ≠ 0.70.")]:
        ph = x / n
        z = (ph - p0) / math.sqrt(p0 * (1 - p0) / n)
        pv = ztail(z, alt)
        SA(U, k, lv, ctx + " Find the test statistic (two decimals) and P-value (four decimals), then state the decision at α = 0.05.",
           f"z ≈ {fmt(z, 2)}, P-value ≈ {fmt(pv, 4)}; " + ("reject H₀" if pv < 0.05 else "fail to reject H₀"),
           [f"p̂ = {x}/{n} = {fmt(ph, 4)}.", f"z = (p̂ − p₀)/√(p₀(1 − p₀)/n) = ({fmt(ph, 4)} − {fmt(p0)})/√({fmt(p0)}·{fmt(1 - p0)}/{n}) ≈ {fmt(z, 3)}.",
            f"P-value ≈ {fmt(pv, 4)}.", "Since P " + ("<" if pv < 0.05 else ">") + " 0.05, " + ("reject H₀." if pv < 0.05 else "fail to reject H₀.")],
           family="u4_z_test", std=sd_, check={"kind": "z_test", "p0": p0, "x": x, "n": n, "alt": alt})
    MC(U, k, "cp2", "In a one-proportion z test, which value is used in the standard deviation of p̂?", "p₀, the value in the null hypothesis", ["p̂, the sample proportion", "0.5 always", "The margin of error"],
       ["The test assumes H₀ is true, so σ = √(p₀(1 − p₀)/n)."], family="u4_z_test_sd", std=sd_)
    MC(U, k, "cp2", "A sample of 30 test scores has x̄ = 78, s = 10. For H₀: μ = 75, what is the t statistic? Round to two decimals.", f"{fmt(3 / (10 / math.sqrt(30)), 2)}",
       ["0.30", f"{fmt(3 / (10 / math.sqrt(29)), 2)}", "3.00"], ["t = (78 − 75)/(10/√30) ≈ 1.64."], family="u4_t_stat", std=sd_,
       check={"kind": "t_stat", "xbar": 78, "mu0": 75, "s": 10, "n": 30})
    SA(U, k, "cp2", "Conditions check: a random sample of 120 drivers (from a city of 80,000) is used to test whether more than 40% text while driving; 56 admit texting. Check Random, 10%, and Large Counts for a one-proportion z test.",
       "Random: random sample. 10%: 120 < 8,000. Large Counts: np₀ = 48 and n(1 − p₀) = 72, both ≥ 10. Conditions are met.",
       ["Random: stated.", "10%: 10% of 80,000 = 8,000 > 120.", "For a test, use p₀ = 0.40: 120(0.40) = 48, 120(0.60) = 72."], family="u4_test_conditions", std=sd_,
       check={"kind": "large_counts", "n": 120, "p": 0.4})
    for lv, xb, mu0, s, n, alt, ctx in [("cp1", 31.2, 30, 3.5, 25, "gt", "A random sample of 25 tires lasted a mean of 31.2 thousand miles (s = 3.5); no outliers. Test H₀: μ = 30 vs Hₐ: μ > 30."),
                                        ("honors", 98.2, 98.6, 0.7, 40, "ne", "A random sample of 40 adults had mean body temperature 98.2 °F (s = 0.7). Test H₀: μ = 98.6 vs Hₐ: μ ≠ 98.6.")]:
        t = (xb - mu0) / (s / math.sqrt(n))
        pv = ttail(t, n - 1, alt)
        SA(U, k, lv, ctx + " Find t (three decimals), df, and the P-value (four decimals), and conclude at α = 0.05.",
           f"t ≈ {fmt(t, 3)}, df = {n - 1}, P-value ≈ {fmt(pv, 4)}; " + ("reject H₀" if pv < 0.05 else "fail to reject H₀"),
           [f"t = ({fmt(xb)} − {fmt(mu0)})/({fmt(s)}/√{n}) ≈ {fmt(t, 3)}.", f"df = {n - 1}.", f"P-value ≈ {fmt(pv, 4)}.",
            "P " + ("<" if pv < 0.05 else ">") + " 0.05, so " + ("reject H₀: convincing evidence for Hₐ." if pv < 0.05 else "fail to reject H₀: not convincing evidence for Hₐ.")],
           family="u4_t_test", std=sd_, check={"kind": "t_test", "xbar": xb, "mu0": mu0, "s": s, "n": n, "alt": alt})
    MC(U, k, "cp1", "Which test is appropriate for “Is the mean amount of soda in 12-oz cans less than 12 oz?” using a random sample of 20 cans?",
       "One-sample t test for a mean", ["One-proportion z test", "Two-sample t test", "Two-proportion z test"], ["One quantitative variable, one sample, σ unknown → one-sample t."], family="u4_choose_test", std=sd_)
    OR(U, k, "honors", "A light-bulb maker claims a mean life of 1,200 hours. A consumer group tests an SRS of 20 bulbs: x̄ = 1,163 hours, s = 74 hours; a dotplot is roughly symmetric with no outliers.",
       [("State hypotheses for testing whether the mean life is less than claimed.", "H₀: μ = 1,200; Hₐ: μ < 1,200 (μ = true mean life)"),
        ("Check conditions.", "Random (SRS); 10% (20 < 10% of all bulbs); Normal: n < 30 but no strong skew/outliers"),
        ("Compute t, df, and the P-value (four decimals).", f"t ≈ {fmt(-37 / (74 / math.sqrt(20)), 3)}, df = 19, P ≈ {fmt(ttail(-37 / (74 / math.sqrt(20)), 19, 'lt'), 4)}"),
        ("Conclude at α = 0.05 in context.", "Reject H₀; convincing evidence the true mean life is less than 1,200 hours")],
       ["1 point each part."], family="u4_t_test_or", std=sd_, check={"kind": "t_test", "xbar": 1163, "mu0": 1200, "s": 74, "n": 20, "alt": "lt"})
    SA(U, k, "honors", "Error analysis. Testing H₀: p = 0.40 with x = 52, n = 100, a student computes z = (0.52 − 0.40)/√(0.52 × 0.48/100) = 2.40. Identify the error and give the correct z (two decimals).",
       f"The SD must use p₀ = 0.40, not p̂: z = 0.12/√(0.40·0.60/100) ≈ {fmt(0.12 / math.sqrt(0.24 / 100), 2)}",
       ["In a test we assume H₀ is true, so the SD uses p₀.", "σ = √(0.40 × 0.60/100) ≈ 0.0490.", f"z = 0.12/0.0490 ≈ {fmt(0.12 / math.sqrt(0.0024), 2)}.", "(Using p̂ in the SE is correct for confidence intervals, not tests.)"],
       family="u4_z_sd_error", std=sd_, check={"kind": "z_stat", "p0": 0.4, "x": 52, "n": 100})


def s08():
    k, sd_ = 8, [TB + ".1"]
    rows = [
        ("A Type I error occurs when we", "reject H₀ when H₀ is actually true", ["fail to reject H₀ when H₀ is false", "reject H₀ when it is false", "fail to reject H₀ when it is true"], ["Type I = false alarm."]),
        ("A Type II error occurs when we", "fail to reject H₀ when H₀ is actually false", ["reject H₀ when H₀ is true", "reject H₀ when it is false", "accept Hₐ when it is true"], ["Type II = missed detection."]),
        ("If α = 0.05, the probability of a Type I error (when H₀ is true) is", "0.05", ["0.95", "unknown", "0.10"], ["P(Type I error) = α."]),
        ("A fire alarm goes off when there is no fire. In testing H₀: “there is no fire,” this is a", "Type I error", ["Type II error", "correct decision", "power"], ["Rejecting a true H₀ (no fire)."]),
        ("A smoke detector does not sound when there is a fire. With H₀: “no fire,” this is a", "Type II error", ["Type I error", "correct decision", "significance level"], ["Failing to reject a false H₀."]),
        ("Power is the probability of", "correctly rejecting H₀ when it is false", ["rejecting H₀ when it is true", "failing to reject H₀", "making a Type II error"], ["Power = 1 − P(Type II error)."]),
    ]
    for p_, c_, w_, s_ in rows:
        MC(U, k, "cp2", p_, c_, w_, s_, family="u4_errors_basic", std=sd_)
    SA(U, k, "cp2", "A factory tests H₀: the machine is working correctly vs Hₐ: the machine is not working correctly. Describe a Type I and a Type II error in context.",
       "Type I: concluding the machine is not working correctly when it actually is (unnecessary shutdown). Type II: concluding there is not enough evidence of a problem when the machine actually is malfunctioning.",
       ["Type I = rejecting a true H₀.", "Type II = failing to reject a false H₀.", "Write each in the context of the machine."], family="u4_errors_context", std=sd_)
    SEL(U, k, "cp2", "Select ALL changes that increase the power of a test (other things equal).",
        ["Increasing the sample size", "Increasing α from 0.01 to 0.05"], ["Decreasing the sample size", "Testing a true parameter value closer to the null value"],
        ["Power rises with larger n, larger α, and a larger true effect."], family="u4_power_sel", std=sd_)
    mcs(k, "cp1", [
        ("A drug company tests H₀: a drug has no serious side effects vs Hₐ: it does. Which error is more serious, and how should α be chosen?",
         "A Type II error (missing real side effects) is more serious, so use a larger α such as 0.10 to increase power.", ["A Type I error; use α = 0.001.", "Neither; α does not matter.", "A Type II error; use α = 0.001."],
         ["When missing a real effect is dangerous, increase power (larger α, larger n)."]),
        ("The power of a test against a specific alternative is 0.72. What is the probability of a Type II error for that alternative?", "0.28", ["0.72", "0.05", "0.95"],
         ["P(Type II) = 1 − power = 0.28."]),
        ("A test rejects H₀ at α = 0.05. Which error could have been made?", "Type I error", ["Type II error", "Both", "Neither error is possible"], ["Only rejecting can produce a Type I error."]),
    ], "u4_errors_cp1", sd_)
    SA(U, k, "cp1", "A school tests H₀: the new reading program has no effect on scores vs Hₐ: it raises scores. Describe the consequence of each type of error for the school.",
       "Type I: the school adopts a program that does not help (wasted money and time). Type II: the school does not adopt a program that would have raised scores (missed benefit).",
       ["Type I: reject H₀ wrongly → adopt an ineffective program.", "Type II: fail to reject wrongly → miss an effective program."], family="u4_errors_consequence", std=sd_)
    mcs(k, "honors", [
        ("Decreasing α from 0.05 to 0.01, with n unchanged, will",
         "decrease P(Type I error) but increase P(Type II error)", ["decrease both error probabilities", "increase power", "increase P(Type I error)"],
         ["Making it harder to reject lowers false alarms but misses more real effects."]),
        ("Why does increasing the sample size increase power?",
         "It reduces the variability of the statistic, so a real difference from the null value is easier to detect.", ["It increases α.", "It changes the null hypothesis.", "It makes H₀ false."],
         ["Smaller SE → the sampling distributions under H₀ and Hₐ overlap less."]),
    ], "u4_errors_honors", sd_)
    crit = 0.5 + 1.645 * math.sqrt(0.25 / 100)
    pw = 1 - Phi((crit - 0.6) / math.sqrt(0.24 / 100))
    OR(U, k, "honors", "A test of H₀: p = 0.5 vs Hₐ: p > 0.5 uses n = 100 and α = 0.05.",
       [("Find the critical value of p̂ for rejecting H₀ (four decimals).", f"p̂ ≥ 0.5 + 1.645√(0.25/100) ≈ {fmt(crit, 4)}"),
        ("If the true p is 0.6, find the power of the test (four decimals).", f"Power = P(p̂ ≥ {fmt(crit, 4)} | p = 0.6) ≈ {fmt(pw, 4)}"),
        ("Find the probability of a Type II error when p = 0.6.", f"≈ {fmt(1 - pw, 4)}"),
        ("Name two ways to increase the power against p = 0.6.", "Increase n; increase α (e.g., to 0.10)")],
       ["1 point each part."], family="u4_power_or", std=sd_, check={"kind": "power_calc", "p0": 0.5, "pa": 0.6, "n": 100, "alpha": 0.05})


def s09():
    k, sd_ = 9, [EA + ".5", TB + ".3"]
    mcs(k, "cp2", [
        ("In a study comparing two proportions, p₁ − p₂ = 0 means", "the two population proportions are equal", ["both proportions are 0", "the samples are the same size", "there is a large difference"],
         ["A difference of 0 means no difference."]),
        ("A 95% CI for p₁ − p₂ is (0.03, 0.11). What does it suggest?", "p₁ is likely greater than p₂, because the whole interval is above 0.", ["p₂ is greater than p₁.", "There is no difference.", "The interval is invalid because it is above 0."],
         ["All plausible differences are positive."]),
        ("A 95% CI for p₁ − p₂ is (−0.04, 0.06). What does it suggest?", "There is no convincing evidence of a difference, because 0 is in the interval.", ["p₁ is greater than p₂.", "p₂ is greater than p₁.", "The proportions differ by 0.06."],
         ["0 is a plausible value of the difference."]),
    ], "u4_two_prop_interpret", sd_)
    for lv, x1, n1, x2, n2, ctx in [("cp2", 48, 120, 30, 120, "In an experiment, 48 of 120 students given reminders turned in homework on time vs 30 of 120 without reminders."),
                                    ("cp2", 72, 200, 57, 190, "A survey found 72 of 200 juniors and 57 of 190 seniors drink coffee daily.")]:
        p1, p2 = x1 / n1, x2 / n2
        SA(U, k, lv, ctx + " Find p̂₁, p̂₂, and the point estimate of p₁ − p₂ (three decimals).", f"p̂₁ = {fmt(p1, 3)}, p̂₂ = {fmt(p2, 3)}, difference = {fmt(p1 - p2, 3)}",
           [f"p̂₁ = {x1}/{n1} = {fmt(p1, 3)}.", f"p̂₂ = {x2}/{n2} = {fmt(p2, 3)}.", f"p̂₁ − p̂₂ = {fmt(p1 - p2, 3)}."], family="u4_two_prop_point", std=sd_,
           check={"kind": "ratio", "num": x1 * n2 - x2 * n1, "den": n1 * n2, "verify_only": True, "expect": (x1 * n2 - x2 * n1) / (n1 * n2)})
    SA(U, k, "cp2", "To compare two proportions with a z procedure, list the conditions that must be checked.",
       "Random (two independent random samples or random assignment); 10% (each sample < 10% of its population, when sampling); Large Counts (at least 10 successes and 10 failures in each group).",
       ["Random for both groups.", "Independence via the 10% condition when sampling without replacement.", "Large counts in each group."], family="u4_two_prop_conditions", std=sd_)
    for lv, x1, n1, x2, n2, c in [("cp1", 132, 300, 105, 300, 95), ("honors", 56, 160, 38, 175, 90)]:
        p1, p2 = x1 / n1, x2 / n2
        se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
        me = ZSTAR[c] * se
        key = iv(p1 - p2 - me, p1 - p2 + me)
        MC(U, k, lv, f"Group 1: {x1} successes in {n1}; Group 2: {x2} successes in {n2} (independent random samples). Construct a {c}% confidence interval for p₁ − p₂ (three decimals).",
           key, [iv(p1 - p2 - m, p1 - p2 + m) for m in (se, ZSTAR[c] * (math.sqrt(p1 * (1 - p1) / n1) + math.sqrt(p2 * (1 - p2) / n2)), ZSTAR[99 if c != 99 else 90] * se)],
           [f"p̂₁ = {fmt(p1, 4)}, p̂₂ = {fmt(p2, 4)}.", f"SE = √(p̂₁(1 − p̂₁)/n₁ + p̂₂(1 − p̂₂)/n₂) ≈ {fmt(se, 4)}.", f"({fmt(p1 - p2, 4)}) ± {ZSTAR[c]}({fmt(se, 4)}) → {key}."],
           family="u4_two_prop_ci", std=sd_, check={"kind": "two_prop_ci", "x1": x1, "n1": n1, "x2": x2, "n2": n2, "conf": c})
    x1, n1, x2, n2 = 90, 250, 65, 250
    pc = (x1 + x2) / (n1 + n2)
    z = (x1 / n1 - x2 / n2) / math.sqrt(pc * (1 - pc) * (2 / 250))
    SA(U, k, "cp1", f"In a randomized experiment, {x1} of {n1} patients improved with a new therapy and {x2} of {n2} improved with the standard therapy. Find the pooled proportion, the z statistic (two decimals), and the one-sided P-value for Hₐ: p_new > p_std (four decimals).",
       f"p̂_C = {fmt(pc, 3)}, z ≈ {fmt(z, 2)}, P-value ≈ {fmt(1 - Phi(z), 4)}",
       [f"p̂_C = ({x1} + {x2})/({n1} + {n2}) = {fmt(pc, 3)}.", f"SE = √(p̂_C(1 − p̂_C)(1/{n1} + 1/{n2})) ≈ {fmt(math.sqrt(pc * (1 - pc) * 2 / 250), 4)}.",
        f"z = ({fmt(x1 / n1, 2)} − {fmt(x2 / n2, 2)})/SE ≈ {fmt(z, 2)}.", f"P-value = P(Z ≥ {fmt(z, 2)}) ≈ {fmt(1 - Phi(z), 4)}."],
       family="u4_two_prop_test", std=sd_, check={"kind": "two_prop_test", "x1": x1, "n1": n1, "x2": x2, "n2": n2, "alt": "gt"})
    MC(U, k, "cp1", "Why is the pooled proportion used in a two-proportion z test but not in the confidence interval?",
       "The test assumes H₀: p₁ = p₂, so one common proportion is estimated; the interval makes no such assumption.", ["Pooling makes the interval narrower.", "Intervals require equal sample sizes.", "Tests do not need standard errors."],
       ["The null model in a test has a single common p."], family="u4_pool_why", std=sd_)
    OR(U, k, "honors", "A random sample of 400 adults under 30 found 236 use a budgeting app; a separate random sample of 350 adults 30 or older found 161 use one.",
       [("State hypotheses for testing whether the proportions differ.", "H₀: p_young = p_older; Hₐ: p_young ≠ p_older"),
        ("Compute the pooled proportion and z statistic (two decimals).", f"p̂_C = {fmt(397 / 750, 4)}; z ≈ {fmt((236 / 400 - 161 / 350) / math.sqrt(397 / 750 * (1 - 397 / 750) * (1 / 400 + 1 / 350)), 2)}"),
        ("Find the P-value (four decimals) and conclude at α = 0.05.", f"P ≈ {fmt(2 * (1 - Phi((236 / 400 - 161 / 350) / math.sqrt(397 / 750 * (1 - 397 / 750) * (1 / 400 + 1 / 350)))), 4)}; reject H₀"),
        ("Can we conclude that age causes app use? Explain.", "No; these are observational samples, so only an association can be concluded")],
       ["1 point each part."], family="u4_two_prop_or", std=sd_, check={"kind": "two_prop_test", "x1": 236, "n1": 400, "x2": 161, "n2": 350, "alt": "ne"})


def s10():
    k, sd_ = 10, [EA + ".7", TB + ".5"]
    mcs(k, "cp2", [
        ("Which situation calls for a paired t procedure?", "Each patient's blood pressure is measured before and after a medication.", ["Comparing heights of a random sample of boys and a random sample of girls", "Comparing two randomly assigned groups of 30 students", "Comparing proportions of voters in two states"],
         ["Paired data: two measurements on the same individual (or matched pairs)."]),
        ("In a paired t procedure, the analysis is carried out on", "the differences within each pair", ["the two sample means separately", "the larger of the two samples", "the pooled proportion"],
         ["Paired data reduce to one sample of differences."]),
        ("For an independent two-sample t interval, what is the point estimate of μ₁ − μ₂?", "x̄₁ − x̄₂", ["s₁ − s₂", "μ₁ − μ₂", "(x̄₁ + x̄₂)/2"], ["Use the difference of sample means."]),
    ], "u4_two_t_basic", sd_)
    before = [62, 70, 58, 75, 66, 71]
    after = [58, 64, 57, 69, 60, 68]
    d = [b - a for b, a in zip(before, after)]
    SA(U, k, "cp2", f"Six people's resting pulse (bpm) before and after a 4-week exercise program:\nBefore: {lst(before)}\nAfter: {lst(after)}\nFind the differences (Before − After), their mean, and their standard deviation (two decimals).",
       f"Differences {lst(d)}; mean = {fmt(sum(d) / 6, 2)}; SD ≈ {fmt(sd(d), 2)}",
       [f"Differences: {lst(d)}.", f"Mean = {sum(d)}/6 = {fmt(sum(d) / 6, 2)}.", f"SD (n − 1) ≈ {fmt(sd(d), 2)}."], family="u4_paired_diffs", std=sd_,
       check={"kind": "paired", "a": before, "b": after, "alt": "gt", "verify_only": True, "expect": [sum(d) / 6, sd(d), (sum(d) / 6) / (sd(d) / math.sqrt(6)), ttail((sum(d) / 6) / (sd(d) / math.sqrt(6)), 5, "gt")], "tol": 1e-9})
    SA(U, k, "cp2", "Group 1: n = 30, x̄ = 72, s = 8. Group 2: n = 35, x̄ = 66, s = 10. Find the point estimate and standard error of μ₁ − μ₂ (three decimals).",
       f"Estimate 6; SE ≈ {fmt(math.sqrt(64 / 30 + 100 / 35), 3)}", ["Estimate = 72 − 66 = 6.", f"SE = √(8²/30 + 10²/35) = √({fmt(64 / 30, 4)} + {fmt(100 / 35, 4)}) ≈ {fmt(math.sqrt(64 / 30 + 100 / 35), 3)}."],
       family="u4_two_t_se", std=sd_, check={"kind": "two_t_ci", "m1": 72, "s1": 8, "n1": 30, "m2": 66, "s2": 10, "n2": 35, "conf": 95, "verify_only": True,
                                             "expect": [6 - tstar(95, 29) * math.sqrt(64 / 30 + 100 / 35), 6 + tstar(95, 29) * math.sqrt(64 / 30 + 100 / 35)], "tol": 1e-9})
    MC(U, k, "cp2", "A 95% CI for μ₁ − μ₂ is (−3.1, 5.4). What can you conclude?", "There is no convincing evidence of a difference in means, because 0 is in the interval.",
       ["μ₁ is greater than μ₂.", "μ₂ is greater than μ₁.", "The means differ by 5.4."], ["0 is a plausible difference."], family="u4_two_t_interpret", std=sd_)
    for lv, m1, s1, n1, m2, s2, n2, c in [("cp1", 81.5, 9.2, 28, 76.0, 11.4, 31, 95), ("honors", 14.6, 3.1, 18, 12.2, 2.4, 20, 90)]:
        se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
        df = min(n1, n2) - 1
        t = tstar(c, df)
        key = iv(m1 - m2 - t * se, m1 - m2 + t * se, 2)
        MC(U, k, lv, f"Independent random samples: Group 1 n = {n1}, x̄ = {m1}, s = {s1}; Group 2 n = {n2}, x̄ = {m2}, s = {s2}. Construct a {c}% CI for μ₁ − μ₂ using the conservative df = {df} (two decimals).",
           key, [iv(m1 - m2 - x, m1 - m2 + x, 2) for x in (ZSTAR[c] * se, t * (s1 / math.sqrt(n1) + s2 / math.sqrt(n2)), t * math.sqrt(s1 ** 2 + s2 ** 2) / math.sqrt(n1 + n2))],
           [f"SE = √({s1}²/{n1} + {s2}²/{n2}) ≈ {fmt(se, 4)}.", f"df = {df}, t* ≈ {fmt(t, 3)}.", f"({fmt(m1 - m2, 2)}) ± {fmt(t * se, 3)} → {key}."],
           family="u4_two_t_ci", std=sd_, check={"kind": "two_t_ci", "m1": m1, "s1": s1, "n1": n1, "m2": m2, "s2": s2, "n2": n2, "conf": c})
    SA(U, k, "cp1", "Twelve students took a vocabulary test before and after a program. The mean of the differences (After − Before) is 3.5 points with SD 4.2. Test H₀: μ_d = 0 vs Hₐ: μ_d > 0: find t (three decimals) and the P-value (four decimals).",
       f"t ≈ {fmt(3.5 / (4.2 / math.sqrt(12)), 3)}, P-value ≈ {fmt(ttail(3.5 / (4.2 / math.sqrt(12)), 11, 'gt'), 4)}",
       ["Paired t on differences: t = x̄_d/(s_d/√n).", f"t = 3.5/(4.2/√12) ≈ {fmt(3.5 / (4.2 / math.sqrt(12)), 3)}, df = 11.", f"P-value ≈ {fmt(ttail(3.5 / (4.2 / math.sqrt(12)), 11, 'gt'), 4)}.", "Small P-value: convincing evidence of a mean improvement."],
       family="u4_paired_test", std=sd_, check={"kind": "paired_summary", "dbar": 3.5, "sd": 4.2, "n": 12, "alt": "gt"})
    MC(U, k, "cp1", "Ten pairs of identical twins are split: one twin uses Program A, the other Program B. Why is a two-sample t test inappropriate?",
       "The observations are paired (twins are matched), so the samples are not independent; analyze the differences.", ["Because n is too small.", "Because twins are not random.", "Because the data are categorical."],
       ["Matched data violate the independence of two samples."], family="u4_paired_vs_two", std=sd_)
    a = [12.1, 13.4, 11.8, 14.0, 12.7, 13.1, 12.5, 13.9]
    b = [11.5, 12.6, 11.9, 13.1, 12.0, 12.4, 12.2, 13.0]
    dd = [x - y for x, y in zip(a, b)]
    md, sdd = sum(dd) / 8, sd(dd)
    tt = md / (sdd / math.sqrt(8))
    OR(U, k, "honors", f"Eight runners ran 1 mile wearing old shoes and new shoes (order randomized). Times (minutes):\nOld: {lst(a)}\nNew: {lst(b)}",
       [("Explain why a paired procedure is appropriate.", "Each runner is measured in both conditions, so the data are paired by runner"),
        ("Find the mean and SD of the differences (Old − New), two decimals.", f"x̄_d ≈ {fmt(md, 2)}, s_d ≈ {fmt(sdd, 2)}"),
        ("Test H₀: μ_d = 0 vs Hₐ: μ_d > 0: give t (two decimals), df, and P-value (four decimals).", f"t ≈ {fmt(tt, 2)}, df = 7, P ≈ {fmt(ttail(tt, 7, 'gt'), 4)}"),
        ("State a conclusion in context.", "Reject H₀: convincing evidence the new shoes reduce mean mile time for runners like these")],
       ["1 point each part."], family="u4_paired_or", std=sd_, check={"kind": "paired", "a": a, "b": b, "alt": "gt"})
    SA(U, k, "honors", "Error analysis. To compare mean scores of 20 students before and after tutoring, a student used a two-sample t test and got P = 0.21. A paired t test on the same data gives P = 0.004. Explain the difference and which analysis is correct.",
       "The paired test is correct: the data are matched by student. The two-sample test ignores the pairing and treats student-to-student variation as noise, inflating the SE and the P-value.",
       ["Before/after scores on the same students are dependent.", "Pairing removes between-student variability.", "The two-sample SE is much larger, so the effect looks insignificant.", "Use the paired t test on the differences."],
       family="u4_paired_error", std=sd_)


def s11():
    k, sd_ = 11, [EA + ".8"]
    out = "Computer output for regressing y on x (n = {n}):\nPredictor  Coef    SE Coef\nConstant   {a}    {sea}\nx          {b}    {seb}\nS = {s}   R-sq = {r2}"
    o1 = out.format(n=20, a=12.4, sea=3.1, b=2.35, seb=0.48, s=4.6, r2="57.1%")
    MC(U, k, "cp2", o1 + "\nWhat is the slope of the least-squares regression line, and what is its standard error?", "Slope 2.35; SE 0.48", ["Slope 12.4; SE 3.1", "Slope 0.48; SE 2.35", "Slope 2.35; SE 4.6"],
       ["The slope is the coefficient on x (2.35); its SE is in the same row (0.48)."], family="u4_read_output", std=sd_)
    MC(U, k, "cp2", "For a confidence interval for the slope of a regression line based on n = 20 points, how many degrees of freedom are used?", "18", ["19", "20", "17"],
       ["df = n − 2 for regression slope inference."], family="u4_slope_df", std=sd_)
    t = tstar(95, 18)
    SA(U, k, "cp2", o1 + f"\nUsing t* = {fmt(t, 3)} (95%, df = 18), construct a 95% confidence interval for the true slope (three decimals).",
       iv(2.35 - t * 0.48, 2.35 + t * 0.48), [f"b ± t*·SE_b = 2.35 ± {fmt(t, 3)}(0.48).", f"Margin = {fmt(t * 0.48, 3)}.", f"Interval = {iv(2.35 - t * 0.48, 2.35 + t * 0.48)}."],
       family="u4_slope_ci_given_t", std=sd_, check={"kind": "slope_ci", "b": 2.35, "se": 0.48, "n": 20, "conf": 95})
    MC(U, k, "cp2", "A 95% confidence interval for the slope relating hours studied to test score is (1.8, 4.2) points per hour. What does it suggest?",
       "There is convincing evidence of a positive linear relationship, because 0 is not in the interval.", ["There is no relationship.", "The relationship is negative.", "Every hour adds exactly 3 points."],
       ["All plausible slopes are positive."], family="u4_slope_interpret", std=sd_)
    o2 = out.format(n=15, a=-4.8, sea=6.2, b=0.92, seb=0.27, s=7.9, r2="47.2%")
    t2 = tstar(90, 13)
    MC(U, k, "cp1", o2 + "\nConstruct a 90% confidence interval for the true slope (three decimals).", iv(0.92 - t2 * 0.27, 0.92 + t2 * 0.27),
       [iv(0.92 - x, 0.92 + x) for x in (1.645 * 0.27, tstar(90, 14) * 0.27 + 0.02, tstar(95, 13) * 0.27)],
       [f"df = n − 2 = 13; t* ≈ {fmt(t2, 3)}.", f"0.92 ± {fmt(t2, 3)}(0.27) → {iv(0.92 - t2 * 0.27, 0.92 + t2 * 0.27)}."], family="u4_slope_ci", std=sd_,
       check={"kind": "slope_ci", "b": 0.92, "se": 0.27, "n": 15, "conf": 90})
    SA(U, k, "cp1", o2 + "\nCompute the t statistic for H₀: β = 0 and the two-sided P-value (four decimals).",
       f"t ≈ {fmt(0.92 / 0.27, 3)}, P-value ≈ {fmt(ttail(0.92 / 0.27, 13, 'ne'), 4)}", ["t = b/SE_b = 0.92/0.27 ≈ 3.407.", "df = 13.", f"P = 2P(t₁₃ ≥ 3.407) ≈ {fmt(ttail(0.92 / 0.27, 13, 'ne'), 4)}."],
       family="u4_slope_test", std=sd_, check={"kind": "slope_t", "b": 0.92, "se": 0.27, "n": 15, "alt": "ne"})
    MC(U, k, "cp1", "Which is a condition for inference about the slope of a regression line?",
       "The residual plot shows no pattern and roughly equal spread; residuals are approximately Normal.", ["The correlation must be greater than 0.8.", "The x-values must be Normal.", "The sample size must be at least 100."],
       ["LINER: Linear, Independent, Normal residuals, Equal SD, Random."], family="u4_slope_conditions", std=sd_)
    MC(U, k, "cp1", "In computer regression output, “S = 4.6” estimates",
       "the standard deviation of the residuals (typical prediction error)", ["the standard error of the slope", "the slope", "the correlation"],
       ["S is the residual standard deviation σ̂."], family="u4_read_S", std=sd_)
    SEL(U, k, "cp1", "Select ALL true statements about a confidence interval for the slope β.",
        ["It uses df = n − 2.", "If it does not contain 0, there is convincing evidence of a linear relationship."], ["It is centered at the y-intercept.", "It uses z* because n is large."],
        ["Center = b; critical value from t with n − 2 df."], family="u4_slope_sel", std=sd_)
    o3 = out.format(n=25, a=1.95, sea=0.84, b=-0.064, seb=0.021, s=0.73, r2="28.8%")
    t3 = tstar(95, 23)
    OR(U, k, "honors", o3 + "\n(x = hours of screen time per week, y = GPA, random sample of 25 students.)",
       [("Write the equation of the LSRL.", "ŷ = 1.95 − 0.064x"),
        ("Construct a 95% CI for the true slope (four decimals).", iv(-0.064 - t3 * 0.021, -0.064 + t3 * 0.021, 4)),
        ("Interpret the interval in context.", "We are 95% confident the interval captures the true change in mean GPA for each additional weekly hour of screen time"),
        ("Does this show screen time causes lower GPAs? Explain.", "No; observational data — association only")],
       ["1 point each part."], family="u4_slope_or", std=sd_, check={"kind": "slope_ci", "b": -0.064, "se": 0.021, "n": 25, "conf": 95})
    MC(U, k, "honors", "Two regressions give slopes with the same b but SE_b = 0.10 for one and 0.40 for the other. Which statement is true?",
       "The interval for the slope with SE 0.10 is narrower; that slope is estimated more precisely.", ["Both intervals have the same width.", "The larger SE gives stronger evidence of a relationship.", "SE_b does not affect inference."],
       ["Width = 2t*·SE_b."], family="u4_seb_compare", std=sd_)
    SA(U, k, "honors", "A residual plot for a regression of y on x shows a clear fan shape (spread increases with x). Explain which inference condition is violated and the consequence for a confidence interval for the slope.",
       "Equal SD (constant spread) is violated; the standard error of the slope may be inaccurate, so the stated confidence level may not be correct.",
       ["Inference for slope assumes the SD of y about the line is the same for all x.", "A fan shape shows changing spread.", "Then SE_b and the t procedure are unreliable.", "A transformation (e.g., log y) might fix it."],
       family="u4_slope_cond_violate", std=sd_)
    MC(U, k, "honors", "For a regression of y on x with n = 30, the 95% CI for β is (−0.12, 0.85). The two-sided test of H₀: β = 0 at α = 0.05 would",
       "fail to reject H₀, because 0 is in the interval", ["reject H₀", "give P-value < 0.05", "require a larger α"], ["Duality of CI and two-sided test."], family="u4_slope_duality", std=sd_)


def build():
    for f in (s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11):
        f()
