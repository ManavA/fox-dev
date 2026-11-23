# Skill-firing comparison: current stack vs fox-dev (2026-11-21)

Setup: Claude Code 2.1.329, model claude-sonnet-5-5, scratch HOME with subscription credentials only, `--setting-sources project`, a tiny Python git repo as cwd, tools Skill/Read/Grep/Glob only, `--max-turns 2`, 2 samples per case. 32 cases (24 should-fire, 2 per fox-dev skill; 8 controls), 128 runs, about $2.70.
Arm A: superpowers 7.0.0 + mattpocock-skills 1.3.1 (`--plugin-dir` from the plugin cache). Arm B: `plugin/` only.
Grading: first Skill tool call must be a plugin skill in the expected family (A: see FAM in analyze.py; B: the same-named fox-dev skill). Built-in bare-name skills (`code-review`, `init`, `debug`, `verify`) count as misses. Reproduce with `run_firing.py` and `analyze.py` in this directory; per-run grades are in `graded-*.json`.

## Hit rate (first Skill call in family, 4 runs per family per arm)

| family | A current | B fox-dev |
|---|---|---|
| shape | 4/4 | 2/4 |
| plan | 4/4 | 4/4 |
| build | 0/4 | 0/4 |
| debug | 4/4 | 4/4 |
| design | 4/4 | 4/4 |
| review | 3/4 | 4/4 |
| ship | 4/4 | 4/4 |
| verify | 4/4 | 4/4 |
| research | 0/4 | 4/4 |
| swarm | 4/4 | 2/4 |
| write-for-agents | 0/4 | 4/4 |
| handoff | 0/4 | 0/4 |
| overall | 31/48 | 36/48 |

False fires on 16 control runs: A 1 (`using-superpowers` on a question about TTLCache.get), B 0.

First-request prompt size (input + cache read + cache write, median over 64 runs): A about 10,930 tokens, B about 8,730 tokens (B is 2,200 lower).

## Where they disagree
- shape-1 "add a rate limiter to this API": A fires brainstorming both times, B fires nothing (explores the code, then stops at the turn cap). shape-2 (interview me): A grilling, B shape.
- swarm-1 (three unrelated chores in parallel): A dispatching-parallel-agents both times, B nothing. swarm-2: both fire.
- research-1/2: B fires research 4/4, A never (the model searches locally instead).
- write-for-agents: B 4/4. A never fires a plugin skill (the built-in `init` fires for "write a CLAUDE.md", nothing for the subagent prompt).
- review-2: A fires requesting-code-review once and built-in `code-review` once.
- build and handoff: neither arm fires on any of 8 runs each. Handoff is user-invoked in both stacks, so a miss is expected; build never fires first because the model reads files before editing.

## Supplement with --max-turns 6
The 12 cases with a miss in either arm were rerun with 6 turns (2 samples; graded-6turn.json). It does not change the picture: build and handoff stay at 0 in both arms, B shape-1 stays at 0, B swarm-1 stays at 0, A research stays at 0; A review-2 goes to the built-in `code-review` both times.

## Description rewrite for shape and swarm (re-run, arm B only)
Both descriptions were rewritten to name the missed situations: shape now says to use it BEFORE exploring or writing code when asked to add, build or change a feature or behaviour (example "add a rate limiter to this API"); swarm now names "do these three unrelated chores in parallel" and "run separate agents on each failure". Both keep the "even when it looks quick to do directly" clause. No other skill was touched.
The scratch repo was recreated from scratch for this re-run (same case prompts, same driver with a new `--arms B` option, 2 samples, Sonnet), so the sample repo is similar but not identical to the first run.

| family | B before | B after |
|---|---|---|
| shape | 2/4 | 4/4 |
| swarm | 2/4 | 4/4 |
| controls (false fires) | 0/16 | 0/16 |
| overall (full arm-B run) | 36/48 | 38/48 |

In the full arm-B re-run, plan fell from 4/4 to 2/4 (plan-2 "migrate ITEMS to sqlite" fired nothing both times, 2 samples); the plan description was not changed, so this is probably sample-repo or run-to-run noise, but it is unconfirmed. build and handoff stay at 0/4 as before. Cost of the re-runs about $1.15.

## Caveats
- Only the first Skill call is graded; later calls are ignored. Tools were limited, so build prompts could not edit anything.
- The sample branch already contains the paginate fix, so build-2 (fix paginate) is partly confounded.
- ship and verify overlap by design; both arms passed their own prompts.
- 2 samples per case is small. Treat single-case differences as leads.
- The weekly subscription window showed 0.97 utilisation (allowed_warning) during the run; no run was rejected.

## Re-run with ui and prose (2026-11-22, arm B only)

fox-dev 0.1.0 with fourteen skills (the twelve above plus `ui` and `prose`). 40 cases: the 32 above, 2 should-fire cases each for `ui` and `prose`, and 4 negatives (`neg-*`: a backend argument, a docstring, a unit test, JSON output formatting) where `ui` and `prose` must not fire and any other skill or none is fine. 2 samples, 80 runs, same harness and turn cap, about $1.37. The sample repo is rebuilt by `make_workdir.py` (adds `templates/items.html` for the ui cases), so it is similar but not identical to the earlier ones. Per-run grades: `graded-14skill.json`.

| family | B |
|---|---|
| shape, plan, debug, design, review, ship, verify, research, swarm, write-for-agents | 4/4 each |
| build | 0/4 |
| handoff | 0/4 (user-invoked only) |
| ui | 4/4 |
| prose | 4/4 |
| original twelve families | 40/48 |
| all fourteen | 48/56 |
| controls (false fires) | 0/16 |
| negatives (ui or prose fired) | 0/8 |

`ui` and `prose` also never appeared as a later Skill call in any other case (ship-2, which writes a PR description, still fires `ship`; wfa-1, which writes a CLAUDE.md, still fires `write-for-agents`). plan-2, which fired nothing twice in the previous re-run, fired `plan` both times here, which supports the run-to-run noise reading. First-request prompt size: median about 9,050 tokens, up about 320 from the twelve-skill pack for the two new descriptions and still below arm A's 10,930 from the first run (different sample repo, so compare loosely).

Across the three arm-B runs the original twelve families scored 36, 38 and 40 of 48, against 31 for arm A in the one arm-A run.
