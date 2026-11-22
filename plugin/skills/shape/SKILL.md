---
name: shape
description: Turns an idea or change request into an agreed spec. Use BEFORE exploring code or writing any code when asked to add, build or change a feature or behaviour (e.g. "add a rate limiter to this API"), or on "grill me", "interview me", "spec this", even when it looks quick to do directly.
---

# Shape

Reach a **shared understanding** with the user, then write it down as a one-page spec. The spec is what `plan` slices and what `review` checks the diff against.

## 0. Is there anything to shape?

Ask yourself what you know about what they want, and why.

- **Everything that matters is in the request** ("make the icon blue", a one-line fix with an obvious test). Skip this skill: do it through `fox-dev:build`, and say in one line any choice you made.
- **Something non-trivial is missing** (who it is for, what done looks like, which of two behaviours). Continue.

The user can say "skip the questions" at any time. Then state your significant assumptions in one list and proceed.

## 1. Look facts up yourself

Finding **facts** is your job; **decisions** are the user's. Before asking anything, read the code, docs, ADRs, git history and prior specs that bear on the request. Dispatch a read-only subagent for a broad sweep and keep asking the questions that do not depend on it while it runs.

## 2. Grill in rounds

Map the request as a **design tree**: every decision branches into the decisions that hang off it. The **frontier** is every decision whose prerequisites are settled.

Ask the whole frontier in one round. Number each question and give your recommended answer, worded so "yes" accepts it:

```
**Q1 - <title>**: <question, with options if useful>
-> Recommended: <answer and one-line reason>
```

A question that depends on another open question in this round waits for a later round. After each round, recompute the frontier. Anchor questions in specifics ("walk me through the last time this bit you") and offer a concrete guess when the user says "you decide".

Done when the frontier is empty: every branch visited, nothing silently assumed, and the user confirms the understanding.

## 3. Keep an assumptions list

Write every assumption you are making as a numbered list the user can strike through: platform, data shape, error behaviour, scale, who calls it. An assumption the user never saw is a decision made in secret.

## 4. Prototype when only running code can answer

If a question is about feel (a state model that is hard to reason about on paper, or what a UI should look like), build a throwaway prototype instead of debating it:

- Logic or state model: see [LOGIC.md](LOGIC.md).
- UI look and layout: see [UI.md](UI.md).

Prototypes are marked as throwaway, run with one command, keep state in memory, skip tests and polish, and show the full state after every action. Fold the verdict back into the spec; keep the prototype off main.

## 5. Write the spec

Save it where the repo keeps such docs, else `docs/specs/YYYY-MM-DD-<slug>.md`. One page:

```markdown
# <Feature>
**Objective:** what changes for whom, and why now.
**Non-goals:** what this deliberately does not do.
**Acceptance criteria:** numbered, observable, each one testable.
**Test seams:** the public interfaces the tests will drive (prefer existing, highest seam, fewest).
**Commands:** build, test, lint, run (copied from the repo, not invented).
**Global constraints:** version floors, naming, compatibility, project rules.
**Decisions:** each settled question with its answer. **Open questions:** anything left.
**Assumptions:** the final list from step 3.
```

If the work spans several independent subsystems, write one spec per subsystem. Publishing to an issue tracker is optional; do it only when the repo uses one.

Done when the user has approved the written spec. Then call the Skill tool with `fox-dev:plan` (multi-step work) or `fox-dev:build` (a single slice).

## Common rationalizations

| Thought | Reality |
|---|---|
| "The request is clear, I'll just start." | Check step 0 honestly. Unstated acceptance criteria are where rework comes from. |
| "I'll ask the user where the config lives." | That is a fact. Look it up. |
| "One question at a time is friendlier." | A numbered round with recommendations is faster and the user can answer "yes". |
| "I'll decide this detail quietly." | Put it on the assumptions list. |

## With foxdb (when the `fox_*` tools are listed)

- `fox_memory op=recall q=<topic>` for past decisions and failed approaches before the first round.
- `fox_find q=<topic> kind=doc` for existing specs and ADRs to build on.

Derived from: mattpocock-skills grilling, to-spec, prototype; superpowers brainstorming; agent-skills interview-me, idea-refine, spec-driven-development (MIT, see NOTICE.md).
