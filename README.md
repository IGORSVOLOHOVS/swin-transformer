# swin-transformer

A console tool that classifies an image with the Swin Transformer (`microsoft/swin-tiny-patch4-window7-224`) on the CPU. It prints the five most likely ImageNet-1k labels with their scores and names the winner.

The code is arranged as ports and adapters. The domain knows nothing about HuggingFace, the filesystem or the terminal, and failures travel as `Result` values rather than exceptions. `docs/architecture.md` explains the design and its trade-offs.

## Use

```powershell
.\recipe.ps1 run                      # classifies the bundled data/image.png
.\recipe.ps1 run path\to\image.png
```

```text
Processing image: data/image.png
          Top-5 Classification Predictions
┌──────┬──────────────────┬────────┬────────────────┐
│ Rank │ Label            │  Score │ Confidence Bar │
├──────┼──────────────────┼────────┼────────────────┤
│  1   │ ox               │ 0.5758 │ ███████████    │
│  2   │ ram, tup         │ 0.0222 │                │
│  3   │ kuvasz           │ 0.0093 │                │
│  4   │ llama            │ 0.0082 │                │
│  5   │ golden retriever │ 0.0056 │                │
└──────┴──────────────────┴────────┴────────────────┘
Winner: ox (Index: 345)
```

`docs/install.md` says what to install and `docs/manual.md` describes the arguments, the tests and the measurements. `.\recipe.ps1 test` runs the tests, mypy and ruff. It never needs the model: no gate fetches the weights.

## What is here

- `src/swin_classifier/` is the program: `domain/`, `application/`, `infrastructure/`, `result.py` and `main.py`.
- `classify_image.py` starts it from the source tree.
- `tests/` holds the tests. `benchmarks/` measures the work around the model.
- `scripts/` holds the helpers kept from before the lab, among them `collect_quality_metrics.py`.
- `docs/` holds the architecture, the ISO/IEC 25010 assessment, the branch model and the generated API pages in `docs/api/`.
- `.agent/`, `workflow_prompts/` and `scratch/` are agent tooling that came with the repository. They are not this project's code, and nothing measures them.

## Everything around the model

Inference is the model's cost, not this repository's. What a change here can actually make slower is the work surrounding it, measured by `benchmarks/test_pipeline_performance.py` as the median of many rounds on 2026-11-07:

| What is measured | Median |
| --- | ---: |
| Load and decode a 64 x 64 PNG | 127.1 µs |
| Load and decode a 224 x 224 PNG | 606.6 µs |
| Load and decode a 1024 x 1024 PNG | 13.31 ms |
| Missing file, the failure path | 12.6 µs |
| Use case: load and orchestrate, model stubbed | 635.7 µs |

The use case costs about as much as the load it contains, so the layering is not what is slow. Decoding grows with image area, so a 1024 x 1024 input spends about 13 ms before the model sees anything: downscale large inputs first.

`docs/quality-iso25010.md` assesses the project against ISO/IEC 25010, including the gaps.

## Licence

MIT, see `LICENSE`.

## Lab requirements

This repository complies with [revision 4.0.0](http://127.0.0.1:3000/igors-lab/software-requirements/src/tag/v4.0.0/BEST_REQUIREMENTS.md) of the lab requirements, except R-02 (#8), R-09 (#9), R-37 (#10), R-41 (#11), R-42 (#12).
