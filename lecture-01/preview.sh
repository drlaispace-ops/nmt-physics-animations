#!/bin/zsh
# Перегляд для Іллі: кожна final/*.mov накладається на тло курсу → preview/*.mp4 (H.264).
# Ці файли зручно скинути на телефон і переглянути «на відстані витягнутої руки».
#   ./preview.sh            — зробити прев'ю для всіх нових фіналів
#   ./preview.sh --all      — перезробити всі
set -e
cd "${0:A:h}"
mkdir -p preview
for src in final/*.mov; do
  out="preview/${${src:t}:r}.mp4"
  if [[ "$1" != "--all" && -f "$out" && "$out" -nt "$src" ]]; then continue; fi
  ffmpeg -loglevel error -y -f lavfi -i "color=c=0x121826:s=1920x1080:r=25" -i "$src" \
    -filter_complex "[0][1]overlay=shortest=1:format=auto" \
    -c:v libx264 -crf 20 -preset medium -pix_fmt yuv420p -movflags +faststart "$out"
  echo "→ $out"
done
