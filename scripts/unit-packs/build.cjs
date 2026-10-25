/* Unit pack builder: one content file -> online mystery, printable whodunnit (+ key), escape room, stations (+ key),
   cheat sheet, thumbnails. Every answer in the content is checked first; the build stops on any mismatch.
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
const prefix = C.unit;

/* ---------------- checking ---------------- */
let checks = 0;
function fail(m) { console.error('CHECK FAILED: ' + m); process.exit(1); }
function num(e) { return Function('return (' + e + ')')(); }
function same(a, b) {   // expressions in x (and y) agree at several points
  const f = Function('x', 'y', 'return (' + a + ')'), g = Function('x', 'y', 'return (' + b + ')');
  return [[1.3, 0.7], [-2.1, 1.9], [0.4, -3.3], [5.2, 2.6]].every(p => Math.abs(f(p[0], p[1]) - g(p[0], p[1])) < 1e-9);
}
function verify(c, where) {
  checks++;
  if (c.num !== undefined && Math.abs(num(c.num) - c.is) > 1e-9) fail(where + ': ' + c.num + ' = ' + num(c.num) + ', not ' + c.is);
  if (c.expr !== undefined && !same(c.expr, c.is)) fail(where + ': ' + c.expr + ' is not ' + c.is);
}
/* TeX of a simple answer -> JS (for checking that wrong choices really are wrong) */
function texToJs(t) {
  return t.replace(/[⟨⟩]/g, '').replace(/\\tfrac\{([^{}]*)\}\{([^{}]*)\}/g, '(($1)/($2))').replace(/\\left|\\right|\\,/g, '').replace(/−/g, '-')
    .replace(/\|([^|]*)\|/g, 'Math.abs($1)').replace(/\^\{?(\d)\}?/g, '**$1').replace(/(\d|\))\s*([a-z(])/g, '$1*$2').replace(/\)\s*\(/g, ')*(').replace(/\s+/g, '');
}

/* ---------------- TeX helpers ---------------- */
function tex(s) { return katex.renderToString(s, { throwOnError: true }); }
function mt(s) { return String(s).split(/(⟨[^⟩]*⟩)/).map(p => /^⟨/.test(p) ? tex(p.slice(1, -1)) : p).join(''); }
/* TeX -> plain HTML for the game engines (which print unicode text, not TeX) */
function plainHtml(s) {
  return String(s).replace(/[⟨⟩]/g, '').replace(/\\dfrac\{([^{}]*)\}\{([^{}]*)\}|\\tfrac\{([^{}]*)\}\{([^{}]*)\}/g, (m, a, b, c2, d) => '(' + (a || c2) + ')/(' + (b || d) + ')')
    .replace(/\^2/g, '²').replace(/\^3/g, '³').replace(/\\cdot/g, '·').replace(/\\times/g, '×').replace(/\\div/g, '÷').replace(/\\to/g, '→')
    .replace(/\\ /g, ' ').replace(/\\,/g, '').replace(/-/g, '−').replace(/\s*=\s*/g, ' = ').replace(/\s*\+\s*/g, ' + ').replace(/(\S)\s*−\s*(\S)/g, '$1 − $2');
}

/* ======================= 1. verify everything ======================= */
const M = C.mystery;
M.questions.forEach((q, i) => {
  verify(q.check, 'mystery #' + (i + 1));
  const right = q.check.num !== undefined ? String(q.check.is) : q.check.is;
  q.wrong.forEach(w => {
    const js = texToJs(w[0]); checks++;
    const eq = q.check.num !== undefined ? Math.abs(num(js) - q.check.is) < 1e-9 : same(js, right);
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
C.stations.forEach((s, i) => s.items.forEach((it, k) => { if (it[2]) verify(it[2], 'station ' + (i + 1) + ' #' + (k + 1)); }));
if (M.falseClues.length < 30) fail('need 30 false clues');
console.log('Content checks passed: ' + checks);

/* ======================= 2. online mystery ======================= */
function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
const R = rng(prefix.length * 7919 + 17);
const caseObj = {
  unit: prefix, eyebrow: M.eyebrow, title: M.title, tagline: M.tagline, palette: M.palette, labels: M.labels,
  placeholder: 'Your answer', inputHint: 'Type a number like -4, or an expression like 3x+5. Use ^ for exponents, like x^2.', symbols: ['^', '|'],
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
  questions: M.questions.map((q, i) => ({ skill: 'Clue ' + (i + 1), instr: q.instr, html: '&nbsp;' + plainHtml(q.tex ? '⟨' + q.tex + '⟩' : q.text),
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
const LET = 'ABCD';
/* ---- whodunnit printable ---- */
const cards = M.questions.map((q, i) => {
  const pos = Math.floor(R() * 4), opts = [], fl = M.falseClues.slice(i * 3, i * 3 + 3);
  let w = 0;
  for (let k = 0; k < 4; k++) opts.push(k === pos ? { a: answerTex(q), clue: q.clue.text, ok: true } : { a: q.wrong[w][0], why: q.wrong[w][1], clue: fl[w++], ok: false });
  return { q: q, opts: opts, pos: pos };
});
function answerTex(q) { return q.answer.t === 'num' ? '⟨' + q.check.is + '⟩' : '⟨' + q.steps[q.steps.length - 1].replace(/^[^⟨]*⟨|⟩.*$/g, '') + '⟩'; }
function plainTexOf(q) { return answerTex(q); }
function problemHtml(q) { return '<div class="ci">' + mt(q.instr) + '</div><div class="cm">' + (q.tex ? tex(q.tex) : mt(q.text)) + '</div>'; }
const WCSS = '.mono{font-family:"Courier New",ui-monospace,monospace;font-weight:700}.ttl{font-size:21pt}.sub{font-size:9pt;color:#555}.rule{border-bottom:2px solid #000;margin:.05in 0 .12in}' +
  '.row{display:flex;justify-content:space-between;align-items:flex-end}.ln{display:inline-block;border-bottom:1.2px solid #000;width:2in}p{font-size:9.6pt;line-height:1.45;margin:.06in 0}' +
  '.box{border:1.6px solid #000;border-radius:7px;padding:.08in .14in;font-size:9pt;margin:.1in 0}.box h3{margin:0 0 4px;font-size:10pt}.box ol{margin:0;padding-left:.2in;line-height:1.45}' +
  '.board{display:grid;grid-template-columns:repeat(3,1fr);gap:.18in;margin-top:.12in}.board h4{font-family:"Courier New",monospace;font-size:10pt;margin:0 0 4px;border-bottom:1.5px solid #000;padding-bottom:3px}' +
  '.bi{display:flex;gap:7px;align-items:flex-start;border-bottom:1px solid #ccc;padding:6px 0;font-size:8.6pt;min-height:.38in}.bi i{display:inline-block;width:.17in;height:.17in;border:1.4px solid #000;flex:none}.bi small{display:block;color:#666;font-size:7pt}' +
  '.culprit{border:1.8px solid #000;border-radius:8px;padding:.1in .14in;font-weight:700;font-size:10pt;margin-top:.15in}.culprit .ln{width:1.5in}' +
  '.wgrid{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(5,1.83in);border:2px solid #000;margin-top:.08in}.wgrid>div{border:1px solid #000;padding:.05in .08in;font-size:9pt;font-weight:700;position:relative}.wgrid small{position:absolute;left:.08in;bottom:.05in;font-weight:400}' +
  '.card{height:4.85in;position:relative}.card+.card{border-top:1.2px dashed #888;margin-top:.12in;padding-top:.2in}.card .cut{position:absolute;top:-.08in;left:50%;transform:translateX(-50%);background:#fff;font-size:7pt;color:#888;padding:0 6px}' +
  '.ch{display:flex;justify-content:space-between;align-items:baseline}.ch .mono{font-size:22pt}.ch span{font-family:"Courier New",monospace;font-size:9pt}.ci{text-align:center;font-size:10pt;margin-top:.08in}.cm{text-align:center;font-size:15pt;margin:.06in 0 .14in}' +
  '.opts{width:100%;border-collapse:collapse;border:2px solid #000}.opts td{border:1px solid #000;padding:.08in .1in;font-size:9pt;vertical-align:middle;height:.58in}.opts td:first-child{width:2in;font-size:10.5pt}.opts b{font-family:"Courier New",monospace}' +
  '.cf{text-align:center;font-size:6.8pt;color:#777;margin-top:4px}table.k{width:100%;border-collapse:collapse;font-size:8.6pt}table.k th,table.k td{border:1px solid #999;padding:4px 6px;text-align:left;vertical-align:top}table.k th{background:#eee}' +
  '.sol{border:2.4px solid #000;padding:.1in;text-align:center;font-weight:700;font-size:13pt;margin:.12in 0}.g{color:#13795b;font-weight:700}';
function whodunnitStudent() {
  let h = '<div class="pg"><div class="row"><div><div class="mono ttl">' + M.title + '</div><div class="sub">Whodunnit? · ' + C.unitName + '</div></div><div>Name: <span class="ln"></span></div></div><div class="rule"></div>' +
    M.intro.map(p => '<p>' + p + '</p>').join('') +
    '<div class="box"><h3>How to crack the case</h3><ol><li>Your teacher will post <b>' + M.questions.length + ' clue cards</b> around the room. Each card has a math problem and four answer choices. Every choice is paired with a clue.</li><li>Solve the problem on the <b>Show Your Work</b> page. Find your answer among the choices and read the clue next to it. If your answer is not there, check your work.</li><li>Use the clue to cross out suspects, places or methods on the case board below. Write the card number beside what it cleared.</li><li>After all ' + M.questions.length + ' cards, exactly one suspect, one place and one method are left. Those three boxes name the culprit. If you end up with none, or more than one, a clue went wrong: recheck your math!</li></ol></div>' +
    '<div class="board"><div><h4>' + M.labels.p + '</h4>' + M.suspects.map(s => '<div class="bi"><i></i><span>' + s.name + '<small>' + s.role + '</small></span></div>').join('') + '</div><div><h4>' + M.labels.l + '</h4>' + M.places.map(p => '<div class="bi"><i></i><span>' + p + '</span></div>').join('') + '</div><div><h4>' + M.labels.m + '</h4>' + M.methods.map(m => '<div class="bi"><i></i><span>' + m + '</span></div>').join('') + '</div></div>' +
    '<div class="culprit">The culprit is <span class="ln"></span> in <span class="ln"></span> using <span class="ln"></span></div></div>';
  h += '<div class="pg"><div class="row"><div><div class="mono ttl">Show Your Work</div><div class="sub">' + M.title + ' · Show every step in the matching box.</div></div><div>Name: <span class="ln"></span></div></div><div class="rule"></div><div class="wgrid">' +
    M.questions.map((_, i) => '<div>' + (i + 1) + '.<small>Choice ______</small></div>').join('') + '</div></div>';
  for (let i = 0; i < cards.length; i += 2) {
    h += '<div class="pg">' + cards.slice(i, i + 2).map((c, k) => '<div class="card">' + (k ? '<span class="cut">✂ cut here</span>' : '') + '<div class="ch"><span class="mono">Clue #' + (i + k + 1) + '</span><span>' + M.title + '</span></div>' + problemHtml(c.q) +
      '<table class="opts">' + c.opts.map((o, j) => '<tr><td><b>' + LET[j] + '.</b> ' + mt(o.a) + '</td><td>' + o.clue + '</td></tr>').join('') + '</table><div class="cf">Solve the problem, find your answer, and read its clue. Cross it off on your case board.</div></div>').join('') + '</div>';
  }
  return doc(WCSS, h);
}
function whodunnitKey() {
  const cul = M.suspects[M.culprit.p].name + ' took it, in the ' + M.places[M.culprit.l] + ', using this method: ' + M.methods[M.culprit.m] + '.';
  let h = '<div class="pg"><div class="mono ttl">' + M.title + '</div><div class="sub">Whodunnit? · ' + C.unitName + ' · Teacher Guide and Answer Key</div><div class="rule"></div>' +
    '<table class="k"><tr><th>Unit</th><th>Time</th><th>Supplies</th><th>Group size</th></tr><tr><td>Unit ' + C.unitNo + ': ' + C.unitName + '</td><td>20–40 minutes</td><td>Pencil, scrap paper, scissors</td><td>Teams of 2–3 (or solo)</td></tr></table>' +
    '<div class="box"><b>Skills practiced:</b> order of operations, evaluating expressions, combining like terms, the distributive property, and writing expressions from words.</div>' +
    '<div class="box"><h3>General procedures</h3><ol><li>Give each student the <b>student sheet</b> (story and case board) and the <b>Show Your Work</b> page.</li><li>Print the <b>Clue Cards</b> (pages 3–7 of the student packet) and cut them apart on the dashed lines. Post them around the room.</li><li>Students visit the cards in any order. At each card they solve the problem, find their answer among the four choices, read the clue beside it, and cross things off the case board. <b>Every wrong choice leads to a false clue</b> that clears the real culprit, so a mistake shows up when the board does not narrow down to one suspect, one place and one method.</li><li>When a team thinks it knows, they bring you the three names. If they are wrong, let them hunt for the card where something went wrong.</li></ol></div>' +
    '<div class="sol">Solution: ' + cul + '</div><div class="box"><b>The reveal (read aloud):</b> ' + M.ending + '</div>' +
    '<div class="box"><h3>Clue map: what each correct clue clears</h3><table class="k"><tr><th>Card</th><th>Clears</th></tr>' + M.questions.map((q, i) => '<tr><td>' + (i + 1) + '</td><td>' + (q.clue.p !== undefined ? 'Suspect: ' + M.suspects[q.clue.p].name + ' · Place: ' + M.places[q.clue.l] : 'Method: ' + M.methods[q.clue.m]) + '</td></tr>').join('') + '</table></div></div>';
  h += '<div class="pg"><div class="mono ttl">Answer Key</div><div class="sub">' + M.title + ' · Correct choice and worked solution for each card</div><div class="rule"></div><table class="k"><tr><th>#</th><th>Problem</th><th>Correct choice</th><th>Worked solution</th><th>Clue it leads to</th></tr>' +
    cards.map((c, i) => '<tr><td><b>' + (i + 1) + '</b></td><td>' + mt(c.q.instr) + ' ' + (c.q.tex ? tex(c.q.tex) : mt(c.q.text)) + '</td><td><span class="g">' + LET[c.pos] + '.</span> ' + mt(c.opts[c.pos].a) + '</td><td>' + c.q.steps.map(mt).join('<br>') + '</td><td>' + c.q.clue.text + '</td></tr>').join('') + '</table></div>';
  h += '<div class="pg"><div class="mono ttl">Wrong Choices</div><div class="sub">' + M.title + ' · The likely mistake behind each wrong choice, and the false clue it leads to</div><div class="rule"></div><table class="k"><tr><th>Card</th><th>Choice</th><th>Likely mistake</th><th>False clue</th></tr>' +
    cards.map((c, i) => c.opts.map((o, j) => o.ok ? '' : '<tr><td>' + (i + 1) + '</td><td>' + LET[j] + '. ' + mt(o.a) + '</td><td>' + o.why + '</td><td>' + o.clue + '</td></tr>').join('')).join('') + '</table></div>';
  return doc(WCSS, h);
}
/* ---- stations ---- */
const SCSS = 'body{font-family:"Times New Roman",Times,serif}.hd{text-align:center;font-size:15pt;margin-bottom:.06in}.st{border:1.5px solid #000;padding:2px 6px;font-size:11pt;margin-bottom:.05in}.nm{display:flex;justify-content:space-between;font-size:10pt;margin-bottom:.08in}.nm i{display:inline-block;border-bottom:1px solid #000;width:2.6in}.nm i.s{width:1.3in}' +
  '.note{font-style:italic;font-size:10pt;margin-bottom:.06in}.q{font-size:11pt;height:.82in;padding-left:.15in}.q b{margin-right:6px}.ft{position:absolute;left:.55in;right:.55in;bottom:.4in;border-top:1px solid #000;padding-top:3px;display:flex;justify-content:space-between;font-size:8.5pt}' +
  '.ks h3{font-size:11pt;margin:.12in 0 .04in}.kg{display:grid;grid-template-columns:1fr 1fr;gap:2px .3in;font-size:10pt}';
function stationsStudent() {
  const n = C.stations.length;
  return doc(SCSS, C.stations.map((s, i) => '<div class="pg"><div class="hd">Algebra Review: Unit ' + C.unitNo + ' — ' + C.unitName + '</div><div class="st"><b>Station ' + (i + 1) + ' of ' + n + ':</b> ' + s.title + '</div><div class="nm"><span>Name: <i></i></span><span>Date: <i class="s"></i></span></div><div class="note">' + s.note + '</div>' +
    s.items.map((it, k) => '<div class="q"><b>' + (k + 1) + '.</b>' + mt(it[0]) + '</div>').join('') + '<div class="ft"><span>Mr. K’s Classroom • Algebra • Unit ' + C.unitNo + ': ' + C.unitName + '</span><span>Page ' + (i + 1) + '</span></div></div>').join(''));
}
function stationsKey() {
  return doc(SCSS, '<div class="pg"><div class="hd">Algebra Review: Unit ' + C.unitNo + ' — ' + C.unitName + '<div style="font-size:11pt">Answer Key</div></div><div class="ks">' + C.stations.map((s, i) => '<h3>Station ' + (i + 1) + ': ' + s.title + '</h3><div class="kg">' +
    s.items.map((it, k) => '<div><b>' + (k + 1) + '.</b> ' + mt(it[1]) + '</div>').join('') + '</div>').join('') + '</div><div class="ft"><span>Mr. K’s Classroom • Algebra • Unit ' + C.unitNo + ': ' + C.unitName + '</span><span>Answer Key</span></div></div>');
}
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
  else if (s.kind === 'list') b = '<ul>' + s.items.map(x => '<li>' + mt(x) + '</li>').join('') + '</ul>';
  return '<div class="sec" style="--c:' + c[0] + ';--t:' + c[1] + '"><h2><i>' + n + '</i>' + s.title + '</h2><div class="in">' + b + '</div></div>';
}
function exHtml(s) { return '<div class="ex"><b class="l">Example:</b> ' + mt(s.example) + '<br>' + s.steps.map(st => '<b class="l">' + st[0] + '</b> ' + mt(st[1])).join('<br>') + '<br><span class="ans">Answer: ' + mt(s.answer) + '</span></div>'; }
function cheatSheet() {
  const ch = C.cheat, title = '<b>Unit ' + C.unitNo + ' · <span>' + C.unitName + '</span> Cheat Sheet</b>';
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
    out('artifacts/' + prefix + '-whodunnit/worksheet.pdf', whodunnitStudent()), out('artifacts/' + prefix + '-whodunnit/teacher-key.pdf', whodunnitKey()),
    out('artifacts/algebra-' + prefix + '-stations/worksheet.pdf', stationsStudent()), out('artifacts/algebra-' + prefix + '-stations/teacher-key.pdf', stationsKey()),
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
  const shot = async (url, file, w, h) => { const p2 = await browser.newPage({ viewport: { width: w, height: h } }); await p2.goto(url); await p2.waitForTimeout(700); await p2.screenshot({ path: file }); await p2.close(); };
  const thumbs = path.join(ROOT, 'thumbs');
  for (const [name, url] of [[prefix + '-' + M.slug, 'file://' + path.join(mysteryDir, 'index.html')], [prefix + '-escape-room', 'file://' + path.join(escDir, 'index.html')]]) await shot(url, path.join(thumbs, name + '.png'), 1200, 750);
  for (const [name, html] of [[prefix + '-whodunnit', whodunnitStudent()], ['algebra-' + prefix + '-stations', stationsStudent()], [prefix + '-cheat-sheet', cheatSheet()]]) {
    const tmp = path.join(thumbs, '_t.html'); fs.writeFileSync(tmp, html);
    const p2 = await browser.newPage({ viewport: { width: 816, height: 510 } }); await p2.goto('file://' + tmp); await p2.waitForTimeout(400); await p2.screenshot({ path: path.join(thumbs, name + '.png') }); await p2.close(); fs.unlinkSync(tmp);
  }
  await browser.close();
  console.log('done');
})();
