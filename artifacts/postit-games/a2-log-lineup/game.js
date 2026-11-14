PG.game({
  id: "a2-log-lineup", title: ["Logarithm", "Line-Up"], course: "Algebra 2", unit: "Exponential & Logarithmic Functions",
  tag: "Order the logs and powers without a calculator.",
  skills: "F.LE.4, F.BF.5 · evaluating logarithms · negative and fractional values · estimating logs · log properties",
  engine: "order",
  levels: [
    "Logs that come out to whole numbers.",
    "Negative and fractional answers: log₂(1/8), log₉ 3.",
    "Estimate: log₂ 10 vs log₃ 20 vs log 500. Some powers mixed in.",
    "Properties: log₂ 12 − log₂ 3, 10^(log 7), 2 log₅ 10 − log₅ 4. You check the order yourself."
  ],
  options: [{ id: "dir", label: "Order", type: "one", choices: [["up", "Least to greatest"], ["down", "Greatest to least"]], default: "up" }],
  round(c) {
    const { h } = c; const M = h.MINUS;
    const lg = (b, x) => b === 10 ? `log ${x}` : b === "e" ? `ln ${x}` : `log<sub>${b}</sub> ${x}`;
    const L = (b, x) => Math.log(x) / Math.log(b === "e" ? Math.E : b);
    const pool = [];
    const add = (html, v) => pool.push({ html, v, cls: "mth" });
    if (c.lvl === 0) {
      [[2, 8], [2, 32], [3, 9], [3, 81], [5, 125], [10, 1000], [10, 100], [4, 64], [2, 1], [7, 7], [6, 36], [2, 64], [3, 243], [5, 625]].forEach(([b, x]) => add(lg(b, x), L(b, x)));
    } else if (c.lvl === 1) {
      [[2, h.frac(1, 8), 1 / 8], [3, h.frac(1, 9), 1 / 9], [9, 3, 3], [4, 8, 8], [10, "0.01", .01], [8, 2, 2], [27, 3, 3], [4, h.frac(1, 2), .5], [2, h.sqrt(2), Math.SQRT2], [25, 125, 125], [16, 4, 4], [10, "0.001", .001], [5, h.frac(1, 25), 1 / 25]].forEach(([b, xh, x]) => add(lg(b, xh), L(b, x)));
      add(`ln ${h.v("e")}<sup>3</sup>`, 3); add(`ln 1`, 0);
    } else if (c.lvl === 2) {
      [[2, 10], [3, 20], [10, 500], [5, 100], [2, 3], [3, 10], [10, 50], [2, 50], [4, 20], [7, 100], [10, 2000], [6, 30], [2, 20]].forEach(([b, x]) => add(lg(b, x), L(b, x)));
      add(`ln 20`, Math.log(20)); add(`8<sup>2/3</sup>`, 4); add(`2<sup>${M}1</sup>`, .5); add(`9<sup>1/2</sup>`, 3); add(`16<sup>3/4</sup>`, 8);
    } else {
      add(`${lg(2, 12)} ${M} ${lg(2, 3)}`, 2); add(`10<sup>log 7</sup>`, 7); add(`2 ${lg(5, 10)} ${M} ${lg(5, 4)}`, 2 * L(5, 10) - L(5, 4));
      add(`${lg(2, "8<sup>5</sup>")}`, 15); add(`${lg(3, 6)} + ${lg(3, 1.5)}`, L(3, 9)); add(`${lg(4, 2)} + ${lg(4, 8)}`, 2);
      add(`${lg(6, 4)} + ${lg(6, 9)}`, 2); add(`ln ${h.v("e")}<sup>${M}2</sup>`, -2); add(`${h.v("e")}<sup>ln 5</sup>`, 5); add(`${lg(2, 40)} ${M} ${lg(2, 5)}`, 3);
      add(`3 ${lg(2, 4)}`, 6); add(`${lg(10, 4)} + ${lg(10, 25)}`, 2); add(`${lg(7, 1)} ${M} ${lg(7, 49)}`, -2); add(`${h.frac(lg(2, 81), lg(2, 3))}`, 4); add(`${lg(3, 2)} ${M} ${lg(3, 18)}`, -2);
    }
    const n = [5, 6, 6, 6][c.lvl] + (c.len === 2 ? 1 : 0) - (c.len === 0 ? 1 : 0);
    const cards = [];
    for (const it of c.shuffle(pool)) { if (cards.length >= n) break; if (cards.every(o => Math.abs(o.v - it.v) > (c.lvl === 2 ? .12 : 1e-6))) cards.push(it); }
    cards.forEach(cd => cd.say = `= ${+cd.v.toFixed(3)}`);
    const down = c.opt.dir === "down";
    return { cards, desc: down, lo: down ? "Greatest" : "Least", hi: down ? "Least" : "Greatest", endCheck: c.lvl === 3, slotMin: c.lvl === 3 ? 160 : 110, tol: 1e-6,
      why: card => c.mode === "practice" ? `log_b x asks “b to what power gives x?” This one is about ${+card.v.toFixed(2)}.` : "" };
  }
});
