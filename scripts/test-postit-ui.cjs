// UI smoke test: dialogs, hint button, real falling mode, keyboard play, narrow screens.
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path");
const OUT = path.resolve(process.env.POSTIT_SITE_DIR || "_site", "artifacts", "postit-games");
const games = fs.readdirSync(OUT).filter(d => fs.existsSync(path.join(OUT, d, "index.html")));
(async () => {
  const b = await chromium.launch({ args: ["--no-sandbox"] });
  let fails = 0;
  for (const g of games) {
    for (const vp of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
      const ctx = await b.newContext({ viewport: vp });
      await ctx.route("**/fonts.googleapis.com/**", r => r.abort());
      await ctx.addInitScript(() => { try { localStorage.setItem("pg:prefs", JSON.stringify({ sound: false })); } catch (e) {} });
      const p = await ctx.newPage(); const errs = [];
      p.on("pageerror", e => errs.push(e.message));
      await p.goto("file://" + path.join(OUT, g, "index.html") + "#level=2&code=31");
      await p.waitForTimeout(150);
      const r = await p.evaluate(async () => {
        const sleep = ms => new Promise(r => setTimeout(r, ms)); const q = s => document.querySelector(s); const out = {};
        for (const id of ["#helpBtn", "#optBtn", "#custBtn"]) { q(id).click(); await sleep(60); out[id] = !q("#dlg").hidden; q("#dlgOk").click(); await sleep(60); }
        const P = window.__PG; const eng = P.data.engine || P.G.engine;
        if (eng === "drop") { const st = q(".field .new"); if (st) { st.click(); await sleep(4500); const t = [...document.querySelectorAll(".field .tile")].find(t => P.data.test(t._item.key, P.K.st) === true && !t.classList.contains("pop")); if (t) t.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true })); await sleep(100); out.dropDone = P.R.done; } }
        // keyboard: focus first draggable tile, Enter selects, then Enter on first zone
        const tile = q(".tiles .tile, .deal .tile"); const zone = q(".dz");
        if (tile && zone) { tile.focus(); tile.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true })); out.kbSel = !!P.K.sel; zone.focus(); zone.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", bubbles: true })); await sleep(50); out.kbAfter = P.R.done + P.R.miss + (eng === "build" && q(".eq .slot .tile") ? 1 : 0); }
        q("#hintBtn").click(); await sleep(50);
        out.overflow = document.documentElement.scrollWidth > window.innerWidth + 2;
        return out;
      });
      const bad = errs.length || !r["#helpBtn"] || !r["#optBtn"] || !r["#custBtn"] || r.overflow || (r.kbSel === false) || (r.kbAfter === 0) || (r.dropDone === 0);
      if (bad) { fails++; console.log("FAIL", g, vp.width, JSON.stringify(r), errs.slice(0, 2).join(" | ")); }
      await ctx.close();
    }
    process.stdout.write(".");
  }
  console.log(`\nUI: ${games.length * 2} checks, ${fails} failures`);
  await b.close();
  process.exit(fails ? 1 : 0);
})();
