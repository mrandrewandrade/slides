#!/usr/bin/env bash
set -euo pipefail

site_root="${1:-_site}"
mkdir -p "$site_root"

# Keep the full local build deliberately simple and self-contained.
# Archive indexes are generated from the files already present in _site.
python scripts/build-archive-pages.py "$site_root"

# Semester planning now lives on this branch. Do not fetch another branch or
# create a temporary worktree during a normal local build. Until the local
# Semester 1 WIP renderer is populated, provide stable placeholder pages so
# navigation remains valid without making the build fragile.
mkdir -p "$site_root/wip"

cat > "$site_root/wip/index.html" <<'EOF'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Work in Progress Slides</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5;color:#2f3439}a{color:#234a73}.muted{color:#777}</style>
</head>
<body>
<h1>Work in Progress</h1>
<p class="muted">Semester 1 planning lives on this branch and is being expanded through the exam period.</p>
<ul>
<li><a href="tej/index.html">TEJ future slides</a></li>
<li><a href="tts/index.html">TTS future slides</a></li>
<li><a href="tas/index.html">TAS future slides</a></li>
</ul>
<p><a href="../index.html">Back to Slides Home</a></p>
</body>
</html>
EOF

for course in tej tts tas; do
  mkdir -p "$site_root/wip/$course"
  label="${course^^}"
  cat > "$site_root/wip/$course/index.html" <<EOF
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${label} Work in Progress</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5;color:#2f3439}a{color:#234a73}.muted{color:#777}</style>
</head>
<body>
<h1>${label} Work in Progress</h1>
<p class="muted">Future Semester 1 material is being built directly on the current planning branch. This page stays intentionally lightweight so the normal full build remains reliable.</p>
<p><a href="../../index.html">Back to Slides Home</a></p>
</body>
</html>
EOF
done
