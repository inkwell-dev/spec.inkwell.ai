#!/usr/bin/env python3
"""Draw the four architecture figures as draw.io files.

  python3 diagrams/tools/gen-architecture.py          # writes all four .drawio
  make one F=fig-3-1-architecture-frontend            # then render each one

The figures used to be drawn by hand on a 1,250 px canvas with 10-13 px text.
Scaled to the report's text width, that text printed at about 5 pt. Here every
figure is laid out on a 780 px canvas with 16 px body text and 18-20 px
headings, so it prints at 9-11 pt, and every figure shares one style:

  * a container per tier, filled with the tier's colour;
  * white boxes inside it, a bold first line and plain lines under it;
  * orthogonal arrows with their label on a white background, and a small arc
    where two arrows cross, so a crossing is never mistaken for a junction.

Colours are draw.io's standard palette, as in the other architecture figures:
blue frontend, green backend and worker, purple storage, red Redis, yellow
external services and notes, grey for what lies outside the system.
"""
from html import escape
from pathlib import Path

DIAGRAMS = Path(__file__).resolve().parent.parent

# fill, stroke
BLUE = ('#dae8fc', '#6c8ebf')
GREEN = ('#d5e8d4', '#82b366')
PURPLE = ('#e1d5e7', '#9673a6')
RED = ('#f8cecc', '#b85450')
YELLOW = ('#fff2cc', '#d6b656')
GREY = ('#f5f5f5', '#666666')
WHITE = ('#ffffff', '#4d4d4d')

FONT = 'fontFamily=Helvetica;'


class Figure:
    """Collects the cells of one figure and writes them as a .drawio file."""

    def __init__(self, name: str, title: str):
        self.name, self.title = name, title
        self.cells: list[str] = []
        self.n = 0

    def _id(self) -> str:
        self.n += 1
        return f'c{self.n}'

    def container(self, x, y, w, h, title, colour, size=20):
        """A tier: rounded, filled, its title at the top."""
        cid = self._id()
        style = (f'rounded=1;arcSize=4;whiteSpace=wrap;html=1;verticalAlign=top;align=center;'
                 f'fillColor={colour[0]};strokeColor={colour[1]};strokeWidth=1.5;'
                 f'fontStyle=1;fontSize={size};spacingTop=6;{FONT}')
        self.cells.append(self._vertex(cid, escape(title), style, x, y, w, h))
        return cid

    def box(self, x, y, w, h, title, lines=(), colour=WHITE, centre=False, size=16, plain=False):
        """A component: a bold first line, then one plain line per item."""
        cid = self._id()
        html = escape(title) if plain else f'<b>{escape(title)}</b>'
        if lines:
            html += '<br>' + '<br>'.join(escape(l) for l in lines)
        align = 'align=center;verticalAlign=middle;' if centre else 'align=left;verticalAlign=top;'
        style = (f'rounded=1;arcSize=6;whiteSpace=wrap;html=1;{align}spacing=10;'
                 f'fillColor={colour[0]};strokeColor={colour[1]};strokeWidth=1.2;'
                 f'fontSize={size};{FONT}')
        self.cells.append(self._vertex(cid, html, style, x, y, w, h))
        return cid

    def edge(self, src, tgt, label='', exit=None, entry=None, points=(), dashed=False, at=0, lift=0):
        """An orthogonal arrow. The label is HTML (a <br> breaks it); exit/entry
        are (x, y) fractions of the source and target boxes; points are
        waypoints that fix the route of the arrow; at moves the label along
        the arrow (-1 at the source, 0 in the middle, 1 at the target), so the
        labels of neighbouring arrows do not overlap; lift raises the label
        above the arrow by that many pixels, for an arrow too short to carry
        its label on the line."""
        cid = self._id()
        style = ('edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;'
                 'strokeWidth=1.5;strokeColor=#333333;jumpStyle=arc;jumpSize=10;'
                 f'fontSize=15;labelBackgroundColor=#ffffff;{FONT}')
        if exit:
            style += f'exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;'
        if entry:
            style += f'entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;'
        if dashed:
            style += 'dashed=1;'
        pts = ''.join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in points)
        geom = (f'<mxGeometry x="{at}" relative="1" as="geometry">'
                + (f'<Array as="points">{pts}</Array>' if pts else '')
                + (f'<mxPoint x="0" y="{-lift}" as="offset"/>' if lift else '') + '</mxGeometry>')
        self.cells.append(f'<mxCell id="{cid}" value="{escape(label)}" style="{style}" '
                          f'edge="1" parent="1" source="{src}" target="{tgt}">{geom}</mxCell>')
        return cid

    @staticmethod
    def _vertex(cid, html, style, x, y, w, h):
        # The value is HTML, stored escaped inside the XML attribute.
        return (f'<mxCell id="{cid}" value="{escape(html)}" style="{style}" vertex="1" parent="1">'
                f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def write(self):
        body = '\n        '.join(self.cells)
        xml = f'''<mxfile host="Electron" type="device">
  <diagram id="{self.name}" name="{escape(self.title)}">
    <mxGraphModel dx="1000" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="800" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
        (DIAGRAMS / self.name / f'{self.name}.drawio').write_text(xml)


# ── Logical architecture: frontend ───────────────────────────────────────────
def frontend():
    f = Figure('fig-3-1-architecture-frontend', 'Logical frontend architecture')
    browser = f.box(290, 0, 200, 50, 'Browser', colour=GREY, centre=True, size=17)
    fe = f.container(0, 90, 780, 470, 'Frontend: Next.js 16, App Router', BLUE)
    # Row 1: what the app is made of.
    f.box(15, 135, 365, 200, 'Routes (app/): 28 pages',
          ['/ · /articles/[slug] · /search', '/editor/[id] · /dashboard/*',
           '/following · /saved · /library', '/discover · /marketplace',
           '/m/[slug] · /u/[username]', '/settings · /admin'])
    f.box(400, 135, 365, 200, 'Features (features/): 18 modules',
          ['editor: TipTap · inline actions', 'ai: docked panel, voice, document sources',
           'documents · saves · reposts', 'marketplace · evaluation',
           'notifications · moderation'])
    # Row 2: what runs before any page.
    f.box(15, 350, 750, 50, 'Request proxy (proxy.ts): route protection before the page renders',
          centre=True)
    # Row 3: the three ways the browser talks to the outside, one above each arrow.
    sse = f.box(15, 415, 240, 130, 'SSE client', ['EventSource,', 'live notifications'], colour=YELLOW)
    state = f.box(270, 415, 240, 130, 'State and data',
                  ['React Query · Zustand', 'axios interceptors', '401 → refresh → retry',
                   'analytics tracker (lib/)'])
    upload = f.box(525, 415, 240, 130, 'Direct upload', ['the browser PUTs the file', 'to a presigned URL'],
                   colour=YELLOW)
    backend = f.box(15, 670, 495, 60, 'Backend: NestJS 11', colour=GREEN, centre=True, size=17)
    minio = f.box(525, 670, 240, 60, 'Object storage: MinIO', colour=PURPLE, centre=True, size=17)
    f.edge(browser, fe, exit=(0.5, 1), entry=(0.5, 0))
    f.edge(sse, backend, 'SSE stream', exit=(0.5, 1), entry=(0.25, 0))
    f.edge(state, backend, 'REST /api (JSON)', exit=(0.5, 1), entry=(0.75, 0))
    f.edge(upload, minio, 'PUT, presigned,<br>10-minute TTL', exit=(0.5, 1), entry=(0.5, 0))
    f.write()


# ── Logical architecture: backend ────────────────────────────────────────────
def backend():
    f = Figure('fig-3-2-architecture-backend', 'Logical backend architecture')
    front = f.box(150, 0, 220, 50, 'Frontend: Next.js', colour=BLUE, centre=True, size=17)
    api = f.container(0, 90, 520, 600, 'Backend: NestJS 11 (api)', GREEN)
    f.box(15, 135, 490, 80, 'Guards',
          ['ThrottlerGuard on every route, then @Auth():',
           'JwtAuth · Roles · Plans · AccountType · Subscription · AiQuota'],
          colour=YELLOW)
    modules = [
        ('Auth and Users', ['JWT · Google OAuth', 'profiles']),
        ('Articles', ['tags · comments', 'access matrix']),
        ('Social', ['likes · reposts · follows', 'blocks · saves · notifications']),
        ('AI', ['chat · inline · RAG', 'memory · insights · voice']),
        ('Analytics', ['event ingestion', 'rollup reads']),
        ('Marketplace', ['purchases · ledger', 'subscriptions · publishing']),
        ('Search and discovery', ['lexical · semantic · fusion']),
        ('Documents', ['private library · attachment', 'citations']),
        ('Moderation, uploads', ['health and readiness']),
    ]
    for i, (title, lines) in enumerate(modules):
        col, row = i % 2, i // 2
        w = 240 if i < 8 else 490
        f.box(15 + col * 250, 230 + row * 90, w, 80, title, lines)
    worker = f.container(540, 90, 240, 600, 'Worker: same image, second entrypoint', GREEN, size=17)
    queues = [('embeddings', 'chunk · embed · memory'), ('analytics', 'article and writer rollups'),
              ('marketplace', 'eligibility · renewal'), ('ai-tokens', 'nightly UTC reset'),
              ('documents', 'extract · chunk · embed'), ('ai-models', 'daily liveness check')]
    for i, (q, what) in enumerate(queues):
        f.box(555, 160 + i * 87, 210, 77, q, [what])
    # The models sit at the top right, so both of their arrows are short: the
    # api's along the top, the worker's straight up. The three stores below
    # take the api's arrows straight down; Redis and PostgreSQL also take the
    # worker's, and each label sits on a stretch no other label shares.
    ai = f.box(560, 0, 220, 60, 'Groq · Gemini', ['LLM, embeddings, speech'], colour=YELLOW, centre=True)
    minio = f.box(0, 860, 240, 80, 'MinIO', ['images · documents'], colour=PURPLE, centre=True)
    pg = f.box(270, 860, 240, 80, 'PostgreSQL 16 + pgvector', ['relational · tsvector · HNSW'],
               colour=PURPLE, centre=True)
    redis = f.box(540, 860, 240, 80, 'Redis', ['BullMQ broker only'], colour=RED, centre=True)
    f.edge(front, api, 'REST and SSE', exit=(0.5, 1), entry=(0.5, 0))
    f.edge(api, ai, 'Vercel AI SDK', exit=(500 / 520, 0), entry=(0, 0.5), points=[(500, 30)])
    f.edge(worker, ai, 'embeddings', exit=(160 / 240, 0), entry=(140 / 220, 1))
    f.edge(api, minio, 'presign · read', exit=(120 / 520, 1), entry=(0.5, 0))
    f.edge(api, pg, 'Drizzle', exit=(330 / 520, 1), entry=(60 / 240, 0))
    f.edge(api, redis, 'enqueue', exit=(470 / 520, 1), entry=(30 / 240, 0),
           points=[(470, 715), (570, 715)], at=0.3)
    f.edge(worker, redis, 'consume', exit=(80 / 240, 1), entry=(80 / 240, 0), at=-0.5)
    f.edge(worker, pg, 'rollups, chunks', exit=(200 / 240, 1), entry=(180 / 240, 0),
           points=[(740, 815), (450, 815)], at=-0.6)
    f.write()


# ── Physical architecture ────────────────────────────────────────────────────
def physical():
    # The deployment, not the data flow (the logical figures carry that): what
    # runs on the server, what is exposed, and where the data lives. Services
    # are grouped, so each arrow is one straight line.
    f = Figure('fig-3-3-architecture-physical', 'Physical architecture')
    browser = f.box(0, 0, 220, 60, "User's browser", colour=GREY, centre=True, size=17)
    ghcr = f.box(250, 0, 260, 60, 'GHCR', ['images tagged latest and git SHA'], colour=GREY, centre=True)
    ext = f.box(540, 0, 240, 60, 'External APIs', ['Groq · Gemini · Sentry'], colour=YELLOW, centre=True)
    vps = f.container(0, 110, 780, 620, 'VPS: Docker Compose, 8 services', GREY)
    nginx = f.box(15, 150, 470, 105, 'nginx',
                  ['TLS termination · reverse proxy · SSE unbuffered',
                   'routes / → web, /api → api, /storage → minio', 'the only service published: 80, 443'],
                  colour=('#ffe6cc', '#d79b00'))
    apps = f.container(15, 275, 750, 175, 'Application services', ('#ffffff', '#999999'), size=17)
    web = f.box(30, 315, 170, 120, 'web', ['Next.js standalone', 'listens 3000'], colour=BLUE)
    api = f.box(215, 315, 170, 120, 'api', ['NestJS', 'listens 3000,', 'publishes nothing'], colour=GREEN)
    worker = f.box(400, 315, 170, 120, 'worker', ['same image,', 'second entrypoint,', '6 queues'],
                   colour=GREEN)
    migrate = f.box(585, 315, 165, 120, 'migrate', ['one-shot, must exit', '0 before api and', 'worker start'],
                    colour=YELLOW)
    data = f.container(15, 510, 750, 140, 'Data services', ('#ffffff', '#999999'), size=17)
    f.box(30, 550, 230, 90, 'db', ['pgvector/pgvector:pg16', '127.0.0.1:5433'], colour=PURPLE)
    f.box(275, 550, 170, 90, 'redis', ['7-alpine', '127.0.0.1:6379'], colour=RED)
    f.box(460, 550, 290, 90, 'minio', ['public images, served via /storage', 'private documents, only via /api'],
          colour=PURPLE)
    f.box(15, 660, 750, 55, 'Volumes', ['postgres_data · minio_data · redis_data · certbot_webroot'])
    f.edge(browser, nginx, 'HTTPS', exit=(0.5, 1), entry=(95 / 470, 0), at=-0.5)
    f.edge(ghcr, vps, 'docker compose pull', exit=(0.5, 1), entry=(380 / 780, 0))
    f.edge(apps, ext, 'LLM · embeddings · speech · errors', exit=(675 / 750, 0), entry=(150 / 240, 1),
           dashed=True, at=0)
    f.edge(nginx, web, '/', exit=(100 / 470, 1), entry=(85 / 170, 0), at=-0.4)
    f.edge(nginx, api, '/api', exit=(235 / 470, 1), entry=(35 / 170, 0), at=-0.4)
    f.edge(api, data, 'queries, enqueue,<br>presign', exit=(0.5, 1), entry=(285 / 750, 0))
    f.edge(worker, data, 'consume, rollups,<br>documents', exit=(0.5, 1), entry=(470 / 750, 0))
    f.edge(migrate, data, 'schema', exit=(0.5, 1), entry=(652 / 750, 0))
    f.write()


# ── Continuous integration and delivery ──────────────────────────────────────
def cicd():
    f = Figure('fig-3-4-architecture-cicd', 'CI/CD pipeline')
    push = f.box(230, 0, 320, 60, 'Push to main', ['backend.inkwell.ai or frontend.inkwell.ai'],
                 colour=GREY, centre=True)
    ci = f.container(0, 100, 780, 250, 'GitHub Actions: continuous integration', BLUE)
    steps = ['1. Install dependencies (pnpm)', '2. Lint: eslint --max-warnings=0',
             '3. Typecheck: tsc --noEmit', '4. Test: 796 backend tests',
             '5. Schema-drift check', '6. Build the multi-stage image']
    for i, s in enumerate(steps):
        col, row = i // 3, i % 3
        f.box(15 + col * 380, 145 + row * 65, 370, 55, s, colour=YELLOW if i == 4 else WHITE, plain=True)
    ghcr = f.box(0, 410, 360, 70, 'GHCR', ['images tagged latest and git SHA'], colour=PURPLE, centre=True)
    dispatch = f.box(420, 410, 360, 70, 'repository_dispatch', ['to docker.inkwell.ai'],
                     colour=YELLOW, centre=True)
    deploy = f.container(0, 540, 780, 250, 'Deploy workflow: docker.inkwell.ai', GREEN)
    steps = ['1. SSH to the VPS', '2. docker compose pull', '3. migrate runs, must exit 0',
             '4. compose up -d: api, worker, web', '5. Verify /health and /ready',
             '6. nginx reloads with the new upstreams']
    for i, s in enumerate(steps):
        col, row = i // 3, i % 3
        f.box(15 + col * 380, 585 + row * 65, 370, 55, s, colour=YELLOW if i == 2 else WHITE, plain=True)
    f.box(0, 830, 780, 60, 'Build arguments, not runtime configuration',
          ['every NEXT_PUBLIC_* value is inlined by next build: changing one means rebuilding the frontend image'],
          colour=YELLOW)
    f.edge(push, ci, exit=(0.5, 1), entry=(0.5, 0))
    f.edge(ci, ghcr, 'push image', exit=(0.23, 1), entry=(0.5, 0))
    f.edge(ghcr, dispatch, 'on success', exit=(1, 0.5), entry=(0, 0.5))
    f.edge(dispatch, deploy, 'trigger', exit=(0.5, 1), entry=(0.77, 0))
    f.write()


if __name__ == '__main__':
    for draw in (frontend, backend, physical, cicd):
        draw()
    print('wrote the four architecture figures')
