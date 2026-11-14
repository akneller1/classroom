PG.game({
  id: "g4-prime-sprint", title: ["Prime Time", "Sprint"], course: "Grade 4", unit: "Factors & Multiples",
  tag: "Sort each number fast: prime or composite?",
  skills: "4.OA.4 · factor pairs · prime and composite numbers to 100 · square numbers have an odd number of factors",
  engine: "sort",
  levels: [
    "Prime or composite, numbers 2 to 30.",
    "Prime or composite, numbers up to 60.",
    "Numbers up to 100, with sneaky ones like 51, 57, 87 and 91.",
    "Sort by how many factors: 1, exactly 2, exactly 3, or 4 or more. Which numbers have exactly 3?"
  ],
  options: [{ id: "deal", label: "Cards", type: "one", choices: [["deal", "One at a time (sprint)"], ["all", "All at once"]], default: "deal" }],
  round(c) {
    const factors = n => { const f = []; for (let i = 1; i <= n; i++) if (n % i === 0) f.push(i); return f; };
    const pairText = n => { for (let i = 2; i * i <= n; i++) if (n % i === 0) return `${n} = ${i} × ${n / i}`; return ""; };
    const tricky = [27, 33, 39, 49, 51, 57, 63, 69, 77, 81, 87, 91, 93, 97, 89, 83, 79, 73, 71, 67, 61, 59, 53];
    const max = [30, 60, 100, 100][c.lvl];
    const N = c.n(14);
    const nums = c.distinct(N, () => (c.lvl >= 2 && c.chance(.5) ? c.pick(tricky) : c.lvl === 3 && c.chance(.25) ? c.pick([1, 4, 9, 25, 49, 16, 36, 64]) : c.ri(2, max)), x => x);
    let bins, cards;
    if (c.lvl < 3) {
      bins = [{ id: "p", label: "Prime", sub: "exactly 2 factors" }, { id: "c", label: "Composite", sub: "more than 2 factors" }];
      cards = nums.map(n => { const f = factors(n); const p = f.length === 2; return { html: String(n), bin: p ? "p" : "c", why: p ? `${n} is prime: its only factors are 1 and ${n}.` : `${n} is composite: ${pairText(n)}.`, hint: "Try dividing by 2, 3, 5 and 7." }; });
    } else {
      bins = [{ id: "1", label: "1 factor" }, { id: "2", label: "Exactly 2", sub: "prime" }, { id: "3", label: "Exactly 3" }, { id: "4", label: "4 or more" }];
      cards = nums.map(n => { const f = factors(n); const k = f.length >= 4 ? "4" : String(f.length); return { html: String(n), bin: k, why: `The factors of ${n} are ${f.join(", ")}: that's ${f.length}.` }; });
    }
    return { bins, cards, deal: c.opt.deal === "deal" };
  }
});
