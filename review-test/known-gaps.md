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

### ~~"Continue with Google" does nothing~~ — closed 2026-08-24, with one gap remaining

**Closed.** The button is wired, and the missing half nobody had noticed is built.

The original entry said "only the click handler is missing". That was wrong on the
larger point: `auth.controller.ts` finishes the handshake and redirects to
`${FRONTEND_URL}/auth/callback`, and **no such page existed**. The backend half had
been complete and unreachable since it was written — a click handler alone would
have sent the user to a 404 carrying their tokens in the URL.

What shipped:

- `(auth)/auth/callback/page.tsx` — a server shell that reads the token pair,
  refuses a cancelled consent (`?error=access_denied`) or a half-delivered pair,
  and hands a valid one to a client component that writes both token stores and
  `router.replace`s away, so credentials do not linger in session history.
- The button navigates to `${API_URL}/auth/google` as a plain `<a>`: OAuth begins
  with a full-page navigation the browser must own, and Google will not render its
  consent screen inside an XHR.
- `e2e/24-google-oauth.spec.ts` — six tests.

**The gap that remains: the round trip cannot be verified here.**
`GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are empty in this deployment, so
everything from Google's consent screen onward is untested. It is untestable
without a live Google Cloud OAuth client, which is a credential this project does
not hold.

Because `GoogleStrategy` falls back to the literal client id `'not-configured'`
rather than failing at boot, an unconfigured deployment that rendered the button
would send users to Google's own `invalid_client` error page — worse than the inert
button this replaces. So the entry point is gated on
`NEXT_PUBLIC_GOOGLE_OAUTH_ENABLED`, which defaults to `false`, and the OR divider
above it is gated on the same flag so no orphaned "or" is left behind.

What **is** verified, with the flag off: `GET /api/auth/google` really does 302 to
`accounts.google.com`; the callback route's three refusals; and the absence of both
the button and the divider on `/login` and `/register`.

---

## Accessibility

### Buttons that navigate announce themselves as buttons

`components/ui/button.tsx`, wherever it is used with `nativeButton={false}`.

The house idiom for a button-styled link is
`<Button nativeButton={false} render={<Link href=… />}>`. Base UI renders that as
`<a role="button" tabindex="0" href="…">` — a real anchor with real navigation, but
announced to a screen reader as a button. The user is told to expect an action and
gets a page change, and the control is missing from any "list all links" navigation.

Found 2026-08-24 while writing `e2e/24-google-oauth.spec.ts`, where
`getByRole('link')` failed against a control that is visibly and functionally a link.
Present on the OAuth callback's "Back to sign in", `writer-card.tsx`'s "View profile",
`ai-quota-notice.tsx`'s upgrade CTA and `writer-evaluation-view.tsx`.

Not fixed here: it is one prop on a shared primitive, so changing it is a
design-system change touching every button-shaped link in the app, and it wants its
own pass with the rest of the a11y sweep rather than being slipped into an OAuth
commit. The specs assert the current role so they do not silently start passing if
it changes — they will fail loudly and be updated deliberately.

---

## The sweep's own tooling

### Running the sweep overwrites the screenshots that bugs.md cites as evidence

`review-test/screenshots/` · `e2e/fixtures/test.ts`

The `shot()` fixture writes `screenshots/<name>.png` on every run, named after the
page and persona. `bugs.md` cites **28** of those files as the evidence for filed
findings — `publish-dialog-footer-720--e2e.png` for BUG-012, `notifications--writer.png`
for BUG-006, and so on. Every one of those bugs is now fixed, so a sweep run replaces
"here is the defect" with "here is the working page", under the same filename, with
nothing to indicate the substitution happened.

It has not bitten yet only because of a second bug that masked it: `SHOT_DIR` was
resolved by counting `..` segments, which is correct for the standalone clone and
wrong for the submodule checkout that Docker actually mounts — so since 2026-08-19
every screenshot had been written into a phantom `docker.inkwell.ai/src/spec.inkwell.ai/`
tree and the real directory sat frozen. Fixing the path (2026-08-24) re-arms this.

**Recommended:** move the 28 cited files into `review-test/findings/`, repoint
`bugs.md`, and leave `screenshots/` as the disposable current-state dump it actually
is. Evidence for a closed finding is an archive; a directory the suite rewrites on
every run is not one.

Not done here because it is 28 file moves and 28 link edits in a commit about Google
sign-in and specification drift. Until it is done, restore `review-test/screenshots/`
from git after any run whose purpose was not to refresh the evidence.

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
