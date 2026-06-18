#!/bin/bash
# scripts/generate_images.sh
# Convierte todos los SVG en /images/ a PNG en /dist/images/ usando Inkscape o rsvg-convert.
# Requisitos: inkscape o rsvg-convert (librsvg), ImageMagick opcional.

set -euo pipefail

mkdir -p dist/images

# Ajustes de resolución por archivo (nombre: widthxheight). Añade o modifica si lo necesitas.
declare -A sizes=(
  [banner_capacitacion_gemini.svg]="1200x400"
  [card_slack_gemini.svg]="1080x1080"
  [infographic_ruta_aprendizaje.svg]="800x2000"
  [slide_title_sesion01.svg]="1920x1080"
  [slide_title_sesion02.svg]="1920x1080"
  [slide_title_sesion03.svg]="1920x1080"
  [slide_title_sesion04.svg]="1920x1080"
  [slide_title_sesion05.svg]="1920x1080"
  [slide_title_sesion06.svg]="1920x1080"
  [slide_title_sesion07.svg]="1920x1080"
  [slide_title_sesion08.svg]="1920x1080"
)

# Función para rasterizar con inkscape o rsvg-convert
rasterize() {
  local svg="$1"; shift
  local out="$1"; shift
  local size="$1"; shift
  local w=${size%x*}
  local h=${size#*x}

  if command -v inkscape >/dev/null 2>&1; then
    inkscape "$svg" --export-filename="$out" --export-width="$w" --export-height="$h"
  elif command -v rsvg-convert >/dev/null 2>&1; then
    rsvg-convert -w "$w" -h "$h" "$svg" -o "$out"
  else
    echo "Ni inkscape ni rsvg-convert disponibles. Instala uno de ellos para usar este script." >&2
    exit 1
  fi
}

for svg in images/*.svg; do
  filename=$(basename "$svg")
  if [[ -n "${sizes[$filename]:-}" ]]; then
    size=${sizes[$filename]}
  else
    size="1200x800"
  fi
  out="dist/images/${filename%.svg}.png"
  echo "Rasterizando $svg -> $out ($size)"
  rasterize "$svg" "$out" "$size"
done

echo "Imágenes generadas en dist/images/"