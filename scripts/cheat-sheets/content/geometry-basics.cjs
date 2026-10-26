const Gm = require('../geo.cjs'), F = require('../figs.cjs');
const naming = Gm.svg(230, 70,
  Gm.line(10, 18, 70, 18) + Gm.dot(10, 18) + Gm.dot(70, 18) + Gm.t(10, 34, 'A') + Gm.t(70, 34, 'B') + Gm.t(40, 58, 'segment AB', { fs: 9, w: 400 }) +
  Gm.line(90, 18, 150, 18) + '<path d="M150 18 l-8 -4 v8z" fill="#1f2a6b"/>' + Gm.dot(90, 18) + Gm.dot(120, 18) + Gm.t(90, 34, 'C') + Gm.t(120, 34, 'D') + Gm.t(120, 58, 'ray CD', { fs: 9, w: 400 }) +
  Gm.line(165, 18, 225, 18) + '<path d="M225 18 l-8 -4 v8z M165 18 l8 -4 v8z" fill="#1f2a6b"/>' + Gm.dot(180, 18) + Gm.dot(210, 18) + Gm.t(180, 34, 'E') + Gm.t(210, 34, 'F') + Gm.t(195, 58, 'line EF', { fs: 9, w: 400 }), 2.7);
module.exports = {
  name: 'geometry-basics', course: 'Geometry', unitNo: 1, unitName: 'Foundations of Geometry',
  focus: 'points, lines, planes, segments, rays and angles',
  morefocus: 'segment and angle addition, midpoints, distance and angle pairs',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['point', 'An exact location; no size.', '⟨A⟩'], ['line', 'Straight path extending forever both ways.', '⟨\\overleftrightarrow{AB}⟩'],
      ['plane', 'A flat surface extending forever.', 'plane ⟨\\mathcal{P}⟩'], ['segment', 'Part of a line with two endpoints.', '⟨\\overline{AB}⟩'],
      ['ray', 'Part of a line with one endpoint.', '⟨\\overrightarrow{AB}⟩'], ['angle', 'Two rays with a common endpoint (vertex).', '⟨\\angle ABC⟩']] },
    { title: 'Naming Figures', color: 'blue', kind: 'list', items: [
      'Ray order matters: ⟨\\overrightarrow{CD}⟩ starts at ⟨C⟩; ⟨\\overrightarrow{DC}⟩ starts at ⟨D⟩.', 'Name an angle with the vertex in the middle: ⟨\\angle ABC = \\angle CBA⟩.', '<b>Collinear</b>: on one line. <b>Coplanar</b>: in one plane.'], fig: naming, figFirst: true },
    { title: 'Classifying Angles', color: 'green', kind: 'table', head: ['Type', 'Measure'], rows: [
      ['acute', '⟨0^\\circ < m\\angle < 90^\\circ⟩'], ['right', '⟨m\\angle = 90^\\circ⟩ (box symbol)'], ['obtuse', '⟨90^\\circ < m\\angle < 180^\\circ⟩'], ['straight', '⟨m\\angle = 180^\\circ⟩']],
      fig: Gm.angle(42, ['A', 'B', 'C'], { m: '42°', in: 1.4 }) },
    { title: 'Angle Pairs', color: 'orange', kind: 'table', head: ['Pair', 'Rule'], rows: [
      ['complementary', 'add to ⟨90^\\circ⟩: ⟨60^\\circ + 30^\\circ⟩'], ['supplementary', 'add to ⟨180^\\circ⟩: ⟨110^\\circ + 70^\\circ⟩'], ['vertical angles', 'opposite angles at an intersection are equal'], ['linear pair', 'adjacent and supplementary']],
      fig: Gm.crossing(40, { in: 1.5 }) },
    { title: 'Algebra with Angles', color: 'pink', kind: 'example', text: 'Set up the equation from the relationship, solve, then find each angle.',
      example: '⟨(x + 15)^\\circ⟩ and ⟨(2x - 3)^\\circ⟩ are supplementary.', steps: [['Equation:', '⟨3x + 12 = 180,\\ x = 56⟩'], ['Angles:', '⟨71^\\circ⟩ and ⟨109^\\circ⟩']], answer: '⟨71^\\circ⟩ and ⟨109^\\circ⟩', check: { list: ['56+15', '2*56-3'], is: [71, 109] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Use degree symbols with angle measures.', 'Vertical angles are congruent (equal).', 'Mark congruent parts with matching ticks and arcs.'],
      bad: [['Ray ⟨AB⟩ = ray ⟨BA⟩', 'the endpoint comes first'], ['Vertical angles add to 180°', 'they are equal'], ['Complementary vs supplementary', '90° vs 180°']] }
  ],
  back: [
    { title: 'Segment Addition', color: 'purple', kind: 'example', text: 'If ⟨B⟩ is between ⟨A⟩ and ⟨C⟩, then ⟨AB + BC = AC⟩.',
      example: '⟨AB = 8⟩ and ⟨BC = 11⟩', steps: [['Add:', '⟨AC = 8 + 11⟩']], answer: '⟨AC = 19⟩', fig: Gm.segment([['A', 0], ['B', 0.42], ['C', 1]], [[0, 0.42, '8'], [0.42, 1, '11']]), check: { num: '8+11', is: 19 } },
    { title: 'Midpoint', color: 'blue', kind: 'example', text: 'The midpoint splits a segment into two congruent halves. On a grid: ⟨M = \\left(\\tfrac{x_1 + x_2}{2}, \\tfrac{y_1 + y_2}{2}\\right)⟩.',
      example: 'Midpoint of ⟨(2, 1)⟩ and ⟨(6, 9)⟩', steps: [['Average:', '⟨\\left(\\tfrac{8}{2}, \\tfrac{10}{2}\\right)⟩']], answer: '⟨(4, 5)⟩', fig: Gm.segment([['A', 0], ['M', 0.5, '#db2777'], ['B', 1]], [], { ticks: [[0, 0.5, 1], [0.5, 1, 1]] }), check: { list: ['(2+6)/2', '(1+9)/2'], is: [4, 5] } },
    { title: 'Distance Formula', color: 'green', kind: 'example', text: '⟨d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}⟩ (the Pythagorean Theorem on a grid).',
      example: '⟨P(2, 1)⟩ to ⟨Q(6, 4)⟩', steps: [['Substitute:', '⟨\\sqrt{4^2 + 3^2} = \\sqrt{25}⟩']], answer: '5 units',
      fig: F.plane({ id: 'gd', xmin: 0, xmax: 7, ymin: 0, ymax: 5, size: 1.3, segments: [{ x1: 2, y1: 1, x2: 6, y2: 4, color: '#2563eb' }, { x1: 2, y1: 1, x2: 6, y2: 1, dashed: true, color: '#db2777', w: 1.5 }, { x1: 6, y1: 1, x2: 6, y2: 4, dashed: true, color: '#db2777', w: 1.5 }], points: [{ x: 2, y: 1, label: 'P' }, { x: 6, y: 4, label: 'Q' }] }), check: { num: 'Math.sqrt(16+9)', is: 5 } },
    { title: 'Angle Addition', color: 'orange', kind: 'example', text: 'If ray ⟨BD⟩ is inside ⟨\\angle ABC⟩: ⟨m\\angle ABD + m\\angle DBC = m\\angle ABC⟩.',
      example: '⟨m\\angle ABD = 34^\\circ⟩, ⟨m\\angle DBC = 56^\\circ⟩', steps: [['Add:', '⟨34^\\circ + 56^\\circ⟩']], answer: '⟨m\\angle ABC = 90^\\circ⟩', check: { num: '34+56', is: 90 } },
    { title: 'Bisectors', color: 'pink', kind: 'list', items: [
      'A <b>segment bisector</b> passes through the midpoint.', 'An <b>angle bisector</b> splits an angle into two congruent angles.', 'If ray ⟨BD⟩ bisects ⟨\\angle ABC = 80^\\circ⟩, each half is ⟨40^\\circ⟩.', '<b>Perpendicular</b> lines meet at ⟨90^\\circ⟩: ⟨\\perp⟩.'] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I put the vertex letter in the middle?', 'Do my parts add up to the whole (segment or angle addition)?', 'Complementary → 90°, supplementary → 180°, vertical → equal.', 'Is my diagram labeled with given lengths and angles?'] }
  ]
};
