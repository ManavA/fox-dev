# Review axes and smell baseline

## Five axes (for the reviewer's own reading of the diff)

1. **Correctness**: does it do what the spec says, including edge cases and error paths? Do the tests prove it, and would they fail without the change? (Line-level bug hunting is the built-in `/code-review`'s job.)
2. **Readability and simplicity**: names reveal intent; no cleverness a reader must decode; no dead code, debug output or commented-out blocks; nothing added "for later".
3. **Architecture**: fits existing patterns; dependencies point the right way; modules stay deep (see `fox-dev:design`); no new seam with a single adapter.
4. **Security**: untrusted input validated at the boundary; authorization on every access; no secrets in code or logs. See [security.md](security.md).
5. **Performance**: no N+1 queries, unbounded loops or loads, or work on the hot path that could be cached or deferred. See [performance.md](performance.md).

Review tests first: they show what the author thinks the change does.

## Change size

Around 100 changed lines reviews well; past roughly 1,000, ask for a split (by layer of the expand-contract sequence, by feature slice, or refactor first then behaviour).

## Smell baseline (Fowler, Refactoring ch. 3)

Always judgement calls, phrased as "possible <smell>". A documented repo rule overrides any of them; skip anything tooling already enforces.

- **Mysterious Name**: name does not reveal what it does. Rename; if no honest name comes, the design is murky.
- **Duplicated Code**: the same logic shape in more than one hunk. Extract and share.
- **Feature Envy**: a function uses another object's data more than its own. Move it to that data.
- **Data Clumps**: the same fields or params travel together. Bundle them into a type.
- **Primitive Obsession**: a string or number stands in for a domain concept. Give it a small type.
- **Repeated Switches**: the same switch on the same type in several places. One map or polymorphism.
- **Shotgun Surgery**: one logical change forces scattered edits. Gather what changes together.
- **Divergent Change**: one module edited for unrelated reasons. Split by reason to change.
- **Speculative Generality**: hooks or parameters for needs the spec lacks. Delete them.
- **Message Chains**: `a.b().c().d()` the caller should not know about. Hide the walk.
- **Middle Man**: a layer that only delegates. Call the target directly.
- **Refused Bequest**: a subtype ignoring most of what it inherits. Use composition.

## Simplification pass

When asked to simplify: preserve behaviour exactly, follow project conventions, prefer clarity to cleverness, and touch only what the change touched. Understand why code exists before removing it (Chesterton's fence). Apply one simplification at a time and re-run the tests after each. The built-in `/simplify` does this pass automatically.
