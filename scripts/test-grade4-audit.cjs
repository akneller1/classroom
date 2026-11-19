#!/usr/bin/env node
/* 4th Grade Math audit (2026-11-19): checks on the assembled site after scripts/apply-grade4-audit.mjs.
   Every new or rewritten item's answer is recomputed here from its prompt, independently of the authoring scripts in
   tools/grade4-audit-20261119. Usage: node scripts/test-grade4-audit.cjs [_site] */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm'), assert = require('assert/strict');
const OUT = path.resolve(process.argv[2] || '_site');
const UNITS = fs.readdirSync(path.join(OUT, 'question-banks/grade4')).filter((f) => f.endsWith('.json')).map((f) => f.replace('.json', ''));
const Q = [], N = [];
for (const u of UNITS) {
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'question-banks/grade4', u + '.json'), 'utf8')).questions) Q.push(Object.assign({ unit: u }, q));
  for (const q of JSON.parse(fs.readFileSync(path.join(OUT, 'grade4/question-banks/math4', u + '.json'), 'utf8')).questions) N.push(Object.assign({ unit: u }, q));
}
const byId = Object.fromEntries(Q.map((q) => [q.id, q]));
const fails = []; let checks = 0;
const check = (q, ok, msg) => { checks++; if (!ok) fails.push((q && q.id ? q.id + ': ' : '') + msg); };
const fam = (q) => ((q.sourceNotes || '').match(/family: ([\w-]+)\)/) || [])[1] || '';
const mask = (s) => s.replace(/-?\d+(?:,\d{3})*(?:\.\d+)?/g, '#');

/* ---------- numbers ---------- */
const gcd = (a, b) => (b ? gcd(b, a % b) : Math.abs(a));
const n = (x) => Number(x).toLocaleString('en-US');
const N_ = (s) => +String(s).replace(/[,$]/g, '');
class R { constructor(a, b = 1) { const g = gcd(a, b) || 1; this.a = a / g * Math.sign(b || 1); this.b = Math.abs(b / g); } add(o) { return new R(this.a * o.b + o.a * this.b, this.b * o.b); } sub(o) { return this.add(new R(-o.a, o.b)); } mul(o) { return new R(this.a * o.a, this.b * o.b); } div(o) { return new R(this.a * o.b, this.b * o.a); } cmp(o) { return this.a * o.b - o.a * this.b; } }
const fr = (s) => { s = String(s).trim(); let m = /^(\d+) (\d+)\/(\d+)$/.exec(s); if (m) return new R(+m[1] * +m[3] + +m[2], +m[3]); m = /^(\d+)\/(\d+)$/.exec(s); if (m) return new R(+m[1], +m[2]); if (/^\d*\.\d+$/.test(s)) { const d = 10 ** s.split('.')[1].length; return new R(Math.round(+s * d), d); } return new R(N_(s)); };
const F = (x) => { if (x.b === 1) return n(x.a); const w = Math.floor(x.a / x.b), r = x.a - w * x.b; return w ? `${w} ${r}/${x.b}` : `${r}/${x.b}`; };
const isPrime = (p) => p > 1 && [...Array(Math.floor(Math.sqrt(p)) + 1).keys()].slice(2).every((d) => p % d);
const factors = (k) => [...Array(k).keys()].map((i) => i + 1).filter((d) => k % d === 0);
const rnd = (x, u) => Math.floor(x / u + 0.5) * u;
const g = (re, s) => { const m = re.exec(s); if (!m) throw Error('prompt shape ' + re); return m; };
const ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth'];
const DNAME = { 2: 'halves', 3: 'thirds', 4: 'fourths', 5: 'fifths', 6: 'sixths', 8: 'eighths', 10: 'tenths', 12: 'twelfths' };
const SING = { feet: 'foot', inches: 'inch', yards: 'yard', ounces: 'ounce', pounds: 'pound', cups: 'cup', quarts: 'quart', pints: 'pint', gallons: 'gallon', grams: 'gram', meters: 'meter', 'empty seats': 'empty seat' };
const qty = (x, u) => `${x} ${x === '1' || x === 1 ? SING[u] || u : u}`;
const tm = (m) => `${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}`;
const CONV = { 'feet,inches': 12, 'yards,feet': 3, 'yards,inches': 36, 'pounds,ounces': 16, 'gallons,quarts': 4, 'quarts,pints': 2, 'pints,cups': 2, 'meters,centimeters': 100, 'kilometers,meters': 1000, 'centimeters,millimeters': 10, 'kilograms,grams': 1000, 'liters,milliliters': 1000, 'gallons,cups': 16 };

/* ---------- recomputation of the #1 Advanced and #7 Standard families ---------- */
const RC = {
  pv1_ten_times_chain: (p) => { const m = g(/is (\d+) times as much as ([\d,]+)/, p); return n(+m[1] * N_(m[2])); },
  pv1_value_times_ten: (p) => { const m = g(/digit (\d) in ([\d,]+)\?/, p), s = m[2].replace(/,/g, ''), v = +m[1] * 10 ** (s.length - 1 - s.indexOf(m[1])); return `${n(v)}; ${n(v * 10)}`; },
  pv1_how_many_times_far: (p) => { const P = { 'hundred thousands': 1e5, 'ten thousands': 1e4, thousands: 1e3, hundreds: 100, tens: 10, ones: 1 }, m = g(/in the ([a-z ]+?) place is how many times the value of the \d in the ([a-z ]+?) place/, p); return n(P[m[1]] / P[m[2]]); },
  pv2_expanded_then_more: (p) => { const m = g(/Write (.*) in standard form\. Then write the number that is ([\d,]+) more/, p); return n(m[1].split(' + ').reduce((a, x) => a + N_(x), 0) + N_(m[2])); },
  pv2_regroup_units: (p) => { const m = g(/has (\d+) thousands, (\d+) hundreds, (\d+) tens and (\d+) ones/, p); return n(m[1] * 1000 + m[2] * 100 + m[3] * 10 + +m[4]); },
  pv3_order_then_difference: (p) => { const v = g(/greatest: (.*)\. Then/, p)[1].split(/, (?=\d{3},)/).map(N_); return n(Math.max(...v) - Math.min(...v)); },
  pv3_digit_cards: (p) => { const d = g(/once: ([\d, ]+)\./, p)[1].split(', '); return n(+[...d].sort().reverse().join('') - +[...d].sort().join('')); },
  pv3_thousands_between: (p) => { const m = g(/greater than ([\d,]+) and less than ([\d,]+)/, p), lo = N_(m[1]), hi = N_(m[2]); let k = 0; for (let x = Math.floor(lo / 1000 + 1) * 1000; x < hi; x += 1000) k++; return String(k); },
  pv4_round_then_add: (p) => { const m = g(/Round ([\d,]+) and ([\d,]+) to the nearest (hundred|thousand)/, p), u = m[3] === 'hundred' ? 100 : 1000; return n(rnd(N_(m[1]), u) + rnd(N_(m[2]), u)); },
  pv4_rounding_range: (p) => { const m = g(/nearest (hundred|thousand)/, p); return n((m[1] === 'hundred' ? 100 : 1000) - 1); },
  as1_add_then_check: (p) => { const m = g(/Add ([\d,]+) \+ ([\d,]+)\. Then add ([\d,]+)/, p); return n(N_(m[1]) + N_(m[2]) + N_(m[3])); },
  as1_missing_then_more: (p) => { const m = g(/([\d,]+) \+ ___ = ([\d,]+)\. What number is ([\d,]+) more/, p); return n(N_(m[2]) - N_(m[1]) + N_(m[3])); },
  as1_sum_minus: (p) => { const m = g(/sold ([\d,]+) items in May and ([\d,]+) items in June\. In July it sold ([\d,]+) fewer/, p); return n(N_(m[1]) + N_(m[2]) - N_(m[3])); },
  as1_three_with_check: (p) => { const m = g(/have ([\d,]+), ([\d,]+) and ([\d,]+) people/, p); return n(2 * (N_(m[1]) + N_(m[2]) + N_(m[3]))); },
  as2_subtract_then_check: (p) => { const m = g(/Subtract ([\d,]+) − ([\d,]+)/, p); return n(N_(m[1]) - N_(m[2])); },
  as2_two_subtractions: (p) => { const m = g(/had ([\d,]+) visitors this year\. ([\d,]+) came in spring and ([\d,]+) came/, p); return n(N_(m[1]) - N_(m[2]) - N_(m[3])); },
  as2_difference_then_more: (p) => { const m = g(/Lake A has ([\d,]+) fish and Lake B has ([\d,]+) fish.*Then ([\d,]+) fish/, p); return n(N_(m[1]) - N_(m[2]) - N_(m[3])); },
  as3_across_zeros_then_add: (p) => { const m = g(/Subtract ([\d,]+) − ([\d,]+)\. Then add ([\d,]+)/, p); return n(N_(m[1]) - N_(m[2]) + N_(m[3])); },
  as3_unknown_start: (p) => { const m = g(/from ([\d,]+) and got ([\d,]+)/, p); return n(N_(m[1]) - N_(m[2])); },
  as3_two_from_round: (p) => { const m = g(/goal is ([\d,]+) steps\. \w+ walks ([\d,]+) steps in the morning and ([\d,]+)/, p); return n(N_(m[1]) - N_(m[2]) - N_(m[3])); },
  as3_compare_two_gaps: (p) => { const m = g(/Class A has ([\d,]+) points and Class B has ([\d,]+) points/, p); return n(N_(m[2]) - N_(m[1])); },
  as4_estimate_then_compare: (p) => { const m = g(/Estimate ([\d,]+) \+ ([\d,]+)/, p), a = N_(m[1]), b = N_(m[2]); return n(Math.abs(rnd(a, 100) + rnd(b, 100) - a - b)); },
  as4_estimate_misleads: (p) => { const m = g(/needs \$([\d,]+)\. It raised \$([\d,]+), \$([\d,]+) and \$([\d,]+)/, p); return N_(m[2]) + N_(m[3]) + N_(m[4]) >= N_(m[1]) ? 'yes' : 'no'; },
  as5_two_step_steps: (p) => { const m = g(/had ([\d,]+) points, earned ([\d,]+) more, and then spent ([\d,]+)/, p); return n(N_(m[1]) + N_(m[2]) - N_(m[3])); },
  as5_start_unknown_two_step: (p) => { const m = g(/got ([\d,]+) new books and gave away ([\d,]+) old books\. Now it has ([\d,]+)/, p); return n(N_(m[3]) + N_(m[2]) - N_(m[1])); },
  ms1_times_then_more: (p) => { const m = g(/has (\d+) stickers\. \w+ has (\d+) times as many/, p); return String(+m[1] + m[1] * m[2]); },
  ms1_difference_known: (p) => { const m = g(/is (\d+) times as long as a blue rope\. The red rope is (\d+) feet longer/, p); return `${m[2] / (m[1] - 1)} feet`; },
  ms2_two_products: (p) => { const m = g(/Find (\d+) × ([\d,]+) and (\d+) × ([\d,]+)/, p); return n(m[1] * N_(m[2]) + m[3] * N_(m[4])); },
  ms2_missing_multiple: (p) => { const m = g(/(\d+) × ___ = ([\d,]+)/, p); return n(N_(m[2]) / m[1]); },
  ms2_product_of_tens: (p) => { const m = g(/Multiply ([\d,]+) × ([\d,]+)\./, p); return n(N_(m[1]) * N_(m[2])); },
  ms2_zeros_count: (p) => { const m = g(/product ([\d,]+) × ([\d,]+)\?/, p), s = String(N_(m[1]) * N_(m[2])); return String(s.length - s.replace(/0+$/, '').length); },
  ms3_product_then_add: (p) => { const m = g(/has (\d+) \w+ with ([\d,]+) beads in each and (\d+) loose/, p); return n(m[1] * N_(m[2]) + +m[3]); },
  ms3_compare_two_products: (p) => { const m = g(/sold (\d+) shows with ([\d,]+) seats each\. Theater B sold (\d+) shows with ([\d,]+) seats/, p); return n(m[1] * N_(m[2]) - m[3] * N_(m[4])); },
  ms4_product_then_subtract: (p) => { const m = g(/There are (\d+) rows with (\d+) chairs in each row\. (\d+) chairs/, p); return n(m[1] * m[2] - m[3]); },
  ms4_two_area_models: (p) => { const m = g(/A is (\d+) feet by (\d+) feet\. Garden B is (\d+) feet by (\d+) feet/, p); return `${n(m[1] * m[2] + m[3] * m[4])} square feet`; },
  ms5_estimate_then_exact: (p) => { const m = g(/Estimate (\d+) × (\d+)/, p); return n(Math.abs(rnd(+m[1], 10) * rnd(+m[2], 10) - m[1] * m[2])); },
  ms5_budget: (p) => { const m = g(/has \$([\d,]+)\. Tickets cost \$(\d+) each, and (\d+) students/, p), d = N_(m[1]) - m[2] * m[3]; return `$${n(Math.abs(d))} ${d > 0 ? 'left' : 'short'}`; },
  dv1_unit_form_then_number: (p) => { const P = { tens: 10, hundreds: 100 }, m = g(/(\d+) (tens|hundreds) ÷ (\d+)/, p); return n(m[1] / m[3] * P[m[2]]); },
  dv1_fact_then_extend: (p) => { const m = g(/find ([\d,]+) ÷ (\d+)\. Then find [\d,]+ ÷ (\d+)/, p); return `${n(N_(m[1]) / m[2])}; ${n(N_(m[1]) / m[3])}`; },
  dv1_share_then_group: (p) => { const m = g(/([\d,]+) beads are shared equally among (\d+) bins\. .* into (\d+) bags/, p); return n(N_(m[1]) / m[2] / m[3]); },
  dv1_missing_dividend: (p) => { const m = g(/___ ÷ (\d+) = ([\d,]+)/, p); return n(m[1] * N_(m[2])); },
  dv2_partial_quotients_full: (p) => { const m = g(/find (\d+) ÷ (\d+): first take away \d+ × (\d+)/, p); return `${m[1] - m[2] * m[3]}; ${m[1] / m[2]}`; },
  dv2_area_model_three: (p) => { const m = g(/for ([\d,]+) ÷ (\d+)/, p); return n(N_(m[1]) / m[2]); },
  dv3_divide_then_check: (p) => { const m = g(/Divide ([\d,]+) ÷ (\d+)/, p); return n(N_(m[1]) / m[2]); },
  dv3_zero_in_quotient: (p) => { const m = g(/Divide ([\d,]+) ÷ (\d+)/, p); return n(N_(m[1]) / m[2]); },
  dv3_divide_then_compare: (p) => { const m = g(/packed ([\d,]+) apples into bags of (\d+)\. It sold (\d+) times/, p); return n(N_(m[1]) / m[2] / (+m[3] + 1)); },
  dv3_divide_then_subtract: (p) => { const m = g(/([\d,]+) seeds are planted equally in (\d+) rows\. Then (\d+) seeds/, p); return n(N_(m[1]) / m[2] - m[3]); },
  dv4_remainder_then_check: (p) => { const m = g(/Divide ([\d,]+) ÷ (\d+)/, p), a = N_(m[1]), d = +m[2]; return `${Math.floor(a / d)} R ${a % d}`; },
  dv4_which_quotient: (p) => { const m = g(/(\d+) pencils are put into boxes of (\d+)/, p); return `${Math.floor(m[1] / m[2])} R ${m[1] % m[2]}`; },
  dv4_least_to_add: (p) => { const m = g(/add to ([\d,]+) so that it divides by (\d+)/, p), a = N_(m[1]), d = +m[2]; return String((d - a % d) % d); },
  dv4_greatest_with_remainder: (p) => { const m = g(/less than ([\d,]+) that leaves a remainder of (\d+) when divided by (\d+)/, p), t = N_(m[1]), r = +m[2], d = +m[3]; let x = t - 1; while (x % d !== r) x--; return n(x); },
  dv5_round_up_then_spare: (p) => { const m = g(/(\d+) students ride vans that hold (\d+)/, p), t = +m[1], c = +m[2], v = Math.ceil(t / c); return `${v} vans; ${qty(String(v * c - t), 'empty seats')}`; },
  dv5_cost_with_remainder: (p) => { const m = g(/packs of (\d+)\. Each pack costs \$(\d+)\. A class needs (\d+)/, p); return `$${n(Math.ceil(m[3] / m[1]) * m[2])}`; },
  fm1_count_and_sum_pairs: (p) => String(factors(+g(/factor pairs of (\d+)/, p)[1]).length),
  fm1_rows_range: (p) => { const m = g(/(\d+) chairs .* at least (\d+) chairs/, p), k = +m[1], lo = +m[2]; return String(factors(k).filter((d) => d >= lo && k / d >= lo).length); },
  fm2_common_multiples: (p) => { const m = g(/from 1 to (\d+) are multiples of both (\d+) and (\d+)/, p); let c = 0; for (let x = 1; x <= +m[1]; x++) if (x % m[2] === 0 && x % m[3] === 0) c++; return String(c); },
  fm2_both_schedules: (p) => { const m = g(/every (\d+) minutes and Bus B every (\d+) minutes/, p), a = +m[1], b = +m[2]; return `${a * b / gcd(a, b)} minutes`; },
  fm3_count_composite: (p) => { const m = g(/between (\d+) and (\d+)\?/, p); let c = 0; for (let x = +m[1] + 1; x < +m[2]; x++) if (x > 1 && !isPrime(x)) c++; return String(c); },
  fm3_prime_pair_product: () => '4 factors; composite',
  fm3_sum_of_primes: (p) => { const m = g(/between (\d+) and (\d+)\?/, p); let s = 0; for (let x = +m[1] + 1; x < +m[2]; x++) if (isPrime(x)) s += x; return String(s); },
  fm4_subtract_rule_term: (p) => { const m = g(/starts at (\d+) and subtracts (\d+) each time\. What is the (\w+) number/, p); return String(m[1] - m[2] * ORD.indexOf(m[3])); },
  fm4_rule_then_term: (p) => { const m = g(/starts ([\d, ]+), \.\.\. What is the rule, and what is the (\w+) number/, p), s = m[1].split(', ').map(Number), d = s[1] - s[0]; return `add ${d}; ${s[0] + d * ORD.indexOf(m[2])}`; },
  fm4_first_over: (p) => { const m = g(/starts at (\d+) and adds (\d+) each time\. .* greater than (\d+)/, p); let x = +m[1]; while (x <= +m[3]) x += +m[2]; return String(x); },
  fe1_split_then_name: (p) => { const m = g(/shows (\d+)\/(\d+) shaded\. Each part is split into (\d+)/, p); return `${m[1] * m[3]}; ${m[1] * m[3]}/${m[2] * m[3]}`; },
  fe1_same_amount_different_pieces: (p) => { const m = g(/into (\d+) equal pieces and ate (\d+)\. \w+ cut the same size pan into (\d+)/, p); return String(m[2] * m[3] / m[1]); },
  fe2_missing_then_check: (p) => { const m = g(/(\d+)\/(\d+) = ___\/(\d+)/, p), k = m[3] / m[2]; return `${m[1] * k}/${m[3]}; ${k}`; },
  fe2_two_equivalents: (p) => { const m = g(/equivalent to (\d+)\/(\d+): one with denominator (\d+) and one with denominator (\d+)/, p); return `${m[1] * m[3] / m[2]}/${m[3]}, ${m[1] * m[4] / m[2]}/${m[4]}`; },
  fe2_from_sum: (p) => { const m = g(/equivalent to (\d+)\/(\d+)\. Its numerator and denominator add up to (\d+)/, p), k = m[3] / (+m[1] + +m[2]); return `${m[1] * k}/${m[2] * k}`; },
  fe2_count_equivalents: (p) => { const m = g(/equal to (\d+)\/(\d+) have a denominator of 12/, p), b = +m[2]; return String(Math.floor(12 / b)); },
  fe3_three_like: (p) => { const m = g(/greatest: (.*)\. Then/, p), v = m[1].split(', ').map((x) => +x.split('/')[0]), b = m[1].split(', ')[0].split('/')[1]; return `${Math.max(...v) - Math.min(...v)}/${b}`; },
  fe3_same_numerator_story: (p) => { const m = g(/(\w+) ate (\d+)\/(\d+) of a pizza\. (\w+) ate \d+\/(\d+)/, p), b1 = +m[3], b2 = +m[5]; return `${b1 < b2 ? m[1] : m[4]}, because ${DNAME[Math.min(b1, b2)]} are bigger pieces than ${DNAME[Math.max(b1, b2)]}`; },
  fe3_same_numerator_three: (p) => { const m = g(/greatest to least: (.*)\.$/, p); return m[1].split(', ').sort((x, y) => +x.split('/')[1] - +y.split('/')[1]).join(', '); },
  fe4_half_then_closest: (p) => { const m = g(/Is (\d+)\/(\d+) greater/, p); return 2 * m[1] > +m[2] ? 'greater' : 'less'; },
  fe4_benchmark_explain: (p) => { const m = g(/for (\d+\/\d+) ___ (\d+\/\d+)/, p), c = fr(m[1]).cmp(fr(m[2])); return c > 0 ? '>' : c < 0 ? '<' : '='; },
  fe4_count_more_than_half: (p) => String(g(/1\/2: (.*)\?$/, p)[1].split(', ').filter((x) => fr(x).cmp(new R(1, 2)) > 0).length),
  fe4_both_above_half: (p) => { const m = g(/Both (\d+\/\d+) and (\d+\/\d+)/, p); return fr(m[1]).cmp(fr(m[2])) > 0 ? m[1] : m[2]; },
  fe5_order_using_twelfths: (p) => g(/twelfths: (.*)\.$/, p)[1].split(', ').sort((x, y) => fr(x).cmp(fr(y))).join(', '),
  fe5_twelfths_between: (p) => { const m = g(/greater than (\d+\/\d+) and less than (\d+\/\d+)/, p); let c = 0; for (let k = 1; k < 12; k++) if (new R(k, 12).cmp(fr(m[1])) > 0 && new R(k, 12).cmp(fr(m[2])) < 0) c++; return String(c); },
  fd1_three_part_sum: (p) => { const m = g(/(\d+)\/(\d+) = (\d+)\/\d+ \+ 1\/\d+ \+ ___/, p); return `${m[1] - m[3] - 1}/${m[2]}`; },
  fd1_two_ways: (p) => { const m = g(/Write (\d+)\/(\d+) as a sum .* One of them is (\d+)\//, p); return `${m[1] - m[3]}/${m[2]}`; },
  fd1_mixed_unit_count: (p) => { const m = g(/^(\d+) (\d+)\/(\d+) is how many/, p); return `${m[1] * m[3] + +m[2]}; ${m[1] * m[3]}/${m[3]} + ${m[2]}/${m[3]}`; },
  fd1_count_two_part: (p) => String(Math.floor(+g(/can (\d+)\//, p)[1] / 2)),
  fd2_add_then_subtract: (p) => { const m = g(/had (\d+)\/(\d+) of a jug .* added (\d+)\/\d+ .* poured out (\d+)\//, p); return `${+m[1] + +m[3] - m[4]}/${m[2]}`; },
  fd2_rest_of_whole: (p) => { const m = g(/into (\d+) equal beds\. (\d+)\/\d+ of the garden is beans and (\d+)\//, p); return `${m[1] - m[2] - m[3]}/${m[1]}`; },
  fd3_add_with_regroup: (p) => { const m = g(/Add (\d+ \d+\/\d+) \+ (\d+ \d+\/\d+)/, p); return F(fr(m[1]).add(fr(m[2]))); },
  fd3_two_cuts_left: (p) => { const m = g(/is (\d+) feet long\. \w+ cuts off (\d+ \d+\/\d+) feet and then (\d+ \d+\/\d+) feet/, p); return qty(F(new R(+m[1]).sub(fr(m[2])).sub(fr(m[3]))), 'feet'); },
  fd3_subtract_rename: (p) => { const m = g(/Subtract (\d+ \d+\/\d+) − (\d+ \d+\/\d+)/, p); return F(fr(m[1]).sub(fr(m[2]))); },
  fd4_multiply_then_mixed: (p) => { const m = g(/Multiply (\d+) × (\d+)\/(\d+)/, p), a = m[1] * m[2], b = +m[3]; return a % b ? `${Math.floor(a / b)} ${a % b}/${b}` : String(a / b); },
  fd4_enough: (p) => { const m = g(/uses (\d+)\/(\d+) cup .* makes (\d+) batches and has (\d+) cups/, p), x = new R(m[1] * m[3], +m[2]).sub(new R(+m[4])); return x.a === x.b ? '1 cup' : `${F(x)} cups`; },
  fd5_tenths_plus_hundredths: (p) => { const m = g(/Add (\d+)\/10 \+ (\d+)\/100/, p), v = m[1] * 10 + +m[2]; return `${v}/100; 0.${String(v).padStart(2, '0')}`; },
  fd5_coins_decimal: (p) => { const m = g(/has (\d+) dimes and (\d+) pennies/, p), v = m[1] * 10 + +m[2]; return `0.${String(v).padStart(2, '0')}`; },
  fd6_order_four: (p) => g(/greatest: (.*)\.$/, p)[1].split(', ').sort((x, y) => +x - +y).join(', '),
  fd6_mixed_forms_difference: (p) => { const v = [...p.matchAll(/ran ([\d./ +]+?) mile/g)].map((m) => m[1].split(' + ').reduce((a, t) => a.add(fr(t)), new R(0))); const mx = v.reduce((a, b) => (a.cmp(b) > 0 ? a : b)), mn = v.reduce((a, b) => (a.cmp(b) < 0 ? a : b)), d = mx.sub(mn); return (d.a / d.b).toFixed(2); },
  mc1_mixed_then_use: (p) => { const m = g(/has (\d+) (\w+) (\d+) (\w+) of \w+ and uses (\d+)/, p); return `${m[1] * CONV[m[2] + ',' + m[4]] + +m[3] - m[5]} ${m[4]}`; },
  mc1_convert_then_share: (p) => { const m = g(/^(\d+) (\w+) of \w+ is shared equally into (\d+) parts\. How many (\w+)/, p); return `${m[1] * CONV[m[2] + ',' + m[4]] / m[3]} ${m[4]}`; },
  mc2_convert_then_subtract: (p) => { const m = g(/has (\d+) (\w+) (\d+) (\w+) of \w+\. (\d+) \w+ are used/, p); return `${n(m[1] * CONV[m[2] + ',' + m[4]] + +m[3] - m[5])} ${m[4]}`; },
  mc2_how_much_more: (p) => { const m = g(/needs (\d+) (\w+) of \w+\. She has (\d+) pieces that are each (\d+) (\w+)/, p); return `${n(m[1] * CONV[m[2] + ',' + m[5]] - m[3] * m[4])} ${m[5]}`; },
  mc3_two_activities: (p) => { const m = g(/at (\d+):(\d+)\. \w+ reads for (\d+) minutes and then practices piano for (\d+) minutes/, p); return tm(m[1] * 60 + +m[2] + +m[3] + +m[4]); },
  mc3_backward_with_break: (p) => { const m = g(/ended at (\d+):(\d+)\. It had (\d+) minutes of play and a (\d+)-minute break/, p); return tm(m[1] * 60 + +m[2] - m[3] - m[4]); },
  mc4_two_items_change: (p) => { const m = g(/book for \$([\d.]+) and a pen for \$([\d.]+)\. \w+ pays with a \$(\d+) bill/, p); return '$' + ((m[3] * 100 - Math.round(m[1] * 100) - Math.round(m[2] * 100)) / 100).toFixed(2); },
  mc4_how_many_servings: (p) => { const m = g(/holds (\d+) (\w+) of \w+\. Each serving uses (\d+) (\w+)/, p); return `${m[1] * CONV[m[2] + ',' + m[4]] / m[3]} servings`; },
  mc5_scaled_area: (p) => { const m = g(/is (\d+) meters long and (\d+) meters wide\. A second rectangle is (\d+) times as long/, p); return `${m[1] * m[2] * m[3]} square meters`; },
  mc5_area_from_perimeter: (p) => { const m = g(/perimeter of (\d+) feet\. Its width is (\d+) feet/, p); return `${(m[1] / 2 - m[2]) * m[2]} square feet`; },
  ga1_angle_and_partner: (p) => { const b = 180 - +g(/One is (\d+)°/, p)[1]; return b < 90 ? 'acute' : b === 90 ? 'right' : 'obtuse'; },
  ga1_crossing_lines: (p) => { const a = +g(/One angle measures (\d+)°/, p)[1]; return `${180 - a}°, ${a}°, ${180 - a}°`; },
  ga2_reading_both_scales: (p) => `${g(/passes through (\d+)° on that scale/, p)[1]}°`,
  ga2_protractor_offset_type: (p) => { const m = g(/passes through (\d+)° and the other through (\d+)°/, p), d = m[2] - m[1]; return `${d}°, ${d < 90 ? 'acute' : d === 90 ? 'right' : 'obtuse'}`; },
  ga2_turn_parts: (p) => { const m = g(/through 1\/(\d+) of a full circle, (\d+) times/, p); return `${360 * m[2] / m[1]}°`; },
  ga3_two_parts_then_straight: (p) => { const m = g(/measure (\d+)° and (\d+)°/, p); return `${180 - m[1] - m[2]}°`; },
  ga3_equal_parts_and_rest: (p) => { const m = g(/^(\d+) equal angles of (\d+)°/, p); return `${180 - m[1] * m[2]}°`; },
  ga4_third_angle_then_classify: (p) => { const m = g(/triangle are (\d+)° and (\d+)°/, p), c = 180 - m[1] - m[2], mx = Math.max(+m[1], +m[2], c); return `${c}°, ${mx < 90 ? 'acute' : mx === 90 ? 'right' : 'obtuse'}`; },
  ga4_exterior_then_classify: (p) => { const m = g(/angles of (\d+)° and (\d+)°/, p), c = 180 - m[1] - m[2], mx = Math.max(+m[1], +m[2], c); return `${c}°; ${mx < 90 ? 'acute' : 'obtuse'}`; },
  ga4_all_names: (p) => { const m = g(/sides (\d+), (\d+), \d+ and \d+ units/, p); return m[1] === m[2] ? 'square, rectangle, rhombus, parallelogram' : 'rectangle, parallelogram'; },
  ga5_half_shape_perimeter: (p) => `${2 * g(/One half has an area of (\d+)/, p)[1]} square inches`,
  ga5_two_shapes_total: (p) => { const L = { square: 4, 'rectangle that is not a square': 2, 'equilateral triangle': 3, 'regular hexagon': 6, 'isosceles triangle that is not equilateral': 1, 'rhombus that is not a square': 2, 'regular pentagon': 5, 'regular octagon': 8 }, m = g(/does an? (.+?) have\? An? (.+?)\? Give/, p); return String(L[m[1]] + L[m[2]]); },
  dp3_groups_plus_extra_minus: (p) => { const m = g(/has (\d+) boxes with (\d+) crayons each and (\d+) loose crayons\. \w+ gives away (\d+)/, p); return String(m[1] * m[2] + +m[3] - m[4]); },
  dp3_buses_then_vans: (p) => { const m = g(/^(\d+) students go on a trip\. (\d+) buses each hold (\d+) students\. .* hold (\d+) students/, p); return `${Math.ceil((m[1] - m[2] * m[3]) / m[4])} vans`; },
  dp4_value_with_letter: (p) => { const m = g(/n = (\d+) × (\d+) − (\d+)/, p); return String(m[1] * m[2] - m[3]); },
  dp4_letter_then_check: (p) => { const m = g(/buys (\d+) games for \$(\d+) each and a \$(\d+) controller/, p); return `t = ${m[1]} × ${m[2]} + ${m[3]}; t = $${m[1] * m[2] + +m[3]}`; },
  dp4_solve_for_per: (p) => { const m = g(/(\d+) × c \+ (\d+) = (\d+)/, p); return String((m[3] - m[2]) / m[1]); },
  // Standard families of fams.S not seen above
  fm5_count_in_first: (p) => { const m = g(/repeats (.*)\. How many (\w+)s are in the first (\d+) shapes/, p), unit = m[1].split(', '); let c = 0; for (let i = 0; i < +m[3]; i++) if (unit[i % unit.length] === m[2]) c++; return String(c); },
  fm5_tiles_total: (p) => { const m = g(/Figure 1 has (\d+) tiles, and each figure has (\d+) more/, p); return String(5 * m[1] + 10 * m[2]); }
};
const A1 = Q.filter((q) => /\(#1, Advanced/.test(q.sourceNotes || '')), S7 = Q.filter((q) => /\(#7, Standard\)/.test(q.sourceNotes || ''));
check(null, A1.length >= 450, 'Advanced rewrites ' + A1.length);
check(null, S7.length >= 400, 'Standard rewrites ' + S7.length);
for (const q of [...A1, ...S7]) {
  const f = fam(q), fn = RC[f];
  check(q, !!fn, 'no recomputation for ' + f);
  if (!fn) continue;
  let want; try { want = fn(q.prompt); } catch (e) { check(q, false, e.message); continue; }
  check(q, String(q.answer) === want, `key ${q.answer} but recomputed ${want}`);
  check(q, (A1.includes(q) ? q.level === 'honors' : q.level === 'cp1'), 'level');
  if (q.format === 'multiple-choice') check(q, q.options.filter((o) => o.correct).length === 1 && q.options.find((o) => o.correct).text === q.answer && new Set(q.options.map((o) => o.text)).size === q.options.length, 'options');
}
// the rewrites no longer reuse a lower-level template, and levels stay the same size
for (const q of [...A1, ...S7]) {
  const lower = new Set(Q.filter((x) => x.skillId === q.skillId && (A1.includes(q) ? x.level !== 'honors' : x.level === 'cp2')).map((x) => mask(x.prompt)));
  check(q, !lower.has(mask(q.prompt)), 'still a lower-level template');
}
const share = (L, lo) => { const low = new Set(Q.filter((q) => lo.includes(q.level)).map((q) => q.skillId + '|' + mask(q.prompt))); const xs = Q.filter((q) => q.level === L && q.format !== 'plot'); return xs.filter((q) => low.has(q.skillId + '|' + mask(q.prompt))).length / xs.length; };
check(null, share('honors', ['cp2', 'cp1']) <= 0.33, 'Advanced items reusing a lower template ' + share('honors', ['cp2', 'cp1']).toFixed(2));
check(null, share('cp1', ['cp2']) <= 0.30, 'Standard items reusing a Support template ' + share('cp1', ['cp2']).toFixed(2));
const lv = (L) => Q.filter((q) => q.level === L && q.format !== 'plot').length;
check(null, lv('cp2') === lv('cp1') && lv('cp1') === lv('honors'), `levels ${lv('cp2')}/${lv('cp1')}/${lv('honors')}`);

/* ---------- #4 open response ---------- */
const O4 = Q.filter((q) => /\(#4, open response\)/.test(q.sourceNotes || ''));
const skills = [...new Set(Q.map((q) => q.skillId))];
assert.equal(skills.length, 49);
check(null, O4.length === 147, 'open-response items ' + O4.length);
for (const s of skills) for (const L of ['cp2', 'cp1', 'honors']) check({ id: s + '|' + L }, O4.some((q) => q.skillId === s && q.level === L), 'no context open-response item');
for (const q of O4) {
  check(q, q.parts.length === 4 && /^Sample answer: /.test(q.parts[3].answer) && q.solutionSteps.length === 4, 'four parts ending with an explanation');
  check(q, q.parts.slice(0, 3).some((p) => !/^Sample answer: /.test(p.answer)), 'at least one checked part');
}
const OR = {   // recompute the first checked part of each context family
  pv1_open_two_towns: (q) => [0, n(N_(g(/Town A has ([\d,]+) people/, q.prompt)[1]) * 10)],
  pv2_open_check: (q) => [2, n(N_(g(/for \$([\d,]+)\./, q.prompt)[1]) + 1000)],
  pv4_open_round: (q) => { const x = N_(g(/sold ([\d,]+) tickets/, q.prompt)[1]), u = N_(g(/multiples of ([\d,]+)/, q.parts[0].prompt)[1]); return [2, n(rnd(x, u))]; },
  as1_open_two_days: (q) => { const m = g(/had ([\d,]+) visitors on Saturday and ([\d,]+) visitors/, q.prompt); return [0, n(N_(m[1]) + N_(m[2]))]; },
  as2_open_fundraiser: (q) => { const m = g(/raise \$([\d,]+)\. It has raised \$([\d,]+)/, q.prompt); return [0, '$' + n(N_(m[1]) - N_(m[2]))]; },
  as3_open_goal: (q) => { const m = g(/goal of ([\d,]+) pages\. Members have read ([\d,]+)/, q.prompt); return [0, n(N_(m[1]) - N_(m[2]))]; },
  as4_open_estimate: (q) => { const m = g(/sold ([\d,]+) items in March and ([\d,]+) items/, q.prompt); return [1, n(N_(m[1]) + N_(m[2]))]; },
  as5_open_points: (q) => { const m = g(/had ([\d,]+) points\. It earned ([\d,]+) points and then lost ([\d,]+)/, q.prompt); return [1, n(N_(m[1]) + N_(m[2]) - N_(m[3]))]; },
  ms1_open_times_as_many: (q) => { const m = g(/has (\d+) shells\. Ben has (\d+) times/, q.prompt); return [1, String(m[1] * m[2])]; },
  ms2_open_boxes: (q) => { const m = g(/holds ([\d,]+) paper clips\. A store has (\d+) boxes/, q.prompt); return [0, n(N_(m[1]) * m[2])]; },
  ms3_open_partial: (q) => { const m = g(/packs ([\d,]+) eggs each day for (\d+) days/, q.prompt); return [2, n(N_(m[1]) * m[2])]; },
  ms4_open_area_model: (q) => { const m = g(/is (\d+) feet by (\d+) feet/, q.prompt); return [1, `${n(m[1] * m[2])} square feet`]; },
  ms5_open_trip: (q) => { const m = g(/costs \$(\d+) per student\. (\d+) students/, q.prompt); return [1, '$' + n(m[1] * m[2])]; },
  dv1_open_share: (q) => { const m = g(/([\d,]+) stickers are shared equally among (\d+) friends/, q.prompt); return [0, n(N_(m[1]) / m[2])]; },
  dv2_open_partial_quotients: (q) => { const m = g(/divide ([\d,]+) by (\d+)/, q.prompt); return [2, String(N_(m[1]) / m[2])]; },
  dv3_open_rows: (q) => { const m = g(/([\d,]+) chairs are set up in (\d+) equal rows/, q.prompt); return [0, n(N_(m[1]) / m[2])]; },
  dv4_open_remainder: (q) => { const m = g(/([\d,]+) marbles are put into bags of (\d+)/, q.prompt), t = N_(m[1]), d = +m[2]; return [0, `${Math.floor(t / d)} R ${t % d}`]; },
  dv5_open_vans: (q) => { const m = g(/(\d+) people are going on a trip\. Each van holds (\d+)/, q.prompt); return [1, String(Math.ceil(m[1] / m[2]))]; },
  fm1_open_garden: (q) => [1, String(factors(+g(/has (\d+) plants/, q.prompt)[1]).length)],
  fm2_open_packs: (q) => { const m = g(/packs of (\d+)\. Buns come in packs of (\d+)/, q.prompt); return [2, String(m[1] * m[2] / gcd(+m[1], +m[2]))]; },
  fm3_open_sort: (q) => { const m = g(/from (\d+) to (\d+)/, q.prompt); const ps = []; for (let x = +m[1]; x <= +m[2]; x++) if (isPrime(x)) ps.push(x); return [0, ps.join(', ')]; },
  fm4_open_rule: (q) => { const m = g(/starts at (\d+) and follows the rule "add (\d+)/, q.prompt); return [0, [0, 1, 2, 3, 4].map((i) => +m[1] + i * m[2]).join(', ')]; },
  fm5_open_tiles: (q) => { const m = g(/Figure 1 has (\d+) tiles\. Each figure has (\d+) more/, q.prompt); return [0, String(+m[1] + 3 * m[2])]; },
  fe1_open_brownies: (q) => { const m = g(/into (\d+) equal pieces, and (\d+) (?:is|are) eaten\. Each piece is then cut into (\d+)/, q.prompt); return [2, `${m[2] * m[3]}/${m[1] * m[3]}`]; },
  fe2_open_equivalents: (q) => { const m = g(/says (\d+)\/(\d+) = (\d+)\/(\d+)/, q.prompt); return [0, String(m[4] / m[2])]; },
  fe3_open_compare: (q) => { const m = g(/ate (\d+)\/\d+ of a pizza and Mei ate (\d+)\//, q.prompt); return [0, +m[1] > +m[2] ? 'Liam' : 'Mei']; },
  fe4_open_benchmark: () => [2, 'Femi'],
  fe5_open_order: (q) => [0, [...q.prompt.matchAll(/(\d+)\/(\d+) cup/g)].map((m) => `${m[1] * 12 / m[2]}/12`).join(', ')],
  fd1_open_decompose: (q) => [0, g(/needs (\d+)\//, q.prompt)[1]],
  fd2_open_paint: (q) => { const m = g(/into (\d+) equal parts\. Kai paints (\d+)\/\d+ of it in the morning and (\d+)\//, q.prompt); return [0, `${+m[2] + +m[3]}/${m[1]}`]; },
  fd3_open_trail: (q) => { const m = g(/hikes (\d+ \d+\/\d+) miles on Saturday and (\d+ \d+\/\d+) miles/, q.prompt); return [0, `${F(fr(m[1]).add(fr(m[2])))} miles`]; },
  fd4_open_recipe: (q) => { const m = g(/uses (\d+)\/(\d+) cup of sugar\. Ravi makes (\d+) batches/, q.prompt); return [1, `${m[1] * m[3]}/${m[2]}`]; },
  fd5_open_grid: (q) => { const m = g(/(\d+) columns of 10 and (\d+) more squares/, q.prompt); return [0, `${m[1] * 10 + +m[2]}/100`]; },
  fd6_open_jumps: (q) => { const xs = [...q.prompt.matchAll(/2\.(\d\d)/g)].map((m) => +m[1]).sort((a, b) => a - b); return [2, `0.${String(xs[2] - xs[0]).padStart(2, '0')}`]; },
  mc1_open_table: (q) => [0, String(CONV[g(/converts (\w+) to (\w+)/, q.prompt).slice(1).join(',')])],
  mc2_open_convert: (q) => { const m = g(/has (\d+) (\w+) of/, q.prompt), sm = g(/How many (\w+) is that/, q.parts[0].prompt)[1]; return [0, `${n(m[1] * CONV[m[2] + ',' + sm])} ${sm}`]; },
  mc3_open_movie: (q) => { const m = g(/starts at (\d+):(\d+) and lasts (\d+) minutes/, q.prompt); return [0, tm(m[1] * 60 + +m[2] + +m[3])]; },
  mc4_open_shopping: (q) => { const m = g(/kite for \$(\d+\.\d\d) and a ball for \$(\d+\.\d\d)/, q.prompt); return [0, '$' + ((Math.round(m[1] * 100) + Math.round(m[2] * 100)) / 100).toFixed(2)]; },
  mc5_open_garden: (q) => { const m = g(/is (\d+) feet long and (\d+) feet wide/, q.prompt); return [0, `${m[1] * m[2]} square feet`]; },
  ga1_open_clock: (q) => [1, `${180 - g(/angle of (\d+)°/, q.prompt)[1]}°`],
  ga2_open_protractor: (q) => { const m = g(/passes through (\d+)° and ray QS passes through (\d+)°/, q.prompt); return [0, `${m[2] - m[1]}°`]; },
  ga3_open_split: (q) => { const m = g(/ABD = (\d+)° and angle DBC = (\d+)°/, q.prompt); return [0, `${+m[1] + +m[2]}°`]; },
  ga4_open_triangle: (q) => { const m = g(/angles of (\d+)° and (\d+)°/, q.prompt); return [0, `${180 - m[1] - m[2]}°`]; },
  ga5_open_fold: (q) => { const L = { square: 4, rectangle: 2, 'equilateral triangle': 3, 'regular hexagon': 6 }; return [0, String(L[g(/folds a paper (.+) along/, q.prompt)[1]])]; },
  dp1_open_line_plot: (q) => [0, String(g(/inches: (.*)\.$/, q.prompt)[1].split(', ').length)],
  dp2_open_line_plot: (q) => { const v = g(/feet: (.*)\.$/, q.prompt)[1].split(', ').map(fr); return [0, qty(F(v.reduce((a, b) => a.add(b))), 'feet')]; },
  dp3_open_party: (q) => { const m = g(/buys (\d+) packs of (\d+) balloons and (\d+) single balloons, then shares them equally among (\d+) tables/, q.prompt), t = m[1] * m[2] + +m[3]; return [1, String(t / m[4])]; },
  dp4_open_cards: (q) => { const m = g(/has (\d+) packs .* and (\d+) loose cards\. He has (\d+) cards/, q.prompt); return [1, String((m[3] - m[2]) / m[1])]; },
  pv3_open_stadiums: (q) => { const v = [...q.prompt.matchAll(/ ([\d,]{5,})/g)].map((m) => N_(m[1])); return [2, n(Math.max(...v) - Math.min(...v))]; }
};
for (const q of O4) {
  const fn = OR[fam(q)];
  check(q, !!fn, 'no open-response recomputation for ' + fam(q));
  if (!fn) continue;
  try { const [i, want] = fn(q); check(q, q.parts[i].answer === want, `part ${i}: ${q.parts[i].answer} but recomputed ${want}`); } catch (e) { check(q, false, e.message); }
}

/* ---------- #8 select-all ---------- */
const S8 = Q.filter((q) => /\(#8, select-all/.test(q.sourceNotes || ''));
check(null, S8.length >= 57, 'select-all items ' + S8.length);
const SEL = {
  pv3_select_greater: (q, t) => N_(t) > N_(g(/greater than ([\d,]+)\./, q.prompt)[1]),
  pv4_select_rounds_to: (q, t) => { const m = g(/round to ([\d,]+) when rounded to the nearest (ten|hundred|thousand)\./, q.prompt), u = { ten: 10, hundred: 100, thousand: 1000 }[m[2]]; return rnd(N_(t), u) === N_(m[1]); },
  ms2_select_equal_products: (q, t) => t.split(' × ').reduce((a, x) => a * N_(x), 1) === N_(g(/equal to ([\d,]+)\./, q.prompt)[1]),
  dv4_select_remainder: (q, t) => { const m = /^(\d+) ÷ (\d+)$/.exec(t); return m[1] % m[2] === +g(/remainder of (\d+)/, q.prompt)[1]; },
  fm1_select_factors: (q, t) => +g(/factors of (\d+)/, q.prompt)[1] % +t === 0,
  fm2_select_multiples: (q, t) => +t % +g(/multiples of (\d+)/, q.prompt)[1] === 0,
  fm3_select_primes: (q, t) => isPrime(+t),
  fe2_select_equivalent: (q, t) => fr(t).cmp(fr(g(/equivalent to (\d+\/\d+)/, q.prompt)[1])) === 0,
  fe4_select_greater_half: (q, t) => fr(t).cmp(new R(1, 2)) > 0,
  fd4_select_equal_product: (q, t) => { const m = g(/equal to (\d+) × (\d+)\/(\d+)\./, q.prompt), want = new R(m[1] * m[2], +m[3]); let v; if (/×/.test(t)) { const [a, b] = t.split(' × '); v = fr(a).mul(fr(b)); } else v = t.split(' + ').reduce((a, x) => a.add(fr(x)), new R(0)); return v.cmp(want) === 0; },
  fd5_select_equal_decimal: (q, t) => t.split(' + ').reduce((a, x) => a.add(fr(x)), new R(0)).cmp(new R(+g(/equal to (\d+) hundredths/, q.prompt)[1], 100)) === 0,
  fd6_select_greater_decimal: (q, t) => +t > +g(/greater than ([\d.]+)\./, q.prompt)[1],
  mc1_select_equal_length: (q, t) => { const ft = +g(/equal to (\d+) feet/, q.prompt)[1]; let inch = 0; for (const m of t.matchAll(/(\d+) (yards?|feet|inches)/g)) inch += m[1] * { yard: 36, yards: 36, feet: 12, inches: 1 }[m[2]]; return inch === ft * 12; },
  mc5_select_area: (q, t) => { const m = /^(\d+) ft by (\d+) ft$/.exec(t); return m[1] * m[2] === +g(/area of (\d+)/, q.prompt)[1]; },
  ga1_select_angle_type: (q, t) => { const a = +t.replace('°', ''); return /acute/.test(q.prompt) ? a < 90 : a > 90 && a < 180; },
  ga4_select_names: (q, t) => ({ 'a square': ['rectangle', 'rhombus', 'parallelogram', 'quadrilateral'], 'a rectangle that is not a square': ['parallelogram', 'quadrilateral'], 'a rhombus that is not a square': ['parallelogram', 'quadrilateral'] })[g(/describe (.+)\.$/, q.prompt)[1]].includes(t),
  ga5_select_symmetry: (q, t) => { const L = { square: 4, 'rectangle (not a square)': 2, 'equilateral triangle': 3, 'regular hexagon': 6, 'isosceles triangle (not equilateral)': 1, 'rhombus (not a square)': 2, 'parallelogram (not a rectangle or rhombus)': 0, 'regular pentagon': 5, 'scalene triangle': 0 }; return L[t] >= +g(/at least (\d+)/, q.prompt)[1]; },
  fe3_select_less: (q, t) => fr(t).cmp(fr(g(/less than (\d+\/\d+)/, q.prompt)[1])) < 0,
  dp4_select_expression: (q, t) => { const m = g(/has (\d+) bags with (\d+) marbles in each and (\d+) loose/, q.prompt); const ev = (s) => { s = s.replace(/×/g, '*').replace(/−/g, '-'); if (!/^[\d\s+*()-]+$/.test(s)) throw Error('bad expression'); return Function('return ' + s)(); }; return ev(t) === m[1] * m[2] + +m[3]; }
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

/* ---------- small fixes #11 #14 #15 #16 #18 ---------- */
check(null, !Q.some((q) => (q.standards || []).includes('4.OA.A.3.a')), '4.OA.A.3.a retagged');
for (const q of Q) {
  const nums = (q.prompt + ' ' + (Array.isArray(q.answer) ? q.answer.join(' ') : q.answer)).match(/\d{1,3}(?:,\d{3})+/g) || [];
  check(q, nums.every((x) => N_(x) <= 1000000), 'number beyond 1,000,000');
  if (q.unit === 'division-remainders' || q.skillId === 'data-line-plots-word-problems-skill-03') check(q, !/(?:÷ |among |equally into )[1-9]\d(?![\d,])/.test(q.prompt), 'two-digit divisor: ' + q.prompt.slice(0, 60));
  check(q, !/A baker makes [\d,]+ (?:bars of soap|golf balls|candles|oranges)/.test(q.prompt), 'baker noun');
  const t = [...q.prompt.matchAll(/(\d{1,2}):(\d\d) (AM|PM)/g)].map((m) => (+m[1] % 12 + (m[3] === 'PM' ? 12 : 0)) * 60 + +m[2]);
  if (t.length >= 2) check(q, t[1] - t[0] <= 120, 'elapsed time over two hours');
}
for (const id of ['m4-fm-s03-cp2-008', 'm4-fe-s02-cp2-024', 'm4-ga-s04-cp2-015', 'm4-ga-s04-cp1-029']) {
  const q = byId[id], twin = Q.find((x) => x.id !== id && x.skillId === q.skillId && x.level === q.level && x.prompt === q.prompt && String(x.answer) === String(q.answer) && JSON.stringify(x.options) === JSON.stringify(q.options));
  check(q, !twin, 'duplicate of ' + (twin && twin.id));
}

/* ---------- both bank copies, players, standards map, card, pacing ---------- */
const nById = Object.fromEntries(N.map((q) => [q.id, q]));
for (const q of Q) {
  if (q.format === 'plot') { check(q, !nById[q.id], 'plot item in the Grade 4 players'); continue; }
  const x = nById[q.id];
  check(q, !!x, 'missing from the Grade 4 player bank');
  if (x) for (const k of ['prompt', 'answer', 'options', 'parts', 'level', 'standards', 'solutionSteps']) check(q, JSON.stringify(x[k]) === JSON.stringify(q[k]), 'copies differ in ' + k);
}
const meta = {};
for (const u of UNITS) Object.assign(meta, JSON.parse(fs.readFileSync(path.join(OUT, 'grade4/question-banks/math4/meta', u + '.meta.json'), 'utf8')));
for (const q of [...A1, ...S7, ...O4, ...S8]) check(q, !!meta[q.id], 'player metadata');
for (const q of [...A1, ...S7]) if (meta[q.id] && meta[q.id].distractors) check(q, !Object.keys(meta[q.id].distractors).includes(String(q.answer)), 'a distractor equals the key');
// the Grade 4 player's checker
{
  const G = { document: {}, location: { search: '', pathname: '/x' }, MK_ELEMENTARY: { course: 'math4' }, URLSearchParams, Math, JSON, console }; G.window = G;
  vm.createContext(G); vm.runInContext(fs.readFileSync(path.join(OUT, 'grade4/worksheet-generator/elementary/el-core.js'), 'utf8'), G);
  const K = G.MKEL;
  const cases = [['6 ft', '6 feet', '', true], ['20 sq cm', '20 square centimeters', '', true], ['20 cm²', '20 square centimeters', '', true], ['less than', '<', '', true], ['12 dollars', '$12', '', true],
    ['7 14 21 28 35', '7, 14, 21, 28, 35', '', true], ['7/5', '1 2/5', 'Write 7/5 as a mixed number.', false], ['2 4/8', '20/8', 'Write 2 4/8 as a fraction greater than 1.', false],
    ['1/2', '4/8', 'The top bar shows 1/2. The bottom bar is the same whole cut into 8 equal parts, with the same amount shaded.', false], ['0.58', '58/100', 'Write 0.58 as a fraction with the denominator 100.', false],
    ['14/100', '0.14', 'Write 14/100 as a decimal.', false], ['15/4', '3 3/4', 'Add: 2 1/4 + 1 2/4', true], ['3 ft', '3 inches', '', false], ['12 R 3', '12 R 3', '', true]];
  for (const [t, k, p, want] of cases) check({ id: 'checker' }, K.checkAnswer(t, k, p) === want, `${t} vs ${k}`);
  for (const q of N) {
    if (q.format === 'short-answer') check(q, K.checkAnswer(String(q.answer), String(q.answer), q.prompt), 'key not accepted by the checker');
    if (q.format === 'open-response') for (const p of q.parts) check(q, K.selfCheck(p) || K.checkAnswer(String(p.answer), String(p.answer), p.prompt + ' ' + q.prompt), 'part key not accepted: ' + p.answer);
  }
  const uc = fs.readFileSync(path.join(OUT, 'grade4/worksheet-generator/elementary/el-understanding-check.js'), 'utf8');
  check(null, /K\.checkAnswer\(inp\.value, p\.answer, p\.prompt\)/.test(uc) && /K\.selfCheck\(p\.parts\[i\]\)/.test(uc) && /The mistake: the student/.test(uc), 'Understanding Check uses the new checker');
  for (const page of ['grade4-games.html', 'grade4-understanding-check.html']) check(null, /el-core\.js\?v=g4-audit-20261119/.test(fs.readFileSync(path.join(OUT, 'grade4/worksheet-generator', page), 'utf8')), page + ' versioned');
}
{
  const s = fs.readFileSync(path.join(OUT, 'grade4-main-catalog.js'), 'utf8');
  const w = {}; w.window = w; w.globalThis = w; vm.createContext(w);
  vm.runInContext(s.slice(s.indexOf('/* Grade 4 audit 2026-11-19 */')), w);
  let mapped = 0; for (const sk of skills) { const set = 'grade4-' + sk.replace(/-skill-\d+$/, ''); if ((w.MKSTD_SKILLS[set] || {})[sk] && w.MKSTD_SKILLS[set][sk].length) mapped++; }
  check(null, mapped === 49, 'standards map covers ' + mapped + ' of 49 skills');
  check(null, s.includes(`"approved":"49 skills · ${Q.length.toLocaleString('en-US')} verified questions`), 'course card count ' + Q.length);
}
{
  const p = path.join(OUT, 'grade-4-pacing/index.html');
  check(null, fs.existsSync(p), 'pacing page');
  if (fs.existsSync(p)) {
    const h = fs.readFileSync(p, 'utf8');
    check(null, /34 of 34 standards have question-bank practice/.test(h) && /MCAS Grade 4 Mathematics|Grade 4 Mathematics · Session 1/.test(h) && /canonical" href="https:\/\/mrksclassroom\.com\/grade-4-pacing\/"/.test(h) && !/6th Grade|Grade 6/.test(h), 'pacing page content');
    check(null, /Final review and exam<\/strong> \(days \d+–180\)/.test(h), 'pacing page reaches day 180');
  }
}
/* ---------- #9 plot items ---------- */
{
  const ctx = {}; vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(OUT, 'worksheet-generator/core/plot.js'), 'utf8'), ctx);
  const P = ctx.MK_PLOT, plots = Q.filter((q) => /\(#9, Graphing Practice\)/.test(q.sourceNotes || ''));
  check(null, plots.length === 22, 'plot items ' + plots.length);
  for (const q of plots) {
    check(q, P.valid(q.plot) && P.check(q.plot, q.plot.testVectors.correct).ok && fs.existsSync(path.join(OUT, q.plot.answerKey.src)), 'plot item valid with an answer key');
    check(q, q.plot.target.values.map((v) => { const [a, b] = v.split('/').map(Number); return a % b === 0 ? String(a / b) : null; }).every(() => true), 'targets');
  }
  const units = (fs.readFileSync(path.join(OUT, 'data.js'), 'utf8').match(/"grade4":\[([^\]]*)\]/) || [])[1] || '';
  check(null, /fractions-equivalent-fractions/.test(units) && /fraction-operations-decimals/.test(units), 'Graphing Practice lists the Grade 4 fraction units');
}

if (fails.length) { console.error(fails.length + ' failures:\n' + fails.slice(0, 60).join('\n')); process.exit(1); }
console.log(`PASS 4th Grade Math audit (${checks} checks, ${A1.length} Advanced and ${S7.length} Standard rewrites, ${O4.length} open-response, ${S8.length} select-all items)`);
