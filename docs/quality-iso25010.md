# Quality assessment — ISO/IEC 25010

Assessed against the eight product quality characteristics of ISO/IEC
25010:2011. Four are measured by `scripts/collect_quality_metrics.py`, which
runs in CI; four need judgement and are argued here, citing those numbers rather
than asserting quality.

Numbers below were measured on 2026-08-05. Regenerate with:

```bash
python scripts/collect_quality_metrics.py --output quality-report.json
```

---

## 1. Functional suitability — measured

*Does it do what it claims, correctly and completely?*

29 tests, all passing. Every port, both adapters, the use case, the `Result`
type and the CLI shell are exercised.

The claim that matters is the one in the README — "classifies an image with
Swin-Tiny" — and it is checked end to end by `tests/test_perf.py`, which runs a
real model against a real image and asserts the result is a success.

**Gap:** there is no test that the labels themselves are correct. The adapter is
trusted to map HuggingFace's `id2label` faithfully; a silent off-by-one there
would pass every test in this suite.

## 2. Performance efficiency — assessed, with measurements

*Time behaviour, resource use, capacity.*

`benchmarks/test_pipeline_performance.py` measures everything the pipeline does
*around* the model — the part a change to this repository can actually make
slower. Measured on this machine:

| Operation | Median |
| --- | --- |
| Load a 64 × 64 PNG | 119 µs |
| Load a 224 × 224 PNG | 631 µs |
| Load a 1024 × 1024 PNG | 14.0 ms |
| Missing file (failure path) | 12.9 µs |
| Use case: load + orchestrate, model stubbed | 643 µs |

Two things fall out of those numbers. The use case costs 643 µs against 631 µs
for the load alone, so the layering — ports, Result objects, the service
indirection — adds about **2 %**; the architecture is not what is slow.
And decoding is linear in image area, so a 1024 × 1024 input spends 14 ms
before the model starts. Callers feeding large images should downscale first.

The failure path costs 12.9 µs, fifty times less than a successful load: a
missing file is a `Path.exists()` check, not an exception unwind.

`tests/test_perf.py` also times inference end to end and fails above 1000 ms.
That is a guard rail rather than a measurement — one `perf_counter` call, no
warm-up, no repetitions — and it covers the model, which these benchmarks
deliberately exclude because loading weights would measure the network.
`scripts/profile_application.py` attributes time to individual functions when a
number moves.

Swin-Tiny computes attention inside shifted local windows instead of across the
whole image, which is the architectural reason CPU inference is viable at all.

**Known limits:** one image per call, no batching, and the model is reloaded on
every process start (~110 MB from cache). For a CLI invoked occasionally that is
the right trade; for a service it would not be.

## 3. Compatibility — assessed

*Co-existence and interoperability.*

The package writes nothing outside paths it is given, holds no global state, and
opens no port. Its only external dependency at runtime is the HuggingFace cache
directory, which is shared with every other tool on the machine by design.

CI installs CPU-only torch wheels explicitly, so the project does not fight over
a CUDA runtime with anything else on the same machine.

## 4. Usability — assessed

*Learnability, operability, error protection.*

| Sub-characteristic | How it is addressed |
| --- | --- |
| Appropriateness recognisability | README opens with a screenshot of real output |
| Learnability | One command, one optional argument |
| Operability | `swin-classify path/to/image.png`, or no argument for the bundled sample |
| User error protection | A missing file, a non-image file and a directory all return a stated failure, not a traceback — see `tests/test_image_loader.py` |
| User interface aesthetics | `rich` table with confidence bars and a highlighted winner |

**Weakest area:** the output is English ImageNet-1k class names with no
explanation that the label set is fixed at 1000 categories. A user classifying a
photo of something outside those categories gets a confident wrong answer with
no hint that the vocabulary was the problem.

## 5. Reliability — measured

*Maturity, fault tolerance, recoverability.*

**Branch coverage: 95%**, with the build failing below 90%
(`fail_under` in `pyproject.toml`).

That figure is recent. Before this pass it was **53%**, and the untested part
was the worst possible one: `ClassifyImageService` — the load-then-classify
sequence and both of its failure branches — had **zero** coverage. It was
covered only indirectly by a test that needs a real model download, so any CI
run without network would have proved nothing about it.

Failures are values, not exceptions: every port returns `Result[..., Exception]`,
and `tests/test_use_case.py` asserts the property that actually matters — a
failed image load never reaches the model.

**Known limits:** no fuzzing, no property-based tests, and no test that the
model's label mapping is right.

## 6. Security — assessed

*Confidentiality, integrity, accountability.*

| Control | Where |
| --- | --- |
| Secret scanning over full history | `gitleaks` job in CI, `fetch-depth: 0` |
| Secret scanning before commit | `gitleaks` in `.pre-commit-config.yaml` |
| Static security linting | `ruff` rule set `S` (bandit rules) |
| No credential in source | nothing here authenticates to anything |
| Artefact integrity | `.sha256` beside every release file |

The program reads an image and prints numbers. It evaluates nothing, unpickles
nothing and runs no subprocess on user input.

**Real risk, stated:** `transformers` downloads and executes model code from the
HuggingFace hub. The pin is a model *name*, not a hash, so a compromised upstream
repository would be trusted. Pinning a revision SHA in `hf_adapter.py` would fix
this and has not been done.

## 7. Maintainability — measured

*Modularity, analysability, modifiability, testability.*

- **Average cyclomatic complexity: A (1.78)** across 27 analysed blocks.
- **Maintainability index: A** on every module (92–100).
- **Outstanding lint findings: 0**, with `ruff` enforcing a complexity ceiling
  of 10 and `mypy --strict` over `src/`.

The layering is what makes the test suite short: because the use case depends on
Protocols, `tests/test_use_case.py` needs no model, no network and no files —
two twelve-line fakes are enough.

## 8. Portability — measured

*Adaptability, installability, replaceability.*

CI runs on Ubuntu and Windows across Python 3.10 and 3.12. Installation is one
command (`pip install -e .`), and `scripts/install_dependencies.py` wraps it.

Replaceability is the strongest point here: swapping HuggingFace for ONNX
Runtime or a remote inference API means one new class in `infrastructure/` and
one changed line in `main.py`. Nothing in `domain/` or `application/` would move.

**Known limit:** macOS is not in the CI matrix, so macOS support is untested.

---

## How to read the score

The overall figure reported by the metrics script is the mean of the four
**measured** characteristics only. Averaging a coverage percentage with a
hand-written opinion about usability would produce a number that looks objective
and is not.
