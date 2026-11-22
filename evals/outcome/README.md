# Outcome eval: none vs current stack vs fox-dev

Compares three Claude Code skill setups on real software tasks, judged on outcomes (correct code, tests, speed, cost), not on whether a skill fired.

Arms (each run is an isolated `claude -p`, scratch HOME holding only OAuth credentials, `--setting-sources project`, fresh copy of the task repo as cwd, Sonnet at low effort, 60 turns, 1.50 USD cap):
- `none`: no plugins.
- `current`: superpowers 7.0.0 + mattpocock-skills 1.3.1 (`--plugin-dir` from the plugin cache).
- `foxdev`: this repo's `plugin/`.

## Layout
- `tasks/<id>/`: `repo/` (the starting repo with its existing tests), `prompt.txt`, `hidden/` (acceptance tests, applied only at grading), `ref/` (reference solution overlay), `meta.json`, `verified.json`.
- `common.py`, `grade_lib.py`: repo prep, test running, grading (hidden tests, existing suite, coverage of changed lines, mutation score, ruff/mypy/tsc deltas, diff size, process notes from the tool order).
- `run_outcome.py`: driver (runs, grades, one blind Opus judge call per run, cost cap, halts on rate limits/permission denials).
- `verify_task.py`, `verify_mutants.py`: prove each task is solvable (reference passes hidden tests, baseline does not) and that the test-writing tasks' hidden mutants are killable.
- `aggregate.py`: tables and paired bootstrap differences.
- `results/`: per-run grades and diffs, aggregate tables.

## Setup (not committed)
`python3 -m venv pyenv && pyenv/bin/pip install pytest coverage ruff mypy` and `mkdir ts-deps && cd ts-deps && npm init -y && npm i @types/node typescript`. Node 22+ is needed (TypeScript runs through Node's type stripping and `node --test`).

## Tasks (10)
Features: py-feat-ttl, py-feat-table, ts-feat-range. Bug fixes from issue text: py-bug-slug, py-bug-cron, ts-bug-duration. Refactors: py-ref-invoice, py-ref-idgen. Add tests to an untested module: py-test-wordstats, ts-test-csv (graded by how many hidden seeded bugs the agent's tests catch).

## Mutation testing
A small in-house mutator (Python AST for .py, line-level operator swaps for .ts), scoped to the source lines the agent changed (all module lines for the test-writing tasks), at most 40 valid mutants per run, run against only the tests the agent wrote or edited. Equivalent mutants are not filtered out, so scores are comparable between arms but not absolute.

## Usage
    python3 verify_task.py && python3 verify_mutants.py
    python3 run_outcome.py --work /path/to/scratch --reps 3 --cap 45
    python3 aggregate.py /path/to/scratch/runs --md results/summary.md
