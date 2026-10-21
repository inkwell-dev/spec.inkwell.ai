#!/bin/sh
# Builds report/build/Inkwell-PFE-Report.pdf and .docx. Needs Docker, and the
# draw.io desktop app for the vector exports of the draw.io figures.
#
#   report/make-pdf.sh
set -eu
cd "$(dirname "$0")"
SPEC="$(cd .. && pwd)"

# Vector exports of the draw.io figures, refreshed when their source is newer.
for src in ../diagrams/*/*.drawio; do
  pdf="${src%.drawio}.pdf"
  if [ ! -f "$pdf" ] || [ "$src" -nt "$pdf" ]; then
    drawio --no-sandbox -x -f pdf --crop -o "$pdf" "$src" >/dev/null 2>&1
  fi
done

python3 build.py

PANDOC="docker run --rm --user $(id -u):$(id -g) -e HOME=/tmp -e OSFONTDIR=/usr/share/fonts/host
  -v $SPEC:/data -v /usr/share/fonts:/usr/share/fonts/host:ro -w /data/report/build pandoc/extra:3.6"
COMMON="-F pandoc-crossref --citeproc --bibliography=../references.bib --csl=../ieee.csl
  --resource-path=/data/report:/data/report/build --metadata-file=../metadata.yaml"

$PANDOC report-latex.md $COMMON --top-level-division=chapter --number-sections \
  -H ../latex/header.tex --lua-filter=../latex/tech-rows.lua --lua-filter=../latex/pin-screens.lua --lua-filter=../latex/grid-tables.lua --lua-filter=../latex/foldouts.lua --pdf-engine=lualatex -o Inkwell-PFE-Report.pdf
[ -n "${DRAFT:-}" ] || $PANDOC report-docx.md $COMMON --top-level-division=chapter --number-sections \
  --lua-filter=../latex/tech-rows.lua -o Inkwell-PFE-Report.docx
echo "built: $(pwd)/build/Inkwell-PFE-Report.pdf and .docx"
