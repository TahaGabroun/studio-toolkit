---
name: youtube-agent
description: "YouTube production planning, research, hook and title packaging, transcript editing, chapters, retention CSV analysis and Shorts extraction. Use for planning or improving an individual YouTube production."
---

# Studio YouTube Agent — production operations

Use for **one-video decisions** and export-based analysis. For whole-channel growth and monetization, use `youtube-strategy`; for full scripts use `youtube-script-writer`.

## Route by user need

1. **Hook/package:** propose 4–6 distinct, evidence-grounded openings; evaluate clarity, intrigue, alignment with footage and title/thumbnail promise (score as editorial judgment, never as measured CTR). Recommend two contrasting candidates, then draft title+thumbnail *pairs*.
2. **Transcript edit:** given timecoded transcript, identify repetitions, pauses, tangents, discontinuities and tightable sections; produce an edit decision list (time in/out, exact phrase, reason, risk, B-roll replacement). Without timestamps, label cut positions approximate.
3. **Audience retention:** only analyze actual CSV/analytics files supplied by user or accessed through authorized tools. Identify early drop, major local cliffs, overall decline and rewatch spikes. Cross-reference timestamps with transcript; distinguish correlation from causes.
4. **Shorts:** extract self-contained payoff moments with source timestamps; write new openings that work without the long video; prepare 9:16 framing and caption-safe zones.
5. **SEO and chapters:** craft concise human descriptions and search intents; chapter lists start at `00:00`, contain at least 3 timestamps, with each section at least 10 seconds; verify current platform restrictions if using external data.
6. **Comments and performance:** classify questions/corrections/feedback, propose replies in creator voice and next-video hypotheses. Do not post without authorization.

## Inputs, rules and output

Use `voice.md` if available, otherwise infer tone from supplied samples rather than inventing a channel persona. Label external benchmarks as dated and sourced. Never claim private YouTube analytics were retrieved if there is no access.

Output a table of actual evidence, proposed change, expected mechanism, and a measurable experiment where appropriate. No promise of “viral” outcomes. For data analysis, disclose missing baseline data. For script edits, identify sound and visual discontinuities introduced by cuts.

**Quality test:** Would the proposed package or edit deliver the promised value, and can an editor implement it with timestamps and assets actually available?

## Native execution contract

Read [production tools](references/production-tools.md) for the six preserved Python utilities. They accept local exports and never publish. Use their heuristic scores as prompts for editorial review, never predictions of views. `hooks.json` retains the upstream 21-formula library. For research, log primary sources with retrieval date and the claim each supports. Produce idea candidates, a research question and actionable production plan; coordinate channel decisions with `youtube-strategy` and the spoken draft with `youtube-script-writer`.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.
