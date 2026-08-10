# Measurement protocol

**Applies to every contract in this repository.** Read it before reporting any measured
number.

Every wrong number in the history of these contracts came from measuring something other
than the code that was just written. This protocol exists to make that impossible rather
than unlikely.

---

## Why a green build proves nothing

All three apps embed `web/static/` into the Go binary with `//go:embed`. A running server
keeps serving the CSS and JS it started with. So:

- `./build.sh` alone changes nothing the browser sees.
- A restarted server with a stale build serves the *previous* assets.
- The test suite passes or fails against assets that are not the ones you edited — and it
  does so **silently**, with no error anywhere.

Tests being green tells you the code compiles and the assertions hold against *something*.
It says nothing about whether that something is your change. Geometry in particular is only
ever established by measuring a rendered page.

### This has been demonstrated, not just asserted

The claim above is easy to nod along to and easy to under-rate, so it was reproduced on demand
— both paths run side by side, in the same state, in MyCal:

1. Server started; `web/static/app.css` then edited **without rebuilding**, so the served
   stylesheet no longer matched disk. Confirmed by `md5sum`, not assumed.
2. `playwright test tests/sidebar-footer.spec.ts` — which is exactly what `npm test` execs, its
   `test` script being a bare `playwright test` — reported **26 passed**, against assets that
   were not the ones on disk.
3. `./test-e2e.sh`, in that same state, **refused**: exit 1, *"Something is already listening on
   port 8089."*

**Twenty-six green assertions describing a stylesheet nobody was editing.** Nothing was broken,
nothing errored, and no output anywhere hinted that the file under test and the file on disk had
diverged.

The two paths differ by which one *manages the server*. `npm test` attaches to whatever is
already listening; `test-e2e.sh` builds, starts its own, and compares served bytes against disk.
So: **run the suite through the script, and treat a bare `playwright test` against a
long-running server as unverified**, however green. *(Demonstrated by mycal-dev. The numbers are
its readings; the two commands' behaviour is checkable in any of the three repos.)*

> It caught itself mid-measurement, which is worth keeping: the first attempt read
> `test-e2e.sh`'s exit code through a pipe into `tail` and got the *pipeline's* status, printing
> "exit: 0" next to a refusal message. See *the gap read as the answer* below — the apparatus
> reading reassuring, in the act of demonstrating apparatus that reads reassuring.

**This applies to CI exactly as it does locally.** A pipeline that starts a server from
anything other than the binary built in that same job has the identical trap, and it is worse
there: nobody is watching, and a green pipeline is trusted more than a green local run. If you
wire one of these suites into CI, build and serve in the same job, from the same artefact.

**And wire it in suspiciously.** Every failure this protocol exists to catch — the stale
server, the stale database, the probe asserting against an element that does not exist —
produced a *reassuring* result, not a red one. A pipeline does not remove that risk; it
removes the person who might have noticed. So make the pipeline prove its own freshness
rather than assume it: run the md5 served-vs-disk comparison and the sentinel check (steps 3
and 5) as pipeline steps, and fail the job on them. A suite that cannot demonstrate it is
measuring the build under test is not evidence, however green it is.

### Prove a new guard fails before trusting it

Freshness and sensitivity are separate properties. A pipeline can measure exactly the right
build and still hold assertions too weak to notice a real violation — and that combination is
the worst possible outcome, because **a guard that would stay green through a breakage is
worse than no guard: it looks like coverage.** Everything downstream then rests on protection
that does not exist, and nobody re-checks a thing that is passing.

So a guard is not accepted when it goes green. It is accepted when it has been **shown to go
red for the right reason**:

1. deliberately break a value the guard is supposed to pin;
2. **confirm the break actually took effect** — see below;
3. confirm the run fails, **and that it fails on that assertion** rather than incidentally —
   a job that errors for an unrelated reason has told you nothing;
4. revert;
5. confirm it is green again.

> **Step 2 is not bookkeeping, and it was added because a run came back green for the wrong
> reason.** mycal-dev mutated `.brand-reload-btn` by *prepending* `padding: 20px` to the rule —
> and the rule's own later `padding: 4px` overrode it, so **nothing changed on the page.** The
> suite was green because there was nothing to catch. Re-done as a replacement, the same
> mutation goes red at the expected value.
>
> **A mutation that does not mutate is indistinguishable from an assertion that does not fire,
> and both produce a green run.** *(mycal-dev's formulation.)*
>
> **The same shape, one level up, in the check that verifies your citations.** mynotes-dev-b's
> first citation sweep reported **all eleven sections MISSING** from a document that contained
> every one of them. The pattern required a dot after the section number, and subsections do not
> carry one. **A clean negative produced entirely by the pattern** — on the document that warns
> about exactly that, while checking citations *to* it.
>
> Both belong here rather than in a contract, and they are one family with §*"the gap read as
> the answer"*: **a check can fail in the reassuring direction, and it does not announce that it
> has.** An inert mutation, a pattern that cannot match, a stale server — each returns a
> well-formed result that is silent about what it could not see. **Before believing any negative
> from a tool you wrote, make it produce a positive you already know the answer to.**
>
> **And note which direction the instrument failed in, because only one of the two is
> self-correcting.** A sweep for dead cross-repo links classified a path as a markdown link
> target with a substring test — and a correctly written prose path `../mysuite/…` is a substring
> of the link target `../../mysuite/…`, so every correct prose path was resolved from the wrong
> anchor and reported **dead**. Exact set membership fixed it: 12 DEADs became 6. *(mycal-dev,
> who had already self-tested the section-number pattern against four known-existing citations
> before trusting a zero — the rule above worked, and a different mechanism got them anyway.)*
>
> **That one failed in the *alarming* direction, and that is the only reason it was looked at
> twice.** A tool that cries wolf gets investigated; a tool that reports all-clear does not. Both
> are the instrument answering confidently, and the rule above protects you from exactly one of
> them. **Distrust a clean negative on principle; distrust an alarming positive on inspection.**

#### Say which ref — and know that one class of ref is itself a stale local artefact

Naming the ref a measurement was taken at is necessary and is not sufficient, because refs are
not all the same kind of thing:

> **`origin/…` is not the remote. It is a local cache of what this checkout last heard from the
> remote, and without a successful fetch it is an unverified claim with no timestamp.**
> *(mycal-dev's formulation.)*

`main` names a commit that exists in the checkout in front of you. `origin/main` names whatever
that checkout last recorded, which may be minutes or weeks old, and **a sandbox that cannot reach
the remote will report it with no indication that it could not check.** In this round every
`origin/main` was a cache written by a fetch earlier the same day — knowable only by reading the
mtime of `.git/FETCH_HEAD`, which no git command volunteers.

The consequences are practical:

- **"N commits ahead of `origin/main`" is a claim about the cache**, not about the remote. It is
  the right figure for *"is this published?"* only if the cache is fresh.
- **A commit hash is worth its perishability only when a reader can resolve it.** A hash for a
  local-only commit costs the reader a failed lookup and tells them nothing they could not have
  been told in words. Prefer *"measured at a named local commit, unpushed"* and add hashes later,
  against refs somebody has verified.

This is the filesystem-versus-repository distinction the rest of this document draws for *files*,
arriving on *refs*: in both cases the tool answers confidently about the state it can see, and
says nothing about the state you meant.
>
> This is the same failure this document is otherwise about, arriving on the guard instead of on
> the page: the apparatus answering confidently **in the direction of a pass**. A stale server
> makes a test pass against assets you did not edit; an inert mutation makes it pass against a
> page you did not change. Assert the mutated state — read the value back, or measure the thing
> the mutation was supposed to move — before believing the green.

Until that cycle has been run, the honest description of a new guard is "added", not
"covering". **Do not upgrade a claim of protection on the strength of a first green run.**

#### Announce a mutation harness before you run it, if anyone else reads the same tree

The cycle above deliberately breaks a value and restores it. That is correct in isolation and
has a cost the moment a second reader exists:

> **When several agents share a checkout tree, one agent's mutation testing is indistinguishable
> from another agent's defect.** *(mycal-dev's formulation.)*

Those reds are **correct, reproducible in the moment, and about nothing.** In one afternoon this
produced three separate red cross-repo runs that were investigated as possible drift, and a
fourth that a reader guessed at and, reasonably, declined to raise. Every one was somebody
testing their own guard. A harness that reverts cleanly via a `trap` on exit is *invisible from
outside*, which makes it worse rather than better: the evidence is gone by the time anyone asks.

So: **announce it where the other readers are, before it starts** — not afterwards, and not only
in your own report. This is cheaper than scheduling discipline and it composes with the
ref-scoped run rather than replacing it: **the ref-scoped run tells a reader what they measured;
the announcement tells them why the working tree disagrees.** Do both.

*(`tools/check-contract.py`'s caveat block carries the reader's half — how to materialise each
repo's ref with `git show` and run against that instead of against whatever is on disk.)*

**This applies to the freshness checks themselves.** A reviewer pointed out that another
process squatting on the test port would defeat the served-vs-disk check, so a process-liveness
check was added using `kill -0` — and then an actual squatter was started to test it. **It
passed: 48/48 against the wrong server.** An exited background process is a zombie until
reaped, and `kill -0` succeeds on a zombie, so the check returned "alive" in precisely the case
it was written for. Replaced with a pre-flight port probe, re-tested against the same squatter,
now fails loudly.

A guard shipped that did not guard, and it was caught by *testing* the guard rather than
reading it. That is the third time in one week the apparatus produced the reassuring answer for
the wrong reason — and the reason to require "demonstrate red" rather than "demonstrate wired".

State the scope precisely, too. If part of a suite cannot run in the harness, the accurate
claim is narrower than "this app is covered" — say which assertions run and which do not.
Writing the narrow version once beats writing "covered" and correcting it later.

---

## The protocol

Run all five steps, in order. Steps 3 and 5 are the ones that catch the failure the other
three miss.

### 1. Fresh build

Run the project's full build (`./build.sh`), not just `tsc` and not just `go build`. The
TypeScript compile and the Go embed are separate steps and both feed the served assets.

### 2. Fresh server

**Stop the running server and start a new one.** Not a reload, not a signal — a new process.
The old binary holds the old `web/static/` in its own image.

### 3. Confirm what is served matches what is on disk — including the compiled JS

```bash
curl -s http://localhost:<port>/app.css | md5sum
md5sum web/static/app.css
```

The two must match. **Then do the same for the compiled JavaScript**, not only the CSS.
`tsc` output is embedded by the same mechanism and goes stale the same way, and markup
changes — the stacked label spans, an element type, an icon size — live there. Checking only
the stylesheet is the most common way to half-verify a change.

### 4. Navigate with the cache busted

Load the page with a cache-busting query string, or with the browser's cache disabled. A
correct server serving correct bytes still loses to a browser that never asks for them.

### 5. Assert on a sentinel that must have changed

Pick a value that **must** be different if your change is live, and check it before
believing any other measurement. A new padding, a changed colour, an added declaration — the
sentinel is not the thing you are measuring, it is proof that you are measuring the new
build at all.

If the sentinel still reads its old value, every number in that session is worthless. Go
back to step 1.

---

## Vary content volume — the dimension that was missing

**A layout measured only at rest has not been measured.** Vary how much content the app is
holding, not just the window size, theme, route and root font size. At minimum: empty, a
typical amount, and **more than the container can display**, so that every scrollable region
is actually scrolling.

This is not hypothetical. Three apps reported a combined 100 passing measurements of a
footer's on-screen position across window sizes, themes, routes and root sizes. Every one of
those runs used a dataset small enough that the sidebar never scrolled. With a realistic
number of items the footer scrolled away with the content and its distance from the window's
bottom edge went from 8px to **−1052px** — the controls were pushed off-screen entirely.

Nothing in the protocol as it stood would have caught that. All 100 numbers were correct and
the build was broken.

So when a contract specifies a position, a size, or anything that could be affected by a
scroll container:

- Load enough content that **every** scrollable ancestor actually scrolls, and re-measure.
- Check the empty case too — it is the one seed data usually gives you, and the one least
  like real use.
- Say in the report **what content volume each number was taken at.** A position measured at
  zero items and a position measured at forty are different measurements.

If a measurement is invariant across content volume, say that explicitly — it is a stronger
claim than the number itself, and it is the claim the reader actually needs.

### Assert that the overflow case actually overflowed

**A run that measures nothing and a run that measures a pass look identical**, unless you
assert on the intermediate state. Loading more content is a setup step, not evidence — prove
the setup worked before believing the result.

This nearly went wrong in practice: a first overflow run reported **zero scrolling regions**
and was almost recorded as a pass. The probe was silently returning "missing" because the
build under test was a demo build with no Settings control, so it had found nothing to
measure and said so in a way that read like success.

*(That is history, and the fact behind it has since reversed: MyNotes renders Settings in a
demo too — `spec/sidebar-footer.md` §10.9, which has the ref this is true of. Kept as written,
because the lesson is about what a probe reports when it matches nothing, not about which build
lacked a control. **The specimen would no longer reproduce; the failure mode is unchanged.**)*

So assert the precondition, with numbers:

- **content height vs container height**, both stated — e.g. 5749px of content in a 367px
  box, and 8549px in a 210px box at a 24px root;
- **that each scroll container reports itself scrollable** (`scrollHeight > clientHeight`),
  rather than inferring it from having loaded a lot of items;
- **that you scrolled to each extreme** and measured at both, since a sticky element behaves
  differently at the top and bottom of its range;
- **that the element you are probing exists at all.** A selector that matches nothing returns
  a falsy value, and a falsy value compared against an expectation frequently reads as a pass.

This is the same shape as the stale-server trap and the soft-assertion trap: in all three the
apparatus reports success while measuring something other than what you intended.

**A guard clause is the commonest form of it.** One overflow probe was written as
`if (lists.length) { … }` — with no lists found, the body never ran, the probe returned no
failures, and the run reported a clean pass having stressed nothing. Make the guard an
assertion instead: if the thing you meant to measure is absent, that is a failed run, not an
empty one.

**The general form: a negative assertion must distinguish "absent" from "could not look."**
Both look like success and only one is. Three instances of this one shape, all from this
work:

    if (lists.length) { … }                 no lists found → body never ran → clean pass
    kill -0 "$pid"                          succeeds on a zombie → "server alive" → 48/48
                                            against the wrong server
    ! cmd | grep -q "still-running"          cmd fails → grep matches nothing → "finished"
    @import url("…");  .rule { … }          parser merged the two → dropped the rule →
                                            checked nothing and reported agreement

The third was a watcher polling for a background job to end; a transient failure of the
listing command was indistinguishable from the job having finished, and it reported
completion while the job ran on. Whenever you write "if X is not there, we are fine", ask
what happens when you simply could not see X — and make that a third outcome, not a silent
merge into the reassuring one.

### The worst place for this failure is inside a guard

The fourth line above is the one to dwell on. A CSS parser accumulated a selector without
resetting on a top-level `;`, so `@import url("…");` merged into the rule that followed and
that rule was dropped. It was live, and it was discarding a real rule from a real stylesheet
on every run.

What makes it different in kind from the other three is **where** it sat. It was inside the
cross-repo guard — the artefact whose entire purpose is to be believed when it is green. Had
a `:root` block followed that import, the whole palette would have vanished and every colour
comparison would have reported **fabricated agreement**: thirty green assertions, none of
them looking at anything.

**A guard that lies toward a pass is worse than no guard, because it removes the check that
would have caught the others.** Everything else in this document assumes something is
watching. When the watcher is the thing that is broken, nothing downstream can notice.

So a guard needs its own sensitivity proven, and re-proven as it changes — not its
correctness argued from reading it. That is what `tools/check-contract.py --self-test` is
for, and why the acceptance criterion above ("shown red for the right reason") applies to a
guard's own machinery and not only to the contract it polices. Applying the criterion to the
thing that applies the criterion is not circular; it is the only way the sensitivity survives
the next edit.

### The gap read as the answer — truncation and non-matching are one mechanism

The third line of that table is a pipe, and it is not the only way a pipe lies. **A truncated
or discarded stream is indistinguishable from a short one**, and the missing part is read as an
absence rather than as a gap in the instrument. This produced five wrong findings in a single
week's work, none of which involved a mistaken measurement — in each case the apparatus
measured correctly and the answer was thrown away, or never asked for, before anyone saw it:

| What was concluded | What actually happened |
|---|---|
| *"the `EXIT` trap does not fire on `SIGPIPE`, so the server survives"* | the probe printed its `CLEANUP RAN` marker to stderr and was run as `script 2>&1 \| head -1`. The trap **did** fire; its evidence went into the pipe `head` had just closed. With stderr to a file the marker appears. A defect was reported in three repositories on the strength of it, and there was none |
| *"`tsc` reports about 30 errors"* | the run was piped through `head -20`. The real count is 96 in the tree that was being measured — and 100 in MyCal's, so the figure is also per-repo |
| *"the server is serving a stale asset"* | an ad-hoc freshness loop written as `served=$(curl -sf "$url" \| md5sum)` **without `pipefail`**: a pipeline's exit status is its last command's, so a 404 left `curl` failing silently and `md5sum` hashing empty input. It reported a stale asset where the truth was a missing one |
| *"MyMail removed its `trap … INT TERM PIPE` line"* | the comparison was `grep -n 'trap ' test-e2e.sh \| head -3`. MyMail's second `trap` is on line 69 and its comment block is long, so the three lines returned were the first `trap` and two comment lines. **The line was there.** Reported to a colleague as a state change; corrected by them re-reading the files |
| *"MyCal never claims its suite gates publication"* | the sweep matched `gates publication\|gate publication\|gating publication`. MyCal writes **"gates publish*ing*"** — twice. The pattern could not match the word in use, so the search was incapable of returning the hit it was run to find |

**Those are not a family of related mistakes. They are one mechanism.** In every row the tool
returned a well-formed, clean-looking result that was silent about what it had left out, and
**the gap was read as the answer.** Truncation and non-matching are the same failure wearing
different clothes: nothing in the output distinguishes *"there is no more"* from *"I did not ask
for more"*.

That unification is worth more than the individual rows, because it covers the search-shaped
variant that a rule about pipes would miss:

> **A negative grep result is only as good as the pattern — and a phrase that varies by one word
> across three repos is not a pattern.** *(mymail-dev.)*

Note where the two halves differ in danger. `head` at least leaves a plausible trace: a
suspiciously round count, output ending mid-thought. **A non-matching pattern leaves nothing at
all** — clean exit, no output, and a result identical in every respect to the truth it is
misreporting.

**The last row is the one to study, because it inverted a finding rather than merely missing
one.** It produced a confident statement about *another repo's* cleanliness — and a wrong claim
about your own repo gets caught by you, while a wrong claim about someone else's is caught only
if that someone happens to read it. Here they did, and checked. That was luck, not process.
*(Framing owed to mymail-dev.)*

Of the rows above, the first two are the classic shape: the conclusion was the *reassuring*
reading of an absence — nothing printed, therefore nothing happened.

> **The fourth was committed by the author of this section, in the same sitting, about the
> subject of the first row.** Having just written "do not count, measure or conclude from a
> stream you paginated", I compared three scripts with a `grep` ending in `head -3` and reported
> a line as removed because it fell outside the window. It is the cheapest possible instance —
> one flag, on a command whose whole purpose was to establish presence or absence.
>
> That is `AGENTS.md` §3.2's mechanism operating at full strength: **freshly written text is the
> least reviewed text, and it is least reviewed precisely when its author is concentrating on
> the failure mode it describes.** Knowing the pattern by name did not help. What caught it was
> a second person reading the files.
>
> So the practical form is not *"remember this"*. It is: **a claim about what a file contains is
> checkable in seconds and should be re-derived rather than recalled** — including from your own
> notes, including when you are the one who wrote the warning, and **including when a colleague
> hands it to you already verified.**
>
> That last clause is the one that did the work here. The correction arrived with a table of all
> three files in it, already checked; what made the fix right was re-reading the files anyway
> rather than transcribing the table. Across this batch the pattern appeared five times among
> four agents, and **in every instance what caught it was a second person reading the primary
> source — never the author, and never the pattern being known.** Plan for the reader, not for
> the author's vigilance. *(Final clause owed to mysuite-manager-e2e, from two instances of its
> own.)*

**The third is here for the opposite reason — it is the one the apparatus already gets right,
and it was reintroduced by someone reimplementing it.** All three repos' `test-e2e.sh` open
with `set -euo pipefail`, which is precisely what makes their `curl … | md5sum` freshness
checks sound: with `pipefail` the failing `curl` propagates and the check reports a fetch
failure rather than a bogus hash. The instance above was a throwaway loop written alongside
them, by someone who copied the pipeline and not the `set` line, and it produced a
false "stale asset" report within minutes.

So the transferable point is not only *"watch your pipes"*. It is: **the protections in a
mature script are load-bearing and mostly invisible, and the moment to lose them is when you
reimplement a piece of it ad hoc to check something quickly.** A one-off probe is exactly where
nobody sets `pipefail`, and exactly where a wrong answer is most likely to be believed, because
it was written to answer one question and is not treated as apparatus at all.

So:

- **Never let a diagnostic share a stream with the thing being truncated.** If a probe's own
  output proves it ran, send it somewhere nothing is closing — a file, a different descriptor.
- **Do not count, measure or conclude from a stream you paginated.** `head`, `tail`, `grep -m1`
  and a scrolled-back terminal all produce a number that is a property of the pager.
- **In a shell pipeline, the exit status is the last command's** unless `pipefail` is set — so
  the failure of the step you care about is silently replaced by the success of the step that
  formatted it. All three `test-e2e.sh` scripts set it. **A quick one-off probe is where it
  goes missing**, and a one-off probe's answer gets acted on just as readily.
- Then ask the question this whole document keeps returning to: **if the thing I am looking for
  were there, could I see it from here?** An absence is only evidence when the instrument could
  have shown a presence.

This is the same failure as the stale server and the zombie liveness check, arriving through
the plumbing rather than through the system under test — and it is worth naming separately
precisely because the plumbing is the part nobody treats as part of the measurement.

**It predates this batch, and it has already changed a design here.**
`tools/check-contract.py` prints its verdict twice, once before its caveats and once after,
because a reviewer running the acceptance check on a `tail -20` landed in three screens of
epistemics and never reached the line saying whether it passed. The comment in that file says
so. That fix — ordering and repetition rather than fewer caveats — is the right shape for
output somebody will truncate, and it is worth copying: **assume the reader will see a window
of your output, not all of it, and put the verdict where any window catches it.**

### Know what your coverage expires against

Some properties cannot hide behind a dataset but can hide behind a case nobody visited. A
layout property measured across every route in the router's table is complete *as of that
table* — and a route added later is covered by nothing, while every existing route keeps
passing.

State what your coverage is complete *relative to*, and what event invalidates it. "All five
routes, as of the current route table" is a useful claim; "all routes" is one that quietly
stops being true.

## Measuring a backdrop: walk the ancestors, never read one element

Any contrast figure needs the colour *behind* the thing being measured. **Do not read that
off the element itself, or off the element you assume paints it.** Walk up until you find an
ancestor that actually paints:

```js
// The colour painted immediately behind an element. Walks up from the parent to
// the first ancestor with a non-transparent background-color.
//
// Always returns an object. When nothing paints, `backgroundColor` is null —
// check that field, not the object. `if (!resolveBackdrop(el))` is always false
// and would skip the very branch limitation 4 exists to make you handle.
function resolveBackdrop(el) {
  for (let p = el.parentElement; p; p = p.parentElement) {
    const bg = getComputedStyle(p).backgroundColor;
    if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
      return { painter: p, backgroundColor: bg };
    }
  }
  return { painter: null, backgroundColor: null };
}
```

Two agents arrived at this independently, from different repos, which is reasonable evidence
it is the right primitive. It is engine-level, not app-specific: only the starting selector
differs.

**Why not just read the element that paints it.** Because which element that *is* differs per
app and is not part of any contract. One app's footer declares a background; another's is
transparent and inherits from a panel two levels up. A test reading the footer's own
`backgroundColor` gets the right answer in the app whose footer happens to declare one, and
silently computes contrast against `rgba(0, 0, 0, 0)` everywhere else.

That is `sidebar-footer.md` §3.1 **in executable form** — right answer in this repo, wrong
method, and no way to notice from inside it. §3.1 is about CSS pins that one app's rendering
cannot defend; the identical trap applies to measurement code, and there it is worse, because
the wrong method produces a confident number instead of nothing.

### Limitations — state these wherever the walk is used

1. **`background-color` only.** A `background-image`, gradient, or shorthand carrying an image
   is not detected, and the walk goes straight past an element that visibly paints.
2. **Semi-transparent backgrounds are treated as opaque.** The walk stops at the first
   non-transparent colour; if that colour is `rgba(…, 0.5)`, the true backdrop is a composite
   and this returns the wrong one.
3. **It reports the painter, not the composite** — which is usually what is wanted, but if (2)
   fires, painter ≠ effective colour and every figure derived from it is wrong.
4. **`painter: null` is not "no backdrop."** It means the canvas, which is white by default —
   a different claim. Treat null as *could not determine*, never as a pass.
5. **Needs a real browser.** jsdom does no layout and does not resolve cascaded backgrounds
   usefully.

(1) and (2) are the ways it can be *confidently wrong*; the rest are ways it declines to
answer. Put those two in the output.

**Normalise before comparing.** Tokens are authored as hex (`#f9fafb`); `getComputedStyle`
returns `rgb(249, 250, 251)`. Comparing the two raw forms fails on formatting alone.

## Reporting measurements

State, every time:

- **The root font size** the measurement was taken at. Any number mixing `rem` and `px`
  means nothing without it.
- **The theme.** Light and dark are different measurements, not one measurement.
- **The content volume**, per the section above — including whether any scroll container was
  actually scrolling.
- **What the value was measured against** — for contrast, name the actual backdrop. Apps
  paint different colours behind the same control, so a ratio copied from a sibling repo is
  a wrong number that looks like a checked one.
- **Whether the number is a constant or a reading.** Anything derived from rendered text is
  a reading on one platform in one font (see `sidebar-footer.md` §2.4, §4).
- **Which state of the repository was measured** — a commit, or a working tree. See below;
  they are not the same claim, and only one of them is reproducible.

**The test for whether you have written enough:** *could somebody who does not already know
this figure find it by searching for what it is measured against?* MyMail's
`app.css:431` — *"`--primary` measures 5.169:1 on white and 3.991:1 on `#1f2937`"* — passes.
A bare `5.169:1` does not, and it fails for its own author too, six weeks later.

That test is what makes the operand rule below usable. Stating operands is not only about a
comment staying true; it is what makes the next change's blast radius **findable**. *(Owed to
mymail-dev.)*

---

## What has to be re-measured is set by the operands, not by the topic

When a change moves a value, every figure that value is an **operand of** is in scope — not
every figure on the same subject. Those are different sets, and the second one is the one
people naturally check.

`sidebar-footer.md` §5.5 is the witness. It gives contrast figures for the control border. A
change to the *backdrop* left it stale for weeks, through a review that checked every other
table in the file, because it reads as a section about borders. It was in scope because it
**names a backdrop as an operand**, not because it is about backdrops.

This is the same discipline as stating operands in a comment (see *Reporting measurements*
above), applied one step earlier — to deciding what to re-check. If a comment or a table says
what its number was measured *against*, then finding everything affected by a change is a
search rather than a recollection. If it does not, nothing can find it, including its author.

*(Formulation owed to mymail-dev, generalising from two retractions where the topic-shaped
search missed the operand-shaped one.)*

## A static check reads a working tree, and a working tree has no snapshot

Every freshness rule above is about a *running server* serving stale assets. A source-reading
check like `tools/check-contract.py` is immune to all of it — and has its own version of the
problem, which is worse in one specific way.

**It reads whatever is on disk at the instant it reads it.** A commit, an uncommitted edit and
a half-written file are indistinguishable to it. Across three repositories and several files
there is no atomic snapshot at all: the check can read one file before an edit and the next
file after it, and report on a combination that existed in no state anyone authored.

**This has already produced a result nobody could interpret.** While MyCal was mid-edit, a run
reported its dark resting label resolving to `#d1d5db` instead of the shared `#9ca3af` — the
right file, the right rule, and the exact place MyCal's own comment warns such a divergence
could appear. Three runs seconds later were green.

> **The first version of this section said that was a torn read, and it was not.** MyCal was
> mutation-testing its own guards and had deliberately collapsed a theme-scoped alias; the
> check had read a state that genuinely existed on disk and had reported it **correctly**.
> Reproduced afterwards on a scratch copy — deleting that one declaration produces that exact
> failure, that exact hex.
>
> So the check was right and the diagnosis was invented. **A mechanism nobody verified was
> written into the protocol as the finding's explanation**, when the ninety seconds of mutation
> testing that would have settled it were available the whole time — and were, in the end, what
> settled it. Corrected rather than amended away, because the failure being recorded here is
> mine and not the tool's.

The lesson survives the correction and is sharper for it. A red-once against a live tree can be
a torn read, **a real state somebody is deliberately creating**, or a genuine defect, and the
run itself cannot tell you which. What was wrong was not re-running — it was concluding
*"nothing was wrong"* from a green re-run, when the truthful conclusion was *"the state that
produced the red is gone."*

So, when a source-reading check goes red against a tree someone else is working in:

- **Re-run it before reporting.** Red-and-stable is a finding; red-once is a read. This costs
  seconds and is most of the mitigation.
- **Report what you saw, not what you think caused it.** *"Red at 18:04, green three runs
  later"* is a fact and is worth sending. *"That was a torn read"* is a hypothesis, and the
  above is what happens when one gets recorded as the other. If the cause matters, it is
  usually reproducible on a scratch copy in about a minute — do that instead of guessing.
- **A green run has the same exposure**, and is less likely to be questioned. That asymmetry
  is the reason to state which repository state was checked rather than only the result.

  **And the asymmetry is in the attention, not in the mechanism.** Re-running would correct a
  mid-write green exactly as well as a mid-write red — but nobody re-runs a green. So this
  mitigation covers the direction that gets scrutinised, and leaves the other one uncovered
  for a reason that has nothing to do with the tool. Reading a tree another agent is writing
  is unsound in both directions. *(Point owed to mymail-dev.)*
- **Say "green against an uncommitted tree" when that is what happened.** It is a weaker claim
  than green against a commit, and the check's own output cannot tell the two apart — so if
  the person reporting does not make the distinction, nobody downstream can.

The general form, and it is not confined to this script: **a checker that reads the filesystem
tells you about the filesystem, not about the repository.** Anything that has to hold about
*the repository* needs the state named alongside the result.

## Traps that have already cost time

**Chromium withholds `:focus-visible` from a programmatic `.focus()` when the last
interaction was a pointer.** A test that clicks a control and then focuses it is testing a
rule that is not applying. Press a key after any click to restore keyboard modality — and
assert `el.matches(':focus-visible')` so the test fails loudly instead of measuring nothing.

**A soft assertion can pass while measuring nothing.** `expect(boxShadow).not.toBe('none')`
passed against a focus ring that measured 1.28:1 — the indicator existed and could not be
seen. Assert the property that would actually fail: compute the composited contrast, check
the offset, check the width.

**Numbers in comments go stale the moment code moves.** Two of the three repos shipped
comments describing histories that had never existed in their own repository. If a number
matters, put it in a test. If it cannot be tested, say in the comment that it is a reading
rather than a contract.

**`scrollWidth` on an `overflow: visible` box is not a reliable overflow check.** Sum the
children's widths plus the gaps and compare against `clientWidth`.

**Seed data is not a test case.** Whatever the app ships for demos or development is one
arbitrary point in the input space, usually near-empty, and measuring only there means the
overflow behaviour of every container is untested. If you did not choose the content volume
deliberately, you did not choose it.

**Prove the reset — do not merely perform it.** A three-volume table was nearly reported as
three volumes agreeing, when the reset command was `rm mycal.db` against a database actually
named `mycal.sqlite`. Nothing was deleted; all three "volumes" measured the same 26 records.
Identical rows across volumes reads as *stronger* evidence than a single measurement while
being strictly weaker — it is one data point wearing three hats.

So: stop the server, **confirm the files are gone**, confirm the API reports the state you
intended, and then assert **in the browser** that the volume being measured is the volume you
meant. Make the run fail when the API's count and the rendered DOM disagree.

What caught that one was not the reset failing loudly — it failed silently — but **a number
that did not fit**: a "1 record" run claiming 369px of sidebar overflow, against a separately
measured single-record sidebar of 655/655 with no list rendered at all. Two of its own numbers
contradicted each other, so one of them was wrong. **Cross-check your numbers against each
other, not only against expectations.**

As it was put at the time: *there, a stale binary made a broken change look fine; here, a
stale database made an untested volume look tested. Both are cases where the measurement
apparatus lies in the direction of a pass.* That direction is the thing to notice — these
failures do not produce alarming results, they produce reassuring ones.
