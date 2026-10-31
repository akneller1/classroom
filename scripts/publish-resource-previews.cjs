/* Publish only actual browser screenshots, never generated mathematical artwork. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const ctx={window:{}};vm.runInNewContext(fs.readFileSync('data.js','utf8'),ctx);
const games=['flashcards','connect-four','tic-tac-toe','picture-reveal','showdown','detective','escape-room'],mapping={};
for(const c of ctx.window.LIBRARY.courses)for(const u of c.units)for(const g of games){const p='thumbs/previews/'+c.id+'/'+u.id+'-'+g+'.png';if(fs.existsSync(p))mapping[c.id+'/'+u.id+'/'+g]=p;}
const expected=ctx.window.LIBRARY.courses.reduce((n,c)=>n+c.units.length*games.length,0);if(Object.keys(mapping).length!==expected)throw Error('Every course/unit/activity needs its actual browser preview before publishing: '+Object.keys(mapping).length+'/'+expected);
fs.writeFileSync('thumbs/resource-previews.js','window.MK_RESOURCE_PREVIEWS = '+JSON.stringify(mapping,null,2)+';\n');
const p='index.html';fs.writeFileSync(p,fs.readFileSync(p,'utf8').replace(/resource-previews\.js\?v=[^"\s]+/,'resource-previews.js?v=previews-'+(process.env.GITHUB_SHA||'class-parity')));
console.log('Prepared '+Object.keys(mapping).length+' real course/activity previews');
