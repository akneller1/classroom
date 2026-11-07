/* Regression checks for the 2026-11-07 tool update and its student-share routing. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),ctx={window:{}};
for(const file of ['data.js','student-game-share.js'])vm.runInNewContext(fs.readFileSync(path.join(root,file),'utf8'),ctx,{filename:file});
const courses=ctx.window.LIBRARY.courses;
for(const [id,count] of [['statistics',4],['discrete',10]]){const c=courses.find(c=>c.id===id);assert(c&&c.planned&&c.units.length===count,'New course outline lost: '+id);}
const manifest=JSON.parse(fs.readFileSync(path.join(root,'tools/interactive-math-20261107/manifest.json'),'utf8'));
assert.equal(manifest.tools.length,14);
for(const tool of manifest.tools){
 const unit=courses.find(c=>c.id===tool.course)?.units.find(u=>u.id===tool.unit);
 const resource=unit?.artifacts.find(a=>a.path===`artifacts/${tool.slug}/index.html`);
 assert(resource&&resource.bankFormat==='interactive-math','Missing course placement: '+tool.slug);
 for(const file of [resource.path,resource.worksheet,resource.answerKey,resource.thumb])assert(file&&fs.existsSync(path.join(root,file)),'Missing tool resource: '+file);
 const html=fs.readFileSync(path.join(root,resource.path),'utf8');
 for(const src of ['../interactive-math/lab.js','../interactive-math/lab-plus.js'])assert(html.includes(src),'Missing runtime '+src+' for '+tool.slug);
}
let placements=0;const paths=new Set();
for(const c of courses)for(const u of c.units)for(const a of u.artifacts){
 if(a.bankFormat!=='interactive-math')continue;
 placements++;paths.add(a.path);
 assert.equal(ctx.window.TeacherGameShare.supports(a.path),false,'Interactive tool must not open a game skill picker: '+a.path);
}
assert(paths.size>=46,'Existing or newly added tools disappeared');
assert.equal(ctx.window.TeacherGameShare.supports('artifacts/foundations-algebra-flashcards/index.html'),true,'Existing game skill selection must remain available');
console.log(`PASS ${manifest.tools.length} new tools, ${paths.size} total tools, ${placements} placements, student-share routing, and both new course outlines`);
// Collinear, separated edges must not count as crossing in the dilation challenge.
const dilation=fs.readFileSync(path.join(root,'tools/interactive-math-20261105/src/geometry-dilation-similarity-lab.js'),'utf8');
const geometry={};vm.createContext(geometry);
for(const name of ['cr','inTri','segX','apart']){const line=dilation.split('\n').find(s=>s.startsWith('function '+name+'('));assert(line,'Missing geometry helper '+name);vm.runInContext(line,geometry);}
assert.equal(geometry.segX([0,0],[1,0],[2,0],[3,0]),false);
assert.equal(geometry.segX([0,0],[2,0],[1,0],[3,0]),true);
assert.equal(geometry.segX([0,0],[1,1],[1,1],[2,0]),true);
assert.equal(geometry.segX([0,0],[2,2],[0,2],[2,0]),true);
assert.equal(geometry.apart([[0,0],[2,0],[0,2]],[[4,0],[6,0],[4,2]]),true);
assert.equal(geometry.apart([[0,0],[2,0],[0,2]],[[1,0],[3,0],[1,2]]),false);
console.log('PASS non-overlap detection for collinear edges, touching vertices, and crossing edges');
