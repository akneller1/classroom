/* Menu Assessment Generator — engine (no DOM).

   • skill-set registry (one file per unit under menu/skills/)
   • class levels and per-problem difficulty (c = 1…7)
   • menu configuration + rule checking (impossible / inconsistent requirements, maximum score)
   • problem generation: generate → verify independently → de-duplicate → retry; a problem that
     fails verification is never used, and a skill that cannot produce a verified problem is
     reported instead of being silently replaced
   • assessment state: versions A/B/C that share one structure (slots), pin, regenerate, edit,
     change difficulty/skill, move, delete, add, problem bank
   • save / load / duplicate (JSON)

   Reuses the worksheet generator's seeded RNG (core/rng.js). */
(function (G) {
  'use strict';
  var WS = G.MKWS, NS = (G.MKMENU = G.MKMENU || {});

  /* ---------------- skill sets ---------------- */
  var sets = NS.skillSets = {};
  NS.registerSkillSet = function (set) {
    set.byId = {}; set.skills.forEach(function (s) { set.byId[s.id] = s; });
    sets[set.id] = set; return set;
  };
  /* Units the generator knows about. Units without a skill set are listed as "not yet supported". */
  NS.CATALOG = [
    { course: 'Algebra 1', units: [   // follows the 180-day roadmap (units 1–12)
      ['algebra1-expressions-equations', 'Units 1–2 · Foundations & Solving Linear Equations'], ['algebra1-inequalities', 'Unit 3 · Linear Inequalities'],
      ['algebra1-relations-functions', 'Unit 4 · Relations and Functions'], ['algebra1-linear-equations-slope', 'Unit 5 · Linear Functions and Graphing'],
      ['algebra1-systems-of-equations', 'Unit 6 · Systems of Equations and Inequalities'], ['algebra1-exponents-scientific-notation', 'Unit 7 · Exponents and Scientific Notation'],
      ['algebra1-exponential-functions', 'Unit 8 · Exponential Functions'], ['algebra1-polynomials', 'Unit 9 · Polynomials'],
      ['algebra1-factoring-zero-product', 'Unit 10 · Factoring and Zero Product Property'], ['algebra1-quadratics', 'Unit 11 · Quadratic Functions and Equations'],
      ['algebra1-statistics-data-modeling', 'Unit 12 · Statistics and Data Modeling']] },
    { course: 'Geometry', units: [
      ['geometry-basics-reasoning', 'Basics & Reasoning'], ['geometry-angles-parallel-lines', 'Angles & Parallel Lines'], ['geometry-triangles-congruence', 'Triangles & Congruence'],
      ['geometry-similarity', 'Similarity'], ['geometry-right-triangles-trigonometry', 'Right Triangles & Trigonometry'], ['geometry-circles', 'Circles'],
      ['geometry-area-surface-area-volume', 'Area, Surface Area & Volume'], ['geometry-coordinate-geometry-transformations', 'Coordinate Geometry & Transformations']] },
    { course: 'Algebra 2', units: [
      ['algebra2-functions-transformations', 'Functions & Transformations'], ['algebra2-linear-functions-systems', 'Linear Functions & Systems'], ['algebra2-quadratic-functions-complex-numbers', 'Quadratic Functions & Complex Numbers'],
      ['algebra2-polynomial-functions', 'Polynomial Functions'], ['algebra2-radicals-rational-exponents', 'Radicals & Rational Exponents'], ['algebra2-exponential-logarithmic-functions', 'Exponential & Logarithmic Functions'],
      ['algebra2-rational-functions', 'Rational Functions'], ['algebra2-sequences-series', 'Sequences & Series'], ['algebra2-trigonometric-functions', 'Trigonometric Functions']] }
  ];

  /* ---------------- levels & difficulty ---------------- */
  NS.LEVELS = {
    cp2: { id: 'cp2', name: 'CP2', long: 'CP2 · Foundational', tiers: [1, 2, 3], intOnly: true,
      about: 'Whole-number answers, fewer steps, positive values first, plain wording.' },
    cp1: { id: 'cp1', name: 'CP1', long: 'CP1 · Standard', tiers: [3, 4, 5], intOnly: true,
      about: 'Grade-level, multi-step problems with negatives, fraction bars and decimals.' },
    honors: { id: 'honors', name: 'Honors', long: 'Honors · Advanced', tiers: [5, 6, 7], intOnly: false,
      about: 'Fraction coefficients, combined concepts, multi-part problems; fraction answers allowed.' }
  };
  NS.DIFF_NAMES = ['', 'Warm-up', 'Basic', 'Developing', 'Standard', 'Strong', 'Advanced', 'Challenge'];
  NS.MIN_C = 1; NS.MAX_C = 7;

  function policyOf(cfg) {
    var lv = NS.LEVELS[cfg.level] || NS.LEVELS.cp1;
    var intOnly = cfg.answers === 'integers' ? true : cfg.answers === 'fractions' ? false : lv.intOnly;
    return { intOnly: intOnly, level: lv.id };
  }
  NS.policyOf = policyOf;
  NS.sectionC = function (cfg, si) {
    var sec = cfg.sections[si], lv = NS.LEVELS[cfg.level] || NS.LEVELS.cp1;
    var tier = sec.tier === 'ramp' ? 1 : sec.tier !== undefined ? sec.tier : Math.min(si, 2);
    var c = lv.tiers[Math.max(0, Math.min(2, tier))] + (sec.adjust || 0);
    return Math.max(NS.MIN_C, Math.min(NS.MAX_C, c));
  };
  /* Difficulty of question i of n in a section. A "ramp" section (standard tests) goes from the level's
     easiest tier to its hardest across the section; any other section uses one difficulty. */
  NS.itemC = function (cfg, si, i, n) {
    var sec = cfg.sections[si]; if (!sec || sec.tier !== 'ramp') return NS.sectionC(cfg, si);
    var lv = NS.LEVELS[cfg.level] || NS.LEVELS.cp1, t = n > 0 ? Math.min(2, Math.floor(3 * i / n)) : 1;
    return Math.max(NS.MIN_C, Math.min(NS.MAX_C, lv.tiers[t] + (sec.adjust || 0)));
  };
  NS.isTest = function (cfg) { return !!cfg && cfg.mode === 'test'; };
  NS.sectionFormat = function (cfg, si) { return (cfg.sections[si] && cfg.sections[si].qformat) || 'open'; };
  NS.FORMATS = { open: 'Short answer (show your work)', mc: 'Multiple choice' };

  /* ---------------- configuration ---------------- */
  var uidN = 0;
  function uid(p) { uidN++; return (p || 'id') + '-' + Date.now().toString(36) + '-' + uidN.toString(36) + '-' + Math.floor(Math.random() * 1e6).toString(36); }
  NS.uid = uid;

  /* Standard test parts: every question is answered; difficulty rises within each part. */
  NS.testSections = function (preset) {
    var P = { std: [['Multiple Choice', 'Choose the best answer.', 4, 10, 'mc'], ['Short Answer', 'Show your work.', 10, 6, 'open']],
      quiz: [['Multiple Choice', 'Choose the best answer.', 5, 6, 'mc'], ['Short Answer', 'Show your work.', 10, 2, 'open']],
      mc: [['Multiple Choice', 'Choose the best answer.', 5, 20, 'mc']],
      open: [['Short Answer', 'Show your work.', 10, 10, 'open']] }[preset || 'std'];
    return P.map(function (x) { return { id: uid('sec'), name: x[0], note: x[1], points: x[2], offered: x[3], required: x[3], tier: 'ramp', adjust: 0, skills: null, qformat: x[4] }; });
  };
  NS.menuSections = function () {
    return [
      { id: 'app', name: 'Appetizers', note: 'Warm-ups', points: 5, offered: 6, required: 4, tier: 0, adjust: 0, skills: null },
      { id: 'ent', name: 'Entrées', note: 'Multi-step problems', points: 10, offered: 6, required: 4, tier: 1, adjust: 0, skills: null },
      { id: 'spc', name: 'Chef’s Specials', note: 'Multi-part challenges', points: 20, offered: 3, required: 2, tier: 2, adjust: 0, skills: null }];
  };
  /* Switch a configuration between the choice menu and a standard test (sections, coverage, default titles). */
  NS.setMode = function (cfg, mode) {
    var set = sets[cfg.unitId], wasDefaultTitle = !cfg.title || cfg.title === (set && set.title) || cfg.title === (set && set.unitName + ' Test');
    var wasDefaultSub = !cfg.subtitle || /^Assessment Menu · |^Unit test · /.test(cfg.subtitle);
    cfg.mode = mode === 'test' ? 'test' : 'menu';
    cfg.sections = cfg.mode === 'test' ? NS.testSections('std') : NS.menuSections();
    cfg.coverage = { on: cfg.mode !== 'test', tags: null };
    if (wasDefaultTitle && set) cfg.title = cfg.mode === 'test' ? set.unitName + ' Test' : set.title;
    if (wasDefaultSub) cfg.subtitle = cfg.mode === 'test' ? 'Unit test · answer every question' : 'Assessment Menu · choose your meal and show what you know';
    return cfg;
  };
  NS.defaultConfig = function (setId, mode) {
    var cfg = NS.menuConfig(setId);
    if (mode === 'test') NS.setMode(cfg, 'test');
    return cfg;
  };
  NS.menuConfig = function (setId) {
    var set = sets[setId];
    var skills = {}; if (set) set.skills.forEach(function (s) { skills[s.id] = true; });
    return {
      format: 'mk-menu-assessment', schema: 1, unitId: setId, mode: 'menu',
      title: set ? set.title : 'Assessment Menu', subtitle: 'Assessment Menu · choose your meal and show what you know',
      level: 'cp1', answers: 'auto', seed: Math.floor(Math.random() * 1e9),
      skills: skills,
      sections: NS.menuSections(),
      coverage: { on: true, tags: null },          // null = every skill category that appears on the menu
      layout: { format: 'together', density: 'standard', grid: 'none', reference: false, guide: true },
      versions: 1
    };
  };

  /* Which skills may appear in a section (teacher choice or all selected skills). */
  NS.sectionSkills = function (cfg, si) {
    var set = sets[cfg.unitId]; if (!set) return [];
    var chosen = set.skills.filter(function (s) { return cfg.skills[s.id]; }).map(function (s) { return s.id; });
    var sec = cfg.sections[si];
    if (sec.skills && sec.skills.length) return sec.skills.filter(function (id) { return chosen.indexOf(id) >= 0; });
    return chosen;
  };
  NS.coverageTags = function (cfg, state) {
    if (!cfg.coverage || !cfg.coverage.on) return [];
    if (cfg.coverage.tags && cfg.coverage.tags.length) return cfg.coverage.tags.slice();
    var set = sets[cfg.unitId], tags = [];
    var ver = state && state.versions[0];
    if (ver) ver.sections.forEach(function (s) { s.items.forEach(function (it) { if (it.tag && tags.indexOf(it.tag) < 0) tags.push(it.tag); }); });
    else if (set) set.skills.forEach(function (s) { if (cfg.skills[s.id] && tags.indexOf(s.tag) < 0) tags.push(s.tag); });
    var order = set ? Object.keys(set.tags) : [];
    return tags.sort(function (a, b) { return order.indexOf(a) - order.indexOf(b); });
  };

  /* Rule check. Returns {errors:[], warnings:[], maxScore, totalOffered, totalRequired, perSection:[]} */
  NS.checkRules = function (cfg, state) {
    var errors = [], warnings = [], max = 0, offered = 0, reqTotal = 0, per = [];
    if (!cfg.sections.length) errors.push('Add at least one menu section.');
    var test = NS.isTest(cfg);
    if (test) cfg.sections.forEach(function (s) { s.required = s.offered; });   // everyone answers every question
    cfg.sections.forEach(function (s, i) {
      var nm = s.name || 'Section ' + (i + 1);
      var o = s.offered | 0, r = s.required | 0, pts = +s.points;
      if (!(o >= 1)) errors.push(nm + ': offer at least one problem.');
      if (r < 0) errors.push(nm + ': the number required cannot be negative.');
      if (r > o) errors.push(nm + ': students must complete ' + r + ' but only ' + o + ' are offered.');
      if (!(pts > 0)) errors.push(nm + ': points per problem must be more than 0.');
      if (r === 0 && o > 0) warnings.push(nm + ': students are not required to complete any of these, so they will not count toward the score.');
      if (r === o && o > 0 && !test) warnings.push(nm + ': students must complete every problem, so there is no choice in this section.');
      if (!NS.sectionSkills(cfg, i).length) errors.push(nm + ': no skills are available for this section.');
      var forced = 0;
      if (state) { var sec = state.versions[0] && state.versions[0].sections[i]; if (sec) forced = sec.items.filter(function (it) { return it.required; }).length; }
      if (forced > r) errors.push(nm + ': ' + forced + ' problems are marked "everyone must do this" but students only complete ' + r + '.');
      max += Math.max(0, Math.min(r, o)) * (pts > 0 ? pts : 0); offered += o; reqTotal += r;
      per.push({ name: nm, offered: o, required: r, points: pts, possible: Math.max(0, Math.min(r, o)) * pts, forced: forced });
    });
    var names = {}; cfg.sections.forEach(function (s) { var k = (s.name || '').trim().toLowerCase(); if (k && names[k]) warnings.push('Two sections are both named "' + s.name + '".'); names[k] = 1; });
    // coverage feasibility
    var tags = NS.coverageTags(cfg, state);
    if (tags.length) {
      if (tags.length > reqTotal) errors.push('Students must cover ' + tags.length + ' skill categories but only complete ' + reqTotal + ' problems in total.');
      else if (state && state.versions[0]) {
        var feas = coverageFeasible(cfg, state.versions[0], tags);
        if (!feas.ok) errors.push(feas.msg);
      } else {
        tags.forEach(function (t) {
          var ok = cfg.sections.some(function (s, i) { return NS.sectionSkills(cfg, i).some(function (id) { return sets[cfg.unitId].byId[id].tag === t; }); });
          if (!ok) errors.push('No section can offer a ' + t + ' problem, but students must complete one.');
        });
      }
    }
    if (max !== 100 && !errors.length) warnings.push('The maximum score is ' + fmt(max) + ' points (not 100). That is fine for a quiz; scale it if you need a percentage.');
    return { errors: errors, warnings: warnings, maxScore: max, totalOffered: offered, totalRequired: reqTotal, perSection: per, tags: tags };
  };
  function fmt(n) { return Math.round(n * 100) / 100; }

  /* Can a student pick exactly `required` dishes in every section, including every dish marked
     required, and still cover every tag? (max-flow: tags -> sections with spare picks) */
  function coverageFeasible(cfg, ver, tags) {
    var need = tags.slice(), spare = [];
    ver.sections.forEach(function (s, i) {
      var forced = s.items.filter(function (it) { return it.required; });
      forced.forEach(function (it) { var k = need.indexOf(it.tag); if (k >= 0) need.splice(k, 1); });
      spare.push(Math.max(0, (cfg.sections[i].required | 0) - forced.length));
    });
    var missing = need.filter(function (t) { return !ver.sections.some(function (s) { return s.items.some(function (it) { return it.tag === t; }); }); });
    if (missing.length) return { ok: false, msg: 'Students must cover ' + missing.join(', ') + ' but the menu has no ' + (missing.length > 1 ? 'problems in those categories.' : 'problem in that category.') };
    // slots: each tag needs one spare pick in a section that offers an unforced dish with that tag
    var match = {}; // slotKey -> tag
    function canUse(t, si) { return ver.sections[si].items.some(function (it) { return it.tag === t && !it.required; }); }
    function augment(t, seen) {
      for (var si = 0; si < spare.length; si++) {
        if (!canUse(t, si)) continue;
        for (var k = 0; k < spare[si]; k++) {
          var key = si + ':' + k; if (seen[key]) continue; seen[key] = 1;
          if (!match[key] || augment(match[key], seen)) { match[key] = t; return true; }
        }
      }
      return false;
    }
    for (var i = 0; i < need.length; i++) if (!augment(need[i], {})) return { ok: false, msg: 'With these "choose" numbers, students cannot cover every skill category (' + need[i] + ' is the problem). Offer it in another section or let students choose more.' };
    return { ok: true };
  }

  /* ---------------- problem generation ---------------- */
  /* Everything a student sees: words, math, shown work and figures. */
  function figKey(p) { return p.fig ? '|fig:' + JSON.stringify(p.fig) : ''; }
  function studentKey(p) { return NS.studentText(p).replace(/\s+/g, '') + figKey(p); }
  function nearSig(skill, p) {
    var nums = ((NS.studentText(p) + figKey(p)).match(/\d+(?:\.\d+)?/g) || []).map(Number).map(Math.abs).sort(function (a, b) { return a - b; });
    return skill + '|' + (p.variant || '') + '|' + nums.join(',');
  }
  NS.stats = { generated: 0, rejectedByVerifier: 0, rejectedByGenerator: 0, duplicates: 0 };

  /* used = {keys:Set, sigs:Set}. Returns a problem or {failed:true, reason}. */
  NS.generateProblem = function (setId, skillId, c, policy, seed, used) {
    var set = sets[setId], sk = set && set.byId[skillId];
    if (!sk) return { failed: true, reason: 'Unknown skill ' + skillId };
    used = used || { keys: new Set(), sigs: new Set() };
    var lastReason = 'no attempt succeeded', fallback = null;
    for (var attempt = 0; attempt < 500; attempt++) {
      var rng = WS.rng.make(WS.rng.hash([seed, skillId, c, attempt].join('|')));
      var ctx = { rng: rng, c: c, intOnly: policy.intOnly, level: policy.level };
      var p;
      try { p = sk.generate(ctx); }
      catch (e) {
        if (e && e.isReject) { NS.stats.rejectedByGenerator++; lastReason = e.message; continue; }
        // A generator bug must never crash the page or slip through: count it, report it, try again.
        NS.stats.generatorErrors = (NS.stats.generatorErrors || 0) + 1; NS.stats.lastError = skillId + ' c' + c + ': ' + (e && e.message);
        lastReason = 'generator error: ' + (e && e.message); continue;
      }
      var key = studentKey(p), sig = nearSig(skillId, p);
      if (used.keys.has(key)) { NS.stats.duplicates++; continue; }
      if (attempt < 350 && used.sigs.has(sig)) { NS.stats.duplicates++; if (!fallback) fallback = { p: p, key: key, sig: sig }; continue; }
      var v = NS.verifyProblem(p, policy);
      if (!v.ok) { NS.stats.rejectedByVerifier++; lastReason = 'verifier: ' + v.issues.join('; '); continue; }
      return finish(p, key, sig, v);
    }
    if (fallback) { var fv = NS.verifyProblem(fallback.p, policy); if (fv.ok) return finish(fallback.p, fallback.key, fallback.sig, fv, true); }
    return { failed: true, reason: lastReason };
    function finish(p, key, sig, v, near) {
      NS.stats.generated++;
      used.keys.add(key); used.sigs.add(sig);
      p.uid = uid('p'); p.skill = skillId; p.c = c; p.tag = sk.tag; p.key = key; p.sig = sig;
      p.verify = { status: v.status, issues: v.issues }; p.source = 'generated'; p.nearRepeat = !!near;
      return p;
    }
  };

  /* ---------------- multiple choice ----------------
     The choices come from the games' question bank: the key plus three wrong answers that the independent
     verifier REJECTS for this exact printed problem (sign slips, off-by-one, reciprocal slopes, …), so a
     choice can never be a second right answer. Only one-part problems with a verified, non-graph answer
     become multiple choice; anything else stays short answer and is flagged. */
  function mcSource(p) { return JSON.stringify([p.prompt || '', (p.parts || []).map(function (x) { return [x.prompt || '', x.answer || '']; }), p.fig || null, p.work || null]); }
  function choicesFor(p) {
    var GB = G.MKGAMES, rng = WS.rng.make(WS.rng.hash('mc|' + mcSource(p))), ds;
    // "(any point in the overlap)" and similar notes are for open answers; a choice is just the value
    var bare = p.parts[0].answer.replace(/\s*\((any|for example)[^)]*\)\s*$/, '');
    if (bare !== p.parts[0].answer && GB.answerOk(p, 0, bare).ok) p.parts[0].answer = bare;
    try { ds = GB.distractors(p, 0, rng, 3); } catch (e) { ds = []; }
    if (ds.length < 3) return null;
    var opts = rng.shuffle([p.parts[0].answer].concat(ds));
    return { opts: opts, key: opts.indexOf(p.parts[0].answer), src: mcSource(p) };
  }
  /* One-part versions of a problem that can be asked as multiple choice: the problem itself, the same problem
     without "and graph" (choices are written answers), or ONE part of a multi-part problem (its question is added
     to the prompt). Each version is verified again on its own before it is used. */
  function mcCandidates(p) {
    var out = [];
    function clean(q) { return JSON.parse(JSON.stringify(q)); }
    if (p.parts.length === 1) {
      if (!p.parts[0].answerFig) out.push({ p: p });
      else if (/^\s*(Solve|Write|Find)/i.test(p.prompt || '')) { var g = clean(p); delete g.parts[0].answerFig;   // "Graph …" questions ARE the graphing: they stay short answer
        g.prompt = g.prompt.replace(/,?\s*and graph (the solution|the solutions|it)( on a number line)?/i, '').replace(/^Graph the solution(s)? (of|to) /i, 'Solve ');
        if (g.fig && Array.isArray(g.fig.pieces) && !g.fig.pieces.length) delete g.fig;   // the blank number line is not needed
        out.push({ p: g, note: 'Asked without the graph.' }); }
    } else {
      for (var k = p.parts.length - 1; k >= 0; k--) {
        var q = clean(p), pt = q.parts[k]; if (pt.answerFig || !pt.prompt) continue;   // only parts with their own question
        pt.label = ''; q.parts = [pt];   // the part's own question prints after the prompt, work lines and figure
        out.push({ p: q, note: 'Made from part (' + (p.parts[k].label || k + 1) + ') of a multi-part problem.' });
      }
    }
    return out;
  }
  NS.makeChoices = function (p) {
    var GB = G.MKGAMES;
    if (!GB || !GB.distractors) return { fail: 'The multiple-choice builder is not loaded.' };
    if (!p || p.failed) return { fail: 'No problem yet.' };
    if (!p.verify || p.verify.status !== 'verified') return { fail: 'The answer is not verified, so no choices were made.' };
    var cands = mcCandidates(p);
    for (var i = 0; i < cands.length; i++) {
      var q = cands[i].p;
      if (q !== p) { var v = NS.verifyProblem(q, { intOnly: false }); if (!v.ok) continue; q.verify = { status: v.status, issues: v.issues }; }
      var m = choicesFor(q);
      if (m) { if (q !== p) { m.derived = q; m.note = cands[i].note; } return m; }
    }
    return { fail: cands.length ? 'There are not enough checked wrong answers for this problem, so it stays short answer.' : 'The answer is a graph, so it stays short answer.' };
  };
  /* Use a derived one-part version in place of the original problem (same slot, uid and flags). */
  function adopt(p, m) {
    var q = m.derived; delete m.derived;
    ['prompt', 'parts', 'fig', 'verify'].forEach(function (k) { if (q[k] === undefined) delete p[k]; else p[k] = q[k]; });
    p.mcNote = m.note; p.key = NS.studentText(p).replace(/\s+/g, '') + (p.fig ? '|fig:' + JSON.stringify(p.fig) : '');
    m.src = mcSource(p); p.mc = m; delete p.mcFail; return p;
  }
  /* Can this skill at this difficulty usually be asked as multiple choice? (sampled once, then cached) */
  var mcCache = {};
  NS.mcCapable = function (setId, skillId, c) {
    var k = setId + '|' + skillId + '|' + c; if (mcCache[k] !== undefined) return mcCache[k];
    var ok = 0, n = 0;
    for (var i = 0; i < 6; i++) { var p = NS.generateProblem(setId, skillId, c, { intOnly: c <= 5, level: 'x' }, 'mccap|' + i, null); if (p.failed) continue; n++; if (!NS.makeChoices(p).fail) ok++; }
    return (mcCache[k] = n > 0 && ok * 2 >= n);
  };
  /* Re-check stored choices against the problem: exactly the key is accepted by the verifier. */
  NS.checkChoices = function (p) {
    var GB = G.MKGAMES; if (!p || !p.mc || !GB || !GB.answerOk) return false;
    if (p.mc.src !== mcSource(p) || !p.mc.opts || p.mc.opts.length < 2) return false;
    return p.mc.opts.every(function (a, i) { var ok; try { ok = GB.answerOk(p, 0, a).ok; } catch (e) { ok = false; } return i === p.mc.key ? ok : !ok; });
  };
  function applyFormat(p, fmt) {
    if (!p || p.failed) return p;
    if (fmt !== 'mc') { delete p.mc; delete p.mcFail; return p; }
    if (p.mc && p.mc.src === mcSource(p)) { delete p.mcFail; return p; }
    var m = NS.makeChoices(p);
    if (m.fail) { delete p.mc; p.mcFail = m.fail; } else if (m.derived) { if (p.edited || p.manual) { delete p.mc; p.mcFail = 'Edited problems must have one part to be multiple choice.'; } else adopt(p, m); } else { p.mc = m; delete p.mcFail; }
    return p;
  }
  /* Every item matches its section's question format (after moves, edits and loading a file). */
  NS.ensureFormats = function (state) {
    state.versions.forEach(function (v) { v.sections.forEach(function (s, si) { var f = NS.sectionFormat(state.config, si); s.items.forEach(function (it) { applyFormat(it, f); }); }); });
  };
  /* Generate for a section: in a multiple-choice section, keep trying fresh problems until one makes good choices. */
  function formatted(state, si, gen) {
    var p = gen(0);
    if (p.failed || si === undefined || si === null || NS.sectionFormat(state.config, si) !== 'mc') return p;
    var best = p;
    for (var t = 0; t < 10; t++) {
      if (t > 0) { var q = gen(t); if (q.failed) break; p = q; }
      var m = NS.makeChoices(p);
      if (!m.fail) { if (m.derived) return adopt(p, m); p.mc = m; delete p.mcFail; return p; }
      if (t === 0) { best = p; best.mcFail = m.fail; }
    }
    return best;
  }

  /* ---------------- assessment state ---------------- */
  var LABELS = ['A', 'B', 'C'];
  function usedSets(state, skipUid) {
    var u = { keys: new Set(), sigs: new Set() };
    state.versions.forEach(function (v) { v.sections.forEach(function (s) { s.items.forEach(function (it) { if (it.uid !== skipUid && it.key) { u.keys.add(it.key); u.sigs.add(it.sig); } }); }); });
    return u;
  }
  function placeholder(slot, skill, c, tag, reason) {
    return { uid: uid('p'), slot: slot, skill: skill, c: c, tag: tag, failed: true, reason: reason, prompt: '', parts: [], steps: [], verify: { status: 'manual', issues: [reason] } };
  }
  function makeItem(state, slot, skill, c, salt, vIdx, si) {
    var cfg = state.config, set = sets[cfg.unitId];
    var p = formatted(state, si, function (t) { return NS.generateProblem(cfg.unitId, skill, c, policyOf(cfg), [cfg.seed, vIdx, slot, salt].join('|') + (t ? '|mc' + t : ''), usedSets(state)); });
    if (p.failed) return placeholder(slot, skill, c, set.byId[skill] ? set.byId[skill].tag : '', 'Could not make a verified ' + (set.byId[skill] ? set.byId[skill].name.toLowerCase() : skill) + ' problem at this difficulty (' + p.reason + '). Write your own or pick another skill.');
    p.slot = slot; return p;
  }

  /* Plan: which skill goes in each slot. Each section prefers the skills that suit its tier
     (simple one-step skills for Appetizers, multi-step and multi-part skills for Chef's Specials),
     rotates through them for balance, and then the whole menu is patched so every required skill
     category appears somewhere. Every version uses the same plan. */
  function planMenu(cfg, counts) {
    var set = sets[cfg.unitId], plans = [];
    cfg.sections.forEach(function (sec, si) {
      var skills = NS.sectionSkills(cfg, si), n = counts[si], out = [];
      if (!skills.length) { plans.push(out); return; }
      var tier = sec.tier !== undefined ? sec.tier : Math.min(si, 2);
      var rng = WS.rng.make(WS.rng.hash([cfg.seed, 'plan', si].join('|')));
      var good = rng.shuffle(skills.filter(function (id) { var b = set.byId[id].best; return !b || b.indexOf(tier) >= 0; }));
      var rest = rng.shuffle(skills.filter(function (id) { return good.indexOf(id) < 0; }));
      var order = good.concat(rest);
      // spread tags: avoid two dishes of the same category next to each other when possible
      for (var i = 0; i < n; i++) out.push(order[i % (good.length && n <= good.length * 2 ? good.length : order.length)]);
      if (NS.sectionFormat(cfg, si) === 'mc' && G.MKGAMES) {   // multiple choice: use skills that make good choices at that difficulty
        var rot = 0;
        out = out.map(function (id, i) {
          var ci = NS.itemC(cfg, si, i, n); if (NS.mcCapable(cfg.unitId, id, ci)) return id;
          for (var k = 0; k < order.length; k++) { var alt = order[(rot + k) % order.length]; if (NS.mcCapable(cfg.unitId, alt, ci)) { rot = (rot + k + 1) % order.length; return alt; } }
          return id;
        });
      }
      plans.push(out);
    });
    // coverage: make sure each required tag is offered at least once
    var tags = NS.coverageTags(cfg, null);
    tags.forEach(function (t) {
      var has = plans.some(function (pl) { return pl.some(function (id) { return set.byId[id].tag === t; }); });
      if (has) return;
      for (var si = 0; si < plans.length && !has; si++) {
        var cand = NS.sectionSkills(cfg, si).filter(function (id) { return set.byId[id].tag === t; });
        if (!cand.length) continue;
        // replace a repeated skill (or the last slot) in this section
        var pl = plans[si], seen = {}, at = -1;
        pl.forEach(function (id, k) { if (seen[id] && at < 0) at = k; seen[id] = 1; });
        if (at < 0) at = pl.length - 1;
        if (at >= 0) { pl[at] = cand[0]; has = true; }
      }
    });
    return plans;
  }
  function planSection(cfg, si, count) {
    var counts = cfg.sections.map(function (s, k) { return k === si ? count : Math.max(0, s.offered | 0); });
    return planMenu(cfg, counts)[si];
  }

  NS.newAssessment = function (cfg) {
    var state = { config: cfg, versions: [], bank: { items: [] }, created: new Date().toISOString() };
    NS.syncStructure(state, true);
    return state;
  };

  /* Make every version match the configuration: same sections, same number of slots,
     same skill + difficulty in each slot. Generates only what is missing. */
  NS.syncStructure = function (state, fresh) {
    var cfg = state.config, nV = Math.max(1, Math.min(3, cfg.versions | 0 || 1));
    if (fresh) state.versions = [];
    while (state.versions.length < nV) state.versions.push({ label: LABELS[state.versions.length], sections: [] });
    state.versions.length = nV;
    var A = state.versions[0];
    // sections follow cfg.sections by id
    state.versions.forEach(function (v) {
      v.sections = cfg.sections.map(function (s) { var old = v.sections.filter(function (x) { return x.id === s.id; })[0]; return old || { id: s.id, items: [] }; });
    });
    cfg.sections.forEach(function (sec, si) {
      var want = Math.max(0, sec.offered | 0), items = A.sections[si].items;
      // drop slots from the end (unpinned, unedited first) if there are too many
      while (items.length > want) {
        var k = -1; for (var j = items.length - 1; j >= 0; j--) if (!items[j].pinned && !items[j].edited) { k = j; break; }
        if (k < 0) k = items.length - 1;
        var slot = items[k].slot;
        state.versions.forEach(function (v) { v.sections[si].items = v.sections[si].items.filter(function (it) { return it.slot !== slot; }); });
        items = A.sections[si].items;
      }
      if (items.length < want) {
        var plan = planSection(cfg, si, want);
        for (var i = items.length; i < want; i++) {
          var slotId = uid('s'), c = NS.itemC(cfg, si, i, want), skill = plan[i];
          if (!skill) continue;
          state.versions.forEach(function (v, vi) { v.sections[si].items.push(makeItem(state, slotId, skill, c, 0, vi, si)); });
          items = A.sections[si].items;
        }
      }
      // later versions: make sure every slot of A exists, in the same order
      for (var vi = 1; vi < state.versions.length; vi++) {
        var vs = state.versions[vi].sections[si];
        vs.items = A.sections[si].items.map(function (a) {
          var mine = vs.items.filter(function (x) { return x.slot === a.slot; })[0];
          if (mine && mine.skill === a.skill && mine.c === a.c) { mine.required = a.required; return mine; }
          var n = makeItem(state, a.slot, a.skill, a.c, 0, vi, si); n.required = a.required; return n;
        });
      }
    });
    if (NS.isTest(cfg)) cfg.sections.forEach(function (s) { s.required = s.offered; });
    NS.ensureFormats(state);
    return state;
  };

  function find(state, vIdx, uidStr) {
    var v = state.versions[vIdx];
    for (var si = 0; si < v.sections.length; si++) for (var i = 0; i < v.sections[si].items.length; i++) if (v.sections[si].items[i].uid === uidStr) return { v: vIdx, si: si, i: i, item: v.sections[si].items[i] };
    return null;
  }
  NS.find = find;
  function slotItems(state, slot) {
    var out = []; state.versions.forEach(function (v, vi) { v.sections.forEach(function (s, si) { s.items.forEach(function (it, i) { if (it.slot === slot) out.push({ v: vi, si: si, i: i, item: it }); }); }); });
    return out;
  }
  function replaceAt(state, loc, item) { var old = state.versions[loc.v].sections[loc.si].items[loc.i]; item.slot = old.slot; item.required = old.required; state.versions[loc.v].sections[loc.si].items[loc.i] = item; return item; }

  /* Content operations: one version only. */
  NS.regenerate = function (state, vIdx, uidStr) {
    var loc = find(state, vIdx, uidStr); if (!loc) return null;
    var it = loc.item, salt = Math.floor(Math.random() * 1e9);
    var used = usedSets(state, null);  // includes the old one, so it is never handed back
    var cfg = state.config, p = formatted(state, loc.si, function (t) { return NS.generateProblem(cfg.unitId, it.skill, it.c, policyOf(cfg), [cfg.seed, vIdx, it.slot, salt, t].join('|'), used); });
    if (p.failed) return { failed: true, reason: p.reason };
    return replaceAt(state, loc, p);
  };
  NS.regenerateAll = function (state, vIdx) {
    var count = 0, skipped = 0;
    state.versions.forEach(function (v, vi) {
      if (vIdx !== undefined && vIdx !== null && vi !== vIdx) return;
      v.sections.forEach(function (s) { s.items.slice().forEach(function (it) {
        if (it.pinned || it.edited || it.manual) { skipped++; return; }
        var r = NS.regenerate(state, vi, it.uid); if (r && !r.failed) count++;
      }); });
    });
    return { regenerated: count, kept: skipped };
  };
  NS.togglePin = function (state, vIdx, uidStr) { var loc = find(state, vIdx, uidStr); if (loc) loc.item.pinned = !loc.item.pinned; return loc && loc.item.pinned; };

  /* Structure operations: applied to the same slot in every version, so versions stay parallel. */
  NS.setDifficulty = function (state, vIdx, uidStr, c) {
    var loc = find(state, vIdx, uidStr); if (!loc) return;
    c = Math.max(NS.MIN_C, Math.min(NS.MAX_C, c));
    slotItems(state, loc.item.slot).forEach(function (l) {
      var cfg = state.config, r0 = Math.random(), p = formatted(state, l.si, function (t) { return NS.generateProblem(cfg.unitId, l.item.skill, c, policyOf(cfg), [cfg.seed, l.v, l.item.slot, 'c' + c, r0, t].join('|'), usedSets(state, l.item.uid)); });
      replaceAt(state, l, p.failed ? placeholder(l.item.slot, l.item.skill, c, l.item.tag, p.reason) : p);
    });
  };
  NS.changeSkill = function (state, vIdx, uidStr, skillId) {
    var loc = find(state, vIdx, uidStr); if (!loc) return;
    slotItems(state, loc.item.slot).forEach(function (l) {
      var cfg = state.config, r0 = Math.random(), p = formatted(state, l.si, function (t) { return NS.generateProblem(cfg.unitId, skillId, l.item.c, policyOf(cfg), [cfg.seed, l.v, l.item.slot, skillId, r0, t].join('|'), usedSets(state, l.item.uid)); });
      var set = sets[cfg.unitId];
      replaceAt(state, l, p.failed ? placeholder(l.item.slot, skillId, l.item.c, set.byId[skillId].tag, p.reason) : p);
    });
  };
  NS.setRequired = function (state, vIdx, uidStr, on) {
    var loc = find(state, vIdx, uidStr); if (!loc) return;
    slotItems(state, loc.item.slot).forEach(function (l) { l.item.required = !!on; });
  };
  NS.moveItem = function (state, vIdx, uidStr, toSection, toIndex) {
    var loc = find(state, vIdx, uidStr); if (!loc) return;
    var slot = loc.item.slot, cfg = state.config;
    state.versions.forEach(function (v) {
      var from = v.sections[loc.si].items, k = -1; from.forEach(function (it, i) { if (it.slot === slot) k = i; });
      if (k < 0) return;
      var it = from.splice(k, 1)[0], dest = v.sections[toSection].items;
      var at = toIndex === undefined || toIndex === null ? dest.length : Math.max(0, Math.min(dest.length, toIndex));
      dest.splice(at, 0, it);
    });
    cfg.sections[loc.si].offered = state.versions[0].sections[loc.si].items.length;
    cfg.sections[toSection].offered = state.versions[0].sections[toSection].items.length;
    if (cfg.sections[loc.si].required > cfg.sections[loc.si].offered) cfg.sections[loc.si].required = cfg.sections[loc.si].offered;
    if (NS.isTest(cfg)) cfg.sections.forEach(function (s) { s.required = s.offered; });
    NS.ensureFormats(state);   // a question moved into a multiple-choice part gets choices (or a flag)
  };
  NS.reorder = function (state, vIdx, uidStr, delta) {
    var loc = find(state, vIdx, uidStr); if (!loc) return;
    NS.moveItem(state, vIdx, uidStr, loc.si, loc.i + delta);
  };
  NS.deleteItem = function (state, vIdx, uidStr) {
    var loc = find(state, vIdx, uidStr); if (!loc) return null;
    var slot = loc.item.slot, removed = [];
    state.versions.forEach(function (v) { v.sections[loc.si].items = v.sections[loc.si].items.filter(function (it) { if (it.slot === slot) { removed.push(it); return false; } return true; }); });
    var sec = state.config.sections[loc.si];
    sec.offered = state.versions[0].sections[loc.si].items.length;
    if (sec.required > sec.offered) sec.required = sec.offered;
    if (NS.isTest(state.config)) sec.required = sec.offered;
    return { section: loc.si, index: loc.i, items: removed };
  };
  NS.undoDelete = function (state, info) {
    if (!info) return;
    state.versions.forEach(function (v, vi) { if (info.items[vi]) v.sections[info.section].items.splice(info.index, 0, info.items[vi]); });
    state.config.sections[info.section].offered = state.versions[0].sections[info.section].items.length;
    if (NS.isTest(state.config)) state.config.sections[info.section].required = state.config.sections[info.section].offered;
  };
  NS.addItem = function (state, si, skillId, c) {
    var slot = uid('s'), cfg = state.config;
    if (c === undefined || c === null) c = NS.sectionC(cfg, si);
    state.versions.forEach(function (v, vi) { v.sections[si].items.push(makeItem(state, slot, skillId, c, 'add' + Math.random(), vi, si)); });
    cfg.sections[si].offered = state.versions[0].sections[si].items.length;
    if (NS.isTest(cfg)) cfg.sections[si].required = cfg.sections[si].offered;
    return state.versions[0].sections[si].items[cfg.sections[si].offered - 1];
  };
  /* A teacher-written problem. The same text is placed in every version (edit each one if you like). */
  NS.addManual = function (state, si, data) {
    var slot = uid('s');
    state.versions.forEach(function (v) {
      var p = NS.buildEdited(data, null); p.slot = slot; p.manual = true; v.sections[si].items.push(p);
    });
    state.config.sections[si].offered = state.versions[0].sections[si].items.length;
    if (NS.isTest(state.config)) state.config.sections[si].required = state.config.sections[si].offered;
    NS.ensureFormats(state);
    return state.versions[0].sections[si].items[state.versions[0].sections[si].items.length - 1];
  };

  /* ---------------- editing ---------------- */
  /* data: {prompt, parts:[{label, prompt, answer, checkType, checkMath, checkVar, values}], tag, c, steps:[text...]}
     The edited problem is re-verified from scratch. Generated answers are NOT trusted after an edit. */
  NS.buildEdited = function (data, original, policy) {
    var p = {
      uid: uid('p'), skill: original ? original.skill : (data.skill || 'custom'), c: data.c || (original ? original.c : 4),
      tag: data.tag || (original ? original.tag : 'CUSTOM'), prompt: data.prompt || '', variant: 'edited',
      parts: (data.parts || []).map(function (pt) {
        var chk = null;
        if (pt.keepCheck) chk = JSON.parse(JSON.stringify(pt.keepCheck));   // word-problem checks re-read the edited text
        else if (pt.checkType && pt.checkType !== 'none') {
          chk = { type: pt.checkType, v: pt.checkVar || 'x' };
          if (pt.checkType === 'simplify' || pt.checkType === 'evaluate') chk.expr = pt.checkMath; else chk.eq = pt.checkMath;
          if (pt.checkType === 'evaluate') chk.values = pt.values || {};
        }
        return { label: pt.label || '', prompt: pt.prompt || '', answer: pt.answer || '', check: chk };
      }),
      steps: (data.steps || []).map(function (s) { return typeof s === 'string' ? { t: s, m: '', w: 1 } : s; }),
      space: original ? original.space : [1.2, 1.5, 1.8], edited: true, pinned: true, source: original ? 'edited' : 'manual'
    };
    var v = NS.verifyProblem(p, policy || { intOnly: false });
    p.verify = { status: v.status, issues: v.issues, computed: v.computed };
    p.approved = v.status === 'verified';
    p.key = (NS.studentText(p) || '').replace(/\s+/g, '') + '|edited';
    p.sig = 'edited|' + p.uid;
    return p;
  };
  NS.applyEdit = function (state, vIdx, uidStr, data) {
    var loc = find(state, vIdx, uidStr); if (!loc) return null;
    var p = NS.buildEdited(data, loc.item, policyOf(state.config));
    replaceAt(state, loc, p); applyFormat(p, NS.sectionFormat(state.config, loc.si));   // choices are rebuilt from the edited problem
    return p;
  };
  NS.approve = function (state, vIdx, uidStr, on) { var loc = find(state, vIdx, uidStr); if (loc) loc.item.approved = !!on; };

  /* ---------------- problem bank ---------------- */
  NS.fillBank = function (state, skillId, c, n) {
    var cfg = state.config, used = usedSets(state), items = [], fails = 0;
    state.bank.items.forEach(function (b) { used.keys.add(b.key); used.sigs.add(b.sig); });
    for (var i = 0; i < n; i++) {
      var p = NS.generateProblem(cfg.unitId, skillId, c, policyOf(cfg), [cfg.seed, 'bank', skillId, c, i, Math.random()].join('|'), used);
      if (p.failed) fails++; else items.push(p);
    }
    state.bank = { skill: skillId, c: c, items: items };
    return { made: items.length, failed: fails };
  };
  /* Put a bank problem into a section (version A). Other versions get a parallel problem of the same skill & difficulty. */
  NS.useBankItem = function (state, bankUid, si) {
    var k = -1; state.bank.items.forEach(function (b, i) { if (b.uid === bankUid) k = i; });
    if (k < 0) return null;
    var b = state.bank.items.splice(k, 1)[0], slot = uid('s');
    b.slot = slot; b.pinned = true; b.source = 'bank';
    state.versions.forEach(function (v, vi) {
      if (vi === 0) v.sections[si].items.push(b);
      else v.sections[si].items.push(makeItem(state, slot, b.skill, b.c, 'bank' + Math.random(), vi, si));
    });
    state.config.sections[si].offered = state.versions[0].sections[si].items.length;
    if (NS.isTest(state.config)) state.config.sections[si].required = state.config.sections[si].offered;
    NS.ensureFormats(state);
    return b;
  };

  /* Re-plan the menu after the teacher changes level, skills or section difficulty.
     Slots that are pinned or edited in ANY version keep their skill, difficulty and problems;
     every other slot gets the planned skill and the section's difficulty and is regenerated. */
  NS.rebuild = function (state) {
    var cfg = state.config, kept = 0, rebuilt = 0;
    NS.syncStructure(state);
    cfg.sections.forEach(function (sec, si) {
      var nItems = state.versions[0].sections[si].items.length, plan = planSection(cfg, si, nItems);
      state.versions[0].sections[si].items.forEach(function (a, i) {
        var c = NS.itemC(cfg, si, i, nItems);
        var locs = slotItems(state, a.slot);
        if (locs.some(function (l) { return l.item.pinned || l.item.edited || l.item.manual; })) { kept++; return; }
        var skill = plan[i] || a.skill;
        locs.forEach(function (l) {
          var r0 = Math.random(), p = formatted(state, si, function (t) { return NS.generateProblem(cfg.unitId, skill, c, policyOf(cfg), [cfg.seed, l.v, a.slot, 'rb', r0, t].join('|'), usedSets(state, l.item.uid)); });
          var set = sets[cfg.unitId];
          replaceAt(state, l, p.failed ? placeholder(a.slot, skill, c, set.byId[skill].tag, p.reason) : p);
        });
        rebuilt++;
      });
    });
    return { kept: kept, rebuilt: rebuilt };
  };

  /* ---------------- versions ---------------- */
  NS.setVersionCount = function (state, n) { state.config.versions = Math.max(1, Math.min(3, n | 0)); NS.syncStructure(state); };
  NS.regenerateVersion = function (state, vIdx) { return NS.regenerateAll(state, vIdx); };

  /* ---------------- summaries ---------------- */
  NS.counts = function (state) {
    var v = state.versions[0], cfg = state.config, out = { offered: 0, problems: 0, unverified: 0, failed: 0, pinned: 0, edited: 0 };
    state.versions.forEach(function (ver) { ver.sections.forEach(function (s) { s.items.forEach(function (it) {
      out.problems++; if (it.failed) out.failed++; else if (it.verify && it.verify.status !== 'verified' && !it.approved) out.unverified++;
      if (it.pinned) out.pinned++; if (it.edited) out.edited++;
    }); }); });
    v.sections.forEach(function (s) { out.offered += s.items.length; });
    return out;
  };
  /* Anything that would make printing unsafe. */
  NS.blockers = function (state) {
    var list = [], rules = NS.checkRules(state.config, state);
    rules.errors.forEach(function (e) { list.push(e); });
    state.versions.forEach(function (ver) { ver.sections.forEach(function (s, si) { s.items.forEach(function (it, i) {
      var where = 'Version ' + ver.label + ', ' + (state.config.sections[si].name) + ' #' + (i + 1);
      if (it.failed) list.push(where + ': no verified problem yet.');
      else if (it.verify && it.verify.status !== 'verified' && !it.approved) list.push(where + ': answer needs your approval.');
    }); }); });
    return list;
  };

  /* ---------------- save / load ---------------- */
  NS.serialize = function (state) {
    return JSON.stringify({ format: 'mk-menu-assessment', schema: 1, saved: new Date().toISOString(), config: state.config, versions: state.versions }, null, 1);
  };
  NS.deserialize = function (text) {
    var o = typeof text === 'string' ? JSON.parse(text) : text;
    if (!o || o.format !== 'mk-menu-assessment') throw new Error('This file is not a Menu Assessment save file.');
    if (!sets[o.config.unitId]) throw new Error('This save file is for a unit this generator does not support yet (' + o.config.unitId + ').');
    var state = { config: o.config, versions: o.versions || [], bank: { items: [] } };
    if (!state.config.mode) state.config.mode = 'menu';
    // re-verify everything on load: a hand-edited file cannot slip in a wrong key
    var pol = policyOf(state.config);
    state.versions.forEach(function (v) { v.sections.forEach(function (s) { s.items.forEach(function (it) {
      if (it.failed) return;
      var r = NS.verifyProblem(it, pol); var was = it.verify && it.verify.status;
      it.verify = { status: r.status, issues: r.issues, computed: r.computed };
      if (r.status !== 'verified' && was === 'verified') it.approved = false;
      if (it.mc && !NS.checkChoices(it)) delete it.mc;   // stored choices are re-checked; a changed key or choice is rebuilt
    }); }); });
    NS.syncStructure(state);
    return state;
  };
  NS.duplicate = function (state) {
    var s = NS.deserialize(NS.serialize(state));
    s.config.title = (s.config.title || '') + ' (copy)';
    return s;
  };
})(typeof window !== 'undefined' ? window : globalThis);
