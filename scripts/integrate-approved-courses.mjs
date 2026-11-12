// Assemble the approved Grade 5 source into the public Classroom artifact.
// Source files stay in FinancialAlgebra; only the assembled _site/site directory changes.
// This is the ONLY Grade 5 assembler used by either public workflow.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const stage=path.resolve(process.env.GRADE5_SOURCE_DIR||'../FinancialAlgebra');
const out=path.resolve(process.env.GRADE5_OUTPUT_DIR||'_site');
const dst=path.join(out,'grade5');
function required(file){if(!fs.existsSync(file))throw Error('Missing approved Grade 5 source '+file);return file;}
if(!fs.existsSync(path.join(out,'index.html')))throw Error('Build main Classroom site before integrating Grade 5');
required(path.join(stage,'grade5.html'));
fs.rmSync(dst,{recursive:true,force:true});
fs.mkdirSync(dst,{recursive:true});
const copied=new Set();
function copyFile(rel){
 if(copied.has(rel))return;
 const from=required(path.join(stage,rel)),to=path.join(dst,rel);
 if(!from.startsWith(stage+path.sep)||!to.startsWith(dst+path.sep))throw Error('Grade 5 copy escapes approved folders: '+rel);
 fs.mkdirSync(path.dirname(to),{recursive:true});
 fs.copyFileSync(from,to);
 copied.add(rel);
}
function copyDir(rel){
 const source=required(path.join(stage,rel)),target=path.join(dst,rel);
 fs.mkdirSync(target,{recursive:true});
 for(const item of fs.readdirSync(source,{withFileTypes:true})){
  if(item.name==='.git'||item.name==='node_modules'||item.name==='__pycache__'||item.name==='.DS_Store')continue;
  const sub=path.posix.join(rel,item.name);
  if(item.isDirectory())copyDir(sub);
  else if(item.isFile()&&!/\.(?:md|py|pyc|zip)$/i.test(item.name))copyFile(sub);
 }
}
// Only the released Grade 5 page, data, tools and runtime are permitted here.
for(const f of ['grade5.html','grade5-resources.html','data.js','course-catalog.js',
 'grade5-resource-catalog.js','question-bank-adapter.js','question-bank-loader.js',
 'manifest.json','styles.css','site-overrides.css','assets/favicon.svg',
 'assets/course-icons/grade5.svg','course-outlines/grade5.json',
 'worksheet-generator/core/math-display.js','worksheet-generator/core/math-display.css',
 'worksheet-generator/games/skill-setup.js'])copyFile(f);
for(const f of fs.readdirSync(path.join(stage,'src')).filter(x=>/^grade5-.*\.js$/.test(x)))copyFile('src/'+f);
for(const f of fs.readdirSync(path.join(stage,'worksheet-generator')).filter(x=>/^grade5-.*\.html$/.test(x)))copyFile('worksheet-generator/'+f);
copyDir('worksheet-generator/grade5');
copyDir('math5');
if(fs.existsSync(path.join(stage,'assets/fonts')))copyDir('assets/fonts');
// Read the source data/catalog and keep the released math5 course only.
const context={window:{}};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(stage,'data.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(stage,'course-catalog.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(stage,'grade5-resource-catalog.js'),'utf8'),context);
const library=context.window.LIBRARY,course=library?.courses.find(c=>c.id==='math5');
const resources=context.window.MK_GRADE5_RESOURCES?.course;
if(!course||!resources||course.units.length!==11||resources.units.length!==11)throw Error('Expected eleven approved Grade 5 units');
library.courses=[course];
fs.writeFileSync(path.join(dst,'data.js'),'window.LIBRARY = '+JSON.stringify(library)+';\n');
// Only package activities actually linked by the approved Grade 5 resource catalog.
for(const unit of resources.units){
 for(const item of unit.artifacts){
  if(item.thumb&&item.thumb.startsWith('thumbs/math5-'))copyFile(item.thumb);
  if(/^math5-[a-z0-9-]+\//.test(item.path||'')){
   const dir=item.path.split('/')[0];
   if(!fs.existsSync(path.join(dst,dir)))copyDir(dir);
  }
 }
}
// Publish only approved Grade 5 manifest entries (no unpublished staging courses).
const manifest=JSON.parse(fs.readFileSync(path.join(stage,'manifest.json'),'utf8'));
const banks=manifest.banks.filter(b=>b.courseId==='math5'&&b.approved===true);
if(banks.length!==11)throw Error('Expected eleven approved Grade 5 bank entries');
fs.writeFileSync(path.join(dst,'manifest.json'),JSON.stringify({version:1,banks},null,2)+'\n');
// All diagrams are loaded from their exact path relative to Grade 5's root.
// In particular, 500+ volume/fraction diagrams have flat .png filenames.
let diagrams=0;
for(const entry of banks){
 const bank=JSON.parse(fs.readFileSync(required(path.join(stage,entry.path)),'utf8'));
 for(const question of bank.questions){
  const src=question.diagram?.spec?.src;
  if(!src)continue;
  if(!/^[a-z0-9/_-]+\.png$/i.test(src)||src.startsWith('/')||src.includes('..'))throw Error('Unsafe Grade 5 diagram path '+src);
  copyFile(src);
  diagrams++;
 }
}

// Derive the public homepage catalog and standards metadata from the approved
// Grade 5 source at assembly time. This is the sole production catalog:
 // the local Classroom snapshot is a fallback for unassembled previews only.
const standardsByUnit=Object.create(null);
for(const entry of banks){
  const bank=JSON.parse(fs.readFileSync(path.join(stage,entry.path),'utf8'));
  const codes=Object.create(null);
  for(const question of bank.questions){
    if(!Array.isArray(question.standards)||!question.standards.length)throw Error('Untagged Grade 5 question '+question.id);
    if(!codes[question.skillId])codes[question.skillId]=new Set();
    for(const code of question.standards)codes[question.skillId].add(code);
  }
  standardsByUnit[entry.unitId]=codes;
}
const classroomResources=resources.units.map(function(unit){
  const mapped=unit.artifacts.map(function(item){
    const parsed=new URL(item.path,'https://mrksclassroom.com/grade5/');
    if(parsed.origin!=='https://mrksclassroom.com'||!parsed.pathname.startsWith('/grade5/'))throw Error('Non-local Grade 5 resource '+item.path);
    const mode=parsed.searchParams.get('mode');
    const game=parsed.searchParams.get('game');
    const format=game?(game==='picture-reveal'?'picture-reveal':game==='connect-four'?'connect-four':'topic-games'):
      mode?({lesson:'lesson-planner',worksheet:'worksheet-generator',assessment:'assessment-generator',activity:'printable-generator'}[mode]):
      item.type==='Interactive'?'interactive-math':item.type==='Project'?'other':
      /flashcards/.test(item.path)?'flashcards':/understanding-check/.test(item.path)?'interactive-practice-test':
      /cheat-sheet/.test(item.path)?'cheat-sheets':'other';
    const result={title:item.title,path:'/grade5/'+item.path,type:item.type==='Printable'?'Generator':item.type,
      bankFormat:format,thumb:item.thumb?'/grade5/'+item.thumb:'',description:item.description||item.title};
    if(item.title==='Error Analysis'||item.title==='Activity Generator')result.visibleInBrowse=true;
    return result;
  });
  // During the cross-repository rollout, preserve access even if the staging
  // source is updated after this build starts.
  if(!mapped.some(function(a){return a.title==='Error Analysis';})){
    mapped.push({title:'Error Analysis',path:'/grade5/worksheet-generator/grade5-generators.html?unit='+encodeURIComponent(unit.id)+'&mode=activity&kind=error',
      type:'Generator',bankFormat:'printable-generator',thumb:'/grade5/thumbs/math5-generator-activity.svg',
      description:'Find, explain and correct Grade 5 math mistakes.',visibleInBrowse:true});
  }
  return {id:unit.id,name:unit.name,artifacts:mapped};
});
const classroomSkills=Object.create(null),classroomStandards=Object.create(null);
for(const unit of resources.units){
  const records=context.window.MK_COURSE_CATALOG.getSkillRecords('math5',unit.id);
  const byId=standardsByUnit[unit.id]||{};
  classroomSkills[unit.id]=records.map(function(r){return {id:r.id,name:r.name};});
  classroomStandards[unit.id]=Object.create(null);
  for(const r of records){
    const codes=byId[r.id]?Array.from(byId[r.id]).sort():[];
    if(!codes.length)throw Error('Missing CCSS standards for '+unit.id+' / '+r.name);
    classroomStandards[unit.id][r.name]=codes;
  }
}
const classroomBridge={units:classroomResources,skills:classroomSkills,standards:classroomStandards};
const bridge='/* Generated by integrate-approved-courses.mjs from the approved source; do not edit. */\n'+
 '(function(root){"use strict";var data='+JSON.stringify(classroomBridge)+';'+
 'var library=root.LIBRARY;if(!library||!Array.isArray(library.courses))return;'+
 'var grade=library.courses.find(function(c){return c.id==="grade5";});'+
 'if(!grade){grade={id:"grade5",name:"5th Grade Math",color:"green",art:"fifth",blurb:"Place value, fractions, decimals, measurement, geometry and data."};library.courses.push(grade);}'+
 'grade.units=data.units;root.MK_GRADE5_STANDARDS=data.standards;'+
 'var catalog=root.MK_COURSE_CATALOG;if(catalog){'+
 'var oldGet=catalog.getSkills,oldRecords=catalog.getSkillRecords;'+
 'catalog.getSkills=function(id,unit){return id==="grade5"&&data.skills[unit]?data.skills[unit].map(function(r){return r.name;}):oldGet(id,unit);};'+
 'catalog.getSkillRecords=function(id,unit){return id==="grade5"&&data.skills[unit]?data.skills[unit].map(function(r,i){return {id:r.id,name:r.name,index:i+1};}):oldRecords(id,unit);};'+
 '}root.MK_GRADE5_RELEASE={units:data.units.length,resources:data.units.reduce(function(n,u){return n+u.artifacts.length;},0)};'+
 '})(typeof window!=="undefined"?window:globalThis);\n';
fs.writeFileSync(path.join(dst,'grade5-main-catalog.js'),bridge);

// All public course browsing uses the main Classroom shell. The packaged
// /grade5/ folder remains the home for games, banks, diagrams and projects.
const html='<!doctype html><html lang="en"><head><meta charset="utf-8">'+
 '<meta name="viewport" content="width=device-width,initial-scale=1">'+
 '<meta name="robots" content="noindex,follow">'+
 '<title>5th Grade Math | Mr. K\\'s Classroom</title>'+
 '<link rel="canonical" href="https://mrksclassroom.com/courses/grade5.html">'+
 '<meta http-equiv="refresh" content="0;url=../#grade5">'+
 '<script>(function(){var hit=/^(?:math5|grade5)\\.([a-z0-9-]+)$/.exec(location.hash.slice(1));'+
 'location.replace("../#grade5"+(hit?"."+hit[1]:""));})();<\\/script>'+
 '</head><body><p>Open <a href="../#grade5">5th Grade Math on Mr. K\\'s Classroom</a>.</p></body></html>\\n';
fs.writeFileSync(path.join(dst,'index.html'),html);
const alias='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex,follow">'+
 "<title>Grade 5 | Mr. K's Classroom</title>"+
 '<meta http-equiv="refresh" content="0;url=./index.html">'+
 "<script>location.replace('./index.html'+location.search+location.hash);</script>"+
 '</head><body><a href="./index.html">5th Grade Math</a></body></html>\n';
fs.writeFileSync(path.join(dst,'grade5.html'),alias);
const siteJs=path.join(dst,'src','grade5-site.js');
if(fs.existsSync(siteJs)){
 const js=fs.readFileSync(siteJs,'utf8').replace(/\['Home','index\.html'\]/g,"['Home','../index.html']");
 fs.writeFileSync(siteJs,js);
}
const sitemap=path.join(out,'sitemap.xml');
if(fs.existsSync(sitemap)){
 let xml=fs.readFileSync(sitemap,'utf8');
 if(!xml.includes('https://mrksclassroom.com/courses/grade5.html'))xml=xml.replace('</urlset>','  <url><loc>https://mrksclassroom.com/courses/grade5.html</loc></url>\n</urlset>');
 fs.writeFileSync(sitemap,xml);
}
console.log('Grade 5 assembled: 11 approved units, '+diagrams+' question diagrams, '+copied.size+' released source files; no other staging pages.');
