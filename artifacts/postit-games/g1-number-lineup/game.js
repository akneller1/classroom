PG.game({
  id: "g1-number-lineup", title: ["Number", "Line-Up"], course: "Grade 1", unit: "Comparing & Ordering Numbers",
  tag: "Put the number cards in order.",
  skills: "1.NBT.1, 1.NBT.3 · counting to 120 · comparing two-digit numbers",
  engine: "order",
  levels: [
    "Five numbers up to 20.",
    "Six numbers up to 100, with flipped digits like 27 and 72.",
    "Seven numbers up to 120 that sit close together.",
    "Seven disguised numbers (10 + 7, 3 tens 2 ones, 1 more than 59). You check the order yourself at the end."
  ],
  options: [{ id: "dir", label: "Order", type: "one", choices: [["up", "Least to greatest"], ["down", "Greatest to least"]], default: "up" }],
  round(c) {
    const n = [5, 6, 7, 7][c.lvl] + (c.len === 2 ? 1 : 0) - (c.len === 0 ? 1 : 0);
    let vals;
    if (c.lvl === 0) vals = c.distinct(n, () => c.ri(0, 20), x => x);
    else if (c.lvl === 1) { vals = []; while (vals.length < n) { const t = c.ri(1, 9), o = c.ri(1, 9); if (t !== o) { [t * 10 + o, o * 10 + t].forEach(v => { if (vals.length < n && !vals.includes(v)) vals.push(v); }); } } }
    else { const base = c.ri(60, 100); vals = c.distinct(n, () => base + c.ri(-12, 20), x => x).filter(v => v <= 120); while (vals.length < n) { const v = c.ri(80, 120); if (!vals.includes(v)) vals.push(v); } }
    const show = v => {
      if (c.lvl < 3 || c.chance(.25)) return { html: String(v) };
      const t = Math.floor(v / 10), o = v % 10;
      const opts = [
        () => `${t} tens ${o} ones`,
        () => `${t * 10} + ${o}`,
        () => `1 more than ${v - 1}`,
        () => `1 less than ${v + 1}`,
        () => `10 more than ${v - 10}`,
        () => `${o} + ${t * 10}`
      ];
      return { html: c.pick(opts)(), cls: "txt" };
    };
    if (c.lvl === 3) vals = c.distinct(n, () => c.ri(25, 115), x => x);
    const cards = vals.map(v => Object.assign({ v }, show(v)));
    const down = c.opt.dir === "down";
    return { cards, desc: down, lo: down ? "Greatest" : "Least", hi: down ? "Least" : "Greatest", endCheck: c.lvl === 3, slotMin: c.lvl === 3 ? 120 : 90,
      why: (card, i, sorted) => c.mode === "practice" ? `${PG.textify(card.html)} is ${card.v}.` : "" };
  }
});
