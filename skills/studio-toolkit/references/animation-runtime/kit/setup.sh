#!/usr/bin/env bash
# Project-local runtime installation. Voice models are optional and explicit.
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
command -v npm >/dev/null
(cd "$KIT" && npm ci --no-audit --no-fund)
if [ "${1:-}" = "--voice" ]; then
  echo 'For optional offline English calibration speech/ASR, run setup-offline-voice.sh explicitly.'
  exit 1
fi
printf '%s\n' 'Runtime ready. Use the toolkit Python environment with Playwright/Chromium. New production speech uses ElevenLabs.'
