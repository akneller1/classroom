/* Pre-Algebra (8th Grade) Unit 6 cheat sheet. Every worked example is checked by build.cjs; figures are drawn from the same coordinates. */
const F = require('../figs.cjs'), Gm = require('../geo.cjs');
const A = [[1, 1], [3, 1], [1, 3]];
const moves = F.plane({ id: 'c6a', xmin: -4, xmax: 4, ymin: -4, ymax: 4, size: 1.25, ticks: 2,
  polys: [{ pts: A, color: '#1f2a6b', fill: '#1f2a6b' }, { pts: A.map(p => [-p[0], p[1]]), color: '#db2777', fill: '#db2777' }, { pts: A.map(p => [p[1], -p[0]]), color: '#16a34a', fill: '#16a34a' }, { pts: A.map(p => [p[0] - 4, p[1] - 4]), color: '#ea7a12', fill: '#ea7a12', dashed: true }],
  labels: [{ x: 2.3, y: 3.3, t: 'A', fs: 9 }, { x: -2.3, y: 3.3, t: 'reflect', fs: 8, color: '#db2777' }, { x: 2.8, y: -3.5, t: 'rotate', fs: 8, color: '#16a34a' }, { x: -2, y: -3.7, t: 'translate', fs: 8, color: '#ea7a12' }] });
const dil = F.plane({ id: 'c6b', xmin: 0, xmax: 7, ymin: 0, ymax: 5, size: 1.15, ticks: 1,
  polys: [{ pts: [[1, 1], [3, 1], [1, 2]], color: '#2563eb', fill: '#2563eb' }, { pts: [[2, 2], [6, 2], [2, 4]], color: '#db2777', fill: '#db2777' }],
  segments: [{ x1: 0, y1: 0, x2: 6, y2: 2, dashed: true, w: 1 }, { x1: 0, y1: 0, x2: 2, y2: 4, dashed: true, w: 1 }] });
const tri = Gm.triangle([[15, 100], [95, 20], [185, 100]], ['', '', ''], { angles: [[0, '48°', 18, -6], [1, 'x', 0, 24], [2, '57°', -22, -6]], w: 200, h: 110, in: 1.7 });
module.exports = {
  name: 'prealgebra-congruence-similarity', course: 'Pre-Algebra (8th Grade)', unitNo: 6, unitName: 'Congruence and Similarity',
  focus: 'translations, reflections, rotations and dilations on the coordinate plane',
  morefocus: 'congruence and similarity through transformations, triangle angles and parallel lines',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['transformation', 'A rule that moves or resizes a figure.', '⟨A \\to A\'⟩'],
      ['rigid motion', 'Translation, reflection or rotation: keeps size and shape.', 'same size'],
      ['dilation', 'Enlarges or shrinks by a scale factor ⟨k⟩.', '⟨k = 2⟩'],
      ['congruent', 'Same size and shape (⟨\\cong⟩).', 'rigid motions only'],
      ['similar', 'Same shape; sides proportional (⟨\\sim⟩).', 'add a dilation']] },
    { title: 'Coordinate Rules', color: 'blue', kind: 'table', plain: true, head: ['Transformation', 'Rule'], rows: [
      ['translate ⟨a⟩ right, ⟨b⟩ up', '⟨(x, y) \\to (x + a, y + b)⟩'], ['reflect over ⟨x⟩-axis', '⟨(x, y) \\to (x, -y)⟩'], ['reflect over ⟨y⟩-axis', '⟨(x, y) \\to (-x, y)⟩'],
      ['rotate 90° clockwise', '⟨(x, y) \\to (y, -x)⟩'], ['rotate 90° counterclockwise', '⟨(x, y) \\to (-y, x)⟩'], ['rotate 180°', '⟨(x, y) \\to (-x, -y)⟩'], ['dilate by ⟨k⟩ (origin)', '⟨(x, y) \\to (kx, ky)⟩']] },
    { title: 'Rigid Motions', color: 'green', kind: 'example', text: 'Apply the rule to every vertex. Lengths and angles stay the same.',
      example: 'Triangle A: ⟨(1, 1), (3, 1), (1, 3)⟩. Rotate 90° clockwise.', steps: [['Rule ⟨(y, -x)⟩:', '⟨(1, -1), (1, -3), (3, -1)⟩']], answer: 'the green triangle', fig: moves, figFirst: false,
      check: { list: ['1', '-1', '1', '-3', '3', '-1'], is: [1, -1, 1, -3, 3, -1] } },
    { title: 'Dilations', color: 'orange', kind: 'example', text: 'Multiply every coordinate by ⟨k⟩. ⟨k > 1⟩ enlarges; ⟨0 < k < 1⟩ shrinks. Angles stay the same; lengths multiply by ⟨k⟩.',
      example: 'Dilate ⟨(1, 1), (3, 1), (1, 2)⟩ by ⟨k = 2⟩.', steps: [['Multiply:', '⟨(2, 2), (6, 2), (2, 4)⟩']], answer: 'similar, every side twice as long', fig: dil,
      check: { num: '(6-2)/(3-1)', is: 2 } },
    { title: 'Sequences of Transformations', color: 'pink', kind: 'list', items: [
      'Do the moves in order; the image of one step is the preimage of the next.', 'Only rigid motions → the figures are <b>congruent</b>.', 'Rigid motions and a dilation → the figures are <b>similar</b>.',
      'Example: ⟨(2, 1)⟩ reflect over ⟨y⟩-axis → ⟨(-2, 1)⟩, then translate down 3 → ⟨(-2, -2)⟩.'] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Label images with primes: ⟨A\', B\', C\'⟩.', 'Clockwise and counterclockwise give different images.', 'Orientation flips after a reflection.'],
      bad: [['Reflecting over the ⟨x⟩-axis by changing ⟨x⟩', 'change the sign of ⟨y⟩'], ['Adding ⟨k⟩ in a dilation', 'multiply by ⟨k⟩'], ['Calling a dilation congruent', 'it is similar']] }
  ],
  back: [
    { title: 'Triangle Angle Sum', color: 'purple', kind: 'example', text: 'The three angles of every triangle add to ⟨180^\\circ⟩. An exterior angle equals the sum of the two remote interior angles.',
      example: 'Angles ⟨48^\\circ⟩, ⟨57^\\circ⟩ and ⟨x⟩.', steps: [['Equation:', '⟨48 + 57 + x = 180⟩']], answer: '⟨x = 75^\\circ⟩', fig: tri,
      check: { num: '180-48-57', is: 75 } },
    { title: 'Parallel Lines and a Transversal', color: 'blue', kind: 'table', plain: true, head: ['Angle pair (diagram)', 'Relationship'], rows: [
      ['corresponding: 1 & 5, 2 & 6', 'congruent'], ['alternate interior: 3 & 5, 4 & 6', 'congruent'], ['alternate exterior: 1 & 7, 2 & 8', 'congruent'], ['same-side interior: 4 & 5, 3 & 6', 'add to ⟨180^\\circ⟩'], ['vertical: 1 & 3', 'congruent']],
      fig: Gm.parallels({ in: 2.0 }) },
    { title: 'Solving with Angle Pairs', color: 'green', kind: 'example', text: 'Name the relationship, write the equation, solve.',
      example: 'Alternate interior angles: ⟨(3x + 10)^\\circ⟩ and ⟨70^\\circ⟩.', steps: [['Congruent:', '⟨3x + 10 = 70⟩'], ['Solve:', '⟨3x = 60⟩']], answer: '⟨x = 20⟩',
      check: { num: '(70-10)/3', is: 20 } },
    { title: 'Similar Triangles (AA)', color: 'orange', kind: 'example', text: 'Two pairs of congruent angles make triangles similar. Then corresponding sides are proportional.',
      example: '⟨\\triangle ABC \\sim \\triangle DEF⟩, ⟨AB = 4⟩, ⟨BC = 6⟩, ⟨DE = 10⟩. Find ⟨EF⟩.', steps: [['Proportion:', '⟨\\tfrac{4}{10} = \\tfrac{6}{x}⟩'], ['Cross multiply:', '⟨4x = 60⟩']], answer: '⟨EF = 15⟩',
      check: { num: '6*10/4', is: 15 } },
    { title: 'Congruent or Similar?', color: 'pink', kind: 'words', rows: [
      ['Reflect, then translate', 'congruent'], ['Rotate 180°, then dilate by ⟨\\tfrac{1}{2}⟩', 'similar'], ['Two triangles with angles 40°, 60°, 80°', 'similar (AA)'], ['Same angles and same side lengths', 'congruent']] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I apply the rule to <b>every</b> vertex?', 'Did I use the right direction for the rotation?', 'Do my triangle angles add to 180°?', 'Did I match corresponding sides in the proportion?'] }
  ]
};
