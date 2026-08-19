# Inkwell.ai — report figures
#
# One folder per figure, named after the figure, holding its source and its
# renders. Sources are PlantUML (*.puml) or draw.io (*.drawio); both render to
# SVG for the report and PNG for quick review.
#
#   make            # render everything
#   make one F=fig-5-4-sequence-ai-chat-rag
#   make check      # parse the PlantUML sources without rendering
#   make regen      # re-run the draw.io generators in tools/
#   make clean
#
# PlantUML runs in Docker: --user keeps output owned by you, and HOME=/tmp stops
# it writing a Java font cache into a literal "?" folder here.
# draw.io needs the desktop app and an X display; prefix with xvfb-run if headless.

IMAGE   := plantuml/plantuml:latest
PRUN    := docker run --rm --user $(shell id -u):$(shell id -g) -e HOME=/tmp \
             -v $(CURDIR):/work -w /work $(IMAGE)
DRAWIO  := drawio --no-sandbox

PUML    := $(wildcard */*.puml)
DIO     := $(wildcard */*.drawio)

.PHONY: all puml dio one regen check clean
all: puml dio

puml:
	@test -n "$(PUML)" || { echo "no PlantUML sources"; exit 0; }
	$(PRUN) -tsvg $(PUML)
	$(PRUN) -tpng $(PUML)
	@echo "✓ PlantUML: $(words $(PUML)) figure(s)"

dio:
	@test -n "$(DIO)" || { echo "no draw.io sources"; exit 0; }
	@for f in $(DIO); do \
	  $(DRAWIO) -x -f svg -o $${f%.drawio}.svg $$f >/dev/null; \
	  $(DRAWIO) -x -f png --scale 1.5 -o $${f%.drawio}.png $$f >/dev/null; \
	done
	@echo "✓ draw.io: $(words $(DIO)) figure(s)"

one:
	@test -n "$(F)" || { echo "usage: make one F=fig-5-4-sequence-ai-chat-rag"; exit 1; }
	@if [ -f "$(F)/$(F).puml" ]; then \
	  $(PRUN) -tsvg $(F)/$(F).puml; $(PRUN) -tpng $(F)/$(F).puml; \
	elif [ -f "$(F)/$(F).drawio" ]; then \
	  $(DRAWIO) -x -f svg -o $(F)/$(F).svg $(F)/$(F).drawio >/dev/null; \
	  $(DRAWIO) -x -f png --scale 1.5 -o $(F)/$(F).png $(F)/$(F).drawio >/dev/null; \
	else echo "no source found for $(F)"; exit 1; fi
	@echo "✓ $(F)"

regen:
	cd tools && python3 gen-fig-2-1.py && python3 gen-architecture.py

check:
	$(PRUN) -checkonly $(PUML) && echo "✓ all PlantUML sources parse"

clean:
	rm -f */*.svg */*.png
