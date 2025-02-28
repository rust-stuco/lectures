#!/bin/bash

# Usage: ./build.sh path/to/slides.md path/to/template.html
# Generates slides at output.html, with template.html injected at end of <body> tags
# Can be used to add extra <script>s to our slides

# Check if the user provided paths to slides.md and template.html
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 path_to_slides.md path_to_template.html"
  exit 1
fi

# Get the paths from the arguments
slides_md="$1"
template_path="$2"

# Generate slides with bespoke template
marp "$slides_md" -o output.html --template bespoke

# Read the template and escape special characters
template=$(cat "$template_path" | awk '{printf "%s\\n", $0}')

sed -i '' "s|</body>|$template</body>|" output.html

chmod +x build.sh
