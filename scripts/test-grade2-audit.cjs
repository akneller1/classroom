#!/usr/bin/env node
/* 2nd Grade Math audit (2026-11-19): checks on the assembled site after scripts/apply-grade2-audit.mjs.
   Every new or rewritten item's answer is recomputed here from its prompt, independently of the authoring scripts in
   tools/grade2-audit-20261119. Usage: node scripts/test-grade3-audit.cjs [_site] */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict');
const OUT = path.resolve(process.argv[2] || '_site');
const UNITS = fs.readdirSync(path.join(OUT, 'question-banks/grade2')).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', ''));
const Q = [], N = [];
for (const u of UNITS) {
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'question-banks/grade2', u + '.json'), 'utf8')).questions) Q.push(Object.assign({ unit: u }, q));
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'grade2/question-banks/math2', u + '.json'), 'utf8')).questions) N.push(Object.assign({ unit: u }, q));
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
const SH = { triangle: 3, quadrilateral: 4, pentagon: 5, hexagon: 6 };
const COIN = { quarter: 25, quarters: 25, dime: 10, dimes: 10, nickel: 5, nickels: 5, penny: 1, pennies: 1 };
const coins = (s) => [...s.matchAll(/(\d+) (quarters?|dimes?|nickels?|penny|pennies)/g)].reduce((a, m) => a + m[1] * COIN[m[2]], 0);
const bills = (s) => [...s.matchAll(/(\d+) \$(\d+) bills?/g)].reduce((a, m) => a + m[1] * m[2], 0);
const ampm = (h, m, x) => { const H = h + x; return `${(H - 1) % 12 + 1}:${String(m).padStart(2, '0')} ${H < 12 ? 'AM' : 'PM'}`; };

/* ---------- recomputation of the #1 Advanced and #7 Standard families ---------- */
const RC = {
  af1_add_then_more: (p) => { const m = g(/Add (\d+) \+ (\d+)\. Then add (\d+) more/, p); return n(+m[1] + +m[2] + +m[3]); },
  af1_two_kids_total_compare: (p) => { const m = g(/has (\d+) (\w+)\. \w+ has (\d+) \w+\. They put them together, then give away (\d+)/, p); return qty(+m[1] + +m[3] - m[4], m[2]); },
  af2_subtract_twice: (p) => { const m = g(/Subtract (\d+) − (\d+)\. Then take away (\d+) more/, p); return n(m[1] - m[2] - m[3]); },
  af2_how_many_more_after: (p) => { const m = g(/had (\d+) crayons and gave (\d+) to a friend/, p); return qty(20 - (m[1] - m[2]), 'crayons'); },
  af3_fact_family_two: (p) => { const m = g(/^(\d+) \+ (\d+) = (\d+)\./, p); return `${m[2]}; ${m[1]}`; },
  af3_which_not_in_family: (p) => { const m = g(/for (\d+), (\d+) and (\d+)\?/, p), a = +m[1], b = +m[2]; return a > b ? `${a} − ${b} = ${a + b}` : `${b} − ${a} = ${a + b}`; },
  af4_missing_both_sides: (p) => { const m = g(/(\d+) \+ (\d+) = (\d+) \+ ___/, p); return n(+m[1] + +m[2] - m[3]); },
  af4_missing_subtract_both: (p) => { const m = g(/(\d+) − (\d+) = (\d+) \+ ___/, p); return n(m[1] - m[2] - m[3]); },
  ah1_add_then_more: (p) => { const m = g(/Add (\d+) \+ (\d+)\. Then add (\d+)\./, p); return n(+m[1] + +m[2] + +m[3]); },
  ah1_sum_then_to_100: (p) => { const m = g(/scored (\d+) points and \w+ scored (\d+) points/, p); return qty(100 - m[1] - m[2], 'points'); },
  ah2_subtract_then_more: (p) => { const m = g(/Subtract (\d+) − (\d+)\. Then subtract (\d+)\./, p); return n(m[1] - m[2] - m[3]); },
  ah2_two_take_aways: (p) => { const m = g(/has (\d+) crayons\. \w+ takes (\d+) and \w+ takes (\d+)/, p); return qty(m[1] - m[2] - m[3], 'crayons'); },
  ah3_missing_then_check: (p) => { const m = g(/(\d+) \+ ___ = (\d+)\./, p); return n(m[2] - m[1]); },
  ah3_missing_start: (p) => { const m = g(/___ − (\d+) = (\d+)/, p); return n(+m[1] + +m[2]); },
  ah4_three_then_take: (p) => { const m = g(/Add (\d+) \+ (\d+) \+ (\d+)\. Then subtract (\d+)/, p); return n(+m[1] + +m[2] + +m[3] - m[4]); },
  ah4_four_addends_story: (p) => { const m = g(/collected (\d+) cans on Monday, (\d+) on Tuesday, (\d+) on Wednesday and (\d+) on Thursday/, p); return qty(+m[1] + +m[2] + +m[3] + +m[4], 'cans'); },
  ah5_break_apart: (p) => { const m = g(/Add (\d+) \+ (\d+) by adding (\d+) first/, p); return `${+m[1] + +m[3]}; ${+m[1] + +m[2]}`; },
  ah5_compensate: (p) => { const m = g(/To find (\d+) \+ (\d+), \w+ adds (\d+) \+ (\d+) instead/, p); return `${+m[1] + +m[2] === +m[3] + +m[4] ? 'yes' : 'no'}; ${+m[1] + +m[2]}`; },
  wp2_groups_then_more: (p) => { const m = g(/There are (\d+) boys and (\d+) girls in the club\. Then (\d+) more/, p); return qty(+m[1] + +m[2] + +m[3], 'children'); },
  wp2_part_unknown_two_step: (p) => { const m = g(/has (\d+) apples\. (\d+) are red, (\d+) are yellow/, p); return qty(m[1] - m[2] - m[3], 'apples'); },
  wp4_on_then_off: (p) => { const m = g(/had (\d+) people\. At the first stop, (\d+) people got on\. At the next stop, (\d+) people got off/, p); return qty(+m[1] + +m[2] - m[3], 'people'); },
  wp4_start_unknown: (p) => { const m = g(/got (\d+) more and then gave away (\d+)\. Now \w+ has (\d+) stickers/, p); return qty(+m[3] + +m[2] - m[1], 'stickers'); },
  pv1_tens_then_hundreds: (p) => { const v = +g(/How many tens are in (\d+)\?/, p)[1]; return `${v / 10}; ${Math.floor(v / 100)}`; },
  pv1_regroup_tens: (p) => { const m = g(/has (\d+) hundreds and (\d+) tens/, p); return n(m[1] * 100 + m[2] * 10); },
  pv2_build_then_more: (p) => { const m = g(/with (\d+) hundreds, (\d+) tens and (\d+) ones\. Then add (\d+)/, p); return n(m[1] * 100 + m[2] * 10 + +m[3] + +m[4]); },
  pv2_regroup_ones: (p) => { const m = g(/has (\d+) hundreds, (\d+) tens and (\d+) ones/, p); return n(m[1] * 100 + m[2] * 10 + +m[3]); },
  pv3_count_hundreds_then: (p) => { const m = g(/Start at (\d+) and count by hundreds (\d+) times/, p); return n(+m[1] + 100 * m[2] - 10); },
  pv3_hundreds_between: (p) => { const m = g(/from (\d+) to (\d+)\?/, p); return n((m[2] - m[1]) / 100); },
  pv4_expanded_then_value: (p) => { const m = g(/value of the (\d) in (\d+)\?/, p), s = m[2]; return n(+m[1] * 10 ** (s.length - 1 - s.indexOf(m[1]))); },
  pv4_mixed_order_expanded: (p) => n(g(/What number is (.+)\?/, p)[1].split(' + ').reduce((a, x) => a + +x, 0)),
  cc1_count_on_k: (p) => { const m = g(/Start at (\d+)\. Count on (\d+) more/, p); return n(+m[1] + +m[2]); },
  cc1_count_over_hundred: (p) => { const m = g(/Count on (\d+) by ones from (\d+)/, p); return n(+m[1] + +m[2]); },
  cc2_skip_k_times: (p) => { const m = g(/Skip count by (\d+)s (\d+) times, starting at (\d+)/, p); return n(+m[3] + m[1] * m[2]); },
  cc2_jumps_between: (p) => { const m = g(/jumps of (\d+) .* from (\d+) to (\d+)/, p); return n((m[3] - m[2]) / m[1]); },
  cc3_order_three: (p) => g(/least to greatest: (.*)$/, p)[1].split(', ').map(Number).sort((a, b) => a - b).join(', '),
  cc3_compare_after_change: (p) => { const m = g(/Compare (\d+) \+ (\d+) ___ (\d+)/, p), v = +m[1] + +m[2]; return v > +m[3] ? '>' : v < +m[3] ? '<' : '='; },
  cc3_greatest_same_hundreds: (p) => { const m = g(/the (greatest|least): (.*)\?/, p), xs = m[2].split(', ').map(Number); return String(m[1] === 'greatest' ? Math.max(...xs) : Math.min(...xs)); },
  cc4_two_changes: (p) => { const m = g(/Start at (\d+)\. Add (\d+), then subtract (\d+)/, p); return n(+m[1] + +m[2] - m[3]); },
  cc4_backward_change: (p) => { const m = g(/is (\d+) × (\d+) more .* The bigger number is (\d+)/, p); return n(m[3] - m[1] * m[2]); },
  at1_hundreds_tens_ones_jumps: (p) => { const m = g(/Start at (\d+)\. Add (\d+), then add (\d+), then add (\d+)\. Then add 10 more/, p); return n(+m[1] + +m[2] + +m[3] + +m[4] + 10); },
  at1_three_three_digit: (p) => { const m = g(/Add (\d+) \+ (\d+) \+ (\d+)\./, p); return n(+m[1] + +m[2] + +m[3]); },
  at2_regroup_then_more: (p) => { const m = g(/sold (\d+) pencils in May and (\d+) pencils in June\. In July it sold (\d+)/, p); return qty(+m[1] + +m[2] + +m[3], 'pencils'); },
  at2_new_ten_and_hundred: (p) => { const m = g(/Add (\d+) \+ (\d+)\./, p); return String(Math.floor((+m[1] + +m[2]) / 100)); },
  at3_subtract_then_add: (p) => { const m = g(/Subtract (\d+) − (\d+)\. Then add (\d+)/, p); return n(m[1] - m[2] + +m[3]); },
  at3_count_up_difference: (p) => { const m = g(/find (\d+) − (\d+)\. First count up to (\d+)/, p); return `${m[3] - m[2]}; ${m[1] - m[2]}`; },
  at4_regroup_then_less: (p) => { const m = g(/Subtract (\d+) − (\d+)\. Then subtract (\d+) more/, p); return n(m[1] - m[2] - m[3]); },
  at4_across_zeros_two: (p) => { const m = g(/has (\d+) stickers\. It gives (\d+) to one class and (\d+) to another/, p); return qty(m[1] - m[2] - m[3], 'stickers'); },
  oe1_sum_odd_even: (p) => { const m = g(/Find (\d+) \+ (\d+)\./, p); return (+m[1] + +m[2]) % 2 ? 'odd' : 'even'; },
  oe1_count_even_between: (p) => { const m = g(/from (\d+) to (\d+)\?/, p); let c = 0; for (let x = +m[1]; x <= +m[2]; x++) if (x % 2 === 0) c++; return n(c); },
  oe2_double_then_even: (p) => n(+g(/Write (\d+) as a sum/, p)[1] / 2),
  oe2_doubles_plus: (p) => { const m = g(/has (\d+) \+ (\d+) \+ (\d+) blocks/, p), v = +m[1] + +m[2] + +m[3]; return `${v}; ${v % 2 ? 'odd' : 'even'}`; },
  oe3_array_plus_dots: (p) => { const m = g(/has (\d+) rows of (\d+) dots\. (\d+) more/, p); return qty(m[1] * m[2] + +m[3], 'dots'); },
  oe3_two_arrays_compare: (p) => { const m = g(/A has (\d+) rows of (\d+)\. Array B has (\d+) rows of (\d+)/, p); return n(Math.abs(m[1] * m[2] - m[3] * m[4])); },
  oe4_seats_minus: (p) => { const m = g(/has (\d+) rows of seats with (\d+) seats in each row\. (\d+) children/, p); return qty(m[1] * m[2] - m[3], 'seats'); },
  oe4_add_rows: (p) => { const m = g(/has (\d+) rows with (\d+) plants in each row\. (\d+) more/, p); return qty((+m[1] + +m[3]) * m[2], 'plants'); },
  ml3_meters_to_cm_plus: (p) => { const m = g(/is (\d+) meters long\. .* (\d+) centimeters longer/, p); return qty(m[1] * 100 + +m[2], 'centimeters'); },
  ml3_feet_to_inches: (p) => qty(12 * g(/is (\d+) feet long/, p)[1], 'inches'),
  ml4_estimate_then_compare: (p) => { const m = g(/pencil is about (\d+) paper clips long and a crayon is about (\d+)/, p); return qty(m[1] - m[2], 'inches'); },
  ml4_steps_two_rooms: (p) => { const m = g(/hallway is about (\d+) steps long and a classroom is about (\d+)/, p); return qty(+m[1] + +m[2], 'meters'); },
  ml5_longer_then_double: (p) => { const m = g(/is (\d+) (\w+) long\. A string is (\d+) \w+ long/, p); return `${m[1] - m[3]} ${m[2]}; ${+m[1] + +m[3]} ${m[2]}`; },
  ml5_cut_two_pieces: (p) => { const m = g(/is (\d+) inches long\. \w+ cuts off (\d+) inches and then (\d+) inches/, p); return qty(m[1] - m[2] - m[3], 'inches'); },
  ln1_three_parts: (p) => { const m = g(/They are (\d+) meters, (\d+) meters and (\d+) meters/, p); return qty(+m[1] + +m[2] + +m[3], 'meters'); },
  ln1_missing_part: (p) => { const m = g(/is (\d+) feet long\. .* Two parts are (\d+) feet and (\d+) feet/, p); return qty(m[1] - m[2] - m[3], 'feet'); },
  ln2_from_to: (p) => { const m = g(/starts at (\d+) on the number line and ends at (\d+)/, p); return qty(m[2] - m[1], 'units'); },
  ln2_end_from_start: (p) => { const m = g(/is (\d+) units long and starts at (\d+)/, p); return `${+m[1] + +m[2]}; ${+m[1] + +m[2] + 10}`; },
  ln3_two_jumps: (p) => { const m = g(/Start at (\d+) on a number line\. Jump forward (\d+), then jump back (\d+)/, p); return n(+m[1] + +m[2] - m[3]); },
  ln3_jump_size: (p) => n(+g(/Start at (\d+) and make one jump/, p)[1]),
  tm1_minute_hand_later: (p) => { const m = g(/points to the (\d+)\. .* (\d+) minutes later/, p); return `${m[1] * 5} minutes; ${m[1] * 5 + +m[2]} minutes`; },
  tm1_time_later: (p) => { const m = g(/shows (\d+:\d+)\. What time will it show (\d+) minutes later/, p); return tm(tmin(m[1]) + +m[2]); },
  tm2_am_hours_later: (p) => { const m = g(/starts at (\d+):(\d+) AM\. Lunch is (\d+) hours? later/, p); return ampm(+m[1], +m[2], +m[3]); },
  tm2_am_to_pm_hours: (p) => { const m = g(/at (\d+):00 AM and eats dinner at (\d+):00 PM/, p); return qty(12 - m[1] + +m[2], 'hours'); },
  tm3_count_then_add: (p) => { const m = g(/has (.*)\. Then finds (\d+)¢ more/, p); return `${coins(m[1]) + +m[2]}¢`; },
  tm3_more_to_dollar: (p) => `${100 - coins(g(/has (.*)\. How many more/, p)[1])}¢`,
  tm4_bills_minus_cost: (p) => { const m = g(/has (.*)\. A game costs \$(\d+)/, p); return `$${bills(m[1]) - m[2]}`; },
  sh1_sides_two_shapes: (p) => { const m = g(/do an? (\w+) and an? (\w+) have/, p); return n(SH[m[1]] + SH[m[2]]); },
  sh1_angles_many: (p) => { const m = g(/do (\d+) (\w+)s have/, p); return n(m[1] * SH[m[2]]); },
  sh2_draw_name_angles: (p) => { const k = +g(/with (\d+) straight sides/, p)[1]; return `${Object.keys(SH).find((x) => SH[x] === k)}; ${k}`; },
  sh2_more_sides: (p) => { const m = g(/draws an? (\w+) and \w+ draws an? (\w+)\./, p); return n(Math.abs(SH[m[1]] - SH[m[2]])); },
  sh3_faces_minus: (p) => { const m = g(/every face of (\d+) cubes\. (\d+) stickers? falls? off/, p); return qty(6 * m[1] - m[2], 'stickers'); },
  sh3_cubes_from_stickers: (p) => qty(g(/used (\d+) stickers/, p)[1] / 6, 'cubes'),
  sh4_squares_minus_shaded: (p) => { const m = g(/split into (\d+) rows of (\d+) same-size squares\. (\d+) squares/, p); return n(m[1] * m[2] - m[3]); },
  sh4_more_rows_columns: (p) => { const m = g(/has (\d+) rows of (\d+) same-size squares\. \w+ adds (\d+) more/, p); return n(m[1] * (+m[2] + +m[3])); }
};
const A1 = Q.filter((q) => /\(#1, Advanced/.test(q.sourceNotes || '')), S7 = Q.filter((q) => /\(#7, Standard\)/.test(q.sourceNotes || ''));
check(null, A1.length >= 350, 'Advanced rewrites ' + A1.length);
check(null, S7.length >= 300, 'Standard rewrites ' + S7.length);
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
  check(q, !(q.prompt + ' ' + q.answer).match(/\d{4,}|\d,\d{3}/), 'number beyond 999');
}
const share = (L, lo) => { const low = new Set(Q.filter((q) => lo.includes(q.level)).map((q) => q.skillId + '|' + mask(q.prompt))); const xs = Q.filter((q) => q.level === L); return xs.filter((q) => low.has(q.skillId + '|' + mask(q.prompt))).length / xs.length; };
check(null, share('honors', ['cp2', 'cp1']) <= 0.26, 'Advanced items reusing a lower template ' + share('honors', ['cp2', 'cp1']).toFixed(2));
check(null, share('cp1', ['cp2']) <= 0.30, 'Standard items reusing a Support template ' + share('cp1', ['cp2']).toFixed(2));
const lv = (L) => Q.filter((q) => q.level === L).length;
check(null, Math.max(lv('cp2'), lv('cp1'), lv('honors')) - Math.min(lv('cp2'), lv('cp1'), lv('honors')) <= 3, `levels ${lv('cp2')}/${lv('cp1')}/${lv('honors')}`);

/* ---------- #4 open response ---------- */
const O4 = Q.filter((q) => /\(#4, open response\)/.test(q.sourceNotes || ''));
const skills = [...new Set(Q.map((q) => q.skillId))];
assert.equal(skills.length, 53);
check(null, O4.length === 159 && Q.filter((q) => q.format === 'open-response').length === 159, 'open-response items ' + O4.length);
for (const s of skills) for (const L of ['cp2', 'cp1', 'honors']) check({ id: s + '|' + L }, O4.filter((q) => q.skillId === s && q.level === L).length === 1, 'one context open-response item');
for (const q of O4) {
  check(q, q.parts.length === 4 && /^Sample answer: /.test(q.parts[3].answer) && q.solutionSteps.length === 4, 'four parts ending with an explanation');
  check(q, q.parts.slice(0, 3).some((p) => !/^Sample answer: /.test(p.answer)), 'at least one checked part');
  check(q, !/^(Answer each part|Match each problem)/.test(q.prompt), 'not the drill template');
}
const OR = {
  af1_open_apples: (q) => { const m = g(/picks (\d+) apples\. \w+ picks (\d+) apples/, q.prompt); return [0, qty(+m[1] + +m[2], 'apples')]; },
  af2_open_balloons: (q) => { const m = g(/There are (\d+) balloons\. (\d+) balloons pop/, q.prompt); return [0, qty(m[1] - m[2], 'balloons')]; },
  af3_open_fact_family: (q) => { const m = g(/has (\d+) red and (\d+) blue/, q.prompt); return [0, qty(+m[1] + +m[2], 'crayons')]; },
  af4_open_balance: (q) => { const m = g(/has (\d+) \+ (\d+) cubes on one side and (\d+) cubes/, q.prompt); return [1, qty(+m[1] + +m[2] - m[3], 'cubes')]; },
  ah1_open_cans: (q) => { const m = g(/A collected (\d+) cans\. Class B collected (\d+)/, q.prompt); return [2, qty(100 - m[1] - m[2], 'cans')]; },
  ah2_open_pages: (q) => { const m = g(/has (\d+) pages\. Mia has read (\d+)/, q.prompt); return [0, qty(m[1] - m[2], 'pages')]; },
  ah3_open_missing: (q) => { const m = g(/had (\d+) marbles\. .* he had (\d+)\./, q.prompt); return [1, qty(m[2] - m[1], 'marbles')]; },
  ah4_open_points: (q) => { const xs = g(/scored (.*) points in/, q.prompt)[1].replace(' and ', ', ').split(', ').map(Number); return [0, qty(xs.reduce((a, b) => a + b, 0), 'points')]; },
  ah5_open_strategies: (q) => { const m = g(/add (\d+) \+ (\d+) in/, q.prompt); return [1, n(+m[1] + +m[2])]; },
  wp1_open_bus: (q) => { const m = g(/has (\d+) people\. (\d+) people get on/, q.prompt), c = +g(/Then (\d+) people get off/, q.parts[1].prompt)[1]; return [1, qty(+m[1] + +m[2] - c, 'people')]; },
  wp2_open_club: (q) => { const m = g(/has (\d+) girls and (\d+) boys/, q.prompt); return [0, qty(+m[1] + +m[2], 'children')]; },
  wp3_open_compare: (q) => { const m = g(/Eli has (\d+) cards\. Lena has (\d+) more/, q.prompt); return [0, qty(+m[1] + +m[2], 'cards')]; },
  wp4_open_two_step: (q) => { const m = g(/had (\d+) stickers\. She got (\d+) more and then gave away (\d+)/, q.prompt); return [1, qty(+m[1] + +m[2] - m[3], 'stickers')]; },
  pv1_open_bundles: (q) => [0, n(10 * g(/has (\d+) bundles/, q.prompt)[1])],
  pv2_open_blocks: (q) => { const m = g(/with (\d+) hundreds, (\d+) tens and (\d+) ones/, q.prompt); return [0, n(m[1] * 100 + m[2] * 10 + +m[3])]; },
  pv3_open_count_hundreds: (q) => { const s = +g(/starting at (\d+)/, q.prompt)[1]; return [1, n((s + 300) / 100)]; },
  pv4_open_check: (q) => { const v = g(/for (\d+) dollars/, q.prompt)[1]; return [1, n(+v[1] * 10)]; },
  cc1_open_tickets: (q) => [0, n(+g(/today is (\d+)/, q.prompt)[1] + 1)],
  cc2_open_skip: (q) => { const m = g(/by (\d+)s, starting at (\d+)/, q.prompt); return [1, n(+m[2] + 6 * m[1])]; },
  cc3_open_compare: (q) => { const m = g(/Oak has (\d+) students and Pine has (\d+)/, q.prompt); return [1, +m[1] > +m[2] ? '>' : '<']; },
  cc4_open_ten_hundred: (q) => [2, n(+g(/shows (\d+) points/, q.prompt)[1] + 90)],
  at1_open_blocks: (q) => { const m = g(/adds (\d+) \+ (\d+) with/, q.prompt); return [2, n(+m[1] + +m[2])]; },
  at2_open_tickets: (q) => { const m = g(/sold (\d+) tickets on Friday and (\d+) tickets/, q.prompt); return [0, qty(+m[1] + +m[2], 'tickets')]; },
  at3_open_seats: (q) => { const m = g(/has (\d+) seats\. (\d+) seats are filled/, q.prompt); return [0, qty(m[1] - m[2], 'seats')]; },
  at4_open_zeros: (q) => { const m = g(/has (\d+) eggs\. (\d+) eggs/, q.prompt); return [0, qty(m[1] - m[2], 'eggs')]; },
  oe1_open_partners: (q) => { const k = +g(/^(\d+) children/, q.prompt)[1]; return [0, k % 2 ? 'odd' : 'even']; },
  oe2_open_doubles: (q) => [0, qty(g(/has (\d+) socks/, q.prompt)[1] / 2, 'socks')],
  oe3_open_array: (q) => { const m = g(/in (\d+) rows with (\d+) desks/, q.prompt); return [1, qty(m[1] * m[2], 'desks')]; },
  oe4_open_garden: (q) => { const m = g(/has (\d+) rows of (\d+) plants\. (\d+) plants/, q.prompt); return [1, qty(m[1] * m[2] - m[3], 'plants')]; },
  ml1_open_ruler: (q) => [0, qty(+g(/is at (\d+) inches/, q.prompt)[1], 'inches')],
  ml2_open_tool: (q) => [0, { book: 'inches', room: 'feet', hallway: 'meters' }[g(/length of a (\w+)\./, q.prompt)[1]]],
  ml3_open_two_units: (q) => [0, qty(12 * g(/is (\d+) feet long/, q.prompt)[1], 'inches')],
  ml4_open_estimate: (q) => [1, qty(2 * g(/about (\d+) paper clips long/, q.prompt)[1], 'inches')],
  ml5_open_ribbons: (q) => { const m = g(/is (\d+) centimeters long\. A blue ribbon is (\d+)/, q.prompt); return [1, qty(+m[1] + +m[2], 'centimeters')]; },
  ml6_open_line_plot: (q) => { const xs = g(/inches: (.*)\. Make/, q.prompt)[1].split(', ').map(Number); return [2, qty(Math.max(...xs) - Math.min(...xs), 'inches')]; },
  ln1_open_track: (q) => { const m = g(/runs (\d+) meters, rests, then runs (\d+) meters/, q.prompt); return [0, qty(+m[1] + +m[2], 'meters')]; },
  ln2_open_points: (q) => { const m = g(/at (\d+) on a number line\. Point B is (\d+) units/, q.prompt); return [0, n(+m[1] + +m[2])]; },
  ln3_open_jumps: (q) => { const m = g(/starts at (\d+) .* forward (\d+), then back (\d+)/, q.prompt); return [1, n(+m[1] + +m[2] - m[3])]; },
  tm1_open_clock: (q) => { const m = g(/past the (\d+) and the minute hand points to the (\d+)/, q.prompt); return [0, tm(m[1] * 60 + m[2] * 5)]; },
  tm2_open_day: (q) => [1, qty(12 - g(/wakes up at (\d+):00 AM/, q.prompt)[1], 'hours')],
  tm3_open_coins: (q) => [0, `${coins(q.prompt)}¢`],
  tm4_open_bills: (q) => [0, `$${bills(q.prompt)}`],
  tm5_open_store: (q) => { const m = g(/costs (\d+)¢ and an eraser costs (\d+)¢/, q.prompt); return [1, `${100 - m[1] - m[2]}¢`]; },
  gd1_open_picture_graph: (q) => { const m = g(/dogs (\d+), cats (\d+), fish (\d+)/, q.prompt); return [0, qty(+m[1] + +m[2] + +m[3], 'pets')]; },
  gd2_open_bar_graph: (q) => { const m = g(/apple (\d+), banana (\d+), grape (\d+)/, q.prompt); return [0, qty(+m[1] + +m[2] + +m[3], 'votes')]; },
  gd3_open_problem: (q) => { const m = g(/shows (\d+) students walk to school and (\d+) ride/, q.prompt); return [0, qty(+m[1] + +m[2], 'students')]; },
  gd4_open_make_graph: (q) => { const m = g(/red (\d+), blue (\d+), green (\d+)/, q.prompt); return [1, n(+m[1] + +m[2] + +m[3])]; },
  sh1_open_shape: (q) => { const s = g(/draws an? (\w+)\./, q.prompt)[1]; return [2, n(3 * SH[s])]; },
  sh2_open_draw: (q) => { const k = +g(/with (\d+) straight sides/, q.prompt)[1]; return [0, Object.keys(SH).find((x) => SH[x] === k)]; },
  sh3_open_cubes: (q) => [1, n(6 * g(/has (\d+) cubes/, q.prompt)[1])],
  sh4_open_squares: (q) => { const m = g(/into (\d+) rows and (\d+) columns/, q.prompt); return [0, n(m[1] * m[2])]; },
  sh5_open_pizza: (q) => [0, n({ halves: 2, thirds: 3, fourths: 4 }[g(/cut into (\w+)\./, q.prompt)[1]])],
  sh6_open_two_pizzas: (q) => [2, n({ halves: 2, thirds: 3, fourths: 4 }[g(/one is cut into (\w+) and/, q.prompt)[1]])]
};
for (const q of O4) {
  const fn = OR[fam(q)];
  check(q, !!fn, 'no open-response recomputation for ' + fam(q));
  if (!fn) continue;
  try { const [i, want] = fn(q); check(q, q.parts[i].answer === want, `part ${i}: ${q.parts[i].answer} but recomputed ${want}`); } catch (e) { check(q, false, e.message); }
}

/* ---------- #8 select-all ---------- */
const S8 = Q.filter((q) => q.format === 'select-all');
check(null, S8.length === 142 && S8.every((q) => /\(#8, select-all/.test(q.sourceNotes || '')), 'every select-all item rewritten: ' + S8.length);
const ev = (s) => { s = s.replace(/×/g, '*').replace(/−/g, '-'); if (!/^[\d\s+*()-]+$/.test(s)) throw Error('bad expression ' + s); return Function('return ' + s)(); };
const T = (q, re) => +g(re, q.prompt)[1];
const SEL = {
  af1_select_sum: (q, t) => ev(t) === T(q, /sum of (\d+)\./),
  af2_select_difference: (q, t) => ev(t) === T(q, /difference of (\d+)\./),
  af3_select_family: (q, t) => { const m = g(/family for (\d+), (\d+) and (\d+)\./, q.prompt), e = /^(\d+) ([+−]) (\d+) = (\d+)$/.exec(t), set = [m[1], m[2], m[3]].map(Number).sort((a, b) => a - b).join(); return [e[1], e[3], e[4]].map(Number).sort((a, b) => a - b).join() === set && ev(`${e[1]} ${e[2]} ${e[3]}`) === +e[4]; },
  af4_select_missing_is: (q, t) => { const x = T(q, /missing number is (\d+)\./); let m = /^(\d+) \+ ___ = (\d+)$/.exec(t); if (m) return m[2] - m[1] === x; m = /^___ \+ (\d+) = (\d+)$/.exec(t); return m[2] - m[1] === x; },
  ah1_select_sum: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  ah2_select_difference: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  ah3_select_related: (q, t) => { const e = /^(\d+) ([+−]) (\d+) = (\d+)$/.exec(t), m = g(/use (\d+), (\d+) and (\d+)\./, q.prompt); return ev(`${e[1]} ${e[2]} ${e[3]}`) === +e[4] && [e[1], e[3], e[4]].map(Number).sort((a, b) => a - b).join() === [m[1], m[2], m[3]].map(Number).sort((a, b) => a - b).join(); },
  ah4_select_three_sum: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  ah5_select_same_sum: (q, t) => { const m = g(/same sum as (\d+) \+ (\d+)\./, q.prompt); return ev(t) === +m[1] + +m[2]; },
  at1_select_sum: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  at2_select_new_ten: (q, t) => { const [a, b] = t.split(' + ').map(Number); return a % 10 + b % 10 >= 10; },
  at3_select_difference: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  at4_select_trade_ten: (q, t) => { const [a, b] = t.split(' − ').map(Number); return a % 10 < b % 10; },
  cc1_select_between: (q, t) => { const m = g(/greater than (\d+) and less than (\d+)\./, q.prompt), v = I(t); return v > +m[1] && v < +m[2]; },
  cc2_select_skip_hits: (q, t) => { const m = g(/by (\d+)s from (\d+)\./, q.prompt), v = I(t); return v > +m[2] && (v - m[2]) % m[1] === 0; },
  cc3_select_greater: (q, t) => I(t) > T(q, /greater than (\d+)\./),
  cc4_select_equals_more: (q, t) => { const m = g(/equal to (\d+) more than (\d+)\./, q.prompt); return ev(t) === +m[1] + +m[2]; },
  gd3_select_true_graph: (q, t) => { const v = {}; for (const m of q.prompt.matchAll(/(apples|bananas|grapes) (\d+)/g)) v[m[1]] = +m[2]; let m = /^(\w+) has more votes than (\w+)$/.exec(t); if (m) return v[m[1]] > v[m[2]]; m = /^(\w+) and (\w+) have (\d+) votes together$/.exec(t); return v[m[1]] + v[m[2]] === +m[3]; },
  gd4_select_bar_heights: (q, t) => { const v = {}; for (const m of q.prompt.matchAll(/(apples|bananas|grapes) (\d+)/g)) v[m[1].replace(/s$/, '').replace(/^banana$/, 'banana')] = +m[2]; let m = /^the tallest bar is (\d+) tall$/.exec(t); if (m) return Math.max(...Object.values(v)) === +m[1]; m = /^the (\w+) bar is (\d+) tall$/.exec(t); return v[m[1]] === +m[2]; },
  ln1_select_total_length: (q, t) => ev(t) === T(q, /make (\d+) meters together/),
  ln2_select_length: (q, t) => { const m = /^from (\d+) to (\d+)$/.exec(t); return m[2] - m[1] === T(q, /that are (\d+) units long/); },
  ln3_select_land_on: (q, t) => { const m = /^start at (\d+), jump (forward|back) (\d+)$/.exec(t); return (m[2] === 'forward' ? +m[1] + +m[3] : m[1] - m[3]) === T(q, /land on (\d+)\./); },
  ml1_select_measure_right: (q, t) => ['line up one end with 0', 'keep the ruler straight along the object', 'read the mark at the other end', 'count the units from 0 to the end'].includes(t),
  ml2_select_best_unit: (q, t) => ({ inches: ['pencil', 'book', 'crayon', 'shoe', 'spoon'], meters: ['soccer field', 'school hallway', 'swimming pool', 'playground', 'bus'] })[g(/measure in (\w+)\./, q.prompt)[1]].includes(t),
  ml3_select_same_length: (q, t) => { const f = T(q, /equal to (\d+) feet/); let m = /^(\d+) feet and (\d+) inches$/.exec(t); if (m) return m[1] * 12 + +m[2] === f * 12; m = /^(.+) inches$/.exec(t); if (m) return ev(m[1]) === f * 12; m = /^(\d+) feet$/.exec(t); return +m[1] === f; },
  ml5_select_difference: (q, t) => { const m = /^(\d+) cm and (\d+) cm$/.exec(t); return m[1] - m[2] === T(q, /is (\d+) centimeters longer/); },
  oe1_select_parity: (q, t) => (+t % 2 === 0) === (g(/Select ALL the (\w+) numbers/, q.prompt)[1] === 'even'),
  oe2_select_doubles: (q, t) => +t % 2 === 0,
  oe3_select_array_total: (q, t) => { const want = T(q, /show (\d+) in all/), m = /^(\d+) rows of (\d+)$/.exec(t); return (m ? m[1] * m[2] : ev(t)) === want; },
  oe4_select_rooms: (q, t) => { const want = T(q, /room with (\d+) seats/), m = /^(\d+) rows of (\d+) seats$/.exec(t); return (m ? m[1] * m[2] : ev(t)) === want; },
  pv1_select_same_number: (q, t) => { const want = T(q, /ways to make (\d+)\./); let v = 0; for (const m of t.matchAll(/(\d+) (hundreds|tens)/g)) v += m[1] * (m[2] === 'hundreds' ? 100 : 10); return v === want; },
  pv2_select_ways_to_make: (q, t) => { const want = T(q, /ways to make (\d+)\./); let v = 0; for (const m of t.matchAll(/(\d+) (hundreds|tens|ones)/g)) v += m[1] * { hundreds: 100, tens: 10, ones: 1 }[m[2]]; return v === want; },
  pv3_select_hundreds: (q, t) => I(t) % 100 === 0 && I(t) >= 100 && I(t) <= 1000,
  pv4_select_expanded: (q, t) => ev(t) === T(q, /equal (\d+)\./),
  sh1_select_sides: (q, t) => { const k = T(q, /have (\d+) sides/), N = { triangle: 3, square: 4, rectangle: 4, rhombus: 4, trapezoid: 4, quadrilateral: 4, pentagon: 5, hexagon: 6 }; const m = /(\d+) (?:angles|sides)$/.exec(t); return m ? +m[1] === k : N[t] === k; },
  sh2_select_four_angles: (q, t) => ['a square', 'a rectangle', 'a rhombus', 'a trapezoid', 'a quadrilateral'].includes(t),
  sh3_select_cube: (q, t) => ['6 faces', '12 edges', '8 vertices', 'square faces', 'all faces the same size'].includes(t),
  sh4_select_rectangle_squares: (q, t) => { const m = /^(\d+) rows of (\d+) squares$/.exec(t); return m[1] * m[2] === T(q, /split into (\d+) same-size/); },
  sh5_select_shares: (q, t) => { const name = g(/cut into (\w+)\./, q.prompt)[1], k = { halves: 2, thirds: 3, fourths: 4 }[name], one = { 2: 'one half', 3: 'one third', 4: 'one fourth' }[k]; return [`there are ${k} equal shares`, `${k} ${name} make the whole`, `each share is ${one}`, 'the shares are the same size'].includes(t); },
  sh6_select_true_shares: (q, t) => ['one half of a pizza is bigger than one fourth of the same pizza', 'two halves make one whole', 'three thirds make one whole', 'four fourths make one whole', 'one third of a pizza is bigger than one fourth of the same pizza'].includes(t),
  tm1_select_within_half_hour: (q, t) => { const t0 = tmin(g(/It is (\d+:\d+)\./, q.prompt)[1]); let d = tmin(t) - t0; if (d < -600) d += 720; return d > 0 && d < 30; },
  tm2_select_am: (q, t) => ['eating breakfast', 'waking up for school', 'the morning bus ride', 'brushing teeth before school', 'morning recess'].includes(t),
  tm3_select_coins_make: (q, t) => coins(t) === T(q, /make (\d+)¢/),
  tm4_select_bills_make: (q, t) => bills(t) === T(q, /make \$(\d+)\./),
  tm5_select_can_buy: (q, t) => { const m = /^a (\d+)¢ toy and a (\d+)¢ toy$/.exec(t); return +m[1] + +m[2] <= T(q, /has (\d+)¢/); },
  wp1_select_stories_end: (q, t) => { const want = T(q, /end with (\d+) birds/); let m = /^(\d+) birds, then (\d+) more come$/.exec(t); if (m) return +m[1] + +m[2] === want; m = /^(\d+) birds, then (\d+) fly away$/.exec(t); return m[1] - m[2] === want; },
  wp2_select_parts_whole: (q, t) => ev(t) === T(q, /has (\d+) children/),
  wp3_select_compare: (q, t) => { const m = /^Eli (\d+), Lena (\d+)$/.exec(t); return m[2] - m[1] === T(q, /has (\d+) more cards/); }
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

/* ---------- small fixes #10 #17 ---------- */
for (const q of Q) {
  const txt = [q.prompt, Array.isArray(q.answer) ? q.answer.join(' ') : q.answer, ...(q.options || []).map((o) => o.text), ...(q.parts || []).map((p) => p.prompt + ' ' + p.answer), ...(q.solutionSteps || [])].join(' | ');
  check(q, !/straight (angles|corners)/.test(txt), 'straight angles');
  check(q, !/(?<![\d/,.$])1 (pets|shells|cubes)\b/.test(txt), 'plural after 1');
}

/* ---------- both bank copies, players, standards map, card, pacing ---------- */
const nById = Object.fromEntries(N.map((q) => [q.id, q]));
for (const q of Q) {
  if (q.format === 'plot') { check(q, !nById[q.id], 'plot item in the Grade 2 players'); continue; }
  const x = nById[q.id];
  check(q, !!x, 'missing from the Grade 2 player bank');
  if (x) for (const k of ['prompt', 'answer', 'options', 'parts', 'level', 'standards', 'solutionSteps']) check(q, JSON.stringify(x[k]) === JSON.stringify(q[k]), 'copies differ in ' + k);
}
const meta = {};
for (const u of UNITS) Object.assign(meta, JSON.parse(fs.readFileSync(path.join(OUT, 'grade2/question-banks/math2/meta', u + '.meta.json'), 'utf8')));
for (const q of [...A1, ...S7, ...O4, ...S8]) check(q, !!meta[q.id], 'player metadata');
for (const q of [...A1, ...S7]) if (meta[q.id] && meta[q.id].distractors) check(q, !Object.keys(meta[q.id].distractors).includes(String(q.answer)), 'a distractor equals the key');
{
  const G = { document: {}, location: { search: '', pathname: '/x' }, MK_ELEMENTARY: { course: 'math2' }, URLSearchParams, Math, JSON, console }; G.window = G;
  vm.createContext(G); vm.runInContext(fs.readFileSync(path.join(OUT, 'grade2/worksheet-generator/elementary/el-core.js'), 'utf8'), G);
  const K = G.MKEL;
  const cases = [['6 ft', '6 feet', '', true], ['6 in', '6 inches', '', true], ['5 cm', '5 centimeters', '', true], ['less than', '<', '', true], ['greater', '>', '', true],
    ['3:30 pm', '3:30', '', true], ['7 14 21', '7, 14, 21', '', true], ['one-third', 'one third', '', true], ['45 cents', '45¢', '', true], ['45', '45¢', '', true], ['$0.45', '45¢', '', true],
    ['$1.25', '$1 and 25¢', '', true], ['125¢', '$1 and 25¢', '', true], ['1 dollar 25 cents', '$1 and 25¢', '', true], ['1 dollar and 25 cents', '$1 and 25¢', '', true],
    ['8 dollars', '$8', '', true], ['$8.00', '$8', '', true], ['$1.30', '$1 and 25¢', '', false], ['35¢', '45¢', '', false], ['3 ft', '3 inches', '', false]];
  for (const [t, k, p, want] of cases) check({ id: 'checker' }, K.checkAnswer(t, k, p) === want, `${t} vs ${k}`);
  for (const q of N) {
    if (q.format === 'short-answer') check(q, K.checkAnswer(String(q.answer), String(q.answer), q.prompt), 'key not accepted by the checker');
    if (q.format === 'open-response') for (const p of q.parts) check(q, K.selfCheck(p) || K.checkAnswer(String(p.answer), String(p.answer), p.prompt + ' ' + q.prompt), 'part key not accepted: ' + p.answer);
  }
  const uc = fs.readFileSync(path.join(OUT, 'grade2/worksheet-generator/elementary/el-understanding-check.js'), 'utf8');
  check(null, /K\.checkAnswer\(inp\.value, p\.answer, p\.prompt\)/.test(uc) && /K\.selfCheck\(p\.parts\[i\]\)/.test(uc) && /The mistake: the student/.test(uc), 'Understanding Check uses the new checker');
  for (const page of ['grade2-games.html', 'grade2-understanding-check.html']) check(null, /el-core\.js\?v=g2-audit-20261119/.test(fs.readFileSync(path.join(OUT, 'grade2/worksheet-generator', page), 'utf8')), page + ' versioned');
}
{
  const s = fs.readFileSync(path.join(OUT, 'grade2-main-catalog.js'), 'utf8');
  const w = {}; w.window = w; w.globalThis = w; vm.createContext(w);
  vm.runInContext(s.slice(s.indexOf('/* Grade 2 audit 2026-11-19 */')), w);
  let mapped = 0; for (const sk of skills) { const set = 'grade2-' + sk.replace(/-skill-\d+$/, ''); if ((w.MKSTD_SKILLS[set] || {})[sk] && w.MKSTD_SKILLS[set][sk].length) mapped++; }
  check(null, mapped === 53, 'standards map covers ' + mapped + ' of 53 skills');
  check(null, s.includes(`"approved":"53 skills · ${Q.length.toLocaleString('en-US')} verified questions`), 'course card count ' + Q.length);
}
{
  const p = path.join(OUT, 'grade-2-pacing/index.html');
  check(null, fs.existsSync(p), 'pacing page');
  if (fs.existsSync(p)) {
    const h = fs.readFileSync(p, 'utf8');
    check(null, /(\d+) of \1 standards have question-bank practice/.test(h) && /Grade 3 preview/.test(h) && /canonical" href="https:\/\/mrksclassroom\.com\/grade-2-pacing\/"/.test(h) && !/6th Grade|Grade 6|4th Grade|3rd Grade Math/.test(h), 'pacing page content');
    check(null, /Final review and exam<\/strong> \(days \d+–180\)/.test(h), 'pacing page reaches day 180');
  }
}
/* ---------- #15 line plots ---------- */
{
  const ctx = {}; vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(OUT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
  const P = ctx.MK_PLOT, plots = Q.filter((q) => /\(#15, Graphing Practice\)/.test(q.sourceNotes || ''));
  check(null, plots.length === 9, 'plot items ' + plots.length);
  for (const q of plots) {
    check(q, P.valid(q.plot) && P.check(q.plot, q.plot.testVectors.correct).ok && fs.existsSync(path.join(OUT, q.plot.answerKey.src)), 'plot item valid with an answer key');
    const data = g(/\(\w+\): ([\d, ]+)\. Make/, q.prompt)[1].split(', ');
    check(q, JSON.stringify([...q.plot.target.values].sort()) === JSON.stringify([...data].sort()), 'plot targets match the data');
  }
  const units = (fs.readFileSync(path.join(OUT, 'data.js'), 'utf8').match(/"grade2": \[([^\]]*)\]/) || [])[1] || '';
  check(null, /measuring-length/.test(units), 'Graphing Practice lists the measuring-length unit');
}

if (fails.length) { console.error(fails.length + ' failures:\n' + fails.slice(0, 60).join('\n')); process.exit(1); }
console.log(`PASS 2nd Grade Math audit (${checks} checks, ${A1.length} Advanced and ${S7.length} Standard rewrites, ${O4.length} open-response, ${S8.length} select-all items)`);
