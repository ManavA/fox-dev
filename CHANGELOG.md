# Changelog

## 0.1.1 (Unreleased)

- New user-invoked `retro` skill: reads a session's transcript and results and proposes ranked changes to the agent's environment (checks, standards, steering files, tooling). It has no description in the skill listing, so it costs no context until you call it.
- Coverage audit against mattpocock-skills 1.3.1 and agent-skills 0.6.17; the full per-item table is in COMPARISON.md. Gaps filled inside existing skills:
  - `shape`: a divergent step for vague ideas, a questionnaire for decisions only someone else can answer, delta specs for changes to shipped features, a restatement check before the spec.
  - `design`: active domain-language work (challenge, sharpen, scenarios, cross-check the code), a stricter ADR bar (all of hard to reverse, surprising, real trade-off), and a candidate format for deepening opportunities.
  - `plan`: removing or replacing things others depend on, an integration branch for batches that cannot stay green, and a decision map for work too big and unclear to slice.
  - `build`: scope discipline, a tree that stays green between slices, flags for unfinished merged work, and pointers to the security checklist and the performance loop for sensitive slices.
  - `debug`: CI-only failures, and a full performance loop (measure, one fix, keep or revert against noise, log attempts, guard).
  - `review`: SSRF, deletes on computed paths, shared-store rate limits and an ask-first list in the security checklist; dependency, comment and dead-code checks in the axes.
  - `ship`: versioned releases (semver, changelog in the same change, tags) and staged production launches with rollback lines.
  - `ui`: browser content treated as data; `write-for-agents`: when to split a skill and router skills.
- `plan` and `ship` descriptions now say to fire before exploring code, and name migrations, deprecations and removals (plan) and cutting a release (ship); without this, those prompts explored the repo instead of firing.
- Firing eval re-run with cases for the new content and `retro` negatives: 64 of 72 should-fire runs hit, no false fires on controls or negatives (details in `evals/RESULTS.md`). `analyze.py` reads any `not-<skills>` family as a negative.

## 0.1.0 (2026-11-22)

First release.

- Fourteen skills for the development loop: shape, design, plan, build, swarm, debug, review, verify, ship, handoff, research, write-for-agents, ui and prose.
- Two agents for Claude Code: `reviewer` (zero-context review with `path:line` findings) and `implementer` (one task, test-first, in its own worktree).
- `ui` and `prose`: on-demand skills for frontend design and plain writing, scoped so they load only for that kind of task.
- Claude Code marketplace and plugin manifests, and a Codex plugin manifest (skills only).
- "With foxdb" steps in eleven skills that use the foxdb tools when they are installed and fall back to grep, reads and git otherwise.
- Firing and outcome evals with their drivers, cases and results under `evals/`.
- LICENSE and NOTICE.md ship inside the plugin directory as well as at the repository root.
- A plugin icon (original artwork; SVG source in `assets/icon.svg`).
