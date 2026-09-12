#!/usr/bin/env bash
set -euo pipefail

# Run the current slide site locally.
# The project render list is intentionally small, so Quarto only watches the
# index and the three current class decks.
exec quarto preview
