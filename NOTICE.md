# Notices

fox-dev is a condensed rewrite of skills from three MIT-licensed packs. Most text is
rewritten, but structure, checklists and some phrases come from the originals, so each
upstream notice is reproduced in full below. Each derived SKILL.md names its sources in
a "Derived from" line.

| Upstream | Version / commit | Repository |
|---|---|---|
| mattpocock-skills | 1.3.1 | https://github.com/mattpocock/skills |
| superpowers | 7.0.0 | https://github.com/obra/superpowers |
| agent-skills | 0.6.17, commit 8c99fa3 | https://github.com/addyosmani/agent-skills |

## Which fox-dev file derives from which upstream skill

| fox-dev | mattpocock-skills | superpowers | agent-skills |
|---|---|---|---|
| shape | grilling, grill-me, grill-with-docs, to-spec, prototype | brainstorming | idea-refine, interview-me, spec-driven-development |
| design | codebase-design (+ DEEPENING, DESIGN-IT-TWICE), improve-codebase-architecture, domain-modeling | writing-plans (file structure) | api-and-interface-design, documentation-and-adrs |
| plan | to-tickets | writing-plans | planning-and-task-breakdown |
| build (+ tests.md, mocking.md) | tdd (+ tests.md, mocking.md), implement | test-driven-development, executing-plans | test-driven-development, incremental-implementation |
| swarm (+ brief.md) | implement-spec | subagent-driven-development, dispatching-parallel-agents, using-git-worktrees | references/orchestration-patterns |
| debug (+ techniques.md) | diagnosing-bugs | systematic-debugging (+ root-cause-tracing, defense-in-depth, condition-based-waiting) | debugging-and-error-recovery |
| review (+ checklists) | code-review | requesting-code-review, receiving-code-review | code-review-and-quality, code-simplification, doubt-driven-development, references/security-checklist, performance-checklist, accessibility-checklist |
| verify | | verification-before-completion | references/definition-of-done, constraint-driven-development |
| ship | pr | finishing-a-development-branch | git-workflow-and-versioning, shipping-and-launch |
| handoff | handoff | executing-plans (ledger) | context-engineering |
| research | research | | source-driven-development |
| write-for-agents (+ evals.md) | writing-for-agents (+ SKILL-MECHANICS) | writing-skills | docs/skill-anatomy, evals |
| agents/reviewer, agents/implementer | | requesting-code-review (code-reviewer.md) | agents/code-reviewer, agents/test-engineer |

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
