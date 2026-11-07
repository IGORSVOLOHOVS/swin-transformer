# Quality assessment — ISO/IEC 25010

Assessed against the eight product quality characteristics of ISO/IEC
25010:2011. Four are measured by `scripts/collect_quality_metrics.py`, which
is run by hand; four need judgement and are argued here, citing those numbers
rather than asserting quality.

Numbers below were measured on 2026-11-07. Regenerate with:

```powershell
uv run --frozen python scripts/collect_quality_metrics.py --output quality-report.json
```

---

## 1. Functional suitability — measured

*Does it do what it claims, correctly and completely?*

30 tests pass in every gate. The use case, the filesystem adapter, the `Result`
type and the CLI shell are exercised. One more test, marked `model`, is left out
of the gates.

The claim that matters is the one in the README — "classifies an image with
Swin-Tiny" — and it is checked end to end only by `tests/test_perf.py`, which
runs the real model on a generated image and asserts the result is a success.
No gate runs it, because no gate may fetch weights: `addopts` deselects the
`model` marker, and `tests/conftest.py` sets `HF_HUB_OFFLINE` as a second lock.
It passed by hand on 2026-11-07 under the pins in `uv.lock`, and `data/image.png`
still came out as `ox` at 0.5758.

**Gap:** there is no test that the labels themselves are correct. The adapter is
trusted to map HuggingFace's `id2label` faithfully; a silent off-by-one there
would pass every test in this suite.

## 2. Performance efficiency — assessed, with measurements

*Time behaviour, resource use, capacity.*

`benchmarks/test_pipeline_performance.py` measures everything the pipeline does
*around* the model — the part a change to this repository can actually make
slower. Measured on HOME i9:

| Operation | Median |
| --- | --- |
| Load a 64 × 64 PNG | 127.1 µs |
| Load a 224 × 224 PNG | 606.6 µs |
| Load a 1024 × 1024 PNG | 13.31 ms |
| Missing file (failure path) | 12.6 µs |
| Use case: load + orchestrate, model stubbed | 635.7 µs |

Two things fall out of those numbers. The use case measures at 636 µs against
607 µs for the load it contains — the two are within run-to-run noise of each
other, which is the finding: the layering (ports, Result objects, the service
indirection) costs less than the variance of decoding a PNG. **The architecture
is not what is slow.** And decoding is linear in image area, so a 1024 × 1024
input spends ~13 ms before the model starts; callers feeding large images should
downscale first.

The failure path costs 12.6 µs, about fifty times less than a successful load: a
missing file is a `Path.exists()` check, not an exception unwind.

`tests/test_perf.py` also times inference end to end and fails above 1000 ms.
That is a guard rail rather than a measurement — one `perf_counter` call, no
warm-up, no repetitions — and it covers the model, which these benchmarks
deliberately exclude because loading weights would measure the network. It
measured 55 ms in one sample on 2026-11-07.
`scripts/profile_application.py` is a leftover of the template: it imports a
package this repository does not have, so it does not run.

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

The lab's runner is Windows, where the pinned `torch` is the CPU build, so the
project does not fight over a CUDA runtime with anything else on that machine.
On Linux the same `uv.lock` brings the CUDA build.

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

**Coverage: 83.33%** of statements and branches, with the build failing below 83
(`--cov-fail-under` in `pyproject.toml`).

The earlier figure of 95% counted `tests/test_perf.py`, which loads the real
weights. The gates no longer run it and nothing was omitted from the measurement,
so the gap shows: `infrastructure/hf_adapter.py` measures 28%, because its model
path runs only with weights. Everything else is at 85% or above.

The figure was **53%** once, when `ClassifyImageService` — the load-then-classify
sequence and both of its failure branches — had **zero** direct coverage.

Failures are values, not exceptions: every port returns `Result[..., Exception]`,
and `tests/test_use_case.py` asserts the property that actually matters — a
failed image load never reaches the model.

**Known limits:** no fuzzing, no property-based tests, and no test that the
model's label mapping is right.

## 6. Security — assessed

*Confidentiality, integrity, accountability.*

| Control | Where |
| --- | --- |
| Secret scanning over full history | `gitleaks`, on GitHub's copy only: no gate on this server runs a scanner |
| Static security linting | `ruff` rule set `S` (bandit rules), in `recipe.ps1 test` |
| No credential in source | nothing here authenticates to anything |
| Pinned dependencies | `uv.lock`, read with `uv run --frozen` |
| What a release was made of | the SBOM `release.yaml` attaches to every release |

The program reads an image and prints numbers. It evaluates nothing, unpickles
nothing and runs no subprocess on user input.

**Real risk, stated:** `transformers` downloads and executes model code from the
HuggingFace hub. The pin is a model *name*, not a hash, so a compromised upstream
repository would be trusted. Pinning a revision SHA in `hf_adapter.py` would fix
this and has not been done.

## 7. Maintainability — measured

*Modularity, analysability, modifiability, testability.*

- **Average cyclomatic complexity: A (1.78)** across 27 analysed blocks.
- **Maintainability index: A** on every module (67–100, 94.9 on average).
- **Outstanding lint findings: 0**, with `ruff` enforcing a complexity ceiling
  of 10 and `mypy --strict` over `src/` and `tools/`, with an empty silence list.

The layering is what makes the test suite short: because the use case depends on
Protocols, `tests/test_use_case.py` needs no model, no network and no files —
two twelve-line fakes are enough.

## 8. Portability — measured

*Adaptability, installability, replaceability.*

The lab's gates run on one Windows runner with Python 3.13, the one version
`requires-python` allows, which is why this characteristic scores 50. Installation
is one command, `uv sync --frozen`.

Replaceability is the strongest point here: swapping HuggingFace for ONNX
Runtime or a remote inference API means one new class in `infrastructure/` and
one changed line in `main.py`. Nothing in `domain/` or `application/` would move.

**Known limit:** no gate runs on Linux or macOS, so neither is tested here.

---

## How to read the score

The overall figure reported by the metrics script is the mean of the four
**measured** characteristics only. Averaging a coverage percentage with a
hand-written opinion about usability would produce a number that looks objective
and is not.
