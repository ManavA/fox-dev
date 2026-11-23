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

The user can say "skip the questions" at any time. Then state your significant assumptions in one list and proceed. If the conversation has already settled every decision, skip the rounds and write the spec straight from it.

**Still a vague idea** (no clear user, problem or direction yet)? Diverge before grilling. Restate it as one "how might we" sentence, then offer 3 to 5 genuinely different directions (another user, the 10x simpler version, the inverse, a different scope), each with what it bets is true and what would kill it. Recommend one and say honestly which are weak. Grill on the direction the user picks; the dropped ones go under Non-goals.

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

Done when the frontier is empty: every branch visited, nothing silently assumed, and the user confirms your restatement of what they want, in their own words.

**A decision only someone else can answer** (another team, a customer, a domain expert): ask the user only who it goes to and what they need back, then write a questionnaire file: purpose and the decision riding on it, one paragraph of context, how to answer (deadline, "I don't know" is fine), then themed questions, most important first, one idea each, with an answer stub. List it under Open questions and carry on with the rest of the frontier.

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

**Changing something already specced and shipped?** Write a small delta spec beside the original instead of editing it: Objective, Current behaviour (link the original), New behaviour, Acceptance criteria (including what must not change), and only the constraints that differ. Once it ships, fold the outcome into the original so it keeps describing the current system. Ideas that arrive mid-build go on a Deferred list in the spec, not into the build.

Done when the user has approved the written spec. Then call the Skill tool with `fox-dev:plan` (multi-step work) or `fox-dev:build` (a single slice).

## Common rationalizations

| Thought | Reality |
|---|---|
| "The request is clear, I'll just start." | Check step 0 honestly. Unstated acceptance criteria are where rework comes from. |
| "I'll ask the user where the config lives." | That is a fact. Look it up. |
| "One question at a time is friendlier." | A numbered round with recommendations is faster and the user can answer "yes". |
| "I'll decide this detail quietly." | Put it on the assumptions list. |

## With fox-db (when the `fox_*` tools are listed)

- `fox_memory op=recall q=<topic>` for past decisions and failed approaches before the first round.
- `fox_find q=<topic> kind=doc` for existing specs and ADRs to build on.

Derived from: mattpocock-skills grilling, to-spec, prototype, to-questionnaire; superpowers brainstorming; agent-skills interview-me, idea-refine, spec-driven-development (MIT, see NOTICE.md).
