#!/usr/bin/env bash
set -euo pipefail

target="${1:-all}"
exec bash scripts/slides.sh build "$target"
