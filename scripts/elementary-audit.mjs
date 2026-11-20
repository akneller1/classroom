// Shared overlay step for the elementary course audits (4th Grade Math 2026-11-19, 3rd Grade Math 2026-11-19).
// Grades 3 and 4 come from pinned FinancialAlgebra releases, so audit fixes are Classroom-owned overlays applied at deploy.
// Every edit is guarded by the value it replaces, so a new release that changes an item fails here instead of being
// silently overwritten.
//  1. content-updates/<date>/grade<N>/<unit>.json: edits, new questions and player metadata for both bank copies
//     (question-banks/grade<N> for the site generators, grade<N>/question-banks/<player> for the players).
//  2. the player's answer checker: units, comparisons, lists, money and times, the form or denominator an item asks
//     for, explanation parts, and the mistake shown on error-analysis items.
//  3. the skill-to-standard map and the course card's question count.
//  4. the pacing guide and standards coverage page.
import fs from 'node:fs';
import path from 'node:path';
import { elementaryPacing } from './geo-planning.mjs';

const ORDS = { 1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 5: '5th' };
export function applyElementaryAudit({ grade: N, player: P, date: DATE, version: VERSION, out }) {
  const ORD = ORDS[N];
  const src = path.resolve(`content-updates/${DATE}/grade${N}`);
  const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
  const write = (p, d) => fs.writeFileSync(p, JSON.stringify(d, null, 1) + '\n');
  let edits = 0, added = 0, metas = 0;

  /* ---------- 1. banks ---------- */
  const same = (a, b) => JSON.stringify(a ?? null) === JSON.stringify(b ?? null);
  for (const name of fs.readdirSync(src).filter((f) => f.endsWith('.json') && f !== 'course.json')) {
    const d = read(path.join(src, name)), unit = d.unit;
    for (const [rel, nested] of [[`question-banks/grade${N}/${unit}.json`, false], [`grade${N}/question-banks/${P}/${unit}.json`, true]]) {
      const file = path.join(out, rel), bank = read(file), byId = new Map(bank.questions.map((q) => [q.id, q]));
      for (const e of d.edits) {
        const q = byId.get(e.id);
        if (!q) throw Error(`Grade ${N} audit: missing item ${e.id} in ${rel}`);
        for (const [field, c] of Object.entries(e.changes)) {
          if (same(q[field], c.to)) continue;
          if (!same(q[field], c.from)) throw Error(`Grade ${N} audit: ${e.id}/${field} changed upstream in ${rel}`);
          if (c.to === null) delete q[field]; else q[field] = c.to;
          edits++;
        }
      }
      for (const original of d.additions) {
        if (byId.has(original.id)) continue;
        if (nested && original.format === 'plot') continue;   // the elementary players cannot show plot items
        const q = structuredClone(original);
        q.courseId = bank.courseId === P ? undefined : q.courseId;
        bank.questions.push(q);
        added++;
      }
      write(file, bank);
    }
    const metaFile = path.join(out, `grade${N}/question-banks/${P}/meta/${unit}.meta.json`), meta = read(metaFile);
    for (const [id, m] of Object.entries(d.meta || {})) { meta[id] = m; metas++; }
    write(metaFile, meta);
  }

  /* ---------- 2. the player's answer checker ---------- */
  function patch(rel, pairs) {
    const file = path.join(out, rel);
    let s = fs.readFileSync(file, 'utf8');
    for (const [from, to] of pairs) {
      if (s.includes(to)) continue;
      if (!s.includes(from)) throw Error(`Grade ${N} audit: patch anchor missing in ${rel}: ${from.slice(0, 60)}`);
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
    // 3rd Grade Math audit (2026-11-19): a bare comparison word (#10) and a time typed with AM or PM (#11)
    if (/^(?:is )?(?:less|fewer|smaller)$/i.test(s)) return '<';
    if (/^(?:is )?(?:greater|more|bigger|larger)$/i.test(s)) return '>';
    var clock = /^(\\d{1,2}:\\d\\d)\\s*(?:a\\.?m\\.?|p\\.?m\\.?)$/i.exec(s); if (clock) return clock[1];
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
    var asks = /mixed number|fraction greater than 1|as a fraction|as a decimal|decimal notation|denominator|simplest form|equivalent|equal parts|cut into \\d+|___\\s*\\/\\s*\\d+|[nk?]\\/\\d+|hundredths|tenths|in (?:halves|thirds|fourths|sixths|eighths)/i.test(prompt);
    if (!asks) return true;
    var kf = formOf(key), tf = formOf(typed);
    if (kf === 'other' || kf === 'whole') return true;
    if (kf !== tf) return false;
    // a named denominator, equal parts or a missing numerator fixes the denominator too
    if ((kf === 'fraction' || kf === 'mixed') && /denominator|equal parts|cut into \\d+|___\\s*\\/\\s*\\d+|[nk?]\\/\\d+|hundredths|tenths|simplest form|in (?:halves|thirds|fourths|sixths|eighths)/i.test(prompt)) return den(typed) === den(key);
    return true;
  }
  /* 2nd Grade Math audit (2026-11-19) #3: money in any equal form. 45¢, 45 cents, $0.45; $1 and 25¢, $1.25, 125¢,
     1 dollar 25 cents, 1 dollar and 25 cents; $8, 8 dollars, $8.00. Returns the amount in cents, or null. */
  function cents(t) {
    var s = String(t || '').trim().toLowerCase().replace(/\\s+/g, ' '), m;
    if ((m = /^\\$?(\\d+)\\.(\\d\\d)$/.exec(s)) && /^\\$/.test(s)) return +m[1] * 100 + +m[2];
    if ((m = /^\\$(\\d+)$/.exec(s))) return +m[1] * 100;
    if ((m = /^(\\d+)\\s*(?:¢|cents?)$/.exec(s))) return +m[1];
    if ((m = /^\\$(\\d+)\\s*(?:and\\s*)?(\\d+)\\s*(?:¢|cents?)$/.exec(s))) return +m[1] * 100 + +m[2];
    if ((m = /^(\\d+)\\s*dollars?(?:\\s*(?:and\\s*)?(\\d+)\\s*(?:¢|cents?))?$/.exec(s))) return +m[1] * 100 + (m[2] ? +m[2] : 0);
    return null;
  }
  function checkAnswer(typed, key, prompt) {
    var ok = matches(typed, key) || matches(spell(typed), key);
    // 1st Grade Math audit (2026-11-19) #1, #3, #16: tens and ones typed as "3 8", "3 tens 8 ones" or "3 tens, 8 ones";
    // clock words ("half past 3", "3 o'clock"); true and false as T, F, yes or no.
    if (!ok) { var tk = /^(\\d+) tens? and (\\d+) ones?$/i.exec(String(key).trim()), tt = /^\\s*(\\d+)\\s*(?:tens?)?\\s*,?\\s*(?:and\\s*)?(\\d+)\\s*(?:ones?)?\\s*$/i.exec(String(typed)); if (tk && tt) ok = +tk[1] === +tt[1] && +tk[2] === +tt[2]; }
    if (!ok && /^\\d{1,2}:(00|30)$/.test(String(key).trim())) { var kh = String(key).trim().split(':'), tw = String(typed).trim().toLowerCase().replace(/[’']/g, '').replace(/\\s+/g, ' '), hm;
      if ((hm = /^half past (\\d{1,2})$/.exec(tw))) ok = kh[1] === '30' && +hm[1] === +kh[0];
      else if ((hm = /^(\\d{1,2}) ?oclock$/.exec(tw))) ok = kh[1] === '00' && +hm[1] === +kh[0]; }
    if (!ok && /^(true|false)$/i.test(String(key).trim())) { var tv = String(typed).trim().toLowerCase().replace(/\\.$/, ''); ok = (String(key).trim().toLowerCase() === 'true') ? /^(t|yes|y|true)$/.test(tv) : /^(f|no|n|false)$/.test(tv); }
    if (!ok && /[¢$]/.test(String(key))) { var kc = cents(key), tc = cents(typed); ok = kc !== null && tc !== null && kc === tc; }
    // one fourth, one-fourth and one‑fourth (non-breaking hyphen) are the same answer (#18)
    if (!ok && /[a-z]/i.test(String(key))) ok = matches(String(typed).replace(/[\\s\\-\\u2010\\u2011]+/g, ' ').trim(), String(key).replace(/[\\s\\-\\u2010\\u2011]+/g, ' ').trim());
    if (!ok && /\\d, \\d/.test(String(key)) && /^\\s*\\d[\\d\\s]*\\d\\s*$/.test(String(typed))) ok = matches(String(typed).trim().split(/\\s+/).join(', '), key);
    return ok && formOk(spell(typed), key, prompt);
  }
  function selfCheck(part) { return /^Sample answer:/.test(String(part && part.answer || '')); }
`;
  const PRE = 'elementary/el-core.js';
  patch(`grade${N}/worksheet-generator/${PRE}`, [
    ['  function compound(t, k) {', CHECKER + '  function compound(t, k) {'],
    ['var ok = matches(inp.value, p.parts[i].answer);', 'var ok = selfCheck(p.parts[i]) ? !!inp.value.trim() : checkAnswer(inp.value, p.parts[i].answer, p.parts[i].prompt + " " + p.prompt);'],
    ['var ok = matches(input.value, p.answer);', 'var ok = checkAnswer(input.value, p.answer, p.prompt);'],
    ['parseNum: parseNum, matches: matches,', 'parseNum: parseNum, matches: matches, checkAnswer: checkAnswer, selfCheck: selfCheck,'],
    // error-analysis items: show the mistake after every answer (#20)
    ['        explain();\n        if (opts.onNext)', '        explain();\n        if (/solved this problem/.test(p.prompt) && p.meta && p.meta.misconception) { var mk = el(\'p\', box, \'el-hint\'); mk.textContent = \'The mistake: the student \' + p.meta.misconception.replace(/\\.$/, \'\') + \'.\'; }\n        if (opts.onNext)']
  ]);
  patch(`grade${N}/worksheet-generator/elementary/el-understanding-check.js`, [
    ['ok: K.matches(inp.value, p.answer)', 'ok: K.checkAnswer(inp.value, p.answer, p.prompt)'],
    ["if (!ok && p.meta.misconception) {", "if (p.meta.misconception && /solved this problem/.test(p.prompt)) { var mk = el('p', box, 'el-hint'); mk.textContent = 'The mistake: the student ' + p.meta.misconception.replace(/\\.$/, '') + '.'; }\n    else if (!ok && p.meta.misconception) {"]
  ]);
  {
    // open-response parts in the Understanding Check: explanation parts are self-checked, the rest use the full checker
    const f = path.join(out, `grade${N}/worksheet-generator/elementary/el-understanding-check.js`);
    let s = fs.readFileSync(f, 'utf8');
    const re = /ok: ins\.every\(function \(x, i\) \{ return K\.matches\(x\.value, p\.parts\[i\]\.answer\); \}\)/;
    if (re.test(s)) s = s.replace(re, 'ok: ins.every(function (x, i) { return K.selfCheck(p.parts[i]) ? !!x.value.trim() : K.checkAnswer(x.value, p.parts[i].answer, p.parts[i].prompt + " " + p.prompt); })');
    else if (!s.includes('K.selfCheck(p.parts[i])')) throw Error(`Grade ${N} audit: Understanding Check part checker anchor missing`);
    fs.writeFileSync(f, s);
  }
  for (const page of [`grade${N}-games.html`, `grade${N}-understanding-check.html`, `grade${N}-flashcards.html`]) {
    const f = path.join(out, `grade${N}/worksheet-generator`, page);
    let s = fs.readFileSync(f, 'utf8');
    s = s.replace(/(elementary\/el-(?:core|understanding-check|games)\.js)(?:\?v=[^"]*)?"/g, `$1?v=${VERSION}"`);
    fs.writeFileSync(f, s);
  }

  /* ---------- 3. standards map and course card ---------- */
  const units = fs.readdirSync(path.join(out, `question-banks/grade${N}`)).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', ''));
  const map = {};
  let total = 0;
  for (const u of units) {
    const bank = read(path.join(out, `question-banks/grade${N}`, u + '.json'));
    total += bank.questions.length;
    const by = {};
    for (const q of bank.questions) for (const c of q.standards || []) { (by[q.skillId] = by[q.skillId] || {})[c] = (by[q.skillId][c] || 0) + 1; }
    map[`grade${N}-` + u] = Object.fromEntries(Object.entries(by).map(([sk, cs]) => [sk, Object.entries(cs).sort((a, b) => b[1] - a[1]).map(([c]) => c)]));
  }
  {
    const f = path.join(out, `grade${N}-main-catalog.js`);
    let s = fs.readFileSync(f, 'utf8');
    const marker = `/* Grade ${N} audit ${DATE} */`;
    if (!s.includes(marker)) {
      s = s.replace(/("approved":"\d+ skills · )[\d,]+( verified questions)/, (m, a, b) => a + total.toLocaleString('en-US') + b);
      s += marker + '(function(G){var M=' + JSON.stringify(map) + ';G.MKSTD_SKILLS=G.MKSTD_SKILLS||{};Object.keys(M).forEach(function(k){G.MKSTD_SKILLS[k]=M[k];});})(typeof window!=="undefined"?window:globalThis);\n';
      fs.writeFileSync(f, s);
    }
    if (!new RegExp('"approved":"\\d+ skills · ' + total.toLocaleString('en-US') + ' verified questions').test(s)) throw Error(`Grade ${N} audit: course card count not updated`);
  }
  // every page that loads the course's catalog bridge gets the new version, so browsers fetch the standards map
  (function walk(dir) {
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      const f = path.join(dir, e.name);
      if (e.isDirectory()) { if (e.name !== 'question-banks' && e.name !== 'assets') walk(f); continue; }
      if (!e.name.endsWith('.html')) continue;
      const s = fs.readFileSync(f, 'utf8');
      if (s.includes(`grade${N}-main-catalog.js?v=`)) fs.writeFileSync(f, s.replace(new RegExp(`grade${N}-main-catalog\\.js\\?v=[^"]*"`, 'g'), `grade${N}-main-catalog.js?v=${VERSION}"`));
    }
  })(out);

  /* ---------- 4. pacing guide ---------- */
  const pacing = elementaryPacing(N, out);
  if (pacing) {
    const tpl = fs.readFileSync(path.join(out, 'grade-6-pacing/index.html'), 'utf8');
    const page = tpl.replace(/<main>[\s\S]*<\/main>/, '<main>\n' + pacing + '\n</main>')
      .replace(/6th Grade Math Pacing Guide and Standards Coverage/g, `${ORD} Grade Math Pacing Guide and Standards Coverage`)
      .replace(/grade-6-pacing\//g, `grade-${N}-pacing/`)
      .replace(/<meta name="description" content="[^"]*"/, `<meta name="description" content="A 180-day ${ORD} Grade Math pacing guide with ${N > 2 ? `Grade ${N} MCAS review` : "a spring review window"}, a one-semester block plan, and Common Core Grade ${N} standards coverage for every question-bank skill."`)
      .replace(/<meta property="og:description" content="[^"]*"/, `<meta property="og:description" content="A 180-day ${ORD} Grade Math pacing guide with ${N > 2 ? `Grade ${N} MCAS review` : "a spring review window"}, a one-semester block plan, and Common Core Grade ${N} standards coverage for every question-bank skill."`)
      .replace(/<a href="\.\.\/u\/math6\/">[^<]*<\/a>/, `<a href="../u/grade${N}/">${ORD} Grade Math</a>`);
    fs.mkdirSync(path.join(out, `grade-${N}-pacing`), { recursive: true });
    fs.writeFileSync(path.join(out, `grade-${N}-pacing/index.html`), page);
  }

  return { edits, added, metas, total, pacing: !!pacing };
}
