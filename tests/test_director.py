import copy
import shutil
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/studio-toolkit/scripts'))
import studio
import director


def brief(**changes):
    value={'schema_version':1,'idea':'Explain a process clearly','audience':'Curious adults','goal':'Understand a mechanism','scope':'full-video','style':'scientific','needs':['anatomy','mechanism'],'narration':{'mode':'generate'},'scenes':[{'id':'a','purpose':'Identify the relevant structure','needs':['anatomy']},{'id':'b','purpose':'Explain what changes and why','needs':['mechanism']}]}
    value.update(changes);return value


class Director(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'film';studio.init(self.root,'Production director test',fmt='vertical',duration=4)
    def tearDown(self):self.temp.cleanup()
    def plan(self,r=None):return director.plan_project(self.root,r or brief())
    def insert(self,**changes):
        return brief(scope='insert',style='auto',needs=['data'],narration={'mode':'none'},scenes=[],**changes)
    def record(self,plan,gate='content',decision='pass'):
        g=next(x for x in plan['gates'] if x['id']==gate)
        return {'gate_id':gate,'actor':'agent','decision':decision,'observations':[{'criterion':c,'verdict':decision,'note':'Unit fixture exercises review storage; this is not a real creative assessment.','evidence':[]} for c in g['criteria']]}
    def script(self):
        (self.root/'script.md').write_text('Unit fixture spoken script.')
        studio.write(self.root/'script.json',{'title':'Process','promise':'Explain the process','language':'en','scenes':[{'id':'a','role':'hook','narration':'What changes?','visual':'Identify the structure','source_ids':['fixture']},{'id':'b','role':'payoff','narration':'A connection changes.','visual':'Show the causal relationship','source_ids':['fixture']}]})
    def test_scientific_routes_anatomy_before_renderer_and_selects_relevant_tools(self):
        p=self.plan();ids=[x['skill'] for x in p['routes']]
        self.assertLess(ids.index('anatomy'),ids.index(p['master']['skill']))
        self.assertNotIn('youtube-strategy',ids);self.assertNotIn('map-route',ids)
        self.assertEqual([x['id'] for x in p['gates']],['content','look','timing','finish','delivery'])
    def test_channel_audit_is_explicit_not_compulsory(self):
        self.assertIn('youtube-strategy',[x['skill'] for x in self.plan(brief(channel_strategy=True))['routes']])
    def test_silent_data_insert_has_no_voice_or_long_form_script_stage(self):
        p=self.plan(self.insert());self.assertEqual(p['master']['skill'],'animated-graph')
        self.assertNotIn('timing',[x['id'] for x in p['gates']]);self.assertEqual(p['narration']['provider'],'none')
        self.assertNotIn('youtube-script-writer',[x['skill'] for x in p['routes']])
    def test_schematic_map_never_substitutes_for_real_geography(self):
        r=brief(scope='insert',style='auto',needs=['route'],narration={'mode':'none'},scenes=[])
        self.assertEqual(director.build(self.root,r)['master']['skill'],'map-route')
        r['real_geography']=True;p=director.build(self.root,r)
        self.assertNotEqual(p['master']['skill'],'map-route');self.assertNotIn('map-route',[x['skill'] for x in p['routes']])
        self.assertTrue(any('coordinates' in x['requirement'] for x in p['conditions']))
    def test_generic_phone_requires_explicit_illustration_permission(self):
        r=brief(scope='insert',style='auto',needs=['layers'],narration={'mode':'none'},scenes=[])
        self.assertIn('anatomy',[x['skill'] for x in director.build(self.root,r)['routes']])
        r['accurate_layers']=False;self.assertEqual(director.build(self.root,r)['master']['skill'],'exploded-view')
    def test_3d_cartoon_native_requirement_is_not_silently_upscaled(self):
        r=brief(style='3d-cartoon',needs=['characters'],scenes=[])
        p=director.build(self.root,r);self.assertNotEqual(p['master']['profile'],'cartoon-720-upscale');self.assertTrue(p['master']['adaptations'])
        r['allow_upscale']=True;self.assertEqual(director.build(self.root,r)['master']['profile'],'cartoon-720-upscale')
    def test_explicit_renderer_and_existing_renderer_are_preserved(self):
        self.assertEqual(director.build(self.root,brief(renderer='remotion'))['master']['engine_family'],'remotion')
        p=studio.read(self.root/'project.json');p['engine']='remotion';studio.write(self.root/'project.json',p)
        self.assertEqual(director.build(self.root,brief())['master']['skill'],'remotion-video')
    def test_long_minimal_video_is_not_a_stretched_quick_template(self):
        p=studio.read(self.root/'project.json');p['duration_frames']=2700;studio.write(self.root/'project.json',p)
        plan=director.build(self.root,brief(style='minimal',needs=[],scenes=[],narration={'mode':'none'}))
        self.assertNotEqual(plan['master']['skill'],'minimalistic-graphics')
    def test_multiple_formats_require_separate_visual_and_media_evidence(self):
        p=self.plan(brief(additional_formats=['landscape','square']))
        self.assertEqual(len(p['formats']),3)
        finish=next(g for g in p['gates'] if g['id']=='finish')
        self.assertIn('variants/1920x1080/render/final.mp4',finish['required_artifacts'])
    def test_provided_recording_mode_preserves_the_take(self):
        p=self.plan(brief(narration={'mode':'provided','path':'assets/approved.m4a'}))
        self.assertEqual(p['narration']['provider'],'provided recording');self.assertEqual(p['narration']['path'],'assets/approved.m4a')
    def test_scene_routes_are_specific(self):
        r=brief(needs=['anatomy','data'],scenes=[{'id':'structure','purpose':'Identify the structure','needs':['anatomy']},{'id':'measurement','purpose':'Compare actual measurements','needs':['data']}])
        p=director.build(self.root,r);self.assertIn('anatomy',p['scene_routes'][0]['skills']);self.assertNotIn('anatomy',p['scene_routes'][1]['skills'])
    def test_replanning_is_deterministic_and_preserves_authored_work(self):
        p=self.plan();before=(self.root/'production-plan.json').read_bytes();(self.root/'my-notes.txt').write_text('keep')
        self.assertEqual(self.plan(),p);self.assertEqual((self.root/'production-plan.json').read_bytes(),before)
        r=brief(style='documentary')
        with self.assertRaises(ValueError):director.plan_project(self.root,r)
        self.assertEqual((self.root/'production-plan.json').read_bytes(),before);self.assertEqual((self.root/'my-notes.txt').read_text(),'keep')
    def test_duplicate_scene_ids_and_path_escape_rejected(self):
        r=brief();r['scenes'].append(r['scenes'][0])
        with self.assertRaises(ValueError):director.build(self.root,r)
        with self.assertRaises(ValueError):director.build(self.root,brief(data_source='../../outside.csv'))
    def test_next_does_not_generate_audio_or_expose_key(self):
        self.plan()
        with patch.dict('os.environ',{'ELEVENLABS_API_KEY':'secret-test-value'}):result=director.next_action(self.root)
        self.assertNotIn('secret-test-value',json.dumps(result));self.assertEqual(result['gate']['id'],'content');self.assertFalse((self.root/'narration.json').exists())
    def test_voice_generation_respects_content_review_before_any_request(self):
        import elevenlabs_narration
        self.plan()
        with self.assertRaisesRegex(ValueError,'Review content'):elevenlabs_narration.generate(self.root,'fixture')
    def test_voice_generation_cannot_override_silent_direction(self):
        import elevenlabs_narration
        self.plan(self.insert())
        with self.assertRaisesRegex(ValueError,'does not request new speech'):elevenlabs_narration.generate(self.root,'fixture')
    def test_missing_evidence_cannot_pass_review(self):
        p=self.plan()
        with self.assertRaisesRegex(ValueError,'Missing review evidence'):director.review(self.root,self.record(p))
    def test_unresolved_findings_and_missing_criteria_cannot_pass(self):
        p=self.plan();self.script();r=self.record(p);r['observations'][0]['verdict']='revise'
        with self.assertRaises(ValueError):director.review(self.root,r)
        r=self.record(p);r['observations'].pop()
        with self.assertRaises(ValueError):director.review(self.root,r)
    def test_upstream_review_must_pass_before_later_review(self):
        p=self.plan()
        with self.assertRaisesRegex(ValueError,'earlier phase'):director.review(self.root,self.record(p,'look'))
    def test_changed_script_stales_content_and_keeps_history(self):
        p=self.plan();self.script();director.review(self.root,self.record(p));self.assertEqual(director.next_action(self.root)['gate']['id'],'look')
        (self.root/'script.md').write_text('Changed spoken argument requires review.')
        result=director.next_action(self.root);self.assertEqual(result['gate']['id'],'content');self.assertEqual(result['gates'][0]['status'],'stale')
        self.assertEqual(len(studio.read(self.root/'.studio-director/reviews.json')),1)
    def test_visual_replan_preserves_reviewed_script_and_no_model_call(self):
        p=self.plan();self.script();record=self.record(p);record['observations'][0]['evidence']=['production-requirements.json','production-plan.json','project.json'];director.review(self.root,record);before=(self.root/'script.json').read_bytes()
        r=brief(style='documentary');director.plan_project(self.root,r,replace=True)
        result=director.next_action(self.root);self.assertEqual(result['gates'][0]['status'],'pass');self.assertEqual(result['gate']['id'],'look');self.assertEqual((self.root/'script.json').read_bytes(),before)
    def test_content_tracks_runtime_but_not_equivalent_fps_conversion(self):
        plan=self.plan();self.script();director.review(self.root,self.record(plan))
        p=studio.read(self.root/'project.json');p['fps']=60;p['duration_frames']=240;studio.write(self.root/'project.json',p)
        director.plan_project(self.root,replace=True);self.assertEqual(director.next_action(self.root)['gate']['id'],'look')
        p['duration_frames']=480;studio.write(self.root/'project.json',p);director.plan_project(self.root,replace=True)
        self.assertEqual(director.next_action(self.root)['gate']['id'],'content')
    def test_changed_requirements_block_next_until_replanned(self):
        self.plan();r=studio.read(self.root/'production-requirements.json');r['goal']='A different promise';studio.write(self.root/'production-requirements.json',r)
        with self.assertRaises(ValueError):director.next_action(self.root)
    def test_changed_scene_claim_or_factual_constraint_invalidates_content(self):
        for change in ['purpose','real_geography','accurate_layers','needs','assumptions']:
            with self.subTest(change=change):
                root=Path(self.temp.name)/change;studio.init(root,'Content change fixture',fmt='vertical',duration=4)
                r=brief(scope='insert',style='auto',needs=[],narration={'mode':'none'},scenes=[{'id':'a','purpose':'Reveal illustrative samples','needs':[]}])
                p=director.plan_project(root,r);director.review(root,self.record(p))
                revised=copy.deepcopy(r)
                if change=='purpose':revised['scenes'][0]['purpose']='Make a materially different factual claim'
                elif change=='needs':revised['needs']=['typography']
                elif change=='assumptions':revised['assumptions']=['These samples represent measured population values.']
                else:revised[change]=not director.requirements(r)[change]
                director.plan_project(root,revised,replace=True)
                self.assertEqual(director.next_action(root)['gate']['id'],'content')
    def test_data_source_is_required_before_content_pass(self):
        p=self.plan(self.insert())
        with self.assertRaisesRegex(ValueError,'data_source'):director.review(self.root,self.record(p))
    def proof_fixture(self):
        from PIL import Image
        p=studio.read(self.root/'project.json');p['width']=p['height']=16;studio.write(self.root/'project.json',p)
        (self.root/'data.csv').write_text('sample,value\nA,2\nB,4\nC,3\nD,8\n')
        plan=self.plan(self.insert(data_source='data.csv'))
        director.review(self.root,self.record(plan))
        (self.root/'design.md').write_text('Unit fixture only; not a professional creative assessment.')
        Image.new('RGB',(16,16),'white').save(self.root/'qa/style-frame.png')
        Image.new('RGB',(360,360),'white').save(self.root/'qa/mobile-preview.png')
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=white:s=16x16:r=30:d=4','-c:v','libx264','-pix_fmt','yuv420p',str(self.root/'qa/motion-test.mp4')],check=True)
        return plan,p
    def finish_fixture(self,plan,p):
        director.review(self.root,self.record(plan,'look'))
        (self.root/'scene.txt').write_text('Explicit calibration source fixture.')
        studio.write(self.root/'render-config.json',{'engine':'html','composition':'fixture','codec':'h264','source_files':['scene.txt'],**{k:p[k] for k in ['width','height','fps','duration_frames']}})
        shutil.copy2(self.root/'qa/motion-test.mp4',self.root/'render/final.mp4')
        (self.root/'qa-report.md').write_text('Automated gate-storage test fixture, no human creative approval.')
        studio.write(self.root/'qa/automated.json',{'status':'pass','video_sha256':studio.digest(self.root/'render/final.mp4'),'input_hashes':studio.fingerprints(self.root,'render')})
    def test_real_media_gate_chain_and_source_change_invalidation(self):
        plan,p=self.proof_fixture();self.finish_fixture(plan,p)
        director.review(self.root,self.record(plan,'finish'))
        (self.root/'publication.md').write_text('Calibration fixture only; rights are original; no upload or human approval.')
        result=director.review(self.root,self.record(plan,'delivery'))
        self.assertEqual(result['status'],'reviewed-delivery-package');self.assertFalse(result['upload_performed'])
        (self.root/'scene.txt').write_text('Changed source requires new render/QA evidence.')
        self.assertEqual(director.next_action(self.root)['gate']['id'],'finish')
        with self.assertRaisesRegex(ValueError,'inputs changed'):director.review(self.root,self.record(plan,'finish'))
    def test_forged_video_qa_hash_cannot_pass_finish(self):
        plan,p=self.proof_fixture();self.finish_fixture(plan,p)
        qa=studio.read(self.root/'qa/automated.json');qa['video_sha256']='0'*64;studio.write(self.root/'qa/automated.json',qa)
        with self.assertRaisesRegex(ValueError,'exact encoded'):director.review(self.root,self.record(plan,'finish'))
    def test_mobile_proof_must_really_be_mobile_size(self):
        from PIL import Image
        plan,p=self.proof_fixture();Image.new('RGB',(1080,1080),'white').save(self.root/'qa/mobile-preview.png')
        with self.assertRaisesRegex(ValueError,'360px'):director.review(self.root,self.record(plan,'look'))
    def test_review_evidence_cannot_escape_project(self):
        plan=self.plan();self.script();record=self.record(plan)
        record['observations'][0]['evidence']=['../private.txt']
        with self.assertRaisesRegex(ValueError,'escapes'):director.review(self.root,record)
    def test_cli_works_from_repository_wrapper(self):
        source=self.root/'requirements-input.json';studio.write(source,brief())
        subprocess.run([sys.executable,str(ROOT/'scripts/studio.py'),'plan',str(self.root),'--requirements',str(source)],check=True,capture_output=True)
        r=subprocess.run([sys.executable,str(ROOT/'scripts/studio.py'),'next',str(self.root)],check=True,capture_output=True,text=True)
        self.assertEqual(json.loads(r.stdout)['gate']['id'],'content')
    def test_silent_scene_rules_do_not_invent_narration_cues(self):
        p=self.plan(self.insert())
        self.assertTrue(any('authored frame events' in rule for rule in p['scene_routes'][0]['rules']))
        self.assertFalse(any('measured cue IDs' in rule for rule in p['scene_routes'][0]['rules']))
    def test_only_explicit_no_narration_projects_can_use_uncued_frame_events(self):
        self.plan(brief(scope='insert',style='auto',needs=[],scenes=[],narration={'mode':'none'}))
        studio.write(self.root/'storyboard.json',{'scenes':[{'id':'a','composition':'Authored visual change','targets':['line'],'focus':'line','transition':'hold'}]})
        studio.write(self.root/'timeline.json',{'fps':30,'duration_frames':120,'scenes':[{'id':'a','start_frame':0,'end_frame':120}],'events':[{'id':'e','start_frame':8,'end_frame':80,'target':'line','effect':'build'}]})
        self.assertFalse(studio.validate(self.root)['errors'])
        r=studio.read(self.root/'production-requirements.json');r['narration']['mode']='generate';studio.write(self.root/'production-requirements.json',r)
        self.assertIn('cue_id required',str(studio.validate(self.root)['errors']))
    def test_portable_package_contains_director_and_contracts(self):
        import importlib.util,zipfile
        spec=importlib.util.spec_from_file_location('director_pack',ROOT/'scripts/package_chatgpt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        path=m.package(Path(self.temp.name)/'portable.skill')
        with zipfile.ZipFile(path) as z:
            self.assertIn('studio-toolkit/scripts/director.py',z.namelist());z.extractall(Path(self.temp.name)/'unpacked')
        source=self.root/'requirements-input.json';studio.write(source,brief())
        script=Path(self.temp.name)/'unpacked/studio-toolkit/scripts/studio.py'
        subprocess.run([sys.executable,str(script),'plan',str(self.root),'--requirements',str(source)],check=True,capture_output=True)

if __name__=='__main__':unittest.main()
