"""Statistics audit #7 and #8 (2026-11-18, batch S2). Run after steps.py. Idempotent.
#8  CP drills get a short context: numeric CP prompts under 60 characters are rewritten with the same numbers and the same
    answer (Partner Check pairs keep equal answers and different prompts). Every CP2 item with a worked solution gets a
    first-step hint (the "hint" field), taken from the first solution step when that step does not give the answer away.
#7  Written short answers that the practice grader leaves to self-check get a 2–3 point self-check list ("selfCheck"):
    the key idea, then context, direction or comparison and the supporting numbers, chosen from the model answer."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

N = r'(−?\d+(?:\.\d+)?)'
RULES = [
    (rf'^Find the mean of ([\d., ]+)\.$', lambda m, i: f'{["Quiz scores", "Points scored in a few games", "Minutes spent reading on several nights", "Hours worked on several days"][i % 4]} were {m[1]}. Find the mean.'),
    (rf'^Find the median of ([\d, ]+)\.$', lambda m, i: f'{["Numbers of books read last month by a few students", "Ages of the players on a small team"][i % 2]}: {m[1]}. Find the median.'),
    (rf'^Find the range of ([\d, ]+)\.$', lambda m, i: f'Daily high temperatures (°F) over five days were {m[1]}. Find the range.'),
    (rf'^Mean {N},? (?:and )?SD {N}\. (?:What is the|Find the) z-score of {N}\?*\.?$', lambda m, i: f'Test scores have mean {m[1]} and SD {m[2]}. {["What is the z-score of a score of", "Find the z-score of a student who scored"][i % 2]} {m[3]}{"?" if i % 2 == 0 else "."}'),
    (rf'^Mean {N},? (?:and )?SD {N}\. Which value has (?:a )?z(?:-score of| =) {N}\?$', lambda m, i: f'Times to finish a puzzle have mean {m[1]} and SD {m[2]} minutes. Which time has a z-score of {m[3]}?'),
    (rf'^Q1 = {N} and Q3 = {N}\. Find the upper fence( \(1\.5 × IQR rule\)| for outliers)\.$', lambda m, i: f'{["Commute times (minutes)", "Daily step counts (hundreds)", "Wait times at a clinic (minutes)", "Daily rainfall amounts (mm)"][i % 4]} have Q1 = {m[1]} and Q3 = {m[2]}. Find the upper fence (1.5 × IQR rule).'),
    (rf'^Q1 = {N} and Q3 = {N}\. Find the IQR\.$', lambda m, i: f'Heights of plants in a greenhouse (cm) have Q1 = {m[1]} and Q3 = {m[2]}. Find the IQR.'),
    (rf'^ŷ = {N} ([+−]) {N}x\. Predict y when x = {N}\.$', lambda m, i: f'A line for predicting {(["a test score (y) from hours studied (x)", "weekly sales (y, hundreds of dollars) from ads placed (x)", "plant height (y, cm) from weeks of growth (x)"] if m[2] == "+" else ["minutes of free time (y) from hours of homework (x)", "the price of a used phone (y, tens of dollars) from its age (x, months)"])[i % (3 if m[2] == "+" else 2)]} is ŷ = {m[1]} {m[2]} {m[3]}x. Predict y when x = {m[4]}.'),
    (rf'^ŷ = {N} ([+−]) {N}?x\. Find the residual for the point \({N}, {N}\)\.$', lambda m, i: f'A regression line for {["plant height (cm, y) on weeks of growth (x)", "price (y) on age of a phone (x)"][1 if m[2] == "−" else 0]} is ŷ = {m[1]} {m[2]} {m[3] or ""}x. Find the residual for the observed point ({m[4]}, {m[5]}).'),
    (rf'^Actual y = {N} and predicted ŷ = {N}\. Find the residual\.$', lambda m, i: f'A student’s actual quiz score is y = {m[1]}, and the regression line predicts ŷ = {m[2]}. Find the residual.'),
    (rf'^{N} brands × {N} temperatures\. How many treatments\?$', lambda m, i: f'An experiment tests {m[1]} brands of popcorn at {m[2]} oven temperatures; each brand–temperature combination is a treatment. How many treatments are there?'),
    (rf'^{N} fertilizers × {N} watering levels\. How many treatments\?$', lambda m, i: f'A garden experiment crosses {m[1]} fertilizers with {m[2]} watering levels; each combination is a treatment. How many treatments are there?'),
    (rf'^{N} treatments with {N} plants each\. How many plants\?$', lambda m, i: f'A greenhouse experiment has {m[1]} treatments, with {m[2]} plants randomly assigned to each. How many plants are needed?'),
    (rf'^P\(A\) = {N}\. Find P\(not A\)\.$', lambda m, i: f'Let A = {["a randomly chosen shopper uses a coupon", "a randomly chosen flight is delayed"][i % 2]}. P(A) = {m[1]}. Find P(not A).'),
    (rf'^P\(A and B\) = {N} and P\(B\) = {N}\. Find P\(A \| B\)\.$', lambda m, i: f'For a randomly chosen student, A = {["is a junior", "plays a sport", "has a job"][i % 3]} and B = {["takes the bus", "is in the band", "owns a car"][i % 3]}. P(A and B) = {m[1]} and P(B) = {m[2]}. Find P(A | B).'),
    (rf'^n = {N} and p = {N}\. What is the binomial mean\?$', lambda m, i: f'A player makes each free throw with probability p = {m[2]} and shoots n = {m[1]} free throws (a binomial setting). What is the mean number made?'),
    (rf'^Binomial with n = {N} and p = {N}\. Find the mean\.$', lambda m, i: f'{["Each seed sprouts with probability", "Each customer buys dessert with probability", "Each email is spam with probability", "Each part is defective with probability"][i % 4]} p = {m[2]}, independently. For n = {m[1]} of them, find the mean number (a binomial count).'),
    (rf'^E\(X\) = {N} and E\(Y\) = {N}\. Find E\(X ([+−]) Y\)\.$', lambda m, i: f'{["X = minutes to walk to the bus stop and Y = minutes on the bus", "X = points scored by a team and Y = points allowed", "X = weight of a full box and Y = weight of the empty box"][(i if m[3] == "+" else 1 + i % 2) % 3]}, with E(X) = {m[1]} and E(Y) = {m[2]}. Find E(X {m[3]} Y).'),
    (rf'^X has mean {N} and Y has mean {N}\. What is the mean of X \+ Y\?$', lambda m, i: f'X = hours of sleep on Friday and Y = hours of sleep on Saturday for a student, with means {m[1]} and {m[2]}. What is the mean of X + Y?'),
    (rf'^Independent X and Y have SDs {N} and {N}\. Find Var\(X \+ Y\)\.$', lambda m, i: f'The times for two independent legs of a relay, X and Y, have SDs {m[1]} and {m[2]} seconds. Find Var(X + Y).'),
    (rf'^σ = {N} and n = {N}\. (?:Find|What is) the SD of x̄\??\.?$', lambda m, i: f'{["Battery lives", "Commute times", "Test scores", "Package weights"][i % 4]} have population SD σ = {m[1]}. For random samples of n = {m[2]}, find the SD of x̄.'),
    (rf'^X = 2 or 8, each with probability 0\.5\. Find E\(X\)\.$', lambda m, i: 'A game pays X = 2 or X = 8 points, each with probability 0.5. Find E(X).'),
    (rf'^(?:The |A )?CI (?:for p )?is \({N}, {N}\)\. (?:What is the|Find the) margin of error\??\.?$', lambda m, i: f'A confidence interval for {["the mean commute time (minutes)", "the mean battery life (hours)", "the proportion of voters who support a plan"][2 if float(m[1].replace("−", "-")) < 1 else i % 2]} is ({m[1]}, {m[2]}). Find the margin of error.'),
    (rf'^The CI is \({N}, {N}\)\. What is the point estimate\?$', lambda m, i: f'A confidence interval for the proportion of students who walk to school is ({m[1]}, {m[2]}). What is the point estimate?'),
    (rf'^A 95% CI is {N} ± {N}\. What is the lower endpoint\?$', lambda m, i: f'A 95% confidence interval for the mean heart rate of adults is {m[1]} ± {m[2]} beats per minute. What is the lower endpoint?'),
    (rf'^One-sample t procedure with n = {N}\. (?:What are the df|df)\?$', lambda m, i: f'A one-sample t interval uses a random sample of n = {m[1]} {["batteries", "students", "bolts", "patients"][i % 4]}. How many degrees of freedom does it use?'),
    (rf'^A paired t procedure uses {N} pairs\. df\?$', lambda m, i: f'A paired t procedure compares before-and-after scores for {m[1]} students. How many degrees of freedom does it use?'),
    (rf'^One-sample t on {N} differences\. df\?$', lambda m, i: f'A paired t test is run on the {m[1]} differences between twins’ scores. How many degrees of freedom does it use?'),
    (rf'^p₀ = {N}, n = {N}, {N} successes\. Find z\.$', lambda m, i: f'{["A test of whether a coin is fair uses", "A test of a claimed success rate uses"][i % 2]} p₀ = {m[1]}. In n = {m[2]} trials there are {m[3]} successes. Find the test statistic z.'),
    (rf'^x̄ = {N}, μ₀ = {N}, s = {N}, n = {N}\. Find t\.$', lambda m, i: f'A test of whether the mean wait time differs from μ₀ = {m[2]} seconds uses a random sample of n = {m[4]} with x̄ = {m[1]} and s = {m[3]}. Find t.'),
    (rf'^b = {N} and SE_b = {N}\. Find t for H₀: β = 0\.$', lambda m, i: f'A regression of {["weekly sales on advertising spending", "test score on hours studied", "plant height on fertilizer amount", "fuel used on distance driven"][i % 4]} gives b = {m[1]} and SE_b = {m[2]}. Find t for H₀: β = 0.'),
    (rf'^z = {N} with Hₐ: p ([<>]) p₀\. p-value \(four decimals\)\?$', lambda m, i: f'A one-proportion z test of Hₐ: p {m[2]} p₀ about the share of voters who support a plan gives z = {m[1]}. Find the p-value to four decimal places.'),
    (rf'^P̂₁ = {N} and p̂₂ = {N}\. Find p̂₁ − p̂₂\.$', lambda m, i: f'In two random samples, the proportions who recycle are p̂₁ = {m[1]} in Town 1 and p̂₂ = {m[2]} in Town 2. Find p̂₁ − p̂₂.'),
    (rf'^p̂₁ = {N} and p̂₂ = {N}\. Difference in percentage points\?$', lambda m, i: f'In two random samples, p̂₁ = {m[1]} of seniors and p̂₂ = {m[2]} of juniors have a part-time job. What is the difference in percentage points?'),
    (rf'^Power = {N}\. What is P\(Type II error\)\?$', lambda m, i: f'A test of whether a new drug lowers blood pressure has power {m[1]} against a particular alternative. What is P(Type II error) for that alternative?'),
    (rf'^Power is {N}\. What is P\(Type II error\) as a percent\?$', lambda m, i: f'A test of a new teaching method has power {m[1]} against a particular alternative. What is P(Type II error), as a percent?'),
    (rf'^α = {N}\. What is P\(Type I error\) when H₀ is true\?$', lambda m, i: f'A factory tests its fill machine at significance level α = {m[1]}. If H₀ is true, what is the probability of a Type I error?'),
    (rf'^p-value = {N} and α = {N}\. Decision\?$', lambda m, i: f'A test of whether a new website design raises sales gives p-value = {m[1]}, and α = {m[2]}. What is the decision?'),
    (rf'^A p-value is {N}\. Express it as a percent\.$', lambda m, i: f'A test of a claim about a coin gives a p-value of {m[1]}. Express it as a percent.'),
    (rf'^Of {N} seniors, 25% drive to school\. How many seniors drive\?$', lambda m, i: f'A random sample of {m[1]} seniors is taken, and 25% of them drive to school. How many seniors in the sample drive?'),
    (rf'^What is z\* for (\d+)% confidence\?$', lambda m, i: f'A poll will report a {m[1]}% confidence interval for the proportion of voters who support a plan. What critical value z* does it use?'),
    (rf'^Which z\* value is used for a (\d+)% confidence interval\?$', lambda m, i: f'A quality engineer builds a {m[1]}% confidence interval for the proportion of defective parts. Which z* value is used?'),
    (rf'^Two-sample t with n₁ = {N} and n₂ = {N}, conservative df\?$', lambda m, i: f'A two-sample t test compares samples of n₁ = {m[1]} and n₂ = {m[2]} students. What is the conservative df?'),
    (rf'^Find the sample standard deviation of ([\d., ]+)\.$', lambda m, i: f'{["Three students’ scores on a short quiz", "Lengths (cm) of three seedlings"][i % 2]} were {m[1]}. Find the sample standard deviation.'),
    (rf'^A data set has standard deviation {N}\. What is its variance\?$', lambda m, i: f'The weekly study hours of a class have standard deviation {m[1]} hours. What is the variance?'),
    (rf'^Mean {N}, SD {N}\. Which score has z = {N}\?$', lambda m, i: f'Scores on a history test have mean {m[1]} and SD {m[2]}. Which score has z = {m[3]}?'),
    (rf'^Q1 = {N} and Q3 = {N}\. Find the lower fence for outliers\.$', lambda m, i: f'Reaction times (hundredths of a second) for a class have Q1 = {m[1]} and Q3 = {m[2]}. Find the lower fence for outliers.'),
    (rf'^Q1 = {N} and Q3 = {N}\. Which value is an outlier\?$', lambda m, i: f'Ages of the members of a book club have Q1 = {m[1]} and Q3 = {m[2]}. Which age is an outlier (1.5 × IQR rule)?'),
    (rf'^[rR] = {N}\. What is r²\?$', lambda m, i: f'The correlation between {(["hours of practice and points scored", "height and arm span"] if not m[1].startswith("−") else ["temperature and hot-chocolate sales", "car age and resale value"])[i % 2]} is r = {m[1]}. What is r²?'),
    (rf'^R = {N} after x and y are swapped\. What is r²\?$', lambda m, i: f'A student swaps the roles of x and y for data with correlation r = {m[1]}. What is r² now?'),
    (rf'^r = {N}\. Find 100·r²\.$', lambda m, i: f'The correlation between hours of screen time and hours of sleep is r = {m[1]}. Find 100·r², the percent of variation explained.'),
    (rf'^[rR] = {N}, s_y = {N}, sₓ = {N}\. Find the slope of the LSRL\.$', lambda m, i: f'For hours studied (x) and test score (y), r = {m[1]}, s_y = {m[2]} and sₓ = {m[3]}. Find the slope of the LSRL.'),
    (rf'^R = {N}, sₓ = {N}, s_y = {N}\. Find the LSRL slope\.$', lambda m, i: f'For {["shoe size (x) and height (y)", "age (x) and reading level (y)"][i % 2]}, r = {m[1]}, sₓ = {m[2]} and s_y = {m[3]}. Find the LSRL slope.'),
    (rf'^Slope {N}, x̄ = {N}, ȳ = {N}\. Find the y-intercept of the LSRL\.$', lambda m, i: f'For weeks of growth (x) and plant height (y), the LSRL has slope {m[1]}, with x̄ = {m[2]} and ȳ = {m[3]}. Find the y-intercept.'),
    (rf'^ŷ = {N} \+ {N}x\. For the point \({N}, {N}\), find the residual\.$', lambda m, i: f'A line for predicting quiz score (y) from hours studied (x) is ŷ = {m[1]} + {m[2]}x. For the student at ({m[3]}, {m[4]}), find the residual.'),
    (rf'^ŷ = {N} \+ {N}x\. Find ŷ at x = {N}\.$', lambda m, i: f'A line for predicting the cost of a taxi ride (y, dollars) from miles driven (x) is ŷ = {m[1]} + {m[2]}x. Find ŷ at x = {m[3]}.'),
    (rf'^For the regression ŷ = {N} \+ {N}x, r² = {N}\. What is r\?$', lambda m, i: f'A regression of quiz score on hours studied is ŷ = {m[1]} + {m[2]}x, with r² = {m[3]}. What is r?'),
    (rf'^X is N\({N}, {N}\)\. Find P\(X ([<>]) {N}\) \(four decimals\)\.$', lambda m, i: f'{["Test scores", "IQ scores"][i % 2]} X are Normal with mean {m[1]} and SD {m[2]}, N({m[1]}, {m[2]}). Find P(X {m[3]} {m[4]}) to four decimal places.'),
    (rf'^Of {N} (\w+), {N} (\w+)\. Find P\((\w+) \| (\w+)\)\.$', lambda m, i: f'A school surveys {m[1]} {m[2]}; {m[3]} of them {"drive to school" if m[4] == "drive" else "have part-time jobs"}. Find P({m[5]} | {m[6]}).'),
    (rf'^{N} factors with {N}, {N}, and {N} levels\. How many treatments\?$', lambda m, i: f'A baking experiment has {m[1]} factors: oven temperature ({m[2]} levels), sugar amount ({m[3]} levels) and pan type ({m[4]} levels). How many treatments are there?'),
    (rf'^{N} × {N} treatments; {N} units per treatment\. Units needed\?$', lambda m, i: f'A crop experiment crosses {m[1]} seed types with {m[2]} watering levels, with {m[3]} plots per treatment. How many plots are needed?'),
    (rf'^P\(A\) = {N}, P\(B\) = {N}, independent\. Find P\(A and B\)\.$', lambda m, i: f'A = a flight is on time and B = the bags arrive on time are independent, with P(A) = {m[1]} and P(B) = {m[2]}. Find P(A and B).'),
    (rf'^P\(A\) = {N}, P\(B\) = {N}, P\(A and B\) = {N}\. Find P\(A or B\)\.$', lambda m, i: f'For a randomly chosen student, A = takes art and B = takes band, with P(A) = {m[1]}, P(B) = {m[2]} and P(A and B) = {m[3]}. Find P(A or B).'),
    (rf'^P\(B \| A\) = {N} and P\(A\) = {N}\. Find P\(A and B\)\.$', lambda m, i: f'For a randomly chosen shopper, A = buys bread and B = buys butter. P(B | A) = {m[1]} and P(A) = {m[2]}. Find P(A and B).'),
    (rf'^P\(A\) = {N} and P\(B \| A\) = {N}\. Find P\(A and B\)\.$', lambda m, i: f'For a randomly chosen student, A = plays a sport and B = has a physical this month. P(A) = {m[1]} and P(B | A) = {m[2]}. Find P(A and B).'),
    (rf'^P\(A and B\) = {N} and P\(A\) = {N}\. Find P\(B \| A\)\.$', lambda m, i: f'For a randomly chosen adult, A = owns a car and B = commutes by car. P(A and B) = {m[1]} and P(A) = {m[2]}. Find P(B | A).'),
    (rf'^X has probabilities {N}, {N}, {N}, k\. Find k\.$', lambda m, i: f'X = the number of pets in a household takes values 0, 1, 2 and 3 with probabilities {m[1]}, {m[2]}, {m[3]} and k. Find k.'),
    (rf'^X = 0, 1, 2 with probabilities {N}, {N}, {N}\. Find E\(X\)\.$', lambda m, i: f'X = the number of cars a family owns is 0, 1 or 2 with probabilities {m[1]}, {m[2]} and {m[3]}. Find E(X).'),
    (rf'^SD\(X\) = {N}\. (?:What is|Find) SD\(([^)]+)\)\??\.?$', lambda m, i: f'{["X = minutes a bus is late", "X = the weight of a package in pounds", "X = the score on a quiz"][i % 3]} has SD(X) = {m[1]}. Find SD({m[2]}).'),
    (rf'^E\(X\) = {N}\. Find E\(([^)]+)\)\.$', lambda m, i: f'{["X = points scored per game", "X = customers served per hour"][i % 2]} has E(X) = {m[1]}. Find E({m[2]}).'),
    (rf'^Independent X and Y have SDs {N} and {N}\. (?:SD of X \+ Y\?|Find SD\(X ([+−]) Y\)\.)$', lambda m, i: f'{["X = time to cook and Y = time to serve a meal", "X = time to drive to work and Y = time to park", "X = length of part A and Y = length of part B"][i % 3]} are independent, with SDs {m[1]} and {m[2]}. Find SD(X {m[3] or "+"} Y).'),
    (rf'^Var\(X\) = {N} and Var\(Y\) = {N}, independent\. Find Var\(X − Y\)\.$', lambda m, i: f'Two machines fill bags independently; the fills X and Y have Var(X) = {m[1]} and Var(Y) = {m[2]}. Find Var(X − Y).'),
    (rf'^E\(X\) = {N} and E\(Y\) = {N}\. Find E\(2X \+ Y\)\.$', lambda m, i: f'A game awards 2 points per goal (X) plus bonus points (Y), with E(X) = {m[1]} and E(Y) = {m[2]}. Find E(2X + Y).'),
    (rf'^[pP] = {N} and n = {N}\. (?:What is|Find) the SD of p̂\??\.?$', lambda m, i: f'{["In a large city", "In a big school district", "In a state"][i % 3]}, the proportion of residents who recycle is p = {m[1]}. For random samples of n = {m[2]}, find the SD of p̂.'),
    (rf'^To halve the SD of x̄, multiply the sample size by …$', lambda m, i: 'A researcher wants the SD of x̄ for battery lives to be half as large. To halve the SD of x̄, multiply the sample size by …'),
    (rf'^By what factor must n be multiplied to halve the SD of (x̄|p̂)\?$', lambda m, i: f'A poll wants to halve the SD of {m[1]}. By what factor must the sample size n be multiplied?'),
    (rf'^σ = {N}\. Smallest n so that the SD of x̄ is at most {N}\?$', lambda m, i: f'{["Package weights have σ = " + m[1] + " grams", "Commute times have σ = " + m[1] + " minutes"][i % 2]}. What is the smallest n so that the SD of x̄ is at most {m[2]}?'),
    (rf'^σ = {N} and the SD of x̄ is {N}\. Find n\.$', lambda m, i: f'Commute times have σ = {m[1]} minutes, and the SD of x̄ for random samples is {m[2]}. Find n.'),
    (rf'^X is uniform from 0 to {N}\. Find P\(X < {N}\)\.$', lambda m, i: f'A bus arrives at a random time X minutes after you reach the stop, uniform from 0 to {m[1]}. Find P(X < {m[2]}).'),
    (rf'^P\(X ≤ 2\) = {N} and P\(X ≤ 3\) = {N}\. Find P\(X = 3\)\.$', lambda m, i: f'X = the number of siblings of a randomly chosen student has P(X ≤ 2) = {m[1]} and P(X ≤ 3) = {m[2]}. Find P(X = 3).'),
    (rf'^p̂ = {N} and n = {N}\. (?:What is the standard error|Find the standard error of p̂)\??\.?$', lambda m, i: f'In a random sample of n = {m[2]} {["voters", "shoppers", "students"][i % 3]}, p̂ = {m[1]} {["support a new park", "use a coupon", "walk to school"][i % 3]}. Find the standard error of p̂.'),
    (rf'^s = {N} and n = {N}\. (?:What is the SE|Find the (?:SE|standard error)) of x̄\??\.?$', lambda m, i: f'A random sample of n = {m[2]} {["batteries", "bags of chips", "students", "commuters"][i % 4]} has s = {m[1]}. Find the standard error of x̄.'),
    (rf'^95% confidence, ME ≤ {N}, p = {N}\. Minimum n\?$', lambda m, i: f'A poll wants a 95% confidence margin of error of at most {m[1]}, using p = {m[2]}. What is the minimum sample size n?'),
    (rf'^Two-sample t with n₁ = {N} and n₂ = {N}\. Conservative df\?$', lambda m, i: f'A two-sample t test compares random samples of n₁ = {m[1]} {["juniors", "morning commuters"][i % 2]} and n₂ = {m[2]} {["seniors", "evening commuters"][i % 2]}. What is the conservative df?'),
    (rf'^p₀ = {N}, n = {N}, p̂ = {N}\. Find z\.$', lambda m, i: f'A test of whether a coin is fair uses p₀ = {m[1]}; in n = {m[2]} flips, p̂ = {m[3]}. Find z.'),
    (rf'^Pool {N}/{N} and {N}/{N}\. (?:What is the pooled proportion|Pooled proportion|Pooled proportion as a percent)\?$', lambda m, i: f'In a two-proportion z test, {m[1]} of {m[2]} in group 1 and {m[3]} of {m[4]} in group 2 {["recycle", "vote early", "own a bike"][i % 3]}. Find the pooled proportion{" as a percent" if "percent" in m[0] else ""}.'),
    (rf'^(?:A regression uses n = {N} points\. df for slope inference|Slope inference (?:from|with) n = {N} points\. df)\?$', lambda m, i: f'A regression of {["fuel used on miles driven uses n = " + (m[1] or m[2]) + " cars", "house price on size uses n = " + (m[1] or m[2]) + " houses", "test score on study time uses n = " + (m[1] or m[2]) + " students"][i % 3]}. How many degrees of freedom does slope inference use?'),
    (rf'^One-sample t with n = {N}\. df\?$', lambda m, i: f'A one-sample t test uses a random sample of n = {m[1]} light bulbs. What are the degrees of freedom?'),
    (rf'^Z\* = {N} and SE = {N}\. Margin of error \(three decimals\)\?$', lambda m, i: f'A 95% interval for the proportion of voters who support a plan uses z* = {m[1]} and SE = {m[2]}. Find the margin of error (three decimals).'),
    (rf'^Two-sided test with z = {N}\. p-value\?$', lambda m, i: f'A two-sided test of whether a die is fair gives z = {m[1]}. What is the p-value?'),
    (rf'^One-sided test \(Hₐ: >\) with z = {N}\. p-value\?$', lambda m, i: f'A one-sided test (Hₐ: p > p₀) of a new teaching method gives z = {m[1]}. What is the p-value?'),
    (rf'^Power against an alternative is {N}\. P\(Type II error\)\?$', lambda m, i: f'A test of a new drug has power {m[1]} against a particular alternative. What is P(Type II error)?'),
    (rf'^Group 1 mean {N} and group 2 mean {N}\. Difference of means\?$', lambda m, i: f'Two independent random samples of students give mean test scores of {m[1]} (group 1) and {m[2]} (group 2). What is the difference of means (group 1 − group 2)?'),
    (rf'^Paired differences have d̄ = {N}, s_d = {N}, n = {N}\. Find t\.$', lambda m, i: f'Before-and-after scores for n = {m[3]} students give differences with d̄ = {m[1]} and s_d = {m[2]}. Find t for H₀: μ_d = 0.'),
    (rf'^A fair die is rolled {N} times\. Expected number of 6s\?$', lambda m, i: f'In a board game, a fair die is rolled {m[1]} times. What is the expected number of 6s?'),
    (rf'^Find the sample standard deviation of ([\d., ]+) by hand\. (.+)$', lambda m, i: f'Five students recorded the hours they slept last night: {m[1]}. Find the sample standard deviation by hand. {m[2]}'),
    (rf'^r = {N} after x and y are swapped\. What is r²\?$', lambda m, i: f'For {"height (x) and weight (y)" if not m[1].startswith("−") else "outside temperature (x) and heating cost (y)"}, r = {m[1]}. A student swaps x and y and recomputes. What is r²?'),
    (rf'^r = {N}, sₓ = {N}, s_y = {N}\. Find the LSRL slope\.$', lambda m, i: f'For {["shoe size (x) and height (y)", "age (x) and reading level (y)"][i % 2]}, r = {m[1]}, sₓ = {m[2]} and s_y = {m[3]}. Find the LSRL slope.'),
    (rf'^r = {N}\. What percent of the variation in y is explained by the linear model \(r² as a percent\)\?$', lambda m, i: f'For {"hours of practice (x) and points scored (y)" if not m[1].startswith("−") else "hours of exercise (x) and resting pulse (y)"}, r = {m[1]}. What percent of the variation in y is explained by the linear model (r² as a percent)?'),
    (rf'^r = {N}, s_y = {N}, sₓ = {N}, x̄ = {N}, ȳ = {N}\. Find the y-intercept of the LSRL\.$', lambda m, i: f'For hours studied (x) and quiz score (y), r = {m[1]}, s_y = {m[2]}, sₓ = {m[3]}, x̄ = {m[4]} and ȳ = {m[5]}. Find the y-intercept of the LSRL.'),
    (rf'^P\(A\) = {N} and P\(B\) = {N}, and A and B are independent\. What is P\(A or B\)\?$', lambda m, i: f'A = the first traffic light is green and B = the second light is green are independent, with P(A) = {m[1]} and P(B) = {m[2]}. What is P(A or B)?'),
    (rf'^n = {N} and p = {N}\. Find P\(X = {N}\)\. (.+)$', lambda m, i: f'A fair coin is tossed n = {m[1]} times, so p = {m[2]} for heads. Find P(X = {m[3]}), where X is the number of heads. {m[4]}'),
    (rf'^P\(rain\) = {N} each day\. Expected number of rainy days in {N} days\?$', lambda m, i: f'In a town, P(rain) = {m[1]} each day, independently. What is the expected number of rainy days in {m[2]} days?'),
    (rf'^X = 0, 1, 2, 3 with probabilities {N}, {N}, {N}, {N}\. (.+)$', lambda m, i: f'X = the number of {["books a student reads in a month", "texts a student sends in class", "late buses in a week"][i % 3]} is 0, 1, 2 or 3 with probabilities {m[1]}, {m[2]}, {m[3]} and {m[4]}. {m[5]}'),
    (rf'^Binomial with n = {N} and p = {N}\. Find the SD \(three decimals\)\.$', lambda m, i: f'{["Each free throw is made with probability", "Each coin toss lands heads with probability"][i % 2]} p = {m[2]}, independently. X counts successes in n = {m[1]} tries (binomial). Find the SD of X (three decimals).'),
    (rf'^P\(A\) = {N} and P\(B \| A\) = {N}\. Among {N} people, expected number with A and B\?$', lambda m, i: f'For a randomly chosen adult, A = owns a dog and B = walks daily. P(A) = {m[1]} and P(B | A) = {m[2]}. Among {m[3]} people, what is the expected number with A and B?'),
    (rf'^P\(A\) = {N}, P\(B\) = {N}, P\(A and B\) = {N}\. Are A and B independent\?$', lambda m, i: f'For a randomly chosen student, A = takes Spanish and B = plays a sport, with P(A) = {m[1]}, P(B) = {m[2]} and P(A and B) = {m[3]}. Are A and B independent?'),
    (rf'^E\(X\) = {N} and SD\(X\) = {N}\. Find the mean and SD of X \+ 10\.$', lambda m, i: f'X = a student’s score on a quiz has E(X) = {m[1]} and SD(X) = {m[2]}. Every score gets 10 bonus points. Find the mean and SD of X + 10.'),
    (rf'^Var\(X\) = {N} and Var\(Y\) = {N}, independent\. Find SD\(X − Y\)\. (.+)$', lambda m, i: f'The weights X and Y of two independently filled bags have Var(X) = {m[1]} and Var(Y) = {m[2]}. Find SD(X − Y). {m[3]}'),
    (rf'^μ = {N}\. What is the mean of the sampling distribution of x̄\?$', lambda m, i: f'Battery lives have population mean μ = {m[1]} hours. What is the mean of the sampling distribution of x̄ for random samples of 25 batteries?'),
    (rf'^p = {N} and n = {N}\. Find the SD of p̂\. (.+)$', lambda m, i: f'In a large school, p = {m[1]} of students bike to school. For random samples of n = {m[2]}, find the SD of p̂. {m[3]}'),
    (rf'^p = {N} and n = {N}\. Is the Normal approximation for p̂ appropriate\?$', lambda m, i: f'About p = {m[1]} of a factory’s parts are defective. For random samples of n = {m[2]} parts, is the Normal approximation for p̂ appropriate?'),
    (rf'^p̂ = {N}, n = {N}, (\d+)% confidence\. (.+)$', lambda m, i: f'In a random sample of n = {m[2]} {["voters", "shoppers", "students"][i % 3]}, p̂ = {m[1]} {["support a new library", "pay with a phone", "have a part-time job"][i % 3]}. For {m[3]}% confidence: {m[4][0].lower() + m[4][1:]}'),
    (rf'^p̂ = {N}, n = {N}\. Construct a 95% CI for p\. (.+)$', lambda m, i: f'In a random sample of n = {m[2]} adults, p̂ = {m[1]} say they read the news daily. Construct a 95% CI for p. {m[3]}'),
    (rf'^z = {N} and Hₐ: p ([<>]) p₀\. (.+)$', lambda m, i: f'A one-proportion z test about the share of {["students who walk to school", "customers who return items"][i % 2]} uses Hₐ: p {m[2]} p₀ and gives z = {m[1]}. {m[3]}'),
    (rf'^z\* = {N} and SE = {N}\. Margin of error \(three decimals\)\?$', lambda m, i: f'A 95% interval for the proportion of adults who exercise daily uses z* = {m[1]} and SE = {m[2]}. Find the margin of error (three decimals).'),
    (rf'^P\(reject H₀ \| H₀ is false\) = {N}\. P\(fail to reject \| H₀ false\)\?$', lambda m, i: f'A test of a new fertilizer has P(reject H₀ | H₀ is false) = {m[1]} for a particular effect size. What is P(fail to reject | H₀ false)?'),
    (rf'^x̄ = {N}, s = {N}, n = {N}\. Construct a 95% t interval for μ\. (.+)$', lambda m, i: f'A random sample of n = {m[3]} bags of coffee has mean weight x̄ = {m[1]} grams and s = {m[2]} grams. Construct a 95% t interval for μ. {m[4]}'),
    (rf'^p₀ = {N}, n = {N}, (?:p̂ = {N}|x = {N})\. Find z\. (.+)$', lambda m, i: f'A test of the claim that p₀ = {m[1]} of {["voters favor a bond", "seeds sprout"][i % 2]} uses a random sample of n = {m[2]}{", with p̂ = " + m[3] if m[3] else ", in which x = " + m[4] + " do"}. Find z. {m[5]}'),
    (rf'^t = {N}, df = {N}, Hₐ: μ > μ₀\. (.+)$', lambda m, i: f'A one-sample t test of whether mean study time exceeds μ₀ gives t = {m[1]} with df = {m[2]} (Hₐ: μ > μ₀). {m[3]}'),
    (rf'^p̂₁ = {N} and p̂₂ = {N}, each with n = {N}\. (.+)$', lambda m, i: f'Random samples of n = {m[3]} from each of two towns show p̂₁ = {m[1]} and p̂₂ = {m[2]} who recycle. {m[4]}'),
    (rf'^x̄₁ = {N} and x̄₂ = {N}\. What is the point estimate of μ₁ − μ₂\?$', lambda m, i: f'Two independent random samples of students score x̄₁ = {m[1]} (with tutoring) and x̄₂ = {m[2]} (without). What is the point estimate of μ₁ − μ₂?'),
    (rf'^s₁ = {N} \(n₁ = {N}\) and s₂ = {N} \(n₂ = {N}\)\. (.+)$', lambda m, i: f'Two independent random samples of commute times give s₁ = {m[1]} (n₁ = {m[2]}) and s₂ = {m[3]} (n₂ = {m[4]}) minutes. {m[5]}'),
    (rf'^n = {N}, b = {N}, SE_b = {N}\. (.+)$', lambda m, i: f'A regression of plant growth on hours of light for n = {m[1]} plants gives b = {m[2]} and SE_b = {m[3]}. {m[4]}'),
    (rf'^A 95% CI for μ is \({N}, {N}\)\. Is {N} a plausible value of μ\?$', lambda m, i: f'A 95% confidence interval for the mean number of texts a student sends per hour is ({m[1]}, {m[2]}). Is {m[3]} a plausible value of μ?'),
]


BARE = re.compile(r'^(?:[A-Za-zμσΣχ][̂̄]?[₀-₉ₓ_A-Za-z]{0,3}(?:\([^)]*\))?\*? ?(?:=|≤) ?[−\d(.]|X is N\(|Mean \d|Q1 =|Binomial with|One-sample t|Two-sample t|Two-sided|One-sided|Pool |Independent X|Find the (?:mean|median|range|sample standard deviation) of \d|\d+% confidence,|Power |Group 1 mean|Paired differences|Slope |A regression uses n|To halve|By what factor|Var\(|SD\(|E\(|A data set has|\d+ (?:brands|factors|fertilizers|treatments) |\d+ × |Of \d+ \w+, \d+ \w+\.)')


def numeric_key(q):
    k = lib.key_text(q)
    return bool(re.fullmatch(r'[−\-]?\d+(?:\.\d+)?%?|yes|no|Reject H₀|Fail to reject H₀', k.strip(), re.I))


FIRST_GIVES = re.compile(r'\d')


def hint_for(q):
    st = q['solutionSteps']
    if len(st) < 2 or q['format'] == 'open-response':
        return None
    first = st[0].strip()
    key = lib.key_text(q).strip().rstrip('.')
    if len(first) < 12 or first.startswith('Answer') or first.lower().startswith('identify what is asked') or (key and len(key) > 1 and key in first) or first.lower().startswith(key.lower()[:20]):
        return None
    return 'First step: ' + first[0].lower() + first[1:] if not first[:2].isupper() else 'First step: ' + first


WORDS_CMP = re.compile(r'\b(more|less|higher|lower|greater|larger|smaller|than|increase|decrease|wider|narrower)\b', re.I)
WORDS_DEC = re.compile(r'\b(reject|evidence|convincing|significant|plausible)\b', re.I)
WORDS_CAUSE = re.compile(r'\b(cause|causation|association|confound)', re.I)


def self_check(q):
    a = re.sub(r'^Step \d+:\s*', '', lib.key_text(q).strip())
    if len(a.split()) <= 3 and not re.search(r'\d', a):
        return [f'Names the correct term: “{a.rstrip(".")}”.', 'Can say in one sentence why it fits this situation (what in the question points to it).']
    first = re.split(r'(?<=[.;])\s', a)[0].strip().rstrip('.;').replace('“', '"').replace('”', '"')
    pts = [f'States the key idea: “{first}”.' if len(first) < 140 else 'States the key idea of the model answer.']
    nums = re.findall(r'[−\-]?\d+(?:\.\d+)?%?', a)
    if WORDS_DEC.search(a):
        pts.append('Links the decision to the evidence (the p-value compared with α, or whether the value is in the interval).')
    elif WORDS_CAUSE.search(a):
        pts.append('Says whether a cause-and-effect conclusion is allowed, and why (random assignment or not).')
    elif WORDS_CMP.search(a):
        pts.append('Makes the comparison or direction explicit (which is larger, or which way the change goes).')
    if nums:
        pts.append('Includes the key value(s): ' + ', '.join(dict.fromkeys(nums[:3])) + '.')
    else:
        pts.append('Uses the context of the problem (the variables, groups or individuals named), not just symbols.')
    return pts[:3]


def main():
    banks = lib.load()
    used = {(q['skillId'], q['prompt']) for _, q in lib.items(banks)}
    seen_rule = {}
    n_ctx = n_hint = n_self = 0
    for u, q in lib.items(banks):
        if q['level'] in ('cp2', 'cp1') and (len(q['prompt']) < 60 or BARE.match(q['prompt'])):
            for pat, fn in RULES:
                m = re.match(pat, q['prompt'])
                if m:
                    i = seen_rule.get((q['skillId'], pat), 0)
                    for j in range(6):
                        new = fn(m, i + j)
                        if (q['skillId'], new) not in used:
                            break
                    seen_rule[(q['skillId'], pat)] = i + j + 1
                    assert (q['skillId'], new) not in used, new
                    used.discard((q['skillId'], q['prompt']))
                    q['prompt'] = new
                    used.add((q['skillId'], new))
                    n_ctx += 1
                    break
        if q['level'] == 'cp2':
            h = hint_for(q)
            if h:
                q['hint'] = h
                n_hint += 1
            else:
                q.pop('hint', None)
    # self-check lists: decided by the practice grader (node) so they match exactly what students self-score
    import json, subprocess
    js = ('const fs=require("fs"),vm=require("vm"),c={};c.window=c;vm.createContext(c);for(const f of ["menu/mathcheck.js","practice/radical-grading.js","practice/exact-grading.js",'
          '"practice/calculus-grading.js","practice/stat-grading.js","practice/grading.js"])vm.runInContext(fs.readFileSync("worksheet-generator/"+f,"utf8"),c);'
          'const keys=JSON.parse(fs.readFileSync(0,"utf8"));console.log(JSON.stringify(keys.map(k=>c.MKPRACTICE.bankAnswer(k)===null)))')
    sa = [q for _, q in lib.items(banks) if q['format'] == 'short-answer']
    flags = json.loads(subprocess.run(['node', '-e', js], cwd=lib.ROOT, input=json.dumps([str(q['answer']) if not isinstance(q['answer'], list) else '; '.join(q['answer']) for q in sa]),
                                      capture_output=True, text=True, check=True).stdout)
    for q, is_self in zip(sa, flags):
        if is_self:
            q['selfCheck'] = self_check(q)
            n_self += 1
        else:
            q.pop('selfCheck', None)
    lib.save(banks)
    print(f'contexts {n_ctx}; CP2 hints {n_hint}; self-check lists {n_self}')


if __name__ == '__main__':
    main()
