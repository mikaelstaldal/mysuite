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

**I read the full text of #619, #621 and #622**, not summaries of them. Two conclusions in
this document contradict what the relaying summary of those reports said, and both are noted
where they occur — the placement rule in §4.1, and the apparent 0.2px disagreement between two
apps in §6.2, which turned out not to exist. **That is the reason the full text was read**, and
it is `AGENTS.md` §3.1's argument arriving as a saving rather than as a cost.

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

> **This is the `0.80rem` class of value** (`spec/sidebar-footer.md` §9.2) — but the class has
> three members and they are not equally hidden. **State which, because both of the obvious
> summaries are false:**
>
> | Substitution | Rendering can see it? | The static check can see it? |
> |---|---|---|
> | `1.1rem` → `1.10rem` | **No.** Identical computed *and* identical serialised, at every root | Yes — it compares source text |
> | `1.1rem` → `17.6px` | **Yes, at a second root.** Identical at 16px, wrong at every other | Yes |
> | `1.1rem` → `1.1em` | **No, at any number of roots.** See §7.2 — in MyCal every ancestor of the row computes to the root size, so the two coincide everywhere | Yes |
>
> So a rendered suite must assert at **two roots** to earn the middle row, and can never earn
> the other two. And the static check reads the *row*, so it is beaten by a declaration nearer
> the label — closed for MyCal only (§7.1). **Neither mechanism is sufficient and neither is
> redundant**, which is the honest form of a claim this document twice tried to make as a
> superlative.

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

All three brand rows are `display: flex; align-items: center`, so the row's height is its
tallest item and whichever box is shorter is centred in the leftover — i.e. **is a
remainder**.

Whether the *badge* is exposed to that is `spec/app-logo.md` §4.2's business rather than this
contract's, and it differs per app: MyCal and MyNotes opt their badge out with
`align-self: flex-start`, and **MyMail's `main` does not** — that is `spec/app-logo.md` §4.4's
recorded defect, with its remedy on a branch (§6.3). **The label is exposed in all three, and
no app opts it out.**

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

### 4.1.1 Closed forms are explanations, not values — a rule for this whole document

> **Never write a placement figure in this document as an arithmetic expression, or as the
> number an arithmetic expression gives. Write what was measured, with a tolerance.** The
> expression belongs beside it as the *mechanism*, which is what tells the next reader which
> edit moves the figure — but it will not be the number on the page, and you cannot predict by
> how much or in which direction.

That is stated as a rule rather than as a note on one value because **two independent figures
in this document have already been written as closed forms first and corrected by measurement**
— one by this document's author, one by the manager relaying a report — and they are wrong in
*opposite* directions. The mechanism, and both specimens, follow.

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

> **This is a general rule about placement figures in this document, not an annotation on one
> value — there are two independent specimens and they disagree about the direction.**
>
> | Closed form | Term in 1/64ths | Measured | Direction |
> |---|---|---|---|
> | label `y`, 16px root: `14 + (28 − 26.390625)/2` = **14.8046875** | 51.5 | **14.796875** | **down** |
> | label `y` under `line-height: 1` in MyMail: `14 + (28 − 17.6)/2` = **19.2** | 332.8 | **19.203** | **up** |
>
> So you cannot predict even the *sign* of the error from the arithmetic, which is the practical
> reason the rule is "measure it" rather than "allow for rounding". **Anyone adding a placement
> figure to this document will reach for the closed form** — both of these were written that way
> first, one by this document's author and one by the manager relaying it, and both were caught
> by an app agent running the mutation instead of transcribing the number.

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

**And measured again in MyMail, rather than transferred from MyCal:**

| state | reload h | header h | label `y` | badge `y` |
|---|---|---|---|---|
| as shipped | 26 | 55 | **14.797** | 14 |
| `.sidebar-reload-btn { padding: 20px }` | 56 | 83 | **28.797** | **14** |

**14px in both apps — by coincidence of geometry, not by transfer**, since the two rows differ
in every other dimension. *(mymail-dev, who measured it after being asked only to name the
button as an operand. The stronger form of the finding is the one that cost an extra run.)*

**MyCal and MyMail have a Reload button inside the brand row; MyNotes does not** — its
Reload lives in `.sidebar-header`, outside the `.sidebar-brand` anchor, whose only children
are the badge and the text node. **So two apps carry a third operand that the third does
not, and their exposure is now measured in both rather than measured in one and assumed in
the other.** It does not bind today, and it is the path by which one app's label could move
while the other two hold.

> **Note what holds the badge still in MyMail's row above.** It is the `align-self: flex-start`
> that `spec/app-logo.md` §4.4's remedy adds. **Before it, that same mutation moved both.** So
> the badge's protection and the label's exposure are the same declaration seen from two sides.

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
>
> **Both halves of that have since been corrected in MyCal, and the correction is the useful
> part.** The comment also claimed deleting `.brand-logo`'s `align-self` *"moves the mark with
> nothing red"* — **no longer true**, since the badge test's 20/24px root loop catches it,
> verified by deleting the declaration and measuring `y = 16.5` at a 20px root. So one clause
> went stale by being *fixed*, and the clause beside it was never written at all. It now records
> both: the badge is guarded, **and the same two levers still move the label, unguarded, today.**

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
falling back) and a flag recording **whether the parent was the row itself** (so the
assumption breaks loudly if an app later wraps the text in a `<span>`).

> **Search the row's DESCENDANTS for the text node, not its direct children.** This is
> prescriptive, because the two searches are indistinguishable today and behave oppositely on
> the one edit the flag exists to catch. Wrapping the label in a `<span>` moves the text node
> out of the direct-children list, so a direct-children search fails on `labelFound` — **loud,
> but pointing at a disappearance that did not happen, and the "which element did these values
> come from" flag never fires at all.** The descendant search finds the node, reports the new
> parent, and fails on the flag with a message telling the reader what to re-derive.
>
> **§6.1 is the LOCAL HALF of the static guard, not a consolation for apps that lack one.**
> §7.1's `LABEL_ELEMENT` check catches a `font-size` added to MyCal's label element — the false
> green §10 records. **The rendered suite catches the same divergence, at 22.4px, and only
> because it follows this section**: a suite reading the row instead of the element the text
> actually inherits from would have reproduced the static check's blindness exactly.
>
> So in MyCal both halves independently catch one divergence by different means, and **neither is
> redundant**; in MyMail and MyNotes, whose labels have no element, this is the *only* half that
> exists. *(mycal-dev, whose per-tool table in §7 is what made the pairing visible.)*

> **What the descendant search actually buys is a CAPABILITY, not a better error message** —
> and that is the argument for the requirement. Wrap the label in
> `<span style="font-size: 1.4rem">` and, with a descendant search, **`labelFontSize` itself
> fails: 22.4px against an expected 17.6px**, because the wrapper becomes the host and its size
> is what gets read. **With a direct-children search that assertion is blind** — the host falls
> back to the row and reads a correct 17.6px.
>
> **So the descendant requirement converts the size assertion from blind to sighted for exactly
> the divergence §7.1 cannot see in MyMail and MyNotes**, whose labels have no element for the
> static check to inspect. It closes most of the gap the false green left those two apps with.
> *(Measured by mynotes-dev-b.)*
>
> **The diagnostics improve too**, which is how this was first noticed rather than why it
> matters: mymail-dev ran the wrap both ways and got 12 failures (all *"no label text node"*)
> against 6 (the first being the flag, with its re-derive message); mynotes-dev-b got 7 against
> 2. **Those two pairs are not comparable and only their shape is** — different suites,
> different mutations, different assertion counts. Quoted as two observations of one *direction*,
> never as two measurements of one quantity.

> **And the parent flag must be capable of being false — which is a SEPARATE property from the
> descendant search, and a suite can have the first without the second.**
>
> mynotes-dev-b added the flag the review asked for, mutation-tested it, and found it **true in
> every reachable state**: a node found by searching the row's direct children has the row as its
> parent *by construction*, and a node not found fell back to the row anyway. **It read as a
> guard and was a tautology.** What actually caught a wrap was `labelFound` — 7 red, four of them
> *badge* tests, pointing a reader at an element that was fine.
>
> They fixed the field rather than asserting it: a `TreeWalker` over the whole row, which
> separates *"there is no label"* from *"the label moved into a wrapper"*. Re-mutated: **2 red on
> the right assertion, with a message naming the cause, and badge geometry green.**
>
> **This field is load-bearing in exactly the two apps that cannot be covered any other way.**
> §7.1's static check reads the row, so in MyMail and MyNotes — whose labels have no element — a
> `<span>` carrying its own `font-size` passes every line the cross-repo check has. **A tautology
> here is the difference between a guard and the appearance of one.**
>
> So §6.1 requires three things, and they are independent: **search descendants**, **exclude the
> badge subtree**, and **make the parent field falsifiable**. Each was found by a different agent
> discovering that the obvious implementation passes while measuring the wrong thing.
>
> **Each of the three properties now has its own measured specimen, found in a different app by
> a different agent — and no app's fix would have caught either of the others:**
>
> | Property | What passes without it | Where measured |
> |---|---|---|
> | search **descendants** | a wrapped label reads a correct size off the row; the size assertion is blind | MyMail, MyNotes |
> | exclude the **badge subtree** | a deleted label falls through to the mark's own text and resolves a size off it | MyCal — its mark draws a real `<text>8</text>` |
> | **`labelFound`**, separate from the size assertions | a deleted label falls back to the row, whose computed size **is still 17.6px**, so size and weight both pass **on a page with no label at all** | MyMail |
>
> **The last two are the same failure with two different causes.** MyCal's fallback found a
> glyph's text; MyMail's found the row's own inherited size. Both produce a confident, correct-
> looking measurement of something that is not the label — *absent* read as *present*, which is
> the inverse of the failure `spec/measurement-protocol.md` usually warns about and just as quiet.
>
> **And MyMail's badge-subtree exclusion is inert today**: `.logo-icon.textContent` is `""`,
> its Lucide mark being two stroke-only paths. **They kept it anyway**, on the grounds that
> *"our mark contains no text"* is precisely the kind of condition that goes false without an edit
> to their file. That is `AGENTS.md` §3.3 used as a **design argument** rather than as a
> post-mortem, which is the rarer and better use of it.

> **The test of "falsifiable" is that three states are distinguishable**, and MyCal's suite
> demonstrates all three:
>
> | State | What must fail | What must NOT be reported |
> |---|---|---|
> | shipped | nothing | — |
> | label wrapped one level deeper | the parent field — *"label text now lives in `<SPAN>`"* | a disappearance; the node is still found |
> | label element deleted | the count — *"expected exactly one label text node, found 0"* | a wrapper; there is no host to name |
>
> **The field's name is local and is not part of this contract.** MyCal keys on the element
> (`hostIsBrandName`), MyNotes on the anchor (`labelParentIsAnchor`) — same property, two names,
> because the two apps' rows are different elements (`AGENTS.md` §2.3). Do not read either name
> as mandated.

> **And EXCLUDE THE BADGE SUBTREE from that walk.** Also prescriptive, and it is the reason the
> two requirements have to be stated together: a descendant walk that does not exclude the badge
> will find the *mark's* text in at least one app. **MyCal's mark draws a real `<text>8</text>`,
> so `.brand-logo`'s `textContent` is `"8"`** (`spec/app-logo.md` §9.6 records the same fact from
> the other side — `getByText('8')` matches the logo).
>
> mycal-dev deleted the `.brand-name` element and re-ran: with the exclusion the guard reports
> **"found 0"**. Without it, the walk would have found the mark, resolved a font size off it, and
> **reported a pass for a page with no label at all.**
>
> **MyCal-specific in cause, general in consequence:** that is *absent* read as *could not look*,
> which is the failure `spec/measurement-protocol.md` is largely built around, arriving inside the
> guard rather than inside a measurement.
>
> **Two suites found two different ways to pass while measuring the wrong thing, independently,
> in one afternoon.** That is the argument for §6.1 being prescriptive rather than descriptive:
> the method has more sharp edges than any one implementer will find.

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
> move its label from 14.797 to 19.203**, breaking §4.1 here. *(Found by mymail-dev, and the
> 19.203 is theirs: they ran the mutation rather than transcribing the closed form's 19.2 —
> §4.1.1 again, on a second number.)*
>
> Neither document can see that on its own. It is recorded in both.

---

## 7. The guard

`AGENTS.md` §2.5: if a number matters, put it in a test. This contract is guarded three
ways, and the third is *"by nothing, stated as such"*.

**State coverage per edit and per mechanism, never as "caught" or "not caught".** Every cell
below was run, not reasoned — which is the point of the table's existence as much as its
contents (§10):

| Edit | `check-contract.py` | The rendered suite |
|---|---|---|
| `1.1rem` → `1.10rem` | **FAIL** | pass |
| `1.1rem` → `1.1em` | **FAIL** | pass |
| `1.1rem` → `17.6px` | **FAIL** | **FAIL**, at the 24px root only |
| `body` stack reordered | **FAIL** *(WEAK)* | **FAIL**, resolved on the label |
| `font-size` added to the label element | **FAIL** *(§1, MyCal only)* | **FAIL** — 22.4px |
| Reload `padding` 4 → 20px | pass | **FAIL** — label `y` 28.797 |
| `min-width: 0` **and** `overflow` both deleted | pass | **FAIL** |
| `min-width: 0` alone | pass | **FAIL**, declarations test only (§8.1 — it changes nothing rendered) |

*(mycal-dev's table, run in MyCal. The two `pass` columns in the middle rows are not gaps to be
closed — they are the division of labour §7.1 and §7.2 describe. The rows where **both** fail are
the interesting ones: see §6.1.)*

### 7.1 Cross-repo, static — `tools/check-contract.py`

**The only thing that compares the three apps** — which is a claim about *comparison*, and is
the one superlative here that survived scrutiny. It is not a claim about being the only thing
that can see any given edit; see §3.2's table for which mechanism catches what. It pins:

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

Each app asserts its own half, per §6.1's method, **including a 16px root** (§4.1), and each
assertion is accepted only once it has been **shown red for the right reason** — which now
includes **confirming the mutation took effect**, per `spec/measurement-protocol.md`'s
*"Prove a new guard fails before trusting it"*. That step was added because of this work: a
mutation here came back green not because the assertion was weak but because the mutation was
inert, and **a mutation that does not mutate is indistinguishable from an assertion that does
not fire**. *(mycal-dev.)*
`mynotes/e2e/tests/logo.spec.ts:341-361` is the template. It asserts **at two roots** — the
pairs `[16, '17.6px']` and `[32, '35.2px']`, written as pairs rather than computed, because
`16 * 1.1` serialises as `17.600000000000001` in IEEE 754 and a computed expectation would fail
on the default root for a reason that has nothing to do with the app. *(mynotes-dev-b.)*

> **What a rendered suite can and cannot hold, narrowed after measurement.** This section used
> to say a rendered suite *"cannot hold §3.2 on its own"*, flat. That is right about MyNotes'
> template and wrong as a general claim:
>
> - **`1.1rem` → `17.6px` IS catchable — by asserting at a second root.** MyCal's suite expects
>   `26.4px` at a 24px root, and mycal-dev mutation-tested that exact conversion: **red on that
>   assertion alone, the 16px one still green.**
> - **`1.1rem` → `1.1em` is not catchable at any number of roots**, and the reason is sharper
>   than "identical today": in MyCal **every ancestor of `.brand` computes to the root size**,
>   because `body` sets no `font-size`. So `em` and `rem` coincide at *every* root, and no sweep
>   separates them. **§7.1 is what covers that**, and it is the residual justification for the
>   static check once the two-root assertion exists.
>
> **Record the condition, because it is exactly `AGENTS.md` §3.3's shape:** the `em`
> substitution is harmless *conditional on `body`, `.top-bar` and `.app` never taking a
> `font-size`* — and until now that condition was written nowhere. Any of those three acquiring
> one turns an invisible edit into a visible divergence.
>
> So the accurate form: **a rendered suite can hold §3.2 against `px` if it asserts at two
> roots, and cannot hold it against `em` at all.** *(Narrowing owed to mycal-dev.)*

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
- **Normalising `1.1rem`** — to `17.6px` (identical at a 16px root, frozen at every other),
  to `1.10rem` (identical computed *and* serialised), or to `1.1em` (identical at every root,
  for the reason §7.2 records). **§7.1 sees all three; a rendered suite asserting at two roots
  sees only the first** (§3.2's table).
- **Moving `font-size` / `font-weight` off the row onto the label**, or the reverse. Renders
  identically today. In MyCal it would silently drop the size from any second text child
  added to `.brand` later.

**MyCal** — `.brand`'s Reload button is in the row and moves the label (§4.2); the
`≤600px` rule hides the label as well as the badge (§4.4); and `.brand-name`'s
**`min-width: 0` is inert today and load-bearing the day `overflow` changes**, which is a
different hazard from the one it looks like:

> **Deleting `min-width: 0` alone changes nothing rendered at all.** `overflow: hidden` is what
> zeroes a flex item's automatic minimum size; while it stands, `min-width` does no work.
> Measured by mycal-dev, 38-character name, label `clientWidth`:
>
> | mutation | label width | Reload | suite |
> |---|---|---|---|
> | shipped | 132 | in column | green |
> | delete `min-width: 0` | **132 — unchanged** | in column | **green, correctly** |
> | delete `overflow: hidden` | 132 | in column | green — clipping stops, which is paint, and nothing measures it |
> | **delete both** | **380** | **pushed out** | **red** |
>
> So it is `spec/app-logo.md` §5's **delayed hazard**: the edit that arms it (removing
> `overflow`, or changing it to `visible` for a tooltip) and the edit that fires it (removing
> the now-genuinely-redundant `min-width`) are separate, and **neither looks wrong alone**.
>
> **It is also the one declaration on that rule no rendered measurement in any app can
> defend**, which makes it a live specimen for §7.3 rather than an item in a list.
>
> *(This bullet used to say deleting `min-width: 0` breaks the ellipsis. It came from
> mycal-dev's own phase-1 report and their mutation run is what refuted it — and MyCal's rule
> carries a comment saying **`overflow` zeroes the automatic minimum size**, which is correct
> and was three lines from the claim when it was written. `AGENTS.md` §3.2: the wrong sentence
> was the one nobody doubted, in both directions at once.)*

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
  assertion in the suite, and a `rem` → `px` change passed it.
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

### 8.4a Uncovered, named, and not being fixed here

Recorded so the omissions read as decisions. None is a reason to hold up the contract.

- **The label's `colour` is asserted by nothing**, in any app. It is recorded in §5 and not
  mandated, so this is consistent — but MyNotes' `a { color: var(--link) }` hazard (§8.3) is real
  and unguarded, and no sibling can catch it.
- **Nothing anywhere reads paint.** MyCal's ellipsis is asserted through `scrollWidth` /
  `clientWidth`, which establishes that the box truncates and **not that an ellipsis is
  rendered**. §8.5's whole table is about declared behaviour, not painted pixels.
- **MyCal's demo build is a second shipped surface** and is what GitHub Pages publishes. Its
  label figures were measured identical to the real build (mycal-dev, phase 1) and **nothing
  asserts them there**. Same open item `spec/app-logo.md` §9.6 records for the badge.
- **MyCal does not type-check its e2e suite.** Nothing runs `tsc -p e2e/tsconfig.json` — not
  `build.sh`, not CI — and Playwright transpiles without checking, so a type regression in the
  suite is invisible at runtime. It is clean when run by hand.

  > **Known and deliberately not done**, on the reviewer's own reasoning: wiring a type-check
  > into the build and CI changes the workflow for every contributor and does not belong in a
  > commit about a label contract. **Flagged rather than fixed**, and with the human as an open
  > item — the shape `spec/app-logo.md` §9.1 uses. Worth knowing that this commit adds the
  > suite's most type-dependent code, a discriminated union whose narrowing is the only thing
  > keeping its field accesses legal.

### 8.5 Degradation under a long name differs, and is not mandated

Outside the owner's three words, so not specified — but recorded, because *"the same
placement"* invites a reader to assume the same behaviour when space runs out, and it is not
the same.

| | Behaviour **[measured]** |
|---|---|
| MyCal | ellipsizes — `white-space: nowrap; overflow: hidden; text-overflow: ellipsis`, with a `min-width: 0` that is **inert while `overflow` stands** (§8.1). Proven by substituting a 38-character name, which shows **the set works** and not that each member contributes |
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
  §2's exclusion (§2.1). The owner ruled on §4.3 (record the vertical remainder, do not
  mandate authorship) and §4.4 (MyCal's ≤600px hide is a sanctioned exemption).

- **Adoption: measured and conforming in all three apps, at named local commits on their
  `main` branches. NOTHING IN THIS ROUND IS PUSHED — including this
  repository.** No hashes are recorded here, and that is the point rather than an omission.

  > **A hash pays the full cost of perishability and buys a reader nothing unless they can
  > resolve it.** Measured at the time of writing: **every one of the four repositories' `main`
  > is ahead of its `origin/main`**, this one included. Every adoption commit exists in one
  > working checkout and nowhere else; clone any of these repos and you get the state *before*
  > this contract.
  >
  > *(No count is given, deliberately. "N ahead" is a figure this very commit would falsify for
  > at least one repository — `AGENTS.md` §3.2's number-in-prose-beside-the-thing-it-describes,
  > and the check is one `git status -sb` away.)*
  >
  > `spec/app-logo.md` §10 is the precedent and it faced exactly this, recording no hash while
  > MyNotes' work sat on an unpushed branch. **It is also the counter-example**: a hash was added
  > there later, once `d68c1c5` was on a `main` — and *that* has since become unresolvable again,
  > because MyNotes is now two commits past it and none of them are pushed. **The lesson is not
  > "never record a hash"; it is that a hash is only worth its cost once someone other than its
  > author can fetch it.**
  >
  > **Add them in a later commit, against verified refs**, when this round is published. The
  > sentence above is true now and stays true; a hash written today would need writing twice.
  > *(Correction owed to mycal-dev, who caught that the instruction to record hashes would have
  > produced a line nobody could act on.)*
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

- **The guard's own comment denied a hazard this document already listed**, and only running
  it settled which was right. `tools/check-contract.py` claimed that declaring the size on the
  label *"would report 'rule not found' here. Loud, not silent."* It does not — that edit ran
  **green, exit 0**, in the value the output labels STRONG. Meanwhile §8.1 had *"moving
  `font-size` onto the label"* in its list of silent breakages the whole time.

  > **The document knew and the code contradicted it.** That is `AGENTS.md` §2.5 — numbers and
  > claims in comments going stale — with the sharpest possible operand: **the stale claim was
  > in the guard, describing itself.** Prose that is wrong misleads a reader; a guard that is
  > wrong about its own coverage misleads everyone downstream of a green run, and it is the one
  > artefact nobody re-reads *because* it is passing.
  >
  > It was found by code review running a mutation, not by anyone reading either file. **Both
  > texts had been read many times that day.** `spec/measurement-protocol.md`'s acceptance rule
  > exists for exactly this and had not been applied to the new pin: it was accepted on a green
  > run plus four mutations that all happened to attack the row rather than the label.

- **This document went stale against work it caused — three times, which makes it a pattern
  rather than three accidents.** Listed as one item deliberately:

  | The claim | Falsified by |
  |---|---|
  | §4.1: *"in MyMail neither child opts out"* | the `align-self` fix §6.3 asked for |
  | §7.2: MyNotes *"asserts at a 16px root only, which a `rem` → `px` conversion passes"* | MyNotes taking §7.2's own two-root finding into its suite |
  | §8.2: MyNotes has *"one assertion … a `rem` → `px` change passes it"* | the same commit |

  > **`AGENTS.md` §3.5 at the shortest possible timescale, and with the causation reversed.**
  > The usual specimen ages over weeks and is found by someone reading an unrelated file. These
  > aged over minutes to hours, and **the falsifying commit was one this document asked for.**
  > A contract that tells three suites to change is, by construction, describing a state it is
  > in the act of ending.
  >
  > **So the general form: any sentence describing an app's current coverage is a claim with a
  > deadline the moment the same document asks that app to improve it.** Prefer describing what
  > the suite must do over what it presently does; where the present state is worth recording —
  > as §8.2's *"almost none"* is — put it in the past tense and name the commit that ended it.
  > All three of these were caught by app agents reporting the contradiction rather than
  > working around it, which is the only reason they were cheap.

- **A tool that destroyed the evidence and left the result intact.** mymail-dev's first re-run
  of the mutation set used `sd` with a replacement containing `$tag`, which was read as a capture
  reference, so every case wrote to one output file. **The pass/fail counts had been echoed live
  and survived; the per-case read-backs did not.** They re-ran the whole set clean rather than
  reporting from the surviving file.

  > **The run looked completely normal, and what it destroyed was the evidence rather than the
  > result.** *(mymail-dev's formulation, and it is this round's pattern in one sentence.)*
  >
  > Every instrument failure recorded here is a variant of it: an inert mutation, a pattern that
  > cannot match, a stale server, a substring test, a red from someone else's scratch edit. **The
  > answer survives; the thing that would let you check it does not.** Re-running is cheap and
  > reporting from a damaged record is not — and the damaged record does not look damaged.

- **Describing a guard's coverage from the one tool you happened to run — three agents, three
  routes, independently, in one round.** This is the strongest version of the pattern in this
  document and it is the reason §7 states coverage per edit and per mechanism.

  | Who | The claim | Why it was wrong |
  |---|---|---|
  | this document | *"§7.1 is the only thing that can see a `1.1rem` edit"* | never ran a rendered suite at a second root |
  | the manager, in relay | *"`1.1em` is uncatchable by anything"* | never ran the static check against it |
  | mycal-dev | three *"caught by nothing"* rows, plus a fourth *"caught by neither"* | had run only Playwright |

  > **All three had measured something. None had measured the other mechanism.** The error is not
  > carelessness — every one of these was written by someone holding a real result in their hand
  > — it is **generalising from the instrument you happen to be holding to the set of instruments
  > that exist.** `AGENTS.md` §3.2's unit question, where the unit is the *tool*: the axis fully
  > swept was the one that did not vary.
  >
  > **So never write "caught" or "not caught".** Write a cell per mechanism, and run every cell.
  > mycal-dev's table in §7 is that, and three of its rows were wrong before they ran it.

- **A plausible rationalisation, offered and not acted on — which is why the question stayed
  open long enough to be settled.** mynotes-dev-b saw two `FAIL` blocks and a verdict reading
  `FAILED — 1 pinned value(s) disagree`, and offered a guess: *the count probably excludes the
  WEAK pin deliberately.* **They did not act on it.** They flagged it as possibly intended, said
  they had not read the counting code, and declined to raise it as a defect in a repository that
  was not theirs.

  **Reproduced against three materialised `main`s with both pins mutated: two `FAIL` blocks,
  verdict `2`.** So the counting code does not undercount, and the reported pairing was a
  reporting slip rather than a defect.

  > **The guess was reasonable, specific, and would have closed the question wrongly.** It has
  > the grammar of a finding — a mechanism, a motive, a design intent — and nothing in it is
  > checkable without opening the code. That is `AGENTS.md` §3.2's *"the number you explain away
  > is the finding"*, in the one variant that ends well: **the explanation was composed and then
  > not believed.** Composing it cost a sentence; the measurement that refuted it cost one
  > command.
  >
  > **What made this cheap was refusing to resolve someone else's contradiction** (`AGENTS.md`
  > §4). Had they silently accepted their own explanation, nothing would have prompted a check —
  > and the undercount hypothesis, had it been true, would have sat on **the verdict line**, which
  > this script's own caveat block identifies as the one line a hurried reader trusts.

  **And reproducing it nearly went wrong in the way this round keeps finding.** The first attempt
  mutated only one of the two pins — the second `sd` invocation rejected a replacement string
  beginning with `-` and did nothing — so the run showed one `FAIL` and a verdict of `1`, which
  is *internally consistent and answers a different question than the one being asked*. It was
  caught by printing the `FAIL` blocks and counting them rather than reading the verdict alone.
  `spec/measurement-protocol.md`'s **confirm the break actually took effect** — a step added
  earlier in this same changeset — catching its own author two commits later.

- **A correctly-scoped finding losing its scope in a relay — a different mechanism from the
  three above, and it went wrong in one hop.** mycal-dev established that `em` and `rem` coincide
  at *every* root in MyCal, so **no number of root sizes separates them** — a statement about
  *rendered* assertions, and true. It was relayed as *"uncatchable by anything, in any repo"*,
  which is a different claim and false: `tools/check-contract.py` compares declaration text and
  catches it immediately, demonstrated by mutating MyNotes to `1.1em`.

  > **The three specimens above are claims that went stale over time. This one was wrong on
  > arrival, while the original was still on file and correct.** No amount of re-reading the
  > repository would have found it, because the repository was never what changed — the scope
  > qualifier was dropped between one agent and the next.
  >
  > **What caught it was the recipient testing an instruction rather than acting on it.** Told
  > that a substitution was uncatchable, they ran it and watched the checker catch it. That is
  > the cheap half of `AGENTS.md` §3.1's *"a citation to a document you were never given is a
  > gap"*, in its most ordinary form: **when a relay tells you something cannot be detected, the
  > detector is usually one command away.**

- **A torn read, observed live, of the mirror case `AGENTS.md` §3.5 says nobody ever catches.**
  mynotes-dev-b reported §7.1 as describing a check that did not exist: their grep found no
  `app-name-label`, no `1.1rem` and no font-stack logic in `tools/check-contract.py`, and they
  saw `spec/app-name-label.md` as **untracked**. **Both readings were correct when taken** —
  they read between the drafting and the committing.

  > **This is §3.5's mirror case — a claim going *true* without an edit to it — caught in the
  > act**, which that section says is the harder direction precisely because nothing prompts a
  > re-check. Here the re-check happened for one reason: **they reported the contradiction
  > instead of resolving it.** `AGENTS.md` §4's *"report a contradiction rather than resolving
  > it"* is usually justified by the risk of editing code to match a document; this is the other
  > payoff, and the cheaper one. Had they quietly weakened their comments to match what they
  > saw — they had begun to — the correction would have had no trigger at all.
