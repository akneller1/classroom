import fs from 'node:fs';
const p='_site/index.html';let s=fs.readFileSync(p,'utf8');
s=s.replace(/<script src="postit-games\.js[^"\n]*"><\/script>\s*/g,'');
const anchor='<script src="app.js';
if(!s.includes(anchor))throw Error('Post-it games: missing app script');
s=s.replace(anchor,'<script src="postit-games.js?v=20261114"></script>\n'+anchor);
fs.writeFileSync(p,s);
console.log('Post-it games placed after released course catalogs.');
