import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { ISO_CSS } from '../kit/iso-kit.mjs';

const args=process.argv.slice(2),source=args[0];
const option=(name,fallback)=>{const i=args.indexOf(name);return i<0?fallback:args[i+1];};
if(!source||args.includes('--help')){
 console.log('Static SVG inspection only: node scripts/render-static.mjs page.html --out shots/light.png --theme light --width 1440 [--svg-out resolved.svg]');
 process.exit(source?0:1);
}
const input=fs.readFileSync(source,'utf8');
const theme=option('--theme',/data-theme="light"/.test(input)?'light':'dark');
if(!['light','dark'].includes(theme))throw new Error('Choose light or dark.');
const block=(selector)=>ISO_CSS.match(new RegExp(selector+'\\s*\\{([^}]+)\\}'))?.[1]||'';
const tokens={};
for(const text of [block('\\.iso'),...(theme==='light'?[block('\\.iso\\[data-theme="light"\\]')]:[])]){
 for(const m of text.matchAll(/(--anatomy-[\w-]+)\s*:\s*([^;]+);?/g))tokens[m[1]]=m[2].trim();
}
const resolve=text=>text.replace(/var\((--anatomy-[\w-]+)(?:,\s*([^)]*))?\)/g,(_,name,fallback)=>{
 if(tokens[name]!==undefined)return tokens[name];if(fallback)return fallback;throw new Error('Unresolved kit token: '+name);
});
const match=input.match(/<svg\b[\s\S]*?<\/svg>/i);
if(!match)throw new Error('No SVG found. A static export requires SVG markup in the built file.');
let svg=match[0];
const beforeScripts=input.includes('<script')?input.slice(0,input.indexOf('<script')):input;
const localStyles=[...beforeScripts.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map(m=>m[1]).join('\n');
if(!/\bxmlns=/.test(svg.slice(0,svg.indexOf('>'))))svg=svg.replace('<svg','<svg xmlns="http://www.w3.org/2000/svg"');
svg=svg.replace(/\s(data-[\w-]+|hidden)(?=[\s>])/g,' $1=""');
svg=resolve(svg.replace(/(<svg\b[^>]*>)/,`$1<style>${resolve(ISO_CSS+'\n'+localStyles)}\n[hidden]{display:none}</style>`));
const svgOut=option('--svg-out',null);
if(svgOut){fs.mkdirSync(path.dirname(svgOut),{recursive:true});fs.writeFileSync(svgOut,svg);}
const require=createRequire(import.meta.url);
let sharp;
try{sharp=require('sharp');}catch{
 const modules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
 if(!modules)throw new Error('Static rendering needs sharp. No browser checks were performed.');
 sharp=require(path.join(modules,'sharp'));
}
const out=option('--out','static.png'),width=Number(option('--width','1440'));
if(!Number.isFinite(width)||width<1)throw new Error('Width must be positive.');
fs.mkdirSync(path.dirname(out),{recursive:true});
await sharp(Buffer.from(svg),{density:192}).resize({width}).flatten({background:tokens['--anatomy-card']}).png().toFile(out);
console.log(JSON.stringify({output:path.resolve(out),theme,width,verification:'static SVG art only; browser layout, native input, JavaScript and WebGL were not verified'}));
