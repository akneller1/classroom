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
    { course: 'Algebra 1', units: [
      ['algebra1-expressions-equations', 'Expressions & Equations'], ['algebra1-inequalities', 'Inequalities'], ['algebra1-linear-equations-slope', 'Linear Equations & Slope'],
      ['algebra1-graphing-inequalities', 'Graphing Inequalities'], ['algebra1-systems-of-equations', 'Systems of Equations'], ['algebra1-exponents-exponential-functions', 'Exponents & Exponential Functions'],
      ['algebra1-polynomials-factoring', 'Polynomials & Factoring'], ['algebra1-quadratics', 'Quadratics']] },
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
    var tier = sec.tier !== undefined ? sec.tier : Math.min(si, 2);
    var c = lv.tiers[Math.max(0, Math.min(2, tier))] + (sec.adjust || 0);
    return Math.max(NS.MIN_C, Math.min(NS.MAX_C, c));
  };

  /* ---------------- configuration ---------------- */
  var uidN = 0;
  function uid(p) { uidN++; return (p || 'id') + '-' + Date.now().toString(36) + '-' + uidN.toString(36) + '-' + Math.floor(Math.random() * 1e6).toString(36); }
  NS.uid = uid;

  NS.defaultConfig = function (setId) {
    var set = sets[setId];
    var skills = {}; if (set) set.skills.forEach(function (s) { skills[s.id] = true; });
    return {
      format: 'mk-menu-assessment', schema: 1, unitId: setId,
      title: set ? set.title : 'Assessment Menu', subtitle: 'Assessment Menu · choose your meal and show what you know',
      level: 'cp1', answers: 'auto', seed: Math.floor(Math.random() * 1e9),
      skills: skills,
      sections: [
        { id: 'app', name: 'Appetizers', note: 'Warm-ups', points: 5, offered: 6, required: 4, tier: 0, adjust: 0, skills: null },
        { id: 'ent', name: 'Entrées', note: 'Multi-step problems', points: 10, offered: 6, required: 4, tier: 1, adjust: 0, skills: null },
        { id: 'spc', name: 'Chef’s Specials', note: 'Multi-part challenges', points: 20, offered: 3, required: 2, tier: 2, adjust: 0, skills: null }
      ],
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
    cfg.sections.forEach(function (s, i) {
      var nm = s.name || 'Section ' + (i + 1);
      var o = s.offered | 0, r = s.required | 0, pts = +s.points;
      if (!(o >= 1)) errors.push(nm + ': offer at least one problem.');
      if (r < 0) errors.push(nm + ': the number required cannot be negative.');
      if (r > o) errors.push(nm + ': students must complete ' + r + ' but only ' + o + ' are offered.');
      if (!(pts > 0)) errors.push(nm + ': points per problem must be more than 0.');
      if (r === 0 && o > 0) warnings.push(nm + ': students are not required to complete any of these, so they will not count toward the score.');
      if (r === o && o > 0) warnings.push(nm + ': students must complete every problem, so there is no choice in this section.');
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
  function studentKey(p) { return NS.studentText(p).replace(/\s+/g, ''); }
  function nearSig(skill, p) {
    var nums = (NS.studentText(p).match(/\d+(?:\.\d+)?/g) || []).map(Number).map(Math.abs).sort(function (a, b) { return a - b; });
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
  function makeItem(state, slot, skill, c, salt, vIdx) {
    var cfg = state.config, set = sets[cfg.unitId];
    var p = NS.generateProblem(cfg.unitId, skill, c, policyOf(cfg), [cfg.seed, vIdx, slot, salt].join('|'), usedSets(state));
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
          var slotId = uid('s'), c = NS.sectionC(cfg, si), skill = plan[i];
          if (!skill) continue;
          state.versions.forEach(function (v, vi) { v.sections[si].items.push(makeItem(state, slotId, skill, c, 0, vi)); });
          items = A.sections[si].items;
        }
      }
      // later versions: make sure every slot of A exists, in the same order
      for (var vi = 1; vi < state.versions.length; vi++) {
        var vs = state.versions[vi].sections[si];
        vs.items = A.sections[si].items.map(function (a) {
          var mine = vs.items.filter(function (x) { return x.slot === a.slot; })[0];
          if (mine && mine.skill === a.skill && mine.c === a.c) { mine.required = a.required; return mine; }
          var n = makeItem(state, a.slot, a.skill, a.c, 0, vi); n.required = a.required; return n;
        });
      }
    });
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
    var cfg = state.config, p = NS.generateProblem(cfg.unitId, it.skill, it.c, policyOf(cfg), [cfg.seed, vIdx, it.slot, salt].join('|'), used);
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
      var cfg = state.config, p = NS.generateProblem(cfg.unitId, l.item.skill, c, policyOf(cfg), [cfg.seed, l.v, l.item.slot, 'c' + c, Math.random()].join('|'), usedSets(state, l.item.uid));
      replaceAt(state, l, p.failed ? placeholder(l.item.slot, l.item.skill, c, l.item.tag, p.reason) : p);
    });
  };
  NS.changeSkill = function (state, vIdx, uidStr, skillId) {
    var loc = find(state, vIdx, uidStr); if (!loc) return;
    slotItems(state, loc.item.slot).forEach(function (l) {
      var cfg = state.config, p = NS.generateProblem(cfg.unitId, skillId, l.item.c, policyOf(cfg), [cfg.seed, l.v, l.item.slot, skillId, Math.random()].join('|'), usedSets(state, l.item.uid));
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
    return { section: loc.si, index: loc.i, items: removed };
  };
  NS.undoDelete = function (state, info) {
    if (!info) return;
    state.versions.forEach(function (v, vi) { if (info.items[vi]) v.sections[info.section].items.splice(info.index, 0, info.items[vi]); });
    state.config.sections[info.section].offered = state.versions[0].sections[info.section].items.length;
  };
  NS.addItem = function (state, si, skillId, c) {
    var slot = uid('s'), cfg = state.config;
    if (c === undefined || c === null) c = NS.sectionC(cfg, si);
    state.versions.forEach(function (v, vi) { v.sections[si].items.push(makeItem(state, slot, skillId, c, 'add' + Math.random(), vi)); });
    cfg.sections[si].offered = state.versions[0].sections[si].items.length;
    return state.versions[0].sections[si].items[cfg.sections[si].offered - 1];
  };
  /* A teacher-written problem. The same text is placed in every version (edit each one if you like). */
  NS.addManual = function (state, si, data) {
    var slot = uid('s');
    state.versions.forEach(function (v) {
      var p = NS.buildEdited(data, null); p.slot = slot; p.manual = true; v.sections[si].items.push(p);
    });
    state.config.sections[si].offered = state.versions[0].sections[si].items.length;
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
    return replaceAt(state, loc, p);
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
      else v.sections[si].items.push(makeItem(state, slot, b.skill, b.c, 'bank' + Math.random(), vi));
    });
    state.config.sections[si].offered = state.versions[0].sections[si].items.length;
    return b;
  };

  /* Re-plan the menu after the teacher changes level, skills or section difficulty.
     Slots that are pinned or edited in ANY version keep their skill, difficulty and problems;
     every other slot gets the planned skill and the section's difficulty and is regenerated. */
  NS.rebuild = function (state) {
    var cfg = state.config, kept = 0, rebuilt = 0;
    NS.syncStructure(state);
    cfg.sections.forEach(function (sec, si) {
      var plan = planSection(cfg, si, state.versions[0].sections[si].items.length), c = NS.sectionC(cfg, si);
      state.versions[0].sections[si].items.forEach(function (a, i) {
        var locs = slotItems(state, a.slot);
        if (locs.some(function (l) { return l.item.pinned || l.item.edited || l.item.manual; })) { kept++; return; }
        var skill = plan[i] || a.skill;
        locs.forEach(function (l) {
          var p = NS.generateProblem(cfg.unitId, skill, c, policyOf(cfg), [cfg.seed, l.v, a.slot, 'rb', Math.random()].join('|'), usedSets(state, l.item.uid));
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
    // re-verify everything on load: a hand-edited file cannot slip in a wrong key
    var pol = policyOf(state.config);
    state.versions.forEach(function (v) { v.sections.forEach(function (s) { s.items.forEach(function (it) {
      if (it.failed) return;
      var r = NS.verifyProblem(it, pol); var was = it.verify && it.verify.status;
      it.verify = { status: r.status, issues: r.issues, computed: r.computed };
      if (r.status !== 'verified' && was === 'verified') it.approved = false;
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
