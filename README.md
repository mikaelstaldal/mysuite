# MySuite

Shared UI contracts for the MySuite apps: [MyCal](https://github.com/mikaelstaldal/mycal), 
[MyMail](https://github.com/mikaelstaldal/mymail) and [MyNotes](https://github.com/mikaelstaldal/mynotes).

Three separate applications, three separate repositories, three separate binaries — but one
product as far as anyone using them is concerned. Somebody with all three open in browser
tabs should be able to switch between them without the furniture moving.

This repository is where the parts that must match are written down, once.

## Why it exists

The three apps are built the same way — Go backend, Preact/TSX frontend compiled by `tsc`,
`web/static/` embedded into the binary with `//go:embed` — and they had grown several UI
elements that were *nearly* the same. Near-identical is worse than either alternative: it
looks like a single product until you compare two windows side by side, and there is nothing
anywhere that can tell you the three have drifted apart.

The first contract, the sidebar footer's theme toggle and Settings button, existed as prose
duplicated in three separate documents. Keeping three copies of a specification in sync by
hand is the problem this repository replaces, not a smaller version of it.

## What belongs here

**Belongs:** anything that is required to be identical across two or more of the apps.
Geometry, resolved colours, interaction behaviour, on-screen position, accessibility
guarantees, and the reasoning behind each — particularly where a value looks arbitrary or a
rule looks redundant.

**Does not belong:**

- Anything true of only one app. That belongs in that app's own `AGENTS.md`, or in its own
  requirements document where it has one.
- CSS class names, token names, or file layout. Those are deliberately per-project. What is
  shared is the *value*, never the name it is reached by.
- Application code. There is no shared stylesheet and no shared component library — the
  apps implement the contracts in their own CSS, with their own class and token names.

  There is one exception, and it is deliberate: **`tools/` holds scripts that check a
  contract.** A specification nothing can verify is a specification that drifts, and this
  repository is the only place a *cross-repo* check can live, because it is the only place
  that knows about all three apps at once. Such a script is a contract artefact — it will be
  read more often than it is run — and must stay dependency-free: no package manager, no
  network, no build step, nothing the app repos would have to adopt.
- Aspirations. A contract here is binding on all three apps; if something is a proposal,
  mark it as one in its status line.

## Who consumes it

| Repository | Path         |
|------------|--------------|
| MyCal      | `../mycal`   |
| MyMail     | `../mymail`  |
| MyNotes    | `../mynotes` |

Each references the relevant contract from its own agent instructions and requirements
documents rather than restating its values.

## Contents

- **[`spec/`](spec/)** — the contracts, one file each, indexed in
  [`spec/README.md`](spec/README.md). Currently two:
  - **[`spec/sidebar-footer.md`](spec/sidebar-footer.md)** — the theme toggle and Settings
    button at the bottom of the left sidebar. Implemented in all three apps.
  - **[`spec/app-logo.md`](spec/app-logo.md)** — the app logo badge at the top left.
    Implemented in MyCal and MyMail; **MyNotes in progress.** The app-name label beside the
    badge is deliberately out of scope, per that contract's §2.
- **[`tools/check-contract.py`](tools/check-contract.py)** — checks the three apps against
  the **sidebar-footer** contract only; the app-logo contract has no checker yet. Run it from
  a checkout with the app repos as siblings:

  ```
  tools/check-contract.py            # 0 agree · 1 disagree · 2 cannot check
  ```

  It compares source text and resolved tokens, never rendering, so it sees things no browser
  test can — and misses everything only a browser can. Every green run prints what it did
  not check; read that, because the accurate claim is narrower than the reassuring one.
- **[`spec/measurement-protocol.md`](spec/measurement-protocol.md)** — how to verify a change
  to shared UI. Applies to every contract.
- **[`AGENTS.md`](AGENTS.md)** — instructions for AI coding agents working in this repo or in
  any of the three app repos. (`CLAUDE.md` is a symlink to it, matching the convention the
  three app repos use.)

## Proposing a change

1. **Raise it before changing anything.** A value here is not a local decision, and the
   reason a value looks wrong is often written down a few lines below it.
2. **Read the contract's "Known gaps" section first.** Several of the obvious objections are
   already recorded there as deliberate, deferred, or accepted — including at least one that
   is genuinely a defect and is waiting on a decision.
3. **Measure, following [`spec/measurement-protocol.md`](spec/measurement-protocol.md).** A
   change proposed with numbers gets decided; one proposed without them gets re-measured
   first. Both a change and a decision to reject one need real numbers behind them.
4. **Land it in all three repositories, or in none.** This is the rule the whole repository
   exists to enforce.

### All three or none

A shared value changed in one app is not a partial improvement — it is a defect, and it is
the specific defect this repository was created to prevent. The three apps have no shared
stylesheet and **no cross-repo test that runs automatically**, so **nothing will detect the
divergence.** It will be found by a person noticing that a button moved when they switched
tabs, possibly months later.

(`tools/check-contract.py` can see cross-repo drift and is the only thing that can, but no
pipeline runs it — see `spec/sidebar-footer.md` §10.7. Each app's own e2e suite checks that
app alone.)

The same applies in the other direction. If you are working in one of the app repos and find
a shared value that looks wrong there, **do not fix it locally.** Raise it here. Whatever is
wrong is wrong in three places, and one person should decide it once rather than three people
fixing it three different ways.

A few rules — "all three or none", how to verify a change, and why numbers in comments go
stale — are deliberately restated across `README.md`, `AGENTS.md` and `spec/`, because a
reader may arrive at any one of those files and read only that one. `AGENTS.md` §3 says
which copy is canonical. That is the only duplication this repository accepts.

## Status

The remote is <https://github.com/mikaelstaldal/mysuite>; the three app repos are linked at the
top of this file.

Cross-references from the app repos name this one **by path** (`../mysuite`,
`spec/sidebar-footer.md`), because `tools/check-contract.py` and every relative link assume the
four checkouts are siblings. `AGENTS.md` §3 is the canonical statement of that, and of when to
give the URL as well.

## Licence

Copyright 2026 Mikael Ståldal.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
