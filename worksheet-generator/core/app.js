/* Teacher-facing app: configuration panel, live preview, regenerate, print.
   Works for any registered unit; the page names its unit with <body data-unit="...">. */
(function (G) {
  'use strict';
  var NS = G.MKWS, doc = G.document;
  var unit = NS.registry.units[doc.body.getAttribute('data-unit')];
  if (!unit) { doc.body.innerHTML = '<p style="padding:2rem">Unknown unit.</p>'; return; }

  var STORE = 'mkws:v1:' + unit.id;
  var DEFAULT_COUNT = 4;
  var DEFAULT_LESSONS = { 'lf-slope-two-points': 4, 'lf-graph-slope-intercept': 3, 'lf-write-two-points': 4, 'lf-identify-slope-intercept': 4 };

  function $(sel, root) { return (root || doc).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || doc).querySelectorAll(sel)); }
  function h(tag, attrs, html) {
    var e = doc.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { if (k === 'class') e.className = attrs[k]; else e.setAttribute(k, attrs[k]); });
    if (html !== undefined) e.innerHTML = html;
    return e;
  }
  var esc = NS.render.esc;

  /* ---------- state ---------- */
  var state = { settings: null, ws: null, view: 'student', ver: 0, zoom: 'fit', cache: {}, token: 0 };
  var lastCount = {};

  function load() {
    var s = NS.defaultSettings();
    s.lessons = JSON.parse(JSON.stringify(DEFAULT_LESSONS));
    try {
      var raw = G.localStorage.getItem(STORE);
      if (raw) {
        var o = JSON.parse(raw);
        Object.keys(o).forEach(function (k) { if (k in s) s[k] = o[k]; });
        Object.keys(s.lessons).forEach(function (id) { if (!NS.registry.lessons[id]) delete s.lessons[id]; });
      }
    } catch (e) { /* storage unavailable: fine */ }
    return s;
  }
  function save() { try { G.localStorage.setItem(STORE, JSON.stringify(state.settings)); } catch (e) { /* ignore */ } }

  /* ---------- configuration panel ---------- */
  function seg(name, label, options, current, hint) {
    var html = '<fieldset class="field"><legend>' + label + '</legend><div class="seg" role="radiogroup">';
    options.forEach(function (o, i) {
      var id = name + '-' + o.v;
      html += '<input type="radio" name="' + name + '" id="' + id + '" value="' + o.v + '"' + (String(o.v) === String(current) ? ' checked' : '') + '>' +
        '<label for="' + id + '">' + o.t + '</label>';
    });
    html += '</div>' + (hint ? '<p class="hint" id="hint-' + name + '"></p>' : '') + '</fieldset>';
    return html;
  }
  function check(id, label, checked, sub) {
    return '<label class="chk"><input type="checkbox" id="' + id + '"' + (checked ? ' checked' : '') + '><span>' + label + (sub ? '<small>' + sub + '</small>' : '') + '</span></label>';
  }

  function buildConfig() {
    var s = state.settings, cfg = $('#config');
    var html = '<section class="card" id="skills"><h2><span class="step">1</span> Choose skills</h2>' +
      '<p class="hint">Check the skills to include and set how many problems of each.</p>' +
      '<div class="bulk"><button type="button" class="btn ghost sm" id="selAll">Select all</button>' +
      '<button type="button" class="btn ghost sm" id="clrAll">Clear all</button>' +
      '<label class="setn">Set every checked skill to <input type="number" id="bulkN" min="1" max="20" value="' + DEFAULT_COUNT + '"> <button type="button" class="btn ghost sm" id="applyN">Apply</button></label></div>';
    unit.categories.forEach(function (cat) {
      html += '<fieldset class="cat" data-cat="' + cat.id + '"><legend>' + cat.letter + ' &middot; ' + esc(cat.name) + '</legend>' +
        '<div class="cat-tools"><button type="button" class="link" data-act="all">Select all</button><button type="button" class="link" data-act="none">Clear</button></div>';
      cat.lessons.forEach(function (id) {
        var L = NS.registry.lessons[id], n = s.lessons[id] | 0;
        html += '<div class="lrow' + (n ? ' on' : '') + '" data-id="' + id + '">' +
          '<label class="lcheck"><input type="checkbox"' + (n ? ' checked' : '') + '><span class="lnum">' + L.num + '</span><span class="ltitle">' + esc(L.title) + '</span></label>' +
          '<div class="count"><button type="button" class="step-btn" data-d="-1" aria-label="Fewer problems for skill ' + L.num + '">&minus;</button>' +
          '<input type="number" min="0" max="20" value="' + (n || '') + '" aria-label="Number of problems for skill ' + L.num + '"' + (n ? '' : ' disabled') + '>' +
          '<button type="button" class="step-btn" data-d="1" aria-label="More problems for skill ' + L.num + '">+</button></div></div>';
      });
      html += '</fieldset>';
    });
    html += '</section>';

    html += '<section class="card" id="options"><h2><span class="step">2</span> Worksheet options</h2>' +
      '<div class="field"><label for="optTitle" class="lbl">Worksheet title</label><input type="text" id="optTitle" maxlength="80" placeholder="' + esc(unit.defaultTitle) + '" value="' + esc(s.title) + '"></div>' +
      seg('difficulty', 'Difficulty', [{ v: 'basic', t: 'Basic' }, { v: 'standard', t: 'Standard' }, { v: 'honors', t: 'Honors' }], s.difficulty, true) +
      seg('numberMode', 'Numbers', [{ v: 'integers', t: 'Integers only' }, { v: 'preferred', t: 'Integers preferred' }, { v: 'fractions', t: 'Fractions allowed' }], s.numberMode, true) +
      seg('space', 'Workspace', [{ v: 'compact', t: 'Compact' }, { v: 'standard', t: 'Standard' }, { v: 'extended', t: 'Extended' }], s.space) +
      '<div class="field checks">' + check('optGrids', 'Include blank coordinate grids', s.grids, 'For graphing problems. Turn off if students use graph paper.') +
      check('optNameDate', 'Name / date line', s.showNameDate) + '</div>' +
      seg('versions', 'Versions', [{ v: 1, t: 'Single' }, { v: 2, t: 'A + B' }, { v: 3, t: 'A + B + C' }], s.versions, true) +
      '<div class="field checks">' + check('optKey', 'Include answer key', s.answerKey) + '</div>' +
      '<div id="keyModeWrap">' + seg('keyMode', 'Answer key shows', [{ v: 'answers', t: 'Final answers' }, { v: 'worked', t: 'Worked solutions' }], s.keyMode) + '</div>' +
      '</section>';
    cfg.innerHTML = html;
    syncHints();
    $('#keyModeWrap').hidden = !s.answerKey;
  }

  var HINTS = {
    difficulty: { basic: 'Smaller numbers, simpler slopes, mostly positive slopes.', standard: 'A balanced mix of positive and negative slopes.', honors: 'Larger numbers, more fractions in play, plus horizontal and vertical lines.' },
    numberMode: { integers: 'Slopes, intercepts and answers are whole numbers. (Perpendicular-line problems show a unit-fraction slope so the answer stays a whole number.)', preferred: 'Mostly whole numbers with an occasional fraction.', fractions: 'Fractions appear often; fractional intercepts appear at Standard and Honors.' },
    versions: { 1: 'One worksheet.', 2: 'Versions A and B: same skills and counts, different values.', 3: 'Versions A, B and C: same skills and counts, different values.' }
  };
  function syncHints() {
    Object.keys(HINTS).forEach(function (k) {
      var e = $('#hint-' + k); if (e) e.textContent = HINTS[k][state.settings[k]] || '';
    });
  }

  function setCount(id, n) {
    n = Math.max(0, Math.min(20, n | 0));
    state.settings.lessons[id] = n;
    if (!n) delete state.settings.lessons[id]; else lastCount[id] = n;
    var row = $('.lrow[data-id="' + id + '"]');
    row.classList.toggle('on', n > 0);
    $('input[type=checkbox]', row).checked = n > 0;
    var inp = $('input[type=number]', row); inp.disabled = !n; inp.value = n || '';
  }

  function wireConfig() {
    var cfg = $('#config');
    cfg.addEventListener('change', function (e) {
      var t = e.target;
      if (t.type === 'checkbox' && t.closest('.lrow')) {
        var id = t.closest('.lrow').getAttribute('data-id');
        setCount(id, t.checked ? (lastCount[id] || DEFAULT_COUNT) : 0); contentChanged();
      } else if (t.type === 'number' && t.closest('.lrow')) {
        setCount(t.closest('.lrow').getAttribute('data-id'), parseInt(t.value, 10) || 0); contentChanged();
      } else if (t.name === 'difficulty' || t.name === 'numberMode') { state.settings[t.name] = t.value; syncHints(); contentChanged(); }
      else if (t.name === 'versions') { state.settings.versions = +t.value; if (state.ver >= state.settings.versions) state.ver = 0; syncHints(); contentChanged(); }
      else if (t.name === 'space') { state.settings.space = t.value; layoutChanged(); }
      else if (t.name === 'keyMode') { state.settings.keyMode = t.value; layoutChanged(); }
      else if (t.id === 'optGrids') { state.settings.grids = t.checked; contentChanged(); }
      else if (t.id === 'optNameDate') { state.settings.showNameDate = t.checked; layoutChanged(); }
      else if (t.id === 'optKey') { state.settings.answerKey = t.checked; $('#keyModeWrap').hidden = !t.checked; if (!t.checked) state.view = 'student'; layoutChanged(); }
    });
    cfg.addEventListener('input', function (e) {
      if (e.target.id === 'optTitle') { state.settings.title = e.target.value; layoutChanged(true); }
    });
    cfg.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.classList.contains('step-btn')) {
        var row = b.closest('.lrow'), id = row.getAttribute('data-id'), cur = state.settings.lessons[id] | 0;
        setCount(id, cur + (+b.getAttribute('data-d')) || (b.getAttribute('data-d') === '1' ? 1 : 0)); contentChanged();
      } else if (b.getAttribute('data-act')) {
        var cat = b.closest('.cat'), all = b.getAttribute('data-act') === 'all';
        $$('.lrow', cat).forEach(function (r) { var id = r.getAttribute('data-id'); setCount(id, all ? (state.settings.lessons[id] || lastCount[id] || DEFAULT_COUNT) : 0); });
        contentChanged();
      } else if (b.id === 'selAll' || b.id === 'clrAll') {
        $$('.lrow').forEach(function (r) { var id = r.getAttribute('data-id'); setCount(id, b.id === 'selAll' ? (state.settings.lessons[id] || lastCount[id] || DEFAULT_COUNT) : 0); });
        contentChanged();
      } else if (b.id === 'applyN') {
        var n = Math.max(1, Math.min(20, parseInt($('#bulkN').value, 10) || DEFAULT_COUNT));
        Object.keys(state.settings.lessons).forEach(function (id) { setCount(id, n); }); contentChanged();
      }
    });
  }

  /* ---------- building and showing the worksheet ---------- */
  var timer = null;
  function schedule(fn, ms) { G.clearTimeout(timer); timer = G.setTimeout(fn, ms); }
  function contentChanged() { save(); schedule(rebuild, 220); setStatus('Updating…'); }
  function layoutChanged(debounce) { save(); state.cache = {}; if (debounce) schedule(render, 200); else render(); }

  function rebuild() {
    state.cache = {};
    var plan = NS.orderedLessons(state.settings, unit.id);
    if (!plan.length) { state.ws = null; render(); return; }
    state.ws = NS.buildWorksheet(state.settings, unit.id);
    render();
  }
  function newProblems() {
    state.settings.seed = Math.floor(Math.random() * 1e9); state.settings.salts = {}; state.settings.pinned = null; save();
    rebuild();
  }

  function setStatus(t) { $('#status').textContent = t; }

  function infoFor(ver, kind) {
    var s = state.settings, title = (s.title && s.title.trim()) || unit.defaultTitle;
    return {
      footer: 'Mr. K’s Classroom · ' + unit.course + ' · ' + unit.name,
      runLeft: title + (kind === 'key' ? ' — Answer Key' : ''),
      runRight: (s.versions > 1 ? 'Version ' + ver.label + ' · ' : '') + (kind === 'key' ? 'Teacher copy' : 'Name: ____________________')
    };
  }

  function getPages(vIdx, view) {
    var key = vIdx + ':' + view;
    if (state.cache[key]) return Promise.resolve(state.cache[key]);
    var ver = state.ws.versions[vIdx];
    var units = view === 'key' ? NS.render.keyUnits(ver, state.settings, unit) : NS.render.studentUnits(ver, state.settings, unit);
    return NS.render.paginate(units, infoFor(ver, view)).then(function (pages) { state.cache[key] = pages; return pages; });
  }

  function applyZoom() {
    var wrap = $('#pagesWrap'), pagesEl = $('#pages');
    var z = state.zoom === 'fit' ? Math.min(1.25, Math.max(0.3, (wrap.clientWidth - 28) / 816)) : parseFloat(state.zoom);
    pagesEl.style.setProperty('--z', z);
    pagesEl.style.zoom = z;
  }

  function render() {
    var s = state.settings, token = ++state.token;
    var empty = $('#empty'), pagesEl = $('#pages');
    // toolbar state
    $('#viewKey').hidden = !s.answerKey; $('#btnPrintKey').hidden = !s.answerKey;
    $('#viewStudent').setAttribute('aria-pressed', state.view === 'student'); $('#viewKey').setAttribute('aria-pressed', state.view === 'key');
    var vt = $('#verTabs'); vt.hidden = s.versions < 2;
    vt.innerHTML = '';
    for (var i = 0; i < s.versions; i++) {
      var b = h('button', { type: 'button', 'class': 'tab', 'data-v': i, 'aria-pressed': String(state.ver === i) }, 'Version ' + 'ABC'[i]);
      vt.appendChild(b);
    }
    $('#btnPrintAll').hidden = s.versions < 2;
    if (!state.ws) {
      pagesEl.innerHTML = ''; empty.hidden = false; setStatus('No skills selected'); setBusy(false);
      ['btnPrint', 'btnPrintAll', 'btnPrintKey', 'btnNew'].forEach(function (id) { $('#' + id).disabled = true; });
      return;
    }
    ['btnPrint', 'btnPrintAll', 'btnPrintKey', 'btnNew'].forEach(function (id) { $('#' + id).disabled = false; });
    empty.hidden = true; setBusy(true);
    var vIdx = Math.min(state.ver, state.ws.versions.length - 1), view = state.view;
    getPages(vIdx, view).then(function (pages) {
      if (token !== state.token) return;
      pagesEl.innerHTML = '';
      pages.forEach(function (p) { pagesEl.appendChild(p); });
      applyZoom(); setBusy(false);
      var n = NS.countProblems(state.ws.versions[vIdx]);
      setStatus(n + ' problem' + (n === 1 ? '' : 's') + ' · ' + pages.length + ' page' + (pages.length === 1 ? '' : 's') + (s.versions > 1 ? ' · Version ' + 'ABC'[vIdx] : '') + (view === 'key' ? ' · answer key' : ''));
    });
  }
  function setBusy(b) { $('#preview').classList.toggle('busy', !!b); }

  /* ---------- preview toolbar ---------- */
  function wirePreview() {
    $('#viewStudent').addEventListener('click', function () { state.view = 'student'; render(); });
    $('#viewKey').addEventListener('click', function () { state.view = 'key'; render(); });
    $('#verTabs').addEventListener('click', function (e) { var b = e.target.closest('button[data-v]'); if (b) { state.ver = +b.getAttribute('data-v'); render(); } });
    $('#zoom').addEventListener('change', function (e) { state.zoom = e.target.value; applyZoom(); });
    G.addEventListener('resize', function () { if (state.zoom === 'fit') applyZoom(); });
    $('#btnNew').addEventListener('click', newProblems);
    $('#btnPrint').addEventListener('click', function () { printSet(false, state.view); });
    $('#btnPrintAll').addEventListener('click', function () { printSet(true, state.view); });
    $('#btnPrintKey').addEventListener('click', function () { printSet(false, 'key'); });
    $('#pages').addEventListener('click', function (e) {
      var b = e.target.closest('.regen'); if (!b) return;
      var blk = b.closest('[data-s]'); var si = +blk.getAttribute('data-s'), pi = +blk.getAttribute('data-p');
      var y = G.scrollY;
      NS.regenerateProblem(state.ws, state.ver, si, pi);
      state.settings.pinned = state.ws.settings.pinned; save();
      delete state.cache[state.ver + ':student']; delete state.cache[state.ver + ':key'];
      render(); G.setTimeout(function () { G.scrollTo(0, y); }, 60);
    });
    $('#pages').addEventListener('click', function (e) {
      // in the answer key, a click on the number regenerates nothing; keep keys read-only
    });
  }

  /* ---------- printing ---------- */
  function printSet(all, view) {
    if (!state.ws) return;
    var vers = all ? state.ws.versions.map(function (v, i) { return i; }) : [Math.min(state.ver, state.ws.versions.length - 1)];
    setStatus('Preparing pages…'); setBusy(true);
    var chain = Promise.resolve([]);
    vers.forEach(function (v) { chain = chain.then(function (acc) { return getPages(v, view).then(function (pages) { return acc.concat(pages); }); }); });
    chain.then(function (pages) {
      var root = $('#printRoot'); root.innerHTML = '';
      pages.forEach(function (p) { root.appendChild(p.cloneNode(true)); });
      var old = doc.title, s = state.settings, title = (s.title && s.title.trim()) || unit.defaultTitle;
      doc.title = title + (view === 'key' ? ' - Answer Key' : '') + (all ? ' - All Versions' : s.versions > 1 ? ' - Version ' + 'ABC'[vers[0]] : '');
      doc.body.classList.add('printing');
      function done() { doc.body.classList.remove('printing'); root.innerHTML = ''; doc.title = old; setBusy(false); render(); G.removeEventListener('afterprint', done); }
      G.addEventListener('afterprint', done);
      G.setTimeout(function () { G.print(); }, 80);
    });
  }

  /* ---------- start ---------- */
  function init() {
    state.settings = load();
    $('#unitName').textContent = unit.course + ' · ' + unit.name;
    buildConfig(); wireConfig(); wirePreview();
    var theme = $('#themeBtn');
    if (theme) theme.addEventListener('click', function () {
      var r = doc.documentElement, dark = r.getAttribute('data-theme') === 'dark' || (!r.getAttribute('data-theme') && G.matchMedia('(prefers-color-scheme: dark)').matches);
      r.setAttribute('data-theme', dark ? 'light' : 'dark');
    });
    rebuild();
  }
  NS.app = { state: state, rebuild: rebuild, render: render, getPages: getPages };
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', init); else init();
})(typeof window !== 'undefined' ? window : globalThis);
