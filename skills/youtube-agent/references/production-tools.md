# Production tools

Run these relative to this skill directory; all are Python stdlib and accept local data:

```bash
python3 scripts/yt-script/hookscore.py --hook "Why does a tree get heavier without eating soil?" --json
python3 scripts/yt-package/title.py --title "Where a tree gets its mass" --thumb "FROM THE AIR" --json
python3 scripts/yt-edit/deadair.py transcript.srt
python3 scripts/yt-chapters/chapters.py transcript.srt --target 5 --json
python3 scripts/yt-retention/retention.py retention.csv
python3 scripts/yt-viral/swipe.py collected.json --min 2 --json
```

Hook formulas, title checking, fillers and vocabulary metrics are English heuristics. For Arabic, use editorial judgment; never treat English scores as multilingual performance measures. Retention slope is descriptive. A CSV cannot tell why viewers left without transcript/traffic context. Outliers require at least four collected videos per channel; median-normalization cannot control age/topic/distribution differences.

For ideation, develop several mechanisms: anomaly, conflict, visual transformation, surprising verified fact, practical goal. Pair the title with a thumbnail that adds information. Chapters are a draft requiring meaningful labels and current platform-rule checking. Comment triage distinguishes corrections, questions, personal experience and low-signal feedback; write proposed replies without posting. Plan production against actual available hours, anchor film plus affordable followups and independently coherent Shorts.
