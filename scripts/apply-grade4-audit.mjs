// 4th Grade Math audit (2026-11-19): Classroom-owned overlays on the pinned Grade 4 release.
// Runs after apply-content-updates.mjs and apply-kid-friendly.mjs. Every edit is guarded by the value it replaces, so
// a new Grade 4 release that changes an item fails here instead of being silently overwritten.
//  1. content-updates/2026-11-19/grade4/<unit>.json: edits, new questions and player metadata for both bank copies
//     (question-banks/grade4 for the site generators, grade4/question-banks/math4 for the Grade 4 players).
//  2. the Grade 4 player's answer checker (audit #2, #3, #10, #12, #13, #20): units, comparisons, lists and money,
//     the form a conversion item asks for, explanation parts, and the mistake shown on error-analysis items.
//  3. the Grade 4 skill-to-standard map (audit #5) and the course card's question count (audit #17).
//  4. the Grade 4 pacing guide and standards coverage page (audit #6).
import fs from 'node:fs';
import path from 'node:path';
import { grade4Pacing } from './geo-planning.mjs';

const out = path.resolve(process.argv[2] || '_site');
const src = path.resolve('content-updates/2026-11-19/grade4');
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const write = (p, d) => fs.writeFileSync(p, JSON.stringify(d, null, 1) + '\n');
const VERSION = 'g4-audit-20261119';
let edits = 0, added = 0, metas = 0;

/* ---------- 1. banks ---------- */
const same = (a, b) => JSON.stringify(a ?? null) === JSON.stringify(b ?? null);
for (const name of fs.readdirSync(src).filter((f) => f.endsWith('.json') && f !== 'course.json')) {
  const d = read(path.join(src, name)), unit = d.unit;
  for (const [rel, nested] of [[`question-banks/grade4/${unit}.json`, false], [`grade4/question-banks/math4/${unit}.json`, true]]) {
    const file = path.join(out, rel), bank = read(file), byId = new Map(bank.questions.map((q) => [q.id, q]));
    for (const e of d.edits) {
      const q = byId.get(e.id);
      if (!q) throw Error(`Grade 4 audit: missing item ${e.id} in ${rel}`);
      for (const [field, c] of Object.entries(e.changes)) {
        if (same(q[field], c.to)) continue;
        if (!same(q[field], c.from)) throw Error(`Grade 4 audit: ${e.id}/${field} changed upstream in ${rel}`);
        if (c.to === null) delete q[field]; else q[field] = c.to;
        edits++;
      }
    }
    for (const original of d.additions) {
      if (byId.has(original.id)) continue;
      if (nested && original.format === 'plot') continue;   // the Grade 4 players cannot show plot items
      const q = structuredClone(original);
      q.courseId = bank.courseId === 'math4' ? undefined : q.courseId;
      bank.questions.push(q);
      added++;
    }
    write(file, bank);
  }
  const metaFile = path.join(out, `grade4/question-banks/math4/meta/${unit}.meta.json`), meta = read(metaFile);
  for (const [id, m] of Object.entries(d.meta || {})) { meta[id] = m; metas++; }
  write(metaFile, meta);
}

/* ---------- 2. the Grade 4 player's answer checker ---------- */
function patch(rel, pairs) {
  const file = path.join(out, rel);
  let s = fs.readFileSync(file, 'utf8');
  for (const [from, to] of pairs) {
    if (s.includes(to)) continue;
    if (!s.includes(from)) throw Error(`Grade 4 audit: patch anchor missing in ${rel}: ${from.slice(0, 60)}`);
    s = s.replace(from, () => to);
  }
  fs.writeFileSync(file, s);
}
const CHECKER = `
  /* 4th Grade Math audit (2026-11-19). A typed answer is also right when it uses a unit abbreviation (6 ft, 20 sq cm,
     20 cm²), words for a comparison (less than) or for money (12 dollars, 75 cents), or spaces between the numbers of a
     list (#2, #10, #12, #13). When the prompt asks for a form (a mixed number, a fraction greater than 1, a decimal, a
     fraction with a given denominator, simplest form, an equivalent fraction), the typed answer must be in that form:
     retyping the number the prompt gives is not an answer (#3). */
  var UNITS = { ft: 'feet', 'in': 'inches', yd: 'yards', mi: 'miles', mm: 'millimeters', cm: 'centimeters', m: 'meters', km: 'kilometers',
    g: 'grams', kg: 'kilograms', mg: 'milligrams', l: 'liters', ml: 'milliliters', lb: 'pounds', lbs: 'pounds', oz: 'ounces', 'fl oz': 'fluid ounces',
    c: 'cups', pt: 'pints', qt: 'quarts', gal: 'gallons', sec: 'seconds', s: 'seconds', min: 'minutes', mins: 'minutes', hr: 'hours', hrs: 'hours', h: 'hours', wk: 'weeks', yr: 'years', deg: 'degrees' };
  function spell(t) {
    var s = String(t || '').trim().replace(/\\s+/g, ' ');
    if (/^(?:is )?(?:less than|fewer than)$/i.test(s)) return '<';
    if (/^(?:is )?(?:greater than|more than)$/i.test(s)) return '>';
    if (/^(?:is )?(?:equal to|equals|equal|the same as)$/i.test(s)) return '=';
    var money = /^([\\d,]+(?:\\.\\d+)?)\\s*dollars?$/i.exec(s); if (money) return '$' + money[1];
    var cents = /^(\\d{1,2})\\s*(?:cents?|¢)$/i.exec(s); if (cents) return '$0.' + (cents[1].length === 1 ? '0' : '') + cents[1];
    s = s.replace(/([\\d.\\/])\\s*(sq\\.?|square)\\s*([a-z]+)\\.?$/i, function (m, d, q, u) { return d + ' square ' + (UNITS[u.toLowerCase()] || u); })
      .replace(/([\\d.\\/])\\s*([a-z]+)(²|\\^2)$/i, function (m, d, u) { return d + ' square ' + (UNITS[u.toLowerCase()] || u); })
      .replace(/([\\d.\\/])\\s*(fl oz|[a-z]+)\\.?((?:\\s+[\\d,]+\\s*(?:fl oz|[a-z]+)\\.?)*)$/i, function (m, d, u, rest) {
        var full = UNITS[u.toLowerCase()];
        rest = rest.replace(/([\\d,]+)\\s*(fl oz|[a-z]+)\\.?/gi, function (m2, n2, u2) { return n2 + ' ' + (UNITS[u2.toLowerCase()] || u2); });
        return d + ' ' + (full || u) + rest;
      });
    return s;
  }
  function formOf(t) {
    t = String(t).trim().replace(/^\\$/, '');
    if (/^\\d+\\s+\\d+\\s*\\/\\s*\\d+/.test(t)) return 'mixed';
    if (/^\\d+\\s*\\/\\s*\\d+/.test(t)) return 'fraction';
    if (/^\\d*\\.\\d+/.test(t)) return 'decimal';
    if (/^[\\d,]+(\\s|$)/.test(t)) return 'whole';
    return 'other';
  }
  function den(t) { var m = /\\/\\s*(\\d+)/.exec(t); return m ? +m[1] : null; }
  function formOk(typed, key, prompt) {
    if (!prompt) return true;
    var asks = /mixed number|fraction greater than 1|as a fraction|as a decimal|decimal notation|denominator|simplest form|equivalent|equal parts|cut into \\d+|___\\s*\\/\\s*\\d+|n\\/\\d+|hundredths|tenths/i.test(prompt);
    if (!asks) return true;
    var kf = formOf(key), tf = formOf(typed);
    if (kf === 'other' || kf === 'whole') return true;
    if (kf !== tf) return false;
    // a named denominator, equal parts or a missing numerator fixes the denominator too
    if ((kf === 'fraction' || kf === 'mixed') && /denominator|equal parts|cut into \\d+|___\\s*\\/\\s*\\d+|n\\/\\d+|hundredths|tenths|simplest form/i.test(prompt)) return den(typed) === den(key);
    return true;
  }
  function checkAnswer(typed, key, prompt) {
    var ok = matches(typed, key) || matches(spell(typed), key);
    if (!ok && /\\d, \\d/.test(String(key)) && /^\\s*\\d[\\d\\s]*\\d\\s*$/.test(String(typed))) ok = matches(String(typed).trim().split(/\\s+/).join(', '), key);
    return ok && formOk(spell(typed), key, prompt);
  }
  function selfCheck(part) { return /^Sample answer:/.test(String(part && part.answer || '')); }
`;
const PRE = 'elementary/el-core.js';
patch(`grade4/worksheet-generator/${PRE}`, [
  ['  function compound(t, k) {', CHECKER + '  function compound(t, k) {'],
  ['var ok = matches(inp.value, p.parts[i].answer);', 'var ok = selfCheck(p.parts[i]) ? !!inp.value.trim() : checkAnswer(inp.value, p.parts[i].answer, p.parts[i].prompt + " " + p.prompt);'],
  ['var ok = matches(input.value, p.answer);', 'var ok = checkAnswer(input.value, p.answer, p.prompt);'],
  ['parseNum: parseNum, matches: matches,', 'parseNum: parseNum, matches: matches, checkAnswer: checkAnswer, selfCheck: selfCheck,'],
  // error-analysis items: show the mistake after every answer (#20)
  ['        explain();\n        if (opts.onNext)', '        explain();\n        if (/solved this problem/.test(p.prompt) && p.meta && p.meta.misconception) { var mk = el(\'p\', box, \'el-hint\'); mk.textContent = \'The mistake: the student \' + p.meta.misconception.replace(/\\.$/, \'\') + \'.\'; }\n        if (opts.onNext)']
]);
patch('grade4/worksheet-generator/elementary/el-understanding-check.js', [
  ['ok: K.matches(inp.value, p.answer)', 'ok: K.checkAnswer(inp.value, p.answer, p.prompt)'],
  ["if (!ok && p.meta.misconception) {", "if (p.meta.misconception && /solved this problem/.test(p.prompt)) { var mk = el('p', box, 'el-hint'); mk.textContent = 'The mistake: the student ' + p.meta.misconception.replace(/\\.$/, '') + '.'; }\n    else if (!ok && p.meta.misconception) {"]
]);
{
  // open-response parts in the Understanding Check: explanation parts are self-checked, the rest use the full checker
  const f = path.join(out, 'grade4/worksheet-generator/elementary/el-understanding-check.js');
  let s = fs.readFileSync(f, 'utf8');
  const re = /ok: ins\.every\(function \(x, i\) \{ return K\.matches\(x\.value, p\.parts\[i\]\.answer\); \}\)/;
  if (re.test(s)) s = s.replace(re, 'ok: ins.every(function (x, i) { return K.selfCheck(p.parts[i]) ? !!x.value.trim() : K.checkAnswer(x.value, p.parts[i].answer, p.parts[i].prompt + " " + p.prompt); })');
  else if (!s.includes('K.selfCheck(p.parts[i])')) throw Error('Grade 4 audit: Understanding Check part checker anchor missing');
  fs.writeFileSync(f, s);
}
for (const page of ['grade4-games.html', 'grade4-understanding-check.html', 'grade4-flashcards.html']) {
  const f = path.join(out, 'grade4/worksheet-generator', page);
  let s = fs.readFileSync(f, 'utf8');
  s = s.replace(/(elementary\/el-(?:core|understanding-check|games)\.js)(?:\?v=[^"]*)?"/g, `$1?v=${VERSION}"`);
  fs.writeFileSync(f, s);
}

/* ---------- 3. standards map and course card ---------- */
const units = fs.readdirSync(path.join(out, 'question-banks/grade4')).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', ''));
const map = {};
let total = 0;
for (const u of units) {
  const bank = read(path.join(out, 'question-banks/grade4', u + '.json'));
  total += bank.questions.length;
  const by = {};
  for (const q of bank.questions) for (const c of q.standards || []) { (by[q.skillId] = by[q.skillId] || {})[c] = (by[q.skillId][c] || 0) + 1; }
  map['grade4-' + u] = Object.fromEntries(Object.entries(by).map(([sk, cs]) => [sk, Object.entries(cs).sort((a, b) => b[1] - a[1]).map(([c]) => c)]));
}
{
  const f = path.join(out, 'grade4-main-catalog.js');
  let s = fs.readFileSync(f, 'utf8');
  const marker = '/* Grade 4 audit 2026-11-19 */';
  if (!s.includes(marker)) {
    s = s.replace(/("approved":"\d+ skills · )[\d,]+( verified questions)/, (m, a, b) => a + total.toLocaleString('en-US') + b);
    s += marker + '(function(G){var M=' + JSON.stringify(map) + ';G.MKSTD_SKILLS=G.MKSTD_SKILLS||{};Object.keys(M).forEach(function(k){G.MKSTD_SKILLS[k]=M[k];});})(typeof window!=="undefined"?window:globalThis);\n';
    fs.writeFileSync(f, s);
  }
  if (!new RegExp('"approved":"\\d+ skills · ' + total.toLocaleString('en-US') + ' verified questions').test(s)) throw Error('Grade 4 audit: course card count not updated');
}
// every page that loads the Grade 4 catalog bridge gets the new version, so browsers fetch the standards map
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) { if (e.name !== 'question-banks' && e.name !== 'assets') walk(f); continue; }
    if (!e.name.endsWith('.html')) continue;
    const s = fs.readFileSync(f, 'utf8');
    if (s.includes('grade4-main-catalog.js?v=')) fs.writeFileSync(f, s.replace(/grade4-main-catalog\.js\?v=[^"]*"/g, `grade4-main-catalog.js?v=${VERSION}"`));
  }
})(out);

/* ---------- 4. pacing guide ---------- */
const pacing = grade4Pacing(out);
if (pacing) {
  const tpl = fs.readFileSync(path.join(out, 'grade-6-pacing/index.html'), 'utf8');
  const page = tpl.replace(/<main>[\s\S]*<\/main>/, '<main>\n' + pacing + '\n</main>')
    .replace(/6th Grade Math Pacing Guide and Standards Coverage/g, '4th Grade Math Pacing Guide and Standards Coverage')
    .replace(/grade-6-pacing\//g, 'grade-4-pacing/')
    .replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="A 180-day 4th Grade Math pacing guide with Grade 4 MCAS review, a one-semester block plan, and Common Core Grade 4 standards coverage for every question-bank skill."')
    .replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="A 180-day 4th Grade Math pacing guide with Grade 4 MCAS review, a one-semester block plan, and Common Core Grade 4 standards coverage for every question-bank skill."')
    .replace(/<a href="\.\.\/u\/math6\/">[^<]*<\/a>/, '<a href="../u/grade4/">4th Grade Math</a>');
  fs.mkdirSync(path.join(out, 'grade-4-pacing'), { recursive: true });
  fs.writeFileSync(path.join(out, 'grade-4-pacing/index.html'), page);
}
console.log(`Grade 4 audit overlay: ${edits} field edits, ${added} new question copies, ${metas} metadata entries, ${total} questions, pacing ${pacing ? 'yes' : 'no'}.`);
