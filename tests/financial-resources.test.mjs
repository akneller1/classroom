import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {course} from '../financial/course.js';
import {resourceThumbnail,resourceHref} from '../financial/lib/resource-previews.mjs';
const root=new URL('../',import.meta.url);
const manifest=JSON.parse(readFileSync(new URL('financial/resources.json',root),'utf8'));
const allGames=['showdown','connect-four','tic-tac-toe','picture-reveal','detective'];
function exists(path){
 const resource=new URL(path,'https://classroom.example/');
 return existsSync(new URL(resource.pathname.slice(1),root));
}
function resources(unit){
 const r=unit.resources;
 return [
  ['Lesson Plan',r.lessonPlan],['Worksheet',r.worksheet],['Assessment',r.assessment],
  ['Practice Test',r.practiceTest],['Flashcards',r.flashcards],['Cheat Sheet',r.cheatSheet],
  ['Decision Lab',r.decisionLab.path],['Decision Lab teacher guide',r.decisionLab.teacherPath],
  ...r.games.map(g=>[g.title,g.path]),
  ...r.projects.map(p=>[p.title,p.path])
 ];
}
test('published Financial Algebra units match the resource manifest',()=>{
 assert.equal(course.units.length,10);
 assert.deepEqual(manifest.units.map(u=>u.unitId),course.units.map(u=>u.id));
 for(const unit of manifest.units){
  assert.ok(unit.resources);
  assert.deepEqual(unit.resources.games.map(g=>g.id),allGames);
  assert.ok(unit.resources.projects.length>=1);
 }
});
test('every Financial Algebra card target and thumbnail exists locally',()=>{
 for(const unit of manifest.units){
  for(const [title,path] of resources(unit)){
   assert.ok(typeof path==='string'&&path.length,unit.unitId+': '+title+' missing target');
   assert.ok(exists(resourceHref(path)),unit.unitId+': '+title+' broken link: '+path);
   const preview=resourceThumbnail(path,unit.unitId);
   assert.ok(exists(preview),unit.unitId+': '+title+' missing preview: '+preview);
  }
  for(const key of ['classroomBank','extendedBank']){
   assert.ok(exists(unit.resources[key]),unit.unitId+': missing '+key);
  }
 }
});
test('all Financial Algebra cards use the current card structure and shareable game links',()=>{
 const source=readFileSync(new URL('financial/classroom-site.mjs',root),'utf8');
 assert.match(source,/finance-resource-item/);
 assert.match(source,/finance-resource-image-link/);
 assert.match(source,/finance-student-link/);
 assert.match(source,/data-student-link/);
 assert.match(source,/resourceHref\(path\)/);
});
