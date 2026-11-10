#!/usr/bin/env bash
# Reuse imported measured narration; synthesis is never an implicit build step.
set -euo pipefail
ENGINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${1:?usage: make.sh PROJECT}"
exec node "$ENGINE/tools/render.js" video render/final.mp4
