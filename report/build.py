#!/usr/bin/env python3
"""Assemble the report, generate its tables, and write the pandoc inputs.

  python3 report/build.py      # writes build/report-latex.md and build/report-docx.md
  report/make-pdf.sh           # runs build.py, then pandoc → LuaLaTeX and pandoc → DOCX

Conventions in the chapter sources
----------------------------------
* Headings carry no numbers; LaTeX numbers them. `{.unnumbered}` for the
  chapter introductions and conclusions.
* A figure is `![Caption](path){#fig:id}` and is cited as `@fig:id`; a table is
  followed by `: Caption {#tbl:id}` and cited as `@tbl:id`; a section is cited
  as `@sec:id`. pandoc-crossref numbers all of them by chapter.
* A bibliography entry is cited as `[@key]` (references.bib, IEEE style).
* `<!-- INCLUDE:name -->` is replaced by a table generated here.

The requirement, backlog and sprint tables are generated from
../10-requirements.md rather than copied, so the report cannot drift from the
specification. Dated annotations in that file are stripped: the report presents
the plan on its own timeline.
"""
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE.parent / '10-requirements.md'
DIAGRAMS = HERE.parent / 'diagrams'
SCREENS = HERE.parent / 'figures' / 'screens'
OUT = HERE / 'build'
OUT.mkdir(exist_ok=True)

FRONT = ['00-front.md']
BODY = ['01-introduction.md', '02-context-requirements.md',
        '04-release-1.md', '05-release-2.md', '06-release-3.md', '07-release-4.md',
        '08-evaluation.md', '09-conclusion.md']
ANNEX = ['10-annexes.md']

spec = SPEC.read_text()


def clean(text: str) -> str:
    text = re.sub(r'\s*—\s*\*superseding the manual insert of FR-30 \([^)]*\)\*',
                  ', superseding the manual insert of FR-30', text)
    text = re.sub(r'\s*\*\((?:amended|added|corrected|updated)[^)]*\)\*', '', text)
    text = re.sub(r'\s*\([^()]*\b20\d\d-\d\d-\d\d[^()]*\)', '', text)
    text = text.replace('**', '')
    return text.strip()


def section(title_prefix: str) -> str:
    start = spec.index(title_prefix)
    ends = [e for e in (spec.find('\n### ', start + 4), spec.find('\n## ', start + 4)) if e != -1]
    return spec[start:min(ends)] if ends else spec[start:]


def rows(block: str):
    for line in block.splitlines():
        if re.match(r'\|\s*(FR|US)-\d+', line):
            yield [clean(c) for c in line.strip().strip('|').split('|')]


def num(ident: str) -> int:
    return int(ident.split('-')[1])


def short_title(story: str) -> str:
    """The goal of a user story, without its "so that…" clause."""
    goal = re.split(r',? so that | — so that ', story, maxsplit=1)[0]
    goal = re.split(r',? without anyone', goal, maxsplit=1)[0]
    goal = goal.strip().rstrip(',')
    return goal[0].upper() + goal[1:]


includes = {}

# ── Functional requirements ──────────────────────────────────────────────────
ACTOR_SECTIONS = [
    (1, 'Visitor (A1)', 'visitor'),
    (2, 'Reader (A2)', 'readers'),
    (3, 'Writer (A3)', 'writers'),
    (4, 'Magazine (A4)', 'magazines'),
    (5, 'Administrator (A5)', 'administrator'),
    (6, 'Cross-cutting', 'cross-cutting'),
]
fr_all = []
summary = ['| Actor | Requirements | Must | Should | Could | Sprints |',
           '|:----------------------|:-:|:-:|:-:|:-:|:------|']
for n, actor, slug in ACTOR_SECTIONS:
    rs = sorted(rows(section(f'### 2.{n} ')), key=lambda r: num(r[0]))
    fr_all += rs
    pri = Counter(r[2] for r in rs)
    sprints = sorted({int(s) for r in rs for s in r[3].split(',') if s.strip().isdigit()})
    summary.append(f'| {actor} | {len(rs)} | {pri["Must"]} | {pri["Should"]} | {pri["Could"]} | '
                   f'{", ".join(map(str, sprints))} |')
    table = ['| ID | Requirement | Priority | Sprint |', '|:----|:------------------------------------------|:---|:--|']
    table += [f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |' for r in rs]
    includes[f'fr-{slug}'] = '\n'.join(table) + f'\n\n: Functional requirements: {actor.split(" (")[0].lower()} {{#tbl:fr-{slug}}}'
pri = Counter(r[2] for r in fr_all)
summary.append(f'| **Total** | **{len(fr_all)}** | **{pri["Must"]}** | **{pri["Should"]}** | **{pri["Could"]}** | |')
includes['fr-summary'] = '\n'.join(summary) + '\n\n: Functional requirements by actor and priority {#tbl:fr-summary}'
FR_COUNT, FR_MUST = len(fr_all), pri['Must']

# ── Backlog ──────────────────────────────────────────────────────────────────
backlog = spec[spec.index('## 4. Product backlog'):spec.index('## 5. Release plan')]
stories = []           # dicts
epic_rows = []
annex = []
for e in re.split(r'\n### ', backlog)[1:]:
    name = e.splitlines()[0].strip()
    rs = []
    for r in rows(e):
        if len(r) == 5:            # E9 has no actor column
            r = [r[0], r[1], 'none', r[2], r[3], r[4]]
        rs.append(dict(epic=name, id=r[0], story=r[1], actor=r[2], pri=r[3], pts=int(r[4]),
                       sprints=[s.strip() for s in r[5].split(',')]))
    rs.sort(key=lambda s: num(s['id']))
    stories += rs
    epic_rows.append((name, len(rs), sum(s['pts'] for s in rs)))
    annex.append(f'\n**{name}**\n')
    annex.append('| ID | User story | Actor | Priority | Points | Sprint |')
    annex.append('|:----|:--------------------------------------------|:--|:---|:-:|:-:|')
    annex += [f'| {s["id"]} | {s["story"]} | {s["actor"]} | {s["pri"]} | {s["pts"]} | {", ".join(s["sprints"])} |'
              for s in rs]
TOTAL_PTS = sum(s['pts'] for s in stories)
summary = ['| Epic | Stories | Points | Share of points |', '|:------------------------------------|:-:|:-:|:-:|']
summary += [f'| {n} | {c} | {p} | {100 * p / TOTAL_PTS:.0f}% |' for n, c, p in epic_rows]
summary.append(f'| **Total** | **{len(stories)}** | **{TOTAL_PTS}** | 100% |')
includes['backlog-summary'] = '\n'.join(summary) + '\n\n: Product backlog by epic {#tbl:backlog-summary}'
includes['backlog-annex'] = '\n'.join(annex)

# ── Sprint backlogs ──────────────────────────────────────────────────────────
sprint_pts = {}
for n in range(1, 10):
    sel = sorted((s for s in stories if str(n) in s['sprints']), key=lambda s: num(s['id']))
    sprint_pts[n] = sum(s['pts'] for s in sel)
    t = ['| ID | User story (goal) | Priority | Points |', '|:----|:---------------------------------------------|:---|:-:|']
    t += [f'| {s["id"]} | {short_title(s["story"])} | {s["pri"]} | {s["pts"]} |' for s in sel]
    t.append(f'| | **{len(sel)} stories** | | **{sprint_pts[n]}** |')
    includes[f'sprint-{n}'] = '\n'.join(t) + f'\n\n: Sprint {n} backlog {{#tbl:sprint-{n}}}'

assert len(stories) == 77, len(stories)

# ── Numbers the prose quotes, checked against the generated tables ───────────
FACTS = {
    'STORIES': str(len(stories)), 'POINTS': str(TOTAL_PTS), 'FRS': str(FR_COUNT), 'FR_MUST': str(FR_MUST),
    **{f'S{n}PTS': str(p) for n, p in sprint_pts.items()},
}


def assemble(files):
    return '\n\n'.join((HERE / f).read_text() for f in files)


def expand(text: str) -> str:
    for key, value in includes.items():
        text = text.replace(f'<!-- INCLUDE:{key} -->', value)
    assert '<!-- INCLUDE:' not in text, re.findall(r'<!-- INCLUDE:[^ ]+', text)
    for key, value in FACTS.items():
        text = text.replace(f'{{{{{key}}}}}', value)
    left = re.findall(r'\{\{[A-Z0-9_]+\}\}', text)
    if os.environ.get('DRAFT'):
        text = re.sub(r'\{\{[A-Z0-9_]+\}\}', '**??**', text)
    else:
        assert not left, left
    return text


# ── Images: the right file for each output ───────────────────────────────────
def image_for(path: str, flavour: str) -> str:
    """Diagrams are vector in the PDF: draw.io as a cropped PDF, PlantUML as SVG
    (pandoc converts it with rsvg-convert). Screenshots stay PNG."""
    m = re.match(r'\.\./diagrams/([^/]+)/\1\.png$', path)
    if not m or flavour == 'docx':
        return path
    name = m.group(1)
    if (DIAGRAMS / name / f'{name}.drawio').exists():
        assert (DIAGRAMS / name / f'{name}.pdf').exists(), f'export {name}.pdf first (make-pdf.sh does)'
        return f'../diagrams/{name}/{name}.pdf'
    return f'../diagrams/{name}/{name}.svg'


def images(text: str, flavour: str) -> str:
    def fig(m):
        caption, path, attrs = m.group(1), m.group(2), m.group(3) or ''
        if not re.search(r'\bwidth=', attrs):
            attrs += ' width=80%' if 'figures/screens/' in path else ' width=100%'
        if not re.search(r'\bheight=', attrs):
            # A sequence diagram is tall and narrow: give it most of the page
            # height, or its width, and its text, shrink to fit.
            attrs += (' height=38%' if 'figures/screens/' in path
                      else ' height=88%' if '-sequence-' in path else ' height=72%')
        return f'![{caption}]({image_for(path, flavour)}){{{attrs.strip()}}}'
    return re.sub(r'!\[([^\]]*)\]\(([^)]+)\)(?:\{([^}]*)\})?', fig, text)


figure_files = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', assemble(BODY + ANNEX))
missing = [f for f in figure_files if not (HERE / f).exists()]
assert not missing, missing

# ── Title page and front matter ──────────────────────────────────────────────
# The cover follows the house layout of TEK-UP reports: the school's logo and
# the host company's in the top corners, the institution centred in bold, the
# report type in small capitals, the author, the project title between double
# rules with the Inkwell mark above it, the supervisors as label-left and
# name-right rows, and the academic year at the foot. The cover alone is set in
# Latin Modern, the reference cover's typeface, which has true small capitals.
# LaTeX compiles in a temporary directory inside the pandoc container, where
# the spec is mounted at /data, so the logos are given by absolute path.
TITLE_LATEX = r'''```{=latex}
\begin{titlepage}
\definecolor{coverrule}{HTML}{1F3A5F}
\newcommand{\coverlogos}{/data/report/Logos}
\newgeometry{top=2.0cm,bottom=2.0cm,left=2.6cm,right=2.6cm}
\fontspec{Latin Modern Roman}[SmallCapsFont={Latin Modern Roman Caps}]
% Logos: the school top left, the host company top right.
\noindent
\begin{minipage}[c]{0.5\textwidth}\raggedright
\includegraphics[height=1.2cm,width=0.85\linewidth,keepaspectratio]{\coverlogos/tekup_logo.jpeg}
\end{minipage}%
\begin{minipage}[c]{0.5\textwidth}\raggedleft
\includegraphics[height=1.15cm,width=0.85\linewidth,keepaspectratio]{\coverlogos/intuitiv_logo.png}
\end{minipage}
\par\vspace{0.9cm}
\centering
% The institution.
{\bfseries\normalsize TEK-UP University\par}
\vspace{5pt}
{\bfseries\normalsize GLSI (Software Engineering and Information Systems)\par}
\vspace{0.9cm}
% The report.
{\LARGE\scshape End-of-Studies Project Report\par}
\vspace{8pt}
{\normalsize Submitted in partial fulfilment of the requirements for the degree of\par}
\vspace{2pt}
{\normalsize\bfseries National Engineering Diploma in Computer Science (GLSI)\par}
\vspace{0.75cm}
{\large\itshape Carried out by\par}
\vspace{5pt}
{\Large\bfseries Oussama Bejaoui\par}
\vspace{0.8cm}
% The project: the Inkwell mark above the title, between double rules.
{\color{coverrule}\rule{\linewidth}{1.4pt}\par\vspace{5pt}\rule{\linewidth}{0.5pt}\par}
\vspace{14pt}
\includegraphics[height=1.6cm]{\coverlogos/inkwell_logo.png}\par
\vspace{8pt}
% As in the reference: the project's name in bold, leading the title.
{\LARGE\setlength{\baselineskip}{1.35\baselineskip}\textbf{Inkwell.ai:} An AI-powered writing marketplace\\
connecting independent writers and magazine publishers\par}
\vspace{14pt}
{\color{coverrule}\rule{\linewidth}{0.5pt}\par\vspace{5pt}\rule{\linewidth}{1.4pt}\par}
\vspace{0.8cm}
% The supervisors: label on the left, name on the right.
{\normalsize
\begin{tabular*}{0.96\linewidth}{@{\extracolsep{\fill}}lr@{}}
Academic supervisor: & \textbf{Mr. Bilel Zemzem} \\[8pt]
Professional supervisor: & \textbf{Mr. Ramzy Chridi} \\[8pt]
Host organisation: & \textbf{Intuitiv Group} \\
\end{tabular*}\par}
\vfill
% The period and the academic year.
{\normalsize Project period: 1 February 2026 – 31 July 2026\par}
\vspace{8pt}
{\large\bfseries Academic year:\par}
\vspace{3pt}
{\large\bfseries 2025–2026\par}
\end{titlepage}
\restoregeometry
```'''

LISTS_LATEX = '```{=latex}\n{\\setstretch{1.0}\\tableofcontents\\listoffigures\\listoftables}\n```\n'
LISTS_DOCX = ('# Table of contents {.unnumbered}\n\n```{=openxml}\n'
              '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/>'
              '<w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>'
              '<w:fldChar w:fldCharType="separate"/><w:t>Right-click and choose Update Field to build the table of contents.</w:t>'
              '<w:fldChar w:fldCharType="end"/></w:r></w:p>\n```\n\n'
              '\\listoffigures\n\n\\listoftables\n')

front_docx = (HERE / FRONT[0]).read_text()
front_latex = re.sub(r'::: \{\.titlepage\}.*?\n:::\n', lambda m: TITLE_LATEX + '\n', front_docx, flags=re.S)
body = expand(assemble(BODY))
annexes = expand(assemble(ANNEX))
refs = '# References {.unnumbered}\n\n::: {#refs}\n:::\n'

for flavour in ('latex', 'docx'):
    f = front_latex if flavour == 'latex' else front_docx
    lists = LISTS_LATEX if flavour == 'latex' else LISTS_DOCX
    f = f.replace('<!-- LISTS -->', lists)
    main = '```{=latex}\n\\mainmatter\n```\n\n' if flavour == 'latex' else ''
    appendix = '```{=latex}\n\\appendix\n\\AtBeginEnvironment{longtable}{\\footnotesize}\n```\n\n' if flavour == 'latex' else ''
    start = '```{=latex}\n\\frontmatter\n```\n\n' if flavour == 'latex' else ''
    doc = start + f + '\n\n' + main + body + '\n\n' + refs + '\n\n' + appendix + annexes
    doc = images(doc, flavour)
    if flavour == 'docx':
        doc = doc.replace('\\newpage', '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```')
    (OUT / f'report-{flavour}.md').write_text(doc)

print(f'{len(figure_files)} figures; {len(stories)} stories, {TOTAL_PTS} points; '
      f'{FR_COUNT} FRs ({FR_MUST} Must); sprint points {sprint_pts}; '
      f'{len(body.split()) + len(annexes.split())} words in the body and annexes')
