import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/studio-toolkit/scripts'))
import studio

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
manage=load('manage',ROOT/'scripts/manage_skills.py')

class Core(unittest.TestCase):
 def setUp(self):
    self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'film';studio.init(self.root,'A tree and its carbon',duration=2)
 def tearDown(self):self.tmp.cleanup()
 def artifacts(self):
    import numpy as np
    import media
    media.wav(self.root/'assets/voice.wav',np.sin(2*np.pi*440*np.arange(96000)/48000)*.1)
    studio.write(self.root/'script.json',{'title':'A tree','promise':'Explain carbon','language':'en','scenes':[{'id':'a','role':'hook','narration':'Where does the mass come from?','visual':'Identify atmospheric carbon','source_ids':['source']},{'id':'b','role':'payoff','narration':'Carbon is incorporated into sugars.','visual':'Build the carbon chain','source_ids':['source']}]})
    studio.write(self.root/'storyboard.json',{'scenes':[{'id':x,'composition':'A carbon chain','targets':['carbon'],'focus':'carbon','transition':'hold'} for x in ['a','b']]})
    studio.write(self.root/'timeline.json',{'fps':30,'duration_frames':60,'scenes':[{'id':'a','start_frame':0,'end_frame':30},{'id':'b','start_frame':30,'end_frame':60}],'events':[{'id':'e','start_frame':0,'end_frame':30,'target':'carbon','cue_id':'c','effect':'focus'}]})
    studio.write(self.root/'segments.json',{'segments':[{'id':'c','start_s':0,'end_s':1,'text':'A carbon chain.'}]})
    studio.align(self.root,'assets/voice.wav',self.root/'segments.json','synthetic-test')
 def test_valid_draft_is_pending(self):
    self.assertFalse(studio.validate(self.root)['errors']);self.assertEqual(studio.statuses(self.root)['idea'],'pending')
 def test_zero_and_nan_duration_rejected(self):
    for x in [0,float('nan')]:
      with self.assertRaises(ValueError):studio.init(Path(self.tmp.name)/str(x),'x',duration=x)
 def test_rounding_contract(self):self.assertEqual(studio.frame('0.05',30),2)
 def test_all_formats(self):
    for fmt,(w,h) in studio.FORMATS.items():
      p=Path(self.tmp.name)/fmt;studio.init(p,'x',fmt);self.assertEqual((studio.read(p/'project.json')['width'],studio.read(p/'project.json')['height']),(w,h))
 def test_schema_wrong_direction(self):
    p=studio.read(self.root/'project.json');p['direction']='sideways';studio.write(self.root/'project.json',p);self.assertTrue(studio.validate(self.root)['errors'])
 def test_valid_synced_project(self):self.artifacts();self.assertFalse(studio.validate(self.root)['errors'])
 def test_scene_gap_fails(self):
    self.artifacts();t=studio.read(self.root/'timeline.json');t['scenes'][1]['start_frame']=31;studio.write(self.root/'timeline.json',t);self.assertIn('gap',str(studio.validate(self.root)['errors']))
 def test_unknown_target_fails(self):
    self.artifacts();t=studio.read(self.root/'timeline.json');t['events'][0]['target']='wrong';studio.write(self.root/'timeline.json',t);self.assertIn('Unknown visual',str(studio.validate(self.root)['errors']))
 def test_sync_drift_fails(self):
    self.artifacts();t=studio.read(self.root/'timeline.json');t['events'][0]['start_frame']=8;studio.write(self.root/'timeline.json',t);self.assertIn('not aligned',str(studio.validate(self.root)['errors']))
 def test_caption_corruption_fails(self):
    self.artifacts();(self.root/'captions.srt').write_text('wrong');self.assertIn('Captions differ',str(studio.validate(self.root)['errors']))
 def test_missing_caption_fails(self):
    self.artifacts();(self.root/'captions.srt').unlink();self.assertIn('Missing captions',str(studio.validate(self.root)['errors']))
 def test_end_drift_fails(self):
    self.artifacts();t=studio.read(self.root/'timeline.json');t['events'][0]['end_frame']=59;studio.write(self.root/'timeline.json',t);self.assertIn('end not aligned',str(studio.validate(self.root)['errors']))
 def test_bad_cue_import_preserves_approved_files(self):
    self.artifacts();before={name:(self.root/name).read_bytes() for name in ['narration.json','timeline.json','captions.srt']}
    studio.write(self.root/'segments.json',{'segments':[{'id':'renamed','start_s':0,'end_s':1,'text':'A carbon chain.'}]})
    with self.assertRaises(ValueError):studio.align(self.root,'assets/voice.wav',self.root/'segments.json','synthetic-test')
    self.assertTrue(all((self.root/name).read_bytes()==value for name,value in before.items()))
 def test_missing_declared_source_fails(self):
    p=studio.read(self.root/'project.json');studio.write(self.root/'render-config.json',{'engine':'html','composition':'scene',**{k:p[k] for k in ['width','height','fps','duration_frames']},'codec':'h264','source_files':['absent.tsx']})
    self.assertIn('Missing renderer source',str(studio.validate(self.root)['errors']))
 def test_nonfinite_json_rejected(self):
    for value in ['NaN','Infinity','1e309']:
      (self.root/'project.json').write_text('{"duration_frames": '+value+'}')
      with self.assertRaises(ValueError):studio.read(self.root/'project.json')
 def test_caption_validation_without_pending_timeline(self):
    self.artifacts();(self.root/'timeline.json').unlink();(self.root/'captions.srt').write_text('corrupted')
    self.assertIn('Captions differ',str(studio.validate(self.root)['errors']))
 def test_narration_byte_change_fails(self):
    self.artifacts();p=self.root/'assets/voice.wav';p.write_bytes(p.read_bytes()+b'changed');self.assertIn('Narration audio changed',str(studio.validate(self.root)['errors']))
 def test_overlap_import_fails(self):
    self.artifacts();studio.write(self.root/'segments.json',{'segments':[{'start_s':0,'end_s':1.5,'text':'one'},{'start_s':1,'end_s':2,'text':'two'}]})
    with self.assertRaises(ValueError):studio.align(self.root,'assets/voice.wav',self.root/'segments.json','synthetic-test')
 def test_missing_asset_and_escape_fail(self):
    studio.write(self.root/'assets.json',{'assets':[{'id':'x','path':'missing.png','sha256':'a'*64,'license':'MIT','source':'original'}]});self.assertIn('Missing asset',str(studio.validate(self.root)['errors']))
    with self.assertRaises(ValueError):studio.local(self.root,'../../outside')
 def test_resume_invalidates_downstream(self):
    studio.complete(self.root,'idea');studio.complete(self.root,'research');self.assertEqual(studio.statuses(self.root)['research'],'complete')
    (self.root/'brief.md').write_text('changed promise');self.assertEqual(studio.statuses(self.root)['research'],'stale')
 def test_new_asset_does_not_invalidate_script_inputs(self):
    studio.complete(self.root,'idea');(self.root/'assets/new.txt').write_text('original');self.assertEqual(studio.statuses(self.root)['idea'],'complete')
 def test_cannot_skip_stage(self):
    with self.assertRaises(ValueError):studio.complete(self.root,'script')
 def test_stale_qa_report_rejected(self):
    self.artifacts()
    for name in ['script.md','animation.md']:(self.root/name).write_text('Reviewed original source')
    p=studio.read(self.root/'project.json')
    studio.write(self.root/'render-config.json',{'engine':'html','composition':'scene',**{k:p[k] for k in ['width','height','fps','duration_frames']},'codec':'h264','source_files':['animation.md']})
    studio.write(self.root/'mix.json',{'target_lufs':-16,'true_peak_db':-1.5,'tracks':[{'path':'assets/voice.wav','role':'narration','start_frame':0,'gain_db':0}]})
    shutil.copy2(self.root/'assets/voice.wav',self.root/'render/mix.wav');(self.root/'render/final.mp4').write_bytes(b'deliberate test fixture; not real media')
    for stage in list(studio.STAGES)[:11]:studio.complete(self.root,stage)
    (self.root/'qa-report.md').write_text('Automated evidence fixture')
    studio.write(self.root/'qa/automated.json',{'status':'pass','video_sha256':'a'*64,'input_hashes':studio.fingerprints(self.root,'render')})
    with self.assertRaisesRegex(ValueError,'different video'):studio.complete(self.root,'qa')
    studio.write(self.root/'qa/automated.json',{'status':'pass','video_sha256':studio.digest(self.root/'render/final.mp4'),'input_hashes':{}})
    with self.assertRaisesRegex(ValueError,'inputs changed'):studio.complete(self.root,'qa')
 def test_install_conflict_atomic_and_uninstall_safe(self):
    dest=Path(self.tmp.name)/'skills';dest.mkdir();unrelated=dest/'youtube-agent';unrelated.mkdir();(unrelated/'keep').write_text('mine')
    with self.assertRaises(ValueError):manage.manage('install',dest)
    self.assertFalse((dest/'studio-toolkit').exists());manage.manage('uninstall',dest);self.assertEqual((unrelated/'keep').read_text(),'mine')
 def test_install_symlink_lifecycle(self):
    dest=Path(self.tmp.name)/'skills';self.assertEqual(manage.manage('install',dest),0);self.assertEqual(manage.manage('validate',dest),0);manage.manage('update',dest);manage.manage('uninstall',dest);self.assertFalse((dest/'studio-toolkit').exists())
 def test_script_hook_payoff_checks(self):
    self.artifacts();s=studio.read(self.root/'script.json');self.assertFalse(studio.script_report(s,30)['errors']);s['scenes'][-1]['role']='context';self.assertTrue(studio.script_report(s,30)['errors'])

class Distribution(unittest.TestCase):
 def test_repository(self):
    validator=load('validator',ROOT/'scripts/validate_repository.py');self.assertEqual(validator.check(),[])
 def test_standalone_bundle_runtime(self):
    import zipfile
    pack=load('pack',ROOT/'scripts/package_chatgpt.py')
    with tempfile.TemporaryDirectory() as d:
      out=pack.package(Path(d)/'toolkit.skill')
      with zipfile.ZipFile(out) as z:
        self.assertEqual(sum(Path(n).name=='SKILL.md' for n in z.namelist()),1);z.extractall(Path(d)/'extracted')
      skill=Path(d)/'extracted/studio-toolkit';target=Path(d)/'new'
      subprocess.run([sys.executable,str(skill/'scripts/studio.py'),'init',str(target),'--title','Portable bundle'],check=True,capture_output=True)
      r=subprocess.run([sys.executable,str(skill/'scripts/studio.py'),'validate',str(target)],check=True,capture_output=True,text=True);self.assertIn('"errors": []',r.stdout)
 def test_upstream_tools_real_cli(self):
    script=ROOT/'skills/youtube-agent/scripts/yt-script/hookscore.py'
    r=subprocess.run([sys.executable,str(script),'--hook','Why does a tree grow heavier?','--json'],check=True,capture_output=True,text=True);self.assertIsInstance(json.loads(r.stdout),list)
 def test_evidence_stale_and_svg(self):
    e=load('evidence',ROOT/'skills/remotion-motion-graphics/scripts/evidence.py')
    with tempfile.TemporaryDirectory() as d:
      root=Path(d);(root/'data.txt').write_text('source');e.snapshot(root,['data.txt']);e.verify(root);(root/'data.txt').write_text('changed')
      with self.assertRaises(ValueError):e.verify(root)
      (root/'bad.svg').write_text('<svg><script>bad()</script></svg>')
      with self.assertRaises(ValueError):e.snapshot(root,['bad.svg'])

if __name__=='__main__':unittest.main()
