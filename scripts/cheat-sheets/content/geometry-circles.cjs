const Gm = require('../geo.cjs');
const cx = 100, cy = 70, r = 52, P = a => [cx + r * Math.cos(Gm.rad(a)), cy - r * Math.sin(Gm.rad(a))];
const parts = Gm.svg(230, 140,
  `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#e6efff" stroke="#1f2a6b" stroke-width="2"/>` +
  Gm.line(...P(180), ...P(0), '#7b4fd0') + Gm.t(70, 66, 'diameter', { c: '#7b4fd0', fs: 9 }) +
  Gm.line(cx, cy, ...P(60), '#db2777') + Gm.t(128, 50, 'radius', { c: '#db2777', fs: 9 }) +
  Gm.line(...P(120), ...P(200), '#16a34a') + Gm.t(48, 28, 'chord', { c: '#16a34a', fs: 9 }) +
  Gm.line(cx + r, cy - 60, cx + r, cy + 60, '#ea7a12') + Gm.t(188, 18, 'tangent', { c: '#ea7a12', fs: 9 }) +
  Gm.line(...P(250).map((v, i) => i ? v + 25 : v - 10), ...P(-30).map((v, i) => i ? v - 10 : v + 30), '#2563eb') + Gm.t(196, 108, 'secant', { c: '#2563eb', fs: 9 }) +
  Gm.dot(cx, cy) + Gm.t(cx - 2, cy + 14, 'O', { fs: 10 }) + Gm.dot(cx + r, cy, '#ea7a12'), 2.9);
module.exports = {
  name: 'geometry-circles', course: 'Geometry', unitNo: 9, unitName: 'Circles',
  focus: 'parts of a circle, circumference, area, arcs and sectors',
  morefocus: 'inscribed angles, chords, tangents and angles inside and outside a circle',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['radius', 'Center to a point on the circle.', '⟨r⟩'], ['diameter', 'Chord through the center: ⟨d = 2r⟩.', '⟨d = 12⟩'],
      ['chord', 'Segment with both endpoints on the circle.', '⟨\\overline{AB}⟩'], ['tangent', 'Touches the circle at exactly one point.', '⟨\\perp⟩ radius'],
      ['secant', 'A line through two points of the circle.', ''], ['arc', 'Part of the circle between two points.', '⟨\\overset{\\frown}{AB}⟩']] },
    { title: 'Parts of a Circle', color: 'blue', kind: 'html', html: '', fig: parts, figFirst: true },
    { title: 'Circumference', color: 'green', kind: 'example', text: '⟨C = 2\\pi r = \\pi d⟩: the distance around.',
      example: 'Radius 5', steps: [['Formula:', '⟨C = 2\\pi(5) = 10\\pi⟩']], answer: '⟨10\\pi \\approx 31.4⟩ units', check: { num: 'Math.round(10*Math.PI*10)/10', is: 31.4 } },
    { title: 'Area', color: 'orange', kind: 'example', text: '⟨A = \\pi r^2⟩: the space inside.',
      example: 'Radius 6', steps: [['Formula:', '⟨A = \\pi(6)^2 = 36\\pi⟩']], answer: '⟨36\\pi \\approx 113.1⟩ units²', check: { num: 'Math.round(36*Math.PI*10)/10', is: 113.1 } },
    { title: 'Arc Length & Sector Area', color: 'pink', kind: 'table', head: ['Find', 'Formula', 'Example: ⟨60^\\circ⟩, ⟨r = 9⟩'], rows: [
      ['arc length', '⟨\\tfrac{\\theta}{360^\\circ} \\cdot 2\\pi r⟩', '⟨\\tfrac{1}{6}(18\\pi) = 3\\pi⟩'], ['sector area', '⟨\\tfrac{\\theta}{360^\\circ} \\cdot \\pi r^2⟩', '⟨\\tfrac{1}{6}(81\\pi) = 13.5\\pi⟩']],
      check: { list: ['60/360*18', '60/360*81'], is: [3, 13.5] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Radius is half the diameter.', 'Use degrees in the arc and sector fractions.', 'Leave answers in terms of ⟨\\pi⟩ unless told to round.'],
      bad: [['Using the diameter in ⟨\\pi r^2⟩', 'halve it first'], ['Circumference vs area', 'distance around vs space inside'], ['Arc measure vs arc length', 'degrees vs a length']] }
  ],
  back: [
    { title: 'Central & Inscribed Angles', color: 'purple', kind: 'table', plain: true, head: ['Angle', 'Measure'], rows: [
      ['central (vertex at center)', '= its arc'], ['inscribed (vertex on circle)', '⟨\\tfrac{1}{2}⟩ its arc'], ['inscribed in a semicircle', '⟨90^\\circ⟩'], ['tangent and chord', '⟨\\tfrac{1}{2}⟩ its arc']],
      after: 'Arc ⟨80^\\circ⟩: central ⟨80^\\circ⟩, inscribed ⟨40^\\circ⟩.', check: { num: '80/2', is: 40 } },
    { title: 'Chords', color: 'blue', kind: 'list', items: [
      'Congruent chords ⟨\\leftrightarrow⟩ congruent arcs.', 'A radius perpendicular to a chord bisects the chord and its arc.', 'Chords that cross inside: ⟨a \\cdot b = c \\cdot d⟩ (products of the pieces).'] },
    { title: 'Tangents', color: 'green', kind: 'list', items: [
      'A tangent is perpendicular to the radius at the point of tangency.', 'Two tangent segments from the same outside point are congruent: ⟨PA = PB⟩.', 'Use the Pythagorean Theorem with the radius, tangent and the segment to the center.'] },
    { title: 'Angles Inside the Circle', color: 'orange', kind: 'example', text: 'Two chords crossing: ⟨m\\angle = \\tfrac{1}{2}(\\text{arc}_1 + \\text{arc}_2)⟩.',
      example: 'Intercepted arcs ⟨80^\\circ⟩ and ⟨100^\\circ⟩', steps: [['Average:', '⟨\\tfrac{1}{2}(180^\\circ)⟩']], answer: '⟨90^\\circ⟩', check: { num: '(80+100)/2', is: 90 } },
    { title: 'Angles Outside the Circle', color: 'pink', kind: 'example', text: 'Secants or tangents meeting outside: ⟨m\\angle = \\tfrac{1}{2}(\\text{far arc} - \\text{near arc})⟩.',
      example: 'Arcs ⟨140^\\circ⟩ and ⟨60^\\circ⟩', steps: [['Half the difference:', '⟨\\tfrac{1}{2}(80^\\circ)⟩']], answer: '⟨40^\\circ⟩', check: { num: '(140-60)/2', is: 40 } },
    { title: 'Equation of a Circle', color: 'teal', kind: 'example', text: 'Center ⟨(h, k)⟩, radius ⟨r⟩: ⟨(x - h)^2 + (y - k)^2 = r^2⟩.',
      example: 'Center ⟨(2, -3)⟩, radius 4', steps: [['Substitute:', '⟨(x - 2)^2 + (y + 3)^2 = 16⟩']], answer: '⟨(x - 2)^2 + (y + 3)^2 = 16⟩', check: { num: '(6-2)**2+(-3+3)**2', is: 16 } }
  ]
};
