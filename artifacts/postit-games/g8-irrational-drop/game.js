PG.game({
  id: "g8-irrational-drop", title: ["Rational or", "Irrational?"], course: "Grade 8", unit: "Real Numbers",
  tag: "Snap the numbers that fit the rule: rational, or irrational. The rule switches!",
  skills: "8.NS.1–2 · rational vs irrational · perfect squares · repeating decimals · square roots and π",
  engine: "drop",
  levels: [
    "Square roots: perfect squares vs not.",
    "Fractions, terminating and repeating decimals, π and square roots.",
    "Sneaky ones: √(4/9), √0.25, 0.121212…, 1.0100100001…",
    "Expressions: √2 · √8, √3 + 1, (√5)², 2π ÷ π."
  ],
  options: [{ id: "board", label: "Board", type: "one", choices: [["fall", "Falling cards"], ["calm", "Calm board (no motion)"]], default: "fall" }],
  round(c) {
    const { h } = c;
    const items = [];
    const add = (html, rat, why) => items.push({ html, rat, why, cls: "mth" });
    for (let n = 2; n <= 100; n++) { const r = Math.sqrt(n); if (Number.isInteger(r)) add(h.sqrt(n), true, `√${n} = ${r}, a whole number.`); else if (c.lvl === 0 || c.chance(.25)) add(h.sqrt(n), false, `${n} isn't a perfect square, so √${n} never ends or repeats.`); }
    if (c.lvl >= 1) {
      add("π", false, "π never ends and never repeats."); add(h.frac(22, 7), true, "22/7 is a fraction of integers (it's only close to π)."); add("3.14", true, "3.14 ends, so it's rational.");
      ["0.75", "2.5", "−4", "0", "1.125"].forEach(x => add(x, true, `${x} can be written as a fraction.`));
      ["0.<span style=\"text-decoration:overline\">3</span>", "1.<span style=\"text-decoration:overline\">27</span>", "0.1<span style=\"text-decoration:overline\">6</span>"].forEach(x => add(x, true, "A repeating decimal is rational."));
      add(h.frac(3, 8), true, "Any fraction of integers is rational."); add("−" + h.frac(5, 3), true, "Negative fractions are rational too.");
      add("2π", false, "A multiple of π is irrational.");
    }
    if (c.lvl >= 2) {
      add(h.sqrt(h.frac(4, 9)), true, "√(4/9) = 2/3."); add(h.sqrt("0.25"), true, "√0.25 = 0.5."); add(h.sqrt(h.frac(2, 9)), false, "√(2/9) = √2 ÷ 3, and √2 is irrational.");
      add("0.121212…", true, "It repeats “12” forever, so it's rational."); add("1.0100100001…", false, "The pattern grows, so it never repeats: irrational."); add("0.123456789101112…", false, "It never repeats: irrational.");
      add("−" + h.sqrt(16), true, "−√16 = −4."); add(h.sqrt(50), false, "√50 = 5√2: irrational."); add(h.sqrt("1.21"), true, "√1.21 = 1.1.");
    }
    if (c.lvl === 3) {
      add(`${h.sqrt(2)} · ${h.sqrt(8)}`, true, "√2 · √8 = √16 = 4."); add(`${h.sqrt(3)} + 1`, false, "Irrational plus rational is irrational."); add(`(${h.sqrt(5)})<sup>2</sup>`, true, "(√5)² = 5.");
      add(`2π ÷ π`, true, "2π ÷ π = 2."); add(`${h.sqrt(12)} ÷ ${h.sqrt(3)}`, true, "√12 ÷ √3 = √4 = 2."); add(`${h.sqrt(2)} + ${h.sqrt(2)}`, false, "√2 + √2 = 2√2: irrational.");
      add(`π − π`, true, "π − π = 0."); add(`${h.sqrt(3)} · ${h.sqrt(3)}`, true, "√3 · √3 = 3."); add(`${h.sqrt(6)} · ${h.sqrt(2)}`, false, "√6 · √2 = √12 = 2√3: irrational."); add(`3${h.sqrt(4)}`, true, "3√4 = 3 · 2 = 6."); add(`${h.frac(h.sqrt(8), h.sqrt(2))}`, true, "√8 / √2 = √4 = 2."); add(`π<sup>2</sup> ÷ π`, false, "π² ÷ π = π.");
    }
    const byKey = {}; items.forEach(it => byKey[it.html] = it);
    const want = st => st.mode === "irr" ? false : true;
    const ensure = st => { if (!st.mode) st.mode = "irr"; };
    return {
      goal: c.n(18), calm: c.opt.board === "calm", size: 130,
      head(st) { ensure(st); return `<div><small>Snap the</small><div class="big">${st.mode === "irr" ? "IRRATIONAL" : "RATIONAL"}</div></div><div><small>numbers</small></div>`; },
      make(st, good) { ensure(st); const pool = items.filter(it => (it.rat === want(st)) === good); const it = c.pick(pool); return it ? { html: it.html, key: it.html, cls: "mth" } : null; },
      test(key, st) { ensure(st); const it = byKey[key]; return it.rat === want(st) ? true : it.why; },
      onHit(st) { if (st.found % 6 === 0) st.mode = st.mode === "irr" ? "rat" : "irr"; }
    };
  }
});
