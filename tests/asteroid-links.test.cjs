const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const app=fs.readFileSync('app.js','utf8');
const route=app.match(/function activityUrl\(a\) \{[^\n]+/)[0];
const oldRoute=fs.readFileSync('activity.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
const units={grade2:['place-value-1000','count-compare-1000'],grade3:['properties-fact-strategies','equivalent-comparing-fractions'],grade4:['factors-multiples-patterns','fractions-equivalent-fractions'],grade5:['place-value-number-sense','multi-digit-multiplication-division','decimal-operations']};
test('all nine elementary Asteroid cards open the game directly',()=>{
 const c={};vm.createContext(c);vm.runInContext(route,c);
 for(const [course,list] of Object.entries(units))for(const unit of list){const path=`worksheet-generator/asteroid-blaster.html?course=${course}&unit=${unit}`;assert.equal(c.activityUrl({path}),path);}
});
test('cached viewer links redirect with unit and student skill choices preserved',()=>{
 for(const [course,list] of Object.entries(units))for(const unit of list){
  const game=`worksheet-generator/asteroid-blaster.html?course=${course}&unit=${unit}`;
  const location={href:'https://mrksclassroom.com/activity.html?path='+encodeURIComponent(game)+'&student=1&skills=s1%2Cs2&level=cp1&share=1',replace(url){this.target=url;}};location.search=new URL(location.href).search;
  vm.runInNewContext(oldRoute,{URL,URLSearchParams,location});
  const url=new URL(location.target);assert.equal(url.pathname,'/worksheet-generator/asteroid-blaster.html');assert.equal(url.searchParams.get('course'),course);assert.equal(url.searchParams.get('unit'),unit);assert.equal(url.searchParams.get('skills'),'s1,s2');assert.equal(url.searchParams.get('student'),'1');assert.equal(url.searchParams.get('level'),'cp1');assert.equal(url.searchParams.get('share'),'1');
 }
});
test('student-link card recognizes the Asteroid route',()=>{
 const match=app.match(/\((\/asteroid-blaster[^\n]+?)\.test\(a\.path/);assert(match);const regex=vm.runInNewContext(match[1]);assert(regex.test('worksheet-generator/asteroid-blaster.html?course=grade2&unit=place-value-1000'));
});
