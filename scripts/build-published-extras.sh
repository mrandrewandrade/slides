#!/usr/bin/env bash
set -euo pipefail

site_root="${1:-_site}"
archive_root="$site_root/archive/2026-27/semester-1"
mkdir -p "$archive_root" "$site_root/wip"

echo "Building archive indexes..."

for course in tej tts tas; do
  label="${course^^}"
  course_root="$archive_root/$course"
  mkdir -p "$course_root"

  {
    cat <<EOF
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${label} All Published Slides</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5;color:#2f3439}a{color:#234a73}.muted{color:#777}li{margin:.45rem 0}</style>
</head>
<body>
<h1>${label} All Published Slides</h1>
<p class="muted">Completed classroom slide decks.</p>
<p><a href="../../../../index.html">Back to Slides Home</a></p>
<ul>
EOF

    found=0
    while IFS= read -r file; do
      [[ -n "$file" ]] || continue
      relative="${file#$course_root/}"
      name="$(basename "$file")"
      if [[ "$name" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.html$ ]]; then
        date="${BASH_REMATCH[1]}"
        day=$((10#${BASH_REMATCH[2]}))
        printf '<li><a href="%s">Day %d - %s</a></li>\n' "$relative" "$day" "$date"
        found=1
      fi
    done < <(find "$course_root" -mindepth 2 -maxdepth 2 -type f -name '*.html' -print 2>/dev/null | sort -r)

    if [[ $found -eq 0 ]]; then
      echo '<li>No published slides yet.</li>'
    fi

    cat <<'EOF'
</ul>
</body>
</html>
EOF
  } > "$course_root/index.html"
done

echo "Building semester planning decks..."

cat > "$site_root/wip/index.html" <<'EOF'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Semester Planning Decks</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5;color:#2f3439}a{color:#234a73}.muted{color:#777}</style>
</head>
<body>
<h1>Semester Planning Decks</h1>
<p class="muted">Calendar-driven work in progress. Staged lesson slides replace placeholders when they exist.</p>
<ul>
<li><a href="tej/index.html">TEJ Semester 1 planning deck</a></li>
<li><a href="tts/index.html">TTS Semester 1 planning deck</a></li>
<li><a href="tas/index.html">TAS Semester 1 planning deck</a></li>
<li><a href="semester2/index.html">Generic Semester 2 planning deck</a></li>
</ul>
<p><a href="../index.html">Back to Slides Home</a></p>
</body>
</html>
EOF

bash scripts/python.sh scripts/build-semester-planning.py "$site_root/wip"

echo "Archive and semester planning pages ready."
