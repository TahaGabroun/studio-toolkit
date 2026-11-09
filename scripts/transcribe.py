#!/usr/bin/env python3
"""Optional local ASR; downloads an open model on first use. Not forced alignment."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('audio');p.add_argument('output');p.add_argument('--model',default='small');p.add_argument('--language',default=None)
a=p.parse_args()
try:from faster_whisper import WhisperModel
except ImportError:raise SystemExit('Install requirements-transcription.txt in a venv; or import reviewed timestamp JSON with studio.py align')
model=WhisperModel(a.model,device='cpu',compute_type='int8')
segments,info=model.transcribe(a.audio,language=a.language,word_timestamps=True)
items=[]
for segment in segments:
 for word in segment.words or []:items.append({'id':f'word-{len(items)+1}','start_s':word.start,'end_s':word.end,'text':word.word.strip()})
Path(a.output).write_text(json.dumps({'method':'asr-unreviewed','language':info.language,'segments':items},ensure_ascii=False,indent=2)+'\n')
print('ASR draft written. Check omissions, terminology, Arabic/English switches and phrase boundaries before import.')
