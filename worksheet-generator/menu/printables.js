/* Printable Generators — engine (no DOM). Maze, Color by Number, Tarsia, Error Analysis, Partner Check.
   Every problem comes from the verified skill generators (menu/skills), every answer is checked by the
   verifier, and every wrong label (maze doors, Tarsia edges, a student's wrong answer) is an answer the
   verifier REJECTS for that problem. Two problems on one printable never accept each other's answer, so a
   door, a color or a matching edge can only mean one thing.
   Needs: core/rng.js, menu engine + skills, games/bank.js (distractors and the answer checker). */
(function (G) {
  'use strict';
  var NS = G.MKMENU, WS = G.MKWS, PR = NS.printables = {};
  function GB() { return G.MKGAMES; }

  PR.KINDS = [
    { id: 'maze', name: 'Maze', blurb: 'Solve the problem in each room and leave through the door with your answer. Wrong answers lead to dead ends.' },
    { id: 'color', name: 'Color by Number', blurb: 'Solve the numbered problems, find each answer in the color code, and color the matching squares to reveal a picture.' },
    { id: 'tarsia', name: 'Tarsia Puzzle', blurb: 'Cut out the triangles and match every problem to its answer to rebuild the shape.' },
    { id: 'error', name: 'Error Analysis', blurb: 'A student solved each problem and made a mistake. Find it, explain it, and fix it.' },
    { id: 'partner', name: 'Partner Check', blurb: 'Partner A and Partner B solve different problems with the same answers, then compare.' }
  ];
  PR.kind = function (id) { return PR.KINDS.filter(function (k) { return k.id === id; })[0]; };

  /* ---------------- helpers ---------------- */
  function rngOf() { return WS.rng.make(WS.rng.hash([].slice.call(arguments).join('|'))); }
  /* Rough printed length of a string with ⟨math⟩ (fractions count as their wider part). */
  function plain(s) {
    return String(s || '').replace(/⟨([^⟩]*)⟩/g, function (m, t) {
      return t.replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, function (x, a, b) { return a.length > b.length ? a : b; })
        .replace(/\\left|\\right|\\,|\\;|\\!|\\ |\\cdot|\\quad/g, '').replace(/\\(pm|le|ge|ne|sqrt|times|div)/g, '#').replace(/\\[a-zA-Z]+/g, '').replace(/[{}^_]/g, '');
    });
  }
  PR.plain = plain;
  function nrm(a) { return String(a).replace(/\s+|⟨|⟩|\\,|\\left|\\right/g, ''); }
  function ok(p, ans) { try { return !!GB().answerOk(p, 0, ans).ok; } catch (e) { return false; } }
  /* Two problems clash when either one accepts the other's answer. */
  function clash(a, b) { return nrm(a.key) === nrm(b.key) || ok(a.p, b.key) || ok(b.p, a.key); }
  PR.clash = clash;
  function snippetsOf(s) { var m, out = [], re = /⟨([^⟩]*)⟩/g; while ((m = re.exec(s))) out.push(m[1]); return out; }

  /* One-part, verified version of a problem (graph answers become written answers), or null. */
  function onePart(p) {
    if (!p || p.failed || !p.verify || p.verify.status !== 'verified') return null;
    if (p.parts.length === 1 && !p.parts[0].answerFig) return { p: p, m: null };
    var m = NS.makeChoices(p);
    if (m.fail || !m.derived) return null;
    return { p: m.derived, m: m };
  }
  /* Wrong answers the verifier rejects for this problem (distinct, up to `want`). */
  function wrongs(p, want, seed) {
    var ds; try { ds = GB().distractors(p, 0, rngOf('w', seed, nrm(p.parts[0].answer)), want); } catch (e) { ds = []; }
    return ds.filter(function (d) { return !ok(p, d); });
  }
  /* Tarsia edges show only the math: "Verb ⟨expr⟩." prompts. */
  /* Shorter wording for a Tarsia edge (the work pages show the full problem). */
  var SHORTEN = [[/^Solve the system( by (substitution|elimination|graphing))?:\s*/, 'Solve '], [/^For (⟨[^⟩]*⟩), find (⟨[^⟩]*⟩)\.?$/, '$1; $2'],
    [/^Find the slope of the line through /, 'Slope through '], [/^Find the (\d+)(st|nd|rd|th) term of (the (geometric|arithmetic) sequence )?/, 'Term $1: '],
    [/^Find the (mean|median|range|mode) of /, '$1: '], [/^Find the mean absolute deviation \(MAD\) of /, 'MAD: '], [/^Find the interquartile range \(IQR\) of /, 'IQR: '],
    [/^Write the equation of the line with slope (⟨[^⟩]*⟩) through (⟨[^⟩]*⟩),? in slope-intercept form\.?$/, 'Line: slope $1, through $2'],
    [/^Write the equation of the line through (⟨[^⟩]*⟩) in slope-intercept form\.?$/, 'Line through $1'],
    [/^Write the equation of the horizontal line through (⟨[^⟩]*⟩)\.?$/, 'Horizontal line through $1'],
    [/^Write (⟨[^⟩]*⟩) in standard form (⟨[^⟩]*⟩) \(integers, (⟨[^⟩]*⟩)\)\.?$/, '$1 in standard form'],
    [/^Write (⟨[^⟩]*⟩) in scientific notation\.?$/, '$1 in sci. notation'], [/^Write (⟨[^⟩]*⟩) in standard form\.?$/, '$1 in standard form']];
  function tarsiaEdge(prompt) {
    var mt = TARSIA_VERB.exec(prompt);
    if (mt && mt[1] === 'Factor completely') mt[1] = 'Factor fully';
    if (mt) return (mt[1] === 'Solve' && /=|<|>|\\le|\\ge/.test(mt[2]) ? '' : mt[1] + ' ') + '⟨' + mt[2] + '⟩';
    var t = prompt;
    SHORTEN.forEach(function (r) { t = t.replace(r[0], r[1]); });
    t = t.replace(/\s*\.\s*$/, '').replace(/ and (⟨)/g, ', $1');
    if (t === prompt.replace(/\s*\.\s*$/, '') && !/^(Solve|Simplify|Factor|Evaluate)\b/.test(t)) return null;
    return t;
  }
  PR.tarsiaEdge = tarsiaEdge;
  var TARSIA_VERB = /^(Solve|Simplify|Factor completely|Factor|Evaluate|Multiply|Expand|Add|Subtract|Divide|Write in scientific notation|Write in standard form|Find the slope of)\s*:?\s*⟨([^⟩]+)⟩\s*\.?$/;
  PR.MODES = {
    maze: { prompt: 92, answer: 19, fig: false, wrong: 4, snippet: 24 },
    tarsia: { prompt: 28, answer: 15, fig: false, wrong: 2, verb: true },
    color: { prompt: 170, answer: 30, fig: true, wrong: 0 },
    error: { prompt: 170, answer: 40, fig: true, wrong: 2, steps: true },
    partner: { prompt: 170, answer: 40, fig: true, wrong: 0 }
  };
  /* Make one printable item: {p, key, wrong[], skill, c, tag, expr?, verb?} or null. */
  function makeItem(cfg, skill, c, seed, used, kind) {
    var lim = PR.MODES[kind], set = NS.skillSets[cfg.unitId];
    var p = NS.generateProblem(cfg.unitId, skill, c, NS.policyOf(cfg), seed, used);
    var o = onePart(p); if (!o) return null;
    var q = o.p, key = q.parts[0].answer;
    if (!lim.fig && q.fig) return null;
    if ((q.parts[0].prompt || '') && !lim.fig) return null;
    if (plain(key).length > lim.answer) return null;
    if (lim.snippet && snippetsOf(q.prompt).some(function (m) { return plain('⟨' + m + '⟩').length > lim.snippet; })) return null;
    var it = { p: q, key: key, skill: skill, c: c, tag: set.byId[skill].tag, wrong: [] };
    if (lim.verb) {
      var edge = tarsiaEdge(q.prompt); if (!edge || plain(edge).length > lim.prompt) return null;
      it.edge = edge;
    } else if (plain(q.prompt).length + (q.parts[0].prompt ? plain(q.parts[0].prompt).length : 0) > lim.prompt) return null;
    if (lim.steps && !(q.steps || []).some(function (s) { return s.m; })) return null;
    if (lim.wrong) {
      it.wrong = wrongs(q, Math.max(lim.wrong, 3), seed).filter(function (w) { return plain(w).length <= lim.answer + 4; });
      if (it.wrong.length < Math.min(lim.wrong, 2)) return null;
    }
    return it;
  }
  PR.makeItem = makeItem;

  /* Which selected skills can make items for this kind (sampled once, cached). */
  var capCache = {};
  PR.capable = function (unitId, skill, kind) {
    var k = unitId + '|' + skill + '|' + kind; if (capCache[k] !== undefined) return capCache[k];
    var hits = 0, cfg = { unitId: unitId, level: 'cp1', answers: 'auto' };
    [2, 3, 4, 5, 6].forEach(function (c) { for (var i = 0; i < 3; i++) if (makeItem(cfg, skill, c, 'cap|' + c + '|' + i, null, kind)) { hits++; break; } });
    return (capCache[k] = hits >= 2);
  };
  PR.skillsFor = function (cfg) {
    var set = NS.skillSets[cfg.unitId];
    return set.skills.filter(function (s) { return cfg.skills[s.id] && PR.capable(cfg.unitId, s.id, cfg.kind); }).map(function (s) { return s.id; });
  };

  /* n items with pairwise different answers; difficulty rises from the level's easiest to hardest tier. */
  function gather(cfg, vIdx, n, kind, extraOk) {
    var lv = NS.LEVELS[cfg.level] || NS.LEVELS.cp1, skills = PR.skillsFor(cfg), out = [];
    if (!skills.length) return out;
    var rng = rngOf(cfg.seed, vIdx, kind, 'plan'), order = rng.shuffle(skills.slice());
    var used = { keys: new Set(), sigs: new Set() };
    for (var i = 0; i < n; i++) {
      var c = lv.tiers[Math.min(2, Math.floor(3 * i / n))];
      for (var t = 0; t < 34; t++) {
        // the planned difficulty first, then the level's other tiers, then one or two steps easier
        var sk = order[(i + t) % order.length], cc = t < 12 ? c : t < 22 ? lv.tiers[t % 3] : Math.max(1, lv.tiers[0] - 1 - (t % 2));
        var it = makeItem(cfg, sk, cc, [cfg.seed, vIdx, kind, i, t].join('|'), used, kind);
        if (!it) continue;
        if (out.some(function (o) { return clash(o, it) || nrm(o.p.prompt) === nrm(it.p.prompt); })) continue;
        if (extraOk && !extraOk(it, out)) continue;
        out.push(it); break;
      }
    }
    return out;
  }
  PR.gather = gather;

  PR.defaultConfig = function (unitId, kind) {
    var set = NS.skillSets[unitId], skills = {};
    set.skills.forEach(function (s) { skills[s.id] = true; });
    return { format: 'mk-printable', schema: 1, unitId: unitId, kind: kind || 'maze', level: 'cp1', answers: 'auto', skills: skills,
      seed: Math.floor(Math.random() * 1e9), versions: 1, picture: 'auto', count: null };
  };

  /* =========================== MAZE =========================== */
  /* A 4 × 4 grid of rooms. The path from START (top left) to FINISH (bottom right) goes through 9–13 rooms;
     every other room is a dead end whose answer is on none of its doors. Each wall between two rooms has
     one door: on the path it shows the answer of the room it leaves; elsewhere it shows a wrong answer that
     BOTH rooms' verifiers reject. */
  function mazePath(rng, R, C, minLen, maxLen) {
    for (var tries = 0; tries < 400; tries++) {
      var path = [[0, 0]], seen = {}; seen['0,0'] = 1;
      var target = rng.int(minLen, maxLen), stuck = false;
      while (!stuck) {
        var cur = path[path.length - 1];
        if (cur[0] === R - 1 && cur[1] === C - 1) break;
        var nb = [[1, 0], [0, 1], [-1, 0], [0, -1]].map(function (d) { return [cur[0] + d[0], cur[1] + d[1]]; })
          .filter(function (q) { return q[0] >= 0 && q[1] >= 0 && q[0] < R && q[1] < C && !seen[q[0] + ',' + q[1]]; });
        // keep the finish reachable and do not arrive too early
        nb = nb.filter(function (q) { return !(q[0] === R - 1 && q[1] === C - 1) || path.length + 1 >= target; });
        if (!nb.length) { stuck = true; break; }
        var q = rng.pick(nb); path.push(q); seen[q[0] + ',' + q[1]] = 1;
        if (path.length > maxLen) { stuck = true; break; }
      }
      var end = path[path.length - 1];
      if (!stuck && end[0] === R - 1 && end[1] === C - 1 && path.length >= minLen && path.length <= maxLen) return path;
    }
    return null;
  }
  PR.buildMaze = function (cfg, vIdx) {
    var R = 4, C = 4, rng = rngOf(cfg.seed, vIdx, 'maze');
    var path = mazePath(rng, R, C, 10, 13);
    var nItems = R * C - 1, items = gather(cfg, vIdx, nItems, 'maze');
    if (items.length < nItems) return { error: 'Not enough different maze problems for these skills and level (' + items.length + ' of ' + nItems + '). Choose more skills.' };
    var onPath = {}; path.forEach(function (q, i) { onPath[q[0] + ',' + q[1]] = i; });
    // easier problems early on the path; dead ends get the rest
    var pathItems = items.slice(0, path.length - 1), deadItems = rng.shuffle(items.slice(path.length - 1));
    var rooms = [];
    for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
      var key = r + ',' + c, step = onPath[key];
      if (r === R - 1 && c === C - 1) rooms.push({ r: r, c: c, finish: true, step: path.length - 1 });
      else if (step !== undefined) rooms.push({ r: r, c: c, item: pathItems[step], step: step });
      else rooms.push({ r: r, c: c, item: deadItems.pop(), step: null });
    }
    var roomAt = function (r, c) { return rooms[r * C + c]; };
    var labels = [], doors = [], spare = [];
    items.forEach(function (it) { it.wrong.forEach(function (w) { spare.push({ w: w, from: it }); }); });
    function labelOk(lbl, a, b) {
      if (labels.some(function (l) { return nrm(l) === nrm(lbl); })) return false;
      return [a, b].every(function (rm) { return rm.finish || !ok(rm.item.p, lbl); });
    }
    for (r = 0; r < R; r++) for (c = 0; c < C; c++) [[0, 1], [1, 0]].forEach(function (d) {
      var r2 = r + d[0], c2 = c + d[1]; if (r2 >= R || c2 >= C) return;
      var A = roomAt(r, c), B = roomAt(r2, c2), sa = onPath[r + ',' + c], sb = onPath[r2 + ',' + c2], door = { a: [r, c], b: [r2, c2] };
      if (sa !== undefined && sb !== undefined && Math.abs(sa - sb) === 1) {
        var from = sa < sb ? A : B; door.label = from.item.key; door.correct = true; door.step = Math.min(sa, sb);
        door.dir = sa < sb ? 'ab' : 'ba';
      } else {
        // a tempting wrong answer: from the earlier path room if there is one, else either room
        var pref = [A, B].filter(function (x) { return !x.finish; }).sort(function (x, y) { return (x.step === null ? 99 : x.step) - (y.step === null ? 99 : y.step); });
        var pick = null;
        pref.forEach(function (rm) { if (pick) return; rm.item.wrong.forEach(function (w) { if (!pick && labelOk(w, A, B)) pick = w; }); });
        if (!pick) rng.shuffle(spare.slice()).forEach(function (s) { if (!pick && labelOk(s.w, A, B)) pick = s.w; });
        if (!pick) { var extra = []; pref.forEach(function (rm) { extra = extra.concat(wrongs(rm.item.p, 8, cfg.seed + '|x' + r + c)); }); extra.forEach(function (w) { if (!pick && labelOk(w, A, B)) pick = w; }); }
        if (!pick) return;   // no safe label: the wall stays closed
        door.label = pick; door.correct = false;
      }
      labels.push(door.label); doors.push(door);
    });
    // final safety check: each path room has exactly one door that accepts its answer, and it is the next step
    var problems = [];
    rooms.forEach(function (rm) {
      if (rm.finish) return;
      var mine = doors.filter(function (d) { return (d.a[0] === rm.r && d.a[1] === rm.c) || (d.b[0] === rm.r && d.b[1] === rm.c); });
      var acc = mine.filter(function (d) { return ok(rm.item.p, d.label); });
      if (rm.step !== null) { if (acc.length !== 1 || !acc[0].correct) problems.push('room ' + rm.r + ',' + rm.c); }
      else if (acc.length) problems.push('dead end ' + rm.r + ',' + rm.c);
    });
    if (problems.length) return { error: 'Maze check failed (' + problems.join(', ') + ').' };
    return { kind: 'maze', R: R, C: C, rooms: rooms, doors: doors, path: path, items: items };
  };

  /* =========================== COLOR BY NUMBER =========================== */
  var COLORS = {
    '.': ['Light blue', '#bfe3ff'], R: ['Red', '#e0393e'], W: ['White (leave blank)', '#ffffff'], A: ['Gray', '#a9b0ba'], B: ['Blue', '#2f6fd6'],
    O: ['Orange', '#f39a2b'], Y: ['Yellow', '#f6d53f'], N: ['Brown', '#8b5a2b'], G: ['Green', '#3aa655'], D: ['Dark green', '#1f6e3a'],
    P: ['Pink', '#f39bc4'], V: ['Purple', '#8a55c9'], K: ['Black', '#222222'], T: ['Tan', '#e3c58f']
  };
  PR.PICTURES = {
    rocket: { name: 'Rocket', rows: ['.....RR.....', '....RWWR....', '....WWWW....', '...WWBBWW...', '...WWBBWW...', '...WWWWWW...', '...WWWWWW...', '...WWRRWW...', '..RWWWWWWR..', '.RRWWWWWWRR.', '.RR.WWWW.RR.', '....OYYO....', '.....OO.....', '.....YY.....'] },
    house: { name: 'House', rows: ['.Y..........', '.....RR.....', '....RRRR....', '...RRRRRR...', '..RRRRRRRR..', '.RRRRRRRRRR.', '..TTTTTTTT..', '..TBBTTBBT..', '..TBBTTBBT..', '..TTTNNTTT..', '..TTTNNTTT..', '..TTTNNTTT..', 'GGGGGGGGGGGG', 'GGGGGGGGGGGG'] },
    tree: { name: 'Apple tree', rows: ['............', '....GGGG....', '..GGGGGGGG..', '.GGGGRGGGGG.', '.GGGGGGGRGG.', 'GGRGGGGGGGGG', '.GGGGGGGGGG.', '..GGGRGGGG..', '....GNNG....', '.....NN.....', '.....NN.....', '.....NN.....', 'DDDDDDDDDDDD', 'DDDDDDDDDDDD'] },
    boat: { name: 'Sailboat', rows: ['............', '.....W......', '.....WW.....', '.....WWW....', '.....WWWW...', '.....WWWWW..', '.....WWWWWW.', '.....N......', '.RRRRRRRRRR.', '..RRRRRRRR..', '...RRRRRR...', 'BBBBBBBBBBBB', 'BBBBBBBBBBBB', 'BBBBBBBBBBBB'] },
    balloon: { name: 'Hot-air balloon', rows: ['....RRRR....', '..RRYYYYRR..', '.RYYRRRRYYR.', '.RYRRRRRRYR.', 'RYRRRRRRRRYR', 'RYRRRRRRRRYR', '.RYRRRRRRYR.', '..RYRRRRYR..', '...RYRRYR...', '....N..N....', '....N..N....', '....NNNN....', '....NNNN....', '............'] },
    fish: { name: 'Fish', rows: ['............', '..........W.', '.....OOO....', '...OOOOOO..O', '..OOWKOOOOOO', '.OOOWWOOOOO.', '.OOOOOOOOOO.', '..OOOOOOOOOO', '...OOOOOO..O', '.....OOO....', '.W..........', '............', 'TTTTTTTTTTTT', 'TTTTTTTTTTTT'] },
    cactus: { name: 'Cactus', rows: ['Y...........', '.....GG.....', '....GGGG....', '....GGGG....', '.GG.GGGG....', '.GG.GGGG.GG.', '.GGGGGGG.GG.', '..GGGGGGGGG.', '....GGGGGG..', '....GGGG....', '....GGGG....', '...RRRRRR...', 'TTTRRRRRRTTT', 'TTTTRRRRTTTT'] },
    heart: { name: 'Heart', rows: ['............', '.RRR....RRR.', 'RRRRR..RRRRR', 'RRWRRRRRRRRR', 'RRRRRRRRRRRR', 'RRRRRRRRRRRR', '.RRRRRRRRRR.', '..RRRRRRRR..', '...RRRRRR...', '....RRRR....', '.....RR.....', '............', 'PPPPPPPPPPPP', 'PPPPPPPPPPPP'] }
  };
  PR.buildColor = function (cfg, vIdx) {
    var rng = rngOf(cfg.seed, vIdx, 'color');
    var picId = cfg.picture && PR.PICTURES[cfg.picture] ? cfg.picture : rng.pick(Object.keys(PR.PICTURES));
    var pic = PR.PICTURES[picId], grid = pic.rows.map(function (r) { return r.split(''); });
    var count = {}; grid.forEach(function (row) { row.forEach(function (ch) { count[ch] = (count[ch] || 0) + 1; }); });
    var chars = Object.keys(count).sort(function (a, b) { return count[b] - count[a]; });
    var N = Math.max(10, Math.min(12, chars.length * 2)), items = gather(cfg, vIdx, N, 'color');
    if (items.length < chars.length + 2) return { error: 'Not enough different problems for these skills and level (' + items.length + '). Choose more skills.' };
    N = items.length;
    // every color gets at least one problem; the rest go to the colors with the most squares
    var byColor = {}; chars.forEach(function (ch) { byColor[ch] = []; });
    var order = rng.shuffle(items.map(function (_, i) { return i; }));
    chars.forEach(function (ch, k) { byColor[ch].push(order[k]); });
    for (var k = chars.length; k < N; k++) {
      var best = chars.slice().sort(function (a, b) { return count[b] / byColor[b].length - count[a] / byColor[a].length; })[0];
      byColor[best].push(order[k]);
    }
    var colorOf = []; chars.forEach(function (ch) { byColor[ch].forEach(function (i) { colorOf[i] = ch; }); });
    var cells = grid.map(function (row) { return row.map(function (ch) { return byColor[ch][rng.int(0, byColor[ch].length - 1)] + 1; }); });
    // every problem number appears in the picture
    chars.forEach(function (ch) { byColor[ch].forEach(function (i) {
      var has = cells.some(function (row) { return row.indexOf(i + 1) >= 0; }); if (has) return;
      var spots = []; grid.forEach(function (row, r) { row.forEach(function (x, c) { if (x === ch) spots.push([r, c]); }); });
      var s = rng.pick(spots); cells[s[0]][s[1]] = i + 1;
    }); });
    var code = chars.map(function (ch) { return { ch: ch, name: COLORS[ch][0], hex: COLORS[ch][1], answers: rng.shuffle(byColor[ch].map(function (i) { return items[i].key; })) }; });
    return { kind: 'color', picture: picId, pictureName: pic.name, grid: grid, cells: cells, items: items, colorOf: colorOf, code: rng.shuffle(code), colors: COLORS };
  };

  /* =========================== PARTNER CHECK =========================== */
  /* Pairs of different problems whose answers each verifier accepts for the other (same answer). */
  function countPairs(pool) { var g = {}; pool.forEach(function (it) { var k = nrm(it.key).replace(/^[a-z]=/, ''); g[k] = (g[k] || 0) + 1; }); return Object.keys(g).filter(function (k) { return g[k] > 1; }).length; }
  PR.buildPartner = function (cfg, vIdx) {
    var lv = NS.LEVELS[cfg.level] || NS.LEVELS.cp1, skills = PR.skillsFor(cfg), rng = rngOf(cfg.seed, vIdx, 'partner');
    if (!skills.length) return { error: 'None of the selected skills can make partner problems.' };
    var want = 8, pool = [], used = { keys: new Set(), sigs: new Set() };
    for (var i = 0; i < 900 && pool.length < (i < 360 ? 340 : 800); i++) {
      if (i === 360 && countPairs(pool) >= want + 2) break;   // most units find enough pairs quickly
      var sk = skills[i % skills.length], c = lv.tiers[i % 3];
      var it = makeItem(cfg, sk, c, [cfg.seed, vIdx, 'pc', i].join('|'), used, 'partner');
      if (it) pool.push(it);
    }
    var groups = {}; pool.forEach(function (it) { var k = nrm(it.key).replace(/^[a-z]=/, ''); (groups[k] = groups[k] || []).push(it); });
    var pairs = [];
    Object.keys(groups).forEach(function (k) {
      var L = groups[k]; if (L.length < 2) return;
      for (var a = 0; a < L.length; a++) for (var b = a + 1; b < L.length; b++) {
        if (nrm(L[a].p.prompt) === nrm(L[b].p.prompt)) continue;
        if (ok(L[a].p, L[b].key) && ok(L[b].p, L[a].key)) { pairs.push({ A: L[a], B: L[b], same: L[a].skill === L[b].skill }); return; }
      }
    });
    // prefer same-skill pairs, spread over skills, no two rows with the same answer
    pairs = rng.shuffle(pairs).sort(function (x, y) { return (y.same ? 1 : 0) - (x.same ? 1 : 0); });
    var rows = [], perSkill = {};
    for (var round = 0; round < 4 && rows.length < want; round++) pairs.forEach(function (pr) {
      if (rows.length >= want || rows.indexOf(pr) >= 0) return;
      if ((perSkill[pr.A.skill] || 0) > round) return;
      if (rows.some(function (r) { return clash(r.A, pr.A); })) return;
      rows.push(pr); perSkill[pr.A.skill] = (perSkill[pr.A.skill] || 0) + 1;
    });
    if (rows.length < 4) return { error: 'These skills rarely give two different problems with the same answer (found ' + rows.length + '). Choose more skills (number answers match most often).' };
    rows.sort(function (x, y) { return Math.max(x.A.c, x.B.c) - Math.max(y.A.c, y.B.c); });
    rows.forEach(function (r) { if (rng.next() < 0.5) { var t = r.A; r.A = r.B; r.B = t; } });
    return { kind: 'partner', rows: rows };
  };

  /* =========================== ERROR ANALYSIS =========================== */
  var NAMES = ['Alex', 'Jordan', 'Sam', 'Taylor', 'Riley', 'Casey', 'Morgan', 'Jamie', 'Avery', 'Quinn'];
  /* The student's work: the worked steps, with the wrong answer written in the step that produces the answer
     (and nothing after it), so the mistake is in one visible line. */
  function wrongWork(it, wrong) {
    var steps = (it.p.steps || []).filter(function (s) { return s.t || s.m; });
    var ks = snippetsOf(it.key), ws = snippetsOf(wrong);
    var last = -1;
    if (ks.length === 1 && ws.length === 1) steps.forEach(function (s, i) { if (s.m && nrm(s.m).indexOf(nrm(ks[0]).replace(/^[a-z]=/, '')) >= 0) last = i; });
    var lines = [];
    if (last >= 0) {
      // replace the answer inside that step's math exactly as it is written; if it is written differently, the
      // wrong answer is shown only as the student's answer
      var lm = steps[last].m || '', kx = ks[0], wx = ws[0], strip = function (t) { return t.replace(/^[a-z]\s*=\s*/, ''); };
      var fixed = lm.indexOf(kx) >= 0 ? lm.replace(kx, wx) : lm.indexOf(strip(kx)) >= 0 && strip(kx).length > 1 ? lm.replace(strip(kx), strip(wx)) : null;
      steps.slice(0, fixed === null ? last : last + 1).forEach(function (s, i) { lines.push({ t: s.t || '', m: i === last ? fixed : s.m || '', bad: i === last }); });
    } else {
      steps.slice(0, Math.max(0, steps.length - 1)).forEach(function (s) { lines.push({ t: s.t || '', m: s.m || '' }); });
      // the wrong answer itself is the mistaken line (shown as the student's answer below the work)
    }
    return lines;
  }
  PR.buildError = function (cfg, vIdx) {
    var rng = rngOf(cfg.seed, vIdx, 'error'), n = 6;
    var items = gather(cfg, vIdx, n, 'error');
    if (items.length < 4) return { error: 'Not enough problems with worked steps for these skills (' + items.length + ').' };
    var names = rng.shuffle(NAMES.slice());
    var cases = items.map(function (it, i) {
      var wrong = rng.pick(it.wrong.slice(0, 2));
      return { item: it, name: names[i % names.length], wrong: wrong, work: wrongWork(it, wrong) };
    });
    return { kind: 'error', cases: cases };
  };

  /* =========================== TARSIA =========================== */
  /* Triangular grid in "lattice" coordinates: point (i, j) is at x = i + j/2, y = j·√3/2. A small triangle is
     up (i,j),(i+1,j),(i,j+1) or down (i+1,j),(i,j+1),(i+1,j+1). Shapes are lists of small triangles. */
  function tri(up, i, j) { return up ? [[i, j], [i + 1, j], [i, j + 1]] : [[i + 1, j], [i, j + 1], [i + 1, j + 1]]; }
  function shapeHex() {   // regular hexagon of side 2: 24 triangles
    var out = [];
    for (var j = -2; j < 2; j++) for (var i = -4; i < 4; i++) [true, false].forEach(function (up) {
      var t = tri(up, i, j), cx = 0, cy = 0;
      t.forEach(function (p) { cx += p[0] + p[1] / 2; cy += p[1] * Math.sqrt(3) / 2; }); cx /= 3; cy /= 3;
      // inside the hexagon |y| ≤ √3, and the slanted sides
      var s3 = Math.sqrt(3);
      if (Math.abs(cy) < s3 && Math.abs(s3 * cx + cy) < 2 * s3 && Math.abs(s3 * cx - cy) < 2 * s3) out.push(t);
    });
    return out;
  }
  function shapeTri() {   // big triangle of side 4: 16 triangles
    var out = [];
    for (var j = 0; j < 4; j++) for (var i = 0; i < 4 - j; i++) { out.push(tri(true, i, j)); if (i < 3 - j) out.push(tri(false, i, j)); }
    return out;
  }
  function ekey(p, q) { var a = p.join(','), b = q.join(','); return a < b ? a + '|' + b : b + '|' + a; }
  PR.TARSIA_SHAPES = { hexagon: { name: 'hexagon', tris: shapeHex }, triangle: { name: 'triangle', tris: shapeTri } };
  PR.buildTarsia = function (cfg, vIdx) {
    var rng = rngOf(cfg.seed, vIdx, 'tarsia'), shapeId = 'hexagon', tris = shapeHex();
    var edges = {}; tris.forEach(function (t, ti) { [[0, 1], [1, 2], [2, 0]].forEach(function (e, ei) { var k = ekey(t[e[0]], t[e[1]]); (edges[k] = edges[k] || []).push({ t: ti, e: ei }); }); });
    var inner = Object.keys(edges).filter(function (k) { return edges[k].length === 2; });
    var items = gather(cfg, vIdx, inner.length, 'tarsia');
    if (items.length < inner.length) {
      shapeId = 'triangle'; tris = shapeTri(); edges = {};
      tris.forEach(function (t, ti) { [[0, 1], [1, 2], [2, 0]].forEach(function (e, ei) { var k = ekey(t[e[0]], t[e[1]]); (edges[k] = edges[k] || []).push({ t: ti, e: ei }); }); });
      inner = Object.keys(edges).filter(function (k) { return edges[k].length === 2; });
      if (items.length < inner.length) return { error: 'A Tarsia needs ' + inner.length + ' short problems with different answers; these skills gave ' + items.length + '. Choose more skills (Tarsia uses problems like “Solve 3x + 4 = 19”).' };
      items = items.slice(0, inner.length);
    }
    // number problems in difficulty order; place them on edges at random
    items.forEach(function (it, i) { it.num = i + 1; });
    var placed = rng.shuffle(items.slice());
    var pieces = tris.map(function (t) { return { pts: t, text: ['', '', ''], kind: ['', '', ''] }; });
    inner.forEach(function (k, n) {
      var it = placed[n], sides = rng.shuffle(edges[k].slice());
      pieces[sides[0].t].text[sides[0].e] = it.num + '. ' + it.edge;
      pieces[sides[0].t].kind[sides[0].e] = 'q';
      pieces[sides[1].t].text[sides[1].e] = it.key;
      pieces[sides[1].t].kind[sides[1].e] = 'a';
      it.edge = k;
    });
    // outer edges: wrong answers (rejected by every problem on the puzzle) so the border is not given away
    var decoys = [];
    items.forEach(function (it) { it.wrong.forEach(function (w) { if (decoys.length < 40 && !items.some(function (o) { return ok(o.p, w); }) && !decoys.some(function (d) { return nrm(d) === nrm(w); }) && !items.some(function (o) { return nrm(o.key) === nrm(w); })) decoys.push(w); }); });
    decoys = rng.shuffle(decoys);
    Object.keys(edges).filter(function (k) { return edges[k].length === 1; }).forEach(function (k, n) {
      var s = edges[k][0]; if (n % 2 === 0 && decoys.length) { pieces[s.t].text[s.e] = decoys.pop(); pieces[s.t].kind[s.e] = 'd'; }
    });
    // the student copy: pieces shuffled into the slots, each turned to fit its slot
    var slots = rng.shuffle(pieces.map(function (_, i) { return i; }));
    var scrambled = slots.map(function (pi, si) { return { piece: pi, slot: si, turn: rng.int(0, 2) }; });
    return { kind: 'tarsia', shape: shapeId, pieces: pieces, items: items, scrambled: scrambled };
  };

  /* Build one version; a draw that cannot be completed is retried with other numbers before giving up. */
  PR.build = function (cfg, vIdx) {
    var f = { maze: PR.buildMaze, color: PR.buildColor, partner: PR.buildPartner, error: PR.buildError, tarsia: PR.buildTarsia }[cfg.kind];
    if (!f) return { error: 'Unknown printable ' + cfg.kind };
    var B = null;
    for (var k = 0; k < 3; k++) {
      var c2 = Object.assign({}, cfg); if (k) c2.seed = cfg.seed + '|retry' + k;
      B = f(c2, vIdx || 0); if (!B.error) return B;
    }
    // Honors problems can be too long for a maze door or a Tarsia edge in some units: use Standard-level problems
    if (cfg.level === 'honors' && (cfg.kind === 'tarsia' || cfg.kind === 'maze')) {
      var c3 = Object.assign({}, cfg, { level: 'cp1' }), B2 = f(c3, vIdx || 0);
      if (!B2.error) { B2.levelNote = 'Honors problems in this unit are too long for a ' + PR.kind(cfg.kind).name.toLowerCase() + ', so it uses Standard (CP1) problems.'; return B2; }
    }
    return B;
  };
})(typeof window !== 'undefined' ? window : globalThis);
