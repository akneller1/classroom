import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {loadSiteCatalog,sitePath} from './load-site-catalog.mjs';
const dir=process.argv[2]||'_site';
const {library,problems}=loadSiteCatalog(dir);assert.deepEqual(problems,[]);
const ids=new Set();let count=0;
for(const c of library.courses)for(const u of c.units||[])for(const a of u.artifacts||[]){
 if(!a.path?.startsWith('artifacts/postit-games/'))continue;
 ids.add(a.path.split('/')[2]);count++;
 assert.equal(a.type,'Game');assert.equal(a.gameMode,'Individual Review');
 for(const value of [a.path,a.thumb])assert.ok(fs.existsSync(path.join(dir,sitePath(value))),value);
}
assert.ok(ids.size>=45,'All 45 games for released courses must be indexed.');
assert.ok(count>=49,'All 49 released-unit placements must be present.');
const html=fs.readFileSync(path.join(dir,'index.html'),'utf8');
const catalogAt=html.indexOf('src="postit-games.js');
assert.ok(catalogAt>html.indexOf('src="grade2-main-catalog.js'),'Post-it supplement follows course release scripts');
assert.ok(catalogAt<html.indexOf('src="app.js'),'Post-it supplement runs before cards render');
console.log(`PASS Post-it catalog: ${ids.size} games, ${count} placements, matching pages and thumbnails.`);
