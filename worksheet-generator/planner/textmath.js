/* Daily Lesson Planner — TeX → plain editable text (for the PowerPoint export).

   MKPLAN.mathText('Solve ⟨\frac{x}{3}-1\le -2⟩.')  →  'Solve x/3 − 1 ≤ −2.'
   Text outside ⟨…⟩ is kept as it is; math inside is turned into Unicode a teacher can edit in PowerPoint:
   fractions a/b (parenthesised when needed), x², a₃, √(…), ≤ ≥ ± · × ÷ ≈ …, a real minus sign and spaces
   around operators. Exponents that have no Unicode superscript are written ^(…).
   tests/planner-tests.cjs converts every problem the planner makes and checks no TeX is left. */
(function (G) {
  'use strict';
  var P = (G.MKPLAN = G.MKPLAN || {});
  var SUP = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '+': '⁺', '−': '⁻', '-': '⁻', '(': '⁽', ')': '⁾', 'n': 'ⁿ', 'x': 'ˣ', 't': 'ᵗ' };
  var SUB = { '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '+': '₊', '−': '₋', '-': '₋', 'n': 'ₙ' };
  var SYM = { le: '≤', ge: '≥', leq: '≤', geq: '≥', lt: '<', gt: '>', ne: '≠', neq: '≠', pm: '±', mp: '∓', cdot: '·', times: '×', div: '÷', approx: '≈',
    dots: '…', ldots: '…', cdots: '⋯', infty: '∞', pi: 'π', to: '→', Rightarrow: '⇒', cup: '∪', cap: '∩', in: '∈', emptyset: '∅', varnothing: '∅',
    circ: '°', degree: '°', theta: 'θ', alpha: 'α', beta: 'β', Delta: 'Δ', mid: '|', vert: '|', quad: ' ', qquad: ' ', colon: ':', prime: '′' };
  function mapAll(s, table) { var out = ''; for (var i = 0; i < s.length; i++) { if (!table[s[i]]) return null; out += table[s[i]]; } return out; }
  function atomic(s) { return /^[−-]?[0-9.]+$/.test(s) || /^[A-Za-zα-ωπ]$/.test(s) || /^[0-9.]*[A-Za-z]$/.test(s) || /^\(.*\)$/.test(s) && balanced(s.slice(1, -1)) || /^√/.test(s) && atomic(s.slice(1)); }
  function balanced(s) { var d = 0; for (var i = 0; i < s.length; i++) { if (s[i] === '(') d++; else if (s[i] === ')') { d--; if (d < 0) return false; } } return d === 0; }
  function wrap(s) { s = s.trim(); return atomic(s) ? s : '(' + s + ')'; }

  /* Parse TeX into plain text. i = position in src; stops at an unmatched '}' (returns the end index). */
  function conv(src) {
    var pos = 0;
    function group() {   // {…} or a single token
      while (src[pos] === ' ') pos++;
      if (src[pos] === '{') { pos++; var s = seq(true); pos++; return s; }
      if (src[pos] === '\\') { return command(); }
      return src[pos++] || '';
    }
    function command() {
      pos++;   // skip backslash
      var m = /^[A-Za-z]+/.exec(src.slice(pos));
      if (!m) { var ch = src[pos++]; return ch === ' ' || ch === ',' || ch === ';' || ch === ':' || ch === '!' ? (ch === '!' ? '' : ' ') : ch; }   // \  \, \{ \} \% \$ \|
      var name = m[0]; pos += name.length;
      if (name === 'frac' || name === 'dfrac' || name === 'tfrac') {
        var a = group(), b = group();
        var f = wrap(a) + '/' + wrap(b);
        var next = src.slice(pos).replace(/^\s+/, '');
        if (/^[A-Za-z(\\]/.test(next) && !/^\\(le|ge|lt|gt|ne|pm|cdot|times|div|approx|text|right|dots|quad)/.test(next)) f = '(' + f + ')';   // (1/2)x, (3/4)(x + 1)
        return { frac: f };
      }
      if (name === 'sqrt') {
        var idx = '';
        if (src[pos] === '[') { var e = src.indexOf(']', pos); idx = src.slice(pos + 1, e); pos = e + 1; }
        var r = group(), root = idx === '3' ? '∛' : idx === '4' ? '∜' : idx ? idx + '√' : '√';
        return root + (/^[0-9A-Za-z]+$/.test(r) ? r : '(' + r + ')');
      }
      if (name === 'left' || name === 'right' || name === 'big' || name === 'Big' || name === 'bigl' || name === 'bigr') {
        if (src[pos] === '\\') { pos++; var d = src[pos++]; return d === '{' ? '{' : d === '}' ? '}' : d === '|' ? '|' : (/[A-Za-z]/.test(d) ? (function () { var mm = /^[A-Za-z]*/.exec(src.slice(pos)); pos += mm[0].length; var nm = d + mm[0]; return nm === 'vert' ? '|' : nm === 'langle' ? '⟨' : nm === 'rangle' ? '⟩' : ''; })() : d); }
        var dl = src[pos++]; return dl === '.' ? '' : dl;
      }
      if (name === 'text' || name === 'textbf' || name === 'mathrm' || name === 'textit' || name === 'mbox' || name === 'operatorname') { pos++; var t = ''; var depth = 1; while (pos < src.length && depth) { if (src[pos] === '{') depth++; else if (src[pos] === '}') { depth--; if (!depth) break; } t += src[pos++]; } pos++; return { text: t }; }
      if (name === 'mathbb') { var bb = group(); return { R: 'ℝ', Z: 'ℤ', N: 'ℕ', Q: 'ℚ' }[bb] || bb; }
      if (name === 'overline') return group() + '̅';
      if (SYM[name] !== undefined) return SYM[name];
      return name;   // unknown command: keep its name rather than lose it
    }
    function seq(inGroup) {
      var parts = [];
      while (pos < src.length) {
        var c = src[pos];
        if (c === '}') { if (inGroup) break; pos++; continue; }
        if (c === '{') { pos++; parts.push(seq(true)); pos++; continue; }
        if (c === '\\') { parts.push(command()); continue; }
        if (c === '^' || c === '_') {
          pos++;
          var g = group(); if (g && g.frac) g = g.frac.replace(/^\((.*)\)$/, '$1');
          if (g && g.text !== undefined) g = g.text;
          var raw = String(g).replace(/\s+/g, '').replace(/-/g, '−');
          var u = mapAll(raw, c === '^' ? SUP : SUB);
          parts.push({ op: u !== null ? u : c + (raw.length === 1 ? raw : '(' + raw + ')') });
          continue;
        }
        parts.push(c); pos++;
      }
      return parts.map(function (p) { return typeof p === 'string' ? p : p.frac !== undefined ? p.frac : p.text !== undefined ? '\u0000' + p.text + '\u0001' : p.op; }).join('');
    }
    var out = seq(false);
    return out;
  }
  /* Spaces around operators and a real minus sign; text from \text{…} (between \0 and \1) is kept as written. */
  function tidy(s) {
    var pieces = s.split(/(\u0000[^\u0001]*\u0001)/);
    return pieces.map(function (p) {
      if (p[0] === '\u0000') return p.slice(1, -1);
      p = p.replace(/\s+/g, ' ');
      var out = '', prev = '';
      for (var i = 0; i < p.length; i++) {
        var c = p[i];
        if (c === ' ') { if (out && out[out.length - 1] !== ' ') out += ' '; continue; }
        if (/[=<>≤≥≠≈·×÷]/.test(c)) { out = out.replace(/ $/, '') + (out ? ' ' : '') + c + ' '; prev = c; continue; }
        if (c === '+' || c === '-' || c === '−' || c === '±') {
          var sign = c === '-' ? '−' : c;
          var binary = /[0-9A-Za-zα-ωπ)\]}|²³¹⁰⁴⁵⁶⁷⁸⁹ⁿˣᵗ⁾′…∞_^₀₁₂₃₄₅₆₇₈₉ₙ%]/.test(prev);
          out = binary ? out.replace(/ $/, '') + ' ' + sign + ' ' : out + sign;
          prev = binary ? sign + ' ' : sign; continue;
        }
        out += c; prev = c;
      }
      return out;
    }).join('').replace(/ +/g, ' ').replace(/\( /g, '(').replace(/ \)/g, ')').replace(/ ,/g, ',').trim();
  }
  P.texToText = function (tex) { return tidy(conv(String(tex || ''))); };
  P.mathText = function (s) {
    return String(s === undefined || s === null ? '' : s).replace(/⟨([^⟩]*)⟩/g, function (_, m) { return P.texToText(m); }).replace(/\s+([.,;:?!])(\s|$)/g, '$1$2').replace(/ {2,}/g, ' ').trim();
  };
})(typeof window !== 'undefined' ? window : globalThis);
