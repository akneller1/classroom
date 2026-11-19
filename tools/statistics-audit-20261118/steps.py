"""Statistics audit #1 (2026-11-18): no computational item keeps a one-line solution.
Each one-step solution of an item with a numeric answer becomes: the rule or formula (chosen from what the item asks),
the existing work, finished with "= <answer>" when it stopped short, and for interpretations of a result the
answer stated in a sentence. Idempotent: an item that already has two or more steps is left alone."""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import lib

# (pattern on prompt, pattern on step or None, rule) – first match wins
RULES = [
 # Rules marked 'T' are matched on the whole prompt in the first pass (the context decides the method); the others are
 # matched first on what the item asks (questions and Find/Predict/... sentences), then on the whole prompt.
 (r'E\(\d+X ?[+−-] ?\d*Y\)', None, 'Means of combinations: E(aX + bY) = a·E(X) + b·E(Y).'),
 (r'(SD|Var)\(X ?[+−-] ?Y\)|(mean and (SD|standard deviation)|SD|Var|mean) of X ?[+−-] ?Y|E\(X ?[+−-] ?Y\)|mean of (their|the) (sum|difference|total)', None, 'For independent random variables, μ_(X ± Y) = μ_X ± μ_Y and Var(X ± Y) = Var(X) + Var(Y).'),
 (r'(?i)(standard error|SE) of x̄(?![₁₂])', None, 'Standard error of x̄: SE = s/√n.'),
 (r'(?i)(CI|interval) (for|of) p₁ − p₂', None, 'Two-proportion z interval: (p̂₁ − p̂₂) ± z*·√(p̂₁(1 − p̂₁)/n₁ + p̂₂(1 − p̂₂)/n₂).'),
 (r'(?i)two-sample t\b', r'/', 'Two-sample t statistic: t = (x̄₁ − x̄₂) ÷ √(s₁²/n₁ + s₂²/n₂).'),
 (r'(?i)(interval|CI) for the slope|confidence interval for β|slope CI', r'±|t\*', 'Confidence interval for the slope: b ± t*·SE_b, with df = n − 2.'),
 (r'(?i)labels? (are )?chosen|label chosen|what rolls result', None, 'Read the digits in groups the size of a label; skip numbers that are not labels, and skip repeats when sampling without replacement.'),
 (r'(?i)typical predictions|how far off', None, 's, the SD of the residuals, is the typical size of a prediction error.'),
 (r'(?i)proportion of heads will', None, 'Law of large numbers: with many trials, the relative frequency gets close to the true probability.'),
 (r'(?i)sample size were \d+ instead|without recalculating', None, 'Standard deviations of sampling distributions shrink like 1/√n: multiplying n by 4 halves the SD (and the margin of error).'),
 (r'(?i)\d+ different random samples', None, 'In repeated sampling, about C% of C% confidence intervals capture the true parameter.'),
 (r'(?i)minimum (sample size|n)', None, 'Solve the margin-of-error formula for n: n = (z*/ME)²·p*(1 − p*) for a proportion, or (z*σ/ME)² for a mean; then round up.'),
 (r'(?i)margin of error', r'\)/2|÷ 2|[Hh]alf', 'Margin of error = half the width of the interval.'),
 (r'(?i)fail to reject \| H₀', None, 'P(fail to reject H₀ | H₀ false) = P(Type II error) = 1 − power.'),
 (r'Find P\(B\)\.', r'\+', 'Total probability: P(B) = P(A)·P(B | A) + P(not A)·P(B | not A).'),
 (r'(?i)equally likely to be', None, 'With equally likely values, probability = (number of values in the event) ÷ (number of values).', 'T'),
 (r'X = 1 if', None, 'P(X = 1) = P(the event) = (favorable outcomes) ÷ (total outcomes).', 'T'),
 (r'Relative frequencies:.* \?', r'1 −', 'Relative frequencies of all the categories add to 1.', 'T'),
 (r'(?i)binomial', r'√', 'Binomial: μ = np and σ = √(np(1 − p)).', 'T'),
 (r'n = \d+ and p = [\d.]+\. Find P\(X', None, 'Binomial: P(X = k) = C(n, k)·pᵏ·(1 − p)ⁿ⁻ᵏ; add the terms for each k in the event.', 'T'),
 (r'(?i)\bCoef\b|SE Coef', None, 'In regression output, the slope b is the coefficient in the x row, and SE_b is the standard error in the same row.', 'T'),
 (r'(?i)cumulative relative frequency', None, 'Cumulative relative frequency at a value is the proportion of values at or below it; subtract two of them for an interval.', 'T'),
 (r'(?i)\(cumulative\)|best estimate of the probability', None, 'Law of large numbers: the relative frequency from the most trials is the best estimate.', 'T'),
 (r'68–95–99\.7', None, 'Empirical rule: about 68%, 95% and 99.7% of values lie within 1, 2 and 3 SDs of the mean.', 'T'),
 (r'(?i)stemplot|\(key \d+ \|', None, 'Read each leaf with its stem, as the key shows (for example, 3 | 1 means 31).', 'T'),
 (r'(?i)mutually exclusive|disjoint', None, 'For disjoint events, P(A or B) = P(A) + P(B) and P(A and B) = 0.', 'T'),
 (r'[Uu]niform (from|on|between)', None, 'For a continuous uniform distribution, probability = (length of the interval) ÷ (total length), and any single value has probability 0.', 'T'),
 (r'[Gg]eometric', None, 'Geometric: P(first success on trial k) = (1 − p)^(k−1)·p, and P(more than k trials) = (1 − p)ᵏ.', 'T'),
 (r'P\(X ≤ \d+\) = [\d.]+,? (and )?P\(X ≤', r'−', 'P(X = k) = P(X ≤ k) − P(X ≤ k − 1).', 'T'),
 (r'P\(B \| A\) = [\d.]+ and P\(A\) = |P\(A\) = [\d.]+ and P\(B \| A\) = ', None, 'General multiplication rule: P(A and B) = P(A)·P(B | A).', 'T'),
 (r'[Bb]onus|°F|\b[YTB] = (\d+(\.\d+)? ?[+−-] ?)?\d*(\.\d+)?X\b|\by = −?\d*x|\by = \d+ − \d*x|[Ee]very value|to every|new SD|new mean|new values|SD of y\b|SD\(−?\d*X ?[+−] ?\d|Var\(\d+X|E\(\d+ ?[−+] ?\d*X|E\(Y\)', None, 'Linear transformation Y = a + bX: μ_Y = a + bμ_X and σ_Y = |b|σ_X (adding a constant does not change the SD).', 'T'),
 (r'(?i)new r\b|What is r\?|converted .* (What is|what is) r|correlation .* converted', None, 'Correlation r has no units and does not change when either variable is rescaled.', 'T'),
 (r'(?i)residual (is|was|of) −?[\d.]+', None, 'Residual = observed y − predicted ŷ, so ŷ = y − residual.', 'T'),
 (r'r² = [\d.]+.*Find r\b', None, 'r = ±√r², with the same sign as the slope.', 'T'),
 (r'(?i)half-width|(margin of error|ME) (is|of|=) [\d.]+.*Find the SE', r'/', 'SE = (margin of error) ÷ (critical value).', 'T'),
 (r'Normal approximation', None, 'Large Counts: np ≥ 10 and n(1 − p) ≥ 10.', 'T'),
 (r'(?i)top \d+%|bottom \d+%|\d+(th|st|nd|rd) percentile', r'z|\d\.\d{3,}\(', 'Find z with the given area to the left (Table A or invNorm), then value = mean + z·SD.'),
 (r'(?i)N\(\d|Normal', r'The value has [\d.]+% of the d|z = −?[\d.]+ →|invNorm|\+ [\d.]{4,}\(', 'Find z with the given area to the left (Table A or invNorm), then value = mean + z·SD.', 'T'),
 (r'(?i)N\(\d|approximately Normal|is Normal with', r'z', 'Standardize with z = (x − μ) ÷ σ, then find the area under the standard Normal curve (Table A or normalcdf).', 'T'),
 (r'(?i)slope of the (LSRL|least-squares)|LSRL slope', None, 'Slope of the least-squares line: b = r·s_y ÷ sₓ.'),
 (r'(?i)predicted z|z_y\?|How many standard deviations (above|below)', None, 'In standard units the least-squares line is ẑ_y = r·zₓ.'),
 (r'(?i)What is the standard deviation\?', r'√', 'SD = √variance.'),
 (r'(?i)What is the variance\?', None, 'Variance = SD².'),
 (r'(?i)which score has z|value .* z-score of|has a z-score of', None, 'value = mean + z·SD.'),
 (r'(?i)symmetric', r'(?i)binomial', 'A binomial distribution is symmetric when p = 0.5 and skewed when p is near 0 or 1.'),
 (r'(mean and (SD|standard deviation)|SD|Var)\(?( of)? X ?[+−-] ?Y|mean of X ?[+−-] ?Y|E\(X ?[+−-] ?Y\)', None, 'For independent random variables, μ_(X ± Y) = μ_X ± μ_Y and Var(X ± Y) = Var(X) + Var(Y).'),
 (r'(?i)binomial (SD|standard deviation|mean)|expected number of heads', None, 'Binomial: μ = np and σ = √(np(1 − p)).'),
 (r'(?i)mean and (SD|standard deviation)|mean number', r'np', 'Binomial: μ = np and σ = √(np(1 − p)).'),
 (r'SD\(X\)\.|Find SD\(X\)', None, 'SD of a random variable: σ_X = √(Σ (x − μ)²·P(x)).'),
 (r'(?i)expected (number|count)|how many times will', r'×', 'Expected count = (number of trials) × (probability).'),
 (r'(?i)expected net', None, 'Expected net gain = (expected prize) − (cost).'),
 (r'(?i)How many times did it occur', None, 'Count = (relative frequency) × (number of trials).'),
 (r'(?i)about how many .* below', None, 'Count below = (percentile as a decimal) × (number of values).'),
 (r'(?i)SD for n = \d+|its SD for n', None, 'The SD of a sampling distribution is proportional to 1/√n.'),
 (r'(?i)probability that (more|less|fewer) than [\d.]+%', None, 'Standardize with the sampling distribution: z = (p̂ − p) ÷ √(p(1 − p)/n), then use the Normal curve.'),
 (r'(?i)(skewed|right-skewed|left-skewed) population', None, 'Central Limit Theorem: the more skewed the population, the larger n must be for x̄ to be approximately Normal (n ≥ 30 is a common guide).'),
 (r'(?i)P\(Type II|Type II error', None, 'P(Type II error) = 1 − power.'),
 (r'(?i)How many differences', None, 'Paired data give one difference per pair (or per person).'),
 (r'(?i)strongest evidence', None, 'The smaller the p-value, the stronger the evidence against H₀.'),
 (r'(?i)outlier|fence', r'(?i)fence|Q1|IQR|1\.5|far from', 'Outlier fences: Q1 − 1.5·IQR and Q3 + 1.5·IQR.'),
 (r'(?i)\bIQR\b|interquartile', None, 'IQR = Q3 − Q1, with Q1 and Q3 the medians of the lower and upper halves.'),
 (r'(?i)Find Q[13]\b', None, 'Q1 and Q3 are the medians of the lower and upper halves of the ordered data.'),
 (r'(?i)pooled proportion', None, 'Pooled proportion: p̂_C = (total successes) ÷ (total sample size).'),
 (r'SE of p̂₁ − p̂₂', None, 'SE of p̂₁ − p̂₂ = √(p̂₁(1 − p̂₁)/n₁ + p̂₂(1 − p̂₂)/n₂).'),
 (r'point estimate of μ₁ − μ₂', None, 'Point estimate of μ₁ − μ₂: x̄₁ − x̄₂.'),
 (r'P\(A and B\)', r'−', 'Addition rule rearranged: P(A and B) = P(A) + P(B) − P(A or B).'),
 (r'(?i)p-value|P-value', r't|z|χ', 'p-value = the probability, if H₀ is true, of a result at least as extreme as the one observed, in the direction of Hₐ (both tails for ≠).'),
 (r'(?i)LinReg|equation of the least-squares|least-squares (regression )?line', r'LinReg', 'Use technology (LinReg a + bx) to find the least-squares line ŷ = a + bx.'),
 (r'(?i)what (percent|proportion|fraction)\b', r'/', 'Proportion = (count in the category) ÷ (total).'),
 (r'(?i)percentile', None, 'A percentile is the percent of values below a given value.'),
 (r'weakest|strongest', None, 'Strength of a linear association depends on |r|: values near ±1 are strong, values near 0 are weak.'),
 (r'box plot', r'%|percent', 'Each of the four parts of a box plot (whisker, box half, box half, whisker) holds about 25% of the values.'),
 (r'CI .*Find (p̂|x̄)|interval .*Find (p̂|x̄)|is \(.*\)\. Find (p̂|x̄)', None, 'The point estimate is the midpoint of the interval: (lower + upper) ÷ 2.'),
 (r'What was p̂', None, 'Solve z = (p̂ − p₀) ÷ √(p₀(1 − p₀)/n) for p̂: p̂ = p₀ + z·√(p₀(1 − p₀)/n).'),
 (r'P\(p̂ [<>]|P\(x̄ [<>]', None, 'Standardize with the sampling distribution: z = (statistic − mean) ÷ (its SD), then use the Normal curve.'),
 (r'tests? positive', None, 'Total probability: P(+) = P(D)·P(+ | D) + P(not D)·P(+ | not D); Bayes: P(D | +) = P(D and +) ÷ P(+).'),
 (r'(?i)\bboth\b', r'P\(A or B\)|\+ .* −', 'Addition rule: P(A or B) = P(A) + P(B) − P(A and B).'),
 (r'(?i)none of them|at least once|at least one', None, 'P(at least one) = 1 − P(none), and for independent trials P(none) is the product of the "no" probabilities.'),
 (r'.', r'binomcdf|binompdf', 'Binomial: P(X = k) = C(n, k)·pᵏ·(1 − p)ⁿ⁻ᵏ; use binomcdf for "at most" and 1 − binomcdf for "at least".'),
 (r'first (prize|expert|\w+)', None, 'Geometric: P(first success on trial k) = (1 − p)^(k−1)·p, and P(more than k trials) = (1 − p)ᵏ.'),
 (r'(?i)does not|not walk', None, 'Complement rule: P(not A) = 1 − P(A).'),
 (r'(?i)digits|pairs \d', None, 'Use equally likely outcomes, and give "success" the fraction of them that matches the probability.'),
 (r'(?i)simulat.*success|simulated trials', None, 'Estimate the probability by the relative frequency: (number of successes) ÷ (number of trials).'),
 (r'rolls of a fair die|in a row', None, 'For independent trials, multiply the probabilities.'),
 (r'P\(x\):|P\(\d+ ≤ X|P\(\d+ < X', r'\+',  'Add the probabilities of the values of X that satisfy the condition.'),
 (r'Type I', None, 'P(Type I error) = α, the significance level.'),
 (r'What is H₀|H₀\?|Which is .*H|Hₐ\?|correct alternative', None, 'Hypotheses are about a parameter: H₀ says "no difference" (=), and Hₐ uses <, > or ≠ to match the question.'),
 (r'wider|narrower', None, 'Higher confidence needs a larger critical value, which makes the interval wider.'),
 (r'p₁ − p₂', None, 'Point estimate of p₁ − p₂: p̂₁ − p̂₂.'),
 (r'±', None, 'An interval is estimate ± margin of error.'),
 (r'SE of x̄₁ − x̄₂|s₁ = .*s₂ = ', None, 'Standard error of x̄₁ − x̄₂: SE = √(s₁²/n₁ + s₂²/n₂).'),
 (r'(?i)standard error|\bSE\b', r'p̂|0\.\d+/|\(0\.', 'Standard error of p̂: SE = √(p̂(1 − p̂)/n).'),
 (r'[Uu]niform', None, 'For a uniform distribution, probability = (length of the interval) ÷ (total length).'),
 (r'could (NOT )?be a probability', None, 'A probability must be between 0 and 1, inclusive.'),
 (r'[Tt]wo fair dice|two dice', None, 'Count equally likely outcomes: two dice have 6 × 6 = 36.'),
 (r'[Hh]ypothes|What is Hₐ|alternative hypothesis', None, 'Hypotheses are about a parameter: H₀ says "no difference" (=), and Hₐ uses <, > or ≠ to match the question.'),
 (r'[dD]̄ = |paired t|Paired t', r'/', 'Paired t statistic: t = (x̄_d − 0) ÷ (s_d/√n), on the differences.'),
 (r'(?i)difference of means|mean difference|pass-rate difference|difference [A-Z] − [A-Z]|rate difference', None, 'Compare the two groups by subtracting in the order asked: (group 1) − (group 2).'),
 (r'SSE', None, 'Standard deviation of the residuals: s = √(SSE ÷ (n − 2)), the typical prediction error.'),
 (r'[Cc]ritical p̂', None, 'Critical value for p̂: p₀ + z*·√(p₀(1 − p₀)/n) (upper-tailed test).'),
 (r'z-value has|[ZzTt]\* ', None, 'The critical value cuts off the middle C% of the standard Normal (z*) or of t with df = n − 1 (t*).'),
 (r'(?i)\bstrata\b|proportional', None, 'Proportional allocation: (total sample size) × (stratum share of the population).'),
 (r'(?i)needed\?|per group|volunteers needed', None, 'Subjects needed = (number of treatments) × (subjects per treatment).'),
 (r'(?i)\bwidth\b', None, 'Width = upper endpoint − lower endpoint = 2 × margin of error.'),
 (r'most likely', None, 'The most likely value is the one with the largest probability.'),
 (r'most reliable', None, 'Law of large numbers: more trials give a more reliable relative frequency.'),
 (r'Normal approximation', None, 'Large Counts: np ≥ 10 and n(1 − p) ≥ 10.'),
 (r'sample mean\?|which value is the sample mean', None, 'The point estimate is the midpoint of the interval: (lower + upper) ÷ 2.'),
 (r'skewed population|strongly (right-|left-)?skewed population', None, 'Central Limit Theorem: the more skewed the population, the larger n must be for x̄ to be approximately Normal (n ≥ 30 is a common guide).'),
 (r'\bAND\b', r'/', 'P(A and B) = (count in both) ÷ (total).'),
 (r'(?i)two-way table|of the \d+ students|students by grade', None, 'Use the counts in the table: probability = (count in the event) ÷ (count in the group considered).'),
  (r'N\(|[Nn]ormal', r'z|Z', 'Standardize with z = (x − μ) ÷ σ, then find the area under the standard Normal curve (Table A or normalcdf).'),
 (r'[Ww]hich value has (a )?z|value .* z-score of|has a z-score of|What \w+ has a z-score of', None, 'value = mean + z·SD.'),
 (r'E\(\d*X ?[+−-] ?\d*Y\)|E\(\d+X', None, 'Means of combinations: E(aX + bY) = a·E(X) + b·E(Y).'),
 (r'(SD|mean and SD|variance) of [XY] ?[+−-] ?[XY]|X ?[+−-] ?Y\b.*(SD|σ|standard)|SDs? .* (sum|total|difference)', None, 'For independent random variables, variances add: Var(X ± Y) = Var(X) + Var(Y), and μ_(X ± Y) = μ_X ± μ_Y.'),
 (r'SE of x̄|standard error of x̄|S = [\d.]+ and n', None, 'Standard error of x̄: SE = s/√n.'),
 (r'intercept', None, 'The least-squares line passes through (x̄, ȳ), so a = ȳ − b·x̄.'),
 (r'[Ee]stimate P\(|times in \d+ (tosses|spins|rolls|trials)', None, 'Estimate the probability by the relative frequency: (number of times) ÷ (number of trials).'),
 (r'block of \d+|units per treatment|per treatment', None, 'Divide the units equally: (units in the block) ÷ (number of treatments).'),
 (r'(?i)(halve|cut .* in half|quadrupl|multiplied to).*(SD|standard deviation|margin|error)|(SD|standard deviation|margin).*(halve|half|quadrupl)', None, 'Standard deviations of sampling distributions shrink like 1/√n: to divide the SD by k, multiply n by k².'),
 (r'P\(D \| \+\)|P\(disease \| positive|given (that )?(a person )?tests? positive', None, 'Bayes: P(D | +) = P(D and +) ÷ P(+), where P(+) = P(D)·P(+ | D) + P(not D)·P(+ | not D).'),
 (r'P\(\+\)', None, 'Total probability: P(+) = P(D)·P(+ | D) + P(not D)·P(+ | not D).'),
 (r'P\(not |not [A-Z]\)|complement', None, 'Complement rule: P(not A) = 1 − P(A).'),
 (r'P\(X > \d+\)|P\(X ≥ \d+\)', r'(?i)^1 −|complement', 'Complement rule: P(X > k) = 1 − P(X ≤ k).'),
 (r'disjoint|mutually exclusive', None, 'For disjoint events, P(A or B) = P(A) + P(B) and P(A and B) = 0.'),
 (r'P\([A-Z] or [A-Z]\)|\bor\b.*P\(|P\(.* or ', None, 'Addition rule: P(A or B) = P(A) + P(B) − P(A and B).'),
 (r'P\([^)]*\|', None, 'Conditional probability: P(A | B) = P(A and B) ÷ P(B), or (count in both) ÷ (count in the condition).'),
 (r'independent.*(both|and)|P\([A-Z] and [A-Z]\)|in a row|all \d|each of', None, 'For independent events, P(A and B) = P(A)·P(B).'),
 (r'at least one', None, 'P(at least one) = 1 − P(none).'),
 (r'missing probability|Find k\b|, k\.|probabilities .* k', None, 'The probabilities in a probability distribution add to 1.'),
 (r'[Rr]elative frequency|long-run|proportion of (heads|tosses|spins)', None, 'Relative frequency = (number of times the outcome occurs) ÷ (number of trials).'),
 (r'digits|random digit|die to model|with a die', None, 'Use equally likely outcomes, and give "success" the fraction of them that matches the probability.'),
 (r'Var\(X [+−-] Y\)|SD of (the )?(sum|difference|total)|SDs? \d.* (sum|total|difference)|σ_\(X ?[+−-] ?Y\)|σ_[TD]\b|Independent X and Y have SDs', None, 'For independent random variables, variances add: Var(X ± Y) = Var(X) + Var(Y).'),
 (r'E\(X [+−-] Y\)|mean of (their|the) (sum|difference|total)|μ_\(X', None, 'Means add or subtract: μ_(X ± Y) = μ_X ± μ_Y.'),
 (r'SD\(X ?[+−-] ?\d|SD\(\d|[YT] = \d+ ?[+−-]|= \d*X\b|bonus|per car|converted|°F|\d+X\b', None, 'Linear transformation Y = a + bX: μ_Y = a + bμ_X and σ_Y = |b|σ_X (adding a constant does not change the SD).'),
 (r'[Gg]eometric|first success|1/p|until|average number of (trials|boxes|tries)', None, 'Geometric: P(first success on trial k) = (1 − p)^(k−1)·p, and the mean number of trials is 1/p.'),
 (r'[Bb]inomial (mean|SD|standard)|binomial mean|np\b|mean of X\b.*n = |n = \d+ and p = |n = \d+, p = ', r'np|√\(np', 'Binomial: μ = np and σ = √(np(1 − p)).'),
 (r'C\(\d|exactly \d|binom|P\(X = \d+\)', None, 'Binomial: P(X = k) = C(n, k)·pᵏ·(1 − p)ⁿ⁻ᵏ.'),
 (r'E\(X\)|[Ee]xpected (payout|value|net|profit|winnings|number)|mean of X|mean \(expected', None, 'Expected value: E(X) = Σ x·P(x).'),
 (r'P\(X [<≤≥>=] \d', r'\+', 'Add the probabilities of the values of X that satisfy the condition.'),
 (r'SD of x̄|σ_x̄|standard deviation of x̄|SD of the sample mean', None, 'σ_x̄ = σ/√n.'),
 (r'[Ss]mallest n|how large (a )?(sample|n)|sample size .* at most|sample size needed', None, 'Solve the inequality for n and round up to the next whole number.'),
 (r'SD of p̂|σ_p̂|standard deviation of p̂', None, 'σ_p̂ = √(p(1 − p)/n).'),
 (r'mean of the sampling distribution|center of the sampling|μ_x̄|μ_p̂', None, 'A sampling distribution of x̄ (or p̂) is centered at the population mean μ (or proportion p).'),
 (r'np ≥ 10|Large Counts|n\(1 − p\)', None, 'Large Counts: np ≥ 10 and n(1 − p) ≥ 10.'),
 (r'df\b|degrees of freedom', None, 'Degrees of freedom: n − 1 for one-sample or paired t; (smaller n) − 1 for the conservative two-sample t; n − 2 for a regression slope; (categories − 1) or (rows − 1)(columns − 1) for chi-square.'),
 (r'[zt]\* ', None, 'The critical value cuts off the middle C% of the standard Normal (z*) or of t with the given df (t*).'),
 (r'[Mm]argin of error|\bME\b', r'[Hh]alf', 'Margin of error = half the width of the interval.'),
 (r'[Mm]argin of error|\bME\b', None, 'Margin of error = (critical value) × (standard error).'),
 (r'point estimate|midpoint', None, 'The point estimate is the midpoint of the interval: (lower + upper) ÷ 2.'),
 (r'CI for p|interval for p\b|confidence interval for the (population )?proportion', None, 'One-proportion z interval: p̂ ± z*·√(p̂(1 − p̂)/n).'),
 (r'CI for μ|interval for μ|interval for the (population )?mean', None, 'One-sample t interval: x̄ ± t*·s/√n.'),
 (r'p̂₁ − p̂₂|p̂_A − p̂_B|difference in (sample )?proportions', None, 'Point estimate of p₁ − p₂: p̂₁ − p̂₂, with each p̂ = successes ÷ n.'),
 (r'x̄₁ − x̄₂|μ₁ − μ₂', None, 'Point estimate of μ₁ − μ₂: x̄₁ − x̄₂.'),
 (r'SE_b|slope b = |b = [\d.]+ and SE', None, 'Test statistic for a slope: t = (b − 0) ÷ SE_b.'),
 (r'p₀|H₀: p =', r'√', 'One-proportion z statistic: z = (p̂ − p₀) ÷ √(p₀(1 − p₀)/n).'),
 (r'μ₀|H₀: μ =', None, 'One-sample t statistic: t = (x̄ − μ₀) ÷ (s/√n).'),
 (r'p-value|P-value', None, 'p-value = the probability, if H₀ is true, of a result at least as extreme as the one observed, in the direction of Hₐ (both tails for ≠).'),
 (r'Type II|power', None, 'Power = 1 − P(Type II error); P(Type I error) = α.'),
 (r'\(O − E\)|expected count|chi-square|χ²', None, 'Chi-square: expected count = (row total)(column total) ÷ (grand total) or n·p, and each cell contributes (O − E)² ÷ E.'),
 (r'z-?score|Find z\b|What is z', None, 'z = (value − mean) ÷ SD.'),
 (r'[Ww]hich value has a z-score|value .* z-score of|z-score of −?[\d.]+\?', None, 'value = mean + z·SD.'),
 (r'percentile', None, 'A percentile is the percent of values below a given value.'),
 (r'IQR|interquartile', None, 'IQR = Q3 − Q1, with Q1 and Q3 the medians of the lower and upper halves.'),
 (r'\bQ1\b|\bQ3\b|quartile', None, 'Q1 and Q3 are the medians of the lower and upper halves of the ordered data.'),
 (r'fence|outlier', None, 'Outlier fences: Q1 − 1.5·IQR and Q3 + 1.5·IQR.'),
 (r'[Mm]edian', None, 'Order the data; the median is the middle value (the mean of the two middle values when n is even).'),
 (r'\b[Rr]ange\b', None, 'Range = maximum − minimum.'),
 (r'(?i)sample (SD|standard deviation)|standard deviation of (the|these) (data|values)', None, 'Sample SD: s = √(Σ(x − x̄)² ÷ (n − 1)).'),
 (r'[Mm]ean of|[Ff]ind the mean|new mean|average', None, 'Mean = (sum of the values) ÷ (number of values).'),
 (r'[Rr]esidual', None, 'Residual = observed y − predicted ŷ.'),
 (r'ŷ|[Pp]redict', None, 'Substitute x into the regression line ŷ = a + bx.'),
 (r'r²|coefficient of determination', None, 'r² = (correlation)²: the fraction of the variation in y accounted for by the linear model.'),
 (r'\br\b|correlation', None, 'Correlation r has no units and does not change when either variable is rescaled.'),
 (r'treatments', None, 'Number of treatments = product of the numbers of levels of the factors.'),
 (r'proportional|strat', None, 'Proportional allocation: (total sample size) × (stratum share of the population).'),
 (r'(?i)how many (students|values|observations|dots)|represented in all', None, 'Add the counts in the categories asked for.'),
 (r'proportion|percent|fraction', None, 'Proportion = (count in the category) ÷ (total).'),
]

# Checked only when no rule above matches the question or the prompt.
FALLBACK = [
 (r'Find P\(|probability', r'/\d|\d/', 'Probability = (count in the event) ÷ (total).'),
 (r'(?i)test statistic', r'/', 'Test statistic = (statistic − value in H₀) ÷ (standard deviation of the statistic).'),
 (r'(?i)before and after|before/after', None, 'Paired data: work with the difference (after − before) for each subject.'),
]


def num_in(s):
    return [x.rstrip('.') for x in re.findall(r'[−-]?\d[\d,]*\.?\d*', s)]


def numeric(ans):
    a = ans.strip()
    return bool(re.search(r'\d', a)) and len(re.findall(r'[A-Za-z]{3,}', a)) <= 2 and len(a) <= 40


def finish(step, ans):
    """Append the answer to a step that stops at the setup."""
    a = ans.strip().rstrip('.')
    lead = num_in(a)
    if not lead or lead[0] in num_in(step.split('=')[-1] if '=' in step else step[-30:]):
        return step
    s = step.rstrip().rstrip('.')
    if re.search(r'[\d)]$', s) and re.search(r'[+−\-×·÷/*√()]', s):
        return f'{s} = {a}.'
    return step


def expand(q):
    if len(q['solutionSteps']) != 1 or q['format'] not in ('short-answer', 'multiple-choice'):
        return False
    ans = lib.key_text(q)
    if not numeric(ans) or q['prompt'].startswith('Error analysis'):
        return False
    step = q['solutionSteps'][0]
    text = q['prompt']
    rule = None
    ask = ' '.join(x for x in re.split(r'(?<=[.?])\s+', text) if x.endswith('?') or re.match(r'(Find|Predict|Compute|Calculate|Estimate|Give|Determine|Use the)', x)) or text
    for first in (True, False):
        for pp, sp, r, *flag in RULES:
            scope = ask if first and not flag else text
            if re.search(pp, scope) and (sp is None or re.search(sp, step)):
                rule = r
                break
        if rule:
            break
    for pp, sp, r in ([] if rule else FALLBACK):
        if re.search(pp, text) and (sp is None or re.search(sp, step)):
            rule = r
            break
    work = finish(step, ans)
    if rule is None:
        parts = [p.strip() for p in re.split(r'(?<=[.;])\s+(?=[A-Zp(])', work) if p.strip()]
        if len(parts) >= 2:
            q['solutionSteps'] = [p if p.endswith(('.', ';')) else p + '.' for p in parts]
            q['solutionSteps'] = [p[:-1] + '.' if p.endswith(';') else p for p in q['solutionSteps']]
            return True
        rule = 'Identify what is asked, then use the values given.'
    out = [rule, work]
    if num_in(ans)[0] not in num_in(work):
        out.append(f'Answer: {ans}' + ('' if ans.endswith('.') else '.'))
    q['solutionSteps'] = out
    return True


def tidy(q):
    """Typeset negative numbers in worked steps: 'a + (-b)(x)' becomes 'a − b(x)', and '(-b' becomes '(−b'."""
    st = q.get('solutionSteps') or []
    new = [re.sub(r'\(-(?=\d)', '(−', re.sub(r'\+ \(-(\d[\d.]*)\)', r'− \1', x)) if isinstance(x, str) else x for x in st]
    if new != st:
        q['solutionSteps'] = new
        return True
    return False


def main():
    banks = lib.load()
    n = sum(expand(q) for u, q in lib.items(banks))
    print('negative signs typeset', sum(tidy(q) for u, q in lib.items(banks)))
    lib.save(banks)
    print('expanded', n)


if __name__ == '__main__':
    main()
