PG.game({
  id: "g5-decimal-lineup", title: ["Decimal", "Line-Up"], course: "Grade 5", unit: "Decimals & Place Value",
  tag: "Order the decimals from least to greatest.",
  skills: "5.NBT.3 · read, write and compare decimals to thousandths · more digits doesn't mean bigger",
  engine: "order",
  levels: [
    "Tenths, and a whole number or two.",
    "Tenths and hundredths mixed together (0.4 vs 0.35).",
    "Thousandths: 0.5, 0.45, 0.455, 0.405… longer isn't bigger!",
    "Decimals, fractions, words and expanded form, all mixed. You check the order yourself."
  ],
  options: [{ id: "dir", label: "Order", type: "one", choices: [["up", "Least to greatest"], ["down", "Greatest to least"]], default: "up" }],
  round(c) {
    const { h } = c;
    const n = [5, 6, 7, 7][c.lvl] + (c.len === 2 ? 1 : 0) - (c.len === 0 ? 1 : 0);
    const dec = k => (k / 1000).toFixed(3).replace(/0+$/, "").replace(/\.$/, "");
    let ks;
    if (c.lvl === 0) ks = c.distinct(n, () => 100 * c.ri(1, 25), x => x);
    else if (c.lvl === 1) { const base = c.ri(1, 8) * 100; ks = c.distinct(n, () => c.chance(.5) ? base + 10 * c.ri(-9, 9) : 100 * c.ri(0, 9) + (c.chance(.5) ? 10 * c.ri(1, 9) : 0), x => x).filter(k => k > 0); }
    else if (c.lvl === 2) { const d = c.ri(1, 8); ks = c.distinct(n, () => c.pick([d * 100, d * 100 + 50, d * 100 + 55, d * 100 + 5, d * 10 + 5, d * 100 + 45 + c.ri(0, 9), (d + 1) * 10, d * 100 + c.ri(1, 9) * 10 + c.ri(1, 9)]), x => x).filter(k => k > 0); }
    else ks = c.distinct(n, () => c.ri(20, 980), x => x);
    while (ks.length < n) { const k = c.ri(1, 999); if (!ks.includes(k)) ks.push(k); }
    const ONES = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"], TEENS = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"], TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"];
    const w99 = x => x < 10 ? ONES[x] : x < 20 ? TEENS[x - 10] : TENS[Math.floor(x / 10)] + (x % 10 ? "-" + ONES[x % 10] : "");
    const fracOf = k => { const g = h.gcd(k, 1000), d = 1000 / g; return d <= 40 ? [k / g, d] : null; };
    const show = k => {
      if (c.lvl < 3 || c.chance(.3)) return { html: dec(k) };
      const forms = [];
      const t = Math.floor(k / 100), hh = Math.floor(k % 100 / 10), th = k % 10;
      const ex = [t && `${t} tenth${t > 1 ? "s" : ""}`, hh && `${hh} hundredth${hh > 1 ? "s" : ""}`, th && `${th} thousandth${th > 1 ? "s" : ""}`].filter(Boolean);
      if (ex.length >= 2) forms.push({ html: ex.join(" + "), cls: "txt" });
      if (k % 10 === 0 && k < 1000) forms.push({ html: `${w99(k / 10)} hundredths`, cls: "txt" });
      const f = fracOf(k); if (f) forms.push({ html: h.frac(f[0], f[1]), cls: "mth", label: `${f[0]} over ${f[1]}` });
      forms.push({ html: `${(k / 1000).toFixed(3)}`, label: dec(k) });
      return c.pick(forms);
    };
    if (c.lvl === 3) { ks = ks.slice(0, n - 2).concat(c.sample([125, 375, 625, 875, 250, 750, 200, 400, 600, 800, 500].filter(k => !ks.includes(k)), 2)); }
    const cards = ks.slice(0, n).map(k => Object.assign({ v: k / 1000 }, show(k)));
    const down = c.opt.dir === "down";
    return { cards, desc: down, lo: down ? "Greatest" : "Least", hi: down ? "Least" : "Greatest", endCheck: c.lvl === 3, slotMin: c.lvl === 3 ? 130 : 96, tol: 1e-9,
      why: card => c.mode === "practice" ? `Line up the decimal points: ${(card.v).toFixed(3)}.` : "" };
  }
});
