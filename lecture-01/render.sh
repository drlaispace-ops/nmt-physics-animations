#!/bin/zsh
# Рендер анімацій Лекції 1.
#   ./render.sh draft a12_trapezoid_cut.py A12_TrapezoidCut   # 480p15, перевірка руху й таймінгу
#   ./render.sh final a12_trapezoid_cut.py A12_TrapezoidCut   # 1080p25, прозорий фон → final/*.mov (ProRes 4444)
#   ./render.sh qa    a12_trapezoid_cut.py A12_TrapezoidCut   # final + контрольний аркуш qa/<Клас>.png
set -e
cd "${0:A:h}"
# venv з manim 0.22.0 (див. requirements.txt); інший шлях — через змінну VENV
VENV="${VENV:-/Users/illia_nakonecnyi/Desktop/abitly_project/.venv-manim}"
MANIM="$VENV/bin/manim"; PY="$VENV/bin/python"
[[ -x $MANIM ]] || { MANIM=manim; PY=python3; }
mode=$1; file=$2; shift 2

case $mode in
  draft)
    $MANIM -ql --media_dir ./media "$file" "$@"
    ;;
  final|qa)
    $MANIM -qh -t --media_dir ./media "$file" "$@"
    mkdir -p final
    stem=${file:r}
    for cls in "$@"; do
      src="media/videos/${stem}/1080p25/${cls}.mov"
      num=${cls[2,3]}
      out="final/anim_1_${num}_${cls}_v1.mov"
      ffmpeg -loglevel error -y -i "$src" -c:v prores_ks -profile:v 4444 \
        -pix_fmt yuva444p10le -alpha_bits 16 -vendor apl0 "$out"
      echo "→ $out"
      if [[ $mode == qa ]]; then
        $PY -I qa.py "$src" "qa/${cls}.png"
      fi
    done
    ;;
  *)
    echo "режим: draft | final | qa"; exit 1;;
esac
