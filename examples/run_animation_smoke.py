#!/usr/bin/env python3
"""Reproduce six short, silent animation checks without any API or model."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/studio-toolkit/scripts'
sys.path.insert(0,str(SCRIPTS))
import animation

def run(output, stills_only=False, kinds=None):
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    choices={'animated-graph':'graph','minimalistic-graphics':'minimal','map-route':'map','exploded-view':'exploded'}
    kinds=kinds or list(choices)+list(animation.ENGINES)
    records=[]
    for kind in kinds:
        if kind in choices:
            spec=output/(kind+'.json')
            if not spec.exists(): shutil.copy2(ROOT/'examples/animation-specs'/(choices[kind]+'.json'),spec)
            command=[sys.executable,str(SCRIPTS/'animation.py'),'build',kind,str(spec)]
            if stills_only: command+=['--snap','0.5,2.5,3.5']
            subprocess.run(command,check=True)
            records.append({'kind':kind,'spec':str(spec),'video':str(spec.with_suffix('.mp4')) if not stills_only else None})
        else:
            project=output/kind
            if not project.exists(): animation.init(kind,project)
            command=[sys.executable,str(SCRIPTS/'animation.py'),'render',str(project),'--out',str(output/(kind+'-stills' if stills_only else kind+'.mp4'))]
            if stills_only: command+=['--snap','0.5,2.5,3.5']
            subprocess.run(command,check=True)
            records.append({'kind':kind,'project':str(project),'video':str(output/(kind+'.mp4')) if not stills_only else None})
    (output/'animation-smoke.json').write_text(json.dumps({'api_requests':0,'narration':'none; silent calibration','results':records},indent=2)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);p.add_argument('--stills-only',action='store_true');p.add_argument('--kinds',nargs='+',choices=list(animation.QUICK)+list(animation.ENGINES));a=p.parse_args();run(a.output,a.stills_only,a.kinds)
