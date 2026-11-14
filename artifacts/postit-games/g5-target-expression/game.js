PG.game({
  id: "g5-target-expression", title: ["Target", "Expression"], course: "Grade 5", unit: "Numerical Expressions & Order of Operations",
  tag: "Drag numbers (and operations) into the boxes to hit the target exactly.",
  skills: "5.OA.1–2 · order of operations · parentheses · writing and evaluating expressions",
  engine: "build",
  levels: [
    "Numbers only: ___ × ___ + ___ = target.",
    "Parentheses change everything: ___ × ( ___ + ___ ).",
    "Choose the operations too: ( ___ ◻ ___ ) ◻ ___.",
    "Four numbers, three operations, two sets of parentheses."
  ],
  how: ["Fill every box, then press Check.", "Multiplication and division happen before addition and subtraction, unless parentheses say otherwise.", "Many answers can work. Any true one counts!"],
  round(c) {
    const OPS = ["+", "−", "×", "÷"];
    const prec = o => (o === "×" || o === "÷" ? 2 : 1);
    const evalT = (toks, strict) => {
      const out = [], st = [];
      for (const t of toks) {
        if (typeof t === "number") out.push(t);
        else if (t === "(") st.push(t);
        else if (t === ")") { while (st.length && st[st.length - 1] !== "(") out.push(st.pop()); st.pop(); }
        else { while (st.length && st[st.length - 1] !== "(" && prec(st[st.length - 1]) >= prec(t)) out.push(st.pop()); st.push(t); }
      }
      while (st.length) out.push(st.pop());
      const s = [];
      for (const t of out) { if (typeof t === "number") { s.push(t); continue; } const b = s.pop(), a = s.pop(); if (a == null || b == null) return NaN; if (t === "÷" && strict && (b === 0 || a % b !== 0)) return NaN; s.push(t === "+" ? a + b : t === "−" ? a - b : t === "×" ? a * b : b === 0 ? NaN : a / b); }
      return s.length === 1 ? s[0] : NaN;
    };
    const templates = [
      ["n", "×", "n", "+", "n"], ["n", "+", "n", "×", "n"], ["n", "×", "n", "−", "n"],
      ["n", "×", "(", "n", "+", "n", ")"], ["(", "n", "−", "n", ")", "×", "n"], ["(", "n", "+", "n", ")", "÷", "n"], ["n", "×", "(", "n", "−", "n", ")"],
      ["(", "n", "o", "n", ")", "o", "n"], ["n", "o", "(", "n", "o", "n", ")"],
      ["(", "n", "o", "n", ")", "o", "(", "n", "o", "n", ")"]
    ];
    const pickT = () => c.lvl === 0 ? c.pick(templates.slice(0, 3)) : c.lvl === 1 ? c.pick(templates.slice(3, 7)) : c.lvl === 2 ? c.pick(templates.slice(7, 9)) : templates[9];
    const N = c.n(6), puzzles = [];
    let guard = 0;
    while (puzzles.length < N && guard++ < 2000) {
      const tpl = pickT();
      const nums = [], ops = [];
      const toks = tpl.map(t => t === "n" ? (nums.push(c.ri(1, c.lvl >= 2 ? 12 : 10)), nums[nums.length - 1]) : t === "o" ? (ops.push(c.pick(OPS)), ops[ops.length - 1]) : t);
      const T = evalT(toks, true);
      if (!Number.isInteger(T) || T <= 0 || T > (c.lvl >= 2 ? 150 : 120)) continue;
      const decoyN = [3, 3, 2, 2][c.lvl];
      const cardNums = nums.slice(); for (let i = 0; i < decoyN; i++) cardNums.push(c.ri(1, 12));
      const cardOps = ops.slice(); if (ops.length) cardOps.push(c.pick(OPS));
      const cards = c.shuffle(cardNums.map(v => ({ html: String(v), v })).concat(cardOps.map(v => ({ html: v, v, cls: "mth" }))));
      // build answer slot by slot
      const ans = []; let ni = 0, oi = 0;
      tpl.forEach(t => { if (t !== "n" && t !== "o") return; const v = t === "n" ? nums[ni++] : ops[oi++]; ans.push(cards.findIndex((cd, j) => cd.v === v && !ans.includes(j))); });
      const parts = tpl.map(t => (t === "n" || t === "o") ? { kind: t } : (t === "(" || t === ")" ? t : ` ${t} `)).concat([" = ", String(T)]);
      puzzles.push({
        prompt: `<div><small>Target</small><div class="big">${T}</div></div>`, parts, cards, answer: ans,
        show: v => v.some(x => x == null) ? "" : (() => { const r = build(v); return r.err ? r.err : `That makes ${+r.val.toFixed(3)}.`; })(),
        test: v => { const r = build(v); if (r.err) return r.err; return Math.abs(r.val - T) < 1e-9 ? true : `That expression equals ${+r.val.toFixed(3)}, not ${T}.${c.lvl >= 1 ? " Remember: parentheses first, then × and ÷, then + and −." : " Remember: × comes before +."}`; }
      });
      function build(v) {
        let k = 0; const tk = [];
        for (const t of tpl) { if (t === "n" || t === "o") { const x = v[k++]; if (t === "n" && typeof x !== "number") return { err: "Put a number in each square box." }; if (t === "o" && typeof x === "number") return { err: "Put an operation (+ − × ÷) in each operation box." }; tk.push(x); } else tk.push(t); }
        const val = evalT(tk); return isFinite(val) ? { val } : { err: "That expression can't be worked out (division by zero?)." };
      }
    }
    return { puzzles, note: c.lvl >= 2 ? "Operation cards: + − × ÷. Each card can be used once." : null };
  }
});
