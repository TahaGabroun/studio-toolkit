---
name: studio-toolkit
description: Coordinate end-to-end video and editorial productions across research, YouTube strategy, scripts, storyboards, narration-driven animation, audio, rendering, QA and publication packages. Use when the request spans multiple studio stages.
---

# Studio Toolkit

Read [pipeline contracts](references/pipeline.md) before creating production artifacts and [quality standards](references/quality.md) before visual work. Use [scripts/studio.py](scripts/studio.py) for initialization, validation, stage records and measured narration import. [scripts/media.py](scripts/media.py) mixes audio, creates test pulses, muxes and validates media. Resolve paths from this skill's actual directory.

For future animated anatomical, biological or technical mechanism diagrams, use the anatomy skill to design the biological structures, then animate its approved assets in the selected renderer. For new production narration, use ElevenLabs. Read [production preferences](references/production-preferences.md) for discovery, credentials/voice setup, measured timing and cache reuse. Missing anatomy skill or ElevenLabs access is a dependency to resolve, not permission to silently substitute generic diagrams or test voices. Existing approved recordings and explicit user overrides take precedence.

## Route the request

| Intent | Specialist | Handoff |
|---|---|---|
| Video idea, research, hook, packaging, chapters, retention, cuts | youtube-agent | brief, research, packaging / edit decisions |
| Channel audit, audience, competitors, SEO, thumbnail, calendar | youtube-strategy | strategy, evidence and prioritized backlog |
| Long-form spoken narrative | youtube-script-writer | script.md + script.json |
| Voice, editorial workflow, assets, repurposing | content-os | editorial plan, assets.json, derivatives |
| Composition, pacing, easing, sound direction | claude-motion-adapted | design.md, timeline effects and sound cues |
| Browser/SVG/simulation rendering | motion-design | deterministic seek(t) source + master |
| Full React video and compositing | remotion-video | composition + rendered master |
| Reusable diagrams, typography, camera, editorial/terminal inserts | remotion-motion-graphics | composition / insert + evidence |
| Character-led 3D cartoon explainers | cartoon-animation | poseable characters, authored shots and measured captions |
| Expressive 2D stick-figure explainers | stick-figure | Canvas rigs, environments, camera and sound cues |
| Quiet black/white line motifs | minimalistic-graphics | short JSON-driven insert |
| Supplied numeric data animation | animated-graph | data-faithful graph and counter |
| Illustrative 3D journey | map-route | schematic city/route; no navigation claim |
| Layered device teardown | exploded-view | labelled generic phone or authored geometry |
| Anatomical, biological and technical mechanism diagrams | anatomy (supplied integration) → selected motion specialist | approved anatomical layers, semantic target IDs and provenance |

Read the selected sibling's SKILL.md before specialist work. In the standalone package the same content is under `references/specialists/<name>.md`. [aliases](references/aliases.md) maps the archive identifiers; aliases route here and do not install duplicate skills. For these six adopted animation workflows, read [animation runtime and timing handoff](references/animation-workflows.md). In the single-skill ChatGPT bundle choose the same specialist reference by intent. Use only relevant specialists, in story order. Apply their procedures yourself; delegation is optional and depends on the host and user's scope.

## Execute a production

Infer brief, audience, locale, deliverable, aspect ratio, target duration, existing narration and asset rights from the request. Ask only for essential missing inputs. Default to landscape, 30 fps, English; prerecorded narration fixes the spoken content unless changes are authorized.

1. Run `python3 <this-skill>/scripts/studio.py init PROJECT --title "Title" --format landscape --duration 60` for a new project. Existing projects: validate and inspect `status` first.
2. Develop idea → research → strategy → script → storyboard → design → assets → animation. For structured explanatory diagrams, read the anatomy skill before visual planning and preserve its diagram quality in the animated implementation. Each output follows [schemas](references/schemas/project.schema.json); load the relevant schema rather than every file. Mark a stage complete only when its files are real and inspected.
3. Generate new narration through ElevenLabs with provider timings, preserving completed responses instead of paying for unchanged speech again. Import its cues with `--method provider-unreviewed` until checked. For supplied recordings use `align PROJECT --audio assets/narration.wav --segments segments.json --method manual-reviewed`. MP3/M4A also work through FFmpeg. Preserve raw ASR output as `asr-unreviewed`; reuse approved script and asset hashes.
4. Connect cue IDs to exact visible target IDs. Use progressive construction, focus, annotations or tracking. Build captions and audio placement from the same timeline. Do not invent equally spaced word timings.
5. Run audio mixing, rendering, full-media decode and QA. Inspect representative frames and listen to the final audio. Automated pass, agent inspection and human approval are separate states.
6. Prepare titles, description, thumbnail brief, captions, sources and licensing notes in publication.md. Account publication requires user authorization; prior explicit authorization remains valid. Preparing a publication package never implies that an upload occurred.

## Completion and recovery

`studio.py complete PROJECT STAGE` checkpoints hashes. `status` detects changed/missing upstream bytes. Fix the first stale artifact, revalidate, and refresh checkpoints; do not rerun expensive models merely to renew hashes. A file's presence alone does not prove quality. Do not assert that an unavailable model/service, render or upload ran.

Deliver existing output paths, measured format/runtime, source/rights notes, test results and material limitations. If the host cannot execute code, deliver the production artifacts and explicit unverified commands. Codex filesystem installation does not install the package in ChatGPT; see the distribution documentation supplied with the repository.
