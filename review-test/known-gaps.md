# Known gaps

Controls that do nothing **by design**, each documented in the source at the time it was
written. These are **not bugs** and must not be filed as such — a sweep that reports them
buries its real findings under twenty entries the team already knows about.

Pre-populated from a grep of `frontend.inkwell.ai/src` before the sweep began, so the
agent does not have to rediscover them.

## How to use this list

When a control does nothing, grep its component for `NOT WIRED`, `TODO(`, or `disabled`.
A marker means it belongs here. No marker means it is a finding.

**Check the marker is not stale.** Several of these are blocked on a phase that has since
shipped; those are real findings and belong in `bugs.md`. Two have already been
reclassified that way — see `BUG-001` and `BUG-002`.

---

## Authentication

### "Continue with Google" does nothing

`src/components/shared/google-oauth-button.tsx:9`

> NOT WIRED UP. Neither copy ever had an onClick; both rendered a button that did nothing
> when pressed. The backend does expose /auth/google and /auth/google/callback, so
> finishing this is a matter of navigating to the former — but doing that is a behaviour
> change with a redirect flow to verify, not a refactor, so it stays inert here.

Appears on `/login`, `/register` and `/register/magazine`. **This is the one the user
reported by hand** — a known unfinished feature, not a defect. The backend half exists;
only the click handler is missing.

---

## Navigation

### "Following" is greyed out

`src/components/layout/nav-items.tsx:74`

> TODO(Phase 3): Wire to following feed

Rendered as a `<span>`, not a disabled link, deliberately — an `aria-disabled` anchor
stays in the tab order and still navigates on Enter. The route does not exist, so the
greying is what stops a 404.

**"Analytics" is no longer here — resolved 2026-08-23.** Its marker read
`TODO(S6): Analytics dashboards ship in S6`, and S6 had closed, which by this file's own
rule at the top made it a real finding rather than a known gap. `/dashboard/analytics`
was built in Phase 6 and the entry is now a live link.

It also pointed at the wrong URL. The nav said `/analytics` while `9-design.md` §6 said
`/dashboard/analytics` — two answers for a page that existed at neither, which is the
kind of thing a greyed-out control hides indefinitely.

---

## Article cards

### Like and comment counts are placeholders

`src/components/shared/article-card.tsx:242, 318, 383`

> TODO(Phase 3): GET /articles carries no likeCount/commentCount, so both pass
> a placeholder.

The feed payload has no counts to render. The numbers on a feed card are not real; the
counts on the article page itself are.

---

## Profile heroes

### Writer profile: article, follower and reader counts

`src/features/profiles/writer-profile-hero.tsx:58, 61, 65, 78`

> TODO(Phase 3): published-article count from GET /u/:username — the endpoint …
> TODO(Phase 3): follower count from GET /users/:username/follow, which ALREADY …
> TODO(Phase 3): lifetime reader count — needs an aggregate over …
> TODO(Phase 3): Wire to share functionality

Note the second one: the follow endpoint **does** exist, so that count is closer to a
stale marker than the others. Worth re-checking against the live API before assuming.

### Magazine profile: counts and founding date

`src/features/profiles/magazine-profile-hero.tsx:54, 56, 58`

> TODO(Phase 3): published-article count from GET /m/:slug.
> TODO(Phase 3): contributing-writer count from GET /m/:slug.
> TODO(Phase 3): founding date — GET /m/:slug returns no createdAt today.

### Magazine profile: hardcoded contributor names

`src/app/(main)/m/[slug]/magazine-profile-view.tsx:113`

> TODO(Phase 3): replace the hardcoded name list with the magazine's real …

The names shown are invented. Worth confirming how visible this is during a demo.

---

## Feed sidebar

### "Writers to follow" is not wired to discovery

`src/features/feed/writers-to-follow.tsx:43, 58`

> TODO(Phase 3): when this widget is wired to the discovery API, swap this …
> TODO(Phase 3): Wire to discovery API

---

## Article page

### Follower count on the author card

`src/features/articles/article-author-card.tsx:40`

> TODO(Phase 3): follower count from GET /users/:username/follow, which …

Same stale-looking marker as the writer hero — the endpoint exists.

---

## Not a gap, despite appearances

### `follow-button.tsx`

Its header comment describes four follow buttons of which only one worked, marked
`TODO(Phase 3)`. That describes the **state before the component was written** — the
comment is explaining what it fixed. The control works. Do not file it.

---

## Reclassified as bugs

Markers whose blocking phase has since shipped. Recorded here so the reasoning survives.

| was | now |
|---|---|
| `ai-quota-notice.tsx:75` — *TODO(Phase 5): enable once the subscription upgrade flow exists* | **`BUG-001`** — the flow exists |
| `magazine-profile-hero.tsx:65` — *TODO(Phase 5): Wire to subscription/payment API* | **`BUG-002`** — the API exists |
