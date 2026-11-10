---
name: cartoon-animation
description: Create procedural 3D cartoon explainers with poseable characters, props, cinematic shots and narration-timed captions. Use for character-led 3D animated shorts.
---

# 3D cartoon animation

Read the shared [animation workflow](../studio-toolkit/references/animation-workflows.md) and [engine controls](references/engine.md) before production. Resolve STUDIO to the actual studio-toolkit sibling skill, or the extracted package root.

1. Take a brief or approved script, audience, duration, locale and narration. For a full production use studio-toolkit for research, script, storyboard and asset provenance. Use Anatomy for crafted anatomical/mechanism diagrams within the cartoon story.
2. Run `python3 "$STUDIO/scripts/animation.py" init cartoon-animation PROJECT/animation` into a new directory. The default is a silent four-second visual calibration; it is not a finished narrated explainer. --example preserves the inherited worked example source without a voice. Rewrite its topic-specific shots and check claims.
3. Use the cached ElevenLabs helper for new production speech or an approved recording. Import actual measured word cues with animation.py sync; label provider/ASR review state. Retiming, captions and SFX share those cues. Do not generate a substitute voice or guess word timing.
4. Write expressive, purposeful shots using the retained rigs, props, environments and camera helpers. Pose updates depend only on time, including when seeking backwards. Let the mechanism determine motion and transitions; protect caption/face safe areas.
5. Use animation.py render --snap at the opening, transitions, important action and ending. Inspect frames before a full render. Render the full authored edit, listen to its mix and review labels/captions; no narration truncation or failed-browser success claims.

Inputs: script, measured audio/word cues, authored shot code and any approved assets. Outputs: editable project, timing.json and renderer cue data, snapshots, MP4 and media/determinism QA. Defaults: vertical/30 fps; resolution and sound limitations differ by engine and are explicit in the shared workflow. Resume from approved code/cached speech; --replace is an explicit replacement of generated timing/media. Human creative/scientific approval is distinct from automated checks.

This is a native ChatGPT/Codex workflow. Use available shell/browser tools, not Claude commands or subagents. A ChatGPT host without execution dependencies can produce source and instructions but must mark rendering unverified.
