const F = require('../figs.cjs');
const half = (cx, cy, a, b, sign) => x => { const t = 1 - ((x - cx) / a) ** 2; return t >= 0 ? cy + sign * b * Math.sqrt(t) : NaN; };
module.exports = {
  name: 'conic-sections', course: 'Algebra 2', unitNo: 9, unitName: 'Conic Sections',
  focus: 'circles, parabolas, ellipses and hyperbolas in standard form',
  morefocus: 'identifying conics, converting to standard form, focus and directrix, and applications',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['conic section', 'A curve made by slicing a double cone with a plane.', 'circle, ellipse'], ['focus', 'Fixed point(s) used to define the conic.', '⟨(0, 2)⟩'],
      ['directrix', 'Fixed line for a parabola: every point is as far from it as from the focus.', '⟨y = -2⟩'], ['vertices', 'Endpoints of the major axis (ellipse) or transverse axis (hyperbola).', '⟨(\\pm 5, 0)⟩'],
      ['asymptotes', 'Lines a hyperbola approaches.', '⟨y = \\pm\\tfrac{3}{4}x⟩']] },
    { title: 'Circles', color: 'blue', kind: 'example', text: '⟨(x - h)^2 + (y - k)^2 = r^2⟩: center ⟨(h, k)⟩, radius ⟨r⟩. Complete the square in ⟨x⟩ and ⟨y⟩.',
      example: '⟨x^2 + y^2 - 6x + 4y - 12 = 0⟩', steps: [['Complete:', '⟨(x - 3)^2 + (y + 2)^2 = 12 + 9 + 4⟩']], answer: 'center ⟨(3, -2)⟩, ⟨r = 5⟩',
      fig: F.plane({ id: 'cc', xmin: -3, xmax: 9, ymin: -8, ymax: 4, size: 1.0, ticks: 3, fns: [{ f: half(3, -2, 5, 5, 1) }, { f: half(3, -2, 5, 5, -1) }], points: [{ x: 3, y: -2, label: '(3, −2)' }] }),
      check: { expr: '(x-3)**2+(y+2)**2-25', is: 'x*x+y*y-6*x+4*y-12' } },
    { title: 'Parabolas', color: 'green', kind: 'example', text: '⟨(x - h)^2 = 4p(y - k)⟩: vertex ⟨(h, k)⟩, focus ⟨(h, k + p)⟩, directrix ⟨y = k - p⟩. Opens up if ⟨p > 0⟩. ⟨(y - k)^2 = 4p(x - h)⟩ opens sideways.',
      example: '⟨y = \\tfrac{1}{8}x^2⟩', steps: [['Rewrite:', '⟨x^2 = 8y⟩, so ⟨4p = 8⟩, ⟨p = 2⟩']], answer: 'focus ⟨(0, 2)⟩, directrix ⟨y = -2⟩',
      fig: F.plane({ id: 'cp', xmin: -6, xmax: 6, ymin: -3, ymax: 5, size: 1.15, ticks: 2, fns: [{ f: x => x * x / 8 }, { f: x => -2, color: '#db2777', dashed: true }], points: [{ x: 0, y: 2, label: 'F', color: '#16a34a' }] }),
      check: { num: '4*4/8', is: 2 } },
    { title: 'Ellipses', color: 'orange', kind: 'example', text: '⟨\\dfrac{(x - h)^2}{a^2} + \\dfrac{(y - k)^2}{b^2} = 1⟩, ⟨a > b⟩: horizontal major axis. Foci: ⟨c^2 = a^2 - b^2⟩.',
      example: '⟨\\dfrac{x^2}{25} + \\dfrac{y^2}{9} = 1⟩', steps: [['Axes:', 'vertices ⟨(\\pm 5, 0)⟩, co-vertices ⟨(0, \\pm 3)⟩'], ['Foci:', '⟨c^2 = 25 - 9 = 16⟩']], answer: 'foci ⟨(\\pm 4, 0)⟩',
      fig: F.plane({ id: 'ce', xmin: -6, xmax: 6, ymin: -4, ymax: 4, size: 1.3, ticks: 2, fns: [{ f: half(0, 0, 5, 3, 1) }, { f: half(0, 0, 5, 3, -1) }], points: [{ x: -4, y: 0, color: '#ea7a12' }, { x: 4, y: 0, color: '#ea7a12' }] }),
      check: { num: 'Math.sqrt(25-9)', is: 4 } },
    { title: 'Hyperbolas', color: 'pink', kind: 'example', text: '⟨\\dfrac{x^2}{a^2} - \\dfrac{y^2}{b^2} = 1⟩ opens left–right. Foci: ⟨c^2 = a^2 + b^2⟩. Asymptotes ⟨y = \\pm\\tfrac{b}{a}x⟩.',
      example: '⟨\\dfrac{x^2}{16} - \\dfrac{y^2}{9} = 1⟩', steps: [['Vertices:', '⟨(\\pm 4, 0)⟩; ⟨c^2 = 25⟩, foci ⟨(\\pm 5, 0)⟩']], answer: 'asymptotes ⟨y = \\pm\\tfrac{3}{4}x⟩',
      fig: F.plane({ id: 'ch', xmin: -8, xmax: 8, ymin: -6, ymax: 6, size: 1.15, ticks: 4, fns: [{ f: x => 3 * Math.sqrt(x * x / 16 - 1), from: 4, to: 8 }, { f: x => -3 * Math.sqrt(x * x / 16 - 1), from: 4, to: 8 }, { f: x => 3 * Math.sqrt(x * x / 16 - 1), from: -8, to: -4 }, { f: x => -3 * Math.sqrt(x * x / 16 - 1), from: -8, to: -4 }, { f: x => 0.75 * x, color: '#999', dashed: true }, { f: x => -0.75 * x, color: '#999', dashed: true }] }),
      check: { num: 'Math.sqrt(16+9)', is: 5 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Ellipse: ⟨a^2⟩ is the larger denominator; hyperbola: ⟨a^2⟩ is under the positive term.', 'Ellipse ⟨c^2 = a^2 - b^2⟩; hyperbola ⟨c^2 = a^2 + b^2⟩.', 'Add the same amounts to both sides when completing the square.'],
      bad: [['⟨(x + 3)^2 + y^2 = 16⟩: center ⟨(3, 0)⟩', 'it is ⟨(-3, 0)⟩, ⟨r = 4⟩'], ['⟨r = 16⟩ for ⟨x^2 + y^2 = 16⟩', '⟨r = 4⟩'], ['⟨c = a + b⟩', 'use squares: ⟨c^2 = a^2 \\pm b^2⟩']] }
  ],
  back: [
    { title: 'Identify the Conic', color: 'purple', kind: 'table', head: ['⟨Ax^2 + Cy^2 + Dx + Ey + F = 0⟩', 'Conic', 'Example'], rows: [
      ['⟨A = C⟩', 'circle', '⟨2x^2 + 2y^2 - 8 = 0⟩'], ['⟨AC > 0⟩, ⟨A \\ne C⟩', 'ellipse', '⟨4x^2 + 9y^2 = 36⟩'], ['⟨AC < 0⟩', 'hyperbola', '⟨x^2 - 4y^2 = 4⟩'], ['⟨A = 0⟩ or ⟨C = 0⟩', 'parabola', '⟨y^2 - 8x = 0⟩']] },
    { title: 'Converting to Standard Form', color: 'blue', kind: 'example', text: 'Group, factor out the squared coefficients, complete each square, divide to get 1.',
      example: '⟨4x^2 + 9y^2 - 16x + 18y - 11 = 0⟩', steps: [['Complete:', '⟨4(x - 2)^2 + 9(y + 1)^2 = 11 + 16 + 9 = 36⟩'], ['Divide by 36:', 'center ⟨(2, -1)⟩, ⟨a = 3⟩, ⟨b = 2⟩']], answer: '⟨\\dfrac{(x - 2)^2}{9} + \\dfrac{(y + 1)^2}{4} = 1⟩',
      check: { expr: '4*(x-2)**2+9*(y+1)**2-36', is: '4*x*x+9*y*y-16*x+18*y-11' } },
    { title: 'Focus & Directrix', color: 'green', kind: 'example', text: 'The vertex is halfway between the focus and the directrix; ⟨p⟩ is that distance.',
      example: 'Focus ⟨(2, 3)⟩, directrix ⟨y = -1⟩', steps: [['Vertex:', '⟨(2, 1)⟩, ⟨p = 2⟩'], ['Check ⟨(6, 3)⟩:', '4 from the focus, 4 from the directrix']], answer: '⟨(x - 2)^2 = 8(y - 1)⟩',
      check: [{ num: '(6-2)**2/8+1', is: 3 }, { num: 'Math.hypot(6-2,3-3)', is: 4 }] },
    { title: 'Vertical Orientation', color: 'orange', kind: 'words', rows: [
      ['⟨\\dfrac{x^2}{4} + \\dfrac{y^2}{25} = 1⟩', 'ellipse, vertices ⟨(0, \\pm 5)⟩, foci ⟨(0, \\pm\\sqrt{21})⟩'], ['⟨\\dfrac{y^2}{9} - \\dfrac{x^2}{16} = 1⟩', 'hyperbola opening up/down, vertices ⟨(0, \\pm 3)⟩'], ['⟨y^2 = -12x⟩', 'parabola opening left, focus ⟨(-3, 0)⟩']],
      check: { list: ['25-4', '-12/4'], is: [21, -3] } },
    { title: 'Graphing Checklist', color: 'pink', kind: 'list', items: ['<b>Circle:</b> center, then ⟨r⟩ up, down, left, right.', '<b>Parabola:</b> vertex, focus, directrix, and the two points ⟨2|p|⟩ either side of the focus.', '<b>Ellipse:</b> center, ⟨a⟩ along the major axis, ⟨b⟩ along the minor axis.', '<b>Hyperbola:</b> center, vertices, the ⟨2a \\times 2b⟩ box, asymptotes through its corners.'] },
    { title: 'Application: Satellite Dish', color: 'teal', kind: 'example', text: 'A parabolic dish reflects signals to its focus. Put the vertex at the origin: ⟨x^2 = 4py⟩.',
      example: 'A dish is 8 ft wide and 2 ft deep. Where is the receiver?', steps: [['Point ⟨(4, 2)⟩:', '⟨16 = 4p(2)⟩'], ['Solve:', '⟨p = 2⟩']], answer: '2 ft above the vertex',
      check: { num: '16/(4*2)', is: 2 } }
  ]
};
