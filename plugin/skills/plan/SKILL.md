---
name: plan
description: Breaks an agreed spec into vertical, test-first tasks with dependencies. Use BEFORE exploring code when work spans more than one commit or file, or on "plan", "break this down", "tickets", or planning a migration, deprecation or removal, even when the steps seem obvious.
---

# Plan

Turn an agreed spec into a **task graph**: thin vertical slices, each with its own test, each declaring what blocks it. The graph's **frontier** (tasks whose blockers are done) is what `build` works through and what `swarm` dispatches from.

No spec yet? Call the Skill tool with `fox-dev:shape` first.

## 1. Read before slicing

Read the spec, then the code it touches: entry points, the modules on the path, existing tests and their command. Note any **prefactor** that would make the change easy ("make the change easy, then make the easy change"); it becomes the first task.

## 2. Slice vertically

Each task is a **tracer bullet**: a narrow but complete path through every layer it needs (schema, logic, interface, test), demoable or verifiable on its own, small enough for one fresh context.

- Prefer vertical over horizontal ("all the models, then all the handlers").
- Risky or unknown parts go early, so the plan fails fast.
- **Wide refactors** (one mechanical change with a huge blast radius) use expand-contract instead: add the new form beside the old, migrate callers in batches (one task each, blocked by the expand), then delete the old form in a task blocked by every batch. If even the batches cannot stay green alone, let them share an integration branch and end in one integrate-and-verify task; green is promised only there.
- **Removing or replacing** something others depend on (an API, a service, a flag, a format): first ask whether it still gives unique value, who depends on it and what migrating costs each of them. Build and prove the replacement before deprecating; announce with a replacement and a migration guide (advisory by default, a hard removal date only when risk or cost forces one); if you own the old thing, migrate its consumers yourself, one per task; remove it only once usage is shown to be zero, together with its tests, docs and config.
- Right-size: fold setup, config and docs into the task whose deliverable needs them. Split only where a reviewer could reject one task while approving its neighbour.

## 3. Write each task

```markdown
### T<N>: <title>
**Blocked by:** T<a>, T<b> | none
**Files:** create/modify/test paths (best current knowledge)
**Interfaces:** consumes <exact names and types from earlier tasks>; produces <exact names and types later tasks rely on>
**Acceptance:** observable criteria, each traceable to a spec line
**Test first:** the failing test to write and the seam it drives
**Verify:** the exact command, and what passing looks like
```

Describe the approach in a line when the test and signature leave a real choice. Leave full code out of the plan; the implementer writes it test-first.

## 4. Add the two plan-wide sections

```markdown
## Global constraints
One line each, copied verbatim from the spec or project rules: version floors, dependency limits, naming, compatibility, commit rules.

## Review focus
The 3 to 5 inputs or failure modes the spec implies but no task's tests exercise, most likely first. For each, add a test to the task that owns that code.
```

## 5. Check the graph with the user

Show the tasks as a numbered list (title, blocked by, what it delivers) and ask: is the granularity right, are the blocking edges real, should anything merge or split? Iterate until the user approves.

Save to where the repo keeps plans, else `docs/plans/YYYY-MM-DD-<slug>.md` next to the spec. A tracker is optional.

Done when the user has approved the graph and every spec acceptance criterion maps to at least one task.

## Too big and too foggy to slice

When the work is larger than one session can hold **and** key decisions are still open, plan the decisions before the build. Keep a map file (or one tracker issue) with: **Destination** (the spec, decision or change this is heading for), **Decisions so far** (one line and a link each), **Not yet specified** (questions you can see coming but cannot phrase yet) and **Out of scope**. Each open question becomes a decision ticket, typed research, prototype, grilling or task (manual work a decision waits on), with blocking edges. Work one decision ticket per session through `fox-dev:shape` or `fox-dev:research`, record the answer, and turn newly sharp questions into tickets. Slice the build only once the way to the destination is clear.

## Next

- Default: call the Skill tool with `fox-dev:build` and work the frontier in this session.
- If the frontier has **2 or more independent tasks** that touch disjoint files, call the Skill tool with `fox-dev:swarm` instead.

## Common rationalizations

| Thought | Reality |
|---|---|
| "The steps are obvious, no plan needed." | Then writing it takes two minutes and the blocking edges become visible. |
| "I'll put the full code in the plan." | That is implementing twice. Give interfaces, tests and acceptance. |
| "One big task is simpler." | It cannot be reviewed or reverted in parts. Slice it. |

## With fox-db (when the `fox_*` tools are listed)

- `fox_graph target=<symbol> rel=impact` on each symbol a task changes, to fill Files and Interfaces and to spot shared files between tasks.
- `fox handoff create --goal ... --next ...` turns the approved plan into a packet that `swarm` can dispatch from.

Derived from: superpowers writing-plans; mattpocock-skills to-tickets, wayfinder; agent-skills planning-and-task-breakdown, deprecation-and-migration (MIT, see NOTICE.md).
