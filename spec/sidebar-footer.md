# Sidebar footer — theme toggle and Settings

**Status:** binding. Implemented in MyCal, MyMail and MyNotes.

**Written from** the three apps' shipped code — which is the ground truth wherever it and a
document disagree — checked against the handover indexed as `INDEX.md`:
`spec-v1` through `spec-v1.6`, `note-literal`, `goal-correction`, `offset-ruling`,
`canonical-LB`, `mycal-gutter`, `ack-mycal`, `aria-ruling`, `defer-fc`, `chromium-ok`, and
the measurement sources `hold`, `stale-check`, `browser-stale`, `js-check`, `closeout`,
`closeout2`. **If you find a ruling cited that is not in that list, it was not available when
this was written — get it and check this document against it** (`AGENTS.md` §3.1).

> That block called this a **"nineteen-document handover"** while enumerating **22 names**
> (7 `spec-v1.x`, 9 rulings, 6 measurement sources). The count has been dropped rather than
> corrected to 22, because which of the two is wrong cannot be settled from inside this
> repository — `INDEX.md` is not here — and `AGENTS.md` §3.1 exists because *guessing* at a
> source set is what went wrong the first time. The enumeration is the usable half: it is what
> the dangling-reference test runs against. Someone holding `INDEX.md` should reconcile it.

**Added in the revision that recorded the three e2e suites** (§9, §9.1), and subject to the
same test: MyMail's and MyNotes' suites and CI workflows as committed on their
`e2e-sidebar-footer` branches; their authors' acceptance runs and mutation results, relayed by
the coordinating agent and recorded as their measurements rather than mine; and first-hand
re-measurements taken for this revision against all three apps' served builds — the §3 route
probe, the §2.4 row widths, the §10.8 narrow-layout coordinates and the §10.12 horizontal-scroll
readings. Every figure in those four is stated with the conditions it was read under; where a
number came from someone else's run, the text says so.

The bottom of the left sidebar in all three apps holds two controls: a light/dark theme
toggle, and — to its right — Settings. This document is the single definition of how they
look, where they sit, and how they behave. The three repositories implement it; none of
them defines it.

**The goal is a user with all three apps open in browser tabs seeing nothing move when
switching between them.** That is what every rule below serves, and it is the test to apply
when something here looks arbitrary.

---

## 1. What this covers, and where

The contract covers exactly two controls per app. Each repo names them locally; the names
are not shared and must not be unified (see §5.2).

| | MyCal | MyMail | MyNotes |
|---|---|---|---|
| Stylesheet | `web/static/app.css` | `web/static/app.css` | `web/static/app.css` |
| Both controls | `.sidebar-footer-btn` | `.sidebar-theme-toggle`, `.sidebar-settings-link` | `.sidebar-footer-actions .theme-toggle`, `.sidebar-footer-actions .settings-open` |
| Footer element | `.sidebar-footer` | `.sidebar-footer` | `.sidebar-footer` |
| Flex row | `.sidebar-footer-actions` | `.sidebar-footer` *(the footer is the row)* | `.sidebar-footer-actions` |
| Stacked label | `.sidebar-theme-label` | `.sidebar-theme-label` | `.theme-toggle-label` |
| Markup | `web/ts/app.tsx`, `web/ts/components/Settings.tsx` | `web/ts/layout/Sidebar.tsx` | `web/ts/app.tsx` |

The Settings control is a different element type in different apps — `<button>` in MyCal
and MyNotes, `<a href="#/settings">` in MyMail — and that is fine. Both carry the identical
rule; the anchor additionally needs `text-decoration: none`.

Whether the footer is itself the flex row (MyMail) or wraps a separate row element (MyCal,
MyNotes) is likewise a local choice. **Only the observable result is specified.** Where this
document names a mechanism, it is because the mechanism is the only thing that produces the
result, and it says so explicitly.

---

## 2. Button geometry

Both controls, all apps:

```css
display: inline-flex;
align-items: center;
gap: 6px;                    /* icon to label */
padding: 4px 8px;
border: 1px solid <resting border>;
border-radius: 6px;
background: none;
color: <resting text>;
font-family: inherit;        /* see §4 */
font-size: 0.80rem;
line-height: 1.5;
font-weight: 400;            /* pinned — see §3 */
font-style: normal;          /* pinned — see §3 */
text-align: center;          /* pinned — see §3 */
white-space: nowrap;
flex-shrink: 0;
cursor: pointer;
transition: background 0.12s, color 0.12s, border-color 0.12s;
```

The row containing them:

```css
display: flex;
flex-wrap: nowrap;
gap: 6px;                    /* between the two controls */
```

Theme toggle first (left), Settings second (right). No `justify-content` — left-aligned.

Values above are the **resolved** ones. Reaching them through a token is a local choice, as
everywhere else in this document: MyCal and MyNotes write `border-radius: 6px` literally,
MyMail writes `var(--border-radius)`, which holds `6px`. Both are correct.

**Icons** are Lucide, inline SVG, `width`/`height` attributes of 16, `stroke-width` 2,
`stroke="currentColor"`, `viewBox="0 0 24 24"`, at **full opacity**. Where an app dims icons
elsewhere (MyMail's `.folder-icon` sets `opacity: .85`), these two do not take that class.

### 2.1 `0.80rem`, with the trailing zero

Write it `0.80rem`, not `0.8rem`. The computed value is identical; the two-decimal form is
the convention that makes one `grep` find the canonical value in all three repositories.
No test can enforce this and a formatter would silently normalise it — it is a convention,
and that is all it is.

### 2.2 The acceptance height: 29.2px

    19.2px line box (0.80rem × 1.5) + 8px padding + 2px border = 29.2px

**at the default 16px root font size.** The box deliberately mixes `rem` text with `px`
padding, so the number holds at 16px root and grows differently at other root sizes. It is
the shared acceptance *measurement*, not a hard contract. Chromium reports ~29.19.

Anywhere this number is written down — CSS comment, test, requirements doc — write it as
"29.2px at the default 16px root font size". A bare "29.2px" is a claim that stops being
true the moment a reader changes their browser font.

### 2.3 Content-sized, and it must stay that way

No `flex-grow`, no `flex-basis` stretching, and `flex-shrink: 0`.

`flex-wrap: nowrap` on the row does **not** by itself prevent shrinking — a flex item
shrinks before it overflows. These items are otherwise saved only by `min-width: auto`
resolving to the nowrap content width, and `min-width: 0` is a routine flex reset that
appears many times in all three stylesheets. If one ever reached these items the labels
would silently squeeze and clip, with `text-overflow: clip` giving no ellipsis to show for
it.

Pinning `flex-shrink: 0` makes **overflow the only possible failure mode** — loud and
visible instead of silent and subtle.

### 2.4 The row is ~174px, and that is a reading, not a constant

The pair measures **174px** — read in Chromium on Linux, at a 16px root, in whatever
`system-ui` resolves to there, during the work that produced this contract (the three app
commits that this repository's initial commit was written against). All three repos measured
it independently and agreed to the pixel.

That agreement shows the three *implementations* agree. It does not show what any other
machine renders — see §4.

Against the width each app has for it, at the default root size:

| | Sidebar | Content box available to the row | Slack |
|---|---|---|---|
| MyCal | 200px (`12.5rem`) | 200px — the footer reclaims `.app`'s 16px of horizontal padding (§8.3), so this is *not* 200 − 16 | 26px |
| MyMail | 220px (`13.75rem`) | 203px (220 − 1px border − 16px padding) | 29px |
| MyNotes | 420px | 403px (420 − 1px border − 16px padding) | 229px |

**MyCal has the tightest budget of the three, at 26px.** Stated explicitly because the rest of
this section is mostly about MyMail — it is where the font size was forced and where the
two-word label overflows — and a reader who takes "the app this section keeps naming" for "the
app with the least room" gets it backwards. One author did, and corrected themselves. The
binding constraint is MyCal's 26px; MyMail's 29px is second; MyNotes' 229px never binds
(§6.4). Re-measured against all three servers while this was written, and the table above still
holds to the pixel: pair 174px in 200 / 203 / 403px of content box.

> **MyNotes' row has a pending change that is not reflected above, deliberately.** Its column
> widens to **464px** (content box 447, slack ~273) to make room for the app-logo badge — see
> `spec/app-logo.md` §10.1. **That work is on an unmerged branch; MyNotes' `main` still ships
> `420px`**, so the row above is correct for shipped code and stays as it is until the branch
> lands. §6.4 carries the same note beside the same figures. Update both on the merge, not
> before — and none of it disturbs this section's conclusion, since MyNotes' slack only grows and
> it was never the binding constraint.

That budget sized the font. At the original `0.85rem` the row measured 182px against
MyCal's then-164px — an 18px overflow that clipped Settings — and the fix was `0.80rem`
together with widening MyCal's sidebar from 180px to 200px. Separately, in MyMail a
two-word "Dark mode" label takes the row to 214px against 203px available: 11px past the
edge, which with `flex-wrap: nowrap` and `flex-shrink: 0` clips rather than wraps. That is
why the one-word width-stable label (§7) is mandatory rather than cosmetic.

**Treat 174px as this platform's number.** It is text measured in a font that resolves
differently on other platforms; Segoe UI or SF Pro will not give exactly this. It is a
budget to re-measure when a label changes, not a value to assert.

---

## 3. Three pinned inherited properties

```css
font-weight: 400;
font-style: normal;
text-align: center;
```

**These change nothing today. That is precisely why pinning them is safe, and it is not why
they are pinned.**

They are pinned because the controls arrive at the same values **by different mechanisms**,
which means they agree by coincidence rather than by contract. The routes are per *control*
and per *property*, not per app — the property matters, because `text-align` does not travel
with the other two:

| | `font-weight`, `font-style` | `text-align` |
|---|---|---|
| **MyCal** — both controls, `<button>` | UA `button` rule's `font` shorthand | UA's separate `text-align: center` on buttons |
| **MyMail** — toggle, `<button>` | UA `font` shorthand | UA `text-align` |
| **MyMail** — Settings, `<a>` | inherited from `body` | inherited from `body` |
| **MyNotes** — both controls, `<button>` | inherited from `body` — its own `button { font: inherit }` displaces the UA font | UA `text-align`, **as MyCal** |

**`font: inherit` does not carry alignment.** `text-align` is not part of the `font`
shorthand, so MyNotes' `button { font: inherit }` never displaces the UA's separate
`text-align: center` for buttons. MyNotes reaches alignment by exactly the route MyCal does,
and **the only control in the suite that inherits `text-align` from `body` is MyMail's
Settings anchor** — which is also the only one with no UA `text-align` of its own to fall
back on.

Measured in **all three apps**, against each one's served build (Chromium/Linux, 16px root):
with the pins deleted from the rule and `body` moved to
`font-weight: 700; font-style: italic; text-align: right`, MyNotes' buttons went to
`700 / italic / center` and MyMail's anchor to `700 / italic / right`, while **MyMail's button
and both of MyCal's stayed `400 / normal / center`** — and neither MyCal nor MyMail has a bare
`button` rule carrying a `font` shorthand, so in those two the UA font is what applies. That is
the table above, one cell at a time. The earlier wording — that MyNotes inherits all three from
`body` — is withdrawn (§11).

An entirely ordinary `button { font-weight: 500 }` added to any one of the three repos would
break the match, in one app only, with nothing anywhere to catch it. And the UA values are
Chromium's — Firefox and Safari set their own, so "whatever the UA says" is not one value
across three projects *and* three engines.

**`text-align: center`, not `start`.** `center` is what a `<button>` already computes. It
reaches the toggle's stacked label cell (§7), where `start` would shift the shorter word by
1px. On the Settings control — one text node, no wider cell — it has no visible effect
either way.

**Do not pin `appearance`.** Every property it could affect is already set explicitly, so
the declaration would have no effect.

### 3.1 These pins cannot be defended by rendering — assert the declaration

There is a structural consequence of "the three apps reach this by different routes", and it
is why these are the easiest declarations in the contract to delete by accident:

> **The app where a value is already correct is the app whose rendering cannot detect the pin
> going missing.** Any pin justified by *"the three reach this by different routes"* is, by
> construction, unenforceable by rendering in at least one of them.

Delete `flex-shrink: 0`, `text-align: center` or `font-weight: 400` from MyCal and **nothing
observable changes there** — the UA `button` rule supplies all three regardless. Nothing is
inherited, so there is nothing to notice.

> **And the earlier version of this paragraph went on to say that what breaks is the match
> with MyNotes. That is wrong, and it was wrong in the reassuring direction.** Measured: with
> each app's `body` at its shipped typography, deleting one of these pins **from MyCal** changes
> no computed value in **any** of the three. MyNotes routes weight and style through `body` —
> but `body` is `400 / normal`, so the value that arrives is the value that was pinned. Deleting
> MyCal's declaration cannot reach into MyNotes' rule in any case; the two are separate files in
> separate repositories, and the old sentence quietly implied otherwise.

That makes the exposure worse than the old wording claimed, not better. The pin does not guard
a divergence that is visible somewhere the moment it is made; it guards one that is **latent**,
waiting on an unrelated edit — `body` taking a weight, or an ordinary
`button { font-weight: 500 }` — in whichever repo receives it.

**One deletion is visible today, and it is not the one the old sentence named.** Deleting
`text-align: center` **from MyMail's own rule** takes its Settings anchor's computed value to
`start`, because an `<a>` has no UA `text-align: center` to fall back on. Even that moves
nothing on screen. So the honest summary is: **no deletion of any of these pins, in any of the
three repos, changes anything a user could see** — and exactly one changes something a computed
value could see.

**Three levels of detectability** (Chromium/Linux, 16px root, each app's `body` at its shipped
typography, the four pins deleted from the live rule and the page re-read):

| Delete a pin and read… | What can see it |
|---|---|
| the **rendered box** | **nothing, in any of the three** — for `font-weight`, `font-style`, `text-align` *or* `flex-shrink`. No control's box changes by any amount |
| the **computed value** | **one control only** — MyMail's Settings anchor, and only for `text-align`, which falls to `body`'s `start` because an `<a>` has no UA `text-align: center` behind it. (`flex-shrink` also moves, `0` → `1`, in every app — but it is a computed value nothing renders differently while the row has slack) |
| the **CSSOM declaration** | **everything**, in all three |

*Basis, since the rows are not all the same kind of claim.* Directly measured: MyCal, all four
pins, both controls, boxes identical to three decimals across all four conditions; and MyMail
for `text-align`, the one case where a computed value actually moved, where the anchor's box,
its icon and its text rect are identical to the pixel because `display: flex` gives alignment
no layout effect on its contents. For the three inherited pins elsewhere, the computed values
do not change at all, so no movement follows without needing its own measurement.

**`flex-shrink` is the one that does not follow that way**, because its computed value *does*
move — `0` → `1`, in every app. It is invisible only while the row has slack, which all three
have at rest (26 / 29 / 229px, §2.4). MyMail's authors saw the same thing from the other side:
deleting it failed their assertions **with nothing rendering differently**. So this row says
nothing whatever about the overflow case, which is §2.3's subject and the entire reason that
pin exists.

So a test measuring the *rendered result* cannot protect these, and a test measuring the
*computed value* protects one case in one app. **Assert that the declaration is present**,
read off the CSSOM rather than off the box. All three suites now do this, and in MyCal it is
what catches three of its seven silent-breakage items (§9.2).

That one exception is worth keeping straight rather than rounding away: **MyMail's
computed-value test is discriminating for `text-align` where MyCal's and MyNotes' are not.**
It is the single place in this contract where the rendering side of the pair earns its keep,
and it earns it in the app that was not previously credited with it.

Same shape as the `prefers-reduced-motion` ruling (§6.1) and the surface coincidence (§5.4):
wherever two things agree today for different reasons, agreement is not evidence that the
mechanism holding them together still exists.

---

## 4. `font-family: inherit` — a verified shared value, not a pinned one

All three write `font-family: inherit`, and all three `body` stacks are identical:

```css
system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif
```

This is recorded as a **verified shared value**: it has been checked and it agrees. It is
deliberately *not* pinned to a literal stack, because inheriting is what keeps these
controls consistent with the app around them, which matters more than pinning a stack that
already matches.

**Caveat, and it is a real one: matching the specified stack is not matching the rendered
face.** `system-ui` resolves to a different font on Linux, Windows and macOS. Three apps on
one machine will always agree — which is exactly what the tab-switching goal requires — but
the 174px row width (§2.4) and any other text measurement is a per-platform reading.

The human has accepted this as a residual risk. Do not build around it, and do not treat it
as blocking.

---

## 5. Colours

### 5.1 Resolved values

| Role | Light | Dark |
|---|---|---|
| Resting text + icon | `#6b7280` | `#9ca3af` |
| Resting border | `#e5e7eb` | `#374151` |
| Hover text + icon | `#1f2937` | `#f3f4f6` |
| Hover background | `#f3f4f6` | `#374151` |
| Hover border | `#9ca3af` | `#6b7280` |
| Focus outline | `#2563eb` | `#3b82f6` |

**The hover border is deliberately not the resting border.** In dark, the hover background
and the resting border are both `#374151`, so keeping the resting border would erase the
button's outline at exactly the moment it lights up.

**The hover fill has a floor: it must not equal the backdrop, and must reach 1.053:1 against
it.** The floor exists because a fill at 1.000:1 is not a weak fill, it is an absent one.

Three things about that number, because it is weaker than it looks:

- **It is a product floor, not a WCAG one.** No criterion was found that binds a hover-only
  fill and none is cited here for one. The label's own contrast *on* the fill keeps its 1.4.3
  obligation regardless (§5.4), and that one is real.
- **It is the weakest the suite already ships** — MyNotes' light fill, `#f3f4f6` on `#f9fafb`.
  So it is reverse-engineered from the status quo rather than derived, and it forbids only
  getting worse than the worst.
- **It is therefore not a quality bar.** §10.1 records the fill doing almost no visual work in
  all three apps as an open item with the owner. Clearing this floor is not evidence of a
  visible hover.

> **This floor was first written as 1.101:1, which MyNotes fails.** 1.101 is MyCal's and
> MyMail's figure; MyNotes has always been at 1.053. Committed in `f02c455` — the same
> changeset that extended `AGENTS.md` §3.2, the rule about a rationale that holds for two apps
> written as though it held for three. Corrected in the commit that follows it, and left in
> the history rather than amended away.
>
> The mechanism is worth naming, because "check all three" did not prevent it: **the number
> came from a table I had just read** (§10.1), and I took the value that appeared twice as the
> value that appeared. A figure shared by two of three apps looks like the shared figure. When
> deriving a bound from a per-app table, take the **extreme**, and say which app it came from —
> naming the app is what makes the error visible.

#### Recorded per-app deviations

The values above are shared. Where an app's own backdrop (§5.3) makes a shared value fail a
stated threshold, that app deviates on that one value — **recorded here with its measurement,
and only then implemented.** `AGENTS.md` §2.2 is unchanged: a deviation is never decided in an app repo.
Anything not in this table is still shared, and finding a difference that is not listed here
means one of the three has drifted.

| App | Role | Shared | Local | Measured against its backdrop | Why |
|---|---|---|---|---|---|
| MyCal | Resting text, **light only** | `#6b7280` | `#4b5563` | 6.867:1 (shared value gives **4.393:1**, fails 1.4.3) | its light backdrop is `#f3f4f6`, not `#ffffff` |
| MyCal | Hover fill, **light only** | `#f3f4f6` | `#e5e7eb` | 1.125:1 (shared value gives **1.000:1** — the fill *is* the backdrop) | same |

Both are confined to light by a theme-scoped alias, because MyCal's dark theme needs neither:
on `#111827` the shared label measures 6.987:1 and the shared fill 1.721:1, both better than
they were. Scoping matters concretely here — MyCal's dark `--text-muted` is `#d1d5db`, so an
unscoped alias would have moved a dark value that was already correct.

**The local label value is rejected option B, and the objection to it has expired.** Darkening
the label to `#4b5563` was rejected once, because it applied a whole ramp step to three apps
to fix one. Per-app backdrops remove that premise: it now applies to one app, which is the
number of apps that have the problem.

> **"Light only" is a claim about token *names*, and half of it is defensible by nothing.**
> Confining a deviation to one theme means the other theme must *name* the shared token. That
> is a claim about the declaration, not about the colour — so wherever the two tokens happen to
> resolve alike, neither rendered output nor a resolved-value comparison can see it. §3.1's
> class, arriving somewhere new.
>
> Both halves of MyCal's dark pair were mutation-tested against `tools/check-contract.py` on
> scratch copies. **They do not behave the same:**
>
> | Collapsing the dark alias for | Resolves to | Caught? |
> |---|---|---|
> | the **label** | `#d1d5db` (dark `--text-muted`) ≠ `#9ca3af` | **yes** — fails §5.1 resting text [dark] |
> | the **hover fill** | `#374151` (dark `--border`) = dark `--hover-bg` | **no** — passes clean |
>
> Only the fill is exposed, and only because two of MyCal's dark tokens are the same hex today.
> The day `--border` moves in dark, the fill follows it away from the mandated `--hover-bg` —
> silently, in the theme that is not supposed to be diverging at all.
>
> **Do not collapse the two theme-scoped pairs into one unscoped pair**, however redundant the
> fill makes it look. MyCal holds this with a CSSOM assertion on the declaration. MyMail and
> MyNotes need no equivalent because they have no deviations — and would need one the day they
> did, which is a cost of deviating that is easy to miss when granting one.

### 5.2 Token names are per-project by design

What is mandated is the **resolved colour**, never the token name or the number of hops to
reach it. The three palettes hold these values under different names, and unifying the names
is explicitly out of scope — that belongs with a future shared stylesheet, if there ever is
one.

| Role | MyCal | MyMail | MyNotes |
|---|---|---|---|
| Resting text | `--text-subtle` | `--sidebar-muted` → `--text-subtle` | `--muted` |
| Resting border | `--border` | `--border` | `--border` |
| Hover text | `--text` → `--fg` | `--text-primary` → `--fg` | `--fg` |
| Hover background | `--hover-bg` | `--sidebar-hover` → `--hover-bg` | `--hover-bg` |
| Hover border | `--text-faint` | `--text-faint` | `--faint` |
| Focus outline | `--primary` | `--primary` | `--primary` |
| Footer separator | `--border` | `--sidebar-footer-border` → `--border` | `--border` |

MyMail's `--sidebar-footer-border` alias exists so the footer separator does not reach past
its sidebar token layer. It is approved and **MyMail-local**. Do not add an equivalent alias
to another repo unless that repo already has that kind of indirection layer.

MyNotes' `--hover-bg`, `--faint` and `--primary` live in `web/static/render/note.css`
alongside its other variables — that file owns the theme selectors, and `app.css` has no
`:root` block of its own. Of the three, **only `--hover-bg` and `--faint` are dead weight**
in the Android render kit: each is used exactly once, by app chrome, and never by
`note.css` itself. `--primary` is used by the render kit and is not dead weight. Carrying
those two is a deliberate trade against splitting MyNotes' palette across two files.

### 5.3 The backdrop is per-app, and it is recorded

> **The colour painted immediately behind the two controls must be opaque, must be recorded
> here as a resolved value for each app and theme, and every colour drawn on it must be
> verified against *that app's* backdrop.**
>
> **It is not required to be the same colour in the three apps, and it is not.**

This replaces a rule requiring the backdrop to be the app's `--surface`. That rule is
withdrawn (§11) **on the owner's instruction, not because it was wrong**:

> *"Now the buttons look the same and have the same placement, good. However, MyCal does not
> look good with that box around the buttons, remove the surrounding box and place the buttons
> directly on the left panel background. Accept that the three apps have different background
> color around the buttons."*

Read precisely, that sanctions a difference in **the colour behind the controls**. It does not
sanction differences in geometry — the first sentence is confirming those — and it does not
by itself sanction anything else in this document. Two further divergences were proposed on
the strength of it and one was refused; see §8.5.

#### What did not fall

The reason the old rule existed survives it intact. Every colour in §5.1 is **half of a
contrast ratio**. Pinning the halves without pinning what they sit on specifies nothing about
how they read, and that is exactly how a WCAG 1.4.3 failure (4.393:1) and an invisible hover
fill got in — two defects, one cause.

So the obligation **moves rather than lapses**: from *which colour* to *the relationship
between the colour and what is drawn on it*. Per app, both themes:

1. **Opaque.** A sticky footer over transparency has content scrolling visibly under it
   (§8.3), and a transparent backdrop makes the resolved value undefined for every check
   below.
2. **Recorded here**, as a resolved value, in the table that follows.
3. **Everything drawn on it re-measured against it** — the resting label to 4.5:1 (§5.4,
   WCAG 1.4.3), the focus indicator to 3:1 (§6.2, WCAG 1.4.11), the hover fill to the product
   floor in §5.1. A shared value that fails one of those against an app's own backdrop
   becomes a recorded per-app deviation (§5.1), never a locally-taken decision (`AGENTS.md` §2.2).

#### The recorded backdrops

| | Light | Dark |
|---|---|---|
| MyCal | `#f3f4f6` (`--bg`) | `#111827` (`--bg`) |
| MyMail | `#ffffff` (`--surface`) | `#1f2937` (`--surface`) |
| MyNotes | `#f9fafb` (`--surface`) | `#1f2937` (`--surface`) |

**Why recorded, rather than "any opaque colour".** Because a rule saying "any opaque colour"
is checkable by nothing, and being checkable was the one durable gain of the old rule — the
thing it had that *"whatever each app happens to paint behind the footer"* never did. Writing
the values down keeps that: `tools/check-contract.py` compares each app's resolved backdrop
against **the value recorded above**, not against a shared literal.

So the process has not loosened even though the colour has. **Changing an app's backdrop is
still a change to this document first.** What changed is that the answer may now differ per
app — not that an app may pick one on its own.

#### It is the resolved backdrop, not the element that declares it

An earlier wording said "the footer paints `--surface`", which was false of MyNotes — its
footer is transparent and the `.sidebar` panel behind it paints, which shows through. A guard
implementing the literal wording would have failed a correct implementation. The three reach
their recorded value three different ways:

| | How the recorded colour gets behind the controls |
|---|---|
| MyCal | footer paints `--bg` explicitly — the same colour the chain already resolves to |
| MyMail | footer paints `--surface` explicitly |
| MyNotes | footer transparent; `.sidebar` paints `--surface` and the footer inherits |

**MyCal's and MyMail's footer backgrounds are load-bearing, not decoration.** Both footers are
sticky, so both need an opaque background whatever colour it is. Neither can satisfy this
section by inheritance the way MyNotes does, even in principle.

**And in MyCal the trap is now sharper than that, because the two colours coincide.** Its
`background: var(--bg)` is **redundant for colour and load-bearing for opacity** — it paints
exactly what is already behind it. A reader who deletes it as a no-op sees **no visual change
at the moment of the edit**; the defect appears later, in the month and year views, to
somebody else, as content sliding under the footer. Every other pin in this contract fails
where you can see it fail. This one does not.

*(Phrasing owed to mycal-dev, who raised it while implementing the change.)*

#### Checking it

The requirement is about the resolved colour, so a check must resolve `var()` chains to
literals rather than match token names — MyMail reaches `--surface` through
`var(--sidebar-bg)`, so a name match would fail the app that satisfies the requirement most
explicitly.

**The browser walk is the authoritative method** — see `measurement-protocol.md`, which
carries the primitive and its limitations. A static reader must *assume* which element paints;
a browser can simply walk up from the button to the first ancestor with a non-transparent
background. `tools/check-contract.py` runs the static form and labels it an approximation.

**Never obtain this backdrop by reading one element's own `backgroundColor`**: that returns
the right answer only in an app whose footer happens to declare one, and computes contrast
against transparency everywhere else — §3.1's trap in executable form. **A backdrop that
cannot be resolved is a failure, not a pass** — the null case is "could not look", never
"agrees".

**Do not copy a contrast figure from one app to another.** With three different backdrops
this is now more dangerous than it was, not less: the light column already differed, and dark
has stopped converging too (§6.2).

> **Implementation status — resolved.** MyMail and MyNotes were unchanged by this amendment and
> already matched their recorded rows. **MyCal's change has since landed**, as `8719695` on
> `main`, so all three rows above are now backed by committed code.
>
> The paragraph this replaces said MyCal's change was uncommitted and that
> `tools/check-contract.py` was therefore green **against an uncommitted tree** — a weaker claim
> than green against a commit, and one the script's own output cannot distinguish. That state is
> over, but the discipline it required is not: **when quoting a green run of that script, say
> which state it read.** Nothing in the script says it for you.
>
> The general form, since it will recur: **a checker that reads the filesystem tells you about
> the filesystem.** Uncommitted work, a stashed change and a landed commit are indistinguishable
> to it, so "the check is green" and "the contract holds in the repositories" are different
> claims whenever anyone is mid-edit — which, in a three-repo change, is most of the time.

### 5.4 Text contrast — WCAG 1.4.3 Contrast (Minimum), Level AA

The label is 12.8px at `font-weight: 400`. That is normal text, so the threshold is
**4.5:1**, not the 3:1 large-text allowance.

Resting text, each app against **its own** backdrop (§5.3), using its own label value (§5.1):

| | Light | Dark |
|---|---|---|
| MyCal | 6.867:1 — `#4b5563` on `#f3f4f6` | 6.987:1 — `#9ca3af` on `#111827` |
| MyMail | 4.834:1 — `#6b7280` on `#ffffff` | 5.782:1 — `#9ca3af` on `#1f2937` |
| MyNotes | 4.626:1 — `#6b7280` on `#f9fafb` | 5.782:1 — `#9ca3af` on `#1f2937` |

All six pass. **Six different numbers now, where the previous rule gave three** — read the row
that belongs to the app you are working in, and see §6.2's standing warning about transcribing
a neighbour's figure.

**Two of these rows are close to the line.** MyNotes clears 4.5:1 by 0.126 and MyMail by
0.334, so **both are sensitive to any change in their backdrop or in the shared label
colour.** MyCal is the app with room, which is the opposite of the position it was in.

> **This row failed once, and it would have failed again.** While MyCal's footer painted
> `--bg` and used the shared label colour, its light figure was **4.393:1** — a real 1.4.3
> failure. Pinning the backdrop to `--surface` fixed it. Withdrawing that pin (§5.3) put the
> same 4.393:1 back, in the same app, in the same theme — the identical defect, arriving the
> second time as a side effect of an instruction about appearance that said nothing about
> contrast.
>
> It was caught before it shipped because both mysuite-spec and mycal-dev computed the table
> rather than assuming the geometry-only ruling was colour-neutral. **A withdrawal is a change
> to everything the withdrawn rule was holding up**, and what it was holding up is not
> necessarily what it was written about.

**Hover text is measured against the hover fill, not the panel** — during hover that fill is
the surface the label sits on:

| | Text on fill | Ratio |
|---|---|---|
| MyMail, MyNotes — light | `#1f2937` on `#f3f4f6` | 13.338:1 |
| MyCal — light | `#1f2937` on `#e5e7eb` | 11.856:1 |
| All three — dark | `#f3f4f6` on `#374151` | 9.366:1 |

All clear 4.5:1 with large margins, so hover is never the problem here.

**MyCal used to be the app where the two surfaces coincided** — its panel is `#f3f4f6` and so
was the mandated fill, so the label sat on `#f3f4f6` whether or not the fill painted. That
coincidence is what made the fill invisible, and it is why MyCal now deviates on that value
(§5.1). It is also why an error in *method* survived so long here:

> **A coincidence between two surfaces hides a methodology error rather than a value error.**
> Every number stays right while the reasoning behind them is wrong, so nothing looks anomalous
> until an app where the two differ gets checked. When two things that could differ happen to
> be equal, that is where to test the method — not where to relax.

That generalisation is the durable part, and it outlived the coincidence that produced it:
hover contrast was once measured against the panel instead of the fill in this document, and
in the app most likely to be checked first the wrong method and the right one gave the same
answer.

### 5.5 The control boundary — why no contrast figure is given for the border

With `background: none`, the 1px border is the control's only boundary, and it is nowhere
near 3:1 against what it sits on:

| | Light (`#e5e7eb`) | Dark (`#374151`) |
|---|---|---|
| MyCal | 1.125:1 | 1.721:1 |
| MyMail | 1.238:1 | 1.424:1 |
| MyNotes | 1.185:1 | 1.424:1 |

> **These two MyCal figures were wrong for the whole life of the previous rule, and this
> amendment makes them right again by accident.** They are the `--bg` figures. When `64d1aab`
> pinned the backdrop to `--surface` they should have become 1.238 / 1.424 and they were not
> updated — through a review in which every other table in this file was checked, by the
> author of both.
>
> Recorded rather than quietly corrected, because *"the amendment fixed it"* would be a false
> account of how it got fixed, and **a table that is right for the wrong reason is the next
> reader's trap.** The lesson is narrow and repeatable: when a rule changes what a figure is
> measured *against*, every table measured against it is in scope — including the ones the
> change is not about. This section is about the border; the change was about the backdrop;
> that is exactly why it was missed.
>
> Stated more usefully: **the scope of a re-measurement is set by the operands, not by the
> topic.** This section was in scope because it *names a backdrop*, not because it is about
> backdrops. See `measurement-protocol.md`, which carries the general form — and note that it
> only works if figures state what they were measured against, which is the same discipline
> arriving one step earlier.

**This is deliberate and is not treated as a 1.4.11 failure.** 1.4.11 requires 3:1 for
visual information needed to *identify* a control — and these controls are identified by
their labels, which are always visible and which clear their own threshold (§5.4, with the
one exception noted there). The border is decoration on top of an already-identifiable
control, so no contrast obligation attaches to it.

The numbers are recorded here so that the omission reads as a decision rather than an
oversight. If the labels were ever removed — the icon-only variant that was proposed and
rejected in §7 — this exemption would stop applying and the border would have to reach 3:1.

---

## 6. Interaction

### 6.1 Hover

```css
background:    <hover background>;
color:         <hover text>;
border-color:  <hover border>;
```

No `:active` styling. Do not style `aria-pressed`.

MyNotes qualifies its hover selector with `:not(:disabled)`; the other two do not. Neither
control is ever disabled, so this has no observable effect. Left as-is rather than churned.

**The transition takes no `prefers-reduced-motion` guard — in any of the three.** This is a
standing ruling, not an omission:

```css
transition: background 0.12s, color 0.12s, border-color 0.12s;
```

It animates **colour only**. There is no movement, no scaling, and nothing that transforms,
so `prefers-reduced-motion` has nothing to act on and a guard would be noise. Adding one is
a plausible, well-intentioned accessibility edit that would diverge whichever repo received
it — and because the guard changes nothing observable, nothing would ever reveal the
divergence.

Worth knowing: in MyCal this is **the only `transition` in a ~2600-line stylesheet**, so it
looks anomalous there and invites deletion for local consistency. It is mandated. Do not
delete it, and do not guard it.

### 6.2 Focus

```css
outline: 2px solid <focus outline colour>;
outline-offset: 2px;
```

**The offset is load-bearing. It is not decoration and it is not a spacing preference.**

WCAG **1.4.11 Non-text Contrast (Level AA)** requires a focus indicator to reach 3:1 against
the colours *adjacent* to it. Drawn tight against the button, the indicator's neighbour is
the button's own 1px border — and in the dark theme `#3b82f6` against `#374151` is
**2.803:1**. That is a ceiling of those two hues: **no opacity value can lift it.** A
translucent ring at full alpha still fails.

Offsetting by 2px lifts the outline clear of the border, so both of its neighbours become
the panel background instead. Measured against each app's own backdrop:

| | Light | Dark |
|---|---|---|
| MyCal | 4.696:1 | 4.823:1 |
| MyMail | 5.169:1 | 3.991:1 |
| MyNotes | 4.946:1 | 3.991:1 |

All six pass, under both the strict-adjacency and the same-pixels readings.

> **Do not copy a figure out of this table into another app.** The light column differs, and
> it differs by an amount that looks like rounding.
>
> **A reviewer produced a sibling's figure for this app.** It reported MyCal's light focus
> contrast as **4.90:1**, where the true value is `5.169`. **The mechanism was not
> determined**: 4.90 matches `4.946` rounded to `4.9` in a readable neighbouring repo's CSS
> comment, and no route to 4.90 exists from MyCal's own palette — but the reviewer's
> transcript was not accessible, it stated MyCal's *correct* operands alongside the wrong
> result, and an arithmetic error landing on a value that happens to exist next door is not
> excluded.
>
> Two things hold regardless of how the number was obtained, and they are the reason this is
> here. It happened to a **reviewer** — the role relied on to catch exactly this. And **it was
> catchable only because the light column was per-app**: dark was `3.991` in all three at the
> time, so a sibling's dark figure would have been indistinguishable from a correct one.
>
> That second point was recorded as a cost of convergence — it removed a class of error in
> dark by making it invisible rather than impossible. **The convergence has since gone
> (below), so the blind spot has gone with it.** That is not a reason to relax: it is a reason
> to notice that the exposure moved because a *different* rule changed. **Recompute; do not
> transcribe.**

**Dark no longer converges, and MyCal is the app that left.** Against a required 3:1:

- MyMail and MyNotes sit at **3.991:1** — about one point of headroom, and it is *their*
  shared margin. Both dark backdrops are `#1f2937`, so any change to `--surface` in dark, or
  to `--primary`, moves both at once from a margin neither can spend.
- MyCal sits at **4.823:1**, because its backdrop moved to `--bg` `#111827` (§5.3). It has
  roughly double the headroom of the other two.

This is worth stating rather than leaving as a table entry, because a claim in the opposite
direction was true and load-bearing until this amendment: *"3.991 is the suite's margin, not
any one app's."* It was written into MyCal's own CSS comment as well as this section. **It is
now false, and the version in the code will outlive the version here** unless someone
corrects it — which is `AGENTS.md` §2.5's whole complaint about numbers in prose, arriving on schedule.

MyCal's light figure moved the other way, `5.169` → **`4.696`**, so no app improved on both
axes. Nothing in the suite is near a threshold in light.

Rules that follow from this, all of which have been got wrong at least once:

- **Never restore `outline: none`.** The `box-shadow` ring it was paired with measured
  1.28:1 light and 1.50:1 dark — an indicator that existed but could not be seen.
- **Never shrink the 2px width.** A 2px perimeter is exactly the minimum indicator area
  WCAG 2.4.13 accepts.
- **1px offset would also work, and 2px is chosen for robustness.** 1px is the minimum that
  breaks the adjacency, and it is the most exposed to fractional device-pixel ratios and
  non-integer scaling. 2px has a whole pixel of slack before the mechanism degrades. If any
  app ever finds 2px clips at any root size, report it — the answer is to move all three to
  1px, not to split the value.
- **Do not add a `forced-colors` fallback.** An `outline` *is* painted under forced colours,
  unlike a `box-shadow`, so the gap that a fallback once patched no longer exists. Worse, a
  block containing `outline: revert` would override this compliant outline with the UA
  default — silently undoing the fix it looks like it is protecting.

### 6.3 Correct WCAG citations

Getting these wrong sent this work down a blind alley once. For the record:

| Criterion | What it actually is | Applies here? |
|---|---|---|
| **1.4.11 Non-text Contrast** | 3:1 for UI components and focus indicators, against **adjacent** colours. **Level AA.** | **Yes — this is the binding one.** |
| 2.4.13 Focus Appearance | Focus indicator contrast *and* minimum area. **Level AAA.** | Informative. The 2px perimeter meets its area minimum. |
| 2.4.11 Focus Not Obscured | Focused controls must not be hidden behind sticky headers. Nothing to do with contrast. | **No.** Do not cite it for contrast. |
| 1.4.4 Resize Text | Content usable at 200% text size. | Yes, but the response is per-app — see below. |
| 1.4.3 Contrast (Minimum) | 4.5:1 for normal text. **Level AA.** | Yes — see §5.4. Currently failed by MyCal's resting label in light (§10.2). |
| 2.5.8 Target Size (Minimum) | 24×24px minimum. **Level AA.** | Yes: the 29.2px height clears 24px by 5.2px. Height is the binding dimension; width (~84px per control) is not close. |
| 2.5.3 Label in Name | The accessible name must contain the visible label. | Yes — see §7. |

Use **1.4.11** in code comments and requirements docs.

### 6.4 Resize Text — the containing column is *not* part of this contract

The controls are sized in `rem`, so they grow with the reader's browser font. Whether the
column *around* them also grows is each app's own problem, and the three answer it
differently — correctly:

| | Column width | |
|---|---|---|
| MyCal | `--sidebar-width: 12.5rem` | converted to `rem`; ~26px of slack, so a `px` column would push Settings out |
| MyMail | `grid-template-columns: 13.75rem 1fr` | converted to `rem`; ~29px of slack, same reason |
| MyNotes | `.sidebar { width: 420px }` | **deliberately left in `px`** |

**MyNotes' `px` column is a sanctioned exemption, not drift.** With 403px available against a
174px row it has ~229px of slack — at a 24px root the row reaches only 217px, still leaving
~186px spare, so the resize case never binds.

> **Three annotations on that figure, because it is being read by people it does not describe.**
>
> **1. It is the sidebar *footer* row, and it is false of the *header* row in the same app.**
> MyNotes' header — brand, tab strip, action buttons — has **6.02px** of slack at a 16px root and
> goes **negative at 20px** (+58px of overlap) and at 24px (+131.58px), which is a shipped WCAG
> 1.4.4 failure with no badge present. Same app, same sidebar, opposite conclusion. **Do not carry
> "the resize case never binds" across to the header** — it is a claim about this row only.
> `AGENTS.md` §3.2's pattern arriving *inside* one app rather than across three.
> *(Measured by mynotes-dev; recorded in `spec/app-logo.md` §10.2.)*
>
> **2. "Do not 'fix' MyNotes' `420px`" below is about the *unit*, not the *value*.** Every
> sentence around it argues against converting `px` to `rem`, and that conversion is the "fix"
> being prohibited. It does **not** prohibit changing the number — which the human has now ruled
> should happen, to make room for the logo (`spec/app-logo.md` §10.1).
>
> **3. The slack figure is a function of a width that is changing.** The available width is the
> sidebar **less its 1px border and the footer's 16px of horizontal padding** — 420 − 17 = 403
> today — and the slack is that minus the ~174px row. So:
>
> | Sidebar | Available | Slack vs a 174px row |
> |---|---|---|
> | 420 (today) | 403 | ~229 |
> | 441 | 424 | ~250 |
> | 514 | 497 | ~323 |
> | 588 | 571 | ~397 |
>
> **The exemption gets stronger, never weaker** — widening cannot put this section at risk.
>
> **Status: MyNotes has widened to 464px, on an unmerged branch.** Its `main` still ships
> `420px`, so the table above and the `403` / `~229` figures elsewhere in this section remain
> correct **for what MyNotes ships today**, and are deliberately left as they are. On that branch
> the values are **464 / 447 / ~273**. The `26.25rem` → 630px argument below is about the *unit*
> and is unaffected either way.
>
> **Update this section when the branch lands on `main`, not before** — this document describes
> shipped code, and a figure changed ahead of the merge would describe a state no branch anyone
> can fetch is in. That is `AGENTS.md` §2.5's complaint about describing history nobody can see,
> arriving as a temptation rather than as a mistake.
>
> *(The first version of this annotation gave 266 / 339 / 413 — each 16px too high, from
> subtracting the border but not the footer's padding, while the 403 it was derived from
> already had both taken out. Caught in review. It is `AGENTS.md` §2.5's complaint in miniature:
> a derived number written beside the figure it was derived from, disagreeing with it by a
> constant nobody re-checked.)*

And converting would not have been merely unnecessary — it would have been **a regression**:
`420px` becomes `26.25rem`, which at a 24px root is a **630px** sidebar, eating the note list
for no benefit. That is the reason the exemption was granted rather than merely tolerated.

Sidebar widths were never unified — 200 / 220 / 420 are deliberately different — so the
*unit* is not a consistency requirement either. Only the buttons must match.

So: do not "fix" MyNotes' `420px`, and do not infer from MyCal and MyMail that a `rem` column
is part of this contract. **It is not.** The contract covers the two controls; how a column
accommodates them is local, and the right answer depends on a budget that differs by an order
of magnitude across the three.

---

## 7. The width-stable theme label

The theme button must not change width when toggled, or the Settings button beside it jumps
sideways. Both words stay mounted, stacked in one grid cell, so the button always takes the
width of the longer of the two:

```jsx
<button aria-label={dark ? 'Switch to light mode' : 'Switch to dark mode'}
        title={/* same */}
        aria-pressed={dark}>
  <Icon name={dark ? 'sun' : 'moon'} size={16} />
  <span class="<local-label-class>" aria-hidden="true">
    <span class={dark ? 'is-shown' : ''}>Light</span>
    <span class={dark ? '' : 'is-shown'}>Dark</span>
  </span>
</button>
```

```css
.<local-label-class>             { display: grid; }
.<local-label-class> > span      { grid-area: 1 / 1; visibility: hidden; }
.<local-label-class> > .is-shown { visibility: visible; }
```

**This mechanism is mandated, not just its effect** — it is the only part of the layout
where the specific technique is the contract.

Notes:

- The icon shows the theme you would switch **to**: a moon in light mode, a sun in dark.
- The label pair is `aria-hidden`; the accessible name comes from `aria-label`.
- **Keep each visible word a substring of its matching accessible name** — "Light" inside
  "Switch to light mode". Otherwise the button breaks WCAG 2.5.3 Label in Name, and because
  the span is `aria-hidden` nothing would catch it.
- Labels stay one word. "Dark mode" / "Light mode" takes the row 11px past the edge in
  MyMail, where it was measured (§2.4). Icon-only Settings and shortened labels were both
  considered and deliberately not taken.
- Settings' accessible name is `Settings` in all three, but it is reached differently, and
  only the name is specified: MyCal and MyNotes set `title` and `aria-label` on a `<button>`
  whose visible label sits in a `<span>`; MyMail's `<a>` carries neither attribute and takes
  its name from its own text content. See §10.11 for the one user-visible consequence.

---

## 8. Position: (L, B) = (8, 8) from the **window**

```
distance from the WINDOW's left edge    = 8px
distance from the WINDOW's bottom edge  = 8px   (both controls)
```

Measured to the buttons' **border box**, with `getBoundingClientRect()` against the
viewport — `rect.left` for L, `window.innerHeight - rect.bottom` for B.

### 8.1 Why container-relative placement was not enough

The first version of this contract said "8px from the sidebar panel's inner edge". **That
rule is withdrawn.** Three apps can each satisfy a container-relative rule perfectly and
still put the buttons in three different places on screen — which is exactly what happened.
MyCal was correct against its own sidebar and ~16px off against the window, because its
column sits inside `.app { padding: 8px 16px }`.

The user's requirement is about the *screen*, so the specification has to be about the
screen. If you find a container-relative offset written down anywhere, it is stale.

### 8.2 (8, 8) must hold under **content overflow**, not just at rest

This is the requirement the contract was missing, and it is the one that has actually been
violated in production code.

**A footer that is a plain last child of a scrolling sidebar scrolls away with the content.**
Once the list above it is taller than the panel, B stops being 8 and becomes negative — the
buttons are pushed below the window entirely. MyMail measured **B = −43.61 at 13 folders and
−1052.16 at 40**, against a `.sidebar` that is `overflow-y: auto` with the footer as an
ordinary last child.

Nothing about this is visible at rest. MyMail's 48 passing measurements all used a demo
dataset with **zero user folders**, so the overflow case was never exercised. MyCal's 20 and
MyNotes' 32 have the same blind spot: none of the three varied content volume.

So, normatively:

> **(8, 8) is required for every content volume the app can reach, including more content
> than the sidebar can display.** An implementation that satisfies (8, 8) only while its
> sidebar does not scroll does not satisfy this contract.

MyMail and MyNotes reach (8, 8) from a single declaration — their footer's own `padding` —
because their sidebar panel is already flush against the window edge. **That holds only while
their sidebars do not scroll**, and the caveat is load-bearing: it is exactly the condition
that failed.

### 8.3 The requirement, and the two sanctioned mechanisms

**The requirement:**

> **The footer must not be in the scroll flow of anything that can scroll.**

That is the invariant. **Two mechanisms satisfy it, both sanctioned. Neither is mandated.**

There are two ways the invariant can be broken, and an app may be exposed to either, both or
neither:

1. **The sidebar's own scrollport** — the content above the footer overflows its panel.
2. **The page scrolling** — the whole document is taller than the window.

#### The property that makes both threats impossible at once

Before reaching for a mechanism, check whether the app already has this:

> **Every scroll happens inside a bounded region, and the footer is outside all of them.**

**That is one architectural property, not two lucky ones**, and an app that has it is immune
to both threats simultaneously. It is worth stating positively rather than as two passing
checklists, because it is a thing an app either has or loses — not two independent facts that
happen to be true today.

MyNotes has it, and is exposed to neither threat. Its two load-bearing declarations:

```css
html, body { height: 100%; }                                    /* app.css:10-12  */
.app-body  { flex: 1; min-height: 0; overflow: hidden; }         /* app.css:54-59 */
```

The first caps the document at viewport height; the second absorbs anything long into an inner
scrollport (`.overview-scroll`, `.note-view-scroll`, `.cm-scroller`, `.preview-pane`).
Measured across 60 readings — 5 routes × 3 viewports × 2 root sizes × 2 themes with a
400-paragraph note — `documentElement.scrollHeight === clientHeight`, `body` likewise, and a
**forced** `window.scrollTo(0, 999999)` left `scrollY` at 0 every time, with L and B both
8.00.

An app with this property needs neither mechanism below. An app without it needs whichever
mechanism matches the threat it is actually exposed to.

#### Mechanism A — contained scrollport (structural). Preferred where achievable.

The footer is a **sibling** of the scrolling region, not a child of it. Content growth is
absorbed by the content area shrinking its own inner scrollport; it cannot push the footer,
because the footer is outside the box that scrolls.

- **MyNotes** is built this way: `.sidebar` is `overflow: hidden` with `.sidebar-content`
  scrolling inside it and `.sidebar-footer` beside it. Measured `sidebarOverflowsY` **false
  in all 108 readings, including at 41× overflow.**
- **MyCal** was restructured to this shape during the gutter work. In its own words:
  *"`.left-sidebar` now holds two children instead of three: `.sidebar-content`, the
  scrolling half, and `.sidebar-footer`, a sibling, never inside the scrollport. The
  scrollport moved from `.left-sidebar` to `.sidebar-content`."* Independently confirmed here
  from its shipped markup.

Preferred because it adds **no declarations, no stacking context, no opaque background, and
no scroll-position dependence.** There is nothing to get wrong.

#### Mechanism B — `position: sticky` + `bottom` + an opaque background

For footers that cannot be lifted out of the scrolling box, and for threat 2 regardless of
structure.

- **MyMail** requires it: its footer is an ordinary last child of an `overflow-y: auto`
  `.sidebar`.
- **MyCal** requires it too, for its month and year page-scrolling path — *in addition to*
  mechanism A for its sidebar.

B carries the sum rule below and **three failure modes A does not have**:

1. the **opaque background is mandatory**, or content shows through as it scrolls under;
2. it **creates a stacking context**, which must be checked against the 4px focus-outline
   clearance of §8.4;
3. it **behaves differently at each scroll extreme**, so both extremes must be measured.

|  | A — contained scrollport | B — sticky |
|---|---|---|
| Declarations added | none | `position`, `bottom`, `background` |
| Stacking context | no | yes — check §8.4 clearance |
| Opaque background | not needed | mandatory |
| Scroll-position dependence | none | must measure both extremes |
| Handles threat 1 | yes | yes |
| Handles threat 2 | no | yes |

**Why neither is mandated: MyCal uses both.** Structural for its sidebar scrollport, sticky
for its page scroll. That alone shows the mechanism is not the contract. Forcing sticky onto
MyNotes would add a stacking context, an opaque background and a `bottom`/`padding-bottom`
interaction to a footer that already satisfies §8.2 structurally — three new ways to be wrong
in exchange for nothing measurable.

**The contract is (8, 8) at every reachable content volume. How an app gets there is its own
business, provided it is stated and measured.**

#### Why MyMail uses B rather than A — the cost of A, measured

**A is preferred, not free, and the difference was measured rather than assumed.** MyMail's
sidebar children are flat, with `overflow-y: auto` on `.sidebar` itself, so introducing a
wrapper forces a choice it cannot avoid:

- the wrapper **excludes** the header → the app title and reload button become permanently
  pinned, a visible behaviour change to elements this contract says nothing about;
- the wrapper **includes** the header → the change stays footer-only, but the scrollport no
  longer corresponds to "the sidebar" in any natural way.

MyMail's header scrolls today: measured at `top: 0`, and at `scrollTop = 300` it sits at
**−300**, fully off-screen. So there is no wrapper placement that is behaviour-neutral there,
where sticky was one declaration plus a background and touched nothing else.

**So prefer A, but do not assume it is a pure refactor.** Where it would change behaviour
outside this contract, that is a cost to weigh and state — not an obstacle to route around
silently, and not a reason to pretend B is equivalent.

#### Structural immunity is always one word from being lost

Where an app is immune to threat 2 by construction, the immunity rests on a single
declaration, and in every case that declaration looks ordinary:

| | Declaration | Immunity ends if |
|---|---|---|
| MyMail | `.app { height: 100vh }` over `grid-template-rows: auto 1fr auto` | `height` becomes `min-height` |
| MyNotes | `html, body { height: 100% }` | that cap is relaxed |

MyMail's shell is **exactly** the viewport, so every overflowing region carries its own
scrollport. Verified across 24 combinations, with the intermediate state asserted:
`documentElement.scrollHeight === clientHeight` throughout, `window.scrollTo(0, 99999)` leaves
`scrollY` at `0.0`, B stays 8.

**Both are one-word edits, and both are changes someone makes for a good reason** —
`min-height` is normally the more forgiving choice. Nothing would fail at the time. The
consequence would not appear until a window happened to be short enough, and by then the edit
is long past.

**Both are now asserted, which they were not when this section was written.** Each app's own
suite holds its own declaration's *effect* — not the declaration — across every route in its
table:

| | How the immunity is exercised |
|---|---|
| MyMail | every route at a **1000 × 400** window, deliberately short enough that a shell sized by content rather than by the viewport would overflow it — `height: 100vh` and `min-height: 100vh` are indistinguishable in a tall window with little content |
| MyNotes | every route **at volume** — 41 notes and a 400-paragraph note — with the assertion that something inner *was* scrolling, so the run cannot pass by having stressed nothing |

Both force `window.scrollTo(0, 99999)` and assert `scrollY` is still 0: an unscrolled page and
an unscrollable one look identical until you try.

**Neither runs anywhere but locally** (§9.1), so this is coverage that exists rather than
coverage that fires. And note the two exercise the immunity along different axes — MyMail's
would not catch a regression that only appears at volume, MyNotes' would not catch one that
only appears in a short window. Neither gap is currently covered by the other, because neither
suite can see the other app.

So: **if an app relies on structural immunity, say so at the declaration that provides it.** A
load-bearing `height: 100vh` looks identical to an incidental one.

#### Threat-2 coverage expires when a route is added

Threat 2 is a property of the **layout**, not of content volume, so unlike threat 1 it cannot
hide behind a small dataset. But it can hide behind **a route nobody visited.**

A measurement covering every route in the router's table is complete *as of that table*. A new
route that renders outside the bounded region — outside `.app-body`, or outside whatever the
app's equivalent is — reintroduces threat 2 in that route alone, and is covered by nothing. No
build step catches it, and the other routes keep passing.

**Adding a route is the event that invalidates threat-2 coverage.** Re-measure the new one;
the old numbers stay valid for the old routes.

#### Mechanism B in detail

```css
position: sticky;
bottom: <see the sum rule below>;
background: <an opaque colour>;   /* content must not show through as it scrolls under */
```

**The sum rule.** `bottom` is not independently meaningful — what B actually equals is:

    sticky `bottom`  +  the footer's own `padding-bottom`  =  8px

Both landed implementations satisfy it from opposite ends, which is why they look divergent
and are not:

| | `bottom` | footer `padding-bottom` | B |
|---|---|---|---|
| MyMail | `0` | `8px` | 8 |
| MyCal | `8px` | `0` (`padding: 8px 8px 0`) | 8 |

MyMail keeps its own padding as the inset and pins the box to the window edge; MyCal pins the
box 8px up and lets `.app`'s padding sit below it, because its e2e suite holds the footer
box's bottom edge against the view beside it. **Setting `bottom: 8px` on a footer that also
has `padding-bottom: 8px` doubles the inset to 16px** — the most likely way to get this
wrong.

The explicit **opaque background** is part of the mechanism, not decoration. A sticky footer
with a transparent background has content sliding visibly underneath it. It must match the
surface behind it, or the footer reads as a band of a different colour.

Where each app stands:

- **MyCal** — footer outside the sidebar's scrollport (structural, threat 1) **and** sticky
  (threat 2: its month and year views page-scroll). It cannot use a uniform padding, because
  `e2e/tests/calendar-views.spec.ts` pins the footer *box*'s bottom edge to the bottom of the
  view beside it — the box may not move down even though the buttons must. So it cancels
  `.app`'s horizontal padding with `margin-left: calc(-1 * var(--app-padding-x))`, uses
  `padding: 8px 8px 0`, and sets `bottom: 8px`.
- **MyMail** — footer inside the scrolling sidebar, fixed positionally with sticky +
  `background` (threat 1).
- **MyNotes** — footer outside the scrollport by construction (threat 1); its page does not
  scroll, so threat 2 does not arise.

**Differing here is not a deviation** — the coordinates are the contract, not the
declarations that produce them. Read §8.5 before concluding otherwise.

#### Where each app stands — all three measured against both threats

| | Threat 1 (sidebar scrollport) | Threat 2 (page scroll) |
|---|---|---|
| **MyCal** | **A** — `footerInScrollport = false` in all 20 readings; footer is a flex sibling of `.sidebar-content`. Verified at 26 calendars, sidebar scrollable by 369px (16px root) / 835px (24px root), both extremes | **B, in 2 of 5 views only** — week/day/schedule are structurally immune (`.app:has(…)` makes them `height: 100dvh; overflow: hidden`, so `pageMax = 0`); month and year scroll the document and use `position: sticky; bottom: 8px; background: var(--bg)`. Page scrollable by 455/784px (month), 342/734px (year) |
| **MyMail** | **B** — footer is a last child of `overflow-y: auto` `.sidebar` | **immune** — `.app { height: 100vh }` |
| **MyNotes** | **A** — `.sidebar-content` scrolls inside `overflow: hidden` `.sidebar` | **immune** — `html, body { height: 100% }` |

**MyCal is the concrete case for sanctioning two mechanisms rather than mandating one**: it
needs A for its sidebar and B for its page scroll, in the same app, at the same time.

It also shows that **exposure can vary by view within one app** — three of MyCal's five views
are structurally immune to threat 2 and two are not. So "this app is immune" is a claim about
a *layout*, and an app with more than one layout has to establish it for each. Measuring one
view and generalising is how this would be missed.

L = 8.00 in every reading across all three. B = 8.00 throughout, with one 8.22 at
year/24px/bottom-extreme — the same subpixel scroll-extent artefact as MyMail's 8.02–8.50 range,
and inside the 0.5px tolerance these assertions use. **Expect fractional B at a scroll extreme;
it is a rounding artefact of the scroll range, not drift.**

### 8.4 The 4px floor — L ≥ 4 and B ≥ 4

The focus outline extends **4px** beyond the button's border box (2px offset + 2px width).
Every app has a clipping ancestor around the footer — MyNotes' `.sidebar` is
`overflow: hidden`, MyMail's is a scroll container in both axes, MyCal's scrolling views
clip too. **Any L or B below 4px silently crops the compliant focus indicator on the
window-facing side.** Nothing errors; the outline is simply cut, undoing §6.2.

Concretely: at L = 8 the focused outline's outer edge sits 4px short of the window edge; at
L = 4 it sits exactly on it. **The 4px is the clearance the outline itself needs, not slack
beyond it** — at the floor the margin is zero, so 4 is a hard minimum and not a comfortable
one. This is the reason to refuse a tighter value than 8 if one is ever proposed.

### 8.5 The full-bleed separator

**The footer element is full-bleed across the sidebar. Its `border-top` spans the full
sidebar width. The 8px inset to the buttons comes from the footer's own `padding`, never
from a horizontal margin.**

```css
.sidebar-footer {
  /* no horizontal margin */
  padding: 8px;                            /* this is the 8px inset */
  border-top: 1px solid <resting border>;  /* spans the full sidebar */
}
```

The separator therefore aligns with nothing but the sidebar's own edges. In MyNotes it is
deliberately full-bleed where the header and note list above it are inset by 0.75rem, and
the footer's 8px is deliberately tighter than the 12px the rest of that sidebar uses. Both
are the price of the shared contract, not oversights.

MyCal's `margin-left` (§8.3) is the one sanctioned exception, and it exists to *reach* the
window edge rather than to inset the buttons — the separator moves out with the buttons
rather than staying behind, so it stays full-bleed relative to the window. The prohibition
is on a margin that insets the buttons and pulls the separator in with them.

This mechanism is also why the viewport position is adjustable by a single declaration in
two of three apps. It was mandated for the separator's sake and happens to have made §8
tractable; expect the same to be true of future shared elements.

**The separator does not have to terminate against anything, and in MyCal it does not.**
MyMail's and MyNotes' sidebar panels carry a `border-right` (`app.css:208` and `app.css:67`
respectively), so their separators meet a vertical line at the column edge. MyCal's column
carries none, so its separator simply stops. **That junction is a property two apps happen to
have. It has never been required, and its absence in the third is not a defect.**

This was proposed as a reason to drop MyCal's `border-top` entirely when §5.3 was withdrawn,
and **refused.** Three reasons, in order of weight:

1. The owner's instruction was about the colour behind the controls. Removing a shared visual
   element is not implied by it, and a separator present in two apps and absent in the third
   is exactly the divergence nothing in this suite detects (§10.7).
2. The argument is `AGENTS.md` §3.2's shape read in reverse — a rationale drawn from the two
   apps in view and applied to the third, where here the third is the one being changed.
3. **MyCal shipped precisely this configuration until `282f00f`.** That commit changed
   `background: var(--bg)` → `var(--surface)` and *added* a `border-right`; it never touched
   `border-top`. So `border-top` over a `--bg` footer with no `border-right` is what MyCal
   showed for the entire life of the footer, and the owner's objection arrived only after the
   white fill landed. **The configuration being called unacceptable is the one that was never
   complained about.**

Point 3 is the one worth reusing. When an app proposes removing something because of how it
will look, check whether the app has already shipped that appearance — the repository often
holds a cheap answer to a question that otherwise gets settled by argument.

MyCal's `border-right` **was** removed with the fill, and correctly. It had been added so the
band would not terminate in mid-air against a different-coloured page, and its comment said
so; with the band gone, the condition its justification rested on is gone. See `AGENTS.md`
§3.3 — this is that rule's first catch on the live path, and it worked because MyCal recorded
the *condition* rather than only the verdict.

---

## 9. Verifying a change

See **[`measurement-protocol.md`](measurement-protocol.md)**. It is short, and skipping it
is how every wrong measurement in this contract's history got taken.

The one-line version: **a green build proves nothing about geometry**, because all three
apps embed `web/static/` into the binary and a running server keeps serving what it started
with.

**All three apps now have a `sidebar-footer` suite.** Until recently MyCal's was the only
machine-checkable statement of this contract anywhere; that is no longer true. Read the one
belonging to the repo you are working in before changing anything here — and read the other
two when you change anything shared, because each one records where and why it *departs* from
the others, which is information that exists nowhere else.

| | Tests | Beyond the shared core |
|---|---|---|
| **MyCal** `e2e/tests/sidebar-footer.spec.ts` | 26 | both coordinates in all five calendar views; page-scroll in the two views that scroll; the dark alias-naming check §5.3 requires of a deviating app; that the footer paints an opaque background of its own |
| **MyMail** `e2e/tests/sidebar-footer.spec.ts` | 33 | its five-route table plus a sixth with a scrolling reading pane; sidebar overflow at 40 folders at 16px and 24px roots; the document-never-scrolls immunity; icon size and opacity; the anchor's `text-decoration`; §8.4's 4px floor; §8.5's full-bleed separator |
| **MyNotes** `e2e/tests/sidebar-footer.spec.ts` | 27 | its five routes; overflow at 41 notes; §8.4's floor **and** the clipping premise the floor depends on; §8.5; a CSSOM walk that follows `@import` into `render/note.css`, with a separate test asserting the walk got there |

The shared core all three hold: the acceptance height, (8, 8) from the window, theme-toggle
width stability, the pinned declarations read off both the computed values and the CSSOM,
resize headroom at 20px and 24px roots, and composited focus contrast in both themes.

**Three per-app suites are not a cross-repo check.** Each asserts its own app's values against
its own rendering, and none can see the other two — so all three stay green through a
divergence between them. That is §10.7, and closing two thirds of the coverage gap has not
touched it.

**All three now run in CI.** Until recently only MyCal's did; §9.1 records what changed, when,
and why nothing in this repository noticed.

### 9.1 What each suite's status actually is — all three run

**The three are now in the same state, and until 2026-08-08 they were not.** Each suite is
executed by its repo's own pipeline on every push to `main`, after `./build.sh` and before the
Pages upload and the release.

| | Landed on | Runs in CI | Shown red for the right reason |
|---|---|---|---|
| MyCal | `main`, `7e65102` | **yes** — gates Pages and the release | yes, **in the pipeline** |
| MyMail | `main`, `6e5c33c` | **yes** — same placement | yes, **locally** (see below) |
| MyNotes | `main`, `afec291` | **yes** — same placement | yes, **locally** (see below) |

Verified 2026-08-08 against each repo's public workflow-run API, **at the step level rather than
the run level** — a green run does not establish that the e2e step ran, which is this section's
own distinction. Latest run on `main` at the time of checking, all three with step 9
*"End-to-end tests"* `success`:

| | Run | Head | e2e step |
|---|---|---|---|
| MyCal | #10 | `2e68ef3` | success |
| MyMail | #12 | `07d14cf` | success |
| MyNotes | #8 | `d9f8ff1` | success |

**Commit hashes are given now because they can be.** This table deliberately withheld them while
the two branches were unpushed and being amended, per §11's rule that a hash from an unpushed
branch pays the cost of perishability without buying anyone the ability to resolve it. Both are
now on `main` and pushed, so the rule points the other way and the hashes are recorded.

> **This section went stale without a single edit to it, and it is the section this document
> nominates as the authority on live suite status.** Nothing was ever committed that made it
> wrong. What made it wrong was a **push** — an act that produces no commit, no diff and no
> changeset in any repository, so no review had anything to review and no `grep` had an event to
> search for. That is `AGENTS.md` §3.5 exactly, landing on the file that is supposed to be
> authoritative about the thing that changed.
>
> **How it was actually caught, since none of it was procedural.** Two app agents were asked to
> confirm their own repo's status rather than assume it, and each corrected its own row — MyMail's
> from the public workflow API, MyNotes' from `git`. **Neither checked the other**, and each said
> so explicitly. The third row and the sweep of everything else this falsified came from the one
> place that reads all three repositories, which is the whole reason this repository exists.
>
> The durable form, because the next status claim here will rot the same way: **a claim about
> another repository's live state has no owner in this one.** It cannot be defended by review,
> because nothing here changes when it goes false. Write such claims with the date they were
> verified and the command that verifies them, so the next reader can re-run rather than re-derive
> — which is what the table above now does.

#### MyCal — runs in CI, and **gates publication**

As of MyCal `7e65102`, the suite runs in `.github/workflows/main.yml` — after `./build.sh`,
before Pages and the release. **Nothing is skipped, loosened or conditional.** `build.sh` is
byte-unchanged; Playwright installs in the workflow.

**"Gates publication" is the accurate claim, not "prevents breakage."** The workflow triggers
on push to `main`, so a commit that breaks the contract is *already on `main`* when the suite
goes red. What the gate stops is a broken contract reaching Pages or the rolling release.

It was accepted the way `measurement-protocol.md` requires — **shown red for the right
reason**, not merely shown green. Restoring `outline: none` on `:focus-visible` (chosen
because `./build.sh` stays green, so the suite genuinely runs) failed exactly the three focus
assertions with `Expected: "solid"  Received: "none"`, 3 failed / 45 passed, exit 1; reverting
gave 48 passed, exit 0.

**Those counts are the whole MyCal suite as of `7e65102`, not a current figure.** It has since
grown past 48 — 56 across seven spec files at the time of writing, 26 of them in
`sidebar-footer.spec.ts`. The 48/45/3 above is a record of one accepted run, and it stays
written as one; do not read it as a count of what runs today.

Operational notes worth keeping: retries stay at **0** deliberately; traces and screenshots
upload on failure. (The config previously paired `trace: 'on-first-retry'` with `retries: 0`,
so it had been capturing nothing at all.)

#### MyMail and MyNotes — accepted locally first, and their pipelines have now run

Both workflows trigger on push to `main`. **Both have since been pushed and both have run
green**, at the step level, per §9.1's table. Before that they were accepted locally only, and
the way they earned the upgrade is worth keeping straight.

The wiring was originally validated by parsing the YAML with `yq`, which establishes that it is
well-formed and nothing whatever about whether it works. Neither author could run `npm ci`
either — npm is unusable in that sandbox, and both copied MyCal's `node_modules` — so the
committed lockfiles were verified by parsing and internal consistency, not by an install.
**Both of those reservations are now discharged by the pipeline itself**: `npm ci` and
`playwright install --with-deps chromium` have executed in CI in both repos, which is the only
thing that could have discharged them.

> **What this section used to say, and why it is left visible rather than amended away.** It
> read: *"Do not write that these two run in CI, and do not let 'wired into CI' stand in for it
> … The first push to `main` is the event that converts these rows, and nothing before it
> does."*
>
> **That was right, and it is exactly why the correction was late.** The rule named its own
> successor event precisely — and the event then arrived with no diff, no notification and
> nobody assigned to notice, which is `AGENTS.md` §3.5's second specimen arriving on schedule:
> *a conditional written into the claim it will invalidate is still only as good as somebody
> noticing the condition fired.* The prohibition was sound; what was missing was anything that
> watches.
>
> The rule itself is **not** withdrawn and is not in §11. *"Wired into CI" still does not mean
> "has run"* — that is what made the step-level check in §9.1 necessary rather than a green run
> being enough. What changed is only that these two apps now satisfy it.

What each earned locally, before any pipeline ran, and which the pipeline does not supersede —
a mutation shown red is evidence about the *assertions*, and a green pipeline is evidence about
the *plumbing*:

**MyMail — 33 tests.** Three mutations, each failing on its own assertion:

| Break | Result |
|---|---|
| `outline: none` + a box-shadow ring | 3 failed / 30 passed — `Expected: "solid"  Received: "none"` |
| delete `flex-shrink: 0` | 2 failed / 31 passed — computed `Expected "0" Received "1"`, CSSOM `Expected "0" Received ""` |
| `.sidebar-footer` padding 8px → 24px | 14 failed / 19 passed — `Expected 8 Received 24` |

The `flex-shrink` row is the one to keep. **Nothing rendered differently** — the row had slack,
so no box moved — and it still failed, on both the computed value and the declaration. That is
§3.1's class caught in the act, in an app whose rendering could not have caught it.

**MyNotes — 27 tests.** Two mutations:

| Break | Result |
|---|---|
| delete `font-weight: 400` | 1 failed / 26 passed — **the CSSOM test only**, `Expected: "400"  Received: ""`, with the computed-value test staying green |
| `.sidebar-footer` padding 8px → 24px | 12 failed / 15 passed |

Each reverted to 27 passed, exit 0. The first row is §3.1 again, and note *which* test survived:
the computed-value test stayed green because the deleted value still arrives from `body`, which
is exactly why the CSSOM assertion is not redundant with it.

**Both authors also showed their harness red, not only their assertions** — the freshness check
against a deliberately stale asset, and the pre-flight port guard against a deliberate squatter.
`measurement-protocol.md` requires this of a guard's own machinery and not only of the contract
it polices, after a liveness check once passed 48/48 against the wrong server.

**The padding break is the informative one, and it is informative because of what it is not.**
Changing `.sidebar-footer`'s padding from 8px to 24px moves the buttons off (8, 8) — the single
violation this whole contract exists to prevent — and §10.7 records that
`tools/check-contract.py` **passes it cleanly**, because geometry is invisible to a source
reader. It now fails 14 of MyMail's 33 tests and 12 of MyNotes' 27. The two mechanisms are
complements, and this is the one break that demonstrates it from both sides at once.

#### A caveat on MyCal as the reference — and what porting fails to carry in *both* directions

Both new suites were ported from MyCal's, and porting carried two of its harness defects across
with it. **Both have since been fixed in the two copies and remain in the original** — so the
script this contract points at as the model is now the only one carrying either. These are repo
hygiene rather than contract terms and are owned by the app repos, but they are recorded here
because **this is the only place that can see one defect in three repositories at once**, which
is the whole reason this repository exists. Verified by reading all three scripts at the time of
writing:

- **`test-e2e.sh`'s CSRF rationale.** MyCal's says `-public-url` must match "or CSRF rejects
  every mutating request with 403 and every write test fails." It does not. `csrf.Middleware`
  allows a request carrying neither `Origin` nor `Referer` — the native-client path, stated in
  its own doc comment — so an API-level call sails through a mismatched flag: measured 201 with
  no headers, 403 with either, independently twice. The flag is still required, because in-page
  `fetch` is stamped with the page's origin. The wrong version matters in the direction that
  costs time: it predicts a 403 for exactly the calls that are allowed, sending anyone debugging
  a write failure to the wrong flag. **MyMail and MyNotes have both corrected their wording;
  MyCal's is unchanged.**
- **`e2e/tsconfig.json` exits non-zero and buries real errors — and in MyCal four of them were
  real.** Run with `-p` (not with file arguments, which makes `tsc` ignore the config and
  measure a different program), against a clean `git archive main e2e` extraction, MyCal's own
  config: **100 errors, 96 of them in Playwright's own type definitions and 4 in its tests.**

  | | Errors in its own `tests/` |
  |---|---|
  | MyCal, `main` | **4** — `import.spec.ts` TS2591 `path`, TS2304 `__dirname`, TS2591 `Buffer`; `sidebar-footer.spec.ts:518` TS2345 `'string \| null'` not assignable to `'string'` |
  | MyMail, MyNotes | **0** — both now exit 0 outright on `ES2022` + `skipLibCheck` |

  Two consequences, and they are why this is not merely noise:

  **MyCal is the only one of the three whose suite reaches for Node globals.** `import.spec.ts`
  uses `path`, `__dirname` and `Buffer`; neither other suite touches any of them. So MyMail and
  MyNotes could keep "`@types/node` deliberately not a dependency" for free and MyCal could not
  — **`skipLibCheck` + `ES2022` alone leaves MyCal non-zero**, and fixing it there needed changes
  to test code rather than two compiler options. The three repos are not interchangeable here,
  which is exactly the kind of thing this document exists to record.

  **One of the four is in the file this contract points at.** `sidebar-footer.spec.ts:518`
  passed a `string | null` backdrop into `parseRgb`. `expect(…).not.toBeNull()` is present on
  the line above and **does not narrow the type for `tsc`**. It is the only one of the nine
  `parseRgb(<backdrop>)` call sites across the three suites without a non-null assertion,
  including the two in its own file. MyCal's fix replaces it with a `throw`, which is a better
  answer than the `!` its siblings use — a broken measurement should stop the test where it
  broke, rather than crash three lines later inside a helper.

  > **What that null check does and does not protect against — because the intuitive reading is
  > wrong, and it is wrong in all three repos' comments.** Running `parseRgb` exactly as written:
  >
  > | Input | Result |
  > |---|---|
  > | `null` | **TypeError** — fails loudly |
  > | `'transparent'` | **TypeError** — fails loudly |
  > | `'rgba(0, 0, 0, 0)'` | **`[0, 0, 0]`** — parses to black, scores a huge ratio against a light backdrop |
  >
  > So `parseRgb(null)` is **not** the meaningless pass; it throws. The genuine silent wrong
  > answer is `rgba(0, 0, 0, 0)`, and **what excludes it is the `toMatch(/^rgb\(/)` guard, not
  > the null check.**
  >
  > The null check is still worth having, for a different reason: it distinguishes **"could not
  > look"** from **"looked and disagreed"** — §5.3's rule that a backdrop which cannot be
  > resolved is a failure and never a pass. Two guards, two distinct hazards, and neither
  > substitutes for the other. *(Found by mynotes-dev, which priced the unreachable branch
  > instead of assuming it; reproduced here before recording.)*

  So the conclusion is **understated, not merely intact**: the file was not just noisy, it was
  hiding four defects in the reference suite, one of them on this contract's own
  soft-assertion trap. And the larger point survives any fix: the file is wired into no build
  and no CI in any of the three, so its `strict: true` still buys nothing anywhere.

  > **The clause "every one in `node_modules` and none in any suite's own tests" was false of
  > MyCal, and it is a `AGENTS.md` §3.2 instance that reached this document's text.** The split
  > was measured for MyMail and MyNotes, found to be zero in each, and generalised to the third —
  > whose *total* had been taken but never broken down. The four-error gap between 100 and 96 was
  > visible the whole time and was explained away as "MyCal has extra spec files". **The number
  > that was rationalised was the finding.** Re-measured here from a clean extraction before this
  > bullet was rewritten.

**And the traffic runs the other way too, which this caveat must not be read as denying.**
MyMail's and MyNotes' docs claimed their suites "gate publication in CI" — false, since neither
workflow has ever run (§9.1 above). **MyCal makes the same claim and makes it correctly**, in
`web/AGENTS.md`, *and bounds it*: the workflow triggers on push to `main`, so a breaking commit
is already on `main` when the suite goes red, and what the gate prevents is a broken contract
reaching Pages or the release rather than the commit landing. That is this section's own
"gates publication, not prevents breakage" distinction, written into the app repo.

So the careful version existed in the reference and **the other two did not inherit it.** Two
failures that look identical in a list and are opposites:

| | Direction | Example |
|---|---|---|
| **Defect originates in the reference and spreads** | argues *against* MyCal as the model | the CSRF rationale, the tsconfig |
| **Care originates in the reference and does not spread** | argues *for* it | the bounded gating claim |

Recording only the first kind would make a ledger that indicts the reference while omitting the
evidence for it. *(Distinction owed to mycal-dev, which checked the claim that its repo was the
clean one rather than accepting it.)*

**How that false claim was actually removed is worth recording, because none of it was
procedural.** Each app agent was handed two locations. Both swept their own repo instead and
found more — MyMail three further, MyNotes seven in total, spanning its workflow, three
`AGENTS.md` files, `spec/REQUIREMENTS.md`, its Playwright config and its spec file
(mynotes `d9f8ff1`). A claim of this kind does not live where you expect it to.

And both, independently and without conferring, reached the same judgement about the **workflow
files**: keep the *"placed to gate publishing"* rationale there and qualify it rather than delete
it, because in the file that *defines* the step the phrase is about ordering, and `on: push` is
visible a few lines above. The claim is only false when it is repeated somewhere that context is
missing. MyMail's addition is the durable form, and it is a rule rather than a correction:

> **"Do not describe it as a gate elsewhere in the repo until it has run once."**
> — `mymail/.github/workflows/main.yml`

That inoculates against re-propagation instead of merely undoing this instance, which is the
difference between fixing seven files and stopping an eighth. **Two agents, the same evidence,
the same answer, no conferring** — which is the best available signal that the answer is a
property of the problem rather than of whoever looked at it.

**When this caveat can be retired.** MyCal's fixes for the first two are queued on their own
branch at the time of writing. When they land, this section stops being true — but **retire it
by verifying the fixes, not by assuming them**: read MyCal's `test-e2e.sh` and
`e2e/tsconfig.json` and confirm the wording and the two compiler options, then delete the
bullets. `AGENTS.md` §3.3's discipline applies in the ordinary direction here — the condition
that makes this caveat *live* is written down, so a future reader can check whether it still is.

A third difference was reported and **is not a defect**. Read at the time of writing, in full:
**MyMail and MyNotes both carry `trap 'exit 1' INT TERM PIPE` alongside `trap cleanup EXIT`;
MyCal carries only the latter.** The leak this was thought to prevent did not reproduce — the
report of it turned out to be an artefact of the probe's own marker going into a closed pipe,
the pattern `measurement-protocol.md` records under *the gap read as the answer*. Only `SIGKILL`
leaks, in all three, and nothing can trap that.

Recorded so the next person comparing the three scripts does not re-derive a bug from the
inconsistency — **and stated as which-repo-has-what rather than as "some do and some do not"**,
because the vague form is what let a wrong version of this survive a report. Two successive
accounts of this line have now been wrong in two different directions. If you are about to
restate it, read all three files rather than any summary of them, this one included.

### 9.2 What CI does **not** catch

MyCal applied all seven items on its silent-breakage list and recorded which assertion fired.
**Six are caught. One cannot be:**

> **Normalising `font-size: 0.80rem` to `0.8rem` is not catchable by any test.** The computed
> *and* serialised values are identical, so nothing in the CSSOM or the rendering can
> distinguish them.

That pin is held by **review, not CI** (§2.1). Do not read "MyCal's assertions run in CI" as
covering the whole list — this one item is exactly as exposed as it was before, in all three
repos.

**And a green suite bounds what was checked, not what is correct.** MyCal's narrow-layout test
asserts only the footer's left edge — its comment says so plainly, and it was a deliberate,
documented limit. Then a change broke that layout badly enough to be obvious on sight, and
**the suite stayed green**, because the breakage was in the axis the test had declared out of
scope. A documented blind spot is still a blind spot; writing it down makes it honest, not
covered.

**The reference implementation has the least complete suite of the three**, and that is worth
stating plainly rather than leaving to be inferred from §9's table. Three gaps, all in MyCal:

- **§8.5, the full-bleed separator**, was asserted by nothing at all until the two new suites
  landed, and **it is still asserted by nothing in MyCal**.
- **§8.4's 4px floor** — same. Both are held in MyMail and MyNotes.
- **§8.3 requires mechanism B to be measured at *both* scroll extremes**, because a sticky
  element behaves differently at each end of its range. MyCal's two page-scroll tests scroll to
  the bottom only. MyMail's sidebar-overflow tests do visit both ends; MyCal's do not.

None of these is a claim that MyCal is wrong — its numbers were measured by hand at the time and
§8.3 records them. It is a claim about what would still be true *tomorrow* if someone changed
it, which is the only thing a suite is for.

> **This paragraph used to close on a sharper formulation, and it has been overtaken:**
> *"What runs is not what is most thorough, and what is most thorough does not run."* That was
> true while MyCal's was the only pipeline. **All three now run** (§9.1), so the second half is
> simply false, and the gap it named has changed character rather than closed: the three gaps
> above are still real and still MyCal's, but they are now gaps in a suite that runs beside two
> more complete suites that also run.
>
> Recorded rather than deleted because the sentence was quotable and will have been quoted. It
> is the kind of line that outlives the condition that made it true — which is `AGENTS.md` §2.5's
> complaint, and the reason §11 exists.

§8.5 is a good example of why the remaining gap matters rather than being merely untidy. The
prohibited alternative — insetting the buttons with a horizontal margin instead of the footer's
padding — puts the buttons in exactly the right place and the separator in the wrong one. **No
position assertion can see it**, which is why §8.5 exists as a separate rule; and in the
reference implementation, nothing looks at it. The habit here is to record where that
implementation is behind rather than to flatter it, and this is where it is behind.

---

## 10. Known gaps and open items

Stated honestly. None of these is a reason to hold up work; all of them are reasons not to
be surprised.

### Open, with the human

1. **The hover fill does almost no visual work — in all three apps.** The fill was always
   faint; no rule about the backdrop has ever fixed that, and the current one does not
   either. Fill against each app's own backdrop:

   | | Light | Dark |
   |---|---|---|
   | MyCal | 1.125:1 | 1.721:1 |
   | MyMail | 1.101:1 | 1.424:1 |
   | MyNotes | 1.053:1 | 1.424:1 |

   The floor in §5.1 exists to stop this reaching 1.000 again; it does not make the fill do
   work. **Clearing a floor and being visible are different claims** — as was
   *"hover is now identical across the suite"*, which was true of the old figures and read as
   stronger than it was.

   Not a defect and not a standards failure. Hover stays clearly signalled by the **border and
   text, which both change in both themes** — so even at 1.000:1 the control still responded,
   which is why the invisible fill was a degradation rather than a loss of function. §5.5
   exempts the fill because the label identifies the control.

   Raising it is a **design** change, it touches other components in two repos, and no
   criterion requires it. With the owner as an optional follow-up. **Do not act on it in one
   app** — and note that this is where the direction question belongs: MyCal's light fill now
   *darkens* against its backdrop like the other two only because `#e5e7eb` was chosen over
   `#ffffff` (§5.1), and a suite-wide redesign should settle direction deliberately rather
   than inherit it from three separate local choices.
2. **MyCal's light resting label — the 4.393:1 failure — has now been introduced twice and
   fixed twice.** First by leaving the backdrop unpinned; then again when the backdrop pin was
   withdrawn (§5.3) on an instruction about appearance that said nothing about contrast. It is
   currently fixed, by a MyCal-local label value measuring 6.867:1 (§5.1).

   Kept as an open entry rather than closed, because **the failure mode is live, not
   historical**: MyCal's light backdrop `#f3f4f6` cannot carry the shared `#6b7280` label. Any
   future change that reverts MyCal's label to the shared value, or moves another app's
   backdrop toward `#f3f4f6`, reintroduces it. §5.4's two near-line rows (MyNotes at 0.126
   over, MyMail at 0.334 over) are where it would surface next.
3. **`aria-pressed` alongside an action-phrased name.** All three toggles carry
   `aria-pressed={dark}` *and* an accessible name of "Switch to light mode", so a screen
   reader announces "Switch to light mode, pressed" — ambiguous about what "pressed" refers
   to. A toggle should either name the control and let `aria-pressed` carry state, or name
   the action and drop `aria-pressed`. Ours does both. This predates the shared contract in
   all three repos. Deferred as a three-repo wording decision that also risks MyCal's e2e
   locators, which match accessible names by substring.
4. **App-wide focus indicators.** The `outline: none` + translucent-ring pattern this
   contract removed from these two controls is still present on many other controls in these
   apps — many rules in MyMail's stylesheet alone, including `.folder-item a` and
   `.sidebar-reload-btn` *in the same sidebar*, so tabbing down it watches the indicator come
   and go. (Deliberately not a count: an exact figure here would be an untestable number in
   prose, which is the thing §11 and `AGENTS.md` §2.5 warn against. Count it when you need
   it.) Deferred as scope expansion, not a defect in this contract. It is not a
   find-and-replace: several of those are inputs in tight containers that need the same
   clearance check §8.4 describes.

### Accepted risks

5. **Chromium-on-Linux is the whole evidence base.** Accepted by the human: *"It's enough if
   you measure and test with Chromium for now."* This works as a proxy because most of what
   is matched — padding chains, panel offsets, box geometry in `rem` and `px` — is
   engine-independent. Font *face* is the part that is not, and that is the part accepted.
   Do not spend effort trying to launch Firefox; the sandbox pins Chromium.
6. **Font substitution** (§4). `system-ui` resolves per platform, so 174px is a
   this-container reading. Three repos agreeing shows the implementations agree, not what a
   given machine renders.

### Structural

7. **There is no cross-repo test that runs automatically.** Nothing that runs anywhere can
   detect that one app has drifted from the other two. **This is the largest gap, and it is
   untouched by everything that has just changed.**

   *(The qualifier is load-bearing and this item used to lack it. `tools/check-contract.py` —
   described forty lines below — is a cross-repo test; what it is not is one that anything
   runs. The unqualified version contradicted the rest of its own item. See `AGENTS.md` §3.5.)*

   This item used to carry two claims at once. They have come apart, so they are separated
   here — and the half that closed is the smaller half.

   **Closed: the two missing suites.** MyMail and MyNotes now each have a
   `sidebar-footer.spec.ts` holding their own half of this contract, each accepted by a
   demonstrated red (§9.1). The sentence this item used to carry — *"every number either of
   them has reported is hand-measured"* — is no longer true, and neither is *"two thirds of
   this contract rests on measurements that were correct once, on one machine."*

   **Open, and undiminished: nothing can see between the repos.** Three suites are still three
   one-sided guards. Each proves its own app satisfies the contract and is structurally blind
   to the other two — so if MyMail's row moves, MyCal's pipeline stays green, *correctly*, and
   so does MyNotes'. **Adding suites cannot close this, however many are added**, because the
   thing missing is not coverage of each app but a comparison between them. That is a
   difference in kind, not in degree, and it is the reason this item keeps the weight it had.

   One further reason the closed half is worth less than it looks:

   - **`0.80rem` is uncatchable even within a single app** (§9.2), so per-app coverage has a
     floor it cannot reach by construction.

   > **A second reason stood here and has expired:** *"Two of the three suites do not run …
   > what exists today is one pipeline and two files. A file that would go red is not a guard
   > until something runs it."* **All three now run in CI** (§9.1), so that is three pipelines.
   >
   > **This changes nothing about the item it sits under**, which is the point worth taking. The
   > open half was never about how many suites run — it is that no suite of any kind can see
   > between the repositories. Three running pipelines are three one-sided guards where there
   > were one pipeline and two files, and the comparison between apps is still performed by
   > nothing that runs. The heading's claim is intact and is now the *only* thing this item
   > claims.

   **A partial cross-repo guard now exists: [`tools/check-contract.py`](../tools/check-contract.py).**
   The human lifted this repo's Markdown-only rule for it. It reads the three sibling
   stylesheets and fails if they disagree on a pinned value — the literals, and the §5.1
   colours resolved through each app's own tokens, in both themes. It never renders
   anything, so it is immune to every staleness trap in `measurement-protocol.md`.

   It is the only thing anywhere that can see **cross-repo** drift, and the only thing that
   can catch `0.80rem` → `0.8rem` at all (§9.2). It also catches the §3.1 class — a pin
   deleted in the app where its value already arrives by another route, which that app's own
   rendering cannot detect by construction.

   Its limits are real and are printed on every green run rather than left in this document:
   **geometry, the cascade, and markup are all invisible to it.** A footer padding changed
   from 8px to 24px — moving the buttons off (8, 8), the violation this whole contract exists
   to prevent — passes it cleanly. Rendering and this check are complements; neither sees
   what the other does.

   **Shown red for the right reason**, per `measurement-protocol.md`, rather than merely
   shown green — for one pin of each kind it checks:

   | Break | Result |
   |---|---|
   | `0.80rem` → `0.8rem` in MyMail | fails §2.1, naming repo, file and rule |
   | `--text-subtle` `#6b7280` → `#6b7281` in MyCal | fails §5.1 resting text, resolved through the token |
   | `padding: 4px 8px` → `4px 10px` in MyNotes | fails §2 button.padding |
   | delete `flex-shrink: 0` from MyCal | fails §2.3 — the §3.1 class, invisible to MyCal's own rendering |
   | MyCal's backdrop, in the live repos | went red, then **green** when MyCal landed the change (see the note below on which commit that was) |

   The last row is the only one that was not staged: the contract was written ahead of the
   code, the check reported the difference, and it cleared when the change landed. **That is
   the first acceptance signal in this work that did not come from the agent making the
   change.**

   > **That row named `9aa9cae`, and no branch contains that commit.** It was real when it was
   > recorded — the green run genuinely happened against it — and MyCal then amended it away.
   > What is on `main` is `282f00f`: same parent (`7e65102`), same subject, thirteen minutes
   > later, carrying more than the original did.
   >
   > The acceptance signal stands. **`git show 9aa9cae` does still resolve in that repo** — an
   > unreferenced object survives until it is garbage-collected — so the failure is not that the
   > hash is unreadable today but that **nothing reaches it from any branch**, and one `gc` ends
   > even that. A hash that resolves only from a reflog is not a citation anyone else can follow.
   >
   > Recorded rather than quietly swapped for `282f00f`, because the substitution is an
   > inference — the two are not the same object, and saying "it landed as `282f00f`" would
   > assert a history I reconstructed rather than one I read. **This is `AGENTS.md` §2.5's own
   > failure, in this repository, in the document that warns about it**: two of the three app
   > repos once shipped comments describing a rule's removal that had only ever existed in an
   > uncommitted amend chain, and this is the same defect one level up. Naming a commit is what
   > makes a claim checkable, and it is also what makes it perishable when somebody rebases.
   > **Prefer naming the commit anyway** — an unresolvable hash announces itself, and a
   > description with no hash does not.

   `--self-test` proves the *parser* still behaves as the checks assume, with ten inline
   cases. It exists because a parser defect is how thirty assertions go green-and-blind at
   once — two such defects were found in review, one of them live: `@import` was swallowing
   the rule that followed it, dropping a real rule from MyNotes' stylesheet.

   **Nobody's CI runs it.** It is a script someone has to run — precisely the state §9.1
   describes MyCal's suite as having been in before `7e65102`. Wiring it in would mean
   choosing whose pipeline runs it, and would need all three repos checked out there, which
   no app repo's CI currently does. **Until then it guards nothing on its own**, and what
   fixes the self-measurement problem is not the script existing but its being run by someone
   other than the author.
8. **MyCal's narrow layout sits exactly on the 4px floor.** Below 600px `.app`'s padding
   drops to 4px and the sidebar stacks under the main content, so **B = 4, not 8**. That is
   within §8.4's floor but with *nothing* spare — the focus outline's outer edge lands
   precisely on the window edge. Deliberately out of scope and documented rather than left
   to be discovered; the left edge is still asserted. Any future reduction anywhere in that
   chain starts clipping the indicator.

   **This is MyCal's alone, and the other two are better rather than merely different.**
   Measured at a 375 × 700 viewport, 16px root, Chromium on Linux:

   | | L | B |
   |---|---|---|
   | MyCal | 8 | **4** |
   | MyMail | 8 | 8 |
   | MyNotes | 8 | 8 |

   MyMail has no width breakpoint at all — one media query in its whole stylesheet,
   `@media (hover: none)` — so nothing about its layout responds to width and the footer keeps
   the contract's 8. MyNotes has no breakpoint either and clips instead, via `.app-body`'s
   `overflow: hidden`. So the contract's own coordinates are **fully satisfied at a phone width
   in two of three apps**, and the exemption is one app's.

   Worth stating in that direction, because "narrow layouts drop to B = 4" would read as a
   property of the contract rather than of MyCal, and a reader checking MyMail or MyNotes
   against it would find a disagreement that is not there.
9. **MyNotes' demo builds have only one control.** Settings is rendered only when
   `!isDemo()`, because a demo has no server to hold the MyMail URL. The geometry contract
   still applies to the toggle; the pair does not exist.
10. **`0.80rem` is unenforceable** (§2.1). A formatter could normalise it with no test
   failing anywhere. Recorded as minor.
11. **Settings has a hover tooltip in two apps and not the third.** MyCal and MyNotes set
    `title="Settings"`, so hovering shows the browser's native tooltip; MyMail's anchor sets
    no `title`, so hovering shows nothing (§7). The accessible name is `Settings` in all
    three either way, so this is not an a11y defect — but it is a small user-visible
    difference in a contract whose goal is that the three behave identically. Never
    specified in either direction. Unresolved; not worth a three-repo change on its own,
    worth folding into the next one that touches this markup.

### Unspecified — a question for the human, not a defect

12. **The contract says nothing about horizontal page scroll, and in MyMail the controls leave
    the window.** §8's (L, B) is measured against the viewport, and §8.3's two threats are both
    vertical. Nothing anywhere addresses the horizontal axis, which was never a decision — the
    case simply did not arise while the rules were being written.

    It arises in MyMail. Nothing in its layout responds to width, so its shell has a
    **min-content width of 415px**; below that the *document* scrolls horizontally. Scrolled
    fully right at a 375px viewport, the toggle measures **L = −32** — it is off the left of
    the window entirely. *(A Chromium-on-Linux, 16px-root, this-container reading, in §2.4's
    sense: `scrollX` reaches 40 and L is 8 − 40. The 415px is a binary search — 414 still
    scrolls, 415 does not — and it depends on the rendered text width, so it is a reading and
    not a constant.)*

    **Measured against all three, because it is exactly the shape `AGENTS.md` §3.2 warns
    about.** The tempting general statement — *"these apps do not respond to width, so they
    scroll horizontally when narrow"* — is false of two of them:

    | | Horizontal document scroll at 375px | Why |
    |---|---|---|
    | MyCal | **no** | its `@media (max-width: 600px)` stacks the sidebar under the content |
    | MyMail | **yes** — `scrollWidth` 415 in a 375 window | one media query in the stylesheet, and it is `(hover: none)` |
    | MyNotes | **no** | no breakpoint either, but `.app-body { overflow: hidden }` clips rather than widening the document |

    So MyMail is exposed and the other two are not, and they avoid it by two different
    mechanisms, neither of which this contract asks for.

    **Left unasserted deliberately, and that was the right call.** MyMail's suite asserts the
    at-rest values and writes the blind spot down rather than either asserting a number or
    "fixing" the layout — a fix here would be a responsive-design change to an app, decided in
    an app repo, on the strength of a contract that says nothing about it (`AGENTS.md` §2.2).

    **The question for the human, stated as a question:** should this contract say anything
    about the horizontal axis — and if so, is the requirement about *the controls* (they must
    remain within the window at every reachable scroll position) or about *the app* (the
    document must not scroll horizontally at supported widths)? Those are different rules with
    different owners: the first belongs here, the second is a per-app layout decision this
    document has consistently refused to make (§6.4 declines exactly that for the sidebar
    column). **Not settled here.** Until it is, the honest position is that MyMail's behaviour
    violates nothing, because there is nothing to violate.

---

## 11. History worth keeping

Rules that were tried and **withdrawn**. They are listed so that nobody re-derives them from
an old comment or an old report:

| Withdrawn | Replaced by | Why |
|---|---|---|
| `font-size: 0.85rem`, height 30.4px | `0.80rem`, 29.2px | 0.85rem overflowed the narrowest sidebar by 18px |
| "8px from the sidebar panel's inner edge" | (L, B) = (8, 8) from the window, §8 | Container-relative offsets let three correct apps land in three places |
| `outline: none` + translucent `box-shadow` ring | Offset outline, §6.2 | Measured 1.28:1 / 1.50:1; no alpha value can fix dark |
| `@media (forced-colors: active) { outline: revert }` | Nothing — deleted | An outline is painted under forced colours; the block would override the real fix |
| WCAG 2.4.11 cited for contrast | 1.4.11, §6.3 | 2.4.11 is Focus Not Obscured |
| Footer inset by horizontal margin | Full-bleed footer, inset by padding, §8.5 | The separator must span the whole sidebar |
| "The backdrop behind the controls is the app's `--surface`" | Per-app recorded backdrop, §5.3 | Owner ruling: MyCal's footer must sit on the left column's background, and the three are accepted to differ |
| "MyNotes' buttons inherit `font-weight`, `font-style` **and `text-align`** from `body` via `button { font: inherit }`" | The per-property route table, §3 | `text-align` is not in the `font` shorthand, so `font: inherit` never displaces the UA's `text-align: center` on buttons. MyNotes takes alignment by MyCal's route, and MyMail's Settings anchor is the only control in the suite that inherits it |
| "Deleting a pin from MyCal breaks the match with MyNotes" | The detectability table, §3.1 | With every `body` at its shipped typography, deleting a pin changes no computed value in **any** of the three. The divergence is latent everywhere, not visible somewhere |
| "MyCal's `sidebar-footer.spec.ts` is the only machine-checkable statement of this contract anywhere" | The three-suite table, §9 | MyMail and MyNotes now have one each. The cross-repo half of the gap (§10.7) is unaffected |

**The first two of those are the same defect at two removes**, and both were written by
someone who had the mechanism right for the app in front of them. The route table in §3 exists
because a per-app claim was not per-property enough — `AGENTS.md` §3.2's pattern arriving on an
axis it had not previously arrived on. Checking against all three *apps* by name would not have
caught either one; checking each *property* against each *control* did.

**Two of these were withdrawn on the owner's instruction rather than because they were
wrong**, and the distinction is worth keeping. The `--surface` rule was not mistaken about
accessibility — it fixed two real defects and its reasoning still stands. It was overreaching
about **appearance**: it specified a colour when what it needed to specify was a relationship.

The practical form of that, for anyone writing a rule here: **prefer pinning the constraint a
value has to satisfy over the value that satisfies it today.** A rule stated as a relationship
survives an appearance ruling; a rule stated as a colour is withdrawn by one.

And a withdrawal is never confined to the section it lands in. Retiring this one **put a
WCAG 1.4.3 failure straight back** in the app whose appearance was being adjusted (§5.4,
§10.2), because the withdrawn rule had been holding up something it was not written about.
**Re-derive everything a rule was carrying before retiring it**, not just the thing it was
named for.

**Two of the three repos once shipped comments describing histories that never existed in
their own repository** — describing a ring being removed, when that ring had only ever
existed in an amend chain. A comment that describes history nobody can see from the diff is
worse than no comment. Prefer an assertion over prose.

**And this document has now done it too**, which is why §10.7 carries the note rather than a
quiet correction: it cited `9aa9cae` as the commit whose landing turned the cross-repo check
green, and that commit is on no branch. It was real when it was written down and was amended
away afterwards.

The practical rule that follows, since this will recur in any three-repo change:

> **A commit hash is the most checkable thing you can write and the first thing to rot.** Name
> it anyway — an unresolvable hash announces itself, where a description with no hash fails
> silently. But **do not record a hash from a branch that is still being amended, or one that
> has not been pushed**: there, the cost is paid and the benefit is not, because nobody else
> can resolve it even while it is current.

That is the reason §9.1's table gives commits for MyCal and deliberately gives none for MyMail
and MyNotes. Both of those branches were being amended while this section was written — one of
them twice within the hour — so any hash here would have named a commit that had already
stopped existing.
