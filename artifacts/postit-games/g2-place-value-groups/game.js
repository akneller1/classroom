PG.game({
  id: "g2-place-value-groups", title: ["Place Value", "Groups"], course: "Grade 2", unit: "Place Value to 1,000",
  tag: "Find the cards that show the same number in different ways.",
  skills: "2.NBT.1, 2.NBT.3 · standard, expanded and word form · hundreds, tens and ones · zeros as placeholders",
  engine: "groups",
  levels: [
    "Three numbers, three ways each.",
    "Four numbers built from the same digits (352, 325, 523…), four ways each.",
    "Numbers with zeros (305, 350, 503…). Zeros hide in every form.",
    "Regrouped disguises: 2 hundreds 15 tens 3 ones is 353."
  ],
  round(c) {
    const ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"];
    const TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
    const words = n => { const h = Math.floor(n / 100), r = n % 100; const rest = r < 20 ? (r ? ONES[r] : "") : TENS[Math.floor(r / 10)] + (r % 10 ? "-" + ONES[r % 10] : ""); return [h ? ONES[h] + " hundred" : "", rest].filter(Boolean).join(" "); };
    const exp = n => { const h = Math.floor(n / 100) * 100, t = Math.floor(n % 100 / 10) * 10, o = n % 10; return [h, t, o].filter(Boolean).join(" + "); };
    const units = n => { const h = Math.floor(n / 100), t = Math.floor(n % 100 / 10), o = n % 10; const p = []; if (h) p.push(h + (h === 1 ? " hundred" : " hundreds")); if (t) p.push(t + (t === 1 ? " ten" : " tens")); if (o) p.push(o + (o === 1 ? " one" : " ones")); return p.join(" "); };
    const odd = n => { const h = Math.floor(n / 100), t = Math.floor(n % 100 / 10), o = n % 10; const opts = []; if (h >= 1 && t <= 8) opts.push(`${h - 1} hundreds ${t + 10} tens ${o} ones`); if (t >= 1) opts.push(`${h} hundreds ${t - 1} tens ${o + 10} ones`); opts.push(`${h * 10 + t} tens ${o} ones`); if (t) opts.push(`${h * 100} + ${t * 10 + o}`); return opts; };
    let nums;
    if (c.lvl === 1) { let d; do { d = c.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3); } while (false); const perms = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]].map(p => d[p[0]] * 100 + d[p[1]] * 10 + d[p[2]]); nums = c.sample(perms, 4); }
    else if (c.lvl === 2) { const a = c.ri(1, 9); let b; do { b = c.ri(1, 9); } while (b === a); nums = c.sample([a * 100 + b, a * 100 + b * 10, b * 100 + a, b * 100 + a * 10, a * 100 + b * 10 + c.ri(1, 9)], 4); }
    else nums = c.distinct(c.lvl === 0 ? 3 : 4, () => c.ri(1, 9) * 100 + c.ri(1, 9) * 10 + c.ri(1, 9), x => x);
    const groups = nums.map(n => {
      let forms;
      if (c.lvl === 0) forms = [String(n), exp(n), units(n)];
      else if (c.lvl < 3) forms = [String(n), exp(n), words(n), units(n)];
      else { const o = c.sample(odd(n), 2); forms = [c.chance(.5) ? String(n) : words(n), exp(n), ...o]; }
      return { label: `${n}`, items: forms.map(f => ({ html: f, cls: /^\d+$/.test(f) ? "" : "txt" })), say: `All of these are ${n}: ${words(n)}.` };
    });
    return { groups, cw: c.lvl >= 2 ? "170px" : "150px" };
  }
});
