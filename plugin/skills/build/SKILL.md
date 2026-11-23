---
name: build
description: "Test-first implementation: failing test, watch it fail, minimal code, commit per slice. Use when implementing a task or plan, fixing a bug, adding tests or changing behaviour, even when the code is pasted inline and the fix looks obvious."
---

# Build

Implement in **vertical slices**, each proven by a test you watched fail and then pass. Work in this session; `swarm` is only for plans with 2+ independent tasks.

## 0. Set up

- **Find the repo's own commands**: build, single-test, full suite, lint, typecheck. Read CLAUDE.md/AGENTS.md, package scripts, Makefile, CI config. Use those, not generic ones.
- Run the relevant tests once before changing anything, so you know the baseline. Pre-existing failures are noted, not fixed silently.
- If working from a plan, read the spec and plan, and start a **ledger** (a short notes file beside the plan, or the todo list): one line per task done and one `Ruling:` line per decision.

## 1. The loop (one slice at a time)

1. **Red.** Write one test for the next behaviour, at the agreed **seam** (the public interface; see `fox-dev:design`). Run it. **Watch it fail**, and check it fails for the expected reason (assertion on the missing behaviour, not a typo or import error).
2. **Green.** Write the least code that makes it pass. No speculative options, no future cases.
3. **Run** the test, then the nearby suite. Read the output.
4. **Commit** the slice when the repo's commit rules allow (atomic, message says why).
5. Next slice. Refactoring is a separate pass after the slice is green, or during review, never mixed into red-green.

**Seams.** Use the seams the spec or plan names. Confirm a seam with the user only when it is a **new interface**; existing interfaces need no sign-off.

## 2. Code came first? Prove the test anyway

Test-first is firm. If implementation code already exists for the behaviour (you wrote it early, the user pasted it, or a subagent did), **keep the code** and prove the test is real:

1. Write the test against the intended behaviour.
2. Show it **fails on the old code**: stash or revert just the implementation (`git stash push <paths>`, or check out the pre-change file), run the test, record the failure.
3. Restore the implementation and show the test passes.

A test that was never seen failing does not count as evidence. Do not delete working code to restart.

## 3. Bugs: the Prove-It pattern

For a bug, the first test reproduces it: it fails on the current code with the user's symptom. Then fix, then watch it pass. If the cause is unclear, call the Skill tool with `fox-dev:debug` first.

## 4. Writing good tests

- Test behaviour through public interfaces; a good test reads like a spec line and survives refactors.
- Expected values come from an independent source (a literal, a worked example, the spec), never recomputed the way the code does.
- Prefer **real > fake > stub > mock**. Mock only at system boundaries you do not control (third-party APIs, time, randomness).
- Anti-patterns: **implementation-coupled** tests (mocking internals, testing privates, verifying via a side channel), **tautological** tests (pass by construction), **horizontal slicing** (all tests first, then all code).
- Examples: [tests.md](tests.md). Mocking guidance: [mocking.md](mocking.md).

## 5. Working a plan: rulings, not stalls

Execute task after task without pausing for "should I continue?". When the plan conflicts with itself or the code, decide, and record `Ruling: <decision> - <why> - <cost if wrong>` in the ledger. The spec outranks the plan.

**Stop and ask only for:** an irreversible or destructive operation; a security-sensitive action; a side effect outside the norms (push, merge to a shared branch, publish); or a plan so broken that every path forward is a guess.

## 6. Finish

Done when every task's acceptance criteria hold, each has a test you watched fail and then pass, the full suite and the repo's gates are green, and the ledger records every ruling. Then call the Skill tool with `fox-dev:review` on the branch, and `fox-dev:verify` before saying done.

## Common rationalizations

| Thought | Reality |
|---|---|
| "Too small to test." | Small changes break things too. The test is small as well. |
| "I'll add tests after." | Then show them failing on the old code (section 2). |
| "It obviously fails, no need to run it." | Run it. A test that passes immediately tests nothing new. |
| "I'll refactor while I'm here." | Finish green first; refactor as its own step. |
| "Mocking this internal class is easier." | It couples the test to the implementation. Use the real thing. |

## With fox-db (when the `fox_*` tools are listed)

- Before changing a signature, `fox_graph target=<symbol> rel=callers`; done means every caller row is accounted for (updated, tested, or ruled unaffected).

Derived from: mattpocock-skills tdd, implement; superpowers test-driven-development, executing-plans; agent-skills test-driven-development, incremental-implementation (MIT, see NOTICE.md).
