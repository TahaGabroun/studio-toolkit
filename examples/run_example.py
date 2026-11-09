#!/usr/bin/env python3
"""Run a complete local HTML production with deterministic visual/audio calibration."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/studio-toolkit/scripts'))
from studio import init,write,read,digest,align,complete,STAGES
from media import test_audio,mux,qa

def run(output,browser=None):
    root=init(output,'Let the cue direct the eye.',duration=4)
    p=read(root/'project.json');p['engine']='html';write(root/'project.json',p)
    text=['Identify one concept.','Then reveal its relationship.'];targets=['concept','relationship']
    write(root/'script.json',{'title':p['title'],'promise':'Use one timeline for visual and audio focus','language':'en','scenes':[{'id':f's{i}','role':'hook' if i==0 else 'payoff','narration':t,'visual':f'Focus the {targets[i]} node','source_ids':['original']} for i,t in enumerate(text)]})
    (root/'script.md').write_text('# Script\n\nIdentify one concept. [VISUAL: concept node]\n\nThen reveal its relationship. [VISUAL: relationship node]\n\nTest signals are not spoken narration.\n')
    write(root/'storyboard.json',{'scenes':[{'id':f's{i}','composition':'Persistent connected nodes','targets':[target],'focus':target,'transition':'12-frame focus handoff'} for i,target in enumerate(targets)]})
    timeline={'fps':30,'duration_frames':120,'scenes':[{'id':'s0','start_frame':0,'end_frame':60},{'id':'s1','start_frame':60,'end_frame':120}],'events':[{'id':f'e{i}','start_frame':15+i*60,'end_frame':54+i*60,'target':target,'cue_id':f'c{i}','effect':'focus'} for i,target in enumerate(targets)]}
    write(root/'timeline.json',timeline);test_audio(root)
    write(root/'segments.json',{'segments':[{'id':f'c{i}','start_s':.5+i*2,'end_s':1.8+i*2,'text':t} for i,t in enumerate(text)]})
    align(root,'assets/calibration.wav',root/'segments.json','synthetic-test')
    write(root/'assets.json',{'assets':[{'id':'test-audio','path':'assets/calibration.wav','sha256':digest(root/'assets/calibration.wav'),'license':'CC0-1.0','source':'Original generated 1200 Hz timing pulses'}]})
    html=(ROOT/'templates/narration.html').read_text().replace('__TIMELINE_JSON__',__import__('json').dumps(timeline))
    (root/'scene.html').write_text(html)
    (root/'animation.md').write_text('# Animation\n\nscene.html consumes the same events used to synthesize the timing pulses. Out-of-order seek hashes are verified during capture.\n')
    (root/'research.md').write_text('# Source\n\nOriginal explanatory timing test. No scientific or measured performance claim.\n')
    write(root/'render-config.json',{'engine':'html','composition':'scene','width':1920,'height':1080,'fps':30,'duration_frames':120,'codec':'h264','source_files':['scene.html']})
    write(root/'mix.json',{'target_lufs':-16,'true_peak_db':-1.5,'tracks':[{'path':'assets/calibration.wav','role':'sfx','start_frame':0,'gain_db':0}]})
    import shutil
    shutil.copy2(root/'assets/calibration.wav',root/'render/mix.wav')
    for stage in list(STAGES)[:10]:complete(root,stage)
    cmd=[sys.executable,str(ROOT/'skills/motion-design/scripts/render_html.py'),str(root/'scene.html'),str(root/'render/silent.mp4'),'--duration','4','--check-determinism']
    if browser:cmd+=['--browser',browser]
    subprocess.run(cmd,check=True);mux(root/'render/silent.mp4',root/'render/mix.wav',root/'render/final.mp4');complete(root,'render')
    result=qa(root,root/'render/final.mp4',calibration=True)
    if result['errors']:raise ValueError(result['errors'])
    complete(root,'qa')
    (root/'publication.md').write_text('# Publication package\n\nOriginal Studio Toolkit calibration example. Test signals are not narration. Attach captions and source. Human review pending; no upload performed.\n')
    complete(root,'publication')
    print('Complete local workflow:',root.resolve())
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True);p.add_argument('--browser',default=os.environ.get('CHROMIUM'));a=p.parse_args();run(a.output,a.browser)
