# Shared contracts

Each file here defines one UI element or behaviour that MyCal, MyMail and MyNotes are
required to render identically. A contract is binding on all three apps or on none of them.

**"Binding on all three" is about what the contract *requires*, not about what has *shipped*
yet.** A contract being adopted can be binding while one app is still implementing it — that is
the state `app-logo.md` is in below, and it is transient by construction. What it must never
become is a standing per-app exemption, which is the thing the sentence above forbids. A status
A status naming an app as still adopting is a claim with a deadline; if you find one that has not
moved, that is the defect.

## Contracts

| Contract                                 | Covers                                                                                                                                           | Status                            |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| [`sidebar-footer.md`](sidebar-footer.md) | The light/dark theme toggle and Settings button at the bottom of the left sidebar — geometry, colours, interaction, and their position on screen | Binding, implemented in all three |
| [`app-logo.md`](app-logo.md)             | The app logo badge at the top left — its box, fill, glyph size and extent, placement, and accessibility. **The app-name label beside it is deliberately out of scope** (`app-logo.md` §2) | Binding. Shipping in MyCal and MyMail; **MyNotes implemented and measured on an unmerged branch** |

## Cross-cutting

| Document                                             | Applies to                                                                                                |
|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| [`measurement-protocol.md`](measurement-protocol.md) | Every contract. How to verify a change to shared UI, and why a green build proves nothing about geometry. |

## How a contract is written

Each contract document states, in this order:

1. **What it covers**, and the local selector, class and file names each repo uses for it.
   Names are per-project; only behaviour is shared.
2. **The mandated values**, as resolved values — pixels, resolved colours, computed
   properties. Not token names.
3. **Which mechanisms are mandated and which are local.** Most of the time only the
   observable result is specified. Where a specific technique *is* the contract, the
   document says so explicitly and says why.
4. **Known gaps and open items**, honestly. Including what is unverified, what is deferred,
   and what is accepted as a residual risk.
5. **Withdrawn rules**, so that nobody re-derives a superseded rule from an old comment.

That last section is not ceremony. Values here have been revised more than once, and a rule
that was withdrawn tends to survive in a comment somewhere long after the code has moved on.

## Adding a contract

Say in the file which repos implement it and which do not yet. A contract nothing implements is
a proposal — mark it as such in its status line rather than writing it as though it were
binding.

**Then register it in every place that enumerates contracts. There are four, and this file is
only one of them:**

| Where | What to add |
|---|---|
| **`spec/README.md`** (here) | a row in the table above |
| **`AGENTS.md` §1**, *"Currently binding"* | a bullet — this is where an agent is told to start |
| **`README.md`**, *Contents* | a bullet under `spec/` — this is where a person starts |
| **`tools/check-contract.py`**'s caveat block | whether the new contract is checked. If it is not, **say so** — the block prints on every run and a green run otherwise implies coverage that does not exist |

And in the app repos, per `AGENTS.md` §4: each needs a short titled section in its
`web/AGENTS.md` saying the new element is governed from outside the repo, naming the routine
tidying that would break it silently. That is the only guard that fires *before* the change.

> **Why this list exists, and it is not bookkeeping.** This section used to read, in full:
> *"Add the file, add a row to the table above."* Someone followed it exactly — and produced a
> repository whose newest binding contract was reachable from **neither** `AGENTS.md` nor
> `README.md`, the two files every reader is pointed at first. Nothing dangled, no link broke,
> no check failed, and there was no event to grep for. It was found by a reviewer, not by any
> rule.
>
> **A checklist that is correct and incomplete is worse than no checklist, because following it
> feels like sufficiency.** The old sentence was accurate about this file and silent about the
> other three, and silence in an instruction reads as *"that is all there is"*. So when you add
> a step here, ask what else would have to change and name it — or say explicitly that nothing
> else does.
