#!/usr/bin/env python3
"""Lay out the use case diagrams as .drawio files, from their PlantUML sources.

The .puml file stays the source of the content — actors, use cases, relations
and notes. What Graphviz could not give these diagrams is a fixed shape: it
moved actors above, below or between the use cases, and routed one actor's
links across another's. This script fixes the layout instead:

  * the actors are stacked in one column on the left, a parent actor above its
    specialisations;
  * the use cases are arranged in columns to the right, each one column further
    than the actor, parent, base or including use case it hangs from;
  * external systems sit in a last column, outside the system boundary;
  * a link that spans columns passes through a waypoint in each, so it runs
    between use cases rather than through them;
  * each column is ordered by the position of its neighbours (barycentre
    sweeps), keeping the order with the fewest crossings;
  * notes are set under the boundary; a note that was attached to a use case
    by a line names it in its text instead.

  python3 gen-use-cases.py            # every */fig-*-use-case-*/ folder
  python3 gen-use-cases.py fig-4-1-use-case-sprint-1

Black on white, like the PlantUML figures (diagrams/_style.puml): only the
notes are coloured.
"""
import glob
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

FONT = "fontFamily=Helvetica;fontColor=#000000;"
S_ACTOR = ("shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;"
           "fillColor=#FFFFFF;strokeColor=#000000;fontStyle=1;fontSize=12;" + FONT)
S_CASE = ("ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
          "fontStyle=1;fontSize=11;" + FONT)
S_EXT = ("rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
         "fontStyle=1;fontSize=11;" + FONT)
S_SYS = ("rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#000000;"
         "verticalAlign=top;fontStyle=1;fontSize=12;" + FONT)
S_NOTE = ("shape=note;whiteSpace=wrap;html=1;size=10;fillColor=#FFF2CC;strokeColor=#D6B656;"
          "align=left;verticalAlign=top;spacingLeft=6;spacingTop=2;fontStyle=2;fontSize=11;" + FONT)
EDGE = "html=1;rounded=0;strokeColor=#000000;fontSize=10;labelBackgroundColor=#FFFFFF;" + FONT
S_ASSOC = EDGE + "endArrow=none;"
S_ASSOC_ARROW = EDGE + "endArrow=open;endSize=10;"
S_GEN = EDGE + "endArrow=block;endFill=0;endSize=12;"
S_DEP = EDGE + "dashed=1;endArrow=open;endSize=10;"

COL_GAP = 130       # between columns: room for «extend» and its [condition]
ROW_GAP = 16        # between use cases in one column
ACTOR_GAP = 50
PAD = 24            # inside the system boundary
TITLE = 22          # boundary title band, when the boundary is named

REL = re.compile(r'^(\w+)\s+(<\|--|--\|>|-\|>|-left-\|>|-->|--|\.\.>|<\.\.|<\.right\.|\.\.|'
                 r'-\[hidden\]\w*-)\s+(\w+)(?:\s*:\s*(.*))?$')


def clean(text):
    """PlantUML label text to plain lines."""
    text = text.strip().strip('"').replace('\\n', '\n')
    return text.replace('<<', '«').replace('>>', '»')


def wrap(text, width=22):
    """Two balanced lines for a long single-line name, so that one long
    use case does not widen its whole column."""
    if '\n' in text or len(text) <= width:
        return text
    words = text.split()
    best = min(range(1, len(words)),
               key=lambda i: abs(len(' '.join(words[:i])) - len(' '.join(words[i:]))))
    return ' '.join(words[:best]) + '\n' + ' '.join(words[best:])


def parse(path):
    actors, cases, exts, notes, rels = {}, {}, {}, {}, []
    system = None
    lines = open(path).read().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("'") or line.startswith('@') or line.startswith('!'):
            continue
        if re.match(r'skinparam \w+ \{', line):             # a skinparam block
            while not lines[i].strip() == '}':
                i += 1
            i += 1
            continue
        if line.startswith(('skinparam', 'left to right', 'top to bottom', 'hide')) or line == '}':
            continue
        if m := re.match(r'actor "(.+?)" as (\w+)$', line):
            actors[m[2]] = clean(m[1]); continue
        if m := re.match(r'usecase "(.+?)" as (\w+)$', line):
            cases[m[2]] = wrap(clean(m[1])); continue
        if m := re.match(r'rectangle(?: "(.+?)")? \{$', line):
            system = clean(m[1]) if m[1] else ''; continue
        if m := re.match(r'rectangle "(.+?)" as (\w+)$', line):
            exts[m[2]] = clean(m[1]); continue
        if m := re.match(r'note as (\w+)$', line):
            body = []
            while lines[i].strip() != 'end note':
                body.append(lines[i].strip()); i += 1
            i += 1
            notes[m[1]] = {'text': ' '.join(body), 'on': None}; continue
        if m := re.match(r'note "(.+?)" as (\w+)$', line):
            notes[m[2]] = {'text': clean(m[1]).replace('\n', ' '), 'on': None}; continue
        if m := re.match(r'note (?:right|left|top|bottom) of (\w+) : (.+)$', line):
            notes[f'_on_{m[1]}'] = {'text': clean(m[2]), 'on': m[1]}; continue
        if m := REL.match(line):
            a, op, b, label = m[1], m[2], m[3], clean(m[4]) if m[4] else ''
            if 'hidden' in op:
                continue
            if op == '..' and a in notes:                   # a note attached by a line
                notes[a]['on'] = b; continue
            if op in ('<|--',):
                rels.append(('gen', b, a, ''))              # child, parent
            elif op in ('--|>', '-|>', '-left-|>'):
                rels.append(('gen', a, b, ''))
            elif op == '..>':
                rels.append(('dep', a, b, label))           # base includes target
            elif op in ('<..', '<.right.'):
                rels.append(('dep', b, a, label))           # extender points at base
            elif op in ('--', '-->'):
                rels.append(('assoc', a, b, op))
            continue
        raise SystemExit(f'{path}: cannot read line: {line!r}')
    return actors, cases, exts, notes, rels, system


def size(text, bold_px=6.9):
    lines = text.split('\n')
    longest = max(len(l) for l in lines)
    return max(110, int(longest * bold_px) + 44), 34 + 14 * (len(lines) - 1)


def layout(actors, cases, exts, rels):
    """Columns, order and coordinates. Returns positions and edge waypoints."""
    # Rightward relations: (left node, right node).
    right = []
    for kind, a, b, extra in rels:
        if kind == 'assoc':
            if a in actors or b in actors:
                act, uc = (a, b) if a in actors else (b, a)
                right.append((act, uc))
            else:                                          # use case — external
                uc, ex = (a, b) if b in exts else (b, a)
                right.append((uc, ex))
        elif kind == 'gen' and a in cases:
            right.append((b, a))                            # parent left, child right
        elif kind == 'dep':
            base, other = (a, b) if extra == '«include»' else (b, a)
            right.append((base, other))

    # Columns by longest path from the actors (cycles cut by visit order).
    col = {a: 0 for a in actors}
    for _ in range(len(cases) + 2):
        changed = False
        for u, v in right:
            if v in exts or u not in col:
                continue
            if col.get(v, -1) < col[u] + 1 and col[u] + 1 <= len(cases):
                col[v] = col[u] + 1; changed = True
        if not changed:
            break
    for c in cases:
        col.setdefault(c, 1)
    last = max([col[c] for c in cases] + [1])
    for e in exts:
        col[e] = last + 1

    # Actor order: declaration order, a parent above its specialisations.
    gen_actor = [(a, b) for k, a, b, _ in rels if k == 'gen' and a in actors]
    children = {a: [c for c, p in gen_actor if p == a] for a in actors}
    roots = [a for a in actors if not any(c == a for c, _ in gen_actor)]
    actor_order = []
    def visit(a):
        if a not in actor_order:
            actor_order.append(a)
            for c in children[a]:
                visit(c)
    for a in roots:
        visit(a)
    for a in actors:
        visit(a)

    # Split long edges with dummy waypoints, one per column crossed.
    layers = {k: [] for k in range(last + 2)}
    layers[0] = actor_order
    nodes = [n for n in list(cases) + list(exts) if n in col]
    for n in sorted(nodes, key=lambda n: list(cases).index(n) if n in cases else 999):
        layers[col[n]].append(n)
    adj = {}                                               # undirected, adjacent columns only
    chains = {}
    def link(p, q):
        adj.setdefault(p, []).append(q); adj.setdefault(q, []).append(p)
    for idx, (u, v) in enumerate(right):
        cu, cv = col[u], col[v]
        lo, hi = (u, v) if cu < cv else (v, u)
        path = [lo]
        for k in range(min(cu, cv) + 1, max(cu, cv)):
            d = f'_d{idx}_{k}'
            layers[k].append(d); col[d] = k; path.append(d)
        path.append(hi)
        for p, q in zip(path, path[1:]):
            link(p, q)
        chains[(u, v)] = path

    def pos_of(layer):
        return {n: i for i, n in enumerate(layer)}

    def crossings():
        total = 0
        for k in range(len(layers) - 1):
            p, q = pos_of(layers[k]), pos_of(layers[k + 1])
            es = [(p[a], q[b]) for a in layers[k] for b in adj.get(a, []) if b in q]
            total += sum(1 for i, (a1, b1) in enumerate(es) for a2, b2 in es[i + 1:]
                         if (a1 - a2) * (b1 - b2) < 0)
        return total

    best, best_layers = crossings(), {k: list(v) for k, v in layers.items()}
    for sweep in range(12):
        ks = range(1, len(layers)) if sweep % 2 == 0 else range(len(layers) - 2, 0, -1)
        for k in ks:
            ref = pos_of(layers[k - 1] if sweep % 2 == 0 else layers[k + 1])
            here = pos_of(layers[k])
            def bary(n):
                ns = [ref[m] for m in adj.get(n, []) if m in ref]
                return sum(ns) / len(ns) if ns else here[n]
            if k == 1 and sweep % 2:
                left = pos_of(layers[0])
                def bary0(n):
                    ns = [left[m] for m in adj.get(n, []) if m in left]
                    return sum(ns) / len(ns) if ns else here[n]
                layers[k].sort(key=lambda n: (bary0(n), bary(n), here[n]))
            else:
                layers[k].sort(key=lambda n: (bary(n), here[n]))
        c = crossings()
        if c < best:
            best, best_layers = c, {k: list(v) for k, v in layers.items()}
    layers = best_layers

    # Sizes.
    dims = {}
    for a in actors:
        dims[a] = (30, 60 + 18)                            # figure plus its name
    for c, t in cases.items():
        dims[c] = size(t)
    for e, t in exts.items():
        w, h = size(t)
        dims[e] = (w - 10, h + 12)
    for k, layer in layers.items():
        for n in layer:
            dims.setdefault(n, (0, 10))                    # waypoints reserve a lane

    # One width per column, so ellipse ends line up and a line leaving or
    # entering a column never grazes a neighbour.
    for k, layer in layers.items():
        uc = [n for n in layer if n in cases]
        if uc:
            w = max(dims[n][0] for n in uc)
            for n in uc:
                dims[n] = (w, dims[n][1])

    # Vertical placement: towards the neighbours, never overlapping.
    y = {}
    for k, layer in layers.items():
        acc = 0
        for n in layer:
            gap = ACTOR_GAP if k == 0 else ROW_GAP
            y[n] = acc + dims[n][1] / 2
            acc += dims[n][1] + gap
    def place(layer, want, gap):
        """Closest positions to `want` that keep the order and the spacing:
        isotonic regression (pool adjacent violators) on the positions minus
        their minimum offsets. Exact, so repeated passes do not drift."""
        off, acc = [], 0.0
        for i, n in enumerate(layer):
            if i:
                p = layer[i - 1]
                acc += dims[p][1] / 2 + gap + dims[n][1] / 2
            off.append(acc)
        blocks = []                                        # [mean, count]
        for i, n in enumerate(layer):
            blocks.append([want[n] - off[i], 1])
            while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
                m2, c2 = blocks.pop(); m1, c1 = blocks.pop()
                blocks.append([(m1 * c1 + m2 * c2) / (c1 + c2), c1 + c2])
        i = 0
        for m, c in blocks:
            for _ in range(c):
                y[layer[i]] = m + off[i]; i += 1

    def settle(layer, gap):
        for i in range(1, len(layer)):
            a, b = layer[i - 1], layer[i]
            low = y[a] + dims[a][1] / 2 + gap + dims[b][1] / 2
            if y[b] < low:
                y[b] = low
    for it in range(30):
        ks = list(range(len(layers))) if it % 2 else list(range(len(layers) - 1, -1, -1))
        for k in ks:
            layer = layers[k]
            if not layer:
                continue
            gap = ACTOR_GAP if k == 0 else ROW_GAP
            want = {n: (sum(y[m] for m in adj.get(n, [])) / len(adj[n])) if adj.get(n) else y[n]
                    for n in layer}
            place(layer, want, gap)
    top = min(y[n] - dims[n][1] / 2 for n in y)
    for n in y:
        y[n] -= top

    # Columns left to right.
    x, cx = {}, 0
    for k in range(len(layers)):
        layer = layers[k]
        width = max([dims[n][0] for n in layer] + [0])
        for n in layer:
            x[n] = cx + width / 2
        cx += width + (COL_GAP if k else COL_GAP + 20)
    colw = {n: max([dims[m][0] for m in layers[col[n]]] + [0]) for n in col if n in x}
    return x, y, dims, chains, actor_order, colw


def build(name):
    folder = os.path.join(ROOT, name)
    actors, cases, exts, notes, rels, system = parse(os.path.join(folder, f'{name}.puml'))
    x, y, dims, chains, actor_order, colw = layout(actors, cases, exts, rels)

    # Leave room for the boundary title and padding above everything.
    shift = PAD + (TITLE if system else 0) + 10
    for n in y:
        y[n] += shift

    cells = []
    def esc(t):
        return html.escape(t, quote=True).replace('\n', '&lt;br&gt;')
    def vertex(i, label, style, n):
        w, h = dims[n]
        cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x[n] - w / 2:.0f}" y="{y[n] - h / 2:.0f}" width="{w}" '
                     f'height="{h if n not in actors else 60}" as="geometry"/></mxCell>')

    # System boundary around every use case and the waypoints between them.
    inner = [n for n in x if n not in actors and n not in exts]
    if inner:
        x0 = min(x[n] - dims[n][0] / 2 for n in inner) - PAD
        x1 = max(x[n] + dims[n][0] / 2 for n in inner) + PAD
        y0 = min(y[n] - dims[n][1] / 2 for n in inner) - PAD - (TITLE if system else 0)
        y1 = max(y[n] + dims[n][1] / 2 for n in inner) + PAD
        cells.append(f'<mxCell id="system" value="{esc(system or "")}" style="{S_SYS}" vertex="1" parent="1">'
                     f'<mxGeometry x="{x0:.0f}" y="{y0:.0f}" width="{x1 - x0:.0f}" height="{y1 - y0:.0f}" '
                     f'as="geometry"/></mxCell>')
    else:
        y1 = max(y.values())

    for a in actors:
        vertex(a, actors[a], S_ACTOR, a)
    for c in cases:
        vertex(c, cases[c], S_CASE, c)
    for e in exts:
        vertex(e, exts[e], S_EXT, e)

    def points(u, v):
        path = chains.get((u, v)) or list(reversed(chains.get((v, u), [])))
        mids = [p for p in path if p.startswith('_d')]
        flip = bool(path) and path[0] != u
        if flip:
            mids = list(reversed(mids))
        # Cross each column horizontally, in the waypoint's own lane, so the
        # line never cuts the corner of a use case beside the lane.
        out = []
        for p in mids:
            l, r = x[p] - colw[p] / 2, x[p] + colw[p] / 2
            for px in ((r, l) if flip else (l, r)):
                out.append(f'<mxPoint x="{px:.0f}" y="{y[p]:.0f}"/>')
        return ''.join(out)

    def edge(i, s, t, style, label='', pts=''):
        # Leave the left-hand shape at its right end and enter the right-hand
        # one at its left end: with the columns' ends aligned, no line crosses
        # a neighbouring use case on its way in or out.
        if 'exitX' not in style and abs(x[s] - x[t]) > 1:
            sx, tx = (1, 0) if x[s] < x[t] else (0, 1)
            style += (f'exitX={sx};exitY=0.5;exitDx=0;exitDy=0;'
                      f'entryX={tx};entryY=0.5;entryDx=0;entryDy=0;')
        # A label sits toward the right-hand end, where the lines fan out,
        # not at the base where several of them converge.
        lx = (' x="-0.25"' if x[s] > x[t] else ' x="0.25"') if label else ''
        geo = (f'<mxGeometry{lx} relative="1" as="geometry"><Array as="points">{pts}</Array></mxGeometry>'
               if pts else f'<mxGeometry{lx} relative="1" as="geometry"/>')
        cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" edge="1" parent="1" '
                     f'source="{s}" target="{t}">{geo}</mxCell>')

    for idx, (kind, a, b, extra) in enumerate(rels):
        eid = f'e{idx}'
        if kind == 'assoc':
            if a in actors or b in actors:
                act, uc = (a, b) if a in actors else (b, a)
                style = S_ASSOC_ARROW if extra == '-->' else S_ASSOC
                edge(eid, act, uc, style, pts=points(act, uc))
            else:
                uc, ex = (a, b) if b in exts else (b, a)
                edge(eid, uc, ex, S_ASSOC, pts=points(uc, ex))
        elif kind == 'gen' and a in actors:
            # Stacked actors: leave the child on its left, run up the left of the
            # column and enter the parent from the side, clear of the names.
            lx = x[a] - 34
            ya, yb = y[a] - 9, y[b] - 9                     # the figures' chests
            pts = f'<mxPoint x="{lx:.0f}" y="{ya:.0f}"/><mxPoint x="{lx:.0f}" y="{yb:.0f}"/>'
            side = ('exitX=0;exitY=0.5;exitDx=0;exitDy=0;'
                    'entryX=0;entryY=0.5;entryDx=0;entryDy=0;')
            edge(eid, a, b, S_GEN + side, pts=pts)
        elif kind == 'gen':
            edge(eid, a, b, S_GEN, pts=points(b, a))
        else:
            base, other = (a, b) if extra == '«include»' else (b, a)
            pts = points(base, other)
            edge(eid, a, b, S_DEP, extra, pts)

    # Notes under the boundary, left to right, wrapping at the drawing's width.
    right_edge = max(x[n] + dims[n][0] / 2 for n in x)
    nx, ny, row_h = 0, y1 + 24, 0
    for nid, note in notes.items():
        text = note['text']
        if note['on']:
            target = (cases.get(note['on']) or actors.get(note['on']) or note['on']).replace('\n', ' ')
            text = f'«{target}»: {text}'
        words, lines_, cur = text.split(), [], ''
        for w in words:
            if len(cur) + len(w) + 1 > 52 and cur:
                lines_.append(cur); cur = w
            else:
                cur = f'{cur} {w}'.strip()
        lines_.append(cur)
        w = max(160, int(max(len(l) for l in lines_) * 6.2) + 30)
        h = 16 * len(lines_) + 14
        if nx and nx + w > right_edge:
            nx, ny, row_h = 0, ny + row_h + 14, 0
        cells.append(f'<mxCell id="note_{nid}" value="{esc(chr(10).join(lines_))}" style="{S_NOTE}" '
                     f'vertex="1" parent="1"><mxGeometry x="{nx:.0f}" y="{ny:.0f}" width="{w}" '
                     f'height="{h}" as="geometry"/></mxCell>')
        nx += w + 16
        row_h = max(row_h, h)

    xml = ('<mxfile host="Electron" type="device">\n'
           f'  <diagram id="{name}" name="{name}">\n'
           '    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
           'connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0">\n'
           '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
           + '\n        '.join(cells) +
           '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    with open(os.path.join(folder, f'{name}.drawio'), 'w') as f:
        f.write(xml)
    print(f'wrote {name}.drawio')


if __name__ == '__main__':
    names = sys.argv[1:] or sorted(os.path.basename(os.path.dirname(p))
                                   for p in glob.glob(os.path.join(ROOT, 'fig-*-use-case-*', '*.puml')))
    for n in names:
        build(n)
