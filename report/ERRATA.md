---
title: "Inkwell.ai — Errata to the printed report"
author: "Oussama Bejaoui"
geometry: [a4paper, margin=16mm]
fontsize: 10pt
mainfont: "Liberation Serif"
header-includes:
  - \pagestyle{empty}
  - \usepackage{booktabs}
  - \renewcommand{\arraystretch}{1.15}
---

\thispagestyle{empty}

Page numbers refer to the printed copy. None of these corrections changes a
result: each brings a sentence or a figure back in line with the tables and the
code it describes. A corrected PDF is available.

| Page | Printed | Correct |
|:--------|:--------------------------|:--------------------------|
| 5, Fig. 1.2 | "74 user stories" | 77 user stories |
| 5, Fig. 1.2 | Role note: all 3 roles held by one person, followed by a writing note | The author holds Scrum Master and Developer; the academic supervisor is Product Owner at sprint boundaries (as in §1.2.2). The writing note is removed |
| 7 | "The administrator carries the fewest (5)" | The administrator carries 8; the cross-cutting requirements are the fewest (4) |
| 14 | AI epic 21%, marketplace 18%, E9 12% | 20%, 17%, 11%, as in Table 1.4 |
| 14 | A purchase records "2 or 3" Transaction rows (p. 63: "writes 3") | Up to 3: each row is written only when its amount is above zero |
| 15, 101 | "Sprint 5 commits 85 points"; "from 16 to 85 points" | 98 points, as in Tables 1.5, 4.1 and 6.6 |
| 19 | "Redis also carries the notification fan-out" | Removed: notifications are pushed from memory by the API; Redis is the BullMQ broker only (Fig. 1.8) |
| 27 | US-49, US-50, US-51 are "almost a fifth" of Sprint 1 | 21 of 45 points: almost half |
| 29 | Article "carries … search vector" | Not shown in Fig. 2.2; the sentence now lists status, placement and visibility |
| 44, 46, 65 | Eligibility rechecked "after each aggregation" (Fig. 3.4) | A separate job every 20 minutes; writer rollups run every 15 minutes. Fig. 3.4 redrawn |
| 77, Fig. 4.24 | "792 backend tests in 51 suites" | 796 tests in 52 suites, as in Table 4.4 |
| 86, 89 | Diagram labels "figure 7.5", "figure 7.4" | Figures 5.9 and 5.8 |
| 91 | Sprint 9 is "the lightest load after Sprint 7" | Sprint 9 (16 points) is the lightest; Sprint 7 has 18 |
| 97 | "about 1,000 embeddings a day … within one day's quota" | The 1,202 passages were embedded ahead of the evaluation; the evaluation itself embeds only its 54 queries |
| 101, Table 6.6 | Total: 363 committed, **342** delivered; "about 38 points per sprint" | **355** delivered (97.8%): US-14 (13 points) spans Sprints 2 and 4 and is counted once. About 40 points per sprint |

**Layout.** Four figures were printed before the figure that precedes them
(3.4 before 3.3, 3.15 before 3.14, 4.4 before 4.3, 5.12 before 5.11), and some
running headers named the wrong part (the acronyms, conclusion and reference
pages, and "Chapter A/B" for the appendices). Both are fixed in the corrected
PDF, where these figures are numbered in reading order.
