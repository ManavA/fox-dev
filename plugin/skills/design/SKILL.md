---
name: design
description: Deep-module design vocabulary and checks. Use when deciding an interface, where a seam goes, how to make code testable, or when recording an ADR or glossary term, even when the structure question comes up mid-task.
---

# Design

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface. This skill is a reference to consult, not a session to run. Use its terms exactly.

## Vocabulary

- **Module**: anything with an interface and an implementation, at any scale (function, class, package, service slice).
- **Interface**: everything a caller must know to use the module correctly: signature, invariants, ordering, error modes, configuration, performance. Wider than the type signature.
- **Depth**: behaviour a caller or test can exercise per unit of interface it must learn. Deep = small interface, much behaviour. Shallow = interface nearly as complex as the body.
- **Seam**: the place where you can change behaviour without editing that place; where the interface lives. Choosing it is its own decision.
- **Adapter**: a concrete thing that satisfies an interface at a seam (Postgres repo, in-memory fake).
- **Leverage**: what callers gain from depth. **Locality**: what maintainers gain: change and bugs concentrate in one place.
- **Contract**: the interface as callers actually rely on it. By **Hyrum's law**, every observable behaviour becomes part of it once there are enough callers.

## Checks

1. **Deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through. If it reappears across N callers, it earns its keep.
2. **Interface is the test surface.** Tests and callers cross the same seam. Wanting to test past the interface means the module is the wrong shape.
3. **One adapter is a hypothetical seam; two adapters make a real one.** Add a port only when something varies across it (usually production plus test).
4. **Classify each dependency** before deepening: in-process (merge and test directly), local-substitutable (test with the stand-in), remote but owned (port plus in-memory adapter), true external (injected port, mock adapter). Detail in [DEEPENING.md](DEEPENING.md).
5. **Contract first.** Write the interface, its error semantics and an example call before the body. Validate input at the boundary, once.
6. **Prefer addition over modification** for anything with callers you do not control. Name things predictably and consistently with the codebase.
7. **Replace, don't layer, tests.** Once the deep module's interface has tests, delete the old unit tests on the shallow pieces it absorbed.

## Designing for testability

- Accept dependencies; do not construct them inside.
- Return results instead of producing side effects where you can.
- Keep the surface small: fewer methods and parameters mean fewer tests and simpler setup.

## Design it twice

When the interface shape is genuinely open and the module has real leverage, produce 3 radically different interfaces before choosing (minimal entry points, maximum flexibility, optimised for the common caller, ports and adapters). Parallel read-only subagents work well for this. Compare on depth, locality and seam placement; present the comparison with a recommendation. Recipe in [DEEPENING.md](DEEPENING.md).

## Finding deepening opportunities

Scope first. Look where the code changed recently (`git log --oneline`, hot files) or where the user points; a read-only subagent can walk it. Note friction: one concept spread across many small modules, shallow wrappers, tests that mock internals, the same change touching many files, code that is hard to test through its current interface.

Present each candidate as: files, problem, proposed deepening (in plain words, no interface yet), benefits in terms of locality, leverage and tests, and a strength (strong, worth exploring, speculative). End with the one you would do first. Raise a candidate that contradicts an ADR only when the friction is real enough to reopen it, and say so. Let the user pick, then grill the chosen one with `fox-dev:shape`. If the user rejects a candidate for a reason a future review would need, offer an ADR so it is not suggested again.

## Recording decisions

- **ADR** only when all three hold: hard to reverse, surprising to a reader without the context, and the result of a real trade-off between alternatives. Follow the repo's existing ADR convention; else `docs/adr/NNNN-<slug>.md` with Status, Context, Decision, Alternatives considered, Consequences. ADRs are append-only; supersede rather than edit.
- **Glossary term** when a word is ambiguous or overloaded in the domain. Add it to the repo's `GLOSSARY.md` if one exists; create one only when the user wants it. A glossary holds meanings only: no implementation detail, no decisions.
- Read existing ADRs and glossary before proposing a design, and do not re-open a recorded decision without saying so.

## Sharpening the domain language

When the conversation is about what the domain's words mean, work the model actively:

- **Challenge conflicts**: "the glossary says a cancellation is X, you seem to mean Y; which is it?"
- **Sharpen fuzzy words**: "account" could be the Customer or the User; propose one precise term for each.
- **Probe with scenarios**: invent concrete edge cases that force a boundary between two concepts.
- **Cross-check the code**: when the user says how something works, check the code agrees and raise any contradiction.
- Record each settled term as it settles, not in a batch at the end.

## Common rationalizations

| Thought | Reality |
|---|---|
| "An interface now keeps it flexible." | One adapter is indirection. Wait for the second. |
| "Many small functions are cleaner." | Small and shallow moves complexity into every caller. Run the deletion test. |
| "I'll test the private helper directly." | Test through the interface, or the interface is wrong. |

## With fox-db (when the `fox_*` tools are listed)

- `fox_graph target=<symbol> rel=callers` and `rel=impact` measure a module's leverage and which callers a seam change touches.
- `fox_read target=<path>` gives declaration outlines; `fox_find kind=doc q=adr` finds recorded decisions.

Derived from: mattpocock-skills codebase-design, improve-codebase-architecture, domain-modeling; agent-skills api-and-interface-design, documentation-and-adrs (MIT, see NOTICE.md).
