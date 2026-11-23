---
name: handoff
description: Compact the current session into a handoff document another agent can pick up.
argument-hint: "What will the next session focus on?"
disable-model-invocation: true
---

# Handoff

Write a document that lets a fresh agent, with none of this session's context, continue the work.

Save it outside the repo: `$TMPDIR` (else `/tmp`; `%TEMP%` on Windows), named `handoff-<slug>-<date>.md`, and print its path.

## Contents

1. **Goal**: what the work is for, one paragraph.
2. **State**: what is done, with commits, branches and worktree paths; what is in progress and exactly where it stopped.
3. **Next steps**: ordered, each concrete enough to start without asking.
4. **Open questions**: decisions waiting on the user, with your recommended answer.
5. **Rulings and failed approaches**: what was decided and why; what was tried and ruled out, so it is not retried.
6. **Pointers**: specs, plans, ADRs, issues, PRs, logs, by path or URL. Point at them; do not copy their content.
7. **Suggested skills**: which skills the next agent should call (for example `fox-dev:build` to continue the plan, `fox-dev:review` before shipping).
8. **How to verify**: the commands that show the current state is green.

Redact secrets, tokens and personal data. If the user passed an argument, tailor the document to that next focus.

Done when a reader could run step 1 of Next steps without asking anything.

## With fox-db (when the `fox_*` tools are listed)

- `fox handoff create --goal ... --state ... --next ... --question ...`, then `fox handoff render h:<N> --for claude|codex`, instead of the markdown file.

Derived from: mattpocock-skills handoff; agent-skills context-engineering; superpowers executing-plans (ledger) (MIT, see NOTICE.md).
