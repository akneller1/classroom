#!/usr/bin/env node
'use strict';
/* Grade 5 production release audit: uses the exact site artifact that gets deployed,
 * not the source repository alone. This prevents missing/rewritten files from slipping
 * through otherwise successful development-bank tests. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const site=path.resolve(process.argv[2]||'_site'),root=path.join(site,'grade5');
const failures=[],warnings=[],counts={htmlFiles:0,links:0,units:0,resources:0,games:0,generators:0,studyGuides:0,interactive:0,projects:0,questions:0,diagrams:0,unreviewedNotes:0};
function fail(message){failures.push(message);}
function warn(message){warnings.push(message);}
function exists(p){return fs.existsSync(path.join(root,p));}
function read(p){return fs.readFileSync(path.join(root,p),'utf8');}
function allFiles(folder){
 if(!fs.existsSync(folder))return [];
 let found=[];
 for(const item of fs.readdirSync(folder,{withFileTypes:true})){
  const loc=path.join(folder,item.name);
  if(item.isDirectory())found.push(...allFiles(loc));
  else if(item.isFile())found.push(loc);
 }
 return found;
}
function localUrl(value,owner){
 if(/^(?:#|mailto:|tel:|data:|blob:)/i.test(value))return null;
 if(/^javascript:/i.test(value)){fail('Unsafe JavaScript link '+owner);return null;}
 const relative=path.relative(site,owner).split(path.sep).join('/');
 const base='https://mrksclassroom.com/'+relative;
 let url;
 try{url=new URL(value.replaceAll('&amp;','&'),base);}catch(e){fail('Unparseable link '+relative+': '+value);return null;}
 if(url.hostname!=='mrksclassroom.com'&&url.hostname!=='www.mrksclassroom.com')return null;
 const clean=decodeURIComponent(url.pathname);
 const target=path.resolve(site,'.'+clean);
 if(target!==site&&!target.startsWith(site+path.sep)){fail('Link escapes production site '+relative+': '+value);return null;}
 return {url,target,relative};
}
if(!exists('index.html')||!exists('manifest.json')){
 console.error('FAIL Grade 5 production output missing index.html or manifest.json');process.exit(1);
}
for(const file of allFiles(root).filter(f=>f.endsWith('.html'))){
 counts.htmlFiles++;
 const html=fs.readFileSync(file,'utf8'),owner=path.relative(site,file);
 for(const match of html.matchAll(/\b(?:href|src)\s*=\s*(["'])(.*?)\1/gi)){
  const value=match[2].trim();
  if(!value||value==='#')continue;
  counts.links++;
  const local=localUrl(value,file);
  if(!local)continue;
  if(!fs.existsSync(local.target)){
   fail('Broken local link '+owner+' → '+value+' ('+path.relative(site,local.target)+')');
  }else if(fs.statSync(local.target).isDirectory()&&!fs.existsSync(path.join(local.target,'index.html'))){
   fail('Link to folder without index.html '+owner+' → '+value);
  }
 }
}
for(const missing of ['index.html','grade5.html','data.js','course-catalog.js','grade5-resource-catalog.js',
 'worksheet-generator/grade5-games.html','worksheet-generator/grade5/g5-games.js',
 'worksheet-generator/grade5/g5-core.js','worksheet-generator/grade5-generators.html',
 'worksheet-generator/grade5-flashcards.html','worksheet-generator/grade5-understanding-check.html']){
 if(!exists(missing))fail('Required entry point missing '+missing);
}
if(exists('grade5.html')&&!read('grade5.html').includes('location.replace'))fail('Legacy Grade 5 game return path has no redirect');
if(exists('worksheet-generator/grade5/g5-core.js')&&!read('worksheet-generator/grade5/g5-core.js').includes("home.href = 'https://mrksclassroom.com/'")){
 fail('Game/flashcards/Understanding Check homepage link does not return to Classroom');
}
const context={};
context.window=context;
try{
 for(const file of ['data.js','course-catalog.js','grade5-resource-catalog.js']) vm.runInNewContext(read(file),context,{filename:file,timeout:6000});
}catch(e){fail('Course catalog failed to initialize: '+e.message);}
const course=context.MK_GRADE5_RESOURCES&&context.MK_GRADE5_RESOURCES.course;
if(!course||!Array.isArray(course.units)||course.units.length!==11){
 fail('Grade 5 published resource catalog is missing or has wrong number of units');
}else{
 counts.units=course.units.length;
 for(const unit of course.units){
  const list=unit.artifacts||[],types=Object.create(null),seen=new Set();
  for(const a of list){
   const type=a.type||'Unknown';types[type]=(types[type]||0)+1;
   counts.resources++;
   if(type==='Game')counts.games++;
   if(type==='Generator'||type==='Printable')counts.generators++;
   if(type==='Study Guide')counts.studyGuides++;
   if(type==='Interactive')counts.interactive++;
   if(type==='Project')counts.projects++;
   if(!a.path)fail(unit.id+': resource '+a.title+' is missing a URL');
   if(seen.has(a.path))fail(unit.id+': duplicate resource URL '+a.path);
   seen.add(a.path);
   for(const [name,target] of [['resource',a.path],['thumbnail',a.thumb]]){
    if(!target)continue;
    const norm=target.split(/[?#]/)[0];
    if(/^https?:\/\//.test(norm)){warn(unit.id+': externally hosted '+name+' '+norm);continue;}
    const resolved=path.resolve(root,norm);
    if(!resolved.startsWith(root+path.sep))fail(unit.id+': '+name+' escapes Grade 5 '+target);
    else if(!fs.existsSync(resolved))fail(unit.id+': missing '+name+' '+target);
   }
  }
  const games=list.filter(a=>a.type==='Game');
  if(games.length<9)fail(unit.id+': expected nine core games; found '+games.length);
  if((types.Generator||0)+(types.Printable||0)<4)fail(unit.id+': fewer than four generators or printable tools');
  for(const title of ['Flashcards','Understanding Check','Cheat Sheet']){
   if(!list.some(a=>a.title===title))fail(unit.id+': missing '+title);
  }
  if(!list.some(a=>a.type==='Project'))fail(unit.id+': no project');
  for(const a of games){
   const url=new URL(a.path,'https://example.test/grade5/');
   if(url.searchParams.get('unit')!==unit.id)fail(unit.id+': incorrect game unit link '+a.path);
   const key=url.searchParams.get('game');
   if(!key||!/^[-a-z0-9]+$/.test(key))fail(unit.id+': invalid game ID '+a.path);
   if(key&&!read('worksheet-generator/grade5/g5-games.js').includes("'"+key+"':"))fail(unit.id+': game has no registered engine '+key);
  }
 }
}
const manifest=JSON.parse(read('manifest.json')), banks=manifest.banks.filter(b=>b.courseId==='math5');
if(banks.length!==11)fail('Expected 11 approved Grade 5 question-bank entries; found '+banks.length);
const ids=new Set();
for(const entry of banks){
 if(entry.approved!==true)fail('Unit not approved: '+entry.unitId);
 if(!exists(entry.path)){fail('Bank missing '+entry.path);continue;}
 const bank=JSON.parse(read(entry.path));
 if(bank.unitId!==entry.unitId||bank.courseId!=='math5')fail('Bank identity mismatch '+entry.path);
 const expected=context.MK_COURSE_CATALOG&&context.MK_COURSE_CATALOG.getSkillRecords('math5',entry.unitId)||[];
 const perSkillLevel=new Map();
 for(const q of bank.questions||[]){
  counts.questions++;
  if(ids.has(q.id))fail('Duplicate question ID '+q.id);ids.add(q.id);
  const key=q.skillId+'/'+q.level;
  perSkillLevel.set(key,(perSkillLevel.get(key)||0)+1);
  if(!q.solutionSteps||!q.solutionSteps.length)fail('Missing worked solution '+q.id);
  if(!q.standards||!q.standards.length)fail('Missing standards '+q.id);
  if(/awaiting human review/i.test(q.sourceNotes||''))counts.unreviewedNotes++;
  if(q.diagram){
   counts.diagrams++;
   const src=q.diagram.spec&&q.diagram.spec.src;
   if(!src||!exists(src))fail('Missing question diagram '+q.id+' → '+src);
   if(!q.diagram.spec.alt)fail('Missing diagram alt text '+q.id);
  }
 }
 for(const skill of expected)for(const level of ['cp2','cp1','honors']){
  const n=perSkillLevel.get(skill.id+'/'+level)||0;
  if(n<30)fail('Insufficient questions for '+entry.unitId+'/'+skill.id+'/'+level+': '+n);
 }
}
for(const f of ['grade1.html','grade2.html','grade3.html','grade4.html']){
 if(exists(f))fail('Unfinished class accidentally published in Grade 5 folder: '+f);
}
if(counts.unreviewedNotes)warn(counts.unreviewedNotes+' question provenance notes still say "Awaiting human review"; independent math verification is not equivalent to editorial approval.');
console.log('Grade 5 production audit: '+JSON.stringify(counts));
for(const error of failures.slice(0,60))console.error('FAIL '+error);
if(failures.length>60)console.error('… '+(failures.length-60)+' more broken items');
for(const item of warnings.slice(0,20))console.warn('REVIEW '+item);
console.log('Grade 5 audit outcome: '+failures.length+' blocking defects; '+warnings.length+' editorial warnings');
if(failures.length)process.exitCode=1;
