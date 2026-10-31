const F = require('../figs.cjs');
module.exports = {
  name: 'trigonometric-functions', course: 'Algebra 2', unitNo: 10, unitName: 'Trigonometric Functions',
  focus: 'radians, the unit circle, reference angles and trig values of any angle',
  morefocus: 'sine and cosine graphs, amplitude, period, phase shift, identities, equations, inverses and modeling',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['radian', 'Angle whose arc equals the radius. ⟨2\\pi⟩ rad = 360°.', '⟨\\pi = 180^\\circ⟩'], ['coterminal', 'Same terminal side; differ by ⟨360^\\circ⟩ (⟨2\\pi⟩).', '⟨30^\\circ, 390^\\circ⟩'],
      ['reference angle', 'Acute angle to the x-axis.', '⟨150^\\circ \\to 30^\\circ⟩'], ['unit circle', 'Radius 1: the point is ⟨(\\cos\\theta, \\sin\\theta)⟩.', '⟨(0, 1)⟩ at ⟨90^\\circ⟩'],
      ['amplitude / period', 'Half the height / length of one cycle.', '⟨3⟩ / ⟨\\pi⟩']] },
    { title: 'Degrees ↔ Radians', color: 'blue', kind: 'words', rows: [
      ['Degrees to radians: × ⟨\\tfrac{\\pi}{180}⟩. ⟨150^\\circ⟩', '⟨\\tfrac{5\\pi}{6}⟩'], ['Radians to degrees: × ⟨\\tfrac{180}{\\pi}⟩. ⟨\\tfrac{7\\pi}{4}⟩', '⟨315^\\circ⟩'],
      ['Coterminal with ⟨-\\tfrac{\\pi}{3}⟩ in ⟨[0, 2\\pi)⟩', '⟨\\tfrac{5\\pi}{3}⟩'], ['Arc length ⟨s = r\\theta⟩: ⟨r = 6⟩, ⟨\\theta = \\tfrac{2\\pi}{3}⟩', '⟨4\\pi⟩']],
      check: { list: ['150/180', '7/4*180', '2-1/3', '6*2/3'], is: [5 / 6, 315, 5 / 3, 4] } },
    { title: 'Unit Circle (Quadrant I)', color: 'green', kind: 'table', head: ['⟨\\theta⟩', '⟨0⟩', '⟨\\tfrac{\\pi}{6}⟩', '⟨\\tfrac{\\pi}{4}⟩', '⟨\\tfrac{\\pi}{3}⟩', '⟨\\tfrac{\\pi}{2}⟩'], rows: [
      ['⟨\\cos⟩', '⟨1⟩', '⟨\\tfrac{\\sqrt{3}}{2}⟩', '⟨\\tfrac{\\sqrt{2}}{2}⟩', '⟨\\tfrac{1}{2}⟩', '⟨0⟩'], ['⟨\\sin⟩', '⟨0⟩', '⟨\\tfrac{1}{2}⟩', '⟨\\tfrac{\\sqrt{2}}{2}⟩', '⟨\\tfrac{\\sqrt{3}}{2}⟩', '⟨1⟩'], ['⟨\\tan⟩', '⟨0⟩', '⟨\\tfrac{\\sqrt{3}}{3}⟩', '⟨1⟩', '⟨\\sqrt{3}⟩', 'undef.']],
      after: 'Signs: All positive in QI, <b>S</b>ine in QII, <b>T</b>angent in QIII, <b>C</b>osine in QIV.',
      check: { list: ['Math.cos(Math.PI/6)', 'Math.sin(Math.PI/6)', 'Math.tan(Math.PI/3)'], is: [Math.sqrt(3) / 2, 0.5, Math.sqrt(3)] } },
    { title: 'Any Angle: Reference Angles', color: 'orange', kind: 'words', rows: [
      ['⟨\\sin 210^\\circ⟩: ref ⟨30^\\circ⟩, QIII (sin < 0)', '⟨-\\tfrac{1}{2}⟩'], ['⟨\\cos \\tfrac{3\\pi}{4}⟩: ref ⟨\\tfrac{\\pi}{4}⟩, QII (cos < 0)', '⟨-\\tfrac{\\sqrt{2}}{2}⟩'], ['⟨\\tan \\tfrac{5\\pi}{3}⟩: ref ⟨\\tfrac{\\pi}{3}⟩, QIV (tan < 0)', '⟨-\\sqrt{3}⟩']],
      check: { list: ['Math.sin(210*Math.PI/180)', 'Math.cos(3*Math.PI/4)', 'Math.tan(5*Math.PI/3)'], is: [-0.5, -Math.SQRT2 / 2, -Math.sqrt(3)] } },
    { title: 'Point on the Terminal Side', color: 'pink', kind: 'example', text: 'For ⟨(x, y)⟩: ⟨r = \\sqrt{x^2 + y^2}⟩, ⟨\\sin\\theta = \\tfrac{y}{r}⟩, ⟨\\cos\\theta = \\tfrac{x}{r}⟩, ⟨\\tan\\theta = \\tfrac{y}{x}⟩.',
      example: 'The terminal side passes through ⟨(-3, 4)⟩.', steps: [['⟨r⟩:', '⟨\\sqrt{9 + 16} = 5⟩']], answer: '⟨\\sin\\theta = \\tfrac{4}{5}⟩, ⟨\\cos\\theta = -\\tfrac{3}{5}⟩, ⟨\\tan\\theta = -\\tfrac{4}{3}⟩',
      check: { num: 'Math.hypot(-3,4)', is: 5 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Set the calculator to the right mode (degrees or radians).', 'Reference angles are always measured to the x-axis.', '⟨\\sin^2\\theta⟩ means ⟨(\\sin\\theta)^2⟩.'],
      bad: [['⟨\\sin^{-1} x = \\tfrac{1}{\\sin x}⟩', 'it is the inverse (arcsin), not the reciprocal'], ['⟨\\sin 2x = 2\\sin x⟩', 'not true in general'], ['Period of ⟨\\sin 2x⟩ is ⟨4\\pi⟩', 'it is ⟨\\tfrac{2\\pi}{2} = \\pi⟩']] }
  ],
  back: [
    { title: 'Graphs of Sine & Cosine', color: 'purple', kind: 'html', html: 'Both have amplitude 1 and period ⟨2\\pi⟩. ⟨\\sin⟩ starts at 0 going up; ⟨\\cos⟩ starts at its maximum. Range ⟨[-1, 1]⟩.',
      fig: F.plane({ id: 'tg', xmin: 0, xmax: 6.4, ymin: -1.5, ymax: 1.5, size: 2.8, fns: [{ f: x => Math.sin(x), color: '#2563eb' }, { f: x => Math.cos(x), color: '#db2777' }], labels: [{ x: 2.3, y: 1.3, t: 'sin x', color: '#2563eb' }, { x: 5.5, y: 1.3, t: 'cos x', color: '#db2777' }, { x: 3.14, y: -0.3, t: 'π', bold: false }, { x: 6.1, y: -0.3, t: '2π', bold: false }] }) },
    { title: 'Amplitude, Period, Shifts', color: 'blue', kind: 'example', text: '⟨y = a\\sin\\big(b(x - h)\\big) + k⟩: amplitude ⟨|a|⟩, period ⟨\\tfrac{2\\pi}{b}⟩, phase shift ⟨h⟩, midline ⟨y = k⟩.',
      example: '⟨y = 3\\sin\\big(2(x - \\tfrac{\\pi}{4})\\big) + 1⟩', steps: [['Read:', 'amplitude 3, period ⟨\\pi⟩, right ⟨\\tfrac{\\pi}{4}⟩, midline ⟨y = 1⟩']], answer: 'max ⟨4⟩, min ⟨-2⟩',
      check: { list: ['2*Math.PI/2', '3+1', '-3+1'], is: [Math.PI, 4, -2] } },
    { title: 'Identities', color: 'green', kind: 'example', text: '⟨\\sin^2\\theta + \\cos^2\\theta = 1⟩ and ⟨\\tan\\theta = \\tfrac{\\sin\\theta}{\\cos\\theta}⟩. Use the quadrant for the sign.',
      example: '⟨\\sin\\theta = \\tfrac{3}{5}⟩, ⟨\\theta⟩ in QII', steps: [['⟨\\cos^2\\theta⟩:', '⟨1 - \\tfrac{9}{25} = \\tfrac{16}{25}⟩, cos < 0 in QII']], answer: '⟨\\cos\\theta = -\\tfrac{4}{5}⟩, ⟨\\tan\\theta = -\\tfrac{3}{4}⟩',
      check: { num: '(3/5)**2+(4/5)**2', is: 1 } },
    { title: 'Solving Trig Equations', color: 'orange', kind: 'words', rows: [
      ['⟨2\\sin x - 1 = 0⟩ on ⟨[0, 2\\pi)⟩', '⟨x = \\tfrac{\\pi}{6},\\ \\tfrac{5\\pi}{6}⟩'], ['⟨2\\cos^2 x - \\cos x - 1 = 0⟩: ⟨(2\\cos x + 1)(\\cos x - 1) = 0⟩', '⟨x = 0,\\ \\tfrac{2\\pi}{3},\\ \\tfrac{4\\pi}{3}⟩'], ['All solutions of ⟨\\tan x = 1⟩', '⟨x = \\tfrac{\\pi}{4} + n\\pi⟩']],
      check: { list: ['Math.round((2*Math.sin(5*Math.PI/6)-1)*1e9)', 'Math.round((2*Math.cos(2*Math.PI/3)**2-Math.cos(2*Math.PI/3)-1)*1e9)', 'Math.round((2*Math.cos(4*Math.PI/3)**2-Math.cos(4*Math.PI/3)-1)*1e9)'], is: [0, 0, 0] } },
    { title: 'Inverse Trig Functions', color: 'pink', kind: 'table', head: ['Function', 'Range', 'Example'], rows: [
      ['⟨\\sin^{-1} x⟩', '⟨[-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2}]⟩', '⟨\\sin^{-1}\\tfrac{1}{2} = \\tfrac{\\pi}{6}⟩'], ['⟨\\cos^{-1} x⟩', '⟨[0, \\pi]⟩', '⟨\\cos^{-1}(-\\tfrac{1}{2}) = \\tfrac{2\\pi}{3}⟩'], ['⟨\\tan^{-1} x⟩', '⟨(-\\tfrac{\\pi}{2}, \\tfrac{\\pi}{2})⟩', '⟨\\tan^{-1}(-1) = -\\tfrac{\\pi}{4}⟩']],
      check: { list: ['Math.asin(0.5)', 'Math.acos(-0.5)', 'Math.atan(-1)'], is: [Math.PI / 6, 2 * Math.PI / 3, -Math.PI / 4] } },
    { title: 'Modeling: Ferris Wheel', color: 'teal', kind: 'example', text: 'Midline = center height, amplitude = radius, period = time for one turn. Starting at the bottom: use ⟨-\\cos⟩.',
      example: 'Diameter 50 m, center 30 m high, one turn every 10 min, start at the bottom.', steps: [['Model:', '⟨h(t) = -25\\cos\\big(\\tfrac{\\pi}{5}t\\big) + 30⟩'], ['Check:', '⟨h(0) = 5⟩, ⟨h(5) = 55⟩']], answer: '⟨h(2.5) = 30⟩ m (level with the center)',
      check: { list: ['-25*Math.cos(0)+30', '-25*Math.cos(Math.PI)+30', 'Math.round(-25*Math.cos(Math.PI/2)+30)'], is: [5, 55, 30] } }
  ]
};
