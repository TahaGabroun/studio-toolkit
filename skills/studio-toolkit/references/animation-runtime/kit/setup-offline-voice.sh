#!/usr/bin/env bash
# One-time setup for the animation skills: checks ffmpeg and Node, installs three.js + Playwright into kit/node_modules,
# fetches GSAP and warms up HyperFrames. Safe to run again.
#   bash kit/setup.sh            # enough for /graph, /minimalistic-graphics, /map-route, /breakdown and the two engines' pictures
#   bash kit/setup.sh --voice    # also makes kit/.venv with the free voice (Kokoro) and word timings (Parakeet), ~1 GB of models
set -euo pipefail
KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
say() { printf '\033[1m%s\033[0m\n' "$*"; }

command -v ffmpeg >/dev/null || { echo "ffmpeg is missing. Mac: brew install ffmpeg"; exit 1; }
command -v npm >/dev/null || { echo "Node.js 18+ is missing. Mac: brew install node"; exit 1; }
PY=$(command -v python3) || { echo "python3 is missing"; exit 1; }
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' || { echo "python 3.9+ is needed"; exit 1; }

if [ "${1:-}" = "--download-models" ]; then
  if [ ! -x "$KIT/.venv/bin/python" ]; then
    say "making kit/.venv"
    "$PY" -m venv "$KIT/.venv"
  fi
  "$KIT/.venv/bin/python" -m pip install -q --upgrade pip
  "$KIT/.venv/bin/python" -m pip install -q numpy scipy soundfile kokoro-onnx sherpa-onnx
  M="$KIT/models"
  mkdir -p "$M"
  say "downloading the voice and word-timing models (about 1 GB, once)"
  [ -s "$M/kokoro-v1.0.onnx" ] || curl -fL -o "$M/kokoro-v1.0.onnx" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
  [ -s "$M/voices-v1.0.bin" ] || curl -fL -o "$M/voices-v1.0.bin" https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
  if ! ls -d "$M"/sherpa-onnx-nemo-parakeet* >/dev/null 2>&1; then
    curl -fL -o "$M/p.tar.bz2" https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2
    (cd "$M" && tar xjf p.tar.bz2 && rm p.tar.bz2)
  fi
fi
say "Optional offline setup requires --download-models (~1 GB). Production narration remains ElevenLabs."
