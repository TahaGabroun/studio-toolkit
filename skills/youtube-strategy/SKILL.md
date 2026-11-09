---
name: youtube-strategy
description: "Audit YouTube channels, position a series, research competitors and SEO, plan thumbnails and calendars, and analyze supplied channel analytics. Use for channel-level growth and audience decisions."
---

# Studio YouTube Channel — strategy desk

Use when the unit of decision is a channel, portfolio, series, editorial calendar or content business, not just a single script.

## Strategy workflow

1. Establish niche, target audience, region/language, publishing capacity and strategic aim: reach, trust, leads, learning outcomes or monetization. Infer missing nonessential factors cautiously.
2. Inventory evidence: user's published videos, views, click-through, audience retention, traffic source, subscriber conversion, impressions and costs, *only where provided*. Separate directly observed channel numbers from public competitor numbers and editorial hypotheses.
3. Diagnose **discoverability → packaging → viewing satisfaction → repeat audience → conversion**. Ask which single stage is the binding constraint, backed by metrics.
4. Analyze competitive content ethically using public URLs/metadata or authorized platform access. Normalize comparison using channel context, upload dates, topic, distribution and size. Never scrape behind authentication or assert a “secret algorithm.”
5. Propose 8–12 concrete ideas with an audience question, packaging angle, unique evidence/experience, production burden, primary KPI and post-publication learning signal. Rank by impact × confidence ÷ cost, state judgment assumptions.
6. Build a realistic cadence: anchor videos, low-cost follow-ups, Shorts, community posts. Respect the creator's actual time and resources.
7. Monetization: distinguish eligibility criteria, ads, sponsors, courses, products and services. Verify current YouTube policies and regional restrictions before presenting as fact.

## Reporting

Produce: a short decision memo, evidence table, ranked backlog, calendar and one main experiment for the next 30 days. Include baseline metrics, success threshold, source links and measurement dates when available. With no analytics, create a **provisional qualitative plan** explicitly marked as such.

Hand off selected ideas to `youtube-script-writer`, production operations to `youtube-agent`, and editorial repurposing to `content-os`.

## Native execution contract

Read [strategy operations](references/strategy-operations.md) for audit, keyword, monetization, thumbnail and channel-format playbooks, plus optional YouTube API fetchers. Accept analytics CSV/JSON or public channel URLs. Without account access label the plan qualitative. Produce a dated audit, normalized competitor evidence, ranked backlog, calendar and experiment. Hand selected ideas to `youtube-agent`; pass repurposing to `content-os`.

Use the installed `studio-toolkit` sibling for the shared CLI and schemas. In a repository checkout its entry is `skills/studio-toolkit/scripts/studio.py`; resolve paths from the actual skill directory, not the current working directory. In a single-skill ChatGPT package use the bundled `scripts/studio.py`.

Default settings, error handling and QA: follow [shared pipeline](../studio-toolkit/references/pipeline.md) and [production standard](../studio-toolkit/references/quality.md). Read only the specialist references needed for the requested task. Do not fabricate unavailable service results; preserve completed artifacts and report actionable failures.
