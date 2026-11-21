---
name: review
description: Reviews a diff against its spec and the repo's standards with fresh-context reviewers, and handles review feedback. Use on "review", a PR, a branch or a pasted diff, or when feedback arrives, even when the diff is short and the review looks quick to do by reading it.
---

# Review

This skill reviews **what the change should do and how it fits**: Spec, Standards and Blast radius. The line-level **bug hunt** goes to the built-in `/code-review`; keep the two separate so neither masks the other.

## Reviewing a change

### 1. Pin the fixed point

Get the base from the user (commit, branch, tag, `main`); if they gave none, use the merge-base with the default branch and say so. Capture `git diff <base>...HEAD` (three-dot) and `git log <base>..HEAD --oneline`. Check that the ref resolves and the diff is non-empty before dispatching anyone.

### 2. Gather the inputs

- **Spec**: issue references in commits, a path the user gave, or a spec/plan under `docs/` matching the branch. If none exists, ask; if there is none, the Spec axis reports "no spec".
- **Standards**: every file that says how code is written here: CLAUDE.md, AGENTS.md, CONTRIBUTING, CODING_STANDARDS, lint and format config. The smell baseline in [axes.md](axes.md) applies on top; a documented repo rule always wins over it.
- **Blast radius**: the callers and consumers of every changed public symbol, config key, schema, CLI flag or file format (grep, or the foxdb block below).

### 3. Dispatch fresh-context reviewers in parallel

Send both in one message, as `fox-dev:reviewer` agents. Give each the diff command, the commit list and its inputs. **Give them the code, never your conclusion** about it.

- **Spec reviewer**: (a) requirements missing or partial; (b) behaviour nobody asked for (scope creep); (c) requirements that look implemented but wrongly. Quote the spec line for each.
- **Standards and blast-radius reviewer**: (a) breaches of documented standards, citing file and rule; (b) baseline smells, labelled as judgement calls; (c) callers, consumers or docs the change affects but did not update; (d) tests that do not drive the public seam or would pass without the change.

Each returns `path:line - severity - issue - suggested fix`, under 400 words. Severities: **Critical** (wrong behaviour, data loss, security), **Required** (must fix before merge), **Optional**, **Nit**. Suggest structural remedies, not only complaints.

For security-, performance- or accessibility-sensitive diffs, point the reviewer at [security.md](security.md), [performance.md](performance.md) or [a11y.md](a11y.md).

### 4. Hand off the bug hunt

Tell the user to run the built-in `/code-review` on the same range for correctness bugs, and `/simplify` if they want a cleanup pass. Do not duplicate that work here.

### 5. Report

Present `## Spec`, `## Standards and blast radius`, each verbatim or lightly cleaned. Do not merge or re-rank across axes. End with one line: findings per axis and the worst issue within each.

Done when both axes have reported (or Spec is marked "no spec") and the bug-hunt handoff is stated.

**Before an irreversible step** (a migration, a deletion, a public API change), get one fresh-context reviewer to argue against the decision first, with only the artifact and the requirement.

## Receiving feedback

1. **Read all of it** before changing anything. Restate any unclear item as a question; do not guess.
2. **Verify each item** against the code: does it hold here? Run it, read it, check the callers.
3. **Push back with reasons** when it is wrong, breaks something, or adds what nobody needs (YAGNI). Cite the code or test.
4. **Fix in order**: Critical, then Required, one item at a time, each with a test where behaviour changes; re-run the suite.
5. Reply with what changed, or why not. Skip thanks and performative agreement ("great point!"); the fix shows you heard it.

## Common rationalizations

| Thought | Reality |
|---|---|
| "It's short, I'll just read it myself." | Your context is anchored on how it was written. A fresh reviewer is not. |
| "I'll tell the reviewer what I think is wrong." | Then it confirms your hypothesis. Give it the code. |
| "The reviewer said so, I'll change it." | Verify first. Reviewers are wrong too. |
| "Spec and standards are one list." | A change can pass one and fail the other. Keep them apart. |

## With foxdb (when the `fox_*` tools are listed)

- `fox_graph rel=impact` with no target gives the working diff's blast radius for the reviewer brief.
- `fox pack <spec.md>` gives a reviewer the spec plus skeletons of the code it cites; `fox drift` flags docs the change made stale.

Derived from: mattpocock-skills code-review; superpowers requesting-code-review, receiving-code-review; agent-skills code-review-and-quality, code-simplification, doubt-driven-development (MIT, see NOTICE.md).
