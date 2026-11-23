# Notices

fox-dev is Copyright (c) 2026 ManavA and released under the MIT License (see LICENSE).

Thirteen of its fifteen skills and both agents are a condensed rewrite of skills from three
MIT-licensed packs. Most text is rewritten, but structure, checklists and some phrases come
from the originals, so each upstream notice is reproduced in full below. Each derived
SKILL.md names its sources in a "Derived from" line. The `ui` and `prose` skills are
original fox-dev text, apart from one browser-safety paragraph in `ui` that follows
agent-skills' browser-testing-with-devtools.

This file and LICENSE ship at the repository root and inside the installable plugin
directory (`plugin/NOTICE.md`, `plugin/LICENSE`), so every installed copy carries the
notices. `scripts/check.sh` fails if the two copies differ.

| Upstream | Version / commit | Repository |
|---|---|---|
| mattpocock-skills | 1.3.1 | https://github.com/mattpocock/skills |
| superpowers | 7.0.0 | https://github.com/obra/superpowers |
| agent-skills | 0.6.17, commit 8c99fa3 | https://github.com/addyosmani/agent-skills |

## Which fox-dev file derives from which upstream skill

| fox-dev | mattpocock-skills | superpowers | agent-skills |
|---|---|---|---|
| shape | grilling, grill-me, grill-with-docs, to-spec, prototype, to-questionnaire | brainstorming | idea-refine, interview-me, spec-driven-development |
| design | codebase-design (+ DEEPENING, DESIGN-IT-TWICE), improve-codebase-architecture, domain-modeling | writing-plans (file structure) | api-and-interface-design, documentation-and-adrs |
| plan | to-tickets, wayfinder | writing-plans | planning-and-task-breakdown, deprecation-and-migration |
| build (+ tests.md, mocking.md) | tdd (+ tests.md, mocking.md), implement | test-driven-development, executing-plans | test-driven-development, incremental-implementation |
| swarm (+ brief.md) | implement-spec | subagent-driven-development, dispatching-parallel-agents, using-git-worktrees | references/orchestration-patterns |
| debug (+ techniques.md) | diagnosing-bugs | systematic-debugging (+ root-cause-tracing, defense-in-depth, condition-based-waiting) | debugging-and-error-recovery, performance-optimization, ci-cd-and-automation |
| review (+ checklists) | code-review | requesting-code-review, receiving-code-review | code-review-and-quality, code-simplification, doubt-driven-development, security-and-hardening, references/security-checklist, performance-checklist, accessibility-checklist |
| verify | | verification-before-completion | references/definition-of-done, constraint-driven-development |
| ship | pr | finishing-a-development-branch | git-workflow-and-versioning, shipping-and-launch |
| handoff | handoff | executing-plans (ledger) | context-engineering |
| retro | retro | | |
| research | research | | source-driven-development |
| write-for-agents (+ evals.md) | writing-for-agents (+ SKILL-MECHANICS) | writing-skills | docs/skill-anatomy, evals |
| agents/reviewer, agents/implementer | | requesting-code-review (code-reviewer.md) | agents/code-reviewer, agents/test-engineer |
| ui | | | browser-testing-with-devtools (one paragraph) |
| prose | | | |

`ui` and `prose` are otherwise written from scratch; they do not copy Anthropic's
`frontend-design` skill or the text of *The Elements of Style*.

## License terms of the upstreams

Each upstream's LICENSE was checked at the version or commit above (and at its current
default branch): all four are the standard MIT License, with no other license files in
those repositories. MIT allows use, modification, redistribution, sublicensing and sale,
including commercial redistribution of derived text, on one condition: the copyright notice
and permission notice stay in all copies or substantial portions. This file meets that
condition. MIT grants no trademark rights; the upstream names appear here only to credit
the sources and imply no endorsement.

## Relationship to fox-db

fox-db (https://github.com/ManavA/fox-db) is a separate project under AGPL-3.0-or-later.
fox-dev contains no fox-db code. Its "With fox-db" blocks only name fox-db commands and tools
to call when they are installed, so fox-dev's MIT license is unaffected by fox-db's.

## Second-hand credit

The PR Summary menu in `ship` (pseudocode, call trees, component and file trees, Mermaid,
diff sketches) reaches fox-dev through mattpocock-skills' `pr`, which took it from
Dex Horthy's `show-me` skill in humanlayer/skills (https://github.com/humanlayer/skills),
MIT licensed, Copyright (c) 2026 HumanLayer.

superpowers' `writing-skills` ships a copy of Anthropic's skill-authoring best-practices
guide. fox-dev copies none of it; `write-for-agents` links to Anthropic's published docs.

## mattpocock-skills

```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## superpowers

```
MIT License

Copyright (c) 2025 Jesse Vincent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## agent-skills

```
MIT License

Copyright (c) 2025 Addy Osmani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## humanlayer/skills (show-me)

```
MIT License

Copyright (c) 2026 HumanLayer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
