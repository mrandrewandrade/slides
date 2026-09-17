#!/usr/bin/env bash
set -euo pipefail

future_root="${1:-.future-slides}"
site_root="${2:-_site/wip}"
main_root="${3:-$PWD}"

future_root="$(cd "$future_root" && pwd)"
mkdir -p "$site_root"
site_root="$(cd "$site_root" && pwd)"
main_root="$(cd "$main_root" && pwd)"

courses=(tej tts tas)

current_date() {
  local course="$1"
  local include_line
  include_line="$(grep -m1 'week-' "$main_root/current/${course}.qmd" || true)"
  if [[ "$include_line" =~ _([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.qmd ]]; then
    printf '%s\n' "${BASH_REMATCH[1]}"
    return 0
  fi
  echo "Could not determine current date for ${course}." >&2
  return 1
}

rm -rf "$future_root/.wip-output"
mkdir -p "$future_root/.wip-output"

for course in "${courses[@]}"; do
  course_label="${course^^}"
  now="$(current_date "$course")"
  output_course="$site_root/$course"
  mkdir -p "$output_course"
  index_tmp="$(mktemp)"

  cat > "$index_tmp" <<EOF
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>${course_label} Work in Progress</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5}h1{margin-bottom:.25rem}.week{border:1px solid #ddd;border-radius:.5rem;margin:1rem 0;padding:.5rem 1rem}li{margin:.45rem 0}.muted{opacity:.65}</style>
</head>
<body>
<h1>${course_label} Work in Progress</h1>
<p class="muted">Future slide decks under development. These may change before they are used in class.</p>
<p><a href="../../index.html">Back to Slides Home</a></p>
EOF

  found=0
  current_week=""

  while IFS= read -r shared_file; do
    base="$(basename "$shared_file")"
    if [[ ! "$base" =~ ^_([0-9]{4}-[0-9]{2}-[0-9]{2})-day-([0-9]{2})\.qmd$ ]]; then
      continue
    fi

    date="${BASH_REMATCH[1]}"
    day="${BASH_REMATCH[2]}"
    [[ "$date" > "$now" ]] || continue

    week_dir="$(basename "$(dirname "$shared_file")")"
    week="${week_dir#week-}"
    week_num=$((10#$week))
    day_num=$((10#$day))

    if [[ "$current_week" != "$week" ]]; then
      if [[ -n "$current_week" ]]; then
        printf '%s\n' '</ul></section>' >> "$index_tmp"
      fi
      printf '%s\n' "<section class=\"week\"><h2>Week ${week_num}</h2><ul>" >> "$index_tmp"
      current_week="$week"
    fi

    wrapper="wip-${course}-${date}-day-${day}.qmd"
    relative_shared="${shared_file#$future_root/}"
    cat > "$future_root/$wrapper" <<EOF
---
title: "${course_label} · Day ${day_num} · Work in Progress"
subtitle: "2026-27 · Semester 1 · Draft"
author: "Andrew Andrade"
---

{{< include ${relative_shared} >}}

<!-- ${course_label}-specific future slides can be added when needed. -->

{{< include 2026-27/semester-1/period-1/shared/routines/_end-of-class.qmd >}}

# Draft Status

This deck is **Work in Progress** and may change before class.
EOF

    (
      cd "$future_root"
      quarto render "$wrapper" --output-dir .wip-output -M embed-resources:true
    )

    mkdir -p "$output_course/week-${week}"
    cp "$future_root/.wip-output/${wrapper%.qmd}.html" "$output_course/week-${week}/${date}-day-${day}.html"
    rm -f "$future_root/$wrapper"

    printf '%s\n' "<li><a href=\"week-${week}/${date}-day-${day}.html\">Day ${day_num} · ${date}</a></li>" >> "$index_tmp"
    found=1
  done < <(find "$future_root/2026-27/semester-1/period-1/shared" -type f -path '*/week-*/*' -name '_*-day-*.qmd' | sort)

  if [[ -n "$current_week" ]]; then
    printf '%s\n' '</ul></section>' >> "$index_tmp"
  fi

  if [[ $found -eq 0 ]]; then
    printf '%s\n' '<p>No future slide decks are staged yet.</p>' >> "$index_tmp"
  fi

  printf '%s\n' '</body></html>' >> "$index_tmp"
  mv "$index_tmp" "$output_course/index.html"
done

cat > "$site_root/index.html" <<'EOF'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Work in Progress Slides</title>
<style>body{font-family:system-ui,sans-serif;max-width:900px;margin:3rem auto;padding:0 1rem;line-height:1.5}li{margin:.6rem 0}.muted{opacity:.65}</style>
</head>
<body>
<h1>Work in Progress</h1>
<p class="muted">Future slides under development. These are tentative and may change before class.</p>
<p><a href="../index.html">Back to Slides Home</a></p>
<ul>
<li><a href="tej/index.html">TEJ future slides</a></li>
<li><a href="tts/index.html">TTS future slides</a></li>
<li><a href="tas/index.html">TAS future slides</a></li>
</ul>
</body>
</html>
EOF

rm -rf "$future_root/.wip-output"
