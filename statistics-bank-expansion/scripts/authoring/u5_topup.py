"""Top-up pass: brings every skill/level cell to at least 8 questions."""
from common import *
from math import comb

ED, SE, AP, SI = "exploring-data", "sampling-experimentation", "anticipating-patterns", "statistical-inference"


def mc(u, k, lv, q, c, w, s, fam, std, check=None):
    MC(u, k, lv, q, c, w, s, family=fam, std=std, check=check)


def ttail(t, df, alt):
    return {"gt": float(st.t.sf(t, df)), "lt": float(st.t.cdf(t, df)), "ne": float(2 * st.t.sf(abs(t), df))}[alt]


def unit1():
    S6, S7 = ["APSTATS.I.E"], ["APSTATS.I.D"]
    tab = ("Seat belt use by driver age group (random sample of 500 drivers):\n        | Belted | Not belted | Total\nUnder 25 |  150   |     50     |  200\n25+      |  270   |     30     |  300\nTotal    |  420   |     80     |  500")
    SA(ED, 6, "honors", tab + "\nFind the percent of unbelted drivers who are under 25, and the percent of under-25 drivers who are unbelted (one decimal). Explain why these two percents answer different questions.",
       "62.5% of unbelted drivers are under 25; 25.0% of under-25 drivers are unbelted. They condition on different groups (unbelted drivers vs. under-25 drivers).",
       ["Unbelted drivers: 80; under 25 among them: 50 → 50/80 = 62.5%.", "Under-25 drivers: 200; unbelted among them: 50 → 50/200 = 25.0%.",
        "The denominators differ because the conditions differ.", "Confusing P(A | B) with P(B | A) is a common error."],
       family="u1_tw_reverse_cond", std=S6, check={"kind": "twoway", "table": [[150, 50], [270, 30]], "type": "cond_given_col", "row": 0, "col": 1, "pct": True})
    mc(ED, 6, "honors", tab + "\nWhich statement best describes the association?",
       "Younger drivers are more likely to be unbelted (25% vs 10%), so age group and belt use are associated.",
       ["There is no association because most drivers in both groups are belted.", "Older drivers are more likely to be unbelted because 270 > 150.", "Age causes belt use."],
       ["Compare conditional percents unbelted: 50/200 = 25% vs 30/300 = 10%.", "Different conditional distributions → association (not causation)."], "u1_tw_assoc_honors", S6)
    mc(ED, 7, "cp1", "Which scatterplot description is complete?",
       "There is a strong, negative, linear association between car age and price, with one unusual car that is old but expensive.",
       ["The correlation is high.", "The points go down.", "Car age is related to price."],
       ["Include direction, form, strength, unusual features, and context."], "u1_scatter_describe", S7)
    mc(ED, 9, "cp1", "A regression of exam score on hours studied has residual 6 for a student who studied 3 hours. What does this mean?",
       "The student scored 6 points higher than the line predicted for someone who studied 3 hours.",
       ["The student studied 6 more hours than predicted.", "The student scored 6 points lower than predicted.", "The slope of the line is 6."],
       ["Residual = actual − predicted; positive means above the line."], "u1_resid_interpret", S7)


def unit2():
    S4, S5, S6, S7, S8 = ["APSTATS.II.A.3", "APSTATS.II.A.4"], ["APSTATS.II.C.2"], ["APSTATS.II.C.3"], ["APSTATS.II.C.5"], ["APSTATS.II.D"]
    mc(SE, 4, "cp1", "A study compares lung function of 500 lifelong runners with 500 non-runners. Why can't it show that running improves lung function?",
       "It is observational; runners chose to run and may differ in other ways, such as not smoking.", ["The samples are too small.", "Lung function cannot be measured.", "Both groups had the same size."],
       ["Self-selection lets lurking variables confound the comparison."], "u2_obs_confound", S4)
    mc(SE, 4, "honors", "Researchers find that children who sleep with a night-light are more likely to be nearsighted. A later study finds that nearsighted parents are more likely to use night-lights. What does this suggest?",
       "Parental nearsightedness may be a lurking variable affecting both night-light use and children's eyesight.", ["Night-lights cause nearsightedness.", "Nearsighted children turn on night-lights.", "The first study proves causation."],
       ["A common cause (genetics through parents) can create the association."], "u2_lurking_honors", S4)
    mc(SE, 4, "honors", "A case-control study compares 200 people with a rare disease to 400 similar people without it and looks back at past exposures. Why is this design used for rare diseases?",
       "A random sample or prospective study would contain too few cases; starting from cases makes the comparison possible.", ["It shows causation better than an experiment.", "It avoids all confounding.", "It requires random assignment."],
       ["Retrospective case-control studies are efficient for rare outcomes but remain observational."], "u2_case_control", S4)
    SA(SE, 4, "honors", "A town notices that months with high ice-cream sales also have more drowning deaths. Explain why this is not evidence that ice cream causes drowning, and describe how an analyst could check your explanation with data.",
       "Temperature/season is a lurking variable: hot months increase both ice-cream sales and swimming. Compare the association within months of similar temperature (or adjust for temperature); it should largely disappear.",
       ["The data are observational (no treatment imposed).", "Hot weather drives both variables.", "Holding temperature roughly constant removes much of the shared variation.", "If the association vanishes within temperature groups, the lurking-variable explanation is supported."],
       family="u2_lurking_check", std=S4)
    mc(SE, 5, "honors", "An experiment has 2 factors: fertilizer (none, low, high) and watering (daily, weekly). Each treatment is applied to 4 plants. What is the total number of experimental units and why might more replication be desirable?",
       "24 plants; more plants per treatment make chance differences less likely to hide or mimic real effects.", ["6 plants; replication is unnecessary.", "12 plants; replication causes bias.", "24 plants; replication guarantees significance."],
       ["Treatments = 3 × 2 = 6; units = 6 × 4 = 24.", "Replication reduces the role of chance in comparisons."], "u2_replication_honors", S5,
       check={"kind": "count_product", "levels": [3, 2], "reps": 4, "skip_distractors": True, "no_print_check": "levels listed"})
    mc(SE, 6, "cp1", "A taste test compares two colas. Tasters are told which cup is the famous brand. Why is this a problem?",
       "Knowing the brand can change preferences, so brand reputation is confounded with taste; tasters should be blinded.", ["It reduces the sample size.", "It creates undercoverage.", "Tasters cannot be randomly assigned."],
       ["Blinding removes expectations from the response."], "u2_blind_taste", S6)
    mc(SE, 6, "honors", "In a placebo-controlled trial, many subjects in the drug group correctly guess their group because of a noticeable side effect. What threat does this create?",
       "Blinding is effectively broken, so expectations may influence responses and bias the comparison.", ["The drug becomes a placebo.", "Random assignment is invalid.", "There is no longer a response variable."],
       ["If subjects can tell their treatment, placebo-related effects are no longer balanced."], "u2_blind_broken", S6)
    mc(SE, 7, "cp1", "A researcher has 40 plots: 20 in shade and 20 in sun, and compares two grass seeds. Which randomization is correct for a block design?",
       "Randomly assign 10 shade plots to each seed and 10 sun plots to each seed.", ["Plant seed A in all shade plots and seed B in all sun plots.", "Randomly assign 20 of all 40 plots to each seed, ignoring sun.", "Let the gardener choose the best plots for seed A."],
       ["Treatments are randomized within each block (sun, shade)."], "u2_block_randomize2", S7)
    mc(SE, 7, "honors", "In a matched pairs experiment comparing two pain relievers, each subject takes both drugs on different days. Why include a “washout” period between treatments?",
       "So the first drug's effect does not carry over and contaminate the response to the second drug.", ["To increase the sample size.", "To make the study double-blind.", "To block by gender."],
       ["Carryover effects would confound treatment with order."], "u2_washout", S7)
    mc(SE, 8, "cp1", "A survey of a random sample of 1,000 U.S. adults finds that those who own pets report lower stress. Which conclusion is justified?",
       "Pet ownership and lower stress are associated among U.S. adults.", ["Owning a pet lowers stress.", "Lower stress causes pet ownership.", "The association applies only to the 1,000 adults."],
       ["Random sample → generalize the association; no random assignment → no causation."], "u2_scope_cp1b", S8)
    mc(SE, 8, "cp1", "Students in one teacher's classes were randomly assigned to two homework formats. Format A produced significantly higher scores. To whom does the conclusion best apply?",
       "To students like those in this teacher's classes", ["To all students in the country", "To no one, since students were not randomly selected", "Only to the teacher"],
       ["Random assignment → causation for these students; no random selection → limited generalization."], "u2_scope_cp1c", S8)
    SA(SE, 8, "cp1", "A study finds a statistically significant difference in mean reaction time between two randomly assigned groups. Explain in one or two sentences what “statistically significant” means here.",
       "The difference between the groups is larger than would plausibly occur from the random assignment alone, so chance is an unlikely explanation.",
       ["Random assignment alone produces some differences.", "Significant = too large to be explained by that chance variation alone."], family="u2_significant_meaning", std=S8)
    mc(SE, 8, "honors", "A randomized experiment on 300 volunteer college students finds a new study app raises scores. A company advertises that the app “raises scores for all students.” What is the most important limitation?",
       "The subjects were volunteer college students, so the result may not generalize to other students (e.g., younger or non-volunteers).", ["No causal conclusion is possible.", "The sample is too large.", "The experiment lacked a response variable."],
       ["Causation is supported for similar subjects; generalization needs random selection from the target population."], "u2_overgeneralize", S8)
    mc(SE, 8, "honors", "Which design allows BOTH a cause-and-effect conclusion and generalization to all employees of a company?",
       "Randomly select employees from the company list, then randomly assign them to treatments.", ["Ask for volunteers, then randomly assign them.", "Randomly select employees and record who chooses each option.", "Compare departments that already use different options."],
       ["Random selection + random assignment."], "u2_scope_design", S8)


def unit3():
    A1, A3, A5, A6, PB, PD = ["APSTATS.III.A.1", "APSTATS.III.A.2"], ["APSTATS.III.A.3"], ["APSTATS.III.A.5"], ["APSTATS.III.A.4"], ["APSTATS.III.B.2"], ["APSTATS.III.D.2", "APSTATS.III.D.3"]
    mc(AP, 1, "cp1", "A website says a new app has a 99% satisfaction rate based on 12 reviews. What is the best response?",
       "With only 12 reviews, the proportion can vary a lot; a long-run rate is not well estimated from so few observations.", ["99% is exact, so the app is excellent.", "12 reviews guarantees accuracy within 1%.", "Satisfaction rates are not probabilities."],
       ["Short-run relative frequencies are unstable; the law of large numbers requires many trials."], "u3_small_n", A1)
    SA(AP, 1, "cp1", "A spinner was spun 400 times and landed on red 92 times. Estimate P(red). If the spinner were spun 4,000 more times, about how many reds would you expect?",
       "P(red) ≈ 0.23; about 920 reds", ["Estimate = 92/400 = 0.23.", "Expected reds in 4,000 spins ≈ 0.23 × 4,000 = 920.", "The actual count will vary around 920."],
       family="u3_relfreq_predict", std=A1, check={"kind": "ratio", "num": 92, "den": 400})
    mc(AP, 1, "honors", "In a lottery, each ticket has probability 1/1,000,000 of winning. Someone has bought tickets every week for 20 years without winning. What is true about next week's ticket?",
       "It still has probability 1/1,000,000; past losses do not change it.", ["It is more likely to win because a win is overdue.", "It is less likely to win because the player is unlucky.", "Its probability is 20/1,000,000."],
       ["Independent draws have no memory."], "u3_lottery", A1)
    mc(AP, 1, "honors", "Which statement is the best interpretation of “the probability a randomly chosen new car needs a warranty repair in year one is 0.08”?",
       "Over a very large number of new cars like these, about 8% will need a warranty repair in year one.", ["8 of every 100 cars will need a repair, exactly.", "A car will need a repair 8% of the year.", "Each car is 8% broken."],
       ["Long-run relative frequency interpretation."], "u3_interpret_honors", A1)
    SA(AP, 1, "honors", "A free-throw shooter's long-run percent is 75%. Over her first 8 shots she makes 4. Explain why this does not contradict her 75% rate, and give the expected number of makes in 8 shots.",
       "Expected 6 makes; short runs vary a lot, so 4 of 8 is not unusual enough to contradict a long-run 75% rate.",
       ["Expected = 0.75 × 8 = 6.", "Short sequences of trials vary widely.", "The 75% describes the long run, not every 8-shot set."],
       family="u3_short_run", std=A1, check={"kind": "product", "values": [0.75, 8], "expect": 6})
    MC(AP, 2, "honors", "P(A) = 0.3, P(B) = 0.5, and P(A or B) = 0.65. Are A and B independent?",
       "Yes, because P(A and B) = 0.15 = P(A)P(B)", ["No, because P(A or B) ≠ 0.8", "No, because the events overlap", "It cannot be determined from this information"],
       ["P(A and B) = P(A) + P(B) − P(A or B) = 0.3 + 0.5 − 0.65 = 0.15.", "P(A)P(B) = 0.3 × 0.5 = 0.15, so the events are independent."],
       family="u3_indep_check2", std=A3, check={"kind": "union", "pa": 0.3, "pb": 0.5, "pab": 0.15, "verify_only": True, "expect": 0.65})
    mc(AP, 3, "cp1", "In a class, 40% of students have a part-time job. Among students with a job, 30% have a GPA above 3.5; among those without a job, 45% do. Are having a job and a GPA above 3.5 independent?",
       "No, because P(GPA > 3.5 | job) = 0.30 differs from P(GPA > 3.5 | no job) = 0.45.", ["Yes, because the percents add to 75%.", "Yes, because 40% is less than 50%.", "Cannot tell without the number of students."],
       ["Independence requires the conditional probability to be the same in both groups."], "u3_indep_cond", A3)
    SA(AP, 4, "cp2", "Describe how to use slips of paper to simulate the gender of the next 5 babies born at a hospital, assuming boys and girls are equally likely and births are independent. What counts as one trial?",
       "Put 1 slip “B” and 1 slip “G” in a bag; draw a slip, record it, and replace it; do this 5 times. One trial is the 5 recorded draws.",
       ["Equal numbers of B and G slips give probability 0.5 each.", "Replacing the slip keeps draws independent.", "One trial models 5 births; repeat many trials."], family="u3_sim_slips", std=A5)
    mc(AP, 4, "cp1", "A simulation of 100 trials of “number of rolls to get a 6” gives a mean of 6.3 rolls. The theoretical mean is 6. What explains the difference?",
       "Chance variation in the simulation; more trials would likely bring the average closer to 6.", ["The die must be unfair.", "The theoretical mean is wrong.", "Simulations always overestimate."],
       ["Simulated averages vary around the true mean."], "u3_sim_mean", A5)
    SA(AP, 4, "cp1", "Explain why a simulation that models a 35% chance using single digits 0–3 as “success” is incorrect, and fix it.",
       "Digits 0–3 give 4/10 = 40%, not 35%. Fix: use pairs 00–34 as success and 35–99 as failure.",
       ["Single digits 0–3 are 4 of 10 outcomes = 0.40.", "35% needs 35 of 100 equally likely outcomes.", "Use two-digit numbers 00–99; let 00–34 = success."], family="u3_sim_fix", std=A5)
    mc(AP, 4, "honors", "To estimate the probability that at least two of 23 people share a birthday, a student plans a simulation. Which assumption is built into the usual model?",
       "Each of 365 birthdays is equally likely and people's birthdays are independent.", ["Birthdays cluster in summer.", "At least one person was born on February 29.", "The 23 people are related."],
       ["Using random integers 1–365 assumes equally likely, independent birthdays."], "u3_sim_birthday", A5)
    SA(AP, 4, "honors", "A cereal box contains one of 3 equally likely prizes. A simulation of “boxes needed to collect all 3 prizes” gives these 10 trial results: 4, 3, 7, 5, 3, 6, 9, 4, 5, 4. Estimate the expected number of boxes, and compare with the theoretical value 5.5.",
       "Simulated mean = 5.0 boxes; close to the theoretical 5.5, with the difference due to chance in only 10 trials.",
       ["Sum = 4 + 3 + 7 + 5 + 3 + 6 + 9 + 4 + 5 + 4 = 50.", "Mean = 50/10 = 5.0.", "Theoretical: 3(1 + 1/2 + 1/3) = 5.5.", "Only 10 trials, so a difference of 0.5 is expected variation."],
       family="u3_sim_coupon", std=A5, check={"kind": "mean", "data": [4, 3, 7, 5, 3, 6, 9, 4, 5, 4]})
    mc(AP, 4, "honors", "A simulation estimates a probability as 0.12 based on 50 trials. Approximately how much might such an estimate typically vary from the true value?",
       "About 0.05 (the SD of a proportion from 50 trials, √(0.12·0.88/50) ≈ 0.046)", ["About 0.001", "About 0.5", "It cannot vary"],
       ["Simulated proportions behave like sample proportions with n = number of trials."], "u3_sim_precision", A5,
       check={"kind": "phat_ms", "p": 0.12, "n": 50, "verify_only": True, "expect": [0.12, math.sqrt(0.12 * 0.88 / 50)]})
    mc(AP, 5, "cp1", "X = number of heads in 3 tosses of a fair coin. Which is P(X ≥ 1)?", "0.875", ["0.375", "0.5", "0.125"],
       ["P(X = 0) = (1/2)³ = 0.125.", "P(X ≥ 1) = 1 − 0.125 = 0.875."], "u3_atleast_heads", A6, check={"kind": "atleast", "p": 0.5, "n": 3, "no_print_check": "fair coin"})
    SA(AP, 5, "cp1", "A bag has 3 red and 2 blue marbles. Two are drawn with replacement. Let X = number of red marbles drawn. Write the probability distribution of X.",
       "x: 0, 1, 2; P(x): 0.16, 0.48, 0.36", ["P(red) = 0.6 each draw (with replacement, independent).", "P(0) = 0.4² = 0.16; P(1) = 2(0.6)(0.4) = 0.48; P(2) = 0.6² = 0.36.", "Check: 0.16 + 0.48 + 0.36 = 1."],
       family="u3_marbles_dist", std=A6, check={"kind": "binom", "n": 2, "p": 0.6, "k": 1, "type": "eq", "no_print_check": "derived"})
    for lv, fam, q, a, w, s, chk in [
        ("honors", "u3_dist_from_cdf", "The cumulative distribution of X is P(X ≤ 0) = 0.10, P(X ≤ 1) = 0.35, P(X ≤ 2) = 0.80, P(X ≤ 3) = 1. Find P(X = 2).", "0.45", ["0.80", "0.35", "0.25"],
         ["P(X = 2) = P(X ≤ 2) − P(X ≤ 1) = 0.80 − 0.35 = 0.45."], {"kind": "ratio", "num": 0.45, "den": 1, "no_print_check": "difference"}),
        ("honors", "u3_continuous_interval", "A continuous random variable is uniform from 2 to 8. Find P(3 < X < 6.5).", "0.75", ["0.5", "0.583", "4.5"],
         ["Density height = 1/6.", "P = (6.5 − 3)/6 = 3.5/6 ≈ 0.583."], None),
    ]:
        if fam == "u3_continuous_interval":
            MC(AP, 5, lv, q, "0.583", ["0.75", "0.5", "3.5"], s, family=fam, std=A6, check={"kind": "uniform_area", "a": 2, "b": 8, "lo": 3, "hi": 6.5})
        else:
            MC(AP, 5, lv, q, a, w, s, family=fam, std=A6, check=chk)
    SA(AP, 5, "honors", "A student takes a 3-question quiz, guessing on each (P(correct) = 0.25, independent). Let X = number correct. Find the full probability distribution (four decimals) and the most likely value.",
       "P(0) = 0.4219, P(1) = 0.4219, P(2) = 0.1406, P(3) = 0.0156; 0 and 1 are equally likely (tie)",
       ["X ~ Binomial(3, 0.25).", "P(0) = 0.75³ = 0.4219; P(1) = 3(0.25)(0.75²) = 0.4219.", "P(2) = 3(0.25²)(0.75) = 0.1406; P(3) = 0.25³ = 0.0156.", "Values 0 and 1 tie for most likely."],
       family="u3_quiz_dist", std=A6, check={"kind": "binom", "n": 3, "p": 0.25, "k": 2, "type": "eq"})
    mc(AP, 5, "honors", "Which random variable is NOT discrete?", "The exact time until the next bus arrives", ["The number of buses that arrive in an hour", "The number of passengers on a bus", "The number of stops before your stop"],
       ["Time is measured on a continuum, so it is continuous."], "u3_discrete_honors", A6)
    SA(AP, 5, "honors", "A random variable X takes values 1, 2, 3, 4 with P(X = x) = x/10. Verify this is a valid distribution and find P(X > 2).",
       "Valid: probabilities 0.1, 0.2, 0.3, 0.4 are between 0 and 1 and sum to 1; P(X > 2) = 0.7",
       ["P(1) = 0.1, P(2) = 0.2, P(3) = 0.3, P(4) = 0.4.", "Each is in [0, 1] and they sum to 1.0.", "P(X > 2) = 0.3 + 0.4 = 0.7."],
       family="u3_formula_dist", std=A6, check={"kind": "rv_cum", "x": [1, 2, 3, 4], "p": [0.1, 0.2, 0.3, 0.4], "cond": "x > 2", "no_print_check": "formula"})
    mc(AP, 6, "honors", "A random variable X has E(X) = 5 and SD(X) = 2. What is Var(3X + 1)?", "36", ["37", "18", "12"],
       ["Var(aX + b) = a²Var(X) = 9 × 4 = 36."], "u3_var_lin", ["APSTATS.III.A.6"])
    SA(AP, 7, "honors", "A student guesses on a 10-question true/false quiz. Find P(X ≥ 8), the probability of passing with at least 8 correct (four decimals). Interpret it.",
       f"{fmt(sum(comb(10, i) for i in range(8, 11)) / 1024, 4)}; only about 5.5% of guessers would pass",
       ["X ~ Binomial(10, 0.5).", "P(X ≥ 8) = [C(10,8) + C(10,9) + C(10,10)]/2¹⁰ = (45 + 10 + 1)/1024.", f"= 56/1024 ≈ {fmt(56 / 1024, 4)}.", "Guessing rarely leads to passing."],
       family="u3_tf_quiz", std=A6, check={"kind": "binom", "n": 10, "p": 0.5, "k": 8, "type": "ge", "no_print_check": "true/false"})
    mc(AP, 7, "honors", "X is geometric with p = 0.2. Which is larger, P(X = 1) or P(X = 2)?", "P(X = 1) = 0.2 > P(X = 2) = 0.16", ["P(X = 2) is larger", "They are equal", "Cannot tell"],
       ["Geometric probabilities decrease: P(1) = p, P(2) = (1 − p)p.", "0.2 > 0.16; the most likely value of a geometric variable is always 1."], "u3_geom_mode", A6,
       check={"kind": "geom", "p": 0.2, "k": 1, "type": "eq", "skip_distractors": True})
    for lv, q, a, w, s, chk in [
        ("cp2", "X and Y are independent with means 40 and 25. What is the mean of X − Y?", "15", ["65", "−15", "Cannot be found"], ["μ_(X−Y) = 40 − 25 = 15."], None),
        ("cp2", "A gift box holds a mug (mean weight 350 g, SD 10 g) and candy (mean 200 g, SD 15 g), independent. What is the mean total weight?", "550 g", ["150 g", "525 g", "565 g"], ["Means add: 350 + 200 = 550 g."], None),
        ("cp1", "Using the gift box (mug: mean 350 g, SD 10 g; candy: mean 200 g, SD 15 g; independent), what is the SD of the total weight? Round to two decimals.", f"{fmt(math.sqrt(325), 2)} g", ["25.00 g", "5.00 g", "325.00 g"],
         ["Var = 10² + 15² = 325.", "SD = √325 ≈ 18.03 g."], {"kind": "combine", "signs": [1, 1], "means": [350, 200], "sds": [10, 15], "verify_only": True, "expect": [550, math.sqrt(325)]}),
        ("cp1", "Two independent random variables each have SD 6. What is the SD of their difference? Round to two decimals.", f"{fmt(math.sqrt(72), 2)}", ["0.00", "12.00", "72.00"],
         ["Var = 36 + 36 = 72.", "SD = √72 ≈ 8.49."], {"kind": "combine", "signs": [1, -1], "means": [0, 0], "sds": [6, 6], "no_print_check": "repeated", "verify_only": True, "expect": [0, math.sqrt(72)]}),
    ]:
        MC(AP, 8, lv, q, a, w, s, family="u3_comb_topup", std=PB, check=chk)
    SA(AP, 8, "cp1", "A student's math score M has mean 520, SD 80; reading score R has mean 510, SD 70; assume independence. Find the mean and SD of the total M + R (two decimals).",
       f"Mean 1,030; SD ≈ {fmt(math.sqrt(80 ** 2 + 70 ** 2), 2)}", ["Mean = 520 + 510 = 1,030.", "Var = 80² + 70² = 11,300.", f"SD ≈ {fmt(math.sqrt(11300), 2)}."],
       family="u3_comb_scores", std=PB, check={"kind": "combine", "signs": [1, 1], "means": [520, 510], "sds": [80, 70]})
    SA(AP, 8, "cp1", "Using M (mean 520, SD 80) and R (mean 510, SD 70), independent and Normal, find P(M > R) using z rounded to two decimals; give four decimals.",
       f"≈ {fmt(1 - Phi(round(-10 / math.sqrt(11300), 2)), 4)}",
       ["D = M − R: mean 10, SD √11,300 ≈ 106.30.", f"z = (0 − 10)/106.30 ≈ {fmt(round(-10 / math.sqrt(11300), 2), 2)}.", f"P(D > 0) ≈ {fmt(1 - Phi(round(-10 / math.sqrt(11300), 2)), 4)}."],
       family="u3_comb_prob2", std=PB, check={"kind": "combine_prob", "signs": [1, -1], "means": [520, 510], "sds": [80, 70], "c": 0, "type": "gt"})
    mc(AP, 8, "honors", "X has SD 3. A student claims SD(X + X) = SD(2X) = √(9 + 9) ≈ 4.24. What is the error?",
       "X + X is not a sum of independent variables; it equals 2X, whose SD is 2 × 3 = 6.", ["There is no error.", "The SD should be 3.", "The SD should be 18."],
       ["Variances add only for independent variables; X is perfectly dependent on itself."], "u3_comb_dependence", PB)
    SA(AP, 8, "honors", "Each of 4 independent packages has weight with mean 2.5 kg and SD 0.3 kg. Compare the SD of the total weight of the 4 packages with the SD of 4 times one package's weight.",
       "Total: mean 10 kg, SD = √(4 × 0.09) = 0.6 kg; 4X: SD = 4 × 0.3 = 1.2 kg. Independent variation partly cancels in the sum.",
       ["Sum of 4 independent: Var = 4(0.3²) = 0.36 → SD 0.6.", "4X: SD = 4 × 0.3 = 1.2.", "The sum is less variable because highs and lows tend to offset."],
       family="u3_sum_vs_scale", std=PB, check={"kind": "combine", "signs": [1, 1, 1, 1], "means": [2.5] * 4, "sds": [0.3] * 4, "no_print_check": "repeated"})
    SA(AP, 9, "honors", "A population has μ = 40 and σ = 10 and is roughly Normal. Find the probability that the mean of a random sample of 25 differs from 40 by more than 3 (z to two decimals; four decimals).",
       f"≈ {fmt(2 * (1 - Phi(1.5)), 4)}", ["σ_x̄ = 10/√25 = 2.", "|x̄ − 40| > 3 means z beyond ±1.50.", f"P = 2(1 − Φ(1.50)) ≈ {fmt(2 * (1 - Phi(1.5)), 4)}."],
       family="u3_xbar_twotail", std=PD, check={"kind": "xbar_prob", "mu": 40, "sigma": 10, "n": 25, "c": 43, "type": "gt", "verify_only": True, "expect": 1 - Phi(1.5)})
    mc(AP, 10, "cp2", "Which statistic is an unbiased estimator of the population proportion p?", "p̂", ["The sample size", "The sample range", "The margin of error"],
       ["μ_p̂ = p."], "u3_unbiased_phat", PD)
    mc(AP, 10, "cp1", "A statistic's sampling distribution for n = 50 has SD 4. Approximately what is its SD for n = 200?", "2", ["1", "4", "8"],
       ["SD ∝ 1/√n; n × 4 → SD ÷ 2."], "u3_sd_scale", PD)
    mc(AP, 10, "cp1", "A survey has a biased sampling frame. What happens if the sample size is increased from 500 to 5,000?",
       "Variability decreases, but the bias remains.", ["The bias disappears.", "Both bias and variability increase.", "Nothing changes."], ["Sample size affects variability, not bias."], "u3_bias_size", PD)
    mc(AP, 10, "honors", "For a strongly right-skewed population, which sample size gives an approximately Normal sampling distribution of x̄?", "n = 60",
       ["n = 5", "n = 10", "No sample size works for skewed populations"], ["The CLT requires larger n for skewed populations (n ≥ 30 rule of thumb; more for strong skew)."], "u3_clt_n", PD)


def unit4():
    E1, E2, E3, E4, T1, T2, E5, E7, E8 = ["APSTATS.IV.A.1"], ["APSTATS.IV.A.3"], ["APSTATS.IV.A.4"], ["APSTATS.IV.A.6"], ["APSTATS.IV.B.1"], ["APSTATS.IV.B.2", "APSTATS.IV.B.4"], ["APSTATS.IV.A.5", "APSTATS.IV.B.3"], ["APSTATS.IV.A.7", "APSTATS.IV.B.5"], ["APSTATS.IV.A.8"]
    mc(SI, 1, "cp1", "A 95% CI for μ is (12.4, 15.0). What is the margin of error?", "1.3", ["2.6", "13.7", "0.65"], ["ME = (15.0 − 12.4)/2 = 1.3."], "u4_me_from_ci2", E1,
       check={"kind": "me_from_ci", "lo": 12.4, "hi": 15.0, "verify_only": True, "expect": [13.7, 1.3]})
    mc(SI, 1, "cp1", "The standard error of x̄ is computed as", "sₓ/√n", ["σ/n", "√n/sₓ", "sₓ·√n"], ["SE_x̄ = sₓ/√n."], "u4_se_mean", E1)
    SA(SI, 1, "cp1", "A random sample of 36 apples has mean weight 152 g and SD 18 g. Find the standard error of x̄.", "3 g", ["SE = sₓ/√n = 18/√36 = 18/6 = 3 g.", "It estimates how much x̄ typically varies between samples of 36."],
       family="u4_se_mean_calc", std=E1, check={"kind": "xbar_ms", "mu": 152, "sigma": 18, "n": 36, "verify_only": True, "expect": [152, 3]})
    mc(SI, 1, "honors", "A 95% interval for p is (0.31, 0.39) from n = 500. Without recalculating, which would be the 95% interval from n = 2,000 with the same p̂?", "About (0.33, 0.37)",
       ["About (0.29, 0.41)", "About (0.31, 0.39)", "About (0.35, 0.39)"], ["Quadrupling n halves the ME: 0.04 → 0.02, same center 0.35."], "u4_ci_scale", E1)
    mc(SI, 1, "honors", "Two estimators of a population mean are both unbiased; estimator A's SE is 1.5 and B's is 3.0. Which is better and why?",
       "A, because it has less sampling variability and so gives narrower intervals.", ["B, because a larger SE is more cautious.", "They are equally good because both are unbiased.", "Cannot choose without the sample size."],
       ["Among unbiased estimators prefer the one with smaller variability."], "u4_estimator_compare", E1)
    SA(SI, 1, "honors", "A 99% confidence interval for a mean is (40.2, 47.8) based on a t* of 2.797. Find the sample mean and the standard error.",
       f"x̄ = 44.0; SE ≈ {fmt(3.8 / 2.797, 4)}", ["x̄ = (40.2 + 47.8)/2 = 44.0.", "ME = 3.8 = t*·SE.", f"SE = 3.8/2.797 ≈ {fmt(3.8 / 2.797, 4)}."],
       family="u4_se_from_ci", std=E1, check={"kind": "me_from_ci", "lo": 40.2, "hi": 47.8, "verify_only": True, "expect": [44.0, 3.8]})
    mc(SI, 2, "cp2", "Which interval interpretation is correct for a 95% CI of (0.62, 0.70) for the proportion of students who own a laptop?",
       "We are 95% confident that between 62% and 70% of all students own a laptop.", ["95% of students own a laptop.", "62% to 70% of the sample owns a laptop.", "There is a 95% chance p̂ is in the interval."],
       ["Interpret about the population proportion."], "u4_interpret_cp2b", E2)
    mc(SI, 2, "cp1", "A 95% confidence interval from a convenience sample of 300 shoppers is (0.48, 0.58). What is the main concern?",
       "The sample was not random, so the interval may not capture the population proportion even with 95% confidence.", ["The interval is too narrow.", "The large counts condition fails.", "95% is too high."],
       ["The Random condition is required for the stated confidence level to hold."], "u4_random_condition", E2)
    mc(SI, 2, "honors", "A simulation draws 200 random samples and computes a 90% CI from each. About how many intervals should miss the true parameter, and why might the count differ?",
       "About 20; the number of misses is itself random (roughly binomial with n = 200, p = 0.10).", ["Exactly 20.", "About 180.", "None, if the samples are random."],
       ["Each interval misses with probability 0.10; misses vary."], "u4_capture_sim", E2, check={"kind": "binom_ms", "n": 200, "p": 0.1, "verify_only": True, "expect": [20, math.sqrt(18)]})
    mc(SI, 2, "honors", "A 95% CI for μ is (8.1, 9.9). Which statement is TRUE?",
       "If the true mean is 10, this particular interval missed it.", ["There is a 95% chance μ is between 8.1 and 9.9.", "95% of observations are between 8.1 and 9.9.", "A 99% CI from the same data would be narrower."],
       ["A computed interval either contains μ or not; 99% intervals are wider."], "u4_interpret_trap", E2)
    for lv, x, n, c in [("cp2", 84, 240, 95), ("cp2", 156, 300, 90)]:
        ph = x / n
        me = ZSTAR[c] * math.sqrt(ph * (1 - ph) / n)
        key = f"({fmt(ph - me, 3)}, {fmt(ph + me, 3)})"
        MC(SI, 3, lv, f"In a random sample of {n} students, {x} said they use the school library weekly. Construct a {c}% CI for the proportion of all students who do (three decimals). Conditions have been checked.",
           key, [f"({fmt(ph - m, 3)}, {fmt(ph + m, 3)})" for m in (math.sqrt(ph * (1 - ph) / n), 2 * me, ZSTAR[99] * math.sqrt(ph * (1 - ph) / n))],
           [f"p̂ = {x}/{n} = {fmt(ph, 4)}.", f"ME = {ZSTAR[c]}√(p̂(1 − p̂)/n) ≈ {fmt(me, 4)}.", f"Interval: {key}."], family="u4_ci_prop_topup", std=E3,
           check={"kind": "ci_prop", "x": x, "n": n, "conf": c})
    SA(SI, 3, "cp1", "A school wants a 95% CI for the proportion of students with part-time jobs within ±0.06, and last year's estimate was 0.30. What sample size is needed?",
       "225", ["n ≥ (1.96/0.06)² × 0.30 × 0.70 ≈ 224.1.", "Round up to 225.", "Check: 1.96√(0.21/225) ≈ 0.0599 ≤ 0.06.", "Using p = 0.5 would require 267."],
       family="u4_samp_size_topup", std=E3, check={"kind": "samp_size", "conf": 95, "me": 0.06, "p": 0.3})
    mc(SI, 3, "honors", "Why does a one-proportion z interval perform poorly when p̂ = 0.02 and n = 100?",
       "There are only 2 successes, so the sampling distribution of p̂ is strongly skewed, not Normal.", ["The sample is too large.", "z* should be smaller.", "The 10% condition always fails for small p."],
       ["Large counts fails (2 < 10)."], "u4_small_count", E3)
    mc(SI, 3, "honors", "Two polls of the same population report 52% ± 3% and 47% ± 3%. What is the most reasonable conclusion?",
       "The intervals barely overlap; the difference may reflect sampling variability, different methods, or a real change over time.", ["One poll must be fraudulent.", "Both are certainly correct.", "The true value must be exactly 49.5%."],
       ["Different random samples give different estimates; nonsampling differences may also matter."], "u4_two_polls", E3)
    mc(SI, 4, "cp2", "For a 95% t interval with n = 20, t* ≈ 2.093. Compared with z* = 1.96, why is t* larger?", "The t distribution has heavier tails because σ is estimated by sₓ.",
       ["Because n is large.", "Because the population is skewed.", "Because t* is for proportions."], ["Extra uncertainty from estimating σ."], "u4_tstar_vs_z", E4)
    mc(SI, 4, "cp1", "A one-sample t interval for mean study time (n = 50) is (2.8, 3.6) hours. Which conclusion is valid?",
       "Plausible values for the population mean study time are between 2.8 and 3.6 hours.", ["95% of students study 2.8 to 3.6 hours.", "The sample mean could be 4 hours.", "The population mean must be 3.2 hours."],
       ["The CI is about μ, centered at x̄ = 3.2."], "u4_t_interval_interpret", E4)
    SA(SI, 4, "cp1", "A random sample of 21 trees had mean height 15.3 m and SD 2.1 m (no strong skew). Find df, t* for 90% confidence (three decimals), and the interval (two decimals).",
       f"df = 20; t* ≈ {fmt(tstar(90, 20), 3)}; ({fmt(15.3 - tstar(90, 20) * 2.1 / math.sqrt(21), 2)}, {fmt(15.3 + tstar(90, 20) * 2.1 / math.sqrt(21), 2)})",
       ["df = 21 − 1 = 20.", f"t* ≈ {fmt(tstar(90, 20), 3)}.", f"ME = t*(2.1/√21) ≈ {fmt(tstar(90, 20) * 2.1 / math.sqrt(21), 3)}.", "Interval = 15.3 ± ME."],
       family="u4_t_interval_full", std=E4, check={"kind": "ci_mean", "xbar": 15.3, "s": 2.1, "n": 21, "conf": 90})
    mc(SI, 4, "honors", "With n = 100, a 95% t interval and a 95% z interval (using sₓ for σ) are computed from the same data. How do they compare?",
       "Nearly identical; t* (≈ 1.984) is only slightly larger than z* (1.96).", ["The t interval is twice as wide.", "The z interval is wider.", "They have different centers."],
       ["For large df, t approaches z."], "u4_t_large_df", E4, check={"kind": "tstar", "conf": 95, "df": 99, "skip_distractors": True, "no_print_check": "df = n − 1"})
    for lv, q, a, w, s in [
        ("cp1", "A researcher suspects that more than 60% of commuters drive alone. Let p be the proportion of all commuters who drive alone. Which hypotheses?", "H₀: p = 0.60; Hₐ: p > 0.60",
         ["H₀: p > 0.60; Hₐ: p = 0.60", "H₀: p̂ = 0.60; Hₐ: p̂ > 0.60", "H₀: p = 0.60; Hₐ: p ≠ 0.60"], ["“More than” → Hₐ: p > 0.60."]),
        ("cp1", "Which statement about H₀ and Hₐ is correct?", "They are statements about parameters and are chosen before collecting data.",
         ["They are statements about sample statistics.", "Hₐ is chosen after seeing the data.", "H₀ is what the researcher hopes to prove."], ["Hypotheses describe the population and come from the research question."]),
        ("cp1", "A teacher wonders whether the mean time students spend on homework differs from 60 minutes. Which is the correct alternative?", "Hₐ: μ ≠ 60",
         ["Hₐ: μ > 60", "Hₐ: x̄ ≠ 60", "Hₐ: μ = 60"], ["“Differs” → two-sided."]),
        ("honors", "A manufacturer wants to show its batteries last longer than a competitor's 8-hour mean. A consumer group wants to show they last less than 8 hours. Which statement is true?",
         "They use the same H₀ (μ = 8) but opposite one-sided alternatives.", ["They must use the same alternative.", "The consumer group's H₀ is μ < 8.", "Both should use μ ≠ 8."], ["H₀ is the no-difference value; Hₐ reflects each party's question."]),
        ("honors", "A test of H₀: p = 0.5 is reported as “we accept H₀ because P = 0.31.” What is wrong with the wording?",
         "We fail to reject H₀; the data are consistent with H₀ but do not prove it.", ["Nothing; 0.31 > 0.05 proves H₀.", "We should reject H₀.", "The P-value is too large to report."], ["Never “accept” H₀."]),
        ("honors", "Which research question leads to a two-sided test?", "Is the proportion of left-handed students at this school different from 10%?",
         ["Is the mean wait time longer than 5 minutes?", "Is the defect rate below 2%?", "Do more than half of voters support the bill?"], ["“Different from” has no direction."]),
    ]:
        MC(SI, 5, lv, q, a, w, s, family="u4_hyp_topup", std=T1)
    SA(SI, 5, "honors", "State the hypotheses for each: (1) testing whether a coin is fair; (2) testing whether a new fertilizer increases mean corn yield above 150 bushels per acre. Define parameters.",
       "(1) p = P(heads); H₀: p = 0.5, Hₐ: p ≠ 0.5. (2) μ = mean yield with the fertilizer; H₀: μ = 150, Hₐ: μ > 150.",
       ["A fair coin has p = 0.5; “fair” vs “not fair” is two-sided.", "“Increases” gives a one-sided Hₐ: μ > 150.", "Define each parameter in context."], family="u4_hyp_pair", std=T1)
    for z, alt in [(2.75, "gt"), (-0.86, "ne")]:
        pv = {"gt": 1 - Phi(z), "lt": Phi(z), "ne": 2 * (1 - Phi(abs(z)))}[alt]
        num_mc(SI, 6, "honors", f"A test of Hₐ: p {'>' if alt == 'gt' else '≠'} p₀ gives z = {fmt(z, 2)}. Find the P-value (four decimals) and state the decision at α = 0.01.", pv,
               [pv / 2 if alt == "ne" else 2 * pv, 1 - pv, Phi(z) if alt == "gt" else 1 - Phi(abs(z)) * 0.5], 4,
               [f"P-value ≈ {fmt(pv, 4)}.", "Compare with 0.01: " + ("reject H₀." if pv < 0.01 else "fail to reject H₀.")], family="u4_p_decision", std=T1, bounds=(0, 1),
               check={"kind": "z_p_only", "z": z, "alt": alt})
    mc(SI, 7, "cp2", "Which test answers “Is the proportion of defective chips greater than 2%?” using an SRS of 1,000 chips?", "One-proportion z test", ["One-sample t test", "Two-proportion z test", "Paired t test"],
       ["One categorical variable, one sample → one-proportion z test."], "u4_choose_test2", T2)
    SA(SI, 7, "cp1", "An SRS of 400 voters finds 222 support a measure. Test H₀: p = 0.5 vs Hₐ: p > 0.5 at α = 0.05: give z (two decimals), P-value (four decimals), and a conclusion.",
       f"z ≈ {fmt((222 / 400 - 0.5) / math.sqrt(0.25 / 400), 2)}, P ≈ {fmt(1 - Phi((222 / 400 - 0.5) / math.sqrt(0.25 / 400)), 4)}; reject H₀: convincing evidence a majority support the measure",
       ["p̂ = 222/400 = 0.555.", "z = (0.555 − 0.5)/√(0.25/400) = 0.055/0.025 = 2.20.", f"P = P(Z ≥ 2.20) ≈ {fmt(1 - Phi(2.2), 4)}.", "P < 0.05 → reject H₀."],
       family="u4_z_test_topup", std=T2, check={"kind": "z_test", "p0": 0.5, "x": 222, "n": 400, "alt": "gt"})
    for lv, q, a, w, s in [
        ("cp1", "A test with α = 0.10 has power 0.85 against a particular alternative. What is P(Type II error) for that alternative?", "0.15", ["0.10", "0.85", "0.90"], ["P(Type II) = 1 − 0.85 = 0.15."]),
        ("cp1", "A medical test is used to screen for a disease (H₀: no disease). A false negative corresponds to", "a Type II error", ["a Type I error", "a correct decision", "the power"], ["Failing to detect a real disease = failing to reject a false H₀."]),
        ("honors", "A researcher doubles her sample size but keeps α = 0.05. What happens to P(Type I error) and power?", "P(Type I) stays 0.05; power increases.",
         ["Both increase.", "P(Type I) decreases; power stays the same.", "Both decrease."], ["α sets P(Type I); larger n raises power."]),
        ("honors", "Power against an alternative far from H₀ compared with one close to H₀ is", "higher, because a larger true difference is easier to detect", ["lower", "the same", "always 1"], ["Effect size increases power."]),
    ]:
        MC(SI, 8, lv, q, a, w, s, family="u4_errors_topup", std=T1)
    for lv, q, a, w, s in [
        ("cp2", "Experiment: 52 of 80 students using flashcards passed; 40 of 80 using notes passed. What is the difference in sample proportions (flashcards − notes)?", "0.15", ["12", "0.65", "−0.15"],
         ["p̂_F = 52/80 = 0.65; p̂_N = 40/80 = 0.50.", "Difference = 0.15."]),
        ("cp2", "When testing H₀: p₁ − p₂ = 0, which value is used to compute the standard error?", "The pooled proportion of successes in both samples combined",
         ["p̂₁ only", "0.5", "The margin of error"], ["Under H₀ the proportions are equal, so pool."]),
    ]:
        MC(SI, 9, lv, q, a, w, s, family="u4_two_prop_topup", std=E5, check={"kind": "ratio", "num": 52 * 80 - 40 * 80, "den": 80 * 80, "verify_only": True, "expect": 0.15} if "52 of 80" in q else None)
    mc(SI, 9, "cp1", "A 95% CI for p_city − p_rural is (−0.02, 0.09). Which statement is correct?", "There is not convincing evidence of a difference; 0 is a plausible value.",
       ["City residents definitely have a higher proportion.", "Rural residents have a higher proportion.", "The difference is exactly 0.035."], ["0 is in the interval."], "u4_two_prop_interp2", E5)
    mc(SI, 9, "honors", "A two-proportion z interval requires checking large counts in each group. With p̂₁ = 0.04, n₁ = 150, what is the problem?", "Only 6 successes in group 1, so the Normal approximation is questionable.",
       ["n₁ is too large.", "The 10% condition always fails.", "Nothing; p̂ values never matter."], ["150 × 0.04 = 6 < 10."], "u4_two_prop_counts", E5,
       check={"kind": "large_counts", "n": 150, "p": 0.04, "verify_only": True, "expect": [6, 144]})
    for lv, q, a, w, s in [
        ("cp2", "In a paired t procedure with 15 pairs, how many degrees of freedom are used?", "14", ["28", "15", "13"], ["df = number of pairs − 1 = 14."]),
        ("cp2", "Independent random samples of 20 boys and 22 girls are compared on mean reaction time. Which procedure fits?", "Two-sample t procedure", ["Paired t procedure", "One-proportion z test", "Two-proportion z test"],
         ["Two independent groups, quantitative response."]),
        ("cp1", "Using the conservative method, what df is used for a two-sample t interval with n₁ = 14 and n₂ = 25?", "13", ["37", "24", "38"], ["df = min(14, 25) − 1 = 13."]),
        ("cp1", "A paired t test on before/after weights gives P = 0.002. What does this indicate about the mean difference?", "Convincing evidence that the mean difference is not 0 (in the direction of Hₐ)",
         ["The mean difference is exactly 0.002.", "The weights did not change.", "The test is invalid."], ["Small P → reject H₀: μ_d = 0."]),
    ]:
        MC(SI, 10, lv, q, a, w, s, family="u4_two_t_topup", std=E7)
    out = "Regression output (n = {n}): slope b = {b}, SE_b = {se}."
    for lv, n, b, se, q, a, w, s, chk in [
        ("cp2", 22, 1.6, 0.4, "What is the t statistic for testing H₀: β = 0?", "4.0", ["0.25", "1.6", "6.4"], ["t = b/SE_b = 1.6/0.4 = 4.0."], {"kind": "slope_t", "b": 1.6, "se": 0.4, "n": 22, "alt": "ne", "verify_only": True, "expect": [4.0, ttail(4.0, 20, "ne")]}),
        ("cp2", 22, 1.6, 0.4, "What is the point estimate of the true slope β?", "1.6", ["0.4", "22", "4.0"], ["The sample slope b estimates β."], None),
        ("cp2", 30, -2.3, 0.9, "What does the negative slope suggest about the relationship between x and y in the sample?", "As x increases, predicted y decreases.", ["As x increases, y increases.", "There is no relationship.", "The relationship is curved."],
         ["Negative b → negative association."], None),
        ("cp2", 30, -2.3, 0.9, "Using t* = 2.048 (95%, df 28), find the margin of error for the slope (three decimals).", fmt(2.048 * 0.9, 3), ["0.900", "4.710", "2.048"], ["ME = t*·SE_b = 2.048 × 0.9 = 1.843."], {"kind": "product", "values": [2.048, 0.9]}),
        ("cp1", 12, 3.4, 1.1, "Find the df and the 95% CI for β (three decimals).", f"df = 10; ({fmt(3.4 - tstar(95, 10) * 1.1, 3)}, {fmt(3.4 + tstar(95, 10) * 1.1, 3)})",
         [f"df = 11; ({fmt(3.4 - tstar(95, 11) * 1.1, 3)}, {fmt(3.4 + tstar(95, 11) * 1.1, 3)})", f"df = 10; ({fmt(3.4 - 1.96 * 1.1, 3)}, {fmt(3.4 + 1.96 * 1.1, 3)})", "df = 12; (2.300, 4.500)"],
         ["df = n − 2 = 10; t* ≈ 2.228.", "3.4 ± 2.228(1.1)."], {"kind": "slope_ci", "b": 3.4, "se": 1.1, "n": 12, "conf": 95}),
        ("cp1", 40, 0.15, 0.09, "Does a two-sided test at α = 0.05 give convincing evidence of a linear relationship?", f"No; t ≈ 1.67 and P ≈ {fmt(ttail(0.15 / 0.09, 38, 'ne'), 3)} > 0.05",
         ["Yes; t ≈ 1.67 > 1", "Yes; the slope is positive", "No; the slope must be 0"], ["t = 0.15/0.09 ≈ 1.67, df = 38.", f"P ≈ {fmt(ttail(0.15 / 0.09, 38, 'ne'), 3)}."], {"kind": "slope_t", "b": 0.15, "se": 0.09, "n": 40, "alt": "ne", "skip_distractors": True}),
        ("honors", 16, 0.48, 0.12, "Construct a 99% CI for β (three decimals) and state whether it supports a positive relationship.", f"({fmt(0.48 - tstar(99, 14) * 0.12, 3)}, {fmt(0.48 + tstar(99, 14) * 0.12, 3)}); yes, the whole interval is above 0",
         [f"({fmt(0.48 - 2.576 * 0.12, 3)}, {fmt(0.48 + 2.576 * 0.12, 3)}); yes", f"({fmt(0.48 - tstar(99, 15) * 0.12, 3)}, {fmt(0.48 + tstar(99, 15) * 0.12, 3)}); no", "(0.360, 0.600); yes"],
         ["df = 14; t* ≈ 2.977.", "0.48 ± 2.977(0.12)."], {"kind": "slope_ci", "b": 0.48, "se": 0.12, "n": 16, "conf": 99}),
        ("cp1", 18, 5.2, 1.3, "A student says: “The slope is 5.2, so every additional unit of x adds exactly 5.2 to y.” What is the best correction?", "The slope estimates the change in PREDICTED (mean) y per unit of x; individual y-values vary around the line.",
         ["The slope should be divided by SE_b first.", "The statement is correct.", "The slope gives the change in x per unit of y."], ["Slope describes the mean response, not each individual."], None),
        ("honors", 50, 2.1, 0.7, "If the same data were reported with x measured in units 10 times larger (so b and SE_b are each 10 times larger), what happens to the t statistic?", "It stays the same (3.0).",
         ["It becomes 10 times larger.", "It becomes 10 times smaller.", "It becomes 100 times larger."], ["t = b/SE_b; both scale by the same factor."], None),
        ("honors", 50, 2.1, 0.7, "Which situation would make this slope inference invalid even though n = 50?", "The residual plot shows a clear curved pattern.",
         ["The slope is positive.", "R-sq is 40%.", "SE_b is less than b."], ["Linearity is required."], None),
    ]:
        MC(SI, 11, lv, out.format(n=n, b=b, se=se) + " " + q, a, w, s, family="u4_slope_topup", std=E8, check=chk)


def build():
    unit1(); unit2(); unit3(); unit4()
