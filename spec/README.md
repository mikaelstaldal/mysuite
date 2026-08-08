# Shared contracts

Each file here defines one UI element or behaviour that MyCal, MyMail and MyNotes are
required to render identically. A contract is binding on all three apps or on none of them.

**"Binding on all three" is about what the contract *requires*, not about what has *shipped*
yet.** A contract being adopted can be binding while one app is still implementing it — that is
the state `app-logo.md` is in below, and it is transient by construction. What it must never
become is a standing per-app exemption, which is the thing the sentence above forbids. A status
of *"implementation in progress"* is a claim with a deadline; if you find one that has not moved,
that is the defect.

## Contracts

| Contract                                 | Covers                                                                                                                                           | Status                            |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------|
| [`sidebar-footer.md`](sidebar-footer.md) | The light/dark theme toggle and Settings button at the bottom of the left sidebar — geometry, colours, interaction, and their position on screen | Binding, implemented in all three |
| [`app-logo.md`](app-logo.md)             | The app logo badge at the top left — its box, fill, glyph size and extent, placement, and accessibility. **The app-name label beside it is deliberately out of scope** (`app-logo.md` §2) | Binding. Implemented in MyCal and MyMail; **MyNotes implementation in progress** |

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

Add the file, add a row to the table above, and say in the file which repos implement it and
which do not yet. A contract nothing implements is a proposal — mark it as such in its
status line rather than writing it as though it were binding.
