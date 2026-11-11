# Production director: choose the workflow before the tools

Use this for a complete video, substantial edit or meaningful insert. For a tiny change, keep the existing treatment and revise only affected work. The objective is viewer understanding and a coherent, finished film; using more skills or effects is not a quality goal.

## Interpret the brief

Read the idea and existing project before choosing tools. Establish the audience, desired understanding/emotion, factual claims, platform/aspect ratio, duration, narration already supplied, visual style, available assets and material constraints. Infer reasonable choices from context and record assumptions; ask only for missing information that would materially change production. A patient explainer and a medical-student lecture need different density and terminology even when they cover the same topic.

Use semantic judgment to write production-requirements.json against [its schema](schemas/production-requirements.schema.json). The deterministic helper validates these interpreted requirements; it does not understand arbitrary prose or creatively direct a video by keyword matching. Required fields are schema_version, idea, audience, goal, scope (full-video/insert/edit), style (auto/documentary/scientific/3d-cartoon/stick-figure/minimal), needs and narration.mode. Scene-level needs can differ. Useful additional fields include renderer, data_source, real_geography, geography_source, accurate_layers, allow_upscale, additional_formats, channel_strategy and assumptions.

Needs: anatomy, mechanism, data, route, layers, characters, footage, screen, typography, raster-assets. Do not activate a specialist just because a word appears in the topic. Choose it because its output solves a scene's communication problem. New speech uses ElevenLabs; an approved supplied recording fixes the spoken content unless changes are authorized. Silent inserts require no substitute voice. Their timeline can contain authored integer-frame events without cue_id only when narration.mode is explicitly none; narrated projects still require actual measured cue IDs.

```bash
python scripts/studio.py plan PROJECT --requirements requirements.json
python scripts/studio.py next PROJECT
# Replan explicitly after inspecting changed requirements:
python scripts/studio.py plan PROJECT --replace
```

The helper creates production-requirements.json, production-plan.json and a readable production-plan.md. It never generates speech/assets, renders, installs tools or publishes. It preserves existing work; a differing existing plan needs --replace. Requirements and plans validate through studio.py validate. Existing projects without these optional artifacts remain compatible.

## Select a visual language and a main renderer

Choose the dominant treatment from the audience and idea. Keep one palette, type system, scale conventions, camera language, caption system and motion grammar. A hybrid can combine several visual methods while preserving those choices. Pick one main renderer and use specialist outputs as authored components or inserts on its shared timeline. Do not concatenate unrelated default templates and call the result a visual identity.

| Communication need | Useful skills | Selection boundary |
|---|---|---|
| Evidence-led documentary or editorial film | youtube-agent, youtube-script-writer, content-os, remotion-video | Footage/compositing and varied inserts favor one Remotion timeline. Channel audits are optional, only when relevant. |
| Scientific structures and causal mechanisms | anatomy → motion-design or remotion-video | Anatomy supplies crafted subject-specific structure. The renderer animates the narrated semantic target; scientific review is separate. |
| Expressive 3D character-led explanation | cartoon-animation + motion director | Reuse the procedural rig/props; author the actual shots. Supplied direct capture is vertical 720×1280 with upscale. Native 1080/4K or other layouts require a custom proven adaptation. |
| 2D character-led explanation | stick-figure + motion director | Native vertical 1080 layout; adapt composition and caption bands for other formats. Expressions/poses should communicate the beat. |
| Numeric comparison or change | animated-graph or remotion-motion-graphics | Real data and units first. The graph template is a short vertical insert; long or differently shaped scenes need authored layout. |
| Journey or location | map-route for schematic scenery; authored map in the main renderer for real geography | Never use the seeded city to assert real streets, routes or live ETA. Source actual geography when accuracy matters. |
| Layered object or cutaway | anatomy for accurate structure, exploded-view for a generic phone or authored layers | Changing six labels does not turn a generic phone into measured CAD or another anatomical structure. |
| Quiet symbolic insert | minimalistic-graphics | The steps motif is useful when it explains progress. A long film needs meaningful visual development rather than a loop. |
| Photographic or painterly material | existing licensed assets; imagegen when available and actually useful | Reuse cleared assets. Use code/SVG/Anatomy for editable precise diagrams; don't turn every scene into a generated bitmap. |

The plan chooses only relevant routes and explains the selection. Explicit user/project renderer preferences win. Native output is the default; upscale permission is explicit. Multiple aspect ratios get separate style/mobile evidence and separate encoded masters/QA under variants/WIDTHxHEIGHT. They reuse the measured audio clock, not a destructive center crop.

Rough beats and thumbnail sketches can precede speech. Lock exact scene partitions, reveals, labels, camera events, captions and sound cues to the measured take. In storyboard.json each scene must answer: what is narrated, what exact subject is visible, how the change clarifies the narration, and what the viewer should notice. Preserve semantic IDs into timeline.json and the renderer.

## Execute the gates in order

1. **Content:** research/evidence, audience promise and narrative or insert purpose. For factual work inspect claims/data/geometry references. For a supplied voice, audit/transcribe that take before rewriting any words. Resolve major factual or structural problems before production speech.
2. **Look:** art direction, one representative style frame, a mobile preview and a short motion study of the hardest scene. Use a clearly silent visual proof where speech is not ready; do not substitute a test voice for production narration. Inspect the actual structures, typography, palette, hierarchy, easing and native output feasibility. An entire four-second insert can be its motion study; reuse it if it passes.
3. **Timing** (narrated work): generate/reuse ElevenLabs after content review, or align the supplied recording. Review pronunciation and real cues, mark narration manual-reviewed, then author the timed storyboard and a low-cost animatic. Inspect causal referents, captions, focus switches, reading holds and transitions before building the complete animation. No fabricated evenly spaced word timing.
4. **Finish:** final assets/animation, sound mix and encoded master. Run media QA; inspect final encoded frames at full and mobile size and listen to the full audio. A technically valid file with illegible labels or a misleading diagram still needs revision. Check every additional format.
5. **Delivery:** complete publication package, masters, captions where applicable, source/rights notes and a candid QA summary. Account upload is a separate authorized action, and existing authorization remains valid.

These are production-quality reviews the agent performs. They do not introduce a new requirement to ask the user for permission at each stage. Seek human input when the user requests a review, subjective direction is genuinely unresolved, or an action needs authorization that has not already been given. Never represent an agent assessment as human approval.

## Record real review evidence and revise selectively

A review record assesses every listed criterion once. Use actual observations and project-relative evidence paths. A pass requires all criteria to pass, required artifacts to exist, valid media/images/JSON and any relevant structural checks. A revise decision identifies what failed. The helper records hashes and history in .studio-director/reviews.json; it cannot judge anatomy, taste, intelligibility or truth from file presence. A record is a declared review, not an authenticated reviewer identity or a numerical professional-quality score.

```json
{
  "gate_id": "content",
  "actor": "agent",
  "decision": "revise",
  "observations": [
    {"criterion": "brief-fit", "verdict": "pass", "note": "The promised outcome matches the stated audience question.", "evidence": ["brief.md"]},
    {"criterion": "truth-and-source-fidelity", "verdict": "revise", "note": "The second numeric claim lacks its supplied dataset; obtain and cite it before charting.", "evidence": ["research.md"]},
    {"criterion": "narrative-or-insert-purpose", "verdict": "pass", "note": "The comparison is needed to answer the hook rather than serving as decorative motion.", "evidence": ["script.md"]}
  ]
}
```

```bash
python scripts/studio.py review PROJECT --record actual-review.json
python scripts/studio.py next PROJECT
```

Do not copy the example observations into a pass. Inspect the actual project. Use actor human only for a review actually supplied by a human, not because an agent completed it. Fix the identified root cause, regenerate affected previews/QA and review again. Never overwrite an approved script merely to make a changed animation fit. A missing service blocks its dependent action; continue independent writing/design and report the concrete recovery step.

next reports the earliest pending/stale/revise phase, its tools, required evidence and dependency notes. Brief evidence citing requirements, plan or project metadata tracks its content-intent fields, language and actual runtime; style/routing changes alone do not falsify that content review. Other evidence tracks exact bytes. Changed script/data invalidate content and downstream reviews; a visual-only replan can retain the unchanged content review. Changed review evidence invalidates its review. The plan detects changed inputs and requires an explicit replan rather than silently applying stale direction. Cached narration stays reusable when its request is unchanged. This is review/resume guidance, not an unattended job scheduler.

The older studio.py complete/status commands retain artifact checkpoint compatibility. Their file-checkpoint order is not the creative execution order: produce measured narration/timed planning before final animation, then checkpoint validated artifacts when prerequisites exist. New end-to-end productions follow director next as well as artifact validation. No gate automatically invokes a model or declares a finished film professional.

## Non-negotiable visual review questions

- Does the visual show the actual narrated object/action, with correct relationships and clearly stated schematic scale/time?
- Can a viewer identify the focal subject and read required labels on a 360px preview without pausing?
- Does motion clarify a change, transfer attention or establish continuity? Can decorative shake/glow/cuts be removed?
- Do compositions feel intentionally related across scenes, with good spacing, contrast and restrained transitions?
- Do timing and breathing room support comprehension rather than maximizing cuts or word density?
- Is speech intelligible, pronunciation correct, the mix consistent and the encoded master free from clipping/cutoffs?
- Are all formats, rights, source claims and automated/agent/human review states represented honestly?
