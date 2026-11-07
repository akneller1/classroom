/* Statistics Unit 3 cheat sheet (Anticipating Patterns). Every worked example is checked by build.cjs. */
const SF = require('../statfigs.cjs');
const r4 = v => String(Math.round(v * 10000) / 10000);
module.exports = {
  name: 'statistics-anticipating-patterns', course: 'Statistics', unitNo: 3, unitName: 'Anticipating Patterns',
  focus: 'probability rules, conditional probability, independence and simulation',
  morefocus: 'random variables, binomial and geometric models, and sampling distributions',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['probability', 'Long-run relative frequency of an outcome.', 'P(heads) = 0.5'],
      ['law of large numbers', 'With many trials, the proportion settles near the true probability.', '10,000 flips ≈ 50% heads'],
      ['sample space', 'The list of all possible outcomes.', '{1, 2, 3, 4, 5, 6}'],
      ['mutually exclusive', 'Events that cannot happen together.', 'roll a 2 and a 5'],
      ['independent', 'Knowing one event doesn’t change the other’s probability.', '⟨P(A \\mid B) = P(A)⟩']] },
    { title: 'Probability Rules', color: 'blue', kind: 'table', plain: true, head: ['Rule', 'Formula'], rows: [
      ['Complement', '⟨P(A^C) = 1 - P(A)⟩'],
      ['Addition (or)', '⟨P(A \\cup B) = P(A) + P(B) - P(A \\cap B)⟩'],
      ['Multiplication (and)', '⟨P(A \\cap B) = P(A) \\cdot P(B \\mid A)⟩'],
      ['Conditional', '⟨P(A \\mid B) = \\dfrac{P(A \\cap B)}{P(B)}⟩']],
      after: '“At least one”: ⟨1 - P(\\text{none})⟩. Three free throws at 80%: ⟨1 - 0.2^3 = 0.992⟩.',
      check: { num: '1-0.2**3', is: 0.992 } },
    { title: 'Conditional Probability from a Table', color: 'green', kind: 'table', head: ['', 'Pass', 'Fail', 'Total'], rows: [
      ['Studied', '42', '8', '50'], ['Didn’t study', '18', '12', '30'], ['Total', '60', '20', '80']],
      after: '⟨P(\\text{pass} \\mid \\text{studied}) = \\tfrac{42}{50} = 0.84⟩, but ⟨P(\\text{studied} \\mid \\text{pass}) = \\tfrac{42}{60} = 0.70⟩. The “given” group is the denominator.',
      check: [{ num: '42/50', is: 0.84 }, { num: '42/60', is: 0.7 }, { num: '42+18', is: 60 }, { num: '8+12', is: 20 }] },
    { title: 'Checking Independence', color: 'orange', kind: 'example', text: '⟨A⟩ and ⟨B⟩ are independent if ⟨P(A \\mid B) = P(A)⟩, or ⟨P(A \\cap B) = P(A) \\cdot P(B)⟩.',
      example: 'Using the table: is passing independent of studying?', steps: [['⟨P(\\text{pass})⟩:', '⟨\\tfrac{60}{80} = 0.75⟩'], ['⟨P(\\text{pass} \\mid \\text{studied})⟩:', '0.84'], ['Compare:', '⟨0.84 \\ne 0.75⟩']],
      answer: 'not independent',
      check: [{ num: '60/80', is: 0.75 }, { true: '42/50 !== 60/80' }] },
    { title: 'Simulation', color: 'pink', kind: 'list', items: [
      '<b>State</b> the question about a chance process.',
      '<b>Plan</b>: assign digits to outcomes. For ⟨p = 0.3⟩: digits 0–2 = success, 3–9 = failure. Say what one trial is and what you record.',
      '<b>Do</b> many trials (repeats allowed when trials are independent).',
      '<b>Conclude</b>: estimated probability = proportion of trials with the event.'],
      check: { num: '3/10', is: 0.3 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Draw a tree diagram for multi-stage problems.', 'Probabilities are between 0 and 1.', 'Mutually exclusive events (with nonzero ⟨P⟩) are never independent.'],
      bad: [['⟨P(A \\mid B) = P(B \\mid A)⟩', 'different denominators'], ['Adding for “and”', 'multiply for “and”'], ['Forgetting the overlap in “or”', 'subtract ⟨P(A \\cap B)⟩']] }
  ],
  back: [
    { title: 'Discrete Random Variables', color: 'purple', kind: 'example', text: '⟨\\mu_X = \\sum x\\,p⟩, ⟨\\sigma_X = \\sqrt{\\sum (x - \\mu)^2 p}⟩. The probabilities must sum to 1.',
      example: '⟨X⟩ = 0, 1, 2, 3 with ⟨p⟩ = 0.1, 0.3, 0.4, 0.2', steps: [['Mean:', '⟨0 + 0.3 + 0.8 + 0.6 = 1.7⟩'], ['Variance:', '⟨0.289 + 0.147 + 0.036 + 0.338 = 0.81⟩']],
      answer: '⟨\\mu_X = 1.7⟩, ⟨\\sigma_X = 0.9⟩',
      check: [{ num: '0*.1+1*.3+2*.4+3*.2', is: 1.7 }, { num: '(1.7**2)*.1+(0.7**2)*.3+(0.3**2)*.4+(1.3**2)*.2', is: 0.81 }, { num: 'Math.sqrt(0.81)', is: 0.9 }, { num: '.1+.3+.4+.2', is: 1 }] },
    { title: 'Transforming and Combining', color: 'blue', kind: 'table', plain: true, head: ['Random variable', 'Mean and SD'], rows: [
      ['⟨Y = a + bX⟩', '⟨\\mu_Y = a + b\\mu_X⟩, ⟨\\sigma_Y = |b|\\sigma_X⟩'],
      ['⟨X + Y⟩ or ⟨X - Y⟩', 'means add or subtract: ⟨\\mu_X \\pm \\mu_Y⟩'],
      ['⟨X \\pm Y⟩, independent', 'variances <b>always add</b>: ⟨\\sigma^2_X + \\sigma^2_Y⟩']],
      after: '⟨\\sigma_X = 3⟩, ⟨\\sigma_Y = 4⟩: ⟨\\sigma_{X - Y} = \\sqrt{9 + 16} = 5⟩ (not ⟨4 - 3⟩).',
      check: { num: 'Math.sqrt(9+16)', is: 5 } },
    { title: 'Binomial Distribution', color: 'green', kind: 'example', text: '<b>BINS</b>: Binary, Independent, fixed Number, Same ⟨p⟩. ⟨P(X = k) = \\binom{n}{k} p^k (1 - p)^{n - k}⟩, ⟨\\mu = np⟩, ⟨\\sigma = \\sqrt{np(1 - p)}⟩.',
      example: '5 free throws at ⟨p = 0.7⟩. ⟨P(X = 4)⟩?', steps: [['Formula:', '⟨\\binom{5}{4}(0.7)^4(0.3)^1⟩'], ['Mean, SD:', '⟨5(0.7) = 3.5⟩, ⟨\\sqrt{1.05} \\approx 1.02⟩']],
      answer: '⟨P(X = 4) \\approx 0.360⟩',
      check: [{ num: 'Math.round(5*0.7**4*0.3*1000)/1000', is: 0.36 }, { num: '5*0.7', is: 3.5 }, { num: 'Math.round(Math.sqrt(5*0.7*0.3)*100)/100', is: 1.02 }] },
    { title: 'Geometric Distribution', color: 'orange', kind: 'example', text: 'Count trials until the first success: ⟨P(X = k) = (1 - p)^{k - 1}p⟩, ⟨\\mu = \\tfrac{1}{p}⟩.',
      example: '20% of cereal boxes hold a prize. First prize in box 3?', steps: [['Formula:', '⟨(0.8)^2(0.2)⟩'], ['Mean:', '⟨\\tfrac{1}{0.2} = 5⟩ boxes']],
      answer: '0.128',
      check: [{ num: '0.8**2*0.2', is: 0.128 }, { num: '1/0.2', is: 5 }] },
    { title: 'Sampling Distributions', color: 'pink', kind: 'table', plain: true, head: ['Statistic', 'Center, spread, shape'], rows: [
      ['⟨\\hat{p}⟩', '⟨\\mu = p⟩, ⟨\\sigma = \\sqrt{\\tfrac{p(1 - p)}{n}}⟩; Normal if ⟨np \\ge 10⟩ and ⟨n(1 - p) \\ge 10⟩'],
      ['⟨\\bar{x}⟩', '⟨\\mu = \\mu⟩, ⟨\\sigma = \\tfrac{\\sigma}{\\sqrt{n}}⟩; Normal if population is Normal or ⟨n \\ge 30⟩ (CLT)']],
      after: '10% condition: ⟨n \\le 10\\%⟩ of the population. Larger ⟨n⟩ ⟹ less variability; an <b>unbiased</b> statistic is centered at the parameter.' },
    { title: 'Central Limit Theorem', color: 'teal', kind: 'example', text: 'For large ⟨n⟩, ⟨\\bar{x}⟩ is approximately Normal even if the population is skewed.',
      example: '⟨\\mu = 40⟩, ⟨\\sigma = 12⟩, ⟨n = 36⟩. ⟨P(\\bar{x} > 44)⟩?', steps: [['SD of ⟨\\bar{x}⟩:', '⟨\\tfrac{12}{\\sqrt{36}} = 2⟩'], ['⟨z⟩:', '⟨\\tfrac{44 - 40}{2} = 2⟩']],
      answer: '⟨P(Z > 2) \\approx 0.0228⟩',
      fig: SF.normal({ shade: [[2, 3.5, '#0d9488']], inches: 2.1, w: 260, marks: [{ z: 0, t: '40' }, { z: 2, t: '44' }], labels: [{ z: 2.6, y: 0.25, t: '0.0228', color: '#0f766e', fs: 9 }] }),
      check: [{ num: '12/Math.sqrt(36)', is: 2 }, { num: '(44-40)/2', is: 2 }, { num: r4(SF.upper(2)), is: 0.0228 }] }
  ]
};
