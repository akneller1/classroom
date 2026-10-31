#!/usr/bin/env node
/* Curriculum structure and static resource integrity: no math content changes. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const ctx={window:{}};ctx.globalThis=ctx.window;
vm.runInNewContext(fs.readFileSync(path.join(root,'data.js'),'utf8'),ctx,{filename:'data.js'});
vm.runInNewContext(fs.readFileSync(path.join(root,'course-catalog.js'),'utf8'),ctx,{filename:'course-catalog.js'});
const library=ctx.window.LIBRARY, catalog=ctx.window.MK_COURSE_CATALOG;let errors=[],courses=0,units=0,skills=0,resources=0;
const unique=(items,label)=>{const seen=new Set();for(const x of items){if(seen.has(x))errors.push('Duplicate '+label+': '+x);seen.add(x)}};
unique(library.courses.map(c=>c.id),'course ID');
for(const course of library.courses){courses++;unique(course.units.map(u=>u.id),course.id+' unit ID');for(const unit of course.units){units++;
  const subskills=catalog.getSkills(course.id,unit.id);if(!subskills.length)errors.push('Missing skills for '+course.id+'/'+unit.id);
  unique(subskills.map(s=>s.toLowerCase().trim()),course.id+'/'+unit.id+' subskill');
  skills+=subskills.length;
  for(const a of unit.artifacts||[]){resources++;if(!a.title||!a.path)errors.push('Incomplete resource '+course.id+'/'+unit.id);if(!a.path)continue;
    if(/^(https?:|\/|\.\.)/i.test(a.path))continue;const file=a.path.split(/[?#]/)[0];if(!fs.existsSync(path.join(root,file)))errors.push('Missing file '+a.path+' in '+course.id+'/'+unit.id);
  }
}}
for(const cid of Object.keys(catalog.skills)){const c=library.courses.find(x=>x.id===cid);if(!c){errors.push('Unknown course in skills: '+cid);continue;}for(const uid of Object.keys(catalog.skills[cid]))if(!c.units.some(x=>x.id===uid))errors.push('Unknown unit in skills: '+cid+'/'+uid)}
console.log('Catalog: '+courses+' courses, '+units+' units, '+skills+' lessons, '+resources+' resource entries');
if(errors.length){console.error(errors.length+' catalog findings:');errors.slice(0,80).forEach(e=>console.error('- '+e));process.exitCode=1;}else console.log('PASS curriculum structure and resource paths');
