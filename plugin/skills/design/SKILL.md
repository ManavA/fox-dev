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

Scope first. Look where the code changed recently (`git log --oneline`, hot files) or where the user points. Note friction: one concept spread across many small modules, shallow wrappers, tests that mock internals, the same change touching many files. Present candidates with the deletion-test result and expected leverage; let the user pick.

## Recording decisions

- **ADR** when a decision is hard to reverse, surprising, or will be re-litigated. Follow the repo's existing ADR convention; else `docs/adr/NNNN-<slug>.md` with Status, Context, Decision, Alternatives considered, Consequences. ADRs are append-only; supersede rather than edit.
- **Glossary term** when a word is ambiguous or overloaded in the domain. Add it to the repo's `GLOSSARY.md` if one exists; create one only when the user wants it.
- Read existing ADRs and glossary before proposing a design, and do not re-open a recorded decision without saying so.

## Common rationalizations

| Thought | Reality |
|---|---|
| "An interface now keeps it flexible." | One adapter is indirection. Wait for the second. |
| "Many small functions are cleaner." | Small and shallow moves complexity into every caller. Run the deletion test. |
| "I'll test the private helper directly." | Test through the interface, or the interface is wrong. |

## With foxdb (when the `fox_*` tools are listed)

- `fox_graph target=<symbol> rel=callers` and `rel=impact` measure a module's leverage and which callers a seam change touches.
- `fox_read target=<path>` gives declaration outlines; `fox_find kind=doc q=adr` finds recorded decisions.

Derived from: mattpocock-skills codebase-design, improve-codebase-architecture, domain-modeling; agent-skills api-and-interface-design, documentation-and-adrs (MIT, see NOTICE.md).
