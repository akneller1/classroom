// Whole-site audit 2, item #4 (2026-11-20): printed cumulative practice tests for Grades 3 and 4, Grade 8, Algebra 1,
// Geometry and Algebra 2.
//
// Each test is made by the site's own Assessment Generator (worksheet-generator/menu-assessment.html), so every question
// is generated and independently verified by the same engine teachers use (menu/verify.js and the approved banks). For
// each unit of the course the generator builds a small unit test with a fixed seed: 2 multiple-choice questions and
// 1 short-answer question (3 and 2 for Grade 8, which has 7 units). The unit tests are then merged into one cumulative test with two parts, rendered with the
// generator's own print layout, and saved as exam.pdf and teacher-key.pdf (plus a card thumbnail). Tests A and B use
// different seeds. A list of the questions goes to practice-tests.json for the tests in scripts/test-site-audit.cjs.
//
// Usage (repository root, after a local site build in _site):  node tools/site-audit-20261120/practice_tests/build.cjs
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '../../..'), SITE = path.join(ROOT, '_site');
const MIME = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf' };

const COURSES = [
  { slug: 'grade3', prefix: 'grade3-', name: 'Grade 3', eyebrow: '3rd Grade Math' },
  { slug: 'grade4', prefix: 'grade4-', name: 'Grade 4', eyebrow: '4th Grade Math' },
  { slug: 'grade8', prefix: 'prealgebra-', name: 'Grade 8', eyebrow: '8th Grade Math', mc: 3, sa: 2 },
  { slug: 'algebra1', prefix: 'algebra1-', name: 'Algebra 1', eyebrow: 'Algebra 1' },
  { slug: 'geometry', prefix: 'geometry-', name: 'Geometry', eyebrow: 'Geometry' },
  { slug: 'algebra2', prefix: 'algebra2-', name: 'Algebra 2', eyebrow: 'Algebra 2' },
];
const SEEDS = { a: 20261120, b: 20261121 };

async function route(ctx) {
  await ctx.route('**/*', async (r) => {
    const u = new URL(r.request().url());
    if (u.hostname !== 'site.test') return r.abort();
    let p = path.join(SITE, decodeURIComponent(u.pathname));
    if (fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, 'index.html');
    if (!fs.existsSync(p)) return r.fulfill({ status: 404, body: '' });
    r.fulfill({ status: 200, contentType: MIME[path.extname(p)] || 'application/octet-stream', body: fs.readFileSync(p) });
  });
}

// Runs in the page: build one cumulative test and return the student and key pages as HTML, plus the item list.
async function buildTest(page, course, ex) {
  return page.evaluate(async ({ course, ex, seed }) => {
    const NS = window.MKMENU;
    const units = Object.keys(NS.skillSets).filter((u) => u.indexOf(course.prefix) === 0).sort((a, b) => {
      const o = window.MK_COURSE_ORDER || null; return 0;
    });
    const mc = [], sa = [], log = [];
    let first = null;
    for (const [ui, unit] of units.entries()) {
      const cfg = NS.defaultConfig(unit, 'test');
      cfg.seed = seed + ui * 7919;
      cfg.level = 'cp1';
      Object.keys(cfg.skills).forEach((k) => { if (/^vocab_|mcas-context|investigation|open-response/.test(k)) cfg.skills[k] = false; });
      cfg.sections = [Object.assign({}, cfg.sections[0], { offered: course.mc || 2, required: course.mc || 2, qformat: 'mc', points: 1, skills: null }),
                      Object.assign({}, cfg.sections[1] || cfg.sections[0], { id: 'sa-' + ui, offered: course.sa || 1, required: course.sa || 1, qformat: 'open', points: 2, skills: null })];
      let st = NS.newAssessment(cfg);
      for (let tries = 0; tries < 6 && st.versions[0].sections.some((s) => s.items.some((it) => it.failed)); tries++) {
        cfg.seed += 101; st = NS.newAssessment(cfg);
      }
      if (!first) first = st;
      const set = NS.skillSets[unit];
      st.versions[0].sections[0].items.forEach((it) => { if (!it.failed) mc.push(Object.assign(it, { _unit: set.unitName, _set: unit })); else log.push(unit + ' mc failed: ' + it.reason); });
      st.versions[0].sections[1].items.forEach((it) => { if (!it.failed) sa.push(Object.assign(it, { _unit: set.unitName, _set: unit })); else log.push(unit + ' sa failed: ' + it.reason); });
    }
    const state = first;
    const cfg = state.config;
    cfg.title = course.name + ' Cumulative Practice Test ' + ex.toUpperCase();
    cfg.subtitle = 'Covers every unit · answer every question';
    cfg.layout = Object.assign({}, cfg.layout, { reference: false, guide: true });
    cfg.sections = [Object.assign({}, cfg.sections[0], { name: 'Multiple Choice', note: 'Choose the best answer.', offered: mc.length, required: mc.length, points: 1 }),
                    Object.assign({}, cfg.sections[1], { name: 'Short Answer', note: 'Show your work.', offered: sa.length, required: sa.length, points: 2 })];
    state.versions = [{ label: 'A', sections: [{ id: cfg.sections[0].id, items: mc }, { id: cfg.sections[1].id, items: sa }] }];
    // The print layout looks skills up in the first unit's set; let it see every unit's skills (this page only).
    const base = NS.skillSets[cfg.unitId];
    mc.concat(sa).forEach((it) => {
      const rec = NS.skillSets[it._set].byId[it.skill];
      if (!rec) return;
      // bank-backed skills are tagged with their id; show the skill name in the key's skill table instead
      base.byId[it.skill] = /-skill-\d+$/.test(rec.tag || '') || !rec.tag ? Object.assign({}, rec, { tag: rec.name }) : rec;
    });
    // Group the key's skill table by unit: "Skill group" = unit, "What it covers" = the skills tested from it.
    base.tags = Object.assign({}, base.tags);
    mc.concat(sa).forEach((it) => {
      const rec = NS.skillSets[it._set].byId[it.skill], names = (base.tags[it._unit] || '').split('; ').filter(Boolean);
      if (rec && !names.includes(rec.name)) names.push(rec.name);
      base.tags[it._unit] = names.join('; ');
      it.tag = it._unit;
    });
    base.unitName = 'All units';   // the elementary print header names the unit; this test covers them all
    const html = async (kind) => (await NS.renderPages(state, 0, kind)).map((p) => p.outerHTML).join('')
      .replace(/(<div class="el-titlewrap">.*?<h1>)[^<]*(<\/h1>)/g, (m, a, b) => a + cfg.title + b);
    const plain = (s) => { const d = document.createElement('div'); d.innerHTML = String(s || ''); return d.textContent; };
    return {
      student: await html('student'), key: await html('key'), log,
      items: mc.concat(sa).map((it) => ({ unit: it._unit, skill: it.skill, verify: it.verify && it.verify.status, prompt: plain(it.prompt).slice(0, 160) })),
      counts: { mc: mc.length, sa: sa.length },
    };
  }, { course, ex, seed: SEEDS[ex] });
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  await route(ctx);
  const page = await ctx.newPage();
  page.on('pageerror', (e) => console.log('page error:', e.message));
  const record = {};
  for (const course of COURSES.filter((c) => !process.env.ONLY || process.env.ONLY.split(',').includes(c.slug))) {
    for (const ex of ['a', 'b']) {
      await page.goto('http://site.test/worksheet-generator/menu-assessment.html#unit=' + course.prefix);
      await page.waitForFunction(() => window.MKMENU && Object.keys(window.MKMENU.skillSets).length > 50, null, { timeout: 30000 });
      await page.waitForTimeout(1500);
      const t = await buildTest(page, course, ex);
      if (t.log.length) console.log(course.slug, ex, t.log.join('; '));
      const slug = `${course.slug}-practice-test-${ex}`, dir = path.join(ROOT, 'artifacts', slug);
      fs.mkdirSync(dir, { recursive: true });
      for (const [kind, out] of [['student', 'exam.pdf'], ['key', 'teacher-key.pdf']]) {
        await page.evaluate((h) => {
          document.body.innerHTML = '<div id="pt-print">' + h + '</div>';
          const s = document.createElement('style');
          s.textContent = '@page{size:letter;margin:0} body{margin:0;background:#fff} #pt-print .page{box-shadow:none;margin:0 auto;break-after:page}';
          document.head.appendChild(s);
        }, t[kind]);
        await page.waitForTimeout(400);
        await page.pdf({ path: path.join(dir, out), format: 'Letter', printBackground: true, preferCSSPageSize: true });
        if (kind === 'student') {
          await page.setViewportSize({ width: 816, height: 1056 });
          const tmp = path.join(require('os').tmpdir(), 'thumb-' + slug + '.png');
          await page.screenshot({ path: tmp, clip: { x: 0, y: 0, width: 816, height: 510 } });
          execFileSync('python3', ['-c', `from PIL import Image\nIm=Image.open('${tmp}').convert('RGB').resize((720,450),Image.LANCZOS)\nIm.save('${path.join(ROOT, 'thumbs', slug + '.jpg')}',quality=86)`]);
        }
      }
      record[slug] = { counts: t.counts, items: t.items };
      console.log(slug, t.counts, 'unverified:', t.items.filter((i) => i.verify && i.verify !== 'verified').length);
    }
  }
  fs.writeFileSync(path.join(__dirname, 'practice-tests.json'), JSON.stringify(record, null, 1) + '\n');
  await browser.close();
})();
