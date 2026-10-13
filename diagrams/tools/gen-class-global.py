#!/usr/bin/env python3
"""Lay out the complete class diagram for an A3 fold-out page.

The CONTENT is read from the drawing itself (fig-1-12-classes-global.drawio):
the classes, their attributes and operations, and the enumerations, as they
were last edited in draw.io. The associations are listed below; they follow
src/database/schema/ in the backend. Running the script re-lays the drawing out
and overwrites it, so it is not part of `make regen`: run it by hand, then
review the result in draw.io.

Readability rules the layout follows, after the supervisor's review:

  * every multiplicity, role name and association name sits ON its line, in an
    opaque white box, so it cannot be read as belonging to a neighbouring line;
  * two classes that face each other are joined by a straight line: the classes
    associated with User only are slid up or down to meet their port on User;
  * a line that has to turn does so in a lane of its own in the gap between two
    columns, and each gap is made wide enough for its lanes, at least LANE px
    apart, with MARGIN px at each box for the multiplicity;
  * vertical space is spent freely (the figure is width-limited on the page, so
    height does not shrink the text): wide row gaps, tall self-association loops;
  * a many-to-many association with data of its own (Like, Save, Repost,
    CommentLike, Follow, Block) is drawn as an association class, next to its
    line and joined to it by a short dashed line.

It also writes fig-1-12-classes-global.puml, the same content as text, so the
two never disagree.

  python3 gen-class-global.py          # rewrites the .drawio and the .puml
"""
import html
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAME = 'fig-1-12-classes-global'

FONT = 11
CHAR = 5.6           # average Helvetica advance at 11 px, measured on the labels
LINE = 14            # line height of a member
PAD = 8

ROW_GAP = 56         # between two classes of one column: room for rows of lines
LANE = 12            # minimum distance between two vertical lanes in a gap
# Text on the lines (multiplicities, roles, association names): larger than the
# class text, so it stays readable once the figure is scaled onto the A3 page.
LABEL_FONT = 18
LABEL_CHAR = 9.9     # average Helvetica advance at LABEL_FONT
MARGIN = 58          # free run at each box before a line may turn: room for a multiplicity
V_LINE = 170        # gap between two stacked classes joined by a named vertical line:
                     # room for a multiplicity at each end and the name between them
ROW_SEP = 24         # minimum distance between two horizontal rows in one gap
PORT_SEP = 30        # minimum distance between two lines along one side of a box
LANE_SEP = 22        # vertical clearance between two runs that share a lane
LOOP_H = 64          # height of a self-association loop
DASH = 18            # length of the dashed line to an association class
END_AT = 28          # distance from the box to the centre of a multiplicity
ENUM_GAP = 18
BAND_GAP = 70

# Grid: columns from left to right, each a list of classes stacked top-down.
COLUMNS = [
    # every class here is associated with User only: one column, each facing User
    ['MagazineProfile', 'MagazineSubscription', 'EligibilityAuditLog', 'Notification', 'Report',
     'WriterMemory', 'PortfolioInsight', 'WriterAudienceMetrics', 'WriterContentMetrics', 'WriterQualityMetrics'],
    ['User', 'Transaction'],
    ['Comment', 'CommentLike', 'Like', 'Repost', 'Save', 'AiInteraction', 'DocumentChunk'],
    ['Purchase', 'AnalyticsEvent', 'Document'],
    ['Article', 'ArticleDocument'],
    ['ArticleTag', 'Tag', 'ArticleChunk', 'ArticleMetrics'],
]
# Row gap per column: the User-only column has straight lines only, so it packs
# tight; the middle column is spread along User's height to give its lines room.
TIGHT = {0: 26}
SPREAD = {2: 'User', 3: 'Article', 5: 'Article'}
SPREAD_MAX = 150
# Columns whose classes each hang off one hub in the next column: slid to meet it.
ALIGN = {0: 'User'}
# Hubs drawn as tall as the columns beside them, so every neighbour faces its side
# and joins it with a straight line, and the lines along the side have room.
STRETCH = {'User': [0], 'Article': 'User'}
# Association classes of User's self-associations, drawn above User.
ABOVE_USER = ['Follow', 'Block']

# (end A, multiplicity at A, multiplicity at B, end B, name, association class)
# A multiplicity may carry its role name in front of it ("follower 0..*").
RELS = [
    ('User', '1', '0..1', 'MagazineProfile', 'extends', None),
    ('User', '1', '0..*', 'Article', 'writes', None),
    ('User', '0..1', '0..*', 'Article', 'publishes', None),
    ('User', '0..*', '0..*', 'Article', 'likes', 'Like'),
    ('User', '0..*', '0..*', 'Article', 'reposts', 'Repost'),
    ('User', '0..*', '0..*', 'Article', 'saves', 'Save'),
    ('User', '1', '0..*', 'Comment', 'posts', None),
    ('User', '0..*', '0..*', 'Comment', 'likes', 'CommentLike'),
    ('User', 'follower 0..*', 'followed 0..*', 'User', 'follows', 'Follow'),
    ('User', 'blocker 0..*', 'blocked 0..*', 'User', 'blocks', 'Block'),
    ('User', '1', '0..*', 'Notification', 'receives', None),
    ('User', '0..1', '0..*', 'Report', 'files', None),
    ('User', '0..1', '0..*', 'Report', 'resolves', None),
    ('Article', '1', '0..*', 'Comment', 'carries', None),
    ('Comment', '0..1', '0..*', 'Comment', 'replies to', None),
    ('Article', '1', '0..*', 'ArticleTag', 'is tagged with', None),
    ('Tag', '1', '0..*', 'ArticleTag', None, None),
    ('Article', '1', '0..*', 'ArticleChunk', 'is chunked into', None),
    ('User', '1', '0..1', 'WriterMemory', 'has voice profile', None),
    ('User', '1', '0..1', 'PortfolioInsight', 'has insights', None),
    ('User', '1', '0..*', 'AiInteraction', 'requests', None),
    ('Article', '0..1', '0..*', 'AiInteraction', 'concerns', None),
    ('User', '1', '0..*', 'Document', 'owns', None),
    ('Document', '1', '0..*', 'DocumentChunk', 'is chunked into', None),
    ('Article', '1', '0..*', 'ArticleDocument', 'is grounded in', None),
    ('Document', '1', '0..*', 'ArticleDocument', None, None),
    ('Article', '1', '0..*', 'Purchase', 'is licensed in', None),
    ('User', '1', '0..*', 'Purchase', 'buys', None),
    ('Purchase', '0..1', '0..1', 'Purchase', 'prior preview', None),
    ('Purchase', '1', '2..3', 'Transaction', 'records', None),
    ('User', 'sender 0..1', '0..*', 'Transaction', 'sends', None),
    ('User', 'receiver 0..1', '0..*', 'Transaction', 'receives', None),
    ('Article', '0..1', '0..*', 'Transaction', 'concerns', None),
    ('User', '1', '0..*', 'MagazineSubscription', 'subscribes', None),
    ('MagazineSubscription', '0..1', '0..1', 'MagazineSubscription', 'renews', None),
    ('User', '1', '0..*', 'EligibilityAuditLog', 'qualifies', None),
    ('User', '0..1', '0..*', 'EligibilityAuditLog', 'grants', None),
    ('Article', '1', '0..*', 'AnalyticsEvent', 'generates', None),
    ('User', '0..1', '0..*', 'AnalyticsEvent', 'views', None),
    ('Article', '1', '0..1', 'ArticleMetrics', 'is measured by', None),
    ('User', '1', '0..1', 'WriterAudienceMetrics', 'is measured by', None),
    ('User', '1', '0..1', 'WriterContentMetrics', 'is measured by', None),
    ('User', '1', '0..1', 'WriterQualityMetrics', 'is measured by', None),
]

S_CLASS = ('rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacingLeft=6;'
           'spacingRight=4;spacingTop=0;fontSize=%d;fontFamily=Helvetica;fontColor=#000000;'
           'strokeColor=#000000;fillColor=#FFFFFF;' % FONT)
S_ENUM = S_CLASS.replace('fillColor=#FFFFFF', 'fillColor=#DAE8FC')
S_EDGE = ('rounded=0;html=1;endArrow=none;strokeColor=#000000;fontSize=10;fontFamily=Helvetica;'
          'fontColor=#000000;labelBackgroundColor=#FFFFFF;edgeStyle=none;')
# On the line, in an opaque box: white in the export, so the line is hidden under it
S_LABEL = ('edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=%d;' % LABEL_FONT
           + 'fontFamily=Helvetica;fontColor=#000000;labelBackgroundColor=#FFFFFF;spacing=1;')
S_DASH = 'endArrow=none;dashed=1;html=1;rounded=0;strokeColor=#000000;'


# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------
def parse(src):
    """Classes and enumerations as drawn: {name: {'enum': bool, 'members': [...]}}."""
    classes = {}
    for c in ET.parse(src).getroot().iter('mxCell'):
        v = c.get('value') or ''
        if c.get('vertex') != '1' or c.get('parent') != '1' or '<b>' not in v:
            continue
        name = html.unescape(re.search(r'<b>(.*?)</b>', v).group(1)).strip()
        parts = re.split(r'<hr[^>]*>', v)[1:]
        members = []
        for p in parts:
            members += [html.unescape(re.sub(r'<[^>]+>', '', m)).replace('\xa0', ' ').strip()
                        for m in re.split(r'<br\s*/?>', p)]
        classes[name] = {'enum': '«Enumeration»' in v, 'members': [m for m in members if m]}
    return classes


def label(name, c):
    esc = lambda t: html.escape(t, quote=False)
    head = (f'<div style="text-align:center;padding-top:3px">'
            + ('«Enumeration»<br>' if c['enum'] else '') + f'<b>{esc(name)}</b></div>')
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


# ----------------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------------
class Layout:
    def __init__(self, classes):
        self.classes = classes
        self.dims = {n: size(n, c) for n, c in classes.items()}
        self.col_of = {n: i for i, col in enumerate(COLUMNS) for n in col}
        self.gaps = [90] * (len(COLUMNS) - 1)          # refined from the lane counts
        self.pos = {}
        self.shift = {}                                 # per class: vertical nudge from ALIGN

    def row_gaps(self, k):
        """The gap above each class of column k (after the first): tight or normal,
        never less than a self-association loop needs, spread if asked."""
        col = COLUMNS[k]
        loops = {r[0] for r in RELS if r[0] == r[3]}
        base = TIGHT.get(k, ROW_GAP)
        gaps = [max(base, LOOP_H + 30) if n in loops else base for n in col[1:]]
        for r, (up, down) in enumerate(zip(col, col[1:])):
            if any({a, b} == {up, down} for a, _, _, b, _, _ in RELS):
                gaps[r] = max(gaps[r], V_LINE)
        if k in SPREAD and SPREAD[k] in self.dims:
            target = self.dims[SPREAD[k]][1]
            have = sum(self.dims[n][1] for n in col) + sum(gaps)
            if have < target and gaps:
                extra = min((target - have) / len(gaps), SPREAD_MAX - base)
                gaps = [g + extra for g in gaps]
        return gaps

    def box(self, n):
        x, y = self.pos[n]
        w, h = self.dims[n]
        return x, y, x + w, y + h

    # -- placing ----------------------------------------------------------------
    def stretch(self):
        """Each hub as tall as the tallest column beside it (never shorter than its text)."""
        for hub, cols in STRETCH.items():
            natural = size(hub, self.classes[hub])[1]
            if isinstance(cols, str):                    # as tall as another hub
                span = self.dims[cols][1]
            else:
                span = max(sum(self.dims[n][1] for n in COLUMNS[k]) + sum(self.row_gaps(k)) for k in cols)
            self.dims[hub] = (self.dims[hub][0], max(natural, span))

    def place(self):
        """Columns left to right, each centred on the tallest; then ALIGN nudges."""
        x, heights, xs = 0, [], []
        above = max(self.dims[n][1] for n in ABOVE_USER) + DASH + LOOP_H + 16
        for i, col in enumerate(COLUMNS):
            w = max(self.dims[n][0] for n in col)
            y = above if ('User' in col or 'Article' in col or i in ALIGN
                          or i in SPREAD) else 0
            gaps = self.row_gaps(i) + [0]
            for n, gap in zip(col, gaps):
                self.pos[n] = (x + (w - self.dims[n][0]) / 2, y)
                y += self.dims[n][1] + gap
            heights.append(y)
            xs.append(x)
            x += w + (self.gaps[i] if i < len(self.gaps) else 0)
        self.width = x
        tallest = max(heights)
        for i, col in enumerate(COLUMNS):
            d = 0                                       # top-aligned: the hubs set the frame
            for n in col:
                self.pos[n] = (self.pos[n][0], self.pos[n][1] + d + self.shift.get(n, 0))
        # Follow and Block above User, each over its loop
        ux0, uy0, ux1, _ = self.box('User')
        for k, n in enumerate(ABOVE_USER):
            w, h = self.dims[n]
            mid = ux0 + (0.19 + 0.62 * k) * (ux1 - ux0)
            bx = mid - w / 2
            if k == 0:
                bx = min(bx, ux0 + (ux1 - ux0) / 2 - 8 - w)
            else:
                bx = max(bx, ux0 + (ux1 - ux0) / 2 + 8)
            self.pos[n] = (bx, uy0 - LOOP_H - DASH - h)

    def align(self, ports):
        """Slide each class of an ALIGN column so its centre meets its port on the hub,
        then pack the column without overlaps, as close to those targets as possible."""
        for k, hub in ALIGN.items():
            col = COLUMNS[k]
            want = {}
            for key, (n, side, fx, fy, px, py) in ports.items():
                i, j = key
                a, _, _, b, _, _ = RELS[i]
                other = b if j == 0 else a
                if n == hub and other in col:
                    want[other] = py
            items = sorted(col, key=lambda n: want.get(n, self.box(n)[1]))
            sep = TIGHT.get(k, ROW_GAP)
            loops = {r[0] for r in RELS if r[0] == r[3]}
            # forward pass: as near the target as the class above allows
            ys = []
            prev = -1e9
            for n in items:
                h = self.dims[n][1]
                y = max(want.get(n, self.box(n)[1] + h / 2) - h / 2,
                        prev + (max(sep, LOOP_H + 30) if n in loops else sep))
                ys.append(y)
                prev = y + h
            # the stack ends at the hub's bottom at the latest
            hub_bottom = self.box(hub)[3]
            ys[-1] = min(ys[-1], hub_bottom - self.dims[items[-1]][1])
            # backward pass: pull the stack up again where it was pushed too far down
            for idx in range(len(items) - 2, -1, -1):
                n = items[idx]
                h = self.dims[n][1]
                target = want.get(n, ys[idx] + h / 2) - h / 2
                nxt = items[idx + 1]
                limit = ys[idx + 1] - (max(sep, LOOP_H + 30) if nxt in loops else sep) - h
                ys[idx] = min(max(target, ys[idx]), limit) if target > ys[idx] else min(ys[idx], limit)
            COLUMNS[k][:] = items
            for n, y in zip(items, ys):
                self.shift[n] = self.shift.get(n, 0) + (y - self.box(n)[1])

    # -- ports ------------------------------------------------------------------
    def plan(self):
        """For every association: its kind, and which side of each box it uses."""
        ends, kinds = {}, []
        for i, (a, ma, mb, b, role, ac) in enumerate(RELS):
            if a == b:
                kinds.append('loop'); continue
            ca, cb = self.col_of[a], self.col_of[b]
            if ca == cb:
                top, bot = (a, b) if self.box(a)[1] < self.box(b)[1] else (b, a)
                ends[(i, 0 if top == a else 1)] = (top, 'bottom')
                ends[(i, 1 if top == a else 0)] = (bot, 'top')
                kinds.append('vertical')
            elif ac == 'CommentLike':
                # User -> Comment passes over CommentLike and enters Comment from below
                ends[(i, 0)] = (a, 'right')
                ends[(i, 1)] = (b, 'bottom')
                kinds.append('under')
            else:
                left, right = (a, b) if ca < cb else (b, a)
                ends[(i, 0 if left == a else 1)] = (left, 'right')
                ends[(i, 1 if left == a else 0)] = (right, 'left')
                kinds.append('direct' if abs(ca - cb) == 1 else 'crossing')
        return ends, kinds

    def ac_row(self, i):
        """The level an association-class line runs at: just under its class, or for
        CommentLike just above it."""
        a, _, _, b, _, ac = RELS[i]
        if not ac or a == b:
            return None
        x0, y0, x1, y1 = self.box(ac)
        return y0 - DASH if ac == 'CommentLike' else y1 + DASH

    def ports(self, ends):
        """Ends on one side of a box, each level with what it faces and packed apart,
        ordered by where the other end is, so lines leaving one side do not cross."""
        def other_c(i, j):
            a, _, _, b, _, _ = RELS[i]
            n = b if j == 0 else a
            x0, y0, x1, y1 = self.box(n)
            row = self.ac_row(i)
            if row is not None and ends[(i, j)][1] in ('left', 'right'):
                return row, (x0 + x1) / 2                # run straight at the class's row
            if a in STRETCH and b in STRETCH and not RELS[i][5]:
                return 1e9, (x0 + x1) / 2                # placed later on a level of its own:
                                                         # keep it out of the others' way
            return (y0 + y1) / 2, (x0 + x1) / 2
        groups = {}
        for key, (n, side) in ends.items():
            groups.setdefault((n, side), []).append(key)
        ports = {}
        for (n, side), keys in groups.items():
            horiz = side in ('left', 'right')
            keys.sort(key=lambda k: other_c(*k)[0 if horiz else 1])
            x0, y0, x1, y1 = self.box(n)
            lo, hi = (y0, y1) if horiz else (x0, x1)
            # each port level with the centre of what it faces, then packed PORT_SEP apart
            want = [min(max(other_c(*k)[0 if horiz else 1], lo + 14), hi - 14) for k in keys]
            at = pack(want, PORT_SEP if horiz else 3 * PORT_SEP, lo + 14, hi - 14)
            for r, k in enumerate(keys):
                f = (at[r] - lo) / (hi - lo)
                if side == 'left':   ports[k] = (n, side, 0, f, x0, y0 + f * (y1 - y0))
                if side == 'right':  ports[k] = (n, side, 1, f, x1, y0 + f * (y1 - y0))
                if side == 'top':    ports[k] = (n, side, f, 0, x0 + f * (x1 - x0), y0)
                if side == 'bottom': ports[k] = (n, side, f, 1, x0 + f * (x1 - x0), y1)
        return ports

    def straighten(self, ports, kinds):
        """Where the box at one end spans the port at the other, move its port level
        with it: the association becomes one straight line."""
        count = {}
        for (n, side, *_ ) in ports.values():
            count[(n, side)] = count.get((n, side), 0) + 1
        for i, kind in enumerate(kinds):
            if kind not in ('direct', 'vertical'):
                continue
            p, q = ports[(i, 0)], ports[(i, 1)]
            # move the end on the side with fewer lines (the leaf), towards the other
            mv, fx = ((i, 1), p) if count[(q[0], q[1])] <= count[(p[0], p[1])] else ((i, 0), q)
            n, side, _, _, px, py = ports[mv]
            x0, y0, x1, y1 = self.box(n)
            if kind == 'direct' and y0 + 10 <= fx[5] <= y1 - 10:
                ports[mv] = (n, side, ports[mv][2], (fx[5] - y0) / (y1 - y0), px, fx[5])
            if kind == 'vertical' and x0 + 10 <= fx[4] <= x1 - 10:
                ports[mv] = (n, side, (fx[4] - x0) / (x1 - x0), ports[mv][3], fx[4], py)

    # -- routing ----------------------------------------------------------------
    def route(self):
        ends, kinds = self.plan()
        ports = self.ports(ends)
        self.straighten(ports, kinds)
        col_l = [min(self.box(n)[0] for n in col) for col in COLUMNS]
        col_r = [max(self.box(n)[2] for n in col) for col in COLUMNS]
        self.col_l, self.col_r = col_l, col_r

        def free_ys(k):
            ys = sorted((self.box(n)[1], self.box(n)[3]) for n in COLUMNS[k])
            if k == self.col_of['User']:                 # Follow, Block and the loops above User
                ys.append((min(self.box(n)[1] for n in ABOVE_USER), self.box('User')[1]))
                ys.sort()
            gaps = [(-400, ys[0][0] - 10)]
            gaps += [(ys[i][1] + 10, ys[i + 1][0] - 10) for i in range(len(ys) - 1)]
            gaps.append((ys[-1][1] + 10, 6000))
            return gaps

        used = {}                                        # column -> y of rows already through it
        for i, kind in enumerate(kinds):                 # keep rows off the loops
            if kind == 'loop':
                n = RELS[i][0]
                k = self.col_of.get(n)
                if k is not None:
                    y0 = self.box(n)[1]
                    used.setdefault(k, []).extend(range(int(y0 - LOOP_H - 20), int(y0), 4))

        def pick_row(k, want, within=None):
            """A y free in column k (inside `within` if given), nearest to want."""
            cands = []
            for lo, hi in free_ys(k):
                if within:
                    lo, hi = max(lo, within[0]), min(hi, within[1])
                y = lo
                while y <= hi:
                    if all(abs(y - u) >= ROW_SEP for u in used.get(k, [])):
                        cands.append(y)
                    y += 2
            if not cands and within:                     # window full: anywhere in the column
                return pick_row(k, want)
            y = min(cands, key=lambda c: abs(c - want))
            used.setdefault(k, []).append(y)
            return y

        # Each line is a list of "legs": horizontal runs through columns joined by
        # vertical runs in gaps. A vertical run in gap g gets a lane x later.
        legs = {}
        verticals = {}                                   # gap -> [(i, idx, y_from, y_to)]
        dashes = {}
        order = sorted(range(len(kinds)), key=lambda i: RELS[i][5] is None)
        for i in order:
            kind = kinds[i]
            a, ma, mb, b, role, ac = RELS[i]
            if kind in ('loop', 'vertical'):
                continue
            p = ports[(i, 0)]
            q = ports[(i, 1)]
            if kind == 'under':
                # User right port -> lane in the gap -> row just above CommentLike -> Comment bottom
                g = self.col_of[a]
                cy0 = self.box(ac)[1]
                y = pick_row(self.col_of[b], cy0 - DASH, (self.box(b)[3] + 8, cy0 - 8))
                cx = (self.box(ac)[0] + self.box(ac)[2]) / 2
                qx = min(self.box(b)[2] - 12, cx + 40)
                ports[(i, 1)] = (b, 'bottom', (qx - self.box(b)[0]) / self.dims[b][0], 1, qx, self.box(b)[3])
                legs[i] = ['L', ('lane', g, p[5], y), ('pt', qx, y)]
                verticals.setdefault(g, []).append((i, 1, p[5], y))
                dashes[ac] = (cx, y, 'top')
                continue
            left, right = (p, q) if p[4] < q[4] else (q, p)
            cl, cr = self.col_of[left[0]], self.col_of[right[0]]
            rows = []
            if not ac and left[0] in STRETCH and right[0] in STRETCH:
                # one level free in every column between: a single straight line
                cols = list(range(cl + 1, cr))
                lo = max(self.box(left[0])[1], self.box(right[0])[1]) + 14
                hi = min(self.box(left[0])[3], self.box(right[0])[3]) - 14
                cands = []
                y = lo
                while y <= hi:
                    if all(any(a0 <= y <= a1 for a0, a1 in free_ys(k)) and
                           all(abs(y - u) >= ROW_SEP for u in used.get(k, [])) for k in cols):
                        taken = [v[5] for v in ports.values() if v[0] in (left[0], right[0])
                                 and v[1] in (left[1], right[1]) and v not in (left, right)]
                        if all(abs(y - t) >= PORT_SEP for t in taken):
                            cands.append(y)
                    y += 2
                if cands:
                    y = min(cands, key=lambda c: abs(c - (left[5] + right[5]) / 2))
                    for k in cols:
                        used.setdefault(k, []).append(y)
                    rows = [y] * len(cols)
            for k in ([] if rows else range(cl + 1, cr)):
                want = rows[-1] if rows else (right[5] if right[0] in STRETCH else left[5])
                within = None
                if ac and ac in COLUMNS[k]:
                    # through the gap right under the association class
                    by = self.box(ac)[3]
                    within = (by + DASH - 4, by + DASH + 26)
                    want = by + DASH
                rows.append(pick_row(k, want, within))
                if ac and ac in COLUMNS[k]:
                    cx = (self.box(ac)[0] + self.box(ac)[2]) / 2
                    dashes[ac] = (cx, rows[-1], 'bottom')
                    # nothing else may cross the dashed line
                    used.setdefault(k, []).extend(range(int(self.box(ac)[3]), int(rows[-1]), 4))
            for end, row in ((left, rows[0] if rows else None), (right, rows[-1] if rows else None)):
                if row is None:
                    continue
                key = (i, 0) if end is p else (i, 1)
                n, side = end[0], end[1]
                x0, y0, x1, y1 = self.box(n)
                taken = [v[5] for k2, v in ports.items() if k2 != key and v[0] == n and v[1] == side]
                if y0 + 14 <= row <= y1 - 14 and all(abs(row - t) >= PORT_SEP for t in taken):
                    ports[key] = (n, side, end[2], (row - y0) / (y1 - y0), end[4], row)
                    if end is left:
                        left = ports[key]
                    else:
                        right = ports[key]
                    if key == (i, 0):
                        p = ports[key]
                    else:
                        q = ports[key]
            ys = [left[5]] + rows + [right[5]]
            path = []
            for g in range(cl, cr):
                y_in, y_out = ys[g - cl], ys[g - cl + 1]
                if abs(y_in - y_out) < 0.5:
                    continue                             # level: no turn in this gap
                path.append(('lane', g, y_in, y_out))
                verticals.setdefault(g, []).append((i, len(path) - 1, y_in, y_out))
            legs[i] = (left is not p, path)

        # Lanes: in each gap, one x per vertical run, ordered to avoid crossings,
        # and the gap widened to fit them.
        lane_x = {}
        need = [2 * MARGIN] * (len(COLUMNS) - 1)
        for g, runs in verticals.items():
            # interval colouring: a lane takes every run that clears the ones in it
            lanes = []
            for run in sorted(runs, key=lambda r: min(r[2], r[3])):
                a0, a1 = sorted((run[2], run[3]))
                for lane in lanes:
                    if all(a0 > max(b[2], b[3]) + LANE_SEP or a1 < min(b[2], b[3]) - LANE_SEP for b in lane):
                        lane.append(run); break
                else:
                    lanes.append([run])
            # order lanes by the mean height of their runs: fewer crossings between them
            lanes.sort(key=lambda lane: sum((r[2] + r[3]) / 2 for r in lane) / len(lane))
            lo, hi = col_r[g] + MARGIN, col_l[g + 1] - MARGIN
            for r, lane in enumerate(lanes):
                for (i, idx, *_ ) in lane:
                    lane_x[(i, idx)] = lo + (hi - lo) * (r + 1) / (len(lanes) + 1)
            need[g] = 2 * MARGIN + (len(lanes) + 1) * LANE
        for i, kind in enumerate(kinds):
            a, ma, mb, b, role, ac = RELS[i]
            if kind == 'direct' and role:
                g = min(self.col_of[a], self.col_of[b])
                need[g] = max(need[g], len(role) * LABEL_CHAR + 8 + 2 * (END_AT + 22) + 16)
        return ports, kinds, legs, lane_x, need, dashes

    # -- assembling the lines ---------------------------------------------------
    def lines(self, ports, kinds, legs, lane_x, dashes):
        out = []
        for i, kind in enumerate(kinds):
            a, ma, mb, b, role, ac = RELS[i]
            if kind == 'loop':
                x0, y0, x1, y1 = self.box(a)
                loops = [j for j, r in enumerate(RELS) if r[0] == r[3] == a]
                k = loops.index(i)
                if len(loops) == 1:
                    f1, f2 = 0.25, 0.75
                else:
                    f1, f2 = (0.04, 0.34) if k == 0 else (0.66, 0.96)
                ty = y0 - LOOP_H
                pts = [(x0 + f1 * (x1 - x0), ty), (x0 + f2 * (x1 - x0), ty)]
                sty = (f'exitX={f1};exitY=0;exitDx=0;exitDy=0;entryX={f2};entryY=0;entryDx=0;entryDy=0;')
                path = [(pts[0][0], y0)] + pts + [(pts[1][0], y0)]
                if ac:
                    dashes[ac] = ((pts[0][0] + pts[1][0]) / 2, ty, 'bottom')
                out.append((f'r{i}', a, b, role, ma, mb, pts, sty, path, ac))
                continue
            p, q = ports[(i, 0)], ports[(i, 1)]
            sty = (f'exitX={p[2]:.4f};exitY={p[3]:.4f};exitDx=0;exitDy=0;'
                   f'entryX={q[2]:.4f};entryY={q[3]:.4f};entryDx=0;entryDy=0;')
            if kind == 'vertical':
                pts = [] if abs(p[4] - q[4]) < 0.5 else [(p[4], (p[5] + q[5]) / 2), (q[4], (p[5] + q[5]) / 2)]
            elif kind == 'under':
                _, (_, g, y_in, y_out), (_, qx, y) = legs[i]
                x = lane_x[(i, 1)]
                pts = [(x, y_in), (x, y_out), (qx, y)]
            else:
                rev, path_legs = legs[i]
                pts = []
                for idx, (_, g, y_in, y_out) in enumerate(path_legs):
                    x = lane_x[(i, idx)]
                    pts += [(x, y_in), (x, y_out)]
                if rev:
                    pts = list(reversed(pts))
            path = [(p[4], p[5])] + pts + [(q[4], q[5])]
            out.append((f'r{i}', a, b, role, ma, mb, pts, sty, path, ac))
        return out


def pack(want, sep, lo, hi):
    """Sorted targets moved as little as possible so that they are sep apart and
    inside [lo, hi]; spread evenly if they cannot all fit."""
    n = len(want)
    if n == 0:
        return []
    if (n - 1) * sep > hi - lo:
        return [lo + (hi - lo) * (r + 1) / (n + 1) for r in range(n)]
    at = list(want)
    for _ in range(50):                               # alternate passes until stable
        for r in range(1, n):
            at[r] = max(at[r], at[r - 1] + sep)
        at[-1] = min(at[-1], hi)
        for r in range(n - 2, -1, -1):
            at[r] = min(at[r], at[r + 1] - sep)
        at[0] = max(at[0], lo)
    return at


def placements(path, dash_x=None):
    """Positions along the line (-1 at the source, 1 at the target): the name at the
    middle of the longest horizontal run (clear of an association class's dashed
    line), and each multiplicity END_AT px from its box, on the first run."""
    segs = list(zip(path, path[1:]))
    lens = [abs(q[0] - p[0]) + abs(q[1] - p[1]) for p, q in segs]
    total = sum(lens) or 1
    best, at, run = -1, 0.5, 0
    for (p, q), l in zip(segs, lens):
        if abs(q[1] - p[1]) < 1 and l > best:
            mid = run + l / 2
            if dash_x is not None and min(p[0], q[0]) - 1 <= dash_x <= max(p[0], q[0]) + 1:
                # put the name halfway along the longer part beside the dashed line
                d = abs(dash_x - p[0])
                mid = run + (d / 2 if d > l - d else d + (l - d) / 2)
            best, at = l, mid / total
        run += l
    if best < 0:                                       # no horizontal run: the middle
        at = 0.5
    e0 = min(END_AT, lens[0] / 2) / total
    e1 = min(END_AT, lens[-1] / 2) / total
    return 2 * at - 1, -1 + 2 * e0, 1 - 2 * e1


def write_puml(classes, path):
    """The same content as text: every class and enumeration as drawn, and every
    association of RELS. An association class is written as a comment under its
    association: PlantUML accepts at most two `(A, B) .. C` per pair of classes,
    and User-Article has three (Like, Repost, Save)."""
    out = ['@startuml',
           "' Complete class diagram, as text. Written by tools/gen-class-global.py from",
           "' fig-1-12-classes-global.drawio and the association list in that script:",
           "' edit the drawing (or the list), then re-run the script. Not rendered.",
           '!include ../_style.puml', '!pragma layout elk', 'hide circle', 'hide empty methods', '']
    for n, c in classes.items():
        if c['enum']:
            out += [f'enum {n} {{'] + [f'  {m}' for m in c['members']] + ['}', '']
        else:
            out += [f'class {n} {{'] + [f'  {m}' for m in c['members']] + ['}', '']
    for a, ma, mb, b, role, ac in RELS:
        out.append(f'{a} "{ma}" -- "{mb}" {b}' + (f' : {role}' if role else ''))
        if ac:
            out.append(f"' association class: ({a}, {b}) .. {ac}")
    out += ['@enduml', '']
    with open(path, 'w') as f:
        f.write('\n'.join(out))


def main():
    src = os.environ.get('CLASS_SRC') or os.path.join(ROOT, NAME, f'{NAME}.drawio')
    out_path = os.environ.get('CLASS_OUT') or os.path.join(ROOT, NAME, f'{NAME}.drawio')
    classes = parse(src)
    placed = {n for col in COLUMNS for n in col} | set(ABOVE_USER)
    missing = [n for n, c in classes.items() if not c['enum'] and n not in placed]
    assert not missing, f'not placed: {missing}'
    unknown = {x for r in RELS for x in (r[0], r[3], r[5]) if x} - set(classes)
    assert not unknown, f'not drawn: {unknown}'

    L = Layout(classes)
    L.stretch()
    # Iterate: place, route, widen the gaps to their lanes, slide the ALIGN columns.
    for _ in range(4):
        L.place()
        ends, kinds = L.plan()
        ports = L.ports(ends)
        L.align(ports)
        L.place()
        ports, kinds, legs, lane_x, need, dashes = L.route()
        L.gaps = need
    L.place()
    ports, kinds, legs, lane_x, need, dashes = L.route()
    routes = L.lines(ports, kinds, legs, lane_x, dashes)

    # Enumerations fill the space under the shorter columns: a skyline of what is
    # already drawn, and each enumeration, tallest first, goes where it rises least.
    BIN = 5
    sky = [-1e9] * (int(L.width / BIN) + 2)
    def raise_sky(x0, x1, y):
        for k in range(max(0, int(x0 / BIN)), min(len(sky), int(x1 / BIN) + 1)):
            sky[k] = max(sky[k], y)
    for n in placed:
        x0, y0, x1, y1 = L.box(n)
        raise_sky(x0, x1, y1)
    for *_, path, _ in routes:
        for (x1, y1), (x2, y2) in zip(path, path[1:]):
            raise_sky(min(x1, x2) - 14, max(x1, x2) + 14, max(y1, y2) + 18)
    floor = min(L.box(n)[1] for n in placed)
    for n in sorted((n for n, c in classes.items() if c['enum']), key=lambda n: -L.dims[n][1]):
        w, h = L.dims[n]
        span = int(w / BIN) + 1
        best = None
        for k in range(0, len(sky) - span):
            top = max(max(sky[k:k + span]), floor) + BAND_GAP / 2
            if best is None or top < best[0] - 0.5:
                best = (top, k)
        top, k = best
        L.pos[n] = (k * BIN, top)
        raise_sky(k * BIN - ENUM_GAP, k * BIN + w + ENUM_GAP, top + h)

    # -- write --------------------------------------------------------------------
    cells = []
    for n, c in classes.items():
        w, h = L.dims[n]
        x, y = L.pos[n]
        style = S_ENUM if c['enum'] else S_CLASS
        cells.append(f'<mxCell id="{n}" value="{html.escape(label(n, c))}" style="{style}" vertex="1" '
                     f'parent="1"><mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" '
                     f'as="geometry"/></mxCell>')

    def lbl(parent, key, text, at):
        # a role name goes above its multiplicity: "follower 0..*" -> two lines
        text = '<br>'.join(html.escape(t, quote=False) for t in text.rsplit(' ', 1)) \
            if re.search(r' [0-9*.]+$', text) else html.escape(text, quote=False)
        return (f'<mxCell id="{parent}{key}" value="{html.escape(text)}" style="{S_LABEL}" vertex="1" '
                f'connectable="0" parent="{parent}"><mxGeometry x="{at:.4f}" y="0" relative="1" '
                f'as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')

    for eid, a, b, role, ma, mb, pts, sty, path, ac in routes:
        dash_x = dashes[ac][0] if ac in dashes else None
        name_at, m0, m1 = placements(path, dash_x)
        pts_xml = ''.join(f'<mxPoint x="{px:.1f}" y="{py:.1f}"/>' for px, py in pts)
        cells.append(f'<mxCell id="{eid}" value="" style="{S_EDGE}{sty}" edge="1" parent="1" '
                     f'source="{a}" target="{b}"><mxGeometry relative="1" as="geometry">'
                     f'<Array as="points">{pts_xml}</Array></mxGeometry></mxCell>')
        if role:
            cells.append(lbl(eid, 'n', role, name_at))
        if a == b:                                     # a loop: one end on each leg
            leg = (LOOP_H / 2) / (2 * LOOP_H + abs(pts[1][0] - pts[0][0]))   # middle of each leg
            cells.append(lbl(eid, 'm0', ma, -1 + 2 * leg))
            cells.append(lbl(eid, 'm1', mb, 1 - 2 * leg))
        else:
            cells.append(lbl(eid, 'm0', ma, m0))
            cells.append(lbl(eid, 'm1', mb, m1))

    for ac, (x, y, side) in dashes.items():
        entry = 'entryX=0.5;entryY=1;' if side == 'bottom' else 'entryX=0.5;entryY=0;'
        cells.append(f'<mxCell id="d_{ac}" value="" style="{S_DASH}{entry}entryDx=0;entryDy=0;" edge="1" '
                     f'parent="1" target="{ac}"><mxGeometry relative="1" as="geometry">'
                     f'<mxPoint x="{x:.1f}" y="{y:.1f}" as="sourcePoint"/></mxGeometry></mxCell>')

    xml = ('<mxfile host="Electron" type="device">\n'
           f'  <diagram id="{NAME}" name="{NAME}">\n'
           '    <mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
           'connect="1" arrows="1" fold="1" page="0" pageScale="1" math="0" shadow="0">\n'
           '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
           + '\n        '.join(cells) +
           '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    with open(out_path, 'w') as f:
        f.write(xml)
    print(f'wrote {os.path.basename(out_path)} ({L.width:.0f} px wide; gaps {[round(g) for g in L.gaps]})')
    puml = os.environ.get('CLASS_PUML') or os.path.join(ROOT, NAME, f'{NAME}.puml')
    write_puml(classes, puml)
    print(f'wrote {os.path.basename(puml)}')


if __name__ == '__main__':
    main()
