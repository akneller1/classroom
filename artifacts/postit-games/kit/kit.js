/* Post-it Math Games kit: shared shell, settings, accessibility and engines. */
(() => {
"use strict";
const PG = window.PG = {};
const COLORS = ["#f4bd3a","#55c4b5","#f08a4b","#a39af7","#ef7fa1","#7fb3f0","#9ed36a"];
const GROUP_COLORS = ["#f4bd3a","#7fb3f0","#9ed36a","#ef7fa1","#a39af7","#55c4b5"];
PG.COLORS = COLORS;
const $ = (s, r = document) => r.querySelector(s);
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
PG.el = el;
const LEVELS = ["Easy", "Medium", "Hard", "Expert"];
const MODES = [["practice", "Practice"], ["timed", "Timed"], ["challenge", "Challenge"]];
const LEN = ["Short", "Standard", "Long"];
const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
};
PG.store = store;

/* ---------- seeded random ---------- */
function hashStr(s) { let h = 1779033703 ^ s.length; for (let i = 0; i < s.length; i++) { h = Math.imul(h ^ s.charCodeAt(i), 3432918353); h = h << 13 | h >>> 19; } h = Math.imul(h ^ h >>> 16, 2246822507); h = Math.imul(h ^ h >>> 13, 3266489909); return (h ^= h >>> 16) >>> 0; }
function makeRng(seed) {
  let a = hashStr(String(seed));
  const r = () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const R = {
    r,
    ri: (lo, hi) => lo + Math.floor(r() * (hi - lo + 1)),
    pick: a => a[Math.floor(r() * a.length)],
    shuffle: a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; },
    chance: p => r() < p,
    sign: () => (r() < .5 ? -1 : 1),
    nz: (lo, hi) => { let v = 0; while (v === 0) v = lo + Math.floor(r() * (hi - lo + 1)); return v; }
  };
  R.sample = (a, k) => R.shuffle(a).slice(0, k);
  /* distinct: call f() until k distinct keys */
  R.distinct = (k, f, key = x => JSON.stringify(x), tries = 400) => { const out = [], seen = new Set(); while (out.length < k && tries-- > 0) { const v = f(); const kk = key(v); if (v == null || seen.has(kk)) continue; seen.add(kk); out.push(v); } return out; };
  return R;
}
PG.rng = makeRng;

/* ---------- math helpers ---------- */
const MINUS = "−";
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a || 1; };
const lcm = (a, b) => Math.abs(a * b) / gcd(a, b);
const fmt = x => { if (typeof x !== "number") return String(x); const s = Number.isInteger(x) ? String(Math.abs(x)) : String(+Math.abs(x).toFixed(6)); return (x < 0 ? MINUS : "") + s; };
const H = PG.h = {
  MINUS, gcd, lcm, fmt, n: fmt,
  frac: (n, d) => `<span class="frac"><span>${n}</span><span>${d}</span></span>`,
  /* signed reduced or unreduced fraction from integers */
  f: (n, d, reduce = true) => { if (d < 0) { n = -n; d = -d; } if (reduce) { const g = gcd(n, d); n /= g; d /= g; } if (d === 1) return fmt(n); return (n < 0 ? MINUS : "") + H.frac(Math.abs(n), d); },
  mixed: (w, n, d) => `${w}${H.frac(n, d)}`,
  v: x => `<i class="mv">${x}</i>`,
  pow: (b, e) => `${b}<sup>${e}</sup>`,
  sqrt: x => `<span class="rad">√<span>${x}</span></span>`,
  par: x => `(${x})`,
  terms(ts) {
    let out = "", first = true;
    ts.forEach(([c, vp]) => {
      if (c === 0) return;
      const neg = c < 0, a = Math.abs(c);
      const body = vp ? ((a === 1 ? "" : fmt(a)) + vp) : fmt(a);
      out += first ? (neg ? MINUS : "") + body : (neg ? " " + MINUS + " " : " + ") + body;
      first = false;
    });
    return out || "0";
  },
  poly(cs, x = "x") { return H.terms(cs.map((c, i) => { const p = cs.length - 1 - i; return [c, p === 0 ? "" : p === 1 ? H.v(x) : H.v(x) + "<sup>" + p + "</sup>"]; })); },
  /* a*x + b style linear in one var */
  lin: (a, b, x = "x") => H.terms([[a, H.v(x)], [b, ""]])
};
/* small exact rationals */
const Q = PG.Q = (n, d = 1) => { if (d < 0) { n = -n; d = -d; } const g = gcd(n, d); return { n: n / g, d: d / g }; };
Q.add = (a, b) => Q(a.n * b.d + b.n * a.d, a.d * b.d);
Q.sub = (a, b) => Q(a.n * b.d - b.n * a.d, a.d * b.d);
Q.mul = (a, b) => Q(a.n * b.n, a.d * b.d);
Q.div = (a, b) => Q(a.n * b.d, a.d * b.n);
Q.eq = (a, b) => a.n === b.n && a.d === b.d;
Q.val = a => a.n / a.d;
Q.html = a => H.f(a.n, a.d);
Q.txt = a => (a.d === 1 ? String(a.n) : a.n + "/" + a.d);

/* ---------- svg helpers ---------- */
const S = PG.svg = {};
/* coordinate plane: returns {open, close, X, Y, w, h} ; ink for cards uses dark stroke */
S.plane = (o = {}) => {
  const { xmin = -6, xmax = 6, ymin = -6, ymax = 6, size = 120, pad = 6, grid = true, ink = "#13202f", gridc = "rgba(19,32,47,.18)", labels = false, step = 1 } = o;
  const w = size, h = size * (ymax - ymin) / (xmax - xmin);
  const X = x => pad + (x - xmin) / (xmax - xmin) * (w - 2 * pad);
  const Y = y => pad + (ymax - y) / (ymax - ymin) * (h - 2 * pad);
  let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-hidden="true">`;
  if (grid) { for (let x = Math.ceil(xmin); x <= xmax; x += step) s += `<line x1="${X(x)}" y1="${Y(ymin)}" x2="${X(x)}" y2="${Y(ymax)}" stroke="${gridc}" stroke-width="${o.gw || .7}"/>`; for (let y = Math.ceil(ymin); y <= ymax; y += step) s += `<line x1="${X(xmin)}" y1="${Y(y)}" x2="${X(xmax)}" y2="${Y(y)}" stroke="${gridc}" stroke-width="${o.gw || .7}"/>`; }
  if (xmin <= 0 && xmax >= 0) s += `<line x1="${X(0)}" y1="${Y(ymin)}" x2="${X(0)}" y2="${Y(ymax)}" stroke="${ink}" stroke-width="${o.aw || 1.3}"/>`;
  if (ymin <= 0 && ymax >= 0) s += `<line x1="${X(xmin)}" y1="${Y(0)}" x2="${X(xmax)}" y2="${Y(0)}" stroke="${ink}" stroke-width="${o.aw || 1.3}"/>`;
  if (labels) { const fs = o.fs || 10; for (let x = Math.ceil(xmin); x <= xmax; x += labels) if (x) s += `<text x="${X(x)}" y="${Y(0) + fs + 2}" font-size="${fs}" text-anchor="middle" fill="${ink}">${fmt(x)}</text>`; for (let y = Math.ceil(ymin); y <= ymax; y += labels) if (y) s += `<text x="${X(0) - 4}" y="${Y(y) + fs / 3}" font-size="${fs}" text-anchor="end" fill="${ink}">${fmt(y)}</text>`; }
  return { s, X, Y, w, h, xmin, xmax, ymin, ymax, ink, close: "</svg>" };
};
/* plot function f over plane P */
S.curve = (P, f, o = {}) => {
  const { color = "#2f5bd3", width = 2.4, x0 = P.xmin, x1 = P.xmax, n = 160 } = o;
  let d = "", pen = false;
  for (let i = 0; i <= n; i++) {
    const x = x0 + (x1 - x0) * i / n, y = f(x);
    if (!isFinite(y) || y < P.ymin - (P.ymax - P.ymin) || y > P.ymax + (P.ymax - P.ymin)) { pen = false; continue; }
    d += (pen ? "L" : "M") + P.X(x).toFixed(1) + " " + P.Y(y).toFixed(1); pen = true;
  }
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round"/>`;
};
S.dot = (P, x, y, o = {}) => `<circle cx="${P.X(x)}" cy="${P.Y(y)}" r="${o.r || 3}" fill="${o.fill || o.color || "#2f5bd3"}" stroke="${o.color || "#2f5bd3"}" stroke-width="1.5"/>`;
S.wrapClip = (P, inner) => { const id = "c" + Math.random().toString(36).slice(2, 8); const x0 = P.X(P.xmin), y0 = P.Y(P.ymax); return `<defs><clipPath id="${id}"><rect x="${x0}" y="${y0}" width="${P.X(P.xmax) - x0}" height="${P.Y(P.ymin) - y0}"/></clipPath></defs><g clip-path="url(#${id})">${inner}</g>`; };
S.graph = (fns, o = {}) => { const P = S.plane(o); let inner = ""; (Array.isArray(fns) ? fns : [fns]).forEach((f, i) => { inner += f.draw ? f.draw(P) : S.curve(P, f, { color: o.color || "#1d3a8f", ...(o.curve || {}) }); }); return P.s + S.wrapClip(P, inner) + P.close; };

/* text for screen readers / read aloud */
PG.textify = html => {
  const d = document.createElement("div"); d.innerHTML = html;
  d.querySelectorAll("svg").forEach(s => s.replaceWith(s.getAttribute("aria-label") || ""));
  d.querySelectorAll(".frac").forEach(f => { const p = f.children; f.replaceWith(" " + (p[0] ? p[0].textContent : "") + " over " + (p[1] ? p[1].textContent : "") + " "); });
  d.querySelectorAll(".rad").forEach(f => f.replaceWith(" square root of " + f.textContent.replace("√", "") + " "));
  d.querySelectorAll("sup").forEach(s => { const t = s.textContent.trim(); s.replaceWith(t === "2" ? " squared " : t === "3" ? " cubed " : /^[\w−-]?\w$/.test(t) ? " to the power " + t + " " : " to the power of (" + t + ") "); });
  return d.textContent.replace(/\s+/g, " ").trim();
};

/* ---------- prefs (accessibility) ---------- */
const prefs = Object.assign({ sound: true, speak: false, fs: 1, plain: false, hc: false, motion: false, theme: "auto" }, store.get("pg:prefs", {}));
function applyPrefs() {
  const r = document.documentElement;
  r.style.setProperty("--fs", prefs.fs);
  r.classList.toggle("plain", !!prefs.plain);
  r.classList.toggle("hc", !!prefs.hc);
  r.classList.toggle("nomotion", !!prefs.motion);
  if (prefs.theme === "auto") r.removeAttribute("data-theme"); else r.setAttribute("data-theme", prefs.theme);
  store.set("pg:prefs", prefs);
}
PG.prefs = prefs;
let ac = null;
function beep(freq, dur = .08, type = "triangle", vol = .07) {
  if (!prefs.sound) return;
  try { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); const o = ac.createOscillator(), g = ac.createGain(); o.type = type; o.frequency.value = freq; g.gain.value = vol; g.gain.exponentialRampToValueAtTime(.0001, ac.currentTime + dur); o.connect(g).connect(ac.destination); o.start(); o.stop(ac.currentTime + dur); } catch (e) {}
}
function speak(t) { if (!prefs.speak || !t || !window.speechSynthesis) return; try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(t); u.rate = .95; speechSynthesis.speak(u); } catch (e) {} }

/* ---------- game boot ---------- */
let G = null;          // game definition
let SET = null;        // settings for this game
let R = null;          // current round state
let K = null;          // engine api for current round
const ENG = {};
PG.engines = ENG;

PG.game = def => { G = def; if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot(); };

function defaults() {
  const o = {};
  (G.options || []).forEach(op => { o[op.id] = op.default != null ? op.default : (op.type === "multi" ? op.choices.map(c => c[0]) : op.choices[0][0]); });
  return { mode: "practice", level: 0, len: 1, opts: o, custom: "", useCustom: false };
}
function readHash() {
  const h = new URLSearchParams(location.hash.slice(1)); const out = {};
  if (h.has("mode")) out.mode = h.get("mode");
  if (h.has("level")) out.level = Math.max(0, Math.min(3, +h.get("level") || 0));
  if (h.has("len")) out.len = Math.max(0, Math.min(2, +h.get("len") || 0));
  if (h.has("code")) out.code = h.get("code").slice(0, 12);
  const o = {};
  h.forEach((v, k) => { if (k.startsWith("o.")) { const id = k.slice(2), op = (G.options || []).find(x => x.id === id); if (op) o[id] = op.type === "multi" ? v.split(",").filter(x => op.choices.some(c => String(c[0]) === x)).map(x => op.choices.find(c => String(c[0]) === x)[0]) : (op.choices.find(c => String(c[0]) === v) || [op.choices[0][0]])[0]; } });
  (G.options || []).filter(op => op.type === "multi").forEach(op => { if (o[op.id] && !o[op.id].length) o[op.id] = op.default || op.choices.map(c => c[0]); });
  if (Object.keys(o).length) out.opts = o;
  return out;
}
function linkFor(code) {
  const p = new URLSearchParams();
  p.set("mode", SET.mode); p.set("level", SET.level); p.set("len", SET.len); if (code) p.set("code", code);
  (G.options || []).forEach(op => { const v = SET.opts[op.id]; p.set("o." + op.id, Array.isArray(v) ? v.join(",") : v); });
  const url = new URL(location.href); url.searchParams.delete("share"); url.searchParams.set("student", "1"); url.hash = p.toString(); return url.href;
}

function boot() {
  applyPrefs();
  const saved = store.get("pg:set:" + G.id, null);
  SET = Object.assign(defaults(), saved || {});
  SET.opts = Object.assign(defaults().opts, SET.opts || {});
  const hs = readHash();
  if (hs.opts) Object.assign(SET.opts, hs.opts);
  ["mode", "level", "len"].forEach(k => { if (hs[k] != null) SET[k] = hs[k]; });
  if (!MODES.some(m => m[0] === SET.mode)) SET.mode = "practice";
  document.title = G.title.join(" ");
  buildShell();
  newRound(hs.code);
  if (new URLSearchParams(location.search).get("share") === "1") showCustomize();
}

function buildShell() {
  const w = el("div", "wrap");
  w.innerHTML = `
  <header class="top"><div><p class="crumb"><a href="../../../index.html">Mr. K’s Classroom</a> · <a href="../index.html">Post-it Games</a> · ${G.course} · ${G.unit}</p>
  <h1>${G.title[0]} <span>${G.title[1] || ""}</span></h1></div><p class="tag">${G.tag}</p></header>
  <div class="bar" role="toolbar" aria-label="Game settings">
    <div class="grp"><span id="modeL">Mode</span><div class="seg" id="modeSeg" role="group" aria-labelledby="modeL"></div></div>
    <div class="grp"><span id="levelL">Level</span><div class="seg" id="levelSeg" role="group" aria-labelledby="levelL"></div></div>
    <button class="new" id="newBtn" type="button">New round</button>
    <button class="tool" id="hintBtn" type="button">Hint</button>
    <button class="tool" id="custBtn" type="button">Customize</button>
    <button class="tool" id="optBtn" type="button">Options</button>
    <button class="tool" id="helpBtn" type="button">How to play</button>
    <div class="stats">
      <div class="stat"><small>Done</small><b id="progEl">0/0</b></div>
      <div class="stat miss"><small>Mistakes</small><b id="missEl">0</b></div>
      <div class="stat" id="scoreSt" hidden><small>Score</small><b id="scoreEl">0</b></div>
      <div class="stat" id="livesSt" hidden><small>Lives</small><div class="lives" id="livesEl"></div></div>
      <div class="stat"><small id="timeL">Time</small><b id="timeEl">0:00</b></div>
    </div>
  </div>
  <div class="main" id="mainEl">
    <section class="board" aria-label="Game board">
      <p class="level-note" id="levelNote"></p>
      <p class="msg" id="msgEl" aria-live="polite"></p>
      <div id="stage"></div>
    </section>
    <aside class="tray" id="trayEl" aria-label="Cards">
      <h2><span id="trayTitle">Cards</span><button type="button" id="shuffleBtn">Shuffle</button></h2>
      <div class="tiles" id="tiles"></div>
      <p class="hint" id="trayHint">Drag a card onto its spot, or tap a card and then tap the spot.</p>
    </aside>
  </div>
  <footer class="foot"><span>Round code <code id="codeEl">—</code> <button class="tool" id="replayBtn" type="button" style="padding:2px 8px;font-size:.8rem">Replay this round</button></span><span>${G.skills || ""}</span></footer>`;
  document.body.appendChild(w);
  if (new URLSearchParams(location.search).get("student") === "1") w.querySelector(".crumb").hidden = true;
  const ov = el("div"); ov.innerHTML = `
  <div class="overlay" id="winOv" hidden><div class="card center" role="dialog" aria-modal="true" aria-labelledby="winTitle">
    <div class="stars" id="starsEl"></div><div id="badgeEl"></div><h2 id="winTitle">Round complete!</h2>
    <div class="res" id="resEl"></div><p id="winNote"></p>
    <div class="row"><button class="new" id="againBtn" type="button">New round</button><button class="ghost-btn" id="upBtn" type="button">Try a harder level</button></div>
    <button class="ghost-btn" id="closeWin" type="button">Look at the board</button></div></div>
  <div class="overlay" id="dlg" hidden><div class="card wide" role="dialog" aria-modal="true" aria-labelledby="dlgTitle"><h2 id="dlgTitle"></h2><div id="dlgBody" style="display:grid;gap:14px"></div><div class="row"><button class="new" id="dlgOk" type="button">Done</button></div></div></div>
  <div class="flash" id="flashEl" aria-hidden="true"></div>`;
  document.body.appendChild(ov);

  const ms = $("#modeSeg");
  MODES.forEach(([v, t]) => { const b = el("button", "", t); b.type = "button"; b.dataset.v = v; ms.appendChild(b); });
  const ls = $("#levelSeg");
  LEVELS.forEach((t, i) => { const b = el("button", "", t); b.type = "button"; b.dataset.v = i; ls.appendChild(b); });
  syncSegs();
  ms.onclick = e => { const b = e.target.closest("button"); if (!b) return; SET.mode = b.dataset.v; saveSet(); syncSegs(); newRound(); };
  ls.onclick = e => { const b = e.target.closest("button"); if (!b) return; SET.level = +b.dataset.v; saveSet(); syncSegs(); newRound(); };
  $("#newBtn").onclick = () => newRound();
  $("#againBtn").onclick = () => newRound();
  $("#replayBtn").onclick = () => newRound(R && R.code);
  $("#closeWin").onclick = () => { $("#winOv").hidden = true; };
  $("#upBtn").onclick = () => upDefault();
  $("#hintBtn").onclick = () => { if (R && R.hint && !R.over) { R.hints++; R.hint(); beep(660, .06); } };
  $("#shuffleBtn").onclick = () => { const t = $("#tiles"); [...t.children].sort(() => Math.random() - .5).forEach(c => t.appendChild(c)); };
  $("#helpBtn").onclick = showHelp;
  $("#optBtn").onclick = showOptions;
  $("#custBtn").onclick = showCustomize;
  $("#dlgOk").onclick = closeDlg;
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") { if (!$("#dlg").hidden) closeDlg(); else if (!$("#winOv").hidden) $("#winOv").hidden = true; else K && K.select(null); }
    if (R && R.keys && $("#dlg").hidden && $("#winOv").hidden && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) R.keys(e);
  });
  window.addEventListener("hashchange", () => location.reload());
  document.addEventListener("visibilitychange", () => { if (document.hidden && R && R.pause) R.pause(); });
}
function syncSegs() {
  $("#modeSeg").querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", b.dataset.v === SET.mode));
  $("#levelSeg").querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", +b.dataset.v === SET.level));
}
function saveSet() { store.set("pg:set:" + G.id, { mode: SET.mode, level: SET.level, len: SET.len, opts: SET.opts, custom: SET.custom, useCustom: SET.useCustom }); }

/* ---------- dialogs ---------- */
let dlgReturn = null, dlgOnClose = null;
function openDlg(title, body, onClose) {
  dlgReturn = document.activeElement; dlgOnClose = onClose || null;
  $("#dlgTitle").textContent = title; const b = $("#dlgBody"); b.textContent = ""; b.appendChild(body);
  $("#dlg").hidden = false; setTimeout(() => (b.querySelector("button,input,textarea") || $("#dlgOk")).focus(), 30);
}
function closeDlg() { $("#dlg").hidden = true; const f = dlgOnClose; dlgOnClose = null; if (f) f(); if (dlgReturn && dlgReturn.focus) dlgReturn.focus(); }
const ENGINE_HOW = {
  sort: "Drag each card into the box where it belongs, or tap a card and then tap a box. With a card selected you can also press 1, 2, 3… to send it to that box.",
  grid: "Drag each card into the cell where it belongs, or tap a card and then tap a cell. The row and column headers light up to help.",
  order: "Put the cards in order from left to right. Drag a card into a slot, or tap a card and then tap a slot.",
  match: "Drag a card from the left column onto its partner in the right column, or tap one and then the other.",
  memory: "All cards start face down. Flip two at a time to find matching partners.",
  groups: "Find the groups hiding in the cards. Tap cards to select a group, then press Check group.",
  target: "Tap cards to select them so they hit the target. Press Check when you're ready.",
  drop: "Cards fall from the top. Tap only the cards that fit the rule before they reach the bottom.",
  spots: "Drag each card onto its spot on the picture, or tap a card and then tap a spot.",
  oddout: "Three cards share something. Tap the one that doesn't belong.",
  build: "Drag cards into the empty boxes to make the statement true. Tap a placed card to send it back."
};
function showHelp() {
  const d = el("div"); d.style.cssText = "display:grid;gap:12px";
  d.innerHTML = `<p>${G.about || G.tag}</p><h3>How to play</h3><ul>${(G.how || [ENGINE_HOW[G.engine]]).map(x => `<li>${x}</li>`).join("")}</ul>
  <h3>Modes</h3><ul><li><b>Practice</b>: no clock pressure. Hints are on and every mistake explains itself.</li><li><b>Timed</b>: race the clock. Your best time on each level is saved on this device.</li><li><b>Challenge</b>: 3 lives, a countdown, and streak bonuses. No hints.</li></ul>
  <h3>Levels</h3><ul>${LEVELS.map((l, i) => `<li><b>${l}</b>: ${G.levels[i]}</li>`).join("")}</ul>
  <p class="small">Teachers: Customize picks the skills, round length and a round code, so the whole class can play the same round. Options has text size, read-aloud, plain font, high contrast and reduced motion.</p>`;
  openDlg("How to play", d);
}
function toggleBtn(label, on, set) { const b = el("button", "tool", label); b.type = "button"; b.setAttribute("aria-pressed", !!on); b.onclick = () => { const v = b.getAttribute("aria-pressed") !== "true"; b.setAttribute("aria-pressed", v); set(v); }; return b; }
function segCtl(label, choices, cur, set) {
  const w = el("div", "opt"); w.appendChild(el("span", "", label)); const s = el("div", "seg");
  choices.forEach(([v, t]) => { const b = el("button", "", t); b.type = "button"; b.setAttribute("aria-pressed", v === cur); b.onclick = () => { s.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); set(v); }; s.appendChild(b); });
  w.appendChild(s); return w;
}
function showOptions() {
  const d = el("div"); d.style.cssText = "display:grid;gap:14px";
  const row = el("div", "chips");
  row.append(toggleBtn("Sound", prefs.sound, v => { prefs.sound = v; applyPrefs(); }),
    toggleBtn("Read cards aloud", prefs.speak, v => { prefs.speak = v; applyPrefs(); speak(v ? "Read aloud is on" : ""); }),
    toggleBtn("Plain font", prefs.plain, v => { prefs.plain = v; applyPrefs(); }),
    toggleBtn("High contrast", prefs.hc, v => { prefs.hc = v; applyPrefs(); }),
    toggleBtn("Reduce motion", prefs.motion, v => { prefs.motion = v; applyPrefs(); }));
  d.appendChild(row);
  d.appendChild(segCtl("Text size", [[1, "Normal"], [1.15, "Large"], [1.3, "Extra large"]], prefs.fs, v => { prefs.fs = v; applyPrefs(); }));
  d.appendChild(segCtl("Theme", [["auto", "Match device"], ["light", "Light"], ["dark", "Dark"]], prefs.theme, v => { prefs.theme = v; applyPrefs(); }));
  d.appendChild(el("p", "small", "Reduce motion also turns falling-card games into calm boards that don't move, which work well with a keyboard or switch. These settings are saved on this device for every game in the library."));
  openDlg("Options", d, () => { if (G.engine === "drop") newRound(R && R.code); });
}
function showCustomize() {
  const d = el("div"); d.style.cssText = "display:grid;gap:14px";
  const draft = JSON.parse(JSON.stringify(SET));
  (G.options || []).forEach(op => {
    const w = el("div", "opt"); w.appendChild(el("span", "", op.label));
    const c = el("div", op.type === "multi" ? "chips" : "seg");
    op.choices.forEach(([v, t]) => {
      const b = el("button", "", t); b.type = "button";
      const on = op.type === "multi" ? draft.opts[op.id].includes(v) : draft.opts[op.id] === v;
      b.setAttribute("aria-pressed", on);
      b.onclick = () => {
        if (op.type === "multi") {
          const cur = draft.opts[op.id]; const i = cur.indexOf(v);
          if (i >= 0) { if (cur.length > 1) cur.splice(i, 1); } else cur.push(v);
          c.querySelectorAll("button").forEach((x, j) => x.setAttribute("aria-pressed", cur.includes(op.choices[j][0])));
        } else { draft.opts[op.id] = v; c.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x === b)); }
      };
      c.appendChild(b);
    });
    w.appendChild(c); if (op.help) w.appendChild(el("p", "small", op.help)); d.appendChild(w);
  });
  d.appendChild(segCtl("Round length", LEN.map((t, i) => [i, t]), draft.len, v => draft.len = v));
  let ta = null, use = null;
  if (G.custom) {
    const w = el("div", "opt"); w.appendChild(el("span", "", G.custom.label || "Your own cards"));
    ta = el("textarea"); ta.value = draft.custom || ""; ta.placeholder = G.custom.placeholder || ""; ta.setAttribute("aria-label", G.custom.label || "Your own cards");
    w.appendChild(ta); w.appendChild(el("p", "small", G.custom.help || ""));
    use = toggleBtn("Play with my cards", draft.useCustom, v => draft.useCustom = v); w.appendChild(use);
    d.appendChild(w);
  }
  const cw = el("div", "opt"); cw.appendChild(el("span", "", "Round code"));
  const cr = el("div", "row"); const ci = el("input"); ci.type = "text"; ci.placeholder = "e.g. 4821"; ci.value = R ? R.code : ""; ci.setAttribute("aria-label", "Round code"); ci.maxLength = 12;
  cr.appendChild(ci); cw.appendChild(cr);
  cw.appendChild(el("p", "small", "Everyone who plays the same code with the same settings gets the same cards, so a class can race the same round."));
  d.appendChild(cw);
  const lr = el("div", "row"); const lb = el("button", "ghost-btn", "Copy link to these settings"); lb.type = "button";
  const rb = el("button", "ghost-btn", "Reset to defaults"); rb.type = "button";
  lr.append(lb, rb); d.appendChild(lr);
  const note = el("p", "small", ""); d.appendChild(note);
  const commit = () => { if (ta) draft.custom = ta.value; Object.assign(SET, { len: draft.len, opts: draft.opts, custom: draft.custom, useCustom: draft.useCustom }); saveSet(); };
  lb.onclick = () => { commit(); const link = linkFor(ci.value.trim() || (R && R.code)); if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(link).then(() => { note.textContent = "Link copied. Students who open it get these settings and this round."; }, () => { note.textContent = link; }); else note.textContent = link; };
  let applied = false;
  rb.onclick = () => { applied = true; Object.assign(SET, defaults()); saveSet(); closeDlg(); newRound(); };
  openDlg("Customize", d, () => { if (!applied) { applied = true; commit(); newRound(ci.value.trim() || undefined); } });
}

/* ---------- rounds ---------- */
function newRound(code) {
  if (R && R.stop) R.stop();
  clearInterval(R && R.iv);
  $("#winOv").hidden = true;
  code = code || String(1000 + Math.floor(Math.random() * 9000));
  const lvl = SET.level, rng = makeRng([G.id, code, SET.mode, lvl, SET.len, JSON.stringify(SET.opts), SET.useCustom ? SET.custom : ""].join("|"));
  R = { code, mode: SET.mode, lvl, done: 0, total: 0, miss: 0, hints: 0, streak: 0, best: 0, score: 0, lives: 3, secs: 0, t0: null, iv: null, over: false, hint: null, keys: null, stop: null, limit: 0 };
  $("#codeEl").textContent = code;
  $("#levelNote").textContent = LEVELS[lvl] + ": " + G.levels[lvl];
  $("#hintBtn").hidden = SET.mode !== "practice";
  $("#scoreSt").hidden = $("#livesSt").hidden = SET.mode !== "challenge";
  $("#timeL").textContent = SET.mode === "challenge" ? "Time left" : "Time";
  msg("");
  $("#stage").textContent = ""; $("#tiles").textContent = "";
  $("#mainEl").classList.remove("wide"); $("#trayEl").hidden = false;
  $("#trayTitle").textContent = "Cards"; $("#trayHint").textContent = "Drag a card onto its spot, or tap a card and then tap the spot.";
  const ctx = Object.assign({}, rng, {
    lvl, level: LEVELS[lvl], mode: SET.mode, len: SET.len, opt: SET.opts, h: H, Q, svg: S,
    n: base => Math.max(2, Math.round(base * [0.6, 1, 1.5][SET.len])),
    custom: null
  });
  if (G.custom && SET.useCustom && SET.custom.trim()) {
    try { ctx.custom = G.custom.parse(SET.custom, ctx); } catch (e) { ctx.custom = null; msg("Your custom cards couldn't be read: " + e.message, "bad"); }
  }
  let data;
  try { data = G.round(ctx); } catch (e) { console.error(e); msg("Something went wrong making this round. Press New round.", "bad"); return; }
  K = makeApi();
  const eng = ENG[data.engine || G.engine];
  const r = eng(data, K, ctx) || {};
  R.hint = r.hint || null; R.keys = r.keys || null; R.stop = r.stop || null; R.pause = r.pause || null;
  if (SET.mode === "challenge") R.limit = data.time || G.time && G.time(ctx, R.total) || Math.round(Math.max(40, R.total * (data.secsPer || G.secsPer || 9) * [1.2, 1, .9, .8][lvl]));
  stats();
  window.__PG = { R, data, K, G, SET };   // test hook
}

function msg(html, kind) { const m = $("#msgEl"); m.innerHTML = html || ""; m.className = "msg" + (kind ? " " + kind : "") + (html ? "" : " idle"); if (html && kind) speak(PG.textify(html)); }
function fmtT(s) { s = Math.max(0, s); return Math.floor(s / 60) + ":" + String(Math.floor(s % 60)).padStart(2, "0"); }
function stats() {
  if (!R) return;
  $("#progEl").textContent = R.done + "/" + R.total;
  $("#missEl").textContent = R.miss;
  $("#scoreEl").textContent = R.score;
  $("#timeEl").textContent = SET.mode === "challenge" ? fmtT(R.limit - R.secs) : fmtT(R.secs);
  const L = $("#livesEl"); L.textContent = ""; for (let i = 0; i < 3; i++) { const s = el("i"); if (i >= R.lives) s.className = "off"; L.appendChild(s); }
}
function startClock() {
  if (!R || R.t0 || R.over) return;
  R.t0 = performance.now() - R.secs * 1000;
  R.iv = setInterval(() => {
    if (R.paused) return;
    R.secs = (performance.now() - R.t0) / 1000; stats();
    if (SET.mode === "challenge" && R.secs >= R.limit) gameOver("Time's up!");
  }, 200);
}
let flashT;
function flash(t, kind) { const f = $("#flashEl"); f.textContent = t; f.className = "flash show " + kind; clearTimeout(flashT); flashT = setTimeout(() => f.className = "flash", 700); }

function finish() {
  if (R.over) return; R.over = true; clearInterval(R.iv);
  if (R.t0) R.secs = (performance.now() - R.t0) / 1000;
  stats();
  let stars, note = "", badge = "";
  const lvlName = LEVELS[R.lvl];
  if (SET.mode === "challenge") {
    const bonus = Math.max(0, Math.round((R.limit - R.secs) * 2)); R.score += bonus + R.lives * 25;
    stars = R.lives; note = `Time bonus +${bonus}, lives bonus +${R.lives * 25}.`;
  } else {
    const allow = Math.max(1, Math.round(R.total / 8));
    stars = R.miss === 0 && R.hints === 0 ? 3 : R.miss + R.hints <= allow ? 2 : 1;
  }
  const key = `pg:best:${G.id}:${SET.mode}:${R.lvl}`; const best = store.get(key, null);
  if (SET.mode === "timed") {
    if (best == null || R.secs < best) { store.set(key, R.secs); if (best != null) badge = "New best time"; note += `${lvlName} level. ` + (best != null ? `Old best ${fmtT(best)}.` : "First time on this level is saved."); }
    else note += `${lvlName} level. Best on this device: ${fmtT(best)}.`;
  } else if (SET.mode === "challenge") {
    if (best == null || R.score > best) { store.set(key, R.score); if (best != null) badge = "New high score"; }
    else note += ` High score on this device: ${best}.`;
  } else {
    const n = store.get(key, 0) + 1; store.set(key, n); note = `Practice rounds finished on ${lvlName}: ${n}.` + (R.hints ? ` Hints used: ${R.hints}.` : "");
  }
  $("#starsEl").innerHTML = "★".repeat(stars) + `<span class="dim">${"★".repeat(3 - stars)}</span>`;
  $("#badgeEl").innerHTML = badge ? `<span class="badge">${badge}</span>` : "";
  $("#winTitle").textContent = pickPraise(stars);
  $("#resEl").innerHTML = `<div><b>${fmtT(R.secs)}</b><span>Time</span></div><div><b>${R.miss}</b><span>Mistakes</span></div>` + (SET.mode === "challenge" ? `<div><b>${R.score}</b><span>Score</span></div>` : `<div><b>${R.best}</b><span>Best streak</span></div>`);
  $("#winNote").textContent = note.trim();
  $("#upBtn").onclick = upDefault;
  $("#upBtn").hidden = R.lvl === 3 && SET.mode === "challenge";
  $("#upBtn").textContent = R.lvl < 3 ? "Try " + LEVELS[R.lvl + 1] : SET.mode === "practice" ? "Try Timed mode" : "Try Challenge mode";
  $("#winOv").hidden = false; $("#againBtn").focus();
  [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => beep(f, .14), i * 110));
  speak($("#winTitle").textContent);
  if (R.stop) R.stop();
}
function pickPraise(s) { return s === 3 ? "Perfect round!" : s === 2 ? "Round complete!" : "You finished it!"; }
function gameOver(why) {
  if (R.over) return; R.over = true; clearInterval(R.iv); if (R.stop) R.stop(); stats();
  const key = `pg:best:${G.id}:challenge:${R.lvl}`; const best = store.get(key, null);
  let badge = ""; if (R.score > 0 && (best == null || R.score > best)) { store.set(key, R.score); badge = best != null ? "New high score" : ""; }
  $("#starsEl").innerHTML = `<span class="dim">★★★</span>`;
  $("#badgeEl").innerHTML = badge ? `<span class="badge">${badge}</span>` : "";
  $("#winTitle").textContent = why;
  $("#resEl").innerHTML = `<div><b>${R.done}/${R.total}</b><span>Done</span></div><div><b>${R.score}</b><span>Score</span></div><div><b>${R.best}</b><span>Best streak</span></div>`;
  $("#winNote").textContent = best != null && !badge ? `High score on this device: ${best}.` : "Challenge mode keeps your best score on each level.";
  $("#upBtn").hidden = false; $("#upBtn").textContent = "Switch to Practice";
  $("#upBtn").onclick = () => { SET.mode = "practice"; saveSet(); syncSegs(); newRound(); $("#upBtn").onclick = upDefault; };
  $("#winOv").hidden = false; $("#againBtn").focus(); beep(120, .35, "sawtooth", .05);
}
const upDefault = () => { if (SET.level < 3) SET.level++; else if (SET.mode !== "challenge") SET.mode = SET.mode === "practice" ? "timed" : "challenge"; saveSet(); syncSegs(); newRound(); };

/* ---------- engine api ---------- */
function makeApi() {
  const api = {
    stage: $("#stage"), tiles: $("#tiles"), sel: null, rng: null,
    mode: SET.mode, lvl: SET.level, practice: SET.mode === "practice",
    h: H, el, textify: PG.textify,
    wide() { $("#mainEl").classList.add("wide"); $("#trayEl").hidden = true; },
    trayTitle(t) { $("#trayTitle").textContent = t; },
    trayHint(t) { $("#trayHint").textContent = t; },
    total(n) { R.total = n; stats(); },
    msg, flash, beep, speak, start: startClock, stats,
    good(text, units = 1) {
      if (R.over) return; startClock();
      R.done += units; R.streak++; R.best = Math.max(R.best, R.streak);
      const mult = Math.min(4, 1 + Math.floor(R.streak / 3)); R.score += 10 * mult * units;
      beep(520 + Math.min(R.streak, 30) * 14, .09);
      if (text) msg(text, "good"); else if (R.streak && R.streak % 5 === 0) msg(`${R.streak} in a row!`, "good"); else msg("");
      stats(); if (R.done >= R.total) setTimeout(finish, 350);
    },
    bad(text, o = {}) {
      if (R.over) return; startClock();
      R.miss++; R.streak = 0; beep(170, .2, "sawtooth", .05);
      msg(text || "Not quite. Try again.", "bad");
      if (SET.mode === "challenge" && o.life !== false) { R.lives--; flash("−1 life", "bad"); if (R.lives <= 0) { stats(); setTimeout(() => gameOver("Out of lives"), 250); return; } }
      stats();
    },
    finish, isOver: () => R.over,
    /* create a post-it tile */
    tile(item, o = {}) {
      const b = el("button", "tile " + (item.cls || o.cls || ""), `<span class="tc">${item.html}</span>`);
      b.type = "button";
      item.color = item.color || o.color || COLORS[Math.floor(Math.random() * COLORS.length)];
      b.style.background = item.color;
      if (!o.flat) b.style.setProperty("--r", (Math.random() * 10 - 5).toFixed(1) + "deg");
      const lab = item.label || PG.textify(item.html);
      b.setAttribute("aria-label", lab); b._label = lab; b._item = item;
      b.addEventListener("focus", () => speak(lab));
      if (o.onClick) b.addEventListener("click", () => o.onClick(b));
      if (o.drag) api.draggable(b, item);
      return b;
    },
    /* selection + drag */
    select(item, btn, keep) {
      api.sel = item && api.sel === item && !keep ? null : item;
      document.querySelectorAll(".tile.sel").forEach(t => { t.classList.remove("sel"); t.setAttribute("aria-pressed", "false"); });
      if (api.sel && btn) { btn.classList.add("sel"); btn.setAttribute("aria-pressed", "true"); speak(btn._label); }
      if (!api.sel) hoverZone(null);
    },
    draggable(btn, item) {
      btn.setAttribute("aria-pressed", "false");
      btn.addEventListener("pointerdown", e => startDrag(e, item, btn));
      btn.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); api.select(item, btn, btn._sticky); } });
    },
    zone(z, accept, label) {
      z.classList.add("dz"); if (z.tagName !== "BUTTON") { z.tabIndex = 0; z.setAttribute("role", "button"); }
      if (label) z.setAttribute("aria-label", label);
      z._accept = accept;
      z.addEventListener("click", e => { if (api.sel) drop(api.sel, z); else if (z._tap) z._tap(e); });
      z.addEventListener("keydown", e => { if ((e.key === "Enter" || e.key === " ") && e.target === z) { e.preventDefault(); if (api.sel) drop(api.sel, z); else if (z._tap) z._tap(e); } });
      z.addEventListener("pointerenter", () => { if (api.sel && !drag) hoverZone(z); });
      z.addEventListener("pointerleave", () => { if (!drag) hoverZone(null); });
      z.addEventListener("focus", () => { if (api.sel) hoverZone(z); });
      return z;
    },
    drop: (item, z) => drop(item, z),
    hiZone: z => { z.classList.remove("hinted"); void z.offsetWidth; z.classList.add("hinted"); setTimeout(() => z.classList.remove("hinted"), 2100); },
    hiTile: t => { t.classList.remove("hinted"); void t.offsetWidth; t.classList.add("hinted"); setTimeout(() => t.classList.remove("hinted"), 2100); },
    shake: t => { if (!t) return; t.classList.remove("shake"); void t.offsetWidth; t.classList.add("shake"); },
    land: t => { if (!t) return; t.classList.remove("just"); void t.offsetWidth; t.classList.add("just"); },
    onHover: null
  };
  return api;
}
function hoverZone(z) {
  document.querySelectorAll(".dz.target").forEach(x => x.classList.remove("target"));
  if (z) z.classList.add("target");
  if (K && K.onHover) K.onHover(z);
}
function drop(item, z) {
  if (!R || R.over || !z || !z._accept) return;
  startClock();
  const ok = z._accept(item, z);
  hoverZone(null);
  if (ok) K.select(null);
  else { const t = document.querySelector(".tile.sel"); K.shake(t); }
}
let drag = null;
function startDrag(e, item, btn) {
  if (e.button !== undefined && e.button !== 0) return;
  if (R && R.over) return;
  e.preventDefault();
  drag = { item, btn, x0: e.clientX, y0: e.clientY, ghost: null, z: null };
  try { btn.setPointerCapture(e.pointerId); } catch (_) {}
  btn.addEventListener("pointermove", moveDrag); btn.addEventListener("pointerup", endDrag); btn.addEventListener("pointercancel", cancelDrag);
}
function moveDrag(e) {
  if (!drag) return;
  if (!drag.ghost) {
    if (Math.hypot(e.clientX - drag.x0, e.clientY - drag.y0) < 6) return;
    const g = drag.btn.cloneNode(true); g.classList.remove("sel", "shake", "hinted"); g.classList.add("drag-ghost"); g.removeAttribute("id");
    g.style.width = drag.btn.offsetWidth + "px"; g.style.height = drag.btn.offsetHeight + "px";
    document.body.appendChild(g); drag.ghost = g; drag.btn.classList.add("lift");
    K.select(drag.item, drag.btn); K.sel = drag.item;
  }
  drag.ghost.style.left = e.clientX + "px"; drag.ghost.style.top = e.clientY + "px";
  const t = document.elementFromPoint(e.clientX, e.clientY);
  const z = t && t.closest ? t.closest(".dz") : null;
  if (z !== drag.z) { drag.z = z; hoverZone(z); }
}
function cleanDrag() { if (!drag) return; const b = drag.btn; b.removeEventListener("pointermove", moveDrag); b.removeEventListener("pointerup", endDrag); b.removeEventListener("pointercancel", cancelDrag); drag.ghost && drag.ghost.remove(); b.classList.remove("lift"); }
function endDrag() {
  if (!drag) return; const d = drag; cleanDrag(); drag = null;
  if (!d.ghost) { K.select(d.item, d.btn); return; }
  hoverZone(null);
  if (d.z) drop(d.item, d.z); else K.select(null);
}
function cancelDrag() { cleanDrag(); drag = null; hoverZone(null); }

/* helper: fill tray with draggable tiles */
function trayFill(K, items, o = {}) {
  const out = items.map(it => { const t = K.tile(it, { drag: true, cls: o.cls }); it._btn = t; K.tiles.appendChild(t); return t; });
  return out;
}
function trayLeft(K) { return [...K.tiles.querySelectorAll(".tile")]; }
function emptyTray(K, text) { if (!K.tiles.querySelector(".tile")) { K.tiles.innerHTML = `<p class="empty">${text || "All cards placed."}</p>`; } }
function mini(item) { const m = el("span", "tile " + (item.cls || "") + " just", `<span class="tc">${item.html}</span>`); m.style.background = item.color || item._btn && item._btn.style.background || COLORS[0]; m.setAttribute("aria-label", item.label || PG.textify(item.html)); m.setAttribute("role", "img"); return m; }
PG.mini = mini;

/* ====================== ENGINES ====================== */

/* SORT: bins or venn; optional deal (one card at a time) */
ENG.sort = (d, K, ctx) => {
  const cards = d.cards; K.total(cards.length);
  const fits = (c, id) => (c.bins ? c.bins.includes(id) : c.bin === id);
  const zones = {};
  const binLabel = id => { const b = d.bins.find(x => x.id === id); return b ? PG.textify(b.label) : id; };
  const accept = (c, z) => {
    if (fits(c, z._id)) {
      c._btn.remove(); const m = mini(c); z._body.appendChild(m);
      K.good(d.say ? d.say(c, z._id) : null); placed++;
      if (d.deal) dealNext(); else emptyTray(K);
      if (z.classList) K.land(z._body);
      return true;
    }
    const right = c.bins ? c.bins.map(binLabel).join(" or ") : binLabel(c.bin);
    K.bad((c.why ? c.why + " " : "") + (K.practice && !c.why ? `It belongs in “${right}”.` : c.why ? "" : `That card doesn't go in “${binLabel(z._id)}”.`));
    return false;
  };
  let placed = 0;
  const st = K.stage;
  if (d.venn) {
    const v = el("div", "venn");
    v.innerHTML = `<svg class="vbg" viewBox="0 0 160 90" aria-hidden="true"><rect x="1" y="1" width="158" height="88" rx="6" fill="none" stroke="var(--line)" stroke-width=".8"/>
      <circle cx="60" cy="49" r="34" fill="color-mix(in srgb,#7fb3f0 22%,transparent)" stroke="var(--accent)" stroke-width="1"/>
      <circle cx="98" cy="49" r="34" fill="color-mix(in srgb,#f4bd3a 22%,transparent)" stroke="var(--gold)" stroke-width="1"/></svg>`;
    const Z = { A: [16, 27, 20, 56], AB: [40.5, 31, 17.5, 46], B: [63, 27, 20, 56], N: [85.5, 4, 13.5, 90] };
    const labs = { A: d.venn.A, B: d.venn.B, AB: "Both", N: d.venn.N || "Neither" };
    Object.entries(Z).forEach(([id, [x, y, w, h]]) => {
      const z = el("div", "vz"); z.style.cssText = `left:${x}%;top:${y}%;width:${w}%;height:${h}%`;
      z._id = id; z._body = z; K.zone(z, accept, labs[id].replace(/<[^>]+>/g, "")); v.appendChild(z); zones[id] = z;
    });
    [["A", 37.5, d.venn.A], ["B", 61.5, d.venn.B]].forEach(([id, x, t]) => { const l = el("span", "vlab", t); l.style.cssText = `left:${x}%;top:1%`; v.appendChild(l); });
    const n = el("span", "vlab", labs.N); n.style.cssText = "left:92%;top:1%;font-size:.75rem"; v.appendChild(n);
    st.appendChild(v);
    d.bins = [{ id: "A", label: d.venn.A + " only" }, { id: "AB", label: "Both" }, { id: "B", label: d.venn.B + " only" }, { id: "N", label: labs.N }];
  } else {
    const b = el("div", "bins"); b.style.setProperty("--bins", Math.min(d.bins.length, d.cols || 4));
    d.bins.forEach((bn, i) => {
      const z = el("div", "bin"); z._id = bn.id;
      z.innerHTML = `<div class="bin-h">${bn.label}${bn.sub ? `<small>${bn.sub}</small>` : ""}</div>`;
      z._body = el("div", "bin-body"); z.appendChild(z._body);
      K.zone(z, accept, `Box ${i + 1}: ${PG.textify(bn.label)}`); b.appendChild(z); zones[bn.id] = z;
    });
    st.appendChild(b);
  }
  let dealBox = null, cur = 0;
  function dealNext() {
    dealBox.textContent = "";
    const nxt = cards[++cur];
    if (!nxt) { dealBox.innerHTML = `<p class="empty">All cards sorted.</p>`; return; }
    show(nxt);
  }
  function show(c) { const t = K.tile(c, { drag: true, cls: c.cls }); t._sticky = true; c._btn = t; dealBox.appendChild(t); K.select(c, t, true); t.focus({ preventScroll: true }); }
  if (d.deal) {
    K.wide(); dealBox = el("div", "deal"); st.insertBefore(dealBox, st.firstChild);
    const hint = el("p", "hint", "Drag the card to its box, tap a box, or press " + d.bins.map((b, i) => (i + 1)).join(", ") + "."); st.insertBefore(hint, dealBox.nextSibling);
    cur = 0; show(cards[0]);
  } else { trayFill(K, ctx.shuffle(cards)); K.trayHint("Drag a card into a box, or tap a card then a box. With a card selected, press 1–" + d.bins.length + "."); }
  return {
    hint() {
      let c = K.sel || (d.deal ? cards[cur] : cards.find(x => x._btn && x._btn.isConnected));
      if (!c) return; if (!K.sel && c._btn) K.select(c, c._btn);
      const id = c.bins ? c.bins[0] : c.bin; K.hiZone(zones[id]);
      if (c.hint) K.msg(c.hint, "info");
    },
    keys(e) { const n = +e.key; if (K.sel && n >= 1 && n <= d.bins.length) { e.preventDefault(); K.drop(K.sel, zones[d.bins[n - 1].id]); } }
  };
};

/* GRID: row/col headers; cards go into cells with same key */
ENG.grid = (d, K, ctx) => {
  const nc = d.cols.length, hasRows = !!d.rows;
  const t = el("div", "gtab"); t.style.gridTemplateColumns = (hasRows ? (d.rowW || "minmax(80px,1.3fr) ") : "") + `repeat(${nc},minmax(0,${d.colW || "1fr"}))`;
  if (d.maxW) t.style.maxWidth = d.maxW;
  const heads = { r: [], c: [] };
  if (!d.noHead) {
    if (d.corner != null || hasRows) { const c = el("div", "gc", d.corner || ""); if (hasRows) t.appendChild(c); }
    d.cols.forEach((h, i) => { const e = el("div", "gh", h); heads.c[i] = e; t.appendChild(e); });
  }
  let zones = [];
  d.cells.forEach((row, ri) => {
    if (hasRows) { const e = el("div", d.rows[ri] === "" ? "blank" : "gh", d.rows[ri]); heads.r[ri] = e; t.appendChild(e); }
    row.forEach((cell, ci) => {
      if (!cell) { t.appendChild(el("div", "blank")); return; }
      if (cell.given) { t.appendChild(el("div", "given", cell.html)); return; }
      const z = el("button", "cell"); z.type = "button"; z._cell = cell; z._r = ri; z._c = ci;
      K.zone(z, accept, (d.cellLabel ? d.cellLabel(ri, ci) : `Row ${ri + 1}, column ${ci + 1}`) + ", empty");
      zones.push(z); t.appendChild(z);
    });
  });
  K.stage.appendChild(t);
  if (d.below) K.stage.appendChild(el("div", "", d.below));
  K.total(zones.length);
  function accept(c, z) {
    if (z._filled) return false;
    if (c.key === z._cell.key) {
      z._filled = true; z.classList.add("ok"); z.innerHTML = `<span class="tc">${z._cell.html || c.html}</span>`; z.disabled = true; K.land(z);
      z.setAttribute("aria-label", PG.textify(z.innerHTML));
      c._btn.remove(); emptyTray(K, d.doneText || "All cards placed. Extra cards left over were decoys.");
      K.good(c.say || null); if (zones.every(x => x._filled)) { K.tiles.querySelectorAll(".tile").forEach(x => x.disabled = true); }
      return true;
    }
    K.bad(d.why ? d.why(c, z._cell, z._r, z._c) : "That card doesn't belong in that cell.");
    return false;
  }
  K.onHover = z => {
    t.querySelectorAll(".gh.on").forEach(x => x.classList.remove("on"));
    if (z && z._cell) { heads.r[z._r] && heads.r[z._r].classList.add("on"); heads.c[z._c] && heads.c[z._c].classList.add("on"); }
  };
  trayFill(K, ctx.shuffle(d.cards), { cls: d.cardCls });
  if (d.trayTitle) K.trayTitle(d.trayTitle);
  return {
    hint() {
      const z = zones.find(x => !x._filled); if (!z) return;
      const c = d.cards.find(x => x._btn.isConnected && x.key === z._cell.key); if (!c) return;
      K.select(c, c._btn); K.hiZone(z); K.hiTile(c._btn);
    }
  };
};

/* ORDER: put cards in order; check each placement or check at end */
ENG.order = (d, K, ctx) => {
  const n = d.cards.length; const vals = d.cards.map(c => c.v).sort((a, b) => a - b); if (d.desc) vals.reverse();
  const tol = d.tol || 1e-9; const endCheck = !!d.endCheck;
  K.total(n);
  const ends = d.vertical ? el("div", "oends", `<span>↓ ${d.lo || "First"} at the top, ${d.hi || "last"} at the bottom</span>`) : el("div", "oends", `<span>← ${d.lo || "Least"}</span><span>${d.hi || "Greatest"} →</span>`);
  const line = el("div", "oline"); if (d.slotMin) line.style.gridTemplateColumns = `repeat(auto-fit,minmax(${d.slotMin}px,1fr))`;
  if (d.vertical) { line.style.gridTemplateColumns = "minmax(0,1fr)"; line.classList.add("vert"); }
  const slots = [];
  for (let i = 0; i < n; i++) {
    const z = el("div", "oslot"); z.innerHTML = `<span class="n">${i + 1}</span>`; z._i = i;
    K.zone(z, accept, `Slot ${i + 1}, empty`); z._tap = () => { if (endCheck && z._card && !z._locked) unplace(z); };
    slots.push(z); line.appendChild(z);
  }
  K.stage.append(ends, line);
  let checkBtn = null;
  if (endCheck) {
    const a = el("div", "actions"); checkBtn = el("button", "new", "Check order"); checkBtn.type = "button"; checkBtn.disabled = true;
    a.appendChild(checkBtn); a.appendChild(el("span", "hint", "Expert: no feedback until you check. Tap a placed card to take it back."));
    K.stage.appendChild(a); checkBtn.onclick = check;
  }
  function put(c, z) { z._card = c; c._btn.remove(); const t = K.tile(c, { flat: true }); t.style.transform = "none"; t.tabIndex = -1; z.appendChild(t); z.setAttribute("aria-label", `Slot ${z._i + 1}: ${t._label}`); K.land(t); }
  function unplace(z) { const c = z._card; z._card = null; z.querySelector(".tile").remove(); z.classList.remove("bad"); z.setAttribute("aria-label", `Slot ${z._i + 1}, empty`); const t = K.tile(c, { drag: true }); c._btn = t; K.tiles.querySelector(".empty") && K.tiles.querySelector(".empty").remove(); K.tiles.appendChild(t); if (checkBtn) checkBtn.disabled = true; }
  function accept(c, z) {
    if (z._card) { if (endCheck && !z._locked) { unplace(z); } else return false; }
    if (endCheck) { put(c, z); emptyTray(K, "All placed. Press Check order."); checkBtn.disabled = slots.some(s => !s._card); return true; }
    if (Math.abs(c.v - vals[z._i]) <= tol) { put(c, z); z._locked = true; z.classList.add("ok"); emptyTray(K); K.good(c.say || null); return true; }
    const exp = d.why ? d.why(c, z._i, vals) : "";
    const target = vals.findIndex((v, i) => Math.abs(v - c.v) <= tol && !slots[i]._card);
    const dir = target > z._i ? (d.desc ? "further right (it's smaller)" : "further right (it's bigger)") : (d.desc ? "further left (it's bigger)" : "further left (it's smaller)");
    K.bad((exp ? exp + " " : "") + (K.practice ? `That card goes ${dir}.` : "Not in that spot."));
    return false;
  }
  function check() {
    let wrong = 0;
    slots.forEach(z => { if (z._locked) return; if (Math.abs(z._card.v - vals[z._i]) <= tol) { z._locked = true; z.classList.add("ok"); } else { wrong++; z.classList.add("bad"); } });
    const good = slots.filter(z => z._locked && !z._counted); good.forEach(z => z._counted = true);
    if (good.length) K.good(wrong ? `${good.length} in the right place.` : null, good.length);
    if (wrong) { K.bad(`${wrong} card${wrong > 1 ? "s are" : " is"} out of place. They go back to the tray.`); setTimeout(() => slots.forEach(z => { if (z.classList.contains("bad")) unplace(z); }), 900); }
  }
  trayFill(K, ctx.shuffle(d.cards), { cls: d.cardCls });
  if (d.trayTitle) K.trayTitle(d.trayTitle);
  return {
    hint() {
      const z = slots.find(s => !s._card); if (!z) return;
      const c = d.cards.find(x => x._btn && x._btn.isConnected && Math.abs(x.v - vals[z._i]) <= tol); if (!c) return;
      K.select(c, c._btn); K.hiZone(z); K.hiTile(c._btn);
    }
  };
};

/* MATCH: open (drag a onto b) or memory (flip two) */
ENG.match = (d, K, ctx) => {
  const pairs = d.pairs; K.total(pairs.length);
  pairs.forEach((p, i) => { p.a.key = p.b.key = p.key != null ? p.key : i; p.a._p = p.b._p = p; });
  const done = el("div", "pairs");
  if (d.style === "memory") {
    K.wide();
    const g = el("div", "cardgrid"); g.style.setProperty("--cw", d.cw || "130px");
    const all = ctx.shuffle(pairs.flatMap(p => [p.a, p.b]));
    let open = [], lock = false; const seen = new Set();
    all.forEach(it => {
      const t = K.tile(it, { onClick: () => flip(t, it), flat: true }); t.classList.add("flip"); t.setAttribute("aria-label", "Face-down card"); it._btn = t; g.appendChild(t);
    });
    function flip(t, it) {
      if (lock || !t.classList.contains("flip") || R.over) return; K.start();
      t.classList.remove("flip"); t.setAttribute("aria-label", it.label || PG.textify(it.html)); K.speak(t._label); open.push([t, it]);
      if (open.length === 2) {
        const [[t1, a], [t2, b]] = open; open = [];
        if (a.key === b.key) {
          [t1, t2].forEach(x => { x.classList.add("gone"); x.disabled = true; });
          const pr = el("span", "pair"); pr.append(mini(a), document.createTextNode("="), mini(b)); done.appendChild(pr);
          K.good(a._p.say || null);
        } else {
          lock = true; const known = seen.has(a.label + a.html) && seen.has(b.label + b.html);
          K.bad(d.memoryWhy || "Not a match. Remember where they are!", { life: known });
          setTimeout(() => { [t1, t2].forEach(x => { x.classList.add("flip"); x.setAttribute("aria-label", "Face-down card"); }); lock = false; }, 1100 - K.lvl * 120);
        }
        seen.add(a.label + a.html); seen.add(b.label + b.html);
      }
    }
    K.stage.append(g, done);
    return { hint() { const rest = all.filter(x => x._btn.classList.contains("flip")); if (!rest.length) return; const a = rest[0]; const b = rest.find(x => x !== a && x.key === a.key); K.hiTile(a._btn); b && K.hiTile(b._btn); } };
  }
  const cols = el("div", "mcols");
  const L = el("div", "mcol"), Rr = el("div", "mcol");
  L.innerHTML = `<h3>${d.aTitle || "Cards"}</h3>`; Rr.innerHTML = `<h3>${d.bTitle || "Partners"}</h3>`;
  const bs = ctx.shuffle(pairs.map(p => p.b).concat(d.extraB || []));
  bs.forEach(b => {
    const t = K.tile(b, { flat: true }); b._btn = t; t.classList.add(...(d.bCls || "").split(" ").filter(Boolean));
    K.zone(t, (a, z) => {
      if (z._matched) return false;
      if (a.key === b.key) {
        z._matched = true; a._btn.remove(); t.remove();
        const pr = el("span", "pair"); pr.append(mini(a), document.createTextNode("↔"), mini(b)); done.appendChild(pr);
        K.good(a._p.say || null); return true;
      }
      K.bad(d.why ? d.why(a, b) : "Those two don't match."); return false;
    });
    Rr.appendChild(t);
  });
  ctx.shuffle(pairs.map(p => p.a)).forEach(a => { const t = K.tile(a, { drag: true, flat: true }); t.classList.add(...(d.aCls || "").split(" ").filter(Boolean)); a._btn = t; L.appendChild(t); });
  cols.append(L, Rr); K.wide(); K.stage.append(cols, el("p", "hint", "Drag a card on the left onto its partner on the right, or tap one and then the other."), done);
  return { hint() { const p = pairs.find(p => p.a._btn.isConnected); if (!p) return; K.select(p.a, p.a._btn); K.hiTile(p.b._btn); } };
};

/* GROUPS: find k groups of size s */
ENG.groups = (d, K, ctx) => {
  const size = d.groups[0].items.length; K.total(d.groups.length); K.wide();
  d.groups.forEach((g, gi) => g.items.forEach(it => it._g = gi));
  const items = ctx.shuffle(d.groups.flatMap(g => g.items));
  const solved = el("div", "solved"), grid = el("div", "cardgrid"); grid.style.setProperty("--cw", d.cw || "130px");
  const bar = el("div", "actions"); const chk = el("button", "new", "Check group"); chk.type = "button"; chk.disabled = true;
  const clr = el("button", "tool", "Deselect all"); clr.type = "button"; const info = el("span", "hint", `Select ${size} cards that belong together.`);
  bar.append(chk, clr, info);
  let picked = [];
  const tries = new Set();
  items.forEach(it => {
    const t = K.tile(it, { flat: true, onClick: () => toggle(t, it) }); it._btn = t; t.setAttribute("aria-pressed", "false"); grid.appendChild(t);
  });
  function toggle(t, it) {
    if (R.over) return; K.start();
    const i = picked.indexOf(it);
    if (i >= 0) picked.splice(i, 1); else if (picked.length < size) picked.push(it);
    items.forEach(x => x._btn.setAttribute("aria-pressed", picked.includes(x)));
    chk.disabled = picked.length !== size; info.textContent = `${picked.length} of ${size} selected.`;
  }
  clr.onclick = () => { picked = []; items.forEach(x => x._btn.setAttribute("aria-pressed", "false")); chk.disabled = true; info.textContent = `Select ${size} cards that belong together.`; };
  chk.onclick = () => {
    const sig = picked.map(x => items.indexOf(x)).sort().join(",");
    const counts = {}; picked.forEach(x => counts[x._g] = (counts[x._g] || 0) + 1);
    const top = Math.max(...Object.values(counts));
    if (top === size) {
      const g = d.groups[picked[0]._g];
      picked.forEach(x => x._btn.remove());
      const row = el("div", "solved-row"); row.style.background = GROUP_COLORS[solved.children.length % GROUP_COLORS.length];
      row.innerHTML = `<b>${g.label}</b><div class="items">${g.items.map(x => `<span>${x.html}</span>`).join("")}</div>`;
      solved.appendChild(row); picked = []; chk.disabled = true; info.textContent = `Select ${size} cards that belong together.`;
      K.good(g.say || null);
    } else {
      if (tries.has(sig)) { K.msg("You already tried that group.", "info"); return; }
      tries.add(sig);
      K.bad(top === size - 1 ? "One away! Three of those belong together." : "Those don't all belong together.");
    }
  };
  K.stage.append(solved, grid, bar);
  return { hint() { const g = d.groups.find(g => g.items.some(x => x._btn.isConnected)); if (!g) return; K.msg(`One group: <b>${g.label}</b>`, "info"); g.items.slice(0, 2).forEach(x => K.hiTile(x._btn)); } };
};

/* TARGET: series of puzzles; tap cards to reach a target */
ENG.target = (d, K) => {
  const P = d.puzzles; K.total(P.length); K.wide();
  const pips = el("div", "pips"); P.forEach(() => pips.appendChild(el("i")));
  const prompt = el("div", "prompt"), grid = el("div", "cardgrid"), bar = el("div", "actions");
  grid.style.setProperty("--cw", d.cw || "110px");
  const chk = el("button", "new", "Check"); chk.type = "button"; const clr = el("button", "tool", "Clear"); clr.type = "button";
  const run = el("span", "hint", "");
  bar.append(chk, clr, run);
  K.stage.append(pips, prompt, grid, bar);
  let i = -1, picked = [], busy = false;
  function next() {
    i++; busy = false; if (i >= P.length) return;
    [...pips.children].forEach((p, j) => p.className = j < i ? (p.classList.contains("x") ? "x" : "on") : j === i ? "cur" : "");
    const p = P[i]; picked = [];
    prompt.innerHTML = p.prompt; grid.textContent = "";
    p.cards.forEach((c, ci) => { c._i = ci; const t = K.tile(c, { flat: !!d.flat, onClick: () => toggle(c) }); t.setAttribute("aria-pressed", "false"); c._btn = t; grid.appendChild(t); });
    upd();
  }
  function toggle(c) {
    if (R.over || busy) return; K.start();
    const j = picked.indexOf(c); if (j >= 0) picked.splice(j, 1); else { if (P[i].k && picked.length >= P[i].k) return; picked.push(c); }
    upd();
    if (P[i].k && picked.length === P[i].k && d.auto !== false) setTimeout(check, 180);
  }
  function upd() {
    const p = P[i]; P[i].cards.forEach(c => c._btn.setAttribute("aria-pressed", picked.includes(c)));
    chk.disabled = !picked.length || (p.k && picked.length !== p.k);
    run.innerHTML = p.show && picked.length && (K.practice || K.lvl < 2) ? p.show(picked.map(c => c.v), picked) : p.k ? `Pick ${p.k} card${p.k > 1 ? "s" : ""}.` : "Pick cards, then press Check.";
  }
  function check() {
    if (R.over || busy || !picked.length) return;
    const res = P[i].test(picked.map(c => c.v), picked);
    if (res === true) { busy = true; chk.disabled = true; pips.children[i].className = pips.children[i].classList.contains("x") ? "x" : "on"; K.good(P[i].say || null); if (i + 1 < P.length) setTimeout(next, 450); }
    else { pips.children[i].classList.add("x"); K.bad(typeof res === "string" ? res : "That doesn't hit the target."); picked = []; upd(); }
  }
  chk.onclick = check; clr.onclick = () => { picked = []; upd(); };
  next();
  return { hint() { const a = P[i] && P[i].answer; if (!a) return; const c = P[i].cards[a.find(x => !picked.includes(P[i].cards[x]))]; c && K.hiTile(c._btn); } };
};

/* ODD ONE OUT: tap the card that doesn't belong; optional reason step */
ENG.oddout = (d, K) => {
  const P = d.puzzles; K.total(P.length); K.wide();
  const pips = el("div", "pips"); P.forEach(() => pips.appendChild(el("i")));
  const grid = el("div", "cardgrid"); grid.style.setProperty("--cw", d.cw || "160px");
  const rs = el("div", "reasons"); const ask = el("p", "hint", "");
  K.stage.append(pips, el("p", "hint", d.ask || "Three cards share something. Tap the odd one out."), grid, ask, rs);
  let i = -1, step = 0, missed = false;
  function next() {
    i++; if (i >= P.length) return; step = 0; missed = false; rs.textContent = ""; ask.textContent = "";
    [...pips.children].forEach((p, j) => { if (j === i) p.className = "cur"; });
    grid.textContent = "";
    P[i].cards.forEach((c, ci) => { const t = K.tile(c, { flat: true, onClick: () => tap(ci, t) }); c._btn = t; grid.appendChild(t); });
  }
  function tap(ci, t) {
    if (R.over || step) return; K.start();
    const p = P[i];
    if (ci === p.odd) {
      t.style.outline = "3px solid var(--good)"; t.style.outlineOffset = "3px";
      if (p.reasons && (K.lvl >= (d.reasonFrom != null ? d.reasonFrom : 2))) {
        step = 1; ask.textContent = "Why doesn't it belong?";
        p.reasons.forEach((r, ri) => { const b = el("button", "", r); b.type = "button"; b.onclick = () => reason(ri, b); rs.appendChild(b); });
        rs.querySelector("button").focus();
      } else done();
    } else { missed = true; K.shake(t); K.bad(p.whyNot ? p.whyNot(ci) : "That one fits with the others. Look again."); }
  }
  function reason(ri, b) {
    if (R.over || step !== 1) return;
    if (ri === P[i].reason) { b.classList.add("good"); step = 2; done(); }
    else { b.classList.add("bad"); b.disabled = true; K.bad("Not the reason. Try another."); }
  }
  function done() { pips.children[i].className = missed ? "x" : "on"; K.good(P[i].why || null); if (i + 1 < P.length) setTimeout(next, P[i].why ? 1400 : 600); }
  next();
  return { hint() { const p = P[i]; if (!p || step) return; const c = p.cards.findIndex((x, j) => j !== p.odd && x._btn.style.opacity !== ".3"); if (c >= 0) { p.cards[c]._btn.style.opacity = ".3"; p.cards[c]._btn.disabled = true; } } };
};

/* BUILD: fill slots in a template with cards to make it true */
ENG.build = (d, K) => {
  const P = d.puzzles; K.total(P.length);
  const pips = el("div", "pips"); P.forEach(() => pips.appendChild(el("i")));
  const prompt = el("div", "prompt"), eq = el("div", "eq"), bar = el("div", "actions");
  const chk = el("button", "new", "Check"); chk.type = "button"; const clr = el("button", "tool", "Clear"); clr.type = "button";
  const info = el("span", "hint", ""); bar.append(chk, clr, info);
  K.stage.append(pips, prompt, eq, bar);
  if (d.note) K.stage.appendChild(el("p", "hint", d.note));
  let i = -1, slots = [], busy = false;
  function next() {
    i++; busy = false; if (i >= P.length) return;
    [...pips.children].forEach((p, j) => { if (j === i) p.className = "cur"; });
    const p = P[i]; prompt.innerHTML = p.prompt || ""; prompt.hidden = !p.prompt; eq.textContent = ""; K.tiles.textContent = ""; slots = [];
    p.parts.forEach(part => {
      if (typeof part === "string") { eq.appendChild(el("span", "fx", part)); return; }
      const z = el("div", "slot" + (part.kind === "o" ? " op" : "")); z._i = slots.length; slots.push(z);
      K.zone(z, (c, zz) => { if (zz._card) unplace(zz); place(c, zz); return true; }, `Box ${slots.length}, empty`);
      z._tap = () => { if (z._card) unplace(z); };
      eq.appendChild(z);
    });
    p.cards.forEach(c => { c._slot = null; const t = K.tile(c, { drag: true, cls: d.cardCls }); c._btn = t; K.tiles.appendChild(t); });
    upd();
  }
  function place(c, z) {
    if (c._slot) unplace(c._slot);
    c._btn.remove(); z._card = c; c._slot = z;
    const t = K.tile(c, { flat: true, cls: d.cardCls }); t.style.transform = "none"; t.tabIndex = -1; z.appendChild(t); K.land(t);
    z.setAttribute("aria-label", `Box ${z._i + 1}: ${t._label}. Activate to remove.`); upd();
    if (slots.every(s => s._card) && d.auto) setTimeout(check, 200);
  }
  function unplace(z) {
    const c = z._card; if (!c) return; z._card = null; c._slot = null; z.querySelector(".tile") && z.querySelector(".tile").remove(); z.setAttribute("aria-label", `Box ${z._i + 1}, empty`);
    const t = K.tile(c, { drag: true, cls: d.cardCls }); c._btn = t; K.tiles.appendChild(t); upd();
  }
  function upd() { if (busy) return; chk.disabled = slots.some(s => !s._card); const p = P[i]; info.innerHTML = p.show && (K.practice || K.lvl < 2) ? p.show(slots.map(s => s._card && s._card.v)) : slots.some(s => !s._card) ? "Fill every box." : "Press Check."; }
  function check() {
    if (R.over || busy || slots.some(s => !s._card)) return;
    const vals = slots.map(s => s._card.v);
    const res = P[i].test(vals, slots.map(s => s._card));
    if (res === true) { busy = true; chk.disabled = true; pips.children[i].className = pips.children[i].classList.contains("x") ? "x" : "on"; K.good(P[i].say || null); slots.forEach(s => s.classList.add("ok")); if (i + 1 < P.length) setTimeout(next, 650); else chk.disabled = true; }
    else { pips.children[i].classList.add("x"); K.bad(typeof res === "string" ? res : "Not true yet. Try different cards."); }
  }
  chk.onclick = check; clr.onclick = () => slots.forEach(unplace);
  if (d.trayTitle) K.trayTitle(d.trayTitle);
  K.trayHint("Drag a card into a box, or tap a card then a box. Tap a placed card to send it back.");
  next();
  return {
    hint() {
      const p = P[i]; if (!p.answer) return;
      const si = slots.findIndex((s, j) => !s._card || s._card !== p.cards[p.answer[j]]);
      if (si < 0) return; const c = p.cards[p.answer[si]]; if (slots[si]._card) unplace(slots[si]);
      place(c, slots[si]);
    }
  };
};

/* SPOTS: drop cards on hotspots placed over an svg picture */
ENG.spots = (d, K, ctx) => {
  const box = el("div", "spots"); box.innerHTML = d.svg; if (d.maxW) box.style.maxWidth = d.maxW;
  const zones = [];
  d.spots.forEach((s, i) => {
    const z = el("button", "spot" + (s.cls ? " " + s.cls : "")); z.type = "button";
    z.style.left = (s.x / d.w * 100) + "%"; z.style.top = (s.y / d.h * 100) + "%";
    if (s.html) z.innerHTML = s.html;
    z._s = s; K.zone(z, accept, s.label || `Spot ${i + 1}, empty`); zones.push(z); box.appendChild(z);
  });
  K.stage.appendChild(box);
  K.total(zones.length);
  function accept(c, z) {
    if (z._filled) return false;
    if (c.key === z._s.key) { z._filled = true; z.classList.add("ok"); z.innerHTML = `<span class="tc">${d.fill ? d.fill(c) : c.html}</span>`; z.setAttribute("aria-label", "Filled: " + (c.label || PG.textify(c.html))); K.land(z); c._btn.remove(); emptyTray(K); K.good(c.say || null); return true; }
    K.bad(d.why ? d.why(c, z._s) : "That card doesn't go on that spot."); return false;
  }
  trayFill(K, ctx.shuffle(d.cards), { cls: d.cardCls });
  if (d.trayTitle) K.trayTitle(d.trayTitle);
  return { hint() { const z = zones.find(x => !x._filled); if (!z) return; const c = d.cards.find(x => x._btn.isConnected && x.key === z._s.key); if (!c) return; K.select(c, c._btn); K.hiZone(z); } };
};

/* DROP: falling cards; tap the ones that fit. Calm (static) board when motion is reduced or chosen. */
ENG.drop = (d, K) => {
  K.wide(); K.total(d.goal);
  const head = el("div", "prompt"); K.stage.appendChild(head);
  const calm = prefs.motion || d.calm;
  const st = { found: 0 }; K.st = st;
  const setHead = () => head.innerHTML = d.head(st);
  setHead();
  if (calm) {
    const grid = el("div", "static-field"); K.stage.appendChild(grid);
    K.stage.appendChild(el("p", "hint", "Calm board: tap every card that fits. A new board appears when you've found them all."));
    let cards = [];
    function fill() {
      grid.textContent = ""; cards = [];
      const n = 9, goods = Math.max(1, Math.min(d.goal - st.found, 2 + (K.lvl < 2 ? 1 : 0)));
      const seen = new Set(); let tries = 0;
      const items = [];
      while (items.length < n && tries++ < 300) { const want = items.filter(x => x.good).length < goods; const it = d.make(st, want); if (!it || seen.has(it.key)) continue; it.good = d.test(it.key, st) === true; if (it.good && !want) continue; seen.add(it.key); items.push(it); }
      items.sort(() => Math.random() - .5).forEach(it => { const t = K.tile(it, { onClick: () => tap(it, t) }); it._btn = t; cards.push(it); grid.appendChild(t); });
    }
    function tap(it, t) {
      if (R.over || t.classList.contains("gone")) return; K.start();
      const r = d.test(it.key, st);
      if (r === true) { t.classList.add("gone"); t.disabled = true; st.found++; if (d.onHit) d.onHit(st, it.key); setHead(); K.good(); if (st.found < d.goal && !cards.some(c => !c._btn.classList.contains("gone") && d.test(c.key, st) === true)) setTimeout(fill, 350); }
      else { K.shake(t); K.bad(typeof r === "string" ? r : "That one doesn't fit."); }
    }
    fill();
    return { hint() { const c = cards.find(c => !c._btn.classList.contains("gone") && d.test(c.key, st) === true); c && K.hiTile(c._btn); } };
  }
  const field = el("div", "field"); K.stage.appendChild(field);
  const startCard = el("div", "overlay"); startCard.style.position = "absolute";
  startCard.innerHTML = `<div class="card center"><h2>Ready?</h2><p>${d.ready || "Tap only the cards that fit the rule. Don't let a good card fall past the red line."}</p><button class="new" type="button">Start</button></div>`;
  field.appendChild(startCard);
  let W = 0, Hh = 0, cols = 5, colW = 0, size = 0, raf = 0, last = 0, tiles = [], playing = false, paused = false, sinceSpawn = 9, sinceGood = 0;
  const speedMul = (K.mode === "practice" ? .7 : 1) * [0.8, 1, 1.2, 1.4][K.lvl] * (d.speed || 1);
  function measure() { const r = field.getBoundingClientRect(); W = r.width; Hh = r.height; cols = W < 440 ? 3 : W < 700 ? 4 : 5; colW = W / cols; size = Math.min(colW - 14, d.size || 110); }
  function onScreenGood() { return tiles.some(t => !t.dead && d.test(t.it.key, st) === true); }
  function spawn(want) {
    const free = []; for (let c = 0; c < cols; c++) if (!tiles.some(t => t.col === c && !t.dead && t.y < size * 1.2)) free.push(c);
    if (!free.length) return false;
    let it = null; for (let k = 0; k < 20 && !it; k++) { const x = d.make(st, want); if (x && !tiles.some(t => !t.dead && t.it.key === x.key)) it = x; }
    if (!it) return false;
    const col = free[Math.floor(Math.random() * free.length)];
    const b = K.tile(it, { flat: true }); b.style.width = size + "px"; b.style.minHeight = Math.round(size * .62) + "px";
    const t = { it, col, y: -size, el: b, dead: false };
    b.addEventListener("pointerdown", e => { e.preventDefault(); hit(t); });
    b.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); hit(t); } });
    field.appendChild(b); tiles.push(t); place(t); return true;
  }
  function place(t) { const x = t.col * colW + (colW - size) / 2; const tr = `translate(${x}px,${t.y}px)`; t.el.style.transform = tr; t.el.style.setProperty("--t", tr); }
  function kill(t, cls) { t.dead = true; if (cls) { t.el.classList.add(cls); setTimeout(() => t.el.remove(), 300); } else t.el.remove(); }
  function hit(t) {
    if (!playing || paused || t.dead || R.over) return;
    const r = d.test(t.it.key, st);
    if (r === true) { kill(t, "pop"); st.found++; sinceGood = 0; if (d.onHit) d.onHit(st, t.it.key); setHead(); K.good(); }
    else { t.el.classList.add("wrongt"); kill(t, "pop"); K.bad(typeof r === "string" ? r : "That one doesn't fit."); }
  }
  function tick(ts) {
    raf = requestAnimationFrame(tick);
    const dt = Math.min(.05, (ts - (last || ts)) / 1000); last = ts;
    if (!playing || paused || R.over) return;
    sinceSpawn += dt; sinceGood += dt;
    const p = st.found / d.goal;
    const speed = Hh * (.085 + .17 * p) * speedMul, every = (1.25 - .55 * p) / Math.sqrt(speedMul);
    if (sinceSpawn >= every) { const want = !onScreenGood() && (sinceGood > 2.2 - p || Math.random() < .4) || Math.random() < .25; if (spawn(want)) sinceSpawn = 0; }
    for (const t of tiles) {
      if (t.dead) continue; t.y += speed * dt; place(t);
      if (t.y > Hh) { const was = d.test(t.it.key, st) === true; kill(t); if (was) { sinceGood = 0; K.bad(`Missed ${t.el._label}!`, { life: true }); if (R.over) break; } }
    }
    tiles = tiles.filter(t => !t.dead || t.el.isConnected);
  }
  startCard.querySelector("button").onclick = () => { startCard.remove(); measure(); playing = true; last = 0; K.start(); };
  const onResize = () => measure(); window.addEventListener("resize", onResize);
  measure(); raf = requestAnimationFrame(tick);
  return {
    stop() { cancelAnimationFrame(raf); window.removeEventListener("resize", onResize); playing = false; },
    pause() { if (playing && !R.over) { paused = true; R.paused = true; const o = el("div", "overlay"); o.style.position = "absolute"; o.innerHTML = `<div class="card center"><h2>Paused</h2><button class="new" type="button">Resume</button></div>`; field.appendChild(o); o.querySelector("button").onclick = () => { o.remove(); paused = false; R.paused = false; R.t0 = performance.now() - R.secs * 1000; last = 0; }; o.querySelector("button").focus(); } },
    hint() { const t = tiles.find(t => !t.dead && d.test(t.it.key, st) === true); t && K.hiTile(t.el); },
    keys(e) { if (e.key === "p" && playing) this.pause(); }
  };
};
})();
