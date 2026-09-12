#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash scripts/preview.sh <tej|tts|tas>" >&2
  exit 1
fi

exec bash scripts/slides.sh preview "$1"
