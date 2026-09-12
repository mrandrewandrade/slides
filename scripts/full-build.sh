#!/usr/bin/env bash
set -euo pipefail

archive_root="${1:-archive}"

bash scripts/site.sh index "$archive_root"
quarto render --profile full
