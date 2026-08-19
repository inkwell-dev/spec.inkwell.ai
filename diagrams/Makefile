# Inkwell.ai — report figures
#
# Renders every *.puml in this directory to SVG (for LaTeX / Word) and PNG
# (for quick review). Requires only Docker: the plantuml/plantuml image ships
# PlantUML 1.2026.6 and Graphviz 14.
#
#   make          # SVG + PNG for every diagram
#   make svg      # SVG only
#   make one F=fig-2-1-cas-utilisation-global
#   make clean
#
# --user keeps output owned by you; without it Docker writes root-owned files
# into the working tree. HOME=/tmp stops PlantUML trying to write a config
# directory it has no permission to create.

IMAGE  := plantuml/plantuml:latest
RUN    := docker run --rm --user $(shell id -u):$(shell id -g) -e HOME=/tmp \
            -v $(CURDIR):/work -w /work $(IMAGE)
SOURCES := $(filter-out _%.puml,$(wildcard *.puml))

# draw.io figures are hand-placed and live in drawio/. They need draw.io Desktop
# and an X display; on a headless box prefix with xvfb-run.
DRAWIO  := drawio --no-sandbox
DRAWIO_SRC := $(wildcard drawio/*.drawio)

.PHONY: all svg png one drawio clean check
all: svg png drawio

svg:
	@test -n "$(SOURCES)" || { echo "no .puml sources"; exit 1; }
	$(RUN) -tsvg $(SOURCES)
	@echo "✓ SVG written: $(words $(SOURCES)) figure(s)"

png:
	@test -n "$(SOURCES)" || { echo "no .puml sources"; exit 1; }
	$(RUN) -tpng $(SOURCES)
	@echo "✓ PNG written: $(words $(SOURCES)) figure(s)"

one:
	@test -n "$(F)" || { echo "usage: make one F=fig-2-1-cas-utilisation-global"; exit 1; }
	$(RUN) -tsvg $(F).puml
	$(RUN) -tpng $(F).puml
	@echo "✓ $(F)"

drawio:
	@test -n "$(DRAWIO_SRC)" || { echo "no .drawio sources"; exit 0; }
	@for f in $(DRAWIO_SRC); do \
	  $(DRAWIO) -x -f svg -o $${f%.drawio}.svg $$f >/dev/null; \
	  $(DRAWIO) -x -f png --scale 1.5 -o $${f%.drawio}.png $$f >/dev/null; \
	done
	@echo "✓ draw.io: $(words $(DRAWIO_SRC)) figure(s)"

check:
	$(RUN) -checkonly $(SOURCES) && echo "✓ all sources parse"

clean:
	rm -f *.svg *.png drawio/*.svg drawio/*.png
