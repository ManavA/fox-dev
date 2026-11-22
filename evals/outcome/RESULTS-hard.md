# Hard outcome eval on real foxdb gaps

Sonnet (claude-sonnet-5-5) at effort high, 150-turn / 4 USD per-run caps, Opus (claude-opus-5-5) low-effort blind judge. 3 tasks x 3 arms (none / current = superpowers 7.0.0 + mattpocock-skills 1.3.1 / foxdev) x 2 runs = 18 graded runs, 3 skills-enabled arms all confirmed loaded (59 skills visible in current). Each run: own git worktree of foxdb eb36a4c, own cargo target dir, scratch HOME. Spend: about 22.6 USD runs + 2.0 judges = 24.6 USD of the 80 cap. Driver and hidden tests: `hard/` (run_hard.py, hidden/, tasks.json, aggregate_hard.py, regrade_cpp.py); every run's diff: `hard/patches/`; per-run table: `hard/results/tables.md`.

Tasks (prompts in hard/tasks.json, 2-4 user-style sentences, no file hints):
1. c-typedef: C member calls and stores through typedef'd function-pointer fields (incl. typedef of typedef).
2. py-mro: Python self./super() method calls follow MRO (mixins, diamonds, subclass overrides).
3. cpp-recv: C++ member calls through typed receivers (locals, pointer/ref params, members, auto = Ctor(), make_unique) are certain, not guesses.
Hidden tests (Rust, tests/treesitter.rs style, inline fixture projects through code::run): 4 / 5 / 5, all fail or partly fail on unmodified main (c-typedef 3 of 4 fail, py-mro 4 of 5, cpp-recv 4 of 5). The c-typedef tests were also run against a plain-member rewrite of the fixtures as an oracle (4/4 pass), so they are satisfiable. py-mro and cpp-recv have no reference solution: they are satisfiable only in the sense that agents passed them.

## Per arm (mean of 6 runs)

| | none | current | foxdev |
|---|---|---|---|
| all hidden tests pass | 6/6 | 6/6 | 6/6 |
| existing suite regressions (360+ tests, whole suite incl. agent edits) | 0 | 0 | 0 |
| clippy -D warnings / fmt clean | 6/6, 6/6 | 6/6, 6/6 | 6/6, 6/6 |
| judge correctness / readability / design / tests | 4.0 / 3.0 / 3.2 / 4.0 | 4.0 / 3.0 / 3.3 / 4.2 | 4.0 / 3.0 / 3.5 / 3.8 |
| tests added | 2.2 | 2.2 | 3.2 |
| cost per run (USD) | 1.16 | 1.27 | 1.33 |
| wall time per run (s) | 961 | 1227 | 1327 |
| turns (two runs report 1 because a background-wait notification created a second result event; use tool calls) | 42 | 33 | 39 |
| Skill calls | 0 | 1 in 6 runs (superpowers:test-driven-development, py-mro r2) | 0 |
| subagents spawned | 0 | 0 | 0 |

## Reading

- Skills essentially did not fire: 1 Skill call in 18 runs, even at effort high on 200-700 line multi-file changes. Tests-before-source ordering was detected in 1 run (foxdev py-mro r2). So the arms are again almost the same agent.
- Outcomes did not differ. Every run passed every hidden test and the whole existing suite, with clippy and fmt clean. Judge scores are within 0.3 on every axis (design 3.2 / 3.3 / 3.5 is within single-judge noise). Cost: current +10% and foxdev +15% over none per run, wall time +28% / +38% (CPU contention from 5 parallel runs makes wall time noisy).
- Hard in size, not in difficulty: runs took 27-63 turns and 200-700 diff lines, but Sonnet solved all of them. The hidden tests, graded with the existing 360-test suite, did not separate arms. These tasks are too easy for process to matter, with one caveat: cpp-recv and py-mro hidden tests were written from my spec, and no run was rejected by them.
- Mutation score was not measured: cargo-mutants is not installed here (and building it plus mutating a 2.7k-line file is not quick). Coverage not measured for Rust. Substitutes: tests added per run (2-3 on average; all runs added tests to tests/treesitter.rs, no existing test was edited or deleted).

## Caveats and corrections

- Task 2 as briefed (an optional semantic tier) is already implemented in foxdb (src/vectors.rs, feature `vectors`, model2vec, tests/vectors.rs, docs/architecture.md), so hidden tests through config + CLI would pass on unmodified main. I replaced it with cpp-recv (a gap from the handoff's known-gaps list). The semantic prompt was not run.
- One hidden test of cpp-recv over-specified (it assumed the untyped receiver would not be counted); all six runs failed it identically (4/5). I fixed the test and regraded all six runs (5/5); both versions are kept in each grade.json (hidden_original).
- The original task list used a typedef task and a positional/macro-initializer task; the latter was dropped on the owner's update and its hidden test is not in this suite.
- turns/cost: cost is cumulative and correct; turns is wrong for the two runs noted above.
- Run records live in the session scratchpad (runs/*/grade.json, out.jsonl transcripts), not committed; patches and tables are.
