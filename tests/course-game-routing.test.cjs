'use strict';
/* Regression: legacy site links must open the course-specific game player. */
const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'worksheet-generator/course-game.html'),'utf8');
const routeScript=html.match(/<script>\s*\/\* Shared compatibility router[\s\S]*?<\/script>/)?.[0]
  .replace(/^<script>/,'').replace(/<\/script>$/,'');
assert.ok(routeScript,'legacy game compatibility router exists');
const manifests=JSON.parse(fs.readFileSync(path.join(root,'financial/resources.json'),'utf8'));
const financeUnits=manifests.units.map(u=>u.unitId);
const games=['showdown','connect-four','tic-tac-toe','picture-reveal','detective'];
const gradeUnits=['place-value-number-sense','multi-digit-multiplication-division','decimal-operations','numerical-expressions-patterns','fraction-addition-subtraction','fraction-multiplication-division','measurement-conversions','volume-three-dimensional-figures','coordinate-plane-graphing','classifying-two-dimensional-figures','data-line-plots-problem-solving'];
const gradeGames=['math-quest','treasure-trail','space-explorer','math-builders','picture-reveal','math-race','math-soccer','connect-four','puzzle-masters'];
function route(course,unit,game,extras=''){
 const href='https://mrksclassroom.com/worksheet-generator/course-game.html?course='+course+'&unit='+unit+'&game='+game+extras;
 const location={href,search:new URL(href).search,replace(next){this.target=next;}};
 const window={};
 const context={URL,URLSearchParams,location,window};
 vm.runInNewContext(routeScript,context,{timeout:1000});
 return {target:location.target,redirecting:window.MK_GAME_REDIRECTING,invalid:window.MK_INVALID_INTEGRATED_GAME};
}
test('every Financial Algebra game uses its dedicated bank-backed player',()=>{
 assert.equal(financeUnits.length,10);
 for(const unit of manifests.units){
  assert.deepEqual(unit.resources.games.map(g=>g.id),games);
  for(const game of games){
   const entry=unit.resources.games.find(g=>g.id===game);
   assert.equal(entry.path,'financial/games/index.html?unit='+unit.unitId+'&game='+game);
   const result=route('financial-algebra',unit.unitId,game);
   const target=new URL(result.target);
   assert.equal(target.pathname,'/financial/games/index.html');
   assert.equal(target.searchParams.get('unit'),unit.unitId);
   assert.equal(target.searchParams.get('game'),game);
   assert.equal(result.redirecting,true);
  }
 }
});
test('Grade 5 legacy links open the Grade 5 player on this site',()=>{
 for(const unit of gradeUnits)for(const game of gradeGames){
  const result=route('grade5',unit,game);
  const target=new URL(result.target);
  assert.equal(target.pathname,'/grade5/worksheet-generator/grade5-games.html');
  assert.equal(target.origin,'https://mrksclassroom.com');
  assert.equal(target.searchParams.get('unit'),unit);
  assert.equal(target.searchParams.get('game'),game);
 }
 for(const unit of ['fraction-addition-subtraction','fraction-multiplication-division']){
  assert.ok(route('grade5',unit,'fraction-frenzy').target);
 }
 assert.equal(route('grade5','banking','tic-tac-toe').invalid,true);
 assert.equal(route('grade5','income','fraction-frenzy').invalid,true);
});
test('student flag and skills survive redirects',()=>{
 const result=route('financial-algebra','banking','tic-tac-toe','&student=1&skills=banking-skill-01');
 const target=new URL(result.target);
 assert.equal(target.searchParams.get('student'),'1');
 assert.equal(target.searchParams.get('skills'),'banking-skill-01');
});
test('legacy core courses are unaffected',()=>{
 for(const course of ['algebra','geometry','algebra2','prealgebra','statistics','discrete']){
  const result=route(course,'example-unit','tic-tac-toe');
  assert.equal(result.target,undefined);
  assert.equal(result.invalid,undefined);
 }
});
test('invalid explicit unit cannot silently fall back to first unit',()=>{
 const source=fs.readFileSync(path.join(root,'worksheet-generator/games/course-source.js'),'utf8');
 assert.match(source,/!requestedUnit\?course\?\.units\[0\]:null/);
});
test('old integrated flashcard bookmarks stay usable',()=>{
 for(const [course,units] of [['grade5',gradeUnits],['financial-algebra',financeUnits]])for(const unit of units){
  const target=new URL(route(course,unit,'flashcards','&student=1&skills=a').target);
  assert.equal(target.pathname,course==='grade5'?'/grade5/worksheet-generator/grade5-flashcards.html':'/financial/flashcards/index.html');
  assert.equal(target.searchParams.get('unit'),unit);assert.equal(target.searchParams.get('student'),'1');assert.equal(target.searchParams.get('skills'),'a');
 }
});
test('resource standards preserve native flashcards, finance games and projects',()=>{
 const project={type:'Project',title:'Sports Stats Showdown',path:'/grade5/math5-project-sports-stats-showdown/index.html'};
 const cards={title:'Flashcards',path:'/grade5/worksheet-generator/grade5-flashcards.html?unit=place-value-number-sense'};
 const finance={title:'Flashcards',path:'financial/flashcards/index.html?unit=income'};
 const game={title:'Showdown',path:'financial/games/index.html?unit=income&game=showdown'};
 const window={LIBRARY:{courses:[{id:'grade5',units:[{id:gradeUnits[0],name:'Place Value',artifacts:[project,cards]}]},{id:'financial-algebra',units:[{id:'income',name:'Income',artifacts:[finance,game]}]}]}};
 vm.runInNewContext(fs.readFileSync(path.join(root,'resource-standards.js'),'utf8'),{window});
 assert.equal(window.MK_RESOURCE_STANDARDS.kind(project),null);
 assert.equal(window.MK_RESOURCE_STANDARDS.kind({path:'artifacts/math5-project-mystery/index.html'}),null);
 assert.equal(window.LIBRARY.courses[0].units[0].artifacts[0].title,project.title);
 for(const c of window.LIBRARY.courses)for(const a of c.units[0].artifacts)assert(!a.path.includes('course-game.html'));
});
test('browsing never labels project paths as team games',()=>{
 const source=fs.readFileSync(path.join(root,'app.js'),'utf8');
 const fn=source.slice(source.indexOf('  function activityFormat(a) {'),source.indexOf('  /* Teaching mode metadata'));
 const classify=vm.runInNewContext(fn+';activityFormat',{toArr:x=>Array.isArray(x)?x:[x]});
 assert.equal(classify({type:'Project',path:'/grade5/math5-project-sports-stats-showdown/index.html'}),'other');
 assert.equal(classify({path:'artifacts/some-project-escape-room/index.html'}),'other');
 assert.equal(classify({type:'Game',path:'artifacts/algebra-showdown/index.html'}),'showdown');
});
