# Branching

Two branches live long: `release` and `test`.

| Branch | Holds |
| --- | --- |
| `release` | What is published. A merge into it makes the release |
| `test` | What is proven and waiting. Every work branch merges here first |

Work happens on a short branch from `test`, named `st-<issue>/<type>/<slug>`, and reaches `test` through a pull request once `propose / gate` is green. `CONTRIBUTING.md` has the steps. Only the owner merges `test` into `release`.

## What came before

This repository used to keep exactly `release`, `dev` and `test`, and a script failed CI when a fourth branch appeared. That policy, its script and its workflow are gone. The one commit `dev` held that `release` did not is kept under the tag `import/dev`: it put the benchmark numbers in the README and the assessment, and both have since been measured again.
