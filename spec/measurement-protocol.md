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
