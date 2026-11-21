# Worker brief template

Fill every field with a pointer or a short fact. Leave out anything the worker can read from a path.

## Implementer

```
Task: T<N> <title> from <plan path>. Spec: <spec path>.
Worktree: <path>, based on <commit>. You are the only writer here.
Files: <paths from the plan>.
Interfaces: consumes <names/types>; produces <names/types>.
Acceptance: see T<N> in the plan.
Test command: <exact command>. Full suite: <command>.
Rules: test first and show the failing run; minimal code; commit per slice; follow <CLAUDE.md/AGENTS.md path>.
Out of scope: anything outside the listed files unless the task cannot pass without it (say so).
Return (under 200 words): status DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED;
commits (sha + one line); the failing-then-passing test output (trimmed); concerns or rulings.
```

## Reviewer

```
Review commits <base>..<head> in <repo or worktree>. Read-only.
What it should do: <spec path> and task T<N> acceptance in <plan path>.
Standards: <CLAUDE.md, CONTRIBUTING, lint config paths>.
Check: each acceptance criterion met; scope creep; tests drive the public seam and would fail without the change;
<plan's Review focus lines that apply>.
Return findings as `path:line - severity (Critical/Required/Optional/Nit) - issue - suggested fix`,
under 400 words. Say "no findings" if none. Do not fix anything.
```

## Parallel fixer (several unrelated failures)

```
Failure: <test id or error, one line>. Reproduce with: <command>.
Scope: <one file or subsystem>. Do not change: <other areas>.
Return: root cause in one sentence, the change, and the passing run.
```
