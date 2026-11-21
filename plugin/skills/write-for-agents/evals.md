# Skill evals

Two kinds, per skill:

- **Must-fire**: a realistic prompt where the skill should trigger, including the "even when" case (the obvious fix, the short diff, the pasted trace).
- **Must-not-fire**: a nearby prompt that belongs to another skill or to no skill (a review request should not fire `build`; "what does this function do?" should not fire `debug`).

## Layout (the `claude plugin eval` format)

```
evals/plugin/<skill>-fires/prompt.md
evals/plugin/<skill>-fires/graders/skill-fired.md
evals/plugin/<skill>-stays-quiet/prompt.md
evals/plugin/<skill>-stays-quiet/graders/skill-not-fired.md
```

`prompt.md` has frontmatter (`description`, `expected_outcome`, `max_turns`, `allowed_tools`) and the user prompt as its body. Graders:

```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?build"'
---
```

Other grader types: `regex` (a pattern the reply must contain) and `llm` (a PASS condition in prose, judged by a model). Use an `llm` grader for behaviour: "PASS if the agent ran the new test and showed it failing before editing the source."

## Running

Run in a scratch HOME with only the plugins under test installed. Pin `--model`, record the CLI version, run each case several times, and compare pass rates rather than single runs. Compare against the stack being replaced on the same prompts.

## Collisions

When two skills' descriptions share most trigger words, one will steal the other's prompts. Check each must-fire prompt fires the intended skill, not just some skill.
