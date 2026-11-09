# Strategy operations

Audit discovery → packaging → viewing satisfaction → return audience → conversion. Preserve the upstream specialist modes: audit, analyze, competitor, ideate, SEO, metadata, thumbnail, hook, script, Shorts, repurpose, monetize, calendar and strategy. Route script/repurposing execution to the dedicated toolkit skill.

Channel formats: education, tutorial, niche authority, personal brand, review, commentary, entertainment, vlog and Shorts-first. Match frequency and success measures to production capacity. Compare CTR only within traffic-source context; raw view counts do not measure idea quality. A low-impression video cannot establish a packaging failure. Thumbnail plan: clear single subject, readable at feed size, honest promised outcome, two materially different experiments. SEO: intent/query fit in topic/title/opening, coherent description and chapters; tags have limited diagnostic value. Verify current monetization eligibility and platform rules rather than freezing dated thresholds in the skill.

Optional read-only connectors:

```bash
python3 scripts/fetch_channel_data.py --help
python3 scripts/search_competitor_videos.py --help
python3 scripts/fetch_transcript.py --help
python3 scripts/fetch_video_analytics.py --help
python3 scripts/utils/youtube_auth.py --check api_key
```

Install repository requirements-youtube.txt in a venv. Public Data API requests use YOUTUBE_API_KEY; private Analytics needs authorized OAuth. State defaults to ~/.local/share/studio-toolkit or STUDIO_STATE_DIR. OAuth scopes are read-only. Keep tokens outside projects and mode 0600. No credentials are bundled. Quota tracking is a local estimate, not authoritative remaining Google quota. Transcripts may fail when captions are disabled or network/platform restrictions intervene. Do not bypass those restrictions. Private analytics endpoints cannot expose competitor private metrics; impressions and CTR require user exports where unavailable in the Analytics API. These live services are optional and need real account testing.
