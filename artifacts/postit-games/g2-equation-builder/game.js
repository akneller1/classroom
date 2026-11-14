PG.game({
  id: "g2-equation-builder", title: ["Equation", "Builder"], course: "Grade 2", unit: "Add & Subtract within 100",
  tag: "Drag number cards into the boxes to make each equation true.",
  skills: "2.NBT.5, 2.OA.1, 1.OA.7 · add and subtract within 100 · unknowns in any position · balanced equations",
  engine: "build",
  levels: [
    "One box: find the missing number (___ + 24 = 57).",
    "Two boxes that add to the total (___ + ___ = 63).",
    "Two boxes with subtraction (___ − ___ = 27).",
    "Balance both sides: 45 + ___ = ___ + 38. Many answers work!"
  ],
  options: [{ id: "regroup", label: "Regrouping", type: "one", choices: [["mix", "Mixed"], ["no", "No regrouping"], ["yes", "Always regroup"]], default: "mix" }],
  round(c) {
    const reg = (a, b) => (a % 10) + (b % 10) >= 10;
    const okPair = (a, b) => c.opt.regroup === "mix" || (c.opt.regroup === "yes") === reg(a, b);
    const pairSum = (lo, hi) => { for (let i = 0; i < 200; i++) { const a = c.ri(lo, hi), b = c.ri(lo, hi); if (a + b <= 99 && okPair(a, b)) return [a, b]; } return [21, 34]; };
    const N = c.n(6), puzzles = [];
    const deck = (need, extra) => { const nums = need.slice(); let g = 0; while (nums.length < need.length + extra && g++ < 200) { const base = c.pick(need); const v = base + c.pick([1, -1, 10, -10, 9, 11, -9]); if (v > 0 && v < 100 && !nums.includes(v)) nums.push(v); } const cards = c.shuffle(nums).map(v => ({ html: String(v), v })); const answer = []; need.forEach(v => answer.push(cards.findIndex((x, j) => x.v === v && !answer.includes(j)))); return { cards, answer }; };
    for (let p = 0; p < N; p++) {
      if (c.lvl === 0) {
        const [a, b] = pairSum(11, 60); const { cards, answer } = deck([a], 4);
        puzzles.push({ parts: [{}, " + ", String(b), " = ", String(a + b)], cards, answer, show: v => v[0] ? `${v[0]} + ${b} = ${v[0] + b}` : "", test: v => v[0] + b === a + b ? true : `${v[0]} + ${b} = ${v[0] + b}, not ${a + b}.` });
      } else if (c.lvl === 1) {
        const [a, b] = pairSum(12, 60); const T = a + b; const { cards, answer } = deck([a, b], 4);
        puzzles.push({ parts: [{}, " + ", {}, " = ", String(T)], cards, answer, show: v => v.every(x => x != null) ? `${v[0]} + ${v[1]} = ${v[0] + v[1]}` : "", test: v => v[0] + v[1] === T ? true : `${v[0]} + ${v[1]} = ${v[0] + v[1]}. You need ${T}.` });
      } else if (c.lvl === 2) {
        let a, b; do { [b, a] = pairSum(10, 55); a = a + b; } while (a > 99);
        const D = a - b; const { cards, answer } = deck([a, b], 4);
        puzzles.push({ parts: [{}, " − ", {}, " = ", String(D)], cards, answer, show: v => v.every(x => x != null) ? `${v[0]} − ${v[1]} = ${v[0] - v[1]}` : "", test: v => v[0] - v[1] === D ? true : `${v[0]} − ${v[1]} = ${v[0] - v[1]}. You need ${D}.` });
      } else {
        const L = c.ri(25, 60), Rr = c.ri(15, 55); if (L === Rr) { p--; continue; }
        const x = c.ri(5, 35); const y = L + x - Rr; if (y <= 0 || y > 99) { p--; continue; }
        const { cards, answer } = deck([x, y], 5);
        puzzles.push({ parts: [String(L), " + ", {}, " = ", {}, " + ", String(Rr)], cards, answer,
          show: v => v.every(x => x != null) ? `Left: ${L + v[0]} · Right: ${v[1] + Rr}` : "",
          test: v => L + v[0] === v[1] + Rr ? true : `Left side is ${L} + ${v[0]} = ${L + v[0]}, right side is ${v[1]} + ${Rr} = ${v[1] + Rr}. They must be equal.`,
          say: `Balanced! Both sides equal ${L + x}.` });
      }
    }
    return { puzzles, note: c.lvl === 3 ? "Tip: compare the two numbers you're given. The boxes have to make up the difference between them." : null };
  }
});
