# fox-dev

One small skill pack for the whole development loop in Claude Code: shape an idea into a spec, design the seams, plan it as vertical tasks, build it test-first, review it with fresh eyes, verify it and ship it. Two on-demand skills cover frontend work and plain writing.

fox-dev replaces three overlapping plugins (superpowers, mattpocock-skills and agent-skills) with fifteen skills and two agents. It merges and condenses their best parts, credited in [NOTICE.md](NOTICE.md), and works well with [fox-db](https://github.com/ManavA/fox-db).

## Who it is for

Developers who use Claude Code (or Codex) and want one consistent process instead of several skill packs that compete for the same prompts. If you run superpowers and mattpocock-skills side by side today, fox-dev is meant to replace both.

## What we measured

In a firing eval (48 prompts that should trigger a skill, 16 control prompts that should not, Sonnet, two samples each; details in [evals/RESULTS.md](evals/RESULTS.md)):

- fox-dev fired the right skill on 36 to 40 of 48 prompts across three runs, against 31 of 48 for superpowers plus mattpocock-skills. In the 0.1.1 re-run, with cases added for the new content, it fired the right skill on 64 of 72; the only misses were `build`, which never fires first because the model reads files before editing, and the user-invoked `handoff`.
- No false fires: no skill fired on any control prompt. `ui` and `prose` fired on all their own prompts and on none of the negatives written to tempt them.
- The opening prompt is smaller: about 9,050 tokens on the first request, against about 10,930 for superpowers plus mattpocock-skills.

What the skills do not do: in outcome evals, where Sonnet solved coding tasks on its own with hidden tests and a blind judge ([evals/outcome/](evals/outcome/)), code quality was the same with fox-dev, with the older plugins and with no skills at all. Skills rarely fired during those autonomous runs, and loading any plugin added roughly 8 to 15 percent to cost per run. fox-dev gives you a cleaner, more predictable process when you ask for one; it does not make the model write better code.

## Install

### Claude Code

```sh
claude plugin marketplace add ManavA/fox-dev
claude plugin install fox-dev@fox-dev
```

From a local clone, pass the clone's path to `marketplace add` instead. Start a new session afterwards.

Use fox-dev instead of superpowers and mattpocock-skills, not next to them: their overlapping descriptions (several TDD, debugging and review skills) split which one fires. Disable or uninstall them first.

### Codex

```sh
codex plugin marketplace add ManavA/fox-dev
codex plugin add fox-dev@fox-dev
```

Codex gets the fifteen skills. The two agents are Claude Code only.

## Skills

Skills load on their own when a request matches their description. You can also call any of them directly as `/fox-dev:<skill>`.

| Command | Use it for |
|---|---|
| `/fox-dev:shape` | Turning an idea or change request into an agreed one-page spec: questions, assumptions, optional prototype. |
| `/fox-dev:design` | Interface and seam decisions, deep modules, ADRs and glossary terms. |
| `/fox-dev:plan` | Breaking a spec into vertical, test-first tasks with dependencies. |
| `/fox-dev:build` | Test-first implementation: failing test, watch it fail, minimal code, commit per slice. |
| `/fox-dev:swarm` | Running two or more independent tasks in parallel, one writer per worktree, with fresh reviewers. |
| `/fox-dev:debug` | Root-cause debugging: reproduce, minimise, ranked hypotheses, fix with a regression test. |
| `/fox-dev:review` | Reviewing a diff against its spec and the repo's standards with fresh-context reviewers, and handling feedback. Bug hunting is left to the built-in `/code-review`. |
| `/fox-dev:verify` | The evidence gate before saying done, fixed or passing. |
| `/fox-dev:ship` | Finishing a branch: green suite, clean commits, merge or PR, PR description. |
| `/fox-dev:handoff` | Only when you call it: a handoff document for the next session. |
| `/fox-dev:retro` | Only when you call it: a retrospective on a session, proposing changes to checks, standards, CLAUDE.md and tooling. |
| `/fox-dev:research` | Answering library and API questions from primary sources, with cited notes. |
| `/fox-dev:write-for-agents` | Writing skills, CLAUDE.md or AGENTS.md files and subagent briefs. |
| `/fox-dev:ui` | Frontend design: visual direction, layout, accessibility, and checking the result in a browser. Loads only for UI work. |
| `/fox-dev:prose` | Plain, concise docs, READMEs, changelogs, commit and PR wording, and reports. Loads only for writing tasks. |

Agents (Claude Code): `fox-dev:reviewer`, a zero-context reviewer that returns `path:line` findings, and `fox-dev:implementer`, which takes one task test-first in its own worktree.

No hooks and no session-start injection: nothing runs unless a skill is picked.

## With fox-db

[fox-db](https://github.com/ManavA/fox-db) is a local code index and shared agent context. When its `fox_*` tools are present, several skills use them in place of grep and re-reading files:

- `debug` and `design` walk callers and impact through the call graph (`fox_graph`), and `debug` records ruled-out hypotheses in shared memory.
- `plan` and `review` measure a change's blast radius (`fox_graph rel=impact`), and `review` hands reviewers the spec plus the code it cites (`fox pack`).
- `shape` and `research` recall past decisions and failed approaches (`fox_memory`).
- `swarm` dispatches workers with writer leases and a shared board (`fox dispatch`, `fox swarm`), and `handoff` writes a handoff packet any harness can pick up.
- `ship` and `prose` list docs that a change made stale (`fox drift`).

Without fox-db every step falls back to grep, file reads and git. fox-db is a separate project under AGPL-3.0-or-later; fox-dev contains none of its code.

## License

MIT. See [LICENSE](LICENSE). fox-dev is derived in part from MIT-licensed work by Matt Pocock, Jesse Vincent and Addy Osmani; their notices are in [NOTICE.md](NOTICE.md), which also ships inside the plugin.

Changes are listed in [CHANGELOG.md](CHANGELOG.md).
