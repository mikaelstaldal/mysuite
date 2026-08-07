# Sidebar footer — theme toggle and Settings

**Status:** binding. Implemented in MyCal, MyMail and MyNotes.

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

They are pinned because the three apps arrive at the same values **by three different
mechanisms**, which means they agree by coincidence rather than by contract:

- **MyCal** — `<button>` elements take weight and style from the UA `button` rule's `font`
  shorthand, and alignment from the UA's separate `text-align: center` on buttons. Nothing
  is inherited.
- **MyMail** — its toggle is a `<button>` and works like MyCal's, but its Settings control
  is an `<a>`, which inherits all three from `body`. Two controls in one app, two routes to
  the same value. This was proved live: setting
  `body { font-weight: 700; font-style: italic; text-align: right }` moved the anchor and
  left the button untouched.
- **MyNotes** — its own `button { font: inherit }` rule means the UA button font never
  applies at all, so its buttons inherit from `body` the way MyMail's anchor does.

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

### 5.3 What the controls sit on is *not* specified — and it shows

This contract pins the colours of the controls but has never pinned the backdrop behind
them, and the three differ:

| | Light | Dark |
|---|---|---|
| MyCal — footer paints `--bg` | `#f3f4f6` | `#111827` |
| MyMail — sidebar paints `--surface` | `#ffffff` | `#1f2937` |
| MyNotes — sidebar paints `--surface` | `#f9fafb` | `#1f2937` |

Three consequences, all known and all live:

1. **The light hover fill is invisible in MyCal.** The mandated `#f3f4f6` is the same colour
   as MyCal's own footer background. Hover stays clearly signalled there — border and text
   both change, in both themes — but "identical on hover" is not currently true across the
   suite. See §10.1.
2. **Focus contrast is a per-app number** (§6.2). Do not copy another app's figure.
3. **The resting label fails WCAG 1.4.3 in MyCal's light theme.** Same root cause, and it
   is the one that is an accessibility defect rather than a cosmetic difference. See §10.2.

### 5.4 Text contrast — WCAG 1.4.3 Contrast (Minimum), Level AA

The label is 12.8px at `font-weight: 400`. That is normal text, so the threshold is
**4.5:1**, not the 3:1 large-text allowance.

Resting text, against each app's own backdrop:

| | Light (`#6b7280`) | Dark (`#9ca3af`) |
|---|---|---|
| MyCal | **4.393:1 — fails** | 6.987:1 |
| MyMail | 4.834:1 | 5.782:1 |
| MyNotes | 4.626:1 | 5.782:1 |

**Hover text is measured against the hover fill, not the panel** — during hover that fill is
the surface the label sits on. Because the fill is mandated (§5.1), the numbers are the same
in all three apps rather than a per-app range:

| | Text on fill | Ratio |
|---|---|---|
| Light | `#1f2937` on `#f3f4f6` | 13.338:1 |
| Dark | `#f3f4f6` on `#374151` | 9.366:1 |

Both clear 4.5:1 with large margins, so hover is never the problem. (MyCal is the one app
where the two surfaces coincide — its panel *is* `#f3f4f6` — which is §10.1, not a contrast
issue.)

**The failure is the resting state, in one app, in one theme** — and it is a defect, not a
difference. Recorded as an open item in §10.2; do not fix it in MyCal alone.

### 5.5 The control boundary — why no contrast figure is given for the border

With `background: none`, the 1px border is the control's only boundary, and it is nowhere
near 3:1 against what it sits on:

| | Light (`#e5e7eb`) | Dark (`#374151`) |
|---|---|---|
| MyCal | 1.125:1 | 1.721:1 |
| MyMail | 1.238:1 | 1.424:1 |
| MyNotes | 1.185:1 | 1.424:1 |

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
~186px spare. The resize case never binds there, so converting would have been churn. MyCal
and MyMail had no such margin and had to convert.

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

### 8.3 Taking the footer out of the scroll flow

A footer inside a scrollable panel has to be removed from the scroll flow, or it moves. The
general mechanism is:

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

**Treat this as the normative approach for any app whose sidebar can overflow**, rather than
as a local quirk. It was first written down as a MyCal detail — MyCal needed it because its
month and year views page-scroll — but MyMail needs the identical mechanism for an unrelated
reason, which is what shows it to be general rather than specific. An app whose sidebar
genuinely cannot scroll does not need it; an app that is not sure does.

The explicit **opaque background** is part of the mechanism, not decoration. A sticky footer
with a transparent background has content sliding visibly underneath it.

Around that, per-app detail is local:

- **MyCal** cannot use a uniform padding, because `e2e/tests/calendar-views.spec.ts` pins the
  footer *box*'s bottom edge to the bottom of the view beside it — the box may not move down
  even though the buttons must. It therefore cancels `.app`'s horizontal padding with
  `margin-left: calc(-1 * var(--app-padding-x))`, uses `padding: 8px 8px 0` so `.app`'s own
  8px supplies B rather than doubling it, and sets `bottom: 8px`.
- **MyMail** and **MyNotes** sit flush against the window edge, so their footer padding alone
  supplies both coordinates when nothing scrolls.

**Differing here is not a deviation** — the coordinates are the contract, not the
declarations that produce them. Read §8.5 before concluding otherwise.

> **Open at the time of writing.** MyMail has landed sticky + an explicit background. MyCal
> and MyNotes are measuring their own overflow cases before changing anything, so that one
> mechanism is chosen for all three rather than two agents inventing two. When those numbers
> arrive this section should say which mechanism all three use. Until then, the *requirement*
> in §8.2 is settled and binding; the uniform mechanism is not yet chosen.

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

---

## 9. Verifying a change

See **[`measurement-protocol.md`](measurement-protocol.md)**. It is short, and skipping it
is how every wrong measurement in this contract's history got taken.

The one-line version: **a green build proves nothing about geometry**, because all three
apps embed `web/static/` into the binary and a running server keeps serving what it started
with.

MyCal's `e2e/tests/sidebar-footer.spec.ts` is the only automated guard this contract has
anywhere (§10). Read it before changing anything here — it encodes the acceptance height,
both viewport coordinates in all five views, theme-toggle width stability, overflow
headroom at 20px and 24px roots, and composited focus contrast in both themes.

---

## 10. Known gaps and open items

Stated honestly. None of these is a reason to hold up work; all of them are reasons not to
be surprised.

### Open, with the human

1. **Hover is not identical across the suite.** The mandated light hover fill `#f3f4f6` is
   the same colour as MyCal's own footer background, so the fill is invisible there while
   MyMail and MyNotes show it against `--surface` (§5.3). Same declaration, different
   result, because the contract pins the fill but not what it sits on. Not an accessibility
   problem — border and text both change in both themes — but "identical on hover" is
   currently false. Fixing it means changing either a backdrop or the mandated fill colour,
   and both are visible changes in all three apps with two defensible answers.
   **Document it where you find it; do not fix it in one app.**
2. **The resting label fails WCAG 1.4.3 (AA) in MyCal's light theme — 4.393:1 against a
   required 4.5:1** (§5.4). This is the same root cause as §10.1 — the contract pins the
   colour but never pinned what it sits on — but unlike §10.1 it is a real accessibility
   defect rather than a cosmetic inconsistency. It is *narrow*: resting state only, light
   only, MyCal only; hover clears 13:1 and dark clears 5.7:1 everywhere.

   **Do not fix it in MyCal.** The two candidate fixes are darkening the mandated resting
   text for all three apps, or changing MyCal's footer backdrop — and those are the *same
   two candidates* as §10.1, which is why the two should be decided together rather than
   separately. Darkening the text fixes both at once; changing MyCal's backdrop fixes both
   at once; doing one of each could fix one and worsen the other.
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

7. **There is no cross-repo test.** Nothing anywhere can detect that one app has drifted
   from the other two. MyCal's `sidebar-footer.spec.ts` is one app's half of the contract —
   and **MyMail and MyNotes have no e2e suite at all**, so every number either of them has
   reported is hand-measured and guarded by nothing in CI. Two thirds of this contract rests
   on measurements that were correct once, on one machine. **This is the largest gap.**

   **A proposal, needing a human decision because it breaks this repo's own rules.** A
   cross-repo guard does not need a browser and does not need CI in the app repos: one
   script here that reads the three sibling stylesheets and fails if they disagree on the
   values this contract pins as literals — `0.80rem`, `padding: 4px 8px`, `gap: 6px`,
   `border-radius: 6px` (resolved), `outline: 2px solid`, `outline-offset: 2px`, and the
   twelve hex values of §5.1. It would catch exactly the drift §2.3 and §5.2 say is the
   shared thing, and it is immune to the staleness trap in `measurement-protocol.md`
   because it never renders anything.

   What it would *not* catch is geometry — computed height, the (8, 8) position, overflow —
   which needs a rendered page and therefore an e2e suite in each app. So this is a partial
   guard, and worth being honest that it is.

   It requires a deliberate exception to "Markdown only, no build system" (`AGENTS.md` §3),
   which is why it is recorded here as a proposal rather than done. **Do not add it without
   the human's decision.**
8. **MyCal's narrow layout is out of scope for B.** Below 600px `.app`'s padding drops to
   4px and the sidebar stacks under the main content. The 8px *bottom* rule is deliberately
   not asserted there; the left edge still is.
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

**Two of the three repos once shipped comments describing histories that never existed in
their own repository** — describing a ring being removed, when that ring had only ever
existed in an amend chain. A comment that describes history nobody can see from the diff is
worse than no comment. Prefer an assertion over prose.
