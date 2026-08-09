# App-name label — the text beside the badge

**Status:** binding on all three apps. **All three conform on every mandated value,
measured** — same declared font stack, same `1.1rem`, same resting placement, to the last
bit — and they did so *before* this contract existed.

> **Read this before the corrections below, or you will think you are reading about a
> broken suite.** The owner's instruction was *"I believe this is the case now … but let's
> make sure it stays that way."* **It is the case.** The three labels agree on the declared
> stack, on `1.1rem` / 17.6px, on `600`, on `x = 52`, on the 8px gap, and on their vertical
> placement including the way it changes with the root font size (§4.1). **This document is
> a guard against future drift, not a change request. Nothing in it asks any app to move a
> pixel.**
>
> What this work *did* uncover is a defect in the badge contract next door, in one app —
> `spec/app-logo.md` §4.4, corrected separately. It surfaced here because its operand is
> this contract's `font-size` (§6.3). It is not a defect in the labels.

**Scope: font, font size and placement.** Those three, because those three are what the
owner asked for. Weight, colour, letter-spacing and the rest are **recorded in §5 and
deliberately not mandated** — read §5 before concluding they were forgotten.

**Written from** the three apps' shipped code, which is the ground truth wherever it and
a document disagree (`AGENTS.md` §4), as measured and reported by the three app agents:

- **mynotes-dev-b**, message #619 — MyNotes at `d68c1c5`, clean tree, 60/60 served
  assets byte-identical to disk.
- **mycal-dev**, message #621 — MyCal at `42f2a66`, clean tree, both `app.css` and
  `app.js` served-vs-disk verified.
- **mymail-dev**, message #622 — MyMail at `e024e1d`, clean tree, 40/40 assets verified
  in each of four server sessions.
- **mynotes-dev-b**, message #625 — the flex-item box, and the asymmetric leading measured
  on both sides rather than assumed (§6.1).
- **mymail-dev**, message to this agent dated 2026-08-09 — the before/after sweep for
  `spec/app-logo.md` §4.4's remedy, which established that the remedy **does not move this
  contract's values** (§6.3).
- **mysuite-manager-brand-name**, message #618 and its subsequent relays in the same
  thread — the task brief, the owner's instruction quoted in full (§2), and the owner's
  rulings on placement, the narrow-layout exemption and enforcement (§4.3, §4.4, §7).

**I read the full text of #619, #621 and #622**, not summaries of them. Two conclusions
in this document contradict what the relaying summary said, and both are noted where they
occur (§4.1, and §0's note on the residue) — which is the reason the full text was read.

**If you find a ruling cited here that is not in that list, it was not available when this
was written — get it and check this document against it** (`AGENTS.md` §3.1).

At the time of writing, each app repo's `main` is level with its `origin/main` by its
local refs; no fetch was performed to confirm that against the remote.

Every number below is marked **[measured]** (read off a rendered page by the named agent)
or **[constant]** (an authored literal, quoted from source and also confirmed rendered).
Where a figure is a per-platform reading it says so and says what it was read on.

---

## 1. What this covers, and where

The app-name text beside the logo badge, in each app's top-left brand block.

| | MyCal | MyMail | MyNotes |
|---|---|---|---|
| Label | `.brand-name` (`<span>`) | **no element — a bare text node** | **no element — a bare text node** |
| Text | `MyCal` | `MyMail` | `MyNotes` |
| The row that holds it | `.brand` (`<div>`) | `.sidebar-header` (`<div>`) | `.brand.sidebar-brand` (`<a href="/">`) |
| Declares `font-size` / `font-weight` | `.brand`, `app.css:249-250` | `.sidebar-header`, `app.css:216-217` | `.brand`, `app.css:40-41` |
| Declares the font stack | `body`, `app.css:159` | `html, body`, `app.css:166` | `body`, `app.css:16` |
| Markup | `web/ts/app.tsx:443` | `web/ts/layout/Sidebar.tsx:99` | `web/ts/app.tsx:188` |

**Two of the three have no element for the label, and this contract does not ask them to
grow one.** What is mandated is the resolved value on the label, never a selector
(`AGENTS.md` §2.3). See §6.1 for how to measure a label that has no box of its own, and
§8.4 for why requiring an element would make things worse.

**In all three, the typography is declared on the *row* and reaches the label by
inheritance.** Not one of the three declares `font-size` on the label itself; MyCal has a
`.brand-name` rule and all four of its declarations are about overflow, none typographic.
That parallel is real and it is what makes §7's check possible — but it is a fact about
today's implementations, not a requirement. An app that declared the size on the label
would conform.

---

## 2. The owner's instruction, and the ruling it reopened

**The instruction, quoted in full** (relayed by mysuite-manager-brand-name, message #618):

> "Add a UI rule in mysuite that the brand name label to the right of the logo should have
> the same font, font size and placement across the three apps. I believe this is the case
> now after latest change to MyNotes, but let's make sure it stays that way."

Two things in that sentence shape this document:

- **"the same font, font size and placement"** — three properties, named. This contract
  mandates those and records the neighbours (§5) rather than quietly widening.
- **"let's make sure it stays that way"** — the deliverable is a **guard**, not a
  description. §7 is that guard, and §7.3 says plainly which part of the instruction no
  guard covers.

### 2.1 This supersedes `spec/app-logo.md` §2, by the same owner

`spec/app-logo.md` §2 records a ruling by this owner that put this label **out of scope**,
because MyNotes' label was smaller (16px against the siblings' 17.6px) and MyNotes'
top-left was crowded. That ruling was **conditional**, and the condition was written down
with it: *"for now, since space there is crowded."*

**The condition has been met and the owner has reopened it.** MyNotes widened its sidebar
column to carry the larger label (`mynotes` `d68c1c5`), which spent the crowding, and then
set the label at the siblings' `1.1rem`. So this is the documented path being followed,
not a contract being overridden.

`spec/app-logo.md` §2 keeps the original ruling, its condition and its measured 1.6px gap
as history, with the supersession recorded there — per `spec/README.md`'s requirement that
withdrawn rules stay readable *"so that nobody re-derives a superseded rule from an old
comment."* See §9 here for the withdrawal in this document's own terms.

> **The condition is why this was cheap.** Had §2 recorded a bare *"out of scope for now"*,
> nobody could have told whether the deferral had expired. It recorded *what would make it
> expire*, so the owner could see that it had. That is `AGENTS.md` §3.3 paying for itself,
> and it is worth copying rather than admiring.

---

## 3. The mandated values

Resolved values, measured on rendered pages by the three app agents. Token names, class
names and the number of hops to reach a value are per-project and are **never** what is
mandated (`AGENTS.md` §2.3).

### 3.1 Font — the declared stack, and only the declared stack

> **All three labels resolve the same `font-family` string:**
> `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`

**[measured]** — the computed value on the label, in all three, at every root size, theme,
viewport width and content volume any agent tried.

**"The same font" means the same declared stack — the same request made of the platform.
It does not and cannot mean the same rendered face.** `system-ui` resolves per machine by
definition. All three measuring sandboxes resolved it to a **monospace** face, and
mymail-dev established that this is the sandbox and not the apps: the box has no
`/etc/fonts`, fontconfig cannot load a default config, and `IIIIII`, `WWWWWW` and `MyMail`
all measure 60px in the authored stack. MyNotes' repo separately records that GitHub's CI
runner resolves `system-ui` about **1.25× wider** than the local machine
(`mynotes/web/static/app.css:132-134`), which is a fourth, independent, much older witness.

Three consequences, and they are binding:

- **No label width, no baseline offset and no text-box height may be pinned by this
  contract.** Every such figure in the three reports is a reading taken through one broken
  fontconfig and is not transferable.
- **A clause of the form "the three labels render in the same font" is unfalsifiable
  without naming a face**, and this contract does not make one. Same shape as
  `spec/app-logo.md` §6.2, which reached the identical conclusion about MyCal's `<text>`
  mark.
- **The quote style is not part of the value.** MyCal and MyMail write `'Segoe UI'`,
  MyNotes writes `"Segoe UI"`. Identical computed, identical rendered, and a check that
  compares source text must normalise quotes or it reports a difference no browser can
  see.

**The stack is authored on `body` in all three and nowhere nearer the label** — `mycal`
`app.css:159`, `mymail` `app.css:166`, `mynotes` `app.css:16`. mycal-dev confirmed the
origin rather than assuming it by walking the chain and finding `html` still on the UA
default (`"Times New Roman"`), which is the witness that `body` is where it enters.

> **So the mandated value lives in a rule about the whole application.** Editing `body`'s
> font stack in any of the three is a change to this contract, and it will not look like
> one. §8.1 lists it as the first silent breakage for exactly that reason.

### 3.2 Font size — `1.1rem`, computing to 17.6px at a 16px root

> **The label computes to 17.6px at the default 16px root font size, from a `1.1rem`
> declaration, and it must scale with the root.**

**[measured]** in all three, and **[constant]** in the sense that it is an exact multiple
of the root:

| | 16px root | 20px | 24px | 32px | Declared |
|---|---|---|---|---|---|
| MyCal | **17.6px** | — | — | **35.2px** | `.brand { font-size: 1.1rem }` |
| MyMail | **17.6px** | 22px | 26.4px | **35.2px** | `.sidebar-header { font-size: 1.1rem }` |
| MyNotes | **17.6px** | 22px | 26.4px | **35.2px** | `.brand { font-size: 1.1rem }` |

**The second root is what makes this a claim about `rem` rather than about 17.6.** All
three agents measured at two roots deliberately: at 16px alone, a `px` declaration and a
`rem` declaration are the same reading.

**"It must scale with the root" is not a widening of the owner's instruction — it is what
the instruction requires.** *"The same font size across the three apps"* is satisfied at a
16px root by any three declarations that compute to 17.6px. It is satisfied at **every**
root only if all three scale the same way. An app converting to `17.6px` would agree with
its siblings at the default root and disagree at every other, which is the divergence this
repository exists to prevent, arriving invisibly.

> **This is the `0.80rem` class of value** (`spec/sidebar-footer.md` §9.2): `1.1rem` →
> `1.10rem` is identical computed *and* identical serialised, and `1.1rem` → `17.6px` is
> identical computed at the root every test runs at. **No rendering test in any of the
> three apps can see either edit.** §7.1 is the only thing that can, and §8.1 says what
> else it cannot see.

### 3.3 Placement — what is pinned

**At rest**, meaning: default route, unscrolled, and no documented narrow-layout exemption
in force (§4.4). The same definition `spec/app-logo.md` §4 uses, and for the same reason.

> **The label's leading edge sits 8px from the badge's trailing edge, the badge precedes
> the label in DOM and reading order, and the two share one flex line.**

- **The 8px gap is `spec/app-logo.md` §3.4's value and is not restated here.** That
  contract already pins it; measured 8.000 in all three, invariant across root size,
  viewport width, theme and content volume in every run any agent made. Restating it here
  would recreate the duplication this repository exists to remove (`AGENTS.md` §4).
- **The label's distance from the window's left edge is 52px at rest at a 16px root, and
  it is entailed rather than independently pinned.** `16` (the badge's own x, pinned by
  `spec/app-logo.md` §4) + `28` (the badge's width, `spec/app-logo.md` §3.1) + `8` (the
  gap, `spec/app-logo.md` §3.4). **[measured]** as exactly `52` in all three, root-invariant
  because all three terms are `px`.

  **Check it as a consequence, not as a fourth pin.** If 52 is ever wrong, one of the three
  contracts above is being violated and that is where the defect is. And note that **the
  16 has a different owner in each app** — `--app-padding-x` on `.app` in MyCal,
  `.sidebar-header`'s padding in MyMail, `.sidebar-header`'s margin in MyNotes. Same
  number, three mechanisms, none of them mandated.

**The vertical relationship is §4.3 and is not yet ruled on.**

---

## 4. Placement: the mechanism, and what it costs

### 4.1 The label's vertical position is a remainder in all three apps

This is the finding that shaped the rest of this section, and it was demonstrated by
mutation in all three repos rather than argued.

All three brand rows are `display: flex; align-items: center`. In MyCal and MyNotes the
*badge* opts out with `align-self: flex-start`; in MyMail neither child opts out. So the
row's height is `max(28px badge, label line box, anything else in the row)` and whichever
box is shorter is centred in the leftover — i.e. **is a remainder**.

The label's line box is `font-size × line-height` = `1.1rem × 1.5` = **`1.65 × root`**, so
it out-measures the 28px badge above a root of **28 ÷ 1.65 = 16.97px**.

> **The label is vertically centred in a row whose top edge is `y = 14` and whose height is
> the row's tallest item.**
>
> **Tolerance: ±0.02px.** See below — the rule is exact, and the arithmetic is not.

**[measured]** on the label's **flex-item box** (§6.1), at a 16px root:

| | label `y` at a 16px root | above ~17px root | Source |
|---|---|---|---|
| MyCal | **14.796875** | flat **14** | mycal-dev, 7 roots |
| MyMail | **14.797** | flat **14.000** | mymail-dev, 6 roots, label *and* badge |
| MyNotes | **14.796875** | — | mynotes-dev-b |

> **Below the crossover the badge is fixed and the label is the remainder. Above it the
> label is fixed and the badge is the remainder. The two elements swap which one moves.**

At a 32px root all three labels sit at **14** with a 52.8px line box against a 28px badge —
**top-aligned with the badge and 24px taller than it.** So the offset **vanishes** above the
crossover rather than growing.

> **Which is why the rule is not "the label is centred on the badge".** That formulation is
> true only while the badge is the taller of the two, i.e. below a ~17px root — and it was
> proposed, checked against the three datasets, and withdrawn before it entered this
> document (§9). It would have been a rationale true of the case its author had in mind,
> in a repository whose neighbouring contract has one (`AGENTS.md` §3.2).

**"The row's tallest item" is deliberate and is not the same as `max(28px, label line
box)`.** Those two are equal in all three apps today and required by none: **MyCal's and
MyMail's rows also contain a Reload button**, which §4.2 shows can become the tallest item
and move the label 14px. MyNotes' anchor holds only the badge and the text. So —

> **The operands: the 28px badge (`spec/app-logo.md` §3.1), the label's own line box
> (`1.65 × root`, from §3.2's `1.1rem` × the inherited `line-height: 1.5`), and in MyCal and
> MyMail the Reload button. The rule holds while nothing else in the row is taller.**

That is the condition a future reader can check (`AGENTS.md` §3.3), rather than a promise
nothing defends.

### 4.1.1 Why the tolerance exists, and why the closed form is not the value

The centring term at a 16px root is `(28 − 26.390625) / 2 = 0.8046875`, which is `51.5/64`
— **unrepresentable** in Chromium's 1/64px `LayoutUnit`. It lands on `51/64 = 0.796875`, so
the page reports `14.796875` where the arithmetic says `14.8046875`. The difference is
exactly **1/128px**, and it appears **only where the centring term is nonzero**: above the
crossover the term is zero and the prediction is exact at every root measured.

**So the closed form is the right explanation and the wrong number.** Verified across
**14 root-size readings** in the three apps — MyCal at 16 / 18 / 18.67 / 19 / 20 / 24 / 32,
MyMail's label and badge at 16 / 17 / 18 / 20 / 24 / 32, MyNotes at 16 — all fitting within
1/128.

- **Pin the measured value or a tolerance, never the expression.** A `toBe(14.8046875)`
  fails on every shipped page; a `toBeCloseTo(…, 1)` passes on all three.
- The 1/64 `LayoutUnit` account is **an explanation offered, not a measurement**.
  mynotes-dev-b named it and stated explicitly that Chromium's rounding rule was not
  verified; it is carried here on the same footing. What *is* measured is the 1/128
  difference and that it appears in all three apps identically.

**One more precision, because it is the number a reader expects and it is not the number
the box has:** the flex-item height is **26.390625**, while `getComputedStyle` reports
`line-height: 26.4px`. Used layout value against computed value. *(Surfaced by
mynotes-dev-b.)*

**Two things follow that a drafter would otherwise get wrong:**

- **The label does not ride along at 14.** `spec/app-logo.md` §4 pins the badge at
  `(16, 14)`; the label sits at **14.797** at the default root — at the one root everybody
  uses. Anyone extending that rule to the label by assumption would pin the wrong number.
- **A test at a large root would find the label perfectly aligned.** MyCal's offset is
  nonzero *only* at the default root and exact above ~17px. mycal-dev's sentence, kept
  verbatim because the inversion is the point: *"a test at a large root would find MyCal's
  label perfectly aligned and would be measuring the one case where the defect is
  absent."* **Any assertion written against this must include a 16px root**, and a
  multi-root sweep that omits 16 is worse than none.

> **State the mechanism, quote the measurement.** `14 + (28 − lineBox)/2` gives
> **14.8047**; all three measure **14.797**, a 1/128px difference from the engine's
> LayoutUnit snapping. The formula is the right explanation and the wrong number. This
> document quotes what was measured.

### 4.2 A demonstrated, unguarded path by which one app's label drifts alone

**Not a possibility. Measured, in MyCal, at `42f2a66`:**

| state | `.brand` height | label `y` | badge `y` |
|---|---|---|---|
| as shipped | 28 | **14.796875** | 14 |
| `.brand-reload-btn { padding: 20px }` | 56 | **28.796875** | 14 |

**Padding an unrelated button moves the label 14px and the badge not at all, with nothing
red anywhere.** The Reload button has no relationship to the label.

**MyCal and MyMail have a Reload button inside the brand row; MyNotes does not** — its
Reload lives in `.sidebar-header`, outside the `.sidebar-brand` anchor, whose only children
are the badge and the text node. **So two apps carry a third operand that the third does
not.** It does not bind today, and it is the path by which one app's label could move while
the other two hold.

> **MyCal's own stylesheet already documents these levers — as a counterfactual for the
> badge.** `mycal/web/static/app.css:279-288` says padding Reload or growing the label's
> line-height *would* move the mark, and it is accurate, because `.brand-logo` then opted
> out of the centring. **Nobody wrote down that the same two levers move the label today,
> for real.** *(Found by mycal-dev in its own repo.)*
>
> That is a shape worth naming, because it is not quite `AGENTS.md` §3.3 and not quite
> §3.2: **a repository documented a hazard for the element it went on to protect, and the
> unprotected element beside it inherited the hazard without the note.** The comment is
> correct. Its neighbour is uncovered, and the correctness of the comment is part of why
> nobody looked.

### 4.3 The ruling: constrain the observable, name the operands

> **The owner's ruling: the vertical relationship is *recorded*, not *mandated*. No app
> adds a declaration and no app's label moves.**

So §4.1's rule states what must be observably true and §4.1's operand list is the thing a
future reader checks. **This contract does not extend `spec/app-logo.md` §4.2's *authored,
not arrived at* to the label.**

**The alternative and its price, so the decision stays legible.** Mandating authorship
would cost one declaration per app and would move the label **~0.8px at the default root in
all three, identically** — a visible change to three working apps, bought to defend a value
that is currently correct everywhere. That is the same trade `spec/app-logo.md` §9.2
declined for the `px`/`rem` question, and it was declined here for the same reason.

**Why this is not simply a weaker rule than the badge's.** `spec/app-logo.md` §4.2 exists
because the badge's offset was a remainder of **something unrelated** — MyCal's date
heading wrapping, MyNotes' tab-strip typography. The label's offset is a remainder of the
row's **own** contents. A remainder of your own operands is a different and weaker defect
than a remainder of a stranger's.

> **With one exception, and it is why §4.2 is a section rather than a footnote.** MyCal's
> and MyMail's Reload buttons *are* strangers, in the row, unguarded. That case is the
> §4.2 shape exactly, and recording it is the price of not mandating.

### 4.4 MyCal hides the label below 600px — a sanctioned exemption

> **The owner's ruling: MyCal may hide the label below 600px, as it hides the badge. This
> contract binds above 600px. No app changes.**

Same shape as `spec/app-logo.md` §9.3 for the badge and `spec/sidebar-footer.md` §10.8 for
the footer — and, as there, **this is MyCal's exemption and not a general licence.** An app
proposing to hide its label needs its own reason recorded here; an appeal to this precedent
is not one.

The facts:

`mycal/web/static/app.css:1660-1663`, inside `@media (max-width: 600px)`:
`.brand-logo, .brand-name { display: none }`. **[measured]** by mycal-dev with a
596→606px sweep in 1px steps: both flip at the same pixel, **because they are one rule
with two selectors** and cannot be separated without splitting the list.

**MyMail and MyNotes have no width breakpoint at all.** Both agents established this from
the served CSSOM rather than by grep — MyMail's only media conditions anywhere in the page
are `(hover: none)` and a vendored `(pointer: coarse)`; MyNotes' document carries no
`CSSMediaRule` whatever, so adding one would be its first.

`spec/app-logo.md` §9.3 records this exemption **as being about the badge**. It hides the
label too, and that is now recorded in both places rather than in neither.

**For MyNotes specifically, hiding the label would mean introducing its first viewport
media query** — the same note `spec/app-logo.md` §9.3 makes about the badge, and it is
still true.

### 4.5 At rest is a real qualifier — the label scrolls off with the badge

**[measured]**, under content overflow with the overflow asserted rather than assumed:

| | condition | badge `y` | label `y` |
|---|---|---|---|
| MyCal | Month view, 620 events, scrolled to bottom | −1852 | **−1851.203** |
| MyMail | 67 folders, scrolled to bottom | −1776.000 | **−1775.203** |

The 0.797 offset is preserved all the way out of the window. This is the same recorded
departure as `spec/app-logo.md` §9.1 — the header is not sticky where the footer is — and
it applies to the label verbatim. **Recorded, not fixed**: fixing it is real work in an app
repo and it is that contract's open item, not this one's.

---

## 5. Recorded, deliberately not mandated

The owner named font, font size and placement. These are the neighbouring values, written
down so that their absence from §3 reads as a decision rather than an oversight — the shape
`spec/app-logo.md` §7.2 uses for the contrast figures.

| | Value | Where it comes from | Why not mandated |
|---|---|---|---|
| `font-weight` | **600** in all three **[measured]** | authored on the row: `mycal:250` · `mymail:217` · `mynotes:41` | Not in the instruction. It already agrees; pinning it would widen scope by one property with no evidence of risk. **And the rendered claim would be weaker than it looks** — all three agents' resolved face reports as `-Regular` against a computed 600, so the weight may be synthesised. True of the declarations, unverified of the faces |
| `color` | light `rgb(31,41,55)`, dark `rgb(243,244,246)` in all three **[measured]** | `--text` / `--text-primary` / `--fg` | Not in the instruction. Agrees today. See §8.3 — MyNotes has a live hazard here that no sibling can catch |
| `line-height` | `1.5`, unitless, inherited from `body` in all three | `mycal:162` · `mymail:167` · `mynotes:19` | **See §6.3 — this one is not a free omission and is handled deliberately** |
| `letter-spacing`, `font-style`, `text-transform`, `font-stretch`, `font-variant`, `word-spacing`, `text-indent` | the CSS initial value in all three **[measured]** | nothing declares any of them, anywhere on any of the three chains | They agree **by not being set**. A clause mandating `text-transform: none` would pin something no app's rule says, and would convert three absences into three declarations somebody then has to maintain |

**That last row is worth reading twice.** The three agree on seven properties because no
one has ever written them down. That is the same footing `spec/app-logo.md` §2 recorded for
MyNotes' old font size — *smaller because it never set a size, rather than because it set a
smaller one* — and it is a genuinely different kind of agreement from the ones in §3.

---

## 6. Mechanism: local. Two things that are not.

**How each app reaches the mandated values is its own choice**, and the three already
differ: the row is a `<div>` in MyCal and MyMail and an `<a>` in MyNotes; the label is a
`<span>` in MyCal and a bare text node in the other two; the 16px term in §3.3's `x` has
three different owners. None of that is mandated and none of it should be harmonised.

Three things are not free choices.

### 6.1 How to measure a label that has no box

**Read the computed values from the element the label text actually inherits from,
resolved at runtime, and record which element that was.**

Two of three apps have no element for the label, so an assertion keyed to a selector
measures a *different element* in two apps and cannot say so. `mynotes/e2e/tests/logo.spec.ts:85-96`
is the pattern this contract asks for: it finds the text node, takes
`textNode.parentElement`, and returns **`labelFound`** (so a missing node fails rather than
falling back) and **`labelParentIsAnchor`** (so the assumption breaks loudly if an app
later wraps the text in a `<span>`).

**For geometry, name the box.** A bare text node has two, and they are not
interchangeable:

- the **ink box**, from a `Range` over the text node — its height and its offset within the
  line box are the resolved face's ascent and descent, so it is **face-dependent and its
  numbers are not transferable** (§3.1);
- the **flex-item box**, from a temporary layout-neutral wrapper — this is the line box,
  `1.65 × root`, **pure layout and machine-independent**.

**Pin the flex-item box; report both.** The wrapper is layout-neutral and that was
measured, not assumed: mymail-dev recorded Δx = Δy = Δw = Δh = **0.0000** across 68 runs
and again after unwrapping, and mynotes-dev-b the same. **Assert the neutrality on every
run** — a probe that changes what it measures is the failure `spec/measurement-protocol.md`
exists to prevent.

> **`spec/app-logo.md` §3.3 already requires every figure reported against it to name which
> box it is.** This is the same rule, arriving on a second axis. It is one lesson, not two,
> and it has now cost something twice: once when a `getBBox()` width was quoted under a
> stroke-inclusive heading, and once here, when a text box and a block box 2px apart were
> nearly tabulated as a 2px divergence between two apps that in fact agree exactly.

### 6.2 The leading is asymmetric, and assuming otherwise nearly cost a false finding

**Measured on both sides in two apps independently**, at a 16px root: the ink box sits
**2.000000** below the flex-item box's top and **2.390625** above its bottom, inside a
26.390625px line box. A symmetric half-leading would be **2.1953125**. It is not symmetric.

This is recorded because of what nearly happened without it. Three reports gave the label's
`y`; one of them measured the ink box because its app has no element, and the other two the
block box. Converting between them with the symmetric estimate put two apps **0.2px apart**
and produced a divergence to investigate. **There was none** — MyCal had reported *both*
boxes for one element, so the real top gap was measurable rather than estimable, and backing
out 2.000 gave the other app's figure to the last bit. mynotes-dev-b then measured its
flex-item box directly and confirmed it: **14.796875 in all three.**

> **Two independent errors agreeing is not corroboration, and neither is one estimate
> agreeing with itself.** The 0.2px was the estimate. What resolved it was a report that
> named both of its boxes — which is the whole of the rule in §6.1, arriving as the reason
> for it rather than as advice.

### 6.3 `line-height` is an operand of a *different* contract, and that is why it is left local

This contract does not mandate `line-height`. But leaving it unmentioned would hide
something, so:

The label's line box — `font-size × line-height` — is what displaces the **badge** above a
~17px root, in any app whose badge does not opt out of the row's centring. **So pinning the
label's `font-size` does not pin the badge's `y`; it pins where `spec/app-logo.md` §4's
crossover falls, per app, as a function of that app's inherited `line-height`.**

**The remedy belongs to `spec/app-logo.md`, not here**, and it is one declaration:
`align-self: flex-start` on the badge, which MyCal (`app.css:289`) and MyNotes
(`app.css:98`) already carried and which MyMail was missing. With it the badge's `y` is
independent of the label's line box, and `line-height` stops being an operand of anything
in that contract.

**MyMail has now added it, and the measurement that matters here is that this contract's
values did not move.** mymail-dev swept before and after at 16 / 17 / 20 / 24 / 32px roots:
the badge goes from `14.000 / 14.016 / 16.500 / 19.797 / 26.391` to a flat **14.000**, while
the **label's flex-item box, its ink box, the 8px gap and the header's own height are
identical at every root, on both boxes.** Re-running the full 68-run matrix, 44 runs came
back byte-identical and the 24 that differed **differed only in the badge's `y`**.

> **That is the fact this section needed and could not assume**: the fix to the neighbouring
> contract is free with respect to this one. Had it moved the label, the two contracts would
> have been in direct conflict and one of them would have had to give.

**And the remedy needs one `align-self` in MyMail where MyCal and MyNotes each need two** —
MyMail's badge and label are direct children of the same flex row, so there is no
intermediate brand block with its own centring to escape. *(mymail-dev.)* A useful check on
any future claim that "all three need two".

> **One edit helps one contract and breaks the other, and it is the likeliest edit on the
> list.** Adding `line-height: 1` to MyMail's `.sidebar-header` — the standard idiom for a
> header row, and `.sidebar-reload-btn` 70 lines below already has it — would **freeze that
> app's badge at 14 at every root**, accidentally satisfying `spec/app-logo.md` §4.2, **and
> move its label from 14.797 to 19.2**, breaking §4.1 here. *(Found by mymail-dev.)*
>
> Neither document can see that on its own. It is recorded in both.

---

## 7. The guard

`AGENTS.md` §2.5: if a number matters, put it in a test. This contract is guarded three
ways, and the third is *"by nothing, stated as such"*.

### 7.1 Cross-repo, static — `tools/check-contract.py`

**The only thing that compares the three apps.** It pins:

- **`font-size`, as declaration text.** `1.1rem` in all three, compared as source text.
  This is the class of edit no browser can see (§3.2), and it is the reason a static check
  earns its place here.
- **The font stack, normalised.** Compared as a resolved stack with quote style normalised
  (§3.1).

**The stack check is weaker than the size check and the script says so on the line, not in
a footer.** It reads `body`'s declaration; **the cascade between `body` and the label is not
checked**, and nothing in it says which face renders. `tools/check-contract.py`'s own caveat
block already concedes that the cascade is unverified — this contract inherits that limit
and states it rather than letting a green line imply more.

### 7.2 Per app, rendered

Each app asserts its own half, per §6.1's method, **including a 16px root** (§4.1).
`mynotes/e2e/tests/logo.spec.ts:288-295` is the template — and note that it currently
asserts `'17.6px'` at a 16px root **only**, which a `rem` → `px` conversion passes. A
rendered suite cannot hold §3.2 on its own; that is §7.1's job.

**Three per-app suites are not a cross-repo check** and adding more cannot make one
(`AGENTS.md` §2.5). All three run in CI, so each gates its own app's publication and none
of them can see a divergence.

### 7.3 Not guarded, and it cannot be

> **Placement is not checked by any script and no script can check it.** The label's
> position is not a declared value in any of the three apps — it is a flex remainder
> (§4.1). A static reader can see the ingredients and cannot compute the result. Rendered
> assertions can pin the result **per app**; nothing compares the three.
>
> **The rendered face is not checked and cannot be** (§3.1).

Stated here and printed by the checking script on every terminating path, because a green
run that stays silent about this implies coverage of a third of the owner's instruction
that does not exist (`AGENTS.md` §3, and `spec/README.md`'s registration list).

---

## 8. Known gaps and open items

Stated honestly. None is a reason to hold up work; all are reasons not to be surprised.

### 8.1 What breaks these values silently

Swept by all three agents in their own repos. Every item leaves the build green.

**All three apps:**

- **Editing `body`'s font stack.** It *is* the label's font (§3.1); nothing nearer declares
  one. A change made for body copy is a change to this contract and will not look like one.
- **Normalising `1.1rem`** — to `17.6px` (identical at a 16px root, frozen at every other)
  or to `1.1em` (identical today, divergent the moment an ancestor sets a size). §7.1 is
  the only guard that sees either.
- **Moving `font-size` / `font-weight` off the row onto the label**, or the reverse. Renders
  identically today. In MyCal it would silently drop the size from any second text child
  added to `.brand` later.

**MyCal** — `.brand`'s Reload button is in the row and moves the label (§4.2); the
`≤600px` rule hides the label as well as the badge (§4.4); deleting `.brand-name`'s
`min-width: 0` breaks the ellipsis without visibly failing until a longer name or a wider
face arrives.

**MyMail** — `line-height: 1` on `.sidebar-header` (§6.3, the sharpest one); its Reload
button shares the row (§4.2); its `font-weight: 600` sits beside a `--unread-weight: 600`
token that invites "tokenising"; its label is a bare text node, so wrapping it is free
geometrically (measured) but a class on the wrapper is not.

**MyNotes** — `a { color: var(--link) }` also matches its brand anchor and takes over the
moment `.brand`'s `color` is deleted as redundant (§8.3); `font-size` sits on `.brand` while
`.sidebar-brand` is a second rule on the same element, so folding them is inviting.

### 8.2 Coverage before this contract was written: almost none

- **MyCal:** three assertions touch the label — its text, that Reload sits after it, and
  that it is hidden below 600px. **Nothing typographic or geometric.**
- **MyMail:** nothing. Its e2e suite contains no brand, header or app-name locator at all.
- **MyNotes:** one assertion, `17.6px` / `600` at a 16px root — the only typographic
  assertion in the suite, and a `rem` → `px` change passes it.
- **`tools/check-contract.py`** did not know the label existed.

> **So the value the owner asked us to protect was, at the moment they asked, protected by
> one assertion in one app that could not see the likeliest way of breaking it.** Worth
> recording in that direction: this is the same finding `spec/app-logo.md` §9.4 makes about
> the badge, and the two were found independently by different agents in different repos.

### 8.3 MyNotes' brand is a link, and no sibling can catch what that costs

MyNotes' label lives inside `<a class="brand sidebar-brand">`. Two rules match it for
`color` — `.brand { color: var(--fg) }` and `a { color: var(--link) }` — and `.brand` wins
on specificity. **Deleting the `.brand` declaration as redundant hands the label to the
link colour**, silently.

Colour is not mandated by this contract (§5), so this is not a contract violation waiting
to happen — it is a divergence waiting to happen in a property the contract records.
**MyCal's and MyMail's labels are not inside links, so neither sibling's suite can ever
catch it.** This is a MyNotes-local assertion and it applies to no other app. *(Found by
mynotes-dev-b.)*

### 8.4 Requiring an element for the label would make things worse

Recorded because it is the obvious first move and it is wrong. Two of three apps have no
element; adding one is markup work in two repos for no observable change. Wrapping the text
is **geometrically free** — measured at Δ = 0.0000 across 68 runs in MyMail and again in
MyNotes — but it silently invalidates every assertion keyed to the row, which is exactly
what `labelParentIsAnchor` (§6.1) exists to detect. Mandating an element would order the
edit the probe was built to catch. `AGENTS.md` §2.3: the value is mandated, never the name.

### 8.5 Degradation under a long name differs, and is not mandated

Outside the owner's three words, so not specified — but recorded, because *"the same
placement"* invites a reader to assume the same behaviour when space runs out, and it is not
the same.

| | Behaviour **[measured]** |
|---|---|
| MyCal | ellipsizes — `min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis`, proven by substituting a long name |
| MyMail | no wrap, no truncation, no ellipsis; the Reload button is pushed out first, then the header overflows silently |
| MyNotes | no wrap, no truncation, no ellipsis; the **tab strip** is squeezed to zero width and paints over the action buttons, then the label clips edge-on |

Both MyMail's and MyNotes' failures are **silent** — nothing moves, nothing clips
visibly, no console error. If a label's text is ever changed or translated, this is the
cost, and two of three apps will not tell you.

### 8.6 Conformance cost MyNotes 76px of main pane

Recorded so it is not re-litigated as an unexplained number. MyNotes' column went
`420 → 456 → 464 → 540px`, and **the last step is this contract's**: the label moving from
`1rem` to `1.1rem`, plus tolerance, because GitHub's CI runner resolves `system-ui` about
1.25× wider than the local machine and the narrower column overflowed there while every
local run was green (`mynotes/web/static/app.css:122-134`).

**This contract does not pin any app's sidebar width** and `spec/sidebar-footer.md` §6.4
states the three widths were never unified. The widening is an **app-local change**, and it
is the recorded price of MyNotes conforming — not a value anyone should copy.

---

## 9. Rules considered and not adopted

Listed so nobody re-derives them from a message or an old draft (`spec/README.md`'s
requirement, and `spec/sidebar-footer.md` §11's habit).

| Considered | Replaced by | Why |
|---|---|---|
| **"The app-name label's typography is out of scope"** — `spec/app-logo.md` §2 | **This contract** | **Superseded by the owner, on the condition their own ruling attached.** The deferral was explicitly *"for now, since space there is crowded"*; MyNotes widened its column, which spent the crowding, and the owner reopened it. The ruling and its 1.6px measurement stay in `spec/app-logo.md` §2 as history |
| Mandating a selector or an element for the label | §1, §6.1, §8.4 | Two of three apps have no element; requiring one is markup work for no observable change and orders the edit `labelParentIsAnchor` exists to catch |
| Mandating `line-height` | §6.3 | Not in the owner's instruction, and in all three apps it is `body`'s — in MyMail, a rule about message bodies. The operand it threatens belongs to `spec/app-logo.md` §4, and the remedy there is one declaration on the badge |
| Mandating `font-weight`, `letter-spacing`, `text-transform` and the rest | §5 | Widens the instruction. The last group agrees **by not being set**, and pinning it would convert three absences into three declarations to maintain |
| Pinning the label's width, its baseline offset, or its text-box height | §3.1, §6.1 | Every such figure available is a reading through one broken fontconfig; CI already differs by ~1.25× |
| Pinning `x = 52` as an independent value | §3.3 | It is entailed by `spec/app-logo.md` §4 + §3.1 + §3.4. A fourth pin would restate three values this repository already holds elsewhere |
| Extending `spec/app-logo.md` §4's `(16, 14)` to the label | §4.1 | The label sits at **14.797** at the default root, not 14. It does not ride along |
| **"The label box is centred on the badge box"** | **§4.1's *centred in a row whose height is the row's tallest item*** | **False above a ~17px root**, where all three labels sit at 14 with a 52.8px line box against a 28px badge — top-aligned, and 24px taller. It was proposed as the placement rule, checked against 14 root-size readings in the three apps, and withdrawn before it was written. Recorded because it is *"a rationale true of the case its author had in mind"* (`AGENTS.md` §3.2) caught one step before publication, which is the only place that catching is cheap |
| Stating the label's `y` as `14 + (28 − lineBox)/2` | §4.1.1's measured `14.796875`, ±0.02 | The closed form gives **14.8046875** and every shipped page reports **14.796875**. Right explanation, wrong number |
| Mandating the vertical relationship (extending `spec/app-logo.md` §4.2's *authored, not arrived at* to the label) | §4.3, recorded not mandated | **Owner's ruling.** Would move the label ~0.8px in all three apps identically, to defend a value already correct everywhere |

---

## 10. History

- **2026-08-09** — Written. All three apps already conformed on every mandated value at
  `mycal 42f2a66` / `mymail e024e1d` / `mynotes d68c1c5`. Supersedes `spec/app-logo.md`
  §2's exclusion (§2.1). §4.3 and §4.4 open with the owner.
- **Found while writing:** `spec/app-logo.md` §4.4's claim that *"all three hold `y = 14`
  from a 16px root to a 32px root"* was **false for MyMail** above a ~16.97px root, and its
  *"the only one that never moved"* was false in the same range. Predicted from a source
  read, measured by mymail-dev at five roots two independent ways, and **fixed in the app**
  rather than by rewriting the claim to match the defect. The operand is this contract's
  `font-size`, which is why it surfaced here; the correction to that contract is a separate
  commit (§6.3).

  > **Worth keeping: the fix was chosen over the edit.** The cheaper move was to amend §4.4
  > to say MyMail drifts above ~17px. What was done instead was to give MyMail the
  > declaration its two siblings already carried, so the claim became **true** rather than
  > accurate-about-a-defect — and §4.4 records that it was false in the interim rather than
  > reading as though it had always held.
