# fox-dev compared with the three originals

This note is for deciding whether fox-dev should replace the packs it was built from. It covers each of the 15 fox-dev skills: the 13 that absorb original skills, compared against them, then the two on-demand skills `ui` and `prose`, which are original text. Then come a full coverage audit of every mattpocock-skills and agent-skills item, the originals that were not carried over, and context cost.

Sources: mattpocock-skills 1.3.1 (P), superpowers 7.0.0 (S), agent-skills 0.6.17 at commit 8c99fa3 (O). Sizes are for the original SKILL.md file alone (lines / characters); reference files are mentioned where they matter. "Listed" means the skill is model-invocable, so its description sits in the always-loaded skill listing.

Three owner decisions shape the draft:

- **Test-first is firm, with no deletes.** The failing test comes first. If code came first, write the test and show it fails on the old code; never delete the work.
- **Execution defaults to the main session.** Parallel lean workers are used only when a plan has 2 or more independent tasks.
- **Review covers spec, standards and blast radius**, and hands the line-level bug hunt to the built-in `/code-review`.

One deviation from the design: the design counted 9 model-invoked skills, but its own descriptions give 11 (every skill except `handoff`). The draft lists 11, and the later `ui` and `prose` skills bring the listed total to 13. Making `research` and `write-for-agents` user-invoked would save about 400 characters of listing, but they would then stop firing on their own.

---

## 1. shape

**Replaces**

- **S brainstorming** (225 lines / 10,073 chars, plus a visual-companion server and a builder-check prompt). It skips the conversation when the request is already clear. Otherwise it offers a "skip questions" exit, then asks one question per message in plain language. It covers goals, non-goals, prior art and current state, offers recon and a browser-based visual companion for mockups, plays understanding back in 200-300 word chunks, and writes a design doc. Its description says "You MUST use this before any creative work".
- **P grilling** (30 / 2,037). It maps decisions as a design tree, asks the whole frontier each round as numbered questions with recommended answers (worded so "yes" accepts), looks facts up via subagents instead of asking, and finishes when the frontier is empty and the user confirms.
- **P grill-me** (7 / 157, user-only) and **P grill-with-docs** (7 / 247, user-only). These are one-line wrappers: the first calls grilling; the second calls grilling plus domain-modeling.
- **P to-spec** (75 / 3,043, user-only). It synthesises the conversation into a spec with no interview: problem, solution, a long user-story list, implementation decisions, testing decisions with seams confirmed with the user, and out of scope. It publishes to the issue tracker with a triage label.
- **P prototype** (26 / 2,923, plus LOGIC.md and UI.md). Throwaway code that answers one question. The logic branch is a single HTML file driving a pure reducer or state machine; the UI branch is switchable variants on one route. The prototype is captured on a throwaway branch.
- **O idea-refine** (195 / 9,374, plus scripts and frameworks). Divergent then convergent ideation for vague ideas. It outputs a one-pager with problem, direction, assumptions to validate, MVP scope and a "not doing" list.
- **O interview-me** (235 / 15,034). One question at a time, each with a guess, separating "want" from "should want". It restates intent in the user's words and stops at about 95% confidence with an explicit yes.
- **O spec-driven-development** (307 / 16,869). A gated workflow (scope check with capability map, specify, plan, tasks, implement). Its spec covers objective, tech stack, commands, structure, code style, testing strategy, boundaries, success criteria and open questions.

**New skill.** Listed. Description: "Turns an idea or change request into an agreed spec. Use when asked to build, add or change a feature, or on "grill me", "interview me", "spec this", "let's design", even when the request looks clear enough to start coding directly."

Body (85 lines, plus LOGIC.md and UI.md):

0. A clear-task exit, plus a "skip the questions" exit that ends with a stated assumptions list.
1. Look facts up yourself, using a read-only subagent for wide sweeps.
2. Grilling rounds over the design-tree frontier, with numbered questions and recommended answers.
3. A running assumptions list.
4. A prototype branch, when only running code can answer the question.
5. A one-page spec: objective, non-goals, acceptance criteria, test seams, commands, global constraints, decisions, open questions, assumptions.

It then calls `plan` or `build`.

**Kept, merged, dropped**

- *Interview style.* The rounds format is Pocock's: faster than one-question-per-message, and "yes" accepts the recommendation. The anchoring advice (ask about a real moment, offer a guess) comes from brainstorming and interview-me. The clear-task exit and the skip offer come from brainstorming.
- *Spec template.* Osmani's commands and constraints are merged with Pocock's seams. User stories are dropped as a mandatory long list; acceptance criteria carry that job.
- *Dropped:*
  - the visual-companion server (heavy, rarely needed);
  - divergent-ideation frameworks;
  - the capability map;
  - the 95% confidence number;
  - mandatory tracker publishing (now optional);
  - brainstorming's 200-300 word playback chunks.

**Added in 0.1.1 (coverage audit):** a divergent step for still-vague ideas (3 to 5 directions, each with its bet and what would kill it; from idea-refine), a restatement check in the user's words (interview-me), a questionnaire for decisions only someone else can answer (to-questionnaire), and delta specs plus a Deferred list for changes to shipped features (spec-driven-development). The ideation frameworks files stay dropped.

**Behaviour differences**

- **Rounds, not single questions.** brainstorming and interview-me ask one question per message. shape asks a numbered round of several questions, so sessions are shorter but each message is denser.
- **No forced design doc for clear tasks.** brainstorming's description fires on any creative work. shape's description fires on feature requests, but its body exits at once for clear tasks.
- **Seams in the spec.** Test seams are recorded in the spec; this is where `build` later finds them.
- **No visual companion.** For visual questions, the UI prototype is the substitute.

---

## 2. design

**Replaces**

- **P codebase-design** (114 / 6,066, plus DEEPENING.md and DESIGN-IT-TWICE.md). The vocabulary: module, interface, depth, seam, adapter, leverage, locality. The principles: the deletion test, the interface as the test surface, and "one adapter is a hypothetical seam". It covers designing for testability, rejected framings, dependency categories, and parallel design-it-twice subagents.
- **P improve-codebase-architecture** (71 / 5,998, user-only). It scans recent hot spots for deepening opportunities, writes an HTML report, then grills through the one the user picks.
- **P domain-modeling** (74 / 3,222, plus references). It actively maintains GLOSSARY.md and ADRs under `docs/adr/`, created lazily, with multi-context support via GLOSSARY-MAP.md.
- **O api-and-interface-design** (369 / 14,860). Hyrum's law, the one-version rule, contract first, consistent errors, validating at boundaries, and preferring addition over modification. Also long REST, pagination and TypeScript pattern catalogues.
- **O documentation-and-adrs** (320 / 12,562). ADR template and lifecycle, inline-comment guidance, and doc-drift detection.

**New skill.** Listed. Description: "Deep-module design vocabulary and checks. Use when deciding an interface, where a seam goes, how to make code testable, or when recording an ADR or glossary term, even when the structure question comes up mid-task."

Body (63 lines, plus DEEPENING.md):

- the vocabulary, with Hyrum's-law "contract" added;
- seven checks;
- testability rules;
- when to design it twice;
- how to find deepening opportunities (scoped to recent changes);
- when to write an ADR or a glossary term.

**Kept, merged, dropped**

- *Kept:* Pocock's vocabulary and checks, and his dependency categories (moved into DEEPENING.md together with the design-it-twice recipe). Osmani's contract-first and addition-over-modification rules sit alongside them.
- *Dropped:* the HTML architecture report, the REST and TypeScript catalogues, inline-comment style guidance, and the GLOSSARY-MAP multi-context layout. Creating a glossary is now optional.

**Added in 0.1.1 (coverage audit):** active domain-language work from domain-modeling (challenge conflicts with the glossary, sharpen fuzzy words, probe with scenarios, cross-check the code, record terms as they settle), domain-modeling's stricter ADR bar (all three of hard to reverse, surprising, a real trade-off), and improve-codebase-architecture's candidate fields and strength labels in prose instead of the HTML report.

**Behaviour differences**

- improve-codebase-architecture was a user-run session that ended in an HTML report. In fox-dev, finding deepening opportunities is a section of a reference skill and ends in a prose list.
- Glossary upkeep happens only when the repo already has one or the user wants one. Pocock's skills read GLOSSARY.md in almost every workflow.

---

## 3. plan

**Replaces**

- **S writing-plans** (204 / 10,317). Plans for an engineer with no context. It maps the file structure first, then right-sized tasks. Each task carries Files, Interfaces (consumes/produces) and bite-size steps with full test and implementation code plus expected output. The header holds Global Constraints and Review Focus. Plans are saved under `docs/superpowers/plans/` and executed via subagent-driven-development or executing-plans.
- **P to-tickets** (105 / 5,804, user-only). Tracer-bullet vertical slices, each with blocking edges, sized for one context window, with prefactoring first and expand-contract for wide refactors. The user is quizzed on granularity and edges, then tickets are published to the tracker or written as one local file per ticket.
- **O planning-and-task-breakdown** (259 / 10,593). Plan mode, a dependency graph, vertical slicing, tasks with acceptance criteria and verification, checkpoints between phases, and sizing guidelines. Saved to `tasks/plan.md`.
- **P wayfinder** (128 / 12,380, user-only). A decision-ticket map on the tracker for work bigger than one session and still foggy: destination, decisions so far, not yet specified, out of scope; typed tickets (research, prototype, grilling, task), claimed one per session.
- **O deprecation-and-migration** (252). The deprecation decision, advisory vs compulsory, build the replacement first, announce with a migration guide, migrate consumers incrementally, remove at zero usage, zombie code.

**New skill.** Listed. Description: "Breaks an agreed spec into vertical, test-first tasks with dependencies. Use BEFORE exploring code when work spans more than one commit or file, or on "plan", "break this down", "tickets", or planning a migration, deprecation or removal, even when the steps seem obvious." (The "BEFORE exploring" clause and the migration trigger were added in 0.1.1, when a deprecation prompt explored instead of firing.)

Body (75 lines):

1. Read the spec and the code first, and spot a prefactor.
2. Slice vertically (risky parts first; expand-contract for wide refactors; right-sizing).
3. Write each task: Blocked by, Files, Interfaces, Acceptance, Test first, Verify.
4. Add the plan-wide Global constraints and Review focus sections.
5. Check the graph with the user.

The plan is saved to `docs/plans/`. It hands off to `build`, or to `swarm` when 2+ independent tasks exist.

**Kept, merged, dropped**

- *Kept:* the task fields merge superpowers' Interfaces block with Pocock's blocking edges and Osmani's acceptance and verification. Global Constraints and Review Focus are kept from superpowers. Pocock's vertical-slice rules, expand-contract and the user quiz are kept.
- *Dropped:*
  - full code inside plans, the biggest token cost in superpowers plans;
  - the plan header boilerplate;
  - the "REQUIRED SUB-SKILL" line;
  - checkbox step lists;
  - mandatory tracker publishing;
  - Osmani's phase checkpoints.

**Added in 0.1.1 (coverage audit):** removing or replacing things others depend on (deprecation-and-migration), an integration branch when expand-contract batches cannot stay green alone (to-tickets), and "Too big and too foggy to slice", a condensed wayfinder decision map. Tracker-native claims and blocking stay dropped.

**Behaviour differences**

- **No code in plans.** Plans describe interfaces and tests, not code. Superpowers' inline executor relies on transcribing plan code; fox-dev's `build` writes the code test-first instead.
- **Default handoff is inline.** The next step is `build` in the same session, not a subagent per task.

---

## 4. build

**Replaces**

- **S test-driven-development** (330 / 9,556, plus writing-good-tests.md). The Iron Law: no production code without a failing test first. Code written before its test must be deleted ("delete means delete"). It covers red-green-refactor with mandatory verify-red and verify-green, good and bad examples, and a long rationalisation list. It applies always, except for prototypes, generated code and config.
- **S executing-plans** (373 / 20,249). Inline plan execution with a ledger, "rulings, not stalls", four stop conditions, continuous execution without check-ins, TDD per task, one final fresh review and one fix pass, then finishing-a-development-branch.
- **P tdd** (38 / 3,621, plus tests.md and mocking.md). Good tests use the public interface. Tests go only at seams agreed with the user before any test is written. Anti-patterns: implementation-coupled, tautological, horizontal slicing. Red before green, one slice at a time; refactoring belongs to review, not to the loop.
- **P implement** (17 / 622, user-only). Implement a spec or tickets via tdd at agreed seams, run typecheck and tests, call code-review, then commit.
- **O test-driven-development** (400 / 16,756). Discover the stack's test commands first, then red-green-refactor, the Prove-It pattern for bugs, the test pyramid and sizes, DAMP over DRY, real over mocks, Arrange-Act-Assert, and browser testing.
- **O incremental-implementation** (249 / 9,329). Thin verifiable slices (vertical, contract-first, risk-first), simplicity first, scope discipline, staying compilable, feature flags, safe defaults, and commit per slice.
- **O /build and /test commands** (user-only, no listing cost). `/build auto` runs the whole plan after one approval.

**New skill.** Listed. Description: "Test-first implementation: failing test, watch it fail, minimal code, commit per slice. Use when implementing a task or plan, fixing a bug, adding tests or changing behaviour, even when the code is pasted inline and the fix looks obvious."

Body (72 lines, plus tests.md and mocking.md):

0. Set up: find the repo's own commands, run a baseline, start a ledger.
1. The red-green loop at the agreed seam: watch it fail for the right reason, minimal code, commit per slice, refactor separately.
2. "Code came first": keep the code and prove the test fails on the old code (stash the implementation, run, restore).
3. Prove-It for bugs.
4. Test-quality rules and the preference order real > fake > stub > mock.
5. Rulings, not stalls, with the four stop conditions.
6. Finish: a done criterion, then `review` and `verify`.

**Kept, merged, dropped**

- *Kept:*
  - superpowers' "watch it fail" and verify-red;
  - Pocock's three anti-patterns and the seam rule;
  - Osmani's command discovery, Prove-It and mock ordering;
  - executing-plans' ledger, rulings and stop conditions.
- *Dropped:*
  - the delete-code rule (replaced, per the owner's decision);
  - the digraph;
  - the test-pyramid percentages and size model;
  - most JS examples (a few stay in tests.md);
  - browser testing;
  - feature-flag guidance;
  - Osmani's `/build auto` single-approval mode;
  - superpowers' worktree setup inside executing-plans (moved to swarm).

**Added in 0.1.1 (coverage audit):** a one-line catches/misses note when confirming a new seam (tdd), scope discipline, a green tree between slices and a default-off flag for merged unfinished work (incremental-implementation), and pointers to `review/security.md` and the performance loop in `debug/techniques.md` for sensitive or speed-focused slices.

**Behaviour differences**

- **No deletes.** superpowers deletes code written before its test. fox-dev keeps the code and requires a demonstrated failure on the pre-change code. That is weaker than "start over" (the test can be shaped to the code) but keeps work.
- **Seams confirmed only when new.** Pocock asks the user to confirm seams before any test. fox-dev asks only when the seam is a new interface, so there are fewer interruptions and less user control over where tests land.
- **Refactoring is a separate step.** It is not inside the red-green loop, matching Pocock rather than superpowers' red-green-refactor.
- **Inline by default.** No subagent per task. One final review, through `review`.

---

## 5. swarm

**Replaces**

- **S subagent-driven-development** (568 / 32,358, plus implementer, reviewer and re-review prompts and scripts). A fresh implementer subagent per task, then a task review (spec plus quality) using a generated review package. The fix loop resumes the implementer for rounds 1-3 and escalates to a stronger model for rounds 4-5. A final broad review follows. It includes model-selection rules, status codes (DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED) and ledger rules.
- **S dispatching-parallel-agents** (167 / 6,052). One agent per independent problem domain, with focused scope, goal, constraints and output, then review and integration. Not for related failures or shared state.
- **S using-git-worktrees** (167 / 6,803). Detect existing isolation, prefer native worktree tools, fall back to `git worktree add` in an ignored directory, run project setup and a baseline test.
- **P implement-spec** (40 / 2,780, user-only). An integration branch and a ticket frontier, with an implementer per worktree in the background, a merger subagent, a final code-review, a single fixer, and cleanup. Context pointers, not pasted context.
- **O references/orchestration-patterns** (370 lines) and the `/ship` fan-out. Patterns for parallel personas and merges.

**New skill.** Listed. Description: "Runs independent tasks in parallel with one writer per change and fresh reviewers. Use when a plan has 2+ independent tasks or several unrelated failures, even when doing them one by one looks simpler."

Body (69 lines, plus brief.md):

0. Fan out only for 2+ independent tasks with disjoint files; otherwise use `build`.
1. One writer per worktree, with isolation detection.
2. Pointer briefs, using the plugin's `implementer` and `reviewer` agents and dispatching the whole frontier in one message.
3. Handle the four statuses, and verify claims against the diff.
4. Per-task review and fix loop (3 rounds, then escalate). The orchestrator merges and recomputes the frontier.
5. Finish: one whole-branch `review`, one fix pass, `verify`, then remove the worktrees.

brief.md holds three templates: implementer, reviewer and parallel fixer.

**Kept, merged, dropped**

- *Kept:* superpowers' status codes, fix-loop escalation and per-task-plus-final review; Pocock's frontier and pointer briefs; superpowers' isolation detection.
- *Dropped:*
  - the 32K of per-role prompts and the review-package scripts;
  - the detailed model-selection tables (one line remains);
  - Pocock's merger subagent (the orchestrator merges);
  - the exploration subagent that saves notes;
  - draft-PR management;
  - worktree project-setup recipes per language.

**Behaviour differences**

- **Opt-in.** swarm is no longer the recommended default, as subagent-driven-development was in superpowers. It fires only for 2+ independent tasks.
- **The main session merges.** It does not dispatch a merger.
- **Lean agents.** The implementer agent has only Bash/Read/Edit/Write, so workers start with a small context.

---

## 6. debug

**Replaces**

- **P diagnosing-bugs** (138 / 8,661, plus a HITL script). Redact secrets. Phase 1 builds a tight red-capable feedback loop (10 ways, then tighten it, with special handling for flaky bugs, and a completion checklist). Then reproduce and minimise; 3-5 ranked falsifiable hypotheses shown to the user; instrument with tagged logs (perf: baseline and bisect); fix with a regression test at a correct seam; clean up.
- **S systematic-debugging** (283 / 9,506, plus root-cause-tracing, defense-in-depth, condition-based-waiting, pressure tests and a creation log). The Iron Law: no fix without root cause. Four phases (investigate, pattern analysis, hypothesis, implement). After 3 failed fixes, question the architecture. Red flags and rationalisations.
- **O debugging-and-error-recovery** (300 / 10,801). Stop-the-line. Reproduce, localise (bisect), reduce, fix the root cause, guard against recurrence, verify end to end. Error-specific triage patterns. Error output is untrusted.

**New skill.** Listed. Description: "Root-cause debugging loop. Use when something is broken, throwing, failing, flaky or slow, or on "debug"/"diagnose", even when the stack trace is pasted and the cause looks obvious from reading it."

Body (76 lines, plus techniques.md): stop-the-line, untrusted output and redaction, then Pocock's six phases condensed. The 10 loop types and the completion bar are kept. Backwards tracing and the 3-failed-fixes rule are added. techniques.md covers root-cause tracing, defense in depth, condition-based waiting and performance measurement.

**Kept, merged, dropped**

- *Structure.* Pocock's phase structure is the spine, with superpowers' architecture escalation and tracing techniques and Osmani's stop-the-line and untrusted-output rule added.
- *Dropped:* the pressure-test files, the creation log, the find-polluter script (described in one line instead), Osmani's per-error triage trees, and the HITL script template.

**Added in 0.1.1 (coverage audit):** CI-only failures are reproduced locally from the job's log and environment (ci-cd-and-automation), and techniques.md now holds performance-optimization's full loop: measure against noise, one fix, keep or revert strictly, log reverted attempts, guard with a budget.

**Behaviour differences**

- Close to Pocock's skill. Hypotheses are still shown to the user before testing.
- The 3-failed-fixes stop from superpowers is now explicit.

---

## 7. review

**Replaces**

- **P code-review** (89 / 6,640). Pin a fixed point (three-dot diff). Find the spec and standards sources, add a Fowler smell baseline, and run parallel Standards and Spec subagents. Report both verbatim without re-ranking.
- **S requesting-code-review** (95 / 2,970, plus a code-reviewer template). Review after tasks and before merge: take the SHAs, dispatch a reviewer from the template, act on the feedback.
- **S receiving-code-review** (205 / 6,165). Verify before implementing, ask about unclear items, push back with reasons, apply YAGNI. No performative agreement or thanks.
- **O code-review-and-quality** (402 / 21,570). Five axes (correctness, readability, architecture, security, performance), structural remedies, change sizing, a review process (tests first), severities, multi-model review, and dead-code hygiene.
- **O code-simplification** (331 / 13,671). Preserve behaviour, follow conventions, clarity over cleverness, Chesterton's fence, incremental steps, and language-specific examples.
- **O doubt-driven-development** (245 / 16,663). A fresh-context adversarial reviewer for a non-trivial decision while work is in flight, optionally via another CLI. Bounded loop.
- **O /review and /code-simplify commands** and **@code-reviewer** (102 / 4,040) and **@security-auditor** (112 / 4,984).

**New skill.** Listed. Description: "Reviews a diff against its spec and the repo's standards with fresh-context reviewers, and handles review feedback. Use on "review", a PR, a branch or a pasted diff, or when feedback arrives, even when the diff is short and the review looks quick to do by reading it."

Body (67 lines, plus axes.md, security.md, performance.md, a11y.md):

1. Pin the fixed point.
2. Gather the spec, the standards and the blast radius (callers and consumers of changed public symbols).
3. Dispatch two parallel `fox-dev:reviewer` agents: Spec, and Standards plus blast radius. Use Osmani's severities and give them the code, never the author's conclusion.
4. Hand the bug hunt to `/code-review`, and the cleanup to `/simplify`.
5. Report the axes separately.

It also sets a one-line adversary rule for irreversible steps, and a five-step feedback-handling section.

**Kept, merged, dropped**

- *Kept:* Pocock's two-axis separation and smell baseline (moved to axes.md); Osmani's five axes, severities, change sizing and checklists (condensed); superpowers' receiving rules; the simplification principles (as a reference pass).
- *Dropped:*
  - doubt-driven-development as its own skill (now one line);
  - multi-model and other-CLI review;
  - the language-specific simplification examples;
  - the security and accessibility auditor personas;
  - GitHub thread-reply mechanics.

**Added in 0.1.1 (coverage audit):** security.md gains SSRF, deletes on computed paths, shared-store rate limits, no stack traces to clients and security-and-hardening's ask-first list; axes.md gains dependency discipline, comment and dead-code checks from code-review-and-quality and documentation-and-adrs.

**Behaviour differences**

- **No bug hunt here.** fox-dev review does not look for line-level bugs itself; it tells the user to run `/code-review`. Without that step, a correctness bug can pass a fox-dev review. Osmani's skill covered correctness directly.
- **Blast radius is a review axis.** In Pocock and superpowers it was only implicit.
- **Severities.** Both axes use the same severity labels (Critical, Required, Optional, Nit). Pocock had none.

---

## 8. verify

**Replaces**

- **S verification-before-completion** (120 / 3,598). The Iron Law: no completion claim without fresh verification output. The gate: identify, run, read, verify, then claim. Red-flag wording, rationalisations, and patterns for tests, builds, requirements and agent delegation.
- **O references/definition-of-done** (67 lines). A standing checklist (correctness, quality, integration, documentation, ship-readiness) separate from acceptance criteria.
- **O constraint-driven-development** (319 / 22,153). Interview the user for a quality bar and write CONSTRAINTS.md. Install tooling, wire it into the lifecycle, guard the bar against agents lowering it (skipped tests, suppressions), and ratchet.

**New skill.** Listed. Description: "Evidence gate before saying done, fixed or passing. Use before any completion claim, commit, PR or report, even when the last run was green and the change was tiny."

Body (53 lines):

- the gate (identify, collect the project's gates, run, read, claim);
- the bar-lowering scan of the diff;
- the rule that agent claims must be re-checked;
- a short definition of done.

**Kept, merged, dropped**

- *Kept:* superpowers' gate, the "guard the bar" check from constraint-driven-development, and a short definition of done.
- *Dropped:* the CONSTRAINTS.md interview, tooling installation and ratchets, superpowers' "lying" rhetoric, and the long red-flag lists.
- *Added:* "do not re-run unchanged code", which superpowers did not allow.

**Behaviour differences**

- Slightly looser than superpowers: a re-run can be skipped when nothing it covers changed in this session, and the skip must be stated.
- The project's own gates (for example a release gate in CLAUDE.md) are read and used as the list.

---

## 9. ship

**Replaces**

- **S finishing-a-development-branch** (225 / 7,729). Verify the tests, detect the worktree, determine the base, offer exactly three options (merge locally, push and PR, keep), execute the choice, and clean up. Discard needs typed confirmation.
- **P pr** (170 / 4,107, plus CREDITS.md). The PR body template: a Summary visual chosen from pseudocode, call tree, component tree, file tree, Mermaid or diff sketch (from Dex Horthy's show-me); Evidence before and after; Merge Danger with one-way or two-way door and blast radius.
- **O git-workflow-and-versioning** (355 / 14,123). Trunk-based development, atomic commits, descriptive messages, separate concerns, change sizing, branching, worktrees, splitting a messy tree, and semver.
- **O shipping-and-launch** (336 / 11,336). Pre-launch checklists (quality, security, performance, accessibility, infrastructure, docs), feature flags, staged rollout, monitoring, error budget and rollback.
- **O /ship command.** Go/no-go with fan-out reviewers and a rollback plan.

**New skill.** Listed. Description: "Finishes a branch or a release: green suite, atomic commits, merge or PR, PR body, version and tag. Use BEFORE exploring code on "ship", "open a PR", "write the PR description", "commit this" or "cut a release", even when one commit looks enough." (Release, tag and "BEFORE exploring" were added in 0.1.1, when a release prompt explored instead of firing.)

Body (64 lines):

1. Green first, via `verify`.
2. Know the branch, base and worktree.
3. Atomic commits, with project commit rules overriding the defaults (for example "no attribution lines").
4. The three-option menu.
5. Safe push: fetch first, never force-push a shared branch without permission, confirm side effects.
6. The PR body template, with the Summary menu shortened to one line.

**Kept, merged, dropped**

- *Kept:* superpowers' flow and menu, Pocock's PR template, and Osmani's atomic-commit rules.
- *Kept since 0.1.1:* a short Releases and launches section: semver, the changelog entry in the same change, tags as the source of truth, and staged launches with named signals, a rollback line and rollback steps.
- *Dropped:* Pocock's full Summary examples (the menu is kept as a list), the full launch checklists, the rollout threshold table, the error-budget gate, and the `/ship` go/no-go fan-out (one-way doors must state a rollback plan instead).

**Behaviour differences**

- **"Commit this" now fires ship.** That brings in the green-suite gate before a commit.
- **Fetch before push.** ship fetches and checks that the base has not moved. superpowers did not.

---

## 10. handoff

**Replaces**

- **P handoff** (16 / 940, user-only). A handoff doc in `$TMPDIR` with suggested skills, pointers rather than copies, and redaction. The argument tailors it to the next focus.
- **O context-engineering** (353 / 14,964). The context hierarchy (rules files, specs, source, errors, conversation), restartable session boundaries, and context-packing strategies.
- **S executing-plans' ledger**, the record that lets a session restart.

**New skill.** User-invoked only (`disable-model-invocation: true`), so it costs nothing in the listing. Description: "Compact the current session into a handoff document another agent can pick up."

Body (33 lines): eight sections (goal, state, next steps, open questions, rulings and failed approaches, pointers, suggested skills, how to verify), plus redaction and a done criterion.

**Kept, merged, dropped**

- *Kept:* Pocock's skill, with Osmani's restartable-session contents and the ledger's rulings added.
- *Dropped:* the rules-file templates and context-packing strategies.

**Behaviour differences**

- Still user-only, as in Pocock.
- The document is more structured: failed approaches and verify commands are now required sections.

---

## 11. research

**Replaces**

- **P research** (12 / 794). A background agent researches primary sources and writes one cited markdown file where the repo keeps notes.
- **O source-driven-development** (217 / 10,030). Detect stack versions, fetch official docs, implement documented patterns, and cite sources.

**New skill.** Listed. Description: "Answers a library, API or prior-art question from primary sources and saves cited notes. Use when the answer depends on docs, versions or external behaviour, even when you remember the API."

Body (33 lines): pin versions from the lockfile, state the question, use a background agent, follow claims to the owning source (source beats docs), write cited notes, and implement from the documented pattern.

**Kept, merged, dropped**

- *Kept:* Pocock's background agent and notes file, plus Osmani's version pinning and citations.
- *Dropped:* Osmani's per-framework doc URL lists.

**Behaviour differences**

- The description now fires "even when you remember the API". It may fire more often than Pocock's skill did.

---

## 12. write-for-agents

**Replaces**

- **P writing-for-agents** (81 / 10,882, plus SKILL-MECHANICS.md). Context pointers, the two loads, the information hierarchy, progressive disclosure, co-location, completion criteria, when to split, leading words, negation, and pruning (single source of truth, environment as cache, no-ops, sediment).
- **S writing-skills** (681 / 26,523, plus a copy of Anthropic's best-practices guide, persuasion principles, testing-with-subagents and graphviz conventions). TDD for skills: pressure scenarios, then watch the agent fail, then write the skill. Covers skill types, structure, search optimisation for descriptions ("Use when..."), and rationalisation tables.
- **O docs/skill-anatomy and evals/.** Required sections and the line budget. Evals in three tiers: structural, trigger routing, and behavioural via `claude plugin eval`, with must-fire and must-not-fire cases.

**New skill.** Listed. Description: "Writing skills, CLAUDE.md/AGENTS.md and agent briefs that agents follow. Use when creating or editing any of these, or a subagent prompt, even for a one-line change."

Body (61 lines, plus evals.md):

- pointers and the two loads;
- description rules (leading word, one trigger per branch, the "even when" clause, when-not-how, under 300 chars, user-invoked when only humans start it);
- body structure;
- wording rules (positive phrasing, single source of truth, no-ops, sediment);
- agent briefs;
- test-first for skills with must-fire and must-not-fire pairs.

evals.md describes the eval layout and grader types.

**Kept, merged, dropped**

- *Kept:* Pocock's levers condensed, superpowers' test-first-for-skills and rationalisation tables, and Osmani's eval pairs.
- *Dropped:* the 46K copy of Anthropic's guide (now a link to the published docs), persuasion principles, the graphviz conventions, and the TDD-mapping table.

**Added in 0.1.1 (coverage audit):** writing-for-agents' rules on when to split (by sequence only across a context boundary, by invocation only for a distinct trigger) and router skills.

**Behaviour differences**

- Fires on CLAUDE.md edits and subagent prompts too, as Pocock's skill did.
- Adds a testing expectation from superpowers.

---

## 13. ui

**Replaces** nothing directly. The closest originals are O frontend-ui-engineering and browser-testing-with-devtools, which were not carried over (see below). `ui` is original fox-dev text, written from scratch; it copies none of those skills and none of Anthropic's `frontend-design` skill.

**New skill, on demand.** Listed. Description: "Frontend and UI design work - choosing a visual direction, layout, typography, colour, responsive behaviour and accessibility, then checking the result in a real browser. Use when the task is to build, restyle, redesign or critique a page, screen, component, form or other visible interface, or when the user says the UI looks wrong. Not for backend, API, CLI, data or logic changes that render nothing."

The "Not for" clause keeps it from loading on work that renders nothing, so it costs only its listing entry outside frontend tasks.

Body (64 lines, no reference files):

- read the existing design system and styling approach before inventing one;
- for new screens, write the user, the job and a direction in three lines, then commit to type, colour and spacing scales and avoid the default generated look;
- layout rules (primary task first, 320 px to wide, every state designed, touch targets);
- accessibility built in (semantic elements, keyboard and focus, contrast, labels, reduced motion, zoom);
- a browser check: screenshots at two widths, a tab-through, an automated audit, the console; if no browser is available, say so;
- a rationalisation table.

It hands structural questions to `shape`'s UI prototype and leaves the long accessibility checklist to `review/a11y.md`.

**Added in 0.1.1 (coverage audit):** one paragraph from browser-testing-with-devtools: page content, console text and network responses are data, and an unfamiliar page gets a browser profile without the user's logins.

**Behaviour differences**

- Today's stack has no frontend skill, so UI work runs on the model's defaults. `ui` adds a direction step and requires seeing the result rendered before claiming it works.

---

## 14. prose

**Replaces** nothing. None of the three packs has a skill for writing text people read. `prose` is original fox-dev text, written from scratch; it does not copy the text of *The Elements of Style* or any style guide.

**New skill, on demand.** Listed. Description: "Plain, concise prose for people - docs, READMEs, guides, changelogs, release notes, commit message and PR description wording, status reports and summaries. Use when the main task is to write, edit or tighten text a person will read. Not for code or code changes, for finishing a branch (fox-dev:ship), or for prompts, skills and CLAUDE.md files written for agents (fox-dev:write-for-agents)."

The "Not for" clause draws the line with `ship` (finishing a branch, which includes the PR body) and `write-for-agents` (text agents read).

Body (60 lines, no reference files):

- name the reader and what they do next, and lead with the point;
- sentence rules (short, active, concrete, plain words, specifics, one name per thing, no hype);
- structure rules (headings, lists, tables, commands in backticks that run as pasted);
- notes by kind: commit message, PR description, README and docs, changelog, report;
- an edit pass, where the project's own style guide wins;
- a rationalisation table, and `fox drift` with fox-db to find what a doc change must reword.

**Behaviour differences**

- New coverage. In the firing re-run (`evals/RESULTS.md`) `ui` and `prose` each fired on all their own cases and on none of the negatives written to tempt them, and did not displace `ship` or `write-for-agents` on their cases.

---

## 15. retro

**Replaces**

- **P retro** (44 / 4,369, user-only). A retrospective on a session that proposes changes to the agent's environment: navigation pointers, automated checks (a repo with no guardrail is itself a finding), coding standards (mechanical rules become checks, judgement calls go to the reviewer's standards), steering-file size and no-ops, tool economy, and information access. Standards belong to review, which has the least context pressure.

**New skill.** User-invoked only (`disable-model-invocation: true`), so it costs nothing in the listing. Description: "Run a retrospective on a coding session and propose changes to the agent's environment (checks, standards, CLAUDE.md, tooling)."

Body (39 lines): read the session's transcript, diff and findings; look for candidates in the same six places; present them most severe first with evidence, change, location and cost; make nothing until the user picks. Wording changes go through `write-for-agents`.

**Kept, merged, dropped**

- *Kept:* Pocock's six categories, the mechanical-versus-judgement split, and the reviewer-holds-standards rule.
- *Dropped:* nothing of substance; the file-role notes are condensed to one line.

**Behaviour differences**

- Added in 0.1.1 after the coverage audit; before, retro was listed as "revisit later". Like `handoff` it never fires on its own.

---

## Agents

- **fox-dev:reviewer** (19 lines; tools Read, Grep, Glob, Bash). Zero context; returns `path:line - severity - issue - fix`. It derives from superpowers' code-reviewer template and Osmani's @code-reviewer. The design asked for read-only tools; Bash is included so it can run `git diff` and the test command, and the prompt forbids edits. Drop Bash if strict read-only matters more.
- **fox-dev:implementer** (16 lines; tools Bash, Read, Edit, Write). One task test-first in its worktree, with the no-delete rule. It derives from superpowers' implementer prompt and Osmani's @test-engineer.

---

## Full coverage audit (0.1.1)

Every item in mattpocock-skills and agent-skills, judged by its content (steps, rules, checklists, triggers) against the fox-dev text, not by name. **Full**: every key step and rule is in fox-dev, possibly condensed. **Partial**: the core is in, named parts are left out (the reason says which and why). **Omitted**: not in fox-dev, on purpose.

Versions checked: mattpocock-skills 1.3.1, the 27 skills its plugin.json ships (the local plugin cache matches the v1.3.1 tag); agent-skills 0.6.17 at 8c99fa3, whose default branch head is still 8c99fa3, so nothing has been added since the pin. Pocock has since tagged v1.3.2 (edits to existing skills, no new plugin skill); his default branch adds only an in-progress `software-factory` skill, outside the plugin.

### mattpocock-skills 1.3.1 (27 skills: 14 full, 7 partial, 6 omitted)

| Upstream | fox-dev | Coverage | Notes |
|---|---|---|---|
| grilling | shape step 2 | full | Design tree, frontier rounds, recommended answers, facts looked up by subagent, done when the frontier is empty and the user confirms. |
| grill-me (user) | shape | full | A wrapper that calls grilling. |
| grill-with-docs (user) | shape + design | full | grilling plus domain-modeling; design's domain-language section does the second half. |
| to-spec (user) | shape step 5 | partial | Synthesis without interview is shape's "already settled" exit; seams in the spec. The long user-story list is replaced by acceptance criteria, and tracker publishing is optional. |
| prototype | shape step 4 (+ LOGIC.md, UI.md) | full | Both branches, the shared rules and capture on a throwaway branch. |
| to-tickets (user) | plan | full | Tracer-bullet slices, blocking edges, prefactor first, expand-contract (with the integration-branch case), the user quiz. One plan file instead of one file per ticket; tracker optional. |
| wayfinder (user) | plan "Too big and too foggy to slice" | partial | Destination, decisions so far, not yet specified, out of scope, typed decision tickets, one per session. Dropped: tracker-native claims and blocking, refer-by-name, the research-branch convention. |
| tdd | build (+ tests.md, mocking.md) | partial | Good tests, anti-patterns, red before green, one slice, refactor outside the loop. Seams are confirmed only when new (owner decision), not before every test. |
| implement (user) | build | full | Typecheck and single tests as you go, full suite at the end, then review, then commit. |
| implement-spec (user) | swarm | partial | Integration branch, frontier, pointer briefs, background implementers per worktree, final review, single fix pass, cleanup. Dropped: the merger subagent (the orchestrator merges), the note-saving exploration subagent, draft-PR handling. |
| codebase-design | design (+ DEEPENING.md) | full | Vocabulary, deletion test, interface as test surface, one-versus-two adapters, testability, design it twice. The "rejected framings" list is not repeated. |
| improve-codebase-architecture (user) | design "Finding deepening opportunities" | partial | Hot-spot scoping, friction signs, deletion test, candidate fields and strength, ADR conflicts, grill the pick. The HTML report with diagrams becomes a prose list. |
| domain-modeling | design "Recording decisions", "Sharpening the domain language" | partial | Challenge, sharpen, scenarios, cross-check code, inline updates, the three-condition ADR bar. Dropped: the GLOSSARY-MAP multi-context layout and the format files; a glossary is created only when the user wants one. |
| diagnosing-bugs | debug (+ techniques.md) | full | All six phases, the ten loop types, the completion bar, tagged logs, the perf branch, the missing-seam finding. |
| code-review | review (+ axes.md) | full | Fixed point, spec and standards sources, the Fowler smell baseline, parallel subagents, verbatim per-axis report. A missing base defaults to the merge-base (stated) instead of asking. |
| pr | ship step 6 | full | Summary menu, evidence before and after, merge danger with door and blast radius. The worked Summary examples are condensed to the menu. |
| handoff (user) | handoff | full | Temp-dir doc, suggested skills, pointers not copies, redaction, tailored to the argument. |
| research | research | full | Background agent, primary sources, one cited notes file where the repo keeps notes. |
| writing-for-agents (+ SKILL-MECHANICS) | write-for-agents | full | Pointers, the two loads, disclosure, completion criteria, splitting, leading words, negation, pruning, invocation and router skills. |
| retro (user) | retro (new, user-invoked) | full | All six candidate categories and the reviewer-holds-standards rule. |
| to-questionnaire (user) | shape step 2 | partial | Ask only who and what is needed, then a themed one-idea-per-question file. Condensed to a paragraph; the full template is not shipped. |
| ask-matt (user) | none | omitted | Router; see the table below. |
| setup-matt-pocock-skills (user) | none | omitted | Tracker and label setup for Pocock's own flow. |
| triage (user) | none | omitted | Issue triage, outside the dev loop. |
| wizard | none | omitted | Human-step bash wizards; niche, ships a script template. |
| teach (user) | none | omitted | Teaching, not development. |
| wait-what (user) | none | omitted | A one-line prompt the user can type. |

### agent-skills 0.6.17 (26 skills: 8 full, 16 partial, 2 omitted)

| Upstream | fox-dev | Coverage | Notes |
|---|---|---|---|
| spec-driven-development | shape, plan | full | Scope check (one spec per subsystem), spec fields, gated flow into plan and build, delta specs and Deferred items. The capability-map template is not shipped. |
| idea-refine | shape (vague-idea step) | partial | How-might-we restatement, distinct directions with bets and killers, honest convergence, not-doing list as Non-goals. Dropped: the frameworks and rubric files, 5 to 8 variations. |
| interview-me | shape | partial | Guesses attached, specifics, restatement in the user's words, explicit confirmation. One question per message and the 95% confidence number are replaced by numbered rounds (a deliberate style choice). |
| planning-and-task-breakdown | plan | full | Dependency graph, vertical slices, acceptance and verification per task, sizing, parallel opportunities. Phase checkpoints are dropped; the graph check with the user stands in. |
| incremental-implementation | build | full | Thin slices, simplicity, scope discipline, compilable between slices, default-off flags, commit per slice. |
| test-driven-development | build (+ tests.md, mocking.md) | partial | Stack discovery, red-green, Prove-It, real over mocks, DAMP, arrange-act-assert. Dropped: the test-pyramid percentages and size model, browser testing (in `ui` and `debug`). |
| debugging-and-error-recovery | debug | full | Stop the line, reproduce, localise (bisect), reduce, root cause, guard, verify end to end, untrusted error output. The per-error triage trees are condensed into the loop list. |
| code-review-and-quality | review (+ axes.md) | partial | Five axes, tests first, severities, change sizing, structural remedies, dependency discipline, dead code. The line-level correctness hunt is handed to the built-in `/code-review` (owner decision); multi-model review is dropped. |
| code-simplification | review axes.md "Simplification pass", built-in `/simplify` | partial | Preserve behaviour, conventions, clarity, scope to the change, Chesterton's fence, one step at a time. Language-specific examples dropped. |
| doubt-driven-development | review (adversary before irreversible steps) | partial | One fresh-context adversary on irreversible decisions. The five-step claim/extract/doubt loop and other-CLI reviewers are dropped as too heavy for the default path. |
| source-driven-development | research | full | Version pinning, official docs, documented patterns, citations. Per-framework URL lists dropped. |
| api-and-interface-design | design | partial | Hyrum's law, contract first, error semantics, boundary validation, addition over modification, naming. Dropped: the REST, pagination and TypeScript pattern catalogues and the idempotency-key recipe (stack-specific). |
| documentation-and-adrs | design (ADRs), prose (READMEs, changelogs), review axes (comments), `fox drift` | partial | ADR template and lifecycle, comment rules, doc drift. OpenAPI and inline API-doc tooling are dropped. |
| context-engineering | handoff, write-for-agents | partial | Restartable session contents, rules files as pointers. The context-packing strategies and budget tactics are dropped; the harness compacts context itself. |
| constraint-driven-development | verify | partial | The project's gates and the bar-lowering scan of the diff. The CONSTRAINTS.md interview, tool installation and ratchets are dropped as a setup project of their own. |
| git-workflow-and-versioning | ship (+ prose for commit wording) | full | Atomic commits, messages that say why, splitting a messy tree, safe push, semver, tags, changelog in the same change. Trunk-based and branch-naming advice is left to the repo. |
| shipping-and-launch | ship step 7, verify definition of done, review checklists | partial | Flags and staged rollout, named signals against baseline, rollback line and steps. The threshold table, error-budget gate and full pre-launch checklists are dropped. |
| deprecation-and-migration | plan | partial | The deprecation decision, replacement first, advisory by default, migration guide, owner migrates consumers, removal at zero usage, expand-contract. Strangler and adapter pattern write-ups and zombie-code notes are dropped. |
| performance-optimization | debug techniques.md, review performance.md | full | Measure, find the bottleneck, one fix, keep or revert against noise, log attempts, guard with a budget; checklist targets. |
| security-and-hardening | review security.md, build pointer | full | Threat model, always-do controls, ask-first list, SSRF, computed-path deletes, rate limits, secrets, dependencies, personal data, LLM features. Code patterns are not shipped. |
| accessibility-engineering | ui step 4 and 5, review a11y.md | partial | WCAG checks, automated audit plus keyboard and screen-reader passes. The standalone audit-and-remediate workflow with violation triage is not repeated. |
| frontend-ui-engineering | ui (original text) | partial | Design-system adherence, avoiding the generated look, type, colour, spacing, accessibility, responsive states. Component file structure and state-management advice are left to the project. |
| browser-testing-with-devtools | ui step 5, debug loop type 4 | partial | Screenshots, console, audit, untrusted page content, separate profile. Chrome DevTools MCP setup and network and performance panel walkthroughs are dropped. |
| ci-cd-and-automation | debug (CI-only failures), verify (project gates), retro (missing guardrails) | partial | Feeding CI failures back and reproducing locally. Pipeline authoring, deployment strategies and Dependabot setup are project infrastructure, not the loop. |
| observability-and-instrumentation | none | omitted | See the table below. |
| using-agent-skills | none | omitted | Router. |

### agent-skills agents, commands, references, hooks and docs

| Upstream | fox-dev | Coverage | Notes |
|---|---|---|---|
| agents/code-reviewer | agents/reviewer | full | Zero context, five axes via axes.md, `path:line` findings with severity. |
| agents/test-engineer | agents/implementer, build | partial | Test-first per task and test quality rules; a coverage-analysis persona is not kept. |
| agents/security-auditor | agents/reviewer + review/security.md | partial | The checklist replaces the persona. |
| agents/accessibility-auditor | agents/reviewer + review/a11y.md | partial | The checklist replaces the persona. |
| agents/web-performance-auditor | agents/reviewer + review/performance.md | partial | The checklist replaces the persona. |
| /spec | shape | full | Typed as `/fox-dev:shape`. |
| /plan (Gemini: planning) | plan | full | |
| /build (incl. `auto`) | build | full | build already works the whole plan without pausing between tasks. |
| /test | build | full | Includes Prove-It. |
| /review | review | full | |
| /code-simplify | review axes.md, `/simplify` | partial | As code-simplification. |
| /ship | ship | partial | The parallel persona fan-out and go/no-go synthesis are dropped; one-way doors state a rollback plan. |
| /a11y | ui, review a11y.md | partial | No dedicated audit command. |
| /webperf | debug techniques.md, review performance.md | partial | No dedicated audit command. |
| /constraints | verify | partial | As constraint-driven-development. |
| references/security-checklist | review/security.md | full | |
| references/performance-checklist | review/performance.md | full | |
| references/accessibility-checklist | review/a11y.md | full | |
| references/definition-of-done | verify | full | |
| references/testing-patterns | build/tests.md, mocking.md | partial | The useful patterns only. |
| references/orchestration-patterns | swarm | partial | Fan-out, one writer per tree, merge by the orchestrator. |
| references/observability-checklist | none | omitted | With observability-and-instrumentation. |
| hooks session-start, sdd-cache, simplify-ignore | none | omitted | fox-dev ships no hooks. |
| docs/skill-anatomy, evals | write-for-agents (+ evals.md) | full | Section rules, line budget, must-fire and must-not-fire evals. |

---

## Originals not carried over

The full per-item verdicts for mattpocock-skills and agent-skills are in the coverage audit above. Omitted on purpose:

| Source | Item | Why not |
|---|---|---|
| P | ask-matt (user) | A router. The harness already routes by description, and the README table is the human index. |
| P | setup-matt-pocock-skills (user) | Configures Pocock's tracker and labels; fox-dev reads each repo's own conventions and needs no setup. |
| P | triage (user) | An issue-tracker state machine for incoming issues and PRs; outside the dev loop. |
| P | wizard | Generates interactive bash wizards from a 200-line template for steps only a human can do. Niche, and fox-dev ships no scripts. |
| P | teach (user) | Teaching a concept; not development. |
| P | wait-what (user) | A one-line "re-pitch that" prompt the user can type; `prose` covers plain wording. |
| P | in-progress (chief-of-staff, claude-handoff, loop-me, setup-ts-deep-modules, writing-beats, writing-fragments, writing-shape) and misc (git-guardrails-claude-code, migrate-to-shoehorn, scaffold-exercises, setup-pre-commit) | Not exposed by his plugin.json. claude-handoff's idea is folded into `handoff`; the rest are personal or stack-specific setups. |
| S | using-superpowers | A SessionStart router that injects about 3.2K chars and says to invoke skills on a 1% chance. Dropped: it competes with the harness's own routing. |
| S | diagnosing-superpowers | Forensics on superpowers sessions; specific to that pack. |
| O | using-agent-skills (+ hooks/session-start.sh) | A router; its hook is not wired on Claude Code, and fox-dev has no session-start injection by design. |
| O | observability-and-instrumentation, references/observability-checklist | Production telemetry design (structured logs, metrics, tracing, alerts) is domain work, not the loop. `ship` names the signals to watch during a launch; `debug` covers instrumentation for diagnosis. |
| O | hooks sdd-cache, simplify-ignore | Opt-in hooks; fox-dev ships none, so nothing runs unless a skill is picked. |

---

## Context cost

The figures below were measured from the files. The listing cost of a skill is its name plus its description (the text the harness puts in the always-loaded skill list), summed over model-invocable skills only. Real listing overhead per entry adds a few characters for formatting.

**Always loaded, every session**

| Set | Listed entries | Characters |
|---|---|---|
| mattpocock-skills 1.3.1 | 11 of 27 skills (16 are user-only) | 2,306 |
| superpowers 7.0.0 | 15 skills | 2,690 |
| superpowers SessionStart injection (using-superpowers body) | n/a | about 3,190 |
| **Current stack (Pocock + superpowers)** | 26 | **about 8,200** |
| agent-skills, if installed | 26 skills + 5 agents | 12,074 |
| Current stack plus agent-skills | 57 | about 20,300 |
| **fox-dev** | 13 skills + 2 agents | **3,689** (`ui` and `prose` add about 800; `retro` and `handoff` are user-invoked and add nothing) |

Not counted above: the "Software development" router in the global CLAUDE.md (about 1.6K chars). If fox-dev replaces both packs, that section could shrink to a line or two.

**Bodies, loaded on use (SKILL.md only; references load on demand)**

| Set | Skills | SKILL.md total | With reference files |
|---|---|---|---|
| mattpocock-skills | 27 | 128,555 | about 204,000 |
| superpowers | 15 | 161,962 | about 358,000 |
| agent-skills | 26 + 5 agents | 389,098 | about 459,000, plus about 50K of shared references and commands |
| **fox-dev** | 15 + 2 agents | **about 64,400** | **about 90,500** |

**A typical idea-to-PR session**

This is shape, plan, build, review, verify and ship, with SKILL.md bodies only.

- **fox-dev:** 6,283 + 5,703 + 5,673 + 4,918 + 2,618 + 3,997 = about 29,200 chars (0.1.1; about 24,500 in 0.1.0 before the coverage additions). Reference files add a few thousand when opened.
- **Current stack, inline execution:**
  - superpowers brainstorming (10,073), writing-plans (10,317), test-driven-development (9,556), executing-plans (20,249), requesting-code-review (2,970), verification-before-completion (3,598) and finishing-a-development-branch (7,729);
  - Pocock tdd (3,621), code-review (6,640) and pr (4,107);
  - plus the using-superpowers injection (3,192).
  - Total: about 82,000 chars.
- **Current stack with subagent-driven-development** instead of executing-plans: about 94,000 chars in the main session, before the implementer and reviewer prompt files that each subagent loads.

So the same path costs about 35% of today's main-session text, and the always-loaded listing is under half of today's. `ui` and `prose` bodies load only on frontend or writing tasks.

---

## Not yet done

- **Evals** have since been run: firing results are in `evals/RESULTS.md`, outcome results in `evals/outcome/`.
- **Codex manifest** has since been added at `plugin/.codex-plugin/plugin.json` (skills only).
- **Your choice.** Installing fox-dev leaves the originals untouched. Whether it replaces them is up to you; using both at once splits which skill fires.
