// node test-kid-ui.cjs <built _site>: for every Grade 1-5 short-answer question, the pad chosen for its answer
// must be able to type an answer the checker accepts (the full answer, or the bare number for "8 cubes").
const fs = require('fs'), path = require('path');
const K = require('../worksheet-generator/core/elementary/kid-ui/kid-ui.js');
const site = process.argv[2];
const PADKEYS = { number: '0123456789', compare: '<>=', time: '0123456789:', 'time-ampm': '0123456789: AMP', cents: '0123456789¢',
  dollars: '0123456789$.', fraction: '0123456789/ ', decimal: '0123456789.', remainder: '0123456789R ', 'number-unit': '0123456789', 'fraction-unit': '0123456789/ ', 'tens-ones': '0123456789 ', 'dollars-cents': '0123456789$¢' };
const kinds = {}, untypeable = [], hints = {};
let n = 0;
for (let g = 1; g <= 5; g++) {
  const dir = path.join(site, 'question-banks', 'grade' + g);
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith('.json')) continue;
    for (const q of JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions) {
      if (q.format !== 'short-answer' || typeof q.answer !== 'string') continue;
      n++;
      const k = K.kind(q.answer); kinds[k] = (kinds[k] || 0) + 1;
      const h = K.hint(q.answer, g); hints[h] = (hints[h] || 0) + 1;
      const keys = PADKEYS[k];
      if (!keys) continue;                                         // pairs and words keep the keyboard
      const target = (k === 'number-unit' ? q.answer.match(/^[\d,]+/)[0].replace(/,/g, '') : k === 'fraction-unit' ? q.answer.match(/^(\d+ )?\d+\/\d+/)[0] : k === 'tens-ones' ? q.answer.replace(/^(\d+) tens? and (\d+) ones?$/i, '$1 $2') : q.answer.replace(/,(?=\d{3})/g, '')).replace(/ and /g, '');
      if ([...target].some(c => !keys.includes(c))) untypeable.push([q.id, q.answer, k]);
    }
  }
}
console.log(n, 'short answers;', 'pad kinds', kinds);
console.log('hint lines', hints);
console.log('answers the pad cannot type:', untypeable.length); untypeable.slice(0, 10).forEach(u => console.log('  ', u.join(' | ')));
process.exit(untypeable.length ? 1 : 0);
