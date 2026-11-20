/* Solo mode (one student against the computer) for the hand-built Connect 4 and Tic-Tac-Toe pages
   (the Algebra 2 games). Load it after the page's own game script and after solo-ai.js:
     <script src="../../worksheet-generator/games/solo-ai.js?v=solo-ai-20261120"></script>
     <script src="../../worksheet-generator/games/solo-legacy.js?v=solo-1"></script>
   It reuses the page's own functions (startTurn, dropCol, submit, afterQuiz, render, ...) and only changes
   what solo mode needs: no steals, and the computer takes its own turns. Two-team play is unchanged. */
(function () {
  'use strict';
  var AI = window.MKSOLOAI;
  if (!AI) return;
  var KEY = 'mk-solo:' + location.pathname, CPU = 'Computer';
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { return {}; } }
  function save(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* private window */ } }
  function q(s) { return document.querySelector(s); }
  function delay() { return 900 + Math.floor(Math.random() * 600); }
  function escH(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  var levelOpts = Object.keys(AI.LEVELS);

  /* ======================= Connect 4 (G.board, startTurn, dropCol) ======================= */
  if (typeof dropCol === 'function' && typeof startTurn === 'function' && typeof toStealOffer === 'function') {
    var saved = load(), teamName1 = q('#name1') ? q('#name1').value : 'Team 2';
    G.solo = new URLSearchParams(location.search).get('student') === '1' || new URLSearchParams(location.search).get('mode') === 'solo' || saved.mode === 'solo'; G.ai = saved.ai || 'medium'; G.cpuNote = ''; G.cpuToken = 0;
    var ctl = q('.controls');
    if (ctl) {
      var lab = document.createElement('label'); lab.setAttribute('for', 'soloSel');
      lab.innerHTML = 'Players<select id="soloSel"><option value="teams">Two teams</option>' +
        levelOpts.map(function (k) { return '<option value="' + k + '">Solo vs. computer (' + AI.levelName(k) + ')</option>'; }).join('') + '</select>';
      ctl.insertBefore(lab, ctl.firstChild);
      q('#soloSel').value = G.solo ? G.ai : 'teams';
      q('#soloSel').addEventListener('change', function () {
        G.solo = this.value !== 'teams'; if (G.solo) G.ai = this.value;
        save({ mode: G.solo ? 'solo' : 'teams', ai: G.ai }); applyNames(); G.wins = [0, 0]; newGame();
      });
    }
    var applyNames = function () {
      var n = q('#name1'); if (!n) return;
      if (G.solo) { if (!n.disabled) teamName1 = n.value; n.value = CPU; n.disabled = true; G.names[1] = CPU; }
      else if (n.disabled) { n.disabled = false; n.value = teamName1; G.names[1] = teamName1; }
      var how = q('details.how p');
      if (how && G.solo) how.textContent = 'Solo mode: answer your problem correctly to earn a disc, then choose a column. A wrong answer means no disc, and the computer goes next. The computer has to solve its own problem too, and it does not always get it right. The worked solution appears after every turn.';
    };
    applyNames();

    var origToSteal = toStealOffer, origStart = startTurn, origRender = render, origNew = newGame, origChoose = choose;
    toStealOffer = function (timeout) {
      if (!G.solo) return origToSteal(timeout);
      endNoDisc(timeout ? 'Time is up. No disc this turn.' : 'Not quite. No disc this turn.');
    };
    choose = function (i) { G.cpuNote = ''; return origChoose(i); };
    newGame = function () { G.cpuToken++; G.cpuNote = ''; return origNew(); };
    startTurn = function (team) {
      if (G.solo && team === 1) return cpuTurn();
      return origStart(team);
    };
    render = function () {
      origRender();
      if (!G.solo) return;
      var box = q('#q'); if (!box) return;
      if (G.phase === 'question' && G.cpuNote) box.insertAdjacentHTML('afterbegin', '<div class="callout" role="status">' + escH(G.cpuNote) + ' Your turn!</div>');
      if (G.phase === 'resolved' && /^(Not quite|Time)/.test(G.note || '')) { var c = box.querySelector('.callout.good'); if (c) { c.classList.remove('good'); c.classList.add('warn'); } }
      if (G.phase === 'over' && !G.draw && G.dropper === 1) {
        var st = box.querySelector('.steps'); if (st) st.remove();
        var co = box.querySelector('.callout'); if (co) co.innerHTML = '<b>The computer connected four.</b> Try again: you can beat it!';
      }
    };
    var cpuTurn = function () {
      var token = ++G.cpuToken;
      stopTimer(); G.turn = 1; G.answerer = 1; G.phase = 'cpu';
      [0, 1].forEach(function (t) { q('#card' + t).classList.toggle('active', t === 1); q('#tag' + t).textContent = t === 1 ? 'Thinking…' : ''; });
      q('#q').innerHTML = '<div class="qhead"><span class="who t1"><i></i>' + CPU + '</span></div><div class="callout" role="status">The computer is working on its problem…</div>';
      syncCols();
      setTimeout(function () {
        if (token !== G.cpuToken || G.phase !== 'cpu' || !G.solo) return;
        if (!AI.answers(G.ai)) { G.cpuNote = 'The computer missed its problem. No disc this turn.'; origStart(0); return; }
        var col = AI.connectFourMove(G.board, 1, 0, G.ai);
        G.dropper = 1; G.stolen = false; G.phase = 'drop';
        dropCol(col);
        if (G.phase === 'resolved') { G.cpuNote = 'The computer solved its problem and dropped a disc in column ' + (col + 1) + '.'; origStart(0); }
      }, delay());
    };
    return;
  }

  /* ======================= Tic-Tac-Toe (B, turn, quiz, submit, afterQuiz) ======================= */
  if (typeof afterQuiz === 'function' && typeof submit === 'function') {
    var s2 = load();
    G.solo = new URLSearchParams(location.search).get('student') === '1'; G.ai = s2.ai || 'medium';
    var cpuNote = '', cpuTried = -1, cpuTimer = null, origRender2 = render, origSubmit = submit, origPick = pick;
    pick = function (i) { if (G.solo && turn === 'B') return; cpuNote = ''; cpuTried = -1; return origPick(i); };
    submit = function (timeout) {
      origSubmit(timeout);
      if (G.solo && quiz && quiz.stage === 'steal') {   // no steals in solo mode: the square stays open
        clearTimer(); quiz.stage = 'result'; quiz.ok = false; quiz.stolen = false; quiz.who = other(quiz.who); render();
      }
    };
    render = function () {
      origRender2();
      if (G.screen === 'setup') return setupExtras();
      if (!G.solo) return;
      var res = q('.modal .res.bad'); if (res) res.textContent = '✖ Not quite. The square stays open, and the computer goes next.';
      var tn = q('.turn');
      if (over) { var w = winner(); if (tn && w && w.t === 'B') tn.innerHTML = 'The computer wins this round. Try again!'; }
      else if (!quiz && turn === 'B') {
        if (tn) tn.textContent = 'The computer is choosing a square…';
        document.querySelectorAll('.sq').forEach(function (b) { b.disabled = true; });
        if (!cpuTimer) cpuTimer = setTimeout(cpuMove, delay());
      }
      if (cpuNote && tn && !(over && winner() && winner().t === 'B')) tn.insertAdjacentHTML('afterend', '<p role="status" style="text-align:center;margin:-4px 0 12px;font-weight:700;background:#fff8de;color:#6b4e00;border-radius:10px;padding:8px">' + escH(cpuNote) + '</p>');
      if (cpuTried >= 0) { var sq = q('.sq[data-i="' + cpuTried + '"]'); if (sq && !over) sq.style.boxShadow = '0 0 0 4px #f2b70599'; }
    };
    var cpuMove = function () {
      cpuTimer = null;
      if (!G.solo || G.screen !== 'play' || over || quiz || turn !== 'B') return;
      var sq = AI.ticTacToeMove(B, 'B', 'A', G.ai);
      if (AI.answers(G.ai)) { B[sq] = 'B'; lastDrop = sq; cpuTried = -1; cpuNote = 'The computer took square ' + (sq + 1) + '.'; }
      else { cpuTried = sq; cpuNote = 'The computer tried square ' + (sq + 1) + ' but missed its problem. The square stays open.'; }
      quiz = null; afterQuiz();
    };
    var setupExtras = function () {
      var start = q('#start'); if (!start || q('#soloMode')) return;
      var solo = new URLSearchParams(location.search).get('student') === '1' || s2.mode === 'solo';
      var box = document.createElement('div');
      box.innerHTML = '<label for="soloMode">Players</label><select id="soloMode"><option value="teams">Two teams</option><option value="solo">Solo vs. computer</option></select>' +
        '<div id="soloOpts"><label for="soloAI">Computer difficulty</label><select id="soloAI">' + levelOpts.map(function (k) { return '<option value="' + k + '">' + AI.levelName(k) + '</option>'; }).join('') + '</select>' +
        '<p style="margin:8px 0 0;line-height:1.5">Solo: you play against the computer. A correct answer takes the square; a wrong answer leaves it open (no steals). The computer has to solve its own problem too, and it does not always get it right.</p></div>';
      var row = q('.row2'); row.parentNode.insertBefore(box, row);
      var nb = q('#nb'), naLab = q('label[for="na"]'), teamLabel = naLab ? naLab.textContent : 'Team A (X)', nbOld = nb.value === CPU ? 'Team B' : nb.value;
      function sync() {
        var on = q('#soloMode').value === 'solo';
        q('#soloOpts').style.display = on ? '' : 'none';
        nb.parentNode.style.display = on ? 'none' : '';
        if (naLab) naLab.textContent = on ? 'Your name (X)' : teamLabel;
        var na = q('#na'); if (na && on && na.value.trim() === 'Team A') na.value = 'You'; else if (na && !on && na.value.trim() === 'You') na.value = 'Team A';
      }
      q('#soloMode').value = solo ? 'solo' : 'teams'; q('#soloAI').value = G.ai; sync();
      q('#soloMode').onchange = sync;
      var origStartBtn = start.onclick;
      start.onclick = function () {
        G.solo = q('#soloMode').value === 'solo'; G.ai = q('#soloAI').value;
        s2 = { mode: G.solo ? 'solo' : 'teams', ai: G.ai }; save(s2);
        nb.value = G.solo ? CPU : (nbOld || 'Team B');
        if (G.solo && q('#na').value.trim() === 'Team A') q('#na').value = 'You';
        cpuNote = ''; cpuTried = -1; if (cpuTimer) { clearTimeout(cpuTimer); cpuTimer = null; }
        G.score = { A: 0, B: 0, D: 0 };
        origStartBtn();
      };
    };
    var origNew2 = newGame;
    newGame = function () { cpuNote = ''; cpuTried = -1; if (cpuTimer) { clearTimeout(cpuTimer); cpuTimer = null; } return origNew2(); };
    if (G.screen === 'setup' && q('#start')) setupExtras();
  }
})();
