---
name: write-for-agents
description: Writing skills, CLAUDE.md/AGENTS.md and agent briefs that agents follow. Use when creating or editing any of these, or a subagent prompt, even for a one-line change.
---

# Write for agents

The same levers apply to a skill, a CLAUDE.md or AGENTS.md, and a subagent brief: the goal is that the agent takes the same **process** every run.

## Pointers and the two loads

A **context pointer** is a line in context that names out-of-context material and the condition for reaching it. A skill description is one; a CLAUDE.md line naming a doc is another. The pointer's wording, not its target, decides when the agent reaches it.

- **Context load**: always-loaded text (descriptions, CLAUDE.md) costs tokens and attention every turn. Prune it hardest.
- **Cognitive load**: what the human must remember (user-invoked skills, files with no pointer). Spend it only where human judgement matters.

## Descriptions (for skills)

- Front-load a **leading word**: a compact concept the model already knows (_tracer bullet_, _red_, _frontier_).
- Name the triggers: the phrases users actually type and the situations, **one trigger per distinct branch**. Synonyms for one branch are one branch.
- Add an **"even when ..." clause** naming the case where the agent would otherwise skip the skill (the obvious fix, the tiny change). Measure it with evals; drop it if it causes false fires.
- Say when, not how. A description that summarises the workflow gets followed instead of the body.
- Keep it under about 300 characters. Make a skill **user-invoked** (`disable-model-invocation: true`) when only a human ever starts it; it then costs no context load.

## Body structure

- **Steps** (ordered actions) and **reference** (rules, facts) can mix. Put what every branch needs in the file; push what only some branches need into a sibling file behind a pointer (**progressive disclosure**). Aim for under about 120 lines.
- **Co-locate**: a concept's definition, rules and caveats under one heading.
- Every step ends on a **completion criterion** that is checkable and demanding ("every caller accounted for", not "check callers"). Vague bounds invite premature completion.
- Add a **common rationalizations** table for the excuses the agent will reach for, each with a one-line reality.
- Call other skills explicitly: "Call the Skill tool with `<plugin>:<skill>`", not a prose mention.
- **Split** only when the cut pays for itself. Split a sequence when later steps tempt the agent to rush the current one; this only helps across a real context boundary (a handoff or a subagent), since an inline call leaves the later steps in view. Split off a new model-invoked skill only for a distinct trigger word or when another skill must reach it, since its description is paid every turn. When user-invoked skills pile up past what a person remembers, one user-invoked router skill that names them helps.

## Wording

- **State the positive target** ("write one-line comments"). A prohibition drags the banned behaviour into context; use one only as a hard guardrail, paired with the positive.
- Retire restatements with leading words: "fast, deterministic, low-overhead" becomes _tight_.
- **Single source of truth**: each meaning in one place. Do not restate what the environment already says (package scripts, config, `--help`); cache only what looking cannot find (unwritten conventions, reasons, gotchas).
- Hunt **no-ops**: a sentence the model obeys by default changes nothing. Delete the whole sentence. A word too weak to beat the default (_be thorough_) needs a stronger one (_relentless_).
- Prune **sediment**: stale lines that settle because adding feels safe and removing feels risky.

## Agent briefs

A brief is the subagent's only context. State the goal, what is already ruled out, pointers to files and docs (not pasted dumps), a narrow scope, and the exact shape and length of what to return. Give reviewers the code, never your conclusion.

## Test it

Write it test-first, like code: before editing, run the target prompt without the change and watch the agent fail in the way you want to fix. After editing, run it again. Keep **must-fire** and **must-not-fire** prompt pairs for each skill; see [evals.md](evals.md).

Done when the must-fire prompts trigger it, the must-not-fire prompts do not, and the behaviour the skill promises shows in the transcripts.

## Common rationalizations

| Thought | Reality |
|---|---|
| "One more line in CLAUDE.md is free." | It is paid every turn. Point at a file instead. |
| "I'll add NEVER in capitals." | State the target behaviour; reserve prohibitions for guardrails. |
| "It's obvious it will fire." | Run the must-fire prompt. |

Anthropic's skill-authoring guidance: https://code.claude.com/docs/en/skills

Derived from: mattpocock-skills writing-for-agents, SKILL-MECHANICS; superpowers writing-skills; agent-skills docs/skill-anatomy, evals (MIT, see NOTICE.md).
