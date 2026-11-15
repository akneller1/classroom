/* Matching kinds for Grades 1–5 (the elementary courses assembled from the FinancialAlgebra staging repository):
     place  Place value: base-ten blocks ↔ numeral ↔ tens and ones / expanded form ↔ number name ↔ place-value chart
     time   Telling time: analog clock ↔ digital time ↔ words
     money  Coins and bills: one collection ↔ the amount ↔ another collection worth the same
     mult   Multiplication and division: equal groups ↔ array ↔ repeated addition ↔ equation (↔ sharing story)
     efrac  Fractions: shaded model ↔ number line ↔ fraction ↔ words (equivalent and mixed-number versions)
     graph  Data: tally chart ↔ picture graph ↔ bar graph ↔ table (↔ facts for scaled graphs)
     expr   Numerical expressions: words ↔ expression ↔ value
     area   Area models: rectangle on a grid or area model ↔ multiplication ↔ partial products ↔ product
   Unit ids are the Classroom ids "grade<N>-<unit>" (the release scripts register these courses in the catalog).
   Every set is generated from its answer and every card is computed from it; MKMATCH.build checks every card
   against every other set.
   Needs: menu/match-kinds.js. */
(function (G) {
  'use strict';
  var MK = G.MKMATCH, U = MK.util, SV = MK.svg, k = U.k, esc = U.esc;
  var INK = '#16202e', BLUE = '#1d4ed8', SHADE = '#93c5fd';
  function svgOpen(W, H, label) { return '<svg class="mg-svg mk-model" viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' + label + '"><rect width="' + W + '" height="' + H + '" fill="#fff"/>'; }
  function txt(x, y, s, fs, o) { o = o || {}; return '<text x="' + x + '" y="' + y + '" text-anchor="' + (o.a || 'middle') + '" font-size="' + fs + '" font-family="Arial,sans-serif"' + (o.bold ? ' font-weight="700"' : '') + ' fill="' + (o.fill || INK) + '">' + s + '</text>'; }
  function comma(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  var ORD = { 2: ['half', 'halves'], 3: ['third', 'thirds'], 4: ['fourth', 'fourths'], 5: ['fifth', 'fifths'], 6: ['sixth', 'sixths'], 8: ['eighth', 'eighths'], 10: ['tenth', 'tenths'], 12: ['twelfth', 'twelfths'], 100: ['hundredth', 'hundredths'], 1000: ['thousandth', 'thousandths'] };
  function fracWords(n, d) { return U.words(n) + ' ' + ORD[d][n === 1 ? 0 : 1]; }

  /* ======================= PLACE VALUE ======================= */
  function blocks(n) {   // hundreds flats (up to 5 per row), tens rods, ones cubes, on one fixed scale so cards compare
    var h = Math.floor(n / 100), t = Math.floor(n / 10) % 10, o = n % 10, c = 6, F = 10 * c, W = n < 100 ? 200 : 420, out = '', x = 8, y = 8;
    for (var i = 0; i < h; i++) {
      if (i && i % 5 === 0) { x = 8; y += F + 8; }
      for (var r = 0; r < 10; r++) for (var q = 0; q < 10; q++) out += '<rect x="' + (x + q * c) + '" y="' + (y + r * c) + '" width="' + c + '" height="' + c + '" fill="#fde68a" stroke="#92400e" stroke-width="0.4"/>';
      out += '<rect x="' + x + '" y="' + y + '" width="' + F + '" height="' + F + '" fill="none" stroke="#92400e" stroke-width="1.6"/>'; x += F + 8;
    }
    var yb = h ? y + F + 10 : 8, xb = 8;
    if (h && h % 5 && x + t * (c + 5) + 30 < W) { yb = y; xb = x + 4; }   // tens and ones fit beside the last row of flats
    for (var j = 0; j < t; j++) { for (var s0 = 0; s0 < 10; s0++) out += '<rect x="' + xb + '" y="' + (yb + s0 * c) + '" width="' + c + '" height="' + c + '" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="0.4"/>'; out += '<rect x="' + xb + '" y="' + yb + '" width="' + c + '" height="' + F + '" fill="none" stroke="#1e3a8a" stroke-width="1.4"/>'; xb += c + 6; }
    if (t) xb += 6;
    for (var m = 0; m < o; m++) out += '<rect x="' + (xb + (m % 2) * (c + 3)) + '" y="' + (yb + F - (Math.floor(m / 2) + 1) * (c + 3) + 3) + '" width="' + c + '" height="' + c + '" fill="#bbf7d0" stroke="#166534" stroke-width="1"/>';
    return svgOpen(W, yb + F + 8, 'base-ten blocks') + out + '</svg>';
  }
  var PLACE_HEAD = { whole: ['Hundred Thousands', 'Ten Thousands', 'Thousands', 'Hundreds', 'Tens', 'Ones'], dec: ['Tens', 'Ones', 'Tenths', 'Hundredths', 'Thousandths'] };
  MK.register({
    id: 'place', name: 'Place Value Matching', short: 'Place Value', noun: 'number', anchor: 'num',
    anchorText: 'Start with each number already in its set', anchorHint: 'Turn this off to start from the pictures instead.',
    blurb: 'Match each <b>number</b> to the other ways of showing it: <b>base-ten blocks</b>, <b>tens and ones</b>, <b>expanded form</b>, its <b>name in words</b> or a <b>place-value chart</b>. Look-alikes use the same digits in a different order or a zero in a different place.',
    tip: 'Look at one place at a time. How many hundreds? How many tens? How many ones? A zero means none of that place.',
    types: [{ id: 'num', L: 'N', name: 'Number', plural: 'Numbers' }, { id: 'blocks', L: 'B', name: 'Base-ten blocks', plural: 'Blocks' }, { id: 'tensones', L: 'T', name: 'Tens and ones', plural: 'Tens & ones' }, { id: 'expanded', L: 'E', name: 'Expanded form', plural: 'Expanded form' }, { id: 'words', L: 'W', name: 'Number name', plural: 'Number names' }, { id: 'chart', L: 'C', name: 'Place-value chart', plural: 'Charts' }],
    units: {
      'grade1-tens-ones': { types: ['num', 'blocks', 'tensones', 'expanded'], name: 'Tens and Ones', range: [11, 99] },
      'grade2-place-value-1000': { types: ['num', 'blocks', 'expanded', 'words'], name: 'Place Value to 1,000', range: [100, 999] },
      'grade4-place-value-number-sense': { types: ['num', 'words', 'expanded', 'chart'], name: 'Place Value and Number Sense', range: [1000, 999999] },
      'grade5-place-value-number-sense': { types: ['num', 'words', 'expanded', 'chart'], name: 'Place Value and Number Sense', dec: true }
    },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true, wide: ['blocks', 'chart'],
    gen: function (rng, L, cfg, Un, sets) {
      var n;
      if (Un.dec) {   // thousandths as an integer: 4215 → 4.215
        var places = L === 'cp2' ? 2 : 3, whole = rng.int(L === 'cp2' ? 0 : 1, L === 'honors' ? 99 : 9), frac = rng.int(1, Math.pow(10, places) - 1);
        if (rng.next() < 0.3) frac = rng.pick(places === 2 ? [5, 50, 7, 70, 30, 3] : [5, 50, 500, 7, 70, 700, 205, 250, 25]);
        n = whole * 1000 + frac * (places === 2 ? 10 : 1);
      } else {
        var lo = Un.range[0], hi = Un.range[1];
        if (Un.range[1] > 99999) hi = L === 'cp2' ? 9999 : L === 'cp1' ? 99999 : 999999;
        if (Un.range[1] <= 99 && L === 'cp2') hi = 59;
        n = rng.int(lo, hi);
        if (rng.next() < 0.3) { var ds = String(n).split(''); ds[rng.int(1, ds.length - 1)] = '0'; n = +ds.join(''); }   // a zero in some place
      }
      var twin = sets.length && rng.next() < 0.45 ? rng.pick(sets) : null;
      if (twin) {   // same digits, different order (34 and 43; 305 and 350)
        var dg = String(twin.n).split(''), i1 = rng.int(0, dg.length - 1), i2 = rng.int(0, dg.length - 1), t0 = dg[i1]; dg[i1] = dg[i2]; dg[i2] = t0;
        if (dg[0] !== '0') n = +dg.join('');
      }
      if (!Un.dec && (n < Un.range[0] || n > Un.range[1])) return null;
      if (Un.dec && n % 1000 === 0) return null;
      return { n: n, dec: !!Un.dec };
    },
    key: function (t, s) { return String(s.n); },
    face: function (s, t, mode) {
      var n = s.n;
      if (s.dec) {
        var whole = Math.floor(n / 1000), fr = n % 1000, fs = ('00' + fr).slice(-3).replace(/0+$/, ''), places = fs.length, num = whole + '.' + fs;
        if (t === 'num') return U.bigTex(num);
        if (t === 'words') return '<div class="mk-txt">' + (whole ? U.words(whole) + ' and ' : '') + U.words(+fs) + ' ' + ORD[Math.pow(10, places)][+fs === 1 ? 0 : 1] + '</div>';
        if (t === 'expanded') { var terms = []; if (Math.floor(whole / 10)) terms.push(Math.floor(whole / 10) * 10); if (whole % 10) terms.push(whole % 10); fs.split('').forEach(function (d, i) { if (+d) terms.push('0.' + '0'.repeat(i) + d); }); return U.bigTex(terms.join(' + ')); }
        var dig = [Math.floor(whole / 10) || '', whole % 10].concat(('00' + fr).slice(-3).split(''));
        return '<table class="mk-tt mk-pv"><tr>' + PLACE_HEAD.dec.map(function (h0, i) { return '<th>' + h0 + '</th>' + (i === 1 ? '<th class="dot"></th>' : ''); }).join('') + '</tr><tr>' + dig.map(function (d, i) { return '<td>' + d + '</td>' + (i === 1 ? '<td class="dot">.</td>' : ''); }).join('') + '</tr></table>';
      }
      if (t === 'num') return U.bigTex(comma(n).replace(/,/g, '{,}'));
      if (t === 'blocks') return '<div class="mk-wide">' + blocks(n) + '</div>';
      if (t === 'tensones') return '<div class="mk-txt mk-big">' + Math.floor(n / 10) + ' tens ' + (n % 10) + ' ones</div>';
      if (t === 'words') return '<div class="mk-txt">' + U.words(n) + '</div>';
      if (t === 'expanded') { var ds = String(n).split(''), tt = ds.map(function (d, i) { return +d ? comma(+d * Math.pow(10, ds.length - 1 - i)) : null; }).filter(Boolean); return U.bigTex(tt.join(' + ').replace(/,/g, '{,}')); }
      var dd = ('000000' + n).slice(-6).split(''), first = dd.findIndex(function (d) { return d !== '0'; });
      return '<table class="mk-tt mk-pv"><tr>' + PLACE_HEAD.whole.map(function (h0) { return '<th>' + h0.replace(' ', '<br>') + '</th>'; }).join('') + '</tr><tr>' + dd.map(function (d, i) { return '<td>' + (i < first ? '' : d) + '</td>'; }).join('') + '</tr></table>';
    },
    summary: function (s) { return k(s.dec ? (s.n / 1000).toFixed(3).replace(/0+$/, '') : comma(s.n).replace(/,/g, '{,}')); }
  });

  /* ======================= TELLING TIME ======================= */
  function clock(h, m) {
    var C = 70, R = 60, out = svgOpen(140, 140, 'analog clock') + '<circle cx="' + C + '" cy="' + C + '" r="' + R + '" fill="#fff" stroke="' + INK + '" stroke-width="4"/>';
    for (var i = 0; i < 60; i++) { var a = i * Math.PI / 30, big = i % 5 === 0; out += '<path d="M' + (C + Math.sin(a) * (R - (big ? 9 : 4))).toFixed(1) + ' ' + (C - Math.cos(a) * (R - (big ? 9 : 4))).toFixed(1) + 'L' + (C + Math.sin(a) * (R - 1)).toFixed(1) + ' ' + (C - Math.cos(a) * (R - 1)).toFixed(1) + '" stroke="' + INK + '" stroke-width="' + (big ? 2.2 : 0.9) + '"/>'; }
    for (var hh = 1; hh <= 12; hh++) { var b = hh * Math.PI / 6; out += txt((C + Math.sin(b) * (R - 19)).toFixed(1), (C - Math.cos(b) * (R - 19) + 5).toFixed(1), hh, 13, { bold: true }); }
    var ha = ((h % 12) + m / 60) * Math.PI / 6, ma = m * Math.PI / 30;
    out += '<path d="M' + C + ' ' + C + 'L' + (C + Math.sin(ha) * 30).toFixed(1) + ' ' + (C - Math.cos(ha) * 30).toFixed(1) + '" stroke="' + INK + '" stroke-width="6" stroke-linecap="round"/>';
    out += '<path d="M' + C + ' ' + C + 'L' + (C + Math.sin(ma) * 48).toFixed(1) + ' ' + (C - Math.cos(ma) * 48).toFixed(1) + '" stroke="' + BLUE + '" stroke-width="3.5" stroke-linecap="round"/>';
    return out + '<circle cx="' + C + '" cy="' + C + '" r="4.5" fill="' + INK + '"/></svg>';
  }
  function timeWords(h, m, L, rng) {
    var nx = h % 12 + 1;
    if (m === 0) return h + ' o’clock';
    if (m === 30) return rng.next() < 0.5 ? 'half past ' + h : '30 minutes after ' + h;
    if (L !== 'cp2' && m === 15 && rng.next() < 0.6) return 'quarter past ' + h;
    if (L !== 'cp2' && m === 45 && rng.next() < 0.6) return 'quarter to ' + nx;
    if (L !== 'cp2' && m > 30 && rng.next() < 0.5) return (60 - m) + ' minute' + (60 - m === 1 ? '' : 's') + ' to ' + nx;
    return m + ' minute' + (m === 1 ? '' : 's') + ' after ' + h;
  }
  MK.register({
    id: 'time', name: 'Clock Matching', short: 'Telling Time', noun: 'time', anchor: 'analog',
    anchorText: 'Start with each clock already in its set', anchorHint: 'Recommended: students read each clock, then find the digital time and the words.',
    blurb: 'Match each <b>clock</b> to its <b>digital time</b> and the time in <b>words</b>. Look-alikes swap the hour hand and the minute hand (3:00 and 12:15).',
    tip: 'The short hand shows the hour. The long hand shows the minutes: count by 5s from the 12. At half past, the short hand is halfway between two numbers.',
    fams: { hour: 'To the hour', half: 'To the half hour', five: 'To five minutes', minute: 'To the minute' }, famLabel: 'Times',
    types: [{ id: 'analog', L: 'A', name: 'Clock', plural: 'Clocks' }, { id: 'digital', L: 'D', name: 'Digital time', plural: 'Digital' }, { id: 'words', L: 'W', name: 'Words', plural: 'Words' }],
    units: {
      'grade1-telling-time': { fams: ['hour', 'half'], def: ['hour', 'half'], name: 'Telling Time' },
      'grade2-time-money': { fams: ['half', 'five'], def: ['five'], name: 'Time and Money' },
      'grade3-time-volume-mass': { fams: ['five', 'minute'], def: ['minute'], name: 'Time, Liquid Volume, and Mass' }
    },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true,
    gen: function (rng, L, cfg, Un, sets) {
      var fam = rng.pick(cfg.fams), h = rng.int(1, 12), m = fam === 'hour' ? 0 : fam === 'half' ? rng.pick([0, 30, 30]) : fam === 'five' ? rng.int(0, 11) * 5 : rng.int(0, 59);
      var twin = sets.length && rng.next() < 0.4 ? rng.pick(sets) : null;
      if (twin && twin.m % 5 === 0) { var h2 = twin.m === 0 ? 12 : twin.m / 5, m2 = (twin.h % 12) * 5; if ((fam === 'hour' && m2 === 0) || (fam === 'half' && (m2 === 0 || m2 === 30)) || fam === 'five' || fam === 'minute') { h = h2; m = m2; } }   // hands swapped
      if (fam === 'hour' && m) return null;
      return { h: h, m: m, words: timeWords(h, m, L, rng) };
    },
    key: function (t, s) { return s.h + ':' + s.m; },
    face: function (s, t) {
      if (t === 'analog') return '<div class="mk-clock">' + clock(s.h, s.m) + '</div>';
      if (t === 'digital') return '<div class="mk-txt"><span class="mk-digital">' + s.h + ':' + ('0' + s.m).slice(-2) + '</span></div>';
      return '<div class="mk-txt">' + s.words + '</div>';
    },
    summary: function (s) { return s.h + ':' + ('0' + s.m).slice(-2); }
  });

  /* ======================= MONEY ======================= */
  var COIN = { 100: { r: 0, label: '$1', fill: '#bbf7d0', stroke: '#166534' }, 25: { r: 25, label: '25¢', fill: '#e5e7eb', stroke: '#4b5563' }, 10: { r: 17, label: '10¢', fill: '#e5e7eb', stroke: '#4b5563' }, 5: { r: 21, label: '5¢', fill: '#d1d5db', stroke: '#4b5563' }, 1: { r: 18, label: '1¢', fill: '#fdba74', stroke: '#9a3412' } };
  function coinsSvg(list) {
    var x = 8, y = 8, rowH = 0, W = 300, out = '', placed = [];
    list.forEach(function (v) {
      var c = COIN[v], w = v === 100 ? 96 : 2 * c.r, h = v === 100 ? 44 : 2 * c.r;
      if (x + w > W - 8) { x = 8; y += rowH + 8; rowH = 0; }
      if (v === 100) out += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="5" fill="' + c.fill + '" stroke="' + c.stroke + '" stroke-width="2"/><rect x="' + (x + 5) + '" y="' + (y + 5) + '" width="' + (w - 10) + '" height="' + (h - 10) + '" rx="3" fill="none" stroke="' + c.stroke + '" stroke-width="1"/>' + txt(x + w / 2, y + h / 2 + 7, '$1', 20, { bold: true, fill: c.stroke });
      else out += '<circle cx="' + (x + c.r) + '" cy="' + (y + c.r) + '" r="' + c.r + '" fill="' + c.fill + '" stroke="' + c.stroke + '" stroke-width="2.4"/>' + txt(x + c.r, y + c.r + 5, c.label, c.r > 20 ? 14 : 12, { bold: true, fill: '#1f2937' });
      x += w + 8; rowH = Math.max(rowH, h);
    });
    return svgOpen(W, y + rowH + 8, 'coins and bills') + out + '</svg>';
  }
  function makeChange(c, rng, avoid) {   // a collection worth c cents: random greedy with skipped denominations
    for (var t = 0; t < 40; t++) {
      var denoms = [100, 25, 10, 5, 1].filter(function (d) { return d <= c && (d === 1 || rng.next() < 0.75); }), left = c, out = [];
      denoms.forEach(function (d) { var most = Math.floor(left / d), use = d === 1 ? most : rng.int(Math.max(0, most - 1), most); for (var i = 0; i < use; i++) out.push(d); left -= use * d; });
      while (left > 0) { var d2 = [25, 10, 5, 1].filter(function (x) { return x <= left; })[0]; out.push(d2); left -= d2; }
      if (out.length <= 10 && (!avoid || out.join() !== avoid.join())) return out;
    }
    return null;
  }
  MK.register({
    id: 'money', name: 'Money Matching', short: 'Coins and Bills', noun: 'amount', anchor: 'amount',
    anchorText: 'Start with each amount already in its set', anchorHint: 'Recommended: students count each collection to find its amount.',
    blurb: 'Match each <b>amount</b> to <b>two different collections</b> of coins (and bills) worth exactly that much. Look-alikes use the same coins in different numbers.',
    tip: 'Count the biggest coins first: count quarters by 25s, dimes by 10s, nickels by 5s and pennies by 1s.',
    types: [{ id: 'amount', L: 'A', name: 'Amount', plural: 'Amounts' }, { id: 'coins', L: 'C', name: 'Coins', plural: 'Coins' }, { id: 'coins2', L: 'O', name: 'Another way', plural: 'Other ways' }],
    units: { 'grade2-time-money': { name: 'Time and Money' } },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true, wide: ['coins', 'coins2'],
    gen: function (rng, L, cfg, Un, sets) {
      var c = L === 'cp2' ? rng.int(6, 60) : L === 'cp1' ? rng.int(15, 99) : rng.int(105, 250);
      var twin = sets.length && rng.next() < 0.4 ? rng.pick(sets) : null;
      if (twin) c = twin.c + rng.pick([-10, -5, 5, 10, 1, -1]);
      if (L === 'cp2' && c > 60 || c < 5) return null;
      var a = makeChange(c, rng), b = a && makeChange(c, rng, a);
      if (!a || !b) return null;
      if (L === 'cp2' && a.concat(b).some(function (x) { return x === 100; })) return null;
      return { c: c, a: a, b: b };
    },
    key: function (t, s) { return String(s.c); },
    face: function (s, t) {
      if (t === 'amount') return '<div class="mk-txt mk-money">' + (s.c < 100 ? s.c + '¢' : '$' + (s.c / 100).toFixed(2)) + '</div>';
      return '<div class="mk-wide">' + coinsSvg(t === 'coins' ? s.a : s.b) + '</div>';
    },
    summary: function (s) { return s.c < 100 ? s.c + '¢' : '$' + (s.c / 100).toFixed(2); }
  });

  /* ======================= MULTIPLICATION AND DIVISION ======================= */
  function dots(n, cx, cy, r, col) { var out = '', per = Math.ceil(Math.sqrt(n)); for (var i = 0; i < n; i++) { var row = Math.floor(i / per), col2 = i % per, sz = per * 11; out += '<circle cx="' + (cx - sz / 2 + col2 * 11 + 5.5) + '" cy="' + (cy - (Math.ceil(n / per) * 11) / 2 + row * 11 + 5.5) + '" r="' + r + '" fill="' + (col || BLUE) + '"/>'; } return out; }
  function groupsSvg(g, each, label) {
    var cols = Math.min(g, 4), rows = Math.ceil(g / cols), R = 30, W = cols * 72 + 10, H = rows * 72 + 10, out = svgOpen(W, H, label || 'equal groups');
    for (var i = 0; i < g; i++) { var cx = 41 + (i % cols) * 72, cy = 41 + Math.floor(i / cols) * 72; out += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="#f8fafc" stroke="' + INK + '" stroke-width="2"/>' + dots(each, cx, cy, 4.2); }
    return out + '</svg>';
  }
  function arraySvg(r, c) { var s0 = Math.min(26, 230 / Math.max(r, c)), W = c * s0 + 16, H = r * s0 + 16, out = svgOpen(W, H, 'array'); for (var i = 0; i < r; i++) for (var j = 0; j < c; j++) out += '<circle cx="' + (8 + j * s0 + s0 / 2) + '" cy="' + (8 + i * s0 + s0 / 2) + '" r="' + (s0 * 0.34) + '" fill="' + BLUE + '"/>'; return out + '</svg>'; }
  var THINGS = [['apples', 'baskets'], ['stickers', 'friends'], ['pencils', 'boxes'], ['cookies', 'plates'], ['marbles', 'bags'], ['shells', 'buckets'], ['crayons', 'cups'], ['books', 'shelves']];
  MK.register({
    id: 'mult', name: 'Multiplication Matching', short: 'Groups and Arrays', noun: 'multiplication fact', anchor: 'eq',
    anchorText: 'Start with each equation already in its set', anchorHint: 'Turn this off to start from the pictures.',
    blurb: 'Match each <b>equation</b> to the <b>equal groups</b>, the <b>array</b>, the <b>repeated addition</b> or the <b>story</b> that shows it. Every set has a different total.',
    tip: 'Count the groups (or rows), then count how many are in each one. Groups × number in each group = total.',
    types: [{ id: 'eq', L: 'E', name: 'Equation', plural: 'Equations' }, { id: 'groups', L: 'G', name: 'Equal groups', plural: 'Groups' }, { id: 'array', L: 'A', name: 'Array', plural: 'Arrays' }, { id: 'add', L: 'R', name: 'Repeated addition', plural: 'Addition' }, { id: 'rows', L: 'W', name: 'Words', plural: 'Words' }, { id: 'story', L: 'S', name: 'Story', plural: 'Stories' }, { id: 'fact', L: 'F', name: 'Related fact', plural: 'Related facts' }],
    units: {
      'grade2-odd-even-arrays': { types: ['add', 'array', 'rows', 'eq'], name: 'Odd and Even Numbers and Arrays', max: 5, plain: true },
      'grade3-multiplication-meaning': { types: ['eq', 'groups', 'array', 'add'], name: 'Understanding Multiplication', max: 9 },
      'grade3-division-meaning': { types: ['eq', 'groups', 'fact', 'story'], name: 'Understanding Division', max: 9, div: true, short: 'Equal Sharing and Division', noun: 'division fact' }
    },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true, wide: ['groups', 'array'],
    gen: function (rng, L, cfg, Un) {
      var mx = Un.max, lo = L === 'cp2' ? 2 : 2, hi = L === 'cp2' ? Math.min(5, mx) : L === 'cp1' ? Math.min(7, mx) : mx;
      var g = rng.int(lo, hi), e = rng.int(lo, hi);
      if (Un.max === 5) { g = rng.int(2, 5); e = rng.int(2, 5); }
      var th = rng.pick(THINGS);
      return { g: g, e: e, p: g * e, things: th, div: !!Un.div, plain: !!Un.plain };
    },
    key: function (t, s) { return String(s.p); },   // every set has a different total, so no card can be read two ways
    face: function (s, t) {
      if (t === 'eq') return U.bigTex(s.div ? s.p + ' \\div ' + s.g + ' = \\,?' : s.plain ? s.g + ' \\times ' + s.e + ' = ' + s.p : s.g + ' \\times ' + s.e + ' = \\,?');
      if (t === 'groups') return '<div class="mk-wide">' + groupsSvg(s.g, s.e, s.div ? s.p + ' shared into ' + s.g + ' equal groups' : 'equal groups') + '</div>';
      if (t === 'array') return '<div class="mk-wide">' + arraySvg(s.g, s.e) + '</div>';
      if (t === 'add') return U.bigTex(Array(s.g).fill(s.e).join(' + ') + (s.plain ? ' = \\,?' : ''));
      if (t === 'rows') return '<div class="mk-txt mk-big">' + s.g + ' rows of ' + s.e + '</div>';
      if (t === 'fact') return U.bigTex(s.g + ' \\times ' + s.e + ' = ' + s.p);
      return '<div class="mk-txt">' + s.p + ' ' + s.things[0] + ' are shared equally among ' + s.g + ' ' + s.things[1] + '. How many ' + s.things[0] + ' are in each of the ' + s.things[1] + '?</div>';
    },
    summary: function (s) { return k(s.div ? s.p + ' \\div ' + s.g + ' = ' + s.e : s.g + ' \\times ' + s.e + ' = ' + s.p); }
  });

  /* ======================= FRACTIONS (elementary) ======================= */
  function fracModel(n, d, shape) {   // n shaded parts of wholes cut into d equal parts (n may exceed d)
    var wholes = Math.max(1, Math.ceil(n / d)), out = '', W, H;
    if (shape === 'circle') {
      W = wholes * 110 + 10; H = 110;
      for (var w = 0; w < wholes; w++) {
        var cx = 60 + w * 110, cy = 55, R = 46;
        for (var i = 0; i < d; i++) { var a0 = i / d * 2 * Math.PI - Math.PI / 2, a1 = (i + 1) / d * 2 * Math.PI - Math.PI / 2, on = w * d + i < n; out += '<path d="M' + cx + ' ' + cy + 'L' + (cx + R * Math.cos(a0)).toFixed(2) + ' ' + (cy + R * Math.sin(a0)).toFixed(2) + 'A' + R + ' ' + R + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + (cx + R * Math.cos(a1)).toFixed(2) + ' ' + (cy + R * Math.sin(a1)).toFixed(2) + 'Z" fill="' + (on ? SHADE : '#fff') + '" stroke="' + INK + '" stroke-width="2"/>'; }
        if (d === 1) out += '<circle cx="' + cx + '" cy="' + cy + '" r="' + R + '" fill="' + (w < n ? SHADE : '#fff') + '" stroke="' + INK + '" stroke-width="2"/>';
      }
    } else {
      var bw = 240, bh = 34, gap = 10; W = bw + 10; H = wholes * (bh + gap) - gap + 10;
      for (var w2 = 0; w2 < wholes; w2++) for (var j = 0; j < d; j++) out += '<rect x="' + (5 + j * bw / d).toFixed(2) + '" y="' + (5 + w2 * (bh + gap)) + '" width="' + (bw / d).toFixed(2) + '" height="' + bh + '" fill="' + (w2 * d + j < n ? SHADE : '#fff') + '" stroke="' + INK + '" stroke-width="2"/>';
    }
    return svgOpen(W, H, 'fraction model') + out + '</svg>';
  }
  function fracLine(n, d, max) {   // number line 0..max cut into d parts per whole, point at n/d
    var W = 330, X0 = 22, X1 = W - 22, Y = 42, sx = (X1 - X0) / max, out = svgOpen(W, 74, 'number line');
    out += '<path d="M' + X0 + ' ' + Y + 'H' + X1 + '" stroke="' + INK + '" stroke-width="2.4"/>';
    for (var i = 0; i <= d * max; i++) { var x = X0 + i / d * sx, whole = i % d === 0; out += '<path d="M' + x.toFixed(1) + ' ' + (Y - (whole ? 11 : 7)) + 'V' + (Y + (whole ? 11 : 7)) + '" stroke="' + INK + '" stroke-width="' + (whole ? 2.4 : 1.6) + '"/>'; if (whole) out += txt(x.toFixed(1), Y + 28, i / d, 16, { bold: true }); }
    return out + '<circle cx="' + (X0 + n / d * sx).toFixed(1) + '" cy="' + Y + '" r="7.5" fill="#dc2626" stroke="#fff" stroke-width="2"/></svg>';
  }
  function fracTex(n, d, mixed) { if (mixed && n > d) { var w = Math.floor(n / d), r = n % d; return r ? w + '\\tfrac{' + r + '}{' + d + '}' : String(w); } return '\\frac{' + n + '}{' + d + '}'; }
  MK.register({
    id: 'efrac', name: 'Fraction Matching', short: 'Fractions', noun: 'fraction', anchor: 'sym',
    anchorText: 'Start with each fraction already in its set', anchorHint: 'Turn this off to start from the pictures.',
    blurb: 'Match each <b>fraction</b> to a <b>shaded model</b>, a point on a <b>number line</b> and the fraction in <b>words</b> (or an <b>equivalent fraction</b>, or the same amount as a mixed number). Look-alikes share a numerator or a denominator.',
    tip: 'The bottom number tells how many equal parts make one whole. The top number tells how many of those parts. On a number line, count the jumps from 0.',
    types: [{ id: 'sym', L: 'F', name: 'Fraction', plural: 'Fractions' }, { id: 'pic', L: 'P', name: 'Model', plural: 'Models' }, { id: 'share', L: 'S', name: 'Equal shares', plural: 'Equal shares' }, { id: 'line', L: 'N', name: 'Number line', plural: 'Number lines' }, { id: 'words', L: 'W', name: 'Words', plural: 'Words' }, { id: 'equiv', L: 'Q', name: 'Equivalent fraction', plural: 'Equivalent' }, { id: 'mixed', L: 'M', name: 'Mixed number', plural: 'Mixed numbers' }],
    units: {
      'grade2-shapes-equal-shares': { types: ['words', 'pic', 'share'], name: 'Shapes and Equal Shares', pool: [[1, 2], [1, 3], [2, 3], [1, 4], [3, 4]], anchor: 'words', maxSets: 5, setOptions: [4, 5], short: 'Equal Shares' },
      'grade3-understanding-fractions': { types: ['sym', 'pic', 'line', 'words'], name: 'Understanding Fractions', dens: [2, 3, 4, 6, 8] },
      'grade3-equivalent-comparing-fractions': { types: ['sym', 'equiv', 'pic', 'line'], name: 'Equivalent and Comparing Fractions', dens: [2, 3, 4, 6, 8], equiv: true, maxSets: 5, setOptions: [4, 5], short: 'Equivalent Fractions' },
      'grade4-fractions-equivalent-fractions': { types: ['sym', 'equiv', 'pic', 'line'], name: 'Fractions and Equivalent Fractions', dens: [2, 3, 4, 5, 6, 8, 10, 12], equiv: true, short: 'Equivalent Fractions' },
      'grade5-fraction-addition-subtraction': { types: ['mixed', 'sym', 'pic', 'line'], name: 'Fraction Concepts and Operations', dens: [2, 3, 4, 5, 6, 8], improper: true, anchor: 'mixed', short: 'Mixed Numbers' }
    },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true, wide: ['pic', 'line'],
    gen: function (rng, L, cfg, Un, sets) {
      var n, d;
      if (Un.pool) { if (sets.length >= Un.pool.length) return null; var p = Un.pool[sets.length]; n = p[0]; d = p[1]; }
      else {
        var dens = Un.dens.filter(function (x) { return L === 'cp2' ? x <= 8 : true; }), twin = sets.length && rng.next() < 0.4 ? rng.pick(sets) : null;
        d = twin && rng.next() < 0.6 ? twin.d : rng.pick(dens);
        if (Un.improper) n = rng.int(d + 1, d * (L === 'cp2' ? 2 : 3) - 1);
        else if (L === 'honors' && !Un.equiv && rng.next() < 0.3) n = rng.int(d + 1, 2 * d - 1);
        else n = twin && twin.n < d && rng.next() < 0.5 ? twin.n : rng.int(1, d - 1);
        if (U.gcd(n, d) !== 1) return null;   // simplest form on the fraction card
      }
      var s = { n: n, d: d, v: n / d, shape: rng.pick(['circle', 'bar']) };
      if (Un.equiv) { var m = rng.pick([2, 3, 4]); s.en = n * m; s.ed = d * m; if (Un.dens.indexOf(s.ed) < 0) return null; }   // the equivalent fraction uses a grade-level denominator
      s.max = Math.max(1, Math.ceil(s.v - 1e-9));
      if (s.max > 3) return null;
      return s;
    },
    key: function (t, s) { return (s.v).toFixed(6); },   // equal values clash on every card
    face: function (s, t) {
      if (t === 'sym') return U.bigTex(fracTex(s.n, s.d), true);
      if (t === 'mixed') return U.bigTex(fracTex(s.n, s.d, true), true);
      if (t === 'equiv') return U.bigTex(fracTex(s.en, s.ed), true);
      if (t === 'words') return '<div class="mk-txt mk-big">' + fracWords(s.n, s.d) + '</div>';
      if (t === 'share') return '<div class="mk-txt">' + s.n + ' of ' + s.d + ' equal shares</div>';
      if (t === 'line') { var dd = s.ed && s.shape === 'circle' ? s.ed : s.d, nn = s.ed && s.shape === 'circle' ? s.en : s.n; return '<div class="mk-wide">' + fracLine(nn, dd, s.max) + '</div>'; }
      var md = s.ed && s.shape !== 'circle' ? s.ed : s.d, mn = s.ed && s.shape !== 'circle' ? s.en : s.n;   // equivalent sets: the model and the number line use different partitions
      return '<div class="mk-wide">' + fracModel(mn, md, s.shape) + '</div>';
    },
    summary: function (s) { return k(fracTex(s.n, s.d)); }
  });

  /* ======================= PICTURE GRAPHS AND BAR GRAPHS ======================= */
  var THEMES = [
    { q: 'Favorite fruit', cats: ['Apples', 'Bananas', 'Grapes', 'Oranges'] }, { q: 'Favorite pet', cats: ['Dogs', 'Cats', 'Fish', 'Birds'] },
    { q: 'How we get to school', cats: ['Bus', 'Car', 'Walk', 'Bike'] }, { q: 'Favorite season', cats: ['Winter', 'Spring', 'Summer', 'Fall'] },
    { q: 'Favorite color', cats: ['Red', 'Blue', 'Green', 'Yellow'] }
  ];
  var CAT_COLORS = ['#ef4444', '#3b82f6', '#22c55e', '#eab308'];
  function star(x, y, r, half) { var p = []; for (var i = 0; i < 10; i++) { var a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * 0.45 : r; p.push((x + rr * Math.cos(a)).toFixed(1) + ',' + (y + rr * Math.sin(a)).toFixed(1)); } return '<polygon points="' + p.join(' ') + '" fill="#f59e0b" stroke="#92400e" stroke-width="1"/>'; }
  function picGraph(cats, counts, key) {
    var W = 320, rowH = 30, H = 34 + cats.length * rowH + 30, out = svgOpen(W, H, 'picture graph');
    cats.forEach(function (c, i) { var y = 30 + i * rowH; out += txt(8, y + 5, c, 13, { a: 'start', bold: true }); for (var j = 0; j < counts[i] / key; j++) out += star(92 + j * 21, y, 9); out += '<path d="M84 ' + (y + rowH / 2) + 'H' + (W - 6) + '" stroke="#e5e7eb"/>'; });
    out += '<path d="M84 10V' + (30 + cats.length * rowH - 12) + '" stroke="' + INK + '" stroke-width="1.5"/>';
    out += star(18, H - 14, 8) + txt(32, H - 9, '= ' + key + ' ' + (key === 1 ? 'vote' : 'votes'), 13, { a: 'start', bold: true });
    return out + '</svg>';
  }
  function barGraph(cats, counts, scale, top) {
    var W = 320, H = 200, X0 = 34, Y0 = 160, out = svgOpen(W, H, 'bar graph'), sy = (Y0 - 14) / top, bw = (W - X0 - 16) / cats.length;
    for (var v = 0; v <= top; v += scale) out += '<path d="M' + X0 + ' ' + (Y0 - v * sy).toFixed(1) + 'H' + (W - 8) + '" stroke="#e5e7eb"/>' + txt(X0 - 5, (Y0 - v * sy + 4).toFixed(1), v, 11, { a: 'end' });
    cats.forEach(function (c, i) { var x = X0 + i * bw + bw * 0.18; out += '<rect x="' + x.toFixed(1) + '" y="' + (Y0 - counts[i] * sy).toFixed(1) + '" width="' + (bw * 0.64).toFixed(1) + '" height="' + (counts[i] * sy).toFixed(1) + '" fill="' + CAT_COLORS[i] + '" fill-opacity="0.8" stroke="' + INK + '" stroke-width="1.5"/>' + txt((x + bw * 0.32).toFixed(1), Y0 + 17, c, 12, { bold: true }); });
    out += '<path d="M' + X0 + ' 8V' + Y0 + 'H' + (W - 8) + '" stroke="' + INK + '" stroke-width="1.8" fill="none"/>';
    return out + '</svg>';
  }
  function tally(n) { var out = '', i; for (i = 0; i < Math.floor(n / 5); i++) out += '<span class="mk-tally5">||||</span> '; return out + '|'.repeat(n % 5); }
  MK.register({
    id: 'graph', name: 'Graph Matching', short: 'Picture and Bar Graphs', noun: 'data set', anchor: 'table',
    anchorText: 'Start with each table already in its set', anchorHint: 'Turn this off to start from the graphs.',
    blurb: 'The same survey shown different ways: match each <b>table</b> to its <b>tally chart</b>, <b>picture graph</b> and <b>bar graph</b> (or the <b>facts</b> it shows). Look-alikes swap two categories, so read every label.',
    tip: 'Read one category at a time. In a picture graph, check the key: one star may stand for more than one vote. In a bar graph, read across from the top of the bar to the scale.',
    types: [{ id: 'table', L: 'T', name: 'Table', plural: 'Tables' }, { id: 'tally', L: 'Y', name: 'Tally chart', plural: 'Tally charts' }, { id: 'pic', L: 'P', name: 'Picture graph', plural: 'Picture graphs' }, { id: 'bar', L: 'B', name: 'Bar graph', plural: 'Bar graphs' }, { id: 'facts', L: 'F', name: 'Facts', plural: 'Facts' }],
    units: {
      'grade1-data': { types: ['table', 'tally', 'pic'], name: 'Organizing and Reading Data', cats: 3, max: 8, key: 1 },
      'grade2-graphs-data': { types: ['table', 'tally', 'pic', 'bar'], name: 'Picture Graphs and Bar Graphs', cats: 4, max: 10, key: 1 },
      'grade3-graphs-measurement-data': { types: ['table', 'pic', 'bar', 'facts'], name: 'Graphs, Measurement Data, and Line Plots', cats: 4, max: 30, key: 'scaled' }
    },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true, wide: ['pic', 'bar'], printCols: { pic: 2, bar: 2, tally: 3, table: 3 },
    context: function (rng, L, cfg, Un) { var th = rng.pick(THEMES); return { q: th.q, cats: th.cats.slice(0, Un.cats), key: Un.key === 'scaled' ? rng.pick([2, 5]) : 1 }; },
    gen: function (rng, L, cfg, Un, sets) {
      var C = cfg.ctx, key = C.key, mx = Un.key === 'scaled' ? (key === 2 ? 20 : 30) : (L === 'cp2' ? Math.min(6, Un.max) : Un.max);
      var counts = C.cats.map(function () { return rng.int(1, mx / key) * key; });
      var twin = sets.length && rng.next() < 0.45 ? rng.pick(sets) : null;
      if (twin && sets.filter(function (o) { return o.counts.slice().sort().join() === twin.counts.slice().sort().join(); }).length < 2) { counts = twin.counts.slice(); var i = rng.int(0, counts.length - 1), j = (i + 1 + rng.int(0, counts.length - 2)) % counts.length, t0 = counts[i]; counts[i] = counts[j]; counts[j] = t0; }
      if (new Set(counts).size < 2) return null;
      return { counts: counts };
    },
    finish: function (sets, rng, L, cfg, Un) {
      if (cfg.types.indexOf('facts') < 0) return true;
      var cats = cfg.ctx.cats;
      var ok = sets.every(function (s) {   // one closure per set, so every fact tests its own numbers
        var made = [], tot = s.counts.reduce(function (a, b) { return a + b; }, 0);
        made.push({ text: 'In all, ' + tot + ' votes were counted.', test: function (o) { return o.counts.reduce(function (a, b) { return a + b; }, 0) === tot; } });
        cats.forEach(function (ca, a) { cats.forEach(function (cb, b) { var dlt = s.counts[a] - s.counts[b]; if (dlt > 0) made.push({ text: dlt + ' more votes for ' + ca + ' than for ' + cb + '.', test: function (o) { return o.counts[a] - o.counts[b] === dlt; } }); }); });
        var best = s.counts.indexOf(Math.max.apply(null, s.counts));
        if (s.counts.filter(function (c) { return c === s.counts[best]; }).length === 1) made.push({ text: cats[best] + ' got the most votes.', test: function (o) { return o.counts.indexOf(Math.max.apply(null, o.counts)) === best && o.counts.filter(function (c) { return c === o.counts[best]; }).length === 1; } });
        for (var t = 0; t < 120; t++) { var fs = rng.shuffle(made).slice(0, 2); if (sets.every(function (o) { return o === s || !fs.every(function (f) { return f.test(o); }); })) { s.facts = fs; return true; } }
        return false;
      });
      if (!ok) return false;
      return true;
    },
    fits: function (t, a, b) { if (t === 'facts') return !!a.facts && a.facts.every(function (f) { return f.test(b); }); return a.counts.join() === b.counts.join(); },
    face: function (s, t, mode, B) {
      var C = B.ctx;
      if (t === 'table') return '<table class="mk-tt"><tr><th>' + esc(C.q) + '</th><th>Votes</th></tr>' + C.cats.map(function (c, i) { return '<tr><td>' + c + '</td><td><b>' + s.counts[i] + '</b></td></tr>'; }).join('') + '</table>';
      if (t === 'tally') return '<table class="mk-tt mk-tally"><tr><th>' + esc(C.q) + '</th><th>Tally</th></tr>' + C.cats.map(function (c, i) { return '<tr><td>' + c + '</td><td class="tl">' + tally(s.counts[i]) + '</td></tr>'; }).join('') + '</table>';
      if (t === 'pic') return '<div class="mk-wide">' + picGraph(C.cats, s.counts, C.key) + '</div>';
      if (t === 'bar') { var top = Math.max(C.key === 1 ? 10 : C.key * 10, Math.max.apply(null, s.counts)); return '<div class="mk-wide">' + barGraph(C.cats, s.counts, C.key === 1 ? (top > 10 ? 2 : 1) : C.key, B.sets.reduce(function (m, o) { return Math.max(m, Math.max.apply(null, o.counts)); }, top)) + '</div>'; }
      return '<div class="mk-txt left">' + s.facts.map(function (f) { return '<p>' + esc(f.text) + '</p>'; }).join('') + '</div>';
    },
    legend: function (B) { return '<p><b>Survey:</b> ' + esc(B.ctx.q) + ' · ' + B.ctx.cats.map(esc).join(', ') + '</p>'; },
    summary: function (s, B) { return B.ctx.cats.map(function (c, i) { return c + ' ' + s.counts[i]; }).join(', '); }
  });

  /* ======================= NUMERICAL EXPRESSIONS (Grade 5) ======================= */
  var EXPR = [
    function (a, b, c) { return { w: 'Add ' + a + ' and ' + b + ', then multiply by ' + c + '.', e: '(' + a + ' + ' + b + ') \\times ' + c, v: (a + b) * c }; },
    function (a, b, c) { return { w: 'Multiply ' + a + ' by ' + b + ', then add ' + c + '.', e: a + ' \\times ' + b + ' + ' + c, v: a * b + c }; },
    function (a, b, c) { return { w: 'Multiply ' + b + ' by ' + c + ', then add the product to ' + a + '.', e: a + ' + ' + b + ' \\times ' + c, v: a + b * c }; },
    function (a, b, c) { return { w: c + ' times the sum of ' + a + ' and ' + b, e: c + ' \\times (' + a + ' + ' + b + ')', v: c * (a + b) }; },
    function (a, b, c) { return a <= b ? null : { w: 'Subtract ' + b + ' from ' + a + ', then multiply by ' + c + '.', e: '(' + a + ' - ' + b + ') \\times ' + c, v: (a - b) * c }; },
    function (a, b, c) { return a * b <= c ? null : { w: 'Multiply ' + a + ' and ' + b + ', then subtract ' + c + '.', e: a + ' \\times ' + b + ' - ' + c, v: a * b - c }; },
    function (a, b, c) { return (a + b) % c ? null : { w: 'Add ' + a + ' and ' + b + ', then divide by ' + c + '.', e: '(' + a + ' + ' + b + ') \\div ' + c, v: (a + b) / c }; },
    function (a, b, c, d) { return { w: 'Add ' + a + ' and ' + b + ', multiply the sum by ' + c + ', then subtract ' + d + '.', e: '[(' + a + ' + ' + b + ') \\times ' + c + '] - ' + d, v: (a + b) * c - d, hard: true }; },
    function (a, b, c, d) { return { w: 'Subtract ' + d + ' from the product of ' + c + ' and the sum of ' + a + ' and ' + b + '.', e: c + ' \\times (' + a + ' + ' + b + ') - ' + d, v: c * (a + b) - d, hard: true }; }
  ];
  MK.register({
    id: 'expr', name: 'Expression Matching', short: 'Numerical Expressions', noun: 'expression', anchor: 'words',
    anchorText: 'Start with each description already in its set', anchorHint: 'Recommended: students write each expression, then evaluate it.',
    blurb: 'Match each <b>description in words</b> to its <b>expression</b> and its <b>value</b>. Look-alikes use the same numbers in a different order of operations, such as 2 × 8 + 7 and 2 × (8 + 7).',
    tip: 'Do what is inside parentheses or brackets first, then multiply or divide, then add or subtract. “The sum of” and “then” tell you what to do first.',
    types: [{ id: 'words', L: 'W', name: 'Words', plural: 'Words' }, { id: 'expr', L: 'E', name: 'Expression', plural: 'Expressions' }, { id: 'val', L: 'V', name: 'Value', plural: 'Values' }],
    units: { 'grade5-numerical-expressions-patterns': { name: 'Numerical Expressions and Patterns' } },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true,
    gen: function (rng, L, cfg, Un, sets) {
      var twin = sets.length && rng.next() < 0.5 ? rng.pick(sets) : null, a = twin ? twin.a : rng.int(2, 12), b = twin ? twin.b : rng.int(2, 12), c = twin ? twin.c : rng.int(2, 9), d = rng.int(1, 9);
      var f = rng.pick(EXPR.slice(0, L === 'honors' ? 9 : 7)), r = f(a, b, c, d);
      if (!r || r.v < 0 || !U.isInt(r.v)) return null;
      // independent check: evaluate the printed expression
      var js = r.e.replace(/\\times/g, '*').replace(/\\div/g, '/').replace(/\[/g, '(').replace(/\]/g, ')');
      if (!/^[\d\s+\-*/()]+$/.test(js) || Function('return ' + js)() !== r.v) return null;
      return { a: a, b: b, c: c, w: r.w, e: r.e, v: r.v };
    },
    key: function (t, s) { return t === 'val' ? String(s.v) : s.e + '|' + s.v; },
    fits: function (t, a, b) { return a.v === b.v || (t !== 'val' && a.e === b.e); },
    face: function (s, t) {
      if (t === 'words') return '<div class="mk-txt">' + esc(s.w) + '</div>';
      if (t === 'expr') return U.bigTex(s.e);
      return U.bigTex(String(s.v));
    },
    summary: function (s) { return k(s.e + ' = ' + s.v); }
  });

  /* ======================= AREA MODELS ======================= */
  function gridRect(w, h) { var c = Math.min(26, 260 / Math.max(w, h)), W = w * c + 12, H = h * c + 12, out = svgOpen(W, H, 'rectangle on a grid'); for (var i = 0; i < h; i++) for (var j = 0; j < w; j++) out += '<rect x="' + (6 + j * c) + '" y="' + (6 + i * c) + '" width="' + c + '" height="' + c + '" fill="#dbeafe" stroke="#1e3a8a" stroke-width="1"/>'; return out + '<rect x="6" y="6" width="' + w * c + '" height="' + h * c + '" fill="none" stroke="' + INK + '" stroke-width="2.4"/></svg>'; }
  function split(n) { var s = String(n).split('').map(function (d, i, a) { return +d * Math.pow(10, a.length - 1 - i); }).filter(Boolean); return s; }
  function areaModel(a, b) {   // rows: parts of b; columns: parts of a; labels only (students find the partial products)
    var A = split(a), Bs = split(b), W = 320, H = 190, X0 = 40, Y0 = 30, w = W - X0 - 10, h = H - Y0 - 10;
    var cw = A.map(function (x) { return Math.max(0.22, x / a); }), sw = cw.reduce(function (p, q) { return p + q; }, 0), ch = Bs.map(function (x) { return Math.max(0.28, x / b); }), sh = ch.reduce(function (p, q) { return p + q; }, 0);
    var out = svgOpen(W, H, 'area model'), x = X0;
    A.forEach(function (v, i) { var ww = cw[i] / sw * w, y = Y0; out += txt((x + ww / 2).toFixed(1), Y0 - 9, comma(v), 15, { bold: true, fill: BLUE }); Bs.forEach(function (u, j) { var hh = ch[j] / sh * h; out += '<rect x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + ww.toFixed(1) + '" height="' + hh.toFixed(1) + '" fill="' + ((i + j) % 2 ? '#e0f2fe' : '#fef9c3') + '" stroke="' + INK + '" stroke-width="2"/>'; if (i === 0) out += txt(X0 - 7, (y + hh / 2 + 5).toFixed(1), comma(u), 15, { a: 'end', bold: true, fill: '#b45309' }); y += hh; }); x += ww; });
    return out + '</svg>';
  }
  MK.register({
    id: 'area', name: 'Area Model Matching', short: 'Area Models', noun: 'product', anchor: 'expr',
    anchorText: 'Start with each multiplication already in its set', anchorHint: 'Recommended: students build the area model for each multiplication.',
    blurb: 'Match each <b>multiplication</b> to its <b>area model</b> (or rectangle on a grid), its <b>partial products</b> and the <b>product</b>. Look-alikes share a factor, so check both sides of every rectangle.',
    tip: 'Break each factor into tens and ones (or hundreds, tens and ones). Multiply every part on the top by every part on the side, then add the partial products.',
    fams: { grid: 'Rectangles on a grid', twoone: 'Two-digit × one-digit', twotwo: 'Two-digit × two-digit', threeone: 'Three-digit × one-digit' }, famLabel: 'Products',
    types: [{ id: 'expr', L: 'E', name: 'Multiplication', plural: 'Multiplications' }, { id: 'grid', L: 'G', name: 'Rectangle', plural: 'Rectangles' }, { id: 'model', L: 'M', name: 'Area model', plural: 'Area models' }, { id: 'partial', L: 'P', name: 'Partial products', plural: 'Partial products' }, { id: 'prod', L: 'A', name: 'Product', plural: 'Products' }, { id: 'units', L: 'U', name: 'Area', plural: 'Areas' }],
    units: {
      'grade3-area': { types: ['expr', 'grid', 'units'], fams: ['grid'], def: ['grid'], name: 'Area', short: 'Area of Rectangles' },
      'grade4-multiplication-strategies': { types: ['expr', 'model', 'partial', 'prod'], fams: ['twoone', 'twotwo', 'threeone'], def: ['twoone', 'twotwo'], name: 'Multiplication Strategies and Multi-Digit Multiplication' },
      'grade5-multi-digit-multiplication-division': { types: ['expr', 'model', 'partial', 'prod'], fams: ['twotwo', 'threeone'], def: ['twotwo', 'threeone'], name: 'Multi-Digit Multiplication and Division' }
    },
    maxSets: 8, setOptions: [4, 6, 8], noGrid: true, wide: ['grid', 'model'],
    gen: function (rng, L, cfg, Un, sets) {
      var fam = rng.pick(cfg.fams), a, b, twin = sets.length && rng.next() < 0.4 ? rng.pick(sets) : null;
      if (fam === 'grid') { a = rng.int(2, L === 'cp2' ? 6 : 9); b = rng.int(2, L === 'cp2' ? 6 : 9); if (twin && twin.fam === 'grid') a = twin.a; }
      else if (fam === 'twoone') { a = rng.int(11, L === 'cp2' ? 49 : 99); b = rng.int(2, 9); }
      else if (fam === 'twotwo') { a = rng.int(11, L === 'cp2' ? 39 : 99); b = rng.int(11, L === 'cp2' ? 29 : 99); }
      else { a = rng.int(101, 999); b = rng.int(2, 9); }
      if (twin && twin.fam === fam && fam !== 'grid' && rng.next() < 0.6) a = twin.a;   // shares a factor
      if (fam !== 'grid' && (a % 10 === 0 || (b > 9 && b % 10 === 0))) return null;
      var A = split(a), Bs = split(b), parts = []; Bs.forEach(function (u) { A.forEach(function (v) { parts.push(u * v); }); });
      if (parts.reduce(function (p, q) { return p + q; }, 0) !== a * b) return null;   // independent check
      return { fam: fam, a: a, b: b, p: a * b, parts: parts };
    },
    key: function (t, s) { return String(s.p); },   // different products and different factor pairs
    fits: function (t, a, b) { return a.p === b.p || (a.a === b.a && a.b === b.b) || (a.a === b.b && a.b === b.a); },
    face: function (s, t) {
      if (t === 'expr') return U.bigTex(comma(s.a).replace(/,/g, '{,}') + ' \\times ' + s.b);
      if (t === 'grid') return '<div class="mk-wide">' + gridRect(s.a, s.b) + '</div>';
      if (t === 'units') return '<div class="mk-txt mk-big">' + s.p + ' square units</div>';
      if (t === 'model') return '<div class="mk-wide">' + areaModel(s.a, s.b) + '</div>';
      if (t === 'partial') return U.bigTex(s.parts.map(function (x) { return comma(x).replace(/,/g, '{,}'); }).join(' + '));
      return U.bigTex(comma(s.p).replace(/,/g, '{,}'));
    },
    summary: function (s) { return k(s.a + ' \\times ' + s.b + ' = ' + s.p); }
  });
})(typeof window !== 'undefined' ? window : globalThis);
