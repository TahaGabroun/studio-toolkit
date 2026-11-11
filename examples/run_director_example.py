#!/usr/bin/env python3
"""Prepare a directed native landscape insert; actual reviews control proof/finish.

No model or paid API calls. The data are declared illustrative calibration data.
"""
import argparse
import csv
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/studio-toolkit/scripts'))
import director,studio,media

def run(output,phase):
    output=Path(output).resolve()
    if phase=='prepare':
        studio.init(output,'A deliberate comparison',duration=4)
        project=studio.read(output/'project.json');project['engine']='html';studio.write(output/'project.json',project)
        data='sample,value\nA,2\nB,4\nC,3\nD,8\n';(output/'assets/data.csv').write_text(data)
        r={'schema_version':1,'idea':'Compare the supplied calibration samples','audience':'General viewers on desktop and mobile','goal':'Recognize the real four-value shape without implying measured performance','scope':'insert','style':'minimal','needs':['data'],'narration':{'mode':'none'},'data_source':'assets/data.csv','allow_upscale':False,'scenes':[{'id':'series','purpose':'Reveal the supplied samples and finish at 8; the series is not monotonic','needs':['data']}],'assumptions':['These are illustrative test values, not scientific measurements.']}
        (output/'brief.md').write_text('# Brief\n\nA four-second landscape insert for a clear, honest visual comparison. No narration or measured-performance claim.\n')
        (output/'research.md').write_text('# Evidence\n\nSupplied illustrative calibration values: A=2, B=4, C=3, D=8. Preserve the decrease from B to C. No population, channel-growth or scientific inference is supported.\n')
        (output/'design.md').write_text('# Visual direction\n\nNative 1920×1080, warm neutral background, teal series, Inter type, large required labels and one continuous graph. Quiet reveal and final hold; no decorative camera shake. Inspect at full resolution and 360px width.\n')
        assets=[]
        for filename in ['inter-500-normal.woff2','inter-700-normal.woff2','OFL-inter.txt']:
            target=output/'assets/fonts'/filename;target.parent.mkdir(exist_ok=True);shutil.copy2(studio.SKILL/'references/animation-runtime/kit/fonts'/filename,target)
            assets.append({'id':filename,'path':str(target.relative_to(output)),'sha256':studio.digest(target),'license':'OFL-1.1','source':'Retained Inter font distribution; original notice adjacent'})
        assets.append({'id':'data','path':'assets/data.csv','sha256':studio.digest(output/'assets/data.csv'),'license':'CC0-1.0','source':'Original explicit calibration fixture, not measured data'})
        studio.write(output/'assets.json',{'assets':assets})
        scene=output/'assets/scene/graph.html';scene.parent.mkdir(exist_ok=True)
        rows=list(csv.DictReader(io.StringIO(data)))
        storyboard={'scenes':[{'id':'series','composition':'One continuous comparison and endpoint counter','targets':['series-line','sample-values'],'focus':'series-line','transition':'readable final hold'}]}
        timeline={'fps':30,'duration_frames':120,'scenes':[{'id':'series','start_frame':0,'end_frame':120}],'events':[{'id':'draw-series','start_frame':8,'end_frame':83,'target':'series-line','effect':'build'}]}
        studio.write(output/'storyboard.json',storyboard);studio.write(output/'timeline.json',timeline)
        scene.write_text((studio.SKILL/'references/director/directed-graph.html').read_text().replace('__DATA__',json.dumps(rows)).replace('__TIMELINE__',json.dumps(timeline)))
        # Font URLs are relative to this nested authored scene.
        studio.write(output/'render-config.json',{'engine':'html','composition':'graph','codec':'h264','source_files':['assets/scene/graph.html','assets/data.csv'],**{k:project[k] for k in ['width','height','fps','duration_frames']}})
        director.plan_project(output,r)
    else:
        action=director.next_action(output)
        expected='look' if phase=='proof' else 'finish'
        if action.get('gate',{}).get('id')!=expected:raise ValueError(f'Review earlier work first; expected {expected}, next is {action.get("gate",{}).get("id")}')
        if phase=='proof':
            renderer=ROOT/'skills/motion-design/scripts/render_html.py'
            subprocess.run([sys.executable,str(renderer),str(output/'assets/scene/graph.html'),str(output/'qa/motion-test.mp4'),'--duration','4','--fps','30','--width','1920','--height','1080','--check-determinism'],check=True)
            subprocess.run(['ffmpeg','-v','error','-y','-ss','3.5','-i',str(output/'qa/motion-test.mp4'),'-frames:v','1',str(output/'qa/style-frame.png')],check=True)
            from PIL import Image
            with Image.open(output/'qa/style-frame.png') as image:image.resize((360,203)).save(output/'qa/mobile-preview.png')
        else:
            source=output/'qa/motion-test.mp4';target=output/'render/final.mp4'
            if target.exists() and studio.digest(target)!=studio.digest(source):raise ValueError('Existing master differs; preserve/review it explicitly')
            shutil.copy2(source,target)
            result=media.qa(output,target,silent=True)
            if result['errors']:raise ValueError(result['errors'])
    print(json.dumps(director.next_action(output),ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True);parser.add_argument('--phase',choices=['prepare','proof','finish'],default='prepare');args=parser.parse_args();run(args.output,args.phase)
