import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'skills/studio-toolkit/scripts'))
import studio,media

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
class Media(unittest.TestCase):
 def setUp(self):
    self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'p';studio.init(self.root,'Calibration',duration=2)
    p=studio.read(self.root/'project.json');p['width']=64;p['height']=64;studio.write(self.root/'project.json',p)
    studio.write(self.root/'storyboard.json',{'scenes':[{'id':'a','composition':'solid calibration','targets':['node'],'focus':'node','transition':'hold'}]})
    studio.write(self.root/'timeline.json',{'fps':30,'duration_frames':60,'scenes':[{'id':'a','start_frame':0,'end_frame':60}],'events':[{'id':'e','start_frame':15,'end_frame':45,'target':'node','cue_id':'c','effect':'focus'}]})
    media.test_audio(self.root);studio.write(self.root/'segments.json',{'segments':[{'id':'c','start_s':.5,'end_s':1.5,'text':'Test signal.'}]});studio.align(self.root,'assets/calibration.wav',self.root/'segments.json','synthetic-test')
    self.video=self.root/'render/silent.mp4';subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=white:s=64x64:r=30:d=2','-c:v','libx264','-pix_fmt','yuv420p',str(self.video)],check=True)
 def tearDown(self):self.temp.cleanup()
 def test_encoded_sync_and_qa(self):
    final=self.root/'render/final.mp4';media.mux(self.video,self.root/'assets/calibration.wav',final);r=media.qa(self.root,final,True)
    self.assertEqual(r['status'],'pass');self.assertLess(abs(r['calibration_peak_offsets_s'][0]),1/30);self.assertTrue((self.root/'qa/contact-sheet.jpg').is_file())
 def test_shifted_audio_detected(self):
    x=media.pcm(self.root/'assets/calibration.wav');x=np.concatenate([np.zeros(4800),x])[:len(x)];media.wav(self.root/'shift.wav',x)
    final=self.root/'render/final.mp4';media.mux(self.video,self.root/'shift.wav',final);r=media.qa(self.root,final,True)
    self.assertIn('Calibration audio',str(r['errors']))
 def test_wrong_resolution_fails(self):
    final=self.root/'render/final.mp4';media.mux(self.video,self.root/'assets/calibration.wav',final);p=studio.read(self.root/'project.json');p['width']=128;studio.write(self.root/'project.json',p)
    self.assertIn('dimensions mismatch',str(media.qa(self.root,final,True)['errors']))
 def test_mux_never_silently_truncates(self):
    media.wav(self.root/'short.wav',np.zeros(4800))
    with self.assertRaises(ValueError):media.mux(self.video,self.root/'short.wav',self.root/'render/final.mp4')

class RetainedCode(unittest.TestCase):
 def test_corpus_reindex_idempotent(self):
    spec=importlib.util.spec_from_file_location('corpus',ROOT/'skills/content-os/scripts/chunk_corpus.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    with tempfile.TemporaryDirectory() as d:
      p=Path(d);(p/'source.md').write_text('Original carbon explanation and editorial evidence. '*100);db=m.create_database(p/'corpus.db')
      with contextlib.redirect_stdout(io.StringIO()):m.process_essays(p,db)
      first=db.execute('select count(*) from chunks').fetchone()[0]
      with contextlib.redirect_stdout(io.StringIO()):m.process_essays(p,db)
      self.assertEqual(first,db.execute('select count(*) from chunks').fetchone()[0]);db.close()
    with self.assertRaises(ValueError):list(m.split_into_chunks('text',10,10))
 def test_procedural_sound_renders(self):
    path=ROOT/'skills/claude-motion-adapted/scripts';sys.path.insert(0,str(path))
    from sfx.mix import Mix
    from sfx.synth import pop
    with tempfile.TemporaryDirectory() as d:
      mix=Mix(1);mix.put(.25,pop(900,400),.2)
      with contextlib.redirect_stdout(io.StringIO()):mix.write(str(Path(d)/'sfx.wav'))
      self.assertTrue((Path(d)/'sfx.wav').stat().st_size>40000)

if __name__=='__main__':unittest.main()
