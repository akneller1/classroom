const Gm = require('../geo.cjs');
const sim = Gm.svg(240, 100,
  '<polygon points="15,85 50,30 85,85" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/>' + Gm.t(25, 55, '6', { c: '#2563eb' }) + Gm.t(50, 98, '8', { c: '#2563eb' }) + Gm.t(10, 95, 'A', { fs: 10 }) + Gm.t(50, 24, 'B', { fs: 10 }) + Gm.t(90, 95, 'C', { fs: 10 }) +
  '<polygon points="110,85 162,5 214,85" fill="#fde8f1" stroke="#1f2a6b" stroke-width="2"/>' + Gm.t(125, 45, '9', { c: '#db2777' }) + Gm.t(162, 98, 'x', { c: '#db2777' }) + Gm.t(104, 95, 'D', { fs: 10 }) + Gm.t(172, 12, 'E', { fs: 10 }) + Gm.t(220, 95, 'F', { fs: 10 }), 2.0);
const shadow = Gm.svg(240, 100,
  Gm.line(10, 85, 230, 85) + Gm.line(40, 85, 40, 55, '#1f2a6b', 3) + Gm.line(40, 55, 80, 85, '#999', 1.3, true) + Gm.t(30, 72, '6', { c: '#2563eb' }) + Gm.t(60, 98, '4', { c: '#2563eb' }) +
  Gm.line(120, 85, 120, 10, '#16a34a', 5) + Gm.line(120, 10, 220, 85, '#999', 1.3, true) + Gm.t(108, 50, 'h', { c: '#db2777' }) + Gm.t(170, 98, '10', { c: '#db2777' }), 2.0);
module.exports = {
  name: 'geometry-similarity', course: 'Geometry', unitNo: 5, unitName: 'Similarity',
  focus: 'scale factors, similar figures and proportions',
  morefocus: 'similarity criteria, dilations, area and indirect measurement',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['similar', 'Same shape, not necessarily the same size: ⟨\\sim⟩.', '⟨\\triangle ABC \\sim \\triangle DEF⟩'], ['corresponding angles', 'Matching angles; they are congruent.', '⟨\\angle A \\cong \\angle D⟩'],
      ['corresponding sides', 'Matching sides; they are proportional.', '⟨\\tfrac{AB}{DE} = \\tfrac{BC}{EF}⟩'], ['scale factor', 'The number each length is multiplied by.', '⟨k = \\tfrac{3}{2}⟩']] },
    { title: 'Similarity Statements', color: 'blue', kind: 'list', items: [
      'The order of the letters tells which parts correspond: ⟨ABCD \\sim EFGH⟩ means ⟨A \\leftrightarrow E⟩, ⟨B \\leftrightarrow F⟩, ….', 'Angles: ⟨\\angle A \\cong \\angle E⟩, ⟨\\angle B \\cong \\angle F⟩, ….', 'Sides: ⟨\\tfrac{AB}{EF} = \\tfrac{BC}{FG} = \\tfrac{CD}{GH} = \\tfrac{DA}{HE}⟩.'] },
    { title: 'Finding a Scale Factor', color: 'green', kind: 'example', text: 'Scale factor = image length ÷ original length (use corresponding sides).',
      example: 'A side changes from 6 to 9.', steps: [['Ratio:', '⟨\\tfrac{9}{6} = \\tfrac{3}{2}⟩']], answer: '⟨k = \\tfrac{3}{2}⟩ (an enlargement)', check: { num: '9/6', is: 1.5 } },
    { title: 'Finding a Missing Side', color: 'orange', kind: 'example', text: 'Set up a proportion with corresponding sides in the same order, then cross multiply.',
      example: '⟨\\triangle ABC \\sim \\triangle DEF⟩: ⟨\\tfrac{6}{9} = \\tfrac{8}{x}⟩', steps: [['Cross multiply:', '⟨6x = 72⟩']], answer: '⟨x = 12⟩', fig: sim, check: { num: '9*8/6', is: 12 } },
    { title: 'Perimeter & Area', color: 'pink', kind: 'table', plain: true, head: ['If the scale factor is ⟨k⟩', 'Ratio'], rows: [
      ['perimeters', '⟨k⟩'], ['areas', '⟨k^2⟩'], ['volumes', '⟨k^3⟩']],
      after: 'Scale factor 3: perimeters ⟨3 : 1⟩, areas ⟨9 : 1⟩. A ⟨4 \\text{ in}^2⟩ figure becomes ⟨36 \\text{ in}^2⟩.', check: { num: '4*3**2', is: 36 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Match corresponding sides in the same order.', 'Keep small-to-large (or large-to-small) on both sides of the proportion.', 'Areas scale by ⟨k^2⟩.'],
      bad: [['Mixing up the order of sides', 'follow the similarity statement'], ['Using ⟨k⟩ for areas', 'use ⟨k^2⟩'], ['Assuming figures are similar', 'check AA, SAS~ or SSS~']] }
  ],
  back: [
    { title: 'Triangle Similarity Criteria', color: 'purple', kind: 'table', head: ['Criterion', 'Needs'], rows: [
      ['AA', 'two pairs of congruent angles'], ['SAS~', 'two pairs of proportional sides and the included angles congruent'], ['SSS~', 'all three pairs of sides proportional']] },
    { title: 'SAS~ Example', color: 'blue', kind: 'example', text: 'The included angles are congruent and the sides around them are proportional.',
      example: '⟨\\angle A \\cong \\angle D = 60^\\circ⟩; ⟨\\tfrac{4}{6} = \\tfrac{8}{x}⟩', steps: [['Cross multiply:', '⟨4x = 48⟩']], answer: '⟨x = 12⟩', check: { num: '6*8/4', is: 12 } },
    { title: 'SSS~ Example', color: 'green', kind: 'example', text: 'All three ratios must be equal.',
      example: 'Sides 5, 7, 9 and 10, ⟨x⟩, 18', steps: [['Ratio:', '⟨\\tfrac{5}{10} = \\tfrac{9}{18} = \\tfrac{1}{2}⟩'], ['Solve:', '⟨\\tfrac{7}{x} = \\tfrac{1}{2}⟩']], answer: '⟨x = 14⟩', check: { list: ['5/10', '9/18', '7/14'], is: [0.5, 0.5, 0.5] } },
    { title: 'Dilations', color: 'orange', kind: 'list', items: [
      'A dilation with scale factor ⟨k⟩ multiplies every length by ⟨k⟩ and keeps angles the same.', '⟨k > 1⟩: enlargement. ⟨0 < k < 1⟩: reduction.', 'Centered at the origin: ⟨(x, y) \\to (kx, ky)⟩.', 'Sides 4, 6, 8 with ⟨k = 3⟩ become 12, 18, 24.'] },
    { title: 'Indirect Measurement', color: 'pink', kind: 'example', text: 'Similar triangles from shadows: object ÷ shadow is the same for both.',
      example: 'A 6-ft person casts a 4-ft shadow; a tree casts a 10-ft shadow.', steps: [['Proportion:', '⟨\\tfrac{6}{4} = \\tfrac{h}{10}⟩']], answer: '⟨h = 15⟩ ft', fig: shadow, check: { num: '6*10/4', is: 15 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I use corresponding sides in the same order?', 'Is my scale factor image ÷ original?', 'Did I square the scale factor for area?', 'Does the answer make sense (bigger figure → bigger lengths)?'] }
  ]
};
