/* Unit pack builder: one content file -> online mystery, escape room, cheat sheet, thumbnails. (Printable whodunnits and
   stations come from the Printable Generator.) Every answer in the content is checked first; the build stops on any mismatch.
   Usage: node scripts/unit-packs/build.cjs <content-name>     (needs Playwright + Chromium for the PDFs)
   The mystery and escape room reuse the engines of the hand-made ones (templates below), so they look and play
   exactly like the existing games. */
'use strict';
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const katex = require(path.join(ROOT, 'worksheet-generator/vendor/katex/katex.min.js'));
const C = require('./' + process.argv[2] + '.cjs');
const T_MYSTERY = path.join(ROOT, 'artifacts/expressions-equations-golden-whisk-caper/index.html');
const T_ESCAPE = path.join(ROOT, 'artifacts/expressions-equations-escape-room/index.html');
const prefix = C.prefix || C.unit;   // file-name prefix (some unit ids are already used as prefixes by another unit's files)
/* Never overwrite another unit's files: every output folder must be unlisted in data.js or listed in this unit. */
{
  const lib = JSON.parse((s => s.slice(s.indexOf('{'), s.lastIndexOf('}') + 1))(fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8')));
  const owner = {};
  (function walk(o) { if (Array.isArray(o)) return o.forEach(walk); if (o && typeof o === 'object') { if (Array.isArray(o.units)) o.units.forEach(u => (u.artifacts || []).forEach(a => { owner[a.path.split('/').slice(0, 2).join('/')] = u.id; })); Object.values(o).forEach(walk); } })(lib);
  const mine = ['-escape-room', '-cheat-sheet', '-' + C.mystery.slug].map(x => 'artifacts/' + prefix + x);
  mine.forEach(d => { if (owner[d] && owner[d] !== C.unit) { console.error('CHECK FAILED: ' + d + ' belongs to unit ' + owner[d] + '. Set a different `prefix` in the content file.'); process.exit(1); } });
}

/* ---------------- checking ---------------- */
let checks = 0;
function fail(m) { console.error('CHECK FAILED: ' + m); process.exit(1); }
function num(e) { return Function('return (' + e + ')')(); }
function same(a, b) {   // expressions in x (and y) agree at several points
  const f = Function('x', 'y', 'return (' + a + ')'), g = Function('x', 'y', 'return (' + b + ')');
  return [[1.3, 0.7], [-2.1, 1.9], [0.4, -3.3], [5.2, 2.6]].every(p => Math.abs(f(p[0], p[1]) - g(p[0], p[1])) < 1e-9 * (1 + Math.abs(g(p[0], p[1]))));
}
function verify(c, where) {
  checks++;
  if (c.num !== undefined && Math.abs(num(c.num) - c.is) > 1e-9) fail(where + ': ' + c.num + ' = ' + num(c.num) + ', not ' + c.is);
  if (c.expr !== undefined && !same(c.expr, c.is)) fail(where + ': ' + c.expr + ' is not ' + c.is);
  if (c.list !== undefined) { const a = c.list.map(num).sort((p, q) => p - q), b = c.is.slice().sort((p, q) => p - q); if (a.length !== b.length || a.some((v, i) => Math.abs(v - b[i]) > 1e-9)) fail(where + ': list ' + a + ' is not ' + b); }
}
function listOf(t) { return texToJs(t).replace(/[{}\[\]]/g, '').split(',').filter(Boolean).map(num).sort((p, q) => p - q); }
/* TeX of a simple answer -> JS (for checking that wrong choices really are wrong) */
function texToJs(t) {
  return t.replace(/[⟨⟩]/g, '').replace(/\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}/g, '(($1)/($2))').replace(/\\times|\\cdot/g, '*').replace(/\\%|%/g, '').replace(/\^\{([^{}]*)\}/g, '**($1)').replace(/\\\{|\\\}/g, '').replace(/\\left|\\right|\\,/g, '').replace(/−/g, '-')
    .replace(/\|([^|]*)\|/g, 'Math.abs($1)').replace(/\^\{?(\d)\}?/g, '**$1').replace(/(\d|\))\s*([a-z(])/g, '$1*$2').replace(/\)\s*\(/g, ')*(').replace(/\s+/g, '');
}

/* ---------------- TeX helpers ---------------- */
function tex(s) { return katex.renderToString(s, { throwOnError: true }); }
function mt(s) { return String(s).split(/(⟨[^⟩]*⟩)/).map(p => /^⟨/.test(p) ? tex(p.slice(1, -1)) : p).join(''); }
/* TeX -> plain HTML for the game engines (which print unicode text, not TeX) */
function plainHtml(s) {   // ⟨TeX⟩ segments become unicode + <sup>/<sub>; text outside ⟨⟩ is left as written
  return String(s).split(/(⟨[^⟩]*⟩)/).map(p => /^⟨/.test(p) ? texPlain(p.slice(1, -1)) : p).join('');
}
function texPlain(t) {
  const SYM = { cdot: '·', times: '×', div: '÷', le: '≤', ge: '≥', leq: '≤', geq: '≥', ne: '≠', pm: '±', to: '→', dots: '…', ldots: '…', cdots: '⋯', Delta: 'Δ', pi: 'π', infty: '∞', approx: '≈', theta: 'θ', degree: '°', circ: '°', lt: '<', gt: '>' };
  const tok = x => /^[\w.]+$|^\(.*\)$/.test(x) ? x : '(' + x + ')';
  // placeholders: \x01 \x02 literal braces, \x04 thousands comma, \x10-\x13 sup/sub tags
  let r = t.replace(/\\left|\\right|\\displaystyle/g, '').replace(/\{,\}/g, '\x04').replace(/\\\{/g, '\x01').replace(/\\\}/g, '\x02').replace(/\\%/g, '%')
    .replace(/\\text\{([^{}]*)\}/g, '$1').replace(/\\(,|;|:|!| |quad|qquad)/g, ' ');
  for (let k = 0; k < 4; k++) r = r.replace(/\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}/g, (m, a, b) => tok(a) + '/' + tok(b)).replace(/\\sqrt\{([^{}]*)\}/g, (m, a) => '√' + tok(a));
  r = r.replace(/\\([A-Za-z]+) ?/g, (m, w) => SYM[w] !== undefined ? SYM[w] : w);
  r = r.replace(/\^\{([^{}]*)\}/g, '\x10$1\x11').replace(/\^(-?\d+|[A-Za-z])/g, '\x10$1\x11').replace(/_\{([^{}]*)\}/g, '\x12$1\x13').replace(/_(\w)/g, '\x12$1\x13');
  r = r.replace(/[{}]/g, '');
  // minus: binary after a number, letter, closing bracket or exponent (spaced); unary otherwise (tight)
  r = r.replace(/\s*-\s*/g, (m, off, all) => { const before = all.slice(0, off).replace(/\s+$/, ''), a = before.slice(-1); const openBar = a === '|' && (before.match(/\|/g) || []).length % 2 === 1; return a && !openBar && /[\w)\]\x02|πθ\x11\x13]/.test(a) ? ' − ' : (before && !openBar && !/[(\[\x01\x10\x12]/.test(a) ? ' −' : '−'); });
  r = r.replace(/\s*([=+<>≤≥≠≈→·×÷])\s*/g, ' $1 ').replace(/\s*,\s*/g, ', ').replace(/ {2,}/g, ' ').replace(/\( /g, '(').replace(/ \)/g, ')').replace(/\x10 /g, '\x10').replace(/ \x11/g, '\x11').trim();
  return r.replace(/\x01/g, '{').replace(/\x02/g, '}').replace(/\x04/g, ',').replace(/\x10/g, '<sup>').replace(/\x11/g, '</sup>').replace(/\x12/g, '<sub>').replace(/\x13/g, '</sub>');
}

/* ======================= 1. verify everything ======================= */
const M = C.mystery;
M.questions.forEach((q, i) => {
  verify(q.check, 'mystery #' + (i + 1));
  const right = q.check.list !== undefined || q.check.num !== undefined ? String(q.check.is) : q.check.is;
  // the typed answer the game accepts must be the checked answer
  { const a = q.answer, js = v => texToJs(String(v).replace(/×/g, '\\times ')); checks++;
    if (a.t === 'num' && Math.abs(num(js(a.v)) - q.check.is) > 1e-9) fail('mystery #' + (i + 1) + ': game answer ' + a.v + ' is not ' + q.check.is);
    if (a.t === 'nums' && JSON.stringify(a.v.map(v => num(js(v))).sort((x, y) => x - y)) !== JSON.stringify(q.check.is.slice().sort((x, y) => x - y))) fail('mystery #' + (i + 1) + ': game answers ' + a.v + ' are not ' + q.check.is);
    if (a.t === 'expr' && !same(js(a.v), q.check.is)) fail('mystery #' + (i + 1) + ': game answer ' + a.v + ' is not ' + q.check.is); }
  (q.wrong || []).forEach(w => {
    const js = texToJs(w[0]); checks++;
    const eq = q.check.list !== undefined ? JSON.stringify(listOf(w[0])) === JSON.stringify(q.check.is.slice().sort((p, r) => p - r)) : q.check.num !== undefined ? Math.abs(num(js) - q.check.is) < 1e-9 : same(js, right);
    if (eq) fail('mystery #' + (i + 1) + ': wrong choice ' + w[0] + ' equals the answer');
  });
});
C.escape.stages.forEach((s, i) => {
  (s.check || []).forEach((c, k) => verify({ num: c[0], is: c[1] }, 'escape room ' + (i + 1) + ' field ' + (k + 1)));
  (s.check || []).forEach((c, k) => { checks++; if (s.fields[k].answer !== c[1]) fail('escape room ' + (i + 1) + ': field answer ' + s.fields[k].answer + ' vs ' + c[1]); });
  if (s.checkNum) { verify({ num: s.checkNum[0], is: s.checkNum[1] }, 'escape cipher'); checks++; if (s.shift !== s.checkNum[1]) fail('cipher shift'); }
  if (s.checkExpr) verify({ expr: s.checkExpr[0], is: s.checkExpr[1] }, 'escape order');
});
{ const st = C.escape.stages.slice().sort((a, b) => a.stamp - b.stamp).map(s => s.letter).join(''); checks++; if (st !== C.escape.word) fail('escape word ' + st + ' vs ' + C.escape.word); }
(C.stations || []).forEach((s, i) => s.items.forEach((it, k) => { if (it[2]) verify(it[2], 'station ' + (i + 1) + ' #' + (k + 1)); }));

console.log('Content checks passed: ' + checks);

/* ======================= 2. online mystery ======================= */
function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
const R = rng(prefix.length * 7919 + 17);
const caseObj = {
  unit: prefix, eyebrow: M.eyebrow, title: M.title, tagline: M.tagline, palette: M.palette, labels: M.labels,
  placeholder: M.placeholder || 'Your answer', inputHint: M.inputHint || 'Type a number like -4, or an expression like 3x+5. Use ^ for exponents, like x^2.', symbols: M.symbols || ['^', '|'],
  intro: M.intro,
  rules: ['Solve each problem correctly to unlock a clue. A wrong answer just means try again; hints appear if you get stuck.',
    'Every clue rules out something on the case board: a suspect and the place they were seen, or a method.',
    'The thief acted alone in a spot nobody else was in, so anyone with an alibi is cleared, and so is the place they were seen.',
    'After all ' + M.questions.length + ' clues, exactly one suspect, one place and one method are left. Make your accusation!'],
  suspects: M.suspects.map((s, i) => Object.assign({ id: 's' + i }, s)),
  places: M.places.map((p, i) => ({ id: 'p' + i, name: p })), methods: M.methods.map((m, i) => ({ id: 'm' + i, name: m })),
  clues: M.questions.map(q => q.clue.p !== undefined ? { p: 's' + q.clue.p, l: 'p' + q.clue.l, text: q.clue.text } : { m: 'm' + q.clue.m, text: q.clue.text }),
  culprit: { p: 's' + M.culprit.p, l: 'p' + M.culprit.l, m: 'm' + M.culprit.m },
  accuseTemplate: 'Suspect: {p} · Place: {l} · Method: {m}', ending: M.ending,
  questions: M.questions.map((q, i) => ({ skill: 'Clue ' + (i + 1), instr: plainHtml(q.instr), html: '&nbsp;' + plainHtml(q.tex ? '⟨' + q.tex + '⟩' : q.text) + (q.html ? '<div style="margin-top:8px">' + q.html + '</div>' : ''),
    answer: q.answer, hint: 'Start here: ' + plainHtml(q.steps[0]), steps: q.steps.map((s, k) => k === q.steps.length - 1 ? '<b>' + plainHtml(s) + '</b>' : plainHtml(s)) }))
};
// every suspect/place except the culprit's is cleared exactly once, and every method except the culprit's
{
  const cp = new Set(), cl = new Set(), cm = new Set();
  caseObj.clues.forEach(c => { if (c.p) { cp.add(c.p); cl.add(c.l); } else cm.add(c.m); });
  checks++;
  if (cp.size !== 5 || cl.size !== 5 || cm.size !== 5 || cp.has(caseObj.culprit.p) || cl.has(caseObj.culprit.l) || cm.has(caseObj.culprit.m)) fail('mystery clues do not leave exactly the culprit');
}
const mysteryDir = path.join(ROOT, 'artifacts', prefix + '-' + M.slug);
fs.mkdirSync(mysteryDir, { recursive: true });
{
  let t = fs.readFileSync(T_MYSTERY, 'utf8');
  t = t.replace(/const CASE=\{.*?\};\n/s, () => 'const CASE=' + JSON.stringify(caseObj) + ';\n').replace(/<title>[^<]*<\/title>/, '<title>' + M.title + '</title>');
  // a set may be typed with braces, like {-1, 0, 2}
  const NUMS = 'function checkNums(raw,a){\n  let got;try{got=parseList(raw);}';
  if (!t.includes(NUMS)) throw new Error('mystery template: checkNums changed');
  t = t.replace(NUMS, 'function checkNums(raw,a){\n  let got;try{got=parseList(String(raw).replace(/[{}]/g,\'\'));}');
  // a number may be typed with thousands commas (40,000) or a percent sign (24%)
  const NUM = 'function checkNum(raw,a){\n  let s=nrm(raw)';
  if (!t.includes(NUM)) throw new Error('mystery template: checkNum changed');
  t = t.replace(NUM, 'function checkNum(raw,a){\n  let s=nrm(String(raw).replace(/(\\d),(?=\\d{3}(?!\\d))/g,\'$1\').replace(/\\s*%\\s*$/,\'\'))');
  fs.writeFileSync(path.join(mysteryDir, 'index.html'), t);
}

/* ======================= 3. escape room ======================= */
const E = C.escape, escDir = path.join(ROOT, 'artifacts', prefix + '-escape-room');
fs.mkdirSync(escDir, { recursive: true });
{
  const room = { id: prefix, title: E.title, emoji: E.emoji, endEmoji: E.endEmoji, intro: E.intro, finalStory: E.finalStory, finalAsk: E.finalAsk, word: E.word, outro: E.outro,
    stages: E.stages.map(s => { const o = Object.assign({}, s); delete o.check; delete o.checkNum; delete o.checkExpr; return o; }) };
  let t = fs.readFileSync(T_ESCAPE, 'utf8');
  const i = t.indexOf('const ROOM={'), j = t.indexOf('const TOTAL=');
  t = t.slice(0, i) + 'const ROOM=' + JSON.stringify(room) + ';\n\n' + t.slice(j);
  t = t.replace(/<title>[^<]*<\/title>/, '<title>' + E.title + '</title>');
  t = t.replace(/<header><h1>[^<]*<\/h1>/, '<header><h1>' + E.emoji + ' ' + E.title + '</h1>');
  if (/Rigged|Bake-Off/.test(t)) throw new Error('escape template text left over');
  fs.writeFileSync(path.join(escDir, 'index.html'), t);
}

/* ======================= 4. printables (HTML -> PDF) ======================= */
const KCSS = 'file://' + path.join(ROOT, 'worksheet-generator/vendor/katex/katex.min.css');
const FONT = '"DejaVu Sans",Verdana,Geneva,sans-serif';
function doc(css, body) {
  return '<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="' + KCSS + '"><style>@page{size:letter;margin:0}*{box-sizing:border-box}body{margin:0;font-family:' + FONT + ';color:#111}' +
    '.pg{width:8.5in;height:11in;padding:.5in .55in;position:relative;page-break-after:always;overflow:hidden}.pg:last-child{page-break-after:auto}.katex{font-size:1.05em}' + css + '</style></head><body>' + body + '</body></html>';
}
/* The printable whodunnit and stations are made by the Printable Generator (worksheet-generator/printables.html). */
/* ---- cheat sheet ---- */
const COL = { purple: ['#7b4fd0', '#f0e9ff'], blue: ['#2563eb', '#e6efff'], green: ['#16a34a', '#e6f8ec'], orange: ['#ea7a12', '#fff1e0'], pink: ['#db2777', '#fde8f1'], teal: ['#0d9488', '#e0f6f3'] };
const CCSS = '.pg{padding:.32in .35in}.ban{background:#ffd23f;border:3px solid #1f2a6b;border-radius:16px;text-align:center;padding:.06in;box-shadow:3px 3px 0 #1f2a6b}.ban b{font-family:"DejaVu Sans",sans-serif;font-size:21pt;white-space:nowrap;color:#1f2a6b;letter-spacing:-.01em}.ban b span{color:#2563eb}' +
  '.foc{text-align:center;font-size:10pt;margin:.08in 0 .1in;color:#1f2a6b}.foc b{color:#2563eb}.pg{display:flex;flex-direction:column}.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;align-content:stretch;gap:.12in}.sec{border:2.4px solid var(--c);border-radius:12px;background:var(--t);padding:0 0 .08in;overflow:hidden;font-size:9pt;line-height:1.42}' +
  '.sec h2{margin:0 0 .06in;background:var(--c);color:#fff;font-size:11.5pt;padding:.04in .1in;letter-spacing:.02em;text-transform:uppercase}.sec h2 i{display:inline-block;background:#fff;color:var(--c);border-radius:50%;width:.26in;height:.26in;text-align:center;font-style:normal;margin-right:6px;line-height:.26in}' +
  '.in{padding:0 .1in}.vt{width:100%;border-collapse:collapse;background:#fff}.vt td{border:1px solid #ddd;padding:3px 5px;vertical-align:top}.vt td:first-child{font-weight:700;color:var(--c);width:22%}' +
  '.ex{background:#fff;border:1.5px dashed var(--c);border-radius:8px;padding:.05in .08in;margin-top:.05in}.ex b.l{color:var(--c)}.ans{display:inline-block;border:2px solid var(--c);border-radius:8px;padding:1px 8px;font-weight:700;background:#fff;margin-top:3px}' +
  '.pem{display:grid;grid-template-columns:auto 1fr;gap:2px 8px;align-items:center}.pem b{display:inline-block;width:.24in;text-align:center;background:var(--c);color:#fff;border-radius:4px}' +
  '.sets{position:relative;height:1.55in;margin:.02in .1in}.sets div{position:absolute;border:2px solid var(--c);border-radius:12px;padding:2px 6px;background:rgba(255,255,255,.55);font-weight:700;font-size:8pt}' +
  '.ok{color:#15803d;font-weight:700}.no{color:#dc2626;font-weight:700}ul{margin:.02in 0;padding-left:.18in}li{margin:1px 0}.ft{text-align:center;font-size:8pt;margin-top:.08in;color:#555}';
function secHtml(s, n) {
  const c = COL[s.color]; let b = '';
  if (s.kind === 'vocab') b = '<table class="vt">' + s.rows.map(r => '<tr><td>' + r[0] + '</td><td>' + mt(r[1]) + '</td><td>' + mt(r[2]) + '</td></tr>').join('') + '</table>';
  else if (s.kind === 'pemdas') b = '<div class="pem">' + [['P', 'Parentheses', 'grouping first'], ['E', 'Exponents', 'powers'], ['M', 'Multiply', 'left to right,'], ['D', 'Divide', 'together'], ['A', 'Add', 'left to right,'], ['S', 'Subtract', 'together']].map(r => '<b>' + r[0] + '</b><span><b style="background:none;color:#111;width:auto">' + r[1] + '</b> — ' + r[2] + '</span>').join('') + '</div>' + exHtml(s);
  else if (s.kind === 'example') b = '<div>' + mt(s.text) + '</div>' + exHtml(s);
  else if (s.kind === 'sets') b = '<div class="sets"><div style="left:0;top:0;right:0;bottom:0">Real numbers</div><div style="left:.08in;top:.22in;width:62%;bottom:.08in">Rational ⟨\\tfrac{a}{b}⟩'.replace(/⟨([^⟩]*)⟩/g, (m, t) => tex(t)) + '</div><div style="left:.18in;top:.48in;width:44%;bottom:.14in">Integers …, −2, −1</div><div style="left:.28in;top:.74in;width:30%;bottom:.2in">Whole 0, 1, 2</div><div style="left:.38in;top:1.0in;width:17%;bottom:.26in;font-size:7pt">Natural 1, 2, 3</div><div style="right:.08in;top:.22in;width:30%;bottom:.08in">Irrational ' + tex('\\sqrt{2},\\ \\pi') + '</div></div><div class="in">Every rational number is a fraction ' + tex('\\tfrac{a}{b}') + ' (or a decimal that ends or repeats). Irrational decimals never end or repeat.</div>';
  else if (s.kind === 'props') b = '<table class="vt">' + s.rows.map(r => '<tr><td>' + r[0] + '<div style="font-weight:400;color:#555;font-size:7.5pt">' + r[1] + '</div></td><td>' + mt(r[2]) + '</td><td>' + mt(r[3]) + '</td></tr>').join('') + '</table>';
  else if (s.kind === 'mistakes') b = '<div class="ok">✔ Do remember</div><ul>' + s.good.map(x => '<li>' + mt(x) + '</li>').join('') + '</ul><div class="no">✘ Common mistakes</div><ul>' + s.bad.map(x => '<li>' + mt(x[0]) + ': ' + mt(x[1]) + '</li>').join('') + '</ul>';
  else if (s.kind === 'words') b = '<table class="vt">' + s.rows.map(r => '<tr><td style="width:65%;font-weight:400;color:#111">' + mt(r[0]) + '</td><td style="font-weight:700">' + mt(r[1]) + '</td></tr>').join('') + '</table>';
  else if (s.kind === 'table') b = '<table class="vt">' + (s.head ? '<tr>' + s.head.map(h => '<td style="font-weight:700;color:var(--c);background:var(--t)">' + mt(h) + '</td>').join('') + '</tr>' : '') + s.rows.map(r => '<tr>' + r.map(x => '<td>' + mt(x) + '</td>').join('') + '</tr>').join('') + '</table>' + (s.after ? '<div style="margin-top:4px">' + mt(s.after) + '</div>' : '');
  else if (s.kind === 'html') b = mt(s.html);
  else if (s.kind === 'list') b = '<ul>' + s.items.map(x => '<li>' + mt(x) + '</li>').join('') + '</ul>';
  return '<div class="sec" style="--c:' + c[0] + ';--t:' + c[1] + '"><h2><i>' + n + '</i>' + s.title + '</h2><div class="in">' + b + '</div></div>';
}
function exHtml(s) { return '<div class="ex"><b class="l">Example:</b> ' + mt(s.example) + '<br>' + s.steps.map(st => '<b class="l">' + mt(st[0]) + '</b> ' + mt(st[1])).join('<br>') + '<br><span class="ans">Answer: ' + mt(s.answer) + '</span></div>'; }
function cheatSheet() {
  const ch = C.cheat, title = '<b style="font-size:' + Math.min(21, 21 * 40 / ('Unit ' + C.unitNo + ' · ' + C.unitName + ' Cheat Sheet').length).toFixed(1) + 'pt">Unit ' + C.unitNo + ' · <span>' + C.unitName + '</span> Cheat Sheet</b>';
  return doc(CCSS, '<div class="pg"><div class="ban">' + title + '</div><div class="foc"><b>Unit ' + C.unitNo + ' focus:</b> ' + ch.focus + '</div><div class="grid">' + ch.front.map((s, i) => secHtml(s, i + 1)).join('') + '</div><div class="ft">Front · Mr. K’s Classroom</div></div>' +
    '<div class="pg"><div class="ban">' + title + '</div><div class="foc"><b>More practice:</b> ' + ch.morefocus + '</div><div class="grid">' + ch.back.map((s, i) => secHtml(s, i + 1)).join('') + '</div><div class="ft">Back · Mr. K’s Classroom</div></div>');
}

/* ======================= 5. render ======================= */
(async () => {
  const pw = require('playwright');
  const browser = await pw.chromium.launch();
  const page = await browser.newPage();
  const out = (rel, html) => ({ rel, html });
  const jobs = [
    out('artifacts/' + prefix + '-cheat-sheet/worksheet.pdf', cheatSheet())];
  const overflow = [];
  for (const j of jobs) {
    const f = path.join(ROOT, j.rel); fs.mkdirSync(path.dirname(f), { recursive: true });
    const tmp = path.join(path.dirname(f), '_tmp.html'); fs.writeFileSync(tmp, j.html);
    await page.goto('file://' + tmp); await page.evaluate(() => document.fonts.ready);
    const o = await page.evaluate(() => [...document.querySelectorAll('.pg')].map((p, i) => p.scrollHeight > p.clientHeight + 2 ? i + 1 : 0).filter(Boolean));
    if (o.length) overflow.push(j.rel + ' pages ' + o.join(','));
    await page.pdf({ path: f, format: 'Letter', printBackground: true, margin: { top: 0, bottom: 0, left: 0, right: 0 } });
    fs.unlinkSync(tmp);
    console.log('wrote ' + j.rel);
  }
  if (overflow.length) { console.error('OVERFLOW: ' + overflow.join('; ')); process.exitCode = 2; }
  // thumbnails (720 × 450): printables from the top of page 1, games from the start screen
  const shot = async (url, file, w, h) => { const p2 = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 720 / w }); await p2.goto(url); await p2.waitForTimeout(700); await p2.screenshot({ path: file, type: 'jpeg', quality: 85 }); await p2.close(); };
  const thumbs = path.join(ROOT, 'thumbs');
  for (const [name, url] of [[prefix + '-' + M.slug, 'file://' + path.join(mysteryDir, 'index.html')], [prefix + '-escape-room', 'file://' + path.join(escDir, 'index.html')]]) await shot(url, path.join(thumbs, name + '.jpg'), 1200, 750);
  for (const [name, html] of [[prefix + '-cheat-sheet', cheatSheet()]]) {
    const tmp = path.join(thumbs, '_t.html'); fs.writeFileSync(tmp, html);
    const p2 = await browser.newPage({ viewport: { width: 816, height: 510 }, deviceScaleFactor: 720 / 816 }); await p2.goto('file://' + tmp); await p2.waitForTimeout(400); await p2.screenshot({ path: path.join(thumbs, name + '.jpg'), type: 'jpeg', quality: 85 }); await p2.close(); fs.unlinkSync(tmp);
  }
  await browser.close();
  console.log('done');
})();
