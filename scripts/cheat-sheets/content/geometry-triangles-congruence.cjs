const Gm = require('../geo.cjs');
const pair = (marks) => {
  const P = [[20, 90], [60, 15], [100, 90]], Q = [[130, 90], [170, 15], [210, 90]];
  let s = '';
  [P, Q].forEach((T, k) => {
    s += `<polygon points="${T.map(p => p.join(',')).join(' ')}" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/>`;
    (marks.sides || []).forEach(m => { s += Gm.tick(T[m[0]][0], T[m[0]][1], T[m[1]][0], T[m[1]][1], m[2]); });
    (marks.angles || []).forEach(m => { const v = T[m[0]], a1 = m[1], a2 = m[2]; s += Gm.arc(v[0], v[1], 13, a1, a2, '#16a34a', true); });
    ['ABC', 'DEF'][k].split('').forEach((l, i) => { s += Gm.t(T[i][0] + [-8, 0, 8][i], T[i][1] + [12, -5, 12][i], l === 'A' || l === 'D' ? l : l); });
  });
  return Gm.svg(230, 108, s, 1.9);
};
module.exports = {
  name: 'geometry-triangles-congruence', course: 'Geometry', unitNo: 3, unitName: 'Triangles & Congruence',
  focus: 'classifying triangles, angle sums, isosceles triangles and side–angle relationships',
  morefocus: 'congruence shortcuts, CPCTC and two-column proofs',
  front: [
    { title: 'Classifying Triangles', color: 'purple', kind: 'table', plain: true, head: ['By sides', 'By angles'], rows: [
      ['<b>scalene</b>: no congruent sides', '<b>acute</b>: all angles ⟨< 90^\\circ⟩'], ['<b>isosceles</b>: at least two congruent sides', '<b>right</b>: one ⟨90^\\circ⟩ angle'], ['<b>equilateral</b>: three congruent sides', '<b>obtuse</b>: one angle ⟨> 90^\\circ⟩']] },
    { title: 'Triangle Sum Theorem', color: 'blue', kind: 'example', text: 'The interior angles of a triangle add to ⟨180^\\circ⟩.',
      example: 'Angles ⟨48^\\circ⟩, ⟨67^\\circ⟩, ⟨x^\\circ⟩', steps: [['Equation:', '⟨115 + x = 180⟩']], answer: '⟨x = 65^\\circ⟩', check: { num: '180-48-67', is: 65 } },
    { title: 'Exterior Angle Theorem', color: 'green', kind: 'example', text: 'An exterior angle equals the sum of the two remote interior angles.',
      example: 'Exterior ⟨110^\\circ⟩; remote angles ⟨35^\\circ⟩ and ⟨x^\\circ⟩', steps: [['Equation:', '⟨110 = 35 + x⟩']], answer: '⟨x = 75^\\circ⟩', check: { num: '110-35', is: 75 } },
    { title: 'Isosceles Triangles', color: 'orange', kind: 'list', items: [
      'If two sides are congruent, the <b>base angles</b> opposite them are congruent.', '<b>Converse</b>: if two angles are congruent, the opposite sides are congruent.', 'Vertex angle ⟨70^\\circ⟩ → base angles ⟨\\tfrac{180 - 70}{2} = 55^\\circ⟩ each.'],
      fig: Gm.triangle([[30, 100], [100, 15], [170, 100]], ['', '', ''], { w: 200, h: 110, in: 1.3, ticks: [[0, 1, 1], [1, 2, 1]], angles: [[0, '55°', 26, -6], [2, '55°', -26, -6]] }), check: { num: '(180-70)/2', is: 55 } },
    { title: 'Triangle Inequality & Sides', color: 'pink', kind: 'list', items: [
      'Any two sides must add to <b>more</b> than the third: 4, 6, 8 works (⟨4 + 6 > 8⟩); 2, 3, 6 does not (⟨2 + 3 < 6⟩).', 'The longest side is opposite the largest angle; the shortest side is opposite the smallest angle.', 'Third side range: ⟨|a - b| < c < a + b⟩.'],
      check: { true: '4+6>8 && !(2+3>6)' } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Mark congruent sides with ticks and angles with arcs.', 'Write congruent triangles in matching vertex order.', 'Use the 180° sum first when angles are missing.'],
      bad: [['Trusting how a picture looks', 'use the marks and the givens'], ['Base angles are opposite each other', 'they are opposite the congruent sides'], ['Exterior angle = 180 − sum', 'it equals the remote sum']] }
  ],
  back: [
    { title: 'Congruence Shortcuts', color: 'purple', kind: 'table', head: ['Shortcut', 'Needs'], rows: [
      ['SSS', 'three pairs of sides'], ['SAS', 'two sides and the <b>included</b> angle'], ['ASA', 'two angles and the <b>included</b> side'], ['AAS', 'two angles and a non-included side'], ['HL', 'right triangles: hypotenuse and a leg']],
      after: '<b>Not</b> enough: AAA (similar only) and SSA.' },
    { title: 'SAS Example', color: 'blue', kind: 'example', text: 'The angle must be <b>between</b> the two sides.',
      example: '⟨AB = DE⟩, ⟨AC = DF⟩, ⟨\\angle A = \\angle D⟩', steps: [['Shortcut:', 'SAS']], answer: '⟨\\triangle ABC \\cong \\triangle DEF⟩', fig: pair({ sides: [[0, 1, 1], [0, 2, 2]], angles: [[0, 0, 62]] }) },
    { title: 'Matching Order', color: 'green', kind: 'list', items: [
      '⟨\\triangle ABC \\cong \\triangle DEF⟩ means ⟨A \\leftrightarrow D⟩, ⟨B \\leftrightarrow E⟩, ⟨C \\leftrightarrow F⟩.', 'So ⟨\\overline{AB} \\cong \\overline{DE}⟩, ⟨\\overline{BC} \\cong \\overline{EF}⟩, ⟨\\angle C \\cong \\angle F⟩.'] },
    { title: 'CPCTC', color: 'orange', kind: 'list', items: [
      '<b>C</b>orresponding <b>P</b>arts of <b>C</b>ongruent <b>T</b>riangles are <b>C</b>ongruent.', 'Use it only <b>after</b> you prove the triangles congruent.', 'It is how you prove two sides or angles are equal.'] },
    { title: 'Two-Column Proof', color: 'pink', kind: 'table', plain: true, head: ['Statement', 'Reason'], rows: [
      ['⟨\\overline{AB} \\cong \\overline{DE}⟩, ⟨\\overline{BC} \\cong \\overline{EF}⟩, ⟨\\overline{AC} \\cong \\overline{DF}⟩', 'Given'], ['⟨\\triangle ABC \\cong \\triangle DEF⟩', 'SSS'], ['⟨\\angle B \\cong \\angle E⟩', 'CPCTC']] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Is the angle in SAS (or side in ASA) really included?', 'For HL, are both triangles right triangles?', 'Did I write the vertices in matching order?', 'Did I prove congruence before using CPCTC?'] }
  ]
};
