# Changelog

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
