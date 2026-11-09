# Validation report — 2026-11-09

This is the original 0.2 baseline. The [0.3 Anatomy/ElevenLabs workflow update](WORKFLOW-UPDATE.md) records its additional tests and limits.

Baseline: Linux Ubuntu 26.04, Python 3.10.9, Node 24.22.2, FFmpeg 4.2.2, Codex 0.165.0-alpha.1.2, Remotion 4.0.542, local Chromium and pinned Python/Node dependency locks. No paid API was used.

| Check | Result |
|---|---|
| All 8 upstream license files and pinned commits | MIT verified; notices retained |
| Native skill metadata | 9/9 pass bundled skill-creator validator |
| Actual Codex discovery | 9/9 listed by CLI prompt inventory; global symlinks verified at ~/.codex/skills |
| Installer lifecycle | Install/validate/update/uninstall and conflict isolation pass |
| Repository YAML, relative links, schema mirrors and Python syntax | Pass |
| Python regression suite | 36 passed, 0 failed |
| Demos Node suite | 7 passed, 0 failed, including fresh-checkout state restoration |
| TypeScript | tsc --noEmit passes |
| Preserved YouTube programs | All 6 executed successfully on labelled synthetic exports |
| Scriptwriting (Test A) | 636 spoken words, 8 source-linked scenes, hook/payoff/visual checks pass; estimated 238.5–293.5 seconds |
| Motion graphics (Test B) | Square Remotion master plus landscape, vertical and educational masters rendered; representative source and encoded frames inspected |
| Narration sync (Test C) | Measured generated speech phrase cues and captions; 4s encoded calibration checks within one frame |
| Complete workflow (Test D) | HTML brief → script → storyboard → timeline → source → audio → MP4 → QA → publication package completed; 4 Remotion projects use the same artifact contracts |
| Narration formats | Actual WAV, MP3 and M4A timestamp import/validation passed |
| Browser fallback | Playwright Ubuntu 24.04 fallback downloaded and actually rendered a 30-frame 1080p deterministic test on this host |
| ChatGPT bundle | Extracted standalone; runtime init/validate and relative references pass; exactly one SKILL.md |

## Rendered demonstrations

| Demo | Size | Frames | Duration | Integrated loudness | True peak |
|---|---|---:|---:|---:|---:|
| documentary | 1920×1080 | 1096 | 36.533s | -16.67 LUFS | -4.33 dBTP |
| vertical | 1080×1920 | 888 | 29.600s | -16.22 LUFS | -4.48 dBTP |
| graphics | 1080×1080 | 777 | 25.900s | -16.83 LUFS | -4.44 dBTP |
| inflammation | 1920×1080 | 1357 | 45.233s | -16.70 LUFS | -4.45 dBTP |

All masters passed complete FFmpeg decoding, expected dimensions/FPS/frame count, duration and audio stream checks, project schemas, media/asset hashes and caption consistency. Agent frame inspection is recorded in gallery evidence. No full human visual, scientific or listening approval is implied. Generated eSpeak test narration is suitable for reproducible timing validation; natural voice quality and Arabic pronunciation require review before release.

## Synchronization evidence

The independent 4s HTML calibration uses labelled 1200 Hz test pulses (not speech), one timeline and deterministic out-of-order seeks. Maximum encoded pulse-peak error: 0.208 ms, below the 33.333 ms frame interval. Stream timing and pulse measurements do not establish semantic or phoneme-level alignment. The educational film aligns visual mechanism changes to measured generated speech phrase boundaries; it does not claim forced alignment of spontaneous recordings.

## Bugs found and corrected

Forward testing found non-atomic cue import preflight, unchecked event ends, missing-caption acceptance, undeclared source absence and stale QA acceptance. Import now resolves cues before writing; end times, captions and renderer files are validated; QA completion is bound to video and current input hashes. Numeric JSON overflow and caption validation without a completed timeline were also corrected. A clean-clone test caught missing local stage records; the demo render command now restores them from validated source artifacts without regenerating approved audio. All relevant regression tests pass.

## Limits and unexecuted checks

- Human creative, scientific and final listening approval: pending. Biological diagrams are original teaching schematics with compressed, overlapping phases, not clinical data.
- Live YouTube OAuth/API access, yt-dlp network retrieval, external logo/SFX services, optional Ollama inference and local Whisper inference: not executed. No credentials or service results are fabricated.
- True word/phoneme forced alignment of a natural prerecorded speaker: not demonstrated; reviewed timestamps and optional ASR drafts are supported.
- Actual 4K master, alpha/ProRes workflow, other operating systems and ChatGPT account import: not executed. 4K project dimensions/schema are tested; alpha remains a documented workflow requiring output verification.
- Primary HTML renderer does not accumulate subframe motion blur. No upstream branded gallery films/logos/music are redistributed.
- GitHub Actions status is verified separately after publication; local success does not imply remote CI success.

The two repositories contain source, documentation, dependency locks, license notices, sample generated assets and automated checks. No YouTube upload or marketplace submission was performed.
