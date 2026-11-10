const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');

const {spawnSync}=require('node:child_process');
const here=__dirname;
const candidates=[process.env.STUDIO_TOOLKIT_SKILL, path.resolve(here,"../../../../../.."), path.join(process.env.CODEX_HOME || path.join(os.homedir(),'.codex'),'skills/studio-toolkit'),path.join(os.homedir(),'.agents/skills/studio-toolkit')].filter(Boolean);
const skill=candidates.find(p=>fs.existsSync(path.join(p,'scripts/animation.py')));
if(!skill) throw new Error('Set STUDIO_TOOLKIT_SKILL to the installed or extracted studio-toolkit skill directory');
const [mode,a,b,...rest]=process.argv.slice(2);
if(rest.some(x=>Number(x)!==0)) throw new Error('Use the shared renderer for clip duration; arbitrary segment rendering is not provided by this adapter');
const args=[path.join(skill,'scripts/animation.py'),'render',process.cwd()];
if(mode==='stills') args.push('--snap',a,'--out',b||'stills');
else if(mode==='video') args.push('--out',a||'silent.mp4');
else throw new Error('Use stills TIMES [FOLDER] or video OUTPUT');
const result=spawnSync(process.env.PYTHON || 'python3',args,{stdio:'inherit'}); process.exit(result.status??1);
