#!/usr/bin/env python3
"""Build a portable single-skill ZIP/.skill with all runtime references and utilities."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import argparse
import json
import re
import sys
ROOT=Path(__file__).resolve().parents[1]

def package(destination):
    destination=Path(destination);destination.parent.mkdir(parents=True,exist_ok=True)
    items={}
    for f in (ROOT/'skills/studio-toolkit').rglob('*'):
        if f.is_file() and '__pycache__' not in f.parts:items[str(f.relative_to(ROOT/'skills/studio-toolkit'))]=f.read_bytes()
    # UI metadata is host-specific; the portable bundle works from SKILL.md itself.
    for skill in json.loads((ROOT/'manifest.json').read_text())['skills']:
        name=skill['id']
        if name=='studio-toolkit':continue
        source=ROOT/'skills'/name
        text=(source/'SKILL.md').read_text()
        text=text.split('---',2)[2].strip()+'\n'
        text=text.replace('../studio-toolkit/references/','../')
        text=re.sub(r'\]\((references|scripts|assets)/',lambda m:f']({name}/{m[1]}/',text)
        items[f'references/specialists/{name}.md']=text.encode()
        for f in source.rglob('*'):
            if f.is_file() and f.name!='SKILL.md' and '__pycache__' not in f.parts:
                items[f'references/specialists/{name}/{f.relative_to(source)}']=f.read_bytes()
    for f in (ROOT/'third_party/licenses').iterdir():items[f'references/licenses/{f.name}']=f.read_bytes()
    items['LICENSE']=(ROOT/'LICENSE').read_bytes()
    for name in ['requirements.txt','requirements-youtube.txt','requirements-transcription.txt']:
        items[name]=(ROOT/name).read_bytes()
    items['scripts/transcribe.py']=(ROOT/'scripts/transcribe.py').read_bytes()
    items['references/upstreams.lock.json']=(ROOT/'upstreams.lock.json').read_bytes()
    items['references/distribution.md']=b'# Distribution\n\nThis is a single skill with specialist references and executable local helpers. Import only in a ChatGPT host that supports skill uploads. No automatic ChatGPT installation is performed. Rendering needs a filesystem, Python dependencies, Node/Remotion where selected, a browser and FFmpeg. Ordinary chat can apply writing workflows; it cannot claim a local render.\n'
    with ZipFile(destination,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for name,content in sorted(items.items()):
            info=ZipInfo('studio-toolkit/'+name,date_time=(1980,1,1,0,0,0))
            info.create_system=3
            info.external_attr=0o100644<<16
            z.writestr(info,content,compress_type=ZIP_DEFLATED,compresslevel=9)
    with ZipFile(destination) as z:
        assert sum(Path(n).name.lower()=='skill.md' for n in z.namelist())==1
        assert all('..' not in Path(n).parts and not n.startswith('/') for n in z.namelist())
    return destination
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination',nargs='?')
    parser.add_argument('--output',dest='output')
    args=parser.parse_args()
    print(package(args.output or args.destination or ROOT/'dist/studio-toolkit-chatgpt.skill'))
