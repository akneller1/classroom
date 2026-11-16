/* read-aloud.js — say a Grades 1-5 question the way a teacher would read it.
 *
 *   MKReadAloud.speakable(text, {grade})  -> plain words for a speech voice ("9 + ___ = 10" -> "9 plus blank equals 10")
 *   MKReadAloud.speak(text, {grade})      -> reads it with the browser's built-in voice (no outside service, no data sent)
 *   MKReadAloud.button(host, getText, {grade}) -> adds a 🔊 "Read to me" button to host
 *
 * Works on prompts, choices and hints. Tested on every Grade 1-5 prompt and choice (see test-read-aloud.cjs).
 */
(function (G) {
  'use strict';
  var ORD = { 2: ['half', 'halves'], 3: ['third', 'thirds'], 4: ['fourth', 'fourths'], 5: ['fifth', 'fifths'], 6: ['sixth', 'sixths'],
    7: ['seventh', 'sevenths'], 8: ['eighth', 'eighths'], 9: ['ninth', 'ninths'], 10: ['tenth', 'tenths'], 12: ['twelfth', 'twelfths'],
    100: ['hundredth', 'hundredths'], 1000: ['thousandth', 'thousandths'] };
  var SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', 'ⁿ': 'n' };
  var UNITS = { cm: 'centimeters', mm: 'millimeters', km: 'kilometers', m: 'meters', in: 'inches', ft: 'feet', yd: 'yards', mi: 'miles',
    kg: 'kilograms', g: 'grams', lb: 'pounds', oz: 'ounces', mL: 'milliliters', L: 'liters', qt: 'quarts', pt: 'pints', gal: 'gallons',
    sec: 'seconds', min: 'minutes', hr: 'hours' };

  function fraction(n, d) {
    var name = ORD[d] || null;
    if (!name) return n + ' over ' + d;
    return n + ' ' + (Number(n) === 1 ? name[0] : name[1]);
  }

  function speakable(text, opts) {
    var grade = (opts && opts.grade) || 3;
    var s = String(text == null ? '' : text);
    s = s.replace(/‑|‐/g, '-').replace(/[“”]/g, '"').replace(/’/g, "'").replace(/…/g, ', and so on');
    s = s.replace(/([.?!:])\s*\n\s*/g, '$1 ').replace(/\s*\n\s*/g, '. ');
    // exponents: 10³ -> 10 to the 3rd power
    s = s.replace(/(\d+)([⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ]+)/g, function (_, b, e) {
      var x = e.split('').map(function (c) { return SUP[c]; }).join('');
      return b + (x === '2' ? ' squared' : x === '3' ? ' cubed' : ' to the power of ' + x);
    });
    // money. A choice written the wrong way on purpose ("15$", "$¢15", "$74¢") is read symbol by symbol, so the child hears what is printed.
    if (/\d\$|\$¢|¢\d|\$\d+¢/.test(s)) s = s.replace(/\$/g, ' dollar sign ').replace(/¢/g, ' cent sign ');
    // money
    s = s.replace(/\$(\d[\d,]*)\.(\d\d)\b/g, function (_, d, c) { return d + ' dollars and ' + Number(c) + ' cents'; });
    s = s.replace(/\$(\d[\d,]*)/g, function (_, d) { return d + (d === '1' ? ' dollar' : ' dollars'); });
    s = s.replace(/(\d+)\s*¢/g, function (_, c) { return c + (c === '1' ? ' cent' : ' cents'); });
    // times of day: 4:00 -> 4 o'clock, 7:05 -> 7 oh 5, 7:30 -> 7 30
    s = s.replace(/\b(\d{1,2}):(\d\d)(?:\s*(AM|PM|a\.m\.|p\.m\.))?/g, function (_, h, m, ap) {
      var t = m === '00' ? h + " o'clock" : m[0] === '0' ? h + ' oh ' + m[1] : h + ' ' + m;
      return t + (ap ? ' ' + ap.replace(/\./g, '').toUpperCase().split('').join(' ') : '');
    });
    // remainders: 12 R 3
    s = s.replace(/(\d)\s*R\s*(\d)/g, '$1 remainder $2');
    // mixed numbers and fractions
    s = s.replace(/\b(\d+)\s+(\d+)\/(\d+)\b/g, function (_, w, n, d) { return w + ' and ' + fraction(n, Number(d)); });
    s = s.replace(/\b(\d+)\/(\d+)\b/g, function (_, n, d) { return fraction(n, Number(d)); });
    // decimals: 0.75 -> 0 point 7 5
    s = s.replace(/\b(\d+)\.(\d+)\b/g, function (_, w, f) { return w + ' point ' + f.split('').join(' '); });
    // units after a number. Short words that are also English (in, m, g, L) count as units only before punctuation or the end.
    s = s.replace(/(\d)\s*(cm|mm|km|kg|mL|ft|yd|mi|lb|oz|qt|gal|sec|hr)\b/g, function (_, d, u) { return d + ' ' + UNITS[u]; });
    s = s.replace(/(\d)\s*(in|m|g|L|pt|min)\.?(?=\s*(?:[,;:)?!]|$|\s(?:and|or|by|long|wide|tall)\b))/g, function (_, d, u) { return d + ' ' + UNITS[u]; });
    s = s.replace(/(\d)\s*°/g, '$1 degrees');
    // a missing digit inside a number ("59,_68"): read the digits one by one
    s = s.replace(/\b[\d,]*\d[\d,]*_[\d,]*|\b_[\d,]*\d[\d,]*/g, function (tok) {
      return tok.replace(/,/g, '').split('').map(function (c) { return c === '_' ? 'blank' : c; }).join(', ');
    });
    // blanks and unknowns
    s = s.replace(/_{2,}|□|▢/g, ' blank ').replace(/△/g, ' triangle ');
    s = s.replace(/=\s*\?/g, '= what number').replace(/\?\s*([+\-−×÷=])/g, 'what number $1');
    s = s.replace(/(^|[\s,(])\?(?=[\s.,)]|$)/g, '$1blank');      // a '?' standing alone is a placeholder: "10, 20, ?" / "where the ? is"
    // operation and comparison symbols
    s = s.replace(/≈/g, ' is about ').replace(/≤/g, ' is less than or equal to ').replace(/≥/g, ' is greater than or equal to ');
    s = s.replace(/\s*<\s*/g, ' is less than ').replace(/\s*>\s*/g, ' is greater than ');
    s = s.replace(/\s*−\s*/g, ' minus ');                                   // the math minus sign is always 'minus'
    s = s.replace(/(\d|\)|blank)\s+-\s+(?=\d|\(|blank|what)/g, '$1 minus ');   // a typed hyphen between numbers
    s = s.replace(/\s*\+\s*/g, ' plus ').replace(/\s*×\s*/g, ' times ').replace(/\s*÷\s*/g, ' divided by ').replace(/\s*=\s*/g, ' equals ');
    s = s.replace(/\s*→\s*/g, ', ');
    s = s.replace(/[\[\{]/g, '(').replace(/[\]\}]/g, ')');
    // read single-symbol choices aloud: "Which symbol goes in the blank: >, <, or ="
    s = s.replace(/: is greater than , is less than , or equals\b/g, ': greater than, less than, or equals');
    return s.replace(/\s+/g, ' ').replace(/\s+([.,?!])/g, '$1').trim();
  }

  var current = null;
  function speak(text, opts) {
    if (!G.speechSynthesis || typeof G.SpeechSynthesisUtterance !== 'function') return false;
    G.speechSynthesis.cancel();
    var u = new G.SpeechSynthesisUtterance(speakable(text, opts));
    u.rate = (opts && opts.rate) || ((opts && opts.grade) <= 2 ? 0.85 : 0.95);
    u.lang = 'en-US';
    current = u; G.speechSynthesis.speak(u);
    return true;
  }

  function button(host, getText, opts) {
    var b = G.document.createElement('button');
    b.type = 'button'; b.className = 'el-read-aloud'; b.setAttribute('aria-label', 'Read the question out loud');
    b.innerHTML = '<span aria-hidden="true">🔊</span> Read to me';
    if (!G.speechSynthesis || typeof G.SpeechSynthesisUtterance !== 'function') { b.disabled = true; b.title = 'This browser cannot read aloud.'; }
    b.onclick = function () { speak(typeof getText === 'function' ? getText() : getText, opts); };
    host.appendChild(b);
    return b;
  }

  G.MKReadAloud = { speakable: speakable, speak: speak, button: button };
  if (typeof module !== 'undefined' && module.exports) module.exports = G.MKReadAloud;
})(typeof window !== 'undefined' ? window : globalThis);
