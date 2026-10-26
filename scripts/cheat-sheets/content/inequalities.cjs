const F = require('../figs.cjs');
module.exports = {
  name: 'inequalities', course: 'Algebra 1', unitNo: 3, unitName: 'Linear Inequalities',
  focus: 'writing, solving and graphing inequalities',
  morefocus: 'compound inequalities, absolute value and inequalities in context',
  front: [
    { title: 'Symbols & Key Phrases', color: 'purple', kind: 'table', head: ['Symbol', 'Means', 'Phrases'], rows: [
      ['⟨<⟩', 'less than', 'fewer than, below'], ['⟨>⟩', 'greater than', 'more than, above'], ['⟨\\le⟩', 'less than or equal to', '<b>at most</b>, no more than'], ['⟨\\ge⟩', 'greater than or equal to', '<b>at least</b>, no less than'], ['⟨\\ne⟩', 'not equal to', 'is not']] },
    { title: 'Graphing on a Number Line', color: 'blue', kind: 'list', items: [
      '<b>Open circle</b> for ⟨<⟩ or ⟨>⟩: the endpoint is not included.', '<b>Closed circle</b> for ⟨\\le⟩ or ⟨\\ge⟩: the endpoint is included.', 'With the variable on the left, shade the way the sign points: ⟨<⟩ left, ⟨>⟩ right.'],
      fig: '<div style="display:flex;gap:6px;justify-content:center;font-size:8pt"><div>x &gt; 1' + F.nl(-3, 4, [{ a: 1, b: null, ac: false }], { scale: 0.72, w: 260 }) + '</div><div>x ≤ −1' + F.nl(-3, 4, [{ a: null, b: -1, bc: true, color: '#db2777' }], { scale: 0.72, w: 260 }) + '</div></div>' },
    { title: 'Solving: Like an Equation', color: 'green', kind: 'example', text: 'Use inverse operations. Keep the variable on one side.',
      example: 'Solve ⟨3x - 7 \\le 8⟩.', steps: [['Add 7:', '⟨3x \\le 15⟩'], ['Divide by 3:', '⟨x \\le 5⟩']], answer: '⟨x \\le 5⟩', check: { true: '3*5-7 <= 8 && 3*6-7 > 8' } },
    { title: 'Reverse the Sign!', color: 'orange', kind: 'example', text: 'When you <b>multiply or divide by a negative</b>, flip the inequality symbol.',
      example: 'Solve ⟨-2p > 10⟩.', steps: [['Divide by ⟨-2⟩ and flip:', '⟨p < -5⟩']], answer: '⟨p < -5⟩', check: { true: '-2*(-6) > 10 && !(-2*(-5) > 10)' },
      fig: F.nl(-8, -2, [{ a: null, b: -5, bc: false, color: '#ea7a12' }]) },
    { title: 'Check a Solution', color: 'pink', kind: 'words', rows: [
      ['Is ⟨x = 6⟩ a solution of ⟨x + 4 > 9⟩? ⟨6 + 4 = 10 > 9⟩', '<span class="ok">✔ yes</span>'], ['Is ⟨x = 4⟩ a solution? ⟨4 + 4 = 8⟩, and ⟨8 > 9⟩ is false', '<span class="no">✘ no</span>'], ['Test a point on the shaded side to check your graph.', 'test point']],
      check: { true: '6+4>9 && !(4+4>9)' } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Open circle: ⟨<, >⟩. Closed circle: ⟨\\le, \\ge⟩.', 'Flip the sign only when multiplying or dividing by a negative.', 'Check a value from your answer in the original inequality.'],
      bad: [['“5 less than ⟨x⟩”', 'is ⟨x - 5⟩, not ⟨5 - x⟩'], ['Flipping when you add or subtract a negative', 'no flip needed'], ['Shading the wrong way', 'test a point']] }
  ],
  back: [
    { title: 'Writing Inequalities', color: 'purple', kind: 'words', rows: [
      ['A number ⟨x⟩ is at least 6.', '⟨x \\ge 6⟩'], ['A number ⟨n⟩ is less than 12.', '⟨n < 12⟩'], ['7 more than ⟨y⟩ is no more than 19.', '⟨y + 7 \\le 19⟩'], ['Twice ⟨p⟩ is greater than 14.', '⟨2p > 14⟩']] },
    { title: 'Compound Inequalities', color: 'blue', kind: 'list', items: [
      '<b>AND</b>: both are true, so shade the <b>overlap</b>. ⟨2 < x \\le 7⟩', '<b>OR</b>: either is true, so shade <b>both</b> parts. ⟨x < -3⟩ or ⟨x \\ge 1⟩'],
      fig: F.nl(0, 9, [{ a: 2, b: 7, ac: false, bc: true }]) + F.nl(-5, 5, [{ a: null, b: -3, bc: false, color: '#7b4fd0' }, { a: 1, b: null, ac: true, color: '#16a34a' }]) },
    { title: 'Solve a Compound Inequality', color: 'green', kind: 'example', text: 'For a three-part inequality, do the same step to all three parts.',
      example: 'Solve ⟨3 < x + 2 \\le 8⟩.', steps: [['Subtract 2:', '⟨1 < x \\le 6⟩']], answer: '⟨1 < x \\le 6⟩', check: { true: '3 < 1.5+2 && 6+2 <= 8 && !(3 < 1+2)' } },
    { title: 'Absolute Value', color: 'orange', kind: 'table', head: ['Type', 'Rewrite as'], rows: [
      ['⟨|x - 3| = 5⟩', '⟨x - 3 = 5⟩ or ⟨x - 3 = -5⟩: ⟨x = 8⟩ or ⟨x = -2⟩'], ['⟨|x| < 4⟩ (less: AND)', '⟨-4 < x < 4⟩'], ['⟨|x| \\ge 4⟩ (greater: OR)', '⟨x \\le -4⟩ or ⟨x \\ge 4⟩']],
      after: 'Isolate the absolute value first. ⟨|x| < -2⟩ has no solution.', check: { list: ['Math.abs(8-3)', 'Math.abs(-2-3)'], is: [5, 5] } },
    { title: 'Inequalities in Context', color: 'pink', kind: 'example', text: 'Write the constraint, solve, and keep answers that make sense (often whole numbers).',
      example: 'Songs cost $1.29. Ava has $10. How many songs can she buy?', steps: [['Inequality:', '⟨1.29s \\le 10⟩'], ['Divide:', '⟨s \\le 7.75⟩']], answer: 'at most 7 songs', check: { true: '1.29*7 <= 10 && 1.29*8 > 10' } },
    { title: 'Special Cases', color: 'teal', kind: 'words', rows: [
      ['⟨2x + 1 < 2x - 4 \\to 1 < -4⟩ is false', 'no solution'], ['⟨4(x + 1) \\ge 4x + 1 \\to 4 \\ge 1⟩ is true', 'all real numbers'], ['Variables on both sides: ⟨5x + 3 > 2x + 12 \\to 3x > 9⟩', '⟨x > 3⟩']],
      check: { true: '5*3.1+3 > 2*3.1+12 && !(5*3+3 > 2*3+12)' } }
  ]
};
