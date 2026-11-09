# Editorial operations

Create a voice.md from actual examples: cadence, vocabulary, sentence length, preferred argument forms, terms to retain and avoided phrasing. Do not invent personal stories or opinions. Use source → structured outline → draft → substantive edit → performance edit → platform adaptation. Transcript polishing removes accidental repetition without rewriting speaker meaning; retain a source anchor for sensitive or ambiguous edits. The archive and upstream include podcast production, caption creation, newsletters, social posts, cold opens, SEO writing and corpus discovery; these remain editorial modes within this one skill.

Repurposing changes the frame and unit of value: long-form explanation → self-contained short; evidence → newsletter argument; practical step → social post; comparison → carousel outline. Do not publish the same truncated paragraph on every platform. Calendars name audience, core claim, source, owner, required assets, status, channel, due date and learning metric. Store asset IDs, source URLs, usage license and SHA-256; obtain actual media rather than assuming a search image is licensed.

Preserved utilities:

```bash
python3 scripts/chunk_corpus.py licensed-markdown corpus.db
python3 scripts/image_optimizer.py --help
python3 scripts/extract_insights.py --db corpus.db --output insights.json --model qwen2.5:7b
```

Chunking is stdlib SQLite, re-indexes idempotently, and does not embed a private corpus. Image optimization needs Pillow. Insight extraction requires requests and an independently installed local Ollama model; it checkpoints completed chunks and retains original text. It is optional and not part of basic production. Use agent analysis for thematic grouping, or TF-IDF clustering from scripts/find_threads.py when a local sklearn environment is installed. Do not silently install packages or call a paid provider. Provider-specific Gemini image generation has been replaced by an optional asset-acquisition interface: use available authorized tools or user assets and record provenance; don't claim images were generated when no service ran.
