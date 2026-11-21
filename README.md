# fox-dev

A small Claude Code plugin with twelve skills for the development loop: shape an idea into a spec, plan it as vertical tasks, build it test-first, review it, verify it and ship it. It merges and condenses three MIT skill packs (mattpocock-skills, superpowers and agent-skills); see NOTICE.md for credits and the exact sources.

Status: draft. Not published.

## Skills

| Skill | Use it for |
|---|---|
| `shape` | Turning an idea or change request into an agreed one-page spec (grilling rounds, assumptions list, optional prototype). |
| `design` | Interface and seam decisions, deep-module vocabulary, ADRs and glossary terms. |
| `plan` | Breaking a spec into vertical, test-first tasks with blocking edges. |
| `build` | Test-first implementation in the main session: failing test, watch it fail, minimal code, commit per slice. |
| `swarm` | Running 2+ independent tasks in parallel with one writer per worktree and fresh reviewers. |
| `debug` | Root-cause debugging: build a red loop, minimise, ranked hypotheses, fix with a regression test. |
| `review` | Spec, standards and blast-radius review with fresh-context reviewers, and handling review feedback. Bug hunting is left to the built-in `/code-review`. |
| `verify` | The evidence gate before saying done, fixed or passing. |
| `ship` | Finishing a branch: green suite, atomic commits, merge or PR, PR body. |
| `handoff` | User-invoked only (`/fox-dev:handoff`): a handoff document for the next session. |
| `research` | Answering library or API questions from primary sources, with cited notes. |
| `write-for-agents` | Writing skills, CLAUDE.md/AGENTS.md and subagent briefs. |

Agents: `fox-dev:reviewer` (zero-context reviewer, returns path:line findings) and `fox-dev:implementer` (one task, test-first, in its own worktree).

The skills have no hooks and no SessionStart injection; the harness picks them by description.

## Install (local)

```
claude plugin marketplace add <path-to-this-repo>
claude plugin install fox-dev@fox-dev
```

Running fox-dev next to superpowers or mattpocock-skills is not recommended long term: overlapping descriptions (several TDD, debugging and review skills) split which one fires.

## foxdb

Several skills end with a short "With foxdb" block naming `fox_*` tools. Those lines apply only when the foxdb tools are present; without them every step falls back to grep, read and git.

## License

MIT. See LICENSE and NOTICE.md.
