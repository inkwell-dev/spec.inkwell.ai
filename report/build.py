#!/usr/bin/env python3
"""Assemble the report and generate its tables, then hand off to pandoc.

  python3 report/build.py            # writes report/build/report.md (docx flavour)
                                     # and report/build/report-html.md (pdf flavour)

The requirement, backlog and sprint tables are generated from
../10-requirements.md rather than copied, so the report cannot drift from the
specification. Internal dated annotations in that file (amendment notes, "(added
2026-…)") are stripped: the report presents the plan on its own timeline.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE.parent / '10-requirements.md'
OUT = HERE / 'build'
OUT.mkdir(exist_ok=True)

CHAPTERS = ['00-front.md', '01-introduction.md', '02-requirements.md',
            '03-environment-architecture.md', '04-release-1.md', '05-release-2.md',
            '06-release-3.md', '07-release-4.md', '08-conclusion.md']

spec = SPEC.read_text()


def clean(text: str) -> str:
    text = re.sub(r'\s*—\s*\*superseding the manual insert of FR-30 \([^)]*\)\*',
                  ' — superseding the manual insert of FR-30', text)
    text = re.sub(r'\s*\*\((?:amended|added|corrected|updated)[^)]*\)\*', '', text)
    text = re.sub(r'\s*\([^()]*\b20\d\d-\d\d-\d\d[^()]*\)', '', text)
    text = text.replace('**', '')
    return text.strip()


def section(title_prefix: str) -> str:
    start = spec.index(title_prefix)
    nxt = spec.find('\n### ', start + 4)
    nxt2 = spec.find('\n## ', start + 4)
    ends = [e for e in (nxt, nxt2) if e != -1]
    return spec[start:min(ends)] if ends else spec[start:]


def rows(block: str):
    for line in block.splitlines():
        if re.match(r'\|\s*(FR|US)-\d+', line):
            yield [clean(c) for c in line.strip().strip('|').split('|')]


includes = {}

# Functional requirements per actor section (2.1 … 2.6).
for n in range(1, 7):
    block = section(f'### 2.{n} ')
    table = ['| ID | Requirement | Priority | Sprint |', '|---|---|---|---|']
    for r in rows(block):
        table.append(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} |')
    includes[f'fr-2.{n}'] = '\n'.join(table)

# Backlog.
backlog_start = spec.index('## 4. Product backlog')
backlog_end = spec.index('## 5. Release plan')
backlog = spec[backlog_start:backlog_end]
epics = re.split(r'\n### ', backlog)[1:]
stories = []          # (epic, id, story, actor, pri, pts, sprint)
summary = ['| Epic | Stories | Points |', '|---|---:|---:|']
full = []
for e in epics:
    name = e.splitlines()[0].strip()
    rs = list(rows(e))
    pts = 0
    full.append(f'**{name}**\n')
    full.append('| ID | User story | Actor | Priority | Points | Sprint |')
    full.append('|---|---|---|---|---:|---|')
    for r in rs:
        if len(r) == 5:            # E9 has no actor column
            r = [r[0], r[1], '—', r[2], r[3], r[4]]
        stories.append((name, *r))
        pts += int(r[4])
        full.append(f'| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |')
    full.append('')
    summary.append(f'| {name} | {len(rs)} | {pts} |')
summary.append(f'| **Total** | **{len(stories)}** | **{sum(int(s[5]) for s in stories)}** |')
includes['backlog-summary'] = '\n'.join(summary)
includes['backlog'] = '**Table 2.9 (continued) – The product backlog, by epic**\n\n' + '\n'.join(full)

# Sprint backlogs.
for n in range(1, 10):
    t = ['| ID | User story | Priority | Points |', '|---|---|---|---:|']
    sel = [s for s in stories if str(n) in [x.strip() for x in s[6].split(',')]]
    for s in sel:
        t.append(f'| {s[1]} | {s[2]} | {s[4]} | {s[5]} |')
    t.append(f'| | **{len(sel)} stories** | | **{sum(int(s[5]) for s in sel)}** |')
    includes[f'sprint-{n}'] = '\n'.join(t)

assert len(stories) == 72, len(stories)

body = '\n\n'.join((HERE / c).read_text() for c in CHAPTERS)
for key, value in includes.items():
    body = body.replace(f'<!-- INCLUDE:{key} -->', value)
assert '<!-- INCLUDE:' not in body, re.findall(r'<!-- INCLUDE:[^ ]+', body)

# Lists of figures and tables, from the captions in order of appearance.
figs = re.findall(r'!\[(Figure [0-9.]+ – [^\]]+)\]|^\*\*(Figure [0-9.]+ – [^*]+)\*\*$', body, re.M)
figs = [a or b for a, b in figs]
tabs = re.findall(r'^\*\*(Table [0-9.]+ – [^*]+)\*\*$', body, re.M)
lists = ('# List of figures {.unnumbered}\n\n' + '\n'.join(f'- {f}' for f in figs) +
         '\n\n\\newpage\n\n# List of tables {.unnumbered}\n\n' +
         '\n'.join(f'- {t}' for t in tabs) + '\n\n\\newpage\n')

PAGE_DOCX = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'
PAGE_HTML = '<div class="pagebreak"></div>'
TOC_DOCX = ('# Table of contents {.unnumbered}\n\n```{=openxml}\n'
            '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/>'
            '<w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText>'
            '<w:fldChar w:fldCharType="separate"/><w:t>Right-click and choose Update Field to build the table of contents.</w:t>'
            '<w:fldChar w:fldCharType="end"/></w:r></w:p>\n```\n\n\\newpage\n')

heads = re.findall(r'^(#{1,2}) (.+?)(?: \{[^}]*\})?$', body, re.M)
toc_html = '# Table of contents {.unnumbered}\n\n' + '\n'.join(
    ('- ' if h == '#' else '    - ') + t for h, t in heads
    if t not in ('Acknowledgements', 'Abstract', 'Résumé', 'List of acronyms',
                 'End-of-Studies Project Report', 'Inkwell.ai')) + '\n\n\\newpage\n'

marker = '# General introduction'
docx = body.replace(marker, TOC_DOCX + '\n' + lists + '\n' + marker, 1).replace('\\newpage', PAGE_DOCX)
html = body.replace(marker, toc_html + '\n' + lists + '\n' + marker, 1).replace('\\newpage', PAGE_HTML)
(OUT / 'report.md').write_text(docx)
(OUT / 'report-html.md').write_text(html)
print(f'{len(figs)} figures, {len(tabs)} tables, {len(stories)} stories; '
      f'{len(body.split())} words')
