PG.game({
  id: "g2-skip-snap", title: ["Skip-Count", "Snap"], course: "Grade 2", unit: "Number Patterns & Skip Counting",
  tag: "Snap up the cards that follow the counting rule before they fall.",
  skills: "2.OA.3, 2.NBT.2, 2.NBT.8 · even and odd · skip-count by 5s, 10s, 100s · 10 or 100 more",
  engine: "drop",
  levels: [
    "Even or odd numbers up to 30. The rule switches every 6 snaps.",
    "Numbers you say counting by 5s or 10s, up to 120.",
    "Counting by 10s from a starting number like 23 (23, 33, 43…), up to 200.",
    "Keep the count going: tap only the NEXT number, counting up or back by 10s or 100s."
  ],
  options: [{ id: "board", label: "Board", type: "one", choices: [["fall", "Falling cards"], ["calm", "Calm board (no motion)"]], default: "fall", help: "Calm board shows still cards and works well with a keyboard or switch." }],
  round(c) {
    const lvl = c.lvl;
    const rules = {
      even: { head: "Snap the <b>EVEN</b> numbers", ok: n => n % 2 === 0, why: n => `${n} is odd. Even numbers end in 0, 2, 4, 6 or 8.`, pool: () => c.ri(1, 30) },
      odd: { head: "Snap the <b>ODD</b> numbers", ok: n => n % 2 === 1, why: n => `${n} is even. Odd numbers end in 1, 3, 5, 7 or 9.`, pool: () => c.ri(1, 30) },
      five: { head: "Snap numbers you say counting by <b>5s</b>", ok: n => n % 5 === 0, why: n => `${n} isn't a 5s number. Counting by 5s ends in 5 or 0.`, pool: () => c.ri(1, 120) },
      ten: { head: "Snap numbers you say counting by <b>10s</b>", ok: n => n % 10 === 0, why: n => `${n} isn't a 10s number. Counting by 10s ends in 0.`, pool: () => c.ri(1, 120) }
    };
    const st0 = {};
    let ruleSeq;
    if (lvl === 0) ruleSeq = c.shuffle(["even", "odd"]);
    else if (lvl === 1) ruleSeq = c.shuffle(["five", "ten"]);
    const newStart = () => { if (lvl === 2) return { start: c.ri(11, 59), step: 10 }; const down = c.chance(.5), step = c.pick([10, 100]); const start = step === 100 ? (down ? c.ri(700, 990) : c.ri(101, 350)) : (down ? c.ri(150, 400) : c.ri(12, 200)); return { start, step: down ? -step : step, k: 1 }; };
    const goal = c.n(18);
    const setRule = st => { if (lvl <= 1) st.rule = ruleSeq[Math.floor(st.found / 6) % 2]; else { Object.assign(st, newStart()); st.k = 1; } };
    let inited = false;
    const init = st => { if (!inited || st.rule == null && st.start == null) { inited = true; setRule(st); } };
    const member = (n, st) => lvl === 2 ? n >= st.start && n <= 210 && (n - st.start) % 10 === 0 : n === st.start + st.step * st.k;
    return {
      goal, calm: c.opt.board === "calm", speed: .9,
      ready: lvl === 3 ? "Tap only the next number in the count. Other numbers cost a life." : "Snap the cards that fit the rule. The rule is shown above the board.",
      head(st) {
        init(st);
        if (lvl <= 1) return `<div>${rules[st.rule].head}</div>`;
        if (lvl === 2) return `<div>Count by 10s from <b class="big">${st.start}</b><small>snap any number in that count, up to 210</small></div>`;
        const seen = []; for (let i = Math.max(0, st.k - 3); i < st.k; i++) seen.push(st.start + st.step * i);
        return `<div><small>Counting ${st.step > 0 ? "up" : "back"} by ${Math.abs(st.step)}s</small><div class="big">${seen.join(", ")}, ?</div></div>`;
      },
      make(st, good) {
        init(st);
        if (lvl <= 1) { const R = rules[st.rule]; if (good) { const n = st.rule === "even" ? 2 * c.ri(1, 15) : st.rule === "odd" ? 2 * c.ri(0, 14) + 1 : st.rule === "five" ? 5 * c.ri(1, 24) : 10 * c.ri(1, 12); return { html: String(n), key: n }; } for (let i = 0; i < 60; i++) { const n = R.pool(); if (R.ok(n) === good) return { html: String(n), key: n }; } return null; }
        if (lvl === 2) {
          if (good) { const n = st.start + 10 * c.ri(0, Math.floor((210 - st.start) / 10)); return { html: String(n), key: n }; }
          const base = st.start + 10 * c.ri(0, 12); const n = base + c.pick([1, -1, 5, -5, 2, 3, -3]); return n > 0 && !member(n, st) ? { html: String(n), key: n } : null;
        }
        const next = st.start + st.step * st.k;
        if (good) return { html: String(next), key: next };
        const n = next + c.pick([1, -1, 10, -10, 100, -100, st.step, 2 * st.step, -st.step].filter(d => d !== 0));
        return n > 0 && n !== next && n !== st.start + st.step * (st.k - 1) ? { html: String(n), key: n } : null;
      },
      test(n, st) {
        init(st);
        if (lvl <= 1) return rules[st.rule].ok(n) ? true : rules[st.rule].why(n);
        if (lvl === 2) return member(n, st) ? true : `${n} isn't in the count ${st.start}, ${st.start + 10}, ${st.start + 20}… Those all end in ${st.start % 10}.`;
        const next = st.start + st.step * st.k;
        return n === next ? true : `The next number is ${st.step > 0 ? Math.abs(st.step) + " more" : Math.abs(st.step) + " less"} than ${next - st.step}.`;
      },
      onHit(st) {
        if (lvl <= 1) { if (st.found % 6 === 0) setRule(st); }
        else if (lvl === 2) { if (st.found % 6 === 0) setRule(st); }
        else { st.k++; if (st.k > 6 || st.start + st.step * st.k <= 0 || st.start + st.step * st.k > 1000) setRule(st); }
      }
    };
  }
});
