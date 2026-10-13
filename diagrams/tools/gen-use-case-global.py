#!/usr/bin/env python3
"""Lay out the global use case diagram for an A3 fold-out page.

The content comes from fig-1-11-use-case-global/…puml (merged by
gen-global-figures.py from the three role diagrams). The per-sprint diagrams
stack their actors on the left; with five actors and 65 use cases that makes a
strip far too tall for a page, so this figure is laid out for a wide sheet:

  * the actors in a row above one Inkwell.ai boundary, a parent actor to the
    left of its specialisation, the generalisations drawn actor to actor;
  * under each actor, a column of the use cases it is associated with, joined
    to it by one vertical trunk;
  * beside that column, the use cases they include or are extended by, level
    with their base;
  * the note under the boundary.

  python3 gen-use-case-global.py     # writes fig-1-11-use-case-global.drawio
"""
import html
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAME = 'fig-1-11-use-case-global'

spec = importlib.util.spec_from_file_location('ucgen', os.path.join(HERE, 'gen-use-cases.py'))
ucgen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ucgen)

FONT = 11
CHAR = 6.4            # bold Helvetica advance at 11 px
WRAP = 15             # characters per line in an ellipse
ROW_GAP = 12
DEP_GAP = 86          # between a column of use cases and their targets: room for the labels
ACTOR_GAP = 30        # between two actors' blocks
TRUNK = 26            # trunk to the left of an actor's column
TOP = 125             # the use cases start this far below the actors' tops

S_ACTOR = ucgen.S_ACTOR
S_CASE = ucgen.S_CASE
S_SYS = ucgen.S_SYS
S_NOTE = ucgen.S_NOTE
S_ASSOC = ucgen.EDGE + 'endArrow=none;edgeStyle=none;'
S_GEN = ucgen.EDGE + 'endArrow=block;endFill=0;endSize=12;edgeStyle=none;'
S_DEP = ucgen.EDGE + 'dashed=1;endArrow=open;endSize=10;edgeStyle=none;'


def wrap(text):
    words = text.replace('\n', ' ').split()
    lines, cur = [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > WRAP:
            lines.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    lines.append(cur)
    return '\n'.join(lines)


def ellipse(text):
    lines = text.split('\n')
    return max(104, round(max(len(l) for l in lines) * CHAR + 34)), 30 + 14 * (len(lines) - 1)


def main():
    actors, cases, exts, notes, rels, system = ucgen.parse(os.path.join(ROOT, NAME, f'{NAME}.puml'))
    cases = {k: wrap(v) for k, v in cases.items()}
    dims = {k: ellipse(v) for k, v in cases.items()}

    order = list(actors)                                  # declaration order: VIS, RDR, WRT, MAG, ADM
    direct = {a: [] for a in order}
    for kind, a, b, extra in rels:
        if kind == 'assoc':
            act, uc = (a, b) if a in actors else (b, a)
            direct[act].append(uc)
    owner = {uc: a for a in order for uc in direct[a]}

    # Dependencies: base -> target, with the label to draw.
    deps = []                                             # (base, target, source, dest, label)
    for kind, a, b, extra in rels:
        if kind == 'dep':
            base, target = (a, b) if extra == '«include»' else (b, a)
            deps.append((base, target, a, b, extra))
        elif kind == 'gen' and a in cases:
            deps.append((b, a, a, b, ''))
    targets = {}                                          # actor -> targets in order
    for base, target, *_ in deps:
        if target in owner:
            continue                                      # a target that is also direct stays in its column
        act = owner.get(base) or next(owner[b] for b, t, *_ in deps if t == base)
        owner[target] = act
        targets.setdefault(act, [])
        if target not in targets[act]:
            targets[act].append(target)

    # Columns.
    pos = {}
    x = 0
    blocks = {}
    for act in order:
        col = direct[act]
        dw = max(dims[u][0] for u in col)
        dx = x + TRUNK
        y = TOP
        for u in col:
            pos[u] = (dx + (dw - dims[u][0]) / 2, y)
            y += dims[u][1] + ROW_GAP
        bottom = y
        tw = 0
        tx = dx + dw + DEP_GAP
        if targets.get(act):
            tw = max(dims[t][0] for t in targets[act])
            # Each target level with the mean of its bases, then pushed apart.
            want = {}
            for t in targets[act]:
                bys = [pos[b][1] + dims[b][1] / 2 for b, tt, *_ in deps if tt == t and b in pos]
                want[t] = sum(bys) / len(bys) - dims[t][1] / 2 if bys else TOP
            ty = TOP
            for t in sorted(targets[act], key=lambda t: want[t]):
                y0 = max(ty, want[t])
                pos[t] = (tx + (tw - dims[t][0]) / 2, y0)
                ty = y0 + dims[t][1] + ROW_GAP
            bottom = max(bottom, ty)
        blocks[act] = (x, dx, dw, tx, tw, bottom)
        x = (tx + tw if tw else dx + dw) + ACTOR_GAP

    width = x - ACTOR_GAP
    height = max(b[5] for b in blocks.values())

    cells = []
    esc = lambda t: html.escape(t, quote=True).replace('\n', '&lt;br&gt;')
    pad = 22
    sys_x0, sys_y0 = -pad + TRUNK - 14, TOP - 34
    cells.append(f'<mxCell id="system" value="{esc(system or "Inkwell.ai")}" style="{S_SYS}" vertex="1" '
                 f'parent="1"><mxGeometry x="{sys_x0:.0f}" y="{sys_y0:.0f}" '
                 f'width="{width - sys_x0 + pad:.0f}" height="{height - sys_y0 + pad - ROW_GAP:.0f}" '
                 f'as="geometry"/></mxCell>')

    # Actors, above their trunk.
    apos = {}
    for act in order:
        _, dx, *_ = blocks[act]
        trunk_x = dx - TRUNK / 2 - 6
        apos[act] = (trunk_x - 15, 0)
        cells.append(f'<mxCell id="{act}" value="{esc(actors[act])}" style="{S_ACTOR}" vertex="1" '
                     f'parent="1"><mxGeometry x="{trunk_x - 15:.0f}" y="0" width="30" height="60" '
                     f'as="geometry"/></mxCell>')
    for u, (ux, uy) in pos.items():
        w, h = dims[u]
        cells.append(f'<mxCell id="{u}" value="{esc(cases[u])}" style="{S_CASE}" vertex="1" '
                     f'parent="1"><mxGeometry x="{ux:.0f}" y="{uy:.0f}" width="{w}" height="{h}" '
                     f'as="geometry"/></mxCell>')

    def edge(eid, s, t, style, label='', pts=(), lx=None):
        geo_x = f' x="{lx:.3f}"' if lx is not None else ''
        arr = ''.join(f'<mxPoint x="{px:.0f}" y="{py:.0f}"/>' for px, py in pts)
        cells.append(f'<mxCell id="{eid}" value="{esc(label)}" style="{style}" edge="1" parent="1" '
                     f'source="{s}" target="{t}"><mxGeometry{geo_x} relative="1" as="geometry">'
                     f'<Array as="points">{arr}</Array></mxGeometry></mxCell>')

    # Associations: down the actor's trunk, then into the use case's left end.
    n = 0
    for act in order:
        trunk_x = apos[act][0] + 15
        for u in direct[act]:
            uy = pos[u][1] + dims[u][1] / 2
            edge(f'a{n}', act, u, S_ASSOC + 'exitX=0.5;exitY=1;exitDx=0;exitDy=0;'
                 'entryX=0;entryY=0.5;entryDx=0;entryDy=0;', pts=[(trunk_x, uy)])
            n += 1

    # Generalisations between actors, along the top.
    for kind, a, b, extra in rels:
        if kind == 'gen' and a in actors:
            edge(f'g{n}', a, b, S_GEN + 'exitX=0;exitY=0.3;exitDx=0;exitDy=0;'
                 'entryX=1;entryY=0.3;entryDx=0;entryDy=0;')
            n += 1

    # Dependencies: from the base's right end, turn in a lane of the gap,
    # enter the target's left end. Ports on a target are spread by base.
    by_target = {}
    for d in deps:
        by_target.setdefault(d[1], []).append(d)
    lanes = {}
    for act in order:
        _, dx, dw, tx, *_ = blocks[act]
        mine = [d for d in deps if owner.get(d[0]) == act and d[0] in direct[act]]
        mine.sort(key=lambda d: (pos[d[0]][1], pos[d[1]][1]))
        lo, hi = dx + dw + 12, tx - 12
        for r, d in enumerate(mine):
            lanes[d] = lo + (hi - lo) * (r + 1) / (len(mine) + 1)
    for t, ds in by_target.items():
        ds.sort(key=lambda d: pos[d[0]][1])
        for r, (base, target, src, dst, label) in enumerate(ds):
            ty = pos[target][1] + dims[target][1] * (r + 1) / (len(ds) + 1)
            by = pos[base][1] + dims[base][1] / 2
            if (base, target, src, dst, label) in lanes:
                lx = lanes[(base, target, src, dst, label)]
                pts = [(lx, by), (lx, ty)]
                ex, ey = 1, 0.5
                nx, ny = 0, (r + 1) / (len(ds) + 1)
            else:                                         # a target below its base, in the same column
                pts = []
                ex, ey, nx, ny = 0.5, 1, 0.5, 0
            # The edge goes from the declaring end; flip the ports for «extend».
            if src == base:
                sty = (f'exitX={ex};exitY={ey};exitDx=0;exitDy=0;entryX={nx};entryY={ny:.3f};'
                       'entryDx=0;entryDy=0;')
                path = pts
            else:
                sty = (f'exitX={nx};exitY={ny:.3f};exitDx=0;exitDy=0;entryX={ex};entryY={ey};'
                       'entryDx=0;entryDy=0;')
                path = list(reversed(pts))
            # The label goes on the horizontal stretch next to the target, the longer one.
            edge(f'd{n}', src, dst, S_DEP + sty, label, path, lx=0.55 if src == base else -0.55)
            n += 1

    # Note under the boundary, at the right.
    for k, (nid, note) in enumerate(notes.items()):
        words, lines, cur = note['text'].split(), [], ''
        for w in words:
            if cur and len(cur) + 1 + len(w) > 70:
                lines.append(cur); cur = w
            else:
                cur = f'{cur} {w}'.strip()
        lines.append(cur)
        w = round(max(len(l) for l in lines) * 6.0 + 30)
        h = 16 * len(lines) + 14
        cells.append(f'<mxCell id="note{k}" value="{esc(chr(10).join(lines))}" style="{S_NOTE}" vertex="1" '
                     f'parent="1"><mxGeometry x="{width + pad - w:.0f}" y="{height + pad + 14:.0f}" '
                     f'width="{w}" height="{h}" as="geometry"/></mxCell>')

    xml = ('<mxfile host="Electron" type="device">\n'
           f'  <diagram id="{NAME}" name="{NAME}">\n'
           '    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
           'connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0">\n'
           '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
           + '\n        '.join(cells) +
           '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    with open(os.path.join(ROOT, NAME, f'{NAME}.drawio'), 'w') as f:
        f.write(xml)
    print(f'wrote {NAME}.drawio ({width:.0f} × {height:.0f} px)')


if __name__ == '__main__':
    main()
