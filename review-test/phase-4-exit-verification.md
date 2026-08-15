# Phase 4 — Exit Criteria Verification

**Date:** 2026-08-15 · **Sprint:** S6 (Aug 10–23) · **Result: 6 of 6 pass**

Phase 4's implementation was complete; only its six exit criteria were unverified.
This is the record of verifying them against the running dev stack — real Gemini
embeddings, real Groq completions, real Postgres.

Two of the six had never been exercised at all. `portfolio_insights` held **zero
rows** since the feature shipped on 2026-08-11, because generation is an explicit
click by design and nobody had ever clicked it. The headline magazine-facing demo
was therefore unproven, and so was the cache invalidation that depends on it.

**Environment:** full dev stack (`make dciup-all`), corpus of 33 live published
articles / 62 chunks at the start.

---

## 1. Publish 5+ articles with distinct topics/vocabulary — PASS

The Phase Q demo seed supplies five writers with deliberately non-overlapping
vocabularies, all embedded:

| Writer | Domain | Articles | Chunks |
|--------|--------|----------|--------|
| `nadia-belhaj` | sea fishing | 3 | 10 |
| `tomas-lindqvist` | ML inference | 3 | 10 |
| `imane-farouk` | urban planning | 3 | 8 |
| `yusuf-adeyemi` | fermentation | 2 | 7 |
| `clara-mensah` | classical music | 2 | 6 |

**No backfill was needed.** `pnpm db:embed-backfill` was planned on the basis of an
apparent ~13-article gap, but that count came from a query that did not filter
`deleted_at`. Filtering it: **0 published, non-deleted articles lack chunks.** The
corpus was already complete, and the Gemini calls were not spent.

## 2. Writer demo — chat demonstrably uses retrieved vocabulary — PASS

As `imane-farouk` (premium, allowance reset to 1,000 that morning), prompt:

> Draft an opening paragraph for a new piece about parking minimums.

**Parking minimums are a topic she has never written about.** The reply:

> …the edge of the street is defined not by the built environment, but by the empty
> expanses of asphalt that separate buildings from the public realm. As a result, the
> vitality of the street is diminished… all in the name of satisfying a land-use
> regulation…

Set against her retrieved corpus:

> Push buildings back from the property line… In a dense old quarter the building
> meets the pavement… The older stretch is busy at pedestrian speed. The newer
> stretch, with more light and more air and more landscaping, is empty

What transferred is the **argument**, not just the keywords: her thesis that a
setback rule hollows out street life, re-applied to a different regulation. That is
the claim RAG is supposed to support, and it is visible in the output.

## 3. Magazine demo — Portfolio Insights panel — PASS

**The risk item.** `POST /ai/portfolio-insights/imane-farouk` as
`the-longform-review` returned `201` and produced the **first row this table has ever
held**. The panel at `/discover/writers/imane-farouk` renders all four named elements
plus the two beyond them:

- **VOICE** — register, sentence construction, tone
- **SUBJECT EXPERTISE** — 5 topics, all from her corpus (transit ridership, land-use
  zoning, urban setback regulations, public-health aspects of city design,
  transportation policy)
- **VOICE CONSISTENCY — 85/100**, labelled as consistency and never as a bare
  "score", per the standing decision that reading it as a quality mark would be
  exactly wrong
- **COMMISSION IDEAS** — 5 entries; this is the "fit" element
- **STRENGTHS AND GAPS**
- Footer: *"Generated from 3 published articles on Aug 15, 2026. Refreshes when the
  writer publishes."*

Screenshot: `screenshots/phase4-portfolio-insights--magazine.png`.
Covered from now on by `e2e/17-phase4-portfolio-insights.spec.ts` in the frontend
repo — 1 passed, 0 console errors.

## 4. `/ai/retrieval-debug` shows correct chunk IDs — PASS

After the criterion-2 chat call, the endpoint returned 5 chunks
(`retrievedCount: 5`, `corpus: {chunks: 8, articles: 3}`), each above the 0.60
semantic floor, top similarity **0.668**.

Cross-checked against the database by ID:

```
5 of 5 chunk IDs exist; 0 belong to anyone else
  imane-farouk | The Setback That Ate the Street            | 4
  imane-farouk | Transit Ridership Is a Land Use Statistic  | 1
```

The author scoping holds. The top chunk is from *The Setback That Ate the Street* —
the same article whose argument criterion 2 shows being reused, which links the two
results.

## 5. Search returns relevant results for keyword and semantic queries — PASS

The fusion measurements recorded in `0-phase-plan.md` reproduce **exactly** against
the current corpus:

```
"tackle"                               2 lexical + 3 semantic → 3 fused
"how do I stop my ferments going bad"  0 lexical + 2 semantic → 2 fused
"reading the water before you cast"    1 lexical + 3 semantic → 3 fused
```

The middle case is the one worth defending: **0 lexical** — no article contains the
searcher's words — and Yusuf's two fermentation pieces still come back.

## 6. Cache invalidation — PASS

| Step | Observed |
|------|----------|
| Cached rows before | 1 |
| Publish `E2E: Curb Cuts Are a Land Use Decision` as `imane-farouk` | `201` |
| Within 3s | `portfolio_insights` = **0**, new article = **2 chunks** |
| Cached read | `{"insights": null}` — reports absence, never stale data |
| Regenerate | `basedOnArticles` **3 → 4** |

The regenerated topic list now leads with **"curb cut design"** and **"urban street
morphology"** — drawn from the article published thirty seconds earlier. Invalidation
and regeneration are both proven, not just the deletion half.

The worker log shows the designed chain, including the job that is chained rather
than parallel because it reads what the first one writes:

```
EmbedArticleService      Embedded article fd6972ad… into 2 chunk(s)
EmbedArticleProcessor    embed-article: fd6972ad… → 2 chunk(s)
WriterMemoryService      Extracted memory for imane-farouk from 7 chunk(s): neutral/measured
EmbedArticleProcessor    extract-writer-memory: refreshed profile for 8d1efd6a…
```

---

## Observations — not defects, but worth knowing

1. **Envelope asymmetry between the two insights endpoints.** `POST
   /ai/portfolio-insights/:username` returns the report bare; `GET
   /writers/:username/portfolio-insights` wraps it as `{"insights": {…}}`. Both are
   200 and the frontend handles both. Noted because reading the two responses with
   the same parser silently yields nulls.
2. **The "fit" element is named three ways** — `suggestedUseCases` in the API,
   "COMMISSION IDEAS" in the UI, "fit" in the exit criterion. All the same thing.
3. **Dev DB drift from this pass:** one new published article
   (`E2E: Curb Cuts Are a Land Use Decision`, `fd6972ad-…`) on `imane-farouk`, taking
   her live corpus from 3 to 4; one cached `portfolio_insights` row. Left in place
   deliberately — deleting the article would re-invalidate the cache and cost another
   model call to restore. It is written in her voice and domain, so it does not
   pollute the corpus.
