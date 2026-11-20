#!/usr/bin/env node
/* 1st Grade Math audit (2026-11-19): checks on the assembled site after scripts/apply-grade1-audit.mjs.
   Every new or rewritten item's answer is recomputed here from its prompt, independently of the authoring scripts in
   tools/grade1-audit-20261119. Usage: node scripts/test-grade3-audit.cjs [_site] */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict');
const OUT = path.resolve(process.argv[2] || '_site');
const UNITS = fs.readdirSync(path.join(OUT, 'question-banks/grade1')).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', ''));
const Q = [], N = [];
for (const u of UNITS) {
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'question-banks/grade1', u + '.json'), 'utf8')).questions) Q.push(Object.assign({ unit: u }, q));
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'grade1/question-banks/math1', u + '.json'), 'utf8')).questions) N.push(Object.assign({ unit: u }, q));
}
const byId = Object.fromEntries(Q.map((q) => [q.id, q]));
const fails = []; let checks = 0;
const check = (q, ok, msg) => { checks++; if (!ok) fails.push((q && q.id ? q.id + ': ' : '') + msg); };
const fam = (q) => ((q.sourceNotes || '').match(/family: ([\w-]+)\)/) || [])[1] || '';
const mask = (s) => s.replace(/-?\d+(?:,\d{3})*(?:\.\d+)?/g, '#');

/* ---------- numbers ---------- */
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
const n = (x) => Number(x).toLocaleString('en-US');
const I = (s) => +String(s).replace(/[,$]/g, '');
class R { constructor(a, b = 1) { const g = gcd(a, b) || 1; this.a = a / g; this.b = b / g; } add(o) { return new R(this.a * o.b + o.a * this.b, this.b * o.b); } sub(o) { return this.add(new R(-o.a, o.b)); } cmp(o) { return this.a * o.b - o.a * this.b; } }
const fr = (s) => { s = String(s).trim(); let m = /^(\d+) (\d+)\/(\d+)$/.exec(s); if (m) return new R(+m[1] * +m[3] + +m[2], +m[3]); m = /^(\d+)\/(\d+)$/.exec(s); if (m) return new R(+m[1], +m[2]); return new R(I(s)); };
const mixed = (x) => { const w = Math.floor(x.a / x.b), p = x.a - w * x.b; return p === 0 ? String(w) : w ? `${w} ${p}/${x.b}` : `${p}/${x.b}`; };
const rnd = (x, u) => Math.floor(x / u + 0.5) * u;
const g = (re, s) => { const m = re.exec(s); if (!m) throw Error('prompt shape ' + re); return m; };
const SING = { liters: 'liter', grams: 'gram', minutes: 'minute', feet: 'foot', 'square units': 'square unit', 'square feet': 'square foot', 'square centimeters': 'square centimeter', 'square inches': 'square inch', 'square meters': 'square meter', 'toy cars': 'toy car', strings: 'string', pieces: 'piece', squares: 'square' };
const qty = (x, u) => `${x} ${String(x) === '1' ? SING[u] || u.replace(/s$/, '') : u}`;
const tmin = (s) => { const [h, m] = s.split(':').map(Number); return h * 60 + m; };
const tm = (x) => `${((Math.floor(x / 60) - 1) % 12 + 12) % 12 + 1}:${String(x % 60).padStart(2, '0')}`;
const DN = { halves: 2, thirds: 3, fourths: 4, sixths: 6, eighths: 8 };
const SQ = { centimeter: 'square centimeters', meter: 'square meters', inch: 'square inches', foot: 'square feet' };
const SIDES = { triangle: 3, square: 4, rectangle: 4, pentagon: 5, hexagon: 6, octagon: 8, trapezoid: 4, rhombus: 4 };

Object.assign(SING, { inches: 'inch', people: 'person', children: 'child', crayons: 'crayon' });
const SH = { triangle: 3, square: 4, rectangle: 4, hexagon: 6 };
const COIN = { quarter: 25, quarters: 25, dime: 10, dimes: 10, nickel: 5, nickels: 5, penny: 1, pennies: 1 };
const coins = (s) => [...s.matchAll(/(\d+) (quarters?|dimes?|nickels?|penny|pennies)/g)].reduce((a, m) => a + m[1] * COIN[m[2]], 0);
const bills = (s) => [...s.matchAll(/(\d+) \$(\d+) bills?/g)].reduce((a, m) => a + m[1] * m[2], 0);
const ampm = (h, m, x) => { const H = h + x; return `${(H - 1) % 12 + 1}:${String(m).padStart(2, '0')} ${H < 12 ? 'AM' : 'PM'}`; };

Object.assign(SING, { ducks: 'duck', marbles: 'marble', grapes: 'grape', pets: 'pet', balloons: 'balloon', 'paper clips': 'paper clip', birds: 'bird', fish: 'fish', votes: 'vote', cars: 'car', stamps: 'stamp' });
const clock = (h, m) => `${h}:${String(m).padStart(2, '0')}`;
const W = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19, twenty: 20, thirty: 30, forty: 40, fifty: 50, sixty: 60, seventy: 70, eighty: 80, ninety: 90 };

/* ---------- recomputation of the #2 Advanced and #7 Standard families ---------- */
const RC = {
  at1_add_then_one_more: (p) => { const m = g(/Add (\d+) \+ (\d+)\. Then add (\d+) more/, p); return n(+m[1] + +m[2] + +m[3]); },
  at1_how_many_more_to_10: (p) => { const m = g(/has (\d+) (\w+)\. \w+ gives \w+ (\d+) more/, p); return qty(10 - m[1] - m[3], m[2]); },
  at2_take_away_twice: (p) => { const m = g(/Take (\d+) away from (\d+)\. Then take away (\d+) more/, p); return n(m[2] - m[1] - m[3]); },
  at2_start_unknown: (p) => { const m = g(/had some (\w+)\. \w+ gave away (\d+)\. Now \w+ has (\d+)/, p); return qty(+m[2] + +m[3], m[1]); },
  at3_make_ten_then_more: (p) => { const m = g(/goes with (\d+) to make 10\? Then add (\d+)/, p); return n(10 - m[1] + +m[2]); },
  at3_two_to_make_ten: (p) => { const m = g(/^(\d+) \+ (\d+) \+ ___ = 10/, p); return n(10 - m[1] - m[2]); },
  at4_partner_then_check: (p) => { const m = g(/^(\d+) is (\d+) and what number/, p); return n(m[1] - m[2]); },
  at4_three_parts: (p) => { const m = g(/^(\d+) is made of three parts\. Two parts are (\d+) and (\d+)/, p); return n(m[1] - m[2] - m[3]); },
  as1_add_then_more: (p) => { const m = g(/sum: (\d+) \+ (\d+)\. Then add (\d+)/, p); return n(+m[1] + +m[2] + +m[3]); },
  as1_make_ten_story: (p) => { const m = g(/has (\d+) stickers and \w+ has (\d+)\./, p); return qty(+m[1] + +m[2], 'stickers'); },
  as2_subtract_then_more: (p) => { const m = g(/Subtract: (\d+) − (\d+)\. Then take away (\d+) more/, p); return n(m[1] - m[2] - m[3]); },
  as2_back_through_ten: (p) => { const m = g(/finds (\d+) − (\d+) by going back/, p); return `${m[1] - 10}; ${m[1] - m[2]}`; },
  as3_three_then_order: (p) => { const m = g(/What is (\d+) \+ (\d+) \+ (\d+)\?/, p), s = +m[1] + +m[2] + +m[3]; return `${s}; ${s}`; },
  as3_find_the_ten: (p) => { const m = g(/Add (\d+) \+ (\d+) \+ (\d+)\./, p); return `${m[2]} and ${m[3]}; ${+m[1] + +m[2] + +m[3]}`; },
  as4_family_two_facts: (p) => { const m = g(/^(\d+) \+ (\d+) = \d+/, p); return `${m[2]}; ${m[1]}`; },
  as4_missing_in_family: (p) => { const m = g(/^(\d+) \+ ___ = (\d+)/, p); return `${m[2] - m[1]}; ${m[2] - m[1]}`; },
  eq1_true_false_sum: (p) => { const m = g(/Is (\d+) \+ (\d+) = (\d+) \+ (\d+) true/, p); return +m[1] + +m[2] === +m[3] + +m[4] ? 'true' : 'false'; },
  eq1_true_false_diff: (p) => { const m = g(/Is (\d+) − (\d+) = (\d+) − (\d+) true/, p); return m[1] - m[2] === m[3] - m[4] ? 'true' : 'false'; },
  eq2_missing_then_more: (p) => { const m = g(/^(\d+) \+ ___ = (\d+)\. .* add (\d+) to it/, p); return n(m[2] - m[1] + +m[3]); },
  eq2_missing_start: (p) => { const m = g(/___ − (\d+) = (\d+)/, p); return n(+m[1] + +m[2]); },
  eq3_balance_missing: (p) => { const m = g(/^(\d+) \+ (\d+) = (\d+) \+ ___/, p); return n(+m[1] + +m[2] - m[3]); },
  eq3_balance_subtract: (p) => { const m = g(/^(\d+) − (\d+) = (\d+) \+ ___/, p); return n(m[1] - m[2] - m[3]); },
  cn1_bags_plus_two: (p) => { const m = g(/There are (\d+) bags with 10 crayons in each bag, (\d+) loose crayons, and then (\d+) more/, p); return qty(10 * m[1] + +m[2] + +m[3], 'crayons'); },
  cn2_count_on_k: (p) => { const m = g(/Start at (\d+)\. Count on (\d+) more/, p); return n(+m[1] + +m[2]); },
  cn2_count_over_ten: (p) => { const m = g(/Count on (\d+) from (\d+)/, p); return n(+m[1] + +m[2]); },
  cn3_name_then_next: (p) => { const m = g(/The number (\w+)-(\w+) is written/, p), v = W[m[1]] + W[m[2]]; return `${v}; ${v + 1}`; },
  cn3_hundred_and: (p) => n(100 + W[g(/write one hundred (\w+) in numbers/, p)[1]]),
  cn4_on_then_back: (p) => { const m = g(/Start at (\d+)\. Count on (\d+), then count back (\d+)/, p); return n(+m[1] + +m[2] - m[3]); },
  cn4_how_many_counted: (p) => { const m = g(/counts on from (\d+) and stops at (\d+)/, p); return n(m[2] - m[1]); },
  to1_tens_plus_ones: (p) => { const m = g(/in (\d+) tens and (\d+) ones/, p); return n(10 * m[1] + +m[2]); },
  to2_teen_then_more: (p) => { const m = g(/1 ten and (\d+) ones\? Then add (\d+) more/, p); return n(10 + +m[1] + +m[2]); },
  to3_tens_jumps: (p) => { const m = g(/Start at (\d+)\. Count by tens (\d+) times/, p); return n(+m[1] + 10 * m[2]); },
  to3_how_many_tens_counted: (p) => { const m = g(/get from (\d+) to (\d+)\?/, p); return n((m[2] - m[1]) / 10); },
  to4_tens_ones_then_ten_more: (p) => { const m = g(/has (\d+) tens and (\d+) ones\?/, p), v = 10 * m[1] + +m[2]; return `${v}; ${v + 10}`; },
  to4_regroup_ones: (p) => { const m = g(/has (\d+) tens and (\d+) ones\. What/, p); return n(10 * m[1] + +m[2]); },
  cm1_greater_then_more: (p) => { const m = g(/greater, (\d+) or (\d+)\? Then add (\d+)/, p); return n(Math.max(+m[1], +m[2]) + +m[3]); },
  cm1_order_three: (p) => g(/least to greatest: (.*)$/, p)[1].split(', ').map(Number).sort((a, b) => a - b).join(', '),
  cm2_symbol_after_change: (p) => { const m = g(/(\d+) \+ (\d+) ___ (\d+)/, p), v = +m[1] + +m[2]; return v > +m[3] ? '>' : v < +m[3] ? '<' : '='; },
  cm2_tens_ones_compare: (p) => { const m = g(/(\d+) tens and (\d+) ones ___ (\d+) tens and (\d+) ones/, p), a = 10 * m[1] + +m[2], b = 10 * m[3] + +m[4]; return a > b ? '>' : a < b ? '<' : '='; },
  cm3_digit_to_make_greater: (p) => { const m = g(/(\d)\? < (\d+)/, p); return n(+m[2] % 10 - 1); },
  cm3_count_between: (p) => { const m = g(/greater than (\d+) and less than (\d+)/, p); return n(m[2] - m[1] - 1); },
  ah1_ten_more_twice: (p) => { const a = +g(/10 more than (\d+)\?/, p)[1]; return `${a + 10}; ${a + 20}`; },
  ah1_ten_less_k_times: (p) => { const m = g(/Start at (\d+)\. Take away 10, (\d+) times/, p); return n(m[1] - 10 * m[2]); },
  ah2_add_two_tens: (p) => { const m = g(/Add: (\d+) \+ (\d+) \+ (\d+)/, p); return n(+m[1] + +m[2] + +m[3]); },
  ah2_tens_sub_then_add: (p) => { const m = g(/Find (\d+) − (\d+) \+ (\d+)\./, p); return n(m[1] - m[2] + +m[3]); },
  ah3_add_ones_twice: (p) => { const m = g(/Add (\d+) \+ (\d+)\. Then add (\d+)/, p); return n(+m[1] + +m[2] + +m[3]); },
  ah3_missing_tens_ones: (p) => { const m = g(/^(\d+) \+ ___ = (\d+)/, p); return n(m[2] - m[1]); },
  ah4_new_ten_then_tens: (p) => { const m = g(/What is (\d+) \+ (\d+)\? Then add (\d+)/, p); return n(+m[1] + +m[2] + +m[3]); },
  ah4_break_to_ten: (p) => { const m = g(/To add (\d+) \+ (\d+), \w+ breaks \d+ into (\d+) and/, p); return `${+m[1] + +m[3]}; ${+m[1] + +m[2]}`; },
  ah5_tens_then_ones: (p) => { const m = g(/Add (\d+) \+ (\d+) by adding tens/, p); return `${Math.floor(m[1] / 10) * 10 + Math.floor(m[2] / 10) * 10}; ${+m[1] + +m[2]}`; },
  ah5_two_digit_plus_more: (p) => { const m = g(/read (\d+) pages on Monday and (\d+) pages on Tuesday\. On Wednesday they read (\d+) more/, p); return `${+m[1] + +m[2] + +m[3]} pages`; },
  tt1_hours_later: (p) => { const m = g(/It is (\d+):00\. What time will it be in (\d+) hours?/, p); return clock((+m[1] + +m[2] - 1) % 12 + 1, 0); },
  tt1_hours_before: (p) => { const m = g(/shows (\d+):00\. What time was it (\d+) hours? ago/, p); return clock(((m[1] - m[2] - 1) % 12 + 12) % 12 + 1, 0); },
  tt2_half_hour_later: (p) => { const h = +g(/It is (\d+):00\./, p)[1]; return `${h}:30; ${h + 1}:00`; },
  tt2_half_hour_before: (p) => clock(+g(/shows (\d+):00/, p)[1] - 1, 30),
  tt3_words_then_later: (p) => { let m = /Write half past (\d+) with/.exec(p); if (m) return `${clock(+m[1], 30)}; ${clock(+m[1] % 12 + 1, 30)}`; m = g(/Write (\d+) o'clock with/, p); return `${clock(+m[1], 0)}; ${clock(+m[1] % 12 + 1, 0)}`; },
  tt3_who_first: (p) => { const m = g(/^(\w+) eats lunch at (\d+:\d+)\. (\w+) eats lunch at (\d+:\d+)/, p); return tmin(m[2]) < tmin(m[4]) ? m[1] : m[3]; },
  dt1_tally_difference: (p) => { const m = g(/shows (\d+) votes for cats and (\d+) votes for dogs/, p); return qty(Math.abs(m[1] - m[2]), 'votes'); },
  dt2_tally_then_more: (p) => { const m = g(/has (\d+) bundles? of 5 and (\d+) more marks\. Then (\d+) more/, p); return n(5 * m[1] + +m[2] + +m[3]); },
  dt3_total_and_compare: (p) => { const m = g(/circles (\d+), squares (\d+) and triangles (\d+)/, p); return n(+m[1] + +m[2] + +m[3]); },
  sh1_corners_many: (p) => { const m = g(/corners do (\d+) (\w+)s have/, p); return n(m[1] * SH[m[2]]); },
  sh2_sides_two_shapes: (p) => { const m = g(/do a (\w+) and a (\w+) have together/, p); return n(SH[m[1]] + SH[m[2]]); },
  sh3_triangles_to_squares: (p) => n(2 * g(/make (\d+) squares/, p)[1]),
  sh4_shares_left: (p) => { const m = g(/cut into (halves|fourths)\. (\d+) shares? (?:is|are) eaten/, p); return n((m[1] === 'halves' ? 2 : 4) - m[2]); },
  sh5_shares_many: (p) => { const m = g(/^(\d+) pizzas are each cut into (halves|fourths)/, p); return n(m[1] * (m[2] === 'halves' ? 2 : 4)); },
  wp1_in_then_out: (p) => { const m = g(/^(\d+) birds were on a wire\. (\d+) more came\. Then (\d+) flew away/, p); return qty(+m[1] + +m[2] - m[3], 'birds'); },
  wp2_three_colors: (p) => { const m = g(/has (\d+) crayons\. (\d+) are red, (\d+) are blue/, p); return qty(m[1] - m[2] - m[3], 'crayons'); }
};
const A1 = Q.filter((q) => /\(#1, Advanced/.test(q.sourceNotes || '')), S7 = Q.filter((q) => /\(#7, Standard\)/.test(q.sourceNotes || ''));
check(null, A1.length >= 220, 'Advanced rewrites ' + A1.length);
check(null, S7.length >= 200, 'Standard rewrites ' + S7.length);
for (const q of [...A1, ...S7]) {
  const f = fam(q), fn = RC[f];
  check(q, !!fn, 'no recomputation for ' + f);
  if (!fn) continue;
  let want; try { want = fn(q.prompt); } catch (e) { check(q, false, e.message); continue; }
  check(q, String(q.answer) === want, `key ${q.answer} but recomputed ${want}`);
  check(q, A1.includes(q) ? q.level === 'honors' : q.level === 'cp1', 'level');
  if (q.format === 'multiple-choice') check(q, q.options.filter((o) => o.correct).length === 1 && q.options.find((o) => o.correct).text === q.answer && new Set(q.options.map((o) => o.text)).size === q.options.length, 'options');
  const lower = new Set(Q.filter((x) => x.skillId === q.skillId && (A1.includes(q) ? x.level !== 'honors' : x.level === 'cp2')).map((x) => mask(x.prompt)));
  check(q, !lower.has(mask(q.prompt)), 'still a lower-level template');
  check(q, (q.prompt + ' ' + q.answer).match(/\d+/g).every((x) => +x <= 120), 'number beyond 120');
}
const share = (L, lo) => { const low = new Set(Q.filter((q) => lo.includes(q.level)).map((q) => q.skillId + '|' + mask(q.prompt))); const xs = Q.filter((q) => q.level === L); return xs.filter((q) => low.has(q.skillId + '|' + mask(q.prompt))).length / xs.length; };
check(null, share('honors', ['cp2', 'cp1']) <= 0.29, 'Advanced items reusing a lower template ' + share('honors', ['cp2', 'cp1']).toFixed(2));
check(null, share('cp1', ['cp2']) <= 0.33, 'Standard items reusing a Support template ' + share('cp1', ['cp2']).toFixed(2));
const lv = (L) => Q.filter((q) => q.level === L).length;
check(null, Math.max(lv('cp2'), lv('cp1'), lv('honors')) - Math.min(lv('cp2'), lv('cp1'), lv('honors')) <= 1, `levels ${lv('cp2')}/${lv('cp1')}/${lv('honors')}`);
for (const L of ['cp2', 'cp1', 'honors']) check({ id: 'telling-time-skill-03' }, Q.filter((q) => q.skillId === 'telling-time-skill-03' && q.level === L).length === 34, 'telling-time skill 3 balanced');

/* ---------- #4 open response ---------- */
const O4 = Q.filter((q) => /\(#4, open response\)/.test(q.sourceNotes || ''));
const skills = [...new Set(Q.map((q) => q.skillId))];
assert.equal(skills.length, 47);
check(null, O4.length === 141 && Q.filter((q) => q.format === 'open-response').length === 141, 'open-response items ' + O4.length);
for (const s of skills) for (const L of ['cp2', 'cp1', 'honors']) check({ id: s + '|' + L }, O4.filter((q) => q.skillId === s && q.level === L).length === 1, 'one context open-response item');
for (const q of O4) {
  check(q, q.parts.length === 4 && /^Sample answer: /.test(q.parts[3].answer) && q.solutionSteps.length === 4, 'four parts ending with an explanation');
  check(q, q.parts.slice(0, 3).some((p) => !/^Sample answer: /.test(p.answer)), 'at least one checked part');
  check(q, !/^(Answer each part|Match each problem)/.test(q.prompt), 'not the drill template');
}
const OR = {
  at1_open_fish: (q) => { const m = g(/There are (\d+) red fish and (\d+) blue fish/, q.prompt); return [0, qty(+m[1] + +m[2], 'fish')]; },
  at2_open_cookies: (q) => { const m = g(/There are (\d+) cookies on a plate\. \w+ eats (\d+)/, q.prompt); return [0, qty(m[1] - m[2], 'cookies')]; },
  at3_open_ten_frame: (q) => [0, n(10 - g(/has (\d+) dots/, q.prompt)[1])],
  at4_open_partners: (q) => { const m = g(/^(\d+) children play in two groups\. (\d+) children/, q.prompt); return [0, n(m[1] - m[2])]; },
  as1_open_shells: (q) => { const m = g(/finds (\d+) shells\. A friend finds (\d+) shells/, q.prompt); return [0, qty(+m[1] + +m[2], 'shells')]; },
  as2_open_balloons: (q) => { const m = g(/There are (\d+) balloons\. (\d+) balloons/, q.prompt); return [0, qty(m[1] - m[2], 'balloons')]; },
  as3_open_three_bowls: (q) => { const m = g(/have (\d+), (\d+) and (\d+) grapes/, q.prompt); return [0, qty(+m[1] + +m[2] + +m[3], 'grapes')]; },
  as4_open_family: (q) => { const m = g(/numbers (\d+), (\d+) and (\d+)\./, q.prompt); return [1, n(m[3] - m[1])]; },
  wp1_open_ducks: (q) => { const m = g(/^(\d+) ducks are in a pond\. (\d+) more/, q.prompt); return [0, qty(+m[1] + +m[2], 'ducks')]; },
  wp2_open_crayons: (q) => { const m = g(/has (\d+) crayons\. (\d+) are red/, q.prompt); return [0, qty(m[1] - m[2], 'crayons')]; },
  wp3_open_compare: (q) => { const m = g(/Ben has (\d+) cars\. Zoe has (\d+) more/, q.prompt); return [0, qty(+m[1] + +m[2], 'cars')]; },
  wp4_open_start_unknown: (q) => { const m = g(/(\d+) more birds come\. Now there are (\d+) birds/, q.prompt); return [0, qty(m[2] - m[1], 'birds')]; },
  wp5_open_three: (q) => { const m = g(/has (\d+) red beads, (\d+) blue beads and (\d+) green/, q.prompt); return [0, qty(+m[1] + +m[2] + +m[3], 'beads')]; },
  eq1_open_true_false: (q) => { const m = g(/Look at (\d+) \+ (\d+) = (\d+) \+ (\d+)\./, q.prompt); return [2, +m[1] + +m[2] === +m[3] + +m[4] ? 'true' : 'false']; },
  eq2_open_missing: (q) => { const m = g(/^(\d+) \+ ___ = (\d+)\./, q.prompt); return [0, n(m[2] - m[1])]; },
  eq3_open_balance: (q) => { const m = g(/has (\d+) \+ (\d+) on one side and (\d+) \+ ___/, q.prompt); return [1, n(+m[1] + +m[2] - m[3])]; },
  cn1_open_bags: (q) => { const m = g(/There are (\d+) bags of 10 crayons and (\d+) loose/, q.prompt); return [0, qty(10 * m[1] + +m[2], 'crayons')]; },
  cn2_open_count_on: (q) => [1, n(+g(/counting at (\d+)/, q.prompt)[1] + 5)],
  cn3_open_write: (q) => { const m = g(/has (\d+) tens and (\d+) ones/, q.prompt); return [0, n(10 * m[1] + +m[2])]; },
  cn4_open_count_add: (q) => { const m = g(/Find (\d+) \+ (\d+) by counting/, q.prompt); return [0, n(+m[1] + +m[2])]; },
  to1_open_bundles: (q) => [0, n(10 * g(/has (\d+) bundles/, q.prompt)[1])],
  to2_open_teen: (q) => [0, n(10 + +g(/1 ten and (\d+) ones/, q.prompt)[1])],
  to3_open_tens_count: (q) => [1, n(+g(/starting at (\d+)/, q.prompt)[1] + 50)],
  to4_open_place: (q) => { const v = +g(/the number (\d+)\./, q.prompt)[1]; return [2, n((v % 10) * 10 + Math.floor(v / 10))]; },
  cm1_open_jars: (q) => { const m = g(/Jar A has (\d+) beans\. Jar B has (\d+)/, q.prompt); return [0, +m[1] > +m[2] ? 'A' : 'B']; },
  cm2_open_symbols: (q) => { const m = g(/Compare (\d+) and (\d+)\./, q.prompt); return [0, +m[1] > +m[2] ? '>' : '<']; },
  cm3_open_digit: (q) => { const v = +g(/> (\d+)\./, q.prompt)[1]; return [0, n(v % 10 + 1)]; },
  ah1_open_ten_more: (q) => [0, n(+g(/has (\d+) stamps/, q.prompt)[1] + 10)],
  ah2_open_tens: (q) => { const m = g(/has (\d+) books\. (\d+) more/, q.prompt); return [0, qty(+m[1] + +m[2], 'books')]; },
  ah3_open_ones: (q) => { const m = g(/has (\d+) marbles and gets (\d+) more/, q.prompt); return [0, qty(+m[1] + +m[2], 'marbles')]; },
  ah4_open_new_ten: (q) => { const m = g(/Add (\d+) \+ (\d+)\./, q.prompt); return [0, n(+m[1] + +m[2])]; },
  ah5_open_models: (q) => { const m = g(/add (\d+) \+ (\d+)\./, q.prompt); return [2, n(+m[1] + +m[2])]; },
  ml1_open_ribbons: (q) => { const xs = [...q.prompt.matchAll(/(\d+) cubes/g)].map((m) => +m[1]); return [2, qty(Math.max(...xs) - Math.min(...xs), 'cubes')]; },
  ml2_open_indirect: () => [0, 'ruler'],
  ml3_open_clips: (q) => [1, qty(2 * g(/is (\d+) paper clips long/, q.prompt)[1], 'paper clips')],
  ml4_open_mistake: (q) => { const m = g(/left (\d+) cube-sized gaps?\. She counted (\d+) cubes/, q.prompt); return [1, qty(+m[1] + +m[2], 'cubes')]; },
  tt1_open_hour: (q) => [0, clock(+g(/at (\d+) o'clock/, q.prompt)[1], 0)],
  tt2_open_half_hour: (q) => [0, clock(+g(/half past (\d+)/, q.prompt)[1], 30)],
  tt3_open_schedule: (q) => [2, clock(+g(/music starts at (\d+):30/, q.prompt)[1] + 1, 0)],
  dt1_open_tally: (q) => { const m = g(/apples (\d+), bananas (\d+), grapes (\d+)/, q.prompt); return [0, qty(+m[1] + +m[2] + +m[3], 'votes')]; },
  dt2_open_picture_graph: (q) => { const m = g(/dogs (\d+), cats (\d+), fish (\d+)/, q.prompt); return [0, qty(+m[1] + +m[2] + +m[3], 'pets')]; },
  dt3_open_table: (q) => { const m = g(/circles (\d+), squares (\d+), triangles (\d+)/, q.prompt); return [0, n(+m[1] + +m[2] + +m[3])]; },
  sh1_open_shape: (q) => [2, n(2 * SH[g(/Draw a (\w+)\./, q.prompt)[1]])],
  sh2_open_solid: (q) => [0, { cube: '6', cone: '1', cylinder: '2' }[g(/Look at a (\w+)\./, q.prompt)[1]]],
  sh3_open_compose: (q) => [0, n(2 * g(/wants to make (\d+) squares/, q.prompt)[1])],
  sh4_open_cookie: (q) => [0, n({ halves: 2, fourths: 4 }[g(/cut into (\w+)\./, q.prompt)[1]])],
  sh5_open_two_pies: () => [2, '2']
};
for (const q of O4) {
  const fn = OR[fam(q)];
  check(q, !!fn, 'no open-response recomputation for ' + fam(q));
  if (!fn) continue;
  try { const [i, want] = fn(q); check(q, q.parts[i].answer === want, `part ${i}: ${q.parts[i].answer} but recomputed ${want}`); } catch (e) { check(q, false, e.message); }
}

/* ---------- #8 select-all ---------- */
const S8 = Q.filter((q) => q.format === 'select-all');
check(null, S8.length === 126 && S8.every((q) => /\(#8, select-all/.test(q.sourceNotes || '')), 'every select-all item rewritten: ' + S8.length);
const ev = (s) => { s = s.replace(/×/g, '*').replace(/−/g, '-'); if (!/^[\d\s+*()-]+$/.test(s)) throw Error('bad expression ' + s); return Function('return ' + s)(); };
const T = (q, re) => +g(re, q.prompt)[1];
const tensOnes = (t) => { let v = 0; for (const m of t.matchAll(/(\d+) (tens?|ones?|bags of 10|more)\b/g)) v += m[1] * (/^ten|bags/.test(m[2]) ? 10 : 1); return v; };
const SEL = {
  at1_select_sum: (q, t) => ev(t) === T(q, /that make (\d+)\./), at2_select_difference: (q, t) => ev(t) === T(q, /that equal (\d+)\./), at3_select_make_ten: (q, t) => ev(t) === 10,
  at4_select_partners: (q, t) => ev(t) === T(q, /partners for (\d+)\./), as1_select_sum: (q, t) => ev(t) === T(q, /that make (\d+)\./), as2_select_difference: (q, t) => ev(t) === T(q, /that equal (\d+)\./),
  as3_select_three_sum: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  as4_select_family: (q, t) => { const m = g(/family for (\d+), (\d+) and (\d+)\./, q.prompt), e = /^(\d+) ([+−]) (\d+) = (\d+)$/.exec(t); return [e[1], e[3], e[4]].map(Number).sort((a, b) => a - b).join() === [m[1], m[2], m[3]].map(Number).sort((a, b) => a - b).join() && ev(`${e[1]} ${e[2]} ${e[3]}`) === +e[4]; },
  wp1_select_stories_end: (q, t) => { const want = T(q, /end with (\d+) birds/); let m = /^(\d+) birds, then (\d+) more come$/.exec(t); if (m) return +m[1] + +m[2] === want; m = /^(\d+) birds, then (\d+) fly away$/.exec(t); return m[1] - m[2] === want; },
  wp2_select_parts: (q, t) => ev(t) === T(q, /has (\d+) crayons/),
  wp3_select_compare: (q, t) => { const m = /^Ben (\d+), Zoe (\d+)$/.exec(t); return m[2] - m[1] === T(q, /has (\d+) more cars/); },
  wp4_select_equations: (q, t) => { const m = g(/^Some birds were on a tree\. (\d+) more came\. Now there are (\d+)\./, q.prompt), b = +m[1], tot = +m[2], s = tot - b; const r = t.replace('___', String(s)), e = /^(\d+) ([+−]) (\d+) = (\d+)$/.exec(r); return !!e && ev(`${e[1]} ${e[2]} ${e[3]}`) === +e[4]; },
  wp5_select_three_parts: (q, t) => { const m = /^(\d+) red, (\d+) blue, (\d+) green$/.exec(t); return +m[1] + +m[2] + +m[3] === T(q, /has (\d+) beads/); },
  eq1_select_true: (q, t) => { const [l, r] = t.split(' = '); return ev(l) === ev(r); },
  eq2_select_missing_is: (q, t) => { const x = T(q, /missing number is (\d+)\./); return ev(t.split(' = ')[0].replace('___', String(x))) === +t.split(' = ')[1]; },
  eq3_select_balance: (q, t) => ev(t) === T(q, /balance is (\d+)\./),
  cn1_select_same_count: (q, t) => tensOnes(t) === T(q, /show (\d+) crayons/),
  cn2_select_between: (q, t) => { const a = T(q, /count on from (\d+) to/); return +t > a && +t <= a + 9; },
  cn3_select_names: (q, t) => { const v = T(q, /name (\d+)\./); if (/^\d+$/.test(t)) return +t === v; let m = /^(\w+)-(\w+)$/.exec(t); if (m) return W[m[1]] + W[m[2]] === v; if (/tens/.test(t)) return tensOnes(t) === v; return ev(t) === v; },
  cn4_select_count_to: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  to1_select_tens: (q, t) => (/^\d+$/.test(t) ? +t : tensOnes(t)) === 10 * T(q, /equal to (\d+) tens/),
  to2_select_teen: (q, t) => +t >= 11 && +t <= 19,
  to3_select_tens_count: (q, t) => { const s = T(q, /tens from (\d+)\./); return +t > s && (+t - s) % 10 === 0; },
  to4_select_tens_digit: (q, t) => Math.floor(+t / 10) === T(q, /have (\d+) tens/),
  cm1_select_greater: (q, t) => +t > T(q, /greater than (\d+)\./), cm2_select_true_compare: (q, t) => { const m = /^(\d+) ([<>]) (\d+)$/.exec(t); return m[2] === '>' ? +m[1] > +m[3] : +m[1] < +m[3]; },
  cm3_select_digit_greater: (q, t) => +t > T(q, /greater than (\d+)\./),
  ah1_select_equals: (q, t) => { const want = T(q, /equal (\d+)\./); let m = /^10 (more|less) than (\d+)$/.exec(t); if (m) return (m[1] === 'more' ? +m[2] + 10 : m[2] - 10) === want; m = /^1 more than (\d+)$/.exec(t); if (m) return +m[1] + 1 === want; return ev(t) === want; },
  ah2_select_tens: (q, t) => ev(t) === T(q, /equal (\d+)\./), ah3_select_sum: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  ah4_select_new_ten: (q, t) => { const [a, b] = t.split(' + ').map(Number); return a % 10 + b >= 10; }, ah5_select_sum: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  ml1_select_longer: (q, t) => +t.split(' ')[0] > T(q, /pencil is (\d+) cubes/),
  ml2_select_indirect: (q, t) => ['the ruler is longer than the pencil', 'the pencil is shorter than the ruler', 'the marker is longer than the pencil', 'the ruler is longer than the marker'].includes(t),
  sh1_select_square: (q, t) => ['4 straight sides', '4 square corners', 'sides that are all the same length', 'a closed shape'].includes(t),
  sh2_select_3d: (q, t) => ['cube', 'cone', 'cylinder', 'sphere', 'rectangular prism'].includes(t),
  sh3_select_compose: (q, t) => ['two triangles make a square', 'two squares make a rectangle', 'two half-circles make a circle', 'four squares make a bigger square'].includes(t),
  sh4_select_shares: (q, t) => ['2 equal shares are halves', '4 equal shares are fourths', 'one of 2 equal shares is one half', 'one of 4 equal shares is one fourth'].includes(t),
  sh5_select_bigger_share: (q, t) => ['one half is bigger than one fourth of the same pie', 'two fourths make one half', 'two halves make a whole', 'four fourths make a whole'].includes(t),
  tt1_select_hour: (q, t) => { const h = T(q, /show (\d+) o'clock/); return [`${h}:00`, `${h} o'clock`, `the short hand points to ${h}, the long hand to 12`].includes(t); },
  tt3_select_half_past: (q, t) => { const h = T(q, /same time as (\d+):30/); return [`${h}:30`, `half past ${h}`, `30 minutes after ${h}:00`, `30 minutes before ${h + 1}:00`].includes(t); },
  dt1_select_tally: (q, t) => { const want = T(q, /show (\d+)\./); let v = 0; for (const m of t.matchAll(/(\d+) (bundles? of 5|bundles? of 10|marks|single marks|more)/g)) v += m[1] * (/of 5/.test(m[2]) ? 5 : /of 10/.test(m[2]) ? 10 : 1); return v === want; },
  dt2_select_graph_true: (q, t) => { const v = {}; for (const m of q.prompt.matchAll(/(dogs|cats|fish) (\d+)/g)) v[m[1]] = +m[2]; let m = /^(\w+) has more than (\w+)$/.exec(t); if (m) return v[m[1]] > v[m[2]]; m = /^(\w+) and (\w+) have (\d+) together$/.exec(t); return v[m[1]] + v[m[2]] === +m[3]; }
};
const corr = {};
for (const q of S8) {
  const k = q.options.filter((o) => o.correct).length; corr[k] = (corr[k] || 0) + 1;
  check(q, k >= 2 && k <= 4 && q.options.length === 5, 'select-all shape');
  check(q, JSON.stringify(q.answer) === JSON.stringify(q.options.filter((o) => o.correct).map((o) => o.text)), 'answer lists the correct choices');
  const fn = SEL[fam(q)];
  check(q, !!fn, 'no select-all recomputation for ' + fam(q));
  if (fn) for (const o of q.options) { let v; try { v = !!fn(q, o.text); } catch (e) { v = 'error ' + e.message; } check(q, v === o.correct, `choice ${o.text}: marked ${o.correct}, recomputed ${v}`); }
}
check(null, corr[2] && corr[3] && corr[4], 'select-all correct counts vary: ' + JSON.stringify(corr));

/* ---------- small fixes #11 #13 ---------- */
check(null, !Q.some((q) => (q.standards || []).includes('3.MD.A.1')), '3.MD.A.1 removed');
{
  const k = {}; for (const q of Q) { const key = [q.skillId, q.level, q.prompt, JSON.stringify(q.answer), JSON.stringify(q.diagram || null), JSON.stringify(q.options || null)].join('|'); k[key] = (k[key] || 0) + 1; }
  check(null, Object.values(k).every((v) => v === 1), 'no duplicate items');
}

/* ---------- both bank copies, players, standards map, card, pacing ---------- */
const nById = Object.fromEntries(N.map((q) => [q.id, q]));
for (const q of Q) {
  if (q.format === 'plot') { check(q, !nById[q.id], 'plot item in the Grade 1 players'); continue; }
  const x = nById[q.id];
  check(q, !!x, 'missing from the Grade 1 player bank');
  if (x) for (const k of ['prompt', 'answer', 'options', 'parts', 'level', 'standards', 'solutionSteps']) check(q, JSON.stringify(x[k]) === JSON.stringify(q[k]), 'copies differ in ' + k);
}
const meta = {};
for (const u of UNITS) Object.assign(meta, JSON.parse(fs.readFileSync(path.join(OUT, 'grade1/question-banks/math1/meta', u + '.meta.json'), 'utf8')));
for (const q of [...A1, ...S7, ...O4, ...S8]) check(q, !!meta[q.id], 'player metadata');
for (const q of [...A1, ...S7]) if (meta[q.id] && meta[q.id].distractors) check(q, !Object.keys(meta[q.id].distractors).includes(String(q.answer)), 'a distractor equals the key');
{
  const G = { document: {}, location: { search: '', pathname: '/x' }, MK_ELEMENTARY: { course: 'math1' }, URLSearchParams, Math, JSON, console }; G.window = G;
  vm.createContext(G); vm.runInContext(fs.readFileSync(path.join(OUT, 'grade1/worksheet-generator/elementary/el-core.js'), 'utf8'), G);
  const K = G.MKEL;
  const cases = [['3 8', '3 tens and 8 ones', '', true], ['3 tens 8 ones', '3 tens and 8 ones', '', true], ['3 tens, 8 ones', '3 tens and 8 ones', '', true], ['1 ten 6 ones', '1 ten and 6 ones', '', true],
    ['8 3', '3 tens and 8 ones', '', false], ['half past 3', '3:30', '', true], ["3 o'clock", '3:00', '', true], ['3 oclock', '3:00', '', true], ['half past 4', '3:30', '', false], ['3:30 pm', '3:30', '', true],
    ['T', 'true', '', true], ['yes', 'true', '', true], ['F', 'false', '', true], ['no', 'true', '', false], ['6 in', '6 inches', '', true], ['less than', '<', '', true], ['7 14 21', '7, 14, 21', '', true], ['one-half', 'one half', '', true], ['5', '5 cubes', '', true]];
  for (const [t, k, p, want] of cases) check({ id: 'checker' }, K.checkAnswer(t, k, p) === want, `${t} vs ${k}`);
  for (const q of N) {
    if (q.format === 'short-answer') check(q, K.checkAnswer(String(q.answer), String(q.answer), q.prompt), 'key not accepted by the checker');
    if (q.format === 'open-response') for (const p of q.parts) check(q, K.selfCheck(p) || K.checkAnswer(String(p.answer), String(p.answer), p.prompt + ' ' + q.prompt), 'part key not accepted: ' + p.answer);
  }
  const kid = require(path.join(OUT, 'worksheet-generator/core/elementary/kid-ui/kid-ui.js'));
  for (const q of N) if (q.format === 'short-answer' && kid.kind(q.answer) === 'tens-ones') { const m = /^(\d+) tens? and (\d+) ones?$/.exec(q.answer); check(q, K.checkAnswer(`${m[1]} ${m[2]}`, q.answer, q.prompt), 'pad answer for tens and ones'); }
  check(null, kid.kind('3 tens and 8 ones') === 'tens-ones' && /space/.test(kid.hint('3 tens and 8 ones', 1)), 'tens-and-ones pad and hint');
  const uc = fs.readFileSync(path.join(OUT, 'grade1/worksheet-generator/elementary/el-understanding-check.js'), 'utf8');
  check(null, /K\.checkAnswer\(inp\.value, p\.answer, p\.prompt\)/.test(uc) && /K\.selfCheck\(p\.parts\[i\]\)/.test(uc) && /The mistake: the student/.test(uc), 'Understanding Check uses the new checker');
  for (const page of ['grade1-games.html', 'grade1-understanding-check.html']) check(null, /el-core\.js\?v=g1-audit-20261119/.test(fs.readFileSync(path.join(OUT, 'grade1/worksheet-generator', page), 'utf8')), page + ' versioned');
}
{
  const s = fs.readFileSync(path.join(OUT, 'grade1-main-catalog.js'), 'utf8');
  const w = {}; w.window = w; w.globalThis = w; vm.createContext(w);
  vm.runInContext(s.slice(s.indexOf('/* Grade 1 audit 2026-11-19 */')), w);
  let mapped = 0; for (const sk of skills) { const set = 'grade1-' + sk.replace(/-skill-\d+$/, ''); if ((w.MKSTD_SKILLS[set] || {})[sk] && w.MKSTD_SKILLS[set][sk].length) mapped++; }
  check(null, mapped === 47, 'standards map covers ' + mapped + ' of 47 skills');
  check(null, new RegExp(`"approved":"47 skills · ${Q.length.toLocaleString('en-US')} verified questions`).test(s), 'course card count ' + Q.length);
}
{
  const p = path.join(OUT, 'grade-1-pacing/index.html');
  check(null, fs.existsSync(p), 'pacing page');
  if (fs.existsSync(p)) {
    const h = fs.readFileSync(p, 'utf8');
    check(null, /(\d+) of \1 standards have question-bank practice/.test(h) && /Grade 2 preview/.test(h) && /canonical" href="https:\/\/mrksclassroom\.com\/grade-1-pacing\/"/.test(h) && !/MCAS|6th Grade|Grade 6/.test(h), 'pacing page content');
    check(null, /Final review and exam<\/strong> \(days \d+–180\)/.test(h), 'pacing page reaches day 180');
  }
}
/* ---------- #15 picture graphs and bar graphs ---------- */
{
  const ctx = {}; vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(OUT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
  const P = ctx.MK_PLOT, plots = Q.filter((q) => /\(#15, Graphing Practice\)/.test(q.sourceNotes || ''));
  check(null, plots.length === 18, 'plot items ' + plots.length);
  for (const q of plots) {
    check(q, P.valid(q.plot) && P.check(q.plot, q.plot.testVectors.correct).ok && fs.existsSync(path.join(OUT, q.plot.answerKey.src)), 'plot item valid with an answer key');
    check(q, JSON.stringify(q.plot.target.values) === JSON.stringify(q.plot.source.counts), 'plot target matches the tally');
  }
}

if (fails.length) { console.error(fails.length + ' failures:\n' + fails.slice(0, 60).join('\n')); process.exit(1); }
console.log(`PASS 1st Grade Math audit (${checks} checks, ${A1.length} Advanced and ${S7.length} Standard rewrites, ${O4.length} open-response, ${S8.length} select-all items)`);
