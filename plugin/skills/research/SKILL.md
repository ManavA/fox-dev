---
name: research
description: Answers a library, API or prior-art question from primary sources and saves cited notes. Use when the answer depends on docs, versions or external behaviour, even when you remember the API.
---

# Research

Answer from **primary sources**: official docs for the version in use, the library's source, specs, first-party APIs and changelogs. Memory and secondary write-ups are leads, not answers.

## Steps

1. **Pin the stack.** Read the lockfile or manifest for the exact versions involved. An answer for the wrong major version is wrong.
2. **State the question** in one or two sentences, with what decision it feeds.
3. **Dispatch a background agent** for anything beyond a single lookup, so the main session keeps working. Its brief: the question, the versions, where to look first, and where to save notes.
4. **Follow each claim to the source that owns it**: the doc page for that version, the function in the source tree, the RFC section. When docs and source disagree, the source wins; note the disagreement.
5. **Write the notes** to one markdown file where the repo keeps such notes (match the existing convention; else `docs/research/<slug>.md`, and say where). Each claim carries its citation (URL with anchor or `path:line` at a tag or commit).
6. **Implement from the documented pattern**, and cite the source in a code comment only where the choice would otherwise look arbitrary.

Done when every claim in the notes has a primary-source citation and the original question has a direct answer at the top.

## Common rationalizations

| Thought | Reality |
|---|---|
| "I know this API." | APIs change between versions. Check the one in the lockfile. |
| "A blog post shows how." | Use it to find the official doc, then cite that. |
| "The docs are vague, I'll guess." | Read the source. |

## With foxdb (when the `fox_*` tools are listed)

- `fox_memory op=recall q=<topic>` and `fox_find kind=doc q=<topic>` for notes already written on this question.

Derived from: mattpocock-skills research; agent-skills source-driven-development (MIT, see NOTICE.md).
