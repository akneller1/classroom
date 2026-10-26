const Gm = require('../geo.cjs');
const tri = Gm.triangle([[30, 100], [110, 20], [170, 100]], ['', '', ''], { w: 230, h: 115, in: 1.7, angles: [[0, '1', 18, -6], [1, '2', 0, 22]] }).replace('</svg>', Gm.line(170, 100, 222, 100) + Gm.t(190, 92, 'ext', { c: '#db2777', fs: 10 }) + '</svg>');
module.exports = {
  name: 'geometry-angles-parallel-lines', course: 'Geometry', unitNo: 2, unitName: 'Angles and Parallel Lines',
  focus: 'angle pairs and parallel lines cut by a transversal',
  morefocus: 'proving lines parallel, triangle angle sums and angle chasing',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['transversal', 'A line that crosses two or more lines.', 'line ⟨t⟩'], ['corresponding', 'Same position at each intersection.', '⟨\\angle 1⟩, ⟨\\angle 5⟩'],
      ['alternate interior', 'Between the lines, opposite sides of ⟨t⟩.', '⟨\\angle 3⟩, ⟨\\angle 5⟩'], ['alternate exterior', 'Outside the lines, opposite sides of ⟨t⟩.', '⟨\\angle 1⟩, ⟨\\angle 7⟩'],
      ['same-side interior', 'Between the lines, same side of ⟨t⟩.', '⟨\\angle 4⟩, ⟨\\angle 5⟩']] },
    { title: 'Parallel Lines & a Transversal', color: 'blue', kind: 'table', head: ['If the lines are parallel…', 'Angles are'], rows: [
      ['corresponding ⟨\\angle 1, \\angle 5⟩', 'congruent'], ['alternate interior ⟨\\angle 3, \\angle 5⟩', 'congruent'], ['alternate exterior ⟨\\angle 1, \\angle 7⟩', 'congruent'], ['same-side interior ⟨\\angle 4, \\angle 5⟩', 'supplementary (180°)']],
      fig: Gm.parallels(), figFirst: true },
    { title: 'Basic Angle Pairs', color: 'green', kind: 'table', head: ['Pair', 'Rule'], rows: [
      ['complementary', 'sum ⟨90^\\circ⟩'], ['supplementary', 'sum ⟨180^\\circ⟩'], ['vertical', 'congruent'], ['linear pair', 'supplementary']],
      after: 'If one angle is ⟨118^\\circ⟩, its vertical angle is ⟨118^\\circ⟩ and each neighbor is ⟨62^\\circ⟩.', check: { num: '180-118', is: 62 } },
    { title: 'Solving Angle Equations', color: 'orange', kind: 'example', text: 'Use the relationship: congruent → set equal; supplementary → add to 180.',
      example: 'Corresponding angles ⟨(3x + 15)^\\circ⟩ and ⟨(5x - 25)^\\circ⟩', steps: [['Set equal:', '⟨3x + 15 = 5x - 25⟩'], ['Solve:', '⟨40 = 2x,\\ x = 20⟩']], answer: '⟨x = 20⟩; each angle ⟨75^\\circ⟩', check: { list: ['3*20+15', '5*20-25'], is: [75, 75] } },
    { title: 'Same-Side Interior Example', color: 'pink', kind: 'example', text: 'Same-side interior angles of parallel lines are supplementary.',
      example: '⟨(x + 30)^\\circ⟩ and ⟨(2x)^\\circ⟩', steps: [['Add to 180:', '⟨3x + 30 = 180,\\ x = 50⟩']], answer: '⟨80^\\circ⟩ and ⟨100^\\circ⟩', check: { list: ['50+30', '2*50'], is: [80, 100] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['These rules need parallel lines.', 'Name the pair before writing an equation.', 'Check: do your angles add correctly?'],
      bad: [['Same-side interior are congruent', 'they are supplementary'], ['Mixing alternate interior and exterior', 'interior = between the lines'], ['Using the rules on non-parallel lines', 'not allowed']] }
  ],
  back: [
    { title: 'Converses: Proving Lines Parallel', color: 'purple', kind: 'words', rows: [
      ['Corresponding angles are congruent', '⟨r \\parallel s⟩'], ['Alternate interior angles are congruent', '⟨r \\parallel s⟩'], ['Alternate exterior angles are congruent', '⟨r \\parallel s⟩'], ['Same-side interior angles are supplementary', '⟨r \\parallel s⟩']] },
    { title: 'Triangle Angle Sum', color: 'blue', kind: 'example', text: 'The interior angles of a triangle add to ⟨180^\\circ⟩.',
      example: 'Angles ⟨47^\\circ⟩, ⟨63^\\circ⟩, ⟨x^\\circ⟩', steps: [['Add:', '⟨110 + x = 180⟩']], answer: '⟨x = 70^\\circ⟩', check: { num: '180-47-63', is: 70 } },
    { title: 'Exterior Angle Theorem', color: 'green', kind: 'example', text: 'An exterior angle equals the sum of the two remote interior angles: ⟨ext = \\angle 1 + \\angle 2⟩.',
      example: 'Exterior ⟨125^\\circ⟩, one remote angle ⟨52^\\circ⟩', steps: [['Equation:', '⟨125 = 52 + x⟩']], answer: '⟨x = 73^\\circ⟩', fig: tri, check: { num: '125-52', is: 73 } },
    { title: 'Angle Chasing', color: 'orange', kind: 'example', text: 'Chain the relationships one step at a time and give a reason for each.',
      example: 'A corresponding angle is ⟨108^\\circ⟩.', steps: [['Corresponding:', '⟨108^\\circ⟩'], ['Vertical:', '⟨108^\\circ⟩'], ['Linear pair:', '⟨180 - 108 = 72^\\circ⟩']], answer: '⟨108^\\circ⟩ and ⟨72^\\circ⟩', check: { num: '180-108', is: 72 } },
    { title: 'Reasons for Proofs', color: 'pink', kind: 'words', rows: [
      ['Vertical angles are congruent.', 'Vertical Angles Thm.'], ['∥ lines → corresponding angles ≅', 'Corresponding Angles Post.'], ['∥ lines → alternate interior angles ≅', 'Alt. Interior Angles Thm.'], ['Two angles that form a line add to 180°.', 'Linear Pair Post.']] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Are the lines marked parallel (arrows)?', 'Which pair is it: corresponding, alternate or same-side?', 'Congruent → set equal; supplementary → add to 180.', 'Did I find the angle measures, not just ⟨x⟩?'] }
  ]
};
