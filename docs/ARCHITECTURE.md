# Artifact and orchestration architecture

The orchestrator selects only relevant specialists. Skills supply editorial and production judgment; deterministic Python utilities validate contracts and media. No daemon, model API, scheduler or hidden agent runtime is needed.

New projects persist production-config.json with anatomy-skill routing for anatomical scenes and ElevenLabs for newly generated narration. The supplied Anatomy skill is read before visual planning; its outputs retain semantic target IDs through the chosen renderer. ElevenLabs output supplies the scene/word timing candidates and audio provenance. Missing skill/access is reported instead of silently substituting generic diagrams or test voices. Preferences participate in storyboard and downstream hashes while research and writing remain reusable.

IDEA → RESEARCH → CONTENT STRATEGY → SCRIPT → STORYBOARD → VISUAL DESIGN → ASSET GENERATION/ACQUISITION → ANIMATION → NARRATION SYNCHRONIZATION → AUDIO MIXING → VIDEO RENDERING → QUALITY ASSURANCE → PUBLICATION PACKAGE.

The schema files in schemas/ and the self-contained orchestrator references describe project, script, storyboard, assets, timeline, narration, mix and render configuration. Scene IDs link script/storyboard/timeline. A visual target ID in a storyboard is referenced by an event; its cue_id resolves to actual narration timestamps. A renderer must implement those target IDs. Schema consistency alone cannot prove the renderer highlights the correct anatomical object.

project.json owns dimensions, FPS, duration_frames, language/direction and renderer choice. All scene and event intervals are half-open integer frames. Import seconds once with nearest-frame half-up rounding. Phrase/word measurements stay in narration.json with audio hash and method; SRT is generated directly from those timestamps. Do not resample captions through a separate duration estimate.

state.json contains stage completion hashes. status recomputes declared outputs/upstream inputs; a changed or missing artifact marks that stage and descendants stale. Revalidation can renew checkpoints without invoking a model. Audio/assets participate once relevant. The demos renderer separately hashes its entire source tree, JSON inputs, final mix and dependency lock, preventing source changes from reusing a stale render. Stage checkpoints carry no implication of human approval.

Default formats: 1920×1080 landscape, 1080×1920 vertical, 1080×1080 square, optional 3840×2160. Default 30 fps. HTML and Remotion are alternative engines; avoid mixing their clocks. Professional quality comes from exact semantic referents, reading holds, source fidelity and review, not a requirement to animate every pixel.
