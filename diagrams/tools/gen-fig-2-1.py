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
#
# The actors are drawn in three groups that touch nowhere, so that no
# generalisation is implied where none exists: the personal accounts on the
# left (Visitor → Free reader → Premium reader, Free reader → Writer → Eligible
# writer), the magazines at the top right, and the administrator alone at the
# bottom right. Neither a magazine nor the administrator specialises a reader.
nodes = {
    "SYS": ("&lt;&lt; System &gt;&gt;", 210, 30, 890, 900, BOX),

    # personal accounts, left
    "A_VIS":  ("Visitor",                    75, 140, 30, 60, ACTOR),
    "A_FREE": ("Free reader",                75, 280, 30, 60, ACTOR),
    "A_PREM": ("Premium reader",             25, 420, 30, 60, ACTOR),
    "A_WRIT": ("Writer",                    135, 420, 30, 60, ACTOR),
    "A_ELIG": ("Eligible writer",           135, 600, 30, 60, ACTOR),
    # magazines, top right
    "A_MUN":  ("Magazine\n(unsubscribed)",  1190, 90, 30, 60, ACTOR),
    "A_MSUB": ("Magazine\n(subscribed)",    1190, 290, 30, 60, ACTOR),
    # administrator, alone at the bottom right
    "A_ADM":  ("Administrator",              1190, 720, 30, 60, ACTOR),

    # left column of use cases
    "FEED":     ("Browse the feed and read an article",      250, 60, 200, 56, UC),
    "SEARCH":   ("Search (lexical + semantic)",              250, 140, 200, 50, UC),
    "INTERACT": ("Interact (like, comment, repost, save, follow, block, report)", 250, 255, 180, 84, UC),
    "WRITE":    ("Write and publish an article",             250, 420, 200, 50, UC),
    "LIST":     ("List on the marketplace",                  250, 510, 200, 50, UC),
    "AI":       ("Use the AI assistant",                     250, 640, 200, 50, UC),
    "STATS":    ("View analytics and earnings",              250, 352, 200, 50, UC),

    # centre column
    "ACCOUNT":  ("Create an account",                        440, 110, 160, 50, UC),
    "GOOGLE":   ("Sign in with Google",                      625, 110, 160, 50, UC),
    "SIGNIN":   ("Sign in",                                  565, 260, 170, 50, UC),
    "RETRIEVE": ("Retrieve passages from the writer's own corpus", 470, 760, 220, 66, UC),
    "DOCS":     ("Ground answers in uploaded reference documents", 470, 520, 220, 66, UC),

    # right column
    "SUBS":    ("Manage subscription and credits",           860,  60, 200, 56, UC),
    "EVAL":    ("Evaluate a writer and read AI insights",    860, 145, 200, 60, UC),
    "ACQUIRE": ("Acquire an article",                        860, 235, 200, 50, UC),
    "PREVIEW": ("Unlock a preview (10% of the price)",       860, 315, 200, 56, UC),
    "PUBLISH": ("Publish a licensed article",                860, 400, 200, 50, UC),
    "QUEUE":   ("Review the report queue",                   860, 620, 200, 50, UC),
    "USERS":   ("Manage users (search, plan, ban)",          860, 710, 200, 50, UC),
    "GRANT":   ("Grant eligibility manually",                860, 800, 200, 50, UC),

    # external systems, outside the boundary
    "EXT_EMB": ("Embedding provider",                        490, 990, 180, 50, EXT),
    "EXT_LLM": ("Large language model provider",             260, 990, 180, 50, EXT),

}

# (source, target, style, label)
edges = [
    # actor generalisation — specific points up to general, within a group only
    ("A_FREE", "A_VIS",  GEN, ""), ("A_PREM", "A_FREE", GEN, ""),
    ("A_WRIT", "A_FREE", GEN, ""), ("A_ELIG", "A_WRIT", GEN, ""),
    ("A_MSUB", "A_MUN",  GEN, ""),

    # associations
    ("A_VIS", "FEED", ASSOC, ""), ("A_VIS", "SEARCH", ASSOC, ""),
    ("A_VIS", "SIGNIN", ASSOC, ""),
    ("A_FREE", "INTERACT", ASSOC, ""), ("A_PREM", "AI", ASSOC, ""),
    ("A_WRIT", "WRITE", ASSOC, ""), ("A_WRIT", "STATS", ASSOC, ""),
    ("A_ELIG", "LIST", ASSOC, ""),
    ("A_MUN", "SUBS", ASSOC, ""),
    ("A_MSUB", "EVAL", ASSOC, ""), ("A_MSUB", "ACQUIRE", ASSOC, ""),
    ("A_MSUB", "PUBLISH", ASSOC, ""),
    ("A_ADM", "QUEUE", ASSOC, ""), ("A_ADM", "USERS", ASSOC, ""),
    ("A_ADM", "GRANT", ASSOC, ""),

    # every authenticated use case includes Sign in — drawn, not implied
    ("INTERACT", "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("WRITE",    "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("AI",       "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("STATS",    "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("SUBS",     "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("EVAL",     "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("ACQUIRE",  "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("PUBLISH",  "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("QUEUE",    "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("USERS",    "SIGNIN", DASH, "\u00abinclude\u00bb"),
    ("GRANT",    "SIGNIN", DASH, "\u00abinclude\u00bb"),

    # extensions — optional behaviour on a base use case. A visitor without an
    # account reaches registration from the sign-in page, as Google sign-in.
    ("ACCOUNT", "SIGNIN",  DASH, "\u00abextend\u00bb"),
    ("GOOGLE",  "SIGNIN",  DASH, "\u00abextend\u00bb"),
    ("LIST",    "WRITE",   DASH, "\u00abextend\u00bb"),
    ("PREVIEW", "ACQUIRE", DASH, "\u00abextend\u00bb"),
    ("DOCS",    "AI",      DASH, "\u00abextend\u00bb"),

    # a mandatory sub-behaviour
    ("AI", "RETRIEVE", DASH, "\u00abinclude\u00bb"),

    # external systems
    ("RETRIEVE", "EXT_EMB", ASSOC, ""),
    ("AI", "EXT_LLM", ASSOC, ""),
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
