/* Error Analysis tasks for the Quantitative Modeling units (2026-11-21): eight per unit, two per skill, like the
 * first ten units. A fictional student shows work with one mistake; the task is to name the mistake. They feed the
 * Error Analysis worksheet (format=error) and stay out of games. verify() recomputes the correct result from the
 * prompt and checks it against the solution's "Correct result" line. */
import { M, money, $, person, mc } from './kit.mjs';
const r2 = M.round2;
const D = (s) => [...String(s).matchAll(/\$([\d,]+(?:\.\d+)?)/g)].map(m => Number(m[1].replace(/,/g, '')));
const P = (s) => [...String(s).matchAll(/([\d.]+)%/g)].map(m => Number(m[1]));
const fx = (x) => String(Math.round(x * 10000) / 10000);
const lastNum = (q) => { const s = q.solutionSteps.find((x) => /^Correct result:/.test(x)).replace(/\$/g, '').replace(/\.$/, ''); const m = s.match(/−?\d[\d,]*(?:\.\d+)?/g); return Number(m[m.length - 1].replace(/,/g, '').replace('−', '-')); };
const E = (id, skill, gen, check) => ({ id, skill, type: 'reasoning', count: 2, game: false, activities: ['worksheet', 'assessment', 'practice-test', 'error-analysis'],
  gen(r) { const g = gen(r); if (!g) return null; const { right, wrong, correct, work, setup, steps } = g;
    return { errorAnalysis: true, prompt: `${setup} ${g.who}’s work: ${work} What mistake did ${g.who} make?`, ...mc(r, right, wrong), misconceptions: [right], solutionSteps: [...steps, `Correct result: ${correct}.`] }; },
  verify: (q, Q) => Math.abs(check(q) - lastNum(Q)) < 0.011 ? Q.answer : 'correct result does not match' });

export const errorFamilies = {
  consumer: [
    E('stack-add-err', 1, (r) => { const p = person(r), price = r.step(40, 160, 5), a = r.pick([20, 25, 30]), b = r.pick([10, 15, 20]);
      return { who: p.name, setup: `A ${$(price)} jacket is ${a}% off, and a coupon takes an extra ${b}% off the sale price.`, work: `${a}% + ${b}% = ${a + b}% off, so ${$(price)} × ${fx(1 - (a + b) / 100)} = ${money(price * (1 - (a + b) / 100))}.`,
        right: 'Added the two discounts; the coupon applies to the sale price, so multiply the multipliers.', wrong: ['Should have subtracted the percents from the price directly.', 'Should have added the discounts to the price.', 'Used the coupon before the sale; the order changes the answer.'], correct: money(price * (1 - a / 100) * (1 - b / 100)),
        steps: [`${$(price)} × ${fx(1 - a / 100)} = ${money(price * (1 - a / 100))}.`, `${money(price * (1 - a / 100))} × ${fx(1 - b / 100)} = ${money(price * (1 - a / 100) * (1 - b / 100))}.`] }; },
      (q) => { const [price] = D(q), [a, b] = P(q); return r2(price * (1 - a / 100) * (1 - b / 100)); }),
    E('tax-decimal-err', 2, (r) => { const p = person(r), price = r.step(20, 90, 1) + 0.5, t = r.pick([5, 6, 7, 8]);
      return { who: p.name, setup: `A ${$(price)} purchase has ${t}% sales tax.`, work: `Tax = ${$(price)} × ${t} = ${money(price * t)}, so the total is ${money(price * (1 + t))}.`,
        right: `Multiplied by ${t} instead of ${t / 100}; a percent must be written as a decimal.`, wrong: ['Should have divided the price by the tax rate.', 'Tax is charged only on prices over $100.', 'Should have subtracted the tax from the price.'], correct: money(price * (1 + t / 100)),
        steps: [`Tax = ${$(price)} × ${t / 100} = ${money(price * t / 100)}.`, `Total = ${money(price * (1 + t / 100))}.`] }; },
      (q) => { const [price] = D(q), [t] = P(q); return r2(price * (1 + t / 100)); }),
    E('pct-change-base-err', 3, (r) => { const p = person(r), a = r.step(20, 80, 2), b = a + r.step(4, 20, 2);
      return { who: p.name, setup: `A concert ticket rose from ${$(a)} to ${$(b)}.`, work: `Change = ${b - a}. ${b - a} ÷ ${b} ≈ ${Math.round((b - a) / b * 1000) / 10}% increase.`,
        right: 'Divided by the new price; percent change divides by the original price.', wrong: ['Should have subtracted the new price from the old price.', 'Should have divided the new price by the old price only.', 'Percent change should be found with the average price.'], correct: `${Math.round((b - a) / a * 1000) / 10}%`,
        steps: [`Change = ${$(b)} − ${$(a)} = ${$(b - a)}.`, `${b - a} ÷ ${a} ≈ ${Math.round((b - a) / a * 1000) / 10}%.`] }; },
      (q) => { const [a, b] = D(q); return Math.round((b - a) / a * 1000) / 10; }),
    E('unit-price-flip-err', 4, (r) => { const p = person(r), s1 = r.pick([12, 16]), s2 = r.pick([24, 32]), u = r.step(18, 30, 1) / 100, p1 = r2(s1 * u), p2 = r2(s2 * u * 0.85);
      return { who: p.name, setup: `Cereal: ${s1} oz for ${$(p1)} or ${s2} oz for ${$(p2)}.`, work: `${s1} ÷ ${p1} ≈ ${fx(s1 / p1)} and ${s2} ÷ ${p2} ≈ ${fx(s2 / p2)}. The smaller number is cheaper, so the ${s1}-oz box is the better buy.`,
        right: 'Found ounces per dollar, where the bigger number is the better buy; dollars per ounce is the unit price.', wrong: ['Should have multiplied price by ounces.', 'Should have compared only the shelf prices.', 'Should have subtracted the sizes.'], correct: money(p2 / s2),
        steps: [`Unit prices: ${$(p1)} ÷ ${s1} = ${money(p1 / s1)} per oz; ${$(p2)} ÷ ${s2} = ${money(p2 / s2)} per oz.`, `The ${s2}-oz box is cheaper per ounce.`] }; },
      (q) => { const [, p2] = D(q), s2 = Number(q.match(/or (\d+) oz/)[1]); return r2(p2 / s2); })
  ],
  linear: [
    E('slope-flip-err', 1, (r) => { const p = person(r), rate = r.step(40, 90, 5), fee = r.step(30, 80, 5), h1 = 2, h2 = r.pick([4, 5, 6]);
      return { who: p.name, setup: `A ${h1}-hour repair costs ${$(fee + rate * h1)} and a ${h2}-hour repair costs ${$(fee + rate * h2)}.`, work: `Rate = (${h2} − ${h1}) ÷ (${fee + rate * h2} − ${fee + rate * h1}) = ${fx((h2 - h1) / (rate * (h2 - h1)))} dollars per hour.`,
        right: 'Divided hours by dollars; the rate is change in cost ÷ change in hours.', wrong: ['Should have added the two costs.', 'Should have divided the larger cost by the larger number of hours only.', 'Forgot to subtract the flat fee from each cost first.'], correct: money(rate),
        steps: [`(${fee + rate * h2} − ${fee + rate * h1}) ÷ (${h2} − ${h1}) = ${money(rate)} per hour.`] }; },
      (q) => { const [c1, c2] = D(q), h = [...q.matchAll(/(\d+)-hour/g)].map((m) => Number(m[1])); return r2((c2 - c1) / (h[1] - h[0])); }),
    E('model-swap-err', 2, (r) => { const p = person(r), fee = r.pick([25, 35, 40]), rate = r.pick([12, 15, 18]), x = r.step(5, 12, 1);
      return { who: p.name, setup: `A gym charges a ${$(fee)} sign-up fee plus ${$(rate)} per month. Find the cost for ${x} months.`, work: `C = ${fee}m + ${rate}, so C = ${fee}(${x}) + ${rate} = ${money(fee * x + rate)}.`,
        right: 'Swapped the rate and the fee; the model is C = (monthly price)m + (fee).', wrong: ['Should have multiplied the fee and the rate.', 'Should have divided the fee by the number of months.', 'Forgot to add tax.'], correct: money(rate * x + fee),
        steps: [`C = ${rate}m + ${fee}.`, `C = ${rate}(${x}) + ${fee} = ${money(rate * x + fee)}.`] }; },
      (q) => { const [fee, rate] = D(q), x = Number(q.match(/for (\d+) months/)[1]); return rate * x + fee; }),
    E('break-even-price-err', 3, (r) => { const p = person(r), F = r.step(600, 1800, 100), v = r.pick([2, 3, 4]), price = v + r.pick([4, 5, 6]);
      return { who: p.name, setup: `A stand has ${$(F)} of fixed costs. Each item costs ${$(v)} to make and sells for ${$(price)}.`, work: `Break-even = ${F} ÷ ${price} ≈ ${Math.ceil(F / price)} items.`,
        right: 'Divided by the price; each sale only covers price − cost per item toward fixed costs.', wrong: ['Should have multiplied fixed costs by the price.', 'Should have divided the price by the fixed costs.', 'Should have added the cost per item to the fixed costs.'], correct: String(Math.ceil(F / (price - v))),
        steps: [`Each sale covers ${$(price)} − ${$(v)} = ${$(price - v)}.`, `${F} ÷ ${price - v} ≈ ${r2(F / (price - v))} → ${Math.ceil(F / (price - v))} items.`] }; },
      (q) => { const [F, v, p] = D(q); return Math.ceil(F / (p - v)); }),
    E('tier-all-err', 4, (r) => { const p = person(r), t = r.pick([500, 600]), a = r.pick([0.12, 0.13]), b = r2(a + 0.05), u = t + r.step(100, 400, 50);
      return { who: p.name, setup: `Electricity costs ${$(a)} per kWh for the first ${t} kWh and ${$(b)} per kWh above that. A home used ${u} kWh.`, work: `${u} kWh is over ${t}, so ${u} × ${$(b)} = ${money(u * b)}.`,
        right: `Charged every kWh at the higher rate; only the usage above ${t} kWh costs ${$(b)}.`, wrong: ['Should have averaged the two rates.', 'Should have charged every kWh at the lower rate.', 'Should have subtracted the two rates.'], correct: money(t * a + (u - t) * b),
        steps: [`${t} × ${$(a)} = ${money(t * a)}.`, `${u - t} × ${$(b)} = ${money((u - t) * b)}.`, `Total = ${money(t * a + (u - t) * b)}.`] }; },
      (q) => { const [a, b] = D(q), t = Number(q.match(/first (\d+) kWh/)[1]), u = Number(q.match(/used (\d+) kWh/)[1]); return r2(t * a + (u - t) * b); })
  ],
  exponential: [
    E('rate-as-factor-err', 1, (r) => { const p = person(r), a = r.step(1000, 5000, 500), g = r.pick([4, 5, 6]), t = r.pick([3, 4, 5]);
      return { who: p.name, setup: `${$(a)} grows ${g}% a year for ${t} years.`, work: `${$(a)} × (${g / 100})^${t} = ${money(a * (g / 100) ** t)}.`,
        right: `Used ${g / 100} as the factor; growth of ${g}% multiplies by 1 + ${g / 100} = ${fx(1 + g / 100)}.`, wrong: ['Should have added the rate each year.', 'Should have divided by the number of years.', 'Should have multiplied by the rate only once.'], correct: money(a * (1 + g / 100) ** t),
        steps: [`${$(a)} × ${fx(1 + g / 100)}^${t} = ${money(a * (1 + g / 100) ** t)}.`] }; },
      (q) => { const [a] = D(q), [g] = P(q), t = Number(q.match(/for (\d+) years/)[1]); return r2(a * (1 + g / 100) ** t); }),
    E('linear-dep-err', 2, (r) => { const p = person(r), v0 = r.step(18000, 30000, 1000), d = r.pick([10, 15, 20]), t = r.pick([3, 4]);
      return { who: p.name, setup: `A ${$(v0)} car loses ${d}% of its value each year. Find its value after ${t} years.`, work: `${d}% of ${$(v0)} is ${money(v0 * d / 100)}. ${t} × ${money(v0 * d / 100)} = ${money(t * v0 * d / 100)}, so the value is ${money(v0 - t * v0 * d / 100)}.`,
        right: 'Took the percent of the original price every year; each year loses a percent of the current value, so multiply by the decay factor.', wrong: ['Should have added the depreciation each year.', 'Should have used the rule of 72.', 'Should have divided the price by the number of years.'], correct: money(v0 * (1 - d / 100) ** t),
        steps: [`${$(v0)} × ${fx(1 - d / 100)}^${t} = ${money(v0 * (1 - d / 100) ** t)}.`] }; },
      (q) => { const [v0] = D(q), [d] = P(q), t = Number(q.match(/after (\d+) years/)[1]); return r2(v0 * (1 - d / 100) ** t); }),
    E('add-percents-err', 3, (r) => { const p = person(r), a = r.step(200, 900, 50), g = r.pick([10, 20, 25]);
      return { who: p.name, setup: `An amount of ${$(a)} grows ${g}% a year for 2 years.`, work: `${g}% + ${g}% = ${2 * g}%, so ${$(a)} × ${fx(1 + 2 * g / 100)} = ${money(a * (1 + 2 * g / 100))}.`,
        right: `Added the yearly percents; growth multiplies, so use ${fx(1 + g / 100)}².`, wrong: ['Should have multiplied by 2.', 'Should have used a decay factor.', 'Should have divided by 2.'], correct: money(a * (1 + g / 100) ** 2),
        steps: [`${$(a)} × ${fx(1 + g / 100)}² = ${money(a * (1 + g / 100) ** 2)}.`] }; },
      (q) => { const [a] = D(q), [g] = P(q); return r2(a * (1 + g / 100) ** 2); }),
    E('rule-100-err', 4, (r) => { const p = person(r), g = r.pick([4, 6, 8, 9, 12]);
      return { who: p.name, setup: `Estimate how long money takes to double at ${g}% a year, compounded yearly.`, work: `100 ÷ ${g} ≈ ${r2(100 / g)} years.`,
        right: 'Used 100 instead of 72; the rule of 72 estimates compound doubling time.', wrong: ['Should have multiplied the rate by 72.', 'Should have divided the rate by 2.', 'Doubling time does not depend on the rate.'], correct: `${r2(72 / g)} years`,
        steps: [`72 ÷ ${g} = ${r2(72 / g)} years.`] }; },
      (q) => { const [g] = P(q); return r2(72 / g); })
  ],
  data: [
    E('median-unsorted-err', 1, (r) => { const p = person(r); let xs; do { xs = Array.from({ length: 7 }, () => r.step(10, 60, 1)); } while (xs[3] === [...xs].sort((a, b) => a - b)[3]);
      return { who: p.name, setup: `Find the median of the data: ${xs.join(', ')}.`, work: `The middle number is the 4th one, ${xs[3]}.`,
        right: 'Did not put the data in order first.', wrong: ['Should have averaged the first and last values.', 'Should have used the most common value.', 'Should have added all the values.'], correct: String([...xs].sort((a, b) => a - b)[3]),
        steps: [`In order: ${[...xs].sort((a, b) => a - b).join(', ')}.`, `Median: ${[...xs].sort((a, b) => a - b)[3]}.`] }; },
      (q) => { const xs = q.match(/data: ([\d, ]+)\./)[1].split(', ').map(Number).sort((a, b) => a - b); return xs[3]; }),
    E('r-sign-err', 2, (r) => { const p = person(r), v = r.pick([-0.92, -0.88, -0.81, -0.76]);
      return { who: p.name, setup: `A study of car age and resale value reports r = −${Math.abs(v)}.`, work: `r is negative, so the relationship is weak.`,
        right: 'Confused direction with strength; the sign shows direction and |r| shows strength, so this is a strong negative relationship.', wrong: ['Should have said there is no relationship.', 'Should have said the relationship is positive.', 'Should have squared r to find the direction.'], correct: String(Math.abs(v)),
        steps: [`|r| = ${Math.abs(v)} ≥ 0.7 → strong.`, 'Negative sign → as age rises, value tends to fall.'] }; },
      (q) => Number(q.match(/r = −([\d.]+)\./)[1])),
    E('predict-swap-err', 3, (r) => { const p = person(r), m = r.pick([2.5, 3, 4.5]), b = r.step(40, 60, 2), x = r.step(3, 9, 1);
      return { who: p.name, setup: `The model ŷ = ${m}x + ${b} predicts a test score from hours studied. Predict the score for ${x} hours.`, work: `ŷ = ${b}(${x}) + ${m} = ${r2(b * x + m)}.`,
        right: 'Swapped the slope and the intercept; multiply x by the slope.', wrong: ['Should have divided by the slope.', 'Should have subtracted the intercept.', 'Should have used the residual.'], correct: String(r2(m * x + b)),
        steps: [`ŷ = ${m}(${x}) + ${b} = ${r2(m * x + b)}.`] }; },
      (q) => { const m = Number(q.match(/ŷ = ([\d.]+)x/)[1]), b = Number(q.match(/x \+ (\d+)/)[1]), x = Number(q.match(/for (\d+) hours/)[1]); return r2(m * x + b); }),
    E('residual-sign-err', 4, (r) => { const p = person(r), pred = r.step(15000, 22000, 100), act = pred - r.step(5, 25, 1) * 100;
      return { who: p.name, setup: `A model predicts a used car’s price as ${$(pred)}. It is listed at ${$(act)}.`, work: `Residual = ${$(pred)} − ${$(act)} = ${money(pred - act)}, so the car is priced above the model.`,
        right: 'Subtracted in the wrong order; residual = actual − predicted, which is negative here, so the car is below the model.', wrong: ['Should have added the two prices.', 'Should have divided actual by predicted.', 'A residual is always positive.'], correct: '−' + money(pred - act),
        steps: [`Residual = ${$(act)} − ${$(pred)} = −${money(pred - act)}.`, 'Negative: priced below the model.'] }; },
      (q) => { const [pred, act] = D(q); return act - pred; })
  ],
  probability: [
    E('prob-total-err', 1, (r) => { const p = person(r), a = r.step(3, 9, 1), b = r.step(4, 12, 1);
      return { who: p.name, setup: `A bag has ${a} red and ${b} blue tickets. Find P(red).`, work: `P(red) = ${a}/${b}.`,
        right: 'Divided by the number of blue tickets; divide by the total number of tickets.', wrong: ['Should have subtracted the blue tickets.', 'Should have multiplied the counts.', 'Probability must always be 1/2 for two colors.'], correct: `${a}/${a + b} ≈ ${Math.round(a / (a + b) * 1000) / 10}%`,
        steps: [`Total: ${a + b}.`, `P(red) = ${a}/${a + b}.`] }; },
      (q) => { const n = [...q.matchAll(/(\d+) (red|blue)/g)].map((m) => Number(m[1])); return Math.round(n[0] / (n[0] + n[1]) * 1000) / 10; }),
    E('and-add-err', 2, (r) => { const p = person(r), a = r.pick([20, 30, 40]), b = r.pick([10, 25, 50]);
      return { who: p.name, setup: `Independent events: P(A) = ${a}% and P(B) = ${b}%. Find P(A and B).`, work: `${a}% + ${b}% = ${a + b}%.`,
        right: 'Added the probabilities; for independent events, “and” means multiply.', wrong: ['Should have subtracted the probabilities.', 'Should have averaged them.', 'Should have used the larger probability.'], correct: `${r2(a * b / 100)}%`,
        steps: [`${a / 100} × ${b / 100} = ${r2(a * b / 10000)}.`] }; },
      (q) => { const [a, b] = P(q); return r2(a * b / 100); }),
    E('ev-cost-err', 3, (r) => { const p = person(r), cost = r.pick([2, 3]), win = r.pick([10, 12, 15]);
      return { who: p.name, setup: `A game costs ${$(cost)} to play. Rolling a 6 on a fair die wins ${$(win)}.`, work: `EV = (1/6)(${win}) = ${money(win / 6)}, so the game is a good deal.`,
        right: 'Forgot to subtract the cost of playing.', wrong: ['Should have multiplied by 6.', 'Should have added the cost.', 'Expected value only applies to insurance.'], correct: (win / 6 - cost < 0 ? '−' : '') + money(Math.abs(win / 6 - cost)),
        steps: [`EV = (1/6)(${win}) − ${cost} = ${money(win / 6 - cost)}.`] }; },
      (q) => { const [cost, win] = D(q); return r2(win / 6 - cost); }),
    E('warranty-ev-err', 4, (r) => { const p = person(r), price = r.pick([99, 129, 149]), pr = r.pick([8, 10, 15]), rep = r.pick([300, 400, 500]);
      return { who: p.name, setup: `A ${$(price)} warranty covers a repair that has a ${pr}% chance of being needed and costs ${$(rep)}.`, work: `The repair costs ${$(rep)}, which is more than ${$(price)}, so the warranty saves ${money(rep - price)}.`,
        right: 'Compared with the full repair cost; use the expected repair cost, probability × repair.', wrong: ['Should have added the warranty to the repair.', 'Should have divided the repair cost by the warranty price.', 'Warranties always save money.'], correct: '−' + money(price - pr / 100 * rep),
        steps: [`Expected repair cost: ${pr / 100} × ${$(rep)} = ${money(pr / 100 * rep)}.`, `EV of the warranty: ${money(pr / 100 * rep)} − ${$(price)} = −${money(price - pr / 100 * rep)}.`] }; },
      (q) => { const [price, rep] = D(q), [pr] = P(q); return r2(pr / 100 * rep - price); })
  ]
};
