"""Breadth pass: new reasoning types for cells with < 8 distinct items, purpose-written
error-analysis items (family ending in _error) at CP2/CP1, and integer-answer (1–25)
multi-step short-answer items usable as Escape Room candidates."""
from common import *
from math import comb

ED, SE, AP, SI = "exploring-data", "sampling-experimentation", "anticipating-patterns", "statistical-inference"
IE, IB, ID = ["APSTATS.I.E"], ["APSTATS.I.B"], ["APSTATS.I.D"]


def ed():
    SA(ED, 6, "cp2", "Error analysis. A two-way table shows 30 of 50 boys and 45 of 75 girls prefer online classes. A student writes: “More girls (45) than boys (30) prefer online classes, so girls are more likely to prefer them.” Explain the error and give the correct comparison.",
       "Comparing counts ignores group sizes. Boys: 30/50 = 60%; girls: 45/75 = 60%. The proportions are equal, so girls are not more likely to prefer online classes.",
       ["Groups have different totals (50 vs 75).", "Compare conditional proportions: 30/50 = 0.60 and 45/75 = 0.60.", "Equal proportions → no association in these data.", "Counts alone can be misleading."],
       family="u1_tw_counts_error", std=IE, check={"kind": "ratio", "num": 30, "den": 50, "skip_distractors": True})
    MC(ED, 6, "cp2", "A bar graph shows the number of students who chose each lunch option: pizza 42, salad 18, sandwich 30, other 10. What percent chose salad?", "18%",
       ["42%", "20%", "25%"], ["Total = 42 + 18 + 30 + 10 = 100.", "Salad: 18/100 = 18%."], family="u1_bar_percent", std=IE, check={"kind": "ratio_pct", "num": 18, "den": 100})
    SA(ED, 6, "cp2", "Students were asked whether they play an instrument. Of 120 freshmen, 36 do; of 80 seniors, 28 do. Fill in the missing table entries: freshmen who do not play, seniors who do not play, total who play, and grand total.",
       "84; 52; 64; 200", ["Freshmen not playing: 120 − 36 = 84.", "Seniors not playing: 80 − 28 = 52.", "Total playing: 36 + 28 = 64.", "Grand total: 120 + 80 = 200."],
       family="u1_tw_complete", std=IE)
    MC(ED, 6, "cp2", "In a pie chart of favorite seasons for 200 students, the “summer” slice is 90°. How many students chose summer?", "50", ["90", "25", "45"],
       ["90° is 90/360 = 1/4 of the circle.", "1/4 of 200 = 50 students."], family="u1_pie_angle", std=IE, check={"kind": "product", "values": [0.25, 200], "expect": 50, "no_print_check": "angle fraction"})
    MC(ED, 6, "cp1", "In a study, the conditional distribution of “recommends the product” is 80% for new customers and 80% for returning customers. A segmented bar graph would show",
       "two bars with identical segments, indicating no association", ["one bar much taller than the other", "segments that sum to more than 100%", "a strong association"],
       ["Identical conditional distributions → identical segmented bars."], family="u1_segbar_same", std=IE)
    SA(ED, 4, "cp2", "Escape step. Find the median of this data set: 25, 12, 17, 9, 21, 14, 19.",
       "17", ["Order the data: 9, 12, 14, 17, 19, 21, 25.", "There are n = 7 values.", "The median is the (7 + 1)/2 = 4th value.", "The 4th value is 17."],
       family="u1_median_escape", std=IB, check={"kind": "median", "data": [25, 12, 17, 9, 21, 14, 19]})
    SA(ED, 3, "cp1", "Escape step. Find the IQR of: 4, 7, 9, 11, 13, 16, 18, 21, 24, 27 (quartiles = medians of the lower and upper halves).",
       "12", ["n = 10, so each half has 5 values.", "Lower half 4, 7, 9, 11, 13 → Q1 = 9.", "Upper half 16, 18, 21, 24, 27 → Q3 = 21.", "IQR = 21 − 9 = 12."],
       family="u1_iqr_escape", std=IB, check={"kind": "five_iqr", "data": [4, 7, 9, 11, 13, 16, 18, 21, 24, 27], "verify_only": True, "expect": [4, 9, 14.5, 21, 27, 12]})
    SA(ED, 3, "cp1", "Error analysis. A student finds the standard deviation of 2, 4, 6 like this: mean = 4; deviations −2, 0, 2; “SD = (−2 + 0 + 2)/3 = 0.” Identify the error and find the correct sample standard deviation.",
       "The deviations must be squared before averaging (they always sum to 0). sₓ = √((4 + 0 + 4)/2) = 2.",
       ["Deviations from the mean always add to 0, so they can't be averaged directly.", "Square them: 4, 0, 4; sum = 8.", "Divide by n − 1 = 2: variance = 4.", "sₓ = √4 = 2."], family="u1_sd_error", std=IB, check={"kind": "sd_sample", "data": [2, 4, 6]})
    SA(ED, 8, "cp2", "Error analysis. Using ŷ = 5 + 3x, a student predicts y for x = 4 as “ŷ = (5 + 3)(4) = 32.” Find and fix the error.",
       "Order of operations: multiply 3 by 4 first. ŷ = 5 + 3(4) = 17.", ["The slope multiplies x only.", "ŷ = 5 + 12 = 17."], family="u1_predict_error", std=ID,
       check={"kind": "predict", "a": 5, "b": 3, "x": 4, "expect": 17})


def ed_honors():
    d = [3, 18, 20, 21, 22, 24, 25, 27, 29, 48, 52]
    SA(ED, 2, "honors", "Escape step. How many values in this data set are outliers by the 1.5 × IQR rule (quartiles = medians of the halves, median excluded)? 3, 18, 20, 21, 22, 24, 25, 27, 29, 48, 52",
       "3", ["n = 11, median = 24; lower half 3, 18, 20, 21, 22 → Q1 = 20; upper half 25, 27, 29, 48, 52 → Q3 = 29.", "IQR = 9; 1.5 × IQR = 13.5.",
             "Fences: 20 − 13.5 = 6.5 and 29 + 13.5 = 42.5.", "Outside the fences: 3, 48, 52 → 3 outliers."],
       family="u1_outlier_count_escape", std=IB, check={"kind": "fences_outliers", "data": d, "expect_out": [3, 48, 52], "verify_only": True, "expect": [6.5, 42.5, 3, 48, 52]})


def se():
    S5, S3 = ["APSTATS.II.C.2"], ["APSTATS.II.B.3"]
    SA(SE, 5, "cp1", "Escape step. An experiment studies 3 study methods, 2 lengths of session, and 2 times of day. How many treatments are there?",
       "12", ["Factor 1: 3 levels.", "Factor 2: 2 levels.", "Factor 3: 2 levels.", "Treatments = 3 × 2 × 2 = 12."], family="u2_treatments_escape", std=S5,
       check={"kind": "count_product", "levels": [3, 2, 2]})
    SA(SE, 5, "honors", "Escape step. An experiment has 4 diets and 2 exercise plans, and each treatment is assigned to 3 volunteers. Volunteers drop out of 2 treatment groups, one person each. How many volunteers finish the study?",
       "22", ["Treatments = 4 × 2 = 8.", "Volunteers assigned = 8 × 3 = 24.", "Dropouts = 2.", "Finishing = 24 − 2 = 22."], family="u2_units_escape", std=S5)
    SA(SE, 3, "cp2", "Error analysis. A student says: “Our survey of 2,000 people who answered an online poll can't be biased because the sample is so large.” Explain the error.",
       "Bias comes from how the sample is chosen, not its size. A voluntary online poll overrepresents people with strong opinions, and a larger sample just gives a more precise wrong answer.",
       ["Large n reduces variability only.", "Voluntary response is systematic (biased) selection.", "Fix with random selection from the population."], family="u2_size_bias_error", std=S3)
    SA(SE, 3, "cp1", "Error analysis. A student claims: “We mailed surveys to a random sample, so nonresponse can't cause bias.” Explain why this is wrong.",
       "Random selection doesn't guarantee random response; if people who don't respond differ from those who do, the results are biased even though the original sample was random.",
       ["The selected sample is random.", "Who responds is not random.", "Nonresponders may differ systematically (e.g., busier people)."], family="u2_nonresponse_error", std=S3)


def ap():
    A3, A4, A6, B = ["APSTATS.III.A.3"], ["APSTATS.III.A.4"], ["APSTATS.III.A.6"], ["APSTATS.III.B.2"]
    MC(AP, 3, "cp2", "A bag has 5 red and 3 blue marbles. One marble is drawn and NOT replaced; then a second is drawn. Given the first was red, what is P(second is red)?", "4/7",
       ["5/8", "5/7", "4/8"], ["After removing one red, 4 red of 7 marbles remain.", "P = 4/7 ≈ 0.571."], family="u3_cond_noreplace", std=A3, check={"kind": "cond", "pab": 4, "pb": 7, "verify_only": True, "expect": 4 / 7})
    SA(AP, 3, "cp1", "Error analysis. P(A) = 0.5 and P(B | A) = 0.4. A student writes P(A and B) = 0.5 + 0.4 = 0.9. Identify the error and compute the correct value.",
       "Use the multiplication rule, not addition: P(A and B) = P(A)·P(B | A) = 0.5 × 0.4 = 0.2.",
       ["“And” probabilities use the multiplication rule.", "P(A and B) = P(A)P(B | A).", "= 0.5 × 0.4 = 0.20.", "0.9 cannot be right: P(A and B) can't exceed P(A)."], family="u3_mult_error", std=A3, check={"kind": "indep_and", "pa": 0.5, "pb": 0.4})
    MC(AP, 5, "cp2", "A random variable X counts the number of tails in 2 fair coin tosses. What is P(X = 0)?", "0.25", ["0.5", "0", "0.75"],
       ["Only HH gives 0 tails: 1 of 4 equally likely outcomes."], family="u3_tails2", std=A4, check={"kind": "binom", "n": 2, "p": 0.5, "k": 0, "type": "eq", "no_print_check": "fair coin", "skip_distractors": True})
    SA(AP, 5, "cp2", "Escape step. A spinner has 4 equal sections numbered 1, 2, 3, 4. It is spun twice and X = the sum. How many of the 16 equally likely outcomes give X = 5?",
       "4", ["List outcomes with sum 5:", "(1,4), (2,3), (3,2), (4,1).", "That is 4 outcomes.", "So P(X = 5) = 4/16 = 0.25."], family="u3_spinner_escape", std=A4)
    SA(AP, 6, "cp2", "Escape step. A game pays $20 with probability 0.25, $8 with probability 0.5, and $0 otherwise. Find the expected payout in dollars.",
       "9", ["Payout values: 20, 8, 0 with probabilities 0.25, 0.5, 0.25.", "20(0.25) = 5.", "8(0.5) = 4.", "E = 5 + 4 + 0 = $9."], family="u3_ev_escape", std=A6,
       check={"kind": "rv", "x": [20, 8, 0], "p": [0.25, 0.5, 0.25], "out": "mean", "no_print_check": "remainder"})
    SA(AP, 6, "cp1", "Error analysis. X has distribution x: 0, 1, 2 with P: 0.5, 0.3, 0.2. A student computes E(X) = (0 + 1 + 2)/3 = 1. What is wrong? Give the correct E(X).",
       "The values are not equally likely, so a simple average is wrong; E(X) = 0(0.5) + 1(0.3) + 2(0.2) = 0.7.",
       ["Expected value weights each value by its probability.", "0(0.5) = 0; 1(0.3) = 0.3; 2(0.2) = 0.4.", "E(X) = 0.7.", "The simple average equals E(X) only when outcomes are equally likely."], family="u3_ev_error", std=A6,
       check={"kind": "rv", "x": [0, 1, 2], "p": [0.5, 0.3, 0.2], "out": "mean"})
    SA(AP, 6, "honors", "Escape step. A charity raffle sells 500 tickets at $5 each. Prizes: one $600 prize and four $100 prizes. What is the charity's expected profit per ticket, in dollars?",
       "3", ["Total prize money = 600 + 4(100) = $1,000.", "Expected payout per ticket = 1,000/500 = $2.", "Each ticket costs $5.", "Charity's expected profit = 5 − 2 = $3 per ticket."], family="u3_raffle_escape", std=A6,
       check={"kind": "rv", "x": [600, 100, 0], "p": [1 / 500, 4 / 500, 495 / 500], "out": "mean", "verify_only": True, "expect": 2})
    MC(AP, 8, "cp2", "Two independent random variables have means 12 and 7. What is the mean of their difference (first minus second)?", "5", ["19", "−5", "84"], ["μ_(X−Y) = 12 − 7 = 5."], family="u3_comb_mean2", std=B)
    SA(AP, 8, "cp2", "Error analysis. X and Y are independent with SDs 5 and 12. A student says SD(X + Y) = 5 + 12 = 17. Correct the error.",
       "Add variances, not SDs: SD = √(25 + 144) = √169 = 13.", ["Variances add for independent variables.", "25 + 144 = 169.", "SD = √169 = 13."], family="u3_comb_error", std=B,
       check={"kind": "combine", "signs": [1, 1], "means": [0, 0], "sds": [5, 12], "verify_only": True, "expect": [0, 13]})
    SA(AP, 7, "cp1", "Escape step. A basketball player makes 80% of free throws and takes 25 shots. Find the expected number of misses.",
       "5", ["Let X = number of misses; X ~ Binomial(n = 25, p = 0.2).", "p(miss) = 1 − 0.8 = 0.2.", "μ = np = 25 × 0.2.", "= 5 misses."], family="u3_binom_escape", std=A4,
       check={"kind": "binom_ms", "n": 25, "p": 0.2, "verify_only": True, "expect": [5, 2]})


def si():
    E1, E3, E4, T1, T2, T6, E5 = ["APSTATS.IV.A.1"], ["APSTATS.IV.A.4"], ["APSTATS.IV.A.6"], ["APSTATS.IV.B.1"], ["APSTATS.IV.B.2", "APSTATS.IV.B.4"], ["APSTATS.IV.B.1"], ["APSTATS.IV.A.5"]
    SA(SI, 1, "cp1", "Error analysis. A student reports: “The 95% CI for the mean is 27.4 ± 2.1, so the margin of error is 4.2.” What is wrong?",
       "The margin of error is the ± amount, 2.1; 4.2 is the width of the interval.", ["Interval = estimate ± ME.", "ME = 2.1; width = 2 × 2.1 = 4.2."], family="u4_me_error", std=E1)
    MC(SI, 1, "cp1", "A 90% CI for the mean time to finish a puzzle is (6.8, 9.4) minutes. Which value is the sample mean?", "8.1 minutes", ["1.3 minutes", "2.6 minutes", "9.4 minutes"],
       ["x̄ = midpoint = (6.8 + 9.4)/2 = 8.1."], family="u4_mean_from_ci", std=E1, check={"kind": "me_from_ci", "lo": 6.8, "hi": 9.4, "verify_only": True, "expect": [8.1, 1.3]})
    SA(SI, 3, "cp2", "Error analysis. A student computes a 95% CI for p as p̂ ± 1.96·p̂ with p̂ = 0.40, n = 100, getting (0.016, 0.784). Identify the error and compute the correct interval (three decimals).",
       f"The margin must use the standard error √(p̂(1 − p̂)/n), not p̂ itself. Correct: 0.40 ± 1.96(0.049) → ({fmt(0.4 - 1.96 * math.sqrt(0.0024), 3)}, {fmt(0.4 + 1.96 * math.sqrt(0.0024), 3)})",
       ["SE = √(0.40 × 0.60/100) ≈ 0.049.", "ME = 1.96 × 0.049 ≈ 0.096.", "Interval ≈ (0.304, 0.496).", "The student's interval is far too wide."], family="u4_ci_error", std=E3,
       check={"kind": "ci_prop", "x": 40, "n": 100, "conf": 95, "no_print_check": "x implied by p̂"})
    MC(SI, 3, "cp2", "Which interval is wider, a 90% CI or a 99% CI built from the same sample?", "The 99% CI", ["The 90% CI", "They are the same width", "It depends on the sample size only"],
       ["Higher confidence needs a larger critical value (2.576 vs 1.645)."], family="u4_conf_width", std=E3)
    SA(SI, 3, "cp1", "Escape step. If 100 independent random samples each produce a 95% confidence interval for p, about how many intervals are expected to miss p?",
       "5", ["Each 95% interval captures p with probability 0.95.", "So it misses with probability 0.05.", "Expected misses = 100 × 0.05.", "= 5 intervals (the actual count varies)."], family="u4_miss_escape", std=E3,
       check={"kind": "binom_ms", "n": 100, "p": 0.05, "verify_only": True, "expect": [5, math.sqrt(4.75)]})
    SA(SI, 4, "cp2", "Escape step. A one-sample t interval is built from a random sample of 24 students. How many degrees of freedom are used?",
       "23", ["One-sample t: df = n − 1.", "n = 24.", "df = 24 − 1 = 23.", "(For a regression slope with 24 points, df would be 22.)"], family="u4_df_escape", std=E4)
    for lv, z, alt, fam in [("cp2", 1.40, "gt", "u4_p_cp2b"), ("cp1", -2.90, "lt", "u4_p_cp1b")]:
        pv = 1 - Phi(z) if alt == "gt" else Phi(z)
        num_mc(SI, 6, lv, f"A one-sided test gives z = {fmt(z, 2)} (Hₐ: p {'>' if alt == 'gt' else '<'} p₀). Find the P-value (four decimals) and decide at α = 0.05.", pv,
               [1 - pv, 2 * pv, 0.05], 4, [f"P-value ≈ {fmt(pv, 4)}.", "Decision: " + ("reject H₀." if pv < 0.05 else "fail to reject H₀.")], family=fam, std=T6, bounds=(0, 1),
               check={"kind": "z_p_only", "z": z, "alt": alt})
    SA(SI, 6, "cp2", "Error analysis. A student writes: “P-value = 0.20, so there is a 20% chance the null hypothesis is true.” Explain the error.",
       "A P-value is the probability of getting a result at least as extreme as observed, assuming H₀ is true; it is not the probability that H₀ is true.",
       ["P-values are computed assuming H₀.", "They describe the data's rarity under H₀, not H₀'s probability."], family="u4_pvalue_error", std=T6)
    SA(SI, 6, "honors", "Error analysis. A researcher reports: “P = 0.03, so the probability that our result is due to chance is 3% and the effect is large.” Identify two errors.",
       "(1) P = 0.03 is the probability of a result this extreme IF H₀ (chance alone) were true, not the probability that chance caused it. (2) A small P-value does not mean the effect is large; it may be small but precisely estimated.",
       ["Condition on H₀ when interpreting P.", "Statistical significance ≠ practical importance.", "Report an effect size or confidence interval."], family="u4_pvalue_error2", std=T6)
    MC(SI, 6, "honors", "Two studies test the same hypothesis. Study A (n = 50) gets P = 0.04; Study B (n = 5,000) gets P = 0.04. Which statement is most reasonable?",
       "Study B's observed effect is likely much smaller, since a tiny effect can reach P = 0.04 with a huge sample.", ["The effects are the same size.", "Study A has stronger evidence.", "Study B must be biased."],
       ["For the same P-value, larger n corresponds to a smaller observed difference."], family="u4_p_vs_n", std=T6)
    SA(SI, 7, "cp2", "Error analysis. Testing H₀: μ = 50 with x̄ = 53, s = 6, n = 36, a student computes t = (53 − 50)/6 = 0.5. Fix the error.",
       "Divide by the standard error s/√n, not s: t = 3/(6/√36) = 3/1 = 3.0.", ["SE = s/√n = 6/6 = 1.", "t = (53 − 50)/1 = 3.0."], family="u4_t_error", std=T2,
       check={"kind": "t_stat", "xbar": 53, "mu0": 50, "s": 6, "n": 36})
    MC(SI, 7, "cp1", "A one-sample t test gives t = 1.20 with df = 30. Which conclusion is correct at α = 0.05 for a two-sided test?", "Fail to reject H₀ (P ≈ 0.24)",
       ["Reject H₀ (P ≈ 0.012)", "Reject H₀ (P ≈ 0.024)", "Fail to reject H₀ (P ≈ 0.88)"], ["P = 2P(t₃₀ ≥ 1.20) ≈ 0.24 > 0.05."], family="u4_t_decision", std=T2,
       check={"kind": "t_p_only", "t": 1.20, "df": 30, "alt": "ne", "tol": 0.005})
    SA(SI, 7, "honors", "Escape step. A one-sample t test is run on 18 observations. If the null hypothesis is rejected at α = 0.05 with t = 2.3, how many degrees of freedom were used?",
       "17", ["One-sample t: df = n − 1.", "n = 18.", "df = 17.", "Check: P(t₁₇ ≥ 2.3) ≈ 0.017, so a two-sided P ≈ 0.034 < 0.05 — consistent with rejecting."],
       family="u4_df_escape2", std=T2)
    SA(SI, 8, "cp2", "Error analysis. A student says: “We rejected H₀ at α = 0.05, so there is a 5% chance we made a Type II error.” Correct the statement.",
       "After rejecting H₀, the only possible error is a Type I error; α = 0.05 is the probability of a Type I error when H₀ is true.",
       ["Type II errors only occur when we fail to reject.", "α is P(Type I error | H₀ true)."], family="u4_errors_error", std=T1)
    MC(SI, 8, "cp1", "Which change decreases the probability of a Type II error without changing α?", "Increasing the sample size", ["Decreasing the sample size", "Using a two-sided test instead of one-sided when the direction is known", "Decreasing the true effect size"],
       ["Larger n increases power, reducing P(Type II)."], family="u4_typeII_reduce", std=T1)
    SA(SI, 9, "cp2", "Error analysis. Comparing 40/100 vs 30/100 successes, a student writes: “p̂₁ − p̂₂ = 40 − 30 = 10.” Fix the error.",
       "Use proportions: p̂₁ = 0.40, p̂₂ = 0.30, so p̂₁ − p̂₂ = 0.10.", ["Convert counts to proportions first.", "0.40 − 0.30 = 0.10."], family="u4_two_prop_error", std=E5,
       check={"kind": "ratio", "num": 10, "den": 100, "verify_only": True, "expect": 0.1})


def build():
    ed(); ed_honors(); se(); ap(); si()
