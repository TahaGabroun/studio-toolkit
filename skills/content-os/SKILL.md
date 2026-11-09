---
name: content-os
description: "Manage source-first editorial planning, creator voice, corpus indexing, assets, production state and cross-platform repurposing. Use for content calendars, editorial workflows or adapting existing material."
---

# Studio Content OS — source-first editorial system

**Transform actual material; do not invent an identity, experience or viewpoint for the creator.** Adapt the 4S loop: Source → Substance → Structure → Style.

## Procedure

1. **Source:** catalogue user notes, recordings, uploads, citations, URLs and direct quotations. Ask which are confidential, copyrighted or not to be quoted. Verify when possible, otherwise mark unverified.
2. **Substance:** extract a central argument, strongest observation, counterpoint and intended consequence. Separate what the author claims from what an external source proves. Preserve uncertainty and nuance.
3. **Structure:** choose a format-native argument rather than paste the long-form script into every platform. For a YouTube essay: compelling lead, argument development, counterargument, payoff. For a social caption: tension, concrete insight, link/call to view. For a newsletter: context, useful takeaways and credible sources.
4. **Style:** build a small `voice.md` from real writing/recording: cadence, sentence length, favored transitions, dialect/register, terms to retain, terms to avoid. If samples are few, state low confidence and ask for corrections only when essential.
5. **Transform:** produce variants with different platform needs while holding facts and voice constant. Label excerpts and links to source segments (timestamps/pages) so editors can audit.
6. **Polish:** remove generic AI filler, slogan-like claims, repetition, excessive adjectives and awkward synthetic Arabic. Keep humor or sarcasm only where the source material authorizes it.
7. **Approval:** sensitive quotes, claims about identifiable persons, controversial allegations and paid endorsements require precise sourcing and review.

## Common output set

A master narrative, a 30–60-second short adaptation, one community post, two distinct social captions, a newsletter teaser and a provenance checklist. Only create the deliverables asked for; do not force the whole set on a simple request.

Respect licenses when processing third-party transcripts. Do not reproduce long copyrighted text or disguise uncredited copying as original writing.

## Native execution contract

Read [editorial operations](references/editorial-operations.md). Inputs: licensed source notes/transcripts, voice examples, audience and channel constraints. Outputs: asset ledger, editorial calendar, production checkpoints and platform-specific derivatives with source anchors. Local corpus chunking and image optimization are preserved executable helpers. Optional insight extraction uses local Ollama, with checkpoints and no Anthropic API. Preserve original meaning and distinguish quotation from paraphrase. Hand YouTube script work to `youtube-script-writer`, rendering to the selected video engine.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.
