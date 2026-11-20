#!/usr/bin/env node
/* 3rd Grade Math audit (2026-11-19): checks on the assembled site after scripts/apply-grade3-audit.mjs.
   Every new or rewritten item's answer is recomputed here from its prompt, independently of the authoring scripts in
   tools/grade3-audit-20261119. Usage: node scripts/test-grade3-audit.cjs [_site] */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict');
const OUT = path.resolve(process.argv[2] || '_site');
const UNITS = fs.readdirSync(path.join(OUT, 'question-banks/grade3')).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', ''));
const Q = [], N = [];
for (const u of UNITS) {
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'question-banks/grade3', u + '.json'), 'utf8')).questions) Q.push(Object.assign({ unit: u }, q));
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'grade3/question-banks/math3', u + '.json'), 'utf8')).questions) N.push(Object.assign({ unit: u }, q));
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

/* ---------- recomputation of the #1 Advanced and #7 Standard families ---------- */
const RC = {
  mm1_groups_plus_more: (p) => { const m = g(/There are (\d+) \w+ with (\d+) (\w+) in each\. \w+ adds (\d+) more/, p); return qty(m[1] * m[2] + +m[4], m[3]); },
  mm1_two_sets_of_groups: (p) => { const m = g(/has (\d+) \w+ of (\d+) (\w+)\. \w+ has (\d+) \w+ of/, p); return qty((+m[1] + +m[4]) * m[2], m[3]); },
  mm2_array_add_rows: (p) => { const m = g(/has (\d+) rows of (\d+) tiles\. (\d+) more/, p); return qty((+m[1] + +m[3]) * m[2], 'tiles'); },
  mm2_array_hidden_rows: (p) => { const m = g(/has (\d+) chairs in each row and (\d+) chairs in all\. A curtain hides (\d+)/, p); return qty((m[2] / m[1] - m[3]) * m[1], 'chairs'); },
  mm3_two_products_sum: (p) => { const m = g(/Find (\d+) × (\d+) and (\d+) × (\d+)\./, p); return n(m[1] * m[2] + m[3] * m[4]); },
  mm3_coins_total: (p) => { const m = g(/has (\d+) dimes and (\d+) nickels/, p); return `${m[1] * 10 + m[2] * 5} cents`; },
  mm4_more_than_twice: (p) => { const m = g(/holds (\d+) liters\. A tank holds as much as (\d+) jugs\. A pool holds as much as (\d+) tanks/, p); return qty(m[1] * m[2] * m[3], 'liters'); },
  dv1_share_then_get_more: (p) => { const m = g(/^(\d+) friends share (\d+) (\w+) equally\. Then each friend gets (\d+) more/, p); return qty(m[2] / m[1] + +m[4], m[3]); },
  dv1_share_two_ways: (p) => { const m = g(/^(\d+) crackers are shared equally among (\d+) friends\. .* among (\d+) friends/, p); return qty(m[1] / m[2] - m[1] / m[3], 'crackers'); },
  dv2_group_then_left: (p) => { const m = g(/^(\d+) chairs are set up in rows of (\d+)\. Then (\d+) of the/, p); return qty(m[1] / m[2] - m[3], 'rows'); },
  dv2_two_bag_sizes: (p) => { const m = g(/has (\d+) beads\. Strings of (\d+) beads or strings of (\d+) beads/, p); return qty(m[1] / m[2] - m[1] / m[3], 'strings'); },
  dv3_unknown_then_add: (p) => { const m = g(/Think (\d+) × ___ = (\d+) to find \d+ ÷ \d+\. Then add (\d+)/, p); return n(m[2] / m[1] + +m[3]); },
  dv3_chain_unknowns: (p) => { const m = g(/^(\d+) × □ = (\d+) and □ × △ = (\d+)/, p); return n(m[3] / (m[2] / m[1])); },
  dv4_rows_then_more: (p) => { const m = g(/plants (\d+) (\w+) in (\d+) equal rows\. Then (\d+) more/, p); return qty(m[1] / m[3] + +m[4], m[2]); },
  dv4_take_away_then_share: (p) => { const m = g(/had (\d+) stickers and gave away (\d+)\. The rest were shared equally into (\d+) albums/, p); return qty((m[1] - m[2]) / m[3], 'stickers'); },
  pf1_turn_around_then_double: (p) => { const m = g(/knows (\d+) × (\d+) = \d+/, p); return n(2 * m[1] * m[2]); },
  pf1_commute_and_add: (p) => { const m = g(/Find (\d+) × (\d+) \+ (\d+) × (\d+)\./, p); return n(m[1] * m[2] + m[3] * m[4]); },
  pf2_group_to_ten: (p) => { const m = g(/Find (\d+) × (\d+) × (\d+)\. .* Then add (\d+)/, p); return n(m[1] * m[2] * m[3] + +m[4]); },
  pf2_three_factor_story: (p) => { const m = g(/There are (\d+) shelves\. Each shelf has (\d+) boxes\. Each box has (\d+)/, p); return qty(m[1] * m[2] * m[3], 'toy cars'); },
  pf3_break_apart_five: (p) => { const m = g(/Find (\d+) × (\d+) by breaking \d+ into 5 \+ (\d+)/, p); return `${m[1] * m[3]}; ${m[1] * m[2]}`; },
  pf3_two_part_area: (p) => { const m = g(/into an? (\d+) by (\d+) part and an? \d+ by (\d+) part/, p); return qty(m[1] * Math.max(+m[2], +m[3]), 'square feet'); },
  pf4_one_and_zero_sum: (p) => n(+g(/Find (\d+) × 1 \+ \d+ × 0/, p)[1]),
  pf4_zero_and_one_chain: (p) => n(+g(/\+ \((\d+) × 1\)/, p)[1]),
  pf5_fact_then_add: (p) => { const m = g(/Multiply (\d+) × (\d+)\. Then add (\d+)/, p); return n(m[1] * m[2] + +m[3]); },
  pf5_known_fact_step: (p) => { const m = g(/then find (\d+) × (\d+) − \d+ × (\d+)\./, p); return n(m[1] * (m[2] - m[3])); },
  up1_unknown_then_add: (p) => { const m = g(/^(\d+) × \? = (\d+)\. Find the unknown, then add (\d+)/, p); return n(m[2] / m[1] + +m[3]); },
  up1_two_equations: (p) => { const m = g(/^(\d+) ÷ (\d+) = □ and □ × (\d+) = △/, p); return n(m[1] / m[2] * m[3]); },
  up2_start_unknown_story: (p) => { const m = g(/packed in (\d+) bags with (\d+) apples in each bag\. (\d+) apples/, p); return qty(m[1] * m[2] + +m[3], 'apples'); },
  up2_backward_groups: (p) => { const m = g(/bought (\d+) more\. Then the markers were put into (\d+) equal boxes with (\d+) in each/, p); return qty(m[2] * m[3] - m[1], 'markers'); },
  up3_tens_product_then_add: (p) => { const m = g(/Multiply (\d+) × (\d+)\. Then add (\d+)/, p); return n(m[1] * m[2] + +m[3]); },
  up3_two_tens_products: (p) => { const m = g(/sells (\d+) rows of (\d+) seats on Friday and (\d+) rows of (\d+) seats/, p); return qty(m[1] * m[2] + m[3] * m[4], 'seats'); },
  up5_groups_minus_sold: (p) => { const m = g(/makes (\d+) trays of (\d+) rolls\. (\d+) rolls are sold/, p); return qty(m[1] * m[2] - m[3], 'rolls'); },
  up5_groups_add_share: (p) => { const m = g(/There are (\d+) packs of (\d+) cards and (\d+) loose cards\. .* among (\d+) players/, p); return qty((m[1] * m[2] + +m[3]) / m[4], 'cards'); },
  up6_cost_then_change: (p) => { const m = g(/buys (\d+) notebooks that cost \$(\d+) each and pays with \$(\d+)/, p); return `$${m[3] - m[1] * m[2]}`; },
  up6_compare_two_products: (p) => { const m = g(/red team sold (\d+) boxes of (\d+) cookies\. The blue team sold (\d+) boxes of (\d+)/, p); return qty(Math.abs(m[1] * m[2] - m[3] * m[4]), 'cookies'); },
  as1_round_both_add: (p) => { const m = g(/Round (\d+) and (\d+) to the nearest 10/, p); return n(rnd(+m[1], 10) + rnd(+m[2], 10)); },
  as1_how_many_round_to: () => '10',
  as2_round_both_subtract: (p) => { const m = g(/Round (\d+) and (\d+) to the nearest 100/, p); return n(rnd(+m[1], 100) - rnd(+m[2], 100)); },
  as2_greatest_least_round: (p) => { const m = g(/the (greatest|least) whole number that rounds to (\d+)/, p); return n(m[1] === 'greatest' ? +m[2] + 49 : m[2] - 50); },
  as3_three_addends: (p) => { const m = g(/Add: (\d+) \+ (\d+) \+ (\d+)/, p); return n(+m[1] + +m[2] + +m[3]); },
  as3_two_days_then_more: (p) => { const m = g(/lent (\d+) books on Monday and (\d+) books on Tuesday\. On Wednesday it lent (\d+) fewer/, p); return qty(+m[1] + +m[2] - m[3], 'books'); },
  as4_subtract_then_add: (p) => { const m = g(/Subtract (\d+) − (\d+)\. Then add (\d+)/, p); return n(m[1] - m[2] + +m[3]); },
  as4_two_take_aways: (p) => { const m = g(/carry (\d+) pounds\. It already has boxes of (\d+) pounds and (\d+) pounds/, p); return qty(m[1] - m[2] - m[3], 'pounds'); },
  as5_estimate_two_step: (p) => { const m = g(/had (\d+) toys\. It got (\d+) more and sold (\d+)/, p); return qty(rnd(+m[1], 100) + rnd(+m[2], 100) - rnd(+m[3], 100), 'toys'); },
  uf1_parts_left: (p) => { const m = g(/cut into (\d+) equal pieces\. (\d+) pieces? (?:is|are) eaten/, p); return `${m[1] - m[2]}/${m[1]}`; },
  uf1_two_parts_rest: (p) => { const m = g(/split into (\d+) equal parts\. Beans grow in (\d+) parts? and corn grows in (\d+) parts?/, p); return `${m[1] - m[2] - m[3]}/${m[1]}`; },
  uf2_copies_plus_more: (p) => { const m = g(/Start with (\d+) copies of 1\/(\d+)\. Add (\d+) more/, p); return `${+m[1] + +m[3]}/${m[2]}`; },
  uf2_copies_difference: (p) => { const m = g(/ate (\d+)\/(\d+) of a pizza\. \w+ ate (\d+)\//, p); return n(m[1] - m[3]); },
  uf3_nth_mark: (p) => { const m = g(/marked into (\d+) equal parts\. Luis cuts at mark number (\d+)/, p); return `${m[2]}/${m[1]} meter`; },
  uf3_between_marks: (p) => { const m = g(/has (\d+) equal parts\. A bench is at (\d+)\/\d+ mile and a fountain is at (\d+)\//, p); return `${m[3] - m[2]}/${m[1]} mile`; },
  ec1_split_each_part: (p) => { const m = g(/shows (\d+)\/(\d+) shaded\. Each part is split into (\d+) equal pieces/, p); return `${m[1] * m[3]}; ${m[1] * m[3]}/${m[2] * m[3]}`; },
  ec1_same_amount_pieces: (p) => { const m = g(/into (\d+) equal pieces and ate (\d+)\. \w+ cut the same size pan into (\d+)/, p); return qty(m[2] * m[3] / m[1], 'pieces'); },
  ec2_missing_then_check: (p) => { const m = g(/Find n: (\d+)\/(\d+) = n\/(\d+)/, p); return `${m[1] * m[3] / m[2]}/${m[3]}`; },
  ec2_two_equivalents: (p) => { const m = g(/equal to (\d+)\/(\d+): one in (\w+) and one in (\w+)\./, p), c1 = DN[m[3]], c2 = DN[m[4]]; return `${m[1] * c1 / m[2]}/${c1}, ${m[1] * c2 / m[2]}/${c2}`; },
  ec3_wholes_to_parts: (p) => { const m = g(/How many (\w+) make (\d+) wholes/, p); return `${m[2] * DN[m[1]]}/${DN[m[1]]}`; },
  ec3_whole_sum: (p) => { const m = g(/is (\d+)\/(\d+) \+ (\d+)\/(\d+)\?/, p); return n(m[1] / m[2] + m[3] / m[4]); },
  ec4_order_three: (p) => g(/least to greatest: (.*)$/, p)[1].split(', ').sort((a, b) => fr(a).cmp(fr(b))).join(', '),
  ec4_who_more_by: (p) => { const m = g(/^(\w+) ran (\d+)\/\d+ mile\. (\w+) ran (\d+)\//, p); return `${+m[2] > +m[4] ? m[1] : m[3]}, by ${Math.abs(m[2] - m[4])}`; },
  ec5_order_same_numerator: (p) => g(/greatest to least: (.*)$/, p)[1].split(', ').sort((a, b) => fr(b).cmp(fr(a))).join(', '),
  ec5_same_numerator_story: (p) => { const m = g(/^(\w+) ate (\d+)\/(\d+) of a sandwich\. (\w+) ate \d+\/(\d+)/, p); return +m[3] < +m[5] ? m[1] : m[4]; },
  tm1_read_then_later: (p) => { const m = g(/shows (\d+:\d+)\. What time will it show (\d+) minutes later/, p); return tm(tmin(m[1]) + +m[2]); },
  tm1_minutes_before: (p) => { const m = g(/is (\d+) minutes before (\d+):00/, p); return tm(m[2] * 60 - m[1]); },
  tm2_two_activities_end: (p) => { const m = g(/reading at (\d+:\d+) and reads for (\d+) minutes\. Then \w+ draws for (\d+) minutes/, p); return tm(tmin(m[1]) + +m[2] + +m[3]); },
  tm2_who_longer: (p) => { const m = g(/^(\w+) practiced from (\d+:\d+) to (\d+:\d+)\. (\w+) practiced from \d+:\d+ to (\d+:\d+)/, p), d1 = tmin(m[3]) - tmin(m[2]), d2 = tmin(m[5]) - tmin(m[2]); return `${d1 > d2 ? m[1] : m[4]}, by ${Math.abs(d1 - d2)} minutes`; },
  tm4_weights_plus: (p) => { const m = g(/has (\d+) weights of (\d+) grams each and one (\d+)-gram/, p); return qty(m[1] * m[2] + +m[3], 'grams'); },
  tm4_total_then_compare: (p) => { const m = g(/mass of (\d+) grams\. A bag of apples has a mass of (\d+) grams\. A box holds (\d+) melons/, p); return qty(m[3] * m[1] - m[2], 'grams'); },
  tm5_buckets_plus: (p) => { const m = g(/^(\d+) buckets each hold (\d+) liters of water\. (\d+) more/, p); return qty(m[1] * m[2] + +m[3], 'liters'); },
  tm5_use_then_share: (p) => { const m = g(/has (\d+) liters of water\. (\d+) liters are used .* into (\d+) buckets/, p); return qty((m[1] - m[2]) / m[3], 'liters'); },
  gd3_symbols_for_two: (p) => { const m = g(/stands for (\d+)\. Apples got (\d+) votes and pears got (\d+) votes/, p); return qty((+m[2] + +m[3]) / m[1], 'symbols'); },
  gd3_more_from_symbols: (p) => { const m = g(/stands for (\d+) books\. Ana has (\d+) symbols and Ben has (\d+) symbols/, p); return qty(Math.abs(m[2] - m[3]) * m[1], 'books'); },
  gd4_quarter_inch_difference: (p) => { const m = g(/One ribbon is ([\d /]+) inches long\. Another ribbon is ([\d /]+) inches long/, p), d = fr(m[2]).sub(fr(m[1])); return n(d.a * 4 / d.b); },
  ar1_two_shapes_total: (p) => { const m = g(/covered by (\d+) unit squares .* covered by (\d+) unit squares/, p); return qty(+m[1] + +m[2], 'square units'); },
  ar1_squares_still_needed: (p) => { const m = g(/rectangle that is (\d+) units long and (\d+) units wide .*\. (\d+) squares are already placed/, p); return qty(m[1] * m[2] - m[3], 'squares'); },
  ar2_count_two_parts: (p) => { const m = g(/covered with (\d+) squares and the other part with (\d+) squares\. Each square is 1 (\w+) long/, p); return qty(+m[1] + +m[2], SQ[m[3]]); },
  ar2_compare_counts: (p) => { const m = g(/Card A is covered by (\d+) squares and card B by (\d+) squares\. Each square is 1 (\w+)/, p); return qty(Math.abs(m[1] - m[2]), SQ[m[3]]); },
  ar3_longer_rectangle: (p) => { const m = g(/is (\d+) feet by (\d+) feet\. It is made (\d+) (?:foot|feet) longer/, p); return qty((+m[1] + +m[3]) * m[2], 'square feet'); },
  ar3_same_area_side: (p) => { const m = g(/Rug A is (\d+) feet by (\d+) feet\. Rug B has the same area and one side is (\d+) feet/, p); return qty(m[1] * m[2] / m[3], 'feet'); },
  ps1_fence_minus_gate: (p) => { const m = g(/is (\d+) feet long and (\d+) feet wide\. A gate (\d+)/, p); return qty(2 * (+m[1] + +m[2]) - m[3], 'feet'); },
  ps3_area_and_perimeter: (p) => { const m = g(/A rectangle is (\d+) by (\d+)\. Find its perimeter and its area/, p); return `${2 * (+m[1] + +m[2])} units; ${m[1] * m[2]} square units`; },
  ps3_greatest_area: (p) => { const P = +g(/perimeter of (\d+) feet/, p)[1], s = P / 2; let b = 0; for (let a = 1; a < s; a++) b = Math.max(b, a * (s - a)); return qty(b, 'square feet'); },
  ps4_count_sides: (p) => { const m = g(/sides are on (\d+) (\w+) and (\d+) (\w+) in all/, p), side = (w) => SIDES[w] || SIDES[w.replace(/s$/, '')] || SIDES[w.replace(/es$/, '')]; return n(m[1] * side(m[2]) + m[3] * side(m[4])); },
  ps5_parts_shaded_squares: (p) => { const m = g(/made of (\d+) unit squares is split into (\d+) parts with equal area\. (\d+) parts? (?:is|are) shaded/, p); return n(m[1] / m[2] * m[3]); }
};
const A1 = Q.filter((q) => /\(#1, Advanced/.test(q.sourceNotes || '')), S7 = Q.filter((q) => /\(#7, Standard\)/.test(q.sourceNotes || ''));
check(null, A1.length >= 300, 'Advanced rewrites ' + A1.length);
check(null, S7.length >= 250, 'Standard rewrites ' + S7.length);
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
}
const share = (L, lo) => { const low = new Set(Q.filter((q) => lo.includes(q.level)).map((q) => q.skillId + '|' + mask(q.prompt))); const xs = Q.filter((q) => q.level === L); return xs.filter((q) => low.has(q.skillId + '|' + mask(q.prompt))).length / xs.length; };
check(null, share('honors', ['cp2', 'cp1']) <= 0.34, 'Advanced items reusing a lower template ' + share('honors', ['cp2', 'cp1']).toFixed(2));
check(null, share('cp1', ['cp2']) <= 0.34, 'Standard items reusing a Support template ' + share('cp1', ['cp2']).toFixed(2));
const lv = (L) => Q.filter((q) => q.level === L).length;
check(null, Math.max(lv('cp2'), lv('cp1'), lv('honors')) - Math.min(lv('cp2'), lv('cp1'), lv('honors')) <= 1, `levels ${lv('cp2')}/${lv('cp1')}/${lv('honors')}`);

/* ---------- #4 open response ---------- */
const O4 = Q.filter((q) => /\(#4, open response\)/.test(q.sourceNotes || ''));
const skills = [...new Set(Q.map((q) => q.skillId))];
assert.equal(skills.length, 53);
check(null, O4.length === 159, 'open-response items ' + O4.length);
check(null, Q.filter((q) => q.format === 'open-response').length === 159, 'every open-response item is a context item');
for (const s of skills) for (const L of ['cp2', 'cp1', 'honors']) check({ id: s + '|' + L }, O4.filter((q) => q.skillId === s && q.level === L).length === 1, 'one context open-response item');
for (const q of O4) {
  check(q, q.parts.length === 4 && /^Sample answer: /.test(q.parts[3].answer) && q.solutionSteps.length === 4, 'four parts ending with an explanation');
  check(q, q.parts.slice(0, 3).some((p) => !/^Sample answer: /.test(p.answer)), 'at least one checked part');
  check(q, !/^(Answer each part|Match each problem)/.test(q.prompt), 'not the drill template');
}
const OR = {   // recompute a checked part of each context family: [part index, expected answer]
  mm1_open_baskets: (q) => { const m = g(/has (\d+) baskets\. Each basket has (\d+) peaches/, q.prompt); return [2, qty(m[1] * m[2], 'peaches')]; },
  mm2_open_garden_array: (q) => { const m = g(/has (\d+) rows of plants with (\d+) plants/, q.prompt); return [0, qty(m[1] * m[2], 'plants')]; },
  mm3_open_packs: (q) => { const f = +g(/packs of (\d+)/, q.prompt)[1], m = g(/Team A gets (\d+) packs and Team B gets (\d+) packs/, q.prompt); return [2, n((+m[1] + +m[2]) * f)]; },
  mm4_open_bus: (q) => { const m = g(/sends (\d+) vans .* carries (\d+) students/, q.prompt); return [0, qty(m[1] * m[2], 'students')]; },
  dv1_open_share: (q) => { const m = g(/^(\d+) stickers are shared equally among (\d+) friends/, q.prompt); return [0, qty(m[1] / m[2], 'stickers')]; },
  dv2_open_teams: (q) => { const m = g(/^(\d+) players are put into teams of (\d+)/, q.prompt); return [0, qty(m[1] / m[2], 'teams')]; },
  dv3_open_fact_family: (q) => { const m = g(/A box of (\d+) crayons has (\d+) crayons in each row/, q.prompt); return [1, qty(m[1] / m[2], 'rows')]; },
  dv4_open_bake_sale: (q) => { const m = g(/has (\d+) cookies to put on (\d+) plates/, q.prompt), x = +g(/^(\d+) cookies are added/, q.parts[1].prompt)[1]; return [2, qty(m[2] * (m[1] / m[2] + x), 'cookies')]; },
  pf1_open_turn_around: (q) => { const m = g(/sets out (\d+) rows of (\d+) chairs/, q.prompt); return [2, qty(2 * m[1] * m[2], 'chairs')]; },
  pf2_open_boxes: (q) => { const m = g(/There are (\d+) boxes\. Each box has (\d+) bags, and each bag has (\d+) marbles/, q.prompt); return [1, qty(m[1] * m[2] * m[3], 'marbles')]; },
  pf3_open_break_apart: (q) => { const m = g(/has (\d+) rows of (\d+) tiles/, q.prompt); return [2, qty(m[1] * m[2], 'tiles')]; },
  pf4_open_empty_boxes: (q) => [0, qty(+g(/Mia has (\d+) boxes/, q.prompt)[1], 'pencils')],
  pf5_open_known_fact: (q) => { const m = g(/wants to find (\d+) × (\d+)/, q.prompt); return [1, n(m[1] * m[2])]; },
  up1_open_unknown: (q) => { const m = g(/holds (\d+) books in (\d+) equal stacks/, q.prompt); return [1, n(m[1] / m[2])]; },
  up2_open_unknown_position: (q) => { const m = g(/^(\d+) students sit at tables\. There are (\d+) students/, q.prompt); return [1, qty(m[1] / m[2], 'tables')]; },
  up3_open_tens: (q) => { const m = g(/has (\d+) rows with (\d+) seats/, q.prompt); return [0, qty(m[1] * m[2], 'seats')]; },
  up4_open_table_pattern: (q) => { const a = +g(/in the (\d+)s row/, q.prompt)[1]; return [2, n(a * 10)]; },
  up5_open_two_step_equation: (q) => { const m = g(/makes (\d+) trays of (\d+) rolls and sells (\d+) rolls/, q.prompt); return [2, n(m[1] * m[2] - m[3])]; },
  up6_open_shopping: (q) => { const m = g(/buys (\d+) books that cost \$(\d+) each\. She pays with \$(\d+)/, q.prompt); return [1, `$${m[3] - m[1] * m[2]}`]; },
  as1_open_round_ten: (q) => [0, n(rnd(+g(/collected (\d+) cans/, q.prompt)[1], 10))],
  as2_open_round_hundred: (q) => [0, n(rnd(+g(/sold (\d+) tickets/, q.prompt)[1], 100))],
  as3_open_reading: (q) => { const m = g(/Class A read (\d+) pages\. Class B read (\d+) pages/, q.prompt); return [0, qty(+m[1] + +m[2], 'pages')]; },
  as4_open_seats: (q) => { const m = g(/has (\d+) seats\. (\d+) seats are filled/, q.prompt); return [0, qty(m[1] - m[2], 'seats')]; },
  as5_open_estimate: (q) => { const m = g(/added (\d+) \+ (\d+)/, q.prompt); return [1, n(+m[1] + +m[2])]; },
  uf1_open_pizza: (q) => [1, n(+g(/cut into (\d+) equal slices/, q.prompt)[1])],
  uf2_open_fence: (q) => { const m = g(/has (\d+) equal sections\. Dev paints (\d+) sections/, q.prompt); return [2, `${m[1] - m[2]}/${m[1]}`]; },
  uf3_open_trail: (q) => [2, n(+g(/marked into (\d+) equal parts/, q.prompt)[1])],
  uf4_open_laps: (q) => { const m = g(/marked in (\w+) of one lap\. Omar swims (\d+)/, q.prompt), d = DN[m[1]]; return [0, `${m[2]}/${d} laps`]; },
  ec1_open_strips: (q) => { const m = g(/One shows (\d+)\/(\d+) shaded\. The other is cut into (\d+) equal parts/, q.prompt); return [1, `${m[1] * m[3] / m[2]}/${m[3]}`]; },
  ec2_open_recipe: (q) => { const m = g(/uses (\d+)\/(\d+) cup of oats\. Mia has only a 1\/(\d+) cup scoop/, q.prompt); return [0, n(m[1] * m[3] / m[2])]; },
  ec3_open_sandwiches: (q) => { const m = g(/^(\d+) sandwiches are each cut into (\d+) equal pieces/, q.prompt); return [1, `${m[1] * m[2]}/${m[2]}`]; },
  ec4_open_juice: (q) => { const m = g(/drank (\d+)\/\d+ of his and Mei drank (\d+)\//, q.prompt); return [1, +m[1] > +m[2] ? '>' : '<']; },
  ec5_open_ribbons: (q) => { const m = g(/used \d+\/(\d+) of one and Zoe used \d+\/(\d+)/, q.prompt); return [0, +m[1] < +m[2] ? 'Raj' : 'Zoe']; },
  tm1_open_clock: (q) => { const t = g(/shows (\d+:\d+)/, q.prompt)[1]; return [2, tm(tmin(t) + 15)]; },
  tm2_open_afternoon: (q) => { const m = g(/starts homework at (\d+:\d+)\. Math takes (\d+) minutes and reading takes (\d+) minutes/, q.prompt); return [2, tm(tmin(m[1]) + +m[2] + +m[3])]; },
  tm3_open_water_jugs: (q) => { const m = g(/fills (\d+) jugs that each hold (\d+) liters/, q.prompt); return [0, `${m[1] * m[2]} liters`]; },
  tm4_open_balance: (q) => { const m = g(/balances (\d+) weights of (\d+) grams/, q.prompt); return [0, `${m[1] * m[2]} grams`]; },
  tm5_open_crates: (q) => { const m = g(/mass of (\d+) kilograms\. Another has a mass of (\d+) kilograms/, q.prompt); return [0, `${+m[1] + +m[2]} kilograms`]; },
  gd1_open_picture_graph: (q) => { const m = g(/stands for (\d+) votes\. Dogs have (\d+) stars, cats have (\d+) stars and fish have (\d+) stars/, q.prompt); return [1, `${(+m[2] + +m[3] + +m[4]) * m[1]} votes`]; },
  gd2_open_bar_graph: (q) => { const m = g(/red ends at (\d+) and the bar for blue ends at (\d+)/, q.prompt); return [1, `${+m[1] + +m[2]} votes`]; },
  gd3_open_make_graph: (q) => { const m = g(/Ana (\d+), Ben (\d+), Cruz (\d+)\. .* stands for (\d+) books/, q.prompt); return [2, n((+m[1] + +m[2] + +m[3]) / m[4])]; },
  gd4_open_ruler: (q) => { const x = fr(g(/is ([\d /]+) inches long/, q.prompt)[1]); return [2, mixed(x.add(x)) + ' inches']; },
  gd5_open_line_plot: (q) => [0, n(g(/inches: (.*)\. Make/, q.prompt)[1].split(', ').length)],
  ar1_open_tiles: (q) => [0, `${g(/Mat A is covered by (\d+) unit squares/, q.prompt)[1]} square units`],
  ar2_open_count: (q) => { const m = g(/covered by (\d+) squares that are 1 (\w+) on each side, and another part by (\d+) more/, q.prompt); return [1, `${+m[1] + +m[3]} ${SQ[m[2]]}`]; },
  ar3_open_rug: (q) => { const m = g(/is (\d+) feet long and (\d+) feet wide/, q.prompt); return [0, `${m[1] * m[2]} square feet`]; },
  ar4_open_two_parts: (q) => { const m = g(/is (\d+) feet by (\d+) feet/, q.prompt); return [2, `${m[1] * m[2]} square feet`]; },
  ar5_open_L_shape: (q) => { const m = g(/a (\d+) by (\d+) rectangle and a (\d+) by (\d+) rectangle/, q.prompt); return [2, `${m[1] * m[2] + m[3] * m[4]} square units`]; },
  ps1_open_fence: (q) => { const m = g(/is (\d+) feet long and (\d+) feet wide/, q.prompt); return [0, `${2 * (+m[1] + +m[2])} feet`]; },
  ps2_open_unknown_side: (q) => { const m = g(/perimeter of (\d+) feet\. Three sides are (\d+), (\d+) and (\d+) feet/, q.prompt); return [1, `${m[1] - m[2] - m[3] - m[4]} feet`]; },
  ps3_open_pen: (q) => { const P = +g(/has (\d+) feet of fence/, q.prompt)[1], s = P / 2; let b = 0; for (let a = 1; a < s; a++) b = Math.max(b, a * (s - a)); return [1, `${b} square feet`]; },
  ps4_open_quadrilateral: () => [0, '4'],
  ps5_open_split: (q) => { const m = g(/made of (\d+) unit squares is split into (\d+) parts with equal area\. (\d+) parts? (?:is|are) shaded/, q.prompt); return [2, n(m[1] / m[2] * m[3])]; }
};
for (const q of O4) {
  const fn = OR[fam(q)];
  check(q, !!fn, 'no open-response recomputation for ' + fam(q));
  if (!fn) continue;
  try { const [i, want] = fn(q); check(q, q.parts[i].answer === want, `part ${i}: ${q.parts[i].answer} but recomputed ${want}`); } catch (e) { check(q, false, e.message); }
}

/* ---------- #8 select-all ---------- */
const S8 = Q.filter((q) => q.format === 'select-all');
check(null, S8.length === 113 && S8.every((q) => /\(#8, select-all/.test(q.sourceNotes || '')), 'every select-all item rewritten: ' + S8.length);
const ev = (s) => { s = s.replace(/×/g, '*').replace(/−/g, '-').replace(/÷/g, '/'); if (!/^[\d\s+*()/-]+$/.test(s)) throw Error('bad expression ' + s); return Function('return ' + s)(); };
const tf = (s) => { const [a, b] = s.split('/').map(Number); return new R(a, b); };
const SEL = {
  as1_select_rounds_to: (q, t) => rnd(I(t), 10) === +g(/round to (\d+) when/, q.prompt)[1],
  as2_select_rounds_to: (q, t) => rnd(I(t), 100) === +g(/round to (\d+) when/, q.prompt)[1],
  as3_select_sum_equals: (q, t) => ev(t) === +g(/equal (\d+)\./, q.prompt)[1],
  as4_select_difference_equals: (q, t) => ev(t) === +g(/equal (\d+)\./, q.prompt)[1],
  as5_select_reasonable: (q, t) => { const [l, r] = t.split(' = '); return ev(l) === +r; },
  ar1_select_area_equals: (q, t) => { const a = +g(/area of (\d+) square units/, q.prompt)[1]; let m = /^covered by (\d+) unit squares with no gaps or overlaps$/.exec(t); if (m) return +m[1] === a; m = /^(\d+) unit squares in rows with no gaps$/.exec(t); if (m) return +m[1] === a; m = /^(\d+) rows of (\d+) unit squares$/.exec(t); if (m) return m[1] * m[2] === a; return false; },
  ar3_select_rectangle_area: (q, t) => { const m = /^(\d+) by (\d+)$/.exec(t); return m[1] * m[2] === +g(/area of (\d+) square feet/, q.prompt)[1]; },
  dv1_select_each_gets: (q, t) => { const m = /^(\d+) shared by (\d+)$/.exec(t); return m[1] / m[2] === +g(/gets (\d+)\./, q.prompt)[1]; },
  dv2_select_number_of_groups: (q, t) => { const m = /^(\d+) in groups of (\d+)$/.exec(t); return m[1] / m[2] === +g(/exactly (\d+) groups/, q.prompt)[1]; },
  dv3_select_fact_family: (q, t) => { const m = g(/family for (\d+), (\d+) and (\d+)\./, q.prompt), e = /^(\d+) ([×÷]) (\d+) = (\d+)$/.exec(t); if (!e) return false; const set = [m[1], m[2], m[3]].map(Number).sort((a, b) => a - b).join(), used = [e[1], e[3], e[4]].map(Number).sort((a, b) => a - b).join(); return set === used && (e[2] === '×' ? e[1] * e[3] === +e[4] : e[1] / e[3] === +e[4]); },
  dv4_select_rows_of: (q, t) => { const m = /^(\d+) seeds in (\d+) equal rows$/.exec(t); return m[1] / m[2] === +g(/have (\d+) seeds in each row/, q.prompt)[1]; },
  ec2_select_equivalent: (q, t) => tf(t).cmp(tf(g(/equal to (\d+\/\d+)\./, q.prompt)[1])) === 0,
  ec3_select_equal_whole: (q, t) => tf(t).cmp(new R(+g(/equal to (\d+)\./, q.prompt)[1])) === 0,
  ec4_select_greater_same_den: (q, t) => tf(t).cmp(tf(g(/greater than (\d+\/\d+)\./, q.prompt)[1])) > 0,
  ec5_select_greater_same_num: (q, t) => tf(t).cmp(tf(g(/greater than (\d+\/\d+)\./, q.prompt)[1])) > 0,
  gd3_select_whole_symbols: (q, t) => +t % +g(/stands for (\d+)\./, q.prompt)[1] === 0,
  mm1_select_same_total: (q, t) => { const tot = +g(/show (\d+) as equal groups/, q.prompt)[1]; const m = /^(\d+) groups of (\d+)$/.exec(t); return (m ? m[1] * m[2] : ev(t)) === tot; },
  mm2_select_array_total: (q, t) => { const m = /^(\d+) rows of (\d+)$/.exec(t); return m[1] * m[2] === +g(/have (\d+) tiles/, q.prompt)[1]; },
  mm3_select_products_of: (q, t) => +t % +g(/products of (\d+) \(/, q.prompt)[1] === 0,
  mm4_select_total_crayons: (q, t) => { const m = /^(\d+) boxes of (\d+) crayons$/.exec(t); return m[1] * m[2] === +g(/have (\d+) crayons/, q.prompt)[1]; },
  up1_select_unknown_is: (q, t) => { const x = +g(/unknown \? is (\d+)\./, q.prompt)[1]; let m = /^(\d+) × \? = (\d+)$/.exec(t); if (m) return m[1] * x === +m[2]; m = /^(\d+) ÷ \? = (\d+)$/.exec(t); return m[1] / x === +m[2]; },
  up2_select_story_equation: (q, t) => { const m = g(/^(\d+) students sit in (\d+) equal rows/, q.prompt), e = /^(\d+) ([×÷+−]) (\d+) = (\d+)$/.exec(t), tot = +m[1], rows = +m[2], each = tot / rows; if (!/[×÷]/.test(e[2]) || ev(`${e[1]} ${e[2]} ${e[3]}`) !== +e[4]) return false; return [tot, rows, each].sort().join() === [+e[1], +e[3], +e[4]].sort().join(); },
  up3_select_tens_product: (q, t) => ev(t) === +g(/equal to (\d+)\./, q.prompt)[1],
  up5_select_expression: (q, t) => { const m = g(/makes (\d+) trays of (\d+) rolls and sells (\d+)\./, q.prompt); return ev(t) === m[1] * m[2] - m[3] && /−/.test(t) && !/\(\d+ − /.test(t) && !/^\d+ − \d+ ×/.test(t); },
  up6_select_estimate: (q, t) => { const m = /^(\d+) \+ (\d+) is about (\d+)$/.exec(t); return rnd(+m[1], 10) + rnd(+m[2], 10) === +m[3]; },
  ps1_select_perimeter: (q, t) => { const P = +g(/perimeter of (\d+) units/, q.prompt)[1]; let m = /^(\d+) by (\d+) rectangle$/.exec(t); if (m) return 2 * (+m[1] + +m[2]) === P; m = /^square with (\d+)-unit sides$/.exec(t); return 4 * m[1] === P; },
  ps2_select_missing_side: (q, t) => { const P = +g(/perimeter of (\d+) units/, q.prompt)[1], m = /^sides (\d+), (\d+), (\d+); missing side (-?\d+)$/.exec(t); return P - m[1] - m[2] - m[3] === +m[4]; },
  ps4_select_names: (q, t) => ({ square: ['quadrilateral', 'rectangle', 'rhombus', 'parallelogram'], rectangle: ['quadrilateral', 'parallelogram', 'shape with 4 right angles'], rhombus: ['quadrilateral', 'parallelogram', 'shape with 4 equal sides'] })[g(/always describe a (\w+)\./, q.prompt)[1]].includes(t),
  pf1_select_same_product: (q, t) => { const m = g(/equal to (\d+) × (\d+)\./, q.prompt); return ev(t) === m[1] * m[2]; },
  pf2_select_associative: (q, t) => { const m = g(/equal to (\d+) × (\d+) × (\d+)\./, q.prompt); return ev(t) === m[1] * m[2] * m[3]; },
  pf3_select_break_apart: (q, t) => { const m = g(/equal to (\d+) × (\d+)\./, q.prompt); return ev(t) === m[1] * m[2]; },
  pf4_select_equals_number: (q, t) => ev(t) === +g(/equal to (\d+)\./, q.prompt)[1],
  pf5_select_fact_product: (q, t) => ev(t) === +g(/product of (\d+)\./, q.prompt)[1],
  tm1_select_after_within: (q, t) => { const t0 = tmin(g(/later than (\d+:\d+)/, q.prompt)[1]); let d = tmin(t) - t0; if (d < -600) d += 720; return d > 0 && d < 15; },
  tm2_select_elapsed: (q, t) => { const m = /^(\d+:\d+) to (\d+:\d+)$/.exec(t); let d = tmin(m[2]) - tmin(m[1]); if (d < 0) d += 720; return d === +g(/exactly (\d+) minutes/, q.prompt)[1]; },
  tm5_select_total_liters: (q, t) => { const m = /^(\d+) buckets of (\d+) liters$/.exec(t); return m[1] * m[2] === +g(/exactly (\d+) liters/, q.prompt)[1]; },
  uf1_select_unit_fraction: (q, t) => { const d = +g(/show 1\/(\d+)\./, q.prompt)[1], W = { 3: 'third', 4: 'fourth', 6: 'sixth', 8: 'eighth' }; return [`1 of ${d} equal parts`, `one ${W[d]} of a whole`, `1 part when a whole is cut into ${d} equal parts`, `1 of ${d} equal slices`].includes(t); },
  uf2_select_copies: (q, t) => {
    const want = tf(g(/equal to (\d+\/\d+)\./, q.prompt)[1]), val = (x) => (/\//.test(x) ? tf(x) : new R(+x));
    let v, m = /^(\d+) copies of (\d+\/\d+|\d+)$/.exec(t);
    if (m) { const u = val(m[2]); v = new R(m[1] * u.a, u.b); }
    else if ((m = /^(\d+) × (\d+\/\d+)$/.exec(t))) { const u = val(m[2]); v = new R(m[1] * u.a, u.b); }
    else if (/ \+ /.test(t)) v = t.split(' + ').reduce((a, x) => a.add(tf(x)), new R(0));
    else v = val(t);
    return v.cmp(want) === 0;
  },
  uf4_select_past_one: (q, t) => tf(t).cmp(new R(1)) > 0
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

/* ---------- small fixes #15 #16 ---------- */
for (const q of Q) {
  const txt = [q.prompt, Array.isArray(q.answer) ? q.answer.join(' ') : q.answer, ...(q.options || []).map((o) => o.text), ...(q.parts || []).map((p) => p.prompt + ' ' + p.answer)].join(' | ');
  check(q, !/(?<![\d/,.])1 (pets|sections|strings|rolls|square units|parts are|parts)\b/.test(txt.replace(/1 parts? (?:is|are) (?:shaded|eaten)/g, '')), 'plural after 1');
}
for (const id of ['m3-as-s01-cp2-028', 'm3-ec-s03-cp1-028', 'm3-ec-s03-honors-028']) check(byId[id], !byId[id].options.some((o) => /answer is 0\b/.test(o.text)), 'throwaway 0 choice');

/* ---------- both bank copies, players, standards map, card, pacing ---------- */
const nById = Object.fromEntries(N.map((q) => [q.id, q]));
for (const q of Q) {
  if (q.format === 'plot') { check(q, !nById[q.id], 'plot item in the Grade 3 players'); continue; }
  const x = nById[q.id];
  check(q, !!x, 'missing from the Grade 3 player bank');
  if (x) for (const k of ['prompt', 'answer', 'options', 'parts', 'level', 'standards', 'solutionSteps']) check(q, JSON.stringify(x[k]) === JSON.stringify(q[k]), 'copies differ in ' + k);
}
const meta = {};
for (const u of UNITS) Object.assign(meta, JSON.parse(fs.readFileSync(path.join(OUT, 'grade3/question-banks/math3/meta', u + '.meta.json'), 'utf8')));
for (const q of [...A1, ...S7, ...O4, ...S8]) check(q, !!meta[q.id], 'player metadata');
for (const q of [...A1, ...S7]) if (meta[q.id] && meta[q.id].distractors) check(q, !Object.keys(meta[q.id].distractors).includes(String(q.answer)), 'a distractor equals the key');
{
  const G = { document: {}, location: { search: '', pathname: '/x' }, MK_ELEMENTARY: { course: 'math3' }, URLSearchParams, Math, JSON, console }; G.window = G;
  vm.createContext(G); vm.runInContext(fs.readFileSync(path.join(OUT, 'grade3/worksheet-generator/elementary/el-core.js'), 'utf8'), G);
  const K = G.MKEL;
  const cases = [['6 ft', '6 feet', '', true], ['12 sq units', '12 square units', '', true], ['5 L', '5 liters', '', true], ['30 min', '30 minutes', '', true], ['20 cm²', '20 square centimeters', '', true],
    ['less than', '<', '', true], ['greater', '>', '', true], ['less', '<', '', true], ['4:30 pm', '4:30', '', true], ['4:30 PM', '4:30', '', true], ['one fourth', 'one‑fourth', '', true],
    ['1/2', '4/8', 'Point P is at 1/2. The line is marked in eighths. Which fraction in eighths names the same point?', false], ['4/8', '4/8', 'Point P is at 1/2. The line is marked in eighths. Which fraction in eighths names the same point?', true],
    ['2/3', '4/6', 'A swim lane is marked in sixths of one lap. Omar swims 4 of those parts. How many laps is that? Write a fraction.', false], ['3 ft', '3 inches', '', false], ['12', '12 square units', '', true]];
  for (const [t, k, p, want] of cases) check({ id: 'checker' }, K.checkAnswer(t, k, p) === want, `${t} vs ${k}`);
  for (const q of N) {
    if (q.format === 'short-answer') check(q, K.checkAnswer(String(q.answer), String(q.answer), q.prompt), 'key not accepted by the checker');
    if (q.format === 'open-response') for (const p of q.parts) check(q, K.selfCheck(p) || K.checkAnswer(String(p.answer), String(p.answer), p.prompt + ' ' + q.prompt), 'part key not accepted: ' + p.answer);
  }
  const uc = fs.readFileSync(path.join(OUT, 'grade3/worksheet-generator/elementary/el-understanding-check.js'), 'utf8');
  check(null, /K\.checkAnswer\(inp\.value, p\.answer, p\.prompt\)/.test(uc) && /K\.selfCheck\(p\.parts\[i\]\)/.test(uc) && /The mistake: the student/.test(uc), 'Understanding Check uses the new checker');
  for (const page of ['grade3-games.html', 'grade3-understanding-check.html']) check(null, /el-core\.js\?v=g3-audit-20261119/.test(fs.readFileSync(path.join(OUT, 'grade3/worksheet-generator', page), 'utf8')), page + ' versioned');
}
{
  const kid = require(path.join(OUT, 'worksheet-generator/core/elementary/kid-ui/kid-ui.js'));
  check(null, kid.kind('1/6 meter') === 'fraction-unit' && /fraction/.test(kid.hint('2 3/4 inches', 3)), 'fraction-with-unit hint');
}
{
  const s = fs.readFileSync(path.join(OUT, 'grade3-main-catalog.js'), 'utf8');
  const w = {}; w.window = w; w.globalThis = w; vm.createContext(w);
  vm.runInContext(s.slice(s.indexOf('/* Grade 3 audit 2026-11-19 */')), w);
  let mapped = 0; for (const sk of skills) { const set = 'grade3-' + sk.replace(/-skill-\d+$/, ''); if ((w.MKSTD_SKILLS[set] || {})[sk] && w.MKSTD_SKILLS[set][sk].length) mapped++; }
  check(null, mapped === 53, 'standards map covers ' + mapped + ' of 53 skills');
  check(null, s.includes(`"approved":"53 skills · ${Q.length.toLocaleString('en-US')} verified questions`), 'course card count ' + Q.length);
}
{
  const p = path.join(OUT, 'grade-3-pacing/index.html');
  check(null, fs.existsSync(p), 'pacing page');
  if (fs.existsSync(p)) {
    const h = fs.readFileSync(p, 'utf8');
    check(null, /33 of 33 standards have question-bank practice/.test(h) && /spring Grade 3 MCAS/.test(h) && /Grade 4 preview/.test(h) && /canonical" href="https:\/\/mrksclassroom\.com\/grade-3-pacing\/"/.test(h) && !/6th Grade|Grade 6|4th Grade/.test(h), 'pacing page content');
    check(null, /Final review and exam<\/strong> \(days \d+–180\)/.test(h), 'pacing page reaches day 180');
  }
}
/* ---------- #13 plot items ---------- */
{
  const ctx = {}; vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(OUT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
  const P = ctx.MK_PLOT, plots = Q.filter((q) => /\(#13, Graphing Practice\)/.test(q.sourceNotes || ''));
  check(null, plots.length === 9, 'plot items ' + plots.length);
  for (const q of plots) {
    check(q, P.valid(q.plot) && P.check(q.plot, q.plot.testVectors.correct).ok && fs.existsSync(path.join(OUT, q.plot.answerKey.src)), 'plot item valid with an answer key');
    const want = q.fam;
    const m = /equals (\d+)\/(\d+)\./.exec(q.prompt) || /Drag the dot to (\d+)\/(\d+)\./.exec(q.prompt);
    if (m) check(q, q.plot.target.values.length === 1 && tf(q.plot.target.values[0]).cmp(tf(`${m[1]}/${m[2]}`)) === 0, 'plot target');
    const c = /Place a dot at (\d+\/\d+) and a dot at (\d+\/\d+)\./.exec(q.prompt);
    if (c) check(q, q.plot.target.values.length === 2 && [c[1], c[2]].every((v) => q.plot.target.values.includes(v)), 'plot targets');
  }
  const units = (fs.readFileSync(path.join(OUT, 'data.js'), 'utf8').match(/"grade3": \[([^\]]*)\]/) || [])[1] || '';
  check(null, /equivalent-comparing-fractions/.test(units), 'Graphing Practice lists the equivalent and comparing fractions unit');
}

if (fails.length) { console.error(fails.length + ' failures:\n' + fails.slice(0, 60).join('\n')); process.exit(1); }
console.log(`PASS 3rd Grade Math audit (${checks} checks, ${A1.length} Advanced and ${S7.length} Standard rewrites, ${O4.length} open-response, ${S8.length} select-all items)`);
