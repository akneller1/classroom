#!/usr/bin/env node
/* Adds the Quantitative Modeling units (tools/fa-modeling/units.json) to the Classroom files that list Financial Algebra
 * units, from the extended Financial Algebra build (scripts/build-fa-extension.mjs). Rerunning replaces the same
 * entries, so it changes nothing the second time.
 *   course-integrations.js           financeUnits: the course and unit pages, cards and thumbnails
 *   course-catalog.js                integrationPreviewSkills['financial-algebra']: skills shown in previews
 *   integrated-student-skills.js     student links: skill ids and names
 *   worksheet-generator/vocabulary-data-financial.js   Vocabulary Builder decks
 * Usage: node tools/fa-modeling/sync-classroom.mjs <extended FA dir> */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const ext = path.resolve(process.argv[2] || '');
const UNITS = JSON.parse(fs.readFileSync(path.join(ROOT, 'tools/fa-modeling/units.json'), 'utf8')).units.map((u) => u.id);
const man = JSON.parse(fs.readFileSync(path.join(ext, 'financial/resources.json'), 'utf8'));
const NEW = man.units.filter((u) => UNITS.includes(u.unitId));
if (NEW.length !== UNITS.length) throw Error('extended build is missing units');
const DESC = { showdown: 'Teams choose categories and point values.', 'connect-four': 'Answer correctly to earn a disc; includes stealing.', 'tic-tac-toe': 'Solve a question to claim a square.', 'picture-reveal': 'Answer questions to uncover the mystery picture.', detective: 'Collect evidence and crack the case.' };
const rd = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8'), wr = (f, s) => fs.writeFileSync(path.join(ROOT, f), s);

// course-integrations.js
{
  let s = rd('course-integrations.js');
  const i = s.indexOf('var financeUnits='), j = s.indexOf('\n', i);
  const arr = JSON.parse(s.slice(i + 'var financeUnits='.length, j).replace(/;\s*$/, '')).filter((u) => !UNITS.includes(u.id));
  for (const u of NEW) {
    const r = u.resources;
    arr.push({ id: u.unitId, name: u.name, resources: { lessonPlan: r.lessonPlan, worksheet: r.worksheet, assessment: r.assessment, practiceTest: r.practiceTest, flashcards: r.flashcards, cheatSheet: r.cheatSheet, decisionLab: r.decisionLab, projects: r.projects, classroomBank: r.classroomBank, extendedBank: r.extendedBank, classroomGames: r.classroomGames, games: r.games.map((g) => ({ id: g.id, title: g.title, path: g.path, description: DESC[g.id] || g.description })) } });
  }
  s = s.slice(0, i) + 'var financeUnits=' + JSON.stringify(arr) + ';' + s.slice(j);
  wr('course-integrations.js', s);
}
// course-catalog.js
{
  let s = rd('course-catalog.js');
  const a = s.indexOf("integrationPreviewSkills['financial-algebra'] = {"), b = s.indexOf('\n  };', a);
  const obj = JSON.parse(s.slice(a + "integrationPreviewSkills['financial-algebra'] = ".length, b + 4).replace(/;\s*$/, ''));
  for (const u of NEW) obj[u.unitId] = u.skills.map((k) => k.name);
  s = s.slice(0, a) + "integrationPreviewSkills['financial-algebra'] = " + JSON.stringify(obj, null, 2).replace(/\n/g, '\n  ') + ';' + s.slice(b + 4);
  wr('course-catalog.js', s);
}
// integrated-student-skills.js
{
  let s = rd('integrated-student-skills.js');
  const a = s.indexOf('"financial-algebra": {'), open = s.indexOf('{', a);
  let depth = 0, k = open;
  for (; k < s.length; k++) { if (s[k] === '{') depth++; else if (s[k] === '}' && --depth === 0) break; }
  const obj = JSON.parse(s.slice(open, k + 1));
  for (const u of NEW) obj[u.unitId] = u.skills.map((x) => ({ id: x.id, name: x.name }));
  const ind = (s.slice(s.lastIndexOf('\n', a) + 1, a).match(/^\s*/) || [''])[0];
  s = s.slice(0, open) + JSON.stringify(obj, null, 2).replace(/\n/g, '\n' + ind) + s.slice(k + 1);
  wr('integrated-student-skills.js', s);
}
// worksheet-generator/vocabulary-data-financial.js
{
  let s = rd('worksheet-generator/vocabulary-data-financial.js');
  const head = 'Object.assign(window.MKVOCAB_BANKS,', i = s.indexOf(head) + head.length, j = s.lastIndexOf('});');
  const obj = JSON.parse(s.slice(i, j + 1));
  const clean = (x) => String(x).replace(/[|;]/g, ',');
  for (const u of NEW) {
    const bank = JSON.parse(fs.readFileSync(path.join(ext, 'financial/banks', u.unitId + '.json'), 'utf8'));
    obj['financial-algebra-' + u.unitId] = bank.vocab.map((v) => [v.term.replace(/^[A-Z][a-z]/, (m) => m.toLowerCase()), v.def + '.', v.example || '', `Give your own example of ${v.term.replace(/^[A-Z][a-z]/, (m) => m.toLowerCase())}`].map(clean).join('|')).join(';');
  }
  s = s.slice(0, i) + '{\n' + Object.entries(obj).map(([k, v]) => ` ${JSON.stringify(k)}: ${JSON.stringify(v)}`).join(',\n') + '\n' + s.slice(j);
  wr('worksheet-generator/vocabulary-data-financial.js', s);
}
console.log(`Classroom files list ${NEW.length} Quantitative Modeling units: ${NEW.map((u) => u.unitId).join(', ')}.`);
