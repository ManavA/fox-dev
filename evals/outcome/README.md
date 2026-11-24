# Outcome eval: none vs current stack vs fox-dev

Compares three Claude Code skill setups on real software tasks, judged on outcomes (correct code, tests, speed, cost [3]), not on whether a skill fired.

Arms (each run is an isolated [7] `claude -p`, scratch HOME holding only OAuth credentials, `--setting-sources project`, fresh copy of the task repo as cwd, Sonnet at low effort, 60 turns, 1.50 USD cap):
- `none`: no plugins.
- `current`: superpowers 7.0.0 + mattpocock-skills 1.3.1 (`--plugin-dir` from the plugin cache).
- `foxdev`: this repo's `plugin/`.

## Layout
- `tasks/<id>/`: `repo/` (the starting repo with its existing tests), `prompt.txt`, `hidden/` (acceptance tests, applied only at grading [1] [2]), `ref/` (reference solution overlay), `meta.json`, `verified.json`.
- `common.py`, `grade_lib.py`: repo prep, test running, grading (hidden tests, existing suite, coverage of changed lines, mutation score, ruff/mypy/tsc deltas, diff size, process notes from the tool order).
- `run_outcome.py`: driver (runs, grades, one blind Opus judge call per run [4], cost cap [3], halts on rate limits/permission denials).
- `verify_task.py`, `verify_mutants.py`: prove each task is solvable (reference passes hidden tests, baseline does not) [1] [2] and that the test-writing tasks' hidden mutants are killable.
- `aggregate.py`: tables and paired bootstrap differences [5].
- `results/`: per-run grades and diffs, aggregate tables.

## Setup (not committed)
`python3 -m venv pyenv && pyenv/bin/pip install pytest coverage ruff mypy` and `mkdir ts-deps && cd ts-deps && npm init -y && npm i @types/node typescript`. Node 22+ is needed (TypeScript runs through Node's type stripping and `node --test`).

## Tasks (10)
Features: py-feat-ttl, py-feat-table, ts-feat-range. Bug fixes from issue text [1]: py-bug-slug, py-bug-cron, ts-bug-duration. Refactors: py-ref-invoice, py-ref-idgen. Add tests to an untested module: py-test-wordstats, ts-test-csv (graded by how many hidden seeded bugs the agent's tests catch).

## Mutation testing
A small in-house mutator [6] (Python AST for .py, line-level operator swaps for .ts), scoped to the source lines the agent changed (all module lines for the test-writing tasks), at most 40 valid mutants per run, run against only the tests the agent wrote or edited. Equivalent mutants are not filtered out, so scores are comparable between arms but not absolute.

## Usage
    python3 verify_task.py && python3 verify_mutants.py
    python3 run_outcome.py --work /path/to/scratch --reps 3 --cap 45
    python3 aggregate.py /path/to/scratch/runs --md results/summary.md

## References
The eval design follows Stanford CS329Z, Engineering AI Agents (Fall 2026, https://cs329z.stanford.edu/): Lecture 12, Data Selection & Quality (a task counts only when the reference passes and the starting code fails); Lecture 13, Evaluation Fundamentals & Benchmark Design (task validity, isolation, costs and error bars in the report); Lecture 15, LLM-as-Judge & Evaluation Infrastructure (grader types, LLM judges); and Lecture 16, the SWE-bench guest lecture (hidden tests on real repositories).

1. Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., Narasimhan, K. (2023). SWE-bench: Can Language Models Resolve Real-World GitHub Issues? arXiv:2310.06770. https://arxiv.org/abs/2310.06770
2. Zhu, Y., Jin, T., Pruksachatkun, Y., et al. (2025). Establishing Best Practices for Building Rigorous Agentic Benchmarks. arXiv:2507.02825. https://arxiv.org/abs/2507.02825
3. Kapoor, S., Stroebl, B., Siegel, Z. S., Nadgir, N., Narayanan, A. (2024). AI Agents That Matter. arXiv:2407.01502. https://arxiv.org/abs/2407.01502
4. Zheng, L., Chiang, W.-L., Sheng, Y., et al. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. arXiv:2306.05685. https://arxiv.org/abs/2306.05685
5. Efron, B. (1979). Bootstrap Methods: Another Look at the Jackknife. The Annals of Statistics 7(1). https://doi.org/10.1214/aos/1176344552
6. DeMillo, R. A., Lipton, R. J., Sayward, F. G. (1978). Hints on Test Data Selection: Help for the Practicing Programmer. Computer 11(4). https://doi.org/10.1109/C-M.1978.218136
7. Grace, M., Hadfield, J., Olivares, R., De Jonghe, J. (2026). Demystifying evals for AI agents. Anthropic. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
