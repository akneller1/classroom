// Headless test: every game × level × mode × several codes; auto-solve and check consistency.
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const OUT = path.resolve(process.env.POSTIT_SITE_DIR || "_site", "artifacts", "postit-games");
const only = process.argv.slice(2).filter(a => !a.startsWith("--"));
const CODES = +(process.argv.find(a => a.startsWith("--codes=")) || "--codes=3").split("=")[1];
const games = fs.readdirSync(OUT).filter(d => fs.existsSync(path.join(OUT, d, "game.js")) || fs.existsSync(path.join(OUT, d, "index.html"))).filter(d => d !== "index.html" && (!only.length || only.includes(d)));

const solver = async (page) => page.evaluate(async () => {
  const sleep = ms => new Promise(r => window.__realST(r, Math.min(ms, 30)));
  const P = window.__PG; if (!P || !P.data) return { err: "no round" };
  const { data, K, G, R } = P; const eng = data.engine || G.engine; const warn = [];
  const txt = h => PG.textify(h);
  const dz = () => [...document.querySelectorAll(".dz")];
  if (eng === "sort") {
    const seen = {}; data.cards.forEach(c => { const t = txt(c.html) + "|" + (c.html.includes("<svg") ? c.html.length + c.html.slice(0,400) : ""); const b = JSON.stringify(c.bins || c.bin); if (seen[t] != null && seen[t] !== b) warn.push("same card text, different bins: " + t); seen[t] = b; });
    for (const c of data.cards) { const id = c.bins ? c.bins[0] : c.bin; const z = dz().find(z => z._id === id); if (!z) return { err: "no bin " + id }; K.drop(c, z); }
  } else if (eng === "grid" || eng === "spots") {
    for (const z of dz()) { const key = (z._cell || z._s).key; const c = data.cards.find(c => c._btn && c._btn.isConnected && c.key === key); if (!c) return { err: "no card for key " + key }; K.drop(c, z); }
  } else if (eng === "order") {
    const vals = data.cards.map(c => c.v).sort((a, b) => a - b); if (data.desc) vals.reverse();
    const slots = [...document.querySelectorAll(".oslot")];
    slots.forEach((z, i) => { const c = data.cards.find(c => c._btn && c._btn.isConnected && Math.abs(c.v - vals[i]) <= (data.tol || 1e-9)); K.drop(c, z); });
    const ch = [...document.querySelectorAll("button.new")].find(b => b.textContent === "Check order"); if (ch) ch.click();
    for (let i = 1; i < data.cards.length; i++) if (Math.abs(vals[i] - vals[i - 1]) < 1e-12 && txt(data.cards.find(c => c.v === vals[i]).html) !== txt(data.cards.filter(c => c.v === vals[i]).slice(-1)[0].html)) {} // ties allowed
  } else if (eng === "match") {
    const as = {}, bs = {}; data.pairs.forEach((p, i) => { const ta = txt(p.a.html) + p.a.html.length, tb = txt(p.b.html) + p.b.html.length; if (as[ta] != null && as[ta] !== p.a.key) warn.push("dup A " + ta); if (bs[tb] != null && bs[tb] !== p.b.key) warn.push("dup B " + tb); as[ta] = p.a.key; bs[tb] = p.b.key; });
    if (data.style === "memory") { for (const p of data.pairs) { p.a._btn.click(); p.b._btn.click(); await sleep(5); } }
    else for (const p of data.pairs) K.drop(p.a, p.b._btn);
  } else if (eng === "groups") {
    const seen = {}; data.groups.forEach((g, gi) => g.items.forEach(it => { const t = txt(it.html) + it.html.length; if (seen[t] != null && seen[t] !== gi) warn.push("item in two groups: " + t); seen[t] = gi; }));
    const chk = [...document.querySelectorAll("button.new")].find(b => b.textContent === "Check group");
    for (const g of data.groups) { g.items.forEach(it => it._btn.click()); chk.click(); await sleep(5); }
  } else if (eng === "target" || eng === "build") {
    for (let i = 0; i < data.puzzles.length; i++) {
      const p = data.puzzles[i];
      if (!p.answer) return { err: "puzzle without answer" };
      const vals = p.answer.map(j => p.cards[j].v);
      if (new Set(p.answer).size !== p.answer.length) return { err: "answer reuses a card " + i };
      const res = p.test(vals, p.answer.map(j => p.cards[j]));
      if (res !== true) return { err: "answer fails own test: puzzle " + i + " -> " + res + " | " + txt(p.prompt || "") + " vals " + JSON.stringify(vals) };
      if (eng === "target") { p.answer.forEach(j => p.cards[j]._btn.click()); await sleep(200); const chk = [...document.querySelectorAll("button.new")].find(b => b.textContent === "Check"); if (chk && !chk.disabled) chk.click(); }
      else { const slots = [...document.querySelectorAll(".eq .slot")]; p.answer.forEach((j, si) => K.drop(p.cards[j], slots[si])); await sleep(220); const chk = [...document.querySelectorAll("button.new")].find(b => b.textContent === "Check"); if (chk && !chk.disabled) chk.click(); }
      await sleep(700);
      if (R.miss) return { err: "mistake after answer on puzzle " + i };
    }
  } else if (eng === "oddout") {
    for (let i = 0; i < data.puzzles.length; i++) {
      const p = data.puzzles[i]; if (p.odd == null || p.odd >= p.cards.length) return { err: "bad odd index" };
      p.cards[p.odd]._btn.click(); await sleep(10);
      const rb = [...document.querySelectorAll(".reasons button")]; if (rb.length) rb[p.reason].click();
      await sleep(p.why ? 1450 : 650);
    }
  } else if (eng === "drop") {
    const st = { found: 0 }; let bad = 0;
    for (let i = 0; i < 40; i++) { const g = data.make(st, true); if (!g || data.test(g.key, st) !== true) bad++; const b = data.make(st, false); if (b && data.test(b.key, st) === true) {} }
    if (bad > 2) return { err: "make(good) produced non-good " + bad + "/40" };
    // play calm board if present
    for (let k = 0; k < 400 && !R.over; k++) {
      const tiles = [...document.querySelectorAll(".static-field .tile:not(.gone)")];
      const t = tiles.find(t => data.test(t._item.key, K.st) === true);
      if (!t) { await sleep(400); continue; }
      t.click(); await sleep(5);
    }
  }
  await sleep(500);
  return { done: R.done, total: R.total, miss: R.miss, over: R.over, win: !document.getElementById('winOv').hidden, warn };
});

(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  let fails = 0, runs = 0; const warns = {};
  for (const g of games) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
    await ctx.addInitScript(() => { try { localStorage.setItem("pg:prefs", JSON.stringify({ sound: false, motion: true })); } catch (e) {} const st = window.setTimeout; window.__realST = st; window.setTimeout = (f, ms, ...a) => st(f, Math.min(ms || 0, 4), ...a); });
    await ctx.route("**/fonts.googleapis.com/**", r => r.abort());
    const page = await ctx.newPage(); const errs = [];
    page.on("pageerror", e => errs.push(e.message)); page.on("console", m => { if (m.type() === "error" && !/ERR_FAILED|net::/.test(m.text())) errs.push(m.text()); });
    let combos = [];
    if (process.argv.includes("--opts")) {
      await page.goto("file://" + path.join(OUT, g, "index.html"));
      const ops = await page.evaluate(() => (window.__PG.G.options || []).map(o => ({ id: o.id, ch: o.choices.map(c => String(c[0])) })));
      ops.forEach(o => o.ch.forEach(ch => { for (let lvl = 0; lvl < 4; lvl++) combos.push({ mode: "practice", lvl, code: "77" + lvl, extra: `&o.${o.id}=${ch}` }); }));
      combos.push({ mode: "practice", lvl: 1, code: "5", extra: "&len=0" }, { mode: "practice", lvl: 3, code: "6", extra: "&len=2" });
    } else for (const mode of ["practice", "timed", "challenge"]) for (let lvl = 0; lvl < 4; lvl++) for (let k = 0; k < (mode === "practice" ? CODES : 1); k++) combos.push({ mode, lvl, code: String(1000 + k * 37 + lvl), extra: "" });
    for (const { mode, lvl, code, extra } of combos) {
      await page.goto("about:blank");
      await page.goto("file://" + path.join(OUT, g, "index.html") + `#mode=${mode}&level=${lvl}&code=${code}${extra}`);
      await page.evaluate(() => new Promise(r => setTimeout(r, 30)));
      let res; try { res = await solver(page); } catch (e) { res = { err: "solver crash " + e.message }; }
      runs++;
      const tag = `${g} ${mode} L${lvl} #${code}${extra}`;
      if (res.warn && res.warn.length) (warns[g] = warns[g] || new Set()).add(res.warn[0]);
      if (res.err || errs.length || res.done !== res.total || res.miss || !res.win) { fails++; console.log("FAIL", tag, JSON.stringify(res), errs.slice(0, 2).map(e => e.split("\n")[0]).join(" | ")); errs.length = 0; }
    }
    await ctx.close();
    process.stdout.write(".");
  }
  console.log(`\n${runs} runs, ${fails} failures`);
  for (const [g, s] of Object.entries(warns)) console.log("WARN", g, [...s].join("; "));
  await browser.close();
  process.exit(fails ? 1 : 0);
})();
