/* Generator framework: lesson registry, difficulty / number-mode controls, validated
   problem creation (generate -> verify -> de-duplicate -> retry), and worksheet assembly.

   Nothing here is specific to Linear Functions. A new unit registers itself with
   NS.registerUnit(...) and NS.registerLesson(...). A future spiral-review generator can call
   NS.buildWorksheet({lessons:{<any registered lesson id>: count, ...}}) across units. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, gcd = NS.frac.gcd;

  var registry = NS.registry = { units: {}, lessons: {} };

  NS.registerUnit = function (u) { registry.units[u.id] = u; return u; };
  NS.registerLesson = function (l) {
    if (registry.lessons[l.id]) throw new Error('duplicate lesson id ' + l.id);
    l.layout = l.layout || 'half';
    l.space = l.space || [0.25, 0.7, 1.4];
    registry.lessons[l.id] = l; return l;
  };

  /* ---------- difficulty and number preferences ---------- */
  var DIFF = {
    basic:    { maxSlope: 4, maxNum: 3, maxDen: 3, maxB: 6,  lim: 6,  posBias: 0.65 },
    standard: { maxSlope: 6, maxNum: 5, maxDen: 4, maxB: 9,  lim: 9,  posBias: 0.5 },
    honors:   { maxSlope: 9, maxNum: 7, maxDen: 6, maxB: 12, lim: 12, posBias: 0.5 }
  };
  var FRAC_CHANCE = {
    integers:  { basic: 0,    standard: 0,    honors: 0 },
    preferred: { basic: 0.15, standard: 0.25, honors: 0.3 },
    fractions: { basic: 0.45, standard: 0.55, honors: 0.6 }
  };

  function Reject(msg) { this.message = msg; this.isReject = true; }
  var gen = NS.gen = {
    Reject: Reject,
    need: function (cond, msg) { if (!cond) throw new Reject(msg || 'constraint'); },

    /* A nonzero slope that respects difficulty and number mode.
       o: {int:true -> integer only, unit:true -> numerator 1 only, sign:+1/-1} */
    slope: function (ctx, o) {
      o = o || {};
      var rng = ctx.rng, sign = o.sign || (rng.chance(ctx.D.posBias) ? 1 : -1);
      var useFrac = !o.int && (o.unit ? true : rng.chance(ctx.fracChance));
      if (useFrac) {
        var d, n, tries = 0;
        do {
          d = rng.int(2, ctx.D.maxDen);
          n = o.unit ? 1 : rng.int(1, ctx.D.maxNum);
          tries++;
        } while (gcd(n, d) !== 1 && tries < 50);
        gen.need(gcd(n, d) === 1);
        return new Fr(sign * n, d);
      }
      return new Fr(sign * rng.int(1, ctx.D.maxSlope), 1);
    },
    /* Integer y-intercept within +-maxB (or +-o.max). */
    intercept: function (ctx, o) {
      o = o || {}; var mx = o.max || ctx.D.maxB;
      var b = ctx.rng.int(-mx, mx);
      if (!o.allowZero && b === 0) b = ctx.rng.sign() * ctx.rng.int(1, mx);
      return b;
    },
    /* Count lattice points (integer x and integer y) of y = m x + b inside |x|,|y| <= w. */
    latticeCount: function (m, b, w) {
      m = Fr.of(m); b = Fr.of(b); var c = 0;
      for (var x = -w; x <= w; x++) {
        var y = m.mul(x).add(b);
        if (y.isInt() && Math.abs(y.n) <= w) c++;
      }
      return c;
    },
    inRange: function (v, lim) { return Math.abs(v) <= lim; }
  };

  /* ---------- settings ---------- */
  NS.defaultSettings = function () {
    return {
      title: '', showNameDate: true, difficulty: 'standard', numberMode: 'preferred',
      grids: true, space: 'standard', answerKey: true, keyMode: 'worked',
      versions: 1, seed: Math.floor(Math.random() * 1e9), lessons: {}, salts: {}, pinned: null
    };
  };
  var SPACE_IDX = { compact: 0, standard: 1, extended: 2 };
  NS.spaceIndex = function (s) { return SPACE_IDX[s] === undefined ? 1 : SPACE_IDX[s]; };

  function makeCtx(settings, lesson, slot, rng, stable) {
    var d = settings.difficulty in DIFF ? settings.difficulty : 'standard';
    var mode = settings.numberMode in FRAC_CHANCE ? settings.numberMode : 'preferred';
    return {
      rng: rng, slot: slot, lessonId: lesson.id, difficulty: d, numberMode: mode, stable: stable || 0,
      grids: settings.grids !== false, D: DIFF[d], fracChance: FRAC_CHANCE[mode][d],
      allowFracIntercept: mode === 'fractions' && d !== 'basic'
    };
  }

  /* ---------- problem creation ---------- */
  /* used = {keys:Set, equiv:Set} shared by a worksheet so problems do not repeat.
     scope identifies the version, so "equivalent" problems are only avoided within one worksheet. */
  NS.makeProblem = function (lessonId, settings, slot, salt, used, scope) {
    var lesson = registry.lessons[lessonId];
    if (!lesson) throw new Error('unknown lesson ' + lessonId);
    used = used || { keys: new Set(), equiv: new Set(), vk: {} };
    if (!used.vk) used.vk = {};
    var base = NS.rng.make(NS.rng.hash([settings.seed, scope || 0, lessonId, slot, salt || 0].join('|')));
    var lastReason = '', fbCross = null, fbAny = null;
    function accept(p, ek, attempt, repeat) {
      used.keys.add(p.key); used.equiv.add(ek); (used.vk[scope] || (used.vk[scope] = new Set())).add(p.key);
      p.lessonId = lessonId; p.slot = slot; p.salt = salt || 0; p.attempts = attempt + 1; p.repeat = !!repeat;
      p.steps = p.steps || [];
      p.figWhere = p.figWhere || (p.fig ? (lesson.layout === 'row' ? 'right' : 'below') : 'none');
      p._ek = ek;
      return p;
    }
    // `stable` is the same for every slot of one lesson in one version, so lessons can rotate
    // through sub-types by slot (A, B, C versions line up) without relying on random draws.
    var stable = NS.rng.hash([settings.seed, 'rot', lessonId].join('|')) % 9973;
    for (var attempt = 0; attempt < 600; attempt++) {
      var ctx = makeCtx(settings, lesson, slot, base.fork('a' + attempt), stable);
      var p;
      try { p = lesson.generate(ctx); }
      catch (e) { if (e && e.isReject) { lastReason = e.message; continue; } throw e; }
      if (!p || !p.prompt || p.answer === undefined || !p.key) continue;
      var ek = scope + '|' + lessonId + '|' + (p.equiv || p.key);
      var vk = used.vk[scope] || (used.vk[scope] = new Set());
      if (used.keys.has(p.key)) {
        // Out of fresh variety: remember a repeat as a last resort, preferring one that is new within this version.
        if (!vk.has(p.key)) { if (!fbCross) fbCross = { p: p, ek: ek }; } else if (!fbAny) fbAny = { p: p, ek: ek };
        continue;
      }
      if (attempt < 250 && used.equiv.has(ek)) continue;
      return accept(p, ek, attempt, false);
    }
    var fb = fbCross || fbAny;
    if (fb) return accept(fb.p, fb.ek, 600, true);
    throw new Error('Could not generate a valid problem for ' + lessonId + ' (' + lastReason + ')');
  };

  /* One-off helper used by tests and by a future spiral-review builder. */
  NS.generateOne = function (lessonId, opts) {
    var s = Object.assign(NS.defaultSettings(), opts || {});
    return NS.makeProblem(lessonId, s, (opts && opts.slot) || 0, (opts && opts.salt) || 0, null, 0);
  };

  /* ---------- worksheets ---------- */
  var LABELS = ['A', 'B', 'C'];

  NS.orderedLessons = function (settings, unitId) {
    // Lessons appear in unit order (category by category), not in click order.
    var out = [];
    var unit = unitId ? registry.units[unitId] : null;
    var ids = unit ? [].concat.apply([], unit.categories.map(function (c) { return c.lessons; })) : Object.keys(registry.lessons);
    ids.forEach(function (id) { var n = settings.lessons[id] | 0; if (n > 0) out.push({ id: id, count: n }); });
    return out;
  };

  /* Pinned problems: after a single-problem regenerate the whole worksheet is remembered exactly,
     so rebuilding (a reload, a setting that does not change the maths) never shuffles anything else.
     They only apply while the settings that shape the maths are unchanged. */
  function pinSig(settings) { return [settings.seed, settings.difficulty, settings.numberMode, settings.grids ? 1 : 0].join('|'); }

  NS.buildWorksheet = function (settings, unitId) {
    var plan = NS.orderedLessons(settings, unitId);
    var used = { keys: new Set(), equiv: new Set(), vk: {} };
    var pin = settings.pinned && settings.pinned.sig === pinSig(settings) ? settings.pinned.items : null;
    var versions = [];
    for (var v = 0; v < (settings.versions || 1); v++) {
      var sections = plan.map(function (pl) {
        var probs = [];
        for (var i = 0; i < pl.count; i++) {
          var pinned = pin && pin[v + '|' + pl.id + '|' + i];
          if (pinned) {
            var c = JSON.parse(JSON.stringify(pinned));
            used.keys.add(c.key); used.equiv.add(c._ek); (used.vk[v] || (used.vk[v] = new Set())).add(c.key); probs.push(c);
          } else probs.push(NS.makeProblem(pl.id, settings, i, 0, used, v));
        }
        return { lessonId: pl.id, problems: probs };
      });
      versions.push({ index: v, label: LABELS[v], sections: sections });
    }
    return { settings: JSON.parse(JSON.stringify(settings)), unitId: unitId, versions: versions };
  };

  function usedFrom(ws, skip) {
    var used = { keys: new Set(), equiv: new Set(), vk: {} };
    ws.versions.forEach(function (ver, vi) {
      ver.sections.forEach(function (sec) {
        sec.problems.forEach(function (p) { if (p !== skip) { used.keys.add(p.key); used.equiv.add(p._ek); (used.vk[vi] || (used.vk[vi] = new Set())).add(p.key); } });
      });
    });
    return used;
  }

  /* Replace exactly one problem; every other problem is untouched. */
  NS.regenerateProblem = function (ws, vIdx, sIdx, pIdx) {
    var sec = ws.versions[vIdx].sections[sIdx], old = sec.problems[pIdx];
    var used = usedFrom(ws, old);
    used.keys.add(old.key);                       // never hand back the problem being replaced
    var salt = (old.salt || 0) + 1 + Math.floor(Math.random() * 1e6);
    var np = NS.makeProblem(sec.lessonId, ws.settings, old.slot, salt, used, vIdx);
    sec.problems[pIdx] = np;
    var items = {};
    ws.versions.forEach(function (ver, v) { ver.sections.forEach(function (sc) { sc.problems.forEach(function (pr) { items[v + '|' + sc.lessonId + '|' + pr.slot] = pr; }); }); });
    ws.settings.pinned = JSON.parse(JSON.stringify({ sig: pinSig(ws.settings), items: items }));
    return np;
  };

  NS.countRepeats = function (ws) {
    var n = 0; ws.versions.forEach(function (v) { v.sections.forEach(function (s) { s.problems.forEach(function (p) { if (p.repeat) n++; }); }); }); return n;
  };

  NS.countProblems = function (ver) {
    return ver.sections.reduce(function (n, s) { return n + s.problems.length; }, 0);
  };
})(typeof window !== 'undefined' ? window : globalThis);
