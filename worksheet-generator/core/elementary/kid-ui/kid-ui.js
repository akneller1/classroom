/* kid-ui.js — on-screen pieces for the Grade 1-5 players (games, Understanding Check, flashcards).
 *
 *   MKKid.numberPad(host, input, {answer, grade, onCheck})  big on-screen keys; the keys fit the answer (digits, time, money, <>=, fractions)
 *   MKKid.hint(answer, grade)                                one kid-sized line under the answer box (replaces CFG.answerHint)
 *   MKKid.praise(grade) / MKKid.nudge(grade, n) / MKKid.lastTry(grade)   feedback messages sized to the grade
 *   MKKid.playScreen(host, {title, grade, mascot, onPlay})  the first screen a student sees on a student link
 *   MKKid.finish(host, {right, total, grade, mascot, unit, onAgain})  celebration with an earned sticker and a sticker book
 *
 * No outside services. The sticker book is kept in this browser only (localStorage, wrapped in try/catch).
 */
(function (G) {
  'use strict';
  var BASE = typeof G.MK_KID_BASE === 'string' ? G.MK_KID_BASE : 'kid-ui/';
  var MASCOTS = { 1: 'grade1-dot', 2: 'grade2-cubie', 3: 'grade3-hexie', 4: 'grade4-zoom', 5: 'grade5-bit' };
  var STICKERS = ['star', 'rocket', 'rainbow', 'planet', 'heart', 'icepop', 'dot', 'trophy'];

  var MSG = {
    young: {   // Grades 1-2: short, sight words, no jargon
      praise: ['You got it!', 'Yes! Great job!', 'Super!', 'Way to go!', 'You did it!', 'Nice work!', 'Hooray!', 'That is right!'],
      nudge: ['Almost! Try again.', 'Look at the picture again.', 'Count again, slowly.', 'Try one more time!', 'Check the numbers again.'],
      last: 'Good try! Let’s see how to solve it.',
      finish: { all: 'You got them all!', most: 'Great job!', some: 'Good work! Keep practicing.' }
    },
    older: {   // Grades 3-5
      praise: ['Great thinking!', 'Correct!', 'Nice work!', 'You nailed it!', 'Excellent!', 'That’s right!', 'Well done!'],
      nudge: ['Not quite. Check each step.', 'Close! Look at the numbers again.', 'Try drawing a picture or a model.', 'Check your place values.', 'Read the question one more time.'],
      last: 'Good effort! Here is how to solve it.',
      finish: { all: 'Perfect score — amazing!', most: 'Great thinking!', some: 'Nice effort! Every mistake helps you learn.' }
    }
  };
  function band(grade) { return (grade || 3) <= 2 ? MSG.young : MSG.older; }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }

  /* ---------- what kind of answer is this? ---------- */
  function kind(answer) {
    var a = String(answer == null ? '' : answer).trim();
    if (/^[<>=]$/.test(a)) return 'compare';
    if (/^\d{1,2}:\d\d(\s*(AM|PM))?$/i.test(a)) return /AM|PM/i.test(a) ? 'time-ampm' : 'time';
    if (/^\$[\d,]+ and \d+¢$/.test(a)) return 'dollars-cents';
    if (/¢$/.test(a)) return 'cents';
    if (/^\$/.test(a)) return 'dollars';
    if (/^\d+\s*R\s*\d+$/i.test(a)) return 'remainder';
    if (/^\d+\s+\d+\/\d+$/.test(a) || /^\d+\/\d+$/.test(a)) return 'fraction';
    if (/^(\d+\s+)?\d+\/\d+\s+[a-z]/i.test(a)) return 'fraction-unit';   // 1/6 meter, 2 3/4 inches (Grade 3 audit #12, 2026-11-19)
    if (/^\d*\.\d+$/.test(a)) return 'decimal';
    if (/^\(.+,.+\)$/.test(a)) return 'pair';
    if (/^\d+ tens? and \d+ ones?$/i.test(a)) return 'tens-ones';   // 3 tens and 8 ones (Grade 1 audit #1, 2026-11-19)
    if (/^\d[\d,]*(?:, \d[\d,]*)+$/.test(a)) return 'list';   // 7, 14, 21 (Grade 4 audit #19, 2026-11-19)
    if (/^[\d,]+\s+[A-Za-z]/.test(a)) return 'number-unit';
    if (/^[\d,]+$/.test(a)) return 'number';
    return 'text';
  }

  function hint(answer, grade) {
    var young = (grade || 3) <= 2;
    switch (kind(answer)) {
      case 'compare': return 'Tap >, <, or =.';
      case 'time': return 'Type the time, like 3:30.';
      case 'time-ampm': return 'Type the time and AM or PM, like 4:05 PM.';
      case 'cents': return young ? 'Type the cents, like 45¢.' : 'Type the amount, like 45¢.';
      case 'dollars': return 'Type the amount, like $4.50.';
      case 'dollars-cents': return 'Type it like $12 and 36¢.';
      case 'remainder': return 'Type it like 12 R 3.';
      case 'fraction': return 'Type a fraction, like 3/4.';
      case 'fraction-unit': return young ? 'Type a fraction, like 3/4.' : 'Type a fraction, like 3/4. You can add the unit.';
      case 'decimal': return 'Type a decimal, like 0.75.';
      case 'pair': return 'Type the point, like (3, 5).';
      case 'number-unit': return young ? 'Just type the number.' : 'Type the number. You can add the unit.';
      case 'tens-ones': return 'Type the tens, a space, then the ones, like 3 8.';
      case 'list': return 'Type the numbers in order, with commas, like 7, 14, 21.';
      case 'number': return young ? 'Type a number.' : '';
      default: return '';
    }
  }

  /* ---------- number pad ---------- */
  var LAYOUT = {
    number: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '⌫', '0', '✓'],
    compare: ['<', '=', '>', '⌫', '✓'],
    time: ['1', '2', '3', '4', '5', '6', '7', '8', '9', ':', '0', '⌫', '✓'],
    cents: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '¢', '0', '⌫', '✓'],
    dollars: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '$', '0', '.', '⌫', '✓'],
    fraction: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '/', '0', 'space', '⌫', '✓'],
    decimal: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '0', '⌫', '✓'],
    remainder: ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'R', '0', '⌫', '✓'],
    'dollars-cents': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '$', '0', '¢', 'and', '⌫', '✓']
  };
  LAYOUT['number-unit'] = LAYOUT.number; LAYOUT['fraction-unit'] = LAYOUT.fraction; LAYOUT['tens-ones'] = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'space', '0', '⌫', '✓']; LAYOUT['time-ampm'] = LAYOUT.time.slice(0, -1).concat(['AM', 'PM', '✓']);

  function numberPad(host, input, opts) {
    opts = opts || {};
    var k = kind(opts.answer), keys = LAYOUT[k];
    if (!keys) return null;                                   // ordered pairs and words keep the keyboard
    var pad = G.document.createElement('div');
    pad.className = 'kid-pad kid-pad-' + k; pad.setAttribute('role', 'group'); pad.setAttribute('aria-label', 'Number pad');
    keys.forEach(function (key) {
      var b = G.document.createElement('button'); b.type = 'button';
      b.className = 'kid-key' + (key === '✓' ? ' kid-check' : key === '⌫' ? ' kid-back' : '');
      b.textContent = key === 'space' ? '␣' : key;
      b.setAttribute('aria-label', { '⌫': 'Delete', '✓': 'Check', 'space': 'Space', '<': 'less than', '>': 'greater than', '=': 'equals', '/': 'fraction bar' }[key] || key);
      b.onclick = function () {
        if (input.disabled || input.readOnly) return;
        if (key === '✓') { if (opts.onCheck) opts.onCheck(); return; }
        if (key === '⌫') input.value = input.value.slice(0, -1);
        else if (key === 'space') input.value += ' ';
        else if (key === 'and') input.value = input.value.replace(/\s+$/, '') + ' and ';
        else if (key === 'AM' || key === 'PM') input.value = input.value.replace(/\s*(AM|PM)$/i, '') + ' ' + key;
        else if (k === 'compare') input.value = key;
        else input.value += key;
        input.dispatchEvent(new G.Event('input', { bubbles: true }));
      };
      pad.appendChild(b);
    });
    if ((opts.grade || 3) <= 2) input.setAttribute('inputmode', 'none');   // Grades 1-2: on tablets, use the big pad instead of the system keyboard
    host.appendChild(pad);
    return pad;
  }

  /* ---------- screens ---------- */
  function el(tag, parent, cls, text) { var e = G.document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; if (parent) parent.appendChild(e); return e; }
  function mascot(grade) { return BASE + 'mascots/' + MASCOTS[grade || 1] + '.svg'; }

  function playScreen(host, o) {
    var box = el('section', host, 'kid-play');
    var img = el('img', box, 'kid-mascot bounce'); img.src = o.mascot || mascot(o.grade); img.alt = '';
    el('h1', box, null, o.title || 'Let’s play!');
    if (o.subtitle) el('p', box, 'kid-sub', o.subtitle);
    var b = el('button', box, 'kid-big-play', '▶  Play'); b.type = 'button';
    b.onclick = function () { box.remove(); if (o.onPlay) o.onPlay(); };
    b.focus();
    return box;
  }

  function book(unit) {
    try { var data=JSON.parse(G.localStorage.getItem('mk-sticker-book') || '{}'); return data && typeof data === 'object' && !Array.isArray(data) ? data : {}; } catch (e) { return {}; }
  }
  function saveBook(b) { try { G.localStorage.setItem('mk-sticker-book', JSON.stringify(b)); } catch (e) { /* storage blocked: the reward still shows */ } }

  function finish(host, o) {
    var m = band(o.grade), right = o.right || 0, total = o.total || 0;
    var level = right === total ? 'all' : right >= total * 0.7 ? 'most' : 'some';
    var box = el('section', host, 'kid-finish');
    var conf = el('div', box, 'kid-confetti'); conf.setAttribute('aria-hidden', 'true');
    for (var i = 0; i < 28; i++) { var c = el('i', conf); c.style.left = (i * 37 % 100) + '%'; c.style.animationDelay = (i % 7) * 0.12 + 's'; c.style.background = ['#ff8a1f', '#3547f5', '#22c08a', '#7448ff', '#ffd23f'][i % 5]; }
    var im = el('img', box, 'kid-mascot bounce'); im.src = o.mascot || mascot(o.grade); im.alt = '';
    el('h2', box, null, m.finish[level]);
    var stars = el('div', box, 'kid-stars'); stars.setAttribute('aria-label', right + ' of ' + total + ' right');
    var shown = Math.min(total, 10);
    for (var s = 0; s < shown; s++) el('span', stars, s < Math.round(right * shown / Math.max(total, 1)) ? 'on' : 'off', '★');
    el('p', box, 'kid-sub', 'You got ' + right + ' out of ' + total + '.');
    // a sticker every finished round; a trophy for a perfect round
    var b = book(), key = o.unit || 'all', have = Array.isArray(b[key]) ? b[key].filter(function(n){return STICKERS.indexOf(n)>=0;}) : [];
    var next = level === 'all' ? 'trophy' : STICKERS[(STICKERS.indexOf(have[have.length-1]) + 1) % (STICKERS.length - 1)];
    have.push(next); have = have.slice(-12); b[key] = have; saveBook(b);
    var st = el('div', box, 'kid-sticker-new');
    el('p', st, null, 'You earned a sticker!');
    var si = el('img', st, 'kid-sticker pop'); si.src = BASE + 'stickers/' + next + '.svg'; si.alt = next + ' sticker';
    var shelf = el('div', box, 'kid-book'); shelf.setAttribute('aria-label', 'My stickers');
    have.slice(-12).forEach(function (n) { var x = el('img', shelf); x.src = BASE + 'stickers/' + n + '.svg'; x.alt = ''; });
    var again = el('button', box, 'kid-big-play', '↻  Play again'); again.type = 'button';
    again.onclick = o.onAgain || function () { G.location.reload(); };
    return box;
  }

  G.MKKid = {
    kind: kind, hint: hint, numberPad: numberPad, playScreen: playScreen, finish: finish,
    praise: function (g) { return pick(band(g).praise); },
    nudge: function (g, n) { var a = band(g).nudge; return n == null ? pick(a) : a[n % a.length]; },
    lastTry: function (g) { return band(g).last; },
    MESSAGES: MSG
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = G.MKKid;
})(typeof window !== 'undefined' ? window : globalThis);
