# Teaching notes, Statistics units 3–4 (Anticipating Patterns; Statistical Inference).
# Each record: obj, idea, voc [[word, meaning]…], watch, cards [{h, big, steps}]. Math in ⟨TeX⟩; {{…}} = blank on guided notes.
AP = 'anticipating-patterns'
SI = 'statistical-inference'
R = {}

R[AP, 1] = dict(obj='interpret probability as a long-run relative frequency and apply the law of large numbers',
  idea='A probability describes what happens in the long run. Short runs vary a lot; the relative frequency settles near the probability as trials pile up.',
  voc=[['probability', 'The long-run relative frequency of an outcome.'], ['law of large numbers', 'As trials increase, the relative frequency approaches the probability.'], ['relative frequency', 'Count of an outcome ÷ number of trials.']],
  watch='The gambler’s fallacy: believing a success is “due” after a run of failures.',
  cards=[dict(h='Long run, not short run', big='Relative frequency = {{count ÷ trials}}; it gets close to the probability only over many trials.',
    steps=['12 makes in 20 free throws: relative frequency {{0.6}}.', 'A 75% shooter in 200 shots: expect about {{150}} makes.'])])

R[AP, 2] = dict(obj='use the addition, complement and multiplication rules',
  idea='“Or” adds and subtracts the overlap; “and” multiplies when events are independent; “not” uses 1 minus.',
  voc=[['complement', 'All outcomes not in A; P(not A) = 1 − P(A).'], ['mutually exclusive', 'Events that cannot happen together: P(A and B) = 0.'], ['independent', 'Knowing one event happened does not change the other’s probability.']],
  watch='Adding probabilities of overlapping events without subtracting P(A and B).',
  cards=[dict(h='Or, and, not', big='⟨P(A \\cup B) = P(A) + P(B) - P(A \\cap B)⟩.',
    steps=['0.5 + 0.4 − 0.1 = {{0.8}}.', 'Independent: P(A and B) = 0.8 × 0.8 = {{0.64}}.', 'At least one failure in 3 tries: 1 − 0.8³ = {{0.488}}.'])])

R[AP, 3] = dict(obj='find conditional probabilities from tables and formulas and test events for independence',
  idea='Conditioning shrinks the sample space to the given group. Events are independent when P(A | B) = P(A).',
  voc=[['conditional probability', 'P(A | B), the probability of A given that B happened.'], ['two-way table', 'Counts for two categorical variables.'], ['tree diagram', 'Branches showing probabilities in stages.']],
  watch='Using the grand total instead of the total of the given group.',
  cards=[dict(h='Given means “divide by the given”', big='⟨P(A \\mid B) = \\dfrac{P(A \\cap B)}{P(B)}⟩.',
    steps=['P(A and B) = 0.12 and P(B) = 0.4: P(A | B) = {{0.3}}.', 'If P(A) = 0.3 as well, A and B are {{independent}}.'])])

R[AP, 4] = dict(obj='design and carry out simulations to estimate probabilities',
  idea='A simulation imitates a chance process: assign digits to outcomes, describe one trial, repeat many times and estimate the probability from the results.',
  voc=[['simulation', 'Imitating a random process with random numbers.'], ['trial', 'One repetition of the simulated process.'], ['estimate', 'The proportion of trials in which the event happens.']],
  watch='Assigning digits that give the wrong probability (0–3 for p = 0.3 gives 0.4).',
  cards=[dict(h='Four parts', big='Assign digits → describe one trial → repeat → {{estimate}}.',
    steps=['p = 0.3: digits 0–{{2}} mean success.', '11 of 40 trials had the event: estimate {{0.275}}.', 'More trials make the estimate {{less variable}}.'])])

R[AP, 5] = dict(obj='build and use discrete probability distributions',
  idea='A probability distribution lists every value of X with its probability; the probabilities are between 0 and 1 and add to 1.',
  voc=[['random variable', 'A numerical outcome of a chance process.'], ['discrete random variable', 'One with a countable set of values.'], ['probability distribution', 'The values of X and their probabilities.']],
  watch='Mixing up “less than” and “at most”: P(X < 2) leaves out X = 2.',
  cards=[dict(h='Using a table', big='Probabilities add to {{1}}; add the probabilities of the values you need.',
    steps=['P(0) = 0.2, P(1) = 0.4, P(2) = 0.3, P(3) = k: k = {{0.1}}.', 'P(X ≥ 2) = 0.3 + 0.1 = {{0.4}}.'])])

R[AP, 6] = dict(obj='calculate and interpret the mean and standard deviation of a discrete random variable, including linear transformations',
  idea='E(X) is the long-run average outcome. Adding a constant shifts the mean only; multiplying by b multiplies the mean and the SD by |b|.',
  voc=[['expected value E(X)', 'Σ x·P(x), the long-run average of X.'], ['standard deviation of X', 'The typical distance of X from its mean.'], ['linear transformation', 'Y = a + bX.']],
  watch='Adding the constant to the standard deviation, or forgetting the absolute value of b.',
  cards=[dict(h='Mean and SD', big='⟨E(X) = \\sum x\\,P(x)⟩; ⟨\\sigma_X = \\sqrt{\\sum (x - \\mu)^2 P(x)}⟩.',
    steps=['X = 0, 1, 2 with 0.3, 0.4, 0.3: E(X) = {{1}}.', 'SD(3X − 7) = 3 × SD(X); if SD(X) = 4, it is {{12}}.'])])

R[AP, 7] = dict(obj='recognize binomial (and geometric) settings and compute probabilities, means and standard deviations',
  idea='Binomial: a fixed number n of independent trials, two outcomes, the same p — X counts successes. μ = np and σ = √(np(1 − p)).',
  voc=[['binomial setting', 'Binary outcomes, Independent trials, fixed Number of trials, Same p (BINS).'], ['binomcdf', 'P(X ≤ k) for a binomial X.'], ['geometric setting (beyond AP)', 'Count trials until the first success.']],
  watch='Using binompdf for “at least” questions; at least k is 1 − P(X ≤ k − 1).',
  cards=[dict(h='Binomial probabilities', big='⟨P(X = k) = \\binom{n}{k}p^k(1 - p)^{n - k}⟩.',
    steps=['n = 10, p = 0.2: μ = {{2}}.', 'σ = √(10 × 0.2 × 0.8) ≈ {{1.265}}.', 'P(X ≥ 3) = 1 − P(X ≤ {{2}}).'])])

R[AP, 8] = dict(obj='combine independent random variables (beyond the 2026 AP course)',
  idea='Means add or subtract as the variables do; for independent variables the variances always add, even for a difference.',
  voc=[['independent random variables', 'Knowing one value tells nothing about the other.'], ['variance', 'The square of the standard deviation.'], ['sum of Normals', 'A sum or difference of independent Normal variables is Normal.']],
  watch='Adding standard deviations instead of variances, or subtracting variances for X − Y.',
  cards=[dict(h='Variances add', big='⟨\\sigma_{X \\pm Y} = \\sqrt{\\sigma_X^2 + \\sigma_Y^2}⟩.',
    steps=['SDs 3 and 4: SD(X + Y) = {{5}}.', 'SD(X − Y) = {{5}} as well.'])])

R[AP, 9] = dict(obj='describe the sampling distributions of p̂ and x̄ (and of differences) and use them to find probabilities',
  idea='A statistic varies from sample to sample. Its sampling distribution is centered at the parameter, with spread that shrinks as n grows, and is approximately Normal when the conditions hold.',
  voc=[['sampling distribution', 'The distribution of a statistic over all possible samples of size n.'], ['standard deviation of p̂', '√(p(1 − p)/n).'], ['Large Counts condition', 'np ≥ 10 and n(1 − p) ≥ 10.']],
  watch='Using the sample size in place of √n, or checking Large Counts with p̂ when p is known.',
  cards=[dict(h='Center, spread, shape', big='⟨\\mu_{\\hat p} = p⟩, ⟨\\sigma_{\\hat p} = \\sqrt{p(1-p)/n}⟩; Normal if Large Counts holds.',
    steps=['p = 0.5, n = 100: σ = {{0.05}}.', 'P(p̂ > 0.6): z = {{2}}, so about 0.0228.'])])

R[AP, 10] = dict(obj='explain bias and variability of estimators and apply the central limit theorem',
  idea='An unbiased estimator is centered on the parameter; larger samples reduce variability, not bias. For large n, x̄ is approximately Normal whatever the population’s shape.',
  voc=[['unbiased estimator', 'Its sampling distribution is centered at the parameter.'], ['central limit theorem', 'For large n (about 30 or more), x̄ is approximately Normal.'], ['variability', 'How spread out the sampling distribution is.']],
  watch='Saying the CLT makes the population, or the sample, Normal — it is the sampling distribution of x̄.',
  cards=[dict(h='Effect of n', big='⟨\\sigma_{\\bar x} = \\sigma/\\sqrt{n}⟩: four times the sample size {{halves}} the spread.',
    steps=['σ = 12, n = 16: σ_x̄ = {{3}}.', 'n = 64: σ_x̄ = {{1.5}}.'])])

R[SI, 1] = dict(obj='identify point estimates and compute standard errors and margins of error',
  idea='A confidence interval is point estimate ± margin of error, and margin of error = critical value × standard error.',
  voc=[['point estimate', 'A single statistic used to estimate a parameter, like p̂ or x̄.'], ['standard error', 'The estimated standard deviation of a statistic.'], ['margin of error', 'How far the estimate is likely to be from the parameter.']],
  watch='Taking the full width of an interval as the margin of error (it is half the width).',
  cards=[dict(h='Reading an interval', big='Point estimate = {{midpoint}}; margin of error = half the width.',
    steps=['(0.30, 0.38): p̂ = {{0.34}}.', 'Margin of error = {{0.04}}.'])])

R[SI, 2] = dict(obj='interpret confidence levels and intervals and check the conditions for inference',
  idea='The confidence level describes the method: about C% of intervals built this way capture the parameter. Check Random, 10% and Large Counts (or Normal) before computing.',
  voc=[['confidence level', 'The long-run capture rate of the method.'], ['10% condition', 'n ≤ 10% of the population, so observations are about independent.'], ['Large Counts', 'At least 10 successes and 10 failures.']],
  watch='Saying “there is a 95% probability that p is in this interval.”',
  cards=[dict(h='Interpretation template', big='“We are C% confident that the interval from __ to __ captures the true {{parameter in context}}.”',
    steps=['Higher confidence → larger z* → {{wider}} interval.', 'Larger n → {{narrower}} interval.'])])

R[SI, 3] = dict(obj='construct and interpret a one-proportion z interval and find the sample size for a margin of error',
  idea='p̂ ± z*·√(p̂(1 − p̂)/n). To plan a study, solve the margin-of-error formula for n and round up.',
  voc=[['z*', 'The critical value: 1.645, 1.96 and 2.576 for 90%, 95% and 99%.'], ['one-sample z interval for p', 'p̂ ± z*√(p̂(1 − p̂)/n).'], ['p*', 'A guess for p; 0.5 gives the largest n.']],
  watch='Rounding the sample size down.',
  cards=[dict(h='Four steps for an interval', big='State, Plan (conditions), Do (compute), {{Conclude}} in context.',
    steps=['n = 400, p̂ = 0.5, 95%: ME = 1.96 × 0.025 = {{0.049}}.', 'Interval: 0.5 ± 0.049 = ({{0.451}}, 0.549).', 'ME ≤ 0.03 at 95% with p* = 0.5: n ≥ {{1,068}}.'])])

R[SI, 4] = dict(obj='construct and interpret a one-sample t interval for a mean',
  idea='When σ is unknown, use s and a t distribution with n − 1 degrees of freedom: x̄ ± t*·s/√n.',
  voc=[['t distribution', 'Like the standard Normal but with heavier tails; depends on df.'], ['degrees of freedom', 'n − 1 for one-sample t procedures.'], ['Normal/large sample condition', 'n ≥ 30, or no strong skew or outliers in the sample.']],
  watch='Using z* instead of t* when σ is unknown.',
  cards=[dict(h='t interval', big='⟨\\bar x \\pm t^* \\dfrac{s}{\\sqrt n}⟩ with df = {{n − 1}}.',
    steps=['n = 16, s = 6: SE = {{1.5}}.', '95% with df = 15: t* ≈ {{2.131}}.', 'x̄ = 48: interval ≈ (44.80, {{51.20}}).'])])

R[SI, 5] = dict(obj='write null and alternative hypotheses about a parameter',
  idea='H₀ is the claim of no effect or no change (=). Hₐ is what the researcher suspects (<, > or ≠), decided before seeing the data. Both are about parameters.',
  voc=[['null hypothesis H₀', 'The claim we look for evidence against.'], ['alternative hypothesis Hₐ', 'The claim we hope to find evidence for.'], ['parameter', 'p, μ, p₁ − p₂, μ_d …']],
  watch='Writing hypotheses with statistics (p̂ or x̄) instead of parameters.',
  cards=[dict(h='Writing hypotheses', big='Define the parameter in words, then H₀ uses {{=}}.',
    steps=['Last year p = 0.12; testing for an increase: Hₐ: p {{>}} 0.12.', 'Testing whether the mean differs from 500: Hₐ: μ {{≠}} 500.'])])

R[SI, 6] = dict(obj='compute test statistics and p-values and state conclusions in context',
  idea='A test statistic measures how far the statistic is from the null value in standard errors. The p-value is the probability of a result at least that extreme if H₀ is true.',
  voc=[['test statistic', '(statistic − null value)/standard error.'], ['p-value', 'P(a result at least as extreme as observed | H₀ true).'], ['significance level α', 'The cutoff for rejecting H₀.']],
  watch='Saying the p-value is the probability that H₀ is true.',
  cards=[dict(h='Decision rule', big='If p-value < α, {{reject H₀}}; otherwise fail to reject H₀ — never “accept” it.',
    steps=['z = 2.00 with Hₐ: >: p-value ≈ {{0.0228}}.', 'At α = 0.05: {{reject H₀}}: convincing evidence for Hₐ.'])])

R[SI, 7] = dict(obj='carry out one-proportion z tests and one-sample t tests',
  idea='Same four steps every time. For proportions, the standard deviation uses p₀; for means, use s and a t distribution with df = n − 1.',
  voc=[['one-sample z test for p', 'z = (p̂ − p₀)/√(p₀(1 − p₀)/n).'], ['one-sample t test for μ', 't = (x̄ − μ₀)/(s/√n).'], ['conclusion in context', 'Link the p-value to α and state what it means for the parameter.']],
  watch='Using p̂ instead of p₀ in the standard deviation for a z test.',
  cards=[dict(h='z test for p', big='Check Large Counts with {{p₀}}: np₀ ≥ 10 and n(1 − p₀) ≥ 10.',
    steps=['p₀ = 0.5, n = 100, p̂ = 0.6: z = 0.1/0.05 = {{2}}.', 'Hₐ: p > 0.5: p-value ≈ {{0.0228}}.'])])

R[SI, 8] = dict(obj='describe Type I and Type II errors and the factors that affect power',
  idea='A Type I error rejects a true H₀ (probability α); a Type II error misses a false H₀. Power, the chance of correctly rejecting, rises with n, α and the size of the effect.',
  voc=[['Type I error', 'Rejecting H₀ when it is true.'], ['Type II error', 'Failing to reject H₀ when it is false.'], ['power', '1 − P(Type II error).']],
  watch='Describing an error without context, or mixing up which error each decision risks.',
  cards=[dict(h='Errors in context', big='Type I: conclude Hₐ when H₀ is {{true}}.',
    steps=['Power = 0.8: P(Type II) = {{0.2}}.', 'To raise power: increase {{n}} or α.'])])

R[SI, 9] = dict(obj='construct intervals and carry out tests for a difference of two proportions',
  idea='Compare p₁ − p₂. Intervals use each sample’s p̂; tests of H₀: p₁ = p₂ use the pooled proportion in the standard error.',
  voc=[['difference of proportions', 'p₁ − p₂.'], ['pooled proportion', '(x₁ + x₂)/(n₁ + n₂), used when H₀ says p₁ = p₂.'], ['two-sample z test', 'z = (p̂₁ − p̂₂)/SE_pooled.']],
  watch='Using the pooled proportion for a confidence interval.',
  cards=[dict(h='Pooling', big='p̂_C = {{(x₁ + x₂)/(n₁ + n₂)}} — for tests only.',
    steps=['30/100 and 50/100: p̂_C = {{0.4}}.', 'An interval for p₁ − p₂ that contains 0 means {{no convincing difference}}.'])])

R[SI, 10] = dict(obj='choose and carry out two-sample t procedures and paired t procedures',
  idea='Two independent groups → two-sample t on x̄₁ − x̄₂. The same individuals measured twice (or matched pairs) → one-sample t on the differences.',
  voc=[['two-sample t', 't = (x̄₁ − x̄₂)/√(s₁²/n₁ + s₂²/n₂).'], ['paired t', 't = d̄/(s_d/√n), df = n − 1.'], ['conservative df', 'min(n₁, n₂) − 1.']],
  watch='Running a two-sample test on paired data, which ignores the pairing and loses power.',
  cards=[dict(h='Paired or two-sample?', big='Same individuals twice → {{paired}}; separate groups → two-sample.',
    steps=['Before-and-after scores for 25 students: paired t, df = {{24}}.', 'd̄ = 2.4, s_d = 3: t = 2.4/0.6 = {{4}}.'])])

R[SI, 11] = dict(obj='construct a confidence interval for the slope of a regression line (beyond the 2026 AP course)',
  idea='The sample slope b estimates the true slope β; the interval is b ± t*·SE_b with df = n − 2. Zero inside the interval means no convincing linear relationship.',
  voc=[['β', 'The slope of the population regression line.'], ['SE_b', 'The standard error of the slope, read from computer output.'], ['LINER', 'Linear, Independent, Normal residuals, Equal SD, Random.']],
  watch='Using df = n − 1 instead of n − 2.',
  cards=[dict(h='Slope interval', big='⟨b \\pm t^*\\,SE_b⟩ with df = {{n − 2}}.',
    steps=['n = 22, b = 0.8, SE_b = 0.2, 95%: t* ≈ {{2.086}}.', 'Interval ≈ (0.383, {{1.217}}); 0 is not inside.'])])

R[SI, 12] = dict(obj='carry out a chi-square goodness-of-fit test (beyond the 2026 AP course)',
  idea='Compare observed counts with the counts expected under a claimed distribution: χ² = Σ(O − E)²/E with df = categories − 1.',
  voc=[['expected count', 'n × claimed proportion.'], ['chi-square statistic', 'Σ (observed − expected)²/expected.'], ['df', 'Number of categories − 1.']],
  watch='Using proportions instead of counts in the χ² formula.',
  cards=[dict(h='Expected counts', big='E = n × (claimed {{proportion}}); every E should be at least 5.',
    steps=['n = 200, claimed 0.30: E = {{60}}.', 'Observed 68: (68 − 60)²/60 ≈ {{1.07}}.'])])

R[SI, 13] = dict(obj='carry out chi-square tests for homogeneity and independence',
  idea='Expected count = row total × column total ÷ table total. Large χ² (small p-value) is evidence of an association or of different distributions.',
  voc=[['test for independence', 'One sample, two categorical variables.'], ['test for homogeneity', 'Several samples or groups, one categorical variable.'], ['df', '(rows − 1)(columns − 1).']],
  watch='Mixing up homogeneity (separate samples) and independence (one sample, two variables).',
  cards=[dict(h='Two-way expected counts', big='⟨E = \\dfrac{\\text{row total} \\times \\text{column total}}{\\text{table total}}⟩.',
    steps=['Row 70, column 120, total 300: E = {{28}}.', '3 × 4 table: df = {{6}}.'])])

R[SI, 14] = dict(obj='test for a linear relationship with a t test for the slope (beyond the 2026 AP course)',
  idea='H₀: β = 0 says there is no linear relationship. t = b/SE_b with df = n − 2; a small p-value is evidence of a linear relationship.',
  voc=[['H₀: β = 0', 'No linear relationship between x and y in the population.'], ['t for the slope', 't = (b − 0)/SE_b.'], ['regression output', 'The Coef and SE Coef columns give b and SE_b.']],
  watch='Reading the intercept row instead of the slope (x) row of the output.',
  cards=[dict(h='Slope test', big='t = b/SE_b, df = {{n − 2}}.',
    steps=['b = 2.4, SE_b = 0.8: t = {{3}}.', 'n = 20: df = {{18}}.'])])
