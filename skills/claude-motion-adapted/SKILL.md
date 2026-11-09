---
name: claude-motion-adapted
description: "Direct advanced motion design with purposeful timing, composition, easing, transitions, camera and procedural sound. Use to design or critique the motion language shared by HTML and Remotion films."
---

# Studio Motion Director — visual language and timing

Use for **motion design decisions independent of engine**. Pair with `motion-design` or `remotion-video` to build; do not confuse an animated concept with a rendered file.

## Direction method

1. Define story mechanism: *what changes* and *why the visual movement helps viewers understand it*. Choose the central metaphor before effects.
2. Build a beat map of scene starts/ends, emphasized words, music accents and causal graphic events, all in seconds and referenced through `timeline.json`. Use audio beat positions only if measured from audio, not guessed.
3. Create a stable visual system: background, focal subject, supporting information, typography, neutral/semantic accent, safe margins and scale. For bilingual content, test real Arabic font coverage and number glyph choices.
4. Animate with semantic motion: position/scale/opacity and camera progress linked to the event being narrated; stagger where it clarifies sequence. Use easing or springs for starts/stops; linear is valid for uniform continuous rotation, scrolling or time-driven scientific simulation.
5. Keep readable holds: a full thought should remain legible for enough time at phone size; reduce motion rather than flash text faster. Keep focal point count low and avoid gratuitous zoom, glow or busy background.
6. Design transitions through persisted objects (e.g., a diagram node becomes the next section) or motivated camera movement, not unrelated effects. Avoid flash frames and mismatched exit/entry velocities.
7. Sound: narration is reference, background music ducks under it, SFX communicate transitions instead of competing with speech. Ensure every cue's source/license is recorded.
8. QA: review first frame, mid-beat and end frame of each scene, transition seams, caption entry timing, label alignment, readability and audio sync. If a visual cannot be interpreted without hearing it, decide whether that's intentional.

## Output

Provide a **style frame brief**, a per-scene camera/choreography table, shared color/type tokens, timestamped sound cues, and measurable checks for the chosen renderer. For a ready-to-render project, keep timing constants in shared data rather than scattered code.

## Native execution contract

Read [motion and sound](references/motion-and-sound.md). Inputs: storyboard, narration cues, brand system and output format. Outputs: design.md, annotated timeline target/effect choices, style frames and sound cue sheet. The retained `scripts/sfx` engine synthesizes deterministic licensed-original sounds with no downloads or API. Direct rendering to `motion-design` or `remotion-video`; review specialist graphics with `remotion-motion-graphics`. The historical name is retained only as an upstream identifier; there is no Claude runtime dependency.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.

## Production providers

For anatomical, biological or physical mechanism diagrams, use the actual anatomy skill before implementing the animation; preserve its recognizable structures and semantic layers. Newly generated production narration uses ElevenLabs with a selected voice and measured provider cues. Read [production preferences](../studio-toolkit/references/production-preferences.md). Report missing anatomy/voice access instead of substituting generic diagrams or a local test voice. Preserve supplied approved recordings and explicit user overrides.
