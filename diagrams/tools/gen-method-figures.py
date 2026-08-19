#!/usr/bin/env python3
"""Generate the method and strategy figures as editable .drawio files.

Chapter 1 needs two figures both example reports carry — the Scrum framework and
the waterfall/agile comparison — and chapter 6 needs the shape of the test
strategy. None of them is UML, so colour is allowed here, following the example
report's split: black and white for UML, pastel groups for everything else.
"""
BLUE   = "fillColor=#DAE8FC;strokeColor=#6C8EBF;"
GREEN  = "fillColor=#D5E8D4;strokeColor=#82B366;"
AMBER  = "fillColor=#FFF2CC;strokeColor=#D6B656;"
RED    = "fillColor=#F8CECC;strokeColor=#B85450;"
PURPLE = "fillColor=#E1D5E7;strokeColor=#9673A6;"
GREY   = "fillColor=#F5F5F5;strokeColor=#666666;"
WHITE  = "fillColor=#FFFFFF;strokeColor=#000000;"

GRP  = "rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=13;arcSize=4;"
BOX  = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;align=left;spacingLeft=8;spacingTop=4;fontSize=11;"
HEAD = "rounded=0;whiteSpace=wrap;html=1;fontStyle=1;fontSize=12;"
NOTE = ("shape=note;whiteSpace=wrap;html=1;size=14;fontSize=11;align=left;"
        "verticalAlign=top;spacingLeft=8;spacingTop=4;")
E    = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;"
        "fontSize=10;labelBackgroundColor=#FFFFFF;")
EV = E + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
EH = E + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
EHL= E + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
# upward: leave the top of the lower shape, enter the bottom of the upper one
EU = E + "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;"

def cell(i, label, x, y, w, h, style):
    return (f'<mxCell id="{i}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def edge(i, s, t, label="", style=E, points=None):
    """points: explicit waypoints, for the routes draw.io would otherwise send
    straight through another box."""
    geo = '<mxGeometry relative="1" as="geometry"/>'
    if points:
        pts = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in points)
        geo = ('<mxGeometry relative="1" as="geometry">'
               f'<Array as="points">{pts}</Array></mxGeometry>')
    return (f'<mxCell id="{i}" value="{label}" style="{style}" edge="1" parent="1" '
            f'source="{s}" target="{t}">{geo}</mxCell>')

def write(name, title, cells, w, h):
    xml = ('<mxfile host="Electron" type="device">\n'
           f'  <diagram id="{name}" name="{title}">\n'
           f'    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
           f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
           f'pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">\n'
           '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
           + "\n        ".join(cells) +
           '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    open(f"../{name}/{name}.drawio", "w").write(xml)
    print(f"wrote {name}")

# ── Figure 1.1 — the Scrum framework, as practised here ──────────────────────
c = [
    cell("pb", "Product backlog&lt;br&gt;&lt;br&gt;54 user stories in 8 epics,&lt;br&gt;"
               "ordered by MoSCoW priority,&lt;br&gt;estimated in story points",
         60, 250, 230, 150, BOX + AMBER),
    cell("plan", "Sprint planning&lt;br&gt;&lt;br&gt;pull the next slice,&lt;br&gt;set the sprint goal",
         340, 120, 200, 110, BOX + BLUE),
    cell("sb", "Sprint backlog&lt;br&gt;&lt;br&gt;the stories committed&lt;br&gt;for this sprint",
         340, 280, 200, 120, BOX + AMBER),
    cell("sprint", "Sprint — two weeks", 600, 100, 540, 320, GRP + GREY),
    cell("work", "Daily work&lt;br&gt;&lt;br&gt;build · test · integrate&lt;br&gt;continuously",
         640, 150, 220, 110, BOX + WHITE),
    cell("inc", "Increment&lt;br&gt;&lt;br&gt;verified against the&lt;br&gt;phase exit criteria",
         900, 150, 200, 110, BOX + GREEN),
    cell("review", "Sprint review", 640, 300, 220, 60, BOX + BLUE),
    cell("retro", "Retrospective", 900, 300, 200, 60, BOX + BLUE),
    cell("roles", "The three Scrum roles, and how they collapse here&lt;br&gt;&lt;br&gt;"
                  "Product Owner · Scrum Master · Development Team — on this project all three "
                  "are the same person. The academic supervisor acts as Product Owner at sprint "
                  "boundaries: scope was re-baselined twice on that basis, on 2026-07-26 and "
                  "2026-08-10. Stated in §1.4.2 rather than left implied, because it is the first "
                  "thing an examiner asks about a solo Scrum project.",
         60, 470, 1080, 130, NOTE + AMBER),
    edge("a1", "pb", "plan", "highest priority first", EH),
    edge("a2", "plan", "sb", "commit", EV),
    edge("a3", "sb", "sprint", "", EH),
    edge("a4", "work", "inc", "", EH),
    edge("a5", "inc", "retro", "", EV),
    edge("a6", "review", "pb", "re-order what remains",
         E + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;",
         [(750, 435), (175, 435)]),
]
write("fig-1-1-scrum-framework", "Figure 1.1 - The Scrum framework as practised", c, 1220, 660)

# ── Figure 1.2 — waterfall against agile ─────────────────────────────────────
c = [
    cell("wf", "Classic — sequential phases", 60, 70, 470, 430, GRP + GREY),
    cell("w1", "Requirements", 110, 120, 370, 50, BOX + BLUE),
    cell("w2", "Design", 110, 190, 370, 50, BOX + BLUE),
    cell("w3", "Implementation", 110, 260, 370, 50, BOX + BLUE),
    cell("w4", "Testing", 110, 330, 370, 50, BOX + BLUE),
    cell("w5", "Delivery — once, at the end", 110, 400, 370, 50, BOX + RED),
    cell("ag", "Agile — Scrum, iterative", 610, 70, 530, 430, GRP + GREEN),
    cell("s1", "Sprint 1 — plan · build · verify → increment", 650, 120, 450, 50, BOX + WHITE),
    cell("s2", "Sprint 2 — plan · build · verify → increment", 650, 190, 450, 50, BOX + WHITE),
    cell("s3", "Sprint n — plan · build · verify → increment", 650, 260, 450, 50, BOX + WHITE),
    cell("s4", "Working software every two weeks", 650, 330, 450, 50, BOX + GREEN),
    cell("s5", "Scope absorbed between sprints, not frozen", 650, 400, 450, 50, BOX + AMBER),
    cell("why", "Why Scrum was chosen for this project&lt;br&gt;&lt;br&gt;"
                "The scope moved twice and neither change restarted the work: voice input and "
                "three other features were descoped on 2026-07-26, and deployment was resequenced "
                "on 2026-08-10. A sequential plan would have had to re-open its requirements phase "
                "for both. Each phase also carries written exit criteria, which is what lets every "
                "release chapter show evidence rather than assert completion.",
         60, 540, 1080, 130, NOTE + AMBER),
    edge("b1", "w1", "w2", "", EV), edge("b2", "w2", "w3", "", EV),
    edge("b3", "w3", "w4", "", EV), edge("b4", "w4", "w5", "", EV),
    edge("b5", "s1", "s2", "", EV), edge("b6", "s2", "s3", "", EV),
    edge("b7", "s3", "s4", "", EV),
]
write("fig-1-2-waterfall-vs-agile", "Figure 1.2 - Classic and agile compared", c, 1220, 730)

# ── Figure 6.7 — the test strategy ───────────────────────────────────────────
c = [
    cell("e2e", "End-to-end&lt;br&gt;155 Playwright specs, 23 files&lt;br&gt;real browser, seeded corpus",
         400, 120, 380, 90, HEAD + AMBER),
    cell("int", "Integration through the API&lt;br&gt;auth → publish → purchase → verify the ledger",
         310, 240, 560, 90, HEAD + BLUE),
    cell("unit", "Unit and service tests&lt;br&gt;the bulk of 479 backend tests, run against a real PostgreSQL",
         220, 360, 740, 90, HEAD + GREEN),
    cell("ledger", "Ledger invariant harness&lt;br&gt;&lt;br&gt;27 tests, most of them&lt;br&gt;"
                   "negative: a fixture builds&lt;br&gt;a coherent purchase, then&lt;br&gt;"
                   "corrupts one column and&lt;br&gt;asserts the right invariant fires",
         60, 500, 300, 170, BOX + PURPLE),
    cell("sweep", "Price sweep&lt;br&gt;&lt;br&gt;every value from 1 to 300,&lt;br&gt;"
                  "both stages and both splits,&lt;br&gt;reconciled exactly",
         400, 500, 280, 170, BOX + PURPLE),
    cell("gates", "CI gates — a red build blocks the image", 1000, 120, 200, 330, GRP + GREY),
    cell("g1", "eslint, 0 warnings", 1020, 170, 160, 40, BOX + WHITE),
    cell("g2", "tsc --noEmit", 1020, 220, 160, 40, BOX + WHITE),
    cell("g3", "the test suites", 1020, 270, 160, 40, BOX + WHITE),
    cell("g4", "schema-drift check", 1020, 320, 160, 40, BOX + AMBER),
    cell("g5", "build and push", 1020, 370, 160, 40, BOX + WHITE),
    cell("note", "Validated by sabotage, not by passing: removing the completed-status filter "
                 "from the earnings query fails exactly the pending-payout test, and dropping "
                 "preview_unlock from the debit list fails seven. That exercise found a real "
                 "coverage gap — nothing pinned the grant type filter — which was then closed.",
         720, 500, 480, 170, NOTE + AMBER),
    edge("c1", "unit", "int", "", EU),
    edge("c2", "int", "e2e", "", EU),
]
write("fig-6-7-test-strategy", "Figure 6.7 - Test strategy", c, 1260, 730)
