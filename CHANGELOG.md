# Changelog

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
