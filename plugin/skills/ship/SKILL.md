---
name: ship
description: "Finishes a branch: green suite, atomic commits, merge or PR, PR body. Use on \"ship\", \"open a PR\", \"write the PR description\" or \"commit this\", even when one commit looks enough."
---

# Ship

Take a finished branch to merged, PR'd, or parked, with nothing broken on the way.

## 1. Green first

Call the Skill tool with `fox-dev:verify`. If any gate fails, report it and stop; the options below come after a green suite.

## 2. Know where you are

- Current branch, base branch (confirm with the user if unclear), and whether this is a linked worktree (`git rev-parse --git-dir` vs `--git-common-dir`).
- `git status` clean apart from the intended change; no stray files.

## 3. Shape the commits

- **Atomic**: each commit is one logical change that builds and passes on its own. Split a messy tree with `git add -p` by concern (refactor, behaviour, tests, docs).
- **Messages** say why, not what the diff already shows. Follow the repo's convention.
- **Project commit rules override defaults**, for example "no attribution or co-author lines", sign-off requirements, or message formats in CLAUDE.md or CONTRIBUTING.

## 4. Offer the choice

Present exactly these, and do what the user picks:

1. **Merge locally** into the base: merge, re-run the suite on the result, then remove the worktree if you created one.
2. **Push and open a PR**: see below.
3. **Keep the branch as is**: report the branch name and worktree path.

Discarding work needs the user to confirm by name.

## 5. Push safely

- `git fetch` first and check the remote base has not moved; rebase or merge if it has, and re-verify.
- **Never force-push** a shared branch without explicit permission. Prefer `--force-with-lease` even on your own branch.
- Pushing and publishing are side effects: confirm with the user unless they already asked for it.

## 6. The PR body

```markdown
## Summary
<the smallest visual that makes the point: pseudocode, call tree, component or file tree, Mermaid, or a diff sketch>

## Evidence
- **Before:** <failing test run, output or screenshot>
  **After:** <passing run, output or screenshot>

## Merge danger
**Door:** one-way | two-way. <why, if not obvious>
**Blast radius:** <one word>. <who or what could break: consumers, data, layouts, CLIs>
```

Keep prose brief, use the project's domain words, and skip preambles. Screenshots are the best evidence for visual changes; test output for everything else. A one-way door (data migration, deleted API, published format) states its rollback plan or why there is none.

Done when the chosen option is complete and reported with the branch, commit range and PR link if any.

## With foxdb (when the `fox_*` tools are listed)

- `fox_graph rel=impact` with no target gives the blast radius line; `fox drift` lists docs the branch made stale.

Derived from: superpowers finishing-a-development-branch; mattpocock-skills pr (Summary menu from Dex Horthy's show-me, humanlayer/skills); agent-skills git-workflow-and-versioning, shipping-and-launch (MIT, see NOTICE.md).
