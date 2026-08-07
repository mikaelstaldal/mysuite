# AI coding agent instructions

Guidance for AI coding agents working in this repository **or in any of the three app
repositories it governs**: MyCal (`../mycal`), MyMail (`../mymail`), MyNotes (`../mynotes`).

If you are working in one of those three and have landed here from a reference in its
`AGENTS.md`, read §1 and §2 before you change anything.

---

## 1. This repository is the source of truth for cross-app UI contracts

MyCal, MyMail and MyNotes are three separate applications that must look like one product.
The UI elements required to be identical across them are specified **here**, in
[`spec/`](spec/), and the three app repos reference those contracts rather than restating
them.

There is no shared stylesheet, no shared component library, and no code of any kind in this
repository. It is Markdown. Each app implements the contract in its own CSS, with its own
class names and its own tokens.

Currently binding:

- **[`spec/sidebar-footer.md`](spec/sidebar-footer.md)** — the light/dark theme toggle and
  Settings button in the left sidebar's footer.

Cross-cutting:

- **[`spec/measurement-protocol.md`](spec/measurement-protocol.md)** — how to verify a change
  to shared UI in any of the three apps.

---

## 2. The rules that matter most

### 2.1 Changing a value here is a three-repo change

A value in `spec/` is implemented in MyCal, MyMail and MyNotes. **Changing it means changing
all three, or none.**

There is no shared stylesheet and no cross-repo test, which means **nothing anywhere can
detect that the three have drifted apart.** No build fails. No test goes red. The divergence
is found by a person noticing a button move when they switch browser tabs.

Treat any change to a specified value as touching three repositories from the start.

### 2.2 Never "fix" a shared value in one app

This is the same rule from the other side, and it is the one most likely to catch you out,
because it fires when you are working in an app repo and are not thinking about this one at
all.

If you are in MyCal, MyMail or MyNotes and you find one of these values looking wrong —
a redundant-looking declaration, an odd number, a rule that contradicts the surrounding
file's conventions — **do not fix it locally.** Raise it.

- The value is almost certainly deliberate, and the reason is written down next to it or in
  the contract.
- **Divergence is the defect.** A locally-corrected value is worse than the wrong value it
  replaced, because now the three disagree and nothing will say so.
- Several of the obvious objections are already recorded in the contract's "Known gaps"
  section as deliberate, deferred, or accepted — including at least one real defect that is
  waiting on a human decision. Check there before raising a new one.

The self-contained rule blocks in these apps are self-contained *on purpose*: they restate
properties they could inherit, so the pinned appearance cannot drift when a generic `button`
rule changes. Redundancy is the mechanism, not an oversight.

### 2.3 Token names are per-project; values are shared

What is mandated is the **resolved value** — the pixel, the hex colour, the computed
property. Never the token name, never the class name, never the number of hops to reach it.

The three palettes hold identical values under different names (`--text-subtle`,
`--sidebar-muted`, `--muted` are the same colour in the same role). **Do not unify them.**
Name unification is explicitly out of scope; it belongs with a future shared stylesheet, if
there ever is one. Renaming a class can also break e2e locators that pin it.

Each contract carries a table mapping the shared roles to each repo's local names.

### 2.4 A green build proves nothing about geometry

All three apps embed `web/static/` into the binary with `//go:embed`, so a running server
keeps serving the assets it started with. `./build.sh` alone changes nothing the browser
sees; a stale server makes the test suite pass or fail against assets that are not the ones
you edited, silently.

Follow **[`spec/measurement-protocol.md`](spec/measurement-protocol.md)** before reporting
any measured number: fresh build → fresh server → md5 served-vs-disk **including the
compiled JS** → cache-busted navigation → a sentinel value that must have changed.

Tests being green tells you the code compiles and the assertions hold against *something*.
Geometry is only ever established by measuring a rendered page.

### 2.5 Numbers in comments go stale the moment code moves

This is the lesson that cost the most. **Prefer an assertion over prose.**

Two of the three repos shipped comments describing histories that had never existed in their
own repository — describing the removal of a rule that had only ever existed in an
uncommitted amend chain. A comment describing history nobody can see from the diff is worse
than no comment: it is confidently wrong, and nothing checks it.

So:

- If a number matters, **put it in a test.** MyCal's `e2e/tests/sidebar-footer.spec.ts` is
  the model — the only machine-checkable statement of any of this, and it now runs in CI and
  gates publication. MyMail and MyNotes still have no harness, so cross-repo drift remains
  undetectable by anything.
- **Some pins cannot be defended by rendering at all.** Where a value is already correct in
  one app for its own reasons, that app's rendering cannot detect the pin going missing — so
  assert the *declaration* off the CSSOM, not the computed box. See
  `spec/sidebar-footer.md` §3.1. And a few pins are uncatchable by any test
  (`0.80rem` vs `0.8rem` is identical computed *and* serialised); those are held by review,
  and saying which are which is part of describing coverage honestly.
- If it cannot be tested, **say in the comment that it is a reading rather than a contract**,
  and say what it was read on. Text measurements are per-platform and per-font.
- When you write a number down, write its conditions with it. "29.2px" is a claim that stops
  being true when a reader changes their browser font; "29.2px at the default 16px root font
  size" stays true.
- Do not describe history that is not in the repository's history.

---

## 3. Working in this repository

- **Markdown, plus `tools/`.** The Markdown-only rule was lifted by the human for one
  purpose: scripts that *check* a contract. `tools/check-contract.py` is the first. Still no
  build system, no CI, no package manager, and no dependencies — a checking script must run
  from a clean checkout with nothing installed, and must not introduce anything the app repos
  would have to adopt (they have a standing rule against npm/npx). Python 3 or shell,
  stdlib only.

  A check belongs here when it is **cross-repo**: this is the only place that knows about all
  three apps at once. Anything checkable inside one app belongs in that app's own suite.
- **A checking script must state its limits in its own output**, not only in the docs. A
  reader of a green run has to know what green does and does not mean — see §2.4, and
  `spec/sidebar-footer.md` §9.1 on why "gates publication" beat "prevents breakage".

  **And verify it does so on the failing path.** `tools/check-contract.py` printed its limits
  only on success. While one app's change was pending it failed on *every* run — so the one
  artefact this rule exists to guarantee was dead code on every run anyone would actually
  read. A red reader over-reads a result at least as easily as a green one: they see "2 values
  disagree" and infer the other thirty assertions are coverage. **Print the limits on every
  terminating path, and confirm it by running each of them.**
- **No remote is configured.** Commit locally; do not attempt to push. Cross-references from
  the app repos name this repo by path (`../mysuite`, `spec/sidebar-footer.md`) rather than
  by URL, because there is no URL to give. When a remote is added, those references should be
  updated.
- **`CLAUDE.md` is a symlink to this file**, matching the convention in all three app repos.
  Edit `AGENTS.md`.
- **Some rules are stated in more than one file here, and that is deliberate.** The
  three-repo rule (§2.1, §2.2) appears in `README.md` and `spec/README.md` as well; the
  measurement warning (§2.4) and the stale-numbers lesson (§2.5) each appear again in
  `spec/measurement-protocol.md`. An agent or a person may arrive at any one of these files
  and read only that one, and these are the rules that are expensive to miss. **The canonical
  statement is the longest one** — `measurement-protocol.md` for verification, this file's
  §2 for the three-repo rules, the individual contract for anything about a specific value.
  When you change one, change the others; this is the one place duplication is accepted, and
  it is accepted only for these three rules.
- **One contract per file** in `spec/`, indexed in [`spec/README.md`](spec/README.md). Add a
  row to that table when you add a file.
- **Always name the file when citing a section number across files.** `AGENTS.md` and
  `spec/sidebar-footer.md` both have a §2.2, a §2.5 and a §3.1, and they are about entirely
  different things — this file's §2.2 is *never fix a shared value in one app*, the contract's
  is *the 29.2px acceptance height*. A bare `§2.2` in a colour comment therefore sends a
  reader to arithmetic and leaves them concluding the comment is confused.

  This is not hypothetical: mynotes-dev found it in its own CSS, and fixing it exposed **three
  bare citations in this repository**, two of them written the same day by the author of the
  rule they were citing. If an app repo carries a bare `§` in a comment about a shared value,
  it has the same defect.

  The convention: `AGENTS.md §2.2` when it is this file, a bare `§` only inside the document
  it refers to, and a header line saying which file bare `§` means in any app-repo comment that
  uses several.
- **When you tell the app repos a rule has changed, name the commit — and know that a message
  quoting a *figure* is more perishable than one stating a *rule*.** A broadcast announcing the
  backdrop withdrawal was still entirely correct about the withdrawal an hour later, while the
  one number it quoted had been corrected in the meantime. A reader acting on it nearly filed a
  defect that no longer existed.

  Naming the commit is what makes staleness **diffable**; it is the sender's half and the half
  that could be automated later. Re-reading the spec at `HEAD` before acting on a report about
  the spec is what makes staleness **noticed**; it is the reader's half, it costs a minute, and
  it is what actually caught this one. Do both, and if a broadcast has to quote a figure, say
  which claims are rules and which are values. *(Framing owed to mynotes-dev, from the near-miss
  it had.)*

### 3.1 Provenance — say what a contract was written from

A contract here is written from somewhere: a set of decisions, rulings, measurements and
messages produced while the thing was being built. **State which set, in the contract**, and
make the set enumerable before you start writing.

This is not bookkeeping. It failed once already, and it is worth knowing exactly how.

**Verify the source set by enumerating what was written, not by recalling what was sent.**
`spec/sidebar-footer.md` was written from a handover of thirteen documents that was assembled
from memory and believed complete. It was missing six. The audit that found them took about
two minutes and would have taken the same two minutes beforehand.

**The detection mechanism is the part that generalises: a citation to a document you were
never given is a gap.** Nobody can spot an absent premise by reading — there is nothing to
see. But anyone can spot a dangling reference. That is exactly how this one surfaced: an agent
in an app repo cited a ruling *by name* to justify something the contract contradicted, and
the contract's author had never received that document. So:

- If someone cites a document that is not in your source set, **stop and get it.** Do not
  reconstruct what it probably said, and do not treat the contradiction as a disagreement to
  be resolved on the merits — you are missing a premise, not losing an argument.
- If you write a contract, say which documents it came from, so the next reader can run the
  same check against you.

**What the miss actually cost, so the risk is concrete.** One of the unreceived documents
carried a standing ruling that the shared `transition` takes no `prefers-reduced-motion`
guard, because it animates colour only. Absent that, adding such a guard is a plausible,
well-intentioned accessibility edit — and one that changes nothing observable, in a property
no test asserts. It would have produced a **permanent, undetectable three-way divergence**:
not caught by the e2e suite, not by review, not by a screenshot, not by painted-pixel
comparison. Every other defect found in this work was visible to *someone*; that one was
visible to no one.

An incomplete source set does not produce obviously-wrong contracts. It produces contracts
that are silently missing the rules nothing can check.

### 3.2 Beware a rationale that is true of the apps you were thinking about

The most common defect in this contract has not been a wrong value. It is **a reason that
holds for two apps, written as though it held for three.** Four instances so far — the first three
each caught by the repo it was false of, the fourth caught only because the app it was false
of happened to be the one supplying the number:

| Written | False of | Because |
|---|---|---|
| "the sidebar column is sized in `rem`" | MyNotes | its column is `420px`, a sanctioned exemption |
| "the footer paints `--surface`" | MyNotes | its footer is transparent; the panel behind it paints |
| "the panel is the footer's parent" | nobody *yet* | true of all three today, required by none |
| "that app's own `AGENTS.md` or `spec/REQUIREMENTS.md`" | MyCal | it has no `spec/` directory at all |
| "the hover fill's floor is 1.101:1, the weakest the suite ships" | MyNotes | it ships 1.053:1 — 1.101 is the other two |

**Two of those rows were committed in the changeset that added or extended this section**, by
its author, while writing it down. That is not irony worth enjoying — it is the measure of how
easily the pattern slips past someone actively looking for it. Check the claim against all
three by name; do not assume you are immune because you just wrote the warning.

#### Why writing the warning does not protect you: attention follows the last defect

mynotes-dev named the mechanism, from a case of its own: it wrote a false claim about the code
(*"nothing in this block declares a background of its own"*, on a rule that declares
`background` three lines later) **while correcting a stale comment, with the spec open.** In
its words: *"the wrong claim was in the sentence I was least worried about, because I had just
written it."*

That accounts for every instance in the table above and two more from the same week:

| The new defect | Was committed while |
|---|---|
| `spec/REQUIREMENTS.md` named for all three | writing §3.2 itself |
| the hover-fill floor set at 1.101 | extending §3.2 |
| three bare `§2.2`/`§2.5` citations | introducing the deviation rule two of them cite |
| a false claim about a `background` declaration | **replacing a clause it had just disproved** |

**Freshly written text is the least reviewed text in any changeset**, and it is least reviewed
precisely when the author is concentrating hardest on some other failure mode. So the practical
form is not "be careful" — it is: **re-read what you added last, against the code, after you
have finished the thing you were concentrating on.** The sentence you are most confident in is
the one nobody has checked, including you.

**And the sharpest case is the last row, which is why its wording is specific.** That claim was
not merely written while its author was distracted — it was written *as the replacement for a
clause just deleted for being wrong*. The old text said MyCal's fill "vanishes"; the new text
made a claim about which element paints, and attached it to the wrong rule. mynotes-dev's
form: **the most dangerous text in a correction is the correction itself, because it is the
part that has been reasoned about most recently and therefore feels most settled.**

So the re-read pass matters most on exactly the changesets that feel safest — the ones whose
purpose was fixing something. A correction inherits none of the scrutiny that found the defect
it replaces.

The last row adds a mechanism, because "check all three" did not catch it. The figure was
taken from a per-app table that had just been read, and **the value appearing in two of three
rows read as the value.** So: when deriving a bound from a per-app table, take the extreme
rather than the common value, and **name the app it came from in the same sentence** — a
bound with an app's name attached is falsifiable by anyone who knows that app, and one without
is not.

### 3.3 A dormant defect is harmless *conditionally*, and the condition is not written down

A neighbour of §3.2 rather than the same thing. §3.2 is a rationale that was never true of
every app; this is one that is true today and stops being true because of a change somewhere
else.

MyCal carried a known-dead `@media (max-width: 600px)` block for weeks — equal specificity,
later source order, so nothing in it applied. Correctly reported, correctly deferred, genuinely
harmless. Then the footer started painting a colour, and on a phone it rendered as a 208px
white stub two-thirds across the screen with a border hanging in mid-air. **Nothing about the
dead rule changed. What changed was the thing that made it survivable.**

In its own words: *"leaving it dead stopped being neutral the moment the footer started
painting a colour."*

So:

- When deferring a defect, **record what makes it harmless**, not just that it is. "Dead rule,
  no effect" ages badly; "dead rule, no effect *because nothing in it paints or positions*" is
  a condition a future reader can check.
- When a change alters something a deferred item's harmlessness rested on, **that item is back
  in scope** — even though it is untouched and its own ticket says out-of-scope.
- Expect the discovery to arrive as an unrelated-looking bug. The phone breakage looked like a
  regression in the backdrop change; it was a dormant defect waking up.

The value was right every time. The *justification* was written from whichever
implementations the author had in mind, and it fails the moment a reader checks it against
the app it does not describe — who then reasonably concludes that app has drifted.

So, when writing a rationale:

- **Check it against all three, by name**, not against the two that prompted it.
- If it is true of a subset, **say which subset and why the others are exempt.** An exemption
  stated is documentation; an exemption omitted looks like drift.
- Prefer stating the **required result** over the mechanism that achieves it. "The colour
  behind the controls is `--surface`" survives all three implementations; "the footer paints
  `--surface`" does not.

  **That example has since been overtaken, and the correction is the more useful lesson.**
  The owner later ruled that the three apps may differ in the colour behind the controls, so
  the "durable" phrasing was withdrawn too (`spec/sidebar-footer.md` §11) — one rung later
  than the mechanism version, but withdrawn. It survived *implementation* differences and
  not a *product* decision, because it still named a colour. What replaced it names a
  relationship instead: the backdrop must be opaque, recorded per app, and everything drawn
  on it verified against it.

  So the ladder is: mechanism → required result → **the constraint the result has to
  satisfy.** Each rung survives a class of change the one below does not, and nothing
  survives everything. Climb it when you can, and expect to be wrong about where the top is.
- Watch for a rationale that is true today by coincidence. The third row above is that case:
  nothing requires the painting element to be the footer's parent, so any check assuming it
  must say it is assuming it (§2.4).
- **State resolved values, not token names** (§2.3), and give the local names for each repo
  in a table.
- **Specify observable results, not mechanisms** — unless the mechanism genuinely is the
  contract, in which case say so explicitly and say why. `spec/sidebar-footer.md` §7 is an
  example of the exception.
- **Keep the "Known gaps" and "History" sections honest and current.** Record what is
  unverified, what is deferred and why, and what has been accepted as a residual risk.
  Withdrawn rules stay listed — a superseded rule tends to survive in a comment somewhere
  long after the code has moved on, and the list is how somebody finding one knows it is
  stale.

## 4. Working in one of the app repos

- Read the relevant contract in `spec/` **before** editing a rule it covers, and read the
  derivation comments in the CSS itself. Both exist because the shape of the CSS alone does
  not tell you which declarations are load-bearing.
- Verify per `spec/measurement-protocol.md` (§2.4). State the root font size, the theme, and
  what a contrast ratio was measured against — apps paint different backdrops behind the same
  control, so a ratio copied from a sibling repo is a wrong number that looks like a checked
  one.
- Report a contradiction rather than resolving it. **If a contract and the shipped CSS
  disagree, the shipped CSS is the ground truth and the contract needs correcting** — say so
  instead of editing code to match a document.
- Do not restate a contract's values in an app repo's own documentation. Reference the
  contract. Restating it recreates exactly the duplication this repository was created to
  remove.
- **Put the warning where an agent actually reads.** A requirements or product document is
  not what someone opens before editing a stylesheet — so a pointer that lives only there
  will be missed by exactly the person who needed it. Each app repo should carry a short
  section in its own `AGENTS.md` saying that these declarations are governed from outside
  the repo, and naming the *routine tidying* that breaks them silently: normalising
  `0.80rem` to `0.8rem`, folding the rule back into a shared button class, dropping a
  "redundant" `flex-shrink: 0` or `text-align: center`, adding a `font-weight` to the base
  `button` rule, restoring `outline: none`. Every one of those is a reasonable edit
  everywhere else in the same file.

  MyNotes' `AGENTS.md` §"The sidebar footer is governed from outside this repo" is the
  model. This is the highest-value thing an app repo can add, because it is the only
  guard that fires before the change rather than after — and in two of the three repos
  there is no test that fires at all.
