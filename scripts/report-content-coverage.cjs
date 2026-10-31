#!/usr/bin/env node
/* Live curriculum/resource coverage report for planning Claude work. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..');const ctx={window:{}};
for(const f of ['data.js','course-catalog.js'])vm.runInNewContext(fs.readFileSync(path.join(root,f),'utf8'),ctx,{filename:f});
const library=ctx.window.LIBRARY,catalog=ctx.window.MK_COURSE_CATALOG;
console.log('# Course content coverage report\n');
console.log('| Course | Units | Lessons | Resource links | Units without resources |');
console.log('|---|---:|---:|---:|---:|');
for(const c of library.courses){let count=0,empty=0,lessons=0;for(const u of c.units){count+=(u.artifacts||[]).length;if(!(u.artifacts||[]).length)empty++;lessons+=catalog.getSkills(c.id,u.id).length}
 console.log('| '+c.name+' | '+c.units.length+' | '+lessons+' | '+count+' | '+empty+' |');}
console.log('\n## Units requiring content work\n');
for(const c of library.courses){let gaps=c.units.filter(u=>!(u.artifacts||[]).length);if(!gaps.length)continue;
 console.log('### '+c.name+'\n');for(const u of gaps){let skills=catalog.getSkillRecords(c.id,u.id);console.log('- **'+u.name+'** ('+skills.length+' lessons): '+skills.map(s=>s.id).join(', '));}
 console.log('');}
console.log('Note: Resource links indicate registered entries, not confirmed mathematical or functional completeness.');
