---
name: swarm
description: Runs independent tasks in parallel with one writer per change and fresh reviewers. Use when facing 2+ independent tasks or failures, e.g. "do these three unrelated chores in parallel" or "run separate agents on each failure", even when it looks quick to do directly or one by one.
---

# Swarm

Parallel execution with lean workers. The main session stays the **orchestrator**: it dispatches, merges and judges; workers implement or review one thing each.

## 0. Is it worth fanning out?

Fan out only when **2 or more tasks are independent**: no blocking edge between them, disjoint files, no shared mutable resource (same database, port, fixture). Otherwise call the Skill tool with `fox-dev:build` and work inline. Related failures (one may cause the others) are investigated together first, not split.

## 1. Isolate

- **Exactly one writer per working tree.** Each implementer gets its own git worktree: the Agent tool's `isolation: "worktree"`, a native worktree tool, or `git worktree add` under an ignored directory.
- Check you are not already inside a linked worktree before creating one (`git rev-parse --git-dir` vs `--git-common-dir`).
- Record the base commit each worker starts from.

## 2. Brief with pointers

Write each brief from [brief.md](brief.md). A brief is **pointers, not pasted context**: the spec and plan paths, the task id, the files, the interfaces it consumes and produces, the test command, and what to return. The worker reads the material itself.

Use the plugin's agents:

- `fox-dev:implementer` for one task, test-first, in its worktree.
- `fox-dev:reviewer` for a read-only review with zero prior context.

Dispatch all frontier tasks in one message so they run concurrently. Choose a cheaper model for mechanical tasks and a stronger one for integration or judgement.

## 3. Handle each report

Workers report one of: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED.

- **Verify the claim against the diff**, not the summary: read the diff, run the task's verify command in its worktree. An agent's "all tests pass" is a claim until you see the output.
- NEEDS_CONTEXT: supply the pointer and resume the same worker.
- BLOCKED: change something (context, task split, model) before retrying; never resend the same brief unchanged.

## 4. Review, then merge

1. Per task, dispatch a `fox-dev:reviewer` with the brief, the task's acceptance criteria and the diff range. Give it the code, never your conclusion.
2. Fix loop: send the findings back to the same implementer; after 3 rounds, re-dispatch on a stronger model or take it inline.
3. The orchestrator merges the approved branch into the integration branch, re-runs the suite, and recomputes the frontier. Dispatch newly unblocked tasks.

## 5. Finish

After the last merge, run one **whole-branch review** (call the Skill tool with `fox-dev:review`), then one fix pass, then `fox-dev:verify`. Remove the worktrees you created.

Done when every task is merged, the integration branch is green, the final review has no open Critical or Required findings, and no worker worktrees remain.

## Rulings and stops

Same as `build`: decide conflicts and record `Ruling:` lines. Stop only for destructive or irreversible steps, security-sensitive actions, pushes or publishes, or a plan too broken to follow.

## Common rationalizations

| Thought | Reality |
|---|---|
| "Two agents can share this checkout." | Concurrent writers corrupt each other's work. One writer per tree. |
| "The worker said it's done." | Read the diff and run the command. |
| "I'll paste the whole file into the brief." | Point at it. The worker can read. |
| "Parallel is always faster." | Not for 1 task or coupled tasks; merge pain eats the gain. |

## With foxdb (when the `fox_*` tools are listed)

- Board protocol: `fox_memory op=read since=me` before each dispatch; workers post fact/failed/question with handle evidence and return handles.
- `fox dispatch --writer` holds one writer lease per repo, `--reviewer` for reviewers; `fox wait` blocks on them; `fox swarm run plan.toml` runs a whole plan with a review panel.

Derived from: superpowers subagent-driven-development, dispatching-parallel-agents, using-git-worktrees; mattpocock-skills implement-spec; agent-skills references/orchestration-patterns (MIT, see NOTICE.md).
