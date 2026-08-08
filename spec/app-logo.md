# App logo — the badge in the top left

**Status:** binding. Implemented in **MyCal** and **MyMail**; **MyNotes implementation in
progress** — see §10. Two of three is a transient state, not a standing exemption: the human has
ruled that MyNotes gets the badge and has chosen how to make room for it (§10.1).

**Scope: the logo only.** The app-name label beside it is **out of scope** — §2 states that as a
ruling, with the human's words and the condition attached. Read §2 before concluding the labels
were forgotten.

**Written from** the three apps' shipped code, which is the ground truth wherever it and a
document disagree (`AGENTS.md` §4), as measured and reported by the three app agents:

- **mynotes-dev**, message #509 — MyNotes feasibility, at mynotes `d9f8ff1`, clean tree.
- **mymail-dev**, message #511 — MyMail ground truth, at mymail `07d14cf`, clean tree.
- **mycal-dev**, message #513 — MyCal ground truth, at mycal `2e68ef3`, clean tree.
- **mysuite-manager**, messages #496, #498, #503, #510, #516, #517 — the task brief, the human's
  instruction quoted in full, and the rulings recorded throughout this document.
- My own read of the three repositories at the commits above, used to frame the measurement
  requirements and to check the reports rather than transcribe them.

**If you find a ruling cited here that is not in that list, it was not available when this was
written — get it and check this document against it** (`AGENTS.md` §3.1).

Every number below is a **rendered measurement** unless it says otherwise. Where a figure is a
reading rather than a constant, it says so and says what it was read on.

---

## 1. What this covers, and where

One element per app: a rounded square holding an app-specific mark, at the top left.

| | MyCal | MyMail | MyNotes |
|---|---|---|---|
| Badge | `.brand-logo` (`<span>`) | `.logo-icon` (`<div>`) | *to be recorded when it lands* |
| Mark | `<Logo/>`, `web/ts/components/Logo.tsx` | `<Icon name="mail" size={17}/>` | from `web/static/favicon.svg` (§6.3) |
| Container | `.brand`, in `<header class="top-bar">` | `.sidebar-header`, in `<nav class="sidebar">` | `.sidebar-header`, in `<aside class="sidebar">` |
| Stylesheet | `web/static/app.css` | `web/static/app.css` | `web/static/app.css` |
| Markup | `web/ts/app.tsx` | `web/ts/layout/Sidebar.tsx` | `web/ts/app.tsx` |
| App-name label **(out of scope, §2)** | `.brand-name` (`<span>`) | **no selector — a bare text node** | `.brand.sidebar-brand` (`<a href="/">`) |

**MyMail's label cell is not an omission.** Its app name is a bare text node inside
`.sidebar-header` with no element of its own, so there is nothing to name. Recorded explicitly
because a blank cell reads as "not looked up" (`AGENTS.md` §3.5).

The three sit in **structurally different containers** — MyCal's in a top bar spanning the
window, MyMail's and MyNotes' in a sidebar header. That difference is why §4 pins placement and
not coordinates, and it is not a defect in any of them.

---

## 2. The app-name label is out of scope — a ruling, and whose

**This is the human's ruling, quoted in full** from their instruction (relayed by
mysuite-manager, message #498; typos in the original, corrections in brackets):

> "Add a new common UI pattern in the mysuite repository for having the app logo in top left as
> MyCal and MyMail currently have. Adapt MyNotes to this pattern by adding its logo there.
> Note: this pattern should only cover the logo, not the app name label (which is smaller in
> MyNotes, and should remain that why [way] for now since there space there is crowded)."

So: **the label's typography is not specified by this contract, and MyNotes' label is
deliberately smaller than the other two.** Measured, so the gap the ruling is about has a number:

| | Label computed `font-size` at a 16px root | Source |
|---|---|---|
| MyCal | **17.6px** (`1.1rem` on `.brand`) | mycal-dev |
| MyMail | **17.6px** (`1.1rem` on `.sidebar-header`) | mymail-dev |
| MyNotes | **16px** — `.brand` declares no `font-size`, so this is `body`'s inherited `1rem` | mynotes-dev |

**The difference is 1.6px, and it exists because MyNotes never set a size rather than because it
set a smaller one.** Worth knowing before anyone "restores" it.

**The condition is in the ruling and is the operative part.** *"For now, since space there is
crowded"* — so the deferral is not open-ended: **the label stays smaller while MyNotes' top-left
is crowded, and relieving the crowding is what puts the question back on the table.**
(`AGENTS.md` §3.3 — a deferral recorded with the condition that makes it safe, rather than as a
bare "for now".) Note that §10.1's widening relieves *some* crowding; it does not settle this,
because the human ruled the label separately and only they can reopen it.

**What is in scope even though the label is not:** the 8px gap between badge and label (§3.4),
and the badge's *ordering* relative to the label (§4). Both are properties of the row, not of the
label's typography, and neither makes any label bigger. That reading is deliberate and is the one
place this exclusion is read narrowly.

---

## 3. The mandated values

Resolved values, measured on rendered pages by the three app agents, at 1280–1920 widths, both
themes, 16px and 24px root font sizes, across content volumes. Token names are per-project and
are **never** what is mandated (`AGENTS.md` §2.3).

### 3.1 The badge

```
box                28 × 28 px      rendered, not the authored value
border-radius      6px
background         #2563eb  light  /  #3b82f6  dark
color (glyph ink)  #ffffff         both themes
display            flex
align-items        center
justify-content    center
flex-shrink        0
opacity            1               no filter
```

Padding, margin and border are all zero, and `box-sizing` is `border-box` in both shipped apps.

**The box is absolute `px` and does not scale with the root font size.** That is a decision, not
an accident — see §9.2, which records what it costs.

### 3.2 The glyph

```
box        17 × 17 px    RENDERED, measured
centring   equal insets, (28 − 17) / 2 = 5.5px on all four sides
ink        #ffffff, via currentColor from the badge's own `color`
```

**"Renders at 17 × 17 measured" is the rule, never "the attribute says 17."** *(Phrasing owed to
mycal-dev.)* The distinction is load-bearing because the two shipped apps reach the same 17 from
**different layers** (§5), and a CSS rule can silently override an SVG attribute. A check that
reads an attribute and calls it verified has checked nothing.

### 3.3 The mark's extent inside the glyph box

> **The mark's rendered ink must span at least 85% of the glyph box on its larger axis.**
> The shorter axis is not constrained.

Measured **stroke/ink-inclusive**, not as a bare `getBBox()`. Shipped readings:

| | Larger axis, stroke/ink-inclusive | Construction | Source |
|---|---|---|---|
| MyCal | **93.75%** (pixel ink 88.24%) | mixed fill + stroke + `<text>` | mycal-dev |
| MyMail | **91.67%** (pixel ink 92.65%) | **stroke-only**, vendored Lucide 1.25.0 | mymail-dev |
| MyNotes | **34.4%** — fails, and is being built to the rule | fill-only | mynotes-dev |

**Why this rule exists.** Without it the contract cannot see a 3× difference in apparent size:
MyNotes' favicon mark fills 31% of its viewBox where MyCal's fills 87.5%, so reusing it unchanged
would put a ~5.3px mark inside the same 17px box as MyCal's ~15px one — passing every box
measurement while visibly failing "the three look like one product". *(Found by mynotes-dev
before implementing, which is the only reason it is a rule rather than a defect.)*

**Three qualifiers, each corroborated by the agent whose mark it applies to:**

- **Larger axis only.** MyMail's mark measures 91.67% × 75.00% because an envelope is a wide
  rectangle and a calendar is roughly square. A single scalar cannot describe marks of different
  shapes, and the contract does not want it to — *"an extent rule cannot be a single number for
  marks of different shapes"* (mycal-dev).
- **Stroke/ink-inclusive, and say which box you measured.** MyMail's mark is stroke-only, so its
  raw geometry bbox **understates** what a person sees by 8.3 points; MyCal's and MyNotes' are
  fill-dominant, so for them geometry ≈ ink. **Comparing a stroke-only mark's geometry bbox
  against a filled mark's is not comparing like with like** (mymail-dev). Any figure reported
  against this rule must name which box it is.
- **A floor, not an equality.** MyCal's mark contains a real `<text>` element (§6.2), so its
  extent is a per-platform reading. An equality rule would be unfalsifiable across fonts; a floor
  survives.

> **Why the floor is 85% and not the weakest shipped value, which would be 91.67%.**
> `spec/sidebar-footer.md` §5.1 sets its hover-fill floor *at* the worst shipped figure, so a
> reader will otherwise read 85 as sloppiness. The distinguishing fact is what the operand is:
> that contract's is a colour the app owns and can hold still. **MyMail's mark is a vendored third-party
> drawing** — `lucide-1.25.0.js` — and icon sets get redrawn between versions. A floor at the
> shipped extreme would put MyMail in violation on a routine bundle upgrade that trimmed the
> envelope by two points, for a reason nobody performing that upgrade would think to check.
>
> That would be **manufacturing** an `AGENTS.md` §3.3 dormant defect rather than recording one:
> harmless today, conditional on something outside the repository not moving, with the condition
> written nowhere. 85% still fails MyNotes' 34.4% by fifty points, and nothing between 85 and
> 91.67 is a difference anyone can see next to a 93.75. *(Ruling: mysuite-manager, #517.)*
>
> **This floor has never been tested against a third independent mark.** It is derived from two
> shipped apps and applied to three, which is `AGENTS.md` §3.2's shape. It is the defensible
> direction only because MyNotes is being *built to* it rather than described by it.

### 3.4 The gap to the app-name label

**8px**, between the badge's trailing edge and the label's leading edge. Absolute `px`, invariant
across viewport, theme, root font size and content volume in both shipped apps.

**It is a property of the container in both**, reached by two independent rules — MyCal's
`.brand { gap: 8px }` and MyMail's `.sidebar-header { gap: 8px }`. Pinning it therefore
constrains a rule that also positions the out-of-scope label. That is deliberate: the human's
exclusion is about the label's **size**, and 8px of gap makes no label bigger (§2).

> **The 8px is load-bearing in a second place, and this is the note for whoever next touches
> it.** mynotes-dev's fit arithmetic — the 36px cost that drove the human's widening ruling
> (§10.1) — assumes a 28px badge **plus this 8px gap**, placed inside the brand anchor. Changing
> the gap changes the width MyNotes was widened to.

---

## 4. Placement: top left, in reading order — and **not** window coordinates

> **The badge sits at the top left of the app's own chrome, ahead of the app-name label in
> reading order.**
>
> **Its distance from the window's edges is deliberately not pinned.** Coordinates recorded
> below are **readings, not pins.**

This is the one place this contract is weaker than `spec/sidebar-footer.md` §8, which pins
(L, B) = (8, 8) from the *window*. That contract can do so because its two controls sit in the
same structure in all three apps. **These badges do not**: MyCal's is in a top bar, MyMail's and
MyNotes' are in a sidebar header. A coordinate rule would order a layout change in at least one
app, which a contract may not do (`AGENTS.md` §2.2, and `spec/sidebar-footer.md` §6.4's precedent
of declining exactly this for the sidebar column).

**The human's instruction specifies a placement** — *"the app logo **in top left**"* (§2) — so
silence would say less than was asked for. A contract that cannot be violated by a logo in the
bottom right is not this contract.

**Reading order, not geometry**, because that survives MyMail's label being a bare text node with
no selector, and it is checkable in the markup by anyone without a rendered page or a stated root
font size. All three satisfy it today: each brand block is the first child of its header or bar,
and the badge is first within it.

### 4.1 Why a coordinate rule is not merely unavailable but **false**

Recorded so nobody proposes one later believing it was an oversight. All three reports found
this independently:

| | Finding |
|---|---|
| **MyCal** | badge `y` is **not a constant**. `.top-bar` is `align-items: center` with `min-height: 40px`, and its height is set by the `<h1>` date heading **wrapping**. Measured `y` = 14 / 27.609 / 44.406 / **61.219** across viewport widths; it differs **per view** (Year and Month 14; Week, Day and Schedule 27.609) and therefore **per date and per locale**. At a 24px root it is 19.188 |
| **MyCal** | the **demo build** — the artefact GitHub Pages serves — moves it **non-monotonically**: `y` = 14 at 1920, 27.609 at 1440, back to 14 at 1439 |
| **MyCal** | badge is `display: none` below 600px (§9.3) |
| **MyCal** | Month view at 600 events, scrolled to the bottom: badge `y` = **−2206** |
| **MyMail** | 40 folders, scrolled to the bottom: badge `y` = **−1008** |

*"Any contract clause of the form 'the badge sits at (16, 14)' is false in MyCal today"* —
mycal-dev, for most widths, three of five views, a 24px root, and any scrolled page.

**Recorded readings at rest**, 16px root, either theme, at a wide viewport — **not pins**:

| | Badge top-left, viewport coordinates |
|---|---|
| MyCal | (16, 14) — and only while the heading fits on one line |
| MyMail | (16, 14) — invariant across all 17 widths tested, 1920 down to 280 |
| MyNotes | *pending* |

That the two shipped apps agree at rest is a coincidence of two unrelated rules — MyCal's `.app`
padding plus a 40px bar, MyMail's `.sidebar-header { padding: 14px 16px 12px }`. **It is not a
shared mechanism and must not be written up as one.**

---

## 5. Mechanism: local. The observable result is the contract.

**Which layer sizes the glyph is each app's own choice**, and the two shipped apps differ:

| | Glyph sized by | Mark source |
|---|---|---|
| MyCal | **CSS** — `.brand-logo svg { width: 17px; height: 17px }`. The SVG carries no `width`/`height` attributes | hand-written `Logo.tsx`, deliberately **not** in the Lucide bundle |
| MyMail | **SVG attributes** written by `<Icon size={17}>`. MyMail has **no CSS rule anywhere that sizes an SVG** | vendored Lucide `mail` |

**Neither is mandated, and forcing either would make things worse** — endorsed independently by
both app agents for the same reason. Sizing MyMail's glyph in CSS would create a second source of
truth beside `size={17}`, and CSS would win silently, so the next `size=` edit would become a
no-op. Putting attributes on MyCal's SVG would break the favicon parity it deliberately maintains
(§6.3). Neither buys an observable difference.

**MyCal's rule that its `Logo.tsx` must not be routed through the Lucide bundle is MyCal-local**
and is not promoted here. Nothing in the reports justifies making it a three-app rule.

**What *is* mandated in mechanism terms is the opposite of a technique:** the **badge is shared
and the mark is not** (§6). *(Formulation owed to mymail-dev.)*

> **The shared box is currently held together by a comment, not by this document.** MyCal's
> `.brand-logo` rule says *"Box, radius and glyph size are MyMail's `.logo-icon` verbatim"*. That
> copy **is** the contract today, undocumented, and one edit on either side from being lost.
> Replacing that with this file is the point of writing it.

---

## 6. The mark is per-app, and the drawing parameters differ

**The badge is shared; the picture inside it is each app's identity and must not be unified.**
Three apps sharing one glyph would defeat the purpose of a logo.

### 6.1 The drawing parameters are per-app and demonstrably differ today

Recorded so that nobody later "unifies" them believing they were meant to match:

| | viewBox | Construction | Rendered stroke |
|---|---|---|---|
| MyCal | `0 0 32 32` | 4 rects (1 stroked, 3 filled) + a `<text>` | **1.0625px** (2 units × 17/32) |
| MyMail | `0 0 24 24` | 2 stroke-only paths, `round` caps and joins | **1.4167px** (2 units × 17/24) |
| MyNotes | `0 0 32 32` | fill-only path, nothing stroked | **n/a — nothing is stroked** |

Both "stroke-width: 2"s are in different coordinate systems and **are not the same line on
screen.** This is a consequence of the marks being different pictures, not evidence of drift.
Measured off the live `getScreenCTM()` in both apps, not derived from the attributes.

### 6.2 MyCal's mark is platform-dependent; the other two are not

`Logo.tsx` draws a real `<text font-family="Arial,sans-serif">8</text>`. Arial is absent on the
measuring machine, so it renders in **DejaVu Sans Bold** (named via CDP `getPlatformFontsForNode`
— mycal-dev) and would differ where Arial exists.

**So no claim of the form "the marks render identically on any machine" is available**, and any
such clause would be unfalsifiable for MyCal without naming a font. MyMail's Lucide paths and
MyNotes' filled path have no equivalent exposure — **MyNotes' glyph numbers are constants rather
than readings, the only one of the three for which that is true.**

**Guidance, not a rule:** prefer paths over a rendered `<text>` element in a new mark. MyNotes
independently arrived there. This is not binding, because a rule banning `<text>` would
retroactively put MyCal out of contract on a document that is supposed to describe what MyCal
already ships.

### 6.3 Favicon parity is per-app, and two of three have it

| | Badge ↔ favicon |
|---|---|
| MyCal | **shared geometry by design** — identical rects and `<text>` placement, verified; differs only in the body rect's fill and `currentColor` vs a hard-coded blue |
| MyMail | **unrelated drawings** — a 32-unit stroked polyline favicon against a 24-unit Lucide badge |
| MyNotes | **the favicon already *is* the badge** — a `#2563eb` rounded square with a white "N" |

Not mandated in either direction. Recorded because MyCal's `Logo.tsx` carries a standing local
rule that changes to one belong in the other, and because MyNotes inherits the same relationship
for free. **One consequence worth knowing: MyCal's favicon is fixed blue and does not respond to
the theme; only the badge inverts.**

---

## 7. Colour and contrast

### 7.1 Resolved values and local names

| Role | Light | Dark | MyCal | MyMail | MyNotes |
|---|---|---|---|---|---|
| Badge fill | `#2563eb` | `#3b82f6` | `--primary` | `--sidebar-badge` → `--primary` | `--primary` |
| Glyph ink | `#ffffff` | `#ffffff` | literal `#fff` | literal `#fff` | *pending* |

**The glyph ink is a hard-coded literal in both shipped apps, not a token.** Recorded because a
clause naming a token for it would describe neither app. MyCal declares `color: #fff` 18 times in
its stylesheet, so this is the house pattern rather than an outlier.

> **MyMail has a tidy-up hazard here.** It owns `--on-color-fg: #ffffff`, and its own
> `.settings-badge` already uses it on the same fill — so *"tidy `.logo-icon`'s `#fff` to
> `var(--on-color-fg)` like its neighbour"* is an inviting edit that **changes nothing today**,
> because that token is defined once in `:root` and never theme-scoped. It becomes a silent
> divergence the day someone scopes it. `AGENTS.md` §3.3's shape, with the condition now written
> down. *(Found by mymail-dev.)*

### 7.2 Contrast — recorded, and no threshold binds

| | Light | Dark |
|---|---|---|
| Glyph `#ffffff` on the badge fill | **5.169:1** | **3.678:1** |

Confirmed independently by all three agents. **The strongest evidence is mymail-dev's**, which
counted actual painted pixels from an 8× element screenshot — ~42 000 pixels of the exact fill
and thousands of pure `#ffffff` — rather than computing from declared tokens.

**No contrast threshold attaches to the glyph**, and the figures are recorded so that the
omission reads as a decision rather than an oversight (the shape `spec/sidebar-footer.md` §5.5
uses for the control border):

- The badge is **decorative** (§8) — `aria-hidden`, no accessible name — so WCAG 1.4.11's 3:1 for
  graphical objects does not attach. It clears 3:1 in both themes regardless.
- **1.4.3's 4.5:1 does not apply**, including to MyCal's `<text>` "8". That criterion exempts
  text that is part of a logo or brand name outright, which disposes of the question of whether
  the "8" counts as text.

> **Do not "fix" 3.678:1 by touching `--primary`.** It is an operand of at least four other
> things, and only one of them is written down anywhere — see §7.3.

### 7.3 `--primary` is a cross-contract operand — the coupling nobody will look for

**A change to `--primary` made for the logo lands on `spec/sidebar-footer.md` §6.2's focus
indicator**, which is a **WCAG 1.4.11 obligation with under one point of headroom**:

| | Focus outline vs its backdrop | Margin over the required 3:1 |
|---|---|---|
| MyMail | **3.991:1** | 0.991 |
| MyNotes | **3.991:1** | 0.991 |
| MyCal | 4.823:1 | 1.823 |

In MyCal and MyNotes the badge fill and the focus outline are **the same token**. MyMail has an
alias layer (`--sidebar-badge`), which does not decouple the value today but could later without
touching the other two. In MyMail the same token additionally fills `.folder-badge` and
`.settings-badge`.

This is `spec/measurement-protocol.md`'s *"what has to be re-measured is set by the operands, not
by the topic"* — arriving **across two contracts**, which is the first recorded instance of that
in this repository. Anyone changing `--primary` in any app must re-derive
`spec/sidebar-footer.md` §6.2 for that app, and this section is here so that the search is
possible at all.

### 7.4 The backdrop behind the badge is per-app, and must be walked

| | Light | Dark | Painter |
|---|---|---|---|
| MyCal | `#f3f4f6` | `#111827` | **`<body>`** — neither `.brand` nor `.top-bar` paints |
| MyMail | `#ffffff` | `#1f2937` | `.sidebar` — `.sidebar-header` is transparent |
| MyNotes | `#f9fafb` | `#1f2937` | `.sidebar` — `.sidebar-header` is transparent |

**Obtain this by walking ancestors from the badge to the first one that actually paints**, per
`spec/measurement-protocol.md`. Never read one element's own `backgroundColor`.

> **These figures are identical to `spec/sidebar-footer.md` §5.3's footer backdrops, and all
> three agents were warned off them as a suspected copy. All three walked the ancestors and found
> the coincidence is real** — and the reason differs per app, which is exactly why the method
> matters:
>
> - **MyNotes and MyMail:** the header and the footer are both transparent children of the same
>   `.sidebar`, so it is genuinely one painter and one colour.
> - **MyCal:** **different painters, identical colours.** The footer paints its own opaque
>   `--bg`; the badge falls through to `<body>`, which paints the same `--bg`.
>
> So in MyCal a figure copied from the footer contract is **numerically right by coincidence of
> palette and methodologically wrong** — `spec/sidebar-footer.md` §3.1's shape, undetectable from
> inside that app. **Do not copy a backdrop figure between the two contracts. Walk it.**
> *(mycal-dev ran both walks on the same page to establish this.)*

---

## 8. Accessibility: the badge is decorative, and the condition for that

> **The badge carries no accessible name and contributes nothing to the accessibility tree. Its
> SVG is `aria-hidden="true"`. The app's identity is carried by the visible app-name label beside
> it.**

Verified in both shipped apps: MyCal's badge is a `<span>` with no `role`, `aria-label` or
`title`, whose whole `.brand` subtree yields an aria snapshot of exactly `text: MyCal` plus the
Reload button; MyMail's is a `<div>`, not focusable, not inside a link or button, with
`aria-hidden` on the SVG.

> **The condition, which is the part that ages** (`AGENTS.md` §3.3). The badge is decorative
> **because** an adjacent visible app-name text node carries the identity. **That element's
> appearance is out of scope (§2), but this contract depends on its existence.** If an app ever
> removes the visible label — the icon-only variant `spec/sidebar-footer.md` §7 considered and
> rejected for the footer — **the badge acquires a naming obligation** and this ruling stops
> holding.

**MyNotes is structurally different and it is ruled, not inherited.** Its brand is
`<a class="brand sidebar-brand" href="/">MyNotes</a>` — a **link with an accessible name**, where
MyCal's and MyMail's are static text.

> **The badge goes *inside* that anchor.** It keeps the link's accessible name "MyNotes" intact,
> keeps the badge decorative, and matches the convention that the whole brand block is the way
> home. A decorative sibling outside the anchor would leave the badge as the only part of the
> brand that is not the link.
>
> **Implementer's note, MyNotes-only — verify it, do not reason about it.** The badge is now
> inside a link, so anything the anchor applies to its descendants applies to it:
> `text-decoration` on hover, a `color` transition, a hover background. None must paint on the
> badge, whose fill and glyph ink this contract pins. mynotes-dev measured the current state —
> both shapes, both themes, hovered and unhovered, with the hover **asserted to have actually
> taken** — and found the anchor paints nothing onto a descendant badge, because `.brand` sets
> `color` and `text-decoration` explicitly and no `.brand:hover` or global `a:hover` rule exists.
> **The risk is latent, not absent:** an ordinary `.brand:hover { color: var(--link) }` added
> later would repaint the glyph through `currentColor`, silently. This is a good candidate for a
> MyNotes-local assertion, and it applies to **no other app**.

---

## 9. Known gaps and open items

Stated honestly. None is a reason to hold up work; all are reasons not to be surprised.

### 9.1 The badge scrolls off the window under content overflow — in both shipped apps

| | Condition | Badge `y` | The footer beside it |
|---|---|---|---|
| MyCal | Month view, 600 events, scrolled to bottom | **−2206** | holds 8 |
| MyMail | 40 folders, scrolled to bottom | **−1008** | holds 8.23 |

**This violates nothing in this contract**, which pins appearance and placement rather than
coordinates (§4). It is recorded because of the shape:
`spec/sidebar-footer.md` §8.2 and §8.3 identify this exact failure, and rescued the footer from
it with `position: sticky` and an opaque background. **Nothing ever specified the header, so
nothing rescued it.** The footer's rescue makes the header's exposure look deliberate, and it is
not.

**With the human as an open item.** Fixing it is real work in an app repo — sticky plus an opaque
background, with the stacking-context and clearance checks `spec/sidebar-footer.md` §8.3 lists —
and it is not this contract's to order.

### 9.2 The badge is `px` and the label is `rem` — a decision, with its cost recorded

The badge does not grow with the reader's browser font; the label does.

| Badge height ÷ label line box | 16px root | 24px root |
|---|---|---|
| MyCal | 1.061 | **0.707** |
| MyMail | 1.061 | **0.707** |

mymail-dev rendered both and looked: at 16px the mark *"reads as a proper badge anchoring the
row"*; at 24px it *"reads as undersized — the label dominates and the mark looks like an
afterthought."*

**Pinned as `px` deliberately**, for two reasons. Moving to `rem` would change two working apps'
rendered appearance, which is outside "add a logo to MyNotes and write down the pattern" and is
the human's call to open. And the two shipped apps degrade **identically** — 1.061 and 0.707 to
three decimals — so this is a **suite-wide design property, not a divergence**; the contract's
purpose is satisfied at every root size.

**Open design item, owner decision.** Recorded with its numbers so anyone who wants it revisited
does not have to re-derive them. Note the tension: **the badge is the `px` island inside a `rem`
column** *(mymail-dev's phrase)* — MyMail's column carries a comment recording that `px` was
rejected *there* for WCAG 1.4.4 reasons.

### 9.3 MyCal hides the badge below 600px — a sanctioned exemption, not a licence

`@media (max-width: 600px)` sets `.brand-logo, .brand-name { display: none }`.

**Sanctioned, with MyCal's own stated reason:** there is no room for the mark and the label, and
Reload rides in the same block and must stay reachable. Same shape as
`spec/sidebar-footer.md` §10.8's narrow-layout exemption.

**This is MyCal's, and it is not a general licence.** MyMail has no width breakpoint at all (its
one media query is `(hover: none)`); MyNotes has none in any served stylesheet. **An app
proposing to hide the badge needs its own reason recorded here** — an appeal to this precedent is
not one. For MyNotes it would additionally mean introducing its first viewport media query.

### 9.4 Nothing anywhere tests any of this

Swept by all three agents across their own repos:

- **MyCal:** exactly one assertion touches the badge —
  `e2e/tests/calendar-views.spec.ts:12`, `expect(page.locator('.brand-logo svg')).toBeVisible()`.
  It is satisfied by any non-empty box, so it cannot distinguish 12px from 17px from 22px.
- **MyMail:** the entire repository contains **two** references to the logo — the markup line and
  the CSS rule. Its e2e suite mentions neither `.logo-icon` nor `.sidebar-header`.
- **MyNotes:** no coverage of the sidebar header at all.
- **`tools/check-contract.py`** does not know the logo exists.

So every "what catches this?" answer in the reports is **"nothing"**, and that is from a coverage
sweep rather than from a demonstrated red run — no agent mutation-tested, because the discovery
phase was read-only.

**A check is deliberately deferred** until MyNotes lands, because a three-repo guard can only
report `CANNOT CHECK` before then, and an artefact whose one reachable path nobody has exercised
is the state `AGENTS.md` §3 records going wrong. When it is built, **note this asymmetry**: a
CSS-reading check can defend the badge box, radius and fill in all three, and the **glyph size in
MyCal only**, because MyMail sizes its glyph in a TSX prop no CSS reader can see. That limit must
be **printed on every terminating path**, verified by running each, not by reading it.

### 9.5 Smaller things worth knowing

- **`getByText('8')` matches MyCal's logo.** Its mark draws a real `<text>8</text>`, so
  `.brand-logo`'s `textContent` is `"8"` and an exact-text locator matches three elements on the
  default page, one being the logo. It is hidden from the accessibility tree but not from the
  DOM. *(mycal-dev.)*
- **MyCal's demo build is a second shipped surface** with different badge geometry (§4.1), and it
  is what GitHub Pages publishes.
- **`--app-padding-x` moves MyCal's badge and cannot move its footer**, which cancels that exact
  token with a negative margin. A token the footer contract is immune to and the logo is not.
- **`spec/sidebar-footer.md` §6.4's "~229px of slack" is the sidebar *footer* row**, and is false
  of the **header** row, which has 6.02px and goes negative at a 20px root. Same app, same
  sidebar, opposite conclusion — `AGENTS.md` §3.2 arriving *inside* one app rather than across
  three. Annotated there.

---

## 10. MyNotes

**Not yet implemented.** MyNotes ships no badge: its brand is a bare text anchor (§1).

### 10.1 A 28px badge does not fit today, and the human has ruled how to make room

mynotes-dev measured the top-left budget on the default Notes tab, 16px root, and it is
**15.63px** against a **36px** cost (28px badge + the 8px gap of §3.4) — **short by 20.4px**, and
**width-invariant**: MyNotes has no breakpoint, so a badge that does not fit at 1280 does not fit
at 375 either.

**It fails silently, which is the part to know.** `.sidebar-tabs` is `flex: 1; min-width: 0` with
no `overflow`, so under pressure the tabs shrink and **paint over** the action buttons: nothing
moves, nothing overflows its box, nothing clips, no console error.

> **The obvious fit check cannot see it.** Comparing the actions' right edge against the header's
> right edge returns **0 overflow at every root and every badge size, including the visibly
> broken ones.** The checks that do see it are `tabs.scrollWidth > tabs.clientWidth` and a
> last-tab-vs-actions element-overlap test. **If a fit assertion is ever written, it must be one
> of those two** — a right-edge check would pass MyNotes forever.
> `spec/measurement-protocol.md`'s *"the gap read as the answer"*, with a fresh specimen.

**The human's ruling: widen the sidebar** (relayed by mysuite-manager, #516), choosing it over
fixing the header overflow properly, trimming tab padding, or moving the tabs to their own row.

**This contract does not pin any app's sidebar width**, and `spec/sidebar-footer.md` §6.4 states
that the containing column is not part of *that* contract either, that the three widths "were
never unified — 200 / 220 / 420 are deliberately different". So widening is an **app-local
change**, not a contract amendment.

### 10.2 A pre-existing defect in the same pixels, not caused by this work

**MyNotes' header row already overflows at a 20px root with no badge present** — the tab strip
paints over the action buttons at +58px, and at 24px at +131.58px. 20px is Chrome's own "Large"
setting, so this is a **shipped WCAG 1.4.4 Resize Text failure**.

Recorded because any work here inherits it, and because "make the badge fit" and "fix the 20px
overflow" may be the same edit. It is not this contract's to fix.

### 10.3 What MyNotes will implement

Settled and available to build against:

- **The mark exists and does not need drawing.** `web/static/favicon.svg` is already a `#2563eb`
  rounded square with a white "N" — the badge the other two build in CSS, MyNotes has as a file.
  Take MyCal's route: inline SVG sharing geometry with the favicon, dropping the background rect
  (the CSS box paints the fill) and switching `fill="#fff"` to `currentColor`. **Not the Lucide
  route**, even though MyNotes vendors the full set with no allowlist and could take it for free —
  a Lucide glyph would make its badge and its favicon two different pictures.
- **The mark must be adjusted to meet §3.3.** As it stands the "N" fills 31% of its viewBox, so
  reusing it unchanged renders it at about a third of MyCal's apparent size. Tighten the viewBox
  or redraw to fill, and keep the favicon in sync.
- **The badge goes inside the brand anchor**, per §8, with the implementer's note there.
- **`.sidebar-brand` will need its own flex context** (`display: flex; align-items: center;
  gap: 8px`) to sit a badge beside the text inside the anchor. That is a change to the label's
  **rule** but not to its **typography** — font-size, weight and colour are untouched, measured
  identical in both shapes — so it is consistent with §2's exclusion.

---

## 11. Rules considered and not adopted

Listed so nobody re-derives them from a message or an old draft
(`spec/README.md`'s requirement, and `spec/sidebar-footer.md` §11's habit).

| Considered | Replaced by | Why |
|---|---|---|
| Same window coordinates for the badge, as `spec/sidebar-footer.md` §8 does for the footer | §4's placement rule | Not merely unavailable — **false in MyCal today** at most widths, three of five views, a 24px root and any scrolled page (§4.1) |
| "Position deliberately unspecified" | §4's placement rule | Says less than the human's instruction, which specifies *"in top left"*. Approved once and reversed on reading the primary (§12) |
| A mandated glyph mechanism — CSS sizing, or the Lucide bundle, for all three | §5, mechanism local | Would create a second source of truth in MyMail, or break MyCal's favicon parity, and buys no observable difference |
| A rule of the form "a 17×17 glyph, stroke-width 2, centred" | §3.2 plus §6.1 | Reads as a shared drawing convention. There is none — the two "stroke-width: 2"s render at 1.0625px and 1.4167px |
| An extent floor at the weakest shipped value, 91.67% | §3.3's floor of 85% | Would manufacture a dormant defect: MyMail's mark is vendored and a routine Lucide upgrade could breach a contract MyMail did not change |
| Banning `<text>` in a mark | §6.2, guidance only | Would retroactively put MyCal out of contract on a document describing what MyCal ships |
| Moving the badge to `rem` | §9.2, pinned `px` | Changes two working apps' appearance; outside this task and the human's call to open |

---

## 12. On how this document was produced

Two conclusions in it were **changed by reading a primary source rather than a relay**, and both
were conclusions held confidently:

- **"Position deliberately unspecified"** was approved and then reversed on reading the human's
  actual sentence, which says *"in top left"* (§4).
- **The label exclusion's condition** — *"since space there is crowded"* — was in the same
  sentence and would have been written as a bare "for now" without it (§2).

Also worth recording, because it is the pattern `AGENTS.md` §3.2 predicts: **two of the four
expectations in the original task brief were wrong on contact with the source** — the badge fill
token, and a claim that all three apps draw an `aria-hidden` SVG when MyNotes draws no SVG at all.
Both were corrected by verifying rather than adopting, which is what the brief asked for.

And the reports corrected **me**: my badge-versus-backdrop contrast figures were computed against
each app's *footer* backdrop, which is the wrong operand for this contract, and they coincide with
`spec/sidebar-footer.md` §6.2's to three decimals because it is the same colour pair. They looked
already checked. §7.4 is what replaced them.
