/* Computer opponent for solo Connect 4 (and Four in a Row) and Tic-Tac-Toe (MKSOLOAI).
   The computer plays sensibly but not perfectly, so a student who answers carefully can beat it:
   - it also has to "answer" its own problem, and sometimes gets it wrong (no move that turn);
   - it takes a win and blocks the student's win when it sees one (on Easy it occasionally overlooks one);
   - it never drops a disc that hands the student a win on top of it, unless every column does;
   - otherwise it plans a few moves ahead (fewer on Easy) and picks among the good moves, not always the best one.
   Before 2026-11-20 it also played fully random moves and skipped many blocks, which looked careless.
   Levels: 'easy' | 'medium' | 'hard' (anything else means medium).
   Board conventions: Tic-Tac-Toe uses 9 cells; Connect 4 uses board[row][col] with row 0 at the top.
   Empty cells are null, undefined or ''. 0 counts as a piece, because some games use team 0 and team 1. */
(function (G) {
  'use strict';
  // answer: how often the computer solves its own problem. missWin / missBlock: how often it overlooks an immediate
  // win or block. depth: Connect 4 look-ahead in moves. slack: how far below its best move (in Connect 4 points) a
  // move may score and still be chosen. ttt.loose: how often in Tic-Tac-Toe it picks any move that does not lose
  // instead of the best one. Tuned by simulation (tests/solo-ai-tests.cjs).
  var LEVELS = {
    easy:   { label: 'Easy',   answer: 0.55, missWin: 0.1,  missBlock: 0.1,  ttt: { loose: 0.8 }, c4: { depth: 2, slack: 12 } },
    medium: { label: 'Medium', answer: 0.65, missWin: 0.03, missBlock: 0.03, ttt: { loose: 0.45 }, c4: { depth: 3, slack: 5 } },
    hard:   { label: 'Hard',   answer: 0.75, missWin: 0,    missBlock: 0,    ttt: { loose: 0.15 }, c4: { depth: 5, slack: 1 } }
  };

  var rand = Math.random;
  function cfg(level) { return LEVELS[level] || LEVELS.medium; }
  function chance(p) { return rand() < p; }
  function pick(a) { return a[Math.floor(rand() * a.length)]; }
  function blank(v) { return v === null || v === undefined || v === ''; }

  /* ---------------- Tic-Tac-Toe ---------------- */
  var LINES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]];
  function tttWinner(b) {
    for (var i = 0; i < 8; i++) { var l = LINES[i]; if (!blank(b[l[0]]) && b[l[0]] === b[l[1]] && b[l[1]] === b[l[2]]) return b[l[0]]; }
    return null;
  }
  function tttFree(b) { var o = []; for (var i = 0; i < 9; i++) if (blank(b[i])) o.push(i); return o; }
  function tttWinningSquare(b, mark) {
    var f = tttFree(b);
    for (var i = 0; i < f.length; i++) { var c = b.slice(); c[f[i]] = mark; if (tttWinner(c) === mark) return f[i]; }
    return -1;
  }
  // Perfect-play score of a position (memoised; 'filled' is the absolute move count so the memo stays valid).
  var memo = {};
  function tttScore(b, turn, me, them) {
    var key = b.map(function (v) { return blank(v) ? '.' : v === me ? 'm' : 't'; }).join('') + (turn === me ? 'M' : 'T');
    if (key in memo) return memo[key];
    var w = tttWinner(b), f = tttFree(b), filled = 9 - f.length, best;
    if (w === me) best = 20 - filled;
    else if (w === them) best = filled - 20;
    else if (!f.length) best = 0;
    else {
      best = turn === me ? -99 : 99;
      for (var i = 0; i < f.length; i++) {
        var c = b.slice(); c[f[i]] = turn;
        var sc = tttScore(c, turn === me ? them : me, me, them);
        best = turn === me ? Math.max(best, sc) : Math.min(best, sc);
      }
    }
    return (memo[key] = best);
  }
  /** The square (0–8) the computer chooses. */
  function tttMove(board, me, them, level) {
    var L = cfg(level), f = tttFree(board);
    if (!f.length) return -1;
    var win = tttWinningSquare(board, me);
    if (win >= 0 && !chance(L.missWin)) return win;
    var block = tttWinningSquare(board, them);
    if (block >= 0 && !chance(L.missBlock)) return block;
    var scored = f.map(function (sq) { var c = board.slice(); c[sq] = me; return { sq: sq, s: tttScore(c, them, me, them) }; });
    var best = Math.max.apply(null, scored.map(function (x) { return x.s; }));
    var pool = scored.filter(function (x) { return x.s === best; });
    if (chance(L.ttt.loose)) {
      // any move that does not lose against good play; the centre and corners are the natural choices
      var safe = scored.filter(function (x) { return x.s >= 0; });
      if (safe.length) pool = safe.filter(function (x) { return x.sq === 4 || x.sq % 2 === 0; }).concat(safe);
    }
    return pick(pool).sq;
  }

  /* ---------------- Connect 4 ---------------- */
  function c4Open(g) { var o = []; for (var c = 0; c < g[0].length; c++) if (blank(g[0][c])) o.push(c); return o; }
  function c4Drop(g, col, p) {
    var k = g.map(function (r) { return r.slice(); });
    for (var r = k.length - 1; r >= 0; r--) if (blank(k[r][col])) { k[r][col] = p; return k; }
    return null;
  }
  function c4Wins(g, p) {
    var R = g.length, C = g[0].length, D = [[0, 1], [1, 0], [1, 1], [1, -1]];
    for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
      if (g[r][c] !== p) continue;
      for (var d = 0; d < 4; d++) {
        var n = 1;
        while (n < 4) { var rr = r + D[d][0] * n, cc = c + D[d][1] * n; if (rr < 0 || rr >= R || cc < 0 || cc >= C || g[rr][cc] !== p) break; n++; }
        if (n === 4) return true;
      }
    }
    return false;
  }
  function windowScore(w, me, them) {
    var m = 0, t = 0, e = 0;
    for (var i = 0; i < 4; i++) { if (w[i] === me) m++; else if (w[i] === them) t++; else if (blank(w[i])) e++; }
    if (m === 3 && e === 1) return 5; if (m === 2 && e === 2) return 2;
    if (t === 3 && e === 1) return -4; if (t === 2 && e === 2) return -1;
    return 0;
  }
  function c4Heuristic(g, me, them) {
    var R = g.length, C = g[0].length, mid = Math.floor(C / 2), s = 0, r, c;
    for (r = 0; r < R; r++) { if (g[r][mid] === me) s += 3; else if (g[r][mid] === them) s -= 3; }
    for (r = 0; r < R; r++) for (c = 0; c < C; c++) {
      if (c + 3 < C) s += windowScore([g[r][c], g[r][c + 1], g[r][c + 2], g[r][c + 3]], me, them);
      if (r + 3 < R) s += windowScore([g[r][c], g[r + 1][c], g[r + 2][c], g[r + 3][c]], me, them);
      if (r + 3 < R && c + 3 < C) s += windowScore([g[r][c], g[r + 1][c + 1], g[r + 2][c + 2], g[r + 3][c + 3]], me, them);
      if (r + 3 < R && c - 3 >= 0) s += windowScore([g[r][c], g[r + 1][c - 1], g[r + 2][c - 2], g[r + 3][c - 3]], me, them);
    }
    return s;
  }
  function c4Order(open, C) { var m = (C - 1) / 2; return open.slice().sort(function (x, y) { return Math.abs(x - m) - Math.abs(y - m); }); }
  function c4Search(g, depth, a, b, mine, me, them) {
    if (c4Wins(g, me)) return 10000 + depth;
    if (c4Wins(g, them)) return -10000 - depth;
    var open = c4Order(c4Open(g), g[0].length);
    if (!open.length) return 0;
    if (depth === 0) return c4Heuristic(g, me, them);
    var v = mine ? -Infinity : Infinity;
    for (var i = 0; i < open.length; i++) {
      var s = c4Search(c4Drop(g, open[i], mine ? me : them), depth - 1, a, b, !mine, me, them);
      if (mine) { v = Math.max(v, s); a = Math.max(a, v); } else { v = Math.min(v, s); b = Math.min(b, v); }
      if (a >= b) break;
    }
    return v;
  }
  // Columns where the other player would win right away.
  function c4Threats(g, p) { return c4Open(g).filter(function (c) { return c4Wins(c4Drop(g, c, p), p); }); }
  /** The column (0-based) the computer drops into. */
  function c4Move(board, me, them, level) {
    var L = cfg(level), open = c4Open(board);
    if (!open.length) return -1;
    var wins = c4Threats(board, me);
    if (wins.length && !chance(L.missWin)) return wins[0];
    var blocks = c4Threats(board, them);
    if (blocks.length && !chance(L.missBlock)) return blocks[0];
    // Never play under the student's winning square (it would hand them the win) while another column is safe.
    var safe = open.filter(function (c) { return !c4Threats(c4Drop(board, c, me), them).length; });
    var cand = safe.length ? safe : open;
    var scored = cand.map(function (c) { return { c: c, s: c4Search(c4Drop(board, c, me), L.c4.depth - 1, -Infinity, Infinity, false, me, them) }; });
    var top = Math.max.apply(null, scored.map(function (x) { return x.s; }));
    // A forced win or loss found by the search is followed; otherwise any move close to the best is fine.
    var slack = Math.abs(top) >= 9000 ? 0 : L.c4.slack;
    return pick(scored.filter(function (x) { return x.s >= top - slack; })).c;
  }

  /** Whether the computer gets its own problem right this turn. */
  function answers(level) { return chance(cfg(level).answer); }

  G.MKSOLOAI = {
    LEVELS: LEVELS,
    levelName: function (k) { return cfg(k).label; },
    answers: answers,
    ticTacToeMove: tttMove,
    connectFourMove: c4Move,
    ticTacToeWinner: tttWinner,
    connectFourWins: c4Wins,
    _setRandom: function (fn) { rand = fn || Math.random; }
  };
})(typeof window !== 'undefined' ? window : globalThis);
