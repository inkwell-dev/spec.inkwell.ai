#!/usr/bin/env python3
"""Generate the four architecture figures as editable .drawio files.

These are the figures where colour is allowed: the example report keeps UML
strictly black and white, and reserves pastel fills with nested group boxes for
architecture and infrastructure. Palette below is draw.io's own default set,
which is what their figures use.
"""
BLUE   = "fillColor=#DAE8FC;strokeColor=#6C8EBF;"
GREEN  = "fillColor=#D5E8D4;strokeColor=#82B366;"
AMBER  = "fillColor=#FFF2CC;strokeColor=#D6B656;"
RED    = "fillColor=#F8CECC;strokeColor=#B85450;"
PURPLE = "fillColor=#E1D5E7;strokeColor=#9673A6;"
ORANGE = "fillColor=#FFE6CC;strokeColor=#D79B00;"
GREY   = "fillColor=#F5F5F5;strokeColor=#666666;"
WHITE  = "fillColor=#FFFFFF;strokeColor=#000000;"

GRP  = "rounded=1;whiteSpace=wrap;html=1;verticalAlign=top;fontStyle=1;fontSize=13;arcSize=4;"
BOX  = "rounded=0;whiteSpace=wrap;html=1;verticalAlign=top;align=left;spacingLeft=8;fontSize=11;"
HEAD = "rounded=0;whiteSpace=wrap;html=1;fontStyle=1;fontSize=12;"
EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;"
        "fontSize=10;labelBackgroundColor=#FFFFFF;")
# Pinned exit/entry sides. Left to itself draw.io routes edges straight through
# other boxes and occasionally snaps to the wrong shape; naming the sides makes
# routing deterministic.
EV  = EDGE + "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
EH  = EDGE + "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
EHL = EDGE + "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"

def cell(i, label, x, y, w, h, style):
    return (f'<mxCell id="{i}" value="{label}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def edge(i, s, t, label="", style=EDGE):
    return (f'<mxCell id="{i}" value="{label}" style="{style}" edge="1" parent="1" '
            f'source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>')

def write(name, title, cells, w=1300, h=900):
    xml = ('<mxfile host="Electron" type="device">\n'
           f'  <diagram id="{name}" name="{title}">\n'
           f'    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
           f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
           f'pageWidth="{w}" pageHeight="{h}" math="0" shadow="0">\n'
           '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        '
           + "\n        ".join(cells) +
           '\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n')
    open(f"../{name}/{name}.drawio", "w").write(xml)
    print(f"wrote {name}.drawio")

# ── Figure 3.1 — logical frontend ────────────────────────────────────────────
c = [
    cell("browser", "Browser", 520, 20, 200, 40, HEAD + GREY),
    cell("fe", "Frontend — Next.js 15, App Router", 60, 100, 1140, 380, GRP + BLUE),
    cell("routes", "Routes (app/)&lt;br&gt;&lt;br&gt;/ · /articles/[slug]&lt;br&gt;/editor/[id] · /search&lt;br&gt;/dashboard · /discover&lt;br&gt;/m/[slug] · /admin",
         100, 150, 240, 150, BOX + WHITE),
    cell("features", "Features (features/)&lt;br&gt;&lt;br&gt;editor — TipTap&lt;br&gt;ai-chat · inline actions&lt;br&gt;analytics capture&lt;br&gt;marketplace · notifications",
         370, 150, 240, 150, BOX + WHITE),
    cell("state", "State and data&lt;br&gt;&lt;br&gt;React Query&lt;br&gt;Zustand&lt;br&gt;axios interceptors&lt;br&gt;401 → refresh → retry",
         640, 150, 240, 150, BOX + WHITE),
    cell("mw", "Edge middleware&lt;br&gt;&lt;br&gt;route protection&lt;br&gt;before the page renders",
         910, 150, 250, 150, BOX + WHITE),
    cell("sse", "SSE client — EventSource, live notifications", 100, 330, 380, 60, BOX + AMBER),
    cell("upload", "Direct upload — browser PUTs to presigned URL", 520, 330, 380, 60, BOX + AMBER),
    cell("be", "Backend — NestJS 11", 400, 560, 400, 60, HEAD + GREEN),
    cell("store", "Object storage — MinIO", 900, 560, 260, 60, HEAD + PURPLE),
    edge("e1", "browser", "fe", "", EV),
    edge("e2", "state", "be", "REST /api (HTTP/JSON)", EV),
    edge("e3", "sse", "be", "GET /api/notifications/stream", EV),
    edge("e4", "upload", "store", "PUT, presigned, 10-minute TTL", EV),
]
write("fig-3-1-architecture-frontend", "Figure 3.1 - Logical frontend architecture", c, 1300, 700)

# ── Figure 3.2 — logical backend ─────────────────────────────────────────────
c = [
    cell("fe2", "Frontend — Next.js", 520, 20, 240, 40, HEAD + BLUE),
    cell("be2", "Backend — NestJS 11 (api)", 40, 100, 900, 430, GRP + GREEN),
    cell("guards", "Guards, composed once by @Auth()&lt;br&gt;JwtAuth · Roles · Plans · AccountType · Subscription · AiQuota",
         80, 150, 820, 60, BOX + AMBER),
    cell("m1", "Auth and Users&lt;br&gt;JWT · Google OAuth&lt;br&gt;profiles", 80, 240, 190, 90, BOX + WHITE),
    cell("m2", "Articles&lt;br&gt;tags · comments&lt;br&gt;access matrix", 290, 240, 190, 90, BOX + WHITE),
    cell("m3", "Social&lt;br&gt;likes · reposts&lt;br&gt;follows · notifications", 500, 240, 190, 90, BOX + WHITE),
    cell("m4", "AI&lt;br&gt;chat · inline · RAG&lt;br&gt;memory · insights", 710, 240, 190, 90, BOX + WHITE),
    cell("m5", "Analytics&lt;br&gt;event ingestion&lt;br&gt;rollup reads", 80, 350, 190, 90, BOX + WHITE),
    cell("m6", "Marketplace&lt;br&gt;purchases · ledger&lt;br&gt;subscriptions", 290, 350, 190, 90, BOX + WHITE),
    cell("m7", "Search&lt;br&gt;lexical · semantic&lt;br&gt;fusion", 500, 350, 190, 90, BOX + WHITE),
    cell("m8", "Moderation, uploads&lt;br&gt;health and readiness", 710, 350, 190, 90, BOX + WHITE),
    cell("wk", "Worker — same image, second entrypoint", 980, 100, 280, 430, GRP + GREEN),
    cell("q1", "embeddings&lt;br&gt;chunk · embed · memory", 1005, 150, 230, 70, BOX + WHITE),
    cell("q2", "analytics&lt;br&gt;article and writer rollups", 1005, 240, 230, 70, BOX + WHITE),
    cell("q3", "marketplace&lt;br&gt;eligibility · renewal", 1005, 330, 230, 70, BOX + WHITE),
    cell("q4", "ai-tokens&lt;br&gt;nightly UTC reset", 1005, 420, 230, 70, BOX + WHITE),
    cell("pg", "PostgreSQL 16 + pgvector&lt;br&gt;relational · tsvector · HNSW", 60, 600, 300, 70, HEAD + PURPLE),
    cell("rd", "Redis&lt;br&gt;BullMQ broker only", 400, 600, 240, 70, HEAD + RED),
    cell("mn", "MinIO&lt;br&gt;object storage", 680, 600, 220, 70, HEAD + PURPLE),
    cell("ext", "Groq · Gemini&lt;br&gt;LLM, embeddings, moderation", 950, 600, 300, 70, HEAD + AMBER),
    edge("f1", "fe2", "be2", "REST and SSE", EV),
    edge("f2", "m5", "pg", "Drizzle", EV),
    edge("f3", "m6", "rd", "enqueue", EV),
    edge("f4", "q4", "rd", "consume", EHL),
    edge("f5", "q2", "pg", "", EHL),
    edge("f6", "m8", "mn", "presign", EV),
    edge("f7", "m4", "ext", "Vercel AI SDK", EV),
]
write("fig-3-2-architecture-backend", "Figure 3.2 - Logical backend architecture", c, 1320, 730)

# ── Figure 3.3 — physical architecture ───────────────────────────────────────
# Layout note: nginx sits above the three application containers and the
# datastores sit below them, so every edge that is short is also true. An earlier
# arrangement had shorter routes but drew web -> api and web -> redis, neither of
# which exists: nginx proxies to api, and only api and the worker open Redis.
c = [
    cell("user", "User's browser", 80, 30, 240, 50, HEAD + GREY),
    cell("ghcr", "GHCR — images tagged latest and git SHA", 940, 30, 320, 50, HEAD + GREY),
    cell("vps", "VPS — Docker Compose, 8 services", 40, 110, 1220, 610, GRP + GREY),
    cell("nginx", "nginx&lt;br&gt;TLS termination · reverse proxy · SSE unbuffered&lt;br&gt;the only service published publicly: 80, 443",
         420, 160, 460, 80, BOX + ORANGE),
    cell("web", "web&lt;br&gt;Next.js standalone&lt;br&gt;listens 3000", 80, 300, 240, 80, BOX + BLUE),
    cell("api", "api&lt;br&gt;NestJS&lt;br&gt;listens 3000, publishes nothing", 380, 300, 240, 80, BOX + GREEN),
    cell("worker", "worker&lt;br&gt;same image, second entrypoint&lt;br&gt;4 queues", 680, 300, 240, 80, BOX + GREEN),
    cell("migrate", "migrate&lt;br&gt;one-shot, must exit 0&lt;br&gt;before api and worker start", 980, 300, 240, 80, BOX + AMBER),
    cell("db", "db&lt;br&gt;pgvector/pgvector:pg16&lt;br&gt;127.0.0.1:5433", 80, 440, 260, 80, BOX + PURPLE),
    cell("redis", "redis&lt;br&gt;7-alpine&lt;br&gt;127.0.0.1:6379", 380, 440, 240, 80, BOX + RED),
    cell("minio", "minio&lt;br&gt;S3 API proxied by nginx at /storage&lt;br&gt;console on 127.0.0.1:9001 only",
         660, 440, 300, 80, BOX + PURPLE),
    cell("ext3", "Groq · Gemini&lt;br&gt;Sentry", 1000, 440, 220, 80, BOX + AMBER),
    cell("vols", "Volumes — postgres_data · minio_data · redis_data · certbot_webroot", 80, 580, 1140, 50, BOX + WHITE),
    edge("g1", "user", "nginx", "HTTPS", EV),
    edge("g2", "nginx", "web", "/", EV),
    edge("g3", "nginx", "api", "/api", EV),
    edge("g4", "api", "db", "", EV),
    edge("g5", "api", "redis", "enqueue", EV),
    edge("g6", "worker", "redis", "consume", EV),
    edge("g7", "worker", "ext3", "embeddings", EV),
    edge("g8", "migrate", "db", "", EV),
    edge("g9", "ghcr", "vps", "docker compose pull", EV),
    edge("g10", "api", "minio", "presign", EV),
    edge("g11", "api", "ext3", "completions", EV),
]
write("fig-3-3-architecture-physical", "Figure 3.3 - Physical architecture", c, 1320, 790)

# ── Figure 3.4 — CI/CD pipeline ──────────────────────────────────────────────
c = [
    cell("push", "Push to main&lt;br&gt;backend.inkwell.ai or frontend.inkwell.ai", 40, 40, 300, 70, HEAD + GREY),
    cell("ci", "GitHub Actions — continuous integration", 40, 160, 620, 250, GRP + BLUE),
    cell("s1", "1. Install dependencies (pnpm)", 70, 210, 260, 40, BOX + WHITE),
    cell("s2", "2. Lint — eslint --max-warnings=0", 70, 260, 260, 40, BOX + WHITE),
    cell("s3", "3. Typecheck — tsc --noEmit", 70, 310, 260, 40, BOX + WHITE),
    cell("s4", "4. Test — 479 backend tests", 360, 210, 270, 40, BOX + WHITE),
    cell("s5", "5. Schema-drift check", 360, 260, 270, 40, BOX + AMBER),
    cell("s6", "6. Build the multi-stage image", 360, 310, 270, 40, BOX + WHITE),
    cell("ghcr2", "GHCR&lt;br&gt;tagged latest and git SHA", 740, 220, 260, 80, HEAD + PURPLE),
    cell("disp", "repository_dispatch&lt;br&gt;to docker.inkwell.ai", 740, 350, 260, 80, HEAD + AMBER),
    cell("dep", "Deploy workflow — docker.inkwell.ai", 40, 470, 960, 240, GRP + GREEN),
    cell("d1", "1. SSH to the VPS", 70, 520, 280, 40, BOX + WHITE),
    cell("d2", "2. docker compose pull", 70, 570, 280, 40, BOX + WHITE),
    cell("d3", "3. migrate runs, must exit 0", 70, 620, 280, 40, BOX + AMBER),
    cell("d4", "4. compose up -d — api, worker, web", 390, 520, 300, 40, BOX + WHITE),
    cell("d5", "5. Verify /health and /ready", 390, 570, 300, 40, BOX + WHITE),
    cell("d6", "6. nginx reloads with the new upstreams", 390, 620, 300, 40, BOX + WHITE),
    cell("note4", "Build args, not runtime config: every NEXT_PUBLIC_* value is inlined "
                  "by next build, so changing one means rebuilding the frontend image.",
         1040, 220, 240, 210, BOX + AMBER),
    edge("h1", "push", "ci", "", EV),
    edge("h2", "s6", "ghcr2", "push image", EH),
    edge("h3", "ghcr2", "disp", "on success", EV),
    edge("h4", "disp", "dep", "trigger", EHL),
]
write("fig-3-4-architecture-cicd", "Figure 3.4 - CI/CD pipeline", c, 1340, 780)
