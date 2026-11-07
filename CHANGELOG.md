# Changelog

## v1.1.0 (2026-11-07)

### Commits since v1.0.0

- 28fdbb0 docs(docs): name revision 4.0.0 and its exceptions in the README
- cc3c2b5 ci(ci): add the five lab workflows and the issue and pull request templates
- b60117e chore(core): add the AI environment, its hooks and the lab-ai-env skill
- e47c5cd docs(docs): add the README, licence, rules and manual
- e741584 build(build): add recipe.ps1 and the test suites it runs
- c69c5f9 refactor(core): settle the sources under the pinned ruff and mypy
- 0b309e9 build(build): pin the toolchain, and decide line endings and ignores
- 6fa1e22 chore: add the pre-push check that mirrors CI
- c16ae54 fix(ci): unescape the quotes in the tag guard
- 465f853 fix(ci): make Run workflow work instead of failing
- 2852b0f docs: remove the course brief - it is the course's text, not this project's
- cebb7d8 chore: add the pre-push check that mirrors CI
- 9f6e218 chore: add the pre-push check that mirrors CI
- 4f59921 feat: benchmark the pipeline around the model
- 9a8f98b chore: add the pre-push check that mirrors CI
- d4071b4 chore: add the pre-push check that mirrors CI
- 8000d9e chore: add the pre-push check that mirrors CI
- 62ef999 chore: add the pre-push check that mirrors CI
- 29794c3 fix: type the quality metrics script for mypy --strict

### Issues

- #1 Pin the toolchain, and decide line endings and ignores in swin-transformer (open)
- #2 Bring the sources of swin-transformer under the pinned tools (open)
- #3 Add recipe.ps1 and its test suites to swin-transformer (open)
- #4 Add the README, licence, rules and manual to swin-transformer (open)
- #5 Add the AI environment to swin-transformer (open)
- #6 Add the gates and templates to swin-transformer (open)
- #7 State the revision 4.0.0 compliance line in swin-transformer (open)

### Pull requests

- #13 build(build): pin the toolchain, and decide line endings and ignores (closed)
- #14 refactor(core): settle the sources under the pinned ruff and mypy (closed)
- #15 build(build): add recipe.ps1 and the test suites it runs (closed)
- #16 docs(docs): add the README, licence, rules and manual (closed)
- #17 chore(core): add the AI environment, its hooks and the lab-ai-env skill (closed)
- #18 ci(ci): add the five lab workflows and the issue and pull request templates (closed)
- #19 docs(docs): name revision 4.0.0 and its exceptions in the README (closed)

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.0.0] - 2026-08-05

Brought up to the project quality standard. The classifier itself is unchanged;
what changed is everything around it.

### Fixed

- **CI had been failing on every push.** `python-ci.yml` ran `uv sync --dev`
  against a `pyproject.toml` that did not exist in the repository. Replaced with
  a workflow that matches the actual layout.
- `pyproject.toml` added: dependencies, entry point, and configuration for
  ruff, mypy, pytest and coverage in one place.
- `swin_classifier.main.main()` added, so the declared `swin-classify` console
  script resolves to something real.

### Added

- **Tests for the application layer.** `ClassifyImageService` — the
  load-then-classify sequence and both of its failure branches — had no
  coverage at all. Branch coverage went from **53% to 95%**, with the build now
  failing below 90%.
- Tests for the filesystem adapter's success path, greyscale conversion, and
  the not-an-image and directory failures.
- Tests for the CLI shell, including both non-zero exit paths.
- `docs/architecture.md` — the ports-and-adapters layout, why errors are values,
  and what was deliberately left out.
- `docs/quality-iso25010.md` — assessment against all eight characteristics,
  with the four measurable ones cited from CI and the gaps stated rather than
  glossed over.
- `docs/screenshots/cli-output.png` — real output, captured from a real run.
- `SECURITY.md`, `CONTRIBUTING.md`, `docs/branching.md`.
- Release workflow: a `v*.*.*` tag now builds an executable, a zip and a SHA-256
  for each, and publishes a GitHub Release.
- Secret scanning with `gitleaks`, in pre-commit and over full history in CI.
- Helper scripts: dependency install, release build, quality metrics, profiling,
  branch policy.

### Changed

- Branch layout is now exactly `release`, `dev` and `test`; CI fails if a fourth
  appears.
- `.agent/`, `workflow_prompts/`, `docs/api/` and `scratch/` are excluded from
  linting and coverage — they are vendored tooling and generated output, not
  this project's code, and including them made the quality numbers meaningless.

[Unreleased]: https://github.com/IGORSVOLOHOVS/swin-transformer/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/IGORSVOLOHOVS/swin-transformer/releases/tag/v1.0.0
