---
name: prose
description: Plain, concise prose for people - docs, READMEs, guides, changelogs, release notes, commit message and PR description wording, status reports and summaries. Use when the main task is to write, edit or tighten text a person will read. Not for code or code changes, for finishing a branch (fox-dev:ship), or for prompts, skills and CLAUDE.md files written for agents (fox-dev:write-for-agents).
---

# Prose

Write for a reader who is busy and capable. Say the thing, show the evidence, stop.

## Before writing

- **Name the reader and what they do next.** Someone bisecting reads the commit; someone deciding whether to install reads the README; someone deciding what to do next reads the report. Write for that moment.
- **Lead with the point**: the answer, the outcome, the change. Background comes after, and only if the reader needs it.

## Sentences

- Short, active and concrete: "The parser drops trailing commas", not "Trailing commas are not being handled correctly".
- One idea per sentence, one topic per paragraph.
- Cut filler (basically, simply, really, in order to), warm-up phrases ("It is worth noting that"), stacked hedges, restating the question, and closing summaries that repeat the body.
- Plain words over grand ones: use, not utilize; help, not facilitate; start, not commence.
- Specifics over adjectives: "fails on files over 2 GB", not "has issues with large files".
- One name per thing. If it is a "job" in the first paragraph, it is not a "task" in the third.
- No hype, emoji or exclamation marks unless the project's own voice uses them.

## Structure

- Headings and lists when the reader scans or follows steps; paragraphs when the text is an argument.
- List items share a grammatical form. A list of one is a sentence.
- Tables only for comparing several things on the same attributes.
- Commands, paths and identifiers in backticks. Commands must run as pasted.

## By kind

- **Commit message**: a subject that says what changes, in the repo's existing style (read `git log`), about 50 to 72 characters; a body that says why and names any non-obvious consequence.
- **PR description**: what and why in two or three lines, how it was tested, where reviewers should look, known risks.
- **README and docs**: what it is and who it is for, then a quick start that works, then reference. Every example has been run.
- **Changelog**: user-visible changes only, grouped as Added, Changed, Fixed, Removed, newest first.
- **Report or status**: outcome first (done, partial, blocked), then the evidence, then what is left and what you need from the reader. Say what you did not check.

## Edit pass

1. Read it once as the reader, start to finish.
2. Delete each sentence the reader does not need, then each word.
3. Check every claim, number, version, command and link against the source.
4. The project's style guide, CONTRIBUTING or existing docs beat these defaults.

## Common rationalizations

| Thought | Reality |
|---|---|
| "More detail is more helpful." | Detail the reader does not need hides the part they do. |
| "A summary at the end helps." | If the opening said it, the summary repeats it. |
| "Hedging is safer." | One accurate qualifier beats three vague ones. |
| "It reads fine to me." | You know what you meant. Read it as someone who does not. |

## With foxdb (when the `fox_*` tools are listed)

- `fox drift <doc>` lists code the doc cites that changed, moved or vanished, so you know what to reword.

Original fox-dev text (no upstream source).
