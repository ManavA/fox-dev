# Deepening a cluster

## Dependency categories

Classify every dependency of the candidate; the category decides how the deepened module is tested across its seam.

1. **In-process**: pure computation or in-memory state. Merge the modules and test through the new interface directly. No adapter.
2. **Local-substitutable**: has a local stand-in (in-memory filesystem, embedded database). Test with the stand-in running in the suite. The seam stays internal.
3. **Remote but owned**: your own service across a network. Define a port at the seam; the deep module owns the logic and the transport is an injected adapter. Production uses the network adapter, tests an in-memory one.
4. **True external**: third-party services you do not control. Inject a port; tests use a mock adapter. Mock only here.

## Seam discipline

- Internal seams (private, used by the module's own tests) are fine. Do not expose them through the interface just because a test wants them.
- Introduce a port only when at least two adapters are justified.

## Testing: replace, don't layer

Write tests at the deepened interface, assert on observable outcomes, then delete the old tests on the absorbed shallow modules. A test that changes when the implementation changes is testing past the interface.

## Design it twice (recipe)

1. **Frame the problem** for the user: constraints any interface must satisfy, the dependencies and their categories, and a rough sketch that makes the constraints concrete (not a proposal). Show it and move on; the user reads while the next step runs.
2. **Dispatch 3 or more read-only subagents in parallel**, each with the same technical brief (paths, coupling, dependency categories, the vocabulary in SKILL.md and the project's glossary) and a different design goal:
   - minimise the interface: 1 to 3 entry points, maximum leverage each;
   - maximise flexibility and extension;
   - make the most common caller trivial;
   - (if relevant) ports and adapters around cross-seam dependencies.
3. Each returns: the interface (types, methods, invariants, ordering, error modes), a usage example, what the implementation hides, the dependency strategy, and trade-offs.
4. **Compare** in prose on depth, locality and seam placement, then recommend one (or a hybrid) and say why. The user decides.
