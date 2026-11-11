#!/usr/bin/env python3
"""Requirement-driven production routing and evidence-backed review checkpoints.

Plans and reviews only: never calls models, buys assets, renders or publishes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
from studio import SKILL, FORMATS, read, write, digest, local, schema_errors, production_config, workflow_check, probe, validate, script_report, fingerprints

VERSION = '1.0'


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()


def sha(value): return hashlib.sha256(canonical(value)).hexdigest()


def content_context(r, project):
    return {'requirements':{k:r[k] for k in ['idea','audience','goal','scope','narration','data_source','geography_source','needs','scenes','assumptions','real_geography','accurate_layers','channel_strategy']},
            'delivery':{'title':project['title'],'language':project['language'],'duration_seconds':project['duration_frames']/project['fps']}}


def evidence_digest(root, name, scope='bytes'):
    path=local(root,name)
    if scope=='content-intent':
        r,p,_=context(root);return sha(content_context(r,p))
    if scope!='bytes':raise ValueError('Unknown review evidence scope')
    return digest(path)


def requirements(value):
    errors = schema_errors('production-requirements', value)
    if errors: raise ValueError('; '.join(errors))
    result = {'renderer':'auto', 'allow_upscale':False, 'real_geography':False, 'accurate_layers':True,
              'channel_strategy':False, 'additional_formats':[], 'scenes':[], 'assumptions':[],
              'data_source':None, 'geography_source':None, **value}
    result['narration'] = {'path':None, **result['narration']}
    if result['narration']['path'] and Path(result['narration']['path']).is_absolute():raise ValueError('Narration path must be project-relative')
    ids = [s['id'] for s in result['scenes']]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate scene IDs')
    for key in ['data_source', 'geography_source']:
        if result[key] is not None and Path(result[key]).is_absolute(): raise ValueError(f'{key} must be project-relative')
    return result


def context(root, supplied=None):
    root = Path(root).resolve()
    value = supplied if supplied is not None else read(root/'production-requirements.json')
    r = requirements(value); p = read(root/'project.json')
    errors = schema_errors('project', p)
    if errors: raise ValueError('; '.join(errors))
    for key in ['data_source','geography_source']:
        if r[key]: local(root,r[key])
    if r['narration']['path']: local(root,r['narration']['path'])
    return r, p, production_config(root)


def needs_for(r): return set(r['needs']) | {n for scene in r['scenes'] for n in scene['needs']}


def master_for(r, p, needs):
    vertical = p['height'] > p['width'] and p['width'] * 16 == p['height'] * 9
    formats = any(FORMATS[fmt] != (p['width'],p['height']) for fmt in r['additional_formats'])
    chosen = r['renderer'] if r['renderer'] != 'auto' else p['engine']
    result = {'skill':'motion-design','engine_family':'html','profile':'custom','reason':'A single authored explanatory world benefits from direct deterministic scene control.','adaptations':[]}
    if chosen in ['html','remotion']:
        result.update(skill='remotion-video' if chosen=='remotion' else 'motion-design', engine_family=chosen, reason='Preserve the explicitly chosen or existing project renderer.')
    elif 'footage' in needs or 'screen' in needs or formats or r['style']=='documentary' or len(needs)>2:
        result.update(skill='remotion-video', engine_family='remotion', reason='Use one compositing timeline for editorial footage, varied inserts or independently reframed deliverables.')
    elif r['style']=='3d-cartoon' and vertical and r['allow_upscale'] and not formats:
        result.update(skill='cartoon-animation', profile='cartoon-720-upscale', reason='The requested vertical 3D character format explicitly permits the supplied engine’s 720×1280 capture and upscale.')
    elif r['style']=='stick-figure' and vertical and not formats:
        result.update(skill='stick-figure', profile='stick-1080', reason='The native vertical Canvas rig fits the requested expressive 2D character format.')
    elif r['scope']=='insert' and vertical and p['duration_frames']/p['fps'] <= 10 and not formats:
        if needs == {'data'}: result.update(skill='animated-graph',profile='graph',reason='A short vertical data insert fits the verified numeric-series template.')
        elif needs == {'route'} and not r['real_geography']: result.update(skill='map-route',profile='illustrative-map',reason='The requested short route is explicitly schematic, so seeded scenery is appropriate.')
        elif needs == {'layers'} and not r['accurate_layers']: result.update(skill='exploded-view',profile='generic-phone',reason='The request explicitly permits an illustrative generic layered phone.')
        elif r['style']=='minimal' and not needs: result.update(skill='minimalistic-graphics',profile='steps',reason='A short vertical progress motif fits the dot/steps/orbit template.')
    if r['style']=='3d-cartoon' and result['skill']!='cartoon-animation':
        result['adaptations'].append('Author the requested 3D character scene at the required resolution/layout using the retained rig/prop source; verify a native motion sample. Do not substitute a 720p clip as native 1080p/4K.')
    if r['style']=='stick-figure' and result['skill']!='stick-figure':
        result['adaptations'].append('Adapt the character rig, camera, caption bands and layout to this master; inspect the reframed motion sample.')
    if r['real_geography'] and 'route' in needs:
        result['adaptations'].append('Use sourced real coordinates and route geometry in an authored map; the seeded map-route template cannot establish real geography or travel times.')
    if r['accurate_layers'] and 'layers' in needs:
        result['adaptations'].append('Use subject-specific sourced geometry and labels; the generic phone template is not measured CAD or a scientific model.')
    if r['scope']!='insert' and r['style']=='minimal':
        result['adaptations'].append('Develop a sequence of meaningful visual states; do not stretch or loop the four-second steps motif into a full film.')
    if not vertical and needs & {'data','route','layers'}:
        result['adaptations'].append('Rebuild vertical-only insert layouts in the master’s native aspect ratio; use specialist source as design/data guidance rather than stretching a vertical clip.')
    if r['additional_formats']: result['adaptations'].append('Author and inspect each aspect ratio independently, preserving hierarchy and cue timing rather than cropping critical structures.')
    return result


def scene_skills(needs, r, master):
    result = []
    if set(needs) & {'anatomy','mechanism'} or 'layers' in needs and r['accurate_layers']: result.append('anatomy')
    if 'data' in needs: result.append('remotion-motion-graphics' if master['engine_family']=='remotion' else 'animated-graph')
    if 'route' in needs and not r['real_geography']: result.append('map-route')
    if 'layers' in needs and not r['accurate_layers']: result.append('exploded-view')
    if 'characters' in needs or r['style'] in ['3d-cartoon','stick-figure']:
        result.append('cartoon-animation' if r['style']=='3d-cartoon' else 'stick-figure' if r['style']=='stick-figure' else master['skill'])
    if 'typography' in needs and master['engine_family']=='remotion': result.append('remotion-motion-graphics')
    return list(dict.fromkeys(result))


def build(root, supplied=None):
    r,p,config=context(root,supplied);needs=needs_for(r);master=master_for(r,p,needs)
    routes=[]
    def route(skill,role,reason):
        if skill not in [x['skill'] for x in routes]:routes.append({'skill':skill,'role':role,'reason':reason})
    if r['channel_strategy']: route('youtube-strategy','channel decisions','Channel-level positioning or audience work was explicitly requested.')
    if r['scope']!='insert':
        route('youtube-agent','brief, evidence and packaging','Develop the audience promise and verifiable claims before visual production.')
        if r['narration']['mode']!='none':route('youtube-script-writer','spoken narrative','Write or audit narration; a supplied approved take fixes its spoken content.')
        route('content-os','asset and editorial continuity','Maintain provenance, approved artifacts and versioned handoffs.')
    route('claude-motion-adapted','art and motion direction','Choose one coherent visual grammar, restrained motion and a readable focal hierarchy.')
    for skill in scene_skills(needs,r,master):route(skill,'scene design or insert source','Use only for matching scene needs; adapt its assets/layout to the main renderer and shared frame clock.')
    route(master['skill'],'master renderer',master['reason'])
    scenes = r['scenes'] or [{'id':'visual-treatment','purpose':r['goal'],'needs':sorted(needs)}]
    scene_routes=[{'id':s['id'],'purpose':s['purpose'],'skills':scene_skills(s['needs'],r,master),'master_skill':master['skill'],
                   'rules':['One identifiable focal subject for this beat; movement explains its meaning.','Use authored frame events for the visible change and optional sound; do not invent speech cues.' if r['narration']['mode']=='none' else 'Preserve semantic target IDs and link focus/reveal/SFX to measured cue IDs.','Treat templates as source material; keep the chosen palette, typography, scale and camera language consistent.']} for s in scenes]
    mode=r['narration']['mode']
    narration={'mode':mode,'provider':config['narration']['provider'] if mode=='generate' else 'provided recording' if mode=='provided' else 'none',
               'path':r['narration']['path'],'rule':'Reuse the approved supplied take and import measured cues without rewriting it.' if mode=='provided' else 'Generate only after content review; reuse the cached request and measure actual cues before locking visual timing.' if mode=='generate' else 'No speech generation, forced narration cues or placeholder voice is needed.'}
    content_files=[]
    if r['channel_strategy']:content_files.append('strategy.md')
    if r['scope']!='insert':
        content_files+=['script.md'] + (['script.json'] if mode!='none' else [])
    factual=bool(needs & {'anatomy','mechanism','data','route','layers'}) or r['style']=='scientific'
    if factual:content_files.append('research.md')
    if mode=='provided' and r['narration']['path']:content_files.append(r['narration']['path'])
    for key in ['data_source','geography_source']:
        if r[key]:content_files.append(r[key])
    content_files=list(dict.fromkeys(content_files))
    gates=[{'id':'content','phase':'Audience promise, evidence and narrative', 'skills':[x['skill'] for x in routes if x['role'] in ['channel decisions','brief, evidence and packaging','spoken narrative','asset and editorial continuity']],
            'required_artifacts':content_files,'criteria':['brief-fit','truth-and-source-fidelity','narrative-or-insert-purpose'],
            'procedure':'Inspect the actual script/data/claim ledger; identify what the viewer should understand and why each beat is present. Resolve material factual or narrative issues before generating production speech.'},
           {'id':'look','phase':'Art direction and a small production proof','skills':[x['skill'] for x in routes if x['role'] in ['art and motion direction','scene design or insert source','master renderer']],
            'required_artifacts':['design.md','qa/style-frame.png','qa/mobile-preview.png','qa/motion-test.mp4'],
            'criteria':['coherent-art-direction','semantic-referents','mobile-typography','purposeful-motion','native-format-feasibility'],
            'procedure':'Create one representative style frame and a 3–5-second motion study of the hardest scene, plus a 360px-wide preview. Inspect hierarchy, geometry, readability and motion; fix major problems before building all assets or shots.'}]
    if mode!='none':gates.append({'id':'timing','phase':'Measured narration, storyboard and animatic','skills':[master['skill']],
       'required_artifacts':['narration.json','storyboard.json','timeline.json','captions.srt','qa/animatic.mp4'],
       'criteria':['measured-cue-alignment','narration-to-visible-target','caption-and-pronunciation','pacing-and-continuity'],
       'procedure':'After content review generate/reuse ElevenLabs speech or align the supplied take. Build the timed storyboard and a low-cost animatic from the actual cues. Inspect every focus switch and the densest caption; fix timing before final animation.'})
    gates += [{'id':'finish','phase':'Final animation, audio mix and encoded master','skills':[master['skill']],
               'required_artifacts':['render-config.json','render/final.mp4','qa/automated.json','qa-report.md'],
               'criteria':['encoded-media-integrity','visual-continuity','sound-or-silence-intent','final-mobile-and-full-frame-review'],
               'procedure':'Finish the approved visual treatment, mix from the shared frame clock, render and run automated QA. Inspect representative final encoded frames and transitions, and listen to the full mix when audio exists. Close critical/major findings; do not replace inspection with an automated score.'},
              {'id':'delivery','phase':'Publication package and honest handoff','skills':['content-os'] if r['scope']!='insert' else [],
               'required_artifacts':['publication.md'],'criteria':['complete-deliverables','rights-and-provenance','honest-review-status'],
               'procedure':'Package masters, captions where applicable, metadata, source/rights notes and QA findings. State automated, agent and human review separately. An upload is a separate authorized action.'}]
    conditions=[]
    def condition(gate,text):conditions.append({'before_gate':gate,'requirement':text})
    if 'data' in needs and not r['data_source']:condition('content','Supply actual data and its provenance in data_source; never invent values for a prettier curve.')
    if r['real_geography'] and 'route' in needs and not r['geography_source']:condition('content','Supply real coordinates/route evidence in geography_source; do not present seeded scenery as geography.')
    if mode=='provided' and not r['narration']['path']:condition('content','Select the approved project-relative recording path; no substitute voice is allowed.')
    for adaptation in master['adaptations']:condition('look',adaptation)
    outputs=[{k:p[k] for k in ['width','height','fps','duration_frames']}]
    for fmt in r['additional_formats']:
        w,h=FORMATS[fmt];variant={'width':w,'height':h,'fps':p['fps'],'duration_frames':p['duration_frames']}
        if variant not in outputs:outputs.append(variant)
    for variant in outputs[1:]:
        tag=f"{variant['width']}x{variant['height']}"
        gates[1]['required_artifacts'] += [f'qa/style-frame-{tag}.png',f'qa/mobile-preview-{tag}.png']
        finish=next(g for g in gates if g['id']=='finish')
        finish['required_artifacts'] += [f'variants/{tag}/render/final.mp4',f'variants/{tag}/qa/automated.json']
    plan={'schema_version':1,'director_version':VERSION,'input_fingerprint':sha([r,p,config]),
          'brief':{k:r[k] for k in ['idea','audience','goal','scope','assumptions']},'master':master,'formats':outputs,'routes':routes,'scene_routes':scene_routes,'narration':narration,
          'gates':gates,'conditions':conditions,
          'reuse_policy':['Keep approved research/script/assets and cached provider responses; do not regenerate merely to refresh a checkpoint.','Recheck the earliest stale review and dependent phases when its actual inputs change.','Use one master renderer; specialist inserts inherit the same palette/fonts, semantic IDs and measured timebase.'],
          'quality_policy':['Narration/meaning controls the visible referent; do not repeat narration as generic slides.','Prioritize correct structure, hierarchy and performance over the number of effects or tools.','Treat review records as evidence of a reviewer’s assessment, not proof of human approval or an automatic professional-quality score.']}
    errors=schema_errors('production-plan',plan)
    if errors:raise ValueError('; '.join(errors))
    return plan


def plan_project(root, supplied=None, replace=False):
    root=Path(root).resolve();r,_,_=context(root,supplied);plan=build(root,r)
    target=root/'production-plan.json'
    if target.exists() and read(target)!=plan and not replace:raise ValueError('Plan differs; inspect changes and use --replace to replan. Existing writing, media and review history are preserved.')
    if not (root/'production-requirements.json').exists() or read(root/'production-requirements.json')!=r:write(root/'production-requirements.json',r)
    if not target.exists() or read(target)!=plan:write(target,plan)
    lines=['# Production direction', '', f"**Goal:** {r['goal']}", f"**Audience:** {r['audience']}",f"**Main renderer:** {plan['master']['skill']} — {plan['master']['reason']}",'','## Tool flow','']
    lines += [f"- {x['skill']}: {x['role']}. {x['reason']}" for x in plan['routes']]
    lines += ['','## Scene assignments','']+[f"- {s['id']}: {s['purpose']} → {', '.join(s['skills']) or 'authored scene'} → {s['master_skill']}" for s in plan['scene_routes']]
    lines += ['','## Production checkpoints','']
    for gate in plan['gates']:
        lines += [f"### {gate['id']}: {gate['phase']}",'',gate['procedure'],'', 'Evidence: '+(', '.join(gate['required_artifacts']) or 'requirements and reviewer observations')+'.','']
    lines += ['## Conditions and adaptations','']+[f"- Before {x['before_gate']}: {x['requirement']}" for x in plan['conditions']]
    lines += ['','## Reuse and quality','']+['- '+x for x in plan['reuse_policy']+plan['quality_policy']]
    (root/'production-plan.md').write_text('\n'.join(lines)+'\n')
    return plan


def current(root):
    plan=read(Path(root)/'production-plan.json')
    if schema_errors('production-plan',plan):raise ValueError('Invalid production plan schema; inspect or replan')
    if plan!=build(root):raise ValueError('Production inputs or plan changed; inspect and replan before executing the next phase')
    return plan


def gate_fingerprint(root, plan, gate, ancestors):
    r,p,_=context(root)
    # A change in visual style does not invalidate the reviewed spoken script.
    semantic=content_context(r,p) if gate['id']=='content' else plan
    files=list(gate['required_artifacts'])
    if gate['id']=='finish' and (Path(root)/'render-config.json').is_file():files+=read(Path(root)/'render-config.json').get('source_files',[])
    hashes={name:digest(local(root,name)) if local(root,name).is_file() else None for name in files}
    return sha([semantic,p['language'],{k:gate[k] for k in ['id','required_artifacts','criteria']},hashes,ancestors])


def state(root, plan):
    path=Path(root)/'.studio-director/reviews.json'
    history=read(path) if path.exists() else []
    result=[];chain=[];prior=True
    for gate in plan['gates']:
        fingerprint=gate_fingerprint(root,plan,gate,chain)
        record=next((x for x in reversed(history) if x['gate_id']==gate['id']),None)
        valid=bool(prior and record and record['decision']=='pass' and record['input_fingerprint']==fingerprint and all(local(root,n).is_file() and evidence_digest(root,n,record.get('evidence_scopes',{}).get(n,'bytes'))==h for n,h in record['evidence_hashes'].items()))
        result.append({'gate_id':gate['id'],'status':'pass' if valid else 'revise' if record and record['decision']=='revise' and prior else 'stale' if record else 'pending','input_fingerprint':fingerprint})
        chain.append(fingerprint);prior=valid
    return result


def next_action(root):
    root=Path(root).resolve();plan=current(root);states=state(root,plan)
    pending=next((x for x in states if x['status']!='pass'),None)
    if pending is None:return {'status':'reviewed-delivery-package','gates':states,'human_approval':'only if separately recorded by a human; not implied','upload_performed':False}
    gate=next(g for g in plan['gates'] if g['id']==pending['gate_id'])
    r,_,_=context(root);needs=needs_for(r)
    dependency=workflow_check(root,anatomical=bool(needs & {'anatomy','mechanism'}) or 'layers' in needs and r['accurate_layers'],generate_narration=gate['id']=='timing' and r['narration']['mode']=='generate')
    return {'status':'work-or-review-required','gate':gate,'gates':states,
            'missing_artifacts':[n for n in gate['required_artifacts'] if not local(root,n).is_file()],
            'conditions':[x['requirement'] for x in plan['conditions'] if x['before_gate']==gate['id']],
            'dependency_notes':dependency['errors'],'rule':'Complete the phase, inspect its evidence and record the actual assessment. Continue independent work when a service is unavailable; do not synthesize a substitute production voice.'}


def review(root, record):
    root=Path(root).resolve();plan=current(root);states=state(root,plan)
    if set(record)!={'gate_id','actor','decision','observations'} or record['actor'] not in ['agent','human'] or record['decision'] not in ['pass','revise']:raise ValueError('Review needs gate_id, actor, decision and observations; actor is a declared reviewer, not an authenticated identity')
    ids=[g['id'] for g in plan['gates']]
    if record['gate_id'] not in ids:raise ValueError('Unknown review gate')
    index=ids.index(record['gate_id']);gate=plan['gates'][index]
    if any(s['status']!='pass' for s in states[:index]):raise ValueError('Review the earlier phase first; its changed inputs invalidate dependent reviews')
    observations=record['observations']
    if not isinstance(observations,list) or {x.get('criterion') for x in observations}!=set(gate['criteria']) or len(observations)!=len(gate['criteria']):raise ValueError('Assess every listed criterion once')
    evidence=set(gate['required_artifacts'])
    for item in observations:
        if set(item)!={'criterion','verdict','note','evidence'} or item['verdict'] not in ['pass','revise'] or not isinstance(item['note'],str) or not item['note'].strip():raise ValueError('Each criterion needs an actual observation, pass/revise verdict and evidence paths')
        if not isinstance(item['evidence'],list) or any(not isinstance(n,str) for n in item['evidence']):raise ValueError('Evidence must be project-relative paths')
        evidence.update(item['evidence'])
    if record['decision']=='pass' and any(x['verdict']!='pass' for x in observations):raise ValueError('Unresolved findings block a pass')
    if record['decision']=='revise' and not any(x['verdict']=='revise' for x in observations):raise ValueError('State which criterion needs revision')
    missing=[n for n in evidence if not local(root,n).is_file() or not local(root,n).stat().st_size]
    if any(Path(n).is_absolute() for n in evidence):raise ValueError('Review evidence must use project-relative paths')
    if missing:raise ValueError(f'Missing review evidence: {sorted(missing)}')
    if record['decision']=='pass':
        r,p,_=context(root);needs=needs_for(r)
        if gate['id']=='content':
            if 'data' in needs and not r['data_source']:raise ValueError('Actual data_source is required')
            if 'route' in needs and r['real_geography'] and not r['geography_source']:raise ValueError('Real geography_source is required')
            if r['narration']['mode']=='provided' and not r['narration']['path']:raise ValueError('Approved recording path is required')
            if r['narration']['mode']=='provided' and not any(s.get('codec_type')=='audio' for s in probe(local(root,r['narration']['path']))['streams']):raise ValueError('Selected recording contains no audio stream')
            if 'script.json' in gate['required_artifacts'] and script_report(read(root/'script.json'),p['fps'])['errors']:raise ValueError('Script contract failed')
        for name in evidence:
            path=local(root,name)
            if path.suffix.lower() in ['.png','.jpg','.jpeg']:
                from PIL import Image
                with Image.open(path) as image:image.verify()
            elif path.suffix.lower() in ['.mp4','.wav','.mp3','.m4a']:probe(path)
            elif path.suffix.lower()=='.json':read(path)
        if gate['id']=='look' and not r['allow_upscale']:
            stream=next(s for s in probe(root/'qa/motion-test.mp4')['streams'] if s['codec_type']=='video')
            if (stream['width'],stream['height'])!=(p['width'],p['height']):raise ValueError('Motion sample must prove native project resolution or explicitly allow upscale')
        if gate['id']=='look':
            from PIL import Image
            for name in gate['required_artifacts']:
                if 'mobile-preview' in name:
                    with Image.open(root/name) as image:
                        if image.width!=360:raise ValueError('Mobile preview must be rendered at 360px width')
        if gate['id']=='timing':
            errors=validate(root)['errors']
            if errors:raise ValueError('; '.join(errors))
            if read(root/'narration.json')['method']!='manual-reviewed':raise ValueError('Review the actual recording/cues and mark measured narration manual-reviewed; unreviewed or synthetic cues are not production approval')
        if gate['id']=='finish':
            qa=read(root/'qa/automated.json')
            if qa.get('video_sha256')!=digest(root/'render/final.mp4') or not (qa.get('status')=='pass' or qa.get('full_decode')=='pass'):raise ValueError('Successful QA must belong to this exact encoded master')
            if 'input_hashes' in qa and qa['input_hashes']!=fingerprints(root,'render'):raise ValueError('Render inputs changed since automated QA; regenerate affected render/QA evidence')
            errors=validate(root)['errors']
            if errors:raise ValueError('; '.join(errors))
            data=probe(root/'render/final.mp4');stream=next(s for s in data['streams'] if s['codec_type']=='video')
            if (stream['width'],stream['height'])!=(p['width'],p['height']) or abs(float(stream['duration'])-p['duration_frames']/p['fps'])>1/p['fps']:raise ValueError('Master dimensions/duration differ from the project')
            from fractions import Fraction
            if abs(float(Fraction(stream['avg_frame_rate']))-p['fps'])>1e-6:raise ValueError('Master frame rate differs from project')
            for variant in plan['formats'][1:]:
                tag=f"{variant['width']}x{variant['height']}";video=root/f'variants/{tag}/render/final.mp4';qa=read(root/f'variants/{tag}/qa/automated.json')
                if qa.get('video_sha256')!=digest(video) or not (qa.get('status')=='pass' or qa.get('full_decode')=='pass'):raise ValueError(f'Variant {tag}: successful QA must match its exact video')
                stream=next(s for s in probe(video)['streams'] if s['codec_type']=='video')
                if (stream['width'],stream['height'])!=(variant['width'],variant['height']) or abs(float(stream['duration'])-variant['duration_frames']/variant['fps'])>1/variant['fps']:raise ValueError(f'Variant {tag}: dimensions/duration mismatch')
                if abs(float(Fraction(stream['avg_frame_rate']))-variant['fps'])>1e-6:raise ValueError(f'Variant {tag}: frame rate mismatch')
    # Brief evidence may legitimately cite the requirements/plan. Track only its
    # declared content intent here so a visual-only replan preserves that review.
    scopes={n:('content-intent' if gate['id']=='content' and str(local(root,n).relative_to(root)) in ['production-requirements.json','production-plan.json','project.json'] else 'bytes') for n in sorted(evidence)}
    hashes={n:evidence_digest(root,n,scopes[n]) for n in sorted(evidence)}
    saved={**record,'input_fingerprint':states[index]['input_fingerprint'],'evidence_hashes':hashes,'evidence_scopes':scopes,'approval_scope':'reviewer assessment; no automatic human approval'}
    path=root/'.studio-director/reviews.json';history=read(path) if path.exists() else [];history.append(saved);write(path,history)
    return next_action(root)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('plan');p.add_argument('project');p.add_argument('--requirements');p.add_argument('--replace',action='store_true')
    p=sub.add_parser('next');p.add_argument('project')
    p=sub.add_parser('review');p.add_argument('project');p.add_argument('--record',required=True)
    args=parser.parse_args()
    try:
        if args.command=='plan':result=plan_project(args.project,read(args.requirements) if args.requirements else None,args.replace)
        elif args.command=='next':result=next_action(args.project)
        else:result=review(args.project,read(args.record))
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except Exception as error:print(f'ERROR: {error}',file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
