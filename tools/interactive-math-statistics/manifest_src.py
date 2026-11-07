# Source of manifest.json for the Statistics Interactive Math tools. Run inside this folder: python3 manifest_src.py
import json
T = []
def tool(slug, unit, unitName, title, intro, description, topics, discovery, also=None):
    d = dict(slug=slug, course='statistics', unit=unit, unitName=unitName, title=title, intro=intro, description=description, topics=topics, discovery=discovery)
    if also: d['also'] = also
    T.append(d)
tool('statistics-sampling-distribution-lab', 'anticipating-patterns', 'Anticipating Patterns', 'Sampling Distribution Lab',
     'Take many random samples from a population and record one statistic from each. Compare the population, a single sample, and the distribution of the statistic.',
     'Draw samples from skewed, uniform, bimodal or normal populations (or a proportion) and build the sampling distribution of x̄ or p̂. See unbiasedness, how spread shrinks with √n, the Central Limit Theorem and the Large Counts condition.',
     ['Sampling distributions', 'Central Limit Theorem', 'Standard deviation of x̄ and p̂'],
     'The sampling distribution of x̄ or p̂ is centered at the parameter, its SD shrinks like 1/√n (σ/√n or √(p(1−p)/n)), and for large enough n its shape is approximately normal whatever the population looks like.')
tool('statistics-confidence-interval-lab', 'statistical-inference', 'Statistical Inference', 'Confidence Interval Lab',
     'Take random sample after random sample and build a confidence interval from each. Count how many capture the true value, and see what changes their width.',
     'Build hundreds of one-proportion z-intervals or one-mean t-intervals from repeated samples. Watch the capture rate, see how confidence level and sample size change the margin of error, and test what happens when conditions fail or z* replaces t*.',
     ['Confidence intervals', 'Margin of error', 'Conditions for inference'],
     'A C% confidence level means about C% of intervals from repeated samples capture the parameter; higher confidence widens intervals, quadrupling n halves the margin of error, and capture rates fall short when conditions fail or z* is used with s for small n.')
tool('statistics-significance-power-explorer', 'statistical-inference', 'Statistical Inference', 'Significance Test & Power Explorer',
     'Run a one-proportion z test. See the p-value as an area under the null model, then switch tabs to see Type I error, Type II error and power as areas.',
     'Set H₀, Hₐ, α, n and the sample result for a one-proportion z test and watch the p-value appear as a tail area under the null model. Then compare the null and true models to see Type I error, Type II error and power, and what raises power.',
     ['p-values', 'Type I and Type II errors', 'Power'],
     'A p-value is the probability of a result at least as extreme as the observed one if H₀ is true (two-sided doubles it); the same p̂ is more significant with larger n; power grows with n, α and the size of the true effect, and lowering α raises β.')
tool('statistics-sampling-methods-lab', 'sampling-experimentation', 'Sampling and Experimentation', 'Sampling Methods Lab',
     'Estimate how much a school’s students sleep. Sample with five different methods, repeat each one many times, and compare where the estimates center and how much they vary.',
     'Take simple random, stratified, cluster, systematic and convenience samples from a 160-student population and repeat them hundreds of times. Separate bias (center) from variability (spread), see why a bigger convenience sample is still biased, and why stratifying helps.',
     ['Sampling methods', 'Bias and variability', 'Stratified and cluster sampling'],
     'Bias is where a method’s estimates center and variability is how much they spread: random methods are unbiased, larger samples reduce variability but not bias, stratifying on a related variable reduces variability, and clusters that each resemble one stratum increase it.')
tool('statistics-conditional-probability-explorer', 'anticipating-patterns', 'Anticipating Patterns', 'Conditional Probability: Screening Tests',
     'A screening test is usually right. So if you test positive, how likely is it that you have the condition? Change the base rate and the test’s accuracy and follow 100,000 people through the tree.',
     'Link a tree diagram, a two-way table and a “who tests positive” bar to see why P(condition | positive) differs from P(positive | condition), how strongly it depends on the base rate and on specificity, and what independence looks like.',
     ['Conditional probability', 'Two-way tables and tree diagrams', 'Independence'],
     'P(A | B) and P(B | A) have different denominators; when a condition is rare, false positives can outnumber true positives, so P(condition | positive) depends heavily on prevalence and specificity; the test result is independent of the condition exactly when P(+ | C) = P(+ | not C).')
tool('statistics-regression-influence-lab', 'exploring-data', 'Exploring Data', 'Residuals & Influence Lab',
     'Drag points and watch the least-squares line, r, r² and the residual plot respond. Then add one extra point and find out what makes a point an outlier, high leverage or influential.',
     'Fit a least-squares line with a linked residual plot. See why a high r does not prove a line is the right model, separate outliers, high-leverage points and influential points with a movable extra point, and check what changing units does to the slope, r and r².',
     ['Least-squares regression', 'Residual plots', 'Outliers, leverage and influence'],
     'A residual plot with a pattern shows a line is the wrong model even when r is near 1; outliers have large residuals, high-leverage points have extreme x-values, and points are influential when removing them changes the line a lot; changing units rescales the slope but not r or r².')
tool('statistics-random-assignment-lab', 'sampling-experimentation', 'Sampling and Experimentation', 'Random Assignment Lab',
     'Does a study app raise quiz scores? Put 20 volunteers into groups three different ways, repeat the experiment, then run a randomization test on one experiment.',
     'Compare random assignment, randomized matched pairs and letting students choose. See confounding create a fake effect, see random assignment balance GPA on average (but not every time), see pairing reduce variability, and find a p-value by re-randomizing the group labels.',
     ['Random assignment and confounding', 'Matched pairs and blocking', 'Randomization tests'],
     'Random assignment balances lurking variables on average, so differences center on the true effect, while self-selection confounds the treatment with GPA; matching reduces variability; and a randomization test’s p-value is the share of label shuffles at least as extreme as the observed difference.')
json.dump({'version': '20261108', 'labVersion': '20261105', 'tools': T}, open('manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(T), 'tools in manifest')
