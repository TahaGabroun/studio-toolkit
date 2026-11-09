---
name: youtube-script-writer
description: "Write or revise long-form YouTube narration with truthful hooks, story causality, retention beats, source-linked claims, visual directions and runtime estimates. Use when the deliverable is a spoken script."
---

# Studio YouTube Script — narrative production

Write for **speech and picture together**, not a blog post with “add B-roll” appended. For short platform-specific hooks and SEO packaging, coordinate with `youtube-agent`.

## Build sequence

1. Define the **promise**: the specific question answered or capability gained. Record format (documentary, scientific explainer, tutorial, essay, interview), viewer baseline, target runtime, title/thumbnail expectations and spoken language/dialect.
2. Build a **claim ledger** before writing: each assertion → source/link or user-provided material → support strength → what remains speculation. Use verified numbers only; insert `[VERIFY]` for unavailable evidence. Distinguish explanatory model from observed result.
3. Propose 3–5 different hooks: concrete image, anomaly, paradox, stakes or reverse expectation. Choose based on truth and storytelling fitness, not fabricated “hook scores.” Confirm the premise within the opening segment; avoid long intros and premature CTAs.
4. Draft **beats**: each beat has a question, explanatory development, concrete illustration/evidence, transition and new curiosity. Every meaningful spoken passage receives a concurrent `[VISUAL @ mm:ss: ...]` cue with location/focus target; specify whether it is a shot, illustration, source quote, data graphic, simulation or B-roll.
5. Budget duration using verified narrator pace if provided, otherwise a clearly labeled *estimate* based on ~130–160 spoken English words/minute. Arabic pacing must be estimated from narration or calibration, not blindly converted from English counts.
6. End with a demonstrated payoff that genuinely answers the opening promise. One optional, relevant call to action, not a repetitive list of engagement requests.
7. Run two edits: **substantive edit** (logic, accurate nuance, source quality, mechanism) and **performance edit** (short utterances, rhythm, natural transitions, pronunciation, read-aloud).

## Visual synchronization contract

For a video that follows an existing recorded narration, **do not rewrite the actual narration without approval**. Derive scene boundaries from audio or subtitle timestamps. Annotate each paragraph with scene ID and a visible referent. For a diagram, identify the exact structure or layer highlighted; soften surrounding material instead of covering it with arbitrary glowing outlines. Caption events should follow spoken words, not arrive prematurely.

For mixed Arabic + scientific terms, preserve recognized technical terminology, verify correct Arabic orthography, use RTL-aware captions and avoid broken bidi sequences.

## Deliver

A production-ready script with a timed beat sheet, exact spoken lines, `[ON SCREEN]` cues, source/claim ledger, expected runtime (estimated vs audio-measured) and notes for edit/caption/sound. The script must stand on its own without a separate narration the editor cannot locate.

## Native execution contract

Read [narrative craft](references/narrative-craft.md). Inputs: brief, audience baseline, claim ledger, narrator voice and target runtime or fixed narration. Outputs: script.md plus structured script.json with hook, development and payoff scenes, narration, visual instructions and source IDs. Check using the orchestrator's `studio.py script-check`. A formula or score cannot substitute for a read-aloud and factual edit. Pass target IDs to storyboarding and measured narration to `remotion-video` or `motion-design`.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.
