/* Daily Lesson Planner: notes content, minutes, notes modes and the PowerPoint export (Node).
   • every key-vocabulary word has a definition and every lesson a key idea
   • every problem the planner makes (all days × levels) turns into plain text with no TeX left (MKPLAN.mathText)
   • editable minutes and the notes setting work in the engine
   • every day builds a deck (pptxgenjs from npm; skipped if it is not installed) whose slide XML has no TeX,
     no unbalanced markup, and the expected slides (title, agenda, answer slide after each problem slide)
   DAYS=all|n (default all), PPTX=0 skips the deck build. */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const env = require('../../menu/tests/load.cjs')();
env.location = { hash: process.env.COURSE === 'geometry' ? '#course=geometry' : '' };   // COURSE=geometry tests the Geometry planner
['planner/scope-algebra1.js', 'planner/lesson-skills.js', 'planner/scope-geometry.js', 'planner/lesson-skills-geometry.js', 'planner/course.js', 'planner/planner.js', 'planner/notes-content.js', 'planner/notes-data-geometry.js', 'planner/notes-geometry.js', 'planner/textmath.js', 'planner/pptx-export.js'].forEach(f =>
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', '..', f), 'utf8'), env, { filename: f }));
const P = env.MKPLAN, SC = env.MKPLAN_SCOPE;
let checks = 0; const fails = [];
const ok = (c, m) => { checks++; if (!c) fails.push(m); };
const TEX = /\\[A-Za-z]|[⟨⟩]|\^\{|_\{|\u0000|\u0001/;

// 1. glossary and key ideas
SC.days.forEach(d => {
  P.vocab(d).forEach(v => ok(P.define(v, d), 'day ' + d.day + ': no definition for "' + v + '"'));
  if (d.day_type === 'Lesson') ok(P.keyIdea(d.lesson_id), d.lesson_id + ': no key idea');
});
Object.values(P.GLOSSARY).concat(Object.values(P.KEY_IDEAS)).forEach(t => ok(!TEX.test(t) && t.length < 260, 'glossary text: ' + t));

// 2. every problem as plain text
let texts = 0;
SC.days.forEach(d => ['cp2', 'cp1', 'honors'].forEach(level => {
  const plan = P.buildDay(d.day, { level, seed: 'pp' });
  P.allItems(plan).forEach(p => {
    if (p.failed) return;
    const strs = [p.prompt || ''].concat((p.parts || []).map(x => x.prompt || ''), (p.parts || []).map(x => x.answer || ''), (p.steps || []).map(s => (s.t || '') + ' ⟨' + (s.m || '') + '⟩'), (p.work || []).map(w => '⟨' + w + '⟩'));
    strs.forEach(s => { texts++; const t = P.mathText(s); ok(!TEX.test(t), 'day ' + d.day + ' ' + p.skill + ': TeX left in "' + t + '" (from ' + s + ')'); });
  });
}));

// 3. minutes and notes modes
{
  const d = SC.days.find(x => x.day_type === 'Lesson');
  const a = P.buildDay(d.day, { seed: 'm' }), b = P.buildDay(d.day, { seed: 'm', minutes: { notes: 25, exit: 0 } });
  ok(JSON.stringify(P.allItems(a).map(p => p.key)) === JSON.stringify(P.allItems(b).map(p => p.key)), 'minutes changed the problems');
  ok(b.sections.find(s => s.id === 'notes').minutes === 25 && b.sections.find(s => s.id === 'exit').minutes === 0, 'minutes not applied');
  ok(P.totalMinutes(b) === P.totalMinutes(a) - 15 + 25 - 5, 'total minutes wrong: ' + P.totalMinutes(b));
  P.applyMinutes(b, { donow: 999, practice: -4, notes: 'x' });
  ok(b.sections[0].minutes === 180 && b.sections.find(s => s.id === 'practice').minutes === 0 && b.sections.find(s => s.id === 'notes').minutes === 15, 'minutes not clamped/reset');
  const pre = SC.days.find(x => /pre-filled/i.test(x.notes_style)), gd = SC.days.find(x => /guided/i.test(x.notes_style));
  ok(P.buildDay(pre.day).notesMode === 'filled' && P.buildDay(gd.day).notesMode === 'fill', 'notes default does not follow notes_style');
  ok(P.buildDay(gd.day, { notes: 'filled' }).notesMode === 'filled' && P.buildDay(pre.day, { notes: 'fill' }).notesMode === 'fill', 'notes setting ignored');
}

// 3b. teacher edits to the notes
{
  const d = SC.days.find(x => x.lesson_id === 'U3-L1'), rv = SC.days.find(x => x.lesson_id === 'U3-R');
  P.noteEdits['U3-L1'] = { words: [['inequality', 'edited meaning'], ['new word', 'new meaning'], ['', '']], idea: 'Edited idea', watch: '', extra: 'Line one' };
  ok(P.vocab(d).join('|') === 'inequality|new word', 'edited words: ' + P.vocab(d).join('|'));
  ok(P.define('inequality', d) === 'edited meaning' && P.define('new word', d) === 'new meaning', 'edited meanings not used');
  ok(P.keyIdea('U3-L1') === 'Edited idea' && P.watchOut(d) === '' && P.myNotes(d) === 'Line one', 'edited idea/watch/extra not used');
  ok(P.define('inequality', rv) !== 'edited meaning', 'an edit leaked into another day');
  ok(P.defaultNotes(d).idea === P.KEY_IDEAS['U3-L1'] && P.keyIdea('U3-L1') === 'Edited idea', 'defaultNotes changed the edits');
  delete P.noteEdits['U3-L1'];
  ok(P.keyIdea('U3-L1') === P.KEY_IDEAS['U3-L1'], 'removing the edit did not restore the key idea');
}

// 4. decks
(async () => {
  let PptxGenJS = null, JSZip = null;
  try { PptxGenJS = require(process.env.PPTXGEN || 'pptxgenjs'); JSZip = require(require.resolve('jszip', { paths: [path.dirname(require.resolve(process.env.PPTXGEN || 'pptxgenjs'))] })); } catch (e) { /* not installed */ }
  let decks = 0, slides = 0;
  if (process.env.PPTX !== '0' && PptxGenJS && JSZip) {
    const png = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
    const figImage = async spec => ({ data: png, w: spec.kind === 'numberline' ? 400 : 300, h: spec.kind === 'numberline' ? 62 : 300 });
    const days = process.env.DAYS && process.env.DAYS !== 'all' ? SC.days.filter((d, i) => i % Math.ceil(SC.days.length / +process.env.DAYS) === 0) : SC.days;
    for (const d of days) {
      const plan = P.buildDay(d.day, { level: ['cp2', 'cp1', 'honors'][d.day % 3], seed: 'deck', notes: d.day % 2 ? 'filled' : 'fill', minutes: d.day % 5 ? null : { donow: 7 } });
      const pres = await P.buildDeck(plan, PptxGenJS, { figImage });
      const buf = await pres.write({ outputType: 'nodebuffer' });
      const zip = await JSZip.loadAsync(buf);
      const names = Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n)).sort((a, b) => parseInt(a.match(/\d+/)) - parseInt(b.match(/\d+/)));
      decks++; slides += names.length;
      ok(names.length >= 3, 'day ' + d.day + ': only ' + names.length + ' slides');
      const texts = [];
      for (const n of names) {
        const x = await zip.file(n).async('string');
        const txt = (x.match(/<a:t>([^<]*)<\/a:t>/g) || []).map(t => t.slice(5, -6)).join(' ');
        texts.push(txt);
        ok(!TEX.test(txt.replace(/&amp;/g, '&')), 'day ' + d.day + ' ' + n + ': TeX on slide: ' + txt.slice(0, 120));
        ok(!/undefined|NaN|\[object/.test(txt.replace(/undefined slope|vertical undefined|slope is undefined|is undefined/g, '')), 'day ' + d.day + ' ' + n + ': bad text: ' + txt.slice(0, 120));
      }
      ok(texts[0].indexOf(d.title.replace(/&/g, '&amp;')) >= 0, 'day ' + d.day + ': title slide missing the title');
      ok(/Today's plan|Today&apos;s plan/.test(texts[1]), 'day ' + d.day + ': no agenda slide');
      const nProb = P.allItems(plan).length, nAns = texts.filter(t => /Answers/.test(t)).length;
      if (nProb) ok(nAns > 0, 'day ' + d.day + ': problems but no answer slides');
      if (d.day % 5 === 0 && plan.sections[0].id === 'donow' && plan.sections[0].groups.length && plan.sections[0].groups[0].items.length) ok(texts.some(t => /7 min/.test(t)), 'day ' + d.day + ': edited minutes not on the slides');
      if (d.day_type === 'Lesson') ok(texts.some(t => t.indexOf(P.keyIdea(d.lesson_id).slice(0, 30).replace(/&/g, '&amp;').replace(/'/g, '&apos;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;')) >= 0), 'day ' + d.day + ': key idea not on the slides');
    }
  }
  fails.slice(0, 30).forEach(f => console.log('FAIL', f));
  console.log('planner notes + slides: ' + checks + ' checks, ' + texts + ' texts converted, ' + (decks ? decks + ' decks (' + slides + ' slides)' : 'decks skipped (pptxgenjs not installed)') + ', ' + fails.length + ' failures');
  process.exit(fails.length ? 1 : 0);
})();
