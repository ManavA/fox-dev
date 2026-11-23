---
name: retro
description: Run a retrospective on a coding session and propose changes to the agent's environment (checks, standards, CLAUDE.md, tooling).
argument-hint: "Which session? (default: this one)"
disable-model-invocation: true
---

# Retro

Improve the **environment** the next agent works in, using what actually happened in a session. The output is a ranked list of proposed changes; make none of them until the user picks.

## 1. Read the primary sources

Default to the current session. If the user names another, read its transcript or logs on this machine, plus the diff, commits and review findings it produced. Note each moment the agent was slow, wrong or stuck, with the evidence (the tool call, the error, the finding).

## 2. Find candidates

Look in these places, and only where the evidence points:

- **Navigation**: the agent took long to find a file or fact. Would a one-line pointer (in CLAUDE.md, a README or a skill) have sent it there?
- **Automated checks**: the agent made a mistake a lint rule, type check, test or hook could have caught. Read the repo's own check command and CI first: a check that exists but is unwired or broken is the finding. A repo with no guardrail at all (no pre-commit hook, no CI running lint, types and tests) is a finding too.
- **Coding standards**: the reviewer missed something. A **mechanical** rule (banned API, import shape, file location) gets a deterministic check in the repo's linter, hooks or CI. Only a genuine judgement call goes in the written standards the reviewer reads.
- **Steering files**: CLAUDE.md or AGENTS.md is long, holds rules that belong in standards or checks, or holds no-ops (lines the agent would follow anyway). Steering files load on every turn, so keep them to pointers.
- **Tool economy**: an expensive or repeated tool call that a better command, script or index lookup would replace.
- **Information access**: something the agent needed and could not see (dev server logs, read-only access to a service, a fixture).

Put standards where the reviewer reads them, not in what the implementer loads: the reviewer gets a diff and has room to spare, the implementer does not.

## 3. Present

List the candidates most severe first. For each: what happened (with the evidence), the proposed change, where it goes, and its cost. Use `fox-dev:write-for-agents` for wording any change to a skill, CLAUDE.md or brief.

Done when every slow, wrong or stuck moment from step 1 has a candidate or a stated reason for none, and the user has the ranked list.

## With fox-db (when the `fox_*` tools are listed)

- `fox_find kind=memory q=<topic>` (memory notes and past sessions) and `fox_memory op=recall kind=failed` find the session and the approaches that failed in it.

Derived from: mattpocock-skills retro (MIT, see NOTICE.md).
