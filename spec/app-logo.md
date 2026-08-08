# App logo — the badge in the top left

**Status:** binding. **§4's placement rule is newly added and no app conforms to it yet as
shipped** — MyCal and MyNotes are both being corrected to it, MyMail already satisfies it and is
the reference. Every other section is implemented and shipping in MyCal and MyMail, and
implemented and measured in MyNotes on an unmerged branch (§10). §4.4 is empty until the two
fixes are measured; it is not filled from either being written.

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
| Badge | `.brand-logo` (`<span>`) | `.logo-icon` (`<div>`) | `.brand-logo` (`<span>`), **inside the brand anchor** |
| Mark | `<Logo/>`, `web/ts/components/Logo.tsx` | `<Icon name="mail" size={17}/>` | `<Logo/>`, `web/ts/components/Logo.tsx` — the favicon "N", viewBox cropped (§6.3) |
| Container | `.brand`, in `<header class="top-bar">` | `.sidebar-header`, in `<nav class="sidebar">` | `.sidebar-header`, in `<aside class="sidebar">` |
| Stylesheet | `web/static/app.css` | `web/static/app.css` | `web/static/app.css` |
| Markup | `web/ts/app.tsx` | `web/ts/layout/Sidebar.tsx` | `web/ts/app.tsx` |
| App-name label **(out of scope, §2)** | `.brand-name` (`<span>`) | **no selector — a bare text node** | `.brand.sidebar-brand` (`<a href="/">`) |

**MyMail's label cell is not an omission.** Its app name is a bare text node inside
`.sidebar-header` with no element of its own, so there is nothing to name. Recorded explicitly
because a blank cell reads as "not looked up" (`AGENTS.md` §3.5).

The three sit in **structurally different containers** — MyCal's in a top bar spanning the
window, MyMail's and MyNotes' in a sidebar header. **That difference is not a defect and does not
excuse a difference in position**: §4 pins the same resting offsets in all three, reached by
whatever mechanism each container needs.

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
**different layers** (§5), and an author CSS rule always beats an SVG presentation attribute.

**That is not a theoretical gap — it is demonstrable in MyCal today.** Its SVG carries no size
attributes, so a checker reading attributes finds nothing; and if someone adds
`width="24" height="24"` to it, the attribute reads **24** while the glyph goes on rendering at
**17**, because `.brand-logo svg` still wins (measured — §5). **A check that reads an attribute
and calls it verified has checked nothing, and can report a number no user will ever see.**

### 3.3 The mark's extent inside the glyph box

> **The mark's rendered ink must span at least 85% of the glyph box on its larger axis.**
> The shorter axis is not constrained.

Measured **stroke/ink-inclusive**, not as a bare `getBBox()`. Shipped readings:

> **Do not reach for `getBBox({ stroke: true })` to get that.** Both mymail-dev and mycal-dev
> found, independently, that it **silently returns the plain geometry box** — no error, no
> warning, just a number that is wrong by the stroke width for any stroked mark. mymail-dev
> caught it because an identical result *cannot* be right for a 2-unit centred stroke; had the
> mark been fill-only it would have looked correct and been believed.
>
> *(A reading on Chromium 145 via Playwright 1.58.2, not a guarantee about the API — re-derive it
> rather than carrying it forward.)* **Count painted pixels instead**, or derive the
> stroke-inclusive box by hand and corroborate it against pixels, which is what both shipped
> figures below did. This is `spec/measurement-protocol.md`'s standing shape: the apparatus
> answering confidently, in the direction of a pass.


| | Larger axis, stroke/ink-inclusive | Construction | Source |
|---|---|---|---|
| MyCal | **93.75%** (pixel ink 88.24%) | mixed fill + stroke + `<text>` | mycal-dev |
| MyMail | **91.67%** (pixel ink 92.65%) | **stroke-only**, vendored Lucide 1.25.0 | mymail-dev |
| MyNotes | **91.67%** — reached by cropping the viewBox to `10 10 12 12`; **34.4%** uncropped | fill-only | mynotes-dev |

**Why this rule exists.** Without it the contract cannot see a difference of roughly 3× in
apparent size. Reusing MyNotes' favicon mark unchanged would put a **5.26 × 5.84px** mark inside
the same 17 × 17 box that holds MyCal's **~15px** one — passing every box measurement in §3.1 and
§3.2 while visibly failing "the three look like one product". *(Found by mynotes-dev before
implementing, which is the only reason it is a rule rather than a defect.)*

> **Those are rendered-ink figures, named as such deliberately.** The raw `getBBox()` widths for
> the same two marks are 30.9% and 87.5%, and quoting *those* beside the table above would mix
> two statistics that differ by 8.3 points for MyMail — which is the qualifier below, violated in
> the paragraph that explains it. **Every figure reported against this rule must say which box it
> is.**

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
> that contract's is a colour the app owns and can hold still. **MyMail's mark is a vendored
> third-party drawing** — `lucide-1.25.0.js` — and icon sets get redrawn between versions. A
> floor at the shipped extreme would put MyMail in violation on a routine bundle upgrade that
> trimmed the envelope by two points, for a reason nobody performing that upgrade would think
> to check.
>
> That would be **manufacturing** an `AGENTS.md` §3.3 dormant defect rather than recording one:
> harmless today, conditional on something outside the repository not moving, with the condition
> written nowhere. 85% still fails MyNotes' 34.4% by fifty points, and nothing between 85 and
> 91.67 is a difference anyone can see next to a 93.75. *(Ruling: mysuite-manager, #517.)*
>
> **This floor has now been tested against a third independent mark, and it held.** It was
> derived from two apps and applied to a third — `AGENTS.md` §3.2's shape, and the caveat that
> stood here while the outcome was unknown. MyNotes reached **91.67%** by cropping its viewBox
> to `10 10 12 12`: the same path data as its favicon, character for character, **with no
> distortion of the letterform**. So the floor did not force an ugly glyph, and it was cleared by
> the cheapest available means rather than by redrawing.
>
> The rule is now tested against three marks of three **different constructions** — mixed
> fill+stroke+text, stroke-only and vendored, and fill-only — which is a materially stronger
> position than one derived from two.
>
> **And there is evidence it does real work, which is rarer than a rule that merely holds.**
> mynotes-dev mutated its mark back to the uncropped `0 0 32 32` viewBox: the extent assertion
> went red at 34.4% **while every badge-box and glyph-box assertion stayed green.** That is
> precisely the blindness this section was invented for, demonstrated rather than argued.

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

## 4. Placement: (16, 14) from the window, at rest

> **At rest, the badge's top-left corner sits 16px from the window's left edge and 14px from its
> top, in all three apps, at the default 16px root font size.**
>
> **At rest** means: default route, unscrolled, and no documented narrow-layout exemption in
> force (§4.2).

Measured to the badge's border box with `getBoundingClientRect()` against the viewport — the same
frame `spec/sidebar-footer.md` §8 uses for the footer controls.

**The root size is named in the rule rather than assumed**, following that contract's §2.2, which
pins its acceptance height *"at the default 16px root font size"* for the same reason: the three
apps reach these offsets through different units, so they hold together at 16px and diverge above
it. §4.3 records that divergence with numbers rather than leaving it unstated.

**(16, 14) is not a new number.** It is what MyCal and MyMail already agreed on — see §4.1, which
is the reason this section exists at all.

### 4.1 The agreement was deliberate, and it lived in a CSS comment

`mycal/web/static/app.css`, verbatim, beside `.top-bar { min-height: 40px }`:

> *"40px puts the 28px badge's top edge at 8px (`.app` padding) + 6px = 14px — **the same offset
> MyMail's sidebar header gives its own badge via `padding-top: 14px`.** Without this the bar
> collapses to ~34px and the mark rides 3px higher than MyMail's."*

So 14 was **chosen**, with its arithmetic and its failure mode written down — and written down in
one repository's stylesheet, where the other two could not see it.

> **This is the defect this repository exists to prevent, arriving inside the contract meant to
> prevent it.** The two apps that knew about each other agreed. **The third had nothing to aim
> at**, because the agreement was a comment rather than a contract. MyNotes' offsets were not
> careless; they were unaimed.

**And this section previously made it worse.** It asserted that the agreement was *"a coincidence
of two unrelated rules … not a shared mechanism and must not be written up as one"* — which is
false, and which told anyone who noticed the misalignment that the question was malformed. That
paragraph is withdrawn (§11).

### 4.2 The position must be **authored**, not arrived at

> **An app satisfies §4 by declaring the offsets, not by happening to compute them.**

Both apps that missed (16, 14) missed it the same way, by different routes: **the badge's
position was a remainder of something unrelated.**

| | What produced the offset before the fix |
|---|---|
| **MyCal** | `y = 8 + (bar height − 28) / 2`, where the bar's height is `max(40px, tallest child)` — so the badge tracked the **date heading's wrapping**, and moved with viewport width, view, date and locale |
| **MyNotes** | `y` = 12px of `.sidebar` padding + `(38.61 − 28) / 2`, where 38.61 is set by **the tab strip's typography** — so the badge moved with `.sidebar-tab`'s font size and padding |
| **MyMail** | authored directly, as `padding: 14px 16px 12px`. **The only one that never moved.** |

Neither remainder was visible, neither had any assertion against it, and both moved the badge
when something with no relationship to the logo changed.

**This is why the rule is about authorship and not only about the number.** A position that is
computed satisfies the contract on the day it is measured and drifts afterwards with nothing red
— which is `spec/sidebar-footer.md` §3.1's class of defect (a value correct today for a reason
nothing defends) arriving on geometry instead of on a declaration.

### 4.3 Departures, recorded

Each of these is a **recorded exemption from §4, not evidence that §4 cannot exist** — which is
the distinction this section had wrong until the owner looked at the shipped result.

| Departure | App | Recorded |
|---|---|---|
| badge hidden entirely below 600px | MyCal | §9.3 |
| badge scrolls off under content overflow — `y` = −2206 / −1008 measured | MyCal, MyMail | §9.1 |
| the **demo build** — the artefact GitHub Pages serves — moved `y` **non-monotonically** with width: 14 at 1920, 27.609 at 1440, back to 14 at 1439 | MyCal | §9.5, and §4.2 is why |
| offsets diverge above a 16px root, because the three reach them through different units | MyNotes | §4.4 |

### 4.4 Conformance — **pending re-measurement**

> **The human has ruled that both outliers are fixed** rather than recorded as departures: MyCal's
> `y` becomes 14 unconditionally, and MyNotes' inset moves to 16px with its column widened to buy
> back the tab clearance that spends.
>
> **Both fixes are in flight, so this table is deliberately empty.** It is filled from measured
> readings when mycal-dev and mynotes-dev report, and not from either fix being written. The
> 24px-root figures land here too — MyNotes' `x` is fixed across roots by that change, and a small
> vertical remainder from the label's line box is **accepted** rather than fixed, on the same
> boundary §9.2 already drew for the badge's box.

The pre-fix readings, so the change is checkable against something: **MyMail (16, 14)** invariant
across 17 widths; **MyCal (16, 14)** at ≥1305px and **(16, 27.609)** at 1280 in three of five
views; **MyNotes (12, 17.297)**, invariant across width and scaling with the root font.

---

## 5. Mechanism: local. The observable result is the contract.

**Which layer sizes the glyph is each app's own choice**, and the two shipped apps differ:

| | Glyph sized by | Mark source |
|---|---|---|
| MyCal | **CSS** — `.brand-logo svg { width: 17px; height: 17px }`. The SVG carries no `width`/`height` attributes | hand-written `Logo.tsx`, deliberately **not** in the Lucide bundle |
| MyMail | **SVG attributes** written by `<Icon size={17}>`. MyMail has **no CSS rule anywhere that sizes an SVG** | vendored Lucide `mail` |

**Neither is mandated, and "harmonising" them would make things worse in both directions** —
endorsed independently by both app agents. The two hazards look opposite and are **one fact**:

> **An author CSS rule beats an SVG presentation attribute.** Presentation attributes carry
> specificity zero and sit at the start of the author origin, so *any* rule that matches wins.

| "Tidy" | What actually happens |
|---|---|
| Size **MyMail's** glyph in CSS, "to match MyCal" | The new rule wins and `size={17}` goes inert. The prop still reads 17, so the next `size=` edit is a **silent no-op** |
| Put `width`/`height` attributes on **MyCal's** SVG, "so it carries its own size" | **Nothing happens at all** — `.brand-logo svg` still wins. It looks like it worked, and it **arms** a breakage that fires later, when someone deletes the now-genuinely-redundant CSS rule |

**The MyCal row is measured, not reasoned.** mycal-dev set `width="24" height="24"` on the live
SVG and re-measured: **still 17 × 17**. Only after also deleting the `.brand-logo svg` rule from
the CSSOM did it become 24 × 24. So the hazard there is **delayed**, which is the worse kind —
the edit that arms it and the edit that fires it are months and authors apart, and neither looks
wrong on its own.

Neither buys an observable difference today, and both convert a single source of truth into two.

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
| Glyph ink | `#ffffff` | `#ffffff` | literal `#fff` | literal `#fff` | literal `#fff` |

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

**This is a recorded departure from §4, not a violation of it** (§4.3) — the resting rule binds
at rest, and this is what happens outside it. It is recorded because of the shape:
`spec/sidebar-footer.md` §8.2 and that contract's §8.3 identify this exact failure, and rescued
the footer from it with `position: sticky` and an opaque background. **Nothing ever specified
the header, so nothing rescued it.** The footer's rescue makes the header's exposure look
deliberate, and it is not.

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

### 9.4 Almost nothing tests any of this — and the one suite that does is not on a `main`

Swept by all three agents across their own repos:

- **MyCal:** exactly one assertion touches the badge —
  `e2e/tests/calendar-views.spec.ts:12`, `expect(page.locator('.brand-logo svg')).toBeVisible()`.
  It is satisfied by any non-empty box, so it cannot distinguish 12px from 17px from 22px.
- **MyMail:** the entire repository contains **two** references to the logo — the markup line and
  the CSS rule. Its e2e suite mentions neither `.logo-icon` nor `.sidebar-header`.
- **MyNotes:** **12 tests in `e2e/tests/logo.spec.ts`**, plus a `Logo.tsx` ↔ `favicon.svg` drift
  guard that runs on every build. Each accepted by a demonstrated red (§10.4). **On an unmerged
  branch**, so nothing runs it yet.
- **`tools/check-contract.py`** does not know the logo exists.

> **So the only real coverage of this contract belongs to the app that adopted it last, and does
> not execute anywhere.** The two apps this contract was *written from* have none. That is worth
> stating in that direction: a contract derived from two implementations ended up guarded only by
> the third, because the third is the only one that had a reason to write assertions while the
> rules were fresh.

One of MyNotes' mutations is the one to keep, because it is this contract's own §3.3 caught in
the act: reverting its mark to the uncropped `0 0 32 32` viewBox **failed 2 tests on the extent
assertion while every badge-box and glyph-box assertion stayed green.** That is exactly the
blindness §3.3 exists for, demonstrated rather than argued.

> **If a fit assertion is ever written, the instrument matters more than the threshold.**
> mynotes-dev swept MyNotes' column 380→760px in 1px steps and found the three candidates
> disagree *systematically*:
>
> | Instrument | Fires at | What it measures |
> |---|---|---|
> | last item vs the next element (**overlap**) | 441px | **whether it is visually broken** |
> | `scrollWidth > clientWidth` on the strip | 450px | stricter early warning, red one container-gap sooner |
> | right edge vs container | **never** | nothing — it reads clean zero in every broken case |
>
> The 9px gap between the first two is the header's own `gap`, and it scales with the root font
> (9 / 12 / 14px at 16 / 20 / 24px roots), because a strip can overflow into that gap before it
> reaches anything. **Use the overlap check for "is it broken"**; the strip check will report red
> on layouts a reader would call fine. **Never the right-edge check** — it is the one a person
> writes first and it cannot fail (§10.1).

**A check is deliberately deferred** until MyNotes lands, because a three-repo guard can only
report `CANNOT CHECK` before then, and an artefact whose one reachable path nobody has exercised
is the state `AGENTS.md` §3 records going wrong. When it is built, **note this asymmetry**: a
CSS-reading check can defend the badge box, radius and fill in all three, and the **glyph size in
MyCal only**, because MyMail sizes its glyph in a TSX prop no CSS reader can see. That limit must
be **printed on every terminating path**, verified by running each, not by reading it.

### 9.5 An empty badge satisfies every rule in §3 — MyMail only, with its condition

**Not a §3.3 amendment.** A rule of the form *"the mark must exist"* would be unfalsifiable
prose in a document whose other rules are measurements, and the extent floor already fails an
absent mark the moment anything measures ink. This is a **mechanism failure in one app with a
cross-app consequence**, which is a known gap, and one repo's prose is the wrong home for it.

MyMail's `<Icon>` **returns `null` for a name absent from the vendored bundle**
(`if (!nodes) return null`). So if `gen-lucide.mjs`'s `ICONS` list ever loses `'mail'`, the badge
becomes **an empty blue square and `./build.sh` stays green** — no error, no warning, nothing red.
An empty badge satisfies §3.1's box, radius and fill, §3.2's centring, and §4's placement. It
fails only §3.3, and only if something measures ink.

**The condition that makes it harmless today, written down because that is the whole point**
(`AGENTS.md` §3.3 — that file's, not this one's):

> `'mail'` is in `gen-lucide.mjs`'s `ICONS` list, and MyMail is the only app that reaches its
> mark through a bundle at all. MyCal and MyNotes hand-write their SVGs, so there is no lookup
> to miss.

So it is armed by exactly one edit — pruning that list, which is a routine size optimisation on
a vendored bundle — and it is invisible to every other guard. **If MyMail ever asserts anything
about this badge, assert that the glyph renders non-empty**, which is the cheapest form of §3.3's
floor and the only one that catches this. *(Found by mymail-dev; escalated here rather than left
in its repo, because the consequence is that the three stop matching.)*

### 9.6 Smaller things worth knowing

- **`getByText('8')` matches MyCal's logo.** Its mark draws a real `<text>8</text>`, so
  `.brand-logo`'s `textContent` is `"8"` and an exact-text locator matches three elements on the
  default page, one being the logo. It is hidden from the accessibility tree but not from the
  DOM. *(mycal-dev.)*
- **MyCal's demo build is a second shipped surface** with different badge geometry, and it is what
  GitHub Pages publishes. Its badge moved *non-monotonically* with viewport width (§4.3) — a
  second symptom of the same computed-position defect §4.2 names, and the fix pinning `y = 14`
  unconditionally should resolve it. **Verify it there too**, since it is a different build.
- **`--app-padding-x` moves MyCal's badge and cannot move its footer**, which cancels that exact
  token with a negative margin. A token the footer contract is immune to and the logo is not.
- **`spec/sidebar-footer.md` §6.4's "~229px of slack" is the sidebar *footer* row**, and is false
  of the **header** row, which has 6.02px and goes negative at a 20px root. Same app, same
  sidebar, opposite conclusion — `AGENTS.md` §3.2 arriving *inside* one app rather than across
  three. Annotated there.

---

## 10. MyNotes

**Implemented and measured, on an unmerged branch.** MyNotes' `main` still ships no badge and a
420px column; the work sits on a local `logo-badge` branch, unpushed. **No commit hash is
recorded here** — `spec/sidebar-footer.md` §11's rule is that a hash from an unpushed branch pays
the cost of perishability and buys nobody the ability to resolve it.

Every value in §3 was implemented and then **measured back** on a rendered page, and every one
agreed. Nothing in this section is a report that code was written; §10.4 lists what was read off
the page.

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

**Widen for the logo only** — the shortfall is **20.4px** (a 36px cost against a 15.63px budget),
not the ~+168px that would also absorb §10.2's pre-existing overflow. **And not at the measured
minimum:** a column
sitting exactly where the tabs stop overlapping is one label change, one font tweak or one
translated string from failing again, in the invisible mode above. Take the minimum, add
headroom, round to MyNotes' own spacing rhythm.

> **Nothing in `spec/sidebar-footer.md` is disturbed by this, and it was checked rather than
> assumed.** That contract pins its controls at (L, B) = (8, 8) from the **window** (its §8), and
> MyNotes' sidebar is flush to the window's left edge — so widening moves the right edge only and
> neither coordinate has a width term. That contract's full-bleed separator rule (its §8.5) is
> relational and MyNotes implements it by reading the sidebar's content width live. And that
> contract's §6.4 slack figure **grows** with the width, so the exemption it grants gets
> stronger, never weaker.
>
> The one thing that *does* break is a test, not a rule — see §10.3.

### 10.2 A pre-existing defect in the same pixels — out of scope, reported, still open

**MyNotes' header row already overflows at a 20px root with no badge present** — the tab strip
paints over the action buttons at +58px, and at 24px at +131.58px. 20px is Chrome's own "Large"
setting, so this is a **shipped WCAG 1.4.4 Resize Text failure**. *(Measured by mynotes-dev; its
report carries the full table, and nobody should re-derive it.)*

**It stays open, deliberately.** The human was offered fixing it as one of four options and
declined, choosing the widening instead. Buying it through width would cost about **+168px**
(420 → ~588) against the ~+20px the logo needs — and a `px` widen costs the main pane at *every*
root size, where the `rem` conversion `spec/sidebar-footer.md` §6.4 already rejected cost it only
at large ones. 588px permanently is a worse trade than the 630px-at-150%-text that its §6.4 turned
down.

So: **pre-existing, not caused by this work, not fixed by it, and reported to the human as a
standing item with its numbers.**

### 10.3 One assertion had to go before the widening — and why it was harmless until it wasn't

**Resolved: the assertion has been removed** (verified on the branch — what remains at that line
is a comment recording the removal, not the assertion). What follows is why it had to go, kept
because the mechanism generalises.

`../mynotes/e2e/tests/sidebar-footer.spec.ts` **used to assert**
`expect(column.width).toBeCloseTo(420, 0)`. **It pinned a value `spec/sidebar-footer.md` §6.4
states is not part of that contract**, inside the suite whose job is to hold that contract. It
was not a stale number; it was an assertion with no owner. The relational checks on the
neighbouring lines — the controls fitting inside the column, and (8, 8) — are what the contract
actually requires, and they survive any width.

**It was deleted rather than updated to the new number**, as this section directed. Re-pinning
would have re-armed the same trap at a different value. The right shape was already known in
that same file, which reads the sidebar's content width live rather than hard-coding it.

> **This had been wrong the whole time and had cost nothing, because nothing executed that
> suite.** That was the condition, and nobody had written it down. Then the branch was pushed and
> this repository recorded it — and between mynotes-dev's report and the human's ruling to widen
> that very column, **a wrong assertion in a file nobody ran became a publication gate.**
>
> **Nobody changed that line. What changed is what it costs.**
>
> The full statement of the pattern, including why the waking commit was in a *third* repository,
> is `AGENTS.md` §3.3. It is the first cross-repo specimen of it.

**And the prediction was checked by running, which is the point.** I predicted "2 of 18 tests"
from reading the file. mynotes-dev restored the assertion against the 456px column and ran it:
**exactly 2 failed, both on that assertion, nothing else** — so the blast radius was right. **The
denominator was not: the suite is 27 tests, not 18.** I had counted `test(` occurrences in a file
rather than running it, which counts what a pattern matches and not what a runner collects.

A wrong denominator is the harmless half of that mistake and it is worth naming anyway: **the
same reading would have produced a wrong "N of M" in either direction, and only the run can tell
you which half you got right.** The `documentElement.scrollWidth` check flagged here as a real
question was also verified rather than assumed — it passes at both 20px and 24px roots with the
wider column, because `.app-body`'s `overflow: hidden` absorbs it.

### 10.4 What MyNotes will implement

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
| **"The badge's distance from the window's edges is deliberately not pinned"** | **§4's (16, 14) at rest** | **Withdrawn on the owner's observation of the shipped result.** It answered *"can a coordinate be pinned that always holds?"* — thoroughly, and correctly. The question that mattered was *"do the three look alike when you open them?"*, and the two are not the same. A rule can be unavailable in general while the **resting** positions agree in the case every user sees |
| **"The two shipped apps agree at rest by coincidence … not a shared mechanism and must not be written up as one"** | **§4.1** | **False.** MyCal chose `min-height: 40px` specifically to land on MyMail's 14px and recorded the 3px it would otherwise miss by, in a comment in its own stylesheet. The second half of the sentence was right and the first was wrong — and together they told anyone who noticed the misalignment that the question was malformed. **A reader who finds that comment must not conclude the contract is confused: the comment is right and this document was wrong** |
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

- **The whole of §4 was rewritten a second time**, after the owner looked at the shipped result
  and reported that MyNotes' badge sat differently from the other two. The section had answered
  *"can a coordinate be pinned that always holds?"* so thoroughly that nobody asked *"do the
  three look alike when you open them?"* — and the evidence for the first answer actively
  discouraged the second question. **A rationale can be true in the general case and wrong about
  the common one**, and no amount of correct measurement inside the wrong question finds that.
  What found it was the owner opening three tabs.
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
