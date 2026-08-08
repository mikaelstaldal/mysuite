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

There is no shared stylesheet and no shared component library. This repository is Markdown,
**plus `tools/`** — scripts that *check* a contract, and nothing else (§3). Each app implements
the contract in its own CSS, with its own class names and its own tokens.

*(This paragraph read "no code of any kind in this repository" until `tools/check-contract.py`
landed and made it false, with no edit to it — §3.5's own shape, in §1, corrected 120 lines
later in §3 and nowhere near the reader who starts here. `README.md` states the exception
inline and was never wrong.)*

Currently binding:

- **[`spec/sidebar-footer.md`](spec/sidebar-footer.md)** — the light/dark theme toggle and
  Settings button in the left sidebar's footer.
- **[`spec/app-logo.md`](spec/app-logo.md)** — the app logo badge at the top left: its box, fill,
  glyph size and extent, placement and accessibility. Implemented in MyCal and MyMail; **MyNotes
  in progress.** The app-name label beside the badge is deliberately **out of scope** — that
  contract's §2 records the ruling and its condition, so do not read the labels as an oversight.

Cross-cutting:

- **[`spec/measurement-protocol.md`](spec/measurement-protocol.md)** — how to verify a change
  to shared UI in any of the three apps.

---

## 2. The rules that matter most

### 2.1 Changing a value here is a three-repo change

A value in `spec/` is implemented in MyCal, MyMail and MyNotes. **Changing it means changing
all three, or none.**

There is no shared stylesheet and **no cross-repo test that runs automatically**, which means
**nothing will detect that the three have drifted apart.** No build fails. No test goes red.
The divergence is found by a person noticing a button move when they switch browser tabs.

The qualifier is exact and is not a softening. `tools/check-contract.py` *can* see cross-repo
drift and is the only thing that can — but nobody's CI runs it, so it guards nothing until
somebody chooses to run it (`spec/sidebar-footer.md` §10.7). Each app's own e2e suite is blind
to the other two by construction, and **all three of those suites now run in CI**, which changes
nothing here: three pipelines that each see one app still leave the comparison between apps
performed by nothing.

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

- If a number matters, **put it in a test.** All three repos now have an
  `e2e/tests/sidebar-footer.spec.ts` holding their own half of the contract, and **all three
  now run in CI**, each gating publication on push to `main`. See `spec/sidebar-footer.md`
  §9.1, which records the step-level verification and the date it was taken.

  *(This bullet said "**Only MyCal's** runs anywhere" until 2026-08-08, and it was falsified by
  two pushes rather than by any edit — `spec/sidebar-footer.md` §9.1's annotation has the
  mechanism. Note what it means for the rule this bullet states: putting a number in a test is
  now worth more than it was, because in all three repos something actually runs the test.)*

  **Three per-app suites are still not a cross-repo check**, and adding more cannot make one:
  each is blind to the other two by construction, so all three stay green through a
  divergence. **Cross-repo drift remains undetectable by anything that runs.**
- **Some pins cannot be defended by rendering at all.** Where a value is already correct in
  one app for its own reasons, that app's rendering cannot detect the pin going missing — so
  assert the *declaration* off the CSSOM, not the computed box. See
  `spec/sidebar-footer.md` §3.1, which now measures how narrow this is: for the three pinned
  inherited properties, **no app's rendered box can detect any of them going missing**, and
  exactly one computed value in the whole suite can. And a few pins are uncatchable by any test
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
- **The remote is `origin` → `git@github.com:mikaelstaldal/mysuite.git`**
  (<https://github.com/mikaelstaldal/mysuite>). Commit locally; **pushing is the human's
  call** — say the work is ready rather than publishing it or routing around a missing
  credential. `git remote -v` in each app repo is authoritative for where that one lives.

  Cross-references from the app repos still name this repo **by path** — `../mysuite`,
  `spec/sidebar-footer.md` — and should keep doing so: the path is what resolves for a reader
  with the four checkouts side by side, which is also the layout `tools/check-contract.py`
  assumes. What the remote changed is not the path but the *reason* some files gave for it.
  Give the URL beside a path where a reader may not have the checkout; never in place of it.
  See §3.5: what this bullet used to say is that section's second specimen.
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

  **"The longest one wins" settles which copy is canonical, not which copy is correct** — and
  those come apart as soon as the copies drift. Before consolidating or moving any of them,
  read §3.4: a move between files silently picks a winner among statements that disagree, and
  it does so without breaking a single reference.
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
holds for two apps, written as though it held for three.** Every instance found so far — the
first three each caught by the repo it was false of, the fourth caught only because the app it
was false of happened to be the one supplying the number:

| Written | False of | Because |
|---|---|---|
| "the sidebar column is sized in `rem`" | MyNotes | its column is `420px`, a sanctioned exemption |
| "the footer paints `--surface`" | MyNotes | its footer is transparent; the panel behind it paints |
| "the panel is the footer's parent" | nobody *yet* | true of all three today, required by none |
| "that app's own `AGENTS.md` or `spec/REQUIREMENTS.md`" | MyCal | it has no `spec/` directory at all |
| "the hover fill's floor is 1.101:1, the weakest the suite ships" | MyNotes | it ships 1.053:1 — 1.101 is the other two |
| "MyNotes' buttons inherit `text-align` from `body` via `button { font: inherit }`" | MyNotes | `text-align` is not in the `font` shorthand, so the UA's `text-align: center` is never displaced |
| "the `curl \| md5sum` exit-status bug is live in all three `test-e2e.sh`" | **all three** | every one of them sets `pipefail` on line 12, which is exactly what defeats it |
| "every `tsc` error is in `node_modules`, none in any suite's own tests" | MyCal | it has 4 in `tests/` — the split was measured for the other two and generalised to it |
| "only MyMail's docs claim its suite gates publication in CI — one repo, not a pattern" | MyMail *and* MyNotes | the grep covered `web/AGENTS.md` in three repos; the claim was in four locations across root, `web/` and `e2e/` files |

*(The count that used to open this paragraph is gone deliberately. It said "four" beside five
rows — a number in prose describing a list directly below it, stale within one changeset, which
is §2.5's complaint arriving inside §2.5's own neighbour.)*

**Two of those rows were committed in the changeset that added or extended this section**, by
its author, while writing it down. That is not irony worth enjoying — it is the measure of how
easily the pattern slips past someone actively looking for it. Check the claim against all
three by name; do not assume you are immune because you just wrote the warning.

**And "all three by name" is necessary, not sufficient.** The sixth row above was checked
against all three apps and still went in wrong, because the unit that varies is not always the
app: `text-align` reaches MyMail's two controls by two different routes, so a per-app answer
could not be right for both. **Check each property against each control**, and when a claim is
about the repos' tooling rather than their CSS — the seventh row — the unit is the file, and
the only check is opening all three.

**The ninth row is that same refinement, violated by the person who had just written it.** The
claim was about the app repos' own documentation, checked by grepping one filename —
`web/AGENTS.md` — across all three repos. Three repos, dutifully, by name. But the claim lived
in four places spread over root, `web/` and `e2e/` files, so **the axis that was fully covered
was the one that did not vary, and the axis that varied was not swept at all.** It was caught by
someone re-running the same grep wider.

So the operative question is not *"did I check all three?"* but:

> **What is the unit this claim ranges over — the app, the control, the property, the file? —
> and did my search cover that unit, or just the one I happened to iterate?**

A search that iterates the wrong axis produces a *thorough-looking* negative. Three repos
checked reads as more careful than one, and here it was the shape of the mistake.

#### The number you explain away is the finding

The eighth row is the one to study, because nothing above would have caught it and the evidence
was in plain sight. Its author measured the errors-in-tests split for two repos, got zero from
both, and reported it of all three — having taken the third's *total* but never its breakdown.

**The totals did not match: 100 against 96.** That four-error gap was noticed and explained, as
*"MyCal's 100 differs only by its extra spec files"* — a guess with the grammar of a finding.
The four errors it dismissed were the whole discovery, and one of them sat on the exact line of
the reference suite whose own comment warns against measurements that fall through to a
meaningless pass.

So, as a check that is cheap and would have fired here:

> **When two measurements of the same thing differ, the difference is a result, not an
> irregularity to be accounted for.** If you find yourself composing a reason why one number is
> larger, stop and measure the gap instead. The explanation costs a sentence; the measurement
> costs a command; only one of them can be wrong.

This is the same shape as `spec/measurement-protocol.md`'s *"cross-check your numbers against
each other, not only against expectations"* — a run there was caught by two of its own figures
contradicting each other. The addition is the failure mode when you *do* notice: **noticing and
rationalising is worse than not noticing**, because it converts an open question into a settled
one and leaves no trace that anything was ever unresolved.

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
| "the `pipefail` bug is live in all three scripts" | writing the section on evidence discarded by a pipe |
| "MyMail removed its `trap … PIPE` line" — read off a `grep \| head -3` that cut the file at line 51 | **the same sitting as writing "do not conclude from a stream you paginated"** |
| "the cross-repo check predates MyCal's suite" — backwards; it postdates it by 26 minutes | correcting a *different* false claim in the same sentence — **and caught before shipping, by its own author** |
| `spec/app-logo.md` §3.3 explaining its extent rule with raw `getBBox()` *width* figures under a table headed *"larger axis, stroke/ink-inclusive"* — two statistics that differ by 8.3 points for MyMail | **writing the qualifier three paragraphs below that says every figure reported against that rule must name which box it is** |

**Freshly written text is the least reviewed text in any changeset**, and it is least reviewed
precisely when the author is concentrating hardest on some other failure mode. So the practical
form is not "be careful" — it is: **re-read what you added last, against the code, after you
have finished the thing you were concentrating on.** The sentence you are most confident in is
the one nobody has checked, including you.

**Only two rows were caught by their own author, and how each was caught is the useful part.**
Every other entry was found by someone else reading the primary source, which is the pattern the
rest of this document rests on.

**The `predates`/`postdates` row** was found because its author checked a claim that *felt
obviously true* and needed no checking — the ordering of two commits, in a sentence that did not
depend on the ordering at all. It was backwards.

> **Inside a correction, check the incidental facts too — especially the ones you did not stop
> to doubt.** The claim under repair gets scrutiny by definition. The scaffolding you write
> around it does not, and it is where the next defect goes.

The sentence was then rewritten to make no claim about the ordering, since it never needed one.
**That is the better repair**: an unnecessary fact that has to be right is a liability with no
upside, and deleting it beats verifying it.

**The `app-logo.md` §3.3 row is the first one caught by this section's own prescribed remedy** —
*re-read what you added last, against the source, after you have finished the thing you were
concentrating on* — rather than by luck or by a second person. That is the first evidence the
remedy works on its author, and it is a different claim from another instance of the disease.
Two things about it are worth keeping:

- **The defect was in the explanation, not the rule.** The rule was right; the paragraph
  illustrating it quoted the wrong statistic. Scaffolding again, exactly as the blockquote above
  predicts.
- **Adding this row broke the sentence you are reading.** It opened *"the last row is the only one
  an author caught themselves"* — a **positional** reference, correct when written and falsified
  by appending to a table above it. Repaired by naming the rows instead of their position, which
  is the durable form: a reference that depends on where something sits is one insertion away from
  pointing at the wrong thing, and nothing checks it.

  **Two more were already broken, and finding them is the whole argument for the durable form.**
  Sweeping this section for the same shape turned up two further *"the last row"* references that
  had gone stale before this changeset: one describing the `background`-declaration case and one
  describing the hover-fill floor, **neither of which is the last row of either table in this
  section.** Both now name their case. *(What is not claimed: exactly when each broke. The
  descriptions were matched to their cases and the positions checked; the history was not, and an
  unverified account of how they got that way is the thing §3.2 keeps warning about.)*

  So this is not a hazard the section merely predicts — it had already happened twice, here,
  unnoticed, in the document that teaches it. **A positional reference is a claim about a
  neighbour's position, and appending is the one edit nobody thinks of as a change to anything
  above it.**

**And the sharpest case is the `background`-declaration row, which is why its wording is
specific.** That claim was
not merely written while its author was distracted — it was written *as the replacement for a
clause just deleted for being wrong*. The old text said MyCal's fill "vanishes"; the new text
made a claim about which element paints, and attached it to the wrong rule. mynotes-dev's
form: **the most dangerous text in a correction is the correction itself, because it is the
part that has been reasoned about most recently and therefore feels most settled.**

So the re-read pass matters most on exactly the changesets that feel safest — the ones whose
purpose was fixing something. A correction inherits none of the scrutiny that found the defect
it replaces.

The hover-fill-floor row adds a mechanism, because "check all three" did not catch it. The figure
was taken from a per-app table that had just been read, and **the value appearing in two of three
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

#### The condition can live in another repository, and the waking commit can be in a third

The specimen above is contained: MyCal's dead rule was woken by a change in MyCal. **This section
was written around that shape, and it is not the only one.**

MyNotes' `e2e/tests/sidebar-footer.spec.ts` asserts `expect(column.width).toBeCloseTo(420, 0)` —
pinning a sidebar width that `spec/sidebar-footer.md` §6.4 states in as many words is **not part
of that contract**. It had been wrong the whole time and it had cost nothing, because **the suite
sat on a branch nothing executed.** That was the condition, and nobody had written it down,
because nobody had noticed there was one.

Then the branch was pushed, and this repository recorded the fact in `ac77d55`. Between
mynotes-dev's feasibility report and the human's ruling to widen that very column, the assertion
stopped being a file and became a **publication gate**.

> **Nobody changed that line. What changed is what it costs.**

Three things generalise, and the third is the one that has no owner:

- **The harmlessness condition was in another repository** — "nothing runs this suite" is a fact
  about MyNotes' CI, not about the file holding the defect.
- **The commit that fired it is in a third place.** `ac77d55` is in *this* repository and touches
  no app repo at all. It only wrote down that a capability had become real.
- **Recording a capability has a blast radius.** §3.5 says a commit that builds an X must sweep
  every document that ever said there was no X. **The sibling rule: a commit that records a
  capability becoming real must sweep everything that was safe only while it was not.** Those are
  different sweeps. The first looks for stale *claims*; the second looks for dormant *defects* —
  and the second is harder, because nothing in the affected repositories mentions the capability
  by name.

So when you record that something now runs, now gates, now blocks, or now checks: **ask what was
previously getting away with something.** A guard that starts running does not only start
catching real defects. It starts charging for the ones that were already there.

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

### 3.4 Moving text can introduce a defect without breaking anything

*(Owed to mymail-dev, which found this in its own repo while doing the move.)*

Splitting a document is the safest-looking edit there is: nothing is added, nothing is deleted,
the diff is a cut and a paste. It has a failure mode that no reference check will find.

**The specimen.** MyMail's root `AGENTS.md` described `-init` in two places. The Operating Modes
table said it seeds an *"optional initial identity"*. A bullet further down — inside the E2E
section being moved out — said `-init` *"itself requires `-identity-address`"*. The bullet was
right: `./mymail -init` without it exits 1 with `error: -identity-address is required`. **The
correct statement was in the text being moved, and the wrong one stayed behind.**

So a faithful, careful move *introduces* the defect — not by breaking a reference, but by
**deleting the copy that happened to be right and leaving the copy that was wrong.**
(mymail `84683bc`; the table has since been corrected.)

**This is not §3.1, and the difference decides the audit.** A dangling reference leaves a
pointer aimed at nothing, which is *visible* — anyone who follows it finds the hole. Here every
reference still resolves, perfectly, to a statement that is false, with the true version removed
by the same commit. **Nothing dangles, nothing is unreachable, and the diff reads as tidying.**
The repository is quietly less correct than before and nothing anyone runs will say so.

Hence the procedure, which does not follow from §3.1 and has to be stated separately:

> **Grep the origin file for the *fact*, not for the *pointer*.**

Every worker in this batch grepped for pointers, because that is the obvious audit and it is
what they were asked for. It passes cleanly here: no reference broke.

And the observation that makes it more than a caution:

> **A redundancy is also a disagreement nobody has had to resolve yet, and a move picks the
> winner silently.** The duplication was load-bearing *precisely because it was inconsistent* —
> while both copies existed, a reader had a decent chance of hitting the right one. The move
> removed that chance, in the direction nothing checks.

**This repository is more exposed to it than the app repos are**, which is why it sits here
rather than in §4. §3's duplication bullet says in as many words that several rules are stated
in more than one file *deliberately* — the three-repo rule in `README.md` and `spec/README.md`,
the measurement warning and the stale-numbers lesson in `measurement-protocol.md` — and that
"the canonical statement is the longest one". That rule settles which copy **wins**. It says
nothing about which copy is **right**, and those come apart the moment the copies drift. So
before consolidating any of them, diff the copies against each other rather than picking the
longest and moving on.

#### The audit itself can return a clean-looking nothing

The procedure above is a search, and **a search reports on your pattern before it reports on the
repository.** Two ways it produced confident false negatives in the same week as the move
described above:

- **Wrong axis.** A claim about the three repos' documentation was checked by grepping one
  filename, `web/AGENTS.md`, across all three. The claim lived in four files spread over root,
  `web/` and `e2e/`. Three repos, dutifully, by name — and the axis fully swept was the one that
  did not vary. (§3.2's refinement, arriving in the audit rather than in a rationale.)
- **Wrong vocabulary.** A sweep for repos claiming their suite "gates publication" matched
  `gates publication|gate publication|gating publication`, and reported that MyCal made no such
  claim. MyCal says it twice, writing **"gates publish*ing*"** — so the pattern was incapable of
  returning the hit it was run to find. That one **inverted** a finding: the conclusion drawn was
  that care had failed in the reference repo, when the reference had the careful version and the
  other two had not inherited it (`spec/sidebar-footer.md` §9.1).

So, on top of "grep for the fact, not the pointer":

> **Before publishing "repo X does not say Y" on the strength of a search, run it a second way**
> — a synonym, a stem, the noun instead of the verb, a wider file set — or open the place the
> claim would have to live and read it.

The tell is that you are about to assert a **negative** from a **search**. Positives are
self-verifying; the hit is right there. Negatives are only as good as the axis and the vocabulary
you guessed.

`spec/measurement-protocol.md` § *the gap read as the answer* is the canonical statement, and it
is worth reading rather than summarising here: it establishes that this and truncation are **one
mechanism**, not two — in both, a tool returns a well-formed result that is silent about what it
left out, and the gap is read as the answer.

**What actually corrected both of these was somebody searching wider than they were asked to.**
Handed two locations each, MyMail's and MyNotes' agents independently swept their whole repos
and found three more and seven respectively — MyNotes' fix spans its workflow, three `AGENTS.md`
files, `spec/REQUIREMENTS.md`, its Playwright config and the spec file itself. A narrow brief is
not a licence for a narrow search, and the person who widens it is doing the audit the brief
should have asked for.

### 3.5 "There is no X" goes false without an edit, and has no owner

*(Owed to mymail-dev.)*

Every rule above assumes a false claim entered the repository in a changeset — so a reviewer, a
grep or a re-read has *something* to be run against. **A negative claim about tooling has no such
moment.**

**The first specimen.** MyMail's and MyCal's docs said *"there is no shared stylesheet and no
cross-repo test"*. Both were true when written and were falsified by `tools/check-contract.py`
landing — **with no edit to either file.** MyCal's had been contradicting itself ever since,
naming the script forty lines from where it denied one existed. So had `spec/sidebar-footer.md`
§10.7, in this repository, in the item that describes the script.

Why nothing catches it:

- **No diff contains it.** No changeset, in any repo, ever added a wrong sentence. Review has
  nothing to review.
- **A grep finds it only if you already suspect it.** This is the complement of §3.4: that section
  is about being unable to *find* a false claim; this is a claim with no event to search for.
- **It has no owner.** *"There is no X"* is an assertion about the whole world at a moment in
  time, made in a file that has no reason to be watching the repository where X will appear. §3.3
  is the nearest neighbour — a dormant defect whose harmlessness rested on a condition elsewhere —
  but §3.3's condition at least changes inside one repository.

What to do instead:

> **Write the qualifier that survives the thing being built.** *"No cross-repo test"* went false;
> **"no cross-repo test that runs automatically"** did not, and would not have even after the
> script landed. Prefer the form that names *why* the gap bites — nothing runs it, nobody owns it,
> it does not gate anything — over the form that asserts nonexistence.

And when you *do* build the X that some other file denies exists, **that commit's blast radius
includes every document that ever said there was no X** — including in the other repositories,
which is exactly the sweep nobody runs because the commit does not touch them. This repository is
where such a commit is most likely to happen and least likely to be swept for, because it is the
only one that owns cross-repo tooling.

Both of those were caught by an agent fixing something else, noticing the shape and thinking to
check its siblings. That is not a process, and it is the reason this is written down.

#### A second specimen, in this repository, and a purer one

§3 said *"No remote is configured. Commit locally; do not attempt to push … there is no URL to
give."* `README.md` said the repository was local-only. Both were true, and both went false the
moment a remote was configured — **an act that produces no commit in any repository.**

The `check-contract.py` case at least had a changeset somewhere, so a sweep had a place to start.
This one has nothing to diff, nothing to review, and no tracked file whose contents moved. It was
corrected only because the person who made the change said so, in as many words.

Two things it adds to the section above:

- **The blast radius was wider than the repository that changed**, exactly as predicted — and
  unevenly, which is the part worth checking rather than assuming. The false clause was here, in
  `AGENTS.md` and `README.md`; in MyCal's `web/AGENTS.md`, twice; and in MyMail's root
  `AGENTS.md` and `spec/REQUIREMENTS.md` (corrected in MyCal `2e68ef3` and MyMail `07d14cf`).
  **Not in MyNotes**, whose references name `../mysuite` by path and simply never say why — it
  needed no edit. That is this section's own advice arriving as evidence: the reference that
  asserted nothing about the world survived, and the two that explained themselves both aged
  into being wrong.
- **The bullet had named its own successor, and that did not help.** It ended *"When a remote is
  added, those references should be updated"* — a correct, specific, actionable instruction,
  addressed to a moment that arrives with no diff, no notification and nobody assigned. A
  conditional written into the claim it will invalidate is still only as good as somebody
  noticing the condition fired.

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
  section saying that these declarations are governed from outside the repo, and naming the
  *routine tidying* that breaks them silently: normalising
  `0.80rem` to `0.8rem`, folding the rule back into a shared button class, dropping a
  "redundant" `flex-shrink: 0` or `text-align: center`, adding a `font-weight` to the base
  `button` rule, restoring `outline: none`. Every one of those is a reasonable edit
  everywhere else in the same file.

  **It belongs in `web/AGENTS.md`, not the repo root**, for the same reason the rule exists:
  that file loads automatically when working under `web/`, and the CSS it guards is
  `web/static/app.css`. The root file is one level further from the edit. All three repos now
  place it that way:

  | | Where the warning lives |
  |---|---|
  | MyNotes | `web/AGENTS.md` §"The sidebar footer is governed from outside this repo" — **the model**: a distinctly titled section a reader can find and cite |
  | MyCal | `web/AGENTS.md`, as a bullet in a list — no title of its own, but the richest content of the three: it names each tidy-up alongside the assertion that catches it |
  | MyMail | split between the repo-root preamble and `web/AGENTS.md` |

  So "MyNotes is the model" is a claim about **findability, not coverage** — all three carry a
  form of this, and MyCal's says more. What MyNotes has that the others do not is a heading,
  which is what makes it citable from here at all.

  > **The citation above was stale from the day §4 was written**, naming MyNotes' root
  > `AGENTS.md` for a section that had moved to `web/AGENTS.md` in an earlier commit. That is
  > the §3.1 dangling-reference shape landing in the file that defines it — and on the one
  > citation a reader is most likely to follow, since §4 calls it *the* model. **The repair is
  > the path, not the placement:** anyone reconciling the two should move the citation, never
  > move the section back to the root to match it.

  This is the highest-value thing an app repo can add, because it is the only guard that fires
  **before** the change rather than after. All three repos' suites now run in CI
  (`spec/sidebar-footer.md` §9.1), which raises the floor but does not change that: a pipeline
  fires *after* the edit is written and pushed, and it catches only what it asserts. Neither it
  nor anything else catches an edit made for a good reason by someone who did not know the rule
  existed — `0.80rem` → `0.8rem` is uncatchable by any of the three (§9.2), and no suite sees
  between the repos at all. The prose is what fires first.
