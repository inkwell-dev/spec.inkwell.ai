#!/usr/bin/env python3
"""Generate fig-2-1 (global use case diagram) as an editable .drawio file.

Hand-placed on purpose. PlantUML's Graphviz layout cannot hold include/extend
relations inside the system boundary at this size — four attempts pushed the
extend targets outside it. Coordinates here are explicit, so containment and
the actor column are guaranteed, and the file still opens in the draw.io GUI
for touch-ups.

Style matches the example report: black on white, stick-figure actors labelled
below, plain rectangle boundary, external systems outside it, yellow note.
"""
from xml.sax.saxutils import escape

ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontStyle=1;fontSize=12;"
UC    = "ellipse;whiteSpace=wrap;html=1;fontStyle=1;fontSize=12;"
BOX   = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=12;"
EXT   = "rounded=0;whiteSpace=wrap;html=1;fontStyle=1;fontSize=12;"
NOTE  = ("shape=note;whiteSpace=wrap;html=1;fillColor=#FFF2CC;strokeColor=#D6B656;"
         "size=14;fontStyle=2;fontSize=11;align=left;verticalAlign=top;spacingLeft=6;")
ASSOC = "endArrow=none;html=1;edgeStyle=none;rounded=0;strokeColor=#000000;"
GEN   = "endArrow=block;endFill=0;html=1;edgeStyle=none;rounded=0;strokeColor=#000000;"
DASH  = ("endArrow=open;endFill=0;dashed=1;html=1;edgeStyle=none;rounded=0;"
         "strokeColor=#000000;fontSize=10;")

# id: (label, x, y, w, h, style)
nodes = {
    "SYS": ("&lt;&lt; System &gt;&gt;", 200, 30, 1000, 860, BOX),

    # actors, one ordered column
    "A_VIS":  ("Visitor",                    50,  70, 30, 60, ACTOR),
    "A_FREE": ("Free reader",                50, 190, 30, 60, ACTOR),
    "A_PREM": ("Premium reader",             50, 310, 30, 60, ACTOR),
    "A_WRIT": ("Writer",                     50, 430, 30, 60, ACTOR),
    "A_ELIG": ("Eligible writer",            50, 550, 30, 60, ACTOR),
    "A_MUN":  ("Magazine\n(unsubscribed)",   50, 670, 30, 60, ACTOR),
    "A_MSUB": ("Magazine\n(subscribed)",     50, 790, 30, 60, ACTOR),
    "A_ADM":  ("Administrator",              50, 910, 30, 60, ACTOR),

    # left column of use cases
    "ACCOUNT":  ("Create an account",                        250,  60, 200, 50, UC),
    "FEED":     ("Browse the feed and read an article",      250, 130, 200, 56, UC),
    "SEARCH":   ("Search (lexical + semantic)",              250, 205, 200, 50, UC),
    "INTERACT": ("Interact (like, comment, follow, report)", 250, 300, 200, 60, UC),
    "WRITE":    ("Write and publish an article",             250, 400, 200, 50, UC),
    "LIST":     ("List on the marketplace",                  250, 480, 200, 50, UC),
    "AI":       ("Use the AI assistant",                     250, 580, 200, 50, UC),
    "STATS":    ("View analytics and earnings",              250, 680, 200, 50, UC),

    # centre column
    "GOOGLE":   ("Sign in with Google",                      530, 300, 170, 50, UC),
    "SIGNIN":   ("Sign in",                                  530, 400, 170, 50, UC),
    "RETRIEVE": ("Retrieve passages from the writer's own corpus", 505, 570, 220, 66, UC),

    # right column
    "SUBS":    ("Manage subscription and credits",           830, 300, 200, 56, UC),
    "EVAL":    ("Evaluate a writer and read AI insights",    830, 395, 200, 60, UC),
    "ACQUIRE": ("Acquire an article",                        830, 490, 200, 50, UC),
    "PREVIEW": ("Unlock a preview (10% of the price)",       830, 570, 200, 56, UC),
    "ADMIN":   ("Administer the platform",                   830, 680, 200, 50, UC),

    # external systems, outside the boundary
    "EXT_LLM": ("Large language model provider",            1270, 395, 180, 50, EXT),
    "EXT_EMB": ("Embedding provider",                       1270, 205, 180, 50, EXT),

    "NOTE": ("Placement is chosen at publish time and is one-way: a marketplace "
             "article may become public, never the reverse.", 980, 60, 200, 110, NOTE),
}

# (source, target, style, label)
edges = [
    # actor generalisation — specific points up to general
    ("A_FREE", "A_VIS",  GEN, ""), ("A_PREM", "A_FREE", GEN, ""),
    ("A_WRIT", "A_FREE", GEN, ""), ("A_ELIG", "A_WRIT", GEN, ""),
    ("A_MSUB", "A_MUN",  GEN, ""),

    # associations
    ("A_VIS", "ACCOUNT", ASSOC, ""), ("A_VIS", "FEED", ASSOC, ""),
    ("A_VIS", "SEARCH", ASSOC, ""), ("A_VIS", "SIGNIN", ASSOC, ""),
    ("A_FREE", "INTERACT", ASSOC, ""), ("A_PREM", "AI", ASSOC, ""),
    ("A_WRIT", "WRITE", ASSOC, ""), ("A_WRIT", "STATS", ASSOC, ""),
    ("A_ELIG", "LIST", ASSOC, ""), ("A_MUN", "SUBS", ASSOC, ""),
    ("A_MSUB", "EVAL", ASSOC, ""), ("A_MSUB", "ACQUIRE", ASSOC, ""),
    ("A_ADM", "ADMIN", ASSOC, ""),

    # every authenticated use case includes Sign in — drawn, not implied
    ("INTERACT", "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("WRITE",    "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("AI",       "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("STATS",    "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("SUBS",     "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("EVAL",     "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("ACQUIRE",  "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("ADMIN",    "SIGNIN", DASH, "\u00abinclude\u00bb"),

    # extensions — optional behaviour on a base use case
    ("GOOGLE",  "SIGNIN",  DASH, "\u00abextend\u00bb"),
    ("LIST",    "WRITE",   DASH, "\u00abextend\u00bb"),
    ("PREVIEW", "ACQUIRE", DASH, "\u00abextend\u00bb"),

    # a mandatory sub-behaviour
    ("AI", "RETRIEVE", DASH, "\u00abinclude\u00bb"),

    # external systems
    ("EVAL", "EXT_LLM", ASSOC, ""),
    ("SEARCH", "EXT_EMB", ASSOC, ""),
]

cells = []
for nid, (label, x, y, w, h, style) in nodes.items():
    parent = "SYS" if nid not in ("SYS",) and style is UC else "1"
    # keep geometry absolute: put everything on the default parent
    cells.append(
        f'<mxCell id="{nid}" value="{label}" style="{style}" vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
for i, (src, dst, style, label) in enumerate(edges):
    cells.append(
        f'<mxCell id="e{i}" value="{label}" style="{style}" edge="1" parent="1" '
        f'source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>')

xml = ('<mxfile host="Electron" type="device">\n'
       '  <diagram id="fig-2-1" name="Figure 2.1 - Global use case diagram">\n'
       '    <mxGraphModel dx="1500" dy="1000" grid="1" gridSize="10" guides="1" '
       'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
       'pageWidth="1600" pageHeight="1100" math="0" shadow="0">\n'
       '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
       + "\n        ".join(cells) +
       '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')

open("../fig-2-1-use-case-global/fig-2-1-use-case-global.drawio", "w").write(xml)
print(f"wrote fig-2-1-use-case-global.drawio — {len(nodes)} nodes, {len(edges)} edges")
