#!/usr/bin/env python3
"""Lay out the complete class diagram on a grid, for an A3 fold-out page.

Two versions of this figure are kept side by side:

  fig-1-12-classes-global-friend-layout.drawio   version A: laid out by hand in
      draw.io. It is also the CONTENT SOURCE of this script: the classes, their
      attributes and operations, and the enumerations are read from it.
  fig-1-12-classes-global.drawio                  version B: written by this
      script, and the one the report uses.

The associations are listed below (they follow src/database/schema/ in the
backend), with each join table drawn as a class between its two ends.

The grid: User in the middle and Article to its right; the classes associated
with User only on the left; those between User and Article in the middle
columns; those of Article only on the right; the enumerations fill the space
left under the shorter columns. Every association is routed here, orthogonally
and out of the boxes: a line leaves its class from the side facing the other
one, turns in the gap between two columns in a lane of its own, and crosses a
column only through a gap between two of its classes. (The draw.io desktop
installed here has no obstacle-avoiding router.)

To go back to version A in the report, copy the friend-layout file over
fig-1-12-classes-global.drawio and stop running this script (make regen).

  python3 gen-class-global.py
"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAME = 'fig-1-12-classes-global'

FONT = 11
CHAR = 5.6           # average Helvetica advance at 11 px, measured on the labels
LINE = 14            # line height of a member
PAD = 8

# Grid: columns from left to right, each a list of classes stacked top-down.
COLUMNS = [
    ['MagazineProfile', 'MagazineSubscription', 'EligibilityAuditLog', 'Notification', 'Report', 'Follow'],
    ['WriterMemory', 'PortfolioInsight', 'WriterAudienceMetrics', 'WriterContentMetrics', 'WriterQualityMetrics', 'Block'],
    ['User', 'Transaction'],
    ['Comment', 'CommentLike', 'Like', 'Repost', 'Save', 'AiInteraction', 'DocumentChunk'],
    ['Purchase', 'AnalyticsEvent', 'Document'],
    ['Article', 'ArticleDocument'],
    ['ArticleTag', 'Tag', 'ArticleChunk', 'ArticleMetrics'],
]
COL_GAP = [70, 80, 130, 100, 110, 70]      # gaps after each column: room for their lanes
ROW_GAP = 34
ENUM_GAP = 16                        # between enumerations in the band
BAND_GAP = 60                        # between the classes and the band

S_CLASS = ('rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=6;'
           'spacingRight=4;spacingTop=0;fontSize=%d;fontFamily=Helvetica;fontColor=#000000;'
           'strokeColor=#000000;fillColor=#FFFFFF;' % FONT)
S_ENUM = S_CLASS.replace('fillColor=#FFFFFF', 'fillColor=#DAE8FC')
S_EDGE = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=none;strokeColor=#000000;'
          'fontSize=10;fontFamily=Helvetica;fontColor=#000000;labelBackgroundColor=#FFFFFF;')
S_END = ('edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];'
         'fontSize=10;fontFamily=Helvetica;labelBackgroundColor=none;')


def parse():
    import xml.etree.ElementTree as ET
    src = os.environ.get('CLASS_SRC') or os.path.join(ROOT, NAME, f'{NAME}-friend-layout.drawio')
    root = ET.parse(src).getroot().find('.//root')
    items = {}
    for el in root:
        cell = el if el.tag == 'mxCell' else el.find('mxCell')
        lab = el.get('value') if el.tag == 'mxCell' else el.get('label')
        items[el.get('id')] = (cell, html.unescape(re.sub('<[^>]+>', ' ', lab or '')).replace('\xa0', ' ').strip())
    classes = {}
    for i, (c, lab) in items.items():
        if c is None or 'swimlane' not in (c.get('style') or ''):
            continue
        enum = lab.startswith('«Enumeration»')
        name = lab.replace('«Enumeration»', '').strip()
        rows = sorted(((float(cc.find('mxGeometry').get('y')), l) for cc, l in items.values()
                       if cc is not None and cc.get('parent') == i and l and (cc.get('style') or '').startswith('text;')), key=lambda r: r[0])
        classes[name] = {'enum': enum, 'members': [l for _, l in rows]}
    J = 'Like Repost Save ArticleTag CommentLike Follow Block ArticleDocument'.split()
    rels = [
        ('User', '1', '0..1', 'MagazineProfile', 'extends'),
        ('User', '1', '0..*', 'Article', 'writes'),
        ('User', '0..1', '0..*', 'Article', 'publishes'),
        ('User', '1', '0..*', 'Comment', 'posts'),
        ('User', '1', '0..*', 'Notification', 'receives'),
        ('User', '0..1', '0..*', 'Report', 'files'),
        ('User', '0..1', '0..*', 'Report', 'resolves'),
        ('Article', '1', '0..*', 'Comment', 'carries'),
        ('Comment', '0..1', '0..*', 'Comment', 'replies to'),
        ('User', '1', '0..*', 'Like', 'likes'), ('Article', '1', '0..*', 'Like', None),
        ('User', '1', '0..*', 'Repost', 'reposts'), ('Article', '1', '0..*', 'Repost', None),
        ('User', '1', '0..*', 'Save', 'saves'), ('Article', '1', '0..*', 'Save', None),
        ('User', '1', '0..*', 'CommentLike', 'likes'), ('Comment', '1', '0..*', 'CommentLike', None),
        ('User', '1', '0..*', 'Follow', 'follows'), ('User', '1', '0..*', 'Follow', 'is followed'),
        ('User', '1', '0..*', 'Block', 'blocks'), ('User', '1', '0..*', 'Block', 'is blocked'),
        ('Article', '1', '0..*', 'ArticleTag', 'is tagged with'), ('Tag', '1', '0..*', 'ArticleTag', None),
        ('Article', '1', '0..*', 'ArticleChunk', 'is chunked into'),
        ('User', '1', '0..1', 'WriterMemory', 'has voice profile'),
        ('User', '1', '0..1', 'PortfolioInsight', 'has insights'),
        ('User', '1', '0..*', 'AiInteraction', 'requests'),
        ('Article', '0..1', '0..*', 'AiInteraction', 'concerns'),
        ('User', '1', '0..*', 'Document', 'owns'),
        ('Document', '1', '0..*', 'DocumentChunk', 'is chunked into'),
        ('Article', '1', '0..*', 'ArticleDocument', 'is grounded in'), ('Document', '1', '0..*', 'ArticleDocument', None),
        ('Article', '1', '0..*', 'Purchase', 'is licensed in'),
        ('User', '1', '0..*', 'Purchase', 'buys'),
        ('Purchase', '0..1', '0..1', 'Purchase', 'prior preview'),
        ('Purchase', '1', '2..3', 'Transaction', 'records'),
        ('User', '0..1', '0..*', 'Transaction', 'from'),
        ('User', '0..1', '0..*', 'Transaction', 'to'),
        ('Article', '0..1', '0..*', 'Transaction', 'concerns'),
        ('User', '1', '0..*', 'MagazineSubscription', 'subscribes'),
        ('MagazineSubscription', '0..1', '0..1', 'MagazineSubscription', 'renews'),
        ('User', '1', '0..*', 'EligibilityAuditLog', 'qualifies'),
        ('User', '0..1', '0..*', 'EligibilityAuditLog', 'grants'),
        ('Article', '1', '0..*', 'AnalyticsEvent', 'generates'),
        ('User', '0..1', '0..*', 'AnalyticsEvent', 'views'),
        ('Article', '1', '0..1', 'ArticleMetrics', 'is measured by'),
        ('User', '1', '0..1', 'WriterAudienceMetrics', 'is measured by'),
        ('User', '1', '0..1', 'WriterContentMetrics', 'is measured by'),
        ('User', '1', '0..1', 'WriterQualityMetrics', 'is measured by'),
    ]
    missing = {a for a, *_ in rels} | {b for *_, b, _ in rels}
    assert missing <= set(classes), missing - set(classes)
    return classes, rels


def label(name, c):
    esc = lambda t: html.escape(t, quote=False)
    head = (f'<div style="text-align:center;padding-top:3px">'
            + ('«Enumeration»<br>' if c['enum'] else '')
            + f'<b>{esc(name)}</b></div>')
    if c['enum']:
        return head + '<hr style="margin:3px 0">' + '<br>'.join(esc(m) for m in c['members'])
    attrs = [m for m in c['members'] if '(' not in m]
    ops = [m for m in c['members'] if '(' in m]
    out = head + '<hr style="margin:3px 0">' + '<br>'.join(esc(m) for m in attrs)
    if ops:
        out += '<hr style="margin:3px 0">' + '<br>'.join(esc(m) for m in ops)
    return out


def size(name, c):
    width = max([len(name) * (CHAR + 1.2)] + [len(m) * CHAR for m in c['members']]) + 2 * PAD + 6
    if c['enum']:
        width = max(width, len('«Enumeration»') * CHAR + 2 * PAD)
    lines = len(c['members']) + (2 if c['enum'] else 1)
    seps = 1 if c['enum'] else (2 if any('(' in m for m in c['members']) else 1)
    return round(width), round(lines * LINE + seps * 8 + 12)


def route(rels, pos, dims):
    """Orthogonal routes for every association. Returns, per association, its
    id, ends, role, multiplicities, waypoints and port style."""
    col_of = {n: i for i, col in enumerate(COLUMNS) for n in col}
    box = {n: (pos[n][0], pos[n][1], pos[n][0] + dims[n][0], pos[n][1] + dims[n][1]) for n in col_of}
    col_l = [min(box[n][0] for n in col) for col in COLUMNS]
    col_r = [max(box[n][2] for n in col) for col in COLUMNS]

    def free_ys(k):
        """Row gaps of column k, as (top, bottom) intervals."""
        ys = sorted((box[n][1], box[n][3]) for n in COLUMNS[k])
        gaps = [(-200, ys[0][0] - 6)]
        gaps += [(ys[i][1] + 6, ys[i + 1][0] - 6) for i in range(len(ys) - 1)]
        gaps.append((ys[-1][1] + 6, 4000))
        return gaps

    used_rows = {}                                   # column -> y values taken
    # A self-association draws a loop above its class: keep crossing lines off it.
    for a, _, _, b, _ in rels:
        if a == b:
            k = col_of[a]
            used_rows.setdefault(k, []).extend([box[a][1] - 40, box[a][1] - 28, box[a][1] - 16, box[a][1] - 4])
    def pick_row(cols, want):
        """A y free in every column of cols, nearest to want, 9 px from others."""
        cands = []
        for lo, hi in free_ys(cols[0]):
            y = lo
            while y <= hi:
                if all(any(l <= y <= h for l, h in free_ys(k)) for k in cols) and \
                   all(abs(y - u) >= 15 for k in cols for u in used_rows.get(k, [])):
                    cands.append(y)
                y += 3
        y = min(cands, key=lambda c: abs(c - want))
        for k in cols:
            used_rows.setdefault(k, []).append(y)
        return y

    # Each end of each association: which side of its box it uses.
    ends = {}                                        # (rel index, 0|1) -> (box, side)
    plan = []
    for i, (a, ma, mb, b, role) in enumerate(rels):
        if a == b:
            plan.append(('loop', i)); continue
        ca, cb = col_of[a], col_of[b]
        if ca == cb:
            top, bot = (a, b) if box[a][1] < box[b][1] else (b, a)
            ends[(i, 0 if top == a else 1)] = (top, 'bottom')
            ends[(i, 1 if top == a else 0)] = (bot, 'top')
            plan.append(('vertical', i))
        else:
            left, right = (a, b) if ca < cb else (b, a)
            ends[(i, 0 if left == a else 1)] = (left, 'right')
            ends[(i, 1 if left == a else 0)] = (right, 'left')
            plan.append(('across', i))

    # Ports: the ends on one side of a box, spread evenly, ordered by the
    # position of the other end so that lines leaving one side do not cross.
    def other(i, j):
        a, _, _, b, _ = rels[i]
        n = b if j == 0 else a
        return (box[n][1] + box[n][3]) / 2, (box[n][0] + box[n][2]) / 2
    port = {}
    groups = {}
    for key, (n, side) in ends.items():
        groups.setdefault((n, side), []).append(key)
    for (n, side), keys in groups.items():
        horiz = side in ('left', 'right')
        keys.sort(key=lambda k: other(*k)[0 if horiz else 1])
        for r, k in enumerate(keys):
            f = (r + 1) / (len(keys) + 1)
            x0, y0, x1, y1 = box[n]
            if side == 'left':   port[k] = (0, f, x0, y0 + f * (y1 - y0))
            if side == 'right':  port[k] = (1, f, x1, y0 + f * (y1 - y0))
            if side == 'top':    port[k] = (f, 0, x0 + f * (x1 - x0), y0)
            if side == 'bottom': port[k] = (f, 1, x0 + f * (x1 - x0), y1)

    # Vertical lanes in each gap between columns, one per line that turns there.
    lanes = {}                                       # gap index -> [(sort key, rel, which turn)]
    routes = {}
    for kind, i in plan:
        if kind != 'across':
            continue
        a, _, _, b, _ = rels[i]
        ja = 0 if col_of[a] < col_of[b] else 1       # which end is the left one
        L, R = (0, 1) if ja == 0 else (1, 0)
        lp, rp = port[(i, L)], port[(i, R)]
        cl, cr = min(col_of[a], col_of[b]), max(col_of[a], col_of[b])
        if cr == cl + 1:
            routes[i] = ('direct', lp, rp, cl, None)
            lanes.setdefault(cl, []).append(((lp[3] + rp[3]) / 2, i, 0))
        else:
            y = pick_row(list(range(cl + 1, cr)), (lp[3] + rp[3]) / 2)
            routes[i] = ('crossing', lp, rp, cl, y)
            lanes.setdefault(cl, []).append(((lp[3] + y) / 2, i, 0))
            lanes.setdefault(cr - 1, []).append(((y + rp[3]) / 2, i, 1))
    lane_x = {}
    for g, items in lanes.items():
        lo, hi = col_r[g] + 14, col_l[g + 1] - 14
        items.sort()
        for r, (_, i, t) in enumerate(items):
            lane_x[(i, t)] = lo + (hi - lo) * (r + 1) / (len(items) + 1)

    out = []
    for kind, i in plan:
        a, ma, mb, b, role = rels[i]
        eid = f'r{i}'
        if kind == 'loop':
            x0, y0, x1, y1 = box[a]
            k = sum(1 for (p, _, _, q, _) in rels[:i] if p == q == a)
            ty = y0 - 26 - 14 * k
            fx1, fx2 = 0.08 + 0.46 * k, 0.40 + 0.46 * k     # wide enough for both multiplicities
            pts = [(x0 + fx1 * (x1 - x0), ty), (x0 + fx2 * (x1 - x0), ty)]
            sty = (f'exitX={fx1};exitY=0;exitDx=0;exitDy=0;entryX={fx2};entryY=0;entryDx=0;entryDy=0;'
                   'edgeStyle=none;')
            out.append((eid, a, b, role, ma, mb, pts, sty)); continue
        pa, pb = port[(i, 0)], port[(i, 1)]
        sty = (f'exitX={pa[0]:.3f};exitY={pa[1]:.3f};exitDx=0;exitDy=0;'
               f'entryX={pb[0]:.3f};entryY={pb[1]:.3f};entryDx=0;entryDy=0;edgeStyle=none;')
        if kind == 'vertical':
            mx = (pa[2] + pb[2]) / 2
            pts = [(mx, pa[3] + (pb[3] - pa[3]) / 2)] if abs(pa[2] - pb[2]) < 2 else \
                  [(pa[2], (pa[3] + pb[3]) / 2), (pb[2], (pa[3] + pb[3]) / 2)]
            out.append((eid, a, b, role, ma, mb, pts, sty)); continue
        how, lp, rp, cl, y = routes[i]
        if how == 'direct':
            x = lane_x[(i, 0)]
            path = [(x, lp[3]), (x, rp[3])]
        else:
            x1, x2 = lane_x[(i, 0)], lane_x[(i, 1)]
            path = [(x1, lp[3]), (x1, y), (x2, y), (x2, rp[3])]
        if port[(i, 0)] != lp:                       # source is the right-hand end
            path = list(reversed(path))
        out.append((eid, a, b, role, ma, mb, path, sty))
    return out


def main():
    classes, rels = parse()
    placed = {n for col in COLUMNS for n in col}
    plain = [n for n, c in classes.items() if not c['enum']]
    missing = [n for n in plain if n not in placed]
    assert not missing, f'not placed: {missing}'
    dims = {n: size(n, c) for n, c in classes.items()}

    pos = {}
    x = 0
    heights = []
    for i, col in enumerate(COLUMNS):
        w = max(dims[n][0] for n in col)
        y = 0
        for n in col:
            pos[n] = (x + (w - dims[n][0]) / 2, y)
            y += dims[n][1] + ROW_GAP
        heights.append(y - ROW_GAP)
        x += w + (COL_GAP[i] if i < len(COL_GAP) else 0)
    total_w = x
    # Centre each column vertically on the tallest one.
    tallest = max(heights)
    for i, col in enumerate(COLUMNS):
        shift = (tallest - heights[i]) / 2
        for n in col:
            pos[n] = (pos[n][0], pos[n][1] + shift)

    enums = [n for n, c in classes.items() if c['enum']]
    routes = route(rels, pos, dims)

    # Enumerations fill the space under the shorter columns: a skyline of
    # what is already drawn (boxes and lines), and each enumeration, tallest
    # first, goes where it rises least.
    BIN = 5
    sky = [0.0] * (int(total_w / BIN) + 2)
    def raise_sky(x0, x1, y):
        for k in range(max(0, int(x0 / BIN)), min(len(sky), int(x1 / BIN) + 1)):
            sky[k] = max(sky[k], y)
    for n in placed:
        raise_sky(pos[n][0], pos[n][0] + dims[n][0], pos[n][1] + dims[n][1])
    def port(n, sty, which):
        mx = float(re.search(which + r'X=([\d.]+)', sty).group(1))
        my = float(re.search(which + r'Y=([\d.]+)', sty).group(1))
        return pos[n][0] + mx * dims[n][0], pos[n][1] + my * dims[n][1]
    for _, a, b, role, _, _, pts, sty in routes:
        path = [port(a, sty, 'exit')] + list(pts) + [port(b, sty, 'entry')]
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            # every segment, with room for its label and multiplicities
            raise_sky(min(x1, x2) - 12, max(x1, x2) + 12, max(y1, y2) + 16)
    for n in sorted(enums, key=lambda n: -dims[n][1]):
        w, h = dims[n]
        span = int(w / BIN) + 1
        best = None
        for k in range(0, len(sky) - span):
            top = max(sky[k:k + span]) + BAND_GAP / 2
            if best is None or top < best[0] - 0.5:
                best = (top, k)
        top, k = best
        pos[n] = (k * BIN, top)
        raise_sky(k * BIN - ENUM_GAP, k * BIN + w + ENUM_GAP, top + h)

    cells = []
    for n, c in classes.items():
        w, h = dims[n]
        cx, cy = pos[n]
        style = S_ENUM if c['enum'] else S_CLASS
        cells.append(f'<mxCell id="{n}" value="{html.escape(label(n, c))}" style="{style}" vertex="1" '
                     f'parent="1"><mxGeometry x="{cx:.0f}" y="{cy:.0f}" width="{w}" height="{h}" '
                     f'as="geometry"/></mxCell>')
    def port_point(n, sty, which):
        mx = float(re.search(which + r'X=([\d.]+)', sty).group(1))
        my = float(re.search(which + r'Y=([\d.]+)', sty).group(1))
        return pos[n][0] + mx * dims[n][0], pos[n][1] + my * dims[n][1]

    def placements(a, b, pts, sty):
        """Relative positions (-1 … 1 along the line) for the role label, at
        the middle of the longest horizontal stretch, and for the two
        multiplicities, a fixed distance from each end."""
        path = [port_point(a, sty, 'exit')] + list(pts) + [port_point(b, sty, 'entry')]
        segs = [(path[k], path[k + 1]) for k in range(len(path) - 1)]
        lens = [abs(q[0] - p[0]) + abs(q[1] - p[1]) for p, q in segs]
        total = sum(lens) or 1
        best, at, run = -1, 0.5, 0
        for (p, q), l in zip(segs, lens):
            if abs(q[1] - p[1]) < 1 and l > best:
                best, at = l, (run + l / 2) / total
            run += l
        near = min(0.45, 20 / total)
        return 2 * at - 1, -1 + 2 * near, 1 - 2 * near

    for eid, a, b, role, ma, mb, pts, sty in routes:
        lx, m0, m1 = placements(a, b, pts, sty)
        cells.append(f'<mxCell id="{eid}" value="{html.escape(role or "")}" style="{S_EDGE}{sty}" edge="1" '
                     f'parent="1" source="{a}" target="{b}"><mxGeometry x="{lx:.3f}" relative="1" as="geometry">'
                     f'<Array as="points">{"".join(f"<mxPoint x=\"{px:.0f}\" y=\"{py:.0f}\"/>" for px, py in pts)}'
                     f'</Array></mxGeometry></mxCell>')
        for j, (mult, at) in enumerate(((ma, m0), (mb, m1))):
            cells.append(f'<mxCell id="{eid}m{j}" value="{html.escape(mult)}" style="{S_END}" vertex="1" '
                         f'connectable="0" parent="{eid}"><mxGeometry x="{at}" y="0" relative="1" '
                         f'as="geometry"><mxPoint x="0" y="-9" as="offset"/></mxGeometry></mxCell>')

    xml = ('<mxfile host="Electron" type="device">\n'
           f'  <diagram id="{NAME}" name="{NAME}">\n'
           '    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
           'connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0">\n'
           '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
           + '\n        '.join(cells) +
           '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    out = os.environ.get('CLASS_OUT') or os.path.join(ROOT, NAME, f'{NAME}.drawio')
    with open(out, 'w') as f:
        f.write(xml)
    print(f'wrote {NAME}.drawio ({total_w:.0f} px wide, classes {tallest:.0f} px tall)')


if __name__ == '__main__':
    main()
