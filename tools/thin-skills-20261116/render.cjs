// Renders answer-key PNGs for the questions written by build.mjs, in the style of the existing plot keys:
// number lines 635×132, coordinate grids 436×440, Inter, blue #1f5fa8 on dark #1d2733 axes.
// Usage: node tools/thin-skills-20261116/render.cjs
'use strict';
const fs = require('node:fs'), path = require('node:path'), { chromium } = require('playwright');
const root = path.resolve(__dirname, '../..'), keys = JSON.parse(fs.readFileSync(path.join(__dirname, 'out/keys.json'), 'utf8'));
const BLUE = '#1f5fa8', DARK = '#1d2733', GRID = '#d5dbe3', FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
const label = (v) => { const s = Number.isInteger(v) ? String(Math.abs(v)) : `${Math.abs(v * 2)}/2`; return (v < 0 ? '-' : '') + s; };

function numberLine({ line, target }) {
  const W = 635, H = 132, y0 = 55, L = 29, R = 607, x = (v) => L + (v - line.min) / (line.max - line.min) * (R - L);
  let s = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="${FONT}"><rect width="${W}" height="${H}" fill="white"/>`;
  s += `<path d="M${L - 8} ${y0} H${R + 8}" stroke="${DARK}" stroke-width="2"/>`;
  s += `<path d="M${L - 10} ${y0} l9 -6 v12 z M${R + 10} ${y0} l-9 -6 v12 z" fill="${DARK}"/>`;
  const steps = Math.round((line.max - line.min) / line.tick), every = line.tick === 1 ? 2 : 1, small = line.tick !== 1;
  for (let i = 0; i <= steps; i++) {
    const v = +(line.min + i * line.tick).toFixed(8);
    s += `<path d="M${x(v)} ${y0 - 10} V${y0 + 10}" stroke="${DARK}" stroke-width="1.6"/>`;
    if (i % every === 0) s += `<text x="${x(v)}" y="98" text-anchor="middle" font-size="${small ? 13 : 15}" fill="${DARK}">${label(v)}</text>`;
  }
  const b = x(target.boundary), end = target.direction === 'left' ? L - 2 : R + 2;
  s += `<path d="M${b} ${y0} H${end + (target.direction === 'left' ? 11 : -11)}" stroke="${BLUE}" stroke-width="5"/>`;
  s += target.direction === 'left' ? `<path d="M${end} ${y0} l12 -8 v16 z" fill="${BLUE}"/>` : `<path d="M${end} ${y0} l-12 -8 v16 z" fill="${BLUE}"/>`;
  s += `<circle cx="${b}" cy="${y0}" r="${target.closed ? 10 : 9}" fill="${target.closed ? BLUE : 'white'}" stroke="${BLUE}" stroke-width="${target.closed ? 2 : 4}"/>`;
  return s + '</svg>';
}

function grid({ grid, a, b, pts }) {
  const W = 436, H = 440, x = (v) => 226 + v * 24.3, y = (v) => 212 - v * 24.3, av = eval(a), bv = eval(b);
  let s = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" font-family="${FONT}"><rect width="${W}" height="${H}" fill="white"/>`;
  s += `<rect x="${x(grid.xmin)}" y="${y(grid.ymax)}" width="${x(grid.xmax) - x(grid.xmin)}" height="${y(grid.ymin) - y(grid.ymax)}" fill="#fafbfb"/>`;
  for (let v = grid.xmin; v <= grid.xmax; v++) s += `<path d="M${x(v)} ${y(grid.ymax)} V${y(grid.ymin)}" stroke="${GRID}"/><path d="M${x(grid.xmin)} ${y(v)} H${x(grid.xmax)}" stroke="${GRID}"/>`;
  s += `<path d="M${x(grid.xmin)} ${y(0)} H${x(grid.xmax)} M${x(0)} ${y(grid.ymax)} V${y(grid.ymin)}" stroke="${DARK}" stroke-width="2"/>`;
  for (let v = grid.xmin; v <= grid.xmax; v += 2) if (v) {
    s += `<text x="${x(v)}" y="${y(grid.ymin) + 17}" text-anchor="middle" font-size="13" fill="${DARK}">${v}</text>`;
    s += `<text x="${x(grid.xmin) - 6}" y="${y(v) + 4}" text-anchor="end" font-size="13" fill="${DARK}">${v}</text>`;
  }
  s += `<text x="${x(grid.xmax) - 10}" y="${y(0) - 6}" font-size="16" font-style="italic" fill="${DARK}">x</text><text x="${x(0) + 8}" y="${y(grid.ymax) + 24}" font-size="16" font-style="italic" fill="${DARK}">y</text>`;
  let d = '', pen = false;
  for (let i = 0; i <= 400; i++) {
    const xv = grid.xmin + (grid.xmax - grid.xmin) * i / 400, yv = av * bv ** xv;
    if (yv <= grid.ymax + 0.6 && yv >= grid.ymin) { d += (pen ? ' L' : 'M') + x(xv).toFixed(2) + ' ' + y(yv).toFixed(2); pen = true; } else pen = false;
  }
  s += `<defs><clipPath id="c"><rect x="${x(grid.xmin)}" y="${y(grid.ymax)}" width="${x(grid.xmax) - x(grid.xmin)}" height="${y(grid.ymin) - y(grid.ymax)}"/></clipPath></defs>`;
  s += `<path clip-path="url(#c)" d="${d}" fill="none" stroke="${BLUE}" stroke-width="4" stroke-linecap="round"/>`;
  for (const [px, py] of pts) s += `<circle cx="${x(px)}" cy="${y(py)}" r="7.5" fill="${BLUE}"/>`;
  return s + '</svg>';
}

(async () => {
  const browser = await chromium.launch(), page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const k of keys) {
    const svg = k.kind === 'nl' ? numberLine(k) : grid(k), m = /width="(\d+)" height="(\d+)"/.exec(svg);
    await page.setViewportSize({ width: +m[1], height: +m[2] });
    await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: path.join(root, 'question-banks/assets/plot-keys', k.id + '.png'), clip: { x: 0, y: 0, width: +m[1], height: +m[2] } });
  }
  await browser.close(); console.log('Rendered ' + keys.length + ' answer keys.');
})().catch((e) => { console.error(e); process.exit(1); });
