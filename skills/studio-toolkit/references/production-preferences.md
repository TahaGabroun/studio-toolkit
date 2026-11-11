# Anatomy and ElevenLabs production workflow

For future productions, use the anatomy skill for anatomical, biological and technical mechanism diagrams and ElevenLabs for newly generated narration. The defaults are in [production-defaults.json](production-defaults.json); `studio.py init` copies them to production-config.json. Project-specific instructions and supplied approved recordings still take precedence. Existing test films are calibration examples, not production voice recommendations.

## Anatomy diagrams and mechanism explainers

Before storyboarding an anatomical, biological or technical mechanism diagram, read the supplied Anatomy skill. The source is bundled at integrations/anatomy/SKILL.md; in the standalone ChatGPT package it is references/integrations/anatomy/guide.md. `studio.py workflow-check PROJECT --anatomical` validates the pinned bundled skill or an explicit diagrams.skill_path, then searches standard skill directories when needed. A configured path may name the skill directory or its SKILL.md. Its use also covers crafted isometric technical cutaways and mechanism diagrams, matching the supplied skill's scope. If it is missing or invalid, resolve that dependency before generating diagrams. Do not substitute generic primitives silently or claim the anatomy skill ran. Continue independent research, writing and voice setup while resolving that dependency.

Use the anatomy skill's actual supported formats and procedures. Preserve recognizable anatomy, compartments, connections and cell morphology. Request editable layers/objects where supported; otherwise use its approved diagram as the visual reference for a faithful layered implementation. Do not claim unsupported export or animation capabilities. Record the actual skill/source revision and asset provenance in design.md and assets.json.

Map each anatomical structure or mechanism part to storyboard.targets and timeline.events.target. Bring anatomical design into the selected HTML/SVG/Canvas or Remotion renderer, with all movement computed from the shared frame clock. Make diagrams lively through explanatory motion: flow along the correct vessel, controlled tissue deformation, progressive construction, cell rolling/adhesion/migration and camera focus on the narrated structure. Use only movements appropriate to the concept; avoid arbitrary pulsing, decorative bouncing or motion that misrepresents biology. Preserve Arabic/English label shaping and scientific caveats about scale and compressed time.

For biological work, read the supplied biological-figures guide: its legacy animal-cell geometry is explicitly not a production template. Preserve the kit and build subject-specific organic structures. For video, adapt the scene in a project workspace to a pure pose-at-time function and a window.seek(seconds) wrapper (HTML), or derive the same pose from Remotion frames. These are project adapters to implement, not invented Anatomy APIs. Preview clocks and user input must not independently advance the render state.

Inspect an anatomy style frame before full animation, then cue boundaries and representative final encoded frames. Verify that the visible object actually matches the narration. Structural schema checks cannot approve anatomy.

## ElevenLabs narration

Prefer a confirmed connected ElevenLabs tool when available. Otherwise use [scripts/elevenlabs_narration.py](../scripts/elevenlabs_narration.py) with ELEVENLABS_API_KEY in the environment and an approved voice ID in production-config.json, ELEVENLABS_VOICE_ID or --voice-id. Never request or record a plaintext API key in project files or chat. If connection/voice is missing, stop the voice-generation stage and report the setup requirement; do not fall back to eSpeak, system voices or test tones for production.

The helper uses a continuous approved script and the [ElevenLabs speech-with-timing endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps). It defaults to the documented Multilingual v2 model and MP3 format; voice selection remains explicit. It does not perform voice cloning. For long scripts exceeding the model limit, prepare chapter-sized requests with continuity context and derive final offsets from measured audio after assembly.

```bash
python scripts/studio.py workflow-check PROJECT --generate-narration
python skills/studio-toolkit/scripts/elevenlabs_narration.py PROJECT --voice-id VOICE_ID --dry-run
python skills/studio-toolkit/scripts/elevenlabs_narration.py PROJECT --voice-id VOICE_ID
```

Generated candidates live under assets/elevenlabs/REQUEST_HASH/CANDIDATE_HASH: narration.mp3, segments.json, words.json and generation.json. Scene cue IDs equal script scene IDs. The helper caches completed provider responses in .studio-cache/elevenlabs before timing review, verifies hashes, and reuses them for the same text/voice/model/output format. Changed inputs create a different request; no automatic billable retries occur. If a request times out, inspect provider history before retrying. Keep this cache private and outside public distributions. Provider usage rights come from the account; do not label generated audio CC0 automatically.

Original-text character timings are grouped into scene and word cues. A normalized-only response may be used only if its text still exactly matches the approved script. Changed number/term normalization, absent timings, nonfinite timestamps or overlapping scene cues require review; no equally spaced or guessed alignment is substituted. The generated method is provider-unreviewed, not ASR and not forced alignment of a natural recording.

After listening and checking pronunciation, derive project duration and scene boundaries from the actual audio. Update timeline event cue IDs to match the returned scene IDs, register the cleared audio in assets.json, and import the candidate:

```bash
python scripts/studio.py align PROJECT --audio assets/elevenlabs/REQUEST_HASH/CANDIDATE_HASH/narration.mp3 --segments PROJECT/assets/elevenlabs/REQUEST_HASH/CANDIDATE_HASH/segments.json --method provider-unreviewed
```

The generation helper does not overwrite approved narration.json, captions or timeline. After actual review, use manual-reviewed on import. Preserve word timestamps for phrase-level captions and concept focus, especially mixed Arabic/English scientific terminology. Mix and render only after these artifacts agree. Changing production-config.json invalidates storyboard and downstream checkpoints while retaining approved research and scripts for revalidation/reuse.

An explicit --import-response corrected.json supersedes a failed cached response while retaining the old response in cache history. Renamed scene IDs create a new cue candidate while reusing the same paid speech response. The candidate hash includes the scene mapping and provider response; edited candidates are preserved instead of overwritten.

When a director plan exists, the speech helper checks that new generation is actually requested and that the content review is current before buying or importing speech. It preserves supplied-recording/no-voice direction. Dry-run remains a planning-only request inspection.
