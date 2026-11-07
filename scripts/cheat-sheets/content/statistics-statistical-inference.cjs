/* Statistics Unit 4 cheat sheet (Statistical Inference). Every worked example is checked by build.cjs. */
const SF = require('../statfigs.cjs');
const r4 = v => String(Math.round(v * 10000) / 10000);
module.exports = {
  name: 'statistics-statistical-inference', course: 'Statistics', unitNo: 4, unitName: 'Statistical Inference',
  focus: 'confidence intervals for a proportion and a mean, conditions and interpretation',
  morefocus: 'significance tests, p-values, Type I and II errors, power and two-sample procedures',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['point estimate', 'A statistic used to estimate a parameter.', '⟨\\hat{p} = 0.6⟩ estimates ⟨p⟩'],
      ['standard error', 'Estimated SD of the statistic.', '⟨\\sqrt{\\hat{p}(1 - \\hat{p})/n}⟩'],
      ['margin of error', 'Critical value × standard error.', '⟨\\pm 0.048⟩'],
      ['confidence level', 'Success rate of the method in repeated samples.', '95%'],
      ['critical value', '⟨z^*⟩ or ⟨t^*⟩ for the confidence level.', '⟨z^* = 1.96⟩']] },
    { title: 'Building an Interval', color: 'blue', kind: 'table', plain: true, head: ['Piece', 'What to use'], rows: [
      ['Form', 'statistic ± (critical value)(standard error)'],
      ['Conditions', '<b>Random</b>; <b>10%</b>: ⟨n \\le 0.1N⟩; <b>Large counts</b> ⟨n\\hat{p}, n(1 - \\hat{p}) \\ge 10⟩ or <b>Normal</b> (⟨n \\ge 30⟩ or no strong skew)'],
      ['⟨z^*⟩', '90%: 1.645 · 95%: 1.96 · 99%: 2.576']],
      after: 'Higher confidence ⟹ wider. Larger ⟨n⟩ ⟹ narrower (ME shrinks like ⟨1/\\sqrt{n}⟩).',
      check: [{ num: 'Math.round(1.6449*1000)/1000', is: 1.645 }, { num: r4(SF.upper(1.96)), is: 0.025 }, { num: r4(SF.upper(2.576)), is: 0.005 }] },
    { title: 'One-Proportion z-Interval', color: 'green', kind: 'example', text: '⟨\\hat{p} \\pm z^* \\sqrt{\\dfrac{\\hat{p}(1 - \\hat{p})}{n}}⟩',
      example: '240 of 400 random voters support a bond. 95% CI?', steps: [['⟨\\hat{p}⟩:', '⟨\\tfrac{240}{400} = 0.60⟩; counts 240 and 160 ≥ 10'], ['SE:', '⟨\\sqrt{0.6(0.4)/400} \\approx 0.0245⟩'], ['ME:', '⟨1.96(0.0245) \\approx 0.048⟩']],
      answer: '(0.552, 0.648)',
      check: [{ num: '240/400', is: 0.6 }, { num: 'Math.round(Math.sqrt(0.24/400)*10000)/10000', is: 0.0245 }, { num: 'Math.round((0.6-1.96*Math.sqrt(0.24/400))*1000)/1000', is: 0.552 }, { num: 'Math.round((0.6+1.96*Math.sqrt(0.24/400))*1000)/1000', is: 0.648 }] },
    { title: 'One-Mean t-Interval', color: 'orange', kind: 'example', text: '⟨\\bar{x} \\pm t^* \\dfrac{s}{\\sqrt{n}}⟩ with ⟨df = n - 1⟩.',
      example: '⟨n = 25⟩, ⟨\\bar{x} = 82⟩, ⟨s = 10⟩. 95% CI?', steps: [['⟨t^*⟩:', 'df = 24, ⟨t^* = 2.064⟩'], ['SE:', '⟨10/\\sqrt{25} = 2⟩'], ['ME:', '⟨2.064(2) = 4.128⟩']],
      answer: '(77.87, 86.13)',
      check: [{ num: '10/Math.sqrt(25)', is: 2 }, { num: 'Math.round((82-2.064*2)*100)/100', is: 77.87 }, { num: 'Math.round((82+2.064*2)*100)/100', is: 86.13 }] },
    { title: 'Interpreting and Planning', color: 'pink', kind: 'table', plain: true, rows: [
      ['<b>Interval</b>', '“We are 95% confident that the interval from 0.552 to 0.648 captures the true proportion of <i>all voters</i> who support the bond.”'],
      ['<b>Level</b>', '“If we took many samples, about 95% of the intervals would capture the true proportion.”'],
      ['<b>Sample size</b>', 'ME ≤ 0.03 at 95%: ⟨n \\ge (\\tfrac{1.96}{0.03})^2(0.5)(0.5) = 1067.1⟩, so ⟨n = 1068⟩']],
      check: [{ num: 'Math.round((1.96/0.03)**2*0.25*10)/10', is: 1067.1 }, { num: 'Math.ceil((1.96/0.03)**2*0.25)', is: 1068 }] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Check conditions before computing.', 'Intervals estimate a <b>parameter</b>, never a statistic.', 'Use ⟨\\hat{p} = 0.5⟩ for sample size when you have no guess.'],
      bad: [['“95% chance ⟨p⟩ is in this interval”', 'the method captures ⟨p⟩ 95% of the time'], ['Using ⟨z^*⟩ for a mean with ⟨s⟩', 'use ⟨t^*⟩ with ⟨df = n - 1⟩'], ['Rounding ⟨n⟩ down', 'always round up']] }
  ],
  back: [
    { title: 'The Four-Step Process', color: 'purple', kind: 'table', plain: true, rows: [
      ['<b>State</b>', '⟨H_0⟩ (no effect, “=”), ⟨H_a⟩ (⟨<⟩, ⟨>⟩ or ⟨\\ne⟩), ⟨\\alpha⟩; define the parameter'],
      ['<b>Plan</b>', 'name the test; check Random, 10%, Large counts / Normal'],
      ['<b>Do</b>', 'test statistic, then the p-value'],
      ['<b>Conclude</b>', 'compare p to ⟨\\alpha⟩ and answer in context']],
      after: 'Hypotheses are always about <b>parameters</b> (⟨p⟩, ⟨\\mu⟩), never ⟨\\hat{p}⟩ or ⟨\\bar{x}⟩.' },
    { title: 'Test Statistics', color: 'blue', kind: 'table', plain: true, head: ['Test', 'Statistic'], rows: [
      ['One proportion', '⟨z = \\dfrac{\\hat{p} - p_0}{\\sqrt{p_0(1 - p_0)/n}}⟩'],
      ['One mean', '⟨t = \\dfrac{\\bar{x} - \\mu_0}{s/\\sqrt{n}}⟩, ⟨df = n - 1⟩'],
      ['Two proportions', '⟨z = \\dfrac{\\hat{p}_1 - \\hat{p}_2}{\\sqrt{\\hat{p}_C(1 - \\hat{p}_C)(\\tfrac{1}{n_1} + \\tfrac{1}{n_2})}}⟩']],
      after: 'statistic = ⟨\\dfrac{\\text{observed} - \\text{hypothesized}}{\\text{SD of statistic}}⟩' },
    { title: 'One-Proportion z-Test', color: 'green', kind: 'example', text: '⟨H_0: p = 0.5⟩, ⟨H_a: p > 0.5⟩, ⟨\\alpha = 0.05⟩.',
      example: '270 of 500 randomly chosen students prefer the new schedule.', steps: [['⟨\\hat{p}⟩:', '⟨\\tfrac{270}{500} = 0.54⟩'], ['⟨z⟩:', '⟨\\tfrac{0.54 - 0.5}{\\sqrt{0.25/500}} \\approx 1.79⟩'], ['p-value:', '⟨P(Z > 1.79) \\approx 0.037 < 0.05⟩']],
      answer: 'reject ⟨H_0⟩: convincing evidence ⟨p > 0.5⟩',
      check: [{ num: '270/500', is: 0.54 }, { num: 'Math.round((0.54-0.5)/Math.sqrt(0.25/500)*100)/100', is: 1.79 }, { num: String(Math.round(SF.upper(1.79) * 1000) / 1000), is: 0.037 }] },
    { title: 'p-Values and Conclusions', color: 'orange', kind: 'words', rows: [
      ['p-value: the probability of a result this extreme <i>if ⟨H_0⟩ is true</i>', 'small p = evidence for ⟨H_a⟩'],
      ['⟨p < \\alpha⟩', 'reject ⟨H_0⟩; convincing evidence for ⟨H_a⟩'],
      ['⟨p \\ge \\alpha⟩', 'fail to reject ⟨H_0⟩; not convincing evidence'],
      ['Never write', '“accept ⟨H_0⟩” or “proves ⟨H_0⟩”']] },
    { title: 'Errors and Power', color: 'pink', kind: 'table', head: ['', '⟨H_0⟩ true', '⟨H_0⟩ false'], rows: [
      ['Reject ⟨H_0⟩', '<b>Type I</b> (prob. ⟨\\alpha⟩)', '✔ correct (power)'],
      ['Fail to reject', '✔ correct', '<b>Type II</b> (prob. ⟨\\beta⟩)']],
      after: 'Power = ⟨1 - \\beta⟩. Power rises with larger ⟨n⟩, larger ⟨\\alpha⟩, or a true value farther from ⟨p_0⟩ or ⟨\\mu_0⟩.' },
    { title: 'Choosing the Procedure', color: 'teal', kind: 'table', plain: true, head: ['Situation', 'Procedure'], rows: [
      ['One group, yes/no data', 'one-proportion z'],
      ['One group, numerical data', 'one-sample t'],
      ['Two independent groups, yes/no', 'two-proportion z (CI or test)'],
      ['Two independent groups, numerical', 'two-sample t'],
      ['Same subjects measured twice / pairs', 'paired t on the differences'],
      ['Slope of a regression line', '⟨b \\pm t^* SE_b⟩, ⟨df = n - 2⟩']] }
  ]
};
