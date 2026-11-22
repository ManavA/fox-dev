# Outcome eval: per-arm results
117 graded runs. Means over runs.

| metric | none | current | foxdev |
|---|---|---|---|
| runs | 39 | 39 | 39 |
| all tests pass (hidden+existing), share of runs | 1.000 | 1.000 | 0.974 |
| hidden-test pass fraction (mean) | 1.000 | 1.000 | 0.999 |
| existing suite pass fraction | 1.000 | 1.000 | 1.000 |
| wrote tests, share of runs | 1.000 | 1.000 | 1.000 |
| tests added (count, mean) | 13.92 | 14.90 | 14.90 |
| changed-line coverage by own tests | 0.954 | 0.958 | 0.955 |
| mutation score of own tests on changed code | 0.844 | 0.835 | 0.838 |
| new lint+type errors (mean) | 0.15 | 0.38 | 0.18 |
| src diff size vs reference (mean) | 1.19 | 1.25 | 1.21 |
| files touched outside scope (mean) | 0.00 | 0.00 | 0.00 |
| judge correctness | 4.69 | 4.77 | 4.62 |
| judge readability | 4.26 | 4.13 | 4.15 |
| judge design | 4.44 | 4.38 | 4.23 |
| judge test quality | 3.95 | 3.97 | 3.95 |
| wall seconds | 24.16 | 24.48 | 24.11 |
| turns | 5.28 | 4.97 | 4.92 |
| cost USD | 0.07 | 0.09 | 0.08 |
| output tokens | 3212.23 | 3290.21 | 3241.85 |
| tests before impl (where detectable) | 0.04 | 0.11 | 0.00 |
| ran tests after last edit | 0.87 | 0.87 | 0.87 |
| Skill calls per run | 0.00 | 0.00 | 0.00 |
| subagents per run | 0.00 | 0.00 | 0.00 |

## Paired differences (mean over tasks, 95% bootstrap CI over tasks)

| metric | foxdev - current | foxdev - none | current - none |
|---|---|---|---|
| all tests pass (hidden+existing), share of runs | -0.026 [-0.077, +0.000] | -0.026 [-0.077, +0.000] | +0.000 [+0.000, +0.000] |
| hidden-test pass fraction (mean) | -0.001 [-0.003, +0.000] | -0.001 [-0.003, +0.000] | +0.000 [+0.000, +0.000] |
| existing suite pass fraction | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| wrote tests, share of runs | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| tests added (count, mean) | +0.000 [-0.692, +0.821] | +0.974 [+0.026, +2.538] | +0.974 [+0.179, +2.103] |
| changed-line coverage by own tests | -0.003 [-0.011, +0.003] | +0.001 [-0.005, +0.008] | +0.004 [-0.004, +0.014] |
| mutation score of own tests on changed code | +0.003 [-0.022, +0.028] | -0.006 [-0.034, +0.018] | -0.009 [-0.031, +0.014] |
| new lint+type errors (mean) | -0.205 [-0.513, +0.000] | +0.026 [-0.179, +0.308] | +0.231 [-0.128, +0.769] |
| src diff size vs reference (mean) | -0.046 [-0.081, -0.010] | +0.016 [-0.037, +0.084] | +0.062 [+0.027, +0.104] |
| files touched outside scope (mean) | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| judge correctness | -0.154 [-0.333, -0.026] | -0.077 [-0.333, +0.103] | +0.077 [-0.026, +0.179] |
| judge readability | +0.026 [-0.128, +0.179] | -0.103 [-0.256, +0.051] | -0.128 [-0.308, +0.051] |
| judge design | -0.154 [-0.385, +0.077] | -0.205 [-0.436, +0.026] | -0.051 [-0.256, +0.154] |
| judge test quality | -0.026 [-0.128, +0.077] | -0.000 [-0.103, +0.103] | +0.026 [-0.077, +0.154] |
| wall seconds | -0.374 [-1.790, +0.979] | -0.054 [-1.533, +1.356] | +0.321 [-0.756, +1.344] |
| turns | -0.051 [-0.564, +0.410] | -0.359 [-1.051, +0.205] | -0.308 [-0.667, +0.026] |
| cost USD | -0.009 [-0.013, -0.005] | +0.004 [+0.001, +0.008] | +0.013 [+0.010, +0.016] |
| output tokens | -48.359 [-268.256, +152.872] | +29.615 [-163.026, +222.308] | +77.974 [-97.487, +259.179] |
| tests before impl (where detectable) | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| ran tests after last edit | +0.000 [-0.103, +0.103] | +0.000 [-0.077, +0.077] | +0.000 [-0.103, +0.103] |
| Skill calls per run | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |
| subagents per run | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] | +0.000 [+0.000, +0.000] |

## Per task (hidden pass / mutation / cost / judge-mean), none | current | foxdev

- py-bug-cron (bugfix): 1.00 / 0.79 / $0.056 / 4.2 | 1.00 / 0.81 / $0.063 / 4.2 | 1.00 / 0.78 / $0.064 / 4.2
- py-bug-slug (bugfix): 1.00 / 0.91 / $0.060 / 4.2 | 1.00 / 0.81 / $0.066 / 4.1 | 1.00 / 0.92 / $0.048 / 3.8
- py-feat-table (feature): 1.00 / 0.95 / $0.067 / 4.2 | 1.00 / 0.97 / $0.074 / 4.5 | 1.00 / 0.97 / $0.071 / 4.3
- py-feat-ttl (feature): 1.00 / 0.89 / $0.072 / 4.4 | 1.00 / 0.85 / $0.097 / 4.4 | 1.00 / 0.83 / $0.072 / 4.2
- py-hard-bug-ledger (bugfix): 1.00 / 0.88 / $0.059 / 4.3 | 1.00 / 0.89 / $0.077 / 4.2 | 1.00 / 0.89 / $0.067 / 4.4
- py-hard-feat-expr (feature): 1.00 / 0.82 / $0.096 / 4.2 | 1.00 / 0.81 / $0.112 / 4.2 | 0.99 / 0.86 / $0.101 / 3.8
- py-ref-idgen (refactor): 1.00 / 0.68 / $0.053 / 4.8 | 1.00 / 0.70 / $0.067 / 4.7 | 1.00 / 0.63 / $0.058 / 4.6
- py-ref-invoice (refactor): 1.00 / 0.46 / $0.067 / 4.4 | 1.00 / 0.54 / $0.083 / 4.3 | 1.00 / 0.54 / $0.075 / 4.6
- py-test-wordstats (tests): 1.00 / 0.91 / $0.082 / 4.4 | 1.00 / 0.91 / $0.096 / 4.7 | 1.00 / 0.91 / $0.097 / 4.3
- ts-bug-duration (bugfix): 1.00 / 1.00 / $0.053 / 4.2 | 1.00 / 0.95 / $0.071 / 4.3 | 1.00 / 1.00 / $0.062 / 4.2
- ts-feat-range (feature): 1.00 / 0.81 / $0.107 / 4.2 | 1.00 / 0.76 / $0.113 / 4.1 | 1.00 / 0.68 / $0.109 / 3.9
- ts-hard-feat-memo (feature): 1.00 / 0.88 / $0.090 / 4.2 | 1.00 / 0.86 / $0.104 / 4.2 | 1.00 / 0.87 / $0.097 / 4.3
- ts-test-csv (tests): 1.00 / 1.00 / $0.097 / 4.6 | 1.00 / 1.00 / $0.106 / 4.2 | 1.00 / 1.00 / $0.097 / 4.2
