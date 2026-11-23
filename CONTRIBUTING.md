# Contributing to fox-dev

fox-dev is free and open source under the MIT license. Issues and pull requests are welcome.

## Reporting a problem
Open an issue with the prompt you gave, the skill you expected, and the skill that fired (or that none did). Transcripts help; remove anything private first.

## Changing or adding a skill
- Keep the set small. Extend an existing skill before adding a new one.
- A new or changed description must pass the firing eval in `evals/`: the right skill fires on its cases, and nothing fires on the controls and negatives. Include the results in the pull request.
- Text derived from another project needs its license allowing it and an entry in both copies of `NOTICE.md`.
- Run `bash scripts/check.sh` and `claude plugin validate ./plugin` before opening the pull request.
