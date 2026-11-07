/* Statistics Unit 1 cheat sheet (Exploring Data). Every worked example is checked by build.cjs. */
const SF = require('../statfigs.cjs');
const r4 = v => String(Math.round(v * 10000) / 10000);
module.exports = {
  name: 'statistics-exploring-data', course: 'Statistics', unitNo: 1, unitName: 'Exploring Data',
  focus: 'displays, shape, center, spread, box plots, outliers, normal models and z-scores',
  morefocus: 'two-way tables, scatterplots, correlation, least-squares regression and residuals',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['categorical variable', 'Places each individual in a group.', 'eye color, grade level'],
      ['quantitative variable', 'A number you can average.', 'height, test score'],
      ['distribution', 'The values a variable takes and how often.', 'a histogram of scores'],
      ['outlier', 'A value far from the rest (1.5 · IQR rule).', '30 in 3, 5, 7, …, 14'],
      ['resistant', 'Not pulled much by outliers.', 'median and IQR']] },
    { title: 'Describing a Distribution', color: 'blue', kind: 'table', plain: true, head: ['SOCS', 'What to say'], rows: [
      ['<b>Shape</b>', 'symmetric, skewed left / right, unimodal / bimodal'],
      ['<b>Outliers</b>', 'name any unusual values (or say none)'],
      ['<b>Center</b>', 'mean (symmetric) or median (skewed)'],
      ['<b>Spread</b>', 'SD (symmetric) or IQR (skewed); range']],
      after: 'Always answer <b>in context</b>. Skewed right (long tail right): mean &gt; median.' },
    { title: 'Mean and Standard Deviation', color: 'green', kind: 'example', text: '⟨\\bar{x} = \\dfrac{\\sum x}{n}⟩, ⟨s = \\sqrt{\\dfrac{\\sum (x - \\bar{x})^2}{n - 1}}⟩: the typical distance from the mean.',
      example: 'Data: 4, 6, 7, 9, 14', steps: [['Mean:', '⟨\\tfrac{40}{5} = 8⟩'], ['Squared deviations:', '16, 4, 1, 1, 36 (sum 58)'], ['⟨s⟩:', '⟨\\sqrt{58/4} = \\sqrt{14.5}⟩']],
      answer: '⟨\\bar{x} = 8⟩, ⟨s \\approx 3.81⟩',
      check: [{ num: '(4+6+7+9+14)/5', is: 8 }, { num: '16+4+1+1+36', is: 58 }, { num: 'Math.round(Math.sqrt(58/4)*100)/100', is: 3.81 }] },
    { title: 'Box Plots and the Outlier Rule', color: 'orange', kind: 'example', text: 'Outlier if below ⟨Q_1 - 1.5\\,\\text{IQR}⟩ or above ⟨Q_3 + 1.5\\,\\text{IQR}⟩.',
      example: '3, 5, 7, 8, 9, 11, 12, 14, 30', steps: [['Summary:', 'min 3, ⟨Q_1⟩ 6, median 9, ⟨Q_3⟩ 13, max 30'], ['Fences:', 'IQR = 7, so ⟨6 - 10.5 = -4.5⟩ and ⟨13 + 10.5 = 23.5⟩']],
      answer: '30 is an outlier',
      fig: SF.boxplot({ min: 3, q1: 6, med: 9, q3: 13, max: 14, outliers: [30], lo: 0, hi: 30, step: 5, inches: 2.6 }),
      check: [{ num: '(5+7)/2', is: 6 }, { num: '(12+14)/2', is: 13 }, { num: '6-1.5*7', is: -4.5 }, { num: '13-6', is: 7 }, { num: '13+1.5*7', is: 23.5 }, { true: '30 > 13+1.5*7 && 3 > 6-1.5*7' }] },
    { title: 'Normal Models and z-Scores', color: 'pink', kind: 'html',
      html: 'Empirical rule: <b>68%</b> within 1σ, <b>95%</b> within 2σ, <b>99.7%</b> within 3σ. ⟨z = \\tfrac{x - \\mu}{\\sigma}⟩ counts SDs from the mean. SAT ⟨N(500, 100)⟩: a 650 has ⟨z = 1.5⟩; ⟨P(Z > 1.5) \\approx 0.067⟩.',
      figFirst: true,
      fig: SF.normal({ shade: [[-1, 1, '#db2777'], [-2, -1, '#2563eb'], [1, 2, '#2563eb']], inches: 2.6, labels: [{ z: 0, y: 0.45, t: '68%', color: '#9d174d' }, { z: -1.5, y: 0.12, t: '13.5%', fs: 8 }, { z: 1.5, y: 0.12, t: '13.5%', fs: 8 }],
        marks: [{ z: -3, t: 'μ−3σ' }, { z: -2, t: 'μ−2σ' }, { z: -1, t: 'μ−σ' }, { z: 0, t: 'μ' }, { z: 1, t: 'μ+σ' }, { z: 2, t: 'μ+2σ' }, { z: 3, t: 'μ+3σ' }] }),
      check: [{ num: '(650-500)/100', is: 1.5 }, { num: r4(SF.upper(1.5)), is: 0.0668 }, { num: '(95-68)/2', is: 13.5 }] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Label displays and describe them in context.', 'Use median & IQR when data are skewed or have outliers.', 'A histogram’s bars touch; a bar graph’s don’t.'],
      bad: [['Dividing by ⟨n⟩ for ⟨s⟩', 'divide by ⟨n - 1⟩'], ['“The data is normal”', 'say “approximately normal”'], ['Comparing only centers', 'compare SOCS for both groups']] }
  ],
  back: [
    { title: 'Two-Way Tables', color: 'purple', kind: 'table', head: ['', 'Plays sport', 'No sport', 'Total'], rows: [
      ['Grade 10', '45', '55', '100'], ['Grade 11', '60', '40', '100'], ['Total', '105', '95', '200']],
      after: 'Marginal: ⟨P(\\text{sport}) = \\tfrac{105}{200} = 52.5\\%⟩. Conditional: ⟨\\tfrac{45}{100} = 45\\%⟩ of 10th graders vs ⟨60\\%⟩ of 11th graders. Different conditional percents ⟹ an <b>association</b>.',
      check: [{ num: '45+60', is: 105 }, { num: '55+40', is: 95 }, { num: '105/200', is: 0.525 }] },
    { title: 'Scatterplots and Correlation', color: 'blue', kind: 'html',
      html: 'Describe <b>direction, form, strength</b> and unusual points. Correlation ⟨-1 \\le r \\le 1⟩ measures the strength of a <b>linear</b> relationship; it has no units and is not resistant.',
      fig: SF.scatter({ pts: [[2, 62], [3, 63], [4, 68], [5, 69], [6, 78], [7, 74], [8, 80]], xlo: 1, xhi: 9, ylo: 55, yhi: 85, xstep: 1, ystep: 10, line: [55, 3], xlab: 'Hours studied', ylab: 'Score', inches: 2.2, h: 130 }),
      check: { true: '[[2,62],[3,63],[4,68],[5,69],[6,78],[7,74],[8,80]].every(p => Math.abs(p[1] - (55 + 3*p[0])) <= 5)' } },
    { title: 'Least-Squares Regression Line', color: 'green', kind: 'example', text: '⟨\\hat{y} = a + bx⟩ with ⟨b = r\\,\\tfrac{s_y}{s_x}⟩ and ⟨a = \\bar{y} - b\\bar{x}⟩. The line passes through ⟨(\\bar{x}, \\bar{y})⟩.',
      example: '⟨\\bar{x} = 5⟩, ⟨s_x = 2⟩, ⟨\\bar{y} = 70⟩, ⟨s_y = 8⟩, ⟨r = 0.75⟩', steps: [['Slope:', '⟨b = 0.75 \\cdot \\tfrac{8}{2} = 3⟩'], ['Intercept:', '⟨a = 70 - 3(5) = 55⟩'], ['Predict at 6 h:', '⟨55 + 3(6) = 73⟩']],
      answer: '⟨\\hat{y} = 55 + 3x⟩; predicted score 73',
      check: [{ num: '0.75*8/2', is: 3 }, { num: '70-3*5', is: 55 }, { num: '55+3*6', is: 73 }] },
    { title: 'Interpreting the Model', color: 'orange', kind: 'table', plain: true, head: ['Value', 'Interpretation in context'], rows: [
      ['<b>Slope</b> ⟨b = 3⟩', 'predicted score rises 3 points per extra hour'],
      ['<b>Intercept</b> ⟨a = 55⟩', 'predicted score for 0 hours (only if 0 makes sense)'],
      ['⟨r^2 = 0.75^2⟩', '56.25% of the variation in score is explained by the line'],
      ['<b>s</b> (residual SD)', 'typical prediction error, in y units']],
      after: 'Template: “The predicted <i>y</i> increases/decreases by <i>b</i> for each 1-unit increase in <i>x</i>.”',
      check: { num: '0.75**2', is: 0.5625 } },
    { title: 'Residuals', color: 'pink', kind: 'example', text: 'Residual = actual − predicted = ⟨y - \\hat{y}⟩. A residual plot with <b>no pattern</b> means a linear model fits.',
      example: 'A student who studied 6 h scored 78.', steps: [['Predicted:', '73'], ['Residual:', '⟨78 - 73 = 5⟩']], answer: '+5: the line under-predicted by 5',
      fig: SF.scatter({ pts: [[2, 1], [3, -1], [4, 1], [5, -1], [6, 5], [7, -2], [8, 1]], xlo: 1, xhi: 9, ylo: -6, yhi: 6, xstep: 1, ystep: 3, resid: true, xlab: 'Hours studied', ylab: 'Residual', inches: 1.9, h: 110 }),
      check: [{ num: '78-73', is: 5 }, { list: [62 - 61, 63 - 64, 68 - 67, 69 - 70, 78 - 73, 74 - 76, 80 - 79], is: [1, -1, 1, -1, 5, -2, 1] }] },
    { title: 'Cautions with Regression', color: 'teal', kind: 'mistakes',
      good: ['Plot the data and the residuals first.', 'Use ⟨\\hat{y}⟩ (“predicted”) in the equation.', 'Influential points (far right or left) can change the slope a lot.'],
      bad: [['Correlation ⟹ causation', 'association only'], ['Predicting far outside the data', 'that is extrapolation'], ['Using ⟨r⟩ for a curved pattern', '⟨r⟩ is for linear form']] }
  ]
};
