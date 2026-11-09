#!/usr/bin/env python3
"""Maintain only Studio-owned symlinks; never replace unrelated skills."""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def manage(action,dest,with_anatomy=False):
    dest=Path(dest).expanduser().absolute(); manifest=json.loads((ROOT/'manifest.json').read_text())
    skills=[x['id'] for x in manifest['skills']]
    paths=[(dest/name,ROOT/'skills'/name) for name in skills]
    if with_anatomy:
        integration=next((x for x in manifest.get('integrations',[]) if x['id']=='anatomy'),None)
        if integration is None:raise ValueError('Bundled Anatomy integration is missing')
        source=(ROOT/integration['path']).resolve()
        if not source.is_relative_to(ROOT) or not (source/'SKILL.md').is_file():raise ValueError('Invalid Anatomy integration path')
        paths.append((dest/'anatomy',source))
    # Preflight the whole batch so a conflict cannot leave a partial installation.
    for target,source in paths:
        exists=os.path.lexists(target)
        ours=target.is_symlink() and target.resolve()==source.resolve()
        if action in ['install','update'] and exists and not ours:raise ValueError(f'Naming conflict: {target}; move it explicitly or choose --dest')
    if action in ['install','update']:dest.mkdir(parents=True,exist_ok=True)
    result=[]
    for target,source in paths:
        ours=target.is_symlink() and target.resolve()==source.resolve()
        if action in ['install','update'] and not ours:target.symlink_to(source,target_is_directory=True)
        if action=='uninstall' and ours:target.unlink()
        state='installed' if target.is_symlink() and target.resolve()==source.resolve() and (target/'SKILL.md').is_file() else 'absent or unrelated'
        result.append({'skill':source.name,'path':str(target),'state':state})
    print(json.dumps(result,indent=2))
    if action=='validate' and any(x['state']!='installed' for x in result):return 1
    return 0

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['install','update','validate','list','uninstall'],nargs='?',default='install')
    p.add_argument('--with-anatomy',action='store_true',help='Also manage the supplied Anatomy skill integration')
    g=p.add_mutually_exclusive_group();g.add_argument('--global',dest='global_',action='store_true');g.add_argument('--project',type=Path);g.add_argument('--dest',type=Path)
    a=p.parse_args()
    # Respect explicit Codex home, otherwise preserve an existing discovery convention.
    modern=Path.home()/'.agents/skills';legacy=Path.home()/'.codex/skills'
    global_dest=Path(os.environ['CODEX_HOME'])/'skills' if os.environ.get('CODEX_HOME') else modern if modern.exists() else legacy if legacy.exists() else modern
    dest=a.dest or (global_dest if a.global_ else (a.project or Path.cwd())/'.agents/skills')
    try:return manage(a.action,dest,a.with_anatomy)
    except (ValueError,OSError) as e:print(f'ERROR: {e}',file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
