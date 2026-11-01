/* Pre-Algebra (8th Grade) Unit 5 cheat sheet. Every worked example is checked by build.cjs; the scatter plot is drawn from the data. */
const F = require('../figs.cjs');
const X = [1, 2, 3, 4, 5, 6, 7, 8], Yv = [62, 65, 71, 70, 78, 80, 85, 88];
const sy = y => (y - 50) / 5;   // the plane is square, so scores are drawn 5 points per grid unit
const scatter = F.plane({ id: 'b5a', xmin: 0, xmax: 9, ymin: 0, ymax: 9, size: 1.55, grid: true,
  fns: [{ f: x => sy(3.75 * x + 58), color: '#db2777', dashed: true }],
  points: X.map((x, i) => ({ x, y: sy(Yv[i]), color: '#2563eb' })),
  labels: [{ x: 4.5, y: -0.1, t: 'hours studied', fs: 9, bold: false }, { x: 1.6, y: 8.4, t: 'score', fs: 9, bold: false }, { x: 8.3, y: 0.5, t: '8', fs: 9, bold: false }, { x: 0.45, y: 8, t: '90', fs: 9, bold: false }, { x: 0.45, y: 0.4, t: '50', fs: 9, bold: false }] });
const shapes = F.svg(300, 70,
  [[0, 'positive'], [75, 'negative'], [150, 'none'], [225, 'nonlinear']].map(([o, t]) => `<rect x="${o + 4}" y="2" width="67" height="50" fill="#fff" stroke="#d5dbe8"/><text x="${o + 37}" y="66" font-size="10" text-anchor="middle" font-weight="700" fill="#1f2a6b">${t}</text>`).join('') +
  [[10, 44], [18, 38], [26, 36], [34, 28], [44, 22], [52, 18], [62, 10]].map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="2.6" fill="#2563eb"/>`).join('') +
  [[10, 10], [18, 16], [28, 18], [36, 26], [44, 30], [54, 38], [62, 44]].map(p => `<circle cx="${p[0] + 75}" cy="${p[1]}" r="2.6" fill="#db2777"/>`).join('') +
  [[10, 20], [18, 42], [26, 12], [36, 34], [44, 18], [54, 44], [62, 28]].map(p => `<circle cx="${p[0] + 150}" cy="${p[1]}" r="2.6" fill="#16a34a"/>`).join('') +
  [10, 18, 26, 36, 44, 54, 62].map((x, i) => `<circle cx="${x + 225}" cy="${(10 + Math.pow(i - 3, 2) * 3.8).toFixed(1)}" r="2.6" fill="#ea7a12"/>`).join(''), 2.9);
module.exports = {
  name: 'prealgebra-patterns-bivariate-data', course: 'Pre-Algebra (8th Grade)', unitNo: 5, unitName: 'Patterns and Bivariate Data',
  focus: 'scatter plots, association and lines of best fit',
  morefocus: 'two-way tables, relative frequencies and making predictions',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['bivariate data', 'Pairs of values for two variables.', '(hours, score)'],
      ['scatter plot', 'A graph of the pairs as points.', 'see section 3'],
      ['association', 'A pattern between the two variables.', 'more study, higher score'],
      ['outlier', 'A point far from the pattern.', 'a 95 after 1 hour'],
      ['cluster', 'A group of points close together.', 'scores in the 80s']] },
    { title: 'Making a Scatter Plot', color: 'blue', kind: 'list', items: [
      'Put the explanatory variable on the ⟨x⟩-axis (hours) and the response on the ⟨y⟩-axis (score).', 'Choose equal steps on each axis; an axis may start above 0 (use a break ⟨\\wr⟩).',
      'Plot each pair as one point; do <b>not</b> connect the dots.', 'Title the graph and label both axes with units.'] },
    { title: 'Line of Best Fit', color: 'green', kind: 'example', text: 'Draw a line close to most points, with about as many above as below. Find its equation from two points on the line.',
      example: 'The line passes through ⟨(0, 58)⟩ and ⟨(8, 88)⟩.', steps: [['Slope:', '⟨\\tfrac{88 - 58}{8 - 0} = 3.75⟩'], ['Equation:', '⟨y = 3.75x + 58⟩']], answer: '⟨y = 3.75x + 58⟩', fig: scatter,
      check: [{ num: '(88-58)/8', is: 3.75 }, { true: '[1,2,3,4,5,6,7,8].filter((x,i)=>[62,65,71,70,78,80,85,88][i] > 3.75*x+58).length === 4' }] },
    { title: 'Types of Association', color: 'orange', kind: 'html', html: '<b>Positive</b>: both increase. <b>Negative</b>: one increases as the other decreases. <b>No association</b>: no pattern. <b>Linear</b> points follow a line; <b>nonlinear</b> points follow a curve. <b>Strong</b> = points close to the pattern.', fig: shapes },
    { title: 'Using the Line to Predict', color: 'pink', kind: 'example', text: 'Substitute into the equation. The slope is the change in ⟨y⟩ per unit of ⟨x⟩; the intercept is the value at ⟨x = 0⟩.',
      example: 'Predict the score after 6.5 hours with ⟨y = 3.75x + 58⟩.', steps: [['Substitute:', '⟨3.75(6.5) + 58 = 24.375 + 58⟩']], answer: 'about 82 points (+3.75 points per hour)',
      check: { num: '3.75*6.5+58', is: 82.375 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['A line of best fit does not have to touch any point.', 'Predictions far outside the data are unreliable.', 'Association does not prove that one thing causes the other.'],
      bad: [['Connecting the dots', 'draw one straight line'], ['Forcing the line through the first and last point', 'balance the points'], ['Calling a curve "linear"', 'check the shape']] }
  ],
  back: [
    { title: 'Two-Way Tables', color: 'purple', kind: 'table', head: ['', 'Plays sport', 'No sport', 'Total'], rows: [
      ['Has a pet', '18', '12', '30'], ['No pet', '14', '6', '20'], ['Total', '32', '18', '50']],
      after: 'Rows and columns add to the totals. The bottom-right cell is the grand total.', check: [{ num: '18+12', is: 30 }, { num: '14+6', is: 20 }, { num: '18+14', is: 32 }, { num: '12+6', is: 18 }, { num: '30+20', is: 50 }] },
    { title: 'Filling In a Table', color: 'blue', kind: 'example', text: 'Use the totals: each missing cell is a total minus the known cells.',
      example: '50 students, 30 have a pet, 32 play a sport, 18 do both.', steps: [['Pet, no sport:', '⟨30 - 18 = 12⟩'], ['Sport, no pet:', '⟨32 - 18 = 14⟩'], ['Neither:', '⟨50 - 18 - 12 - 14 = 6⟩']], answer: 'the table in section 1',
      check: { num: '50-18-12-14', is: 6 } },
    { title: 'Relative Frequency', color: 'green', kind: 'table', plain: true, head: ['Question', 'Divide by'], rows: [
      ['What fraction of <b>all</b> students have a pet and play?', 'grand total: ⟨\\tfrac{18}{50} = 36\\%⟩'], ['Of pet owners, what fraction play?', 'row total: ⟨\\tfrac{18}{30} = 60\\%⟩'], ['Of non-pet owners, what fraction play?', 'row total: ⟨\\tfrac{14}{20} = 70\\%⟩']],
      check: [{ num: '18/50', is: 0.36 }, { num: '18/30', is: 0.6 }, { num: '14/20', is: 0.7 }] },
    { title: 'Is There an Association?', color: 'orange', kind: 'example', text: 'Compare row (or column) percentages. Very different percentages suggest an association.',
      example: '60% of pet owners play a sport; 70% of non-pet owners play.', steps: [['Compare:', '60% vs. 70%: a 10-point difference']], answer: 'a weak association (the percents are close)',
      check: { num: '14/20-18/30', is: 0.1 } },
    { title: 'Reading Slope and Intercept', color: 'pink', kind: 'words', rows: [
      ['⟨y = 3.75x + 58⟩, ⟨x⟩ = hours, ⟨y⟩ = score: the slope means…', '+3.75 points per hour'], ['…and the ⟨y⟩-intercept means…', 'about 58 with no study'],
      ['A line ⟨y = -2x + 40⟩ for minutes of phone use vs. pages read: association?', 'negative'], ['Data points far from the line?', 'outliers']],
      check: { num: '3.75*0+58', is: 58 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Are the axes labeled with equal steps?', 'Does my line have about the same number of points above and below it?', 'Did I divide by the correct total (grand, row or column)?', 'Did I describe direction, form and strength of the association?'] }
  ]
};
