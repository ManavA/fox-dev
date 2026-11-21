---
name: verify
description: Evidence gate before saying done, fixed or passing. Use before any completion claim, commit, PR or report, even when the last run was green and the change was tiny.
---

# Verify

**Evidence before claims.** A claim of done, fixed or passing needs fresh output from a command that proves it, read in this turn.

## The gate

1. **Identify** what proves the claim: the test that covers the change, the full suite, the build, the lint and typecheck, the repro loop for a bug, the command the spec's acceptance criteria name.
2. **Collect the project's gates** from CLAUDE.md, AGENTS.md, CONTRIBUTING, CONSTRAINTS.md or CI config. The project's list beats your own.
3. **Run** each one, fully, now. Skip a re-run only when nothing it covers has changed since its last green run in this session, and say so.
4. **Read the output**: exit code, pass and fail counts, warnings, the actual assertion. "No output" is not success.
5. **Claim** only what the output shows, and quote the evidence briefly (command plus result line).

If any gate fails, report the failure; do not claim partial success as done.

## Check the bar was not lowered

Before claiming done, scan the diff (`git diff <base>...HEAD`) for:

- tests deleted, skipped, marked expected-fail, or with assertions loosened;
- new lint or type suppressions (`eslint-disable`, `# type: ignore`, `#[allow]`, `@ts-expect-error`), widened thresholds, or coverage excludes;
- stubs, TODOs or hard-coded values standing in for the real behaviour;
- error handling that swallows failures.

Each one is either justified in the PR or report, or removed.

## Claims about other agents' work

A subagent's "done" or "tests pass" is a claim. Read its diff and run its verify command yourself before repeating it.

## Definition of done

- Acceptance criteria met, verified at runtime, not only compiled.
- New behaviour covered by tests that fail without the change.
- Existing tests pass; no regressions.
- No debug output, dead code or unrelated changes left in.
- Docs and config updated where behaviour or interfaces changed.
- Risky changes have a rollback path.

## Common rationalizations

| Thought | Reality |
|---|---|
| "It passed a minute ago." | Did anything change since? Then run it again. |
| "It's a one-line change." | One-line changes break builds. Run the gate. |
| "The agent said tests pass." | Run them. |
| "Should work now." | That is a prediction, not evidence. |

Derived from: superpowers verification-before-completion; agent-skills references/definition-of-done, constraint-driven-development (MIT, see NOTICE.md).
