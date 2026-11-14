PG.game({
  id: "g3-round-up", title: ["Rounding", "Rush"], course: "Grade 3", unit: "Place Value & Rounding",
  tag: "Snap every number that rounds to the target.",
  skills: "3.NBT.1 · round to the nearest 10 or 100 · halfway numbers round up",
  engine: "drop",
  levels: [
    "Nearest ten, numbers up to 100.",
    "Nearest ten, numbers up to 1,000.",
    "Nearest hundred, numbers up to 1,000.",
    "Tens and hundreds switch every few snaps, and halfway numbers (like 345 or 650) show up a lot."
  ],
  options: [{ id: "board", label: "Board", type: "one", choices: [["fall", "Falling cards"], ["calm", "Calm board (no motion)"]], default: "fall" }],
  round(c) {
    const rnd = (n, p) => Math.floor((n + p / 2) / p) * p;
    const newRule = st => {
      st.place = c.lvl <= 1 ? 10 : c.lvl === 2 ? 100 : (st.place === 10 ? 100 : 10);
      if (st.place === 10) st.T = c.lvl === 0 ? 10 * c.ri(2, 9) : 10 * c.ri(11, 98);
      else st.T = 100 * c.ri(2, 9);
    };
    const ensure = st => { if (st.T == null) newRule(st); };
    return {
      goal: c.n(18), calm: c.opt.board === "calm",
      head(st) { ensure(st); return `<div><small>Snap numbers that round to</small><div class="big">${st.T}</div></div><div><small>to the nearest</small><b>${st.place === 10 ? "ten" : "hundred"}</b></div>`; },
      make(st, good) {
        ensure(st); const p = st.place, T = st.T, half = p / 2;
        if (good) { const edge = c.lvl === 3 && c.chance(.45); const n = edge ? c.pick([T - half, T + half - 1]) : c.ri(T - half, T + half - 1); return n > 0 ? { html: String(n), key: n } : null; }
        const edge = c.chance(.4); let n = edge ? c.pick([T + half, T - half - 1]) : c.ri(T - 2 * p, T + 2 * p);
        if (rnd(n, p) === T || n <= 0) return null;
        return { html: String(n), key: n };
      },
      test(n, st) { ensure(st); const r = rnd(n, st.place); return r === st.T ? true : `${n} rounds to ${r}${n % (st.place / 2) === 0 && n % st.place !== 0 ? " (halfway rounds up)" : ""}.`; },
      onHit(st) { if (st.found % (c.lvl === 3 ? 4 : 6) === 0) newRule(st); }
    };
  }
});
