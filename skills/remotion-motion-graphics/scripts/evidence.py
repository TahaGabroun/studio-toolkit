#!/usr/bin/env python3
"""Snapshot declared sources/assets/candidates and reject stale evidence."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def contained(root,raw):
    p=(root/raw).resolve()
    if not p.is_relative_to(root):raise ValueError(f'File must be inside project: {raw}')
    return p
def snapshot(root,files):
    result={}
    for raw in files:
        p=contained(root,raw)
        if not p.is_file():raise ValueError(f'Missing file: {raw}')
        if p.suffix.lower()=='.svg':
            text=p.read_text()
            if re.search(r'<script|<foreignObject|\bon\w+\s*=|(?:href|xlink:href)\s*=\s*["\']\s*(?:https?:|data:|javascript:)',text,re.I):raise ValueError(f'Unsafe SVG: {raw}')
        result[str(p.relative_to(root))]=digest(p)
    out=root/'qa/evidence.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps({'files':result,'approval':'pending; hashes do not establish authenticity'},indent=2)+'\n')
def verify(root):
    data=json.loads((root/'qa/evidence.json').read_text())
    for name,sha in data['files'].items():
        p=contained(root,name)
        if not p.is_file() or digest(p)!=sha:raise ValueError(f'Stale evidence: {name}')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['snapshot','verify']);p.add_argument('project',type=Path);p.add_argument('files',nargs='*');a=p.parse_args()
    try:
        if a.action=='snapshot':
            if not a.files:raise ValueError('Declare at least one file')
            snapshot(a.project.resolve(),a.files)
        else:verify(a.project.resolve())
        print('Evidence hashes verified; creative and authenticity review remain separate.')
    except (OSError,ValueError) as e:raise SystemExit(f'ERROR: {e}')
