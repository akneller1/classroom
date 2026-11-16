// node test-read-aloud.cjs <built _site>: every Grade 1-5 prompt and choice must come out as plain words.
const fs = require('fs'), path = require('path');
const RA = require('../worksheet-generator/core/elementary/kid-ui/read-aloud.js');
const site = process.argv[2];
const LEFT = /[+−×÷=<>_$¢\[\]{}^□▢△→°≈⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ]|\d\/\d|\d:\d\d|\d[a-z]{2}|[?!]\./;
let n = 0, bad = [], samples = [];
for (let g = 1; g <= 5; g++) {
  const dir = path.join(site, 'question-banks', 'grade' + g);
  for (const f of fs.readdirSync(dir)) {
    if (!f.endsWith('.json')) continue;
    for (const q of JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')).questions) {
      const texts = [typeof q.prompt === 'string' ? q.prompt : ''].concat((q.options || []).map(o => o && o.text || ''));
      for (const t of texts) {
        if (!t) continue; n++;
        const out = RA.speakable(t, { grade: g });
        if (LEFT.test(out)) bad.push([q.id, t, out]);
        if (/[+−×÷=_$¢\/]/.test(t) && samples.length < 4000) samples.push([g, t, out]);
      }
    }
  }
}
console.log(`${n} texts checked, ${bad.length} still contain a symbol`);
bad.slice(0, 15).forEach(b => console.log('  BAD', b[0], '|', b[1].slice(0, 80), '=>', b[2].slice(0, 100)));
// fixed spot checks
const cases = [['9 + ___ = 10', '9 plus blank equals 10'], ['What is 3/4 of 12?', 'What is 3 fourths of 12?'], ['1/2 + 1/4', '1 half plus 1 fourth'],
  ['$4.50', '4 dollars and 50 cents'], ['45¢', '45 cents'], ['It is 7:05 PM.', "It is 7 oh 5 P M."], ['4:00', "4 o'clock"], ['12 R 3', '12 remainder 3'],
  ['2 1/2 cups', '2 and 1 half cups'], ['33 ___ 15', '33 blank 15'], ['5 > 3', '5 is greater than 3'], ['10³', '10 cubed'], ['0.75', '0 point 7 5'],
  ['There are 5 in the box.', 'There are 5 in the box.'], ['The rope is 12 in.', 'The rope is 12 inches'], ['22 + 16 = ?', '22 plus 16 equals what number'],
  ['A ribbon is 24 cm long.', 'A ribbon is 24 centimeters long.'], ['thirty‑five', 'thirty-five'], ['72 − 53', '72 minus 53'], ['15$', '15 dollar sign'], ['$74¢', 'dollar sign 74 cent sign'], ['___ − 3 = 12', 'blank minus 3 equals 12'], ['59,_68 < 59,468', '5, 9, blank, 6, 8 is less than 59,468'], ['from 2:23 to 3:35.', 'from 2 23 to 3 35.'], ['start?\nIvy answered: 10', 'start? Ivy answered: 10'], ['Ivy solved this problem.\nAdd 1 + 2', 'Ivy solved this problem. Add 1 plus 2'], ['10, 20, ?. What number goes where the ? is?', '10, 20, blank. What number goes where the blank is?'], ['How many are left?', 'How many are left?']];
let fail = 0;
for (const [i, want] of cases) { const got = RA.speakable(i); if (got !== want) { fail++; console.log('  CASE FAIL', JSON.stringify(i), '=>', JSON.stringify(got), 'want', JSON.stringify(want)); } }
console.log(`${cases.length - fail}/${cases.length} spot checks pass`);
fs.mkdirSync('test-results', {recursive:true}); fs.writeFileSync('test-results/read-aloud-samples.txt', samples.filter((_, i) => i % 40 === 0).map(s => `G${s[0]} | ${s[1].replace(/\n/g, ' / ')}\n   → ${s[2]}`).join('\n'));
process.exit(bad.length || fail ? 1 : 0);
