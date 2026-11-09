#!/usr/bin/env python3
"""Analyze a rights-cleared reference into scene-cut times and representative frames."""
import argparse,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('video');p.add_argument('output',type=Path);p.add_argument('--threshold',type=float,default=.25);a=p.parse_args()
if not 0<a.threshold<1:raise SystemExit('Threshold must be 0..1')
a.output.mkdir(parents=True,exist_ok=True)
cmd=['ffmpeg','-hide_banner','-i',a.video,'-vf',f"select=gt(scene\\,{a.threshold}),showinfo",'-vsync','vfr',str(a.output/'cut-%04d.png')]
r=subprocess.run(cmd,capture_output=True,text=True,check=True)
cuts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',r.stderr)]
(a.output/'cuts.json').write_text(json.dumps({'source':str(Path(a.video).name),'cut_times_s':cuts,'rights':'User must verify reference use; no asset license inferred'},indent=2)+'\n')
print(f'Extracted {len(cuts)} scene candidates. Build a shot table and compare original licensed assets separately.')
