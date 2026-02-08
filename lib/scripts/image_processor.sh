#!/bin/bash

set -euo pipefail

# Usage:
#   ./image_processor.sh (find|download|convert) [args...]
#
#   - `find` all markdown files in the current directory and subdirectories,
#       extracts image URLs, and prints them in the format "location:url".
#       Example output: "path/to/image|https://example.com/image.png"
#   - `download` images from the provided URLs and saves them in the
#       "imgs" directory, naming them sequentially based on existing files.
#       Example input: "path/to/image|https://example.com/image.png"
#   - `convert` images from the provided paths to AVIF format.
#       Example input: "imgs/path/to/image/0.png"
#
# Workflow:
# - bash lib/scripts/image_processor.sh find > image_urls.txt
# - Manually review and edit image_urls.txt if needed
# - grep 'imgur.com' image_urls.txt | xargs bash lib/scripts/image_processor.sh download
# - find imgs/src -name '*' -type f | xargs bash lib/scripts/image_processor.sh convert

cmd="$1"
shift
if [ "$cmd" = 'find' ]; then
  find src -name '*.md' -print0 | xargs -0 grep '!\[' | sed 's/:.*\[/:/' | while read -r line; do
    file=$(echo "$line" | cut -d':' -f1)
    name=$(echo "$line" | cut -d']' -f1 | cut -d':' -f2)
    link=$(echo "$line" | cut -d'(' -f2- | cut -d')' -f1 | cut -d' ' -f1)
    echo "$file|$link|$name"
  done
elif [ "$cmd" = 'download' ]; then
  for line in "$@"; do
    loc=$(echo "$line" | cut -d'|' -f1 | rev | cut -d'.' -f2- | rev)
    url=$(echo "$line" | cut -d'|' -f2-)
    if [ -z "$url" ]; then
      echo "Skipping empty URL for location $loc"
      continue
    fi

    mkdir -p "imgs/$loc"
    file_exists=$(find "imgs/$loc" -maxdepth 1 -type f | wc -l | awk '{print $1}')
    dest="imgs/$loc/$file_exists.${url##*.}"
    echo "Downloading $url to $dest"
    curl "$url" -o "$dest"
  done
elif [ "$cmd" = 'convert' ]; then
  for img in "$@"; do
    filename=$(basename "$img")
    extension="${filename##*.}"
    dest="${img%.*}.avif"
    dest="imgs/compressed/$(echo "$dest" | cut -d'/' -f3-)"
    if [ "$extension" = "avif" ] || [ "$extension" = "" ]; then
      echo "$img: avif-ed"
      continue
    fi
    if [ -f "$dest" ]; then
      echo "$img: done"
      continue
    fi

    echo "$img: start"
    mkdir -p "$(dirname "$dest")"
    if [ "$extension" = "webp" ]; then
      tmp="${img%.*}.png"
      dwebp "$img" -o "$tmp"
      img="$tmp"
    elif [ "$extension" = "gif" ]; then
      ffmpeg -i "$img" -c:v libaom-av1 -crf 30 -b:v 0 "$dest"
      continue
    fi
    # slowest but highest compression
    avifenc --speed 0 "$img" "$dest"
  done
else
  echo "Usage: $0 {find|download|convert} [args...]"
  exit 1
fi
