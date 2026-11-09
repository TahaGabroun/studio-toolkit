---
name: remotion-video
description: "Build and edit full React/Remotion videos with compositing, footage, narration, captions, programmatic rendering and frame inspection. Use for complete Remotion productions or changes to existing ones."
---

# Studio Remotion Editor — full-video edit

Remotion is a programmable React/TypeScript renderer. Use it when the user wants a **complete edited video** with narration/footage/graphics or modifications to an existing Remotion project. For modular overlays and transparent graphics, involve `remotion-motion-graphics`.

## Workflow

1. Inspect project files, existing compositions, actual media, recorded narration and any transcript with word timings. Preserve source project and do not overwrite user media without permission.
2. Pin `fps`, frame size, duration and composition ID; make one timeline source of truth. Convert seconds to frame numbers at the composition boundary, not ad hoc inside each component.
3. Build scene components driven by `useCurrentFrame()` and `useVideoConfig()`. Animate deterministically with `spring()`/`interpolate()` and clamped extrapolation where needed. Do not use CSS timing or non-seeded random visual behavior during frame render.
4. Mount footage and stills using supported Remotion primitives and `staticFile()`. Use a content-aware crop, actual rights-cleared imagery, conservative color corrections and readable overlay hierarchy.
5. Align every visual emphasis and caption to *concurrent* narration. For uploaded audio, derive word timing from alignment/transcript data if available; do not claim forced alignment was done if it wasn't. Keep technical labels visible as the corresponding phrase is spoken.
6. Add sound cautiously: speech-first gain staging, music ducking, limited SFX and no clipped voice. Do not use copyrighted tracks without appropriate rights.
7. Typecheck, render, inspect frame samples at scene seams/important narration moments, read captions at 360px width, check Arabic shaping and audit exact runtime with ffprobe.

Example commands (adapt to actual project entry and composition ID):



## QA disposition

Deliver only what actually exists. In the report, include video dimensions, duration, what was visually inspected, source rights/unknowns, and outstanding rendering limitations. When asked for *interactive* material rather than video, keep a web deliverable instead of collapsing it to MP4.

## Native execution contract

Read [Remotion production](references/remotion-production.md), then consult [component patterns](references/motion-patterns.md) only for needed effects. The preserved upstream [theme](assets/theme.ts) is a starting point; adapt its decorative effects to the narrative. Inputs: project, storyboard, assets and shared timeline. Outputs: React source, composition metadata, master, captions and QA. Validate source with TypeScript and final media with the orchestrator. `remotion-motion-graphics` provides reusable inserts; `claude-motion-adapted` reviews motion language.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.

## Production providers

For anatomical, biological or physical mechanism diagrams, use the actual anatomy skill before implementing the animation; preserve its recognizable structures and semantic layers. Newly generated production narration uses ElevenLabs with a selected voice and measured provider cues. Read [production preferences](../studio-toolkit/references/production-preferences.md). Report missing anatomy/voice access instead of substituting generic diagrams or a local test voice. Preserve supplied approved recordings and explicit user overrides.
