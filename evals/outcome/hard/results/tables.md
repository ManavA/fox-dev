| task | arm | run | hidden | existing regressions | clippy | fmt | judge c/r/d/t | tests added | cost | wall s | turns | skills fired | subagents | tests first |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| c-typedef | none | r1 | 4/4 | 0 | ok | ok | 4/3/3/4 | 2 | 0.72 | 829 | 35 | - | 0 | None |
| c-typedef | none | r2 | 4/4 | 0 | ok | ok | 4/3/3/4 | 1 | 0.74 | 582 | 35 | - | 0 | None |
| c-typedef | current | r1 | 4/4 | 0 | ok | ok | 4/3/3/5 | 3 | 1.04 | 1246 | 40 | - | 0 | None |
| c-typedef | current | r2 | 4/4 | 0 | ok | ok | 4/3/4/4 | 2 | 1.10 | 587 | 43 | - | 0 | None |
| c-typedef | foxdev | r1 | 4/4 | 0 | ok | ok | 4/3/4/4 | 2 | 0.68 | 1014 | 31 | - | 0 | None |
| c-typedef | foxdev | r2 | 4/4 | 0 | ok | ok | 4/3/3/4 | 2 | 0.73 | 690 | 29 | - | 0 | None |
| cpp-recv | none | r1 | 5/5 | 0 | ok | ok | 4/3/3/4 | 4 | 1.96 | 1499 | 62 | - | 0 | None |
| cpp-recv | none | r2 | 5/5 | 0 | ok | ok | 4/3/3/4 | 3 | 1.61 | 991 | 46 | - | 0 | None |
| cpp-recv | current | r1 | 5/5 | 0 | ok | ok | 4/3/4/4 | 2 | 1.39 | 1030 | 38 | - | 0 | None |
| cpp-recv | current | r2 | 5/5 | 0 | ok | ok | 4/3/3/4 | 3 | 1.96 | 2294 | 1 | - | 0 | None |
| cpp-recv | foxdev | r1 | 5/5 | 0 | ok | ok | 4/3/3/3 | 3 | 1.79 | 1627 | 56 | - | 0 | None |
| cpp-recv | foxdev | r2 | 5/5 | 0 | ok | ok | 4/3/3/4 | 4 | 2.12 | 1441 | 63 | - | 0 | None |
| py-mro | none | r1 | 5/5 | 0 | ok | ok | 4/3/4/4 | 1 | 0.73 | 650 | 27 | - | 0 | None |
| py-mro | none | r2 | 5/5 | 0 | ok | ok | 4/3/3/4 | 2 | 1.20 | 1216 | 49 | - | 0 | None |
| py-mro | current | r1 | 5/5 | 0 | ok | ok | 4/3/3/4 | 2 | 1.29 | 1463 | 45 | - | 0 | None |
| py-mro | current | r2 | 5/5 | 0 | ok | ok | 4/3/3/4 | 1 | 0.86 | 740 | 32 | superpowers:test-driven-development | 0 | None |
| py-mro | foxdev | r1 | 5/5 | 0 | ok | ok | 4/3/4/4 | 1 | 1.07 | 1957 | 1 | - | 0 | None |
| py-mro | foxdev | r2 | 5/5 | 0 | ok | ok | 4/3/4/4 | 7 | 1.61 | 1229 | 54 | - | 0 | True |

| arm | runs | hidden pass frac | all hidden pass | runs with regression | clippy ok | judge correctness | readability | design | tests | tests added | cost | wall s | turns | skill calls | subagents |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| none | 6 | 1.0 | 6/6 | 0 | 6/6 | 4 | 3 | 3.17 | 4 | 2.17 | 1.16 | 961.27 | 42.33 | 0 | 0 |
| current | 6 | 1.0 | 6/6 | 0 | 6/6 | 4 | 3 | 3.33 | 4.17 | 2.17 | 1.27 | 1226.65 | 33.17 | 0.17 | 0 |
| foxdev | 6 | 1.0 | 6/6 | 0 | 6/6 | 4 | 3 | 3.5 | 3.83 | 3.17 | 1.33 | 1326.58 | 39 | 0 | 0 |
