/* Computer opponent for solo Connect 4 and Tic-Tac-Toe (MKSOLOAI).
   The computer plays well but not perfectly, so a student who answers carefully can beat it:
   - it also has to "answer" its own problem, and sometimes gets it wrong (no move that turn);
   - it looks only a few moves ahead in Connect 4;
   - now and then it plays a random or second-best move, or misses a block or a win.
   Levels: 'easy' | 'medium' | 'hard' (anything else means medium).
   Board conventions: Tic-Tac-Toe uses 9 cells; Connect 4 uses board[row][col] with row 0 at the top.
   Empty cells are null, undefined or ''. 0 counts as a piece, because some games use team 0 and team 1. */
(function (G) {
  'use strict';
  // answer: how often the computer solves its own problem. The other numbers are how often it slips:
  // random = plays a random move, missWin = overlooks its own winning move, missBlock = fails to block yours.
  // Tuned by simulation (tests/solo-ai-tests.cjs). A student who answers about 70% of problems correctly
  // and plays sensibly wins about 55–70% of games on Easy, 40–45% on Medium and about 20% on Hard;
  // a student who answers 85% correctly wins about half the time even on Hard.
  var LEVELS = {
    easy:   { label: 'Easy',   answer: 0.6, ttt: { random: 0.45, missWin: 0.3,  missBlock: 0.55 }, c4: { random: 0.4,  missWin: 0.3,  missBlock: 0.55, depth: 1 } },
    medium: { label: 'Medium', answer: 0.7, ttt: { random: 0.3,  missWin: 0.15, missBlock: 0.4  }, c4: { random: 0.3,  missWin: 0.2,  missBlock: 0.45, depth: 2 } },
    hard:   { label: 'Hard',   answer: 0.8, ttt: { random: 0.15, missWin: 0.05, missBlock: 0.2  }, c4: { random: 0.15, missWin: 0.05, missBlock: 0.25, depth: 3 } }
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
    var s = cfg(level).ttt, f = tttFree(board);
    if (!f.length) return -1;
    var win = tttWinningSquare(board, me);
    if (win >= 0 && !chance(s.missWin)) return win;
    var block = tttWinningSquare(board, them);
    if (block >= 0 && !chance(s.missBlock)) return block;
    if (chance(s.random)) return pick(f);
    var best = -99, opts = [];
    for (var i = 0; i < f.length; i++) {
      var c = board.slice(); c[f[i]] = me;
      var sc = tttScore(c, them, me, them);
      if (sc > best) { best = sc; opts = [f[i]]; } else if (sc === best) opts.push(f[i]);
    }
    return pick(opts);
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
  function c4Search(g, depth, a, b, mine, me, them) {
    if (c4Wins(g, me)) return 10000 + depth;
    if (c4Wins(g, them)) return -10000 - depth;
    var open = c4Open(g);
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
  /** The column (0-based) the computer drops into. */
  function c4Move(board, me, them, level) {
    var s = cfg(level).c4, open = c4Open(board), i;
    if (!open.length) return -1;
    if (!chance(s.missWin)) for (i = 0; i < open.length; i++) if (c4Wins(c4Drop(board, open[i], me), me)) return open[i];
    if (!chance(s.missBlock)) for (i = 0; i < open.length; i++) if (c4Wins(c4Drop(board, open[i], them), them)) return open[i];
    if (chance(s.random)) return pick(open);
    var scored = open.map(function (c) { return { c: c, s: c4Search(c4Drop(board, c, me), s.depth - 1, -Infinity, Infinity, false, me, them) }; });
    var top = Math.max.apply(null, scored.map(function (x) { return x.s; }));
    return pick(scored.filter(function (x) { return x.s >= top - 2; })).c;
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
