/* Menu Assessment Generator — teacher interface.
   Steps: 1 course & unit · 2 class level · 3 menu & rules · 4 skills · 5 build · 6 review & edit
          7 preview · 8 print & save.
   All state lives in this browser (autosaved to localStorage) and can be exported as a file. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, WS = G.MKWS, doc = G.document;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var mathSafe = NS.mathSafe;

  var KEY_CUR = 'mk-menu-current-v1', KEY_SAVES = 'mk-menu-saves-v1', KEY_THEME = 'mkws-theme', KEY_LAST = 'mk-menu-last-unit';
  /* Each unit keeps its own autosave, so switching units never loses work. */
  function curKey(unit) { return KEY_CUR + ':' + unit; }
  function hashUnit() { var m = /unit=([a-z0-9\-]+)/.exec(G.location.hash || ''); return m && NS.skillSets[m[1]] ? m[1] : null; }
  var defaultUnit = doc.body.getAttribute('data-unit') || 'algebra1-expressions-equations';
  var ui = { view: 'setup', version: 0, preview: 'student', showAns: {}, zoom: 'fit', bankSkill: null, bankC: null, bankN: 10, bankOpen: false };
  var draft = null, S = null, undoStack = [];

  /* ---------------- storage ---------------- */
  function lsGet(k) { try { return G.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { G.localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function cfg() { return S ? S.config : draft; }
  function isTest() { return NS.isTest(cfg()); }
  function noun() { return isTest() ? 'test' : 'menu'; }
  function autosave() {
    var unit = cfg().unitId;
    var ok = lsSet(curKey(unit), S ? NS.serialize(S) : JSON.stringify({ draft: draft })); lsSet(KEY_LAST, unit);
    var el = $('#mmSaveState'); if (el) el.textContent = ok ? 'Saved in this browser' : 'Could not save in this browser — download a file to keep your work';
  }
  function snapshot() { undoStack.push(S ? NS.serialize(S) : JSON.stringify({ draft: draft })); if (undoStack.length > 30) undoStack.shift(); $('#mmUndo').disabled = false; }
  function undo() {
    var last = undoStack.pop(); if (!last) return;
    var o = JSON.parse(last);
    if (o.draft) { draft = o.draft; S = null; } else { S = NS.deserialize(o); draft = null; }
    $('#mmUndo').disabled = !undoStack.length; toast('Undone.'); render(); autosave();
  }
  /* Run a change: snapshot first so it can be undone, then re-render and autosave. */
  function change(fn, msg) {
    snapshot();
    var r; try { r = fn(); if (S) NS.ensureFormats(S); } catch (e) { console.error(e); toast('Something went wrong: ' + e.message); }
    render(); autosave(); if (msg) toast(typeof msg === 'function' ? msg(r) : msg);
    return r;
  }

  /* ---------------- toast ---------------- */
  var toastTimer = null;
  function toast(msg, action) {
    var t = $('#mmToast'); t.innerHTML = esc(msg) + (action ? ' <button type="button" class="btn sm ghost" id="mmToastAct">' + esc(action.label) + '</button>' : '');
    t.hidden = false; clearTimeout(toastTimer);
    if (action) $('#mmToastAct').onclick = function () { t.hidden = true; action.fn(); };
    toastTimer = setTimeout(function () { t.hidden = true; }, action ? 9000 : 3500);
  }

  /* ---------------- top: steps + summary ---------------- */
  var STEPS = [['setup', '1', 'Course & unit', 'mmUnit'], ['setup', '2', 'Class level', 'mmLevel'], ['setup', '3', 'Menu & rules', 'mmMenu'], ['setup', '4', 'Skills', 'mmSkills'],
    ['setup', '5', 'Build', 'mmBuild'], ['review', '6', 'Review & edit', null], ['preview', '7', 'Preview', null], ['export', '8', 'Print & save', null]];
  function renderSteps() {
    $('.mm-stepnav').innerHTML = STEPS.map(function (s, i) {
      var dis = !S && i >= 5; if (i === 2 && isTest()) s = [s[0], s[1], 'Test parts', s[3]];
      var cur = ui.view === s[0] && (s[0] !== 'setup' || i === 0);
      return '<button type="button" class="mm-stepbtn' + (ui.view === s[0] ? ' on' : '') + '" data-step="' + i + '"' + (dis ? ' disabled' : '') + (cur ? ' aria-current="step"' : '') + '><span class="step">' + s[1] + '</span>' + esc(s[2]) + '</button>';
    }).join('');
    $$('.mm-stepbtn').forEach(function (b) { b.onclick = function () {
      var s = STEPS[+b.getAttribute('data-step')]; ui.view = s[0]; render();
      if (s[3]) { var t = doc.getElementById(s[3]); if (t) { t.scrollIntoView({ behavior: 'smooth', block: 'start' }); var f = t.querySelector('h2'); if (f) { f.setAttribute('tabindex', '-1'); f.focus({ preventScroll: true }); } } }
    }; });
  }
  function renderSummary() {
    var c = cfg(), rules = NS.checkRules(c, S), box = $('#mmSummary');
    var bits = [];
    if (NS.isTest(c)) bits.push('<span><b>' + rules.totalOffered + '</b> questions</span>');
    else { bits.push('<span><b>' + rules.totalOffered + '</b> offered</span>'); bits.push('<span><b>' + rules.totalRequired + '</b> students complete</span>'); }
    bits.push('<span><b>' + rules.maxScore + '</b> points possible</span>');
    if (S) {
      var cnt = NS.counts(S);
      bits.push('<span>' + S.versions.length + (S.versions.length > 1 ? ' versions' : ' version') + '</span>');
      if (cnt.failed) bits.push('<span class="bad">' + cnt.failed + ' missing</span>');
      if (cnt.unverified) bits.push('<span class="warn">' + cnt.unverified + ' need approval</span>');
      if (!cnt.failed && !cnt.unverified) bits.push('<span class="ok">✓ every answer verified</span>');
    }
    if (rules.errors.length) bits.push('<span class="bad">' + rules.errors.length + ' rule problem' + (rules.errors.length > 1 ? 's' : '') + '</span>');
    box.innerHTML = bits.join('');
  }

  /* ---------------- SETUP (steps 1–5) ---------------- */
  function unitOptions(sel) {
    return NS.CATALOG.map(function (g) {
      return '<optgroup label="' + esc(g.course) + '">' + g.units.map(function (u) {
        var ok = !!NS.skillSets[u[0]];
        return '<option value="' + u[0] + '"' + (u[0] === sel ? ' selected' : '') + (ok ? '' : ' disabled') + '>' + esc(u[1]) + (ok ? '' : ' — not yet supported') + '</option>';
      }).join('') + '</optgroup>';
    }).join('');
  }
  function viewSetup() {
    var c = cfg(), set = NS.skillSets[c.unitId], rules = NS.checkRules(c, S);
    var h = '';
    // 1
    h += '<section class="card mm-card" id="mmUnit"><h2><span class="step">1</span>Course and unit</h2>' +
      '<label class="field"><span class="lbl">Unit</span><select id="mmUnitSel">' + unitOptions(c.unitId) + '</select></label>' +
      '<p class="hint">Available now: <b>' + Object.keys(NS.skillSets).filter(function (k) { return NS.skillSets[k].courseName; }).map(function (k) { return esc(NS.skillSets[k].courseName + ' · ' + NS.skillSets[k].unitName); }).join('</b>, <b>') + '</b>. Other units are listed so you can see what is planned; each one is added only after its problem generators pass the same verification tests. The ready-to-print Assessment Menu PDFs for every unit are still on each unit page.</p>' +
      '<fieldset class="field mm-mode"><legend class="lbl">Format</legend>' +
      '<label class="chk"><input type="radio" name="mmMode" value="menu"' + (NS.isTest(c) ? '' : ' checked') + '><span>Choice menu<small>Students choose problems from Appetizers, Entrées and Chef’s Specials.</small></span></label>' +
      '<label class="chk"><input type="radio" name="mmMode" value="test"' + (NS.isTest(c) ? ' checked' : '') + '><span>Standard test<small>Everyone answers every question: multiple-choice and short-answer parts, easier to harder.</small></span></label></fieldset>' +
      '<label class="field"><span class="lbl">' + (NS.isTest(c) ? 'Test' : 'Menu') + ' title</span><input type="text" id="mmTitle" value="' + esc(c.title) + '" maxlength="80"></label>' +
      '<label class="field"><span class="lbl">Subtitle</span><input type="text" id="mmSubtitle" value="' + esc(c.subtitle) + '" maxlength="120"></label></section>';
    // 2
    h += '<section class="card mm-card" id="mmLevel"><h2><span class="step">2</span>Class level</h2><div class="mm-levels" role="radiogroup" aria-label="Class level">' +
      Object.keys(NS.LEVELS).map(function (k) { var L = NS.LEVELS[k];
        return '<label class="mm-level' + (c.level === k ? ' on' : '') + '"><input type="radio" name="mmLevel" value="' + k + '"' + (c.level === k ? ' checked' : '') + '><b>' + esc(L.long) + '</b><small>' + esc(L.about) + '</small><small class="mm-tiers">Difficulty by section: ' + L.tiers.map(function (t) { return t + ' ' + NS.DIFF_NAMES[t]; }).join(' → ') + '</small></label>';
      }).join('') + '</div>' +
      '<label class="field"><span class="lbl">Answers</span><select id="mmAnswers">' +
      [['auto', 'Match the level (whole numbers for CP2/CP1, fractions allowed for Honors)'], ['integers', 'Whole-number answers only'], ['fractions', 'Allow fraction answers']].map(function (o) { return '<option value="' + o[0] + '"' + (c.answers === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label></section>';
    // 3
    if (NS.isTest(c)) h += testPartsHtml(c, rules); else
    h += '<section class="card mm-card" id="mmMenu"><h2><span class="step">3</span>Menu sections and rules</h2>' +
      '<div class="mm-presets"><span class="lbl">Start from:</span> <button type="button" class="btn ghost sm" data-preset="std">Standard menu (100 pts)</button> <button type="button" class="btn ghost sm" data-preset="quiz">Short quiz</button> <button type="button" class="btn ghost sm" data-preset="big">Unit test</button></div>' +
      '<div class="mm-tablewrap"><table class="mm-sectbl"><thead><tr><th>Section name</th><th>Points each</th><th>Offered</th><th>Students complete</th><th>Difficulty</th><th>Skills</th><th><span class="sr">Remove</span></th></tr></thead><tbody>' +
      c.sections.map(function (s, si) {
        var sc = NS.sectionC(c, si), skillsTxt = s.skills && s.skills.length ? s.skills.length + ' chosen' : 'All selected';
        return '<tr data-si="' + si + '"><td><input type="text" class="mmSecName" value="' + esc(s.name) + '" aria-label="Section ' + (si + 1) + ' name" maxlength="40"><input type="text" class="mmSecNote" value="' + esc(s.note || '') + '" aria-label="Section ' + (si + 1) + ' note" placeholder="Note (optional)" maxlength="60"></td>' +
          '<td><input type="number" class="mmSecPts" min="0.5" step="0.5" value="' + s.points + '" aria-label="' + esc(s.name) + ' points each"></td>' +
          '<td><input type="number" class="mmSecOff" min="1" max="20" value="' + s.offered + '" aria-label="' + esc(s.name) + ' problems offered"></td>' +
          '<td><input type="number" class="mmSecReq" min="0" max="20" value="' + s.required + '" aria-label="' + esc(s.name) + ' problems students complete"></td>' +
          '<td><select class="mmSecTier" aria-label="' + esc(s.name) + ' difficulty">' + [0, 1, 2].map(function (t) { return '<option value="' + t + '"' + ((s.tier === undefined ? Math.min(si, 2) : s.tier) === t ? ' selected' : '') + '>' + ['Appetizer level', 'Entrée level', 'Chef’s Special level'][t] + '</option>'; }).join('') + '</select>' +
          '<span class="mm-adj"><button type="button" class="step-btn mmAdj" data-d="-1" aria-label="Make ' + esc(s.name) + ' easier">−</button><span class="mm-cval" title="Difficulty ' + sc + ' of 7">' + sc + ' · ' + NS.DIFF_NAMES[sc] + '</span><button type="button" class="step-btn mmAdj" data-d="1" aria-label="Make ' + esc(s.name) + ' harder">+</button></span></td>' +
          '<td><button type="button" class="btn ghost sm mmSecSkills">' + skillsTxt + '</button></td>' +
          '<td><button type="button" class="btn ghost sm mmSecDel" aria-label="Remove section ' + esc(s.name) + '"' + (c.sections.length < 2 ? ' disabled' : '') + '>✕</button></td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<p><button type="button" class="btn ghost sm" id="mmAddSec">+ Add a section</button></p>' +
      '<label class="chk"><input type="checkbox" id="mmCov"' + (c.coverage.on ? ' checked' : '') + '><span>Students must choose at least one problem from each skill category<small>Categories: ' + esc(Object.keys(set.tags).join(', ')) + '</small></span></label>' +
      (c.coverage.on ? '<div class="mm-covtags">' + Object.keys(set.tags).map(function (t) {
        var on = !c.coverage.tags || c.coverage.tags.indexOf(t) >= 0;
        return '<label class="mm-tagchk"><input type="checkbox" class="mmCovTag" value="' + t + '"' + (on ? ' checked' : '') + '>' + esc(t) + '</label>';
      }).join('') + '<small class="hint">Leave all checked to require every category that appears on the menu.</small></div>' : '') +
      rulesHtml(rules) + '</section>';
    // 4
    h += '<section class="card mm-card" id="mmSkills"><h2><span class="step">4</span>Skills and topics</h2><p class="hint">Uncheck a skill to leave it off the ' + noun() + '. Each skill gets harder with the difficulty number (1–7); the examples show what changes.</p>' +
      Object.keys(set.tags).map(function (t) {
        var list = set.skills.filter(function (s) { return s.tag === t; });
        return '<fieldset class="mm-skillgrp"><legend><span class="mm-chip">' + esc(t) + '</span> ' + esc(set.tags[t]) + '</legend>' + list.map(function (s) {
          return '<label class="chk"><input type="checkbox" class="mmSkill" value="' + s.id + '"' + (c.skills[s.id] ? ' checked' : '') + '><span>' + esc(s.name) + '<small>' + esc(s.blurb) + '</small></span><button type="button" class="link mmSample" data-skill="' + s.id + '">Sample</button></label>';
        }).join('') + '</fieldset>';
      }).join('') +
      '<div class="mm-gaps"><b>Not generated yet in this unit:</b><ul>' + set.gaps.map(function (g) { return '<li>' + esc(g) + '</li>'; }).join('') + '</ul></div></section>';
    // 5
    h += '<section class="card mm-card" id="mmBuild"><h2><span class="step">5</span>Build the ' + noun() + '</h2>' +
      '<label class="field"><span class="lbl">Versions</span><select id="mmVersions">' + [1, 2, 3].map(function (n) { return '<option value="' + n + '"' + ((c.versions | 0) === n ? ' selected' : '') + '>' + ['Version A only', 'Versions A and B', 'Versions A, B and C'][n - 1] + '</option>'; }).join('') + '</select></label>' +
      '<p class="hint">Versions share the same skills, difficulty and layout, with different numbers' + (isTest() ? ' (multiple-choice letters are reshuffled).' : '.') + '</p>' +
      (S ? '<p><button type="button" class="btn" id="mmGoReview">Review my ' + noun() + ' →</button> <button type="button" class="btn ghost" id="mmRebuild">Rebuild with these settings</button></p><p class="hint">Rebuilding keeps every pinned or edited problem and replaces the rest.</p>'
         : '<p><button type="button" class="btn" id="mmBuildBtn"' + (rules.errors.length ? ' disabled' : '') + '>Build my ' + noun() + '</button></p>' + (rules.errors.length ? '<p class="hint bad">Fix the rule problems in step 3 first.</p>' : '')) +
      '</section>';
    return h;
  }
  /* Step 3 for a standard test: parts with a question format; everyone answers every question. */
  var TIERS_TEST = [['ramp', 'Easier → harder'], [0, 'Easier'], [1, 'Middle'], [2, 'Harder']];
  function testPartsHtml(c, rules) {
    return '<section class="card mm-card" id="mmMenu"><h2><span class="step">3</span>Test parts</h2>' +
      '<div class="mm-presets"><span class="lbl">Start from:</span> ' + [['std', 'Standard test (100 pts)'], ['quiz', 'Short quiz (50 pts)'], ['mc', 'All multiple choice'], ['open', 'All short answer']].map(function (x) { return '<button type="button" class="btn ghost sm" data-tpreset="' + x[0] + '">' + x[1] + '</button>'; }).join(' ') + '</div>' +
      '<div class="mm-tablewrap"><table class="mm-sectbl"><thead><tr><th>Part name</th><th>Points each</th><th>Questions</th><th>Question format</th><th>Difficulty</th><th>Skills</th><th><span class="sr">Remove</span></th></tr></thead><tbody>' +
      c.sections.map(function (s, si) {
        var skillsTxt = s.skills && s.skills.length ? s.skills.length + ' chosen' : 'All selected', tierV = s.tier === undefined ? 'ramp' : s.tier, cs = [0, 1, 2].map(function (k) { return NS.itemC(c, si, k, 3); });
        var cTxt = tierV === 'ramp' ? cs[0] + '–' + cs[2] : String(NS.sectionC(c, si));
        return '<tr data-si="' + si + '"><td><input type="text" class="mmSecName" value="' + esc(s.name) + '" aria-label="Part ' + (si + 1) + ' name" maxlength="40"><input type="text" class="mmSecNote" value="' + esc(s.note || '') + '" aria-label="Part ' + (si + 1) + ' directions" placeholder="Directions (optional)" maxlength="60"></td>' +
          '<td><input type="number" class="mmSecPts" min="0.5" step="0.5" value="' + s.points + '" aria-label="' + esc(s.name) + ' points each"></td>' +
          '<td><input type="number" class="mmSecOff" min="1" max="30" value="' + s.offered + '" aria-label="' + esc(s.name) + ' number of questions"></td>' +
          '<td><select class="mmSecFmt" aria-label="' + esc(s.name) + ' question format">' + Object.keys(NS.FORMATS).map(function (k) { return '<option value="' + k + '"' + ((s.qformat || 'open') === k ? ' selected' : '') + '>' + esc(NS.FORMATS[k]) + '</option>'; }).join('') + '</select></td>' +
          '<td><select class="mmSecTier" aria-label="' + esc(s.name) + ' difficulty">' + TIERS_TEST.map(function (t) { return '<option value="' + t[0] + '"' + (String(tierV) === String(t[0]) ? ' selected' : '') + '>' + t[1] + '</option>'; }).join('') + '</select>' +
          '<span class="mm-adj"><button type="button" class="step-btn mmAdj" data-d="-1" aria-label="Make ' + esc(s.name) + ' easier">−</button><span class="mm-cval" title="Difficulty (1 to 7)">' + cTxt + '</span><button type="button" class="step-btn mmAdj" data-d="1" aria-label="Make ' + esc(s.name) + ' harder">+</button></span></td>' +
          '<td><button type="button" class="btn ghost sm mmSecSkills">' + skillsTxt + '</button></td>' +
          '<td><button type="button" class="btn ghost sm mmSecDel" aria-label="Remove part ' + esc(s.name) + '"' + (c.sections.length < 2 ? ' disabled' : '') + '>✕</button></td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<p><button type="button" class="btn ghost sm" id="mmAddSec">+ Add a part</button></p>' +
      '<p class="hint">Every student answers every question. Within each part the questions go from easier to harder inside the class level, unless you choose one difficulty. Multiple-choice answers are checked: the right answer is verified and every wrong choice is a checked mistake.</p>' +
      rulesHtml(rules) + '</section>';
  }
  function rulesHtml(rules) {
    return '<div class="mm-rules" aria-live="polite"><div class="mm-max">Maximum score: <b>' + rules.maxScore + '</b> points · ' + (isTest() ? '<b>' + rules.totalOffered + '</b> questions' : 'students complete <b>' + rules.totalRequired + '</b> of <b>' + rules.totalOffered + '</b>') + '</div>' +
      rules.errors.map(function (e) { return '<p class="mm-err">✕ ' + esc(e) + '</p>'; }).join('') +
      rules.warnings.map(function (w) { return '<p class="mm-warn">! ' + esc(w) + '</p>'; }).join('') + '</div>';
  }
  var PRESETS = {
    std: [['Appetizers', 'Warm-ups', 5, 6, 4, 0], ['Entrées', 'Multi-step problems', 10, 6, 4, 1], ['Chef’s Specials', 'Multi-part challenges', 20, 3, 2, 2]],
    quiz: [['Appetizers', 'Warm-ups', 5, 4, 2, 0], ['Entrées', 'Multi-step problems', 10, 4, 2, 1]],
    big: [['Appetizers', 'Warm-ups', 4, 8, 5, 0], ['Entrées', 'Multi-step problems', 8, 8, 5, 1], ['Chef’s Specials', 'Multi-part challenges', 15, 4, 2, 2], ['Dessert', 'Bonus · optional', 5, 2, 1, 2]]
  };
  function bindSetup() {
    var c = cfg();
    function upd(fn, rerender) { return function (e) { if (S) snapshot(); fn(e); afterConfigChange(rerender); }; }
    $('#mmUnitSel').onchange = function (e) { var id = e.target.value; if (!NS.skillSets[id]) return; snapshot(); autosave(); loadUnit(id, c.level); try { G.history.replaceState(null, '', '#unit=' + id); } catch (er) { /* ignore */ } render(); autosave(); };
    $$('input[name=mmMode]').forEach(function (r) { r.onchange = function () {
      if (S) { change(function () { NS.setMode(S.config, r.value); S.versions.forEach(function (v) { v.sections = []; }); NS.syncStructure(S); }, r.value === 'test' ? 'Switched to a standard test. New questions were made for the test parts.' : 'Switched to a choice menu. New problems were made for the menu sections.'); }
      else { NS.setMode(draft, r.value); autosave(); render(); }
    }; });
    $('#mmTitle').oninput = function (e) { c.title = e.target.value; autosave(); };
    $('#mmSubtitle').oninput = function (e) { c.subtitle = e.target.value; autosave(); };
    $$('input[name=mmLevel]').forEach(function (r) { r.onchange = upd(function () { c.level = r.value; if (S) levelChanged(); }, true); });
    $('#mmAnswers').onchange = upd(function (e) { c.answers = e.target.value; if (S) levelChanged(); }, true);
    $$('[data-tpreset]').forEach(function (b) { b.onclick = upd(function () {
      c.sections = NS.testSections(b.getAttribute('data-tpreset'));
      if (S) { S.versions.forEach(function (v) { v.sections = []; }); NS.syncStructure(S); }
    }, true); });
    $$('[data-preset]').forEach(function (b) { b.onclick = upd(function () {
      c.sections = PRESETS[b.getAttribute('data-preset')].map(function (p, i) { return { id: NS.uid('sec'), name: p[0], note: p[1], points: p[2], offered: p[3], required: p[4], tier: p[5], adjust: 0, skills: null }; });
      if (S) { S.versions.forEach(function (v) { v.sections = []; }); NS.syncStructure(S); }
    }, true); });
    $$('.mm-sectbl tbody tr').forEach(function (tr) {
      var si = +tr.getAttribute('data-si'), s = c.sections[si];
      $('.mmSecName', tr).onchange = upd(function (e) { s.name = e.target.value.trim() || 'Section ' + (si + 1); }, true);
      $('.mmSecNote', tr).onchange = upd(function (e) { s.note = e.target.value; }, false);
      $('.mmSecPts', tr).onchange = upd(function (e) { var v = Math.round(parseFloat(e.target.value) * 2) / 2; s.points = v > 0 ? v : s.points; }, true);
      $('.mmSecOff', tr).onchange = upd(function (e) { var v = Math.max(1, Math.min(20, parseInt(e.target.value, 10) || 1)); s.offered = v; if (S) NS.syncStructure(S); }, true);
      if ($('.mmSecReq', tr)) $('.mmSecReq', tr).onchange = upd(function (e) { var v = Math.max(0, Math.min(20, parseInt(e.target.value, 10) || 0)); s.required = v; }, true);
      if ($('.mmSecFmt', tr)) $('.mmSecFmt', tr).onchange = upd(function (e) { s.qformat = e.target.value; if (S) { NS.rebuild(S); NS.ensureFormats(S); } }, true);
      $('.mmSecTier', tr).onchange = upd(function (e) { s.tier = e.target.value === 'ramp' ? 'ramp' : +e.target.value; if (S) sectionDifficultyChanged(si); }, true);
      $$('.mmAdj', tr).forEach(function (b) { b.onclick = upd(function () { var d = +b.getAttribute('data-d'), sig = function () { return [0, 1, 2].map(function (k) { return NS.itemC(c, si, k, 3); }).join(',') + NS.sectionC(c, si); }, before = sig(); s.adjust = (s.adjust || 0) + d; if (sig() === before) s.adjust -= d; if (S) sectionDifficultyChanged(si); }, true); });
      $('.mmSecSkills', tr).onclick = function () { sectionSkillsDialog(si); };
      $('.mmSecDel', tr).onclick = upd(function () { c.sections.splice(si, 1); if (S) S.versions.forEach(function (v) { v.sections.splice(si, 1); }); }, true);
    });
    $('#mmAddSec').onclick = upd(function () { c.sections.push(NS.isTest(c) ? { id: NS.uid('sec'), name: 'Part ' + (c.sections.length + 1), note: 'Show your work.', points: 10, offered: 3, required: 3, tier: 'ramp', adjust: 0, skills: null, qformat: 'open' } : { id: NS.uid('sec'), name: 'Dessert', note: 'Bonus', points: 5, offered: 2, required: 1, tier: 2, adjust: 0, skills: null }); if (S) NS.syncStructure(S); }, true);
    if ($('#mmCov')) $('#mmCov').onchange = upd(function (e) { c.coverage.on = e.target.checked; }, true);
    $$('.mmCovTag').forEach(function (b) { b.onchange = upd(function () {
      var on = $$('.mmCovTag').filter(function (x) { return x.checked; }).map(function (x) { return x.value; });
      c.coverage.tags = on.length === $$('.mmCovTag').length ? null : on;
    }, true); });
    $$('.mmSkill').forEach(function (b) { b.onchange = upd(function () { c.skills[b.value] = b.checked; }, true); });
    $$('.mmSample').forEach(function (b) { b.onclick = function (e) { e.preventDefault(); sampleDialog(b.getAttribute('data-skill')); }; });
    $('#mmVersions').onchange = upd(function (e) { c.versions = +e.target.value; if (S) NS.syncStructure(S); }, true);
    if ($('#mmBuildBtn')) $('#mmBuildBtn').onclick = function () { build(); };
    if ($('#mmGoReview')) $('#mmGoReview').onclick = function () { ui.view = 'review'; render(); };
    if ($('#mmRebuild')) $('#mmRebuild').onclick = function () {
      change(function () { return NS.rebuild(S); }, function (r) { return 'Rebuilt ' + r.rebuilt + ' problems; kept ' + r.kept + ' pinned or edited.'; });
      ui.view = 'review'; render();
    };
  }
  function afterConfigChange(rerender) {
    autosave();
    if (rerender) { var y = G.scrollY; render(); G.scrollTo(0, y); } else { renderSummary(); }
  }
  /* Level changed after building: move every unpinned, unedited slot to its section's new difficulty. */
  function levelChanged() { S.config.sections.forEach(function (s, si) { sectionDifficultyChanged(si); }); }
  function sectionDifficultyChanged(si) {
    var c = S.config, all = S.versions[0].sections[si].items.slice();
    all.forEach(function (a, i) {
      var target = NS.itemC(c, si, i, all.length);
      var locked = S.versions.some(function (v) { return v.sections[si].items.some(function (it) { return it.slot === a.slot && (it.pinned || it.edited || it.manual); }); });
      if (!locked && a.c !== target) NS.setDifficulty(S, 0, a.uid, target);
    });
    S.versions.forEach(function (v) { v.sections[si].items.forEach(function (it) { if (!it.pinned && !it.edited && !it.manual && it.verify && it.verify.status === 'verified') { /* policy may have changed */ var r = NS.verifyProblem(it, NS.policyOf(c)); if (!r.ok) NS.regenerate(S, S.versions.indexOf(v), it.uid); } }); });
  }
  function build() {
    var c = cfg(), rules = NS.checkRules(c, null);
    if (rules.errors.length) { toast('Fix the rule problems in step 3 first.'); return; }
    snapshot();
    $('#mmView').classList.add('busy');
    setTimeout(function () {
      S = NS.newAssessment(c); draft = null; ui.view = 'review'; ui.version = 0;
      $('#mmView').classList.remove('busy');
      render(); autosave();
      var cnt = NS.counts(S);
      toast(cnt.failed ? cnt.failed + ' problem slot(s) could not be filled with a verified problem — they are marked in red.' : (isTest() ? 'Test' : 'Menu') + ' built. Every answer was checked independently.');
    }, 20);
  }

  /* ---------------- dialogs ---------------- */
  function openDialog(html, onBind) {
    var d = $('#mmDialog'); d.innerHTML = html;
    if (onBind) onBind(d);
    if (typeof d.showModal === 'function') d.showModal(); else d.setAttribute('open', '');
    var f = d.querySelector('input,select,textarea,button'); if (f) f.focus();
    $$('[data-close]', d).forEach(function (b) { b.onclick = function () { closeDialog(); }; });
  }
  function closeDialog() { var d = $('#mmDialog'); if (d.open && d.close) d.close(); else d.removeAttribute('open'); }
  function sectionSkillsDialog(si) {
    var c = cfg(), set = NS.skillSets[c.unitId], s = c.sections[si];
    openDialog('<h2 id="mmDialogTitle">Skills for ' + esc(s.name) + '</h2><p class="hint">Leave all unchecked to use every skill selected in step 4.</p>' +
      set.skills.map(function (k) { return '<label class="chk"><input type="checkbox" value="' + k.id + '"' + (s.skills && s.skills.indexOf(k.id) >= 0 ? ' checked' : '') + (c.skills[k.id] ? '' : ' disabled') + '><span>' + esc(k.name) + ' <span class="mm-chip">' + k.tag + '</span>' + (c.skills[k.id] ? '' : '<small>Turned off in step 4</small>') + '</span></label>'; }).join('') +
      '<div class="mm-dlgbtns"><button type="button" class="btn ghost" data-close>Cancel</button><button type="button" class="btn" id="mmSecSkillsOk">Save</button></div>', function (d) {
      $('#mmSecSkillsOk', d).onclick = function () {
        var on = $$('input:checked', d).map(function (x) { return x.value; });
        if (S) snapshot();
        s.skills = on.length ? on : null; closeDialog(); afterConfigChange(true);
      };
    });
  }
  function sampleDialog(skillId) {
    var c = cfg(), set = NS.skillSets[c.unitId], sk = set.byId[skillId], pol = NS.policyOf(c), used = { keys: new Set(), sigs: new Set() };
    var rows = [1, 2, 3, 4, 5, 6, 7].map(function (lv) {
      var p = NS.generateProblem(c.unitId, skillId, lv, { intOnly: lv <= 5 ? true : pol.intOnly, level: c.level }, 'sample' + lv + Math.random(), used);
      return '<tr><td><b>' + lv + '</b> ' + NS.DIFF_NAMES[lv] + '</td><td>' + (p.failed ? '<i>none available</i>' : promptBlock(p)) + '</td></tr>';
    }).join('');
    openDialog('<h2 id="mmDialogTitle">' + esc(sk.name) + ': how difficulty changes</h2><div class="mm-tablewrap"><table class="mm-sample"><tbody>' + rows + '</tbody></table></div><div class="mm-dlgbtns"><button type="button" class="btn" data-close>Close</button></div>');
  }

  /* ---------------- REVIEW (step 6) ---------------- */
  function promptBlock(p) {
    var h = '<div class="mm-cq">' + mathSafe(p.prompt) + '</div>';
    if (p.work && p.work.length) h += '<ol class="mm-work-lines">' + p.work.map(function (w, i) { return '<li><span>Line ' + (i + 1) + ':</span> ' + mathSafe('⟨' + w + '⟩') + '</li>'; }).join('') + '</ol>';
    if (p.fig) h += NS.figHtml(p.fig);
    var parts = (p.parts || []).filter(function (pt) { return pt.prompt; });
    if (parts.length) h += '<div class="mm-cparts">' + parts.map(function (pt) { return '<div>' + (pt.label ? '<b>(' + esc(pt.label) + ')</b> ' : '') + mathSafe(pt.prompt) + '</div>'; }).join('') + '</div>';
    return h;
  }
  function answerBlock(p) {
    var ans = (p.parts || []).map(function (pt) { return (pt.label ? '<b>(' + esc(pt.label) + ')</b> ' : '') + mathSafe(pt.answer) + (pt.answerFig ? NS.figHtml(pt.answerFig) : ''); }).join('<br>');
    var steps = (p.steps || []).filter(function (s) { return s.t || (s.m && s.w > 0); }).map(function (s) { return '<li>' + mathSafe(s.t) + (s.m ? ' ' + mathSafe('⟨' + s.m + '⟩') : '') + '</li>'; }).join('');
    return '<div class="mm-cans"><div><b>Answer:</b> ' + ans + '</div>' + (steps ? '<ol>' + steps + '</ol>' : '') + '</div>';
  }
  function badge(p) {
    if (p.failed) return '<span class="mm-badge bad" title="' + esc(p.reason) + '">✕ No verified problem</span>';
    var st = p.verify && p.verify.status;
    if (st === 'verified') return '<span class="mm-badge ok" title="Answer recomputed independently from the printed problem">✓ Verified' + (p.edited ? ' (edited)' : '') + '</span>';
    if (p.approved) return '<span class="mm-badge warn" title="' + esc((p.verify.issues || []).join(' ')) + '">✓ Approved by you</span>';
    return '<span class="mm-badge bad" title="' + esc((p.verify.issues || []).join(' ')) + '">! Needs your approval</span>';
  }
  function dishCard(p, si, i) {
    var c = S.config, set = NS.skillSets[c.unitId], lab = NS.dishLabel(c, si, i), show = ui.showAns[p.uid];
    var sk = set.byId[p.skill];
    var head = '<div class="mm-ch"><span class="mm-clab">' + lab + '</span>' + (p.tag ? '<span class="mm-chip">' + esc(p.tag) + '</span>' : '') +
      '<span class="mm-cdiff" title="Difficulty ' + p.c + ' of 7">Lv ' + p.c + ' · ' + NS.DIFF_NAMES[p.c] + '</span>' + badge(p) +
      (p.pinned ? '<span class="mm-badge pin">📌 Pinned</span>' : '') + (p.required && !NS.isTest(c) ? '<span class="mm-badge req">★ Everyone must do</span>' : '') +
      (p.nearRepeat ? '<span class="mm-badge warn" title="This skill ran out of fresh variety at this difficulty">similar to another</span>' : '') + '</div>';
    var skillName = sk ? sk.name : (p.manual ? 'Teacher-written problem' : p.skill);
    var body = p.failed ? '<p class="mm-failmsg">' + esc(p.reason) + '</p>' : promptBlock(p);
    if (!p.failed && NS.sectionFormat(c, si) === 'mc') {
      if (p.mc) body += '<ol class="mm-cchoices' + (p.mc.opts.some(function (o) { return o.replace(/⟨[^⟩]*⟩/g, 'xxxxxx').length > 24; }) ? ' one' : '') + '">' + p.mc.opts.map(function (o, k) { return '<li' + (show && k === p.mc.key ? ' class="ok"' : '') + '><b>' + 'ABCDEFGH'[k] + '</b> <span>' + mathSafe(o) + (show && k === p.mc.key ? ' ✓' : '') + '</span></li>'; }).join('') + '</ol>' + (p.mcNote ? '<p class="mm-fmtnote">' + esc(p.mcNote) + '</p>' : '');
      else body += '<p class="mm-fmtnote bad">Prints as short answer: ' + esc(p.mcFail || 'no choices could be made') + ' Try ↻ New problem, or move it to a short-answer part.</p>';
    }
    var issues = (!p.failed && p.verify && p.verify.status !== 'verified') ? '<div class="mm-issues">' + (p.verify.issues || []).map(function (x) { return '<div>' + esc(x) + '</div>'; }).join('') +
      '<label class="chk"><input type="checkbox" class="mmApprove"' + (p.approved ? ' checked' : '') + '><span>I checked this answer myself and approve it for the key.</span></label></div>' : '';
    var secOpts = c.sections.map(function (s, k) { return '<option value="' + k + '"' + (k === si ? ' disabled' : '') + '>' + esc(s.name) + '</option>'; }).join('');
    var skillOpts = set.skills.map(function (s) { return '<option value="' + s.id + '"' + (s.id === p.skill ? ' selected' : '') + '>' + esc(s.name) + '</option>'; }).join('');
    var lockedNote = p.edited || p.manual ? ' (edited problems are pinned)' : '';
    var tools = '<div class="mm-tools" role="toolbar" aria-label="Tools for ' + lab + '">' +
      '<button type="button" class="btn sm" data-act="regen"' + (p.pinned ? ' disabled title="Unpin to regenerate"' : '') + '>↻ New problem</button>' +
      '<button type="button" class="btn sm ghost" data-act="pin" aria-pressed="' + !!p.pinned + '">' + (p.pinned ? 'Unpin' : '📌 Pin') + '</button>' +
      '<button type="button" class="btn sm ghost" data-act="edit">✎ Edit</button>' +
      '<button type="button" class="btn sm ghost" data-act="easier"' + (p.c <= 1 || p.manual ? ' disabled' : '') + '>Easier</button>' +
      '<button type="button" class="btn sm ghost" data-act="harder"' + (p.c >= 7 || p.manual ? ' disabled' : '') + '>Harder</button>' +
      '<button type="button" class="btn sm ghost" data-act="answer" aria-expanded="' + !!show + '">' + (show ? 'Hide answer' : 'Show answer') + '</button>' +
      '<span class="mm-more">' +
      '<label><span class="sr">Change skill</span><select data-act="skill" aria-label="Change skill for ' + lab + '"' + (p.manual ? ' disabled' : '') + '>' + skillOpts + '</select></label>' +
      '<label><span class="sr">Move to section</span><select data-act="move" aria-label="Move ' + lab + ' to another section"><option value="">Move to…</option>' + secOpts + '</select></label>' +
      '<button type="button" class="btn sm ghost" data-act="up" aria-label="Move ' + lab + ' up"' + (i === 0 ? ' disabled' : '') + '>↑</button>' +
      '<button type="button" class="btn sm ghost" data-act="down" aria-label="Move ' + lab + ' down"' + (i === S.versions[ui.version].sections[si].items.length - 1 ? ' disabled' : '') + '>↓</button>' +
      (NS.isTest(c) ? '' : '<button type="button" class="btn sm ghost" data-act="required" aria-pressed="' + !!p.required + '">' + (p.required ? '★ Required' : '☆ Make required') + '</button>') +
      '<button type="button" class="btn sm ghost danger" data-act="delete" aria-label="Delete ' + lab + '">🗑 Delete</button></span></div>';
    return '<article class="mm-dcard' + (p.failed ? ' failed' : '') + (p.pinned ? ' pinned' : '') + '" data-uid="' + p.uid + '" aria-label="' + lab + ' ' + esc(skillName) + '">' + head +
      '<div class="mm-cskill">' + esc(skillName) + lockedNote + '</div>' + body + issues + (show && !p.failed ? answerBlock(p) : '') + tools + '</article>';
  }
  function viewReview() {
    var c = S.config, v = S.versions[ui.version], set = NS.skillSets[c.unitId];
    var h = '<div class="mm-revbar card"><div class="mm-vtabs" role="group" aria-label="Version">' + S.versions.map(function (x, i) { return '<button type="button" class="tab" data-ver="' + i + '" aria-pressed="' + (i === ui.version) + '">Version ' + x.label + '</button>'; }).join('') + '</div>' +
      '<button type="button" class="btn sec2" id="mmRegenVer">↻ New problems (unpinned, Version ' + v.label + ')</button>' +
      (S.versions.length > 1 ? '<button type="button" class="btn ghost" id="mmRegenAll">↻ Unpinned, all versions</button>' : '') +
      '<button type="button" class="btn ghost" id="mmShowAll">' + (ui.allAns ? 'Hide all answers' : 'Show all answers') + '</button>' +
      '<button type="button" class="btn ghost" id="mmBankToggle" aria-expanded="' + ui.bankOpen + '">Problem bank</button>' +
      '<span class="sp"></span><button type="button" class="btn" id="mmToPreview">Preview →</button></div>' +
      '<p class="hint mm-howto"><b>Regenerate, pin, edit and approve</b> apply to this version only. <b>Easier/Harder, skill, move, delete, add and required</b> change the menu’s structure, so they apply to every version at once.</p>';
    h += '<div class="mm-revgrid' + (ui.bankOpen ? ' withbank' : '') + '"><div class="mm-sections">';
    c.sections.forEach(function (sec, si) {
      var items = v.sections[si].items, req = items.filter(function (x) { return x.required; }).length;
      h += '<section class="mm-secblock" aria-labelledby="mmsec' + si + '"><div class="mm-sechd"><h2 id="mmsec' + si + '">' + esc(sec.name) + '</h2><span class="mm-secinfo">' + (NS.isTest(c) ? items.length + ' questions · ' + esc(NS.FORMATS[NS.sectionFormat(c, si)]) + ' · ' + sec.points + ' pts each' : items.length + ' offered · students complete ' + sec.required + ' · ' + sec.points + ' pts each' + (req ? ' · ' + req + ' required' : '')) + '</span></div>' +
        '<div class="mm-cards">' + items.map(function (p, i) { return dishCard(p, si, i); }).join('') + '</div>' +
        '<div class="mm-addrow"><label>Add a problem: <select class="mmAddSkill" data-si="' + si + '">' + set.skills.map(function (s) { return '<option value="' + s.id + '">' + esc(s.name) + '</option>'; }).join('') + '</select></label>' +
        '<label>Difficulty <select class="mmAddC" data-si="' + si + '">' + [1, 2, 3, 4, 5, 6, 7].map(function (k) { return '<option value="' + k + '"' + (k === NS.sectionC(c, si) ? ' selected' : '') + '>' + k + ' · ' + NS.DIFF_NAMES[k] + '</option>'; }).join('') + '</select></label>' +
        '<button type="button" class="btn sm" data-add="' + si + '">+ Add</button><button type="button" class="btn sm ghost" data-manual="' + si + '">+ Write your own</button></div></section>';
    });
    h += '</div>';
    if (ui.bankOpen) h += bankHtml();
    h += '</div>';
    return h;
  }
  function bankHtml() {
    var c = S.config, set = NS.skillSets[c.unitId], b = S.bank || { items: [] };
    var sk = ui.bankSkill || set.skills[0].id, cc = ui.bankC || NS.sectionC(c, 1);
    return '<aside class="mm-bank card" aria-labelledby="mmBankH"><h2 id="mmBankH">Problem bank</h2><p class="hint">Preview several problems with answers and solutions, then put the ones you want on the menu.</p>' +
      '<label class="field"><span class="lbl">Skill</span><select id="mmBankSkill">' + set.skills.map(function (s) { return '<option value="' + s.id + '"' + (s.id === sk ? ' selected' : '') + '>' + esc(s.name) + '</option>'; }).join('') + '</select></label>' +
      '<div class="mm-bankrow"><label class="field"><span class="lbl">Difficulty</span><select id="mmBankC">' + [1, 2, 3, 4, 5, 6, 7].map(function (k) { return '<option value="' + k + '"' + (k === cc ? ' selected' : '') + '>' + k + ' · ' + NS.DIFF_NAMES[k] + '</option>'; }).join('') + '</select></label>' +
      '<label class="field"><span class="lbl">How many</span><input type="number" id="mmBankN" min="1" max="20" value="' + ui.bankN + '"></label></div>' +
      '<button type="button" class="btn" id="mmBankGo">Generate</button>' +
      '<div class="mm-bankitems">' + (b.items || []).map(function (p, k) {
        return '<article class="mm-bcard" data-buid="' + p.uid + '"><div class="mm-ch"><b>#' + (k + 1) + '</b> <span class="mm-cdiff">Lv ' + p.c + '</span>' + badge(p) + '</div>' + promptBlock(p) + answerBlock(p) +
          '<div class="mm-tools"><label>Add to <select class="mmBankTo">' + c.sections.map(function (s, si) { return '<option value="' + si + '">' + esc(s.name) + '</option>'; }).join('') + '</select></label><button type="button" class="btn sm" data-use="' + p.uid + '">Add</button></div></article>';
      }).join('') + '</div></aside>';
  }
  function bindReview() {
    $$('[data-ver]').forEach(function (b) { b.onclick = function () { ui.version = +b.getAttribute('data-ver'); render(); }; });
    $('#mmRegenVer').onclick = function () { regenAll(ui.version); };
    if ($('#mmRegenAll')) $('#mmRegenAll').onclick = function () { regenAll(null); };
    $('#mmShowAll').onclick = function () { ui.allAns = !ui.allAns; S.versions[ui.version].sections.forEach(function (s) { s.items.forEach(function (p) { ui.showAns[p.uid] = ui.allAns; }); }); render(); };
    $('#mmBankToggle').onclick = function () { ui.bankOpen = !ui.bankOpen; render(); };
    $('#mmToPreview').onclick = function () { ui.view = 'preview'; render(); G.scrollTo(0, 0); };
    $$('.mm-dcard').forEach(function (card) {
      var id = card.getAttribute('data-uid');
      $$('[data-act]', card).forEach(function (b) {
        var act = b.getAttribute('data-act');
        var h = function () { dishAction(act, id, b); };
        if (b.tagName === 'SELECT') b.onchange = h; else b.onclick = h;
      });
      var ap = $('.mmApprove', card); if (ap) ap.onchange = function () { change(function () { NS.approve(S, ui.version, id, ap.checked); }, ap.checked ? 'Approved for the answer key.' : 'Approval removed.'); };
    });
    $$('[data-add]').forEach(function (b) { b.onclick = function () {
      var si = +b.getAttribute('data-add'), sk = $('.mmAddSkill[data-si="' + si + '"]').value, cc = +$('.mmAddC[data-si="' + si + '"]').value;
      change(function () { return NS.addItem(S, si, sk, cc); }, 'Problem added to every version.');
    }; });
    $$('[data-manual]').forEach(function (b) { b.onclick = function () { editDialog(null, +b.getAttribute('data-manual')); }; });
    if (ui.bankOpen) {
      $('#mmBankSkill').onchange = function (e) { ui.bankSkill = e.target.value; };
      $('#mmBankC').onchange = function (e) { ui.bankC = +e.target.value; };
      $('#mmBankN').onchange = function (e) { ui.bankN = Math.max(1, Math.min(20, +e.target.value || 10)); };
      $('#mmBankGo').onclick = function () {
        var set = NS.skillSets[S.config.unitId]; ui.bankSkill = $('#mmBankSkill').value; ui.bankC = +$('#mmBankC').value; ui.bankN = Math.max(1, Math.min(20, +$('#mmBankN').value || 10));
        var r = NS.fillBank(S, ui.bankSkill, ui.bankC, ui.bankN); render();
        toast(r.made + ' verified problems' + (r.failed ? ' (' + r.failed + ' more were not possible without repeating)' : '') + '.');
      };
      $$('[data-use]').forEach(function (b) { b.onclick = function () {
        var si = +$('.mmBankTo', b.closest('.mm-bcard')).value;
        change(function () { return NS.useBankItem(S, b.getAttribute('data-use'), si); }, 'Added (pinned) to ' + S.config.sections[si].name + '. Other versions got a matching problem.');
      }; });
    }
  }
  function regenAll(vIdx) {
    change(function () { return NS.regenerateAll(S, vIdx); }, function (r) { return 'New problems: ' + r.regenerated + '. Kept ' + r.kept + ' pinned or edited.'; });
  }
  function dishAction(act, id, el) {
    var loc = NS.find(S, ui.version, id); if (!loc) return; var p = loc.item;
    if (act === 'answer') { ui.showAns[id] = !ui.showAns[id]; render(); return; }
    if (act === 'edit') { editDialog(p, loc.si); return; }
    if (act === 'regen') return change(function () { var r = NS.regenerate(S, ui.version, id); if (r && r.failed) throw new Error(r.reason); }, 'New problem (same skill and difficulty).');
    if (act === 'pin') return change(function () { NS.togglePin(S, ui.version, id); });
    if (act === 'easier' || act === 'harder') return change(function () { NS.setDifficulty(S, ui.version, id, p.c + (act === 'easier' ? -1 : 1)); }, 'Difficulty changed in every version.');
    if (act === 'skill') return change(function () { NS.changeSkill(S, ui.version, id, el.value); }, 'Skill changed in every version.');
    if (act === 'move') { if (el.value === '') return; var to = +el.value; return change(function () { NS.moveItem(S, ui.version, id, to); }, 'Moved to ' + S.config.sections[to].name + ' in every version. Check the “students complete” numbers.'); }
    if (act === 'up' || act === 'down') return change(function () { NS.reorder(S, ui.version, id, act === 'up' ? -1 : 1); });
    if (act === 'required') return change(function () { NS.setRequired(S, ui.version, id, !p.required); });
    if (act === 'delete') {
      snapshot();
      var info = NS.deleteItem(S, ui.version, id); render(); autosave();
      toast('Problem deleted from every version.', { label: 'Undo', fn: function () { NS.undoDelete(S, info); render(); autosave(); } });
    }
  }

  /* ---------------- edit dialog ---------------- */
  var CHECKS = [['solve', 'Solve an equation (one variable)'], ['classify', 'One / no / infinitely many solutions'], ['simplify', 'Simplify an expression'], ['evaluate', 'Evaluate an expression'], ['literal', 'Solve a formula for a variable'], ['none', 'No automatic check (I will approve the answer)']];
  function toEditText(markup) { return String(markup || '').replace(/⟨([^⟩]*)⟩/g, function (m, t) { return '$' + t + '$'; }); }
  function fromEditText(txt) {
    return String(txt || '').replace(/\$([^$]*)\$/g, function (m, t) {
      t = t.trim(); if (!t) return '';
      if (/\\/.test(t)) return '⟨' + t + '⟩';
      try { return '⟨' + NS.check.toTeX(t) + '⟩'; } catch (e) { return '⟨' + t + '⟩'; }
    });
  }
  function editDialog(p, si) {
    var isNew = !p, set = NS.skillSets[S.config.unitId];
    var parts = p ? p.parts : [{ label: '', prompt: '', answer: '', check: { type: 'solve', v: 'x' } }];
    var partHtml = function (pt, k) {
      var chk = pt.check || { type: 'none' };
      return '<fieldset class="mm-editpart" data-k="' + k + '"><legend>' + (parts.length > 1 ? 'Part ' + (pt.label || k + 1) : 'Answer') + '</legend>' +
        (parts.length > 1 ? '<label class="field"><span class="lbl">Part question</span><input type="text" class="mmEPprompt" value="' + esc(toEditText(pt.prompt)) + '"></label>' : '') +
        '<label class="field"><span class="lbl">Answer shown in the key</span><input type="text" class="mmEPans" value="' + esc(toEditText(pt.answer)) + '" placeholder="e.g. $x=4$"></label>' +
        '<div class="mm-editrow"><label class="field"><span class="lbl">How should this answer be checked?</span><select class="mmEPtype">' + CHECKS.map(function (o) { return '<option value="' + o[0] + '"' + (chk.type === o[0] || (o[0] === 'none' && ['model-eq', 'scenario', 'literal-eval'].indexOf(chk.type) >= 0) ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
        '<label class="field"><span class="lbl">Variable</span><input type="text" class="mmEPvar" maxlength="1" value="' + esc(chk.v || 'x') + '" style="width:3em"></label></div>' +
        '<label class="field"><span class="lbl">Which math in the question is checked?</span><select class="mmEPmath"></select></label>' +
        '<label class="field mmEPvalsWrap"><span class="lbl">Values (for “evaluate”), e.g. x=3, y=-2</span><input type="text" class="mmEPvals" value="' + esc(chk.values ? Object.keys(chk.values).map(function (k2) { return k2 + '=' + chk.values[k2]; }).join(', ') : '') + '"></label>' +
        '<div class="mmEPresult" aria-live="polite"></div></fieldset>';
    };
    var html = '<h2 id="mmDialogTitle">' + (isNew ? 'Write your own problem' : 'Edit ' + NS.dishLabel(S.config, si, NS.find(S, ui.version, p.uid).i)) + '</h2>' +
      '<p class="hint">Put math between dollar signs. You can type it plainly, like <code>$3(x-4)=2x+5$</code> or <code>$x/4+2=7$</code>, or use TeX like <code>$\\frac{x}{4}$</code>. The answer is checked again from what students will see; the old answer is never trusted after an edit.</p>' +
      '<label class="field"><span class="lbl">Question (what students see)</span><textarea id="mmEQ" rows="3">' + esc(toEditText(p ? p.prompt : 'Solve $$.')) + '</textarea></label>' +
      '<div class="mm-eprev" id="mmEQprev" aria-live="polite"></div>' +
      (isNew ? '<label class="field"><span class="lbl">Skill category</span><select id="mmETag">' + Object.keys(set.tags).map(function (t) { return '<option value="' + t + '">' + t + ' — ' + esc(set.tags[t]) + '</option>'; }).join('') + '</select></label>' : '') +
      '<div id="mmEParts">' + parts.map(partHtml).join('') + '</div>' +
      '<label class="field"><span class="lbl">Worked solution for the key (one step per line, optional)</span><textarea id="mmESteps" rows="4">' + esc(p ? (p.steps || []).filter(function (s) { return s.t || s.m; }).map(function (s) { return toEditText(s.t) + (s.m ? ' $' + s.m + '$' : ''); }).join('\n') : '') + '</textarea></label>' +
      '<div class="mm-dlgbtns"><button type="button" class="btn ghost" data-close>Cancel</button><button type="button" class="btn ghost" id="mmECheck">Check answer</button><button type="button" class="btn" id="mmESave">Save</button></div>';
    openDialog(html, function (d) {
      function refreshMath() {
        var q = fromEditText($('#mmEQ', d).value);
        $('#mmEQprev', d).innerHTML = '<b>Preview:</b> ' + mathSafe(q);
        var snips = NS.check.snippets(q).concat([].concat.apply([], $$('.mmEPprompt', d).map(function (x) { return NS.check.snippets(fromEditText(x.value)); })));
        $$('.mm-editpart', d).forEach(function (fs, k) {
          var sel = $('.mmEPmath', fs), old = sel.value || ((parts[k].check || {}).eq || (parts[k].check || {}).expr || '');
          sel.innerHTML = snips.map(function (s) { return '<option value="' + esc(s) + '"' + (s.replace(/\s/g, '') === String(old).replace(/\s/g, '') ? ' selected' : '') + '>' + esc(s) + '</option>'; }).join('') || '<option value="">(no math found — put it between $ signs)</option>';
          $('.mmEPvalsWrap', fs).hidden = $('.mmEPtype', fs).value !== 'evaluate';
        });
      }
      function collect() {
        var data = { prompt: fromEditText($('#mmEQ', d).value), tag: isNew ? $('#mmETag', d).value : p.tag, c: p ? p.c : NS.sectionC(S.config, si), parts: [],
          steps: $('#mmESteps', d).value.split('\n').map(function (l) { return l.trim(); }).filter(Boolean).map(function (l) { return { t: fromEditText(l), m: '', w: 1 }; }) };
        $$('.mm-editpart', d).forEach(function (fs, k) {
          var type = $('.mmEPtype', fs).value, vals = {};
          $('.mmEPvals', fs).value.split(',').forEach(function (pair) { var m = /^\s*([a-zA-Z])\s*=\s*(.+?)\s*$/.exec(pair); if (m) { try { vals[m[1]] = NS.check.toTeX(m[2]); } catch (e) { vals[m[1]] = m[2]; } } });
          var ansRaw = $('.mmEPans', fs).value.trim(), ans = /\$/.test(ansRaw) ? fromEditText(ansRaw) : (function () { try { NS.check.parseRelation(ansRaw); return '⟨' + NS.check.toTeX(ansRaw) + '⟩'; } catch (e) { try { NS.check.parseExpr(ansRaw); return '⟨' + NS.check.toTeX(ansRaw) + '⟩'; } catch (e2) { return ansRaw; } } })();
          var orig = parts[k].check, special = orig && ['model-eq', 'scenario', 'literal-eval'].indexOf(orig.type) >= 0;
          data.parts.push({ label: parts[k].label || '', prompt: parts.length > 1 ? fromEditText($('.mmEPprompt', fs).value) : '', answer: ans, checkType: type, checkMath: $('.mmEPmath', fs).value, checkVar: $('.mmEPvar', fs).value.trim() || 'x', values: vals,
            keepCheck: special && type === 'none' && !$('.mmEPtype', fs).dataset.touched ? orig : null });
        });
        return data;
      }
      function runCheck() {
        var data = collect(), test = NS.buildEdited(data, p, NS.policyOf(S.config));
        $$('.mm-editpart', d).forEach(function (fs, k) {
          var box = $('.mmEPresult', fs), pt = test.parts[k], comp = test.verify.computed && test.verify.computed[k];
          var single = NS.verifyProblem({ prompt: test.prompt, parts: [pt], steps: [], edited: true }, NS.policyOf(S.config));
          if (single.status === 'verified') box.innerHTML = '<p class="ok">✓ Verified: the answer matches the problem.</p>';
          else if (single.status === 'manual') box.innerHTML = '<p class="warn">No automatic check. You will need to approve this answer.</p>';
          else box.innerHTML = '<p class="bad">✕ ' + esc(single.issues.join(' ')) + '</p>' + (comp ? '<button type="button" class="btn sm" data-use-computed="' + k + '">Use the computed answer: ' + mathSafe('⟨' + comp + '⟩') + '</button>' : '');
          var uc = $('[data-use-computed]', box); if (uc) uc.onclick = function () { $('.mmEPans', fs).value = '$' + comp + '$'; runCheck(); };
        });
        return test;
      }
      $('#mmEQ', d).oninput = refreshMath; $$('.mmEPprompt', d).forEach(function (x) { x.oninput = refreshMath; });
      $$('.mmEPtype', d).forEach(function (x) { x.onchange = function () { x.dataset.touched = '1'; refreshMath(); }; });
      refreshMath();
      $('#mmECheck', d).onclick = runCheck;
      $('#mmESave', d).onclick = function () {
        var data = collect();
        if (!data.prompt.trim()) { toast('Write the question first.'); return; }
        snapshot();
        var res;
        if (isNew) res = NS.addManual(S, si, Object.assign(data, { c: NS.sectionC(S.config, si) }));
        else res = NS.applyEdit(S, ui.version, p.uid, data);
        closeDialog(); render(); autosave();
        toast(res.verify.status === 'verified' ? 'Saved and verified. Edited problems are pinned.' : 'Saved. This answer is not verified — approve it on the card after checking it yourself.');
      };
    });
  }

  /* ---------------- PREVIEW (step 7) ---------------- */
  function layoutControls() {
    var L = S.config.layout;
    function seg(name, opts, val) { return '<div class="seg" role="radiogroup" aria-label="' + name + '">' + opts.map(function (o, i) { var id = 'mmL' + name.replace(/\W/g, '') + i; return '<input type="radio" id="' + id + '" name="mmL' + name.replace(/\W/g, '') + '" value="' + o[0] + '"' + (val === o[0] ? ' checked' : '') + '><label for="' + id + '">' + o[1] + '</label>'; }).join('') + '</div>'; }
    return '<div class="card mm-layout"><h2>Print layout</h2>' +
      (isTest() ? '' : '<div class="field"><span class="lbl">Format</span>' + seg('Format', [['together', 'Problems with workspace'], ['menu-only', 'Menu + separate work pages']], L.format) + '</div>') +
      '<div class="field"><span class="lbl">Spacing</span>' + seg('Spacing', [['compact', 'Compact'], ['standard', 'Standard'], ['spacious', 'Spacious']], L.density) + '</div>' +
      '<div class="field"><span class="lbl">Workspace</span>' + seg('Workspace', [['none', 'Blank'], ['graph', 'Graph paper'], ['coordinate', 'Coordinate plane']], L.grid) + '</div>' +
      '<label class="chk"><input type="checkbox" id="mmLRef"' + (L.reference ? ' checked' : '') + '><span>Add a reference page for students</span></label>' +
      '<label class="chk"><input type="checkbox" id="mmLGuide"' + (L.guide !== false ? ' checked' : '') + '><span>Include the teacher guide page in the key</span></label></div>';
  }
  function viewPreview() {
    return '<div class="mm-prevgrid"><div>' + layoutControls() + '</div><div><div class="ptool"><div class="grp" role="group" aria-label="Document"><button type="button" class="tab" data-doc="student" aria-pressed="' + (ui.preview === 'student') + '">Student ' + noun() + '</button><button type="button" class="tab" data-doc="key" aria-pressed="' + (ui.preview === 'key') + '">Teacher key</button></div>' +
      (S.versions.length > 1 ? '<div class="grp" role="group" aria-label="Version">' + S.versions.map(function (x, i) { return '<button type="button" class="tab" data-pver="' + i + '" aria-pressed="' + (i === ui.version) + '">' + x.label + '</button>'; }).join('') + '</div>' : '') +
      '<span class="sp"></span><span id="mmPStatus" role="status"></span><select id="mmZoom" aria-label="Zoom">' + [['fit', 'Fit width'], ['0.6', '60%'], ['0.8', '80%'], ['1', '100%']].map(function (z) { return '<option value="' + z[0] + '"' + (ui.zoom === z[0] ? ' selected' : '') + '>' + z[1] + '</option>'; }).join('') + '</select>' +
      '<button type="button" class="btn" id="mmToExport">Print & save →</button></div><div id="pagesWrap"><div id="pages"></div></div></div></div>';
  }
  var previewToken = 0;
  function bindPreview() {
    var L = S.config.layout;
    $$('input[name=mmLFormat]').forEach(function (r) { r.onchange = function () { snapshot(); L.format = r.value; autosave(); drawPreview(); }; });
    $$('input[name=mmLSpacing]').forEach(function (r) { r.onchange = function () { snapshot(); L.density = r.value; autosave(); drawPreview(); }; });
    $$('input[name=mmLWorkspace]').forEach(function (r) { r.onchange = function () { snapshot(); L.grid = r.value; autosave(); drawPreview(); }; });
    $('#mmLRef').onchange = function (e) { snapshot(); L.reference = e.target.checked; autosave(); drawPreview(); };
    $('#mmLGuide').onchange = function (e) { snapshot(); L.guide = e.target.checked; autosave(); drawPreview(); };
    $$('[data-doc]').forEach(function (b) { b.onclick = function () { ui.preview = b.getAttribute('data-doc'); render(); }; });
    $$('[data-pver]').forEach(function (b) { b.onclick = function () { ui.version = +b.getAttribute('data-pver'); render(); }; });
    $('#mmZoom').onchange = function (e) { ui.zoom = e.target.value; fitZoom(); };
    $('#mmToExport').onclick = function () { ui.view = 'export'; render(); G.scrollTo(0, 0); };
    drawPreview();
  }
  function drawPreview() {
    var tok = ++previewToken, box = $('#pages'); if (!box) return;
    $('#mmPStatus').textContent = 'Laying out pages…';
    NS.renderPages(S, ui.version, ui.preview).then(function (pages) {
      if (tok !== previewToken || !$('#pages')) return;
      box.innerHTML = ''; pages.forEach(function (pg) { box.appendChild(pg); });
      $('#mmPStatus').textContent = pages.length + ' page' + (pages.length > 1 ? 's' : '') + (pages.overflow.length ? ' · ⚠ a block is taller than one page' : '');
      fitZoom();
    });
  }
  function fitZoom() {
    var box = $('#pages'), wrap = $('#pagesWrap'); if (!box || !wrap) return;
    var z = ui.zoom === 'fit' ? Math.min(1, (wrap.clientWidth - 30) / (8.5 * 96)) : +ui.zoom;
    $$('.page', box).forEach(function (p) { p.style.zoom = z; });
  }

  /* ---------------- EXPORT (step 8) ---------------- */
  function viewExport() {
    var blockers = NS.blockers(S), saves = listSaves();
    return '<div class="mm-exgrid"><section class="card mm-card"><h2><span class="step">8</span>Print or save as PDF</h2>' +
      (blockers.length ? '<div class="mm-block"><b>Before you print:</b><ul>' + blockers.slice(0, 12).map(function (b) { return '<li>' + esc(b) + '</li>'; }).join('') + (blockers.length > 12 ? '<li>…and ' + (blockers.length - 12) + ' more</li>' : '') + '</ul></div>' : '<p class="ok">✓ Ready to print. Every answer in the key was checked against the printed problem.</p>') +
      '<div class="mm-printbtns">' + S.versions.map(function (v, i) { return '<button type="button" class="btn" data-print="student" data-pv="' + i + '">Student ' + noun() + (S.versions.length > 1 ? ' · Version ' + v.label : '') + '</button>'; }).join('') +
      (S.versions.length > 1 ? '<button type="button" class="btn ghost" data-print="student" data-pv="all">All student versions</button>' : '') + '</div>' +
      '<div class="mm-printbtns">' + S.versions.map(function (v, i) { return '<button type="button" class="btn sec2" data-print="key" data-pv="' + i + '">Teacher key' + (S.versions.length > 1 ? ' · Version ' + v.label : '') + '</button>'; }).join('') +
      (S.versions.length > 1 ? '<button type="button" class="btn ghost" data-print="key" data-pv="all">All keys</button>' : '') + '</div>' +
      '<p class="hint">In the print dialog choose <b>Save as PDF</b> (or your printer), paper <b>Letter</b>, margins <b>None</b>, scale <b>100%</b>, and turn <b>headers and footers off</b>. Student menus never contain answers; keys are printed separately.</p>' +
      '<p class="hint"><b>About answer keys:</b> keys you print stay on your computer. If you post a key online, a code prompt on a web page is only a convenience, not real security, so do not treat a publicly hosted key as private.</p></section>' +
      '<section class="card mm-card"><h2>Save this assessment</h2><p class="hint">Your current menu or test is saved in this browser automatically. Save a named copy to come back to it, or download a file to move it to another computer or share it with a colleague.</p>' +
      '<div class="mm-saverow"><input type="text" id="mmSaveName" value="' + esc(S.config.title + ' · ' + NS.LEVELS[S.config.level].name) + '" aria-label="Name for this saved assessment"><button type="button" class="btn" id="mmSaveNamed">Save in this browser</button></div>' +
      '<div class="mm-saverow"><button type="button" class="btn ghost" id="mmDownload">Download file (.json)</button><label class="btn ghost mm-filebtn">Open a file…<input type="file" id="mmOpenFile" accept=".json,application/json"></label><button type="button" class="btn ghost" id="mmDup">Duplicate as a new copy</button><button type="button" class="btn ghost danger" id="mmNew">Start over</button></div>' +
      (saves.length ? '<h3>Saved in this browser</h3><ul class="mm-saves">' + saves.map(function (s) { return '<li><span><b>' + esc(s.name) + '</b><small>' + esc(new Date(s.saved).toLocaleString()) + '</small></span><span><button type="button" class="btn sm" data-load="' + s.id + '">Open</button><button type="button" class="btn sm ghost" data-dupsave="' + s.id + '">Duplicate</button><button type="button" class="btn sm ghost danger" data-delsave="' + s.id + '">Delete</button></span></li>'; }).join('') + '</ul>' : '') +
      '</section></div>';
  }
  function listSaves() { try { var o = JSON.parse(lsGet(KEY_SAVES) || '{}'); return Object.keys(o).map(function (k) { return Object.assign({ id: k }, o[k]); }).sort(function (a, b) { return b.saved < a.saved ? -1 : 1; }); } catch (e) { return []; } }
  function writeSaves(list) { var o = {}; list.forEach(function (s) { o[s.id] = { name: s.name, saved: s.saved, data: s.data }; }); return lsSet(KEY_SAVES, JSON.stringify(o)); }
  function bindExport() {
    $$('[data-print]').forEach(function (b) { b.onclick = function () {
      var kind = b.getAttribute('data-print'), pv = b.getAttribute('data-pv');
      var list = pv === 'all' ? S.versions.map(function (v, i) { return i; }) : [+pv];
      var blockers = NS.blockers(S);
      if (blockers.length && !G.confirm('Some problems are not ready:\n\n' + blockers.slice(0, 6).join('\n') + (blockers.length > 6 ? '\n…' : '') + '\n\nPrint anyway?')) return;
      printDocs(list.map(function (v) { return { v: v, kind: kind }; }));
    }; });
    $('#mmSaveNamed').onclick = function () {
      var name = $('#mmSaveName').value.trim() || S.config.title, list = listSaves();
      list.push({ id: NS.uid('save'), name: name, saved: new Date().toISOString(), data: NS.serialize(S) });
      toast(writeSaves(list) ? 'Saved “' + name + '” in this browser.' : 'This browser would not save it (storage full or blocked). Download a file instead.'); render();
    };
    $('#mmDownload').onclick = function () {
      var blob = new Blob([NS.serialize(S)], { type: 'application/json' }), a = doc.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = (S.config.title || 'menu-assessment').replace(/[^\w\- ]+/g, '').replace(/\s+/g, '-').toLowerCase() + '-' + S.config.level + '.json';
      doc.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    };
    $('#mmOpenFile').onchange = function (e) {
      var f = e.target.files[0]; if (!f) return;
      var rd = new FileReader(); rd.onload = function () {
        try { var st = NS.deserialize(rd.result); snapshot(); S = st; draft = null; ui.view = 'review'; ui.version = 0; render(); autosave(); toast('Opened. Every answer was re-checked.'); }
        catch (err) { toast('Could not open that file: ' + err.message); }
      }; rd.readAsText(f);
    };
    $('#mmDup').onclick = function () { snapshot(); S = NS.duplicate(S); render(); autosave(); toast('Duplicated. You are now editing the copy.'); };
    $('#mmNew').onclick = function () { if (!G.confirm('Start over? (You can undo this.)')) return; snapshot(); draft = NS.defaultConfig(S.config.unitId, S.config.mode); S = null; ui.view = 'setup'; render(); autosave(); };
    $$('[data-load]').forEach(function (b) { b.onclick = function () { var s = listSaves().filter(function (x) { return x.id === b.getAttribute('data-load'); })[0]; if (!s) return; try { snapshot(); S = NS.deserialize(s.data); draft = null; ui.view = 'review'; ui.version = 0; render(); autosave(); toast('Opened “' + s.name + '”.'); } catch (e) { toast('Could not open: ' + e.message); } }; });
    $$('[data-dupsave]').forEach(function (b) { b.onclick = function () { var list = listSaves(), s = list.filter(function (x) { return x.id === b.getAttribute('data-dupsave'); })[0]; if (!s) return; list.push({ id: NS.uid('save'), name: s.name + ' (copy)', saved: new Date().toISOString(), data: s.data }); writeSaves(list); render(); }; });
    $$('[data-delsave]').forEach(function (b) { b.onclick = function () { if (!G.confirm('Delete this saved menu from this browser?')) return; writeSaves(listSaves().filter(function (x) { return x.id !== b.getAttribute('data-delsave'); })); render(); }; });
  }
  function printDocs(jobs) {
    var root = $('#printRoot'); root.innerHTML = '';
    toast('Preparing pages…');
    var chain = Promise.resolve();
    jobs.forEach(function (j) { chain = chain.then(function () { return NS.renderPages(S, j.v, j.kind).then(function (pages) { pages.forEach(function (p) { p.style.zoom = ''; root.appendChild(p); }); }); }); });
    chain.then(function () {
      doc.body.classList.add('printing');
      var done = function () { doc.body.classList.remove('printing'); root.innerHTML = ''; G.removeEventListener('afterprint', done); };
      G.addEventListener('afterprint', done);
      setTimeout(function () { G.print(); setTimeout(function () { if (doc.body.classList.contains('printing') && !G.matchMedia('print').matches) done(); }, 1500); }, 60);
    });
  }

  /* ---------------- main render ---------------- */
  function render() {
    renderSteps(); renderSummary();
    var v = $('#mmView');
    if (ui.view !== 'setup' && !S) ui.view = 'setup';
    if (ui.version >= (S ? S.versions.length : 1)) ui.version = 0;
    v.className = 'mm-view-' + ui.view;
    if (ui.view === 'setup') { v.innerHTML = viewSetup(); bindSetup(); }
    else if (ui.view === 'review') { v.innerHTML = viewReview(); bindReview(); }
    else if (ui.view === 'preview') { v.innerHTML = viewPreview(); bindPreview(); }
    else { v.innerHTML = viewExport(); bindExport(); }
  }

  /* ---------------- start ---------------- */
  function applyTheme(t) { if (t) doc.documentElement.setAttribute('data-theme', t); else doc.documentElement.removeAttribute('data-theme'); }
  applyTheme(lsGet(KEY_THEME));
  $('#themeBtn').onclick = function () {
    var cur = doc.documentElement.getAttribute('data-theme') || (G.matchMedia && G.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark'; applyTheme(next); lsSet(KEY_THEME, next);
  };
  $('#mmUndo').onclick = undo;
  doc.addEventListener('keydown', function (e) { if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !/INPUT|TEXTAREA|SELECT/.test(doc.activeElement.tagName)) { e.preventDefault(); undo(); } });
  G.addEventListener('resize', function () { if (ui.view === 'preview') fitZoom(); });

  /* Load a unit's autosaved work (or a fresh menu for it). */
  function loadUnit(unit, level) {
    draft = null; S = null; ui.view = 'setup'; ui.version = 0;
    var raw = lsGet(curKey(unit));
    if (!raw && unit === 'algebra1-expressions-equations') raw = lsGet(KEY_CUR);     // autosave from the first release
    if (raw) {
      try {
        var o = JSON.parse(raw);
        if (o.draft && o.draft.unitId === unit) draft = o.draft;
        else if (o.format === 'mk-menu-assessment' && o.config.unitId === unit) { S = NS.deserialize(o); ui.view = 'review'; }
      } catch (e) { draft = null; S = null; }
    }
    if (!draft && !S) { draft = NS.defaultConfig(unit, /mode=test/.test(G.location.hash || '') ? 'test' : 'menu'); if (level) draft.level = level; }
    return !!S;
  }
  (function restore() {
    var unit = hashUnit() || (NS.skillSets[lsGet(KEY_LAST)] ? lsGet(KEY_LAST) : null) || (NS.skillSets[defaultUnit] ? defaultUnit : Object.keys(NS.skillSets)[0]);
    var restored = loadUnit(unit);
    render();
    if (restored) toast('Welcome back. Your last ' + NS.skillSets[unit].unitName + ' ' + noun() + ' was restored from this browser.');
  })();
  G.addEventListener('hashchange', function () { var u = hashUnit(); if (u && u !== cfg().unitId) { autosave(); loadUnit(u); render(); } });
  NS.app = { state: function () { return S; }, render: render, ui: ui };   // for tests
})(window);
