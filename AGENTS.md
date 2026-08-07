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
  the model, and is currently the only automated guard any of this has.
- If it cannot be tested, **say in the comment that it is a reading rather than a contract**,
  and say what it was read on. Text measurements are per-platform and per-font.
- When you write a number down, write its conditions with it. "29.2px" is a claim that stops
  being true when a reader changes their browser font; "29.2px at the default 16px root font
  size" stays true.
- Do not describe history that is not in the repository's history.

---

## 3. Working in this repository

- **Markdown only.** No build system, no CI, no package manager, no dependencies. Nothing to
  run and nothing to install.
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
