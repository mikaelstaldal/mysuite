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
2. confirm the run fails, **and that it fails on that assertion** rather than incidentally —
   a job that errors for an unrelated reason has told you nothing;
3. revert;
4. confirm it is green again.

Until that cycle has been run, the honest description of a new guard is "added", not
"covering". **Do not upgrade a claim of protection on the strength of a first green run.**

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

The third was a watcher polling for a background job to end; a transient failure of the
listing command was indistinguishable from the job having finished, and it reported
completion while the job ran on. Whenever you write "if X is not there, we are fine", ask
what happens when you simply could not see X — and make that a third outcome, not a silent
merge into the reassuring one.

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
// Returns null when nothing paints — a distinguishable result, not a default.
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

---

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
